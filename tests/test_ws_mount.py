"""ws-door mount tests (the locksmith cycle, 2026-10-06).

The door itself was proven byte-level in tests/test_room.py (Mickey17 W1).
What was NEVER proven is the mount: ws_door.py shipped 2026-09-29 with a
3-line integration recipe, zero production importers, and a stale seam
(B15 moved the encode+broadcast into GameRoom.pump_once). These tests pin
the landed wiring:

  - default off: WorldServer without open_ws never opens a door and stats
    report ws_clients 0 (the no-regression law).
  - spectator lens: an RFC6455 client on the mounted door receives the SAME
    encoded tick line bytes the TCP peers got, in order (encode-once across
    transports).
  - isolation: side-room ticks never reach the standing world's door.

Run:
    .venv/Scripts/python.exe -m pytest tests/test_ws_mount.py -q
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.protocol import encode  # noqa: E402
from server.server import WorldServer  # noqa: E402
from server.ws_door import WS_GUID  # noqa: E402


async def _seat_ws_member(port: int) -> tuple[asyncio.StreamReader,
                                              asyncio.StreamWriter]:
    """Handshake one raw RFC6455 socket in and wait for its room seat."""
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    key = base64.b64encode(b"0123456789abcdef").decode()
    writer.write(
        ("GET /ws HTTP/1.1\r\n"
         "Host: mount-test\r\n"
         "Upgrade: WebSocket\r\n"
         "Connection: Upgrade\r\n"
         f"Sec-WebSocket-Key: {key}\r\n"
         "Sec-WebSocket-Version: 13\r\n"
         "\r\n").encode("ascii"))
    await writer.drain()
    resp = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=5.0)
    expected_accept = base64.b64encode(
        hashlib.sha1((key + WS_GUID).encode()).digest()).decode()
    assert resp.startswith(b"HTTP/1.1 101")
    assert expected_accept.encode() in resp
    return reader, writer


async def _wait_seated(door, count: int) -> None:
    for _ in range(100):
        if len(door.room.members) == count:
            return
        await asyncio.sleep(0.02)
    raise AssertionError(f"membership never reached {count}")


async def _read_frame(reader: asyncio.StreamReader) -> tuple[int, bytes]:
    hdr = await reader.readexactly(2)
    op = hdr[0] & 0x0F
    assert bool(hdr[1] & 0x80) is False  # server frames are never masked
    ln = hdr[1] & 0x7F
    if ln == 126:
        ln = int.from_bytes(await reader.readexactly(2), "big")
    elif ln == 127:
        ln = int.from_bytes(await reader.readexactly(8), "big")
    return op, (await reader.readexactly(ln) if ln else b"")


def test_ws_door_off_by_default_no_regression():
    async def scenario():
        srv = WorldServer(port=0, tick_interval=None)
        assert srv.ws_door is None
        assert srv.stats()["ws_clients"] == 0
        await srv.start()
        assert srv.ws_door is None  # start() opened nothing
        assert srv.rooms.default_room.on_broadcast is None
        await srv.pump_once()  # the tick path runs unchanged without a door
        await srv.stop()

    asyncio.run(scenario())


def test_ws_spectator_receives_tick_lines_byte_identical():
    async def scenario():
        srv = WorldServer(port=0, tick_interval=None, open_ws=True)
        await srv.start()
        assert srv.ws_door is not None
        assert srv.ws_door.bound_port  # ephemeral port bound
        reader, writer = await _seat_ws_member(srv.ws_door.bound_port)
        await _wait_seated(srv.ws_door, 1)
        assert srv.stats()["ws_clients"] == 1  # counts filed, not estimated

        lines: list[bytes] = []
        for _ in range(2):
            payload = await srv.pump_once()
            lines.append(encode(payload))
        for expected in lines:
            op, data = await asyncio.wait_for(_read_frame(reader), timeout=5.0)
            assert op == 0x1
            assert data == expected  # the SAME bytes the TCP peers were queued

        writer.close()
        await srv.stop()
        assert srv.ws_door is None  # stop() closed and dropped the door
        assert srv.stats()["ws_clients"] == 0

    asyncio.run(scenario())


def test_side_room_ticks_never_reach_the_standing_door():
    async def scenario():
        srv = WorldServer(port=0, tick_interval=None, open_ws=True)
        await srv.start()
        reader, writer = await _seat_ws_member(srv.ws_door.bound_port)
        await _wait_seated(srv.ws_door, 1)

        bothy = srv.rooms.get_or_create("bothy")
        bothy.pump_once()
        bothy.pump_once()
        assert srv.ws_door.room.published == 0  # isolation: nothing crossed

        payload = await srv.pump_once()  # the standing world DOES feed the door
        assert srv.ws_door.room.published == 1
        op, data = await asyncio.wait_for(_read_frame(reader), timeout=5.0)
        assert op == 0x1 and data == encode(payload)

        writer.close()
        await srv.stop()

    asyncio.run(scenario())
