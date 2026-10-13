"""rooms tests (B15, 2026-09-30): minimal multi-room v0.

Laws under test (receipt watch/inbox/last_mile_20260930/B15_ROOMS.md):
  - two rooms tick independently: separate worlds, separate tick counters,
    each room's own pump drives only its own world
  - cross-room isolation, hard: a tick in room A NEVER broadcasts to room B
    -- room B's raw broadcast bytes are byte-identical to a solo world run
    with no other rooms in play, and room A's client receives nothing when
    room B pumps (and vice versa)
  - join/default compat: a client that never says a room lands in "summit"
    (welcome states it, the default room's log lands at exactly the log_path
    the server was given, and the old no-room action wire still stages)
  - the action's room argument: a room-naming action works for a sid issued
    by that room, UNKNOWN_ROOM for a room no hello ever made, BAD_ROOM for
    a malformed id, and a sid from another room meets that world's own
    UNKNOWN_SID (routing is honest, not guessed)
  - the innkeeper is per-room with memories scoped per room: two visits to
    one room earn "Welcome back", the first visit to the other room still
    hears "Welcome" -- and the memory files are distinct paths
  - capacity: a soft cap per room; a full room refuses hello with ROOM_FULL
    before any sid is issued, and the refused connection keeps its old
    binding; capacity counts seats (peers), not sessions
  - empty side rooms sleep (pump stops with the last peer, world stays
    open) while the default room keeps the server's cadence

Every wire law is proven against a REAL in-process TCP server on an
ephemeral port (the test_server_v0 house style).
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.auth import AuthStore  # noqa: E402
from server.protocol import encode  # noqa: E402
from server.rooms import DEFAULT_ROOM  # noqa: E402
from server.server import Client, WorldServer  # noqa: E402
from server.world import MountainWorld  # noqa: E402


async def _start_server(
    tmp_path: Path,
    tick_interval: float | None = None,
    room_capacity: int | None = None,
) -> WorldServer:
    auth = AuthStore(tmp_path / "users.json")
    for user, pw in (("ada", "steam"), ("ben", "fish"), ("cy", "kerosene")):
        auth.ensure_user(user, pw)
    kwargs: dict = {"port": 0, "tick_interval": tick_interval, "auth": auth,
                    "log_path": tmp_path / "world_log.jsonl"}
    if room_capacity is not None:
        kwargs["room_capacity"] = room_capacity
    srv = WorldServer(**kwargs)
    return await srv.start()


async def _ask(client: Client, sid: str, verb: str, target: str,
               room: str | None = None) -> dict:
    """Manual mode: the very next line after an action is its reply."""
    msg: dict = {"op": "action", "sid": sid, "verb": verb, "target": target}
    if room is not None:
        msg["room"] = room
    await client.send(msg)
    return await client.recv()


async def _hello_raw(client: Client, user: str, pw: str,
                     room: object = None) -> dict:
    """hello read as the NEXT line, so rejects (ROOM_FULL/BAD_ROOM) surface."""
    msg: dict = {"op": "hello", "user": user, "pass": pw}
    if room is not None:
        msg["room"] = room
    await client.send(msg)
    return await client.recv()


async def _assert_silent(client: Client, timeout: float = 0.15) -> None:
    """The isolation lens: nothing this room did not broadcast to us."""
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(client.recv(), timeout=timeout)


def _events(tick: dict) -> str:
    return " | ".join(tick.get("events", []))


# -------------------------------------------------------- independence ----

def test_two_rooms_tick_independently(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c_ada = await Client.connect("127.0.0.1", srv.bound_port)
        c_ben = await Client.connect("127.0.0.1", srv.bound_port)
        w_ada = await c_ada.do_hello("ada", "steam")            # no room: summit
        w_ben = await c_ben.do_hello("ben", "fish", room="basecamp")
        assert w_ada["room"] == "summit" and w_ben["room"] == "basecamp"
        # one world per room: distinct objects, distinct logs
        assert srv.rooms["summit"].world is not srv.rooms["basecamp"].world

        # ada boils in summit; ben stages a tag in basecamp
        assert (await _ask(c_ada, w_ada["sid"], "boil", "spring"))["op"] == "ack"
        assert (await _ask(c_ben, w_ben["sid"], "tag", "hollow"))["op"] == "ack"

        # summit's pump advances ONLY summit
        srv.rooms["summit"].pump_once()
        t_ada = await c_ada.recv()
        assert t_ada["op"] == "tick" and t_ada["n"] == 1
        assert "ada boils 1 at spring; it rises." in t_ada["events"]
        await _assert_silent(c_ben)  # basecamp's wire never saw summit's tick

        # basecamp's pump advances ONLY basecamp: same tick number, a
        # different world -- ben's events, not ada's
        srv.rooms["basecamp"].pump_once()
        t_ben = await c_ben.recv()
        assert t_ben["op"] == "tick" and t_ben["n"] == 1  # independent clock
        assert "ben tags a fish at hollow (score 1)." in t_ben["events"]
        assert "ada" not in _events(t_ben)
        await _assert_silent(c_ada)

        # and the clocks drift: pump summit again, basecamp stays at 1
        srv.rooms["summit"].pump_once()
        assert (await c_ada.recv())["n"] == 2
        assert srv.rooms["summit"].world.graph.tick_count == 2
        assert srv.rooms["basecamp"].world.graph.tick_count == 1
        assert srv.rooms["summit"].world.node_volumes() != \
            srv.rooms["basecamp"].world.node_volumes()  # different histories

        c_ada.close()
        c_ben.close()
        await srv.stop()

    asyncio.run(scenario())


def test_cross_room_isolation_is_byte_hard(tmp_path):
    """Room B's broadcast must be BYTE-IDENTICAL to a solo world: the
    presence and actions of room A leave no trace on room B's wire."""
    async def scenario():
        srv = await _start_server(tmp_path)
        c_ada = await Client.connect("127.0.0.1", srv.bound_port)
        c_ben = await Client.connect("127.0.0.1", srv.bound_port)
        w_ada = await c_ada.do_hello("ada", "steam")
        w_ben = await c_ben.do_hello("ben", "fish", room="basecamp")
        # ada is loud in summit (two verbs, two sids)
        sid2 = (await c_ada.do_hello("ada", "steam"))["sid"]
        assert (await _ask(c_ada, w_ada["sid"], "boil", "spring"))["op"] == "ack"
        assert (await _ask(c_ada, sid2, "say", "summit is the only world"))["op"] == "ack"

        # basecamp ticks alone, twice; ben's raw bytes must equal a fresh
        # solo world ticked the same way (determinism law does the diffing)
        solo = MountainWorld()
        try:
            srv.rooms["basecamp"].pump_once()
            srv.rooms["basecamp"].pump_once()
            raw1, raw2 = await c_ben.recv_raw(), await c_ben.recv_raw()
            assert raw1 == encode(solo.tick())
            assert raw2 == encode(solo.tick())
            assert "ada" not in raw1.decode() and "ada" not in raw2.decode()
        finally:
            solo.close()
        await _assert_silent(c_ada)  # ada's wire never saw basecamp's ticks

        # the whole-server beat pumps BOTH rooms: each client gets exactly
        # its own room's line and then silence
        await srv.pump_once()
        assert (await c_ada.recv())["n"] == 1   # summit tick 1 (ada's boil+say)
        assert (await c_ben.recv())["n"] == 3   # basecamp tick 3
        await _assert_silent(c_ada)
        await _assert_silent(c_ben)

        c_ada.close()
        c_ben.close()
        await srv.stop()

    asyncio.run(scenario())


# ------------------------------------------------------ join / default ----

def test_join_without_room_lands_in_summit_and_log_is_unchanged(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c_old = await Client.connect("127.0.0.1", srv.bound_port)  # a v0 client
        w = await c_old.do_hello("ada", "steam")  # no room key on the wire
        assert w["op"] == "welcome" and w["room"] == DEFAULT_ROOM == "summit"
        sid = w["sid"]
        # the old action line (no room) still stages in the default room
        assert (await _ask(c_old, sid, "boil", "spring"))["op"] == "ack"
        await srv.pump_once()
        t = await c_old.recv()
        assert t["n"] == 1 and "ada boils 1 at spring; it rises." in t["events"]
        # the default room's log is EXACTLY the log_path given (compat law)
        log = tmp_path / "world_log.jsonl"
        assert log.exists()
        rows = [json.loads(x) for x in log.read_text("utf-8").splitlines() if x]
        assert rows and all(r["seq"] == i + 1 for i, r in enumerate(rows))
        # naming the default room explicitly is the same room
        c_new = await Client.connect("127.0.0.1", srv.bound_port)
        w2 = await c_new.do_hello("ben", "fish", room="summit")
        assert w2["room"] == "summit"
        assert (await _ask(c_new, w2["sid"], "join", "terrace",
                           room="summit"))["op"] == "ack"
        c_old.close()
        c_new.close()
        await srv.stop()

    asyncio.run(scenario())


def test_action_room_argument_routes_and_refuses_honestly(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        w_ada = await c.do_hello("ada", "steam")
        w_ben = await c.do_hello("ben", "fish", room="basecamp")
        # the join verb with a room argument stages in that room's world
        ack = await _ask(c, w_ben["sid"], "join", "terrace", room="basecamp")
        assert ack == {"op": "ack", "verb": "join", "target": "terrace",
                       "user": "ben", "applies_at_tick": 1}
        # a room no hello ever made: typed refusal, never a guess
        r = await _ask(c, w_ada["sid"], "join", "terrace", room="ghost")
        assert r["op"] == "reject" and r["why"] == "UNKNOWN_ROOM"
        # malformed ids (str and non-str) refuse BAD_ROOM on both surfaces
        r = await _ask(c, w_ada["sid"], "join", "terrace", room="Not A Room")
        assert r["why"] == "BAD_ROOM"
        r = await _ask(c, w_ada["sid"], "join", "terrace", room=7)
        assert r["why"] == "BAD_ROOM"
        assert (await _hello_raw(c, "ada", "steam", room="Not A Room"))["why"] == "BAD_ROOM"
        assert (await _hello_raw(c, "ada", "steam", room=7))["why"] == "BAD_ROOM"
        # a summit sid naming basecamp: basecamp's world never issued it,
        # and its own honest answer is UNKNOWN_SID
        r = await _ask(c, w_ada["sid"], "join", "terrace", room="basecamp")
        assert r["why"] == "UNKNOWN_SID"
        # the staged join really applies in basecamp alone
        srv.rooms["basecamp"].pump_once()
        t = await c.recv()
        assert "ben joins at terrace." in t["events"]
        c.close()
        await srv.stop()

    asyncio.run(scenario())


# -------------------------------------------------------- innkeeper ----

def test_innkeeper_is_per_room_with_scoped_memories(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)

        async def visit(room_id: str | None, user: str, pw: str) -> dict:
            c = await Client.connect("127.0.0.1", srv.bound_port)
            w = await c.do_hello(user, pw, room=room_id)
            assert (await _ask(c, w["sid"], "join", "spring"))["op"] == "ack"
            room = srv.rooms[w["room"]]
            room.pump_once()
            t1 = await c.recv()   # the join event, no greeting yet
            room.pump_once()
            t2 = await c.recv()   # the innkeeper's staged say applies here
            c.close()
            return {"welcome": w, "t1": t1, "t2": t2}

        v1 = await visit(None, "ada", "steam")            # summit, first visit
        assert "ada joins at spring." in v1["t1"]["events"]
        assert any(e.startswith("innkeeper: Welcome, ada")
                   for e in v1["t2"]["events"])
        assert not any("Welcome back" in e for e in v1["t2"]["events"])

        v2 = await visit(None, "ada", "steam")            # summit, known now
        assert any(e.startswith("innkeeper: Welcome back, ada")
                   for e in v2["t2"]["events"])

        # same player, other room: a STRANGER there -- scoping proven
        v3 = await visit("basecamp", "ada", "steam")
        assert v3["welcome"]["room"] == "basecamp"
        assert any(e.startswith("innkeeper: Welcome, ada")
                   for e in v3["t2"]["events"])
        assert not any("Welcome back" in e for e in v3["t2"]["events"])

        # memories are distinct files with distinct truth
        mem_summit = tmp_path / "world_log.players.json"
        mem_base = tmp_path / "world_log.basecamp.players.json"
        assert mem_summit.exists() and mem_base.exists()
        s = json.loads(mem_summit.read_text("utf-8"))["ada"]
        b = json.loads(mem_base.read_text("utf-8"))["ada"]
        assert s["visits"] == 2 and b["visits"] == 1
        # side rooms get durable roots beside the standing log
        assert (tmp_path / "world_log.basecamp.jsonl").exists()
        await srv.stop()

    asyncio.run(scenario())


# ---------------------------------------------------------- capacity ----

def test_capacity_soft_cap_refuses_honestly(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path, room_capacity=2)
        c1 = await Client.connect("127.0.0.1", srv.bound_port)
        c2 = await Client.connect("127.0.0.1", srv.bound_port)
        c3 = await Client.connect("127.0.0.1", srv.bound_port)
        assert (await c1.do_hello("ada", "steam", room="bothy"))["room"] == "bothy"
        assert (await c2.do_hello("ben", "fish", room="bothy"))["room"] == "bothy"
        # the third seat: refused BEFORE a sid is issued, with the room named
        r = await _hello_raw(c3, "cy", "kerosene", room="bothy")
        assert r == {"op": "reject", "why": "ROOM_FULL", "room": "bothy"}
        assert "sid" not in r
        assert srv.rooms["bothy"].world.roster.get("cy") is None
        # honest refusal leaves the caller free: cy seats in the default room
        assert (await c3.do_hello("cy", "kerosene"))["room"] == "summit"
        # capacity counts SEATS, not sessions: one connection holding two
        # sessions in a cap-1 room never fills its own seat
        srv2 = await _start_server(tmp_path / "cap1", room_capacity=1)
        c = await Client.connect("127.0.0.1", srv2.bound_port)
        w1 = await c.do_hello("ada", "steam", room="den")
        w2 = await c.do_hello("ada", "steam", room="den")  # re-hello: same seat
        assert w1["room"] == w2["room"] == "den"
        assert len(srv2.rooms["den"].peers) == 1
        c1.close()
        c2.close()
        c3.close()
        c.close()
        await srv.stop()
        await srv2.stop()

    asyncio.run(scenario())


# ------------------------------------------------------ the sleep law ----

def test_empty_side_room_sleeps_default_room_keeps_cadence(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path, tick_interval=0.03)
        c_b = await Client.connect("127.0.0.1", srv.bound_port)
        c_s = await Client.connect("127.0.0.1", srv.bound_port)
        await c_b.do_hello("ben", "fish", room="bothy")
        await c_s.do_hello("ada", "steam")
        bothy = srv.rooms["bothy"]
        assert bothy.pumping and srv.rooms["summit"].pumping
        # both rooms tick on their own pumps
        t1 = await asyncio.wait_for(c_b.recv(), timeout=5.0)
        t2 = await asyncio.wait_for(c_b.recv(), timeout=5.0)
        assert t1["op"] == t2["op"] == "tick" and t2["n"] == t1["n"] + 1
        ben_ticks = bothy.world.graph.tick_count
        c_b.close()  # the last peer leaves the side room
        await asyncio.sleep(0.25)
        assert not bothy.pumping                    # asleep...
        assert bothy.world.graph.tick_count == ben_ticks  # ...and frozen
        assert srv.rooms["summit"].pumping          # the default room never sleeps
        # drain ada's buffered ticks: the standing room ticked through the
        # whole window (>=3 ticks in 0.25s at a 0.03s cadence)
        t = None
        for _ in range(8):
            t = await asyncio.wait_for(c_s.recv(), timeout=5.0)
            assert t["op"] == "tick"
            if t["n"] >= 3:
                break
        assert t is not None and t["n"] >= 3
        c_s.close()
        await srv.stop()

    asyncio.run(scenario())
