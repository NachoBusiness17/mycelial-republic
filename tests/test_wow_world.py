"""tests for mag/wow_world.py -- the bones-world skeleton, bound by M0's falsifiers.

Determinism falsifier: same seed + same route, played twice, byte-identical receipt (and sha256).
Refusal falsifier: a locked/missing exit is a typed gate refusal with handler_ran False and the
room unchanged -- never silent. The gate is the bones Dispatch class over a world table; the
DONE guard is the Instance kernel's own. Both falsifiers must pass or M0 failed.
Skips cleanly when the fixture is absent.
"""
from __future__ import annotations

import hashlib

import pytest

from mag.wow_bones import Dispatch, load_fixture
from mag.wow_bones_session import DRAW_TARGET, TURN_LIMIT, canonical
from mag.wow_world import (DEFAULT_WORLD, RECEIPT_SCHEMA, WorldSession, room_fixture,
                           world_digest, world_session_id)

pytestmark = pytest.mark.skipif(load_fixture() is None, reason="bones fixture absent")


@pytest.fixture(scope="module")
def fx():
    return load_fixture()


def winning_line(fx, seed, *, world_boss=False):
    """atrium -> (look: promote) -> north -> east -> vault (look: load) -> 3 looks -> DONE."""
    ses = WorldSession(fx, seed, world_boss=world_boss)
    ses.turn("look")               # promotion; draws nothing
    ses.turn("go", "north")        # atrium -> torch_hall; draws nothing
    ses.turn("go", "east")         # torch_hall -> vault; draws nothing
    ses.turn("look")               # the load: TO_BE_DECIDED -> IN_PROGRESS; draws nothing
    for _ in range(DRAW_TARGET):
        ses.turn("look")           # one draw each; guarded DONE attempted on the last
    return ses


def test_wow_world_gate_is_the_bones_gate(fx):
    """The room table rides the SAME Dispatch class -- no duplicated gating logic."""
    gate = WorldSession(fx, "t-gate").room_gate
    assert isinstance(gate, Dispatch)
    names = list(gate.rows)
    assert len(names) == len(set(names)), "room rows must be name-unique (no cross-room collision)"
    row = gate.rows["GO_NORTH@ROOM:atrium"]
    assert row["status"] == "ROOM:atrium"           # a room is a status
    lock = gate.rows["GO_WEST@ROOM:torch_hall"]
    assert lock["status"] == "STATUS_NEVER"         # a locked door is a legality row
    assert all(r["status"] in gate.enums["session_status"] or r["status"] == "STATUS_NEVER"
               for r in gate.rows.values())


def test_wow_world_missing_exit_is_typed_and_never_silent(fx):
    ses = WorldSession(fx, "t-missing")
    before = (ses.room, ses.session_status, ses.stream.index)
    entry = ses.turn("go", "west")                  # atrium has no west door anywhere
    assert entry["ok"] is False
    assert entry["reason"] == "UNKNOWN_OPCODE"
    assert entry["handler_ran"] is False
    assert (ses.room, ses.session_status, ses.stream.index) == before


def test_wow_world_locked_exit_is_status_never(fx):
    ses = WorldSession(fx, "t-locked")
    ses.turn("go", "north")                         # atrium -> torch_hall
    entry = ses.turn("go", "west")                  # the locked ash_gallery door
    assert entry["ok"] is False
    assert entry["reason"] == "STATUS_NEVER"
    assert entry["handler_ran"] is False
    assert ses.room == "torch_hall"


def test_wow_world_unknown_verb_is_typed(fx):
    ses = WorldSession(fx, "t-verb")
    entry = ses.turn("dance")
    assert entry["ok"] is False and entry["reason"] == "UNKNOWN_OPCODE"
    assert entry["handler_ran"] is False


def test_wow_world_traversal_costs_no_draws(fx):
    ses = WorldSession(fx, "t-walk")
    ses.turn("look")                                # promotion only
    ses.turn("go", "north")
    ses.turn("go", "east")
    assert ses.room == "vault"
    assert ses.route == ["atrium", "torch_hall", "vault"]
    assert ses.stream.index == 0 and ses.draws == 0  # movement never draws
    assert ses.encounter_name() == "TO_BE_DECIDED"   # movement never loads


def test_wow_world_arc_promote_load_done(fx):
    ses = winning_line(fx, "t-arc")
    assert ses.session_status == "STATUS_LOGGEDIN"
    assert ses.encounter_name() == "DONE"
    assert ses.draws == DRAW_TARGET
    assert ses.verdict() == "COMPLETE"
    assert len(ses.moves) == 3 + 1 + DRAW_TARGET


def test_wow_world_world_boss_guard_never_completes(fx):
    ses = winning_line(fx, "t-guard", world_boss=True)
    assert ses.encounter_name() == "IN_PROGRESS"     # DONE refused by the inherited guard
    for _ in range(TURN_LIMIT):
        if ses.verdict() != "OPEN":
            break
        ses.turn("look")
    assert ses.verdict() == "EXHAUSTED"


def test_wow_world_determinism_byte_identical_receipts(fx):
    a = winning_line(fx, "seed-determinism")
    b = winning_line(fx, "seed-determinism")
    ra, rb = a.receipt(), b.receipt()
    assert canonical(ra) == canonical(rb)            # byte-identical, not just hash-equal
    assert ra["sha256"] == rb["sha256"]
    assert ra["session_id"] == b.session_id == world_session_id("seed-determinism", False,
                                                                DEFAULT_WORLD)


def test_wow_world_splice_save_load_byte_identical(fx):
    whole = winning_line(fx, "seed-splice")
    part = WorldSession(fx, "seed-splice")
    part.turn("look")
    part.turn("go", "north")
    part.turn("go", "east")
    part.save()
    resumed = WorldSession.load(part.session_id)
    assert resumed is not None and resumed.room == "vault"
    for _ in range(1 + DRAW_TARGET):
        resumed.turn("look")
    assert canonical(resumed.receipt()) == canonical(whole.receipt())


def test_wow_world_receipt_schema_and_self_hash(fx):
    ses = winning_line(fx, "t-schema")
    r = ses.receipt()
    for key in ("schema", "session_id", "seed", "world", "world_sha256_12", "room", "route",
                "bones_digest", "session_status", "encounter_state", "draw_index", "moves",
                "verdict", "sha256"):
        assert key in r, f"receipt missing {key}"
    assert r["schema"] == RECEIPT_SCHEMA
    assert r["room"] == "vault" and r["route"][-1] == "vault"
    body = {k: v for k, v in r.items() if k != "sha256"}
    assert r["sha256"] == hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()
    for m in r["moves"]:
        base = {"n", "verb", "arg", "room", "ok", "reason", "handler_ran"}
        allowed = base | ({"handler", "to"} if m["verb"] == "go" else {"handler"}) \
            if m["ok"] else base
        assert base <= set(m) <= allowed, f"move keys off-contract: {sorted(m)}"
        assert m["handler_ran"] is (m["ok"] is True)


def test_wow_world_world_digest_binds_the_table():
    d = world_digest(DEFAULT_WORLD)
    assert len(d) == 12 and int(d, 16) >= 0
    mutated = {**DEFAULT_WORLD, "rooms": [
        {**r, "id": "atrium_x"} if r["id"] == "atrium" else r for r in DEFAULT_WORLD["rooms"]]}
    assert world_digest(mutated) != d


def test_wow_world_cli_start_turn_receipt(fx, capsys):
    from mag import wow_world
    assert wow_world.main(["start", "--seed", "t-cli"]) == 0
    sid = canonical_check(capsys)["session_id"]
    assert wow_world.main(["turn", "--session", sid, "--verb", "go", "--arg", "north"]) == 0
    body = canonical_check(capsys)
    assert body["ok"] is True
    assert wow_world.main(["receipt", "--session", sid]) == 0
    receipt = canonical_check(capsys)
    assert receipt["session_id"] == sid
    assert receipt["verdict"] == "OPEN"


def canonical_check(capsys):
    import json
    return json.loads(capsys.readouterr().out)
