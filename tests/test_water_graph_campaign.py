"""Graph-mode campaign tests — water:graph spec routes the keep through the
real pipe network (mag/water_graph.py). Legacy 3-tank path must stay the
regression floor: no spec in flags -> untouched behavior.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.game_campaign import (  # noqa: E402
    apply_action,
    begin_play,
    load_campaign,
    parse_character,
    parse_player_speech,
    save_campaign,
    set_character,
)
from mag.water_computer import (  # noqa: E402
    cheated,
    default_graph_spec,
    graph_spec,
    heights,
    seed_graph,
    sight_glass,
    won,
)


def _boot_graph(spec=None) -> str:
    b = begin_play(module_id="water_computer", voice_session_id="pytest-water-graph", force_new=True)
    cid = str(b.get("campaign_id") or (b.get("campaign") or {}).get("campaign_id") or "")
    if b.get("need_character"):
        set_character(cid, parse_character("I'm Ash a curious engineer"))
    camp = load_campaign(cid) or {}
    seed_graph(camp, spec if spec is not None else default_graph_spec())
    save_campaign(camp)
    return cid


def _boot_legacy() -> str:
    b = begin_play(module_id="water_computer", voice_session_id="pytest-water-legacy", force_new=True)
    cid = str(b.get("campaign_id") or (b.get("campaign") or {}).get("campaign_id") or "")
    if b.get("need_character"):
        set_character(cid, parse_character("I'm Ash a curious engineer"))
    return cid


def _do(cid: str, line: str):
    act = parse_player_speech(line) or {"type": "look"}
    return apply_action(cid, act)


def _g(cid: str):
    return graph_spec(load_campaign(cid) or {})


def test_seed_graph_roundtrip_and_mode_flip():
    cid = _boot_graph()
    spec0 = default_graph_spec()
    got = _g(cid)
    assert got == spec0, "spec must survive the flag JSON roundtrip"
    glass = sight_glass(load_campaign(cid))
    assert "GLASS" in glass
    assert "JUNCTION" in glass, "graph glass shows the network, not the 3 tanks"


def test_wait_runs_graph_ticks_and_persists():
    cid = _boot_graph()
    assert _do(cid, "go west").get("ok")
    assert _do(cid, "open valve").get("ok")
    spec = _g(cid)
    assert spec["pipes"]["main"]["open"] is True
    t0 = spec["tick"]
    r = _do(cid, "wait")
    assert r.get("ok"), r
    spec = _g(cid)
    assert spec["tick"] == t0 + 1, "wait must run exactly one graph tick"
    assert spec["nodes"]["source"]["volume"] == 5
    assert spec["nodes"]["junction"]["volume"] == 0, "XOR passed it straight through"
    assert spec["nodes"]["out"]["volume"] == 1
    # persisted on disk, not just in the returned dict
    fresh = graph_spec(load_campaign(cid))
    assert fresh["tick"] == t0 + 1


def test_close_valve_stops_flow():
    cid = _boot_graph()
    _do(cid, "go west")
    _do(cid, "open valve")
    _do(cid, "wait")
    _do(cid, "close valve")
    spec = _g(cid)
    assert spec["pipes"]["main"]["open"] is False
    out0 = spec["nodes"]["out"]["volume"]
    _do(cid, "wait")
    spec = _g(cid)
    assert spec["nodes"]["out"]["volume"] == out0, "closed pipe must move nothing"


def test_room_pipe_map_contract():
    cid = _boot_graph()
    # gallery maps to the side feed (spec["valves"]), not to main
    _do(cid, "open valve")
    spec = _g(cid)
    assert spec["pipes"]["side"]["open"] is True
    assert spec["pipes"]["main"]["open"] is False
    _do(cid, "close valve")
    spec = _g(cid)
    assert spec["pipes"]["side"]["open"] is False


def test_xor_gates_flow_one_inlet_passes_two_overflow():
    cid = _boot_graph()
    _do(cid, "go west")
    _do(cid, "open valve")   # main: source -> junction
    _do(cid, "go east")      # gallery
    _do(cid, "open valve")   # side: reservoir -> junction
    _do(cid, "wait")         # both inlets -> XOR refuses
    spec = _g(cid)
    assert spec["nodes"]["out"]["volume"] == 0, "XOR: both inlets -> no delivery"
    # STARVATION LAW (2026-09-28): refused inflow now POOLS at the junction
    # (a real gate holds water) instead of vanishing to waste; the old
    # "refused inflow stays in source" semantics is what the law replaced.
    assert spec["nodes"]["junction"]["volume"] == 2
    assert spec["nodes"]["source"]["volume"] == 5  # traced: main pipe cap drew 1
    _do(cid, "close valve")  # side shut
    _do(cid, "wait")         # sole inlet passes: pooled 2 flow out; this
                             # tick's fresh inflow pools anew (traced live:
                             # out=2, jx=1 pooling toward the next pass)
    spec = _g(cid)
    assert spec["nodes"]["out"]["volume"] == 2
    assert spec["nodes"]["junction"]["volume"] == 1


def test_graph_flow_wins_honestly():
    cid = _boot_graph()
    for line in ("go west", "open valve", "wait", "wait"):
        r = _do(cid, line)
        assert r.get("ok"), (line, r.get("error"))
    camp = load_campaign(cid)
    assert not cheated(camp)
    assert won(camp), "gravity through the network to OUT is a real win"
    assert heights(camp)["out"] >= 2


def test_unmapped_room_has_no_valve():
    spec = default_graph_spec()
    spec.pop("valves")
    cid = _boot_graph(spec)
    r = _do(cid, "open valve")
    assert r.get("ok") is False
    assert "valve" in str(r.get("error") or "").lower()


def test_valve_on_burst_pipe_names_the_burst():
    """Valve-honesty law (2026-10-10, receipt receipt_20261010_mariner.md;
    cycle 1 finding 4 probed the lie here: "Valve main open." while main
    stayed shut). A valve verb on a fractured pipe must word the burst,
    change nothing, and save nothing."""
    cid = _boot_graph()
    camp = load_campaign(cid)
    camp["room_id"] = "source_cistern"
    spec = graph_spec(camp)
    spec["pipes"]["main"]["fractured"] = True   # the AJ4-feeder end state
    seed_graph(camp, spec)
    save_campaign(camp)
    r = _do(cid, "open valve")
    assert r.get("ok"), r
    text = " | ".join(str(e) for e in (r.get("events") or []))
    assert "Valve main spins free; the pipe is burst (closed for good)." in text
    assert "Valve main open." not in text, "the hash-chain lie must stay dead"
    fresh = _g(cid)
    assert fresh["pipes"]["main"]["open"] is False
    assert fresh["pipes"]["main"]["fractured"] is True


def test_legacy_mode_untouched_without_spec():
    cid = _boot_legacy()
    assert graph_spec(load_campaign(cid)) is None
    assert _do(cid, "go west").get("ok")
    assert _do(cid, "open valve").get("ok")
    before = heights(load_campaign(cid))
    assert _do(cid, "wait").get("ok")
    after = heights(load_campaign(cid))
    assert after["source"] == before["source"] - 1
    assert after["work"] == before["work"] + 1
    assert "SOURCE" in sight_glass(load_campaign(cid)), "legacy glass in legacy mode"


def test_water_graph_module_id_loads_graph_mode():
    """resolve_module('water_graph') + begin_play auto-seeds water:graph spec."""
    from mag.game_campaign import apply_action, begin_play, load_campaign, parse_player_speech, set_character  # noqa: E402
    from mag.water_computer import graph_spec, heights  # noqa: E402

    b = begin_play(module_id="water_graph", voice_session_id="pytest-water-graph-mod", force_new=True)
    assert b.get("ok"), b
    cid = str(b.get("campaign_id") or (b.get("campaign") or {}).get("campaign_id") or "")
    if b.get("need_character"):
        set_character(cid, parse_character("I'm Ash a curious engineer"))

    camp = load_campaign(cid) or {}
    # Graph mode auto-seeded: water:graph flag present, spec matches default
    gs = graph_spec(camp)
    assert gs is not None, "water_graph module must auto-seed water:graph spec"
    assert set(gs["nodes"]) == {"source", "reservoir", "junction", "out", "waste"}
    assert gs["valves"]["source_cistern"] == "main"
    assert gs["valves"]["gallery"] == "side"
    assert gs["valves"]["work_gallery"] == "spout"
    assert gs["valves"]["out_cistern"] == "drain"

    # Room: source_cistern, open the main valve, wait — out volume must grow
    camp["room_id"] = "source_cistern"
    save_campaign(camp)
    r = apply_action(cid, parse_player_speech("open valve") or {"type": "look"})
    assert r.get("ok"), r
    r = apply_action(cid, parse_player_speech("wait") or {"type": "look"})
    assert r.get("ok"), r
    after = heights(load_campaign(cid) or {})
    assert after["out"] > 0, f"out volume must grow after open+wait, got {after}"
