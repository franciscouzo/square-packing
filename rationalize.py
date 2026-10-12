#!/usr/bin/env python3
"""Turn a float packing into an exactly-rational one and certify it.

Angles become rational half-angle tangents t, so cos = (1-t^2)/(1+t^2) and
sin = 2t/(1+t^2) are rational and every square is *exactly* a unit square.
Centers become rationals, then are scaled apart just enough that the rounding
cannot create an overlap. The result is checked in exact rational arithmetic by
the independent verifier from github.com/jlevy/squares (sqpack.verify).
"""
import sys, math
from fractions import Fraction as F

sys.path.insert(0, sys.argv[3] if len(sys.argv) > 3 else '.')
from verify import verify_packing  # sqpack.verify, copied in as an independent oracle

def sign(v):
    return (v > 0) - (v < 0)

def load(path):
    out = []
    for line in open(path):
        if line.startswith('#') or not line.strip():
            continue
        x, y, t = (float(v) for v in line.split()[:3])
        out.append((x, y, t))
    return out

def build(poses, tden, cden, grow):
    sq = []
    cs = []
    for x, y, th in poses:
        t = F(math.tan(th / 2)).limit_denominator(tden)
        d = 1 + t * t
        c, s = (1 - t * t) / d, 2 * t / d
        cs.append((F(x).limit_denominator(cden), F(y).limit_denominator(cden), c, s))
    cx = sum(p[0] for p in cs) / len(cs)
    cy = sum(p[1] for p in cs) / len(cs)
    for X, Y, c, s in cs:
        X = cx + (X - cx) * grow
        Y = cy + (Y - cy) * grow
        corners = []
        for dx, dy in ((F(-1,2), F(-1,2)), (F(1,2), F(-1,2)), (F(1,2), F(1,2)), (F(-1,2), F(1,2))):
            corners.append((X + dx * c - dy * s, Y + dx * s + dy * c))
        sq.append(corners)
    x0 = min(p[0] for q in sq for p in q)
    y0 = min(p[1] for q in sq for p in q)
    sq = [[(px - x0, py - y0) for px, py in q] for q in sq]
    side = max(max(max(px, py) for px, py in q) for q in sq)
    return sq, side

poses = load(sys.argv[1])
record = F(sys.argv[2]) if len(sys.argv) > 2 else None
for grow_exp in range(12, 3, -1):
    grow = 1 + F(1, 10**grow_exp)
    sq, side = build(poses, 10**10, 10**13, grow)
    rep = verify_packing(sq, side, sign)
    if rep.valid:
        print(f"n={rep.n} EXACT-VALID  side = {float(side):.15f}")
        print(f"  rational side  = {side.numerator}/{side.denominator}")
        print(f"  pairs tested={rep.pairs_tested} touching={rep.touching_pairs} container contacts={rep.container_contacts}")
        if record is not None:
            print(f"  record         = {float(record):.15f}   margin = {float(record - side):+.3e}")
        break
    print(f"  grow=1+1e-{grow_exp}: {len(rep.failures)} failures, e.g. {rep.failures[0]}")
else:
    print("no rational witness found")
