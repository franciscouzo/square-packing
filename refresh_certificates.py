#!/usr/bin/env python3
"""Rebuild certificates/ for every installed packing nN.txt.

Each count gets one certificate in Evan Daniel's .cert format (rational
centres and t = tan(theta/2)), plus one current metadata file at nN.json:
  - "exact optimum": found/nN_s<side>.exact.cert from exact_finish.py, within
    about 1e-19 of the packing's KKT point (run first when missing);
  - "rational witness": found/nN_s<side>.witness.cert, the installed decimal
    packing as rationals with adaptive dilation starting at 1+1e-12 and
    increasing until exact verification succeeds, when the exact solve
    does not certify a smaller side.
With --fast, a packing whose exact solve has not run yet gets its rational
witness now (the next refresh replaces it). Both kinds pass verify.py
(sqpack) and Evan Daniel's verify_cert.py. The
README table gives each count's standing from known_best.json. Run
import_external.py --offline first so the standings are current.
"""
import hashlib
import json
import math
import shutil
from fractions import Fraction
from pathlib import Path

import exact_finish
from expanded_comparisons import comparison_entry, external_comparison

ROOT = Path(__file__).resolve().parent
STANDING = {"best known": "best known", "tied (within 1e-10)": "registered / tied", "superseded": "superseded"}


FAST = "--fast" in __import__("sys").argv  # never run the exact solve inline; witness meanwhile


def certificate_for(n):
    packing = ROOT/f"n{n}.txt"
    digest = hashlib.sha256(packing.read_bytes()).hexdigest()
    side = next(float(l.split("=")[1]) for l in packing.read_text().splitlines() if l.startswith("# s ="))
    exact = ROOT/"found"/f"n{n}_s{side:.12f}.exact.json"
    if not exact.exists() and not FAST:
        exact_finish.finish(n, print)
    meta = json.loads(exact.read_text()) if exact.exists() else {}
    if meta.get("ok") and meta.get("input_sha256") == digest:
        return ROOT/"found"/f"n{n}_s{side:.12f}.exact.cert", Fraction(meta["certified_side"]), "exact optimum"
    meta = exact_finish.witness(n)
    if meta and meta.get("input_sha256") == digest:
        return ROOT/"found"/f"n{n}_s{side:.12f}.witness.cert", Fraction(meta["certified_side"]), "rational witness"
    raise SystemExit(f"n={n}: no certificate for the installed packing")


def current_metadata(n, src, side, kind):
    """Publish current hashes and credit without copying historical certificates."""
    packing = ROOT/f"n{n}.txt"
    digest = hashlib.sha256(packing.read_bytes()).hexdigest()
    proof = json.loads(src.with_suffix(".json").read_text())
    assert proof["input_sha256"] == digest
    assert Fraction(proof["certified_side"]) == side
    assert proof.get("ok") if kind == "exact optimum" else proof.get("valid")
    header = next(float(line.split("=")[1]) for line in packing.read_text().splitlines()
                  if line.startswith("# s ="))
    path = ROOT/"found"/f"n{n}_s{header:.12f}.certificate.json"
    current = json.loads(path.read_text()) if path.exists() else {}
    previous = ROOT/"certificates"/f"n{n}.json"
    origin = json.loads(previous.read_text()).get("origin", {}) if previous.exists() else {}
    # Extract attribution while the local search archive is available. The
    # published metadata does not depend on parent files being in the repository.
    pending, seen = [current], set()
    lineage = []
    while pending:
        item = pending.pop()
        lineage.append(item)
        parents = []
        if item.get("seed_inherited_from"):
            parents.append(item["seed_inherited_from"])
        polished = item.get("exact_polish_of", {}).get("file")
        if polished:
            parents.append(str(Path(polished).with_suffix(".certificate.json")))
        for parent in parents:
            if Path(parent).name != parent or parent in seen:
                continue
            seen.add(parent)
            parent_path = ROOT/"found"/parent
            if parent_path.exists():
                pending.append(json.loads(parent_path.read_text()))
    for field in ("seed_credit", "seed_certificate"):
        value = next((item[field] for item in lineage if item.get(field)), None)
        if value:
            origin[field] = value
    construction = next((item['construction'] for item in lineage if item.get('construction')), None)
    if construction:
        origin['construction'] = construction
    job = current.get("search_job") or {}
    if job:
        origin["search_job"] = {key: job[key] for key in
                                ("id", "method", "source", "source_origin", "source_sha256", "constructed_seed")
                                if key in job}
    web = next((item["web_submission"] for item in lineage if item.get("web_submission")), None)
    if web:
        origin["web_seed"] = {key: web[key] for key in
                              ("id", "n", "side", "method", "attribution", "name", "received", "original_packing_sha256")
                              if key in web}
    web_seed = origin.get("web_seed", {})
    owner_names = {"franciscouzo", "francisco couzo"}
    if any(str(web_seed.get(key, "")).strip().casefold() in owner_names
           for key in ("attribution", "name")):
        web_seed.pop("attribution", None)
        web_seed.pop("name", None)
    metadata = {"n": n, "packing": packing.name, "packing_sha256": digest,
                "certificate": f"certificates/n{n}.cert",
                "certificate_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
                "rational_side": str(side), "kind": kind, "origin": origin}
    if proof.get("dilation"):
        metadata["dilation"] = proof["dilation"]
    return metadata


def main():
    known = json.loads((ROOT/"known_best.json").read_text())
    counts = sorted(int(p.stem[1:]) for p in ROOT.glob("n[0-9]*.txt"))
    chosen = {n: certificate_for(n) for n in counts}
    out = ROOT/"certificates"
    out.mkdir(exist_ok=True)
    for old in out.glob("n*.cert"):
        old.unlink()
    for old in out.glob("n[0-9]*.json"):
        if int(old.stem[1:]) not in counts:
            old.unlink()
    rows = []
    for n, (src, S, kind) in chosen.items():
        dst = out/f"n{n}.cert"
        shutil.copy2(src, dst)
        metadata = current_metadata(n, src, S, kind)
        (out/f"n{n}.json").write_text(json.dumps(metadata, indent=2)+"\n")
        e = known["entries"].get(str(n), {})
        if n > 324:
            standing = external_comparison(str(S), comparison_entry(known, n))[2].replace('**', '')
        else:
            standing = STANDING.get(e.get("own_status"), "—")
        rows.append((n, str(S), math.ceil(S*10**12)/10**12, kind, standing,
                     hashlib.sha256(dst.read_bytes()).hexdigest()))
    lines = ["# Certificates", "",
             "One certificate per packing `nN.txt` in this repository, in Evan Daniel's format",
             "([evand/square-packing](https://github.com/evand/square-packing), MIT): `n S`, then one line per",
             "square with a rational centre (x, y) and t = tan(θ/2), so that (cos θ, sin θ) = ((1−t²)/(1+t²),",
             "2t/(1+t²)) and every square is exactly a unit square inside the open box (0, S)². Each proves s(n) ≤ S.", "",
             "Where provided, `nN.json` records the current packing and certificate hashes, exact bound, and seed credit.",
             "Only current certificates and provenance are published; earlier versions are in Git history.", "",
             "- **exact optimum**: written by Evan Daniel's exact contact solver (`search/exact`, commit 77f3c0ab);",
             "  S lies within about 1e-19 of the packing's exact KKT point.",
             "- **rational witness**: the decimal packing as rationals, with an adaptive rational dilation of",
             "  the centres, where the exact solve did not certify a smaller side. The dilation starts at",
             "  1+1e-12 and increases until exact verification succeeds; the amount varies by certificate.", "",
             "Check with his verifier (standard library only):", "",
             "```sh", "python3 search/exact/verify_cert.py nN.cert   # in a checkout of evand/square-packing", "```", "",
             "Every certificate also replays as valid in exact rational arithmetic with `verify.py` from",
             "[jlevy/squares](https://github.com/jlevy/squares) (`sqpack.verify`). The standing is against the",
             "jlevy/squares register and verified published submissions, as in the README. Above n=324,",
             "the comparison is with reviewed published bounds where available, otherwise only with",
             "the frozen derived reference; it is not an optimality claim.", "",
             "| n | S (exact) | rounded up | certificate | standing | SHA-256 |", "|---:|---|---|---|---|---|"]
    lines += [f"| {n} | `{s}` | {up:.12f} | {kind} | {standing} | `{sha[:16]}` |" for n, s, up, kind, standing, sha in rows]
    (out/"README.md").write_text("\n".join(lines)+"\n")
    print(f"certificates: {len(rows)} ({sum(r[3] == 'exact optimum' for r in rows)} exact optimum, "
          f"{sum(r[3] == 'rational witness' for r in rows)} rational witness)")
    return rows


if __name__ == "__main__":
    main()
