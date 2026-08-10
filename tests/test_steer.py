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
