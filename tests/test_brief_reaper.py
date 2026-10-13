"""Tests for tools/brief_reaper.py (Mickey17 W1, 2026-09-29).

Covers: fixture board parsing, queue-row schema match against a real
stealth_work_queue.jsonl row, idempotency (second run adds nothing),
dedupe against ids already armed in the queue, dry-run no-write, and
the live FREE_LANE_BRIEFS.md board parsing. Em-dash law: the board's
header separator is built with chr(0x2014) so this file stays clean.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from tools import brief_reaper

EM = chr(0x2014)  # separator used by the live board's brief headers

REPO_ROOT = Path(__file__).resolve().parents[1]
LIVE_QUEUE = REPO_ROOT / "state" / "fuel" / "stealth_work_queue.jsonl"
LIVE_BOARD = (REPO_ROOT / "watch" / "inbox" /
              "game_platform_basecamp_20260929" / "FREE_LANE_BRIEFS.md")


def _board_text() -> str:
    return (
        "# TEST BRIEFS BOARD\n\n"
        "Capsule line one.\nCapsule line two.\n\n"
        f"## BRIEF FL-1 {EM} First title\n"
        "Body of the first brief.\nSecond line.\n\n"
        f"## BRIEF FL-2 {EM} Second title\n"
        "Body of the second brief.\n"
    )


def _make_board(tmp_path: Path) -> Path:
    root = tmp_path / "watch" / "inbox"
    root.mkdir(parents=True)
    board = root / "TEST_BRIEFS.md"
    board.write_text(_board_text(), encoding="utf-8")
    return root


def _read_rows(queue: Path) -> list[dict]:
    return [json.loads(l) for l in
            queue.read_text(encoding="utf-8").splitlines() if l.strip()]


def test_parse_fixture_board(tmp_path):
    root = _make_board(tmp_path)
    boards = brief_reaper.discover_boards(root)
    assert len(boards) == 1
    parsed = brief_reaper.parse_board(boards[0])
    assert "Capsule line one." in parsed["preamble"]
    assert [b["id"] for b in parsed["briefs"]] == ["FL-1", "FL-2"]
    assert parsed["briefs"][0]["title"] == "First title"
    assert "Body of the first brief." in parsed["briefs"][0]["body"]
    assert "Second line." in parsed["briefs"][0]["body"]
    # the ask capsule inheritance: preamble must not leak into bodies
    assert "Capsule" not in parsed["briefs"][1]["body"]


def test_row_schema_matches_real_row(tmp_path):
    root = _make_board(tmp_path)
    queue = tmp_path / "stealth_work_queue.jsonl"
    census = brief_reaper.reap(root, queue)
    assert census["new"] == 2
    rows = _read_rows(queue)
    # every promised key present, driver-required subset exact
    for key in brief_reaper.ROW_KEYS:
        assert all(key in r for r in rows), f"missing key {key}"
    for r in rows:
        assert r["tier"] == "free"
        assert r["status"] == "queued"
        assert r["depth"] == 0
        assert r["parent_id"] is None
        assert "done_ts" not in r  # driver _next_work picks it up
        assert "Capsule line one." in r["ask"]  # capsule inherited
        assert f"BRIEF {r['id']}:" in r["ask"]
    # ask must contain the brief body so the row is self-contained
    assert "Body of the second brief." in rows[1]["ask"]
    # the driver's _next_work contract: selectable + readable fields
    first_open = next(r for r in rows if not r.get("done_ts"))
    assert first_open["ask"] and first_open["id"]

    # schema match against a REAL queued row from the live queue, when
    # present: every real key except the selffeed-only stamp must exist
    # on reaper rows (selffed_ts is selffeed provenance, operator
    # property per stealth_driver.py ~line 1034; impfeed rows omit it).
    if LIVE_QUEUE.is_file():
        real = None
        for r in _read_rows(LIVE_QUEUE):
            if r.get("status") == "queued":
                real = r  # keep the last queued-shape row seen
        if real is not None:
            missing = set(real) - {"selffed_ts"} - set(rows[0])
            assert not missing, f"real-row keys absent from reaper rows: {missing}"


def test_idempotency_second_run_adds_nothing(tmp_path):
    root = _make_board(tmp_path)
    queue = tmp_path / "stealth_work_queue.jsonl"
    first = brief_reaper.reap(root, queue)
    assert first["new"] == 2
    second = brief_reaper.reap(root, queue)
    assert second["new"] == 0
    assert second["appended"] == []
    assert second["armed"] == 2
    assert len(_read_rows(queue)) == 2  # nothing appended twice


def test_dedupe_skips_ids_already_in_queue(tmp_path):
    root = _make_board(tmp_path)
    queue = tmp_path / "stealth_work_queue.jsonl"
    # FL-1 already fired and done: dedupe must hold across lifecycle
    queue.write_text(json.dumps({
        "id": "FL-1", "ask": "old ask", "tier": "free",
        "status": "sensed", "queued_ts": "2026-09-29T00:00:00+00:00",
        "done_ts": "2026-09-29T01:00:00+00:00",
    }) + "\n", encoding="utf-8")
    census = brief_reaper.reap(root, queue)
    assert census["appended"] == ["FL-2"]
    assert census["armed"] == 1
    rows = _read_rows(queue)
    assert len(rows) == 2
    assert rows[0]["ask"] == "old ask"  # existing row untouched


def test_dry_run_writes_nothing(tmp_path):
    root = _make_board(tmp_path)
    queue = tmp_path / "stealth_work_queue.jsonl"
    census = brief_reaper.reap(root, queue, dry=True)
    assert census["dry"] is True
    assert census["new"] == 2
    assert not queue.exists()  # dry never creates or appends


def test_census_counts_boards_and_briefs(tmp_path):
    root = _make_board(tmp_path)
    # a second board in a nested dir must be discovered too
    nested = root / "sub"
    nested.mkdir()
    (nested / "MORE_BRIEFS.md").write_text(
        f"## BRIEF FL-9 {EM} Nested title\nNested body.\n",
        encoding="utf-8")
    queue = tmp_path / "q.jsonl"
    census = brief_reaper.reap(root, queue)
    assert census["boards"] == 2
    assert census["briefs"] == 3
    assert census["new"] == 3
    assert census["rows_in_queue"] == 3


@pytest.mark.skipif(not LIVE_BOARD.is_file(), reason="live board absent")
def test_live_free_lane_board_parses():
    parsed = brief_reaper.parse_board(LIVE_BOARD)
    ids = [b["id"] for b in parsed["briefs"]]
    assert len(ids) == 10, f"expected 10 FL briefs, saw {ids}"
    assert all(re.fullmatch(r"FL-\d+", i) for i in ids)
    # every brief must carry a real body and the shared capsule
    assert all(b["body"].strip() for b in parsed["briefs"])
    assert "Context capsule" in parsed["preamble"]
