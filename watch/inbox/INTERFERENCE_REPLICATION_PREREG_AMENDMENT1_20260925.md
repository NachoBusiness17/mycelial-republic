# PREREG AMENDMENT 1 — Arm C budget calibration (filed before Arm C runs)

Frozen original: watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md.
This amendment is filed AFTER Arm B (their system, our hardware) but BEFORE Arm A
and Arm C produce any row. Reason: Arm B measured the budget-response curve and
exposed a calibration error in the frozen Arm C bar.

## What Arm B measured (our hardware, torch 2.13 CPU, exact seed-11 problems)

At budget 50: one-line trained judge 27% (8.1/30), frontier-no-merge 13%,
interference 23% (6.9/30). At budget 200: one-line 70% (21/30, matches their
published 21/30 exactly), frontier-no-merge 100%, interference 100% (30/30,
matches published exactly). ARM B VERDICT: PASS at the frozen >=27/30 bar.

## The error

The frozen Arm C bar demanded >=15/30 (50%) at a 50-state budget. But the
TRAINED judge itself only solves 23% at 50 states. The bar compared gemma-as-
judge against a reference no judge meets at that budget. Comparing at 50 would
measure the budget, not the judge.

## The amendment

1. Arm C runs at BOTH budgets: 50 (frozen bar kept, now expected to FAIL; a
   fail there is the finding "no judge, dumb or trained, solves Countdown-30
   at 50 states") and 200 (added secondary reading, frozen bar >=15/30;
   informative reference at 200 is the trained judge's own 21/30 linear and
   30/30 interference).
2. Parse-fail policy (was unspecified): an unparsed gemma line scores 0.5
   (neutral, never prunes on missing signal) and is COUNTED; parse-fail rate
   is reported in the close receipt.
3. Everything else in the original prereg stands unchanged: one seed, honest n,
   no rerolls, no post-hoc reinterpretation of the 200-state reading.

Filed 2026-09-25, before Arm A/C launch.
