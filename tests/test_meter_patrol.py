"""Meter patrol tests (B2-469, 2026-09-26).

Follows tests/test_census_drift_patrol.py house style: the pure cores
(boundary-true matching, row shapes) pinned in-process, and the CLI contract
(0 rows current, 1 GAP named, 2 cannot-verify) pinned through a subprocess
against a synthetic mini-inbox in tmp_path. The regression anchor is the
B2-166 Evidence 5 disease: a case-insensitive "ebs" match inside "website"
must never arm the national-alert meter, and silence must emit an explicit
NOBS row instead of staying implicit.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

import tools.meter_patrol as mp

TOOL = Path(mp.__file__).resolve()


@pytest.fixture()
def estate(tmp_path: Path) -> Path:
    (tmp_path / "watch" / "inbox").mkdir(parents=True)
    return tmp_path


def meter_class_rows(ledger: Path, cls: str, day: str) -> list[dict]:
    rows = [json.loads(x) for x in ledger.read_text(encoding="utf-8").splitlines() if x.strip()]
    return [r for r in rows if r["meter_class"] == cls and r["date"] == day]


def test_website_never_arms_ebs() -> None:
    text = "read the full note on the website"
    assert not any(p.search(text) for p in mp.METERS["national_alert_nonweather"]["patterns"])


def test_case_sensitive_tokens() -> None:
    assert any(p.search("MOEX halted trading") for p in mp.METERS["moex_xrp_halt"]["patterns"])
    assert not any(p.search("moex halted trading") for p in mp.METERS["moex_xrp_halt"]["patterns"])
    assert any(p.search("EBS activated") for p in mp.METERS["national_alert_nonweather"]["patterns"])


def test_nobs_row_names_the_absence() -> None:
    row = mp.build_row(mp.date(2026, 9, 26), "T", "g20_circuit_breaker", [])
    assert row["state"] == "NOBS"
    assert row["pointers"] == []
    assert "not evidence of absence" in row["note"]


def test_receipt_row_is_candidate_only() -> None:
    row = mp.build_row(mp.date(2026, 9, 26), "T", "g20_circuit_breaker", ["watch/inbox/x.md"])
    assert row["state"] == "RECEIPT"
    assert "never a HIT verdict" in row["note"]
    assert row["pointer_count"] == 1


def test_cli_nobs_and_receipt_and_idempotency(estate: Path) -> None:
    inbox = estate / "watch" / "inbox"
    (inbox / "wire.md").write_text("MOEX XRP futures halted", encoding="utf-8")
    first = subprocess.run([sys.executable, str(TOOL), "--root", str(estate)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    assert first.returncode == 0, first.stdout + first.stderr
    ledger = estate / "watch" / "inbox" / "DATED_METERS.jsonl"
    lines = ledger.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 4  # one row per frozen meter class
    day = json.loads(lines[0])["date"]
    moex = meter_class_rows(ledger, "moex_xrp_halt", day)[0]
    assert moex["state"] == "RECEIPT"
    assert moex["pointers"] == ["watch/inbox/wire.md"]
    blackout = meter_class_rows(ledger, "g20_blackout_gt1m_6h", moex["date"])[0]
    assert blackout["state"] == "NOBS"
    # Rerun the same day: zero new rows, never duplicates.
    second = subprocess.run([sys.executable, str(TOOL), "--root", str(estate)],
                            capture_output=True, text=True, encoding="utf-8", errors="replace",
                            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    assert second.returncode == 0
    assert len(ledger.read_text(encoding="utf-8").splitlines()) == 4
    assert "0 new, 4 already metered" in second.stdout


def test_cli_gap_is_named_never_backfilled(estate: Path) -> None:
    ledger = estate / "watch" / "inbox" / "DATED_METERS.jsonl"
    day1 = json.dumps({"schema": "dated_meter_v1", "ts": "T", "date": "2026-09-26",
                       "organ": "meter_patrol", "meter_class": "g20_circuit_breaker",
                       "state": "NOBS", "pointers": [], "note": "n"}, ensure_ascii=False)
    ledger.write_text(day1 + "\n", encoding="utf-8")
    out = subprocess.run([sys.executable, str(TOOL), "--root", str(estate),
                          "--date", "2026-09-28"], capture_output=True, text=True,
                         encoding="utf-8", errors="replace",
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    assert out.returncode == 1
    assert "GAP" in out.stdout and "2026-09-27" in out.stdout
    days = {json.loads(x)["date"] for x in ledger.read_text(encoding="utf-8").splitlines() if x.strip()}
    assert days == {"2026-09-26", "2026-09-28"}  # the dark day got no invented rows


def test_cli_corrupt_ledger_fails_closed(estate: Path) -> None:
    ledger = estate / "watch" / "inbox" / "DATED_METERS.jsonl"
    ledger.write_text("{not json\n", encoding="utf-8")
    out = subprocess.run([sys.executable, str(TOOL), "--root", str(estate)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    assert out.returncode == 2
    assert "cannot verify" in out.stdout


def test_cli_missing_inbox_fails_closed(tmp_path: Path) -> None:
    out = subprocess.run([sys.executable, str(TOOL), "--root", str(tmp_path)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    assert out.returncode == 2
    assert "cannot verify" in out.stdout
