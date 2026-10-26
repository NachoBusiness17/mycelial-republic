"""explore_decay tests (WAVE invariant-percolator, 2026-10-21, wave 6).

Binds tools/explore_decay.py:
  decay.plan(rows, already, days, now) -> classification rows
  decay.backlog(rows, already, now) -> live/stale split
  decay.main(["--root", tmp, "--apply"]) -> 0 ok / 1 refused / 2 unverifiable

The laws pinned here: the queue file is never rewritten (append-only
classification), aging is idempotent, and a fresh row is never aged.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import tools.explore_decay as decay

TOOL = Path(__file__).resolve().parents[1] / "tools" / "explore_decay.py"
NOW = datetime.now(timezone.utc)


def _row(canonical: str, days_old: float, status: str = "open") -> dict:
    return {"ts": (NOW - timedelta(days=days_old)).isoformat().replace("+00:00", "Z"),
            "source": "test", "domain": "behavioral", "signal": "s",
            "canonical": canonical, "status": status}


def _estate(tmp_path: Path, rows: list[dict]) -> Path:
    d = tmp_path / "memory" / "percolator"
    d.mkdir(parents=True, exist_ok=True)
    (d / "explore.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return tmp_path


def test_plan_ages_only_old_open_rows():
    rows = [_row("old", 30), _row("fresh", 2), _row("done", 30, status="done")]
    batch = decay.plan(rows, {}, 14, NOW)
    assert [r["canonical"] for r in batch] == ["old"]
    assert batch[0]["status"] == "stale" and batch[0]["age_days"] >= 29


def test_plan_is_idempotent():
    rows = [_row("old", 30)]
    already = {"old": {"canonical": "old", "status": "stale"}}
    assert decay.plan(rows, already, 14, NOW) == []


def test_backlog_splits_live_and_stale():
    rows = [_row("a", 30), _row("b", 20), _row("c", 1)]
    stats = decay.backlog(rows, {"a": {}, "b": {}}, NOW)
    assert stats["open"] == 3 and stats["stale"] == 2 and stats["live"] == 1
    assert stats["live_median_age_days"] < 2


def test_apply_appends_and_never_rewrites_the_queue(tmp_path):
    root = _estate(tmp_path, [_row("a", 30), _row("b", 1)])
    queue = root / "memory" / "percolator" / "explore.jsonl"
    before = hashlib.sha256(queue.read_bytes()).hexdigest()
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply", "--json"],
                        capture_output=True, text=True)
    assert cp.returncode == 0, cp.stdout + cp.stderr
    receipt = json.loads(cp.stdout)
    assert receipt["written"] == 1
    assert hashlib.sha256(queue.read_bytes()).hexdigest() == before
    ledger = root / "memory" / "percolator" / "explore_decay.jsonl"
    assert len(ledger.read_text(encoding="utf-8").splitlines()) == 1


def test_second_apply_writes_zero(tmp_path):
    root = _estate(tmp_path, [_row("a", 30)])
    subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply"],
                   capture_output=True, text=True, check=True)
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply", "--json"],
                        capture_output=True, text=True, check=True)
    assert json.loads(cp.stdout)["written"] == 0


def test_dry_run_writes_nothing(tmp_path):
    root = _estate(tmp_path, [_row("a", 30)])
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--json"],
                        capture_output=True, text=True)
    receipt = json.loads(cp.stdout)
    assert receipt["applied"] is False and receipt["pending"] == 1
    assert not (root / "memory" / "percolator" / "explore_decay.jsonl").exists()


def test_missing_queue_exits_2(tmp_path):
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(tmp_path)],
                        capture_output=True, text=True)
    assert cp.returncode == 2 and cp.stdout.startswith("EXPLORE-DECAY: UNVERIFIABLE")


def test_malformed_ledger_lines_are_skipped(tmp_path):
    root = _estate(tmp_path, [_row("a", 30)])
    ledger = root / "memory" / "percolator" / "explore_decay.jsonl"
    ledger.write_text("{not json}\n", encoding="utf-8")
    cp = subprocess.run([sys.executable, str(TOOL), "--root", str(root), "--apply"],
                        capture_output=True, text=True)
    assert cp.returncode == 0
    assert len(ledger.read_text(encoding="utf-8").splitlines()) == 2
