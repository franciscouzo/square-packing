#!/usr/bin/env python3
"""Flatten squares whose tilt is numerical dust, letting them sit a hair looser.

Sliding squares into contact can jam one a few times 1e-11 too close to a diagonal
neighbour, and it then has to lean by a billionth of a degree. Setting such a square
exactly axis-aligned and pushing it out of the resulting sub-nanometre overlap costs
nothing: the motion is far below the packing's own slack, and the container is
unchanged. Only the squares below the cutoff move.

Usage: flatten_dust.py IN.txt OUT.txt [cutoff_degrees]
"""
import math, sys

src, dst = sys.argv[1], sys.argv[2]
cutoff = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-6
sq = [list(float(v) for v in l.split()[:3])
      for l in open(src) if not l.startswith('#') and l.strip()]
ext = lambda t: 0.5 * (abs(math.cos(t)) + abs(math.sin(t)))
before = max(max(x + ext(t) for x, y, t in sq), max(y + ext(t) for x, y, t in sq))

def corners(x, y, t):
    c, s = math.cos(t), math.sin(t)
    return [(x + dx * c - dy * s, y + dx * s + dy * c)
            for dx, dy in ((-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5))]

def penetration_pose(i, j):
    """Depth and push-out direction for square i against j, or None if disjoint.

    Uses the same support-function test as the Rust verifier (0.5 + h(psi) - |p|
    per axis) rather than projecting corners: the corner form disagrees with it at
    the 1e-16 level, which is enough to leave a residual overlap behind.
    """
    xi, yi, ti = sq[i]
    xj, yj, tj = sq[j]
    ci, si = math.cos(ti), math.sin(ti)
    cj, sj = math.cos(tj), math.sin(tj)
    dx, dy = xj - xi, yj - yi
    best = None
    for (oc, os_, tc, ts) in ((ci, si, cj, sj), (cj, sj, ci, si)):
        for k in range(2):
            uc, us = (oc, os_) if k == 0 else (-os_, oc)
            p = dx * uc + dy * us
            pc = uc * tc + us * ts
            ps = us * tc - uc * ts
            o = 0.5 + 0.5 * (abs(pc) + abs(ps)) - abs(p)
            if o <= 0:
                return None
            if best is None or o < best[0]:
                sign = -1.0 if p > 0 else 1.0     # push i away from j
                best = (o, uc * sign, us * sign)
    return best


X0 = min(x - ext(t) for x, y, t in sq)
Y0 = min(y - ext(t) for x, y, t in sq)
X1 = max(x + ext(t) for x, y, t in sq)
Y1 = max(y + ext(t) for x, y, t in sq)

def outside(i):
    """Does square i stick out of the box the packing started in?"""
    x, y, t = sq[i]
    e = ext(t)
    return x - e < X0 - 1e-15 or y - e < Y0 - 1e-15 or x + e > X1 + 1e-15 or y + e > Y1 + 1e-15

free = [i for i, (x, y, t) in enumerate(sq) if t != 0.0 and abs(math.degrees(t)) < cutoff]
free_set = set(free)
# clearance must beat the float spacing at these coordinates, which grows with the container
clear = max(1e-16, before * 1e-15)
for i in free:
    sq[i][2] = 0.0


def spread():
    """Push the flattened squares out of the overlaps that flattening created."""
    for _ in range(500):
        moved = 0.0
        for i in free:
            ci = corners(*sq[i])
            for j in range(len(sq)):
                if j == i or math.hypot(sq[j][0] - sq[i][0], sq[j][1] - sq[i][1]) > 2:
                    continue
                p = penetration_pose(i, j)
                if p:
                    d, nx, ny = p
                    # when both squares may move, each gives half, or they shove
                    # each other back and forth and settle overlapping by the step
                    step = (d + clear) * (0.5 if j in free_set else 1.0)
                    sq[i][0] += nx * step
                    sq[i][1] += ny * step
                    e = ext(sq[i][2])   # the starting box is a wall: never grow the side
                    sq[i][0] = min(max(sq[i][0], X0 + e), X1 - e)
                    sq[i][1] = min(max(sq[i][1], Y0 + e), Y1 - e)
                    moved += step
                    ci = corners(*sq[i])
        if moved < 1e-18:
            return


spread()

# Guarantee validity: a square that could not be freed goes back exactly as it was.
orig = [list(map(float, l.split()[:3]))
        for l in open(src) if not l.startswith('#') and l.strip()]
for _ in range(len(free) + 1):   # each pass gives up one square, so allow them all
    # Revert the single worst offender, then let the rest settle again. Reverting
    # every clashing square at once lets one square that truly cannot straighten
    # drag back the whole group it touches, and those are often free once it is
    # back in place.
    worst = None
    for i in list(free):
        ci = corners(*sq[i])
        deepest = 0.0
        for j in range(len(sq)):
            if j == i or math.hypot(sq[j][0] - sq[i][0], sq[j][1] - sq[i][1]) > 2:
                continue
            pen = penetration_pose(i, j)
            if pen and pen[0] > deepest:
                deepest = pen[0]
        if outside(i):
            deepest = max(deepest, 1.0)   # sticking out is worse than any overlap
        if deepest > 0 and (worst is None or deepest > worst[0]):
            worst = (deepest, i)
    if worst is None:
        break
    i = worst[1]
    sq[i] = list(orig[i])
    free.remove(i)
    free_set.discard(i)
    spread()

x0 = min(x - ext(t) for x, y, t in sq)
y0 = min(y - ext(t) for x, y, t in sq)
side = max(max(x + ext(t) for x, y, t in sq) - x0, max(y + ext(t) for x, y, t in sq) - y0)
with open(dst, 'w') as f:
    f.write(f"# n = {len(sq)}\n# s = {side:.15f}\n# x y theta(rad)\n")
    for x, y, t in sq:
        f.write(f"{x - x0:.17e} {y - y0:.17e} {t:.17e}\n")
print(f"flattened {len(free)} dust squares (reverted {sum(1 for i,(a,b) in enumerate(zip(sq,orig)) if a[2] != 0.0 and abs(math.degrees(b[2])) < cutoff and b[2] != 0.0)}); side {before:.15f} -> {side:.15f} ({side - before:+.3e})")
