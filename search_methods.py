#!/usr/bin/env python3
"""Seed selection and the externally implemented search methods.

Coordinator side (needs the repository; no SciPy):
  load_weights      method mix, from search_methods.json if present
  best_source       best packing available for n: an external seed that beats
                    ours (external/seeds/, see import_external.py), else ours,
                    else the catalogue reference, else the best older basin
  below_grid        counts whose best known side is below the grid ceil(sqrt(n))
  old_basin         an older packing of n: earlier register packings, superseded
                    external ones, the catalogue reference, our earlier versions,
                    and our packings removed as superseded (superseded/)
  graft_seed        SQUISH-style graft: a smaller packing plus L borders, a few
                    squares short of n; the Rust search inserts the rest
  neighbour_source  the best packing of n+1 or n+2, for shrink-hopping

Worker side (standard library + the binaries; runs on either host):
  run_external      "shrink": remove the surplus squares, then Evan Daniel's
                    `packer hop` (fixed-side overlap energy, hop until feasible,
                    then a lower target); "fq": basin hopping on his `fq quench`
                    (proposals of his hop.py). Both return candidates for the
                    usual LP refinement and exact acceptance.
  fq_finish         polish every candidate with fq (face flips) before LP

Binaries: ROOT/fq and ROOT/packer, else external/evand/search/packer/target/release/.
"""
import json
import math
from pathlib import Path
import random
import subprocess
import time

# 2026-10-12: 24,863 completed jobs since October 7. Hop/FQ produced
# 83/25 accepted improvements; cheap SLP produced 20. Graft, grow, random
# starts and compression produced none. Keep reduced shares for older
# basins, shrink-hopping, deletion and CUDA starts.
DEFAULT_WEIGHTS = {"slp": .25, "hop": .45, "fq": .20, "drop": .03,
                   "shrink": .02, "old": .015, "gpu": .005,
                   "graft": 0., "grow": 0., "compress": 0., "random": 0.}
COMPRESS_MAX_N = 120  # the browser engine is O(n^2) per evaluation; its page caps n at 120
PUBLISHED_MAX = 324


def load_weights(root):
    path = Path(root)/"search_methods.json"
    weights = dict(DEFAULT_WEIGHTS)
    if path.exists():
        weights.update(json.loads(path.read_text()).get("weights", {}))
    total = sum(weights.values())
    return {k: v/total for k, v in weights.items() if v > 0}


def pick(weights, roll):
    for method, w in weights.items():
        if roll < w:
            return method
        roll -= w
    return next(iter(weights))


def side_of(path):
    for line in Path(path).read_text().splitlines()[:3]:
        if line.startswith("# s ="):
            return float(line.split("=")[1])
    rows = [list(map(float, l.split()[:3])) for l in Path(path).read_text().splitlines()
            if l.strip() and not l.startswith("#")]
    # A file without poses (a placeholder) is no usable source.
    return max((max(x, y)+(abs(math.cos(t))+abs(math.sin(t)))/2 for x, y, t in rows), default=math.inf)


def best_source(root, n):
    """(path, origin) of the best packing we may start n from."""
    root = Path(root)
    own, ext, ref = root/f"n{n}.txt", root/"external/seeds"/f"n{n}.txt", root/"records"/f"n{n}.txt"
    try:
        if ext.exists() and (not own.exists() or side_of(ext) < side_of(own)-1e-9):
            return ext, "external"
    except (OSError, ValueError, StopIteration):
        pass  # being replaced by import_external.py; use ours this time
    if own.exists():
        return own, "own"
    if ref.exists():
        return ref, "catalogue"
    # No packing of ours or the catalogue's: the best older external basin
    # (e.g. Evan Daniel's copy of a register packing).
    old = []
    for path in (root/"external/seeds/old").glob(f"n{n}_*.txt"):
        try:
            old.append((side_of(path), path))
        except (OSError, ValueError, StopIteration):
            pass
    return (min(old)[1], "old basin") if old else (None, None)


def old_basin(root, n, rng):
    root = Path(root)
    current = best_source(root, n)[0]
    options = sorted((root/"external/seeds/old").glob(f"n{n}_*.txt"))
    options += [p for p in [root/"records"/f"n{n}.txt", root/"superseded"/f"n{n}.txt"] if p.exists()]
    own = sorted((root/"found").glob(f"n{n}_s*.txt"))
    options += own[1:]  # earlier versions of ours, not the current best
    options = [p for p in options if current is None or p.resolve() != current.resolve()]
    return rng.choice(options) if options else None


def read_rows(path):
    return [tuple(map(float, l.split()[:3])) for l in Path(path).read_text().splitlines()
            if l.strip() and not l.startswith("#")]


def graft_seed(root, n, rng, max_insert=3):
    """An L-bordered smaller packing with 1..max_insert squares missing.

    Candidates are the best packings of every m < n whose border count lands
    just below n; the smaller the bordered side, the likelier the choice.
    Returns (packing text, provenance) or None.
    """
    from expand_search import add_border, wrap, format_packing
    root = Path(root)
    target = best_source(root, n)[0]
    target_side = side_of(target) if target else float(math.isqrt(n-1)+1)
    choices = []
    for m in range(max(2, n//3), n):
        path, origin = best_source(root, m)
        if path is None:
            continue
        side = side_of(path)
        if not math.isfinite(side) or abs(side-round(side)) < 1e-9:
            continue  # bordered grids are grids
        count, s, layers = m, side, 0
        while count < n:
            if 1 <= n-count <= max_insert and s < target_side+.05:
                choices.append((s, m, layers, path, origin))
            count += 2*math.floor(s)+1
            s += 1
            layers += 1
    if not choices:
        return None
    choices.sort()
    s, m, layers, path, origin = choices[min(int(rng.expovariate(1/3)), len(choices)-1)]
    rows, side = wrap(read_rows(path))
    for _ in range(layers):
        rows, side = add_border(rows, side)
    rows, side = wrap(rows)
    return format_packing(rows, side), {"construction": "L-border graft, insertion by search",
                                         "source": str(path.relative_to(root)), "source_origin": origin,
                                         "source_n": m, "layers": layers, "missing": n-len(rows),
                                         "side": side}


def neighbour_source(root, n, rng):
    options = []
    for k in (1, 2):
        path, origin = best_source(root, n+k)
        side = side_of(path) if path is not None else math.inf
        if math.isfinite(side) and abs(side-round(side)) > 1e-9:
            options.append((path, origin))
    return rng.choice(options) if options else (None, None)


# ---------------------------------------------------------------- worker side

def binary(root, name):
    for p in (Path(root)/name, Path(root)/"external/evand/search/packer/target/release"/name):
        if p.exists():
            return p
    raise FileNotFoundError(f"{name} binary not found under {root}")


def to_evand(path, side, rows):
    Path(path).write_text(f"{len(rows)} {side:.17f}\n" +
                          "".join(f"{x:.17f} {y:.17f} {math.degrees(t):.15f}\n" for x, y, t in rows))


def from_evand(path):
    lines = [l.split() for l in Path(path).read_text().splitlines() if l.strip() and not l.startswith("#")]
    n, side = int(lines[0][0]), float(lines[0][1])
    return side, [(float(r[0]), float(r[1]), math.radians(float(r[2]))) for r in lines[1:n+1]]


def bbox(rows):
    return max(max(x, y)+(abs(math.cos(t))+abs(math.sin(t)))/2 for x, y, t in rows)


def fq_quench(fq, wd, side, rows, loosen, timeout, extra=()):
    a, b = wd/"fq_a.txt", wd/"fq_b.txt"
    to_evand(a, side, rows)
    try:
        r = subprocess.run([str(fq), "quench", "--in", str(a), "--out", str(b), "--loosen", str(loosen), *extra],
                           capture_output=True, text=True, timeout=max(1, timeout))
        d = json.loads(r.stdout)
    except (subprocess.TimeoutExpired, ValueError):
        return None
    if not (d["min_gap"] >= 0 and d["min_wall"] >= 0):
        return None
    return from_evand(b)


def propose(rows, rng):
    # Evan Daniel's hop.py move set (angles in radians here: 20 sigma degrees).
    if rng.random() < .5:
        sig = rng.choice((.003, .01, .03))
        return [(x+rng.gauss(0, sig), y+rng.gauss(0, sig), t+math.radians(rng.gauss(0, 20*sig))) for x, y, t in rows]
    cx, cy, _ = rows[rng.randrange(len(rows))]
    r, sig = rng.choice((1.5, 2.5, 3.5)), rng.choice((.05, .1, .2))
    out = []
    for x, y, t in rows:
        sg = sig if (x-cx)**2+(y-cy)**2 < r*r else .002
        out.append((x+rng.gauss(0, sg), y+rng.gauss(0, sg), t+math.radians(rng.gauss(0, 20*sg))))
    return out


def run_external(method, root, wd, job, seed_path):
    """Returns ([(name, rows)], details); rows are (x, y, theta) with n squares."""
    rng = random.Random(job["seed"])
    n, budget = job["n"], job["hop_seconds"]
    deadline = time.monotonic()+budget
    rows = read_rows(seed_path)
    details = {"external_method": method, "seed_squares": len(rows)}
    candidates = []
    if method == "compress":
        # Ryan Xu's packing-lab engine from random starts (compress_lab.js).
        node = next((p for p in (Path(root)/"node/bin/node", Path("/usr/local/bin/node"), Path("/usr/bin/node"))
                     if p.exists()), None)
        if node is None:
            raise FileNotFoundError("node runtime not found")
        out = wd/"compress.txt"
        r = subprocess.run([str(node), str(Path(root)/"compress_lab.js"), str(n), str(max(10, budget-15)), str(out),
                            "--seed", str(job["seed"] % 2**31), "--wind", rng.choice(("off", "seq"))],
                           capture_output=True, text=True, timeout=budget+60)
        details["compress"] = r.stdout.strip()[-400:]
        if out.exists():
            candidates.append(("compress", read_rows(out)))
        return candidates, details
    fq = binary(root, "fq")
    if method == "fq":
        side = bbox(rows)
        cur = best = (side, rows)
        proposals = accepted = since = 0
        while time.monotonic() < deadline-5:
            r = fq_quench(fq, wd, cur[0], propose(cur[1], rng), 1.02, deadline-time.monotonic())
            proposals += 1
            if r is None:
                continue
            if r[0] < cur[0] or rng.random() < math.exp(-(r[0]-cur[0])/1e-5):
                cur, accepted = r, accepted+1
            if r[0] < best[0]-1e-12:
                best, since = r, 0
            else:
                since += 1
            if since >= 40:
                cur, since = best, 0
        details.update(proposals=proposals, accepted=accepted, best=best[0], start=side)
        if best[1] is not rows:
            candidates.append(("fq_best", best[1]))
        return candidates, details
    # shrink: remove the surplus, quench once, then fixed-side shrink-hopping
    packer = binary(root, "packer")
    extra = len(rows)-n
    if extra <= 0:
        raise ValueError("shrink needs a seed with more than n squares")
    side = bbox(rows)
    drop = set(rng.sample(range(len(rows)), extra))
    rows = [q for i, q in enumerate(rows) if i not in drop]
    details["removed"] = sorted(drop)
    inp, out = wd/"shrink_in.txt", wd/"shrink_out.txt"
    to_evand(inp, side, rows)
    try:
        r = subprocess.run([str(packer), "hop", "--in", str(inp), "--s", f"{side:.12f}", "--seed", str(job["seed"]),
                            "--iters", "1000000", "--descend", "2e-4", "--out", str(out), "--quiet"],
                           capture_output=True, text=True, timeout=max(5, deadline-time.monotonic()-30))
        details["packer"] = r.stdout.strip().splitlines()[-1:] if r.stdout else []
    except subprocess.TimeoutExpired:
        details["packer"] = ["budget reached"]
    if out.exists():
        s, found = from_evand(out)
        details["shrink_side"] = s
        candidates.append(("shrink", found))
        q = fq_quench(fq, wd, s, found, 1.0, max(5, deadline-time.monotonic()))
        if q:
            details["shrink_fq_side"] = q[0]
            candidates.append(("shrink_fq", q[1]))
    return candidates, details


def fq_finish(root, wd, candidates, budget):
    """fq polish (--no-alm: candidates are feasible) of each candidate.

    The 2026-10-08 benchmark (experiments/bench-fq-vs-slp) found our LP refiner
    stalling 0.003-0.025 above the basin minimum from kicked starts where fq
    returned to it in seconds. Returns extra (name, rows) candidates.
    """
    try:
        fq = binary(root, "fq")
    except FileNotFoundError:
        return [], {"fq_finish": "fq binary unavailable"}
    deadline = time.monotonic()+budget
    out, sides = [], {}
    for name, rows in candidates:
        remaining = deadline-time.monotonic()
        if remaining < 2:
            break
        rows = [tuple(map(float, q)) for q in rows]
        r = fq_quench(fq, wd, bbox(rows), rows, 1.0, remaining, extra=("--no-alm",))
        if r:
            out.append((name+"+fq", r[1]))
            sides[name] = r[0]
    return out, {"fq_finish": sides}


def below_grid(root, max_n=PUBLISHED_MAX):
    """Counts n <= max_n whose best known value (known_best.json) is below the
    grid side ceil(sqrt(n)): searchable even where the catalogue lists the grid."""
    path = Path(root)/"known_best.json"
    if not path.exists():
        return []
    entries = json.loads(path.read_text())["entries"]
    return sorted(int(n) for n, e in entries.items()
                  if int(n) <= max_n and e.get("side") and e["side"] < math.isqrt(int(n)-1)+1-1e-9)
