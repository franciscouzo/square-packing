"""Published comparisons alongside frozen reference bounds through n=1024."""
from fractions import Fraction
import math

MARKER = '<!-- expanded-search-results -->'
END_MARKER = '<!-- /expanded-search-results -->'
ROUNDING = Fraction(1, 10**10)
PUBLISHED_MAX = 324


def reviewed_publications(found, verified, sources, credit_for, request_for, max_n=1024):
    """Retain verified published bounds, including those adopted by our search.

    This is documentation data. The importer's competitor entries and seed
    selection still exclude geometries already archived in this repository.
    """
    comparisons = {}
    for n, candidates in sorted(found.items()):
        if not PUBLISHED_MAX < n <= max_n:
            continue
        publications = []
        for item in sorted(candidates, key=lambda item: Fraction(item['side'])):
            check = verified.get(item['sha256'], {})
            if not check.get('valid') or Fraction(item['side']) >= math.isqrt(n-1)+1:
                continue
            source = sources[item['source']]
            relative = item['path'].split('/', 1)[1]
            publication = {
                'side': str(item['side']), 'source': item['source'],
                'credit': credit_for(item['source'], item['path']),
                'request': request_for(item['source'], item['path']),
                'certificate': item['path'], 'sha256': item['sha256'],
                'certificate_url': source['url'].removesuffix('.git')+'/blob/'
                                   +source['commit']+'/'+relative,
                'checked': check.get('checked'),
            }
            if item.get('same_as_ours'):
                publication['same_as_ours'] = item['same_as_ours']
            publications.append(publication)
        if publications:
            best = publications[0]
            comparisons[str(n)] = {
                'side': float(Fraction(best['side'])), 'source': best['source'],
                'external': best, 'certificates': publications,
            }
    return comparisons


def comparison_entry(known, n):
    current=(known.get('published_above_324', {}).get(str(n))
             or known.get('entries', {}).get(str(n)))
    reviewed=known.get('public_comparisons', {}).get(str(n))
    if reviewed and (not current or reviewed['side']<current['side']-1e-10):
        return reviewed
    return current


def rounded_up(value, places=12):
    scaled = Fraction(value)*10**places
    ceiling = -(-scaled.numerator//scaled.denominator)
    return f'{ceiling//10**places}.{ceiling%10**places:0{places}d}'


def external_comparison(side, entry):
    """Return a reviewed published bound, source link and local standing."""
    if not entry or entry.get('side') is None:
        return '—', '—', 'reference comparison only'
    external = entry.get('external')
    other = Fraction(external['side']) if external and entry.get('source') != 'register' else Fraction(str(entry['side']))
    ours = Fraction(str(side))
    if ours < other-ROUNDING:
        status = '**smaller than reviewed published bound**'
    elif ours <= other+ROUNDING:
        status = 'tied (within 1e-10)'
    else:
        status = f'superseded by {float(ours-other):.1e}'
    if external and entry.get('source') != 'register':
        credit = external['credit'].replace('|', '&#124;').replace('\n', ' ')
        source = f'[{credit}]({external["request"]})'
    else:
        source = '[register](https://jlevy.github.io/squares/)'
    return rounded_up(other), source, status


def render(rows, known):
    """Extend the original four-column rows without changing frozen comparisons."""
    table = []
    reviewed = 0
    for row in rows:
        fields = row.split('|')
        n = int(fields[1])
        side = fields[3].strip().strip('*')
        other, source, status = external_comparison(side, comparison_entry(known, n))
        reviewed += other != '—'
        table.append(row+f' {other} | {source} | {status} |')
    date = known.get('generated', '')[:10]
    coverage = f' Reviewed published comparisons cover {reviewed} of these {len(rows)} counts'
    if date:
        coverage += f' as of {date}'
    coverage += '.'
    upper = max([400, *[int(row.split('|')[1]) for row in rows]])
    return (MARKER+f'\n\nRecorded packings also cover n=325–{upper}. The derived reference bounds '
            'remain the frozen L-border/grid comparisons. Published bounds '
            'come from the reviewed sources in `known_best.json`; their values below '
            'are rounded upward.'+coverage+' A dash means no published comparison '
            'was established in the reviewed sources. Source revisions and certificate links '
            'are recorded in [known_best.json](known_best.json).\n\n'
            '| n | derived reference bound | found here (numerical) | improvement over reference | '
            'reviewed public bound | published source | standing |\n'
            '|---|---|---|---|---|---|---|\n'+'\n'.join(table)+'\n\n'+END_MARKER)
