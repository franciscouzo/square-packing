"""CSV identity, exact grids, and safe decimal conversion of rotated contacts."""
import csv
from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest

import mpmath as mp

from gobel_bounds import Q2
import prepare_kaggle as export


class KaggleExportTests(unittest.TestCase):
    def test_polynomial_without_an_explicit_coefficient_array(self):
        self.assertEqual(export.field_polynomial(dict(
            polynomial='t^7-9*t^6+3*t^5-t^4-t^3+t^2-3*t+1')),
            list(map(F, [1,-9,3,-1,-1,1,-3,1])))

    def test_csv_grids_and_rotated_touching_squares(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'certificates/best').mkdir(parents=True)
            upper={str(n):dict(verified=dict(bound=str(1 if n==1 else 2),source='integer square grid',
                                            credit='square grid'))for n in range(1,5)}
            side=Q2(2,F(1,2))
            upper['5']=dict(verified=dict(bound=str(side.enclosure()[1]),exact_bound=side.record(),
                source='classical construction',credit='Frits Göbel',family='square',a=1,b=1))
            (root/'upper_bounds.json').write_text(json.dumps(dict(entries=upper)))
            (root/'certified_bounds.json').write_text(json.dumps(dict(entries={})))
            (root/'certificates/best/manifest.json').write_text(json.dumps(dict(witnesses={})))
            output=root/'output';export.export(root,output,limit=5)
            with(output/'submission.csv').open()as f:
                reader=csv.DictReader(f);self.assertEqual(reader.fieldnames,export.COLUMNS);rows=list(reader)
            self.assertEqual([int(r['id'])for r in rows],list(range(15)))
            self.assertEqual([int(r['square_id'])for r in rows if r['n']=='5'],list(range(5)))
            with mp.workdps(100):
                grid=[tuple(mp.mpf(r[k])for k in ['x','y','angle'])for r in rows if r['n']=='4']
                self.assertEqual(grid,[(mp.mpf('.5'),mp.mpf('.5'),0),(mp.mpf('1.5'),mp.mpf('.5'),0),
                                      (mp.mpf('.5'),mp.mpf('1.5'),0),(mp.mpf('1.5'),mp.mpf('1.5'),0)])
                rotated=[tuple(mp.mpf(r[k])for k in ['x','y','angle'])for r in rows if r['n']=='5']
                for i,(x,y,t)in enumerate(rotated):
                    for X,Y,T in rotated[i+1:]:
                        radius=(1+abs(mp.cos(T-t))+abs(mp.sin(T-t)))/2
                        separation=max(abs((X-x)*mp.cos(a)+(Y-y)*mp.sin(a))-radius
                                       for a in [t,t+mp.pi/2,T,T+mp.pi/2])
                        self.assertGreater(separation,0)
                extents=[(x,y,(abs(mp.cos(t))+abs(mp.sin(t)))/2)for x,y,t in rotated]
                measured=max(max(x+h for x,y,h in extents)-min(x-h for x,y,h in extents),
                             max(y+h for x,y,h in extents)-min(y-h for x,y,h in extents))
                self.assertLess(abs(measured-(2+mp.sqrt(2)/2)),mp.mpf('1e-35'))


if __name__=='__main__':unittest.main()
