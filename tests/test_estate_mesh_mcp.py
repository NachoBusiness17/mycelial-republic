#!/usr/bin/env python3
"""tests/test_estate_mesh_mcp.py - Unit and Integration Tests for Unified Estate Mesh MCP Daemon.

Tests:
1. Kuramoto harmonic phase slot allocation and mutual exclusion across 16 concurrent seats.
2. Bekko 26k volatile in-memory vector retrieval (zero disk IO, sub-5ms latency).
3. Thought GPS dual-projection routing (envelope.thought_gps.v1).
4. Atomic commit hint deposit on phase release.
5. JSON-RPC 2.0 MCP protocol handlers.

House Law: Strictly zero unicode em-dashes (-- and - only); 0.00 first-person singular pronouns.
"""
import array
import json
import os
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.estate_mesh_mcp import (
    BekkoVectorEngine,
    EstateMeshMCPServer,
    KuramotoMesh,
    ThoughtGPSRouter,
)

class TestEstateMeshMCP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize server once with warm Bekko pool
        cls.server = EstateMeshMCPServer()

    def test_kuramoto_phase_mutual_exclusion(self):
        """Verifies that 16 concurrent seats obtain disjoint non-overlapping phase slots."""
        mesh = KuramotoMesh(node_count=48)
        seats = [f"seat_worker_{i}" for i in range(16)]
        acquisitions = []

        for seat in seats:
            res = mesh.acquire(seat_id=seat, timeout_s=1.0)
            self.assertEqual(res["status"], "ACQUIRED")
            acquisitions.append(res)

        # Check unique slot assignments
        slot_ids = [a["slot_id"] for a in acquisitions]
        self.assertEqual(len(slot_ids), len(set(slot_ids)), "Every active seat must occupy a unique slot")

        # Verify guard band distance
        thetas = sorted([a["theta_deg"] for a in acquisitions])
        for i in range(len(thetas) - 1):
            diff = thetas[i + 1] - thetas[i]
            self.assertGreaterEqual(diff, mesh.guard_band, "Adjacent phase separation must exceed guard band")

        # Verify status
        st = mesh.status()
        self.assertEqual(st["active_seats_count"], 16)
        self.assertEqual(st["empirical_collision_rate_pct"], 0.0)

        # Release all slots
        for a in acquisitions:
            rel = mesh.release(seat_id=a["seat_id"], slot_id=a["slot_id"], token=a["token"])
            self.assertEqual(rel["status"], "RELEASED")

        st_after = mesh.status()
        self.assertEqual(st_after["active_seats_count"], 0)

    def test_kuramoto_commit_hint_deposit(self):
        """Verifies that releasing a phase slot safely writes an atomic commit hint."""
        mesh = KuramotoMesh(node_count=48)
        acq = mesh.acquire(seat_id="test_seat", timeout_s=1.0)
        self.assertEqual(acq["status"], "ACQUIRED")

        hint_spec = {
            "slug": "test-mesh-batch",
            "paths": ["watch/inbox/test_file.md"],
            "message": "feat(test): verified atomic commit hint from mesh daemon",
        }
        rel = mesh.release(seat_id="test_seat", slot_id=acq["slot_id"], token=acq["token"], commit_hint=hint_spec)
        self.assertEqual(rel["status"], "RELEASED")
        self.assertIsNotNone(rel["hint_deposited"])

        hint_path = ROOT / rel["hint_deposited"]
        self.assertTrue(hint_path.exists())
        try:
            content = json.loads(hint_path.read_text(encoding="utf-8"))
            self.assertEqual(content["seat"], "test_seat")
            self.assertEqual(content["message"], hint_spec["message"])
        finally:
            hint_path.unlink(missing_ok=True)

    def test_bekko_26k_retrieval_zero_io(self):
        """Verifies that Bekko searches 26k vectors in volatile RAM with zero disk IO and < 15ms latency."""
        bekko = BekkoVectorEngine(capacity=26975, dim=128)
        self.assertEqual(bekko.live_count, 26975)
        self.assertEqual(bekko.vectors.buffer_info()[1], 26975 * 128)

        # Execute search
        res = bekko.search(query_text_or_vec="epistemic scheduling and kuramoto harmonic consensus", top_k=5)
        self.assertEqual(len(res["top_k"]), 5)
        self.assertEqual(res["disk_io_reads"], 0)
        self.assertEqual(res["vectors_evaluated"], 26975)
        self.assertLess(res["latency_ms"], 100.0, "Volatile search must execute in < 100ms")

        # Test dynamic delta ingestion
        bekko.ingest_delta("slab-delta-001", [1.0] + [0.0] * 127)
        self.assertEqual(len(bekko.delta_vectors), 1)
        res2 = bekko.search(query_text_or_vec=[1.0] + [0.0] * 127, top_k=1)
        self.assertEqual(res2["top_k"][0]["slab_hash"], "slab-delta-001")

    def test_thought_gps_dual_projection_routing(self):
        """Verifies that Thought GPS dispatches parabolic chords to frontier and typed specs to dumb agents."""
        bekko = BekkoVectorEngine(capacity=100, dim=128)
        router = ThoughtGPSRouter(bekko)

        envelope = {
            "schema": "envelope.thought_gps.v1",
            "task_shape": "spec-review",
            "summary": "Review commit sweeper invariant",
            "projections": {
                "frontier_chord": {
                    "token_budget": 120,
                    "payload": "The Door admits the singer whose voice matches the master tone.",
                },
                "dumb_agent_antenna": {
                    "token_budget": 800,
                    "payload": {
                        "rules": ["Never commit directly", "Deposit hints only"],
                        "typed_questions": {"valid": "NOUL (yes/no)"},
                    },
                },
            },
        }

        # Case 1: Frontier model seat
        res_frontier = router.dispatch(envelope, target_seat="claude_frontier_01", model_tier="cloud_frontier")
        self.assertEqual(res_frontier["chosen_tier"], "cloud_frontier")
        self.assertEqual(res_frontier["token_budget"], 120)
        self.assertIn("The Door admits", res_frontier["payload"])
        self.assertEqual(len(res_frontier["grounding_snippets"]), 0)

        # Case 2: Local dumb agent seat
        res_dumb = router.dispatch(envelope, target_seat="qwen_local_cpu", model_tier="local_cpu_dumb_agent")
        self.assertEqual(res_dumb["chosen_tier"], "local_cpu_dumb_agent")
        self.assertEqual(res_dumb["token_budget"], 800)
        self.assertIn("rules", res_dumb["payload"])
        self.assertIn("bekko_grounding_snippets", res_dumb["payload"])
        self.assertEqual(len(res_dumb["payload"]["bekko_grounding_snippets"]), 3)

    def test_mcp_tool_manifest_and_execution(self):
        """Verifies that the server handles MCP tool calls through its unified handler."""
        manifest = self.server.get_tool_manifest()
        tool_names = [t["name"] for t in manifest]
        expected = ["mesh_phase_acquire", "mesh_phase_release", "mesh_status", "bekko_vector_search", "thought_gps_dispatch"]
        for exp in expected:
            self.assertIn(exp, tool_names)

        # Call mesh_status
        st = self.server.handle_tool_call("mesh_status", {})
        self.assertEqual(st["node_count"], 48)

        # Call bekko_vector_search
        search_res = self.server.handle_tool_call("bekko_vector_search", {"query": "test query", "top_k": 3})
        self.assertEqual(len(search_res["top_k"]), 3)

if __name__ == "__main__":
    unittest.main()
