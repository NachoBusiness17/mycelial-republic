"""auth: dead-simple v0 auth for the estate's world server.

HONEST SCOPE (read before trusting this):
    Users live in a JSON file with salted SHA256 password hashes.
    Session ids are sha256(user + salt + time_ns). The password crosses
    the wire in PLAINTEXT inside hello; there is no TLS, no SRP, no
    mutual proof, no replay protection beyond session-id entropy, no
    lockout. This is v0 scaffolding so the protocol shape (hello ->
    welcome -> sid-bearing actions) exists and is testable.

    The CMaNGOS lesson to port later is SRP6-class auth (what realmd
    does): the server never sees the password, client and server derive
    a shared proof, the session key falls out of the exchange. v1 owes
    exactly that. Until then this server binds to 127.0.0.1 and that is
    the whole security model.

    No RNG anywhere (estate determinism law): salts derive from
    user + clock, exactly like session ids. Salt entropy is therefore
    only as good as clock entropy, which is fine for v0 and would NOT
    be fine for production. Named here so nobody mistakes it later.

CLI (add a user interactively):
    .venv/Scripts/python.exe -m server.auth <users.json> add <username>
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
import time
from pathlib import Path

from .store_io import atomic_write_text, exclusive

# Deterministic monotonic counter (no RNG, estate law): two calls inside the
# same clock tick on a coarse-resolution Windows clock must still mint
# distinct salts and session ids. Caught by test_server_v0 on 2026-09-29,
# where time.time_ns() resolution was coarser than back-to-back calls.
_COUNTER = itertools.count(1)


def hash_password(salt: str, password: str) -> str:
    return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()


def _new_salt(user: str) -> str:
    # time + counter salted, not random: estate law is no RNG. See module docstring.
    material = f"salt:{user}:{time.time_ns()}:{next(_COUNTER)}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


class AuthStore:
    """JSON user file: {"users": {name: {"salt": hex16, "hash": sha256hex}}}."""

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
    def ensure_user(self, user: str, password: str) -> None:
        """Create or reset a user (new salt each call).

        Read-modify-write under the store lock: Q21 (2026-10-01) proved 8
        concurrent registrations on one file lost 7/8 when each instance
        saved its stale construction-time dict (last-writer-wins).
        """
        if not user or ":" in user:
            raise ValueError("username must be non-empty and colon-free")
        with exclusive(self.path):
            self._load()
            salt = _new_salt(user)
            self.users[user] = {"salt": salt, "hash": hash_password(salt, password)}
            self._save()

    def has_user(self, user: str) -> bool:
        return user in self.users

    def verify(self, user: str, password: str) -> bool:
        row = self.users.get(user)
        if row is None:
            # burn the same hash work so timing does not enumerate users
            hash_password("0" * 16, password)
            return False
        return row["hash"] == hash_password(row["salt"], password)

    # --------------------------------------------------------- sessions ----
    def new_session_id(self, user: str) -> str:
        row = self.users.get(user)
        if row is None:
            raise KeyError(f"no such user {user!r}")
        material = f"{user}{row['salt']}{time.time_ns()}:{next(_COUNTER)}"
        return hashlib.sha256(material.encode("utf-8")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 3 or argv[1] != "add":
        print("usage: python -m server.auth <users.json> add <username>")
        return 2
    path, _, user = argv
    import getpass

    password = getpass.getpass(f"password for {user}: ")
    store = AuthStore(path)
    store.ensure_user(user, password)
    print(f"user {user!r} written to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
