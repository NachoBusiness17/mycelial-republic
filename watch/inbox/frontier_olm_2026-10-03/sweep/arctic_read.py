# Pass 2 deep read: fetch full selftext + top comments for chosen threads via Arctic Shift
import json, subprocess, time, sys

def fetch(url):
    out = subprocess.run(["curl", "-s", "-m", "40", url], capture_output=True, text=True, creationflags=0x08000000)
    return json.loads(out.stdout)

ids = sys.argv[1:]
for pid in ids:
    d = fetch("https://arctic-shift.photon-reddit.com/api/posts/ids?ids=" + pid)
    rows = d.get("data", [])
    if not rows:
        print("### %s NOT FOUND" % pid)
        continue
    p = rows[0]
    print("=" * 100)
    print("### %s | r/%s | %s | score=%s c=%s" % (pid, p.get("subreddit"), p.get("title"), p.get("score"), p.get("num_comments")))
    print("URL: https://www.reddit.com/r/%s/comments/%s/" % (p.get("subreddit"), pid))
    print("SELFTEXT:")
    print((p.get("selftext") or "(empty)"))
    time.sleep(1)
    c = fetch("https://arctic-shift.photon-reddit.com/api/comments/search?link_id=%s&limit=60" % pid)
    comments = c.get("data", [])
    comments.sort(key=lambda x: -(x.get("score") or 0))
    print("TOP COMMENTS (%d fetched):" % len(comments))
    for cm in comments[:12]:
        body = (cm.get("body") or "").replace("\n", " | ")
        print("  [score=%s u=%s] %s" % (cm.get("score"), cm.get("author"), body[:700]))
    time.sleep(1)
