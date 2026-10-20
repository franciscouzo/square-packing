#!/usr/bin/env python3
"""Construct reference bounds and reusable seeds beyond the published table.

An L border extends m squares in side s to m + 2*floor(s) + 1 in
side s+1. Deleting squares gives all intermediate counts. These are derived
reference bounds, not independently surveyed best-known records.
"""
import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLISHED_MAX = 324
SEARCH_MAX = 1024


def catalogue(root):
    return {int(n): Fraction(s) for line in (root/"records.txt").read_text().splitlines()
            if line.strip() and not line.startswith("#") for n, s in [line.split()]}


def targets(root, max_n=SEARCH_MAX):
    # Area proves full square grids optimal; retain their bounds and witnesses
    # but spend optimization time on the other counts, including integer bounds.
    return [n for n in range(PUBLISHED_MAX+1, max_n+1)
            if math.isqrt(n)**2 != n and (root/f"records/n{n}.txt").exists()]


def extend_bound(count, side, target):
    layers = 0
    while count < target:
        count += 2*math.floor(side)+1
        side += 1
        layers += 1
    return side, count-target, layers


def wrap(rows):
    halves = [(abs(math.cos(t))+abs(math.sin(t)))/2 for _, _, t in rows]
    lo = [min(p[k]-h for p, h in zip(rows, halves)) for k in (0, 1)]
    hi = [max(p[k]+h for p, h in zip(rows, halves)) for k in (0, 1)]
    return [(x-lo[0], y-lo[1], t) for x, y, t in rows], max(hi[k]-lo[k] for k in (0, 1))


@lru_cache(maxsize=1024)
def read_source(path, mtime_ns, size):
    text = Path(path).read_text()
    rows = [tuple(map(float, line.split())) for line in text.splitlines()
            if line.strip() and not line.startswith("#")]
    if not rows or any(len(p) != 3 or not all(map(math.isfinite, p)) for p in rows):
        raise ValueError(f"Invalid source {path}")
    rows, side = wrap(rows)
    return rows, side, hashlib.sha256(text.encode()).hexdigest()


def add_border(rows, side):
    k = math.floor(side)
    # A small clearance protects touching border squares from float roundoff.
    gap = 2e-12
    edge = side+gap+.5
    # Along each row use exact half-integers. Stretching the row itself would
    # push its end into the perpendicular column when s is an integer.
    added = [(edge, .5+i, 0.) for i in range(k+1)]
    added += [(.5+i, edge, 0.) for i in range(k)]
    return rows+added, side+1+gap


def format_packing(rows, side):
    return (f"# n = {len(rows)}\n# s = {side:.17g}\n# x y theta(rad)\n"
            + "".join(" ".join(f"{v:.17g}" for v in p)+"\n" for p in rows))


def construct_seed(root, n, references_only=False):
    width = math.isqrt(n-1)+1
    best = (float(width), width*width-n, 0)
    chosen = None
    paths = list((root/"records").glob("n[0-9]*.txt"))
    if references_only:
        paths = [p for p in paths if int(p.stem[1:]) <= PUBLISHED_MAX]
    else:
        paths += list(root.glob("n[0-9]*.txt"))
    for path in sorted(paths):
        if int(path.stem[1:]) > SEARCH_MAX:
            continue
        stat = path.stat()
        rows, side, digest = read_source(str(path), stat.st_mtime_ns, stat.st_size)
        plan = extend_bound(len(rows), side, n)
        if plan[0] >= width-1e-10:
            continue  # Prefer an exact grid to an equal-size floating seed.
        if plan < best:
            best, chosen = plan, (path, rows, side, digest)
    if chosen is None:
        rows = [(.5+i % width, .5+i//width, 0.) for i in range(n)]
        info = {"construction": "grid", "width": width, "source": None, "layers": 0}
    else:
        path, rows, side, digest = chosen
        info = {"construction": "L-border and deletion", "source": str(path.relative_to(root)),
                "source_sha256": digest, "source_n": len(rows), "source_side": side,
                "layers": best[2], "deleted": best[1]}
        for _ in range(best[2]):
            rows, side = add_border(rows, side)
        rows = rows[:n]
    rows, side = wrap(rows)
    info["side"] = side
    return format_packing(rows, side), info


def prepare(root):
    from slp_refine import load, repair, save
    from accept_candidates import measure

    manifest_path = root/"expanded_reference_bounds.json"
    if manifest_path.exists():
        raise SystemExit("Expanded references already exist; preserve them for stable comparisons.")
    records = catalogue(root)
    original = {n: s for n, s in records.items() if n <= PUBLISHED_MAX}
    if any(n in records for n in range(PUBLISHED_MAX+1, SEARCH_MAX+1)):
        raise SystemExit("Refusing to overwrite existing bounds.")
    entries = {}
    for n in range(PUBLISHED_MAX+1, SEARCH_MAX+1):
        grid = math.isqrt(n-1)+1
        bound, deleted, layers, source = min(
            [(Fraction(grid), grid*grid-n, 0, None)] +
            [(*extend_bound(m, s, n), m) for m, s in original.items()],
            key=lambda p: (p[0], p[1], p[2]))
        text, seed_info = construct_seed(root, n, references_only=True)
        path = root/f"records/n{n}.txt"
        path.write_text(text)
        # Preserve exact half-integer grids; repair imported float poses.
        if seed_info["construction"] != "grid":
            z, side = repair(load(path))
            save(path, z, side)
        measured = measure(path, n)
        value = str(bound.numerator) if bound.denominator == 1 else f"{float(bound):.14f}"
        entries[str(n)] = {"bound": value, "type": "derived reference upper bound",
            "source_n": source, "source_bound": str(original[source]) if source else None,
            "layers": layers, "deleted": deleted, "grid_optimal": math.isqrt(n)**2 == n,
            "seed": seed_info, "seed_side": str(measured),
            "seed_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        print(f"n={n} bound={value} seed={float(measured):.12f}", flush=True)
    manifest = {"published_range_max": PUBLISHED_MAX, "search_max": SEARCH_MAX,
        "source": "https://kingbird.myphotos.cc/packing/squares_in_squares.html",
        "construction": "m -> m+2*floor(s)+1, s -> s+1; repeat and delete surplus squares",
        "notice": "Constructed comparisons for 325..400; not surveyed published records.",
        "entries": entries}
    manifest_path.write_text(json.dumps(manifest, indent=2)+"\n")
    records.update({int(n): Fraction(e["bound"]) for n, e in entries.items()})
    # Atomic replacement: the running coordinator can finish its old jobs.
    old = (root/"records.txt").read_text()
    comments = "\n".join(line for line in old.splitlines() if line.startswith("#"))
    comments += "\n# n=325..400: derived L-border/grid reference bounds, NOT published records; see expanded_reference_bounds.json"
    values = {int(n): s for line in old.splitlines() if line and not line.startswith("#")
              for n, s in [line.split()]}
    values.update({int(n): e["bound"] for n, e in entries.items()})
    temporary = root/"records.txt.expanding"
    temporary.write_text(comments+"\n"+"".join(f"{n} {values[n]}\n" for n in sorted(values)))
    temporary.replace(root/"records.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    args = parser.parse_args()
    if args.prepare:
        prepare(ROOT)
