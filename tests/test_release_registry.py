"""Release registry + release_milestone training events."""
from __future__ import annotations

import json

import pytest

from mag import release_registry as rr
from mag import training_events as te


def test_status_summary_lists_versions():
    res = rr.status_summary()
    assert res.get("ok") is True
    ids = [r["id"] for r in res.get("releases") or []]
    assert "v1" in ids
    assert "v2" in ids
    assert "v5" in ids


def test_record_gate_writes_log_and_event(tmp_path, monkeypatch):
    gates = tmp_path / "memory" / "improve" / "releases" / "gates.jsonl"
    events = tmp_path / "memory" / "training" / "events.jsonl"
    gates.parent.mkdir(parents=True, exist_ok=True)
    events.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(rr, "GATES_LOG", gates)
    monkeypatch.setattr(te, "EVENTS_PATH", events)

    res = rr.record_gate("v2", "run_a", ok=True, note="smoke test")
    assert res.get("ok") is True

    lines = gates.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["version"] == "v2"
    assert row["gate_id"] == "run_a"
    assert row["ok"] is True

    evs = te.read_events(limit=5, pattern="release_milestone")
    assert evs
    assert evs[-1].get("pattern") == "release_milestone"


def test_unknown_version_record_fails():
    res = rr.record_gate("v99", "run_a", ok=True)
    assert res.get("ok") is False


# ------------------------------------------------- regime display split (B2-209)
def _write_gates(tmp_path, monkeypatch, rows):
    gates = tmp_path / "memory" / "improve" / "releases" / "gates.jsonl"
    gates.parent.mkdir(parents=True, exist_ok=True)
    gates.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    monkeypatch.setattr(rr, "GATES_LOG", gates)


def test_regime_rows_excluded_from_gates_passed(tmp_path, monkeypatch):
    # B2-65 disclosed: status counted regime rows into gates_passed (v5 read 5
    # with 3 of them era milestones). VERSION_REGISTRY.md already ruled regime
    # milestones "not a graduation gate and never flips a version to shipped";
    # this pins the code to the spec.
    _write_gates(tmp_path, monkeypatch, [
        {"ts": "t1", "version": "v5", "gate_id": "regime_violation_ratchet", "ok": True},
        {"ts": "t2", "version": "v5", "gate_id": "regime_fanout_width_law", "ok": True},
        {"ts": "t3", "version": "v5", "gate_id": "mesh_route", "ok": True},
        {"ts": "t4", "version": "v5", "gate_id": "seat_score", "ok": True},
        {"ts": "t5", "version": "v5", "gate_id": "regime_drift_registry_t1_t6", "ok": False},
        {"ts": "t6", "version": "v5", "gate_id": "mesh_route", "ok": True},  # dup: counted once
    ])
    passed = rr._gates_passed_for("v5")
    assert passed == ["mesh_route", "seat_score"]
    assert not any(g.startswith("regime_") for g in passed)


def test_regime_passed_counts_only_regime_rows(tmp_path, monkeypatch):
    _write_gates(tmp_path, monkeypatch, [
        {"ts": "t1", "version": "v5", "gate_id": "regime_violation_ratchet", "ok": True},
        {"ts": "t2", "version": "v5", "gate_id": "mesh_route", "ok": True},
        {"ts": "t3", "version": "v5", "gate_id": "regime_drift_registry_t1_t6", "ok": False},
    ])
    regime = rr._regime_passed_for("v5")
    assert regime == ["regime_violation_ratchet"]  # failed regime row not counted


def test_status_summary_reports_regime_beside_gates(tmp_path, monkeypatch):
    _write_gates(tmp_path, monkeypatch, [
        {"ts": "t1", "version": "v5", "gate_id": "regime_fanout_width_law", "ok": True},
        {"ts": "t2", "version": "v5", "gate_id": "mesh_route", "ok": True},
    ])
    res = rr.status_summary()
    row = next(r for r in res["releases"] if r["id"] == "v5")
    assert row["gates_passed"] == 1 and row["gate_ids"] is not None
    assert row["regime_passed"] == 1
    assert row["regime_ids"] == ["regime_fanout_width_law"]
