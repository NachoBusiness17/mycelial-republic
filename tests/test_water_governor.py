"""Tests for tools/water_governor.py - census classification, row banking,
conservation report. Consumer: water_governor module docstring.
Verifier: this file (run with the repo venv)."""
from __future__ import annotations

import json

import pytest

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.water_governor import census, report, CARRIER_FAMILIES  # noqa: E402


FIXTURE_ENV = (
    "ZAI_API_KEY=x\nZAI_API_KEY_2=y\nOPENROUTER_API_KEY=o\nDEEPSEEK_API_KEY=d\n"
    "GROQ_API_KEY=g\nGEMINI_API_KEY=gm\nHERMES_API_KEY_1=h\nOLLAMA_HOST=oh\n"
    "OPENCODE=oc\nTOTALLY_UNKNOWN_KEY=u\n"
)


def test_census_classifies_families_and_never_reads_values():
    c = census(FIXTURE_ENV)
    got = {t["tank"]: t for t in c["tanks"]}
    assert got["zai_session"]["keys_found"] == 2
    assert got["zai_session"]["status"] == "WIRED"
    assert got["openrouter_free"]["status"] == "WIRED"
    assert got["deepseek"]["status"] == "WIRED"
    assert got["groq"]["status"] == "DEAD"
    assert got["google"]["status"] == "MOUNTED"
    assert got["local_shelf"]["status"] == "WIRED"
    assert got["opencode_cli"]["status"] == "EXTERNAL"
    # values never appear anywhere in the census output
    blob = json.dumps(c)
    for value in ("=x", "=y", "=o", "=d", "=g", "=gm", "=h", "=oh", "=oc", "=u"):
        assert value not in blob


def test_census_unmatched_names_are_counted_not_silent():
    c = census(FIXTURE_ENV)
    # TOTALLY_UNKNOWN_KEY is not a carrier family but must be accounted for
    named = sum(t["keys_found"] for t in c["tanks"])
    assert named < c["total_key_names"], "unknown names must keep the total honest"


def test_every_family_declares_status_and_mount():
    for pattern, family, status, note in CARRIER_FAMILIES:
        assert status in ("WIRED", "MOUNTED", "DEAD", "EXTERNAL"), family
        assert note and len(note) > 10, family


def test_report_flags_handwave_crime(tmp_path, monkeypatch):
    import tools.water_governor as wg
    ledger = tmp_path / "usage.jsonl"
    good = {"ts": "t", "beat": "b", "tank": "x", "model": "m", "ok_api": True,
            "ok_material": True, "latency_ms": 1, "note": "n"}
    orphan = dict(good, ok_api=None)
    ledger.write_text(json.dumps(good) + "\n" + json.dumps(orphan) + "\n", encoding="utf-8")
    monkeypatch.setattr(wg, "LEDGER", ledger)
    rep = wg.report()
    assert rep["rows_total"] == 2
    assert rep["handwave_crime"] is True and rep["orphan_unbanked"] == 1
    assert rep["by_tank"]["x"]["dispatched"] == 2
    monkeypatch.setattr(wg, "LEDGER", tmp_path / "clean.jsonl")
    (tmp_path / "clean.jsonl").write_text(json.dumps(good) + "\n", encoding="utf-8")
    rep2 = wg.report()
    assert rep2["handwave_crime"] is False


def test_report_no_ledger_is_honest(tmp_path, monkeypatch):
    import tools.water_governor as wg
    monkeypatch.setattr(wg, "LEDGER", tmp_path / "missing.jsonl")
    assert "error" in wg.report()


def test_window_state_burn_down_calculus():
    from datetime import datetime, timezone, timedelta
    from tools.water_governor import window_state, WINDOW_HOURS
    now = datetime(2026, 10, 20, 12, 0, tzinfo=timezone.utc)
    # window opened 4h ago with one ask: 1h to reset
    fresh = now - timedelta(hours=4)
    st = window_state([fresh.isoformat()], now=now)
    assert st["window_open"] and st["asks_in_window"] == 1
    assert st["minutes_to_reset"] == 60
    # near reset + unspent: BURN-DOWN NOW
    near = now - timedelta(hours=WINDOW_HOURS) + timedelta(minutes=30)
    st2 = window_state([near.isoformat()], now=now)
    assert "BURN-DOWN NOW" in st2["posture"]
    # old asks age out of the window
    stale = now - timedelta(hours=9)
    st3 = window_state([stale.isoformat()], now=now)
    assert st3["window_open"] is False and st3["asks_in_window"] == 0


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
