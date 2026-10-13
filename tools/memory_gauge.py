"""nightly memory gauge (ask A8).

Builds an undirected graph from memory/knowledge_graph.json
(schema knowledge_graph.v2: {"nodes": [{id, ...}], "edges": [{from, to, ...}]}),
computes:
  beta0   -- number of connected components (union-find)
  orphans -- number of degree-0 vertices (touched by no edge)
and appends exactly one JSON line to watch/inbox/MEMORY_GAUGE.jsonl.

Vertex semantics: vertices = declared node ids (nodes[].id, deduped) UNION
every endpoint referenced by an edge. Endpoints referenced by edges but absent
from nodes[] are counted separately as "implied_nodes" so the line shows how
much of the graph lives only inside edges. Orphans can only be declared nodes
that no edge touches (implied endpoints always have degree >= 1).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KG_PATH = ROOT / "memory" / "knowledge_graph.json"
OUT_PATH = ROOT / "watch" / "inbox" / "MEMORY_GAUGE.jsonl"


def load_graph(path: Path) -> tuple[set[str], list[tuple[str, str]], int]:
    """Return (declared node ids, undirected edge pairs, duplicate-entry count)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    nodes = data.get("nodes") or []
    edges = data.get("edges") or []
    declared: set[str] = set()
    dups = 0
    for n in nodes:
        nid = n.get("id")
        if nid is None:
            continue
        if nid in declared:
            dups += 1
        declared.add(nid)
    pairs: list[tuple[str, str]] = []
    for e in edges:
        a, b = e.get("from"), e.get("to")
        if a is None or b is None:
            continue
        pairs.append((a, b))
    return declared, pairs, dups


def beta0(vertices: set[str], pairs: list[tuple[str, str]]) -> int:
    """Connected-component count via union-find with path compression."""
    parent = {v: v for v in vertices}

    def find(x: str) -> str:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:  # compress
            parent[x], x = root, parent[x]
        return root

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    return len({find(v) for v in vertices})


def main() -> None:
    declared, pairs, dup_entries = load_graph(KG_PATH)
    endpoints = {x for pair in pairs for x in pair}
    implied = endpoints - declared
    vertices = declared | endpoints
    degree = dict.fromkeys(vertices, 0)
    for a, b in pairs:
        degree[a] += 1
        degree[b] += 1
    orphans = sum(1 for v in vertices if degree[v] == 0)
    line = json.dumps(
        {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "source": "memory/knowledge_graph.json",
            "nodes": len(declared),
            "duplicate_node_entries": dup_entries,
            "implied_nodes": len(implied),
            "edges": len(pairs),
            "beta0": beta0(vertices, pairs),
            "orphans": orphans,
        },
        separators=(",", ":"),
    )
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()
