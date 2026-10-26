"""Tests for mag/bintree_v2_min.py. Pure in-memory; never touches the live chain."""
from __future__ import annotations

import hashlib
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import bintree_v2_min as m  # noqa: E402


def test_empty_tree_is_zero():
    assert m.root({}) == m.ZERO


def test_domain_tags_match_spec():
    a, b = b"\x11" * 32, b"\x22" * 32
    assert m.h_inner(a, b) == hashlib.sha256(b"\x01" + a + b).digest()
    assert m.h_stem(b"\x33" * 31, a) == hashlib.sha256(b"\x02" + b"\x33" * 31 + a).digest()
    assert m.h_leaf(a) == hashlib.sha256(b"\x03" + a).digest()
    assert m.h_sub(a, b) == hashlib.sha256(b"\x04" + a + b).digest()
    assert m.h_inner(m.ZERO, m.ZERO) == m.ZERO and m.h_sub(m.ZERO, m.ZERO) == m.ZERO
    assert m.h_inner(a, b) != m.h_sub(a, b)  # tags separate node kinds


def test_single_key_root():
    k, v = m.key(m.row_stem(1), 0), b"\x07" * 32
    sub = {0: v}
    assert m.root({k: v}) == m.h_stem(k[:31], m.stem_subroot(sub))


def test_key_layout():
    assert m.row_stem(5) == b"\x00" + (5).to_bytes(8, "big") + b"\x00" * 22
    assert len(m.session_stem("abc")) == 31 and m.session_stem("abc")[0] == 0x80
    assert m.META_STEM == b"\xc0" + b"\x00" * 30
    assert m.u64v(3)[-1] == 3 and len(m.u64v(3)) == 32


def _sample(n=60, seed=7):
    rnd = random.Random(seed)
    kv = {}
    for i in range(1, n + 1):
        kv[m.key(m.row_stem(i), rnd.randrange(4))] = rnd.randbytes(32)
    for s in ("s1", "s2", "s3"):
        kv[m.key(m.session_stem(s), 0)] = rnd.randbytes(32)
    kv[m.key(m.META_STEM, 0)] = m.u64v(n)
    return kv


def test_order_independent_and_sensitive():
    kv = _sample()
    items = list(kv.items())
    random.Random(1).shuffle(items)
    assert m.root(dict(items)) == m.root(kv)
    k0 = next(iter(kv))
    kv2 = dict(kv); kv2[k0] = b"\xff" * 32
    assert m.root(kv2) != m.root(kv)


def test_matches_existing_bintree_v2_in_memory():
    """Cross-check against mag.bintree_v2.BinaryTree (in-memory only, no Chain, no files)."""
    from mag import bintree_v2 as ref
    kv = _sample(200, seed=11)
    t = ref.BinaryTree("mag")
    for k, v in kv.items():
        t.insert(k, v)
    assert t.root_hash() == m.root(kv)
    assert ref.row_stem(9) == m.row_stem(9) and ref.session_stem("x") == m.session_stem("x")


def test_module_has_no_io():
    src = (ROOT / "mag" / "bintree_v2_min.py").read_text(encoding="utf-8")
    for bad in ("open(", "Path(", "verkle", "biography", "subprocess", "os.environ"):
        assert bad not in src, bad
