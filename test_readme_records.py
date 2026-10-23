"""Published ownership and exact refinements survive record housekeeping."""
from fractions import Fraction
import unittest

from readme_records import classification, our_credit, public_comparison


class RecordStandingTests(unittest.TestCase):
    def test_account_credit_with_source_details_is_still_owned(self):
        self.assertTrue(our_credit('franciscouzo; earlier seed and construction credits retained in provenance'))

    def test_publishing_our_9913_witness_retains_the_record(self):
        side = ('183571976140896212114115030871896304362171894487/'
                '1835758951082200000018357589510822000000000000')
        public = dict(bound=side, credit='Francisco Couzo (assembly/refinement)',
                      source='https://github.com/jlevy/squares/issues/715')
        self.assertEqual(classification(dict(rational_side=side), public, {}),
                         'Published record held by this project')

    def test_own_refinements_have_no_minimum_gain(self):
        for gain in [Fraction(1, 10**12), Fraction(1, 10**40)]:
            with self.subTest(gain=gain):
                self.assertEqual(classification(dict(rational_side=str(6-gain)),
                    dict(bound='6', credit='this repository; source credit in certificate metadata'), {}),
                    'Refinement of our published record')

    def test_stronger_public_record_supersedes_even_our_earlier_credit(self):
        for owner in ['Francisco Couzo', 'another author']:
            with self.subTest(owner=owner):
                self.assertIsNone(classification(dict(rational_side='6'),
                    dict(bound=str(6-Fraction(1, 10**6)), credit=owner),
                    dict(register_found_by=['Francisco Couzo'])))

    def test_recertifying_our_packing_within_rounding_keeps_the_record(self):
        for gap in [0, Fraction(1, 10**15), Fraction(1, 10**10)]:
            with self.subTest(gap=gap):
                self.assertEqual(classification(dict(rational_side='6'),
                    dict(bound=str(6-gap), credit='another author'),
                    dict(register_found_by=['Francisco Couzo'])),
                    'Published record held by this project')
        self.assertEqual(classification(dict(rational_side='6'),
            dict(bound=str(6-Fraction(1, 10**15)), credit='another author'),
            dict(external=dict(credit='Francisco Couzo (Kaggle push search)'))),
            'Published record held by this project')

    def test_value_within_rounding_of_our_superseded_review_keeps_the_record(self):
        public = dict(bound=str(6-Fraction(4, 10**12)), credit='another author',
                      superseded_review=dict(bound='6', credit='Francisco Couzo'))
        self.assertEqual(classification(dict(rational_side='6'), public, {}),
                         'Published record held by this project')
        public['bound'] = str(6-Fraction(1, 10**6))
        self.assertIsNone(classification(dict(rational_side='6'), public, {}))

    def test_matching_another_author_does_not_claim_the_record(self):
        for registered in [{}, dict(register_found_by=['another author'])]:
            with self.subTest(registered=registered):
                self.assertIsNone(classification(dict(rational_side='6'),
                    dict(bound='6', credit='another author'), registered))

    def test_new_external_certificate_cannot_be_hidden_by_reporting_tolerance(self):
        tighter = str(6-Fraction(1, 10**40))
        public = {'9913': dict(bound='6', credit='Francisco Couzo')}
        known = dict(entries={'9913': dict(side=6, source='reviewed-submission',
            external=dict(side=tighter, credit='another author', request='issue'))})
        comparison = public_comparison(9913, public, known)
        self.assertEqual(comparison['bound'], tighter)
        self.assertIsNone(classification(dict(rational_side='6'), comparison, {}))

    def test_register_display_rounding_does_not_replace_exact_public_certificate(self):
        public = {'9913': dict(bound='6', credit='Francisco Couzo')}
        known = dict(entries={'9913': dict(side=5.999999999999999, source='register')})
        self.assertEqual(public_comparison(9913, public, known), public['9913'])


if __name__ == '__main__':
    unittest.main()
