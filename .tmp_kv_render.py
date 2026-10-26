import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
OUT = ".tmp_kv_deep"

def render(sid):
    with open(f"{OUT}/sub_{sid}.json", encoding="utf-8") as f:
        s = json.load(f)
    with open(f"{OUT}/com_{sid}.json", encoding="utf-8") as f:
        coms = json.load(f)
    lines = []
    lines.append(f"ID {sid} [{s.get('subreddit')}] {s.get('title')}")
    lines.append(f"date={s.get('created_utc')} score={s.get('score')} comments={s.get('num_comments')} author={s.get('author')} url={s.get('url')}")
    lines.append("PERMALINK https://www.reddit.com" + (s.get("permalink") or ""))
    body = (s.get("selftext") or "").strip()
    lines.append("SELFTEXT:")
    lines.append(body if body else "(empty)")
    coms.sort(key=lambda c: (c.get("score") or 0), reverse=True)
    lines.append(f"COMMENTS ({len(coms)}, top-scored order):")
    for c in coms:
        a = (c.get("body") or "").replace("\r", "").strip()
        lines.append(f"--- {c.get('author')} ({c.get('score')}): {a}")
    txt = "\n".join(lines)
    with open(f"{OUT}/read_{sid}.txt", "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"{sid}: {len(txt)} chars, {len(coms)} comments")

for sid in ["1wd4xxv", "1whx5xi", "1weolwq", "1wbgqnp", "1wn6vwm", "1wlss89", "1wdaq1v", "1wtg12r", "1wiu7xj"]:
    try:
        render(sid)
    except Exception as e:
        print(sid, "ERR", e)
