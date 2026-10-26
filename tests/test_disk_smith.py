"""disk_smith tests (disk-crisis-20261008, the 1.3TB-in-36h incident).

The Smith chart must attribute growth without ever writing to the disk it
measures beyond its own ledger. These pins cover the pure functions: delta
math, alert rules, history shape, and the v1.1 projection/movers upgrade.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from tools.disk_smith import alerts, delta, projection, snap, top_movers


def _rows(spec: list[tuple[float, float]]) -> list[dict]:
    """(hours_ago, free_gb) -> ledger rows, oldest first."""
    now = datetime(2026, 10, 10, 6, 0, tzinfo=timezone.utc)
    return [
        {"ts": (now - timedelta(hours=h)).isoformat().replace("+00:00", "Z"),
         "free_gb": f}
        for h, f in spec
    ]


def _row(free=95.0, vhdx=132.0, page=132.9):
    return {
        "ts": "2026-10-08T21:00:00Z",
        "monsters": {"pagefile": page, "hiberfil": 25.6,
                     "docker_data_vhdx": vhdx, "wsl_ext4": 9.8},
        "seats": {"ollama_garden": 66.0, "hf_cache": 66.0},
        "estate": {"repo_logs": 11.6},
        "free_gb": free,
        "total_gb": 1862.0,
    }


def test_delta_reports_grown_and_shrunk():
    prev = _row(free=6.1, vhdx=100.0, page=32.0)
    prev["seats"]["ollama_garden"] = 162.0
    curr = _row()
    d = delta(curr, prev)
    assert d["monsters"]["docker_data_vhdx"] == 32.0
    assert d["monsters"]["pagefile"] == 100.9
    assert d["seats"]["ollama_garden"] == -96.0
    assert d["free_gb"] == 88.9


def test_delta_empty_without_previous():
    assert delta(_row(), None) == {}


def test_delta_ignores_sub_threshold_and_missing():
    prev = _row()
    prev["seats"]["hf_cache"] = None  # new home appeared since
    curr = _row()
    curr["estate"]["repo_logs"] = 11.604  # diffs to 0.004, rounds under threshold
    d = delta(curr, prev)
    assert "estate" not in d
    assert "hf_cache" not in d.get("seats", {})


def test_alerts_free_below_floor():
    fired = alerts(_row(free=6.1), floor_gb=15.0)
    assert any("DISK FLOOR" in a for a in fired)


def test_alerts_quiet_when_healthy():
    row = _row(free=95.0, vhdx=40.0, page=32.0)
    assert alerts(row, floor_gb=15.0) == []


def test_alerts_vhdx_bloat_and_pagefile_balloon():
    fired = alerts(_row(vhdx=132.0, page=132.9), floor_gb=15.0)
    assert any("VHDX BLOAT" in a for a in fired)
    assert any("PAGEFILE BALLOON" in a for a in fired)


def test_snap_shape_live():
    row = snap_now = snap.__wrapped__ if hasattr(snap, "__wrapped__") else None
    import datetime as dt
    r = snap(dt.datetime.now(dt.timezone.utc))
    assert r["free_gb"] > 0
    assert r["total_gb"] >= r["free_gb"]
    assert "docker_data_vhdx" in r["monsters"]
    assert "ollama_garden" in r["seats"]
    assert r["ts"].endswith("Z")


# ---- v1.1: projection + movers (the chart that does useful stuff) ----

def test_projection_exact_linear_burn():
    # -10GB per hour for 5 hours = 240GB/day; 95GB free, floor 15 -> 1/3 day.
    rows = _rows([(20, 195.0), (15, 145.0), (10, 95.0), (5, 45.0), (0, 95.0 - 0)])
    rows[-1]["free_gb"] = 45.0 - 50.0  # keep the same slope into now
    rows = _rows([(20, 195.0), (15, 145.0), (10, 95.0), (5, 45.0)])
    p = projection(rows, 15.0)
    assert p["eta_class"] == "trending"
    assert abs(p["median_daily_delta_gb"] - 240.0) < 0.5
    assert 0.0 < p["eta_days"] < 0.3


def test_projection_unstable_refuses_eta():
    # Free space whipsaws: the IQR dwarfs the median; no ETA may be offered.
    rows = _rows([(24, 100.0), (18, 10.0), (12, 190.0), (6, 60.0), (0, 120.0)])
    p = projection(rows, 15.0)
    assert p["eta_days"] is None
    assert p["eta_class"] == "unstable"


def test_projection_gaining_space():
    rows = _rows([(24, 40.0), (12, 60.0), (0, 80.0)])
    p = projection(rows, 15.0)
    assert p["eta_days"] is None
    assert p["eta_class"] == "gaining-space"


def test_projection_needs_three_rows():
    assert projection(_rows([(2, 50.0), (0, 40.0)]), 15.0)["eta_class"] == "insufficient-history"


def test_eta_alert_fires_inside_fourteen_days():
    rows = _rows([(24, 95.0), (12, 70.0), (0, 45.0)])  # 50GB/day, 30GB above floor
    p = projection(rows, 15.0)
    fired = alerts({"free_gb": 45.0, "total_gb": 1862.0}, 15.0, p)
    assert any("DISK ETA" in a for a in fired)


def test_eta_alert_quiet_when_healthy():
    rows = _rows([(24, 900.0), (12, 899.0), (0, 898.0)])  # 2GB/day, ~441 days out
    p = projection(rows, 15.0)
    row = {"free_gb": 898.0, "total_gb": 1862.0, "monsters": {}}
    assert alerts(row, 15.0, p) == []


def test_top_movers_ranks_by_absolute_gb():
    chg = {
        "monsters": {"pagefile": 3.0, "docker_data_vhdx": 12.5},
        "seats": {"zcode_cache": -20.0},
        "estate": {},
        "free_gb": 4.5,
    }
    movers = top_movers(chg)
    assert movers[0] == ("seats.zcode_cache", -20.0)
    assert movers[1] == ("monsters.docker_data_vhdx", 12.5)
    assert all(not k.startswith("free_gb") for k, _ in movers)
