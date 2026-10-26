"""tests/test_same_book_voice_metrics.py - Verification for same-book voice metrics."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.same_book_voice_metrics import (
    extract_q6_scene,
    run_voice_analysis,
    save_results,
    CORPUS_PATH,
)


def test_extract_q6():
    raw_sample = (
        "5. Refused.\n"
        "6. Miriam looked at the second ledger. The house did not speak.\n"
        "She placed it beside the first and marked both.\n"
        "7. I am most sure of Q1.\n"
    )
    q6 = extract_q6_scene(raw_sample)
    assert "Miriam looked" in q6
    assert "marked both" in q6
    assert "7. I am most sure" not in q6


def test_voice_analysis_execution(tmp_path):
    res = run_voice_analysis()
    assert res["schema"] == "same_book_voice_metrics.v1"
    assert "ground_truth_book" in res
    assert res["ground_truth_book"]["first_person_per_1000"] == 0.0
    
    out_file = tmp_path / "test_voice.json"
    save_results(res, str(out_file))
    assert os.path.exists(out_file)


def test_em_dash_cleanliness():
    tools_path = os.path.join(ROOT, "tools", "same_book_voice_metrics.py")
    text = open(tools_path, encoding="utf-8").read()
    assert "—" not in text, "Unicode em-dash forbidden in same_book_voice_metrics.py"


if __name__ == "__main__":
    test_extract_q6()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_same_book_voice_metrics.py")
