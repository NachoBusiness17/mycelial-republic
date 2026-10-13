"""Disk-free floor check (disk-crisis-20261008).

Founding incident: C: at 6.1GB free / 100 percent on 2026-10-08 with ledgers
live; the patrol was blind to disk exhaustion (receipt
watch/inbox/DISK_INVENTORY_20261008.md). These tests pin the pure floor
function: breach fires, healthy volume stays quiet, absent config disables.
"""
from __future__ import annotations

from tools.longrunner_patrol import disk_floor_rows


def _policy(floor_gb, paths=(".",)):
    return {
        "disk_free_floor_gb": {
            "floor_gb": floor_gb,
            "watch_paths": list(paths),
        }
    }


def test_floor_breach_fires_on_impossible_floor():
    # 999999GB floor can never be met on real hardware: the breach path must
    # fire and carry free/floor/total for the alert line.
    rows = disk_floor_rows(_policy(999999))
    assert len(rows) == 1
    row = rows[0]
    assert row["floor_gb"] == 999999.0
    assert row["free_gb"] > 0
    assert row["total_gb"] > row["free_gb"]


def test_healthy_volume_is_quiet():
    # 0GB floor is always met: no rows, no alert.
    assert disk_floor_rows(_policy(0)) == []


def test_absent_config_disables_check():
    # Old policy files without the key must not crash the patrol.
    assert disk_floor_rows({"bare_longrunner_max_age_min": 120}) == []


def test_breach_rows_carry_watch_path_name():
    rows = disk_floor_rows(_policy(999999, paths=(".", "corpus")))
    assert [r["path"] for r in rows] == [".", "corpus"]


def test_policy_file_carries_the_floor_block():
    # Spec-first law: the shipped policy config is the spec carrier; if the
    # block disappears the check silently disables, so pin its presence and
    # the 15GB floor the founding incident calibrated.
    import json
    from pathlib import Path
    policy = json.loads(
        (Path(__file__).resolve().parent.parent / "configs" / "longrunner_policy.json")
        .read_text(encoding="utf-8")
    )
    cfg = policy["disk_free_floor_gb"]
    assert cfg["floor_gb"] == 15
    assert cfg["watch_paths"] == ["."]
