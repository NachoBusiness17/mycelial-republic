"""Stateless tests for sovereign_handshake — the connection layer between sovereign systems.
RIB: sovereign_handshake.v1 — advertise (willful, deduped, verified-only-by-running), discover
(grounded web), handshake (both participate, never capture, deduped), web (mesh not hierarchy),
connect (routes through swarm_surface.route_novel). Stateless: tmp_path, no monkeypatch."""
from __future__ import annotations

import json


def test_advertise_willful_and_deduped(tmp_path, monkeypatch):
    import mag.sovereign_handshake as m
    monkeypatch.setattr(m, "CONNECT_DIR", tmp_path)
    monkeypatch.setattr(m, "PEERS", tmp_path / "peers.jsonl")
    monkeypatch.setattr(m, "LINKS", tmp_path / "links.jsonl")
    r1 = m.advertise("rep", values=["sovereign"])
    assert r1["ok"] and r1["deduped"] is False
    assert r1["peer"]["verified"] is False  # never verified on self-report
    r2 = m.advertise("rep", values=["sovereign"])
    assert r2["ok"] and r2["deduped"] is True  # content-addressed -> idempotent


def test_discover_reads_grounded_web(tmp_path, monkeypatch):
    import mag.sovereign_handshake as m
    monkeypatch.setattr(m, "CONNECT_DIR", tmp_path)
    monkeypatch.setattr(m, "PEERS", tmp_path / "peers.jsonl")
    monkeypatch.setattr(m, "LINKS", tmp_path / "links.jsonl")
    m.advertise("alpha")
    m.advertise("beta")
    d = m.discover()
    assert d["ok"] and d["n_peers"] >= 2
    systems = [p.get("system") for p in d["peers"] if isinstance(p, dict) and p.get("system")]
    assert "alpha" in systems and "beta" in systems


def test_handshake_willful_and_deduped(tmp_path, monkeypatch):
    import mag.sovereign_handshake as m
    monkeypatch.setattr(m, "CONNECT_DIR", tmp_path)
    monkeypatch.setattr(m, "PEERS", tmp_path / "peers.jsonl")
    monkeypatch.setattr(m, "LINKS", tmp_path / "links.jsonl")
    r1 = m.handshake("alpha", "beta")
    assert r1["ok"] and r1["deduped"] is False
    assert "NONE" in r1["connection"]["capture"].upper()  # never capture
    r2 = m.handshake("beta", "alpha")
    assert r2["ok"] and r2["deduped"] is True  # ordered pair dedupes regardless of direction
    bad = m.handshake("alpha", "alpha")
    assert bad["ok"] is False  # no self-handshake


def test_web_is_mesh_not_hierarchy(tmp_path, monkeypatch):
    import mag.sovereign_handshake as m
    monkeypatch.setattr(m, "CONNECT_DIR", tmp_path)
    monkeypatch.setattr(m, "PEERS", tmp_path / "peers.jsonl")
    monkeypatch.setattr(m, "LINKS", tmp_path / "links.jsonl")
    m.advertise("alpha")
    m.advertise("beta")
    m.advertise("gamma")
    m.handshake("alpha", "beta")
    w = m.web()
    assert w["ok"] and w["n_peers"] == 3 and w["n_links"] == 1
    assert "mesh" in w["structure"].lower()  # no root, no owner, no gatekeeper


def test_connect_routes_through_swarm_surface(tmp_path, monkeypatch):
    import mag.sovereign_handshake as m
    import mag.swarm_surface as ss
    called = {}

    def fake_route(goal, *, surface=None, lens=None, domain=None, provider=None, model=None):
        called["goal"] = goal
        called["surface"] = surface
        return {"ok": True, "surface": surface, "anchor": "x" * 16, "task_id": "t"}

    monkeypatch.setattr(ss, "route_novel", fake_route)
    r = m.connect()
    assert r["ok"] is True
    assert called["surface"] == "sovereign-connect"
    assert "metaverse" in called["goal"].lower() and "corpo" in called["goal"].lower()
