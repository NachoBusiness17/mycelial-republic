# Arctic Shift sweep: r/LocalLLaMA quantization posts, last 30 days (2026-09-03..2026-10-03)
# Part of frontier_olm sweep quantization-and-compression-reddit. Temporary tool, disposable.
import json, subprocess, time, datetime

def fetch(url):
    out = subprocess.run(["curl", "-s", "-m", "40", url], capture_output=True, text=True, creationflags=0x08000000)
    return json.loads(out.stdout)

posts = []
after = None
for page in range(6):
    url = "https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=LocalLLaMA&limit=100&after=1780492800"
    if after:
        url += "&before=" + str(after)
    d = fetch(url)
    batch = d.get("data", [])
    if not batch:
        break
    posts.extend(batch)
    after = batch[-1]["created_utc"]
    time.sleep(1)

print("total fetched: %d" % len(posts))
KW = ["quant", "q4", "q8", "gguf", "nvfp4", "w4a4", "1-bit", "2-bit", "1.58", "awq",
      "gptq", "kv cache quant", "iq2", "ik_", "unsloth quant", "k-quant", "bitnet", "compression"]
hits = []
for p in posts:
    t = (p.get("title") or "").lower()
    st = (p.get("selftext") or "")[:400].lower()
    blob = t + " " + st
    if any(k in blob for k in KW):
        hits.append(p)

hits.sort(key=lambda p: -(p.get("score") or 0))
print("quant-related: %d" % len(hits))
for p in hits[:45]:
    dt = datetime.datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d")
    gist = (p.get("selftext") or "").replace("\n", " ")[:120]
    print("%s | score=%s | c=%s | %s | id=%s | %s" % (dt, p.get("score"), p.get("num_comments"), p["title"], p["id"], gist))
