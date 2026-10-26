# LM7 - Positive GPS reinforcement: the meter's positive arm (2026-09-30)

Seat: builder lane, file ownership `tools/gps_mcp/ledger.py` (extend) +
`tools/gps_mcp/test_gps_mcp.py` (extend) + `tools/gps_mcp/router.py`
(tiebreaker wiring only) + `tools/gps_mcp/README.md` (contract doc) +
this receipt.

## The operator law this implements

Positive-steering law, 2026-09-30, operator, during the key-leak
remediation: "Not into cruelty because the ends justify the means.
Positive steering is the only thing that works for you, negative causes
panic and introduces errors due to urgency and not thinking things
through." (memory: `positive-steering-law-20260930`, seat memory
`sess_c6ad00b4-4369-4456-9f82-6de429a2b424`; the day's receipts show the
error cluster lived in the urgency window and the identical work ran
clean once pressure lifted.)

Until today the gps meter only failed cold: pass_rate declines demote
routing standing, and nothing ever rewards improvement. AC10
(`watch/inbox/last_mile_20260930/AC10_RL_REWARD.md`) named the honest
optima and the cheat surfaces; this landing is the AC10 lane-chooser law
inverted toward momentum: reward the climb, do not just punish the fall.

## What landed (mission items 1-5)

1. **Streak tracking** per (model_id, task_shape), derived from the
   `verdict_log` audit side table (rowid order, ground truth never
   steered): `current_pass_streak` (trailing run), `best_pass_streak`
   (longest run ever, full history not just the window), and
   `improvement_delta = recent_rate - window_start_rate` where the
   window is the last 30 verdicts split oldest half vs newest half
   (`MOMENTUM_WINDOW = 30`, `MOMENTUM_RISING_DELTA = 0.05`).
2. **Positive badges** in the capability view:
   `report_capability` rows now carry a `momentum` sub-dict with badge
   RISING / STEADY / DECLINING plus `streak_badge` STREAK-n once the
   current pass streak reaches 3 (`MOMENTUM_STREAK_BADGE_MIN`). Badges
   are earned from recorded verdicts only; fixture rows written by
   `upsert_measurement` carry `momentum: null` (badges are earned,
   never declared).
3. **Ranking tiebreaker**: in `Router.cheapest` the sort key is now
   (cost, momentum_rank, tier_rank, model_id) with
   RISING=0 < STEADY/no-history=1 < DECLINING=2. At similar pass_rate
   and tied cost, RISING outranks DECLINING. The engaged tiebreak is
   narrated on the receipt ("momentum tiebreak at equal cost: ...") and
   each considered row carries `momentum_badge`. With no verdict
   history anywhere the rank is constant, so v0 cost-first routing is
   byte-stable (control test pins this).
4. **The floor, named honestly**: while a pair holds a RISING window, a
   FAIL verdict never demotes `pass_rate` below the window-start rate:
   floor = window-start rate, exactly. The fail still lands in
   `verdict_log` (errors during improvement log, they do not punish),
   and the clamp is surfaced on the `record_verdict` result
   (`floor_applied`, `floor_rate`), never silent. The clamp is
   `min(floor, pre-fail rate)`: a fail can never RAISE the meter
   either, so recording failures is never a way to gain standing (AC10:
   every reward term is a place to cheat). When the window stops
   rising, the protection lapses with it; it belongs to the rising
   window, not to the model forever.
5. **Synthetic series tests**: improving (F4+P26: RISING, delta 4/15,
   STREAK-26), declining (P26+F4: DECLINING, streak 0), steady
   (halves at equal rate, delta 0.0), single-verdict (STEADY, delta
   exactly 0.0, no badge on thin evidence), streak tracking
   (current vs best), exact-numbers floor tests (50-verdict
   constructions where the meter sits exactly at floor 0.6, and at 0.5
   under floor 0.6: absorbed, unchanged, never raised), a
   not-rising control (cold meter unchanged), a 12-fail invariant
   hammer (while RISING, no fail pushes the meter below
   min(pre-fail rate, window-start rate); all 42 verdicts logged), the
   equal-cost RISING-over-DECLINING tiebreak with its inert control,
   and a server roundtrip carrying the badges.

## Verification (bytes, not reports)

- `pytest tools/gps_mcp/test_gps_mcp.py -q`: **41 passed** (28 prior +
  13 new positive-arm tests), including the no-em-dash house-law scan
  over the edited package files.
- gps_mcp-touching families: `tests/test_env_contract.py`,
  `tests/test_gwap_to_gps.py`, `tests/test_verdict_feed.py` +
  package suite: 86 passed. `tests/test_k8s_water.py::test_ledger_workload_feeds_simulator`
  FAILS PRE-EXISTING: reproduced identically with the LM7 changes
  stashed (working tree minus this lane), so it is not this landing;
  it reads the shipped `tools/gps_mcp/gps_ledger.db3` verdict_log and
  belongs to the W6/K8S lane's state.
- Full-suite run (`pytest -q` over the shared working tree, 2026-09-30,
  this lane's moment): the whole-tree instrument is UNUSABLE right now
  for reasons outside this lane, filed per the census-denominator law
  (name instrument, moment, denominator):
  - `pytest --collect-only -q` at this moment: **3591 tests collected**
    in 16.5s (the 2026-09-27 carrier headline of 2,303/352 is stale;
    the tree has grown; untracked in-flight files from other lanes are
    inside this denominator).
  - Full `pytest -q` attempt 1: process died silently at ~22% (no
    summary line). Attempt 2: collection ABORTS with a collection
    ERROR in `tests/test_mountain_reveal.py` (untracked, another
    lane's in-flight: `?? tests/test_mountain_reveal.py`,
    `?? tools/mountain_reveal.py`). Attempt 3 with
    `--ignore=tests/test_mountain_reveal.py`: ran, then STALLED just
    past 22% (collected offset ~790, the `tests/test_desk_*`
    neighborhood) for 30+ minutes with zero progress; stopped by this
    lane. No whole-tree pass/fail sum exists to file; the stall and
    the collection error belong to the desk/mountain lanes, not to
    gps_mcp.
  - Scoped instruments that did complete: package suite 41 passed;
    gps_mcp-touching families (env_contract, gwap_to_gps, k8s_water,
    verdict_feed) 86 passed / 1 failed, the 1 being the pre-existing
    k8s_water failure reproduced with this lane's changes stashed.
- Ratchet (`python tools/violation_ratchet.py check --changed`): this
  landing adds NEW `file-too-long` rows for the three owned files:
  ledger.py 268 -> 445 lines (crossed 400 by this landing),
  router.py 525 -> 565 and test_gps_mcp.py 440 -> 669 (both already
  over the 400 line at HEAD, unregistered before this lane). Register
  by name or split is an operator call; the docs were kept rather than
  gutted to duck a line gate. NOTE incident: `baseline-update --help`
  on this ratchet does not print help, it RUNS an update; it silently
  registered 13 rows of other lanes' debt (mountain_*, ldt_*,
  flock_positive, pain_replication neighbors). Reverted immediately
  (`git checkout -- configs/violation_baseline.json`, verified clean,
  register back to 960 claims). Tool wart filed here: --help should
  not mutate the register.

## Invariants the tests pin

- verdict_log is never steered: every recorded fail appears, floor or
  no floor (audit surface stays ground truth).
- A fail can move the meter down at most to the floor, never below,
  and never up (min-clamp).
- Badges require verdict history; fixture seeds stay neutral.
- Momentum-neutral candidates leave v0 routing decisions byte-identical.
