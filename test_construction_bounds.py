from fractions import Fraction as F
import unittest

from construction_bounds import l_border_catalogue
from gobel_bounds import Q2, exact_value


class ClassicalBorderTests(unittest.TestCase):
    def test_offcentre_border_and_repeated_border_keep_exact_sides_and_parent(self):
        side = Q2(F(21, 2), F(13, 2))
        parent = {'bound': str(side.enclosure()[1]), 'exact_bound': side.record(),
                  'source_n': 368, 'deleted_squares': 0, 'proof': 'friedman_bounds.json',
                  'credit': 'Erich Friedman', 'source': 'original construction'}
        result = l_border_catalogue([{'368': parent}], max_n=491)
        for n, layers in [(407, 1), (448, 2), (491, 3)]:
            row = result[str(n)]
            self.assertEqual(exact_value(row), side + layers)
            self.assertEqual(row['source_n'], n)
            self.assertEqual(row['construction']['source_n'], 368)
            self.assertEqual(row['construction']['layers'], layers)
            self.assertEqual(row['proof'], parent['proof'])
            self.assertEqual(row['credit'], parent['credit'])

    def test_exact_floor_does_not_round_an_algebraic_side_to_an_integer(self):
        # This is just below 3; using float floor would add two extra squares.
        side = Q2(3 + F(1, 10**100), -F(1, 10**100))
        parent = {'bound': str(side.enclosure(120)[1]), 'exact_bound': side.record(),
                  'source_n': 5, 'source': 'fixture'}
        result = l_border_catalogue([{'5': parent}], max_n=11)
        self.assertIn('10', result)
        self.assertNotIn('12', result)
        self.assertEqual(exact_value(result['10']), side + 1)


if __name__ == '__main__':
    unittest.main()
