"""MERKLE CURE (2026-10-07): position-bound leaf hashing behind a flag.

Defect proven live in watch/inbox/MERKLE_COLLISION_PROOF_20261007.md:
_merkle_root duplicates the last node at every odd level, so [a,b,c] and
[a,b,c,c] build byte-identical roots (length ambiguity; content forgery stays
blocked by the b"leaf:" domain). Cure shipped here (the receipt's Option A):
MAG_POSITION_BOUND_LEAVES=1 binds the leaf's chain index into its hash domain
(b"leaf:<i>:" + raw), which flips the probe to COLLISION: False.

Laws pinned by this file:
  1. Flag OFF (default): legacy b"leaf:" domain BYTE-IDENTICAL to the
     pre-change algorithm (reference implementation copied verbatim from the
     HEAD bytes of mag/verkle_knot.py, commit 5d2263f10) across a fixture
     matrix, and the receipt's collision still reproduces untouched.
  2. Flag ON: [a,b,c] vs [a,b,c,c] roots DIFFER (the staged falsifier),
     across a family of length-ambiguous pairs.
  3. Flag ON with no index stays in the legacy domain so pre-migration
     verifiers (knot_rehash_patrol, verkle_dangling_repair,
     VerkleProof.verify) remain coherent.
  4. Flag parsing fails closed: any value outside the truthy set is OFF.

Pure-function tests only: the LIVE chain (memory/biography/) is read-only by
ruling and is never touched here; migration stays operator-gated.
"""
from __future__ import annotations

import hashlib
import json

import pytest

from mag import verkle_knot as vk

ENV = vk.POSITION_BOUND_LEAVES_ENV


# --- reference implementation: the pre-change algorithm, byte-copied ---------
# (mag/verkle_knot.py HEAD 5d2263f10, _h/_leaf_hash/_merkle_root). This is the
# backward-compat oracle: flag-off output must equal it byte for byte.

def _ref_h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _ref_leaf_hash(obj) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
    return _ref_h(b"leaf:" + raw)


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


# --- fixtures ----------------------------------------------------------------

A, B, C, D = {"k": "a"}, {"k": "b"}, {"k": "c"}, {"k": "d"}


@pytest.fixture(autouse=True)
def _pin_env(monkeypatch):
    """Every test pins the flag explicitly; no operator env leakage."""
    monkeypatch.delenv(ENV, raising=False)


# --- 1. flag OFF: byte-identical legacy behavior -----------------------------

def test_flag_default_off():
    assert vk.position_bound_leaves() is False


def test_flag_off_leaf_hash_matches_pre_change_reference():
    for obj in (A, B, C, D, {"u": "thème-λ", "n": [1, 2.5, None]},
                {"k": "c", "extra": {"deep": ["x" * 40]}}, 42, "raw-str"):
        assert vk._leaf_hash(obj) == _ref_leaf_hash(obj)


def test_flag_off_root_matches_pre_change_reference_lengths_0_to_9():
    for n in range(0, 10):
        objs = [{"i": i, "content": f"leaf-{i}", "nested": {"x": [i, 2 * i]}}
                for i in range(n)]
        hashes = [_ref_leaf_hash(o) for o in objs]
        assert vk._merkle_root(hashes) == _ref_merkle_root(hashes)


def test_flag_off_ignores_index_argument():
    # The signature grew an optional index; flag OFF it must change nothing.
    assert vk._leaf_hash(C, 0) == _ref_leaf_hash(C)
    assert vk._leaf_hash(C, 3) == _ref_leaf_hash(C)


def test_flag_off_reproduces_the_receipt_collision_untouched():
    # The defect exists flag-off BY DESIGN until the operator migrates: the
    # receipt's probe ([a,b,c] vs [a,b,c,c]) must still collide so the live
    # chain's stored roots keep verifying byte-identically.
    r3 = vk._merkle_root([_ref_leaf_hash(A), _ref_leaf_hash(B), _ref_leaf_hash(C)])
    r3c = vk._merkle_root([_ref_leaf_hash(A), _ref_leaf_hash(B),
                           _ref_leaf_hash(C), _ref_leaf_hash(C)])
    assert r3 == r3c


def test_empty_chain_root_unchanged_both_flags(monkeypatch):
    monkeypatch.setenv(ENV, "1")
    assert vk._merkle_root([]) == _ref_h(b"empty")


# --- 2. flag ON: the probe flips ---------------------------------------------

def _bound(objs: list) -> list[str]:
    return [vk._leaf_hash(o, i) for i, o in enumerate(objs)]


def test_flag_on_probe_flips_collision_false(monkeypatch):
    monkeypatch.setenv(ENV, "1")
    r3 = vk._merkle_root(_bound([A, B, C]))
    r3c = vk._merkle_root(_bound([A, B, C, C]))
    assert r3 != r3c  # COLLISION: False (the receipt's staged falsifier)


def test_flag_on_length_ambiguity_family_all_distinct(monkeypatch):
    monkeypatch.setenv(ENV, "1")
    family = [
        [A],
        [A, A],
        [A, B],
        [A, B, B],
        [A, B, C],
        [A, B, C, C],
        [A, B, C, C, C],
        [A, B, C, D],
        [A, B, C, D, D],
    ]
    roots = [vk._merkle_root(_bound(seq)) for seq in family]
    assert len(set(roots)) == len(roots)


def test_flag_on_root_matches_independent_bound_formula(monkeypatch):
    # Hand-rolled expected value for [A,B,C]: leaves are position-bound, then
    # the legacy duplicate-last node fold. Independent of vk internals.
    monkeypatch.setenv(ENV, "1")
    l0 = _ref_h(b"leaf:0:" + json.dumps(A, sort_keys=True, default=str).encode("utf-8"))
    l1 = _ref_h(b"leaf:1:" + json.dumps(B, sort_keys=True, default=str).encode("utf-8"))
    l2 = _ref_h(b"leaf:2:" + json.dumps(C, sort_keys=True, default=str).encode("utf-8"))
    n01 = _ref_h(b"node:" + l0.encode() + b":" + l1.encode())
    n22 = _ref_h(b"node:" + l2.encode() + b":" + l2.encode())
    expect = _ref_h(b"node:" + n01.encode() + b":" + n22.encode())
    assert vk._merkle_root(_bound([A, B, C])) == expect


def test_flag_on_same_content_different_position_hashes_differ(monkeypatch):
    monkeypatch.setenv(ENV, "1")
    assert vk._leaf_hash(C, 2) != vk._leaf_hash(C, 3)
    assert vk._leaf_hash(C, 2) == vk._leaf_hash(C, 2)  # deterministic


def test_flag_on_prefix_chain_roots_distinguish_dropped_tail(monkeypatch):
    # The operationally dangerous shape from the receipt: a record that
    # double-wrote its trailing leaf vs one that wrote it once.
    monkeypatch.setenv(ENV, "1")
    four = vk._merkle_root(_bound([A, B, C, D]))
    four_dup = vk._merkle_root(_bound([A, B, C, D, D]))
    assert four != four_dup


# --- 3. flag ON without index: documented legacy fallback ---------------------

def test_flag_on_without_index_stays_legacy_domain(monkeypatch):
    monkeypatch.setenv(ENV, "1")
    for obj in (A, C, {"u": "thème-λ"}):
        assert vk._leaf_hash(obj) == _ref_leaf_hash(obj)
        assert vk._leaf_hash(obj, None) == _ref_leaf_hash(obj)


# --- 4. flag parsing fails closed ---------------------------------------------

@pytest.mark.parametrize("value,expected", [
    ("1", True), ("true", True), ("True", True), ("yes", True), ("on", True),
    ("", False), ("0", False), ("false", False), ("no", False), ("garbage", False),
    (" 1 ", True),
])
def test_flag_parse(monkeypatch, value, expected):
    monkeypatch.setenv(ENV, value)
    assert vk.position_bound_leaves() is expected
