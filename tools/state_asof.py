"""STATE ASOF — the time-machine query for the estate's record.

Answers "what did the estate know on date D" from the append-only event log:
files registered on/before D, and the day's last events. No reconstruction is
invented — this only reads index_events.jsonl (rib.md.record.v1 records).

Usage: .venv/Scripts/python.exe tools/state_asof.py 2026-09-19 [YYYY-MM-DD ...]
"""

import json
import sys
from collections import OrderedDict
from pathlib import Path

INBOX = Path.cwd() / "watch" / "inbox" / "index_events.jsonl"


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    for day in sys.argv[1:]:
        known = OrderedDict()
        day_events = []
        for line in INBOX.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                e = json.loads(line.strip())
            except Exception:
                continue
            ts = str(e.get("ts", ""))
            if ts[:10] <= day:
                name = str(e.get("file", "")).rsplit("/", 1)[-1]
                if name:
                    known[name] = True
            if ts[:10] == day:
                day_events.append(e)
        print(f"\n== as of {day}: {len(known)} files known ==")
        last = day_events[-5:]
        print(f"   {len(day_events)} events that day; last {len(last)}:")
        for e in last:
            print(f"   {str(e.get('ts',''))[:19]} {e.get('op','?'):9s} "
                  f"{str(e.get('file','')).rsplit('/',1)[-1][:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
