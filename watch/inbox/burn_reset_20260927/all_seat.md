# Burn lane all_seat: test_class_selection_reads_prior_selections

Date: 2026-09-27 · Lane: BURN_RESET_20260927_EVENING lane 1/10

## Root cause (bytes, not reports)

The test imported `mag.quest_party`, which does not exist. Byte trail:

1. Test landed 2026-08-19 (commit 799ddb6fe) in the same commit that last touched
   the then-alive `mag/quest_party.py` (+18 lines, the party_subchain hook the
   test asserts on). The test passed at landing.
2. 2026-09-08: kill list executed with operator GO ("keep it going"). Row in
   `attic/kill_list_20260908/MANIFEST.md`: `mag/quest_party.py | 17199 |
   90a30bd25be4d72b | unreferenced>3wk (path+string scan), parse-clean`. The
   attic copy verifies byte-identical today (17199 bytes, sha256 head
   90a30bd25be4d72b).
3. The kill scan's "unreferenced" claim was scoped to fleet text and missed the
   test reference, but the reference is the ONLY reference: repo-wide grep finds
   `quest_party` in the attic copy and this test file, nowhere else. No runtime
   consumer, and no live module absorbed `self_select` (grep across mag/ for
   self_select / CLASS: prompt surface: nothing).
4. No precedent of other killed-module tests surviving: grep for hero_journey,
   table_turn, mirror_persona, sol_seat in tests/ returns nothing. This file was
   the single orphan.
5. Registered as known: `watch/inbox/SUITE_BURNDOWN_20260927.md` remaining-13
   list, "all_seat_interaction (class selection reads priors)".

## Verdict and fix

Stale contract on the test side. The surface it guarded was deliberately
retired by an operator-approved kill; restoring the module would resurrect 17KB
of dormant product code whose only consumer would be its own test. The file's
charter ("every party surface exposes earlier same-run moves to later seats")
stays fully covered by the two live surfaces (quest_roshomon, frontier_game).

Fix: retired the test function in
`tests/test_all_seat_interaction.py`, replaced with a dated comment naming the
kill receipt path, byte count, sha16, and kill date. No live assertion was
weakened.

## Test numbers (real run)

Command: `.venv/Scripts/python.exe -m pytest tests/test_all_seat_interaction.py tests/test_party_subchain.py tests/test_roshomon_mine.py tests/test_frontier_advisor.py tests/test_frontier_council.py tests/test_frontier_salon.py -q`

Before (fixed file alone, -x): 1 failed (ImportError: cannot import name
'quest_party'), 1 passed.
After: 28 passed in 10.80s (fixed file 2 passed + party_subchain, roshomon_mine,
frontier_advisor, frontier_council, frontier_salon neighbors 26 passed).
