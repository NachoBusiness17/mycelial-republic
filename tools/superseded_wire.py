#!/usr/bin/env python3
"""superseded_wire.py - the demotion register as graph facts (2026-10-07, lane
m6-graph-supersession of morning-block-20261007; R5 next-loop target 2).

memory/fold_history/SUPERSEDED.md rows were prose only. This wire appends, per
register row, ONE node pair joined by ONE superseded_by edge into
memory/knowledge_graph.json:

  superseded:row-<n>  kind superseded, outcome falsified, carries
                      superseded_by=<replacement node id> + the evidence cell
  superseder:row-<n>  kind superseder, the replacing truth
  edge {from: superseded:row-<n>, to: superseder:row-<n>, rel: superseded_by,
        text: <evidence cell>}

Parsing/minting lives in mag/knowledge_graph.py (_superseded_wire) so a graph
build() regenerates the same facts from the register (collector-kind law).
This tool exists because a rebuild also WIPES manually appended edges
(measured 2026-10-07 on a copy: 117 why_context edges -> 0 after build()), so
the d04 graph_heal-style append-only approach cannot be the whole wire - the
collector half in mag/knowledge_graph.py is the durable half, this is the
apply-to-live-graph half. Amend-only: never rewrites or removes existing
nodes/edges. Idempotent: node ids and (from,to,rel) edge keys dedupe, a
second pass adds zero. --dry reports and writes nothing. Exit 0 = ran;
exit 2 = cannot verify (missing/corrupt graph or a missing/unparseable
register) - fail-closed, never a guess.

Usage: python tools/superseded_wire.py [--root PATH] [--graph PATH]
       [--register PATH] [--dry] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag import knowledge_graph as kg  # noqa: E402  (path bootstrap above)


class WireError(Exception):
    """Fail-closed: cannot verify inputs (graph or register unusable)."""


def load_graph(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            g = json.load(f)
    except (OSError, ValueError) as exc:
        raise WireError(f"cannot load graph {path}: {exc}") from exc
    if not isinstance(g, dict) or not isinstance(g.get("nodes"), list) \
            or not isinstance(g.get("edges"), list):
        raise WireError(f"graph {path} lacks nodes/edges lists")
    return g


def plan(g: dict, register: Path) -> tuple[list[dict], list[dict], dict]:
    """Pure: what a real pass would add, given the graph and register bytes."""
    mint_nodes, mint_edges = kg._superseded_wire(register)
    if not mint_nodes:
        raise WireError(f"register {register} parsed to zero rows - "
                        f"cannot verify the demotion register")
    node_ids = {n["id"] for n in g["nodes"]}
    edge_keys = {(e.get("from"), e.get("to"), e.get("rel"))
                 for e in g["edges"]}
    new_nodes = [n for n in mint_nodes if n["id"] not in node_ids]
    new_edges = [e for e in mint_edges
                 if (e["from"], e["to"], e["rel"]) not in edge_keys]
    already = {"nodes": len(mint_nodes) - len(new_nodes),
               "edges": len(mint_edges) - len(new_edges)}
    return new_nodes, new_edges, already


def save_graph(g: dict, path: Path) -> None:
    """Atomic in-place write preserving the compact single-line shape
    (same discipline as tools/graph_heal.save_graph)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(g, f, ensure_ascii=False, default=str)
    os.replace(tmp, path)


def _report(g: dict, register: Path, new_nodes: list[dict],
            new_edges: list[dict], already: dict, dry: bool) -> dict:
    return {
        "mode": "dry" if dry else "apply",
        "register": str(register),
        "graph_ts": g.get("ts", ""),
        "rows": len(new_nodes) // 2 + already["nodes"] // 2,
        "add_nodes": len(new_nodes),
        "add_edges": len(new_edges),
        "already_present": already,
        "samples": [f"{e['from']} -[{e['rel']}]-> {e['to']}"
                    for e in new_edges[:6]],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=ROOT,
                    help="repo root (default: inferred from this file)")
    ap.add_argument("--graph", type=Path, default=None,
                    help="graph path (default: <root>/memory/knowledge_graph.json)")
    ap.add_argument("--register", type=Path, default=None,
                    help="register path (default: <root>/memory/fold_history/SUPERSEDED.md)")
    ap.add_argument("--dry", action="store_true",
                    help="report the plan, write nothing")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="machine-readable report")
    args = ap.parse_args(argv)

    graph_path = args.graph or (args.root / "memory" / "knowledge_graph.json")
    register = args.register or kg.superseded_register_path()
    try:
        g = load_graph(graph_path)
        new_nodes, new_edges, already = plan(g, register)
    except WireError as exc:
        print(f"RESULT: FAIL {exc}", file=sys.stderr)
        return 2

    if args.dry:
        report = _report(g, register, new_nodes, new_edges, already, dry=True)
        print(json.dumps(report, ensure_ascii=False, indent=2)
              if args.as_json else _human(report))
        print("RESULT: DRY rows=%d add_nodes=%d add_edges=%d"
              % (report["rows"], len(new_nodes), len(new_edges)))
        return 0

    g["nodes"].extend(new_nodes)
    g["edges"].extend(new_edges)
    save_graph(g, graph_path)
    report = _report(g, register, new_nodes, new_edges, already, dry=False)
    print(json.dumps(report, ensure_ascii=False, indent=2)
          if args.as_json else _human(report))
    print("RESULT: PASS wired_edges=%d add_nodes=%d graph_nodes=%d graph_edges=%d"
          % (len(new_edges), len(new_nodes), len(g["nodes"]), len(g["edges"])))
    return 0


def _human(r: dict) -> str:
    lines = [
        "superseded_wire (%s) register=%s graph_ts=%s"
        % (r["mode"], r["register"], r["graph_ts"]),
        "WIRE    rows=%d add_nodes=%d add_edges=%d already_present=%s"
        % (r["rows"], r["add_nodes"], r["add_edges"], r["already_present"]),
    ]
    lines += ["  edge: " + s for s in r["samples"]]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
