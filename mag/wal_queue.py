"""mag/wal_queue.py — Atomic SQLite WAL task queue with lease expiry and dead-PID reaper.

Implements STEAL 2 (SQLite WAL claim-lease queue replacing ad-hoc file claims):
- PRAGMA journal_mode=WAL + synchronous=NORMAL + busy_timeout=10000
- Atomic claims using BEGIN IMMEDIATE transactions (zero write collisions under concurrent dispatch)
- Lease timeout expiry with periodic and on-claim reaping
- Dead-PID reaper: detects dead worker processes via cross-platform OS query and frees their claims immediately
- Ash Twin hypothesis_hash deduplication: prevents duplicate execution of identical hypotheses
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def is_pid_alive(pid: int | None) -> bool:
    """Check if a process with `pid` is currently alive on the host system."""
    if pid is None or pid <= 0:
        return False
    if sys.platform == "win32":
        try:
            import ctypes
            import ctypes.wintypes
            kernel32 = ctypes.windll.kernel32
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            SYNCHRONIZE = 0x00100000
            handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | SYNCHRONIZE, False, int(pid))
            if not handle:
                return False
            try:
                exit_code = ctypes.wintypes.DWORD()
                if kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)):
                    STILL_ACTIVE = 259
                    return exit_code.value == STILL_ACTIVE
                return False
            finally:
                kernel32.CloseHandle(handle)
        except Exception:
            return True  # conservative fallback
    else:
        try:
            os.kill(pid, 0)
            return True
        except (ProcessLookupError, PermissionError):
            return False


class TaskQueue:
    """SQLite WAL-backed persistent atomic task queue."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=10.0,
            isolation_level=None,  # autocommit / explicit transaction control
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=10000;")
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    queue_name TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    hypothesis_hash TEXT,
                    status TEXT NOT NULL DEFAULT 'pending',
                    claimed_by_pid INTEGER,
                    claimed_by_seat TEXT,
                    claimed_at REAL,
                    lease_timeout_s REAL DEFAULT 60.0,
                    lease_expires_at REAL,
                    created_at REAL NOT NULL,
                    completed_at REAL,
                    result_json TEXT,
                    error_text TEXT,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    max_attempts INTEGER NOT NULL DEFAULT 3
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_wal_tasks_queue_status ON tasks(queue_name, status, created_at);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_wal_tasks_lease ON tasks(status, lease_expires_at);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_wal_tasks_hypo ON tasks(queue_name, hypothesis_hash);")

    def enqueue(
        self,
        queue_name: str,
        payload: Any,
        hypothesis_hash: Optional[str] = None,
        lease_timeout_s: float = 60.0,
        max_attempts: int = 3,
    ) -> Tuple[str, bool]:
        """Enqueue a task.

        Returns (task_id, is_new).
        If `hypothesis_hash` matches an existing pending or completed task in the same queue,
        the existing task_id is returned with is_new=False (Ash Twin deduplication).
        """
        payload_str = json.dumps(payload) if not isinstance(payload, str) else payload
        now = time.time()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            if hypothesis_hash:
                row = conn.execute(
                    """SELECT task_id, status FROM tasks 
                       WHERE queue_name = ? AND hypothesis_hash = ? AND status IN ('pending', 'claimed', 'completed')
                       LIMIT 1;""",
                    (queue_name, hypothesis_hash),
                ).fetchone()
                if row:
                    conn.execute("COMMIT;")
                    return row["task_id"], False

            task_id = f"task_{int(now * 1000)}_{os.urandom(4).hex()}"
            conn.execute(
                """INSERT INTO tasks (
                    task_id, queue_name, payload_json, hypothesis_hash,
                    status, lease_timeout_s, created_at, attempts, max_attempts
                ) VALUES (?, ?, ?, ?, 'pending', ?, ?, 0, ?);""",
                (task_id, queue_name, payload_str, hypothesis_hash, lease_timeout_s, now, max_attempts),
            )
            conn.execute("COMMIT;")
            return task_id, True
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()

    def claim(
        self,
        queue_name: str,
        worker_pid: Optional[int] = None,
        worker_seat: Optional[str] = None,
        lease_timeout_s: Optional[float] = None,
    ) -> Optional[Dict[str, Any]]:
        """Atomically claim the next pending task for `queue_name`.

        Automatically reaps dead/expired leases in this queue first.
        Returns the claimed task record as a dict, or None if no tasks are available.
        """
        worker_pid = worker_pid or os.getpid()
        worker_seat = worker_seat or os.getenv("GSTD_BODY_NAME", "local")
        now = time.time()

        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            # 1. Inline reap of dead/expired leases in this queue
            self._reap_internal(conn, queue_name, now)

            # 2. Pick next pending task
            row = conn.execute(
                """SELECT * FROM tasks 
                   WHERE queue_name = ? AND status = 'pending' AND attempts < max_attempts
                   ORDER BY created_at ASC LIMIT 1;""",
                (queue_name,),
            ).fetchone()

            if not row:
                conn.execute("COMMIT;")
                return None

            task_id = row["task_id"]
            timeout = lease_timeout_s or float(row["lease_timeout_s"] or 60.0)
            lease_expires = now + timeout
            new_attempts = int(row["attempts"]) + 1

            conn.execute(
                """UPDATE tasks SET
                    status = 'claimed',
                    claimed_by_pid = ?,
                    claimed_by_seat = ?,
                    claimed_at = ?,
                    lease_expires_at = ?,
                    lease_timeout_s = ?,
                    attempts = ?
                   WHERE task_id = ?;""",
                (worker_pid, worker_seat, now, lease_expires, timeout, new_attempts, task_id),
            )
            conn.execute("COMMIT;")

            out = dict(row)
            out["status"] = "claimed"
            out["claimed_by_pid"] = worker_pid
            out["claimed_by_seat"] = worker_seat
            out["claimed_at"] = now
            out["lease_expires_at"] = lease_expires
            out["attempts"] = new_attempts
            try:
                out["payload"] = json.loads(out["payload_json"])
            except Exception:
                out["payload"] = out["payload_json"]
            return out
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()

    def complete(self, task_id: str, result: Any = None) -> bool:
        """Mark a claimed task as completed."""
        result_str = json.dumps(result) if result is not None and not isinstance(result, str) else (result or "")
        now = time.time()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            cur = conn.execute(
                """UPDATE tasks SET
                    status = 'completed',
                    completed_at = ?,
                    result_json = ?
                   WHERE task_id = ? AND status = 'claimed';""",
                (now, result_str, task_id),
            )
            affected = cur.rowcount > 0
            conn.execute("COMMIT;")
            return affected
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()

    def fail(self, task_id: str, error: str = "", retry: bool = True) -> bool:
        """Mark a claimed task as failed or return it to pending for retry."""
        now = time.time()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            row = conn.execute("SELECT attempts, max_attempts FROM tasks WHERE task_id = ?;", (task_id,)).fetchone()
            if not row:
                conn.execute("COMMIT;")
                return False

            can_retry = retry and (int(row["attempts"]) < int(row["max_attempts"]))
            new_status = "pending" if can_retry else "failed"

            conn.execute(
                """UPDATE tasks SET
                    status = ?,
                    claimed_by_pid = NULL,
                    claimed_by_seat = NULL,
                    lease_expires_at = NULL,
                    error_text = ?
                   WHERE task_id = ?;""",
                (new_status, error, task_id),
            )
            conn.execute("COMMIT;")
            return True
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()

    def renew_lease(self, task_id: str, extend_s: float = 60.0) -> bool:
        """Extend the lease of an actively running task."""
        now = time.time()
        new_expires = now + extend_s
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            cur = conn.execute(
                "UPDATE tasks SET lease_expires_at = ? WHERE task_id = ? AND status = 'claimed';",
                (new_expires, task_id),
            )
            affected = cur.rowcount > 0
            conn.execute("COMMIT;")
            return affected
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()

    def _reap_internal(self, conn: sqlite3.Connection, queue_name: Optional[str], now: float) -> int:
        """Helper to reap dead or expired tasks within an existing transaction."""
        query = "SELECT task_id, claimed_by_pid, lease_expires_at, attempts, max_attempts FROM tasks WHERE status = 'claimed'"
        params: List[Any] = []
        if queue_name:
            query += " AND queue_name = ?"
            params.append(queue_name)

        rows = conn.execute(query, params).fetchall()
        reaped = 0
        for r in rows:
            tid = r["task_id"]
            pid = r["claimed_by_pid"]
            expires_at = float(r["lease_expires_at"] or 0.0)
            attempts = int(r["attempts"])
            max_attempts = int(r["max_attempts"])

            is_expired = expires_at > 0 and expires_at <= now
            is_dead = (pid is not None) and not is_pid_alive(pid)

            if is_expired or is_dead:
                reason = "lease_expired" if is_expired else f"dead_pid_{pid}"
                if attempts >= max_attempts:
                    conn.execute(
                        "UPDATE tasks SET status = 'failed', error_text = ? WHERE task_id = ?;",
                        (f"reaped:{reason}:max_attempts_exceeded", tid),
                    )
                else:
                    conn.execute(
                        """UPDATE tasks SET
                            status = 'pending',
                            claimed_by_pid = NULL,
                            claimed_by_seat = NULL,
                            lease_expires_at = NULL,
                            error_text = ?
                           WHERE task_id = ?;""",
                        (f"reaped:{reason}", tid),
                    )
                reaped += 1
        return reaped

    def reap(self, queue_name: Optional[str] = None) -> int:
        """Reap all dead worker leases or timed out claims."""
        now = time.time()
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE;")
            count = self._reap_internal(conn, queue_name, now)
            conn.execute("COMMIT;")
            return count
        except Exception:
            conn.execute("ROLLBACK;")
            raise
        finally:
            conn.close()

    def stats(self, queue_name: Optional[str] = None) -> Dict[str, int]:
        """Return counts by status."""
        query = "SELECT status, COUNT(*) as cnt FROM tasks"
        params: List[Any] = []
        if queue_name:
            query += " WHERE queue_name = ?"
            params.append(queue_name)
        query += " GROUP BY status;"

        out = {"pending": 0, "claimed": 0, "completed": 0, "failed": 0, "total": 0}
        with self._get_connection() as conn:
            for r in conn.execute(query, params):
                st = r["status"]
                c = int(r["cnt"])
                out[st] = c
                out["total"] += c
        return out
