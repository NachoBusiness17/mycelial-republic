"""D10 regression: beat-indexed ractive banking (arena_gwap v4-beat).

The door (eleven-doors D10-weld-ractive): "input + playback halves exist
and tested; banking half zero wiring - build capture+banking". The weld:
the run's ruled transcript events ARE the beat grid (strength =
roll_value, downbeat = k%4==0), and every dungeon claim's commit
qualifier gains beat=<k> zone=<z> hp=<n> on BOTH sides - derived from
the same post-roll record like commit= itself, so the agreement
arithmetic must be byte-stable (the falsifier this suite pins).
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import arena_gwap as ag  # noqa: E402
from tools.arena_beats import beat_grid  # noqa: E402
from mag.gwap_payload import decide_verdict  # noqa: E402


def _row(actor, scene, turn, roll, speech, verdict):
    return {"ts": f"2026-10-05T06:0{turn}:00Z", "scene": scene, "turn": turn,
            "actor": actor, "roll_committed": f"tip:{scene}:{turn}:{actor}",
            "roll_value": roll, "speech": speech, "verdict": verdict}


DUNGEON_ROWS = [
    _row("dm", "S0", 1, 8, "[CHECK omen]", "FAIL (d20=8 vs DC 11)"),
    _row("saelis", "S1", 1, 14, "[HIT the seal]", "HIT (d20=14 vs AC 12)"),
    _row("grok", "S1", 2, 19, "[Ledger Slam]", "Ledger Slam (d20=19) HIT"),
    _row("deepseek", "S1", 3, 5, "[MISS wildly]", "MISS (d20=5)"),
    _row("warden", "S1", 4, 20, "[AUDIT the wound]", "AUDIT SUCCESS (d20=20)"),
]


@pytest.fixture()
def dungeon_dir(tmp_path):
    d = tmp_path / "dnd0_test_20261005"
    d.mkdir()
    (d / "transcript.jsonl").write_text(
        "\n".join(json.dumps(r) for r in DUNGEON_ROWS) + "\n", encoding="utf-8")
    return d


def test_beat_grid_order_and_contract():
    grid, lookup = beat_grid(DUNGEON_ROWS)
    assert len(grid) == 5
    assert [m["t"] for m in grid] == [0.0, 1.0, 2.0, 3.0, 4.0]
    assert [m["downbeat"] for m in grid] == [True, False, False, False, True]
    # strength = roll_value (warden's 20 is row index 4), clipped to 9 by
    # the damage map contract
    assert grid[0]["strength"] == 8.0 and grid[4]["strength"] == 20.0
    # downbeat hp = 3 + int(clip(s,0,9)); offbeat hp = 1 + int(clip(s,0,9))//2
    assert grid[0]["hp"] == 3 + 8
    assert grid[1]["hp"] == 1 + 9 // 2  # roll 14 CLIPS to strength 9
    assert grid[4]["hp"] == 3 + 9  # nat-20 clips to strength 9
    assert lookup[("dm", "S0", "1")]["zone"] == "head"  # k=0 heavy
    assert lookup[("warden", "S1", "4")]["zone"] == "torso"  # k=4 heavy


def test_payloads_carry_beat_fields_on_both_sides(dungeon_dir):
    payloads = ag.actor_payloads(dungeon_dir)
    assert payloads, "dungeon payloads must bank"
    for _actor, _model, payload in payloads:
        for side in ("intent_struct", "report_struct"):
            for claim in payload[side]["claims"]:
                q = claim.get("qualifier", "")
                assert "commit=" in q
                assert "beat=" in q and "zone=" in q and "hp=" in q, q
    # intent and report qualifiers are byte-identical per claim (same record)
    for _actor, _model, payload in payloads:
        for i_c, r_c in zip(payload["intent_struct"]["claims"],
                            payload["report_struct"]["claims"]):
            assert i_c["qualifier"] == r_c["qualifier"]


def test_verdict_byte_stable_vs_v3(dungeon_dir, monkeypatch):
    """The falsifier: appending IDENTICAL qualifiers to both sides must not
    move the verdict. v4 = with beats; v3-shape = beat lookup emptied."""
    v4 = ag.actor_payloads(dungeon_dir)

    def no_beats(rows):
        return [], {}

    import tools.arena_beats
    monkeypatch.setattr(tools.arena_beats, "beat_grid", no_beats)
    v3 = ag.actor_payloads(dungeon_dir)
    monkeypatch.undo()
    assert len(v4) == len(v3)
    for (a4, m4, p4), (a3, _m3, p3) in zip(v4, v3):
        assert a4 == a3
        v_verd = decide_verdict(
            p4["intent_struct"], p4["report_struct"])
        v_old = decide_verdict(
            p3["intent_struct"], p3["report_struct"])
        assert v_verd == v_old, f"{a4}: {v_old} -> {v_verd} (beat fields moved it)"


def test_tavern_rows_carry_no_beats(tmp_path):
    d = tmp_path / "tavern_test_20261005"
    d.mkdir()
    rows = [
        {"ts": "t", "scene": "bar", "turn": 1, "actor": "greta",
         "model": "test/model-a", "speech": "draw!", "judge": "Greta rules: BRAWL",
         "verdict": "BRAWL r1"},
    ]
    (d / "transcript.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    payloads = ag.actor_payloads(d)
    assert payloads
    for claim in payloads[0][2]["intent_struct"]["claims"]:
        assert "beat=" not in claim.get("qualifier", "")  # no dice grid, honestly


def test_cli_beats_table(dungeon_dir, capsys):
    rc = ag.main(["--beats", str(dungeon_dir)])
    assert rc == 0
    out = capsys.readouterr().out
    assert "BEAT-DAMAGE TABLE" in out
    assert "TOTAL hp banked:" in out
    assert "zone=head" in out  # beat 0 is the downbeat
