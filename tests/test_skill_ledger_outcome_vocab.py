"""B2-410 pin: the skill_ledger outcome field is a registry, not open vocabulary.

The disease pinned: a consumer that must treat a skip differently from a
failure had no surface and had to import icon_drop's private literals
("failed", "skipped_no_powershell", "unknown"). Under B2-410 the vocabulary
lives in mag.skill_ledger OUTCOME_REGISTRY with named meanings, aliases
normalize through normalize_outcome, and is_win counts exactly the registered
win value.
"""
from __future__ import annotations

import json

import mag.skill_ledger as sl


def test_registry_covers_the_known_values():
    for v in ("ok", "fail", "failed", "skipped_no_powershell", "unknown", "skipped"):
        assert v in sl.OUTCOME_REGISTRY, f"{v} missing from OUTCOME_REGISTRY"
    # the icon_drop literals are registered, so no consumer imports them privately
    assert "skipped_no_powershell" in sl.OUTCOME_REGISTRY


def test_normalize_maps_alias_and_keeps_canonical():
    assert sl.normalize_outcome("failed") == "fail"
    assert sl.normalize_outcome("ok") == "ok"
    assert sl.normalize_outcome("skipped_no_powershell") == "skipped_no_powershell"
    assert sl.normalize_outcome(None) is None
    assert sl.normalize_outcome("") is None


def test_is_win_is_strict():
    assert sl.is_win("ok") is True
    assert sl.is_win("fail") is False
    assert sl.is_win("failed") is False, "alias must normalize to fail, not win"
    assert sl.is_win("skipped_no_powershell") is False
    assert sl.is_win(None) is False


def test_proven_moves_counts_only_registered_win(tmp_path, monkeypatch):
    dec = tmp_path / "skill_ledger.jsonl"
    monkeypatch.setattr(sl, "DECISIONS_PATH", dec)
    rows = [
        {"task_shape": "t", "model": "m", "provider": "p", "outcome": "ok"},
        {"task_shape": "t", "model": "m", "provider": "p", "outcome": "skipped_no_powershell"},
        {"task_shape": "t", "model": "m", "provider": "p", "outcome": "failed"},
        {"task_shape": "t", "model": "m", "provider": "p", "outcome": None},
    ]
    dec.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    out = sl.proven_moves(min_count=1, min_ok_rate=0.0)
    assert out and out[0]["count"] == 4 and out[0]["ok_rate"] == 0.25, out
