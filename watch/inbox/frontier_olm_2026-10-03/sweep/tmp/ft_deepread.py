# Pass-2 deep reads: finetuning-and-adaptation-reddit, frontier_olm 2026-10-03.
# Door: arctic-shift.photon-reddit.com (working reddit engine; see sw2_crawl.py
# header, same inbox). Full selftext from the sibling pool where present, rest
# via posts/search ids; comments via comments/search link_id. urllib direct.
import json, time, datetime, urllib.request, sys

BASE = "https://arctic-shift.photon-reddit.com/api"
POOL = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep\tmp\candidates_full.jsonl"
OUT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep\tmp\ft_deepread.json"

IDS = ["1wj6c4l", "1wjnklv", "1v0egoi", "1wgvfpr", "1wefk8o",
       "1wgxzvw", "1wavhij", "1w7umnd", "1wcqa03", "1weum85",
       "1wkorli", "1wkwz69"]

def get(url, tries=4):
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

posts = {}
with open(POOL, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            p = json.loads(line)
        except Exception:
            continue
        if p.get("id") in IDS:
            posts[p["id"]] = p

# fetch missing posts (e.g. 1v0egoi outside the sibling window) by id
missing = [i for i in IDS if i not in posts]
for mid in missing:
    d = get("%s/posts/ids?ids=%s" % (BASE, mid))
    if d and d.get("data"):
        for p in d["data"]:
            posts[p["id"]] = p
    else:
        d = get("%s/posts/search?ids=%s&fields=id,subreddit,created_utc,title,score,num_comments,author,selftext,permalink" % (BASE, mid))
        if d and d.get("data"):
            for p in d["data"]:
                posts[p["id"]] = p
    time.sleep(0.7)

result = {}
for pid in IDS:
    p = posts.get(pid)
    if not p:
        result[pid] = {"error": "post not found"}
        continue
    d = get("%s/comments/search?link_id=%s&limit=100&fields=id,author,body,created_utc,parent_id,score" % (BASE, pid))
    comments = (d or {}).get("data") or []
    comments.sort(key=lambda c: -(c.get("score") or 0))
    result[pid] = {"post": p, "comments": comments}
    time.sleep(0.7)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("saved %d threads" % len(result), flush=True)
for pid in IDS:
    r = result.get(pid, {})
    p = r.get("post")
    if not p:
        print("%s: MISSING" % pid, flush=True)
        continue
    dt = datetime.datetime.fromtimestamp(p["created_utc"], datetime.timezone.utc).strftime("%Y-%m-%d")
    print("%s | r/%s | %s | s=%s c=%d | %s" % (dt, p.get("subreddit"), pid, p.get("score"), len(r.get("comments", [])), p.get("title", "")[:100]), flush=True)
