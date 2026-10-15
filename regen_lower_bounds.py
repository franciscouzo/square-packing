"""Refresh upstream lower-bound statements without promoting unverified claims."""
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
from pathlib import Path
import re

from lower_bounds import approximation, closed_form, rational_floor

ROOT=Path(__file__).resolve().parent


def render(max_n=1024):
    old=json.loads((ROOT/'lower_bounds.json').read_text())
    known=json.loads((ROOT/'known_best.json').read_text())
    revision=known['sources']['register']['commit']
    status=(ROOT/'external/sources/register-STATUS.md').read_text()
    rows={}
    for line in status.splitlines():
        match=re.match(r'\| \[`(\d+)`\]',line)
        if match:rows[int(match[1])]=[s.strip().strip('`') for s in line.strip().strip('|').split('|')]
    family=json.loads((ROOT/'lower_bound_families.json').read_text())
    entries={}
    for n in range(1,max_n+1):
        previous=old['entries'].get(str(n),{})
        area={'bound':f'sqrt({n})','approximation':math.sqrt(n),'source':'area: n unit squares occupy area n','status':'verified mathematical bound'}
        verified=dict(previous.get('verified',area))
        reports=[dict(area),*previous.get('reports',[])]
        if n in rows:
            row=rows[n]
            source=f'https://github.com/jlevy/squares/blob/{revision}/packing/frontier/n-{n:03d}.md'
            upstream={'bound':row[4],'approximation':approximation(row[4]),'source':source,
                      'status':'verified by upstream register; verification tier retained from source'}
            if upstream['approximation']>=verified['approximation']-1e-12:verified=upstream
            reports.append({'bound':row[3],'approximation':approximation(row[3]),'source':source,
                            'status':'reported by upstream register'})
        result=closed_form(n,family['intervals'])
        if result:
            bound,index=result
            reports.append({'bound':str(bound),'rounded_down':rational_floor(bound),'approximation':float(bound),
                            'source':family['source'],'source_revision':family['source_revision'],'interval':index,
                            'credit':'Hiroaki Hosono','status':'reported; full covering proof not independently replayed here'})
        unique=[];seen=set()
        for report in reports:
            key=(report['bound'],report.get('source'),report.get('status'))
            if key not in seen:seen.add(key);unique.append(report)
        best=max([verified,*unique],key=lambda r:(r['approximation'],revision in r.get('source','')))
        entries[str(n)]={'verified':verified,'reported':best,'reports':unique}
    return {'generated':datetime.now(timezone.utc).isoformat(),'max_n':max_n,
            'note':'Reported and verified lower bounds remain separate. Formula evaluation does not replay the covering proof; registration is not independent proof verification.',
            'source_register_revision':revision,'families':'lower_bound_families.json','entries':entries}


if __name__=='__main__':
    (ROOT/'lower_bounds.json').write_text(json.dumps(render(),indent=2)+'\n')
