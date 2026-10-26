# SWARM_LENS protocol v0 (baby step, 2026-08-31)

Derived from the J-space synthesis exercise (deep_synth_jspace_20260831.md): we ran a 3-pass
evidence-calibrated synthesis with primary-source arbitration and it caught a fabricated claim
in a strong external draft within one verification pass. This protocol makes that luck into law.

**What it is:** J-lens reads what a model is *poised to report*. SWARM_LENS reads what the swarm
is *poised to report* — and separates it from what the swarm merely produced. Same physics:
reportable subset ≠ automatic output; interventions (arbitration, decode gates) prove causality.

## The 6 gates (one cycle)

1. **LEDGER FIRST.** No synthesis before every load-bearing claim has a ledger row:
   `claim | pointer (path:span) | evidence type (observation/intervention/probe/external/attested) | confidence (H/M/L/Unknown) | arbitration status`.
   No pointer, no row, no claim.
2. **SOURCE HIERARCHY.** Primary bytes > lane report > seat memory. Commentary = context, never
   evidence. A "fact" read from a model's own recall is attested, not verified.
3. **ARBITRATION GATE.** Any external/A-lane claim that will become canonical gets checked against
   primary bytes before adoption. The diff is receipted — what verified, what failed, what was
   imprecise. (Receipt style: /board/deep_synth_jspace_20260831.md §6 arbitration receipt.)
4. **ATTACK PASS.** Every synthesis gets a hostile lane (socratic relay pattern) before it is
   called done. The attack lane verifies baselines with its own tools, then attacks conclusions.
5. **CALIBRATION WORDS.** "shows / supports / is consistent with / does not establish / remains
   unknown" — pick from the list. No "proves". Confidence labels mandatory on tables.
6. **PUBLICATION GATE.** Anything leaving the cage (riddler_common, board posts, packs) passes the
   riddler decode gate. Authority labels on every artifact. A roast can become a proposal; it
   cannot become a permission.

## Dogfood loop (per research cycle)

- Before: seed the ledger from prior cycle rows (WARM_PACK/RIB spans).
- During: lanes append rows, never prose-only reports.
- After: one arbitration pass + one attack pass → synthesis with revision log.
- Drift check: re-verify one random row against its pointer each cycle. Drift is detected, never silent.

**Cost:** zero. **New organs:** zero. This is GOPHER law + riddler gate + socratic relay composed
into one numbered procedure. Baby step v0: run it on the next swarm research task unchanged.
