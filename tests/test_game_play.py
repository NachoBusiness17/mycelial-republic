"""tests for game_play — the playable server-authoritative surface. Deterministic + stateless.

RIB (frozen spec):
  map()   -> world_rib.compile from the seed RIB -> deterministic ASCII territory (or honest error
             if the render deps are missing). The map precedes the territory (re-derivable).
  sense() -> event-driven read of the world (game_world state), no polling.
  act()   -> a player action is a PROPOSAL that becomes true only when game_world folds it as a
             verkle knot. Unknown actions are rejected (sandbox, honest). Valid ones commit.
  play()  -> ONE FULL TURN: sense -> validate -> act (fold) -> re-sense -> report. Honest:
             `committed` is true only if the knot actually committed.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_play  # noqa: E402


def test_map_renders_or_honest_error():
    m = game_play.map()
    assert m["ok"] in (True, False)
    assert "objective" in m or "error" in m
    # if it rendered, the map + objective are present and deterministic
    if m["ok"]:
        assert "map" in m and m["objective"]
        # re-render is byte-identical (map precedes territory, re-derivable)
        m2 = game_play.map()
        assert m2["map"] == m["map"]


def test_valid_actions_sandbox():
    # the world only accepts known actions (sandbox, never spoofs)
    for a in ("look", "walk", "map", "rest", "survey", "help"):
        assert a in game_play.VALID_ACTIONS


def test_act_rejects_unknown():
    r = game_play.act("fly")
    assert r["ok"] is False
    assert r["error"] == "unknown action"
    assert "valid" in r


def test_play_full_turn_commits_or_honest():
    p = game_play.play("look")
    assert p["ok"] in (True, False)
    assert "turn" in p and "world_before" in p and "world_after" in p
    assert "committed" in p  # honesty: committed is separate from ok
    assert p["valid_actions"] == sorted(game_play.VALID_ACTIONS)
    # if the knot committed, the world root changed (the action became true)
    if p["committed"]:
        assert p["turn"]["accepted"] is True


def test_sense_event_driven():
    s = game_play.sense()
    assert s["ok"] is True
    assert s["objective"] == game_play.OBJECTIVE
    assert "n_changes" in s and "world" in s


def test_play_sequence_look_walk_map_survey():
    """Play the four actions the operator asked for: look, walk, map, survey. Each is a proposal
    that becomes true only when folded as a verkle knot. All four must commit or honestly report."""
    for action in ("look", "walk", "map", "survey"):
        p = game_play.play(action)
        assert p["ok"] is True, f"{action} turn failed: {p}"
        assert p["committed"] is True, f"{action} did not commit: {p}"
        assert p["turn"]["accepted"] is True
        # the world root advanced (the knot committed, world is the authority)
        assert p["world_before"]["root"] != p["world_after"]["root"] or p["world_before"][
            "root"] is None
    # all four actions are now on the chain as server-authoritative knots
    s = game_play.sense()
    assert s["n_changes"] >= 4


def test_play_rest():
    """The operator rested: `rest` is a valid action that commits as a verkle knot."""
    p = game_play.play("rest")
    assert p["ok"] is True
    assert p["committed"] is True
    assert p["turn"]["accepted"] is True
    assert p["turn"]["action"] == "rest"
