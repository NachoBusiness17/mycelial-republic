# B2-199 2026-09-26: QUEUE.md self-feed with collision-safe dynamic numbering.
# Ledger row for B2-199 already appended exactly once by B2_199_ledger_queue.py
# (verified count==1); this script touches ONLY QUEUE.md.
import re
from pathlib import Path

REPO = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
queue = REPO / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"

briefs = [
    (
        "living-downgrade detector: a plain `add` re-register legally drops the living flag "
        "(last-register-wins, LIVING_HASH_LAW_20260926.md section 5), so one stale whole-file refresh "
        "silently reverts LINKS.jsonl/QUEUE.md/phone_relay_log.jsonl to a shape that hard-fails on the "
        "next append; add a validate warning in mag/shared_surface.py items loop when one of the three "
        "known living paths folds to an item without item.living; pointers mag/shared_surface.py:224-258 "
        "+ watch/inbox/LIVING_HASH_LAW_20260926.md sections 4-5"
    ),
    (
        "drift-patrol prompt persistence: the amended living-law patrol prompt lives only in "
        "%USERPROFILE%/.zcode/v2/tasks-index.sqlite automations row automation-a7c71ad1 (rewritten by "
        "watch/inbox/burn_wave_20260926/B2_199_update_prompt.py), no repo copy, so a harness rebuild or "
        "DB reset silently reverts the patrol to whole-file hash refreshes; land a repo-side copy plus a "
        "check diffing the DB row against it (freshness_check.py pattern); pointers "
        "watch/inbox/burn_wave_20260926/B2_199_patrol_living_20260926.md falsifier section + "
        "tools/freshness_check.py"
    ),
    (
        "fold verify cwd trap: scripts/index_fold_host.mjs verify resolves inbox-relative item paths "
        "against process cwd, so from repo root it reports every file MISSING (observed 09-26: 8+ MISSING "
        "lines from root, 0 from watch/inbox) and would send any runner chasing phantom truncations; "
        "resolve items against INBOX_DIR or die with a cwd hint when INDEX.json is not under cwd; "
        "pointers scripts/index_fold_host.mjs:379-386 + B2_199 receipt verify evidence"
    ),
]

for b in briefs:
    assert chr(0x2014) not in b and chr(0x2013) not in b

text = queue.read_text(encoding="utf-8")
nums = [int(m) for m in re.findall(r"B2-(\d+)", text)]
start = max(nums) + 1
lines = []
for i, b in enumerate(briefs):
    lines.append(f"- [ ] B2-{start + i} {b}")
marker = lines[0][:40]
if marker in text:
    raise SystemExit("collision during write, aborting without writing")
if not text.endswith("\n"):
    text += "\n"
text += "\n".join(lines) + "\n"
queue.write_text(text, encoding="utf-8", newline="\n")

back = queue.read_text(encoding="utf-8")
for i in range(len(briefs)):
    assert f"B2-{start + i} " in back, f"B2-{start + i} missing after write"
print(f"queue self-fed: B2-{start} .. B2-{start + len(briefs) - 1}")
