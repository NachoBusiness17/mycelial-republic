"""Spec gate (wrong-offset) + job floor (DFHack designation manager)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import mag.spec_gate as sg
import mag.job_floor as jf


@pytest.fixture
def isolated(tmp_path, monkeypatch):
    gate_state = tmp_path / "spec_gate.json"
    floor_path = tmp_path / "job_floor" / "jobs.json"
    monkeypatch.setattr(sg, "GATE_STATE", gate_state)
    monkeypatch.setattr(jf, "JOBS_PATH", floor_path)
    return tmp_path


def test_gate_freezes_and_blocks_on_drift(isolated):
    target = isolated / "target.py"
    target.write_text("def a():\n    return 1\n", encoding="utf-8")

    # no base yet -> gate blocks (nothing frozen)
    g = sg.gate(target)
    assert g["blocked"] is True

    # freeze the base
    f = sg.freeze(target, label="v1")
    assert f["ok"] is True

    # unchanged -> gate passes
    g2 = sg.gate(target)
    assert g2["blocked"] is False

    # drift -> gate blocks (wrong offset refusal)
    target.write_text("def a():\n    return 999\n", encoding="utf-8")
    g3 = sg.gate(target)
    assert g3["blocked"] is True
    assert "DRIFT" in g3["detail"]


def test_job_floor_lifecycle_and_stuck_watchdog(isolated):
    r = jf.create_job("add timeout to chat()", seat="local", targets=[str(isolated / "none.py")])
    assert r["state"] == "designated"

    claimed = jf.claim_job(r["id"])
    assert claimed["job"]["state"] == "executing"

    ok = jf.verify_job(r["id"], ok=True, detail="passed")
    assert ok["job"]["state"] == "done"

    # a stuck job: create + claim, then force max_s past
    j2 = jf.create_job("hanging job", seat="deepseek", max_s=0.0)
    jf.claim_job(j2["id"])
    stuck = jf.stuck_jobs(max_s=0.0)
    ids = {str(s["id"]) for s in stuck}
    assert j2["id"] in ids
    assert jf._job(j2["id"])["state"] == "stuck"


def test_job_floor_fail_goes_to_needs_escalate(isolated):
    j = jf.create_job("vague edit", seat="local")
    jf.claim_job(j["id"])
    r = jf.verify_job(j["id"], ok=False, detail="fake success, no diff")
    assert r["job"]["state"] == "needs_escalate"
    st = jf.status()
    assert st["by_state"].get("needs_escalate") == 1
