"""mountain_selfplay tests: the game plays itself against the REAL stack.

Every match test drives a REAL in-process TCP WorldServer on an ephemeral
port (the test_server_v0 house style): SRP6 door for the player (RFC 5054
default, M2 mutual-auth checked), plaintext hello for the spectator,
nonce-bearing actions, per-room manual ticks, and the hash-chained log
verified from disk after the world closes.

Laws under test:
  - strategy ladder: greedy ties the provable 4-tick floor on the sprint
    board; heuristic wins every board (paying a 1-tick conservation tax on
    the sprint, ending with ZERO water in waste); random is seeded and its
    tape is reproducible (byte-identical world logs across two fresh runs
    — the determinism law's self-play leg)
  - boards separate skill: greedy DNFs exactly where boiling is a trap
    (decoy peak above the crown; no cold node at all) — the win lives in
    valve discipline, not the core verb
  - the engine finding is pinned: with NO cold node, steam NEVER returns
    to liquid play (mag/water_graph's docstring promises an origin
    fallback that the code does not implement) — boil is an irreversible
    sink on no-cold boards
  - fracture fires under sustained full bore (cap-8 firehose vs threshold
    233), the spray conserves water, and the disciplined player prevents
    the wear entirely (0 stress)
  - the chain verifies after every run, from disk; a tampered log file
    refuses to reload (the append-only law)
  - the stress suite: multi-room isolation, both auth doors, chains OK,
    and the deliberate STALE_NONCE / RATE_CAP probes fire
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.water_graph import WaterGraph  # noqa: E402
from server.world import load_log_rows  # noqa: E402
from tools.mountain_selfplay import (  # noqa: E402
    _foundry,
    classify_event,
    run_match,
    stress_suite,
)


def _run(root: Path, board: str, strategy: str, seed: int = 1,
         ticks: int = 60):
    return asyncio.run(run_match(root, board, strategy, seed, max_ticks=ticks))


# ------------------------------------------------------ the strategy ladder ----

def test_greedy_ties_the_provable_floor_on_mountain(tmp_path):
    """4 is optimal for one sid (rate cap 1 action/tick, boil = +1 crown,
    win 4) — greedy must hit it exactly, zero rejects, chain green."""
    r = _run(tmp_path, "mountain", "greedy")
    assert r.won and r.win_tick == 4
    assert r.acked == 4 and r.rejects == {}
    assert r.chain_ok and r.conserved and r.steam_locked == 0
    assert r.srp_m2_ok


def test_heuristic_pays_conservation_tax_but_ends_clean(tmp_path):
    """R1 shuts the waste drain on tick 1 (one tick slower than greedy) and
    the run ends with ZERO water in waste — conservation is measurable."""
    r = _run(tmp_path, "mountain", "heuristic")
    assert r.won and r.win_tick == 5
    assert r.waste == 0 and r.crown == 4
    assert r.events.get("valve_shut", 0) >= 1
    assert r.chain_ok and r.conserved


def test_random_tape_is_reproducible(tmp_path):
    """Same seed -> byte-identical world logs from two fresh servers (the
    determinism law; SRP6 entropy and sids never enter the log)."""
    a = _run(tmp_path / "a", "mountain", "random", seed=7, ticks=30)
    b = _run(tmp_path / "b", "mountain", "random", seed=7, ticks=30)
    assert a.won == b.won and a.win_tick == b.win_tick and a.acked == b.acked
    log_a = (tmp_path / "a" / "mountain.random.s7.jsonl").read_bytes()
    log_b = (tmp_path / "b" / "mountain.random.s7.jsonl").read_bytes()
    assert log_a == log_b


# ------------------------------------------------- boards separate skill ----

def test_greedy_vapor_locks_foundry_heuristic_wins(tmp_path):
    """No cold node: every boil permanently locks a unit out of liquid
    play. Greedy boils all 8 units and DNFs; heuristic plays one valve
    (xor discipline) and lets gravity win."""
    greedy = _run(tmp_path, "foundry", "greedy", ticks=14)
    assert not greedy.won
    assert greedy.steam_locked == 8      # the whole economy, vaporized
    assert greedy.acked == 8             # eight boils, nothing else
    assert greedy.chain_ok and greedy.conserved

    smart = _run(tmp_path, "foundry", "heuristic")
    assert smart.won and smart.win_tick == 4
    assert smart.acked == 1              # ONE valve move, then gravity
    assert smart.steam_locked == 0 and smart.crown == 4
    assert smart.events.get("junction_pass", 0) >= 3


def test_shrine_decoy_peak_traps_greedy(tmp_path):
    """A taller cold node over the crown eats every boil. Greedy parks its
    water on the outlet-less peak and DNFs; heuristic never boils."""
    greedy = _run(tmp_path, "shrine", "greedy", ticks=20)
    assert not greedy.won
    assert greedy.events.get("condense", 0) >= 4   # steam fed the PEAK
    assert greedy.chain_ok and greedy.conserved

    smart = _run(tmp_path, "shrine", "heuristic")
    assert smart.won and smart.win_tick == 4
    assert smart.acked == 1 and smart.waste == 0   # shut the leak, gravity


def test_spelunk_fracture_fires_and_spray_conserves(tmp_path):
    """The cap-8 firehose runs full bore every tick: stress +8/tick against
    threshold 233 -> it FRACTURES, and the burst spray lands on the lowest
    node (the crown), finishing the fill early — while water stays
    conserved. Heuristic shuts the drain on tick 1: no wear, no burst."""
    greedy = _run(tmp_path, "spelunk", "greedy", ticks=31)
    assert greedy.won and greedy.win_tick == 30
    assert greedy.fractures == ["p_a1"]
    assert greedy.events.get("fracture", 0) == 1
    assert greedy.crown == 38            # 30 by needle + 8 by burst spray
    assert greedy.conserved and greedy.chain_ok
    assert greedy.stress["p_a1"] > 233

    smart = _run(tmp_path, "spelunk", "heuristic")
    assert smart.won and smart.win_tick == 30
    assert smart.fractures == [] and smart.stress["p_a1"] == 0
    assert smart.acked == 1 and smart.waste == 0


# ------------------------------------------------------ the engine finding ----

def test_no_cold_node_locks_steam_forever():
    """PINNED SPEC/CODE DIVERGENCE: water_graph's docstring says steam
    "falls back to its origin node when no cold node exists" — the code
    has no fallback. On a no-cold board a boil is an irreversible sink:
    the liquid never comes back, on any later tick."""
    g = _foundry()
    g.boil("forgeA", 2)
    for _ in range(5):
        g.tick()
    forge = g.nodes["forgeA"]
    assert forge.steam == 2                       # never condensed
    assert sum(n.volume for n in g.nodes.values()) == 8 - 2  # out of play
    assert not any(n.kind == "cold" for n in g.nodes.values())


def test_classify_event_reads_the_ledger_grammar():
    users = ("SP-GREEDY", "watcher", "innkeeper")
    assert classify_event("SP-GREEDY boils 1 at spring; it rises.", users) == "boil_rise"
    assert classify_event("Steam condenses at crown (+1).", users) == "condense"
    assert classify_event("p_spring: 1 spring->gate1.", users) == "pipe_flow"
    assert classify_event("p_drain: 1 to waste at waste.", users) == "waste_fill"
    assert classify_event("Junction gate1 holds 1 below gate (2 inlets); pooling.", users) == "junction_hold"
    assert classify_event("Pipe p_a1 FRACTURES (stress 240): spray to crown.", users) == "fracture"
    assert classify_event("innkeeper: The crown is dry.", users) == "say"
    assert classify_event("something novel", users) == "other"


# ------------------------------------------------------------- the chain ----

def test_chain_reload_refuses_a_tampered_log(tmp_path):
    """The append-only law has teeth: a junk row appended to the log file
    makes the reload refuse (in-memory chain of the finished run is
    already verified inside run_match — this is the DISK instrument)."""
    r = _run(tmp_path, "mountain", "heuristic", ticks=5)
    assert r.chain_ok and r.chain_rows > 0
    log = tmp_path / "mountain.heuristic.s1.jsonl"
    with log.open("a", encoding="utf-8") as fh:
        fh.write('{"seq": 999, "prev": "0" * 64, "sha": "deadbeef"}\n')
    try:
        load_log_rows(log)
        raised = False
    except ValueError:
        raised = True
    assert raised, "a tampered log must refuse to load"


# --------------------------------------------------------- the stack stress ----

def test_stress_suite_rooms_doors_anticheat(tmp_path):
    """Four rooms' worth of surface in one server: 3 rooms, 7 clients over
    BOTH auth doors, isolation (every client saw exactly its room's ticks,
    same bytes as its room-mates), every room's chain verified from disk,
    water conserved per room, and both deliberate anti-cheat probes
    (replayed nonce, same-tick second action) rejected by law."""
    out = asyncio.run(stress_suite(tmp_path, ticks=12))
    checks = out["checks"]
    assert checks["all_chains_ok"]
    assert checks["isolation"]
    assert checks["water_conserved"]
    assert checks["stale_nonce_fired"], out["probes"]
    assert checks["rate_cap_fired"], out["probes"]
    assert checks["actions_staged_matches"]
    assert out["stats"]["srp_sessions"] == 3    # the three SRP6-door seats
    assert len(out["rooms"]) == 3 and len(out["clients"]) == 7
    doors = {c["door"] for c in out["clients"]}
    assert doors == {"srp6", "plain"}


def test_water_graph_roundtrip_on_boards(tmp_path):
    """Every harness board round-trips through the estate spec (the LW5/AC2
    law: primed siphons and burst pipes survive) and conserves water on a
    dry physics run (no actions: gravity alone never deletes volume)."""
    from mag.water_graph import from_spec
    from tools.mountain_selfplay import BOARDS

    for name, (builder, _win) in BOARDS.items():
        g: WaterGraph = builder()
        total = sum(n.volume for n in g.nodes.values())
        spec = g.to_spec()
        h = from_spec(spec)
        assert h.to_spec() == spec, name
        for _ in range(10):
            g.tick()
        now = sum(n.volume for n in g.nodes.values()) + sum(n.steam for n in g.nodes.values())
        assert now == total, (name, now, total)
