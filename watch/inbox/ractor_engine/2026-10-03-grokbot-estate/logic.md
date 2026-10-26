# logic.md - ractor lens: logic (2026-10-03 grokbot-estate run)

Lens: logic (instrument theorist; jacket: two instruments disagreeing with no
adjudicator). Verdicts: TRUE / FALSE / THEATER / UNVERIFIED.

## Findings

L1. Label vs rate. TRUE contradiction. Janitor goals end "$0."
(mag/ghost.py:1442, 1462) while the provider/model is deepseek /
deepseek-v4-flash, priced at configs/cost_rates.yaml:9-15 (0.22-0.44 USD per
M input miss, 0.66-1.32 per M output). The label is false; it only reads true
today because every run dies before its first token.

L2. Bus event vs fact. TRUE. "autonomous_task_completed" is published at
spawn (mag/ghost.py:1515-1521); orchestrator receipts say failed exit 1 in
about 5 s (e.g. t57a5a3a9e1, duration_s 5.1).

L3. Two boot instruments disagree. TRUE. memory/biography/verkle_tip.json
"Tip is the chain tail" now names autonomous-auto-fkb-632d09 (a failed-task
knot); scripts/verkle_boot_view.py:35-42 filters autonomous- and dwf- as
noise. The read-side view is right; the canonical tip pointer is noise. No
adjudicator decides which one a cold boot reads (boot consumer not read:
OWED).

L4. Plan fix (a) vs site semantics. FALSE. CONVERGENT with accuracy A5:
outcome at mag/ghost.py:1506 is spawned/spawn_failed only (ghost.py:1129).

L5. Chain consistency instruments agree (negative result, banked so nobody
re-spends it). TRUE. stealth driver "CHAIN-REPAIR: nothing to do (chain
consistent (11203 leaves))" (state/fuel/stealth_driver.jsonl, 22:37Z row) and
verify_verkle_full exit 0 at 11,203 rows.

L6 (new). Exit-code semantics are not uniform across the red patrols:
CensusPatrol rc=1 is a designed signal (2026-10-02-dogfood-48h/break-security.md:61),
TipWitness/XRadar rc=2 are cannot-verify class, Spine Index 0xC000013A is a
Ctrl-C termination. "8 failing" counts unlike things. TRUE.

Tally (this lens): TRUE 5, FALSE 1, THEATER 0, UNVERIFIED 0.

No em-dash bytes. Filed by the logic lens.
