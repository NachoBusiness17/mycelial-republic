"""Drain must not spawn into a spent Mag cap; leave the task queued."""
from __future__ import annotations

import json


def _task(tmp_path, tid="sw-gate1", provider="deepseek", goal="do a thing"):
    q = tmp_path / "queue"
    r = tmp_path / "results"
    q.mkdir()
    r.mkdir()
    spec = {
        "task_id": tid,
        "goal": goal,
        "provider": provider,
        "status": "queued",
        "domain": "research",
        "agent_idx": 0,
        "model": None,
    }
    (q / f"{tid}.json").write_text(json.dumps(spec), encoding="utf-8")
    return q, r, spec


def test_run_once_skips_and_leaves_queued_when_spent(tmp_path, monkeypatch):
    from mag import swarm_worker as sw

    q, r, _ = _task(tmp_path)
    monkeypatch.setattr(sw, "QUEUE_DIR", q)
    monkeypatch.setattr(sw, "RESULTS_DIR", r)
    monkeypatch.setattr(
        sw, "provider_spawn_allowed",
        lambda p: {
            "ok": False,
            "reason": "quota_exhausted",
            "provider": "deepseek",
            "reset_in_hours": 1.5,
        },
    )
    called = []
    monkeypatch.setattr(sw, "_execute", lambda t: called.append(t) or ("nope", 1))

    out = sw.run_once(max_per_pass=2)
    assert called == []
    assert out["skipped"] == 1
    assert out["failed"] == 0
    assert out["done"] == 0
    queued = json.loads((q / "sw-gate1.json").read_text(encoding="utf-8"))
    assert queued["status"] == "queued"
    assert not (r / "sw-gate1.json").exists()


def test_rightsized_local_still_drains_when_remote_spent(tmp_path, monkeypatch):
    from mag import swarm_worker as sw

    q, r, _ = _task(tmp_path, tid="sw-local1", goal="list the repo files")
    monkeypatch.setattr(sw, "QUEUE_DIR", q)
    monkeypatch.setattr(sw, "RESULTS_DIR", r)
    monkeypatch.setattr(sw, "_task_tier", lambda goal: ("scut", "local"))
    monkeypatch.setattr(
        sw, "provider_spawn_allowed",
        lambda p: {"ok": False, "reason": "quota_exhausted", "provider": "deepseek"},
    )
    called = []
    monkeypatch.setattr(sw, "_execute", lambda t: called.append(t) or ("nope", 1))

    out = sw.run_rightsized_once(max_per_pass=1)
    assert called == []
    assert out["done"] == 1
    assert out["skipped"] == 0
    done = json.loads((q / "sw-local1.json").read_text(encoding="utf-8"))
    assert done["status"] == "done"
