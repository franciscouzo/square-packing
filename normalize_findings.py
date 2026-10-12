#!/usr/bin/env python3
"""Orient a packing like a reference, using all eight square symmetries.

Hungarian matching minimizes center displacement plus mean squared corner
displacement due to relative square angles. Square labels do not affect the
score. Output rows follow the matched reference rows. This does not optimize
the packing or change individual square orientations relative to one another.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import numpy as np
from scipy.optimize import linear_sum_assignment
from slp_refine import load, repair, save, wrap


def transform(z, side, turns, mirror):
    out = z.copy()
    if mirror:
        out[:, 0] = side-out[:, 0]
        out[:, 2] = -out[:, 2]
    for _ in range(turns):
        out[:, 0], out[:, 1] = side-out[:, 1].copy(), out[:, 0].copy()
    # A square's angle already represents the same shape modulo pi/2.
    # Avoid adding pi/2 and introducing needless trigonometric roundoff.
    return out


def align(z, reference):
    if len(z) != len(reference):
        raise ValueError("Packing and reference must have the same square count")
    base, side = wrap(z)
    ref, ref_side = wrap(reference)
    best = None
    scores = []
    for mirror in (False, True):
        for turns in range(4):
            candidate = transform(base, side, turns, mirror)
            delta_xy = ((candidate[:, None, :2]-side/2)
                        -(ref[None, :, :2]-ref_side/2))
            delta_angle = (candidate[:, None, 2]-ref[None, :, 2]+np.pi/4) % (np.pi/2)-np.pi/4
            cost = np.sum(delta_xy**2, axis=2)+1-np.cos(delta_angle)
            rows, cols = linear_sum_assignment(cost)
            score = float(cost[rows, cols].sum())
            name = ("mirror_x_then_" if mirror else "")+f"rotate_{90*turns}"
            if not mirror and not turns:
                name = "identity"
            scores.append({"symmetry": name, "score": score})
            # Prefer the identity on ties, making repeated normalization stable.
            if best is None or score < best[0]-1e-11:
                order = rows[np.argsort(cols)]
                best = (score, candidate[order], name, order)
    score, out, name, order = best
    # Do not perturb an already canonical file by translating its roundoff.
    if name == "identity":
        out = z[order].copy()
    return out, {"symmetry": name, "score_before": scores[0]["score"],
                 "score_after": score, "scores": scores,
                 "reordered": bool(np.any(order != np.arange(len(z)))),
                 "rms_corner_displacement": float(np.sqrt(score/len(z)))}


def normalize(source, reference, output, binary):
    original = load(source)
    aligned, report = align(original, load(reference))
    report.update({"reference": str(reference),
                   "reference_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
                   "original_sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
    if np.array_equal(original, aligned):
        if source != output:
            output.write_bytes(source.read_bytes())
        report["changed"] = False
        return report
    _, side_before = wrap(original)
    _, side = wrap(aligned)
    save(output, aligned, side)
    numerical = subprocess.check_output([str(binary), "verify", str(output)], text=True)
    overlap = float(re.search(r"max_pair_overlap=([\de.+-]+)", numerical)[1])
    if overlap > 0:
        # Reflections can round a center subtraction by an ulp. Repair only
        # when needed, and prohibit any material change to the packing size.
        aligned, side = repair(aligned)
        save(output, aligned, side)
    numerical = subprocess.check_output([str(binary), "verify", str(output)], text=True)
    overlap = float(re.search(r"max_pair_overlap=([\de.+-]+)", numerical)[1])
    if overlap != 0 or abs(side-side_before) > 1e-9:
        raise ValueError(f"Normalization changed geometry beyond roundoff: {numerical}")
    report.update({"changed": True, "side_before": side_before, "side_after": side,
                   "roundoff_repair": side-side_before})
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("reference", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--binary", type=Path, default=Path(__file__).resolve().parent/"target/release/sqpack")
    args = parser.parse_args()
    if args.input.resolve() == args.out.resolve():
        parser.error("Use a separate output; exact certification precedes installation")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    print(json.dumps(normalize(args.input, args.reference, args.out, args.binary.resolve())))


if __name__ == "__main__":
    main()
