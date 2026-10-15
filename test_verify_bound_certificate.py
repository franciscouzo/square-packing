"""Pair coverage and verdict agreement with the original exact verifier."""
from fractions import Fraction as F
import importlib.util
from pathlib import Path
import random
import unittest

from verify_bound_certificate import candidate_pairs,verify


class ExactBoundVerifier(unittest.TestCase):
    def test_every_pair_with_intersecting_circumscribed_discs_is_enumerated(self):
        rng=random.Random(237)
        squares=[(F(rng.randrange(-100,100),7),F(rng.randrange(-100,100),11),F(1),F(0)) for _ in range(80)]
        pairs=set(candidate_pairs(squares))
        for i in range(len(squares)):
            for j in range(i+1,len(squares)):
                dx=squares[i][0]-squares[j][0];dy=squares[i][1]-squares[j][1]
                if dx*dx+dy*dy<=2:self.assertIn((i,j),pairs)

    def test_closed_feasibility_is_distinct_from_strict_separation(self):
        squares=[(F(1,2),F(1,2),F(1),F(0)),(F(3,2),F(1,2),F(1),F(0))]
        result=verify(2,F(2),squares)
        self.assertTrue(result['valid']);self.assertFalse(result['strict_valid'])
        self.assertFalse(verify(2,F(2),[squares[0],squares[0]])['valid'])

    def test_strict_verdict_matches_original_geometry_on_valid_and_invalid_inputs(self):
        path=Path(__file__).parent/'external/evand/search/exact/verify_cert.py'
        if not path.exists():self.skipTest('Optional upstream comparison checkout is unavailable')
        spec=importlib.util.spec_from_file_location('original_evand_verify',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        cases=[(2,F(3),[(F(3,4),F(3,4),F(1),F(0)),(F(9,4),F(9,4),F(1),F(0))]),
               (2,F(3),[(F(3,4),F(3,4),F(1),F(0))]*2),
               (1,F(1),[(F(1,2),F(1,2),F(1),F(0))])]
        for n,S,squares in cases:
            self.assertEqual(verify(n,S,squares)['strict_valid'],module.verify(n,S,squares,verbose=False)[0])


if __name__=='__main__':unittest.main()
