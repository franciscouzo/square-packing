Please register the following improved feasible upper bounds. This updates my earlier reports in #488 and #506 and submits new refinements at 156, 176 and 271.

**Bounds and comparisons**

Every displayed side is rounded upward to 12 decimal places from its certificate’s exact rational side. The improvements are computed from the rational sides, before rounding.

| n | new certified upper bound | comparison bound | improvement |
|---:|---:|---:|---:|
| 156 | 12.979165853835 | 12.979172613645 | 6.76e-06 |
| 176 | 13.807637227056 | 13.808663234387 | 0.00103 |
| 237 | 15.902947773659 | 15.902949607678 | 1.83e-06 |
| 271 | 16.948992356452 | 16.949116687816 | 0.000124 |

The register comparison is pinned to [`562fdbdff1d98948f68b36b81b53f9c8165ffd08`](https://github.com/jlevy/squares/tree/562fdbdff1d98948f68b36b81b53f9c8165ffd08). The previous 156 bound is Daniil Ostashev’s; 237 is my refinement of SQUISH from #488; 271 is SQUISH’s #500 packing. For 176, the comparison uses [Daniil Ostashev’s smaller published certificate](https://github.com/dostashev/square-packing/blob/fe43a64ecf2581cdbd11830e8a5be0989746c5d3/records/n0176.sqcert), rather than the larger bound currently in the register.

For the beyond-horizon list, these five bounds improve the corresponding rows confirmed from #506. The comparisons below use the exact certificates of that report at `337078ca3e05153aceb099237b175cf64af5748a`.

| n | new certified upper bound | previously reported in #506 | improvement |
|---:|---:|---:|---:|
| 338 | 18.906332809853 | 18.906436500552 | 0.000104 |
| 344 | 18.993741872920 | 18.994353244944 | 0.000611 |
| 375 | 19.901618621328 | 19.906335145009 | 0.00472 |
| 376 | 19.904949736499 | 19.910276586885 | 0.00533 |
| 378 | 19.942536155970 | 19.942541777355 | 5.62e-06 |

These are updates to published beyond-horizon packings. The frozen L-border reference used by my search is only a construction baseline.

**Certificates and fixed versions**

All nine certificates are in [`franciscouzo/square-packing` at `0fa0e0de2ef0b414655e871b1baffcfe0d33c815`](https://github.com/franciscouzo/square-packing/tree/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates). Each file starts with `n S`, followed by exactly n rational triples `(x, y, t)`, where `t = tan(theta/2)`. The exact S in each header is the authoritative bound.

| n | certificate | SHA-256 |
|---:|---|---|
| 156 | [n156.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n156.cert) | `1b4dfa721e3289c9f55f6920fe10360b75eb56dd03b366c281ddabf2dbf24dd2` |
| 176 | [n176.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n176.cert) | `1b132aa65b3a513267c9bfd260395216c070946c62220cfba663115baf3c901b` |
| 237 | [n237.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n237.cert) | `7b65988e7da36573f7b1318839f0da023c16a730225404a299870898db8cfa70` |
| 271 | [n271.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n271.cert) | `690a1d024f271dffdd0c54d0203f0f1ac1295ccb84f835b7ebe4ff14e5253617` |
| 338 | [n338.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n338.cert) | `20cfd3cab9120d956848b342c378fd04837dfacd6e9c2f37fac294478bf7a519` |
| 344 | [n344.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n344.cert) | `145c020467e1af49210b5f5d815ce7eb7e248f1bbee072c7fe79c5f61c4058ca` |
| 375 | [n375.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n375.cert) | `0252c1ee50315af5065a7ddf7f7a252ea3e5d48ef70e4e3925f7c7b56bcc785c` |
| 376 | [n376.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n376.cert) | `428cf419e40b40758e32ae932b51b4613d34ddb293f233fcdbc6c7499af468e9` |
| 378 | [n378.cert](https://github.com/franciscouzo/square-packing/blob/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/certificates/n378.cert) | `c15aeb0fa927ec749bab7ae22eca36645a2f2343c184ebccb9cf29c3afb7aa03` |

The certificates for 156, 237, 271, 338 and 376 were produced with Evan Daniel’s exact contact solver. The certificates for 176, 344, 375 and 378 are rational witnesses from the decimal poses, with centre dilation respectively `1+1e-11`, `1+1e-12`, `1+1e-10` and `1+1e-12`. I have also corrected the certificate README’s blanket `1+1e-12` statement in response to the review of #506.

**Verification and reproduction**

I fetched all nine certificates from the fixed commit above, checked their complete SHA-256 hashes and exact row counts, and replayed both of the following checkers using Python’s exact `Fraction` arithmetic:

- [jlevy/squares / packing/src/sqpack/verify.py](https://github.com/jlevy/squares/blob/562fdbdff1d98948f68b36b81b53f9c8165ffd08/packing/src/sqpack/verify.py) at `562fdbdff1d98948f68b36b81b53f9c8165ffd08`; checker SHA-256 `56bc5b9f690b054ba30e82547dea4aa9d0ccea0a2b1827fab28fcc4e98677337`.
- [evand/square-packing / search/exact/verify_cert.py](https://github.com/evand/square-packing/blob/31523f87316bdfda00f5459dd9077928e264f133/search/exact/verify_cert.py) at `31523f87316bdfda00f5459dd9077928e264f133`; checker SHA-256 `3299ca0c0f02f7c221deeea69a9a85b5a90db6bc410b20727fdff211c92bed52`.

Both routes passed all nine certificates. On CT104, the geometry checks took 4.52 seconds in total for `sqpack.verify`, and 5.56 seconds including interpreter startup for Evan Daniel’s verifier. These times exclude downloads.

The [manifest](https://github.com/franciscouzo/square-packing/blob/master/publications/20261012/manifest.json) retains the full rational bounds, comparison fractions, certificate hashes and checker pins. The [receipt](https://github.com/franciscouzo/square-packing/blob/master/publications/20261012/receipt.json) records each verdict and elapsed time. Reproduce from this repository with Python 3 and network access:

```sh
python3 publications/20261012/replay.py --output replay-receipt.json
```

The [replay script](https://github.com/franciscouzo/square-packing/blob/master/publications/20261012/replay.py) downloads only the pinned certificates and pinned checker files, verifies their hashes, reconstructs exact unit-square corners, and checks each rational improvement.

**Shared assumptions and limits**

Both checkers use rational half-angle rotations and separating-axis geometry. The `sqpack.verify` route is the upstream project’s own checker, not a third independent implementation; Evan Daniel supplies the contact solver and the second verifier. No independent human review or optimality proof is claimed. These certificates establish finite packing feasibility only; they do not certify a local or global optimum.

**Origins and credit**

- 156 and 176: Daniil Ostashev’s arrangements, continued with my basin hopping and refinement. The 176 search also continued improvements obtained through my web app.
- 237 and 271: Nate Chaoweeraprasit’s SQUISH arrangements, continued with my basin hopping and Evan Daniel’s `fq` refinement. For 237 this improves my previously registered #488 certificate.
- 344: Kevin Fang’s 344 (#484), continued from the packing reported in #506 with my basin hopping and refinement.
- 338, 375, 376 and 378: continued from my L-border constructions reported in #506. The original 338 and 375 constructions use my 303, derived from SQUISH #401; 376 uses my earlier 304; 378 uses my 306. The new 338 and 376 refinements used Evan Daniel’s `fq`, and 378 used my basin hopping.
- 375: the latest improvement was found in my browser web app using the Ellsworth search, after a native search improvement to the starting packing. The accepted submission is attributed to `franciscouzo`; its [original submission and certificate archive](https://github.com/franciscouzo/square-packing/tree/0fa0e0de2ef0b414655e871b1baffcfe0d33c815/found/web) includes record `a87a2fa7fd11f1295eff8016b0a8c1a1`, received on 12 October 2026 at 18:16:59 UTC. The normalized installed pose has numerical side 19.901618619437087; the certified rational upper bound is the larger 19.901618621328 printed above.

Please retain the original construction credits. Evan Daniel’s optimizer, contact solver and verifier, David Ellsworth’s refinement/search ideas, and the upstream `sqpack.verify` checker were used in this work.

**AI disclosure**

The continuing search and application work, this source audit, the exact verification orchestration, and this issue preparation were assisted by OpenAI Codex. Earlier search code and earlier submissions were also prepared with Claude Code. Francisco Couzo directed the work; the checker receipts report automated validation and do not assert independent human review.
