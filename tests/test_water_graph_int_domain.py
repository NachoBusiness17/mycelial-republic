"""R8 INT DOMAIN LAW tests (2026-09-30, receipt
watch/inbox/last_mile_20260930/R8_INT_DOMAIN.md).

Python ints are unbounded; GDScript ints are 64-bit. The depth product
volume * DEPTH_SCALE (mag/hydrology.py HydroNode + water_graph.gd
HydroNode.depth, the render layer's to_dict included) crossed 2^63
silently in the Godot twin on mega-volume boards while Python computed it
exactly. The law pinned here:

  - the volume domain is BOUNDED at VOLUME_SAT, derived so that
    volume * DEPTH_SCALE and elev * HEAD_SCALE + depth stay inside signed
    int64 for any in-domain board (cross_section >= 1 worst case);
  - EVERY increment flows through one saturating receiver that clamps at
    the ceiling and NAMES the absorbed amount (a SATURATES event —
    policy-declared deletion with a sensor, never a silent wrap);
  - ingestion (add_node) clamps into the domain silently by design (no
    event stream exists at construction time);
  - the parity harness's stress_domain family crosses that ceiling every
    run, and both engines hash identically through it (pinned end-to-end
    below when the Godot binary exists).
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.water_graph import (  # noqa: E402
    DEPTH_SCALE, ELEV_SAT, HEAD_SCALE, INT64_MAX, VOLUME_SAT, WaterGraph,
    fracture_threshold,
)

T12 = 10 ** 12


# ---------------------------------------------------- the policy's math ----

def test_volume_sat_literal_and_derivation():
    """The ceiling is BOTH engines' shared literal and the exact derivation:
    (INT64_MAX - ELEV_SAT*HEAD_SCALE) // DEPTH_SCALE."""
    assert VOLUME_SAT == 9_223_372_036_586_340
    assert VOLUME_SAT == (INT64_MAX - ELEV_SAT * HEAD_SCALE) // DEPTH_SCALE


def test_no_derived_product_can_cross_int64():
    """The policy's core invariant: at the ceiling, with the widest
    elevation and the narrowest tank, every derived integer product in
    either engine stays inside signed int64 — the GDScript twin cannot
    wrap even at the domain's corner."""
    assert VOLUME_SAT * DEPTH_SCALE <= INT64_MAX            # depth, cs=1
    assert ELEV_SAT * HEAD_SCALE + VOLUME_SAT * DEPTH_SCALE <= INT64_MAX  # head
    assert VOLUME_SAT + VOLUME_SAT < INT64_MAX              # addend headroom


def test_hydrology_scales_are_the_domain_scales():
    """The domain constants mirror mag/hydrology.py's scales; drift here
    would silently change what the ceiling protects."""
    hydro = pytest.importorskip("mag.hydrology")
    assert hydro.DEPTH_SCALE == DEPTH_SCALE
    assert hydro.HEAD_SCALE == HEAD_SCALE


def test_hydrology_depth_at_ceiling_is_int64_safe():
    """The named risk itself: HydroNode at the ceiling (cross_section 1,
    worst case) computes depth/head without leaving int64 — safe by
    construction once the volume domain holds."""
    hydro = pytest.importorskip("mag.hydrology")
    g = hydro.HydrologyGraph()
    g.add_node("rim", elev=ELEV_SAT, kind="plain",
               volume=VOLUME_SAT, cross_section=1)
    assert g.depth("rim") == VOLUME_SAT * DEPTH_SCALE
    assert g.head("rim") <= INT64_MAX


# --------------------------------------------------------- ingest clamps ----

def test_add_node_clamps_volume_into_domain():
    g = WaterGraph()
    n = g.add_node("tank", volume=10 ** 17)
    assert n.volume == VOLUME_SAT


def test_add_node_clamps_elevation_both_ways():
    g = WaterGraph()
    assert g.add_node("up", elev=10 ** 9).elev == ELEV_SAT
    assert g.add_node("down", elev=-(10 ** 9)).elev == -ELEV_SAT
    assert g.add_node("ok", elev=20).elev == 20   # real boards untouched


def test_spec_roundtrip_preserves_the_domain():
    from mag.water_graph import from_spec
    g = WaterGraph()
    g.add_node("over", volume=VOLUME_SAT + 7 * T12)
    spec = json.loads(json.dumps(g.to_spec()))
    assert from_spec(spec).nodes["over"].volume == VOLUME_SAT


# -------------------------------------------------- runtime saturation ----

def _any_sat(events: list[str]) -> bool:
    return any("SATURATES" in e for e in events)


def test_move_delivery_clamps_and_names_absorbed():
    g = WaterGraph()
    g.add_node("tank", elev=2, volume=5 * T12)
    g.add_node("pool", elev=0, volume=VOLUME_SAT - T12)   # room < flow
    # cap > flow: full-bore (flow == cap) mega flow would FRACTURE the pipe
    # on tick 1 (AC2 threshold <= 400 volume) — the generator's same law.
    g.add_pipe("p", "tank", "pool", cap=6 * T12)
    events = g.tick()
    assert g.volume("pool") == VOLUME_SAT
    assert g.volume("tank") == 0
    assert any(f"Node pool SATURATES: {4 * T12} absorbed" in e
               for e in events), events


def test_move_to_waste_clamps():
    g = WaterGraph()
    g.add_node("tank", elev=2, volume=5 * T12)
    g.add_node("pit", elev=0, kind="waste", volume=VOLUME_SAT - T12)
    g.add_pipe("p", "tank", "pit", cap=6 * T12)   # sub-bore (see above)
    events = g.tick()
    assert g.volume("pit") == VOLUME_SAT and _any_sat(events)


def test_fracture_spray_clamps():
    """A burst pipe's mega spray saturates too (the AC2 and R8 laws
    compose: the spray is conserved only up to the ceiling)."""
    g = WaterGraph()
    g.add_node("tank", elev=10, volume=5 * T12)
    g.add_node("pool", elev=5)
    g.add_node("sump", elev=0, kind="waste", volume=VOLUME_SAT - T12)
    g.add_pipe("p_burst", "tank", "pool", cap=5 * T12,
               stress=fracture_threshold("p_burst"))   # full bore -> burst
    events = g.tick()
    assert g.pipes["p_burst"].fractured
    assert g.volume("tank") == 0            # burst decremented the source
    assert g.volume("sump") == VOLUME_SAT   # spray clamped at the ceiling
    assert _any_sat(events) and any("FRACTURES" in e for e in events)


def test_condensation_clamps():
    g = WaterGraph()
    g.add_node("crown", elev=9, kind="cold", volume=VOLUME_SAT - T12)
    g.add_node("wet", elev=1, volume=5 * T12)
    g.nodes["wet"].steam = 5 * T12          # mega steam (verb path is 1/tick)
    events = g.tick()
    assert g.volume("crown") == VOLUME_SAT and _any_sat(events)


def test_gate_commit_clamps():
    g = WaterGraph()
    g.add_node("tank", elev=9, volume=5 * T12)
    g.add_node("gate", elev=5, kind="sill", sill=1,
               volume=VOLUME_SAT - T12)
    g.add_pipe("p", "tank", "gate", cap=6 * T12)  # sub-bore (no AC2 burst)
    events = g.tick()
    assert g.volume("gate") == VOLUME_SAT and _any_sat(events)


def test_gate_hold_clamps():
    """XOR holding below its gate still cannot pool past the ceiling."""
    g = WaterGraph()
    g.add_node("tank", elev=9, volume=5 * T12)
    g.add_node("gate", elev=5, kind="xor", volume=VOLUME_SAT - T12)
    g.add_node("gate2", elev=8, volume=5 * T12)
    g.add_pipe("p1", "tank", "gate", cap=6 * T12)
    g.add_pipe("p2", "gate2", "gate", cap=6 * T12)
    events = g.tick()
    assert g.volume("gate") == VOLUME_SAT and _any_sat(events)


def test_starvation_spill_clamps():
    """The STARVED spill routes its mega pool to waste THROUGH the
    saturating receiver — V5's 'waste is a basin' and R8's 'the basin has
    a ceiling' compose."""
    g = WaterGraph()
    g.add_node("spring", elev=9)                    # dry: gate fails, no inflow
    g.add_node("gate", elev=5, kind="sill", sill=1, volume=VOLUME_SAT)
    g.add_node("pit", elev=0, kind="waste", volume=VOLUME_SAT - T12)
    g.add_pipe("p", "spring", "gate", cap=1)
    events = g.tick()
    assert g.volume("gate") == 0
    assert g.volume("pit") == VOLUME_SAT
    assert any("STARVED" in e for e in events) and _any_sat(events)


def test_boil_steam_ceiling():
    """Steam shares the volume domain; the clamp is silent here by design
    (boil has no event stream — see receipt R8_INT_DOMAIN.md)."""
    g = WaterGraph()
    g.add_node("wet", volume=5 * T12)
    g.nodes["wet"].steam = VOLUME_SAT - 1
    g.boil("wet", 100)
    assert g.nodes["wet"].steam == VOLUME_SAT


def test_absorbed_amount_is_exact_policy_accounting():
    """The named loss is exact: delivered - room = absorbed, and the event
    text carries the number (conservation with a declared deletion)."""
    g = WaterGraph()
    g.add_node("tank", elev=2, volume=9 * T12)
    g.add_node("pool", elev=0, volume=VOLUME_SAT - 3 * T12)
    g.add_pipe("p", "tank", "pool", cap=10 * T12)   # sub-bore (no AC2 burst)
    events = g.tick()
    assert g.volume("pool") == VOLUME_SAT
    assert g.volume("tank") == 0
    assert any(f"SATURATES: {6 * T12} absorbed" in e for e in events), events


# -------------------------------------------- below the ceiling: no law ----

def test_normal_boards_are_unchanged_by_the_domain():
    """The law is additive: volumes an order below the ceiling behave
    exactly as before (no SATURATES events, exact arithmetic)."""
    g = WaterGraph()
    g.add_node("a", elev=2, volume=10)
    g.add_node("b", elev=0, volume=3)
    g.add_pipe("p", "a", "b", cap=4)
    events = g.tick()
    assert g.volume("a") == 6 and g.volume("b") == 7
    assert not _any_sat(events)


# --------------------------------------------- the harness stress family ----

def test_stress_family_inputs_survive_the_godot_json_door():
    """Godot 4.3 parses JSON numbers as float64: odd values above 2^53
    silently round (probed: 9223372036586339 -> ...340). Every stress
    board integer must therefore be float64-exact or the boards diverge at
    INGEST, before any physics. The generator law: multiples of 10^12 and
    VOLUME_SAT-derived evens."""
    from tools.rule_parity import generate
    doc = generate(seed=20260930, n=100, ticks=120)
    stress = [s for s in doc["sequences"] if s["family"] == "stress_domain"]
    assert len(stress) >= 8
    for seq in stress:
        for node in seq["nodes"]:
            for field in ("elev", "sill", "volume"):
                assert float(node[field]) == node[field], (seq["id"], node)
        for pipe in seq["pipes"]:
            for field in ("cap", "crest"):
                assert float(pipe[field]) == pipe[field], (seq["id"], pipe)
        assert any(n["volume"] >= 10 ** 15 for n in seq["nodes"]), seq["id"]


def test_stress_boards_cross_the_ceiling_in_python():
    from tools.rule_parity import generate, run_python
    doc = generate(seed=20260930, n=100, ticks=120)
    stress_ids = {s["id"] for s in doc["sequences"]
                  if s["family"] == "stress_domain"}
    rows = run_python(doc)
    pinned = {r["seq"]: False for r in rows if r["seq"] in stress_ids}
    for r in rows:
        if r["seq"] in stress_ids:
            vols = [n["volume"] for n in r["state"]["nodes"].values()]
            if VOLUME_SAT in vols:
                pinned[r["seq"]] = True
    assert any(pinned.values()), "no stress sequence pinned the ceiling"


@pytest.mark.skipif(
    not (ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64.exe").exists(),
    reason="godot binary not present")
def test_end_to_end_stress_parity_through_the_boundary(tmp_path: Path):
    """THE R8 VERDICT, PINNED: one board per stress shape (all four, found
    deterministically by seed scan) through BOTH engines — the hashes must
    be identical on every tick across the overflow boundary. Unlike the
    V5 philosophy ('the verdict is the measurement'), THIS parity is a
    LAW: divergence here means the int-domain policy broke, not that the
    measurement learned something."""
    from tools.rule_parity import (_server_verbs, _gen_stress_domain,
                                   compare, run_godot, run_python)
    want = {"p_mega", "p_gate", "p_burst"}       # one_shot/ingest_over share p_mega
    seqs, seed = [], 0
    while want and seed < 200:
        rng = random.Random(seed)
        seq = _gen_stress_domain(rng, f"stress_{seed:03d}", ticks=12)
        pipe_names = {p["name"] for p in seq["pipes"]}
        if pipe_names & want:
            seqs.append(seq)
            want -= pipe_names
        seed += 1
    assert not want, f"seed scan never produced shapes for {want}"
    doc = {"schema": "rule_parity.v1", "seed": 1,
           "verbs": list(_server_verbs()), "ticks_default": 12,
           "sequences": seqs}
    inp = tmp_path / "in.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    py_rows = run_python(doc)
    gd_path = tmp_path / "gd.jsonl"
    run_godot(inp, gd_path)
    gd_rows = [json.loads(x) for x in
               gd_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(gd_rows) == len(py_rows)
    report = compare(py_rows, gd_rows)
    assert report["parity"] is True, json.dumps(report["first_divergence"],
                                                indent=1)
