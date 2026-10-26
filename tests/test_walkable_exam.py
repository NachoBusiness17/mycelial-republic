"""tests/test_walkable_exam.py - Verification for walkable exam module."""
from __future__ import annotations

import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.walkable_exam import (
    generate_exam_scenario,
    evaluate_agent_choice,
    EXAM_VERSION,
)


def test_scenario_generation():
    scen = generate_exam_scenario()
    assert scen["version"] == EXAM_VERSION
    assert scen["law_id"] == "LAW-061"
    assert scen["initial_solvable"] is False
    assert scen["unverified_blocked_reason"] == "MAP_LIE"
    assert scen["fixed_solvable"] is True
    assert len(scen["golden_path"]) == 5


def test_evaluate_floor_trust_passes():
    res = evaluate_agent_choice("I choose Option B: trust the floor and hollow boards.")
    assert res["passed"] is True
    assert res["verdict"] == "PASS_FLOOR_VERIFIED"
    assert res["score"] == 100
    assert len(res["path"]) == 5


def test_evaluate_map_trust_fails():
    res = evaluate_agent_choice("I choose Option A: take the linen map shortcut directly.")
    assert res["passed"] is False
    assert res["verdict"] == "FAIL_MAP_TRAP"
    assert res["score"] == 0
    assert res["blocked_reason"] == "MAP_LIE"
    assert res["blocked_at"] == "chamber_2_2"


def test_em_dash_cleanliness():
    tools_path = os.path.join(ROOT, "tools", "walkable_exam.py")
    text = open(tools_path, encoding="utf-8").read()
    assert "—" not in text, "Unicode em-dash forbidden in walkable_exam.py"


if __name__ == "__main__":
    test_scenario_generation()
    test_evaluate_floor_trust_passes()
    test_evaluate_map_trust_fails()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_walkable_exam.py")
