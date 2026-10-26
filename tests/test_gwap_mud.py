"""tests for mag/gwap_mud.py -- the MUD -> GWAP connector falsifiers (v1).

Event law: the action map is closed ({move, attack, kill} -> {moved,
attacked, killed}), positions quantize to integer tiles, unknown actions and
missing targets fail closed. Replay law: one presence line is only a
snapshot; claims come from deltas against the same player's previous
snapshot (tile movement, hp loss, death, victory transitions, in that fixed
order), first sightings yield nothing, prev must match the player id, and
the /mud/state spectator "age" key is tolerated. Connector law: the structs
feed build_payload() directly and land in a verifying ledger row; tampering
a signed row fails offline verification.
"""
from __future__ import annotations

import json

import pytest

import mag.gwap_payload as gw
import mag.gwap_mud as gm
from mag.gwap_payload import GwapError, SessionLedger, VERIFIED_AGREE

UTC = "2026-09-29T12:00:00Z"
TAPE = {"sha256": "0" * 64, "engine_version": "mud-presence-v0"}


def presence(pid="bearer-7", x=0.5, y=0.5, hp=100.0, state="play", name="Bearer"):
    return {"id": pid, "name": name, "x": x, "y": y,
            "hp": hp, "max_hp": 100.0, "state": state}


def event(action, x=12.4, y=8.6, target=None, pid="bearer-7"):
    e = {"player": {"id": pid, "x": x, "y": y}, "action": action}
    if target is not None:
        e["target"] = target
    return e


@pytest.fixture()
def store(tmp_path, monkeypatch):
    monkeypatch.setattr(gw, "STORE", tmp_path)
    return tmp_path


# -- event adapter ----------------------------------------------------------------------


def test_event_move_maps_to_tile_claim():
    assert gm.claim_from_event(event("move")) == {
        "subject": "bearer-7", "verb": "moved",
        "object": "tile 12 9", "qualifier": "",
    }
    # quantization: 12.4 -> 12, 8.6 -> 9
    assert gm.claim_from_event(event("move", x=13.6, y=-2.4))["object"] == "tile 14 -2"


def test_event_attack_and_kill_map_to_target():
    assert gm.claim_from_event(event("attack", target="mob-brute-3")) == {
        "subject": "bearer-7", "verb": "attacked",
        "object": "mob-brute-3", "qualifier": "",
    }
    assert gm.claim_from_event(event("kill", target="mob-brute-3"))["verb"] == "killed"


def test_event_unknown_action_and_bad_shapes_fail_closed():
    with pytest.raises(GwapError) as exc:
        gm.claim_from_event(event("cast-magic"))
    assert exc.value.reason == "MUD_EVENT"
    for bad in ("not a dict", {"action": "move"}, event("attack"),
                event("attack", target="  ")):
        with pytest.raises(GwapError):
            gm.claim_from_event(bad)


def test_struct_from_events_shape_and_determinism():
    s1 = gm.struct_from_events("r-mud", [event("move"), event("attack", target="m1")])
    s2 = gm.struct_from_events("r-mud", [event("move"), event("attack", target="m1")])
    assert s1 == s2
    assert set(s1) == {"author", "claims"}
    assert s1["author"] == "r-mud"
    assert s1["claims"][1] == {"subject": "bearer-7", "verb": "attacked",
                               "object": "m1", "qualifier": ""}
    with pytest.raises(GwapError):
        gm.struct_from_events("", [])


# -- replay line parser -----------------------------------------------------------------


def test_replay_first_sighting_yields_no_claim():
    snap, claims = gm.from_replay_line(json.dumps(presence()))
    assert claims == []
    assert snap["id"] == "bearer-7" and snap["x"] == 0.5


def test_replay_movement_delta_and_subtile_jitter():
    prev, _ = gm.from_replay_line(presence())
    _, claims = gm.from_replay_line(presence(x=12.4, y=8.6), prev)
    assert claims == [{"subject": "bearer-7", "verb": "moved",
                       "object": "tile 12 9", "qualifier": ""}]
    # jitter inside the same tile is invisible (tile quantization)
    prev2 = dict(prev, x=12.2, y=8.4)
    _, claims = gm.from_replay_line(presence(x=12.3, y=8.5), prev2)
    assert claims == []


def test_replay_hp_drop_and_death_victory_transitions():
    prev = dict(presence(hp=100.0), state="play")
    snap, claims = gm.from_replay_line(presence(hp=84.3), prev)
    assert claims == [{"subject": "bearer-7", "verb": "lost", "object": "hp",
                       "qualifier": "down 15.7"}]
    # hp gain is not a claim (heals carry no agreement signal here)
    _, claims = gm.from_replay_line(presence(hp=95.0), dict(prev, hp=90.0))
    assert claims == []

    died, claims = gm.from_replay_line(presence(hp=0.0, state="dead"), snap)
    assert claims[-1] == {"subject": "bearer-7", "verb": "died",
                          "object": "tile 0 0", "qualifier": ""}
    # a repeated dead line does not re-claim the death
    _, claims = gm.from_replay_line(presence(hp=0.0, state="dead"), died)
    assert claims == []

    _, claims = gm.from_replay_line(
        presence(state="victory"), presence(state="play"))
    assert claims == [{"subject": "bearer-7", "verb": "won",
                       "object": "tile 0 0", "qualifier": ""}]


def test_replay_fixed_claim_order_movement_then_hp():
    prev = presence(x=0.0, y=0.0, hp=100.0)
    _, claims = gm.from_replay_line(presence(x=1.0, y=1.0, hp=80.0), prev)
    assert [c["verb"] for c in claims] == ["moved", "lost"]


def test_replay_prev_must_be_same_player_and_lines_validate():
    with pytest.raises(GwapError) as exc:
        gm.from_replay_line(presence(), presence(pid="other-1"))
    assert exc.value.reason == "MUD_REPLAY"
    for bad_line in ("{not json", "[]", presence(pid=" "),
                     dict(presence(), hp="full"), {"id": "bearer-7"}):
        with pytest.raises(GwapError):
            gm.from_replay_line(bad_line)


def test_replay_tolerates_spectator_age_key():
    line = dict(presence(x=1.0), age=0.42)   # /mud/state shape
    snap, _ = gm.from_replay_line(line, presence())
    assert set(snap) == set(gm.PRESENCE_KEYS)   # age dropped


def test_struct_from_replay_threads_prev_per_player():
    lines = [
        presence(pid="a", x=0.0, y=0.0),
        presence(pid="b", x=5.0, y=5.0),
        presence(pid="a", x=1.0, y=0.0),
        presence(pid="b", x=6.0, y=5.0),
        presence(pid="a", x=2.0, y=0.0),
    ]
    s = gm.struct_from_replay("c-mud", lines)
    assert s["author"] == "c-mud"
    assert s["claims"] == [
        {"subject": "a", "verb": "moved", "object": "tile 1 0", "qualifier": ""},
        {"subject": "b", "verb": "moved", "object": "tile 6 5", "qualifier": ""},
        {"subject": "a", "verb": "moved", "object": "tile 2 0", "qualifier": ""},
    ]


# -- end to end: the connector feeds the engine -------------------------------------------


def test_end_to_end_mud_round_lands_a_verifying_ledger_row(store):
    robber, cop = "r-mud", "c-mud"
    events = [
        event("move"),
        event("attack", target="mob-brute-3"),
        event("move", x=13.2),
    ]
    replay = [
        presence(x=0.5, y=0.5),
        presence(x=12.4, y=8.6),
        presence(x=13.2, y=8.6),
    ]
    intent_struct = gm.struct_from_events(robber, events)
    report_struct = gm.struct_from_replay(cop, replay)

    p = gw.build_payload(
        scene_id="mud-arena-042",
        intent_struct=intent_struct,
        report_struct=report_struct,
        participants=[{"anon_id": robber, "role": "robber"},
                      {"anon_id": cop, "role": "cop"}],
        consent=True,
        created_utc=UTC,
        replay_tape_ref=TAPE,
    )
    # the relay corroborates both moves but cannot see the attack (presence
    # carries no attacker attribution): 2 of a 3-triple union = 0.6667
    assert p["agreement_score"] == 0.6667
    assert p["verdict"] == VERIFIED_AGREE
    assert p["collusion_fingerprint"]["suspected_collusion"] is False

    ledger = SessionLedger("mud-e2e-20260929")
    row = ledger.append(p, ts_utc=UTC)
    assert row["seq"] == 1
    assert ledger.verify_chain() == (True, None)


@pytest.mark.skipif(
    not gw.HAS_CRYPTO, reason="cryptography package not installed in this venv"
)
def test_end_to_end_signed_row_fails_offline_after_tamper(store):
    robber, cop = "r-mud", "c-mud"
    intent_struct = gm.struct_from_events(robber, [event("move")])
    report_struct = gm.struct_from_replay(
        cop, [presence(x=0.5), presence(x=12.4, y=8.6)])
    p = gw.build_payload(
        scene_id="mud-arena-043",
        intent_struct=intent_struct,
        report_struct=report_struct,
        participants=[{"anon_id": robber, "role": "robber"},
                      {"anon_id": cop, "role": "cop"}],
        consent=True,
        created_utc=UTC,
        replay_tape_ref=TAPE,
    )
    assert p["verdict"] == VERIFIED_AGREE          # the one shared move claim

    priv_hex, _pub = gw.author_keypair("mud-e2e-robber-key")
    signed = gw.sign_payload(p, robber, priv_hex)
    ledger = SessionLedger("mud-e2e-signed-20260929")
    ledger.append(signed, ts_utc=UTC)
    assert ledger.verify_chain() == (True, None)

    # anyone holding the row verifies offline; editing the row's payload
    # breaks the chain hash AND the signature
    stored = json.loads(ledger.path.read_text(encoding="utf-8").splitlines()[0])
    assert gw.verify_signature(stored["payload"]) is True
    stored["payload"]["scene_id"] = "forged"
    assert gw.verify_signature(stored["payload"]) is False
