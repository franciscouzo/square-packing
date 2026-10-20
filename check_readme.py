#!/usr/bin/env python3
"""Check current record selection, certificate bindings and packing previews."""
from fractions import Fraction
import hashlib
from pathlib import Path
import re
import subprocess
import sys

from readme_records import END, START, catalogue, render


def main():
    records, omitted, context = catalogue()
    text = Path('README.md').read_text()
    problems = []
    if text.count(START) != 1 or text.count(END) != 1:
        problems.append('Expected one generated current-record section')
    elif text[text.index(START):text.index(END)+len(END)] != render(records, context):
        problems.append('Current record selection, bounds, credits or summary are stale')
    listed = [int(n) for n in re.findall(r'^\| \[(\d+)\]\(n\d+\.svg\)', text, re.M)]
    if len(listed) != len(set(listed)) or set(listed) != set(records):
        problems.append('README count list differs from the current credited records')
    if re.search(r'^\| \d+ \||!\[n = \d+\]|<!-- current-status -->|<!-- expanded-search-results -->', text, re.M):
        problems.append('An obsolete catalogue table or example image remains')
    for n, row in records.items():
        meta = row['metadata']
        for path_key, hash_key in [('packing', 'packing_sha256'), ('certificate', 'certificate_sha256')]:
            path = Path(meta[path_key])
            if hashlib.sha256(path.read_bytes()).hexdigest() != meta[hash_key]:
                problems.append(f'n={n}: {path_key} hash mismatch')
        certificate = Path(meta['certificate'])
        header = next(line.split() for line in certificate.read_text().splitlines()
                      if line.strip() and not line.lstrip().startswith('#'))
        if int(header[0]) != n or Fraction(header[1]) != Fraction(meta['rational_side']):
            problems.append(f'n={n}: certificate count or side mismatch')
        result = subprocess.run(['./target/release/sqpack', 'verify', f'n{n}.txt'],
                                capture_output=True, text=True, check=True).stdout
        if 'max_pair_overlap=0.000e0' not in result:
            problems.append(f'n={n}: packing overlaps')
        side = re.search(r'bbox_side=([0-9.]+)', result)
        if not side or float(side[1]) > float(Fraction(meta['rational_side']))+1e-9:
            problems.append(f'n={n}: preview exceeds its certificate beyond rounding tolerance')
        if not Path(f'n{n}.svg').exists():
            problems.append(f'n={n}: missing SVG preview')
    for problem in problems:
        print(problem)
    print(f'{len(records)} current records, {len(omitted)} retained packings excluded, {len(problems)} problems')
    return bool(problems)


if __name__ == '__main__':
    sys.exit(main())
