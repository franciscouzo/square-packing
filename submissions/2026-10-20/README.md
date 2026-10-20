# Certified upper-bound updates, 20 October 2026

The [manifest](manifest.json) lists 135 new or stronger retained witnesses since the preceding local commit. Each improves the reviewed public comparison by more than `1e-10`. The 5 improvements smaller than `1e-7` are identified separately; a tighter witness does not establish a new arrangement.

The certificate header gives the exact rational upper bound. Displayed values are rounded upward to 12 places. Certificates and per-count construction/seed metadata are linked from the manifest. Credit remains with the starting construction authors, numerical refiners and certificate suppliers recorded there.

[Verification receipts](verification-receipts.json) retain both exact geometry routes, bound to certificate SHA-256. The corner route uses jlevy/squares' retained `sqpack.verify`; the projection route uses this repository's [standard-library checker](../../verify_bound_certificate.py). Cached verdicts are reused only for identical bytes. To replay a certificate:

```sh
python3 verify_bound_certificate.py certificates/n867.cert
```

Run that command from the repository root. Closed-container feasibility, including edge and wall contacts, is the packing convention. Local or global optimality is not claimed.

[all-improvements.csv](all-improvements.csv) records the full 1221-count index of retained bounds and construction consequences below the public comparison, including earlier retained results. The registration request covers the 135 manifest rows. The complete index extends through n=10000 in [upper_bounds.json](../../upper_bounds.json).
