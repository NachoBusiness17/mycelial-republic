"""Idempotency + read-path contract for the attention market's trade ledger.

The ledger memory/attention_feedback.jsonl recorded ZERO trades in its first 54
days (w4-03, w4-37): the POST /api/v1/attention-feedback handler passed the raw
body signal to record_feedback, so a thumbs-vocabulary cast was rejected, and
nothing anywhere pinned a retried POST to a single append. These tests pin the
2026-09-29 ball attention-ledger wiring: settle-once cast_id idempotency, the
unified five-signal vocabulary at the dashboard surface, and the public read
path (mag.attention_ranker.read_feedback) that feeds the next ranking pass.
"""
from __future__ import annotations

import json

import mag.attention_ranker as ranker


def _isolate(tmp_path, monkeypatch):
    """Point the trade ledger at tmp; never the live estate."""
    monkeypatch.setattr(ranker, "FEEDBACK_PATH", tmp_path / "attention_feedback.jsonl")


def _rows(tmp_path):
    p = tmp_path / "attention_feedback.jsonl"
    if not p.is_file():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x]


def _soft_repo(monkeypatch):
    """Ranker collectors patched to one soft (priceable) item: repo:ready."""
    monkeypatch.setattr(ranker, "_repo_snapshot", lambda: {
        "ok": True, "branch": "mag/test", "upstream": "origin/mag/test",
        "head": "abc", "handoff_ready": True, "blockers": [],
    })
    monkeypatch.setattr(ranker, "_task_rows", lambda: [])
    monkeypatch.setattr(ranker, "_roadmap_snapshot", lambda: {"next": {"ok": False}})
    monkeypatch.setattr(ranker, "_inbox_snapshot", lambda: {"pending_n": 0})


def test_retried_post_with_same_cast_id_appends_exactly_once(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    first = ranker.record_feedback("repo:ready", "useful", source="dashboard", cast_id="ball-1")
    assert first["ok"] is True and "duplicate" not in first
    replay = ranker.record_feedback("repo:ready", "useful", source="dashboard", cast_id="ball-1")
    assert replay["ok"] is True and replay["duplicate"] is True
    assert replay["event"] == first["event"]
    assert len(_rows(tmp_path)) == 1  # zero-double-append


def test_replay_settles_the_original_trade_even_when_the_retry_disagrees(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    first = ranker.record_feedback("repo:ready", "useful", cast_id="ball-2")
    replay = ranker.record_feedback("repo:ready", "wallpaper", cast_id="ball-2")
    assert replay["duplicate"] is True
    assert replay["event"]["signal"] == "useful"  # the first settled trade wins
    assert [r["signal"] for r in _rows(tmp_path)] == ["useful"]


def test_cast_without_idempotency_key_is_a_distinct_trade(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    ranker.record_feedback("repo:ready", "useful")
    ranker.record_feedback("repo:ready", "useful")
    assert len(_rows(tmp_path)) == 2  # legacy semantics: every cast is a trade


def test_ledger_rows_carry_the_unified_five_signal_vocabulary(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    for sig in sorted(ranker.ALLOWED_SIGNALS):
        assert ranker.record_feedback("repo:ready", sig, cast_id=f"c-{sig}")["ok"] is True
    rejected = ranker.record_feedback("repo:ready", "good")  # thumbs never lands raw
    assert rejected["ok"] is False
    assert {r["signal"] for r in _rows(tmp_path)} == ranker.ALLOWED_SIGNALS


def test_real_cast_feeds_the_next_ranking_pass(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    _soft_repo(monkeypatch)
    before = ranker.build_ranked_attention()["items"][0]
    assert before["id"] == "repo:ready"
    res = ranker.record_feedback("repo:ready", "useful", source="dashboard", cast_id="ball-live")
    assert res["ok"] is True
    after_item = ranker.build_ranked_attention()["items"][0]
    assert after_item["score"] == before["score"] + 4  # the cast repriced the feed
    assert "useful" in after_item["feedback"]
    assert ranker.read_feedback() == {"repo:ready": ["useful"]}  # public read path


def test_dashboard_post_normalizes_thumbs_and_replays_idempotently(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    from dashboard import rest

    body = {"item_id": "repo:ready", "signal": "good", "cast_id": "ball-ui-1"}
    hit1 = rest.dispatch("POST", "/api/v1/attention-feedback", dict(body))
    assert hit1 is not None and hit1[0] == 200 and hit1[1]["ok"] is True
    hit2 = rest.dispatch("POST", "/api/v1/attention-feedback", dict(body))
    assert hit2 is not None and hit2[0] == 200 and hit2[1]["duplicate"] is True
    rows = _rows(tmp_path)
    assert len(rows) == 1
    assert rows[0]["signal"] == "useful"  # thumbs mapped at the REST surface
    assert rows[0]["cast_id"] == "ball-ui-1"


def test_dashboard_post_rejects_unknown_signal_loudly(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    from dashboard import rest

    hit = rest.dispatch("POST", "/api/v1/attention-feedback",
                        {"item_id": "repo:ready", "signal": "meh"})
    assert hit is not None and hit[0] == 400
    assert _rows(tmp_path) == []
