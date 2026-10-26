# B2-199 2026-09-26: ledger row + QUEUE.md self-feed (json.dumps, never heredoc).
import json
from pathlib import Path

REPO = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")

row = {
    "ts": "2026-09-26T14:58:00Z",
    "slug": "B2-199-patrol-living",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_199_patrol_living_20260926.md",
    "one_line": (
        "drift-patrol-cron living-law adoption: the patrol is ZCode automation "
        "automation-a7c71ad1-f43f-403d-8677-105f5176df2b in %USERPROFILE%/.zcode/v2/tasks-index.sqlite "
        "(cron 0 8 * * *, enabled; no on-disk source, answers B2-211's location question); its prompt "
        "drove the daily whole-file LINKS.jsonl hash refreshes (last 2026-09-26T12:03:24Z, index_events.jsonl:3054, "
        "predating the 13:30:57.884Z B2-156 migration register at :3091); prompt amended per LIVING_HASH_LAW_20260926.md "
        "section 6: fold-host verify living-ok/living-open count as PASS and are never a re-register reason, whole-file "
        "refreshes of living rows FORBIDDEN, LIVING PREFIX MISMATCH/TRUNCATED report-and-owe (tampering, not growth), "
        "living re-seals via add --living (LINKS.jsonl/phone_relay_log/EVENTS) or --living-open (QUEUE.md), patrol "
        "receipt now registers through the fold host (retires hand-minted seq=epoch-ms composed-path events); DB "
        "readback verified with all clauses, zero em-dash; tests 18/18 green (7 living); receipt registered seq "
        "1789823567015749412; exposure filed as B2-215 (prompt lives only in sqlite)"
    ),
}
assert chr(0x2014) not in json.dumps(row) and chr(0x2013) not in json.dumps(row)

ledger = REPO / "memory" / "burns" / "LEDGER.jsonl"
with ledger.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row) + "\n")
print("ledger appended")

briefs = [
    (
        "B2-214 living-downgrade detector: a plain `add` re-register legally drops the living flag "
        "(last-register-wins, LIVING_HASH_LAW_20260926.md section 5), so one stale whole-file refresh "
        "silently reverts LINKS.jsonl/QUEUE.md/phone_relay_log.jsonl to a shape that fails on the next "
        "append; add a validate warning in mag/shared_surface.py items loop when one of the three known "
        "living paths folds to an item without item.living; pointers mag/shared_surface.py:224-258 + "
        "watch/inbox/LIVING_HASH_LAW_20260926.md sections 4-5"
    ),
    (
        "B2-215 drift-patrol prompt persistence: the amended living-law patrol prompt lives only in "
        "%USERPROFILE%/.zcode/v2/tasks-index.sqlite automations row automation-a7c71ad1 (updated by "
        "watch/inbox/burn_wave_20260926/B2_199_update_prompt.py) with no repo copy, so a harness rebuild "
        "or DB reset silently reverts to whole-file hash refreshes; land a repo-side copy plus a check "
        "that diffs the DB row against it (freshness_check.py pattern); pointers "
        "watch/inbox/burn_wave_20260926/B2_199_patrol_living_20260926.md + tools/freshness_check.py"
    ),
    (
        "B2-216 fold verify cwd trap: scripts/index_fold_host.mjs verify resolves inbox-relative item "
        "paths against process cwd, so running it from repo root reports every file MISSING (observed "
        "09-26: 8+ MISSING lines from root, 0 from watch/inbox) and would send the patrol chasing phantom "
        "truncations; resolve items against INBOX_DIR or die with a cwd hint when INDEX.json is not under "
        "cwd; pointers scripts/index_fold_host.mjs:379-386 + the B2_199 receipt verify evidence"
    ),
]

queue = REPO / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
text = queue.read_text(encoding="utf-8")
for n in ("B2-214", "B2-215", "B2-216"):
    assert n not in text, f"{n} already queued"
for b in briefs:
    assert chr(0x2014) not in b and chr(0x2013) not in b
open_idx = text.index("## Open")
open_section = text[open_idx:]
assert "B2-213" in open_section, "expected B2-213 as current highest open brief"
# ascending order: B2-213 is the last open line, so new briefs append at file end
if not text.endswith("\n"):
    text += "\n"
text += "".join("- [ ] " + b + "\n" for b in briefs)
queue.write_text(text, encoding="utf-8")
print("queue self-fed:", len(briefs), "briefs (B2-214, B2-215, B2-216)")
