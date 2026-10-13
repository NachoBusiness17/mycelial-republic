"""B3 netcode v0 tests: Gaffer snapshot interpolation over the live wire.

Laws under test (receipt watch/inbox/last_mile_20260930/B3_NETCODE.md).
The netcode lives in roblox_to_godot/network/ - the empty dir MC3's gap
analysis and ROUTE_COUNTER's "gap row 2 true literally, false in spirit"
named. The estate box still has no Godot binary
(watch/inbox/GODOT_SLICE_20260929.md), so the laws run as a byte-mirrored
Python client against a LIVE in-process WorldServer on an ephemeral port
(the test_server_v0 pattern), and the .gd bytes are pinned structurally
to the same constants (the AC5 mirror law: the mirror may not silently
drift from the bytes):

  - the interpolation layer EXTENDS the existing W1 transport
    (roblox_to_godot/scripts/net_client.gd, byte-identical to
    the-mountain/game/scripts/net_client.gd), it is not a parallel
    client: extends path, tick interception, passthrough for every
    other op
  - NO PREDICTION (ROUTE_COUNTER: "prediction is polish, not
    existence"): send_action stays the inherited passthrough, nothing
    swallows acks or emits compensating ones
  - the buffer fills: 300 live ticks, capacity reached and held
  - NO RUBBER-BAND beyond epsilon: every rendered frame stays inside
    the truth corridor [lo, hi] of the two snapshots it was
    interpolated from, and the render timeline never rewinds
    (bracket tick n is non-decreasing)
  - interpolation RECONCILES with server truth: sampling AT a
    snapshot's stamp returns that snapshot's volumes exactly
    (endpoint identity, zero error), the whole 300-tick run long
  - events/winner deliver EXACTLY ONCE (cursor law equals the
    full-scan law every frame), never interpolated
  - starvation law: a starved render freezes on the newest sample,
    never extrapolates (unit-proven on the mirror)
"""
from __future__ import annotations

import asyncio
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.auth import AuthStore  # noqa: E402
from server.protocol import decode_line, encode  # noqa: E402
from server.server import WorldServer  # noqa: E402

GD_NET = ROOT / "roblox_to_godot" / "network"
SNAP_GD = GD_NET / "snapshot_buffer.gd"
NET_GD = GD_NET / "net_client.gd"
TRANSPORT_GD = ROOT / "roblox_to_godot" / "scripts" / "net_client.gd"
GAME_GD = ROOT / "roblox_to_godot" / "scripts" / "game.gd"

INTERP_DELAY_S = 0.100
CAPACITY = 32
EPS = 1.0e-6
BOIL_ORDER = ("spring", "terrace", "gate1", "hollow")


# --------------------------------------------------------------- mirror ----

class SnapBuffer:
    """Byte-mirror of network/snapshot_buffer.gd: same laws, same names,
    so a drift between these bytes and those bytes is visible in review."""

    CAPACITY = 32

    def __init__(self) -> None:
        self.snaps: list[dict] = []

    def push(self, n: int, t: float, nodes: dict, events: list, winner: bool) -> bool:
        # Law 1: the ring only moves forward (stale/duplicate refuses).
        if self.snaps and n <= self.snaps[-1]["n"]:
            return False
        self.snaps.append({"n": n, "t": t, "nodes": dict(nodes),
                           "events": list(events), "winner": bool(winner)})
        if len(self.snaps) > self.CAPACITY:
            self.snaps.pop(0)
        return True

    def size(self) -> int:
        return len(self.snaps)

    def sample(self, render_t: float) -> dict | None:
        # Laws 2+3: interpolate between brackets, clamp inside the window.
        if len(self.snaps) < 2:
            return None
        rt = min(max(render_t, self.snaps[0]["t"]), self.snaps[-1]["t"])
        hi = 1
        while hi < len(self.snaps) and self.snaps[hi]["t"] < rt:
            hi += 1
        if hi >= len(self.snaps):
            hi = len(self.snaps) - 1
        a, b = self.snaps[hi - 1], self.snaps[hi]
        span = b["t"] - a["t"]
        frac = 0.0 if span <= 0 else (rt - a["t"]) / span
        nodes = {k: float(a["nodes"].get(k, 0))
                 + (float(b["nodes"].get(k, 0)) - float(a["nodes"].get(k, 0))) * frac
                 for k in b["nodes"]}
        return {"n": a["n"], "hi_n": b["n"], "frac": frac, "nodes": nodes,
                "lo_nodes": a["nodes"], "hi_nodes": b["nodes"]}

    def crossed(self, render_t: float, cursor_n: int) -> dict:
        # Law 4: exactly-once side channels, UNCLAMPED render clock.
        events: list = []
        winner = False
        high = cursor_n
        for s in self.snaps:
            if s["n"] > cursor_n and s["t"] <= render_t:
                events.extend(s["events"])
                winner = winner or s["winner"]
                high = max(high, s["n"])
        return {"n": high, "events": events, "winner": winner}


class InterpClient:
    """Byte-mirror of network/net_client.gd: the interpolation layer on
    the transport. NO PREDICTION - actions are sent and forgotten, the
    rendered world is pure interpolated server truth."""

    INTERP_DELAY_S = 0.100

    def __init__(self) -> None:
        self.buf = SnapBuffer()
        self.truth: dict[str, int] = {}
        self.events_cursor_n = 0
        self.winner_emitted = False
        # law counters (mirror net_client.gd stats())
        self.render_frames = 0
        self.rubber_band_frames = 0
        self.max_truth_error = 0.0
        self.events_delivered = 0
        self.winner_fired = 0
        self.acks_seen = 0
        self.rejects_seen: list[str] = []
        self.emitted_frames: list[dict] = []

    async def send(self, writer: asyncio.StreamWriter, sid: str,
                   verb: str, target: str) -> None:
        # The inherited passthrough: send and forget, predict nothing.
        writer.write(encode({"op": "action", "sid": sid, "verb": verb,
                             "target": target}))
        await writer.drain()

    def on_line(self, msg: dict) -> None:
        # Passthrough ops (ack/reject) ride the base signals; the mirror
        # only counts them.
        if msg.get("op") == "ack":
            self.acks_seen += 1
        elif msg.get("op") == "reject":
            self.rejects_seen.append(str(msg.get("why", "")))

    def feed_tick(self, msg: dict, t: float) -> None:
        self.buf.push(int(msg.get("n", 0)), t, msg.get("nodes", {}),
                      msg.get("events", []), bool(msg.get("winner", False)))
        self.truth = dict(msg.get("nodes", {}))

    def render(self, now: float) -> dict | None:
        # The _process render step: sample at now - 100ms, envelope-law
        # check, exactly-once side channels, re-emit ticked.
        rt = now - self.INTERP_DELAY_S
        frame = self.buf.sample(rt)
        if frame is None:
            return None
        for name, v in frame["nodes"].items():
            va = float(frame["lo_nodes"].get(name, 0))
            vb = float(frame["hi_nodes"].get(name, 0))
            floor_v, ceil_v = min(va, vb), max(va, vb)
            if v < floor_v - EPS or v > ceil_v + EPS:
                self.rubber_band_frames += 1
                self.max_truth_error = max(self.max_truth_error,
                                           max(floor_v - v, v - ceil_v))
        crossed = self.buf.crossed(rt, self.events_cursor_n)
        self.events_cursor_n = crossed["n"]
        self.events_delivered += len(crossed["events"])
        winner = False
        if crossed["winner"] and not self.winner_emitted:
            self.winner_emitted = True
            winner = True
            self.winner_fired += 1
        self.render_frames += 1
        emitted = {"n": frame["n"], "nodes": frame["nodes"], "events": crossed["events"],
                   "winner": winner, "rt": rt}
        self.emitted_frames.append(emitted)
        return emitted


# ------------------------------------------------------ .gd byte pins ----

def test_netcode_files_carry_the_laws():
    snap = SNAP_GD.read_text(encoding="utf-8")
    net = NET_GD.read_text(encoding="utf-8")
    game = GAME_GD.read_text(encoding="utf-8")

    # The buffer: pure RefCounted ring, capacity law, clamp law.
    assert snap.lstrip().startswith("extends RefCounted")
    assert "const CAPACITY := 32" in snap
    assert "clampf" in snap  # the no-extrapolation freeze law
    assert "func push" in snap and "func sample(" in snap and "func crossed(" in snap

    # The client: an EXTENSION of the existing transport, not a parallel one.
    assert net.lstrip().startswith('extends "res://scripts/net_client.gd"')
    assert TRANSPORT_GD.exists()  # the extended bytes are the-mountain's client
    assert "const SnapshotBuffer := preload(\"res://network/snapshot_buffer.gd\")" in net
    assert "const INTERP_DELAY_MS := 100" in net  # the Gaffer t-100ms delay
    assert "super._process(delta)" in net
    assert "super._handle_line(text)" in net  # every non-tick op passes through
    assert '"tick"' in net  # the one intercepted op
    assert "ticked.emit(" in net  # re-emitted on the render clock, interpolated
    assert "rubber_band_frames" in net and "max_truth_error" in net

    # NO PREDICTION (ROUTE_COUNTER): send_action stays inherited, no ack
    # swallowing, no compensating acks, no delta staging.
    assert "func send_action" not in net
    assert "acked.emit" not in net
    assert "_pred" not in net

    # Clock law: no wall clock anywhere in the netcode (delta-accumulated).
    for text in (snap, net):
        assert "Time.get_" not in text
        assert "OS.get_ticks" not in text

    # Em-dash law (house): zero in both authored files.
    assert "\u2014" not in snap and "\u2014" not in net

    # The switch is wired: game.gd preloads the interpolation layer.
    assert 'const NetClient := preload("res://network/net_client.gd")' in game


# ------------------------------------------------- mirror unit laws ----

def test_snapshot_buffer_mirror_unit_laws():
    b = SnapBuffer()
    assert b.sample(0.0) is None  # fewer than two truths: no render yet
    assert b.push(1, 0.0, {"a": 0, "b": 6}, ["e1"], False)
    assert b.push(2, 1.0, {"a": 10, "b": 6}, ["e2"], False)

    mid = b.sample(0.5)
    assert mid is not None
    assert mid["nodes"]["a"] == pytest.approx(5.0)
    assert mid["nodes"]["b"] == pytest.approx(6.0)
    assert mid["frac"] == pytest.approx(0.5)

    # Endpoint identity (the reconcile law): AT a stamp, the exact truth.
    at_hi = b.sample(1.0)
    assert at_hi is not None and at_hi["nodes"]["a"] == pytest.approx(10.0)
    at_lo = b.sample(0.0)
    assert at_lo is not None and at_lo["nodes"]["a"] == pytest.approx(0.0)

    # No extrapolation: both ends freeze instead of guessing.
    future = b.sample(600.0)
    assert future is not None and future["nodes"]["a"] == pytest.approx(10.0)
    past = b.sample(-600.0)
    assert past is not None and past["nodes"]["a"] == pytest.approx(0.0)

    # Stale/duplicate ticks never enter (render timeline stays monotone).
    assert b.push(2, 2.0, {"a": 99, "b": 99}, [], False) is False
    assert b.push(1, 3.0, {"a": 99, "b": 99}, [], False) is False
    assert b.sample(1.5) is not None

    # Capacity: the ring trims to CAPACITY, keeps the NEWEST truths.
    for i in range(3, 45):
        assert b.push(i, float(i), {"a": i, "b": 0}, [], False)
    assert b.size() == CAPACITY
    newest = b.sample(float(600))
    assert newest is not None and newest["nodes"]["a"] == pytest.approx(44.0)

    # Exactly-once side channels: the cursor advances, nothing reships.
    # (The ring holds n 13..44 now; the render clock at t=40 has passed
    # every snapshot up to n=40, and nothing past it.)
    c1 = b.crossed(float(40), 0)
    assert c1["n"] == 40
    c2 = b.crossed(float(40), c1["n"])
    assert c2["events"] == [] and c2["winner"] is False
    c3 = b.crossed(float(44.5), c1["n"])
    assert c3["n"] == 44


def test_starved_render_freezes_never_extrapolates():
    b = SnapBuffer()
    b.push(1, 0.0, {"a": 3}, [], False)
    b.push(2, 1.0, {"a": 7}, [], False)
    starved = b.sample(10.0)  # render far past the newest truth
    assert starved is not None
    assert starved["nodes"]["a"] == pytest.approx(7.0)  # frozen, not guessed
    assert starved["frac"] == pytest.approx(1.0)


def test_draining_node_renders_inside_its_corridor():
    # Fix pin (first live run): a node whose volume DECREASES between
    # brackets (the mountain drains) interpolates downward; the envelope
    # law must read the per-node min/max corridor, not
    # lower-snapshot/upper-snapshot, or every drain reads as a phantom
    # rubber-band.
    nc = InterpClient()
    nc.feed_tick({"op": "tick", "n": 1, "nodes": {"spring": 6, "waste": 0},
                  "events": [], "winner": False}, 0.0)
    nc.feed_tick({"op": "tick", "n": 2, "nodes": {"spring": 5, "waste": 1},
                  "events": [], "winner": False}, 1.0)
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0, 0.5):  # both directions
        frame = nc.render(0.0 + nc.INTERP_DELAY_S + frac)
        assert frame is not None
        assert frame["nodes"]["spring"] == pytest.approx(6.0 - frac)
        assert frame["nodes"]["waste"] == pytest.approx(frac)
    assert nc.rubber_band_frames == 0
    assert nc.max_truth_error == 0.0


# ------------------------------------------------------- the live run ----

def _wettest(truth: dict[str, int]) -> str:
    best, best_v = "", 0
    for name in BOIL_ORDER:
        v = int(truth.get(name, 0))
        if v > best_v:
            best, best_v = name, v
    return best


def _ledger_due(ledger: list[tuple], rt: float) -> int:
    # Independent oracle for "events the render clock has passed": every
    # tick ever received (n, stamp, events), NEVER trimmed - unlike the
    # ring, whose CAPACITY trims old snapshots, so the ring's own
    # contents are not a valid oracle once trimming starts.
    return sum(len(evs) for (_, t, evs) in ledger if t <= rt)


def _ledger_cursor(ledger: list[tuple], rt: float) -> int:
    # The cursor truth: the highest tick number whose stamp the render
    # clock has passed, over all history. A ring that trimmed a snapshot
    # before the render clock crossed it would strand its events and
    # fall behind this (capacity 32 vs ~6 ticks of 100ms lag: never).
    return max((n for (n, t, _) in ledger if t <= rt), default=0)


def test_live_300_ticks_interpolation_no_rubberband():
    asyncio.run(_live_scenario())


async def _live_scenario(ticks: int = 300, cadence: float = 0.02) -> None:
    tmp = Path(tempfile.mkdtemp(prefix="b3_netcode_"))
    auth = AuthStore(tmp / "users.json")
    auth.ensure_user("ada", "steam")
    srv = WorldServer(port=0, tick_interval=None, auth=auth,
                      log_path=tmp / "world.jsonl")
    await srv.start()
    try:
        reader, writer = await asyncio.open_connection(
            "127.0.0.1", srv.bound_port, limit=65536)
        writer.write(encode({"op": "hello", "user": "ada", "pass": "steam"}))
        await writer.drain()
        welcome = decode_line(await asyncio.wait_for(reader.readline(), 5))
        assert welcome["op"] == "welcome"
        sid = welcome["sid"]

        nc = InterpClient()
        loop = asyncio.get_running_loop()
        max_buffered = 0
        endpoint_errors: list[float] = []
        prev_emitted_n = -1
        ledger: list[tuple] = []  # (n, stamp, events) for every tick received

        for i in range(1, ticks + 1):
            await asyncio.sleep(cadence)
            # Action policy (at most one ask per tick bucket: RATE_CAP is
            # 1 staged action per sid per tick). Exercises the passthrough
            # lanes: acks, DRY_POOL, RATE_CAP, valves, tags. Honest about
            # the world's own law: 8 units total, waste is terminal, so
            # boils go quiet once the mountain drains; VALVES never dry
            # out, so they keep the wire moving across all 300 ticks.
            if i == 3:
                dry = next(n for n in ("terrace", "gate1", "waste", "crown")
                           if nc.truth.get(n, 0) == 0)
                await nc.send(writer, sid, "boil", dry)  # DRY_POOL reject lane
            elif i == 6:
                wet = _wettest(nc.truth)
                await nc.send(writer, sid, "boil", wet)  # acked
                await nc.send(writer, sid, "boil", wet)  # RATE_CAP reject lane
            elif i == 10:
                await nc.send(writer, sid, "valve", "p_bypass")  # acked, opens at 11
            elif i % 25 == 0:
                await nc.send(writer, sid, "valve", "p_out")  # valve lane, never dry
            elif i % 50 == 0:
                wet = _wettest(nc.truth)
                if wet:
                    await nc.send(writer, sid, "tag", wet)  # event/score lane
            elif i % 5 == 0:
                wet = _wettest(nc.truth)
                if wet:
                    await nc.send(writer, sid, "boil", wet)

            await srv.pump_once()
            # Drain replies (ack/reject) then the tick, in wire order.
            while True:
                raw = await asyncio.wait_for(reader.readline(), 5)
                msg = decode_line(raw)
                if msg.get("op") == "tick":
                    break
                nc.on_line(msg)
            stamp = loop.time()
            nc.feed_tick(msg, stamp)
            ledger.append((int(msg.get("n", 0)), stamp, list(msg.get("events", []))))
            max_buffered = max(max_buffered, nc.buf.size())

            # The reconcile identity every tick: sampling AT the stamp the
            # tick just landed returns its volumes exactly (frac clamps to
            # 1.0 at the newest bracket). Skipped on the very first tick:
            # one snapshot is not yet a segment to interpolate.
            at_newest = nc.buf.sample(stamp)
            if at_newest is not None:
                for name, v in msg["nodes"].items():
                    endpoint_errors.append(
                        abs(at_newest["nodes"][name] - float(v)))

            frame = nc.render(stamp)
            if frame is not None:
                # Rubber-band complement: the render timeline never rewinds.
                assert frame["n"] >= prev_emitted_n
                prev_emitted_n = frame["n"]
                # Cursor law vs the never-trimmed ledger oracle, every frame:
                # the cursor reaches exactly the ticks the render clock
                # passed, and exactly those events shipped, exactly once.
                assert nc.events_cursor_n == _ledger_cursor(ledger, frame["rt"])
                assert nc.events_delivered == _ledger_due(ledger, frame["rt"])

        # THE FILLED BUFFER: capacity reached and held over 300 live ticks.
        assert max_buffered == CAPACITY
        assert nc.buf.size() == CAPACITY
        # THE RENDER: it ran, smoothly behind the wire.
        assert nc.render_frames >= ticks - 20
        # NO RUBBER-BAND beyond epsilon: zero corridor exits, zero endpoint
        # error, zero winner double-fires.
        assert nc.rubber_band_frames == 0
        assert nc.max_truth_error == 0.0
        assert max(endpoint_errors, default=0.0) == 0.0
        assert nc.winner_fired <= 1
        if any(s["winner"] for s in nc.buf.snaps) or nc.winner_emitted:
            assert nc.winner_fired == 1  # sticky win delivered exactly once
        # The passthrough lanes all fired: acks (12 valve toggles ride the
        # whole run; boils go quiet when the 8-unit mountain drains, the
        # world's own law) plus the typed rejects.
        assert nc.acks_seen >= 12
        assert "DRY_POOL" in nc.rejects_seen
        assert "RATE_CAP" in nc.rejects_seen
        # The valve really opened server-side (the ack was honest).
        assert srv.world.graph.pipes["p_bypass"].open is True
        # Side channels fully caught up to the final render clock (the
        # ledger oracle, never trimmed).
        assert nc.events_delivered == _ledger_due(ledger, nc.emitted_frames[-1]["rt"])
        assert nc.events_delivered > 0

        writer.close()
    finally:
        await srv.stop()
