"""room: the one transport library (Mickey17 W1, 2026-09-29).

Six hand-rolled transports around the estate (mud_relay, cast_server,
api_server, saelis_room, server/, lan_proxy) all repeat one shape: a JSON
send helper, a presence sweep, a fan-out dict under a lock. This module is
that shape harvested once, asyncio-native, so the next transport is a door
and not a seventh copy. Findings it closes: MICKEY17_WAVE_LEDGER_20260929
return 1 (six transports one shape; head-of-line freeze).

Laws the room enforces:
  - encode-once fan-out: publish() hands the SAME bytes object to every
    member queue. No per-client re-encoding, ever.
  - drop-on-slow: each member owns a bounded asyncio.Queue drained by its
    own writer task. A full queue disconnects that laggard (reason "slow")
    inside publish(); publish() is fully synchronous, so one stalled peer
    can never freeze the room's cadence (the mud_relay single-broadcaster
    blocking-sendall bug, closed as a class).
  - presence/expiry: members carry last_seen + meta; sweep() removes
    members not touched within `expire` seconds. Any inbound frame touches.

Not in scope: authority (server/world.py owns it) and wire vocabulary
(server/protocol.py owns it). The room moves bytes, nothing else.
"""
from __future__ import annotations

import asyncio
import time
from typing import Any, Awaitable, Callable

SendFn = Callable[[bytes], Awaitable[None]]
CloseFn = Callable[[], None]

DROP_SLOW = "slow"        # queue full at publish time: the laggard is disconnected
DROP_EXPIRED = "expired"  # presence sweep removed a silent member
DROP_LEFT = "left"        # peer went away (socket closed)
DROP_ERROR = "error"      # the member's own send raised
DROP_CLOSED = "closed"    # room shutdown

DEFAULT_MAXSIZE = 64
DEFAULT_EXPIRE = 6.0  # seconds without a touch before sweep() removes a member


class Member:
    """One seat in the room: a bounded inbox plus the task that drains it."""

    def __init__(
        self,
        mid: str,
        send: SendFn,
        close_fn: CloseFn | None = None,
        meta: dict[str, Any] | None = None,
        maxsize: int = DEFAULT_MAXSIZE,
    ) -> None:
        self.id = mid
        self.send = send
        self.close_fn = close_fn  # called on every drop path to unblock a stuck drain
        self.meta: dict[str, Any] = dict(meta or {})
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self.last_seen = time.time()
        self.task: asyncio.Task | None = None

    def touch(self, now: float | None = None) -> None:
        self.last_seen = now if now is not None else time.time()

    def age(self, now: float | None = None) -> float:
        return (now if now is not None else time.time()) - self.last_seen


class Room:
    """Per-client queues, encode-once fan-out, drop-on-slow, presence/expiry.

    Shape:
        room = Room(maxsize=64, expire=6.0)
        member = room.join(send=async_writer, close_fn=writer.close, meta={...})
        room.publish(frame_bytes)     # sync; same bytes object to every queue
        room.touch(member.id)         # any inbound frame refreshes presence
        await room.close()            # cancels every writer task

    publish() must be callable from a tick loop without awaiting, so every
    path inside it is put_nowait/drop, never a blocking send.
    """

    def __init__(
        self,
        maxsize: int = DEFAULT_MAXSIZE,
        expire: float = DEFAULT_EXPIRE,
        on_drop: Callable[[Member, str], None] | None = None,
    ) -> None:
        self.maxsize = maxsize
        self.expire = expire
        self.on_drop = on_drop  # optional (member, reason) observer; best-effort
        self.members: dict[str, Member] = {}
        self.published = 0
        self.dropped: dict[str, int] = {}
        self._seq = 0

    # ------------------------------------------------------------- seats ----
    def join(
        self,
        send: SendFn,
        close_fn: CloseFn | None = None,
        meta: dict[str, Any] | None = None,
        mid: str | None = None,
    ) -> Member:
        """Take a seat. Must be called inside a running event loop (the
        writer task is spawned here). Presence clock starts now."""
        self._seq += 1
        mid = mid if mid is not None else f"m{self._seq}"
        member = Member(mid, send, close_fn, meta, self.maxsize)
        self.members[mid] = member
        member.task = asyncio.create_task(self._writer(member))
        return member

    def leave(self, mid: str, reason: str = DROP_LEFT) -> bool:
        """The single drop path (peer close, slow, expired, error, shutdown).
        Idempotent: dropping an already-dropped member is a no-op."""
        member = self.members.pop(mid, None)
        if member is None:
            return False
        self.dropped[reason] = self.dropped.get(reason, 0) + 1
        if member.close_fn is not None:
            try:
                member.close_fn()
            except Exception:
                pass  # transport already dead; the drop still stands
        try:
            member.queue.put_nowait(None)  # wake a writer parked on get()
        except asyncio.QueueFull:
            pass  # queue full: close_fn above makes the in-flight send raise
        if member.task is not None and member.task is not asyncio.current_task():
            member.task.cancel()
        if self.on_drop is not None:
            try:
                self.on_drop(member, reason)
            except Exception:
                pass  # an observer must never break the drop path
        return True

    async def _writer(self, member: Member) -> None:
        """Drain this member's inbox. Only this task ever awaits send(), so
        backpressure lives here, per client, never in the publish path."""
        try:
            while True:
                data = await member.queue.get()
                try:
                    if data is None:
                        return
                    await member.send(data)
                finally:
                    member.queue.task_done()
        except (asyncio.CancelledError, ConnectionError, OSError):
            return
        except Exception:
            self.leave(member.id, DROP_ERROR)

    # ------------------------------------------------------------ fanout ----
    def publish(self, data: bytes) -> int:
        """Encode-once fan-out: the SAME bytes object goes to every member
        queue. A member whose queue is full is dropped (reason "slow") on
        the spot; the loop is never blocked. Returns delivered count."""
        delivered = 0
        for member in list(self.members.values()):
            try:
                member.queue.put_nowait(data)
                delivered += 1
            except asyncio.QueueFull:
                self.leave(member.id, DROP_SLOW)
        self.published += 1
        return delivered

    async def wait_idle(self) -> None:
        """Block until every member's inbox is fully drained. Test/demo
        primitive; the room itself never needs it."""
        for member in list(self.members.values()):
            await member.queue.join()

    # ---------------------------------------------------------- presence ----
    def touch(self, mid: str) -> None:
        member = self.members.get(mid)
        if member is not None:
            member.touch()

    def presence(self, now: float | None = None) -> dict[str, dict[str, Any]]:
        """Fresh members only: id, age, meta. Spectator lens, read-only."""
        now = now if now is not None else time.time()
        rows: dict[str, dict[str, Any]] = {}
        for mid, member in self.members.items():
            if member.age(now) <= self.expire:
                rows[mid] = {"id": mid, "age": round(member.age(now), 3), **member.meta}
        return rows

    def sweep(self, now: float | None = None) -> int:
        """Drop members silent longer than expire. Returns how many went."""
        now = now if now is not None else time.time()
        stale = [m for m in self.members.values() if m.age(now) > self.expire]
        for member in stale:
            self.leave(member.id, DROP_EXPIRED)
        return len(stale)

    def stats(self) -> dict[str, int]:
        out: dict[str, int] = {"members": len(self.members), "published": self.published}
        out.update({f"dropped_{k}": v for k, v in self.dropped.items()})
        return out

    async def close(self) -> None:
        """Shutdown: drop every member (closes transports), reap tasks."""
        tasks = [m.task for m in self.members.values() if m.task is not None]
        for mid in list(self.members):
            self.leave(mid, DROP_CLOSED)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
