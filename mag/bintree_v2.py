"""Mag v2 chain: an EIP-7864-shaped binary hash tree over the v1 Verkle-chain rows.

Spec: BINTREE_V2_SEED_SPEC.md (2026-10-17, Nacho approved all 8 decisions).
Port of the box spike (bintree_spike/bintree.py + magv2.py, 25 tests) plus the
repo glue: row log + tip under memory/biography_v2/, immutable knot copies,
the v1 -> v2 shadow write, the idempotent reconciler, unsigned checkpoints
with extends-proofs, and DEFAULT-OFF signing / publishing paths.

Tree (EIP-7864): 32-byte keys = 31-byte stem + 1-byte subindex; 256-wide stem
subtree; minimal internal nodes; empty = 0^32.  Hash profile "mag" = SHA-256
with one-byte domain tags (leaf 0x03, sub 0x04, stem 0x02, inner 0x01).

Key layout: ROW stem 0x00||u64be(i)||0^22 (index-ordered, insert-once);
SESSION stem 0x80||sha256("mag.v2.session\0"+sid)[:30]; META stem 0xC0||0^30.

Hard rules honoured here: this module NEVER writes memory/biography/* (v1 is
read-only to v2); it never reads memory/trajectory/*; signing needs
configs/mag.yaml chain_v2_signing: true AND env MAG_CHAIN_V2_SIGNING=1, an
existing seal key file and the pinned key_id; publishing needs
chain_v2_publish: true AND env MAG_CHAIN_V2_PUBLISH=1 and never runs git.
"""
from __future__ import annotations

import base64
import contextlib
import hashlib
import json
import os
import re
import stat
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional



ZERO = b"\x00" * 32
STEM_BITS = 248


# ---------------------------------------------------------------- hashing
class Hasher:
    def __init__(self, profile: str = "mag"):
        self.profile = profile
        if profile == "mag":
            self._H = lambda b: hashlib.sha256(b).digest()
        elif profile == "eip-sha256":
            self._H = lambda b: hashlib.sha256(b).digest()
        elif profile == "eip-blake3":
            from blake3 import blake3  # optional, test-only
            self._H = lambda b: blake3(b).digest()
        else:
            raise ValueError(profile)
        self.tagged = profile == "mag"

    def _eip(self, data: Optional[bytes]) -> bytes:
        if data is None or data == b"\x00" * 64:
            return ZERO
        assert len(data) in (32, 64)
        return self._H(data)

    def leaf(self, value: Optional[bytes]) -> bytes:
        if value is None:
            return ZERO
        return self._H(b"\x03" + value) if self.tagged else self._eip(value)

    def sub(self, l: bytes, r: bytes) -> bytes:
        if l == ZERO and r == ZERO:
            return ZERO
        return self._H(b"\x04" + l + r) if self.tagged else self._eip(l + r)

    def stem(self, stem: bytes, subroot: bytes) -> bytes:
        return self._H(b"\x02" + stem + subroot) if self.tagged else self._eip(stem + b"\x00" + subroot)

    def inner(self, l: bytes, r: bytes) -> bytes:
        return self._H(b"\x01" + l + r) if self.tagged else self._eip(l + r)


def stem_bit(stem_int: int, d: int) -> int:
    return (stem_int >> (STEM_BITS - 1 - d)) & 1


def h2s(h: bytes) -> str:
    """Proof JSON encoding: the empty hash is "0", others are 64 hex chars."""
    return "0" if h == ZERO else h.hex()


def s2h(s: str) -> bytes:
    if s == "0":
        return ZERO
    b = bytes.fromhex(s)
    if len(b) != 32:
        raise ValueError("hash must be 32 bytes")
    return b


# ---------------------------------------------------------------- nodes
class StemNode:
    __slots__ = ("stem", "si", "values", "h", "sub")

    def __init__(self, stem: bytes):
        self.stem = stem
        self.si = int.from_bytes(stem, "big")
        self.values: dict[int, bytes] = {}
        self.h: Optional[bytes] = None
        self.sub: Optional[list] = None  # cached levels of the 256-subtree


class InternalNode:
    __slots__ = ("left", "right", "h")

    def __init__(self):
        self.left = None
        self.right = None
        self.h: Optional[bytes] = None


def _subtree_levels(hs: Hasher, values: dict[int, bytes]) -> list[dict[int, bytes]]:
    """Sparse levels of the 256-wide stem subtree: levels[0] = leaves ... levels[8] = {0: root}."""
    lvl = {i: hs.leaf(v) for i, v in values.items()}
    levels = [lvl]
    for _ in range(8):
        nxt: dict[int, bytes] = {}
        for p in {i >> 1 for i in lvl}:
            h = hs.sub(lvl.get(2 * p, ZERO), lvl.get(2 * p + 1, ZERO))
            if h != ZERO:
                nxt[p] = h
        levels.append(nxt)
        lvl = nxt
    return levels


# ---------------------------------------------------------------- tree
class BinaryTree:
    def __init__(self, profile: str = "mag"):
        self.hs = Hasher(profile)
        self.root = None

    # -- writes
    def insert(self, key: bytes, value: bytes) -> None:
        assert len(key) == 32 and len(value) == 32
        stem, sub = key[:31], key[31]
        self.root = self._insert(self.root, stem, int.from_bytes(stem, "big"), sub, value, 0)

    def _insert(self, node, stem, si, sub, value, depth):
        if node is None:
            n = StemNode(stem)
            n.values[sub] = value
            return n
        if isinstance(node, StemNode):
            if node.si == si:
                node.values[sub] = value
                node.h = node.sub = None
                return node
            return self._split(node, stem, si, sub, value, depth)
        node.h = None
        assert depth < STEM_BITS
        if stem_bit(si, depth) == 0:
            node.left = self._insert(node.left, stem, si, sub, value, depth + 1)
        else:
            node.right = self._insert(node.right, stem, si, sub, value, depth + 1)
        return node

    def _split(self, existing: StemNode, stem, si, sub, value, depth):
        top = cur = InternalNode()
        while stem_bit(si, depth) == stem_bit(existing.si, depth):
            nxt = InternalNode()
            if stem_bit(si, depth) == 0:
                cur.left = nxt
            else:
                cur.right = nxt
            cur, depth = nxt, depth + 1
        new = StemNode(stem)
        new.values[sub] = value
        if stem_bit(si, depth) == 0:
            cur.left, cur.right = new, existing
        else:
            cur.left, cur.right = existing, new
        return top

    # -- reads
    def get(self, key: bytes) -> Optional[bytes]:
        si, node, d = int.from_bytes(key[:31], "big"), self.root, 0
        while isinstance(node, InternalNode):
            node = node.left if stem_bit(si, d) == 0 else node.right
            d += 1
        if isinstance(node, StemNode) and node.si == si:
            return node.values.get(key[31])
        return None

    def node_hash(self, node) -> bytes:
        if node is None:
            return ZERO
        if node.h is not None:
            return node.h
        if isinstance(node, StemNode):
            if node.sub is None:
                node.sub = _subtree_levels(self.hs, node.values)
            node.h = self.hs.stem(node.stem, node.sub[8].get(0, ZERO))
        else:
            node.h = self.hs.inner(self.node_hash(node.left), self.node_hash(node.right))
        return node.h

    def root_hash(self) -> bytes:
        return self.node_hash(self.root)

    def node_at(self, prefix_int: int, depth: int):
        """Node whose position is the first `depth` bits given in prefix_int (MSB-aligned in 248 bits)."""
        node, d = self.root, 0
        while d < depth:
            if not isinstance(node, InternalNode):
                return node, d  # stem pulled up above the requested depth (or empty)
            node = node.left if stem_bit(prefix_int, d) == 0 else node.right
            d += 1
        return node, d

    # -- proofs ---------------------------------------------------------
    def prove(self, present: Iterable[bytes] = (), absent: Iterable[bytes] = ()) -> dict:
        """Multiproof for present keys (values revealed) and absent keys (non-membership).

        Output (all hex in JSON form): {"keys": [...], "terminals": [...], "witness": [...]}
        terminals/witness are in DFS (left-first) order, consumed by verify().
        """
        present, absent = list(present), list(absent)
        for k in present:
            if self.get(k) is None:
                raise KeyError(f"key not present: {k.hex()}")
        for k in absent:
            if self.get(k) is not None:
                raise KeyError(f"key is present: {k.hex()}")
        claims: dict[bytes, list[int]] = {}
        for k in present + absent:
            claims.setdefault(k[:31], []).append(k[31])
        stems = sorted(claims, key=lambda s: int.from_bytes(s, "big"))
        terminals: list[dict] = []
        witness: list[bytes] = []
        self._gen(self.root, 0, [(int.from_bytes(s, "big"), s) for s in stems], claims, terminals, witness)
        return {"keys": [k.hex() for k in present + absent], "terminals": terminals,
                "witness": [h2s(w) for w in witness], "profile": self.hs.profile}

    def _gen(self, node, d, targets, claims, terminals, witness):
        if node is None:
            terminals.append({"depth": d, "kind": "empty"})
            return
        if isinstance(node, StemNode):
            subs = sorted({x for si, s in targets if si == node.si for x in claims[s]})
            if subs:
                if node.sub is None:
                    self.node_hash(node)
                terminals.append({"depth": d, "kind": "stem", "stem": node.stem.hex(),
                                  "values": {str(x): (node.values[x].hex() if x in node.values else None) for x in subs},
                                  "sub_witness": [h2s(h) for h in self._sub_witness(node, subs)]})
            else:
                self.node_hash(node)
                terminals.append({"depth": d, "kind": "foreign", "stem": node.stem.hex(),
                                  "subroot": node.sub[8].get(0, ZERO).hex()})
            return
        left = [t for t in targets if stem_bit(t[0], d) == 0]
        right = [t for t in targets if stem_bit(t[0], d) == 1]
        for side, child in ((left, node.left), (right, node.right)):
            if side:
                self._gen(child, d + 1, side, claims, terminals, witness)
            else:
                witness.append(self.node_hash(child))

    @staticmethod
    def _sub_witness(node: StemNode, subs: list[int]) -> list[bytes]:
        out: list[bytes] = []

        def rec(level: int, idx: int, ts: list[int]):  # level 8 = root ... 0 = leaves
            if level == 0:
                return
            l, r = [t for t in ts if (t >> (level - 1)) & 1 == 0], [t for t in ts if (t >> (level - 1)) & 1]
            for side, cidx in ((l, idx * 2), (r, idx * 2 + 1)):
                if side:
                    rec(level - 1, cidx, side)
                else:
                    out.append(node.sub[level - 1].get(cidx, ZERO))
        rec(8, 0, subs)
        return out


# ---------------------------------------------------------------- stateless verify
class ProofError(Exception):
    pass


def verify(root: bytes, proof: dict, profile: str = "mag") -> dict[bytes, Optional[bytes]]:
    """Verify a multiproof against `root`. Returns {key: value-or-None}; raises ProofError.

    Needs nothing but the proof and the root (no tree, no chain file)."""
    hs = Hasher(profile)
    if proof.get("profile", profile) != profile:
        raise ProofError("profile mismatch")
    keys = [bytes.fromhex(k) for k in proof["keys"]]
    if not keys or any(len(k) != 32 for k in keys) or len(set(keys)) != len(keys):
        raise ProofError("bad key list")
    claims: dict[bytes, set[int]] = {}
    for k in keys:
        claims.setdefault(k[:31], set()).add(k[31])
    targets = sorted((int.from_bytes(s, "big"), s) for s in claims)
    terms = list(proof["terminals"])
    wit = [s2h(w) for w in proof["witness"]]
    ti, wi = [0], [0]
    result: dict[bytes, Optional[bytes]] = {}

    def pop_w() -> bytes:
        if wi[0] >= len(wit):
            raise ProofError("witness exhausted")
        wi[0] += 1
        return wit[wi[0] - 1]

    def rec(d: int, ts) -> bytes:
        if d > STEM_BITS:
            raise ProofError("depth overflow")
        if ti[0] >= len(terms):
            raise ProofError("terminals exhausted")
        t = terms[ti[0]]
        if t["depth"] == d:
            ti[0] += 1
            kind = t["kind"]
            if kind == "empty":
                for _, s in ts:
                    for x in claims[s]:
                        result[s + bytes([x])] = None
                return ZERO
            stem = bytes.fromhex(t["stem"])
            if len(stem) != 31:
                raise ProofError("bad stem length")
            si = int.from_bytes(stem, "big")
            ref = ts[0][0]
            if d and (si >> (STEM_BITS - d)) != (ref >> (STEM_BITS - d)):
                raise ProofError("terminal stem not on the claimed path")
            if kind == "foreign":
                if any(s == stem for _, s in ts):
                    raise ProofError("foreign terminal equals a claimed stem")
                for _, s in ts:
                    for x in claims[s]:
                        result[s + bytes([x])] = None
                return hs.stem(stem, bytes.fromhex(t["subroot"]))
            if kind != "stem":
                raise ProofError("bad terminal kind")
            vals = {int(k): (bytes.fromhex(v) if v is not None else None) for k, v in t["values"].items()}
            for _, s in ts:
                if s == stem:
                    if set(vals) != claims[s]:
                        raise ProofError("opened suffixes != claimed suffixes")
                    for x, v in vals.items():
                        if v is not None and len(v) != 32:
                            raise ProofError("bad value length")
                        result[s + bytes([x])] = v
                else:  # other claimed stems that terminate here are absent
                    for x in claims[s]:
                        result[s + bytes([x])] = None
            if not any(s == stem for _, s in ts):
                raise ProofError("stem terminal without a matching claim")
            sw = [s2h(h) for h in t["sub_witness"]]
            si_ = [0]

            def srec(level: int, idx: int, subs: list[int]) -> bytes:
                if level == 0:
                    return hs.leaf(vals[idx])
                l = [x for x in subs if (x >> (level - 1)) & 1 == 0]
                r = [x for x in subs if (x >> (level - 1)) & 1]
                hh = []
                for side, cidx in ((l, idx * 2), (r, idx * 2 + 1)):
                    if side:
                        hh.append(srec(level - 1, cidx, side))
                    else:
                        if si_[0] >= len(sw):
                            raise ProofError("sub-witness exhausted")
                        hh.append(sw[si_[0]]); si_[0] += 1
                return hs.sub(hh[0], hh[1])
            subroot = srec(8, 0, sorted(vals))
            if si_[0] != len(sw):
                raise ProofError("unused sub-witness")
            return hs.stem(stem, subroot)
        if t["depth"] < d:
            raise ProofError("terminal above current depth")
        l = [x for x in ts if stem_bit(x[0], d) == 0]
        r = [x for x in ts if stem_bit(x[0], d) == 1]
        lh = rec(d + 1, l) if l else pop_w()
        rh = rec(d + 1, r) if r else pop_w()
        return hs.inner(lh, rh)

    got = rec(0, targets)
    if ti[0] != len(terms) or wi[0] != len(wit):
        raise ProofError("unused proof material")
    if got != root:
        raise ProofError("root mismatch")
    if set(result) != set(keys):
        raise ProofError("not every claimed key was resolved")
    return result


def proof_size_bytes(proof: dict) -> int:
    """Compact binary size: zero hashes cost one bitmap bit, others 32 bytes."""
    def hashes(lst):
        nz = sum(1 for h in lst if h not in ("0", ZERO.hex()))
        return 2 + (len(lst) + 7) // 8 + 32 * nz
    n = 2 + 32 * len(proof["keys"]) + hashes(proof["witness"])
    for t in proof["terminals"]:
        n += 2
        if t["kind"] == "foreign":
            n += 31 + 32
        elif t["kind"] == "stem":
            n += 31 + 1 + sum(1 + (32 if v is not None else 0) for v in t["values"].values())
            n += hashes(t["sub_witness"])
    return n



# ---------------------------------------------------------------- Mag v2 key layout
ROW_PREFIX, SESSION_PREFIX, META_PREFIX = 0x00, 0x80, 0xC0
ROW_INDEX_BITS = 71  # bits 1..71 of the stem: 7 zero bits + u64 index


def row_stem(i: int) -> bytes:
    return bytes([ROW_PREFIX]) + i.to_bytes(8, "big") + b"\x00" * 22


def session_stem(session_id: str) -> bytes:
    return bytes([SESSION_PREFIX]) + hashlib.sha256(b"mag.v2.session\x00" + session_id.encode()).digest()[:30]


META_STEM = bytes([META_PREFIX]) + b"\x00" * 30


def key(stem: bytes, sub: int) -> bytes:
    return stem + bytes([sub])


def u64v(x: int) -> bytes:
    return b"\x00" * 24 + int(x).to_bytes(8, "big")


# ---------------------------------------------------------------- append-only consistency
def _rows_hash(hs: Hasher, n_old: int, n: int, old_blocks: list[bytes], new_blocks: list[bytes]) -> bytes:
    """Hash of the depth-1 ROW subtree holding rows [0,n), rebuilt from block hashes.

    Ranges fully inside [0,n_old) are taken from old_blocks; ranges whose rows all lie
    in [n_old,n) (complete, or a single row) from new_blocks. Shape is a pure function of
    n because row stems are index-ordered (stem bits 1..71 = index)."""
    oi, ni = [0], [0]

    def pop(lst, ix):
        if ix[0] >= len(lst):
            raise ProofError("consistency blocks exhausted")
        ix[0] += 1
        return lst[ix[0] - 1]

    def rec(a: int, size: int) -> bytes:
        lo, hi = a, min(a + size, n)
        cnt = max(0, hi - lo)
        if cnt == 0:
            return ZERO
        if a + size <= n_old:
            return pop(old_blocks, oi)
        if lo >= n_old and (a + size <= n or cnt == 1):
            return pop(new_blocks, ni)
        if cnt == 1:  # single row < n_old inside a partial range: only when n == n_old
            return pop(old_blocks, oi)
        half = size // 2
        return hs.inner(rec(a, half), rec(a + half, half))

    h = rec(0, 1 << ROW_INDEX_BITS)
    if oi[0] != len(old_blocks) or ni[0] != len(new_blocks):
        raise ProofError("unused consistency blocks")
    return h


def prove_consistency(tree: BinaryTree, n_old: int, n_new: int, state_old: bytes,
                      state_new: Optional[bytes] = None) -> dict:
    """Prove root(n_new) extends root(n_old). state_old = the STATE (depth-1 right) subtree hash
    recorded when root(n_old) was published (session/meta state is mutable, rows are not).
    state_new defaults to the current tree's STATE subtree (n_new == current n); pass the
    recorded value to prove between two historical roots."""
    assert 1 <= n_old <= n_new
    old_blocks: list[bytes] = []
    new_blocks: list[bytes] = []

    def block_hash(a: int, size: int) -> bytes:
        if size == 1:
            node, _ = tree.node_at(int.from_bytes(row_stem(a), "big"), 1 + ROW_INDEX_BITS)
            assert isinstance(node, StemNode) and node.stem == row_stem(a)
            return tree.node_hash(node)
        depth = 1 + ROW_INDEX_BITS - (size.bit_length() - 1)
        node, d = tree.node_at(int.from_bytes(row_stem(a), "big"), depth)
        assert isinstance(node, InternalNode) and d == depth
        return tree.node_hash(node)

    def rec(a: int, size: int, n: int, sink_old, sink_new):
        lo, hi = a, min(a + size, n)
        cnt = max(0, hi - lo)
        if cnt == 0:
            return
        if a + size <= n_old:
            sink_old.append(block_hash(a, size)); return
        if lo >= n_old and (a + size <= n or cnt == 1):
            sink_new.append(block_hash(a, size) if cnt == size else block_hash(lo, 1)); return
        if cnt == 1:
            sink_old.append(block_hash(lo, 1)); return
        rec(a, size // 2, n, sink_old, sink_new); rec(a + size // 2, size // 2, n, sink_old, sink_new)

    rec(0, 1 << ROW_INDEX_BITS, n_new, old_blocks, new_blocks)
    root = tree.root
    assert isinstance(root, InternalNode)
    return {"n_old": n_old, "n_new": n_new, "old_blocks": [h.hex() for h in old_blocks],
            "new_blocks": [h.hex() for h in new_blocks], "state_old": state_old.hex(),
            "state_new": (state_new or tree.node_hash(root.right)).hex()}


def verify_consistency(root_old: bytes, root_new: bytes, proof: dict, profile: str = "mag") -> bool:
    hs = Hasher(profile)
    n_old, n_new = int(proof["n_old"]), int(proof["n_new"])
    if not (1 <= n_old <= n_new):
        raise ProofError("bad sizes")
    ob = [bytes.fromhex(h) for h in proof["old_blocks"]]
    nb = [bytes.fromhex(h) for h in proof["new_blocks"]]
    # old tree: every row is "old"
    rows_old = _rows_hash(hs, n_old, n_old, ob, [])
    if hs.inner(rows_old, bytes.fromhex(proof["state_old"])) != root_old:
        raise ProofError("old root mismatch")
    rows_new = _rows_hash(hs, n_old, n_new, ob, nb)
    if hs.inner(rows_new, bytes.fromhex(proof["state_new"])) != root_new:
        raise ProofError("new root mismatch")
    return True


# ================================================================ Mag v2 chain layer
try:  # repo root (same anchor verkle_knot uses); fallback keeps the module importable standalone
    from config import ROOT as _CFG_ROOT
    ROOT = Path(_CFG_ROOT)
except Exception:  # noqa: BLE001
    ROOT = Path(__file__).resolve().parents[1]

V1_BIO_DEFAULT = ROOT / "memory" / "biography"       # READ-ONLY to v2
V2_DIR_DEFAULT = ROOT / "memory" / "biography_v2"
SCHEMA_ROW = "mag_bintree_row.v2"
SCHEMA_TIP = "mag_bintree_tip.v2"
SCHEMA_PROOF = "mag_bintree_proof.v2"
SCHEMA_CHECKPOINT = "mag_bintree_checkpoint.v2"
SCHEMA_GENESIS = "mag_bintree_genesis.v2"
PINNED_SEAL_KEY_ID = "de5fc05e962c43ab"   # decision 6: same seal key as the Oct 15 restore seal
SEAL_KEY_DOMAIN = b"mag-seed-seal-pubkey:"  # == mag.seed_seal.KEY_DOMAIN (public key fingerprint)

KIND = {"genesis": 0, "knot": 1, "amend": 2, "seed_import": 3}
KIND_NAME = {v: k for k, v in KIND.items()}

# row subindexes (spec section 4)
SUB_HEADER, SUB_LEAF, SUB_SESSION, SUB_PREV_ROOT = 0, 1, 2, 3
SUB_SUPERSEDES, SUB_V1_INDEX, SUB_SUPERSEDED_LEAF = 4, 5, 6
SUB_FILENAME, SUB_DOSSIER, SUB_V1_LEAF, SUB_FLAGS, SUB_BODY_SHA = 7, 8, 9, 10, 11
FLAG_BODY_MISSING = 1     # v1 row points at a knot file that exists nowhere (leaf still committed)
FLAG_BODY_WITHHELD = 2    # knot body matched a secret pattern: hash committed, body NOT copied
FLAG_BODY_COPIED = 4      # immutable copy present under knots_v2/
V1_VOLATILE = ("index", "n_leaves", "parent_verkle_root", "verkle_root")


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False, default=str).encode("utf-8")


def sha(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def v1_merkle_root(leaf_hashes: list[str]) -> str:
    """Byte-identical port of mag.verkle_knot._merkle_root (legacy duplicate-last)."""
    if not leaf_hashes:
        return hashlib.sha256(b"empty").hexdigest()
    layer = list(leaf_hashes)
    while len(layer) > 1:
        nxt = []
        for i in range(0, len(layer), 2):
            l = layer[i]
            r = layer[i + 1] if i + 1 < len(layer) else l
            nxt.append(hashlib.sha256(b"node:" + l.encode() + b":" + r.encode()).hexdigest())
        layer = nxt
    return layer[0]


def header(version: int, kind: int, index: int, ts_ms: int, seq: int) -> bytes:
    return (bytes([version, kind]) + b"\x00" * 6 + index.to_bytes(8, "big")
            + int(ts_ms).to_bytes(8, "big") + int(seq).to_bytes(8, "big"))


def hexval(h: Optional[str]) -> Optional[bytes]:
    """32-byte value for a hex-ish field: raw if it is 64 hex chars, else sha256 of the text."""
    if not h:
        return None
    try:
        b = bytes.fromhex(str(h))
        return b if len(b) == 32 else sha(str(h).encode())
    except ValueError:
        return sha(str(h).encode())


def ts_to_ms(ts: Any) -> int:
    try:
        s = str(ts).replace("Z", "+00:00")
        return max(0, int(datetime.fromisoformat(s).timestamp() * 1000))
    except Exception:  # noqa: BLE001
        return 0


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def v1_row_stable(row: dict) -> dict:
    """The v1 row minus the root bookkeeping that later v1 amends rewrite (index, n_leaves,
    parent_verkle_root, verkle_root). What v2 commits is the row CONTENT."""
    return {k: v for k, v in row.items() if k not in V1_VOLATILE}


def v1_row_leaf(row: dict) -> bytes:
    return sha(b"mag.v2.v1row:" + canonical_json(v1_row_stable(row)))


def session_key_of(row: dict) -> str:
    sid = row.get("session_id")
    return str(sid) if sid not in (None, "") else "file:" + str(row.get("filename") or "")


def session_commit(sid: str) -> bytes:
    return sha(b"mag.v2.sid\x00" + sid.encode("utf-8"))


def impl_fingerprint(root: Path | None = None) -> bytes:
    """Decision 7 code fingerprint: sha256 over the LF-normalised bytes of the v2 code."""
    base = Path(root) if root else ROOT
    h = hashlib.sha256(b"mag.v2.impl\x00")
    for rel in ("mag/bintree_v2.py", "scripts/verify_knot_v2.py", "scripts/freeze_v1_seed.py",
                "scripts/catchup_v2.py"):
        p = base / rel
        data = p.read_bytes().replace(b"\r\n", b"\n") if p.is_file() else b"<absent>"
        h.update(rel.encode() + b"\x00" + hashlib.sha256(data).digest())
    return h.digest()


# ---------------------------------------------------------------- secret scan (decision: body_withheld)
_SECRET_PATTERNS = [
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("sk_token", re.compile(r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{20,}")),
    ("xai_key", re.compile(r"\bxai-[A-Za-z0-9]{20,}")),
    ("github_token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
    ("aws_access_key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("slack_token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("google_api_key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("assigned_secret", re.compile(
        r"(?i)[\"']?\b(?:api[_-]?key|secret[_-]?key|client[_-]?secret|access[_-]?token|auth[_-]?token|"
        r"password|passwd|private[_-]?key|bearer)\b[\"']?\s*[:=]\s*[\"']?(?:Bearer\s+)?[A-Za-z0-9/+_.\-]{16,}")),
    ("trajectory_steps_ref", re.compile(r"trajectory[/\\]+steps\.jsonl")),
]


def secret_scan(data: bytes) -> list[str]:
    """Names of the secret patterns that hit (NEVER the matched values)."""
    text = data.decode("utf-8", errors="replace")
    return [name for name, rx in _SECRET_PATTERNS if rx.search(text)]


# ---------------------------------------------------------------- in-memory chain
class Chain:
    """v2 chain state: append-only rows + mutable SESSION / META state, all in one tree."""

    def __init__(self, profile: str = "mag"):
        self.profile = profile
        self.tree = BinaryTree(profile)
        self.n = 0
        self.rows: list[dict] = []           # log entries (what chain_v2.jsonl holds)
        self.sessions: dict[str, dict] = {}  # sid -> {index, v1_leaf, seq}

    # -- core
    def state_hash(self) -> bytes:
        r = self.tree.root
        return self.tree.node_hash(r.right) if isinstance(r, InternalNode) else ZERO

    def root(self) -> bytes:
        return self.tree.root_hash()

    @property
    def chain_id(self) -> Optional[str]:
        return self.rows[0]["root_after"] if self.rows else None

    def _apply(self, i: int, vals: dict[int, bytes], session_id: Optional[str]) -> None:
        stem = row_stem(i)
        if self.tree.get(key(stem, SUB_HEADER)) is not None:
            raise RuntimeError(f"row {i} already written (insert-once law)")
        for s, v in sorted(vals.items()):
            self.tree.insert(key(stem, s), v)
        if session_id is not None:
            ss = session_stem(session_id)
            if self.tree.get(key(ss, 3)) is None:
                self.tree.insert(key(ss, 3), u64v(i))
            seq = int.from_bytes(vals[SUB_HEADER][24:32], "big")
            self.tree.insert(key(ss, 0), u64v(i))
            self.tree.insert(key(ss, 1), vals[SUB_LEAF])
            self.tree.insert(key(ss, 2), u64v(seq))
            if SUB_V1_LEAF in vals:
                self.tree.insert(key(ss, 4), vals[SUB_V1_LEAF])
            self.sessions[session_id] = {"index": i, "seq": seq,
                                         "v1_leaf": vals[SUB_V1_LEAF].hex() if SUB_V1_LEAF in vals else None}
        self.tree.insert(key(META_STEM, 0), u64v(i + 1))
        self.tree.insert(key(META_STEM, 1), vals[SUB_LEAF])
        self.n = i + 1

    def append(self, kind: str, values: dict[int, bytes], session_id: Optional[str],
               ts_ms: int = 0, meta: Optional[dict] = None) -> dict:
        i = self.n
        prev_root = self.root() if i else None
        seq = 0
        if session_id is not None:
            cur = self.sessions.get(session_id)
            seq = (cur["seq"] + 1) if cur else 1
        vals = dict(values)
        vals[SUB_HEADER] = header(2, KIND[kind], i, ts_ms, seq)
        if prev_root is not None:
            vals[SUB_PREV_ROOT] = prev_root
        if session_id is not None:
            vals[SUB_SESSION] = session_commit(session_id)
        self._apply(i, vals, session_id)
        root = self.root()
        entry = {"schema": SCHEMA_ROW, "index": i, "kind": kind, "session_id": session_id,
                 "ts_ms": int(ts_ms)}
        entry.update(meta or {})
        entry["kv"] = {str(s): v.hex() for s, v in sorted(vals.items())}
        entry["root_after"] = root.hex()
        entry["state_after"] = self.state_hash().hex()
        self.rows.append(entry)
        return entry

    def replay(self, entries: Iterable[dict], verify_each: bool = False) -> None:
        for e in entries:
            i = int(e["index"])
            if i != self.n:
                raise ValueError(f"row log out of order: got {i}, expected {self.n}")
            vals = {int(s): bytes.fromhex(v) for s, v in e["kv"].items()}
            hdr = vals.get(SUB_HEADER)
            if not hdr or hdr[0] != 2 or int.from_bytes(hdr[8:16], "big") != i:
                raise ValueError(f"row {i}: bad header")
            if i and vals.get(SUB_PREV_ROOT, b"").hex() != self.rows[-1]["root_after"]:
                raise ValueError(f"row {i}: prev_root does not link to row {i - 1}")
            sid = e.get("session_id")
            if sid is not None and vals.get(SUB_SESSION) != session_commit(sid):
                raise ValueError(f"row {i}: session commitment mismatch")
            self._apply(i, vals, sid)
            self.rows.append(e)
            if verify_each and self.root().hex() != e["root_after"]:
                raise ValueError(f"row {i}: root_after mismatch")
        if self.rows and self.root().hex() != self.rows[-1]["root_after"]:
            raise ValueError("replayed root != logged root_after of the last row")

    # -- builders
    def genesis(self, v1_root: str, n_seed: int, manifest_sha: bytes, chain_sha: bytes,
                last_leaf: str, seal_root: bytes, restore_sha: bytes, impl_sha: bytes,
                ts_ms: int = 0, meta: Optional[dict] = None, doc_extra: Optional[dict] = None) -> dict:
        doc = {"schema": SCHEMA_GENESIS, "v1_root": v1_root, "n_seed": n_seed,
               "manifest_sha256": manifest_sha.hex(), "chain_sha256": chain_sha.hex(),
               "restore_sha256": restore_sha.hex(), "impl_sha256": impl_sha.hex()}
        if doc_extra:  # committed via the genesis leaf (sub 1); e.g. seed_source, rewritten rows
            doc.update(doc_extra)
        vals = {SUB_LEAF: sha(b"mag.v2.genesis:" + canonical_json(doc)), 64: bytes.fromhex(v1_root),
                65: u64v(n_seed), 66: manifest_sha, 67: chain_sha, 68: bytes.fromhex(last_leaf),
                69: seal_root, 70: restore_sha, 71: impl_sha}
        m = {"genesis": doc}
        m.update(meta or {})
        return self.append("genesis", vals, None, ts_ms=ts_ms, meta=m)

    def v1_values(self, v1_row: dict, v1_index: Optional[int], flags: int,
                  body_sha: Optional[bytes]) -> dict[int, bytes]:
        vals = {SUB_LEAF: v1_row_leaf(v1_row),
                SUB_FILENAME: sha(str(v1_row.get("filename") or "").encode("utf-8")),
                SUB_V1_LEAF: hexval(v1_row.get("leaf_hash")) or ZERO,
                SUB_FLAGS: u64v(flags)}
        if v1_index is not None:
            vals[SUB_V1_INDEX] = u64v(int(v1_index))
        dc = hexval(v1_row.get("dossier_commit"))
        if dc:
            vals[SUB_DOSSIER] = dc
        if body_sha is not None:
            vals[SUB_BODY_SHA] = body_sha
        return vals

    def append_v1(self, v1_row: dict, v1_index: Optional[int], flags: int = 0,
                  body_sha: Optional[bytes] = None, seed: bool = False, extra: Optional[dict] = None) -> dict:
        sid = session_key_of(v1_row)
        vals = self.v1_values(v1_row, v1_index, flags, body_sha)
        cur = self.sessions.get(sid)
        if seed:
            kind = "seed_import"
        elif cur is None:
            kind = "knot"
        else:
            kind = "amend"
            vals[SUB_SUPERSEDES] = u64v(cur["index"])
            vals[SUB_SUPERSEDED_LEAF] = bytes.fromhex(self.rows[cur["index"]]["kv"][str(SUB_LEAF)])
        meta = {"v1_index": v1_index, "filename": v1_row.get("filename"),
                "flags": flags, "v1_row": v1_row_stable(v1_row)}
        meta.update(extra or {})
        return self.append(kind, vals, sid, ts_ms=ts_to_ms(v1_row.get("ts")), meta=meta)

    # -- proofs
    def row_keys(self, i: int) -> list[bytes]:
        return [key(row_stem(i), int(s)) for s in self.rows[i]["kv"]]

    def prove_row(self, i: int, with_length: bool = True, extra_rows=()) -> dict:
        present = self.row_keys(i)
        for j in extra_rows:
            present += self.row_keys(j)
        absent = []
        if with_length:
            present.append(key(META_STEM, 0))
            absent.append(key(row_stem(self.n), 0))
        return self.tree.prove(present, absent)

    def prove_session(self, sid: str) -> dict:
        """Current-state proof for one session (latest index + leaf), or its non-membership."""
        ss = session_stem(sid)
        if self.tree.get(key(ss, 0)) is None:
            return self.tree.prove([], [key(ss, 0)])
        return self.tree.prove([key(ss, s) for s in (0, 1, 2, 3) if self.tree.get(key(ss, s)) is not None])

    def extends_proof(self, n_old: int, state_old_hex: str) -> dict:
        return prove_consistency(self.tree, n_old, self.n, bytes.fromhex(state_old_hex))


# ---------------------------------------------------------------- flags / policy
def _policy() -> dict:
    try:
        from mag.policy import load_policy
        p = load_policy()
        return p if isinstance(p, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def _flag(env_name: str, policy_key: str) -> bool:
    env = os.environ.get(env_name)
    if env is not None and env.strip():
        return env.strip().lower() in ("1", "true", "yes", "on")
    return bool(_policy().get(policy_key, False))


def shadow_enabled() -> bool:
    """configs/mag.yaml chain_v2_shadow (default false); env MAG_CHAIN_V2_SHADOW overrides."""
    return _flag("MAG_CHAIN_V2_SHADOW", "chain_v2_shadow")


def signing_enabled() -> bool:
    """BOTH configs/mag.yaml chain_v2_signing: true AND env MAG_CHAIN_V2_SIGNING=1."""
    return bool(_policy().get("chain_v2_signing", False)) and os.environ.get("MAG_CHAIN_V2_SIGNING") == "1"


def publish_enabled() -> bool:
    """BOTH configs/mag.yaml chain_v2_publish: true AND env MAG_CHAIN_V2_PUBLISH=1."""
    return bool(_policy().get("chain_v2_publish", False)) and os.environ.get("MAG_CHAIN_V2_PUBLISH") == "1"


# ---------------------------------------------------------------- persistence
def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp{os.getpid()}")
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def read_jsonl_complete(path: Path) -> tuple[list[dict], int]:
    """Rows of a JSONL file, ignoring a torn (newline-less) last line. Returns (rows, torn_or_bad)."""
    data = path.read_bytes()
    lines = data.split(b"\n")
    bad = 0
    if lines and lines[-1].strip():
        bad += 1  # torn tail: a writer is mid-append
    out = []
    for ln in lines[:-1]:
        if not ln.strip():
            continue
        try:
            out.append(json.loads(ln.decode("utf-8")))
        except ValueError:
            bad += 1
    return out, bad


class Store:
    """memory/biography_v2/ layout. v1 paths are only ever READ."""

    def __init__(self, base: Path | str | None = None, v1_bio: Path | str | None = None,
                 knot_dirs: Optional[list] = None):
        self.base = Path(base or os.environ.get("MAG_BINTREE_V2_DIR") or V2_DIR_DEFAULT)
        self.v1_bio = Path(v1_bio or os.environ.get("MAG_BINTREE_V1_BIO") or V1_BIO_DEFAULT)
        self.knot_dirs = ([Path(d) for d in knot_dirs] if knot_dirs
                          else [self.v1_bio / "knots", self.v1_bio / "knots_attic"])
        self.chain = self.base / "chain_v2.jsonl"
        self.tip = self.base / "tip_v2.json"
        self.knots = self.base / "knots_v2"
        self.seed = self.base / "seed"
        self.checkpoints = self.base / "checkpoints_v2.jsonl"
        self.mismatch = self.base / "shadow_mismatch.jsonl"
        self.lock = self.base / ".bintree_v2.lock"

    # -- v1 (read-only)
    @property
    def v1_chain(self) -> Path:
        return self.v1_bio / "verkle_chain.jsonl"

    def find_v1_knot(self, filename: Optional[str]) -> Optional[Path]:
        if not filename or "/" in str(filename) or "\\" in str(filename) or ".." in str(filename):
            return None
        for d in self.knot_dirs:
            p = d / str(filename)
            if p.is_file():
                return p
        return None

    # -- state
    def exists(self) -> bool:
        return self.tip.is_file() and self.chain.is_file()

    def read_tip(self) -> Optional[dict]:
        try:
            return json.loads(self.tip.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    def load(self, verify_each: bool = False, repair_tip: bool = True) -> Chain:
        ch = Chain()
        if not self.chain.is_file():
            return ch
        rows, bad = read_jsonl_complete(self.chain)
        if bad:
            raise ValueError(f"v2 row log has {bad} unparsable/torn line(s) - refusing to build on it")
        ch.replay(rows, verify_each=verify_each)
        if ch.n and ch.rows[0].get("kind") != "genesis":
            raise ValueError("v2 row log does not start with a genesis row")
        tip0 = self.read_tip()
        if tip0 and int(tip0.get("n", 0)) > ch.n:
            raise ValueError(f"v2 tip says n={tip0.get('n')} but the row log holds {ch.n} rows")
        tip = self.read_tip()
        if repair_tip and tip and (int(tip.get("n", -1)) != ch.n or tip.get("root") != ch.root().hex()):
            # tip lags a completed log append (crash between the two): the log is the truth
            self.write_tip(ch)
        return ch

    def append_entries(self, entries: list[dict]) -> None:
        if not entries:
            return
        self.base.mkdir(parents=True, exist_ok=True)
        with open(self.chain, "a", encoding="utf-8", newline="") as fh:
            for e in entries:
                fh.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
            fh.flush()
            os.fsync(fh.fileno())

    def write_tip(self, ch: Chain) -> dict:
        tip = {"schema": SCHEMA_TIP, "chain_id": ch.chain_id, "n": ch.n, "root": ch.root().hex(),
               "state_hash": ch.state_hash().hex(), "profile": ch.profile, "updated": now_iso(),
               "last_kind": ch.rows[-1]["kind"] if ch.rows else None}
        _atomic_write_text(self.tip, json.dumps(tip, indent=2) + "\n")
        return tip

    def log_mismatch(self, rec: dict) -> None:
        try:
            self.base.mkdir(parents=True, exist_ok=True)
            rec = {"ts": now_iso(), **rec}
            with open(self.mismatch, "a", encoding="utf-8", newline="") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False, default=str) + "\n")
        except Exception:  # noqa: BLE001 - logging must never raise into a v1 write
            pass

    # -- knot bodies (decision 8: v2 keeps its own immutable copies)
    def read_body(self, src: Optional[Path]) -> tuple[int, Optional[bytes], Optional[bytes], list[str]]:
        """(flags, body_sha, bytes_to_copy, secret_pattern_names) for a v1 knot file."""
        if src is None or not Path(src).is_file():
            return FLAG_BODY_MISSING, None, None, []
        data = Path(src).read_bytes()
        hits = secret_scan(data)
        if hits:
            return FLAG_BODY_WITHHELD, sha(data), None, hits
        return FLAG_BODY_COPIED, sha(data), data, []

    def knot_copy_path(self, index: int, filename: Optional[str]) -> Path:
        safe = re.sub(r"[^A-Za-z0-9._-]+", "-", str(filename or "knot"))[:120]
        return self.knots / f"{index:08d}__{safe}"

    def write_knot_copy(self, index: int, filename: Optional[str], data: bytes) -> Path:
        p = self.knot_copy_path(index, filename)
        self.knots.mkdir(parents=True, exist_ok=True)
        if p.exists():
            if p.read_bytes() != data:
                raise RuntimeError(f"immutable knot copy {p.name} exists with different bytes")
            return p
        tmp = p.with_name(p.name + ".tmp")
        tmp.write_bytes(data)
        os.replace(tmp, p)
        try:
            os.chmod(p, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
        except OSError:
            pass
        return p

    # -- checkpoints
    def last_checkpoint(self) -> Optional[dict]:
        if not self.checkpoints.is_file():
            return None
        rows, _ = read_jsonl_complete(self.checkpoints)
        return rows[-1] if rows else None


# ---------------------------------------------------------------- v2 lock (same heartbeat law as v1)
@contextlib.contextmanager
def v2_lock(store: Store, timeout: float = 60.0):
    """Single-writer lock for memory/biography_v2. Reuses verkle_knot's heartbeat helpers so a
    lock is only ever broken same-host with a stale heartbeat. Distinct file from the v1 lock."""
    try:
        from mag import verkle_knot as _vk
    except Exception:  # noqa: BLE001
        _vk = None
    store.base.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(str(store.lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if _vk is not None:
                    rec = _vk.read_lock_record(store.lock)
                    stale = _vk.lock_breakable(rec) if rec else (time.time() - store.lock.stat().st_mtime > 900)
                else:
                    stale = time.time() - store.lock.stat().st_mtime > 900
                if stale:
                    store.lock.unlink()
            except OSError:
                pass
            if time.time() > deadline:
                raise TimeoutError(f"bintree_v2 lock timeout after {timeout}s")
            time.sleep(0.05)
    import threading
    guard = threading.Lock()
    alive = [True]

    def _write(rec: dict) -> None:
        data = json.dumps(rec).encode("utf-8")
        with guard:
            if not alive[0]:
                return
            os.lseek(fd, 0, os.SEEK_SET)
            os.write(fd, data)
            os.ftruncate(fd, len(data))

    stop = None
    try:
        if _vk is not None:
            _write(_vk.lock_record())
            stop, _ = _vk.start_lock_heartbeat(_write)
        else:
            _write({"pid": os.getpid(), "heartbeat_ts": time.time()})
        yield
    finally:
        if stop is not None:
            stop.set()
        with guard:
            alive[0] = False
            os.close(fd)
        try:
            store.lock.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------- mirroring v1 -> v2
def mirror_v1_row(store: Store, ch: Chain, row: dict, v1_index: Optional[int],
                  knot_path: Optional[Path] = None, source: str = "catchup") -> dict:
    """Append ONE v1 row to v2 unless that session's latest v1 leaf is already mirrored.
    Caller holds v2_lock. Order: log line -> tip -> knot copy (a crash leaves v2 behind, healed
    by the next catchup; it never leaves a half row)."""
    if ch.n == 0 or ch.rows[0].get("kind") != "genesis":
        raise RuntimeError("v2 chain has no genesis - refusing to mirror")
    leaf = row.get("leaf_hash")
    if not leaf:
        return {"skipped": "no_leaf_hash"}
    sid = session_key_of(row)
    cur = ch.sessions.get(sid)
    if cur is not None and cur.get("v1_leaf") == (hexval(leaf) or ZERO).hex():
        return {"skipped": "already_mirrored", "index": cur["index"]}
    src = Path(knot_path) if knot_path else store.find_v1_knot(row.get("filename"))
    flags, body_sha, body, hits = store.read_body(src)
    entry = ch.append_v1(row, v1_index, flags=flags, body_sha=body_sha,
                         extra={"source": source, "withheld_patterns": len(hits) if hits else 0})
    try:
        store.append_entries([entry])
    except Exception:
        # roll the in-memory chain back so the cache never runs ahead of disk
        _CACHE.pop(str(store.base), None)
        raise
    store.write_tip(ch)
    if body is not None:
        try:
            store.write_knot_copy(entry["index"], row.get("filename"), body)
        except Exception as e:  # noqa: BLE001
            store.log_mismatch({"event": "knot_copy_failed", "index": entry["index"], "error": type(e).__name__})
    return {"appended": entry["index"], "kind": entry["kind"], "flags": flags, "root": entry["root_after"]}


_CACHE: dict[str, Chain] = {}


def _cached_chain(store: Store) -> Chain:
    """Per-process tree cache; rebuilt from the row log whenever the tip moved under us."""
    tip = store.read_tip() or {}
    ch = _CACHE.get(str(store.base))
    if ch is not None and tip.get("n") == ch.n and tip.get("root") == ch.root().hex():
        return ch
    ch = store.load()
    _CACHE[str(store.base)] = ch
    return ch


def shadow_append(row: dict, knot_path: Any = None, store: Optional[Store] = None) -> Optional[dict]:
    """v1 -> v2 shadow write, called by verkle_knot AFTER the v1 append + tip write complete.
    Inert unless shadow_enabled(). Never raises; problems go to shadow_mismatch.jsonl."""
    if not shadow_enabled():
        return None
    st = store or Store()
    try:
        if not st.exists():
            st.log_mismatch({"event": "no_v2_genesis", "note": "run scripts/freeze_v1_seed.py first",
                             "session_id": row.get("session_id")})
            return None
        with v2_lock(st, timeout=10.0):
            ch = _cached_chain(st)
            res = mirror_v1_row(st, ch, dict(row), row.get("index"),
                                knot_path=Path(knot_path) if knot_path else None, source="shadow")
        return res
    except Exception as e:  # noqa: BLE001
        _CACHE.pop(str(st.base), None)
        st.log_mismatch({"event": "shadow_error", "error": type(e).__name__, "msg": str(e)[:300],
                         "session_id": row.get("session_id"), "leaf_hash": row.get("leaf_hash")})
        return None


def reconcile(store: Store, v1_chain: Optional[Path] = None, check_only: bool = False) -> dict:
    """Idempotent catch-up: for every v1 session, its LAST v1 row must be the session's latest v2
    v1-leaf. Reads the v1 chain WITHOUT the v1 lock (a torn tail line is ignored)."""
    if not store.exists():
        return {"ok": False, "error": "no v2 genesis (seed not frozen) - run scripts/freeze_v1_seed.py"}
    path = Path(v1_chain) if v1_chain else store.v1_chain
    rows, bad = read_jsonl_complete(path)
    last: dict[str, tuple[int, dict]] = {}
    for pos, r in enumerate(rows):
        if r.get("leaf_hash"):
            last[session_key_of(r)] = (pos, r)

    def pending_for(ch: Chain):
        out = []
        for sid, (pos, r) in last.items():
            cur = ch.sessions.get(sid)
            if cur is None or cur.get("v1_leaf") != (hexval(r["leaf_hash"]) or ZERO).hex():
                out.append((pos, r))
        return sorted(out, key=lambda t: t[0])

    rep = {"ok": True, "v1_rows": len(rows), "v1_unparsed_or_torn": bad, "v1_sessions": len(last)}
    if check_only:
        ch = store.load(repair_tip=False)
        pend = pending_for(ch)
        rep.update({"n": ch.n, "root": ch.root().hex(), "pending": len(pend),
                    "pending_new_sessions": sum(1 for _, r in pend if session_key_of(r) not in ch.sessions),
                    "v2_sessions_absent_from_v1": sum(1 for s in ch.sessions if s not in last and s is not None)})
        return rep
    appended = []
    with v2_lock(store, timeout=120.0):
        ch = store.load()
        for pos, r in pending_for(ch):
            res = mirror_v1_row(store, ch, r, r.get("index", pos), source="catchup")
            if "appended" in res:
                appended.append(res)
        _CACHE[str(store.base)] = ch
        rep.update({"n": ch.n, "root": ch.root().hex(), "appended": len(appended),
                    "kinds": {k: sum(1 for a in appended if a["kind"] == k) for k in ("knot", "amend")},
                    "body_missing": sum(1 for a in appended if a["flags"] & FLAG_BODY_MISSING),
                    "body_withheld": sum(1 for a in appended if a["flags"] & FLAG_BODY_WITHHELD)})
    return rep


# ---------------------------------------------------------------- proofs for export
def build_proof(store: Store, ch: Chain, i: int, full: bool = False,
                checkpoint: Optional[dict] = None) -> dict:
    """Decision 8: hash-only by default; full=True embeds the v1 row content and, when an
    immutable copy exists (not withheld), the knot body (base64)."""
    if not (0 <= i < ch.n):
        raise IndexError(i)
    doc = {"schema": SCHEMA_PROOF, "profile": ch.profile, "chain_id": ch.chain_id,
           "root": ch.root().hex(), "index": i, "n": ch.n, "mode": "full" if full else "hash",
           "proof": ch.prove_row(i)}
    if checkpoint is not None:
        if checkpoint.get("root") != doc["root"] or int(checkpoint.get("n", -1)) != ch.n:
            raise ValueError("checkpoint does not attest this root/n")
        doc["checkpoint"] = checkpoint
    if full:
        e = ch.rows[i]
        if "v1_row" in e:
            doc["v1_row"] = e["v1_row"]
        if int(e.get("flags") or 0) & FLAG_BODY_COPIED:
            p = store.knot_copy_path(i, e.get("filename"))
            if p.is_file():
                doc["knot_body_b64"] = base64.b64encode(p.read_bytes()).decode("ascii")
    return doc


# ---------------------------------------------------------------- checkpoints (decision 6)
def checkpoint_payload(cp: dict) -> bytes:
    """Signed message = sha256 hex (utf-8) of the canonical attestation fields, mirroring
    seed_seal (which signs seed_root.encode())."""
    fields = {k: cp.get(k) for k in ("schema", "chain_id", "n", "root", "state_hash",
                                      "prev_checkpoint_root", "prev_checkpoint_n")}
    return hashlib.sha256(canonical_json(fields)).hexdigest().encode("utf-8")


def make_checkpoint(store: Store, ch: Chain, write: bool = True, sign: bool = False) -> dict:
    prev = store.last_checkpoint()
    if prev and int(prev["n"]) == ch.n and prev["root"] == ch.root().hex():
        return prev
    cp = {"schema": SCHEMA_CHECKPOINT, "chain_id": ch.chain_id, "n": ch.n, "root": ch.root().hex(),
          "state_hash": ch.state_hash().hex(), "ts": now_iso(),
          "prev_checkpoint_root": prev["root"] if prev else None,
          "prev_checkpoint_n": int(prev["n"]) if prev else None,
          "extends_proof": ch.extends_proof(int(prev["n"]), prev["state_hash"]) if prev else None,
          "signature": None, "key_id": None, "public_key": None, "sig_alg": None,
          "status": "unsigned-pending-operator"}
    cp["payload_sha256_hex"] = checkpoint_payload(cp).decode()
    if sign:
        cp = sign_checkpoint(cp)
    if write:
        store.base.mkdir(parents=True, exist_ok=True)
        with open(store.checkpoints, "a", encoding="utf-8", newline="") as fh:
            fh.write(json.dumps(cp, sort_keys=True) + "\n")
    return cp


class SigningDisabled(RuntimeError):
    pass


def sign_checkpoint(cp: dict, key_file: Optional[Path] = None) -> dict:
    """DEFAULT OFF. Signs with the existing seal key ONLY when signing_enabled(), the key file
    already exists (seed_seal would silently mint a new one) and its key_id is the pinned one."""
    if not signing_enabled():
        raise SigningDisabled("chain_v2_signing is off (needs mag.yaml chain_v2_signing: true "
                              "AND env MAG_CHAIN_V2_SIGNING=1)")
    kf = Path(key_file) if key_file else ROOT / "state" / "keys" / "seed_seal_key"
    if not kf.is_file():  # checked BEFORE seed_seal is touched: load_signing_key would mint a new key
        raise RuntimeError("seal key file absent - refusing (would mint a new key)")
    from mag import seed_seal
    k = seed_seal.load_signing_key(kf)
    if not k.get("ok"):
        raise RuntimeError("seal key unusable")
    pub = seed_seal._pubkey_raw(k["key"])
    kid = seed_seal.key_id_for(pub)
    if kid != PINNED_SEAL_KEY_ID:
        raise RuntimeError(f"seal key_id {kid} != pinned {PINNED_SEAL_KEY_ID} - refusing")
    out = dict(cp)
    out["signature"] = k["key"].sign(checkpoint_payload(cp)).hex()
    out.update({"key_id": kid, "public_key": pub.hex(), "sig_alg": "ed25519", "status": "signed"})
    return out


def publish_checkpoint(cp: dict, falsifier_dir: Optional[Path] = None) -> Path:
    """DEFAULT OFF. Drops a SIGNED checkpoint into falsifier-index/evidence/chain_v2/.
    Never runs git: committing/pushing stays with the operator."""
    if not publish_enabled():
        raise RuntimeError("chain_v2_publish is off (needs mag.yaml chain_v2_publish: true "
                           "AND env MAG_CHAIN_V2_PUBLISH=1)")
    if cp.get("status") != "signed" or not cp.get("signature"):
        raise RuntimeError("refusing to publish an unsigned checkpoint")
    d = Path(falsifier_dir or (ROOT / "falsifier-index")) / "evidence" / "chain_v2"
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"checkpoint_{int(cp['n']):08d}.json"
    if p.exists():
        raise RuntimeError(f"{p.name} already published")
    _atomic_write_text(p, json.dumps(cp, indent=2, sort_keys=True) + "\n")
    return p


def _key_id_for(pub: bytes) -> str:
    return hashlib.sha256(SEAL_KEY_DOMAIN + pub).hexdigest()[:16]
