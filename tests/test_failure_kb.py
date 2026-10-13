"""Tests for mag.failure_kb — dedupe, query, auto-draft remedy."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import failure_kb as fkb


@pytest.fixture(autouse=True)
def _isolate_fkb(tmp_path, monkeypatch):
    log_path = tmp_path / "failure_kb.jsonl"
    index_path = tmp_path / "signatures.json"
    remedy_dir = tmp_path / "remedies"
    monkeypatch.setattr(fkb, "LOG_PATH", log_path)
    monkeypatch.setattr(fkb, "INDEX_PATH", index_path)
    monkeypatch.setattr(fkb, "REMEDY_DIR", remedy_dir)
    monkeypatch.setattr(fkb, "AUTO_DRAFT_THRESHOLD", 3)
    yield


def test_log_failure_dedupes_signature():
    for _ in range(2):
        fkb.log_failure(kind="tool_fail", tool="write_file", detail="missing path", error="preflight")
    idx = json.loads(fkb.INDEX_PATH.read_text(encoding="utf-8"))
    sigs = idx["signatures"]
    assert len(sigs) == 1
    only = next(iter(sigs.values()))
    assert only["count"] == 2
    assert only["tool"] == "write_file"


def test_query_by_tool():
    fkb.log_failure(kind="tool_fail", tool="write_file", detail="bad shape", error="arguments")
    fkb.log_failure(kind="tool_fail", tool="run_python", detail="too short", error="preflight")
    hits = fkb.query("shape", tool="write_file")
    assert len(hits) == 1
    assert hits[0]["tool"] == "write_file"


def test_auto_draft_remedy_on_threshold(monkeypatch):
    monkeypatch.setattr("mag.remedy.REMEDY_DIR", fkb.REMEDY_DIR)
    for _ in range(3):
        fkb.log_failure(kind="collapse", tool="grep_tool", detail="5x identical grep", error="collapse")
    idx = json.loads(fkb.INDEX_PATH.read_text(encoding="utf-8"))
    rec = next(iter(idx["signatures"].values()))
    assert rec.get("remedy_id")
    card = fkb.REMEDY_DIR / f"{rec['remedy_id']}.md"
    assert card.is_file()
    assert "grep_tool" in card.read_text(encoding="utf-8")


def test_surface_hits_skips_single_occurrence():
    fkb.log_failure(kind="tool_fail", tool="write_file", detail="once", error="x")
    hits = fkb.surface_hits(goal="implement write_file patch")
    assert hits == []


def test_surface_hits_includes_recurring():
    for _ in range(3):
        fkb.log_failure(kind="tool_fail", tool="write_file", detail="missing path", error="preflight")
    hits = fkb.surface_hits(goal="write_file", limit=2)
    assert len(hits) == 1
    assert hits[0]["source"] == "failure_kb"
    assert "×3" in hits[0]["tip"]


def test_format_block_nonempty():
    for _ in range(2):
        fkb.log_failure(kind="tool_fail", tool="write_file", detail="x", error="y")
    recs = fkb.query("write_file", limit=1)
    block = fkb.format_block(recs)
    assert "FAILURE KB" in block


def test_rebuild_index_restores_counts_after_reset_and_writes_receipt():
    # B2-87 continuity pin: the log is authoritative across an index reset.
    for _ in range(4):
        fkb.log_failure(kind="tool_fail", tool="run_shell", detail="backend reported failure", error="backend reported failure")
    fkb.log_failure(kind="tool_fail", tool="write_file", detail="once", error="once")
    recurring_sig = fkb.signature_key(tool="run_shell", error="backend reported failure", detail="backend reported failure")
    singleton_sig = fkb.signature_key(tool="write_file", error="once", detail="once")
    # Simulate the 2026-09-22T14:54 reset: index zeroed, log untouched.
    fkb._save_index({"schema": "failure_kb.signatures.v1", "signatures": {}})
    receipt = fkb.rebuild_index(reason="test reset recovery", actor="B2-87")
    idx = json.loads(fkb.INDEX_PATH.read_text(encoding="utf-8"))
    assert idx["signatures"][recurring_sig]["count"] == 4
    assert receipt["total_count_before"] == 0
    assert receipt["total_count_after"] == 4
    assert receipt["signatures_after"] == 1
    assert receipt["log_rows_parsed"] == 5
    assert receipt["reason"] == "test reset recovery"
    assert idx["rebuild_receipt"]["ts"] == receipt["ts"]
    # Singleton policy: count-1 sigs stay log-only under min_count=2.
    assert singleton_sig not in idx["signatures"]
    # First/last seen come from log timestamps, not the rebuild moment.
    rec = idx["signatures"][recurring_sig]
    assert rec["first_seen"] <= rec["last_seen"]
    assert rec["error_sample"] == "backend reported failure"


def test_rebuild_preserves_remedy_and_chains_previous_receipt():
    sig_tool, sig_detail, sig_error = "grep_tool", "5x identical grep", "collapse"
    for _ in range(3):
        fkb.log_failure(kind="collapse", tool=sig_tool, detail=sig_detail, error=sig_error)
    first_sig = fkb.signature_key(tool=sig_tool, error=sig_error, detail=sig_detail)
    fkb.rebuild_index(reason="first rebuild", actor="B2-87")
    idx = json.loads(fkb.INDEX_PATH.read_text(encoding="utf-8"))
    assert idx["signatures"][first_sig].get("remedy_id")
    first_receipt_ts = idx["rebuild_receipt"]["ts"]
    second = fkb.rebuild_index(reason="second rebuild", actor="B2-87")
    idx2 = json.loads(fkb.INDEX_PATH.read_text(encoding="utf-8"))
    # remedy_id survives the rebuild (no mass redraft, no loss).
    assert idx2["signatures"][first_sig]["remedy_id"] == idx["signatures"][first_sig]["remedy_id"]
    # The receipt chain names what the previous rebuild did.
    assert idx2["rebuild_receipt"]["previous_rebuild_ts"] == first_receipt_ts
    assert idx2["rebuild_receipt"]["previous_rebuild_reason"] == "first rebuild"
    assert second["total_count_before"] == second["total_count_after"]


# ---- B2-362: log-tail search reaches the count-1 sigs the index hides ----

def test_search_log_finds_count1_sig_that_index_hides(tmp_path, monkeypatch):
    log = tmp_path / "failure_kb.jsonl"
    idx = tmp_path / "signatures.json"
    log.write_text(
        json.dumps({"ts": "2026-09-26T10:00:00Z", "kind": "tool_fail",
                    "tool": "widget_maker", "error": "phantom fuse blew",
                    "detail": "one-off", "sig": "aaa111"}) + "\n" +
        json.dumps({"ts": "2026-09-26T11:00:00Z", "kind": "tool_fail",
                    "tool": "other", "error": "ordinary", "detail": "x",
                    "sig": "bbb222"}) + "\n",
        encoding="utf-8")
    # the index carries only the count>=2 sig (the B2-87 law)
    idx.write_text(json.dumps({"signatures": {
        "bbb222": {"count": 2, "tool": "other"}}}), encoding="utf-8")
    monkeypatch.setattr(fkb, "LOG_PATH", log)
    monkeypatch.setattr(fkb, "INDEX_PATH", idx)
    # falsifier precondition: the index-only query cannot see the count-1 sig
    assert fkb.query("phantom fuse") == []
    r = fkb.search_log("phantom fuse")
    assert r["hits"] and r["hits"][0]["sig"] == "aaa111"
    assert r["hits"][0]["tool"] == "widget_maker"


def test_search_log_is_bounded_and_tool_filtered(tmp_path, monkeypatch):
    log = tmp_path / "failure_kb.jsonl"
    lines = [json.dumps({"ts": f"2026-09-26T{i:02d}:00:00Z", "kind": "k",
                         "tool": f"t{i}", "error": "e", "detail": "d",
                         "sig": f"s{i}"}) + "\n" for i in range(50)]
    log.write_text("".join(lines), encoding="utf-8")
    monkeypatch.setattr(fkb, "LOG_PATH", log)
    r = fkb.search_log("e", tail=10, limit=3)
    assert len(r["hits"]) == 3
    # every tail row matches, so the limit short-circuits the scan at 3;
    # the tail bound itself is proven by the read never reaching rows 41..50
    assert r["scanned"] == 3
    r2 = fkb.search_log("", tool="t7", tail=50, limit=5)
    assert len(r2["hits"]) == 1 and r2["hits"][0]["tool"] == "t7"
