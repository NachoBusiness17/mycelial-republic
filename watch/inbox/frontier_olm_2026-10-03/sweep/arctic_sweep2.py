# Arctic Shift sweep round 2: r/LocalLLM, r/ollama, r/MachineLearning + specific ids + dates
import json, subprocess, time, datetime

def fetch(url):
    out = subprocess.run(["curl", "-s", "-m", "40", url], capture_output=True, text=True, creationflags=0x08000000)
    return json.loads(out.stdout)

def dt(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")

KW = ["quant", "q4", "q8", "gguf", "nvfp4", "w4a4", "1-bit", "2-bit", "1.58", "awq",
      "gptq", "iq2", "ik_", "k-quant", "bitnet", "compression", "prune", "bpw"]

for sub in ["LocalLLM", "ollama", "MachineLearning"]:
    posts = []
    after = None
    for page in range(3):
        url = "https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=%s&limit=100&after=1780492800" % sub
        if after:
            url += "&before=" + str(after)
        d = fetch(url)
        batch = d.get("data", [])
        if not batch:
            break
        posts.extend(batch)
        after = batch[-1]["created_utc"]
        time.sleep(1)
    hits = []
    for p in posts:
        blob = ((p.get("title") or "") + " " + (p.get("selftext") or "")[:400]).lower()
        if any(k in blob for k in KW):
            hits.append(p)
    hits.sort(key=lambda p: -(p.get("score") or 0))
    print("=== r/%s: fetched %d, quant-related %d" % (sub, len(posts), len(hits)))
    for p in hits[:15]:
        gist = (p.get("selftext") or "").replace("\n", " ")[:110]
        print("%s | score=%s | c=%s | %s | id=%s | %s" % (dt(p["created_utc"]), p.get("score"), p.get("num_comments"), p["title"], p["id"], gist))
    time.sleep(1)

# date check on WebSearch-found ids
ids = ["1us7a22", "1vsmrwn", "1sxzqry", "1usniqh", "1v1tr2b", "1n3ezr4", "1pyrjke", "1rfds1h", "1s88x5g", "1tfqfvt", "1tyfnqi", "1tzlt37", "1vwt6m7", "1mwevt4"]
print("=== specific id dates ===")
for i in ids:
    d = fetch("https://arctic-shift.photon-reddit.com/api/posts/ids?ids=" + i)
    rows = d.get("data", [])
    if rows:
        p = rows[0]
        print("%s | r/%s | %s | score=%s c=%s | %s" % (i, p.get("subreddit"), dt(p["created_utc"]), p.get("score"), p.get("num_comments"), p["title"][:90]))
    else:
        print("%s | NOT FOUND" % i)
    time.sleep(0.5)
