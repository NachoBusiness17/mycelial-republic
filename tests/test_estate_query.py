"""estate_query tests (IMP4, receipt watch/inbox/last_mile_20260930/IMP4_QUERY.md).

The three laws under test:
  CORR  — query --corr joins fixture rows across the AH14 writers
          (trajectory, gameflow, duel) into one timeline.
  PATH  — query --path is the legacy join: pre-AH14 rows without corr_id
          (an old step, a burn receipt) still surface when they mention a path.
  HONESTY — zero matches prints an explicit 0-rows line and fabricates
          nothing; the unfiltered dump is refused; bad JSONL lines are
          skipped and counted, never fatal.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import estate_query  # noqa: E402


def write_surfaces(root: Path) -> None:
    """Fixture estate: one AH14 corr (deadbeef) across three writers, plus
    pre-AH14 rows (no corr_id) that must only surface via path joins, plus
    one malformed line in the steps stream."""
    steps = [
        # pre-AH14 step (2026-09-28, no corr_id): legacy path-join only
        {"schema_version": "trajectory_step.v1", "step_hash": "a" * 16,
         "ts": "2026-09-28T10:00:00+00:00", "session_id": "s-old", "face": "bash",
         "command": "pytest tools/duel_harness.py -q",
         "result": {"exit": 0, "output_excerpt": "19 passed", "truncated": False}},
        # AH14 step carrying the lane corr_id
        {"schema_version": "trajectory_step.v1", "step_hash": "b" * 16,
         "ts": "2026-09-30T12:00:00+00:00", "session_id": "s-new",
         "corr_id": "deadbeef", "face": "bash",
         "command": "python tools/estate_query.py query --corr deadbeef",
         "result": {"exit": 0, "output_excerpt": "", "truncated": False}},
    ]
    burns = [  # burn receipt ledger: pre-AH14 shape, no corr_id field at all
        {"ts": "2026-09-29T08:00:00Z", "slug": "demo-burn", "verdict": "green",
         "fresh_failure_mode": False,
         "landing": "watch/inbox/BURN_demo_20260930.md",
         "one_line": "demo burn closed green with a landing receipt"},
    ]
    gameflow = [  # AH14 burns writer row, corr stamped at the _log choke point
        {"ts": "2026-09-30T12:05:00Z", "action": "test", "piece": "estate_query",
         "module": "tools/estate_query.py", "enqueued": True,
         "queue_id": "q1234abcd", "corr_id": "deadbeef"},
    ]
    duel = [  # duel ledger row, corr from MAG_CORR_ID (env wins over the mint)
        {"ask_id": "imp4-demo", "a_model": "z-ai/glm-5.3-prime",
         "b_model": "qwen/qwen3.8-max-prime", "a_cost": 0.03, "b_cost": 0.03,
         "judge": "fireworks/ember-1", "winner": "A",
         "rubric": ["evidence"], "ts": "2026-09-30T13:00:00+00:00",
         "corr_id": "deadbeef", "mode": "live", "swap": False,
         "judge_cost": 0.018, "criteria": [], "rationale": "A cited bytes.",
         "a_chars": 10, "b_chars": 10, "a_headers": 0, "b_headers": 0},
    ]
    files = {
        "memory/trajectory/steps.jsonl": steps,
        "memory/burns/LEDGER.jsonl": burns,
        "memory/game/FLOW_LEDGER.jsonl": gameflow,
        "logs/duel/duels.jsonl": duel,
    }
    for rel, rows in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            if rel.endswith("steps.jsonl"):
                f.write("this line is not json {\n")  # bad line: skipped, not fatal
            for row in rows:
                f.write(json.dumps(row) + "\n")


@pytest.fixture()
def estate(tmp_path: Path) -> Path:
    write_surfaces(tmp_path)
    return tmp_path


# --- CORR: the AH14 join -----------------------------------------------------


def test_corr_join_binds_the_three_writers(estate: Path) -> None:
    events, stats = estate_query.query(estate, corr="deadbeef")
    assert [e.surface for e in events] == ["trajectory", "gameflow", "duel"]
    # one merged timeline, oldest first, ts normalized to UTC
    assert [e.ts_raw[:10] for e in events] == ["2026-09-30"] * 3
    assert events[0].ts < events[1].ts < events[2].ts
    # kind + summary per surface
    assert (events[0].kind, "estate_query.py" in events[0].summary) == ("bash", True)
    assert (events[1].kind, "estate_query" in events[1].summary) == ("test", True)
    assert (events[2].kind, "imp4-demo" in events[2].summary) == ("duel", True)
    # the pre-AH14 step (no corr) and the corr-less burn receipt stay out
    assert stats["matched"] == {"trajectory": 1, "burns": 0, "gameflow": 1, "duel": 1}
    # bad line skipped and counted, honest read stats
    assert stats["skipped"]["trajectory"] == 1
    assert stats["read"]["trajectory"] == 2


def test_corr_join_is_case_insensitive_hex(estate: Path) -> None:
    events, _ = estate_query.query(estate, corr="DEADBEEF")
    assert len(events) == 3


# --- PATH: the legacy join ---------------------------------------------------


def test_path_join_surfaces_pre_corr_rows(estate: Path) -> None:
    events, _ = estate_query.query(estate, path="duel_harness.py")
    # the 2026-09-28 step has no corr_id; the path join still finds it
    assert [e.surface for e in events] == ["trajectory"]
    assert events[0].corr_id is None
    assert events[0].ts_raw.startswith("2026-09-28")


def test_path_join_reaches_the_burn_receipts_ledger(estate: Path) -> None:
    events, _ = estate_query.query(estate, path="BURN_demo_20260930")
    assert [e.surface for e in events] == ["burns"]
    assert events[0].kind == "verdict"
    assert "demo-burn" in events[0].summary and "green" in events[0].summary


def test_path_join_matches_the_row_text_case_insensitively(estate: Path) -> None:
    events, _ = estate_query.query(estate, path="TOOLS/ESTATE_QUERY.PY")
    surfaces = {e.surface for e in events}
    assert surfaces == {"trajectory", "gameflow"}  # step command + gameflow module


# --- since + model: the time-filtered rollup ---------------------------------


def test_since_model_rollup_per_surface(estate: Path) -> None:
    since = estate_query.parse_since("2026-09-30T00:00:00Z")
    events, stats = estate_query.query(estate, since=since, model="glm-5.3-prime")
    # only the duel row is both on/after the cutoff and model-matched
    assert [e.surface for e in events] == ["duel"]
    assert stats["matched"]["duel"] == 1
    assert "z-ai/glm-5.3-prime" in events[0].summary


def test_since_excludes_older_rows(estate: Path) -> None:
    events, _ = estate_query.query(estate, since=estate_query.parse_since("2026-09-29"))
    dates = {e.ts_raw[:10] for e in events}
    assert "2026-09-28" not in dates  # the pre-AH14 step drops out
    assert dates == {"2026-09-29", "2026-09-30"}


def test_since_date_only_means_midnight_utc(estate: Path) -> None:
    assert estate_query.parse_since("2026-09-30").hour == 0
    with pytest.raises(ValueError):
        estate_query.parse_since("yesterday")


# --- HONESTY: empty results, refused dumps, bad lines -------------------------


def test_empty_result_is_honest(estate: Path, capsys) -> None:
    events, stats = estate_query.query(estate, corr="00000000")
    assert events == []
    assert stats["matched"] == {"trajectory": 0, "burns": 0, "gameflow": 0, "duel": 0}
    code = estate_query.main(["query", "--corr", "00000000", "--root", str(estate)])
    out = capsys.readouterr().out
    assert code == 0  # an honest empty is a successful query, not an error
    assert "0 rows matched" in out
    assert "no fabricated rows" in out
    assert "timeline" not in out  # no timeline invented for an empty match


def test_unfiltered_dump_is_refused(estate: Path) -> None:
    with pytest.raises(SystemExit) as exc:
        estate_query.main(["query", "--root", str(estate)])
    assert exc.value.code == 2


def test_missing_surface_file_reads_as_empty(tmp_path: Path) -> None:
    events, stats = estate_query.query(tmp_path, corr="deadbeef")
    assert events == []
    assert stats["read"] == {"trajectory": 0, "burns": 0, "gameflow": 0, "duel": 0}


def test_bad_jsonl_lines_are_skipped_not_fatal(estate: Path, capsys) -> None:
    code = estate_query.main(["query", "--corr", "deadbeef", "--root", str(estate)])
    out = capsys.readouterr().out
    assert code == 0
    assert "bad lines skipped: 1" in out
    assert "3 rows matched" in out


# --- CLI end to end -----------------------------------------------------------


def test_cli_corr_join_prints_one_merged_timeline(estate: Path, capsys) -> None:
    code = estate_query.main(["query", "--corr", "deadbeef", "--root", str(estate)])
    out = capsys.readouterr().out
    assert code == 0
    assert "rollup: trajectory 1 | gameflow 1 | duel 1" in out
    assert "timeline (oldest first):" in out
    lines = [l for l in out.splitlines() if l.startswith("2026-09-30T")]
    assert len(lines) == 3
    assert lines[0].startswith("2026-09-30T12:00:00Z  trajectory bash")
    assert lines[2].startswith("2026-09-30T13:00:00Z  duel       duel")
    assert "imp4-demo" in lines[2]


def test_cli_limit_reports_hidden_rows(estate: Path, capsys) -> None:
    estate_query.main(["query", "--corr", "deadbeef", "--root", str(estate),
                       "--limit", "2"])
    out = capsys.readouterr().out
    assert "+1 more rows (raise --limit" in out
