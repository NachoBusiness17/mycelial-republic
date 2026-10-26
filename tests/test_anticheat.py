"""anti-cheat v1 tests (LW7, S20's design, 2026-09-30).

Every test is a law from the lane brief:
  - RATE_CAP: per-sid, per-tick staged-action budget of 1. A second
    action in the same tick rejects RATE_CAP at receipt and NEVER
    stages; the FIRST action of every tick is always legal (the budget
    resets when the tick rolls); budgets are per-sid (two clients each
    get one); a world-rejected action (DRY_POOL) does not spend the
    budget.
  - STALE_NONCE: per-session monotonic action ids. Replayed ids reject
    STALE_NONCE (a taped session cannot re-earn: the whole tape
    replays to nothing); ids burn at receipt, even when the action then
    fails world validation; a session that has used 'n' can never go
    nonce-less again; a malformed id (bool/str/float) rejects and does
    not bind.
  - The GWAP tag-dispute stub: a disputed tag routes through the
    agreement engine (score 0.0, verdict DISPUTE, cop report owed)
    while the tag itself still applies; undisputed tags and disputed
    non-tag verbs do not route.

The wire tests drive a REAL in-process TCP server on an ephemeral port,
manual ticks (tick_interval=None), exactly like tests/test_server_v0.py.
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.auth import AuthStore  # noqa: E402
from server.protocol import REJECT_CODES  # noqa: E402
from server.protocol_table import (  # noqa: E402
    ANTICHEAT_DIGEST,
    ANTICHEAT_TABLE,
    DEFAULT_TABLE,
    NO_NONCE,
    PROTOCOL_DIGEST,
    ReceiptGate,
)
from server.server import Client, WorldServer  # noqa: E402

_ABSENT = object()


async def _start_server(tmp_path: Path) -> WorldServer:
    auth = AuthStore(tmp_path / "users.json")
    auth.ensure_user("ada", "steam")
    auth.ensure_user("ben", "fish")
    srv = WorldServer(
        port=0, tick_interval=None, auth=auth,
        log_path=tmp_path / "world_log.jsonl",
    )
    return await srv.start()


async def _act(client: Client, sid: str, verb: str, target: str,
               n: Any = _ABSENT, dispute: Any = _ABSENT) -> dict:
    """One action over the real wire; the very next line is its reply."""
    msg: dict[str, Any] = {"op": "action", "sid": sid, "verb": verb, "target": target}
    if n is not _ABSENT:
        msg["n"] = n
    if dispute is not _ABSENT:
        msg["dispute"] = dispute
    await client.send(msg)
    return await client.recv()


async def _hello(client: Client, user: str) -> str:
    return (await client.do_hello(user, "steam" if user == "ada" else "fish"))["sid"]


# ------------------------------------------------------------ the contract ----

def test_anticheat_table_is_a_new_contract_version():
    # the two codes are in the closed anticheat vocabulary...
    assert ANTICHEAT_TABLE.reject_codes == DEFAULT_TABLE.reject_codes + (
        "RATE_CAP", "STALE_NONCE")
    # ...and the bound v0 surface (protocol.REJECT_CODES) did not move
    assert "RATE_CAP" not in REJECT_CODES and "STALE_NONCE" not in REJECT_CODES
    # rows are the DEFAULT rows: receipt laws own no verb
    assert ANTICHEAT_TABLE.rows == DEFAULT_TABLE.rows
    assert ANTICHEAT_TABLE.verbs == DEFAULT_TABLE.verbs
    # a NEW contract version, digest-pinned, DEFAULT byte-identical
    assert ANTICHEAT_DIGEST != PROTOCOL_DIGEST
    assert len(ANTICHEAT_DIGEST) == 64
    int(ANTICHEAT_DIGEST, 16)


def test_receipt_gate_unit_laws():
    g = ReceiptGate()
    # nonce: first id binds and burns; replay, lower, and equal reject
    assert g.admit_nonce("s1", 5) is None
    assert g.nonce_hwm("s1") == 5
    assert g.admit_nonce("s1", 5) == "STALE_NONCE"
    assert g.admit_nonce("s1", 4) == "STALE_NONCE"
    # a bound session cannot unbind (the tape-stripping trick)
    assert g.admit_nonce("s1", NO_NONCE) == "STALE_NONCE"
    # type law: bools are verdicts, strings and floats are not ids
    assert g.admit_nonce("s1", True) == "STALE_NONCE"
    assert g.admit_nonce("s1", "6") == "STALE_NONCE"
    assert g.admit_nonce("s1", 6.0) == "STALE_NONCE"
    assert g.admit_nonce("s1", 6) is None and g.nonce_hwm("s1") == 6
    # an unbound session stays legal without 'n' (v0 legacy wire)
    assert g.admit_nonce("s2", NO_NONCE) is None
    # cap: read-only until commit; spent per tick bucket; per sid
    assert g.admit_cap("s1", 1) is None
    g.commit("s1", 1)
    assert g.staged_tick("s1") == 1
    assert g.admit_cap("s1", 1) == "RATE_CAP"
    assert g.admit_cap("s1", 2) is None          # the tick rolled
    assert g.admit_cap("s2", 1) is None          # budgets are per sid


# ------------------------------------------------------ RATE_CAP (the wire) ----

def test_rate_cap_fires_on_second_action_in_tick(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        assert (await _act(c, sid, "tag", "hollow"))["op"] == "ack"
        # the second action in the SAME tick: rejected at receipt, with
        # the same reject shape every world reject carries
        r = await _act(c, sid, "tag", "hollow")
        assert r == {"op": "reject", "why": "RATE_CAP",
                     "verb": "tag", "target": "hollow"}
        assert srv.stats()["actions_staged"] == 1
        assert srv.anticheat_rejects["RATE_CAP"] == 1
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_rate_cap_never_stages(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        await _act(c, sid, "tag", "hollow")
        await _act(c, sid, "tag", "hollow")   # RATE_CAP, never staged
        await srv.pump_once()
        t = await c.recv()
        # exactly one tag applied: the world never saw the second one
        assert t["events"].count("ada tags a fish at hollow (score 1).") == 1
        assert srv.world.scores == {"ada": 1}
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_first_action_per_tick_law(tmp_path):
    """Every tick's FIRST action is legal; the cap resets when the tick
    rolls; the second action of the new tick rejects again."""
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        for tick in (1, 2, 3):
            assert (await _act(c, sid, "tag", "hollow"))["op"] == "ack", tick
            assert (await _act(c, sid, "tag", "hollow"))["why"] == "RATE_CAP"
            await srv.pump_once()
            t = await c.recv()
            assert t["n"] == tick
        assert srv.world.scores == {"ada": 3}   # one tag per tick, three ticks
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_cap_budgets_are_per_sid(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c1 = await Client.connect("127.0.0.1", srv.bound_port)
        c2 = await Client.connect("127.0.0.1", srv.bound_port)
        sid1, sid2 = await _hello(c1, "ada"), await _hello(c2, "ben")
        # both clients act in the SAME tick window: both ack
        assert (await _act(c1, sid1, "tag", "hollow"))["op"] == "ack"
        assert (await _act(c2, sid2, "tag", "hollow"))["op"] == "ack"
        # and each sid's second action is capped by its OWN budget
        assert (await _act(c1, sid1, "tag", "hollow"))["why"] == "RATE_CAP"
        assert (await _act(c2, sid2, "tag", "hollow"))["why"] == "RATE_CAP"
        c1.close()
        c2.close()
        await srv.stop()

    asyncio.run(scenario())


def test_world_reject_does_not_spend_the_budget(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        # crown starts dry: DRY_POOL, never staged, budget untouched
        assert (await _act(c, sid, "tag", "crown"))["why"] == "DRY_POOL"
        # so the first STAGED action of this tick is still legal
        assert (await _act(c, sid, "tag", "hollow"))["op"] == "ack"
        assert (await _act(c, sid, "tag", "hollow"))["why"] == "RATE_CAP"
        c.close()
        await srv.stop()

    asyncio.run(scenario())


# --------------------------------------------------- STALE_NONCE (the wire) ----

def test_nonce_replay_rejected(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        assert (await _act(c, sid, "tag", "hollow", n=1))["op"] == "ack"
        # the exact replay of the taped line...
        assert (await _act(c, sid, "tag", "hollow", n=1))["why"] == "STALE_NONCE"
        # ...and a lower id, and an equal one on another verb
        assert (await _act(c, sid, "tag", "hollow", n=0))["why"] == "STALE_NONCE"
        assert (await _act(c, sid, "boil", "spring", n=1))["why"] == "STALE_NONCE"
        # monotonic ids keep flowing (next tick: the budget has rolled,
        # and the replay flood above never staged so it never spent it)
        await srv.pump_once()
        await c.recv()
        assert (await _act(c, sid, "tag", "hollow", n=2))["op"] == "ack"
        assert srv.gate.nonce_hwm(sid) == 2
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_tape_cannot_re_earn(tmp_path):
    """The S20 law: tapes verify (the world log chains them) but cannot
    re-earn. Replaying a recorded session against itself stages nothing
    and the score does not move."""
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        tape = [
            {"op": "action", "sid": sid, "verb": "tag", "target": "hollow", "n": 1},
            {"op": "action", "sid": sid, "verb": "tag", "target": "hollow", "n": 2},
            {"op": "action", "sid": sid, "verb": "boil", "target": "spring", "n": 3},
        ]
        for msg in tape:                       # the original session
            await c.send(msg)
            assert (await c.recv())["op"] == "ack"
            await srv.pump_once()
            await c.recv()
        assert srv.world.scores == {"ada": 2}
        for msg in tape:                       # the replay, verbatim
            await c.send(msg)
            assert (await c.recv())["why"] == "STALE_NONCE"
        await srv.pump_once()
        assert srv.world.scores == {"ada": 2}   # nothing re-earned
        assert srv.anticheat_rejects["STALE_NONCE"] == 3
        assert srv.world.verify_log() is True   # the tape itself still verifies
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_nonce_burns_at_receipt_even_on_world_reject(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        # DRY_POOL with n=1: the world refuses it, but the id was RECEIVED
        assert (await _act(c, sid, "tag", "crown", n=1))["why"] == "DRY_POOL"
        # so replaying that id on a legal target is still stale
        assert (await _act(c, sid, "tag", "hollow", n=1))["why"] == "STALE_NONCE"
        assert (await _act(c, sid, "tag", "hollow", n=2))["op"] == "ack"
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_malformed_nonce_rejects_and_does_not_bind(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        assert (await _act(c, sid, "tag", "hollow", n=True))["why"] == "STALE_NONCE"
        assert (await _act(c, sid, "tag", "hollow", n="5"))["why"] == "STALE_NONCE"
        assert (await _act(c, sid, "tag", "hollow", n=5.0))["why"] == "STALE_NONCE"
        assert srv.gate.nonce_hwm(sid) is None  # no malformed id ever bound
        # the session is still legacy-legal without 'n'
        assert (await _act(c, sid, "tag", "hollow"))["op"] == "ack"
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_legacy_nonceless_client_rides_the_cap(tmp_path):
    """The v0 wire keeps working nonce-less (existing clients, the demo
    before LW7) — but the spam law is verb- and nonce-agnostic: one
    action per sid per tick holds for legacy clients too."""
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ben")
        assert (await _act(c, sid, "boil", "spring"))["op"] == "ack"
        assert (await _act(c, sid, "boil", "spring"))["why"] == "RATE_CAP"
        await srv.pump_once()
        await c.recv()
        assert (await _act(c, sid, "boil", "spring"))["op"] == "ack"
        c.close()
        await srv.stop()

    asyncio.run(scenario())


# ------------------------------------------------------- GWAP dispute stub ----

def test_disputed_tag_routes_through_the_agreement_engine(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        ack = await _act(c, sid, "tag", "hollow", dispute=True)
        assert ack["op"] == "ack"
        # the stub routes through mag/gwap_payload: no cop report yet,
        # so the score is 0.0 and the ladder verdicts DISPUTE
        assert ack["gwap"]["verdict"] == "DISPUTE"
        assert ack["gwap"]["score"] == 0.0
        assert ack["gwap"]["scene"] == f"tag-dispute:{sid}:1"
        row = srv.tag_disputes[0]
        assert row["user"] == "ada" and row["target"] == "hollow"
        assert row["owed"] == "cop report (the independent side of the round)"
        # the dispute routes, it does not veto: the tag still applies
        await srv.pump_once()
        t = await c.recv()
        assert "ada tags a fish at hollow (score 1)." in t["events"]
        # an undisputed tag does not route
        assert (await _act(c, sid, "tag", "hollow"))["op"] == "ack"
        await srv.pump_once()
        await c.recv()
        assert len(srv.tag_disputes) == 1
        assert srv.stats()["tag_disputes"] == 1
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_dispute_routes_only_for_tags_that_stage(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        sid = await _hello(c, "ada")
        # a disputed tag at a dry pool: world-rejected, nothing to dispute
        assert (await _act(c, sid, "tag", "crown", dispute=True))["why"] == "DRY_POOL"
        # a disputed boil is not a tag dispute
        assert (await _act(c, sid, "boil", "spring", dispute=True))["op"] == "ack"
        assert srv.tag_disputes == []
        c.close()
        await srv.stop()

    asyncio.run(scenario())
