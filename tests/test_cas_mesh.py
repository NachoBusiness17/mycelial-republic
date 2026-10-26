#!/usr/bin/env python3
"""tests/test_cas_mesh.py - Verification for CAS Mesh and EPGM Provenance.

Validates:
1. Deterministic content-addressed storage (SHA-256).
2. Atomic write, retrieval, and corrupt-detection.
3. EPGM provenance sidecar tracking with parent links.
4. Mesh verification and manifest generation.

HOUSE LAW: Strictly zero unicode em-dashes; standard library only.
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.cas_mesh import CasMesh, compute_sha256


class TestCasMesh(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="test_cas_mesh_")
        self.mesh = CasMesh(base_dir=self.test_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_put_and_get_roundtrip(self) -> None:
        data = b"Hello sovereign mesh: 10 TB shared invariant slab!"
        expected_hash = compute_sha256(data)

        rec = self.mesh.put_slab(data, actor_seat="pixel-grokbot", labels=["test", "slab"])
        self.assertEqual(rec["content_hash"], expected_hash)
        self.assertEqual(rec["byte_size"], len(data))
        self.assertEqual(rec["actor_seat"], "pixel-grokbot")
        self.assertTrue(self.mesh.has_slab(expected_hash))

        retrieved_data, retrieved_epgm = self.mesh.get_slab(expected_hash)
        self.assertEqual(retrieved_data, data)
        self.assertEqual(retrieved_epgm["content_hash"], expected_hash)
        self.assertEqual(retrieved_epgm["actor_seat"], "pixel-grokbot")

    def test_causal_parent_chain(self) -> None:
        parent_data = b"Genesis invariant block"
        p_rec = self.mesh.put_slab(parent_data, actor_seat="desktop-gpu")
        p_hash = p_rec["content_hash"]

        child_data = b"Subsequent transaction block"
        c_rec = self.mesh.put_slab(child_data, actor_seat="bob-laptop", causal_parent=p_hash)
        self.assertEqual(c_rec["causal_parent"], p_hash)

        # Verify mesh passes cleanly
        report = self.mesh.verify_mesh()
        self.assertTrue(report["integrity_ok"])
        self.assertEqual(report["total_slabs"], 2)
        self.assertEqual(len(report["missing_parent_links"]), 0)

    def test_detect_corrupted_slab(self) -> None:
        data = b"Pure immutable bytes"
        rec = self.mesh.put_slab(data, actor_seat="witness")
        h = rec["content_hash"]

        # Corrupt the slab file directly
        slab_path = self.mesh._slab_path(h)
        with open(slab_path, "wb") as fp:
            fp.write(b"Tampered bytes!")

        # get_slab should raise ValueError on corruption
        with self.assertRaises(ValueError):
            self.mesh.get_slab(h)

        # verify_mesh should flag it
        report = self.mesh.verify_mesh()
        self.assertFalse(report["integrity_ok"])
        self.assertIn(h, report["corrupted_slabs"])

    def test_manifest_export(self) -> None:
        self.mesh.put_slab(b"item A", actor_seat="seat1")
        self.mesh.put_slab(b"item B", actor_seat="seat2")

        manifest = self.mesh.export_mesh_manifest()
        self.assertEqual(manifest["slab_count"], 2)
        self.assertTrue(len(manifest["mesh_root_hash"]) == 64)
        self.assertEqual(len(manifest["slabs"]), 2)


if __name__ == "__main__":
    unittest.main()
