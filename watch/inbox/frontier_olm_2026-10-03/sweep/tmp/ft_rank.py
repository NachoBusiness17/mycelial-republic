# Pass-1 ranker for finetuning-and-adaptation-reddit sweep, frontier_olm 2026-10-03.
# Reuses the sibling's Arctic Shift post pool (candidates_full.jsonl, same date
# window) and adds r/MachineLearning (not in the sibling's SUBS). Door:
# arctic-shift.photon-reddit.com per sw2_crawl.py header / lens burns.md door note.
# Disposable tool. urllib direct, no subprocess spawn.
import json, time, datetime, urllib.request, sys

BASE = "https://arctic-shift.photon-reddit.com/api"
FIELDS = "id,subreddit,created_utc,title,score,num_comments,author,selftext"
POOL = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep\tmp\candidates_full.jsonl"

KW = ["lora", "qlora", "fine-tun", "finetun", "fine tun", "adapter", "ternary",
      "bitnet", "1.58", "unsloth", "axolotl", "peft", "sft ", "dpo", "rlhf",
      "reward model", "grader", "judge", "test-time", "test time", "self-train",
      "self train", "training data", "dataset for training", "train a model",
      "trained on my", "train on my", "gemma", "gemma3", "gemma 3"]

rows = []
with open(POOL, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass

# add r/MachineLearning top month (not in sibling SUBS)
def get(url, tries=3):
    delay = 4
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("  try %d failed: %s" % (i + 1, e), flush=True)
            time.sleep(delay)
            delay *= 2
    return None

ml_rows = []
cursor = None
for page in range(8):
    url = ("%s/posts/search?subreddit=MachineLearning&after=2026-09-03&before=2026-10-05&limit=100&fields=%s"
           % (BASE, FIELDS))
    if cursor:
        url += "&before=%d" % cursor
    d = get(url)
    if not d or not d.get("data"):
        break
    posts = d["data"]
    ml_rows.extend(posts)
    if len(posts) < 100:
        break
    cursor = min(p["created_utc"] for p in posts)
    time.sleep(0.7)
print("MachineLearning fetched: %d" % len(ml_rows), flush=True)
rows.extend(ml_rows)

per_sub = {}
for p in rows:
    per_sub[p.get("subreddit", "?")] = per_sub.get(p.get("subreddit", "?"), 0) + 1
print("pool subs: %s" % json.dumps(per_sub), flush=True)

hits = []
for p in rows:
    blob = ((p.get("title") or "") + " " + (p.get("selftext") or "")[:600]).lower()
    m = sorted({k for k in KW if k in blob})
    if m:
        p["_kw"] = m
        hits.append(p)
hits.sort(key=lambda p: (-(p.get("score") or 0) - 5 * (p.get("num_comments") or 0)))
print("keyword hits: %d" % len(hits), flush=True)
for p in hits[:60]:
    dt = datetime.datetime.fromtimestamp(p["created_utc"], datetime.timezone.utc).strftime("%Y-%m-%d")
    gist = (p.get("selftext") or "").replace("\n", " ")[:130]
    print("%s | s=%s c=%s | r/%s | id=%s | kw=%s | %s | %s" % (
        dt, p.get("score"), p.get("num_comments"), p.get("subreddit"), p["id"],
        ",".join(p["_kw"][:6]), p.get("title", "")[:95], gist), flush=True)

with open(r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep\tmp\ft_hits.jsonl", "w", encoding="utf-8") as f:
    for p in hits:
        f.write(json.dumps(p, ensure_ascii=False) + "\n")
