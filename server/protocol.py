"""protocol: OUR wire protocol v0: line-based JSON over TCP.

Simple, debuggable, ours. One JSON object per line (newline = \\n, UTF-8),
both directions. You can drive the whole server from a terminal with
telnet/nc if you ever need to. No binary framing, no versioning headers:
v0 earns the right to exist before it earns the right to be clever.

Client to server:
    {"op":"hello","user":str,"pass":str}          v0 plaintext fallback (flag-gated)
    {"op":"srp_register","user":str,"pass":str}   SRP6 enrollment (B4): the one
                                                  moment the secret crosses the
                                                  wire; the server keeps only
                                                  salt + verifier
    {"op":"srp_challenge","user":str,"a":hex}     SRP6 step 1: client public A
    {"op":"srp_proof","user":str,"m1":hex}        SRP6 step 2: client proof M1
    {"op":"action","sid":str,"verb":str,"target":str}

Server to client:
    {"op":"welcome","sid":str,"world":<snapshot dict>}
    {"op":"srp_registered","user":str}            account stored (salt+verifier)
    {"op":"srp_challenge","user":str,"salt":hex,"b":hex}
                                                  SRP6 step 1 reply: salt + B
    {"op":"welcome","sid":str,"m2":hex,"auth":"srp6","world":...}
                                                  SRP6 success: server proof M2
                                                  + the same session welcome
    {"op":"ack",...}          action staged, applies at next tick
    {"op":"reject","why":str} typed refusal (see REJECT_CODES)
    {"op":"tick","n":int,"nodes":{name:vol},"events":[str],"winner":bool}

SRP6 note (B4, 2026-09-30): the handshake verbs are frozen table rows
(SRP6_AUTH_TABLE in server/protocol_table.py; the math lives in
server/auth_srp6.py, ported from the realmd-proven tools/realmd_client).
All SRP6 integers ride as lowercase hex; the operand byte order is
little-endian everywhere, the convention the live realmd proved. Login
proof failures reject BAD_PROOF; a proof with no pending single-use
challenge (a replay) rejects STALE_CHALLENGE — both codes ride the
SRP6_AUTH_TABLE's closed vocabulary. hello stays as the flag-gated
plaintext fallback (WorldServer(allow_plaintext_hello=...)) until SRP6
is the standing default; unknown-user and wrong-password still share one
code (BAD_AUTH / BAD_PROOF) so the wire does not enumerate users.

Frame MAC (R3, 2026-09-30, receipt watch/inbox/last_mile_20260930/
R3_FRAME_MAC.md; spec: watch/inbox/frontier_asks/volley2/results/V2ASK1.md,
Q03): after a successful SRP6 proof the session holds K, and every
post-auth line-JSON frame from that connection carries two fields,
    "seq"  int, per-direction counter starting at 0 (client->server and
          server->client count independently)
    "mac"  32 lowercase hex chars = HMAC-SHA256(k_dir, domain || canonical
          body)[:16], where the canonical body is the frame WITHOUT its
          "mac" field in the house canonical form (sorted keys, compact
          separators -- the world.row_sha law: the digest covers the row
          minus its own field). Keys derive per direction from the
          handshake (HKDF over K salted with SHA256(A||B)); the math and
          the derivation live in server/frame_mac.py.
The server verifies BEFORE processing (gate order: decode -> MAC -> op
ladder, so a tampered frame never reaches the nonce gate). Any bad tag,
wrong/replayed seq, malformed mac field, or a bare frame after the
session went MAC-sticky is tamper: reject BAD_MAC, append a
kind:mac_tamper row to the world's hash chain, disconnect. Never resync,
never downgrade within a session.
Migration, not breakage: the plaintext hello door carries no K and stays
bare; an SRP6 client that never sends "mac" fields stays legal while
WorldServer(require_frame_mac=False) (the default) -- its frames process
as today. Flip the flag and every frame after SRP6 auth must carry a
valid MAC. Server->client DIRECT replies (welcome, ack, reject) are
sealed with the s2c key; broadcast ticks stay bare (the encode-once
determinism law -- full s2c broadcast sealing is the TLS-phase lane).

Action rejection codes (the five the v0 spec fixes):
    UNKNOWN_SID      action arrived with a sid the world never issued
    NOT_YOUR_TURN    RESERVED, not applicable in v0: there is no turn
                     structure, any authed client may act at any time.
                     The code exists so v1 turn modes do not invent a
                     new vocabulary mid-stream. v0 never emits it.
    UNKNOWN_VERB     verb not in VERBS
    UNKNOWN_TARGET   target is neither a node nor (for valve) a pipe
    DRY_POOL         boil/tag on a pool holding zero water

Transport rejection codes (outside the action-validation five):
    BAD_AUTH         hello failed (unknown user or wrong password; one
                     code for both so the wire does not enumerate users)
    BAD_JSON         line was not a JSON object
    UNKNOWN_OP       op is not hello/action

Determinism note: encode() is canonical (sorted keys, compact separators)
so identical payloads produce byte-identical lines. Broadcasts are encoded
once per tick and the same bytes go to every client.

Table note (2026-09-29, W1): the verb and reject vocabularies below are no
longer literals here; they are re-exported from server/protocol_table.py,
the frozen verbs-as-data layer (rows of verb/required_state/handler_name/
reject_code + state enums + protocol_digest over the canonical table
bytes). The values and order are byte-identical to the v0 spec, so every
existing import keeps working; the table is now the source of truth behind
them. NOT_YOUR_TURN has machinery there (a required_state column: compile a
TURN_HELD row and the gate emits it) while the v0 table still never does.
"""
from __future__ import annotations

import json
from typing import Any

from server import frame_mac  # noqa: E402 - R3: the post-auth MAC law
from server.protocol_table import (  # noqa: E402,F401 - re-exported surface
    DEFAULT_TABLE,
    PROTOCOL_DIGEST,
    REJECT_CODES,
    TRANSPORT_REJECT_CODES,
    VERBS,
)

MAX_LINE = 65536  # bytes; asyncio stream reader limit


def encode(msg: dict[str, Any]) -> bytes:
    """Canonical wire form: sorted keys, compact, newline-terminated."""
    return json.dumps(msg, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"


def decode_line(line: bytes) -> dict[str, Any]:
    """Parse one wire line. Raises ValueError on anything that is not a
    JSON object."""
    if len(line) > MAX_LINE:
        raise ValueError("line exceeds MAX_LINE")
    text = line.decode("utf-8").strip()
    if not text:
        raise ValueError("empty line")
    msg = json.loads(text)
    if not isinstance(msg, dict):
        raise ValueError("wire line is not a JSON object")
    return msg


# ------------------------------------------------------------ builders ----

def hello(user: str, password: str) -> dict[str, Any]:
    return {"op": "hello", "user": user, "pass": password}


def action(sid: str, verb: str, target: str) -> dict[str, Any]:
    return {"op": "action", "sid": sid, "verb": verb, "target": target}


# ------------------------------------------------------- SRP6 (B4, 2026-09-30) ----


def srp_register(user: str, password: str) -> dict[str, Any]:
    """Enrollment: the one op that carries the secret. Server stores salt +
    verifier only (server/auth_srp6.py)."""
    return {"op": "srp_register", "user": user, "pass": password}


def srp_challenge(user: str, a_hex: str) -> dict[str, Any]:
    """Handshake step 1: the client's public ephemeral A (lowercase hex)."""
    return {"op": "srp_challenge", "user": user, "a": a_hex}


def srp_proof(user: str, m1_hex: str) -> dict[str, Any]:
    """Handshake step 2: the client's proof M1 (lowercase hex, 20 bytes)."""
    return {"op": "srp_proof", "user": user, "m1": m1_hex}


def srp_challenge_ok(user: str, salt_hex: str, b_hex: str) -> dict[str, Any]:
    return {"op": "srp_challenge", "user": user, "salt": salt_hex, "b": b_hex}


def srp_registered(user: str) -> dict[str, Any]:
    return {"op": "srp_registered", "user": user}


def srp_welcome(sid: str, m2_hex: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    """Proof success: the server proof M2 plus the standard session welcome
    (same op as hello's, so client session handling is one shape)."""
    return {"op": "welcome", "sid": sid, "m2": m2_hex, "auth": "srp6",
            "world": snapshot}


def welcome(sid: str, snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"op": "welcome", "sid": sid, "world": snapshot}


def reject(why: str, **extra: Any) -> dict[str, Any]:
    msg: dict[str, Any] = {"op": "reject", "why": why}
    msg.update(extra)
    return msg


def ack(verb: str, target: str, user: str, applies_at_tick: int) -> dict[str, Any]:
    return {
        "op": "ack",
        "verb": verb,
        "target": target,
        "user": user,
        "applies_at_tick": applies_at_tick,
    }


# -------------------------------------------------- frame MAC fields (R3, 2026-09-30)

# The two wire fields a post-auth frame carries (the docstring law above).
MAC_SEQ_FIELD = "seq"
MAC_FIELD = "mac"


def with_mac(msg: dict[str, Any], keys: frame_mac.FrameKeys, seq: int,
             direction: bytes = frame_mac.C2S) -> dict[str, Any]:
    """Attach the R3 frame MAC: returns a NEW dict = msg + "seq" + "mac".
    Pure sugar over frame_mac.seal so client-side wire builders (action,
    srp frames) seal through the same surface they build on. The server
    verifies with frame_mac.check before the op ladder runs."""
    return frame_mac.seal(keys, direction, msg, seq)
