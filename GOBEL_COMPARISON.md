# Göbel comparison

The all-count comparison is [gobel_comparison.csv](gobel_comparison.csv). It compares the verified index at commit `4e4c8ce23cb5e87f033021687010992c40575480` with the complete Göbel square and strip families, their corner-constrained strip variant, and deletion. The corrected index covers n=1..1024.

These are established constructions, credited to Frits Göbel and the family generalizations described by David Ellsworth. Their tighter algebraic values correct 73 index entries; 47 rows were removed from the registration draft because these constructions already match or beat them. The remaining draft lists 310 counts.

For n=416, a=10 and b=14 give n=2a(a+1)+b²=416 and exact side 11+7√2. Its upward-rounded display is **20.899494936612**, compared with the previous certificate display **20.899494936651**. The finite rational certificate remains a valid witness at its larger side.

## Formulas and sources

- [Göbel squares](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html): a−1 < b√2/2 < a+1; n=2a(a+1)+b²; s=a+1+b√2/2.
- [Göbel strips](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html): b=1+⌊(a−1)√2⌋; n=a(a+1)+2+b; s=a+1+√2/2.
- The corner-constrained strip variant on the same strip page has n=a(a+1)+3+b and s=2+(b+1)√2/2.

Every candidate construction through n=1024 was built and verified over Q(√2), using exact signs for containment and separating axes. The comparison also uses larger formula instances as benchmarks near the upper cutoff; those exceed the size-32 grid by the area bound and cannot improve any entry in scope.

## Verification and representation

[gobel_bounds.json](gobel_bounds.json) retains all 102 exact construction receipts, parameters, credits and the checker hash. Its `exact_bound` stores p and q in p+q√2. The `bound` field is an outward rational enclosure, preserving compatibility with existing consumers; the index chooses and propagates bounds by their exact algebraic values.

The spatial filter uses exact floors in cells of side 2. Squares whose centres lie in non-neighbouring cells cannot intersect, since a unit square has circumradius √2/2. Every potentially intersecting pair is checked with exact separating axes. Tests cover duplicate squares, shrunken containers, rotated contacts, very close rational approximations and agreement with an all-pair sweep.

A separate pinned jlevy/squares corner/edge verifier checked all pairs and unit-square shapes at n=5,27,202,416. Its source, hash and receipts are retained in `independent_checks`. It shares this report’s Q(√2) arithmetic; its geometry and all-pair enumeration are separate from the specialized centre tests.

Regenerate the construction receipts and complete index:

```sh
python3 gobel_bounds.py
python3 regen_bounds.py
python3 -m unittest test_gobel_bounds test_regen_bounds
```

The CSV is a historical before/after comparison; its previous-index column remains pinned to the stated commit. No new discovery or optimality claim is made for the Göbel bounds.

## Corrected entries

| n | Previous verified upper, rounded up | Exact Göbel bound | Source count |
|---:|---:|---|---:|
| 5 | 2.707106781187 | 2 + 1/2*sqrt(2) | 5 |
| 10 | 3.707106781187 | 3 + 1/2*sqrt(2) | 10 |
| 27 | 5.707106781187 | 5 + 1/2*sqrt(2) | 27 |
| 38 | 6.707106781187 | 6 + 1/2*sqrt(2) | 38 |
| 40 | 6.828427124747 | 4 + 2*sqrt(2) | 40 |
| 52 | 7.707106781187 | 7 + 1/2*sqrt(2) | 52 |
| 65 | 8.535533905933 | 5 + 5/2*sqrt(2) | 65 |
| 67 | 8.707106781187 | 8 + 1/2*sqrt(2) | 67 |
| 89 | 9.949747468306 | 5 + 7/2*sqrt(2) | 89 |
| 104 | 10.707106781187 | 10 + 1/2*sqrt(2) | 104 |
| 109 | 10.949747468306 | 6 + 7/2*sqrt(2) | 109 |
| 124 | 11.656854249493 | 6 + 4*sqrt(2) | 124 |
| 125 | 11.707106781187 | 11 + 1/2*sqrt(2) | 125 |
| 147 | 12.656854249493 | 7 + 4*sqrt(2) | 148 |
| 148 | 12.656854249493 | 7 + 4*sqrt(2) | 148 |
| 149 | 12.707106781187 | 12 + 1/2*sqrt(2) | 149 |
| 174 | 13.707106781187 | 13 + 1/2*sqrt(2) | 174 |
| 201 | 14.707106781187 | 14 + 1/2*sqrt(2) | 201 |
| 202 | 14.727922061358 | 2 + 9*sqrt(2) | 202 |
| 231 | 15.707106781187 | 15 + 1/2*sqrt(2) | 231 |
| 233 | 15.778174593053 | 8 + 11/2*sqrt(2) | 233 |
| 262 | 16.707106781187 | 16 + 1/2*sqrt(2) | 262 |
| 265 | 16.778174593053 | 9 + 11/2*sqrt(2) | 265 |
| 296 | 17.707106781187 | 17 + 1/2*sqrt(2) | 296 |
| 331 | 18.707106781187 | 18 + 1/2*sqrt(2) | 331 |
| 368 | 19.707106781187 | 19 + 1/2*sqrt(2) | 369 |
| 369 | 19.707106781187 | 19 + 1/2*sqrt(2) | 369 |
| 376 | 19.899494936612 | 10 + 7*sqrt(2) | 376 |
| 407 | 20.707106781187 | 20 + 1/2*sqrt(2) | 408 |
| 408 | 20.707106781187 | 20 + 1/2*sqrt(2) | 408 |
| 415 | 20.899494936612 | 11 + 7*sqrt(2) | 416 |
| 416 | 20.899494936651 | 11 + 7*sqrt(2) | 416 |
| 445 | 21.606601717827 | 11 + 15/2*sqrt(2) | 445 |
| 448 | 21.707106781187 | 21 + 1/2*sqrt(2) | 449 |
| 449 | 21.707106781187 | 21 + 1/2*sqrt(2) | 449 |
| 488 | 22.606601717827 | 12 + 15/2*sqrt(2) | 489 |
| 489 | 22.606601717845 | 12 + 15/2*sqrt(2) | 489 |
| 491 | 22.707106781187 | 22 + 1/2*sqrt(2) | 493 |
| 492 | 22.707106781187 | 22 + 1/2*sqrt(2) | 493 |
| 493 | 22.707106781227 | 22 + 1/2*sqrt(2) | 493 |
| 537 | 23.707106781187 | 23 + 1/2*sqrt(2) | 538 |
| 538 | 23.707106781227 | 23 + 1/2*sqrt(2) | 538 |
| 585 | 24.707106781227 | 24 + 1/2*sqrt(2) | 586 |
| 586 | 24.707106781231 | 24 + 1/2*sqrt(2) | 586 |
| 634 | 25.707106781225 | 25 + 1/2*sqrt(2) | 635 |
| 635 | 25.707106781231 | 25 + 1/2*sqrt(2) | 635 |
| 636 | 25.727922061390 | 13 + 9*sqrt(2) | 636 |
| 685 | 26.707106781220 | 26 + 1/2*sqrt(2) | 686 |
| 686 | 26.707106781231 | 26 + 1/2*sqrt(2) | 686 |
| 687 | 26.727922061390 | 14 + 9*sqrt(2) | 688 |
| 688 | 26.727922061420 | 14 + 9*sqrt(2) | 688 |
| 738 | 27.707106781220 | 27 + 1/2*sqrt(2) | 740 |
| 739 | 27.707106781231 | 27 + 1/2*sqrt(2) | 740 |
| 740 | 27.707106781239 | 27 + 1/2*sqrt(2) | 740 |
| 793 | 28.707106781220 | 28 + 1/2*sqrt(2) | 795 |
| 794 | 28.707106781231 | 28 + 1/2*sqrt(2) | 795 |
| 795 | 28.707106781239 | 28 + 1/2*sqrt(2) | 795 |
| 851 | 29.707106781231 | 29 + 1/2*sqrt(2) | 853 |
| 852 | 29.707106781235 | 29 + 1/2*sqrt(2) | 853 |
| 853 | 29.707106781235 | 29 + 1/2*sqrt(2) | 853 |
| 860 | 29.849242404954 | 15 + 21/2*sqrt(2) | 861 |
| 861 | 29.849242404954 | 15 + 21/2*sqrt(2) | 861 |
| 910 | 30.707106781225 | 30 + 1/2*sqrt(2) | 912 |
| 911 | 30.707106781235 | 30 + 1/2*sqrt(2) | 912 |
| 912 | 30.707106781235 | 30 + 1/2*sqrt(2) | 912 |
| 919 | 30.849242404954 | 16 + 21/2*sqrt(2) | 921 |
| 920 | 30.849242404954 | 16 + 21/2*sqrt(2) | 921 |
| 921 | 30.849242405004 | 16 + 21/2*sqrt(2) | 921 |
| 964 | 31.556349186143 | 16 + 11*sqrt(2) | 964 |
| 971 | 31.707106781225 | 31 + 1/2*sqrt(2) | 974 |
| 972 | 31.707106781227 | 31 + 1/2*sqrt(2) | 974 |
| 973 | 31.707106781227 | 31 + 1/2*sqrt(2) | 974 |
| 974 | 31.707106781227 | 31 + 1/2*sqrt(2) | 974 |
