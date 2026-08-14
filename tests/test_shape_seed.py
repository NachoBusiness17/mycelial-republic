"""Stateless tests for shape_seed — "all people need is the shape and the rest is inevitable."
RIB: shape_seed.v1 — seed() canonical shape (8 invariants, one root); derive() the inevitable rest
from the seed alone (same seed -> same root, no external state); verify() a node with only the shape
re-derives and confirms; give() the gift; route_shape() routes the thesis through swarm_surface.
Stateless: no disk writes, no monkeypatch of files."""
from __future__ import annotations


def test_seed_is_compact_and_stable():
    import mag.shape_seed as m
    s = m.seed()
    assert "ok" not in s  # seed is the canonical shape, not a call envelope
    assert s["n_invariants"] == 8
    assert len(s["root"]) == 64  # sha256 hex
    # determinism: same seed twice -> same root
    assert m.seed()["root"] == s["root"]


def test_derive_is_deterministic_and_sufficient():
    import mag.shape_seed as m
    d1 = m.derive()
    d2 = m.derive()
    assert d1["derived_root"] == d2["derived_root"]  # same seed -> same rest (inevitable)
    assert d1["n_surfaces"] >= 6
    # a derived subset with explicit surfaces is still stable
    d3 = m.derive(use=["a", "b"])
    d4 = m.derive(use=["a", "b"])
    assert d3["derived_root"] == d4["derived_root"]
    assert d3["n_surfaces"] == 2


def test_verify_confirms_shape_sufficiency():
    import mag.shape_seed as m
    v = m.verify()
    assert v["ok"] is True  # the invariants re-derive to the canonical root -> shape is sufficient
    assert v["canonical_seed_root"] == v["derived_invariants_root"]


def test_give_is_the_gift():
    import mag.shape_seed as m
    g = m.give()
    assert g["ok"] is True
    assert "never capture" in g["gift"]["framing"].lower()
    assert len(g["gift"]["shape"]) == 8
    assert "the rest is inevitable" in g["thesis"].lower()


def test_route_shape_uses_swarm_surface(monkeypatch):
    import mag.shape_seed as m
    import mag.swarm_surface as ss
    called = {}

    def fake_route(goal, *, surface=None, lens=None, domain=None, provider=None, model=None):
        called["goal"] = goal
        called["surface"] = surface
        return {"ok": True, "surface": surface, "anchor": "y" * 16, "task_id": "t"}

    monkeypatch.setattr(ss, "route_novel", fake_route)
    r = m.route_shape()
    assert r["ok"] is True
    assert called["surface"] == "shape-seed"
    assert "shape" in called["goal"].lower() and "inevitable" in called["goal"].lower()
