"""Pass 1 broad sweep: finetuning-adaptation via reddit, arctic-shift archive door.

Fallback door: named old.reddit.com/r/<sub>/top.json doors 302 to a login HTML wall
(verified by curl -sL this session: final URL old.reddit.com/login/?reason=lor2).
arctic-shift.photon-reddit.com carried the 2026-10-10 adhoc sibling sweep and answers
this session too (HTTP 200 JSON). Window: 2026-09-11 .. 2026-10-12 (last 30 days).
"""
import json, time, urllib.request, urllib.parse, datetime, sys

OUT = r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/frontier_olm_2026-10-11/sweep/_ftr_candidates.json"
AFTER = "2026-09-11"
BEFORE = "2026-10-12"
SUBS = ["LocalLLaMA", "MachineLearning", "LocalLLM", "ollama"]
# Full-word title filters (archive 422s on partial words and many short acronyms).
QUERIES = [
    "LoRA", "finetuning", "fine-tuning", "finetune", "fine-tune",
    "Unsloth", "adapter", "distill", "distillation", "merging",
    "test-time", "training", "RL", "quantization-free", "gradient",
]
BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"

def get(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/2026-10-11"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            print(f"  retry {attempt+1} for {url[:120]}: {e}", flush=True)
            time.sleep(4)
    return None

pool = {}
def add(posts, src):
    for p in posts or []:
        pid = p.get("id")
        if not pid or pid in pool:
            continue
        pool[pid] = {
            "id": pid, "sub": p.get("subreddit"), "title": p.get("title"),
            "score": p.get("score"), "created": p.get("created_utc"),
            "num_comments": p.get("num_comments"), "url": "https://www.reddit.com" + (p.get("permalink") or ""),
            "selftext": (p.get("selftext") or "")[:900], "src": src,
        }

for sub in SUBS:
    for q in QUERIES:
        u = f"{BASE}?subreddit={sub}&limit=100&after={AFTER}&before={BEFORE}&sort=desc&title={urllib.parse.quote(q)}"
        d = get(u)
        n = len((d or {}).get("data") or [])
        add((d or {}).get("data"), f"title:{q}")
        print(f"{sub} title={q!r}: {n} rows", flush=True)
        time.sleep(1.2)

# Score-ranked full-window pages per sub (no title filter), 3 pages each.
for sub in SUBS:
    for page in range(3):
        u = f"{BASE}?subreddit={sub}&limit=100&after={AFTER}&before={BEFORE}&sort=desc&page={page}"
        d = get(u)
        rows = (d or {}).get("data") or []
        add(rows, f"window:p{page}")
        print(f"{sub} window p{page}: {len(rows)} rows", flush=True)
        time.sleep(1.2)
        if len(rows) < 100:
            break

# Rank: keep everything, sort by score desc for triage.
rows = sorted(pool.values(), key=lambda r: (r["score"] or 0), reverse=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=1)
print(f"TOTAL distinct candidates: {len(rows)} -> {OUT}", flush=True)
