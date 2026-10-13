"""rooms: minimal multi-room v0 (B15, 2026-09-30).

MC3's gap dossier row (watch/inbox/mountain_climb/GAP_ANALYSIS.md, system 1):
"One room (room.py); no multi-room". This module closes it the v0 way: a
GameRoom is ONE MountainWorld + its own tick pump + its peers; a RoomBook
keys rooms by short id; the default room "summit" is the standing world
every existing client already lives in. Naming is deliberate:
server/room.py owns the TRANSPORT Room (per-client queues, fan-out); this
module owns the GAME room (a world + a pump + the peers seated around it).

Laws (receipt watch/inbox/last_mile_20260930/B15_ROOMS.md):
  - one world per room, one tick pump per room: a tick in room A advances
    ONLY room A's world and broadcasts ONLY to room A's peers. Cross-room
    isolation is structural: pump_once() fans out over self.peers, and a
    peer sits in exactly one room's peers dict (bound at hello).
  - the join surface gains a room argument: hello {"room": id} (default
    "summit" -- existing clients that never say a room are unchanged), and
    an action may carry "room" naming the room it stages into. Routing is
    by sid first (the sid was issued by ONE room's world); a sid from
    another room honestly meets that world's own UNKNOWN_SID.
  - rooms are born at hello: get_or_create fires only on the hello path,
    so an action naming a room no hello ever made refuses UNKNOWN_ROOM.
  - capacity: a soft cap per room (DEFAULT_ROOM_CAPACITY seats). A full
    room refuses hello with ROOM_FULL -- honest refusal: no sid issued, no
    peer re-binding, the connection keeps whatever room it already held.
    Capacity counts PEERS (seated connections), not sids: one connection
    may hold many sessions in its room (the v0 multi-hello pattern).
  - the innkeeper instantiates per room, its memories scoped per room:
    rooms/summit remembers you, rooms/basecamp has never met you. Its say
    rows are staged back into ITS room's world (the LW6 channel, zero new
    wire ops) so they apply at the next tick of that room alone.
  - empty side rooms sleep: the pump stops when the last peer leaves and
    restarts on the next join. The default room ticks with the server
    (v0 behavior: a zero-client server still ticks the standing world).

Typed rejects (the rooms vocabulary; protocol_table.py is another lane's
fence, so these live here as the next contract version's codes, the LW7
RATE_CAP/STALE_NONCE precedent):
    BAD_ROOM       malformed room id (not [a-z0-9][a-z0-9_-]{0,15})
    UNKNOWN_ROOM   well-formed id, but no hello ever created that room
    ROOM_FULL      the capacity law refused the seat

Not in scope (v1 debt): live session travel between rooms, per-room
capacity overrides, a rooms listing op, cross-room chat.

Run:
    .venv/Scripts/python.exe -m pytest tests/test_rooms.py -q
Tests: tests/test_rooms.py
Schema: rooms.v1 . deterministic + $0 . pump_once is pure fan-out, no RNG
"""
from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.innkeeper import INNKEEPER_SID, Innkeeper  # noqa: E402
from server.protocol import encode  # noqa: E402
from server.world import MountainWorld  # noqa: E402

DEFAULT_ROOM = "summit"
DEFAULT_ROOM_CAPACITY = 8  # seats (peers); the soft cap
ROOM_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,15}$")
ROOM_REJECT_CODES = ("ROOM_FULL", "UNKNOWN_ROOM", "BAD_ROOM")


class GameRoom:
    """One MountainWorld, its tick pump, and the peers seated around it.

    peers maps peer-id -> the server's peer dicts (the same dicts
    server.py registers; the entry with the asyncio.Queue). broadcast()
    fans the SAME encoded line to every seated peer -- the encode-once law,
    scoped to this room alone.

    on_broadcast is the transport weld hook (2026-10-06, the ws-door mount;
    receipt watch/inbox/mates_leave_protocol/receipts/20261006_locksmith.md):
    pump_once hands the hook the SAME encoded line object the TCP peers got,
    after broadcast() lands it. Fail-open by the same law as on_tick: a
    transport hook error must never kill the tick.
    """

    def __init__(
        self,
        room_id: str,
        world: MountainWorld,
        *,
        capacity: int = DEFAULT_ROOM_CAPACITY,
        innkeeper: Innkeeper | None = None,
        tick_interval: float | None = None,
        default: bool = False,
    ) -> None:
        self.id = room_id
        self.world = world
        self.capacity = capacity
        self.innkeeper = innkeeper
        self.default = default
        self.tick_interval = tick_interval
        self.peers: dict[int, dict[str, Any]] = {}
        self.innkeeper_says_staged = 0
        # The after-tick hook (the Z1 verdict-feed weld). Called AFTER the
        # broadcast so clients never wait on the meter; fail-open by law: an
        # on_tick error must NEVER kill the tick.
        self.on_tick: Callable[[dict[str, Any]], None] | None = None
        # The transport weld hook (the ws-door mount, 2026-10-06): sees the
        # SAME encoded line object broadcast() queued to the TCP peers.
        # Fail-open, same law as on_tick: the transport never kills the tick.
        self.on_broadcast: Callable[[bytes], None] | None = None
        self._pump: asyncio.Task | None = None
        self._retired: list[asyncio.Task] = []  # cancelled pumps awaiting reap

    # ------------------------------------------------------------- seats ----
    def is_full(self, peer_id: int | None = None) -> bool:
        """The capacity law. A peer already seated in THIS room never counts
        against itself (re-hello is a re-bind, not a second seat)."""
        if peer_id is not None and peer_id in self.peers:
            return False
        return len(self.peers) >= self.capacity

    def join_peer(self, peer: dict[str, Any]) -> None:
        """Seat a peer (must already have passed is_full). Wakes a sleeping
        side-room pump: a room with players ticks."""
        self.peers[peer["id"]] = peer
        peer["room"] = self
        self.ensure_pump()

    def drop_peer(self, peer_id: int) -> None:
        """Remove a seat. The last peer out of a SIDE room puts it to sleep
        (pump stops, world stays open so a rejoin continues the chain); the
        default room never sleeps."""
        self.peers.pop(peer_id, None)
        if not self.default and not self.peers:
            self.stop_pump()

    # ----------------------------------------------------------- fanout ----
    def broadcast(self, line: bytes) -> int:
        """The isolation law's teeth: fan the SAME bytes to THIS room's
        seated peers and nobody else. Sync by contract (tick loop path)."""
        delivered = 0
        for peer in list(self.peers.values()):
            if peer["queue"] is not None:
                peer["queue"].put_nowait(line)
                delivered += 1
        return delivered

    # -------------------------------------------------------------- tick ----
    def pump_once(self) -> dict[str, Any]:
        """One beat of THIS room: world tick -> broadcast to this room's
        peers -> innkeeper pump (its say rows stage into this world and
        apply next tick) -> on_tick hook. The only driver of this world's
        mutation, and the only broadcaster into this room's queues."""
        payload = self.world.tick()
        line = encode(payload)
        self.broadcast(line)
        if self.on_broadcast is not None:
            # The ws-door mount (2026-10-06): the hook gets the SAME line
            # object the TCP peers got (encode-once across transports).
            # Fail-open by the on_tick law: the transport never kills the tick.
            try:
                self.on_broadcast(line)
            except Exception as exc:  # noqa: BLE001 -- the transport never kills the tick
                print(
                    f"on_broadcast error on tick {payload.get('n')}: {exc!r}"
                    " (door missed this tick; world and cadence continue)",
                    file=sys.stderr,
                )
        if self.innkeeper is not None:
            self._pump_innkeeper(payload)
        if self.on_tick is not None:
            # Z1 weld law, moved with the pump: fail-open, the world
            # outranks the meter.
            try:
                self.on_tick(payload)
            except Exception as exc:  # noqa: BLE001 -- the world outranks the meter
                print(
                    f"verdict_feed error on tick {payload.get('n')}: {exc!r}"
                    " (nothing fed; world and cadence continue)",
                    file=sys.stderr,
                )
        return payload

    def _pump_innkeeper(self, payload: dict[str, Any]) -> None:
        """This room's innkeeper reacts to this room's tick. Every gated say
        row is staged back into THIS world through the ordinary say channel
        (zero new wire ops, determinism law untouched), so its words ride
        the next tick's events to this room's peers alone."""
        rows = self.innkeeper.pump(payload)
        for row in rows["say"]:
            if row.get("op") == "reject":
                continue  # our own law violation never reaches the world
            reply = self.world.stage(INNKEEPER_SID, "say", row.get("text"))
            if reply.get("op") == "ack":
                self.innkeeper_says_staged += 1

    # -------------------------------------------------------------- pump ----
    def ensure_pump(self) -> bool:
        """Start this room's own tick pump if the server runs a cadence and
        the room is awake (the default room, or any room holding peers).
        Manual mode (tick_interval None) never pumps -- tests drive
        pump_once() directly."""
        if self.tick_interval is None or self._pump is not None:
            return False
        if not self.default and not self.peers:
            return False  # the sleep law: empty side rooms do not tick
        self._pump = asyncio.create_task(self._tick_loop())
        return True

    def stop_pump(self) -> None:
        """Cancel the pump without closing the world (sleep, or shutdown)."""
        if self._pump is not None:
            self._pump.cancel()
            self._retired.append(self._pump)
            self._pump = None

    @property
    def pumping(self) -> bool:
        """Is this room's own tick pump running? (test/operability lens)"""
        return self._pump is not None

    async def _tick_loop(self) -> None:
        try:
            while True:
                await asyncio.sleep(self.tick_interval)
                self.pump_once()
        except asyncio.CancelledError:
            return

    async def stop(self) -> None:
        """Full shutdown: cancel the pump, reap every retired task, close
        the world (flushes the chained log)."""
        self.stop_pump()
        tasks = [t for t in self._retired if not t.done()]
        self._retired.clear()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        self.world.close()


class RoomBook:
    """Rooms keyed by short id. The default room "summit" exists from
    construction (the backward-compat world: clients that never say a room
    land there, and its log lands at exactly the log_path the server was
    given); every other room is born at the first hello that names it.

    Path law: a side room's artifacts sit beside the server's log with the
    room id in the stem -- log 'world_log.jsonl', room 'bothy' ->
    'world_log.bothy.jsonl' + innkeeper memories
    'world_log.bothy.players.json'. With no log_path there is no durable
    root, so side rooms run in-memory and no innkeeper keeps memories.
    """

    def __init__(
        self,
        *,
        log_path: Path | str | None = None,
        world: MountainWorld | None = None,
        capacity: int = DEFAULT_ROOM_CAPACITY,
        innkeeper: bool = True,
        tick_interval: float | None = None,
    ) -> None:
        self.log_path = Path(log_path) if log_path is not None else None
        self.capacity = capacity
        self.want_innkeeper = innkeeper
        self.tick_interval = tick_interval
        self.rooms: dict[str, GameRoom] = {}
        self.default_room = self._create(DEFAULT_ROOM, world=world, default=True)

    # -------------------------------------------------------------- ids ----
    @staticmethod
    def valid_id(room_id: Any) -> bool:
        return isinstance(room_id, str) and ROOM_ID_RE.match(room_id) is not None

    # ------------------------------------------------------------ paths ----
    def room_log_path(self, room_id: str) -> Path | None:
        if self.log_path is None:
            return None
        if room_id == DEFAULT_ROOM:
            return self.log_path
        return self.log_path.with_name(f"{self.log_path.stem}.{room_id}.jsonl")

    def room_memories_path(self, room_id: str) -> Path | None:
        """The innkeeper's per-room memory file (the scoping law)."""
        if self.log_path is None:
            return None
        if room_id == DEFAULT_ROOM:
            return self.log_path.with_name(f"{self.log_path.stem}.players.json")
        return self.log_path.with_name(
            f"{self.log_path.stem}.{room_id}.players.json")

    # ------------------------------------------------------------ rooms ----
    def get(self, room_id: str) -> GameRoom | None:
        return self.rooms.get(room_id)

    def get_or_create(self, room_id: str) -> GameRoom:
        """Born at hello: only the hello path may create a room, so an
        action naming a room nobody joined refuses UNKNOWN_ROOM."""
        room = self.rooms.get(room_id)
        if room is None:
            # callers validate the id first; the guard is for future lanes
            if not self.valid_id(room_id):
                raise ValueError(f"invalid room id: {room_id!r}")
            room = self._create(room_id)
        return room

    def _create(
        self,
        room_id: str,
        world: MountainWorld | None = None,
        default: bool = False,
    ) -> GameRoom:
        w = world if world is not None else MountainWorld(
            log_path=self.room_log_path(room_id))
        keep: Innkeeper | None = None
        mem = self.room_memories_path(room_id)
        if self.want_innkeeper and mem is not None:
            keep = Innkeeper(w, mem)
            keep.attach()  # the ike3 seam: a roster row in THIS world
        room = GameRoom(
            room_id, w,
            capacity=self.capacity, innkeeper=keep,
            tick_interval=self.tick_interval, default=default,
        )
        self.rooms[room_id] = room
        return room

    def room_of_sid(self, sid: str) -> GameRoom | None:
        """The room whose world issued this sid. Sids are globally unique
        (64-hex time-salted), so a scan over rosters needs no second index
        to keep in sync; None means no room knows it (the caller falls back
        to the default room, whose world then answers UNKNOWN_SID -- the
        v0 bytes unchanged)."""
        for room in self.rooms.values():
            if sid in room.world.roster:
                return room
        return None

    async def stop_all(self) -> None:
        for room in list(self.rooms.values()):
            await room.stop()

    # dict conveniences (tests, operability)
    def __getitem__(self, room_id: str) -> GameRoom:
        return self.rooms[room_id]

    def __len__(self) -> int:
        return len(self.rooms)

    def __iter__(self):
        return iter(self.rooms.values())
