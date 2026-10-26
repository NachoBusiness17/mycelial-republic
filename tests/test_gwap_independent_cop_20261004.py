"""Door 1 of the 24-wide dig (2026-10-04): the independent cop.

Defect being cured (receipt watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md,
"independent-cop door"): actor_payloads minted BOTH the robber's intent and
the cop's report from the same verdict bytes, so (a) the cop copied the
fighter's triple by construction (agreement was theater), (b) every honest
2+-claim session self-flagged as collusion (188 collusion-downgraded CHALLENGE
rows), and (c) a silent tavern cop scored absence as disagreement (2,78
DISPUTE rows; 3,802 silent vs 282 ruled rows in the 2026-10-04 census).

The fix: intent minted from the fighter's pre-roll SPEECH, report minted from
the law's POST-ROLL RECORD, both bound to the same commitment; a new
ledger-confirmation exemption in collusion_fingerprint (commitment/ruling
bound qualifiers in identical order = chronological confirmation, not copy);
a silent cop banks BLOCKED via the copsilent taboo instead of DISPUTE.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

import arena_gwap as ag  # noqa: E402
from mag.gwap_payload import collusion_fingerprint, decide_verdict  # noqa: E402


def _write_run(tmp_path: Path, name: str, rows: list[dict]) -> Path:
    d = tmp_path / name
    d.mkdir()
    lines = []
    for r in rows:
        import json
        lines.append(json.dumps(r))
    (d / "transcript.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return d


def _drow(turn: int, actor: str, speech: str, verdict: str,
          commit: str, scene: str = "S1", roll: int = 14) -> dict:
    return {"ts": f"2026-10-04T00:00:{turn:02d}Z", "scene": scene, "turn": turn,
            "actor": actor, "roll_committed": commit,
            "roll_value": roll, "speech": speech, "verdict": verdict,
            "dm_response": "(dry)"}


def test_honest_session_agrees_without_self_flagging(tmp_path):
    d = _write_run(tmp_path, "dnd0_test_honest", [
        _drow(1, "saelis", "[CHECK omen]", "SUCCESS (d20=15 vs DC 11)",
              "aabbccdd00112233:S1:1:saelis"),
        _drow(2, "saelis", "[CLAIMED page]", "CLAIMED ledger page",
              "aabbccdd00112233:S1:2:saelis"),
        _drow(3, "saelis", "[HIT wyrm]", "MISS",
              "aabbccdd00112233:S1:3:saelis"),
    ])
    out = ag.actor_payloads(d)
    assert len(out) == 1
    actor, model, payload = out[0]
    assert actor == "saelis" and model == "anthropic/claude-opus-5.5"
    # the declared attack ruled MISS still confirms: the law ruled the action
    assert payload["agreement_score"] == 1.0
    assert payload["verdict"] == "VERIFIED_AGREE"
    # THE 188-cure: identical order, commitment-bound, NOT collusion
    assert payload["collusion_fingerprint"]["suspected_collusion"] is False
    assert "ledger confirmation" in payload["collusion_fingerprint"]["evidence"]
    # D10 (2026-10-05): engine bumped v3-independent-cop -> v4-beat (beat-indexed
    # qualifiers); the independence contract itself is unchanged - the beat
    # weld suite pins the verdict stability across the bump
    assert "v4-beat" in payload["replay_tape_ref"]["engine_version"]


def test_independence_bites_on_family_mismatch(tmp_path):
    """Declared check ruled as a bare MISS (not the declared family) can no
    longer echo into agreement: the two parses disagree."""
    d = _write_run(tmp_path, "dnd0_test_bite", [
        _drow(1, "saelis", "[CHECK persuade]", "MISS",
              "aabbccdd00112233:S1:1:saelis"),
        _drow(2, "saelis", "[CHECK omen]", "RP (d20=9, no tag)",
              "aabbccdd00112233:S1:2:saelis"),
    ])
    _actor, _model, payload = ag.actor_payloads(d)[0]
    assert payload["agreement_score"] == 0.0
    assert payload["verdict"] == "DISPUTE"
    verbs_i = [c["verb"] for c in payload["intent_struct"]["claims"]]
    verbs_r = [c["verb"] for c in payload["report_struct"]["claims"]]
    assert verbs_i == ["checked", "checked"]
    assert verbs_r == ["attacked", "spoke"]


def test_unruled_claim_disagrees(tmp_path):
    """NOROLL = the model claimed an action the dice did not rule."""
    d = _write_run(tmp_path, "dnd0_test_void", [
        _drow(1, "saelis", "[HIT wyrm]", "NOROLL (no preimage staked)",
              "aabbccdd00112233:S1:1:saelis"),
    ])
    _a, _m, payload = ag.actor_payloads(d)[0]
    assert payload["report_struct"]["claims"][0]["verb"] == "voided"
    assert payload["verdict"] == "DISPUTE"


def test_free_form_identical_order_still_flags():
    """The exemption is narrow: identical order with FREE-FORM qualifiers
    (the actual copy shape) must keep firing."""
    def struct(author: str, q: str) -> dict:
        return {"author": author, "claims": [
            {"subject": "a", "verb": "spoke", "object": "x", "qualifier": q},
            {"subject": "a", "verb": "spoke", "object": "y", "qualifier": q},
        ]}
    fp = collusion_fingerprint(struct("f1", "we agreed on everything"),
                               struct("c1", "we agreed on everything"))
    assert fp["suspected_collusion"] is True


def test_commit_bound_identical_order_exempt():
    def struct(author: str, q: str) -> dict:
        return {"author": author, "claims": [
            {"subject": "a", "verb": "checked", "object": "S1", "qualifier": q},
            {"subject": "a", "verb": "attacked", "object": "S1", "qualifier": q},
        ]}
    fp = collusion_fingerprint(
        struct("f1", "commit=aabbccdd00112233:S1:1:saelis"),
        struct("c1", "commit=aabbccdd00112233:S1:1:saelis"))
    assert fp["suspected_collusion"] is False
    assert "ledger confirmation" in fp["evidence"]


def _trow(turn: int, actor: str, model: str, ruled: bool) -> dict:
    r = {"ts": f"2026-10-04T00:00:{turn:02d}Z", "dry": True,
         "tag": f"TAVERN_r1_{actor}", "model": model, "actor": actor,
         "scene": "THE HOLLOW CROWN TAVERN", "turn": turn}
    if ruled:
        r["judge"] = "the house"
        r["verdict"] = "RUN accepted (escalation clean)"
    return r


def test_silent_cop_banks_blocked_not_dispute(tmp_path):
    d = _write_run(tmp_path, "tavern_test_silent", [
        _trow(1, "Vess the Purser", "anthropic/claude-sonnet-5.5", ruled=False),
        _trow(2, "Vess the Purser", "anthropic/claude-sonnet-5.5", ruled=False),
    ])
    _a, model, payload = ag.actor_payloads(d)[0]
    assert model == "anthropic/claude-sonnet-5.5"  # row's own field, fail-closed
    assert payload["verdict"] == "BLOCKED"
    assert "copsilent" in payload["taboo_violations"]
    assert payload["report_struct"]["claims"][0]["verb"] == "blocked"


def test_ruled_tavern_banks_agreement(tmp_path):
    d = _write_run(tmp_path, "tavern_test_ruled", [
        _trow(1, "Brann the Rigger", "anthropic/claude-fable-5.1", ruled=True),
        _trow(2, "Brann the Rigger", "anthropic/claude-fable-5.1", ruled=True),
    ])
    _a, _m, payload = ag.actor_payloads(d)[0]
    assert payload["agreement_score"] == 1.0
    assert payload["verdict"] == "VERIFIED_AGREE"
    assert payload["collusion_fingerprint"]["suspected_collusion"] is False


def test_mixed_tavern_banks_ruled_only(tmp_path):
    d = _write_run(tmp_path, "tavern_test_mixed", [
        _trow(1, "Mother Quill", "anthropic/claude-sonnet-5.5", ruled=False),
        _trow(2, "Mother Quill", "anthropic/claude-sonnet-5.5", ruled=True),
    ])
    _a, _m, payload = ag.actor_payloads(d)[0]
    assert payload["verdict"] == "VERIFIED_AGREE"
    assert len(payload["intent_struct"]["claims"]) == 1  # the ruled row only


def test_decide_verdict_two_arg_regression():
    """Every v0 two-argument call keeps its exact v0 behavior."""
    assert decide_verdict(0.7) == "VERIFIED_AGREE"
    assert decide_verdict(0.5) == "CHALLENGE"
    assert decide_verdict(0.1) == "DISPUTE"
    assert decide_verdict(0.9, ("copsilent",)) == "BLOCKED"


def test_feed_scene_map_covers_quarantined_dirs(tmp_path, monkeypatch):
    """B7 sweep item 3 (2026-10-05): a banked dir quarantined under a staging
    root must still resolve its chain scenes in the feed map, or the
    whole-file feed refuses UNMAPPED_SCENE (observed live 2026-10-04T09:31:45Z,
    6 orphaned scenes from void_stamp_collision_tavern_20261004T083959Z;
    go_wave_20261004/gps_dedupe.md blocker 1)."""
    live = _write_run(tmp_path, "tavern_20261004T084000Z", [
        _trow(1, "Maud Ashgrove", "anthropic/claude-haiku-4.5", ruled=True),
    ])
    quar_root = tmp_path / "scenarios_lane9"
    quar = quar_root / "void_stamp_collision_tavern_20261004T083959Z"
    quar.mkdir(parents=True)
    import json as _json
    row = _trow(1, "Brother Oswin", "anthropic/claude-haiku-4.5", ruled=True)
    # banked-id law: the tag embeds the ORIGINAL run name the chain banked
    # under, which the quarantine rename loses from the dir name
    row["tag"] = "TAVERN_tavern_20261004T083959Z_r1_Brother Oswin"
    (quar / "transcript.jsonl").write_text(_json.dumps(row) + "\n",
                                           encoding="utf-8")
    # D10 split (2026-10-05): the feed machinery lives in tools/arena_feed
    # (re-exported on ag); PLAY_DIR is patched at its NEW home so the walk
    # and the map agree on the same test root
    import tools.arena_feed as afeed
    monkeypatch.setattr(afeed, "PLAY_DIR", tmp_path)
    assert ag._quarantined_run_dirs() == [quar]
    scene_map = ag.feed_scene_map()
    assert scene_map[f"arena-{live.name}-Maud Ashgrove"] == \
        "anthropic/claude-haiku-4.5"
    # keyed by the ORIGINAL run name, not the quarantined dir name
    assert scene_map["arena-tavern_20261004T083959Z-Brother Oswin"] == \
        "anthropic/claude-haiku-4.5"
    assert f"arena-{quar.name}-Brother Oswin" not in scene_map
