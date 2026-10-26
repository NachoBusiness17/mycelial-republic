"""Compact-project the arctic-shift ids payload: id, date, score, comments, selftext head."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

p = Path(sys.argv[1])
data = json.loads(p.read_text(encoding="utf-8"))
rows = data.get("data", data) if isinstance(data, dict) else data
for r in rows:
    ts = r.get("created_utc")
    when = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat() if ts else "?"
    print("=" * 80)
    print(f"{r.get('id')}  {when}  score={r.get('score')}  comments={r.get('num_comments')}  subreddit={r.get('subreddit')}")
    print(f"TITLE: {r.get('title')}")
    st = (r.get("selftext") or "")[:1200]
    print(f"SELFTEXT: {st}")
