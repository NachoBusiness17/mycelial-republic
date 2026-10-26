# GO WAVE 20261004 fold: all 10 fold-GO items executed

Coordinator: zcode-seat. Shape: 12 Task-agent lane runs (9 first drop at width
9, 2 staggered refires after a simultaneous 1302 burst, 1 held second-drop lane),
disjoint file ownership, no lane commits, coordinator batch commit. Combined
gate: 160 passed / 0 failed in ~18s (instrument: pytest -q -p no:cacheprovider
over the 15 wave test files + tools/gps_mcp testpath). Ratchet: PASS, 2 size
debts accepted by name (go-wave-20261004-coordinator): file-too-long
tools/dungeon.py:756 and gps_mcp/ledger.py growth 728 -> 840. One NEW smell
fixed in-wave instead of registered: the silent except-pass at
mag/route_chat.py:174 now writes the reason to stderr.

## Scoreboard (per lane receipts in this dir)

1. route_chat.md - GO 1: docstring scoped, disable_thinking wired, reasoning
   fallback fixed, depth enum validated, 11 tests, exception-path bank row,
   fence TOCTOU closed (pinned DNS), first non-smoke production ask banked
   ($0.00007, deepseek lane; local ollama refused by the https-only fence by
   design - loopback http, noted for the operator).
2. gps_dedupe.md - GO 2: partial unique index + INSERT-that-skips + race
   backstop, .bak migration (494 rows, zero moved), 99 fed / 252 duplicate-
   skipped / 351 distinct, idempotence proven 593 -> 593, 82 tests. Upstream
   arena_gwap defects filed (live-dirs-only walk orphans quarantined scenes).
3. ds_workhorse.md - GO 3+9: register repaired (caveats, tallies, ds_capped,
   measured costs; $0.14 figure matches no ledger), rails 39/39, gaming_corpus
   re-judged 9-5, max_tokens override + content slice deleted, 29 hollow rows
   void-stamped, ok_api/ok_material split, render guard + 4 tests. ds arm
   re-fired uncapped: 3/28 vs the capped 0/26 - the routing table correction
   of the day; frontier 12-2, flash 13-1. Spend $0.2016.
4. dungeon.md - GO 4: parser fixed (last-tag-wins, dice brackets filtered),
   14/14 S4 verdicts replayed (12/14 were collapse artifacts, 2 coincide),
   Phantom Regrowth enforced, case-folded lookup, verdict-gated wipe,
   finish_reason banked, erratum filed (40/50 DM readbacks voided), 15 tests.
5. index_seal.md - GO 5: INDEX refolded 842 stale events (9,237 -> 10,084),
   4 seals landed, all 11 receipt names confirmed by grep.
6. arena_cadence.md - GO 6: fire-atomic bank in both carriers, parable erratum
   ($25 cap vs $25.11 meter crossing, $0.62 over-cap close, 1 failed 13:00Z
   fire), banked_at column, UNPROVEN backfill attribution. Live dogfood fire
   banked same-second, $0.0312, 45 tests.
7. queue_truth.md - GO 7: Q-005/Q-025 closed, todo paths fixed, todo:31
   parked, NIGHT_CLOSE move 2 struck, A16 addendum (real path was in
   model_garden/archeology_w2), GAP_REGISTER ranks 2/3/4/6/7 annotated FILLED.
   Finding filed: 8 sibling WO-12 todo lines still cite dead queue/Q-0xx paths.
8. fifty_wide_guard.md - GO 8 (D1): NO RUNNER EXISTED - the 50-wide waves were
   ad hoc Task fan-outs. Countermeasure is tools/fifty_wide_guard.py (303
   lines, 10 tests): fail-loud unit/lane equality, dropped-unit list into the
   receipt, replayable dispatch log. Live demo: exits 1 naming exactly the 10
   dropped units on the real 60-unit artifact. Per-agent archive retention is
   operator-owed. D1's original mechanism stays unknown; em-dash refuted.
9. tavern_refresh.md - GO 10: calibration cells cite RUN DONE greps, brawl
   table filed (TAVERN_CURVE_AUDIT_20261003.md), p0 labeled run + p2 n=2
   landed ($1.31 spend), falsifier FIRED and now first-class (3/14 at fold
   moment, 5/23 at census - p1 is a distribution). Carrier bug found:
   same-second stamp collisions corrupt concurrent fires (quarantined + filed).
10. prepush_instruments.md - alternates: golden-vector (11/11), credential-
    shape (WARN-ONLY, zero-baseline), seal patrol (bounded window). 19 tests.
    SEE THE INCIDENT BELOW.

## INCIDENT: live OpenRouter key caught PRE-COMMIT (KEY_SCRUB_20261004.md)

The credential-shape instrument's first live run flagged the live .env
OpenRouter key inside the elder lane trail + surface and both dashboard
renders - a CYCLE_FAIL detail had echoed the raw Bearer header. Byte-exact
.env match confirmed. Never committed (entered the tree after a7ca49be1,
caught before the next one). Scrubbed in 4 files, source-fixed at the
lane_runner _trail chokepoint, 4 regression tests. No rotation required on
current evidence; operator hygiene: skim OpenRouter usage for
10-03T20:00Z - 10-04T09:20Z.

## Spend

Metered: $0.2016 (ds re-fire) + $0.00007 (production ask) + $0.0312 (arena
dogfood) + $1.963 (tavern fires) + ~$0.13 (gps/route misc per receipts) =
under $2.40 total. Agent tokens: ~35M across 12 runs on the individual plan.

## Held for operator

- D3: route_chat arm 2 thinking-on disagreement (two law surfaces) - needs
  your signature before the PRIORS scoping amendment lands.
- D4: deepseek v4 thinking-omission default (two in-repo sources contradict).
- 8 sibling WO-12 todo lines cite dead queue/Q-0xx paths (lane 7 finding,
  outside its named scope).
- Per-agent output archive retention for 50-wide waves (operator behavior).
- dungeon.py engine split (756 lines) or the debt stands accepted.
