"""Minimal, standalone BINTREE V2 root builder (watch/inbox/BINTREE_V2_SEED_SPEC.md sec 1-2).

Built 2026-10-23 as an independent re-derivation of the "mag" hash profile. It is NOT wired
to the live chain: no file I/O, no chain reads or writes, no genesis/freeze logic. Pure stdlib.
It computes the same root as mag/bintree_v2.BinaryTree by a different method (bulk build from
sorted keys instead of incremental insert), so it doubles as a cross-check oracle.

Profile "mag" (labeled SHA-256, EIP-7864 shape, empty = 0^32):
  inner = sha256(0x01||L||R)  (0^32 if L == R == 0^32)
  stem  = sha256(0x02||stem31||subroot32)
  leaf  = sha256(0x03||value)
  sub   = sha256(0x04||L||R)  inside the 8-level 256-wide stem subtree (0^32 if both empty)
"""
from __future__ import annotations

import hashlib

ZERO = b"\x00" * 32
STEM_BITS = 248
ROW_PREFIX, SESSION_PREFIX, META_PREFIX = 0x00, 0x80, 0xC0


def _h(tag: int, data: bytes) -> bytes:
    return hashlib.sha256(bytes([tag]) + data).digest()


def h_inner(l: bytes, r: bytes) -> bytes:
    return ZERO if l == ZERO and r == ZERO else _h(0x01, l + r)


def h_stem(stem: bytes, subroot: bytes) -> bytes:
    return _h(0x02, stem + subroot)


def h_leaf(value: bytes | None) -> bytes:
    return ZERO if value is None else _h(0x03, value)


def h_sub(l: bytes, r: bytes) -> bytes:
    return ZERO if l == ZERO and r == ZERO else _h(0x04, l + r)


# ---- key layout (spec sec 2)
def row_stem(i: int) -> bytes:
    return bytes([ROW_PREFIX]) + int(i).to_bytes(8, "big") + b"\x00" * 22


def session_stem(session_id: str) -> bytes:
    return bytes([SESSION_PREFIX]) + hashlib.sha256(b"mag.v2.session\x00" + session_id.encode()).digest()[:30]


META_STEM = bytes([META_PREFIX]) + b"\x00" * 30


def key(stem: bytes, sub: int) -> bytes:
    if len(stem) != 31 or not 0 <= sub < 256:
        raise ValueError("stem must be 31 bytes, sub 0..255")
    return stem + bytes([sub])


def u64v(x: int) -> bytes:
    return b"\x00" * 24 + int(x).to_bytes(8, "big")


# ---- root
def stem_subroot(values: dict[int, bytes]) -> bytes:
    lvl = {i: h_leaf(v) for i, v in values.items()}
    for _ in range(8):
        nxt = {}
        for p in {i >> 1 for i in lvl}:
            h = h_sub(lvl.get(2 * p, ZERO), lvl.get(2 * p + 1, ZERO))
            if h != ZERO:
                nxt[p] = h
        lvl = nxt
    return lvl.get(0, ZERO)


def _bit(si: int, d: int) -> int:
    return (si >> (STEM_BITS - 1 - d)) & 1


def root(kv: dict[bytes, bytes]) -> bytes:
    """Root of the tree holding every key->value in kv (32-byte keys, 32-byte values)."""
    stems: dict[int, tuple[bytes, dict[int, bytes]]] = {}
    for k, v in kv.items():
        if len(k) != 32 or len(v) != 32:
            raise ValueError("keys and values must be 32 bytes")
        si = int.from_bytes(k[:31], "big")
        stems.setdefault(si, (k[:31], {}))[1][k[31]] = v
    order = sorted(stems)

    def build(items: list[int], d: int) -> bytes:
        if not items:
            return ZERO
        if len(items) == 1:  # a lone stem sits as high as possible (no extension nodes)
            s, vals = stems[items[0]]
            return h_stem(s, stem_subroot(vals))
        left = [x for x in items if _bit(x, d) == 0]
        right = [x for x in items if _bit(x, d) == 1]
        return _h(0x01, build(left, d + 1) + build(right, d + 1))

    return build(order, 0)
