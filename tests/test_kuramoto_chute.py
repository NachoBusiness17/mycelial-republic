#!/usr/bin/env python3
"""tests/test_kuramoto_chute.py - Unit tests for Kuramoto Phase Chute & Bartnik Gate.

Validates:
1. Periodic system phase mapping theta(t) in [0, 2pi).
2. Phase window detection for fleet nodes (Desktop, Bob, Pixel).
3. Bartnik Hamiltonian boundary flux calculation and fail-closed rejection.
4. Single-writer commit hint emission.

HOUSE LAW: Strictly zero unicode em-dashes; standard library only.
"""
from __future__ import annotations

import math
import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.kuramoto_chute import KuramotoChute, NODE_PHASE_OFFSETS


class TestKuramotoChute(unittest.TestCase):
    def setUp(self) -> None:
        self.test_queue = tempfile.mkdtemp(prefix="test_hint_queue_")
        self.chute = KuramotoChute(queue_dir=self.test_queue, cycle_period_s=60.0, max_flux=50.0)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_queue, ignore_errors=True)

    def test_phase_window_detection(self) -> None:
        # At t=0s, system_phase = 0.0 rad. Desktop target is 0.0 rad -> should be OPEN.
        res = self.chute.check_phase_window("desktop", t=0.0)
        self.assertEqual(res["node_id"], "desktop")
        self.assertTrue(res["window_open"])
        self.assertEqual(res["wait_seconds_to_open"], 0.0)

        # Pixel target is 3.1416 rad (180 deg). At t=0s, angular distance is large -> should be CLOSED.
        p_res = self.chute.check_phase_window("pixel", t=0.0)
        self.assertFalse(p_res["window_open"])
        self.assertGreater(p_res["wait_seconds_to_open"], 0.0)

        # At t=30s (1/2 of 60s), system_phase ~= 3.1416 rad -> Pixel window should be OPEN.
        p_open = self.chute.check_phase_window("pixel", t=30.0)
        self.assertTrue(p_open["window_open"])

    def test_bartnik_boundary_admission_pass_and_fail(self) -> None:
        # Initial empty queue -> flux is low, admission passes
        adm = self.chute.admit_mutation("desktop", "test_task", payload_bytes=500, t=0.0)
        self.assertTrue(adm["admitted"])
        self.assertLess(adm["boundary_flux"], 50.0)

        # Artificially create low flux threshold to trigger Bartnik boundary refusal
        strict_chute = KuramotoChute(queue_dir=self.test_queue, max_flux=1.0)
        # Create a few dummy files in queue to saturate flux
        for i in range(2):
            with open(os.path.join(self.test_queue, f"hint_{i}.json"), "w") as fp:
                fp.write("{}")

        refused = strict_chute.admit_mutation("desktop", "flood_task", payload_bytes=1000, t=0.0)
        self.assertFalse(refused["admitted"])
        self.assertEqual(refused["reason"], "REFUSED_IRREVERSIBILITY_EXCEEDED")

    def test_emit_commit_hint(self) -> None:
        # Emit with bypass_phase=True to verify atomic hint write
        payload = {"action": "UPDATE_MEM_SLAB", "hash": "abc12345"}
        res = self.chute.emit_commit_hint("bob", "bob_slab_update", payload, bypass_phase=True)
        self.assertTrue(res["emitted"])
        self.assertTrue(os.path.isfile(res["hint_path"]))

        # Verify hint file content
        with open(res["hint_path"], "r", encoding="utf-8") as fp:
            import json
            doc = json.load(fp)
            self.assertEqual(doc["node_id"], "bob")
            self.assertEqual(doc["payload"]["action"], "UPDATE_MEM_SLAB")


if __name__ == "__main__":
    unittest.main()
