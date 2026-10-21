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

The [publication-order and attribution review](RECORD_PROVENANCE.md) separates
construction, refinement and certificate credit, with
[source metadata for every count through 1024](record_provenance.json).
Tighter certification preserves the original arrangement credit. Imported and
superseded packings remain available in the full catalogue and search archives.

<!-- current-records -->

## Current records

Reviewed 2026-10-21: **263 counts** — strict improvements over the reviewed public bound.

Each n opens its packing. Certified sides and public comparisons are rounded upward to 12 decimal places. A difference within `1e-10` is treated as rounding; ties and worse bounds are excluded even when earlier record credit is retained. Construction, seed and certificate credits are linked for each packing.

| n | certified side s | reviewed public bound | standing | credits |
|---:|---:|---:|---|---|
| [328](n328.svg) | [18.614368938513](certificates/n328.cert) | [18.614376892295](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n328.json) |
| [335](n335.svg) | [18.822875655562](certificates/n335.cert) | [18.824123388479](https://github.com/jlevy/squares/blob/f8d547728c7761f78f29cf52c8974e1eba04ad4d/packing/frontier/STATUS.md) | Improvement over public bound | [credits](certificates/n335.json) |
| [336](n336.svg) | [18.825571499862](certificates/n336.cert) | [18.846667192844](https://github.com/jlevy/squares/pull/574) | Improvement over public bound | [credits](certificates/n336.json) |
| [337](n337.svg) | [18.858391767637](certificates/n337.cert) | [18.870013850405](https://github.com/jlevy/squares/issues/593) | Improvement over public bound | [credits](certificates/n337.json) |
| [338](n338.svg) | [18.906332809853](certificates/n338.cert) | [18.906436500552](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/resources/web/couzo-certificates-2026-10-11/source/certificates/n338.cert) | Improvement over public bound | [credits](certificates/n338.json) |
| [340](n340.svg) | [18.939649632892](certificates/n340.cert) | [18.939701150684](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/resources/web/couzo-certificates-2026-10-10/source/certificates/n340.cert) | Improvement over public bound | [credits](certificates/n340.json) |
| [341](n341.svg) | [18.951882408720](certificates/n341.cert) | [18.963433717492](https://github.com/jlevy/squares/pull/574) | Improvement over public bound | [credits](certificates/n341.json) |
| [343](n343.svg) | [18.977575126267](certificates/n343.cert) | [18.977682482405](https://github.com/evand/square-packing/blob/88385ab/search/packer/candidates/s343_sw.cert) | Improvement over public bound | [credits](certificates/n343.json) |
| [365](n365.svg) | [19.614368938513](certificates/n365.cert) | [19.614376892295](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n365.json) |
| [373](n373.svg) | [19.823062082838](certificates/n373.cert) | [19.846667192844](https://github.com/jlevy/squares/pull/574) | Improvement over public bound | [credits](certificates/n373.json) |
| [374](n374.svg) | [19.832356217033](certificates/n374.cert) | [19.870013850405](https://github.com/jlevy/squares/issues/593) | Improvement over public bound | [credits](certificates/n374.json) |
| [404](n404.svg) | [20.614368938513](certificates/n404.cert) | [20.614376892295](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n404.json) |
| [410](n410.svg) | [20.778174593076](certificates/n410.cert) | [20.822875655533](https://kingbird.myphotos.cc/packing/squares_in_squares.html) | Improvement over public bound | [credits](certificates/n410.json) |
| [413](n413.svg) | [20.831663365378](certificates/n413.cert) | [20.870013850405](https://github.com/jlevy/squares/issues/593) | Improvement over public bound | [credits](certificates/n413.json) |
| [417](n417.svg) | [20.933672777441](certificates/n417.cert) | [20.934672165249](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n417.json) |
| [454](n454.svg) | [21.828427124844](certificates/n454.cert) | [21.870013850405](https://github.com/jlevy/squares/issues/593) | Improvement over public bound | [credits](certificates/n454.json) |
| [455](n455.svg) | [21.848427413955](certificates/n455.cert) | [21.882183551471](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n455.json) |
| [456](n456.svg) | [21.881307463869](certificates/n456.cert) | [21.882183551471](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n456.json) |
| [458](n458.svg) | [21.903616797192](certificates/n458.cert) | [21.903778442820](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n458.json) |
| [459](n459.svg) | [21.937022304151](certificates/n459.cert) | [21.937227864890](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n459.json) |
| [461](n461.svg) | [21.964134608334](certificates/n461.cert) | [21.966193114415](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n461.json) |
| [463](n463.svg) | [21.971254044975](certificates/n463.cert) | [21.973675720478](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n463.json) |
| [490](n490.svg) | [22.656854249519](certificates/n490.cert) | 22.692388155426 | Improvement over public bound | [credits](certificates/n490.json) |
| [496](n496.svg) | [22.822875655559](certificates/n496.cert) | [22.822875659410](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n496.json) |
| [497](n497.svg) | [22.823102656285](certificates/n497.cert) | [22.823104027272](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n497.json) |
| [498](n498.svg) | [22.828427124827](certificates/n498.cert) | [22.882183551471](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n498.json) |
| [499](n499.svg) | [22.881306218323](certificates/n499.cert) | [22.882183551471](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n499.json) |
| [500](n500.svg) | [22.887841512273](certificates/n500.cert) | 22.899494936612 | Improvement over public bound | [credits](certificates/n500.json) |
| [501](n501.svg) | [22.887841512273](certificates/n501.cert) | [22.903778442820](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n501.json) |
| [502](n502.svg) | [22.933269925480](certificates/n502.cert) | [22.934445598629](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n502.json) |
| [503](n503.svg) | [22.943933771540](certificates/n503.cert) | [22.944667600408](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n503.json) |
| [504](n504.svg) | [22.961828398888](certificates/n504.cert) | [22.962118925864](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n504.json) |
| [505](n505.svg) | [22.964182800913](certificates/n505.cert) | [22.964253709990](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n505.json) |
| [506](n506.svg) | [22.971254044975](certificates/n506.cert) | [22.972145072004](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n506.json) |
| [509](n509.svg) | [22.993588501431](certificates/n509.cert) | [22.994328036438](https://github.com/jlevy/squares/issues/666) | Improvement over public bound | [credits](certificates/n509.json) |
| [535](n535.svg) | [23.656854249519](certificates/n535.cert) | [23.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n535.json) |
| [544](n544.svg) | [23.828427124775](certificates/n544.cert) | [23.882183551471](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n544.json) |
| [545](n545.svg) | [23.883414761903](certificates/n545.cert) | [23.889010439304](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n545.json) |
| [546](n546.svg) | [23.887841512273](certificates/n546.cert) | [23.889010439304](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n546.json) |
| [547](n547.svg) | [23.898819144794](certificates/n547.cert) | [23.906371163646](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n547.json) |
| [548](n548.svg) | [23.943933771540](certificates/n548.cert) | [23.944667600408](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n548.json) |
| [549](n549.svg) | [23.955501804754](certificates/n549.cert) | [23.956345132949](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n549.json) |
| [550](n550.svg) | [23.960681444798](certificates/n550.cert) | [23.961058656836](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n550.json) |
| [553](n553.svg) | [23.979452392567](certificates/n553.cert) | [23.979786600216](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n553.json) |
| [554](n554.svg) | [23.986307325908](certificates/n554.cert) | [23.986315054038](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n554.json) |
| [582](n582.svg) | [24.656854249519](certificates/n582.cert) | [24.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n582.json) |
| [584](n584.svg) | [24.677669529693](certificates/n584.cert) | 24.707106781187 | Improvement over public bound | [credits](certificates/n584.json) |
| [591](n591.svg) | [24.828427124775](certificates/n591.cert) | [24.882183551471](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n591.json) |
| [592](n592.svg) | [24.883414761903](certificates/n592.cert) | [24.888988759404](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n592.json) |
| [593](n593.svg) | [24.887841512273](certificates/n593.cert) | [24.888988761769](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n593.json) |
| [594](n594.svg) | [24.898819144794](certificates/n594.cert) | [24.906371163646](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n594.json) |
| [595](n595.svg) | [24.943933771540](certificates/n595.cert) | [24.944667600408](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n595.json) |
| [596](n596.svg) | [24.949747468335](certificates/n596.cert) | [24.956345132949](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n596.json) |
| [597](n597.svg) | [24.950690418637](certificates/n597.cert) | [24.958141573308](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n597.json) |
| [598](n598.svg) | [24.954250129268](certificates/n598.cert) | [24.958220677836](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n598.json) |
| [599](n599.svg) | [24.959619887409](certificates/n599.cert) | [24.962832858736](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n599.json) |
| [600](n600.svg) | [24.978172747238](certificates/n600.cert) | [24.979786600216](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n600.json) |
| [601](n601.svg) | [24.986189080604](certificates/n601.cert) | [24.986315054038](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n601.json) |
| [602](n602.svg) | [24.988237878425](certificates/n602.cert) | [24.990355569380](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n602.json) |
| [631](n631.svg) | [25.656854249519](certificates/n631.cert) | [25.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n631.json) |
| [633](n633.svg) | [25.677669529693](certificates/n633.cert) | 25.707106781187 | Improvement over public bound | [credits](certificates/n633.json) |
| [637](n637.svg) | [25.778174593082](certificates/n637.cert) | 25.813708498985 | Improvement over public bound | [credits](certificates/n637.json) |
| [640](n640.svg) | [25.828427124775](certificates/n640.cert) | [25.881306220594](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n640.json) |
| [643](n643.svg) | [25.898819144794](certificates/n643.cert) | [25.906371163646](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n643.json) |
| [644](n644.svg) | [25.899494936642](certificates/n644.cert) | [25.944667600408](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n644.json) |
| [645](n645.svg) | [25.946937290069](certificates/n645.cert) | [25.949897942499](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n645.json) |
| [646](n646.svg) | [25.946937290069](certificates/n646.cert) | [25.949897942499](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n646.json) |
| [647](n647.svg) | [25.946937290069](certificates/n647.cert) | [25.949897942499](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n647.json) |
| [648](n648.svg) | [25.959619886978](certificates/n648.cert) | [25.961052856925](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n648.json) |
| [651](n651.svg) | [25.981928099991](certificates/n651.cert) | [25.982878838107](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n651.json) |
| [652](n652.svg) | [25.990044325432](certificates/n652.cert) | [25.990355569380](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n652.json) |
| [653](n653.svg) | [25.992652721826](certificates/n653.cert) | [25.994414202392](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n653.json) |
| [654](n654.svg) | [25.994801642508](certificates/n654.cert) | [25.994867334133](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n654.json) |
| [682](n682.svg) | [26.656854249519](certificates/n682.cert) | [26.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n682.json) |
| [684](n684.svg) | [26.677669529693](certificates/n684.cert) | 26.707106781187 | Improvement over public bound | [credits](certificates/n684.json) |
| [689](n689.svg) | [26.778174593084](certificates/n689.cert) | 26.813708498985 | Improvement over public bound | [credits](certificates/n689.json) |
| [691](n691.svg) | [26.828427124775](certificates/n691.cert) | [26.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n691.json) |
| [692](n692.svg) | [26.828427124777](certificates/n692.cert) | [26.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n692.json) |
| [694](n694.svg) | [26.898819144794](certificates/n694.cert) | [26.906371163646](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n694.json) |
| [695](n695.svg) | [26.899494936642](certificates/n695.cert) | [26.944667600408](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n695.json) |
| [696](n696.svg) | [26.946937290069](certificates/n696.cert) | [26.949897942499](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n696.json) |
| [697](n697.svg) | [26.946937290069](certificates/n697.cert) | [26.949897942499](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n697.json) |
| [698](n698.svg) | [26.946937290069](certificates/n698.cert) | [26.949897942499](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n698.json) |
| [699](n699.svg) | [26.949747468415](certificates/n699.cert) | [26.961052856925](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n699.json) |
| [700](n700.svg) | [26.963723854128](certificates/n700.cert) | [26.963730153904](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n700.json) |
| [702](n702.svg) | [26.976012028499](certificates/n702.cert) | [26.976692903976](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n702.json) |
| [705](n705.svg) | [26.990419622637](certificates/n705.cert) | [26.990473400223](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n705.json) |
| [735](n735.svg) | [27.656854249519](certificates/n735.cert) | [27.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n735.json) |
| [736](n736.svg) | [27.656854249525](certificates/n736.cert) | [27.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n736.json) |
| [737](n737.svg) | [27.677669529693](certificates/n737.cert) | 27.707106781187 | Improvement over public bound | [credits](certificates/n737.json) |
| [742](n742.svg) | [27.778174593084](certificates/n742.cert) | 27.813708498985 | Improvement over public bound | [credits](certificates/n742.json) |
| [743](n743.svg) | [27.798989873256](certificates/n743.cert) | 27.813708498985 | Improvement over public bound | [credits](certificates/n743.json) |
| [744](n744.svg) | [27.798989873256](certificates/n744.cert) | [27.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n744.json) |
| [745](n745.svg) | [27.828427124777](certificates/n745.cert) | [27.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n745.json) |
| [746](n746.svg) | [27.828427124795](certificates/n746.cert) | [27.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n746.json) |
| [747](n747.svg) | [27.884019388658](certificates/n747.cert) | [27.906371163646](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n747.json) |
| [748](n748.svg) | [27.884019388658](certificates/n748.cert) | [27.911194713730](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n748.json) |
| [749](n749.svg) | [27.884019388658](certificates/n749.cert) | [27.911194713730](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n749.json) |
| [750](n750.svg) | [27.911200800711](certificates/n750.cert) | [27.927909095101](https://github.com/jlevy/squares/issues/672) | Improvement over public bound | [credits](certificates/n750.json) |
| [751](n751.svg) | [27.914175785603](certificates/n751.cert) | [27.932448900769](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n751.json) |
| [752](n752.svg) | [27.932396768486](certificates/n752.cert) | [27.932449886404](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n752.json) |
| [756](n756.svg) | [27.976782251658](certificates/n756.cert) | [27.976914446464](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n756.json) |
| [758](n758.svg) | [27.983731022945](certificates/n758.cert) | [27.984283608421](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n758.json) |
| [790](n790.svg) | [28.656854249519](certificates/n790.cert) | [28.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n790.json) |
| [791](n791.svg) | [28.656854249525](certificates/n791.cert) | [28.677669529701](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n791.json) |
| [792](n792.svg) | [28.656854249526](certificates/n792.cert) | 28.707106781187 | Improvement over public bound | [credits](certificates/n792.json) |
| [797](n797.svg) | [28.778174593084](certificates/n797.cert) | 28.813708498985 | Improvement over public bound | [credits](certificates/n797.json) |
| [798](n798.svg) | [28.798989873256](certificates/n798.cert) | 28.813708498985 | Improvement over public bound | [credits](certificates/n798.json) |
| [799](n799.svg) | [28.798989873256](certificates/n799.cert) | [28.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n799.json) |
| [800](n800.svg) | [28.798989873257](certificates/n800.cert) | [28.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n800.json) |
| [801](n801.svg) | [28.825777528963](certificates/n801.cert) | [28.881306218365](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n801.json) |
| [802](n802.svg) | [28.827439471389](certificates/n802.cert) | [28.906371163646](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n802.json) |
| [803](n803.svg) | [28.827585222385](certificates/n803.cert) | [28.909246527138](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n803.json) |
| [804](n804.svg) | [28.884019388658](certificates/n804.cert) | [28.909246527138](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n804.json) |
| [805](n805.svg) | [28.902673974184](certificates/n805.cert) | [28.909665866810](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n805.json) |
| [806](n806.svg) | [28.902673974184](certificates/n806.cert) | [28.919759255285](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n806.json) |
| [807](n807.svg) | [28.924694876402](certificates/n807.cert) | [28.924702911083](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n807.json) |
| [808](n808.svg) | [28.931498747933](certificates/n808.cert) | [28.932449886404](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n808.json) |
| [809](n809.svg) | [28.933954694456](certificates/n809.cert) | [28.937423314202](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n809.json) |
| [813](n813.svg) | [28.979120019579](certificates/n813.cert) | [28.981594177156](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n813.json) |
| [814](n814.svg) | [28.981388189193](certificates/n814.cert) | [28.981594177156](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n814.json) |
| [815](n815.svg) | [28.992261716554](certificates/n815.cert) | [28.992923233307](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n815.json) |
| [850](n850.svg) | [29.656854249528](certificates/n850.cert) | 29.707106781187 | Improvement over public bound | [credits](certificates/n850.json) |
| [854](n854.svg) | [29.778174593084](certificates/n854.cert) | 29.813708498985 | Improvement over public bound | [credits](certificates/n854.json) |
| [855](n855.svg) | [29.798989873256](certificates/n855.cert) | 29.813708498985 | Improvement over public bound | [credits](certificates/n855.json) |
| [856](n856.svg) | [29.798989873256](certificates/n856.cert) | 29.849242404918 | Improvement over public bound | [credits](certificates/n856.json) |
| [857](n857.svg) | [29.798989873257](certificates/n857.cert) | 29.849242404918 | Improvement over public bound | [credits](certificates/n857.json) |
| [858](n858.svg) | [29.825571500168](certificates/n858.cert) | 29.849242404918 | Improvement over public bound | [credits](certificates/n858.json) |
| [859](n859.svg) | [29.825571500168](certificates/n859.cert) | 29.849242404918 | Improvement over public bound | [credits](certificates/n859.json) |
| [860](n860.svg) | [29.827585222385](certificates/n860.cert) | 29.849242404918 | Improvement over public bound | [credits](certificates/n860.json) |
| [862](n862.svg) | [29.899494936647](certificates/n862.cert) | [29.909665866810](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n862.json) |
| [863](n863.svg) | [29.902673974184](certificates/n863.cert) | [29.916419307447](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n863.json) |
| [864](n864.svg) | [29.924694876402](certificates/n864.cert) | [29.924702911083](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n864.json) |
| [865](n865.svg) | [29.931498747933](certificates/n865.cert) | [29.932449886402](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n865.json) |
| [866](n866.svg) | [29.933954694456](certificates/n866.cert) | [29.935764472087](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n866.json) |
| [867](n867.svg) | [29.942070418091](certificates/n867.cert) | [29.949688481977](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n867.json) |
| [868](n868.svg) | [29.974553547719](certificates/n868.cert) | [29.974562439898](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n868.json) |
| [869](n869.svg) | [29.974935743865](certificates/n869.cert) | [29.974936836674](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n869.json) |
| [870](n870.svg) | [29.979120019579](certificates/n870.cert) | [29.981594177156](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n870.json) |
| [871](n871.svg) | [29.981295638373](certificates/n871.cert) | [29.981594177156](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n871.json) |
| [872](n872.svg) | [29.992261716554](certificates/n872.cert) | [29.992623086291](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n872.json) |
| [873](n873.svg) | [29.992265777039](certificates/n873.cert) | [29.992623086291](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n873.json) |
| [909](n909.svg) | [30.656854249528](certificates/n909.cert) | 30.707106781187 | Improvement over public bound | [credits](certificates/n909.json) |
| [913](n913.svg) | [30.778174593084](certificates/n913.cert) | 30.813708498985 | Improvement over public bound | [credits](certificates/n913.json) |
| [914](n914.svg) | [30.778174593089](certificates/n914.cert) | 30.813708498985 | Improvement over public bound | [credits](certificates/n914.json) |
| [915](n915.svg) | [30.798989873256](certificates/n915.cert) | [30.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n915.json) |
| [916](n916.svg) | [30.798989873257](certificates/n916.cert) | [30.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n916.json) |
| [917](n917.svg) | [30.825571499902](certificates/n917.cert) | [30.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n917.json) |
| [918](n918.svg) | [30.825571499902](certificates/n918.cert) | [30.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n918.json) |
| [919](n919.svg) | [30.827585222385](certificates/n919.cert) | [30.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n919.json) |
| [923](n923.svg) | [30.924694876402](certificates/n923.cert) | [30.924702911083](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n923.json) |
| [924](n924.svg) | [30.931498747933](certificates/n924.cert) | [30.932449886402](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n924.json) |
| [925](n925.svg) | [30.933954694456](certificates/n925.cert) | [30.935764472087](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n925.json) |
| [926](n926.svg) | [30.942070418091](certificates/n926.cert) | [30.945612117331](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n926.json) |
| [927](n927.svg) | [30.969443226806](certificates/n927.cert) | [30.969979227502](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n927.json) |
| [928](n928.svg) | [30.974935654060](certificates/n928.cert) | [30.974936836674](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n928.json) |
| [931](n931.svg) | [30.989934444611](certificates/n931.cert) | [30.989934734721](https://github.com/jlevy/squares/issues/675) | Improvement over public bound | [credits](certificates/n931.json) |
| [932](n932.svg) | [30.992265777039](certificates/n932.cert) | [30.992623086291](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n932.json) |
| [970](n970.svg) | [31.656854249528](certificates/n970.cert) | 31.707106781187 | Improvement over public bound | [credits](certificates/n970.json) |
| [975](n975.svg) | [31.778174593089](certificates/n975.cert) | 31.813708498985 | Improvement over public bound | [credits](certificates/n975.json) |
| [976](n976.svg) | [31.778174593090](certificates/n976.cert) | [31.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n976.json) |
| [977](n977.svg) | [31.798989873257](certificates/n977.cert) | [31.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n977.json) |
| [978](n978.svg) | [31.825090165859](certificates/n978.cert) | [31.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n978.json) |
| [979](n979.svg) | [31.825090165859](certificates/n979.cert) | [31.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n979.json) |
| [980](n980.svg) | [31.827585222385](certificates/n980.cert) | [31.844931419278](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n980.json) |
| [985](n985.svg) | [31.920310216821](certificates/n985.cert) | [31.932449886402](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n985.json) |
| [986](n986.svg) | [31.920310216821](certificates/n986.cert) | [31.935764472087](https://github.com/jlevy/squares/issues/670) | Improvement over public bound | [credits](certificates/n986.json) |
| [987](n987.svg) | [31.941797078452](certificates/n987.cert) | [31.944662519483](https://github.com/jlevy/squares/issues/678) | Improvement over public bound | [credits](certificates/n987.json) |
| [988](n988.svg) | [31.949747468406](certificates/n988.cert) | [31.969979227502](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n988.json) |
| [989](n989.svg) | [31.974181306003](certificates/n989.cert) | [31.974936836674](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n989.json) |
| [994](n994.svg) | [31.992271544010](certificates/n994.cert) | [31.992883399226](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n994.json) |
| [995](n995.svg) | [31.993696413074](certificates/n995.cert) | [31.994174058157](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n995.json) |
| [996](n996.svg) | [31.994135336337](certificates/n996.cert) | [31.994174058157](https://github.com/jlevy/squares/issues/686) | Improvement over public bound | [credits](certificates/n996.json) |
| [1061](n1061.svg) | [32.995954738136](certificates/n1061.cert) | 32.996048342114 | Improvement over public bound | [credits](certificates/n1061.json) |
| [1263](n1263.svg) | [35.993549626549](certificates/n1263.cert) | 35.996046404219 | Improvement over public bound | [credits](certificates/n1263.json) |
| [1266](n1266.svg) | [35.996046403807](certificates/n1266.cert) | [35.996046404219](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/19f7412d7f33ff430b9bfa2f0b4482b711a97526/square-packing-above-324/n1266.cert) | Improvement over public bound | [credits](certificates/n1266.json) |
| [1335](n1335.svg) | [36.990072025463](certificates/n1335.cert) | [36.995489275431](https://github.com/TheSnakeFang/squarepack-certs/blob/9ffba0f3a84b38f0c92790c1d3089f979ef53f0b/composites/n037_j3_1335.cert) | Improvement over public bound | [credits](certificates/n1335.json) |
| [1339](n1339.svg) | [36.997865205268](certificates/n1339.cert) | [36.997865207179](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/19f7412d7f33ff430b9bfa2f0b4482b711a97526/square-packing-above-324/n1339.cert) | Improvement over public bound | [credits](certificates/n1339.json) |
| [1413](n1413.svg) | [37.999315487115](certificates/n1413.cert) | 37.999463832123 | Improvement over public bound | [credits](certificates/n1413.json) |
| [1489](n1489.svg) | [38.997599735618](certificates/n1489.cert) | 38.997600184483 | Improvement over public bound | [credits](certificates/n1489.json) |
| [1564](n1564.svg) | [39.992727809619](certificates/n1564.cert) | 39.997600184483 | Improvement over public bound | [credits](certificates/n1564.json) |
| [1568](n1568.svg) | [39.999336624698](certificates/n1568.cert) | [39.999336626159](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/19f7412d7f33ff430b9bfa2f0b4482b711a97526/square-packing-above-324/n1568.cert) | Improvement over public bound | [credits](certificates/n1568.json) |
| [1644](n1644.svg) | [40.994328036200](certificates/n1644.cert) | 40.997600184483 | Improvement over public bound | [credits](certificates/n1644.json) |
| [1648](n1648.svg) | [40.999321109325](certificates/n1648.cert) | 41.000000000000 | Improvement over public bound | [credits](certificates/n1648.json) |
| [1727](n1727.svg) | [41.999256219691](certificates/n1727.cert) | 41.999336626159 | Improvement over public bound | [credits](certificates/n1727.json) |
| [1729](n1729.svg) | [41.999321109325](certificates/n1729.cert) | 42.000000000000 | Improvement over public bound | [credits](certificates/n1729.json) |
| [1811](n1811.svg) | [42.997550241724](certificates/n1811.cert) | [42.999336626159](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/19f7412d7f33ff430b9bfa2f0b4482b711a97526/square-packing-above-324/n1568.cert) | Improvement over public bound | [credits](certificates/n1811.json) |
| [1812](n1812.svg) | [42.997600183876](certificates/n1812.cert) | 43.000000000000 | Improvement over public bound | [credits](certificates/n1812.json) |
| [1897](n1897.svg) | [43.994328036204](certificates/n1897.cert) | 44.000000000000 | Improvement over public bound | [credits](certificates/n1897.json) |
| [1899](n1899.svg) | [43.999336623227](certificates/n1899.cert) | 44.000000000000 | Improvement over public bound | [credits](certificates/n1899.json) |
| [1986](n1986.svg) | [44.997600183879](certificates/n1986.cert) | 45.000000000000 | Improvement over public bound | [credits](certificates/n1986.json) |
| [2043](n2043.svg) | [45.695704158830](certificates/n2043.cert) | [45.696427839410](https://kingbird.myphotos.cc/packing/squares_in_squares.html) | Improvement over public bound | [credits](certificates/n2043.json) |
| [2076](n2076.svg) | [45.997550240009](certificates/n2076.cert) | 46.000000000000 | Improvement over public bound | [credits](certificates/n2076.json) |
| [2168](n2168.svg) | [46.994867334396](certificates/n2168.cert) | 47.000000000000 | Improvement over public bound | [credits](certificates/n2168.json) |
| [2262](n2262.svg) | [47.997550817674](certificates/n2262.cert) | 48.000000000000 | Improvement over public bound | [credits](certificates/n2262.json) |
| [2263](n2263.svg) | [47.999256231755](certificates/n2263.cert) | 48.000000000000 | Improvement over public bound | [credits](certificates/n2263.json) |
| [2358](n2358.svg) | [48.995949339886](certificates/n2358.cert) | 49.000000000000 | Improvement over public bound | [credits](certificates/n2358.json) |
| [2359](n2359.svg) | [48.997550269630](certificates/n2359.cert) | 49.000000000000 | Improvement over public bound | [credits](certificates/n2359.json) |
| [2457](n2457.svg) | [49.996875920562](certificates/n2457.cert) | 50.000000000000 | Improvement over public bound | [credits](certificates/n2457.json) |
| [2557](n2557.svg) | [50.996974282121](certificates/n2557.cert) | 51.000000000000 | Improvement over public bound | [credits](certificates/n2557.json) |
| [2659](n2659.svg) | [51.994174058427](certificates/n2659.cert) | 52.000000000000 | Improvement over public bound | [credits](certificates/n2659.json) |
| [2764](n2764.svg) | [52.996875920566](certificates/n2764.cert) | 53.000000000000 | Improvement over public bound | [credits](certificates/n2764.json) |
| [2870](n2870.svg) | [53.997865205474](certificates/n2870.cert) | 54.000000000000 | Improvement over public bound | [credits](certificates/n2870.json) |
| [2978](n2978.svg) | [54.997865205476](certificates/n2978.cert) | 55.000000000000 | Improvement over public bound | [credits](certificates/n2978.json) |
| [3088](n3088.svg) | [55.997600152266](certificates/n3088.cert) | 56.000000000000 | Improvement over public bound | [credits](certificates/n3088.json) |
| [3089](n3089.svg) | [55.999336626356](certificates/n3089.cert) | 56.000000000000 | Improvement over public bound | [credits](certificates/n3089.json) |
| [3201](n3201.svg) | [56.999336625014](certificates/n3201.cert) | 57.000000000000 | Improvement over public bound | [credits](certificates/n3201.json) |
| [3315](n3315.svg) | [57.997865205479](certificates/n3315.cert) | 58.000000000000 | Improvement over public bound | [credits](certificates/n3315.json) |
| [3431](n3431.svg) | [58.999336623410](certificates/n3431.cert) | 59.000000000000 | Improvement over public bound | [credits](certificates/n3431.json) |
| [3549](n3549.svg) | [59.997600152271](certificates/n3549.cert) | 60.000000000000 | Improvement over public bound | [credits](certificates/n3549.json) |
| [3669](n3669.svg) | [60.999336622351](certificates/n3669.cert) | 61.000000000000 | Improvement over public bound | [credits](certificates/n3669.json) |
| [3670](n3670.svg) | [60.999336626362](certificates/n3670.cert) | 61.000000000000 | Improvement over public bound | [credits](certificates/n3670.json) |
| [3791](n3791.svg) | [61.999336625020](certificates/n3791.cert) | 62.000000000000 | Improvement over public bound | [credits](certificates/n3791.json) |
| [3792](n3792.svg) | [61.999336625020](certificates/n3792.cert) | 62.000000000000 | Improvement over public bound | [credits](certificates/n3792.json) |
| [3914](n3914.svg) | [62.999336625020](certificates/n3914.cert) | 63.000000000000 | Improvement over public bound | [credits](certificates/n3914.json) |
| [3915](n3915.svg) | [62.999336625020](certificates/n3915.cert) | 63.000000000000 | Improvement over public bound | [credits](certificates/n3915.json) |
| [4040](n4040.svg) | [63.997600184152](certificates/n4040.cert) | 64.000000000000 | Improvement over public bound | [credits](certificates/n4040.json) |
| [4168](n4168.svg) | [64.999256232549](certificates/n4168.cert) | 65.000000000000 | Improvement over public bound | [credits](certificates/n4168.json) |
| [4169](n4169.svg) | [64.999336626619](certificates/n4169.cert) | 65.000000000000 | Improvement over public bound | [credits](certificates/n4169.json) |
| [4298](n4298.svg) | [65.997550817909](certificates/n4298.cert) | 66.000000000000 | Improvement over public bound | [credits](certificates/n4298.json) |
| [4430](n4430.svg) | [66.997550243025](certificates/n4430.cert) | 67.000000000000 | Improvement over public bound | [credits](certificates/n4430.json) |
| [4564](n4564.svg) | [67.994867334626](certificates/n4564.cert) | 68.000000000000 | Improvement over public bound | [credits](certificates/n4564.json) |
| [4701](n4701.svg) | [68.999256219267](certificates/n4701.cert) | 69.000000000000 | Improvement over public bound | [credits](certificates/n4701.json) |
| [4839](n4839.svg) | [69.997550252215](certificates/n4839.cert) | 70.000000000000 | Improvement over public bound | [credits](certificates/n4839.json) |
| [4979](n4979.svg) | [70.996875920791](certificates/n4979.cert) | 71.000000000000 | Improvement over public bound | [credits](certificates/n4979.json) |
| [5121](n5121.svg) | [71.996974282350](certificates/n5121.cert) | 72.000000000000 | Improvement over public bound | [credits](certificates/n5121.json) |
| [5122](n5122.svg) | [71.999336626575](certificates/n5122.cert) | 72.000000000000 | Improvement over public bound | [credits](certificates/n5122.json) |
| [5266](n5266.svg) | [72.999336625233](certificates/n5266.cert) | 73.000000000000 | Improvement over public bound | [credits](certificates/n5266.json) |
| [5412](n5412.svg) | [73.996875920795](certificates/n5412.cert) | 74.000000000000 | Improvement over public bound | [credits](certificates/n5412.json) |
| [5560](n5560.svg) | [74.997865205700](certificates/n5560.cert) | 75.000000000000 | Improvement over public bound | [credits](certificates/n5560.json) |
| [5710](n5710.svg) | [75.997865205701](certificates/n5710.cert) | 76.000000000000 | Improvement over public bound | [credits](certificates/n5710.json) |
| [5862](n5862.svg) | [76.997600152491](certificates/n5862.cert) | 77.000000000000 | Improvement over public bound | [credits](certificates/n5862.json) |
| [5863](n5863.svg) | [76.999336626581](certificates/n5863.cert) | 77.000000000000 | Improvement over public bound | [credits](certificates/n5863.json) |
| [6017](n6017.svg) | [77.999336625239](certificates/n6017.cert) | 78.000000000000 | Improvement over public bound | [credits](certificates/n6017.json) |
| [6173](n6173.svg) | [78.997865205705](certificates/n6173.cert) | 79.000000000000 | Improvement over public bound | [credits](certificates/n6173.json) |
| [6331](n6331.svg) | [79.999336623635](certificates/n6331.cert) | 80.000000000000 | Improvement over public bound | [credits](certificates/n6331.json) |
| [6491](n6491.svg) | [80.997600152496](certificates/n6491.cert) | 81.000000000000 | Improvement over public bound | [credits](certificates/n6491.json) |
| [6653](n6653.svg) | [81.999336622664](certificates/n6653.cert) | 82.000000000000 | Improvement over public bound | [credits](certificates/n6653.json) |
| [6654](n6654.svg) | [81.999336626587](certificates/n6654.cert) | 82.000000000000 | Improvement over public bound | [credits](certificates/n6654.json) |
| [6817](n6817.svg) | [82.999336625245](certificates/n6817.cert) | 83.000000000000 | Improvement over public bound | [credits](certificates/n6817.json) |
| [6818](n6818.svg) | [82.999336625245](certificates/n6818.cert) | 83.000000000000 | Improvement over public bound | [credits](certificates/n6818.json) |
| [6982](n6982.svg) | [83.999336625245](certificates/n6982.cert) | 84.000000000000 | Improvement over public bound | [credits](certificates/n6982.json) |
| [6983](n6983.svg) | [83.999336625245](certificates/n6983.cert) | 84.000000000000 | Improvement over public bound | [credits](certificates/n6983.json) |
| [7150](n7150.svg) | [84.997600184377](certificates/n7150.cert) | 85.000000000000 | Improvement over public bound | [credits](certificates/n7150.json) |
| [7320](n7320.svg) | [85.999256308750](certificates/n7320.cert) | 86.000000000000 | Improvement over public bound | [credits](certificates/n7320.json) |
| [7321](n7321.svg) | [85.999336626844](certificates/n7321.cert) | 86.000000000000 | Improvement over public bound | [credits](certificates/n7321.json) |
| [7492](n7492.svg) | [86.997550817938](certificates/n7492.cert) | 87.000000000000 | Improvement over public bound | [credits](certificates/n7492.json) |
| [7666](n7666.svg) | [87.997865205915](certificates/n7666.cert) | 88.000000000000 | Improvement over public bound | [credits](certificates/n7666.json) |
| [7667](n7667.svg) | [87.999336626795](certificates/n7667.cert) | 88.000000000000 | Improvement over public bound | [credits](certificates/n7667.json) |
| [7843](n7843.svg) | [88.999336625453](certificates/n7843.cert) | 89.000000000000 | Improvement over public bound | [credits](certificates/n7843.json) |
| [8021](n8021.svg) | [89.999256219591](certificates/n8021.cert) | 90.000000000000 | Improvement over public bound | [credits](certificates/n8021.json) |
| [8201](n8201.svg) | [90.997550817744](certificates/n8201.cert) | 91.000000000000 | Improvement over public bound | [credits](certificates/n8201.json) |
| [8383](n8383.svg) | [91.996875921021](certificates/n8383.cert) | 92.000000000000 | Improvement over public bound | [credits](certificates/n8383.json) |
| [8567](n8567.svg) | [92.997865205921](certificates/n8567.cert) | 93.000000000000 | Improvement over public bound | [credits](certificates/n8567.json) |
| [8568](n8568.svg) | [92.999336626801](certificates/n8568.cert) | 93.000000000000 | Improvement over public bound | [credits](certificates/n8568.json) |
| [8754](n8754.svg) | [93.999336625459](certificates/n8754.cert) | 94.000000000000 | Improvement over public bound | [credits](certificates/n8754.json) |
| [8942](n8942.svg) | [94.996875921025](certificates/n8942.cert) | 95.000000000000 | Improvement over public bound | [credits](certificates/n8942.json) |
| [9132](n9132.svg) | [95.997865205925](certificates/n9132.cert) | 96.000000000000 | Improvement over public bound | [credits](certificates/n9132.json) |
| [9324](n9324.svg) | [96.997865205926](certificates/n9324.cert) | 97.000000000000 | Improvement over public bound | [credits](certificates/n9324.json) |
| [9518](n9518.svg) | [97.997600152717](certificates/n9518.cert) | 98.000000000000 | Improvement over public bound | [credits](certificates/n9518.json) |
| [9519](n9519.svg) | [97.999336626807](certificates/n9519.cert) | 98.000000000000 | Improvement over public bound | [credits](certificates/n9519.json) |
| [9715](n9715.svg) | [98.999336625465](certificates/n9715.cert) | 99.000000000000 | Improvement over public bound | [credits](certificates/n9715.json) |
| [9913](n9913.svg) | [99.997865205930](certificates/n9913.cert) | 100.000000000000 | Improvement over public bound | [credits](certificates/n9913.json) |

The [complete bound catalogue](certificates/best/README.md) covers n=1–10000 and retains 857 finite source witnesses, including imported packings and classical constructions. Historical improvements and search seeds remain in the repository with their provenance.

<!-- /current-records -->
