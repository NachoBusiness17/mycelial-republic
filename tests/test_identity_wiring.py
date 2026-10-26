"""Identity WIRING tests (V7 owed-next, landed 2026-10-01): the hello path
meets the key-bound identity (receipt watch/inbox/last_mile_20260930/
V7_IDENTITY_BIND.md, "Owed next" section — this lane).

The V7 module (server/identity_binding.py, tests/test_identity_binding.py)
proved the challenge/proof math against real ssh-keygen; what it could not
prove is the wiring the receipt owed: the op ladder gating
identity_challenge/identity_proof through IDENTITY_AUTH_DISPATCH, the
_grant on a good proof with the binding recorded on the session row, the
grant-time binding policy flag (shape mirroring allow_plaintext_hello), and
the stats() counters. Every law here is the receipt's "Owed next" list,
one test per line.

THE FIXTURE LAW (inherited from tests/test_identity_binding.py): every
keypair is LOCALLY GENERATED at test time (ssh-keygen -t ed25519 -N "") —
never a real key, never the network. The fetcher is a fake (returns the
fixture's public line); the only live subprocess is ssh-keygen sign itself,
the reference peer.

Laws under test:
    promotion     protocol_table.IDENTITY_AUTH_* is byte-identical to
                  identity_binding.IDENTITY_AUTH_* (one contract, digest
                  pinned to the receipt's value; DEFAULT unmoved)
    policy (a)    with allow_unbound_hello False, hello without an identity
                  proof on the connection rejects typed BAD_AUTH (the v0
                  one-code law; "any connection can hold a sid" stops)
    bind (b)      a good proof GRANTS a session (the srp_proof precedent)
                  and binds the key to the sid: session_identities[sid] is
                  the {user, fingerprint} record, the welcome states it
                  (auth:"identity"), and a bound connection's LATER hello
                  grants a sid that carries the same binding
    typed law     STALE_CHALLENGE (no pending / replay), BAD_PROOF (wrong
                  key), BAD_AUTH (login grammar), NO_KEYS (fetch failed)
                  all fire through the wire with the receipt's counters
    compat        default flags keep the v0 door open: hello with NO
                  identity at all still grants, byte-shape v0 (no auth key)
"""
from __future__ import annotations

import asyncio
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.auth import AuthStore  # noqa: E402
from server.identity_binding import (  # noqa: E402
    IDENTITY_AUTH_TABLE as MODULE_TABLE,
    IdentityBindService,
    IdentityFetchError,
    parse_public_keys,
)
from server.protocol_table import (  # noqa: E402
    DEFAULT_TABLE,
    IDENTITY_AUTH_DIGEST,
    IDENTITY_AUTH_TABLE,
    PROTOCOL_DIGEST,
)
from server.server import Client, WorldServer  # noqa: E402

SSH_KEYGEN = shutil.which("ssh-keygen") or "ssh-keygen"
SIGN_TIMEOUT = 30.0

# The receipt's pinned digests (trust bytes): the promoted table IS the
# module's table, and the bound v0 wire never moved.
RECEIPT_IDENTITY_DIGEST = (
    "9de8ad04e75e2e1c46fadc844187a57f942b8c08542ff925760b08b2362b9897")
RECEIPT_PROTOCOL_DIGEST = (
    "d41f7cba635174628cfdff928555de340258ac6f33612dfb84217ff0958179cf")


# ------------------------------------------------------------------ fixtures ----


@pytest.fixture(scope="session")
def fixture_key(tmp_path_factory) -> Path:
    """The LOCALLY-GENERATED fixture keypair (never a real key)."""
    path = tmp_path_factory.mktemp("wiring_fixture") / "fixture_ed25519"
    proc = subprocess.run(
        [SSH_KEYGEN, "-q", "-t", "ed25519", "-N", "", "-C",
         "mag-test-fixture", "-f", str(path)],
        capture_output=True, timeout=SIGN_TIMEOUT)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    return path


@pytest.fixture(scope="session")
def other_key(tmp_path_factory) -> Path:
    """A second, different fixture keypair (the wrong-key adversary)."""
    path = tmp_path_factory.mktemp("wiring_other") / "other_ed25519"
    proc = subprocess.run(
        [SSH_KEYGEN, "-q", "-t", "ed25519", "-N", "", "-C",
         "mag-test-fixture-other", "-f", str(path)],
        capture_output=True, timeout=SIGN_TIMEOUT)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    return path


@pytest.fixture(scope="session")
def fixture_pub(fixture_key: Path):
    return parse_public_keys(
        fixture_key.with_suffix(".pub").read_text(encoding="ascii"))[0]


def _identity_service(fixture_pub, fetcher=None) -> IdentityBindService:
    """The wired service: fake fetcher by default (never the network)."""
    return IdentityBindService(
        fetcher=fetcher or (lambda user: (fixture_pub,)))


async def _start_server(tmp_path: Path, *, fixture_pub=None,
                        fetcher=None,
                        allow_unbound_hello: bool = True) -> WorldServer:
    auth = AuthStore(tmp_path / "users.json")
    auth.ensure_user("ada", "steam")
    srv = WorldServer(
        port=0, tick_interval=None, auth=auth,
        log_path=tmp_path / "world_log.jsonl",
        identity=_identity_service(fixture_pub, fetcher),
        allow_unbound_hello=allow_unbound_hello,
    )
    return await srv.start()


def _sign(priv: Path, message: str) -> str:
    """The Adam stdin-sign flow (the receipt's literal command): -Y sign
    reads the message from stdin, armor to stdout — real ssh-keygen is the
    reference peer."""
    proc = subprocess.run(
        [SSH_KEYGEN, "-Y", "sign", "-n", "core", "-f", str(priv)],
        input=message.encode("utf-8"), capture_output=True,
        timeout=SIGN_TIMEOUT)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    return proc.stdout.decode("ascii")


async def _challenge(c: Client, user: str = "adam") -> dict:
    await c.send({"op": "identity_challenge", "user": user})
    return await c.recv()


async def _prove(c: Client, sig: str, user: str = "adam") -> dict:
    await c.send({"op": "identity_proof", "user": user, "sig": sig})
    return await c.recv()


async def _hello(c: Client, user: str, password: str) -> dict:
    """hello whose VERY NEXT line is the reply (reject or welcome)."""
    await c.send({"op": "hello", "user": user, "pass": password})
    return await c.recv()


# ----------------------------------------------------------------- promotion ----


def test_promoted_table_is_the_modules_table():
    """The promotion (B4's placement, assigned to the wiring lane by the V7
    receipt): protocol_table.IDENTITY_AUTH_* compiles byte-identical to
    identity_binding.IDENTITY_AUTH_* — one contract, digest pinned to the
    receipt's value — and the bound v0 wire (DEFAULT / PROTOCOL_DIGEST)
    never moved. This is the drift pin: either spec moving alone fails."""
    assert IDENTITY_AUTH_DIGEST == RECEIPT_IDENTITY_DIGEST
    assert IDENTITY_AUTH_TABLE.to_document() == MODULE_TABLE.to_document()
    assert IDENTITY_AUTH_TABLE.verbs == DEFAULT_TABLE.verbs + (
        "identity_challenge", "identity_proof")
    assert PROTOCOL_DIGEST == RECEIPT_PROTOCOL_DIGEST
    assert "identity_challenge" not in DEFAULT_TABLE.verbs


# ---------------------------------------------------------- policy law (a) ----


def test_hello_without_identity_proof_rejects_typed(tmp_path, fixture_pub):
    """With the binding policy on (allow_unbound_hello False — the flag
    shape the receipt says mirrors allow_plaintext_hello), a connection
    that never proved a key cannot hold a sid: hello rejects typed BAD_AUTH
    (the v0 hello one-code law — the same code the plaintext-door refusal
    uses, no new vocabulary). A WRONG password stays BAD_AUTH too: the
    policy refusal does not enumerate which law fired."""
    async def scenario():
        srv = await _start_server(tmp_path, fixture_pub=fixture_pub,
                                  allow_unbound_hello=False)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        r = await _hello(c, "ada", "steam")
        assert r == {"op": "reject", "why": "BAD_AUTH"}
        r = await _hello(c, "ada", "wrong")
        assert r == {"op": "reject", "why": "BAD_AUTH"}
        # nothing was granted: no session rows, no bound sids
        assert srv.session_identities == {}
        assert srv.stats()["identity_sessions"] == 0
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_default_flags_keep_the_v0_door_open(tmp_path, fixture_pub):
    """Backward compat IS the receipt's flag law: allow_unbound_hello
    defaults True (the standing no-regression law, exactly like
    allow_plaintext_hello), so v0 hello with NO identity at all still
    grants, and the welcome keeps the byte-shape v0 (no auth/identity
    keys). The identity ops ride alongside without changing the old door."""
    async def scenario():
        srv = await _start_server(tmp_path, fixture_pub=fixture_pub)
        assert srv.allow_unbound_hello is True
        c = await Client.connect("127.0.0.1", srv.bound_port)
        w = await c.do_hello("ada", "steam")
        assert w["op"] == "welcome" and len(w["sid"]) == 64
        assert "auth" not in w and "identity" not in w  # byte-shape v0
        assert srv.session_identities == {}
        c.close()
        await srv.stop()

    asyncio.run(scenario())


# ------------------------------------------------------------- bind law (b) ----


def test_proof_grants_a_key_bound_session(tmp_path, fixture_pub, fixture_key):
    """The receipt's owed wiring: _grant_session on a good proof. The proof
    itself grants (the srp_proof precedent) AND the key is bound to the
    sid: session_identities[sid] = {user, fingerprint} (the session-row
    record), the welcome states auth:"identity" + the binding, the world
    roster holds the sid under the GitHub login, stats() counts it."""
    async def scenario():
        srv = await _start_server(tmp_path, fixture_pub=fixture_pub)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        ch = await _challenge(c)
        assert ch["op"] == "identity_challenge" and ch["user"] == "adam"
        assert ch["challenge"].startswith("the-mountain identity binding v1\n")
        assert not ch["challenge"].endswith("\n")  # exact-bytes law
        sig = _sign(fixture_key, ch["challenge"])
        w = await _prove(c, sig)
        assert w["op"] == "welcome", w
        sid = w["sid"]
        assert len(sid) == 64 and int(sid, 16) >= 0  # the v0 sid grammar
        binding = {"user": "adam", "fingerprint": fixture_pub.fingerprint}
        assert w["auth"] == "identity" and w["identity"] == binding
        assert w["room"] == "summit"
        # THE record: the key is bound to the sid
        assert srv.session_identities[sid] == binding
        assert w["world"]["roster"][sid]["user"] == "adam"
        st = srv.stats()
        assert st["identity_sessions"] == 1 and st["identity_bound_sids"] == 1
        assert st["identity_bad_proof"] == 0 and st["identity_stale_challenge"] == 0
        c.close()
        await srv.stop()

    asyncio.run(scenario())


def test_hello_with_proof_binds_the_key_to_the_sid(tmp_path, fixture_pub,
                                                   fixture_key):
    """Hello WITH proof: on a bound connection, a later hello grants a sid
    that carries the same binding (the key follows the connection onto
    every session it grants), even under the strict policy. The sids are
    distinct (fresh grant per hello, the v0 law), both are answerable to
    the same key."""
    async def scenario():
        srv = await _start_server(tmp_path, fixture_pub=fixture_pub,
                                  allow_unbound_hello=False)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        # unbound hello refuses (law (a)); bind the connection first
        r = await _hello(c, "ada", "steam")
        assert r["why"] == "BAD_AUTH"
        ch = await _challenge(c)
        w1 = await _prove(c, _sign(fixture_key, ch["challenge"]))
        assert w1["op"] == "welcome" and w1["auth"] == "identity"
        # the SAME connection now hellos: the grant carries the binding
        w2 = await _hello(c, "ada", "steam")
        assert w2["op"] == "welcome"
        binding = {"user": "adam", "fingerprint": fixture_pub.fingerprint}
        assert w2["identity"] == binding and w2["auth"] == "identity"
        assert w2["sid"] != w1["sid"]
        assert srv.session_identities[w2["sid"]] == binding
        assert srv.session_identities[w1["sid"]] == binding
        assert srv.stats()["identity_bound_sids"] == 2
        c.close()
        await srv.stop()

    asyncio.run(scenario())


# -------------------------------------------------------------- typed laws ----


def test_typed_rejects_fire_through_the_wire(tmp_path, fixture_pub,
                                             fixture_key, other_key):
    """The dialect's closed vocabulary at the enforcement point: proof with
    no pending (STALE_CHALLENGE), wrong key (BAD_PROOF), login grammar
    (BAD_AUTH), failed fetch (NO_KEYS + the detail that is LW2's
    wrong-username signal). Counters file every identity reject."""
    async def scenario():
        srv = await _start_server(
            tmp_path, fixture_pub=fixture_pub,
            fetcher=lambda user: (_ for _ in ()).throw(
                IdentityFetchError("https://github.com/ghost.keys answered "
                                   "HTTP 404 (no such user or no keys published)")))
        c = await Client.connect("127.0.0.1", srv.bound_port)
        # proof with no pending challenge: the replay law's floor
        r = await _prove(c, "-----BEGIN SSH SIGNATURE-----x")
        assert r == {"op": "reject", "why": "STALE_CHALLENGE"}
        # grammar refusal fires BEFORE any fetch (the injection law)
        r = await _challenge(c, "../keys")
        assert r == {"op": "reject", "why": "BAD_AUTH"}
        # the fetch failed: NO_KEYS, with the operator's signal on the wire
        r = await _challenge(c, "ghost")
        assert r["op"] == "reject" and r["why"] == "NO_KEYS"
        assert "404" in r["detail"]
        c.close()
        await srv.stop()

    asyncio.run(scenario())

    async def scenario2():
        srv = await _start_server(tmp_path, fixture_pub=fixture_pub)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        ch = await _challenge(c)
        # the adversary's key over the real challenge: BAD_PROOF
        r = await _prove(c, _sign(other_key, ch["challenge"]))
        assert r == {"op": "reject", "why": "BAD_PROOF"}
        # the burned-at-receipt law: even the RIGHT proof now finds no
        # pending (the wrong-key receipt burned it)
        r = await _prove(c, _sign(fixture_key, ch["challenge"]))
        assert r == {"op": "reject", "why": "STALE_CHALLENGE"}
        st = srv.stats()
        assert st["identity_bad_proof"] == 1 and st["identity_stale_challenge"] == 1
        assert st["identity_sessions"] == 0  # nothing was ever granted
        # unknown op still UNKNOWN_OP (the ladder owns its else branch)
        await c.send({"op": "identity_bogus"})
        r = await c.recv()
        assert r["why"] == "UNKNOWN_OP"
        c.close()
        await srv.stop()

    asyncio.run(scenario2())


# --------------------------------------------------- module law still green ----


def test_identity_module_contract_survives_the_wiring(fixture_pub):
    """(c) of the wiring brief: the identity module's own contract is
    untouched by the wiring — the service still mints/verifies standalone
    (a fresh service over the same fixture key round-trips), and the full
    module suite (41 tests, tests/test_identity_binding.py) runs green in
    this lane's test command beside this file."""
    svc = IdentityBindService(fetcher=lambda user: (fixture_pub,))
    out = svc.mint_challenge("conn", "adam")
    assert out["ok"] is True and out["challenge"].startswith(
        "the-mountain identity binding v1\n")
    assert svc.verify_proof("conn", "adam", "garbage")["why"] == "BAD_PROOF"
    assert svc.verify_proof("conn", "adam", "garbage")["why"] == "STALE_CHALLENGE"
