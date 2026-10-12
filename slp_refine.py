#!/usr/bin/env python3
"""Refine a packing with trust-region sequential linear programming.

Each nearby pair keeps its current separating axis for one LP step. Four
support-corner inequalities avoid differentiating abs(sin(theta)) at zero,
so aligned squares can rotate without an arbitrary one-sided derivative.
All pairs are checked again after each step, independently of the LP model.
Requires numpy and scipy; output is a numerical candidate, not an exact proof.
"""
import argparse
import json
from pathlib import Path
import time
import warnings

import numpy as np
from scipy.optimize import OptimizeWarning, linprog
from scipy.sparse import coo_matrix


def load(path):
    z = np.loadtxt(path, comments="#", ndmin=2)
    if z.shape[1] != 3 or not len(z) or not np.isfinite(z).all():
        raise ValueError("Expected finite x, y, theta rows")
    return z


def wrap(z):
    z = z.copy()
    h = (np.abs(np.cos(z[:, 2])) + np.abs(np.sin(z[:, 2]))) / 2
    lo = np.min(z[:, :2] - h[:, None], axis=0)
    hi = np.max(z[:, :2] + h[:, None], axis=0)
    z[:, :2] -= lo
    return z, float(np.max(hi - lo))


def pair_geometry(z):
    i, j = np.triu_indices(len(z), 1)
    d = z[j, :2] - z[i, :2]
    a = np.stack([z[i, 2], z[i, 2] + np.pi / 2,
                  z[j, 2], z[j, 2] + np.pi / 2], axis=1)
    u = np.stack([np.cos(a), np.sin(a)], axis=2)
    p = np.abs(np.einsum("pk,plk->pl", d, u))
    da = z[j, 2] - z[i, 2]
    h = .5 + .5 * (np.abs(np.cos(da)) + np.abs(np.sin(da)))
    return i, j, p, h


def repair(z):
    """Uniformly separate centers, then shrink-wrap; recheck every pair."""
    z = z.copy()
    _, _, p, h = pair_geometry(z)
    projected = np.max(p, axis=1)
    if len(projected) and np.any(projected == 0):
        raise ValueError("Coincident centers cannot be repaired by scaling")
    ratio = float(np.max(h / projected)) if len(projected) else 1.0
    factor = max(1., ratio) * (1. + 2e-13)
    center = np.mean(z[:, :2], axis=0)
    z[:, :2] = center + factor * (z[:, :2] - center)
    z, side = wrap(z)
    _, _, p, h = pair_geometry(z)
    if np.any(np.max(p, axis=1) < h):
        raise ValueError("Repair left an overlap")
    return z, side


def linear_model(z, side, radius):
    n = len(z)
    rows, cols, vals, rhs = [], [], [], []

    def add(gap, entries):
        # The largest possible motion of a corner in this trust region is
        # smaller than 4*radius for either a wall or a pair constraint.
        if gap > 8 * radius + 1e-6:
            return
        r = len(rhs)
        rhs.append(gap + 2e-12)
        for c, v in entries:
            rows.append(r)
            cols.append(c)
            vals.append(-v)

    c, s = np.cos(z[:, 2]), np.sin(z[:, 2])
    for i in range(n):
        for sc in (-1, 1):
            for ss in (-1, 1):
                h = .5 * (sc * c[i] + ss * s[i])
                dh = .5 * (-sc * s[i] + ss * c[i])
                for k in (0, 1):
                    add(z[i, k] - h, [(3*i+k, 1), (3*i+2, -dh)])
                    add(side-z[i, k]-h,
                        [(3*n, 1), (3*i+k, -1), (3*i+2, -dh)])

    ii, jj = np.triu_indices(n, 1)
    d = z[jj, :2] - z[ii, :2]
    close = np.sum(d*d, axis=1) < (2 + 4 * radius)**2
    for i, j in zip(ii[close], jj[close]):
        delta = z[j, :2] - z[i, :2]
        axes = [(c[i], s[i]), (-s[i], c[i]),
                (c[j], s[j]), (-s[j], c[j])]
        projections = [delta @ u for u in axes]
        axis = int(np.argmax(np.abs(projections)))
        if axis >= 2:
            i, j = j, i
            delta = -delta
        ux, uy = axes[axis]
        if delta @ (ux, uy) < 0:
            ux, uy = -ux, -uy
        p = delta @ (ux, uy)
        dp = delta @ (-uy, ux)
        ca = c[j]*ux + s[j]*uy
        sa = s[j]*ux - c[j]*uy
        for sc in (-1, 1):
            for ss in (-1, 1):
                h = .5 * (sc * ca + ss * sa)
                dh = .5 * (-sc * sa + ss * ca)
                add(p-.5-h, [(3*i, -ux), (3*i+1, -uy),
                              (3*j, ux), (3*j+1, uy),
                              (3*i+2, dp+dh), (3*j+2, -dh)])
    matrix = coo_matrix((vals, (rows, cols)), shape=(len(rhs), 3*n+1)).tocsr()
    return matrix, np.array(rhs)


def translation_polish(z, radius=.05, seconds=10.):
    """An exact LP for the selected separating axes with angles held fixed.

    Rotations introduce second-order errors in the main LP's contact model.
    Correct them by moving individual centers before resorting to uniform
    expansion. Independent all-pairs repair remains the final gate.
    """
    z, side = wrap(z)
    n = len(z)
    rows, cols, vals, b = [], [], [], []

    def add(gap, entries):
        r = len(b)
        b.append(gap)
        for column, value in entries:
            rows.append(r)
            cols.append(column)
            vals.append(-value)

    half = .5*(np.abs(np.cos(z[:, 2]))+np.abs(np.sin(z[:, 2])))
    for i in range(n):
        for k in (0, 1):
            add(z[i, k]-half[i], [(2*i+k, 1)])
            add(side-z[i, k]-half[i], [(2*n, 1), (2*i+k, -1)])
    ii, jj, projection, h = pair_geometry(z)
    distance = np.linalg.norm(z[jj, :2]-z[ii, :2], axis=1)
    for index in np.flatnonzero(distance < 2+4*radius):
        i, j = ii[index], jj[index]
        axis = int(np.argmax(projection[index]))
        angle = z[i if axis < 2 else j, 2]+(axis % 2)*np.pi/2
        ux, uy = np.cos(angle), np.sin(angle)
        dx, dy = z[j, :2]-z[i, :2]
        if dx*ux+dy*uy < 0:
            ux, uy = -ux, -uy
        add(dx*ux+dy*uy-h[index], [(2*i, -ux), (2*i+1, -uy),
                                     (2*j, ux), (2*j+1, uy)])
    a = coo_matrix((vals, (rows, cols)), shape=(len(b), 2*n+1)).tocsr()
    objective = np.zeros(2*n+1)
    objective[-1] = 1
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Unrecognized options detected:.*threads",
                                category=OptimizeWarning)
        lp = linprog(objective, A_ub=a, b_ub=b, bounds=[(-radius, radius)]*(2*n+1),
                     method="highs", options={"threads": 1, "time_limit": max(.01, seconds),
                     "primal_feasibility_tolerance": 1e-10, "dual_feasibility_tolerance": 1e-10})
    if lp.success:
        z[:, :2] += lp.x[:-1].reshape(-1, 2)
    return repair(z)


def refine(z, iterations=150, radius=.02, seconds=120., verbose=False, translations=False):
    z, side = repair(z)
    start = time.monotonic()
    ceiling = radius
    objective = np.zeros(3*len(z)+1)
    objective[-1] = 1.
    history = []
    for step in range(iterations):
        if time.monotonic() - start >= seconds or radius < 2e-8:
            break
        a, b = linear_model(z, side, radius)
        # A campaign runs one process per core. Pass the native HiGHS option
        # through SciPy so each LP does not create another pool of CPU threads.
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="Unrecognized options detected:.*threads",
                                    category=OptimizeWarning)
            lp = linprog(objective, A_ub=a, b_ub=b,
                         bounds=[(-radius, radius)] * len(objective), method="highs",
                         options={"dual_feasibility_tolerance": 1e-9,
                                  "primal_feasibility_tolerance": 1e-9,
                                  "threads": 1,
                                  "time_limit": max(.01, seconds-(time.monotonic()-start))})
        if not lp.success:
            radius *= .5
            continue
        proposal = z + lp.x[:-1].reshape(-1, 3)
        trial, candidate = repair(proposal)
        if translations:
            corrected, corrected_side = translation_polish(
                proposal, radius=max(radius, .001),
                seconds=max(.01, seconds-(time.monotonic()-start)))
            if corrected_side < candidate:
                trial, candidate = corrected, corrected_side
        gain = side - candidate
        accepted = gain > 1e-11
        history.append({"step": step, "side": candidate, "radius": radius,
                        "predicted_gain": -float(lp.x[-1]), "accepted": accepted})
        if verbose and (accepted or step % 10 == 0):
            print(f"step={step} side={candidate:.14f} gain={gain:+.3e} "
                  f"radius={radius:.2e} accepted={accepted}", flush=True)
        if accepted:
            z, side = trial, candidate
            if gain > .25 * -lp.x[-1]:
                radius = min(ceiling, radius * 1.3)
        else:
            radius *= .5
    return z, side, history


def save(path, z, side):
    np.savetxt(path, z, fmt="%.17e", header=f"n = {len(z)}\ns = {side:.15f}\nx y theta(rad)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=150)
    parser.add_argument("--seconds", type=float, default=120)
    parser.add_argument("--radius", type=float, default=.02)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--translations", action="store_true",
                        help="Repair each rotation step with a fixed-angle translation LP")
    args = parser.parse_args()
    if args.input.resolve() == args.out.resolve():
        parser.error("Use a separate output path; certify before replacing a record")
    original = load(args.input)
    _, before = wrap(original)
    z, side, history = refine(original, args.iterations, args.radius, args.seconds,
                             args.verbose, args.translations)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if side < before:
        save(args.out, z, side)
    else:
        args.out.write_bytes(args.input.read_bytes())
        side = before
    summary = {"input": str(args.input), "n": len(z), "before": before,
               "after": side, "gain": before-side, "translations": args.translations,
               "history": history}
    args.out.with_suffix(".json").write_text(json.dumps(summary, indent=2)+"\n")
    print(f"n={len(z)} before={before:.14f} after={side:.14f} gain={before-side:.6e}")


if __name__ == "__main__":
    main()
