"""frame_mac: K-derived per-frame MACs over the line-JSON wire (R3, 2026-09-30).

THE KILL (Q03, the frontier's top security finding; spec
watch/inbox/frontier_asks/volley2/results/V2ASK1.md, "The Auth Trinity"):
post-auth frames carried no integrity -- one flipped byte on the wire
reattributes a forged move to a real identity, because the sid field
inside the JSON is the ONLY thing binding a move to its author. This
module binds every post-auth frame to the session key K the SRP6
handshake minted: the attacker without K cannot produce a tag the server
accepts, so attribution stops being a claimable field and becomes a
provable property. The spec's own caveat stands and is named here: K
rides a 256-bit-group SRP6, so a DLP-solving eavesdropper still breaks
this; the MAC is Phase 1 (raises "flip one byte" to "run a DLP solver"),
TLS is Phase 2 (V2ASK1 Q04).

THE WIRE LAW (owned by server/protocol.py's docstring; this module is
the math + the law executable): after srp_proof succeeds, every frame
on that connection carries
    "seq"  per-direction int counter, both sides start at 0
    "mac"  32 lowercase hex chars = HMAC-SHA256(k_dir, dom || body)[:16]
where body is the frame minus its own "mac" field in the house canonical
form (sorted keys, compact separators, the world.row_sha law: a digest
covers the row minus the field that carries it). The domain prefix
b"mac1-v1 " + direction + b"\\x00" binds the tag to its direction, so a
server->client frame fed back as client->server rejects (reflection).
Keys are per-session and per-direction, so a frame from session X cannot
verify under session Y's keys (splice).

KEY DERIVATION (V2ASK1 Q03 verbatim, HKDF per RFC 5869 over
HMAC-SHA256):
    prk    = HMAC-SHA256(key = SHA256(A_le || B_le), msg = K)
    k_c2s  = HKDF-Expand(prk, "mesh-frame-v1 c2s", 32)
    k_s2c  = HKDF-Expand(prk, "mesh-frame-v1 s2c", 32)
    mac_id = HKDF-Expand(prk, "mesh-frame-v1 sid", 16)
A_le/B_le are the handshake's public ephemerals in the estate's
little-endian le_min shape (the operand order the live realmd proved,
tools/realmd_client); the salt binds the keys to THIS handshake, and the
fresh b per challenge makes every session's keys unique.

RECEIVER RULES (the spec's, kept): constant-time compare
(hmac.compare_digest); seq must EQUAL expected, then increment -- any
gap, repeat, or bad tag is tamper; never resync; never downgrade within
a session (once a client has sent one valid MAC-bearing frame, bare
frames from it are tamper too). Server-side the failure is one code,
BAD_MAC (which check failed is not the attacker's business), and the
enforcement point (server/server.py) answers BAD_MAC, files a
kind:mac_tamper row in the world's hash chain, and disconnects.

MIGRATION (the mission law: migration, not breakage): the flag
require_frame_mac (WorldServer, default False) is the window. While
False, an SRP6-authed client that never sends "mac" fields stays legal
-- old clients keep working, byte-compat, their sessions running at
integrity "none". Flip it and every frame after SRP6 auth must carry a
valid MAC; the plaintext hello door carries no K and is bare either way.

NAMED DEVIATIONS FROM THE V2ASK1 WIRE FORMAT (the mission chose the
hmac-field-in-JSON shape over the spec's "M1 <seq> <tag> <payload>"
prefix line; deviations follow the estate law of naming them):
    canonical body, not exact transmitted bytes: the spec's M1 MACs the
        raw payload bytes; an in-JSON field cannot contain a tag over
        the bytes that contain it, so the tag covers the DECODED frame
        recanonicalized in the house form instead. The parse-
        differential class the spec warned about is bounded by the
        estate's canonical encode() being the only producer on this
        wire (both ends rebuild identical body bytes from the dict).
    hex tag, not base64url: SRP6 material already rides lowercase hex;
        the mac field follows (32 hex chars = the spec's 16 tag bytes).
    no caps/caps_tag negotiation: the sealed SRP6 welcome (s2c seq 0)
        IS the capability announcement -- its valid tag proves the
        server can MAC -- and the client's first valid MAC-bearing
        frame (c2s seq 0) is the opt-in (the spec's sticky rule).
    broadcast ticks stay bare: encode-once fan-out is the determinism
        law (rooms.broadcast); s2c sealing covers DIRECT replies only.
        Full s2c broadcast sealing is owed to the TLS-phase lane.

Run: no operability main -- this is a library lane; the laws run under
    .venv/Scripts/python.exe -m pytest tests/test_frame_mac.py -q
Tests: tests/test_frame_mac.py (roundtrip, flipped-byte, replay, the
no-MAC flag path, reflection, splice, seq, bit-flip exhaustion, table)

Schema: frame_mac.v1 . stdlib + tools.realmd_client (le_min) only . no
world-log writes (the tamper row is appended by server/server.py, the
enforcement point, not this module)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.protocol_table import (  # noqa: E402
    DEFAULT_SPEC,
    canonical_json,
    compile_table,
)
from tools.realmd_client import le_min  # noqa: E402 - the proven byte order

# Directions (the reflection kill: the domain prefix differs per side)
C2S = b"c2s"
S2C = b"s2c"

TAG_BYTES = 16                 # the spec's tag width; rides as 32 hex chars
_DOMAIN_PREFIX = b"mac1-v1 "   # domain separation: not any HMAC on this wire


class MacError(ValueError):
    """Typed, fail-closed refusal. why is an internal reason string
    ("SHAPE" | "SEQ" | "TAG"); the wire always sees one code, BAD_MAC --
    which check failed is not the attacker's business."""

    def __init__(self, why: str) -> None:
        super().__init__(f"frame MAC failure: {why}")
        self.why = why


# ---------------------------------------------------------------------------------------------
# Key derivation (V2ASK1 Q03 verbatim)
# ---------------------------------------------------------------------------------------------


def _hkdf_expand(prk: bytes, info: str, length: int) -> bytes:
    """RFC 5869 expand over HMAC-SHA256. 32-byte outputs need exactly one
    block, but the loop is the general shape so longer outputs stay lawful."""
    out = b""
    block, counter = b"", 0
    while len(out) < length:
        counter += 1
        block = hmac.new(prk, block + info.encode("utf-8")
                         + bytes([counter]), hashlib.sha256).digest()
        out += block
    return out[:length]


@dataclass(frozen=True)
class FrameKeys:
    """One session's MAC material. k_c2s seals client frames and verifies
    them server-side; k_s2c seals server replies and verifies them
    client-side; mac_id is the 16-byte session binding id (the spec's sid
    expand -- a diagnostic surface: frame provenance without logging K)."""
    k_c2s: bytes
    k_s2c: bytes
    mac_id: bytes

    @property
    def mac_id_hex(self) -> str:
        return self.mac_id.hex()


def derive(session_key: bytes, a_le: bytes, b_le: bytes) -> FrameKeys:
    """HKDF from the SRP6 session key, salted by the handshake's publics.
    Same (K, A, B) in, same keys out, on both sides of the wire."""
    salt = hashlib.sha256(a_le + b_le).digest()
    prk = hmac.new(salt, session_key, hashlib.sha256).digest()
    return FrameKeys(
        k_c2s=_hkdf_expand(prk, "mesh-frame-v1 c2s", 32),
        k_s2c=_hkdf_expand(prk, "mesh-frame-v1 s2c", 32),
        mac_id=_hkdf_expand(prk, "mesh-frame-v1 sid", 16),
    )


def derive_from_wire(session_key_hex: str, a_hex: str, b_hex: str) -> FrameKeys:
    """The wire-shape wrapper: K as hex (auth_srp6.verify_proof's
    session_key), A/B as the lowercase-hex integers the handshake
    exchanged, converted with the proven little-endian le_min."""
    return derive(bytes.fromhex(session_key_hex),
                  le_min(int(a_hex, 16)), le_min(int(b_hex, 16)))


# ---------------------------------------------------------------------------------------------
# The frame law: body, tag, seal, check
# ---------------------------------------------------------------------------------------------


def frame_body(msg: dict[str, Any]) -> bytes:
    """The MAC-covered bytes: the frame minus its own "mac" field, in the
    house canonical form (protocol_table.canonical_json, the world.row_sha
    law). "seq" stays INSIDE the body, so a tag is bound to its sequence
    number -- an attacker cannot retag an old frame with a new seq."""
    body = {k: v for k, v in msg.items() if k != "mac"}
    return canonical_json(body).encode("utf-8")


def compute_tag(keys: FrameKeys, direction: bytes, body: bytes) -> bytes:
    return hmac.new(keys.k_c2s if direction == C2S else keys.k_s2c,
                    _DOMAIN_PREFIX + direction + b"\x00" + body,
                    hashlib.sha256).digest()[:TAG_BYTES]


def seal(keys: FrameKeys, direction: bytes, msg: dict[str, Any],
         seq: int) -> dict[str, Any]:
    """Attach "seq" + "mac" to a copy of msg. The sender-side builder
    (clients seal c2s, the server seals s2c replies)."""
    out = dict(msg)
    out["seq"] = seq
    out["mac"] = compute_tag(keys, direction, frame_body(out)).hex()
    return out


def check(keys: FrameKeys, direction: bytes, expected_seq: int,
          msg: dict[str, Any]) -> None:
    """Verify one MAC-bearing frame (the receiver-side law). Raises the
    typed MacError on any shape violation, seq mismatch, or tag mismatch;
    returns None when the frame is authentic, ordered, and untampered.
    Constant-time compare (hmac.compare_digest, the spec's rule)."""
    seq = msg.get("seq")
    # type(seq) is int: a bool is a verdict, not a sequence number (the
    # X9 u8 / LW7 nonce law); floats and strings are not seqs either
    if type(seq) is not int or seq < 0:
        raise MacError("SHAPE")
    if seq != expected_seq:
        raise MacError("SEQ")
    tag = msg.get("mac")
    if (not isinstance(tag, str) or len(tag) != TAG_BYTES * 2):
        raise MacError("SHAPE")
    try:
        given = bytes.fromhex(tag)
    except ValueError as exc:
        raise MacError("SHAPE") from exc
    want = compute_tag(keys, direction, frame_body(msg))
    if not hmac.compare_digest(want, given):
        raise MacError("TAG")


# ---------------------------------------------------------------------------------------------
# The per-session state machine (server side of the law)
# ---------------------------------------------------------------------------------------------


class FrameMacState:
    """One armed session: expected c2s seq, next s2c seq, and the sticky
    mac_mode bit (the spec's rule: the first VALID MAC-bearing frame opts
    the session in; after that a bare frame is a downgrade attempt, which
    is tamper). Owned by server/server.py's peer dict; integrity is the
    spec's receipts field -- "mac1" once MAC-bound, "none" while the
    session rides the migration window."""

    __slots__ = ("keys", "expected_seq", "s2c_seq", "mac_mode")

    def __init__(self, keys: FrameKeys) -> None:
        self.keys = keys
        self.expected_seq = 0
        self.s2c_seq = 0
        self.mac_mode = False

    @property
    def integrity(self) -> str:
        return "mac1" if self.mac_mode else "none"

    def admit(self, msg: dict[str, Any], *, require: bool = False) -> str | None:
        """The receipt gate for one incoming frame. None = admitted (a
        verified MAC-bearing frame, or a legal bare frame inside the
        migration window); "BAD_MAC" = tamper. require is the server's
        require_frame_mac flag: when True a bare frame from an armed
        session is tamper even before the session ever went sticky."""
        if "mac" not in msg:
            if self.mac_mode or require:
                # sticky: stripping "mac" off is the downgrade attack;
                # require: the flag closed the bare window
                return "BAD_MAC"
            return None  # migration window: an old SRP6 client, integrity none
        try:
            check(self.keys, C2S, self.expected_seq, msg)
        except MacError:
            return "BAD_MAC"
        self.expected_seq += 1
        self.mac_mode = True
        return None

    def seal_reply(self, msg: dict[str, Any]) -> dict[str, Any]:
        """Seal one server->client DIRECT reply (the s2c direction counts
        independently from c2s). Broadcast ticks never pass through here."""
        out = seal(self.keys, S2C, msg, self.s2c_seq)
        self.s2c_seq += 1
        return out


# ---------------------------------------------------------------------------------------------
# The frozen vocabulary row (the LW7 law: transport codes are closed data)
# ---------------------------------------------------------------------------------------------

# BAD_MAC is a TRANSPORT code (the BAD_JSON class): it gates BEFORE the
# op ladder and no verb row may own it -- tampering is illegal on every
# op alike. FRAME_MAC_TABLE compiles the DEFAULT rows + the code as a NEW
# contract version (the identity_binding/SRP6 precedent); DEFAULT stays
# byte-identical and PROTOCOL_DIGEST does not move.
FRAME_MAC_SPEC: dict[str, Any] = {
    "schema": DEFAULT_SPEC["schema"],
    "session_states": list(DEFAULT_SPEC["session_states"]),
    "reject_codes": list(DEFAULT_SPEC["reject_codes"]),
    "transport_reject_codes": list(DEFAULT_SPEC["transport_reject_codes"])
    + ["BAD_MAC"],
    "rows": [dict(r) for r in DEFAULT_SPEC["rows"]],
}

FRAME_MAC_TABLE = compile_table(FRAME_MAC_SPEC)
FRAME_MAC_DIGEST: str = FRAME_MAC_TABLE.digest


def _self_check() -> int:  # pragma: no cover - operability probe
    """Print one end-to-end vector: derive, seal, check. The cross-language
    vector table (V2ASK1 F3.5) is owed to the Godot client lane."""
    k = bytes(range(40))
    keys = derive(k, le_min(0xA1B2), le_min(0xC3D4))
    frame = seal(keys, C2S, {"op": "action", "sid": "s", "verb": "boil",
                             "target": "spring"}, 0)
    check(keys, C2S, 0, frame)
    print(json.dumps({"mac_id": keys.mac_id_hex, "frame": frame,
                      "digest": FRAME_MAC_DIGEST}, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_self_check())
