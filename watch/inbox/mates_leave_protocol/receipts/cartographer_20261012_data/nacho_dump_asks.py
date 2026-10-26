import json
import sys
from pathlib import Path

out = Path("watch/inbox/mates_leave_protocol/receipts/cartographer_20261012_data")
dump = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("nacho_asks_dump.txt")
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 200

lines = []
for tid in ("4a30dd44", "3d371c13"):
    rows = [json.loads(l) for l in (out / ("nacho_parent_asks_" + tid + ".jsonl")).open(encoding="utf-8")]
    lines.append(f"===== {tid} {len(rows)} asks")
    for i, a in enumerate(rows):
        t = a["text"].replace("\n", " | ")
        lines.append(f"{i + 1}. [{a['ts']}] {t[:limit]}")
dump.write_text("\n".join(lines), encoding="utf-8")
print("wrote", dump, len(lines), "rows")
