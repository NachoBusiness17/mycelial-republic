"""Drift-patrol prompt repo-copy freshness test (B2-267, 2026-09-26).

The drift-patrol cron's prompt lives OUTSIDE the repo
(%USERPROFILE%/.zcode/v2/tasks-index.sqlite, automations row
automation-a7c71ad1), which is why the B2-199 living-law amendment had no
repo copy and the touch law (B2-237) could silently postdate it. This test
is the freshness_check pattern applied to that prompt: the DB bytes are the
source of truth, configs/drift_patrol_prompt.txt is the repo-side copy, and
a drift between them is RED with repair instructions (rerun
watch/inbox/burn_wave_20260926/B2_267_update_prompt.py, which is idempotent
and rewrites the copy from the DB). Skips (never fails) when the DB or the
automation row is unreachable: a different machine has no DB, and this test
must not manufacture a failure the repo cannot own.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
COPY = REPO / "configs" / "drift_patrol_prompt.txt"
DB = Path(r"C:/Users/foste/.zcode/v2/tasks-index.sqlite")
AID = "automation-a7c71ad1-f43f-403d-8677-105f5176df2b"

TOUCH_LAW_MARKERS = (
    "TOUCH LAW (B2-237",                    # the law block header
    "never open registered or living-sealed logs in write-capable mode",   # clause 6a
    "mtime is not tamper evidence",         # clause 6b
    "still filed (paths, window, writer or \"unattributed\")",             # clause 6c
)


def _db_prompt() -> str | None:
    if not DB.is_file():
        return None
    try:
        con = sqlite3.connect(f"file:{DB.as_posix()}?mode=ro", uri=True)
        row = con.execute(
            "SELECT prompt FROM automations WHERE automation_id = ?", (AID,)
        ).fetchone()
        con.close()
    except sqlite3.Error:
        return None
    return row[0] if row else None


def test_repo_copy_exists_and_carries_touch_law():
    assert COPY.is_file(), (
        "configs/drift_patrol_prompt.txt missing: rerun "
        "watch/inbox/burn_wave_20260926/B2_267_update_prompt.py"
    )
    text = COPY.read_text(encoding="utf-8")
    for marker in TOUCH_LAW_MARKERS:
        assert marker in text, f"repo copy lacks touch-law clause: {marker!r}"


def test_repo_copy_matches_live_db_bytes():
    db = _db_prompt()
    if db is None:
        pytest.skip("tasks-index.sqlite or automation row unreachable from this machine")
    assert COPY.is_file(), "repo copy missing while the live prompt exists"
    live = COPY.read_text(encoding="utf-8")
    assert live == db, (
        "drift-patrol prompt drifted from its repo copy: the DB prompt was "
        "amended without rerunning "
        "watch/inbox/burn_wave_20260926/B2_267_update_prompt.py (which "
        "rewrites configs/drift_patrol_prompt.txt from the DB)"
    )


def test_db_prompt_carries_touch_law_when_reachable():
    db = _db_prompt()
    if db is None:
        pytest.skip("tasks-index.sqlite or automation row unreachable from this machine")
    for marker in TOUCH_LAW_MARKERS:
        assert marker in db, f"live patrol prompt lacks touch-law clause: {marker!r}"
