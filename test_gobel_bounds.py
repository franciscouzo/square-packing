"""Controls for exact signs, tight Göbel packings and the spatial pair filter."""
from fractions import Fraction as F
import unittest

from gobel_bounds import Q2, SQRT2, build, candidates, overlaps, verify


class GobelBoundsTests(unittest.TestCase):
    def candidate(self, family, a, b):
        return next(r for r in candidates() if (r['family'], r['a'], r['b']) == (family, a, b))

    def test_ordering_at_a_close_rational_approximation_to_sqrt_two(self):
        lo, hi = SQRT2.enclosure()
        self.assertLess(Q2(lo), SQRT2)
        self.assertLess(SQRT2, Q2(hi))
        self.assertEqual((SQRT2-Q2(lo)).sign(), 1)
        self.assertEqual((Q2(lo)-SQRT2).sign(), -1)
        self.assertEqual((SQRT2*SQRT2-Q2(2)).sign(), 0)
        self.assertEqual((-SQRT2+Q2(hi)).sign(), 1)

    def test_decimal_upper_rounding_and_cell_boundary_floors(self):
        self.assertEqual(Q2(11, 7).rounded_up(), '20.899494936612')
        self.assertEqual(Q2(F(3, 2)).rounded_up(), '1.500000000000')
        self.assertEqual(Q2(F(-1, 3)).rounded_up(), '-0.333333333333')
        self.assertEqual((SQRT2-2).floor(), -1)
        self.assertEqual(Q2(2).floor(), 2)
        self.assertEqual(Q2(2)-SQRT2, Q2(2, -1))

    def test_n416_tight_construction_and_negative_controls(self):
        candidate = self.candidate('square', 10, 14)
        squares = build(candidate)
        self.assertEqual(len(squares), 416)
        self.assertEqual(candidate['side'], Q2(11, 7))
        self.assertTrue(verify(squares, candidate['side'])['valid'])
        self.assertFalse(verify(squares+[squares[0]], candidate['side'])['valid'])
        self.assertFalse(verify(squares, candidate['side']-F(1, 10**30))['valid'])

    def test_regular_and_corner_strips(self):
        for family, a, b, n, side in [('strip', 4, 5, 27, Q2(5, F(1, 2))),
                                     ('corner_strip', 13, 17, 202, Q2(2, 9))]:
            candidate = self.candidate(family, a, b)
            squares = build(candidate)
            self.assertEqual(len(squares), n)
            self.assertEqual(candidate['side'], side)
            self.assertTrue(verify(squares, side)['valid'])
            self.assertFalse(verify(squares+[squares[-1]], side)['valid'])

    def test_spatial_filter_matches_all_pairs_at_cell_edges(self):
        for candidate in [self.candidate('square', 3, 4), self.candidate('strip', 4, 5)]:
            squares = build(candidate)
            for dx, dy in [(0, 0), (F(1, 3), F(2, 3))]:
                shifted = [(x+dx, y+dy, angle) for x, y, angle in squares]
                oracle = all(not overlaps(left, right) for i, left in enumerate(shifted)
                             for right in shifted[:i])
                self.assertTrue(oracle)
                self.assertEqual(verify(shifted, candidate['side']+1)['valid'], oracle)
                self.assertFalse(verify(shifted+[shifted[-1]], candidate['side']+1)['valid'])

    def test_pair_contacts_and_rotated_collisions(self):
        axis = (Q2(2), Q2(2), 0)
        self.assertFalse(overlaps(axis, (Q2(3), Q2(2), 0)))
        self.assertTrue(overlaps(axis, (Q2(3)-F(1, 10**30), Q2(2), 0)))
        self.assertFalse(overlaps(axis, (Q2(2)+Q2(F(1, 2), F(1, 2)), Q2(2), 1)))
        self.assertTrue(overlaps(axis, (Q2(3), Q2(2), 1)))
        rotated = (Q2(2), Q2(2), 1)
        self.assertFalse(overlaps(rotated, (Q2(2)+SQRT2/2, Q2(2)+SQRT2/2, 1)))


if __name__ == '__main__':
    unittest.main()
