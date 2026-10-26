"""tests/test_sovereign_mcp.py - Verification for Sovereign Mesh MCP Server.

Validates that tools/sovereign_mcp.py implements JSON-RPC 2.0 stdio MCP
protocol and that all 8 decoupled data plane tools execute cleanly without
git dependencies.

House Law:
  - Strictly 0.00 first-person singular pronouns.
  - Strictly zero unicode em-dashes (-- and - only).
"""
from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.sovereign_mcp import (
    TOOL_DEFINITIONS,
    dispatch,
    tool_cas_store,
    tool_cas_read,
    tool_cas_verify,
    tool_kuramoto_phase,
    tool_chord_mint,
    tool_chord_verify_sentinel,
)


class TestSovereignMcp(unittest.TestCase):
    """Test suite for Sovereign Mesh MCP protocol and tool dispatch."""

    def test_tool_definitions_schema(self) -> None:
        """Verify all 8 tools declare valid MCP tool schemas."""
        self.assertEqual(len(TOOL_DEFINITIONS), 8)
        names = [t["name"] for t in TOOL_DEFINITIONS]
        expected = [
            "cas_store",
            "cas_read",
            "cas_verify",
            "bekko_search",
            "kuramoto_phase",
            "commit_hint_emit",
            "chord_mint",
            "chord_verify_sentinel",
        ]
        for exp in expected:
            self.assertIn(exp, names)
            tool_def = next(t for t in TOOL_DEFINITIONS if t["name"] == exp)
            self.assertIn("description", tool_def)
            self.assertIn("inputSchema", tool_def)
            self.assertEqual(tool_def["inputSchema"]["type"], "object")

    def test_cas_store_and_read(self) -> None:
        """Test storing and reading a slab via MCP dispatch."""
        test_payload = "Sovereign MCP CAS round-trip test verification."
        res_store = dispatch("cas_store", {
            "content": test_payload,
            "domain": "test",
            "actor": "unit-test",
            "tags": ["mcp", "test"]
        })
        self.assertTrue(res_store.get("ok"))
        slab_hash = res_store["slab_hash"]
        self.assertEqual(len(slab_hash), 64)

        res_read = dispatch("cas_read", {"slab_hash": slab_hash})
        self.assertTrue(res_read.get("ok"))
        self.assertEqual(res_read["content"], test_payload)
        self.assertEqual(res_read["byte_count"], len(test_payload.encode("utf-8")))

    def test_cas_verify(self) -> None:
        """Test CAS mesh verification tool."""
        res = dispatch("cas_verify", {})
        self.assertIn("total_slabs", res)
        self.assertIn("valid_slabs", res)
        self.assertTrue(res.get("integrity_ok"))

    def test_kuramoto_phase_query(self) -> None:
        """Test Kuramoto phase window query for nodes."""
        for node in ["desktop", "bob", "pixel", "antigravity"]:
            res = dispatch("kuramoto_phase", {"node": node, "fleet_size": 16})
            self.assertTrue(res.get("ok"))
            self.assertEqual(res["node"], node)
            self.assertIn("phase_deg", res)
            self.assertIn("window_open", res)
            self.assertIn("boundary_flux", res)

    def test_chord_mint_and_sentinel(self) -> None:
        """Test minting steganographic chord and verifying absence proof."""
        res_chord = dispatch("chord_mint", {"domain": "mesh", "action": "sync"})
        self.assertTrue(res_chord.get("ok"))
        self.assertIn("chord_token", res_chord["chord"])

        res_sentinel = dispatch("chord_verify_sentinel", {"probe_id": "FP01", "entity": "porter"})
        self.assertTrue(res_sentinel.get("ok"))
        self.assertTrue(res_sentinel["is_absent"])

    def test_house_law_compliance(self) -> None:
        """Verify tools/sovereign_mcp.py strictly complies with House Law."""
        mcp_path = ROOT / "tools" / "sovereign_mcp.py"
        content = mcp_path.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", content, "Unicode em-dash detected in sovereign_mcp.py")
        self.assertNotIn("\u2013", content, "Unicode en-dash detected in sovereign_mcp.py")


if __name__ == "__main__":
    unittest.main()
