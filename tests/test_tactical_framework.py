"""tests for tactical_framework — see the entire framework as tactical (STRATEGY -> OPERATIONS ->
TACTICS -> LOGISTICS -> INTELLIGENCE -> COMMAND); if a subsystem can't be stated tactically, it's
impractical.

RIB (frozen spec):
  war_map()            -> the whole framework as tactical layers.
  strategic_objective()-> why we fight (the moonshot destination).
  tactical_layer(name) -> examine one layer (what it advances, against what, at what cost).
  impractical_audit()  -> find subsystems that are defined but not advancing an objective.

Contract: reuses self_steal + coordination + arena_strategies; the law = tactical or impractical.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import tactical_framework  # noqa: E402


def test_war_map_layers():
    m = tactical_framework.war_map()
    assert m["ok"] is True
    layers = [l["layer"] for l in m["layers"]]
    assert "STRATEGY" in layers and "OPERATIONS" in layers and "TACTICS" in layers
    assert "LOGISTICS" in layers and "INTELLIGENCE" in layers and "COMMAND" in layers


def test_strategic_objective():
    o = tactical_framework.strategic_objective()
    assert o["ok"] is True
    assert "republic" in o["objective"].lower() or "mycelial" in o["objective"].lower()


def test_tactical_layer_known_and_unknown():
    r = tactical_framework.tactical_layer("TACTICS")
    assert r["ok"] is True
    assert "subsystems" in r  # the concrete subsystems of the layer
    bad = tactical_framework.tactical_layer("NOT-A-LAYER")
    assert bad["ok"] is False  # honest error


def test_impractical_audit_reports():
    a = tactical_framework.impractical_audit()
    assert a["ok"] is True
    assert "n_underutilized" in a or "audit_error" in a
