"""tests for game_portal — the Mycelial Republic login (old-school-WoW campfire, dark) + generative
raids where humans solve real problems as emergent play, narrated by AI agents.

RIB (frozen spec):
  login()   -> the campfire login: player enters the game by choosing a role + joining the wave;
               the entry folds as a verkle knot (server-authoritative). Role = emergent play.
  raid()    -> a generative raid: the challenge is a REAL problem from the shared wave, narrated by
               the DM, populated by agents, solved by humans. Never a fake monster.
  scene()   -> render the world as the dark campfire scene (ASCII + world root).
  roles()   -> the raid roles, each mapping to a real contribution.

Contract: reuses game_world (authoritative) + game_dm_voice (narration) + republic_wave (real
challenge). Deterministic + $0.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_portal  # noqa: E402


def test_roles_each_real_contribution():
    assert len(game_portal.ROLES) >= 5
    for r in game_portal.ROLES:
        assert "emergent_play" in r  # every role is a real contribution, not a fake class


def test_login_enters_game_via_wave(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    r = game_portal.login("hero", role="Warden")
    assert r["ok"] is True
    assert r["player"] == "hero"
    assert "emergent_play" in r
    assert "campfire" in r["scene"] or "CAMPFIRE" in r["scene"] or "fire" in r["scene"].lower()


def test_raid_generates_real_challenge():
    rd = game_portal.raid("the Cold Vein")
    assert rd["ok"] is True
    assert rd["raid"] == "the Cold Vein"
    assert "challenge" in rd  # a real problem, not a fake boss
    assert "narration" in rd
    assert "emergent play" in rd["note"]


def test_scene_renders_world():
    s = game_portal.scene()
    assert s["ok"] is True
    assert "ascii" in s
    assert "world_root" in s or "n_world_entities" in s
