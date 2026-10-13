#!/usr/bin/env python3
"""rib_fork.py - pre-warmed RIBs as forks over the mycelium graph (F13, 2026-09-30).

Operator insight (2026-09-30): "pre-warmed ribs can act as forks via different
world lines." A rib (memory/rib/*.md, mounted by mag/rib_boot.py) is a pre-warmed
starting point; the mycelium graph (memory/mycelium/) is the higher-dimensional
space. Given a question this tool: (1) projects it onto the ribs (nearest rib =
the fork's handle); (2) projects question+rib onto the graph's giant component
(the only subgraph where paths exist) as the seed set; (3) traces K world lines
from that one rib projection -- per-line seed, edge-type affinity (lineage /
semantic / thread), salience-weighted walk, cross-line divergence penalty; (4)
converges: nodes reached by >=2 lines, or line pairs linked at <=2 hops in the
adjacency matrix (the A^2 test), are the high-confidence findings, single-line
reach is where the novel lives; (5) matrix census: A^2/A^3 expose indirect
connections no direct edge shows.

READ-ONLY over the graph by law (matches mag/rib_boot.py's mount-only stance):
never writes to memory/mycelium or memory/rib. Ratchet-clean: no bare except,
no except-pass, ROOT-anchored paths, <400 lines.

Usage: tools/rib_fork.py census | indirect --top 12 | fork --question "..." --lines 3
Exit 0 ok; 1 projection/trace failure; 2 graph unreadable.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
NODES = ROOT / "memory" / "mycelium" / "nodes.jsonl"
EDGES = ROOT / "memory" / "mycelium" / "edges.jsonl"
RIB_DIR = ROOT / "memory" / "rib"
SCHEMA = "rib_fork.v1"

# Affinity families: causal lineage, semantic relation, session/thread time.
LINE_STYLES = {
    "lineage":  {"produced": 1.0, "depends": 1.0, "consumption": 0.9, "handoff": 0.8,
                 "same_thread": 0.6, "related": 0.5},
    "semantic": {"related": 1.0, "evidence_for": 0.9, "supports": 0.9, "same_thread": 0.7,
                 "produced": 0.4},
    "thread":   {"same_thread": 1.0, "consumption": 0.9, "handoff": 0.9, "produced": 0.5,
                 "related": 0.4},
}
CROSS_PENALTY = 0.35  # node already on an earlier line -> its score scales by this
STOP = set("""a an and are as at be but by for from has have how i if in into is it its
of on or our should that the their them then there these they this to we what when
where which who why will with you your""".split())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()  # single clock, every schema row stamps it


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]{2,}", (text or "").lower()) if t not in STOP]


def load_graph() -> tuple[dict[str, dict], list[dict]]:
    """Nodes deduped last-write-wins (same semantics as mag.mycelium._load_nodes)."""
    nodes: dict[str, dict] = {}
    bad = 0
    if not NODES.is_file() or not EDGES.is_file():
        print(json.dumps({"ok": False, "error": "graph files missing", "exit": 2}))
        raise SystemExit(2)
    for line in NODES.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            n = json.loads(line)
            nodes[str(n["id"])] = n
        except Exception:
            bad += 1
    if bad:
        sys.stderr.write(f"node parse issues: {bad}\n")
    edges: list[dict] = []
    for line in EDGES.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            e = json.loads(line)
            if str(e.get("src")) in nodes and str(e.get("dst")) in nodes:
                edges.append(e)
        except Exception as ex:
            sys.stderr.write(f"edge parse issue: {ex}\n")
    return nodes, edges


def undirected_adj(nodes: dict[str, dict], edges: list[dict]) -> dict[str, list[tuple]]:
    """node -> [(neighbor, weight, salience, etype)] with parallel edges kept."""
    adj: dict[str, list[tuple]] = {i: [] for i in nodes}
    for e in edges:
        s, d = str(e["src"]), str(e["dst"])
        w = float(e.get("weight") or 0.5)
        sal = float(e.get("salience") or w)
        adj[s].append((d, w, sal, str(e.get("type") or "related")))
        if s != d:
            adj[d].append((s, w, sal, str(e.get("type") or "related")))
    return adj


# ------------------------------------------------------------------ census ----
def census() -> dict:
    nodes, edges = load_graph()
    real = [e for e in edges if e["src"] != e["dst"]]
    und_pairs = {frozenset((e["src"], e["dst"])) for e in real}
    n = len(nodes)
    density = len(und_pairs) / (n * (n - 1) / 2) if n > 1 else 0.0
    adj = {k: v for k, v in undirected_adj(nodes, edges).items() if v}
    # components over ALL nodes (isolated nodes are their own component)
    seen: set[str] = set()
    comps: list[int] = []
    for start in nodes:
        if start in seen:
            continue
        q, c = deque([start]), 0
        seen.add(start)
        while q:
            cur = q.popleft()
            c += 1
            for nb, *_ in adj.get(cur, ()):
                if nb not in seen:
                    seen.add(nb)
                    q.append(nb)
        comps.append(c)
    comps.sort(reverse=True)
    isolated = sum(1 for c in comps if c == 1)
    # exact hop histogram on the giant component (all-pairs BFS; graph is small)
    giant = max(nodes, key=lambda i: len(adj.get(i, ())))
    hops: Counter[int] = Counter()
    dist_total = pairs = 0
    diam, diam_pair = 0, ("", "")
    seen = {giant}
    q = deque([(giant, 0)])
    reach: dict[str, int] = {giant: 0}
    while q:
        cur, d = q.popleft()
        for nb, *_ in adj.get(cur, ()):
            if nb not in reach:
                reach[nb] = d + 1
                hops[d + 1] += 1
                pairs += 1
                dist_total += d + 1
                if d + 1 > diam:
                    diam, diam_pair = d + 1, (giant, nb)
                q.append((nb, d + 1))
    hist = sorted(hops.items())
    med = [h for h, c in hist for _ in range(c)][pairs // 2] if pairs else 0
    return {
        "schema": SCHEMA, "ok": True, "ts": _now(),
        "node_lines": sum(1 for l in NODES.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()),
        "nodes_unique": n, "edges": len(edges),
        "self_loops": len(edges) - len(real),
        "edge_types": dict(Counter(str(e.get("type")) for e in edges)),
        "density_undirected": round(density, 8),
        "components": {"count": len(comps), "largest": comps[0] if comps else 0,
                       "isolated_nodes": isolated,
                       "top5_sizes": comps[:5]},
        "giant_component": {"nodes": len(reach),
                            "hop_histogram": {str(h): c for h, c in hist},
                            "mean_hops": round(dist_total / pairs, 3) if pairs else None,
                            "median_hops": med, "diameter_hops": diam,
                            "diameter_pair": [nodes[i].get("title", i) for i in diam_pair]},
    }


# ---------------------------------------------------------------- indirect ----
def indirect(top: int) -> dict:
    nodes, edges = load_graph()
    active = sorted({str(e[k]) for e in edges for k in ("src", "dst")})
    idx = {nid: i for i, nid in enumerate(active)}
    m = len(active)
    W = np.zeros((m, m), dtype=np.float64)
    for e in edges:
        s, d = idx[str(e["src"])], idx[str(e["dst"])]
        if s == d:
            continue
        w = float(e.get("salience") or e.get("weight") or 0.5)
        W[s, d] = max(W[s, d], w)
        W[d, s] = max(W[d, s], w)
    A2 = W @ W
    A3 = A2 @ W
    direct = W > 0
    reach2 = direct | (A2 > 0)
    np.fill_diagonal(A2, 0.0)
    np.fill_diagonal(A3, 0.0)
    pure2 = np.where(direct, 0.0, A2)
    pure3 = np.where(reach2, 0.0, A3)

    def pairs_of(mat: np.ndarray, k: int) -> list[dict]:
        flat = mat.flatten()
        order = np.argpartition(flat, -min(k, flat.size - 1))[-k:]
        out = []
        for f in sorted(order, key=lambda x: -flat[x]):
            i, j = divmod(int(f), m)
            if flat[f] <= 0 or j <= i:  # undirected: keep one orientation per pair
                continue
            row = {"a": nodes[active[i]].get("title", active[i]),
                   "b": nodes[active[j]].get("title", active[j]),
                   "score": round(float(flat[f]), 4), "hops": 2 if mat is pure2 else 3}
            if mat is pure2:
                via = int(np.argmax(W[i, :] * W[:, j]))
                row["via"] = nodes[active[via]].get("title", active[via])
            out.append(row)
            if len(out) >= k:
                break
        return out

    per_node = {nodes[nid].get("title", nid): [
        {"to": nodes[active[int(j)]].get("title", active[int(j)]),
         "score": round(float(pure2[i][j]), 4)}
        for j in sorted(np.argpartition(pure2[i], -min(top, m - 1))[-top:],
                        key=lambda j: -pure2[i][j]) if pure2[i][j] > 0][:top]
        for nid, i in idx.items() if pure2[i].max() > 0}
    return {
        "schema": SCHEMA, "ok": True, "ts": _now(), "active_nodes": m,
        "direct_undirected_pairs": int(direct.sum() // 2),
        "two_hop_only_pairs": int((pure2 > 0).sum() // 2),
        "three_hop_only_pairs": int((pure3 > 0).sum() // 2),
        "strongest_two_hop": pairs_of(pure2, top),
        "strongest_three_hop": pairs_of(pure3, max(3, top // 2)),
        "per_node_top_two_hop": per_node,
    }


# -------------------------------------------------------------------- fork ----
def _idf(docs: list[list[str]]) -> dict[str, float]:
    df = Counter(t for d in docs for t in set(d))
    tot = max(1, len(docs))
    return {t: math.log(tot / c) for t, c in df.items()}


def fork(question: str, lines: int, rib_path: str | None, depth: int, seeds: int) -> dict:
    nodes, edges = load_graph()
    adj = {k: v for k, v in undirected_adj(nodes, edges).items() if v}
    node_ids = list(nodes)
    node_docs = [tokenize(" ".join([nodes[i].get("title", ""), nodes[i].get("label", ""),
                                    " ".join(nodes[i].get("tags") or []),
                                    nodes[i].get("body", "")])) for i in node_ids]
    node_sets = [set(d) for d in node_docs]
    idf = _idf(node_docs)
    # 1. rib projection: nearest rib by rib-corpus IDF-weighted overlap
    rib_files = sorted(RIB_DIR.glob("*.md"))
    rib_docs = [tokenize(p.read_text(encoding="utf-8", errors="replace")) for p in rib_files]
    ridf = _idf(rib_docs)
    qtoks = tokenize(question)
    # rib score uses capped token COUNTS (not set membership): a rib that talks
    # at length about the question's tokens outranks one that mentions them once
    rib_scores = [sum(ridf.get(t, 0.0) * min(c, 5) for t, c in Counter(rib_docs[k]).items()
                      if t in set(qtoks)) for k in range(len(rib_files))]
    if rib_path:
        rib = ROOT / rib_path if not Path(rib_path).is_absolute() else Path(rib_path)
        pick = rib_files.index(rib) if rib in rib_files else -1
        if pick < 0:
            return {"ok": False, "error": f"rib not found: {rib_path}", "exit": 1}
    else:
        pick = max(range(len(rib_files)), key=lambda k: rib_scores[k])
    rib_tokens = set(rib_docs[pick])
    # rib pre-warms the query: its distinctive tokens join the question at half weight
    warm = sorted((t for t in rib_tokens - set(qtoks) if ridf.get(t, 0) > 0),
                  key=lambda t: (-ridf[t], t))[:15]  # name tiebreak: hash-order-free
    qcount = Counter(qtoks)
    for t in warm:
        qcount[t] += 0.5  # half weight: pre-warmed, not asked

    def relevance(k: int) -> float:
        return sum(w * idf.get(t, 0.0) for t, w in qcount.items() if t in node_sets[k])

    rel = {nid: relevance(k) for k, nid in enumerate(node_ids)}
    # 2. graph projection, restricted to the giant component: a world line is a
    #    PATH, so the projection targets the one subgraph where paths exist
    #    (485-node core vs 3,106 isolated leaves). The rib+question query
    #    projects to k nearest nodes there; every line starts inside that
    #    projection, so the rib is the shared fork origin.
    hub0 = max(adj, key=lambda i: len(adj[i]))
    core, q = {hub0}, deque([hub0])
    while q:
        for nb, *_ in adj.get(q.popleft(), ()):
            if nb not in core:
                core.add(nb)
                q.append(nb)
    ranked = sorted((i for i in core if i in adj), key=lambda i: (-rel[i], i))
    if not ranked:
        return {"ok": False, "error": "no active nodes project onto the question", "exit": 1}
    starts = (ranked + ranked[:1] * lines)[:lines]  # reuse best seed if projection is narrow
    # 3. K world lines: per-line seed + edge-type affinity + divergence penalty
    style_names = [k for k in ("lineage", "semantic", "thread")] + ["semantic"] * lines
    styles = [LINE_STYLES[style_names[k]] for k in range(lines)]
    used_by: dict[str, list[int]] = {}
    world_lines = []
    for li, style in enumerate(styles):
        start = starts[li]
        cur, path, steps = start, [start], []
        for _ in range(depth):
            best, best_s = None, -1.0
            for nb, w, sal, et in adj.get(cur, ()):
                if nb in path:
                    continue
                s = (style.get(et, 0.4) * (0.4 * sal + 0.3) *
                     (0.5 + min(1.0, rel.get(nb, 0.0))) *
                     (CROSS_PENALTY if nb in used_by else 1.0))
                if s > best_s:
                    best, best_s, best_et = (nb, et), s, et
            if best is None:
                break
            cur = best[0]
            path.append(cur)
            used_by.setdefault(cur, []).append(li)
            steps.append({"to": nodes[cur].get("title", cur), "edge": best_et,
                          "via_score": round(best_s, 4)})
        world_lines.append({"line": li + 1, "style": style_names[li],
                            "start": nodes[start].get("title", start), "steps": steps,
                            "terminal": nodes[cur].get("title", cur), "path_ids": path,
                            "path": [nodes[p].get("title", p) for p in path]})
    # 4. convergence: node reached by >=2 lines = high confidence; one line = novel
    line_nodes = [set(wl["path"]) for wl in world_lines]  # paths already carry titles
    hits = sorted({(t, li) for li, ns in enumerate(line_nodes) for t in ns})
    member = {t: [li for tt, li in hits if tt == t] for t, _ in hits}
    converged = {t: v for t, v in member.items() if len(v) >= 2}
    novel = {t: li + 1 for li, ns in enumerate(line_nodes)
             for t in ns if sum(t in x for x in line_nodes) == 1}
    # 4b. matrix convergence: two lines CONVERGE when path nodes of different
    # lines link directly or at two hops (the A^2 test) -- same answer
    # neighborhood from different directions; >2 hops is divergence/novelty.
    core_ids = sorted(core)
    cidx = {i: k for k, i in enumerate(core_ids)}
    m = len(core_ids)
    Wc = np.zeros((m, m))
    for e in edges:
        s, d = str(e["src"]), str(e["dst"])
        if s != d and s in cidx and d in cidx:
            k1, k2 = cidx[s], cidx[d]
            w = float(e.get("salience") or e.get("weight") or 0.5)
            Wc[k1, k2] = Wc[k2, k1] = max(Wc[k1, k2], w)
    reach2 = (Wc > 0) | ((Wc @ Wc) > 0)
    line_idsets = [wl["path_ids"] for wl in world_lines]
    bridges = []
    for a in range(len(world_lines)):
        for b in range(a + 1, len(world_lines)):
            best = (3, None, None)
            for u in line_idsets[a]:
                for v in line_idsets[b]:
                    if u not in cidx or v not in cidx:
                        continue
                    h = 1 if Wc[cidx[u], cidx[v]] > 0 else (2 if reach2[cidx[u], cidx[v]] else 3)
                    if h < best[0]:
                        best = (h, u, v)
            if best[1] is not None:
                bridges.append({"lines": [a + 1, b + 1], "min_hops": best[0],
                                "a": nodes[best[1]].get("title", best[1])[:70],
                                "b": nodes[best[2]].get("title", best[2])[:70],
                                "converged": best[0] <= 2})
    return {
        "schema": SCHEMA, "ok": True, "ts": _now(), "question": question,
        "rib": rib_files[pick].name, "rib_warm_tokens": warm[:10],
        "rib_scores_top3": [{"rib": rib_files[k].name, "score": round(rib_scores[k], 3)} for k in
                            sorted(range(len(rib_files)), key=lambda k: -rib_scores[k])[:3]],
        "seed_projection": [{"node": nodes[i].get("title", i), "relevance": round(rel[i], 3),
                             "degree": len(adj[i])} for i in ranked[:max(seeds, lines)]],
        "world_lines": world_lines,
        "converged": [{"node": t, "lines": v} for t, v in
                      sorted(converged.items(), key=lambda kv: -len(kv[1]))],
        "matrix_bridges": bridges,
        "novel_single_line": [{"node": t, "line": li} for t, li in
                              sorted(novel.items(), key=lambda kv: (kv[1], kv[0]))]}


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception as ex:
        sys.stderr.write(f"stdout reconfigure failed: {ex}\n")
    ap = argparse.ArgumentParser(prog="rib_fork", description="ribs as forks over the mycelium graph")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("census", help="nodes/edges/density/components/hop distribution")
    p_in = sub.add_parser("indirect", help="A^2/A^3 indirect-connection census")
    p_in.add_argument("--top", type=int, default=10)
    p_fork = sub.add_parser("fork", help="trace world lines for a question")
    p_fork.add_argument("--question", required=True)
    p_fork.add_argument("--lines", type=int, default=3)
    p_fork.add_argument("--rib", default=None, help="explicit rib path (else projected)")
    p_fork.add_argument("--depth", type=int, default=6)
    p_fork.add_argument("--seeds", type=int, default=4)
    args = ap.parse_args(argv)
    out = {"census": census, "indirect": lambda: indirect(args.top),
           "fork": lambda: fork(args.question, args.lines, args.rib, args.depth, args.seeds)}[args.cmd]()
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    return 0 if out.get("ok") else int(out.get("exit", 1))


if __name__ == "__main__":
    raise SystemExit(main())
