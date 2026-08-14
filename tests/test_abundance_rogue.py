"""tests for abundance_rogue — the roguelike with permanent generative history mapped to global
issues, where playing unties real topological problems to introduce abundance for all.

RIB (frozen spec):
  enter()   -> start a perm-death run; the run's start folds as a permanent knot (history persists).
  dungeon() -> the floors = GLOBAL ISSUES = real topological problems (tangles), grounded in the
               real chain (knot_untangle.scan_chain).
  play()    -> untie a floor's tangle (real invariant -> shared wave = abundance) OR perm-die
               (attempt folded as permanent history). Idempotent per floor.
  history() -> the permanent generative history (content-addressed knots, never reset).
  abundance() -> what untangling earned for all (measured from republic_wave).

Contract: reuses knot_untangle + game_world + republic_wave; perm-death is real, history permanent.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import abundance_rogue  # noqa: E402


def test_floors_map_global_issues():
    assert len(abundance_rogue.FLOORS) >= 5
    for f in abundance_rogue.FLOORS:
        assert "issue" in f and "tangle" in f  # every floor is a real problem to untie


def test_enter_starts_run(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    r = abundance_rogue.enter("hero")
    assert r["ok"] is True
    assert r["n_floors"] >= 5
    assert "perm" in r["goal"].lower() or "history" in r["goal"].lower()


def test_play_unties_and_perm_dies(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    # untie floor 1 -> success, idempotent on re-play
    ok = abundance_rogue.play("hero", floor=1, untie=True)
    assert ok["untied"] is True
    again = abundance_rogue.play("hero", floor=1, untie=True)
    assert again["already"] is True  # history remembers
    # a failed attempt (untie=False) = perm-death, history persists
    died = abundance_rogue.play("other", floor=2, untie=False)
    assert died["perm_death"] is True


def test_history_permanent(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    abundance_rogue.enter("a")
    abundance_rogue.play("a", floor=1, untie=True)
    h = abundance_rogue.history()
    assert h["ok"] is True
    assert h["n_history_knots"] >= 1  # the run is on the chain (permanent)
    assert "world_root" in h


def test_abundance_measured():
    a = abundance_rogue.abundance()
    assert a["ok"] is True
    assert "abundance" in a  # what untangling earned (measured, honest)
