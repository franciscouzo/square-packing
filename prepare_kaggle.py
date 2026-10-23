#!/usr/bin/env python3
"""Export certified packings to Kaggle Squares in Squares decimal coordinates.

The competition measures angles, rather than rational half-angle tangents.
Render at high precision and separate centres by 1+1e-40 so conversion of
touching exact squares cannot introduce microscopic overlaps. Grid packings
retain their exact half-integer coordinates and zero angles.
"""
import argparse
import csv
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import re

import mpmath as mp

from certificate_constructions import derive, expand
import friedman_bounds
import gobel_bounds
from gobel_bounds import Q2, exact_value
from import_external import read_cert_text

ROOT = Path(__file__).resolve().parent
DPS = 100
DIGITS = 75
CENTRE_DILATION = '1e-40'
COLUMNS = ['id', 'n', 'square_id', 'x', 'y', 'angle']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def number(value):
    if not value:
        return '0'
    return mp.nstr(value, DIGITS, strip_zeros=False)


def rational(value):
    value = F(value)
    return mp.mpf(value.numerator)/value.denominator


def algebraic(value):
    return rational(value.p)+rational(value.q)*mp.sqrt(2)


def field_polynomial(field):
    if field.get('polynomial_coefficients_descending'):
        return list(map(F, field['polynomial_coefficients_descending']))
    expression = field['polynomial'].replace(' ', '')
    terms = re.findall(r'[+-]?[^+-]+', expression)
    if ''.join(terms) != expression:
        raise ValueError('Unsupported polynomial')
    coefficients = {}
    for term in terms:
        match = re.fullmatch(r'([+-]?)(?:(\d+(?:/\d+)?)\*?)?(t)?(?:\^(\d+))?', term)
        if not match or not (match[2] or match[3]):
            raise ValueError('Unsupported polynomial term')
        exponent = int(match[4] or 1) if match[3] else 0
        value = F(match[2] or 1)*(-1 if match[1] == '-' else 1)
        coefficients[exponent] = coefficients.get(exponent, F(0))+value
    return [coefficients.get(i, F(0)) for i in range(max(coefficients), -1, -1)]


class Packings:
    def __init__(self, root=ROOT, overrides=()):
        self.root = Path(root)
        self.upper = json.loads((self.root/'upper_bounds.json').read_text())['entries']
        self.finite = json.loads((self.root/'certified_bounds.json').read_text())['entries']
        self.sources = json.loads((self.root/'certificates/best/manifest.json').read_text())['witnesses']
        self.classical = {(r['family'], r['a'], r['b']): r
                          for r in [*gobel_bounds.candidates(1000), *friedman_bounds.candidates(1000)]}
        self.additional_sources = {}
        for row in overrides:
            if not row['corner_check']['valid'] or not row['projection_check']['valid']:
                raise ValueError('An additional source has no passing exact checks')
            parent = int(row['n'])
            if parent > 1000:
                continue
            digest = row['certificate_sha256']
            source = dict(credit=row['credit'], provenance=row['origin'])
            self.additional_sources[digest] = source
            for tiles in range(1, math.isqrt(1000//parent)+1):
                capacity, side, layers = parent*tiles*tiles, F(row['bound'])*tiles, 0
                while side <= 32:
                    first = (side.numerator//side.denominator)**2+1
                    for target in range(first, min(capacity, 1000)+1):
                        key = str(target)
                        if Q2(side) < exact_value(self.upper[key]['verified']):
                            self.upper[key]['verified'] = dict(bound=str(side), source=row['certificate'], credit=row['credit'])
                            finite = dict(bound=str(side), certificate=row['certificate'], certificate_sha256=digest)
                            if tiles != 1 or layers:
                                finite['construction'] = dict(source_n=parent, tiles_per_side=tiles, layers=layers)
                            self.finite[key] = finite
                    capacity += 2*(side.numerator//side.denominator)+1
                    side += 1
                    layers += 1

    @lru_cache(maxsize=1024)
    def certificate(self, relative, expected_hash):
        path = self.root/relative
        if digest(path) != expected_hash:
            raise ValueError(f'Certificate hash mismatch: {relative}')
        return read_cert_text(path)

    @lru_cache(maxsize=1024)
    def classical_rows(self, family, a, b):
        candidate = self.classical[family, a, b]
        rows = (friedman_bounds.build if family == 'offcentre' else gobel_bounds.build)(candidate)
        return rows, candidate['side']

    def algebraic_rows(self, n, record):
        """Render retained, already replayed polynomial-field certificates."""
        parent_n = record.get('source_n', n)
        candidates = [self.root/'experiments/land-bounds-20261014'/relative/f'n{parent_n:03d}/geometry.json'
                      for relative in ['algebraic/pingyou-algebraic-refinements-2026-10-13',
                                       'exact-endpoints/pingyou-exact-153-302']]
        path = next((p for p in candidates if p.is_file() and digest(p) == record.get('sha256')), None)
        if path is None:
            raise ValueError(f'n={n}: canonical algebraic certificate is unavailable')
        data = json.loads(path.read_text())
        field = data['field']
        coefficients = field_polynomial(field)
        lo, hi = map(F, field['isolating_interval'])

        def polynomial(value):
            result = F(0)
            for coefficient in coefficients:
                result = result*value+coefficient
            return result

        f_lo, f_hi = polynomial(lo), polynomial(hi)
        if not f_lo*f_hi < 0:
            raise ValueError('Field root is not bracketed by its isolating interval')
        while hi-lo > F(1, 10**120):
            mid = (lo+hi)/2
            f_mid = polynomial(mid)
            if not f_mid:
                lo = hi = mid
                break
            if (f_mid > 0) == (f_lo > 0):
                lo, f_lo = mid, f_mid
            else:
                hi, f_hi = mid, f_mid
        root = rational((lo+hi)/2)

        def evaluate(poly):
            result = mp.mpf(0)
            for coefficient in poly:
                result = result*root+rational(coefficient)
            return result

        assert data['n'] >= n and len(data['centers']) == len(data['frames']) == data['n']
        rows = []
        for (x, y), frame in zip(data['centers'][:n], data['frames'][:n]):
            ux, uy = map(evaluate, frame[0])
            rows.append((evaluate(x), evaluate(y), mp.atan2(uy, ux)))
        return rows, dict(kind='algebraic certificate', certificate=str(path.relative_to(self.root)),
                          certificate_sha256=record['sha256'], source_n=data['n'], deleted_squares=data['n']-n,
                          provenance_file='known_best.json')

    def rows(self, n):
        """Return (x,y,angle) in high precision plus immutable source credit."""
        v = self.upper[str(n)]['verified']
        info = dict(n=n, credit=v.get('credit'), exact_bound=exact_value(v).record())
        if v['source'] == 'integer square grid':
            width = math.isqrt(n-1)+1
            info.update(kind='grid', source='integer square grid')
            return [(mp.mpf(2*(i % width)+1)/2, mp.mpf(2*(i//width)+1)/2, mp.mpf(0))
                    for i in range(n)], info
        if v.get('exact_bound'):
            base, side = self.classical_rows(v['family'], v['a'], v['b'])
            rows = list(base)
            recipe = v.get('construction') or {}
            for _ in range(recipe.get('layers', 0)):
                k = side.floor()
                rows.extend((side+Q2(F(1, 2)), Q2(F(2*i+1, 2)), 0) for i in range(k+1))
                rows.extend((Q2(F(2*i+1, 2)), side+Q2(F(1, 2)), 0) for i in range(k))
                side += 1
            assert side == exact_value(v) and len(rows) >= n
            info.update(kind='classical', source=v['source'], family=v['family'], a=v['a'], b=v['b'],
                        construction=recipe, capacity=len(rows))
            return [(algebraic(x), algebraic(y), mp.pi/4 if tilted else mp.mpf(0))
                    for x, y, tilted in rows[:n]], info
        finite = self.finite[str(n)]
        if exact_value(finite) != exact_value(v):
            rows, algebraic_source = self.algebraic_rows(n, v)
            info.update(algebraic_source)
            return rows, info
        parent_n, side, source_rows = self.certificate(finite['certificate'], finite['certificate_sha256'])
        recipe = finite.get('construction') or {}
        capacity, bound = derive(parent_n, side, recipe.get('tiles_per_side', 1), recipe.get('layers', 0))
        rows, expanded = expand(source_rows, side, recipe.get('tiles_per_side', 1), recipe.get('layers', 0))
        assert expanded == bound == F(finite['bound']) and len(rows) == capacity and capacity >= n
        source = self.additional_sources.get(finite['certificate_sha256']) or self.sources[str(parent_n)]
        info.update(kind='certificate', certificate=finite['certificate'], certificate_sha256=finite['certificate_sha256'],
                    source_n=parent_n, construction=recipe, deleted_squares=capacity-n,
                    credit=source['credit'], provenance_file='certificates/best/manifest.json')
        return [(rational(x), rational(y), angle(t, mp.mp.dps)) for x, y, t in rows[:n]], info


@lru_cache(maxsize=16384)
def angle(t, dps):
    with mp.workdps(dps):
        return 2*mp.atan(rational(t)) if t else mp.mpf(0)


def export(root, destination, limit=1000, overrides=()):
    if not 1 <= limit <= 1000:
        raise ValueError('Kaggle scores n=1..1000')
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    with mp.workdps(DPS):
        packings = Packings(root, overrides)
        manifest = []
        target = destination/'submission.csv'
        temporary = target.with_suffix('.csv.incoming')
        index = 0
        with temporary.open('w', newline='') as handle:
            writer = csv.writer(handle, lineterminator='\n')
            writer.writerow(COLUMNS)
            for n in range(1, limit+1):
                rows, source = packings.rows(n)
                assert len(rows) == n
                factor = 1 if source['kind'] == 'grid' else 1+mp.mpf(CENTRE_DILATION)
                for sid, (x, y, theta) in enumerate(rows):
                    if source['kind'] == 'grid':
                        values = [str(float(x)), str(float(y)), '0']
                    else:
                        values = [number(x*factor), number(y*factor), number(theta)]
                    writer.writerow([index, n, sid, *values])
                    index += 1
                manifest.append(source)
                if n % 100 == 0:
                    print(f'Exported n=1..{n}; {index} rows', flush=True)
        assert index == limit*(limit+1)//2
        temporary.replace(target)
        metadata = dict(competition='https://www.kaggle.com/competitions/squares-in-squares',
                        format=COLUMNS, puzzles=limit, rows=index, decimal_digits=DIGITS,
                        working_precision=DPS, non_grid_centre_dilation='1+'+CENTRE_DILATION,
                        snapshot_sha256=digest(Path(root)/'upper_bounds.json'),
                        source_manifest_sha256=digest(Path(root)/'certificates/best/manifest.json'),
                        submission_sha256=digest(target), sources=manifest)
        if overrides:
            metadata['additional_certificates'] = [{k:r[k] for k in ['n','certificate','certificate_sha256','credit']}
                                                   for r in overrides if r['n'] <= 1000]
        (destination/'sources.json').write_text(json.dumps(metadata, indent=2)+'\n')
        return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT/'submissions/kaggle-squares-20261022')
    parser.add_argument('--overrides', type=Path, help='Additional public certificates with both exact replay receipts')
    args = parser.parse_args()
    overrides = json.loads(args.overrides.read_text()) if args.overrides else []
    result = export(args.root, args.output, overrides=overrides)
    print(json.dumps({k:result[k] for k in ['puzzles','rows','submission_sha256']}))


if __name__ == '__main__':
    main()
