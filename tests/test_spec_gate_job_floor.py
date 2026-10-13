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


def test_verify_after_expected_sha_oracle(isolated):
    target = isolated / "target.py"
    target.write_text("def a():\n    return 1\n", encoding="utf-8")

    # freeze the base
    f = sg.freeze(target, label="v1")
    assert f["ok"] is True

    # gate passes before apply
    assert sg.gate(target)["blocked"] is False

    # mutate the file (the apply)
    target.write_text("def a():\n    return 999\n", encoding="utf-8")
    expected = sg.fingerprint(target)

    # verify_after with expected sha -> passes when it matches
    v = sg.verify_after(target, expected_sha=expected, label="apply-v2")
    assert v["ok"] is True
    assert v["changed"] is True
    assert v["current_sha"] == expected
    assert v["expected_sha"] == expected

    # verify_after with a wrong expected sha -> fails (drifted result)
    v2 = sg.verify_after(target, expected_sha="0" * 64, label="apply-v2")
    assert v2["ok"] is False
    assert "MISMATCH" in v2["detail"]


def test_verify_after_no_expected_sha_checks_mutation(isolated):
    target = isolated / "target.py"
    target.write_text("def a():\n    return 1\n", encoding="utf-8")

    sg.freeze(target, label="v1")

    # unchanged -> not ok (apply did not mutate)
    v = sg.verify_after(target)
    assert v["ok"] is False
    assert v["changed"] is False
    assert "UNCHANGED" in v["detail"]

    # mutate -> ok (apply actually mutated the file)
    target.write_text("def a():\n    return 999\n", encoding="utf-8")
    v2 = sg.verify_after(target)
    assert v2["ok"] is True
    assert v2["changed"] is True
    assert "CHANGED" in v2["detail"]


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
