import json, time, urllib.request, urllib.parse, sys, io
from datetime import datetime, timezone, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

NOW = datetime.now(timezone.utc)
CUT_I = int((NOW - timedelta(days=30)).timestamp()); NOW_I = int(NOW.timestamp())
BASE = "https://api.pullpush.io/reddit/search/submission/"
QUERIES = [
    ("llama_kvcache", {"subreddit": "LocalLLaMA", "q": "\"KV cache\""}),
    ("llama_prefix", {"subreddit": "LocalLLaMA", "q": "\"prefix caching\""}),
    ("llama_compact", {"subreddit": "LocalLLaMA", "q": "compaction"}),
    ("llama_ctxeng", {"subreddit": "LocalLLaMA", "q": "\"context engineering\""}),
    ("q_lmcache", {"q": "LMCache"}),
    ("ml_longctx", {"subreddit": "MachineLearning", "q": "\"long context\""}),
]

def fetch(label, params):
    p = dict(params); p.update({"sort": "desc", "sort_type": "score", "size": "100", "after": CUT_I})
    url = BASE + "?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": "estate-frontier-sweep/1.0 (kv-cache-context)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
        rows = d.get("data", [])
        print(f"{label}: {len(rows)} rows", flush=True)
        return rows
    except Exception as e:
        print(f"{label}: FAIL {e}", flush=True)
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
    time.sleep(20)

out = []
for sid, s in all_rows.items():
    out.append({
        "id": sid, "subreddit": s.get("subreddit"), "title": s.get("title"),
        "created_utc": s.get("created_utc"),
        "date": time.strftime("%Y-%m-%d", time.gmtime(s.get("created_utc", 0))),
        "score": s.get("score"), "num_comments": s.get("num_comments"),
        "permalink": "https://www.reddit.com" + (s.get("permalink") or ""),
        "selftext_len": len(s.get("selftext") or ""), "found_by": s.get("_found_by"),
        "selftext_head": (s.get("selftext") or "")[:400],
    })
out.sort(key=lambda x: (x["score"] or 0), reverse=True)
with open(".tmp_kv_pass1b_candidates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("TOTAL UNIQUE IN-WINDOW:", len(out), flush=True)
for o in out[:80]:
    print(f"{o['score']:>6} {o['date']} [{o['subreddit']}] {o['num_comments']:>4}c {o['title'][:100]}", flush=True)
print("PASS1B DONE", flush=True)
