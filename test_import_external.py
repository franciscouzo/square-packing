"""Refresh comparisons without losing reviewed bounds, seeds or source credits."""
from contextlib import redirect_stdout
from fractions import Fraction
import gzip
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import import_external as importer


class ExternalImport(unittest.TestCase):
    def refresh(self, candidate_side, reviewed_side):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sources, seeds = root/'external/sources', root/'external/seeds'
            source = sources/'evand/example.cert'
            source.parent.mkdir(parents=True)
            source.write_text('fixture certificate')
            seeds.mkdir(parents=True)
            seed = seeds/'n5.txt'
            seed.write_text('existing reviewed seed')
            reviewed = {'5': {'side': float(reviewed_side), 'source': 'catalogue',
                        'seed': 'external/seeds/n5.txt', 'external': {'side': str(reviewed_side)}}}
            (root/'known_best.json').write_text(json.dumps({'reviewed_comparisons': reviewed}))
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            (seeds/'verified.json').write_text(json.dumps({digest: {'valid': True}}))
            squares = [(Fraction(0), Fraction(0), Fraction(0))]*5
            commits = {'evand': {'url': 'https://github.com/evand/square-packing.git', 'commit': 'fixture'}}
            def write_seed(path, side, _squares):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text('new verified seed '+str(side))
            with patch.multiple(importer, ROOT=root, SOURCES=sources, SEEDS=seeds), \
                 patch.object(importer, 'fetch', return_value=commits), \
                 patch.object(importer, 'register_bounds', return_value={}), \
                 patch.object(importer, 'certificates', return_value=iter([(5,candidate_side,squares,'evand',source)])), \
                 patch.object(importer, 'decimal_packings', return_value=iter([])), \
                 patch.object(importer, 'same_as_ours', return_value=None), \
                 patch.object(importer, 'write_pose', side_effect=write_seed), \
                 patch('sys.argv', ['import_external.py','--offline']), redirect_stdout(io.StringIO()):
                importer.main()
            return json.loads((root/'known_best.json').read_text()), seed.read_text()

    def test_reviewed_bound_keeps_its_better_seed(self):
        known, seed = self.refresh(Fraction('2.95'), Fraction('2.9'))
        self.assertEqual(known['entries']['5']['side'], 2.9)
        self.assertEqual(seed, 'existing reviewed seed')
        self.assertIn('5', known['reviewed_comparisons'])

    def test_new_smaller_certificate_replaces_reviewed_seed(self):
        known, seed = self.refresh(Fraction('2.8'), Fraction('2.9'))
        self.assertEqual(known['entries']['5']['side'], 2.8)
        self.assertTrue(seed.startswith('new verified seed'))

    def test_compressed_certificate_matches_plain_format(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'n5.cert.gz'
            with gzip.open(path,'wt') as stream:
                stream.write('# certificate\n5 14/5\n'+''.join('1/2 1/2 0\n' for _ in range(5)))
            n, side, squares = importer.read_cert_text(path)
            self.assertEqual((n,side,len(squares)), (5,Fraction(14,5),5))

    def test_atlas_certificate_keeps_original_constructor(self):
        atlas = {'131': {'credit': {'who': 'Nate Chaoweeraprasit (SQUISH)',
                                  'url': 'https://github.com/jlevy/squares/issues/481'}}}
        path = 'evand/search/regularize/lists/certs/n-131.cert.gz'
        with patch.object(importer, '_ATLAS', atlas):
            self.assertEqual(importer.credit_for('evand',path), 'Nate Chaoweeraprasit (SQUISH)')
            self.assertTrue(importer.request_for('evand',path).endswith('/481'))

    def test_matching_atlas_copy_does_not_add_self_attribution(self):
        atlas = {'110': {'credit': {'who': 'Francisco Couzo',
                                  'url': 'https://github.com/franciscouzo/square-packing'}}}
        also = []
        with patch.object(importer, '_ATLAS', atlas):
            importer.note_same_packing(also, {'source':'evand',
                'path':'evand/search/regularize/lists/certs/n-110.cert.gz'}, 'n110.txt')
        self.assertEqual(also, [])

    def test_matching_certificate_and_decimal_copy_share_one_citation(self):
        also = []
        for path in ['mishapolk/certificates/square-267.cert','mishapolk/certificates/square-267.txt']:
            importer.note_same_packing(also, {'source':'mishapolk','path':path}, 'n267.txt')
        self.assertEqual(len(also), 1)

    def test_numbered_mishapolk_certificates_are_discovered_and_cited(self):
        with tempfile.TemporaryDirectory() as directory:
            sources = Path(directory)
            certificate = sources/'mishapolk/certificates/n5.cert'
            certificate.parent.mkdir(parents=True)
            certificate.write_text('5 14/5\n'+'1/2 1/2 0\n'*5)
            with patch.object(importer, 'SOURCES', sources):
                rows = list(importer.certificates())
            self.assertEqual(len(rows), 1)
            self.assertEqual((rows[0][0], rows[0][1], rows[0][3]), (5, Fraction(14, 5), 'mishapolk'))
            self.assertEqual(importer.request_for('mishapolk', 'mishapolk/certificates/n5.cert'),
                             'https://github.com/jlevy/squares/issues/593')


if __name__ == '__main__':
    unittest.main()
