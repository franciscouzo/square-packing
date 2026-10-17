# Verified upper-bound witnesses

The complete index covers every n=1..1024. Exact certificate headers and algebraic proofs are authoritative; displayed sides are rounded upward to 12 decimal places.

This directory retains **532 finite rational witnesses**. Original construction and certificate credits, source submissions, parent witnesses and byte hashes are in [manifest.json](manifest.json). The machine, repository, issue and PR review is recorded in [bound_sources.json](../../bound_sources.json).

Replay the finite witnesses from the repository root using Python 3 and its standard library:

```sh
python3 verify_bound_certificate.py certificates/best/*.cert
```

The default contract is containment in a closed square with disjoint square interiors. `--strict` also requires open-container containment and disjoint closed squares. Both verdicts are retained. New or changed witness bytes were checked using the jlevy/squares exact rational corner verifier and the separate centre/projection verifier in this repository. Earlier receipts are reused only for identical certificate bytes. Both implementations share the rational half-angle representation, separating-axis geometry and conservative spatial prefilters.

The complete index also preserves exact Göbel square/strip and Friedman off-centre bounds, their repeated L borders, and deletion. These established constructions retain their original credits. A border extends (m,s) to (m+2 floor(s)+1,s+1). The integer grid at n=1024 has exact side 32; area proves optimality there.

| n / certificate | Certified upper, rounded up | Certificate provider / source credit |
|---:|---:|---|
| [5](n5.cert) | 2.707106781187 | PingYou Ltd (BuddenPing) |
| [10](n10.cert) | 3.707106781187 | PingYou Ltd (BuddenPing) |
| [11](n11.cert) | 3.877083590023 | PingYou Ltd (BuddenPing) |
| [17](n17.cert) | 4.675530093605 | PingYou Ltd (BuddenPing) |
| [18](n18.cert) | 4.822875655533 | PingYou Ltd (BuddenPing) |
| [19](n19.cert) | 4.885618083165 | PingYou Ltd (BuddenPing) |
| [26](n26.cert) | 5.621320343560 | PingYou Ltd (BuddenPing) |
| [27](n27.cert) | 5.707106781187 | PingYou Ltd (BuddenPing) |
| [28](n28.cert) | 5.824444616675 | PingYou Ltd (BuddenPing) |
| [29](n29.cert) | 5.933833462677 | Thomas Schadt and David Ellsworth; exact certificate refinement by PingYou Ltd |
| [37](n37.cert) | 6.598619609245 | PingYou Ltd (BuddenPing) |
| [38](n38.cert) | 6.707106781187 | PingYou Ltd (BuddenPing) |
| [39](n39.cert) | 6.810722083069 | PingYou Ltd (BuddenPing) |
| [40](n40.cert) | 6.828427124747 | PingYou Ltd (BuddenPing) |
| [41](n41.cert) | 6.926693094469 | PingYou Ltd (BuddenPing) |
| [50](n50.cert) | 7.571428571429 | PingYou Ltd (BuddenPing) |
| [51](n51.cert) | 7.690355937289 | PingYou Ltd (BuddenPing) |
| [52](n52.cert) | 7.707106781187 | PingYou Ltd (BuddenPing) |
| [53](n53.cert) | 7.822875655533 | PingYou Ltd (BuddenPing) |
| [54](n54.cert) | 7.846667192844 | PingYou Ltd (BuddenPing) |
| [55](n55.cert) | 7.945771007504 | PingYou Ltd (BuddenPing) |
| [65](n65.cert) | 8.535533905933 | PingYou Ltd (BuddenPing) |
| [66](n66.cert) | 8.656854249493 | PingYou Ltd (BuddenPing) |
| [67](n67.cert) | 8.707106781187 | PingYou Ltd (BuddenPing) |
| [68](n68.cert) | 8.798795237219 | PingYou Ltd (BuddenPing) |
| [69](n69.cert) | 8.827194655730 | PingYou Ltd (BuddenPing) |
| [70](n70.cert) | 8.880960371556 | PingYou Ltd (BuddenPing) |
| [71](n71.cert) | 8.944071557571 | PingYou Ltd (BuddenPing) |
| [82](n82.cert) | 9.535533905933 | PingYou Ltd (BuddenPing) |
| [83](n83.cert) | 9.634757648632 | PingYou Ltd (BuddenPing) |
| [84](n84.cert) | 9.697934799015 | PingYou Ltd (BuddenPing) |
| [85](n85.cert) | 9.742640687120 | PingYou Ltd (BuddenPing) |
| [86](n86.cert) | 9.820535407497 | PingYou Ltd (BuddenPing) |
| [87](n87.cert) | 9.838815269949 | PingYou Ltd (BuddenPing) |
| [88](n88.cert) | 9.882451030482 | PingYou Ltd (BuddenPing) |
| [89](n89.cert) | 9.949747468306 | PingYou Ltd (BuddenPing) |
| [101](n101.cert) | 10.535533905933 | PingYou Ltd (BuddenPing) |
| [102](n102.cert) | 10.605828696432 | PingYou Ltd (BuddenPing) |
| [103](n103.cert) | 10.679232047362 | PingYou Ltd (BuddenPing) |
| [104](n104.cert) | 10.707106781187 | PingYou Ltd (BuddenPing) |
| [105](n105.cert) | 10.789303783749 | PingYou Ltd (BuddenPing) |
| [106](n106.cert) | 10.822908044133 | PingYou Ltd (BuddenPing) |
| [107](n107.cert) | 10.846667192844 | PingYou Ltd (BuddenPing) |
| [108](n108.cert) | 10.904821012321 | PingYou Ltd (BuddenPing) |
| [109](n109.cert) | 10.949747468306 | PingYou Ltd (BuddenPing) |
| [110](n110.cert) | 10.996783396632 | PingYou Ltd (BuddenPing) |
| [122](n122.cert) | 11.535533905933 | PingYou Ltd (BuddenPing) |
| [123](n123.cert) | 11.591378145498 | PingYou Ltd (BuddenPing) |
| [124](n124.cert) | 11.656854249493 | PingYou Ltd (BuddenPing) |
| [125](n125.cert) | 11.707106781187 | PingYou Ltd (BuddenPing) |
| [126](n126.cert) | 11.742640687120 | PingYou Ltd (BuddenPing) |
| [127](n127.cert) | 11.810878787590 | PingYou Ltd (BuddenPing) |
| [128](n128.cert) | 11.825091968214 | PingYou Ltd (BuddenPing) |
| [129](n129.cert) | 11.870013850405 | Mykhailo Polkovskyi (Mishapolk) |
| [130](n130.cert) | 11.904483032516 | PingYou Ltd (BuddenPing) |
| [131](n131.cert) | 11.949659588036 | PingYou Ltd (BuddenPing) |
| [132](n132.cert) | 11.985680198846 | PingYou Ltd (BuddenPing) |
| [145](n145.cert) | 12.535533905933 | PingYou Ltd (BuddenPing) |
| [146](n146.cert) | 12.583782190152 | Evan Daniel |
| [147](n147.cert) | 12.656854249493 | PingYou Ltd (BuddenPing) |
| [148](n148.cert) | 12.656854249493 | PingYou Ltd (BuddenPing) |
| [149](n149.cert) | 12.707106781187 | PingYou Ltd (BuddenPing) |
| [150](n150.cert) | 12.778174593053 | PingYou Ltd (BuddenPing) |
| [151](n151.cert) | 12.822875655533 | PingYou Ltd (BuddenPing) |
| [152](n152.cert) | 12.830718800977 | PingYou Ltd (BuddenPing) |
| [153](n153.cert) | 12.870013850405 | Mykhailo Polkovskyi (Mishapolk) |
| [154](n154.cert) | 12.921206577133 | Mykhailo Polkovskyi (Mishapolk) |
| [155](n155.cert) | 12.952260944651 | Evan Daniel |
| [156](n156.cert) | 12.979165853835 | Mykhailo Polkovskyi (Mishapolk) |
| [170](n170.cert) | 13.535533905933 | PingYou Ltd (BuddenPing) |
| [171](n171.cert) | 13.571428571429 | PingYou Ltd (BuddenPing) |
| [172](n172.cert) | 13.618988956900 | PingYou Ltd (BuddenPing) |
| [173](n173.cert) | 13.656854249493 | PingYou Ltd (BuddenPing) |
| [174](n174.cert) | 13.707106781187 | PingYou Ltd (BuddenPing) |
| [175](n175.cert) | 13.764174317487 | Mykhailo Polkovskyi (Mishapolk) |
| [176](n176.cert) | 13.795872318437 | Mykhailo Polkovskyi (Mishapolk) |
| [177](n177.cert) | 13.822979734170 | PingYou Ltd (BuddenPing) |
| [178](n178.cert) | 13.846667192844 | PingYou Ltd (BuddenPing) |
| [179](n179.cert) | 13.883795490511 | PingYou Ltd (BuddenPing) |
| [180](n180.cert) | 13.916993522478 | PingYou Ltd (BuddenPing) |
| [181](n181.cert) | 13.950819531023 | PingYou Ltd (BuddenPing) |
| [182](n182.cert) | 13.974090713122 | PingYou Ltd (BuddenPing) |
| [197](n197.cert) | 14.535533905933 | PingYou Ltd (BuddenPing) |
| [198](n198.cert) | 14.571428571429 | PingYou Ltd (BuddenPing) |
| [199](n199.cert) | 14.617572173593 | PingYou Ltd (BuddenPing) |
| [200](n200.cert) | 14.656854249493 | PingYou Ltd (BuddenPing) |
| [201](n201.cert) | 14.707106781187 | PingYou Ltd (BuddenPing) |
| [202](n202.cert) | 14.727922061358 | PingYou Ltd (BuddenPing) |
| [203](n203.cert) | 14.778174593053 | PingYou Ltd (BuddenPing) |
| [204](n204.cert) | 14.808644417690 | Francisco Couzo; seed/construction: Mykhailo Polkovskyi (Mishapolk) |
| [205](n205.cert) | 14.824451146125 | PingYou Ltd (BuddenPing) |
| [206](n206.cert) | 14.860158663392 | PingYou Ltd (BuddenPing) |
| [207](n207.cert) | 14.880960371556 | Mykhailo Polkovskyi (Mishapolk) |
| [208](n208.cert) | 14.924518772030 | PingYou Ltd (BuddenPing) |
| [209](n209.cert) | 14.946223226447 | PingYou Ltd (BuddenPing) |
| [210](n210.cert) | 14.973001116588 | PingYou Ltd (BuddenPing) |
| [211](n211.cert) | 14.993549626300 | Francisco Couzo |
| [226](n226.cert) | 15.535533905933 | PingYou Ltd (BuddenPing) |
| [227](n227.cert) | 15.563796703670 | Joost de Winter |
| [228](n228.cert) | 15.604601475730 | PingYou Ltd (BuddenPing) |
| [229](n229.cert) | 15.650174756949 | Joost de Winter |
| [230](n230.cert) | 15.682926829269 | PingYou Ltd (BuddenPing) |
| [231](n231.cert) | 15.707106781187 | PingYou Ltd (BuddenPing) |
| [232](n232.cert) | 15.764174317487 | Mykhailo Polkovskyi (Mishapolk) |
| [233](n233.cert) | 15.778174593053 | PingYou Ltd (BuddenPing) |
| [234](n234.cert) | 15.822875655533 | PingYou Ltd (BuddenPing) |
| [235](n235.cert) | 15.826605633429 | PingYou Ltd (BuddenPing) |
| [236](n236.cert) | 15.861934390608 | Evan Daniel |
| [237](n237.cert) | 15.902603638260 | Francisco Couzo |
| [238](n238.cert) | 15.924106785322 | PingYou Ltd (BuddenPing) |
| [239](n239.cert) | 15.948443327301 | PingYou Ltd (BuddenPing) |
| [240](n240.cert) | 15.969685337531 | PingYou Ltd (BuddenPing) |
| [241](n241.cert) | 15.987117095151 | Francisco Couzo |
| [257](n257.cert) | 16.535533905933 | PingYou Ltd (BuddenPing) |
| [258](n258.cert) | 16.563448002134 | PingYou Ltd (BuddenPing) |
| [259](n259.cert) | 16.591378145498 | PingYou Ltd (BuddenPing) |
| [260](n260.cert) | 16.645778804182 | Joost de Winter |
| [261](n261.cert) | 16.678779875343 | BuddenPing |
| [262](n262.cert) | 16.707106781187 | PingYou Ltd (BuddenPing) |
| [263](n263.cert) | 16.733166007900 | PingYou Ltd (BuddenPing) |
| [264](n264.cert) | 16.774735132388 | Mykhailo Polkovskyi (Mishapolk) |
| [265](n265.cert) | 16.778174593053 | PingYou Ltd (BuddenPing) |
| [266](n266.cert) | 16.823028750757 | PingYou Ltd (BuddenPing) |
| [267](n267.cert) | 16.838815269949 | PingYou Ltd (BuddenPing) |
| [268](n268.cert) | 16.878814821007 | PingYou Ltd (BuddenPing) |
| [269](n269.cert) | 16.901513582190 | PingYou Ltd (BuddenPing) |
| [270](n270.cert) | 16.928196993330 | PingYou Ltd (BuddenPing) |
| [271](n271.cert) | 16.948947733714 | Evan Daniel |
| [272](n272.cert) | 16.965586474838 | PingYou Ltd (BuddenPing) |
| [273](n273.cert) | 16.983925962651 | PingYou Ltd (BuddenPing) |
| [290](n290.cert) | 17.535533905933 | PingYou Ltd (BuddenPing) |
| [291](n291.cert) | 17.535533905933 | PingYou Ltd (BuddenPing) |
| [292](n292.cert) | 17.591378145498 | PingYou Ltd (BuddenPing) |
| [293](n293.cert) | 17.634146341464 | PingYou Ltd (BuddenPing) |
| [294](n294.cert) | 17.656854249493 | PingYou Ltd (BuddenPing) |
| [295](n295.cert) | 17.704232790737 | PingYou Ltd (BuddenPing) |
| [296](n296.cert) | 17.707106781187 | PingYou Ltd (BuddenPing) |
| [297](n297.cert) | 17.740417287544 | PingYou Ltd (BuddenPing) |
| [298](n298.cert) | 17.778174593053 | PingYou Ltd (BuddenPing) |
| [299](n299.cert) | 17.822875655533 | PingYou Ltd (BuddenPing) |
| [300](n300.cert) | 17.824123388479 | PingYou Ltd (BuddenPing) |
| [301](n301.cert) | 17.846667192844 | PingYou Ltd (BuddenPing) |
| [302](n302.cert) | 17.870013850405 | Mykhailo Polkovskyi (Mishapolk) |
| [303](n303.cert) | 17.909958291070 | Mykhailo Polkovskyi (Mishapolk) |
| [304](n304.cert) | 17.929427758076 | Mykhailo Polkovskyi (Mishapolk) |
| [305](n305.cert) | 17.950466482138 | PingYou Ltd (BuddenPing) |
| [306](n306.cert) | 17.963433717492 | PingYou Ltd (BuddenPing) |
| [307](n307.cert) | 17.980862784055 | PingYou Ltd (BuddenPing) |
| [308](n308.cert) | 17.998269879527 | PingYou Ltd (BuddenPing) |
| [325](n325.cert) | 18.535533905933 | PingYou Ltd (BuddenPing) |
| [326](n326.cert) | 18.535533905933 | PingYou Ltd (BuddenPing) |
| [327](n327.cert) | 18.591378145498 | Francisco Couzo |
| [328](n328.cert) | 18.634146341464 | PingYou Ltd (BuddenPing) |
| [329](n329.cert) | 18.656854249493 | PingYou Ltd (BuddenPing) |
| [330](n330.cert) | 18.701641583454 | Francisco Couzo |
| [331](n331.cert) | 18.707106781187 | PingYou Ltd (BuddenPing) |
| [332](n332.cert) | 18.740417287544 | PingYou Ltd (BuddenPing) |
| [333](n333.cert) | 18.778174593053 | PingYou Ltd (BuddenPing) |
| [334](n334.cert) | 18.822875655533 | PingYou Ltd (BuddenPing) |
| [335](n335.cert) | 18.822875655562 | Francisco Couzo |
| [336](n336.cert) | 18.825571499862 | Francisco Couzo |
| [337](n337.cert) | 18.858391767637 | Francisco Couzo |
| [338](n338.cert) | 18.906332809853 | Francisco Couzo |
| [339](n339.cert) | 18.911307592083 | Francisco Couzo |
| [340](n340.cert) | 18.939649632892 | Francisco Couzo |
| [341](n341.cert) | 18.951882408720 | Francisco Couzo |
| [342](n342.cert) | 18.964706723173 | Francisco Couzo |
| [343](n343.cert) | 18.978232523636 | Evan Daniel (after Kevin Fang) |
| [344](n344.cert) | 18.993724691804 | Francisco Couzo |
| [362](n362.cert) | 19.535533905933 | PingYou Ltd (BuddenPing) |
| [363](n363.cert) | 19.535533905933 | PingYou Ltd (BuddenPing) |
| [364](n364.cert) | 19.583782190152 | Francisco Couzo; seed/construction: Evan Daniel |
| [365](n365.cert) | 19.621320343560 | Evan Daniel |
| [366](n366.cert) | 19.656854249493 | PingYou Ltd (BuddenPing) |
| [367](n367.cert) | 19.704232790737 | PingYou Ltd (BuddenPing) |
| [368](n368.cert) | 19.692388155448 | Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [369](n369.cert) | 19.707106781187 | Francisco Couzo |
| [370](n370.cert) | 19.767428349965 | Francisco Couzo |
| [371](n371.cert) | 19.822875655533 | PingYou Ltd (BuddenPing) |
| [372](n372.cert) | 19.822875655562 | Francisco Couzo |
| [373](n373.cert) | 19.823062082838 | Francisco Couzo |
| [374](n374.cert) | 19.832356217033 | Francisco Couzo |
| [375](n375.cert) | 19.882451030482 | Evan Daniel |
| [376](n376.cert) | 19.899494936612 | Francisco Couzo |
| [377](n377.cert) | 19.925720814331 | Francisco Couzo |
| [378](n378.cert) | 19.942505611659 | Francisco Couzo |
| [379](n379.cert) | 19.953014213942 | Francisco Couzo |
| [380](n380.cert) | 19.961601762402 | Francisco Couzo |
| [381](n381.cert) | 19.974740439431 | Francisco Couzo |
| [382](n382.cert) | 19.987621153966 | Francisco Couzo; seed/construction: Kevin Fang (TheSnakeFang) |
| [401](n401.cert) | 20.535533905933 | PingYou Ltd (BuddenPing) |
| [402](n402.cert) | 20.535533905933 | PingYou Ltd (BuddenPing) |
| [403](n403.cert) | 20.583782190152 | Francisco Couzo; seed/construction: Evan Daniel |
| [404](n404.cert) | 20.621320343560 | Evan Daniel |
| [405](n405.cert) | 20.656854249493 | PingYou Ltd (BuddenPing) |
| [406](n406.cert) | 20.692388155450 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [407](n407.cert) | 20.692388155451 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [408](n408.cert) | 20.707106781187 | Francisco Couzo |
| [409](n409.cert) | 20.767428349966 | Francisco Couzo |
| [410](n410.cert) | 20.778174593076 | Francisco Couzo |
| [411](n411.cert) | 20.822875655557 | Francisco Couzo |
| [412](n412.cert) | 20.823062082838 | Francisco Couzo |
| [413](n413.cert) | 20.831663365378 | Francisco Couzo |
| [414](n414.cert) | 20.882451030482 | Evan Daniel |
| [415](n415.cert) | 20.899494936612 | Francisco Couzo |
| [416](n416.cert) | 20.899494936636 | Frits Göbel; family formulas generalized by David Ellsworth |
| [417](n417.cert) | 20.942505611684 | Francisco Couzo |
| [418](n418.cert) | 20.945240141353 | Francisco Couzo |
| [419](n419.cert) | 20.959713620588 | Francisco Couzo |
| [420](n420.cert) | 20.974473103465 | Francisco Couzo |
| [421](n421.cert) | 20.982817421775 | Francisco Couzo |
| [422](n422.cert) | 20.984021832955 | Francisco Couzo |
| [442](n442.cert) | 21.535533905933 | PingYou Ltd (BuddenPing) |
| [443](n443.cert) | 21.535533905933 | PingYou Ltd (BuddenPing) |
| [444](n444.cert) | 21.583782190152 | Francisco Couzo; seed/construction: Evan Daniel |
| [445](n445.cert) | 21.606601717823 | Frits Göbel; family formulas generalized by David Ellsworth |
| [446](n446.cert) | 21.656854249493 | PingYou Ltd (BuddenPing) |
| [447](n447.cert) | 21.692388155457 | Francisco Couzo |
| [448](n448.cert) | 21.692388155458 | Francisco Couzo |
| [449](n449.cert) | 21.707106781187 | Francisco Couzo |
| [450](n450.cert) | 21.767428349966 | Francisco Couzo |
| [451](n451.cert) | 21.778174593076 | Francisco Couzo |
| [452](n452.cert) | 21.778174593086 | Francisco Couzo |
| [453](n453.cert) | 21.823014758318 | Francisco Couzo |
| [454](n454.cert) | 21.828427124844 | Francisco Couzo |
| [455](n455.cert) | 21.882451030482 | Evan Daniel |
| [456](n456.cert) | 21.899494936612 | Francisco Couzo |
| [457](n457.cert) | 21.899494936637 | Francisco Couzo |
| [458](n458.cert) | 21.942505611689 | Francisco Couzo |
| [459](n459.cert) | 21.943735551416 | Francisco Couzo |
| [460](n460.cert) | 21.957651945776 | Francisco Couzo |
| [461](n461.cert) | 21.972483922352 | Francisco Couzo |
| [462](n462.cert) | 21.980759715480 | Francisco Couzo |
| [463](n463.cert) | 21.984021832955 | Francisco Couzo |
| [464](n464.cert) | 21.988813022694 | Joost de Winter |
| [485](n485.cert) | 22.535533905933 | PingYou Ltd (BuddenPing) |
| [486](n486.cert) | 22.535533905933 | PingYou Ltd (BuddenPing) |
| [487](n487.cert) | 22.583782190178 | Francisco Couzo |
| [488](n488.cert) | 22.606601717827 | Francisco Couzo |
| [489](n489.cert) | 22.606601717825 | Frits Göbel; family formulas generalized by David Ellsworth |
| [490](n490.cert) | 22.656854249519 | Francisco Couzo |
| [491](n491.cert) | 22.692388155461 | Francisco Couzo |
| [492](n492.cert) | 22.707106781187 | Francisco Couzo |
| [493](n493.cert) | 22.707106781213 | Frits Göbel; family formulas generalized by David Ellsworth |
| [494](n494.cert) | 22.778174593076 | Francisco Couzo |
| [495](n495.cert) | 22.778174593079 | Francisco Couzo |
| [496](n496.cert) | 22.823014758318 | Francisco Couzo |
| [497](n497.cert) | 22.828427124774 | Francisco Couzo |
| [498](n498.cert) | 22.828427124827 | Francisco Couzo |
| [499](n499.cert) | 22.899494936612 | Francisco Couzo |
| [500](n500.cert) | 22.899494936637 | Francisco Couzo |
| [501](n501.cert) | 22.933763683699 | Francisco Couzo |
| [502](n502.cert) | 22.942809041609 | Francisco Couzo |
| [503](n503.cert) | 22.957558542542 | Francisco Couzo |
| [504](n504.cert) | 22.970562748504 | Francisco Couzo |
| [505](n505.cert) | 22.972317735354 | Francisco Couzo |
| [506](n506.cert) | 22.973102824304 | Francisco Couzo |
| [507](n507.cert) | 22.973760910106 | Francisco Couzo |
| [508](n508.cert) | 22.987759965313 | Francisco Couzo |
| [509](n509.cert) | 22.994328036438 | Joost de Winter |
| [530](n530.cert) | 23.535533905933 | PingYou Ltd (BuddenPing) |
| [531](n531.cert) | 23.535533905933 | PingYou Ltd (BuddenPing) |
| [532](n532.cert) | 23.583782190178 | Francisco Couzo |
| [533](n533.cert) | 23.606601717865 | Francisco Couzo |
| [534](n534.cert) | 23.606601717826 | Francisco Couzo |
| [535](n535.cert) | 23.656854249519 | Francisco Couzo |
| [536](n536.cert) | 23.677669529701 | Francisco Couzo |
| [537](n537.cert) | 23.707106781187 | Francisco Couzo |
| [538](n538.cert) | 23.707106781214 | Frits Göbel; family formulas generalized by David Ellsworth |
| [539](n539.cert) | 23.778174593076 | Francisco Couzo |
| [540](n540.cert) | 23.778174593079 | Francisco Couzo |
| [541](n541.cert) | 23.823014758318 | Francisco Couzo |
| [542](n542.cert) | 23.828427124774 | Francisco Couzo |
| [543](n543.cert) | 23.813708499013 | Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [544](n544.cert) | 23.828427124775 | Francisco Couzo |
| [545](n545.cert) | 23.899494936637 | Francisco Couzo |
| [546](n546.cert) | 23.933763683699 | Francisco Couzo |
| [547](n547.cert) | 23.942809041643 | Francisco Couzo |
| [548](n548.cert) | 23.957558542543 | Francisco Couzo |
| [549](n549.cert) | 23.961513018492 | elimination from n=550 (this project) |
| [550](n550.cert) | 23.961513018469 | Francisco Couzo |
| [551](n551.cert) | 23.966898919633 | Francisco Couzo |
| [552](n552.cert) | 23.966901721108 | Francisco Couzo |
| [553](n553.cert) | 23.981588093282 | Francisco Couzo; seed/construction: franciscouzo |
| [555](n555.cert) | 23.993653790591 | Joost de Winter |
| [577](n577.cert) | 24.535533905933 | PingYou Ltd (BuddenPing) |
| [578](n578.cert) | 24.535533905933 | PingYou Ltd (BuddenPing) |
| [579](n579.cert) | 24.583782190178 | Francisco Couzo |
| [580](n580.cert) | 24.606601717827 | Francisco Couzo |
| [581](n581.cert) | 24.606601717826 | Francisco Couzo |
| [582](n582.cert) | 24.656854249519 | Francisco Couzo |
| [583](n583.cert) | 24.677669529693 | Francisco Couzo |
| [584](n584.cert) | 24.677669529693 | Francisco Couzo |
| [585](n585.cert) | 24.707106781227 | Francisco Couzo |
| [586](n586.cert) | 24.707106781216 | Frits Göbel; family formulas generalized by David Ellsworth |
| [587](n587.cert) | 24.778174593079 | Francisco Couzo |
| [588](n588.cert) | 24.813708499018 | Francisco Couzo |
| [589](n589.cert) | 24.813708499019 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [590](n590.cert) | 24.813708499238 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [591](n591.cert) | 24.828427124775 | Francisco Couzo |
| [592](n592.cert) | 24.899494936637 | Francisco Couzo |
| [593](n593.cert) | 24.899494936641 | Francisco Couzo |
| [594](n594.cert) | 24.899494936641 | Francisco Couzo |
| [595](n595.cert) | 24.949747468431 | Francisco Couzo |
| [596](n596.cert) | 24.949747468335 | Francisco Couzo |
| [597](n597.cert) | 24.961513018469 | Francisco Couzo |
| [598](n598.cert) | 24.962916747309 | Francisco Couzo |
| [599](n599.cert) | 24.966901721108 | Francisco Couzo |
| [600](n600.cert) | 24.981585347399 | Francisco Couzo |
| [601](n601.cert) | 24.989482347414 | Francisco Couzo |
| [602](n602.cert) | 24.993653790591 | Joost de Winter |
| [603](n603.cert) | 24.995268064197 | Joost de Winter |
| [626](n626.cert) | 25.520815280201 | Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [627](n627.cert) | 25.535533905933 | PingYou Ltd (BuddenPing) |
| [628](n628.cert) | 25.583782190178 | Francisco Couzo |
| [629](n629.cert) | 25.606601717827 | Francisco Couzo |
| [630](n630.cert) | 25.606601717826 | Francisco Couzo |
| [631](n631.cert) | 25.656854249519 | Francisco Couzo |
| [632](n632.cert) | 25.677669529693 | Francisco Couzo |
| [633](n633.cert) | 25.677669529693 | Francisco Couzo |
| [634](n634.cert) | 25.707106781225 | Francisco Couzo |
| [635](n635.cert) | 25.707106781217 | Frits Göbel; family formulas generalized by David Ellsworth |
| [636](n636.cert) | 25.727922061388 | Frits Göbel; family formulas generalized by David Ellsworth |
| [637](n637.cert) | 25.778174593082 | Francisco Couzo |
| [638](n638.cert) | 25.813708499023 | Francisco Couzo |
| [639](n639.cert) | 25.813708499025 | Francisco Couzo |
| [640](n640.cert) | 25.828427124775 | Francisco Couzo |
| [641](n641.cert) | 25.899494936637 | Francisco Couzo |
| [642](n642.cert) | 25.899494936641 | Francisco Couzo |
| [643](n643.cert) | 25.899494936641 | Francisco Couzo |
| [644](n644.cert) | 25.899494936642 | Francisco Couzo |
| [645](n645.cert) | 25.949747468335 | Francisco Couzo |
| [646](n646.cert) | 25.949747468336 | Francisco Couzo |
| [647](n647.cert) | 25.953248543199 | Francisco Couzo |
| [648](n648.cert) | 25.966901721108 | Francisco Couzo |
| [649](n649.cert) | 25.976974088403 | Francisco Couzo |
| [650](n650.cert) | 25.982429027496 | Francisco Couzo |
| [651](n651.cert) | 25.983790120159 | Francisco Couzo |
| [652](n652.cert) | 25.995268064197 | Joost de Winter |
| [654](n654.cert) | 25.996103908965 | Joost de Winter |
| [677](n677.cert) | 26.520815280213 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [678](n678.cert) | 26.535533905933 | PingYou Ltd (BuddenPing) |
| [679](n679.cert) | 26.583782190178 | Francisco Couzo |
| [680](n680.cert) | 26.606601717827 | Francisco Couzo |
| [681](n681.cert) | 26.606601717826 | Francisco Couzo |
| [682](n682.cert) | 26.656854249519 | Francisco Couzo |
| [683](n683.cert) | 26.677669529693 | Francisco Couzo |
| [684](n684.cert) | 26.677669529693 | Francisco Couzo |
| [685](n685.cert) | 26.707106781220 | Francisco Couzo |
| [686](n686.cert) | 26.707106781218 | Frits Göbel; family formulas generalized by David Ellsworth |
| [687](n687.cert) | 26.727922061390 | Francisco Couzo |
| [688](n688.cert) | 26.727922061389 | Frits Göbel; family formulas generalized by David Ellsworth |
| [689](n689.cert) | 26.778174593084 | Francisco Couzo |
| [690](n690.cert) | 26.813708499267 | Francisco Couzo |
| [691](n691.cert) | 26.828427124775 | Francisco Couzo |
| [692](n692.cert) | 26.828427124777 | Francisco Couzo |
| [693](n693.cert) | 26.899494936641 | Francisco Couzo |
| [694](n694.cert) | 26.899494936641 | Francisco Couzo |
| [695](n695.cert) | 26.899494936642 | Francisco Couzo |
| [696](n696.cert) | 26.949747468335 | Francisco Couzo |
| [697](n697.cert) | 26.949747468336 | Francisco Couzo |
| [698](n698.cert) | 26.949747468338 | Francisco Couzo |
| [699](n699.cert) | 26.949747468415 | Francisco Couzo |
| [700](n700.cert) | 26.972996848621 | Francisco Couzo |
| [701](n701.cert) | 26.975561031531 | Francisco Couzo |
| [702](n702.cert) | 26.977494114977 | Francisco Couzo |
| [703](n703.cert) | 26.987493360751 | Francisco Couzo; seed/construction: Kevin Fang (rectangle and gluing); PingYou Ltd (BuddenPing) (square input) |
| [705](n705.cert) | 26.996103908965 | Joost de Winter |
| [706](n706.cert) | 26.998712100405 | Joost de Winter |
| [730](n730.cert) | 27.520815280206 | Francisco Couzo |
| [731](n731.cert) | 27.535533905933 | PingYou Ltd (BuddenPing) |
| [732](n732.cert) | 27.583782190178 | Francisco Couzo |
| [733](n733.cert) | 27.606601717827 | Francisco Couzo |
| [734](n734.cert) | 27.606601717826 | Francisco Couzo |
| [735](n735.cert) | 27.656854249519 | Francisco Couzo |
| [736](n736.cert) | 27.656854249525 | Francisco Couzo |
| [737](n737.cert) | 27.677669529693 | Francisco Couzo |
| [738](n738.cert) | 27.707106781220 | Francisco Couzo |
| [739](n739.cert) | 27.707106781231 | Francisco Couzo |
| [740](n740.cert) | 27.707106781219 | Frits Göbel; family formulas generalized by David Ellsworth |
| [741](n741.cert) | 27.727922061420 | Francisco Couzo |
| [742](n742.cert) | 27.778174593084 | Francisco Couzo |
| [743](n743.cert) | 27.798989873283 | elimination from n=744 (this project) |
| [744](n744.cert) | 27.798989873256 | Francisco Couzo |
| [745](n745.cert) | 27.828427124777 | Francisco Couzo |
| [746](n746.cert) | 27.828427124795 | Francisco Couzo |
| [747](n747.cert) | 27.899494936641 | Francisco Couzo |
| [748](n748.cert) | 27.899494936642 | Francisco Couzo |
| [749](n749.cert) | 27.925883089331 | Francisco Couzo; seed/construction: franciscouzo |
| [750](n750.cert) | 27.928780276056 | Francisco Couzo |
| [751](n751.cert) | 27.942911732376 | elimination from n=754 (this project) |
| [752](n752.cert) | 27.935028842577 | Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [753](n753.cert) | 27.938719376566 | Francisco Couzo |
| [754](n754.cert) | 27.937423518013 | Francisco Couzo |
| [755](n755.cert) | 27.952229334413 | Francisco Couzo |
| [756](n756.cert) | 27.984237490911 | Francisco Couzo |
| [757](n757.cert) | 27.989936988207 | Francisco Couzo; seed/construction: Kevin Fang (rectangle and gluing); PingYou Ltd (BuddenPing) (square input) |
| [758](n758.cert) | 27.994980212536 | Francisco Couzo |
| [760](n760.cert) | 27.995949340329 | Joost de Winter |
| [785](n785.cert) | 28.520815280214 | Francisco Couzo |
| [786](n786.cert) | 28.535533905933 | PingYou Ltd (BuddenPing) |
| [787](n787.cert) | 28.583782190178 | Francisco Couzo |
| [788](n788.cert) | 28.606601717827 | Francisco Couzo |
| [789](n789.cert) | 28.606601717826 | Francisco Couzo |
| [790](n790.cert) | 28.656854249519 | Francisco Couzo |
| [791](n791.cert) | 28.656854249525 | Francisco Couzo |
| [792](n792.cert) | 28.656854249526 | Francisco Couzo |
| [793](n793.cert) | 28.707106781220 | Francisco Couzo |
| [794](n794.cert) | 28.707106781231 | Francisco Couzo |
| [795](n795.cert) | 28.707106781220 | Frits Göbel; family formulas generalized by David Ellsworth |
| [796](n796.cert) | 28.727922061393 | Francisco Couzo |
| [797](n797.cert) | 28.778174593084 | Francisco Couzo |
| [798](n798.cert) | 28.798989873285 | elimination from n=800 (this project) |
| [799](n799.cert) | 28.798989873256 | Francisco Couzo |
| [800](n800.cert) | 28.798989873257 | Francisco Couzo |
| [801](n801.cert) | 28.828427124795 | Francisco Couzo |
| [802](n802.cert) | 28.828427124817 | Francisco Couzo |
| [803](n803.cert) | 28.899494936642 | Francisco Couzo |
| [804](n804.cert) | 28.917335789888 | Francisco Couzo |
| [805](n805.cert) | 28.921843659464 | Francisco Couzo |
| [806](n806.cert) | 28.921843662228 | Francisco Couzo |
| [807](n807.cert) | 28.933881004742 | elimination from n=808 (this project) |
| [808](n808.cert) | 28.933881004714 | Francisco Couzo |
| [809](n809.cert) | 28.937423518015 | Francisco Couzo |
| [810](n810.cert) | 28.951463124704 | Francisco Couzo |
| [811](n811.cert) | 28.983553774277 | Francisco Couzo |
| [812](n812.cert) | 28.982472918533 | Francisco Couzo |
| [813](n813.cert) | 28.990394020145 | Francisco Couzo; seed/construction: Kevin Fang (rectangle and gluing); PingYou Ltd (BuddenPing) (square input) |
| [814](n814.cert) | 28.997905039848 | Francisco Couzo |
| [815](n815.cert) | 28.995949340329 | Joost de Winter |
| [817](n817.cert) | 28.998488480775 | Joost de Winter |
| [842](n842.cert) | 29.520815280218 | Francisco Couzo |
| [843](n843.cert) | 29.535533905933 | PingYou Ltd (BuddenPing) |
| [844](n844.cert) | 29.583782190178 | Francisco Couzo |
| [845](n845.cert) | 29.606601717827 | Francisco Couzo |
| [846](n846.cert) | 29.606601717826 | Francisco Couzo |
| [847](n847.cert) | 29.656854249519 | Francisco Couzo |
| [848](n848.cert) | 29.656854249525 | Francisco Couzo |
| [849](n849.cert) | 29.642135623766 | Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [850](n850.cert) | 29.656854249528 | Francisco Couzo |
| [851](n851.cert) | 29.707106781231 | Francisco Couzo |
| [852](n852.cert) | 29.707106781250 | Francisco Couzo |
| [853](n853.cert) | 29.707106781222 | Frits Göbel; family formulas generalized by David Ellsworth |
| [854](n854.cert) | 29.778174593084 | Francisco Couzo |
| [855](n855.cert) | 29.798989873287 | elimination from n=856 (this project) |
| [856](n856.cert) | 29.798989873256 | Francisco Couzo |
| [857](n857.cert) | 29.798989873257 | Francisco Couzo |
| [858](n858.cert) | 29.828427124795 | Francisco Couzo |
| [859](n859.cert) | 29.828427124807 | Francisco Couzo |
| [860](n860.cert) | 29.849242405007 | Francisco Couzo |
| [861](n861.cert) | 29.849242404953 | Frits Göbel; family formulas generalized by David Ellsworth |
| [862](n862.cert) | 29.899494936647 | Francisco Couzo |
| [863](n863.cert) | 29.921843659464 | Francisco Couzo |
| [864](n864.cert) | 29.933881004742 | elimination from n=808 (this project) |
| [865](n865.cert) | 29.933881004714 | Francisco Couzo |
| [866](n866.cert) | 29.935764472087 | Francisco Couzo |
| [867](n867.cert) | 29.950265025802 | Francisco Couzo |
| [868](n868.cert) | 29.982204111182 | Francisco Couzo |
| [869](n869.cert) | 29.982472918533 | Francisco Couzo |
| [870](n870.cert) | 29.985969207342 | Francisco Couzo |
| [871](n871.cert) | 29.989329079687 | Francisco Couzo |
| [872](n872.cert) | 29.995949340329 | Joost de Winter |
| [874](n874.cert) | 29.998488480775 | Joost de Winter |
| [875](n875.cert) | 29.998783733108 | Joost de Winter |
| [901](n901.cert) | 30.520815280221 | Francisco Couzo |
| [902](n902.cert) | 30.535533905933 | PingYou Ltd (BuddenPing) |
| [903](n903.cert) | 30.583782190178 | Francisco Couzo |
| [904](n904.cert) | 30.606601717827 | Francisco Couzo |
| [905](n905.cert) | 30.606601717826 | Francisco Couzo |
| [906](n906.cert) | 30.642135623809 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [907](n907.cert) | 30.642135623809 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [908](n908.cert) | 30.642135626714 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [909](n909.cert) | 30.656854249528 | Francisco Couzo |
| [910](n910.cert) | 30.707106781225 | Francisco Couzo |
| [911](n911.cert) | 30.707106781239 | Francisco Couzo |
| [912](n912.cert) | 30.707106781223 | Frits Göbel; family formulas generalized by David Ellsworth |
| [913](n913.cert) | 30.778174593084 | Francisco Couzo |
| [914](n914.cert) | 30.778174593089 | Francisco Couzo |
| [915](n915.cert) | 30.798989873256 | Francisco Couzo |
| [916](n916.cert) | 30.798989873257 | Francisco Couzo |
| [917](n917.cert) | 30.828427124795 | Francisco Couzo |
| [918](n918.cert) | 30.828427124807 | Francisco Couzo |
| [919](n919.cert) | 30.849242404990 | Francisco Couzo |
| [920](n920.cert) | 30.849242404954 | Francisco Couzo |
| [921](n921.cert) | 30.849242404954 | Frits Göbel; family formulas generalized by David Ellsworth |
| [922](n922.cert) | 30.899494936660 | Francisco Couzo |
| [923](n923.cert) | 30.933766814067 | elimination from n=924 (this project) |
| [924](n924.cert) | 30.933766814037 | Francisco Couzo |
| [925](n925.cert) | 30.935764472087 | Francisco Couzo |
| [926](n926.cert) | 30.949634321517 | Francisco Couzo |
| [927](n927.cert) | 30.978751259458 | Francisco Couzo |
| [928](n928.cert) | 30.976993727283 | Francisco Couzo |
| [929](n929.cert) | 30.978848462737 | Francisco Couzo |
| [930](n930.cert) | 30.982052182975 | Francisco Couzo |
| [931](n931.cert) | 30.989936243547 | Francisco Couzo; seed/construction: Kevin Fang (rectangle and gluing); PingYou Ltd (BuddenPing) (square input) |
| [932](n932.cert) | 30.998315839258 | Francisco Couzo |
| [935](n935.cert) | 30.995955854834 | Joost de Winter |
| [962](n962.cert) | 31.520815280221 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [963](n963.cert) | 31.535533905933 | PingYou Ltd (BuddenPing) |
| [964](n964.cert) | 31.556349186141 | Frits Göbel; family formulas generalized by David Ellsworth |
| [965](n965.cert) | 31.606601717827 | Francisco Couzo |
| [966](n966.cert) | 31.606601717826 | Francisco Couzo |
| [967](n967.cert) | 31.642135623812 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [968](n968.cert) | 31.642135623812 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [969](n969.cert) | 31.642135623812 | Francisco Couzo; seed/construction: Erich Friedman (off-centre extension of Frits Göbel’s construction) |
| [970](n970.cert) | 31.656854249528 | Francisco Couzo |
| [971](n971.cert) | 31.707106781225 | Francisco Couzo |
| [972](n972.cert) | 31.707106781248 | Francisco Couzo |
| [973](n973.cert) | 31.707106781282 | Francisco Couzo |
| [974](n974.cert) | 31.707106781224 | Frits Göbel; family formulas generalized by David Ellsworth |
| [975](n975.cert) | 31.778174593089 | Francisco Couzo |
| [976](n976.cert) | 31.778174593090 | Francisco Couzo |
| [977](n977.cert) | 31.798989873257 | Francisco Couzo |
| [978](n978.cert) | 31.828427124795 | Francisco Couzo |
| [979](n979.cert) | 31.828427124833 | Francisco Couzo |
| [980](n980.cert) | 31.828427124802 | Francisco Couzo |
| [981](n981.cert) | 31.849242404954 | Francisco Couzo |
| [982](n982.cert) | 31.849242405004 | Francisco Couzo |
| [983](n983.cert) | 31.899494936650 | Francisco Couzo |
| [984](n984.cert) | 31.920310216821 | Francisco Couzo |
| [985](n985.cert) | 31.920310216858 | Francisco Couzo |
| [986](n986.cert) | 31.920310216821 | Francisco Couzo |
| [987](n987.cert) | 31.949634321517 | Francisco Couzo |
| [988](n988.cert) | 31.949747468406 | Francisco Couzo |
| [989](n989.cert) | 31.976993727283 | Francisco Couzo |
| [990](n990.cert) | 31.978848462737 | Francisco Couzo |
| [991](n991.cert) | 31.982052182975 | Francisco Couzo |
| [992](n992.cert) | 31.985186362925 | Francisco Couzo; seed/construction: Kevin Fang (rectangle and gluing); PingYou Ltd (BuddenPing) (square input) |
| [993](n993.cert) | 31.985130163599 | Francisco Couzo |
| [994](n994.cert) | 31.996783396632 | Kevin Fang (rectangle and gluing); PingYou Ltd (BuddenPing) (square input) |
| [996](n996.cert) | 31.995955854834 | Joost de Winter |
| [998](n998.cert) | 31.998349747355 | Joost de Winter |

## Complete catalogue

| n | Verified upper, rounded up | Witness |
|---:|---:|---|
| 1 | 1.000000000000 | grid |
| 2 | 2.000000000000 | grid |
| 3 | 2.000000000000 | grid |
| 4 | 2.000000000000 | grid |
| 5 | 2.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 6 | 3.000000000000 | grid |
| 7 | 3.000000000000 | grid |
| 8 | 3.000000000000 | grid |
| 9 | 3.000000000000 | grid |
| 10 | 3.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 11 | 3.877083590023 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 12 | 4.000000000000 | grid |
| 13 | 4.000000000000 | grid |
| 14 | 4.000000000000 | grid |
| 15 | 4.000000000000 | grid |
| 16 | 4.000000000000 | grid |
| 17 | 4.675530093605 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 18 | 4.822875655533 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 19 | 4.885618083165 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 20 | 5.000000000000 | grid |
| 21 | 5.000000000000 | grid |
| 22 | 5.000000000000 | grid |
| 23 | 5.000000000000 | grid |
| 24 | 5.000000000000 | grid |
| 25 | 5.000000000000 | grid |
| 26 | 5.621320343560 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 27 | 5.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 28 | 5.824444616675 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 29 | 5.933833462677 | [source](https://github.com/jlevy/squares/blob/ad28cc7845ebe08d9a894f61fd1ab45cc604cfd7/packing/resources/web/pingyou-pr622-certificate-2026-10-15/facts/n-029.yaml.gz) |
| 30 | 6.000000000000 | grid |
| 31 | 6.000000000000 | grid |
| 32 | 6.000000000000 | grid |
| 33 | 6.000000000000 | grid |
| 34 | 6.000000000000 | grid |
| 35 | 6.000000000000 | grid |
| 36 | 6.000000000000 | grid |
| 37 | 6.598619609245 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 38 | 6.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 39 | 6.810722083069 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 40 | 6.828427124747 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 41 | 6.926693094469 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 42 | 7.000000000000 | grid |
| 43 | 7.000000000000 | grid |
| 44 | 7.000000000000 | grid |
| 45 | 7.000000000000 | grid |
| 46 | 7.000000000000 | grid |
| 47 | 7.000000000000 | grid |
| 48 | 7.000000000000 | grid |
| 49 | 7.000000000000 | grid |
| 50 | 7.571428571429 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 51 | 7.690355937289 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 52 | 7.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 53 | 7.822875655533 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 54 | 7.846667192844 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 55 | 7.945771007504 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 56 | 8.000000000000 | grid |
| 57 | 8.000000000000 | grid |
| 58 | 8.000000000000 | grid |
| 59 | 8.000000000000 | grid |
| 60 | 8.000000000000 | grid |
| 61 | 8.000000000000 | grid |
| 62 | 8.000000000000 | grid |
| 63 | 8.000000000000 | grid |
| 64 | 8.000000000000 | grid |
| 65 | 8.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 66 | 8.656854249493 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 67 | 8.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 68 | 8.798795237219 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 69 | 8.827194655730 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 70 | 8.880960371556 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 71 | 8.944071557571 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 72 | 9.000000000000 | grid |
| 73 | 9.000000000000 | grid |
| 74 | 9.000000000000 | grid |
| 75 | 9.000000000000 | grid |
| 76 | 9.000000000000 | grid |
| 77 | 9.000000000000 | grid |
| 78 | 9.000000000000 | grid |
| 79 | 9.000000000000 | grid |
| 80 | 9.000000000000 | grid |
| 81 | 9.000000000000 | grid |
| 82 | 9.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 83 | 9.634757648632 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 84 | 9.697934799015 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 85 | 9.742640687120 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 86 | 9.820535407497 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 87 | 9.838815269949 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 88 | 9.882451030482 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 89 | 9.949747468306 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 90 | 10.000000000000 | grid |
| 91 | 10.000000000000 | grid |
| 92 | 10.000000000000 | grid |
| 93 | 10.000000000000 | grid |
| 94 | 10.000000000000 | grid |
| 95 | 10.000000000000 | grid |
| 96 | 10.000000000000 | grid |
| 97 | 10.000000000000 | grid |
| 98 | 10.000000000000 | grid |
| 99 | 10.000000000000 | grid |
| 100 | 10.000000000000 | grid |
| 101 | 10.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 102 | 10.605828696432 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 103 | 10.679232047362 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 104 | 10.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 105 | 10.789303783749 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 106 | 10.822908044133 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 107 | 10.846667192844 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 108 | 10.904821012321 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 109 | 10.949747468306 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 110 | 10.996783396632 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 111 | 11.000000000000 | grid |
| 112 | 11.000000000000 | grid |
| 113 | 11.000000000000 | grid |
| 114 | 11.000000000000 | grid |
| 115 | 11.000000000000 | grid |
| 116 | 11.000000000000 | grid |
| 117 | 11.000000000000 | grid |
| 118 | 11.000000000000 | grid |
| 119 | 11.000000000000 | grid |
| 120 | 11.000000000000 | grid |
| 121 | 11.000000000000 | grid |
| 122 | 11.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 123 | 11.591378145498 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 124 | 11.656854249493 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 125 | 11.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 126 | 11.742640687120 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 127 | 11.810878787590 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 128 | 11.825091968214 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 129 | 11.870013850405 | [certificate](n129.cert) |
| 130 | 11.904483032516 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 131 | 11.949659588036 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 132 | 11.985680198846 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 133 | 12.000000000000 | grid |
| 134 | 12.000000000000 | grid |
| 135 | 12.000000000000 | grid |
| 136 | 12.000000000000 | grid |
| 137 | 12.000000000000 | grid |
| 138 | 12.000000000000 | grid |
| 139 | 12.000000000000 | grid |
| 140 | 12.000000000000 | grid |
| 141 | 12.000000000000 | grid |
| 142 | 12.000000000000 | grid |
| 143 | 12.000000000000 | grid |
| 144 | 12.000000000000 | grid |
| 145 | 12.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 146 | 12.583782190152 | [source](https://github.com/jlevy/squares/issues/399) |
| 147 | 12.656854249493 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 148 | 12.656854249493 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 149 | 12.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 150 | 12.778174593053 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 151 | 12.822875655533 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 152 | 12.830718800977 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 153 | 12.870013850405 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-exact-153-302-2026-10-13-v1) |
| 154 | 12.921206577133 | [certificate](n154.cert) |
| 155 | 12.952260944651 | [source](https://github.com/evand/square-packing/blob/59326b8/search/packer/candidates/s155_ex2.cert) |
| 156 | 12.979165853835 | [certificate](n156.cert) |
| 157 | 13.000000000000 | grid |
| 158 | 13.000000000000 | grid |
| 159 | 13.000000000000 | grid |
| 160 | 13.000000000000 | grid |
| 161 | 13.000000000000 | grid |
| 162 | 13.000000000000 | grid |
| 163 | 13.000000000000 | grid |
| 164 | 13.000000000000 | grid |
| 165 | 13.000000000000 | grid |
| 166 | 13.000000000000 | grid |
| 167 | 13.000000000000 | grid |
| 168 | 13.000000000000 | grid |
| 169 | 13.000000000000 | grid |
| 170 | 13.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 171 | 13.571428571429 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 172 | 13.618988956900 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 173 | 13.656854249493 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 174 | 13.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 175 | 13.764174317487 | [certificate](n175.cert) |
| 176 | 13.795872318437 | [certificate](n176.cert) |
| 177 | 13.822979734170 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 178 | 13.846667192844 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 179 | 13.883795490511 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 180 | 13.916993522478 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 181 | 13.950819531023 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 182 | 13.974090713122 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 183 | 14.000000000000 | grid |
| 184 | 14.000000000000 | grid |
| 185 | 14.000000000000 | grid |
| 186 | 14.000000000000 | grid |
| 187 | 14.000000000000 | grid |
| 188 | 14.000000000000 | grid |
| 189 | 14.000000000000 | grid |
| 190 | 14.000000000000 | grid |
| 191 | 14.000000000000 | grid |
| 192 | 14.000000000000 | grid |
| 193 | 14.000000000000 | grid |
| 194 | 14.000000000000 | grid |
| 195 | 14.000000000000 | grid |
| 196 | 14.000000000000 | grid |
| 197 | 14.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 198 | 14.571428571429 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 199 | 14.617572173593 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 200 | 14.656854249493 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 201 | 14.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 202 | 14.727922061358 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 203 | 14.778174593053 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 204 | 14.808644417690 | [current certificate](../n204.cert) |
| 205 | 14.824451146125 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 206 | 14.860158663392 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 207 | 14.880960371556 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 208 | 14.924518772030 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 209 | 14.946223226447 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 210 | 14.973001116588 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 211 | 14.993549626300 | [current certificate](../n211.cert) |
| 212 | 15.000000000000 | grid |
| 213 | 15.000000000000 | grid |
| 214 | 15.000000000000 | grid |
| 215 | 15.000000000000 | grid |
| 216 | 15.000000000000 | grid |
| 217 | 15.000000000000 | grid |
| 218 | 15.000000000000 | grid |
| 219 | 15.000000000000 | grid |
| 220 | 15.000000000000 | grid |
| 221 | 15.000000000000 | grid |
| 222 | 15.000000000000 | grid |
| 223 | 15.000000000000 | grid |
| 224 | 15.000000000000 | grid |
| 225 | 15.000000000000 | grid |
| 226 | 15.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 227 | 15.563796703670 | [source](https://github.com/JoostdeWinter/square-packing/blob/c95c4938f068ed44a1819ef973e770ec241aa567/n227/n227_record.cert) |
| 228 | 15.604601475730 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 229 | 15.650174756949 | [source](https://github.com/JoostdeWinter/square-packing/blob/c95c4938f068ed44a1819ef973e770ec241aa567/n229/n229_record.cert) |
| 230 | 15.682926829269 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 231 | 15.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 232 | 15.764174317487 | [certificate](n232.cert) |
| 233 | 15.778174593053 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 234 | 15.822875655533 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 235 | 15.826605633429 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 236 | 15.861934390608 | [source](https://github.com/jlevy/squares/issues/399) |
| 237 | 15.902603638260 | [current certificate](../n237.cert) |
| 238 | 15.924106785322 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 239 | 15.948443327301 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 240 | 15.969685337531 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 241 | 15.987117095151 | [current certificate](../n241.cert) |
| 242 | 16.000000000000 | grid |
| 243 | 16.000000000000 | grid |
| 244 | 16.000000000000 | grid |
| 245 | 16.000000000000 | grid |
| 246 | 16.000000000000 | grid |
| 247 | 16.000000000000 | grid |
| 248 | 16.000000000000 | grid |
| 249 | 16.000000000000 | grid |
| 250 | 16.000000000000 | grid |
| 251 | 16.000000000000 | grid |
| 252 | 16.000000000000 | grid |
| 253 | 16.000000000000 | grid |
| 254 | 16.000000000000 | grid |
| 255 | 16.000000000000 | grid |
| 256 | 16.000000000000 | grid |
| 257 | 16.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 258 | 16.563448002134 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 259 | 16.591378145498 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 260 | 16.645778804182 | [source](https://github.com/JoostdeWinter/square-packing/blob/c95c4938f068ed44a1819ef973e770ec241aa567/n260/n260_record.cert) |
| 261 | 16.678779875343 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 262 | 16.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 263 | 16.733166007900 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 264 | 16.774735132388 | [certificate](n264.cert) |
| 265 | 16.778174593053 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 266 | 16.823028750757 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 267 | 16.838815269949 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 268 | 16.878814821007 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 269 | 16.901513582190 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 270 | 16.928196993330 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 271 | 16.948947733714 | [source](https://github.com/evand/square-packing/blob/757b40b/search/packer/candidates/s271_ex1.cert) |
| 272 | 16.965586474838 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 273 | 16.983925962651 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 274 | 17.000000000000 | grid |
| 275 | 17.000000000000 | grid |
| 276 | 17.000000000000 | grid |
| 277 | 17.000000000000 | grid |
| 278 | 17.000000000000 | grid |
| 279 | 17.000000000000 | grid |
| 280 | 17.000000000000 | grid |
| 281 | 17.000000000000 | grid |
| 282 | 17.000000000000 | grid |
| 283 | 17.000000000000 | grid |
| 284 | 17.000000000000 | grid |
| 285 | 17.000000000000 | grid |
| 286 | 17.000000000000 | grid |
| 287 | 17.000000000000 | grid |
| 288 | 17.000000000000 | grid |
| 289 | 17.000000000000 | grid |
| 290 | 17.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 291 | 17.535533905933 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 292 | 17.591378145498 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 293 | 17.634146341464 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 294 | 17.656854249493 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 295 | 17.704232790737 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 296 | 17.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 297 | 17.740417287544 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 298 | 17.778174593053 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 299 | 17.822875655533 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-algebraic-refinements-2026-10-13-v1) |
| 300 | 17.824123388479 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 301 | 17.846667192844 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 302 | 17.870013850405 | [certificate](n302.cert) |
| 303 | 17.909958291070 | [certificate](n303.cert) |
| 304 | 17.929427758076 | [certificate](n304.cert) |
| 305 | 17.950466482138 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 306 | 17.963433717492 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 307 | 17.980862784055 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 308 | 17.998269879527 | [source](https://github.com/BuddenPing/square-packing-certificates/releases/tag/data/pingyou-numerical-refinements-2026-10-13-v2) |
| 309 | 18.000000000000 | grid |
| 310 | 18.000000000000 | grid |
| 311 | 18.000000000000 | grid |
| 312 | 18.000000000000 | grid |
| 313 | 18.000000000000 | grid |
| 314 | 18.000000000000 | grid |
| 315 | 18.000000000000 | grid |
| 316 | 18.000000000000 | grid |
| 317 | 18.000000000000 | grid |
| 318 | 18.000000000000 | grid |
| 319 | 18.000000000000 | grid |
| 320 | 18.000000000000 | grid |
| 321 | 18.000000000000 | grid |
| 322 | 18.000000000000 | grid |
| 323 | 18.000000000000 | grid |
| 324 | 18.000000000000 | grid |
| 325 | 18.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 326 | 18.535533905933 | [certificate](n326.cert) |
| 327 | 18.591378145498 | [certificate](n327.cert) |
| 328 | 18.634146341464 | [certificate](n328.cert) |
| 329 | 18.656854249493 | [certificate](n329.cert) |
| 330 | 18.701641583454 | [current certificate](../n330.cert) |
| 331 | 18.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 332 | 18.740417287544 | [certificate](n332.cert) |
| 333 | 18.778174593053 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 334 | 18.822875655533 | [certificate](n334.cert) |
| 335 | 18.822875655562 | [current certificate](../n335.cert) |
| 336 | 18.825571499862 | [current certificate](../n336.cert) |
| 337 | 18.858391767637 | [current certificate](../n337.cert) |
| 338 | 18.906332809853 | [current certificate](../n338.cert) |
| 339 | 18.911307592083 | [current certificate](../n339.cert) |
| 340 | 18.939649632892 | [current certificate](../n340.cert) |
| 341 | 18.951882408720 | [current certificate](../n341.cert) |
| 342 | 18.964706723173 | [certificate](n342.cert) |
| 343 | 18.978232523636 | [current certificate](../n343.cert) |
| 344 | 18.993724691804 | [current certificate](../n344.cert) |
| 345 | 19.000000000000 | grid |
| 346 | 19.000000000000 | grid |
| 347 | 19.000000000000 | grid |
| 348 | 19.000000000000 | grid |
| 349 | 19.000000000000 | grid |
| 350 | 19.000000000000 | grid |
| 351 | 19.000000000000 | grid |
| 352 | 19.000000000000 | grid |
| 353 | 19.000000000000 | grid |
| 354 | 19.000000000000 | grid |
| 355 | 19.000000000000 | grid |
| 356 | 19.000000000000 | grid |
| 357 | 19.000000000000 | grid |
| 358 | 19.000000000000 | grid |
| 359 | 19.000000000000 | grid |
| 360 | 19.000000000000 | grid |
| 361 | 19.000000000000 | grid |
| 362 | 19.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 363 | 19.535533905933 | [certificate](n363.cert) |
| 364 | 19.583782190152 | [current certificate](../n364.cert) |
| 365 | 19.621320343560 | [current certificate](../n365.cert) |
| 366 | 19.656854249493 | [certificate](n366.cert) |
| 367 | 19.692388155426 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 368 | 19.692388155426 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 369 | 19.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 370 | 19.767428349965 | [current certificate](../n370.cert) |
| 371 | 19.822875655533 | [certificate](n371.cert) |
| 372 | 19.822875655562 | [certificate](n372.cert) |
| 373 | 19.823062082838 | [current certificate](../n373.cert) |
| 374 | 19.832356217033 | [current certificate](../n374.cert) |
| 375 | 19.882451030482 | [current certificate](../n375.cert) |
| 376 | 19.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 377 | 19.925720814331 | [current certificate](../n377.cert) |
| 378 | 19.942505611659 | [current certificate](../n378.cert) |
| 379 | 19.953014213942 | [current certificate](../n379.cert) |
| 380 | 19.961601762402 | [current certificate](../n380.cert) |
| 381 | 19.974740439431 | [certificate](n381.cert) |
| 382 | 19.987621153966 | [current certificate](../n382.cert) |
| 383 | 20.000000000000 | grid |
| 384 | 20.000000000000 | grid |
| 385 | 20.000000000000 | grid |
| 386 | 20.000000000000 | grid |
| 387 | 20.000000000000 | grid |
| 388 | 20.000000000000 | grid |
| 389 | 20.000000000000 | grid |
| 390 | 20.000000000000 | grid |
| 391 | 20.000000000000 | grid |
| 392 | 20.000000000000 | grid |
| 393 | 20.000000000000 | grid |
| 394 | 20.000000000000 | grid |
| 395 | 20.000000000000 | grid |
| 396 | 20.000000000000 | grid |
| 397 | 20.000000000000 | grid |
| 398 | 20.000000000000 | grid |
| 399 | 20.000000000000 | grid |
| 400 | 20.000000000000 | grid |
| 401 | 20.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 402 | 20.535533905933 | [certificate](n402.cert) |
| 403 | 20.583782190152 | [current certificate](../n403.cert) |
| 404 | 20.621320343560 | [certificate](n404.cert) |
| 405 | 20.656854249493 | [certificate](n405.cert) |
| 406 | 20.692388155426 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 407 | 20.692388155426 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 408 | 20.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 409 | 20.767428349966 | [certificate](n409.cert) |
| 410 | 20.778174593076 | [certificate](n410.cert) |
| 411 | 20.822875655557 | [certificate](n411.cert) |
| 412 | 20.823062082838 | [certificate](n412.cert) |
| 413 | 20.831663365378 | [certificate](n413.cert) |
| 414 | 20.882451030482 | [certificate](n414.cert) |
| 415 | 20.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 416 | 20.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 417 | 20.942505611684 | [current certificate](../n417.cert) |
| 418 | 20.945240141353 | [current certificate](../n418.cert) |
| 419 | 20.959713620588 | [current certificate](../n419.cert) |
| 420 | 20.974473103465 | [certificate](n420.cert) |
| 421 | 20.982817421775 | [current certificate](../n421.cert) |
| 422 | 20.984021832955 | [current certificate](../n422.cert) |
| 423 | 21.000000000000 | grid |
| 424 | 21.000000000000 | grid |
| 425 | 21.000000000000 | grid |
| 426 | 21.000000000000 | grid |
| 427 | 21.000000000000 | grid |
| 428 | 21.000000000000 | grid |
| 429 | 21.000000000000 | grid |
| 430 | 21.000000000000 | grid |
| 431 | 21.000000000000 | grid |
| 432 | 21.000000000000 | grid |
| 433 | 21.000000000000 | grid |
| 434 | 21.000000000000 | grid |
| 435 | 21.000000000000 | grid |
| 436 | 21.000000000000 | grid |
| 437 | 21.000000000000 | grid |
| 438 | 21.000000000000 | grid |
| 439 | 21.000000000000 | grid |
| 440 | 21.000000000000 | grid |
| 441 | 21.000000000000 | grid |
| 442 | 21.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 443 | 21.535533905933 | [certificate](n443.cert) |
| 444 | 21.583782190152 | [current certificate](../n444.cert) |
| 445 | 21.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 446 | 21.656854249493 | [certificate](n446.cert) |
| 447 | 21.692388155426 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 448 | 21.692388155426 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 449 | 21.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 450 | 21.767428349966 | [certificate](n450.cert) |
| 451 | 21.778174593076 | [certificate](n451.cert) |
| 452 | 21.778174593086 | [current certificate](../n452.cert) |
| 453 | 21.823014758318 | [certificate](n453.cert) |
| 454 | 21.828427124844 | [certificate](n454.cert) |
| 455 | 21.882451030482 | [certificate](n455.cert) |
| 456 | 21.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 457 | 21.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 458 | 21.942505611689 | [current certificate](../n458.cert) |
| 459 | 21.943735551416 | [current certificate](../n459.cert) |
| 460 | 21.957651945776 | [current certificate](../n460.cert) |
| 461 | 21.972483922352 | [current certificate](../n461.cert) |
| 462 | 21.980759715480 | [current certificate](../n462.cert) |
| 463 | 21.984021832955 | [current certificate](../n463.cert) |
| 464 | 21.988813022694 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0464.cert) |
| 465 | 22.000000000000 | grid |
| 466 | 22.000000000000 | grid |
| 467 | 22.000000000000 | grid |
| 468 | 22.000000000000 | grid |
| 469 | 22.000000000000 | grid |
| 470 | 22.000000000000 | grid |
| 471 | 22.000000000000 | grid |
| 472 | 22.000000000000 | grid |
| 473 | 22.000000000000 | grid |
| 474 | 22.000000000000 | grid |
| 475 | 22.000000000000 | grid |
| 476 | 22.000000000000 | grid |
| 477 | 22.000000000000 | grid |
| 478 | 22.000000000000 | grid |
| 479 | 22.000000000000 | grid |
| 480 | 22.000000000000 | grid |
| 481 | 22.000000000000 | grid |
| 482 | 22.000000000000 | grid |
| 483 | 22.000000000000 | grid |
| 484 | 22.000000000000 | grid |
| 485 | 22.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 486 | 22.535533905933 | [certificate](n486.cert) |
| 487 | 22.583782190178 | [certificate](n487.cert) |
| 488 | 22.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 489 | 22.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 490 | 22.656854249519 | [certificate](n490.cert) |
| 491 | 22.692388155426 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 492 | 22.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 493 | 22.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 494 | 22.778174593076 | [certificate](n494.cert) |
| 495 | 22.778174593079 | [certificate](n495.cert) |
| 496 | 22.823014758318 | [certificate](n496.cert) |
| 497 | 22.828427124774 | [certificate](n497.cert) |
| 498 | 22.828427124827 | [certificate](n498.cert) |
| 499 | 22.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 500 | 22.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 501 | 22.933763683699 | [current certificate](../n501.cert) |
| 502 | 22.942809041609 | [certificate](n502.cert) |
| 503 | 22.957558542542 | [current certificate](../n503.cert) |
| 504 | 22.970562748504 | [certificate](n504.cert) |
| 505 | 22.972317735354 | [current certificate](../n505.cert) |
| 506 | 22.973102824304 | [certificate](n506.cert) |
| 507 | 22.973760910106 | [certificate](n507.cert) |
| 508 | 22.987759965313 | [certificate](n508.cert) |
| 509 | 22.994328036438 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0509.cert) |
| 510 | 23.000000000000 | grid |
| 511 | 23.000000000000 | grid |
| 512 | 23.000000000000 | grid |
| 513 | 23.000000000000 | grid |
| 514 | 23.000000000000 | grid |
| 515 | 23.000000000000 | grid |
| 516 | 23.000000000000 | grid |
| 517 | 23.000000000000 | grid |
| 518 | 23.000000000000 | grid |
| 519 | 23.000000000000 | grid |
| 520 | 23.000000000000 | grid |
| 521 | 23.000000000000 | grid |
| 522 | 23.000000000000 | grid |
| 523 | 23.000000000000 | grid |
| 524 | 23.000000000000 | grid |
| 525 | 23.000000000000 | grid |
| 526 | 23.000000000000 | grid |
| 527 | 23.000000000000 | grid |
| 528 | 23.000000000000 | grid |
| 529 | 23.000000000000 | grid |
| 530 | 23.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 531 | 23.535533905933 | [certificate](n531.cert) |
| 532 | 23.583782190178 | [certificate](n532.cert) |
| 533 | 23.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 534 | 23.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 535 | 23.656854249519 | [certificate](n535.cert) |
| 536 | 23.677669529701 | [current certificate](../n536.cert) |
| 537 | 23.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 538 | 23.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 539 | 23.778174593076 | [certificate](n539.cert) |
| 540 | 23.778174593079 | [certificate](n540.cert) |
| 541 | 23.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 542 | 23.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 543 | 23.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 544 | 23.828427124775 | [certificate](n544.cert) |
| 545 | 23.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 546 | 23.933763683699 | [current certificate](../n546.cert) |
| 547 | 23.942809041643 | [current certificate](../n547.cert) |
| 548 | 23.957558542543 | [current certificate](../n548.cert) |
| 549 | 23.961513018469 | [certificate](n550.cert) (deletion) |
| 550 | 23.961513018469 | [certificate](n550.cert) |
| 551 | 23.966898919633 | [current certificate](../n551.cert) |
| 552 | 23.966901721108 | [certificate](n552.cert) |
| 553 | 23.981588093282 | [current certificate](../n553.cert) |
| 554 | 23.993653790591 | [current certificate](../n554.cert) |
| 555 | 23.993653790591 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0555.cert) |
| 556 | 24.000000000000 | grid |
| 557 | 24.000000000000 | grid |
| 558 | 24.000000000000 | grid |
| 559 | 24.000000000000 | grid |
| 560 | 24.000000000000 | grid |
| 561 | 24.000000000000 | grid |
| 562 | 24.000000000000 | grid |
| 563 | 24.000000000000 | grid |
| 564 | 24.000000000000 | grid |
| 565 | 24.000000000000 | grid |
| 566 | 24.000000000000 | grid |
| 567 | 24.000000000000 | grid |
| 568 | 24.000000000000 | grid |
| 569 | 24.000000000000 | grid |
| 570 | 24.000000000000 | grid |
| 571 | 24.000000000000 | grid |
| 572 | 24.000000000000 | grid |
| 573 | 24.000000000000 | grid |
| 574 | 24.000000000000 | grid |
| 575 | 24.000000000000 | grid |
| 576 | 24.000000000000 | grid |
| 577 | 24.535533905933 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 578 | 24.535533905933 | [certificate](n578.cert) |
| 579 | 24.583782190178 | [certificate](n579.cert) |
| 580 | 24.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 581 | 24.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 582 | 24.656854249519 | [certificate](n582.cert) |
| 583 | 24.677669529693 | [certificate](n584.cert) (deletion) |
| 584 | 24.677669529693 | [certificate](n584.cert) |
| 585 | 24.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 586 | 24.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 587 | 24.778174593079 | [certificate](n587.cert) |
| 588 | 24.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 589 | 24.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 590 | 24.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 591 | 24.828427124775 | [certificate](n591.cert) |
| 592 | 24.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 593 | 24.899494936641 | [certificate](n594.cert) (deletion) |
| 594 | 24.899494936641 | [certificate](n594.cert) |
| 595 | 24.949747468335 | [current certificate](../n595.cert) |
| 596 | 24.949747468335 | [certificate](n596.cert) |
| 597 | 24.961513018469 | [certificate](n597.cert) |
| 598 | 24.962916747309 | [current certificate](../n598.cert) |
| 599 | 24.966901721108 | [certificate](n599.cert) |
| 600 | 24.981585347399 | [current certificate](../n600.cert) |
| 601 | 24.989482347414 | [certificate](n601.cert) |
| 602 | 24.993653790591 | [current certificate](../n602.cert) |
| 603 | 24.995268064197 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0603.cert) |
| 604 | 25.000000000000 | grid |
| 605 | 25.000000000000 | grid |
| 606 | 25.000000000000 | grid |
| 607 | 25.000000000000 | grid |
| 608 | 25.000000000000 | grid |
| 609 | 25.000000000000 | grid |
| 610 | 25.000000000000 | grid |
| 611 | 25.000000000000 | grid |
| 612 | 25.000000000000 | grid |
| 613 | 25.000000000000 | grid |
| 614 | 25.000000000000 | grid |
| 615 | 25.000000000000 | grid |
| 616 | 25.000000000000 | grid |
| 617 | 25.000000000000 | grid |
| 618 | 25.000000000000 | grid |
| 619 | 25.000000000000 | grid |
| 620 | 25.000000000000 | grid |
| 621 | 25.000000000000 | grid |
| 622 | 25.000000000000 | grid |
| 623 | 25.000000000000 | grid |
| 624 | 25.000000000000 | grid |
| 625 | 25.000000000000 | grid |
| 626 | 25.520815280172 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 627 | 25.535533905933 | [certificate](n627.cert) |
| 628 | 25.583782190178 | [certificate](n628.cert) |
| 629 | 25.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 630 | 25.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 631 | 25.656854249519 | [certificate](n631.cert) |
| 632 | 25.677669529693 | [certificate](n633.cert) (deletion) |
| 633 | 25.677669529693 | [certificate](n633.cert) |
| 634 | 25.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 635 | 25.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 636 | 25.727922061358 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 637 | 25.778174593082 | [certificate](n637.cert) |
| 638 | 25.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 639 | 25.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 640 | 25.828427124775 | [certificate](n640.cert) |
| 641 | 25.899494936612 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 642 | 25.899494936641 | [certificate](n643.cert) (deletion) |
| 643 | 25.899494936641 | [certificate](n643.cert) |
| 644 | 25.899494936642 | [certificate](n644.cert) |
| 645 | 25.949747468335 | [certificate](n645.cert) |
| 646 | 25.949747468336 | [certificate](n646.cert) |
| 647 | 25.953248543199 | [current certificate](../n647.cert) |
| 648 | 25.966901721108 | [certificate](n648.cert) |
| 649 | 25.976974088403 | [certificate](n649.cert) |
| 650 | 25.982429027496 | [current certificate](../n650.cert) |
| 651 | 25.983790120159 | [current certificate](../n651.cert) |
| 652 | 25.995268064197 | [current certificate](../n652.cert) |
| 653 | 25.996103908965 | [current certificate](../n653.cert) |
| 654 | 25.996103908965 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0654.cert) |
| 655 | 26.000000000000 | grid |
| 656 | 26.000000000000 | grid |
| 657 | 26.000000000000 | grid |
| 658 | 26.000000000000 | grid |
| 659 | 26.000000000000 | grid |
| 660 | 26.000000000000 | grid |
| 661 | 26.000000000000 | grid |
| 662 | 26.000000000000 | grid |
| 663 | 26.000000000000 | grid |
| 664 | 26.000000000000 | grid |
| 665 | 26.000000000000 | grid |
| 666 | 26.000000000000 | grid |
| 667 | 26.000000000000 | grid |
| 668 | 26.000000000000 | grid |
| 669 | 26.000000000000 | grid |
| 670 | 26.000000000000 | grid |
| 671 | 26.000000000000 | grid |
| 672 | 26.000000000000 | grid |
| 673 | 26.000000000000 | grid |
| 674 | 26.000000000000 | grid |
| 675 | 26.000000000000 | grid |
| 676 | 26.000000000000 | grid |
| 677 | 26.520815280172 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 678 | 26.535533905933 | [certificate](n678.cert) |
| 679 | 26.583782190178 | [certificate](n679.cert) |
| 680 | 26.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 681 | 26.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 682 | 26.656854249519 | [certificate](n682.cert) |
| 683 | 26.677669529693 | [certificate](n684.cert) (deletion) |
| 684 | 26.677669529693 | [certificate](n684.cert) |
| 685 | 26.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 686 | 26.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 687 | 26.727922061358 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 688 | 26.727922061358 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 689 | 26.778174593084 | [certificate](n689.cert) |
| 690 | 26.813708498985 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 691 | 26.828427124775 | [certificate](n691.cert) |
| 692 | 26.828427124777 | [certificate](n692.cert) |
| 693 | 26.899494936641 | [certificate](n694.cert) (deletion) |
| 694 | 26.899494936641 | [certificate](n694.cert) |
| 695 | 26.899494936642 | [certificate](n695.cert) |
| 696 | 26.949747468335 | [certificate](n696.cert) |
| 697 | 26.949747468336 | [certificate](n697.cert) |
| 698 | 26.949747468338 | [certificate](n698.cert) |
| 699 | 26.949747468415 | [certificate](n699.cert) |
| 700 | 26.972996848621 | [current certificate](../n700.cert) |
| 701 | 26.975561031531 | [current certificate](../n701.cert) |
| 702 | 26.977494114977 | [current certificate](../n702.cert) |
| 703 | 26.987493360751 | [current certificate](../n703.cert) |
| 704 | 26.996103908965 | [current certificate](../n704.cert) |
| 705 | 26.996103908965 | [current certificate](../n705.cert) |
| 706 | 26.998712100405 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0706.cert) |
| 707 | 27.000000000000 | grid |
| 708 | 27.000000000000 | grid |
| 709 | 27.000000000000 | grid |
| 710 | 27.000000000000 | grid |
| 711 | 27.000000000000 | grid |
| 712 | 27.000000000000 | grid |
| 713 | 27.000000000000 | grid |
| 714 | 27.000000000000 | grid |
| 715 | 27.000000000000 | grid |
| 716 | 27.000000000000 | grid |
| 717 | 27.000000000000 | grid |
| 718 | 27.000000000000 | grid |
| 719 | 27.000000000000 | grid |
| 720 | 27.000000000000 | grid |
| 721 | 27.000000000000 | grid |
| 722 | 27.000000000000 | grid |
| 723 | 27.000000000000 | grid |
| 724 | 27.000000000000 | grid |
| 725 | 27.000000000000 | grid |
| 726 | 27.000000000000 | grid |
| 727 | 27.000000000000 | grid |
| 728 | 27.000000000000 | grid |
| 729 | 27.000000000000 | grid |
| 730 | 27.520815280172 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 731 | 27.535533905933 | [certificate](n731.cert) |
| 732 | 27.583782190178 | [certificate](n732.cert) |
| 733 | 27.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 734 | 27.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 735 | 27.656854249519 | [current certificate](../n735.cert) |
| 736 | 27.656854249525 | [certificate](n736.cert) |
| 737 | 27.677669529693 | [certificate](n737.cert) |
| 738 | 27.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 739 | 27.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 740 | 27.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 741 | 27.727922061358 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 742 | 27.778174593084 | [certificate](n742.cert) |
| 743 | 27.798989873256 | [certificate](n744.cert) (deletion) |
| 744 | 27.798989873256 | [certificate](n744.cert) |
| 745 | 27.828427124777 | [certificate](n745.cert) |
| 746 | 27.828427124795 | [certificate](n746.cert) |
| 747 | 27.899494936641 | [certificate](n747.cert) |
| 748 | 27.899494936642 | [certificate](n748.cert) |
| 749 | 27.925883089331 | [current certificate](../n749.cert) |
| 750 | 27.928780276056 | [certificate](n750.cert) |
| 751 | 27.935028842545 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 752 | 27.935028842545 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 753 | 27.937423518013 | [current certificate](../n753.cert) |
| 754 | 27.937423518013 | [current certificate](../n754.cert) |
| 755 | 27.952229334413 | [certificate](n755.cert) |
| 756 | 27.984237490911 | [current certificate](../n756.cert) |
| 757 | 27.989936988207 | [current certificate](../n757.cert) |
| 758 | 27.994980212536 | [current certificate](../n758.cert) |
| 759 | 27.995949340329 | [current certificate](../n759.cert) |
| 760 | 27.995949340329 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0760.cert) |
| 761 | 28.000000000000 | grid |
| 762 | 28.000000000000 | grid |
| 763 | 28.000000000000 | grid |
| 764 | 28.000000000000 | grid |
| 765 | 28.000000000000 | grid |
| 766 | 28.000000000000 | grid |
| 767 | 28.000000000000 | grid |
| 768 | 28.000000000000 | grid |
| 769 | 28.000000000000 | grid |
| 770 | 28.000000000000 | grid |
| 771 | 28.000000000000 | grid |
| 772 | 28.000000000000 | grid |
| 773 | 28.000000000000 | grid |
| 774 | 28.000000000000 | grid |
| 775 | 28.000000000000 | grid |
| 776 | 28.000000000000 | grid |
| 777 | 28.000000000000 | grid |
| 778 | 28.000000000000 | grid |
| 779 | 28.000000000000 | grid |
| 780 | 28.000000000000 | grid |
| 781 | 28.000000000000 | grid |
| 782 | 28.000000000000 | grid |
| 783 | 28.000000000000 | grid |
| 784 | 28.000000000000 | grid |
| 785 | 28.520815280172 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 786 | 28.535533905933 | [certificate](n786.cert) |
| 787 | 28.583782190178 | [certificate](n787.cert) |
| 788 | 28.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 789 | 28.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 790 | 28.656854249519 | [certificate](n790.cert) |
| 791 | 28.656854249525 | [certificate](n791.cert) |
| 792 | 28.656854249526 | [certificate](n792.cert) |
| 793 | 28.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 794 | 28.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 795 | 28.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 796 | 28.727922061358 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 797 | 28.778174593084 | [certificate](n797.cert) |
| 798 | 28.798989873256 | [certificate](n799.cert) (deletion) |
| 799 | 28.798989873256 | [certificate](n799.cert) |
| 800 | 28.798989873257 | [certificate](n800.cert) |
| 801 | 28.828427124795 | [certificate](n801.cert) |
| 802 | 28.828427124817 | [certificate](n802.cert) |
| 803 | 28.899494936642 | [certificate](n803.cert) |
| 804 | 28.917335789888 | [current certificate](../n804.cert) |
| 805 | 28.921843659464 | [current certificate](../n805.cert) |
| 806 | 28.921843662228 | [current certificate](../n806.cert) |
| 807 | 28.933881004714 | [certificate](n808.cert) (deletion) |
| 808 | 28.933881004714 | [certificate](n808.cert) |
| 809 | 28.937423518015 | [current certificate](../n809.cert) |
| 810 | 28.951463124704 | [certificate](n810.cert) |
| 811 | 28.982472918533 | [current certificate](../n811.cert) |
| 812 | 28.982472918533 | [current certificate](../n812.cert) |
| 813 | 28.990394020145 | [current certificate](../n813.cert) |
| 814 | 28.995949340329 | [current certificate](../n814.cert) |
| 815 | 28.995949340329 | [current certificate](../n815.cert) |
| 816 | 28.998488480775 | [current certificate](../n816.cert) |
| 817 | 28.998488480775 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0817.cert) |
| 818 | 29.000000000000 | grid |
| 819 | 29.000000000000 | grid |
| 820 | 29.000000000000 | grid |
| 821 | 29.000000000000 | grid |
| 822 | 29.000000000000 | grid |
| 823 | 29.000000000000 | grid |
| 824 | 29.000000000000 | grid |
| 825 | 29.000000000000 | grid |
| 826 | 29.000000000000 | grid |
| 827 | 29.000000000000 | grid |
| 828 | 29.000000000000 | grid |
| 829 | 29.000000000000 | grid |
| 830 | 29.000000000000 | grid |
| 831 | 29.000000000000 | grid |
| 832 | 29.000000000000 | grid |
| 833 | 29.000000000000 | grid |
| 834 | 29.000000000000 | grid |
| 835 | 29.000000000000 | grid |
| 836 | 29.000000000000 | grid |
| 837 | 29.000000000000 | grid |
| 838 | 29.000000000000 | grid |
| 839 | 29.000000000000 | grid |
| 840 | 29.000000000000 | grid |
| 841 | 29.000000000000 | grid |
| 842 | 29.520815280172 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 843 | 29.535533905933 | [certificate](n843.cert) |
| 844 | 29.583782190178 | [certificate](n844.cert) |
| 845 | 29.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 846 | 29.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 847 | 29.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 848 | 29.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 849 | 29.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) |
| 850 | 29.656854249528 | [certificate](n850.cert) |
| 851 | 29.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 852 | 29.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 853 | 29.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 854 | 29.778174593084 | [certificate](n854.cert) |
| 855 | 29.798989873256 | [certificate](n856.cert) (deletion) |
| 856 | 29.798989873256 | [certificate](n856.cert) |
| 857 | 29.798989873257 | [certificate](n857.cert) |
| 858 | 29.828427124795 | [current certificate](../n858.cert) |
| 859 | 29.828427124807 | [certificate](n859.cert) |
| 860 | 29.849242404918 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 861 | 29.849242404918 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 862 | 29.899494936647 | [certificate](n862.cert) |
| 863 | 29.921843659464 | [current certificate](../n863.cert) |
| 864 | 29.933881004714 | [certificate](n865.cert) (deletion) |
| 865 | 29.933881004714 | [certificate](n865.cert) |
| 866 | 29.935764472087 | [current certificate](../n866.cert) |
| 867 | 29.950265025802 | [current certificate](../n867.cert) |
| 868 | 29.982204111182 | [current certificate](../n868.cert) |
| 869 | 29.982472918533 | [current certificate](../n869.cert) |
| 870 | 29.985969207342 | [current certificate](../n870.cert) |
| 871 | 29.989329079687 | [current certificate](../n871.cert) |
| 872 | 29.995949340329 | [current certificate](../n872.cert) |
| 873 | 29.998488480775 | [current certificate](../n873.cert) |
| 874 | 29.998488480775 | [current certificate](../n874.cert) |
| 875 | 29.998783733108 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0875.cert) |
| 876 | 30.000000000000 | grid |
| 877 | 30.000000000000 | grid |
| 878 | 30.000000000000 | grid |
| 879 | 30.000000000000 | grid |
| 880 | 30.000000000000 | grid |
| 881 | 30.000000000000 | grid |
| 882 | 30.000000000000 | grid |
| 883 | 30.000000000000 | grid |
| 884 | 30.000000000000 | grid |
| 885 | 30.000000000000 | grid |
| 886 | 30.000000000000 | grid |
| 887 | 30.000000000000 | grid |
| 888 | 30.000000000000 | grid |
| 889 | 30.000000000000 | grid |
| 890 | 30.000000000000 | grid |
| 891 | 30.000000000000 | grid |
| 892 | 30.000000000000 | grid |
| 893 | 30.000000000000 | grid |
| 894 | 30.000000000000 | grid |
| 895 | 30.000000000000 | grid |
| 896 | 30.000000000000 | grid |
| 897 | 30.000000000000 | grid |
| 898 | 30.000000000000 | grid |
| 899 | 30.000000000000 | grid |
| 900 | 30.000000000000 | grid |
| 901 | 30.520815280172 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 902 | 30.535533905933 | [certificate](n902.cert) |
| 903 | 30.583782190178 | [certificate](n903.cert) |
| 904 | 30.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 905 | 30.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 906 | 30.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 907 | 30.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 908 | 30.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 909 | 30.656854249528 | [certificate](n909.cert) |
| 910 | 30.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 911 | 30.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 912 | 30.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) + L borders |
| 913 | 30.778174593084 | [certificate](n913.cert) |
| 914 | 30.778174593089 | [certificate](n914.cert) |
| 915 | 30.798989873256 | [certificate](n915.cert) |
| 916 | 30.798989873257 | [certificate](n916.cert) |
| 917 | 30.828427124795 | [certificate](n917.cert) |
| 918 | 30.828427124807 | [current certificate](../n918.cert) |
| 919 | 30.849242404918 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 920 | 30.849242404918 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 921 | 30.849242404918 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 922 | 30.899494936660 | [current certificate](../n922.cert) |
| 923 | 30.933766814037 | [certificate](n924.cert) (deletion) |
| 924 | 30.933766814037 | [certificate](n924.cert) |
| 925 | 30.935764472087 | [current certificate](../n925.cert) |
| 926 | 30.949634321517 | [current certificate](../n926.cert) |
| 927 | 30.976993727283 | [current certificate](../n927.cert) |
| 928 | 30.976993727283 | [current certificate](../n928.cert) |
| 929 | 30.978848462737 | [current certificate](../n929.cert) |
| 930 | 30.982052182975 | [current certificate](../n930.cert) |
| 931 | 30.989936243547 | [current certificate](../n931.cert) |
| 932 | 30.995955854834 | [current certificate](../n932.cert) |
| 933 | 30.995955854834 | [current certificate](../n933.cert) |
| 934 | 30.995955854834 | [current certificate](../n934.cert) |
| 935 | 30.995955854834 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0935.cert) |
| 936 | 31.000000000000 | grid |
| 937 | 31.000000000000 | grid |
| 938 | 31.000000000000 | grid |
| 939 | 31.000000000000 | grid |
| 940 | 31.000000000000 | grid |
| 941 | 31.000000000000 | grid |
| 942 | 31.000000000000 | grid |
| 943 | 31.000000000000 | grid |
| 944 | 31.000000000000 | grid |
| 945 | 31.000000000000 | grid |
| 946 | 31.000000000000 | grid |
| 947 | 31.000000000000 | grid |
| 948 | 31.000000000000 | grid |
| 949 | 31.000000000000 | grid |
| 950 | 31.000000000000 | grid |
| 951 | 31.000000000000 | grid |
| 952 | 31.000000000000 | grid |
| 953 | 31.000000000000 | grid |
| 954 | 31.000000000000 | grid |
| 955 | 31.000000000000 | grid |
| 956 | 31.000000000000 | grid |
| 957 | 31.000000000000 | grid |
| 958 | 31.000000000000 | grid |
| 959 | 31.000000000000 | grid |
| 960 | 31.000000000000 | grid |
| 961 | 31.000000000000 | grid |
| 962 | 31.520815280172 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 963 | 31.535533905933 | [certificate](n963.cert) |
| 964 | 31.556349186105 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) |
| 965 | 31.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 966 | 31.606601717799 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 967 | 31.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 968 | 31.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 969 | 31.642135623731 | [source](https://github.com/jlevy/squares/blob/c593e2bfd0a5da50d0d69a93b6897722a54ddb82/packing/cases/gobel_offcentre/packing.py) + L borders |
| 970 | 31.656854249528 | [certificate](n970.cert) |
| 971 | 31.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 972 | 31.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 973 | 31.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 974 | 31.707106781187 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html) |
| 975 | 31.778174593089 | [certificate](n975.cert) |
| 976 | 31.778174593090 | [certificate](n976.cert) |
| 977 | 31.798989873257 | [certificate](n977.cert) |
| 978 | 31.828427124795 | [certificate](n978.cert) |
| 979 | 31.828427124802 | [certificate](n980.cert) (deletion) |
| 980 | 31.828427124802 | [certificate](n980.cert) |
| 981 | 31.849242404918 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 982 | 31.849242404918 | [source](https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html) + L borders |
| 983 | 31.899494936650 | [certificate](n983.cert) |
| 984 | 31.920310216821 | [certificate](n984.cert) |
| 985 | 31.920310216821 | [certificate](n986.cert) (deletion) |
| 986 | 31.920310216821 | [certificate](n986.cert) |
| 987 | 31.949634321517 | [current certificate](../n987.cert) |
| 988 | 31.949747468406 | [certificate](n988.cert) |
| 989 | 31.976993727283 | [current certificate](../n989.cert) |
| 990 | 31.978848462737 | [current certificate](../n990.cert) |
| 991 | 31.982052182975 | [current certificate](../n991.cert) |
| 992 | 31.985130163599 | [current certificate](../n992.cert) |
| 993 | 31.985130163599 | [current certificate](../n993.cert) |
| 994 | 31.995955854834 | [current certificate](../n994.cert) |
| 995 | 31.995955854834 | [current certificate](../n995.cert) |
| 996 | 31.995955854834 | [current certificate](../n996.cert) |
| 997 | 31.998349747355 | [current certificate](../n997.cert) |
| 998 | 31.998349747355 | [source](https://github.com/JoostdeWinter/joostdewinter.github.io/blob/b3152f526f23bc3ae450e51b6e906841233086d1/square-packing-above-324/n0998.cert) |
| 999 | 32.000000000000 | grid |
| 1000 | 32.000000000000 | grid |
| 1001 | 32.000000000000 | grid |
| 1002 | 32.000000000000 | grid |
| 1003 | 32.000000000000 | grid |
| 1004 | 32.000000000000 | grid |
| 1005 | 32.000000000000 | grid |
| 1006 | 32.000000000000 | grid |
| 1007 | 32.000000000000 | grid |
| 1008 | 32.000000000000 | grid |
| 1009 | 32.000000000000 | grid |
| 1010 | 32.000000000000 | grid |
| 1011 | 32.000000000000 | grid |
| 1012 | 32.000000000000 | grid |
| 1013 | 32.000000000000 | grid |
| 1014 | 32.000000000000 | grid |
| 1015 | 32.000000000000 | grid |
| 1016 | 32.000000000000 | grid |
| 1017 | 32.000000000000 | grid |
| 1018 | 32.000000000000 | grid |
| 1019 | 32.000000000000 | grid |
| 1020 | 32.000000000000 | grid |
| 1021 | 32.000000000000 | grid |
| 1022 | 32.000000000000 | grid |
| 1023 | 32.000000000000 | grid |
| 1024 | 32.000000000000 | grid |
