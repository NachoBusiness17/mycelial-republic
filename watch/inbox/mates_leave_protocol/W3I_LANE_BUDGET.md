# W3I - LANE BUDGET (mechanism 1: pre-bound metered budgets that HALT a lane)

Filed: 2026-09-29 (UTC 2026-09-30T02:2x) · zcode-seat W3 lane · files: `tools/lane_budget.py` (new, 329 lines) + `tests/test_lane_budget.py` (new, 193 lines) · NOT committed (lane rule).

## What landed

The S22 orb-spec's missing mechanism (a): "pre-bound metered budgets that HALT a running lane (we only have post-hoc billing receipts)" — wave ledger `watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md` S22. `mag/lane_effort.py` stays the pure tier-decision half; this is the runtime half.

- `Budget(name, max_actions, max_seconds, max_usd_estimate)` — caps bound at construction; the lane cannot re-raise its own ceiling (resume reloads caps from the checkpoint; overrides are supervisor actions).
- `.spend(n=1, seconds=, usd=)` — applies the spend, then checks dimensions in order actions -> seconds -> usd_estimate; the spend that pushes strictly past a cap is fatal; reaching a cap exactly is legal. BEFORE raising `BudgetExhausted` it appends `{lane, reason, spent, ts}` to `logs/lane_budget/deaths.jsonl`. One receipt per death (transition-only; re-spends re-raise without a second epitaph).
- Auto-stop on time: wall-clock elapsed since budget start counts toward `max_seconds` with zero caller action (S22 "auto-stop"); the `seconds=` arg meters work time NOT on the lane's own wall clock (child-lane reported time).
- Context manager: `with Budget(...) as b:` — exit always writes a checkpoint (`logs/lane_budget/checkpoints/<name>.json`, schema `lane_budget.v1`) banking spent/caps/dead; `Budget.resume(path)` rebuilds with the REMAINING budget (spent carries verbatim; dead state cannot be laundered into a live one).
- No budget = UNMETERED, explicit: a singleton with the same surface that never halts and never writes; the opt-out is a greppable token in code, never a missing-argument accident. A Budget with all-None caps is the distinct "meter that never halts" (still counts via `spent()`).

## Tests (real counts, instrument + moment named)

`pytest -q tests/test_lane_budget.py` at 2026-09-29 ~22:20 local: **12 passed in 0.63s** (12 collected, `--collect-only -q` same moment). Coverage: exhaustion raises + receipt written before the raise (actions/seconds/usd dims + wall-clock monkeypatched); one-epitaph; resume inherits remaining (2-of-3 spent -> third legal, fourth trips the same cap); dead-resume refuses; foreign-schema checkpoint rejected; UNMETERED never halts + writes nothing; all-None caps never halt. Full 2,303+ suite NOT run by this lane: zero existing files edited (both files new, `git status` untracked-only), so blast radius is nil; counts above are the file-scoped instrument, not a suite claim (denominator law B2-216).

## Gates

- Ratchet `check --changed`: FAIL is the dirty tree's pre-existing debt (`mag/physical_compute_acquire.py` NEW file-too-long + 2 GROWTH rows) — other lanes' uncommitted work, zero hits from lane_budget files (329/193 lines, under the 400 cap). Not committed, not baseline-touched by this lane.
- Module smoke (`python tools/lane_budget.py`) verified live: halt, receipt row, resume-remaining all printed.

HANDOFF: mechanism 2 (fail-closed worktree isolation) remains owed to the W3 builder lane; a natural next mount is wrapping the duel-harness driver's per-ask loop in `Budget` so S5-style lanes get auto-stop priced in effort tiers.
