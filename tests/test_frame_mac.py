"""Frame-MAC tests (R3, 2026-09-30): the Q03 kill landed on OUR wire.

The certification strategy mirrors tests/test_auth_srp6.py: the CLIENT
side of every handshake here is tools.realmd_client.client_session itself
(the math wire-verified against the live realmd), and the client-side
MAC keys derive from the SAME handshake material the server stashed --
so a passing roundtrip means both ends of the wire derive identical keys
from the same (K, A, B) and agree on every tag.

Laws under test:
    roundtrip      srp_proof arms the session; MAC-bearing actions ack;
                   direct replies ride sealed s2c and verify client-side;
                   broadcast ticks stay bare (the encode-once law)
    flipped byte   one flipped byte in a sealed frame = BAD_MAC +
                   disconnect + a kind:mac_tamper row in the world chain
    replay         a resent frame (same seq, valid tag) = BAD_MAC +
                   disconnect + chain row -- and BAD_MAC beats the nonce
                   gate, proving the MAC gate runs FIRST
    no-MAC flag    require_frame_mac=False (default): an old SRP6 client
                   sending bare frames keeps working (migration, not
                   breakage), integrity "none"; True: the first bare
                   frame after proof is tamper
    sticky         once a session sent one valid MAC-bearing frame, a
                   bare frame is a downgrade attempt: tamper, flag or not
    unit falsifiers (the V2ASK1 F3 list, adapted to the hmac-field law)
                   every single-bit body flip, every tag flip, reflection
                   (dir is in the MAC), cross-session splice, seq gap,
                   shape refusals, derive determinism/uniqueness
    table law      BAD_MAC rides a NEW contract version's transport
                   vocabulary; DEFAULT and PROTOCOL_DIGEST unmoved
"""
from __future__ import annotations

import asyncio
import secrets
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tools.realmd_client as rc  # noqa: E402
from server import frame_mac  # noqa: E402
from server.auth import AuthStore  # noqa: E402
from server.auth_srp6 import Srp6AuthService, SrpStore  # noqa: E402
from server.protocol import (  # noqa: E402
    MAC_FIELD,
    MAC_SEQ_FIELD,
    encode,
    with_mac,
)
from server.protocol_table import (  # noqa: E402
    DEFAULT_TABLE,
)
from server.server import Client, WorldServer  # noqa: E402

SALT = bytes(range(1, 33))  # the same fixed salt as the realmd golden vectors
# R5 (2026-09-30, sibling lane) made rfc5054-2048 the default dialect; the
# MAC lane is dialect-agnostic (it keys on the wire hex A/B and K, which
# both ends hold identically whatever math minted them). These tests drive
# the handshake with the proven realmd CLIENT math, so the account rides
# the mangos-256 compat dialect R5 keeps alive for exactly this differential.
MAC_TEST_GROUP = "mangos-256"


async def _start_server(tmp_path: Path, *, require_frame_mac: bool = False,
                        register: tuple[str, str] | None = ("ada", "steam"),
                        ) -> WorldServer:
    auth = AuthStore(tmp_path / "users.json")
    auth.ensure_user("ada", "steam")
    svc = Srp6AuthService(SrpStore(tmp_path / "srp_users.json"))
    if register is not None:
        svc.register(*register, salt=SALT, group=MAC_TEST_GROUP)
    srv = WorldServer(
        port=0, tick_interval=None, auth=auth, srp_auth=svc,
        require_frame_mac=require_frame_mac,
        log_path=tmp_path / "world_log.jsonl",
    )
    return await srv.start()


class MacClient:
    """Drives the SRP6 handshake with the PROVEN client math, then speaks
    the R3 MAC dialect: derives the session's FrameKeys from the same
    (K, A, B) the server saw and seals/verifies frames with them."""

    def __init__(self, client: Client):
        self.client = client
        self.keys: frame_mac.FrameKeys | None = None
        self.seq = 0  # next c2s seq to seal with
        self.welcome: dict | None = None

    async def login(self, user: str, password: str) -> dict:
        a_secret = secrets.randbits(256)
        a_int = pow(rc.G, a_secret, rc.N)
        await self.client.send({"op": "srp_challenge", "user": user,
                                "a": f"{a_int:x}"})
        reply = await self.client.recv()
        assert reply["op"] == "srp_challenge", reply
        b_int = int(reply["b"], 16)
        salt_le = int(reply["salt"], 16).to_bytes(32, "little")
        ch = rc.Challenge(b_int=b_int, g_int=rc.G, n_int=rc.N,
                          salt_le=salt_le, version_challenge=b"",
                          security_flags=0)
        sess = rc.client_session(user, password, ch, a_secret=a_secret)
        await self.client.send({"op": "srp_proof", "user": user,
                                "m1": sess["m1"].hex()})
        self.welcome = await self.client.recv()
        assert self.welcome["op"] == "welcome", self.welcome
        # the client-side twin of server.py's derive_from_wire: same K,
        # same publics, same little-endian operand law -> same keys
        self.keys = frame_mac.derive_from_wire(
            sess["session_key"].hex(), f"{a_int:x}", f"{b_int:x}")
        self.seq = 0
        return self.welcome

    def action(self, sid: str, verb: str, target: str, n: int) -> dict:
        """One sealed action at the client's next seq."""
        frame = with_mac({"op": "action", "sid": sid, "verb": verb,
                          "target": target, "n": n}, self.keys, self.seq)
        self.seq += 1
        return frame

    async def send_sealed(self, frame: dict) -> None:
        await self.client.send(frame)

    async def expect_dead(self, why: str) -> dict:
        """Read the terminal reject, then prove the server disconnected."""
        reply = await self.client.recv()
        assert reply["op"] == "reject" and reply["why"] == why, reply
        with pytest.raises(ConnectionError):
            await self.client.recv()  # EOF: tamper = disconnect
        return reply


def _tamper_rows(srv: WorldServer) -> list[dict]:
    return [r for r in srv.rooms.default_room.world.rows
            if r["kind"] == "mac_tamper"]


# ------------------------------------------------------------------ unit ----


def _unit_keys(seed: int = 1) -> frame_mac.FrameKeys:
    return frame_mac.derive(bytes([seed]) * 40,
                            rc.le_min(0xA1B2 + seed), rc.le_min(0xC3D4))


def test_derive_is_deterministic_directional_and_session_unique():
    k1, k2 = _unit_keys(1), _unit_keys(1)
    assert k1 == k2                                   # same handshake, same keys
    assert k1.k_c2s != k1.k_s2c                       # directions never share
    assert len(k1.mac_id) == 16 and k1.mac_id_hex == k1.mac_id.hex()
    # a fresh b (a different handshake) mints different keys: spliced
    # frames cannot verify across sessions
    assert _unit_keys(1) != _unit_keys(2)
    # the wire wrapper agrees with the raw-bytes core
    k = frame_mac.derive(bytes(range(40)), rc.le_min(7), rc.le_min(9))
    kw = frame_mac.derive_from_wire(bytes(range(40)).hex(), "7", "9")
    assert k == kw


def test_check_rejects_every_single_bit_flip_in_the_body():
    """F3.1 adapted: for every byte position and every one of 8 bit flips
    in the canonical body, the tag must change -- i.e. NO single-bit
    alteration of the body verifies under the original tag. (A wire-line
    flip that survives JSON parsing becomes exactly this altered body;
    one that breaks parsing dies at decode as BAD_JSON -- both paths are
    exercised over the wire in the tests below.)"""
    keys = _unit_keys()
    frame = frame_mac.seal(keys, frame_mac.C2S,
                           {"op": "action", "sid": "s", "verb": "boil",
                            "target": "spring"}, 0)
    body = frame_mac.frame_body(frame)
    tag = bytes.fromhex(frame["mac"])
    frame_mac.check(keys, frame_mac.C2S, 0, frame)  # the untouched frame passes
    for pos in range(len(body)):
        for bit in range(8):
            flipped = bytearray(body)
            flipped[pos] ^= 1 << bit
            assert frame_mac.compute_tag(
                keys, frame_mac.C2S, bytes(flipped)) != tag
    # and field-level forgeries through check(): altered target/sid/n with
    # the original tag replayed -- all TAG failures
    for forged in ({"op": "action", "sid": "s", "verb": "boil",
                    "target": "sprint", "seq": 0, "mac": frame["mac"]},
                   {"op": "action", "sid": "other-sid", "verb": "boil",
                    "target": "spring", "seq": 0, "mac": frame["mac"]},
                   {"op": "action", "sid": "s", "verb": "tag",
                    "target": "spring", "seq": 0, "mac": frame["mac"]}):
        with pytest.raises(frame_mac.MacError, match="TAG"):
            frame_mac.check(keys, frame_mac.C2S, 0, forged)


def test_check_rejects_every_tag_flip():
    keys = _unit_keys()
    frame = frame_mac.seal(keys, frame_mac.C2S, {"op": "action"}, 0)
    tag = frame["mac"]
    for pos in range(len(tag)):
        c = tag[pos]
        swapped = "0" if c != "0" else "1"  # any different hex char
        broken = dict(frame)
        broken["mac"] = tag[:pos] + swapped + tag[pos + 1:]
        with pytest.raises(frame_mac.MacError, match="TAG"):
            frame_mac.check(keys, frame_mac.C2S, 0, broken)


def test_reflection_rejected_direction_is_in_the_mac():
    """F3.3: a server->client frame fed back as client->server must fail."""
    keys = _unit_keys()
    reflected = frame_mac.seal(keys, frame_mac.S2C,
                               {"op": "ack", "verb": "boil"}, 0)
    with pytest.raises(frame_mac.MacError):
        frame_mac.check(keys, frame_mac.C2S, 0, reflected)


def test_cross_session_splice_rejected():
    """F3.4: a frame sealed under session X's keys fails under session Y's."""
    x, y = _unit_keys(1), _unit_keys(2)
    frame = frame_mac.seal(x, frame_mac.C2S, {"op": "action", "n": 1}, 0)
    with pytest.raises(frame_mac.MacError, match="TAG"):
        frame_mac.check(y, frame_mac.C2S, 0, frame)


def test_seq_law_gap_and_shapes():
    keys = _unit_keys()
    # a VALID tag over seq 1 still rejects while 0 is expected: the seq
    # is inside the MACed body, and the receiver law is exact-order
    frame1 = frame_mac.seal(keys, frame_mac.C2S, {"op": "action"}, 1)
    with pytest.raises(frame_mac.MacError, match="SEQ"):
        frame_mac.check(keys, frame_mac.C2S, 0, frame1)
    # shape refusals: bool seq (a verdict, not an id), missing/malformed
    # mac field, negative seq
    ok = frame_mac.seal(keys, frame_mac.C2S, {"op": "action"}, 0)
    for bad in ({"op": "action", "seq": True, "mac": ok["mac"]},
                {"op": "action", "seq": 0},
                {"op": "action", "seq": 0, "mac": "zz"},
                {"op": "action", "seq": 0, "mac": 5},
                {"op": "action", "seq": -1, "mac": ok["mac"]}):
        with pytest.raises(frame_mac.MacError, match="SHAPE"):
            frame_mac.check(keys, frame_mac.C2S, 0, bad)
    # and after a valid frame the counter advances: a replay of seq 0
    # is now a SEQ failure even with its still-valid tag
    with pytest.raises(frame_mac.MacError, match="SEQ"):
        frame_mac.check(keys, frame_mac.C2S, 1, ok)


def test_admit_law_migration_sticky_and_flag():
    keys = _unit_keys()
    # migration window (require off): bare frames pass, integrity stays none
    st = frame_mac.FrameMacState(keys)
    assert st.admit({"op": "action", "sid": "s"}) is None
    assert st.integrity == "none"
    # require on: a bare frame from an armed session is tamper
    st_req = frame_mac.FrameMacState(keys)
    assert st_req.admit({"op": "action", "sid": "s"}, require=True) == "BAD_MAC"
    # a malformed mac field is tamper whichever way the flag sits
    assert st.admit({"op": "action", "seq": 0, "mac": "nothex"}) == "BAD_MAC"
    # a valid MAC-bearing frame opts the session in (sticky)
    sealed = frame_mac.seal(keys, frame_mac.C2S, {"op": "action"}, 0)
    assert st.admit(sealed) is None
    assert st.integrity == "mac1" and st.expected_seq == 1
    # never downgrade: a bare frame from a sticky session is tamper
    assert st.admit({"op": "action", "sid": "s"}) == "BAD_MAC"
    # replay of the same sealed frame: SEQ mismatch -> tamper
    assert st.admit(sealed) == "BAD_MAC"


def test_table_law_bad_mac_is_a_new_contract_not_an_edit():
    from server.protocol_table import PROTOCOL_DIGEST, compile_table
    assert frame_mac.FRAME_MAC_TABLE.transport_reject_codes == \
        DEFAULT_TABLE.transport_reject_codes + ("BAD_MAC",)
    assert frame_mac.FRAME_MAC_TABLE.rows == DEFAULT_TABLE.rows
    assert "BAD_MAC" not in DEFAULT_TABLE.transport_reject_codes
    assert frame_mac.FRAME_MAC_TABLE.digest == frame_mac.FRAME_MAC_DIGEST
    # DEFAULT is byte-identical and untouched: digest pinned
    assert compile_table(None).digest == PROTOCOL_DIGEST


def test_protocol_with_mac_is_the_seal_sugar():
    keys = _unit_keys()
    msg = {"op": "action", "sid": "s", "verb": "tag", "target": "spring"}
    frame = with_mac(msg, keys, 3)
    assert frame == frame_mac.seal(keys, frame_mac.C2S, msg, 3)
    assert set(frame) - set(msg) == {MAC_SEQ_FIELD, MAC_FIELD}
    frame_mac.check(keys, frame_mac.C2S, 3, frame)  # and it verifies


# ---------------------------------------------------------- wire: TCP laws ----


def test_mac_roundtrip_over_the_wire(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = MacClient(await Client.connect("127.0.0.1", srv.bound_port))
        w = await c.login("ada", "steam")
        sid = w["sid"]
        # the welcome itself rides sealed (s2c seq 0): the server proving
        # it holds K by MACing IS the capability announcement
        assert MAC_FIELD in w and w[MAC_SEQ_FIELD] == 0
        frame_mac.check(c.keys, frame_mac.S2C, 0, w)
        # sealed action seq 0 -> ack sealed s2c seq 1, verifiable client-side
        await c.send_sealed(c.action(sid, "boil", "spring", 1))
        ack = await c.client.recv()
        assert ack["op"] == "ack" and ack["user"] == "ADA"
        frame_mac.check(c.keys, frame_mac.S2C, 1, ack)
        # the session went MAC-sticky; the world applied the sealed move
        assert srv.stats()["mac_sessions"] == 1
        await srv.pump_once()
        tick = await c.client.recv()
        assert tick["op"] == "tick" and "ADA boils 1 at spring" in \
            " | ".join(tick["events"])
        assert MAC_FIELD not in tick  # broadcast ticks stay bare (encode-once)
        # seq 1 carries the next move (counter advanced on both sides);
        # one acked action per tick bucket, so pump between them
        await c.send_sealed(c.action(sid, "boil", "spring", 2))
        assert (await c.client.recv())["op"] == "ack"
        await srv.pump_once()
        assert (await c.client.recv())["op"] == "tick"
        # a non-JSON line is still BAD_JSON, not tamper: decode precedes
        # the MAC gate (an unparseable line carries nothing to verify)
        c.client.writer.write(b"this is not json\n")
        await c.client.writer.drain()
        rj = await c.client.recv()
        assert rj["op"] == "reject" and rj["why"] == "BAD_JSON"
        await c.send_sealed(c.action(sid, "boil", "spring", 3))  # still alive
        assert (await c.client.recv())["op"] == "ack"
        assert srv.stats()["mac_tampers"] == 0
        c.client.close()
        await srv.stop()

    asyncio.run(scenario())


def test_flipped_byte_rejected_disconnect_and_chained(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = MacClient(await Client.connect("127.0.0.1", srv.bound_port))
        w = await c.login("ada", "steam")
        line = encode(c.action(w["sid"], "boil", "spring", 1))
        # THE ATTACK: one flipped byte reattributing the move -- boil
        # becomes boik, the sid/verb/n all still parse, only the author's
        # intent is forged. The tag refuses it.
        tampered = line.replace(b'"boil"', b'"boik"')
        assert tampered != line
        c.client.writer.write(tampered)
        await c.client.writer.drain()
        await c.expect_dead("BAD_MAC")
        # the chain event: one mac_tamper row, user-bound, chain still valid
        rows = _tamper_rows(srv)
        assert len(rows) == 1
        assert rows[0]["user"] == "ADA" and rows[0]["sid"] == w["sid"]
        assert rows[0]["code"] == "BAD_MAC"
        assert rows[0]["integrity"] == "none"  # it never got to go sticky
        assert srv.rooms.default_room.world.verify_log() is True
        # the row is durable: the on-disk log carries it and still verifies
        from server.world import load_log_rows
        disk = load_log_rows(tmp_path / "world_log.jsonl")
        assert any(r["kind"] == "mac_tamper" for r in disk)
        assert srv.stats()["mac_tampers"] == 1
        await srv.stop()

    asyncio.run(scenario())


def test_replay_rejected_mac_gate_beats_the_nonce_gate(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = MacClient(await Client.connect("127.0.0.1", srv.bound_port))
        w = await c.login("ada", "steam")
        frame = c.action(w["sid"], "tag", "spring", 1)
        line = encode(frame)
        c.client.writer.write(line)  # the original: acked
        await c.client.writer.drain()
        assert (await c.client.recv())["op"] == "ack"
        # THE ATTACK: the exact same bytes again. The frame carries 'n': 1,
        # so the nonce gate alone would say STALE_NONCE -- BAD_MAC instead
        # PROVES the MAC gate ran first (verify before processing).
        c.client.writer.write(line)
        await c.client.writer.drain()
        await c.expect_dead("BAD_MAC")
        rows = _tamper_rows(srv)
        assert len(rows) == 1 and rows[0]["code"] == "BAD_MAC"
        assert rows[0]["integrity"] == "mac1"  # the session WAS MAC-bound
        assert srv.stats()["mac_tampers"] == 1
        await srv.stop()

    asyncio.run(scenario())


def test_reflection_over_the_wire(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        c = MacClient(await Client.connect("127.0.0.1", srv.bound_port))
        w = await c.login("ada", "steam")
        # THE ATTACK: feed the server's own sealed welcome back to it. The
        # seq even matches (0), but the tag was minted under k_s2c.
        c.client.writer.write(encode(w))
        await c.client.writer.drain()
        await c.expect_dead("BAD_MAC")
        assert len(_tamper_rows(srv)) == 1
        await srv.stop()

    asyncio.run(scenario())


def test_no_mac_client_on_the_flag_path(tmp_path):
    """The migration law: old clients without MACs keep working while the
    flag is off; the flag closes the bare window without touching the
    pre-auth handshake (challenge/proof were always bare)."""
    async def scenario():
        # flag OFF (default): an old SRP6 client never sends mac fields.
        # It logs in, acts, ticks -- byte-compat behavior, integrity none.
        srv = await _start_server(tmp_path)
        old = MacClient(await Client.connect("127.0.0.1", srv.bound_port))
        w = await old.login("ada", "steam")
        await old.client.send({"op": "action", "sid": w["sid"],
                               "verb": "boil", "target": "spring", "n": 1})
        ack = await old.client.recv()
        assert ack["op"] == "ack"
        await srv.pump_once()
        assert (await old.client.recv())["op"] == "tick"
        assert srv.stats()["mac_sessions"] == 0  # never went MAC-sticky
        assert srv.stats()["mac_tampers"] == 0
        old.client.close()
        await srv.stop()

        # flag ON: the first bare frame after srp_proof is tamper
        srv2 = await _start_server(tmp_path / "strict", require_frame_mac=True)
        c2 = MacClient(await Client.connect("127.0.0.1", srv2.bound_port))
        w2 = await c2.login("ada", "steam")  # handshake itself stays bare
        assert w2["op"] == "welcome"
        await c2.client.send({"op": "action", "sid": w2["sid"],
                              "verb": "boil", "target": "spring", "n": 1})
        await c2.expect_dead("BAD_MAC")
        rows = _tamper_rows(srv2)
        assert len(rows) == 1 and rows[0]["code"] == "BAD_MAC"
        assert srv2.stats()["mac_tampers"] == 1
        await srv2.stop()

    asyncio.run(scenario())


def test_sticky_session_never_downgrades_even_on_the_migration_flag(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)  # flag OFF: bare frames are legal
        c = MacClient(await Client.connect("127.0.0.1", srv.bound_port))
        w = await c.login("ada", "steam")
        await c.send_sealed(c.action(w["sid"], "boil", "spring", 1))
        assert (await c.client.recv())["op"] == "ack"  # sticky now
        # THE ATTACK: strip the mac fields off the next frame -- the
        # session already proved MAC capability, so bare is a downgrade
        await c.client.send({"op": "action", "sid": w["sid"], "verb": "boil",
                             "target": "spring", "n": 2})
        await c.expect_dead("BAD_MAC")
        rows = _tamper_rows(srv)
        assert len(rows) == 1 and rows[0]["integrity"] == "mac1"
        await srv.stop()

    asyncio.run(scenario())


def test_plaintext_hello_door_stays_bare(tmp_path):
    """The hello door carries no K, so it can never MAC: its welcome is
    byte-identical v0 (no seq/mac fields), the exact migration promise."""
    async def scenario():
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        w = await c.do_hello("ada", "steam")
        assert w["op"] == "welcome"
        assert MAC_FIELD not in w and MAC_SEQ_FIELD not in w
        assert set(w) == {"op", "sid", "world", "room"}
        await c.send({"op": "action", "sid": w["sid"], "verb": "boil",
                      "target": "spring", "n": 1})
        assert (await c.recv())["op"] == "ack"
        c.close()
        await srv.stop()

    asyncio.run(scenario())
