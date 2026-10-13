"""identity_binding: first contact bound to the GitHub-published SSH key (C1 step 4, 2026-09-30).

THE LENS: LW2 (watch/inbox/last_mile_20260930/LW2_ADAM_INVITE.md) refused to
invite Adam — no GitHub username exists in the estate, and both guesses 404'd.
A push-permission invite to a guessed handle would grant a possible stranger
write access: the exact identity-skipped-for-resemblance failure the stranger
register exists to stop. This module is the other half of that stop: the
moment his REAL username arrives, the server can bind first contact to the
SSH key GitHub itself serves at https://github.com/<user>.keys — key material
Adam controls, published on a surface the estate never hosts. He proves
ownership the standard way, an sshsig signature (ssh-keygen -Y sign), and the
server verifies it the standard way (ssh-keygen -Y verify). No password
crosses the wire, nothing is stored that Adam did not already publish.

THE FLOW (what Adam follows, byte-exact — the receipt expands this):
    1. server  fetches github.com/<user>.keys      (urllib, timeout, no auth)
    2. server  mints a challenge string: nonce + issued + expires + user
    3. Adam    saves it EXACTLY to challenge.txt and runs
               ssh-keygen -Y sign -n core -f ~/.ssh/id_ed25519 < challenge.txt \
                   > challenge.txt.sig
    4. server  ssh-keygen -Y verify -f <allowed_signers> -I <user> -n core \
                   -s challenge.txt.sig  with the challenge on stdin
    Exit 0 + Good "core" signature => the peer holds the PRIVATE half of a
    key GitHub serves for that login. Identity bound.

THE VERIFY DIALECT (pinned on this box, OpenSSH 10.3p1, 2026-09-30): modern
ssh-keygen (8.2+) takes the allowed_signers file via -f AFTER -Y verify:
    ssh-keygen -Y verify -f allowed_signers_file -I signer_identity \
                  -n namespace -s signature_file
and reads the signed MESSAGE from stdin; success prints
    Good "core" signature for <id> with ED25519 key SHA256:...
to stderr with exit 0. (The old positional-tail form is refused by 10.x as
"Too few arguments for sign: missing allowed keys file".) The allowed_signers
file is one line per key: "<principal> <keytype> <base64 blob>".

THE TABLE (the srp table pattern, B4 law): identity_challenge /
identity_proof are FROZEN table rows — IDENTITY_AUTH_TABLE compiles the
DEFAULT rows plus the two identity verbs as a NEW contract version
(IDENTITY_AUTH_DIGEST); DEFAULT (the bound v0 wire) stays byte-identical and
PROTOCOL_DIGEST does not move. required_state is CONNECTED (pre-auth by
definition, the B4 precedent); the real laws ride the closed reject
VOCABULARY, never per-verb rows:
    STALE_CHALLENGE  proof with no pending single-use challenge, a user
                     mismatch, or an expired one (the replay/nonce law)
    BAD_PROOF        signature does not verify (wrong key, tampered bytes,
                     wrong namespace, garbage armor)
    NO_KEYS          the fetch failed or the login publishes no usable keys
                     (a 404 IS the operator's signal the username is wrong —
                     enumeration is not a secret here: the username is the
                     claimed identity, not a password)

THE NONCE LAW (srp law, verbatim): a pending challenge is SINGLE-USE and
BURNS AT RECEIPT of a proof — success, failure, or garbage alike. A replayed
proof finds no pending and rejects STALE_CHALLENGE. A fresh challenge always
replaces (burns) the old one for that connection; a dead connection's
pending dies with it (drop). Expiry is enforced server-side from the mint
timestamp — the signed string says when it dies, the server believes its own
clock, and an expired challenge burns like any other.

NAMED DEVIATIONS FROM THE v0 ESTATE LAWS (auth_srp6 precedent of naming):
    secrets for nonces      real entropy; a clock+counter nonce would be
                            guessable and the challenge is a signed-ownership
                            proof, the one place guessability is fatal.
    network + subprocess    urllib fetch and ssh-keygen subprocess are the
                            point of the module; auth material never enters
                            the world log, so the determinism law is
                            untouched. Tests inject fake fetchers and
                            locally-generated fixture keys — never real keys,
                            never the network.

Run (operability probe — live fetch + fingerprints, no challenge minted):
    .venv/Scripts/python.exe -m server.identity_binding <github-username>
Tests: tests/test_identity_binding.py

Schema: identity_binding.v1 . stdlib only . no world-log writes . no real keys
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import re
import secrets
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from server.protocol_table import (  # noqa: E402
    DEFAULT_SPEC,
    ProtocolDispatch,
    compile_table,
)

NAMESPACE = "core"
DEFAULT_TTL_SECONDS = 300
FETCH_TIMEOUT_SECONDS = 10.0
VERIFY_TIMEOUT_SECONDS = 10.0
KEYS_URL = "https://github.com/{user}.keys"
MAX_KEYS_BYTES = 65536

# The openssh single-line public key grammar we accept. GitHub serves exactly
# these; anything else on the page means we are not looking at a key list.
KNOWN_KEY_TYPES = frozenset({
    "ssh-ed25519", "ssh-rsa",
    "ecdsa-sha2-nistp256", "ecdsa-sha2-nistp384", "ecdsa-sha2-nistp521",
    "sk-ssh-ed25519@openssh.com", "sk-ecdsa-sha2-nistp256@openssh.com",
})

# GitHub login grammar (the safe core): alphanumeric + inner hyphens, 1..39.
# This is ALSO the injection law: the name is interpolated into a URL, an
# allowed_signers principal line, and an -I argument — the grammar forecloses
# path traversal, query strings, spaces, and newlines in all three.
_USERNAME_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")

SSHSIG_BEGIN = "-----BEGIN SSH SIGNATURE-----"
SSHSIG_END = "-----END SSH SIGNATURE-----"

# The fingerprint line ssh-keygen -Y verify prints on success (stderr):
#   Good "core" signature for <id> with ED25519 key SHA256:xxxx
_GOOD_FP_RE = re.compile(r"SHA256:([A-Za-z0-9+/=]+)")


class IdentityError(ValueError):
    """Typed, fail-closed refusal (malformed username, unparsable key list)."""


class IdentityFetchError(RuntimeError):
    """The .keys fetch failed (network, status, timeout). Maps to NO_KEYS."""


# ---------------------------------------------------------------------------------------------
# Username + public key parsing
# ---------------------------------------------------------------------------------------------


def validate_username(name: Any) -> str:
    """GitHub login grammar or typed refusal. THE INJECTION LAW: this name is
    interpolated into a URL, an allowed_signers principal, and an ssh-keygen
    -I argument; the grammar (alphanumeric + inner hyphens, <=39) admits none
    of the metacharacters any of those surfaces would honor."""
    if not isinstance(name, str) or not _USERNAME_RE.fullmatch(name):
        raise IdentityError(
            "username must be a GitHub login (alphanumeric + inner hyphens, "
            "1-39 chars)")
    return name


@dataclass(frozen=True)
class PublicKeyLine:
    """One parsed openssh public key line: '<keytype> <base64> [comment]'."""
    keytype: str
    blob_b64: str
    comment: str

    @property
    def blob(self) -> bytes:
        return base64.b64decode(self.blob_b64, validate=True)

    @property
    def fingerprint(self) -> str:
        """The standard SHA256 fingerprint (ssh-keygen -lf shape)."""
        digest = hashlib.sha256(self.blob).digest()
        return "SHA256:" + base64.b64encode(digest).decode("ascii").rstrip("=")

    def to_signers_line(self, principal: str) -> str:
        return f"{principal} {self.keytype} {self.blob_b64}"


def parse_public_keys(body: str) -> tuple[PublicKeyLine, ...]:
    """STRICT parse of a .keys body: every non-blank line must be a known
    keytype + valid base64 blob whose embedded wire-type matches. No silent
    skipping — a key list with junk in it is not a key list (fail closed)."""
    keys: list[PublicKeyLine] = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2 or parts[0] not in KNOWN_KEY_TYPES:
            raise IdentityError(f"not an openssh public key line: {line[:60]!r}")
        keytype, blob_b64 = parts[0], parts[1]
        comment = " ".join(parts[2:])
        try:
            blob = base64.b64decode(blob_b64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise IdentityError(f"key blob is not valid base64: {exc}") from exc
        # the blob's first field is the wire type string; it must agree
        wire_type, offset = _read_wire_string(blob)
        if wire_type.decode("ascii", errors="replace") != keytype:
            raise IdentityError(
                f"key blob type {wire_type!r} disagrees with line type {keytype!r}")
        if offset >= len(blob):
            raise IdentityError("key blob truncated before the key material")
        keys.append(PublicKeyLine(keytype=keytype, blob_b64=blob_b64,
                                  comment=comment))
    return tuple(keys)


def _read_wire_string(blob: bytes) -> tuple[bytes, int]:
    """Read one length-prefixed ssh wire string; returns (bytes, next offset)."""
    if len(blob) < 4:
        raise IdentityError("key blob too short for a wire string")
    length = int.from_bytes(blob[:4], "big")
    end = 4 + length
    if length > len(blob) - 4:
        raise IdentityError("key blob wire string overruns the blob")
    return blob[4:end], end


def fetch_github_keys(username: str, *,
                      timeout: float = FETCH_TIMEOUT_SECONDS,
                      ) -> tuple[PublicKeyLine, ...]:
    """GET https://github.com/<user>.keys with stdlib urllib — timeout set,
    no auth, no redirects honored beyond urllib's default. A 404 is the
    operator's signal the username is wrong (LW2's exact failure mode);
    every failure is a typed IdentityFetchError the caller maps to NO_KEYS."""
    validate_username(username)
    url = KEYS_URL.format(user=username)
    request = urllib.request.Request(
        url, headers={"User-Agent": "mag-identity-binding/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            if response.status != 200:
                raise IdentityFetchError(
                    f"{url} answered HTTP {response.status}")
            raw = response.read(MAX_KEYS_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise IdentityFetchError(
            f"{url} answered HTTP {exc.code}"
            + (" (no such user or no keys published)" if exc.code == 404 else "")
        ) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise IdentityFetchError(f"fetching {url} failed: {exc}") from exc
    if len(raw) > MAX_KEYS_BYTES:
        raise IdentityFetchError(f"{url} body exceeds {MAX_KEYS_BYTES} bytes")
    keys = parse_public_keys(raw.decode("utf-8", errors="strict"))
    if not keys:
        raise IdentityFetchError(f"{url} publishes no usable keys")
    return keys


# ---------------------------------------------------------------------------------------------
# The binding service (server side of the challenge)
# ---------------------------------------------------------------------------------------------


def _format_ts(unix: float) -> str:
    """UTC ISO-8601 to the second, Z suffix — what Adam reads in the string."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(unix))


CHALLENGE_TEMPLATE = (
    "the-mountain identity binding v1\n"
    "user: {user}\n"
    "nonce: {nonce}\n"
    "issued: {issued}\n"
    "expires: {expires}"
)
# NOTE: no trailing newline. The law is EXACT BYTES: Adam signs the file as
# the server delivered it and the server verifies those same bytes on stdin;
# an editor that adds or strips a trailing newline moves the signed content
# and the proof rejects BAD_PROOF. That is the signature working, not a bug.


@dataclass
class PendingIdentityChallenge:
    """One single-use challenge. Burns at first proof receipt (the nonce law)."""
    username: str
    challenge: str
    nonce: str
    issued: float
    expires: float
    keys: tuple[PublicKeyLine, ...]


class IdentityBindService:
    """Owns the identity-binding state: per-connection pending challenges.
    The enforcement point (a later server.py lane, the B4 srp_* precedent)
    calls mint_challenge / verify_proof keyed by the connection id, so a
    pending challenge dies with its connection (drop)."""

    def __init__(self, *,
                 fetcher: Callable[[str], tuple[PublicKeyLine, ...]] = fetch_github_keys,
                 ttl_seconds: float = DEFAULT_TTL_SECONDS,
                 now: Callable[[], float] = time.time,
                 nonce_fn: Callable[[], str] = lambda: secrets.token_hex(16),
                 ssh_keygen: str | None = None,
                 namespace: str = NAMESPACE,
                 verify_timeout: float = VERIFY_TIMEOUT_SECONDS) -> None:
        self._fetcher = fetcher
        self._ttl = float(ttl_seconds)
        self._now = now
        self._nonce_fn = nonce_fn
        self._ssh_keygen = ssh_keygen or shutil.which("ssh-keygen") or "ssh-keygen"
        self._namespace = namespace
        self._verify_timeout = verify_timeout
        self._pending: dict[Any, PendingIdentityChallenge] = {}

    # -------------------------------------------------------- challenge ----
    def mint_challenge(self, key: Any, username: str) -> dict[str, Any]:
        """Fetch the login's published keys and mint a fresh single-use
        challenge for this connection key. Replaces (burns) any pending for
        the key — only the newest challenge is provable against.

        Returns {"ok": True, "user", "challenge", "nonce", "expires"} or
        {"ok": False, "why": "BAD_AUTH" | "NO_KEYS"} (typed, fail closed)."""
        try:
            username = validate_username(username)
        except IdentityError as exc:
            return {"ok": False, "why": "BAD_AUTH", "detail": str(exc)}
        try:
            keys = self._fetcher(username)
        except IdentityFetchError as exc:
            return {"ok": False, "why": "NO_KEYS", "detail": str(exc)}
        if not keys:
            return {"ok": False, "why": "NO_KEYS",
                    "detail": "fetcher returned no keys"}
        now = self._now()
        nonce = self._nonce_fn()
        expires = now + self._ttl
        challenge = CHALLENGE_TEMPLATE.format(
            user=username, nonce=nonce,
            issued=_format_ts(now), expires=_format_ts(expires))
        self._pending[key] = PendingIdentityChallenge(
            username=username, challenge=challenge, nonce=nonce,
            issued=now, expires=expires, keys=keys)
        return {"ok": True, "user": username, "challenge": challenge,
                "nonce": nonce, "expires": _format_ts(expires)}

    # ----------------------------------------------------------- proof ----
    def verify_proof(self, key: Any, username: str, signature: Any) -> dict[str, Any]:
        """Consume the pending challenge and verify the sshsig armor over the
        exact challenge bytes. BURNS AT RECEIPT: the pending entry is spent
        whether the proof passes, fails, or is garbage (the srp nonce law).

        Returns {"ok": True, "user", "fingerprint"} on success, else
        {"ok": False, "why": "STALE_CHALLENGE" | "BAD_PROOF"}."""
        pending = self._pending.pop(key, None)
        if pending is None or pending.username != username:
            return {"ok": False, "why": "STALE_CHALLENGE"}
        if self._now() > pending.expires:
            return {"ok": False, "why": "STALE_CHALLENGE"}
        if (not isinstance(signature, str)
                or SSHSIG_BEGIN not in signature or SSHSIG_END not in signature):
            return {"ok": False, "why": "BAD_PROOF"}
        # armor-only byte hygiene: a Windows clipboard may hand the armor to
        # the wire with CRLF; ssh-keygen's parser wants \n. The SIGNED MESSAGE
        # is never touched — it rides stdin as the exact utf-8 bytes minted.
        signature = signature.replace("\r\n", "\n")
        return self._sshsig_verify(pending, signature)

    def _sshsig_verify(self, pending: PendingIdentityChallenge,
                       signature: str) -> dict[str, Any]:
        """The standard path: write the armor + an allowed_signers file, run
        ssh-keygen -Y verify -f <signers> -I <user> -n <ns> -s <sig> with the
        challenge bytes on stdin (the dialect pinned in the module docstring).
        Every subprocess failure — wrong key, tampered bytes, wrong
        namespace, timeout, missing binary — is BAD_PROOF, fail closed."""
        with tempfile.TemporaryDirectory(prefix="mag_identity_") as tmp:
            tmp_dir = Path(tmp)
            sig_path = tmp_dir / "challenge.txt.sig"
            signers_path = tmp_dir / "allowed_signers"
            sig_path.write_text(signature, encoding="ascii", newline="\n")
            signers_path.write_text(
                "\n".join(k.to_signers_line(pending.username)
                          for k in pending.keys) + "\n",
                encoding="ascii", newline="\n")
            try:
                proc = subprocess.run(
                    [self._ssh_keygen, "-Y", "verify",
                     "-f", str(signers_path),
                     "-I", pending.username,
                     "-n", self._namespace,
                     "-s", str(sig_path)],
                    input=pending.challenge.encode("utf-8"),
                    capture_output=True, timeout=self._verify_timeout)
            except (OSError, subprocess.TimeoutExpired):
                return {"ok": False, "why": "BAD_PROOF"}
            if proc.returncode == 0:
                # the exit code is the verdict; the "Good ... SHA256:..."
                # line rides STDERR on Unix but STDOUT on Windows OpenSSH
                # (probed 2026-09-30, both dialects on this box) — search both
                text = (proc.stdout + proc.stderr).decode(
                    "utf-8", errors="replace")
                match = _GOOD_FP_RE.search(text)
                fingerprint = match.group(0) if match else None
                return {"ok": True, "user": pending.username,
                        "fingerprint": fingerprint}
            return {"ok": False, "why": "BAD_PROOF"}

    # ---------------------------------------------------------- hygiene ----
    def drop(self, key: Any) -> None:
        """Connection gone: its pending challenge (if any) dies with it."""
        self._pending.pop(key, None)

    def pending_count(self) -> int:
        return len(self._pending)


# ---------------------------------------------------------------------------------------------
# The frozen table rows (the srp table pattern: B4 law, one home per dialect)
# ---------------------------------------------------------------------------------------------

# C1 step 4 law: verbs are frozen data rows, never hardcoded strings. The
# table compiles the DEFAULT rows plus the two identity verbs as a NEW
# contract version — DEFAULT stays byte-identical and PROTOCOL_DIGEST does
# not move (pinned by tests). required_state is CONNECTED (pre-auth by
# definition, the B4 precedent: the row's reject_code slot is a reserved
# never-fires slot). The dialect's real laws — BAD_PROOF / STALE_CHALLENGE /
# NO_KEYS — ride the closed reject VOCABULARY and fire in the service layer,
# the LW6/LW7 shape: a replayed proof is stale whichever arm carried it, and
# no row may own that. handler_name names the future server.py owners
# (_on_identity_* handlers, the auth_srp_* precedent); this module owns the
# table + the service, the op-ladder wiring is the next lane's fence.
IDENTITY_AUTH_VERBS: tuple[str, ...] = ("identity_challenge", "identity_proof")

IDENTITY_AUTH_SPEC: dict[str, Any] = {
    "schema": "protocol_table.v1",
    "session_states": list(DEFAULT_SPEC["session_states"]),
    "reject_codes": list(DEFAULT_SPEC["reject_codes"])
    + ["BAD_PROOF", "STALE_CHALLENGE", "NO_KEYS"],
    "transport_reject_codes": list(DEFAULT_SPEC["transport_reject_codes"]),
    "rows": [dict(r) for r in DEFAULT_SPEC["rows"]] + [
        {"verb": "identity_challenge", "required_state": "CONNECTED",
         "handler_name": "auth_identity_challenge", "reject_code": "UNKNOWN_SID"},
        {"verb": "identity_proof", "required_state": "CONNECTED",
         "handler_name": "auth_identity_proof", "reject_code": "UNKNOWN_SID"},
    ],
}

IDENTITY_AUTH_TABLE = compile_table(IDENTITY_AUTH_SPEC)
IDENTITY_AUTH_DIGEST: str = IDENTITY_AUTH_TABLE.digest
IDENTITY_AUTH_DISPATCH = ProtocolDispatch(IDENTITY_AUTH_TABLE)


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - operability
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1:
        print("usage: python -m server.identity_binding <github-username>")
        print("  live-fetches github.com/<user>.keys and prints fingerprints")
        return 2
    username = argv[0]
    try:
        keys = fetch_github_keys(username)
    except (IdentityError, IdentityFetchError) as exc:
        print(f"NO_KEYS: {exc}")
        return 1
    print(f"{username}: {len(keys)} key(s) published")
    for k in keys:
        print(f"  {k.fingerprint}  {k.keytype}  {k.comment}".rstrip())
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
