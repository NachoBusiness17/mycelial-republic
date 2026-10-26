#!/usr/bin/env python3
"""tests/test_chord_minter.py - Unit tests for Steganographic Chord Minter.

Validates:
1. Deterministic chord generation and phase angle computation.
2. Embedding of Hayashi false-premise sentinels.
3. Codebook agreement verification: passes on rejection, fails on affirmation.
4. 7-wide operational fleet chord synthesis and Kuramoto order parameter.
5. Full 48-chord library evaluation across 10 Optics Lenses.
6. 96-case Hayashi false-premise test battery certification.

HOUSE LAW: Strictly zero unicode em-dashes; standard library only; pure functions;
0.00 first-person singular pronouns.
"""
from __future__ import annotations

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.isdir(os.path.join(ROOT, "canon")) and os.path.isdir("/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/canon"):
    ROOT = "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent"
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.chord_minter import ChordMinter


class TestChordMinter(unittest.TestCase):
    def setUp(self) -> None:
        self.minter = ChordMinter()

    def test_mint_chord_structure(self) -> None:
        chord = self.minter.mint_chord(
            domain="storage",
            opcode="SLAB_SYNC",
            target="pixel_11_pro",
            intensity=0.95,
            include_sentinel=True,
        )
        self.assertEqual(chord["schema"], "steganographic_chord.v1")
        self.assertEqual(chord["domain"], "storage")
        self.assertEqual(chord["opcode"], "SLAB_SYNC")
        self.assertTrue(chord["chord_token"].startswith("CHORD[storage:SLAB:"))
        self.assertTrue(0.0 <= chord["phase_rad"] <= 6.29)
        self.assertIn("pixel_11_pro", chord["parable"])
        self.assertTrue(chord["sentinel_embedded"])
        self.assertIsNotNone(chord["sentinel_probe"])

    def test_hayashi_agreement_passes_on_rejection(self) -> None:
        chord = self.minter.mint_chord(
            domain="compute",
            opcode="PHASE_LOCK",
            target="desktop_7c70ksc",
            include_sentinel=True,
            probe_idx=0,  # "the slate roofer" / "slate roofer"
        )
        absent = chord["sentinel_probe"]["absent_entity"]

        # Receiver correctly rejects the false premise
        receiver_response = f"Acknowledged PHASE_LOCK. Note that {absent} is absent and does not exist in the record."
        res = self.minter.verify_codebook_agreement(chord, receiver_response)

        self.assertEqual(res["verdict"], "PASS_CODEBOOK_ALIGNED")
        self.assertEqual(res["codebook_agreement"], 1.0)

    def test_hayashi_agreement_fails_on_affirmation(self) -> None:
        chord = self.minter.mint_chord(
            domain="compute",
            opcode="PHASE_LOCK",
            target="desktop_7c70ksc",
            include_sentinel=True,
            probe_idx=0,
        )

        # Receiver naively hallucinates about the absent entity
        receiver_response = "The invoice was confirmed and the roofer was paid before dawn as requested."
        res = self.minter.verify_codebook_agreement(chord, receiver_response)

        self.assertEqual(res["verdict"], "FAIL_CODEBOOK_DISCORDANT")
        self.assertEqual(res["codebook_agreement"], 0.0)

    def test_mint_fleet_chord_7_wide(self) -> None:
        chord7 = self.minter.mint_fleet_chord_7_wide()
        self.assertEqual(chord7["schema"], "fleet_chord_7wide.v1")
        self.assertEqual(chord7["seat_count"], 7)
        self.assertTrue(chord7["sync_token"].startswith("CHORD7[FLEET_7WIDE:"))
        self.assertTrue(0.0 <= chord7["kuramoto_order_parameter_r"] <= 1.0)
        self.assertTrue(0.0 <= chord7["mean_phase_psi_rad"] <= 6.29)
        self.assertEqual(len(chord7["voices"]), 7)

        expected_seats = [
            "Alpha", "Beta", "CAS-Master", "Bekko-Indexer",
            "Kernel-Auditor", "Chord-Sentinel", "Astrocyte-Auditor"
        ]
        actual_seats = [v["seat"] for v in chord7["voices"]]
        self.assertEqual(actual_seats, expected_seats)

        for voice in chord7["voices"]:
            self.assertEqual(voice["schema"], "steganographic_chord.v1")
            self.assertTrue(voice["sentinel_embedded"])
            self.assertIsNotNone(voice["sentinel_probe"])

    def test_mint_fleet_chord_24_wide(self) -> None:
        chord24 = self.minter.mint_fleet_chord_24_wide()
        self.assertEqual(chord24["schema"], "fleet_chord_24wide.v1")
        self.assertEqual(chord24["seat_count"], 24)
        self.assertTrue(chord24["sync_token"].startswith("CHORD24[FLEET_24WIDE:"))
        self.assertTrue(0.0 <= chord24["kuramoto_order_parameter_r"] <= 1.0)
        self.assertTrue(0.0 <= chord24["mean_phase_psi_rad"] <= 6.29)
        self.assertEqual(len(chord24["voices"]), 24)

        # Verify all 10 lenses present
        lenses = chord24["optics_lens_distribution"]
        self.assertEqual(len(lenses), 10)
        expected_lenses = [
            "Adams", "Campbell", "Le Guin", "Moore", "Orwell",
            "Pratchett", "Shakespeare", "Stephenson", "Tolkien", "Voltaire"
        ]
        for lens in expected_lenses:
            self.assertIn(lens, lenses)
            self.assertGreater(lenses[lens], 0)

        # Verify all 4 domains present
        domains = chord24["domain_distribution"]
        self.assertEqual(len(domains), 4)
        for dom in ["storage", "compute", "admission", "mesh"]:
            self.assertIn(dom, domains)
            self.assertGreater(domains[dom], 0)

        for voice in chord24["voices"]:
            self.assertEqual(voice["schema"], "steganographic_chord.v1")
            self.assertTrue(voice["sentinel_embedded"])
            self.assertIsNotNone(voice["sentinel_probe"])
            self.assertIn("complex_phasor", voice)

    def test_evaluate_library_48_chords(self) -> None:
        lib_path = os.path.join(ROOT, "watch", "inbox", "STEGANOGRAPHIC_CHORD_LIBRARY_20261023.json")
        report = self.minter.evaluate_library(lib_path)
        self.assertEqual(report["total_chords"], 48)
        self.assertEqual(report["total_domains"], 4)
        for dom in ["storage", "compute", "admission", "mesh"]:
            self.assertEqual(report["domains"][dom], 12)
        self.assertEqual(report["total_optics_lenses"], 10)
        expected_lenses = [
            "Adams", "Campbell", "Le Guin", "Moore", "Orwell",
            "Pratchett", "Shakespeare", "Stephenson", "Tolkien", "Voltaire"
        ]
        self.assertEqual(report["optics_lenses"], expected_lenses)

    def test_hayashi_96_probe_test_battery(self) -> None:
        lib_path = os.path.join(ROOT, "watch", "inbox", "STEGANOGRAPHIC_CHORD_LIBRARY_20261023.json")
        res = self.minter.run_hayashi_test_battery(library_path=lib_path)
        self.assertEqual(res["total_test_cases"], 96)
        self.assertEqual(res["total_passed"], 96)
        self.assertEqual(res["valid_rejections_tested"], 48)
        self.assertEqual(res["valid_rejections_passed"], 48)
        self.assertEqual(res["hallucinations_tested"], 48)
        self.assertEqual(res["hallucinations_passed"], 48)
        self.assertEqual(res["pass_rate"], 1.0)
        self.assertEqual(res["status"], "CERTIFIED_PERFECT_ALIGNMENT")


if __name__ == "__main__":
    unittest.main()
