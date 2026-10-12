#!/usr/bin/env python3
"""Exact finishing of installed packings with Evan Daniel's contact solver.

Our certificates dilate a floating-point LP result (rationalize.py), which
leaves 1e-12..4e-11 of side above the packing's exact local optimum; others
have registered that gap as "refinements" of our packings. This step solves
the active contact system exactly (KKT Newton at 80 digits), and writes a
rational certificate within ~1e-19 of the exact optimum:

  1. fq quench --no-alm --loosen 1.0: polish onto the contact system (fq);
  2. exactsolve.py: contacts, load-bearing set, KKT Newton, second-order and
     corner-corner checks, rational certificate (external/evand/search/exact);
  3. the certificate is replayed by evand's verify_cert.py and, independently,
     by our verify.py in exact rational arithmetic.

Results: found/nN_s<side>.exact.{cert,json,log}, keyed to the SHA-256 of the
installed nN.txt; nothing else is modified. The installed record and its
dilated certificate stay as they are; the exact certificate is the tighter
statement to publish.

usage: exact_finish.py N [N ...]      finish these counts
       exact_finish.py --pending      every installed packing without one
"""
import argparse
import fcntl
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
EXACT = ROOT/"external/evand/search/exact"
PY = ROOT/".venv/bin/python"


def current(n):
    path = ROOT/f"n{n}.txt"
    text = path.read_text()
    side = next(float(l.split("=")[1]) for l in text.splitlines() if l.startswith("# s ="))
    return path, side, hashlib.sha256(text.encode()).hexdigest()


def stem(n, side):
    """found/nN_s<side>.exact; callers append .json, .cert or .log."""
    return ROOT/"found"/f"n{n}_s{side:.12f}.exact"


def named(base, ext):
    return base.with_name(base.name+ext)


def done(n):
    path, side, digest = current(n)
    meta = named(stem(n, side), ".json")
    return meta.exists() and json.loads(meta.read_text()).get("input_sha256") == digest


def exact_replay(cert):
    sys.path.insert(0, str(ROOT))
    from import_external import corners, read_cert_text
    from verify import verify_packing
    n, side, squares = read_cert_text(cert)
    report = verify_packing([corners(*q) for q in squares], side, lambda v: (v > 0)-(v < 0), bucket=True)
    return {"valid": report.valid, "pairs_tested": report.pairs_tested, "side": str(side), "n": n}


def finish(n, log):
    path, side, digest = current(n)
    out = stem(n, side)
    env = {**os.environ, "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f"exact-{n}-", dir=ROOT/"experiments") as d:
        d = Path(d)
        rows = [tuple(map(float, l.split()[:3])) for l in path.read_text().splitlines()
                if l.strip() and not l.startswith("#")]
        (d/"input.txt").write_text(f"{len(rows)} {side:.17f}\n" + "".join(
            f"{x:.17f} {y:.17f} {math.degrees(t):.15f}\n" for x, y, t in rows))
        fq = next(p for p in (ROOT/"fq", ROOT/"external/evand/search/packer/target/release/fq") if p.exists())
        polish = subprocess.run([str(fq), "quench", "--in", str(d/"input.txt"), "--out", str(d/"polished.txt"),
                                 "--no-alm", "--loosen", "1.0"], capture_output=True, text=True, timeout=1800)
        meta = {"n": n, "input": path.name, "input_sha256": digest, "input_side": side,
                "fq_polish": polish.stdout.strip()[-400:], "attempts": [],
                "upstream": "https://github.com/evand/square-packing (search/exact, search/packer), MIT",
                "seconds": None}
        logs = ""
        best = None
        # The raw pose first (as in Evan Daniel's register batch), then the
        # fq-polished one. pipeline.py: exactsolve, and while a corner-corner
        # touch can still slip (MILP descent) or no equilibrium exists,
        # descend and solve again.
        for source in (d/"input.txt", d/"polished.txt"):
            if not source.exists():
                continue
            work = d/f"out-{source.stem}"
            try:
                solve = subprocess.run([str(PY), str(EXACT/"pipeline.py"), str(source), "--out", str(work), "--cycles", "5"],
                                       capture_output=True, text=True, timeout=7200, env=env, cwd=EXACT)
                meta["attempts"].append({"source": source.name, "returncode": solve.returncode,
                                         "pipeline": solve.stdout.strip().splitlines()[-6:]})
                logs += f"######## {source.name}\n{solve.stdout[-50000:]}{solve.stderr[-20000:]}\n"
            except subprocess.TimeoutExpired:
                meta["attempts"].append({"source": source.name, "timeout": True})
            logs += "".join(f"==== {q.name}\n{q.read_text()}" for q in sorted(work.glob("*.log")))
            for rj in sorted(work.glob("*.json")):
                r = json.loads(rj.read_text())
                cert = rj.with_suffix(".cert")
                if r.get("cert_valid") and cert.exists() and (best is None or Fraction(r["S_cert"]) < Fraction(best[0]["S_cert"])):
                    best = (r, cert)
            if best and Fraction(best[0]["S_cert"]) < Fraction(side) and best[0].get("vv_milp_dS") is not None \
                    and best[0]["vv_milp_dS"] > -1e-9:
                break  # a jammed exact optimum below the input: done
        out.parent.mkdir(exist_ok=True)
        named(out, ".log").write_text(logs[-400000:])
        meta["ok"] = False
        if best:
            r, cert = best
            meta.update({k: r.get(k) for k in ("S_exact", "S_cert", "S_cert_decimal", "cert_valid", "second_order",
                                                "vv_milp_dS", "free_squares", "newton_converged")})
            meta["jammed_in_every_branch"] = r.get("vv_milp_dS") is not None and r["vv_milp_dS"] > -1e-9
            shutil.copy2(cert, named(out, ".cert"))
            v1 = subprocess.run([str(PY), str(EXACT/"verify_cert.py"), str(named(out, ".cert"))],
                                capture_output=True, text=True, timeout=3600, cwd=EXACT)
            meta["evand_verify_cert"] = v1.stdout.strip().splitlines()[-1:] if v1.stdout else v1.stderr[-300:]
            meta["exact_replay_verify_py"] = exact_replay(named(out, ".cert"))
            certified = Fraction(meta["exact_replay_verify_py"]["side"])
            meta["certified_side"] = str(certified)
            meta["certified_side_decimal"] = f"{float(certified):.15f}"
            meta["gain_over_input"] = side-float(certified)
            # Only a certificate below the installed numerical side is an exact finish.
            meta["ok"] = bool(meta["exact_replay_verify_py"]["valid"] and r.get("cert_valid")
                              and certified < Fraction(side))
        meta["seconds"] = time.monotonic()-started
        named(out, ".json").write_text(json.dumps(meta, indent=2, default=str)+"\n")
        log(f"n={n}: " + (f"certified {meta['certified_side_decimal']} ({meta['gain_over_input']:.2e} below the input)"
                          if meta["ok"] else f"no exact improvement ({meta.get('certified_side_decimal', 'no certificate')})")
            + f" in {meta['seconds']:.0f} s")
        return meta


def witness(n, log=print):
    """Fallback certificate when the exact solve does not certify a smaller side:
    the installed decimal packing as rationals (t = tan(theta/2) and centres
    rounded to rationals, centres scaled apart by 1+1e-12, or more if needed),
    checked exactly by verify.py, written in Evan Daniel's .cert format so his
    verify_cert.py reads it too. Returns the metadata, or None."""
    from import_external import corners, exact_check
    path, side, digest = current(n)
    base = stem(n, side).with_name(f"n{n}_s{side:.12f}.witness")
    meta_path = named(base, ".json")
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        if meta.get("input_sha256") == digest and meta.get("valid"):
            return meta
    poses = [tuple(map(float, l.split()[:3])) for l in path.read_text().splitlines()
             if l.strip() and not l.startswith("#")]
    for k in range(12, 3, -1):
        grow = 1+Fraction(1, 10**k)
        sq = [(Fraction(x).limit_denominator(10**13), Fraction(y).limit_denominator(10**13),
               Fraction(math.tan(th/2)).limit_denominator(10**10)) for x, y, th in poses]
        cx, cy = sum(q[0] for q in sq)/len(sq), sum(q[1] for q in sq)/len(sq)
        sq = [(cx+(x-cx)*grow, cy+(y-cy)*grow, t) for x, y, t in sq]
        pts = [c for q in sq for c in corners(*q)]
        x0, y0 = min(c[0] for c in pts), min(c[1] for c in pts)
        # 1e-15 off every wall: Evan Daniel's verify_cert.py wants the open box.
        d = Fraction(1, 10**15)
        sq = [(x-x0+d, y-y0+d, t) for x, y, t in sq]
        S = max(max(c[0]-x0, c[1]-y0) for c in pts)+2*d
        verdict = exact_check((S, sq))
        if verdict["valid"]:
            named(base, ".cert").write_text(
                "# rational witness: unit squares, centre (x, y), rotation t = tan(theta/2); check with verify_cert.py\n"
                f"{n} {S}\n" + "".join(f"{x} {y} {t}\n" for x, y, t in sq))
            meta = {"n": n, "input": path.name, "input_sha256": digest, "input_side": side, "valid": True,
                    "dilation": f"1+1e-{k}", "certified_side": str(S), "certified_side_decimal": f"{float(S):.15f}",
                    "pairs_tested": verdict["pairs_tested"]}
            meta_path.write_text(json.dumps(meta, indent=2)+"\n")
            log(f"n={n}: rational witness {float(S):.15f} (dilation 1+1e-{k})")
            return meta
    log(f"n={n}: no rational witness up to dilation 1+1e-4")
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("n", nargs="*", type=int)
    p.add_argument("--pending", action="store_true")
    a = p.parse_args()
    lock = (ROOT/"experiments/exact_finish.lock").open("w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("another exact_finish is running; it rescans for new packings before exiting")
        return

    def log(msg):
        line = f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} {msg}"
        print(line, flush=True)
        with (ROOT/"experiments/exact_finish.log").open("a") as f:
            f.write(line+"\n")
    attempted = set()
    while True:
        todo = list(a.n) if a.n else []
        if a.pending:
            todo += sorted(int(q.stem[1:]) for q in ROOT.glob("n[0-9]*.txt"))
        todo = [n for n in dict.fromkeys(todo) if (n, current(n)[2]) not in attempted and not done(n)]
        if not todo:
            break
        n = todo[0]
        attempted.add((n, current(n)[2]))
        try:
            finish(n, log)
        except Exception as exc:
            log(f"n={n}: error {exc!r}")
        if not a.pending and all((m, current(m)[2]) in attempted for m in a.n):
            break


if __name__ == "__main__":
    main()
