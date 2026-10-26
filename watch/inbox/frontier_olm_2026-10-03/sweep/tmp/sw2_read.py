# Deep-read tool for window 2: fetch full post + comment tree per id from
# Arctic Shift, save raw bytes, print a readable digest. Disposable.
import json, time, datetime, urllib.request, sys, os

BASE = "https://arctic-shift.photon-reddit.com/api"
OUTDIR = os.path.dirname(os.path.abspath(__file__))

def get(url, tries=4):
    delay = 4
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("  fetch try %d failed: %s" % (i + 1, e), flush=True)
            time.sleep(delay)
            delay *= 2
    return None

for pid in sys.argv[1:]:
    d = get("%s/posts/ids?ids=%s&fields=id,subreddit,created_utc,title,score,num_comments,author,selftext,url" % (BASE, pid))
    if not d or not d.get("data"):
        print("NO POST for %s" % pid, flush=True)
        continue
    post = d["data"][0]
    comments, cursor = [], None
    for page in range(10):
        url = "%s/comments/search?link_id=%s&limit=100&fields=id,author,score,body,created_utc,parent_id" % (BASE, pid)
        if cursor:
            url += "&before=%d" % cursor
        c = get(url)
        if not c or not c.get("data"):
            break
        comments.extend(c["data"])
        if len(c["data"]) < 100:
            break
        cursor = c["data"][-1]["created_utc"]
        time.sleep(0.6)
    raw = {"post": post, "comments": comments}
    path = os.path.join(OUTDIR, "sw2_item_%s.json" % pid)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False)
    dt = datetime.datetime.fromtimestamp(post["created_utc"], datetime.timezone.utc).strftime("%Y-%m-%d")
    print("=" * 100, flush=True)
    print("[%s] r/%s | id=%s | score=%s | comments_fetched=%d (post claims %s)" % (
        dt, post["subreddit"], pid, post.get("score"), len(comments), post.get("num_comments")), flush=True)
    print("TITLE: %s" % post["title"], flush=True)
    st = post.get("selftext") or "(no selftext)"
    print("SELFTEXT (%d chars):" % len(st), flush=True)
    print(st[:3500], flush=True)
    print("--- TOP COMMENTS by score:", flush=True)
    for cm in sorted(comments, key=lambda c: -(c.get("score") or 0))[:14]:
        body = (cm.get("body") or "").replace("\n", " ")
        print("  [s=%s] u/%s: %s" % (cm.get("score"), cm.get("author"), body[:520]), flush=True)
    time.sleep(0.6)
