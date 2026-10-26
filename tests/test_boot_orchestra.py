#!/usr/bin/env python3
"""Tests for tools/boot_orchestra.py."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from tools.boot_orchestra import (
    stage1_verify_ledger_and_seats,
    stage2_verify_static_retrieval,
    stage3_verify_kuramoto_timing,
    stage4_verify_ultrasensitive_gate,
    stage5_verify_topological_sandbox,
    stage6_verify_single_writer_chute,
    stage7_verify_epistemic_calibration,
    run_full_bootstrap,
)


def test_individual_stages():
    s1 = stage1_verify_ledger_and_seats()
    assert s1["passed"] is True
    assert s1["stage"] == 1

    s2 = stage2_verify_static_retrieval()
    assert s2["passed"] is True
    assert s2["stage"] == 2

    s3 = stage3_verify_kuramoto_timing()
    assert s3["passed"] is True
    assert s3["stage"] == 3

    s4 = stage4_verify_ultrasensitive_gate()
    assert s4["passed"] is True
    assert s4["stage"] == 4

    s5 = stage5_verify_topological_sandbox()
    assert s5["passed"] is True
    assert s5["stage"] == 5

    s6 = stage6_verify_single_writer_chute()
    assert s6["passed"] is True
    assert s6["stage"] == 6

    s7 = stage7_verify_epistemic_calibration()
    assert s7["passed"] is True
    assert s7["stage"] == 7


def test_full_bootstrap_attestation():
    att = run_full_bootstrap()
    assert att["schema"] == "sovereign_boot_attestation.v1"
    assert att["status"] == "SOVEREIGN_READY"
    assert att["all_passed"] is True
    assert att["stages_verified"] == 7
    assert att["stages_passed"] == 7


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "boot_orchestra.py")
    content = open(tool_file, "r", encoding="utf-8").read()
    assert "\u2014" not in content, "Forbidden unicode em-dash found in boot_orchestra.py"
    assert "\u2013" not in content, "Forbidden unicode en-dash found in boot_orchestra.py"


if __name__ == "__main__":
    test_individual_stages()
    test_full_bootstrap_attestation()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_boot_orchestra.py")
