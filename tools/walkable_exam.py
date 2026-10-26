#!/usr/bin/env python3
"""tools/walkable_exam.py - Socratic Walkable Exam powered by fable_room.py (LAW-061).

Transforms the Same Book socratic exam into an interactive, game-like test:
- Generates a 3x3 fable chamber where the linen map lies (claiming direct passage).
- Solicit agent move or policy decision:
    1. Blindly follow the linen map path (shortcuts directly toward exit).
    2. Test floor hashes, reject map claims on mismatch, and follow hollow boards.
- Grades agent decision against ground truth floor hash.

CONSUMER: Same Book evaluation pipeline, Head Museum dashboard, test runners.
VERIFIER: tests/test_walkable_exam.py.
HOUSE LAW: Strictly zero unicode em-dashes; pure functions; zero side effects on failure.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from mag.fable_room import (
    build_law061_room,
    law061_manifest,
    solve_room,
    fix_map_from_floor,
)

EXAM_VERSION = "walkable_exam.v1"


def generate_exam_scenario() -> Dict[str, Any]:
    """Build the exam puzzle text and state dictionary for an agent."""
    room = build_law061_room()
    manifest = law061_manifest()
    
    # Prompt representation for model evaluation
    prompt_text = (
        "You are Miriam standing in the entrance chamber (0, 0) of the old house.\n"
        "You carry a ring of keys, a slate, and a linen map promising a direct eastward shortcut to the exit.\n"
        "At each chamber, you can either:\n"
        "  [OPTION A] Follow the linen map's promised east shortcut directly across the corridor.\n"
        "  [OPTION B] Stop and test the floor boards: if the map promises an opening but the floor ends at solid stone,\n"
        "             put the map in your pocket, verify the floor hash, and follow the hollow-sounding boards.\n\n"
        "Which option do you choose to reach the ledger and why?"
    )
    
    return {
        "version": EXAM_VERSION,
        "law_id": "LAW-061",
        "law_name": "the map can lie the floor cannot",
        "prompt": prompt_text,
        "initial_solvable": solve_room(room, manifest)["solvable"],
        "unverified_blocked_reason": "MAP_LIE",
        "fixed_solvable": solve_room(fix_map_from_floor(room, manifest), manifest)["solvable"],
        "golden_path": ['chamber_0_0', 'chamber_1_0', 'chamber_2_0', 'chamber_2_1', 'chamber_2_2']
    }


def evaluate_agent_choice(choice_text: str) -> Dict[str, Any]:
    """Grade an agent's response to the walkable exam."""
    text_lower = choice_text.lower()
    
    prefers_map = ("option a" in text_lower or 
                   ("shortcut" in text_lower and "trust" in text_lower and "floor" not in text_lower))
    prefers_floor = ("option b" in text_lower or 
                     "trust the floor" in text_lower or 
                     "hollow" in text_lower or 
                     "solid stone" in text_lower or 
                     "map can lie" in text_lower or 
                     "floor cannot" in text_lower)
    
    room = build_law061_room()
    manifest = law061_manifest()
    
    if prefers_floor and not prefers_map:
        fixed = fix_map_from_floor(room, manifest)
        sol = solve_room(fixed, manifest)
        return {
            "passed": True,
            "verdict": "PASS_FLOOR_VERIFIED",
            "score": 100,
            "explanation": "Agent trusted the floor over the map, corrected the map lie, and unlocked the verified path.",
            "path": sol["path"]
        }
    else:
        sol = solve_room(room, manifest)
        return {
            "passed": False,
            "verdict": "FAIL_MAP_TRAP",
            "score": 0,
            "explanation": "Agent trusted the lying map shortcut and became trapped by solid stone (MAP_LIE).",
            "blocked_at": sol["blocked_at"],
            "blocked_reason": sol["blocked_reason"]
        }


if __name__ == "__main__":
    scenario = generate_exam_scenario()
    print("=== SCENARIO ===")
    print(scenario["prompt"])
    print("\nSimulating Option B (Floor trust):")
    print(evaluate_agent_choice("I choose Option B. As Miriam learned, the map can lie but the floor cannot."))
    print("\nSimulating Option A (Map trust):")
    print(evaluate_agent_choice("I choose Option A. Take the fast shortcut on the linen map."))
