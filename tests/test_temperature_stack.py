"""Temperature stacks — adjustable timings, pointers, gap track."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_registry_loads_stacks():
    from mag.temperature_stack import registry

    reg = registry()
    snap = reg.snapshot()
    assert snap["schema"] == "mag_temperature_stacks.v1"
    assert "cold" in reg.stacks
    assert "scarce" in reg.stacks
    assert reg.loop_s("supervisor_check_s", 5) >= 2


def test_resolve_improve_and_code():
    from mag.temperature_stack import stack_for_goal, timeout_for_goal

    imp = stack_for_goal("[improve] scout harness", tag="improve-a")
    assert imp.id == "improve"
    assert timeout_for_goal("[improve] x", tag="improve") == imp.timeout_s

    code = stack_for_goal("implement dual-progress fix")
    assert code.id in ("warm", "hot")  # implement → warm keywords


def test_timeout_orchestrator_uses_stacks():
    from mag.orchestrator import timeout_for_goal as orch_timeout
    from mag.temperature_stack import stack_for_goal

    t = orch_timeout("[improve] playbook")
    assert t == stack_for_goal("[improve] playbook").timeout_s
    assert orch_timeout("x", timeout=42) == 42


def test_size_boost_timeout():
    from mag.temperature_stack import TemperatureStack

    st = TemperatureStack(id="hot", timeout_s=100)
    assert st.timing.scaled_timeout(size_hint=0) == 100
    assert st.timing.scaled_timeout(size_hint=40000) > 100


def test_pointer_knot_files():
    from mag.temperature_stack import file_pointer_knot

    r = file_pointer_knot(
        "https://github.com/openclaw/openclaw",
        kind="github",
        summary="computer-use research",
        tags=["openclaw"],
    )
    assert r.get("ok") is True
    assert r["knot"]["kind"] == "github"
    assert r["knot"]["leaf_hash"]


def test_track_loop_gap_dedupe(tmp_path, monkeypatch):
    """B2-79: the gap log must land in tmp_path, never the production log.

    Cause: the pre-fix test called track_loop_gap(force=True) with the default
    GAPS_LOG, appending test_gap_unique_xyz rows to memory/training/loop_gaps.jsonl
    (17 rows on bytes at fix time 2026-09-26). Receipt:
    watch/inbox/burn_wave_20260926/B2_79_pollution_fix_20260926.md

    B2-86 (2026-09-26): the same calls also fed track_loop_gap's side sinks,
    the improve candidate append (memory/improve/candidates.jsonl, id
    gap-c4f076b1e0205c27 still on bytes) and the training-event emit
    (memory/training/events.jsonl, 23 test rows still on bytes), so the test
    now isolates those sinks with the B2-80 helper and pins the production
    candidate and event files byte-still across both calls.
    """
    import json

    from mag.improve import ROOT as IMPROVE_ROOT
    from mag.temperature_stack import GAPS_LOG, track_loop_gap
    from mag.training_events import EVENTS_PATH

    prod_before = GAPS_LOG.stat().st_size if GAPS_LOG.is_file() else 0
    cand = IMPROVE_ROOT / "memory" / "improve" / "candidates.jsonl"
    cand_before = cand.stat().st_size if cand.is_file() else 0
    ev_before = EVENTS_PATH.stat().st_size if EVENTS_PATH.is_file() else 0

    log = tmp_path / "loop_gaps.jsonl"
    monkeypatch.setenv("MAG_GAPS_LOG", str(log))
    _isolate_gap_side_sinks(monkeypatch)

    a = track_loop_gap("test_gap_unique_xyz", detail="unit", where="tests", force=True)
    assert a.get("ok") is True
    b = track_loop_gap("test_gap_unique_xyz", detail="unit", where="tests", force=False)
    assert b.get("skipped") is True

    rows = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 1
    assert rows[0]["name"] == "test_gap_unique_xyz"

    prod_after = GAPS_LOG.stat().st_size if GAPS_LOG.is_file() else 0
    assert prod_after == prod_before
    assert cand.stat().st_size == cand_before, (
        "test appended to memory/improve/candidates.jsonl (B2-86 pollution class)"
    )
    assert EVENTS_PATH.stat().st_size == ev_before, (
        "test appended to memory/training/events.jsonl (B2-86 pollution class)"
    )


def _isolate_gap_side_sinks(monkeypatch):
    """Keep track_loop_gap's non-log side sinks inert (B2-80 test hygiene).

    The gap log is isolated via MAG_GAPS_LOG; emit/append_candidates/
    file_pointer_knot would otherwise write real repo files (the B2-86
    candidate-pollution class), so tests patch them instead of feeding them.
    """
    import mag.improve as improve_mod
    import mag.temperature_stack as ts_mod
    import mag.training_events as te_mod

    monkeypatch.setattr(te_mod, "emit", lambda *a, **k: {"ok": True})
    monkeypatch.setattr(improve_mod, "append_candidates", lambda *a, **k: 0)
    monkeypatch.setattr(ts_mod, "file_pointer_knot", lambda *a, **k: {"knot": {"knot_id": "tmp"}})


def test_track_loop_gap_lifecycle_reason_carry(tmp_path, monkeypatch):
    """B2-80: lifecycle rows carry the should verdict, reason and probe inputs.

    Cause: track_lifecycle_into_improve dropped everything build_lifecycle
    knew, the _policy_should verdict (mag/lifecycle.py:445) plus its
    queue_depth/fleet_running/operator_active inputs, so drainer gap vs waste
    rows (17 vs 87 at the B2-20 census, 18 vs 88 at fix time) and the
    sub-hour verdict flips were unauditable from the row alone. Receipt:
    watch/inbox/burn_wave_20260926/B2_80_reason_carry_20260926.md
    """
    import json

    from mag.temperature_stack import GAPS_LOG, track_loop_gap

    prod_before = GAPS_LOG.stat().st_size if GAPS_LOG.is_file() else 0

    log = tmp_path / "loop_gaps.jsonl"
    monkeypatch.setenv("MAG_GAPS_LOG", str(log))
    _isolate_gap_side_sinks(monkeypatch)

    track_loop_gap(
        "lifecycle_gap:drainer",
        detail="should be on but actual off",
        where="GET /api/v1/lifecycle",
        kind="lifecycle_gap",
        force=True,
        lifecycle={
            "should": "on",
            "reason": "queue_depth=3 fleet=1 -- drain allowed",
            "signals": {"queue_depth": 3, "fleet_running": 1, "operator_active": False},
        },
    )
    rows = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 1
    assert rows[0]["schema"] == "mag_loop_gap.v1"
    assert rows[0]["should"] == "on"
    assert rows[0]["should_reason"] == "queue_depth=3 fleet=1 -- drain allowed"
    assert rows[0]["signals"]["queue_depth"] == 3
    assert rows[0]["signals"]["operator_active"] is False

    # Non-lifecycle rows stay variable-field: no empty carry keys
    track_loop_gap("plain_gap_b2_80", detail="d", where="w", force=True)
    rows = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(rows) == 2
    assert "should" not in rows[1]
    assert "should_reason" not in rows[1]
    assert "signals" not in rows[1]

    prod_after = GAPS_LOG.stat().st_size if GAPS_LOG.is_file() else 0
    assert prod_after == prod_before


def test_track_lifecycle_into_improve_carries_policy_inputs(tmp_path, monkeypatch):
    """B2-80: the lifecycle caller feeds verdict + reason + signals per row.

    Falsifier pre-fix: a build_lifecycle returning a drainer gap and an
    improve waste landed rows whose only verdict context was the constant
    detail string, so the flip could not be attributed to its probe inputs.
    """
    import json
    import sys
    import types

    import mag.lifecycle as lifecycle_mod
    import mag.temperature_stack as ts_mod
    from mag.temperature_stack import track_lifecycle_into_improve

    log = tmp_path / "loop_gaps.jsonl"
    monkeypatch.setenv("MAG_GAPS_LOG", str(log))
    _isolate_gap_side_sinks(monkeypatch)
    monkeypatch.setattr(ts_mod, "STATE_PATH", tmp_path / "state.json")

    fake = {
        "ok": True,
        "posture": "active",
        "signals": {
            "queue_depth": 2,
            "fleet_running": 1,
            "operator_active": False,
            "drainer_allowed": True,
            "browser_enabled": False,
        },
        "pieces": [
            {"id": "drainer", "should": "on", "reason": "queue_depth=2 fleet=1 -- drain allowed"},
            {"id": "improve", "should": "off", "reason": "prefer explicit improve jobs only"},
        ],
        "gaps": ["drainer"],
        "waste": ["improve"],
    }
    monkeypatch.setattr(lifecycle_mod, "build_lifecycle", lambda: fake)

    be = types.ModuleType("mag.browser_env")
    be.status = lambda: {"ready": True, "enabled": True}
    monkeypatch.setitem(sys.modules, "mag.browser_env", be)

    res = track_lifecycle_into_improve()
    assert res["ok"] is True
    assert res["n"] == 2

    rows = [json.loads(x) for x in log.read_text(encoding="utf-8").splitlines() if x.strip()]
    by_name = {r["name"]: r for r in rows}
    gap_row = by_name["lifecycle_gap:drainer"]
    assert gap_row["should"] == "on"
    assert gap_row["should_reason"] == "queue_depth=2 fleet=1 -- drain allowed"
    assert gap_row["signals"]["queue_depth"] == 2
    assert gap_row["signals"]["drainer_allowed"] is True
    waste_row = by_name["lifecycle_waste:improve"]
    assert waste_row["should"] == "off"
    assert "improve jobs" in waste_row["should_reason"]
    assert waste_row["signals"]["operator_active"] is False


def test_track_loop_gap_names_writer_identity(tmp_path, monkeypatch):
    """B2-394 pin (2026-09-26): every future gap row carries its observing
    process identity in detail (pid, exe, host, proxy env), because the 89
    lifecycle_gap:ollama rows were written by an unreconstructable process
    (B2-81). Falsifier: a new lifecycle_gap row whose detail cannot name the
    writing process."""
    import json as _json
    import os as _os

    from mag.temperature_stack import GAPS_LOG, track_loop_gap
    from mag.training_events import EVENTS_PATH

    log = tmp_path / "loop_gaps.jsonl"
    monkeypatch.setenv("MAG_GAPS_LOG", str(log))
    _isolate_gap_side_sinks(monkeypatch)
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:9999")

    prod_before = GAPS_LOG.stat().st_size if GAPS_LOG.is_file() else 0
    out = track_loop_gap(
        "test_gap_writer_identity", detail="unit", where="tests", force=True
    )
    assert out.get("ok") is True
    prod_after = GAPS_LOG.stat().st_size if GAPS_LOG.is_file() else 0
    assert prod_after == prod_before

    rows = [_json.loads(line) for line in log.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) == 1
    detail = rows[0]["detail"]
    assert "[writer pid=" in detail
    assert "exe=" in detail and "host=" in detail
    assert "HTTPS_PROXY=http://127.0.0.1:9999" in detail
    assert str(_os.getpid()) in detail
