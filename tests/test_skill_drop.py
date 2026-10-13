"""Skill-drop — timed, frozen, right-sized breadcrumbs (deterministic, no model)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mag.operator_inbox as oi  # noqa: E402
import mag.skill_drop as sd  # noqa: E402
from mag import job_floor as jf  # noqa: E402


def _isolate(monkeypatch, tmp_path):
    monkeypatch.setattr(sd, "DROPS_PATH", tmp_path / "skill_drops.json")
    monkeypatch.setattr(oi, "INBOX_PATH", tmp_path / "inbox.json")
    monkeypatch.setattr(oi, "EVENTS_PATH", tmp_path / "events.jsonl")
    monkeypatch.setattr(jf, "JOBS_PATH", tmp_path / "jobs.json")


def test_right_size_caps(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    _isolate(monkeypatch, tmp_path)
    long = ("Do the thing. " * 40) + "\nverify: run pytest and check green"
    nug = sd.right_size(long)
    assert len(nug) <= sd.NUGGET_LIMIT
    assert "verify" in nug


def test_freeze_verify_drift(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    _isolate(monkeypatch, tmp_path)
    r = sd.drop_skill("test", "Verify with diff before done.")
    did = r["drop"]["id"]
    assert sd.verify_drop(did)["ok"] is True
    # tamper the stored content → drift
    d = sd._load()
    d["drops"][0]["content"] = "TAMPERED"
    sd._save(d)
    assert sd.verify_drop(did)["ok"] is False


def test_drop_queues_then_releases_only_on_done(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    _isolate(monkeypatch, tmp_path)
    sd.drop_skill("skill-a", "Verify with diff before declaring done.", job_id="job-1")
    assert sd.status()["by_state"].get("queued") == 1
    # not released on executing
    assert sd.release_due(job_state="executing", job_id="job-1") == []
    assert sd.status()["by_state"].get("queued") == 1
    # released on done
    rel = sd.release_due(job_state="done", job_id="job-1")
    assert len(rel) == 1
    assert rel[0]["state"] == "released"


def test_release_filters_by_job_id(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    _isolate(monkeypatch, tmp_path)
    sd.drop_skill("for-job-a", "Do A.", job_id="job-a")
    assert sd.release_due(job_state="done", job_id="job-b") == []
    assert len(sd.release_due(job_state="done", job_id="job-a")) == 1


def test_job_floor_hook_releases_on_done(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    """The exact-right-time hook: verify→done fires the skill drop."""
    _isolate(monkeypatch, tmp_path)
    sd.drop_skill("post-job", "Verify with git diff before declaring done.", job_id="")
    job = jf.create_job("test hook", seat="local")
    jid = job["id"]
    jf.claim_job(jid)
    jf.verify_job(jid, ok=True, detail="verified")
    # the drop should now be released and sitting in the inbox as guidance
    st = sd.status()
    assert st["by_state"].get("released") == 1
    inbox = oi.status()
    assert inbox["pending_n"] >= 1
    assert any("SKILL DROP" in str(x.get("text") or "") for x in inbox["pending"])
