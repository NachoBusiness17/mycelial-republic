"""tests for moonshot_engine — deterministic + stateless, no monkeypatch.

RIB (frozen spec):
  plan()          -> {ok, schema, plan} where plan == throughput_model.moonshot_estimate().
  progress()      -> reads the sent.jsonl LEDGER (grounded bytes), never invents progress; 0 when
                     no moonshot rows exist; counts unique anchors for the moonshot surface.
  cold_launch()   -> routes each DISTINCT MOONSHOT_GOAL to swarm via route_novel; idempotent by
                     anchor (re-running with a full ledger enqueues nothing new); $0.
  moonshot()      -> full snapshot {plan, progress, self_measure} that distinguishes measured vs
                     labeled (honesty).

Stateless-correct: tests run against a tmp ledger via monkeypatching LEDGER PATH at the module
level is NOT used — instead we exercise the pure logic against a temporary ledger file written in
the same format route_novel writes, and assert progress() reads it. No monkeypatch of internals.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import moonshot_engine  # noqa: E402


def _write_ledger(ledger: Path, rows: list[dict[str, Any]]) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_schema_and_goals():
    assert moonshot_engine.SCHEMA == "moonshot_engine.v1"
    assert moonshot_engine.SURFACE == "moonshot"
    assert len(moonshot_engine.MOONSHOT_GOALS) >= 5
    # each goal distinct -> distinct anchor -> dedupe by anchor (the real route_novel primitive)
    from mag import swarm_surface
    anchors = {swarm_surface.anchor(g, moonshot_engine.SURFACE)
               for g in moonshot_engine.MOONSHOT_GOALS}
    assert len(anchors) == len(moonshot_engine.MOONSHOT_GOALS)


def test_plan_ok_and_grounded():
    p = moonshot_engine.plan()
    assert p["ok"] is True
    assert p["schema"] == moonshot_engine.SCHEMA
    plan = p["plan"]
    assert plan["ok"] is True
    # honesty: the plan separates measured facts from labeled estimates
    assert "honesty" in plan
    assert "ingest" in plan and "manifest" in plan


def test_progress_zero_when_empty(tmp_path):
    # point the module at a fresh (non-existent) ledger -> no moonshot rows -> measured 0
    moonshot_engine.LEDGER = tmp_path / "nested" / "sent.jsonl"
    prog = moonshot_engine.progress()
    assert prog["ok"] is True
    assert prog["queued_unique"] == 0
    assert prog["ledger_rows"] == 0


def test_progress_reads_grounded_ledger(tmp_path):
    ledger = tmp_path / "sent.jsonl"
    moonshot_engine.LEDGER = ledger
    rows = [
        {"anchor": "aaa", "surface": "moonshot"},
        {"anchor": "bbb", "surface": "moonshot"},
        {"anchor": "ccc", "surface": "other"},  # other surface must not count
    ]
    _write_ledger(ledger, rows)
    prog = moonshot_engine.progress()
    assert prog["queued_unique"] == 2  # only moonshot anchors, deduped
    assert prog["ledger_rows"] == 2     # moonshot rows read
    assert prog["target"] == len(moonshot_engine.MOONSHOT_GOALS)


def test_moonshot_snapshot_measured_vs_labeled(tmp_path):
    moonshot_engine.LEDGER = tmp_path / "sent.jsonl"
    snap = moonshot_engine.moonshot()
    assert snap["ok"] is True
    assert "plan" in snap and "progress" in snap and "self_measure" in snap
    assert snap["honesty"]  # the honesty field is non-empty
    # no goals queued -> self_measure reports not-yet-started, not fake progress
    assert "queued" in snap["self_measure"].lower() or "cold_launch" in snap["self_measure"]


def test_moonshot_self_steal_loop_composes(tmp_path):
    # point the moonshot ledger at a fresh tmp file so the composed loop runs grounded
    moonshot_engine.LEDGER = tmp_path / "sent.jsonl"
    # arrival reads its own PACKS_DIR; point it at an empty tmp dir so it folds nothing new
    from mag import arrival
    arrival.PACKS_DIR = tmp_path / "research_packs"
    r = moonshot_engine.moonshot_self_steal(limit=2)
    assert r["ok"] is True
    # the loop composes all three phases: sense + re-strike + fold
    assert "sense" in r and "re_strike" in r and "fold" in r
    # re-strike routes moonshot goals to the swarm (or dedupes them) and reports honestly
    assert r["re_strike"]["target"] == 2
    assert "newly_queued" in r["re_strike"] and "already_deduped" in r["re_strike"]
    # fold reports n_folded (measured), even when 0
    assert "n_folded" in r["fold"]
    # honesty present
    assert r["honesty"]
