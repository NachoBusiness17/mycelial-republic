"""Gap gauges tests (lamplighter, 2026-10-06).

Covers the tools/gap_gauges.py contract in the test_gap_sentinel house style:
the grow/shrink diff over sentinel history byte rows (GROW over the 1 GiB/day
bar, SHRINK past the deletion floor, the blind spot that let the -123.34 GiB
window of 2026-10-04 -> 10-05 pass with no instrument flagging it), the B2-215
evidence-only short window, the rot gauge against a synthetic ORPHAN_CENSUS.json
(ROT when never_consumed grows past the bar while consumed stays flat, baseline
on first run with no prior gauge row, CENSUS-DARK when the artifact is absent),
the KPI tail truth (KPI-DARK on stale mtime, no full-file slurp), the sensor
watchlist (SENSOR-DARK / SENSOR-MISSING), fail-closed exit 2 on a garbage
sentinel history row, and dry-run writing nothing.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import gap_gauges as gg

NOW = datetime(2026, 10, 6, 12, 0, tzinfo=timezone.utc)
GIB = gg.GIB

SENSORS = gg.SENSORS


def make_estate(root: Path) -> None:
    """Fresh synthetic estate: two sentinel snapshots 1 day apart with a small
    clean delta, a fresh census, and every watched sensor mtime-fresh."""
    t0 = NOW - timedelta(days=1)
    t1 = NOW
    root.joinpath("logs/gap_sentinel").mkdir(parents=True, exist_ok=True)
    rows = [
        {"ts": t0.isoformat(), "total_bytes": 100 * GIB,
         "projects": {"a": 60 * GIB, "b": 40 * GIB}},
        {"ts": t1.isoformat(), "total_bytes": 100 * GIB + 10 * GIB // 16,
         "projects": {"a": 60 * GIB, "b": 40 * GIB + 10 * GIB // 16}},
    ]
    with root.joinpath("logs/gap_sentinel/history.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    write_census(root, 100, ["x", "y", "z"])
    root.joinpath("logs").mkdir(exist_ok=True)
    kpi_p = root / "logs/kpi.jsonl"
    kpi_p.write_text(json.dumps({"schema": "mag_records_kpi.v1", "ts": t1.isoformat(),
                                 "source": "summarize"}) + "\n", encoding="utf-8")
    root.joinpath("dashboard/static/index_data").mkdir(parents=True, exist_ok=True)
    root.joinpath("dashboard/static").mkdir(exist_ok=True)
    for rel in SENSORS:
        p = root / rel
        p.write_text("{}", encoding="utf-8")
        stamp = NOW.timestamp()
        os.utime(p, (stamp, stamp))
    # the census artifact is on the SENSORS watchlist since 2026-10-09: the loop
    # above overwrote it with "{}", so restore the real census body (the helper
    # pins its mtime at NOW).
    write_census(root, 100, ["x", "y", "z"])


def write_census(root: Path, never_consumed: int, consumed: list[str]) -> None:
    p = root / gg.CENSUS_RELPATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({
        "generated_at": NOW.isoformat(),
        "counts": {"never_registered": 1, "registered_missing": 0,
                   "registered_never_consumed": never_consumed},
        "consumed": consumed,
    }), encoding="utf-8")
    # the census is a watched sensor since 2026-10-09: a real wall-clock write
    # stamp would read as a negative age against the frozen NOW (SENSOR-DARK).
    stamp = NOW.timestamp()
    os.utime(p, (stamp, stamp))


def seed_gauge_history(root: Path, never_consumed: int, consumed_total: int) -> None:
    p = root / gg.HISTORY_RELPATH
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": (NOW - timedelta(days=7)).isoformat(),
                             "census_never_consumed": never_consumed,
                             "census_consumed_total": consumed_total}) + "\n")


def fresh_mtime(root: Path, rel: str) -> None:
    stamp = NOW.timestamp()
    os.utime(root / rel, (stamp, stamp))


def test_grow_flag_over_bar(tmp_path, capsys):
    make_estate(tmp_path)
    # total delta +10/16 GiB over exactly 1d = 0.625 GiB/day... over the 1.0 bar
    # needs a bigger delta: rewrite the second snapshot to +2 GiB.
    h = tmp_path / "logs/gap_sentinel/history.jsonl"
    rows = h.read_text(encoding="utf-8").splitlines()
    cur = json.loads(rows[1])
    cur["total_bytes"] = 100 * GIB + 2 * GIB
    cur["projects"]["b"] = 40 * GIB + 2 * GIB
    rows[1] = json.dumps(cur)
    h.write_text("\n".join(rows) + "\n", encoding="utf-8")
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 1
    assert "GROW total" in out


def test_shrink_flag_past_floor(tmp_path, capsys):
    make_estate(tmp_path)
    h = tmp_path / "logs/gap_sentinel/history.jsonl"
    rows = h.read_text(encoding="utf-8").splitlines()
    cur = json.loads(rows[1])
    cur["total_bytes"] = 100 * GIB - 2 * GIB
    cur["projects"]["b"] = 40 * GIB - 2 * GIB
    rows[1] = json.dumps(cur)
    h.write_text("\n".join(rows) + "\n", encoding="utf-8")
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 1
    assert "SHRINK total" in out


def test_evidence_only_short_window(tmp_path, capsys):
    make_estate(tmp_path)
    h = tmp_path / "logs/gap_sentinel/history.jsonl"
    rows = h.read_text(encoding="utf-8").splitlines()
    prev = json.loads(rows[0])
    prev["ts"] = (NOW - timedelta(days=0.1)).isoformat()
    rows[0] = json.dumps(prev)
    h.write_text("\n".join(rows) + "\n", encoding="utf-8")
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 0
    assert "evidence only" in out


def test_rot_flag_when_consumed_flat(tmp_path, capsys):
    make_estate(tmp_path)
    seed_gauge_history(tmp_path, 2207, 3)
    write_census(tmp_path, 3381, ["x", "y", "z"])  # +1174, consumed flat at 3
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 1
    assert "ROT never_consumed 2207 -> 3381" in out


def test_rot_clean_when_consumption_moved(tmp_path, capsys):
    make_estate(tmp_path)
    seed_gauge_history(tmp_path, 2207, 3)
    write_census(tmp_path, 3381, ["x", "y", "z", "w"])  # grew but consumed +1
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 0
    assert "consumption moved" in out


def test_rot_baseline_first_run(tmp_path, capsys):
    make_estate(tmp_path)
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 0
    assert "rot baseline" in out


def test_census_dark(tmp_path, capsys):
    make_estate(tmp_path)
    (tmp_path / gg.CENSUS_RELPATH).unlink()
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 1
    assert "CENSUS-DARK" in out


def test_kpi_dark_on_stale_mtime(tmp_path, capsys):
    make_estate(tmp_path)
    stamp = (NOW - timedelta(days=3)).timestamp()
    os.utime(tmp_path / "logs/kpi.jsonl", (stamp, stamp))
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 1
    assert "KPI-DARK" in out


def test_sensor_dark_and_missing(tmp_path, capsys):
    make_estate(tmp_path)
    stamp = (NOW - timedelta(days=3)).timestamp()
    os.utime(tmp_path / "dashboard/static/x_radar.json", (stamp, stamp))
    (tmp_path / "dashboard/static/index_data/rollup.json").unlink()
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 1
    assert "SENSOR-DARK dashboard/static/x_radar.json" in out
    assert "SENSOR-MISSING dashboard/static/index_data/rollup.json" in out


def test_census_sensor_stale(tmp_path, capsys):
    """The 2026-10-09 hole: the rot input went 3.0d stale while present, and
    CENSUS-DARK only sees absence. The watchlist row must see staleness."""
    make_estate(tmp_path)
    stamp = (NOW - timedelta(days=3)).timestamp()
    os.utime(tmp_path / gg.CENSUS_RELPATH, (stamp, stamp))
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 1
    assert "SENSOR-DARK watch/inbox/ORPHAN_CENSUS.json" in out


def test_exit2_on_garbage_sentinel_row(tmp_path, capsys):
    make_estate(tmp_path)
    h = tmp_path / "logs/gap_sentinel/history.jsonl"
    h.write_text(h.read_text(encoding="utf-8") + "not-json\n", encoding="utf-8")
    rc = gg.run(tmp_path, now=NOW)
    out = capsys.readouterr().out
    assert rc == 2
    assert "cannot verify" in out


def test_dry_run_writes_nothing(tmp_path, capsys):
    make_estate(tmp_path)
    rc = gg.run(tmp_path, dry_run=True, now=NOW)
    assert rc == 0
    assert not (tmp_path / "logs/gap_gauges/history.jsonl").exists()
    assert not (tmp_path / "logs/gap_gauges/run.log").exists()
