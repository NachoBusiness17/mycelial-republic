"""LM9 positive-flock tests: the food-gradient steering law, the threat
mirror's fidelity to flock.gd, and the A/B verdict (operator law 2026-09-30:
positive mode moves the school with fewer panic errors than threat mode).

Laws under test (receipt watch/inbox/last_mile_20260930/LM9_POSITIVE_FLOCK.md):
  - THREAT MIRROR FIDELITY: mag/flock_positive.py step_threat carries
    flock.gd's V6 tuning byte-for-byte (constants parse-equal from both
    files: FLEE_RADIUS 20, push 6.0, tire dt/COAST_TIME) and the tire law
    holds: ~0.8s of continuous fleeing spends a fish (fatigue 1.0).
  - POSITIVE MODE: food ATTRACTS (fish moves toward food), feeding converts
    food units to satiation, a full fish does not bite, digestion spends
    satiation, food depletes, and the pull scales with hunger
    (explore-vs-exploit: hungry exploit the gradient, fed fish explore).
  - NO PANIC BY CONSTRUCTION: a positive-mode episode logs zero flee-state
    entries; a threat episode with a chasing cursor logs panic.
  - A/B VERDICT (same board, same seed, same budget, same target): positive
    reaches 80% of the school at target strictly sooner-or-equal, with fewer
    panic entries and tighter (never looser) cohesion. The threat policy
    census shows no single-cursor threat policy transits the school.
  - FLAG GATE: flock.gd defaults to threat (positive := false) and gates the
    catch window on `not positive`, so the landed game is byte-identical to
    V6's tuning until the operator opts into positive mode.
"""
from __future__ import annotations

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import flock_positive as fp  # noqa: E402
from mag import flock_positive_ab as fab  # noqa: E402

FLOCK_GD = ROOT / "roblox_to_godot" / "systems" / "flock.gd"


# ------------------------------------------------ threat mirror fidelity ----

# R4 2026-09-30 (Q15/R7): flock.gd's shared-family constants are now
# ALIASES of systems/game_constants.gd (`const FLEE_RADIUS := GC.FLEE_RADIUS`)
# so the pin resolves through the single source; only flock-local literals
# (SEP_RADIUS + the LM9 food law) still parse from flock.gd itself.
GC_GD = ROOT / "roblox_to_godot" / "systems" / "game_constants.gd"
_GC_ALIASED = {  # flock.gd name -> game_constants.gd name
    "FLEE_RADIUS": "FLEE_RADIUS", "CATCH_RADIUS": "CATCH_RADIUS",
    "SCHOOL_RADIUS": "SCHOOL_RADIUS", "FATIGUE_DECAY": "FATIGUE_DECAY",
    "DRAG": "DRAG", "COAST_TIME": "COAST_TIME",
    "FOOD_PREF_DIST": "POOL_PREF_DIST", "FOOD_PULL": "POOL_PULL",
}


def _py_consts() -> dict[str, float]:
    src = Path(fp.__file__).read_text(encoding="utf-8")
    names = ("FLEE_RADIUS", "CATCH_RADIUS", "SCHOOL_RADIUS", "SEP_RADIUS",
             "FATIGUE_DECAY", "DRAG", "COAST_TIME", "FOOD_PREF_DIST",
             "FOOD_PULL", "EAT_RADIUS", "EAT_RATE", "SATIATION_GAIN",
             "DIGEST_RATE", "EXPLORE_BASE", "EXPLORE_SAT")
    out = {}
    for name in names:
        m = re.search(rf"^{name} = ([0-9.]+)", src, re.M)
        assert m, f"{name} missing from mag/flock_positive.py"
        out[name] = float(m.group(1))
    return out


def _gd_consts() -> dict[str, float]:
    """flock.gd's constants: GC-aliased names resolve through
    game_constants.gd (the single source, Q15), flock-local from flock.gd."""
    gd_src = FLOCK_GD.read_text(encoding="utf-8")
    gc_src = GC_GD.read_text(encoding="utf-8")
    names = ("FLEE_RADIUS", "CATCH_RADIUS", "SCHOOL_RADIUS", "SEP_RADIUS",
             "FATIGUE_DECAY", "DRAG", "COAST_TIME", "FOOD_PREF_DIST",
             "FOOD_PULL", "EAT_RADIUS", "EAT_RATE", "SATIATION_GAIN",
             "DIGEST_RATE", "EXPLORE_BASE", "EXPLORE_SAT")
    out = {}
    for name in names:
        if name in _GC_ALIASED:
            gc_name = _GC_ALIASED[name]
            m = re.search(rf"^const {gc_name} := ([0-9.]+)", gc_src, re.M)
            assert m, f"{gc_name} missing from game_constants.gd"
            # and flock.gd must actually carry the alias, not a forked
            # literal (?=\s|$): alias lines carry inline receipt comments
            assert re.search(rf"^const {name} := GC\.{gc_name}(?=\s|$)",
                             gd_src, re.M), \
                f"flock.gd lost its GC alias for {name}"
        else:
            m = re.search(rf"^const {name} := ([0-9.]+)", gd_src, re.M)
            assert m, f"{name} missing from flock.gd"
        out[name] = float(m.group(1))
    return out


def test_threat_mirror_constants_match_flock_gd():
    # The drift law: the Python instrument and the in-game module must carry
    # the same numbers or the A/B measures a different game than it plays.
    py, gd = _py_consts(), _gd_consts()
    assert py == gd
    assert py["FLEE_RADIUS"] == 20.0   # V6/Z14 tuning preserved
    assert py["FOOD_PULL"] == 22.0     # cites game.gd POOL_PULL — no secret force


def test_flee_push_is_v6_value_in_game_file():
    # R4/Q15: the inline 6.0 is now the named FLEE_PUSH alias of
    # game_constants.gd (still the V6/Z14 value — the pin is the same).
    src = FLOCK_GD.read_text(encoding="utf-8")
    assert re.search(r"^const FLEE_PUSH := GC\.FLEE_PUSH(?=\s|$)", src, re.M)
    assert re.search(r"f\.vel \+= -to_player\.normalized\(\) \* FLEE_PUSH \* dt", src)
    gc_src = GC_GD.read_text(encoding="utf-8")
    m = re.search(r"^const FLEE_PUSH := ([0-9.]+)", gc_src, re.M)
    assert m and float(m.group(1)) == 6.0  # V6: 2.5 -> 6.0 rides unchanged


def test_tire_law_fatigue_full_at_coast_time():
    # V6's verified law: continuous fleeing spends a fish in ~COAST_TIME 0.8s.
    f = fp.Fish(pos=(0.0, 0.0))
    player = (10.0, 0.0)  # inside FLEE_RADIUS, static cursor
    ticks = 0
    while f.fatigue < 1.0 and ticks < 600:
        fp.step_threat(f, [], player, fp.DT, ticks * fp.DT)
        ticks += 1
    assert f.fatigue == 1.0
    assert abs(ticks * fp.DT - fp.COAST_TIME) < 0.05


def test_threat_flag_gate_in_game_file():
    src = FLOCK_GD.read_text(encoding="utf-8")
    assert re.search(r"^var positive := false$", src, re.M)  # default = threat
    assert "if not positive and dist < CATCH_RADIUS" in src  # catch needs threat
    assert "if positive and food.size() > 0:" in src         # food branch is gated


# ------------------------------------------------ positive-mode mechanics ----

def test_food_attracts():
    f = fp.Fish(pos=(0.0, 0.0))
    food = [fp.FoodSource(pos=(100.0, 0.0), amount=3000.0)]
    fp.step_positive(f, [], food, 0.1, 0.0)
    assert f.pos[0] > 0.0  # moved TOWARD the food (positive gradient)


def test_feeding_raises_satiation_and_depletes_food():
    f = fp.Fish(pos=(0.0, 0.0))
    src = fp.FoodSource(pos=(5.0, 0.0), amount=3000.0)  # inside EAT_RADIUS
    fp.step_positive(f, [], [src], 1.0, 0.0)
    assert f.satiation > 0.0
    assert src.amount < 3000.0
    assert f.feeding


def test_full_fish_does_not_bite():
    f = fp.Fish(pos=(0.0, 0.0), satiation=1.0)
    src = fp.FoodSource(pos=(5.0, 0.0), amount=3000.0)
    fp.step_positive(f, [], [src], 1.0, 0.0)
    assert src.amount == 3000.0          # no bite at satiation 1.0
    assert f.satiation < 1.0             # digestion spent it instead


def test_digestion_spends_satiation_away_from_food():
    f = fp.Fish(pos=(0.0, 0.0), satiation=1.0)
    fp.step_positive(f, [], [fp.FoodSource(pos=(500.0, 0.0), amount=10.0)], 1.0, 0.0)
    assert f.satiation < 1.0


def test_hunger_scales_the_pull_exploit_vs_exploit():
    # hungry fish exploits the gradient harder than a fed one (same distance)
    hungry = fp.Fish(pos=(0.0, 0.0), satiation=0.0)
    fed = fp.Fish(pos=(0.0, 0.0), satiation=1.0)
    food = [fp.FoodSource(pos=(200.0, 0.0), amount=3000.0)]
    fp.step_positive(hungry, [], food, 0.2, 0.0)
    fp.step_positive(fed, [], food, 0.2, 0.0)
    assert hungry.vel[0] > fed.vel[0] > -1e-9 or hungry.vel[0] > fed.vel[0]


def test_satiated_fish_explores_more_at_the_patch():
    # at the patch (no pull): the wiggle amplitude grows with satiation —
    # EXPLORE_BASE + EXPLORE_SAT * sat — so a fed fish moves more than a
    # hungry one per tick
    hungry = fp.Fish(pos=(0.0, 0.0), satiation=0.0)
    fed = fp.Fish(pos=(0.0, 0.0), satiation=1.0)
    food = [fp.FoodSource(pos=(0.0, 5.0), amount=0.0)]  # inside EAT, empty
    fp.step_positive(hungry, [], food, 0.1, 0.3)
    fp.step_positive(fed, [], food, 0.1, 0.3)
    assert fp._len(fed.vel) > fp._len(hungry.vel)


def test_positive_episode_zero_panic_threat_episode_panics():
    pos = fab.run_episode("positive", seed=20260929, ticks=900, target="hollow")
    thr = fab.run_episode("threat", seed=20260929, ticks=900, target="hollow")
    assert pos.panic_entries == 0     # no flee state exists without threat
    assert thr.panic_entries > 0      # a chasing cursor manufactures panic


def test_determinism_same_seed_same_bytes():
    a = fab.run_episode("positive", seed=777, ticks=240, target="hollow")
    b = fab.run_episode("positive", seed=777, ticks=240, target="hollow")
    assert [(f.pos, f.vel, f.satiation) for f in a.fish] == \
           [(f.pos, f.vel, f.satiation) for f in b.fish]


# ------------------------------------------------------- A/B verdict law ----

def test_ab_verdict_positive_beats_threat():
    # The operator's law, measured: same board/seed/budget/target (hollow is
    # the near target so the test stays fast; crown is in the receipt).
    ab = fab.run_ab(seed=20260929, ticks=2400, target="hollow")
    tm, pm = ab["ab"]["threat"], ab["ab"]["positive"]
    assert pm["panic_entries"] < tm["panic_entries"]        # fewer errors
    assert pm["t80_seconds"] is not None                    # luring transits
    assert tm["t80_seconds"] is None or pm["t80_seconds"] <= tm["t80_seconds"]
    assert pm["cohesion_mean_px"] <= tm["cohesion_mean_px"]  # tighter school
    assert ab["verdict"]["operator_law_holds"] is True
    # the census: NO single-cursor threat policy transits the school
    assert ab["verdict"]["no_threat_policy_transits"] is True
    for p in fab.THREAT_POLICIES:
        assert ab["threat_policy_census"][p]["t80_seconds"] is None


def test_ab_census_chase_policy_kills_the_school():
    # The literal current behavior (chase-bites) is fishing, not herding:
    # the census row proves the cursor exterminates rather than moves.
    ab = fab.run_ab(seed=20260929, ticks=2400, target="hollow")
    chase = ab["threat_policy_census"]["chase"]
    assert chase["catches"] >= 10            # nearly the whole school caught
    assert chase["t80_seconds"] is None      # nobody left to move
