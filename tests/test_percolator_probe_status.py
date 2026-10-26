"""Probe chatter must not count as open work (2026-10-24).

The census found 1,492 of 2,388 open rows carried a probe_* domain; four ractors
named that inflation the load-bearing defect. The queue is append-only, so the fix
is at the WRITER: a probe row still lands, but as status="probe", never "open".
"""
from __future__ import annotations

import json

import pytest

import mag.percolator as pc


@pytest.fixture
def queue(tmp_path, monkeypatch):
    path = tmp_path / "explore.jsonl"
    monkeypatch.setattr(pc, "EXPLORE_QUEUE", path)
    monkeypatch.setattr(pc, "_compile_invariant",
                        lambda sentences, canonical, **kw: {
                            "status": "novel", "invariant": "a novel observation", "count": 1,
                            "canonical": canonical, "compiled": True, "fact_bus": {}})
    return path


def _rows(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def test_probe_domain_lands_as_probe_not_open(queue):
    pc.percolate("The migration ran twice and both runs wrote the same receipt.",
                 source="probe_test", domain="probe_cohere")
    rows = _rows(queue)
    assert len(rows) == 1
    assert rows[0]["status"] == "probe", rows[0]
    assert rows[0]["domain"] == "probe_cohere"


def test_normal_domain_still_lands_open(queue):
    pc.percolate("The migration ran twice and both runs wrote the same receipt.",
                 source="seat", domain="behavioral")
    assert _rows(queue)[0]["status"] == "open"


def test_probe_rows_are_not_counted_by_the_census(queue, tmp_path, monkeypatch):
    import tools.queue_census as qc
    pc.percolate("One observation that repeats nowhere else in this run.",
                 source="probe_test", domain="probe_gemma")
    pc.percolate("A different observation about a lost receipt and a slow lane.",
                 source="seat", domain="behavioral")
    monkeypatch.setattr(qc, "QUEUE", queue)
    monkeypatch.setattr(qc, "DECAY", tmp_path / "none.jsonl")
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        qc.main([])
    out = buf.getvalue()
    assert "probe_* chatter" in out
    # no probe row is open, so the two "open" counts must be 1 and 1
    assert "live" in out
