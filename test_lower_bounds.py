from fractions import Fraction
import unittest

from lower_bounds import approximation, closed_form, rational_floor


class LowerBoundEvaluationTests(unittest.TestCase):
    def test_source_root_is_rounded_down_and_interval_cap_is_exact(self):
        interval = {'index': 1, 'd0': '0', 'd1': '1', 'alpha': '0', 'beta': '0'}
        bound, index = closed_form(50, [interval], places=12)
        self.assertEqual(index, 1)
        self.assertLessEqual(bound*bound, 50)
        self.assertGreater((bound+Fraction(1, 10**12))**2, 50)
        capped = dict(interval, d1='1/100')
        self.assertEqual(closed_form(50, [capped])[0], Fraction('7.01'))

    def test_strict_interval_threshold_excludes_a_root_at_the_open_endpoint(self):
        interval = {'index': 1, 'd0': '1/2', 'd1': '1', 'alpha': '0', 'beta': '25/16'}
        self.assertIsNone(closed_form(50, [interval]))
        interval['d0'] = '49/100'
        self.assertEqual(closed_form(50, [interval])[0], Fraction('7.5'))

    def test_family_scope_and_decimal_direction(self):
        self.assertIsNone(closed_form(48, []))
        self.assertIsNone(closed_form(49, []))
        self.assertEqual(rational_floor(Fraction(1, 3)), '0.333333333333')

    def test_register_formulas_and_named_root_approximations(self):
        self.assertAlmostEqual(approximation('1/2 + sqrt(106 - floor(√106) + 1/4)'), 10.310708435174292)
        self.assertEqual(approximation('root(P_trump11, 3.877083590022814)'), 3.877083590022814)
        with self.assertRaises(ValueError):
            approximation('__import__("os").getcwd()')


if __name__ == '__main__':
    unittest.main()
