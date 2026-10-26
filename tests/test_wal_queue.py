"""tests/test_wal_queue.py — Unit and stress tests for mag/wal_queue.py."""

import os
import sqlite3
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest
from mag.wal_queue import TaskQueue, is_pid_alive


@pytest.fixture
def queue(tmp_path):
    db_file = tmp_path / "test_queue.db"
    return TaskQueue(db_file)


def test_wal_pragmas_and_creation(queue):
    conn = sqlite3.connect(str(queue.db_path))
    journal_mode = conn.execute("PRAGMA journal_mode;").fetchone()[0]
    conn.close()
    assert journal_mode.lower() == "wal"

    stats = queue.stats("default")
    assert stats["total"] == 0


def test_enqueue_and_claim(queue):
    task_id, is_new = queue.enqueue("burn_lane", {"prompt": "test 1"})
    assert is_new is True
    assert task_id.startswith("task_")

    claimed = queue.claim("burn_lane", worker_pid=os.getpid(), worker_seat="bob_test")
    assert claimed is not None
    assert claimed["task_id"] == task_id
    assert claimed["status"] == "claimed"
    assert claimed["claimed_by_pid"] == os.getpid()
    assert claimed["payload"]["prompt"] == "test 1"
    assert claimed["attempts"] == 1

    # Second claim should return None (queue empty)
    assert queue.claim("burn_lane") is None


def test_ash_twin_hypothesis_deduplication(queue):
    hypo_hash = "sha256_mock_hypothesis_12345"
    tid1, is_new1 = queue.enqueue("research", {"query": "A"}, hypothesis_hash=hypo_hash)
    assert is_new1 is True

    # Duplicate enqueue with same hypothesis_hash
    tid2, is_new2 = queue.enqueue("research", {"query": "B"}, hypothesis_hash=hypo_hash)
    assert is_new2 is False
    assert tid2 == tid1

    # Only 1 task in queue
    assert queue.stats("research")["total"] == 1


def test_complete_lifecycle(queue):
    tid, _ = queue.enqueue("eval", {"metric": "loss"})
    claimed = queue.claim("eval")
    assert claimed is not None

    ok = queue.complete(tid, result={"loss": 0.042})
    assert ok is True

    stats = queue.stats("eval")
    assert stats["completed"] == 1
    assert stats["pending"] == 0
    assert stats["claimed"] == 0


def test_fail_and_retry_until_max_attempts(queue):
    tid, _ = queue.enqueue("retry_test", {"x": 1}, max_attempts=2)

    # Attempt 1
    c1 = queue.claim("retry_test")
    assert c1 is not None
    assert c1["attempts"] == 1
    queue.fail(tid, error="transient network error", retry=True)

    # Re-claim (attempt 2)
    c2 = queue.claim("retry_test")
    assert c2 is not None
    assert c2["attempts"] == 2
    queue.fail(tid, error="permanent error", retry=True)

    # Max attempts reached -> marked failed
    stats = queue.stats("retry_test")
    assert stats["failed"] == 1
    assert stats["pending"] == 0
    assert queue.claim("retry_test") is None


def test_lease_expiry_reap(queue):
    tid, _ = queue.enqueue("lease_test", {"item": 99}, lease_timeout_s=0.1)
    claimed = queue.claim("lease_test")
    assert claimed is not None

    # Wait for lease to expire
    time.sleep(0.15)

    # Claim should trigger reap and reclaim the task
    reclaimed = queue.claim("lease_test")
    assert reclaimed is not None
    assert reclaimed["task_id"] == tid
    assert reclaimed["attempts"] == 2


def test_dead_pid_reaping(queue):
    tid, _ = queue.enqueue("dead_pid_test", {"worker": "ghost"}, lease_timeout_s=3600.0)

    # Claim with a definitely non-existent PID (e.g. 999999 on most OSes)
    fake_dead_pid = 9999999
    assert is_pid_alive(fake_dead_pid) is False

    claimed = queue.claim("dead_pid_test", worker_pid=fake_dead_pid)
    assert claimed is not None

    # Even though lease timeout is 1 hour, reap detects dead PID and reaps it
    reaped = queue.reap("dead_pid_test")
    assert reaped == 1

    stats = queue.stats("dead_pid_test")
    assert stats["pending"] == 1
    assert stats["claimed"] == 0


def test_renew_lease(queue):
    tid, _ = queue.enqueue("renew_test", {}, lease_timeout_s=1.0)
    c = queue.claim("renew_test")
    old_expires = c["lease_expires_at"]

    time.sleep(0.05)
    queue.renew_lease(tid, extend_s=10.0)

    conn = sqlite3.connect(str(queue.db_path))
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT lease_expires_at FROM tasks WHERE task_id = ?;", (tid,)).fetchone()
    conn.close()
    assert row["lease_expires_at"] > old_expires


def test_concurrent_claims_no_double_claim(tmp_path):
    """Stress test: 10 worker threads simultaneously claiming 50 tasks.

    Falsifier: Every task must be claimed exactly once (zero double claims).
    """
    db_file = tmp_path / "concurrent_queue.db"
    q = TaskQueue(db_file)

    task_count = 50
    for i in range(task_count):
        q.enqueue("stress_queue", {"idx": i})

    claimed_task_ids = []

    def worker_loop():
        local_claimed = []
        for _ in range(task_count):
            task = q.claim("stress_queue")
            if task:
                local_claimed.append(task["task_id"])
                time.sleep(0.001)
                q.complete(task["task_id"], {"status": "ok"})
            else:
                break
        return local_claimed

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker_loop) for _ in range(10)]
        for f in futures:
            claimed_task_ids.extend(f.result())

    # Invariants:
    assert len(claimed_task_ids) == task_count
    assert len(set(claimed_task_ids)) == task_count  # ZERO duplicates
    stats = q.stats("stress_queue")
    assert stats["completed"] == task_count
    assert stats["pending"] == 0
    assert stats["claimed"] == 0
