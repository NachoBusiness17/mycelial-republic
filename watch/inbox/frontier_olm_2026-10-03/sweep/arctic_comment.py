# Fetch full comment bodies for one thread
import json, subprocess, time, sys

def fetch(url):
    out = subprocess.run(["curl", "-s", "-m", "40", url], capture_output=True, text=True, creationflags=0x08000000)
    return json.loads(out.stdout)

pid = sys.argv[1]
c = fetch("https://arctic-shift.photon-reddit.com/api/comments/search?link_id=%s&limit=100" % pid)
comments = c.get("data", [])
comments.sort(key=lambda x: -(x.get("score") or 0))
for cm in comments:
    print("----- [score=%s u=%s id=%s]" % (cm.get("score"), cm.get("author"), cm.get("id")))
    print(cm.get("body") or "")
    print()
