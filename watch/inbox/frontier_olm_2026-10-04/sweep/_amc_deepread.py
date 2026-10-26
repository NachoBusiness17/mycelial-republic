"""Deep-read fetcher: full selftext + comment trees for chosen ids, via Arctic Shift.
Writes one .txt per id into the sweep dir; the seat then reads those files itself.
"""
import json, time, urllib.request, urllib.error, os, datetime

OUT_DIR = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-04\sweep"
BASE_P = "https://arctic-shift.photon-reddit.com/api/posts/search"
BASE_C = "https://arctic-shift.photon-reddit.com/api/comments/search"
IDS = ["1wjq4vh", "1wui0hj", "1wqudww", "1wpo86h", "1wg41et", "1wu31ir", "1wfzp1a", "1wwd5rd"]

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "mag-frontier-sweep/2026-10-04"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 422, 500, 502, 503):
                time.sleep(15 * (attempt + 1))
                continue
            raise
        except Exception:
            time.sleep(8)
    return None

def ts(epoch):
    return datetime.datetime.fromtimestamp(epoch or 0, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M") if epoch else "?"

def render_comment(c, depth, out):
    body = (c.get("body") or "").strip()
    out.append(f"{'  ' * depth}[{c.get('author')} | {ts(c.get('created_utc'))} | score {c.get('score')}] {body}")
    for child in c.get("_children", []):
        render_comment(child, depth + 1, out)

def main():
    for rid in IDS:
        p = get(f"https://arctic-shift.photon-reddit.com/api/posts/ids?ids={rid}")
        post = (p or {}).get("data", [None])[0]
        if not post:
            print(f"{rid}: post fetch failed", flush=True)
            continue
        out = [f"=== {rid} r/{post.get('subreddit')} | {ts(post.get('created_utc'))} | score {post.get('score')} | {post.get('num_comments')} comments | author u/{post.get('author')}",
               f"TITLE: {post.get('title')}",
               f"PERMALINK: {post.get('permalink')}",
               "SELFTEXT:", (post.get("selftext") or "(empty)").strip(), "", "COMMENTS:"]
        comments = []
        before = None
        for _ in range(30):
            url = f"{BASE_C}?link_id={rid}&limit=100"
            if before:
                url += f"&before={before}"
            data = get(url)
            if not data or not data.get("data"):
                break
            batch = data["data"]
            comments.extend(batch)
            before = min(int(c["created_utc"]) for c in batch if c.get("created_utc"))
            if len(batch) < 100:
                break
            time.sleep(1.2)
        # nest by parent_id
        by_id = {c["id"]: c for c in comments}
        for c in comments:
            c["_children"] = []
        roots = []
        for c in comments:
            pid = (c.get("parent_id") or "").split("_", 1)[-1]
            if pid in by_id and pid != c["id"]:
                by_id[pid]["_children"].append(c)
            else:
                roots.append(c)
        roots.sort(key=lambda c: -(c.get("score") or 0))
        for c in roots[:40]:
            render_comment(c, 1, out)
        out.append(f"\n(fetched {len(comments)} comments total; rendered top {min(40, len(roots))} roots by score)")
        path = os.path.join(OUT_DIR, f"_amc_thread_{rid}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print(f"{rid}: post ok, {len(comments)} comments -> {path}", flush=True)
        time.sleep(1.5)

if __name__ == "__main__":
    main()
