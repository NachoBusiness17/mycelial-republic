"""MERKLE CURE, SOLVER B (2026-10-07): subtree-size node binding.

Lane p4b-merkle-cure, the mesh's second arm (independent implementation).
Wound: mag/verkle_knot.py::_merkle_root duplicates the last node at every
odd level, so [a,b,c] and [a,b,c,c] build byte-identical roots — proven live
in watch/inbox/MERKLE_COLLISION_PROOF_20261007.md (COLLISION True, root
922f2912c926141c…). Solver A shipped the receipt's Option A (leaf-position
binding, MAG_POSITION_BOUND_LEAVES, in verkle_knot.py itself). THIS module is
the receipt's Option B in its deep form: bind the SUBTREE LEAF COUNT into
every internal node hash,

    node:<size>:<left>:<right>      (size = leaves under the node)

so the length ambiguity dies at EVERY internal node, not just at the tip:
the padded tail-leaf of [a,b,c] folds into a size-1 padding pair
(node:1:c:c) while an explicit fourth leaf folds into a size-2 pair
(node:2:c:c), and the roots bind 3 vs 4. Content forgery stays blocked by
the unchanged b"leaf:" leaf domain — this cure never touches leaf hashing,
so every stored leaf_hash, knot_rehash_patrol and verkle_dangling_repair
stay coherent even with the cure active (solver A's flag must stay OFF for
new leaf-domain hashing until a full re-hash; the two cures are independent
and composable).

Selector: MAG_MERKLE_SIZED=1 marks the sized binding as the estate's chosen
Merkle law (fail-closed: any other value or unset = legacy). Flag OFF, this
module is INERT — the live chain's stored legacy roots verify unchanged and
nothing here is consulted by verkle_knot. Flag ON does not migrate history
by itself: run migrate_chain_to_sized() once, under quiescence, to rewrite
every row's verkle_root/parent_verkle_root plus the tip into sized form
(the documented migration path; it refuses unless the chain is consistent
under its current binding first — the sanctioned healer stays
verkle_knot.repair_tip_if_consistent).

Honest residual (named for the fold): verkle_knot's append writer still
writes legacy roots; after a sized migration the legacy integrity gate
refuses further appends (fail-closed, never silent forking) until the
append seam is wired to the sized prefix roots — that wiring is the fold's
decision to make, not this arm's unilateral edit to solver A's file.
Pure-function core + migration verb + O(log n) inclusion proofs, pinned by
tests/test_merkle_cure_p4b_sized.py.
"""
from __future__ import annotations

import contextlib
import json
import os
from typing import Any

from mag import verkle_knot as vk

MERKLE_SIZED_ENV = "MAG_MERKLE_SIZED"

_MERKLE_SIZED_TRUTHY = {"1", "true", "yes", "on"}

BINDING_NAME = "subtree-size"


def sized_mode() -> bool:
    """Read MAG_MERKLE_SIZED (default OFF, fail-closed to legacy).

    Mirrors verkle_knot.position_bound_leaves()' flag grammar: any value
    outside the truthy set keeps the estate on the legacy binding.
    """
    return os.environ.get(MERKLE_SIZED_ENV, "").strip().lower() in _MERKLE_SIZED_TRUTHY


def sized_node_hash(left: str, right: str, size: int) -> str:
    """Internal node hash with the subtree leaf count bound into the domain."""
    return vk._h(b"node:" + str(int(size)).encode("ascii") + b":" + left.encode() + b":" + right.encode())


def sized_merkle_root(leaf_hashes: list[str]) -> str:
    """Naive reference root over the sized tree.

    Padding law: an odd layer's last node pairs with a DUPLICATE of itself
    and the duplicate adds ZERO leaves (the pair's subtree still holds one
    real leaf). That is exactly the property the legacy tree lacks: under
    legacy hashing the padding pair and an explicit equal-content pair are
    indistinguishable; here the size domain separates node:1:c:c from
    node:2:c:c. Same genesis and single-leaf semantics as the legacy root
    (empty -> H(b"empty"), one leaf -> the leaf hash itself).
    """
    if not leaf_hashes:
        return vk._h(b"empty")
    layer: list[tuple[str, int]] = [(h, 1) for h in leaf_hashes]
    while len(layer) > 1:
        nxt: list[tuple[str, int]] = []
        for i in range(0, len(layer), 2):
            left_h, left_size = layer[i]
            if i + 1 < len(layer):
                right_h, right_size = layer[i + 1]
                size = left_size + right_size
            else:
                right_h, size = left_h, left_size  # padding dup adds zero leaves
            nxt.append((sized_node_hash(left_h, right_h, size), size))
        layer = nxt
    return layer[0][0]


def sized_merkle_prefix_roots(leaf_hashes: list[str]) -> list[str]:
    """Root for every non-empty prefix, O(n log n) total (the writer's math).

    Binary forest of complete (hash, size, height) subtrees; heights descend
    strictly left to right, so a right fold with self-duplication lifts a
    shorter suffix — the lift is the padding dup (size unchanged, the
    duplicate adds zero leaves), byte-equivalent to sized_merkle_root for
    every prefix. Brute-force parity across n=0..64 is pinned by
    tests/test_merkle_cure_p4b_sized.py (the writer must never drift from
    the verifier's naive recomputation).
    """
    if not leaf_hashes:
        return []

    forest: list[tuple[str, int, int]] = []  # (hash, size, height)
    roots: list[str] = []
    for leaf in leaf_hashes:
        forest.append((leaf, 1, 0))
        while len(forest) >= 2 and forest[-1][2] == forest[-2][2]:
            right_h, right_s, height = forest.pop()
            left_h, left_s, _ = forest.pop()
            forest.append((sized_node_hash(left_h, right_h, left_s + right_s),
                           left_s + right_s, height + 1))

        cur_h, cur_s, cur_height = forest[-1]
        for left_h, left_s, left_height in reversed(forest[:-1]):
            while cur_height < left_height:
                cur_h = sized_node_hash(cur_h, cur_h, cur_s)  # lift = padding dup
                cur_height += 1
            cur_h = sized_node_hash(left_h, cur_h, left_s + cur_s)
            cur_s = left_s + cur_s
            cur_height = left_height + 1
        roots.append(cur_h)
    return roots


class SizedVerkleProof:
    """Membership proof over a sized-bound chain: index + siblings -> root.

    verify() reconstructs the root with subtree sizes derived from
    ``n_leaves`` (the count IS the position binding, so it is mandatory —
    fail-closed False when omitted, unlike the legacy root-only check) and
    matches the committed root. Padding joins are recomputed, never trusted
    from the path: a padded tail node duplicates itself at unchanged size.
    """

    def __init__(self, index: int, leaf_hash: str, path: list[str], root: str) -> None:
        self.index = index
        self.leaf_hash = leaf_hash
        self.path = path  # sibling subtree hashes, bottom-up
        self.root = root

    def verify(self, leaf_obj: Any | None = None, leaf_hash: str | None = None,
               n_leaves: int | None = None) -> bool:
        h = leaf_hash or (vk._leaf_hash(leaf_obj) if leaf_obj is not None else self.leaf_hash)
        if h != self.leaf_hash:
            return False
        if n_leaves is None:
            return False  # the count is the binding; a countless proof proves nothing
        n = int(n_leaves)
        if n < 1 or not (0 <= self.index < n):
            return False
        depth = (n - 1).bit_length()
        if len(self.path) != depth:
            return False
        idx = self.index
        size = 1
        for step in range(depth):
            shift = 1 << step
            level_len = (n + shift - 1) >> step  # ceil(n / 2**step) nodes at this level
            sib = self.path[step]
            # idx IS the node position at this level (halved each iteration).
            if idx % 2 == 0 and idx == level_len - 1 and level_len % 2 == 1:
                # padded tail: the node duplicates itself, count unchanged
                h = sized_node_hash(h, h, size)
            else:
                pshift = shift << 1
                psize = max(1, min(pshift, n - ((idx >> 1) << (step + 1))))
                if idx % 2 == 0:
                    h = sized_node_hash(h, sib, psize)
                else:
                    h = sized_node_hash(sib, h, psize)
                size = psize
            idx //= 2
        return h == self.root


def prove_sized(index: int | None = None) -> dict[str, Any]:
    """O(log n) inclusion proof over the knot chain's leaves, sized binding.

    Reads the chain through verkle_knot (no side effects); mirrors the
    prove() result shape plus ``binding``. Padded siblings carry the node's
    own hash (verify recomputes padding joins and ignores the path value).
    """
    leaves = vk._leaf_hashes_in_order()
    if not leaves:
        return {"ok": False, "error": "no verkle leaves committed yet"}
    idx = index if index is not None else len(leaves) - 1
    if not (0 <= idx < len(leaves)):
        return {"ok": False, "error": f"index {idx} out of range (0..{len(leaves)-1})"}
    root = sized_merkle_root(leaves)
    layers: list[list[tuple[str, int]]] = [[(h, 1) for h in leaves]]
    while len(layers[-1]) > 1:
        layer = layers[-1]
        nxt: list[tuple[str, int]] = []
        for i in range(0, len(layer), 2):
            left_h, left_s = layer[i]
            if i + 1 < len(layer):
                right_h, right_s = layer[i + 1]
                nxt.append((sized_node_hash(left_h, right_h, left_s + right_s),
                            left_s + right_s))
            else:
                nxt.append((sized_node_hash(left_h, left_h, left_s), left_s))
        layers.append(nxt)
    path: list[str] = []
    i = idx
    for layer in layers[:-1]:
        # sibling position is i^1; a padded tail carries its own hash
        # (verify recomputes padding joins and never trusts this value)
        if i % 2 == 0:
            path.append(layer[i + 1][0] if i + 1 < len(layer) else layer[i][0])
        else:
            path.append(layer[i - 1][0])
        i //= 2
    proof = SizedVerkleProof(index=idx, leaf_hash=leaves[idx], path=path, root=root)
    return {
        "ok": True,
        "index": idx,
        "n_leaves": len(leaves),
        "leaf_hash": leaves[idx],
        "path": path,
        "root": root,
        "binding": BINDING_NAME,
        "verified": proof.verify(n_leaves=len(leaves)),
    }


def verify_chain_consistent_sized() -> tuple[bool, str]:
    """Sized-binding twin of verkle_knot._verify_chain_consistent (the gate).

    Recomputes the sized root over ALL leaves and requires the last row's
    committed root, the tip root and the tip n_leaves to match. For a chain
    still carrying legacy roots this refuses with a named migration hint —
    the two bindings are mutually exclusive by design (never silently fork).
    """
    rows = vk._load_chain_rows()
    if not rows:
        return True, "empty chain (genesis ok)"
    hashes = [r.get("leaf_hash") for r in rows if r.get("leaf_hash")]
    if not hashes:
        return True, "no leaf hashes yet"
    expect = sized_merkle_root(hashes)
    if rows[-1].get("verkle_root") != expect:
        return False, (f"last row root mismatch under {BINDING_NAME} binding "
                       f"(committed {str(rows[-1].get('verkle_root'))[:16]} vs "
                       f"recomputed {expect[:16]}; legacy chain? run "
                       "merkle_sized.migrate_chain_to_sized() or keep MAG_MERKLE_SIZED off)")
    try:
        tip = json.loads(vk.TIP.read_text(encoding="utf-8")) if vk.TIP.is_file() else None
    except (OSError, json.JSONDecodeError):
        tip = None
    if not isinstance(tip, dict) or not tip:
        return False, (f"tip missing or unreadable on a non-empty chain "
                       f"(expected sized root {expect[:16]}..., {len(hashes)} leaves)")
    if tip.get("root") != expect:
        return False, f"tip root mismatch (tip {str(tip.get('root'))[:16]} vs recomputed {expect[:16]})"
    if tip.get("n_leaves") != len(hashes):
        return False, f"tip n_leaves mismatch (tip {tip.get('n_leaves')} vs recomputed {len(hashes)})"
    return True, f"chain consistent under {BINDING_NAME} binding ({len(hashes)} leaves)"


def migrate_chain_to_sized() -> dict[str, Any]:
    """Rewrite every row's verkle_root/parent_verkle_root + the tip, sized.

    The documented Option-B migration path. Under the single-writer lock it
    FIRST proves the chain is consistent under its CURRENT (legacy) binding
    — a chain that fails that must be healed by verkle_knot's sanctioned
    repair, never papered over — then recomputes every prefix root with the
    sized math (byte-exact LF chain law: tmp + os.replace, same contract as
    verkle_knot._rewrite_chain) and rewrites the tip atomically with
    ``merkle_binding: subtree-size`` stamped in. Refuses (mutating nothing)
    on an empty chain, a legacy-inconsistent chain, or when the gate cannot
    be re-proved after the rewrite.
    """
    with vk.verkle_lock():
        rows = vk._load_chain_rows()
        hashes = [str(r["leaf_hash"]) for r in rows if r.get("leaf_hash")]
        if not hashes:
            return {"ok": False, "migrated": False,
                    "error": "empty chain: nothing to migrate"}
        legacy_root = vk._merkle_root(hashes)
        if rows[-1].get("verkle_root") != legacy_root:
            return {"ok": False, "migrated": False,
                    "error": ("chain inconsistent under its current (legacy) binding; "
                              "heal via verkle_knot.repair_tip_if_consistent first"),
                    "n_leaves": len(hashes)}
        prefix = sized_merkle_prefix_roots(hashes)
        out_rows: list[dict[str, Any]] = []
        hash_i = 0
        for i, row in enumerate(rows):
            if not row.get("leaf_hash"):
                continue
            row = dict(row)
            row["index"] = i
            row["n_leaves"] = hash_i + 1
            row["parent_verkle_root"] = prefix[hash_i - 1] if hash_i else vk._h(b"empty")
            row["verkle_root"] = prefix[hash_i]
            out_rows.append(row)
            hash_i += 1
        payload = ("\n".join(json.dumps(r) for r in out_rows)
                   + ("\n" if out_rows else "")).encode("utf-8")
        tmp = vk.CHAIN.with_name(f"{vk.CHAIN.name}.{os.getpid()}.migrate.tmp")
        try:
            tmp.write_bytes(payload)
            os.replace(tmp, vk.CHAIN)
        finally:
            with contextlib.suppress(OSError):
                tmp.unlink()
        root = prefix[-1]
        tip = vk._tip_for_tail(out_rows, hashes, root)
        tip["merkle_binding"] = BINDING_NAME
        vk._write_tip_atomic(tip)
        ok, why = verify_chain_consistent_sized()
        return {"ok": ok, "migrated": ok, "from": "legacy", "to": BINDING_NAME,
                "n_leaves": len(hashes), "root": root, "verify": why}
