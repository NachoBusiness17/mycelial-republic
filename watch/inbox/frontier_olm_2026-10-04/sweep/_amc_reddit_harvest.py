"""Arctic Shift reddit harvest for agent-memory-and-continuity sweep, 2026-10-04.

Door provenance: arctic-shift.photon-reddit.com proved working by the 10-03 sibling
(watch/inbox/frontier_olm_2026-10-03/sweep/agent-memory-and-continuity-reddit.md AMENDMENT).
Window: 2026-09-04T00:00:00Z .. now, 4 subreddits, paged by `before`.
Output: _amc_reddit_harvest.jsonl in this sweep dir.
"""
import json, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

OUT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-04\sweep\_amc_reddit_harvest.jsonl"
BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"
SUBS = ["LocalLLaMA", "LocalLLM", "MachineLearning", "ollama", "AI_Agents", "Rag", "ClaudeAI", "LLMDevs"]
WINDOW_START = int(datetime(2026, 9, 4, tzinfo=timezone.utc).timestamp())
MAX_PAGES_PER_SUB = 45
PAGE = 100

KEYWORDS = ["memori", "memory", "remember", "recall", "knowledge graph", "knowledgeGraph",
            "graphrag", "graphiti", "mem0", "zep ", "letta", "memgpt", "compaction",
            "consolidat", "continuity", "warm boot", "warm-start", "warm start",
            "handoff", "hand-off", "session resume", "session resum", "summariz",
            "dedup", "entity resolution", "identity", "append-only", "append only",
            "sleep-time", "sleep time", "reflection", "decay", "forget", "stale",
            "pointer", "unlinked", "orphan", "regenerat", "re-deriv", "rederiv",
            "context rot", "context engineer", "long-term memory", "long term memory",
            "persistent memory", "persist memory", "agentic memory", "agent memory",
            "memory system", "memory layer", "memory store", "claude.md", "memory.md"]

def fetch(sub, before):
    url = f"{BASE}?subreddit={sub}&limit={PAGE}&before={before}"
    req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/2026-10-04"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 422, 500, 502, 503):
                time.sleep(20 * (attempt + 1))
                continue
            raise
        except Exception:
            time.sleep(10)
    return None

def main():
    import os
    seen = {}
    for sub in SUBS:
        part_path = os.path.join(os.path.dirname(OUT), f"_amc_harvest_{sub}.jsonl")
        if os.path.exists(part_path):
            with open(part_path, encoding="utf-8") as f:
                for line in f:
                    row = json.loads(line)
                    seen[row["id"]] = row
            print(f"{sub}: resume from file, {len(seen)} total seen", flush=True)
            continue
        rows_sub = {}
        before = int(time.time())
        pages = 0
        got = 0
        try:
            while pages < MAX_PAGES_PER_SUB:
                data = fetch(sub, before)
                if not data or not data.get("data"):
                    break
                rows = data["data"]
                for row in rows:
                    rid = row.get("id")
                    if rid and rid not in seen:
                        rec = {
                            "id": rid, "subreddit": row.get("subreddit"),
                            "title": row.get("title"), "selftext": (row.get("selftext") or "")[:4000],
                            "score": row.get("score"), "num_comments": row.get("num_comments"),
                            "created_utc": row.get("created_utc"), "author": row.get("author"),
                            "permalink": row.get("permalink"),
                        }
                        seen[rid] = rec
                        rows_sub[rid] = rec
                        got += 1
                before = min(int(r["created_utc"]) for r in rows)
                pages += 1
                if before < WINDOW_START:
                    break
                time.sleep(1.5)
        except Exception as e:
            print(f"{sub}: aborted early at page {pages}: {e!r}", flush=True)
        with open(part_path, "w", encoding="utf-8") as f:
            for rec in rows_sub.values():
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"{sub}: {pages} pages, {got} new rows, oldest={datetime.fromtimestamp(before, timezone.utc).isoformat() if before else 'n/a'}", flush=True)
    # keyword rank, window filter
    hits = []
    for row in seen.values():
        if not row["created_utc"] or row["created_utc"] < WINDOW_START:
            continue
        text = (row["title"] + " " + row["selftext"]).lower()
        score = sum(2 if k in text else 0 for k in KEYWORDS)
        if score > 0:
            row["kw_score"] = score
            hits.append(row)
    hits.sort(key=lambda r: (-(r["kw_score"]), -(r["score"] or 0)))
    with open(OUT, "w", encoding="utf-8") as f:
        for row in hits:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"TOTAL unique posts seen: {len(seen)}; in-window keyword hits: {len(hits)} -> {OUT}", flush=True)

if __name__ == "__main__":
    main()
