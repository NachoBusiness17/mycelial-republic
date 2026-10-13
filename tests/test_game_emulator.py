"""Stateless tests for game_emulator — the server-authoritative action resolver.
RIB: game_emulator.v1 — act() validates + resolves deterministically (hash-seeded) + folds a world
knot; room_attempt() the DND room conquest grounded in dungeon_dev; session() a playable run;
determinism (same input+world -> same roll). Stateless: tmp_path for game_world state, no framework."""
from __future__ import annotations


def test_act_resolves_and_is_deterministic(tmp_path, monkeypatch):
    import mag.game_emulator as m
    import mag.game_world as gw
    monkeypatch.setattr(gw, "WORLD_DIR", tmp_path)
    monkeypatch.setattr(gw, "WORLD", tmp_path / "world_state.json")
    r1 = m.act("scout", actor="player", difficulty=12)
    assert r1["ok"] and r1["outcome"] in ("success", "failure", "critical-success", "critical-failure")
    assert r1["folded"] is True  # the outcome committed as a verkle knot
    # determinism: same actor+action+world root -> same roll
    assert m._roll("player", "scout") == m._roll("player", "scout")


def test_act_empty_rejected():
    import mag.game_emulator as m
    assert m.act("", actor="player")["ok"] is False


def test_room_attempt_grounded_in_dungeon(tmp_path, monkeypatch):
    import mag.game_emulator as m
    import mag.game_world as gw
    monkeypatch.setattr(gw, "WORLD_DIR", tmp_path)
    monkeypatch.setattr(gw, "WORLD", tmp_path / "world_state.json")
    r = m.room_attempt(actor="adventurer")
    assert r["ok"] and r["room"]  # grounded in dungeon_dev rooms
    assert "emulator-core" in r["room"] or r["region"]
    assert r["conquered"] in (True, False)


def test_session_returns_turns():
    import mag.game_emulator as m
    s = m.session()
    assert s["ok"] and len(s["turns"]) == 3
    for t in s["turns"]:
        assert t["outcome"] in ("success", "failure", "critical-success", "critical-failure")


def test_roll_boundary():
    import mag.game_emulator as m
    # the roll is 1..20 (d20), byte-stable
    for actor in ("a", "b", "c"):
        for action in ("x", "y"):
            r = m._roll(actor, action)
            assert 1 <= r <= 20
