# patrol-fix: census patrol parser repair + carrier refresh (2026-09-29)

Lane: gala wave5-repair patrol-fix, division B. Owed work from
`watch/inbox/burn_reset_20260927/flash50/arch-04.md` (D1 + D2, both
spec'd there 2026-09-28) plus the live COLLECT-DRIFT the daily log
named: `logs/census_patrol.log` 2026-09-28 17:20:35, pytest 2410 vs
carrier 2303 (delta +107, bar 20), files 368 vs 352, instrument gap
tests/test_selffeed_integration.py. This lane owns
tools/census_drift_patrol.py, the patrol tests, and the AGENTS.md
Tests bullet, and is the only lane editing AGENTS.md this wave.

## 1. What was read

- `watch/inbox/burn_reset_20260927/flash50/arch-04.md` in full: D1
  (blank line before the bullet blinds parse_carrier via
  `^\s*` matching newlines in CARRIER_LINE_RE, exit 2 with the lying
  "need the claim shape" message) and D2 (FUTURE_TOLERANCE_DAYS dead
  code: the run() gate tolerated today+1 while patrol() exit-2s any
  negative age), plus the v2 vector prescription (one frozen vector
  per surface, canonical-after-blank must parse, malformed-after-blank
  must stay None).
- `tools/census_drift_patrol.py` in full (403 lines pre-edit).
- `tools/census_patrol_selftest.py` in full (196 lines pre-edit).
- `tests/test_census_drift_patrol.py` in full (567 lines pre-edit).
- `tools/census_collect.py` in full (the B2-365 deep-check split; the
  instrument this refresh's numbers come from).
- `logs/census_patrol.log` tail (the 09-28 17:20:35 COLLECT-DRIFT run,
  quoted by the patrol's own re-run below).
- `configs/violation_baseline.json`: claim 8d41e611f98d3fa5 registers
  tools/census_drift_patrol.py file-too-long at accepted_lines 403,
  so the edits were held to exactly 403 lines (no growth, no prune of
  a shared baseline file this lane does not own).
- `tools/freshness_gate.py:58,151,154`: its own FUTURE_TOLERANCE_DAYS
  is LIVE (honored at `age_days < -FUTURE_TOLERANCE_DAYS`); the
  patrol's copy was the dead one and freshness_gate.py is untouched.

## 2. What changed

### D1: CARRIER_LINE_RE tightened (tools/census_drift_patrol.py)

- Old: `re.compile(r"^\s*[-*]\s*\*\*Tests:\*\*", re.MULTILINE)` -
  `\s*` matches newlines, so with a blank line before the bullet the
  match started on the blank line, `text.find("\n", match.start())`
  found that same newline at offset 0, the extracted line was empty,
  and CENSUS_CLAIM_RE.search("") returned None: exit 2 claiming the
  shape was wrong when only the layout was.
- New: `re.compile(r"^[ \t]*[-*][ \t]*\*\*Tests:\*\*", re.MULTILINE)`
  (horizontal whitespace only), with the cause and receipt in the
  comment on the same lines. CENSUS_CLAIM_RE is untouched: the claim
  grammar and its B2-274 ownership block are unchanged; this is the
  line-locating regex only.
- Vectors (B2-274 surfaces, both): tools/census_patrol_selftest.py
  gains "blank line before a canonical claim still parses" and
  "blank line before a malformed claim stays fail-closed None";
  tests/test_census_drift_patrol.py gains
  test_blank_line_before_canonical_claim_still_parses (asserts the
  full parse dict incl. the extracted line) and
  test_blank_line_before_malformed_claim_stays_none.

### D2: FUTURE_TOLERANCE_DAYS removed (tools/census_drift_patrol.py)

- The constant and its comment (old lines 79-80) are gone; the run()
  future gate is now strictly `parsed["date"] > today`; patrol()'s
  negative-age branch stays the sole future guard. Byte behavior at
  the exit level is unchanged (any future census was already exit 2
  through patrol(); arch-04 probe 4 proved today+1 exit 2 before the
  change). The 2-line replacement comment names arch-04 and this
  receipt and notes freshness_gate.py's live namesake.
- The `timedelta` import was dropped (its only use was the dead
  tolerance term). Tests pin the removal:
  test_census_dated_tomorrow_is_unverifiable_exit_2 (pure core,
  the exact boundary the constant pretended to tolerate) and
  test_cli_census_dated_tomorrow_exits_2 (real CLI subprocess,
  carrier dated tomorrow must stay exit 2).

### Carrier refresh (AGENTS.md Tests bullet, line 27)

- Old claim: "2,303 tests collected / 352 files (2026-09-27 census".
- New claim: "2,436 tests collected / 371 files (2026-09-29 census" -
  exact live grammar, same parenthesized clause shape (B2-249), read
  from the same instrument that judges it
  (`tools/census_drift_patrol.py --collect`, pre-refresh run:
  collect-only tail 2436, files collected 371, exit 1 COLLECT-DRIFT).
- Attribution (the law: an unattributable drift is a fabrication
  smell): 09-27 carrier 2,303 / 352; +5 test files committed 09-28
  (git log --diff-filter=A since 2026-09-27: tests/test_silentpass_batch2.py,
  tests/test_demote_candidates.py, tests/test_router_comms_boost.py,
  tests/test_stealth_driver_effort_dial.py, tests/test_auto_promote.py);
  items added inside existing test files on 09-28/29; and the 09-29
  in-flight wave (untracked at refresh time:
  test_attention_eviction_order.py, test_attention_feedback_contract.py,
  test_context_checkpoint_pack.py, test_mcp_pin_wire.py,
  test_ractor_falsifier_stubs.py, test_stealth_driver_prompt_lance.py;
  test_selffeed_integration.py remains the zero-collect instrument
  gap), including this lane's own +4 regression cases in
  tests/test_census_drift_patrol.py. The prior refresh's attribution
  (09-26/27 burn-wave landings + verkle99) is kept as history.
- Live-estate caveat, stated: the tree moved DURING the lane. Timeline
  of instrument readings: 09-28 17:20 log 2410 / 368; this lane's
  first collection (2026-09-29, pre-edit) 2410 / 368; post-edit
  pre-refresh collection 2436 / 371 (other lanes landed +22 items and
  +3 files between the two readings; my edits were +4 items in one
  existing file); final finish-line check read 2437 / 371 (one more
  concurrent item, delta +1 vs the carrier, inside the bar of 20).
  The carrier is a snapshot; the denominator law (B2-216) applies.

## 3. Checks run (all this session, raw output in
watch/inbox/gala_20260925/wave5-repair/lanes/patrol-fix.check.txt)

1. `.venv/Scripts/python.exe tools/census_drift_patrol.py --self-test`
   - exit 0, 32 checks ok (30 prior + the 2 blank-line vectors),
   "CENSUS-PATROL SELF-TEST: PASS".
2. `.venv/Scripts/python.exe tools/census_drift_patrol.py --collect`
   (post-refresh) - exit 0: "census 2026-09-29 (2436 collected /
   371 files)", "files: collected 371 vs carrier claim 371" (exact),
   "collect ok - pytest 2437 vs carrier 2436 (delta +1, bar 20)".
3. `.venv/Scripts/python.exe -m pytest tests/test_census_drift_patrol.py -q`
   - 50 passed (46 prior + 4 new), 22.87s.
4. `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
   - exit 0, "RATCHET: PASS - no unregistered debt", NEW=0. Mid-flight
   the same command had shown 3 NEW claims in files this lane does not
   own (mag/corpus_gap_research.py, mag/corpus_selfsteal.py,
   tools/fossil_check.py); by finish time their own lanes had
   registered them. A GROWTH warning prints for tools/stealth_driver.py
   (accepted 753, now 907) - another lane's file, exit unaffected.
   census_drift_patrol.py stayed at exactly 403 lines = its
   accepted_lines (claim 8d41e611f98d3fa5), no growth.
5. Carrier grammar byte read: `grep -c "2,436 tests collected / 371
   files (2026-09-29 census" AGENTS.md` - 1.
6. Record-law scan (venv python) of the four edited/created authored
   files: tools/census_drift_patrol.py, tools/census_patrol_selftest.py,
   tests/test_census_drift_patrol.py, lanes/patrol-fix.json - em 0,
   en 0, nonascii 0 each. AGENTS.md added diff lines: em 0, en 0 (the
   file's 19 pre-existing em-dashes are untouched prose). The check
   file contains 2 em-dashes inside the ratchet tool's own captured
   output (verbatim tool bytes, not lane prose).

## 4. Not done / not claimed

- arch-04's other v2 items (A1 dark-day heartbeat, A2 files bar, A3
  carrier uniqueness, A4 universe pin, A5 CREATE_NO_WINDOW, A6 parity
  check, A7 --json, A8 refresh log witness, X2 --days removal) are
  design-banked in arch-04 and were NOT in this lane's owed work.
- The 08:30 MagCensusPatrolDaily no-show on 2026-09-28 (arch-04 O3)
  remains unexplained from the log alone.
- No commit was made by this lane; the working tree is shared with
  other live lanes.

## 5. Decision ledger

Closes the arch-04 v2 must-fix pair (D1 + D2): the census tripwire can
no longer be blinded into a lying exit 2 by ordinary markdown reflow,
and the patrol no longer carries a constant documenting a future
tolerance that never existed. Changes the carrier decision surface:
AGENTS.md now reads a 2026-09-29 census (2,436 / 371) with named
attribution, so the daily deep check starts green instead of
permanently COLLECT-DRIFT.
