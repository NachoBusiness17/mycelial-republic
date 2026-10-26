#!/usr/bin/env python3
"""realmd_client.py - pure-stdlib SRP6 client that logs into the estate's realmd (LW4, 2026-09-30).

B2 begins: our client speaks the WoW logon protocol to the running CMaNGOS realmd
(WSL, 127.0.0.1:3724). Every byte shape and every math step below is copied from the
compiled specimen's own source, clone at ~/mangos-wotlk in WSL, and was verified on the
wire against the live server on 2026-09-30 (receipt watch/inbox/last_mile_20260930/):

  flow        AuthSocket.cpp:200 table (CHALLENGE 0x00 -> PROOF 0x01 -> REALM_LIST 0x10),
              AuthCodes.h:30-34 opcode values
  challenge   AuthSocket.cpp:64-82 struct sAuthLogonChallenge_C; size read native-LE
              (EndianConvert is a nop on x86, ByteConverter.h:57-60), build read native-LE
  reply       AuthSocket.cpp:448-460: [0x00, 0x00, 0x00] + B(32) + g_len(1)=1 + g +
              N_len(1)=32 + N(32) + s(32) + version_challenge(16) + security_flags(1)
  bignum wire BigNumber.h:84 AsByteArray(minSize=0, reverse=true): ALL big numbers are
              LITTLE-ENDIAN on the wire and in every hash (SetBinary reverses input,
              BigNumber.cpp). Empirical oracle: N arrives as 0xB7.. (reversed hex), salt
              arrives reversed. A classic big-endian SRP6 client fails against this server.
  SRP6 math   src/shared/SRP6/SRP6.cpp: B=(3v+g^b)%N (line 37), x=sha1(s||sha1(I:P))
              (107-114), u=sha1(A||B) (78-84), S=(A*v^u)^b (83), K=sha-interleave of S
              LE-bytes (117-143), M1=sha1(sha1(N)^sha1(g) || sha1(I) || s || A || B || K)
              (46-73), M2=sha1(A || M1 || K) (167-172)

The client mirrors the server formula on the client side: S = (B - 3*g^x)^(a + u*x) mod N,
which equals (A * v^u)^b mod N when B = (3v + g^b) mod N (algebra in tests, by vector).

Edge honored: SRP6::Proof (SRP6.cpp:186-193) memcmp's M.AsByteArray() (LE-minimal) against
the raw 20 wire bytes; if the M1 digest's last byte is 0x00 the server over-reads its own
19-byte buffer and auth flakes. client_session regenerates `a` when M1 ends in 0x00.

RUN:
  python tools/realmd_client.py -u LW4PROBE -p LASTMILE            # full handshake + realmlist
  python tools/realmd_client.py --verifier LW4PROBE LASTMILE 7E5C...   # print v/s for the DB
Tests: tests/test_realmd_client.py (math vectors + byte shapes + live self-skip).

Schema: realmd_client.v1 . stdlib only . no DB, no writes .
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import socket
import struct
import sys
from dataclasses import dataclass
from typing import Any

CMD_AUTH_LOGON_CHALLENGE = 0x00
CMD_AUTH_LOGON_PROOF = 0x01
CMD_REALM_LIST = 0x10

AUTH_LOGON_SUCCESS = 0x00
AUTH_LOGON_FAILED_UNKNOWN_ACCOUNT = 0x04
AUTH_LOGON_FAILED_VERSION_INVALID = 0x09

BUILD_WOTLK_335 = 12340
VERSION_WOTLK = (3, 3, 5)
VERSION_CHALLENGE = bytes.fromhex("BAA31E99A00B2157FC373FB369CDD2F1")  # AuthSocket.cpp:177

# SRP6.cpp:26-28. Fixed 256-bit group; g=7; mangos hardcodes k=3 (SRP6.cpp:39).
N_HEX = "894B645E89E1535BBDAD5B8B290650530801B18EBFBF5E8FAB3C82872A3E9BB7"
N = int(N_HEX, 16)
G = 7
SRP_K = 3


class ProtocolError(Exception):
    """Malformed or refused server packet; typed, never a crash."""


def sha1(data: bytes) -> bytes:
    return hashlib.sha1(data).digest()


def le_min(value: int) -> bytes:
    """BigNumber::AsByteArray(0): minimal little-endian bytes (trailing 0x00 stripped)."""
    if value == 0:
        return b"\x00"
    return value.to_bytes((value.bit_length() + 7) // 8, "little")


def le_pad(value: int, size: int) -> bytes:
    """BigNumber::AsByteArray(size): little-endian, arithmetic-padded to exactly size bytes."""
    return value.to_bytes(size, "little")


# ---------------------------------------------------------------------------------------------
# Registration math (SRP6::CalculateVerifier, SRP6.cpp:88-114): x = sha1(s || sha1(I:P)),
# read little-endian; v = g^x mod N. The account table stores v and s as big-endian hex.
# ---------------------------------------------------------------------------------------------


def srp6_x(username: bytes, password: bytes, salt_le: bytes) -> int:
    digest = sha1(username + b":" + password)
    return int.from_bytes(sha1(salt_le + digest), "little")


def srp6_verifier(username: bytes, password: bytes, salt_le: bytes) -> int:
    return pow(G, srp6_x(username, password, salt_le), N)


def verifier_sql(username: str, password: str, salt_hex: str) -> dict[str, str]:
    """The INSERT/UPDATE shape used to arm the fixture account (dogfood: LW4PROBE, id 6)."""
    user = username.upper().encode("ascii")
    salt_le = int(salt_hex, 16).to_bytes(32, "little")
    v = srp6_verifier(user, password.upper().encode("ascii"), salt_le)
    return {
        "s": f"{int.from_bytes(salt_le, 'little'):X}",
        "v": f"{v:X}",
        "sql": ("INSERT INTO account (username, gmlevel, v, s, expansion) VALUES "
                f"('{user.decode()}', 0, '{v:X}', '{int.from_bytes(salt_le, 'little'):X}', 2) "
                f"ON DUPLICATE KEY UPDATE v=VALUES(v), s=VALUES(s);"),
    }


# ---------------------------------------------------------------------------------------------
# Packet builders (pure; byte shapes pinned by tests/test_realmd_client.py)
# ---------------------------------------------------------------------------------------------


def build_logon_challenge(username: str, *, build: int = BUILD_WOTLK_335,
                          version: tuple[int, int, int] = VERSION_WOTLK,
                          platform: bytes = b"68x\x00", os_name: bytes = b"Win\x00",
                          country: bytes = b"USA\x00", tz_bias: int = 0,
                          ip: int = 0x7F000001) -> bytes:
    """CMD_AUTH_LOGON_CHALLENGE, struct sAuthLogonChallenge_C (AuthSocket.cpp:64-82).

    All integer fields are little-endian: the server reads them natively (EndianConvert
    is a nop on x86). The size field covers the body only and is little-endian too,
    verified on the wire 2026-09-30: LE size got a reply, BE size made the server wait.
    """
    ident = username.upper().encode("ascii")
    if not 1 <= len(ident) <= 16:
        raise ProtocolError(f"username length {len(ident)} out of 1..16")
    body = (b"WoW\x00" + bytes(version) + struct.pack("<H", build)
            + platform + os_name + country
            + struct.pack("<i", tz_bias) + struct.pack("<I", ip)
            + bytes([len(ident)]) + ident)
    return struct.pack("<BBH", CMD_AUTH_LOGON_CHALLENGE, 0, len(body)) + body


def build_logon_proof(a_int: int, m1: bytes) -> bytes:
    """CMD_AUTH_LOGON_PROOF, struct sAuthLogonProof_C (AuthSocket.cpp:107-115): 75 bytes,
    A as 32 LE bytes (server SetBinary(A,32) reverses), crc_hash zeros (StrictVersionCheck
    defaults false, AuthSocket.cpp:1011-1013), keys/securityFlags zero."""
    return (bytes([CMD_AUTH_LOGON_PROOF]) + le_pad(a_int, 32) + m1
            + b"\x00" * 20 + b"\x00" + b"\x00")


def build_realm_list_request() -> bytes:
    """CMD_REALM_LIST: 5 bytes, server does ReadSkip(5) (AuthSocket.cpp:787-790)."""
    return bytes([CMD_REALM_LIST]) + b"\x00" * 4


# ---------------------------------------------------------------------------------------------
# Packet parsers (pure, typed refusal on malformation)
# ---------------------------------------------------------------------------------------------


@dataclass
class Challenge:
    b_int: int
    g_int: int
    n_int: int
    salt_le: bytes
    version_challenge: bytes
    security_flags: int


@dataclass
class ProofResult:
    ok: bool
    error: int
    m2: bytes
    account_flags: int


def parse_logon_challenge(data: bytes) -> Challenge:
    """AuthSocket.cpp:448-460 reply shape. Refuses N/g that differ from the fixed group
    (a real client binds to its constants; a moved server is not silently accepted)."""
    if len(data) < 3:
        raise ProtocolError(f"challenge reply truncated: {len(data)} bytes")
    if data[0] != CMD_AUTH_LOGON_CHALLENGE:
        raise ProtocolError(f"expected cmd 0x00, got 0x{data[0]:02x}")
    if data[2] != AUTH_LOGON_SUCCESS:
        raise ProtocolError(f"logon refused, result code 0x{data[2]:02x}")
    if len(data) < 3 + 32 + 1 + 1 + 1 + 32 + 32 + 16 + 1:
        raise ProtocolError(f"challenge body truncated: {len(data)} bytes")
    off = 3
    b_int = int.from_bytes(data[off:off + 32], "little")
    off += 32
    g_len = data[off]
    off += 1
    g_int = int.from_bytes(data[off:off + g_len], "little")
    off += g_len
    n_len = data[off]
    off += 1
    n_int = int.from_bytes(data[off:off + n_len], "little")
    off += n_len
    salt_le = data[off:off + 32]  # no length byte; 32 LE bytes (AuthSocket.cpp:456)
    off += 32
    version_challenge = data[off:off + 16]
    off += 16
    security_flags = data[off]
    if security_flags != 0:
        raise ProtocolError(f"unsupported security flags 0x{security_flags:02x}")
    if n_int != N or g_int != G:
        raise ProtocolError("server sent a non-standard SRP6 group (N or g mismatch)")
    return Challenge(b_int, g_int, n_int, salt_le, version_challenge, security_flags)


def parse_logon_proof(data: bytes) -> ProofResult:
    """Success: 32-byte sAuthLogonProof_S (M2 + accountFlags, AuthSocket.cpp:129-133, 295).
    Failure: 4 bytes [0x01, error, 0, 0] (AuthSocket.cpp:641)."""
    if not data or data[0] != CMD_AUTH_LOGON_PROOF:
        raise ProtocolError(f"expected cmd 0x01, got {data[:1].hex()}")
    if data[1] == AUTH_LOGON_SUCCESS and len(data) >= 32:
        return ProofResult(True, 0, data[2:22], struct.unpack("<I", data[22:26])[0])
    return ProofResult(False, data[1] if len(data) > 1 else 0xFF, b"", 0)


def parse_realm_list(data: bytes) -> list[dict[str, Any]]:
    """AuthSocket.cpp:810-816 header + LoadRealmlist 3.3.5 branch (886-937): body is
    uint32(0), uint16 count, realm entries (null-terminated name/address), uint16 footer."""
    if len(data) < 9 or data[0] != CMD_REALM_LIST:
        raise ProtocolError("malformed realm list header")
    size = struct.unpack("<H", data[1:3])[0]
    body = data[3:3 + size]
    off = 6  # uint32(0) + uint16 count
    realms: list[dict[str, Any]] = []
    while off < len(body) - 2:
        icon, lock, flags = body[off], body[off + 1], body[off + 2]
        off += 3
        fields: list[bytes] = []
        for _ in range(2):  # name, address: both null-terminated
            end = body.index(b"\x00", off)
            fields.append(body[off:end])
            off = end + 1
        population = struct.unpack("<f", body[off:off + 4])[0]
        off += 4
        numchars, timezone = body[off], body[off + 1]
        off += 3  # numchars, timezone, unk 0x2C (AuthSocket.cpp:928)
        realm: dict[str, Any] = {"icon": icon, "locked": lock, "flags": flags,
                                 "name": fields[0].decode("utf-8"),
                                 "address": fields[1].decode("utf-8"),
                                 "population": population, "characters": numchars,
                                 "timezone": timezone}
        if flags & 0x04:  # REALM_FLAG_SPECIFYBUILD: major.minor.bugfix + build
            realm["version"] = (body[off], body[off + 1], body[off + 2],
                                struct.unpack("<H", body[off + 3:off + 5])[0])
            off += 5
        realms.append(realm)
    if struct.unpack("<H", body[-2:])[0] != 0x0010:
        raise ProtocolError("realm list footer is not 0x0010")
    return realms


# ---------------------------------------------------------------------------------------------
# SRP6 client math (mirror of SRP6.cpp; see module docstring for the line receipts)
# ---------------------------------------------------------------------------------------------


def _interleave(s_int: int) -> bytes:
    """SRP6::HashSessionKey (SRP6.cpp:117-143): S as 32 LE bytes; K = weave(sha1(evens),
    sha1(odds)) with the even digest at indexes 0,2,4.. and odd at 1,3,5.. (40 bytes)."""
    t = s_int.to_bytes(32, "little")
    even, odd = sha1(t[0::2]), sha1(t[1::2])
    return bytes(b for pair in zip(even, odd) for b in pair)


def _ng_xor() -> bytes:
    return bytes(a ^ b for a, b in zip(sha1(le_min(N)), sha1(le_min(G))))


def client_session(username: str, password: str, ch: Challenge, *,
                   a_secret: int | None = None) -> dict[str, Any]:
    """Full client-side SRP6 given the parsed challenge. Returns A, M1, expected M2, K, S.
    Regenerates `a` if M1 ends in 0x00 (server memcmp over-read edge, SRP6.cpp:186)."""
    ident = username.upper().encode("ascii")
    x = srp6_x(ident, password.upper().encode("ascii"), ch.salt_le)
    for attempt in range(32):
        a = a_secret if (a_secret is not None and attempt == 0) else secrets.randbits(256)
        a_int = pow(G, a, N)
        u = int.from_bytes(sha1(le_min(a_int) + le_min(ch.b_int)), "little")
        s_int = pow(ch.b_int - SRP_K * pow(G, x, N), a + u * x, N) % N
        k40 = _interleave(s_int)
        k_int = int.from_bytes(k40, "little")
        m1 = sha1(le_min(int.from_bytes(_ng_xor(), "little")) + sha1(ident)
                  + le_min(int.from_bytes(ch.salt_le, "little")) + le_min(a_int)
                  + le_min(ch.b_int) + le_min(k_int))
        if m1[19] != 0 or a_secret is not None:
            m2 = sha1(le_min(a_int) + le_min(int.from_bytes(m1, "little")) + le_min(k_int))
            return {"a_secret": a, "a_int": a_int, "m1": m1, "m2_expected": m2,
                    "session_key": k40, "s_int": s_int}
    raise ProtocolError("32 attempts all landed M1 ending in 0x00 (server memcmp edge)")


# ---------------------------------------------------------------------------------------------
# Live handshake
# ---------------------------------------------------------------------------------------------


def _recv_reply(sock: socket.socket) -> bytes:
    """One recv per reply: realmd writes each reply with a single Write (AuthSocket.cpp
    Write calls), so one segment carries it whole. Success replies are 119/32 bytes,
    refusals are 3/4 bytes; callers type-check the length, nothing is papered over."""
    return sock.recv(512)


def handshake(host: str, port: int, username: str, password: str, *,
              timeout: float = 5.0, realm_list: bool = True) -> dict[str, Any]:
    """Connect -> challenge -> proof (verify M2) -> realm list. The session key returned
    is the same K realmd persists to account.sessionkey (the inter-process contract)."""
    with socket.create_connection((host, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall(build_logon_challenge(username))
        reply = _recv_reply(sock)
        if len(reply) < 3:
            return {"ok": False, "stage": "challenge", "error": f"short reply {reply.hex()}"}
        if reply[2] != AUTH_LOGON_SUCCESS:
            return {"ok": False, "stage": "challenge", "error": f"result 0x{reply[2]:02x}"}
        if len(reply) < 119:
            return {"ok": False, "stage": "challenge",
                    "error": f"challenge truncated: {len(reply)} bytes"}
        ch = parse_logon_challenge(reply)
        sess = client_session(username, password, ch)
        sock.sendall(build_logon_proof(sess["a_int"], sess["m1"]))
        proof_raw = _recv_reply(sock)
        if len(proof_raw) < 4:
            return {"ok": False, "stage": "proof",
                    "error": f"proof reply truncated: {proof_raw.hex()}"}
        proof = parse_logon_proof(proof_raw)
        if not proof.ok:
            return {"ok": False, "stage": "proof", "error": f"0x{proof.error:02x}",
                    "expected_m2_match": False}
        if proof.m2 != sess["m2_expected"]:
            return {"ok": False, "stage": "m2_verify", "error": "server M2 != expected M2"}
        out: dict[str, Any] = {"ok": True, "stage": "authed", "username": username.upper(),
                               "session_key": sess["session_key"].hex(),
                               "m2_verified": True, "realms": []}
        if realm_list:
            sock.sendall(build_realm_list_request())
            raw = _recv_reply(sock)
            if len(raw) < 3:
                return {"ok": False, "stage": "realm_list", "error": f"short reply {raw.hex()}"}
            size = struct.unpack("<H", raw[1:3])[0]
            if len(raw) < 3 + size:
                return {"ok": False, "stage": "realm_list",
                        "error": f"realm list truncated: {len(raw)} < {3 + size}"}
            out["realms"] = parse_realm_list(raw[:3 + size])
        return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="realmd-client")
    ap.add_argument("-H", "--host", default="127.0.0.1")
    ap.add_argument("-P", "--port", type=int, default=3724)
    ap.add_argument("-u", "--user")
    ap.add_argument("-p", "--password")
    ap.add_argument("--timeout", type=float, default=5.0)
    ap.add_argument("--no-realmlist", action="store_true")
    ap.add_argument("--verifier", nargs=3, metavar=("USER", "PASS", "SALT_HEX"),
                    help="print the v/s pair + account INSERT for fixture setup")
    args = ap.parse_args(argv)
    if args.verifier:
        print(json.dumps(verifier_sql(*args.verifier), indent=2))
        return 0
    if not args.user or not args.password:
        ap.error("-u/-password required (or --verifier USER PASS SALT_HEX)")
    result = handshake(args.host, args.port, args.user, args.password,
                       timeout=args.timeout, realm_list=not args.no_realmlist)
    print(json.dumps(result, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
