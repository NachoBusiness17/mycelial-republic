"""Every party surface exposes earlier same-run moves to later seats."""
from __future__ import annotations


def test_roshomon_quest_is_sequential_and_chained(monkeypatch):
    from mag import party_subchain, quest_roshomon

    prompts = []
    chained = []

    class DM:
        @staticmethod
        def party():
            return ["chatgpt", "supergrok", "v4-pro"]

        @staticmethod
        def dm_narrate(_room):
            return {"narration": "A test chamber.", "legal_actions": ["forge"]}

        @staticmethod
        def ask_player(seat, prompt):
            prompts.append(prompt)
            return {"ok": True, "seat": seat, "move": f"{seat} mechanism"}

    monkeypatch.setattr(quest_roshomon, "_dm", lambda: DM)
    monkeypatch.setattr(party_subchain, "append", lambda **row: chained.append(row) or {"ok": True})
    result = quest_roshomon.play("connect the seats")
    assert result["n_reachable"] == 3
    assert "nothing yet" in prompts[0]
    assert "chatgpt: chatgpt mechanism" in prompts[1]
    assert "supergrok: supergrok mechanism" in prompts[2]
    assert [row["kind"] for row in chained] == ["quest_roshomon"] * 3


def test_class_selection_reads_prior_selections(monkeypatch):
    from mag import party_subchain, quest_party

    prompts = []

    class DM:
        @staticmethod
        def party():
            return ["chatgpt", "supergrok"]

        @staticmethod
        def ask_player(seat, prompt):
            prompts.append(prompt)
            return {"ok": True, "seat": seat,
                    "move": f"CLASS: bard\nABILITIES: {seat} relay"}

    monkeypatch.setattr(quest_party, "_dm", lambda: DM)
    monkeypatch.setattr(party_subchain, "append", lambda **_row: {"ok": True})
    result = quest_party.self_select("choose a communication invariant")
    assert len(result["picks"]) == 2
    assert "nothing yet" in prompts[0]
    assert "chatgpt: CLASS: bard" in prompts[1]


def test_frontier_game_rebuilds_prompt_after_each_move(monkeypatch):
    from mag import frontier_game, party_subchain

    prompts = []

    class DM:
        @staticmethod
        def party():
            return ["chatgpt", "supergrok"]

        @staticmethod
        def ask_player(seat, prompt):
            prompts.append(prompt)
            return {"ok": True, "seat": seat, "move": f"{seat} observes the mirror"}

    class Environment:
        REGIONS = {"the_mirror_sea": {
            "invariant": "observer mirror", "desc": "The sea reflects the observer."
        }}

        @staticmethod
        def explore(region):
            return {"region": region, "desc": "The sea reflects the observer."}

    class World:
        n = 0

        @classmethod
        def set_state(cls, *_args, **_kwargs):
            cls.n += 1
            return {"ok": True}

        @classmethod
        def world_status(cls):
            return {"n_entities": cls.n, "root": "test-root"}

    class Renderer:
        @staticmethod
        def render():
            return {"ascii": "mirror"}

    monkeypatch.setattr(frontier_game, "_env", lambda: (DM, Environment, World, Renderer))
    monkeypatch.setattr(party_subchain, "append", lambda **_row: {"ok": True})
    result = frontier_game.play(rounds=1)
    assert result["ok"] is True
    assert "nothing yet" in prompts[0]
    assert "chatgpt: chatgpt observes the mirror" in prompts[1]
