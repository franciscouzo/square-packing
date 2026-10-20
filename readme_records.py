"""Current record claims for the README, separate from retained search seeds."""
from fractions import Fraction
import json
from pathlib import Path

from gobel_bounds import Q2, exact_value

START = '<!-- current-records -->'
END = '<!-- /current-records -->'
ROUNDING = Q2(Fraction(1, 10**10))


def our_credit(credit):
    credit = credit.casefold().strip()
    return (credit == 'franciscouzo' or credit.startswith('franciscouzo (')
            or credit == 'francisco couzo' or credit.startswith('francisco couzo;')
            or credit.startswith('francisco couzo ('))


def classification(metadata, public, registered):
    """A tied imported witness or classical construction is not our record."""
    ours = Q2(Fraction(metadata['rational_side']))
    other = exact_value(public)
    if other + ROUNDING < ours:
        return None
    if ours < other - ROUNDING:
        return 'Improvement over public bound'
    register_bound = registered.get('register')
    if (register_bound is not None
            and any(our_credit(who) for who in registered.get('register_found_by') or [])
            and not ROUNDING < abs(ours - Q2(Fraction(str(register_bound))))):
        return 'Registered'
    origin = metadata.get('origin', {})
    precision = origin.get('source_provenance') or {}
    if (precision.get('precision_only')
            and our_credit(precision.get('original_record_credit', ''))):
        return 'Published'
    # Preserve native refinements of adopted witnesses when the retained seed
    # side establishes a real gain; a search_job alone supplies no such proof.
    seed = origin.get('seed_certificate') or {}
    native_gain = (origin.get('search_job') and seed.get('side')
                   and ours < Q2(Fraction(seed['side'])) - ROUNDING)
    adopted = (origin.get('category') == 'reviewed public submission'
               and not origin.get('web_seed') and not origin.get('refined_by')
               and not native_gain)
    if our_credit(public.get('credit', '')) and not adopted:
        return 'Published'
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
        if best is None or exact_value(candidate) < exact_value(best) - ROUNDING:
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
    counts = {status: sum(row['status'] == status for row in records.values())
              for status in ['Registered', 'Published', 'Improvement over public bound']}
    lines = [START, '', '## Current records', '',
             f'Reviewed {context["date"]}: **{len(records)} counts** — '
             f'{counts["Registered"]} registered, {counts["Published"]} published, and '
             f'{counts["Improvement over public bound"]} improvements over the reviewed public bound.', '',
             'Each n opens its packing. Certified sides and public comparisons are rounded upward to '
             '12 decimal places. A difference within `1e-10` is treated as rounding; '
             'such a tie is listed only when record credit is retained here. '
             'Construction, seed and certificate credits are linked for each packing.', '',
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
