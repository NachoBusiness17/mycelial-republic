# B2-58: append LEDGER row (json.dumps) + QUEUE self-feed briefs. No heredoc.
# Pre-write collision check per the B2-53/B2-50 restoration notes: verify the
# target numbers are unclaimed immediately before append.
import json
import re
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

queue_path = "watch/inbox/burn_wave_20260926/QUEUE.md"
with open(queue_path, encoding="utf-8") as f:
    queue_text = f.read()

claimed = set(int(n) for n in re.findall(r"B2-(\d+)", queue_text))

ledger_row = {
    "ts": TS,
    "slug": "B2-58-prompt-amendments-20260926",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_58_prompt_amendments_20260926.md",
    "one_line": "prompt-law v2 amendments landed in roblox/prompts/README.md (74 insertions, 0 deletions, no code): law 1 split judge-side ANCHOR vs candidate-side LOCK with per-template invariant blocks, law 3 judge-must-quote (element+quote+verdict, only-a-number named anti-pattern), law 5 seed-paired uplift (unpaired claims are CLAIMED), law 4 BIB_LAUNDER auto-revert per the TARA gate (adopt iff paired score beats seed else revert); first landing of the pass-d draft which left roblox/prompts untouched; TARA 2607.18724 and VQQA 2603.12310 corroborated live at abstract level, full-text quotes rest on B2-09 same-day reads",
}

with open("memory/burns/LEDGER.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(ledger_row, ensure_ascii=True) + "\n")
print("ledger row appended")

briefs = [
    "- [ ] B2-150 Land the BIB_LAUNDER pre-flight checker: build tools/bib_launder_check.py per the v2 spec and pass-d shape (extract invariant blocks by fixed marker, sha256 against the SEED hash never the previous candidate, no whitespace or unicode normalization, empty diff is the only pass, exit 2 on fail, never a judge instruction); the README law level landed but the mechanical check is still draft-named, so the lock has no teeth until this exists; pointers roblox/prompts/README.md V2 AMENDMENTS section + watch/inbox/burn_wave_20260926/B2_58_prompt_amendments_20260926.md + watch/inbox/BURN_prompt-uplift-lane_20260925_d.md:28-30",
    "- [ ] B2-151 Seed-paired uplift harness with TARA gate: build the paired eval that runs the seed prompt and every candidate on the same fixed seed set and applies adopt-iff-paired-score-beats-seed-else-revert (the v2 amendment D), so amendment D is testable instead of spec-only; falsifier pre-registered in B2-58 receipt F2: if the gate does not beat flag-only adoption on seed-paired regression rate, the auto-revert clause is vacuous; pointers watch/inbox/burn_wave_20260926/B2_58_prompt_amendments_20260926.md Falsifier + roblox/prompts/README.md amendment C/D",
]

# dynamic pick: next free integers after the current max (B2-53 lesson), read
# immediately before append; briefs carry placeholder numbers B2-150/B2-151
targets = []
n = max(claimed)
while len(targets) < len(briefs):
    n += 1
    if n not in claimed:
        targets.append(n)
print("picked numbers:", targets)
briefs = [b.replace("B2-150", f"B2-{targets[0]}").replace("B2-151", f"B2-{targets[1]}")
          for b in briefs]

with open(queue_path, "a", encoding="utf-8") as f:
    f.write("\n".join(briefs) + "\n")
print("queue briefs appended:", len(briefs))
