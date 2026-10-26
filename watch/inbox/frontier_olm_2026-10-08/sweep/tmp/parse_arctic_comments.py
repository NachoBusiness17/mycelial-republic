"""Print top comments per thread from arctic-shift payloads, sorted by score.

Scratch instrument for sweep-open-local-models-reddit, 2026-10-08.
Usage: python parse_arctic_comments.py <thread_id> <top_n> [body_limit]
"""
import json
import sys

RAW = (
    r"C:/Users/foste/Documents/projects/local_sovereign_agent"
    r"/watch/inbox/frontier_olm_2026-10-08/sweep/_raw"
)
tid = sys.argv[1]
top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
body_limit = int(sys.argv[3]) if len(sys.argv) > 3 else 600

d = json.load(open(f"{RAW}/arctic_comments_{tid}.json", encoding="utf-8"))
rows = d.get("data", [])
rows = [r for r in rows if not r.get("author_deleted") and (r.get("author") or "").strip() not in ("[deleted]", "AutoModerator")]
rows.sort(key=lambda r: r.get("score") or 0, reverse=True)
print(f"### {tid}: {len(rows)} live comments (of {len(d.get('data', []))} pulled)")
for r in rows[:top_n]:
    body = (r.get("body") or "").strip().replace("\r", "")
    print("-" * 90)
    print(f"u/{r.get('author')} | {r.get('score')} pts | {r.get('created_utc')}")
    print(body[:body_limit])
print()
