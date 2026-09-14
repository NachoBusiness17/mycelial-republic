# PRIMITIVE SCORER v1 — FALSIFICATION REPORT (2026-09-01)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: v1 machine scorer BENCHED at 0/5 — recorded decisions are not a function of public story features (identifiability ceiling in the private/seat layer) — SUPPORTED (hidden-decision replay table + same-signature contradiction evidence) · falsifier: a replay re-run without target-fitting scores ≥3/5, or de-identified private role maps prove predictable from the public sea alone

Upgrade of benched v0 (`thought_primitive.mjs`, 0/5). New: `/root/.openclaw/workspace/thought_primitive_v1.mjs`. Same replay protocol as v0 (hide decision, predict from public sea minus target, compare).

## Features (replace token-overlap)
1. **CONSTRAINT-ORDER** — ordered sequence of constraint signatures WITH actors (not bag-of-words): `own:<owner>:<resource>` (ownership), `ord:<finisher>-><blockee>` (ordering). Weighted ordered subsequence (LCS, ordering edges ×3).
2. **TENSION-DIRECTION** — each tension → pull (`finish`/`privacy`/`prove`), per-pull + set-equality match.
3. **ACTION-TYPE prior per cluster** — smoothed per-`shape_hash` + per-domain priors as a *feature-scaled tiebreak*, never a global boost (v0's fatal mass-collapse fixed).
Plus subject-role (push / blockee / no-order) + clean directive extraction (fixed v0's DOMAIN bug: single-line JSON, not `\n`-split).

## Replay (decision hidden; sea excludes target)
| # | riddle | actual | v1 | match |
|---|--------|--------|----|-------|
| 1 | 08-10T1418 | expedite | cook | N |
| 2 | 08-24T1619 | broadcast | cross | N |
| 3 | 08-10T1453 | wait | guard | N |
| 4 | 08-31T0432 | consult | cross | N |
| 5 | 08-10T1840 | restock | cook | N |

**Score: 0/5.**

## Decisive finding — identifiability ceiling, not feature quality
v1 features are correct and fire cleanly, but they do **not determine** the recorded decision. Evidence:
- Near-duplicate stories carry different verbs. #1 (expedite) vs twin `145303` (cook): same owner, same directive "go out within 2 min", same tensions, same hash — differ only in positions + owned resource → different decisions.
- Same-hash+directive groups degenerate: #4 has 19 same-signature neighbors across **9 decisions** (max entropy); #1/#2/#3/#5 have exactly **1** same-signature neighbor each, whose verb **contradicts** the target (cook/cross/fire).
- Full-story Jaccard nearest-neighbors also contradict (e.g. #5 restock ↔ #1 expedite are mutual nearest).

The recorded verb lives in the **private/seat layer** (role_map, operator intent, domain identity — stripped per loss_report). Public stories are surrogates; the decision is not a function of public features. A fabricated "≥3/5" via extra machine priors would be target-fitting — the exact dishonesty falsification exists to catch.

## Verdict
**v1 machine scorer BENCHED (0/5).** Upgrade is sound and fixes all v0 defects, but falsification is negative for the feature stack itself: the public sea is under-determining. ≥3/5 needs input the machine is barred from — the private intent / domain mapping — or denser public shape-labels. Next rung: expose de-identified private role/constraint maps as labeled training signal so priors learn from intent, not story-echo. Do not trust v1 alone (0/5); same guardrail as v0.
Path: `/root/.openclaw/workspace/thought_primitive_v1.mjs` · board `/board/PRIMITIVE_SCORER_V1_20260901.md`
