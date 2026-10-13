"""dirac_loop tests — the topological problem-solving organ.

Pins the laws on KNOWN graphs (rank math you can do by hand), the invariant's
order-independence, and the closed/open classification. The organ walks the
live operational graph; these tests pin the MATH it must get right anywhere.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mag.dirac_loop as dl  # noqa: E402


def _mkloop(n: int) -> tuple[list[dict], list[dict]]:
    """A single n-cycle: n vertices, n edges (beta1 = 1 by hand)."""
    ids = [f"n{i}" for i in range(n)]
    nodes = [{"id": i, "kind": "organ", "label": i} for i in ids]
    edges = [{"from": ids[i], "to": ids[(i + 1) % n]} for i in range(n)]
    return nodes, edges


def test_rank_single_cycle_beta1_one():
    nodes, edges = _mkloop(4)
    n = len(dl._all_vertices(nodes, edges))
    c = dl._components(edges, dl._all_vertices(nodes, edges))
    assert len(edges) - n + c == 1, "a square has exactly one independent loop"


def test_rank_figure8_beta1_two():
    """Two triangles sharing one vertex: 6 edges, 5 vertices, 1 component."""
    ids = ["hub", "a", "b", "c", "d", "e"]
    nodes = [{"id": i, "kind": "organ", "label": i} for i in ids]
    edges = [
        {"from": "hub", "to": "a"}, {"from": "a", "to": "b"}, {"from": "b", "to": "hub"},
        {"from": "hub", "to": "c"}, {"from": "c", "to": "d"}, {"from": "d", "to": "hub"},
    ]
    n = len(dl._all_vertices(nodes, edges))
    c = dl._components(edges, ids)
    assert 6 - n + c == 2, "figure-8 has two independent loops"


def test_tree_has_zero_loops():
    nodes, edges = _mkloop(4)
    tree_edges = edges[:3]  # drop the closing edge -> a path (tree)
    n = len(dl._all_vertices(nodes, tree_edges))
    c = dl._components(tree_edges, dl._all_vertices(nodes, tree_edges))
    assert len(tree_edges) - n + c == 0, "a tree has no cycles"


def test_fundamental_cycles_finds_the_closing_edge():
    nodes, edges = _mkloop(4)
    fc = dl.fundamental_cycles.__wrapped__ if hasattr(dl.fundamental_cycles, "__wrapped__") else None
    # exercise the machinery directly on a synthetic graph via monkeypatched loader
    import mag.dirac_loop as m
    orig = m._graph
    m._graph = lambda scope="operational": (nodes, edges)
    try:
        fc = m.fundamental_cycles()
    finally:
        m._graph = orig
    assert len(fc["loops"]) == 1, "one non-tree edge -> one fundamental cycle"
    loop = fc["loops"][0]
    assert set(loop["path"]) == {"n0", "n1", "n2", "n3"}, (
        "the cycle path visits every vertex of the square")


def test_invariant_order_and_dupe_independent():
    a = dl.loop_invariant(["pack", "audit", "swarm"])
    b = dl.loop_invariant(["swarm", "audit", "pack"])
    c = dl.loop_invariant(["pack", "pack", "audit", "swarm", "swarm"])
    assert a == b, "traversal order must not change the invariant"
    assert a == c, "duplicate membership must not change the invariant (set semantics)"


def test_scan_classifies_closed_vs_open():
    import mag.dirac_loop as m
    nodes, edges = _mkloop(3)
    orig_graph = m._graph
    orig_known = m._known_invariants
    m._graph = lambda scope="operational": (nodes, edges)
    # pre-hold this exact loop's invariant: known set built the same way scan does
    labels = [str(x) for x in ("n0", "n1", "n2")]
    held = {dl.loop_invariant(labels)}
    m._known_invariants = lambda scope="operational": held
    try:
        scan = m.scan()
    finally:
        m._graph = orig_graph
        m._known_invariants = orig_known
    assert scan["closed_solved"] == 1 and scan["open_gaps"] == 0, (
        "a loop whose invariant is already in the lattice is CLOSED (tesuji)")


def test_dangling_endpoints_count_as_vertices():
    """The ancestor's own law: every edge endpoint is a vertex even when no
    node carries it (invariant:/module: targets), or components disagree."""
    nodes: list[dict] = [{"id": "a", "kind": "organ", "label": "a"}]
    edges = [{"from": "a", "to": "invariant:thing"}, {"from": "invariant:thing", "to": "a"}]
    ids = dl._all_vertices(nodes, edges)
    assert "invariant:thing" in ids, "dangling endpoint must enter the vertex set"
    c = dl._components(edges, ids)
    assert len(edges) - len(ids) + c == 1, "a dangling 2-cycle is still beta1=1"


def test_pack_offload_emits_shed_sections_when_pack_overflows(tmp_path):
    """format_context_pack_text must emit a PACK_OFFLOAD.jsonl row naming
    the shed sections when the rendered pack exceeds max_chars."""
    import json
    import mag.context_pack as cp

    offload = tmp_path / "PACK_OFFLOAD.jsonl"
    orig = cp.PACK_OFFLOAD_FILE
    cp.PACK_OFFLOAD_FILE = offload
    try:
        pack = cp.build_context_pack(mode="build")
        text = cp.format_context_pack_text(pack, mode="build", max_chars=80)
        assert len(text) <= 80 + 30, f"pack not clipped: {len(text)} chars"

        rows = [json.loads(l) for l in offload.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert rows, "at least one offload row emitted when pack overflowed"
        for r in rows:
            assert r["schema"] == "pack_offload.v1", f"bad schema: {r}"
            assert isinstance(r["shed_sections"], list) and r["shed_sections"], f"no shed sections: {r}"
            assert isinstance(r["stage"], int) and 1 <= r["stage"] <= 4, f"bad stage: {r}"

        all_sheds = set()
        for r in rows:
            all_sheds.update(r["shed_sections"])
        assert "hard clip" in all_sheds, f"hard clip stage missing from: {all_sheds}"
    finally:
        cp.PACK_OFFLOAD_FILE = orig
