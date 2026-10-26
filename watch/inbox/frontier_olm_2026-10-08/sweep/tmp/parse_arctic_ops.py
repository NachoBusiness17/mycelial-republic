"""Project arctic-shift /api/posts/ids payloads: id, date, score, comments, title, selftext.

Scratch instrument for sweep-open-local-models-reddit, 2026-10-08.
"""
import json
import sys

PATH = (
    r"C:/Users/foste/Documents/projects/local_sovereign_agent"
    r"/watch/inbox/frontier_olm_2026-10-08/sweep/_raw/arctic_ops_batch1.json"
)
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 1400

d = json.load(open(PATH, encoding="utf-8"))
rows = d.get("data") or d if isinstance(d, list) else d.get("data", [])
for p in rows:
    print("=" * 100)
    print(
        p.get("id"), "|", p.get("subreddit"), "|",
        p.get("created_utc"), "| score", p.get("score"), "| comments", p.get("num_comments"),
    )
    print("TITLE:", (p.get("title") or "").strip())
    body = (p.get("selftext") or "").strip()
    print("LINK:", p.get("url"))
    print("BODY:", body[:LIMIT].replace("\r", ""))
    print()
