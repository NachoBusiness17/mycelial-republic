"""Freshness disclosure pins (B2-104, 2026-09-26): mag/catalog_freshness.py.

The read-side verdict: a missing manifest can never read fresh (asof falls
back to the map file mtime); the manifest snapshot wins over the file mtime;
a corrupt snapshot_ts falls back rather than crashing; the 48h budget is
readable from the manifest.
"""
from __future__ import annotations

import datetime

import mag.catalog_freshness as cf


NOW = datetime.datetime(2026, 9, 26, 12, 0, 0, tzinfo=datetime.timezone.utc)


def _iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def test_missing_manifest_never_reads_fresh():
    map_mt = NOW - datetime.timedelta(hours=1)
    v = cf.manifest_freshness(None, NOW, map_mt)
    assert v["map_asof"] == _iso(map_mt)
    assert v["map_stale"] is False  # 1h old is inside the 48h budget
    old = cf.manifest_freshness(None, NOW, NOW - datetime.timedelta(hours=49))
    assert old["map_stale"] is True


def test_manifest_snapshot_decides_and_corrupt_falls_back():
    fresh_m = {"snapshot_ts": _iso(NOW - datetime.timedelta(hours=2))}
    v = cf.manifest_freshness(fresh_m, NOW, NOW - datetime.timedelta(hours=200))
    assert v["map_stale"] is False  # manifest wins over the old map file mtime
    assert v["map_asof"] == fresh_m["snapshot_ts"]
    bad = {"snapshot_ts": "not-a-date"}
    v2 = cf.manifest_freshness(bad, NOW, NOW - datetime.timedelta(hours=200))
    assert v2["map_stale"] is True   # corrupt stamp falls back to map mtime
    assert v2["map_asof"] == _iso(NOW - datetime.timedelta(hours=200))


def test_budget_is_readable_from_manifest():
    m = {"snapshot_ts": _iso(NOW - datetime.timedelta(hours=50)),
         "staleness_budget_hours": 72}
    v = cf.manifest_freshness(m, NOW, NOW)
    assert v["map_stale"] is False  # 50h stale only against a 72h budget
    assert v["staleness_budget_hours"] == 72
