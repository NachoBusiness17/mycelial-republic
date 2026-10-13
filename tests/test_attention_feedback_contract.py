"""Contract test: a cast through the flagship feedback pipe (mag.feedback) is
accepted by the attention ranker's vocabulary.

Guards the 2026-08 contract drift (w4-37 Receipt 6): mag/feedback.py normalized
every cast to good/bad while mag/attention_ranker.py:17 accepts only
{useful, wallpaper, pin, mute, acted}, so every cast was rejected with
{"ok": False, "error": "signal must be one of ..."} while the pipe still
reported overall success. Since this file exists, the drift is a red test, not
a silent zero on the only price-discovery channel the estate owns.
"""
from __future__ import annotations

import json

import mag.attention_ranker as ranker
import mag.feedback as feedback


def _isolate(tmp_path, monkeypatch):
    """Point every ledger the pipe touches at tmp; never the live estate."""
    monkeypatch.setattr(ranker, "FEEDBACK_PATH", tmp_path / "attention_feedback.jsonl")
    monkeypatch.setattr(feedback, "TRAINING", tmp_path / "training_rows.jsonl")
    monkeypatch.setattr(feedback, "FEEDBACK_LEDGER", tmp_path / "feedback.jsonl")
    import mag.verkle_knot as vk

    monkeypatch.setattr(vk, "append_verkle_knot", lambda payload: {"ok": True})


def _soft_repo(monkeypatch):
    """Ranker collectors patched to one soft (priceable) item: repo:ready."""
    monkeypatch.setattr(ranker, "_repo_snapshot", lambda: {
        "ok": True, "branch": "mag/test", "upstream": "origin/mag/test",
        "head": "abc", "handoff_ready": True, "blockers": [],
    })
    monkeypatch.setattr(ranker, "_task_rows", lambda: [])
    monkeypatch.setattr(ranker, "_roadmap_snapshot", lambda: {"next": {"ok": False}})
    monkeypatch.setattr(ranker, "_inbox_snapshot", lambda: {"pending_n": 0})


def test_good_cast_through_flagship_pipe_is_accepted_by_ranker_vocabulary(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    res = feedback.capture("good", item_id="repo:ready", source="test")
    assert res["ok"] is True
    assert res["ranking"] is True
    assert res["signal"] == "useful"
    rows = [json.loads(x) for x in
            (tmp_path / "attention_feedback.jsonl").read_text(encoding="utf-8").splitlines() if x]
    assert len(rows) == 1
    assert rows[0]["signal"] in ranker.ALLOWED_SIGNALS
    assert rows[0]["item_id"] == "repo:ready"
    # the ranker's own trade ledger now maps the cast
    assert ranker._feedback() == {"repo:ready": ["useful"]}


def test_bad_cast_lands_as_wallpaper_and_reprices_the_feed(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    _soft_repo(monkeypatch)
    before = ranker.build_ranked_attention()["items"][0]
    assert before["id"] == "repo:ready"
    res = feedback.capture("bad", item_id="repo:ready", source="test")
    assert res["ok"] is True and res["ranking"] is True
    assert res["signal"] == "wallpaper"
    after = ranker.build_ranked_attention()["items"][0]
    assert after["score"] == before["score"] - 8  # the ranker's wallpaper tax settled


def test_thumbs_aliases_map_into_the_one_vocabulary(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    assert feedback.capture("thumbs-up", item_id="x1")["signal"] == "useful"
    assert feedback.capture("thumbs-down", item_id="x2")["signal"] == "wallpaper"
    assert feedback.capture("down", item_id="x3")["signal"] == "wallpaper"
    signals = [json.loads(x)["signal"] for x in
               (tmp_path / "attention_feedback.jsonl").read_text(encoding="utf-8").splitlines() if x]
    assert set(signals) <= ranker.ALLOWED_SIGNALS


def test_native_ranker_signals_pass_through_untouched(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    _soft_repo(monkeypatch)
    res = feedback.capture("mute", item_id="repo:ready", source="test")
    assert res["ok"] is True and res["signal"] == "mute"
    item = ranker.build_ranked_attention()["items"][0]
    assert item["id"] == "repo:ready"
    assert item["band"] == "P5" and item["score"] == 0


def test_pipe_ledger_and_training_row_carry_the_canonical_signal(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    feedback.capture("good", item_id="repo:ready", source="test")
    ledger = [json.loads(x) for x in
              (tmp_path / "feedback.jsonl").read_text(encoding="utf-8").splitlines() if x]
    training = [json.loads(x) for x in
                (tmp_path / "training_rows.jsonl").read_text(encoding="utf-8").splitlines() if x]
    assert ledger[0]["signal"] == "useful"
    assert training[0]["signal"] == "useful"
    assert training[0]["source"] == "feedback"


def test_ranker_rejection_is_exit_code_visible_not_boolean_cosmetic(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    # simulate the exact historical drift: the ranker refuses the cast.
    # feedback.py binds record_feedback at module import, so patch the name the
    # pipe actually calls.
    monkeypatch.setattr(feedback, "record_feedback",
                        lambda item_id, signal, source="dashboard": {
                            "ok": False, "error": "signal must be one of ['acted', ...]"})
    res = feedback.capture("good", item_id="repo:ready", source="test")
    assert res["ok"] is False
    assert res["ranking"] is False
    assert "signal must be one of" in res["ranking_error"]
    assert feedback.main(["good", "repo:ready"]) == 1


def test_unknown_signal_is_rejected_loudly(tmp_path, monkeypatch):
    _isolate(tmp_path, monkeypatch)
    res = feedback.capture("meh", item_id="x")
    assert res["ok"] is False
    assert "useful" in res["error"]
