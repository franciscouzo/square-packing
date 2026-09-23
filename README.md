# Square packings for n = 102 and n = 103

Two packings of `n` unit squares in a square of side `s`, smaller than the best known
values in the [Friedman/Ellsworth catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
(fetched 2026-09-22).

| n | previous best known | here | improvement |
|---|---|---|---|
| 102 | 10.61138794077522 | **10.60790201773** | 3.49e-3 |
| 103 | 10.70378195534368 | **10.70358345693** | 1.99e-4 |

![n = 102 packed into a square of side 10.6079, with 102 unit squares, most axis-aligned and a diagonal band tilted.](n102_s10.607902017700.svg)

![n = 103 packed into a square of side 10.7036, with 103 unit squares, a tilted cluster surrounded by axis-aligned rows.](n103_s10.703583456903.svg)

Each `.txt` line is one unit square as `x y theta`, the centre and angle in radians,
in a container `[0, s]^2`. Both are verified free of overlaps in exact arithmetic.
