"""tests/test_ultrasensitive_gate.py - Verification for Ultrasensitive Step Gate."""
from __future__ import annotations

import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.ultrasensitive_gate import (
    evaluate_hill_curve,
    evaluate_ultrasensitive_gate,
)


def test_hill_curve_response():
    kd = 0.80
    n = 8.0

    # Below threshold: response should be suppressed near zero
    val_low = evaluate_hill_curve(0.50, kd=kd, n=n)
    assert val_low < 0.05

    # Exactly at threshold: response must equal 0.50
    val_mid = evaluate_hill_curve(kd, kd=kd, n=n)
    assert math.isclose(val_mid, 0.50, rel_tol=1e-5)

    # Above threshold: response snaps above midpoint
    val_high = evaluate_hill_curve(0.95, kd=kd, n=n)
    assert val_high > 0.75


def test_gate_decision_fol_refusal():
    # Signal is 0.99, but FOL logic check fails
    decision = evaluate_ultrasensitive_gate(
        signal_score=0.99,
        threshold_kd=0.80,
        fol_entailed=False,
    )
    assert decision.permitted is False
    assert decision.force == 0.0
    assert decision.verdict == "FOL_REFUSED"


def test_gate_decision_sub_threshold():
    # FOL is True, but continuous score (0.70) is below Kd (0.80)
    decision = evaluate_ultrasensitive_gate(
        signal_score=0.70,
        threshold_kd=0.80,
        fol_entailed=True,
    )
    assert decision.permitted is False
    assert decision.force == 0.0
    assert decision.verdict == "SUB_THRESHOLD_SUPPRESSED"


def test_gate_decision_step_permitted():
    # FOL is True, and score (0.85) is supra-threshold
    decision = evaluate_ultrasensitive_gate(
        signal_score=0.85,
        threshold_kd=0.80,
        fol_entailed=True,
    )
    assert decision.permitted is True
    assert decision.force == 1.0
    assert decision.verdict == "STEP_PERMITTED"


def test_zero_dithering_invariant():
    # Across a scan of 20 signal scores, force is ALWAYS exactly 0.0 or 1.0 (never fractional)
    for i in range(21):
        sig = i * 0.05
        dec = evaluate_ultrasensitive_gate(sig, threshold_kd=0.80, fol_entailed=True)
        assert dec.force in (0.0, 1.0), f"Fractional force {dec.force} violated zero-dithering law!"


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "ultrasensitive_gate.py")
    test_file = os.path.join(ROOT, "tests", "test_ultrasensitive_gate.py")
    for fpath in [tool_file, test_file]:
        content = open(fpath, "r", encoding="utf-8").read()
        assert "\u2014" not in content, f"Forbidden unicode em-dash found in {fpath}"


if __name__ == "__main__":
    test_hill_curve_response()
    test_gate_decision_fol_refusal()
    test_gate_decision_sub_threshold()
    test_gate_decision_step_permitted()
    test_zero_dithering_invariant()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_ultrasensitive_gate.py")
