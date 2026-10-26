"""Pass 1 round 2: slower single-token sweep to fill 429/422 gaps."""
import json
import time
import urllib.parse
import urllib.request

BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"
SUBS = ["LocalLLaMA", "MachineLearning", "LocalLLM", "ollama"]
QUERIES = [
    "Jev",
    "verdict",
    "panel",
    "attribution",
    "harness",
    "gate",
    "dedup",
    "benchmark",
    "eval",
    "skills",
    "calibrat",
    "abstention",
    "decision",
]
AFTER = "2026-09-11"
OUT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_adhoc\sweep\tmp\candidates.jsonl"

seen = {}
try:
    with open(OUT, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            seen[r["id"]] = r
except FileNotFoundError:
    pass
print(f"loaded existing: {len(seen)}")

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
        except Exception as exc:  # noqa: BLE001
            print(f"ERR {sub} '{q}': {exc}")
            time.sleep(6)
            continue
        rows = payload.get("data", [])
        fresh = 0
        for p in rows:
            pid = p.get("id")
            if not pid or pid in seen:
                continue
            fresh += 1
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
        print(f"OK {sub} '{q}': +{fresh} new (total {len(seen)})")
        time.sleep(4)

with open(OUT, "w", encoding="utf-8") as fh:
    for row in seen.values():
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")

rows = sorted(seen.values(), key=lambda r: (r["num_comments"] or 0), reverse=True)
print(f"\nTOTAL unique candidates: {len(rows)}; by comments:\n")
for r in rows[:50]:
    print(f"{r['score']:>5} {r['num_comments']:>4}c  r/{r['subreddit']:<15} {r['id']}  {r['title'][:110]}")
