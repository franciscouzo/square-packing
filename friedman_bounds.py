#!/usr/bin/env python3
"""Friedman's off-centre extension of Göbel's square construction.

For a-1/2 < b/sqrt(2) < a+1/2, place a b by b rotated block
in an off-centre staircase frame and append a column of 2a+1 squares.
The count is 2a^2+4a+b^2+1, at side a+3/2+b*sqrt(2)/2.
Source: Friedman's survey, section 3; retained jlevy/squares builder below.
Only feasibility is established. All geometry uses exact Q(sqrt(2)).
"""
from datetime import datetime,timezone
from fractions import Fraction as F
import hashlib,json
from math import isqrt
from pathlib import Path

import gobel_bounds
from gobel_bounds import Q2,SQRT2,HALF,exact_value,verify

ROOT=Path(__file__).resolve().parent
SOURCE='https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py'
CREDIT='Erich Friedman (off-centre extension of Frits Göbel’s construction)'


def candidates(max_n=1024):
    for a in range(1,isqrt(max_n)+1):
        for b in range(1,isqrt(max_n)+1):
            n=2*a*a+4*a+b*b+1
            if n<=max_n and (2*a-1)**2<2*b*b<(2*a+1)**2:
                yield {'family':'offcentre','a':a,'b':b,'n':n,
                       'side':Q2(F(2*a+3,2),F(b,2))}


def build(candidate):
    a,b,side=candidate['a'],candidate['b'],candidate['side']
    if not (2*a-1)**2<2*b*b<(2*a+1)**2:
        raise ValueError('Invalid off-centre parameters')
    width=side-1;cx,cy=width/2,side/2
    tilted=[(cx+SQRT2*F(u+v-b+1,2),cy+SQRT2*F(v-u,2),1)
            for u in range(b) for v in range(b)]
    low=[Q2(F(2*k+1,2)) for k in range(a)]
    xs=low+[width-v for v in low];ys=low+[side-v for v in low]
    def intersects_block(x,y):
        dx,dy=x-cx,y-cy
        return (abs(dx)<HALF+SQRT2*F(b,2) and abs(dy)<HALF+SQRT2*F(b,2)
                and abs(dx+dy)<1+SQRT2*F(b,2) and abs(dx-dy)<1+SQRT2*F(b,2))
    axis=[(x,y,0) for x in xs for y in ys if not intersects_block(x,y)]
    column=[(width+HALF,Q2(F(2*k+1,2)),0) for k in range(2*a+1)]
    if len(axis)!=2*a*(a+1):raise ValueError('Wrong staircase count')
    squares=axis+tilted+column
    if len(squares)!=candidate['n']:raise ValueError('Wrong construction count')
    return squares


def hashes():
    return {'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'arithmetic_geometry_sha256':hashlib.sha256(Path(gobel_bounds.__file__).read_bytes()).hexdigest()}


def generate(max_n=1024):
    rows=[]
    for candidate in candidates(max_n):
        receipt=verify(build(candidate),candidate['side'])
        if not receipt['valid']:raise ValueError((candidate,receipt))
        side=candidate['side'];lo,hi=side.enclosure()
        rows.append({k:v for k,v in candidate.items() if k!='side'} | {
            'bound':str(hi),'exact_bound':side.record(),'enclosure_lower':str(lo),
            'rounded_up':side.rounded_up(),'source':SOURCE,'credit':CREDIT,'verification':receipt})
    return {'generated':datetime.now(timezone.utc).isoformat(),'max_n':max_n,
            'checker':'friedman_bounds.py',**hashes(),'witnesses':rows}


def catalogue(max_n=1024,root=ROOT):
    path=root/'friedman_bounds.json'
    if not path.exists():return {}
    data=json.loads(path.read_text())
    if any(data.get(k)!=v for k,v in hashes().items()):
        raise ValueError('Off-centre checker changed; regenerate its exact receipts')
    formulas={(r['a'],r['b']):r for r in candidates(data['max_n'])};selected={}
    for row in data['witnesses']:
        formula=formulas[(row['a'],row['b'])]
        if (row['n']!=formula['n'] or exact_value(row)!=formula['side']
                or Q2(row['bound'])<formula['side'] or not row['verification']['valid']
                or row['verification']['n']!=row['n']):
            raise ValueError('Invalid off-centre construction receipt')
        if row['n']>max_n:continue
        entry={k:row[k] for k in ['bound','exact_bound','source','credit','family','a','b']}
        entry.update(source_n=row['n'],deleted_squares=0,proof='friedman_bounds.json',
                     status='exact algebraic construction verified',**hashes())
        old=selected.get(str(row['n']))
        if old is None or exact_value(entry)<exact_value(old):selected[str(row['n'])]=entry
    return selected


if __name__=='__main__':
    data=generate();(ROOT/'friedman_bounds.json').write_text(json.dumps(data,indent=2)+'\n')
    print('Exactly verified',len(data['witnesses']),'off-centre constructions through n=1024.')
