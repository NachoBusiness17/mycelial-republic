"""disk_smith --prune tests (L2 retention leg, disk-audit-20261009).

The retention sweep must kill exactly the aged set, never touch the live
window, refuse escaping names through the same containment guards as the
harvester (safe_child pattern, harvest_exec_forest.py), refuse degenerate
contracts, and bank one receipt row per apply. Synthetic trees in tmp_path
only; the real exec forest is never touched here.
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

from tools import disk_smith

DAY = 86400.0


def _plant(root: Path, rel: str, age_days: float, size: int = 10) -> Path:
    """Write one file under root with a pinned mtime age_days in the past."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b"x" * size)
    mt = time.time() - age_days * DAY
    os.utime(p, (mt, mt))
    return p


def _synthetic_tree(tmp_path: Path):
    """One exec-forest shape: nested session dirs, young and aged files,
    plus one loose file at the root. Returns (root, young, aged) path sets."""
    root = tmp_path / "exec"
    root.mkdir()
    young = {
        _plant(root, "sess_live/now.txt", 0.5),
        _plant(root, "sess_live/recent.jsonl", 3.0),
        _plant(root, "sess_mid/six.txt", 6.9, size=20),
        _plant(root, "loose_young.txt", 2.0),
    }
    aged = {
        _plant(root, "sess_live/old_stdout.json", 7.5, size=100),
        _plant(root, "sess_mid/deep/aged.log", 10.0, size=50),
        _plant(root, "loose_aged.bin", 30.0, size=200),
    }
    return root, young, aged


def test_prune_plan_kills_exactly_the_aged_set(tmp_path):
    root, young, aged = _synthetic_tree(tmp_path)
    now = time.time()
    plan = disk_smith.prune_plan({"t": str(root)}, 7.0, now)
    killed = {item["path"] for item in plan["t"]["kill"]}
    assert killed == {str(p) for p in aged}
    assert all(str(p) not in killed for p in young)
    assert plan["t"]["scanned"] == 7
    assert plan["t"]["kill_files"] == 3
    assert plan["t"]["kill_bytes"] == 350
    assert plan["t"]["errors"] == 0
    # the L2 falsifier guard: no kill younger than min_age (1d) exists
    assert min(item["age_days"] for item in plan["t"]["kill"]) > 1.0


def test_prune_dry_run_deletes_nothing_and_writes_nothing(tmp_path, capsys):
    root, young, aged = _synthetic_tree(tmp_path)
    ledger = tmp_path / "prune_ledger.jsonl"
    rc = disk_smith.prune({"t": str(root)}, 7.0, 1.0,
                          apply=False, ledger=ledger)
    out = capsys.readouterr().out
    assert rc == 0
    assert "DRY RUN - nothing deleted" in out
    assert "TOTAL: 3 files" in out
    for p in young | aged:
        assert p.exists()
    assert not ledger.exists()


def test_prune_apply_deletes_exactly_the_aged_set_and_banks_receipt(
        tmp_path, capsys):
    root, young, aged = _synthetic_tree(tmp_path)
    ledger = tmp_path / "prune_ledger.jsonl"
    rc = disk_smith.prune({"t": str(root)}, 7.0, 1.0,
                          apply=True, ledger=ledger)
    out = capsys.readouterr().out
    assert rc == 0
    assert "APPLIED: deleted 3" in out
    for p in aged:
        assert not p.exists()
    for p in young:
        assert p.exists()
    rows = [json.loads(line) for line in
            ledger.read_text(encoding="utf-8").strip().splitlines()]
    assert len(rows) == 1
    row = rows[0]
    assert row["kind"] == "prune"
    assert row["mode"] == "apply"
    assert row["deleted"] == 3
    assert row["freed_bytes"] == 350
    assert row["failed"] == 0
    assert row["roots"]["t"]["kill_files"] == 3
    assert row["ts"].endswith("Z")


def test_prune_apply_failure_is_counted_never_fatal(tmp_path):
    # a kill row whose path escapes the root (forged plan) must be counted
    # failed by the guard-adjacent-to-access re-check, not deleted
    root, young, aged = _synthetic_tree(tmp_path)
    outside = _plant(tmp_path, "outside/never_kill.txt", 30.0)
    real_plan = disk_smith.prune_plan({"t": str(root)}, 7.0, time.time())
    forged = real_plan["t"]["kill"] + [
        {"path": str(outside), "bytes": 10, "age_days": 30.0}]
    real_plan["t"]["kill"] = forged
    ledger = tmp_path / "prune_ledger.jsonl"
    orig = disk_smith.prune_plan
    disk_smith.prune_plan = lambda *a, **k: real_plan
    try:
        rc = disk_smith.prune({"t": str(root)}, 7.0, 1.0,
                              apply=True, ledger=ledger)
    finally:
        disk_smith.prune_plan = orig
    assert rc == 0
    assert outside.exists()
    for p in aged:
        assert not p.exists()
    row = json.loads(ledger.read_text(encoding="utf-8").strip())
    assert row["deleted"] == 3
    assert row["failed"] == 1
    assert row["fail_list"] == [str(outside)]


def test_safe_child_refuses_escaping_names(tmp_path):
    root = tmp_path / "exec"
    (root / "sess").mkdir(parents=True)
    allow = root.resolve()
    ok = disk_smith.safe_child(root / "sess", "plain.txt", allow)
    assert ok == root / "sess" / "plain.txt"
    for bad in ("", ".", "..", "a/b", "a\\b", "..\\evil", "x/y.txt"):
        assert disk_smith.safe_child(root / "sess", bad, allow) is None
    # resolve-check: a join made outside the allowroot refuses even with a
    # plain filename
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    assert disk_smith.safe_child(elsewhere, "plain.txt", allow) is None


def test_prune_contract_refuses_zero_and_under_min_age(tmp_path, capsys):
    root, _young, aged = _synthetic_tree(tmp_path)
    ledger = tmp_path / "prune_ledger.jsonl"
    assert disk_smith.prune({"t": str(root)}, 0.0, 1.0,
                            apply=True, ledger=ledger) == 2
    assert disk_smith.prune({"t": str(root)}, 0.5, 1.0,
                            apply=True, ledger=ledger) == 2
    for p in aged:
        assert p.exists()
    assert not ledger.exists()


def test_prune_disabled_contract_refuses(tmp_path):
    root, _young, aged = _synthetic_tree(tmp_path)
    ledger = tmp_path / "prune_ledger.jsonl"
    orig = dict(disk_smith.RETENTION)
    disk_smith.RETENTION["enabled"] = False
    try:
        rc = disk_smith.prune({"t": str(root)}, 7.0, 1.0,
                              apply=True, ledger=ledger)
    finally:
        disk_smith.RETENTION.clear()
        disk_smith.RETENTION.update(orig)
    assert rc == 2
    for p in aged:
        assert p.exists()
    assert not ledger.exists()


def test_prune_ledger_resolves_from_config_at_call_time(tmp_path, monkeypatch):
    # footgun caught by the landing demo 2026-10-09: a def-time default
    # arg (ledger=PRUNE_LEDGER) ignores module-global redirects, so a
    # config-pointed ledger silently receives nothing and the row lands in
    # the real logs/ dir. The default must resolve at call time.
    root, _young, _aged = _synthetic_tree(tmp_path)
    ledger = tmp_path / "redirected.jsonl"
    monkeypatch.setattr(disk_smith, "PRUNE_LEDGER", ledger)
    rc = disk_smith.prune({"t": str(root)}, 7.0, 1.0, apply=True)
    assert rc == 0
    assert ledger.exists()
    assert len(ledger.read_text(encoding="utf-8").strip().splitlines()) == 1


def test_snap_path_output_shape_unchanged(tmp_path, capsys, monkeypatch):
    # the mission law: the daily snap path stays byte-identical in output
    # shape; the --prune wiring must not leak into a plain snap row. snap()
    # itself is canned here (the live walk is test_disk_smith.py's lane);
    # this pins what main() prints, appends, and exits.
    import sys as _sys
    from datetime import datetime, timezone

    canned = {
        "ts": "2026-10-09T00:00:00Z", "monsters": {"pagefile": 40.0},
        "seats": {}, "estate": {}, "free_gb": 95.0, "total_gb": 1862.0,
    }
    ledger = tmp_path / "snap.jsonl"
    monkeypatch.setattr(disk_smith, "LEDGER", ledger)
    monkeypatch.setattr(disk_smith, "snap", lambda now: dict(
        canned, ts=now.isoformat().replace("+00:00", "Z")))
    monkeypatch.setattr(_sys, "argv", ["disk_smith"])
    rc = disk_smith.main()
    assert rc == 0  # canned row is healthy: no alert may fire
    first = capsys.readouterr().out.splitlines()[0]
    row = json.loads(first)
    assert set(row) == {"ts", "monsters", "seats", "estate", "free_gb",
                        "total_gb", "delta"}
    lines = ledger.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["ts"].endswith("Z")
