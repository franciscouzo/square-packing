"""Current record claims for the README, separate from retained search seeds."""
from fractions import Fraction
import json
from pathlib import Path

from gobel_bounds import Q2, exact_value

START = '<!-- current-records -->'
END = '<!-- /current-records -->'
ROUNDING = Q2(Fraction(1, 10**10))


def our_credit(credit):
    credit = (credit or '').casefold().strip()
    return (credit == 'this project' or credit.startswith('this repository;')
            or credit == 'franciscouzo' or credit.startswith(('franciscouzo (', 'franciscouzo;'))
            or credit == 'francisco couzo' or credit.startswith('francisco couzo;')
            or credit.startswith('francisco couzo ('))


def classification(metadata, public, registered):
    """Publication of our own witness must not retire the record we hold.

    Ownership comes from the best public comparison, never from a superseded
    local claim or an older registration credit.
    """
    ours = Q2(Fraction(metadata['rational_side']))
    other = exact_value(public)
    if other < ours:
        return None
    if our_credit(public.get('credit')):
        return ('Refinement of our published record' if ours < other
                else 'Published record held by this project')
    if ours < other - ROUNDING:
        return 'Improvement over public bound'
    return None


def read(path):
    return json.loads(path.read_text())


def public_comparison(n, public, known):
    """Honor a newer importer result if it improves the reviewed snapshot."""
    best = public.get(str(n))
    for table in ['entries', 'published_above_324', 'public_comparisons']:
        entry = known.get(table, {}).get(str(n), {})
        if entry.get('side') is None:
            continue
        external = entry.get('external') if entry.get('source') != 'register' else None
        candidate = dict(bound=external['side'] if external else str(entry['side']),
                         credit=external.get('credit', '') if external else
                         ', '.join(entry.get('register_found_by') or []),
                         source=external.get('request', '') if external else
                         f'https://jlevy.github.io/squares/cases/{n}.html')
        # Exact certificates take precedence even for a tiny gain. Register
        # display decimals can round below their certificate, so retain the
        # reporting tolerance only for those approximate comparisons.
        margin = Q2(0) if external else ROUNDING
        if best is None or exact_value(candidate) < exact_value(best) - margin:
            best = candidate
    return best


def catalogue(root=Path('.')):
    root = Path(root)
    known = read(root/'known_best.json')
    public = read(root/'public_bounds.json')
    manifest = read(root/'certificates/best/manifest.json')
    records, omitted = {}, {}
    for path in root.glob('n[0-9]*.txt'):
        n = int(path.stem[1:])
        metadata = read(root/f'certificates/n{n}.json')
        comparison = public_comparison(n, public['entries'], known)
        status = classification(metadata, comparison, known.get('entries', {}).get(str(n), {})) if comparison else None
        if status is None:
            omitted[n] = 'No current record credit or improvement over the reviewed public bound'
            continue
        records[n] = dict(n=n, metadata=metadata, public=comparison, status=status)
    context = dict(date=max(public['generated'], known['generated'])[:10],
                   max_n=public['max_n'], witnesses=len(manifest['witnesses']))
    return records, omitted, context


def render(records, context):
    lines = [START, '', '## Current records', '',
             f'Reviewed {context["date"]}: **{len(records)} counts** — '
             'published records held by this project and improvements over the reviewed public bound.', '',
             'Each n opens its packing. Certified sides and public comparisons are rounded upward to '
             '12 decimal places. Matching our own published bound retains the record and its credit; '
             'a stronger public bound supersedes it. Matching another author’s record does not claim ownership. '
             'Construction, seed and certificate credits are linked for each packing. '
             'Updates to our own packings have no minimum gain: their exact certified bound '
             'must strictly decrease. The `1e-10` reporting tolerance applies only to claims of '
             'new improvements over another author’s public bound.', '',
             '| n | certified side s | reviewed public bound | standing | credits |',
             '|---:|---:|---:|---|---|']
    for n, row in sorted(records.items()):
        side = Q2(Fraction(row['metadata']['rational_side'])).rounded_up()
        public = exact_value(row['public']).rounded_up()
        source = row['public'].get('source', '')
        if source.startswith(('https://', 'http://')):
            public = f'[{public}]({source})'
        lines.append(f'| [{n}](n{n}.svg) | [{side}](certificates/n{n}.cert) | {public} | '
                     f'{row["status"]} | [credits](certificates/n{n}.json) |')
    lines += ['', f'The [complete bound catalogue](certificates/best/README.md) covers n=1–{context["max_n"]} '
              f'and retains {context["witnesses"]} finite source witnesses, including imported packings and '
              'classical constructions. Historical improvements and search seeds remain in the repository '
              'with their provenance.', '', END]
    return '\n'.join(lines)
