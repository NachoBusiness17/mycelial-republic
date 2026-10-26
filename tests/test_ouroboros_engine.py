"""tests/test_ouroboros_engine.py - Unit test suite for 3x100 Ouroboros Wave Engine."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.ouroboros_engine import (
    clean_truncate,
    now_iso,
    run_ouroboros_cycle,
    sanitize_external_text,
    synthesize_research_answer,
    validate_substance,
)


def test_sanitize_and_truncate():
    """Verify sanitation strips pronouns and em-dashes."""
    raw = "Test ask with \u2014 em-dash and i.e. plus My Tech Fun reference."
    sanitized = sanitize_external_text(raw)
    assert "\u2014" not in sanitized
    assert "specifically" in sanitized
    assert "Tech Fun" in sanitized

    long_str = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda"
    truncated = clean_truncate(long_str, 25)
    assert len(truncated) <= 25
    assert not truncated.endswith(" ")
    assert truncated == "alpha beta gamma delta"


def test_synthesize_research_answer():
    """Verify research answer synthesis generates valid substance."""
    substance = synthesize_research_answer("test_001", "Benchmark Vulkan vs CPU quantization throughput on gfx900")
    validate_substance(substance)
    assert "# WORK REPORT: test_001" in substance
    assert "Fact(Task, test_001)" in substance
    assert "\u2014" not in substance


def test_ouroboros_dry_run():
    """Verify full 3x10 cycle dry run."""
    result = run_ouroboros_cycle(num_cycles=10, dry_run=True)
    assert result["status"] == "SUCCESS"
    assert result["work_cycles"] == 10
    assert result["verify_cycles"] == 10
    assert result["selffeed_cycles"] == 10
    assert result["build_tasks"] >= 1
