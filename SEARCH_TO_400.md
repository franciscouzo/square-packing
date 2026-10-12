# Search through n=400

Enabled 2026-09-27. Two local workers continue David Ellsworth's refiner,
settling/flattening, Rust packing search, and LP refinement. Twelve workers on
`fran@192.168.0.200` continue CPU search, LP, and occasional CUDA annealing.
Half the jobs on each machine now target n=325–400; the other half continue
the previous campaign. Persistent, independent rotation counters cover every
new unsolved count, including those with integer reference bounds.

n=361 and n=400 have exact 19×19 and 20×20 grid witnesses. The area lower
bound sqrt(n) equals those side lengths, so optimization skips these two
proven optima. All 76 new counts have saved reference poses; 74 receive search.

The [Friedman/Ellsworth catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
systematically covers through n=324, with a few larger examples. Published
certificate submissions now supply published comparisons at some counts above
324. Their entries in `records.txt` remain **derived comparison bounds** for
the original campaign; current published bounds, sources, and standings come
from `known_best.json` and appear alongside those references in the README.
An improvement over a derived reference can still be superseded by a published
packing. Counts without a reviewed published comparison are labeled as such.

## Published comparisons, reviewed 12 October 2026

[Kevin Fang's submission #484](https://github.com/jlevy/squares/issues/484)
supplied rational certificates for n=343 and n=344. [Evan Daniel's Hunt 3
submission #489](https://github.com/jlevy/squares/issues/489) subsequently
improved both, crediting Fang's construction. The current source certificates
from both repositories passed fresh exact rational checks in this review.

| n | Fang's certified bound | Daniel's certified bound | Current external comparison |
|---:|---:|---:|---|
| 343 | 18.994903529221 | **18.978232523636** | Evan Daniel after Kevin Fang |
| 344 | 18.995489275431 | **18.994450514278** | Evan Daniel after Kevin Fang |

All four values above are rounded **upward** to 12 decimal places. The exact
rational sides, certificate hashes, pinned repository revisions, and source
links are retained by the importer. The local n=343 packing is superseded by
Daniel's result; the local n=344 packing is smaller than the reviewed external
bound. These are comparisons with the reviewed sources, not optimality proofs.

[Daniel's search notes at the reviewed revision](https://github.com/evand/square-packing/blob/31523f87316bdfda00f5459dd9077928e264f133/search/packer/PACKER.md#L942-L988)
also publish two n=375 certificates: `big1_n375.cert`, with S rounded up to
**19.906981767291**, and the earlier `polish_n375.cert`, **19.907024202137**.
Both passed fresh exact rational checks. These searches started from a Couzo
seed; the improved basin was subsequently adopted here and our current result
is smaller again. The published bounds remain in the comparison history even
though their geometries match archived packings here. They do not become new
competitors in the acceptance gate merely because a copy was published.

The six checked certificates provide published comparisons below the grid at
**three counts**, 343, 344, and 375, in 325–400. All six exact rational bounds,
SHA-256 hashes, pinned certificate URLs, source links and checked dates are
retained in `known_best.json` under `published_above_324`. Mishapolk's
exports in 343–360 were also examined; they equal or exceed the trivial grid
bound and do not replace the comparison table. Other rows retain a derived
reference comparison, without claiming that no published packing exists.
The corpus of formal case records remains n≤324: the jlevy/squares intake
keeps 343 and 344 in its verified beyond-horizon list.

The README generator reads this comparison data on every rebuild, so later
native improvements update the local side and standing without reverting to
the old reference-only table.

## Derived references and search

An m-square packing of side s can be extended by an L border: add floor(s)+1
axis-aligned squares in a column to its right, and floor(s) squares in a row
above it. This gives m+2 floor(s)+1 squares in side s+1. Repeat the construction
and delete surplus squares to reach a target count. A full grid supplies a
fallback. `expanded_reference_bounds.json` records the original catalogue
bound, source count, border layers, deletions, seed provenance, and hashes for
every new count. Bounds are frozen for consistent comparisons.

`expand_search.py --prepare` generated the initial references. At dispatch,
`construct_seed` also considers current local improvements and already improved
larger cases. Thus improvements in smaller packings automatically seed larger
ones without restarting the search. This may produce a better bound through
construction alone; such gains are not attributed solely to optimization.
The job certificate records the construction and source hash.

The existing acceptance gate remains in use: normalize against the saved
reference under rotations/reflections, require zero numerical overlap, and
independently verify an exact rational witness strictly better than both the
reference bound and the incumbent. Only the coordinator installs results.

The CUDA variant `sa_large` uses `-DLPP=8 -DPPB=4` above n=396; 512 blocks
retain 2,048 starts while fitting the RTX 3090's shared-memory limit. The
original PPB=8 variant uses 256 blocks for smaller cases. Rust and the LP and
Ellsworth pipelines use dynamically sized packings.

The service runs indefinitely and resumes on boot. `--max-n 400` is the
coordinator default; `experiments/forever/status.json` records the active limit
and running jobs. Reloads drain in-flight work before launching the new rotation.

Validation: all 76 saved references pass the Rust all-pairs geometry check.
Independent exact rational checks tested all 64,980 pairs for n=361 and
79,800 pairs for n=400 and confirmed both grids meet the area lower bound.
Sixteen Python tests cover the construction, complete scheduling coverage,
normalization, Ellsworth format conversion, and LP behavior. Short integration
runs exercised the local Ellsworth/packing/LP pipeline at n=399, remote CPU/LP
at n=400, and the PPB=4 CUDA/CPU-polishing/LP pipeline at n=400 (51,200
bytes shared memory per CUDA block). These short trials test operation, not search quality.
