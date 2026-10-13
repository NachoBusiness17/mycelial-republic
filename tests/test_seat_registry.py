"""Seat registry union — desktop/cloud seats visible to orchestrator + switchboard."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _isolate_seat_trail(tmp_path, monkeypatch):
    """B2-401: the writer's env seam points the trail at tmp, so register/
    unregister calls never append to the production seat_registry_trail.jsonl
    (111 pytest-parent rows were on disk at fix time)."""
    monkeypatch.setenv("MAG_SEAT_REGISTRY_TRAIL", str(tmp_path / "seat_registry_trail.jsonl"))
    # mesh_peers exercises orchestrator touch_external, which writes the
    # orchestrator trail; isolate both seams in one fixture.
    monkeypatch.setenv("MAG_ORCHESTRATOR_TRAIL", str(tmp_path / "orchestrator_trail.jsonl"))


def test_register_external():
    from mag.seat_registry import register, unregister

    rec = register(seat="cursor", goal="test session", parent="pytest", mode="interactive")
    assert rec.get("ok") is True
    tid = rec["task_id"]
    assert tid.startswith("ext-")
    assert rec.get("mag_task_id") == tid
    done = unregister(tid, status="done")
    assert done.get("ok") is True


def test_timeout_for_improve():
    from mag.orchestrator import IMPROVE_TIMEOUT, DEFAULT_TIMEOUT, timeout_for_goal

    assert timeout_for_goal("[improve] fix flaky test", tag="improve-c1") == IMPROVE_TIMEOUT
    # rebased 2026-09-26 (B2-401, claim-law rebase on already-landed bytes):
    # timeout_for_goal defers to the temperature-stack YAML heat band before
    # the DEFAULT_TIMEOUT fallback, so tag "api" resolves to the stack value
    # (600), not the bare constant.
    assert timeout_for_goal("normal job", tag="api") == 600
    assert IMPROVE_TIMEOUT < DEFAULT_TIMEOUT


def test_mesh_peers_includes_external():
    from mag.seat_registry import mesh_peers, register, unregister

    rec = register(seat="cloud", goal="cloud agent", parent="pytest", mode="cloud")
    tid = rec["task_id"]
    peers = mesh_peers()
    assert any(p.get("task_id") == tid for p in peers)
    unregister(tid)


def test_switchboard_sees_external():
    from mag.seat_registry import register, unregister
    from mag.switchboard import mesh

    rec = register(seat="cursor", goal="switchboard test", parent="pytest")
    tid = rec["task_id"]
    m = mesh(include_seats=False)
    peer_ids = [p.get("task_id") for p in m.get("peers") or []]
    assert tid in peer_ids
    unregister(tid)
