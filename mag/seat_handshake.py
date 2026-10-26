"""seat_handshake: Ed25519-signed seat requests for the warm MCP doors (2026-10-17).

Operator ask: "host the brain off machine ... a growing organism". Before any
door leaves loopback, every request must be attributable to a seat whose
PUBLIC key the operator put on the allowlist. This module is that check.

WIRE (one envelope for both doors, so no header plumbing is needed):

    {"mag_seat": {"seat_id": "gemini", "ts": 1760700000, "nonce": "<16-64 url-safe>",
                  "sig": "<ed25519 signature, hex>"},
     "body": "<the JSON-RPC message exactly as sent, as a string>"}

    signed bytes = b"mag-seat-handshake.v1\n" + "\n".join(
        method, sha256(body utf-8).hex(), seat_id, str(ts), nonce)

  method is the JSON-RPC "method" of body ("batch" for a list). Signing the
  body sha (not a re-serialisation) means the server checks exactly the bytes
  it forwards.

  - HTTP  POST /mcp     (mag/mcp_http.py): the JSON body IS the envelope.
  - TCP   :8766 bridge  (scripts/container/mcp_tcp_bridge.py --handshake):
          each newline-delimited line is an envelope; the bridge forwards only
          the verified inner body to the mcp_server subprocess.
  - stdio needs none: the seat spawned the process itself.

CHECKS: seat on configs/seat_allowlist.json (public keys only), signature
valid, |now - ts| <= skew (default 60 s), nonce never seen within the window
(bounded replay cache). ANY failure = silent drop: HTTP answers 404 with an
empty JSON object, TCP closes the connection. No reason ever reaches the
caller (reasons go to stderr on the server only when MAG_SEAT_HANDSHAKE_DEBUG=1).

MODE: env MAG_SEAT_HANDSHAKE = off (default: legacy behaviour, envelopes are
still verified if sent) | optional (same, explicit) | required (plain
messages are dropped). The bridge also takes --handshake.

KEYS: scripts/seat_keygen.py, run BY THE SEAT, writes the private key to a
path the seat picks outside the repo (default %USERPROFILE%/.mag_seat/<seat>.key)
and prints only the public key. Client side: sign_request()/wrap() read the
key from a path or env MAG_SEAT_KEY_PATH. This repo never stores a private key.

CRYPTO: the `cryptography` package when importable; otherwise the pure-Python
RFC 8032 code in scripts/verify_knot_v2.py (reused, not re-implemented).

Schema: seat_handshake.v1 · stdlib + optional cryptography
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import sys
import time
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_PATH = ROOT / "configs" / "seat_allowlist.json"
DOMAIN = b"mag-seat-handshake.v1\n"
SCHEMA = "seat_handshake.v1"
KEY_SCHEMA = "mag_seat_key.v1"
DEFAULT_SKEW_S = 60
# 2026-10-17 harness2: an optional "mate:" namespace so each leave-protocol mate
# holds its OWN key (seat ids like mate:jester). A colon is not a legal Windows
# filename character, so any filesystem name uses seat_slug() instead.
SEAT_RE = re.compile(r"^(?:mate:)?[A-Za-z0-9][A-Za-z0-9_.-]{0,31}$")
MATE_PREFIX = "mate:"
ENV_KEY_DIR = "MAG_SEAT_KEY_DIR"  # override of ~/.mag_seat (tests, other hosts)
NONCE_RE = re.compile(r"^[A-Za-z0-9_-]{16,64}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
HEX128 = re.compile(r"^[0-9a-f]{128}$")
ENV_KEY_PATH = "MAG_SEAT_KEY_PATH"
ENV_MODE = "MAG_SEAT_HANDSHAKE"
MODES = ("off", "optional", "required")


# ─────────────────────────────── Ed25519 ──────────────────────────────────

def _pure():
    """scripts/verify_knot_v2.py pure RFC 8032 functions (reused)."""
    scripts = str(ROOT / "scripts")
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import verify_knot_v2 as vk  # type: ignore

    return vk


def _have_cryptography() -> bool:
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: F401
    except Exception:  # noqa: BLE001
        return False
    return True


def public_from_seed(seed: bytes) -> bytes:
    if _have_cryptography():
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        return Ed25519PrivateKey.from_private_bytes(seed).public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return _pure().ed25519_public_reference(seed)


def sign_bytes(seed: bytes, msg: bytes) -> bytes:
    if _have_cryptography():
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

        return Ed25519PrivateKey.from_private_bytes(seed).sign(msg)
    return _pure().ed25519_sign_reference(seed, msg)


def verify_bytes(public: bytes, msg: bytes, sig: bytes) -> bool:
    if len(public) != 32 or len(sig) != 64:
        return False
    if _have_cryptography():
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

        try:
            Ed25519PublicKey.from_public_bytes(public).verify(sig, msg)
            return True
        except (InvalidSignature, ValueError):
            return False
    try:
        return bool(_pure().ed25519_verify_pure(public, msg, sig))
    except Exception:  # noqa: BLE001
        return False


def generate_seed() -> bytes:
    return secrets.token_bytes(32)


# ─────────────────────────────── keys ─────────────────────────────────────

def seat_slug(seat_id: str) -> str:
    """Filesystem-safe form of a seat id ("mate:jester" -> "mate__jester")."""
    return str(seat_id).replace(":", "__")


def default_key_path(seat_id: str) -> Path:
    """Where a seat key lives by default, always OUTSIDE the repo:
    ~/.mag_seat/<seat>.key, mates under ~/.mag_seat/mates/mate__<name>.key."""
    base = os.environ.get(ENV_KEY_DIR, "").strip()
    root = Path(base) if base else Path(os.environ.get("USERPROFILE") or Path.home()) / ".mag_seat"
    if str(seat_id).startswith(MATE_PREFIX):
        root = root / "mates"
    return root / f"{seat_slug(seat_id)}.key"


def fingerprint(public_hex: str) -> str:
    """Short public-key fingerprint: sha256(raw public key)[:16] hex."""
    return hashlib.sha256(bytes.fromhex(public_hex)).hexdigest()[:16]


def key_record(seat_id: str, seed: bytes) -> dict[str, Any]:
    if not SEAT_RE.fullmatch(seat_id or ""):
        raise ValueError(f"seat_id must match {SEAT_RE.pattern}")
    return {"schema": KEY_SCHEMA, "seat_id": seat_id, "private_seed_hex": seed.hex(),
            "public_hex": public_from_seed(seed).hex(),
            "created": datetime.now(timezone.utc).isoformat()}


def load_key(path: str | Path | None = None) -> tuple[str, bytes]:
    """(seat_id, seed) from a seat key file; path or env MAG_SEAT_KEY_PATH."""
    p = path or os.environ.get(ENV_KEY_PATH, "").strip()
    if not p:
        raise ValueError(f"no seat key: pass a key path or set {ENV_KEY_PATH}")
    rec = json.loads(Path(p).read_text(encoding="utf-8"))
    if rec.get("schema") != KEY_SCHEMA or not HEX64.fullmatch(str(rec.get("private_seed_hex", ""))):
        raise ValueError("not a mag seat key file")
    seat_id = str(rec.get("seat_id") or "")
    if not SEAT_RE.fullmatch(seat_id):
        raise ValueError("seat key has an invalid seat_id")
    return seat_id, bytes.fromhex(rec["private_seed_hex"])


# ─────────────────────────────── allowlist ────────────────────────────────

def load_allowlist(path: str | Path | None = None) -> dict[str, Any]:
    p = Path(path) if path else ALLOWLIST_PATH
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"seats": {}}
    return data if isinstance(data, dict) else {"seats": {}}


def seat_public(allowlist: dict[str, Any], seat_id: str) -> bytes | None:
    row = (allowlist.get("seats") or {}).get(seat_id)
    if not isinstance(row, dict) or row.get("revoked"):
        return None
    pub = str(row.get("public_hex") or "").lower()
    return bytes.fromhex(pub) if HEX64.fullmatch(pub) else None


# ─────────────────────────────── signing ──────────────────────────────────

def body_method(body: str) -> str:
    try:
        msg = json.loads(body)
    except ValueError:
        return ""
    if isinstance(msg, list):
        return "batch"
    return str(msg.get("method") or "") if isinstance(msg, dict) else ""


def canonical(method: str, body: str | bytes, seat_id: str, ts: int, nonce: str) -> bytes:
    raw = body.encode("utf-8") if isinstance(body, str) else bytes(body)
    fields = [method, hashlib.sha256(raw).hexdigest(), seat_id, str(int(ts)), nonce]
    if any("\n" in f for f in fields):
        raise ValueError("handshake fields may not contain newlines")
    return DOMAIN + "\n".join(fields).encode("utf-8")


def sign_request(method: str, body: str | bytes, *, key_path: str | Path | None = None,
                 seed: bytes | None = None, seat_id: str | None = None,
                 now: float | None = None, nonce: str | None = None) -> dict[str, Any]:
    """Handshake fields for one request. Key from seed+seat_id, key_path, or env."""
    if seed is None:
        seat_id, seed = load_key(key_path)
    if not seat_id or not SEAT_RE.fullmatch(seat_id):
        raise ValueError("seat_id required")
    ts = int(now if now is not None else time.time())
    nonce = nonce or secrets.token_urlsafe(18)
    sig = sign_bytes(seed, canonical(method, body, seat_id, ts, nonce))
    return {"seat_id": seat_id, "ts": ts, "nonce": nonce, "sig": sig.hex()}


def wrap(body: str, **kw: Any) -> dict[str, Any]:
    """Envelope for one JSON-RPC message string (HTTP body or one TCP line)."""
    return {"mag_seat": sign_request(body_method(body), body, **kw), "body": body}


def verify_signature(method: str, body: str | bytes, fields: dict[str, Any],
                     allowlist: dict[str, Any]) -> str | None:
    """Pure signature + allowlist check (no clock, no replay). seat_id or None."""
    try:
        seat_id = str(fields.get("seat_id") or "")
        nonce = str(fields.get("nonce") or "")
        ts = int(fields.get("ts"))
        sig_hex = str(fields.get("sig") or "").lower()
    except (TypeError, ValueError):
        return None
    if not (SEAT_RE.fullmatch(seat_id) and NONCE_RE.fullmatch(nonce) and HEX128.fullmatch(sig_hex)):
        return None
    pub = seat_public(allowlist, seat_id)
    if pub is None:
        return None
    try:
        msg = canonical(method, body, seat_id, ts, nonce)
    except ValueError:
        return None
    return seat_id if verify_bytes(pub, msg, bytes.fromhex(sig_hex)) else None


# ─────────────────────────────── replay + verify ──────────────────────────

class ReplayCache:
    """Bounded (seat, nonce) memory; entries older than ttl_s are forgotten."""

    def __init__(self, max_entries: int = 8192, ttl_s: float = 2 * DEFAULT_SKEW_S + 5):
        self.max_entries = max_entries
        self.ttl_s = ttl_s
        self._seen: OrderedDict[tuple[str, str], float] = OrderedDict()

    def _evict(self, now: float) -> None:
        while self._seen:
            key, t = next(iter(self._seen.items()))
            if now - t > self.ttl_s or len(self._seen) > self.max_entries:
                self._seen.popitem(last=False)
            else:
                break

    def seen_or_add(self, seat_id: str, nonce: str, now: float) -> bool:
        self._evict(now)
        key = (seat_id, nonce)
        if key in self._seen:
            return True
        self._seen[key] = now
        if len(self._seen) > self.max_entries:
            self._seen.popitem(last=False)
        return False

    def __len__(self) -> int:
        return len(self._seen)


_CACHE = ReplayCache()


def _debug(reason: str) -> None:
    if os.environ.get("MAG_SEAT_HANDSHAKE_DEBUG") == "1":
        sys.stderr.write(f"[seat_handshake] drop: {reason}\n")


def verify_envelope(env: Any, *, allowlist: dict[str, Any] | None = None,
                    cache: ReplayCache | None = None, now: float | None = None,
                    skew_s: int | None = None) -> tuple[str, str] | None:
    """(seat_id, inner_body) when the envelope passes every check, else None."""
    if not is_envelope(env):
        _debug("not an envelope")
        return None
    allowlist = allowlist if allowlist is not None else load_allowlist()
    cache = cache if cache is not None else _CACHE
    skew = int(skew_s if skew_s is not None else allowlist.get("skew_s", DEFAULT_SKEW_S))
    fields, body = env["mag_seat"], env["body"]
    t = time.time() if now is None else now
    try:
        if abs(t - int(fields.get("ts"))) > skew:
            _debug("skew")
            return None
    except (TypeError, ValueError):
        return None
    seat_id = verify_signature(body_method(body), body, fields, allowlist)
    if seat_id is None:
        _debug("signature/allowlist")
        return None
    if cache.seen_or_add(seat_id, str(fields["nonce"]), t):
        _debug("replay")
        return None
    return seat_id, body


def is_envelope(obj: Any) -> bool:
    return (isinstance(obj, dict) and isinstance(obj.get("mag_seat"), dict)
            and isinstance(obj.get("body"), str))


def mode(override: str | None = None) -> str:
    m = (override or os.environ.get(ENV_MODE, "off")).strip().lower()
    return m if m in MODES else "required"  # unknown value fails closed


# 404-style silent drop for HTTP (no detail, same shape as "no such route").
DROP_HTTP: tuple[int, dict[str, Any]] = (404, {})
