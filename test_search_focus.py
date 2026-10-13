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


class LocalConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        context = patch.object(search, "HERE", self.root)
        context.start()
        self.addCleanup(context.stop)

    def parse(self, *arguments):
        with patch("sys.argv", ["search_forever.py", "coordinator", *arguments]), \
             patch.object(search, "coordinator") as coordinator:
            search.main()
        return coordinator.call_args.args[0]

    def test_default_search_uses_no_private_remote(self):
        args = self.parse()
        self.assertEqual(args.remote_jobs, 0)
        self.assertIsNone(args.remote)
        self.assertIsNone(args.remote_root)

    def test_private_hosts_configuration_and_cli_override(self):
        (self.root/"search_hosts.json").write_text(json.dumps({
            "remote": "search@example.test", "remote_root": "/srv/packing", "remote_jobs": 3}))
        args = self.parse()
        self.assertEqual((args.remote, args.remote_root, args.remote_jobs),
                         ("search@example.test", "/srv/packing", 3))
        args = self.parse("--remote", "override@example.test", "--remote-jobs", "1")
        self.assertEqual((args.remote, args.remote_jobs), ("override@example.test", 1))

    def test_remote_jobs_require_both_connection_arguments(self):
        with patch("sys.stderr", search.io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                self.parse("--remote-jobs", "1", "--remote", "search@example.test")
        self.assertEqual(raised.exception.code, 2)

    def test_missing_private_notification_module_is_a_noop(self):
        with patch.dict("sys.modules", {"notify": None}):
            search.notify_record({"n": 84}, {"after": "9.7"})

    def test_private_notification_callback_receives_the_record(self):
        from types import SimpleNamespace
        from unittest.mock import Mock
        callback = Mock()
        job, entry = {"n": 84}, {"after": "9.7"}
        with patch.dict("sys.modules", {"notify": SimpleNamespace(notify_record=callback)}):
            search.notify_record(job, entry)
        callback.assert_called_once_with(job, entry)


if __name__ == "__main__":
    unittest.main()
