import json, time, urllib.request, urllib.parse, sys, datetime

BASE = "https://arctic-shift.photon-reddit.com/api"
OUT = "candidates.jsonl"
AFTER = "2026-09-03"
BEFORE = "2026-10-04"
FIELDS = "id,subreddit,created_utc,title,score,num_comments,author,selftext"
SUBS = ["LocalLLaMA", "ClaudeCode", "ClaudeAI", "AI_Agents", "aiagents", "LLMDevs",
        "LocalLLM", "ollama", "claudeskills", "LangChain", "Anthropic"]

def get(url, tries=4):
    delay = 4
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print(f"  try {i+1} failed: {e}; backoff {delay}s", flush=True)
            time.sleep(delay)
            delay *= 2
    return None

seen = set()
with open(OUT, "a", encoding="utf-8") as f:
    for sub in SUBS:
        after = AFTER
        got_any = False
        for page in range(4):  # up to 400 posts per sub
            url = (f"{BASE}/posts/search?subreddit={sub}&after={after}&before={BEFORE}"
                   f"&limit=100&fields={FIELDS}")
            d = get(url)
            if not d or not d.get("data"):
                print(f"{sub}: no data (page {page})", flush=True)
                break
            posts = d["data"]
            for p in posts:
                if p["id"] in seen:
                    continue
                seen.add(p["id"])
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
            got_any = True
            print(f"{sub} page {page}: +{len(posts)} (window oldest {posts[-1]['created_utc']})", flush=True)
            if len(posts) < 100:
                break
            after = datetime.datetime.fromtimestamp(
                posts[-1]["created_utc"], datetime.timezone.utc).strftime("%Y-%m-%d")
            time.sleep(4)
        time.sleep(4)
print(f"total candidates: {len(seen)}")
