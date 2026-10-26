# FW-20 — Fold self-heal verify: surface delta vs the 12:07 patrol state

- **class:** RECEIPT · **writer:** queue-gopher2-q023 · **board:** memory/plans/fifty_wide_20260917.md §D · **date:** 2026-09-28

## What ran

1. `node scripts/index_fold_host.mjs rebuild` (cwd = repo root) → exit 2 on the designed warn channel:
   `rebuild: folded 4671 events -> 1409 active items`; INDEX.json re-derived at 2026-09-28T18:13:14.679Z.
   Events file: 4,674 lines; 3 malformed skipped (lines 94,95,96 — the grandfathered PENDING_CODEX junk).
2. `node scripts/index_fold_host.mjs verify` (pre-burn) → first run's tail showed 3 `HASH MISMATCH` failure lines and 0 MISSING/TRUNCATED/PREFIX lines (pattern grep count = 3); its full summary line was not captured before the heal — the post-burn verify below is the complete recorded run. Item-count race line: `verify: INDEX.json item count (1409) != folded count (1410)` (a live writer appended between rebuild and verify).
3. `node scripts/index_fold_host.mjs verify` (post-burn, the recorded full run) →
   `verify: 1389 hash-clean, 5 living-ok, 18 living-open, 0 mismatched, 0 missing, 0 living-unverified (of 1412 active items)`; item-count race line now 1410 vs 1412 (live writers still appending — daytime autoseal traffic).
   Note: the `verify` CLI branch sets no exit code (scripts/index_fold_host.mjs:774-775) — the summary line is the signal, exit is always 0.

## Delta vs the 12:07 patrol state (the ask's named comparison)

The comparison target in the board is the 2026-09-17 patrol fold state, recorded in watch/inbox/DRIFT_PATROL_20260917.md: **174→176 events → 159 active items** (the patrol's two hash-refresh registers took 174 to 176; "12:07" is the ask's name for that patrol-moment state — the receipt itself carries no clock time, so the delta is taken against its recorded counts).

| measure | 09-17 patrol state | this fold (09-28T18:13Z) | delta |
|---|---|---|---|
| events folded | 176 | 4,671 | +4,495 |
| active items | 159 | 1,409 | +1,250 |
| fold_errors | n/a (fold was one-way then) | 0 | — |
| surface validate errors | 107 (the +34 day) | 5 pre-burn → 1 post-burn | −106 |

Same-day intra-delta: the morning patrol fold (INDEX derived_at 2026-09-28T12:10:55Z) read 4,513 events → 1,363 items; my refold 158 events / 46 items later — live daytime writer traffic (autoseal registers, BURN drops), not a regression.

## Fold warnings this fold (all legacy, all counted channels)

- 130 writer nonce GAP warnings (pre-2026-09-26 writers minted non-contiguous nonces; replay-protection channel, informational).
- 7 outside-dropped register rows: watch/ x349 (328 distinct), tools/ x5, corpus/, dashboard/, memory/, scripts/, tests/ x1 each — the B2-40/B2-147 poison census, dropped not folded, zero impact on items.
- 1 inexact-seq warning: 561 past-2^53 number literals demoted below exact seqs (the B2-279 total-order law; 09-28 patrol recorded the same 561).

## Post-refold integrity

After burning the 4 live-writer race drifts (see FW19_patrol_debt_1_10.md), the fold holds at the recorded post-burn verify: 1,389 hash-clean, 5 sealed-living-ok, 18 living-open, 0 mismatched, 0 missing, 0 living-unverified. The self-heal loop the 09-17 patrol armed ("NOW SELF-HEALING") is confirmed alive at refold + verify + heal cadence.
