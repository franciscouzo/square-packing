"""The acceptance threshold retains verified constructions across imports."""
from fractions import Fraction
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import accept_candidates


class AcceptanceBoundsTests(unittest.TestCase):
    def test_verified_construction_survives_missing_register_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'known_best.json').write_text(json.dumps({'entries':{}}))
            (root/'upper_bounds.json').write_text(json.dumps({'entries':{'416':{
                'verified':{'bound':'20899494936612/1000000000000'}}}}))
            with patch.object(accept_candidates,'ROOT',root):
                self.assertEqual(accept_candidates.known_best(416),Fraction('20.899494936612'))

    def test_a_tighter_import_still_takes_precedence(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'known_best.json').write_text(json.dumps({'entries':{'806':{'side':'28.90'}}}))
            (root/'upper_bounds.json').write_text(json.dumps({'entries':{'806':{
                'verified':{'bound':'28924508775310/1000000000000'}}}}))
            with patch.object(accept_candidates,'ROOT',root):
                self.assertEqual(accept_candidates.known_best(806),Fraction('28.90'))
                self.assertIsNone(accept_candidates.known_best(1025))

    def test_reported_public_bound_blocks_reintroducing_a_superseded_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'known_best.json').write_text(json.dumps({'entries':{}}))
            (root/'upper_bounds.json').write_text(json.dumps({'entries':{'1453':{
                'verified':{'bound':'38.656854249528'},
                'reported':{'bound':'38.62799971540531'}}}}))
            with patch.object(accept_candidates,'ROOT',root):
                self.assertEqual(accept_candidates.known_best(1453),Fraction('38.62799971540531'))


if __name__=='__main__':unittest.main()
