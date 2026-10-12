import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import search_forever as search
from search_methods import load_weights


class FocusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/"records").mkdir()
        self.focus = [69, 83, 87]
        for n in [68, 69, 70, 82, 83, 84, 86, 87, 88]:
            (self.root/f"records/n{n}.txt").write_text(f"# source n={n}\n")
        (self.root/"records.txt").write_text("69 8.827\n83 9.634\n87 9.838\n")
        self.patch = patch.object(search, "HERE", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_remote_all_targets_and_methods_with_matching_seeds(self):
        seen = {n:set() for n in self.focus}
        counts = {n:0 for n in self.focus}
        weights = {"hop":.40, "slp":.15, "gpu":.15, "drop":.15, "grow":.10, "random":.05}
        with patch.object(search, "load_weights", return_value=weights):
            for i in range(108):
                job = search.choose_job(30000+i, host="remote", rotation=i, focus=self.focus)
                n, method = job["n"], job["method"]
                self.assertIn(n, self.focus)
                counts[n] += 1
                seen[n].add(method)
                seed_n = n+(1 if method == "drop" else -1 if method == "grow" else 0)
                self.assertEqual(job["packing"], f"# source n={seed_n}\n")
                self.assertEqual(job["range_group"], "focus")
        self.assertEqual(set(counts.values()), {36})
        for methods in seen.values():
            self.assertEqual(methods, {"hop", "slp", "gpu", "drop", "grow", "random"})

    def test_disabled_methods_are_not_forced_at_periodic_slots(self):
        with patch.object(search, "PRIORITY", self.focus), \
             patch.object(search, "load_weights", return_value={"slp":1.}):
            for focus in (None, self.focus):
                for counter in (22, 120, 143, 241, 362):
                    job = search.choose_job(counter, host="remote", rotation=0, max_n=324, focus=focus)
                    self.assertEqual(job["method"], "slp")

    def test_local_slots_redistribute_gpu_weight(self):
        with patch.object(search, "load_weights", return_value={"gpu":.5, "slp":.5}):
            for counter in range(20):
                job = search.choose_job(counter, host="local", focus=self.focus)
                self.assertEqual(job["method"], "slp")

    def test_reviewed_defaults_disable_zero_yield_methods(self):
        weights = load_weights(self.root)
        self.assertAlmostEqual(sum(weights.values()), 1.)
        self.assertTrue({"graft", "grow", "random", "compress"}.isdisjoint(weights))

    def test_local_can_use_unbeaten_references_and_varies_radius(self):
        seen = {n:set() for n in self.focus}
        for i in range(63):
            job = search.choose_local_cycle(30000+i, i, focus=self.focus)
            n = job["n"]
            self.assertIn(n, self.focus)
            self.assertEqual(job["packing"], f"# source n={n}\n")
            self.assertTrue(job["repair_seed"])
            seen[n].add(job["radius"])
        for radii in seen.values():
            self.assertEqual(radii, {.003, .01, .02})

    def test_saved_configuration_and_validation(self):
        self.assertEqual(search.load_focus(), [])
        p = self.root/"search_focus.json"
        p.write_text(json.dumps({"targets": self.focus}))
        self.assertEqual(search.load_focus(), self.focus)
        for targets in ([], [69,69], [999], [71]):
            p.write_text(json.dumps({"targets": targets}))
            with self.assertRaises(ValueError):
                search.load_focus()


if __name__ == "__main__":
    unittest.main()
