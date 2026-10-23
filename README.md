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

Reviewed 2026-10-22: **148 counts** — published records held by this project and improvements over the reviewed public bound.

Each n opens its packing. Certified sides and public comparisons are rounded upward to 12 decimal places. Matching our own published bound retains the record and its credit; a stronger public bound supersedes it. Matching another author’s record does not claim ownership. Construction, seed and certificate credits are linked for each packing. Updates to our own packings have no minimum gain: their exact certified bound must strictly decrease. The `1e-10` reporting tolerance applies only to claims of new improvements over another author’s public bound.

| n | certified side s | reviewed public bound | standing | credits |
|---:|---:|---:|---|---|
| [328](n328.svg) | [18.614368938495](certificates/n328.cert) | [18.614368938513](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n328.json) |
| [336](n336.svg) | [18.825571499862](certificates/n336.cert) | [18.825571499862](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n336.json) |
| [337](n337.svg) | [18.858391767637](certificates/n337.cert) | [18.858391767637](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n337.json) |
| [338](n338.svg) | [18.906332809853](certificates/n338.cert) | [18.906332809853](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n338.json) |
| [340](n340.svg) | [18.939649632892](certificates/n340.cert) | [18.939649632892](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n340.json) |
| [341](n341.svg) | [18.951882408720](certificates/n341.cert) | [18.951882408720](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n341.json) |
| [343](n343.svg) | [18.977575126250](certificates/n343.cert) | [18.977575126267](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n343.json) |
| [365](n365.svg) | [19.614368938495](certificates/n365.cert) | [19.614368938513](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n365.json) |
| [373](n373.svg) | [19.823062082838](certificates/n373.cert) | [19.823062082838](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n373.json) |
| [374](n374.svg) | [19.832356217033](certificates/n374.cert) | [19.832356217033](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n374.json) |
| [404](n404.svg) | [20.614368938495](certificates/n404.cert) | [20.614368938513](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n404.json) |
| [420](n420.svg) | [20.966577898708](certificates/n420.cert) | [20.966588191179](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n420.cert) | Improvement over public bound | [credits](certificates/n420.json) |
| [422](n422.svg) | [20.983570193585](certificates/n422.cert) | [20.983575254580](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n422.cert) | Improvement over public bound | [credits](certificates/n422.json) |
| [454](n454.svg) | [21.824764034677](certificates/n454.cert) | [21.828427124769](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n454.cert) | Improvement over public bound | [credits](certificates/n454.json) |
| [455](n455.svg) | [21.846667192857](certificates/n455.cert) | [21.848427413955](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n455.json) |
| [456](n456.svg) | [21.875426651387](certificates/n456.cert) | [21.881306218113](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n456.cert) | Improvement over public bound | [credits](certificates/n456.json) |
| [458](n458.svg) | [21.903616795094](certificates/n458.cert) | [21.903616797192](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n458.json) |
| [459](n459.svg) | [21.937021053087](certificates/n459.cert) | [21.937022304151](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n459.json) |
| [461](n461.svg) | [21.963794208477](certificates/n461.cert) | [21.964134536435](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n461.cert) | Improvement over public bound | [credits](certificates/n461.json) |
| [462](n462.svg) | [21.965535885145](certificates/n462.cert) | [21.966192211190](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n462.cert) | Improvement over public bound | [credits](certificates/n462.json) |
| [463](n463.svg) | [21.971122057117](certificates/n463.cert) | [21.971254044975](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n463.json) |
| [496](n496.svg) | [22.822875655538](certificates/n496.cert) | [22.822875655559](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n496.json) |
| [497](n497.svg) | [22.823102656271](certificates/n497.cert) | [22.823102656285](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n497.json) |
| [499](n499.svg) | [22.866399781552](certificates/n499.cert) | [22.881306218113](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n456.cert) | Improvement over public bound | [credits](certificates/n499.json) |
| [500](n500.svg) | [22.886007770011](certificates/n500.cert) | [22.887841512273](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n500.json) |
| [501](n501.svg) | [22.887683574922](certificates/n501.cert) | [22.887841512273](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n501.json) |
| [502](n502.svg) | [22.933269925480](certificates/n502.cert) | [22.933269925480](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n502.json) |
| [503](n503.svg) | [22.943933771519](certificates/n503.cert) | [22.943933771540](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n503.json) |
| [504](n504.svg) | [22.961828398888](certificates/n504.cert) | [22.961828398888](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n504.json) |
| [505](n505.svg) | [22.964182800913](certificates/n505.cert) | [22.964182800913](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n505.json) |
| [506](n506.svg) | [22.971122057117](certificates/n506.cert) | [22.971213308854](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n506.cert) | Improvement over public bound | [credits](certificates/n506.json) |
| [509](n509.svg) | [22.993588501431](certificates/n509.cert) | [22.993588501431](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n509.json) |
| [545](n545.svg) | [23.883159509357](certificates/n545.cert) | [23.883414761903](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n545.json) |
| [546](n546.svg) | [23.887683574922](certificates/n546.cert) | [23.887841512273](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n546.json) |
| [547](n547.svg) | [23.898819144794](certificates/n547.cert) | [23.898819144794](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n547.json) |
| [548](n548.svg) | [23.920310216788](certificates/n548.cert) | [23.943933771540](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n548.json) |
| [549](n549.svg) | [23.955467723214](certificates/n549.cert) | [23.955501804754](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n549.json) |
| [550](n550.svg) | [23.960681444798](certificates/n550.cert) | [23.960681444798](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n550.json) |
| [551](n551.svg) | [23.964873439804](certificates/n551.cert) | [23.965801641963](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n551.cert) | Improvement over public bound | [credits](certificates/n551.json) |
| [553](n553.svg) | [23.977927639657](certificates/n553.cert) | [23.978921076228](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n553.cert) | Improvement over public bound | [credits](certificates/n553.json) |
| [554](n554.svg) | [23.986307325908](certificates/n554.cert) | [23.986307325908](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n554.json) |
| [592](n592.svg) | [24.882927273823](certificates/n592.cert) | [24.883414761903](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n592.json) |
| [593](n593.svg) | [24.887683574922](certificates/n593.cert) | [24.887841512273](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n593.json) |
| [594](n594.svg) | [24.896263780065](certificates/n594.cert) | [24.898819144794](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n594.json) |
| [595](n595.svg) | [24.920310216788](certificates/n595.cert) | [24.943933771540](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n595.json) |
| [596](n596.svg) | [24.948767393866](certificates/n596.cert) | [24.949747468331](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n596.cert) | Improvement over public bound | [credits](certificates/n596.json) |
| [597](n597.svg) | [24.948816876704](certificates/n597.cert) | [24.950690418637](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n597.json) |
| [598](n598.svg) | [24.953332793068](certificates/n598.cert) | [24.954250129268](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n598.json) |
| [599](n599.svg) | [24.959619754559](certificates/n599.cert) | [24.959619792263](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n599.cert) | Improvement over public bound | [credits](certificates/n599.json) |
| [600](n600.svg) | [24.977927639657](certificates/n600.cert) | [24.978172747238](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n600.json) |
| [602](n602.svg) | [24.987891297022](certificates/n602.cert) | [24.988237878425](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n602.json) |
| [641](n641.svg) | [25.880039037912](certificates/n641.cert) | [25.881306218116](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n641.cert) | Improvement over public bound | [credits](certificates/n641.json) |
| [643](n643.svg) | [25.896263780065](certificates/n643.cert) | [25.898819144794](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n643.json) |
| [645](n645.svg) | [25.907009805052](certificates/n645.cert) | [25.946623458826](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n645.cert) | Improvement over public bound | [credits](certificates/n645.json) |
| [646](n646.svg) | [25.946523722610](certificates/n646.cert) | [25.946653181671](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n646.cert) | Improvement over public bound | [credits](certificates/n646.json) |
| [647](n647.svg) | [25.946936319318](certificates/n647.cert) | [25.946936912812](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n647.cert) | Improvement over public bound | [credits](certificates/n647.json) |
| [648](n648.svg) | [25.959072621826](certificates/n648.cert) | [25.959619775225](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n648.cert) | Improvement over public bound | [credits](certificates/n648.json) |
| [649](n649.svg) | [25.973662437040](certificates/n649.cert) | [25.974880942003](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n649.cert) | Improvement over public bound | [credits](certificates/n649.json) |
| [650](n650.svg) | [25.973786539735](certificates/n650.cert) | [25.974880942003](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n650.cert) | Improvement over public bound | [credits](certificates/n650.json) |
| [651](n651.svg) | [25.981695053458](certificates/n651.cert) | [25.981703321304](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n651.cert) | Improvement over public bound | [credits](certificates/n651.json) |
| [654](n654.svg) | [25.994801642508](certificates/n654.cert) | [25.994801642508](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n654.json) |
| [694](n694.svg) | [26.889879705795](certificates/n694.cert) | [26.898819144794](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n694.json) |
| [696](n696.svg) | [26.907009805052](certificates/n696.cert) | [26.946623458826](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n645.cert) | Improvement over public bound | [credits](certificates/n696.json) |
| [697](n697.svg) | [26.946234972260](certificates/n697.cert) | [26.946653181671](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n646.cert) | Improvement over public bound | [credits](certificates/n697.json) |
| [698](n698.svg) | [26.946926360996](certificates/n698.cert) | [26.946936912812](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n647.cert) | Improvement over public bound | [credits](certificates/n698.json) |
| [700](n700.svg) | [26.963723854128](certificates/n700.cert) | [26.963723854128](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n700.json) |
| [705](n705.svg) | [26.990375483504](certificates/n705.cert) | [26.990375578026](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n705.cert) | Improvement over public bound | [credits](certificates/n705.json) |
| [706](n706.svg) | [26.997916874564](certificates/n706.cert) | [26.997919093470](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n706.json) |
| [747](n747.svg) | [27.881306218096](certificates/n747.cert) | [27.884019388658](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n747.json) |
| [748](n748.svg) | [27.883920294486](certificates/n748.cert) | [27.884019388658](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n748.json) |
| [749](n749.svg) | [27.884019388642](certificates/n749.cert) | [27.884019388658](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n749.json) |
| [750](n750.svg) | [27.910827203971](certificates/n750.cert) | [27.911195756382](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n750.cert) | Improvement over public bound | [credits](certificates/n750.json) |
| [752](n752.svg) | [27.928790966656](certificates/n752.cert) | [27.931659253271](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n752.cert) | Improvement over public bound | [credits](certificates/n752.json) |
| [753](n753.svg) | [27.928790966656](certificates/n753.cert) | [27.932449886389](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n753.cert) | Improvement over public bound | [credits](certificates/n753.json) |
| [758](n758.svg) | [27.981168698642](certificates/n758.cert) | [27.982235537431](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n758.cert) | Improvement over public bound | [credits](certificates/n758.json) |
| [801](n801.svg) | [28.825019065210](certificates/n801.cert) | [28.825777528963](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n801.json) |
| [802](n802.svg) | [28.827332635379](certificates/n802.cert) | [28.827439471389](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n802.json) |
| [803](n803.svg) | [28.827585222354](certificates/n803.cert) | [28.827585222385](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n803.json) |
| [804](n804.svg) | [28.883977065812](certificates/n804.cert) | [28.884019388658](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n804.json) |
| [805](n805.svg) | [28.902673974145](certificates/n805.cert) | [28.902673974184](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n805.json) |
| [806](n806.svg) | [28.902673974145](certificates/n806.cert) | [28.902673974184](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n806.json) |
| [808](n808.svg) | [28.928790966656](certificates/n808.cert) | [28.931498747933](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n808.json) |
| [809](n809.svg) | [28.933268995267](certificates/n809.cert) | [28.933954128802](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n809.cert) | Improvement over public bound | [credits](certificates/n809.json) |
| [810](n810.svg) | [28.943689603564](certificates/n810.cert) | [28.951462957761](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n755.cert) | Improvement over public bound | [credits](certificates/n810.json) |
| [814](n814.svg) | [28.981344337792](certificates/n814.cert) | [28.981388113792](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n814.cert) | Improvement over public bound | [credits](certificates/n814.json) |
| [815](n815.svg) | [28.992261716527](certificates/n815.cert) | [28.992261716554](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n815.json) |
| [816](n816.svg) | [28.995928899209](certificates/n816.cert) | [28.995944538687](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n816.cert) | Improvement over public bound | [credits](certificates/n816.json) |
| [850](n850.svg) | [29.656854249499](certificates/n850.cert) | [29.656854249528](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n850.json) |
| [858](n858.svg) | [29.824728376140](certificates/n858.cert) | [29.825571500168](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n858.json) |
| [859](n859.svg) | [29.824728376140](certificates/n859.cert) | [29.825571500168](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n859.json) |
| [860](n860.svg) | [29.827585222354](certificates/n860.cert) | [29.827585222385](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n860.json) |
| [862](n862.svg) | [29.891065848639](certificates/n862.cert) | [29.899494936647](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n862.json) |
| [863](n863.svg) | [29.891065848639](certificates/n863.cert) | [29.902673974184](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n863.json) |
| [864](n864.svg) | [29.899838977702](certificates/n864.cert) | [29.924694842541](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n864.cert) | Improvement over public bound | [credits](certificates/n864.json) |
| [865](n865.svg) | [29.928790966656](certificates/n865.cert) | [29.931498747933](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n865.json) |
| [866](n866.svg) | [29.929509737782](certificates/n866.cert) | [29.933954024988](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n866.cert) | Improvement over public bound | [credits](certificates/n866.json) |
| [867](n867.svg) | [29.942070418091](certificates/n867.cert) | [29.942070418091](https://github.com/jlevy/squares/issues/715) | Published record held by this project | [credits](certificates/n867.json) |
| [868](n868.svg) | [29.973985523812](certificates/n868.cert) | [29.974216609256](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n868.cert) | Improvement over public bound | [credits](certificates/n868.json) |
| [871](n871.svg) | [29.980426400136](certificates/n871.cert) | [29.981222446775](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n871.cert) | Improvement over public bound | [credits](certificates/n871.json) |
| [873](n873.svg) | [29.992265777022](certificates/n873.cert) | [29.992265777039](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n873.json) |
| [909](n909.svg) | [30.656854249499](certificates/n909.cert) | [30.656854249528](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n909.json) |
| [914](n914.svg) | [30.778174593061](certificates/n914.cert) | [30.778174593089](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n914.json) |
| [917](n917.svg) | [30.824728376140](certificates/n917.cert) | [30.825571499902](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n917.json) |
| [918](n918.svg) | [30.824728376140](certificates/n918.cert) | [30.825571499902](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n918.json) |
| [919](n919.svg) | [30.827585222354](certificates/n919.cert) | [30.827585222385](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n919.json) |
| [922](n922.svg) | [30.891065848639](certificates/n922.cert) | [30.899494936660](https://github.com/jlevy/squares/issues/670) | Refinement of our published record | [credits](certificates/n922.json) |
| [923](n923.svg) | [30.899838977702](certificates/n923.cert) | [30.924694841577](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n923.cert) | Improvement over public bound | [credits](certificates/n923.json) |
| [924](n924.svg) | [30.928790966656](certificates/n924.cert) | [30.931498747933](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n924.json) |
| [925](n925.svg) | [30.929509737782](certificates/n925.cert) | [30.933954024988](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n866.cert) | Improvement over public bound | [credits](certificates/n925.json) |
| [926](n926.svg) | [30.941822318592](certificates/n926.cert) | [30.942070418091](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n926.json) |
| [927](n927.svg) | [30.968767627660](certificates/n927.cert) | [30.969190310883](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n927.cert) | Improvement over public bound | [credits](certificates/n927.json) |
| [970](n970.svg) | [31.656854249499](certificates/n970.cert) | [31.656854249528](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n970.json) |
| [975](n975.svg) | [31.778174593061](certificates/n975.cert) | [31.778174593089](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n975.json) |
| [976](n976.svg) | [31.778174593074](certificates/n976.cert) | [31.778174593090](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n976.json) |
| [978](n978.svg) | [31.823223304711](certificates/n978.cert) | [31.825090165859](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n978.json) |
| [979](n979.svg) | [31.823223304711](certificates/n979.cert) | [31.825090165859](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n979.json) |
| [980](n980.svg) | [31.827585222354](certificates/n980.cert) | [31.827585222385](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n980.json) |
| [983](n983.svg) | [31.891065843369](certificates/n983.cert) | [31.899494936650](https://github.com/jlevy/squares/pull/730) | Refinement of our published record | [credits](certificates/n983.json) |
| [984](n984.svg) | [31.895323373796](certificates/n984.cert) | [31.914115712696](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n984.cert) | Improvement over public bound | [credits](certificates/n984.json) |
| [985](n985.svg) | [31.920310216790](certificates/n985.cert) | [31.920310216821](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n985.json) |
| [986](n986.svg) | [31.920310216790](certificates/n986.cert) | [31.920310216821](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n986.json) |
| [987](n987.svg) | [31.941797078383](certificates/n987.cert) | [31.941797078452](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n987.json) |
| [988](n988.svg) | [31.949747468325](certificates/n988.cert) | [31.949747468406](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n988.json) |
| [992](n992.svg) | [31.977626910952](certificates/n992.cert) | [31.977647375503](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n992.cert) | Improvement over public bound | [credits](certificates/n992.json) |
| [1107](n1107.svg) | [33.823223304711](certificates/n1107.cert) | [33.825090165859](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n1107.json) |
| [1179](n1179.svg) | [34.895323373796](certificates/n1179.cert) | [34.914115712696](https://github.com/Mishapolk/square-packing-records/blob/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999/n984.cert) | Improvement over public bound | [credits](certificates/n1179.json) |
| [1251](n1251.svg) | [35.941774779809](certificates/n1251.cert) | [35.941797078452](https://github.com/jlevy/squares/issues/715) | Refinement of our published record | [credits](certificates/n1251.json) |
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

The [complete bound catalogue](certificates/best/README.md) covers n=1–10000 and retains 1086 finite source witnesses, including imported packings and classical constructions. Historical improvements and search seeds remain in the repository with their provenance.

<!-- /current-records -->
