"""Deep-read puller: full selftext + comments for shortlist ids via arctic-shift.

Writes raw JSON to _raw/deep_<id>_post.json and _raw/deep_<id>_comments.json
plus a readable digest _raw/deep_<id>.txt. Paced: 20s between API calls.
"""
import json
import time
import subprocess
import os
import sys
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
IDS = sys.argv[1:] or []


def call(url, tries=5):
    for attempt in range(1, tries + 1):
        r = subprocess.run(
            ["curl", "-s", "-m", "60", "-A", UA, url],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        try:
            d = json.loads(r.stdout)
        except Exception:
            d = None
        if isinstance(d, dict) and isinstance(d.get("data"), (list, dict)):
            return d
        err = (d or {}).get("error") if isinstance(d, dict) else (r.stdout[:80] if r.stdout else f"rc={r.returncode}")
        print(f"    retry {attempt}: {str(err)[:70]}", flush=True)
        time.sleep(25)
    return None


def main():
    for pid in IDS:
        print(f"== {pid} ==", flush=True)
        post = call(
            f"https://arctic-shift.photon-reddit.com/api/posts/ids?ids={pid}&md2html=false"
        )
        if not post or not (post.get("data") or []):
            print("    POST FETCH FAILED", flush=True)
            continue
        p = post["data"][0]
        with open(os.path.join(HERE, f"deep_{pid}_post.json"), "w", encoding="utf-8") as f:
            json.dump(p, f)
        dt = datetime.datetime.utcfromtimestamp(p["created_utc"]).strftime("%Y-%m-%d %H:%M")
        lines = [
            f"ID: {p['id']}",
            f"SUB: r/{p.get('subreddit')}",
            f"DATE: {dt} UTC (created_utc={p['created_utc']})",
            f"TITLE: {p.get('title')}",
            f"SCORE: {p.get('score')}  COMMENTS: {p.get('num_comments')}  UPVOTE_RATIO: {p.get('upvote_ratio')}",
            f"PERMALINK: https://www.reddit.com{p.get('permalink','')}",
            "SELFTEXT:",
            p.get("selftext") or "(empty)",
        ]
        time.sleep(20)
        com = call(
            f"https://arctic-shift.photon-reddit.com/api/comments/search?link_id={pid}&limit=100&sort=asc"
        )
        rows = (com or {}).get("data") or []
        with open(os.path.join(HERE, f"deep_{pid}_comments.json"), "w", encoding="utf-8") as f:
            json.dump(rows, f)
        lines.append(f"COMMENTS FETCHED: {len(rows)}")
        for c in rows:
            cd = datetime.datetime.utcfromtimestamp(c["created_utc"]).strftime("%Y-%m-%d")
            body = (c.get("body") or "").replace("\n", " ")
            lines.append(f"--- [{c.get('author')} | {cd} | score {c.get('score')}] {body}")
        with open(os.path.join(HERE, f"deep_{pid}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"    ok: {len((p.get('selftext') or ''))} chars selftext, {len(rows)} comments", flush=True)
        time.sleep(20)


if __name__ == "__main__":
    main()
