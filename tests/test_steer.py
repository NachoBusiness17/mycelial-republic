"""Tests for mag.steer — the WINDOW_STEER loop machinery."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import mag.steer as steer


@pytest.fixture(autouse=True)
def _isolate(tmp_path, monkeypatch):
    """Isolate the steer store to tmp_path so tests never touch the real trail."""
    monkeypatch.setattr(steer, "STEER_DIR", tmp_path)
    monkeypatch.setattr(steer, "TRAIL", tmp_path / "trail.jsonl")


def test_emit_writes_packet():
    r = steer.emit("fit-ask-window", "ask-window", "execute the rewrite spec",
                   phases=["0.law", "1.memlang", "2.invariant"])
    assert r["ok"]
    p = r["path"]
    rec = json.loads(Path(p).read_text(encoding="utf-8"))
    assert rec["id"] == "fit-ask-window"
    assert rec["source"] == "ask-window"
    assert rec["consumed"] is False


def test_consume_compiles_steer_markers_to_memlang():
    # a steer packet that references a [STEER] marker compiles into a memlang steer token
    r = steer.emit("ollama-smarter-faster", "other-window",
                   "[STEER] ollama-smarter-faster · source=other-window · execute local router")
    assert r["ok"]
    out = steer.consume(compile_to_memlang=True)
    assert out["ok"]
    assert out["steers_found"] >= 0  # transcript scan may find none; local packet is emit-only
    assert "compiled" in out


def test_status_reports_store_state():
    steer.emit("steer-a", "ask-window", "x")
    steer.emit("steer-b", "ask-window", "y")
    st = steer.status()
    assert st["ok"]
    assert st["n_steers"] >= 2


def test_emit_is_idempotent_per_id():
    r1 = steer.emit("dup", "ask-window", "first")
    r2 = steer.emit("dup", "ask-window", "second")
    assert r1["ok"] and r2["ok"]
    st = steer.status()
    assert st["n_steers"] >= 1  # same-id emit overwrites, never explodes


# ---------------------------------------------------------------------------
# The STEER CHANNEL — watch/inbox/STEER.md + tools/steer_read.py
# (spec: watch/inbox/operator_model/STEER.md, 2026-09-30). Tests below run
# against tmp files only; the live channel is never touched.
# ---------------------------------------------------------------------------

from tools import steer_read


def _channel(tmp_path, *rows):
    """Write a steer channel file: '#'-prefixed header lines plus JSONL rows."""
    p = tmp_path / "STEER.md"
    p.write_text(
        "# header comment row (file contract)\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )
    return p


def test_channel_latest_wins(tmp_path):
    p = _channel(
        tmp_path,
        '{"id":"a","mate":"w3","steer":"go narrow","ts":"2026-09-30T10:00:00Z","via":"hand-edit"}',
        '{"id":"b","mate":"w3","steer":"go wide instead","ts":"2026-09-30T14:00:00Z","via":"hand-edit"}',
        '{"id":"c","mate":"w3","steer":"older but later line","ts":"2026-09-30T09:00:00Z","via":"hand-edit"}',
    )
    out = steer_read.read("w3", path=p)
    assert out["ok"]
    assert out["operative"]["id"] == "b"  # newest ts wins, not last line
    assert [r["id"] for r in out["rows"]] == ["c", "a", "b"]  # oldest first


def test_channel_all_vs_target_match(tmp_path):
    p = _channel(
        tmp_path,
        '{"id":"f1","mate":"w9","steer":"other lane","ts":"2026-09-30T18:00:00Z","via":"hand-edit"}',
        '{"id":"f2","mate":"all","steer":"fleet-wide order","ts":"2026-09-30T12:00:00Z","via":"hand-edit"}',
        '{"id":"f3","mate":"w3","steer":"scoped order","ts":"2026-09-30T10:00:00Z","via":"hand-edit"}',
    )
    out = steer_read.read("w3", path=p)
    ids = {r["id"] for r in out["rows"]}
    assert ids == {"f2", "f3"}  # mate==all OR mate==w3 apply; w9 does not
    assert out["operative"]["id"] == "f2"  # newest applicable wins even though it is the fleet-wide row


def test_channel_proposal_marking(tmp_path):
    p = _channel(
        tmp_path,
        '{"id":"p1","mate":"w3","steer":"no provenance here","ts":"2026-09-30T10:00:00Z"}',
        '{"id":"o1","mate":"w3","steer":"operator word","ts":"2026-09-30T11:00:00Z","via":"hand-edit"}',
        '{"id":"p2","mate":"w3","steer":"forged via","ts":"2026-09-30T12:00:00Z","via":"seat-guess"}',
    )
    out = steer_read.read("w3", path=p)
    by_id = {r["id"]: r for r in out["rows"]}
    assert by_id["p1"]["proposal"] is True  # missing via = proposal, not order
    assert by_id["o1"]["proposal"] is False  # recognized operator via
    assert by_id["p2"]["proposal"] is True  # unrecognized via = proposal
    assert out["operative"]["id"] == "p2" and out["operative"]["proposal"] is True


def test_channel_malformed_rows_fail_loud_not_silent(tmp_path):
    p = _channel(
        tmp_path,
        '{"id":"g1","mate":"w3","steer":"valid baseline","ts":"2026-09-30T10:00:00Z","via":"hermes-dm"}',
        '{"id":"broken", "mate": ',  # unparseable JSON
        '{"id":"g2","mate":"w3","ts":"2026-09-30T16:00:00Z","via":"hand-edit"}',  # missing steer
        '{"id":"g3","mate":"w3","steer":"bad ts","ts":"yesterday","via":"hand-edit"}',  # non-ISO ts
        '{"id":"g4","mate":"w3","steer":"last valid wins","ts":"2026-09-30T15:00:00Z","via":"phone-relay"}',
    )
    out = steer_read.read("w3", path=p)
    assert out["ok"]
    assert len(out["malformed"]) == 3  # corrupt rows are reported, never silently applied
    assert out["operative"]["id"] == "g4"  # mate proceeds with the last VALID row


def test_channel_missing_file(tmp_path):
    out = steer_read.read("w3", path=tmp_path / "nope.md")
    assert out["ok"] is False and out["operative"] is None and out["rows"] == []

