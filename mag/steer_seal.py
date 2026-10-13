#!/usr/bin/env python3
"""STEER SEAL - anti-forgery gate for steering directives (A1, 2026-10-01).

Spec: watch/inbox/hermes_burn/A1_steer_antiforgery_ASSEMBLED.md (+ the
reasoning channel A1_steer_antiforgery.md for every decision below).

- HMAC-SHA256 envelope over canonical JSON (sort_keys, tight separators,
  UTF-8): version, key_id, nonce, timestamp, payload; mac over those five.
- Keyfile OUTSIDE ROOT (default %USERPROFILE%/.mag/steer_seal_key), hex
  >= 256 bits, key_id = sha256(key) prefix; optional JSON map for rotation
  (ids self-checked). MAG_STEER_SEAL_HOME moves the whole seal state.
- Replay: exclusive-create nonce markers in a seen-dir outside ROOT;
  reuse fails verify even inside the freshness window.
- Mode: sentinel file outside ROOT ("warn"|"enforce"); env
  MAG_STEER_SEAL_MODE / mode= override; missing = warn (migration).
  Missing keyfile in enforce fails closed.
- SAFE-FAIL: restrictive words (STOP HALT PAUSE WAIT HOLD NO STAND DOWN,
  whole-message only; "kill" dropped as ambiguous) honored even on verify
  failure; permit needs a verified seal (warn mode passes with a warning).
- NFC, never NFKC: lookalikes stay distinct codepoints; NFKC would fold
  fullwidth "GO" into a permit word. 0600 keyfile check is POSIX-only
  (win32 has no mode bits; outside-ROOT path is the boundary there).
- Mint: ingress adapters seal() at receipt time (no local signing CLI by
  intent). Single admit path: admit_text()/admit() -> one _gate() core ->
  verify() exactly once; failures honor the restrictive default.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import string
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

VERSION = 1
FRESHNESS_SECONDS = 300
MIN_KEY_BITS = 256
KEY_ID_HEX_CHARS = 16  # sha256(key) hex prefix

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "memory" / "runs" / "steer_seal_log.jsonl"

# Closed restrictive grammar (interrupt law: a forged STOP costs a pause; a
# blocked real STOP costs the run). Whole-message match only; "kill" dropped.
RESTRICTIVE_WORDS = frozenset({"STOP", "HALT", "PAUSE", "WAIT", "HOLD", "NO", "STAND DOWN"})

_NONCE_RE = re.compile(r"[0-9a-fA-F]{8,128}")
_PUNCT_TO_SPACE = str.maketrans({c: " " for c in string.punctuation})

class VerifyError(Exception):
    """Any contract violation: parse, version, key, mac, nonce, timestamp."""

class SteerRefused(VerifyError):
    """The gate refused a permit word without verified operator authority."""

class Admitted(NamedTuple):
    text: str       # operative words to steer with (envelope payload if sealed)
    authority: str  # "operator-seal" | "unverified-restrictive" | "unverified-warn"
    event: str

def _seal_home() -> Path:
    """MAG_STEER_SEAL_HOME moves the outside-ROOT seal state (HERMES_HOME
    precedent); default %USERPROFILE%/.mag."""
    env = os.environ.get("MAG_STEER_SEAL_HOME")
    return Path(env) if env else Path.home() / ".mag"

def default_keyfile() -> Path:
    return _seal_home() / "steer_seal_key"

def default_seen_dir() -> Path:
    return _seal_home() / "steer_seal_seen"

def default_mode_path() -> Path:
    return _seal_home() / "steer_seal_mode"

def resolve_mode(explicit: str | None = None) -> str:
    """warn | enforce: explicit arg > env MAG_STEER_SEAL_MODE > sentinel > warn."""
    if explicit is not None:
        m = explicit.strip().lower()
        if m not in ("warn", "enforce"):
            raise VerifyError(f"unknown mode {explicit!r}")
        return m
    env = os.environ.get("MAG_STEER_SEAL_MODE", "").strip().lower()
    if env in ("warn", "enforce"):
        return env
    v = ""
    try:
        v = default_mode_path().read_text(encoding="utf-8").strip().lower()
    except OSError:
        v = ""  # a missing sentinel is the normal warn-default state
    if v in ("warn", "enforce"):
        return v
    if v:
        _log_event("mode_sentinel_garbage", v)
    return "warn"

def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def _log_event(event: str, text: str = "", extra: dict | None = None) -> None:
    """Audit receipt. Best-effort by design: a log failure never changes the
    gate decision, but it is never silent either (one stderr line)."""
    if LOG is None:
        return
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        row = {"ts": _now_iso(), "event": event, "text": (text or "")[:80]}
        row.update(extra or {})
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    except Exception as exc:
        sys.stderr.write(f"steer_seal: audit log write failed "
                         f"({exc.__class__.__name__}); gate decision stands\n")

def key_id_for(key: bytes) -> str:
    return hashlib.sha256(key).hexdigest()[:KEY_ID_HEX_CHARS]

def write_keyfile(path: str | Path, key: bytes | None = None, *, force: bool = False) -> str:
    """Create the keyfile (exclusive create unless force). Returns key_id."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    key = key if key is not None else os.urandom(32)
    if len(key) * 8 < MIN_KEY_BITS:
        raise VerifyError(f"key must be >= {MIN_KEY_BITS} bits")
    if force:
        tmp = path.with_name(f"{path.name}.tmp-{os.getpid()}")
        tmp.write_text(key.hex() + "\n", encoding="utf-8")
        os.replace(tmp, path)
    else:
        try:
            fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise VerifyError(f"keyfile exists: {path} (pass force to replace)")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(key.hex() + "\n")
    return key_id_for(key)

def _checked_key(hexval, kid: str | None = None) -> bytes:
    """hex -> key bytes, enforcing hex form, >= MIN_KEY_BITS, and (map form,
    kid given) the sha256-prefix id self-check."""
    try:
        key = bytes.fromhex(hexval if isinstance(hexval, str) else "")
    except ValueError:
        raise VerifyError("keyfile is neither hex nor a JSON key map"
                          if kid is None else f"keyfile entry {kid!r} is not hex")
    if len(key) * 8 < MIN_KEY_BITS:
        raise VerifyError(f"keyfile key < {MIN_KEY_BITS} bits")
    if kid is not None and key_id_for(key) != kid:
        raise VerifyError(f"keyfile entry {kid!r} id != sha256 prefix")
    return key

def load_keys(path: str | Path | None = None) -> dict[str, bytes]:
    """Keyfile -> {key_id: key_bytes}. Bare hex (single key, id derived) or
    JSON map for rotation. Any contract violation raises VerifyError;
    callers treat that as "no authority can be minted"."""
    p = Path(path) if path is not None else default_keyfile()
    try:
        st = os.stat(p)
    except OSError as exc:
        raise VerifyError(f"keyfile missing: {p} ({exc.__class__.__name__})")
    # POSIX-only 0600 check (spec sketch); win32 has no mode bits, so there
    # the outside-ROOT path alone is the boundary.
    if os.name == "posix" and st.st_mode & 0o077:
        raise VerifyError("keyfile permissions too open (want 0600)")
    raw = p.read_text(encoding="utf-8").strip()
    if not raw:
        raise VerifyError("keyfile empty")
    if not raw.startswith("{"):
        key = _checked_key(raw)
        return {key_id_for(key): key}
    try:
        obj = json.loads(raw)
    except ValueError as exc:
        raise VerifyError(f"keyfile JSON invalid: {exc}")
    if not isinstance(obj, dict) or not obj:
        raise VerifyError("keyfile map form must be a non-empty object")
    return {kid: _checked_key(hexval, kid) for kid, hexval in obj.items()}

def canonical(env: dict) -> bytes:
    """Canonical serialization of the covered fields. Type-strict: an
    attacker cannot sneak a non-str payload or a float timestamp through."""
    covered = {}
    for name in ("version", "key_id", "nonce", "timestamp", "payload"):
        if name not in env:
            raise VerifyError(f"envelope missing {name}")
        v = env[name]
        if name in ("version", "timestamp"):
            if isinstance(v, bool) or not isinstance(v, int):
                raise VerifyError(f"{name} must be an int")
        elif not isinstance(v, str):
            raise VerifyError(f"{name} must be a str")
        covered[name] = v
    return json.dumps(covered, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")

def compute_mac(key: bytes, env: dict) -> str:
    return hmac.new(key, canonical(env), hashlib.sha256).hexdigest()

def seal(payload: str, key: bytes | None = None, *, keyfile: str | Path | None = None,
         nonce: str | None = None, timestamp: int | None = None) -> dict:
    """Mint a sealed envelope. key= direct, else loaded from keyfile (which
    must then hold exactly one key). nonce/timestamp injectable for tests."""
    if not isinstance(payload, str):
        raise VerifyError("payload must be str (the verbatim steer text)")
    if key is None:
        keys = load_keys(keyfile if keyfile is not None else default_keyfile())
        if len(keys) != 1:
            raise VerifyError("keyfile holds multiple keys; pass key= explicitly")
        key_id, key = next(iter(keys.items()))
    else:
        if len(key) * 8 < MIN_KEY_BITS:
            raise VerifyError(f"key must be >= {MIN_KEY_BITS} bits")
        key_id = key_id_for(key)
    env = {
        "version": VERSION,
        "key_id": key_id,
        "nonce": nonce if nonce is not None else os.urandom(16).hex(),
        "timestamp": timestamp if timestamp is not None else int(time.time()),
        "payload": payload,
    }
    env["mac"] = compute_mac(key, env)
    return env

def _no_dupes(pairs):
    """object_pairs_hook: reject duplicate keys (json.loads otherwise keeps
    the last duplicate silently - reasoning-channel negative case)."""
    out = {}
    for k, v in pairs:
        if k in out:
            raise VerifyError(f"duplicate envelope key {k!r}")
        out[k] = v
    return out

def parse_envelope(text: str) -> dict:
    """Strict parse: JSON object, no duplicate keys. Raises VerifyError."""
    try:
        obj = json.loads(text, object_pairs_hook=_no_dupes)
    except VerifyError:
        raise
    except ValueError as exc:
        raise VerifyError(f"envelope not valid JSON: {exc}")
    if not isinstance(obj, dict):
        raise VerifyError("envelope must be a JSON object")
    return obj

def _try_parse_envelope(text: str) -> dict | None:
    """None when the text is plainly not an envelope (no leading '{')."""
    t = (text or "").lstrip()
    if not t.startswith("{"):
        return None
    try:
        return parse_envelope(t)
    except VerifyError:
        return None  # broken envelope attempt falls through as unsealed text

def classify(text: str) -> str:
    """"restrictive" iff the WHOLE message matches the closed grammar.

    NFC only: a mixed-script lookalike "STOP" (Cyrillic Te/O/Er) stays
    distinct codepoints and is NOT restrictive. NFKC is banned because it
    would fold fullwidth "GO" into a real permit word."""
    norm = unicodedata.normalize("NFC", text or "")
    norm = norm.upper().translate(_PUNCT_TO_SPACE)
    norm = " ".join(norm.split())
    return "restrictive" if norm in RESTRICTIVE_WORDS else "permit"

class FileNonceStore:
    """Seen-nonce dir of marker files. Exclusive create is the atomic claim:
    two processes can never both record the same nonce. Markers older than
    twice the freshness window are pruned (grace so an in-window nonce is
    never evicted early)."""

    def __init__(self, dirpath: str | Path):
        self.dir = Path(dirpath)

    def check_and_record(self, nonce, now: int) -> None:
        if not isinstance(nonce, str) or not _NONCE_RE.fullmatch(nonce):
            raise VerifyError("bad nonce (want 8-128 hex chars)")
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
            marker = self.dir / f"{nonce.lower()}.seen"
            fd = os.open(str(marker), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            raise VerifyError("nonce reuse")
        except OSError as exc:
            raise VerifyError(f"nonce store error: {exc.__class__.__name__}")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(str(now))
        # Eviction runs on REAL wall time, never the injectable verify clock:
        # comparing marker mtimes against a caller-frozen `now` deleted
        # just-recorded markers (caught by the frozen-clock replay test).
        self._evict()

    def _evict(self) -> None:
        cutoff = time.time() - 2 * FRESHNESS_SECONDS
        try:
            markers = list(self.dir.glob("*.seen"))
        except OSError as exc:
            sys.stderr.write(f"steer_seal: nonce eviction scan failed "
                             f"({exc.__class__.__name__}); exclusive-create still protects\n")
            return
        for p in markers:
            try:
                if p.stat().st_mtime < cutoff:
                    p.unlink()
            except OSError:
                continue  # unremovable stale marker; the next evict retries

def verify(env, *, keys: dict[str, bytes] | None = None,
           keyfile: str | Path | None = None, seen_dir: str | Path | None = None,
           now: int | None = None) -> bool:
    """True only on full affirmation (version -> key -> mac -> timestamp ->
    nonce). Any exception, missing/unreadable keyfile, ambiguous shape, or
    store error is a verify failure (safe-fail: never a "proceed")."""
    try:
        if not isinstance(env, dict):
            return False
        v = env.get("version")
        if isinstance(v, bool) or v != VERSION:
            raise VerifyError("unsupported version")
        ks = keys if keys is not None else load_keys(
            keyfile if keyfile is not None else default_keyfile())
        kid = env.get("key_id")
        key = ks.get(kid) if isinstance(kid, str) else None
        if key is None:
            raise VerifyError("unknown key_id")
        if not isinstance(env.get("mac"), str):
            raise VerifyError("mac missing")
        expected = compute_mac(key, env)  # type checks raise inside canonical()
        if not hmac.compare_digest(expected, env["mac"]):
            raise VerifyError("mac mismatch")
        ts = env["timestamp"]
        if isinstance(ts, bool) or not isinstance(ts, int):
            raise VerifyError("bad timestamp")
        now_v = now if now is not None else int(time.time())
        if abs(now_v - ts) > FRESHNESS_SECONDS:
            raise VerifyError("stale timestamp")
        FileNonceStore(seen_dir if seen_dir is not None else default_seen_dir()).check_and_record(
            env["nonce"], now_v)
        return True
    except VerifyError:
        return False
    except Exception:
        return False

def _gate(text: str, env: dict | None, *, mode: str | None, keyfile, seen_dir, now) -> Admitted:
    if env is not None and verify(env, keyfile=keyfile, seen_dir=seen_dir, now=now):
        return Admitted(env["payload"], "operator-seal", "sealed_admitted")
    # Safe-fail: restrictive honored even on verify failure, missing key, or
    # no envelope at all. Envelope payloads count too (a broken seal whose
    # payload says STOP is still honored - interrupt law beats MAC law).
    payload = env.get("payload") if isinstance(env, dict) else None
    if classify(text) == "restrictive" or (
            isinstance(payload, str) and classify(payload) == "restrictive"):
        honored = payload if isinstance(payload, str) and classify(payload) == "restrictive" else text
        _log_event("unsealed_restrictive_honored", honored)
        return Admitted(honored, "unverified-restrictive", "unsealed_restrictive_honored")
    # Permit word without verified authority. Name whether the keyfile is
    # even loadable (missing keyfile in enforce = nobody can mint authority).
    reason = "unsealed"
    try:
        load_keys(keyfile if keyfile is not None else default_keyfile())
    except VerifyError as exc:
        reason = str(exc)
    if resolve_mode(mode) == "enforce":
        _log_event("permit_refused_enforce", text, {"reason": reason})
        raise SteerRefused(
            f"unsealed permit word refused in enforce mode ({reason}); "
            f"seal it first via mag.steer_seal.seal() at a trusted ingress")
    _log_event("unsealed_permit_warned", text, {"reason": reason})
    return Admitted(text, "unverified-warn", "unsealed_permit_warned")

def admit_text(text: str, *, mode: str | None = None, keyfile: str | Path | None = None,
               seen_dir: str | Path | None = None, now: int | None = None) -> Admitted:
    """The wired gate: steering words enter here BEFORE the steer executes.
    Inline envelope JSON is verified and unwrapped; plain text is classified;
    restrictive always passes; unsealed permit passes only in warn mode
    (with a logged warning)."""
    return _gate(text, _try_parse_envelope(text), mode=mode, keyfile=keyfile,
                 seen_dir=seen_dir, now=now)

def admit(path: str | Path, *, mode: str | None = None, keyfile: str | Path | None = None,
          seen_dir: str | Path | None = None, now: int | None = None) -> Admitted:
    """File-directive form (spec admit(path)): reads bytes, STRICT envelope
    parse (a non-envelope directive file is a verify failure, never a raw
    fallback), then the same single gate."""
    try:
        data = Path(path).read_bytes()
    except OSError as exc:
        raise VerifyError(f"directive unreadable: {exc.__class__.__name__}")
    text = data.decode("utf-8", errors="replace")
    return _gate(text, parse_envelope(text), mode=mode, keyfile=keyfile,
                 seen_dir=seen_dir, now=now)
