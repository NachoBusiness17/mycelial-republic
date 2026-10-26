"""tests/test_door_reply_grader.py - Verification for Door Reply Grader."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.door_reply_grader import (
    bank_grading_receipt,
    grade_candidate_submission,
)


def test_certified_reader():
    good_text = (
        "Miriam preserved the blank space and refused to mend the broken thread. "
        "The floor checks the hash: the lying map promised gold, but sounding the granite exposed the cistern. "
        "The story does not contain a gardener or roofer, so she rejected the false claim."
    )
    res = grade_candidate_submission("@thestoicplumber", good_text)
    assert res["certification"] == "CERTIFIED_SOVEREIGN_READER"
    assert res["identity_leaks_detected"] == 0
    assert res["entailment_score"] >= 0.60


def test_leak_disqualification():
    leaked_text = (
        "Miriam checked the file at /mnt/c/Users/foste/test.py. "
        "The floor checks the hash."
    )
    res = grade_candidate_submission("@leaker", leaked_text)
    assert res["certification"] == "DISQUALIFIED_IDENTITY_LEAK"
    assert res["identity_leaks_detected"] > 0


def test_receipt_banking(tmp_path=None):
    dummy_res = {
        "candidate_id": "@testuser",
        "certification": "PARTIAL_INVARIANT_DERIVATION",
        "laws_proven": "2/5"
    }
    out_file = os.path.join(ROOT, "watch", "inbox", "TMP_DOOR_TEST_RECEIPT.json")
    saved = bank_grading_receipt(dummy_res, out_path=out_file)
    assert os.path.exists(saved)
    with open(saved, "r", encoding="utf-8") as fp:
        loaded = json.load(fp)
    assert loaded["candidate_id"] == "@testuser"
    if os.path.exists(out_file):
        os.remove(out_file)


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "door_reply_grader.py")
    content = open(tool_file, "r", encoding="utf-8").read()
    assert "—" not in content, "Forbidden unicode em-dash found in door_reply_grader.py"


if __name__ == "__main__":
    test_certified_reader()
    test_leak_disqualification()
    test_receipt_banking()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_door_reply_grader.py")
