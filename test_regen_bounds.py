"""Published witnesses remain available and propagate through deletion."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import regen_bounds


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


if __name__=='__main__':unittest.main()
