# Square packings for n = 102, 103, 152, 180 and 206

Packings of `n` unit squares in a square of side `s`, smaller than the best known values
in the [Friedman/Ellsworth catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
(fetched 2026-09-22).

| n | previous best known | here | improvement |
|---|---|---|---|
| 102 | 10.61138794077522 | **10.607902017732** | 3.486e-03 |
| 103 | 10.70378195534368 | **10.703583456926** | 1.985e-04 |
| 152 | 12.83095954472600 | **12.830764338144** | 1.952e-04 |
| 180 | 13.93508705291129 | **13.932235154396** | 2.852e-03 |
| 206 | 14.87221902902620 | **14.860232206380** | 1.199e-02 |

![n = 102 packed into a square of side 10.6079: a field of axis-aligned squares crossed by one diagonal band of squares tilted about 40 degrees.](n102_s10.607902017732.svg)

![n = 103 packed into a square of side 10.7036: axis-aligned rows around a central cluster tilted about 29 degrees.](n103_s10.703583456926.svg)
![n = 152 packed into a square of side 12.8308: two axis-aligned fields separated by a diagonal band of tilted squares running corner to corner.](n152_s12.830764338144.svg)
![n = 180 packed into a square of side 13.9323: two separate tilted clusters, one in the upper-left corner and a larger one sweeping through the lower right, with axis-aligned fields between them.](n180_s13.932235154396.svg)
![n = 206 packed into a square of side 14.8602: a straight diagonal band of squares tilted about 30 degrees running corner to corner through an axis-aligned field.](n206_s14.860232206380.svg)

Each `.txt` line is one unit square as `x y theta`, the centre and angle in radians, in a
container `[0, s]^2`.
