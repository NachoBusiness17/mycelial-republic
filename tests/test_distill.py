"""tests for distill — the liquid-intelligence distillation machine (sw59-62). Deterministic + $0.

RIB (frozen spec):
  lattice_invariants() -> read the 'tons of invariants' from the standing wave.
  boil(raw)            -> heat = how distinct the raw is from the invariant corpus.
  quantize(states)     -> many -> one: collapse state-hashes into a single root.
  distill(raw)         -> boil + filter through bones -> emit inference + quantization.
  trace(entry)         -> write breadcrumbs to the maze.
  cycle(raw,n)         -> top talks to bottom: converge many toward one across cycles.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import distill as d  # noqa: E402


def test_lattice_invariants_present():
    inv = d.lattice_invariants()
    assert isinstance(inv, list) and len(inv) > 0


def test_boil_steam_heat():
    b = d.boil("some raw datum")
    assert b["state"] == "steam" and b["heat"] >= 0
    assert b["n_invariants"] > 0 and b["lattice_root"]


def test_quantize_many_to_one():
    q = d.quantize(["a", "b", "c", "d"])
    assert q["state"] == "one" and q["n"] == 4 and len(q["root"]) == 16
    # deterministic: same inputs -> same root
    assert d.quantize(["a", "b", "c", "d"])["root"] == q["root"]


def test_distill_emits_inference_and_root():
    r = d.distill("the liquid rises")
    assert r["state"] == "distilled"
    assert r["inference"].startswith("many -> one")
    assert len(r["quantize"]["root"]) == 16


def test_cycle_converges_and_traces():
    c = d.cycle("seed", n=2)
    assert c["ok"] is True and c["n"] == 2
    assert c["converged_root"]
    for s in c["steps"]:
        assert s["trace"]["ok"] is True
