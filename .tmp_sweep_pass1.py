import json, time, urllib.request, urllib.parse, sys

CUTOFF = 1788619888  # 2026-09-05T14:51Z
NOW = 1791211888

BASE = "https://api.pullpush.io/reddit/search/submission/"

QUERIES = [
    # (label, params)
    ("llama_top", {"subreddit": "LocalLLaMA", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("localllm_top", {"subreddit": "LocalLLM", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("ollama_top", {"subreddit": "ollama", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("ml_top", {"subreddit": "MachineLearning", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_quant", {"q": "quantization", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_q4", {"q": "Q4", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_toolcall", {"q": "\"tool calling\"", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_json", {"q": "structured output", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_compress", {"q": "context compression", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
    ("q_awq", {"q": "AWQ", "after": CUTOFF, "sort": "desc", "sort_type": "score", "size": "100"}),
]

def fetch(label, params):
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "research-sweep/1.0 (estate frontier sweep)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                d = json.load(r)
            rows = d.get("data", [])
            print(f"{label}: {len(rows)} rows", flush=True)
            return rows
        except Exception as e:
            print(f"{label}: attempt {attempt} error {e}", flush=True)
            time.sleep(8)
    return []

all_rows = {}
for label, params in QUERIES:
    rows = fetch(label, params)
    for s in rows:
        sid = s.get("id")
        if not sid:
            continue
        cu = s.get("created_utc", 0)
        if cu < CUTOFF or cu > NOW + 3600:
            continue  # hard window filter
        if sid not in all_rows:
            s["_found_by"] = label
            all_rows[sid] = s
    time.sleep(4)  # be polite to pullpush

out = []
for sid, s in all_rows.items():
    out.append({
        "id": sid,
        "subreddit": s.get("subreddit"),
        "title": s.get("title"),
        "created_utc": s.get("created_utc"),
        "date": time.strftime("%Y-%m-%d", time.gmtime(s.get("created_utc", 0))),
        "score": s.get("score"),
        "num_comments": s.get("num_comments"),
        "permalink": "https://www.reddit.com" + s.get("permalink", ""),
        "selftext_len": len(s.get("selftext") or ""),
        "found_by": s.get("_found_by"),
        "selftext_head": (s.get("selftext") or "")[:220],
    })

out.sort(key=lambda x: (x["score"] or 0), reverse=True)
with open(".tmp_sweep_candidates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("TOTAL UNIQUE IN-WINDOW:", len(out), flush=True)
for o in out[:60]:
    print(f"{o['score']:>6} {o['date']} [{o['subreddit']}] {o['num_comments']:>4}c {o['title'][:95]}")
