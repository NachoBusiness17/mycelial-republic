"""tests for route_trace — the deterministic route-provenance debugger (billion-scale 'where did
they go from').

RIB (frozen spec):
  hop(who,what,from,to)  -> record + fold one route hop as a content-addressed knot (game_world).
                            Idempotent: same hop -> same key -> never duplicates.
  trace(who)             -> the deterministic 'where did they go from': verkle_lance temporal map +
                            recorded hops from game_world. $0, no inference.
  origin(who)            -> the deepest parent: source_trace (if pid) or earliest hop (person).
  status()               -> contract + scaling rationale.

Contract: reuses verkle_lance + source_trace + game_world — no invention. Content-addressed hops +
temporal parent chain = a billion routes traceable by walking parents.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import route_trace  # noqa: E402


def test_hop_records_idempotent(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    r1 = route_trace.hop(who="alice", what="enter", frm="gate", to="spire")
    assert r1["ok"] is True
    assert r1["recorded"] is True
    assert r1["from"] == "gate" and r1["to"] == "spire"
    # same hop again -> deduped (idempotent)
    r2 = route_trace.hop(who="alice", what="enter", frm="gate", to="spire")
    assert r2["deduped"] is True
    assert r2["recorded"] is False


def test_hop_requires_who_and_what():
    r = route_trace.hop(who="", what="", frm="", to="")
    assert r["ok"] is False


def test_trace_reports_route(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    route_trace.hop(who="bob", what="walk", frm="gate", to="seam")
    route_trace.hop(who="bob", what="survey", frm="seam", to="castle")
    t = route_trace.trace("bob")
    assert t["ok"] is True
    assert t["n_hops"] >= 2
    assert "route" in t  # the deterministic path
    # the route reflects the hops
    assert any(h.get("to") == "castle" for h in t["route"])


def test_origin_earliest_hop(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    route_trace.hop(who="carol", what="first", frm="genesis", to="mid")
    route_trace.hop(who="carol", what="second", frm="mid", to="end")
    o = route_trace.origin("carol")
    assert o["ok"] is True
    assert "origin" in o  # earliest hop = the origin


def test_status_contract():
    s = route_trace.status()
    assert s["ok"] is True
    assert "hop" in s["contract"] and "trace" in s["contract"]
    assert "scales" in s  # the billion-scale rationale
