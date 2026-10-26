"""Draft tests for tools/breath_watchdog.py (all paths redirected to tmp)."""
from __future__ import annotations
import json
from datetime import datetime, timedelta, timezone
from tools import breath_watchdog as bw


def _setup(tmp_path, monkeypatch, start):
    led = tmp_path / "breath_ledger.jsonl"
    led.write_text(json.dumps({"start": start}) + "\n", encoding="utf-8")
    monkeypatch.setattr(bw, "LEDGER", led)
    monkeypatch.setattr(bw, "TASK_LOG", tmp_path / "none.log")
    monkeypatch.setattr(bw, "STATE", tmp_path / "state.json")
    filed = []
    monkeypatch.setattr(bw, "_file_notice", lambda rep, dry: filed.append(rep) or {"ok": 1})
    return filed


def test_fresh_breath_files_nothing(tmp_path, monkeypatch):
    now = datetime(2026, 10, 22, 23, 0, tzinfo=timezone.utc)
    filed = _setup(tmp_path, monkeypatch, (now - timedelta(minutes=9)).isoformat())
    assert bw.check(now=now)["stale"] is False and filed == []


def test_stale_files_once_then_cancels(tmp_path, monkeypatch):
    now = datetime(2026, 10, 22, 23, 0, tzinfo=timezone.utc)
    filed = _setup(tmp_path, monkeypatch, (now - timedelta(minutes=21)).isoformat())
    bw.check(now=now); bw.check(now=now + timedelta(minutes=5))
    assert len(filed) == 1 and filed[0]["category"] == "lane_down"
    (tmp_path / "breath_ledger.jsonl").write_text(json.dumps({"start": now.isoformat()}) + "\n")
    bw.check(now=now + timedelta(minutes=6))
    assert len(filed) == 2 and filed[1]["cancels"] == filed[0]["notice_id"]
