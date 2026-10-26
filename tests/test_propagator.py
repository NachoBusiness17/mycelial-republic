"""propagator tests — Y10 receipts (Mickey17 W3K lane, 2026-09-29).

THE AGREEMENT LAW: tools/legality_propagator.py labels (state, action)
pairs by constraint propagation alone; tools.legality_dataset.label_sample
labels the same pairs by RUNNING the real engine (WaterGraph.tick). On
sampled W3K cases the two verdicts must be byte-equal — any disagreement
is a bug in the PROPAGATOR (the engine is ground truth by definition of
the lane). Plus hand-checked unit constraints: each named rejection
reason, and the crown_gain physics (steam path, drain negation, primed
siphon climb, valve-opened route). V5 ECONOMY LAW (2026-09-29) units:
waste is a basin (held units feed a later primed siphon to the crown) and
a STARVED junction's spill routes to the first waste node in insertion
order — or is held at the junction with no waste node.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.legality_dataset import (  # noqa: E402
    label_sample,
    make_graph_spec,
    rebuild_graph,
    sample_action,
)
from tools.legality_propagator import (  # noqa: E402
    _fracture_threshold,
    _propagate_flow,
    crown_gain,
    dry_pool,
    propagate,
    unknown_target,
    unknown_verb,
)

AGREEMENT_N = 100
AGREEMENT_SEED = 1010


# ---------------------------------------------------------- agreement law ----
def test_agreement_law_100_sampled_cases() -> None:
    """100 seeded W3K cases: propagator verdict == engine verdict, full
    dict equality (legal + illegal_reason + crown_gain + label)."""
    rng = __import__("random").Random(AGREEMENT_SEED)
    for i in range(AGREEMENT_N):
        spec = make_graph_spec(rng)
        verb, target = sample_action(rng, spec)
        engine = label_sample(spec, verb, target)     # runs WaterGraph.tick
        oracle = propagate(spec, verb, target)        # constraints only
        assert oracle == engine, (
            f"case {i}: verb={verb} target={target} "
            f"engine={engine} oracle={oracle}")


def test_agreement_covers_every_label() -> None:
    """The 100 sampled cases must exercise all five labels, else the
    agreement law above could pass while never testing a class."""
    rng = __import__("random").Random(AGREEMENT_SEED)
    seen: set[str] = set()
    for _ in range(AGREEMENT_N):
        spec = make_graph_spec(rng)
        verb, target = sample_action(rng, spec)
        seen.add(propagate(spec, verb, target)["label"])
        assert label_sample(spec, verb, target)["label"] in seen
    assert seen == {"illegal_unknown_verb", "illegal_unknown_target",
                    "illegal_dry_pool", "legal_gain", "legal_no_gain"}, seen


def test_propagator_is_engine_free() -> None:
    """Independence law: the oracle propagates constraints over the raw
    spec — it must not import the engine it is an oracle FOR (else the
    agreement test would be the engine agreeing with itself)."""
    src = (ROOT / "tools" / "legality_propagator.py").read_text(encoding="utf-8")
    assert "water_graph" not in src
    assert "WaterGraph" not in src
    assert "from_spec" not in src


def test_propagate_is_pure() -> None:
    """Calling the oracle twice on the same spec gives the same verdict
    and never mutates the caller's state dict."""
    rng = __import__("random").Random(7)
    spec = make_graph_spec(rng)
    verb, target = sample_action(rng, spec)
    snapshot = __import__("json").dumps(spec, sort_keys=True)
    first = propagate(spec, verb, target)
    second = propagate(spec, verb, target)
    assert first == second
    assert __import__("json").dumps(spec, sort_keys=True) == snapshot


# ------------------------------------------------------------- unit laws ----
def _spec(nodes: dict, pipes: dict) -> dict:
    """Minimal water_graph.v1-shaped spec for hand-checked cases."""
    ns = {}
    for name, (elev, kind, volume, steam, sill) in nodes.items():
        ns[name] = {"elev": elev, "kind": kind, "sill": sill,
                    "volume": volume, "steam": steam}
    ps = {}
    for name, (src, dst, cap, siphon, crest, primed, open_) in pipes.items():
        ps[name] = {"src": src, "dst": dst, "cap": cap, "siphon": siphon,
                    "crest": crest, "primed": primed, "open": open_}
    return {"schema": "water_graph.v1", "tick": 0, "nodes": ns, "pipes": ps}


_BASE_NODES = {
    #        elev  kind    volume steam sill
    "a":     (5,   "plain", 3,     0,    0),
    "crown": (15,  "cold",  0,     0,    0),
    "waste": (0,   "waste", 0,     0,    0),
}


def test_unknown_verb_constraint() -> None:
    spec = _spec(_BASE_NODES, {})
    assert unknown_verb("purify")
    assert not unknown_verb("boil")
    assert propagate(spec, "purify", "a")["label"] == "illegal_unknown_verb"
    assert label_sample(spec, "purify", "a")["label"] == "illegal_unknown_verb"


def test_unknown_target_constraint() -> None:
    spec = _spec(_BASE_NODES, {"p_out": ("a", "waste", 1, False, 2, False, True)})
    assert unknown_target(spec, "boil", "ghost")
    assert unknown_target(spec, "valve", "a")        # valve resolves pipes only
    assert unknown_target(spec, "valve", "p_ghost")
    assert propagate(spec, "boil", "ghost")["label"] == "illegal_unknown_target"
    assert propagate(spec, "valve", "a")["label"] == "illegal_unknown_target"
    assert label_sample(spec, "valve", "a")["label"] == "illegal_unknown_target"


def test_dry_pool_constraint() -> None:
    nodes = dict(_BASE_NODES)
    nodes["dry"] = (3, "plain", 0, 0, 0)
    spec = _spec(nodes, {})
    assert dry_pool(spec, "boil", "dry")
    assert dry_pool(spec, "tag", "dry")
    assert not dry_pool(spec, "boil", "a")
    assert not dry_pool(spec, "valve", "dry")        # valve has no pool need
    assert propagate(spec, "boil", "dry")["label"] == "illegal_dry_pool"
    assert label_sample(spec, "tag", "dry")["label"] == "illegal_dry_pool"


def test_crown_gain_steam_path() -> None:
    """boil arms the steam path: steam ignores pipes and condenses at the
    COLD node even with NO route through the graph."""
    spec = _spec(_BASE_NODES, {})
    assert crown_gain(spec, "boil", "a")
    assert propagate(spec, "boil", "a")["label"] == "legal_gain"
    assert label_sample(spec, "boil", "a")["label"] == "legal_gain"


def test_crown_gain_negated_by_drain() -> None:
    """A steam path alone is not a gain: crown's own open out-pipe drains
    the condensate the same tick (condense runs BEFORE flow)."""
    spec = _spec(_BASE_NODES, {"p_drain": ("crown", "waste", 1, False, 2, False, True)})
    assert not crown_gain(spec, "boil", "a")
    assert propagate(spec, "boil", "a")["label"] == "legal_no_gain"
    assert label_sample(spec, "boil", "a")["label"] == "legal_no_gain"


def test_crown_gain_via_valve_opened_route() -> None:
    """valve can arm the only climbing route: a PRIMED siphon ignores head
    (the one mechanism that can reach the strict-max cold node) but here
    starts shut — the action opens it."""
    pipes = {"p_climb": ("a", "crown", 1, True, 2, True, False)}
    spec = _spec(_BASE_NODES, pipes)
    assert crown_gain(spec, "valve", "p_climb")
    assert propagate(spec, "valve", "p_climb")["label"] == "legal_gain"
    assert label_sample(spec, "valve", "p_climb")["label"] == "legal_gain"


def test_crown_gain_from_prewired_state() -> None:
    """A social verb (tag) changes no hydraulics, yet a pre-primed open
    siphon still delivers: gain is a property of the PROPAGATED state."""
    nodes = dict(_BASE_NODES)
    nodes["a"] = (5, "plain", 2, 0, 0)
    pipes = {"p_climb": ("a", "crown", 1, True, 2, True, True)}
    spec = _spec(nodes, pipes)
    assert crown_gain(spec, "tag", "a")
    assert propagate(spec, "tag", "a")["label"] == "legal_gain"
    assert label_sample(spec, "tag", "a")["label"] == "legal_gain"


def test_no_gain_when_nothing_moves() -> None:
    """Wet target, no steam, no climbing route: legal, no gain."""
    spec = _spec(_BASE_NODES, {"p_out": ("a", "waste", 1, False, 2, False, True)})
    assert not crown_gain(spec, "join", "a")
    assert propagate(spec, "join", "a")["label"] == "legal_no_gain"
    assert label_sample(spec, "join", "a")["label"] == "legal_no_gain"


# ------------------------------------------------------- V5 economy laws ----
def _flow_volumes(spec: dict) -> dict:
    """Run ONLY the propagator's FLOW phase on a spec (the same normalized
    node/pipe dicts crown_gain builds) and return node -> volume. For
    state-level laws the verdict cannot see (the STARVED spill lands after
    the plain-pipe phase and gated outflow never sources waste, so it can
    never reach the crown in the same tick)."""
    nodes = {name: {"elev": int(nd.get("elev", 0)),
                    "kind": str(nd.get("kind", "plain")),
                    "sill": int(nd.get("sill", 0)),
                    "volume": int(nd.get("volume", 0)),
                    "steam": int(nd.get("steam", 0))}
             for name, nd in spec["nodes"].items()}
    pipes = [{"name": name, "src": pp["src"], "dst": pp["dst"],
              "cap": int(pp.get("cap", 1)), "siphon": bool(pp.get("siphon", False)),
              "crest": int(pp.get("crest", 2)),
              "primed": bool(pp.get("primed", False)),
              "open": bool(pp.get("open", True)),
              "stress": int(pp.get("stress", 0)),
              "fractured": bool(pp.get("fractured", False))}
             for name, pp in spec["pipes"].items()]
    _propagate_flow(nodes, pipes)
    return {name: nd["volume"] for name, nd in nodes.items()}


def test_waste_basin_feeds_a_primed_siphon() -> None:
    """V5: waste HOLDS what it receives (a basin, not a void) — so water
    piped to waste is spendable by a later-in-insertion-order PRIMED siphon
    out of waste climbing to the crown. The pre-V5 swallow law deleted the
    units and read legal_no_gain where the engine measures a gain."""
    pipes = {"p_down": ("a", "waste", 2, False, 2, False, True),
             "p_up": ("waste", "crown", 2, True, 2, True, True)}
    spec = _spec(_BASE_NODES, pipes)
    assert crown_gain(spec, "tag", "a")
    assert propagate(spec, "tag", "a")["label"] == "legal_gain"
    assert label_sample(spec, "tag", "a")["label"] == "legal_gain"


def test_starved_spill_routes_to_first_waste_basin() -> None:
    """V5: a STARVED junction's pooled spill ROUTES to the FIRST waste node
    in insertion order (waste receives, never deletes). Pinned at state
    level against the engine's own tick — the verdict cannot see this law."""
    nodes = {"j": (4, "xor", 2, 0, 0),
             "waste": (0, "waste", 0, 0, 0),
             "waste2": (0, "waste", 0, 0, 0),
             "crown": (15, "cold", 0, 0, 0)}
    spec = _spec(nodes, {})
    g = rebuild_graph(spec)
    g.tick()
    assert (g.volume("j"), g.volume("waste"), g.volume("waste2")) == (0, 2, 0)
    assert _flow_volumes(spec) == {"j": 0, "waste": 2, "waste2": 0, "crown": 0}


def test_starved_without_waste_node_holds_at_junction() -> None:
    """V5: no waste node to receive the spill -> the pooled units are HELD
    at the junction (conservation beats deletion), matching the engine."""
    nodes = {"j": (4, "sill", 2, 0, 2),
             "crown": (15, "cold", 0, 0, 0)}
    spec = _spec(nodes, {})
    g = rebuild_graph(spec)
    g.tick()
    assert g.volume("j") == 2
    assert _flow_volumes(spec) == {"j": 2, "crown": 0}


# --------------------------------------------------- AC2 fracture laws ----
# (2026-09-30, watch/inbox/last_mile_20260930/AD1_FRACTURE.md; reach retuned
# B1 2026-09-30, B1_FRACTURE_REACH.md): a fractured pipe is closed for
# legality purposes; the burst is permanent (valve cannot reopen); full-bore
# flow past 200 + djb2(name) % 201 (= [200, 400] volume units) fractures
# MID-TICK and sprays to the lowest-elev node other than dst. Oracle
# re-derives the law engine-free; every test below is pinned against the
# engine's own tick.


def _fracture_board(fractured: bool, open_: bool = False) -> dict:
    """A pre-primed siphon a -> crown (the sole climbing route) that arrives
    FRACTURED: without the law both labelers would read legal_gain."""
    pipes = {"p_climb": ("a", "crown", 1, True, 2, True, open_)}
    spec = _spec(_BASE_NODES, pipes)
    spec["pipes"]["p_climb"]["fractured"] = fractured
    return spec


def test_fractured_pipe_is_closed_for_legality_purposes() -> None:
    spec = _fracture_board(fractured=True)
    assert propagate(spec, "tag", "a") == label_sample(spec, "tag", "a")
    assert propagate(spec, "tag", "a")["label"] == "legal_no_gain"
    # adversarial spec shape (burst flag with open=True): the skip law, not
    # the open flag, is what closes it — both labelers agree anyway.
    weird = _fracture_board(fractured=True, open_=True)
    assert propagate(weird, "tag", "a") == label_sample(weird, "tag", "a")
    assert propagate(weird, "tag", "a")["label"] == "legal_no_gain"


def test_valve_on_fractured_pipe_cannot_reopen() -> None:
    """valve targets a fractured pipe: legal (the pipe exists) but the burst
    is permanent — the engine refuses the reopen, the oracle never toggles,
    and the verdicts agree with no gain."""
    spec = _fracture_board(fractured=True)
    assert propagate(spec, "valve", "p_climb") == label_sample(spec, "valve", "p_climb")
    assert propagate(spec, "valve", "p_climb")["label"] == "legal_no_gain"
    weird = _fracture_board(fractured=True, open_=True)
    assert propagate(weird, "valve", "p_climb") == label_sample(weird, "valve", "p_climb")


def test_mid_tick_fracture_spray_agrees_verdict_level() -> None:
    """A pipe pre-stressed AT its threshold fractures ON the propagated
    tick: the climbing siphon's flow sprays to the lowest-elev node other
    than the crown instead of delivering — engine and oracle both read
    legal_no_gain (without the propagated stress law this reads legal_gain
    and the agreement law breaks)."""
    spec = _fracture_board(fractured=False, open_=True)
    spec["pipes"]["p_climb"]["stress"] = _fracture_threshold("p_climb")
    assert propagate(spec, "tag", "a") == label_sample(spec, "tag", "a")
    assert propagate(spec, "tag", "a")["label"] == "legal_no_gain"


def test_mid_tick_fracture_spray_agrees_state_level() -> None:
    """State-level pin: a plain pipe one below threshold bursts on the flow
    phase — dst receives nothing, the lowest-elev node other than dst
    receives the full flow. Engine tick and the propagator's FLOW phase
    land the spray at the same node."""
    nodes = {"a": (5, "plain", 2, 0, 0),
             "b": (3, "plain", 0, 0, 0),
             "sump": (0, "plain", 0, 0, 0),
             "crown": (15, "cold", 0, 0, 0)}
    pipes = {"p_hot": ("a", "b", 2, False, 2, False, True)}
    spec = _spec(nodes, pipes)
    spec["pipes"]["p_hot"]["stress"] = _fracture_threshold("p_hot") - 1
    g = rebuild_graph(spec)
    g.tick()
    assert g.pipes["p_hot"].fractured
    assert (g.volume("a"), g.volume("b"), g.volume("sump")) == (0, 0, 2)
    assert _flow_volumes(spec) == {"a": 0, "b": 0, "sump": 2, "crown": 0}


def test_gated_inlet_fracture_agrees_b1_seam() -> None:
    """B1 seam fix (2026-09-30, B1_FRACTURE_REACH.md): a GATED inlet two
    below threshold bursts ON the probe in both labelers (probe adds cap 3
    -> threshold+1, strictly past) — full-bore flow into a gated junction
    stresses at probe time (the engine's tick() and this oracle's gated
    branch carry the same law), the gate never sees that tick's inlet, and
    the spray lands at the same node. Without the seam fix on either side
    the verdicts diverge (engine bursts, oracle delivers through the gate)
    and the agreement law breaks."""
    nodes = {"a": (6, "plain", 3, 0, 0),
             "gate": (2, "xor", 0, 0, 0),
             "sump": (0, "plain", 0, 0, 0),
             "crown": (15, "cold", 0, 0, 0)}
    pipes = {"p_gate": ("a", "gate", 3, False, 2, False, True)}
    spec = _spec(nodes, pipes)
    spec["pipes"]["p_gate"]["stress"] = _fracture_threshold("p_gate") - 2
    g = rebuild_graph(spec)
    g.tick()
    assert g.pipes["p_gate"].fractured, "engine: gated inlet bursts at probe"
    assert g.volume("gate") == 0, "burst tick's flow never reaches the gate"
    assert g.volume("sump") == 3
    assert propagate(spec, "tag", "a") == label_sample(spec, "tag", "a")
    assert _flow_volumes(spec) == {"a": 0, "gate": 0, "sump": 3, "crown": 0}
