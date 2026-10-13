"""legality_propagator — Y10: the deterministic legality oracle, NO engine.

Mickey17 W3K lane (2026-09-29), N4's first actionable step: the LDT
experiment design (logs/mates/night_burn_20260930.jsonl, row
"N4-ldt-experiment") puts a constraint propagator at the bottom of the
stack — "trivially exact, so the experiment tests whether the MODEL
internalizes it, not whether the oracle is right."

tools/legality_dataset.py labels by RUNNING the real engine (rebuild the
graph, validate, apply, tick, measure the crown). This module labels the
SAME (state, action) pairs by propagating constraints over the raw spec
dict — it never imports or instantiates the engine:

  - unknown_verb      the verb is not in the protocol table (VERBS).
  - unknown_target    valve names a pipe that does not exist; every other
                      verb names a node that does not exist.
  - dry_pool          boil/tag on a node whose volume is 0.
  - crown_gain        legal actions: propagate ONE tick of physics to the
                      COLD node ("crown", the Mountain family's unique
                      strict-max-elevation cold node) and ask whether its
                      volume strictly rose:
                        (a) ACTION: boil lifts 1 volume to steam at the
                            target; valve toggles the named pipe's gate;
                            join/tag touch no hydraulics.
                        (b) STEAM: steam ignores pipes — every unit of
                            steam in the graph condenses at the highest
                            cold node (first-max in insertion order, the
                            engine's max() tie rule).
                        (c) FLOW: pipes carry water downhill only
                            (src.elev > dst.elev, the check-valve law),
                            cap-limited; a siphon must prime at its crest
                            (volume >= crest AND downhill) but once primed
                            runs regardless of head until its intake dries;
                            xor junctions pass exactly one delivering
                            inlet, sill junctions pass when the COUNT of
                            delivering inlets >= sill (under-gate inflow is
                            held pooled at the junction, water still leaves
                            the source); junction outflow waits for its
                            gate. V5 ECONOMY LAW (2026-09-29): waste is a
                            BASIN, not a void — it holds what it receives,
                            so a later pipe (in insertion order) out of
                            waste can still spend it; a STARVED junction's
                            pooled spill ROUTES to the first waste node in
                            insertion order, and is HELD at the junction
                            when no waste node exists (deletion is theft).
                            AC2 FRACTURE LAW (2026-09-30; reach retuned B1
                            2026-09-30, watch/inbox/last_mile_20260930/
                            B1_FRACTURE_REACH.md): a FRACTURED pipe
                            is closed for legality purposes — it carries
                            nothing and a valve action cannot reopen it
                            (the burst is permanent). Full-bore flow
                            (flow == cap) accumulates stress as cumulative
                            VOLUME; past 200 + djb2(name) % 201 (= [200,
                            400] volume units) the pipe fractures
                            mid-tick and that tick's flow sprays to the
                            lowest-elevation node other than dst (first-min
                            in insertion order) — conserved, never deleted.
                            A fresh board cannot reach the threshold inside
                            the one-tick horizon, but specs may carry
                            stress/fractured state, so the propagation
                            implements the law rather than assuming it
                            cannot fire.

The crown can only GAIN from steam condensation and from primed siphons
(the sole mechanism that can climb to the strict max elevation) — but it
can LOSE through its own open out-pipes, so "a steam path exists" alone
is not the verdict: the net delta after all constraints propagate is.
phases (a)-(c) are re-derived here from the physics laws, not copied from
the engine's tick loop; agreement is pinned by tests/test_propagator.py
on sampled W3K cases (the agreement law: any disagreement is a bug in
the PROPAGATOR).

CLI: score agreement against the engine-labeled dataset over N seeded
cases and print the match rate. $0, stdlib, deterministic.
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.protocol import VERBS  # noqa: E402 — the verb table (data, not engine)

_GATED_KINDS = ("xor", "sill")


def _name_hash(s: str) -> int:
    """AC2 re-derivation: djb2 32-bit string hash (the fracture threshold's
    entropy source). Independent copy, byte-identical loop — the oracle must
    not import the engine it is an oracle FOR, so the law is re-derived here
    like every other constraint. Deterministic, zero RNG."""
    h = 5381
    for ch in s:
        h = ((h * 33) + ord(ch)) & 0xFFFFFFFF
    return h


def _fracture_threshold(pipe_name: str) -> int:
    """AC2 + B1 (2026-09-30): volume a pipe survives at full bore:
    200 + hash(name) % 201 -> [200, 400] VOLUME units (stress accumulates
    as cumulative throughput — same re-derivation duty as every other
    constraint; see the AC2/B1 paragraph in the module docstring)."""
    return 200 + _name_hash(pipe_name) % 201


# ------------------------------------------------------------ constraints ----
def unknown_verb(verb: str) -> bool:
    """Constraint: the verb must live in the live protocol table."""
    return verb not in VERBS


def unknown_target(spec: dict[str, Any], verb: str, target: str) -> bool:
    """Constraint: valve resolves against pipes, everything else against
    nodes (server/world.py validate's rule, minus the sid check)."""
    if verb == "valve":
        return target not in spec.get("pipes", {})
    return target not in spec.get("nodes", {})


def dry_pool(spec: dict[str, Any], verb: str, target: str) -> bool:
    """Constraint: boil and tag need water in the pool (volume > 0)."""
    if verb not in ("boil", "tag"):
        return False
    node = spec.get("nodes", {}).get(target)
    return node is None or int(node.get("volume", 0)) <= 0


def _condense(nodes: dict[str, dict[str, Any]]) -> None:
    """STEAM constraint: every steam unit condenses at the highest cold
    node; no cold node -> steam stays put (nothing falls back this tick)."""
    cold = None
    for nd in nodes.values():
        if nd["kind"] == "cold" and (cold is None or nd["elev"] > cold["elev"]):
            cold = nd
    if cold is None:
        return
    for nd in nodes.values():
        if nd["steam"]:
            cold["volume"] += nd["steam"]
            nd["steam"] = 0


def _stress_and_maybe_burst(pipe: dict[str, Any], src: dict[str, Any],
                            dst: dict[str, Any],
                            nodes: dict[str, dict[str, Any]], flow: int) -> bool:
    """AC2+B1 fracture constraint, shared by _carry and the gated-inlet
    probe: full-bore flow (flow == cap) loads the pipe (stress += flow,
    cumulative VOLUME); past 200 + djb2(name) % 201 it bursts mid-tick —
    closed forever — and the flow sprays to the lowest-elevation node other
    than dst (first-min in insertion order) instead of delivering. Returns
    True when the burst fired (volumes already moved: src -= flow, spray
    += flow). B1 SEAM FIX (2026-09-30): gated inlets stress at probe time
    too — mirrors the engine's tick() gated branch, without which the
    default Mountain's main artery (spring -> xor gate) could never burst
    and this oracle would disagree with the engine on any pre-stressed
    gated board."""
    if flow != pipe["cap"]:
        return False
    pipe["stress"] += flow
    if pipe["stress"] <= _fracture_threshold(pipe["name"]):
        return False
    pipe["fractured"] = True
    pipe["open"] = False
    src["volume"] -= flow
    spray = min((nd for nd in nodes.values() if nd is not dst),
                key=lambda nd: nd["elev"])
    spray["volume"] += flow
    return True


def _carry(pipe: dict[str, Any], src: dict[str, Any], dst: dict[str, Any],
           nodes: dict[str, dict[str, Any]]) -> int:
    """FLOW constraint helper: units this pipe would carry src -> dst right
    now, committing priming/breaking and (on success) the volume move —
    the physics of one pipe evaluated once, in order. AC2+B1: full-bore
    flow loads the pipe (shared burst law in _stress_and_maybe_burst); on
    burst the flow sprays instead of delivering."""
    if src["volume"] <= 0:
        if pipe["siphon"] and pipe["primed"]:
            pipe["primed"] = False          # intake dry: siphon breaks
        return 0
    head_ok = src["elev"] > dst["elev"]     # check valve: downhill only
    if pipe["siphon"]:
        if not pipe["primed"]:
            if src["volume"] < pipe["crest"] or not head_ok:
                return 0                    # cannot prime at crest
            pipe["primed"] = True
        flow = min(pipe["cap"], src["volume"])   # primed: head no longer matters
    else:
        if not head_ok:
            return 0
        flow = min(pipe["cap"], src["volume"])
    if _stress_and_maybe_burst(pipe, src, dst, nodes, flow):
        return flow                    # burst: sprayed, not delivered
    src["volume"] -= flow
    # V5 ECONOMY LAW (2026-09-29): waste is a BASIN, not a void — it HOLDS
    # what it receives, so a later-in-insertion-order pipe out of waste (or
    # a boil, on multi-tick horizons) can still spend it. The old "waste
    # swallows, nothing pools" guard deleted units the engine now conserves.
    # Evidence fixed-on: the hand-built basin cascade (a -> waste, then a
    # primed siphon waste -> crown) where the engine's verdict is legal_gain
    # and this cut read legal_no_gain; engine post-tick state holds the
    # units at the waste node.
    dst["volume"] += flow
    return flow


def _carry_no_commit(pipe: dict[str, Any], src: dict[str, Any],
                     dst: dict[str, Any]) -> int:
    """Units a pipe INTO a gated junction would carry (volumes commit only
    if the gate passes or holds; priming DOES commit — a primed siphon
    stays primed either way)."""
    if src["volume"] <= 0:
        return 0
    head_ok = src["elev"] > dst["elev"]
    if pipe["siphon"]:
        if not pipe["primed"]:
            if src["volume"] < pipe["crest"] or not head_ok:
                return 0
            pipe["primed"] = True
        return min(pipe["cap"], src["volume"])
    if not head_ok:
        return 0
    return min(pipe["cap"], src["volume"])


def _propagate_flow(nodes: dict[str, dict[str, Any]],
                    pipes: list[dict[str, Any]]) -> None:
    """FLOW constraints, one pass in pipe order: plain pipes move now;
    pipes into gated junctions defer (gate reads the delivering-inlet
    count); gated junctions' outflow runs only under an open gate."""
    deferred: dict[str, list[tuple[dict[str, Any], int]]] = {}
    gated_out: list[dict[str, Any]] = []
    for pipe in pipes:
        if not pipe["open"] or pipe["fractured"]:
            continue                        # AC2: a fractured pipe is closed
        src, dst = nodes[pipe["src"]], nodes[pipe["dst"]]
        if src["kind"] in _GATED_KINDS:
            gated_out.append(pipe)
            continue
        if dst["kind"] in _GATED_KINDS:
            flow = _carry_no_commit(pipe, src, dst)
            if flow:
                # B1 SEAM FIX mirror: a gated inlet running full bore
                # stresses AT PROBE TIME (the water left the source through
                # the pipe section) — same law the engine's tick() gated
                # branch now carries. On burst the probe-time flow sprays
                # (conserved) and the gate never sees the inlet.
                if _stress_and_maybe_burst(pipe, src, dst, nodes, flow):
                    continue
                deferred.setdefault(pipe["dst"], []).append((pipe, flow))
            continue
        _carry(pipe, src, dst, nodes)

    gate: dict[str, bool] = {}
    for name, node in nodes.items():
        if node["kind"] not in _GATED_KINDS:
            continue
        ins = deferred.get(name, [])
        if node["kind"] == "xor":
            allow = len(ins) == 1           # exactly one inlet delivers
        else:
            allow = len(ins) >= max(1, node["sill"])   # inlet COUNT meets sill
        gate[name] = allow
        for pipe, flow in ins:              # pass or hold: water leaves src
            nodes[pipe["src"]]["volume"] -= flow
            node["volume"] += flow
        if not allow and not ins and node["volume"] > 0:
            # STARVED: pooled units spill. V5 ECONOMY LAW (2026-09-29): the
            # spill ROUTES to the first waste node in insertion order (a
            # boilable basin), and with no waste node it is HELD at the
            # junction — deletion is theft. The old zeroing mirrored the
            # pre-V5 engine's silent deletion. Evidence fixed-on: engine
            # post-tick state on the hand-built STARVED board reads
            # junction 0 / first-waste +spill (and junction HELD when no
            # waste node exists) where this cut read all zeros.
            spill = node["volume"]
            basin = next((nd for nd in nodes.values() if nd["kind"] == "waste"),
                         None)
            if basin is not None:
                basin["volume"] += spill
                node["volume"] = 0

    for pipe in gated_out:
        if gate.get(pipe["src"]):
            _carry(pipe, nodes[pipe["src"]], nodes[pipe["dst"]], nodes)


def crown_gain(spec: dict[str, Any], verb: str, target: str) -> bool:
    """Does the COLD node's volume strictly rise under (action + one tick)?
    Pure constraint propagation over copies of the spec — the engine is
    never touched. The Mountain law makes "crown" the unique COLD node at
    the strict max elevation: it can only be fed by steam (and, outside
    the Mountain family, by an already-primed siphon)."""
    nodes = {name: {"elev": int(nd.get("elev", 0)),
                    "kind": str(nd.get("kind", "plain")),
                    "sill": int(nd.get("sill", 0)),
                    "volume": int(nd.get("volume", 0)),
                    "steam": int(nd.get("steam", 0))}
             for name, nd in spec.get("nodes", {}).items()}
    pipes = [{"name": name, "src": pp["src"], "dst": pp["dst"],
              "cap": int(pp.get("cap", 1)), "siphon": bool(pp.get("siphon", False)),
              "crest": int(pp.get("crest", 2)),
              "primed": bool(pp.get("primed", False)),
              "open": bool(pp.get("open", True)),
              "stress": int(pp.get("stress", 0)),
              "fractured": bool(pp.get("fractured", False))}
             for name, pp in spec.get("pipes", {}).items()]

    before = nodes["crown"]["volume"]

    # (a) ACTION constraints
    if verb == "boil":
        node = nodes[target]
        units = min(1, node["volume"])      # validate guarantees >= 1
        node["volume"] -= units
        node["steam"] += units
    elif verb == "valve":
        for pipe in pipes:
            # AC2: a FRACTURED pipe is closed for legality purposes — the
            # valve verb targets it legally (it exists) but the burst is
            # permanent: no toggle, exactly like the engine's refused reopen.
            if pipe["name"] == target and not pipe["fractured"]:
                pipe["open"] = not pipe["open"]
    # join/tag: social verbs — no hydraulic constraint

    # (b) STEAM, then (c) FLOW — the tick's phase order
    _condense(nodes)
    _propagate_flow(nodes, pipes)
    return nodes["crown"]["volume"] > before


# ---------------------------------------------------------------- verdict ----
def propagate(spec: dict[str, Any], verb: str, target: str) -> dict[str, Any]:
    """The oracle: (state, action) -> the same verdict dict the engine-run
    labeler produces (legal / illegal_reason / crown_gain / label)."""
    reason: str | None = None
    if unknown_verb(verb):
        reason = "unknown_verb"
    elif unknown_target(spec, verb, target):
        reason = "unknown_target"
    elif dry_pool(spec, verb, target):
        reason = "dry_pool"
    if reason is not None:
        return {"legal": False, "illegal_reason": reason,
                "crown_gain": False, "label": f"illegal_{reason}"}
    gain = crown_gain(spec, verb, target)
    return {"legal": True, "illegal_reason": None, "crown_gain": gain,
            "label": "legal_gain" if gain else "legal_no_gain"}


# -------------------------------------------------------------------- CLI ----
def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--n", type=int, default=1000,
                    help="sampled W3K cases to score (engine vs propagator)")
    ap.add_argument("--seed", type=int, default=17)
    args = ap.parse_args(argv)

    from tools.legality_dataset import (label_sample, make_graph_spec,  # noqa: E402
                                        sample_action)

    rng = random.Random(args.seed)
    agree = 0
    by_label: dict[str, int] = {}
    disagreements: list[str] = []
    for i in range(args.n):
        spec = make_graph_spec(rng)
        verb, target = sample_action(rng, spec)
        engine = label_sample(spec, verb, target)      # runs the REAL engine
        oracle = propagate(spec, verb, target)         # constraints only
        if oracle == engine:
            agree += 1
            by_label[engine["label"]] = by_label.get(engine["label"], 0) + 1
        else:
            disagreements.append(f"case {i}: verb={verb} target={target} "
                                 f"engine={engine} oracle={oracle}")
    rate = agree / args.n if args.n else 0.0
    print(f"agreement: {agree}/{args.n} ({rate:.2%})")
    print(f"label coverage (agreed): {dict(sorted(by_label.items()))}")
    for line in disagreements[:10]:
        print(f"DISAGREE {line}")
    return 0 if agree == args.n else 1


if __name__ == "__main__":
    sys.exit(_main())
