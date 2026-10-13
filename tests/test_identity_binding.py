"""Identity-binding tests (C1 step 4, 2026-09-30): the server side of the
GitHub-published SSH-key challenge (server/identity_binding.py).

THE FIXTURE LAW: every keypair in this file is LOCALLY GENERATED at test time
(ssh-keygen -t ed25519 -N "" into a tmp dir) — never a real key, never the
network. The fetch surface is exercised against a fake urlopen (URL shape,
timeout, status mapping) and the parse surface against synthetic .keys
bodies; the only live subprocess calls are ssh-keygen sign/verify themselves,
which is the standard path under test.

The certification strategy: verify_proof is driven END TO END with real
ssh-keygen signatures — the same binary, armor format, and -Y dialect Adam
will use — so a passing roundtrip means the server speaks OpenSSH's own
sshsig dialect, proven by the same bytes (the test_realmd_client /
test_auth_srp6 differential pattern: the peer side is the reference
implementation).

Laws under test:
    table law      identity_challenge / identity_proof are frozen rows in
                   IDENTITY_AUTH_TABLE (a NEW contract version); DEFAULT and
                   PROTOCOL_DIGEST unmoved; gate before verb holds
    username law   the GitHub login grammar is the injection law (URL,
                   allowed_signers principal, -I argument)
    parse law      strict: known keytype + valid base64 + agreeing wire type,
                   no silent skipping; the fingerprint matches ssh-keygen -lf
    fetch law      exact URL, timeout set, no auth; 404/network/empty map to
                   a typed IdentityFetchError -> NO_KEYS
    challenge law  nonce + issued + expires in the exact-bytes template;
                   pending is single-use per connection, replaced on re-mint,
                   killed by drop
    proof law      burn at receipt (success, failure, garbage); expiry from
                   the mint clock; wrong key / tampered bytes / wrong
                   namespace / missing armor / missing binary all BAD_PROOF;
                   the Adam stdin-sign flow certifies the receipt's command
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import urllib.error
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.identity_binding import (  # noqa: E402
    IDENTITY_AUTH_DISPATCH,
    IDENTITY_AUTH_TABLE,
    IdentityBindService,
    IdentityError,
    IdentityFetchError,
    PublicKeyLine,
    fetch_github_keys,
    parse_public_keys,
    validate_username,
)
from server.protocol_table import (  # noqa: E402
    DEFAULT_TABLE,
    PROTOCOL_DIGEST,
    compile_table,
)

SSH_KEYGEN = shutil.which("ssh-keygen") or "ssh-keygen"
SIGN_TIMEOUT = 30.0


# ------------------------------------------------------------------ fixtures ----


@pytest.fixture(scope="session")
def fixture_key(tmp_path_factory) -> Path:
    """The LOCALLY-GENERATED fixture keypair (never a real key): ed25519,
    no passphrase, comment marks it as a test artifact."""
    path = tmp_path_factory.mktemp("identity_fixture") / "fixture_ed25519"
    proc = subprocess.run(
        [SSH_KEYGEN, "-q", "-t", "ed25519", "-N", "", "-C",
         "mag-test-fixture", "-f", str(path)],
        capture_output=True, timeout=SIGN_TIMEOUT)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    return path


@pytest.fixture(scope="session")
def other_key(tmp_path_factory) -> Path:
    """A second, different fixture keypair (the wrong-key adversary)."""
    path = tmp_path_factory.mktemp("identity_other") / "other_ed25519"
    proc = subprocess.run(
        [SSH_KEYGEN, "-q", "-t", "ed25519", "-N", "", "-C",
         "mag-test-fixture-other", "-f", str(path)],
        capture_output=True, timeout=SIGN_TIMEOUT)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    return path


@pytest.fixture(scope="session")
def fixture_pub(fixture_key: Path) -> PublicKeyLine:
    """The fixture's public key, parsed the way the GitHub fetch would."""
    return parse_public_keys(
        fixture_key.with_suffix(".pub").read_text(encoding="ascii"))[0]


class Clock:
    """Frozen, advanceable clock: determinism for expiry + issued/expires."""

    def __init__(self, t: float = 1_800_000_000.0) -> None:
        self.t = t

    def __call__(self) -> float:
        return self.t

    def advance(self, seconds: float) -> None:
        self.t += seconds


def _service(keys: tuple[PublicKeyLine, ...], clock: Clock, **kwargs
             ) -> IdentityBindService:
    return IdentityBindService(fetcher=lambda user: keys, now=clock, **kwargs)


def _sign(priv: Path, message: str, *, namespace: str = "core",
          stdin_mode: bool = False, name: str = "challenge.txt") -> str:
    """Sign with real ssh-keygen — the reference peer.

    file mode  (the everyday shape): writes <name>, signs it, reads .sig
    stdin mode (the receipt's literal Adam command): -Y sign reads the
               message from stdin and writes the armor to stdout"""
    if stdin_mode:
        proc = subprocess.run(
            [SSH_KEYGEN, "-Y", "sign", "-n", namespace, "-f", str(priv)],
            input=message.encode("utf-8"), capture_output=True,
            timeout=SIGN_TIMEOUT)
        assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
        return proc.stdout.decode("ascii")
    workdir = priv.parent
    message_path = workdir / name
    message_path.write_bytes(message.encode("utf-8"))  # exact bytes, no EOL xlat
    proc = subprocess.run(
        [SSH_KEYGEN, "-Y", "sign", "-n", namespace, "-f", str(priv),
         str(message_path)],
        capture_output=True, timeout=SIGN_TIMEOUT)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    sig = (workdir / (name + ".sig")).read_text(encoding="ascii")
    (workdir / (name + ".sig")).unlink()
    message_path.unlink()
    return sig


def _minted(svc: IdentityBindService, user: str = "adam"):
    out = svc.mint_challenge("conn", user)
    assert out["ok"] is True, out
    return out


# ------------------------------------------------------------------ table law ----


def test_identity_verbs_are_frozen_rows_and_default_stays_unmoved():
    assert IDENTITY_AUTH_TABLE.verbs == DEFAULT_TABLE.verbs + (
        "identity_challenge", "identity_proof")
    for verb in ("identity_challenge", "identity_proof"):
        row = IDENTITY_AUTH_TABLE.row(verb)
        assert row.required_state == "CONNECTED" and row.args == ()
        assert row.handler_name == f"auth_{verb}"
        assert row.reject_code == "UNKNOWN_SID"
    # the real laws ride the closed vocabulary (LW6/LW7 law), transport disjoint
    assert {"BAD_PROOF", "STALE_CHALLENGE", "NO_KEYS"} <= set(
        IDENTITY_AUTH_TABLE.reject_codes)
    assert (IDENTITY_AUTH_TABLE.transport_reject_codes
            == DEFAULT_TABLE.transport_reject_codes)
    # DEFAULT is byte-identical and untouched: digest pinned, no verb leaked
    assert "identity_challenge" not in DEFAULT_TABLE.verbs
    assert compile_table(None).digest == PROTOCOL_DIGEST


def test_gate_before_verb_on_the_identity_rows():
    ok = IDENTITY_AUTH_DISPATCH.ask("identity_proof", "CONNECTED")
    assert ok["ok"] is True and ok["handler"] == "auth_identity_proof"
    assert ok["required_state"] == "CONNECTED" and ok["handler_ran"] is True
    # an authed peer may re-run the binding handshake (re-bind is legal)
    assert IDENTITY_AUTH_DISPATCH.ask("identity_challenge", "AUTHED")["ok"] is True
    # the verbs do not exist on the bound v0 contract
    assert DEFAULT_TABLE.row("identity_challenge") is None
    # internal invariant guard: a state outside the enum refuses typed
    bad = IDENTITY_AUTH_DISPATCH.ask("identity_proof", "BOGUS_STATE")
    assert bad == {"ok": False, "reason": "UNKNOWN_STATE", "handler_ran": False}


# -------------------------------------------------------------- username law ----


@pytest.mark.parametrize("good", ["adam", "ItsCommodore", "a-b", "A" * 39, "a1"])
def test_username_grammar_accepts_github_logins(good):
    assert validate_username(good) == good


@pytest.mark.parametrize("bad", [
    "", "a" * 40, "a b", "a/b", "../keys", "a?b", "a_b", "a:b", "-a", "a-",
    "a\nb", "a#frag", None, 123, ["adam"],
])
def test_username_grammar_refuses_injection_shapes(bad):
    with pytest.raises(IdentityError):
        validate_username(bad)


# ---------------------------------------------------------------- parse law ----


def test_parse_public_keys_strict(fixture_pub: PublicKeyLine, other_key: Path):
    other_line = other_key.with_suffix(".pub").read_text(encoding="ascii")
    # a real two-key body (the GitHub page shape) parses whole
    body = f"{fixture_key_line(fixture_pub)}\n\n{other_line}"
    keys = parse_public_keys(body)
    assert len(keys) == 2
    assert keys[0].keytype == "ssh-ed25519" and keys[0] == fixture_pub
    assert keys[1].comment == "mag-test-fixture-other"
    # blob round-trips and fingerprint has the standard shape
    assert keys[0].blob_b64 == fixture_pub.blob_b64
    assert keys[0].fingerprint.startswith("SHA256:") and "=" not in keys[0].fingerprint
    # the allowed_signers line is principal + the exact published fields
    line = keys[0].to_signers_line("adam")
    assert line == f"adam {fixture_pub.keytype} {fixture_pub.blob_b64}"


def fixture_key_line(key: PublicKeyLine) -> str:
    return f"{key.keytype} {key.blob_b64} {key.comment}"


@pytest.mark.parametrize("junk", [
    "not a key line at all",
    "ssh-ed25519 !!!not-base64!!!",
    "ssh-ed25519 YWJj",  # decodes, but blob wire type is not ssh-ed25519
    "ssh-gpg-openpgp AAAAB3NzaC1yc2EAAAADAQABAAABgQ==",
])
def test_parse_public_keys_fails_closed_on_junk(junk):
    with pytest.raises(IdentityError):
        parse_public_keys(junk)


def test_parse_public_keys_empty_body_is_no_keys():
    assert parse_public_keys("") == ()
    assert parse_public_keys("\n \n") == ()


# ---------------------------------------------------------------- fetch law ----


class _FakeResponse:
    def __init__(self, status: int, body: bytes) -> None:
        self.status = status
        self._body = body

    def read(self, limit: int = -1) -> bytes:
        return self._body if limit < 0 else self._body[:limit]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def test_fetch_hits_the_exact_url_with_timeout_no_auth(monkeypatch, fixture_pub):
    seen = {}

    def fake_urlopen(request, timeout=None):
        seen["url"] = request.full_url
        seen["timeout"] = timeout
        seen["ua"] = request.get_header("User-agent")
        return _FakeResponse(200, fixture_key_line(fixture_pub).encode())

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    keys = fetch_github_keys("ItsCommodore", timeout=7.5)
    assert seen["url"] == "https://github.com/ItsCommodore.keys"
    assert seen["timeout"] == 7.5 and seen["ua"].startswith("mag-identity-binding")
    assert keys == (fixture_pub,)
    # the grammar is the injection law: a bad login never reaches the network
    with pytest.raises(IdentityError):
        fetch_github_keys("../users?x=")


def test_fetch_maps_failures_to_typed_errors(monkeypatch, fixture_pub):
    # 404 = no such user / no keys published (LW2's signal)
    def raise_404(request, timeout=None):
        raise urllib.error.HTTPError(request.full_url, 404, "Not Found", {}, None)

    monkeypatch.setattr("urllib.request.urlopen", raise_404)
    with pytest.raises(IdentityFetchError, match="404"):
        fetch_github_keys("ghost-user")

    def raise_net(request, timeout=None):
        raise urllib.error.URLError("name resolution failed")

    monkeypatch.setattr("urllib.request.urlopen", raise_net)
    with pytest.raises(IdentityFetchError, match="failed"):
        fetch_github_keys("adam")

    # 200 but zero usable keys is also NO_KEYS-shaped (fail closed)
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout=None: _FakeResponse(200, b"\n"))
    with pytest.raises(IdentityFetchError, match="no usable keys"):
        fetch_github_keys("adam")

    # a non-200 non-404 status is typed too
    monkeypatch.setattr(
        "urllib.request.urlopen",
        lambda request, timeout=None: _FakeResponse(503, b""))
    with pytest.raises(IdentityFetchError, match="503"):
        fetch_github_keys("adam")


# ------------------------------------------------------------- challenge law ----


def test_mint_challenge_shape_and_pending_lifecycle(fixture_pub):
    clock = Clock(1_800_000_000.0)
    svc = _service((fixture_pub,), clock, ttl_seconds=300,
                   nonce_fn=lambda: "ab12" * 8)
    out = _minted(svc)
    # the exact-bytes template: every line a signer can eyeball
    assert out["challenge"] == (
        "the-mountain identity binding v1\n"
        "user: adam\n"
        "nonce: ab12ab12ab12ab12ab12ab12ab12ab12\n"
        "issued: 2027-01-15T08:00:00Z\n"
        "expires: 2027-01-15T08:05:00Z")
    assert not out["challenge"].endswith("\n")  # exact-bytes law, no EOL
    assert out["nonce"] == "ab12" * 8 and out["expires"] == "2027-01-15T08:05:00Z"
    assert svc.pending_count() == 1
    # re-mint replaces (burns) the old pending: only the newest proves
    _minted(svc)
    assert svc.pending_count() == 1
    # drop kills the pending with its connection
    svc.drop("conn")
    assert svc.pending_count() == 0


def test_mint_challenge_typed_refusals(fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    assert svc.mint_challenge("conn", "bad name")["why"] == "BAD_AUTH"
    assert svc.mint_challenge("conn", "../keys")["why"] == "BAD_AUTH"
    svc = IdentityBindService(
        fetcher=lambda user: (_ for _ in ()).throw(
            IdentityFetchError("HTTP 404")), now=clock)
    out = svc.mint_challenge("conn", "ghost")
    assert out["ok"] is False and out["why"] == "NO_KEYS"
    assert "404" in out["detail"]


# ---------------------------------------------------------------- proof law ----


def test_roundtrip_sign_verify_with_real_ssh_keygen(fixture_key, fixture_pub):
    """THE core test: mint -> sign (file mode) -> verify. The peer is real
    ssh-keygen, so passing means the server speaks OpenSSH's sshsig dialect."""
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"])
    assert sig.startswith("-----BEGIN SSH SIGNATURE-----")
    res = svc.verify_proof("conn", "adam", sig)
    assert res["ok"] is True and res["user"] == "adam"
    # the fingerprint the server reports is the one ssh-keygen itself prints
    assert res["fingerprint"] == _ssh_keygen_fingerprint(fixture_key)
    assert res["fingerprint"] == fixture_pub.fingerprint


def test_adam_stdin_sign_flow_certifies_the_receipt_command(fixture_key, fixture_pub):
    """The receipt's literal Adam command — ssh-keygen -Y sign -n core
    < challenge.txt — signs from stdin and writes the armor to stdout; the
    server verifies that armor without any accommodation."""
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"], stdin_mode=True)
    assert sig.startswith("-----BEGIN SSH SIGNATURE-----")
    assert svc.verify_proof("conn", "adam", sig)["ok"] is True


def test_wrong_key_rejects_bad_proof(other_key, fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    out = _minted(svc)
    sig = _sign(other_key, out["challenge"])  # the adversary's key
    assert svc.verify_proof("conn", "adam", sig) == {
        "ok": False, "why": "BAD_PROOF"}


def test_tampered_challenge_rejects_bad_proof(fixture_key, fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"].replace("user: adam", "user: root"))
    assert svc.verify_proof("conn", "adam", sig)["why"] == "BAD_PROOF"


def test_wrong_namespace_rejects_bad_proof(fixture_key, fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"], namespace="file")
    assert svc.verify_proof("conn", "adam", sig)["why"] == "BAD_PROOF"


def test_replay_burns_at_receipt_even_on_garbage(fixture_key, fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"])
    assert svc.verify_proof("conn", "adam", sig)["ok"] is True
    # replay 1: the exact proof bytes again -> the pending burned at the
    # successful receipt, so the tape finds no challenge
    assert svc.verify_proof("conn", "adam", sig)["why"] == "STALE_CHALLENGE"
    # replay 2: garbage burns a fresh pending just the same (burn-at-receipt)
    out2 = _minted(svc)
    assert svc.verify_proof("conn", "adam", "not-a-signature")["why"] == "BAD_PROOF"
    good = _sign(fixture_key, out2["challenge"])
    assert svc.verify_proof("conn", "adam", good)["why"] == "STALE_CHALLENGE"


def test_expired_challenge_rejects_stale(fixture_key, fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock, ttl_seconds=300)
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"])
    clock.advance(301)  # past expiry: the signed string said when it dies
    assert svc.verify_proof("conn", "adam", sig)["why"] == "STALE_CHALLENGE"
    # within TTL it would have passed (the boundary is the signed expiry)
    clock2 = Clock()
    svc2 = _service((fixture_pub,), clock2, ttl_seconds=300)
    out2 = _minted(svc2)
    sig2 = _sign(fixture_key, out2["challenge"])
    clock2.advance(299)
    assert svc2.verify_proof("conn", "adam", sig2)["ok"] is True


def test_user_mismatch_and_armor_shape_laws(fixture_key, fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock)
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"])
    # a proof naming a DIFFERENT user than the pending challenge
    assert svc.verify_proof("conn", "ben", sig)["why"] == "STALE_CHALLENGE"
    # proof with no pending handshake at all
    assert svc.verify_proof("no-such-conn", "adam", sig)["why"] == "STALE_CHALLENGE"
    # armor markers missing / non-string payload -> BAD_PROOF, burn included:
    # EACH bad needs a fresh mint (the previous one burned at its receipt)
    for bad in ("", "-----BEGIN PGP SIGNATURE-----x", None, 5):
        _minted(svc)
        assert svc.verify_proof("conn", "adam", bad)["why"] == "BAD_PROOF"
    assert svc.verify_proof("conn", "adam", sig)["why"] == "STALE_CHALLENGE"


def test_missing_ssh_keygen_binary_fails_closed(fixture_key, fixture_pub):
    clock = Clock()
    svc = _service((fixture_pub,), clock, ssh_keygen="definitely-not-ssh-keygen-mag")
    out = _minted(svc)
    sig = _sign(fixture_key, out["challenge"])
    assert svc.verify_proof("conn", "adam", sig)["why"] == "BAD_PROOF"


# ---------------------------------------------------------------- reference ----


def _ssh_keygen_fingerprint(priv: Path) -> str:
    """The reference fingerprint straight from ssh-keygen -lf (the tool the
    estate already trusts); our hashlib fingerprint must match it exactly."""
    proc = subprocess.run(
        [SSH_KEYGEN, "-lf", str(priv.with_suffix(".pub"))],
        capture_output=True, timeout=SIGN_TIMEOUT)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    # "<bits> SHA256:xxx comment (keytype)"
    return proc.stdout.decode("ascii").split()[1]
