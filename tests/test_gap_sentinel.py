"""Gap sentinel tests (Mickey17 wave 3, 2026-09-29).

Covers the tools/gap_sentinel.py contract in the test_census_drift_patrol house
style: the pure growth core (window days, bytes/day, bar flags), the short-window
evidence-only law, sensor silence by mtime with the embedded-date preference,
idempotent alerting (one attention.md block and one alerted.jsonl row per key
across repeated runs), snapshot dedupe on the rollup run ts, and the real CLI
exit codes (0 ok/baseline, 1 gap, 2 cannot-verify) through run() over a
synthetic mini-estate in tmp_path.
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

import gap_sentinel as gs

GIB = gs.GIB
NOW = datetime(2026, 9, 29, 20, 0, tzinfo=timezone.utc)


def write_estate(root: Path, ts: datetime, projects: dict[str, int],
                 total_bytes: int | None = None, radar: dict | None = None) -> None:
    idx = root / "dashboard" / "static" / "index_data"
    idx.mkdir(parents=True, exist_ok=True)
    (idx / "rollup.json").write_text(
        json.dumps({name: {"files": 1, "bytes": b, "newest": ts.isoformat(),
                           "oldest": ts.isoformat(), "temps": {}, "relations": {}}
                    for name, b in projects.items()}),
        encoding="utf-8")
    (idx / "last_run.json").write_text(
        json.dumps({"ts": ts.isoformat(), "total_bytes": total_bytes or sum(projects.values()),
                    "projects": {n: 1 for n in projects}, "newest_20": [], "skipped": 0,
                    "seconds": 1.0}),
        encoding="utf-8")
    static = root / "dashboard" / "static"
    static.mkdir(parents=True, exist_ok=True)
    if radar is not None:
        radar_path = static / "x_radar.json"
        radar_path.write_text(json.dumps(radar), encoding="utf-8")
        # Stamp mtime to the TEST clock: the real wall clock can run past NOW,
        # which would read as a future stamp (fabrication smell) and false-flag.
        just_written = NOW.timestamp()
        os.utime(radar_path, (just_written, just_written))


def fresh_radar() -> dict:
    return {"threads": [], "leaderboard": [], "patterns": []}


def run(root: Path, **kw) -> int:
    kw.setdefault("now", NOW)
    return gs.run(root, **kw)


def test_growth_computed_from_fixture_rollups(tmp_path: Path, capsys) -> None:
    t0 = NOW - timedelta(days=1)
    write_estate(tmp_path, t0, {"alpha": 10 * GIB, "beta": 5 * GIB}, radar=fresh_radar())
    assert run(tmp_path) == 0  # baseline: no prior snapshot to diff
    history = (tmp_path / "logs" / "gap_sentinel" / "history.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(history) == 1

    # Pure core: 1.0d window, alpha +2 GiB/day over the 1 GiB bar, beta under it.
    prev = {"ts_dt": t0, "total_bytes": 15 * GIB,
            "projects": {"alpha": 10 * GIB, "beta": 5 * GIB}}
    cur = {"ts_dt": NOW, "total_bytes": 17 * GIB + int(0.1 * GIB),
           "projects": {"alpha": 12 * GIB, "beta": 5 * GIB + int(0.1 * GIB)}}
    growth = gs.compute_growth(prev, cur)
    assert abs(growth["days"] - 1.0) < 1e-9
    by_name = {r["project"]: r for r in growth["rows"]}
    assert by_name["alpha"]["bytes_per_day"] == 2 * GIB
    flags = gs.growth_flags(growth, 1.0 * GIB)
    assert [r["project"] for r in flags] == ["alpha"]

    write_estate(tmp_path, NOW, {"alpha": 12 * GIB, "beta": 5 * GIB + int(0.1 * GIB)},
                 radar=fresh_radar())
    assert run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "GAP-SENTINEL: GROWTH - 1 project(s) over 1.00 GiB/day bar" in out
    assert "alpha 2.00 GiB (2.00 GiB/day)" in out
    assert "beta" not in out.split("bar in", 1)[1]
    history = (tmp_path / "logs" / "gap_sentinel" / "history.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(history) == 2
    attention = (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")
    assert "### Gap sentinel fired (" in attention
    assert "GAP-SENTINEL: GROWTH" in attention


def test_short_window_is_evidence_only(tmp_path: Path, capsys) -> None:
    t0 = NOW - timedelta(hours=1)
    write_estate(tmp_path, t0, {"alpha": 1 * GIB}, radar=fresh_radar())
    assert run(tmp_path) == 0
    write_estate(tmp_path, NOW, {"alpha": 20 * GIB}, radar=fresh_radar())
    assert run(tmp_path) == 0  # 1h window: 456 GiB/day would flag, evidence-only law holds
    assert "evidence only" in capsys.readouterr().out


def test_stale_sensor_detected_by_mtime(tmp_path: Path, capsys) -> None:
    stale = NOW - timedelta(days=3)
    write_estate(tmp_path, NOW - timedelta(days=4), {"alpha": 1 * GIB}, radar=fresh_radar())
    radar_path = tmp_path / "dashboard" / "static" / "x_radar.json"
    stamp = stale.timestamp()
    os.utime(radar_path, (stamp, stamp))
    assert run(tmp_path, silence_days=2.0) == 1
    out = capsys.readouterr().out
    assert "GAP-SENTINEL: SENSOR-SILENCE - dashboard/static/x_radar.json dark 3.00d" in out
    assert "source mtime" in out  # no embedded date field: mtime is the stated truth


def test_sensor_embedded_date_beats_mtime(tmp_path: Path, capsys) -> None:
    write_estate(tmp_path, NOW - timedelta(days=4), {"alpha": 1 * GIB},
                 radar={"ts": NOW.isoformat(), "threads": []})
    radar_path = tmp_path / "dashboard" / "static" / "x_radar.json"
    stamp = (NOW - timedelta(days=5)).timestamp()
    os.utime(radar_path, (stamp, stamp))
    assert run(tmp_path, silence_days=2.0) == 0
    assert "field:ts age 0.00d" in capsys.readouterr().out


def test_missing_sensor_flags(tmp_path: Path, capsys) -> None:
    write_estate(tmp_path, NOW - timedelta(days=4), {"alpha": 1 * GIB})  # no radar file
    assert run(tmp_path, silence_days=2.0) == 1
    assert "GAP-SENTINEL: SENSOR-MISSING - dashboard/static/x_radar.json absent" \
        in capsys.readouterr().out


def test_idempotent_alerting(tmp_path: Path, capsys) -> None:
    write_estate(tmp_path, NOW - timedelta(days=4), {"alpha": 1 * GIB}, radar=fresh_radar())
    radar_path = tmp_path / "dashboard" / "static" / "x_radar.json"
    stamp = (NOW - timedelta(days=3)).timestamp()
    os.utime(radar_path, (stamp, stamp))
    assert run(tmp_path, silence_days=2.0) == 1
    assert run(tmp_path, silence_days=2.0) == 1  # persistent gap stays exit 1
    out = capsys.readouterr().out
    assert "alert filed" in out
    assert "already on file, not duplicated" in out
    attention = (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")
    assert attention.count("### Gap sentinel fired (") == 1
    assert attention.count("- key: sensor-silence dashboard/static/x_radar.json") == 1
    alerted = (tmp_path / "logs" / "gap_sentinel" / "alerted.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(alerted) == 1

    # The sensor heals and goes dark again at a NEW origin stamp: new key, new block.
    stamp2 = (NOW - timedelta(days=2.5)).timestamp()
    os.utime(radar_path, (stamp2, stamp2))
    assert run(tmp_path, silence_days=2.0) == 1
    attention = (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")
    assert attention.count("### Gap sentinel fired (") == 2


def test_attention_survivor_heals_alerted_ledger(tmp_path: Path) -> None:
    write_estate(tmp_path, NOW - timedelta(days=4), {"alpha": 1 * GIB}, radar=fresh_radar())
    radar_path = tmp_path / "dashboard" / "static" / "x_radar.json"
    stamp = (NOW - timedelta(days=3)).timestamp()
    os.utime(radar_path, (stamp, stamp))
    assert run(tmp_path, silence_days=2.0) == 1
    alerted_p = tmp_path / "logs" / "gap_sentinel" / "alerted.jsonl"
    alerted_p.write_text("", encoding="utf-8")  # jsonl lost, attention block survives
    assert run(tmp_path, silence_days=2.0) == 1
    attention = (tmp_path / "memory" / "attention.md").read_text(encoding="utf-8")
    assert attention.count("### Gap sentinel fired (") == 1  # no double-file
    healed = [json.loads(x) for x in alerted_p.read_text(encoding="utf-8").splitlines()]
    assert healed and healed[0].get("healed") is True


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    write_estate(tmp_path, NOW - timedelta(days=4), {"alpha": 1 * GIB}, radar=fresh_radar())
    assert gs.run(tmp_path, dry_run=True, now=NOW) == 0
    assert not (tmp_path / "logs" / "gap_sentinel" / "history.jsonl").exists()
    assert not (tmp_path / "memory").exists()


def test_missing_inputs_exit_2(tmp_path: Path, capsys) -> None:
    assert gs.run(tmp_path, now=NOW) == 2
    assert "cannot verify" in capsys.readouterr().out


def test_cli_exit_codes(tmp_path: Path) -> None:
    write_estate(tmp_path, NOW - timedelta(days=4), {"alpha": 1 * GIB}, radar=fresh_radar())
    rc = gs.main(["--root", str(tmp_path), "--silence-days", "2"])
    assert rc == 0
