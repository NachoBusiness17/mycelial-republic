"""MERKLE CURE, SOLVER B fixtures (2026-10-07): subtree-size node binding.

Lane p4b-merkle-cure, mag/merkle_sized.py. The receipt
(watch/inbox/MERKLE_COLLISION_PROOF_20261007.md) proved [a,b,c] and
[a,b,c,c] share one legacy root; its Option B ("carry leaf-count inside the
structure") is shipped here in the deep form: every internal node hash binds
its subtree leaf count. Laws pinned by this file:

  1. COLLISION DIES (the staged falsifier): sized [a,b,c] vs [a,b,c,c]
     roots differ, across the whole length-ambiguity family; the padding
     pair (node:1:c:c) is domain-separated from an explicit pair
     (node:2:c:c).
  2. OLD-FLAG-OFF COMPATIBILITY: the module is inert flag-off (genesis and
     single-leaf semantics match the legacy algorithm byte-for-byte, whose
     reference is copied verbatim from mag/verkle_knot.py HEAD 5d2263f10);
     the live chain's stored roots are untouched and the receipt's collision
     still reproduces under the legacy root (documented wound, flag-off).
  3. DOCUMENTED MIGRATION PATH: migrate_chain_to_sized() rewrites row roots
     + tip under the single-writer lock, refuses an inconsistent chain
     byte-untouched, and the sized gate then holds while the legacy gate
     refuses (the bindings are mutually exclusive, never silently forked).
  4. WRITER=VERIFIER PIN: sized_merkle_prefix_roots (O(n log n) incremental)
     equals sized_merkle_root (naive) for EVERY prefix, n=0..64.
  5. PROOFS: SizedVerkleProof.verify is fail-closed (countless proofs
     refused, tampered siblings/paths/counts refused, index bounds checked)
     and prove_sized verifies every index of a real appended chain.
  6. CROSS-ARM COMPOSITION: solver A's MAG_POSITION_BOUND_LEAVES flag state
     does not affect this cure (leaf domain untouched here).

Hermetic: the LIVE chain (memory/biography/) is never touched; every
chain-mutating fixture runs on a tmp estate via monkeypatch.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from mag import merkle_sized as ms
from mag import verkle_knot as vk

ENV = ms.MERKLE_SIZED_ENV
CROSS_ENV = "MAG_POSITION_BOUND_LEAVES"


# --- reference implementation: the pre-change legacy algorithm, byte-copied --
# (mag/verkle_knot.py HEAD 5d2263f10, _merkle_root). Backward-compat oracle.

def _ref_h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ref_merkle_root(leaf_hashes: list[str]) -> str:
    if not leaf_hashes:
        return _ref_h(b"empty")
    layer = leaf_hashes[:]
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            right = layer[i + 1] if i + 1 < len(layer) else left
            nxt.append(_ref_h(b"node:" + left.encode() + b":" + right.encode()))
        layer = nxt
    return layer[0]


def _leaf(i: int) -> str:
    return hashlib.sha256(f"fixture-leaf-{i}".encode("utf-8")).hexdigest()


A, B, C, D = _leaf(0), _leaf(1), _leaf(2), _leaf(3)


@pytest.fixture(autouse=True)
def _pin_env(monkeypatch):
    """Pin BOTH cure flags explicitly; no operator env leakage."""
    monkeypatch.delenv(ENV, raising=False)
    monkeypatch.delenv(CROSS_ENV, raising=False)


@pytest.fixture
def estate(tmp_path: Path, monkeypatch) -> Path:
    """Point the whole verkle estate (chain/tip/knots/lock) at tmp_path."""
    monkeypatch.setattr(vk, "CHAIN", tmp_path / "verkle_chain.jsonl")
    monkeypatch.setattr(vk, "TIP", tmp_path / "verkle_tip.json")
    monkeypatch.setattr(vk, "KNOTS", tmp_path / "knots")
    monkeypatch.setattr(vk, "EVOLUTION", tmp_path / "topic_evolution.json")
    monkeypatch.setattr(vk, "LATEST", tmp_path / "latest.knot.json")
    monkeypatch.setattr(vk, "LOCK", tmp_path / ".verkle.lock")
    (tmp_path / "knots").mkdir(parents=True, exist_ok=True)
    return tmp_path


def _dossier(sid: str) -> dict:
    return {
        "session_id": sid,
        "time": {"created_at": {"iso_minute": "2026-10-07T12:00", "unix_minute": 100,
                                "date": "2026-10-07"},
                 "updated_at": {"iso_minute": "2026-10-07T12:10", "unix_minute": 160}},
        "scalar_knot": {"duration_minutes": 10.0},
        "theme_vector": {"dominant": "harness"},
        "content_commit": {"hex": sid[-8:]},
    }


def _hand_chain(leaf_hashes: list[str]) -> None:
    """Write a minimal chain + tip for the given leaf hashes (legacy roots)."""
    rows = [{"ts": f"2026-10-07T12:0{i}Z", "filename": f"f{i}.knot.json",
             "leaf_hash": h, "session_id": f"s{i}"} for i, h in enumerate(leaf_hashes)]
    root = _ref_merkle_root(leaf_hashes) if leaf_hashes else _ref_h(b"empty")
    lines = []
    for i, r in enumerate(rows):
        r = dict(r)
        r["index"] = i
        r["n_leaves"] = i + 1
        r["verkle_root"] = _ref_merkle_root(leaf_hashes[: i + 1])
        lines.append(json.dumps(r))
    vk.CHAIN.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    tip = vk._tip_for_tail(rows, leaf_hashes, root)
    vk._write_tip_atomic(tip)


# --- flag law -----------------------------------------------------------------

def test_flag_default_off():
    assert ms.sized_mode() is False


@pytest.mark.parametrize("value,expected", [
    ("1", True), ("true", True), ("yes", True), ("on", True), (" 1 ", True),
    ("", False), ("0", False), ("false", False), ("no", False), ("garbage", False),
])
def test_flag_parse(monkeypatch, value, expected):
    monkeypatch.setenv(ENV, value)
    assert ms.sized_mode() is expected


# --- 1. COLLISION DIES ---------------------------------------------------------

def test_probe_flips_collision_false():
    r3 = ms.sized_merkle_root([A, B, C])
    r3c = ms.sized_merkle_root([A, B, C, C])
    assert r3 != r3c  # the receipt's staged falsifier: COLLISION: False


def test_length_ambiguity_family_all_distinct():
    family = [
        [A], [A, A], [A, B], [A, B, B], [A, B, C], [A, B, C, C],
        [A, B, C, C, C], [A, B, C, D], [A, B, C, D, D],
        [_leaf(i) for i in range(13)], [_leaf(i) for i in range(12)] + [_leaf(11)],
    ]
    roots = [ms.sized_merkle_root(seq) for seq in family]
    assert len(set(roots)) == len(roots)


def test_padding_pair_domain_separated_from_explicit_pair():
    # The mechanism: a padded tail folds as node:1:c:c, an explicit second c
    # as node:2:c:c. At an odd boundary the legacy tree folds both shapes to
    # the same bytes (the wound); sized does not.
    assert ms.sized_node_hash(C, C, 1) != ms.sized_node_hash(C, C, 2)
    assert _ref_merkle_root([A, B, C]) == _ref_merkle_root([A, B, C, C])
    assert ms.sized_merkle_root([A, B, C]) != ms.sized_merkle_root([A, B, C, C])


def test_sized_root_matches_independent_formula():
    # Hand-rolled expected values, independent of mag/merkle_sized internals.
    n01 = _ref_h(b"node:2:" + A.encode() + b":" + B.encode())
    pad_cc = _ref_h(b"node:1:" + C.encode() + b":" + C.encode())
    expect3 = _ref_h(b"node:3:" + n01.encode() + b":" + pad_cc.encode())
    assert ms.sized_merkle_root([A, B, C]) == expect3
    cc = _ref_h(b"node:2:" + C.encode() + b":" + C.encode())
    expect4 = _ref_h(b"node:4:" + n01.encode() + b":" + cc.encode())
    assert ms.sized_merkle_root([A, B, C, C]) == expect4


def test_prefix_chain_roots_distinguish_dropped_tail():
    four = ms.sized_merkle_root([A, B, C, D])
    four_dup = ms.sized_merkle_root([A, B, C, D, D])
    assert four != four_dup  # double-written trailing leaf is now visible


# --- 2. OLD-FLAG-OFF COMPATIBILITY ---------------------------------------------

def test_legacy_wound_still_reproduces_flag_off():
    # Documented: flag-off the estate keeps legacy roots (the receipt's
    # collision reproduces) so the live chain verifies byte-identically.
    assert vk._merkle_root([A, B, C]) == vk._merkle_root([A, B, C, C])
    assert vk._merkle_root([A, B, C]) == _ref_merkle_root([A, B, C])


def test_genesis_and_single_leaf_match_legacy_semantics():
    assert ms.sized_merkle_root([]) == _ref_h(b"empty")
    assert ms.sized_merkle_root([]) == vk._merkle_root([])
    assert ms.sized_merkle_root([A]) == A
    assert ms.sized_merkle_root([A]) == vk._merkle_root([A])


def test_cross_arm_composition_leaf_domain_untouched(estate):
    # Solver A's leaf-position flag does not move this cure: sized proofs are
    # built and verified over the legacy leaf domain regardless of its state.
    # HERMETICITY FIX 2026-10-10 (archaeologist mate, receipt
    # watch/inbox/mates_leave_protocol/receipts/receipt_20261010_archaeologist.md):
    # this test previously called _hand_chain([A, B, C]) with NO estate
    # fixture, so vk.CHAIN/vk.TIP stayed the LIVE memory/biography/ paths and
    # any pytest run overwrote the live provenance chain with this 3-row
    # fixture (byte-verified: live chain rows 0-2 carried sha256 of
    # "fixture-leaf-{i}" and legacy roots on 2026-10-10). The missing
    # parameter is the whole fix; the estate fixture redirects CHAIN, TIP,
    # KNOTS, EVOLUTION, LATEST and LOCK to tmp_path.
    _hand_chain([A, B, C])
    monkey_bound = pytest.MonkeyPatch()
    try:
        monkey_bound.setenv(CROSS_ENV, "1")
        proof = ms.prove_sized(1)
        assert proof["ok"] is True
        assert proof["verified"] is True
    finally:
        monkey_bound.undo()


# --- 4. WRITER=VERIFIER PIN ----------------------------------------------------

def test_prefix_roots_parity_brute_force():
    for n in range(0, 65):
        hashes = [_leaf(i) for i in range(n)]
        prefix = ms.sized_merkle_prefix_roots(hashes)
        assert len(prefix) == n
        for i in range(n):
            assert prefix[i] == ms.sized_merkle_root(hashes[: i + 1]), n


def test_prefix_roots_empty():
    assert ms.sized_merkle_prefix_roots([]) == []


# --- 5. PROOFS ------------------------------------------------------------------

def test_prove_sized_verifies_every_index(estate):
    hashes = [_leaf(i) for i in range(6)]
    _hand_chain(hashes)
    for idx in range(6):
        proof = ms.prove_sized(idx)
        assert proof["ok"] is True
        assert proof["binding"] == ms.BINDING_NAME
        assert proof["root"] == ms.sized_merkle_root(hashes)
        assert proof["verified"] is True
        assert ms.SizedVerkleProof(
            index=proof["index"], leaf_hash=proof["leaf_hash"],
            path=proof["path"], root=proof["root"],
        ).verify(n_leaves=6) is True


def test_prove_sized_rejects_out_of_range(estate):
    _hand_chain([A, B, C])
    assert ms.prove_sized(3)["ok"] is False
    assert ms.prove_sized(-1)["ok"] is False
    assert ms.prove_sized()["index"] == 2  # default = latest


def test_proof_fail_closed_on_missing_count(estate):
    _hand_chain([A, B, C])
    proof = ms.prove_sized(0)
    bare = ms.SizedVerkleProof(proof["index"], proof["leaf_hash"],
                               proof["path"], proof["root"])
    assert bare.verify() is False  # the count IS the binding; countless = refused


def test_proof_refuses_tamper(estate):
    hashes = [_leaf(i) for i in range(6)]
    _hand_chain(hashes)
    proof = ms.prove_sized(2)
    good = ms.SizedVerkleProof(proof["index"], proof["leaf_hash"],
                               list(proof["path"]), proof["root"])
    assert good.verify(n_leaves=6) is True
    # tampered sibling
    bad_path = list(proof["path"])
    bad_path[0] = _leaf(99)
    assert ms.SizedVerkleProof(2, proof["leaf_hash"], bad_path,
                               proof["root"]).verify(n_leaves=6) is False
    # truncated path
    assert ms.SizedVerkleProof(2, proof["leaf_hash"], proof["path"][:-1],
                               proof["root"]).verify(n_leaves=6) is False
    # wrong count
    assert good.verify(n_leaves=5) is False
    assert good.verify(n_leaves=7) is False
    # tampered leaf hash
    assert ms.SizedVerkleProof(2, _leaf(98), proof["path"],
                               proof["root"]).verify(n_leaves=6) is False
    # index beyond the count
    assert ms.SizedVerkleProof(6, proof["leaf_hash"], proof["path"],
                               proof["root"]).verify(n_leaves=6) is False


def test_padded_replay_dies(estate):
    # The attack the receipt staged: a proof from the 4-leaf chain replayed
    # against the trailing-duplicated 5-leaf tree. Legacy shares one root;
    # sized does not, and the count-bound verifier refuses the replay.
    hashes4 = [A, B, C, D]
    _hand_chain(hashes4)
    p4 = ms.prove_sized(3)
    root5 = ms.sized_merkle_root([A, B, C, D, D])
    assert p4["root"] != root5
    replay = ms.SizedVerkleProof(index=3, leaf_hash=p4["leaf_hash"],
                                 path=p4["path"], root=root5)
    assert replay.verify(n_leaves=5) is False
    assert replay.verify(n_leaves=4) is False


def test_single_leaf_chain_proof(estate):
    _hand_chain([A])
    proof = ms.prove_sized()
    assert proof["ok"] is True
    assert proof["path"] == []
    assert proof["verified"] is True


def test_prove_verify_exhaustive_every_index_every_size(estate):
    # The sibling-parity bug class dies only exhaustively: build a 33-leaf
    # chain once, then re-root the chain file to each prefix and prove+verify
    # EVERY index at EVERY length 1..33.
    all_hashes = [_leaf(i) for i in range(33)]
    for n in range(1, 34):
        _hand_chain(all_hashes[:n])
        root = ms.sized_merkle_root(all_hashes[:n])
        for idx in range(n):
            proof = ms.prove_sized(idx)
            assert proof["ok"] is True, (n, idx)
            assert proof["verified"] is True, (n, idx)
            assert proof["root"] == root, (n, idx)
            bare = ms.SizedVerkleProof(proof["index"], proof["leaf_hash"],
                                       proof["path"], proof["root"])
            assert bare.verify(n_leaves=n) is True, (n, idx)
            # the same proof never verifies against a neighboring count
            if n > 1:
                assert bare.verify(n_leaves=n - 1) is False, (n, idx)


# --- 3. DOCUMENTED MIGRATION PATH ----------------------------------------------

def test_migration_happy_path(estate):
    # Real appended legacy chain (v1 writer), then the documented migration.
    for i in range(5):
        out = vk.append_verkle_knot(_dossier(f"2026-10-07_mig_s{i}"))
        assert out["ok"] is True
    ok, why = vk._verify_chain_consistent()
    assert ok, why  # legacy gate holds pre-migration
    report = ms.migrate_chain_to_sized()
    assert report["ok"] is True and report["migrated"] is True, report
    assert report["from"] == "legacy" and report["to"] == ms.BINDING_NAME
    rows = vk._load_chain_rows()
    hashes = [r["leaf_hash"] for r in rows]
    prefix = ms.sized_merkle_prefix_roots(hashes)
    for i, r in enumerate(rows):
        assert r["verkle_root"] == prefix[i]
    tip = json.loads(vk.TIP.read_text(encoding="utf-8"))
    assert tip["merkle_binding"] == ms.BINDING_NAME
    assert tip["root"] == prefix[-1]
    ok_sized, why_sized = ms.verify_chain_consistent_sized()
    assert ok_sized, why_sized
    ok_legacy, _ = vk._verify_chain_consistent()
    assert ok_legacy is False  # bindings are mutually exclusive, never forked
    assert ms.prove_sized()["verified"] is True


def test_migration_refuses_inconsistent_chain_byte_untouched(estate):
    _hand_chain([A, B, C])
    rows = vk._load_chain_rows()
    rows[-1]["verkle_root"] = "0" * 64
    vk.CHAIN.write_bytes(("\n".join(json.dumps(r) for r in rows) + "\n").encode("utf-8"))
    before = vk.CHAIN.read_bytes()
    report = ms.migrate_chain_to_sized()
    assert report["ok"] is False and report["migrated"] is False
    assert "heal" in report["error"]
    assert vk.CHAIN.read_bytes() == before


def test_migration_refuses_empty_chain(estate):
    report = ms.migrate_chain_to_sized()
    assert report["ok"] is False
    assert "empty chain" in report["error"]


def test_sized_gate_names_migration_on_legacy_chain(estate):
    _hand_chain([A, B, C])
    ok, why = ms.verify_chain_consistent_sized()
    assert ok is False
    assert "migrate_chain_to_sized" in why


def test_sized_gate_passes_after_migration_and_checks_tip(estate):
    _hand_chain([A, B, C])
    assert ms.migrate_chain_to_sized()["ok"] is True
    ok, why = ms.verify_chain_consistent_sized()
    assert ok, why
    # a count-lying tip refuses the sized gate too
    tip = json.loads(vk.TIP.read_text(encoding="utf-8"))
    tip["n_leaves"] = 99
    vk.TIP.write_text(json.dumps(tip), encoding="utf-8")
    ok2, why2 = ms.verify_chain_consistent_sized()
    assert ok2 is False
    assert "n_leaves" in why2
