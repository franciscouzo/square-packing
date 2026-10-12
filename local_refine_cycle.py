#!/usr/bin/env python3
"""Local experiments: Ellsworth refinement, repacking, search, and LP.

Runs the unmodified upstream executable. Its output is an experimental seed,
never a certificate. The coordinator remains the only writer of records.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import time

import numpy as np
from slp_refine import load, refine, repair, save, wrap

UPSTREAM_COMMIT = "79f8a378d52e757d70f7cfb2c2f7a24a53da0204"
MODES = [["--snap-grid", "0.001", "0.01"], ["--snap-grid", "0.01", "0.1"],
         ["--shift", "N"], ["--shift", "E"], ["--shift", "S"], ["--shift", "W"], []]
NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?"
ROW = re.compile(rf"^Square\s+(\d+):\s*x=({NUMBER}),\s*y=({NUMBER}),\s*deg=({NUMBER})\s*$")


def export_ellsworth(z, path):
    z, side = wrap(z)
    with path.open("w") as f:
        f.write(f"Final s: {side:.20f}\n\n")
        for i, (x, y, theta) in enumerate(z, 1):
            f.write(f"Square {i}: x={x-side/2:.20f}, y={y-side/2:.20f}, deg={math.degrees(theta):.20f}\n")


def import_ellsworth(path, expected_n):
    rows = []
    ids = set()
    for line in path.read_text().splitlines():
        if not line.startswith("Square"):
            continue
        match = ROW.fullmatch(line)
        if not match or int(match[1]) in ids:
            raise ValueError("Malformed or duplicate square in Ellsworth output")
        ids.add(int(match[1]))
        rows.append([float(match[2]), float(match[3]), math.radians(float(match[4]))])
    z = np.array(rows)
    if len(z) != expected_n or not np.isfinite(z).all():
        raise ValueError("Invalid square count or non-finite Ellsworth output")
    return repair(z)


def run_cycle(root, job):
    start = time.monotonic()
    n = job["n"]
    base = root/"experiments/local-cycles"
    base.mkdir(parents=True, exist_ok=True)
    wd = base/f"job-{job['id']}"
    wd.mkdir(exist_ok=False)
    binary = root/"target/release/sqpack"
    upstream = root/"external/ellsworth/refine_packing"
    if not upstream.exists():
        raise FileNotFoundError("Build external/ellsworth/refine_packing before starting local cycles")
    seed = wd/"input.txt"
    seed.write_text(job["packing"])
    shutil.copy2(root/"records.txt", wd/"records.txt")
    z = load(seed)
    if len(z) != n:
        raise ValueError("Local cycle needs a seed with the target square count")
    if job.get("constructed_seed") is not None or job.get("repair_seed"):
        # Imported poses and new touching border rows can carry tiny float
        # overlaps. The retained incumbent must pass the same all-pairs check
        # as every later stage, even if optimization never improves it.
        z, incumbent = repair(z)
        save(seed, z, incumbent)
    else:
        _, incumbent = wrap(z)
    best, best_side = z.copy(), incumbent
    cycle = job.get("local_cycle", job["id"])
    options = MODES[cycle % len(MODES)]
    stages = []
    details = {"actual_method": "ellsworth_cycle", "upstream_commit": UPSTREAM_COMMIT,
               "upstream_source_sha256": hashlib.sha256(upstream.with_suffix('.cpp').read_bytes()).hexdigest(),
               "upstream_binary_sha256": hashlib.sha256(upstream.read_bytes()).hexdigest(),
               "cycle_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "rust_binary_sha256": hashlib.sha256(binary.read_bytes()).hexdigest(),
               "refiner_sha256": hashlib.sha256((root/'slp_refine.py').read_bytes()).hexdigest(),
               "precision_digits": 40, "ellsworth_options": options,
               "stages": stages, "experiment": str(wd.relative_to(root))}
    (wd/"job.json").write_text(json.dumps({k:v for k,v in job.items() if k != 'packing'}, indent=2)+"\n")

    def run(name, command, seconds):
        t = time.monotonic()
        stage = {"name": name, "command": list(map(str, command)), "budget": seconds}
        with (wd/f"{name}.log").open("w") as log:
            process = subprocess.Popen(command, cwd=wd, stdout=log, stderr=subprocess.STDOUT,
                                       start_new_session=True)
            try:
                process.wait(timeout=max(.1, seconds))
                stage["status"] = "ok" if process.returncode == 0 else "failed"
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
                stage["status"] = "timeout"
        stage.update({"returncode": process.returncode, "seconds": time.monotonic()-t})
        stages.append(stage)
        return stage["status"] == "ok"

    candidates = [("incumbent", z.copy())]
    experimental = z.copy()
    ell_in, ell_out = wd/"ellsworth-input.txt", wd/"ellsworth-output.txt"
    export_ellsworth(z, ell_in)
    command = [str(upstream), str(ell_in), "40", str(ell_out), *options]
    complete = run("ellsworth", command, job.get("ellsworth_seconds", 45))
    if not complete:
        # Preserve snapped/shifted poses even if arbitrary-precision nudging
        # takes too long; our CPU solvers can repair those experimental starts.
        ell_out.unlink(missing_ok=True)
        complete = run("ellsworth-export", [*command, "--no-fix"], 10)
    if complete and ell_out.exists():
        try:
            trial, side = import_ellsworth(ell_out, n)
            details["after_ellsworth"] = side
            if side <= incumbent+.1:
                experimental = trial
                candidates.append(("ellsworth", trial.copy()))
        except ValueError as exc:
            details["ellsworth_output_error"] = str(exc)
    packed = wd/"packed.txt"
    _, side = wrap(experimental)
    save(packed, experimental, side)
    contact_before = int(subprocess.check_output([str(binary), "contacts", str(seed)], text=True))
    compact_start = time.monotonic()
    compact_seconds = job.get("compact_seconds", 30)
    schedule = 1+job["seed"] % 10
    details["settle_schedule"] = schedule
    for name, args in (("settle", ["--outward", "--schedule", str(schedule), "--snap", "1"]),
                       ("flatten", ["--tol", "1"])):
        remaining = compact_seconds-(time.monotonic()-compact_start)
        if remaining <= .1:
            break
        target = wd/f"{name}.txt"
        if run(name, [str(binary), name, str(packed), *args, "--out", str(target)], remaining):
            try:
                trial, side = repair(load(target))
                if len(trial) == n and side <= incumbent+.1:
                    experimental = trial
                    save(packed, trial, side)
            except ValueError as exc:
                details.setdefault("compaction_errors", []).append(str(exc))
    candidates.append(("packed", experimental.copy()))
    details["contacts_before"] = contact_before
    details["contacts_after"] = int(subprocess.check_output([str(binary), "contacts", str(packed)], text=True))
    details["after_packing"] = wrap(experimental)[1]
    run("search", [str(binary), "search", str(n), "--init", str(packed), "--local",
                    "--time", str(job['hop_seconds']), "--threads", "1", "--seed", str(job['seed']),
                    "--pool", "6", "--pool-gap", "0.02"], job['hop_seconds']+45)
    result = wd/"results"/f"n{n}.txt"
    if result.exists():
        candidates.append(("search-best", load(result)))
    candidates.extend((p.stem, load(p)) for p in sorted((wd/"pool").glob(f"n{n}_*.txt")))
    polish_start = time.monotonic()
    rng = np.random.default_rng(job["seed"])
    outcomes = []
    iterations = 0
    for index, (name, source) in enumerate(candidates):
        remaining = job["slp_seconds"]-(time.monotonic()-polish_start)
        if remaining <= .1:
            break
        source, before = repair(source)
        # Keep a valid improvement found before LP even if LP times out.
        if before < best_side:
            best, best_side = source.copy(), before
            details["winner"] = name
        source = source[rng.permutation(n)]
        corrected = (cycle+index) % 2 == 0
        trial, side, history = refine(source, iterations=1000, radius=job["radius"],
            seconds=remaining/(len(candidates)-index), translations=corrected)
        outcomes.append({"name": name, "before": before, "after": side, "translations": corrected})
        iterations += len(history)
        if side < best_side:
            best, best_side = trial, side
            details["winner"] = name
    details["refinement_candidates"] = outcomes
    output = wd/"candidate.txt"
    save(output, best, best_side)
    result = {"id":job["id"], "n":n, "packing":output.read_text(), "side":best_side,
              "before_polish":incumbent, "iterations":iterations,
              "seconds":time.monotonic()-start, "worker_details":details}
    # Keep recent experiments for comparisons; accepted poses/certificates are
    # separately archived by the coordinator and are never pruned here.
    (wd/"summary.json").write_text(json.dumps({k:v for k,v in result.items() if k != 'packing'}, indent=2)+"\n")
    finished = sorted(base.glob("job-*/summary.json"), key=lambda p:p.stat().st_mtime)
    for old in finished[:-250]:
        try:
            shutil.rmtree(old.parent)
        except FileNotFoundError:
            pass
    return result
