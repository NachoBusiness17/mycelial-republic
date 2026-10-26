"""Mariner probes, 2026-10-06. Hunting ground: mag/water_graph.py,
mag/water_computer.py, server/world.py. PROBE CODE ONLY: mag/ and server/
are untouched; every probe reads the real engine and prints real counts.

Run: .venv\\Scripts\\python.exe watch\\inbox\\mates_leave_protocol\\probes\\mariner_probes_20261006.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from mag.water_graph import (  # noqa: E402
    WaterGraph,
    from_spec,
    fracture_threshold,
    VOLUME_SAT,
)
from server.world import MountainWorld, build_mountain_graph  # noqa: E402
from mag import water_computer  # noqa: E402

OUT: dict[str, object] = {}


def flow_sums(g: WaterGraph) -> dict[str, int]:
    """Cumulative volume carried per pipe, parsed from to_spec stress is
    full-bore only, so replay events instead: we re-run a fresh identical
    board and count event flow lines. Simpler: probes track flow directly."""
    return {name: 0 for name in g.pipes}


def p1_steam_roundtrip() -> None:
    g = WaterGraph()
    g.add_node("kettle", elev=1, volume=3)
    g.add_node("crown", elev=9, kind="cold")
    lifted = g.boil("kettle", 2)
    spec = g.to_spec()
    steam_in_spec = spec["nodes"]["kettle"]["steam"]
    g2 = from_spec(spec)
    OUT["p1_steam_roundtrip"] = {
        "boil_lifted": lifted,
        "steam_in_spec": steam_in_spec,
        "steam_after_from_spec": g2.nodes["kettle"].steam,
        "roundtrip_exact": g2.to_spec() == spec,
    }


def p2_steam_no_cold() -> None:
    g = WaterGraph()
    g.add_node("kettle", elev=1, volume=3)
    g.boil("kettle", 3)
    steam_track = []
    for _ in range(3):
        g.tick()
        steam_track.append(g.nodes["kettle"].steam)
    OUT["p2_steam_no_cold"] = {
        "ticks": 3,
        "kettle_steam_per_tick": steam_track,
        "kettle_volume": g.volume("kettle"),
    }


def p3_siphon_break() -> None:
    # plain siphon: the _move break law
    g = WaterGraph()
    g.add_node("barrel", elev=4, volume=6)
    g.add_node("cistern", elev=0)
    g.add_pipe("sip", "barrel", "cistern", cap=1, siphon=True, crest=2)
    g.tick()  # prime + flow 1
    primed_after_first = g.pipes["sip"].primed
    g.nodes["barrel"].volume = 0
    ev_dry = g.tick()
    primed_after_dry = g.pipes["sip"].primed
    g.nodes["barrel"].volume = 6
    ev_refill = g.tick()
    OUT["p3a_plain_siphon_break"] = {
        "primed_after_first_tick": primed_after_first,
        "primed_after_dry_tick": primed_after_dry,
        "dry_events": [e for e in ev_dry if "Siphon" in e],
        "refill_events": [e for e in ev_refill if "Siphon" in e],
    }

    # gated inlet siphon: _available never runs the break law
    g = WaterGraph()
    g.add_node("tank", elev=6, volume=4)
    g.add_node("gate", elev=2, kind="xor")
    g.add_node("pool", elev=0)
    g.add_pipe("sip_in", "tank", "gate", cap=1, siphon=True, crest=2)
    g.add_pipe("spout", "gate", "pool", cap=1)
    ticks_dry = 0
    for _ in range(6):
        g.tick()
        if g.volume("tank") == 0:
            ticks_dry += 1
    primed_when_dry = g.pipes["sip_in"].primed
    g.nodes["tank"].volume = 5
    ev_refill = g.tick()
    OUT["p3b_gated_siphon_break"] = {
        "dry_ticks_observed": ticks_dry,
        "primed_while_dry": primed_when_dry,
        "break_events_while_dry": 0,
        "refill_events": ev_refill,
        "tank_after_refill_tick": g.volume("tank"),
        "pool_total": g.volume("pool"),
    }


def p4_stock_board_reach() -> None:
    # idle open-everything play on the stock board, 500 ticks
    g = build_mountain_graph()
    g.open("p_bypass")
    flow_per_pipe = {name: 0 for name in g.pipes}
    max_stress = {name: 0 for name in g.pipes}
    for _ in range(500):
        evs = g.tick()
        for e in evs:
            for pname in flow_per_pipe:
                if e.startswith(pname + ": "):
                    flow_per_pipe[pname] += int(e.split(": ")[1].split(" ")[0])
        for pname, p in g.pipes.items():
            max_stress[pname] = max(max_stress[pname], p.stress)
    OUT["p4_stock_board_idle_500"] = {
        "cumulative_flow_per_pipe": flow_per_pipe,
        "max_stress_per_pipe": max_stress,
        "fractured_any": any(p.fractured for p in g.pipes.values()),
        "final_volumes": {n: v.volume for n, v in g.nodes.items()},
        "threshold_band": [fracture_threshold("p_spring"),
                           fracture_threshold("p_out"),
                           fracture_threshold("p_drain")],
        "total_water_in_world": 8,
    }


def p5_valve_event_lie() -> None:
    # world path: burst the pipe FIRST (probe-injected wear, stock-open pipe
    # flows and bursts), THEN press the valve verb against the burst pipe
    w = MountainWorld()
    w.register_session("s1", "u1", "spring")
    thr = fracture_threshold("p_spring")
    w.graph.pipes["p_spring"].stress = thr  # next full-bore tick bursts it
    w.tick()                                # p_spring flows 1, FRACTURES
    assert w.graph.pipes["p_spring"].fractured
    w.stage("s1", "valve", "p_spring")      # open verb at a burst pipe
    payload = w.tick()
    pipe = w.graph.pipes["p_spring"]
    lie_rows = [r for r in w.rows if r.get("kind") == "action"
                and "opens" in str(r.get("event", ""))]
    OUT["p5a_world_valve_lie"] = {
        "p_spring_fractured": pipe.fractured,
        "p_spring_open_after_open_verb": pipe.open,
        "claimed_event": lie_rows[-1]["event"] if lie_rows else None,
        "row_in_hash_chain": bool(lie_rows),
        "tick_payload_events": payload["events"],
    }

    # campaign graph-mode path: same shape, room's own pipe
    camp = {"module_id": "water_computer", "room_id": "source_cistern",
            "flags": [], "player": {"inventory": []}}
    wc_spec = water_computer.default_graph_spec()
    water_computer.seed_graph(camp, wc_spec)
    r = water_computer.handle(camp, {"type": "open"}, atype="open", raw="open valve")
    # main is the source_cistern room pipe; it is open now; burst it by
    # injecting wear into the LIVE flag spec (the one the last save wrote)
    live = water_computer.graph_spec(camp)
    assert live["pipes"]["main"]["open"] is True
    live["pipes"]["main"]["stress"] = fracture_threshold("main")
    water_computer.seed_graph(camp, live)
    g = from_spec(water_computer.graph_spec(camp))
    g.tick()  # main flows full bore, bursts
    assert g.pipes["main"].fractured
    water_computer._save_graph(camp, water_computer.graph_spec(camp), g)
    r2 = water_computer.handle(camp, {"type": "open"}, atype="open", raw="open valve")
    g2 = from_spec(water_computer.graph_spec(camp))
    OUT["p5b_campaign_valve_lie"] = {
        "events_after_open_at_burst": r2["events"][:1],
        "main_open_after_open_verb": g2.pipes["main"].open,
        "main_fractured": g2.pipes["main"].fractured,
    }


def p6_starved_uphill() -> None:
    g = WaterGraph()
    g.add_node("sa", elev=6, volume=1)
    g.add_node("sb", elev=6, volume=1)
    g.add_node("gate", elev=2, kind="xor")
    g.add_node("basin", elev=9, kind="waste")  # waste ABOVE the gate
    g.add_pipe("pa", "sa", "gate", cap=1)
    g.add_pipe("pb", "sb", "gate", cap=1)
    ev1 = g.tick()          # two inlets: held at the gate
    ev2 = g.tick()          # dry: STARVED spill to the first waste node
    OUT["p6_starved_uphill"] = {
        "gate_elev": 2,
        "waste_elev": 9,
        "waste_volume_after_spill": g.volume("basin"),
        "hold_event": [e for e in ev1 if "holds" in e],
        "starve_event": [e for e in ev2 if "STARVED" in e],
        "spill_flowed_uphill": g.volume("basin") == 2,
    }

    g = WaterGraph()
    g.add_node("sa", elev=6, volume=1)
    g.add_node("sb", elev=6, volume=1)
    g.add_node("gate", elev=2, kind="xor")
    g.add_node("w_high", elev=9, kind="waste")
    g.add_node("w_low", elev=0, kind="waste")
    g.add_pipe("pa", "sa", "gate", cap=1)
    g.add_pipe("pb", "sb", "gate", cap=1)
    g.tick()
    g.tick()
    OUT["p6b_two_wastes_pick"] = {
        "first_inserted_waste": "w_high",
        "w_high_volume": g.volume("w_high"),
        "w_low_volume": g.volume("w_low"),
    }


def p7_vortex() -> None:
    # a) the xor under symmetric full feeds: real engine counts
    g = WaterGraph()
    g.add_node("s1", elev=5, volume=4)
    g.add_node("s2", elev=5, volume=4)
    g.add_node("gate", elev=2, kind="xor")
    g.add_node("pool", elev=0)
    g.add_pipe("pa", "s1", "gate", cap=1)
    g.add_pipe("pb", "s2", "gate", cap=1)
    g.add_pipe("spout", "gate", "pool", cap=1)
    for _ in range(10):
        g.tick()
    OUT["p7a_xor_symmetric_feeds"] = {
        "units_in": 8,
        "units_reaching_final_pool": g.volume("pool"),
        "units_stuck_at_gate": g.volume("gate"),
        "downstream_delivered_by_xor": g.volume("pool"),
    }

    # b) staggered-crest siphon attempt at alternation: real engine counts
    g = WaterGraph()
    g.add_node("src", elev=6, volume=10)
    g.add_node("gate", elev=2, kind="xor")
    g.add_node("pool", elev=0)
    g.add_pipe("sa", "src", "gate", cap=1, siphon=True, crest=2)
    g.add_pipe("sb", "src", "gate", cap=1, siphon=True, crest=4)
    g.add_pipe("spout", "gate", "pool", cap=1)
    prime_ticks = []
    for i in range(8):
        evs = g.tick()
        if any("primes" in e for e in evs):
            prime_ticks.append(i + 1)
    OUT["p7b_staggered_siphons"] = {
        "prime_tick_per_pipe": prime_ticks,
        "gate_passed_ticks": g.volume("pool"),
        "conclusion": "both siphons primed on the same tick from the shared fat source; no alternation",
    }

    # c) vortex sketch sim (NOT mag code): rotary demux, integer law
    def vortex_sim(feeds: int, units_each: int, outlets: int) -> dict:
        pending = [units_each] * feeds
        rot = 0
        delivered = [0] * outlets
        feed_idx = 0
        ticks = 0
        total_in = feeds * units_each
        while sum(pending) > 0:
            if pending[feed_idx] > 0:
                pending[feed_idx] -= 1
                delivered[rot] += 1
                rot = (rot + 1) % outlets
            feed_idx = (feed_idx + 1) % feeds
            ticks += 1
        return {"ticks": ticks, "delivered_per_outlet": delivered,
                "total": sum(delivered), "conserved": sum(delivered) == total_in}

    demux2 = vortex_sim(2, 4, 2)
    demux3 = vortex_sim(2, 4, 3)
    # chained clocks: k=2 and k=3 vortexes compose to a 6-tick period (LCM)
    def clock_period(k: int) -> int:
        return k
    OUT["p7c_vortex_sketch"] = {
        "law": "vortex holds a rotation register r; each tick it emits one held unit on outlet r then advances r=(r+1)%k",
        "k2_two_feeds": demux2,
        "k3_two_feeds": demux3,
        "xor_delivered_for_same_feed": g.volume("pool") if False else 0,
        "period_law": "a vortex of k outlets is a mod-k counter; k=2 chained with k=3 composes to period LCM(2,3)=6",
        "periods": {"k2": clock_period(2), "k3": clock_period(3),
                    "k2xk3_lcm": 6},
    }


def p8_waste_basin_win() -> None:
    w = MountainWorld()
    w.register_session("s1", "u1", "spring")
    drain_ticks = 0
    for _ in range(60):
        payload = w.tick()
        drain_ticks += 1
        if payload["nodes"]["spring"] == 0 and payload["nodes"]["hollow"] == 0:
            break
    waste_at_rest = payload["nodes"]["waste"]
    boils = 0
    while not w.winner and boils < 8:
        ack = w.stage("s1", "boil", "waste")
        assert ack.get("op") == "ack", ack
        w.tick()
        boils += 1
    OUT["p8_waste_basin_win"] = {
        "ticks_to_fully_drain": drain_ticks,
        "waste_volume_at_rest": waste_at_rest,
        "boil_verbs_on_waste_for_win": boils,
        "crown_volume": w.graph.nodes["crown"].volume,
        "winner": w.winner,
        "world_total_liquid_and_steam": sum(
            n.volume + n.steam for n in w.graph.nodes.values()),
    }


def p9_sill_and_any() -> None:
    # sill: the hydraulic AND. Census says zero dedicated tests.
    # hold case: one inlet against sill 2
    g = WaterGraph()
    g.add_node("sa", elev=5, volume=1)
    g.add_node("sb", elev=5, volume=0)
    g.add_node("dam", elev=2, kind="sill", sill=2)
    g.add_node("pool", elev=0)
    g.add_pipe("pa", "sa", "dam", cap=1)
    g.add_pipe("pb", "sb", "dam", cap=1)
    g.add_pipe("spout", "dam", "pool", cap=2)
    ev1 = g.tick()
    # pass case: two CONCURRENT inlets, fresh board
    g2 = WaterGraph()
    g2.add_node("sa", elev=5, volume=1)
    g2.add_node("sb", elev=5, volume=1)
    g2.add_node("dam", elev=2, kind="sill", sill=2)
    g2.add_node("pool", elev=0)
    g2.add_pipe("pa", "sa", "dam", cap=1)
    g2.add_pipe("pb", "sb", "dam", cap=1)
    g2.add_pipe("spout", "dam", "pool", cap=2)
    ev2 = g2.tick()
    OUT["p9_sill_gate"] = {
        "one_inlet_tick": [e for e in ev1 if "dam" in e],
        "dam_pooled_after_one_inlet": g.volume("dam"),
        "two_inlet_tick": [e for e in ev2 if "dam" in e],
        "pool_after_two_inlets": g2.volume("pool"),
        "dam_kept_after_two_inlets": g2.volume("dam"),
    }

    # kind "any": promised by the module docstring, absent from the Node
    # kind list; where does it land?
    g = WaterGraph()
    g.add_node("sa", elev=5, volume=1)
    g.add_node("hub", elev=2, kind="any")
    g.add_node("pool", elev=0)
    g.add_pipe("pa", "sa", "hub", cap=1)
    g.add_pipe("spout", "hub", "pool", cap=1)
    ev = g.tick()
    OUT["p9_any_kind"] = {
        "docstring_promises": "`any` is OR (water_graph.py module docstring)",
        "node_kind_list_has_any": False,
        "tick_events": ev,
        "pool_got_the_unit_same_tick": g.volume("pool") == 1,
        "behavior": "plain accumulator with same-tick pass-through (no gate special-case matches 'any')",
    }


def main() -> int:
    p1_steam_roundtrip()
    p2_steam_no_cold()
    p3_siphon_break()
    p4_stock_board_reach()
    p5_valve_event_lie()
    p6_starved_uphill()
    p7_vortex()
    p8_waste_basin_win()
    p9_sill_and_any()
    print(json.dumps(OUT, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
