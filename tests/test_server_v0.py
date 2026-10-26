"""server v0 tests: the estate's own world server.

Every test is a law: the wire round-trips against a REAL in-process TCP
server on an ephemeral port, auth works and wrong passwords reject, all
action reject types fire, two fresh worlds fed the same action sequence
produce byte-identical node-volume sequences, two clients see the same
broadcast bytes, WIN is detected and sticky, and the event log is
append-only and tamper-evident.
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.auth import AuthStore  # noqa: E402
from server.protocol import REJECT_CODES, decode_line, encode  # noqa: E402
from server.server import Client, WorldServer  # noqa: E402
from server.world import (  # noqa: E402
    GENESIS,
    MountainWorld,
    actor_class_of,
    load_log_rows,
    row_sha,
    verify_log_rows,
)


async def _start_server(tmp_path: Path, tick_interval: float | None = None) -> WorldServer:
    auth = AuthStore(tmp_path / "users.json")
    auth.ensure_user("ada", "steam")
    auth.ensure_user("ben", "fish")
    srv = WorldServer(
        port=0, tick_interval=tick_interval, auth=auth,
        log_path=tmp_path / "world_log.jsonl",
    )
    return await srv.start()


async def _ask(client: Client, sid: str, verb: str, target: str) -> dict:
    """Manual mode: the very next line after an action is its reply."""
    await client.send({"op": "action", "sid": sid, "verb": verb, "target": target})
    return await client.recv()


# ------------------------------------------------------------- protocol ----

def test_hello_welcome_roundtrip_and_snapshot(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        w = await c.do_hello("ada", "steam")
        assert w["op"] == "welcome"
        sid = w["sid"]
        assert len(sid) == 64 and int(sid, 16) >= 0
        snap = w["world"]
        # rot joined the node spec dict additively (VORTEX law, 2026-10-10):
        # same family as steam (V-wave) and stress/fractured (AC2) before it.
        # sill joins the same way (LATCH roundtrip law, 2026-10-12, cycle 5:
        # the latch LEVEL is runtime gate state; always emitted, additive).
        assert snap["nodes"]["spring"] == {"elev": 10, "kind": "plain", "sill": 0, "volume": 6, "steam": 0, "rot": 0}
        assert snap["nodes"]["gate1"]["kind"] == "xor"
        assert snap["nodes"]["crown"]["kind"] == "cold"
        assert snap["nodes"]["hollow"]["volume"] == 2
        assert snap["pipes"]["p_bypass"]["siphon"] is True
        assert snap["pipes"]["p_bypass"]["crest"] == 2
        assert snap["pipes"]["p_bypass"]["open"] is False  # starts shut
        assert snap["win_crown"] == 4 and snap["winner"] is False
        ack = await _ask(c, sid, "boil", "spring")
        assert ack == {"op": "ack", "verb": "boil", "target": "spring",
                       "user": "ada", "applies_at_tick": 1}
        await srv.pump_once()
        t = await c.recv()
        assert t["op"] == "tick" and t["n"] == 1
        assert t["nodes"]["spring"] == 4  # 6 minus 1 boiled minus 1 gravity-fed to gate1
        assert t["nodes"]["crown"] == 1  # steam condenses at the highest cold node
        assert t["nodes"]["hollow"] == 2  # drained 1 to waste, refilled 1 via gate1
        assert t["winner"] is False
        assert "ada boils 1 at spring; it rises." in t["events"]
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_wrong_password_and_unknown_user_reject(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        await c.send({"op": "hello", "user": "ada", "pass": "wrong"})
        r = await c.recv()
        assert r == {"op": "reject", "why": "BAD_AUTH"}
        await c.send({"op": "hello", "user": "nobody", "pass": "steam"})
        r = await c.recv()
        assert r["why"] == "BAD_AUTH"  # one code: no user enumeration on the wire
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_action_reject_types(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        # action before any hello
        r = await _ask(c, "bogus-sid", "boil", "spring")
        assert r["why"] == "UNKNOWN_SID"
        w = await c.do_hello("ada", "steam")
        sid = w["sid"]
        # a well-formed but never-issued sid
        r = await _ask(c, "f" * 64, "boil", "spring")
        assert r["why"] == "UNKNOWN_SID"
        r = await _ask(c, sid, "dance", "spring")
        assert r["why"] == "UNKNOWN_VERB"
        r = await _ask(c, sid, "boil", "volcano")
        assert r["why"] == "UNKNOWN_TARGET"
        r = await _ask(c, sid, "valve", "p_magic")
        assert r["why"] == "UNKNOWN_TARGET"
        r = await _ask(c, sid, "join", "mars")
        assert r["why"] == "UNKNOWN_TARGET"
        r = await _ask(c, sid, "tag", "moon")
        assert r["why"] == "UNKNOWN_TARGET"
        # crown starts dry, waste never fills: both are DRY_POOL for boil/tag
        r = await _ask(c, sid, "boil", "crown")
        assert r["why"] == "DRY_POOL"
        r = await _ask(c, sid, "tag", "waste")
        assert r["why"] == "DRY_POOL"
        # NOT_YOUR_TURN is reserved vocabulary, never emitted by v0
        assert "NOT_YOUR_TURN" in REJECT_CODES
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_not_your_turn_is_reserved_never_emitted():
    world = MountainWorld()
    world.register_session("s1", "ada")
    whys = set()
    for verb in ("boil", "valve", "join", "tag", "dance", ""):
        for target in ("spring", "volcano", "p_bypass", "p_magic", "crown", ""):
            reply = world.stage("s1", verb, target)
            if reply["op"] == "reject":
                whys.add(reply["why"])
    assert "NOT_YOUR_TURN" not in whys
    assert whys == {"UNKNOWN_VERB", "UNKNOWN_TARGET", "DRY_POOL"}


def test_unknown_op_and_bad_json_reject(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        await c.send({"op": "teleport", "x": 1})
        r = await c.recv()
        assert r["why"] == "UNKNOWN_OP"
        c.writer.write(b"this is not json\n")
        await c.writer.drain()
        r = await c.recv()
        assert r["why"] == "BAD_JSON"
        c.close()
        await srv.stop()

    asyncio.run(scenario())


# ------------------------------------------------------------- behavior ----

def test_join_tag_and_valve_apply_at_tick(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        # LW7 (S20 rate cap, 2026-09-30): one staged action per sid per
        # tick, so this one-tick three-verb script rides three sids (all
        # ben: the events carry the USER, the budget is per-SID). What
        # the test proves is unchanged: all three verbs apply at the same
        # tick, in arrival order.
        sids = [(await c.do_hello("ben", "fish"))["sid"] for _ in range(3)]
        assert (await _ask(c, sids[0], "join", "terrace"))["op"] == "ack"
        assert (await _ask(c, sids[1], "tag", "hollow"))["op"] == "ack"
        assert (await _ask(c, sids[2], "valve", "p_bypass"))["op"] == "ack"
        await srv.pump_once()
        t = await c.recv()
        ev = " | ".join(t["events"])
        assert "ben joins at terrace." in ev
        assert "ben tags a fish at hollow (score 1)." in ev
        assert "ben opens p_bypass." in ev
        assert "Siphon p_bypass primes at crest (2)." in ev
        # pipes evaluate in insertion order: p_terrace computed its inflow
        # BEFORE p_bypass filled terrace, so gate1 passes this tick...
        assert "Junction gate1 passes (p_spring sole inlet)." in ev
        assert t["nodes"]["terrace"] == 1
        assert t["nodes"]["gate1"] == 0
        # ...and HOLDS on the next tick when both inlets deliver: the XOR
        await srv.pump_once()
        t = await c.recv()
        assert "Junction gate1 holds 2 below gate (2 inlets); pooling." in t["events"]
        assert t["nodes"]["gate1"] == 2
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_valve_on_burst_pipe_names_the_burst():
    """Valve-honesty law (2026-10-10, receipt receipt_20261010_mariner.md;
    cycle 1 finding 4 probed the lie on this path: the row claimed
    "u1 opens p_spring." while the pipe stayed shut). A valve verb on a
    fractured pipe must word the burst, change nothing, and keep the
    chain verifiable. The burst is injected at the AJ4-feeder end state
    (fracture is unreachable in stock play, cycle 1 finding 3)."""
    world = MountainWorld()
    world.register_session("s1", "ada")
    world.graph.pipes["p_bypass"].fractured = True
    reply = world.stage("s1", "valve", "p_bypass")
    assert reply["op"] == "ack"
    t = world.tick()
    ev = " | ".join(t["events"])
    assert "ada spins the valve on p_bypass; the pipe is burst (closed for good)." in ev
    assert "ada opens p_bypass" not in ev, "the hash-chain lie must stay dead"
    assert world.graph.pipes["p_bypass"].open is False
    assert world.graph.pipes["p_bypass"].fractured is True
    assert world.verify_log()


def test_two_clients_see_identical_broadcast_bytes(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c1 = await Client.connect("127.0.0.1", srv.bound_port)
        c2 = await Client.connect("127.0.0.1", srv.bound_port)
        sid1 = (await c1.do_hello("ada", "steam"))["sid"]
        await c2.do_hello("ben", "fish")
        await _ask(c1, sid1, "boil", "spring")
        await srv.pump_once()
        raw1, raw2 = await c1.recv_raw(), await c2.recv_raw()
        assert raw1 == raw2  # encoded once, same bytes to every client
        t = decode_line(raw1)
        assert t["op"] == "tick" and t["n"] == 1 and t["nodes"]["crown"] == 1
        await srv.pump_once()
        assert (await c1.recv_raw()) == (await c2.recv_raw())
        c1.close()
        c2.close()
        await srv.stop()

    asyncio.run(scenario())


def test_fixed_cadence_ticks_flow_without_manual_pump(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path, tick_interval=0.05)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        await c.do_hello("ada", "steam")
        ns = []
        for _ in range(3):
            t = await asyncio.wait_for(c.recv(), timeout=5.0)
            assert t["op"] == "tick"
            ns.append(t["n"])
        assert ns == [1, 2, 3]  # the server loop drives the cadence
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_win_detection_is_sticky(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = (await c.do_hello("ada", "steam"))["sid"]
        last = None
        for target in ("spring", "spring", "spring", "hollow"):
            assert (await _ask(c, sid, "boil", target))["op"] == "ack"
            await srv.pump_once()
            last = await c.recv()
        assert last["n"] == 4 and last["winner"] is True
        assert last["nodes"]["crown"] == 4
        # the crown has no outlet: winner stays true, the mountain keeps drinking
        await srv.pump_once()
        t = await c.recv()
        assert t["n"] == 5 and t["winner"] is True
        c.close()
        await srv.stop()

    asyncio.run(scenario())


# ---------------------------------------------------------- determinism ----

SCRIPT = [
    ("stage", "s1", "boil", "spring"),
    ("tick",),
    ("stage", "s2", "tag", "hollow"),
    ("stage", "s1", "valve", "p_bypass"),
    ("tick",),
    ("stage", "s1", "boil", "spring"),
    ("stage", "s2", "join", "terrace"),
    ("tick",),
    ("stage", "s1", "boil", "spring"),   # spring is dry here: DRY_POOL, deterministic
    ("stage", "s1", "boil", "gate1"),    # pooled XOR water is still boilable
    ("tick",),
    ("stage", "s2", "tag", "crown"),
    ("stage", "s1", "boil", "crown"),    # crown steam condenses back at the crown
    ("tick",),
]


def _run_script(log_path=None):
    w = MountainWorld(log_path=log_path)
    w.register_session("s1", "ada")
    w.register_session("s2", "ben")
    vols, rows, whys = [], [], set()
    for step in SCRIPT:
        if step[0] == "stage":
            reply = w.stage(step[1], step[2], step[3])
            if reply["op"] == "reject":
                whys.add(reply["why"])
        else:
            w.tick()
            vols.append(json.dumps(w.node_volumes(), sort_keys=True))
    rows = [json.dumps(r, sort_keys=True) for r in w.rows]
    return vols, rows, whys


def test_determinism_two_fresh_worlds_byte_identical():
    vols_a, rows_a, whys_a = _run_script()
    vols_b, rows_b, whys_b = _run_script()
    assert vols_a == vols_b, "same actions, same ticks: volumes must match byte for byte"
    assert rows_a == rows_b, "the whole chained log must replay identically"
    assert whys_a == whys_b == {"DRY_POOL"}
    assert len(vols_a) == 5 and len(rows_a) > 5
    # the script really exercises the board: crown rises, water reaches gate1
    assert json.loads(vols_a[2])["gate1"] == 2  # XOR pools on the both-inlet tick
    assert json.loads(vols_a[3])["crown"] == 3  # boiling pooled water lifts it


def test_determinism_holds_through_the_server_path(tmp_path):
    async def scenario():
        results = []
        for _ in range(2):
            srv = await _start_server(tmp_path / f"u{_}")
            c = await Client.connect("127.0.0.1", srv.bound_port)
            sid = (await c.do_hello("ada", "steam"))["sid"]
            ticks = []
            for target in ("spring", "spring", "spring", "hollow"):
                await _ask(c, sid, "boil", target)
                await srv.pump_once()
                t = await c.recv()
                ticks.append(json.dumps(t["nodes"], sort_keys=True))
            results.append(ticks)
            c.close()
            await srv.stop()
        assert results[0] == results[1]

    asyncio.run(scenario())


# ------------------------------------------------------------- event log ----

def test_event_log_append_only_and_tamper_evident(tmp_path):
    log = tmp_path / "chain.jsonl"
    w = MountainWorld(log_path=log)
    w.register_session("s1", "ada")
    w.stage("s1", "boil", "spring")
    w.tick()
    w.tick()
    w.close()
    rows = load_log_rows(log)
    assert [r["seq"] for r in rows] == list(range(1, len(rows) + 1))
    assert verify_log_rows(rows) is True
    assert rows == w.rows  # file and memory agree
    kinds = [r["kind"] for r in rows]
    assert kinds[0] == "action" and kinds[1] == "tick" and kinds[2] == "tick"

    # reopening continues the chain: append-only across runs
    w2 = MountainWorld(log_path=log)
    w2.register_session("s2", "ben")
    w2.tick()
    w2.close()
    rows2 = load_log_rows(log)
    assert len(rows2) == len(rows) + 1
    assert rows2[-1]["seq"] == rows[-1]["seq"] + 1
    assert rows2[-1]["prev"] == rows[-1]["sha"]
    assert verify_log_rows(rows2) is True

    # tampering with a past row breaks the chain and refuses to load
    lines = log.read_text(encoding="utf-8").splitlines()
    victim = json.loads(lines[0])
    victim["tick"] = 99  # every row kind carries a tick field
    lines[0] = json.dumps(victim, sort_keys=True, separators=(",", ":"))
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_log_rows(log)


# ------------------------------------------ Q23: actor classes on the tape ----

def _q23_world() -> MountainWorld:
    """One tick with one bot hand and one player hand, both channels."""
    w = MountainWorld()
    w.register_session("s_bot", "innkeeper")   # the LW8 bot: a user string
    w.register_session("s1", "ada")
    assert w.stage("s_bot", "say", "rounds on the house")["op"] == "ack"
    assert w.stage("s1", "boil", "spring")["op"] == "ack"
    assert w.stage("s_bot", "whisper", "ada|your room is ready")["op"] == "ack"
    w.tick()
    return w


def test_q23_bot_rows_carry_actor_class_and_verify():
    w = _q23_world()
    bot_rows = [r for r in w.rows if r.get("user") == "innkeeper"]
    kinds = {r["kind"] for r in bot_rows}
    assert kinds == {"action", "whisper"}     # say row + whisper audit row
    for r in bot_rows:
        assert r["actor_class"] == "bot"
    assert actor_class_of("innkeeper") == "bot"
    assert w.verify_log() is True             # the class rides INSIDE the sha


def test_q23_player_rows_default_to_player_and_verify():
    w = _q23_world()
    ada = [r for r in w.rows
           if r.get("user") == "ada" and r["kind"] == "action"]
    assert len(ada) == 1
    # the default is structural: a player row carries NO actor_class field
    assert "actor_class" not in ada[0]
    assert ada[0].get("actor_class", "player") == "player"
    assert actor_class_of("ada") == "player"
    assert w.verify_log() is True


def test_q23_pre_change_shaped_rows_still_verify():
    """Grandfather law: a pre-Q23 row (no actor_class) verifies as-is —
    the sha covers exactly the fields the row carries, so nothing is
    rewritten and old tapes stay legal evidence."""
    old_rows = [
        {"kind": "whisper", "tick": 1,
         "user": "innkeeper", "verb": "whisper", "target": "ada|psst",
         "event": "innkeeper whispers to ada."},
        {"kind": "action", "tick": 1,
         "user": "innkeeper", "verb": "say", "target": "rounds",
         "event": "innkeeper: rounds"},
        {"kind": "action", "tick": 1,
         "user": "ada", "verb": "boil", "target": "spring",
         "event": "ada boils 1 at spring; it rises."},
    ]
    prev = GENESIS                            # chain it exactly like the log
    for i, r in enumerate(old_rows):
        r["seq"], r["prev"] = i + 1, prev
        r["sha"] = row_sha(r)
        prev = r["sha"]
    assert all("actor_class" not in r for r in old_rows)
    assert verify_log_rows(old_rows) is True


def test_q23_tampering_actor_class_breaks_the_sha():
    w = _q23_world()
    assert w.verify_log() is True

    # a bot row laundered into a player row: the sha no longer covers the body
    laundered = [dict(r) for r in w.rows]
    for r in laundered:
        if r.get("user") == "innkeeper":
            r["actor_class"] = "player"       # no re-hash: the tamper
    assert verify_log_rows(laundered) is False

    # a player row promoted to bot breaks too: the ABSENCE is covered —
    # adding the field changes the canonical body the sha committed to
    promoted = [dict(r) for r in w.rows]
    for r in promoted:
        if r.get("user") == "ada" and r["kind"] == "action":
            r["actor_class"] = "bot"
    assert verify_log_rows(promoted) is False


# ----------------------------------------------------------------- auth ----

def test_auth_store_salted_hash_and_sessions(tmp_path):
    store = AuthStore(tmp_path / "users.json")
    store.ensure_user("ada", "steam")
    row = store.users["ada"]
    assert set(row) == {"salt", "hash"}
    assert row["hash"] != __import__("hashlib").sha256(b"steam").hexdigest()
    assert store.verify("ada", "steam") is True
    assert store.verify("ada", "wrong") is False
    assert store.verify("nobody", "steam") is False
    sid1, sid2 = store.new_session_id("ada"), store.new_session_id("ada")
    assert sid1 != sid2 and len(sid1) == 64
    # reset rotates the salt
    old_salt = row["salt"]
    store.ensure_user("ada", "new-pass")
    assert store.verify("ada", "new-pass") is True
    assert store.verify("ada", "steam") is False
    assert store.users["ada"]["salt"] != old_salt
    # file round-trip
    store2 = AuthStore(tmp_path / "users.json")
    assert store2.verify("ada", "new-pass") is True


# ----------------------------------------------------------------- demo ----

def test_demo_headless_subprocess_prints_the_win():
    proc = subprocess.run(
        [sys.executable, "-m", "server.server", "--demo", "--tick-ms", "25", "--ticks", "30"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=180,
    )
    assert proc.returncode == 0, f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
    assert "THE CROWN FILLS" in proc.stdout
    assert "WIN at tick" in proc.stdout
    assert "tick  30:" in proc.stdout


def test_graceful_stop_closes_the_port_and_flushes_the_log(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        await c.do_hello("ada", "steam")
        await srv.pump_once()
        await c.recv()
        c.close()
        await srv.stop()
        assert (tmp_path / "world_log.jsonl").read_text(encoding="utf-8").count("\n") >= 1
        with pytest.raises((ConnectionRefusedError, OSError)):
            await asyncio.wait_for(
                Client.connect("127.0.0.1", srv.bound_port), timeout=2.0
            )

    asyncio.run(scenario())
