"""B2-42 ledger row + QUEUE self-feed (2026-09-26 flash-lane burn).

Pattern per B2_27/B2_37/B2_52: run with .venv/Scripts/python.exe, json.dumps
only (never heredoc), collision-check QUEUE numbers immediately before write
(B2-53 lesson), refuse em-dashes (law).
"""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

# script sits at watch/inbox/burn_wave_20260926/: three levels below repo root
ROOT = Path(__file__).resolve().parents[3]
LEDGER = ROOT / "memory" / "burns" / "LEDGER.jsonl"
QUEUE = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"

row = {
    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "slug": "B2-42-events-hygiene",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_42_events_hygiene_20260926.md",
    "one_line": (
        "events-log hygiene closed: lines 94-96 of index_events.jsonl confirmed the only "
        "malformed lines in the log (python dict-repr register with PENDING_CODEX sha + two "
        "amends with unquoted seq NEXT, all CRLF-terminated); no-erase law kept them verbatim, "
        "note event seq 1789823567015749478 (writer zcode-b2-42-events-hygiene) documents all "
        "three (the 09-01 note at line 98 covered line 94 only); debt grandfathered by content "
        "sha256 in configs/events_malformed_baseline.json; mag.shared_surface validate now "
        "errors on NEW malformed lines (strict json.loads, NaN rejected to match the fold's "
        "JSON.parse, CRLF/blank handled like the fold), 8 new tests in "
        "tests/test_shared_surface_events.py, fold still skips exactly 94,95,96, validate "
        "error delta on the real surface is only concurrent QUEUE.md hash drift; known "
        "deviation filed as B2-156: the note seq is a past-2^53 NUMBER literal where the "
        "B2-40 scheme prescribes a decimal string (even value, exactly representable, "
        "ordering exact)"
    ),
}

briefs = [
    (
        "Normalize past-2^53 seq emission forms: the B2-42 note event appended a NUMBER "
        "literal seq 1789823567015749478 (last line of index_events.jsonl) where the B2-40 "
        "scheme prescribes decimal STRING past 2^53 (scripts/index_fold_host.mjs:105-138); "
        "audit the log for other number-literal seqs past 2^53, decide codify-or-warn in "
        "seqOf/nextSeq (even values are exactly representable, odd ones quantize), falsifier: "
        "a number-literal seq that sorts after a later decimal-string seq."
    ),
    (
        "QUEUE registered-hash drift flap: mag.shared_surface validate reports 'hash mismatch: "
        "burn_wave_20260926/QUEUE.md' whenever any lane appends self-feeds between register "
        "and append (visible in watch/inbox/burn_wave_20260926/B2_42_validate_after.json); "
        "either make QUEUE.md self-feed appends refresh its INDEX registration hash in the "
        "same critical section, or teach validate to exempt registered-then-appended queue "
        "files for N minutes, falsifier: a drift-free burn wave with zero QUEUE.md mismatch "
        "errors at close."
    ),
]

# never em-dashes (law)
for text in [row["one_line"], row["verdict"]] + [b for b in briefs]:
    assert "\u2014" not in text and " -- " not in text, f"em-dash law: {text[:60]}"

with LEDGER.open("a", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(row, ensure_ascii=True) + "\n")
print("ledger row appended:", row["slug"], row["ts"])

# collision-checked self-feed: highest existing B2-N wins, re-read at write time
qtext = QUEUE.read_text(encoding="utf-8")
claimed = {int(m) for m in re.findall(r"B2-(\d+)", qtext)}
n = max(claimed) + 1
mine = [n, n + 1]
overlap = [x for x in mine if x in claimed]
assert not overlap, f"collision: {overlap} already claimed"
add = "".join(f"- [ ] B2-{x} {briefs[i]}\n" for i, x in enumerate(mine))
marker = "## Open"
idx = qtext.index(marker)
end = qtext.index("\n## ", idx + 1) if "\n## " in qtext[idx + 1:] else len(qtext)
qtext = qtext[:end] + add + qtext[end:]
QUEUE.write_text(qtext, encoding="utf-8", newline="\n")
print(f"QUEUE.md: appended B2-{mine[0]} and B2-{mine[1]} under Open (highest was {max(claimed)})")
