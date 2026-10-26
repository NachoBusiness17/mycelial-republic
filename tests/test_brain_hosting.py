"""Brain hosting (2026-10-17): seat handshake, brain manifest + append-only
replication, the one-way public lattice, and signed seat proposals.

Every path is redirected to tmp_path; the live-estate write fence in
tests/conftest.py stays armed (MAG_ALLOW_LIVE_WRITES must be unset). No
network, no rclone remote, no real key: keys are minted into tmp folders.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from mag import proposals as P  # noqa: E402
from mag import seat_handshake as sh  # noqa: E402

import brain_manifest as bm  # noqa: E402
import brain_replicate as br  # noqa: E402
import public_lattice_manifest as plm  # noqa: E402
import seat_keygen  # noqa: E402

FAKE_SK = "sk-" + "q9w8e7r6t5y4u3i2o1p0"
INIT = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})


def _seat(name):
    seed = sh.generate_seed()
    return name, seed, sh.public_from_seed(seed).hex()


@pytest.fixture
def seats():
    return {n: _seat(n) for n in ("grok", "gemini", "deepseek", "nacho")}


def _allow(seats, *, operators=(), quorum=2, omit=(), revoked=()):
    return {"schema": "seat_allowlist.v1", "skew_s": 60, "quorum": {"default": quorum},
            "operator_seats": list(operators),
            "seats": {n: {"public_hex": pub, **({"revoked": True} if n in revoked else {})}
                      for n, (_, _, pub) in seats.items() if n not in omit}}


# ═════════════════════════════ 1. seat handshake ═════════════════════════════

def test_handshake_accepts_valid_envelope(seats):
    name, seed, _ = seats["grok"]
    env = sh.wrap(INIT, seed=seed, seat_id=name)
    got = sh.verify_envelope(env, allowlist=_allow(seats), cache=sh.ReplayCache())
    assert got == ("grok", INIT)


def test_handshake_rejects_bad_signature(seats):
    name, seed, _ = seats["grok"]
    env = sh.wrap(INIT, seed=seed, seat_id=name)
    sig = env["mag_seat"]["sig"]
    env["mag_seat"]["sig"] = ("0" if sig[0] != "0" else "1") + sig[1:]
    assert sh.verify_envelope(env, allowlist=_allow(seats), cache=sh.ReplayCache()) is None


def test_handshake_rejects_tampered_body(seats):
    name, seed, _ = seats["grok"]
    env = sh.wrap(INIT, seed=seed, seat_id=name)
    env["body"] = INIT.replace("initialize", "tools/list")
    assert sh.verify_envelope(env, allowlist=_allow(seats), cache=sh.ReplayCache()) is None


def test_handshake_rejects_other_seats_key(seats):
    _, seed_b, _ = seats["gemini"]
    env = sh.wrap(INIT, seed=seed_b, seat_id="grok")  # claims grok, signed by gemini
    assert sh.verify_envelope(env, allowlist=_allow(seats), cache=sh.ReplayCache()) is None


@pytest.mark.parametrize("offset", [61, -61, 3600])
def test_handshake_rejects_clock_skew(seats, offset):
    name, seed, _ = seats["grok"]
    t0 = 1_800_000_000
    env = sh.wrap(INIT, seed=seed, seat_id=name, now=t0)
    assert sh.verify_envelope(env, allowlist=_allow(seats), cache=sh.ReplayCache(),
                              now=t0 + offset) is None
    assert sh.verify_envelope(env, allowlist=_allow(seats), cache=sh.ReplayCache(),
                              now=t0 + 59) is not None


def test_handshake_rejects_replay(seats):
    name, seed, _ = seats["grok"]
    env = sh.wrap(INIT, seed=seed, seat_id=name)
    cache = sh.ReplayCache()
    assert sh.verify_envelope(env, allowlist=_allow(seats), cache=cache) is not None
    assert sh.verify_envelope(env, allowlist=_allow(seats), cache=cache) is None


def test_replay_cache_is_bounded():
    c = sh.ReplayCache(max_entries=10, ttl_s=1000)
    for i in range(50):
        c.seen_or_add("s", f"nonce{i:012d}", 1.0)
    assert len(c) <= 10


def test_handshake_rejects_unknown_and_revoked_seat(seats):
    name, seed, _ = seats["grok"]
    env = sh.wrap(INIT, seed=seed, seat_id=name)
    assert sh.verify_envelope(env, allowlist=_allow(seats, omit=("grok",)),
                              cache=sh.ReplayCache()) is None
    assert sh.verify_envelope(env, allowlist=_allow(seats, revoked=("grok",)),
                              cache=sh.ReplayCache()) is None
    assert sh.verify_envelope(env, allowlist={"seats": {}}, cache=sh.ReplayCache()) is None


def test_pure_ed25519_fallback_agrees_with_cryptography(seats):
    _, seed, pub = seats["grok"]
    msg = sh.canonical("initialize", INIT, "grok", 1, "n" * 16)
    sig = sh.sign_bytes(seed, msg)
    pure = sh._pure()
    assert pure.ed25519_public_reference(seed).hex() == pub
    assert pure.ed25519_verify_pure(bytes.fromhex(pub), msg, sig)


def test_mode_defaults_off_and_unknown_fails_closed(monkeypatch):
    monkeypatch.delenv(sh.ENV_MODE, raising=False)
    assert sh.mode() == "off"
    monkeypatch.setenv(sh.ENV_MODE, "maybe")
    assert sh.mode() == "required"


@pytest.fixture
def allow_file(tmp_path, monkeypatch, seats):
    p = tmp_path / "seat_allowlist.json"
    p.write_text(json.dumps(_allow(seats, operators=("nacho",))), encoding="utf-8")
    monkeypatch.setattr(sh, "ALLOWLIST_PATH", p)
    monkeypatch.setattr(sh, "_CACHE", sh.ReplayCache())
    return p


def test_http_mcp_route_verifies_and_drops_silently(allow_file, seats, monkeypatch):
    from mag import mcp_http

    name, seed, _ = seats["gemini"]
    monkeypatch.delenv(sh.ENV_MODE, raising=False)
    st, body = mcp_http._mcp_post({}, json.loads(INIT))  # legacy plain still works when off
    assert st == 200 and body["result"]
    env = sh.wrap(INIT, seed=seed, seat_id=name)
    st, body = mcp_http._mcp_post({}, env)
    assert st == 200 and body["result"]
    assert mcp_http._mcp_post({}, env) == (404, {})  # replay: bare 404, no detail
    bad = sh.wrap(INIT, seed=seeds_other(seats), seat_id=name)
    assert mcp_http._mcp_post({}, bad) == (404, {})
    monkeypatch.setenv(sh.ENV_MODE, "required")
    assert mcp_http._mcp_post({}, json.loads(INIT)) == (404, {})
    st, _ = mcp_http._mcp_post({}, sh.wrap(INIT, seed=seed, seat_id=name))
    assert st == 200


def seeds_other(seats):
    return seats["deepseek"][1]


def _bridge():
    spec = importlib.util.spec_from_file_location(
        "mcp_tcp_bridge_t", ROOT / "scripts" / "container" / "mcp_tcp_bridge.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_tcp_bridge_line_verification(seats):
    b = _bridge()
    al, cache = _allow(seats), sh.ReplayCache()
    name, seed, _ = seats["hermes"] if "hermes" in seats else seats["grok"]
    line = (json.dumps(sh.wrap(INIT, seed=seed, seat_id=name)) + "\n").encode()
    assert b.verify_line(line, "required", al, cache) == INIT.encode() + b"\n"
    assert b.verify_line(line, "required", al, cache) is None          # replay
    plain = (INIT + "\n").encode()
    assert b.verify_line(plain, "required", al, cache) is None          # plain under required
    assert b.verify_line(plain, "optional", al, cache) == plain         # plain under optional
    forged = json.loads(line)
    forged["body"] = INIT.replace("1", "2")
    assert b.verify_line(json.dumps(forged).encode(), "optional", al, cache) is None


@pytest.fixture
def outside_tmp():
    """Key tests need a folder OUTSIDE the repo (pytest tmp lives under agents/)."""
    import shutil
    import tempfile

    d = Path(tempfile.mkdtemp(prefix="mag_seat_test_"))
    yield d
    shutil.rmtree(d, ignore_errors=True)


def test_shim_signed_writer_wraps_every_line(outside_tmp, seats, monkeypatch):
    import io
    import socket as _s

    import mcp_stdio_shim as shim

    out = seat_keygen.keygen("grok", outside_tmp / "k" / "grok.key")
    a, b = _s.socketpair()
    shim._stdin_to_sock_signed(io.BytesIO((INIT + "\n\n").encode()), a, out["key_path"])
    data = b.recv(65536).decode().strip().splitlines()
    assert len(data) == 1
    env = json.loads(data[0])
    al = {"seats": {"grok": {"public_hex": out["public_hex"]}}}
    assert sh.verify_envelope(env, allowlist=al, cache=sh.ReplayCache()) == ("grok", INIT)
    a.close()
    b.close()


def test_keygen_writes_outside_repo_and_prints_only_public(outside_tmp, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("USERPROFILE", str(outside_tmp))
    assert seat_keygen.main(["--seat", "gemini"]) == 0
    key = outside_tmp / ".mag_seat" / "gemini.key"
    rec = json.loads(key.read_text(encoding="utf-8"))
    out = capsys.readouterr()
    assert rec["private_seed_hex"] not in out.out and rec["private_seed_hex"] not in out.err
    row = json.loads(out.out)
    assert row["gemini"]["public_hex"] == rec["public_hex"]
    assert sh.load_key(key) == ("gemini", bytes.fromhex(rec["private_seed_hex"]))
    with pytest.raises(SystemExit):           # never overwrite an existing key
        seat_keygen.keygen("gemini", key)
    with pytest.raises(SystemExit):           # never inside the repo
        seat_keygen.keygen("gemini", tmp_path / "x.key")   # pytest tmp is inside the repo
    assert not (tmp_path / "x.key").exists()


def test_allowlist_config_ships_with_public_keys_only():
    al = json.loads((ROOT / "configs" / "seat_allowlist.json").read_text(encoding="utf-8"))
    assert al["schema"] == "seat_allowlist.v1" and al["quorum"]["default"] == 2
    assert "private" not in json.dumps(al["seats"]).lower()


# ═════════════════════════════ 2. brain manifest + replicate ═════════════════

def _estate(root: Path) -> Path:
    def w(rel, text):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    w("memory/biography/verkle_tip.json", json.dumps({"root": "ab" * 32, "n_leaves": 3}))
    w("memory/biography/verkle_chain.jsonl", '{"i":0}\n{"i":1}\n')
    w("memory/warm_state.json", json.dumps({"chain": {"n_leaves": 3}}))
    w("memory/zknot/LATEST.md", "# zknot\n")
    w("memory/rib_boot.json", json.dumps({
        "ts": "2026-10-17T00:00:00+00:00",
        "core_laws": [{"id": "chain-is-truth", "law": "seen at C:\\Users\\foste\\x and 100.96.161.76"}],
        "vault": {"law_ribs": [{"file": "RIB_X.md", "law_head": "head", "law_amendments": [],
                                "amendment_count": 0}]}}))
    w("watch/LIBRARY/INDEX.md", "# index\n")
    w("watch/LIBRARY/catalog.jsonl", '{"k":1}\n')
    w("watch/LIBRARY/S_CHAIN/LATEST.md", "# shelf\n")
    w("watch/inbox/raw.md", "raw inbox must never ride\n")
    w("memory/biography_v2/tip_v2.json", json.dumps({"root": "cd" * 32, "n": 2, "chain_id": "ef" * 32}))
    w("memory/biography_v2/chain_v2.jsonl", '{"n":1}\n')
    w("memory/biography_v2/checkpoints_v2.jsonl", '{"n":1,"status":"unsigned-pending-operator"}\n')
    w("memory/biography_v2/seed/seed_manifest.v1.json", "{}")
    w("memory/biography_v2/knots_v2/0001__a.knot.json", '{"body":"clean knot"}')
    w("memory/biography_v2/knots_v2/0002__b.knot.json", '{"note":"api_key = ' + FAKE_SK + '"}')
    w("memory/biography_v2/knots_v2/0003__secret_notes.knot.json", '{"body":"named badly"}')
    w("memory/biography_backup/biography_backup_20261016/BACKUP_COMPLETE.json", "{}")
    w("memory/biography_backup/biography_backup_20261016/knots/k1.knot.json", '{"old":1}')
    w("memory/biography_backup/biography_backup_20261017/BACKUP_INCOMPLETE.json", "{}")
    w("memory/biography_backup/biography_backup_20261017/knots/k2.knot.json", '{"half":1}')
    w("scripts/verify_knot_v2.py", "# verifier\nprint('ok')\n")
    return root


def test_manifest_excludes_denylisted_and_secret_files_by_path_only(tmp_path):
    root = _estate(tmp_path / "estate")
    m, raw, sha = bm.build(root)
    paths = {f["path"] for f in m["files"]}
    assert "memory/biography_v2/knots_v2/0001__a.knot.json" in paths
    assert set(m["excluded"]) == {"memory/biography_v2/knots_v2/0002__b.knot.json",
                                  "memory/biography_v2/knots_v2/0003__secret_notes.knot.json"}
    assert FAKE_SK not in raw.decode() and "api_key" not in raw.decode()
    assert not any(p.startswith("watch/inbox") for p in paths)
    # latest COMPLETE backup only (backup_chain rule): 20261016, not the incomplete 20261017
    assert any("biography_backup_20261016" in p for p in paths)
    assert not any("biography_backup_20261017" in p for p in paths)
    assert m["v2"]["root"] == "cd" * 32 and sha == hashlib.sha256(raw).hexdigest()
    for f in m["files"]:
        assert hashlib.sha256((root / f["path"]).read_bytes()).hexdigest() == f["sha256"]


def _cfg(vault, *extra):
    return {"targets": [{"name": "local_vault", "kind": "vault", "path": str(vault)}, *extra]}


def test_replicate_is_append_only_and_never_deletes(tmp_path):
    root = _estate(tmp_path / "estate")
    vault, rec = tmp_path / "vault", tmp_path / "receipts"
    stray = vault / "objects" / "zz" / "not_in_any_manifest"
    stray.parent.mkdir(parents=True)
    stray.write_bytes(b"pre-existing target file")
    r1 = br.replicate(config=_cfg(vault), root=root, receipts=rec)
    assert r1["verify_all_pass"] and r1["files"] > 5
    zk = root / "memory" / "zknot" / "LATEST.md"
    old_obj = br.object_path(vault, hashlib.sha256(zk.read_bytes()).hexdigest())
    zk.write_text("# zknot v2\n", encoding="utf-8")
    time.sleep(1.1)
    r2 = br.replicate(config=_cfg(vault), root=root, receipts=rec)
    assert r2["manifest_sha256"] != r1["manifest_sha256"]
    assert stray.read_bytes() == b"pre-existing target file"      # untouched
    assert old_obj.is_file()                                        # old version kept
    assert len(list((vault / "manifests").glob("*.json"))) == 2     # manifests accumulate
    rcpt = json.loads(Path(r2["receipt_path"]).read_text(encoding="utf-8"))
    for k in ("targets", "files", "bytes", "manifest_sha256", "verify_all_pass"):
        assert k in rcpt


def test_copy_commands_carry_no_delete_verbs():
    for cmd in (br.robocopy_cmd(Path("C:/v"), "D:/t"), br.rclone_copy_cmd("rclone", Path("v"), "magbrain:"),
                br.rclone_cryptcheck_cmd("rclone", Path("v"), "magbrain:")):
        assert not {t.lower() for t in cmd[1:]} & br.FORBIDDEN
    for bad in (["robocopy", "a", "b", "/MIR"], ["robocopy", "a", "b", "/PURGE"],
                ["rclone", "sync", "a", "b:"], ["rclone", "delete", "b:"],
                ["rclone", "copy", "a", "b:", "--delete-after"]):
        with pytest.raises(RuntimeError):
            br.guard(bad)


@pytest.mark.skipif(os.name != "nt", reason="robocopy is Windows-only")
def test_smb_push_keeps_target_extras_and_verify_catches_corruption(tmp_path, monkeypatch):
    root = _estate(tmp_path / "estate")
    vault, dst = tmp_path / "vault", tmp_path / "bob_share"
    dst.mkdir()
    (dst / "bob_owned.txt").write_text("bob's own file", encoding="utf-8")
    monkeypatch.setattr(br, "tcp_probe", lambda *a, **k: True)
    t = {"name": "bob", "kind": "smb", "host": "127.0.0.1", "path": str(dst)}
    r = br.replicate(config=_cfg(vault, t), root=root, receipts=tmp_path / "rc")
    bob = next(x for x in r["targets"] if x["name"] == "bob")
    assert bob["status"] == "ok" and bob["verify"]["pass"], bob
    assert (dst / "bob_owned.txt").read_text(encoding="utf-8") == "bob's own file"
    m, _, msha = bm.build(root)
    victim = br.object_path(dst, m["files"][0]["sha256"])
    victim.write_bytes(b"bit rot")
    v = br.verify_tree(dst, m, msha)
    assert not v["pass"] and v["n_corrupt"] == 1


def test_vault_verify_catches_corrupt_and_missing(tmp_path):
    root = _estate(tmp_path / "estate")
    vault = tmp_path / "vault"
    m, raw, sha, _ = br.vault_run(vault, root)
    br.store_manifest(vault, raw, sha, "20261017T000000Z")
    assert br.verify_tree(vault, m, sha)["pass"]
    shas = sorted({f["sha256"] for f in m["files"]})
    br.object_path(vault, shas[0]).write_bytes(b"corrupt")
    br.object_path(vault, shas[1]).unlink()
    v = br.verify_tree(vault, m, sha)
    assert not v["pass"] and v["n_corrupt"] == 1 and v["n_missing"] == 1


def test_offline_bob_and_unconfigured_drive_skip_cleanly(tmp_path, monkeypatch):
    root = _estate(tmp_path / "estate")
    monkeypatch.setattr(br, "tcp_probe", lambda *a, **k: False)
    monkeypatch.setattr(br, "rclone_bin", lambda: "rclone")
    monkeypatch.setattr(br, "rclone_remotes", lambda _r: set())
    cfg = _cfg(tmp_path / "vault",
               {"name": "bob", "kind": "smb", "host": "100.125.103.60", "path": r"\\x\y"},
               {"name": "drive_private", "kind": "rclone_crypt", "remote": "magbrain:"})
    r = br.replicate(config=cfg, root=root, receipts=tmp_path / "rc")
    st = {x["name"]: x for x in r["targets"]}
    assert st["bob"]["status"] == "skipped" and "unreachable" in st["bob"]["reason"]
    assert st["drive_private"]["status"] == "skipped" and "not configured" in st["drive_private"]["reason"]
    assert r["verify_all_pass"]


def test_restore_rebuilds_tree_from_vault(tmp_path):
    root = _estate(tmp_path / "estate")
    vault = tmp_path / "vault"
    m, raw, sha, _ = br.vault_run(vault, root)
    mp = br.store_manifest(vault, raw, sha, "20261017T000000Z")
    out = br.restore(mp, tmp_path / "restored", vault)
    assert out["corrupt"] == 0
    for f in m["files"]:
        assert (tmp_path / "restored" / f["path"]).read_bytes() == (root / f["path"]).read_bytes()


def test_targets_yaml_has_three_private_tiers_and_public():
    cfg = br.load_config()
    kinds = {t["kind"] for t in cfg["targets"]}
    assert kinds == {"vault", "smb", "rclone_crypt"}
    assert cfg["public"]["remote"] == "magpublic:" and cfg["public"]["auto_push"] is False


# ═════════════════════════════ 3. public lattice (one-way) ═══════════════════

@pytest.fixture
def staged(tmp_path):
    root = _estate(tmp_path / "estate")
    vault = tmp_path / "vault"
    m, raw, sha, _ = br.vault_run(vault, root)
    br.store_manifest(vault, raw, sha, "20261017T000000Z")
    out = plm.build(vault, tmp_path / "staging", review_copy=tmp_path / "REVIEW.md")
    return {"root": root, "vault": vault, "out": out, "tmp": tmp_path}


def test_public_build_is_strict_allowlist_and_masked(staged):
    payload = Path(staged["out"]["staging"]) / "payload"
    files = {p.relative_to(payload).as_posix() for p in payload.rglob("*") if p.is_file()}
    assert files == {"law_cards.json", "chain_v2/tip_v2.json", "chain_v2/checkpoints_v2.jsonl",
                     "verify/verify_knot_v2.py", plm.MANIFEST_NAME}
    blob = "".join((payload / f).read_text(encoding="utf-8") for f in files)
    assert "foste" not in blob and "100.96.161.76" not in blob and FAKE_SK not in blob
    assert "<home>" in blob and ("<tailnet-ip>" in blob or "<ip>" in blob)
    review = (staged["tmp"] / "REVIEW.md").read_text(encoding="utf-8")
    for f in files - {plm.MANIFEST_NAME}:
        assert f"`{f}`" in review
    assert staged["out"]["manifest_sha256"] in review
    # code is published verbatim (masking would corrupt it)
    assert (payload / "verify" / "verify_knot_v2.py").read_bytes() == \
        (staged["root"] / "scripts" / "verify_knot_v2.py").read_bytes()


def test_public_verifier_with_host_detail_is_excluded_not_mangled(tmp_path):
    root = _estate(tmp_path / "estate")
    (root / "scripts" / "verify_knot_v2.py").write_text(
        "def f(secret: bytes):\n    return 'C:\\\\Users\\\\foste\\\\x'\n", encoding="utf-8")
    vault = tmp_path / "vault"
    m, raw, sha, _ = br.vault_run(vault, root)
    br.store_manifest(vault, raw, sha, "20261017T000000Z")
    out = plm.build(vault, tmp_path / "staging")
    assert "verify/verify_knot_v2.py" in out["excluded"]
    assert not (Path(out["staging"]) / "payload" / "verify" / "verify_knot_v2.py").exists()


def test_public_push_requires_matching_approval(staged, monkeypatch):
    cfg = {"public": {"remote": "magpublic:", "dest": "lattice"}}
    sroot = staged["tmp"] / "staging"
    sha = staged["out"]["manifest_sha256"]
    for bad in (None, "", "0" * 64, sha[:-1] + ("0" if sha[-1] != "0" else "1")):
        with pytest.raises(SystemExit):
            plm.push(cfg, bad, staging_root=sroot, receipts=staged["tmp"] / "rc")
    # tampering after review breaks the approval
    lc = Path(staged["out"]["staging"]) / "payload" / "law_cards.json"
    orig = lc.read_bytes()
    lc.write_bytes(orig + b" ")
    with pytest.raises(SystemExit):
        plm.push(cfg, sha, staging_root=sroot, receipts=staged["tmp"] / "rc")
    lc.write_bytes(orig)
    extra = Path(staged["out"]["staging"]) / "payload" / "sneak.txt"
    extra.write_text("x", encoding="utf-8")
    with pytest.raises(SystemExit):
        plm.push(cfg, sha, staging_root=sroot, receipts=staged["tmp"] / "rc")
    extra.unlink()


def _snapshot(*dirs):
    out = {}
    for d in dirs:
        for p in Path(d).rglob("*"):
            if p.is_file():
                out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def test_public_path_has_no_read_into_brain_path(staged, monkeypatch):
    """The public tier only ever WRITES to public and compares hashes; nothing comes back."""
    cfg = {"public": {"remote": "magpublic:", "dest": "lattice"}}
    sha = staged["out"]["manifest_sha256"]
    calls = []

    def runner(cmd, timeout):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 0, stdout="UNTRUSTED PUBLIC OUTPUT", stderr="")

    monkeypatch.setattr(br, "rclone_bin", lambda: "rclone")
    monkeypatch.setattr(br, "rclone_remotes", lambda _r: {"magpublic:"})
    before = _snapshot(staged["root"], staged["vault"])
    res = plm.push(cfg, sha, staging_root=staged["tmp"] / "staging",
                   receipts=staged["tmp"] / "rc", runner=runner)
    assert res["status"] == "ok" and res["verify"]["pass"]
    assert _snapshot(staged["root"], staged["vault"]) == before      # brain untouched
    assert "UNTRUSTED" not in Path(res["receipt_path"]).read_text(encoding="utf-8")
    assert [c[1] for c in calls] == ["copy", "check"]
    payload = str(Path(staged["out"]["staging"]) / "payload")
    for c in calls:
        assert c[2] == payload                                       # local source
        assert c[3] == f"magpublic:lattice/{sha}"                    # public is dest only
    assert "--ignore-existing" in calls[0] and "--one-way" in calls[1]
    assert "--download" not in calls[1]
    # static: the module names no read-back verb and no remote as a source
    src = (ROOT / "scripts" / "public_lattice_manifest.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    strings = {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    for verb in ("cat", "copyto", "lsjson", "lsf", "ls", "lsl", "md5sum", "sha1sum", "hashsum",
                 "mount", "serve", "sync", "bisync", "move", "moveto", "--download", "cryptdecode"):
        assert verb not in strings, verb
    assert "subprocess" not in {a.name for n in ast.walk(tree) if isinstance(n, ast.Import)
                                for a in n.names}


# ═════════════════════════════ 4. seat proposals ═════════════════════════════

@pytest.fixture
def props(tmp_path, monkeypatch, seats):
    al = _allow(seats, operators=("nacho",))
    root = tmp_path / "proposals"
    monkeypatch.setattr(P, "PROPOSALS_DIR", root)
    keys = {}
    for n, (_, seed, _) in seats.items():
        keys[n] = seed
    return {"al": al, "root": root, "keys": keys}


def _msg(props, kind, seat, payload):
    return P.sign_message(kind, payload, seed=props["keys"][seat], seat_id=seat)


def _propose(props, seat="grok"):
    m = _msg(props, "proposal", seat, {"title": "tighten verify", "targets": ["mag/x.py"],
                                       "diff": "--- a\n+++ b\n@@\n-x\n+y\n", "rationale": "r"})
    return P.submit(m, root=props["root"], allowlist=props["al"])["proposal_id"]


def _review(props, pid, seat, verdict):
    return P.submit(_msg(props, "review", seat, {"proposal_id": pid, "verdict": verdict,
                                                 "reason": "because"}),
                    root=props["root"], allowlist=props["al"])


def test_proposal_signature_checked(props):
    m = _msg(props, "proposal", "grok", {"title": "t", "targets": ["a.py"], "diff": "d", "rationale": ""})
    m["payload"]["title"] = "swapped after signing"
    with pytest.raises(ValueError):
        P.submit(m, root=props["root"], allowlist=props["al"])
    m2 = _msg(props, "proposal", "grok", {"title": "t", "targets": ["a.py"], "diff": "d", "rationale": ""})
    m2["payload"]["seat"] = "gemini"  # impersonation
    with pytest.raises(ValueError):
        P.submit(m2, root=props["root"], allowlist=props["al"])
    stranger = sh.generate_seed()
    m3 = P.sign_message("proposal", {"title": "t", "targets": ["a.py"], "diff": "d"},
                        seed=stranger, seat_id="stranger")
    with pytest.raises(ValueError):
        P.submit(m3, root=props["root"], allowlist=props["al"])
    assert not props["root"].exists() or not any(props["root"].iterdir())


def test_quorum_needs_two_distinct_non_author_seats(props):
    pid = _propose(props)
    _review(props, pid, "grok", "approve")            # author self-approval does not count
    assert not P.tally(pid, root=props["root"], allowlist=props["al"])["ready"]
    _review(props, pid, "gemini", "approve")
    _review(props, pid, "gemini", "approve")          # duplicate seat vote counts once
    t = P.tally(pid, root=props["root"], allowlist=props["al"])
    assert t["approvers"] == ["gemini"] and not t["ready"]
    promo = _msg(props, "promotion", "gemini", {"proposal_id": pid, "state": "ready"})
    with pytest.raises(ValueError):
        P.submit(promo, root=props["root"], allowlist=props["al"])
    _review(props, pid, "deepseek", "approve")
    t = P.tally(pid, root=props["root"], allowlist=props["al"])
    assert t["ready"] and t["approvers"] == ["deepseek", "gemini"]
    P.submit(_msg(props, "promotion", "deepseek", {"proposal_id": pid, "state": "ready"}),
             root=props["root"], allowlist=props["al"])
    assert P.tally(pid, root=props["root"], allowlist=props["al"])["promoted"]


def test_duplicate_seat_latest_vote_wins(props):
    pid = _propose(props)
    _review(props, pid, "gemini", "approve")
    time.sleep(0.01)
    _review(props, pid, "gemini", "reject")
    t = P.tally(pid, root=props["root"], allowlist=props["al"])
    assert t["approvers"] == [] and t["rejecters"] == ["gemini"] and t["distinct_votes"] == 1


def test_operator_override_and_operator_veto(props):
    pid = _propose(props)
    _review(props, pid, "nacho", "approve")
    t = P.tally(pid, root=props["root"], allowlist=props["al"])
    assert t["ready"] and t["operator_override"]
    pid2 = _propose(props, "gemini")
    for s in ("grok", "deepseek"):
        _review(props, pid2, s, "approve")
    _review(props, pid2, "nacho", "reject")
    assert not P.tally(pid2, root=props["root"], allowlist=props["al"])["ready"]


def test_replayed_review_and_revoked_votes(props, seats):
    pid = _propose(props)
    m = _msg(props, "review", "gemini", {"proposal_id": pid, "verdict": "approve"})
    P.submit(m, root=props["root"], allowlist=props["al"])
    with pytest.raises(ValueError):
        P.submit(m, root=props["root"], allowlist=props["al"])
    _review(props, pid, "deepseek", "approve")
    assert P.tally(pid, root=props["root"], allowlist=props["al"])["ready"]
    revoked = _allow(seats, operators=("nacho",), revoked=("deepseek",))
    t = P.tally(pid, root=props["root"], allowlist=revoked)
    assert not t["ready"] and t["invalid_messages"]


def test_proposal_path_confinement(props):
    for bad in ("../escape", "p_20261017T000000Z_../../x", "..", "/abs", "p_x"):
        with pytest.raises(ValueError):
            P._pdir(bad, props["root"])
    for targets in (["../outside.py"], ["/etc/passwd"], ["C:/Windows/x"], [".env"],
                    ["secret_gate_results/a"], ["memory/trajectory/steps.jsonl"]):
        with pytest.raises(ValueError):
            _msg(props, "proposal", "grok", {"title": "t", "targets": targets, "diff": "d"})
    with pytest.raises(ValueError):
        _msg(props, "proposal", "grok", {"title": "t", "targets": ["a.py"], "patch_path": "../p.diff"})
    with pytest.raises(ValueError):
        _msg(props, "proposal", "grok", {"title": "t", "targets": ["a.py"],
                                         "diff": "+key = " + FAKE_SK})
    with pytest.raises(ValueError):
        _msg(props, "review", "grok", {"proposal_id": "../../x", "verdict": "approve"})
    pid = _propose(props)
    _review(props, pid, "gemini", "approve")
    root = props["root"].resolve()
    for p in props["root"].rglob("*"):
        assert root in p.resolve().parents


def test_proposal_files_never_overwritten(props):
    pid = _propose(props)
    pj = props["root"] / pid / "proposal.json"
    before = pj.read_bytes()
    with pytest.raises(ValueError):  # same signed payload -> same id -> refused
        m = json.loads(before)
        P.submit(m, root=props["root"], allowlist=props["al"])
    assert pj.read_bytes() == before


def test_warm_mcp_proposal_tools(props, tmp_path, monkeypatch, seats):
    from mag import mcp_server as ms

    al_path = tmp_path / "allow.json"
    al_path.write_text(json.dumps(props["al"]), encoding="utf-8")
    monkeypatch.setattr(sh, "ALLOWLIST_PATH", al_path)
    names = {t["name"] for t in ms.tools_manifest("warm")}
    assert {"estate_propose", "estate_review", "estate_proposals"} <= names
    rec = sh.key_record("gemini", props["keys"]["gemini"])
    kp = tmp_path / "gemini.key"
    kp.write_text(json.dumps(rec), encoding="utf-8")
    monkeypatch.setenv(sh.ENV_KEY_PATH, str(kp))

    def call(name, args):
        out = ms.call_tool(name, args, set(ms._profile_names("warm")))
        return out, json.loads(out["content"][0]["text"])

    out, body = call("estate_propose", {"title": "x", "targets": ["mag/a.py"], "diff": "d",
                                        "rationale": "why"})
    assert not out.get("isError"), body
    pid = body.get("proposal_id") or body.get("result", {}).get("proposal_id")
    assert pid and (props["root"] / pid / "proposal.json").is_file()
    out, body = call("estate_proposals", {"action": "list"})
    assert not out.get("isError") and pid in json.dumps(body)
    signed = _msg(props, "review", "grok", {"proposal_id": pid, "verdict": "approve"})
    out, body = call("estate_review", {"signed": signed})
    assert not out.get("isError"), body
    monkeypatch.delenv(sh.ENV_KEY_PATH)
    out, body = call("estate_propose", {"title": "y", "targets": ["a.py"], "diff": "d"})
    assert out.get("isError")
