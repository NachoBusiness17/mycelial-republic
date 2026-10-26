"""ws_door: a minimal RFC6455 server-side door that plugs a Room into the
world server's tick broadcast (Mickey17 W1, 2026-09-29).

The handshake and frame byte logic are stolen from dashboard/mud_relay.py
(FW-37 ws spike, 2026-09-28: _ws_read_frame, _ws_send_frame, the SHA1+GUID
accept computation, the 7/16/64-bit length forms, the 1 MiB monster-frame
cap). That file is the original author of the bytes; this module ports them
from blocking sockets + one broadcaster thread to asyncio StreamReader/
Writer + per-client writer tasks, because the thread version is the
head-of-line freeze the room exists to kill (ledger return 1).

THE MOUNT (LANDED 2026-10-06, receipt watch/inbox/mates_leave_protocol/
receipts/20261006_locksmith.md). The original W1 note said "the server owner
adds 3 lines to server/server.py; this lane does not edit that file" -- the
server owner never came, so the door sat unmounted for a week (imported by
nobody but its test). The landed shape, adapted to B15 rooms (which moved the
encode+broadcast off WorldServer.pump_once into GameRoom.pump_once):

    WorldServer(--ws) mounts ONE door on the DEFAULT room ("summit",
    the standing world; side rooms stay TCP-only v0, the Z1 weld precedent):

        open_ws: bool = False      # WorldServer.__init__: default-off, the
        ws_port: int = 0           #   migration-flag shape; 0 = ephemeral
        # start(): self.ws_door = await WsDoor().start(self.host, self.ws_port)
        #           self.rooms.default_room.on_broadcast = self.ws_door.publish
        # stop():   await self.ws_door.stop()
        # CLI: --ws / --ws-port (never 8766: mud_relay's port)

GameRoom.pump_once hands on_broadcast the SAME encoded line object the TCP
peers got (encode-once across transports); WsDoor.publish frames it once and
fans the same frame bytes to every socket. publish is synchronous: the tick
loop never awaits it. Scope is unchanged: the door is a SPECTATOR lens --
inbound text frames carry presence meta only; actions stay on the TCP line
protocol (server/README.md).

Port law: the door NEVER defaults to 8766 (mud_relay's port; cast_server
already collided there, ledger return 1). start() binds ephemeral (port 0);
the standalone demo below defaults to 8801.

Scope is deliberately minimal: text frames + ping/pong + close echo.
Fragmented continuation frames are ignored (out of scope, named honestly).
Mask law (Q22 fix, 2026-10-01): RFC6455 5.1 requires a server to FAIL the
connection on an unmasked client frame, so the default is strict, closing
with 1002 (protocol error, 7.4.1). The old v0 leniency (mud_relay parity)
survives only as an opt-in: WsDoor(allow_unmasked_client=True), the estate's
allow_plaintext_hello flag shape. Every real client of this door is a
browser WebSocket (browsers mask mandatorily, RFC6455 5.3), so the strict
default breaks no known caller. Any inbound frame touches the sender's
presence (room law).

Run standalone:  .venv/Scripts/python.exe -m server.ws_door [--port 8801]
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.room import Room  # noqa: E402

WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
MAX_FRAME = 1 << 20  # refuse frames over 1 MiB (presence/tick frames are tiny)
OP_CONT, OP_TEXT, OP_CLOSE, OP_PING, OP_PONG = 0x0, 0x1, 0x8, 0x9, 0xA
DOOR_PORT = 8801  # never 8766: that is mud_relay's room
CLOSE_PROTOCOL_ERROR = 1002  # RFC6455 7.4.1: the code 5.1 failures close with


class UnmaskedClientFrame(Exception):
    """RFC6455 5.1 (Q22 fix, 2026-10-01): a client frame arrived with the
    mask bit clear while the door is strict. The session answers with close
    1002 and drops the socket; distinct from the None return, which is
    EOF/truncation/oversize, not a protocol violation."""


# ------------------------------------------------------------- framing ----
# Byte logic stolen from dashboard/mud_relay.py _ws_send_frame: server-to-
# client frames are unmasked (RFC6455 5.1); lengths 7/16/64-bit.
def ws_frame(payload: bytes, op: int = OP_TEXT) -> bytes:
    """Build one server-to-client frame. Pure, so publish() can build the
    frame once and hand the same bytes to every member queue."""
    ln = len(payload)
    hdr = bytearray([0x80 | op])
    if ln < 126:
        hdr.append(ln)
    elif ln < 65536:
        hdr.append(126)
        hdr += ln.to_bytes(2, "big")
    else:
        hdr.append(127)
        hdr += ln.to_bytes(8, "big")
    return bytes(hdr) + payload


# Byte logic stolen from dashboard/mud_relay.py _ws_read_frame: client
# frames are masked; length forms 7/16/64-bit all parsed; over-size refused.
# Q22 fix (2026-10-01): the mask bit is no longer optional. RFC6455 5.1
# fails unmasked client frames; the old v0 tolerance lives only behind the
# allow_unmasked_client flag (mud_relay parity opt-in).
async def read_ws_frame(reader: asyncio.StreamReader, *,
                        allow_unmasked_client: bool = False
                        ) -> tuple[int, bytes] | None:
    """One client frame -> (opcode, payload), None on close/error/truncation,
    or UnmaskedClientFrame when the mask bit is clear and the door is strict."""
    try:
        hdr = await reader.readexactly(2)
        op = hdr[0] & 0x0F
        masked = bool(hdr[1] & 0x80)
        if not masked and not allow_unmasked_client:
            # fail fast: do not drain bytes of a frame the spec already
            # doomed; the caller sends close 1002 and drops the socket
            raise UnmaskedClientFrame()
        ln = hdr[1] & 0x7F
        if ln == 126:
            ln = int.from_bytes(await reader.readexactly(2), "big")
        elif ln == 127:
            ln = int.from_bytes(await reader.readexactly(8), "big")
        if ln > MAX_FRAME:
            return None
        mask = await reader.readexactly(4) if masked else b"\x00\x00\x00\x00"
        data = await reader.readexactly(ln) if ln else b""
    except (asyncio.IncompleteReadError, ConnectionError, OSError):
        return None
    if masked:
        data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    return op, data


def accept_key(key: str) -> str:
    """RFC6455 4.2.2: base64(SHA1(key + GUID)). Stolen from mud_relay."""
    digest = hashlib.sha1((key + WS_GUID).encode("utf-8")).digest()
    return base64.b64encode(digest).decode("ascii")


# ----------------------------------------------------------- handshake ----
async def handshake(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
    """Byte-level RFC6455 server handshake on a raw connection.

    Reads the GET request up to the blank line, requires Upgrade: websocket
    and Sec-WebSocket-Key, answers 101 with the computed accept. Anything
    else gets a 400 and a closed socket. Returns True when the connection
    is now a websocket."""
    try:
        raw = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=10.0)
    except (asyncio.IncompleteReadError, asyncio.TimeoutError,
            asyncio.LimitOverrunError, ConnectionError, OSError):
        return False
    lines = raw.decode("latin-1", "replace").split("\r\n")
    if not lines or not lines[0].upper().startswith("GET"):
        return _reject(writer)
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    if "websocket" not in headers.get("upgrade", "").lower():
        return _reject(writer)
    key = headers.get("sec-websocket-key", "")
    if not key:
        return _reject(writer)
    resp = (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept_key(key)}\r\n"
        "\r\n"
    )
    try:
        writer.write(resp.encode("ascii"))
        await writer.drain()
    except (ConnectionError, OSError):
        return False
    return True


def _reject(writer: asyncio.StreamWriter) -> bool:
    try:
        writer.write(b"HTTP/1.1 400 Bad Request\r\n"
                     b"Content-Length: 0\r\nConnection: close\r\n\r\n")
    except (ConnectionError, OSError):
        pass
    return False


# ---------------------------------------------------------------- door ----
class WsDoor:
    """A websocket listener whose every socket is a Room member.

    The room does the transport law (per-client queues, encode-once
    fan-out, drop-on-slow, presence/expiry); the door does RFC6455 bytes
    and the one-hook integration above.
    """

    def __init__(self, room: Room | None = None,
                 maxsize: int = 64, expire: float = 6.0,
                 allow_unmasked_client: bool = False) -> None:
        self.room = room if room is not None else Room(maxsize=maxsize, expire=expire)
        self._server: asyncio.AbstractServer | None = None
        self.bound_port: int | None = None
        # Q22 fix (2026-10-01): RFC6455 5.1 strict by default, unmasked
        # client frames fail with close 1002. True is the v0 leniency
        # (mud_relay parity) as an OPT-IN, mirroring the estate's
        # allow_plaintext_hello flag shape: named, defaulted, documented.
        # Census at flip time: every known client is a browser WebSocket
        # (browsers mask mandatorily), so the default breaks no caller.
        self.allow_unmasked_client = allow_unmasked_client

    async def start(self, host: str = "127.0.0.1", port: int = 0) -> "WsDoor":
        """Open the door. port 0 (default) = ephemeral, so a second door
        never fights a live one (and 8766 is never touched)."""
        self._server = await asyncio.start_server(self._handle, host, port)
        self.bound_port = self._server.sockets[0].getsockname()[1]
        return self

    def publish(self, line: bytes) -> int:
        """The tick hook (integration line 3): frame the encoded line ONCE,
        fan the same frame bytes to every socket. Sync by contract."""
        return self.room.publish(ws_frame(line))

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
        await self.room.close()

    # ------------------------------------------------------------ inner ----
    async def _handle(self, reader: asyncio.StreamReader,
                      writer: asyncio.StreamWriter) -> None:
        if not await handshake(reader, writer):
            writer.close()
            try:
                await writer.wait_closed()
            except (ConnectionError, OSError):
                pass
            return
        await self._session(reader, writer)

    @staticmethod
    def _sender(writer: asyncio.StreamWriter):
        async def send(data: bytes) -> None:
            writer.write(data)
            await writer.drain()  # backpressure lands in this member's task only
        return send

    async def _session(self, reader: asyncio.StreamReader,
                       writer: asyncio.StreamWriter) -> None:
        peername = writer.get_extra_info("peername")
        member = self.room.join(
            send=self._sender(writer),
            close_fn=writer.close,
            meta={"transport": "ws", "peer": str(peername)},
        )
        try:
            while True:
                try:
                    frame = await read_ws_frame(
                        reader, allow_unmasked_client=self.allow_unmasked_client)
                except UnmaskedClientFrame:
                    # RFC6455 5.1: fail the connection (7.1.7) with the
                    # protocol-error code (7.4.1), then drop the socket.
                    # Q22 fix 2026-10-01: this replaces the v0 silent
                    # tolerance, which read the frame as if mask b"\0"*4.
                    try:
                        writer.write(ws_frame(
                            CLOSE_PROTOCOL_ERROR.to_bytes(2, "big"), OP_CLOSE))
                        await writer.drain()
                    except (ConnectionError, OSError):
                        pass
                    return
                if frame is None:
                    return
                op, data = frame
                if op == OP_CLOSE:
                    try:
                        writer.write(ws_frame(data[:2], OP_CLOSE))  # echo the code
                        await writer.drain()
                    except (ConnectionError, OSError):
                        pass
                    return
                if op == OP_PING:
                    try:
                        writer.write(ws_frame(data, OP_PONG))
                        await writer.drain()
                    except (ConnectionError, OSError):
                        return
                    continue
                if op != OP_TEXT:
                    continue  # minimal door: text frames carry meaning
                self.room.touch(member.id)  # any inbound frame refreshes presence
                try:
                    row = json.loads(data.decode("utf-8"))
                except (ValueError, UnicodeDecodeError):
                    continue
                if isinstance(row, dict):
                    # presence meta, mud_relay shape: {"id":..., "name":...}
                    if row.get("id"):
                        member.meta["id"] = str(row["id"])[:24]
                    if row.get("name"):
                        member.meta["name"] = str(row["name"])[:24]
        finally:
            self.room.leave(member.id)  # socket gone: no expiry ghost
            writer.close()
            try:
                await writer.wait_closed()
            except (ConnectionError, OSError):
                pass


# ---------------------------------------------------------------- demo ----
async def _serve(args: argparse.Namespace) -> None:
    """Standalone heartbeat: the door broadcasting one JSON tick line every
    125ms, so an owner can proof the room with any ws client before wiring
    the real server."""
    door = WsDoor()
    await door.start(args.host, args.port)
    print(f"ws_door: room open at ws://{args.host}:{door.bound_port}/  "
          f"(heartbeat 8Hz, port {door.bound_port}; 8766 is mud_relay's, untouched)")
    n = 0
    try:
        while True:
            await asyncio.sleep(0.125)
            n += 1
            door.publish(json.dumps({"op": "tick", "n": n},
                                    sort_keys=True, separators=(",", ":")).encode()
                         + b"\n")
            door.room.sweep()
    except asyncio.CancelledError:
        pass
    finally:
        await door.stop()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="standalone ws door demo")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DOOR_PORT)
    args = parser.parse_args(argv)
    asyncio.run(_serve(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
