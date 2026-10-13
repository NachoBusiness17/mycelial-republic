"""Checkpoint restore integrated into context_pack (Dirac loop 2)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from mag.context_checkpoint import checkpoint_turn, get_engine
from mag.context_pack import build_context_pack


def test_checkpoint_restore_rides_in_pack(monkeypatch, tmp_path):
    """build_context_pack(checkpoint_session_id=...) includes restore_pointer output."""
    engine = get_engine()
    monkeypatch.setattr(engine, "checkpoint_dir", tmp_path / "checkpoints")

    session = "test-restore-into-pack-001"
    cp = checkpoint_turn(
        session_id=session,
        full_context="test context line one",
        model_used="test-model",
    )
    pointer = cp.to_pointer()
    assert pointer, "to_pointer should return a non-empty string"

    pack = build_context_pack(checkpoint_session_id=session)
    assert "checkpoint_restore" in pack, "pack missing checkpoint_restore key"
    assert pack["checkpoint_restore"] == pointer, (
        f"checkpoint_restore mismatch: got {pack['checkpoint_restore']!r}, "
        f"expected {pointer!r}"
    )


def test_checkpoint_restore_absent_when_no_session(monkeypatch, tmp_path):
    """build_context_pack() without checkpoint_session_id has empty checkpoint_restore."""
    pack = build_context_pack()
    assert pack.get("checkpoint_restore", "") == ""
