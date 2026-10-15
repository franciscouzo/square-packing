#!/usr/bin/env python3
"""Build a complete upper-bound index through the requested count limit.

Frozen reference comparisons and reported register bounds remain separate
from exact certificates and the unconditional integer grid construction.
"""
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

from expanded_comparisons import rounded_up
from lower_bounds import approximation

ROOT = Path(__file__).resolve().parent


def certified_catalogue():
    """Read retained witnesses and their deletions, checking the byte bindings.

    A catalogue survives hourly comparison imports and root-packing refreshes.
    Its verification receipts apply to the immutable certificate bytes.
    """
    path = ROOT/'certified_bounds.json'
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    entries, checked = {}, {}
    for key, item in data['entries'].items():
        n = int(key)
        if item.get('kind') == 'grid':
            continue
        certificate = ROOT/item['certificate']
        if certificate not in checked:
            content = certificate.read_bytes()
            digest = hashlib.sha256(content).hexdigest()
            header = next(line.split() for line in content.decode().splitlines()
                          if line.strip() and not line.lstrip().startswith('#'))
            checked[certificate] = (digest, int(header[0]), Fraction(header[1]))
        digest, source_n, bound = checked[certificate]
        if (digest != item['certificate_sha256'] or not n <= source_n
                or source_n != item['source_n'] or bound != Fraction(item['bound'])
                or not item['verification']['valid']):
            raise ValueError(f'Certificate binding or verification is invalid at n={n}')
        entries[key] = {'bound': item['bound'], 'source': item['certificate'],
                        'source_n': source_n, 'deleted_squares': source_n-n,
                        'status': 'exact certificate verified' if source_n == n
                                  else 'verified by deletion from an exact certificate',
                        'credit': item['credit'], 'sha256': digest}
    return entries


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
    catalogue = certified_catalogue()
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
        if str(n) in catalogue:
            verified.append(catalogue[str(n)])
        best_verified = min(verified, key=lambda item: Fraction(item['bound']))
        best_reported = min([*reported, *verified], key=lambda item: scalar(item['bound']))
        entries[str(n)] = {'verified': dict(best_verified, rounded_up=rounded_up(best_verified['bound'])),
                          'reported': best_reported}
    # Removing squares from a witness preserves feasibility. Propagate a
    # stronger bound downwards even when a later root certificate improves.
    for n in range(max_n-1, 0, -1):
        current, larger = entries[str(n)], entries[str(n+1)]
        if Fraction(larger['verified']['bound']) < Fraction(current['verified']['bound']):
            inherited = dict(larger['verified'])
            source_n = inherited.get('source_n', n+1)
            inherited.update(source_n=source_n, deleted_squares=source_n-n,
                             status='verified by deletion from an exact certificate')
            current['verified'] = inherited
            if scalar(inherited['bound']) < scalar(current['reported']['bound']):
                current['reported'] = dict(inherited)
    return {'generated': datetime.now(timezone.utc).isoformat(), 'max_n': max_n,
            'note': 'Each count has an unconditional grid upper bound. Exact rational/algebraic certificate bounds are retained separately from frozen reference comparisons and reported register values. Source links and certificate hashes preserve attribution.',
            'entries': entries}


if __name__ == '__main__':
    (ROOT/'upper_bounds.json').write_text(json.dumps(render(), indent=2)+'\n')
