"""Stateless tests for mag.water_swarm — instruct the swarms to be water (deterministic + $0)."""
from __future__ import annotations

from mag.water_swarm import flow, invariant_lattice, water_doctrine


def test_invariant_lattice_deterministic_bones():
    lat = invariant_lattice()
    assert isinstance(lat, list)
    assert all("kind" in i and "id" in i for i in lat)


def test_water_doctrine_present():
    d = water_doctrine()
    assert "be water" in d.lower() or "WATER" in d
    assert "FLOW" in d and "FORM" in d
    assert "turtles all the way down" in d


def test_flow_dry_no_spawn():
    """flow() in DRY mode (no swarm spawn) — deterministic, no shared state."""
    f = flow(enqueue=False, limit=3)
    assert f["ok"] is True
    assert f["enqueue"] is False
    assert all(r.get("dry") is True for r in f["routed"])
    assert "before detection" in f["note"]


def test_flow_doctrine_consistent():
    """The water doctrine is a stable constant (deterministic — same output each call)."""
    assert water_doctrine() == water_doctrine()
