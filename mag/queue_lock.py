#!/usr/bin/env python3
"""queue_lock -- one writer at a time on the explore queue.

The queue has two writers with different shapes (2026-10-24):
  - mag/percolator.py APPENDS a row per novel signal;
  - mag/fuel_feed.py REWRITES the file when it merges repeats.
An append that lands inside a read-modify-write is silently lost. This is the
advisory lock both sides take; it is deliberately dumb (O_CREAT|O_EXCL, stale
steal after 60s) because a clever lock is a second scheduler.
"""
from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path

STALE_S = 60.0
TIMEOUT_S = 10.0


def lock_path(path: Path) -> Path:
    return path.with_suffix(path.suffix + ".lock")


@contextmanager
def queue_lock(path: Path, timeout: float = TIMEOUT_S, stale_s: float = STALE_S):
    lock = lock_path(path)
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + timeout
    fd = None
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                age = time.time() - lock.stat().st_mtime
            except OSError:
                age = 0.0
            if age > stale_s:
                try:
                    lock.unlink()
                except OSError:
                    pass
                continue
            if time.time() > deadline:
                raise TimeoutError(f"queue lock held > {timeout:g}s: {lock}")
            time.sleep(0.05)
    try:
        yield
    finally:
        try:
            lock.unlink()
        except OSError:
            pass
