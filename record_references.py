"""Frozen comparison values for documentation, separate from current records."""
import json
from pathlib import Path


def load(root=Path('.')):
    root = Path(root)
    values = {int(row[0]):row[1] for line in (root/'records.txt').read_text().splitlines()
              if (row:=line.split()) and not line.startswith('#')}
    path = root/'record_reference_bounds.json'
    if path.exists():
        for key, row in json.loads(path.read_text())['entries'].items():
            values.setdefault(int(key), row['rounded_up'])
    return values
