"""server: asyncio TCP world server (v0).

THE ESTATE'S OWN WORLD SERVER. Line-based JSON over TCP (server/protocol),
the Mountain world ticked at a fixed cadence (server/world), fan-out to
per-client queues, graceful shutdown.

Shape:
    WorldServer(tick_interval=0.8)     real cadence (the 800ms world law)
    WorldServer(tick_interval=None)    manual mode: tests/demo drive pump_once()

Per client: hello is answered directly (welcome + snapshot); every authed
client gets an asyncio.Queue of pre-encoded broadcast lines drained by its
own writer task. Broadcasts are encoded ONCE per tick so every client
receives the same bytes.

B4 (2026-09-30): SRP6 auth is wired beside hello — srp_register /
srp_challenge / srp_proof ops (frozen rows in server/protocol_table.py,
math in server/auth_srp6.py, ported from the realmd-proven
tools/realmd_client). hello remains as the flag-gated plaintext fallback
(allow_plaintext_hello / --no-plaintext-hello) until SRP6 is the standing
default.

B15 (2026-09-30): minimal multi-room. The server hosts a RoomBook
(server/rooms.py) -- one MountainWorld + its own tick pump + its peers per
room, keyed by short id. hello gains an optional "room" argument (default
"summit"; clients that never say a room are unchanged), actions route by
the sid's room, and an action may carry "room" naming it. A tick in room
A never reaches room B's peers; the innkeeper keeps memories per room.

R3 (2026-09-30): post-auth frame MACs (the frontier's Q03 kill; spec
watch/inbox/frontier_asks/volley2/results/V2ASK1.md, math
server/frame_mac.py, wire law server/protocol.py's docstring). A
successful srp_proof arms the session's FrameMacState (HKDF keys from K,
A, B) and every later frame on that connection passes the MAC gate
BEFORE the op ladder (decode -> MAC -> ops). A bad tag, replayed/gapped
seq, malformed mac, or bare frame after the session went sticky (or
while require_frame_mac is set) is tamper: reject BAD_MAC, one
kind:mac_tamper row appended to the room world's hash chain (the
whisper precedent: a receipt-time audit row outside the tick), then
disconnect. Direct replies are sealed s2c; broadcast ticks stay bare
(encode-once law). The plaintext hello door carries no K and stays bare
either way -- migration, not breakage.

V7 (2026-09-30 receipt, wired 2026-10-01): key-bound identity. Two pre-auth
ops, identity_challenge / identity_proof (frozen rows in
server/protocol_table.py IDENTITY_AUTH_TABLE — the promoted home the V7
receipt assigned to the wiring lane; service in server/identity_binding.py):
the server fetches github.com/<user>.keys, mints a single-use exact-bytes
challenge, and the peer proves ownership of the private half with an sshsig
signature (ssh-keygen -Y sign/-Y verify, namespace core). A good proof
GRANTS a session (the srp_proof precedent: _grant_session with the binding
recorded) and binds the key to the sid: server_identities[sid] = {user,
fingerprint}, the welcome states auth:"identity" + the binding. The binding
policy flag mirrors allow_plaintext_hello: allow_unbound_hello=True (the
default) keeps the v0 door open; False refuses hello (BAD_AUTH, the v0
one-code law) from any connection that has not proved its key, so a sid can
only be held by a key-bound connection. Typed rejects ride the table's
closed vocabulary: BAD_PROOF / STALE_CHALLENGE (burn-at-receipt, the nonce
law) / NO_KEYS (fetch failed or login publishes nothing — LW2's signal).

Run:
    .venv/Scripts/python.exe -m server.server                       # serve :8800
    .venv/Scripts/python.exe -m server.server --demo                # 30 ticks, prints WIN
    .venv/Scripts/python.exe -m server.server --demo --tick-ms 80   # fast demo
"""
from __future__ import annotations

import argparse
import asyncio
import secrets
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import gwap_payload as gwap  # noqa: E402
from server.auth import AuthStore  # noqa: E402
from server.auth_srp6 import Srp6AuthService, SrpStore  # noqa: E402
from server import frame_mac  # noqa: E402
from server.frame_mac import FrameMacState  # noqa: E402
from server.protocol import (  # noqa: E402
    MAX_LINE,
    action,
    decode_line,
    encode,
    hello,
    reject,
    srp_challenge_ok,
    srp_registered,
    srp_welcome,
    welcome,
)
from server.identity_binding import IdentityBindService  # noqa: E402
from server.protocol_table import (  # noqa: E402
    IDENTITY_AUTH_DISPATCH,
    NO_NONCE,
    SRP6_AUTH_DISPATCH,
    ReceiptGate,
)
from server.verdict_feed import PRODUCTION_GPS_DB, VerdictFeed  # noqa: E402
from server.rooms import DEFAULT_ROOM_CAPACITY, GameRoom, RoomBook  # noqa: E402
from server.ws_door import WsDoor  # noqa: E402
from server.world import MountainWorld  # noqa: E402

DEFAULT_PORT = 8800
BOIL_ORDER = ("spring", "terrace", "gate1", "hollow")  # crown excluded: already won water
TAG_ORDER = ("spring", "terrace", "gate1", "hollow", "crown")


class WorldServer:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = DEFAULT_PORT,
        tick_interval: float | None = 0.8,
        auth: AuthStore | None = None,
        world: MountainWorld | None = None,
        log_path: Path | str | None = None,
        verdict_feed: VerdictFeed | None = None,
        srp_auth: Srp6AuthService | None = None,
        allow_plaintext_hello: bool = True,
        room_capacity: int = DEFAULT_ROOM_CAPACITY,
        require_frame_mac: bool = False,
        identity: IdentityBindService | None = None,
        allow_unbound_hello: bool = True,
        open_ws: bool = False,
        ws_port: int = 0,
    ) -> None:
        self.host = host
        self.port = port
        self.tick_interval = tick_interval
        self.auth = auth
        # B4 (2026-09-30): SRP6 as the account system. srp_auth is None only
        # in untouched v0 callers/tests; _serve wires a real Srp6AuthService.
        # allow_plaintext_hello is the v0 FALLBACK FLAG: True keeps the v0
        # plaintext hello door open (byte-identical v0 wire, the standing
        # no-regression law); False makes SRP6 the only way in. Flip the
        # default to False when SRP6 has soaked; the flag is the fallback.
        self.srp_auth = srp_auth
        self.allow_plaintext_hello = allow_plaintext_hello
        # R3 (2026-09-30): the frame-MAC migration flag. False (default)
        # keeps the migration window open -- an SRP6-authed client that
        # never sends "mac" fields stays legal, its session running at
        # integrity "none"; frames that DO carry a mac are verified and a
        # bad one is tamper regardless of the flag. True closes the bare
        # window: after srp_proof every frame must carry a valid MAC.
        # Flip the default when the MAC-bearing clients have soaked, the
        # same law as allow_plaintext_hello's sunset.
        self.require_frame_mac = require_frame_mac
        # B15 (2026-09-30): rooms replace the single world. The default room
        # "summit" is the backward-compat world (its log lands at exactly the
        # log_path given; clients that never say a room land there), every
        # other room is born at the first hello that names it. self.world
        # stays as the default room's world so every existing caller and
        # test keeps its meaning.
        self.rooms = RoomBook(
            log_path=log_path, world=world, capacity=room_capacity,
            tick_interval=tick_interval,
        )
        self.world = self.rooms.default_room.world
        # X11's debt (Z1 weld): dormant by default; _serve wires the
        # production feed, tests may inject one, the demo runs without.
        # The weld binds to the DEFAULT room's pump (rooms.py on_tick):
        # the meter rides the standing world, side rooms stay unmetered v0.
        self.verdict_feed = verdict_feed
        if verdict_feed is not None:
            self.rooms.default_room.on_tick = verdict_feed.feed_tick
        self._server: asyncio.AbstractServer | None = None
        self._peers: dict[int, dict[str, Any]] = {}
        self._peer_seq = 0
        self.bound_port: int | None = None
        self.actions_staged = 0
        # LW7 (S20's design, 2026-09-30): anti-cheat at receipt. The LAW
        # lives in protocol_table.ReceiptGate; THIS file is the enforcement
        # point — nonce law, world validation, rate cap, stage — so a
        # RATE_CAP or STALE_NONCE reject lands at receipt and never stages.
        self.gate = ReceiptGate()
        self.anticheat_rejects = {"RATE_CAP": 0, "STALE_NONCE": 0}
        # B4: SRP6 handshake counters (the receipt layer, same honesty as
        # anticheat_rejects: counts are filed, not estimated)
        self.srp_rejects = {"BAD_PROOF": 0, "STALE_CHALLENGE": 0}
        self.srp_sessions = 0
        # R3: frame-MAC counters (the same receipt honesty): sessions that
        # went MAC-sticky, and tamper events (each also a chain row)
        self.mac_sessions = 0
        self.mac_tampers = 0
        # V7 (2026-09-30): key-bound identity. identity is None only in
        # untouched v0 callers/tests; _serve wires a real IdentityBindService
        # (tests inject one with a fake fetcher — never the network).
        # allow_unbound_hello is the BINDING POLICY FLAG, shape mirroring
        # allow_plaintext_hello (the V7 receipt's "flag shape mirrors
        # allow_plaintext_hello"): True (default) keeps the v0 plaintext
        # hello door open for unbound connections (the standing no-regression
        # law); False refuses hello from any connection that has not proved
        # its GitHub-published key, so every sid is key-bound. Flip the
        # default when identity has soaked — the same sunset law.
        self.identity = identity
        self.allow_unbound_hello = allow_unbound_hello
        # The binding record per granted sid (the session row): sid ->
        # {"user", "fingerprint"} of the GitHub login whose key the
        # connection proved. This is the estate's answer surface for "which
        # key holds sid X" — the LW2 stop made queryable.
        self.session_identities: dict[str, dict[str, Any]] = {}
        # V7 receipt-layer counters (the same honesty as anticheat_rejects
        # and srp_rejects: counts are filed, not estimated)
        self.identity_rejects = {"BAD_PROOF": 0, "STALE_CHALLENGE": 0,
                                 "NO_KEYS": 0}
        self.identity_sessions = 0
        # Disputed tags routed through the mag/gwap_payload agreement
        # engine (stub call site; the cop report is owed — see
        # _route_tag_dispute).
        self.tag_disputes: list[dict[str, Any]] = []
        # The ws-door mount (2026-10-06, receipt
        # watch/inbox/mates_leave_protocol/receipts/20261006_locksmith.md):
        # ws_door.py shipped 2026-09-29 with a mount recipe nobody applied
        # (zero production importers for a week). Default-off (open_ws
        # False) keeps every existing caller and test byte-identical, the
        # allow_plaintext_hello migration-flag shape; start() opens the
        # door on the DEFAULT room only (side rooms stay TCP-only v0, the
        # Z1 weld precedent). ws_port 0 = ephemeral; 8766 is never
        # touched (mud_relay's port, ws_door's own port law).
        self.open_ws = open_ws
        self.ws_port = ws_port
        self.ws_door: WsDoor | None = None

    # ------------------------------------------------------------ cycle ----
    async def start(self) -> "WorldServer":
        self._server = await asyncio.start_server(
            self._handle_client, self.host, self.port, limit=MAX_LINE
        )
        self.bound_port = self._server.sockets[0].getsockname()[1]
        # B15: each room pumps itself (the default room now, rooms born at a
        # later hello ensure their own pump on join_peer). Manual mode
        # (tick_interval None) starts no pump -- tests drive pump_once().
        for room in self.rooms:
            room.ensure_pump()
        if self.open_ws:
            # The ws-door mount (2026-10-06): one spectator door on the
            # standing world. on_broadcast receives the SAME encoded line
            # object broadcast() queued to the TCP peers (encode-once).
            self.ws_door = await WsDoor().start(self.host, self.ws_port)
            self.rooms.default_room.on_broadcast = self.ws_door.publish
        return self

    async def pump_once(self) -> dict[str, Any]:
        """One beat of every live room: each room ticks its OWN world and
        broadcasts to its OWN peers (cross-room isolation is structural --
        server/rooms.py GameRoom.pump_once). Returns the DEFAULT room's
        payload, the v0 contract existing callers read. A single room's
        manual drive is self.rooms[<id>].pump_once()."""
        default = self.rooms.default_room
        for room in self.rooms:
            if room is not default:
                room.pump_once()
        return default.pump_once()

    async def stop(self) -> None:
        for peer in list(self._peers.values()):
            if peer["queue"] is not None:
                peer["queue"].put_nowait(None)
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
        await self.rooms.stop_all()
        if self.ws_door is not None:
            await self.ws_door.stop()
            self.ws_door = None

    def stats(self) -> dict[str, int]:
        return {
            "clients": sum(1 for p in self._peers.values() if p["queue"] is not None),
            # B15: ticks/rooms are the default room's clock and the book's
            # size (the v0 "ticks" meaning is unchanged: the standing world)
            "ticks": self.rooms.default_room.world.graph.tick_count,
            "rooms": len(self.rooms),
            "actions_staged": self.actions_staged,
            "rate_capped": self.anticheat_rejects["RATE_CAP"],
            "stale_nonce": self.anticheat_rejects["STALE_NONCE"],
            "srp_sessions": self.srp_sessions,
            "bad_proof": self.srp_rejects["BAD_PROOF"],
            "stale_challenge": self.srp_rejects["STALE_CHALLENGE"],
            "mac_sessions": self.mac_sessions,
            "mac_tampers": self.mac_tampers,
            "tag_disputes": len(self.tag_disputes),
            "identity_sessions": self.identity_sessions,
            "identity_bound_sids": len(self.session_identities),
            "identity_bad_proof": self.identity_rejects["BAD_PROOF"],
            "identity_stale_challenge": self.identity_rejects["STALE_CHALLENGE"],
            "identity_no_keys": self.identity_rejects["NO_KEYS"],
            # The ws-door mount (2026-10-06): seated spectators, counts
            # filed not estimated (the same honesty as the counters above).
            "ws_clients": (len(self.ws_door.room.members)
                           if self.ws_door is not None else 0),
        }

    # ---------------------------------------------------------- clients ----
    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        self._peer_seq += 1
        peer: dict[str, Any] = {
            "id": self._peer_seq,
            "reader": reader,
            "writer": writer,
            "queue": None,
            "writer_task": None,
            "user": None,
            "sid": None,
            "room": None,  # B15: the GameRoom this connection is seated in
            # R3: the armed frame-MAC state (None until srp_proof succeeds
            # on this connection) + the handshake publics stash the keys
            # derive from (srp_a_wire/srp_b_wire, set at srp_challenge)
            "mac_state": None,
            "srp_a_wire": None,
            "srp_b_wire": None,
            # V7: the connection's verified key binding (None until an
            # identity_proof succeeds here) — {"user", "fingerprint"} of the
            # GitHub login whose key this connection proved
            "identity": None,
        }
        self._peers[peer["id"]] = peer
        try:
            while True:
                line = await reader.readline()
                if not line:
                    break
                try:
                    msg = decode_line(line)
                except ValueError:
                    await self._reply(peer, reject("BAD_JSON"))
                    continue
                # R3: the MAC gate, BEFORE any op runs (verify before
                # processing -- a tampered frame never reaches the nonce
                # gate or an op handler). Only armed sessions (K exists)
                # pass through here; pre-auth frames and the plaintext
                # hello door are below the law by construction.
                state = peer["mac_state"]
                if state is not None:
                    was_sticky = state.mac_mode
                    why = state.admit(msg, require=self.require_frame_mac)
                    if why is not None:
                        await self._on_mac_tamper(peer, why)
                        break  # tamper = disconnect (never resync)
                    if not was_sticky and state.mac_mode:
                        self.mac_sessions += 1  # the session went MAC-sticky
                op = msg.get("op")
                if op == "hello":
                    await self._on_hello(peer, msg)
                elif op in ("srp_register", "srp_challenge", "srp_proof"):
                    # B4: the SRP6 handshake verbs. Gated through the frozen
                    # table rows BEFORE any handler runs (the ordering law);
                    # handler_ran is provably False on every refusal.
                    gated = self._gate_srp(peer, op)
                    if gated is not None:
                        await self._reply(peer, gated)
                    elif op == "srp_register":
                        await self._on_srp_register(peer, msg)
                    elif op == "srp_challenge":
                        await self._on_srp_challenge(peer, msg)
                    else:
                        await self._on_srp_proof(peer, msg)
                elif op in ("identity_challenge", "identity_proof"):
                    # V7: the identity-binding verbs. Gated through the
                    # promoted frozen rows BEFORE any handler runs (the
                    # ordering law, the auth_srp_* precedent);
                    # handler_ran is provably False on every refusal.
                    gated = self._gate_identity(peer, op)
                    if gated is not None:
                        await self._reply(peer, gated)
                    elif op == "identity_challenge":
                        await self._on_identity_challenge(peer, msg)
                    else:
                        await self._on_identity_proof(peer, msg)
                elif op == "action":
                    reply = self._admit_action(msg)
                    if reply["op"] == "ack":
                        self.actions_staged += 1
                    await self._reply(peer, reply)
                else:
                    await self._reply(peer, reject("UNKNOWN_OP"))
        except (ConnectionResetError, asyncio.IncompleteReadError, OSError):
            pass
        finally:
            await self._drop_peer(peer)

    async def _on_hello(self, peer: dict[str, Any], msg: dict[str, Any]) -> None:
        # B4: the v0 plaintext door is now a FALLBACK FLAG. allow_plaintext_hello
        # is True by default (the no-regression law: the v0 wire stays
        # byte-identical until SRP6 has soaked); False rejects BAD_AUTH and
        # SRP6 is the only way in.
        if not self.allow_plaintext_hello:
            await self._reply(peer, reject("BAD_AUTH"))
            return
        # V7 binding policy (the receipt's grant-time flag, shape mirroring
        # allow_plaintext_hello): with allow_unbound_hello False, hello is
        # refused unless THIS connection proved its GitHub-published key —
        # "any connection can hold a sid" stops being true. BAD_AUTH, the v0
        # hello one-code law (the plaintext-door refusal above uses the same
        # code); a bound connection's hello grants below with the binding on
        # the session row.
        if not self.allow_unbound_hello and peer.get("identity") is None:
            await self._reply(peer, reject("BAD_AUTH"))
            return
        user = str(msg.get("user", ""))
        password = str(msg.get("pass", ""))
        if self.auth is None or not self.auth.verify(user, password):
            await self._reply(peer, reject("BAD_AUTH"))
            return
        # B15: the join surface's room argument. No "room" key = the default
        # room, byte-identical v0. The capacity law refuses BEFORE a sid is
        # issued (honest refusal: nothing granted, the peer keeps its seat).
        room, why = self._resolve_room(msg)
        if why is not None:
            await self._reply(peer, reject(why))
            return
        if room.is_full(peer["id"]):
            await self._reply(peer, reject("ROOM_FULL", room=room.id))
            return
        sid = self.auth.new_session_id(user)
        # V7: a bound connection's hello carries its verified key binding
        # onto the granted session (the key is bound to the sid — the
        # unbound default path is byte-identical v0: identity=None).
        await self._reply(peer, self._grant_session(
            peer, user, sid, room=room, identity=peer.get("identity")))

    def _resolve_room(
        self, msg: dict[str, Any]
    ) -> tuple[GameRoom | None, str | None]:
        """(room, why): the room a hello asks for. Absent/None -> the default
        room; malformed id -> BAD_ROOM; otherwise born-at-hello
        get_or_create. This is the ONLY creation path -- an action naming a
        room no hello ever made refuses UNKNOWN_ROOM."""
        if "room" not in msg or msg["room"] is None:
            return self.rooms.default_room, None
        if not RoomBook.valid_id(msg["room"]):
            return None, "BAD_ROOM"
        return self.rooms.get_or_create(msg["room"]), None

    def _grant_session(
        self, peer: dict[str, Any], user: str, sid: str,
        room: GameRoom | None = None,
        identity: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """The one place a session is granted: register the sid with the
        room's world, bind the peer to that room, start its broadcast queue
        + writer, and hand back the welcome. Both doors (v0 hello, B4 SRP6
        proof) walk through here so an authed peer is one shape however it
        authed. room=None (the B4 SRP6 door, v0) lands in the default room;
        the hello door passes the room it resolved + capacity-checked.
        V7: identity is the key binding a verified proof left on the
        connection — it is recorded on the session row
        (self.session_identities[sid]) and stated in the welcome
        (auth:"identity" + the binding), so the sid is answerable to its
        key. None (the unbound paths) keeps the welcome byte-identical v0."""
        room = room if room is not None else self.rooms.default_room
        room.world.register_session(sid, user)
        if identity is not None:
            self.session_identities[sid] = dict(identity)
        peer["user"], peer["sid"] = user, sid
        old = peer.get("room")
        if old is not None and old is not room:
            old.drop_peer(peer["id"])  # one connection, one room at a time
        if peer.get("room") is not room:
            room.join_peer(peer)
        if peer["queue"] is None:
            peer["queue"] = asyncio.Queue()
            peer["writer_task"] = asyncio.create_task(self._writer_loop(peer))
        reply = welcome(sid, room.world.snapshot())
        reply["room"] = room.id  # B15: the client's room, always stated
        if identity is not None:
            reply["auth"] = "identity"
            reply["identity"] = dict(identity)
        return reply

    # ------------------------------------------------------- B4: SRP6 ----
    def _gate_srp(self, peer: dict[str, Any], verb: str) -> dict[str, Any] | None:
        """Gate before verb (the ordering law) on the frozen SRP6_AUTH_TABLE
        rows. State resolves like state_for_sid: a peer holding a granted sid
        is AUTHED, anything else CONNECTED (the auth verbs' floor, so the
        gate's reject slot is a reserved never-fires slot — the NOT_YOUR_TURN
        precedent; the real laws BAD_PROOF/STALE_CHALLENGE fire in the
        service layer, the LW6/LW7 vocabulary law)."""
        state = "AUTHED" if peer.get("sid") is not None else "CONNECTED"
        out = SRP6_AUTH_DISPATCH.ask(verb, state)
        if out["ok"]:
            return None
        return reject(out["reason"], verb=verb)

    async def _on_srp_register(self, peer: dict[str, Any], msg: dict[str, Any]) -> None:
        if self.srp_auth is None:
            await self._reply(peer, reject("BAD_AUTH"))
            return
        user = str(msg.get("user", ""))
        password = str(msg.get("pass", ""))
        try:
            self.srp_auth.register(user, password)
        except (ValueError, UnicodeEncodeError):
            # malformed identity (empty, colon-bearing, non-ascii): one code,
            # no enumeration, exactly the v0 hello law
            await self._reply(peer, reject("BAD_AUTH"))
            return
        await self._reply(peer, srp_registered(user))

    async def _on_srp_challenge(self, peer: dict[str, Any], msg: dict[str, Any]) -> None:
        if self.srp_auth is None:
            await self._reply(peer, reject("BAD_AUTH"))
            return
        try:
            out = self.srp_auth.begin_challenge(
                peer["id"], str(msg.get("user", "")), msg.get("a"))
        except (ValueError, UnicodeEncodeError):
            await self._reply(peer, reject("BAD_AUTH"))
            return
        # R3: stash this handshake's publics (wire hex). begin_challenge
        # has validated A and minted B, and a provable proof can only
        # come from this same pending handshake, so at proof success the
        # stash is exactly the (A, B) K was born from.
        peer["srp_a_wire"] = str(msg["a"])
        peer["srp_b_wire"] = out["b"]
        await self._reply(peer, srp_challenge_ok(out["user"], out["salt"], out["b"]))

    async def _on_srp_proof(self, peer: dict[str, Any], msg: dict[str, Any]) -> None:
        if self.srp_auth is None:
            await self._reply(peer, reject("BAD_AUTH"))
            return
        # B15 capacity law, paid by this door too: the seat is refused BEFORE
        # the proof is consumed (honest refusal: nothing granted, nothing
        # burned — the challenge stays usable if a seat frees up). The SRP6
        # door lands in the DEFAULT room (room selection on this door is the
        # owed follow-up once rooms + SRP6 have both soaked).
        room = self.rooms.default_room
        if room.is_full(peer["id"]):
            await self._reply(peer, reject("ROOM_FULL", room=room.id))
            return
        # the pending handshake BURNS inside verify_proof (nonce law): a
        # replayed M1 — success-replay or failure-replay — can never re-earn
        user = str(msg.get("user", ""))
        out = self.srp_auth.verify_proof(peer["id"], user, msg.get("m1"))
        if not out["ok"]:
            self.srp_rejects[out["why"]] += 1
            await self._reply(peer, reject(out["why"]))
            return
        self.srp_sessions += 1
        # R3: arm the frame-MAC keys. K exists only on this door, so MAC
        # protection is SRP6-only by construction; the stashed (A, B) are
        # the handshake K was born from (the challenge handler's invariant:
        # verify_proof success implies a begin_challenge on this peer).
        # A re-login replaces the state wholesale: new handshake, new K,
        # both seq counters reborn at 0 with the fresh welcome.
        peer["mac_state"] = FrameMacState(frame_mac.derive_from_wire(
            out["session_key"], peer.pop("srp_a_wire"), peer.pop("srp_b_wire")))
        # register the roster under the UPPER identity (the mangos law the
        # math already follows; "ada" and "ADA" are one account)
        granted = self._grant_session(peer, user.upper(), out["sid"])
        reply = srp_welcome(out["sid"], out["m2"], granted["world"])
        reply["room"] = granted["room"]  # B15: one welcome shape, both doors
        await self._reply(peer, reply)

    # ------------------------------------------------------- V7: identity ----
    def _gate_identity(self, peer: dict[str, Any], verb: str) -> dict[str, Any] | None:
        """Gate before verb (the ordering law) on the promoted IDENTITY_AUTH
        rows. State resolves exactly like _gate_srp: a peer holding a granted
        sid is AUTHED, anything else CONNECTED — the identity verbs' floor is
        CONNECTED (pre-auth by definition, the B4 precedent), so the gate's
        reject slot is a reserved never-fires slot; the dialect's real laws
        (BAD_PROOF / STALE_CHALLENGE / NO_KEYS) fire in the service layer,
        the LW6/LW7 vocabulary law. An AUTHED peer may re-run the binding
        handshake (re-bind is legal, the module's gate test)."""
        state = "AUTHED" if peer.get("sid") is not None else "CONNECTED"
        out = IDENTITY_AUTH_DISPATCH.ask(verb, state)
        if out["ok"]:
            return None
        return reject(out["reason"], verb=verb)

    async def _on_identity_challenge(self, peer: dict[str, Any],
                                     msg: dict[str, Any]) -> None:
        """Step 1 (the receipt's Adam flow): fetch github.com/<user>.keys,
        mint the single-use exact-bytes challenge for THIS connection.
        Typed refusals: BAD_AUTH (login grammar — the injection law fires
        before any fetch) and NO_KEYS (fetch failed or the login publishes
        nothing; the detail rides the wire because NO_KEYS is the
        operator's wrong-username signal, not a leak — the receipt's law)."""
        if self.identity is None:
            await self._reply(peer, reject("BAD_AUTH"))
            return
        out = self.identity.mint_challenge(peer["id"], str(msg.get("user", "")))
        if not out["ok"]:
            if out["why"] == "NO_KEYS":
                self.identity_rejects["NO_KEYS"] += 1
                await self._reply(peer, reject("NO_KEYS", detail=out.get("detail")))
            else:
                await self._reply(peer, reject("BAD_AUTH"))
            return
        await self._reply(peer, {
            "op": "identity_challenge",
            "user": out["user"],
            "challenge": out["challenge"],
            "nonce": out["nonce"],
            "expires": out["expires"],
        })

    async def _on_identity_proof(self, peer: dict[str, Any],
                                 msg: dict[str, Any]) -> None:
        """Step 2: consume the pending challenge (BURNS AT RECEIPT inside
        verify_proof — the srp nonce law: a replayed tape finds
        STALE_CHALLENGE) and verify the sshsig armor over the exact challenge
        bytes. On success the receipt's owed wiring: RECORD the binding on
        the connection (peer["identity"]), GRANT a session through
        _grant_session with the binding on the session row (the key is bound
        to the sid), and count it. The capacity law is paid BEFORE the proof
        is consumed (the srp_proof precedent: honest refusal — nothing
        granted, nothing burned)."""
        if self.identity is None:
            await self._reply(peer, reject("BAD_AUTH"))
            return
        room = self.rooms.default_room
        if room.is_full(peer["id"]):
            await self._reply(peer, reject("ROOM_FULL", room=room.id))
            return
        user = str(msg.get("user", ""))
        out = self.identity.verify_proof(peer["id"], user, msg.get("sig"))
        if not out["ok"]:
            self.identity_rejects[out["why"]] += 1
            await self._reply(peer, reject(out["why"]))
            return
        binding = {"user": out["user"], "fingerprint": out["fingerprint"]}
        peer["identity"] = binding
        self.identity_sessions += 1
        # sid mint: real entropy (the V7 receipt's named deviation — secrets
        # for auth material). SRP6 derives its sid from K, the handshake's
        # shared secret; identity binding has no shared secret (the sshsig
        # IS the proof), so entropy is the sid's unforgeable source. Shape is
        # the v0 64-hex grammar; world.register_session is agnostic.
        sid = secrets.token_hex(32)
        granted = self._grant_session(peer, out["user"], sid, identity=binding)
        await self._reply(peer, granted)

    # --------------------------------------------------- R3: frame MAC ----
    async def _on_mac_tamper(self, peer: dict[str, Any], why: str) -> None:
        """Tamper = disconnect + chain event. The row lands in the peer's
        room world's hash chain (the whisper precedent: a receipt-time
        audit row outside the canonical tick), carries the session's
        integrity state (the spec's laundering fix: the chain records
        what it could and could not see), and then the caller breaks the
        read loop -- the connection dies in _drop_peer, never resync,
        never downgrade. No wall clock, no RNG in the row (the log
        determinism law)."""
        self.mac_tampers += 1
        state = peer.get("mac_state")
        room = peer.get("room") or self.rooms.default_room
        room.world._append_row({
            "kind": "mac_tamper",
            "tick": room.world.graph.tick_count,
            "user": peer.get("user"),
            "sid": peer.get("sid"),
            "peer": peer["id"],
            "code": why,
            "integrity": state.integrity if state is not None else "none",
        })
        await self._reply(peer, reject(why))

    def _room_for_action(self, msg: dict[str, Any]) -> tuple[GameRoom | None, dict[str, Any] | None]:
        """(room, reject): the room an action stages into. No "room" key ->
        the sid's own room (fallback default -- a sid no room issued meets
        the default world's UNKNOWN_SID, the v0 bytes unchanged). A named
        room must exist (born at hello) and must be the world that issued
        the sid; a sid from another room honestly meets that world's own
        UNKNOWN_SID."""
        if "room" not in msg or msg["room"] is None:
            room = self.rooms.room_of_sid(str(msg.get("sid", "")))
            return (room if room is not None else self.rooms.default_room), None
        if not RoomBook.valid_id(msg["room"]):
            return None, reject("BAD_ROOM")
        room = self.rooms.get(msg["room"])
        if room is None:
            return None, reject("UNKNOWN_ROOM")
        return room, None

    def _admit_action(self, msg: dict[str, Any]) -> dict[str, Any]:
        """The receipt ladder (LW7, S20's design): nonce law (the replay
        envelope — a passing id burns here), then world validation (the
        semantic rejects keep their codes: BAD_TEXT still beats the cap),
        then the rate cap (the spam envelope, spent only by an ack), then
        stage. A RATE_CAP or STALE_NONCE reject lands in this method and
        never reaches world.stage. B15: the ladder runs against the ROOM
        the action belongs to (sid's room, or a well-formed named room)."""
        sid = str(msg.get("sid", ""))
        verb = str(msg.get("verb", ""))
        target = str(msg.get("target", ""))
        room, room_reject = self._room_for_action(msg)
        if room_reject is not None:
            return room_reject
        nonce = msg["n"] if "n" in msg else NO_NONCE
        why = self.gate.admit_nonce(sid, nonce)
        if why is not None:
            self.anticheat_rejects[why] += 1
            return reject(why, verb=verb, target=target)
        ok, why = room.world.validate(sid, verb, target)
        if not ok:
            return {"op": "reject", "why": why, "verb": verb, "target": target}
        applies_at_tick = room.world.graph.tick_count + 1
        why = self.gate.admit_cap(sid, applies_at_tick)
        if why is not None:
            self.anticheat_rejects[why] += 1
            return reject(why, verb=verb, target=target)
        reply = room.world.stage(sid, verb, target)
        if reply["op"] == "ack":
            self.gate.commit(sid, applies_at_tick)
            if verb == "tag" and msg.get("dispute") is True:
                reply["gwap"] = self._route_tag_dispute(sid, reply)
        return reply

    def _route_tag_dispute(self, sid: str, ack: dict[str, Any]) -> dict[str, Any]:
        """The GWAP tag-dispute stub (LW7; S20's design: "tag disputes as
        GWAP rounds — agreement + collusion fingerprint server-side,
        feeding the owed judge queue"). The engine side is REAL: the
        tagger's claim becomes the intent side, agreement_score() scores
        it against the independent side, decide_verdict() runs the ladder
        (mag/gwap_payload). The cop report is OWED, so the independent
        side is empty, the score is 0.0, and the ladder verdicts DISPUTE —
        exactly the row a judge must look at. No ledger write and no
        fingerprint here: both need the independent author, which is the
        round machinery this stub is the call site for. The tag itself
        stands until judgment: a dispute routes, it does not veto.
        """
        user, target = ack["user"], ack["target"]
        # the cap guarantees one staged action per sid per tick, so the
        # scene id is unique without any counter state
        scene_id = f"tag-dispute:{sid}:{ack['applies_at_tick']}"
        intent_claims = [
            {"subject": user, "verb": "tagged", "object": f"fish at {target}"},
        ]
        score = gwap.agreement_score(intent_claims, [])
        verdict = gwap.decide_verdict(score)
        row = {
            "scene_id": scene_id,
            "sid": sid,
            "user": user,
            "target": target,
            "agreement_score": score,
            "verdict": verdict,
            "owed": "cop report (the independent side of the round)",
        }
        self.tag_disputes.append(row)
        return {"scene": scene_id, "verdict": verdict, "score": score}

    async def _writer_loop(self, peer: dict[str, Any]) -> None:
        queue: asyncio.Queue = peer["queue"]
        writer: asyncio.StreamWriter = peer["writer"]
        try:
            while True:
                line = await queue.get()
                if line is None:
                    return
                writer.write(line)
                await writer.drain()
        except (ConnectionResetError, OSError):
            return

    async def _reply(self, peer: dict[str, Any], msg: dict[str, Any]) -> None:
        # R3: direct replies on an armed session ride sealed s2c (the
        # client verifies with its k_s2c). Broadcast ticks bypass _reply
        # entirely (the encode-once law) and stay bare by design.
        state = peer.get("mac_state")
        if state is not None:
            msg = state.seal_reply(msg)
        peer["writer"].write(encode(msg))
        try:
            await peer["writer"].drain()
        except (ConnectionResetError, OSError):
            pass

    async def _drop_peer(self, peer: dict[str, Any]) -> None:
        self._peers.pop(peer["id"], None)
        # B4: the dead connection's pending SRP6 handshake dies with it
        # (single-use, keyed by connection — no orphan challenge outlives
        # its asker)
        if self.srp_auth is not None:
            self.srp_auth.drop(peer["id"])
        # V7: the same law for the pending identity challenge (the module's
        # drop): single-use, keyed by connection, dies with its asker
        if self.identity is not None:
            self.identity.drop(peer["id"])
        room = peer.get("room")
        if room is not None:
            room.drop_peer(peer["id"])  # B15: free the seat (may sleep the room)
        if peer["queue"] is not None:
            peer["queue"].put_nowait(None)
        task = peer["writer_task"]
        if task is not None:
            try:
                await asyncio.wait_for(task, timeout=2.0)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                task.cancel()
        peer["writer"].close()
        try:
            await peer["writer"].wait_closed()
        except (ConnectionResetError, OSError):
            pass


class Client:
    """Minimal test/demo client speaking the wire protocol."""

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

    @classmethod
    async def connect(cls, host: str, port: int, limit: int = MAX_LINE) -> "Client":
        reader, writer = await asyncio.open_connection(host, port, limit=limit)
        return cls(reader, writer)

    async def send(self, msg: dict[str, Any]) -> None:
        self.writer.write(encode(msg))
        await self.writer.drain()

    async def recv_raw(self) -> bytes:
        line = await self.reader.readline()
        if not line:
            raise ConnectionError("server closed the connection")
        return line

    async def recv(self) -> dict[str, Any]:
        return decode_line(await self.recv_raw())

    async def until(self, op: str) -> dict[str, Any]:
        """Receive until a message with this op arrives (others skipped)."""
        while True:
            msg = await self.recv()
            if msg.get("op") == op:
                return msg

    async def do_hello(
        self, user: str, password: str, room: str | None = None
    ) -> dict[str, Any]:
        msg = hello(user, password)
        if room is not None:
            msg["room"] = room  # B15: the join surface's room argument
        await self.send(msg)
        return await self.until("welcome")

    async def do_action(
        self, sid: str, verb: str, target: str, room: str | None = None
    ) -> dict[str, Any]:
        msg = action(sid, verb, target)
        if room is not None:
            msg["room"] = room
        await self.send(msg)
        return await self.until("ack")

    def close(self) -> None:
        self.writer.close()


# -------------------------------------------------------------- demo ----

def _pick_target(order: tuple[str, ...], mirror: dict[str, int]) -> str | None:
    """Deterministic policy: the wettest pool in a fixed preference order."""
    best, best_v = None, 0
    for name in order:
        v = int(mirror.get(name, 0))
        if v > best_v:
            best, best_v = name, v
    return best


async def _ask(client: Client, sid: str, verb: str, target: str, n: int) -> dict[str, Any]:
    """Send one action, return the reply. n is the per-session action id
    (LW7 STALE_NONCE law): the demo is the first nonce-bearing client, so
    every standing --demo run exercises the monotonic-id path. Safe here
    because the demo drives a manually-pumped world: no tick can
    interleave between ask and reply."""
    await client.send({"op": "action", "sid": sid, "verb": verb,
                       "target": target, "n": n})
    return await client.recv()


async def _demo(args: argparse.Namespace) -> int:
    tmp = Path(tempfile.mkdtemp(prefix="our_server_demo_"))
    users_file = tmp / "users.json"
    auth = AuthStore(users_file)
    auth.ensure_user("boiler", "steam")
    auth.ensure_user("tagger", "fish")
    # main() nulls args.log for --demo unless --log was passed explicitly,
    # so demo runs never append to the standing server log.
    log_path = Path(args.log) if args.log else tmp / "world_demo.jsonl"

    # tick_interval=None: the demo loop IS the cadence driver, so the wire
    # order (reply, reply, tick) is deterministic and the demo never races.
    server = WorldServer(
        host=args.host,
        port=args.port,
        tick_interval=None,
        auth=auth,
        log_path=log_path,
    )
    await server.start()
    print(f"demo world server on {args.host}:{server.bound_port} "
          f"(tick {args.tick_ms}ms, log {log_path})")

    boiler = await Client.connect(args.host, server.bound_port)
    tagger = await Client.connect(args.host, server.bound_port)
    w_boiler = await boiler.do_hello("boiler", "steam")
    w_tagger = await tagger.do_hello("tagger", "fish")
    sid_boiler, sid_tagger = w_boiler["sid"], w_tagger["sid"]
    mirror: dict[str, int] = {
        k: int(v["volume"]) for k, v in w_boiler["world"]["nodes"].items()
    }

    cadence = args.tick_ms / 1000.0
    boiled = 0
    tagged = 0
    n_boil = n_tag = 0   # per-session action ids (LW7 nonce dogfood)
    won_tick = None
    for _ in range(args.ticks):
        await asyncio.sleep(cadence)
        if won_tick is None:
            target = _pick_target(BOIL_ORDER, mirror)
            if target is not None:
                n_boil += 1
                reply = await _ask(boiler, sid_boiler, "boil", target, n_boil)
                if reply["op"] == "ack":
                    boiled += 1
        tag_at = _pick_target(TAG_ORDER, mirror)
        if tag_at is not None:
            n_tag += 1
            reply = await _ask(tagger, sid_tagger, "tag", tag_at, n_tag)
            if reply["op"] == "ack":
                tagged += 1
        await server.pump_once()
        tick = await boiler.recv()
        tick2 = await tagger.recv()
        assert tick["op"] == "tick" and tick2 == tick, "clients must see one world"
        mirror = {k: int(v) for k, v in tick["nodes"].items()}
        mark = "  WIN" if tick["winner"] else ""
        print(f"tick {tick['n']:>3}: " +
              " ".join(f"{k}={v}" for k, v in tick["nodes"].items()) + mark)
        if tick["winner"] and won_tick is None:
            won_tick = tick["n"]

    print(f"stats: {server.stats()}")
    if won_tick is not None:
        print(f"THE CROWN FILLS. WIN at tick {won_tick}; "
              f"boiler boiled {boiled}, tagger tagged {tagged}.")
    else:
        print(f"no WIN in {args.ticks} ticks; boiler boiled {boiled}, "
              f"tagger tagged {tagged}.")
    boiler.close()
    tagger.close()
    await server.stop()
    return 0 if won_tick is not None else 1


async def _serve(args: argparse.Namespace) -> None:
    auth = AuthStore(args.users)
    # B4 (2026-09-30): SRP6 is the wired account system of the standing
    # server (salt + verifier store, fresh per handshake); v0 hello stays
    # open behind the fallback flag until the operator flips it off.
    srp_auth = Srp6AuthService(SrpStore(args.srp_users))
    # The production leg of the Z1 weld: the LIVE server feeds each tick
    # through the bridge into the production gps ledger (model
    # mountain-world-v0 / task_shape world-tick), with the per-tick gwap
    # session files landing beside the world log. VerdictFeed construction
    # touches no db (the bridge opens/closes per feed); every feed failure
    # is caught in pump_once -- fail-open, the world outranks the meter.
    world = MountainWorld(log_path=args.log)
    server = WorldServer(
        host=args.host, port=args.port,
        tick_interval=args.tick_ms / 1000.0,
        auth=auth, world=world,
        # B15: log_path is passed so side rooms get durable roots beside the
        # standing log (world_server.<room>.jsonl + per-room innkeeper
        # memories); the default room reuses the injected world, no reopen.
        log_path=args.log,
        verdict_feed=VerdictFeed(
            world, PRODUCTION_GPS_DB,
            store=Path(args.log).parent / "gwap",
        ),
        srp_auth=srp_auth,
        allow_plaintext_hello=not args.no_plaintext_hello,
        require_frame_mac=args.require_frame_mac,
        identity=IdentityBindService(),
        allow_unbound_hello=not args.require_identity,
        open_ws=args.ws,
        ws_port=args.ws_port,
    )
    await server.start()
    if not auth.users:
        print(f"note: {args.users} has no users; add one with "
              f"python -m server.auth {args.users} add <name>")
    if not srp_auth.store.users:
        print(f"note: {args.srp_users} has no SRP6 accounts; add one with "
              f"python -m server.auth_srp6 {args.srp_users} add <name>")
    doors = "SRP6 + plaintext-hello fallback" if server.allow_plaintext_hello \
        else "SRP6 only (plaintext hello refused)"
    mac = "; frame MACs required post-auth" if server.require_frame_mac \
        else "; frame MACs verified when present (migration window open)"
    ident = "; identity-bound sessions only" if not server.allow_unbound_hello \
        else "; identity binding optional (unbound hello open)"
    ws_note = (f"; ws spectator door ws://{args.host}:{server.ws_door.bound_port}/"
               if server.ws_door is not None else "")
    print(f"world server listening on {args.host}:{server.bound_port} "
          f"(tick {args.tick_ms}ms, log {args.log}; auth: {doors}{mac}{ident})"
          f"{ws_note}; Ctrl-C to exit")
    try:
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        await server.stop()


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description="the estate's own world server v0")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--tick-ms", type=int, default=MountainWorld.TICK_MS,
                        help="world tick cadence (default 800)")
    parser.add_argument("--users", default=str(ROOT / "server" / "users.json"),
                        help="path to the auth users JSON file")
    parser.add_argument("--srp-users", default=str(ROOT / "server" / "srp_users.json"),
                        help="path to the SRP6 salt+verifier accounts JSON file")
    parser.add_argument("--no-plaintext-hello", action="store_true",
                        help="refuse the v0 plaintext hello (B4 fallback flag): "
                             "SRP6 becomes the only way in")
    parser.add_argument("--require-frame-mac", action="store_true",
                        help="close the R3 migration window: every frame after "
                             "srp_proof must carry a valid K-derived MAC "
                             "(tamper = BAD_MAC + chain row + disconnect)")
    parser.add_argument("--require-identity", action="store_true",
                        help="V7 binding policy (mirror of --no-plaintext-hello): "
                             "refuse hello from connections that have not proved "
                             "their GitHub-published SSH key — every sid key-bound")
    parser.add_argument("--log", default=str(ROOT / "logs" / "world_server.jsonl"),
                        help="path to the append-only event log JSONL")
    parser.add_argument("--ws", action="store_true",
                        help="open the RFC6455 spectator door on the standing "
                             "world (the ws_door mount, 2026-10-06): browsers "
                             "see every tick frame; actions stay on the TCP "
                             "line protocol")
    parser.add_argument("--ws-port", type=int, default=0,
                        help="fixed port for the ws spectator door "
                             "(default 0 = ephemeral; 8766 is mud_relay's, "
                             "never touched")
    parser.add_argument("--demo", action="store_true",
                        help="run 30 ticks headless with two simulated clients, print the WIN")
    parser.add_argument("--ticks", type=int, default=30, help="demo length in ticks")
    args = parser.parse_args(argv)
    if args.demo and "--port" not in argv:
        args.port = 0  # ephemeral: --demo never fights a live server for 8800
    if args.demo and "--log" not in argv:
        args.log = None  # demo logs to a temp dir unless --log is explicit
    if args.demo:
        return asyncio.run(_demo(args))
    asyncio.run(_serve(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
