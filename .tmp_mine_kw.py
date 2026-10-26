import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
root = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
with open(root + r"\.tmp_sweep_candidates.json", encoding="utf-8") as f:
    items = json.load(f)
kw = ["kv", "cache", "caching", "prefix", "context", "compact", "summariz", "tokenlat",
      "lmcache", "sglang", "vllm", "long context", "long-context", "attention", "memory",
      "agent", "prompt", "ordering", "needle", "tool call", "conversation"]
seen = set()
hits = []
for it in items:
    t = str(it.get("title", ""))
    tl = t.lower()
    if any(k in tl for k in kw):
        key = t[:80]
        if key in seen: continue
        seen.add(key)
        hits.append((it.get("date","?"), it.get("score",""), t, str(it.get("url",""))[:120]))
hits.sort(key=lambda x: str(x[1]), reverse=True)
print("total hits:", len(hits))
for h in hits[:70]:
    print(f"{h[0]} | {h[1]} | {h[2][:120]}")
    print(f"    {h[3]}")
# also show top-scored items overall for sense of the file
tops = sorted(items, key=lambda x: int(x.get("score", 0) or 0), reverse=True)[:15]
print("---- top overall ----")
for t in tops:
    print(f"{t.get('date','?')} | {t.get('score','')} | {str(t.get('title',''))[:110]}")
