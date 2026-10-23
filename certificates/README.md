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
| 127 | `5905439393794589919821183554001/500000000000000000000000000000` | 11.810878787590 | [certificate](n127.cert) | Ryan Xu | `2e039a654aa7afbe` |
| 152 | `3207679700244152488748455910853/250000000000000000000000000000` | 12.830718800977 | [certificate](n152.cert) | source credits in metadata | `0ef3fca3ad11bacf` |
| 156 | `12979165853834276453965882038847/1000000000000000000000000000000` | 12.979165853835 | [certificate](n156.cert) | Daniil Ostashev | `1b4dfa721e3289c9` |
| 172 | `340474723922484960724992287973/25000000000000000000000000000` | 13.618988956900 | [certificate](n172.cert) | source credits in metadata | `62ff74ec0426b151` |
| 177 | `13822979734169448600231882896281/1000000000000000000000000000000` | 13.822979734170 | [certificate](n177.cert) | source credits in metadata | `522383966164b4b0` |
| 180 | `13916993522477832483558124720393/1000000000000000000000000000000` | 13.916993522478 | [certificate](n180.cert) | Nate Chaoweeraprasit (SQUISH), precision-refined by SidG2k1 | `a66d49e35a3c841d` |
| 182 | `3493522678280359751787532508193/250000000000000000000000000000` | 13.974090713122 | [certificate](n182.cert) | source credits in metadata | `5826ad138cf2c98b` |
| 206 | `232189979115498488075628916091/15625000000000000000000000000` | 14.860158663392 | [certificate](n206.cert) | source credits in metadata | `2167021c418c9689` |
| 209 | `14946223226446451055256712327571/1000000000000000000000000000000` | 14.946223226447 | [certificate](n209.cert) | Nate Chaoweeraprasit (SQUISH) | `1a16e42ebf3dbc66` |
| 210 | `3743250279146906435495754512617/250000000000000000000000000000` | 14.973001116588 | [certificate](n210.cert) | source credits in metadata | `85648fe7d80c9486` |
| 211 | `7496774813149710519467765230441/500000000000000000000000000000` | 14.993549626300 | [certificate](n211.cert) | Francisco Couzo | `806a37e2dd5b7c60` |
| 227 | `7781812826162574542396221861851/500000000000000000000000000000` | 15.563625652326 | [certificate](n227.cert) | Francisco Couzo (franciscouzo) | `52f9fbf2fb302031` |
| 228 | `3901150368932418571180158525547/250000000000000000000000000000` | 15.604601475730 | [certificate](n228.cert) | source credits in metadata | `cb5e49904ac5e4b5` |
| 237 | `7951301819129798440089572127137/500000000000000000000000000000` | 15.902603638260 | [certificate](n237.cert) | Francisco Couzo | `e367f769988aaa47` |
| 240 | `7984842668765390168028037160291/500000000000000000000000000000` | 15.969685337531 | [certificate](n240.cert) | source credits in metadata | `7e76b3cce42829f0` |
| 241 | `15987117095150238758321758129189/1000000000000000000000000000000` | 15.987117095151 | [certificate](n241.cert) | Francisco Couzo | `add404b34276f4ce` |
| 260 | `4161438312629953048686574163329/250000000000000000000000000000` | 16.645753250520 | [certificate](n260.cert) | Francisco Couzo (franciscouzo) | `ba7b521b15d086f1` |
| 267 | `4209703817487065565108620335551/250000000000000000000000000000` | 16.838815269949 | [certificate](n267.cert) | Ryan Xu | `711814d2d7ca078d` |
| 273 | `16983925962650404316108837346991/1000000000000000000000000000000` | 16.983925962651 | [certificate](n273.cert) | source credits in metadata | `405171da4809f61b` |
| 297 | `221755216094297523139415072097/12500000000000000000000000000` | 17.740417287544 | [certificate](n297.cert) | source credits in metadata | `9efe45053a36bba4` |
| 301 | `17846667192843489783121781262887/1000000000000000000000000000000` | 17.846667192844 | [certificate](n301.cert) | source credits in metadata | `55090ed78b6e9688` |
| 302 | `3574002770080892868927770707857/200000000000000000000000000000` | 17.870013850405 | [certificate](n302.cert) | BuddenPing | `834837d0693624c4` |
| 303 | `5814753983527539509183317807407711265481/324711028902771953001378000000000000000` | 17.907473001999 | [certificate](n303.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `22f07a7c318328d2` |
| 306 | `8981716858745712869796920037761/500000000000000000000000000000` | 17.963433717492 | [certificate](n306.cert) | source credits in metadata | `f58de39d385fcc00` |
| 328 | `157108007457079003558899729471/8440146855163000000000000000` | 18.614368938495 | [certificate](n328.cert) | franciscouzo; earlier seed and construction credits retained in provenance | `e84b87d229218d8b` |
| 336 | `18825571499861668938686306400451/1000000000000000000000000000000` | 18.825571499862 | [certificate](n336.cert) | Francisco Couzo | `08f1dafe436d44ba` |
| 337 | `3771678353527245620694257618907/200000000000000000000000000000` | 18.858391767637 | [certificate](n337.cert) | Francisco Couzo | `2bcf92a216a88380` |
| 365 | `165548154312242003558899729471/8440146855163000000000000000` | 19.614368938495 | [certificate](n365.cert) | franciscouzo; earlier seed and construction credits retained in provenance | `1fe5179ceb6f0b1b` |
| 373 | `19823062082837804646390244631729/1000000000000000000000000000000` | 19.823062082838 | [certificate](n373.cert) | Francisco Couzo | `494742aa3408d8a3` |
| 374 | `19832356217032762224853652799723/1000000000000000000000000000000` | 19.832356217033 | [certificate](n374.cert) | Francisco Couzo | `e46d218321a2ba49` |
| 417 | `21346022201532190804718566688329568429063689409412217226131/1021073725955279982867483585730206247184065500000000000000` | 20.905466137190 | [certificate](n417.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `4078be773923839c` |
| 420 | `6984999048372209495153230051451290381458140444136228721/333149218824243425064894337609322364543000000000000000` | 20.966577898708 | [certificate](n420.cert) | franciscouzo; earlier seed and construction credits retained in provenance | `0cb3f39abe313ff9` |
| 465 | `275718726779711258630767726040783310289320675409303293756427792811851704836893/12532728573685415539184198802364817418474378711791067289616384000000000000000` | 21.999896124666 | [certificate](n465.cert) | Francisco Couzo (Kaggle push search); earlier construction credits retained; earlier seed and construction credits retained in provenance | `7b308c52f4395b8c` |
| 503 | `2149272717279402811206840221656040644572262821313904757387758665372680281152706089/93854904270208852104554111760359424920000210077176573363989640544500000000000000` | 22.899951089308 | [certificate](n503.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `65e94ab14d9a53d1` |
| 505 | `1495635991468013743213944149988232850688390215391409306306567/65199903518727124679397536535187271246787455375000000000000` | 22.939236268018 | [certificate](n505.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `e94c532e963af018` |
| 506 | `11499895986299246940243842856651165009299/501014826329800005901024500000000000000` | 22.953204939148 | [certificate](n506.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `25ea966224be64e3` |
| 550 | `2002112743004934342420535835538164868168942920197131424334255009504923582550731/83723446250870296747450458847609345927885686299957826305095490500000000000000` | 23.913405774122 | [certificate](n550.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `e985df7528a7024e` |
| 553 | `108532374273267820720627402437862056282832457473961912494049257/4527884697425222959214366696974252229591690878500000000000000` | 23.969774304321 | [certificate](n553.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `458420a1d9a0cfb2` |
| 555 | `38966166306944527506631134260528164220300459962375641393483244430463929267977/1624215195267418493361608058381957621303301622110060349757801000000000000000` | 23.990765768282 | [certificate](n555.cert) | Francisco Couzo (Kaggle push search); earlier construction credits retained; earlier seed and construction credits retained in provenance | `0923c85f9da7a8d3` |
| 596 | `406671299451039816663150394447687555239978828526536511173748077272901708400741777/16339429263454443484028313075325434537020294287826908901021816451000000000000000` | 24.888953762946 | [certificate](n596.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `2612c37f18739f24` |
| 601 | `20906235301052914419772020043274789817586901609805773914122589490557671576536573/837467468444450006995274004662664382989660525785189812742532186500000000000000` | 24.963638694988 | [certificate](n601.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `4bedb485854e873a` |
| 700 | `9315292903038638285528502092662172571993723347335876121381462473910992505847/346189232924114698594371918732798468710759100264035573217248500000000000000` | 26.908095391519 | [certificate](n700.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `f8b35aa4829d1dd8` |
| 704 | `3091395328300968986892923029045046088463598770666916587369505929389769686110449/114643697642887255984752920161960379456819202987834034976926849500000000000000` | 26.965244421291 | [certificate](n704.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `8a3538ec4aee726d` |
| 759 | `177832363817104056842025608600065917909793/6356396183176821739159896500000000000000` | 27.976916273370 | [certificate](n759.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `1e28f35e9676fba2` |
| 850 | `5067207364951307925873256989/170861255962000000000000000` | 29.656854249499 | [certificate](n850.cert) | franciscouzo; earlier seed and construction credits retained in provenance | `6f005673962cf31d` |
| 922 | `1447819369343458403087509965263879111967945103797725422537831768702416125885454387/46942520319507157219773545825867754393500572609884430210241131443500000000000000` | 30.842386806015 | [certificate](n922.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `6177ea9133d040c6` |
| 983 | `555644685289324578761626773645700299574622160623444836279816588030642779848478429/17455241430706794995418713215138362650943369308008312947009909277000000000000000` | 31.832540815612 | [certificate](n983.cert) | Francisco Couzo (Kaggle push search); refines the packing of Vladislav Lavrentev (lightningv08), Kaggle "CUDA Packing Search" v11; earlier construction credits retained; earlier seed and construction credits retained in provenance | `01e2f9dfb45b5e91` |
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
