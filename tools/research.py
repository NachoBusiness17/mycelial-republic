"""research -- read-only surfacing tools over the fleet's research corpus.

Sources unified here (all local, all read-only):
  * watch/inbox/LINKS.jsonl            -- the canonical link ledger (245+ rows;
                                          event-derived rows carry no canonical
                                          and are excluded here, see EVENTS)
  * watch/inbox/EVENTS.jsonl           -- the 51 split-out event rows (event.v1),
                                          searched as their own source so their
                                          titles/details stay reachable without
                                          minting empty pointers
  * memory/lenses/corpus_index.json    -- research packs (107 indexed asks)
  * memory/corpus/*/                   -- the canon lanes (ai, esoteric, games,
                                          mycology, electronics, steering,
                                          moonshot, founding_law, shadertoy21k,
                                          training_pdfs, ...)

LAW: pointers, not bodies -- hits carry path + snippet; corpus_get/research
files themselves stay the retrieval target. Confined to the repo root.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LINKS = REPO / "watch" / "inbox" / "LINKS.jsonl"
EVENTS = REPO / "watch" / "inbox" / "EVENTS.jsonl"
CORPUS_INDEX = REPO / "memory" / "lenses" / "corpus_index.json"
CANON = REPO / "memory" / "corpus"


def _terms(query: str) -> list[str]:
    return [t.lower() for t in (query or "").split() if t]


def _hit(terms: list[str], *texts: str) -> bool:
    if not terms:
        return True
    hay = "\n".join(t or "" for t in texts).lower()
    return all(t in hay for t in terms)


def research_search(query: str = "", source: str = "all", limit: int = 20) -> dict:
    """Search the research corpus: links ledger, pack index, canon filenames.

    source: all | links | events | packs | canon. Returns pointers + short snippets.
    """
    limit = max(1, min(int(limit), 100))
    terms = _terms(query)
    hits: list[dict] = []

    if source in ("all", "links"):
        try:
            for line in open(LINKS, encoding="utf-8", errors="replace"):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                canonical = str(row.get("canonical") or "")
                # B2-169: event-derived LINKS rows carry an empty canonical; a hit
                # on them would emit an empty pointer, so they are excluded here
                # and searchable as their own source below (watch/inbox/EVENTS.jsonl).
                if not canonical.strip():
                    continue
                note = str(row.get("note") or "")
                title = str(row.get("title") or "")
                if _hit(terms, canonical, title, note):
                    hits.append({"src": "links", "title": title or canonical[:80],
                                 "pointer": canonical,
                                 "snippet": note[:220],
                                 "ts": row.get("ts") or ""})
                if len(hits) >= limit:
                    break
        except OSError:
            pass

    if source in ("all", "events") and len(hits) < limit:
        try:
            for line in open(EVENTS, encoding="utf-8", errors="replace"):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                title = str(row.get("title") or "")
                detail = str(row.get("detail") or "")
                ev_id = str(row.get("id") or "")
                if _hit(terms, title, detail, ev_id):
                    hits.append({"src": "events", "title": title or ev_id,
                                 "pointer": "watch/inbox/EVENTS.jsonl#" + ev_id,
                                 "snippet": detail[:220],
                                 "ts": row.get("ts") or ""})
                if len(hits) >= limit:
                    break
        except OSError:
            pass

    if source in ("all", "packs") and len(hits) < limit:
        try:
            idx = json.loads(CORPUS_INDEX.read_text(encoding="utf-8"))
            for k, item in (idx.get("items") or {}).items():
                title = str(item.get("title") or "")
                ask = str(item.get("ask") or "")
                excerpt = str(item.get("answer_excerpt") or "")[:300]
                if _hit(terms, title, ask, excerpt):
                    hits.append({"src": "packs", "title": title or ask[:80],
                                 "pointer": "memory/lenses/corpus_index.json#" + k,
                                 "snippet": (ask + " :: " + excerpt)[:220],
                                 "ts": item.get("ts") or ""})
                if len(hits) >= limit:
                    break
        except (OSError, json.JSONDecodeError):
            pass

    if source in ("all", "canon") and len(hits) < limit:
        try:
            for lane_dir in sorted(CANON.iterdir()):
                if not lane_dir.is_dir():
                    continue
                for path in sorted(lane_dir.rglob("*")):
                    if not path.is_file():
                        continue
                    name = path.name
                    if _hit(terms, name, str(path.parent.name)):
                        hits.append({"src": "canon:" + lane_dir.name,
                                     "title": name,
                                     "pointer": str(path.relative_to(REPO)).replace(os.sep, "/"),
                                     "snippet": "",
                                     "ts": ""})
                    if len(hits) >= limit:
                        break
                if len(hits) >= limit:
                    break
        except OSError:
            pass

    return {"ok": True, "tool": "research_search", "query": query, "source": source,
            "hit_count": len(hits), "hits": hits,
            "law": "pointers only -- open the file (corpus_get) before quoting it as evidence"}


def research_sources() -> dict:
    """Inventory the canon lanes: primary evidence sources by lane."""
    lanes = []
    try:
        for lane_dir in sorted(CANON.iterdir()):
            if not lane_dir.is_dir():
                continue
            files = [p for p in lane_dir.rglob("*") if p.is_file()]
            sample = [p.name for p in sorted(files)[:4]]
            lanes.append({"lane": lane_dir.name, "files": len(files),
                          "bytes": sum(p.stat().st_size for p in files[:400]),
                          "sample": sample})
    except OSError as e:
        return {"ok": False, "error": str(e)}
    lanes.sort(key=lambda l: -l["files"])
    return {"ok": True, "tool": "research_sources", "lanes": lanes,
            "lane_count": len(lanes),
            "law": "primary evidence lives here; cite the file, not the summary"}


def research_stats() -> dict:
    """Counts across the research organs."""
    out = {}
    try:
        out["links_rows"] = sum(1 for _ in open(LINKS, encoding="utf-8", errors="replace"))
    except OSError:
        out["links_rows"] = 0
    try:
        idx = json.loads(CORPUS_INDEX.read_text(encoding="utf-8"))
        out["packs_indexed"] = idx.get("count")
    except Exception:  # noqa: BLE001
        out["packs_indexed"] = 0
    lane_files = 0
    lane_count = 0
    try:
        for lane_dir in CANON.iterdir():
            if lane_dir.is_dir():
                lane_count += 1
                lane_files += sum(1 for p in lane_dir.rglob("*") if p.is_file())
    except OSError:
        pass
    out["canon_lanes"] = lane_count
    out["canon_files"] = lane_files
    return {"ok": True, "tool": "research_stats", **out}
