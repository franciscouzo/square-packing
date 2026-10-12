#!/usr/bin/env python3
"""Check the README table against the packings on disk. Reports, never rewrites."""
import glob, json, re, subprocess, sys
from pathlib import Path
from expanded_comparisons import END_MARKER, MARKER, PUBLISHED_MAX, render

rec = {}
for line in open('records.txt'):
    if not line.startswith('#'):
        n, s = line.split()
        rec[int(n)] = s

table = {}
readme = Path('README.md').read_text()
for m in re.finditer(r'^\| (\d+) \| ([0-9.]+) \| \*\*([0-9.]+)\*\* \| ([0-9.e+-]+) \|(?: [^\n]+)?$',
                     readme, re.M):
    table[int(m.group(1))] = (m.group(2), m.group(3), m.group(4))

files = {int(re.findall(r'\d+', f)[0]) for f in glob.glob('n[0-9]*.txt')}
bad = 0
for n in sorted(files | set(table)):
    if n not in table:
        print(f"n={n}: packing on disk but missing from the table"); bad += 1; continue
    if n not in files:
        print(f"n={n}: in the table but no n{n}.txt"); bad += 1; continue
    out = subprocess.run(['./target/release/sqpack', 'verify', f'n{n}.txt'],
                         capture_output=True, text=True).stdout
    side = re.search(r'bbox_side=([0-9.]+)', out).group(1)
    ov = re.search(r'max_pair_overlap=([0-9.e-]+)', out).group(1)
    t_rec, t_side, t_gain = table[n]
    if ov != '0.000e0':
        print(f"n={n}: OVERLAP {ov}"); bad += 1
    if t_side != side:
        print(f"n={n}: table says {t_side}, file measures {side}"); bad += 1
    if t_rec != rec[n]:
        print(f"n={n}: table record {t_rec} != records.txt {rec[n]}"); bad += 1
    gain = float(rec[n]) - float(side)
    if gain <= 0:
        print(f"n={n}: no improvement over the reference ({side} vs {rec[n]})"); bad += 1
    elif abs(gain - float(t_gain)) > 5e-4 * abs(gain):   # table is rounded to 4 digits
        print(f"n={n}: table gain {t_gain}, computed {gain:.3e}"); bad += 1
expanded = [f'| {n} | {record} | **{side}** | {gain} |'
            for n, (record, side, gain) in sorted(table.items()) if n > PUBLISHED_MAX]
if expanded:
    known_path = Path('known_best.json')
    known = json.loads(known_path.read_text()) if known_path.exists() else {}
    if MARKER not in readme or END_MARKER not in readme:
        print('Missing published comparison section above n=324'); bad += 1
    elif readme[readme.index(MARKER):readme.index(END_MARKER)+len(END_MARKER)] != render(expanded, known):
        print('Published comparison bounds, sources, standings or coverage are stale'); bad += 1
print(f"{len(files)} packings, {len(table)} table rows, {bad} problems")
sys.exit(1 if bad else 0)
