#!/usr/bin/env python3
"""Tests for scripts/wave_driver.py v1 — the ACT stage.

Covers: the 10-tick/2-lane self-test (subprocess, exit-code check), the three
per-lane gates, the op-ledger exactly-once resume rule, and the deterministic
worker's fault modes. Stdlib only. Zero live-file contact (all state in temp).
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import wave_driver  # noqa: E402


class GatesTest(unittest.TestCase):
    """Gate 2/3 (gate 1, the steer verify, is exercised by every self-test tick)."""

    def _state(self, **lane_kw):
        state = {"lanes": {"alpha": lane_kw}}
        return state

    def test_quota_frozen_blocks(self):
        ok, why = wave_driver._lane_gates(
            self._state(), "alpha", {"quota_frozen_ticks": 1}, [], 6)
        self.assertFalse(ok)
        self.assertEqual(why, "quota-frozen")

    def test_clamp_blocks(self):
        ok, why = wave_driver._lane_gates(
            self._state(acts=6), "alpha", {"quota_frozen_ticks": 0}, [], 6)
        self.assertFalse(ok)
        self.assertEqual(why, "clamp")

    def test_halt_blocks(self):
        ok, why = wave_driver._lane_gates(
            self._state(halted=True), "alpha", {}, [], 6)
        self.assertFalse(ok)
        self.assertEqual(why, "halted(halt-not-hammer)")

    def test_open_lane_passes(self):
        ok, why = wave_driver._lane_gates(
            self._state(acts=1), "alpha", {"quota_frozen_ticks": 0}, [], 6)
        self.assertTrue(ok)
        self.assertEqual(why, "")


class LedgerScanTest(unittest.TestCase):
    """intent -> effect -> resume semantics; re-issue exactly once, ever."""

    def _write(self, tmp, rows):
        path = os.path.join(tmp, "op_ledger.jsonl")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for r in rows:
                fh.write(json.dumps(r) + "\n")
        return path

    def test_pending_intent_is_resumable(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, [{"kind": "intent", "op_id": "a"}])
            scan = wave_driver._ledger_scan(p)
            self.assertEqual(len(scan["resumable"]), 1)

    def test_effect_closes_intent(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, [{"kind": "intent", "op_id": "a"},
                                  {"kind": "effect", "op_id": "a"}])
            scan = wave_driver._ledger_scan(p)
            self.assertEqual(scan["pending"], [])

    def test_resolved_resume_closes_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, [{"kind": "intent", "op_id": "a"},
                                  {"kind": "resume", "op_id": "a",
                                   "reissued_as": "a-r"},
                                  {"kind": "effect", "op_id": "a-r"}])
            scan = wave_driver._ledger_scan(p)
            self.assertEqual(scan["pending"], [])

    def test_exhausted_resume_never_resumable_again(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self._write(tmp, [{"kind": "intent", "op_id": "a"},
                                  {"kind": "resume", "op_id": "a",
                                   "reissued_as": "a-r"}])
            scan = wave_driver._ledger_scan(p)
            self.assertEqual(len(scan["pending"]), 1)
            self.assertEqual(scan["resumable"], [])


class WorkerTest(unittest.TestCase):
    """Deterministic hash-compute worker, no LLM; fault modes by contract."""

    def _run_worker(self, fault):
        tmp = tempfile.mkdtemp(prefix="wave_worker_test_")
        lane_dir = os.path.join(tmp, "lanes", "alpha")
        os.makedirs(os.path.join(lane_dir, "tasks"), exist_ok=True)
        task = {"op_id": "t1", "lane": "alpha", "payload": {"x": 1},
                "payload_sha": "0" * 64, "rounds": 8, "fault": fault,
                "resumed_from": None, "ts": "now", "seat": "test", "tick": 1}
        task_path = os.path.join(lane_dir, "tasks", "t1.json")
        with open(task_path, "w", encoding="utf-8") as fh:
            json.dump(task, fh)
        rc = wave_driver.worker_main(task_path)
        ledger = wave_driver._read_jsonl(os.path.join(lane_dir, "op_ledger.jsonl"))
        return rc, ledger

    def test_clean_worker_effect_ok(self):
        rc, ledger = self._run_worker("")
        self.assertEqual(rc, 0)
        self.assertEqual(ledger[-1]["kind"], "effect")
        self.assertEqual(ledger[-1]["status"], "OK")
        # contract: chain starts at payload_sha, one sha256 per round
        h = task_sha = "0" * 64
        for _ in range(8):
            h = wave_driver.hashlib.sha256(h.encode("utf-8")).hexdigest()
        self.assertEqual(task_sha, "0" * 64)  # guard: chain seed unchanged
        self.assertEqual(ledger[-1]["result_sha"], h)

    def test_fail_worker_effect_failed(self):
        rc, ledger = self._run_worker("fail")
        self.assertEqual(rc, 3)
        self.assertEqual(ledger[-1]["status"], "FAILED")

    def test_crash_worker_leaves_no_effect(self):
        rc, ledger = self._run_worker("crash")
        self.assertEqual(rc, 3)
        self.assertEqual([r for r in ledger if r.get("kind") == "effect"], [])


class SelfTestIntegration(unittest.TestCase):
    """The full 10-tick/2-lane kifu run, in its own process."""

    def test_selftest_passes(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(ROOT, "scripts", "wave_driver.py"),
             "--selftest"], capture_output=True, text=True, cwd=ROOT, timeout=300)
        self.assertEqual(proc.returncode, 0,
                         msg=proc.stdout[-2000:] + proc.stderr[-2000:])
        self.assertIn("SELFTEST PASS", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
