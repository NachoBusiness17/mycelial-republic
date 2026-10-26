"""Census patrol liveness tripwire tests (B2-314, 2026-09-26).

The B2-246 falsifier class: a week where no scheduled surface runs the deep
census check, with zero signal. The tripwire names the darkness from the last
bracketed START stamp in logs/census_patrol.log (the ps1's own operator
paragraph defines the condition; this module makes an attended surface read
it). The deregistration falsifier is simulated at the bytes level: a stale /
empty / missing log must produce a "census patrol dark" line.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from mag.census_liveness import patrol_status, report

NOW = datetime(2026, 9, 26, 12, 0, 0)
FRESH = "2026-09-26 11:34:24"          # real log's last START
STALE = "2026-09-24 08:31:00"          # > 26h old


def _log(tmp_path, body: str):
    p = tmp_path / "census_patrol.log"
    p.write_text(body, encoding="utf-8")
    return p


def test_fresh_start_is_live(tmp_path):
    st = patrol_status(_log(tmp_path, f"[{FRESH}] START census deep check (--collect) cwd=x"), now=NOW)
    assert st["dark"] is False
    assert st["last_start"] == FRESH
    assert "dark" not in st["line"]


def test_stale_start_names_darkness_with_stamp(tmp_path):
    st = patrol_status(_log(tmp_path, f"[{STALE}] START census deep check (--collect) cwd=x"), now=NOW)
    assert st["dark"] is True
    assert st["line"].startswith(f"census patrol dark since {STALE}")
    assert "MagCensusPatrolDaily" in st["line"]  # names the response path
    assert 51.0 < st["age_hours"] < 52.0  # 09-24 08:31 -> 09-26 12:00 = 51.48h


def test_missing_or_empty_log_is_dark_with_reason(tmp_path):
    st = patrol_status(tmp_path / "nope.log", now=NOW)
    assert st["dark"] is True and st["last_start"] is None
    assert "no START stamp" in st["line"]
    st2 = patrol_status(_log(tmp_path, "collect-only tail: 1910 tests collected\n"), now=NOW)
    assert st2["dark"] is True and "no START stamp" in st2["line"]


def test_last_stamp_wins_and_garbage_never_crashes(tmp_path):
    body = (f"[{STALE}] START census deep check (--collect) cwd=x\n"
            "END exit=0\n"
            f"[{FRESH}] START census deep check (--collect) cwd=x\n")
    st = patrol_status(_log(tmp_path, body), now=NOW)
    assert st["dark"] is False and st["last_start"] == FRESH
    garbage = _log(tmp_path, "[not-a-timestamp] START nonsense\n\x00\r\n")
    st2 = patrol_status(garbage, now=NOW)
    assert st2["dark"] is True


def test_report_prints_the_line(tmp_path, capsys):
    p = _log(tmp_path, f"[{STALE}] START census deep check (--collect) cwd=x")
    line = report(log_path=p, now=NOW)
    assert line.startswith("census patrol dark since")
    assert line in capsys.readouterr().out


def test_context_pack_surface_is_wired():
    # the attended surface must call the report: main.py context-pack branch
    # imports and invokes mag.census_liveness.report (B2-314)
    main_src = (REPO_SRC := __import__("pathlib").Path(__file__).resolve().parents[1] / "main.py").read_text(encoding="utf-8")
    assert "from mag.census_liveness import report as census_liveness_report" in main_src
    assert "census_liveness_report()" in main_src
    # and it sits inside the context-pack branch, after the pack print
    idx_branch = main_src.index('if args.cmd == "context-pack":')
    idx_call = main_src.index("census_liveness_report()")
    assert idx_branch < idx_call
