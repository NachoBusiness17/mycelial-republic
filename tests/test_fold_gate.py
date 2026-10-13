"""fold_gate tests: the cross-run fold mutex (2026-10-05).

Exercised CLI-end-to-end (subprocess) because the real callers are separate
short-lived processes - workflow world.run bash calls and agent tool-calls -
never an in-process import. All locks live in a tmp dir via --dir; the repo's
memory/runs/fold_locks is never touched by tests.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "fold_gate.py"


def run_gate(tmp_path, *args):
    return subprocess.run(
        [sys.executable, str(TOOL), *args, "--dir", str(tmp_path)],
        capture_output=True, text=True, timeout=60,
    )


def log_rows(tmp_path, name="workflow-fold"):
    p = tmp_path / f"{name}.lock.log"
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line]


def test_acquire_status_release_cycle(tmp_path):
    a = run_gate(tmp_path, "acquire", "--holder", "mine-a", "--wait", "0")
    assert a.returncode == 0, a.stderr
    assert "HELD" in a.stdout

    s = run_gate(tmp_path, "status")
    assert s.returncode == 0
    assert "holder=mine-a" in s.stdout

    r = run_gate(tmp_path, "release", "--holder", "mine-a")
    assert r.returncode == 0, r.stderr
    s = run_gate(tmp_path, "status")
    assert "FREE" in s.stdout

    events = [row["event"] for row in log_rows(tmp_path)]
    assert events == ["acquire", "release"]


def test_second_acquire_waits_then_proceeds(tmp_path):
    """The cure species: fold B waits for fold A instead of erroring."""
    a = run_gate(tmp_path, "acquire", "--holder", "fold-a", "--wait", "0")
    assert a.returncode == 0

    proc = subprocess.Popen(
        [sys.executable, str(TOOL), "acquire", "--holder", "fold-b",
         "--wait", "30", "--poll", "1", "--dir", str(tmp_path)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    time.sleep(2)  # fold-b is now parked waiting on fold-a
    assert proc.poll() is None, "waiter gave up before the holder released"

    rel = run_gate(tmp_path, "release", "--holder", "fold-a")
    assert rel.returncode == 0
    out, _ = proc.communicate(timeout=30)
    assert proc.returncode == 0, out
    assert "HELD" in out

    s = run_gate(tmp_path, "status")
    assert "holder=fold-b" in s.stdout
    assert run_gate(tmp_path, "release", "--holder", "fold-b").returncode == 0


def test_wait_timeout_exits_4_and_keeps_lock(tmp_path):
    a = run_gate(tmp_path, "acquire", "--holder", "fold-a", "--wait", "0")
    assert a.returncode == 0

    b = run_gate(tmp_path, "acquire", "--holder", "fold-b", "--wait", "1", "--poll", "1")
    assert b.returncode == 4
    assert "ledger_lock" in b.stderr  # the proceed-unlocked instruction

    s = run_gate(tmp_path, "status")
    assert "holder=fold-a" in s.stdout  # timeout never stole the lock
    assert any(r["event"] == "wait-timeout" for r in log_rows(tmp_path))


def test_stale_break_takes_dead_holder_lock(tmp_path):
    """The reboot species: a holder that died mid-fold clears at stale age."""
    a = run_gate(tmp_path, "acquire", "--holder", "dead-fold", "--wait", "0")
    assert a.returncode == 0
    lock = tmp_path / "workflow-fold.lock"
    old = time.time() - 3600  # 1h old
    os.utime(lock, (old, old))

    b = run_gate(tmp_path, "acquire", "--holder", "fold-b", "--wait", "0", "--stale-seconds", "60")
    assert b.returncode == 0, b.stderr
    assert "holder=fold-b" in run_gate(tmp_path, "status").stdout

    rows = log_rows(tmp_path)
    brk = next(r for r in rows if r["event"] == "stale-break")
    assert brk["prior_holder"] == "unknown"  # stamped post-remove; see tool comment


def test_release_wrong_holder_refused_then_forced(tmp_path):
    assert run_gate(tmp_path, "acquire", "--holder", "fold-a", "--wait", "0").returncode == 0

    wrong = run_gate(tmp_path, "release", "--holder", "not-the-holder")
    assert wrong.returncode == 5
    assert "holder=fold-a" in run_gate(tmp_path, "status").stdout
    assert any(r["event"] == "release-refused" for r in log_rows(tmp_path))

    forced = run_gate(tmp_path, "release", "--holder", "operator", "--force")
    assert forced.returncode == 0
    assert any(r["event"] == "force-release" for r in log_rows(tmp_path))
    assert "FREE" in run_gate(tmp_path, "status").stdout


def test_release_when_free_is_success(tmp_path):
    r = run_gate(tmp_path, "release", "--holder", "anyone")
    assert r.returncode == 0
    assert "FREE" in r.stdout
