"""tests/test_bintree_v2.py - Mag v2 binary-tree chain (BINTREE_V2_SEED_SPEC, 2026-10-17).

Port of the box spike's 25 tests + the repo glue (freeze / catchup / shadow / checkpoints /
standalone verifier) + RFC 8032 Ed25519 vectors. Every write goes to tmp_path: the live
memory/biography and memory/biography_v2 are fenced by conftest and never touched.
"""
from __future__ import annotations

import copy
import hashlib
import importlib
import json
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from mag import bintree_v2 as bt  # noqa: E402
import verify_knot_v2 as vkv  # noqa: E402

VERIFIER = ROOT / "scripts" / "verify_knot_v2.py"
FREEZE = ROOT / "scripts" / "freeze_v1_seed.py"
CATCHUP = ROOT / "scripts" / "catchup_v2.py"


@pytest.fixture(autouse=True)
def _no_v2_env(monkeypatch):
    for k in ("MAG_CHAIN_V2_SHADOW", "MAG_CHAIN_V2_SIGNING", "MAG_CHAIN_V2_PUBLISH",
              "MAG_BINTREE_V2_DIR", "MAG_BINTREE_V1_BIO"):
        monkeypatch.delenv(k, raising=False)
    bt._CACHE.clear()
    yield
    bt._CACHE.clear()


def rand_tree(profile="mag", n=200, seed=1):
    rnd = random.Random(seed)
    t, kv = bt.BinaryTree(profile), {}
    for _ in range(n):
        k = bytes(rnd.getrandbits(8) for _ in range(31)) + bytes([rnd.randrange(256)])
        v = bytes(rnd.getrandbits(8) for _ in range(32))
        t.insert(k, v)
        kv[k] = v
    return t, kv


def small_chain(n_rows=300, seed=7):
    rnd = random.Random(seed)
    ch = bt.Chain("mag")
    ch.genesis("ab" * 32, 12016, b"\x01" * 32, b"\x02" * 32, "cd" * 32, b"\x03" * 32, b"\x04" * 32, b"\x05" * 32)
    for i in range(n_rows):
        sid = f"s{rnd.randrange(max(1, n_rows // 3))}"
        ch.append("knot", {1: hashlib.sha256(f"leaf{i}".encode()).digest(), 7: b"\x07" * 32}, sid, ts_ms=i)
    return ch


def _ref(hashfn):
    import _bintree_v2_ref_eip7864 as ref_mod  # vendored EIP-7864 reference (tests/ is on sys.path)
    ref = importlib.reload(ref_mod)
    if hashfn == "sha256":
        ref.blake3 = lambda d: hashlib.sha256(d)
    elif ref.blake3 is None:
        pytest.skip("blake3 not installed (not added to .venv)")
    return ref


# ============================================================ 1. structure (spike tests 1-6)
def test_root_independent_of_insert_order():
    t, kv = rand_tree(n=300)
    items = list(kv.items())
    random.Random(3).shuffle(items)
    t2 = bt.BinaryTree()
    for k, v in items:
        t2.insert(k, v)
    assert t.root_hash() == t2.root_hash()


def test_get():
    t, kv = rand_tree(n=100)
    for k, v in kv.items():
        assert t.get(k) == v


def test_empty_and_single():
    assert bt.BinaryTree().root_hash() == bt.ZERO
    t = bt.BinaryTree()
    t.insert(b"\x01" * 32, b"\x02" * 32)
    assert t.root_hash() != bt.ZERO


def test_zero_value_differs_from_empty():
    a = bt.BinaryTree()
    a.insert(b"\x01" * 31 + b"\x00", b"\x09" * 32)
    b = copy.deepcopy(a)
    b.insert(b"\x01" * 31 + b"\x05", bt.ZERO)
    assert a.root_hash() != b.root_hash()


def test_matches_eip7864_python_reference_blake3():
    ref = _ref(None)
    for seed in range(5):
        t, kv = rand_tree("eip-blake3", n=60, seed=seed)
        r = ref.BinaryTree()
        for k, v in kv.items():
            r.insert(k, v)
        assert t.root_hash() == r.merkelize(), seed


def test_matches_eip7864_python_reference_with_sha256():
    ref = _ref("sha256")
    t, kv = rand_tree("eip-sha256", n=80, seed=11)
    r = ref.BinaryTree()
    for k, v in kv.items():
        r.insert(k, v)
    assert t.root_hash() == r.merkelize()


# ============================================================ 2. proofs (spike tests 7-12)
@pytest.fixture(scope="module")
def ptree():
    t, kv = rand_tree(n=400, seed=5)
    return t, kv, t.root_hash(), list(kv)


def test_random_inclusion(ptree):
    t, kv, root, keys = ptree
    rnd = random.Random(9)
    for _ in range(30):
        k = rnd.choice(keys)
        assert bt.verify(root, t.prove([k]))[k] == kv[k]


def test_multiproof(ptree):
    t, kv, root, keys = ptree
    ks = random.Random(2).sample(keys, 40)
    assert bt.verify(root, t.prove(ks)) == {k: kv[k] for k in ks}


def test_nonmembership_all_terminal_kinds(ptree):
    t, kv, root, keys = ptree
    k0 = keys[0]
    for k in [k0[:31] + bytes([(k0[31] + 1) % 256]), b"\xff" * 32, bytes(32), k0[:20] + b"\x00" * 12]:
        if k in kv:
            continue
        assert bt.verify(root, t.prove([], [k]))[k] is None


def test_prover_refuses_wrong_claims(ptree):
    t, kv, root, keys = ptree
    with pytest.raises(KeyError):
        t.prove([], [keys[0]])
    with pytest.raises(KeyError):
        t.prove([b"\xee" * 32])


def test_tamper_fails(ptree):
    t, kv, root, keys = ptree
    p = t.prove([keys[3]])
    bad = bytearray(root)
    bad[1] ^= 1
    with pytest.raises(bt.ProofError):
        bt.verify(bytes(bad), p)
    q = copy.deepcopy(p)
    term = next(x for x in q["terminals"] if x["kind"] == "stem")
    s = next(iter(term["values"]))
    v = bytearray(bytes.fromhex(term["values"][s]))
    v[-1] ^= 1
    term["values"][s] = v.hex()
    with pytest.raises(bt.ProofError):
        bt.verify(root, q)
    q = copy.deepcopy(p)
    q["witness"].append("0")
    with pytest.raises(bt.ProofError):
        bt.verify(root, q)
    q = copy.deepcopy(p)
    q["witness"] = q["witness"][:-1]
    with pytest.raises(bt.ProofError):
        bt.verify(root, q)


def test_absent_claim_for_present_key_cannot_be_built_by_editing(ptree):
    t, kv, root, keys = ptree
    q = copy.deepcopy(t.prove([keys[4]]))
    term = next(x for x in q["terminals"] if x["kind"] == "stem")
    term["values"] = {s: None for s in term["values"]}
    with pytest.raises(bt.ProofError):
        bt.verify(root, q)


# ============================================================ 3. domain separation (spike 13-14)
def _grind(profile):
    for seed in range(5000):
        t, kv = rand_tree(profile, n=12, seed=1000 + seed)
        if isinstance(t.root, bt.InternalNode) and t.node_hash(t.root.left)[31] == 0:
            return t, kv
    pytest.fail("no grind hit")


def _forge(t, k):
    L, R = t.node_hash(t.root.left), t.node_hash(t.root.right)
    return {"keys": [k.hex()], "terminals": [{"depth": 0, "kind": "foreign", "stem": L[:31].hex(),
                                              "subroot": R.hex()}], "witness": [], "profile": t.hs.profile}


def test_eip_untagged_nonmembership_forgery():
    t, kv = _grind("eip-sha256")
    k = next(iter(kv))
    assert bt.verify(t.root_hash(), _forge(t, k), "eip-sha256")[k] is None  # forged
    assert t.get(k) is not None


def test_mag_tagged_profile_resists():
    t, kv = _grind("mag")
    k = next(iter(kv))
    with pytest.raises(bt.ProofError):
        bt.verify(t.root_hash(), _forge(t, k), "mag")


# ============================================================ 4. chain (spike 15-23)
@pytest.fixture(scope="module")
def chain300():
    return small_chain(300)


def test_rebuild_root(chain300):
    again = small_chain(300)
    assert again.root() == chain300.root()
    replayed = bt.Chain()
    replayed.replay(copy.deepcopy(chain300.rows), verify_each=True)
    assert replayed.root() == chain300.root()


def test_row_proof_with_length(chain300):
    ch, root = chain300, chain300.root()
    for i in random.Random(4).sample(range(ch.n), 25):
        res = bt.verify(root, ch.prove_row(i))
        assert int.from_bytes(res[bt.key(bt.META_STEM, 0)], "big") == ch.n
        assert res[bt.key(bt.row_stem(ch.n), 0)] is None
        assert int.from_bytes(res[bt.key(bt.row_stem(i), 0)][8:16], "big") == i


def test_prev_root_links(chain300):
    for i in range(1, 50):
        assert chain300.rows[i]["kv"]["3"] == chain300.rows[i - 1]["root_after"]


def test_insert_once():
    ch = small_chain(5)
    ch.n -= 1
    with pytest.raises(RuntimeError):
        ch.append("knot", {1: b"\x01" * 32}, "x")


def test_amend_is_append_only():
    ch = small_chain(20)
    old_root, old_state = ch.root(), ch.rows[20]["state_after"]
    sid = ch.rows[5]["session_id"]
    before = {k: ch.tree.get(k) for k in ch.row_keys(5)}
    ch.append("amend", {1: b"\x0a" * 32, 4: bt.u64v(5)}, sid)
    assert {k: ch.tree.get(k) for k in ch.row_keys(5)} == before
    assert ch.tree.get(bt.key(bt.session_stem(sid), 0)) == bt.u64v(ch.n - 1)
    bt.verify(ch.root(), ch.prove_row(5))
    cp = bt.prove_consistency(ch.tree, 21, ch.n, bytes.fromhex(old_state))
    assert bt.verify_consistency(old_root, ch.root(), cp)


def test_genesis_anchors_seed(chain300):
    ch = chain300
    res = bt.verify(ch.root(), ch.tree.prove([bt.key(bt.row_stem(0), s) for s in (0, 64, 65, 66, 70)]))
    assert res[bt.key(bt.row_stem(0), 64)] == bytes.fromhex("ab" * 32)
    assert int.from_bytes(res[bt.key(bt.row_stem(0), 65)], "big") == 12016
    assert res[bt.key(bt.row_stem(0), 66)] == b"\x01" * 32
    assert res[bt.key(bt.row_stem(0), 0)][1] == bt.KIND["genesis"]


def test_consistency_random_pairs(chain300):
    ch, rnd = chain300, random.Random(8)
    for _ in range(40):
        a = rnd.randrange(1, ch.n + 1)
        b = rnd.randrange(a, ch.n + 1)
        ra, rb = ch.rows[a - 1], ch.rows[b - 1]
        cp = bt.prove_consistency(ch.tree, a, b, bytes.fromhex(ra["state_after"]), bytes.fromhex(rb["state_after"]))
        assert bt.verify_consistency(bytes.fromhex(ra["root_after"]), bytes.fromhex(rb["root_after"]), cp)
        assert vkv.verify_consistency(bytes.fromhex(ra["root_after"]), bytes.fromhex(rb["root_after"]), cp)


def test_consistency_rejects_rewritten_history():
    ch = small_chain(64)
    a = 40
    old_root, old_state = bytes.fromhex(ch.rows[a - 1]["root_after"]), bytes.fromhex(ch.rows[a - 1]["state_after"])
    ch.tree.insert(bt.key(bt.row_stem(10), 1), b"\x66" * 32)  # forbidden history rewrite
    cp = bt.prove_consistency(ch.tree, a, ch.n, old_state)
    with pytest.raises(bt.ProofError):
        bt.verify_consistency(old_root, ch.root(), cp)


def test_consistency_rejects_wrong_sizes(chain300):
    ch = chain300
    cp = bt.prove_consistency(ch.tree, 100, ch.n, bytes.fromhex(ch.rows[99]["state_after"]))
    cp["n_old"] = 101
    with pytest.raises(bt.ProofError):
        bt.verify_consistency(bytes.fromhex(ch.rows[99]["root_after"]), ch.root(), cp)


# ============================================================ 5. standalone verifier (spike 24-25)
def _run_verifier(d: Path, *args):
    return subprocess.run([sys.executable, "verify_knot_v2.py", *args], cwd=d, capture_output=True, text=True)


def test_verify_knot_stateless_subprocess(tmp_path):
    ch = small_chain(120)
    root, i = ch.root(), 77
    shutil.copy(VERIFIER, tmp_path)  # ONE file, nothing else
    pf = tmp_path / "p.json"
    pf.write_text(json.dumps({"schema": "mag_bintree_proof.v2", "root": root.hex(), "index": i,
                              "n": ch.n, "proof": ch.prove_row(i)}))
    ok = _run_verifier(tmp_path, "p.json", "--root", root.hex())
    assert ok.returncode == 0, ok.stdout + ok.stderr
    bad = bytearray(root)
    bad[0] ^= 1
    assert _run_verifier(tmp_path, "p.json", "--root", bytes(bad).hex()).returncode == 1
    assert {p.name for p in tmp_path.iterdir()} - {"__pycache__"} == {"verify_knot_v2.py", "p.json"}


def test_v1_row_binding_and_forgery(tmp_path):
    rows = [{"ts": f"2026-10-01T00:00:{j:02d}Z", "filename": f"k{j}.knot.json",
             "leaf_hash": hashlib.sha256(f"l{j}".encode()).hexdigest(), "session_id": f"s{j}",
             "tension_index": 0.1 * j, "index": j, "verkle_root": "ff" * 32} for j in range(40)]
    ch = bt.Chain()
    ch.genesis("ab" * 32, 40, b"\x01" * 32, b"\x02" * 32, rows[-1]["leaf_hash"], bt.ZERO, b"\x04" * 32, b"\x05" * 32)
    for j, r in enumerate(rows):
        ch.append_v1(r, j, seed=True)
    shutil.copy(VERIFIER, tmp_path)
    i = 13
    (tmp_path / "p.json").write_text(json.dumps({"schema": "mag_bintree_proof.v2", "root": ch.root().hex(),
                                                 "index": i, "n": ch.n, "proof": ch.prove_row(i)}))
    row = dict(rows[i - 1], verkle_root="00" * 32, index=999)  # volatile fields do not matter
    (tmp_path / "row.json").write_text(json.dumps(row))
    assert _run_verifier(tmp_path, "p.json", "--root", ch.root().hex(), "--v1-row", "row.json").returncode == 0
    row["tension_index"] = 0.999
    (tmp_path / "row.json").write_text(json.dumps(row))
    assert _run_verifier(tmp_path, "p.json", "--root", ch.root().hex(), "--v1-row", "row.json").returncode == 1


# ============================================================ 6. Ed25519 (RFC 8032) + seal
def test_rfc8032_vectors_pure_python():
    assert vkv.selftest()
    for sk, pk, msg, sig in vkv.RFC8032_VECTORS:
        pk, msg, sig = bytes.fromhex(pk), bytes.fromhex(msg), bytes.fromhex(sig)
        assert vkv.ed25519_verify_pure(pk, msg, sig)
        assert vkv.ed25519_verify(pk, msg, sig, backend="pure")


def test_ed25519_rejects_malleable_s_and_bad_points():
    sk, pk, msg, sig = (bytes.fromhex(x) for x in vkv.RFC8032_VECTORS[1])
    s = int.from_bytes(sig[32:], "little") + vkv._L  # s + L: same group element, must be rejected
    assert not vkv.ed25519_verify_pure(pk, msg, sig[:32] + s.to_bytes(32, "little"))
    assert not vkv.ed25519_verify_pure(b"\xff" * 32, msg, sig)
    assert not vkv.ed25519_verify_pure(pk[:31], msg, sig)


def test_pure_and_cryptography_agree_on_random_keys():
    crypto = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    from cryptography.hazmat.primitives import serialization
    rnd = random.Random(42)
    for j in range(5):
        k = crypto.Ed25519PrivateKey.from_private_bytes(bytes(rnd.getrandbits(8) for _ in range(32)))
        pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        msg = f"mag v2 {j}".encode()
        sig = k.sign(msg)
        assert vkv.ed25519_verify_pure(pub, msg, sig)
        assert vkv.ed25519_verify(pub, msg, sig, backend="cryptography")
        assert not vkv.ed25519_verify_pure(pub, msg + b"!", sig)


def test_restore_seal_public_signature_verifies_pure_python():
    """The published Oct 15 seal (PUBLIC key + signature only) verifies with the pure fallback."""
    seal_p = ROOT / "watch" / "inbox" / "CHAIN_RESTORE_20261015.seal"
    if not seal_p.is_file():
        pytest.skip("restore seal not present")
    seal = json.loads(seal_p.read_text(encoding="utf-8"))
    pub, sig = vkv.decode_bytes(seal["public_key"]), vkv.decode_bytes(seal["signature"])  # seed_seal: base64
    assert len(pub) == 32 and len(sig) == 64
    assert vkv.key_id_for(pub) == seal["key_id"] == bt.PINNED_SEAL_KEY_ID
    assert vkv.ed25519_verify_pure(pub, seal["seed_root"].encode("utf-8"), sig)
    assert not vkv.ed25519_verify_pure(pub, (seal["seed_root"][:-1] + "0").encode("utf-8"), sig) \
        or seal["seed_root"].endswith("0")


def test_signed_checkpoint_roundtrip_with_test_key(tmp_path):
    """Checkpoint signature format, verified by the standalone verifier (test key, pinned id swapped)."""
    crypto = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    from cryptography.hazmat.primitives import serialization
    st = bt.Store(tmp_path / "v2", tmp_path / "v1")
    ch = small_chain(30)
    st.append_entries(ch.rows)
    st.write_tip(ch)
    cp1 = bt.make_checkpoint(st, ch)
    ch.append("knot", {1: b"\x09" * 32}, "zz")
    st.append_entries(ch.rows[-1:])
    st.write_tip(ch)
    cp2 = bt.make_checkpoint(st, ch)
    k = crypto.Ed25519PrivateKey.from_private_bytes(b"\x11" * 32)
    pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    for cp in (cp1, cp2):
        cp.update(signature=k.sign(bt.checkpoint_payload(cp)).hex(), public_key=pub.hex(),
                  key_id=vkv.key_id_for(pub), status="signed", sig_alg="ed25519")
    test_kid = vkv.key_id_for(pub)
    assert bt.checkpoint_payload(cp2) == vkv.checkpoint_payload(cp2)
    assert vkv.verify_checkpoint(cp2, test_kid, "pure") == ch.root()
    vkv.verify_extends(cp1, cp2)
    with pytest.raises(vkv.ProofError):
        vkv.verify_checkpoint(cp2)  # not the pinned seal key
    bad = dict(cp2, root="00" * 32)
    with pytest.raises(vkv.ProofError):
        vkv.verify_checkpoint(bad, test_kid, "pure")


# ============================================================ 7. flags default OFF
def test_shadow_signing_publish_default_off(monkeypatch):
    monkeypatch.setattr(bt, "_policy", lambda: {})
    assert not bt.shadow_enabled() and not bt.signing_enabled() and not bt.publish_enabled()
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "1")
    assert bt.shadow_enabled()
    monkeypatch.setattr(bt, "_policy", lambda: {"chain_v2_shadow": True})
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "0")
    assert not bt.shadow_enabled()  # env overrides the yaml both ways
    monkeypatch.setenv("MAG_CHAIN_V2_SIGNING", "1")
    assert not bt.signing_enabled()  # env alone is not enough
    with pytest.raises(bt.SigningDisabled):
        bt.sign_checkpoint({"n": 1})
    with pytest.raises(RuntimeError):
        bt.publish_checkpoint({"n": 1, "status": "signed", "signature": "00"})


def test_repo_yaml_ships_flags_off():
    from mag.policy import load_policy
    p = load_policy()
    assert isinstance(p.get("chain_v2_shadow"), bool)  # live shadow flipped true 2026-10-17; signing/publish stay off (A7)
    assert p.get("chain_v2_signing") is False
    assert not p.get("chain_v2_publish", False)


def test_sign_refuses_missing_key_file(tmp_path, monkeypatch):
    monkeypatch.setattr(bt, "signing_enabled", lambda: True)
    with pytest.raises(RuntimeError, match="absent"):
        bt.sign_checkpoint({"n": 1}, key_file=tmp_path / "nope")
    assert not (tmp_path / "nope").exists()  # never mints a key


def test_publish_refuses_unsigned(tmp_path, monkeypatch):
    monkeypatch.setattr(bt, "publish_enabled", lambda: True)
    with pytest.raises(RuntimeError, match="unsigned"):
        bt.publish_checkpoint({"n": 1, "status": "unsigned-pending-operator", "signature": None}, tmp_path)
    assert not any(tmp_path.iterdir())


# ============================================================ 8. freeze / catchup / shadow (temp estate)
RESTORE_N = 30


def _v1_estate(tmp: Path, n=40, secret_at=None, missing=()):
    """A synthetic v1 estate: chain rows with v1 roots, knot files; returns (bio, restore_json)."""
    bio = tmp / "v1"
    (bio / "knots").mkdir(parents=True)
    rows, leaves = [], []
    for j in range(n):
        leaf = hashlib.sha256(f"leaf{j}".encode()).hexdigest()
        leaves.append(leaf)
        r = {"ts": f"2026-10-0{1 + j % 9}T00:00:00Z", "filename": f"k{j:03d}.knot.json", "leaf_hash": leaf,
             "session_id": f"sess{j:03d}", "amended": False, "index": j, "n_leaves": j + 1,
             "parent_verkle_root": bt.v1_merkle_root(leaves[:-1]), "verkle_root": bt.v1_merkle_root(leaves)}
        rows.append(r)
        if j in missing:
            continue
        body = {"leaf_hash": leaf, "note": "ok"}
        if j == secret_at:
            body["note"] = "api_key = " + "Q" * 24
        (bio / "knots" / r["filename"]).write_text(json.dumps(body), encoding="utf-8")
    data = "".join(json.dumps(r) + "\n" for r in rows).encode()
    (bio / "verkle_chain.jsonl").write_bytes(data)
    prefix = b"".join(ln + b"\n" for ln in data.split(b"\n")[:RESTORE_N])
    rj = tmp / "restore.chain.json"
    rj.write_text(json.dumps({"restored_sha256": hashlib.sha256(prefix).hexdigest(), "n_restored": RESTORE_N}))
    return bio, rj, rows


def _freeze(tmp, bio, rj, *extra):
    return subprocess.run([sys.executable, str(FREEZE), "--v2-dir", str(tmp / "v2"), "--v1-bio", str(bio),
                           "--restore-json", str(rj), *extra], capture_output=True, text=True)


def test_freeze_import_catchup_verify_end_to_end(tmp_path):
    bio, rj, rows = _v1_estate(tmp_path, secret_at=12, missing=(3, 4))
    r = _freeze(tmp_path, bio, rj)
    assert r.returncode == 0, r.stdout + r.stderr
    out = json.loads(r.stdout)
    assert out["prefix_ok"] and out["n_v2"] == 41
    assert out["bodies"] == {"copied": 37, "body_missing": 2, "body_withheld": 1}
    assert out["checkpoint_status"] == "unsigned-pending-operator"
    st = bt.Store(tmp_path / "v2", bio)
    man = json.loads((st.seed / "seed_manifest.v1.json").read_text())
    assert man["v1_root_matches_row"] and man["n"] == 40
    assert man["chain_sha256"] == hashlib.sha256((bio / "verkle_chain.jsonl").read_bytes()).hexdigest()
    assert "git_head" in man and "restore_seal" in man
    assert [m["v1_index"] for m in json.loads((st.seed / "missing_bodies.json").read_text())] == [3, 4]
    wh = json.loads((st.seed / "withheld_bodies.json").read_text())
    assert wh[0]["v1_index"] == 12 and "Q" * 24 not in json.dumps(wh)
    copies = sorted(p.name for p in st.knots.iterdir())
    assert len(copies) == 37 and not any("k012" in c for c in copies)
    assert all("Q" * 24 not in p.read_text() for p in st.knots.iterdir())
    ch = st.load(verify_each=True)
    assert ch.root().hex() == out["root_v2"]
    assert int(ch.rows[4]["flags"]) == bt.FLAG_BODY_MISSING and int(ch.rows[13]["flags"]) == bt.FLAG_BODY_WITHHELD

    # v1 moves on: in-place amend of row 5 + two new rows (+ a torn tail line)
    rows[5] = dict(rows[5], leaf_hash=hashlib.sha256(b"amend5").hexdigest(), amended=True)
    (bio / "knots" / rows[5]["filename"]).write_text('{"amended": true}')
    for j in (40, 41):
        rows.append({"ts": "2026-10-17T00:00:00Z", "filename": f"k{j:03d}.knot.json",
                     "leaf_hash": hashlib.sha256(f"leaf{j}".encode()).hexdigest(), "session_id": f"sess{j:03d}"})
    (bio / "verkle_chain.jsonl").write_bytes(("".join(json.dumps(x) + "\n" for x in rows) + '{"torn"').encode())
    c = subprocess.run([sys.executable, str(CATCHUP), "--v2-dir", str(tmp_path / "v2"), "--v1-bio", str(bio), "--check"],
                       capture_output=True, text=True)
    assert c.returncode == 3 and json.loads(c.stdout)["pending"] == 3
    c = subprocess.run([sys.executable, str(CATCHUP), "--v2-dir", str(tmp_path / "v2"), "--v1-bio", str(bio),
                        "--checkpoint"], capture_output=True, text=True)
    rep = json.loads(c.stdout)
    assert rep["appended"] == 3 and rep["kinds"] == {"knot": 2, "amend": 1}
    c2 = subprocess.run([sys.executable, str(CATCHUP), "--v2-dir", str(tmp_path / "v2"), "--v1-bio", str(bio)],
                        capture_output=True, text=True)
    assert json.loads(c2.stdout)["appended"] == 0  # idempotent
    ch = st.load(verify_each=True)
    assert ch.n == 44
    amend = next(e for e in ch.rows if e["kind"] == "amend")
    assert amend["kv"]["4"] == bt.u64v(6).hex()  # supersedes the seed row of session sess005
    # old row 6 still provable, checkpoint chain extends
    cps = [json.loads(x) for x in st.checkpoints.read_text().splitlines()]
    assert len(cps) == 2 and cps[1]["prev_checkpoint_n"] == 41
    assert bt.verify_consistency(bytes.fromhex(cps[0]["root"]), bytes.fromhex(cps[1]["root"]), cps[1]["extends_proof"])

    # verify a seed knot (full) and the latest knot from an EMPTY folder
    empty = tmp_path / "empty"
    empty.mkdir()
    shutil.copy(VERIFIER, empty)
    for i, full in ((7, True), (ch.n - 1, False)):
        (empty / f"p{i}.json").write_text(json.dumps(bt.build_proof(st, ch, i, full=full)))
        v = _run_verifier(empty, f"p{i}.json", "--root", ch.root().hex())
        assert v.returncode == 0, v.stdout
        assert ("body_bound=True" in v.stdout) == full
    # an unsigned checkpoint is not a trust anchor
    (empty / "cp.json").write_text(json.dumps(cps[1]))
    assert _run_verifier(empty, f"p{ch.n - 1}.json", "--checkpoint", "cp.json").returncode == 1


def test_freeze_refuses_when_restore_is_not_a_prefix(tmp_path):
    bio, rj, rows = _v1_estate(tmp_path)
    restore_copy = tmp_path / "restore_rows.jsonl"
    restore_copy.write_bytes(b"".join(ln + b"\n" for ln in (bio / "verkle_chain.jsonl").read_bytes().split(b"\n")[:RESTORE_N]))
    # an in-place v1 amend of row 7 rewrites history after the restore
    leaves = [r["leaf_hash"] for r in rows]
    leaves[7] = hashlib.sha256(b"rewritten").hexdigest()
    rows[7] = dict(rows[7], leaf_hash=leaves[7], amended=True)
    for j, r in enumerate(rows):
        r.update(n_leaves=len(rows), verkle_root=bt.v1_merkle_root(leaves[: j + 1]))
    rows[-1]["verkle_root"] = bt.v1_merkle_root(leaves)
    (bio / "verkle_chain.jsonl").write_bytes("".join(json.dumps(r) + "\n" for r in rows).encode())
    r = _freeze(tmp_path, bio, rj, "--restore-file", str(restore_copy))
    assert r.returncode == 2, r.stdout
    rep = json.loads(r.stdout)
    assert rep["prefix_ok"] is False
    assert [x["index"] for x in rep["diagnosis"]["changed_leaf_rows"]] == [7]
    assert not (tmp_path / "v2" / "tip_v2.json").exists() and not (tmp_path / "v2" / "seed").exists()
    assert list((tmp_path / "v2").glob("FREEZE_REFUSED_*.json"))


def test_freeze_refuses_second_run(tmp_path):
    bio, rj, _ = _v1_estate(tmp_path)
    assert _freeze(tmp_path, bio, rj).returncode == 0
    assert _freeze(tmp_path, bio, rj).returncode == 2


def test_catchup_without_seed_refuses(tmp_path):
    bio, rj, _ = _v1_estate(tmp_path)
    c = subprocess.run([sys.executable, str(CATCHUP), "--v2-dir", str(tmp_path / "v2"), "--v1-bio", str(bio)],
                       capture_output=True, text=True)
    assert c.returncode == 2 and not (tmp_path / "v2").exists()


def test_secret_scan_reports_names_not_values():
    hits = bt.secret_scan(b'{"x": "-----BEGIN OPENSSH PRIVATE KEY-----", "token": "sk-' + b"A" * 30 + b'"}')
    assert "pem_private_key" in hits and "sk_token" in hits
    assert bt.secret_scan(b'{"leaf_hash": "' + b"ab" * 32 + b'", "theme": "harness"}') == []


def test_shadow_append_inert_when_flag_off(tmp_path, monkeypatch):
    monkeypatch.setattr(bt, "_policy", lambda: {})
    st = bt.Store(tmp_path / "v2", tmp_path / "v1")
    assert bt.shadow_append({"leaf_hash": "ab" * 32, "session_id": "s"}, store=st) is None
    assert not (tmp_path / "v2").exists()


def test_shadow_append_mirrors_idempotently_and_logs(tmp_path, monkeypatch):
    bio, rj, rows = _v1_estate(tmp_path)
    assert _freeze(tmp_path, bio, rj).returncode == 0
    st = bt.Store(tmp_path / "v2", bio)
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "1")
    new = {"ts": "2026-10-17T01:00:00Z", "filename": "k999.knot.json", "leaf_hash": "cd" * 32,
           "session_id": "fresh", "index": 40}
    (bio / "knots" / "k999.knot.json").write_text('{"x":1}')
    r1 = bt.shadow_append(new, knot_path=bio / "knots" / "k999.knot.json", store=st)
    assert r1["appended"] == 41 and r1["kind"] == "knot"
    assert bt.shadow_append(new, store=st)["skipped"] == "already_mirrored"
    r3 = bt.shadow_append(dict(new, leaf_hash="ef" * 32), store=st)
    assert r3["kind"] == "amend"
    assert st.load(verify_each=True).n == 43
    # a broken v2 store never raises; the problem lands in shadow_mismatch.jsonl
    st.chain.write_text("garbage\n", encoding="utf-8")
    bt._CACHE.clear()
    assert bt.shadow_append(dict(new, leaf_hash="11" * 32), store=st) is None
    assert "shadow_error" in st.mismatch.read_text()


def test_shadow_without_genesis_logs_only(tmp_path, monkeypatch):
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "1")
    st = bt.Store(tmp_path / "v2", tmp_path / "v1")
    assert bt.shadow_append({"leaf_hash": "ab" * 32, "session_id": "s"}, store=st) is None
    assert "no_v2_genesis" in st.mismatch.read_text()
    assert not st.chain.exists()


# ============================================================ 9. the verkle_knot hook
def test_hook_sits_after_v1_append_and_tip_write():
    src = (ROOT / "mag" / "verkle_knot.py").read_text(encoding="utf-8")
    body = src[src.index("def _append_verkle_knot_unlocked"):src.index("def append_verkle_knot(")]
    hook = body.index("_bt2.shadow_append(chain_row")
    assert body.index("_write_tip_atomic(tip)") < hook
    assert body.index("_write_tip_atomic(tip2)") < hook  # after the self-heal rewrite too
    assert hook < body.index("_update_topic_evolution(")
    seg = body[body.rindex("# V2 shadow", 0, hook):body.index("_update_topic_evolution(")]
    assert len([ln for ln in seg.strip().splitlines() if ln.strip()]) < 10


@pytest.fixture()
def estate(tmp_path: Path, monkeypatch) -> Path:
    from mag import verkle_knot as vk
    monkeypatch.setattr(vk, "CHAIN", tmp_path / "verkle_chain.jsonl")
    monkeypatch.setattr(vk, "TIP", tmp_path / "verkle_tip.json")
    monkeypatch.setattr(vk, "KNOTS", tmp_path / "knots")
    monkeypatch.setattr(vk, "EVOLUTION", tmp_path / "topic_evolution.json")
    monkeypatch.setattr(vk, "LATEST", tmp_path / "latest.knot.json")
    monkeypatch.setattr(vk, "LOCK", tmp_path / ".verkle.lock")
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "0")
    (tmp_path / "knots").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _dossier(session_id: str, salt: str = "") -> dict:
    return {"session_id": session_id,
            "time": {"created_at": {"iso_minute": "2026-10-17T00:00:00Z", "unix_minute": 5000000, "date": "2026-10-17"},
                     "updated_at": {"iso_minute": "2026-10-17T00:01:00Z", "unix_minute": 5000001}},
            "scalar_knot": {"tension_index": 0.3, "duration_minutes": 1},
            "content_commit": {"hex": hashlib.sha256(f"{session_id}:{salt}".encode()).hexdigest()}}


def test_v1_write_survives_a_crashing_shadow(estate, monkeypatch):
    from mag import verkle_knot as vk
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "1")

    def boom(*a, **k):
        raise RuntimeError("v2 exploded")
    monkeypatch.setattr(bt, "shadow_append", boom)
    res = vk.append_verkle_knot(_dossier("hook-crash"))
    assert res["ok"] and vk.CHAIN.read_text().count("\n") == 1


def test_v1_append_drives_shadow_into_temp_v2(estate, tmp_path, monkeypatch):
    from mag import verkle_knot as vk
    v2 = tmp_path / "v2dir"
    monkeypatch.setenv("MAG_BINTREE_V2_DIR", str(v2))
    vk.append_verkle_knot(_dossier("before-genesis"))  # flag off: nothing happens
    assert not v2.exists()
    # genesis over the temp v1 chain (restore = first row), then shadow on
    first = vk.CHAIN.read_bytes()
    rj = tmp_path / "rj.json"
    rj.write_text(json.dumps({"restored_sha256": hashlib.sha256(first).hexdigest(), "n_restored": 1}))
    r = subprocess.run([sys.executable, str(FREEZE), "--v2-dir", str(v2), "--v1-bio", str(estate),
                        "--knots-dir", str(estate / "knots"), "--restore-json", str(rj)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "1")
    vk.append_verkle_knot(_dossier("after-genesis"))
    vk.append_verkle_knot(_dossier("after-genesis", salt="v2"))  # v1 amend -> v2 amend row
    st = bt.Store(v2, estate, [estate / "knots"])
    ch = st.load(verify_each=True)
    assert [e["kind"] for e in ch.rows] == ["genesis", "seed_import", "knot", "amend"]
    assert not st.mismatch.exists() or "shadow_error" not in st.mismatch.read_text()
    assert bt.reconcile(st, check_only=True)["pending"] == 0


def test_freeze_from_certified_restore_copy_then_catchup_amends(tmp_path):
    """Operator path 2026-10-17: seed from the signed restore copy; live rewrites land as amend rows."""
    crypto = pytest.importorskip("cryptography.hazmat.primitives.asymmetric.ed25519")
    from cryptography.hazmat.primitives import serialization
    import base64
    bio, rj, rows = _v1_estate(tmp_path)
    live = bio / "verkle_chain.jsonl"
    restore = tmp_path / "restore_copy.jsonl"
    restore.write_bytes(b"".join(ln + b"\n" for ln in live.read_bytes().split(b"\n")[:RESTORE_N]))
    arc_root = bt.v1_merkle_root([r["leaf_hash"] for r in rows[:RESTORE_N]])
    # live v1 rewrites restore row 7 in place, then grows
    leaves = [r["leaf_hash"] for r in rows]
    leaves[7] = hashlib.sha256(b"rewritten").hexdigest()
    rows[7] = dict(rows[7], leaf_hash=leaves[7], amended=True, filename="k007b.knot.json")
    for j, r in enumerate(rows):
        r.update(verkle_root=bt.v1_merkle_root(leaves[: j + 1]))
    live.write_bytes("".join(json.dumps(r) + "\n" for r in rows).encode())
    # a seal over the restore companion files, signed with a TEST key
    md = tmp_path / "restore.chain.md"
    md.write_text("restore receipt")
    seal_p = tmp_path / "restore.chain.seal"
    k = crypto.Ed25519PrivateKey.from_private_bytes(b"\x22" * 32)
    pub = k.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    payload = {"arc_root": arc_root, "chain_sha": hashlib.sha256(rj.read_bytes()).hexdigest(),
               "seed_sha": hashlib.sha256(md.read_bytes()).hexdigest(), "session": "test-restore"}
    seed_root = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    seal = dict(payload, seed_root=seed_root, key_id=vkv.key_id_for(pub),
                public_key=base64.b64encode(pub).decode(), signature=base64.b64encode(k.sign(seed_root.encode())).decode())
    seal_p.write_text(json.dumps(seal))
    args = ["--source-restore", str(restore), "--restore-seal", str(seal_p)]
    # the live chain alone is refused (restore is no longer a prefix) ...
    assert _freeze(tmp_path, bio, rj).returncode == 2
    # ... a wrong pinned key refuses the restore path ...
    assert _freeze(tmp_path, bio, rj, *args).returncode == 2
    # ... a tampered restore copy refuses
    bad = tmp_path / "bad.jsonl"
    bad.write_bytes(restore.read_bytes().replace(b"leaf", b"Leaf", 1) if b"leaf" in restore.read_bytes()
                    else restore.read_bytes() + b"\n")
    assert _freeze(tmp_path, bio, rj, "--source-restore", str(bad), "--restore-seal", str(seal_p),
                   "--seal-key-id", vkv.key_id_for(pub)).returncode == 2
    r = _freeze(tmp_path, bio, rj, *args, "--seal-key-id", vkv.key_id_for(pub))
    assert r.returncode == 0, r.stdout + r.stderr
    out = json.loads(r.stdout)
    assert out["seed_source"] == "restore_copy" and out["n_v2"] == RESTORE_N + 1 and out["restore_seal_ok"]
    st = bt.Store(tmp_path / "v2", bio)
    man = json.loads((st.seed / "seed_manifest.v1.json").read_text())
    assert man["seed_source"] == "restore_copy"
    assert man["restore_rows_rewritten_in_live"] == [{"index": 7, "fields_changed": ["amended", "filename", "leaf_hash", "verkle_root"]}]
    assert man["live_chain_at_freeze"]["restore_is_prefix"] is False
    assert "rewritten" not in json.dumps(man["restore_rows_rewritten_in_live"])  # no values
    assert (st.seed / "verkle_chain.v1.seed.jsonl").read_bytes() == restore.read_bytes()
    ch = st.load(verify_each=True)
    assert ch.rows[0]["genesis"]["seed_source"] == "restore_copy"
    assert ch.rows[0]["genesis"]["restore_rows_rewritten_in_live"] == [7]
    rep = bt.reconcile(st)
    assert rep["kinds"] == {"knot": len(rows) - RESTORE_N, "amend": 1}
    amend = next(e for e in st.load().rows if e["kind"] == "amend")
    assert amend["v1_index"] == 7 and amend["kv"]["4"] == bt.u64v(8).hex()
    assert bt.reconcile(st, check_only=True)["pending"] == 0


# ============================================================ 10. v1 append-only amends (chain_mode v2, 2026-10-17)
def test_v1_chain_mode_v2_amend_appends_superseding_row(estate, tmp_path, monkeypatch):
    from mag import verkle_knot as vk
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V2)
    vk.append_verkle_knot(_dossier("ao-sess"))
    first = vk.CHAIN.read_bytes()
    r2 = vk.append_verkle_knot(_dossier("ao-sess", salt="changed"))
    assert r2["ok"] and not r2["amended"]
    data = vk.CHAIN.read_bytes()
    assert data.startswith(first), "old v1 rows must stay byte-identical"
    rows = [json.loads(x) for x in data.decode().splitlines()]
    assert len(rows) == 2
    assert rows[1]["supersedes_index"] == 0 and rows[1]["supersedes_leaf_hash"] == rows[0]["leaf_hash"]
    # identical re-save dedupes even when the v2 pointer file is gone (row-scan fallback)
    vk.session_pointer_v2("ao-sess").unlink()
    r3 = vk.append_verkle_knot(_dossier("ao-sess", salt="changed"))
    assert r3.get("skipped") is True and vk.CHAIN.read_bytes() == data


def test_v1_chain_mode_v2_rows_shadow_into_v2_as_amends(estate, tmp_path, monkeypatch):
    from mag import verkle_knot as vk
    v2 = tmp_path / "v2dir"
    monkeypatch.setenv("MAG_BINTREE_V2_DIR", str(v2))
    vk.append_verkle_knot(_dossier("seed-sess"))
    rj = tmp_path / "rj.json"
    rj.write_text(json.dumps({"restored_sha256": hashlib.sha256(vk.CHAIN.read_bytes()).hexdigest(), "n_restored": 1}))
    r = subprocess.run([sys.executable, str(FREEZE), "--v2-dir", str(v2), "--v1-bio", str(estate),
                        "--knots-dir", str(estate / "knots"), "--restore-json", str(rj)], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    monkeypatch.setattr(vk, "chain_mode", lambda: vk.CHAIN_MODE_V2)
    monkeypatch.setenv("MAG_CHAIN_V2_SHADOW", "1")
    vk.append_verkle_knot(_dossier("seed-sess", salt="b"))
    vk.append_verkle_knot(_dossier("seed-sess", salt="c"))
    st = bt.Store(v2, estate, [estate / "knots"])
    ch = st.load(verify_each=True)
    assert [e["kind"] for e in ch.rows] == ["genesis", "seed_import", "amend", "amend"]
    assert ch.rows[3]["v1_index"] == 2 and ch.rows[3]["v1_row"]["supersedes_index"] == 1
    assert bt.reconcile(st, check_only=True)["pending"] == 0
    assert not st.mismatch.exists()
