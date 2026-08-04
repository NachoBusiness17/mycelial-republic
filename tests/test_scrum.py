"""Scrum board store + gates."""
from __future__ import annotations

from mycelial_republic.scrum import store


def test_load_backlog_has_tickets():
    data = store.load_backlog()
    assert "tickets" in data
    assert any(t.get("id") == "W0.0" for t in data["tickets"])


def test_render_board():
    md = store.render_board()
    assert "Sprint board" in md
    assert "W0.0" in md


def test_gate_raw_empty_blocks_train():
    t = {"id": "W0.6", "blocks_r0": True, "status": "ready", "role": "AGT_TRAIN"}
    if store.raw_empty():
        ok, reason = store.gate_check(t)
        assert ok is False
        assert "W0.0" in reason
