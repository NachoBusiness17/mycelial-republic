"""LM4 tests: tools/mountain_units.py — the DFHack-style units inspector.

Laws under test (receipt watch/inbox/last_mile_20260930/LM4_UNITS.md):
  - decide() is the fish_brain.gd port: pure, deterministic, branch order
    threat -> tire window -> pool pull -> wiggle, with the exact Q8 law
  - every emitted row passes the REAL MOTION_TABLE gate (the X9 dialect);
    an illegal row would be a loud UnitsError, never a silent fallback
  - the rig applies rows faithfully: flee spends fatigue (dt/COAST_TIME),
    catch fires only inside CATCH_RADIUS with fatigue > TIRED
  - determinism: spawn jitter is the only RNG (random.Random(seed), default
    20260929, game.gd:180's own seed); same (ticks, seed, player) in, same
    bytes out; a different seed moves the school
  - the board is the estate's own organ: unboiled, it drains to waste by
    water tick 8 (frame 240), so wettest honestly goes "" (dry)
  - POP_CAP law (flock.gd:22): add_fish returns -1 at cap; headroom = cap
    minus alive
  - `unit <id> --trace` returns the fish's full motion-row history plus the
    caught event that ended it; CLI typed errors exit 2
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.protocol_table import MOTION_DISPATCH  # noqa: E402
from tools.mountain_units import (  # noqa: E402
    BOARD,
    FLEE_RADIUS,
    POP_CAP,
    SPAWN_COUNT,
    FishSchool,
    MountainUnits,
    UnitsError,
    _pool_by,
    decide,
    dist,
    main as cli_main,
    q8,
)

POOLS = MountainUnits(seed=1, player_mode="still").pools


def _snap(fish, player, pools=POOLS, wettest="spring"):
    return {"fish": fish, "player_pos": player, "pools": pools,
            "wettest": wettest}


def _fish(pos=(200.0, 300.0), fatigue=0.0, alive=True):
    return {"pos": pos, "vel": (0.0, 0.0), "fatigue": fatigue, "alive": alive}


# ------------------------------------------------------------- the q8 law ----

@pytest.mark.parametrize("x,expect", [
    (-1.0, 0), (0.0, 0), (1.0, 255), (2.0, 255),          # clamp law
    (0.5, 128), (127.5 / 255.0, 128),                      # half away from 0
    (0.25, 64),
])
def test_q8_clamps_and_rounds_half_away_from_zero(x, expect):
    # Godot round() is half-away-from-zero; Python round() is banker's —
    # the port must not drift on exact .5 boundaries
    assert q8(x) == expect


# ------------------------------------------------------ decide() fidelity ----

def test_dead_or_unknown_fish_idles_at_the_wettest_pool():
    row = decide(-1, 7, _snap([_fish()], (900.0, 100.0)))
    assert row == {"verb": "idle", "intensity_q8": 0, "dir": "spring"}
    assert decide(0, 7, _snap([_fish(alive=False)], (900.0, 100.0))) == row


def test_threat_inside_flee_radius_flees_to_the_far_pool():
    fish = _fish(pos=(130.0, 240.0))                       # at the spring
    player = (135.0, 240.0)                                # 5px away: threat
    row = decide(0, 9, _snap([fish], player))
    assert row["verb"] == "flee"
    assert row["intensity_q8"] == q8(1.0 - 5.0 / FLEE_RADIUS)
    assert row["dir"] == _pool_by(player, POOLS, far=True)  # escape target
    assert row["dir"] == "crown"                            # farthest from player


def test_tired_fish_is_carried_by_the_schools_pull():
    row = decide(0, 9, _snap([_fish(fatigue=0.8)], (900.0, 100.0)))
    assert row == {"verb": "carry", "intensity_q8": q8(0.8), "dir": "spring"}


def test_fresh_fish_beyond_the_prefer_ring_pursues_the_wettest():
    row = decide(0, 9, _snap([_fish(pos=(700.0, 500.0))], (900.0, 100.0)))
    d_home = dist((700.0, 500.0), POOLS["spring"])
    assert d_home > 30.0
    assert row == {"verb": "pursue", "intensity_q8": q8(d_home / 38.0),
                   "dir": "spring"}


def test_alone_and_fresh_idles_near_its_pool():
    row = decide(0, 9, _snap([_fish(pos=(131.0, 241.0))], (900.0, 100.0)))
    assert row["verb"] == "idle"
    assert row["intensity_q8"] == q8(1.0 - 0.0) == 255      # fully rested
    assert row["dir"] == _pool_by((131.0, 241.0), POOLS, far=False)


def test_schoolmates_within_school_radius_dance():
    two = [_fish(pos=(130.0, 240.0)), _fish(pos=(140.0, 248.0))]
    row = decide(0, 13, _snap(two, (900.0, 100.0)))
    assert row["verb"] == "dance"
    assert row["intensity_q8"] == q8(
        (__import__("math").sin(13 * 0.7 + 130.0 * 0.05) + 1.0) / 2.0)


def test_decide_is_pure_no_input_mutation():
    snap = _snap([_fish(), _fish(pos=(50.0, 50.0))], (10.0, 10.0))
    before = copy.deepcopy(snap)
    a = decide(0, 21, snap)
    b = decide(0, 21, snap)
    assert a == b                          # same inputs, same row bytes
    assert snap == before                  # the snapshot is never mutated


def test_every_decide_row_passes_the_real_motion_table():
    targets = frozenset(POOLS)
    for fish_id, tick in [(0, 1), (0, 999), (1, 42)]:
        snap = _snap([_fish(), _fish(pos=(140.0, 248.0), fatigue=0.9)],
                     (132.0, 241.0))
        row = decide(fish_id, tick, snap)
        ask = MOTION_DISPATCH.ask(row["verb"], "AUTHED",
                                  {"intensity_q8": row["intensity_q8"],
                                   "dir": row["dir"]}, targets)
        assert ask["ok"] is True, (row, ask)


# --------------------------------------------------------- the rig laws ----

def test_hunt_run_gates_every_row_and_catches_tired_fish():
    sim = MountainUnits(seed=20260929, player_mode="hunt")
    sim.run(600)  # would raise UnitsError on any illegal row (none: passes)
    s = sim.summary()
    assert s["spawned"] == SPAWN_COUNT
    assert s["dead"] >= 1                    # the hunter caught tired fish
    assert s["alive"] == SPAWN_COUNT - s["dead"]
    observed = set()
    for fid in range(SPAWN_COUNT):
        trace = sim.trace(fid)
        observed.update(r["verb"] for r in trace if "verb" in r)
        last = trace[-1]
        if sim.unit_row(fid)["alive"] is False:
            assert last["event"] == "caught"
            # the flock.gd:77 catch window: fatigue was strictly > 0.7 at the
            # catch (a 0.7000x value rounds to 0.7 at the trace's 4 decimals)
            assert last["fatigue"] >= 0.7
            assert sim.unit_row(fid)["killed_at"] == last["tick"]
        assert sim.unit_row(fid)["age_in_state_frames"] <= 600
    assert observed <= {"idle", "flee", "pursue", "carry", "dance"}
    assert {"flee", "pursue", "dance"} <= observed   # the lane really fires


def test_still_player_never_threatens_the_school():
    sim = MountainUnits(seed=20260929, player_mode="still")
    sim.run(300)
    assert sim.player == (BOARD[0], BOARD[1])
    s = sim.summary()
    assert s["dead"] == 0
    for fid in range(SPAWN_COUNT):
        verbs = {r["verb"] for r in sim.trace(fid) if "verb" in r}
        assert "flee" not in verbs and "carry" not in verbs
        assert verbs <= {"idle", "pursue", "dance"}


def test_transitions_summary_counts_every_state_change():
    sim = MountainUnits(seed=7, player_mode="hunt")
    sim.run(400)
    total = sum(u["transitions"] for u in sim.dump()["units"])
    assert sim.summary()["transitions"] == total > 0


# -------------------------------------------------------- determinism ----

def test_same_seed_same_player_same_bytes():
    a = MountainUnits(seed=11, player_mode="hunt")
    b = MountainUnits(seed=11, player_mode="hunt")
    a.run(300)
    b.run(300)
    assert json.dumps(a.dump(), sort_keys=True) == json.dumps(b.dump(), sort_keys=True)
    assert a.trace(3) == b.trace(3)


def test_different_seed_moves_the_school():
    a = MountainUnits(seed=1, player_mode="still")
    b = MountainUnits(seed=2, player_mode="still")
    assert a.unit_row(0)["pos"] != b.unit_row(0)["pos"]


def test_default_seed_is_the_slices_own_seed():
    assert MountainUnits().seed == 20260929   # game.gd:180


# ------------------------------------------------- board + pop_cap laws ----

def test_unboiled_board_drains_to_waste_and_wettest_goes_dry():
    sim = MountainUnits(seed=1, player_mode="still")
    sim.run(240)  # 8 water ticks: the estate organ holds all 8 units in waste
    assert sim.wettest() == ""
    sim.run(60)
    assert sim.summary()["wettest"] == ""     # dry is reported, never faked


def test_pop_cap_law_and_headroom():
    school = FishSchool()
    ids = [school.add_fish((0.0, 0.0)) for _ in range(POP_CAP)]
    assert ids[-1] == POP_CAP - 1
    assert school.add_fish((0.0, 0.0)) == -1   # flock.gd:22: the cap refuses
    sim = MountainUnits(seed=1, player_mode="still")
    sim.run(1)
    assert sim.summary()["headroom"] == POP_CAP - SPAWN_COUNT


def test_cell_is_the_board_anchored_20px_tile():
    sim = MountainUnits(seed=1, player_mode="still")
    assert sim.cell((BOARD[0], BOARD[1])) == (0, 0)
    assert sim.cell((BOARD[2] - 0.1, BOARD[3] - 0.1)) == (55, 30)
    assert sim.cell((BOARD[0] + 20.0, BOARD[1])) == (1, 0)


# ------------------------------------------------------------------ CLI ----

def test_cli_units_json_exits_zero_and_parses(capsys):
    assert cli_main(["units", "--ticks", "60", "--json"]) == 0
    doc = json.loads(capsys.readouterr().out)
    assert doc["schema"] == "mountain_units.v1"
    assert len(doc["units"]) == SPAWN_COUNT
    assert doc["summary"]["pop_cap"] == POP_CAP


def test_cli_unit_trace_and_typed_errors(capsys):
    assert cli_main(["unit", "0", "--ticks", "30", "--trace"]) == 0
    out = capsys.readouterr().out
    assert "trace:" in out and "rows" in out
    assert cli_main(["unit", "99", "--ticks", "5"]) == 2
    assert "unknown unit id 99" in capsys.readouterr().err
    assert cli_main(["units", "--ticks", "0"]) == 2
    # argparse owns the bad-choice reject: its exit code is 2 as well
    with pytest.raises(SystemExit) as exc:
        cli_main(["units", "--player", "ghost", "--ticks", "5"])
    assert exc.value.code == 2
