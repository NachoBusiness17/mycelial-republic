# EXECUTOR-SWEEP: routing tables vs production consumers (2026-10-03)

Lane: executor-sweep, division B, GALA 20260925 / build-it-all.
Owed law: the executor law mined in
`watch/inbox/gala_20260925/localfirst-steal/lanes/atlas.json` rows[1]
(Atlas AUTO_APPLY defect): "A routing bucket that no module consumes is a
claim that work happened when it did not; Atlas declares auto-apply and
ships no executor." The same law's estate-facing steal names this sweep:
"grep our own routing tables (effect broker, doctrine arbiter) for buckets
with no consumer" (`watch/inbox/localfirst-steal_RECEIPT.md` item 2).

## Surfaces swept and method

1. `mag/effect_broker.py` BROKERS dict (7 declared effect routes).
2. `mag/switchboard_v2.py` EFFECTS list (mirrors the broker) plus the
   reconcile rules in `_detect_unmet` (producer side of the same routes).
3. `mag/policy_engine.py` DEFAULT_POLICY effects + require_confirmation
   lists, and the live `memory/policy.json` copy.
4. `tools/doctrine_arbiter.py` instrument table (gps_ledger, duel_table,
   parity_gate, anomaly_counts) and its kind taxonomy, measured against
   `memory/doctrine/LEDGER.jsonl` registrations.

Consumer test per bucket: grep production code (mag/, tools/, tests/,
main.py, scripts/, configs/) for any module dispatching INTO the bucket,
split test-only from production consumers, then check the empirical
production ledgers (`memory/runs/effect_broker/effects.jsonl`, the broker
receipt tree, `memory/runs/switchboard/trail.jsonl`) for whether the route
has ever carried work. A code path that exists but has banked zero
production work is exactly the Atlas shape: a claim of work, not work.

## The census (byte-backed, checks in executor-sweep.check.txt)

| bucket | declared in | module consumers | production work ever | verdict |
|---|---|---|---|---|
| board_write | BROKERS, EFFECTS, policy x2 | state_snapshot.py:169, swarm_cycle.py:129, harness.py:295 | 3 meter rows + 15 non-test receipts | LIVE, keep |
| tool_invoke | all 4 tables | ZERO (harness.py:470 is test scenario 2) | 0 receipts (trail: 10 DENIED + 1 AUTHORIZED reconcile proposals) | DORMANT, registered |
| model_call | all 4 tables | ZERO (tests/test_effect_broker_ah18.py:64 only) | 0 receipts | DORMANT, registered |
| network_access | all 4 tables | ZERO (tests/test_effect_broker_fix.py:108 only) | 117 receipts, ALL test-prefixed | DORMANT, registered |
| fs_write | all 4 tables | ZERO (harness.py:503 is test scenario 3) | 74 receipts, ALL test-prefixed | DORMANT, registered |
| lane_spawn | all 4 tables | ZERO (tests/test_effect_broker_ah18.py:178,201,240 only) | 0 receipts, 0 trail rows (the board_quiescent reconcile rule never fired) | DORMANT, registered |
| verkle_link | all 4 tables + a reconcile rule | ZERO anywhere (code grep matches only the declaring tables) | 11 trail rows on 2026-08-31 (7 DENIED + 4 AUTHORIZED), ZERO executions, 0 receipts, 0 meter rows | DEAD, KILLED |

Doctrine arbiter: NOT consumer-less. All 4 instruments are consumed by at
least one registration in memory/doctrine/LEDGER.jsonl (duel_table 2,
parity_gate 2, anomaly_counts 1, gps_ledger 1; the 7th registration,
minimal-exposure-law, is VOID by the pre-registration four-tuple law with
an empty instrument, which is the designed behavior, not a defect). The
arbiter's production consumer is `tools/cycle_brief.py:125`
(`_run("tools.doctrine_arbiter", "scorecard")`).

## The production-trail proof that verkle_link was the Atlas shape

The reconcile rule at `mag/switchboard_v2.py:713-716` (pre-sweep) declared
`{"condition": "missing_fork_verdicts", "eligible_organ": "verkle_lance",
"capability": "verkle_link"}`. It fired 11 times in production on
2026-08-31 (memory/runs/switchboard/trail.jsonl, event ids
`reconcile:missing_fork_verdicts:*`): 7 proposals DENIED, 4 AUTHORIZED.
Zero of the 4 authorized grants were ever executed: no EXECUTING,
COMPLETED or FAILED trail rows, zero broker receipt files, zero meter rows.
Eleven declarations of work, zero work. That is the AUTO_APPLY defect in
estate code, not just in the mined repo. The declared "eligible organ"
(verkle_lance) is real but reached in production by direct imports in 9
modules (ask_router, game_campaign, ghost_server, novelty_lens,
openclaw_catalog, reconstruct, route_trace, spine_exercise, swarm_cycle);
the broker bucket was a second door nobody ever walked through.

## Fixes applied this sitting (KILL + REGISTER, 4 files)

1. KILLED verkle_link everywhere it was declared:
   - `mag/effect_broker.py`: removed from BROKERS, removed
     `_broker_verkle_link`, removed its branches in `_pre_state`,
     `_post_state` and `_postcondition_evidence`; ROUTING-TABLE STATUS
     block added to the module docstring naming every bucket's consumer
     state (this is the durable dormant-registration for the 5 DORMANT
     buckets too).
   - `mag/switchboard_v2.py`: removed from EFFECTS; tier-gate comment
     updated ("low-impact effects (board_write, verkle_link)" to
     "(board_write)"); the `missing_fork_verdicts` reconcile rule removed
     with its `fork_verdict_knot` seen-key and detector, kill receipt in
     the comment.
   - `mag/policy_engine.py`: removed from DEFAULT_POLICY effects.
   - `memory/policy.json`: removed from the live policy effects list.
   Fail-closed both layers (check file CHECK 6):
   `execute("verkle_link")` now returns FAILED with
   `authority check failed: unknown/disabled effect verkle_link`, and
   `policy_engine.validate_authority` denies with
   `unknown/disabled effect verkle_link`. A denied cheap route is
   recoverable; a declared route that claims work and never runs it is the
   defect.
2. REGISTERED the 5 DORMANT buckets (tool_invoke, model_call,
   network_access, fs_write, lane_spawn) in the effect_broker module
   docstring ROUTING-TABLE STATUS block: zero organ dispatches is their
   deliberate state (high-impact tier gate in
   `switchboard_v2._implicit_authority` + `require_confirmation` policy),
   the operator CLI and harness confirm path are their intended consumers.
   Killing them would have deleted documented operator capability (T1
   Kabuki tier verdict, switchboard_v2.py:314-316); the AH18 receipt
   (`watch/inbox/last_mile_20260930/AH18_BROKER_STUBS.md`) already paid
   for their real implementations.

Not touched, named for honesty: `_detect_unmet` also tracks
`prediction_measurement` and `principle_protocol` seen-keys that no rule
ever appends from (counted, never routed). They declare nothing, so they
are dead booleans, not consumer-less buckets; left for the owner.

## Gates run

- `tools/violation_ratchet.py check --changed`: PASS, exit 0, NEW=0
  (12 pre-registered debts, none mine).
- Covering tests: `pytest tests/test_effect_broker_ah18.py
  tests/test_effect_broker_fix.py tests/test_effect_broker_production.py
  tests/test_switchboard.py -q -p no:cacheprovider`: 35 passed, exit 0.
- Check battery: 11 checks in
  `watch/inbox/gala_20260925/build-it-all/lanes/executor-sweep.check.txt`
  (consumer greps, meter census, receipt census, trail census, fail-closed
  proof, BROKERS keys, doctrine census, ratchet, pytest).

## Decision ledger

Closes: the executor law's inward-pointing steal ("the estate's own
routing tables owe the same no-consumer grep"). The law's falsifier named
"an estate routing bucket proven wired" as what would dissolve it; this
sweep instead proved one estate bucket (verkle_link) consumer-less at the
production-trail level and killed it, and registered the five
deliberately-dormant operator-tier buckets so the next grep reads intent
instead of re-deriving it. Changes the routing-table spec:
effect_broker.py ROUTING-TABLE STATUS is now the standing census location;
future bucket additions must state their consumer at birth.
