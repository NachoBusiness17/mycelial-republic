"""tests for mag/skill_lifecycle — EPHEMERAL one-turn skill flag (adk-week steal).

FROZEN SPEC:
  gate            ADK_ENABLE_SKILL_LIFECYCLE read at CHECK time (ADK is_env_enabled
                  pattern): enabled iff value case-insensitively '1' or 'true'.
                  Default OFF: load() refuses and the registry is never mutated.
  load(id)        registers skill_<id> into tools.TOOL_MAP (the seat tool registry)
                  stamped with the current seat-turn; dispatchable during that turn.
  end_turn()      turn boundary: every skill loaded this turn AUTO-UNLOADS; the
                  name dispatches as unknown (exit 127) afterwards.
  sweep           load() first unloads skills from turns older than the current
                  one, so a seat that never calls end_turn() cannot accumulate.
  safety          never shadows or removes a static registry tool (tools.STATIC_TOOLS);
                  unload idempotent; every mutation returns a receipt.

Contract: pure stdlib at test time (yaml import guarded in the module itself).
Exercises the real tools.TOOL_MAP and restores it in a finally, so the shared
registry is never polluted for other tests.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402

from mag import skill_lifecycle as lc  # noqa: E402
import tools  # noqa: E402

GATE = "ADK_ENABLE_SKILL_LIFECYCLE"


@pytest.fixture(autouse=True)
def _clean_registry_and_gate(monkeypatch):
    """Gate off + empty overlay before and after every test (shared TOOL_MAP)."""
    monkeypatch.delenv(GATE, raising=False)
    tools.unload_ephemeral_all()
    lc.reset_state()
    baseline = set(tools.TOOL_MAP)
    yield
    tools.unload_ephemeral_all()
    lc.reset_state()
    assert set(tools.TOOL_MAP) == baseline, "test leaked registry entries"


def test_gate_default_off_and_registry_untouched():
    assert lc.is_enabled() is False
    res = lc.load("ponytail")
    assert res["ok"] is False
    assert res["reason"] == "gate_off"
    assert "skill_ponytail" not in tools.TOOL_MAP


@pytest.mark.parametrize(
    "val,want",
    [("1", True), ("true", True), ("TRUE", True), ("0", False), ("false", False), ("", False)],
)
def test_gate_values_follow_adk_is_env_enabled(monkeypatch, val, want):
    monkeypatch.setenv(GATE, val)
    assert lc.is_enabled() is want


def test_skill_auto_unloads_after_one_seat_turn(monkeypatch):
    monkeypatch.setenv(GATE, "1")
    baseline = set(tools.TOOL_MAP)
    res = lc.load("ponytail")
    assert res["ok"] is True
    assert res["loaded_turn"] == 0 and res["unloads_at_turn"] == 1
    name = res["tool"]
    assert name == "skill_ponytail"
    assert name in tools.TOOL_MAP
    out = tools.dispatch(name, {})
    assert out["ok"] is True and out["skill_id"] == "ponytail" and out["body_chars"] > 0
    # the turn boundary: auto-unload, and the name is dead afterwards
    et = lc.end_turn()
    assert name in et["unloaded"] and et["ok"] is True
    assert name not in tools.TOOL_MAP
    dead = tools.dispatch(name, {})
    assert dead["ok"] is False and dead["exit_code"] == 127
    assert set(tools.TOOL_MAP) == baseline


def test_stale_sweep_when_seat_misses_end_turn(monkeypatch):
    monkeypatch.setenv(GATE, "1")
    lc.load("ponytail")          # turn 0
    lc.begin_turn()              # turn 1, no end_turn ever called
    res = lc.load("caveman")
    assert res["ok"] is True
    assert res["swept_stale"] == ["skill_ponytail"]
    assert "skill_ponytail" not in tools.TOOL_MAP
    assert "skill_caveman" in tools.TOOL_MAP
    lc.end_turn()
    assert "skill_caveman" not in tools.TOOL_MAP


def test_static_tools_never_shadowed_or_removed(monkeypatch):
    monkeypatch.setenv(GATE, "1")
    conflict = lc.load("list_dir")  # not a skill id -> unknown_skill, registry untouched
    assert conflict["reason"] == "unknown_skill"
    reg = tools.register_ephemeral("run_shell", lambda **kw: {"ok": True})
    assert reg["ok"] is False and reg["reason"] == "name_conflict"
    assert "run_shell" in tools.TOOL_MAP  # the real static tool survived
    un = tools.unregister_ephemeral("run_shell")
    assert un["ok"] is False and un["reason"] == "not_ephemeral"
    assert tools.dispatch("list_dir", {"path": "."})["ok"] is True
    lc.end_turn()
    assert tools.STATIC_TOOLS <= set(tools.TOOL_MAP)


def test_unknown_skill_refused_with_available_list(monkeypatch):
    monkeypatch.setenv(GATE, "1")
    res = lc.load("no-such-skill")
    assert res["ok"] is False and res["reason"] == "unknown_skill"
    assert "ponytail" in res["available"] and "caveman" in res["available"]


def test_duplicate_ephemeral_registration_refused(monkeypatch):
    monkeypatch.setenv(GATE, "1")
    first = lc.load("ponytail")
    assert first["ok"] is True
    second = lc.load("ponytail")
    assert second["ok"] is False and second["reason"] == "already_registered"
    assert first["tool"] in tools.TOOL_MAP  # the original lease stands
    lc.end_turn()
    assert first["tool"] not in tools.TOOL_MAP


def test_unload_is_idempotent_and_receipt_bearing(monkeypatch):
    monkeypatch.setenv(GATE, "1")
    res = lc.load("ponytail")
    name = res["tool"]
    u1 = lc.unload(name)
    assert u1["ok"] is True and u1.get("unregistered") is True
    u2 = lc.unload(name)
    assert u2["ok"] is True and u2.get("already_gone") is True


def test_end_turn_receipt_reports_loaded_turn(monkeypatch):
    monkeypatch.setenv(GATE, "1")
    lc.begin_turn()
    res = lc.load("ponytail")
    et = lc.end_turn()
    assert et["receipts"] == [
        {"tool": res["tool"], "skill_id": "ponytail", "loaded_turn": 1}
    ]
    assert et["turn"] == 1 and et["damaged_static"] == []
