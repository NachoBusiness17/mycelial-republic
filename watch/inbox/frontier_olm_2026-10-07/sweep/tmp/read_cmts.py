"""Project arctic-shift comment trees: top-level comments by score, with bodies."""
import json
import sys
from pathlib import Path

p = Path(sys.argv[1])
data = json.loads(p.read_text(encoding="utf-8"))
rows = data.get("data", data) if isinstance(data, dict) else data
tops = [r for r in rows if not r.get("parent_id") or r.get("parent_id", "").startswith("t3_")]
tops.sort(key=lambda r: -(r.get("score") or 0))
print(f"total comments fetched: {len(rows)}; top-level: {len(tops)}")
for r in tops[:15]:
    body = (r.get("body") or "").replace("\n", " ")[:420]
    print(f"[{r.get('score'):>4}] u/{r.get('author')}: {body}")
