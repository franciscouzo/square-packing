#!/usr/bin/env python3
"""Exact Göbel square/strip constructions and comparisons over Q(sqrt(2)).

Construction formulas: Frits Göbel, as generalized in David Ellsworth's
square and strip catalogues. Layouts follow their staircase descriptions;
the centred block and ordinary strip agree with jlevy/squares' builders.
All arithmetic, admissibility, containment and pair tests are exact.
The rational `bound` is an outward enclosure for existing index consumers;
`exact_bound` retains the algebraic value used when choosing bounds.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES = {
    'square': 'https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html',
    'strip': 'https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html',
    'corner_strip': 'https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html',
}


@dataclass(frozen=True)
class Q2:
    """p + q sqrt(2), with its positive square root and exact ordering."""
    p: Fraction = Fraction(0)
    q: Fraction = Fraction(0)

    def __post_init__(self):
        object.__setattr__(self, 'p', Fraction(self.p))
        object.__setattr__(self, 'q', Fraction(self.q))

    def __add__(self, other):
        other = other if isinstance(other, Q2) else Q2(other)
        return Q2(self.p+other.p, self.q+other.q)

    __radd__ = __add__

    def __neg__(self):
        return Q2(-self.p, -self.q)

    def __sub__(self, other):
        return self + (-other if isinstance(other, Q2) else -Q2(other))

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        other = other if isinstance(other, Q2) else Q2(other)
        return Q2(self.p*other.p+2*self.q*other.q,
                  self.p*other.q+self.q*other.p)

    __rmul__ = __mul__

    def __truediv__(self, rational):
        return Q2(self.p/Fraction(rational), self.q/Fraction(rational))

    def sign(self):
        p, q = self.p, self.q
        if not p:
            return (q > 0)-(q < 0)
        if not q or (p > 0) == (q > 0):
            return (p > 0)-(p < 0)
        delta = p*p-2*q*q
        return ((delta > 0)-(delta < 0))*((p > 0)-(p < 0))

    def __lt__(self, other):
        return (self-other).sign() < 0

    def __abs__(self):
        return -self if self.sign() < 0 else self

    def enclosure(self, places=80):
        scale = 10**places
        lo = Fraction(isqrt(2*scale*scale), scale)
        hi = lo+Fraction(1, scale)
        values = self.p+self.q*lo, self.p+self.q*hi
        return min(values), max(values)

    def floor(self):
        lo, hi = self.enclosure()
        result = lo.numerator//lo.denominator
        # Exact signs handle the rare case of an enclosure crossing an integer.
        while (self-(result+1)).sign() >= 0:
            result += 1
        while (self-result).sign() < 0:
            result -= 1
        return result

    def rounded_up(self, places=12):
        value = self*10**places
        ceiling = value.floor()+(value.q != 0 or value.p.denominator != 1)
        magnitude = abs(ceiling)
        return f'{"-" if ceiling < 0 else ""}{magnitude//10**places}.{magnitude%10**places:0{places}d}'

    def record(self):
        return {'rational': str(self.p), 'sqrt2': str(self.q),
                'expression': f'{self.p} + {self.q}*sqrt(2)'}


SQRT2 = Q2(0, 1)
HALF = Q2(Fraction(1, 2))


def exact_value(record):
    item = record.get('exact_bound')
    return Q2(item['rational'], item['sqrt2']) if item else Q2(record['bound'])


def candidates(max_n=1024):
    """Enumerate both complete families and the corner-constrained strip."""
    for a in range(1, isqrt(max_n)+1):
        for b in range(1, isqrt(max_n)+1):
            n = 2*a*(a+1)+b*b
            if n <= max_n and 2*(a-1)**2 < b*b < 2*(a+1)**2:
                yield {'family': 'square', 'a': a, 'b': b, 'n': n,
                       'side': Q2(a+1, Fraction(b, 2))}
        b = 1+isqrt(2*(a-1)**2)
        for family, n, side in (
            ('strip', a*(a+1)+2+b, Q2(a+1, Fraction(1, 2))),
            ('corner_strip', a*(a+1)+3+b, Q2(2, Fraction(b+1, 2))),
        ):
            if n <= max_n:
                yield {'family': family, 'a': a, 'b': b, 'n': n, 'side': side}


def overlaps(left, right):
    """Closed unit squares at angle 0 or pi/4: disjoint interiors via SAT."""
    x, y = left[0]-right[0], left[1]-right[1]
    if left[2] == right[2] == 0:
        return abs(x) < 1 and abs(y) < 1
    if left[2] == right[2] == 1:
        return abs(x+y) < SQRT2 and abs(x-y) < SQRT2
    axis_radius = (1+SQRT2)/2
    diagonal_radius = 1+SQRT2/2
    return (abs(x) < axis_radius and abs(y) < axis_radius
            and abs(x+y) < diagonal_radius and abs(x-y) < diagonal_radius)


def build(candidate):
    a, b, side = candidate['a'], candidate['b'], candidate['side']
    family = candidate['family']
    if family == 'square':
        if not 2*(a-1)**2 < b*b < 2*(a+1)**2:
            raise ValueError('Invalid Göbel square parameters')
        c = side/2
        tilted = [(c+SQRT2*Fraction(u+v-b+1, 2),
                   c+SQRT2*Fraction(v-u, 2), 1)
                  for u in range(b) for v in range(b)]
        offsets = [Q2(Fraction(2*k+1, 2)) for k in range(a)]
        offsets += [side-v for v in offsets]
        # The b by b rotated unit squares fill a solid rotated block. Testing
        # each frame square against that block uses its four separating axes.
        def intersects_block(x, y):
            dx, dy = x-c, y-c
            return (abs(dx) < HALF+SQRT2*Fraction(b, 2)
                    and abs(dy) < HALF+SQRT2*Fraction(b, 2)
                    and abs(dx+dy) < 1+SQRT2*Fraction(b, 2)
                    and abs(dx-dy) < 1+SQRT2*Fraction(b, 2))
        axis = [(x, y, 0) for x in offsets for y in offsets
                if not intersects_block(x, y)]
        if len(axis) != 2*a*(a+1):
            raise ValueError('Wrong staircase count')
        return axis+tilted
    low = [(Q2(Fraction(2*i+1, 2)), Q2(Fraction(2*j+1, 2)), 0)
           for i in range(a) for j in range(a-i)]
    high = [(side-x, side-y, angle) for x, y, angle in low]
    corner = [(side-HALF, HALF, 0), (HALF, side-HALF, 0)]
    m = b if family == 'strip' else b+1
    tilted = []
    for k in range(m):
        d = SQRT2*Fraction(2*k-m+1, 2)
        tilted.append(((side+d)/2, (side-d)/2, 1))
    return low+high+corner+tilted


def verify(squares, side):
    """Exact wall tests and every potentially intersecting pair.

    Cells of side 2 are indexed by exact floors. Non-neighbour cells imply
    centre distance > 2 along one axis; unit-square radii are sqrt(2)/2.
    """
    buckets = {}
    tested = 0
    for i, (x, y, angle) in enumerate(squares):
        if angle not in (0, 1):
            return {'valid': False, 'reason': 'invalid orientation'}
        radius = HALF if angle == 0 else SQRT2/2
        if any(v.sign() < 0 for v in (x-radius, y-radius, side-x-radius, side-y-radius)):
            return {'valid': False, 'reason': 'outside container', 'square': i}
        cell = (x/2).floor(), (y/2).floor()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in buckets.get((cell[0]+dx, cell[1]+dy), ()):
                    tested += 1
                    if overlaps(squares[i], squares[j]):
                        return {'valid': False, 'reason': 'overlap', 'pair': [j, i]}
        buckets.setdefault(cell, []).append(i)
    return {'valid': True, 'n': len(squares), 'pairs_tested': tested,
            'arithmetic': 'exact Q(sqrt(2)); closed box, disjoint interiors'}


def generate(max_n=1024):
    witnesses = []
    for candidate in candidates(max_n):
        squares = build(candidate)
        receipt = verify(squares, candidate['side'])
        if not receipt['valid'] or len(squares) != candidate['n']:
            raise ValueError((candidate, receipt))
        side = candidate['side']
        lo, hi = side.enclosure()
        witnesses.append({k: v for k, v in candidate.items() if k != 'side'} | {
            'bound': str(hi), 'exact_bound': side.record(), 'enclosure_lower': str(lo),
            'rounded_up': side.rounded_up(), 'source': SOURCES[candidate['family']],
            'credit': 'Frits Göbel; family formulas generalized by David Ellsworth',
            'verification': receipt,
        })
    return {'generated': datetime.now(timezone.utc).isoformat(), 'max_n': max_n,
            'checker': 'gobel_bounds.py',
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'witnesses': witnesses}


def catalogue(max_n=1024, root=ROOT):
    path = root/'gobel_bounds.json'
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    if data['checker_sha256'] != hashlib.sha256(Path(__file__).read_bytes()).hexdigest():
        raise ValueError('Göbel checker changed; regenerate its exact receipts')
    formulas = {(r['family'], r['a'], r['b']): r for r in candidates(data['max_n'])}
    selected = {}
    for row in data['witnesses']:
        key = row['family'], row['a'], row['b']
        formula = formulas[key]
        if (row['n'] != formula['n'] or not row['verification']['valid']
                or row['verification']['n'] != row['n']
                or exact_value(row) != formula['side']
                or Q2(row['bound']) < formula['side']):
            raise ValueError(f'Invalid Göbel construction receipt: {key}')
        if row['n'] > max_n:
            continue
        item = {k: row[k] for k in ('bound', 'exact_bound', 'source', 'credit', 'family', 'a', 'b')}
        item.update(source_n=row['n'], deleted_squares=0,
                    status='exact algebraic construction verified',
                    proof='gobel_bounds.json', checker_sha256=data['checker_sha256'])
        current = selected.get(str(row['n']))
        if current is None or exact_value(item) < exact_value(current):
            selected[str(row['n'])] = item
    return selected


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=1024)
    parser.add_argument('--output', type=Path, default=ROOT/'gobel_bounds.json')
    args = parser.parse_args()
    data = generate(args.max_n)
    args.output.write_text(json.dumps(data, indent=2)+'\n')
    print(f'Verified {len(data["witnesses"])} Göbel constructions through n={args.max_n}.')
