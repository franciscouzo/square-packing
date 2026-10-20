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

from gobel_bounds import catalogue as gobel_catalogue, exact_value
from friedman_bounds import catalogue as friedman_catalogue
from construction_bounds import l_border_catalogue
from lower_bounds import approximation
from certificate_constructions import derive

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
        construction = item.get('construction')
        if construction:
            if construction.get('checker_sha256') != hashlib.sha256((ROOT/'certificate_constructions.py').read_bytes()).hexdigest():
                raise ValueError(f'Construction checker binding is invalid at n={n}')
            capacity, derived = derive(source_n, bound, construction['tiles_per_side'], construction['layers'])
            valid = (capacity == item['source_n'] and n <= capacity
                     and derived == Fraction(item['bound'])
                     and source_n == construction['source_n']
                     and bound == Fraction(construction['source_bound']))
        else:
            valid = n <= source_n and source_n == item['source_n'] and bound == Fraction(item['bound'])
        if (digest != item['certificate_sha256'] or not valid or not item['verification']['valid']):
            raise ValueError(f'Certificate binding or verification is invalid at n={n}')
        entries[key] = {'bound': item['bound'], 'source': item['certificate'],
                        'source_n': item['source_n'], 'deleted_squares': item['source_n']-n,
                        'status': 'exact certificate verified' if source_n == n
                                  else 'verified by deletion from an exact certificate',
                        'credit': item['credit'], 'sha256': digest}
        if construction:
            entries[key].update(construction=construction,
                status='exact tiling/L-border construction from a verified certificate')
    return entries


def scalar(bound):
    try:
        return float(Fraction(bound))
    except ValueError:
        return approximation(bound)


def render(max_n=None):
    known = json.loads((ROOT/'known_best.json').read_text())
    if max_n is None:
        max_n = known.get('bounds_max_n', 1024)
    references = {int(line.split()[0]): line.split()[1] for line in (ROOT/'records.txt').read_text().splitlines()
                  if line.strip() and not line.startswith('#')}
    certificates = {int(path.stem[1:]): json.loads(path.read_text())
                    for path in (ROOT/'certificates').glob('n[0-9]*.json')}
    catalogue = certified_catalogue()
    gobel = gobel_catalogue(max_n, root=ROOT)
    friedman = friedman_catalogue(max_n, root=ROOT)
    classical = l_border_catalogue([gobel, friedman], max_n)
    if max_n > 1024:
        # Universal published constructions apply beyond the individually
        # replayed catalogue. Keep their verification origin explicit.
        from gobel_bounds import candidates as gobel_candidates, SOURCES
        from friedman_bounds import candidates as friedman_candidates
        general = {}
        for row in [*gobel_candidates(max_n), *friedman_candidates(max_n)]:
            if row['n'] <= 1024:
                continue
            side = row['side']
            source = SOURCES.get(row['family'], 'https://kingbird.myphotos.cc/packing/squares_in_squares.html')
            value = {'bound':str(side.enclosure()[1]), 'exact_bound':side.record(),
                'source':source, 'source_n':row['n'], 'deleted_squares':0,
                'credit':'Frits Göbel / Erich Friedman; generalized catalogue by David Ellsworth',
                'status':'published exact construction formula',
                'verification_origin':'Universal published construction; this instance was not geometrically replayed here',
                'family':row['family'], 'a':row['a'], 'b':row['b']}
            old = general.get(str(row['n']))
            if old is None or side < exact_value(old):
                general[str(row['n'])] = value
        for key, value in l_border_catalogue([general], max_n).items():
            if key not in classical or exact_value(value) < exact_value(classical[key]):
                classical[key] = value
    reference_path = ROOT/'record_reference_bounds.json'
    reviewed = json.loads(reference_path.read_text()).get('entries', {}) if reference_path.exists() else {}
    public_path = ROOT/'public_bounds.json'
    public = json.loads(public_path.read_text()).get('entries', {}) if public_path.exists() else {}
    entries = {}
    for n in range(1, max_n+1):
        grid = {'bound': str(math.isqrt(n-1)+1), 'source': 'integer square grid',
                'status': 'verified construction', 'credit': 'square grid'}
        verified = [grid]
        reported = [dict(grid)]
        if str(n) in public:
            reported.append(dict(public[str(n)], status='reviewed public upper bound'))
        if str(n) in reviewed:
            reference = reviewed[str(n)]
            reported.append({'bound':reference['bound'], 'source':'record_reference_bounds.json',
                'status':'reviewed reference upper bound', 'origin':reference.get('origin')})
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
        if str(n) in classical:
            verified.append(classical[str(n)])
        best_verified = min(verified, key=exact_value)
        best_reported = min([*reported, *verified], key=lambda item: scalar(item['bound']))
        entries[str(n)] = {'verified': dict(best_verified, rounded_up=exact_value(best_verified).rounded_up()),
                          'reported': best_reported}
    # Removing squares from a witness preserves feasibility. Propagate a
    # stronger bound downwards even when a later root certificate improves.
    for n in range(max_n-1, 0, -1):
        current, larger = entries[str(n)], entries[str(n+1)]
        current_value = exact_value(current['verified'])
        larger_value = exact_value(larger['verified'])
        simpler_equal_proof = ((larger_value-current_value).sign() == 0
                               and current['verified'].get('construction')
                               and not larger['verified'].get('construction'))
        if larger_value < current_value or simpler_equal_proof:
            inherited = dict(larger['verified'])
            source_n = inherited.get('source_n', n+1)
            status = ('verified by deletion from an exact algebraic construction'
                      if inherited.get('exact_bound') else 'verified by deletion from an exact certificate')
            inherited.update(source_n=source_n, deleted_squares=source_n-n, status=status)
            current['verified'] = inherited
            if scalar(inherited['bound']) < scalar(current['reported']['bound']):
                current['reported'] = dict(inherited)
    return {'generated': datetime.now(timezone.utc).isoformat(), 'max_n': max_n,
            'note': 'Each count has an unconditional grid upper bound. Exact rational certificates and algebraic Göbel/Friedman constructions are retained separately from frozen reference comparisons and reported register values. Algebraic exact_bound values select verified bounds; bound is an outward rational enclosure for existing consumers. Source links, checker receipts and certificate hashes preserve attribution.',
            'entries': entries}


if __name__ == '__main__':
    (ROOT/'upper_bounds.json').write_text(json.dumps(render(), indent=2)+'\n')
