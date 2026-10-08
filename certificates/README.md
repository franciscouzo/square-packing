# Exact certificates

Exact rational certificates for the packings `nN.txt` in this repository, written by
Evan Daniel's exact contact solver ([evand/square-packing](https://github.com/evand/square-packing),
`search/exact`, MIT, commit 77f3c0ab). Each file gives `n S` and then one line per square:
a rational centre (x, y) and t = tan(θ/2), so that (cos θ, sin θ) = ((1−t²)/(1+t²), 2t/(1+t²))
and every square is exactly a unit square inside [0, S]². This proves s(n) ≤ S, and S lies
within about 1e-19 of the exact KKT point of the packing.

Check with his verifier (standard library only):

```sh
python3 search/exact/verify_cert.py nN.cert   # in a checkout of evand/square-packing
```

| n | S (exact) | rounded up | KKT point S* | SHA-256 |
|---:|---|---|---|---|
| 105 | `5395309134053572252907689667933/500000000000000000000000000000` | 10.790618268108 | 10.790618268107144505707… | `6f22b0cf51cf6ff8` |
| 108 | `5452410506160178214527814352111/500000000000000000000000000000` | 10.904821012321 | 10.904821012320356428946… | `528741a37ad0ae6d` |
| 127 | `5905439393794589919821183554001/500000000000000000000000000000` | 11.810878787590 | 11.810878787589179839524… | `2e039a654aa7afbe` |
| 131 | `11951105389414677460694240669403/1000000000000000000000000000000` | 11.951105389415 | 11.951105389414677460574… | `9ce74fda03fac60e` |
| 155 | `647624947200700369098292528347/50000000000000000000000000000` | 12.952498944015 | 12.952498944014007381836… | `cc9f7c800211acc2` |
| 180 | `13916993522477832483558124720393/1000000000000000000000000000000` | 13.916993522478 | 13.916993522477832483418… | `a66d49e35a3c841d` |
| 228 | `3901150368932418571180158525547/250000000000000000000000000000` | 15.604601475730 | 15.604601475729674284564… | `cb5e49904ac5e4b5` |
| 306 | `8981716858745712869796920037761/500000000000000000000000000000` | 17.963433717492 | 17.963433717491425739414… | `f58de39d385fcc00` |

Each certificate also replays as valid in exact rational arithmetic with `verify.py` from
[jlevy/squares](https://github.com/jlevy/squares) (`sqpack.verify`).
