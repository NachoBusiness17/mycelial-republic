"""amh pass1: HN Algolia broad sweep for agent-memory-continuity (2026-10-11).

Fresh query angles not used by the eight prior HN folds of this area, plus a
post-2026-10-10 catch-up lane (the 10-10 sweep's moment cutoff) to surface
stories no prior fold could have seen. Receipts: _amh_p1_hits.json.

SSRF guard: every request URL must be https and its host must be in
_ALLOWED_HOSTS (the ask's named door, hn.algolia.com); checked after parsing,
before any socket is opened.
"""
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
CUTOFF_30D = 1789084800       # 2026-09-11T00:00:00Z
CUTOFF_POST_1010 = 1791388800  # 2026-10-10T00:00:00Z (after the 10-10 sweep moment)

_ALLOWED_HOSTS = {"hn.algolia.com"}
_API_BASE = "https://hn.algolia.com/api/v1/"


def guard(url: str) -> None:
    """Fail closed unless the URL is https to an allowlisted host."""
    p = urllib.parse.urlparse(url)
    if p.scheme != "https" or p.hostname not in _ALLOWED_HOSTS:
        raise ValueError(f"blocked non-allowlisted fetch target: {p.scheme} {p.hostname}")


QUERIES = [
    # fresh angles (never used by prior folds of this area)
    ("agent handoff", "search_by_date", CUTOFF_30D),
    ("AGENTS.md", "search_by_date", CUTOFF_30D),
    ("episodic memory", "search_by_date", CUTOFF_30D),
    ("memory palace", "search_by_date", CUTOFF_30D),
    ("zettelkasten", "search_by_date", CUTOFF_30D),
    ("second brain", "search_by_date", CUTOFF_30D),
    ("scratchpad", "search_by_date", CUTOFF_30D),
    ("context engineering", "search_by_date", CUTOFF_30D),
    ("memory poisoning", "search_by_date", CUTOFF_30D),
    ("experience replay", "search_by_date", CUTOFF_30D),
    ("procedural memory", "search_by_date", CUTOFF_30D),
    ("memory consolidation", "search_by_date", CUTOFF_30D),
    ("working memory", "search_by_date", CUTOFF_30D),
    ("memory decay", "search_by_date", CUTOFF_30D),
    ("agent checkpoint", "search_by_date", CUTOFF_30D),
    ("LLM journal", "search_by_date", CUTOFF_30D),
    ("AI diary", "search_by_date", CUTOFF_30D),
    ("world model memory", "search_by_date", CUTOFF_30D),
    ("conversation summary", "search_by_date", CUTOFF_30D),
    ("sleep learning", "search_by_date", CUTOFF_30D),
    # relevance lanes for named systems not previously swept
    ("HippoRAG", "search", None),
    ("A-MEM agentic memory", "search", None),
    ("Memento LLM agent", "search", None),
    ("Letta", "search_by_date", CUTOFF_30D),
    # catch-up: anything after the 10-10 sweep moment (guaranteed unswept)
    ("agent memory", "search_by_date", CUTOFF_POST_1010),
    ("memory", "search_by_date", CUTOFF_POST_1010),
    ("context", "search_by_date", CUTOFF_POST_1010),
    ("agent state", "search_by_date", CUTOFF_POST_1010),
    ("warm boot", "search_by_date", CUTOFF_POST_1010),
    ("session", "search_by_date", CUTOFF_POST_1010),
]


def fetch(url: str, tries: int = 3) -> dict:
    guard(url)
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    return {"_error": str(last), "_url": url}


def main() -> None:
    all_hits: dict[str, dict] = {}
    lane_report = []
    for q, endpoint, cutoff in QUERIES:
        params = {"query": q, "tags": "story", "hitsPerPage": "30"}
        if endpoint == "search_by_date" and cutoff:
            params["numericFilters"] = f"created_at_i>{cutoff}"
        url = _API_BASE + endpoint + "?" + urllib.parse.urlencode(params)
        res = fetch(url)
        n = res.get("nbHits", 0)
        hits = res.get("hits", [])
        lane_report.append({"query": q, "endpoint": endpoint, "cutoff": cutoff,
                            "nbHits": n, "fetched": len(hits), "error": res.get("_error")})
        for h in hits:
            oid = h.get("objectID")
            if not oid:
                continue
            cur = all_hits.get(oid)
            if cur is None:
                all_hits[oid] = {
                    "id": oid, "title": h.get("title"), "url": h.get("url"),
                    "points": h.get("points"), "num_comments": h.get("num_comments"),
                    "created_at": h.get("created_at"), "created_at_i": h.get("created_at_i"),
                    "author": h.get("author"), "lanes": [q],
                }
            else:
                cur["lanes"].append(q)
        time.sleep(0.4)
    in_window = [h for h in all_hits.values()
                 if h["created_at_i"] and h["created_at_i"] > CUTOFF_30D]
    out = {"cutoff_30d": CUTOFF_30D, "cutoff_post_1010": CUTOFF_POST_1010,
           "lanes": lane_report, "unique_total": len(all_hits),
           "in_window": sorted(in_window, key=lambda h: h["created_at_i"])}
    (HERE / "_amh_p1_hits.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"lanes={len(lane_report)} unique={len(all_hits)} in_window={len(in_window)}")
    for lr in lane_report:
        tag = "ERR " if lr["error"] else ""
        print(f"  {tag}{lr['endpoint']:16s} {lr['query'][:28]:28s} nb={lr['nbHits']:6d} got={lr['fetched']}")
    print("\n== in-window candidates (newest first) ==")
    for h in sorted(in_window, key=lambda h: -h["created_at_i"]):
        d = h["created_at"][:10]
        print(f"{h['id']:>9} {d} {h['points'] or 0:>4}p {h['num_comments'] or 0:>4}c "
              f"{(h['title'] or '')[:88]}")


if __name__ == "__main__":
    main()
