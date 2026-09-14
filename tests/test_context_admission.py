"""Deterministic tests for the context admission rib and durable evidence."""
from __future__ import annotations

import json

from mag.context_admission import assess, write_receipt
from mag.context_checkpoint import ContextCheckpoint
from mag.context_compression import CompressionResult, load_compressed


def test_admission_bands_and_budget():
    green = assess(estimated_tokens=10_000, context_window=100_000)
    red = assess(estimated_tokens=90_000, context_window=100_000)
    black = assess(estimated_tokens=101_000, context_window=100_000)
    assert green["band"] == "green" and green["allowed"] is True
    assert red["band"] == "red" and red["allowed"] is False
    assert black["band"] == "black" and black["allowed"] is False


def test_pressure_receipt_has_measurements_not_prompt(tmp_path):
    path = write_receipt(tmp_path, {"reason": "test", "estimated_tokens": 99})
    row = json.loads((tmp_path / "memory" / "runs" / "context_admission" / "receipts.jsonl").read_text().strip())
    assert path.endswith("receipts.jsonl")
    assert row["schema"] == "context_admission.v1"
    assert row["estimated_tokens"] == 99
    assert "prompt" not in row


def test_checkpoint_round_trips_state_snapshot():
    cp = ContextCheckpoint("s", 1, "summary", "hash", "model", 0.0, "genesis",
                           state_snapshot={"phase": "working"})
    assert cp.to_dict()["state_snapshot"] == {"phase": "working"}


def test_compressed_artifact_is_reloadable(tmp_path, monkeypatch):
    import mag.context_compression as cc

    log = tmp_path / "compression_log.jsonl"
    monkeypatch.setattr(cc, "COMPRESSION_LOG", log)
    result = CompressionResult("demo", "original", "compressed", 10, 3, .3, 70,
                               "algorithmic", verified=True)
    cc._save_result(result)
    assert load_compressed("demo") == "compressed"
