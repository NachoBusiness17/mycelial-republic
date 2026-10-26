"""tmp_ff_deep_read.py - inference-efficiency reddit sweep, pass 2 (2026-10-06).

Fetches full post JSON + top comments for chosen thread ids via arctic-shift
(curl.exe subprocess, CREATE_NO_WINDOW). Evidence lands in sweep/doors/ff_deep/.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

CREATE_NO_WINDOW = 0x08000000
REPO_ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = (REPO_ROOT / "watch/inbox/frontier_olm_2026-10-06/sweep/doors/ff_deep").resolve()
OUT_DIR.mkdir(parents=True, exist_ok=True)

POST_FIELDS = ("id,subreddit,title,score,num_comments,created_utc,selftext,url,"
               "link_flair_text,author")
COMMENT_FIELDS = "id,author,body,score,created_utc,parent_id"


def curl_json(url):
    for attempt in range(4):
        r = subprocess.run(
            ["curl.exe", "-s", "--max-time", "60", "-A",
             "frontier-sweep/1.0 (research; local-sovereign-agent)", url],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            creationflags=CREATE_NO_WINDOW)
        body = (r.stdout or "").strip()
        if body:
            try:
                d = json.loads(body)
                if isinstance(d, dict) and not d.get("error"):
                    return d
                print(f"  api error: {(d or {}).get('error')}", file=sys.stderr)
            except json.JSONDecodeError:
                print(f"  non-json body len={len(body)}", file=sys.stderr)
        time.sleep(6 + attempt * 6)
    return None


def main():
    ids = sys.argv[1:]
    for pid in ids:
        pf = OUT_DIR / f"{pid}.post.json"
        if not pf.exists():
            d = curl_json(f"https://arctic-shift.photon-reddit.com/api/posts/ids?ids={pid}&fields={POST_FIELDS}")
            if not d or not d.get("data"):
                print(f"{pid}: POST FETCH FAILED", file=sys.stderr)
                continue
            pf.write_text(json.dumps(d["data"][0], ensure_ascii=False, indent=1), encoding="utf-8")
        # comments: up to 3 pages of 100, top-heavy by score if the API allows
        cf = OUT_DIR / f"{pid}.comments.json"
        if not cf.exists():
            allc = []
            after = None
            for _page in range(3):
                u = (f"https://arctic-shift.photon-reddit.com/api/comments/search"
                     f"?link_id={pid}&limit=100&fields={COMMENT_FIELDS}&sort=desc")
                if after:
                    u += f"&after={after}"
                d = curl_json(u)
                if not d or not d.get("data"):
                    break
                allc.extend(d["data"])
                if len(d["data"]) < 100:
                    break
                after = d["data"][-1]["created_utc"]
                time.sleep(2)
            allc.sort(key=lambda c: c.get("score") or 0, reverse=True)
            cf.write_text(json.dumps(allc, ensure_ascii=False, indent=1), encoding="utf-8")
        post = json.loads(pf.read_text(encoding="utf-8"))
        ncom = len(json.loads(cf.read_text(encoding="utf-8")))
        print(f"{pid}: score={post.get('score')} selftext={len(post.get('selftext') or '')}ch "
              f"url={post.get('url')} comments_fetched={ncom}")


if __name__ == "__main__":
    sys.exit(main())
