"""Retain exact L-border consequences of the verified classical families."""
import hashlib
from pathlib import Path

from gobel_bounds import exact_value


def l_border_catalogue(catalogues, max_n=1024):
    """Extend (m, s) to (m + 2 floor(s) + 1, s + 1), repeatedly.

    The right column holds floor(s)+1 aligned squares and the top row
    holds floor(s); their interiors avoid each other and the old box.
    Deletion is applied separately by the complete bound index.
    """
    selected = {}
    checker_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    for catalogue in catalogues:
        for key, parent in catalogue.items():
            source_n = int(key)
            count, side, layers = source_n, exact_value(parent), 0
            while count <= max_n:
                entry = dict(parent)
                if layers:
                    entry.update(
                        bound=str(side.enclosure()[1]), exact_bound=side.record(),
                        source_n=count, deleted_squares=0,
                        status='exact L-border extension of a verified algebraic construction',
                        construction={
                            'kind': 'L-border', 'source_n': source_n,
                            'source_bound': parent['bound'],
                            'source_exact_bound': parent['exact_bound'],
                            'layers': layers, 'capacity': count,
                            'checker': 'construction_bounds.py',
                            'checker_sha256': checker_sha})
                previous = selected.get(str(count))
                if previous is None or side < exact_value(previous):
                    selected[str(count)] = entry
                count += 2 * side.floor() + 1
                side += 1
                layers += 1
    return selected
