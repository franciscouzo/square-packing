#!/usr/bin/env python3
"""Fetch the fixed certificates and checkers in manifest.json; replay both routes."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen


def fetch(url, digest):
    with urlopen(url, timeout=60) as response:
        data = response.read()
    assert hashlib.sha256(data).hexdigest() == digest, (url, "SHA-256 mismatch")
    return data


def corners(x, y, t):
    denominator = 1 + t*t
    cosine, sine = (1-t*t)/denominator, 2*t/denominator
    half = Fraction(1, 2)
    return [(x+dx*cosine-dy*sine, y+dx*sine+dy*cosine)
            for dx, dy in ((-half, -half), (half, -half), (half, half), (-half, half))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="save the verification receipt")
    args = parser.parse_args()
    manifest_path = Path(__file__).with_name("manifest.json")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    receipt = {"certificate_commit": manifest["certificate_commit"],
               "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
               "checked_at": datetime.now(timezone.utc).isoformat(), "records": []}
    with tempfile.TemporaryDirectory(prefix="couzo-record-replay-") as directory:
        work = Path(directory)
        checkers = {}
        for checker in manifest["checkers"]:
            path = work / (checker["name"] + ".py")
            path.write_bytes(fetch(checker["url"], checker["sha256"]))
            checkers[checker["name"]] = path
        spec = importlib.util.spec_from_file_location("pinned_sqpack_verify", checkers["sqpack"])
        verifier = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = verifier
        spec.loader.exec_module(verifier)
        for record in manifest["records"]:
            n = record["n"]
            url = (f'https://raw.githubusercontent.com/{manifest["certificate_repository"]}/'
                   f'{manifest["certificate_commit"]}/{record["certificate_path"]}')
            data = fetch(url, record["certificate_sha256"])
            path = work / f"n{n}.cert"
            path.write_bytes(data)
            rows = [line.split() for line in data.decode().splitlines()
                    if line.strip() and not line.lstrip().startswith("#")]
            assert len(rows) == n+1 and len(rows[0]) == 2 and int(rows[0][0]) == n
            side = Fraction(rows[0][1])
            assert side == Fraction(record["rational_side"])
            assert side < Fraction(record["comparison"]["side"])
            assert all(len(row) == 3 for row in rows[1:])
            squares = [tuple(map(Fraction, row)) for row in rows[1:]]
            started = time.monotonic()
            report = verifier.verify_packing([corners(*square) for square in squares],
                                             side, lambda v: (v > 0)-(v < 0), bucket=True)
            sqpack_seconds = time.monotonic() - started
            assert report.valid and report.n == n, (n, report)
            started = time.monotonic()
            evand = subprocess.run([sys.executable, str(checkers["evand"]), str(path)],
                                   capture_output=True, text=True, timeout=120)
            evand_seconds = time.monotonic() - started
            assert evand.returncode == 0, (n, evand.stdout, evand.stderr)
            receipt["records"].append({"n": n, "certificate_sha256": record["certificate_sha256"],
                                       "sqpack_valid": report.valid, "sqpack_pairs_tested": report.pairs_tested,
                                       "sqpack_seconds": sqpack_seconds,
                                       "evand_exit_code": evand.returncode,
                                       "evand_seconds": evand_seconds,
                                       "evand_output": evand.stdout.strip()})
            print(f"n={n}: both exact rational checks passed", flush=True)
    if args.output:
        args.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f'Validated {len(receipt["records"])} fixed certificates and comparison bounds.')


if __name__ == "__main__":
    main()
