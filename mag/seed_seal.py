"""seed_seal - SS-1: the Ed25519 seed-seal over the arc-seed export.

Spec: watch/inbox/localfirst/pam.md clause "The estate port" (PAM DIG RECEIPT,
lane pam, 2026-10-01); ticket SS-1 = GAP_REGISTER rank 5
(watch/inbox/gap_analysis_20261001/GAP_REGISTER.md). Key-custody shape follows
the landed AH2 pattern in mag/proof.py (hex-seed key file, mint-on-first-use,
0600 where the OS supports it, never committed).

THE PAM LESSON, PORTED: hashes alone are forgeable by anyone - an attacker who
tampered bytes can recompute every sha256. The only trust anchor is an Ed25519
signature the attacker cannot mint. PAM's own consume path skips that anchor
(its verify() with no key returns True on forged content, live-proven in
watch/inbox/gala_20260925/localfirst-steal/lanes/pam.check.txt section 4).
This module is the opposite shape: verify_seed() is FAIL-CLOSED on every
path - missing seal, missing signature, tampered bytes, rehashed tamper,
swapped key - and returns ok=False with the reason, never a silent pass.

SIGN-THE-ROOT-NOT-THE-BODY (the ask's phrase, per spec clause 1):
    seed_root = sha256(canonical_json{arc_root, chain_sha, seed_sha, session})
    signature = Ed25519(private_key, seed_root_hex.utf-8)
The signature covers the root; the root covers BOTH file byte strings
(seed .md AND chain .json) plus the arc identity (session, arc_root). Unlike
PAM's ID-list-only root (its spec-vs-code drift, pam.md section 6), no body
byte is left outside the signature - a seed has no per-entry hashes to lean on.

KEY CUSTODY, NOT PAM'S WAY (spec clause 3): the private key lives OUTSIDE the
seed dir, in state/keys/seed_seal_key (hex seed; state/ is gitignored by
.gitignore lines 40-42, so the key never lands in git). The PUBLIC key travels
inline inside the .seal sidecar, because the verifying falsifier may be a
stranger seat with no shared secret; key_id (sha256 over a domain-separated
pubkey, 16 hex) gives strangers a rotation path. PAM's raw unencrypted
~/.pam/keys/agent.key with no key-ID is rated HIGH by its own audit (SEC-004).
win32 has no enforceable mode bits; 0600 is attempted and the gitignore +
never-commit law carries custody there (same accepted debt as mag/proof.py).

THE ENFORCING FLIP IS DELIBERATELY NOT LANDED (SS-1 boundary): this module
ARMS the capability - sign, verify, keygen - but nothing in mag/arc_seed.py or
any consumer REFUSES an unsealed/forged seed yet. Making consumption reject
ok=False is the operator's gated flip: call verify_seed() at the consume site
and treat failure as fatal. Until that order, these are opt-in tools.

Schema: seed_seal.v1 · CLI: python -m mag.seed_seal sign|verify|keyinfo
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
KEYS_DIR = ROOT / "state" / "keys"
KEY_FILE = KEYS_DIR / "seed_seal_key"
SCHEMA = "seed_seal.v1"
KEY_DOMAIN = b"mag-seed-seal-pubkey:"

_STDOUT_RECONFIG: str = ""
try:  # make the CLI safe on win32 consoles (proof.py precedent)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    _STDOUT_RECONFIG = "utf-8"
except Exception as e:  # console reconfig is best-effort; default stream still works
    _STDOUT_RECONFIG = f"skipped ({type(e).__name__})"


class SealError(Exception):
    """Any fail-closed seal or verify condition; message names the reason."""


def canonical_root(session: str, arc_root: str, seed_sha: str, chain_sha: str) -> str:
    """seed_root per spec clause 1: sha256 over the canonical json of the four
    identity+byte-binding fields. Canonical form is fixed here: sort_keys,
    tight separators, ensure_ascii, utf-8 - the one serialization that hashes
    (pretty forms are display only, so formatting drift cannot move the root).
    """
    payload = {
        "arc_root": arc_root,
        "chain_sha": chain_sha,
        "seed_sha": seed_sha,
        "session": session,
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    """sha256 hex over exact file bytes - the only truth the seal binds."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key_id_for(pubkey_raw: bytes) -> str:
    """Domain-separated stable key fingerprint (16 hex) - the rotation handle."""
    return hashlib.sha256(KEY_DOMAIN + pubkey_raw).hexdigest()[:16]


def load_signing_key(key_file: Path | None = None) -> dict[str, Any]:
    """Resolve the Ed25519 private key: explicit path arg, else
    state/keys/seed_seal_key. Absent file -> mint a random 32-byte seed and
    persist it as hex. NEVER log or return the seed bytes; callers get the
    key object, the key_id and the raw pubkey only."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    kf = Path(key_file) if key_file else KEY_FILE
    if kf.is_file():
        hexseed = kf.read_text(encoding="utf-8").strip()
        try:
            seed = bytes.fromhex(hexseed)
        except ValueError:
            return {"ok": False, "error": f"{kf}: key file is not valid hex"}
        if len(seed) != 32:
            return {"ok": False, "error": f"{kf}: ed25519 seed must be 32 bytes (64 hex chars)"}
        return {"ok": True, "key": Ed25519PrivateKey.from_private_bytes(seed), "source": str(kf)}
    kf.parent.mkdir(parents=True, exist_ok=True)
    seed = os.urandom(32)
    kf.write_text(seed.hex(), encoding="utf-8")
    mode_note = ""
    try:
        os.chmod(kf, 0o600)
        mode_note = " (chmod 0600)"
    except OSError as e:
        mode_note = f" (chmod unavailable: {type(e).__name__}; custody = gitignore + never-commit)"
    return {"ok": True, "key": Ed25519PrivateKey.from_private_bytes(seed),
            "source": f"generated:{kf}{mode_note}"}


def _pubkey_raw(private_key: Any) -> bytes:
    from cryptography.hazmat.primitives import serialization
    return private_key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def _chain_identity(chain_path: Path) -> tuple[str, str]:
    """(session, arc_root) from the chain json - the structured authority for
    the arc identity. Fail-closed: absent fields are a SealError, never ''."""
    try:
        chain = json.loads(chain_path.read_bytes().decode("utf-8"))
    except (OSError, ValueError) as e:
        raise SealError(f"chain unreadable or not json: {chain_path} ({type(e).__name__})") from e
    session = chain.get("session")
    arc_root = (chain.get("anatomy") or {}).get("arc_root")
    if not session or not arc_root:
        raise SealError(f"chain missing session/anatomy.arc_root: {chain_path}")
    return str(session), str(arc_root)


def _default_chain(seed_path: Path) -> Path:
    """arc_seed_<tail>.md pairs with arc_chain_<tail>.json in the same dir."""
    return seed_path.with_name(seed_path.name.replace("arc_seed_", "arc_chain_", 1)).with_suffix(".json")


def _default_seal(seed_path: Path) -> Path:
    return seed_path.with_suffix(".seal")


def sign_seed(seed_path: Path, chain_path: Path | None = None,
              key_file: Path | None = None) -> dict[str, Any]:
    """Sign one real seed+chain pair and write the .seal sidecar next to the
    seed (spec clause 1: 'The seal lands as a .seal sidecar next to the seed
    and chain in watch/arc_seeds/'). Returns the seal dict written."""
    seed_path, chain_path = Path(seed_path), Path(chain_path) if chain_path else _default_chain(Path(seed_path))
    if not seed_path.is_file():
        raise SealError(f"seed missing: {seed_path}")
    if not chain_path.is_file():
        raise SealError(f"chain missing: {chain_path}")
    loaded = load_signing_key(key_file)
    if not loaded.get("ok"):
        raise SealError(str(loaded.get("error") or "no signing key"))
    private_key = loaded["key"]
    session, arc_root = _chain_identity(chain_path)
    seed_sha = sha256_file(seed_path)
    chain_sha = sha256_file(chain_path)
    seed_root = canonical_root(session, arc_root, seed_sha, chain_sha)
    pubkey_raw = _pubkey_raw(private_key)
    signature = private_key.sign(seed_root.encode("utf-8"))
    seal = {
        "schema": SCHEMA,
        "session": session,
        "arc_root": arc_root,
        "seed_sha": seed_sha,
        "chain_sha": chain_sha,
        "seed_root": seed_root,
        "key_id": key_id_for(pubkey_raw),
        "public_key": base64.b64encode(pubkey_raw).decode("ascii"),
        "signature": base64.b64encode(signature).decode("ascii"),
        "sig_alg": "ed25519",
        "root_alg": "sha256(canonical_json{arc_root,chain_sha,seed_sha,session})",
        "sealed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "sealed_by": "mag/seed_seal.py seed_seal.v1 (SS-1)",
    }
    seal_path = _default_seal(seed_path)
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    return {"ok": True, "seal_path": str(seal_path), "seal": seal,
            "key_source": loaded["source"]}


def verify_seed(seed_path: Path, chain_path: Path | None = None,
                seal_path: Path | None = None) -> dict[str, Any]:
    """Verify-at-consume, FAIL-CLOSED (spec clause 2): recompute both file
    shas from the bytes on disk, take session/arc_root from the chain json
    (never from the seal's own word), rebuild seed_root, cross-check every
    seal field, then verify the Ed25519 signature with the inline pubkey.
    Returns {ok: True, ...} only when EVERY check passes; any single failure
    returns {ok: False, reason: ...}. There is no code path that returns True
    by silence - that exact shape is PAM's SEC-005 defect."""
    seed_path, chain_path = Path(seed_path), Path(chain_path) if chain_path else _default_chain(Path(seed_path))
    seal_path = Path(seal_path) if seal_path else _default_seal(seed_path)
    for label, p in (("seed", seed_path), ("chain", chain_path), ("seal", seal_path)):
        if not p.is_file():
            return {"ok": False, "reason": f"{label} missing: {p}"}
    try:
        seal = json.loads(seal_path.read_bytes().decode("utf-8"))
    except (OSError, ValueError) as e:
        return {"ok": False, "reason": f"seal unreadable or not json ({type(e).__name__})"}
    if seal.get("schema") != SCHEMA:
        return {"ok": False, "reason": f"seal schema is {seal.get('schema')!r}, want {SCHEMA!r}"}
    for field in ("session", "arc_root", "seed_sha", "chain_sha", "seed_root",
                  "key_id", "public_key", "signature"):
        if not seal.get(field):
            return {"ok": False, "reason": f"seal field missing or empty: {field}"}
    try:
        session, arc_root = _chain_identity(chain_path)
    except SealError as e:
        return {"ok": False, "reason": str(e)}
    if seal["session"] != session or seal["arc_root"] != arc_root:
        return {"ok": False, "reason": "arc identity mismatch: seal vs chain json"}
    seed_sha = sha256_file(seed_path)
    chain_sha = sha256_file(chain_path)
    if seal["seed_sha"] != seed_sha:
        return {"ok": False, "reason": "seed bytes tampered: seed_sha mismatch (recomputed vs seal)"}
    if seal["chain_sha"] != chain_sha:
        return {"ok": False, "reason": "chain bytes tampered: chain_sha mismatch (recomputed vs seal)"}
    rebuilt_root = canonical_root(session, arc_root, seed_sha, chain_sha)
    if seal["seed_root"] != rebuilt_root:
        return {"ok": False, "reason": "seed_root mismatch: rebuilt root differs from seal"}
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    from cryptography.exceptions import InvalidSignature
    try:
        pubkey_raw = base64.b64decode(seal["public_key"], validate=True)
        signature = base64.b64decode(seal["signature"], validate=True)
    except (ValueError, TypeError) as e:
        return {"ok": False, "reason": f"seal pubkey/signature not valid base64 ({type(e).__name__})"}
    if len(pubkey_raw) != 32:
        return {"ok": False, "reason": f"public key must be 32 raw bytes, got {len(pubkey_raw)}"}
    if seal["key_id"] != key_id_for(pubkey_raw):
        return {"ok": False, "reason": "key_id does not match the inline public key (key swap refused)"}
    try:
        Ed25519PublicKey.from_public_bytes(pubkey_raw).verify(signature, rebuilt_root.encode("utf-8"))
    except InvalidSignature:
        return {"ok": False, "reason": "FORGERY REFUSED: ed25519 signature does not verify over the rebuilt seed_root"}
    return {"ok": True, "reason": "verified",
            "session": session, "arc_root": arc_root, "key_id": seal["key_id"],
            "seed_root": rebuilt_root}


def main() -> int:
    usage = ("usage: python -m mag.seed_seal sign <seed.md> [chain.json]\n"
             "       python -m mag.seed_seal verify <seed.md> [chain.json] [seal]\n"
             "       python -m mag.seed_seal keyinfo")
    if len(sys.argv) < 2:
        print(usage)
        return 2
    cmd = sys.argv[1]
    if cmd == "keyinfo":
        loaded = load_signing_key()
        if not loaded.get("ok"):
            print(f"key error: {loaded.get('error')}")
            return 1
        pub = _pubkey_raw(loaded["key"])
        print(json.dumps({"key_file": str(KEY_FILE), "key_id": key_id_for(pub),
                          "public_key": base64.b64encode(pub).decode("ascii"),
                          "source": loaded["source"]}, indent=1))
        return 0
    if cmd in ("sign", "verify") and len(sys.argv) >= 3:
        seed_path = Path(sys.argv[2])
        if cmd == "sign":
            out = sign_seed(seed_path, Path(sys.argv[3]) if len(sys.argv) > 3 else None)
            print(json.dumps({"ok": True, "seal_path": out["seal_path"],
                              "key_id": out["seal"]["key_id"],
                              "seed_root": out["seal"]["seed_root"],
                              "key_source": out["key_source"]}, indent=1))
            return 0
        out = verify_seed(seed_path,
                          Path(sys.argv[3]) if len(sys.argv) > 3 else None,
                          Path(sys.argv[4]) if len(sys.argv) > 4 else None)
        print(json.dumps(out, indent=1))
        return 0 if out.get("ok") else 1
    print(usage)
    return 2


if __name__ == "__main__":
    sys.exit(main())
