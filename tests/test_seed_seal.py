"""tests/test_seed_seal.py - SS-1 forge drill (2026-10-01).

The forge drill the ticket names: tamper bytes, recompute the hashes (the
honest-looking attacker of pam.check.txt section 3), and assert the verifier
REFUSES. Every drill patches the seal as far as an attacker WITHOUT the key
can go - rehashed shas, rebuilt seed_root - and the Ed25519 signature over
the root is the one thing they cannot mint. Also pinned: the PAM SEC-005
shape (stripped signature must NOT verify by silence), fail-closed missing
seal, key-swap refusal, and root determinism over the canonical form.

Tests NEVER touch state/keys/seed_seal_key - every signing call passes an
explicit tmp key_file (same law as tests/test_ah2_proof.py).
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from pathlib import Path

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import seed_seal  # noqa: E402

SESSION = "sess_testdrill"
ARC_ROOT = "eacb5b32e9ad5b9a"
KEY_HEX = "22" * 32  # fixed test-only dev seed


def _pair(tmp_path: Path, body: str = "operator fork 1\noperator fork 2\n") -> tuple[Path, Path]:
    """A real-shaped seed+chain pair under the arc_seed_/arc_chain_ convention."""
    chain = {"schema": "arc_seed.v1", "session": SESSION,
             "anatomy": {"arc_root": ARC_ROOT, "calls": 2}, "turns": [{"i": 0}, {"i": 1}]}
    seed = f"# ARC SEED\n\nsession: {SESSION[:13]}  arc_root: {ARC_ROOT}\n\n{body}"
    chain_path = tmp_path / f"arc_chain_{SESSION[:13]}_20260101_0000.json"
    seed_path = tmp_path / f"arc_seed_{SESSION[:13]}_20260101_0000.md"
    chain_path.write_text(json.dumps(chain, indent=1), encoding="utf-8")
    seed_path.write_text(seed, encoding="utf-8")
    return seed_path, chain_path


@pytest.fixture()
def key_file(tmp_path: Path) -> Path:
    return tmp_path / "test_only_key"


def _sign(tmp_path: Path, key_file: Path) -> dict:
    seed_path, chain_path = _pair(tmp_path)
    out = seed_seal.sign_seed(seed_path, chain_path, key_file=key_file)
    assert out["ok"] is True
    return {"out": out, "seed_path": seed_path, "chain_path": chain_path}


def _rebuild_root(session: str, arc_root: str, seed_sha: str, chain_sha: str) -> str:
    payload = {"arc_root": arc_root, "chain_sha": chain_sha,
               "seed_sha": seed_sha, "session": session}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def test_sign_then_verify_happy_path(tmp_path, key_file):
    d = _sign(tmp_path, key_file)
    v = seed_seal.verify_seed(d["seed_path"], d["chain_path"])
    assert v["ok"] is True, v
    assert v["session"] == SESSION and v["arc_root"] == ARC_ROOT
    assert (v["reason"] == "verified")


def test_root_is_deterministic_over_canonical_form(tmp_path, key_file):
    """Same bytes -> same seed_root; re-running sign is byte-stable apart from
    the outside-the-root sealed_at stamp."""
    d = _sign(tmp_path, key_file)
    root1 = d["out"]["seal"]["seed_root"]
    expect = _rebuild_root(SESSION, ARC_ROOT,
                           seed_seal.sha256_file(d["seed_path"]),
                           seed_seal.sha256_file(d["chain_path"]))
    assert root1 == expect


def test_forge_drill_seed_body_tamper_with_full_rehash(tmp_path, key_file):
    """THE DRILL: tamper seed bytes, recompute seed_sha, patch the seal's
    seed_sha AND seed_root with the attacker's honest-looking values - the
    verifier must refuse because the signature no longer covers the root."""
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seal_path = seed_path.with_suffix(".seal")
    seed_path.write_text("# ARC SEED\n\nFORGED: the attacker rewrote LAYER 1\n",
                         encoding="utf-8")
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["seed_sha"] = seed_seal.sha256_file(seed_path)  # attacker rehashes
    seal["seed_root"] = _rebuild_root(seal["session"], seal["arc_root"],
                                      seal["seed_sha"], seal["chain_sha"])
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False, "full-rehash forge MUST NOT verify"
    assert "signature" in v["reason"].lower(), v


def test_forge_drill_chain_tamper_with_full_rehash(tmp_path, key_file):
    """Tamper chain bytes (a turn), recompute chain_sha, patch seal shas and
    root, keep the original signature - refused at the signature."""
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seal_path = seed_path.with_suffix(".seal")
    chain = json.loads(chain_path.read_text(encoding="utf-8"))
    chain["turns"][0]["i"] = 999
    chain_path.write_text(json.dumps(chain, indent=1), encoding="utf-8")
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["chain_sha"] = seed_seal.sha256_file(chain_path)
    seal["seed_root"] = _rebuild_root(seal["session"], seal["arc_root"],
                                      seal["seed_sha"], seal["chain_sha"])
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False
    assert "signature" in v["reason"].lower(), v


def test_forge_drill_session_swap_in_chain(tmp_path, key_file):
    """Point the chain at a different session, rehash everything the attacker
    can rehash - session feeds the root, signature refuses."""
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seal_path = seed_path.with_suffix(".seal")
    chain = json.loads(chain_path.read_text(encoding="utf-8"))
    chain["session"] = "sess_swapped"
    chain_path.write_text(json.dumps(chain, indent=1), encoding="utf-8")
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["session"] = "sess_swapped"
    seal["chain_sha"] = seed_seal.sha256_file(chain_path)
    seal["seed_root"] = _rebuild_root(seal["session"], seal["arc_root"],
                                      seal["seed_sha"], seal["chain_sha"])
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False
    assert "signature" in v["reason"].lower(), v


def test_stripped_signature_refused_not_silent(tmp_path, key_file):
    """PAM's SEC-005 defect shape: an attacker strips the signature entirely;
    our verifier must refuse, never return True by silence."""
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seal_path = seed_path.with_suffix(".seal")
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    del seal["signature"]
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False
    assert "signature" in v["reason"].lower(), v


def test_empty_signature_refused(tmp_path, key_file):
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seal_path = seed_path.with_suffix(".seal")
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["signature"] = ""
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    assert seed_seal.verify_seed(seed_path, chain_path)["ok"] is False


def test_missing_seal_fails_closed(tmp_path, key_file):
    d = _sign(tmp_path, key_file)
    d["seed_path"].with_suffix(".seal").unlink()
    v = seed_seal.verify_seed(d["seed_path"], d["chain_path"])
    assert v["ok"] is False and "seal missing" in v["reason"], v


def test_missing_seed_byte_drift_fails_closed(tmp_path, key_file):
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seed_path.write_text("# ARC SEED\n\nsession line drifted\n", encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False and "seed_sha mismatch" in v["reason"], v


def test_key_swap_refused(tmp_path, key_file):
    """An attacker swaps in their own pubkey + matching key_id - key_id is
    domain-separated from the pubkey bytes, but a self-consistent attacker
    pair still fails: the signature was minted by the REAL key."""
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seal_path = seed_path.with_suffix(".seal")
    attacker_key = tmp_path / "attacker_key"
    attacker_key.write_text("33" * 32, encoding="utf-8")
    ak = Ed25519PrivateKey.from_private_bytes(bytes.fromhex("33" * 32))
    pub_raw = ak.public_key().public_bytes(serialization.Encoding.Raw,
                                           serialization.PublicFormat.Raw)
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["public_key"] = base64.b64encode(pub_raw).decode("ascii")
    seal["key_id"] = seed_seal.key_id_for(pub_raw)  # self-consistent swap
    seal["seed_root"] = _rebuild_root(seal["session"], seal["arc_root"],
                                      seal["seed_sha"], seal["chain_sha"])
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False
    assert "signature" in v["reason"].lower(), v


def test_key_id_pubkey_inconsistency_refused(tmp_path, key_file):
    d = _sign(tmp_path, key_file)
    seed_path, chain_path = d["seed_path"], d["chain_path"]
    seal_path = seed_path.with_suffix(".seal")
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    seal["key_id"] = "0" * 16
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False and "key_id" in v["reason"], v


def test_wrong_key_signing_never_verifies(tmp_path, key_file):
    """A seal minted by a different key than the one the pair claims is a
    forgery by construction: sign under attacker key, verify refuses."""
    seed_path, chain_path = _pair(tmp_path)
    attacker_key = tmp_path / "attacker_key"
    out = seed_seal.sign_seed(seed_path, chain_path, key_file=attacker_key)
    assert out["ok"] is True
    # verify against the REAL fleet key instead of the attacker key that signed
    real_key_file = tmp_path / "fleet_key"
    real_key_file.write_text(KEY_HEX, encoding="utf-8")
    seal_path = seed_path.with_suffix(".seal")
    seal = json.loads(seal_path.read_text(encoding="utf-8"))
    rk = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(KEY_HEX))
    pub_raw = rk.public_key().public_bytes(serialization.Encoding.Raw,
                                           serialization.PublicFormat.Raw)
    seal["public_key"] = base64.b64encode(pub_raw).decode("ascii")
    seal["key_id"] = seed_seal.key_id_for(pub_raw)
    seal_path.write_text(json.dumps(seal, indent=1, sort_keys=True), encoding="utf-8")
    v = seed_seal.verify_seed(seed_path, chain_path)
    assert v["ok"] is False and "signature" in v["reason"].lower(), v


def test_sign_mints_key_once_and_reuses(tmp_path, key_file):
    """Key law: first sign mints the key file, second sign reuses it (same
    key_id), and the file never contains anything but the hex seed."""
    d1 = _sign(tmp_path, key_file)
    assert key_file.is_file()
    assert bytes.fromhex(key_file.read_text(encoding="utf-8").strip()).__len__() == 32
    d2 = seed_seal.sign_seed(d1["seed_path"], d1["chain_path"], key_file=key_file)
    assert d2["seal"]["key_id"] == d1["out"]["seal"]["key_id"]


def test_verify_real_repo_seed_if_sealed():
    """The landed real-seal check: if watch/arc_seeds carries a .seal sidecar,
    it must verify fail-closed green against the current bytes. Skipped (not
    failed) when no sidecar exists yet - the CLI check in the lane receipt is
    the byte-proof of the real seed."""
    seeds_dir = ROOT / "watch" / "arc_seeds"
    seals = sorted(seeds_dir.glob("*.seal")) if seeds_dir.is_dir() else []
    if not seals:
        pytest.skip("no .seal sidecar landed yet")
    for seal_path in seals:
        seed_path = seal_path.with_suffix(".md")
        assert seed_path.is_file(), f"seal without seed: {seal_path}"
        v = seed_seal.verify_seed(seed_path)
        assert v["ok"] is True, f"{seal_path}: {v}"
