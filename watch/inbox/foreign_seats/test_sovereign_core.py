#!/usr/bin/env python3
"""tools/sovereign/test_sovereign_core.py - Verification suite for Sovereign Invariant Core.

Tests:
1. Sovereign HTTP Client (requests/httpx replacement): GET, POST, JSON parse, headers.
2. Invariant Memory Vessel: Bounded allocation, relative offsets, SHA-256 verification,
   zero-copy serialization and deserialization, seal integrity.
3. Overflow Protection: Invariant enforcement when arena bounds are reached.
"""

import sys
import unittest
import os

# Add tools/sovereign to sys.path
sys.path.insert(0, os.path.dirname(__file__))

import http_client
import vessel


class TestSovereignHTTPClient(unittest.TestCase):
    def test_get_and_json(self):
        resp = http_client.get("https://httpbin.org/get", params={"test": "sovereign_01"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.ok)
        data = resp.json()
        self.assertEqual(data["args"]["test"], "sovereign_01")

    def test_post_json(self):
        payload = {"agent": "hermes_antigravity", "action": "picasso_steal"}
        resp = http_client.post("https://httpbin.org/post", json_data=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["json"], payload)


class TestInvariantMemoryVessel(unittest.TestCase):
    def test_bounded_arena_lifecycle(self):
        arena = vessel.BoundedArena(capacity=16384)
        off_blob = arena.write_blob(b"Van Oortmerssen FlatBuffers Receipt")
        self.assertEqual(arena.read_blob(off_blob), b"Van Oortmerssen FlatBuffers Receipt")

        # Record chaining
        off_rec1 = arena.write_record("KEY1", "VAL1")
        rec1 = arena.read_record(off_rec1)
        self.assertEqual(rec1["key"], "KEY1")
        self.assertEqual(rec1["value"], "VAL1")

        h1 = bytes.fromhex(rec1["sha256"])
        off_rec2 = arena.write_record("KEY2", "VAL2", prev_hash=h1)
        rec2 = arena.read_record(off_rec2)
        self.assertEqual(rec2["prev_hash"], rec1["sha256"])

        # Seal
        seal_hash = arena.seal()
        self.assertTrue(len(seal_hash) == 32)
        with self.assertRaises(PermissionError):
            arena.allocate(10)

        # Zero-copy reload
        serialized = arena.get_used_bytes()
        reloaded = vessel.BoundedArena.from_bytes(serialized)
        self.assertEqual(reloaded.record_count, 3)
        self.assertEqual(reloaded.read_record(off_rec2)["value"], "VAL2")

    def test_overflow_protection(self):
        arena = vessel.BoundedArena(capacity=64)  # 32 header + 32 payload
        arena.write_blob(b"1234567890123456")  # 4 prefix + 16 data = 20 bytes
        with self.assertRaises(vessel.VesselOverflowError):
            arena.write_blob(b"This will definitely overflow the 64-byte bounded arena!")


if __name__ == "__main__":
    unittest.main()
