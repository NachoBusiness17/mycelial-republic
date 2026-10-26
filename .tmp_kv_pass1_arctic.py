import json, urllib.request, urllib.parse, sys, io, time, socket, ipaddress
from datetime import datetime, timezone, timedelta
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Mimosa SSRF guard: https-only, fixed allowlist host, resolve + block private/loopback/link-local
ALLOWED_HOST = "arctic-shift.photon-reddit.com"
_addrs = {ai[4][0] for ai in socket.getaddrinfo(ALLOWED_HOST, 443, proto=socket.IPPROTO_TCP)}
for a in _addrs:
    ip = ipaddress.ip_address(a)
    assert not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved), f"blocked {a}"
BASE = "https://" + ALLOWED_HOST + "/api"

NOW = datetime.now(timezone.utc)
CUT_I = int((NOW - timedelta(days=30)).timestamp())
NOW_I = int(NOW.timestamp())
print("window:", datetime.fromtimestamp(CUT_I, timezone.utc).isoformat(), "->", datetime.fromtimestamp(NOW_I, timezone.utc).isoformat(), flush=True)

def get(path, params, timeout=60):
    assert path.startswith("/posts") or path.startswith("/comments")
    url = "https://" + ALLOWED_HOST + "/api" + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "estate-frontier-sweep/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r).get("data", [])
    except Exception as e:
        print(f"  FAIL {path} {params} -> {e}", flush=True)
        return None

all_rows = {}
def absorb(rows, label):
    if not rows: return 0
    kept = 0
    for s in rows:
        sid = s.get("id")
        if not sid: continue
        cu = s.get("created_utc", 0)
        if cu < CUT_I or cu > NOW_I + 3600: continue
        if sid not in all_rows:
            s["_found_by"] = label
            all_rows[sid] = s
            kept += 1
    return kept

# 1) keyword queries first (cheap if q is supported)
KW_QUERIES = [
    ("llama_kvcache", {"subreddit": "LocalLLaMA", "q": "KV cache"}),
    ("llama_prefix", {"subreddit": "LocalLLaMA", "q": "prefix caching"}),
    ("llama_compact", {"subreddit": "LocalLLaMA", "q": "compaction"}),
    ("llama_ctxeng", {"subreddit": "LocalLLaMA", "q": "context engineering"}),
    ("llama_lmcache", {"subreddit": "LocalLLaMA", "q": "LMCache"}),
    ("ml_longctx", {"subreddit": "MachineLearning", "q": "long context"}),
    ("ml_cache", {"subreddit": "MachineLearning", "q": "KV cache"}),
    ("localllm_ctx", {"subreddit": "LocalLLM", "q": "context"}),
    ("ollama_cache", {"subreddit": "ollama", "q": "cache"}),
]
q_supported = False
for label, p in KW_QUERIES:
    pp = dict(p); pp.update({"after": CUT_I, "limit": 100, "sort": "desc"})
    rows = get("/posts/search", pp)
    if rows is not None: q_supported = True
    absorb(rows, label)
    time.sleep(2.5)
print("q param supported:", q_supported, flush=True)

# 2) paged time sweeps per subreddit (covers what q missed)
for sub, max_pages in [("LocalLLaMA", 25), ("LocalLLM", 12), ("ollama", 12)]:
    before = NOW_I + 3600
    for page in range(max_pages):
        rows = get("/posts/search", {"subreddit": sub, "before": before, "limit": 100, "sort": "desc"})
        if not rows: break
        absorb(rows, f"sweep_{sub}")
        oldest = min((s.get("created_utc", 0) for s in rows), default=0)
        if oldest < CUT_I or oldest >= before: break
        before = oldest
        time.sleep(2.0)
    print(f"sweep {sub} done, cumulative unique in-window: {len(all_rows)}", flush=True)

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
with open(".tmp_kv_arctic_candidates.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("TOTAL UNIQUE IN-WINDOW:", len(out), flush=True)
for o in out[:80]:
    print(f"{o['score']:>6} {o['date']} [{o['subreddit']}] {o['num_comments']:>4}c {o['title'][:105]}", flush=True)
print("PASS1 DONE", flush=True)
