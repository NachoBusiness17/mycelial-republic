import json, time, urllib.request, urllib.parse, datetime

AFTER = 1785628800  # 2026-08-31T00:00:00Z
BASE = "https://api.pullpush.io/reddit/search/submission/"

QUERIES = [
    ("LocalLLaMA", "memory"),
    ("LocalLLaMA", "knowledge graph"),
    ("LocalLLaMA", "session"),
    ("LocalLLaMA", "context"),
    ("MachineLearning", "memory"),
    ("MachineLearning", "agent"),
    ("LocalLLM", "memory"),
    ("ollama", "memory"),
    ("AI_Agents", "memory"),
    ("AI_Agents", "knowledge graph"),
    ("Rag", "memory"),
    ("Rag", "knowledge graph"),
    ("LangChain", "memory"),
    ("AIMemory", None),
    ("LLMDevs", "memory"),
    ("ClaudeCode", "memory"),
    ("KnowledgeGraph", "identity resolution"),
    ("hermesagent", None),
]

seen = {}
for sub, q in QUERIES:
    params = {"subreddit": sub, "after": str(AFTER), "sort_type": "score",
              "sort": "desc", "size": "50"}
    if q:
        params["q"] = q
    url = BASE + "?" + urllib.parse.urlencode(params)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "frontier-sweep-research/1.0"})
        with urllib.request.urlopen(req, timeout=40) as r:
            d = json.load(r)
    except Exception as e:
        print(f"ERR {sub}/{q}: {e}", flush=True)
        time.sleep(3)
        continue
    rows = d.get("data", [])
    for s in rows:
        sid = s.get("id")
        if sid and sid not in seen:
            seen[sid] = s
    print(f"OK {sub}/{q}: {len(rows)} rows (total unique {len(seen)})", flush=True)
    time.sleep(2)

out = []
for s in seen.values():
    out.append({
        "id": s.get("id"),
        "sub": s.get("subreddit"),
        "title": (s.get("title") or "")[:160],
        "utc": datetime.datetime.utcfromtimestamp(s["created_utc"]).isoformat() if s.get("created_utc") else "?",
        "score": s.get("score"),
        "comments": s.get("num_comments"),
        "selftext_len": len(s.get("selftext") or ""),
        "permalink": "https://old.reddit.com" + (s.get("permalink") or ""),
    })
out.sort(key=lambda x: -(x["score"] or 0))
with open("_sweep_pp_memory_pool.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
for r in out:
    print(f"{r['score']:>6} {r['comments']:>4} {r['utc'][:10]} r/{r['sub']:<14} {r['id']} {r['title'][:100]}")
