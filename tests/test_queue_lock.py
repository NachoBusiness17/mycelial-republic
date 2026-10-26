"""The explore queue has two writers; the lock must actually exclude.

2026-10-24: percolator appends while fuel_feed.clarify rewrites. The rewrite was
made atomic, but an append landing inside the read-modify-write is still lost.
These tests pin the advisory lock that both sides now take.
"""
from __future__ import annotations

import json
import threading
import time

import pytest

from mag.queue_lock import lock_path, queue_lock


def test_lock_is_exclusive(tmp_path):
    target = tmp_path / "explore.jsonl"
    target.write_text("", encoding="utf-8")
    order = []

    def holder(name, hold):
        with queue_lock(target, timeout=5):
            order.append(f"{name}-in")
            time.sleep(hold)
            order.append(f"{name}-out")

    a = threading.Thread(target=holder, args=("a", 0.4))
    b = threading.Thread(target=holder, args=("b", 0.05))
    a.start(); time.sleep(0.05); b.start()
    a.join(); b.join()
    # b cannot enter until a has left
    assert order == ["a-in", "a-out", "b-in", "b-out"], order


def test_lock_is_released_even_on_error(tmp_path):
    target = tmp_path / "explore.jsonl"
    with pytest.raises(RuntimeError):
        with queue_lock(target):
            raise RuntimeError("boom")
    assert not lock_path(target).exists()


def test_stale_lock_is_stolen(tmp_path):
    target = tmp_path / "explore.jsonl"
    lock = lock_path(target)
    lock.write_text("999999", encoding="utf-8")
    old = time.time() - 120
    import os
    os.utime(lock, (old, old))
    with queue_lock(target, timeout=1, stale_s=60):
        pass
    assert not lock.exists()


def test_timeout_when_lock_is_fresh(tmp_path):
    target = tmp_path / "explore.jsonl"
    with queue_lock(target):
        with pytest.raises(TimeoutError):
            with queue_lock(target, timeout=0.2):
                pass


def test_percolator_append_keeps_rows_under_concurrency(tmp_path, monkeypatch):
    """Twenty threads append through the public path; every row survives."""
    import mag.percolator as pc
    q = tmp_path / "explore.jsonl"
    q.write_text("", encoding="utf-8")
    monkeypatch.setattr(pc, "EXPLORE_QUEUE", q)
    monkeypatch.setattr(pc, "_compile_invariant",
                        lambda s, c, **kw: {"status": "novel", "invariant": "x", "count": 1,
                                            "canonical": c, "compiled": True, "fact_bus": {}})

    def worker(i):
        pc.percolate("The migration ran twice and both runs wrote the same receipt.",
                     source=f"s{i}", domain="behavioral")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    rows = [json.loads(l) for l in q.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 20, len(rows)
