#!/usr/bin/env python3
"""graph_heal.py - knowledge-graph compaction pass v0 (Mickey17 W3, 2026-09-29).

Design owner: the S9 ARC lane (watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md,
"S9 - memory compaction ... THE ARC DESIGN"). The S9 survivorship law is
generational GC: promotion requires ONE why-context edge (Zettelkasten law:
unlinked is not knowledge), demotion emits forget-pointers, the destination
is the quantized_thought archive, and nothing is ever deleted. This tool is
the v0 compaction pass over memory/knowledge_graph.json:

  1. CENSUS    - degree-0 nodes (in+out) counted by kind. Byte truth, not
                 hand-copied headlines (the B2-69 census law): the ask's
                 "1167 orphans" does not byte-match; this pass recomputes.
  2. HEAL      - the cheap class only. An orphan earns ONE inbound why_context
                 edge when its name tokens (alnum, len>=4, own kind-word
                 dropped: 300 degenerate case_law rows are literally labeled
                 "law" and carry no name signal) match EXACTLY ONE module,
                 or its source file exists on disk and EXACTLY ONE other
                 module owns the same basename. Two different candidate
                 modules = ambiguous = NOT healed. Never self-heals. Skips
                 an edge that already exists (idempotent).
  3. DEMOTE    - every orphan not healed is LISTED, never deleted: a
                 forget-event JSONL row {name -> archive pointer} under
                 memory/corpus/quantized_thought/graph_ghosts/ (the pointer
                 law). The graph itself is untouched by demotion.

Idempotent by construction: re-running adds 0 edges (existing why_context
edges are skipped) and rewrites the derived forget/heal logs as the same
bytes (rows key on ids, not wall-clock; the graph's own ts is carried).

--dry reports the census/heal/demote plan and writes NOTHING. A real pass
appends only the planned edges to the graph (atomic tmp+replace) and writes
the two derived logs. Exit 0 = ran; exit 2 = cannot verify (missing or
corrupt graph) - fail-closed, never a guess.

Usage: python tools/graph_heal.py [--root PATH] [--graph PATH] [--dry] [--json]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "memory" / "knowledge_graph.json"
GHOST_DIR_REL = "memory/corpus/quantized_thought/graph_ghosts"
FORGET_LIST_REL = GHOST_DIR_REL + "/forget_events.jsonl"
HEAL_LOG_REL = GHOST_DIR_REL + "/heal_log.jsonl"
HEAL_REL = "why_context"
HEAL_MARKER = "graph_heal.v0"
KIND_WORDS = {"module", "knot", "law", "case_law", "doctrine", "steal",
              "landscape", "family"}
MIN_TOKEN_LEN = 4
SAFE_NAME_RE = re.compile(r"[^A-Za-z0-9._-]+")


class GraphHealError(Exception):
    """Fail-closed: cannot verify inputs (missing/corrupt graph)."""


def load_graph(path: Path) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            g = json.load(f)
    except (OSError, ValueError) as exc:
        raise GraphHealError(f"cannot load graph {path}: {exc}") from exc
    if not isinstance(g, dict) or not isinstance(g.get("nodes"), list) \
            or not isinstance(g.get("edges"), list):
        raise GraphHealError(f"graph {path} lacks nodes/edges lists")
    for n in g["nodes"]:
        if not isinstance(n, dict) or not n.get("id") or not n.get("kind"):
            raise GraphHealError(f"graph {path} has a node without id/kind")
    return g


def degree_map(edges: list[dict]) -> Counter:
    deg: Counter = Counter()
    for e in edges:
        deg[e.get("from", "")] += 1
        deg[e.get("to", "")] += 1
    return deg


def census(g: dict) -> dict:
    deg = degree_map(g["edges"])
    orphans = [n for n in g["nodes"] if deg[n["id"]] == 0]
    by_kind = Counter(n["kind"] for n in orphans)
    ids = Counter(n["id"] for n in g["nodes"])
    dup_ids = {k: v for k, v in ids.items() if v > 1}
    return {
        "nodes": len(g["nodes"]),
        "edges": len(g["edges"]),
        "orphans": len(orphans),
        "orphans_by_kind": dict(sorted(by_kind.items())),
        # byte truth: the builder emits duplicate-id rows (300x "law:") and
        # the census says so instead of papering over them
        "duplicate_node_ids": dict(sorted(dup_ids.items())),
    }


def _tokens(label: str | None, kind: str) -> set[str]:
    toks = {t for t in re.split(r"[^a-z0-9]+", (label or "").lower())
            if len(t) >= MIN_TOKEN_LEN}
    toks.discard(kind.lower())  # a node named only by its kind has no name signal
    return toks


def _basename(path: str | None) -> str:
    return os.path.basename((path or "").replace("\\", "/"))


def _safe_name(name: str) -> str:
    safe = SAFE_NAME_RE.sub("_", (name or "").strip()).strip("._-")
    return safe[:100] or "unnamed"


def archive_pointer(kind: str, label: str, node_id: str,
                    used: set[str]) -> str:
    """Deterministic repo-relative archive path. Collision fallbacks: an
    id-hash suffix, then a sequence suffix - the REAL graph carries 300
    byte-identical rows with id "law:" (an upstream builder defect the
    census reports), so even (label, id) is not unique in the wild."""
    base = f"{GHOST_DIR_REL}/{_safe_name(kind)}/{_safe_name(label)}"
    rel = base + ".md"
    if rel not in used:
        used.add(rel)
        return rel
    digest = hashlib.sha1(node_id.encode("utf-8")).hexdigest()[:8]
    rel = f"{base}-{digest}.md"
    seq = 2
    while rel in used:
        rel = f"{base}-{digest}-{seq}.md"
        seq += 1
    used.add(rel)
    return rel


@dataclass
class HealPlan:
    census: dict
    heal_ops: list[dict] = field(default_factory=list)
    demotions: list[dict] = field(default_factory=list)
    ambiguous: int = 0
    already_healed: int = 0

    @property
    def heal_count(self) -> int:
        return len(self.heal_ops)

    @property
    def demote_count(self) -> int:
        return len(self.demotions)


def plan(g: dict, repo_root: Path) -> HealPlan:
    """Pure planning: reads the graph, returns exactly what a real pass would
    do. No writes here - dry and real passes share this code path."""
    deg = degree_map(g["edges"])
    mods = [n for n in g["nodes"] if n["kind"] == "module"]
    mod_tokens: dict[str, set[str]] = defaultdict(set)
    for m in mods:
        for t in _tokens(m.get("label"), "module"):
            mod_tokens[t].add(m["id"])

    existing = {(e.get("from"), e.get("to"), e.get("rel"))
                for e in g["edges"]}
    used_paths: set[str] = set()
    plan_ = HealPlan(census=census(g))
    for o in sorted(g["nodes"], key=lambda n: (n["kind"], n["id"])):
        if deg[o["id"]] != 0:
            continue
        # Candidate modules from BOTH cheap rules, unioned before deciding:
        # one survivor heals, two or more competing stories heal nothing
        # (conservative), zero stories demotes. An orphan module may anchor
        # another orphan's heal - the anchor then earns out-degree itself,
        # which links it too (the graph's edges are module-sourced fan-out).
        token_cands: set[str] = set()
        for t in _tokens(o.get("label"), o["kind"]):
            token_cands |= mod_tokens.get(t, set())
        token_cands.discard(o["id"])

        file_cands: set[str] = set()
        src = o.get("source")
        if src and (Path(src).is_file() or (repo_root / src).is_file()):
            base = _basename(src)
            file_cands = {m["id"] for m in mods
                          if m["id"] != o["id"]
                          and _basename(m.get("source")) == base}

        picks = token_cands | file_cands
        if len(picks) > 1:
            plan_.ambiguous += 1  # conservative: competing stories, no edge
        pick = next(iter(picks)) if len(picks) == 1 else None

        if pick is None:
            plan_.demotions.append({
                "event": "forget",
                "law": "pointer-law: demoted-not-deleted (S9 ARC)",
                "id": o["id"],
                "name": o.get("label") or o["id"],
                "kind": o["kind"],
                "source": o.get("source", ""),
                "pointer": archive_pointer(o["kind"], o.get("label") or "",
                                           o["id"], used_paths),
            })
            continue
        if (pick, o["id"], HEAL_REL) in existing:
            plan_.already_healed += 1
            continue
        reason = ("name token matches exactly one module"
                  if pick in token_cands and pick not in file_cands else
                  "source file exists and exactly one other module owns it"
                  if pick in file_cands and pick not in token_cands else
                  "token and file rules agree on one module")
        plan_.heal_ops.append({
            "from": pick,
            "to": o["id"],
            "rel": HEAL_REL,
            "text": f"graph_heal v0 why-context: {reason}",
            "heal": HEAL_MARKER,
            "_orphan_kind": o["kind"],
        })
    return plan_


def apply_heal(g: dict, ops: list[dict]) -> dict:
    """Append the planned edges. Only (from,to,rel) shape keys land in the
    graph; the _-prefixed planning key is stripped."""
    for op in ops:
        edge = {k: v for k, v in op.items() if not k.startswith("_")}
        g["edges"].append(edge)
    return g


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def forget_rows(g: dict, plan_: HealPlan) -> tuple[list[dict], list[dict]]:
    """This pass's forget-events + a mirror of every why_context edge
    currently in the graph (the heal log). The heal log is derived state
    (deterministic for the same graph); forget-events are HISTORY - the
    caller merges them append-only by id (a later heal does not un-happen
    a demotion; the pointer law keeps the event)."""
    rows = [dict(d, graph_ts=g.get("ts", "")) for d in plan_.demotions]
    heal_rows = [{"log": "heal", "graph_ts": g.get("ts", ""), "from": e["from"],
                  "to": e["to"], "text": e.get("text", ""),
                  "heal": e.get("heal", "")}
                 for e in g["edges"] if e.get("rel") == HEAL_REL]
    return rows, heal_rows


def merge_forget(path: Path, new_rows: list[dict]) -> list[dict]:
    """Append-only merge by node id: existing rows keep their order/bytes,
    only never-recorded demotion IDS append, deduped within the new batch
    too (the real graph's 300 duplicate "law:" rows are ONE forget-event
    identity; idempotent reruns append zero rows)."""
    rows: list[dict] = []
    if path.is_file():
        with open(path, encoding="utf-8") as f:
            rows = [json.loads(x) for x in f.read().splitlines() if x.strip()]
    seen = {r.get("id") for r in rows}
    fresh: list[dict] = []
    for r in new_rows:
        if r.get("id") in seen:
            continue
        seen.add(r.get("id"))
        fresh.append(r)
    return rows + fresh


def save_graph(g: dict, path: Path) -> None:
    """Atomic in-place write preserving the file's compact ensure_ascii=False
    single-line shape (minimal diff noise against the builder's output)."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(g, f, ensure_ascii=False)
    os.replace(tmp, path)


def _report(g: dict, plan_: HealPlan, dry: bool) -> dict:
    by_kind_heal = Counter(op["_orphan_kind"] for op in plan_.heal_ops)
    return {
        "mode": "dry" if dry else "apply",
        "graph_ts": g.get("ts", ""),
        "census": plan_.census,
        "heal": {"add_edges": plan_.heal_count,
                 "already_healed": plan_.already_healed,
                 "ambiguous_skipped": plan_.ambiguous,
                 "by_kind": dict(sorted(by_kind_heal.items()))},
        "demote": {"listed": plan_.demote_count,
                   "pointer_list": FORGET_LIST_REL,
                   "deleted": 0,
                   "recorded_ids_total": None},
        "heal_samples": [f"{op['from']} -> {op['to']} ({op['text']})"
                         for op in plan_.heal_ops[:5]],
        "demote_samples": [f"{d['kind']}: {d['name']} -> {d['pointer']}"
                           for d in plan_.demotions[:5]],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=ROOT,
                    help="repo root (default: inferred from this file)")
    ap.add_argument("--graph", type=Path, default=None,
                    help="graph path (default: <root>/memory/knowledge_graph.json)")
    ap.add_argument("--dry", action="store_true",
                    help="report the plan, write nothing")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="machine-readable report")
    args = ap.parse_args(argv)

    graph_path = args.graph or (args.root / "memory" / "knowledge_graph.json")
    try:
        g = load_graph(graph_path)
    except GraphHealError as exc:
        print(f"RESULT: FAIL {exc}", file=sys.stderr)
        return 2

    plan_ = plan(g, args.root)
    if args.dry:
        report = _report(g, plan_, dry=True)
        print(json.dumps(report, ensure_ascii=False, indent=2)
              if args.as_json else _human(report))
        print("RESULT: DRY census=%d orphans heal=%d demote=%d"
              % (plan_.census["orphans"], plan_.heal_count,
                 plan_.demote_count))
        return 0

    apply_heal(g, plan_.heal_ops)
    save_graph(g, graph_path)
    forget, heal_rows = forget_rows(g, plan_)
    merged = merge_forget(args.root / FORGET_LIST_REL, forget)
    _write_jsonl(args.root / FORGET_LIST_REL, merged)
    _write_jsonl(args.root / HEAL_LOG_REL, heal_rows)
    report = _report(g, plan_, dry=False)
    report["demote"]["recorded_ids_total"] = len(merged)
    print(json.dumps(report, ensure_ascii=False, indent=2)
          if args.as_json else _human(report))
    print("RESULT: PASS healed=%d demoted_listed=%d deleted=0 graph_edges=%d"
          % (plan_.heal_count, plan_.demote_count, len(g["edges"])))
    return 0


def _human(r: dict) -> str:
    c = r["census"]
    lines = [
        "graph_heal v0 (%s) graph_ts=%s" % (r["mode"], r["graph_ts"]),
        "CENSUS  nodes=%d edges=%d orphans=%d by_kind=%s duplicate_ids=%s"
        % (c["nodes"], c["edges"], c["orphans"], c["orphans_by_kind"],
           c["duplicate_node_ids"] or "none"),
        "HEAL    add_edges=%d already_healed=%d ambiguous_skipped=%d by_kind=%s"
        % (r["heal"]["add_edges"], r["heal"]["already_healed"],
           r["heal"]["ambiguous_skipped"], r["heal"]["by_kind"]),
        "DEMOTE  listed=%d recorded_ids_total=%s deleted=%d pointer_list=%s"
        % (r["demote"]["listed"], r["demote"]["recorded_ids_total"],
           r["demote"]["deleted"], r["demote"]["pointer_list"]),
    ]
    lines += ["  heal: " + s for s in r["heal_samples"]]
    lines += ["  demote: " + s for s in r["demote_samples"]]
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
