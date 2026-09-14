#!/usr/bin/env python
"""edg_compiler.py — STRACE steal: compile watch/room.jsonl into an Execution Dependency Graph.

Parses room rows into EDG nodes, builds typed heuristic edges (references /
follows / executes), marks failure nodes, and slices the "guilty neighborhood"
(causal slice, <=2 hops, capped) per failure. Stdlib only. Measure, never
repair: corrupt rows become counted orphans (HarnessEval discipline).
"""
import json
import re
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOM = REPO / "watch" / "room.jsonl"
OUTDIR = REPO / "memory" / "runs" / "edg"

FOLLOW_WINDOW = 20       # rows
SLICE_HOPS = 2
SLICE_CAP = 10
FAIL_WORDS = re.compile(r"\b(fail|fails|failed|violation|violations|refused|disputed)\b", re.IGNORECASE)
SLUG = re.compile(r"[A-Z][A-Z0-9]+(?:[_+][A-Z0-9]+)+")


def parse_room(path):
    nodes, corrupt = {}, []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                corrupt.append(lineno)
                continue
            # spec attrs with honest fallbacks to the real schema
            nodes[lineno] = {
                "id": lineno,
                "ts": d.get("ts", ""),
                "thread": d.get("thread", ""),
                "type": d.get("type") or d.get("event", ""),
                "seat": d.get("seat", ""),
                "item": d.get("item", ""),
                "gist": d.get("gist") or d.get("text") or "",
                "file": d.get("file", ""),
            }
    return nodes, corrupt


def norm_slug(s):
    """INTAKE_X_20260904 (from a filename mention) and item INTAKE_X are the same thing."""
    return re.sub(r"[_+]\d{6,8}(T\d{4,6}Z?)?$", "", s)


def build_edges(nodes):
    edges = []  # (src, dst, kind)
    by_item = {}  # item slug -> [ids]

    def register(slug, nid):
        by_item.setdefault(norm_slug(slug), []).append(nid)

    for nid, n in nodes.items():
        if n["item"]:
            register(n["item"], nid)
        for m in SLUG.findall(n["gist"] + " " + n["file"]):
            if m != n["item"]:
                register(m, nid)

    # (a) item reference: row mentions another row's item slug -> mentioned -> mentioner
    for nid, n in nodes.items():
        hay = n["gist"] + " " + n["file"]
        for m in set(norm_slug(x) for x in SLUG.findall(hay)):
            if m == norm_slug(n["item"]):
                continue
            for mid in by_item.get(m, []):
                if mid != nid:
                    edges.append((mid, nid, "references"))

    # (b) thread continuation: same thread + same item within FOLLOW_WINDOW rows
    rows = sorted(nodes.items())
    for i, (nid, n) in enumerate(rows):
        if not (n["thread"] and n["item"]):
            continue
        for j in range(i + 1, len(rows)):
            oid, o = rows[j]
            if oid - nid > FOLLOW_WINDOW:
                break
            if o["thread"] == n["thread"] and o["item"] and norm_slug(o["item"]) == norm_slug(n["item"]):
                edges.append((nid, oid, "follows"))

    # (c) build-receipt: receipt row's item matches a card row's item -> card -> receipt
    for rid, r in nodes.items():
        if r["type"] != "receipt" or not r["item"]:
            continue
        for cid, c in nodes.items():
            if (c["item"] == r["item"] or norm_slug(c["item"]) == norm_slug(r["item"])) and c["type"] == "card" and cid != rid:
                edges.append((cid, rid, "executes"))
    return edges


def is_failure(n):
    if n["type"] == "correction":
        return True
    return bool(FAIL_WORDS.search(n["gist"]))


def causal_slice(fail_id, adj):
    """Guilty neighborhood: nodes within SLICE_HOPS of the failure, both directions."""
    seen, frontier = {fail_id}, {fail_id}
    for _ in range(SLICE_HOPS):
        nxt = set()
        for nid in frontier:
            nxt |= adj[nid] - seen
        seen |= nxt
        frontier = nxt
        if not frontier:
            break
    seen.discard(fail_id)
    return sorted(seen)[:SLICE_CAP]


def main():
    nodes, corrupt = parse_room(ROOM)
    edges = build_edges(nodes)
    adj = {i: set() for i in nodes}
    for s, d, _k in edges:
        adj[s].add(d)
        adj[d].add(s)
    failures = sorted(i for i, n in nodes.items() if is_failure(n))

    by_kind = {}
    for _s, _d, k in edges:
        by_kind[k] = by_kind.get(k, 0) + 1

    print("=== EDG (STRACE steal) over watch/room.jsonl ===")
    print("nodes: %d | edges: %d (by type: %s)" % (len(nodes), len(edges), by_kind))
    print("corrupt rows (graph orphans): %d at lines %s" % (len(corrupt), corrupt))
    print("failure nodes: %d" % len(failures))
    print()
    # headline the most-connected slices first (a slice with no edges is an orphan, not a diagnosis)
    shown = sorted(failures, key=lambda i: (-len(adj[i]), i))[:3]
    for fid in shown:
        n = nodes[fid]
        print("SLICE for node %d [%s/%s] seat=%s item=%s" % (fid, n["thread"], n["type"], n["seat"], n["item"]))
        print("  gist: %s" % n["gist"][:160].replace("\n", " "))
        sids = causal_slice(fid, adj)
        print("  guilty neighborhood (%d, cap %d): %s" % (len(sids), SLICE_CAP, sids))
        for sid in sids:
            s = nodes[sid]
            print("    <- %d [%s/%s] %s" % (sid, s["thread"], s["type"], s["gist"][:100].replace("\n", " ")))
        print()

    OUTDIR.mkdir(parents=True, exist_ok=True)
    out = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "watch/room.jsonl",
        "stats": {
            "nodes": len(nodes),
            "edges": len(edges),
            "edges_by_type": by_kind,
            "corrupt": len(corrupt),
            "corrupt_lines": corrupt,
            "failures": len(failures),
        },
        "nodes": [nodes[i] for i in sorted(nodes)],
        "edges": [{"src": s, "dst": d, "kind": k} for s, d, k in edges],
        "failure_nodes": failures,
        "failure_slices": {str(f): causal_slice(f, adj) for f in shown},
    }
    path = OUTDIR / ("edg_%s.json" % time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()))
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("graph written: %s" % path)
    return path


if __name__ == "__main__":
    main()
