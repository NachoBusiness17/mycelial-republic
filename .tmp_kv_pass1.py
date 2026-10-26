import json, time, urllib.request, urllib.parse, sys, io, os
from datetime import datetime, timezone, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NOW = datetime.now(timezone.utc)
CUTOFF = NOW - timedelta(days=30)
NOW_I = int(NOW.timestamp()); CUT_I = int(CUTOFF.timestamp())
print("window:", CUTOFF.isoformat(), "->", NOW.isoformat(), flush=True)

BASE = "https://api.pullpush.io/reddit/search/submission/"
QUERIES = [
    ("llama_kvcache", {"subreddit": "LocalLLaMA", "q": "\"KV cache\"", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("llama_prefix", {"subreddit": "LocalLLaMA", "q": "\"prefix caching\"", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("llama_compact", {"subreddit": "LocalLLaMA", "q": "compaction", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("llama_ctxeng", {"subreddit": "LocalLLaMA", "q": "\"context engineering\"", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("llml_ctx", {"subreddit": "LocalLLM", "q": "context", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("ollama_ctx", {"subreddit": "ollama", "q": "context cache", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_lmcache", {"q": "LMCache", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_promptcache", {"q": "\"prompt caching\"", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_longcontext", {"subreddit": "LocalLLaMA", "q": "\"long context\"", "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_summarize", {"subreddit": "LocalLLaMA", "q": "summarize conversation agent", "sort": "desc", "sort_type": "score", "size": "100"}),
]

def fetch(label, params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "estate-frontier-sweep/1.0 (kv-cache-context-engineering)"})
    for attempt in range(2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.load(r)
            rows = d.get("data", [])
            print(f"{label}: {len(rows)} rows", flush=True)
            return rows
        except Exception as e:
            print(f"{label}: attempt {attempt} error {e}", flush=True)
            time.sleep(6)
    return []

all_rows = {}
for label, params in QUERIES:
    rows = fetch(label, params)
    for s in rows:
        sid = s.get("id")
        if not sid: continue
        cu = s.get("created_utc", 0)
        if cu < CUT_I or cu > NOW_I + 3600: continue
        if sid not in all_rows:
            s["_found_by"] = label
            all_rows[sid] = s
    time.sleep(4)

out = []
for sid, s in all_rows.items():
    out.append({
        "id": sid, "subreddit": s.get("subreddit"), "title": s.get("title"),
        "created_utc": s.get("created_utc"),
        "date": time.strftime("%Y-%m-%d", time.gmtime(s.get("created_utc", 0))),
        "score": s.get("score"), "num_comments": s.get("num_comments"),
        "permalink": "https://www.reddit.com" + (s.get("permalink") or ""),
        "selftext_len": len(s.get("selftext") or ""), "found_by": s.get("_found_by"),
        "selftext_head": (s.get("selftext") or "")[:300],
    })
out.sort(key=lambda x: (x["score"] or 0), reverse=True)
with open(".tmp_kv_pass1_candidates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("TOTAL UNIQUE IN-WINDOW:", len(out), flush=True)
for o in out[:60]:
    print(f"{o['score']:>6} {o['date']} [{o['subreddit']}] {o['num_comments']:>4}c {o['title'][:100]}", flush=True)
