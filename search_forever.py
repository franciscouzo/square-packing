#!/usr/bin/env python3
"""Persistent distributed search: local coordinator and one-job SSH workers.

Only the coordinator installs records, after independent exact verification.
Workers use disposable private directories and never write the repository's
records. systemd restarts the coordinator; its job counter survives restarts.
"""
import argparse
import concurrent.futures
from fractions import Fraction
import hashlib
import io
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import random
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import traceback

from expand_search import SEARCH_MAX, PUBLISHED_MAX, construct_seed, targets as expanded_targets
from search_methods import (COMPRESS_MAX_N, below_grid, best_source, graft_seed, load_weights,
                            neighbour_source, old_basin, pick)


HERE = Path(__file__).resolve().parent
FRONTIER = [51, 68, 86, 87, 88, 101, 122, 124, 125, 150, 151, 153,
            178, 179, 205, 207, 229, 235, 269, 270, 296, 298, 299, 300]
PRIORITY = [228, 210, 181, 307, 273, 241, 208, 272, 239, 240, 304, 305,
            306, 303, 271, 263, 238, 180, 236, 103, 102, 152, 268, 209,
            206, 297, 302, 123, 237, 301]


def atomic_json(path, data):
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2) + "\n")
    temp.replace(path)


def gpu_seeds(root, wd, seed, binary, job, details):
    """Generate coarse CUDA candidates; retain the incumbent separately.

    Take the GPU lock without waiting so a busy/missing GPU falls back to CPU
    search. CPU polishing happens after releasing the lock.
    """
    import fcntl
    from slp_refine import load, repair, save

    large = job["n"] > 396
    gpu = root / ("sa_large" if large else "sa")
    if not gpu.exists():
        details["gpu_fallback"] = "CUDA binary unavailable"
        return [], ""
    started = time.monotonic()
    with (root/"gpu.lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            details["gpu_fallback"] = "GPU busy"
            return [], ""
        level = (job["id"]//23) % 3
        parameters = {"blocks": 512 if large else 256, "sweeps": 5000, "keep": 8,
                      "perturb": [.003, .01, .04][level],
                      "temp": [.0002, .0005, .002][level],
                      "mu0": [1000, 200, 50][level], "mu1": 10000000,
                      "seed": job["seed"]}
        parameters.update(job.get("gpu_parameters", {}))
        details["gpu_parameters"] = parameters
        details["gpu_binary_sha256"] = hashlib.sha256(gpu.read_bytes()).hexdigest()
        command = [str(gpu), "--in", str(seed), "--out", str(wd/"gpu")]
        for key, value in parameters.items():
            command += ["--"+key, str(value)]
        try:
            process = subprocess.run(command, cwd=wd, capture_output=True, text=True,
                                     check=True, timeout=min(120, job["hop_seconds"]))
        except (subprocess.SubprocessError, OSError) as exc:
            details["gpu_fallback"] = str(exc)
            return [], ""
    trace = (process.stdout+process.stderr)[-8000:]
    candidates = []
    for path in sorted(wd.glob("gpu.*.txt")):
        remaining = job["hop_seconds"]-(time.monotonic()-started)
        if remaining <= 0:
            break
        try:
            z, side = repair(load(path))
            if len(z) != job["n"]:
                raise ValueError("CUDA candidate has the wrong square count")
            save(path, z, side)
            polished = subprocess.run([str(binary), "polish", str(path)], cwd=wd,
                                      capture_output=True, text=True, check=True,
                                      timeout=min(20, remaining))
            trace = (trace+polished.stdout+polished.stderr)[-8000:]
            candidates.append((path.stem, load(path)))
        except (ValueError, subprocess.SubprocessError) as exc:
            details.setdefault("gpu_candidate_errors", []).append(str(exc))
    details["gpu_seconds"] = time.monotonic()-started
    return candidates, trace


def run_worker(root, job):
    if job["method"] == "ellsworth_cycle":
        from local_refine_cycle import run_cycle
        return run_cycle(root, job)
    # Imports stay in the worker: coordinator needs no SciPy runtime.
    import numpy as np
    from slp_refine import load, refine, repair, save, wrap

    start = time.monotonic()
    work = root / "work"
    work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"job-{job['id']}-", dir=work) as directory:
        wd = Path(directory)
        seed = wd / "seed.txt"
        seed.write_text(job["packing"])
        shutil.copy2(root / "records.txt", wd / "records.txt")
        binary = root / "sqpack"
        if not binary.exists():
            binary = root / "target/release/sqpack"
        n = job["n"]
        method = job["method"]
        rng = np.random.default_rng(job["seed"])
        original = load(seed)
        trace = ""
        worker_details = {"translations": job["id"] % 2 == 0,
                          "worker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                          "refiner_sha256": hashlib.sha256((HERE/"slp_refine.py").read_bytes()).hexdigest()}
        pool_size = job.get("pool_size", 6 if job["id"] % 3 != 0 and method not in ("slp", "gpu") else 0)
        worker_details["pool_size"] = pool_size
        # New experimental candidates enter the usual certification pipeline
        # through a worker, preserving the coordinator as the sole writer.
        incoming = root/"inbox"/f"n{n}.txt"
        if len(original) == n and incoming.exists():
            candidate, candidate_side = repair(load(incoming))
            original, original_side = repair(original)
            if len(candidate) == n and candidate_side < original_side:
                original = candidate
                save(seed, original, candidate_side)
                worker_details["inbox_sha256"] = hashlib.sha256(incoming.read_bytes()).hexdigest()
        extra_candidates = []
        if method == "gpu":
            extra_candidates, trace = gpu_seeds(root, wd, seed, binary, job, worker_details)
            if not extra_candidates:
                method = "hop"
                worker_details.setdefault("gpu_fallback", "No usable CUDA candidates")
        worker_details["actual_method"] = method
        if method in ("shrink", "fq", "compress"):
            # Evan Daniel's packer/fq binaries, Ryan Xu's engine (search_methods.run_external).
            from search_methods import run_external
            found, external_details = run_external(method, root, wd, job, seed)
            worker_details.update(external_details)
            found = [(name, np.array(rows)) for name, rows in found]
            if len(original) != n:
                if not found:
                    return {"id": job["id"], "n": n, "packing": None, "trace": json.dumps(external_details),
                            "seconds": time.monotonic()-start, "worker_details": worker_details}
                original = found.pop(0)[1]
            extra_candidates += found
        elif method not in ("slp", "gpu"):
            command = [str(binary), "search", str(n), "--time", str(job["hop_seconds"]),
                       "--threads", "1", "--seed", str(job["seed"])]
            if method != "random":
                command += ["--init", str(seed), "--local"]
            if pool_size:
                command += ["--pool", str(pool_size)]
                if "pool_gap" in job:
                    command += ["--pool-gap", str(job["pool_gap"])]
            process = subprocess.run(command, cwd=wd, text=True, capture_output=True,
                                     timeout=job["hop_seconds"]+120, check=True)
            trace = (process.stdout+process.stderr)[-8000:]
            result = wd / "results" / f"n{n}.txt"
            if result.exists():
                original = load(result)
            elif len(original) != n:
                return {"id": job["id"], "n": n, "packing": None,
                        "trace": trace, "seconds": time.monotonic()-start}
        if len(original) != n:
            raise ValueError("Worker seed/result has the wrong square count")
        original, before = repair(original)
        candidates = [("incumbent", original)]
        candidates += extra_candidates
        candidates += [(p.stem, load(p)) for p in sorted((wd/"pool").glob(f"n{n}_*.txt"))]
        z, side = original, before
        polish_start = time.monotonic()
        if job.get("fq_finish", True):
            from search_methods import fq_finish
            # Search outputs only: the incumbent is already at its minimum.
            finished, fq_details = fq_finish(root, wd, [c for c in candidates if c[0] != "incumbent"],
                                             (.6 if n > 250 else .4)*job["slp_seconds"])
            worker_details.update(fq_details)
            candidates += [(name, np.array(rows)) for name, rows in finished]
        iterations = 0
        details = []
        for index, (name, source) in enumerate(candidates):
            remaining = job["slp_seconds"]-(time.monotonic()-polish_start)
            if remaining <= 0:
                break
            source, source_side = repair(source)
            # Equivalent permutations and square symmetries change degenerate
            # LP choices while preserving the starting geometry.
            trial = source.copy()
            if job["variant"]:
                trial = trial[rng.permutation(n)]
                if rng.integers(2):
                    trial[:, 0] = source_side-trial[:, 0]
                    trial[:, 2] = np.pi-trial[:, 2]
                if rng.integers(2):
                    trial[:, [0, 1]] = trial[:, [1, 0]]
                    trial[:, 2] = np.pi/2-trial[:, 2]
                trial[:, 2] = (trial[:, 2]+np.pi/4) % (np.pi/2)-np.pi/4
            trial, candidate_side, history = refine(trial, iterations=job["iterations"],
                                  radius=job["radius"], seconds=remaining/(len(candidates)-index),
                                  translations=worker_details["translations"])
            iterations += len(history)
            details.append({"name": name, "before": source_side, "after": candidate_side})
            if candidate_side < side:
                z, side = trial, candidate_side
                worker_details["winner"] = name
        worker_details["refinement_candidates"] = details
        output = wd / "candidate.txt"
        save(output, z, side)
        return {"id": job["id"], "n": n, "packing": output.read_text(),
                "side": side, "before_polish": before, "iterations": iterations,
                "seconds": time.monotonic()-start, "trace": trace,
                "worker_details": worker_details}


def notify_record(job, entry):
    """Run an optional local callback; notification code is kept outside Git."""
    try:
        from notify import notify_record as callback
    except ModuleNotFoundError as exc:
        if exc.name != "notify":
            raise
        return
    callback(job, entry)


def seed_credit(cert, job):
    """Credit the author of an external seed in the certificate, as known now.

    A job that started from one of our packings inherits the credit of that
    packing's certificate (matched by the SHA-256 of the packing sent), so an
    improvement of an improvement still names the original construction.
    """
    if "external/seeds/" not in str(job.get("source") or ""):
        for parent in (HERE/"found").glob(f"n{job['n']}_s*.certificate.json"):
            previous = json.loads(parent.read_text())
            if previous.get("sha256") == job.get("source_sha256") and previous.get("seed_credit"):
                cert["seed_credit"] = previous["seed_credit"]
                cert["seed_certificate"] = previous.get("seed_certificate")
                cert["seed_inherited_from"] = parent.name
                return
        return
    known = HERE/"known_best.json"
    entry = json.loads(known.read_text())["entries"].get(str(job["n"]), {}) if known.exists() else {}
    external = entry.get("external")
    if external:
        cert["seed_credit"] = external["credit"]
        cert["seed_certificate"] = {k: external[k] for k in ("source", "certificate", "sha256", "request", "side")}


def dispatch(job, host, remote_root):
    payload = json.dumps({**job, "host": host, "started": time.time()})
    if host == "local":
        command = [str(HERE / ".venv/bin/python"), str(HERE / "search_forever.py"),
                   "worker", "--root", str(HERE)]
    else:
        import shlex
        # Avoid sshd's unauthenticated-connection burst limit at startup.
        time.sleep(.1 * (job["id"] % 12))
        worker_command = " ".join(map(shlex.quote, [remote_root+"/.venv/bin/python",
                           remote_root+"/search_forever.py", "worker", "--root", remote_root]))
        command = ["ssh", "-T", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15",
                   "-o", "ServerAliveInterval=30", "-o", "ServerAliveCountMax=3",
                   host, worker_command]
    process = subprocess.run(command, input=payload, text=True, capture_output=True,
                             timeout=job.get("timeout_seconds", job["hop_seconds"]+job["slp_seconds"]+180),
                             env={**os.environ, "OPENBLAS_NUM_THREADS": "1",
                                  "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"})
    if process.returncode:
        raise RuntimeError(f"{host}: worker exited {process.returncode}: {process.stderr[-3000:]}")
    return json.loads(process.stdout)


def load_focus():
    path = HERE/"search_focus.json"
    if not path.exists():
        return []
    values = json.loads(path.read_text())["targets"]
    if not isinstance(values, list) or not values or len(set(values)) != len(values):
        raise ValueError("Focus targets must be a nonempty list of unique square counts")
    for n in values:
        if type(n) is not int or not 1 <= n <= SEARCH_MAX:
            raise ValueError(f"Invalid focus target: {n!r}")
        if not (HERE/f"records/n{n}.txt").exists():
            raise ValueError(f"Missing focus reference n={n}")
    return values


def slot_limits(state_dir, slots):
    """Optional runtime caps from slots.json, e.g. {"remote_jobs": 8}.

    Lowering a cap lets running jobs finish and stops refilling the excess
    slots, so cores can be lent to a manual experiment without a restart.
    """
    path = state_dir/"slots.json"
    try:
        limits = json.loads(path.read_text()) if path.exists() else {}
    except (OSError, ValueError):
        return set()
    disabled, seen = set(), {"local": 0, "remote": 0}
    for slot, host in enumerate(slots):
        kind = "local" if host == "local" else "remote"
        if seen[kind] >= limits.get(kind+"_jobs", len(slots)):
            disabled.add(slot)
        seen[kind] += 1
    return disabled


def choose_job(counter, seconds=120, host="local", rotation=None, max_n=SEARCH_MAX, focus=None):
    rng = random.Random(925000000+counter)
    rotation = counter if rotation is None else rotation
    own = sorted(int(p.stem[1:]) for p in HERE.glob("n[0-9]*.txt")
                 if int(p.stem[1:]) <= min(PUBLISHED_MAX, max_n))
    priority = PRIORITY + [n for n in own if n not in PRIORITY]
    new_targets = expanded_targets(HERE, max_n)
    legacy_rotation = rotation//2 if new_targets else rotation
    if focus:
        n = focus[rotation % len(focus)]
    elif new_targets and rotation % 2 == 0:
        n = new_targets[(rotation//2) % len(new_targets)]
    elif legacy_rotation % 5 == 4:
        catalogue = {}
        for line in (HERE/"records.txt").read_text().splitlines():
            if line.strip() and not line.startswith("#"):
                k, side = line.split()
                catalogue[int(k)] = float(side)
        extended = FRONTIER+[n for n, side in sorted(catalogue.items())
                             if 10 <= n <= min(PUBLISHED_MAX, max_n) and n not in FRONTIER
                             and abs(side-round(side)) > 1e-7]
        # Counts the catalogue lists as the grid but where a smaller packing is
        # now known (e.g. Kevin Fang's s(308) < 18, #484).
        extended += [n for n in below_grid(HERE, min(PUBLISHED_MAX, max_n)) if n >= 10 and n not in extended]
        available = [n for n in extended if n not in own and best_source(HERE, n)[0] is not None]
        if not available:
            available = priority
        n = available[(legacy_rotation//5) % len(available)]
    else:
        index = legacy_rotation-legacy_rotation//5
        n = priority[index % len(priority)]
    # Start from the best packing available: a verified external packing when
    # it beats ours (import_external.py), so no job polishes a superseded basin.
    base, origin = best_source(HERE, n)
    construction = None
    # Use the reviewed mix for every target, including focused searches;
    # fixed periodic overrides would keep disabled methods running.
    weights = load_weights(HERE)
    if host == "local" and "gpu" in weights:
        weights = {method: weight for method, weight in weights.items() if method != "gpu"}
        total = sum(weights.values())
        weights = {method: weight/total for method, weight in weights.items()} if total else {"hop": 1.}
    method = pick(weights, rng.random())
    if method == "old":
        # Kick an older basin of the same count (Evan Daniel's s(270), s(272)).
        old = old_basin(HERE, n, rng)
        base, origin, method = (old, "old basin", "old") if old else (base, origin, "hop")
    elif method == "graft":
        graft = graft_seed(HERE, n, rng)
        if graft:
            construction = {**graft[1], "packing": graft[0]}
        else:
            method = "hop"
    elif method == "shrink":
        other, other_origin = neighbour_source(HERE, n, rng)
        if other:
            base, origin = other, other_origin
        else:
            method = "hop"
    elif method == "compress" and n > COMPRESS_MAX_N:
        method = "hop"
    elif method in ("drop", "grow"):
        # Infrequent insertion/removal chains explore different contact graphs.
        other, other_origin = best_source(HERE, n+1 if method == "drop" else n-1)
        if other:
            base, origin = other, other_origin
        else:
            method = "hop"
    if construction:
        packing = construction.pop("packing")
    else:
        packing = base.read_text()
    if n > PUBLISHED_MAX and method not in ("drop", "grow", "graft", "shrink", "old"):
        packing, construction = construct_seed(HERE, n)
    hop_seconds = 0 if method == "slp" else 900 if method == "compress" else 360 if method in ("fq", "shrink") else 240
    return {"id": counter, "n": n, "seed": 925000000+counter, "method": method,
            "variant": counter % 4 != 0, "radius": rng.choice([.001, .003, .01, .02, .05]),
            "iterations": 1000, "hop_seconds": hop_seconds,
            "slp_seconds": seconds, "source": str(base.relative_to(HERE)) if not construction else construction["source"],
            "source_origin": origin if not construction else construction.get("source_origin", "constructed"),
            "range_group": "focus" if focus else ("expanded" if n > PUBLISHED_MAX else "published"),
            "focus_targets": focus,
            **({"pool_size": 8 if method not in ("slp", "gpu") else 0,
                "pool_gap": .02} if focus else {}),
            "constructed_seed": construction,
            "source_sha256": hashlib.sha256(packing.encode()).hexdigest(), "packing": packing}


def choose_local_cycle(counter, cycle, max_n=SEARCH_MAX, focus=None):
    own = sorted(int(p.stem[1:]) for p in HERE.glob("n[0-9]*.txt")
                 if int(p.stem[1:]) <= min(PUBLISHED_MAX, max_n))
    preferred = [239, 272, 303, 208, 268, 228, 181, 307]
    targets = [n for n in preferred if n in own]+[n for n in own if n not in preferred]
    expanded = expanded_targets(HERE, max_n)
    legacy_cycle = cycle//2 if expanded else cycle
    n = (focus[cycle % len(focus)] if focus else
         expanded[(cycle//2) % len(expanded)] if expanded and cycle % 2 == 0
         else targets[legacy_cycle % len(targets)])
    source = HERE/f"n{n}.txt"
    construction = None
    if n > PUBLISHED_MAX:
        packing, construction = construct_seed(HERE, n)
        if not source.exists():
            source = HERE/f"records/n{n}.txt"
    else:
        source = best_source(HERE, n)[0]
        packing = source.read_text()
    return {"id":counter, "n":n, "seed":926000000+counter, "method":"ellsworth_cycle",
            "local_cycle":cycle, "variant":True,
            "radius":[.003, .01, .02][(cycle//len(focus) if focus else cycle) % 3],
            "hop_seconds":150, "slp_seconds":120, "ellsworth_seconds":45,
            "compact_seconds":30, "timeout_seconds":600,
            "range_group":"focus" if focus else ("expanded" if n > PUBLISHED_MAX else "published"),
            "focus_targets":focus,
            "repair_seed": bool(focus) or "external/" in str(source),
            "constructed_seed":construction,
            "source":str(source.relative_to(HERE)),
            "source_origin": "external" if "external/" in str(source) else "constructed" if construction else "own",
            "source_sha256":hashlib.sha256(packing.encode()).hexdigest(),
            "packing":packing}


def coordinator(args):
    from accept_candidates import accept

    os.chdir(HERE)
    state_dir = HERE / "experiments/forever"
    state_dir.mkdir(parents=True, exist_ok=True)
    # A service restart or accidental second invocation must never start a
    # competing writer of the official records.
    import fcntl
    lock = (state_dir/"coordinator.lock").open("w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    lock.write(str(os.getpid()))
    lock.flush()
    logger = logging.getLogger("search")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(state_dir/"events.jsonl", maxBytes=10_000_000, backupCount=5)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    def event(kind, **data):
        value = {"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "event": kind, **data}
        logger.info(json.dumps(value))
        print(json.dumps(value), flush=True)

    records = {}
    for line in (HERE/"records.txt").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            n, side = line.split()
            records[int(n)] = Fraction(side)
    focus = load_focus()
    if any(n not in records or n > args.max_n for n in focus):
        raise ValueError("Focus targets must have reference bounds and be within --max-n")
    state_path = state_dir/"state.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {
        "next_job": 0, "completed": 0, "improvements": 0, "errors": 0, "by_n": {}}
    stop = False
    reload_requested = False

    def stopping(signum, frame):
        nonlocal stop
        stop = True

    signal.signal(signal.SIGTERM, stopping)
    signal.signal(signal.SIGINT, stopping)

    def reloading(signum, frame):
        nonlocal reload_requested
        reload_requested = True

    signal.signal(signal.SIGUSR1, reloading)
    slots = ["local"]*args.local_jobs + [args.remote]*args.remote_jobs
    pending = {}
    cooldown = {}
    ready = state_dir/"pending"
    ready.mkdir(exist_ok=True)

    def acknowledge(job):
        name = f"job-{int(job['id'])}.json"
        if job["host"] == "local":
            (HERE/"completed"/name).unlink(missing_ok=True)
        else:
            import shlex
            path = args.remote_root+"/completed/"+name
            subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                            args.remote, "rm -f -- "+shlex.quote(path)],
                           timeout=20, capture_output=True, check=True)

    def install(directory, job):
        candidate = directory/f"n{job['n']}.txt"
        entry = accept(candidate, records)
        if entry:
            state["improvements"] += 1
            nstat = state["by_n"].setdefault(str(job["n"]), {"improvements": 0})
            nstat["improvements"] += 1
            nstat["side"] = float(Fraction(entry["after"]))
            archive = HERE/"found"/f"n{job['n']}_s{float(Fraction(entry['after'])):.12f}.certificate.json"
            cert = json.loads(archive.read_text())
            cert["search_job"] = job
            seed_credit(cert, job)
            atomic_json(archive, cert)
            subprocess.run(["python3", "regen_readme.py"], check=True, capture_output=True)
            subprocess.run(["python3", "check_readme.py"], check=True, capture_output=True)
            event("improvement", job=job, before=entry["before"], after=entry["after"],
                  rational_side=entry["rational_side"])
            notify_record(job, entry)
            # Exact finish (exact_finish.py, Evan Daniel's contact solver) in
            # the background; one instance at a time, it rescans before exiting.
            subprocess.Popen(["nice", "-n", "10", str(HERE/".venv/bin/python"), str(HERE/"exact_finish.py"), "--pending"],
                             cwd=HERE, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
        shutil.rmtree(directory)
        acknowledge(job)

    def stage(job, result):
        if result.get("packing"):
            directory = ready/str(job["id"])
            directory.mkdir(exist_ok=True)
            if "worker_details" in result:
                job["worker_details"] = result["worker_details"]
            (directory/f"n{job['n']}.txt").write_text(result["packing"])
            atomic_json(directory/"job.json", job)
            install(directory, job)
        else:
            acknowledge(job)

    # Recover complete, unprocessed candidates after a crash.
    for directory in sorted(ready.iterdir()):
        if directory.is_dir() and (directory/"job.json").exists():
            try:
                install(directory, json.loads((directory/"job.json").read_text()))
            except Exception as exc:
                event("recovery_error", path=str(directory), error=str(exc))
    # A worker durably stores its result before returning over SSH. Recover
    # results whose connection or coordinator disappeared before acceptance.
    for host in ("local", args.remote):
        try:
            if host == "local":
                recovered = [json.loads(p.read_text()) for p in (HERE/"completed").glob("job-*.json")]
            else:
                import shlex
                script = ("import json; from pathlib import Path; "
                          f"print(json.dumps([json.loads(p.read_text()) for p in Path({args.remote_root!r})"
                          ".joinpath('completed').glob('job-*.json')]))")
                process = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                            host, "python3 -c "+shlex.quote(script)],
                            capture_output=True, text=True, timeout=45, check=True)
                recovered = json.loads(process.stdout)
            for item in recovered:
                job = item["job"]
                job["host"] = host
                stage(job, item["result"])
            event("recovered", host=host, count=len(recovered))
        except Exception as exc:
            event("recovery_error", host=host, error=str(exc))
    event("started", pid=os.getpid(), slots=slots, next_job=state["next_job"], max_n=args.max_n,
          focus_targets=focus,
          expanded_targets=expanded_targets(HERE, args.max_n))
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(slots)) as pool:
        while not stop:
            normalization_request = state_dir/"normalize.request"
            if normalization_request.exists():
                from accept_candidates import normalize_existing
                report = normalize_existing(records)
                atomic_json(state_dir/"normalization.json", report)
                for item in report:
                    if "side" in item and str(item["n"]) in state["by_n"]:
                        state["by_n"][str(item["n"])]["side"] = item["side"]
                atomic_json(state_path, state)
                normalization_request.unlink()
                event("normalized", count=len(report), changed=sum(r["changed"] for r in report))
            if reload_requested and not pending:
                break
            # Refresh the best-known table (register + verified external
            # certificates) hourly; new seeds apply to later dispatches.
            known = HERE/"known_best.json"
            if not known.exists() or time.time()-known.stat().st_mtime > 3600:
                if time.time() > state.get("next_import", 0):
                    state["next_import"] = time.time()+3600
                    subprocess.Popen(["nice", "-n", "10", str(HERE/".venv/bin/python"), str(HERE/"import_external.py")],
                                     cwd=HERE, stdin=subprocess.DEVNULL,
                                     stdout=(state_dir/"import_external.log").open("a"),
                                     stderr=subprocess.STDOUT, start_new_session=True)
                    event("import_external_started")
            # Install exact polishes of our packings (exact_finish.py results), a few per pass.
            if time.time() > state.get("next_polish", 0):
                state["next_polish"] = time.time()+600
                try:
                    # The coordinator runs without SciPy: polish in the project's
                    # virtualenv, waiting for it so installation stays serialized.
                    run = subprocess.run([str(HERE/".venv/bin/python"), "-c",
                                          "import json; from accept_candidates import install_polished; "
                                          "print(json.dumps(install_polished()))"],
                                         cwd=HERE, capture_output=True, text=True, timeout=1800, check=True)
                    polished = json.loads(run.stdout.strip().splitlines()[-1])
                    for item in polished:
                        state["by_n"].setdefault(str(item["n"]), {"improvements": 0})["side"] = float(Fraction(item["after"]))
                    if polished:
                        event("polished", changed=polished)
                except Exception as exc:
                    event("polish_error", error=str(exc), traceback=traceback.format_exc()[-3000:])
            disabled = slot_limits(state_dir, slots)
            for slot, host in enumerate(slots):
                if reload_requested:
                    break
                if slot in disabled or slot in (item[0] for item in pending.values()) \
                        or time.time() < cooldown.get(slot, 0):
                    continue
                if host == "local" and args.local_mode == "ellsworth":
                    cycle = state.get("local_cycles", 0)
                    job = choose_local_cycle(state["next_job"], cycle, args.max_n, focus)
                    state["local_cycles"] = cycle+1
                else:
                    rotation = state.get("search_cycles", 0)
                    job = choose_job(state["next_job"], args.seconds, host, rotation, args.max_n, focus)
                    state["search_cycles"] = rotation+1
                state["next_job"] += 1
                atomic_json(state_path, state)
                future = pool.submit(dispatch, job, host, args.remote_root)
                metadata = {k: v for k, v in job.items() if k != "packing"}
                metadata["host"] = host
                metadata["started"] = time.time()
                pending[future] = (slot, metadata)
                event("dispatched", job=metadata)
            atomic_json(state_dir/"status.json", {**state, "updated": time.time(),
                        "pid": os.getpid(), "max_n": args.max_n, "focus_targets": focus,
                        "disabled_slots": sorted(disabled),
                        "running": [m for _, m in pending.values()]})
            if not pending:
                time.sleep(10)
                continue
            done, _ = concurrent.futures.wait(pending, timeout=10,
                                              return_when=concurrent.futures.FIRST_COMPLETED)
            for future in done:
                slot, job = pending.pop(future)
                try:
                    result = future.result()
                    state["completed"] += 1
                    event("completed", job=job, result={k: v for k, v in result.items()
                                                        if k not in ("packing", "trace")})
                    stage(job, result)
                except Exception as exc:
                    state["errors"] += 1
                    cooldown[slot] = time.time()+60
                    event("error", job=job, error=str(exc), traceback=traceback.format_exc()[-3000:])
                atomic_json(state_path, state)
    if reload_requested:
        event("restarting")
        os.execv(sys.executable, [sys.executable, *sys.argv])
    event("stopped")


def main():
    hosts = HERE/"search_hosts.json"
    defaults = json.loads(hosts.read_text()) if hosts.exists() else {}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["worker", "coordinator"])
    parser.add_argument("--root", type=Path, default=HERE)
    parser.add_argument("--remote", default=defaults.get("remote"))
    parser.add_argument("--remote-root", default=defaults.get("remote_root"))
    parser.add_argument("--local-jobs", type=int, default=2)
    parser.add_argument("--local-mode", choices=["search", "ellsworth"], default="ellsworth")
    parser.add_argument("--remote-jobs", type=int, default=defaults.get("remote_jobs", 0))
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--max-n", type=int, choices=range(PUBLISHED_MAX, SEARCH_MAX+1),
                        default=SEARCH_MAX, metavar="324..400")
    args = parser.parse_args()
    if args.mode == "coordinator" and args.remote_jobs and not (args.remote and args.remote_root):
        parser.error("remote jobs require --remote and --remote-root")
    if args.mode == "worker":
        os.environ["OPENBLAS_NUM_THREADS"] = "1"
        os.environ["OMP_NUM_THREADS"] = "1"
        job = json.load(sys.stdin)
        result = run_worker(args.root, job)
        completed = args.root/"completed"
        completed.mkdir(exist_ok=True)
        atomic_json(completed/f"job-{job['id']}.json", {
            "job": {k: v for k, v in job.items() if k != "packing"}, "result": result})
        print(json.dumps(result))
    else:
        coordinator(args)


if __name__ == "__main__":
    main()
