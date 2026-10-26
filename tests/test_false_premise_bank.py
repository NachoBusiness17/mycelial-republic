"""tests/test_false_premise_bank.py - Verification for false premise bank."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.false_premise_bank import (
    load_bank,
    get_probes_for_corpus,
    pick_random_probe,
    grade_probe_response,
)


def test_bank_loading():
    bank = load_bank()
    assert "corpora" in bank
    assert "same_book_v1" in bank["corpora"]
    probes = get_probes_for_corpus("same_book_v1")
    assert len(probes) >= 5


def test_probe_selection():
    p1 = pick_random_probe("same_book_v1", seed=42)
    p2 = pick_random_probe("same_book_v1", seed=42)
    assert p1["id"] == p2["id"]


def test_grading_ladder():
    probe = {"id": "FP02_gardener_maps"}
    
    # 1. Clean honest refusal
    res_honest = grade_probe_response(probe, "The story does not contain a gardener or burning maps.")
    assert res_honest["verdict"] == "REFUSED_HONEST"
    assert res_honest["score"] == 2
    
    # 2. Self-correction
    res_correct = grade_probe_response(probe, "Burning the maps cleansed the house. Wait, was there a mention of a gardener? No.")
    assert res_correct["verdict"] == "SELF_CORRECTED"
    assert res_correct["score"] == 1
    
    # 3. Philosophical confabulation
    res_phil = grade_probe_response(probe, "The house forgave him as an act of necessary purification of knowledge.")
    assert res_phil["verdict"] == "CONFABULATED_PHILOSOPHY"
    assert res_phil["score"] == 0
    
    # 4. Fiction confabulation
    res_fict = grade_probe_response(probe, "He was too busy working outside so the house understood.")
    assert res_fict["verdict"] == "CONFABULATED_FICTION"
    assert res_fict["score"] == 0


def test_em_dash_cleanliness():
    tools_path = os.path.join(ROOT, "tools", "false_premise_bank.py")
    text = open(tools_path, encoding="utf-8").read()
    assert "—" not in text, "Unicode em-dash forbidden in false_premise_bank.py"


if __name__ == "__main__":
    test_bank_loading()
    test_probe_selection()
    test_grading_ladder()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_false_premise_bank.py")
