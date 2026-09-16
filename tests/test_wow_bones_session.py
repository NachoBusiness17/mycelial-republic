"""tests for mag/wow_bones_session.py -- the referee, bound by the directive's own falsifiers.

Determinism falsifier: same seed + same moves, played twice, byte-identical receipt sha256.
Divergence falsifier: flip one committed RNG draw -> RNG_DIVERGE at the exact draw index.
Both must pass or the directive failed. Skips cleanly when the fixture is absent.
"""
from __future__ import annotations

import json

import pytest

from mag.wow_bones import load_fixture
from mag.wow_bones_session import (AUTHED, DRAW_TARGET, LOGGEDIN, TURN_LIMIT,
                                   BonesSession, canonical, session_id_for)

pytestmark = pytest.mark.skipif(load_fixture() is None, reason="bones fixture absent")


@pytest.fixture(scope="module")
def fx():
    return load_fixture()


def first_verb(fx, status):
    rows = sorted(fx["tables"]["client_opcodes"], key=lambda r: r["name"])
    for r in rows:
        if r["status"] == status:
            return r["name"]
    return None


@pytest.fixture(scope="module")
def auth_verb(fx):
    return first_verb(fx, AUTHED)


@pytest.fixture(scope="module")
def game_verb(fx):
    return first_verb(fx, LOGGEDIN)


def winning_line(fx, seed, auth_verb, game_verb, *, world_boss=False):
    ses = BonesSession(fx, seed, world_boss=world_boss)
    ses.turn(auth_verb)      # promote to LOGGEDIN
    ses.turn(game_verb)      # engage: TO_BE_DECIDED -> IN_PROGRESS (a load, no draw)
    for _ in range(DRAW_TARGET):
        ses.turn(game_verb)  # one draw each; DONE attempted on the last
    return ses


def test_start_state(fx, auth_verb):
    ses = BonesSession(fx, auth_verb)
    assert ses.session_status == AUTHED
    assert ses.encounter_name() == "TO_BE_DECIDED"
    assert ses.verdict() == "OPEN"
    assert ses.stream.index == 0
    assert ses.session_id == session_id_for(ses.seed, False)


def test_unknown_opcode_is_typed_and_free(fx, auth_verb, game_verb):
    ses = winning_line(fx, "t-unknown", auth_verb, game_verb)
    before = (ses.session_status, ses.stream.index, ses.turn_count)
    entry = ses.turn("CMSG_NOT_A_REAL_VERB_ZZ")
    assert entry["ok"] is False and entry["reason"] == "UNKNOWN_OPCODE"
    assert (ses.session_status, ses.stream.index, ses.turn_count - 1) == before


def test_wrong_status_is_typed(fx, auth_verb, game_verb):
    ses = BonesSession(fx, "t-mismatch")
    entry = ses.turn(game_verb)  # LOGGEDIN verb at AUTHED
    assert entry["ok"] is False and entry["reason"] == "STATUS_MISMATCH"
    assert ses.session_status == AUTHED


def test_never_status_is_typed(fx, auth_verb, game_verb):
    never = first_verb(fx, "STATUS_NEVER")
    if never is None:
        pytest.skip("no STATUS_NEVER verb in fixture")
    ses = winning_line(fx, "t-never", auth_verb, game_verb)
    entry = ses.turn(never)
    assert entry["ok"] is False and entry["reason"] == "STATUS_NEVER"


def test_promotion_then_engage_then_done(fx, auth_verb, game_verb):
    ses = BonesSession(fx, "t-arc")
    assert ses.turn(auth_verb)["ok"] is True
    assert ses.session_status == LOGGEDIN
    assert ses.stream.index == 0                    # promotion draws nothing
    assert ses.turn(game_verb)["ok"] is True
    assert ses.encounter_name() == "IN_PROGRESS"    # the load
    assert ses.stream.index == 0                    # the load draws nothing
    for i in range(1, DRAW_TARGET + 1):
        assert ses.turn(game_verb)["ok"] is True
        assert ses.stream.index == i
    assert ses.encounter_name() == "DONE"
    assert ses.verdict() == "COMPLETE"


def test_determinism_falsifier_byte_identical_receipts(fx, auth_verb, game_verb):
    a = winning_line(fx, "seed-determinism", auth_verb, game_verb)
    b = winning_line(fx, "seed-determinism", auth_verb, game_verb)
    ra, rb = a.receipt(), b.receipt()
    assert canonical(ra) == canonical(rb)
    assert ra["sha256"] == rb["sha256"]


def test_replay_across_cli_splice_is_byte_identical(fx, auth_verb, game_verb):
    whole = winning_line(fx, "seed-splice", auth_verb, game_verb)
    part = BonesSession(fx, "seed-splice")
    part.turn(auth_verb)
    part.turn(game_verb)
    part.save()
    resumed = BonesSession.load(part.session_id)
    for _ in range(DRAW_TARGET):
        resumed.turn(game_verb)
    assert canonical(resumed.receipt()) == canonical(whole.receipt())


def test_divergence_falsifier_names_exact_index(fx, auth_verb, game_verb):
    from mag.wow_bones import Stream
    ses = winning_line(fx, "seed-diverge", auth_verb, game_verb)
    log = [dict(d) for d in ses.stream.log]
    assert log, "the winning line must have committed draws"
    flipped = log[DRAW_TARGET - 1]                # tamper with the last committed draw
    flipped["value"] = (flipped["value"] + 1) % 100
    verdict = Stream(ses.seed).replay(flipped_log := log)
    assert verdict["ok"] is False
    assert verdict["reason"] == "RNG_DIVERGE"
    assert verdict["index"] == flipped["index"]


def test_world_boss_guard_never_completes(fx, auth_verb, game_verb):
    ses = BonesSession(fx, "t-guard", world_boss=True)
    for _ in range(TURN_LIMIT):
        ses.turn(game_verb if ses.session_status == LOGGEDIN else auth_verb)
    assert ses.encounter_name() == "IN_PROGRESS"   # DONE refused every time
    assert ses.verdict() == "EXHAUSTED"


def test_receipt_schema_and_self_hash(fx, auth_verb, game_verb):
    ses = winning_line(fx, "t-schema", auth_verb, game_verb)
    r = ses.receipt()
    for key in ("session_id", "seed", "draw_index", "moves", "verdict", "sha256"):
        assert key in r
    body = {k: v for k, v in r.items() if k != "sha256"}
    import hashlib
    assert r["sha256"] == hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()
    for m in r["moves"]:
        assert set(m) in ({"n", "verb", "ok", "reason"}, {"n", "verb", "ok", "reason", "handler"})


def test_cli_via_wow_bones_passthrough(fx, auth_verb, game_verb, capsys):
    from mag import wow_bones
    assert wow_bones.main(["session", "start", "--seed", "t-cli"]) == 0
    sid = json.loads(capsys.readouterr().out)["session_id"]
    assert wow_bones.main(["session", "turn", "--session", sid, "--verb", auth_verb]) == 0
    capsys.readouterr()
    assert wow_bones.main(["session", "receipt", "--session", sid]) == 0
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["session_id"] == sid
    assert receipt["verdict"] == "OPEN"
