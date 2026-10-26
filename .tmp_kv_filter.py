import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
with open(".tmp_kv_arctic_candidates.json", encoding="utf-8") as f:
    items = json.load(f)
print("total:", len(items))
kw = ["kv", "prefix", "compaction", "compact ", "context engineering", "long context",
      "lmcache", "radix", "prompt cache", "caching", "summariz", "prefill", "context window",
      "context length", "vllm", "sglang", "llama.cpp server", "llama-server", "offload",
      "context offload", "attention", "context compression", "needle"]
seen = set(); hits = []
for it in items:
    t = (it.get("title") or "").lower()
    st = (it.get("selftext_head") or "").lower()
    hay = t + " " + st[:200]
    if any(k in hay for k in kw):
        key = it["id"]
        if key in seen: continue
        seen.add(key)
        hits.append(it)
hits.sort(key=lambda x: (x.get("score") or 0), reverse=True)
print("keyword hits:", len(hits))
for h in hits[:90]:
    print(f"{h['score']:>5} {h['date']} [{h['subreddit']}] {h['num_comments']:>4}c {h['id']} {h['title'][:110]}")
