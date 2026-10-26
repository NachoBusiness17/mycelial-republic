"""backup_brain.py — the orchestration drill must know the mosaic honestly.

The no-sacred-cows law as tests: the four named gaps stay named (the moment
someone builds one, the test flips and the spec must be updated in the same
commit); the inventory never invents an organ; drills never raise.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import tools.backup_brain as bb  # noqa: E402


def test_inventory_shape():
    rows = bb.inventory()
    assert rows, "inventory returned nothing"
    for r in rows:
        assert {"role", "name", "status", "note"} <= set(r)
        assert r["status"] in ("EXISTS", "MISSING")


def test_known_organs_exist():
    by_name = {r["name"]: r for r in bb.inventory()}
    for name in ("WAL task queue", "body router", "verkle lattice",
                 "local ollama battery", "tesuji corpus", "checkpoints"):
        assert by_name[name]["status"] == "EXISTS", name


def test_named_gaps_stay_named():
    """The four handwaved organs. Flipping one of these to EXISTS is a spec
    event: the same commit must update the crosswalk doc."""
    missing = {r["name"] for r in bb.inventory() if r["status"] == "MISSING"}
    assert {"SEVERED-mode consumer", "knot proof CLI",
            "tails settlement ledger", "gold anchor"} <= missing


def test_report_names_the_loop():
    md = bb.report_md()
    for role in ("inference", "memory", "queue", "sync", "settlement", "face"):
        assert "## " + role in md
    assert "missing organs" in md


def test_chain_tip_shape():
    tip = bb.chain_tip()
    assert "tip" in tip and "n_new" in tip


def test_local_brain_probe_never_raises():
    out = bb.local_brain_probe(timeout=1.0)
    assert set(out) >= {"ollama", "models"}


def test_severed_drill_writes_ledger(tmp_path, monkeypatch):
    monkeypatch.setattr(bb, "DRILL_LOG", tmp_path / "drill.jsonl")
    res = bb.drill_severed()
    assert res["drill"] == "severed" and "verdict" in res
    lines = (tmp_path / "drill.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["verdict"] == res["verdict"]
