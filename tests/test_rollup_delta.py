"""Rollup delta tests (hydrology Z17, 2026-09-29).

Covers the tools/rollup_delta.py contract in the test_gap_sentinel house
style: the pure delta core (window days, per-lane bytes/files/hot daily
deltas, appeared/gone semantics, unmetered dims from bytes-only sentinel
rows), the 5 GiB/day GROWTH bar and SHRINK deletion-event floor (boundaries
included), the short-window evidence-only law, the history union (own rich
rows first, sentinel bytes-only second, --bootstrap-from diff-only), the
emitted ROLLUP_DELTA.json the dashboard renders, snapshot dedupe, and the
real CLI exit codes (0 ok/baseline, 1 flags, 2 cannot-verify) through run()
over a synthetic mini-estate in tmp_path.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import rollup_delta as rd

GIB, MIB = rd.GIB, rd.MIB
NOW = datetime(2026, 9, 29, 20, 0, tzinfo=timezone.utc)


def write_estate(root: Path, ts: datetime,
                 lanes: dict[str, dict]) -> None:
    idx = root / "dashboard" / "static" / "index_data"
    idx.mkdir(parents=True, exist_ok=True)
    rollup = {}
    for name, lane in lanes.items():
        temps = {"HOT": lane.get("hot", 0), "WARM": lane.get("warm", 0)}
        rollup[name] = {"files": lane["files"], "bytes": lane["bytes"],
                        "newest": ts.isoformat(), "oldest": ts.isoformat(),
                        "temps": temps, "relations": {}}
    (idx / "rollup.json").write_text(json.dumps(rollup), encoding="utf-8")
    (idx / "last_run.json").write_text(
        json.dumps({"ts": ts.isoformat(),
                    "total_bytes": sum(l["bytes"] for l in lanes.values()),
                    "projects": {n: l["files"] for n, l in lanes.items()},
                    "newest_20": [], "skipped": 0, "seconds": 1.0}),
        encoding="utf-8")


def snap(ts: datetime, lanes: dict) -> dict:
    return {"ts": ts, "ts_raw": ts.isoformat(), "source": "test",
            "total_bytes": sum(v["bytes"] for v in lanes.values()), "lanes": lanes}


def run(root: Path, **kw) -> int:
    kw.setdefault("now", NOW)
    return rd.run(root, **kw)


def load_out(root: Path) -> dict:
    return json.loads((root / rd.OUT_RELPATH).read_text(encoding="utf-8"))


def by_lane(report: dict) -> dict:
    return {l["lane"]: l for l in report["lanes"]}


def test_pure_core_compute_delta() -> None:
    t0 = NOW - timedelta(days=2)
    prev = snap(t0, {"alpha": {"bytes": 10 * GIB, "files": 100, "hot": 10,
                               "warm": 5, "cold": 0, "frozen": 0}})
    # sentinel-shaped cur: bytes only, other dims None (never fabricated)
    cur = snap(NOW, {"alpha": {"bytes": 14 * GIB, "files": None, "hot": None,
                               "warm": None, "cold": None, "frozen": None},
                     "beta": {"bytes": 1 * GIB, "files": None, "hot": None,
                              "warm": None, "cold": None, "frozen": None}})
    d = rd.compute_delta(prev, cur)
    assert abs(d["days"] - 2.0) < 1e-9
    a = d["lanes"]["alpha"]
    assert a["bytes_delta"] == 4 * GIB and a["bytes_per_day"] == 2 * GIB
    assert a["files_delta"] is None and a["hot_per_day"] is None
    assert a["appeared"] is False and a["gone"] is False
    b = d["lanes"]["beta"]
    assert b["appeared"] is True and b["bytes_delta"] == 1 * GIB


def test_delta_from_fixture_rollups_flags_grow_and_shrink(tmp_path: Path, capsys) -> None:
    t0 = NOW - timedelta(days=1)
    write_estate(tmp_path, t0, {
        "alpha": {"files": 100, "bytes": 10 * GIB, "hot": 10},
        "beta": {"files": 50, "bytes": 5 * GIB, "hot": 2},
        "gamma": {"files": 80, "bytes": 8 * GIB, "hot": 4},
        "deadlane": {"files": 30, "bytes": 3 * GIB, "hot": 1},
    })
    assert run(tmp_path) == 0  # baseline
    history = (tmp_path / "logs" / "rollup_delta" / "history.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(history) == 1
    assert load_out(tmp_path)["status"] == "baseline"

    write_estate(tmp_path, NOW, {
        # +12 GiB/day over the 5 GiB/day bar; files +20, hot velocity +6/day
        "alpha": {"files": 120, "bytes": 22 * GIB, "hot": 16},
        # +0.1 GiB/day: evidence, under the bar
        "beta": {"files": 52, "bytes": 5 * GIB + int(0.1 * GIB), "hot": 2},
        # -2 GiB: deletion event; files -2, hot -1
        "gamma": {"files": 78, "bytes": 6 * GIB, "hot": 3},
        # deadlane vanishes: gone, full -3 GiB is one deletion event
        # epsilon appears at +6 GiB: 6 GiB/day over the bar
        "epsilon": {"files": 9, "bytes": 6 * GIB, "hot": 9},
    })
    assert run(tmp_path) == 1
    out = capsys.readouterr().out
    assert "ROLLUP-DELTA: FLAGS - 4 lane(s)" in out
    assert "GROWTH alpha" in out and "(12.00 GiB/day" in out
    assert "SHRINK gamma" in out and "SHRINK deadlane" in out
    assert "gone (absent from current snapshot)" in out

    report = load_out(tmp_path)
    assert report["status"] == "flags"
    assert report["window"]["days"] == 1.0
    assert report["window"]["source"] == "history"
    lanes = by_lane(report)
    a, g, dl, e = lanes["alpha"], lanes["gamma"], lanes["deadlane"], lanes["epsilon"]
    assert a["bytes_delta"] == 12 * GIB and a["bytes_per_day"] == 12 * GIB
    assert a["files_delta"] == 20 and a["hot_delta"] == 6 and a["hot_per_day"] == 6
    assert a["flags"] == ["GROWTH"]
    assert g["bytes_delta"] == -2 * GIB and g["flags"] == ["SHRINK"]
    assert dl["bytes_delta"] == -3 * GIB and dl["gone"] is True and dl["flags"] == ["SHRINK"]
    assert e["appeared"] is True and e["flags"] == ["GROWTH"]
    assert lanes["beta"]["flags"] == []
    assert report["top_growing"] == ["alpha", "epsilon", "beta"]
    assert report["top_shrinking"] == ["deadlane", "gamma"]  # most negative first
    assert report["totals"]["total_bytes_delta"] == sum(
        [12 * GIB, int(0.1 * GIB), -2 * GIB, -3 * GIB, 6 * GIB])
    assert (tmp_path / "logs" / "rollup_delta" / "history.jsonl").read_text(
        encoding="utf-8").count("\n") == 2


def test_bar_boundaries_strict_growth_inclusive_shrink(tmp_path: Path) -> None:
    t0 = NOW - timedelta(days=1)
    write_estate(tmp_path, t0, {
        "atedge": {"files": 1, "bytes": 5 * GIB},
        "shrinkfloor": {"files": 1, "bytes": 1 * MIB},
    })
    assert run(tmp_path) == 0  # baseline
    write_estate(tmp_path, NOW, {
        # exactly +5 GiB/day == bar: NOT flagged (strictly over, sentinel law)
        "atedge": {"files": 1, "bytes": 10 * GIB},
        # exactly -1 MiB == floor: flagged (at-or-past the deletion floor)
        "shrinkfloor": {"files": 1, "bytes": 0},
    })
    assert run(tmp_path) == 1
    report = load_out(tmp_path)
    lanes = by_lane(report)
    assert lanes["atedge"]["flags"] == []
    assert lanes["shrinkfloor"]["flags"] == ["SHRINK"]


def test_short_window_is_evidence_only(tmp_path: Path, capsys) -> None:
    write_estate(tmp_path, NOW - timedelta(hours=1),
                 {"alpha": {"files": 1, "bytes": 1 * GIB, "hot": 1}})
    assert run(tmp_path) == 0
    write_estate(tmp_path, NOW,
                 {"alpha": {"files": 1, "bytes": 20 * GIB, "hot": 1}})
    assert run(tmp_path) == 0  # 1h window: 456 GiB/day would flag, law holds
    assert "evidence only" in capsys.readouterr().out
    report = load_out(tmp_path)
    assert report["status"] == "evidence_only"
    assert report["flags"] == [] and report["window"]["evidence_only"] is True
    assert by_lane(report)["alpha"]["bytes_delta"] == 19 * GIB  # evidence kept


def test_sentinel_history_is_bytes_only_source(tmp_path: Path) -> None:
    sentinel = tmp_path / "logs" / "gap_sentinel" / "history.jsonl"
    sentinel.parent.mkdir(parents=True)
    t0 = NOW - timedelta(days=1)
    sentinel.write_text(json.dumps(
        {"ts": t0.isoformat(), "total_bytes": 10 * GIB,
         "projects": {"alpha": 10 * GIB}}) + "\n", encoding="utf-8")
    write_estate(tmp_path, NOW, {"alpha": {"files": 42, "bytes": 12 * GIB, "hot": 7}})
    assert run(tmp_path) == 0  # 2 GiB/day under the 5 GiB/day bar
    report = load_out(tmp_path)
    assert report["window"]["source"] == "sentinel"
    a = by_lane(report)["alpha"]
    assert a["bytes_delta"] == 2 * GIB and a["bytes_per_day"] == 2 * GIB
    assert a["files_delta"] is None and a["hot_delta"] is None
    assert report["unmetered_note"] is not None


def test_bootstrap_from_is_diff_only_never_recorded(tmp_path: Path) -> None:
    old_root = tmp_path / "old_deploy"
    t0 = NOW - timedelta(days=1)
    write_estate(old_root, t0, {"gamma": {"files": 80, "bytes": 8 * GIB, "hot": 4}})
    boot = old_root / "dashboard" / "static" / "index_data"

    write_estate(tmp_path, NOW, {"gamma": {"files": 78, "bytes": 6 * GIB, "hot": 3}})
    assert run(tmp_path, bootstrap=boot) == 1  # -2 GiB deletion event vs the old copy
    report = load_out(tmp_path)
    assert report["window"]["source"] == "bootstrap"
    assert by_lane(report)["gamma"]["flags"] == ["SHRINK"]
    history = (tmp_path / "logs" / "rollup_delta" / "history.jsonl").read_text(
        encoding="utf-8").splitlines()
    assert len(history) == 1  # only the CURRENT rollup run, never the bootstrap row
    assert json.loads(history[0])["ts"] == NOW.isoformat()


def test_missing_and_garbage_inputs_exit_2(tmp_path: Path, capsys) -> None:
    assert run(tmp_path) == 2
    assert "cannot verify" in capsys.readouterr().out
    idx = tmp_path / "dashboard" / "static" / "index_data"
    idx.mkdir(parents=True)
    (idx / "rollup.json").write_text("{not json", encoding="utf-8")
    (idx / "last_run.json").write_text("{}", encoding="utf-8")
    assert run(tmp_path) == 2


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    t0 = NOW - timedelta(days=1)
    write_estate(tmp_path, t0, {"alpha": {"files": 1, "bytes": 8 * GIB, "hot": 1}})
    assert run(tmp_path) == 0
    out_p = tmp_path / rd.OUT_RELPATH
    before = out_p.read_text(encoding="utf-8")  # baseline run already emitted it
    write_estate(tmp_path, NOW, {"alpha": {"files": 1, "bytes": 1 * GIB, "hot": 1}})
    assert run(tmp_path, dry_run=True) == 1
    assert out_p.read_text(encoding="utf-8") == before  # untouched by the dry run
    assert (tmp_path / "logs" / "rollup_delta" / "history.jsonl").read_text(
        encoding="utf-8").count("\n") == 1  # only the t0 baseline row


def test_cli_exit_codes(tmp_path: Path) -> None:
    write_estate(tmp_path, NOW - timedelta(days=1),
                 {"alpha": {"files": 1, "bytes": 1 * GIB, "hot": 1}})
    assert rd.main(["--root", str(tmp_path)]) == 0
