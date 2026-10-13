"""build_knowledge_graph -- organize every artifact, knowledge-graph style, old -> new.

Operator order (2026-09-17): "have our lite librarian load everything in our local
sovereign agent drive and files and organize them knowledge graph style, every artifact
grouping them to what they contain and represented mapped from old to new. self steal --
we've done this before."

SELF-STEAL REUSED:
  * mag/catalog_scan.py ZONE_MAP -- the estate's zone logic (intake/watch/basecamp...)
  * memory/mycelium/edges.jsonl -- the mycelium.v1 association schema (src/dst/type/weight)
  * memory/lenses/corpus_index.json -- the corpus lens
The Librarian (Lite lane, chat_provider) then annotates: names each family, flags
orphans/duplicates, extends the old->new lineages. INVENTED MECHANISMS = BUILD CANDIDATES
(operator: "if something invents maybe we need to build it").

OUT: watch/inbox/FLEET_KNOWLEDGE_GRAPH_20260917.json (+ .md map)
RUN: .venv\\Scripts\\python.exe scripts\\build_knowledge_graph.py [--annotate]
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_JSON = ROOT / "watch" / "inbox" / "FLEET_KNOWLEDGE_GRAPH_20260917.json"
OUT_MD = ROOT / "watch" / "inbox" / "FLEET_KNOWLEDGE_GRAPH_20260917.md"

# content families: (family, [relative dirs/globs]) -- what artifacts CONTAIN
FAMILIES = {
    "laws": ["docs/DNA.md", "CONSTITUTION.md", "AGENTS.md", "memory/law",
             "mag/lite_guard.py", "docs/ref/canon"],
    "boards-plans": ["memory/plans", "queue/todo.md", "watch/inbox/FIFTY_WIDE_BOARD*.md",
                     "watch/inbox/wave_20260916/WAVE_STATE*.md"],
    "receipts-wave": ["watch/inbox/wave_20260916/receipts",
                      "watch/inbox/physical_computing/receipts",
                      "watch/inbox/moonshot_20260916/receipts"],
    "research-packs": ["memory/runs", "memory/research_packs", "training"],
    "canon-corpus": ["memory/corpus", "memory/lenses/corpus_index.json"],
    "parable-operator": ["watch/inbox/THE_PARABLE_REGISTER.md",
                         "watch/inbox/journal_mark_202609",
                         "watch/inbox/LOOKING_GLASS*",
                         "watch/inbox/transcripts"],
    "sessions-histories": ["memories/session", "memory/trajectory", "memory/biography",
                           "watch/flight_recorder.jsonl"],
    "links-press": ["watch/inbox/LINKS.jsonl", "memory/press", "watch/X_REPLY_RADAR*",
                    "watch/inbox/X_REPLY_RADAR*"],
    "game-builds": ["dashboard/static/games", "scripts/test_*", "scripts/build_lane_game.py",
                    "watch/inbox/*MAZE*", "watch/inbox/*DUNGEON*"],
    "providers-drive": ["configs/providers.yaml", "scripts/union_fullsend_day.py",
                        "scripts/build_lane_game.py", "scripts/librarian.py",
                        "scripts/build_fleet_imprint.py", "watch/inbox/union_fullsend_20260917"],
    "estate-catalog": ["watch/ESTATE_INDEX", "dashboard/data/ESTATE_INDEX.jsonl",
                       "catalog", "mag/catalog.py", "mag/catalog_scan.py"],
    "mycelium-graph": ["memory/mycelium", "memory/percolator", "memory/rib_bus"],
    "lanes-trails": ["queue/lanes", "dashboard/static/trails", "dashboard/static/lanes",
                     "watch/monitor_lane.state", "watch/HUNGER_LEDGER.md"],
    "imprint-librarian": ["watch/inbox/FLEET_IMPRINT*.md", "scripts/build_fleet_imprint.py",
                          "scripts/librarian.py", "memory/corpus/tide_cards"],
    "skills-engine": [".agents/skills/memweave", ".agents/skills/memlance",
                      ".agents/skills/retrocausal-steering", ".agents/skills/mesh-comms",
                      ".agents/skills/salon", "tools/corpus.py", "tools/research.py",
                      "mag/mcp_server.py"],
    "askability-layer": ["watch/inbox/CORPUS_MAP_SALON_20260918.md", "catalog/tags.jsonl",
                         "catalog/TAG_REPORT.md", "watch/inbox/SEAT_CAPABILITIES_20260918.md",
                         "watch/WANTS.md"],
    "shadow-corpus": ["memory/corpus/zcode_history", "memory/corpus/watch_mining",
                      "watch/inbox/ZCODE_SHADOW_STEAL_20260918.md",
                      "watch/inbox/WATCH_MINING_20260918.md"],
    "operating-doctrine": ["watch/inbox/CONTEXT_OS_20260918.md",
                           "watch/inbox/STANDING_WAVE_PROTOCOL_20260918.md",
                           "watch/inbox/SKILL_FORGE_20260918.md"],
    "audits-lenses": ["watch/inbox/SELF_AUDIT_ZCODE_20260918.md",
                      "watch/inbox/SOCRATIC_GAPS_20260918.md",
                      "watch/inbox/SELF_STEAL_DEEP_20260918.md", "queue/lanes/elder"],
}

# explicit successions (old -> new) the map must carry by name
SUCCESSIONS = [
    ("fifty-wide board 2026-09-15", "fifty-wide board 2026-09-17"),
    ("PROSE_CENSUS_20260904..0916", "PROSE_CENSUS_20260917"),
    ("X_REPLY_RADAR daily chain", "X_REPLY_RADAR_20260917"),
    ("maze_arena.html", "ruins_go.html (the -GO steal)"),
    ("wave_20260916 receipts", "HANDOFF_GOODNIGHT_20260917 -> fifty-wide 0917"),
    ("catalog_scan estate zones", "FLEET_KNOWLEDGE_GRAPH (this file)"),
    ("memory index MEMORY.md", "FLEET_IMPRINT (librarian cold-load)"),
    ("salon_50 / research_fanout 12 lanes", "union_fullsend wave mode (18 lanes)"),
    ("Sep-16 estate snapshot (946,773 rows, junction doubles)", "catalog v3 rebuild (757,667 rows, deduped, junction-pruned)"),
    ("chan clause 11 + ractor panels", "mesh-comms skill"),
    ("napkin seed + dead-drop ribs", "retrocausal-steering + memlance skills"),
    ("MINDSWEAVE eval + ghost doctrine", "memweave skill"),
    ("zcode store operator-voice attrition", "watch card timeline (770-card arc)"),
    ("standing wave 143 receipts / 16 lanes", "STANDING_WAVE_PROTOCOL spec"),
    ("catalog map without consumer", "corpus + research askability tools"),
    ("elder 14-lens question canon", "self-audit + socratic gaps (the seat audits itself)"),
]


def _iter_targets():
    seen = set()
    for fam, pats in FAMILIES.items():
        for pat in pats:
            p = ROOT / pat
            if p.is_file():
                yield fam, p
            elif any(ch in pat for ch in "*["):
                for hit in ROOT.glob(pat):
                    if hit.is_file():
                        yield fam, hit
            elif p.is_dir():
                for dirpath, dirnames, filenames in os.walk(p):
                    dirnames[:] = [d for d in dirnames
                                   if d not in {".git", ".venv", "node_modules", "__pycache__",
                                                ".mimosa", ".pytest_cache", ".ruff_cache"}]
                    for f in filenames:
                        yield fam, Path(dirpath) / f


def build_nodes_edges() -> tuple[list[dict], list[dict]]:
    fams: dict[str, dict] = {}
    for fam, p in _iter_targets():
        rel = str(p.relative_to(ROOT))
        if rel in seen_set():
            continue
        try:
            st = p.stat()
        except OSError:
            continue
        d = fams.setdefault(fam, {"family": fam, "files": 0, "bytes": 0,
                                  "oldest": None, "newest": None, "sample": []})
        d["files"] += 1
        d["bytes"] += st.st_size
        mt = st.st_mtime
        d["oldest"] = min(d["oldest"] or mt, mt)
        d["newest"] = max(d["newest"] or mt, mt)
        if len(d["sample"]) < 5:
            d["sample"].append(rel)
    nodes = []
    for fam, d in fams.items():
        nodes.append({
            "id": f"fam-{fam}", "kind": "family", "family": fam,
            "contains": FAMILY_DESC.get(fam, ""),
            "files": d["files"], "bytes": d["bytes"],
            "oldest": datetime.fromtimestamp(d["oldest"], tz=timezone.utc).isoformat()
            if d["oldest"] else None,
            "newest": datetime.fromtimestamp(d["newest"], tz=timezone.utc).isoformat()
            if d["newest"] else None,
            "sample": d["sample"],
        })
    edges = [{"src": a, "dst": b, "type": "succeeded-by"}
             for a, b in SUCCESSIONS]
    # mycelium edges import (association layer)
    mine = ROOT / "memory" / "mycelium" / "edges.jsonl"
    if mine.is_file():
        n = 0
        for ln in mine.read_text(encoding="utf-8", errors="replace").splitlines()[:4000]:
            try:
                r = json.loads(ln)
            except Exception:
                continue
            edges.append({"src": r.get("src"), "dst": r.get("dst"),
                          "type": f"mycelium:{r.get('type')}",
                          "weight": r.get("weight")})
            n += 1
            if n >= 500:
                break
    return nodes, edges


def seen_set() -> set:
    global _SEEN
    try:
        return _SEEN
    except NameError:
        _SEEN = set()
        return _SEEN


FAMILY_DESC = {
    "laws": "constitution, DNA, pacing law, canon-gated doctrine",
    "boards-plans": "fifty-wide boards, wave state, the queue",
    "receipts-wave": "wave/physical/moonshot receipt rows",
    "research-packs": "fanout batteries, salon artifacts, training rows",
    "canon-corpus": "PD primary documents (ai/game/electronics/esoteric/moonshot/mycology)",
    "parable-operator": "the operator's voice: parables, journals, the looking-glass lens",
    "sessions-histories": "session cards, trajectory steps, biography, flight recorder",
    "links-press": "canonical link ledger, press digests, X radar chains",
    "game-builds": "shipped games + their harnesses (mud, frontier, ruins_go...)",
    "providers-drive": "the 24/7 drive: lanes, keys mapping, evolution loop, librarian",
    "estate-catalog": "the askability spine: catalog.jsonl (757,667 rows post-v3) + walkers + tags",
    "mycelium-graph": "association edges, percolator invariants, rib doctrine",
    "lanes-trails": "lane trails and states (7 base lanes; 12/16/18 in wave modes)",
    "imprint-librarian": "the anti-forgetting layer: imprint, librarian, tide cards",
    "skills-engine": "forged skills (memweave, memlance, retrocausal-steering, mesh-comms) + the tool drivers they run on",
    "askability-layer": "the map-consumer layer: corpus/research tools, tags, WANTS intake",
    "shadow-corpus": "recovered primary voices: zcode session history + the 770-card watch timeline",
    "operating-doctrine": "specs distilled from our own machinery: context OS, standing wave, skill forge",
    "audits-lenses": "the seat examining itself: self-audit, socratic gaps, deep steal, elder surface",
}


def annotate(nodes: list[dict], edges: list[dict]) -> str:
    """The Librarian pass (Lite lane, canonical door): name/flag/extend the graph."""
    sys.path.insert(0, str(ROOT))
    from models.providers import chat_provider
    brief = json.dumps({"families": [{k: n[k] for k in ("family", "contains", "files",
                                                        "oldest", "newest")} for n in nodes],
                        "successions": SUCCESSIONS,
                        "mycelium_edge_count": sum(1 for e in edges
                                                   if str(e.get("type", "")).startswith("mycelium"))},
                       ensure_ascii=False)[:14000]
    r = chat_provider(
        "z_ai3",
        system=("You are the fleet's Librarian organizing its knowledge graph. Given the "
                "family summary and successions, return compact markdown: (1) one line per "
                "family naming what it REALLY contains and its old->new arc; (2) ORPHANS "
                "(families or files that seem misplaced/duplicated); (3) MISSING LINEAGES "
                "(old->new progressions the successions list misses); (4) BUILD CANDIDATES: "
                "mechanisms the graph implies should exist but no family shows -- a invented "
                "mechanism is a build order. Be exact; do not invent file names."),
        user=brief, model="glm-5.3-flash", tier="T2", timeout=300)
    return r.get("text", "") if r.get("ok") else f"(librarian pass failed: {r.get('error')})"


def main(argv=None) -> int:
    do_annotate = "--annotate" in (argv or sys.argv[1:])
    nodes, edges = build_nodes_edges()
    doc = {
        "schema": "fleet_knowledge_graph.v1",
        "generated": datetime.now(timezone.utc).isoformat(),
        "reuses": ["mag/catalog_scan.py ZONE_MAP", "memory/mycelium/edges.jsonl schema",
                   "memory/lenses/corpus_index.json"],
        "nodes": nodes, "edges": edges,
    }
    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    md = ["# FLEET KNOWLEDGE GRAPH — every artifact, grouped by what it contains, old -> new", ""]
    for n in sorted(nodes, key=lambda x: -x["files"]):
        md.append(f"## {n['family']} — {n['files']} files, {n['bytes']//1024//1024 or n['bytes']//1024}K")
        md.append(f"*contains:* {n['contains']}  ·  *span:* {n['oldest']} → {n['newest']}")
        md.append("*samples:* " + ", ".join("`" + s + "`" for s in n["sample"]))
        md.append("")
    md.append("## OLD → NEW (the successions)")
    md.extend(f"- {a} → **{b}**" for a, b in SUCCESSIONS)
    md.append("")
    if do_annotate:
        md.append("## LIBRARIAN ANNOTATION (glm-5.3-flash, Lite lane)")
        md.append(annotate(nodes, edges))
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps({"ok": True, "json": str(OUT_JSON), "md": str(OUT_MD),
                      "families": len(nodes), "edges": len(edges),
                      "annotated": do_annotate}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
