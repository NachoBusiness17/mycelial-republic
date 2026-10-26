"""SRP6 account-system tests — R5 (2026-09-30): RFC 5054 2048-bit/SHA-256 as
the DEFAULT, the mangos 256-bit variant behind the compat flag.

Certification strategy (two independent oracles):
    RFC path    RFC 5054 Appendix B vectors (1024-bit group + SHA-1) replayed
                through the dialect API itself — k, x, v, A, B, u, the server
                premaster AND the client premirror all match the published
                bytes. The 2048-bit default group's N is checked against the
                RFC 5054 Appendix A.2 #3 constant (bit length + probable
                prime + safe prime). M1/M2 have no published RFC vector; they
                ride the RFC 2945 [SRP-RFC] evidence shape and are certified
                by cross-derivation (server formula vs the independent
                client formula in RFC 5054 §2.6).
    mangos path the CLIENT side is tools.realmd_client.client_session itself —
                the exact math wire-verified against the live CMaNGOS realmd
                on 2026-09-30 — so a passing roundtrip means our compat
                dialect speaks the proven little-endian SRP6 dialect.

Laws under test:
    rfc vectors     Appendix B replays; 2048-bit N is the RFC constant
    default         new registrations land in rfc5054-2048 + SHA-256
    roundtrip       both groups: register -> challenge -> proof -> welcome
                    (m2 verified) -> world action acks
    wrong password  rejects BAD_PROOF in BOTH groups (fresh-challenge
                    recovery included)
    compat flag     allow_mangos=False retires the variant (register AND
                    grandfathered challenge refuse); rfc path unaffected
    migration       B4 rows without "group" are grandfathered mangos-256 and
                    keep authenticating; re-registration upgrades the row
    replay/nonce    a pending handshake is SINGLE-USE and burns at receipt
    no enumeration  unknown users get a well-formed decoy challenge in the
                    default dialect and the same BAD_PROOF
    fallback flag   hello stays the flag-gated plaintext fallback
    table law       the srp_* verbs are frozen rows in SRP6_AUTH_TABLE
"""
from __future__ import annotations

import asyncio
import hashlib
import secrets
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tools.realmd_client as rc  # noqa: E402
from server.auth import AuthStore  # noqa: E402
from server.auth_srp6 import (  # noqa: E402
    DEFAULT_GROUP,
    MANGOS_GROUP,
    RFC5054_2048_N_HEX,
    Rfc5054Dialect,
    Srp6AuthService,
    SrpStore,
    VARIANTS,
)
from server.protocol_table import (  # noqa: E402
    DEFAULT_TABLE,
    PROTOCOL_DIGEST,
    SRP6_AUTH_DISPATCH,
    SRP6_AUTH_TABLE,
)
from server.server import Client, WorldServer  # noqa: E402

SALT = bytes(range(1, 33))  # the same fixed salt as the realmd golden vectors
RFC = VARIANTS[DEFAULT_GROUP]  # the rfc5054-2048 dialect under test

# ---------------------------------------------------------------------------------------------
# RFC 5054 Appendix B vectors (1024-bit group, SHA-1) — byte-truth from the
# published RFC text; every constant below is consumed by
# test_rfc5054_appendix_b_vectors.
# ---------------------------------------------------------------------------------------------
RFCB_N = 0xEEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3
RFCB_SALT = bytes.fromhex("BEB25379D1A8581EB5A727673A2441EE")
RFCB_K = 0x7556AA045AEF2CDD07ABAF0F665C3E818913186F
RFCB_X = 0x94B7555AABE9127CC58CCF4993DB6CF84D16C124
RFCB_V = 0x7E273DE8696FFC4F4E337D05B4B375BEB0DDE1569E8FA00A9886D8129BADA1F1822223CA1A605B530E379BA4729FDC59F105B4787E5186F5C671085A1447B52A48CF1970B4FB6F8400BBF4CEBFBB168152E08AB5EA53D15C1AFF87B2B9DA6E04E058AD51CC72BFC9033B564E26480D78E955A5E29E7AB245DB2BE315E2099AFB
RFCB_A_SECRET = 0x60975527035CF2AD1989806F0407210BC81EDC04E2762A56AFD529DDDA2D4393
RFCB_B_SECRET = 0xE487CB59D31AC550471E81F00F6928E01DDA08E974A004F49E61F5D105284D20
RFCB_A = 0x61D5E490F6F1B79547B0704C436F523DD0E560F0C64115BB72557EC44352E8903211C04692272D8B2D1A5358A2CF1B6E0BFCF99F921530EC8E39356179EAE45E42BA92AEACED825171E1E8B9AF6D9C03E1327F44BE087EF06530E69F66615261EEF54073CA11CF5858F0EDFDFE15EFEAB349EF5D76988A3672FAC47B0769447B
RFCB_B = 0xBD0C61512C692C0CB6D041FA01BB152D4916A1E77AF46AE105393011BAF38964DC46A0670DD125B95A981652236F99D9B681CBF87837EC996C6DA04453728610D0C6DDB58B318885D7D82C7F8DEB75CE7BD4FBAA37089E6F9C6059F388838E7A00030B331EB76840910440B1B27AAEAEEB4012B7D7665238A8E3FB004B117B58
RFCB_U = 0xCE38B9593487DA98554ED47D70A7AE5F462EF019
RFCB_S = 0xB0DC82BABCF30674AE450C0287745E7990A3381F63B387AAF271A10D233861E359B48220F7C4693C9AE12B0A6F67809F0876E2D013800D6C41BB59B6D5979B5C00A172B4A2A5903A0BDCAF8A709585EB2AFAFA8F3499B200210DCC1F10EB33943CD67FC88A2F39A4BE5BEC4EC0A3212DC346D7E474B29EDE8A469FFECA686E5A


# ---------------------------------------------------------------------------------------------
# Client-side mirrors (independent of the server's formulas)
# ---------------------------------------------------------------------------------------------


def rfc_client_session(dialect: Rfc5054Dialect, user: str, password: str,
                       salt: bytes, b_int: int, a_secret: int) -> dict:
    """The CLIENT formula from RFC 5054 §2.6: S = (B - k*g^x)^(a + u*x) % N.
    Independent of the server's S = (A * v^u)^b % N; agreement is the SRP
    property itself, certified against the Appendix B premaster above."""
    ident = dialect.ident_of(user)
    pw = password.encode("ascii")
    x = dialect.x_of(ident, pw, salt)
    a_int = pow(dialect.g, a_secret, dialect.n)
    u = dialect.u_of(a_int, b_int)
    s_int = pow(b_int - dialect.multiplier() * pow(dialect.g, x, dialect.n),
                a_secret + u * x, dialect.n) % dialect.n
    key = dialect.session_key(s_int)
    m1 = dialect.m1_of(ident, salt, a_int, b_int, key)
    return {"a_int": a_int, "u": u, "s_int": s_int, "session_key": key,
            "m1": m1, "m2_expected": dialect.m2_of(a_int, m1, key)}


def _is_probable_prime(m: int, rounds: int = 12) -> bool:
    """Small deterministic-enough Miller-Rabin (fixed seeded bases) — enough
    to catch a corrupted N constant, not a proof."""
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if m % p == 0:
            return m == p
    d, r = m - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    import random
    rng = random.Random(0x5054)
    for _ in range(rounds):
        a = rng.randrange(2, m - 1)
        x = pow(a, d, m)
        if x in (1, m - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, m)
            if x == m - 1:
                break
        else:
            return False
    return True


async def _start_server(tmp_path: Path, *, allow_plaintext_hello: bool = True,
                        register: tuple[str, str] | None = ("ada", "steam"),
                        group: str | None = None,
                        allow_mangos: bool = True) -> WorldServer:
    auth = AuthStore(tmp_path / "users.json")
    auth.ensure_user("ada", "steam")
    svc = Srp6AuthService(SrpStore(tmp_path / "srp_users.json"),
                          allow_mangos=allow_mangos)
    if register is not None:
        svc.register(*register, group=group)
    srv = WorldServer(
        port=0, tick_interval=None, auth=auth, srp_auth=svc,
        allow_plaintext_hello=allow_plaintext_hello,
        log_path=tmp_path / "world_log.jsonl",
    )
    return await srv.start()


class SrpClient:
    """Drives the SRP6 handshake over our wire for EITHER dialect.

    mangos: the proven client math (tools.realmd_client.client_session).
    rfc5054: the RFC 5054 §2.6 client formula (rfc_client_session above)."""

    def __init__(self, client: Client, dialect=RFC):
        self.client = client
        self.dialect = dialect
        self.last_b = 0
        self.last_salt = b""
        self.a_secret = 0

    async def register(self, user: str, password: str) -> dict:
        await self.client.send({"op": "srp_register", "user": user, "pass": password})
        return await self.client.recv()

    async def challenge(self, user: str, a_secret: int | None = None) -> tuple[dict, int, int]:
        """Returns (reply, parsed salt bytes, a_secret used)."""
        self.a_secret = a_secret if a_secret is not None else secrets.randbits(256)
        a_int = pow(self.dialect.g, self.a_secret, self.dialect.n)
        await self.client.send({"op": "srp_challenge", "user": user,
                                "a": f"{a_int:x}"})
        reply = await self.client.recv()
        if reply.get("op") == "reject":
            return reply, b"", self.a_secret
        self.last_b = int(reply["b"], 16)
        self.last_salt = self.dialect.salt_decode(reply["salt"])
        return reply, self.last_salt, self.a_secret

    async def proof(self, user: str, password: str, salt: bytes, b_int: int,
                    a_secret: int) -> tuple[dict, dict]:
        """Sends M1 computed by the dialect's client math for `password`.
        Returns (reply, session dict with m1/m2_expected/session_key)."""
        if self.dialect.name == MANGOS_GROUP:
            ch = rc.Challenge(b_int=b_int, g_int=rc.G, n_int=rc.N,
                              salt_le=salt, version_challenge=b"", security_flags=0)
            sess = rc.client_session(user, password, ch, a_secret=a_secret)
        else:
            sess = rfc_client_session(self.dialect, user, password, salt,
                                      b_int, a_secret)
        await self.client.send({"op": "srp_proof", "user": user,
                                "m1": sess["m1"].hex()})
        return await self.client.recv(), sess

    async def login(self, user: str, password: str,
                    password_used: str | None = None) -> tuple[dict, dict]:
        """Full handshake. password_used lets a test compute M1 for the WRONG
        password (the attacker's view) while keeping one code path."""
        reply, salt, a = await self.challenge(user)
        assert reply.get("op") == "srp_challenge", reply
        return await self.proof(user, password_used or password, salt,
                                self.last_b, a)


def _tmp_store() -> SrpStore:
    return SrpStore(Path(tempfile.mkdtemp(prefix="srp6_unit_")) / "srp_users.json")


# ----------------------------------------------------------- RFC 5054 vectors ----


def test_rfc5054_appendix_b_vectors():
    """The published RFC 5054 test vectors (1024-bit group, SHA-1) must
    reproduce through the dialect API: k, x, v, A, B, u, the server premaster
    AND the client §2.6 premirror. This certifies every padding convention
    the 2048-bit default inherits (PAD to |N| bytes, big-endian, k and u
    hash shapes)."""
    d = Rfc5054Dialect("rfc5054-1024", RFCB_N, 2, hashlib.sha1)
    assert d.n_len == 128 and d.m1_len == 20
    assert d.multiplier() == RFCB_K
    assert d.x_of(b"alice", b"password123", RFCB_SALT) == RFCB_X
    assert d.verifier(b"alice", b"password123", RFCB_SALT) == RFCB_V
    assert pow(2, RFCB_A_SECRET, RFCB_N) == RFCB_A
    assert d.public_b(RFCB_V, RFCB_B_SECRET) == RFCB_B
    assert d.u_of(RFCB_A, RFCB_B) == RFCB_U
    assert d.server_s(RFCB_A, RFCB_V, RFCB_U, RFCB_B_SECRET) == RFCB_S
    # the client formula, independent derivation, same published premaster
    assert rfc_client_session(d, "alice", "password123", RFCB_SALT,
                              RFCB_B, RFCB_A_SECRET)["s_int"] == RFCB_S


def test_default_group_is_rfc5054_2048_sha256():
    """The registered default: RFC 5054 Appendix A.2 #3 group (g=2, safe
    prime — N byte-checked against the RFC text), SHA-256, 16-byte salt,
    32-byte M1."""
    assert DEFAULT_GROUP == "rfc5054-2048"
    assert int(RFC5054_2048_N_HEX, 16) == RFC.n and RFC.n.bit_length() == 2048
    assert RFC.g == 2 and RFC.n_len == 256
    assert RFC.salt_len == 16 and RFC.m1_len == 32
    assert _is_probable_prime(RFC.n) and _is_probable_prime((RFC.n - 1) // 2)
    # the compat variant is registered but NOT the default
    assert set(VARIANTS) == {DEFAULT_GROUP, MANGOS_GROUP}
    assert VARIANTS[MANGOS_GROUP].n == rc.N and VARIANTS[MANGOS_GROUP].g == rc.G


# ------------------------------------------------------------------ store ----


def test_store_default_register_lands_rfc5054_mangos_keeps_b4_shape(tmp_path):
    store = SrpStore(tmp_path / "srp_users.json")
    row = store.register("ada", "steam")  # no group: the R5 default
    assert row["group"] == DEFAULT_GROUP
    assert len(row["salt"]) == 32  # 16-byte salt, big-endian hex
    assert 0 < int(row["verifier"], 16) < RFC.n
    # nothing password-shaped ever hits the disk
    disk = (tmp_path / "srp_users.json").read_text(encoding="utf-8")
    assert "steam" not in disk.lower() and "hash" not in disk
    # file round-trip: the verifier + group is all a reboot needs
    dialect, salt, v = SrpStore(tmp_path / "srp_users.json").lookup("ada")
    assert dialect.name == DEFAULT_GROUP and len(salt) == 16
    assert v == int(row["verifier"], 16)
    # the mangos compat row keeps the exact B4 byte shape (plus "group")
    mrow = store.register("Legacy", "OldPass", salt=SALT, group=MANGOS_GROUP)
    want_v = rc.srp6_verifier(b"LEGACY", b"OLDPASS", SALT)
    assert mrow == {"salt": f"{int.from_bytes(SALT, 'little'):x}",
                    "verifier": f"{want_v:x}", "group": MANGOS_GROUP}
    mdialect, msalt, mv = store.lookup("Legacy")
    assert mdialect.name == MANGOS_GROUP and msalt == SALT and mv == want_v
    # reset rotates credentials and stays in its group (fresh salt => fresh v)
    row2 = store.register("ada", "other")
    assert row2["group"] == DEFAULT_GROUP
    assert row2["salt"] != row["salt"] and row2["verifier"] != row["verifier"]
    assert store.lookup("ada")[2] == int(row2["verifier"], 16)
    assert store.has_user("ben") is False


def test_store_refuses_ambiguous_identities_and_bad_salts(tmp_path):
    store = SrpStore(tmp_path / "srp_users.json")
    with pytest.raises(ValueError, match="colon-free"):
        store.register("a:b", "x")
    with pytest.raises(ValueError, match="non-empty"):
        store.register("", "x")
    with pytest.raises(ValueError, match="16 bytes"):
        store.register("ada", "x", salt=b"\x01" * 15)
    with pytest.raises(ValueError, match="32 bytes"):
        store.register("ada", "x", salt=b"\x01" * 31, group=MANGOS_GROUP)
    with pytest.raises(ValueError, match="unknown SRP6 group"):
        store.register("ada", "x", group="mangos-128")


def test_b4_rows_are_grandfathered_and_re_registration_upgrades(tmp_path):
    """THE MIGRATION LAW: a row written by B4 (salt+verifier, no "group")
    authenticates as mangos-256 byte-identically; the NEXT re-registration
    upgrades the row to the RFC default. No forced re-registration."""
    path = tmp_path / "srp_users.json"
    legacy_v = rc.srp6_verifier(b"ADA", b"STEAM", SALT)
    path.write_text(
        '{"users": {"ada": {"salt": "%s", "verifier": "%s"}}}'
        % (f"{int.from_bytes(SALT, 'little'):x}", f"{legacy_v:x}"),
        encoding="utf-8")
    store = SrpStore(path)
    dialect, salt, v = store.lookup("ada")
    assert (dialect.name, salt, v) == (MANGOS_GROUP, SALT, legacy_v)
    # grandfathered login still proves against the proven client math
    svc = Srp6AuthService(store)
    a_secret = 0xABCD
    a_int = pow(rc.G, a_secret, rc.N)
    out = svc.begin_challenge("k", "ada", f"{a_int:x}", b_secret=0x1234)
    ch = rc.Challenge(b_int=int(out["b"], 16), g_int=rc.G, n_int=rc.N,
                      salt_le=int(out["salt"], 16).to_bytes(32, "little"),
                      version_challenge=b"", security_flags=0)
    sess = rc.client_session("ada", "steam", ch, a_secret=a_secret)
    assert svc.verify_proof("k", "ada", sess["m1"].hex())["ok"] is True
    # re-registration (same op, same password) upgrades the row
    store.register("ada", "steam")
    assert store.lookup("ada")[0].name == DEFAULT_GROUP


# ------------------------------------------------- math (the differential) ----


def test_service_math_agrees_with_the_proven_client_mangos():
    """The compat dialect's M1/M2/K must equal tools.realmd_client
    byte for byte — the same differential that certified the client against
    realmd's SRP6.cpp, now run against OUR dialect surface."""
    a_secret = 0x0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF
    b_secret = 0xFEDCBA9876543210FEDCBA9876543210FEDCBA9876543210FEDCBA9876543210
    svc = Srp6AuthService(_tmp_store())
    svc.register("DiffUser", "Password1", salt=SALT, group=MANGOS_GROUP)
    a_int = pow(rc.G, a_secret, rc.N)
    out = svc.begin_challenge("k1", "DiffUser", f"{a_int:x}", b_secret=b_secret)
    assert out["user"] == "DIFFUSER" and out["group"] == MANGOS_GROUP

    ch = rc.Challenge(b_int=int(out["b"], 16), g_int=rc.G, n_int=rc.N,
                      salt_le=int(out["salt"], 16).to_bytes(32, "little"),
                      version_challenge=b"", security_flags=0)
    sess = rc.client_session("DiffUser", "Password1", ch, a_secret=a_secret)
    res = svc.verify_proof("k1", "DiffUser", sess["m1"].hex())
    assert res["ok"] is True
    assert res["m2"] == sess["m2_expected"].hex()
    assert res["session_key"] == sess["session_key"].hex()
    assert len(res["sid"]) == 64 and int(res["sid"], 16) >= 0


def test_service_math_rfc2048_server_client_agreement():
    """Server S=(A*v^u)^b vs client S=(B-k*g^x)^(a+u*x) on the DEFAULT
    group: M1/M2/K must agree across the two independent formulas (the SRP
    property; the shared helpers are Appendix-B-certified)."""
    a_secret = 0x0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF
    b_secret = 0xFEDCBA9876543210FEDCBA9876543210FEDCBA9876543210FEDCBA9876543210
    svc = Srp6AuthService(_tmp_store())
    svc.register("DiffUser", "Password1", salt=b"\x07" * 16)
    a_int = pow(RFC.g, a_secret, RFC.n)
    out = svc.begin_challenge("k1", "DiffUser", f"{a_int:x}", b_secret=b_secret)
    assert out["user"] == "DiffUser"  # verbatim identity, the RFC law
    assert out["group"] == DEFAULT_GROUP
    assert len(out["b"]) <= 512 and 0 < int(out["b"], 16) < RFC.n
    sess = rfc_client_session(RFC, "DiffUser", "Password1",
                              bytes.fromhex(out["salt"]), int(out["b"], 16),
                              a_secret)
    res = svc.verify_proof("k1", "DiffUser", sess["m1"].hex())
    assert res["ok"] is True
    assert res["m2"] == sess["m2_expected"].hex()
    assert res["session_key"] == sess["session_key"].hex()
    assert len(bytes.fromhex(res["session_key"])) == 32


def test_pending_is_single_use_and_dies_with_the_connection():
    svc = Srp6AuthService(_tmp_store())
    svc.register("ada", "steam", salt=SALT, group=MANGOS_GROUP)
    a_int = pow(rc.G, 0xAA, rc.N)
    svc.begin_challenge("k", "ada", f"{a_int:x}")
    assert svc.pending_count() == 1
    # a fresh challenge replaces (burns) the old one: only the newest B proves
    svc.begin_challenge("k", "ada", f"{a_int:x}")
    assert svc.pending_count() == 1
    # burn at receipt, even on garbage (mangos M1 is 20 bytes)
    assert svc.verify_proof("k", "ada", "not-hex")["why"] == "BAD_PROOF"
    assert svc.verify_proof("k", "ada", "00" * 20)["why"] == "STALE_CHALLENGE"
    # the RFC dialect wants 32-byte proofs (typed length refusal, not stale)
    svc.register("rfc", "steam", salt=b"\x09" * 16)
    a2 = pow(RFC.g, 0xAA, RFC.n)
    svc.begin_challenge("k2", "rfc", f"{a2:x}")
    assert svc.verify_proof("k2", "rfc", "00" * 20)["why"] == "BAD_PROOF"
    assert svc.verify_proof("k2", "rfc", "00" * 32)["why"] == "STALE_CHALLENGE"
    # connection drop kills the pending challenge
    svc.begin_challenge("k", "ada", f"{a_int:x}")
    svc.drop("k")
    assert svc.verify_proof("k", "ada", "00" * 20)["why"] == "STALE_CHALLENGE"
    assert svc.pending_count() == 0


# --------------------------------------------------------- the compat flag ----


def test_compat_flag_retires_mangos_but_not_the_default(tmp_path):
    svc = Srp6AuthService(_tmp_store(), allow_mangos=False)
    # registration into the retired variant refuses, named
    with pytest.raises(ValueError, match="retired"):
        svc.register("ada", "x", group=MANGOS_GROUP)
    # a grandfathered mangos row refuses at challenge, named
    svc.store.users["legacy"] = {
        "salt": f"{int.from_bytes(SALT, 'little'):x}", "verifier": "abc"}
    svc.store._save()
    with pytest.raises(ValueError, match="retired"):
        svc.begin_challenge("k", "legacy", f"{pow(rc.G, 5, rc.N):x}")
    # the default path is untouched
    row = svc.register("fresh", "pw")
    assert row["group"] == DEFAULT_GROUP
    a_int = pow(RFC.g, 0x42, RFC.n)
    out = svc.begin_challenge("k2", "fresh", f"{a_int:x}")
    assert out["group"] == DEFAULT_GROUP
    # flag ON (default): the CMaNGOS training path keeps working
    svc_on = Srp6AuthService(_tmp_store())
    assert svc_on.register("ada", "x", group=MANGOS_GROUP)["group"] == MANGOS_GROUP


# ----------------------------------------------------------- wire: TCP laws ----


def test_register_handshake_roundtrip_default_rfc5054(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)  # default group: rfc5054-2048
        c = SrpClient(await Client.connect("127.0.0.1", srv.bound_port))
        r = await c.register("ada", "steam")
        assert r == {"op": "srp_registered", "user": "ada"}
        w, sess = await c.login("ada", "steam")
        # welcome is the standard session welcome plus the server proof M2
        assert w["op"] == "welcome" and w["auth"] == "srp6"
        assert len(w["sid"]) == 64
        assert w["m2"] == sess["m2_expected"].hex()  # the mutual proof
        assert w["world"]["nodes"]["spring"]["volume"] == 6
        # the SRP6 session IS a world session: actions ack and ticks flow
        raw = c.client
        await raw.send({"op": "action", "sid": w["sid"], "verb": "boil",
                        "target": "spring", "n": 1})
        ack = await raw.recv()
        assert ack["op"] == "ack" and ack["user"] == "ADA"
        await srv.pump_once()
        t = await raw.recv()
        assert t["op"] == "tick" and "ADA boils 1 at spring" in " | ".join(t["events"])
        assert srv.stats()["srp_sessions"] == 1
        raw.close()
        await srv.stop()

    asyncio.run(scenario())


def test_register_handshake_roundtrip_mangos_compat(tmp_path):
    async def scenario():
        # account seeded through the service API with group=MANGOS_GROUP (the
        # CMaNGOS training shape): the wire srp_register op always lands in
        # the service DEFAULT group, so compat rows come from the CLI/service
        srv = await _start_server(tmp_path, group=MANGOS_GROUP)
        c = SrpClient(await Client.connect("127.0.0.1", srv.bound_port),
                      dialect=VARIANTS[MANGOS_GROUP])
        w, sess = await c.login("ada", "steam")  # the PROVEN client math
        assert w["op"] == "welcome" and w["m2"] == sess["m2_expected"].hex()
        assert w["auth"] == "srp6"
        assert srv.stats()["srp_sessions"] == 1
        c.client.close()
        await srv.stop()

    asyncio.run(scenario())


def test_wrong_password_rejects_in_both_groups_then_recovers(tmp_path):
    async def scenario():
        # default (rfc5054-2048)
        srv = await _start_server(tmp_path)
        c = SrpClient(await Client.connect("127.0.0.1", srv.bound_port))
        w, _ = await c.login("ada", "wrong-password")
        assert w == {"op": "reject", "why": "BAD_PROOF"}
        # burn-at-receipt: even the CORRECT M1 for the old B is now stale
        w2, _ = await c.proof("ada", "steam", c.last_salt, c.last_b, c.a_secret)
        assert w2 == {"op": "reject", "why": "STALE_CHALLENGE"}
        # a fresh challenge + the right password recovers
        w3, sess = await c.login("ada", "steam")
        assert w3["op"] == "welcome" and w3["m2"] == sess["m2_expected"].hex()
        assert srv.stats()["bad_proof"] >= 1 and srv.stats()["stale_challenge"] >= 1
        c.client.close()
        await srv.stop()

        # compat (mangos-256)
        srv2 = await _start_server(tmp_path / "mangos", group=MANGOS_GROUP)
        c2 = SrpClient(await Client.connect("127.0.0.1", srv2.bound_port),
                       dialect=VARIANTS[MANGOS_GROUP])
        w4, _ = await c2.login("ada", "wrong-password")
        assert w4 == {"op": "reject", "why": "BAD_PROOF"}
        w5, sess5 = await c2.login("ada", "steam")
        assert w5["op"] == "welcome" and w5["m2"] == sess5["m2_expected"].hex()
        assert srv2.stats()["bad_proof"] >= 1
        c2.client.close()
        await srv2.stop()

    asyncio.run(scenario())


def test_replayed_handshake_cannot_re_earn_a_session(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        client = await Client.connect("127.0.0.1", srv.bound_port)
        c = SrpClient(client)
        # manual login so the ORIGINAL B is retained for the replay contrast
        reply1, salt1, a1 = await c.challenge("ada")
        assert reply1["op"] == "srp_challenge"
        w, sess = await c.proof("ada", "steam", salt1, c.last_b, a1)
        assert w["op"] == "welcome"
        sid = w["sid"]
        b_first = c.last_b

        # replay 1: the exact proof bytes again -> the pending burned at the
        # successful receipt, so the tape finds no challenge (post-welcome
        # frames carry the M1 MAC layer's mac/seq fields — compare the law,
        # not the whole frame)
        await client.send({"op": "srp_proof", "user": "ada",
                           "m1": sess["m1"].hex()})
        r1 = await client.recv()
        assert r1["op"] == "reject" and r1["why"] == "STALE_CHALLENGE"

        # replay 2: the whole pair, same A and same M1 -> fresh b => fresh B,
        # and M1 covers B, so the old proof is now simply WRONG
        reply2, salt2, a2 = await c.challenge("ada", a_secret=a1)  # same A
        assert reply2["op"] == "srp_challenge"
        assert c.last_b != b_first  # random b: the challenge is not the taped one
        await client.send({"op": "srp_proof", "user": "ada",
                           "m1": sess["m1"].hex()})
        r2 = await client.recv()
        assert r2["op"] == "reject" and r2["why"] == "BAD_PROOF"

        # nothing re-earned: one session, one sid, still the only valid one
        assert srv.stats()["srp_sessions"] == 1
        await client.send({"op": "action", "sid": sid, "verb": "boil",
                           "target": "spring", "n": 1})
        assert (await client.recv())["op"] == "ack"
        client.close()
        await srv.stop()

    asyncio.run(scenario())


def test_unknown_user_gets_a_decoy_no_enumeration_on_the_wire(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        client = await Client.connect("127.0.0.1", srv.bound_port)
        c = SrpClient(client)
        # a REAL account's challenge shapes (for comparison)
        real_reply, real_salt, real_a = await c.challenge("ada")
        ghost = SrpClient(await Client.connect("127.0.0.1", srv.bound_port))
        g_reply, g_salt, g_a = await ghost.challenge("ghost-user")
        # the decoy is well-formed and indistinguishable in shape: parseable
        # 16-byte salt and 2048-bit B, same op and key set, no reject at
        # challenge stage (decoys speak the DEFAULT dialect)
        assert g_reply["op"] == real_reply["op"] == "srp_challenge"
        assert set(g_reply) == set(real_reply) == {"op", "user", "salt", "b"}
        for reply in (g_reply, real_reply):
            assert 0 < int(reply["salt"], 16) < 2 ** 128
            assert 0 < int(reply["b"], 16) < 2 ** 2048
        # and its proof fails with the SAME code as a wrong password
        w, _ = await ghost.proof("ghost-user", "anything", g_salt,
                                 ghost.last_b, g_a)
        assert w == {"op": "reject", "why": "BAD_PROOF"}
        real = await Client.connect("127.0.0.1", srv.bound_port)
        rc_ = SrpClient(real)
        w2, _ = await rc_.login("ada", "wrong-password")
        assert w2["why"] == w["why"]  # one code, the v0 no-enumeration law
        client.close(); ghost.client.close(); real.close()
        await srv.stop()

    asyncio.run(scenario())


def test_malformed_wire_values_reject_typed(tmp_path):
    async def scenario():
        srv = await _start_server(tmp_path)
        client = await Client.connect("127.0.0.1", srv.bound_port)
        c = SrpClient(client)
        # challenge-stage garbage: non-hex / zero / N-or-bigger A (per group)
        rfc_n = f"{RFC.n:x}"
        for bad in ("zzz", "0", rfc_n, None, 123):
            await client.send({"op": "srp_challenge", "user": "ada", "a": bad})
            assert (await client.recv()) == {"op": "reject", "why": "BAD_AUTH"}
        # proof with no pending handshake at all
        await client.send({"op": "srp_proof", "user": "ada", "m1": "00" * 32})
        assert (await client.recv()) == {"op": "reject", "why": "STALE_CHALLENGE"}
        # proof for a DIFFERENT user than the pending challenge
        await c.challenge("ada")
        await client.send({"op": "srp_proof", "user": "ben", "m1": "00" * 32})
        assert (await client.recv()) == {"op": "reject", "why": "STALE_CHALLENGE"}
        # short / long / non-hex M1 against a live pending: BAD_PROOF, burn included
        for bad in ("abcd", "00" * 20, "00" * 33, 5):
            await c.challenge("ada")  # fresh pending each time (each burns on proof)
            await client.send({"op": "srp_proof", "user": "ada", "m1": bad})
            assert (await client.recv()) == {"op": "reject", "why": "BAD_PROOF"}
        # register-stage: ambiguous identity
        await client.send({"op": "srp_register", "user": "a:b", "pass": "x"})
        assert (await client.recv()) == {"op": "reject", "why": "BAD_AUTH"}
        # srp ops on a server with no SRP service configured
        bare = await _start_server(tmp_path / "bare", register=None)
        bare.srp_auth = None  # exercise the None path directly
        b = await Client.connect("127.0.0.1", bare.bound_port)
        await b.send({"op": "srp_challenge", "user": "ada", "a": "ff"})
        assert (await b.recv()) == {"op": "reject", "why": "BAD_AUTH"}
        b.close()
        await bare.stop()
        client.close()
        await srv.stop()

    asyncio.run(scenario())


def test_retired_mangos_answers_bad_auth_on_the_wire(tmp_path):
    async def scenario():
        # a B4-era file + a retired service: the account is refused at
        # challenge (BAD_AUTH, the existing typed path), the default path runs
        path = tmp_path / "srp_users.json"
        legacy_v = rc.srp6_verifier(b"ADA", b"STEAM", SALT)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            '{"users": {"ada": {"salt": "%s", "verifier": "%s"}}}'
            % (f"{int.from_bytes(SALT, 'little'):x}", f"{legacy_v:x}"),
            encoding="utf-8")
        auth = AuthStore(tmp_path / "users.json")
        auth.ensure_user("ada", "steam")
        svc = Srp6AuthService(SrpStore(path), allow_mangos=False)
        srv = WorldServer(port=0, tick_interval=None, auth=auth, srp_auth=svc,
                          log_path=tmp_path / "world_log.jsonl")
        await srv.start()
        client = await Client.connect("127.0.0.1", srv.bound_port)
        a_int = pow(rc.G, 0x11, rc.N)
        await client.send({"op": "srp_challenge", "user": "ada",
                           "a": f"{a_int:x}"})
        assert await client.recv() == {"op": "reject", "why": "BAD_AUTH"}
        # the RFC path on the same retired service works end to end
        await client.send({"op": "srp_register", "user": "new", "pass": "pw"})
        assert (await client.recv())["op"] == "srp_registered"
        w, sess = await SrpClient(client, RFC).login("new", "pw")
        assert w["op"] == "welcome" and w["m2"] == sess["m2_expected"].hex()
        client.close()
        await srv.stop()

    asyncio.run(scenario())


# ------------------------------------------------------- the fallback flag ----


def test_plaintext_hello_is_the_flag_gated_fallback(tmp_path):
    async def scenario():
        # flag ON (default): the v0 door still opens, no SRP6 fields added
        # (the welcome shape is B15's — op/sid/world/room — untouched by B4/R5)
        srv = await _start_server(tmp_path)
        c = await Client.connect("127.0.0.1", srv.bound_port)
        w = await c.do_hello("ada", "steam")
        assert w["op"] == "welcome" and "m2" not in w and len(w["sid"]) == 64
        assert set(w) == {"op", "sid", "world", "room"}
        c.close()
        await srv.stop()

        # flag OFF: hello is refused, SRP6 is the only way in
        srv2 = await _start_server(tmp_path / "off", allow_plaintext_hello=False)
        c2 = await Client.connect("127.0.0.1", srv2.bound_port)
        await c2.send({"op": "hello", "user": "ada", "pass": "steam"})
        assert await c2.recv() == {"op": "reject", "why": "BAD_AUTH"}
        w2, sess = await SrpClient(c2).login("ada", "steam")
        assert w2["op"] == "welcome" and w2["m2"] == sess["m2_expected"].hex()
        assert w2["room"] == srv2.rooms.default_room.id  # B15 shape, both doors
        c2.close()
        await srv2.stop()

    asyncio.run(scenario())


# ----------------------------------------------------------- the table law ----


def test_srp6_verbs_are_frozen_rows_and_default_stays_unmoved():
    # the new contract carries the auth verbs behind the DEFAULT rows
    assert SRP6_AUTH_TABLE.verbs == DEFAULT_TABLE.verbs + (
        "srp_register", "srp_challenge", "srp_proof")
    for row in SRP6_AUTH_TABLE.rows[:len(DEFAULT_TABLE.rows)]:
        assert row.required_state == "AUTHED"  # DEFAULT rows rode along whole
    for verb in ("srp_register", "srp_challenge", "srp_proof"):
        row = SRP6_AUTH_TABLE.row(verb)
        assert row.required_state == "CONNECTED" and row.args == ()
        assert row.handler_name == f"auth_{verb}"
    # the real laws ride the closed vocabulary (LW6/LW7 law), transport disjoint
    assert {"BAD_PROOF", "STALE_CHALLENGE"} <= set(SRP6_AUTH_TABLE.reject_codes)
    assert SRP6_AUTH_TABLE.transport_reject_codes == DEFAULT_TABLE.transport_reject_codes
    # DEFAULT is byte-identical and untouched: digest pinned, no verb leaked
    assert "srp_register" not in DEFAULT_TABLE.verbs
    from server.protocol_table import compile_table
    assert compile_table(None).digest == PROTOCOL_DIGEST


def test_gate_before_verb_on_the_srp6_rows():
    ok = SRP6_AUTH_DISPATCH.ask("srp_proof", "CONNECTED")
    assert ok == {"ok": True, "reason": "DISPATCHED", "handler": "auth_srp_proof",
                  "required_state": "CONNECTED", "args": None, "handler_ran": True}
    # an authed peer may re-run the handshake (re-login is legal)
    assert SRP6_AUTH_DISPATCH.ask("srp_challenge", "AUTHED")["ok"] is True
    # the verbs do not exist on the bound v0 contract
    assert DEFAULT_TABLE.row("srp_proof") is None
    # internal invariant guard: a state outside the enum refuses typed
    bad = SRP6_AUTH_DISPATCH.ask("srp_proof", "BOGUS_STATE")
    assert bad == {"ok": False, "reason": "UNKNOWN_STATE", "handler_ran": False}
