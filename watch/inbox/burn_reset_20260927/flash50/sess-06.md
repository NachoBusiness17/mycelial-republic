# sess-06: the operator's MINIMUM BRIEFING

Item: sess-06, source state/CURRENT.md (seed-seal stranger slot). Date 2026-09-28.
Ask: the operator said "I don't want to keep the entire estate in my head." Design the
one document, max 500 chars, that tells him everything he needs to know right now.
What goes in it, what stays out.

## 1. The slot, as read

state/CURRENT.md:34-44, "owed (Mag P0-5 stranger / seed verify 2026-09-26)":
EXTERNAL FALSIFIER OPEN. `seed/verify_seal.py` ran on the Mag seat 09-26 with exit 1
(DRIFT TRUST_BYTES_LAW.md, 55/56 verified, 1 drifted, 0 missing). Named stranger slot,
do not silently defer: a human who did not mint the seed (operator hand, Nacho/Mark)
runs `python verify_seal.py` on a clean tree (or Linux `sha256sum -c MANIFEST.sha256`)
plus FIRST_BOOT steps 1-2 and files a receipt under watch/inbox/. Until then the
portable-seed claim stays Unproven. Authority: ELDER_ASK_SEED_AUDIT_20260926.md:22-24
(P0-5 SUPPORT, execute-now, "do not silently defer") and :30 (compounding rank 3: the
self-steal ratchet has no stranger check without it). seed/FIRST_BOOT.md:1-7 defines
the stranger's first hour (read THE_METHOD.md, run the smith chart, and so on).

## 2. Checks I ran this session

1. `./.venv/Scripts/python.exe seed/verify_seal.py; echo "EXIT=$?"` (read-only hash
   check, seed/verify_seal.py:8-17) -> output:
   `DRIFT    engines/key_law.py` / `56/57 verified, 1 drifted, 0 missing` / `EXIT=1`.
   The falsifier is still open today. The drifted file CHANGED between runs
   (TRUST_BYTES_LAW.md on 09-26 per CURRENT.md:35-36; engines/key_law.py today).
   Design consequence: hash-level detail churns; the operator decision does not.
   Exactly the kind of detail that must stay out of his head.
2. Read mag/state_brief.py (260 lines): the estate already computes a deterministic,
   $0 operator greeting (docstring :1-19, "wired into watch/sancho_boot_hook.py
   (SessionStart) + main.py state-brief" :19). `--dry` prints without writing (:243).
   It renders loops-alive plus the wake command on loud absence (:173-180), queue
   totals (:186-190), landed answers (:193-201), health counters (:204-210), and a
   transfer-measure block (:213-217) per seed/STATE_BRIEF_CONTRACT.md:1-18, whose law
   is "Orientation is computed from state, never generated" (:3) and "Loud absence
   beats silence" (:36-37).
3. `wc -l -c memories/session/next-window-handoff.md` -> 466 lines, 36,599 chars.
   That is the "full handoff" CURRENT.md:17-18 points at: 73x the 500-char budget.
   `grep -n -i "stranger\|operator key\|operator-gated\|crons"` over it returns only
   the same two operator-gated items CURRENT.md already carries (LLM7 token unlock
   "operator key call" :85; "scheduling stays OPERATOR-GATED (no crons law)" :87).
   No new operator-only action hides in the long doc.

## 3. The MINIMUM BRIEFING (the deliverable)

Measured 498 chars (python len of the exact line inside the fence, via
_sess06_check.py in this dir; single line). 498 <= 500 cap holds.

```
OP BRIEF 09-28: Quiet. 09-27 window closed clean, nothing burning. ONE action only you can do: name a stranger human (Nacho/Mark) to run seed/verify_seal.py + FIRST_BOOT 1-2 on a clean tree, receipt to watch/inbox/; portable-seed stays Unproven till then. Also yours: LLM7 key call; cron scheduling. Everything else self-computes: read state/CURRENT.md or run .venv\Scripts\python.exe -m mag.state_brief --dry. Depth when needed: MEMORY.md > ATLAS.md > ESTATE_INDEX. Carry pointers, not the estate.
```

## 4. What goes in, and why (5 rows)

1. A status word, "Quiet": loud absence is a section, not an error
   (seed/STATE_BRIEF_CONTRACT.md:36-37; rendered live at mag/state_brief.py:179-180).
   The operator's worst cost is silently wondering whether something is burning.
2. The operator-only decision queue. Only three classes of item cannot be done by a
   seat: naming a stranger human (CURRENT.md:40 "operator hand (Nacho/Mark) - name a
   human who did not mint the seed"), the LLM7 token unlock ("operator key call",
   CURRENT.md:21), and scheduling ("No crons law holds: scheduling is operator-gated",
   CURRENT.md:22). The stranger item is non-deferrable by elder ruling
   (ELDER_ASK_SEED_AUDIT_20260926.md:24).
3. The unproven-claim clause: "portable-seed stays Unproven till then" (CURRENT.md:43).
   An open falsifier must survive compression; its acceptance test is one command a
   stranger can run (verify_seal.py:17 exits 1 on any drift or missing file).
4. The one command that computes everything else: `python -m mag.state_brief --dry`
   (state_brief.py:16,243; deterministic $0 per STATE_BRIEF_CONTRACT.md:3-5,36). Plus
   the pointer to CURRENT.md, the 46-line live truth the briefing distills.
5. The depth ladder as pointers, not contents: memory MEMORY.md -> ESTATE_ATLAS/ATLAS.md
   -> grep ESTATE_INDEX (CURRENT.md:45-46). He carries addresses; the estate carries
   the rooms.

## 5. What stays out, and why (5 rows)

1. Everything the brief computes: loop liveness, queue totals, landed answers, health
   counters (all rendered at $0 by state_brief.py:173-217). Memorizing them pays a
   human to be a deterministic function.
2. History and narrative: the closed 09-27 marathon window, 150/150 game dig,
   PRIVLIDGE pin recipe (CURRENT.md:3-30). Closed work leaves the head; it lives in
   GAMEDIG_MASTER_ATLAS_20260927.md and the pinned memory file (CURRENT.md:26-30).
   Hence the briefing's one word "Quiet" instead of the story.
3. Doctrine and laws: DRIVING LADDER, ratchet, gates, census law. They are held by
   ribs and hooks that fire without him (AGENTS.md Clippy block; rib receipt
   memory/rib/RIB_DRIVING_LADDER_20260928.md; seed/FIRST_BOOT.md:5 "That is what the
   meters are for": enforcement by machine, not recitation).
4. The full owed list beyond operator-gated rows: "owed (top, all ledgered)"
   (CURRENT.md:19-22) are machine-runnable or already queued; the fleet drains them.
5. Hash-level detail like WHICH file drifted. It churned between 09-26 and 09-28
   (check 1 above) while the decision stayed fixed. Volatile detail loses to stable
   decisions under a 500-char budget.

## 6. Patterns extracted (6)

1. Compute-don't-carry: orientation is computed from state, never generated or
   memorized (STATE_BRIEF_CONTRACT.md:3; state_brief.py:97).
2. Operator-gated-only filter: a minimum briefing carries exactly the decisions a
   machine cannot make, and nothing else (CURRENT.md:19-22,38-44).
3. Loud absence: say "quiet" out loud; silence is not a status
   (STATE_BRIEF_CONTRACT.md:36-37).
4. Pointers over contents: depth is an address ladder (CURRENT.md:45-46), and indexes
   regenerate, they are never hand-maintained (seed/FIRST_BOOT.md:12-13).
5. Unproven rides along: compressed state must still carry its open falsifier and its
   acceptance command (CURRENT.md:43; verify_seal.py:17; ELDER:24 no silent defer).
6. Volatility filter: within the operator-only set, prefer stable decisions over
   churning detail (drift file changed 09-26 to 09-28; decision did not).

## 7. Scans and commit

- Em/en dash scan: `./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_sess06_check.py`
  -> `em_dash=0 en_dash=0` on this file.
- Char check: same run -> `brief_chars=498`, `brief_le500=True` (the exact fenced line).
- Banked at watch/inbox/burn_reset_20260927/flash50/sess-06.md, committed with
  sess-06 prefix on the run branch.
