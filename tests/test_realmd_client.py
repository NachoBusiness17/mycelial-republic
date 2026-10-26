"""Tests for realmd_client -- SRP6 math on vectors, packet builders as byte shapes, live
handshake when the estate's realmd is up (self-skipping, the test_wow_bones convention).

The math is cross-certified three ways (LW4, 2026-09-30):

  1. DB VECTOR: the v/s pair in the estate's realmd account table (LW4PROBE, id 6, armed
     2026-09-30 via mariadb) was computed by srp6_verifier; reproducing it here ties the
     repo math to the live server's credentials.
  2. GOLDEN VECTOR: fixed a-secret/salt/password produce pinned A, B, S, K40, M1, M2.
     N (894B645E...BB7) and g (7) are the standard WoW 256-bit SRP6 group, and the byte
     order everywhere is little-endian (BigNumber.h:84 AsByteArray(reverse=true)), the
     convention a big-endian textbook SRP6 implementation gets wrong.
  3. SERVER DIFFERENTIAL: the server's own formulas re-implemented here from
     src/shared/SRP6/SRP6.cpp (B=(3v+g^b), S=(A*v^u)^b, K interleave, M1, M2) must agree
     with client_session on every derived value: the algebraic identity is the test.
"""
from __future__ import annotations

import hashlib
import socket
import struct

import pytest

import tools.realmd_client as rc

LIVE = ("127.0.0.1", 3724)


def _sha1(data: bytes) -> bytes:
    return hashlib.sha1(data).digest()


def _le_min(value: int) -> bytes:
    if value == 0:
        return b"\x00"
    return value.to_bytes((value.bit_length() + 7) // 8, "little")


def _realmd_up() -> bool:
    try:
        with socket.create_connection(LIVE, timeout=0.5):
            return True
    except OSError:
        return False


# --- the serialization law: BigNumber::AsByteArray is minimal LITTLE-endian ---------------------


def test_le_min_strips_trailing_zeros_in_little_endian():
    assert rc.le_min(0) == b"\x00"
    assert rc.le_min(7) == b"\x07"
    assert rc.le_min(0x0100) == b"\x00\x01"
    assert rc.le_min(0x00FF00) == b"\x00\xff"  # high-order zero byte dropped, LE order kept
    assert len(rc.le_min(rc.N)) == 32


def test_le_pad_arithmetic_pads_to_size():
    assert rc.le_pad(1, 32) == b"\x01" + b"\x00" * 31
    assert rc.le_pad(rc.N, 32) == rc.N.to_bytes(32, "little")


# --- vector 1: the credentials the live realmd database actually stores ------------------------


def test_verifier_reproduces_the_live_db_pair():
    salt_hex = "7E5C1A94B2F6D38E0A19C5F72B4D3A689F0E2C4D5B6A7980F1E3D2C4B5A6978"
    salt_le = int(salt_hex, 16).to_bytes(32, "little")
    v = rc.srp6_verifier(b"LW4PROBE", b"LASTMILE", salt_le)
    assert f"{v:X}" == "5FCEE9850BA6369681768ED6576550258194DA32D58A54BBB4303BB7F3FD3186"


def test_x_is_hash_then_little_endian_interpretation():
    salt_le = bytes(range(1, 33))
    want = int.from_bytes(_sha1(salt_le + _sha1(b"VECTORONE:GOLDENTEST")), "little")
    assert rc.srp6_x(b"VECTORONE", b"GOLDENTEST", salt_le) == want


# --- vector 2: golden SRP6 outputs, byte-pinned -------------------------------------------------


def _golden_session():
    salt_le = bytes(range(1, 33))
    ch = rc.Challenge(b_int=0, g_int=rc.G, n_int=rc.N, salt_le=salt_le,
                      version_challenge=rc.VERSION_CHALLENGE, security_flags=0)
    # B built server-side from a fixed b-secret (see the differential test for the formula)
    b_secret = 0xFEDCBA9876543210FEDCBA9876543210FEDCBA9876543210FEDCBA9876543210
    x = rc.srp6_x(b"VECTORONE", b"GOLDENTEST", salt_le)
    v = pow(rc.G, x, rc.N)
    ch.b_int = (rc.SRP_K * v + pow(rc.G, b_secret, rc.N)) % rc.N
    a_secret = 0x0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF
    return ch, rc.client_session("VectorOne", "GoldenTest", ch, a_secret=a_secret), ch.b_int


def test_golden_vector_pinned():
    ch, sess, b_int = _golden_session()
    assert b_int == 0x40081FC434A8F00113E567D44C8AF2870AB68735EA1F68844F9432D30F8A750E
    assert sess["a_int"] == 0x4004E0C67C1944273A5A4FB23031526BE2E6AA67D2934E8765582190485CF077
    assert sess["s_int"] == 0x274E0C33242E8871A2051719418E84E8130D2C730AAEE5638B026E2DFFB92D96
    assert sess["session_key"].hex() == (
        "e7f86badc73c15f76971af5088c1d62a6fd17c5b91ebbfcb6ee4057c9f9803339289f21ccfacdad2")
    assert sess["m1"].hex() == "05a2cb2fb5b95d6915d5da776b45d1fcb237c2d0"
    assert sess["m2_expected"].hex() == "ad096dfb8711cae3aa283282a5dbeb9624e2a153"


# --- vector 3: differential against the server's own SRP6.cpp formulas -------------------------


def test_server_side_formulas_agree_with_client_session():
    salt_le = bytes.fromhex("11223344" * 8)
    ident = b"DIFFTWO"  # client_session uppercases both sides before hashing
    x = rc.srp6_x(ident, b"PASSWORD2", salt_le)
    v = pow(rc.G, x, rc.N)
    b_secret = 0xA1B2C3D4E5F60718293A4B5C6D7E8F90A1B2C3D4E5F60718293A4B5C6D7E8F90
    a_secret = 0x0F0E0D0C0B0A09080706050403020100FFEEDDCCBBAA99887766554433221100
    ch = rc.Challenge(b_int=(rc.SRP_K * v + pow(rc.G, b_secret, rc.N)) % rc.N,
                      g_int=rc.G, n_int=rc.N, salt_le=salt_le,
                      version_challenge=rc.VERSION_CHALLENGE, security_flags=0)
    sess = rc.client_session("DiffTwo", "Password2", ch, a_secret=a_secret)
    A = sess["a_int"]
    B = ch.b_int

    # SRP6.cpp:78-84 u = sha1(A || B) little-endian; S = (A * v^u)^b mod N
    u = int.from_bytes(_sha1(_le_min(A) + _le_min(B)), "little")
    s_server = pow(A * pow(v, u, rc.N), b_secret, rc.N)
    assert s_server == sess["s_int"]

    # SRP6.cpp:117-143 K = weave(sha1(S LE evens), sha1(S LE odds))
    t = s_server.to_bytes(32, "little")
    k_server = bytes(b for pair in zip(_sha1(t[0::2]), _sha1(t[1::2])) for b in pair)
    assert k_server == sess["session_key"]

    # SRP6.cpp:46-73 M1 = sha1(sha1(N)^sha1(g) || sha1(I) || s || A || B || K)
    t3 = bytes(p ^ q for p, q in zip(_sha1(_le_min(rc.N)), _sha1(_le_min(rc.G))))
    k_int = int.from_bytes(k_server, "little")
    m1_server = _sha1(_le_min(int.from_bytes(t3, "little")) + _sha1(ident)
                      + _le_min(int.from_bytes(salt_le, "little"))
                      + _le_min(A) + _le_min(B) + _le_min(k_int))
    assert m1_server == sess["m1"]

    # SRP6.cpp:167-172 M2 = sha1(A || M1 || K)
    m2_server = _sha1(_le_min(A) + _le_min(int.from_bytes(m1_server, "little"))
                      + _le_min(k_int))
    assert m2_server == sess["m2_expected"]


def test_interleave_independent_construction():
    # SRP6.cpp:117-143 weaves the two digests: vK[2i]=sha1(evens)[i], vK[2i+1]=sha1(odds)[i]
    t = bytes(range(32))  # S whose LE bytes are 0x00..0x1f
    s_int = int.from_bytes(t, "little")
    assert rc._interleave(s_int) == bytes(b for pair in zip(_sha1(t[0::2]), _sha1(t[1::2]))
                                          for b in pair)


# --- packet builders: exact byte shapes ---------------------------------------------------------


def test_logon_challenge_bytes_probe_verified():
    # The exact packet that got the live server's 119-byte challenge reply on 2026-09-30.
    pkt = rc.build_logon_challenge("lw4probe")
    assert pkt.hex() == (
        "00002600"                       # cmd 0x00, error 0x00, size 38 LITTLE-endian
        "576f5700"                       # gamename[4] 'WoW\0'
        "030305"                         # version 3.3.5
        "3430"                           # build 12340 = 0x3034, little-endian
        "36387800"                       # platform[4] '68x\0'
        "57696e00"                       # os[4] 'Win\0'
        "55534100"                       # country[4] 'USA\0'
        "00000000"                       # timezone bias
        "0100007f"                       # ip 127.0.0.1
        "08"                             # I_len
        "4c573450524f4245"               # I 'LW4PROBE' (uppercased by the client)
    )


def test_logon_challenge_size_field_covers_body_and_is_little_endian():
    for name in ("A", "LW4PROBE", "SIXTEENCHARNAME"):
        pkt = rc.build_logon_challenge(name)
        size = struct.unpack("<H", pkt[2:4])[0]
        assert size == len(pkt) - 4 == 30 + len(name.upper())


def test_logon_proof_is_75_bytes_with_pinned_layout():
    a_int = 0x01  # A = 1 -> 32 LE bytes 01 then zeros
    m1 = bytes(range(20))
    pkt = rc.build_logon_proof(a_int, m1)
    assert len(pkt) == 75
    assert pkt[0] == 0x01
    assert pkt[1:33] == b"\x01" + b"\x00" * 31
    assert pkt[33:53] == m1
    assert pkt[53:75] == b"\x00" * 22  # crc_hash zeros + keys 0 + securityFlags 0


def test_realm_list_request_is_five_bytes():
    assert rc.build_realm_list_request() == b"\x10\x00\x00\x00\x00"


# --- packet parsers: synthetic shapes and typed refusals ----------------------------------------


def _synth_challenge(salt_le: bytes, b_int: int = 0x1234, n_int: int | None = None) -> bytes:
    return (b"\x00\x00\x00" + b_int.to_bytes(32, "little")
            + b"\x01\x07" + b"\x20"
            + (n_int if n_int is not None else rc.N).to_bytes(32, "little")
            + salt_le + rc.VERSION_CHALLENGE + b"\x00")


def test_parse_logon_challenge_extracts_le_fields():
    salt_le = bytes(range(32))
    ch = rc.parse_logon_challenge(_synth_challenge(salt_le, b_int=0xABCD))
    assert ch.b_int == 0xABCD
    assert ch.g_int == 7 and ch.n_int == rc.N
    assert ch.salt_le == salt_le
    assert ch.version_challenge == rc.VERSION_CHALLENGE
    assert ch.security_flags == 0


def test_parse_logon_challenge_refuses_foreign_group_and_bad_shapes():
    salt_le = bytes(32)
    with pytest.raises(rc.ProtocolError, match="non-standard SRP6 group"):
        rc.parse_logon_challenge(_synth_challenge(salt_le, n_int=rc.N - 2))
    with pytest.raises(rc.ProtocolError, match="result code"):
        rc.parse_logon_challenge(b"\x00\x00\x04")
    with pytest.raises(rc.ProtocolError, match="truncated"):
        rc.parse_logon_challenge(b"\x00\x00\x00")


def test_parse_logon_proof_success_and_failure_shapes():
    m2 = bytes(range(20))
    ok_pkt = (b"\x01\x00" + m2 + struct.pack("<I", 0x00800000)  # ACCOUNT_FLAG_PROPASS
              + struct.pack("<I", 0) + struct.pack("<H", 0))    # surveyId, unkFlags
    assert len(ok_pkt) == 32                                     # sizeof(sAuthLogonProof_S)
    res = rc.parse_logon_proof(ok_pkt)
    assert res.ok and res.m2 == m2 and res.account_flags == 0x00800000
    res = rc.parse_logon_proof(b"\x01\x04\x00\x00")
    assert not res.ok and res.error == rc.AUTH_LOGON_FAILED_UNKNOWN_ACCOUNT
    with pytest.raises(rc.ProtocolError):
        rc.parse_logon_proof(b"\x02")


def test_parse_realm_list_roundtrip():
    entry = (b"\x01\x00\x04" + b"Test\x00" + b"127.0.0.1:8085\x00"
             + struct.pack("<f", 1.5) + b"\x03\x02\x2c" + bytes([3, 3, 5])
             + struct.pack("<H", 12340))
    body = struct.pack("<IH", 0, 1) + entry + struct.pack("<H", 0x0010)
    pkt = b"\x10" + struct.pack("<H", len(body)) + body
    realms = rc.parse_realm_list(pkt)
    assert realms == [{"icon": 1, "locked": 0, "flags": 4, "name": "Test",
                       "address": "127.0.0.1:8085", "population": 1.5, "characters": 3,
                       "timezone": 2, "version": (3, 3, 5, 12340)}]
    with pytest.raises(rc.ProtocolError):
        rc.parse_realm_list(b"\x10" + struct.pack("<H", 2) + b"\x00\x00\x00\x99")


# --- live: the whole point -- does the handshake complete? --------------------------------------


@pytest.mark.skipif(not _realmd_up(), reason="estate realmd not listening on 127.0.0.1:3724")
def test_live_handshake_completes_and_persists_session_key():
    out = rc.handshake(*LIVE, "LW4PROBE", "LASTMILE", timeout=5.0)
    assert out["ok"], out
    assert out["stage"] == "authed"
    assert out["m2_verified"] is True
    assert len(out["session_key"]) == 80  # 40 bytes hex; realmd persists this to account.sessionkey
    assert any(r["name"] == "MaNGOS" and r["address"] == "127.0.0.1:8085" for r in out["realms"])


@pytest.mark.skipif(not _realmd_up(), reason="estate realmd not listening on 127.0.0.1:3724")
def test_live_wrong_password_is_refused_at_proof_stage():
    # Falsification guard: a client whose M1 always "passed" would fail here. The server
    # checks M1 (SRP6::Proof) and answers the 4-byte UNKNOWN_ACCOUNT refusal (0x04).
    out = rc.handshake(*LIVE, "LW4PROBE", "DEFINITELY-NOT-IT", timeout=5.0)
    assert out == {"ok": False, "stage": "proof",
                   "error": f"0x{rc.AUTH_LOGON_FAILED_UNKNOWN_ACCOUNT:02x}",
                   "expected_m2_match": False}
