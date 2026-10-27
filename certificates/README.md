# Certificates

One certificate per packing `nN.txt` in this repository, in Evan Daniel's format
([evand/square-packing](https://github.com/evand/square-packing), MIT): `n S`, then one line per
square with a rational centre (x, y) and t = tan(θ/2), so that (cos θ, sin θ) = ((1−t²)/(1+t²),
2t/(1+t²)) and every square is exactly a unit square inside the closed box [0, S]², with disjoint square interiors. Each proves s(n) ≤ S.

Where provided, `nN.json` records the current packing and certificate hashes, exact bound, and seed credit.
Current certificates and provenance are listed here. Superseded parent certificates remain in `parents/` and Git history.

- **exact optimum**: written by Evan Daniel's exact contact solver (`search/exact`, commit 77f3c0ab);
  S lies within about 1e-19 of the packing's exact KKT point.
- **rational witness**: the decimal packing as rationals, with an adaptive rational dilation of
  the centres, where the exact solve did not certify a smaller side. The dilation starts at
  1+1e-12 and increases until exact verification succeeds; the amount varies by certificate.

Replay exact closed-container feasibility from this repository (standard library only):

```sh
python3 verify_bound_certificate.py certificates/nN.cert
```

Use `--strict` to additionally require an open container and disjoint closed squares,
as in Evan Daniel's original verifier. Exact L borders can have touching edges and
walls; their default closed-container verdict proves the packing bound.

Every certificate also replays as valid in exact rational arithmetic with `verify.py` from
[jlevy/squares](https://github.com/jlevy/squares) (`sqpack.verify`). The standing is against the
jlevy/squares register and verified published submissions, as in the README. Above n=324,
the comparison is with reviewed published bounds where available, otherwise only with
the frozen derived reference; it is not an optimality claim.

The canonical upper-bound index covers every n through 10,000. Source and construction credits are retained in `best/manifest.json` and each certificate metadata file.

| n | S (exact) | rounded up | certificate | source credit | SHA-256 |
|---:|---|---|---|---|---|
| 68 | `4399397618609141951332334459697/500000000000000000000000000000` | 8.798795237219 | [certificate](n68.cert) | source credits in metadata | `c52392c260140708` |
| 106 | `10822908044132847555194436943331/1000000000000000000000000000000` | 10.822908044133 | [certificate](n106.cert) | source credits in metadata | `186d69780b5cfbac` |
| 110 | `10996783396631591639612746267957/1000000000000000000000000000000` | 10.996783396632 | [certificate](n110.cert) | source credits in metadata | `91e46c27e6252f87` |
| 130 | `466915711841738962256077475351530705109199164124122993/39228601764570445403995003040207131754000000000000000` | 11.902430645985 | [certificate](n130.cert) | Francisco Couzo (square-packing live search); refines the packing of PingYou Ltd (BuddenPing); earlier construction credits retained; earlier seed and construction credits retained in provenance | `a2618e1a7a2961cf` |
| 152 | `3207679700244152488748455910853/250000000000000000000000000000` | 12.830718800977 | [certificate](n152.cert) | source credits in metadata | `0ef3fca3ad11bacf` |
| 156 | `12979165853834276453965882038847/1000000000000000000000000000000` | 12.979165853835 | [certificate](n156.cert) | Daniil Ostashev | `1b4dfa721e3289c9` |
| 172 | `340474723922484960724992287973/25000000000000000000000000000` | 13.618988956900 | [certificate](n172.cert) | source credits in metadata | `62ff74ec0426b151` |
| 177 | `13822979734169448600231882896281/1000000000000000000000000000000` | 13.822979734170 | [certificate](n177.cert) | source credits in metadata | `522383966164b4b0` |
| 206 | `232189979115498488075628916091/15625000000000000000000000000` | 14.860158663392 | [certificate](n206.cert) | source credits in metadata | `2167021c418c9689` |
| 210 | `3743250279146906435495754512617/250000000000000000000000000000` | 14.973001116588 | [certificate](n210.cert) | source credits in metadata | `85648fe7d80c9486` |
| 211 | `7496774813149710519467765230441/500000000000000000000000000000` | 14.993549626300 | [certificate](n211.cert) | Francisco Couzo | `806a37e2dd5b7c60` |
| 227 | `7781812826162574542396221861851/500000000000000000000000000000` | 15.563625652326 | [certificate](n227.cert) | Francisco Couzo (franciscouzo) | `52f9fbf2fb302031` |
| 237 | `7951301819129798440089572127137/500000000000000000000000000000` | 15.902603638260 | [certificate](n237.cert) | Francisco Couzo | `e367f769988aaa47` |
| 240 | `7984842668765390168028037160291/500000000000000000000000000000` | 15.969685337531 | [certificate](n240.cert) | source credits in metadata | `7e76b3cce42829f0` |
| 241 | `15987117095150238758321758129189/1000000000000000000000000000000` | 15.987117095151 | [certificate](n241.cert) | Francisco Couzo | `add404b34276f4ce` |
| 260 | `4161438312629953048686574163329/250000000000000000000000000000` | 16.645753250520 | [certificate](n260.cert) | Francisco Couzo (franciscouzo) | `ba7b521b15d086f1` |
| 267 | `4209703817487065565108620335551/250000000000000000000000000000` | 16.838815269949 | [certificate](n267.cert) | Ryan Xu | `711814d2d7ca078d` |
| 268 | `8437180857934672912242411148233/500000000000000000000000000000` | 16.874361715870 | [certificate](n268.cert) | Evan Daniel; earlier seed and construction credits retained in provenance | `c87da316589dd384` |
| 273 | `16983925962650404316108837346991/1000000000000000000000000000000` | 16.983925962651 | [certificate](n273.cert) | source credits in metadata | `405171da4809f61b` |
| 297 | `221755216094297523139415072097/12500000000000000000000000000` | 17.740417287544 | [certificate](n297.cert) | source credits in metadata | `9efe45053a36bba4` |
| 301 | `17846667192843489783121781262887/1000000000000000000000000000000` | 17.846667192844 | [certificate](n301.cert) | source credits in metadata | `55090ed78b6e9688` |
| 302 | `3574002770080892868927770707857/200000000000000000000000000000` | 17.870013850405 | [certificate](n302.cert) | BuddenPing | `834837d0693624c4` |
| 306 | `8981716858745712869796920037761/500000000000000000000000000000` | 17.963433717492 | [certificate](n306.cert) | source credits in metadata | `f58de39d385fcc00` |
| 336 | `18825571499861668938686306400451/1000000000000000000000000000000` | 18.825571499862 | [certificate](n336.cert) | Francisco Couzo | `08f1dafe436d44ba` |
| 337 | `3771678353527245620694257618907/200000000000000000000000000000` | 18.858391767637 | [certificate](n337.cert) | Francisco Couzo | `2bcf92a216a88380` |
| 340 | `75375865612922446301687569606954711302688177170345281/3982473093438747882466958721603362497000000000000000` | 18.926898900361 | [certificate](n340.cert) | Francisco Couzo (square-packing live search); refines the packing of Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3; earlier construction credits retained; earlier seed and construction credits retained in provenance | `0b3316697d3ef6a4` |
| 374 | `19832356217032762224853652799723/1000000000000000000000000000000` | 19.832356217033 | [certificate](n374.cert) | Francisco Couzo | `e46d218321a2ba49` |
| 465 | `11381963121791634297027591853202848406820941591819292633723829868728208613327540197717763909/517364402872842820091676921462723497551810647082106513813856525534732746752000000000000000` | 21.999896124646 | [certificate](n465.cert) | Francisco Couzo (square-packing live search); earlier construction credits retained; earlier seed and construction credits retained in provenance | `72d8111d34b9cf2c` |
| 552 | `29850248138483371247641167101336161312715703769174003096078538075763/1246531156408590782246242412465311564085907822462424000000000000000` | 23.946652263780 | [certificate](n552.cert) | Francisco Couzo (square-packing live search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `82d11374ef373124` |
| 679 | `191147160352286353844073274581/7203441281033000000000000000` | 26.535533905939 | [certificate](n679.cert) | Francisco Couzo (square-packing live search); refines the packing of Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3; earlier construction credits retained; earlier seed and construction credits retained in provenance | `7095162f352b6b1b` |
| 704 | `285835818447793989634635767070508175928477340806413441120239846749054265838875766028691467/10600156778938142755076137559124460414455199673909808231303438926520940814375000000000000` | 26.965244421265 | [certificate](n704.cert) | Francisco Couzo (square-packing live search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `a680fb01cf8fb610` |
| 732 | `198350601633319353844073274581/7203441281033000000000000000` | 27.535533905939 | [certificate](n732.cert) | Francisco Couzo (square-packing live search); refines the packing of Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3; earlier construction credits retained; earlier seed and construction credits retained in provenance | `e17a8acffe74e480` |
| 787 | `205554042914352353844073274581/7203441281033000000000000000` | 28.535533905939 | [certificate](n787.cert) | Francisco Couzo (square-packing live search); refines the packing of Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3; earlier construction credits retained; earlier seed and construction credits retained in provenance | `20b7c30f87d5689d` |
| 844 | `212757484195385353844073274581/7203441281033000000000000000` | 29.535533905939 | [certificate](n844.cert) | Francisco Couzo (square-packing live search); refines the packing of Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3; earlier construction credits retained; earlier seed and construction credits retained in provenance | `0da6b2b2067ba391` |
| 850 | `5067207364951307925873256989/170861255962000000000000000` | 29.656854249499 | [certificate](n850.cert) | franciscouzo; earlier seed and construction credits retained in provenance | `6f005673962cf31d` |
| 903 | `219960925476418353844073274581/7203441281033000000000000000` | 30.535533905939 | [certificate](n903.cert) | Francisco Couzo (square-packing live search); refines the packing of Kirill Tymchishin (kirilltym), Kaggle "CPU Alternating Reclosure" v3; earlier construction credits retained; earlier seed and construction credits retained in provenance | `fd6baf6e86044dc5` |
| 1335 | `69180562063073403153103677/1870246752032600000000000` | 36.990072025463 | [certificate](n1335.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `ca738797bb61bf8e` |
| 1486 | `4235477124275102347031803538168655964408914858790200769/108611527834200000000000001086115278342000000000000000` | 38.996570702336 | [certificate](n1486.cert) | Francisco Couzo; earlier seed and construction credits retained in provenance | `36add1a6388cd489` |
| 1647 | `23087243529118941808278952977153558388256498296206178093458849919079/563131386416725665519693275631313864167256655196932700000000000000` | 40.997969720754 | [certificate](n1647.cert) | Francisco Couzo; earlier seed and construction credits retained in provenance | `03f93d8c26143a0d` |
| 1648 | `65221011849834736302117874047/1590800062429400000000000000` | 40.998874333857 | [certificate](n1648.cert) | Francisco Couzo; earlier seed and construction credits retained in provenance | `79a816e9d6346068` |
| 1727 | `23650374915535667473798646252784872252423754951403110793458849919079/563131386416725665519693275631313864167256655196932700000000000000` | 41.997969720754 | [certificate](n1727.cert) | Francisco Couzo; earlier seed and construction credits retained in provenance | `fb71ad2a3468d606` |
| 1729 | `66811811912264136302117874047/1590800062429400000000000000` | 41.998874333857 | [certificate](n1729.cert) | Francisco Couzo; earlier seed and construction credits retained in provenance | `5d991ca27922bde3` |
| 1765 | `28002119135132679255274383527643925803305409802580272891578078111571/659064374869358231070691056590643748693582310706910500000000000000` | 42.487684364192 | [certificate](n1765.cert) | Francisco Couzo; earlier seed and construction credits retained in provenance | `96c6b2737631dbe3` |
| 1811 | `26690023882286124942107676633076597119801989844698792987461/620733593710348110512795920177407651091556010000000000000` | 42.997550241724 | [certificate](n1811.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `350a59699a1cc3c0` |
| 1812 | `787528855106674213208378207/18315646727698000000000000` | 42.997600183876 | [certificate](n1812.cert) | Francisco Couzo (assembly/refinement); original piece credits below | `1e44fc204930db7c` |
| 1898 | `1881688907605905763867111254699862714245700769187979443427397043217963911077181034144079293727/42766369135411921538421572379861791854202716736665819521981005000835013524501000000000000000` | 43.999267313246 | [certificate](n1898.cert) | franciscouzo; earlier seed and construction credits retained in provenance | `643346dda50a8c4f` |
| 1899 | `517924629878249153438091073/11771191786670000000000000` | 43.999336623227 | [certificate](n1899.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `8853c28c411e4bf1` |
| 1986 | `47869529575182805705518307/1063824056829000000000000` | 44.997600183879 | [certificate](n1986.cert) | Francisco Couzo (assembly/refinement); original piece credits below | `5f048fc21d41f585` |
| 2043 | `145304373451793524547773799/3179825677852400000000000` | 45.695704158830 | [certificate](n2043.cert) | Francisco Couzo (refinement); source packing from David Ellsworth's catalogue | `42332981f239b949` |
| 2076 | `29130830406233127489905240398774884295278107346819466218439/633312649352684127964061139516880492261539840000000000000` | 45.997550240009 | [certificate](n2076.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `47ec4dede18be997` |
| 2263 | `30617400428198710497186966269318024505664216456845197992974335083908379350713824142786336449/637873910819029501539219542901750492570270836037356298896547761887504534960950000000000000` | 47.999142007370 | [certificate](n2263.cert) | Francisco Couzo; earlier seed and construction credits retained in provenance | `abfb481218015e8c` |
| 2359 | `252280942751164369822816412209811129246428818461896133435439/5148848082462948672066472024902262050820758314000000000000` | 48.997550269630 | [certificate](n2359.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `9c69c6a5b0a05a9e` |
| 4168 | `3729788233335631310328887/57382014034000000000000` | 64.999256232549 | [certificate](n4168.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `7825d5b5de55b241` |
| 4430 | `209136601175925015045231997/3121555943722000000000000` | 66.997550243025 | [certificate](n4430.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `cebf53e683c4f571` |
| 4701 | `294504398156394757784167948884668665074553701042901008803/4268225692470045092528403740792512589607661800000000000` | 68.999256219267 | [certificate](n4701.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `2f68f378cdc77f25` |
| 4839 | `120908228810017505243798476902557645294661024627063650865567/1727320861578185453400474108282500927721570304000000000000` | 69.997550252215 | [certificate](n4839.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `d0e1d8105e309df3` |
| 8021 | `117283440142653980280038009/1303160104529000000000000` | 89.999256219591 | [certificate](n8021.cert) | Francisco Couzo (assembly/refinement); source construction credits retained below | `751f1c7b0862d862` |
