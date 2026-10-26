"""chat v1 tests (LW6, S19's spec, 2026-09-30).

Every test is a law from the lane brief:
  - say rides the EXISTING action op, staged at receipt, applied at the
    next tick: the event "user: text" lands in that tick's events array,
    in arrival order with every other verb, zero new wire ops
  - determinism survives chat: two fresh worlds fed the same say/action
    interleaving replay byte-identical logs
  - the text law: empty or >240 chars -> BAD_TEXT (240 itself is legal)
  - whisper is a direct line to the target sid ONLY, readable before any
    tick (outside the canonical tick), never broadcast, never in events
  - the audit chain keeps holding with chat rows in it
  - any registered session can say — a bot (a fish, the innkeeper)
    registers and rides the same channel as a player
  - the table stays honest: CHAT_TABLE is a strict superset contract and
    the bound v0 surface (protocol.VERBS) did not move
"""
from __future__ import annotations

import asyncio
import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import server.protocol as protocol  # noqa: E402
from server.auth import AuthStore  # noqa: E402
from server.protocol_table import (  # noqa: E402
    CHAT_DIGEST,
    CHAT_SPEC,
    CHAT_TABLE,
    DEFAULT_TABLE,
    PROTOCOL_DIGEST,
    ProtocolDispatch,
)
from server.server import Client, WorldServer  # noqa: E402
from server.world import MAX_SAY, MountainWorld  # noqa: E402


# ---------------------------------------------------------- the contract ----

def test_chat_table_is_a_strict_superset_contract():
    assert CHAT_TABLE.verbs == ("boil", "valve", "join", "tag", "say", "whisper")
    assert CHAT_TABLE.rows[:4] == DEFAULT_TABLE.rows  # v0 rows byte-identical
    assert "BAD_TEXT" in CHAT_TABLE.reject_codes
    assert CHAT_DIGEST != PROTOCOL_DIGEST  # a NEW contract version, not an edit
    # the bound v0 wire did not move: the pinned surface keeps its bytes
    assert protocol.VERBS == ("boil", "valve", "join", "tag")
    assert "BAD_TEXT" not in protocol.REJECT_CODES


def test_chat_rows_gate_and_route():
    d = ProtocolDispatch(CHAT_TABLE)
    assert d.dispatch("say", "AUTHED") == {
        "ok": True, "reason": "DISPATCHED", "handler": "world_say",
        "required_state": "AUTHED", "handler_ran": True}
    assert d.dispatch("whisper", "AUTHED")["handler"] == "world_whisper"
    for verb in ("say", "whisper"):
        assert d.dispatch(verb, "CONNECTED") == {
            "ok": False, "reason": "UNKNOWN_SID", "handler_ran": False}
    assert d.dispatch("dance", "AUTHED")["reason"] == "UNKNOWN_VERB"
    assert CHAT_SPEC["rows"][-2]["handler_name"] == "world_say"
    assert CHAT_SPEC["rows"][-1]["handler_name"] == "world_whisper"


# ------------------------------------------------------------------ say ----

def test_say_appears_in_next_tick_events():
    w = MountainWorld()
    w.register_session("s1", "ada")
    reply = w.stage("s1", "say", "hello world")
    assert reply == {"op": "ack", "verb": "say", "target": "hello world",
                     "user": "ada", "applies_at_tick": 1}
    # not yet: say is staged like every other verb, the tick is still the
    # only mutator
    assert w.direct == [] and len(w.pending) == 1
    t = w.tick()
    assert "ada: hello world" in t["events"]
    assert w.pending == []
    action_rows = [r for r in w.rows if r["kind"] == "action"]
    assert action_rows[-1]["verb"] == "say"
    assert action_rows[-1]["event"] == "ada: hello world"
    assert w.verify_log() is True


def test_say_interleaves_in_arrival_order():
    w = MountainWorld()
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    assert w.stage("s1", "say", "first")["op"] == "ack"
    assert w.stage("s2", "tag", "hollow")["op"] == "ack"
    assert w.stage("s1", "say", "second")["op"] == "ack"
    t = w.tick()
    i_hello = t["events"].index("ada: first")
    i_tag = t["events"].index("ben tags a fish at hollow (score 1).")
    i_bye = t["events"].index("ada: second")
    assert i_hello < i_tag < i_bye  # arrival order, one channel


def test_say_determinism_two_fresh_worlds_byte_identical():
    def run():
        w = MountainWorld()
        w.register_session("s1", "ada")
        w.register_session("s2", "innkeeper")
        w.stage("s1", "say", "rounds on the house")
        w.stage("s1", "boil", "spring")
        w.tick()
        w.stage("s2", "say", "mind the gate")
        w.stage("s2", "valve", "p_bypass")
        w.tick()
        return ([json.dumps(r, sort_keys=True) for r in w.rows],
                json.dumps(w.node_volumes(), sort_keys=True))

    rows_a, vols_a = run()
    rows_b, vols_b = run()
    assert rows_a == rows_b and vols_a == vols_b


def test_say_text_law_empty_and_over_length_reject():
    w = MountainWorld()
    w.register_session("s1", "ada")
    assert w.stage("s1", "say", "")["why"] == "BAD_TEXT"
    assert w.stage("s1", "say", "x" * (MAX_SAY + 1))["why"] == "BAD_TEXT"
    # the boundary itself is legal: 240 chars pass
    assert w.stage("s1", "say", "x" * MAX_SAY)["op"] == "ack"
    assert "ada: " + "x" * MAX_SAY in w.tick()["events"]
    assert MAX_SAY == 240  # the S19 spec number, pinned


def test_say_requires_a_registered_session():
    w = MountainWorld()
    assert w.stage("ghost", "say", "anyone?")["why"] == "UNKNOWN_SID"


# -------------------------------------------------------------- whisper ----

def test_whisper_is_a_direct_line_to_the_target_sid_only():
    w = MountainWorld()
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    w.register_session("s3", "cy")
    reply = w.stage("s1", "whisper", "ben|psst")
    assert reply == {"op": "ack", "verb": "whisper",
                     "target": "ben|psst", "user": "ada"}
    # delivered OUTSIDE the canonical tick: readable before any tick,
    # never staged, never broadcast
    assert w.pending == []
    assert w.drain_direct("s2") == [{"op": "whisper", "from": "ada", "text": "psst"}]
    assert w.drain_direct("s1") == []   # not the sender
    assert w.drain_direct("s3") == []   # not anyone else
    t = w.tick()
    assert "psst" not in " | ".join(t["events"])  # never in tick events
    assert w.drain_direct("s2") == []             # already taken, once only


def test_whisper_reaches_every_sid_of_the_target_user():
    w = MountainWorld()
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")     # ben, first session
    w.register_session("s3", "cy")
    w.register_session("s4", "ben")     # ben, second session
    assert w.stage("s1", "whisper", "ben|both screens")["op"] == "ack"
    for sid in ("s2", "s4"):
        assert w.drain_direct(sid) == [
            {"op": "whisper", "from": "ada", "text": "both screens"}]
    assert w.drain_direct("s3") == []


def test_whisper_target_and_text_law():
    w = MountainWorld()
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    # malformed: no pipe, empty user, empty text, over-length text
    assert w.stage("s1", "whisper", "ben")["why"] == "BAD_TEXT"
    assert w.stage("s1", "whisper", "|hi")["why"] == "BAD_TEXT"
    assert w.stage("s1", "whisper", "ben|")["why"] == "BAD_TEXT"
    assert w.stage("s1", "whisper", "ben|" + "x" * (MAX_SAY + 1))["why"] == "BAD_TEXT"
    # a user with no registered session is an unknown target
    assert w.stage("s1", "whisper", "nobody|hi")["why"] == "UNKNOWN_TARGET"
    # unauthed sid rejects before any text is read
    assert w.stage("ghost", "whisper", "ben|hi")["why"] == "UNKNOWN_SID"
    # the FIRST pipe splits; the text may carry more pipes
    assert w.stage("s1", "whisper", "ben|left|right")["op"] == "ack"
    assert w.drain_direct("s2") == [
        {"op": "whisper", "from": "ada", "text": "left|right"}]


def test_whisper_row_is_audited_outside_the_tick_events():
    w = MountainWorld()
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    w.stage("s1", "whisper", "ben|quiet")
    w.stage("s1", "say", "loud")
    w.tick()
    kinds = [r["kind"] for r in w.rows]
    assert kinds == ["whisper", "action", "tick"]
    whisper_row = w.rows[0]
    assert whisper_row["tick"] == 1      # every row kind carries a tick field
    assert whisper_row["user"] == "ada"
    assert "quiet" not in w.rows[2]["events"][0]  # say event only
    assert w.verify_log() is True


def test_whisper_mutates_no_world_state():
    w = MountainWorld()
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    before = w.node_volumes()
    w.stage("s1", "whisper", "ben|no physics touches this")
    assert w.node_volumes() == before
    assert w.pending == []
    # the physics still runs its tick normally afterwards
    assert w.tick()["op"] == "tick"


# ------------------------------------------------------------- the bots ----

def test_bot_sessions_say_on_the_same_channel():
    w = MountainWorld()
    w.register_session("s_player", "ada")
    w.register_session("s_innkeeper", "innkeeper")   # a bot: register + say
    w.register_session("s_fish", "fish_scout")       # another bot
    assert w.stage("s_player", "say", "anyone here?")["op"] == "ack"
    assert w.stage("s_innkeeper", "say", "rounds on the house")["op"] == "ack"
    assert w.stage("s_fish", "say", "blub")["op"] == "ack"
    t = w.tick()
    assert t["events"][:3] == [
        "ada: anyone here?",
        "innkeeper: rounds on the house",
        "fish_scout: blub",
    ]
    # bots whisper on the same path too
    assert w.stage("s_innkeeper", "whisper", "ada|your room is ready")["op"] == "ack"
    assert w.drain_direct("s_player") == [
        {"op": "whisper", "from": "innkeeper", "text": "your room is ready"}]


# ----------------------------------------------------- the real wire (TCP) ----

async def _start_server(tmp_path: Path) -> WorldServer:
    auth = AuthStore(tmp_path / "users.json")
    auth.ensure_user("ada", "steam")
    auth.ensure_user("ben", "fish")
    srv = WorldServer(
        port=0, tick_interval=None, auth=auth,
        log_path=tmp_path / "world_log.jsonl",
    )
    return await srv.start()


async def _ask(client: Client, sid: str, verb: str, target: str) -> dict:
    await client.send({"op": "action", "sid": sid, "verb": verb, "target": target})
    return await client.recv()


def test_say_rides_the_existing_action_op_over_tcp(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = (await c.do_hello("ada", "steam"))["sid"]
        # zero new ops: the v0 action line, verb=say, nothing else changed
        ack = await _ask(c, sid, "say", "first words on the wire")
        assert ack == {"op": "ack", "verb": "say",
                       "target": "first words on the wire",
                       "user": "ada", "applies_at_tick": 1}
        over = await _ask(c, sid, "say", "x" * 241)
        assert over["why"] == "BAD_TEXT"
        await srv.pump_once()
        t = await c.recv()
        assert t["op"] == "tick" and "ada: first words on the wire" in t["events"]
        assert srv.stats()["actions_staged"] == 1
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_whisper_over_the_wire_lands_in_the_target_outbox_only(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c1 = await Client.connect("127.0.0.1", srv.bound_port)
        c2 = await Client.connect("127.0.0.1", srv.bound_port)
        sid1 = (await c1.do_hello("ada", "steam"))["sid"]
        sid2 = (await c2.do_hello("ben", "fish"))["sid"]
        ack = await _ask(c1, sid1, "whisper", "ben|over the wire, quietly")
        assert ack["op"] == "ack" and ack["verb"] == "whisper"
        # server-side queue routing is the next lane (server.py fence); the
        # world-side law already holds: the line waits for ben's sid alone
        assert srv.world.drain_direct(sid2) == [
            {"op": "whisper", "from": "ada", "text": "over the wire, quietly"}]
        assert srv.world.drain_direct(sid1) == []
        c1.close()
        c2.close()
        await srv.stop()

    asyncio.run(scenario())


# --------------------------------------------------- no collateral damage ----

def test_v0_verbs_still_reject_their_old_way():
    w = MountainWorld()
    w.register_session("s1", "ada")
    assert w.stage("s1", "boil", "volcano")["why"] == "UNKNOWN_TARGET"
    assert w.stage("s1", "dance", "spring")["why"] == "UNKNOWN_VERB"
    assert w.stage("s1", "tag", "crown")["why"] == "DRY_POOL"
    assert w.stage("s1", "say", "x" * MAX_SAY)["op"] == "ack"


def test_chat_spec_is_still_a_pure_function_of_its_bytes():
    from server.protocol_table import compile_table
    fresh = compile_table(copy.deepcopy(CHAT_SPEC))
    assert fresh.digest == CHAT_DIGEST
    assert fresh.verbs == CHAT_TABLE.verbs
