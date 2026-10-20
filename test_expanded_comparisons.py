from fractions import Fraction
import unittest

from expanded_comparisons import comparison_entry, external_comparison, render, reviewed_publications, rounded_up


def certificate(n, side):
    return {'side': float(Fraction(side)), 'source': 'evand', 'external': {
        'side': side, 'credit': 'Evan Daniel',
        'request': 'https://github.com/jlevy/squares/issues/489'}}


class ExpandedComparisonTests(unittest.TestCase):
    def test_external_bound_is_rounded_up(self):
        self.assertEqual(rounded_up('18.994450514277401521114135796864'), '18.994450514278')
        self.assertEqual(rounded_up('19'), '19.000000000000')

    def test_improving_a_derived_bound_can_still_be_superseded(self):
        section = render(['| 343 | 19 | **18.993870589753** | 6.129e-03 |'], {
            'entries': {'343': certificate(343, '18.978232523635611279730512106023')}})
        self.assertIn('superseded by 1.6e-02', section)
        self.assertNotIn('smaller than reviewed published bound', section)
        self.assertIn('18.978232523636', section)
        self.assertIn('[Evan Daniel](https://github.com/jlevy/squares/issues/489)', section)

    def test_comparison_credit_does_not_imply_global_optimality(self):
        result = external_comparison('18.993744819377', certificate(344, '18.994450514277401521114135796864'))
        self.assertEqual(result[0], '18.994450514278')
        self.assertEqual(result[2], '**smaller than reviewed published bound**')

    def test_rounding_ties_are_not_record_claims(self):
        entry = certificate(344, '19')
        for value in ('18.99999999995', '19.00000000005'):
            self.assertEqual(external_comparison(value, entry)[2], 'tied (within 1e-10)')

    def test_reviewed_public_construction_overrides_an_older_certificate(self):
        old=certificate(343,'18.99');current=certificate(343,'18.98')
        known={'published_above_324':{'343':old},'public_comparisons':{'343':current}}
        self.assertEqual(comparison_entry(known,343),current)
        self.assertIn('superseded',external_comparison('18.985',comparison_entry(known,343))[2])

    def test_absent_source_remains_a_reference_comparison(self):
        self.assertEqual(external_comparison('19.9', None), ('—', '—', 'reference comparison only'))
        rows = ['| 375 | 19.93125509556197 | **19.902353152174** | 2.890e-02 |']
        section = render(rows, {'entries': {}, 'generated': '2026-10-12T00:00:00Z'})
        self.assertIn('0 of these 1 counts as of 2026-10-12', section)
        self.assertIn(rows[0], section)
        self.assertNotIn('best known', section)

    def test_adopted_geometry_is_retained_as_a_published_comparison(self):
        found = {375: [
            {'side': Fraction('19.906981767290602'), 'source': 'evand',
             'path': 'evand/search/packer/candidates/big1_n375.cert',
             'sha256': 'best', 'same_as_ours': 'found/n375_old.txt'},
            {'side': Fraction('19.907024202136837'), 'source': 'evand',
             'path': 'evand/search/packer/candidates/polish_n375.cert', 'sha256': 'old'},
            {'side': Fraction('19.8'), 'source': 'evand', 'path': 'evand/invalid.cert', 'sha256': 'invalid'},
            {'side': Fraction('20'), 'source': 'evand', 'path': 'evand/grid.cert', 'sha256': 'grid'},
        ]}
        verified = {sha: {'valid': sha != 'invalid'} for sha in ('best', 'old', 'invalid', 'grid')}
        sources = {'evand': {'url': 'https://github.com/evand/square-packing.git', 'commit': 'pinned'}}
        published = reviewed_publications(found, verified, sources,
            lambda source, path: 'Evan Daniel (from a Francisco Couzo seed)',
            lambda source, path: 'https://github.com/evand/square-packing')
        self.assertEqual(len(published['375']['certificates']), 2)
        self.assertEqual(published['375']['external']['same_as_ours'], 'found/n375_old.txt')
        self.assertIn('/blob/pinned/', published['375']['external']['certificate_url'])
        known = {'entries': {}, 'published_above_324': published}
        self.assertNotIn('375', known['entries'])
        entry = comparison_entry(known, 375)
        self.assertEqual(external_comparison('19.902353152174', entry)[0], '19.906981767291')
        section = render(['| 375 | 19.93125509556197 | **19.902353152174** | 2.890e-02 |'], known)
        self.assertIn('1 of these 1 counts', section)
        self.assertIn('Francisco Couzo seed', section)

    def test_published_comparisons_cover_the_requested_larger_range(self):
        found = {1023: [{'side': Fraction('31.99'), 'source': 'evand',
                        'path': 'evand/n1023.cert', 'sha256': 'large'}],
                 1025: [{'side': Fraction('32.99'), 'source': 'evand',
                         'path': 'evand/n1025.cert', 'sha256': 'outside'}]}
        verified = {'large': {'valid': True}, 'outside': {'valid': True}}
        sources = {'evand': {'url': 'https://github.com/evand/square-packing.git', 'commit': 'pinned'}}
        published = reviewed_publications(found, verified, sources,
                                         lambda *_: 'Evan Daniel', lambda *_: 'https://example.com/source')
        self.assertEqual(set(published), {'1023'})
        section = render(['| 1023 | 32 | **31.990000000000** | 1.000e-02 |'],
                         {'published_above_324': published})
        self.assertIn('n=325–1023', section)
        self.assertIn('31.990000000000', section)


if __name__ == '__main__':
    unittest.main()
