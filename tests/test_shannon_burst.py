"""tests/test_shannon_burst.py - Verification for Shannon Token Burst Generator."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.shannon_burst import (
    compute_shannon_entropy,
    generate_shannon_burst,
)


def test_entropy_calculation():
    # Empty string has 0 entropy
    assert compute_shannon_entropy("") == 0.0

    # Low entropy string (all same chars)
    low_ent = compute_shannon_entropy("AAAAAAAAAA")
    assert low_ent == 0.0

    # High entropy string (diverse character set)
    high_ent = compute_shannon_entropy("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()")
    assert high_ent > 4.5


def test_shannon_burst_structure():
    burst = generate_shannon_burst(repo_root=Path(ROOT))
    assert burst["schema"] == "shannon_burst.v1"
    assert burst["char_count"] > 100
    assert burst["entropy_bits_per_char"] > 3.5
    assert "Constraint(1p_sg_voice, 0.00)" in burst["shannon_payload"]
    assert "Governor(ultrasensitive_step" in burst["shannon_payload"]


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "shannon_burst.py")
    test_file = os.path.join(ROOT, "tests", "test_shannon_burst.py")
    for fpath in [tool_file, test_file]:
        content = open(fpath, "r", encoding="utf-8").read()
        assert "\u2014" not in content, f"Forbidden unicode em-dash found in {fpath}"


if __name__ == "__main__":
    test_entropy_calculation()
    test_shannon_burst_structure()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_shannon_burst.py")
