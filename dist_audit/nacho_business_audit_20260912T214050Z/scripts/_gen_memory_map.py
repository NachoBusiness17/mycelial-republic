"""_gen_memory_map.py — emit a browsable snapshot of knowledge_graph.json for memory_map.html.

Operator (2026-08-15): surface the existing 1,572-node knowledge graph as a sane, seeable map (the
memory is mapped; the map just isn't visible). This generator reads memory/knowledge_graph.json and
writes memory_graph_data.js — real bytes, categorized, relational.

Schema: _gen_memory_map.v1 · deterministic + $0 · read-only (never mutates the graph)
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "memory" / "knowledge_graph.json"
OUT = ROOT / "memory_graph_data.js"

MAX_NODES = 1500


def main() -> None:
    g = json.loads(GRAPH.read_text(encoding="utf-8", errors="replace"))
    nodes = (g.get("nodes") or [])[:MAX_NODES]
    edges = g.get("edges") or []
    slim_nodes = []
    for n in nodes:
        slim_nodes.append({
            "id": str(n.get("id") or n.get("label") or n.get("name") or "?"),
            "label": str(n.get("label") or n.get("name") or n.get("id") or "?"),
            "kind": str(n.get("kind") or n.get("type") or "?"),
            "source": str(n.get("source") or "")[:120],
        })
    slim_edges = []
    for e in edges[:1000]:
        slim_edges.append({"from": str(e.get("from") or e.get("src") or e.get("source") or ""),
                           "to": str(e.get("to") or e.get("dst") or e.get("target") or ""),
                           "rel": str(e.get("rel") or e.get("label") or "")[:40]})
    js = "// AUTO-GENERATED from memory/knowledge_graph.json (mag/knowledge_graph.py). Real bytes.\n"
    js += "const MEMORY_GRAPH = " + json.dumps({"nodes": slim_nodes, "edges": slim_edges}, ensure_ascii=False) + ";\n"
    OUT.write_text(js, encoding="utf-8")
    print(f"wrote {OUT.name}: {len(slim_nodes)} nodes, {len(slim_edges)} edges")


if __name__ == "__main__":
    main()
