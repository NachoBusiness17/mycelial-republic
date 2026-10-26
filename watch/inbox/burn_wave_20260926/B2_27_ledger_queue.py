# B2-27: append LEDGER row (json.dumps) + QUEUE self-feed briefs. No heredoc.
import json
import re
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ledger_row = {
    "ts": TS,
    "slug": "B2-27-scout-checkgate-20260926",
    "verdict": "landed: python -m mag.link_library check wired into the free-resource-scout filing path at spec (module docstring law citing B2-06), code (check_url() gate, CLI check delegates, add stamps duplicate_of at submission), and firing config (MANIFEST free-resource-landscape pointer); 4 new tests pin the B2-06 dupe shape, suite 30 passed; live checks on thundercompute + arxiv 19107 dupe URLs both exit 1",
    "landing": "watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md",
    "one_line": "The scout (an agent writer with no script, proven by repo + schtasks census) lost its bypass: all 21 scout link rows carried empty duplicate_of before this gate, the exact mechanism behind B2-06's 5 silent dupes",
}

with open("memory/burns/LEDGER.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(ledger_row, ensure_ascii=True) + "\n")
print("ledger row appended")

briefs = [
    "- [ ] B2-119 known_canonicals is last-writer-wins: the dict comprehension overwrites per canonical, so check_url first_entry and add_urls duplicate_of point at the NEWEST row, not the first filing (live proof 2026-09-26: check on thundercompute returns the dupe-triage row seq 1790422309734386, not the 09-16 original seq 1789484000012); make the gate return the earliest filing, with a test; pointers mag/link_library.py known_canonicals + watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md",
    "- [ ] B2-120 Scout charter: the free-resource scout is a LEAD watcher (DIRECTIVE_WATCHERS_20260926.md:14, 8 runs) with no written spec on disk (no module, no schtasks entry, no brief file); write the one-page charter naming its writers (free-resource-scout link vs event rows), the filing doors (python -m mag.link_library add for links, EVENTS.jsonl event.v1 for findings per B2-28), and the dedupe law, so the next patrol audits against a spec instead of observed work; pointers watch/inbox/burn_wave_20260926/B2_27_scout_checkgate_20260926.md evidence section",
    "- [ ] B2-121 paste_pipeline door consolidation: mag/paste_pipeline.py:149 re-implements the known-canonicals lookup inline instead of calling the new check_url() single door (annotate-never-gate behavior must be preserved byte-for-byte); refactor + test, per the B2-27 gate law; pointers mag/paste_pipeline.py:126-149 + mag/link_library.py check_url",
]

with open("watch/inbox/burn_wave_20260926/QUEUE.md", "a", encoding="utf-8") as f:
    f.write("\n".join(briefs) + "\n")
print("queue briefs appended:", len(briefs))
