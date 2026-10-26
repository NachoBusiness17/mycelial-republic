"""room + ws_door tests (Mickey17 W1, 2026-09-29).

Every test is a law: fan-out hands the SAME bytes object to three members,
a full queue drops the laggard while the loop and the fast members carry
on, presence expires the silent, the RFC6455 handshake answers a crafted
client hello with the byte-exact 101 (SHA1+GUID accept computed
independently here), and frames round-trip both directions over a real
socket (publish, masked text presence, ping/pong, close echo, 16-bit
length forms), plus the RFC6455 5.1 mask law (Q22 fix, 2026-10-01): an
unmasked client frame on the strict default fails the connection with
close 1002, a masked frame is accepted as before, and the
allow_unmasked_client flag restores the v0 mud_relay-parity leniency.
"""
from __future__ import annotations

import asyncio
import base64
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mag.game_brawl as gb  # noqa: E402
import mag.game_campaign as gc  # noqa: E402
from server.protocol import encode  # noqa: E402
from server.room import Room  # noqa: E402
from server.ws_door import WS_GUID, WsDoor  # noqa: E402

CLOSE_PROTOCOL_ERROR = 1002  # RFC6455 7.4.1, the code 5.1 failures close with


class FakeClient:
    """A member whose transport is a list: records every delivery."""

    def __init__(self) -> None:
        self.got: list[bytes] = []
        self.closed = False

    async def send(self, data: bytes) -> None:
        self.got.append(data)

    def close(self) -> None:
        self.closed = True


class StalledClient(FakeClient):
    """A member whose send never completes: the laggard the law is about."""

    async def send(self, data: bytes) -> None:
        await asyncio.Event().wait()


class StallAfterRecord(FakeClient):
    """Records one frame, then parks inside send() forever: the slow
    spectator who got their lines and then stopped draining."""

    async def send(self, data: bytes) -> None:
        self.got.append(data)
        await asyncio.Event().wait()


# ------------------------------------------------------------ room laws ----

def test_fanout_three_fake_clients_same_bytes_object():
    async def scenario():
        room = Room()
        clients = [FakeClient() for _ in range(3)]
        for c in clients:
            room.join(send=c.send, close_fn=c.close)
        payloads = [f"tick-{i}".encode() for i in range(3)]
        for p in payloads:
            assert room.publish(p) == 3
        await room.wait_idle()
        for c in clients:
            assert c.got == payloads  # order preserved, nothing lost
        # the encode-once law: not just equal bytes, the SAME bytes object
        assert clients[0].got[0] is clients[1].got[0] is clients[2].got[0]
        assert clients[0].got[2] is clients[2].got[2]
        assert room.stats()["members"] == 3
        await room.close()

    asyncio.run(scenario())


def test_slow_client_dropped_loop_never_blocks():
    async def scenario():
        room = Room(maxsize=2)
        slow, fast = StalledClient(), FakeClient()
        slow_m = room.join(send=slow.send, close_fn=slow.close, meta={"name": "laggard"})
        room.join(send=fast.send, close_fn=fast.close)
        # three publishes, yielding between each so the fast member drains:
        # the slow writer picked up "a" and stalled inside send(), so its
        # inbox stops moving and fills while the fast one keeps emptying
        assert room.publish(b"a") == 2
        await asyncio.sleep(0)
        assert room.publish(b"b") == 2
        await asyncio.sleep(0)
        assert room.publish(b"c") == 2  # slow inbox now at its bound (2)
        # the fourth finds that queue full: the laggard is disconnected NOW,
        # publish stays synchronous, the fast member still gets the bytes
        assert room.publish(b"d") == 1
        await asyncio.sleep(0)  # let the fast writer drain c and d
        assert slow.closed is True  # drop path closed the transport
        assert slow_m.id not in room.members
        assert room.dropped["slow"] == 1
        assert "laggard" not in [m.get("name") for m in room.presence().values()]
        assert room.publish(b"e") == 1  # the room carries on without it
        await room.wait_idle()
        assert fast.got == [b"a", b"b", b"c", b"d", b"e"]
        await room.close()  # reaps the stalled writer without hanging

    asyncio.run(scenario())


def test_presence_touch_and_sweep_expiry():
    async def scenario():
        room = Room(expire=6.0)
        fresh = FakeClient()
        silent = FakeClient()
        room.join(send=fresh.send, meta={"id": "ada"}, mid="ada")
        room.join(send=silent.send, meta={"id": "ben"}, mid="ben")
        assert set(room.presence()) == {"ada", "ben"}
        room.touch("ada")  # any inbound frame refreshes presence
        import time as _t
        room.members["ben"].last_seen = _t.time() - 7.0  # backdate the silent one
        assert room.sweep() == 1
        assert room.dropped["expired"] == 1
        rows = room.presence()
        assert set(rows) == {"ada"} and rows["ada"]["id"] == "ada"
        assert 0.0 <= rows["ada"]["age"] <= 6.0
        assert room.sweep() == 0  # a fresh room sweeps clean
        await room.close()

    asyncio.run(scenario())


# ------------------------------------------- game_brawl room integration ----
# Z6 (2026-09-29): game_brawl wires the tavern into ONE Room per brawl_id.
# handle_brawl_voice is the inbound-frame handler — room.touch per frame,
# engine run (authority untouched), publish() of the advance/react lines,
# sweep() of a silent awaiting_player. Dice are pinned (every roll totals 2
# → all attacks miss, HP never moves) so the engine loop is deterministic
# and the assertions below are about bytes, not luck.

def _patch_brawl_tree(monkeypatch, tmp_path):
    monkeypatch.setattr(gb, "BRAWL_DIR", tmp_path / "brawls")
    monkeypatch.setattr(gc, "CAMP_DIR", tmp_path / "campaigns")
    monkeypatch.setattr("mag.game_freeze.freeze_campaign", lambda *a, **k: {"ok": False})
    monkeypatch.setattr("mag.training_events.emit", lambda *a, **k: None)
    monkeypatch.setattr("mag.corpus_query.inspire_for_scene", lambda **k: {"ok": False})
    monkeypatch.setattr(
        gb,
        "roll_dice",
        lambda notation, **k: {
            "ok": True, "notation": notation, "faces": [2], "modifier": 0, "total": 2,
        },
    )


def test_brawl_room_two_spectators_publish_touch_sweep(monkeypatch, tmp_path):
    _patch_brawl_tree(monkeypatch, tmp_path)

    # fixture brawl: awaiting_player at the pc's seat, campaign linked by session
    bid, sess = "br-roomlaw1", "sess-roomlaw"
    pc = gb.tavern_brawler_sheet("Ash")
    combatants = gb._roll_initiative([pc] + gb._clone_roster())
    order = [c["id"] for c in combatants]
    gb.save_brawl(
        {
            "schema": gb.SCHEMA,
            "brawl_id": bid,
            "session_id": sess,
            "campaign_id": "gc-roomlaw",
            "status": "awaiting_player",
            "room_id": "tavern_lantern",
            "story": "failed_hunt",
            "round": 1,
            "turn_index": order.index("pc"),
            "combatants": combatants,
            "initiative_order": order,
            "history": [],
            "metrics": {
                "npc_turns": 0, "player_turns": 0, "absurd_n": 0,
                "ds_rounds": 0, "text_n": 0, "speech_n": 0,
            },
        }
    )
    gc.save_campaign(
        {
            "schema": "mag_game_campaign.v1",
            "campaign_id": "gc-roomlaw",
            "voice_session_id": sess,
            "module_id": "classic",
            "status": "active",
            "room_id": "tavern_lantern",
            "player": {"name": "Ash", "hp": 12, "hp_max": 12, "ac": 12},
            "storyteller": {"brawl_id": bid},
            "flags": ["failed_hunt"],
            "log": [],
        }
    )

    async def scenario():
        # one Room per brawl_id: the player seat + two spectators
        room = gb.brawl_room(bid, create=True, maxsize=1)
        player, ada, bog = FakeClient(), FakeClient(), StallAfterRecord()
        gb.join_brawl_room(bid, send=player.send, close_fn=player.close, mid="pc-seat")
        gb.join_brawl_room(
            bid, send=ada.send, close_fn=ada.close, meta={"name": "ada"}, mid="spec-ada"
        )
        gb.join_brawl_room(
            bid, send=bog.send, close_fn=bog.close, meta={"name": "bog"}, mid="spec-bog"
        )
        assert gb.brawl_room(bid, create=True) is room  # ONE room per brawl_id
        assert set(room.presence()) == {"pc-seat", "spec-ada", "spec-bog"}

        # frame 1 — a real player line: engine runs, lines published to all seats
        res1 = gb.handle_brawl_voice(
            "punch vex", session_id=sess, use_ds=False, member_id="pc-seat"
        )
        await asyncio.sleep(0.01)
        assert res1["ok"] and res1["brawl_id"] == bid
        f1 = player.got[0]
        assert f1 is ada.got[0] is bog.got[0]  # encode-once: the SAME bytes object
        frame1 = json.loads(f1.decode())
        assert frame1["op"] == "brawl" and frame1["brawl_id"] == bid
        assert frame1["status"] == "awaiting_player" and frame1["lines"]

        # frames 2 and 3 — bog's writer is parked in send with a full inbox:
        # the third publish drops the laggard, the frame handler still returns
        res2 = gb.handle_brawl_voice("look", session_id=sess, member_id="pc-seat")
        await asyncio.sleep(0.01)
        assert res2["ok"]
        res3 = gb.handle_brawl_voice("look", session_id=sess, member_id="pc-seat")
        await asyncio.sleep(0.01)
        assert res3["ok"]  # the dropped laggard never blocked the handler
        assert bog.closed is True and "spec-bog" not in room.members
        assert room.dropped["slow"] == 1
        assert len(player.got) == 3 and len(ada.got) == 3 and len(bog.got) == 1
        assert player.got[1] is ada.got[1] and player.got[2] is ada.got[2]

        # sweep law — an awaiting_player brawl expires silent seats; the
        # inbound frame's touch refreshes only the sender's seat
        import time as _t

        room.members["pc-seat"].last_seen = _t.time() - 7.0
        room.members["spec-ada"].last_seen = _t.time() - 7.0
        res4 = gb.handle_brawl_voice("look", session_id=sess, member_id="pc-seat")
        await asyncio.sleep(0.01)
        assert res4["ok"]
        assert room.dropped["expired"] == 1  # ada sat silent: swept
        assert set(room.members) == {"pc-seat"}  # pc-seat was touched per frame
        assert "spec-ada" not in room.presence()
        assert len(player.got) == 4  # the survivor keeps receiving

        # shutdown: room closed, writers reaped, registry entry gone
        assert await gb.close_brawl_room(bid) is True
        assert gb.brawl_room(bid) is None
        assert room.stats()["members"] == 0

    asyncio.run(scenario())


# ---------------------------------------------------------- ws door laws ----

def _expected_accept(key: str) -> str:
    """Independent RFC6455 4.2.2 computation: base64(SHA1(key + GUID))."""
    return base64.b64encode(hashlib.sha1((key + WS_GUID).encode()).digest()).decode()


async def _open_raw(port: int) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    return await asyncio.open_connection("127.0.0.1", port)


def _client_hello(key: str, path: str = "/ws") -> bytes:
    return (
        f"GET {path} HTTP/1.1\r\n"
        "Host: room-test\r\n"
        "Upgrade: WebSocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Key: {key}\r\n"
        "Sec-WebSocket-Version: 13\r\n"
        "\r\n"
    ).encode("ascii")


def _client_frame(payload: bytes, op: int = 0x1) -> bytes:
    """Masked client frame (RFC6455 5.3), all length forms."""
    mask = b"\x0f\x1e\x2d\x3c"
    masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
    ln = len(payload)
    hdr = bytearray([0x80 | op])
    if ln < 126:
        hdr.append(0x80 | ln)
    elif ln < 65536:
        hdr.append(0x80 | 126)
        hdr += ln.to_bytes(2, "big")
    else:
        hdr.append(0x80 | 127)
        hdr += ln.to_bytes(8, "big")
    return bytes(hdr) + mask + masked


def _client_frame_unmasked(payload: bytes, op: int = 0x1) -> bytes:
    """UNMASKED client frame: mask bit clear, no mask bytes. This is the
    shape RFC6455 5.1 dooms, legal here only behind the lenient flag."""
    assert len(payload) < 126  # tiny payloads only: one 7-bit length byte
    return bytes([0x80 | op, len(payload)]) + payload


async def _read_server_frame(reader: asyncio.StreamReader) -> tuple[int, bytes]:
    hdr = await reader.readexactly(2)
    op = hdr[0] & 0x0F
    assert bool(hdr[1] & 0x80) is False  # server frames are never masked
    ln = hdr[1] & 0x7F
    if ln == 126:
        ln = int.from_bytes(await reader.readexactly(2), "big")
    elif ln == 127:
        ln = int.from_bytes(await reader.readexactly(8), "big")
    data = await reader.readexactly(ln) if ln else b""
    return op, data


async def _ws_member(door: WsDoor) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    """Handshake one raw socket in and wait for its room seat to land."""
    reader, writer = await _open_raw(door.bound_port)
    key = base64.b64encode(b"0123456789abcdef").decode()
    writer.write(_client_hello(key))
    await writer.drain()
    resp = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=5.0)
    assert resp.startswith(b"HTTP/1.1 101")
    for _ in range(40):
        if len(door.room.members) == 1:
            break
        await asyncio.sleep(0.02)
    assert len(door.room.members) == 1
    return reader, writer


def test_ws_handshake_byte_level_against_crafted_hello():
    async def scenario():
        door = WsDoor()
        await door.start("127.0.0.1", 0)
        # a crafted hello with a known 16-byte key
        key = base64.b64encode(b"0123456789abcdef").decode()
        reader, writer = await _open_raw(door.bound_port)
        writer.write(_client_hello(key))
        await writer.drain()
        resp = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), timeout=5.0)
        expected = (
            "HTTP/1.1 101 Switching Protocols\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Sec-WebSocket-Accept: {_expected_accept(key)}\r\n"
            "\r\n"
        ).encode("ascii")
        assert resp == expected  # byte-exact, accept computed independently

        # a plain GET without the upgrade gets 400 and a closed door
        reader2, writer2 = await _open_raw(door.bound_port)
        writer2.write(b"GET /nope HTTP/1.1\r\nHost: t\r\n\r\n")
        await writer2.drain()
        resp2 = await asyncio.wait_for(
            reader2.readuntil(b"\r\n\r\n"), timeout=5.0)
        assert resp2.startswith(b"HTTP/1.1 400")
        assert await reader2.read() == b""  # the door closed behind the 400

        writer.close()
        writer2.close()
        await door.stop()

    asyncio.run(scenario())


def test_ws_frame_roundtrip_publish_touch_ping_close():
    async def scenario():
        door = WsDoor()
        await door.start("127.0.0.1", 0)

        # two sockets handshake in and become room members
        readers, writers = [], []
        for _ in range(2):
            r, w = await _open_raw(door.bound_port)
            key = base64.b64encode(b"0123456789abcdef").decode()
            w.write(_client_hello(key))
            await w.drain()
            resp = await asyncio.wait_for(r.readuntil(b"\r\n\r\n"), timeout=5.0)
            assert resp.startswith(b"HTTP/1.1 101")
            readers.append(r)
            writers.append(w)
        for _ in range(40):  # membership lands after each handshake
            if len(door.room.members) == 2:
                break
            await asyncio.sleep(0.02)
        assert len(door.room.members) == 2
        assert all(m.meta.get("transport") == "ws" for m in door.room.members.values())

        # publish: the tick hook frames once, both sockets read the same bytes
        line = encode({"op": "tick", "n": 1, "nodes": {"spring": 4}})
        assert door.publish(line) == 2  # sync hook, delivered count returned
        op, data = await asyncio.wait_for(_read_server_frame(readers[0]), timeout=5.0)
        assert op == 0x1 and data == line
        op2, data2 = await asyncio.wait_for(_read_server_frame(readers[1]), timeout=5.0)
        assert op2 == 0x1 and data2 == data

        # 16-bit length form both directions: a >125-byte tick and a
        # >125-byte masked presence frame
        big = encode({"op": "tick", "n": 2, "pad": "x" * 300})
        assert len(big) >= 126
        door.publish(big)
        op, data = await asyncio.wait_for(_read_server_frame(readers[0]), timeout=5.0)
        assert op == 0x1 and data == big and len(data) >= 126
        op, data = await asyncio.wait_for(_read_server_frame(readers[1]), timeout=5.0)
        assert op == 0x1 and data == big  # same big frame on the second socket too
        # client -> server: masked text presence frame refreshes presence + meta
        writers[0].write(_client_frame(
            ('{"id":"ada","name":"Ada","pad":"' + "y" * 200 + '"}').encode()))
        await writers[0].drain()
        seen_meta = False
        for _ in range(50):
            rows = door.room.presence()
            if any(m.get("name") == "Ada" and m.get("id") == "ada" for m in rows.values()):
                seen_meta = True
                break
            await asyncio.sleep(0.02)
        assert seen_meta is True

        # masked ping -> unmasked pong with the same payload
        writers[0].write(_client_frame(b"heartbeat", op=0x9))
        await writers[0].drain()
        op, data = await asyncio.wait_for(_read_server_frame(readers[0]), timeout=5.0)
        assert op == 0xA and data == b"heartbeat"

        # close handshake: echo of the code, then EOF and the seat is freed
        writers[0].write(_client_frame((1000).to_bytes(2, "big"), op=0x8))
        await writers[0].drain()
        op, data = await asyncio.wait_for(_read_server_frame(readers[0]), timeout=5.0)
        assert op == 0x8 and data == (1000).to_bytes(2, "big")
        assert await asyncio.wait_for(readers[0].read(), timeout=5.0) == b""
        for _ in range(50):
            if len(door.room.members) == 1:
                break
            await asyncio.sleep(0.02)
        assert len(door.room.members) == 1  # socket closed: no expiry ghost

        # the surviving socket still receives ticks after the other left
        door.publish(encode({"op": "tick", "n": 3}))
        op, data = await asyncio.wait_for(_read_server_frame(readers[1]), timeout=5.0)
        assert op == 0x1 and b'"n":3' in data

        writers[0].close()
        writers[1].close()
        await door.stop()
        assert door.room.stats()["members"] == 0

    asyncio.run(scenario())


# ------------------------------------------- RFC6455 5.1 mask law (Q22) ----

def test_ws_unmasked_client_frame_fails_1002_strict_default():
    async def scenario():
        door = WsDoor()  # strict default: no leniency flag
        await door.start("127.0.0.1", 0)
        reader, writer = await _ws_member(door)

        # an UNMASKED client text frame: the door fails the connection per
        # RFC6455 5.1, answering close 1002 (7.4.1) then EOF
        writer.write(_client_frame_unmasked(b'{"id":"raw"}'))
        await writer.drain()
        op, data = await asyncio.wait_for(_read_server_frame(reader), timeout=5.0)
        assert op == 0x8 and data == CLOSE_PROTOCOL_ERROR.to_bytes(2, "big")
        assert await asyncio.wait_for(reader.read(), timeout=5.0) == b""

        # the seat is freed: no expiry ghost after a protocol failure
        for _ in range(50):
            if len(door.room.members) == 0:
                break
            await asyncio.sleep(0.02)
        assert len(door.room.members) == 0

        writer.close()
        await door.stop()

    asyncio.run(scenario())


def test_ws_masked_frame_accepted_on_strict_door():
    async def scenario():
        door = WsDoor()  # same strict default as the 1002 law above
        await door.start("127.0.0.1", 0)
        reader, writer = await _ws_member(door)

        # a MASKED presence frame is accepted exactly as before the 5.1 fix:
        # meta lands, presence is touched, no close frame comes back
        writer.write(_client_frame(b'{"id":"ada","name":"Ada"}'))
        await writer.drain()
        seen_meta = False
        for _ in range(50):
            rows = door.room.presence()
            if any(m.get("id") == "ada" and m.get("name") == "Ada"
                   for m in rows.values()):
                seen_meta = True
                break
            await asyncio.sleep(0.02)
        assert seen_meta is True
        assert len(door.room.members) == 1  # still seated, not failed

        # and the door still answers a masked ping: the strict mask check
        # did not disturb the control-frame paths
        writer.write(_client_frame(b"hb", op=0x9))
        await writer.drain()
        op, data = await asyncio.wait_for(_read_server_frame(reader), timeout=5.0)
        assert op == 0xA and data == b"hb"

        writer.close()
        await door.stop()

    asyncio.run(scenario())


def test_ws_lenient_flag_accepts_unmasked_frame():
    async def scenario():
        # the v0 mud_relay-parity leniency as an opt-in (the estate's
        # allow_plaintext_hello flag shape): unmasked frames tolerated again
        door = WsDoor(allow_unmasked_client=True)
        await door.start("127.0.0.1", 0)
        reader, writer = await _ws_member(door)

        # the same unmasked text frame the strict door 1002'd is now read
        # with the zero mask: meta lands, the member stays seated
        writer.write(_client_frame_unmasked(b'{"id":"raw","name":"Raw"}'))
        await writer.drain()
        seen_meta = False
        for _ in range(50):
            rows = door.room.presence()
            if any(m.get("id") == "raw" and m.get("name") == "Raw"
                   for m in rows.values()):
                seen_meta = True
                break
            await asyncio.sleep(0.02)
        assert seen_meta is True
        assert len(door.room.members) == 1

        # an unmasked ping is ponged too: the flag covers every opcode
        writer.write(_client_frame_unmasked(b"hb", op=0x9))
        await writer.drain()
        op, data = await asyncio.wait_for(_read_server_frame(reader), timeout=5.0)
        assert op == 0xA and data == b"hb"

        writer.close()
        await door.stop()

    asyncio.run(scenario())
