"""tests for game_dm — I AM THE DM, our frontiers are the party. Deterministic $0 DM core.

RIB (frozen spec):
  party()        -> our frontier seats as the party (salon WITNESSES).
  dm_narrate()   -> I DM: grounded narration of the room (never fabricated).
  ask_player()   -> a frontier's move via seat_steer (honest per-seat ok, never fabricated).
  judge(seat, m) -> I rule deterministically (advances/wastes/no_move).
  turn()         -> I DM -> frontiers act -> I judge -> record to the world.
  play(room, n)  -> the table, n turns.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_dm as gd  # noqa: E402


def test_party_is_frontiers():
    p = gd.party()
    assert isinstance(p, list) and len(p) >= 3


def test_dm_narrates_grounded():
    n = gd.dm_narrate("tavern_lantern")
    assert n["ok"] is True and n["narration"]
    assert "legal_actions" in n


def test_judge_rules():
    assert gd.judge("chatgpt", "I search the room", "tavern_lantern")["verdict"] == "advances"
    assert gd.judge("supergrok", "", "tavern_lantern")["verdict"] == "no_move"


def test_turn_runs_and_records(monkeypatch):
    from mag import party_subchain

    prompts = []

    def fake_player(seat, prompt):
        prompts.append(prompt)
        return {"ok": True, "seat": seat, "surface": seat, "move": f"{seat} searches", "error": ""}

    class FakeWorld:
        @staticmethod
        def set_state(*_args, **_kwargs):
            return {"ok": True}

    monkeypatch.setattr(gd, "party", lambda: ["chatgpt", "supergrok", "v4-pro"])
    monkeypatch.setattr(gd, "ask_player", fake_player)
    monkeypatch.setattr(gd, "_world", lambda: FakeWorld)
    monkeypatch.setattr(
        party_subchain, "mount", lambda **_kwargs: {"ok": True, "transcript": "nothing yet"}
    )
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})
    t = gd.turn("tavern_lantern")
    assert t["ok"] is True
    assert len(t["frontiers"]) == len(gd.party())
    # honest: reachable <= total, never more
    assert t["n_reachable"] <= len(t["frontiers"])
    assert "nothing yet" in prompts[0]
    assert "chatgpt: chatgpt searches" in prompts[1]
    assert "supergrok: supergrok searches" in prompts[2]


def test_play_table(monkeypatch):
    from mag import party_subchain

    monkeypatch.setattr(gd, "party", lambda: ["chatgpt", "supergrok", "v4-pro"])
    monkeypatch.setattr(
        gd,
        "ask_player",
        lambda seat, prompt: {"ok": True, "seat": seat, "move": "search", "error": ""},
    )
    monkeypatch.setattr(
        gd,
        "_world",
        lambda: type("FakeWorld", (), {"set_state": staticmethod(lambda *_a, **_k: {"ok": True})}),
    )
    monkeypatch.setattr(
        party_subchain, "mount", lambda **_kwargs: {"ok": True, "transcript": "nothing yet"}
    )
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})
    r = gd.play("tavern_lantern", n=2)
    assert r["ok"] is True and r["n_turns"] == 2
    assert "reachable" in r
