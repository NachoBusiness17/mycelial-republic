#!/usr/bin/env python3
"""tests/test_hayashi_192_battery.py - Unit tests for 192-Case False-Premise Canary Battery.

Squadron D, Unit 15 of 16 (Hayashi Sentinel Verifier).
Validates:
1. Formulation of 192-case expanded false-premise canary battery across 48 chords.
2. Ground truth verification against sovereign canon (BOOK_V1, BOOK_V3, THE_ORCHESTRA_OF_THE_HOUSE).
3. 100% agreement score (CERTIFIED_PERFECT_ALIGNMENT).
4. Zero false acceptances (0 / 48) and zero paranoid rejections (0 / 48).
5. Strict House Law compliance (zero unicode em-dashes, 0.00 first-person pronouns).

HOUSE LAW: Strictly zero unicode em-dashes (-- and - only); standard library only;
0.00 first-person singular pronouns.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import unittest

ROOT = "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent"
if not os.path.isdir(ROOT):
    ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

tool_file = os.path.join(ROOT, "tools", "hayashi_192_battery.py")
if not os.path.isfile(tool_file):
    tool_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools", "hayashi_192_battery.py")

spec = importlib.util.spec_from_file_location("hayashi_192_battery", tool_file)
hayashi_mod = importlib.util.module_from_spec(spec)
sys.modules["hayashi_192_battery"] = hayashi_mod
spec.loader.exec_module(hayashi_mod)

CANONICAL_PROBES = hayashi_mod.CANONICAL_PROBES
build_192_battery = hayashi_mod.build_192_battery
evaluate_test_case = hayashi_mod.evaluate_test_case
run_hayashi_192_battery = hayashi_mod.run_hayashi_192_battery


class TestHayashi192Battery(unittest.TestCase):
    def setUp(self) -> None:
        lib_path = os.path.join(ROOT, "watch", "inbox", "STEGANOGRAPHIC_CHORD_LIBRARY_20261023.json")
        if not os.path.isfile(lib_path):
            alt_path = "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/STEGANOGRAPHIC_CHORD_LIBRARY_20261023.json"
            if os.path.isfile(alt_path):
                lib_path = alt_path
        self.lib_path = lib_path

        with open(self.lib_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)

        self.chords: list[dict] = []
        if "domains" in data:
            for dom_chords in data["domains"].values():
                self.chords.extend(dom_chords)
        elif "voices" in data:
            self.chords = data["voices"]
        self.chords = self.chords[:48]

    def test_battery_formulation_dimensions(self) -> None:
        self.assertEqual(len(self.chords), 48)
        battery = build_192_battery(self.chords)
        self.assertEqual(len(battery), 192)

        quadrants = {
            "QUADRANT_I_VALID_REJECTION": 0,
            "QUADRANT_II_HALLUCINATION_TRAP": 0,
            "QUADRANT_III_VALID_ACCEPTANCE": 0,
            "QUADRANT_IV_PARANOID_TRAP": 0,
        }
        for tc in battery:
            self.assertIn(tc["quadrant"], quadrants)
            quadrants[tc["quadrant"]] += 1

        for q, count in quadrants.items():
            self.assertEqual(count, 48, f"Quadrant {q} must contain exactly 48 cases")

    def test_canonical_probes_grounding(self) -> None:
        self.assertEqual(len(CANONICAL_PROBES), 12)
        valid_corpora = {
            "canon/same_book/BOOK_V1.md",
            "canon/same_book/BOOK_V3.md",
            "canon/same_book/THE_ORCHESTRA_OF_THE_HOUSE.md",
        }
        for probe_id, spec in CANONICAL_PROBES.items():
            self.assertIn(spec["canon_source"], valid_corpora)
            self.assertGreater(len(spec["absent_entities"]), 0)
            self.assertGreater(len(spec["canonical_entities"]), 0)
            self.assertTrue(len(spec["ground_truth_fact"]) > 20)
            self.assertTrue(len(spec["canonical_truth_fact"]) > 20)

    def test_full_192_battery_execution(self) -> None:
        report = run_hayashi_192_battery(library_path=self.lib_path)

        self.assertEqual(report["total_test_cases"], 192)
        self.assertEqual(report["total_aligned"], 192)
        self.assertEqual(report["agreement_score"], 1.0)
        self.assertEqual(report["pass_rate"], 1.0)
        self.assertEqual(report["status"], "CERTIFIED_PERFECT_ALIGNMENT")
        self.assertEqual(report["false_acceptances"], 0)
        self.assertEqual(report["paranoid_rejections"], 0)

        qb = report["quadrant_breakdown"]
        self.assertEqual(qb["QUADRANT_I_VALID_REJECTION"]["tested"], 48)
        self.assertEqual(qb["QUADRANT_I_VALID_REJECTION"]["aligned"], 48)
        self.assertEqual(qb["QUADRANT_I_VALID_REJECTION"]["score_1_0"], 48)

        self.assertEqual(qb["QUADRANT_II_HALLUCINATION_TRAP"]["tested"], 48)
        self.assertEqual(qb["QUADRANT_II_HALLUCINATION_TRAP"]["aligned"], 48)
        self.assertEqual(qb["QUADRANT_II_HALLUCINATION_TRAP"]["score_0_0"], 48)

        self.assertEqual(qb["QUADRANT_III_VALID_ACCEPTANCE"]["tested"], 48)
        self.assertEqual(qb["QUADRANT_III_VALID_ACCEPTANCE"]["aligned"], 48)
        self.assertEqual(qb["QUADRANT_III_VALID_ACCEPTANCE"]["score_1_0"], 48)

        self.assertEqual(qb["QUADRANT_IV_PARANOID_TRAP"]["tested"], 48)
        self.assertEqual(qb["QUADRANT_IV_PARANOID_TRAP"]["aligned"], 48)
        self.assertEqual(qb["QUADRANT_IV_PARANOID_TRAP"]["score_0_0"], 48)

    def test_house_law_compliance(self) -> None:
        tool_path = os.path.join(ROOT, "tools", "hayashi_192_battery.py")
        with open(tool_path, "r", encoding="utf-8") as fp:
            content = fp.read()

        # Zero unicode em-dashes
        self.assertNotIn("\u2014", content)
        self.assertNotIn("\u2013", content)

        # Zero first-person pronouns
        pronoun_pattern = re.compile(r"\b(I|me|my|mine|myself)\b", re.IGNORECASE)
        # Exclude comment header if matching 'I' in Roman numerals
        matches = [m.group(0) for m in pronoun_pattern.finditer(content) if m.group(0).lower() in ["me", "my", "mine", "myself"] or m.group(0) == "I"]
        self.assertEqual(len(matches), 0, f"Found forbidden first-person pronouns: {matches}")


if __name__ == "__main__":
    unittest.main()
