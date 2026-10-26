"""store_io: locked, atomic persistence for the JSON account stores.

Root cause (Q21, watch/inbox/mountain_climb/FIFTY_QUESTIONS_ANSWERED.md,
executed probe 2026-10-01): 8 threads x 8 store instances on one users.json
lost 7/8 registrations. The stores loaded once at construction and saved the
whole in-memory dict, so concurrent writers overwrote each other
(last-writer-wins) and a reader could catch a torn file mid-write.

The fix is two mechanisms and neither substitutes for the other:

1. ``exclusive(path)`` — a per-path in-process RLock plus a cross-process
   byte lock on ``<path>.lock``. Mutators re-read the file UNDER the lock
   before mutating (read-modify-write as one critical section), so separate
   store instances and separate processes serialize instead of racing.
2. ``atomic_write_text`` — mkstemp in the same directory + ``os.replace``
   (the estate idiom, cf. mag/realign.py, tools/receipt_body_fts.py).
   Lockless readers never observe a half-written file; a crashed writer
   leaves the old bytes plus a stray ``.tmp`` file, never corruption.

Write targets are validated against allowlisted roots (repo tree + the OS
temp dir) and reject ``..`` segments before any derived path exists: the
``.lock`` / ``.tmp`` siblings inherit the store path verbatim, so an
unvalidated path could place them outside the intended directory (Mimosa
gate ruling, 2026-10-01).

Windows locks use ``msvcrt.locking``, POSIX uses ``fcntl.flock``. No RNG,
no threads spawned, no fsync-dir dance (account files are not databases;
crash-atomicity of the rename is enough).
"""
from __future__ import annotations

import os
import tempfile
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, TextIO

if os.name == "nt":  # pragma: no cover - platform branch exercised live on win32
    import msvcrt

    def _lock_byte(fh: TextIO) -> None:
        fh.seek(0)
        while True:
            try:
                msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
                return
            except OSError:
                time.sleep(0.01)

    def _unlock_byte(fh: TextIO) -> None:
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_UNLCK, 1)

else:  # pragma: no cover - POSIX twin
    import fcntl

    def _lock_byte(fh: TextIO) -> None:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)

    def _unlock_byte(fh: TextIO) -> None:
        fcntl.flock(fh.fileno(), fcntl.LOCK_UN)

_THREAD_LOCKS: dict[str, threading.RLock] = {}
_THREAD_LOCKS_GUARD = threading.Lock()
_LOCK_TIMEOUT_S = 30.0
_REPLACE_TIMEOUT_S = 5.0

# Store files live in the repo tree (state/, run dirs) or in test/user temp
# dirs. Anything else (network shares, other repos) is refused loudly.
_ALLOWED_ROOTS = (Path(__file__).resolve().parent.parent,
                  Path(tempfile.gettempdir()).resolve())


def _validated(path: Path | str) -> Path:
    """Resolve and confine ``path`` to the allowlisted roots; reject ``..``."""
    p = Path(path)
    if ".." in p.parts:
        raise ValueError(f"path must not contain '..' segments: {p}")
    resolved = p.resolve()
    for root in _ALLOWED_ROOTS:
        if resolved == root or root in resolved.parents:
            return resolved
    raise ValueError(
        f"write target {resolved} is outside the allowed roots "
        f"{[str(r) for r in _ALLOWED_ROOTS]}")


def _thread_lock_for(path: Path) -> threading.RLock:
    key = str(path)
    with _THREAD_LOCKS_GUARD:
        lock = _THREAD_LOCKS.get(key)
        if lock is None:
            lock = threading.RLock()
            _THREAD_LOCKS[key] = lock
        return lock


@contextmanager
def exclusive(path: Path | str) -> Iterator[None]:
    """Serialize read-modify-write on ``path`` across threads and processes.

    The OS lock file (``<name>.lock``) is created lazily and never removed:
    unlinking a lock file is its own race (a waiter can hold a lock on an
    unlinked inode while a newcomer locks a fresh file).
    """
    path = _validated(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_file = path.with_name(path.name + ".lock")
    tlock = _thread_lock_for(path)
    deadline = time.monotonic() + _LOCK_TIMEOUT_S
    with tlock:
        with open(lock_file, "a+b") as fh:
            while True:
                try:
                    _lock_byte(fh)
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise TimeoutError(
                            f"could not acquire {lock_file} within "
                            f"{_LOCK_TIMEOUT_S}s")
                    time.sleep(0.01)
            try:
                yield
            finally:
                _unlock_byte(fh)


def atomic_write_text(path: Path | str, text: str) -> None:
    """Write ``text`` so readers see either the old bytes or the new bytes.

    On Windows ``os.replace`` raises PermissionError while any other handle
    holds the target open (a lockless reader mid-``read_text``): retry with
    a short backoff, since such handles close in microseconds. POSIX renames
    never see this and take the first branch.
    """
    path = _validated(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=path.name + ".tmp-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        deadline = time.monotonic() + _REPLACE_TIMEOUT_S
        while True:
            try:
                os.replace(tmp_name, path)
                return
            except PermissionError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(0.005)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise
