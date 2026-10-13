"""Q21 regression: concurrent registrations on one account file must all land.

Executed probe 2026-10-01 (watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md
row Q21): 8 threads x 8 store instances on one users.json persisted 1/8 —
last-writer-wins, because each store saved its stale construction-time dict.
These tests hold the fixed contract: every registration survives, and no
reader ever observes a torn file.
"""
from __future__ import annotations

import json
import threading
from pathlib import Path

from server.auth import AuthStore
from server.auth_srp6 import SrpStore


def _run_threads(targets) -> None:
    threads = [threading.Thread(target=t) for t in targets]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def test_auth_store_8_threads_8_instances_all_persist(tmp_path: Path) -> None:
    path = tmp_path / "users.json"
    stores = [AuthStore(path) for _ in range(8)]

    def register(i: int, store: AuthStore) -> None:
        store.ensure_user(f"user{i}", f"pw{i}")

    _run_threads([lambda i=i, s=s: register(i, s) for i, s in enumerate(stores)])
    persisted = json.loads(path.read_text(encoding="utf-8"))["users"]
    assert sorted(persisted) == sorted(f"user{i}" for i in range(8))
    # and a fresh store sees the same world (no in-memory-only survivor)
    fresh = AuthStore(path)
    assert sorted(fresh.users) == sorted(f"user{i}" for i in range(8))


def test_srp_store_8_threads_8_instances_all_persist(tmp_path: Path) -> None:
    path = tmp_path / "users.json"
    stores = [SrpStore(path) for _ in range(8)]

    def register(i: int, store: SrpStore) -> None:
        store.register(f"srpuser{i}", f"pw{i}")

    _run_threads([lambda i=i, s=s: register(i, s) for i, s in enumerate(stores)])
    persisted = json.loads(path.read_text(encoding="utf-8"))["users"]
    assert sorted(persisted) == sorted(f"srpuser{i}" for i in range(8))
    for row in persisted.values():
        assert row.get("group") and row.get("verifier") and row.get("salt")


def test_concurrent_writes_never_expose_a_torn_file(tmp_path: Path) -> None:
    path = tmp_path / "users.json"
    store = AuthStore(path)
    store.ensure_user("seed", "pw")
    stop = threading.Event()
    errors: list[str] = []

    def writer() -> None:
        for i in range(200):
            store.ensure_user(f"w{i}", "pw")

    def reader() -> None:
        # Contract: a lockless reader never sees TORN CONTENT. On Windows a
        # reader whose open lands mid-os.replace gets a transient sharing
        # violation (PermissionError 13) — retryable contention, not torn
        # bytes; a JSONDecodeError is the disease this test exists to catch.
        retries = 0
        while not stop.is_set():
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except PermissionError:
                retries += 1
                assert retries < 1000, "reader starved beyond contention"
            except (json.JSONDecodeError, OSError) as exc:
                errors.append(repr(exc))
                return

    readers = [threading.Thread(target=reader) for _ in range(2)]
    for r in readers:
        r.start()
    writer()
    stop.set()
    for r in readers:
        r.join()
    assert errors == []


def test_store_io_rejects_parent_steps(tmp_path: Path) -> None:
    from server.store_io import atomic_write_text, exclusive

    evil = tmp_path / ".." / "escape.json"
    try:
        atomic_write_text(evil, "{}")
    except ValueError as exc:
        assert ".." in str(exc)
    else:
        raise AssertionError("parent-step path must be refused")
    try:
        with exclusive(evil):
            pass
    except ValueError:
        pass
    else:
        raise AssertionError("parent-step path must be refused")
