#!/usr/bin/env python3
"""Install numerical improvements only after an exact rational witness succeeds.

Usage: python3 accept_candidates.py CANDIDATE_DIRECTORY
Requires the existing Rust binary and rationalize.py's independent verify.py.
Archived numerical poses, certificate logs, hashes, and rational side lengths
make every accepted change reproducible. Existing better files are preserved.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from expand_search import SEARCH_MAX


BIN = Path(__file__).resolve().parent / "target/release/sqpack"
EXTERNAL_MARGIN = Fraction(1, 10**7)
ROOT = Path(__file__).resolve().parent


def measure(path, expected_n):
    poses = [list(map(float, line.split())) for line in path.read_text().splitlines()
             if line.strip() and not line.startswith("#")]
    if len(poses) != expected_n or any(len(p) != 3 or not all(map(math.isfinite, p)) for p in poses):
        raise ValueError(f"{path}: invalid pose data or square count")
    result = subprocess.check_output([str(BIN), "verify", str(path)], text=True)
    match = re.search(r"n=(\d+) max_pair_overlap=([\de.+-]+) bbox_side=([\d.]+)", result)
    if not match or int(match[1]) != expected_n or float(match[2]) != 0:
        raise ValueError(f"{path}: invalid geometry: {result}")
    return Fraction(match[3])


def orient(path, n):
    reference = ROOT/"records"/f"n{n}.txt"
    if not reference.exists():
        # No catalogue pose (e.g. counts the catalogue lists as the grid): align
        # to the external packing we started from, else leave the pose as found.
        from search_methods import best_source
        candidates = [ROOT/"external/seeds"/f"n{n}.txt", *sorted((ROOT/"external/seeds/old").glob(f"n{n}_*.txt"))]
        reference = next((c for c in candidates if c.exists()), None)
        if reference is None:
            return {"symmetry": "identity", "changed": False, "reference": None,
                    "note": "no orientation reference for this count"}
    output = path.with_suffix(".oriented.txt")
    process = subprocess.run([str(ROOT/".venv/bin/python"), str(ROOT/"normalize_findings.py"),
                              str(path), str(reference), "--out", str(output)],
                             capture_output=True, text=True, check=True)
    report = json.loads(process.stdout)
    output.replace(path)
    return report


def certify(path, n, threshold):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    # Adjacent logs or certificate JSONs are metadata, never proof of validity:
    # recompute the exact check for every candidate we intend to install.
    process = subprocess.run(["python3", str(ROOT/"rationalize.py"), str(path),
                              str(float(threshold)), str(ROOT)],
                             text=True, capture_output=True, check=True)
    log = process.stdout
    match = re.search(r"rational side  = (\d+/\d+)", log)
    if not match or f"n={n} EXACT-VALID" not in log:
        raise ValueError(f"{path}: exact verification failed\n{log}\n{process.stderr}")
    return {"sha256": digest, "rational_side": match[1], "log": log}


def known_best(n):
    """Best known upper bound elsewhere (known_best.json: the register or a
    verified external certificate), or None. Since 2026-10-08 a candidate must
    beat it as well as our own packing: improving one of our superseded
    packings is not a result."""
    bounds = []
    path = ROOT/"known_best.json"
    if path.exists():
        entry = json.loads(path.read_text())["entries"].get(str(n))
        if entry:
            bounds.append(Fraction(str(entry["side"])))
    # The complete verified index also retains constructions absent from the
    # register import, including exact Göbel families above the old range.
    path = ROOT/"upper_bounds.json"
    if path.exists():
        entry = json.loads(path.read_text())["entries"].get(str(n), {})
        for kind in ('verified', 'reported'):
            candidate = entry.get(kind)
            if candidate:
                try:
                    bounds.append(Fraction(candidate["bound"]))
                except ValueError:
                    # Algebraic public expressions remain in the reported
                    # lane; the verified lane retains its rational enclosure.
                    pass
    return min(bounds) if bounds else None


def accept(path, records):
    n = int(path.stem[1:])
    side = measure(path, n)
    destination = ROOT / path.name
    result_path = ROOT / "results" / path.name
    before = measure(destination, n) if destination.exists() else records[n]
    result_before = measure(result_path, n) if result_path.exists() else records[n]
    elsewhere = known_best(n)
    threshold = min(before, result_before, records[n], *([elsewhere] if elsewhere else []))
    if elsewhere is not None and elsewhere < min(before, result_before):
        # Beating another author's packing by rounding-level amounts is a
        # precision refinement of their construction, not a new result.
        threshold = elsewhere - EXTERNAL_MARGIN
    if side >= threshold - Fraction(1, 10**10):
        print(f"n={n}: no improvement over the best known packing", flush=True)
        return None
    orientation = orient(path, n)
    side = measure(path, n)
    if side >= threshold - Fraction(1, 10**10):
        print(f"n={n}: orientation roundoff consumed the improvement; skipped", flush=True)
        return None
    certificate = {**certify(path, n, threshold), "orientation": orientation}
    if elsewhere is not None:
        certificate["known_best_elsewhere"] = {"side": str(elsewhere), "table": "known_best.json",
                                               "table_sha256": hashlib.sha256((ROOT/"known_best.json").read_bytes()).hexdigest()}
    reference_manifest = ROOT/"expanded_reference_bounds.json"
    if 325 <= n <= SEARCH_MAX and reference_manifest.exists():
        entry = json.loads(reference_manifest.read_text())["entries"][str(n)]
        certificate["reference"] = {
            "kind": "derived reference upper bound, not a published-record comparison",
            "bound": entry["bound"], "source_n": entry["source_n"],
            "source_bound": entry["source_bound"], "layers": entry["layers"],
            "deleted": entry["deleted"],
            "manifest_sha256": hashlib.sha256(reference_manifest.read_bytes()).hexdigest()}
    cache_path = path.with_suffix(".certificate.json")
    cache_path.write_text(json.dumps(certificate, indent=2)+"\n")
    if Fraction(certificate["rational_side"]) >= threshold:
        print(f"n={n}: rational witness does not beat incumbent; skipped", flush=True)
        return None
    # Re-read immediately before changing files in case a running search has
    # improved an incumbent during the relatively slow exact check.
    current = measure(destination, n) if destination.exists() else records[n]
    current_result = measure(result_path, n) if result_path.exists() else records[n]
    if side >= min(current, current_result, threshold) - Fraction(1, 10**10):
        print(f"n={n}: local packing improved during certification; skipped", flush=True)
        return None
    archive = ROOT / "found" / f"n{n}_s{float(side):.12f}.txt"
    archive.parent.mkdir(exist_ok=True)
    result_path.parent.mkdir(exist_ok=True)
    shutil.copy2(path, archive)
    archive.with_suffix(".certificate.json").write_text(json.dumps(certificate, indent=2)+"\n")
    shutil.copy2(path, destination)
    subprocess.run([str(BIN), "svg", str(destination)], check=True)
    shutil.copy2(destination, result_path)
    shutil.copy2(destination.with_suffix(".svg"), result_path.with_suffix(".svg"))
    print(f"n={n}: {float(current):.12f} -> {float(side):.12f} (exact witness verified)", flush=True)
    return {"n": n, "before": str(current), "after": str(side),
            "source": str(path), **certificate}


def install_polished(limit=20):
    """Replace installed packings by their exact polish (exact_finish.py).

    The exact solve keeps the packing and lowers its side by 1e-12..1e-10; the
    decimal file is rebuilt from the exact certificate, repaired to zero float
    overlap, measured, and exactly re-certified like any candidate. Installed
    only when strictly smaller. Called only by the coordinator, so record
    installation stays serialized. Returns the counts changed.
    """
    import numpy as np
    from slp_refine import repair, save
    from import_external import read_cert_text
    changed = []
    work = ROOT/"experiments/polish"
    work.mkdir(parents=True, exist_ok=True)
    for destination in sorted(ROOT.glob("n[0-9]*.txt"), key=lambda p: int(p.stem[1:])):
        n = int(destination.stem[1:])
        data = destination.read_bytes()
        header = next(float(l.split("=")[1]) for l in data.decode().splitlines() if l.startswith("# s ="))
        old = ROOT/"found"/f"n{n}_s{header:.12f}"
        meta_path = Path(f"{old}.exact.json")
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        if (not meta.get("ok") or meta.get("input_sha256") != hashlib.sha256(data).hexdigest()
                or meta.get("polish_installed") or meta.get("polish_skipped")):
            continue
        side = measure(destination, n)
        _, _, squares = read_cert_text(Path(f"{old}.exact.cert"))
        z = np.array([(float(x), float(y), 2*float(np.arctan(float(t)))) for x, y, t in squares])
        z, polished = repair(z)
        candidate = work/destination.name
        save(candidate, z, polished)
        try:
            new_side = measure(candidate, n)
        except ValueError as exc:
            meta["polish_skipped"] = f"float file invalid: {exc}"
            meta_path.write_text(json.dumps(meta, indent=2, default=str)+"\n")
            continue
        if new_side >= side:
            meta["polish_skipped"] = f"no float gain ({float(new_side):.15f} >= {float(side):.15f})"
            meta_path.write_text(json.dumps(meta, indent=2, default=str)+"\n")
            continue
        certificate = certify(candidate, n, side)
        previous = json.loads(Path(f"{old}.certificate.json").read_text()) if Path(f"{old}.certificate.json").exists() else {}
        # Compare like with like: both rational witnesses carry the same ~1e-12 dilation.
        if previous.get("rational_side") and Fraction(certificate["rational_side"]) >= Fraction(previous["rational_side"]):
            meta["polish_skipped"] = "rational witness not below the installed packing's witness"
            meta_path.write_text(json.dumps(meta, indent=2, default=str)+"\n")
            continue
        new = ROOT/"found"/f"n{n}_s{float(new_side):.12f}"
        certificate.update({k: previous[k] for k in ("search_job", "seed_credit", "seed_certificate",
                                                     "seed_inherited_from", "orientation", "reference") if k in previous})
        certificate["exact_polish_of"] = {"file": f"{old.name}.txt", "exact_certificate": f"{old.name}.exact.cert",
                                          "side_before": str(side)}
        shutil.copy2(candidate, f"{new}.txt")
        Path(f"{new}.certificate.json").write_text(json.dumps(certificate, indent=2)+"\n")
        shutil.copy2(f"{old}.exact.cert", f"{new}.exact.cert")
        polished_meta = {**meta, "input": destination.name, "input_side": float(new_side),
                         "input_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
                         "polished_from": f"{old.name}.txt"}
        polished_meta.pop("polish_installed", None)
        polished_meta["polish_skipped"] = "this is the polished packing"
        Path(f"{new}.exact.json").write_text(json.dumps(polished_meta, indent=2, default=str)+"\n")
        for target in (destination, ROOT/"results"/destination.name):
            staged = target.with_suffix(".polish.tmp")
            shutil.copy2(candidate, staged)
            staged.replace(target)
        subprocess.run([str(BIN), "svg", str(destination)], check=True)
        shutil.copy2(destination.with_suffix(".svg"), ROOT/"results"/destination.with_suffix(".svg").name)
        meta["polish_installed"] = f"{new.name}.txt"
        meta_path.write_text(json.dumps(meta, indent=2, default=str)+"\n")
        changed.append({"n": n, "before": str(side), "after": str(new_side)})
        print(f"n={n}: exact polish installed, {float(side):.15f} -> {float(new_side):.15f}", flush=True)
        if len(changed) >= limit:
            break  # the coordinator dispatches nothing meanwhile; the rest waits for the next pass
    if changed:
        subprocess.run(["python3", str(ROOT/"regen_readme.py")], cwd=ROOT, check=True, capture_output=True)
        subprocess.run(["python3", str(ROOT/"check_readme.py")], cwd=ROOT, check=True, capture_output=True)
    return changed


def normalize_existing(records):
    """Called only by the coordinator, so record installation stays serialized."""
    summaries = []
    backup = ROOT/"found/orientation_originals"
    backup.mkdir(exist_ok=True)
    for destination in sorted(ROOT.glob("n[0-9]*.txt"), key=lambda p: int(p.stem[1:])):
        n = int(destination.stem[1:])
        before = measure(destination, n)
        with tempfile.TemporaryDirectory(prefix="orientation-", dir=ROOT/"experiments") as d:
            candidate = Path(d)/destination.name
            shutil.copy2(destination, candidate)
            report = orient(candidate, n)
            if not report["changed"]:
                summaries.append({"n": n, **report})
                continue
            side = measure(candidate, n)
            if abs(side-before) > Fraction(1, 10**9):
                raise ValueError(f"n={n}: orientation changed side beyond roundoff")
            certificate = certify(candidate, n, records[n])
            if Fraction(certificate["rational_side"]) >= records[n]:
                raise ValueError(f"n={n}: normalized witness no longer beats catalogue")
            old_archive = ROOT/"found"/f"n{n}_s{float(before):.12f}.certificate.json"
            previous = json.loads(old_archive.read_text()) if old_archive.exists() else {}
            certificate = {**previous, **certificate, "orientation": report}
            original = backup/f"n{n}_s{float(before):.12f}_{report['original_sha256'][:12]}.txt"
            shutil.copy2(destination, original)
            original.with_suffix(".certificate.json").write_text(json.dumps(previous, indent=2)+"\n")
            archive = ROOT/"found"/f"n{n}_s{float(side):.12f}.txt"
            shutil.copy2(candidate, archive)
            archive.with_suffix(".certificate.json").write_text(json.dumps(certificate, indent=2)+"\n")
            # Stage beside each official target so readers see whole files.
            for target in (destination, ROOT/"results"/destination.name):
                staged = target.with_suffix(".orientation.tmp")
                shutil.copy2(candidate, staged)
                staged.replace(target)
            subprocess.run([str(BIN), "svg", str(destination)], check=True)
            shutil.copy2(destination.with_suffix(".svg"), ROOT/"results"/destination.with_suffix(".svg").name)
            summaries.append({"n": n, "side": float(side), **report})
            print(f"n={n}: normalized via {report['symmetry']}; exact witness verified", flush=True)
    subprocess.run(["python3", str(ROOT/"regen_readme.py")], cwd=ROOT, check=True)
    subprocess.run(["python3", str(ROOT/"check_readme.py")], cwd=ROOT, check=True)
    return summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    records = {}
    for line in (ROOT/"records.txt").read_text().splitlines():
        if line.strip() and not line.startswith("#"):
            n, side = line.split()
            records[int(n)] = Fraction(side)
    installed = []
    files = sorted(args.directory.glob("n[0-9]*.txt"), key=lambda p: int(p.stem[1:]))
    for path in files:
        entry = accept(path.resolve(), records)
        if entry:
            installed.append(entry)
    manifest = args.directory/"accepted.json"
    previous = json.loads(manifest.read_text()) if manifest.exists() else []
    manifest.write_text(json.dumps(previous+installed, indent=2)+"\n")
    subprocess.run(["python3", "regen_readme.py"], cwd=ROOT, check=True)
    subprocess.run(["python3", "check_readme.py"], cwd=ROOT, check=True)
    print(f"Installed {len(installed)} improvements")


if __name__ == "__main__":
    main()
