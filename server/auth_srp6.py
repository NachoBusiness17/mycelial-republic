"""auth_srp6: SRP6 as OUR account system — RFC 5054 2048-bit/SHA-256 DEFAULT,
mangos 256-bit/SHA-1 behind a compat flag (R5, 2026-09-30).

THE UPGRADE (Q04 / V2ASK1): the B4 port imported the mangos WoW variant
verbatim (fixed 256-bit N, g=7, k=3, SHA-1) — proven on the wire against the
estate's CMaNGOS realmd (LW4, receipt
watch/inbox/last_mile_20260930/LW4_REALMD_CLIENT.md) but cryptographically
dead on arrival for production: a 256-bit safe prime is inside reach of
off-the-shelf index-calculus tooling, so one logged login yields the session
key and one leaked verifier is a password-equivalent forgery kit. The
frontier's decision tree (Q04 verdict, receipt
watch/inbox/frontier_asks/volley2/results/V2ASK1.md) reads:

    untrusted federated servers hold credentials? -> OPAQUE (GDExtension)
    one-stranger-first + "operator never sees the password" promised?
        -> Option A: SRP-2048/SHA-256 (benchmark F4.2 first)
    otherwise -> Option B: TLS + memory-hard hash

THE OPERATOR'S CALL (this module): the "server never sees the password"
promise is the product's (the SRP6 account system IS B4's headline), so
Option A is built: **RFC 5054 2048-bit group + SHA-256 is the DEFAULT** for
every new registration; the mangos 256-bit variant stays available behind
the compat flag (allow_mangos, default True) because the CMaNGOS TRAINING
path (tools/realmd_client.py differential) still needs it. The verdict's
own disconfirming note stands: the full verdict recommended Option B for a
stranger reusing passwords (scrypt at rest beats a fast SHA verifier); if
that trade is ever accepted, auth_v2 replaces this module, not amends it.

THE CLIENT-SIDE BIGINT QUESTION (GDScript has no bigint — verdict, Option A
cost): the 2048-bit client needs a hand-rolled bignum — 30-bit limbs so
products fit int64, Montgomery reduction; ~69 limbs, ~10k limb ops per
modmul, ~3 exponentiations with a >=256-bit ephemeral (RFC 5054 §2.5.3) =
~15M limb ops, **~2-8 s at login on GDScript [verdict inference]** — the
F4.2 benchmark on the slowest target device is owed BEFORE any client ship.
The server wire keeps integers as plain lowercase hex so the client limbs
stay byte-simple (no ASN.1, no signed-magnitude containers).

WHAT EACH VARIANT IS (one dialect object per math, no second copies):
    rfc5054-2048 (DEFAULT)  RFC 5054 Appendix A.2 #3 group (g=2, safe
                            prime, byte-checked against the RFC text),
                            SHA-256, big-endian PAD() to |N| bytes,
                            k = H(N | PAD(g))                    (RFC 5054 §2.5.3)
                            x = H(s | H(I | ":" | P))            (RFC 5054 §2.6)
                            u = H(PAD(A) | PAD(B))               (RFC 5054 §2.6)
                            B = (k*v + g^b) mod N                (RFC 5054 §2.5.3)
                            S = (A * v^u)^b mod N                (RFC 5054 §2.6)
                            K = H(PAD(S))
                            M1 = H(H(N)^H(g) | H(I) | s | A | B | K)  (RFC 2945
                                  [SRP-RFC] evidence shape, which RFC 5054
                                  §2.6 points at; no vector published —
                                  certified by cross-derivation in tests)
                            M2 = H(A | M1 | K)
                            identity hashed VERBATIM (the appendix vectors
                            are lowercase "alice"); salt 16 bytes (appendix
                            B size), wire/storage hex big-endian.
    mangos-256 (compat)     the proven bytes, unchanged, imported from
                            tools.realmd_client (the anti-drift law): fixed
                            256-bit N/g=7, k=3, SHA-1, little-endian
                            minimal operands, sha-interleave K, upper-case
                            identity law, 32-byte LE salt, mangos M1/M2.
                            Registrations into this group and logins of
                            grandfathered rows require allow_mangos=True.

The RFC dialect is parameterized (n, g, digest) so tests replay RFC 5054
Appendix B (1024-bit group + SHA-1) against the published vectors — that
replay is what certifies the padding conventions; only "rfc5054-2048" and
"mangos-256" are registered for accounts.

MIGRATION (grandfathering, not forced re-registration): every account row
now carries "group". Rows written by B4 (salt+verifier only, no "group")
are GRANDFATHERED as mangos-256 and keep authenticating byte-identically
while allow_mangos stays True — existing verifiers are group-bound (a
2048-bit verifier cannot be recomputed from a 256-bit one), so forced
migration would mean forced re-registration; instead, the NEXT successful
re-registration (same op, same password) silently upgrades the row to
rfc5054-2048. Setting allow_mangos=False retires the variant: mangos
challenges raise ValueError (the server answers BAD_AUTH, the existing
typed path) and only rfc5054-2048 remains.

THE HANDSHAKE (wire unchanged from B4 — integers as lowercase hex):
    C->S {"op":"srp_register","user","pass"}   -> {"op":"srp_registered"}
    C->S {"op":"srp_challenge","user","a"}     -> {"op":"srp_challenge","salt","b"}
    C->S {"op":"srp_proof","user","m1"}        -> {"op":"welcome","sid","m2",...}
    begin_challenge's dict also carries "group" (dialect name) for the
    follow-up that puts it on the wire (server.py drops it today — clients
    discover the group from their own account state meanwhile).

THE NONCE LAW, DECOY LAW, NO-ENUMERATION (unchanged from B4): challenges
mint fresh b and a single-use pending entry keyed to the connection, burned
at proof receipt (success, failure, garbage alike); unknown users get a
well-formed decoy challenge in the service's default dialect whose proof
can only reject BAD_PROOF — identical to the wrong-password reject.

NAMED DEVIATIONS (unchanged): salts and b secrets use `secrets` (real
entropy — SRP6 is broken without unpredictable b); auth material never
enters the world log. u == 0 rejects BAD_PROOF on the RFC dialects only
(RFC 5054 rejects degenerate u; the mangos path keeps its historical
behavior so the realmd differential stays byte-exact — 2^-160 event).

Run:
    .venv/Scripts/python.exe -m server.auth_srp6 <users.json> add <username> [group]
Tests: tests/test_auth_srp6.py (RFC 5054 appendix B vectors, roundtrip both
groups, wrong-password both, grandfathering, compat-flag retirement, replay/
nonce, decoy, differential against the proven realmd client, table laws)

Schema: auth_srp6.v2 . stdlib + tools.realmd_client only . no world-log writes
"""
from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .store_io import atomic_write_text, exclusive

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Single source of truth for the MANGOS math: the module proven against the
# live realmd on 2026-09-30 (the anti-drift law: import, never re-type).
from tools.realmd_client import (  # noqa: E402
    G as MANGOS_G,
    N as MANGOS_N,
    _interleave,
    _ng_xor,
    le_min,
    sha1,
    srp6_verifier,
    srp6_x,
)

# RFC 5054 Appendix A.2 #3, 2048-bit group, byte-checked against the RFC
# text (512 hex chars; N and q=(N-1)/2 both probable-prime, verified in
# tests). g = 2.
RFC5054_2048_N_HEX = (
    "AC6BDB41324A9A9BF166DE5E1389582FAF72B6651987EE07FC3192943DB56050"
    "A37329CBB4A099ED8193E0757767A13DD52312AB4B03310DCD7F48A9DA04FD50"
    "E8083969EDB767B0CF6095179A163AB3661A05FBD5FAAAE82918A9962F0B93B8"
    "55F97993EC975EEAA80D740ADBF4FF747359D041D5C33EA71D281E446B14773B"
    "CA97B43A23FB801676BD207A436C6481F1D2B9078717461A5B9D32E688F87748"
    "544523B524B0D57D5EA77A2775D2ECFA032CFBDBF52FB3786160279004E57AE6"
    "AF874E7303CE53299CCC041C7BC308D82A5698F3A8D0C38271AE35F8E9DBFBB6"
    "94B5C803D89F7AE435DE236D525F54759B65E372FCD68EF20FA7111F9E4AFF73"
)

DEFAULT_GROUP = "rfc5054-2048"
MANGOS_GROUP = "mangos-256"
SECRET_BITS = 256  # RFC 5054 §2.5.3: b at least 256 bits; mangos used 256


def _hex(value: int) -> str:
    return f"{value:x}"


def _int_or_none(text: Any) -> int | None:
    """Wire hex -> int, typed refusal (None) on anything malformed."""
    if not isinstance(text, str) or not text:
        return None
    try:
        return int(text, 16)
    except ValueError:
        return None


# ---------------------------------------------------------------------------------------------
# Dialects: one object per SRP6 math. MangosDialect wraps the proven bytes;
# Rfc5054Dialect is the RFC math, parameterized so tests replay appendix B.
# ---------------------------------------------------------------------------------------------


class SrpDialect:
    """The math surface both variants implement. A dialect owns: group
    constants, hash, identity normalization, salt shape (bytes length +
    wire/storage encoding), and every SRP6 formula. No second copies of the
    mangos bytes exist anywhere else in the server."""

    name: str
    n: int
    g: int
    salt_len: int

    # ------------------------------------------------------ identity ----
    def ident_of(self, user: str) -> bytes:
        """Identity bytes as this dialect hashes them into x and M1
        (mangos upper-cases; RFC is verbatim). ascii-strict."""
        raise NotImplementedError

    def normalize(self, user: str, password: str) -> tuple[bytes, bytes]:
        """(identity bytes, password bytes) as this dialect hashes them.
        Both dialects are ascii-strict (typed refusal upstream)."""
        raise NotImplementedError

    def display_user(self, user: str) -> str:
        """The wire-canonical account name (mangos upper-cases; RFC is
        verbatim — appendix B hashes lowercase "alice")."""
        raise NotImplementedError

    # --------------------------------------------------------- salts ----
    def salt_wire(self, salt: bytes) -> str:
        raise NotImplementedError

    def salt_decode(self, text: Any) -> bytes | None:
        raise NotImplementedError

    # ---------------------------------------------------------- math ----
    def x_of(self, ident: bytes, password: bytes, salt: bytes) -> int:
        raise NotImplementedError

    def verifier(self, ident: bytes, password: bytes, salt: bytes) -> int:
        return pow(self.g, self.x_of(ident, password, salt), self.n)

    def multiplier(self) -> int:
        raise NotImplementedError

    def public_b(self, v: int, b_secret: int) -> int:
        raise NotImplementedError

    def u_of(self, a_int: int, b_int: int) -> int:
        raise NotImplementedError

    def server_s(self, a_int: int, v: int, u: int, b_secret: int) -> int:
        raise NotImplementedError

    def session_key(self, s_int: int) -> bytes:
        raise NotImplementedError

    def m1_of(self, ident: bytes, salt: bytes, a_int: int, b_int: int,
              key: bytes) -> bytes:
        raise NotImplementedError

    def m2_of(self, a_int: int, m1: bytes, key: bytes) -> bytes:
        raise NotImplementedError

    @property
    def m1_len(self) -> int:
        raise NotImplementedError


class MangosDialect(SrpDialect):
    """The proven realmd bytes (SRP6.cpp): fixed 256-bit N, g=7, k=3, SHA-1,
    little-endian minimal operands, sha-interleave K, upper-case identity.
    Every formula below is the B4 code moved onto the dialect surface —
    tests/test_auth_srp6.py differentials it against tools.realmd_client.
    Compat-only: registrations and grandfathered logins require
    allow_mangos=True on the service."""

    name = MANGOS_GROUP
    n = MANGOS_N
    g = MANGOS_G
    salt_len = 32

    def normalize(self, user: str, password: str) -> tuple[bytes, bytes]:
        return (user.upper().encode("ascii", errors="strict"),
                password.upper().encode("ascii", errors="strict"))

    def ident_of(self, user: str) -> bytes:
        return user.upper().encode("ascii", errors="strict")

    def display_user(self, user: str) -> str:
        return user.upper()

    def salt_wire(self, salt: bytes) -> str:
        # the mangos account-table shape: hex of the 32 LE bytes as an int
        return _hex(int.from_bytes(salt, "little"))

    def salt_decode(self, text: Any) -> bytes | None:
        if not isinstance(text, str) or not text:
            return None
        try:
            return int(text, 16).to_bytes(self.salt_len, "little")
        except (ValueError, OverflowError):
            return None

    def x_of(self, ident: bytes, password: bytes, salt: bytes) -> int:
        return srp6_x(ident, password, salt)          # SRP6.cpp:107-114

    def multiplier(self) -> int:
        return 3                                        # SRP6.cpp:39

    def public_b(self, v: int, b_secret: int) -> int:
        return (3 * v + pow(self.g, b_secret, self.n)) % self.n   # SRP6.cpp:37

    def u_of(self, a_int: int, b_int: int) -> int:
        return int.from_bytes(sha1(le_min(a_int) + le_min(b_int)), "little")

    def server_s(self, a_int: int, v: int, u: int, b_secret: int) -> int:
        return pow(a_int * pow(v, u, self.n), b_secret, self.n) % self.n

    def session_key(self, s_int: int) -> bytes:
        return _interleave(s_int)                      # SRP6.cpp:117-143

    def m1_of(self, ident: bytes, salt: bytes, a_int: int, b_int: int,
              key: bytes) -> bytes:
        return sha1(
            le_min(int.from_bytes(_ng_xor(), "little")) + sha1(ident)
            + le_min(int.from_bytes(salt, "little"))
            + le_min(a_int) + le_min(b_int) + le_min(int.from_bytes(key, "little")))

    def m2_of(self, a_int: int, m1: bytes, key: bytes) -> bytes:
        return sha1(le_min(a_int) + le_min(int.from_bytes(m1, "little"))
                    + le_min(int.from_bytes(key, "little")))

    @property
    def m1_len(self) -> int:
        return 20


class Rfc5054Dialect(SrpDialect):
    """RFC 5054 big-endian SRP-6: PAD() left-pads to |N| bytes (RFC 5054
    §2.1), k = H(N | PAD(g)) (§2.5.3), x = H(s | H(I | ':' | P)) (§2.6),
    u = H(PAD(A) | PAD(B)), K = H(PAD(S)), and the RFC 2945 evidence shape
    M1 = H(H(N)^H(g) | H(I) | s | A | B | K), M2 = H(A | M1 | K). Identity
    is hashed VERBATIM (the appendix vectors are lowercase). Parameterized
    (n, g, digest) so tests replay Appendix B with 1024-bit + SHA-1; the
    registered account variant is 2048-bit + SHA-256."""

    def __init__(self, name: str, n: int, g: int,
                 digest: Callable[[], "hashlib._Hash"]) -> None:
        self.name = name
        self.n = n
        self.g = g
        self.salt_len = 16  # RFC 5054 Appendix B salt size
        self._digest = digest
        self.n_len = (n.bit_length() + 7) // 8
        self._k = int.from_bytes(
            self._h(self._pad(n) + self._pad(g)), "big")

    # ------------------------------------------------------- helpers ----
    def _h(self, data: bytes) -> bytes:
        return self._digest(data).digest()

    def _pad(self, value: int) -> bytes:
        return value.to_bytes(self.n_len, "big")

    # ------------------------------------------------------ identity ----
    def normalize(self, user: str, password: str) -> tuple[bytes, bytes]:
        return (user.encode("ascii", errors="strict"),
                password.encode("ascii", errors="strict"))

    def ident_of(self, user: str) -> bytes:
        return user.encode("ascii", errors="strict")

    def display_user(self, user: str) -> str:
        return user

    # --------------------------------------------------------- salts ----
    def salt_wire(self, salt: bytes) -> str:
        return salt.hex()  # big-endian bytes verbatim (lossless)

    def salt_decode(self, text: Any) -> bytes | None:
        if not isinstance(text, str) or not text:
            return None
        try:
            salt = bytes.fromhex(text)
        except ValueError:
            return None
        return salt if len(salt) == self.salt_len else None

    # ---------------------------------------------------------- math ----
    def x_of(self, ident: bytes, password: bytes, salt: bytes) -> int:
        return int.from_bytes(self._h(salt + self._h(ident + b":" + password)), "big")

    def multiplier(self) -> int:
        return self._k

    def public_b(self, v: int, b_secret: int) -> int:
        return (self._k * v + pow(self.g, b_secret, self.n)) % self.n

    def u_of(self, a_int: int, b_int: int) -> int:
        return int.from_bytes(self._h(self._pad(a_int) + self._pad(b_int)), "big")

    def server_s(self, a_int: int, v: int, u: int, b_secret: int) -> int:
        return pow(a_int * pow(v, u, self.n), b_secret, self.n) % self.n

    def session_key(self, s_int: int) -> bytes:
        return self._h(self._pad(s_int))

    def m1_of(self, ident: bytes, salt: bytes, a_int: int, b_int: int,
              key: bytes) -> bytes:
        h_n = self._h(self._pad(self.n))
        h_g = self._h(self._pad(self.g))
        ng_xor = bytes(a ^ b for a, b in zip(h_n, h_g))
        return self._h(ng_xor + self._h(ident) + salt
                       + self._pad(a_int) + self._pad(b_int) + key)

    def m2_of(self, a_int: int, m1: bytes, key: bytes) -> bytes:
        return self._h(self._pad(a_int) + m1 + key)

    @property
    def m1_len(self) -> int:
        return self._digest(b"").digest_size


# The registered account variants. The 1024-bit/SHA-1 appendix-B replay
# dialect is built in tests, never registered for accounts.
VARIANTS: dict[str, SrpDialect] = {
    DEFAULT_GROUP: Rfc5054Dialect(
        DEFAULT_GROUP, int(RFC5054_2048_N_HEX, 16), 2, hashlib.sha256),
    MANGOS_GROUP: MangosDialect(),
}


# ---------------------------------------------------------------------------------------------
# Verifier storage
# -----------------------------------------------------------------------------


class SrpStore:
    """JSON account file: {"users": {name: {"salt": hex, "verifier": hex,
    "group": name}}}.

    group names the dialect the verifier was computed under (verifiers are
    group-bound — they cannot be re-keyed, only re-registered). Rows without
    "group" are B4-era mangos rows: GRANDFATHERED as mangos-256 and kept
    byte-identically working (the migration law — no forced re-registration).
    salt encoding is the dialect's own (mangos: hex of the 32 LE bytes as an
    int, the B4 shape; RFC: big-endian hex). No password, no hash of the
    password, ever touches this file.
    """

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.users: dict[str, dict[str, str]] = {}
        self._load()

    # ------------------------------------------------------------- file ----
    def _load(self) -> None:
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._save()
            return
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        users = raw.get("users", {})
        if not isinstance(users, dict):
            raise ValueError(f"{self.path}: 'users' must be an object")
        self.users = users

    def _save(self) -> None:
        atomic_write_text(
            self.path,
            json.dumps({"users": self.users}, indent=2, sort_keys=True) + "\n",
        )

    # ------------------------------------------------------------ users ----
    @staticmethod
    def _check_name(user: str) -> str:
        # colon-free: both dialects hash I | b":" | P, so a colon in I would
        # be ambiguous (same law as auth.py's ensure_user)
        if not user or ":" in user:
            raise ValueError("username must be non-empty and colon-free")
        return user

    @staticmethod
    def _dialect(group: str) -> SrpDialect:
        try:
            return VARIANTS[group]
        except KeyError:
            raise ValueError(
                f"unknown SRP6 group {group!r} (known: {sorted(VARIANTS)})") from None

    def register(self, user: str, password: str, *,
                 salt: bytes | None = None,
                 group: str | None = None) -> dict[str, str]:
        """Create or reset an account under `group` (default: the RFC 5054
        2048-bit default): mint a salt, compute v = g^x mod N, store
        {salt, verifier, group}, forget the password. Returns the stored
        row. Re-registering an existing account UPGRADES it (a B4 mangos
        row re-registered becomes rfc5054-2048)."""
        self._check_name(user)
        dialect = self._dialect(group or DEFAULT_GROUP)
        if salt is None:
            # real entropy, not clock+counter: the named B4 deviation stands
            salt = secrets.token_bytes(dialect.salt_len)
        elif len(salt) != dialect.salt_len:
            raise ValueError(f"salt must be {dialect.salt_len} bytes")
        ident, pw = dialect.normalize(user, password)
        v = dialect.verifier(ident, pw, salt)
        row = {"salt": dialect.salt_wire(salt),
               "verifier": _hex(v),
               "group": dialect.name}
        # read-modify-write under the store lock: Q21 (2026-10-01) proved the
        # unlocked shape loses concurrent registrations (last-writer-wins)
        with exclusive(self.path):
            self._load()
            self.users[user] = row
            self._save()
        return dict(row)

    def lookup(self, user: str) -> tuple[SrpDialect, bytes, int] | None:
        """(dialect, salt bytes, v) for an account, or None (the decoy path
        handles it). B4 rows without "group" are grandfathered mangos."""
        row = self.users.get(user)
        if row is None:
            return None
        dialect = self._dialect(row.get("group", MANGOS_GROUP))
        salt = dialect.salt_decode(row.get("salt"))
        if salt is None or not row.get("verifier"):
            raise ValueError(f"{self.path}: account {user!r} has a malformed row")
        return dialect, salt, int(row["verifier"], 16)

    def has_user(self, user: str) -> bool:
        return user in self.users


# ---------------------------------------------------------------------------------------------
# The handshake service (server side)
# -----------------------------------------------------------------------------


@dataclass
class PendingHandshake:
    """One single-use challenge. Burns at first proof receipt (the nonce law)."""
    user: str          # wire-canonical identity (mangos upper, RFC verbatim)
    ident: bytes       # identity bytes as the dialect hashes them
    dialect: SrpDialect
    salt: bytes
    v: int
    b_secret: int
    b_int: int
    a_int: int
    decoy: bool = False


class Srp6AuthService:
    """Owns the SRP6 server state: the account store plus the per-connection
    pending handshakes. The enforcement point (server/server.py) calls
    register / begin_challenge / verify_proof keyed by the connection id, so
    pending challenges die with their connection (drop).

    default_group: what NEW registrations and decoy challenges use
    (rfc5054-2048 unless overridden — the R5 default).
    allow_mangos: the COMPAT FLAG. True (default) keeps the CMaNGOS
    training path alive: mangos registrations are accepted and grandfathered
    B4 rows keep logging in. False RETIRES the variant: both raise
    ValueError, which the server answers with its existing typed BAD_AUTH
    path — re-registration is the only way home for those accounts."""

    def __init__(self, store: SrpStore, *,
                 default_group: str = DEFAULT_GROUP,
                 allow_mangos: bool = True) -> None:
        if default_group not in VARIANTS:
            raise ValueError(f"unknown default group {default_group!r}")
        self.store = store
        self.default = VARIANTS[default_group]
        self.allow_mangos = allow_mangos
        self._pending: dict[Any, PendingHandshake] = {}

    # --------------------------------------------------------- register ----
    def register(self, user: str, password: str, *,
                 salt: bytes | None = None,
                 group: str | None = None) -> dict[str, str]:
        group = group or self.default.name
        if group == MANGOS_GROUP and not self.allow_mangos:
            raise ValueError(
                "mangos-256 is retired on this service (allow_mangos=False); "
                "re-register under the rfc5054 default")
        return self.store.register(user, password, salt=salt, group=group)

    # -------------------------------------------------------- challenge ----
    def begin_challenge(self, key: Any, user: str, a_wire: Any, *,
                        b_secret: int | None = None) -> dict[str, str]:
        """Issue (salt, B) for the caller's A (wire hex), under the dialect
        the ACCOUNT ROW names (grandfathered rows speak mangos; new rows
        speak rfc5054). Replaces any pending handshake for this key (a fresh
        challenge is always legal — but it burns the old one: only the
        newest B is provable against). Raises ValueError on a malformed A,
        a malformed username, or a retired group; unknown users get a decoy
        challenge in the default dialect (no enumeration)."""
        self.store._check_name(user)
        found = self.store.lookup(user)
        if found is not None:
            dialect, salt, v = found
            if dialect.name == MANGOS_GROUP and not self.allow_mangos:
                raise ValueError(
                    "mangos-256 is retired on this service "
                    "(allow_mangos=False); the account must re-register")
            decoy = False
        else:
            # decoy: deterministic public material; the wire shape is
            # identical to a real challenge in the DEFAULT dialect
            dialect = self.default
            ident = dialect.ident_of(user)
            salt = hashlib.sha256(b"srp6-decoy:" + ident).digest()[:dialect.salt_len]
            v = dialect.verifier(ident, b"SRP6-DECOY-PASSWORD", salt)
            decoy = True
        a_int = _int_or_none(a_wire)
        if a_int is None or not 0 < a_int < dialect.n:
            raise ValueError(f"A must be lowercase-hex int in 1..N-1 for {dialect.name}")
        ident = dialect.ident_of(user)
        if b_secret is None:
            b_secret = secrets.randbits(SECRET_BITS)  # named deviation, docstring
        b_int = dialect.public_b(v, b_secret)
        self._pending[key] = PendingHandshake(
            user=dialect.display_user(user), ident=ident, dialect=dialect,
            salt=salt, v=v, b_secret=b_secret, b_int=b_int, a_int=a_int,
            decoy=decoy)
        return {"user": dialect.display_user(user),
                "salt": dialect.salt_wire(salt),
                "b": _hex(b_int),
                "group": dialect.name}  # for the wire follow-up (dropped today)

    # ------------------------------------------------------------ proof ----
    def verify_proof(self, key: Any, user: str, m1_wire: Any) -> dict[str, Any]:
        """Consume the pending handshake and check M1 (wire hex). BURNS AT
        RECEIPT: the pending entry is spent whether the proof passes, fails,
        or is garbage (the ReceiptGate nonce law — a replayed tape finds no
        challenge).

        Returns {"ok": True, "sid", "m2", "session_key"} on success, else
        {"ok": False, "why": "STALE_CHALLENGE" | "BAD_PROOF"}."""
        pending = self._pending.pop(key, None)
        if pending is None or pending.user != pending.dialect.display_user(user):
            return {"ok": False, "why": "STALE_CHALLENGE"}
        dialect = pending.dialect
        m1 = _hexbytes_or_none(m1_wire)
        if m1 is None or len(m1) != dialect.m1_len or pending.decoy:
            return {"ok": False, "why": "BAD_PROOF"}

        a_int, b_int, v = pending.a_int, pending.b_int, pending.v
        u = dialect.u_of(a_int, b_int)
        if u == 0 and dialect.name != MANGOS_GROUP:
            # RFC 5054 rejects degenerate u (~2^-256 with SHA-256); the
            # mangos path keeps its historical behavior (differential law)
            return {"ok": False, "why": "BAD_PROOF"}
        s_int = dialect.server_s(a_int, v, u, pending.b_secret)
        key = dialect.session_key(s_int)
        m1_server = dialect.m1_of(pending.ident, pending.salt, a_int, b_int, key)
        if not hmac.compare_digest(m1_server, m1):
            return {"ok": False, "why": "BAD_PROOF"}
        m2 = dialect.m2_of(a_int, m1, key)
        # sid mints from handshake material: K differs per handshake (fresh b),
        # so the sid is unforgeable without completing the exchange, and the
        # shape stays the v0 64-hex sid (world.register_session is agnostic)
        sid = hashlib.sha256(
            f"srp6-sid:{pending.user}:{key.hex()}".encode("utf-8")).hexdigest()
        return {"ok": True, "sid": sid, "m2": m2.hex(),
                "session_key": key.hex()}

    # ----------------------------------------------------------- hygiene ----
    def drop(self, key: Any) -> None:
        """Connection gone: its pending handshake (if any) dies with it."""
        self._pending.pop(key, None)

    def pending_count(self) -> int:
        return len(self._pending)


def _hexbytes_or_none(text: Any) -> bytes | None:
    """Wire hex -> bytes, typed refusal (None) on anything malformed."""
    if not isinstance(text, str) or not text:
        return None
    try:
        return bytes.fromhex(text)
    except ValueError:
        return None


def main(argv: list[str] | None = None) -> int:  # pragma: no cover - operability
    argv = list(sys.argv[1:] if argv is None else argv)
    usage = "usage: python -m server.auth_srp6 <users.json> add <username> [group]"
    if len(argv) not in (3, 4) or argv[1] != "add":
        print(usage)
        return 2
    path, _, user = argv[0], argv[1], argv[2]
    group = argv[3] if len(argv) == 4 else None
    if group is not None and group not in VARIANTS:
        print(f"unknown group {group!r}; known: {sorted(VARIANTS)}")
        return 2
    import getpass

    password = getpass.getpass(f"password for {user}: ")
    SrpStore(path).register(user, password, group=group)
    print(f"srp6 account {user!r} written to {path} "
          f"(group {group or DEFAULT_GROUP}; salt + verifier; no password stored)")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
