"""Tests for mag.verkle_audit — deterministic audit + ticket reconcile."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mag.verkle_audit import reconcile_tickets, run_audit, verkle_gaps


def test_verkle_gaps_returns_list():
    gaps = verkle_gaps()
    assert isinstance(gaps, list)
    for g in gaps:
        assert "kind" in g
        assert "detail" in g


def test_reconcile_tickets_schema():
    out = reconcile_tickets()
    assert out.get("ok") is True
    assert out.get("schema") == "tickets_reconcile.v1"
    assert "open" in out
    assert "counts" in out
    assert isinstance(out["counts"].get("open"), int)


def test_run_audit_dry_no_write(tmp_path, monkeypatch):
    monkeypatch.setattr("mag.verkle_audit.DAILY", tmp_path / "daily")
    res = run_audit(full=False, synth=False, reconcile=True, dry=True)
    assert res.get("ok") is True
    assert res.get("schema") == "verkle_audit.v1"
    assert "gaps" in res
    assert "reconcile" in res
    assert res.get("dry") is True
    assert "report_path" not in res


def test_run_audit_writes_report(tmp_path, monkeypatch):
    monkeypatch.setattr("mag.verkle_audit.DAILY", tmp_path / "daily")
    res = run_audit(full=False, synth=False, reconcile=False, dry=False)
    assert res.get("ok") is True
    assert "report_path" in res
    report = tmp_path / "daily"
    files = list(report.glob("*-verkle-audit.json"))
    assert len(files) == 1
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data.get("schema") == "verkle_audit.v1"


def test_tip_repair_does_not_rewrite_verified_chain(tmp_path, monkeypatch):
    from mag import verkle_knot as vk

    chain = tmp_path / "verkle_chain.jsonl"
    tip = tmp_path / "verkle_tip.json"
    knots = tmp_path / "knots"
    knots.mkdir()
    monkeypatch.setattr(vk, "CHAIN", chain)
    monkeypatch.setattr(vk, "TIP", tip)
    monkeypatch.setattr(vk, "KNOTS", knots)
    monkeypatch.setattr(vk, "LATEST", tmp_path / "latest.knot.json")
    monkeypatch.setattr(vk, "LOCK", tmp_path / ".verkle.lock")
    leaves = ["leaf-a", "leaf-b"]
    root = vk._merkle_root(leaves)
    rows = [
        {"index": 0, "leaf_hash": leaves[0], "verkle_root": leaves[0], "session_id": "a",
         "filename": "old.knot.json"},
        {"index": 1, "leaf_hash": leaves[1], "verkle_root": root, "session_id": "b",
         "filename": "tail.knot.json", "end_minute": "2026-09-26T00:36:00Z"},
    ]
    chain.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    tip.write_text(json.dumps({
        "root": "stale", "n_leaves": 2, "last_filename": "old.knot.json",
        "last_session_id": "a",
    }), encoding="utf-8")
    (knots / "tail.knot.json").write_text('{"session_id":"b"}', encoding="utf-8")
    before = chain.read_bytes()

    result = vk.repair_tip_if_consistent()

    assert result["ok"] is True
    assert result["repaired"] is True
    repaired = json.loads(tip.read_text(encoding="utf-8"))
    assert repaired["root"] == root
    assert repaired["last_filename"] == "tail.knot.json"
    assert repaired["last_session_id"] == "b"
    assert repaired["updated_minute"] == "2026-09-26T00:36:00Z"
    assert (tmp_path / "latest.knot.json").read_text(encoding="utf-8") == '{"session_id":"b"}'
    assert chain.read_bytes() == before
