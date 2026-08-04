"""Sprint 0.1 unit tests — schema capture guards + annotate heuristics."""

from __future__ import annotations

import json
from pathlib import Path

from mycelial_republic.data.annotate import estimate_signal, heuristic_tags
from mycelial_republic.data.schema import TrainingExample
from mycelial_republic.data.validate import run_validate


def test_capture_fields_rejected():
    ex = TrainingExample(
        id="1",
        source="manual",
        text="x" * 40,
        meta={"token_balance": 99},
    )
    errs = ex.validate()
    assert any("capture vector" in e for e in errs)


def test_heuristic_chord():
    tags = heuristic_tags("Please Strike the chord on this plan.")
    assert "chord" in tags


def test_heuristic_refusal():
    tags = heuristic_tags("I do not consent to that framing.")
    assert "refusal" in tags


def test_sample_jsonl_validates():
    root = Path(__file__).resolve().parents[1]
    sample = root / "data" / "annotated" / "examples" / "sample_train.jsonl"
    assert sample.is_file()
    code = run_validate(str(sample), min_examples=3)
    assert code == 0


def test_estimate_signal_high_for_chord():
    assert estimate_signal("short", ["chord"]) == "high"
