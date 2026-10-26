# R10_DOCTRINE_ARBITER — doctrine is measured, not obeyed: pre-registration ledger + check pass + scorecard

2026-09-30 · seat: zcode (R10, last_mile) · ownership: `tools/doctrine_arbiter.py`,
`tools/doctrine_arbiter_core.py`, `tools/doctrine_arbiter_instruments.py`,
`tests/test_doctrine_arbiter.py`, the seeded `memory/doctrine/LEDGER.jsonl` +
`memory/doctrine/scorecard_latest.json` (the tool's own output surfaces), this
receipt. No commit by me (operator order).

## Mission (the frontier interrogation's #1 structural finding, ASK6)

"a single verdict can reach every lane before anything measures whether the
doctrine itself improved outcomes." Ribs, spec amendments, and route pitches
become law the moment a verdict blesses them; nothing ever asks whether the
predicted world arrived. The arbiter v0 is that measurement: every piece of
doctrine pre-registers a falsifiable outcome bound to an estate instrument, and
a check pass scores each item VINDICATED / EXPIRED / PENDING.

## What landed

1. **Three modules** (split forced by the ratchet's 400-line file cap — the
   first single-file build was 822 lines with 2 NEW violations; fixed by
   structure, not by registering debt):
   - `tools/doctrine_arbiter.py` (324 lines) — the spec (three laws, instrument
     table, verdict semantics) + CLI: `register` / `check` / `scorecard` /
     `retire`, `--from-json` batch path, all instrument paths injectable.
   - `tools/doctrine_arbiter_core.py` (336) — pre-registration law as code
     (`prediction_void_reasons`), append-only ledger + `fold_ledger` (event
     stream: registration / check / retirement rows; state is always a fold),
     `run_check`, scorecard render + JSON artifact
     (`memory/doctrine/scorecard_latest.json`, schema `doctrine_scorecard.v1`).
   - `tools/doctrine_arbiter_instruments.py` (140) — read-only adapters over
     the four instruments named by the mission: **gps ledger pass_rate**
     (`tools/gps_mcp/ledger.py` CapabilityLedger, `gps_ledger.db3`),
     **duel table** (`logs/duel/duels.jsonl`; winner already logical A/B per
     the harness's slot-swap remap; TIE/UNPARSED excluded from decided),
     **parity gate** (`tools/rule_parity_out/latest.json`, the D2 standing
     artifact; optional `mode` selector, mismatch = no data not error),
     **anomaly counts** (`tools/anomaly_flagger.py` scans; the anomalous ROW is
     the unit; optional `surface` selector).
2. **Pre-registration law (mission #4).** The registration contract is the
   four-tuple {id, source_verdict, predicted_outcome, deadline}. Missing /
   all-blank / uncheckable prediction (unknown instrument, metric, selector
   key, op), missing id or source, unparseable deadline → the row is still
   appended but **VOID at registration**: never checked, never active doctrine.
   Duplicate ids refuse hard (exit 2, nothing written). Predictions are
   structured `{instrument, metric, selector, op, value}` — no judge model in
   the loop; the check pass is mechanical.
3. **Check pass + scorecard (mission #2, #3).** Per PENDING item: query its
   instrument; append one check row banking `measured`, `satisfies`, verdict,
   and the FULL `instrument_saw` doc. Verdicts: PENDING (not yet, deadline
   unpassed), VINDICATED (measured true **on a check that ran on/before the
   deadline** — a truth first measured after the term is a late arrival, not a
   vindication; terminal and permanent, later drift cannot un-vindicate),
   EXPIRED (deadline passed unmet; terminal; flagged RETIRE CANDIDATE). Dark
   instrument surface (missing stream) = InstrumentError exit 2, distinct from
   no-data (unmeasured gps pair, zero decided duels, wrong parity mode →
   PENDING, never a fake vindication).
4. **Operator retirement gate (mission #3).** `check` only scores; EXPIRED is
   flagged, never auto-removed, never reworded. `retire --id --note` is the
   only close, refused (exit 2) on PENDING/VOID — retiring an unmeasured
   prediction would dodge exactly the measurement this tool exists to force.
5. **Tests.** `tests/test_doctrine_arbiter.py`, **39 passed in 2.1s**
   (instrument: `pytest tests/test_doctrine_arbiter.py -q`, 2026-09-30
   ~23:05 UTC). Fixtures: gps db via CapabilityLedger, duel jsonl, parity
   latest.json, anomaly streams (absolute landings — pathlib join law).
   Pinned: every void reason class, duplicate refusal, win_rate logical-side
   mapping + TIE/UNPARSED handling + zero-decided no-data, parity mode
   mismatch, anomaly row-units + surface scoping, in-term vindication law
   (`test_late_truth_is_not_vindication`), freeze semantics (second check adds
   no rows on terminal items; later drift cannot un-vindicate), retire gate
   refusals, append-only (registration line byte-identical after check+retire),
   scorecard artifact + ordering + exit codes 0/1/2, VOID rendering, empty
   ledger, `--from-json` both arms, fold robustness (orphan/rogue rows).

## Live dogfood (real instruments, real receipts, 2026-09-30 ~23:17 UTC)

Three items seeded from real doctrine, one live `check` pass banked:

| id | kind | source verdict | prediction | verdict (measured) |
|---|---|---|---|---|
| rib-driving-ladder-duel | rib | memory/rib/RIB_DRIVING_LADDER_20260928.md | duel_table.win_rate >= 0.55 [glm-5.3-prime] by 10-15 | **VINDICATED** (0.611, 54 decided) |
| spec-parity-standing | spec_amendment | D2_PARITY_GATE.md | parity_gate.parity_ok == true by 10-07 | **VINDICATED** (full, 100 seqs) |
| spec-anomaly-clean | spec_amendment | IMP6_ANOMALY.md | anomaly_counts.anomaly_count <= 0 by 10-07 | **PENDING** (measured 98) |

The PENDING row is the arbiter doing its job honestly: the live sweep names 98
anomalous rows (byte-checked via `python tools/anomaly_flagger.py`, 2026-09-30
~23:25 UTC: steps 38 = 36 malformed_json + 1 hash_shape + 1 ts descent over
38,466 rows; oral_law_index 60 ts_sort descents over 183 rows — the class IMP6
already triaged as structural from the miner's seeded shuffle; burns clean),
so "stays clean" is currently NOT materialized and will EXPIRE on 10-07 unless
the streams heal or the operator retires/re-scopes the claim (e.g.
`surface=steps` alone would still read 38; an honest threshold budgets the
accepted structural descents). That is the ASK6 loop closing: doctrine now
carries a date and a number, and the estate's own instruments grade it.

## Refire pass (same day ~23:47 UTC): today's four named doctrines + the FIRST SCORECARD

The R10 refire named four pieces of today's doctrine. All four landed in the
ledger (one by being honestly VOID):

| id | kind | source verdict | prediction | verdict (measured) |
|---|---|---|---|---|
| lensing-route-reorder | route_pitch | `watch/inbox/mountain_climb/THE_LENSING.md` (applied by R12_PITCHES.md) | parity_gate.parity_ok == true by 10-07 (the reordered XP6 parity spine holds while it lands) | **VINDICATED** (true, 0 diverged) |
| positive-steering-gps | rib | `LM7_POSITIVE_GPS.md` (operator law 2026-09-30) | gps_ledger.pass_rate >= 0.83 [z-ai/glm-5.3-prime, night-judgment] by 10-07 (the LM7 positive arm holds the workhorse's standing rate) | **VINDICATED** (0.8333, n=6) |
| animal-gates-grok47 | rib | `memory/rib/RIB_MODEL_GATES_20261001.md` + `tools/animal_profiles.py` | duel_table.win_rate >= 0.75 [x-ai/grok-4.7] by 10-07 (the gate law's champion stays champion-class as duels land) | **VINDICATED** (1.0, 9 decided) |
| minimal-exposure-law | rib | `memory/rib/RIB_MODEL_GATES_20261001.md` (OPENCODE/z.ai section) | none — no instrument grades env hygiene | **VOID at registration** |

The VOID row is the pre-registration law firing on live doctrine, not a
failure: "scheduled tasks carry NO env; whitelist exactly the two ZAI vars,
never the full .env" cannot pre-register a checkable prediction because none
of the four instruments (gps / duels / parity / anomaly) ever observes env
exposure. The arbiter records the item, marks it never-active (exit 1
attention), and the honest reading is: this doctrine is currently unmeasured;
build the instrument first, then re-register a four-tuple.

**FIRST SCORECARD** (7 items, check pass 2026-09-30T23:47:05Z, artifact
`memory/doctrine/scorecard_latest.json`):

> VINDICATED 5 | EXPIRED 0 (retire candidates) | PENDING 1 | VOID 1 | RETIRED 0

The lone PENDING is `spec-anomaly-clean` (98 anomalous rows vs <= 0 by
10-07) — the only item currently heading for EXPIRED and the retirement gate.
VINDICATED items are terminal and frozen; a keep-holding claim needs a NEW
item with a NEW deadline (the freeze law working as designed).

## Numbers (instrument + moment named, census law)

- New tests: 39 passed / 1 file (`pytest tests/test_doctrine_arbiter.py -q`,
  2026-09-30 ~23:05 UTC; executed denominator, this file only).
- Related surfaces re-run clean: tests/test_anomaly_flagger.py +
  test_duel_harness.py + test_gwap_to_gps.py → 39 passed (same moment).
- Full-suite run: no completed whole-tree sum exists to file — the census
  section below records the attempts and the stall byte-honestly.
- Ratchet: `python tools/violation_ratchet.py check --changed` → **zero NEW
  violations in the three doctrine files** (pre-split there were 2: file-too-long
  822>400 + except-pass; both fixed by the module split and the nested-try in
  `_parse_value`; the NEW rows the ratchet still lists belong to sibling lanes'
  files — pain_replication/runner.py, tip_witness.py — not this lane).

## Known edges (v0, named not hidden)

- duel_table v0 counts every ledger row including altjudge re-judgments
  (double-counts rejudged asks); a `rejudge_of` dedupe is the v1 move.
- The gps instrument is exercised by tests via fixture dbs; the live seeded
  items do not use it (no live doctrine claim on gps yet — LM7's momentum work
  is the natural first claim).
- `anomaly_counts <= 0` is a blunt first claim (see dogfood note above); the
  selector exists precisely so claims can scope to a surface.

## Full-suite census

- Collected denominator (byte-backed, this lane's moment): `pytest
  --collect-only -q` at 2026-09-30 ~23:44 UTC → **3,876 tests collected in
  20.2s** (the AGENTS.md carrier headline of 2,303/352 is stale; the tree has
  grown; other lanes' untracked in-flight files are inside this denominator).
- Executed denominator (whole tree): **NO SUM EXISTS TO FILE — the
  whole-tree instrument stalls.** Full `pytest -q` run started 2026-09-30
  ~23:45 UTC; at ~00:15 UTC the process was CPU-flat (8911.6 → 8927.9 CPU-s
  over 5 wall minutes, ~0.05 cores) with zero progress — the same stall
  LM7_POSITIVE_GPS.md documented just past 22% (its neighborhood:
  `tests/test_desk_*`). Killed at ~25 minutes elapsed; nothing was counted,
  no hand-written substitute. The stall belongs to the desk/mountain lanes,
  not this one; until it heals, every lane's honest census is scoped.
- Scoped executed instruments at this moment (byte-backed):
  `pytest tests/test_doctrine_arbiter.py -q` → **39 passed in ~2.0s** (this
  receipt's ownership, re-run after the refire registrations — the tool code
  is unchanged; the ledger growth touched no test fixture).
- Ratchet (`python tools/violation_ratchet.py check --changed`): zero NEW
  violations in the doctrine files; the 4 NEW rows it lists
  (flock_parity.py, mountain_selfplay.py, reverse_map.py,
  trajectory_minimizer.py) belong to sibling lanes.
