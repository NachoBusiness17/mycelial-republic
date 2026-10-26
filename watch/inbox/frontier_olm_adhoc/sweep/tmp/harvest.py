"""Pass 1 broad sweep: Arctic Shift Reddit search across 4 subreddits, last 30 days.

Serial + stdlib only (no subprocess, no extra deps). Output: candidates.jsonl + top table.
"""
import json
import time
import urllib.parse
import urllib.request

BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"
SUBS = ["LocalLLaMA", "MachineLearning", "LocalLLM", "ollama"]
QUERIES = [
    "judge",
    "as judge",
    "evaluator",
    "reward model",
    "failure attribution",
    "agent eval",
    "benchmark harness",
    "self-improve",
    "self-improving",
    "skill library",
    "variance",
    "contamination",
    "blind evaluation",
    "rubric",
    "regression",
    "case law",
    "telemetry",
]
AFTER = "2026-09-11"
OUT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep\tmp\candidates.jsonl"

seen = {}
for sub in SUBS:
    for q in QUERIES:
        params = urllib.parse.urlencode(
            {"subreddit": sub, "query": q, "after": AFTER, "limit": 100}
        )
        url = f"{BASE}?{params}"
        req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload = json.load(resp)
        except Exception as exc:  # noqa: BLE001 - log and continue, door health matters
            print(f"ERR {sub} '{q}': {exc}")
            time.sleep(3)
            continue
        rows = payload.get("data", [])
        for p in rows:
            pid = p.get("id")
            if not pid or pid in seen:
                continue
            seen[pid] = {
                "id": pid,
                "subreddit": p.get("subreddit"),
                "title": p.get("title"),
                "score": p.get("score", 0),
                "num_comments": p.get("num_comments", 0),
                "created_utc": p.get("created_utc"),
                "permalink": p.get("permalink"),
                "selftext": (p.get("selftext") or "")[:600],
                "matched": q,
                "link_flair_text": p.get("link_flair_text"),
            }
        print(f"OK {sub} '{q}': +{len(rows)} rows (unique so far {len(seen)})")
        time.sleep(1.5)

with open(OUT, "w", encoding="utf-8") as fh:
    for row in seen.values():
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")

rows = sorted(seen.values(), key=lambda r: (r["score"] or 0), reverse=True)
print(f"\nTOTAL unique candidates: {len(rows)}\n")
for r in rows[:60]:
    print(f"{r['score']:>5} {r['num_comments']:>4}c  r/{r['subreddit']:<15} {r['id']}  {r['title'][:110]}")
