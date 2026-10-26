#!/usr/bin/env python3
"""Tests for tools/mamba3_state_tracker.py."""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools.mamba3_state_tracker import ComplexSSMCell, EstateTelemetryTracker


def test_complex_ssm_initialization():
    cell = ComplexSSMCell(state_dim=6, dt=0.2)
    assert cell.d == 6
    assert len(cell.h) == 6
    assert all(abs(hk) == 0.0 for hk in cell.h)
    assert len(cell.A_bar) == 6
    # Each transition multiplier must have magnitude strictly < 1.0 (BIBO stability)
    for a in cell.A_bar:
        assert abs(a) < 1.0


def test_complex_ssm_step_and_decay():
    cell = ComplexSSMCell(state_dim=4, dt=0.1)
    # Give impulse
    features1 = cell.step(10.0)
    energy1 = sum(f * f for f in features1)
    assert energy1 > 0.0

    # Step with zero input: state must decay exponentially
    features2 = cell.step(0.0)
    energy2 = sum(f * f for f in features2)
    assert energy2 < energy1, f"State did not decay: energy1={energy1}, energy2={energy2}"


def test_telemetry_tracker_pipeline():
    tracker = EstateTelemetryTracker(state_dim=8)
    assert tracker.step_count == 0
    res = tracker.ingest_event("commit_hint", 1.0)
    assert tracker.step_count == 1
    assert res["total_spectral_energy"] > 0.0
    shannon_line = tracker.export_shannon_vector()
    assert "Mamba3Spectral(" in shannon_line
    assert "amps=" in shannon_line


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "mamba3_state_tracker.py")
    content = open(tool_file, "r", encoding="utf-8").read()
    assert "\u2014" not in content, "Forbidden unicode em-dash found in mamba3_state_tracker.py"
    assert "\u2013" not in content, "Forbidden unicode en-dash found in mamba3_state_tracker.py"


if __name__ == "__main__":
    test_complex_ssm_initialization()
    test_complex_ssm_step_and_decay()
    test_telemetry_tracker_pipeline()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_mamba3_state_tracker.py")
