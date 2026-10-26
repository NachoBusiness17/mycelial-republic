"""Tests for tools/commit_sweeper.py - the single git writer.
Verifier: this file. Consumer: module docstring."""
from __future__ import annotations

import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import commit_sweeper as cs  # noqa: E402


import pytest


@pytest.fixture(autouse=True)
def _isolate_pid_dir(tmp_path, monkeypatch):
    """Never claim the live sweeper's pidfile from a test (2026-10-21)."""
    monkeypatch.setattr(cs, "PID_DIR", tmp_path / "state")
    monkeypatch.setattr(cs, "BREATH_LEDGER", tmp_path / "breath_ledger.jsonl")
    # never run real git against the live repo from any test (2026-10-23)
    monkeypatch.setattr(cs, "git", lambda *a, **k: type("P", (), {"stdout": "", "returncode": 0})())


def test_malformed_hint_never_blocks_others(tmp_path, monkeypatch):
    good = tmp_path / "b-good.json"
    bad = tmp_path / "a-bad.json"
    bad.write_text("{not json", encoding="utf-8")
    good.write_text(json.dumps({"paths": [], "message": "m"}), encoding="utf-8")
    monkeypatch.setattr(cs, "HINTS", tmp_path)
    monkeypatch.setattr(cs, "lock_busy", lambda: False)
    calls = []
    monkeypatch.setattr(cs, "commit_batch", lambda p, m, timeout=900: calls.append(m) or (True, "tip"))
    rep = cs.sweep()
    # both hints processed; the malformed one did not stop the good one;
    # the leftover sweep may append after them
    assert [r["hint"] for r in rep["results"]][:2] == ["a-bad.json", "b-good.json"]
    assert rep["results"][0]["committed"] is False
    assert calls[:1] == ["m"]


def test_good_hint_is_consumed(tmp_path, monkeypatch):
    h = tmp_path / "seat-x.json"
    h.write_text(json.dumps({"paths": ["a.md"], "message": "named batch"}), encoding="utf-8")
    monkeypatch.setattr(cs, "HINTS", tmp_path)
    monkeypatch.setattr(cs, "lock_busy", lambda: False)
    calls = []
    monkeypatch.setattr(cs, "commit_batch", lambda p, m, timeout=900: calls.append({"paths": p, "msg": m}) or (True, "tip"))
    cs.sweep()
    named = [c for c in calls if c["msg"] == "named batch"]
    assert named and named[0]["paths"] == ["a.md"], calls
    assert not h.exists(), "consumed hints are removed"


def test_lock_busy_skips_cleanly(tmp_path, monkeypatch):
    monkeypatch.setattr(cs, "HINTS", tmp_path)
    monkeypatch.setattr(cs, "lock_busy", lambda: True)
    # the sweeper now waits out a transient lock; pin the wait to "still held"
    # so the test exercises the skip path without sleeping 30s.
    monkeypatch.setattr(cs, "wait_for_git_lock", lambda *a, **k: False)
    rep = cs.sweep()
    assert rep == {"skipped": "index.lock held after wait"}


def test_dry_mode_touches_nothing(tmp_path, monkeypatch):
    h = tmp_path / "s.json"
    h.write_text(json.dumps({"paths": ["x"], "message": "m"}), encoding="utf-8")
    monkeypatch.setattr(cs, "HINTS", tmp_path)
    monkeypatch.setattr(cs, "lock_busy", lambda: False)
    rep = cs.sweep(dry=True)
    assert rep["hints"][0]["dry"] is True
    assert h.exists(), "dry mode must not consume hints"


def test_breath_id_shape_and_trailers(monkeypatch):
    monkeypatch.setitem(cs._CTX, "breath_id", "B-20261022T225900Z-abc123")
    monkeypatch.setitem(cs._CTX, "seat", "hermes")
    monkeypatch.setitem(cs._CTX, "model", "glm-4.6")
    msg = cs._trailers("named batch")
    assert msg.startswith("named batch\n\nBreath-Id: B-20261022T225900Z-abc123\n")
    assert "Seat: hermes" in msg and "Model: glm-4.6" in msg
    assert cs._author_args() == ["--author=hermes <hermes@seats.mag.local>"]
    import re as _re
    assert _re.match(r"^B-\d{8}T\d{6}Z-[0-9a-f]{6}$", cs.new_breath_id())


def test_no_breath_means_message_untouched(monkeypatch):
    monkeypatch.setitem(cs._CTX, "breath_id", None)
    assert cs._trailers("m") == "m" and cs._author_args() == []


def test_unattributed_falls_back_honestly(monkeypatch):
    monkeypatch.setitem(cs._CTX, "breath_id", "B-x")
    monkeypatch.setitem(cs._CTX, "seat", None)
    assert "Seat: unknown-seat" in cs._trailers("m")
    assert cs._author_args() == ["--author=unknown-seat <unknown-seat@seats.mag.local>"]


def test_hint_attribution(tmp_path, monkeypatch):
    monkeypatch.setenv("MAG_SEAT_MODEL_HERMES", "kimi-k2")
    assert cs.hint_attribution(tmp_path / "hermes-fold.json", {}) == ("hermes", "kimi-k2")
    assert cs.hint_attribution(tmp_path / "x.json", {"seat": "bob", "model": "m1"}) == ("bob", "m1")
    assert cs.hint_attribution(tmp_path / "noseat.json", {})[0] == "unknown-seat"
    assert cs.hint_attribution(tmp_path / "bad seat!-x.json", {})[0] == "unknown-seat"


def test_sweep_writes_one_ledger_row_with_one_breath(tmp_path, monkeypatch):
    h = tmp_path / "hermes-a.json"
    h.write_text(json.dumps({"paths": ["a.md"], "message": "named"}), encoding="utf-8")
    monkeypatch.setattr(cs, "HINTS", tmp_path)
    monkeypatch.setattr(cs, "lock_busy", lambda: False)
    seen = []
    monkeypatch.setattr(cs, "commit_batch",
                        lambda p, m, timeout=900: seen.append(dict(cs._CTX)) or (True, "tip"))
    # keep the test off the live repo index entirely
    monkeypatch.setattr(cs, "git", lambda *a, **k: type("P", (), {"stdout": "", "returncode": 0})())
    rep = cs.sweep()
    rows = (tmp_path / "breath_ledger.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(rows) == 1 and json.loads(rows[0])["breath_id"] == rep["breath_id"]
    assert seen and seen[0]["seat"] == "hermes" and seen[0]["breath_id"] == rep["breath_id"]
