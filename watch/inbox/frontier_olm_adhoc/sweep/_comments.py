"""Fetch comment trees for deep-read threads via arctic-shift."""
import json, time, urllib.request, urllib.parse

UA = {"User-Agent": "mag-estate-frontier-gopher/1.0 (research sweep)"}
OUT = r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/frontier_olm_adhoc/sweep"

def fetch_comments(link_id, limit=100):
    url = "https://arctic-shift.photon-reddit.com/api/comments/search?" + urllib.parse.urlencode(
        {"link_id": link_id, "limit": limit, "sort": "desc"})
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r).get("data") or []

for lid in ["1wgszma", "1wyui4o", "1wyc2b0"]:
    for attempt in range(3):
        try:
            cs = fetch_comments(lid)
            cs.sort(key=lambda c: -(c.get("score") or 0))
            print("=" * 90)
            print(f"THREAD {lid}: {len(cs)} comments fetched")
            for c in cs[:12]:
                body = (c.get("body") or "").replace("\n", " ")[:400]
                print(f'[{c.get("score")}|{c.get("author")}] {body}')
            with open(f"{OUT}/_comments_{lid}.json", "w", encoding="utf-8") as f:
                json.dump(cs, f)
            break
        except Exception as e:
            print("ERR", lid, str(e)[:160]); time.sleep(5 + attempt * 5)
    time.sleep(2)
