"""knowledge_graph — one accurate, source-backed graph so things are 'just known spookily'.

The operator's ask (2026-08-10): "how can we use our system to produce an accurate knowledge graph
so i don't have to keep telling you to do these things they just are known spookily."

ANSWER: the substrate already exists and is content-addressed + verifiable —
  * verkle_chain.jsonl   — the shared fact ledger (every knot = a fact/event, tamper-evident)
  * code_map             — code-as-knowledge: module -> purpose -> invariants (LAW/DOCTRINE/SCHEMA)
  * skill_ledger         — case law (what worked, maps_to a module/skill)
  * memory/steal         — stolen knowledge (families + deltas)
  * ai_landscape         — the bleeding-edge registry mapped onto our modules
  * archetype_image      — the lens/archetype reading of any concept

This module TIES them into one queryable graph (nodes + source-backed edges) and adds the missing
piece: auto-consult. `known(query)` pulls the relevant subgraph for any ask and returns a compact
'we already know this' bundle — so the agent doesn't need to be re-told. `context()` turns it into
a session preamble (like cold_boot but from the whole graph). `fold()` grows the graph with each
new discovery, so knowledge accumulates and the operator never re-explains.

Deterministic, $0, no LLM. Every node carries a SOURCE (file/ref) so accuracy is grounded, not
hallucinated — 'known spookily' = 'known from the actual record.'

Schema: knowledge_graph.v1
CLI: python -m mag.knowledge_graph build | known "<query>" | context "<query>" | fold <label> <kind> "<note>" | status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except Exception:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SCHEMA = "knowledge_graph.v2"  # v2 = GraphRAG communities + Mem0 multi-signal + Letta dream
GRAPH_PATH = ROOT / "memory" / "knowledge_graph.json"

# Kinds regenerated from sources on every build(); every other kind is a hand-fold that build()
# must PRESERVE (amend-not-erase) so the weave accumulates and percolates instead of being wiped.
# 'invariant' joined the regenerated set 2026-10-05 (day-4 mine steal card defect 3): invariant
# nodes are derived from module docstrings, so they must rebuild with their modules, not persist.
# 'superseded'/'superseder' joined 2026-10-07 (lane m6-graph-supersession of
# morning-block-20261007, R5 next-loop target 2): the demotion register
# memory/fold_history/SUPERSEDED.md becomes graph facts - each row is a
# superseded/superseder node pair joined by one superseded_by edge, regenerated
# from the register on every build() like every other collector kind.
_COLLECTOR_KINDS = {"module", "invariant", "knot", "case_law", "steal", "landscape",
                    "superseded", "superseder"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower())


# ─────────────────────────────────────────────── node collectors (source-backed) ──
def _nodes_code() -> list[dict[str, Any]]:
    """code-as-knowledge: every mag module -> purpose + invariants (from code_map)."""
    nodes: list[dict[str, Any]] = []
    mag = ROOT / "mag"
    if not mag.is_dir():
        return nodes
    for p in sorted(mag.glob("*.py")):
        if p.name.startswith("_"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        doc = (re.search(r'"""(.*?)"""', text, re.S) or [None, ""])[1]
        purpose = ""
        invariants: list[str] = []
        for ln in (doc or "").splitlines():
            s = ln.strip()
            if not s:
                continue
            if not purpose:
                purpose = s[:160]
            if s.lower().startswith(("law", "doctrine", "schema", "invariant", "constitution", "never", "always")):
                invariants.append(s[:200])
        nodes.append({"id": f"module:{p.name}", "kind": "module", "label": p.stem,
                      "purpose": purpose, "invariants": invariants[:6],
                      "source": str(p)})
    return nodes


def _nodes_verkle() -> list[dict[str, Any]]:
    """the fact ledger: verkle knots -> theme (content-addressed).

    DEFECT FIX 1 (2026-10-05, day-4 mine steal card, watch/inbox/frontier_olm_2026-10-04/
    steal/agent-memory-and-continuity via x.md, estate map; evidence lens/graph.md item 4):
    the old reader pulled r['theme'] / r['summary'], fields verkle_chain.jsonl rows NEVER
    carry, so all 400 knots were label='knot' empty-summary stubs. Rows actually carry
    dominant_theme / session_id / tension_index / filename / leaf_hash (verified on the
    live 11,299-row chain this session), so label + summary are backfilled from those bytes.
    Fixed the same session; proof: knot_stub count 400 -> 0 in the b1_knowledge_graph receipt."""
    nodes: list[dict[str, Any]] = []
    for p in (ROOT / "memory" / "biography").glob("verkle_chain*.jsonl"):
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            label = str(r.get("dominant_theme")
                        or Path(str(r.get("filename") or "")).stem or "knot")
            summary = (f"session={r.get('session_id', '')} tension={r.get('tension_index', '')} "
                       f"amended={r.get('amended', '')} {r.get('filename', '')}")
            nodes.append({"id": f"knot:{str(r.get('leaf_hash') or r.get('hash') or '')[:16]}",
                          "kind": "knot", "label": label[:160],
                          "summary": summary[:200],
                          "tension": r.get("tension_index"),
                          "ts": r.get("ts") or r.get("t") or r.get("time") or "", "source": str(p)})
    return nodes[-400:]  # recent, bounded


def _nodes_case_law() -> list[dict[str, Any]]:
    """case law: skill_ledger rows -> signature + maps_to.

    DEFECT FIX 2 + 4 (2026-10-05, day-4 mine steal card, watch/inbox/frontier_olm_2026-10-04/
    steal/agent-memory-and-continuity via x.md, estate map + headline probe; evidence
    lens/graph.md item 5): the old id builder law:{str(r.get('id') or '')[:12]} collapsed
    all 300 rows onto the empty id 'law:' because skill_ledger.jsonl rows carry no id
    field. The live 8,879-row ledger carries exactly two schemas: skill_fired.v1
    (skill_id/job/pack_mode/chars_injected/ts) and skill_ledger.decision.v1
    (goal/task_shape/provider/model/outcome/detail/seat). Per the card's headline probe:
    key each node on sha256(skill_id + job + ts) for fired rows (decision rows:
    schema + ts + goal) so every precedent row stays individually addressable, and
    backfill label/summary/maps_to from the fields the rows actually carry.
    maps_to names the mag module that WRITES each schema (skill_fired.v1 receipts:
    mag/skills_pack.py:99-106; decision.v1 rows: mag/skill_ledger.py:137 record_decision),
    which is the only byte-backed module reference in the rows; that fires the previously
    dead maps_to edge builder and binds it to real module: nodes."""
    nodes: list[dict[str, Any]] = []
    p = ROOT / "memory" / "improve" / "skill_ledger.jsonl"
    if not p.is_file():
        return nodes
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines()[-300:]:
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if r.get("schema") == "skill_fired.v1":
            key = f"{r.get('skill_id', '')}|{r.get('job', '')}|{r.get('ts', '')}"
            label = str(r.get("skill_id") or "skill_fired")
            summary = (f"skill_fired {r.get('skill_id', '')} job={r.get('job', '')} "
                       f"pack={r.get('pack_mode', '')} chars_injected={r.get('chars_injected', '')}")
            maps_to = "mag/skills_pack.py"
        else:  # skill_ledger.decision.v1 (the only other schema in the ledger)
            key = f"{r.get('schema', '')}|{r.get('ts', '')}|{r.get('goal', '')}"
            label = str(r.get("goal") or r.get("task_shape") or "decision")[:80]
            summary = (f"decision task={r.get('task_shape', '')} provider={r.get('provider', '')}/"
                       f"{r.get('model', '')} outcome={r.get('outcome', '')} seat={r.get('seat', '')}")
            maps_to = "mag/skill_ledger.py"
        nodes.append({"id": f"law:{hashlib.sha256(key.encode('utf-8')).hexdigest()[:12]}",
                      "kind": "case_law", "label": label,
                      "summary": summary[:200],
                      "maps_to": maps_to, "source": str(p)})
    return nodes


def _nodes_invariants(module_nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Materialize one node per distinct invariant text the module docstrings carry.

    DEFECT FIX 3 (2026-10-05, day-4 mine steal card, watch/inbox/frontier_olm_2026-10-04/
    steal/agent-memory-and-continuity via x.md, estate map; evidence lens/graph.md items
    1 + 2): the old builder emitted 794 has_invariant edges to invariant:{_norm(inv)[:40]}
    targets that were NEVER materialized as nodes, so every one dangled (0 invariant
    nodes in nodes[]; only 2 of 825 edges joined two real nodes). Materializing them
    binds the whole law layer; same normalized text = same invariant id, so modules
    sharing a law text bind to one shared node (the old 'invariant:law ' degree-9
    collision becomes real connectivity instead of a dangling artifact)."""
    seen: dict[str, dict[str, Any]] = {}
    for m in module_nodes:
        for inv in m.get("invariants", []):
            iid = f"invariant:{_norm(inv)[:40]}"
            if iid not in seen:
                seen[iid] = {"id": iid, "kind": "invariant", "label": inv[:120],
                             "summary": inv[:200], "source": m.get("source", "")}
    return list(seen.values())


def _nodes_steal() -> list[dict[str, Any]]:
    """stolen knowledge: memory/steal docs -> family (from filename)."""
    nodes: list[dict[str, Any]] = []
    d = ROOT / "memory" / "steal"
    if not d.is_dir():
        return nodes
    for p in sorted(d.glob("*.md")):
        first = p.read_text(encoding="utf-8", errors="replace").splitlines()
        title = next((l.strip().lstrip("# ").strip() for l in first if l.strip()), p.stem)
        nodes.append({"id": f"steal:{p.stem}", "kind": "steal", "label": p.stem,
                      "summary": title[:200], "source": str(p)})
    return nodes


def _nodes_landscape() -> list[dict[str, Any]]:
    """the bleeding-edge registry: family -> we_have modules + delta."""
    nodes: list[dict[str, Any]] = []
    try:
        from mag.ai_landscape import LANDSCAPE
        for f in LANDSCAPE:
            nodes.append({"id": f"family:{f['family']}", "kind": "landscape",
                          "label": f["family"], "summary": f.get("name", ""),
                          "we_have": f.get("we_have", []),
                          "delta": f.get("delta", ""), "source": "mag/ai_landscape.py"})
    except Exception:
        pass
    return nodes


# ───────────────────────── supersession wire (the demotion register as graph facts) ──
# m6-graph-supersession (2026-10-07, lane m6 of morning-block-20261007, R5
# next-loop target 2): SUPERSEDED.md rows were prose only. Each register row now
# mints a superseded/superseder node pair joined by one superseded_by edge with
# both node ids. Collector-kind by construction: the d04 graph_heal appended
# edges manually and a rebuild wipes manual edges (measured 2026-10-07 on a
# copy: 117 why_context edges -> 0 after build()), so the edge branch in
# _edges() regenerates the edge from the dead node's superseded_by field (the
# maps_to precedent) and supersession survives the weave's own rebuild.
SUPERSEDED_REL = "superseded_by"


def superseded_register_path() -> Path:
    return ROOT / "memory" / "fold_history" / "SUPERSEDED.md"


def superseded_rows(register: Path | None = None) -> list[dict[str, str]]:
    """Parse the demotion register's ROWS table into one dict per row:
    {n, believed, banked, superseding, evidence}. Header and separator lines
    skip on the non-numeric first cell; a cell is never empty in a lawful row."""
    reg = register or superseded_register_path()
    if not reg.is_file():
        return []
    rows: list[dict[str, str]] = []
    for line in reg.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.strip()
        if not (s.startswith("|") and s.endswith("|")):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 5 or not cells[0].isdigit():
            continue  # header (# ...) and |---| separator lines
        rows.append({"n": cells[0], "believed": cells[1], "banked": cells[2],
                     "superseding": cells[3], "evidence": cells[4]})
    return rows


def _superseded_wire(register: Path | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Pure minter: register rows -> (node pairs, superseded_by edges). No I/O
    on the graph; build() takes the nodes, _edges() regenerates the edges from
    the dead node's superseded_by field, tools/superseded_wire.py applies both
    to the live graph."""
    src = "memory/fold_history/SUPERSEDED.md"
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    for r in superseded_rows(register):
        dead = f"superseded:row-{r['n']}"
        live = f"superseder:row-{r['n']}"
        nodes.append({"id": dead, "kind": "superseded",
                      "label": r["believed"][:80],
                      "summary": r["believed"][:200],
                      "banked": r["banked"][:160],
                      "outcome": "falsified",
                      "superseded_by": live,
                      "evidence": r["evidence"][:200],
                      "source": src})
        nodes.append({"id": live, "kind": "superseder",
                      "label": r["superseding"][:80],
                      "summary": r["superseding"][:200],
                      "source": src})
        edges.append({"from": dead, "to": live, "rel": SUPERSEDED_REL,
                      "text": r["evidence"][:160]})
    return nodes, edges


def _nodes_superseded(register: Path | None = None) -> list[dict[str, Any]]:
    return _superseded_wire(register)[0]


# ─────────────────────────────────────────────── graph assembly ──
def _edges(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    edges: list[dict[str, Any]] = []
    ids = {n["id"] for n in nodes}
    for n in nodes:
        # supersession wire (m6, 2026-10-07): a superseded node carries its
        # replacement's node id + the evidence cell, so the superseded_by edge
        # regenerates on every build() instead of dying as a manual append.
        if n.get("superseded_by"):
            edges.append({"from": n["id"], "to": n["superseded_by"],
                          "rel": SUPERSEDED_REL,
                          "text": str(n.get("evidence") or "")[:160]})
        if n["kind"] == "module":
            # DEFECT FIX 3b (2026-10-05, day-4 mine steal card, estate map; evidence
            # lens/graph.md section 2): the old [:4] cap truncated each module to at most
            # 4 invariant edges while the module node itself carries up to 6 (27 modules
            # were pinned at degree 4 purely by this cap). The fan now carries every
            # invariant the node carries; the invariant: targets are materialized as
            # nodes by _nodes_invariants so these edges no longer dangle.
            for inv in n.get("invariants", []):
                edges.append({"from": n["id"], "to": f"invariant:{_norm(inv)[:40]}",
                              "rel": "has_invariant", "text": inv[:120]})
        if n["kind"] == "landscape":
            # R4b filter (2026-10-06, ouroboros R4 memory fold finding S5, lane
            # r4b: watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/
            # SYNTHESIS.md row 3): we_have entries are free prose (examples on the
            # live landscape: "stateless-ghost-swarm / cheap_swarm / stateless_research
            # (stateless doctrine)", "surfaces built FOR agents end-to-end"), and the
            # old mint module:{Path(str(m)).name} turned every prose entry into an
            # already_inside edge aimed at a module id nothing materializes -- all 29
            # dangling edges in the 2026-10-06T09:20Z census were already_inside. Only
            # py-shaped entries (leading token a *.py path whose module node exists)
            # may mint; prose recognition stays on the node, not on a fake edge.
            for m in n.get("we_have", [])[:4]:
                token = str(m).strip().split()[0] if str(m).strip() else ""
                target = f"module:{Path(token).name}"
                if not token.endswith(".py") or target not in ids:
                    continue
                edges.append({"from": n["id"], "to": target,
                              "rel": "already_inside", "text": str(m)[:120]})
        if n.get("maps_to"):
            edges.append({"from": n["id"], "to": f"module:{Path(str(n['maps_to'])).name}",
                          "rel": "maps_to", "text": str(n["maps_to"])[:120]})
    return edges


# ─────────────────────────────────────────────── v2: GraphRAG + Mem0 + Letta steals ──
# kind importance for multi-signal retrieval (Mem0): modules/landscape > steal > law > knot
# 'invariant' added 2026-10-05 with defect fix 3: law-layer text ranks with case_law/doctrine.
_KIND_WEIGHT = {"module": 3, "landscape": 3, "steal": 2, "case_law": 2, "knot": 1,
                "doctrine": 2, "invariant": 2}


def _community_detect(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> dict[str, int]:
    """Deterministic community detection (label propagation) over module/invariant/landscape edges."""
    adj: dict[str, set[str]] = {}
    for e in edges:
        adj.setdefault(e["from"], set()).add(e["to"])
        adj.setdefault(e["to"], set()).add(e["from"])
    ids = [n["id"] for n in nodes]
    labels = {nid: i for i, nid in enumerate(ids)}
    for _ in range(6):
        changed = False
        for nid in ids:
            nb = adj.get(nid, set())
            if not nb:
                continue
            counts: dict[int, int] = {}
            for b in nb:
                counts[labels.get(b, -1)] = counts.get(labels.get(b, -1), 0) + 1
            best = max(counts, key=lambda k: (counts[k], -k))
            if labels[nid] != best:
                labels[nid] = best
                changed = True
        if not changed:
            break
    comp: dict[int, list[str]] = {}
    for nid in ids:
        comp.setdefault(labels[nid], []).append(nid)
    mapping: dict[str, int] = {}
    for ci, members in enumerate(comp.values()):
        for nid in members:
            mapping[nid] = ci
    return mapping


def _community_summaries(nodes: list[dict[str, Any]], mapping: dict[str, int]) -> list[dict[str, Any]]:
    """Community summaries (GraphRAG): cluster nodes -> one summary per community."""
    by_comm: dict[int, list[dict[str, Any]]] = {}
    for n in nodes:
        by_comm.setdefault(mapping[n["id"]], []).append(n)
    summaries = []
    for ci, members in by_comm.items():
        kinds: dict[str, int] = {}
        for m in members:
            kinds[m["kind"]] = kinds.get(m["kind"], 0) + 1
        labels = [m["label"] for m in members[:8]]
        summaries.append({"community": ci, "size": len(members), "kinds": kinds,
                          "members": [m["id"] for m in members[:14]],
                          "summary": "; ".join(labels)[:400]})
    return sorted(summaries, key=lambda s: -s["size"])


def global_search(query: str) -> dict[str, Any]:
    """GraphRAG Global Search: answer holistic questions via community summaries."""
    g = _read_graph() or build()
    nodes = g.get("nodes", []); edges = g.get("edges", [])
    mapping = _community_detect(nodes, edges)
    summaries = _community_summaries(nodes, mapping)
    q = _norm(query); qwords = set(w for w in q.split() if len(w) > 2)
    scored = []
    for s in summaries:
        hay = _norm(s["summary"])
        score = sum(1 for w in qwords if w in hay)
        if score:
            scored.append((score, s))
    scored.sort(key=lambda t: -t[0])
    return {"ok": True, "schema": SCHEMA, "mode": "global", "hits": len(scored),
            "communities": [s for _, s in scored[:6]]}


def local_search(query: str) -> dict[str, Any]:
    """GraphRAG Local Search: seed entities -> fan out to neighbors."""
    g = _read_graph() or build()
    nodes = g.get("nodes", []); edges = g.get("edges", [])
    adj: dict[str, set[str]] = {}
    for e in edges:
        adj.setdefault(e["from"], set()).add(e["to"])
        adj.setdefault(e["to"], set()).add(e["from"])
    q = _norm(query); qwords = set(w for w in q.split() if len(w) > 2)
    seeds = [n for n in nodes
             if any(w in _norm(f"{n['label']} {n.get('purpose','')} {n.get('summary','')}") for w in qwords)]
    results = []
    for s in seeds[:5]:
        neighbors = [n for n in nodes if n["id"] in adj.get(s["id"], set())][:8]
        results.append({"seed": s["label"], "seed_kind": s["kind"],
                        "neighbors": [{"id": n["id"], "label": n["label"], "kind": n["kind"]}
                                      for n in neighbors]})
    return {"ok": True, "schema": SCHEMA, "mode": "local", "seeds": len(seeds), "results": results}


def _node_text(n: dict[str, Any]) -> str:
    """The searchable haystack for a node (all text signals we index over)."""
    return _norm(f"{n['label']} {n.get('purpose','')} {n.get('summary','')} "
                 f"{' '.join(n.get('invariants',[]))} {' '.join(n.get('we_have',[]))} "
                 f"{n.get('delta','')} {n.get('maps_to','')}")


def _tokenize(text: str) -> list[str]:
    """Deterministic tokenizer: lowercase alnum runs, drop stopwords + 1-2 char tokens."""
    _STOP = {"the", "and", "for", "with", "our", "that", "this", "from", "into", "over",
             "how", "can", "you", "your", "what", "have", "has", "are", "was", "its", "not",
             "all", "any", "one", "but", "per", "via", "mag"}
    return [w for w in _norm(text).split()
            if len(w) > 2 and w not in _STOP]


def _bm25_index(nodes: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a deterministic BM25 index over the node corpus (no external deps).
    BM25 = sum over query terms of IDF * (tf*(k1+1)) / (tf + k1*(1 - b + b*dl/avgdl))."""
    k1, b = 1.2, 0.75
    docs = [_tokenize(_node_text(n)) for n in nodes]
    n_docs = len(docs)
    df: dict[str, int] = {}
    for d in docs:
        for w in set(d):
            df[w] = df.get(w, 0) + 1
    avgdl = sum(len(d) for d in docs) / max(n_docs, 1)
    idf = {w: max(0.1, ((n_docs - f + 0.5) / (f + 0.5)) + 1.0) for w, f in df.items()}
    return {"docs": docs, "idf": idf, "avgdl": avgdl, "k1": k1, "b": b}


def _bm25_score(idx: dict[str, Any], qwords: list[str], doc: list[str]) -> float:
    """Score one document against the BM25 index."""
    dl = len(doc)
    tf: dict[str, int] = {}
    for w in doc:
        tf[w] = tf.get(w, 0) + 1
    s = 0.0
    for w in qwords:
        if w not in tf:
            continue
        idf = idx["idf"].get(w, 0.0)
        f = tf[w]
        s += idf * (f * (idx["k1"] + 1)) / (f + idx["k1"] * (1 - idx["b"] + idx["b"] * dl / max(idx["avgdl"], 1)))
    return s


def _entity_overlap(qwords: set[str], n: dict[str, Any]) -> int:
    """Entity fusion (mem0): overlap between query tokens and the node's KEY identifiers
    (label / maps_to / we_have / invariants) — links facts that share entities, not just raw text."""
    hay = _tokenize(f"{n['label']} {n.get('maps_to','')} {' '.join(n.get('we_have',[]))} "
                    f"{' '.join(n.get('invariants',[]))}")
    return sum(1 for w in qwords if w in set(hay))


def _temporal_score(n: dict[str, Any], max_i: int) -> float:
    """Temporal ranker (mem0 time-aware): later knots/case-law are 'now-er' -> ranked for the
    current state, not just date-filtered. Deterministic by chain index."""
    if n["kind"] not in ("knot", "case_law"):
        return 0.0
    i = n.get("_i", 0)
    return 0.15 * (i / max(max_i, 1))  # recency weight scales 0..0.15 with chain position


def _score_node(n: dict[str, Any], qwords: set[str], idx: dict[str, Any]) -> dict[str, Any]:
    """True multi-signal (mem0): BM25 relevance + entity overlap + kind importance + temporal.
    Returns a BREAKDOWN so retrieval can say WHY a node won (honest provenance on the X-ray)."""
    doc = idx["docs"][n.get("_i", 0)] if 0 <= n.get("_i", 0) < len(idx["docs"]) else _tokenize(_node_text(n))
    bm25 = _bm25_score(idx, list(qwords), doc)
    entity = _entity_overlap(qwords, n)
    w = _KIND_WEIGHT.get(n["kind"], 1)
    temp = _temporal_score(n, max(len(idx["docs"]) - 1, 1))
    total = bm25 * w + entity * 0.5 + temp
    return {"total": total, "bm25": round(bm25, 3), "entity": entity,
            "temporal": round(temp, 3), "kind_weight": w}


def _rank_known(query: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Shared multi-signal ranker for known()/context(). Builds the corpus once, scores all nodes,
    returns (top nodes w/ why, diagnostics)."""
    q = _norm(query)
    qwords = set(_tokenize(query))
    nodes = build()["nodes"]
    for i, n in enumerate(nodes):
        n["_i"] = i
    idx = _bm25_index(nodes)
    scored = []
    for n in nodes:
        sc = _score_node(n, qwords, idx)
        if sc["total"] > 0:
            scored.append((sc["total"], sc, n))
    scored.sort(key=lambda t: -t[0])
    top = [dict(n, _why=sc, _score=round(tot, 3)) for tot, sc, n in scored[:12]]
    return top, {"nodes": len(nodes), "qwords": sorted(qwords)[:12]}


def capability_atom(*, domain: str = "general") -> dict[str, Any]:
    """MAG'S BPE SURFACE — the ONE atomic handle for this capability (operator law: new capabilities
    are addressable as atoms in our tokenizer; FACTS are NOT steered, only CAPABILITIES are).

    SELF-STEAL correction (2026-08-15, sacred-cow audit): mint_ribs() folded every retrieval hit
    into a `KNOWN[...]` steer atom — WRONG. RIBs are INSTRUCTIONS; a retrieval hit is a FACT. Seats
    should not carry per-hit facts in compiled steer. The honest surface is ONE capability handle the
    steering can reference ("consult multi-signal retrieval"), not N injected facts.

    This mints a single RIB atom advertising the multi-signal retrieval CAPABILITY so a seat can be
    steered to it — deterministic, deduped by content hash, $0."""
    atom = ("CAPABILITY: consult knowledge_graph.known()/context() for source-backed multi-signal "
            "retrieval (BM25 relevance + entity overlap + temporal ranker), each hit annotated with "
            "a _why breakdown; facts live in the knowledge layer, instructions in the atom layer.")
    try:
        from mag import rib_bus
        r = rib_bus.publish_rib(atom, domain=domain, source="knowledge_graph.capability",
                                target_rank="T2", fold=True, publish=True)
        return {"ok": True, "schema": SCHEMA, "mode": "capability_atom", "domain": domain,
                "key": r.get("key", ""), "verkle": bool(r.get("verkle", {}).get("ok", r.get("verkle"))),
                "published": r.get("published", False),
                "note": "ONE capability atom minted (not per-hit facts) — seats are steered TO the "
                        "retrieval capability; facts stay in the knowledge layer"}
    except Exception as e:
        return {"ok": False, "schema": SCHEMA, "mode": "capability_atom", "error": str(e)[:120]}


def dream(prune: bool = True) -> dict[str, Any]:
    """LETTA 'dreaming': offline consolidation of the graph while idle. Reclusters, summarizes,
    prunes duplicate knots/case-law, and folds a 'dreamed' community summary. This is the aimbotting
    engine — the graph self-maintains toward accuracy with zero operator effort."""
    g = build()
    nodes = g.get("nodes", []); edges = g.get("edges", [])
    mapping = _community_detect(nodes, edges)
    summaries = _community_summaries(nodes, mapping)
    pruned = 0
    if prune:
        seen: set[tuple[str, str]] = set()
        kept: list[dict[str, Any]] = []
        for i, n in enumerate(nodes):
            n["_i"] = i
            if n["kind"] in ("knot", "case_law"):
                key = (n["kind"], _norm(str(n.get("summary") or n["label"]))[:80])
                if key in seen:
                    pruned += 1
                    continue
                seen.add(key)
            kept.append(n)
        nodes = kept
    # persist community-augmented graph (versioned, content-addressed, amend-not-erase)
    g["nodes"] = nodes
    g["communities"] = summaries
    g["last_dream"] = _now()
    GRAPH_PATH.write_text(json.dumps(g, ensure_ascii=False, default=str), encoding="utf-8")
    try:
        from mag.schema_registry import checkpoint
        checkpoint("knowledge_graph", {"nodes": len(nodes), "edges": len(edges),
                                        "communities": len(summaries), "pruned": pruned},
                   label="dream")  # versioned history: LATEST + versions/, amend-never-erase
    except Exception:
        pass
    # fold a dreamed summary as a doctrine node so the consolidation itself becomes known
    fold("dreamed-communities", "doctrine",
         f"dreamed {len(summaries)} community/communities over {len(nodes)} node(s); pruned {pruned} duplicate(s)",
         source="dream")
    return {"ok": True, "schema": SCHEMA, "mode": "dream", "communities": len(summaries),
            "nodes": len(nodes), "edges": len(edges), "pruned": pruned}


def build() -> dict[str, Any]:
    # DEFECT FIX 3 wiring (2026-10-05, day-4 mine steal card): invariant nodes are derived
    # from module docstrings and must join the regenerated collector set so has_invariant
    # edges bind to real nodes instead of dangling on ids nothing materializes.
    modules = _nodes_code()
    nodes = (modules + _nodes_invariants(modules) + _nodes_verkle()
             + _nodes_case_law() + _nodes_steal() + _nodes_landscape()
             + _nodes_superseded())
    # PRESERVE hand-folded nodes (doctrine etc.) — build() must NOT clobber the weave.
    # Collector kinds are regenerated from sources each build; every other kind is a hand-fold
    # that accumulates and must survive rebuilds (amend-not-erase), else percolation is impossible.
    folded = [n for n in _read_graph().get("nodes", []) if n.get("kind") not in _COLLECTOR_KINDS]
    seen = {n["id"] for n in nodes}
    for n in folded:
        if n.get("id") not in seen:
            nodes.append(n)
    edges = _edges(nodes)
    graph = {"schema": SCHEMA, "ts": _now(), "nodes": nodes, "edges": edges}
    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_PATH.write_text(json.dumps(graph, ensure_ascii=False, default=str), encoding="utf-8")
    graph["counts"] = _counts(nodes)
    return graph


def _counts(nodes: list[dict[str, Any]]) -> dict[str, int]:
    c: dict[str, int] = {}
    for n in nodes:
        c[n["kind"]] = c.get(n["kind"], 0) + 1
    return c


# ─────────────────────────────────────────────── auto-consult (the 'spookily known') ──
def known(query: str) -> dict[str, Any]:
    """Pull the relevant subgraph for any ask — what we ALREADY know, source-backed.
    v2 multi-signal (mem0): BM25 relevance + entity overlap + kind importance + temporal ranker,
    each node annotated with a _why breakdown so the answer is honest about WHY it won."""
    top, diag = _rank_known(query)
    lens: dict[str, Any] = {}
    try:
        from mag.archetype_image import classify, ARCHETYPES
        name = classify(query)
        a = ARCHETYPES.get(name) or {}
        lens = {"archetype": a.get("canon", name), "lens": a.get("lens"),
                "shadow": a.get("shadow"), "essence": a.get("essence"), "minds": a.get("minds", [])}
    except Exception:
        pass
    return {"ok": True, "schema": SCHEMA, "query": query, "hits": len(top),
            "mode": "multi-signal-v2", "known": top, "lens": lens, "diagnostics": diag,
            "summary": f"already know {len(top)} source-backed node(s) about this; nothing to re-derive",
            "accuracy": "every node carries a source (verkle/code/ledger/steal/landscape); each hit "
                        "carries a _why breakdown (bm25/entity/temporal/kind_weight)"}


def context(query: str, max_chars: int = 2400) -> str:
    """A compact session preamble from the graph — inject so the agent 'just knows'."""
    k = known(query)
    if not k.get("known"):
        return f"# Known — nothing on '{query}'\n\nBoot cold on this."
    lines = [f"# Known (auto-consulted knowledge graph) — '{query}'", ""]
    ln = k.get("lens") or {}
    if ln:
        lines.append(f"- **Lens:** {ln.get('archetype')} / {ln.get('lens')} — {ln.get('essence')} · shadow: {ln.get('shadow')}")
    for n in k["known"][:8]:
        body = n.get("purpose") or n.get("summary") or n.get("label")
        lines.append(f"- [{n['kind']}] **{n.get('label')}**: {str(body)[:180]}")
    text = "\n".join(lines)
    return text if len(text) <= max_chars else text[:max_chars] + " …"


# R4b outcome stamps (2026-10-06, ouroboros R4 memory fold finding S5): a graph that
# can only GROW cannot represent a superseded conclusion -- fold()-rot is one of the
# no-demotion disease's four masks. Every fold now carries held/falsified/pending;
# the falsifier that fires flips the stamp instead of leaving forever-true doctrine.
_OUTCOMES = ("held", "falsified", "pending")


def fold(label: str, kind: str, note: str, source: str = "session",
         outcome: str = "pending") -> dict[str, Any]:
    """Grow the graph with a new discovered node (knowledge accumulates).

    outcome: held (a falsifier ran and the claim survived) / falsified (a
    falsifier fired and killed it) / pending (folded but unverified -- the
    default, and how legacy pre-stamp nodes read by absence)."""
    if outcome not in _OUTCOMES:
        raise ValueError(f"outcome must be one of {_OUTCOMES}, got {outcome!r}")
    g = _read_graph()
    nid = f"{kind}:{_norm(label)[:40]}"
    if any(n["id"] == nid for n in g.get("nodes", [])):
        return {"ok": True, "schema": SCHEMA, "id": nid, "already_present": True}
    g.setdefault("nodes", []).append({"id": nid, "kind": kind, "label": label,
                                      "summary": note[:200], "source": source,
                                      "outcome": outcome})
    GRAPH_PATH.write_text(json.dumps(g, ensure_ascii=False, default=str), encoding="utf-8")
    return {"ok": True, "schema": SCHEMA, "id": nid, "already_present": False,
            "outcome": outcome, "counts": _counts(g.get("nodes", []))}


def _read_graph() -> dict[str, Any]:
    if GRAPH_PATH.is_file():
        try:
            return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {"nodes": [], "edges": []}


def status() -> dict[str, Any]:
    g = build()
    return {"ok": True, "schema": SCHEMA, "counts": g["counts"], "n_edges": len(g.get("edges", [])),
            "graph_path": str(GRAPH_PATH)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="knowledge_graph", description="accurate source-backed knowledge graph + auto-consult")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("build")
    k = sub.add_parser("known"); k.add_argument("query", nargs="+")
    c = sub.add_parser("context"); c.add_argument("query", nargs="+")
    g = sub.add_parser("global"); g.add_argument("query", nargs="+")
    l = sub.add_parser("local"); l.add_argument("query", nargs="+")
    sub.add_parser("dream")
    f = sub.add_parser("fold"); f.add_argument("label"); f.add_argument("kind"); f.add_argument("note", nargs="+")
    f.add_argument("--outcome", choices=list(_OUTCOMES), default="pending")
    sub.add_parser("status")
    a = p.parse_args(argv)
    if a.cmd == "build":
        g = build(); print(json.dumps({"counts": g["counts"], "n_edges": len(g.get("edges", []))}, indent=2))
    elif a.cmd == "known":
        print(json.dumps(known(" ".join(a.query)), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "context":
        print(context(" ".join(a.query)))
    elif a.cmd == "global":
        print(json.dumps(global_search(" ".join(a.query)), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "local":
        print(json.dumps(local_search(" ".join(a.query)), indent=2, ensure_ascii=False, default=str))
    elif a.cmd == "dream":
        print(json.dumps(dream(), indent=2, ensure_ascii=False))
    elif a.cmd == "fold":
        print(json.dumps(fold(a.label, a.kind, " ".join(a.note), outcome=a.outcome),
                         indent=2, ensure_ascii=False))
    elif a.cmd == "status":
        print(json.dumps(status(), indent=2, ensure_ascii=False))
    else:
        p.print_help(); return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
