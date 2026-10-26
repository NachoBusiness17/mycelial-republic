"""The explore queue has two writers; the rewrite must never truncate it.

percolator appends (status=open/probe); fuel_feed.clarify rewrites the file when it
merges repeats. Before 2026-10-24 that rewrite was a plain write_text - a crash
mid-write left a truncated queue, and a concurrent append could be lost.
"""
from __future__ import annotations

import json

import mag.fuel_feed as ff


def test_write_explore_is_atomic_and_leaves_no_temp(tmp_path, monkeypatch):
    q = tmp_path / "explore.jsonl"
    q.write_text('{"old": true}\n', encoding="utf-8")
    monkeypatch.setattr(ff, "EXPLORE_QUEUE", q)
    rows = [{"ts": "t1", "status": "open"}, {"ts": "t2", "status": "probe"}]
    ff._write_explore(rows)
    got = [json.loads(l) for l in q.read_text(encoding="utf-8").splitlines()]
    assert got == rows
    leftovers = [p.name for p in tmp_path.iterdir() if ".tmp" in p.name]
    assert leftovers == [], leftovers


def test_write_explore_handles_empty(tmp_path, monkeypatch):
    q = tmp_path / "explore.jsonl"
    q.write_text('{"old": true}\n', encoding="utf-8")
    monkeypatch.setattr(ff, "EXPLORE_QUEUE", q)
    ff._write_explore([])
    assert q.read_text(encoding="utf-8") == ""
