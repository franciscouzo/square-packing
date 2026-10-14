#!/usr/bin/env python3
"""Build a complete upper-bound index through the requested count limit.

Frozen reference comparisons and reported register bounds remain separate
from exact certificates and the unconditional integer grid construction.
"""
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
from pathlib import Path

from expanded_comparisons import rounded_up
from lower_bounds import approximation

ROOT = Path(__file__).resolve().parent


def scalar(bound):
    try:
        return float(Fraction(bound))
    except ValueError:
        return approximation(bound)


def render(max_n=1024):
    known = json.loads((ROOT/'known_best.json').read_text())
    references = {int(line.split()[0]): line.split()[1] for line in (ROOT/'records.txt').read_text().splitlines()
                  if line.strip() and not line.startswith('#')}
    certificates = {int(path.stem[1:]): json.loads(path.read_text())
                    for path in (ROOT/'certificates').glob('n[0-9]*.json')}
    entries = {}
    for n in range(1, max_n+1):
        grid = {'bound': str(math.isqrt(n-1)+1), 'source': 'integer square grid',
                'status': 'verified construction', 'credit': 'square grid'}
        verified = [grid]
        reported = [dict(grid)]
        if n in references:
            reported.append({'bound': references[n], 'source': 'records.txt',
                             'status': 'frozen catalogue/derived reference comparison'})
        entry = known['entries'].get(str(n), {})
        if entry:
            reported.append({'bound': entry.get('register_text') or str(entry['side']),
                             'source': 'https://github.com/jlevy/squares', 'status': 'reported upper bound'})
        external = entry.get('external')
        if external:
            verified.append({'bound': external['side'], 'source': external.get('certificate_url') or external['request'],
                'status': 'exact certificate verified; adoption pending' if external.get('pending') else 'exact certificate verified',
                'credit': external['credit'], 'sha256': external['sha256']})
        for external in known.get('reviewed_submissions', {}).get(str(n), []):
            verified.append({'bound': external['side'], 'source': external.get('certificate_url') or external['request'],
                'status': 'exact certificate replayed; upstream adoption pending',
                'credit': external['credit'], 'sha256': external['sha256']})
        if n in certificates:
            certificate = certificates[n]
            verified.append({'bound': certificate['rational_side'], 'source': certificate['certificate'],
                'status': 'exact certificate verified', 'credit': 'this repository; source credit in certificate metadata',
                'sha256': certificate['certificate_sha256']})
        best_verified = min(verified, key=lambda item: Fraction(item['bound']))
        best_reported = min([*reported, *verified], key=lambda item: scalar(item['bound']))
        entries[str(n)] = {'verified': dict(best_verified, rounded_up=rounded_up(best_verified['bound'])),
                          'reported': best_reported}
    return {'generated': datetime.now(timezone.utc).isoformat(), 'max_n': max_n,
            'note': 'Each count has an unconditional grid upper bound. Exact rational/algebraic certificate bounds are retained separately from frozen reference comparisons and reported register values. Source links and certificate hashes preserve attribution.',
            'entries': entries}


if __name__ == '__main__':
    (ROOT/'upper_bounds.json').write_text(json.dumps(render(), indent=2)+'\n')
