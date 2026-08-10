"""Test the elevate module: right-sized ask shaping + capture."""
from __future__ import annotations

from mag.elevate import capture, shape_ask, should_elevate


def test_should_elevate_on_high_stakes():
    assert should_elevate("OPSEC-review this packet before sending to partner") is True
    assert should_elevate("append a log line") is False


def test_shape_ask_has_frozen_prefix_and_contract():
    a = shape_ask("Review the embassy packet for gaps")
    assert a["frozen_prefix_chars"] > 0
    assert "OUTPUT CONTRACT" in a["full_prompt"]
    assert a["estimated_tokens"] > 0
    # The ask is SMALL relative to the prefix (the point of the deliberate-ask).
    assert a["ask_chars"] < a["frozen_prefix_chars"] or a["ask_chars"] < 400


def test_shape_ask_is_deterministic():
    a1 = shape_ask("Review the embassy packet")
    a2 = shape_ask("Review the embassy packet")
    assert a1["ask"] == a2["ask"]
    assert a1["estimated_tokens"] == a2["estimated_tokens"]


def test_capture_folds_to_case_law():
    a = shape_ask("Review the embassy packet")
    rec = capture(a, "shaped")
    # pro_library is the primary surface; must not raise.
    assert "pro_library" in rec
