# Record square packings

Current arrangements and refinements credited to Francisco Couzo for packing
`n` unit squares in a square of side `s`. The table uses the reviewed public
registry, issues, PRs and construction bounds to select the records still held.

[Upper bounds](upper_bounds.json) cover every count through n=10000;
[lower bounds](lower_bounds.json) cover every count through n=1024.
The [reviewed public bounds](public_bounds.json) include the registry, open issues,
PRs and construction consequences. The [20 October reconciliation](certificates/review-20261020/README.md)
records the comparison and archived claims.
Exact certificate bounds, frozen reference comparisons,
and reported lower-bound or optimality claims retain their source and verification
status. The [closed-form lower-bound parameters](lower_bound_families.json) can be
evaluated with `lower_bounds.py`; evaluating the formula does not replay its proof.

Live packings are kept in one transactional store on CT105. The web app and Desktopo read its current bounds and immutable seeds; native results use the same exact acceptance path as browser results. Repository files are reviewed Git snapshots. See [Packing store](PACKING_STORE.md) for operation and record intake.

The [publication-order and attribution review](RECORD_PROVENANCE.md) separates
construction, refinement and certificate credit, with
[source metadata for every count through 1024](record_provenance.json).
Tighter certification preserves the original arrangement credit. Imported and
superseded packings remain available in the full catalogue and search archives.

[Kaggle export](KAGGLE.md) prepares the current packings for n=1–1000, with source credits and local verification against the competition metric.

<!-- current-records -->

## Current records

Reviewed 2026-10-23: **71 counts** — published records held by this project and improvements over the reviewed public bound.

Each n opens its packing. Certified sides and public comparisons are rounded upward to 12 decimal places. Matching our own published bound retains the record and its credit, as does another author’s re-certification within `1e-10` of a packing credited to us; a public bound stronger by more than that supersedes it. Matching another author’s record does not claim ownership. Construction, seed and certificate credits are linked for each packing. Updates to our own packings have no minimum gain: their exact certified bound must strictly decrease. The `1e-10` reporting tolerance applies only to claims of new improvements over another author’s public bound and to keeping a record credited to us.

| n | certified side s | reviewed public bound | standing | credits |
|---:|---:|---:|---|---|
| [68](n68.svg) | [8.798795237219](certificates/n68.cert) | [8.798795237219](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n68.json) |
| [106](n106.svg) | [10.822908044133](certificates/n106.cert) | [10.822908044133](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n106.json) |
| [110](n110.svg) | [10.996783396632](certificates/n110.cert) | [10.996783396632](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n110.json) |
| [127](n127.svg) | [11.810878787590](certificates/n127.cert) | [11.810878787590](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n127.json) |
| [152](n152.svg) | [12.830718800977](certificates/n152.cert) | [12.830718800977](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n152.json) |
| [156](n156.svg) | [12.979165853835](certificates/n156.cert) | [12.979165853835](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n156.json) |
| [172](n172.svg) | [13.618988956900](certificates/n172.cert) | [13.618988956900](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n172.json) |
| [177](n177.svg) | [13.822979734170](certificates/n177.cert) | [13.822979734170](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n177.json) |
| [180](n180.svg) | [13.916993522478](certificates/n180.cert) | [13.916993522478](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n180.json) |
| [182](n182.svg) | [13.974090713122](certificates/n182.cert) | [13.974090713122](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n182.json) |
| [206](n206.svg) | [14.860158663392](certificates/n206.cert) | [14.860158663392](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n206.json) |
| [209](n209.svg) | [14.946223226447](certificates/n209.cert) | [14.946223226447](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n209.json) |
| [210](n210.svg) | [14.973001116588](certificates/n210.cert) | [14.973001116588](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n210.json) |
| [211](n211.svg) | [14.993549626300](certificates/n211.cert) | [14.993549626300](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-211.cert.gz) | Published record held by this project | [credits](certificates/n211.json) |
| [227](n227.svg) | [15.563625652326](certificates/n227.cert) | [15.563625652326](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-227.cert.gz) | Published record held by this project | [credits](certificates/n227.json) |
| [228](n228.svg) | [15.604601475730](certificates/n228.cert) | [15.604601475730](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n228.json) |
| [237](n237.svg) | [15.902603638260](certificates/n237.cert) | [15.902603638260](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-237.cert.gz) | Published record held by this project | [credits](certificates/n237.json) |
| [240](n240.svg) | [15.969685337531](certificates/n240.cert) | [15.969685337531](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n240.json) |
| [241](n241.svg) | [15.987117095151](certificates/n241.cert) | [15.987117095151](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-241.cert.gz) | Published record held by this project | [credits](certificates/n241.json) |
| [260](n260.svg) | [16.645753250520](certificates/n260.cert) | [16.645753250520](https://github.com/evand/square-packing/blob/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/regularize/lists/certs/n-260.cert.gz) | Published record held by this project | [credits](certificates/n260.json) |
| [267](n267.svg) | [16.838815269949](certificates/n267.cert) | [16.838815269949](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n267.json) |
| [273](n273.svg) | [16.983925962651](certificates/n273.cert) | [16.983925962651](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n273.json) |
| [297](n297.svg) | [17.740417287544](certificates/n297.cert) | [17.740417287544](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n297.json) |
| [301](n301.svg) | [17.846667192844](certificates/n301.cert) | [17.846667192844](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n301.json) |
| [302](n302.svg) | [17.870013850405](certificates/n302.cert) | [17.870013850405](https://github.com/jlevy/squares/issues/593) | Published record held by this project | [credits](certificates/n302.json) |
| [303](n303.svg) | [17.907473001999](certificates/n303.cert) | [17.908331255817](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n303.json) |
| [306](n306.svg) | [17.963433717492](certificates/n306.cert) | [17.963433717492](https://github.com/jlevy/squares/pull/574) | Published record held by this project | [credits](certificates/n306.json) |
| [328](n328.svg) | [18.614368938495](certificates/n328.cert) | [18.614368938491](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Published record held by this project | [credits](certificates/n328.json) |
| [336](n336.svg) | [18.825571499862](certificates/n336.cert) | [18.825571499862](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n336.json) |
| [337](n337.svg) | [18.858391767637](certificates/n337.cert) | [18.858391767637](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n337.json) |
| [365](n365.svg) | [19.614368938495](certificates/n365.cert) | [19.614368938491](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Published record held by this project | [credits](certificates/n365.json) |
| [373](n373.svg) | [19.823062082838](certificates/n373.cert) | [19.823062082838](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n373.json) |
| [374](n374.svg) | [19.832356217033](certificates/n374.cert) | [19.832356217033](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n374.json) |
| [417](n417.svg) | [20.905466137190](certificates/n417.cert) | [20.907676811601](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n417.json) |
| [420](n420.svg) | [20.966577898708](certificates/n420.cert) | [20.966577906822](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n420.json) |
| [465](n465.svg) | [21.999896124666](certificates/n465.cert) | 22.000000000000 | Improvement over public bound | [credits](certificates/n465.json) |
| [503](n503.svg) | [22.899951089308](certificates/n503.cert) | [22.905523107849](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n503.json) |
| [505](n505.svg) | [22.939236268018](certificates/n505.cert) | [22.940976207828](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n505.json) |
| [506](n506.svg) | [22.953204939148](certificates/n506.cert) | [22.962143184574](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n506.json) |
| [550](n550.svg) | [23.913405774122](certificates/n550.cert) | [23.915000004584](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n550.json) |
| [553](n553.svg) | [23.969774304321](certificates/n553.cert) | [23.969821595520](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n553.json) |
| [555](n555.svg) | [23.990765768282](certificates/n555.cert) | [23.993580713533](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n555.json) |
| [596](n596.svg) | [24.888953762946](certificates/n596.cert) | [24.890372922832](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n596.json) |
| [601](n601.svg) | [24.963638694988](certificates/n601.cert) | [24.971076834193](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n601.json) |
| [700](n700.svg) | [26.908095391519](certificates/n700.cert) | [26.908398596052](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n700.json) |
| [704](n704.svg) | [26.965244421291](certificates/n704.cert) | [26.974262142927](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n704.json) |
| [759](n759.svg) | [27.976916273370](certificates/n759.cert) | [27.982237988867](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n759.json) |
| [850](n850.svg) | [29.656854249499](certificates/n850.cert) | [29.656854249493](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Published record held by this project | [credits](certificates/n850.json) |
| [922](n922.svg) | [30.842386806015](certificates/n922.cert) | [30.845247910673](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n922.json) |
| [983](n983.svg) | [31.832540815612](certificates/n983.cert) | [31.832544847969](https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard) | Improvement over public bound | [credits](certificates/n983.json) |
| [1335](n1335.svg) | [36.990072025463](certificates/n1335.cert) | [36.990072025463](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n1335.json) |
| [1486](n1486.svg) | [38.996570702336](certificates/n1486.cert) | [38.997149121271](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/1000-1999/n1486.cert) | Improvement over public bound | [credits](certificates/n1486.json) |
| [1647](n1647.svg) | [40.997969720754](certificates/n1647.cert) | [40.998670469324](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/1000-1999/n1568.cert) | Improvement over public bound | [credits](certificates/n1647.json) |
| [1648](n1648.svg) | [40.998874333857](certificates/n1648.cert) | [40.999321109325](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n1648.json) |
| [1727](n1727.svg) | [41.997969720754](certificates/n1727.cert) | [41.998670469324](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/1000-1999/n1567.cert) | Improvement over public bound | [credits](certificates/n1727.json) |
| [1729](n1729.svg) | [41.998874333857](certificates/n1729.cert) | [41.999321109325](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n1729.json) |
| [1765](n1765.svg) | [42.487684364192](certificates/n1765.cert) | [42.487978511861](https://kingbird.myphotos.cc/packing/squares_in_squares.html) | Improvement over public bound | [credits](certificates/n1765.json) |
| [1811](n1811.svg) | [42.997550241724](certificates/n1811.cert) | [42.997550241724](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n1811.json) |
| [1812](n1812.svg) | [42.997600183876](certificates/n1812.cert) | [42.997600183876](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n1812.json) |
| [1898](n1898.svg) | [43.999267313246](certificates/n1898.cert) | [43.999336623227](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n1898.json) |
| [1899](n1899.svg) | [43.999336623227](certificates/n1899.cert) | [43.999336623227](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n1899.json) |
| [1986](n1986.svg) | [44.997600183879](certificates/n1986.cert) | [44.997600183879](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n1986.json) |
| [2043](n2043.svg) | [45.695704158830](certificates/n2043.cert) | [45.695704158830](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n2043.json) |
| [2076](n2076.svg) | [45.997550240009](certificates/n2076.cert) | [45.997550240009](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n2076.json) |
| [2263](n2263.svg) | [47.999142007370](certificates/n2263.cert) | [47.999256231755](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n2263.json) |
| [2359](n2359.svg) | [48.997550269630](certificates/n2359.cert) | [48.997550269630](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n2359.json) |
| [4168](n4168.svg) | [64.999256232549](certificates/n4168.cert) | [64.999256232549](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n4168.json) |
| [4430](n4430.svg) | [66.997550243025](certificates/n4430.cert) | [66.997550243025](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n4430.json) |
| [4701](n4701.svg) | [68.999256219267](certificates/n4701.cert) | [68.999256219267](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n4701.json) |
| [4839](n4839.svg) | [69.997550252215](certificates/n4839.cert) | [69.997550252215](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n4839.json) |
| [8021](n8021.svg) | [89.999256219591](certificates/n8021.cert) | [89.999256219591](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n8021.json) |

The [complete bound catalogue](certificates/best/README.md) covers n=1–10000 and retains 1087 finite source witnesses, including imported packings and classical constructions. Historical improvements and search seeds remain in the repository with their provenance.

<!-- /current-records -->
