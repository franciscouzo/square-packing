# Kaggle Squares in Squares export

The [competition](https://www.kaggle.com/competitions/squares-in-squares)
scores n=1–1000. A complete file contains 500,500 rows with columns
`id,n,square_id,x,y,angle`. Angles are in radians. The score is the sum of
`L/sqrt(n) - 1`, with smaller scores preferred. The container side is measured
from the submitted coordinates.

Install [requirements-kaggle.txt](requirements-kaggle.txt) in a separate Python
environment, then export the reviewed catalogue:

```sh
python prepare_kaggle.py --output submissions/kaggle-squares-20261022
```

The output directory contains `submission.csv` and `sources.json`, which binds
each packing to its certificate or classical construction and retains credit.
Generated submissions are excluded from Git. Upload the CSV with Kaggle's
**Submit Predictions** button after joining the competition.

The exporter retains exact half-integer grids. Other packings use 100-digit
arithmetic and 75-significant-digit decimal coordinates and angles. Centres
are separated by a factor of `1 + 1e-40` to preserve disjoint interiors when
touching rational or algebraic rotations become decimal angles. This changes
container sides far below double precision.

The current export's local validation uses the published [competition
metric](https://www.kaggle.com/code/metric/squares-in-squares), version 17,
SHA-256 `66bff90fbf8475bac64b89221a29260ab41e78c9007c3c663728d83e2f2617f8`.
The metric is Apache-2.0 licensed. Its parsing, interval SAT, precision
escalation, measurement and scoring functions run unchanged; immutable
interval calculations are memoized with the working precision in each cache
key. Cached and uncached checks agree on the retained sample cases.

`validation.json` records the score, input hash and acceptance of every puzzle.
`submission_details.csv` contains the metric's measured sides at 50 decimal
places. These are local checks; the uploaded file receives its official score
on Kaggle.
