from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from friedman_bounds import candidates,build,generate
from gobel_bounds import Q2,verify,exact_value
import regen_bounds


class OffcentreTests(unittest.TestCase):
    def test_published_n26_and_larger_n368_with_negative_controls(self):
        for n,expected in [(26,Q2(F(7,2),F(3,2))),
                           (368,Q2(F(21,2),F(13,2)))]:
            row=next(r for r in candidates() if r['n']==n)
            squares=build(row)
            self.assertEqual(row['side'],expected)
            self.assertEqual(len(squares),n)
            self.assertTrue(verify(squares,row['side'])['valid'])
            self.assertFalse(verify(squares+[squares[0]],row['side'])['valid'])
            self.assertFalse(verify(squares,row['side']-F(1,10**30))['valid'])

    def test_exact_offcentre_bound_is_selected_and_propagated_by_deletion(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'certificates').mkdir()
            (root/'known_best.json').write_text(json.dumps({'entries':{}}))
            (root/'records.txt').write_text('')
            (root/'friedman_bounds.json').write_text(json.dumps(generate(max_n=368)))
            with patch.object(regen_bounds,'ROOT',root):entries=regen_bounds.render(368)['entries']
            expected=Q2(F(21,2),F(13,2))
            self.assertEqual(exact_value(entries['368']['verified']),expected)
            row=entries['367']['verified']
            self.assertEqual(exact_value(row),expected)
            self.assertEqual(row['source_n'],368)
            self.assertEqual(row['deleted_squares'],1)


if __name__=='__main__':unittest.main()
