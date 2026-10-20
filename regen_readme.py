#!/usr/bin/env python3
"""Refresh the README's current records without listing retained foreign seeds."""
from pathlib import Path

from readme_records import END, START, catalogue, render


def main():
    records, omitted, context = catalogue()
    path = Path('README.md')
    before = path.read_text()
    block = render(records, context)
    if START in before and END in before:
        start, end = before.index(START), before.index(END) + len(END)
    else:
        # Migrate the old catalogue/status tables and their example images.
        start = before.index('| n | previous best known |')
        marker = '<!-- /complete-bound-catalogue -->'
        end = before.index(marker) + len(marker)
    after = before[:start] + block + before[end:]
    if after != before:
        path.write_text(after)
        print(f'README updated: {len(records)} current records; {len(omitted)} retained packings omitted')
    else:
        print(f'README already current: {len(records)} records; {len(omitted)} retained packings omitted')


if __name__ == '__main__':
    main()
