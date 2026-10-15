"""Published witnesses remain available and propagate through deletion."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import regen_bounds
from gobel_bounds import generate as generate_gobel, exact_value, Q2


class RetainedCertifiedBounds(unittest.TestCase):
    def fixture(self, root):
        (root/'certificates/best').mkdir(parents=True)
        (root/'known_best.json').write_text(json.dumps({'entries':{}}))
        (root/'records.txt').write_text('')
        certificate=root/'certificates/best/n5.cert'
        certificate.write_text('5 14/5\n'+'1/2 1/2 0\n'*5)
        entry={'kind':'certificate','source_n':5,'bound':'14/5',
               'certificate':'certificates/best/n5.cert',
               'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),
               'credit':'original constructor','verification':{'valid':True}}
        (root/'certified_bounds.json').write_text(json.dumps({'entries':{'5':entry}}))
        return certificate

    def test_retained_witness_survives_empty_comparison_import_and_root_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            with patch.object(regen_bounds,'ROOT',root):
                entries=regen_bounds.render(max_n=6)['entries']
            self.assertEqual(Fraction(entries['5']['verified']['bound']),Fraction(14,5))
            self.assertEqual(entries['5']['verified']['credit'],'original constructor')
            self.assertEqual(entries['6']['verified']['bound'],'3')
            self.assertEqual(entries['4']['verified']['bound'],'2')

    def test_a_larger_witness_gives_a_stronger_bound_after_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            path=root/'certified_bounds.json';data=json.loads(path.read_text())
            entry=data['entries'].pop('5');entry.update(bound='77/10',source_n=51)
            certificate=root/entry['certificate'];certificate.write_text('51 77/10\n'+'1/2 1/2 0\n'*51)
            entry['certificate_sha256']=hashlib.sha256(certificate.read_bytes()).hexdigest()
            data['entries']['51']=entry;path.write_text(json.dumps(data))
            with patch.object(regen_bounds,'ROOT',root):entries=regen_bounds.render(max_n=51)['entries']
            self.assertEqual(entries['50']['verified']['bound'],'77/10')
            self.assertEqual(entries['50']['verified']['source_n'],51)
            self.assertEqual(entries['50']['verified']['deleted_squares'],1)
            self.assertEqual(entries['49']['verified']['bound'],'7')

    def test_changed_certificate_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);certificate=self.fixture(root)
            certificate.write_text(certificate.read_text()+'# changed\n')
            with patch.object(regen_bounds,'ROOT',root),self.assertRaises(ValueError):
                regen_bounds.render(max_n=6)

    def test_exact_algebraic_comparison_beats_a_smaller_rational_enclosure(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);certificate=self.fixture(root)
            data=generate_gobel(max_n=5)
            (root/'gobel_bounds.json').write_text(json.dumps(data))
            # This certificate is above the algebraic value but below its
            # outward enclosure. Comparing only rational enclosures is wrong.
            hi=Fraction(data['witnesses'][0]['bound'])
            challenger=hi-Fraction(1,10**90)
            self.assertLess(Q2(2,Fraction(1,2)),Q2(challenger))
            certificate.write_text(f'5 {challenger}\n'+'1/2 1/2 0\n'*5)
            path=root/'certified_bounds.json';retained=json.loads(path.read_text())
            retained['entries']['5'].update(bound=str(challenger),
                certificate_sha256=hashlib.sha256(certificate.read_bytes()).hexdigest())
            path.write_text(json.dumps(retained))
            with patch.object(regen_bounds,'ROOT',root):
                entry=regen_bounds.render(max_n=5)['entries']['5']['verified']
            self.assertEqual(exact_value(entry),Q2(2,Fraction(1,2)))
            self.assertEqual(entry['credit'],'Frits Göbel; family formulas generalized by David Ellsworth')

    def test_algebraic_constructions_propagate_by_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);self.fixture(root)
            (root/'gobel_bounds.json').write_text(json.dumps(generate_gobel(max_n=27)))
            with patch.object(regen_bounds,'ROOT',root):
                entry=regen_bounds.render(max_n=27)['entries']['26']['verified']
            self.assertEqual(exact_value(entry),Q2(5,Fraction(1,2)))
            self.assertEqual(entry['source_n'],27)
            self.assertEqual(entry['deleted_squares'],1)
            self.assertEqual(entry['status'],'verified by deletion from an exact algebraic construction')


if __name__=='__main__':unittest.main()
