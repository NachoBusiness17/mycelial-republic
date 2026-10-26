"""orbit tests - the skyrmion trap line (mariner cycle 14, 2026-10-23).

THE ORBIT: a vortex whose outlets all RETURN to the basin closes a
recirculation lap (waste basin -> cold crown -> vortex hub -> outlet
legs -> waste): the engine's first mass-free computer. Six laws: (1)
THE ORBITAL CLOCK (one shovel per emission, keyed on the OUTLET PIPE
NAME: the arrow-key control dies after the prime), (2) THE ORBIT'S
SHAPE (return depths are the waveform), (3) THE SKY MOD K (a batch
wind of N parks byte-identical to birth except rot = N mod k), (4)
THE DAMPED ORBIT (one export leg leaks one unit per k turns), (5)
THE PARK IS THE BIRTH STATE (one momentum tick, only the register
differs), (6) THE CROSS-ENGINE ORBIT (the rule_parity harness's
first vortex-kind sequence; NAMED LIMIT: the parity state hash
covers no rot field, so volume and verdict parity only).
Spec: mag/water_graph.py module docstring, THE ORBIT block; the
twin's header mirror in roblox_to_godot/systems/water_graph.gd;
receipt watch/inbox/mates_leave_protocol/receipts/
receipt_20261023_mariner.md.
Consumers: the pytest water family floor and the pre-push gates
(ratchet, citation lint) read this file; the Godot twin's header
mirror is the spec's second copy.
Verifier: these tests are the executable proof; the parity test
executes the twin binary and compares per-tick state hashes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402

BOIL = "mariner boils 1 at waste; it rises."
COND = "Steam condenses at crown (+1)."
CR = "cr: 1 crown->swirl."


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def _orbit(bank: int, k: int, export: bool = False) -> WaterGraph:
    """The cycle-14 orbit board: waste basin -> cold crown -> vortex
    hub -> k outlets. Outlet 0 returns direct (depth 1); the rest
    return via one rest tank each (depth 2) unless export=True, which
    sends outlet 1 to a dead sink instead."""
    g = WaterGraph()
    g.add_node("waste", elev=0, kind="waste", volume=bank)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("swirl", elev=5, kind="vortex")
    g.add_pipe("cr", "crown", "swirl", cap=1)
    g.add_pipe("ra", "swirl", "waste", cap=1)
    for i in range(1, k):
        if i == 1 and export:
            g.add_node("sink", elev=1)
            g.add_pipe("rx", "swirl", "sink", cap=1)
        else:
            g.add_node(f"t{i}", elev=3)
            g.add_pipe(f"r{i}", "swirl", f"t{i}", cap=1)
            g.add_pipe(f"r{i}b", f"t{i}", "waste", cap=1)
    return g


CLOCK_ODD_FIRST = [COND, CR, "ra: 1 to waste at waste."]
CLOCK_EVEN = [COND, CR, "r1: 1 swirl->t1."]
CLOCK_ODD_LATER = [COND, CR, "r1b: 1 to waste at waste.",
                   "ra: 1 to waste at waste."]


def test_the_orbital_clock():
    """THE ORBITAL CLOCK (probe P1r, traced): bank 4, k=2 both-return,
    one prime then one shovel per emission of ticks 1..7. The wheel
    turns ONE PER TICK for the whole window: serves == turns == 8,
    mass exactly 4 at every tick boundary, rot = serves mod 2. The
    waveform: odd ticks hold the full bank at the basin (t1) or the
    bank refilled by the direct leg plus the rest tank's drain (t3,
    t5, t7), even ticks park one unit in the rest tank. THE ARROW-KEY
    CONTROL: a serve keyed on the "swirl->" grammar never fires on a
    returning leg ("ra: 1 to waste at waste." names the waste-hold,
    not the arrow): one serve, silence from t2, the wheel dead on the
    prime's single turn."""
    g = _orbit(4, 2)
    g.boil("waste", 1)  # the prime
    serves = 1
    rows = []
    for t in range(1, 9):
        evs = g.tick()
        if t == 1:
            want = CLOCK_ODD_FIRST
        elif t % 2 == 0:
            want = CLOCK_EVEN
        else:
            want = CLOCK_ODD_LATER
        assert evs == want, (t, evs)
        if t % 2 == 1:
            assert (g.volume("waste"), g.volume("t1")) == (4, 0), t
            assert g.nodes["swirl"].rot == 1, t
        else:
            assert (g.volume("waste"), g.volume("t1")) == (3, 1), t
            assert g.nodes["swirl"].rot == 0, t
        assert _total(g) == 4, t
        rows.append(t)
        if t <= 7:
            g.boil("waste", 1)
            serves += 1
    assert rows == list(range(1, 9))
    assert serves == 8, "serves == turns == ticks"
    assert (g.volume("waste"), g.volume("t1")) == (3, 1)
    assert _total(g) == 4

    # the arrow-key control: the same board, served on the wrong key
    w = _orbit(4, 2)
    w.boil("waste", 1)
    wrong_serves = 1
    for _ in range(5):
        evs = w.tick()
        if any("swirl->" in e for e in evs):
            w.boil("waste", 1)
            wrong_serves += 1
    assert wrong_serves == 1, "the arrow key never matches a returning leg"
    assert w.nodes["swirl"].rot == 1, "the wheel died on the prime's turn"
    assert w.volume("waste") == 4 and w.volume("t1") == 0
    assert _total(w) == 4


def test_the_sky_mod_k():
    """THE SKY MOD K (probes P2/P2b on the t-tank builder, traced):
    one batch lift of N at the basin on a k=3 both-return board, no
    serve. The wheel turns EXACTLY N times over N ticks (the crown
    drains at cap 1/tick), the last rest tank drains one tick later,
    silence follows, and the park is BYTE-IDENTICAL TO BIRTH except
    rot = N mod k: N=5 reads rot 2, N=6 (a multiple) reads rot 0.
    Mass N at every tick of both runs: the modulus was computed for
    no water."""
    for N, want_rot, turns in ((5, 2, 5), (6, 0, 6)):
        g = _orbit(N, 3)
        birth = {n: g.nodes[n].volume for n in g.nodes}
        lifted = g.boil("waste", N)
        assert lifted == N
        emissions = 0
        for t in range(1, 11):
            evs = g.tick()
            assert _total(g) == N, (N, t)
            if t == 1:
                assert evs == [f"Steam condenses at crown (+{N}).", CR,
                               "ra: 1 to waste at waste."], (N, t, evs)
                assert g.volume("crown") == N - 1
            elif t <= turns:
                assert evs[0] == CR, (N, t, evs)
                assert len(evs) in (2, 3), (N, t, evs)
            elif t <= turns + 1:
                assert evs in (["r1b: 1 to waste at waste."],
                               ["r2b: 1 to waste at waste."]), (N, t, evs)
            else:
                assert evs == [], (N, t, evs)
            emissions += sum(1 for e in evs
                             if e.split(":")[0] in ("ra", "r1", "r2"))
            for nm in g.nodes:
                assert g.nodes[nm].volume >= 0
        assert emissions == N, (N, emissions)
        assert g.nodes["swirl"].rot == want_rot, (N, g.nodes["swirl"].rot)
        park = {n: g.nodes[n].volume for n in g.nodes}
        assert park == birth, (N, birth, park)
        assert _total(g) == N


def test_the_damped_orbit():
    """THE DAMPED ORBIT (probe P3r, traced): bank 4, k=2 with outlet 1
    exported to a dead sink, served per emission. The trap leaks one
    unit per 2 turns: the bank spends in exactly 2B == 8 turns (8
    acked serves, sink 4, waste 0), the register lands back at birth
    (8 mod 2 == 0), and the train asks one serve past the empty basin
    exactly once (silent at the engine layer: boil lifts 0). Silence
    from t9; mass 4 at every tick."""
    g = _orbit(4, 2, export=True)
    g.boil("waste", 1)  # the prime
    serves = 1
    dry = 0
    want_waste = (4, 3, 3, 2, 2, 1, 1, 0)
    want_sink = (0, 1, 1, 2, 2, 3, 3, 4)
    for t in range(1, 12):
        evs = g.tick()
        assert _total(g) == 4, t
        if t <= 8:
            if t % 2 == 1:
                assert evs == [COND, CR, "ra: 1 to waste at waste."], (t, evs)
            else:
                assert evs == [COND, CR, "rx: 1 swirl->sink."], (t, evs)
            assert g.volume("waste") == want_waste[t - 1], (t, g.volume("waste"))
            assert g.volume("sink") == want_sink[t - 1], (t, g.volume("sink"))
            lifted = g.boil("waste", 1)
            if lifted:
                serves += 1
            else:
                dry += 1
        else:
            assert evs == [], (t, evs)
    assert (serves, dry) == (8, 1)
    assert (g.volume("waste"), g.volume("sink")) == (0, 4)
    assert g.nodes["swirl"].rot == 0, "2B mod 2: the register lands at birth"
    assert _total(g) == 4


def test_the_world_verb_orbit_and_the_park():
    """THE WORLD-VERB ORBIT + THE PARK IS THE BIRTH STATE (probe P4,
    traced): the serve rides staged boils through MountainWorld, one
    per wheel emission. 12 served ticks at period 1 (each tick row:
    the boil line, the condense, the crown leg, that tick's outlet
    lines), 13 serves total (prime + 12), ZERO rejects: the
    both-return lap never knocks dry (contrast the banked governor's
    standing dry knock). Stop staging after t12: the staged in-flight
    serve turns ONE momentum tick (t13, rot 1), then t14 is silent,
    and the park is byte-identical to birth except the register."""
    from server.world import MountainWorld

    g = _orbit(4, 2)
    w = MountainWorld()
    w.graph = g
    w.register_session("s1", "mariner")
    assert w.stage("s1", "boil", "waste")["op"] == "ack"  # the prime
    serves = 1
    rejects = 0
    for t in range(1, 15):
        res = w.tick()
        evs = res["events"]
        assert _total(g) == 4, t
        if t <= 13:
            if t == 1:
                want = [BOIL, COND, CR, "ra: 1 to waste at waste."]
            elif t % 2 == 1:
                want = [BOIL, COND, CR, "r1b: 1 to waste at waste.",
                        "ra: 1 to waste at waste."]
            else:
                want = [BOIL, COND, CR, "r1: 1 swirl->t1."]
            assert evs == want, (t, evs)
            assert res["nodes"]["crown"] == 0, t
            assert g.nodes["swirl"].rot == t % 2, t
        else:
            assert evs == [], (t, evs)
        if t <= 12:
            outlets = ("ra", "r1")
            for _ in range(sum(1 for e in evs
                               if any(e.startswith(o + ":") for o in outlets))):
                r = w.stage("s1", "boil", "waste")
                if r["op"] == "ack":
                    serves += 1
                else:
                    rejects += 1
    assert (serves, rejects) == (13, 0)
    assert len(w.pending) == 0
    park = {n: g.nodes[n].volume for n in g.nodes}
    assert park == {"waste": 4, "crown": 0, "swirl": 0, "t1": 0}
    assert g.nodes["swirl"].rot == 1, "13 turns mod 2: the register is the only witness"
    assert _total(g) == 4


@pytest.mark.skipif(
    not (ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64.exe").exists(),
    reason="godot binary not present")
def test_the_cross_engine_orbit(tmp_path: Path):
    """THE CROSS-ENGINE ORBIT (probe P5, traced): the k=2 both-return
    orbit board through BOTH engines via the rule_parity harness, the
    instrument's first vortex-kind sequence (no vortex node appears in
    any generator family or prior parity test). 8 boil frames, one per
    tick: per-tick state hashes and verdict rows identical, all ack,
    end waste 3 and rest tank 1. NAMED LIMIT: the parity state hash
    covers no rot field (tools/rule_parity.py state_hash, the twin's
    nodes_out the same), so this pin proves volume and verdict parity,
    never register parity."""
    from tools.rule_parity import (_server_verbs, compare, run_godot,
                                   run_python)
    boil_act = {"sid": "s1", "verb": "boil", "target": "waste"}
    seq = {
        "id": "orbit_001", "family": "orbit", "ticks": 8, "sids": ["s1"],
        "nodes": [
            {"name": "waste", "elev": 0, "kind": "waste", "sill": 0,
             "volume": 4},
            {"name": "crown", "elev": 10, "kind": "cold", "sill": 0,
             "volume": 0},
            {"name": "swirl", "elev": 5, "kind": "vortex", "sill": 0,
             "volume": 0},
            {"name": "t1", "elev": 3, "kind": "plain", "sill": 0,
             "volume": 0},
        ],
        "pipes": [
            {"name": "cr", "src": "crown", "dst": "swirl", "cap": 1,
             "siphon": False, "crest": 2, "open": True},
            {"name": "ra", "src": "swirl", "dst": "waste", "cap": 1,
             "siphon": False, "crest": 2, "open": True},
            {"name": "r1", "src": "swirl", "dst": "t1", "cap": 1,
             "siphon": False, "crest": 2, "open": True},
            {"name": "r1b", "src": "t1", "dst": "waste", "cap": 1,
             "siphon": False, "crest": 2, "open": True},
        ],
        "frames": [[boil_act] for _ in range(8)],
    }
    doc = {"schema": "rule_parity.v1", "seed": 1,
           "verbs": list(_server_verbs()), "ticks_default": 8,
           "sequences": [seq]}
    py_rows = run_python(doc)
    assert len(py_rows) == 8
    for i, row in enumerate(py_rows, start=1):
        assert row["verdicts"] == ["ack"], (i, row["verdicts"])
        want_waste = 4 if i % 2 == 1 else 3
        assert row["state"]["nodes"]["waste"]["volume"] == want_waste, i
    inp = tmp_path / "orbit_in.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    gd_path = tmp_path / "orbit_gd.jsonl"
    run_godot(inp, gd_path)
    gd_rows = [json.loads(x) for x in
               gd_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(gd_rows) == len(py_rows)
    report = compare(py_rows, gd_rows)
    assert report["parity"] is True, json.dumps(
        report["first_divergence"], indent=1)
    end = py_rows[-1]["state"]["nodes"]
    assert (end["waste"]["volume"], end["t1"]["volume"]) == (3, 1)
