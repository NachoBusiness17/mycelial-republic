"""banked governor tests - the gauge-line serve, the floor tax, and
the cross-engine verdict (mariner cycle 13, 2026-10-20).

THE BANKED GOVERNOR, the cycle-12 receipt's self-chosen NEXT THREAD,
landed with ZERO engine bytes: every pin here composes kinds the
engine already has. Laws: (1) THE GAUGE-LINE SERVE: one prime shovel
then one per reader open runs the wheel unattended at one serve per
two ticks, the lag stretches the period and eats nothing; (2) THE
PRIME LAW HOLDS AT THE GAUGE: a sub-level prime strands the bank;
(3) THE FLOOR TAX: the primed sill-2 governor serves N-1 and parks
the level-1 blind spot; (4) THE DRY KNOCK: the train asks one serve
past the bank, exactly 1 rejected stage per spent bank (pinned
inside the serve and floor tests' drivers); (5) THE ORDER IS THE
METER: drain-first keeps the balance split behind any tap cap,
tap-first meters the full stream and balloons its reader; (6) THE
METER'S FLOOR: cap-1 floors at level-1, cap-2 reads to the bank's
residue mod the cap; (7) THE CROSS-ENGINE VERDICT: the governor
board runs both engines through the rule_parity harness.
Spec: mag/water_graph.py module docstring, THE BANKED GOVERNOR
block; receipt watch/inbox/mates_leave_protocol/receipts/
receipt_20261020_mariner.md.
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


def _total(g: WaterGraph) -> int:
    return sum(n.volume + n.steam for n in g.nodes.values())


def _gov_board(bank: int, sill: int) -> WaterGraph:
    """The banked governor: waste basin of bank, cold crown, store
    latch L, reader latch R (sill 1), counter sink; legs cl
    (crown->L), tap (L->R), ro (R->sink)."""
    g = WaterGraph()
    g.add_node("waste", elev=0, kind="waste", volume=bank)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("L", elev=4, kind="latch", sill=sill)
    g.add_node("R", elev=2, kind="latch", sill=1)
    g.add_node("sink", elev=1)
    g.add_pipe("cl", "crown", "L", cap=1)
    g.add_pipe("tap", "L", "R", cap=1)
    g.add_pipe("ro", "R", "sink", cap=1)
    return g


def _run_governor(bank: int, sill: int, prime: int,
                  max_ticks: int = 40):
    """The unattended serve loop through the world-verb layer:
    stage the prime, then one shovel per "Latch R opens" line of
    the previous tick, riding to 6 silent ticks. Returns the tick
    trace, the acked shovel count, the rejected stage count."""
    from server.world import MountainWorld

    g = _gov_board(bank, sill)
    w = MountainWorld()
    w.graph = g
    w.register_session("s1", "mariner")
    for _ in range(prime):
        w.stage("s1", "boil", "waste")
    shovels = prime
    rejects = 0
    trace = []
    silent = 0
    for _t in range(max_ticks):
        res = w.tick()
        evs = res["events"]
        trace.append((evs, res["nodes"]))
        assert _total(g) == bank
        if not evs and not w.pending:
            silent += 1
            if silent >= 6:
                break
        else:
            silent = 0
        for _ in range(sum(1 for e in evs if e.startswith("Latch R opens"))):
            if w.stage("s1", "boil", "waste")["op"] == "ack":
                shovels += 1
            else:
                rejects += 1
    return g, trace, shovels, rejects


BOIL = "mariner boils 1 at waste; it rises."
RAIN1 = "Steam condenses at crown (+1)."
SERVE1 = [BOIL, RAIN1, "cl: 1 crown->L.",
          "Latch L opens (pool 1 >= level 1).", "tap: 1 L->R."]
READ1 = ["Latch R opens (pool 1 >= level 1).", "ro: 1 R->sink."]


def test_the_gauge_line_serve_runs_unattended():
    """THE GAUGE-LINE SERVE (probe P1, traced): bank 6, sill 1,
    one prime shovel. The wheel runs unattended at one serve per
    TWO ticks: prime at t1, reader opens t2,t4,t6,t8,t10,t12, the
    chases land t3,t5,t7,t9,t11, the sink ends at 6, the bank is
    empty, silence from t13. The lag stretches the period but eats
    nothing; the first serve is never eaten."""
    g, trace, shovels, rejects = _run_governor(6, 1, 1)
    assert len(trace) == 18
    for i, (evs, nodes) in enumerate(trace, start=1):
        if i == 1 or i % 2 == 1 and i <= 11:
            assert evs == SERVE1, (i, evs)
        elif i <= 12:
            assert evs == READ1, (i, evs)
        else:
            assert evs == [], (i, evs)
        want_waste = 5 - (i - 1) // 2 if i <= 12 else 0
        assert nodes["waste"] == want_waste, (i, nodes)
        want_sink = i // 2 if i <= 12 else 6
        assert nodes["sink"] == want_sink, (i, nodes)
        assert _total(g) == 6, i
    assert (g.volume("waste"), g.volume("crown"), g.volume("L"),
            g.volume("R"), g.volume("sink")) == (0, 0, 0, 0, 6)
    assert shovels == 6 and rejects == 1


def test_the_prime_law_holds_at_the_gauge():
    """THE PRIME LAW HOLDS AT THE GAUGE (probe P2a, traced): bank 6,
    sill 2, ONE prime shovel: the store pools 1 and holds, zero
    reader opens fire, the governor never starts: 7 ticks, zero
    serves, bank 5 stranded at the basin, the hostage pool 1."""
    g, trace, shovels, rejects = _run_governor(6, 2, 1)
    assert len(trace) == 7
    assert trace[0][0] == [BOIL, RAIN1,
                           "Latch L holds pool 1 below level 2; pooling."]
    assert trace[0][1] == {"waste": 5, "crown": 0, "L": 1,
                           "R": 0, "sink": 0}
    for i in range(2, 8):
        assert trace[i - 1][0] == [], (i, trace[i - 1][0])
    assert (g.volume("waste"), g.volume("L"), g.volume("sink")) == (5, 1, 0)
    assert shovels == 1 and rejects == 0


def test_the_floor_tax_parks_the_blind_spot():
    """THE FLOOR TAX (probe P2b, traced): bank 6, sill 2, prime 2.
    The 2-prime through the cap-1 sense leg parks one hostage at
    the crown for one tick (the wheel starts at t2, first reader
    open t3), then the train serves at period 2: opens t3,t5,t7,
    t9,t11, five serves, the store sleeps at the level-1 blind
    spot, and the last open knocks on the empty basin (1 reject)."""
    g, trace, shovels, rejects = _run_governor(6, 2, 2)
    assert len(trace) == 17
    serve2 = [BOIL, RAIN1, "cl: 1 crown->L.",
              "Latch L opens (pool 2 >= level 2).", "tap: 1 L->R."]
    for i, (evs, nodes) in enumerate(trace, start=1):
        if i == 1:
            assert evs == [BOIL, BOIL,
                           "Steam condenses at crown (+2).",
                           "Latch L holds pool 1 below level 2; pooling."]
            assert nodes["crown"] == 1 and nodes["L"] == 1, (i, nodes)
        elif i == 2:
            assert evs == ["cl: 1 crown->L.",
                           "Latch L opens (pool 2 >= level 2).",
                           "tap: 1 L->R."], (i, evs)
        elif i % 2 == 1 and i <= 11:
            assert evs == READ1, (i, evs)
        elif i <= 10:
            assert evs == serve2, (i, evs)
        else:
            assert evs == [], (i, evs)
        want_waste = {1: 4, 2: 4, 3: 4, 4: 3, 5: 3, 6: 2, 7: 2,
                      8: 1, 9: 1, 10: 0}.get(i, 0)
        assert nodes["waste"] == want_waste, (i, nodes)
        assert _total(g) == 6, i
    assert (g.volume("waste"), g.volume("crown"), g.volume("L"),
            g.volume("R"), g.volume("sink")) == (0, 0, 1, 0, 5)
    assert shovels == 6 and rejects == 1


def test_the_dry_knock():
    """THE DRY KNOCK (both drivers, traced): the train always asks
    one serve past the bank: the last reader open stages a shovel
    the empty basin rejects at stage time. Exactly 1 rejected
    stage on every spent bank: the sill-1 wheel (bank 6) and the
    sill-2 wheel (bank 6) each end with shovels == bank served or
    served+floor and rejects == 1."""
    _, _, shovels1, rejects1 = _run_governor(6, 1, 1)
    _, _, shovels2, rejects2 = _run_governor(6, 2, 2)
    assert (shovels1, rejects1) == (6, 1)
    assert (shovels2, rejects2) == (6, 1)
    assert shovels1 + rejects1 == 7 and shovels2 + rejects2 == 7


def _meter_board(tap_first: bool, bank: int = 8) -> WaterGraph:
    g = WaterGraph()
    g.add_node("waste", elev=0, kind="waste", volume=bank)
    g.add_node("crown", elev=10, kind="cold")
    g.add_node("L", elev=4, kind="latch", sill=2)
    g.add_node("R", elev=2, kind="latch", sill=1)
    g.add_node("sink", elev=1)
    g.add_pipe("cl", "crown", "L", cap=2)
    if tap_first:
        g.add_pipe("tap", "L", "R", cap=2)
        g.add_pipe("ol", "L", "waste", cap=1)
    else:
        g.add_pipe("ol", "L", "waste", cap=1)
        g.add_pipe("tap", "L", "R", cap=2)
    g.add_pipe("ro", "R", "sink", cap=1)
    return g


def test_the_order_is_the_meter():
    """THE ORDER IS THE METER (probes P3i and P3ii, traced): the
    live-wire board with a cap-2 tap under the 8-unit wind. Drain
    first: the balance split holds (4 of 8 to the sink; the drain
    takes its unit, the tap passes min(cap, remainder): the cap is
    invisible behind the order). Tap first: the FULL stream (8 of
    8) and the reader balloons +1/tick while the wind lasts (pool
    2,3,4,5), draining the backlog 1/tick after the wind dies (the
    sink's last unit 5 ticks after the last served tick). Mass 8
    conserved at every tick, both boards."""
    for tap_first in (False, True):
        g = _meter_board(tap_first)
        g.boil("waste", 2)
        for t in range(1, 13):
            evs = g.tick()
            if t <= 3:
                g.boil("waste", min(2, g.volume("waste")))
            assert _total(g) == 8, (tap_first, t)
            if not tap_first:
                if t == 1:
                    assert evs == ["Steam condenses at crown (+2).",
                                   "cl: 2 crown->L.",
                                   "Latch L opens (pool 2 >= level 2).",
                                   "ol: 1 to waste at waste.",
                                   "tap: 1 L->R."], (t, evs)
                elif t <= 4:
                    assert evs == ["Steam condenses at crown (+2).",
                                   "cl: 2 crown->L.",
                                   "Latch L opens (pool 2 >= level 2).",
                                   "Latch R opens (pool 1 >= level 1).",
                                   "ol: 1 to waste at waste.",
                                   "tap: 1 L->R.",
                                   "ro: 1 R->sink."], (t, evs)
                elif t == 5:
                    assert evs == ["Latch R opens (pool 1 >= level 1).",
                                   "ro: 1 R->sink."], (t, evs)
                else:
                    assert evs == [], (t, evs)
            else:
                if t == 1:
                    assert evs == ["Steam condenses at crown (+2).",
                                   "cl: 2 crown->L.",
                                   "Latch L opens (pool 2 >= level 2).",
                                   "tap: 2 L->R."], (t, evs)
                elif t <= 4:
                    assert evs == ["Steam condenses at crown (+2).",
                                   "cl: 2 crown->L.",
                                   "Latch L opens (pool 2 >= level 2).",
                                   f"Latch R opens (pool {t} >= level 1).",
                                   "tap: 2 L->R.",
                                   "ro: 1 R->sink."], (t, evs)
                elif t <= 9:
                    assert evs == [f"Latch R opens (pool {10 - t} "
                                   f">= level 1).", "ro: 1 R->sink."], (t, evs)
                else:
                    assert evs == [], (t, evs)
        if not tap_first:
            assert (g.volume("sink"), g.volume("R"), g.volume("L"),
                    g.volume("waste")) == (4, 0, 0, 4)
        else:
            assert (g.volume("sink"), g.volume("R"), g.volume("L"),
                    g.volume("waste")) == (8, 0, 0, 0)


def test_the_meters_floor():
    """THE METER'S FLOOR (probes P4a, P4b, P4c, P4d, traced): the
    terminal pool is the first value below the level in the descent
    bank, bank-cap, bank-2cap, ...: a cap-1 tap floors at level-1
    regardless of the bank (stored 6 reads 5); a cap-2 tap reads
    past that floor to the residue mod the cap (stored 6 reads 6,
    opens at 6, 4, 2; stored 5 reads 4; stored 7 reads 6). Mass 6
    or 7 conserved at every tick, all boards."""
    g = WaterGraph()
    g.add_node("L", elev=4, kind="latch", sill=2, volume=6)
    g.add_node("R", elev=2, kind="latch", sill=1)
    g.add_node("sink", elev=1)
    g.add_pipe("tap", "L", "R", cap=1)
    g.add_pipe("ro", "R", "sink", cap=1)
    for t in range(1, 7):
        evs = g.tick()
        if t == 1:
            assert evs == ["Latch L opens (pool 6 >= level 2).",
                           "tap: 1 L->R."], (t, evs)
        elif t <= 5:
            assert evs == [f"Latch L opens (pool {7 - t} >= level 2).",
                           "Latch R opens (pool 1 >= level 1).",
                           "tap: 1 L->R.", "ro: 1 R->sink."], (t, evs)
        else:
            assert evs == ["Latch R opens (pool 1 >= level 1).",
                           "ro: 1 R->sink."], (t, evs)
        assert _total(g) == 6, t
    assert g.volume("L") == 1 and g.volume("sink") == 5

    for stored, want_sink, opens in ((6, 6, (6, 4, 2)),
                                     (5, 4, (5, 3)),
                                     (7, 6, (7, 5, 3))):
        wide = WaterGraph()
        wide.add_node("L", elev=4, kind="latch", sill=2, volume=stored)
        wide.add_node("R", elev=2, kind="latch", sill=1)
        wide.add_node("sink", elev=1)
        wide.add_pipe("tap", "L", "R", cap=2)
        wide.add_pipe("ro", "R", "sink", cap=1)
        store_opens = []
        for t in range(1, 14):
            evs = wide.tick()
            assert _total(wide) == stored, (stored, t)
            heads = [e for e in evs if e.startswith("Latch L opens")]
            if heads:
                store_opens.append(heads[0])
        assert store_opens == [f"Latch L opens (pool {p} >= level 2)."
                               for p in opens], (stored, store_opens)
        assert wide.volume("sink") == want_sink, stored
        assert _total(wide) == stored, stored


@pytest.mark.skipif(
    not (ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64.exe").exists(),
    reason="godot binary not present")
def test_the_cross_engine_verdict(tmp_path: Path):
    """THE CROSS-ENGINE VERDICT (probe P5, traced): the banked
    governor board through BOTH engines via the rule_parity
    harness: 12 ticks, per-tick state hashes and verdict rows
    identical, including a reject:RATE_CAP row (the receipt
    ladder's per-tick action cap ate the second prime) both
    engines agree on. Ladder parity on a composition board, not
    just the stress family."""
    from tools.rule_parity import (_server_verbs, compare, run_godot,
                                   run_python)
    boil_act = {"sid": "s1", "verb": "boil", "target": "waste"}
    frames = [[boil_act, boil_act]] + [[] for _ in range(11)]
    for i in (3, 5, 7, 9, 11):
        frames[i] = [boil_act]
    seq = {
        "id": "gov_banked_001", "family": "banked_governor", "ticks": 12,
        "sids": ["s1"],
        "nodes": [
            {"name": "waste", "elev": 0, "kind": "waste", "sill": 0,
             "volume": 6},
            {"name": "crown", "elev": 10, "kind": "cold", "sill": 0,
             "volume": 0},
            {"name": "L", "elev": 4, "kind": "latch", "sill": 2,
             "volume": 0},
            {"name": "R", "elev": 2, "kind": "latch", "sill": 1,
             "volume": 0},
            {"name": "sink", "elev": 1, "kind": "plain", "sill": 0,
             "volume": 0},
        ],
        "pipes": [
            {"name": "cl", "src": "crown", "dst": "L", "cap": 1,
             "siphon": False, "crest": 2, "open": True},
            {"name": "tap", "src": "L", "dst": "R", "cap": 1,
             "siphon": False, "crest": 2, "open": True},
            {"name": "ro", "src": "R", "dst": "sink", "cap": 1,
             "siphon": False, "crest": 2, "open": True},
        ],
        "frames": frames,
    }
    doc = {"schema": "rule_parity.v1", "seed": 1,
           "verbs": list(_server_verbs()), "ticks_default": 12,
           "sequences": [seq]}
    py_rows = run_python(doc)
    assert len(py_rows) == 12
    assert py_rows[0]["verdicts"] == ["ack", "reject:RATE_CAP"]
    inp = tmp_path / "gov_in.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    gd_path = tmp_path / "gov_gd.jsonl"
    run_godot(inp, gd_path)
    gd_rows = [json.loads(x) for x in
               gd_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(gd_rows) == len(py_rows)
    report = compare(py_rows, gd_rows)
    assert report["parity"] is True, json.dumps(
        report["first_divergence"], indent=1)
    end = py_rows[-1]["state"]["nodes"]
    assert (end["waste"]["volume"], end["L"]["volume"],
            end["R"]["volume"], end["sink"]["volume"]) == (0, 1, 1, 4)
