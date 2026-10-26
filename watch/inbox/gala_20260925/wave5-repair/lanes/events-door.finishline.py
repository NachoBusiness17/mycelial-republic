# Finish line for the events-door lane: the sanctioned loader serves every row
# with zero raise. Run with the repo venv python from the repo root.
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))))

from mag.link_library import EVENTS, load_events

lines = [l for l in EVENTS.read_text(encoding="utf-8").splitlines() if l.strip()]
print("file non-empty lines:", len(lines))
parsed = 0
for l in lines:  # every line must json-parse; any raise fails the run
    json.loads(l)
    parsed += 1
print("json.loads on every line: OK, zero raise, parsed", parsed)
rows = load_events()
print("load_events() served rows:", len(rows), "(expect 58 charter rows)")
bad = ["B2-142-HN-QWEN38-DIG", "B2-142-HN-CODEPLAN-DIG", "B2-142-TRIAL-SHAPES-LIVE",
       "B2-142-REDDIT-TRIAL-DECAY", "LINKS-329-CORRECTION"]
ids = {r.get("id") for r in rows}
on_file = [json.loads(l).get("id") for l in lines]
print("named debt skipped from service (id absent from served rows):",
      [b for b in bad if b not in ids])
print("named debt bytes still on file (no-erase):",
      all(b in on_file for b in bad))
print("carriers served:", [b + "-BACKFILL" for b in bad if b + "-BACKFILL" in ids])
ok = (parsed == 63 and len(rows) == 58
      and all(b in on_file for b in bad)
      and all(b + "-BACKFILL" in ids for b in bad)
      and all(b not in ids for b in bad))
print("FINISH LINE:", "PASS" if ok else "FAIL")
raise SystemExit(0 if ok else 1)
