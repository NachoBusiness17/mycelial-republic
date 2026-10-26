# NIGHT SHIFT CLOSE - 2026-10-05 (four doors landed, bubbles kept blowing)

Open receipt: NIGHT_SHIFT_20261005_OPEN.md (the operator's bubbles
good-night, canon). Close: 08:50Z. Health at close: scheduler alive
through 08:34:10Z, research lane cycling rc=0, errno-22 last row still
03:59:15Z (the twin-site cure commit 3b271d44c rides the next cage
restart - see decisions owed).

## The night's landings (all doors struck in the eleven-doors ledger)

1. **D5 errno-22 DISPOSITIONED + twin-site cured** (3b271d44c). The
   ledger's "dormant since 12:31:38Z" was STALE: 4,674 lifetime rows,
   day-buckets 3848 (09-29) -> 311 (10-04) -> 1 (10-05), and today's
   single row at 03:59:15Z is "mirror fail research" - the UNCURED
   TWIN of the state-path O_TRUNC class (plain write_text through the
   cage bind mount; no daemon restart gaps). NOT daemon-masked; the
   10-04 cure was class-incomplete. Fix: _atomic_copy ports the proven
   tmp+os.replace rename-CAS to _mirror; 3 tripwire tests.
2. **EG-20 pass@K coverage column LANDED** (f7f6b6e2b, gap register
   row closed). tools/gps_mcp/coverage.py: problem key = arena run
   parsed from gwap scene_id inside evidence_bytes (209 keyed = 209
   resolved on production; the 252 unkeyed rows are exactly the pre-a04
   unresolved class, excluded AND reported). PROOF ON ONE BATCH (58
   problems): all-fleet pass@K 0.586 vs best single 0.500 (+0.086
   collective) BUT cheap mesh (haiku+sonnet) 0.349 < frontier (fable)
   0.500 -> ROUTE_FRONTIER. The column separates what win rate could
   not: coverage is collective across tiers, not within the cheap tier.
3. **D7 GPS capability metabolism LANDED** (ae2712f89).
   tools/gps_mcp/metabolism.py: alpha-decay (tau 14d toward 0.5 prior -
   decay measures absence, not merit), dispute-streak slashing
   (0.85^min(streak,3)), drift-patrol-keyed epoch reset (explicit
   marker; pre-marker rows collapse to prior). Read-only: stored mean
   stays the audit surface. Production proof: 4.4d-stale rows decay
   1.000 -> 0.866; glm-prime adv-review 7-fail streak 0.435 -> 0.278;
   haiku 10-fail streak -> 0.030.
4. **D6 monoculture agreement-rate proxy LANDED** (7bf3bcec8).
   tools/monoculture_proxy.py: roshomon primitives imported, grouping
   loop reimplemented (NEVER compare - k8s-welded), threshold sweep
   0.40/0.55/0.70, UNMEASURABLE verdicts for the falsifier's
   all-or-nothing case, history + attention.md alert on core-size drop.
   Baseline: 7 lanes / 929 instances / agreement 0.117 @0.55 - 88% of
   what lanes say is single-witness; the estate is far from
   monoculture. The identical-texts test caught two real module
   defects pre-ship (both fixed, stale-semantics history rows cleared
   honestly).

Test total tonight: 26 new tests landed (3 mirror-atomic + 10 coverage
+ 7 metabolism + 6 monoculture), every suite green at its own commit
with RC captured before pipes; the final combined pass ran 23 (the
three GPS-side files) - the census-denominator law applied to our own
night: name the file set behind every count. Ratchet PASS at every
gate.

## Decisions owed to the operator (morning)

1. **Cage restart**: the D5 mirror cure is committed but the scheduler
   daemon inside the cage runs old code until its next restart - the
   one lever that loads _atomic_copy (and confirms the cure on live
   cycles).
2. **Epoch stamping (D7)**: `python tools/gps_mcp/metabolism.py
   --set-epoch "reason|ts"` collapses 26/30 capability rows to the 0.5
   prior (tainted-era) leaving today's 4 arena rows standing. Deliberately
   NOT stamped overnight: with mates parked and arena the only live
   feeder, flattening every non-arena routing row is the operator's
   call. The demo proves it works.
3. **Router wiring**: the router still reads stored pass_rate; wiring
   it to effective rates (metabolism) is one import away and a
   separate act.

## Board state at close

Doors remaining open: D3 (clippy-as-prober), D8 (decay-family schema
port), D9 (gate triage: agentmemory pin + Gero-4B), D11 (three-signal
query broker), D12 (gwap v3 backfill, operator-gated), D13 (parked).
D10 (weld ractive) promoted-schedulable. Vast stage-1 pick (3090 vs
4090) still on the operator. Kit v0.3 queue unchanged (handbook mine,
profile-grower card, Hermes reasoning_effort fields, profile
import/export).

Banked by GLM-5.3 window, night shift 2026-10-05. The bubbles were
kept blowing: every lane that popped this night is remembered in the
chain.
