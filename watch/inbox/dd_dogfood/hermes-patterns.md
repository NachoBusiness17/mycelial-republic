# HERMES BURN PATTERNS - the GALA lane receipt (division B, hermes-burn-patterns)

Owed waltz: mine the burn ledger for temporal / model / plan patterns; cross-reference
the TICKET_LEDGER redemption row. Lane: GALA dd-selfsteal 2026-10-03.

- Instrument: `watch/inbox/dd_dogfood/hermes_patterns_probe.py` (re-runnable, read-only)
- Frozen probe output: `watch/inbox/gala_20260925/dd-selfsteal/lanes/hermes-burn-patterns.check.txt`
- Probe moment: 2026-10-03T19:20:53Z. B2-216 note: the ledger is LIVE (descent driver
  still beating; last beat 18:58:56Z cycle=1675); earlier reads this sitting saw 1099
  rows / $62.85 and 1134 / $63.16 before this freeze at 1150 rows / $63.58. All numbers
  below are from the frozen moment; a recount will drift by live playground fires.

## 0. LEDGER PROFILE (frozen moment)

`memory/runs/hermes_burn/usage.jsonl`: 1150 rows, 2026-10-01T13:11:41Z .. 2026-10-03T19:08:04Z,
$63.58 total, 10,327,419 tokens, 910/1150 ok (79.1%). Five models: opus-5.5 (447 fires,
$45.65 = 71.8 percent of spend), sonnet-5.5 (308, $7.59), fable-5.1 (172, $8.22),
haiku-4.5 (218, $0.95), z-ai/glm-5.3-prime (5, $1.17).

## 1. TEMPORAL PATTERN: mechanism, not clock

Hour-of-day rollup (all days, UTC): best window 11:00-13:00Z (97.7 / 85.4 / 93.9 percent ok);
worst 19:00-20:00Z (52.4 / 35.5 percent) and 14:00Z (67.3 percent). The trough diagnosis
(fails by hour x class, check file section 3) shows the 19-20Z trough is 75 of the 89
refusal rows - the DUEL1_hidden_5 x46 + N1_parables_songmap x42 provider-refusal loops
that burned 18:00-20:00Z on 10-01 - not a daily cycle. The 12:00Z and 14:00Z dents are
silent-empty DND0 dungeon-beat fails (143 of the 151 silent-empty rows). Per-day: 10-01
$37.76 at 62.3 percent ok (the carrier-patch day), 10-03 $24.65 at 83.6 percent ok (the
post-patch playground day). Steal: drain the paid queue in the 11-13Z window; when a
trough appears, ask what was IN the queue before blaming the clock.

## 2. MODEL PATTERN: sonnet-5.5 is the receipt-efficiency king; fable-5.1 is a refusal magnet

Landed receipts are the 79 clean `.md` files in `watch/inbox/hermes_burn/` (header names
the model; garbage-confessing receipts excluded). Receipt bytes per dollar:

| model | fires | ok | landed receipts | cost | receipt KB per $ |
|---|---|---|---|---|---|
| claude-sonnet-5.5 | 308 | 82.8% | 39 | $7.59 | 33.9 |
| claude-opus-5.5 | 447 | 75.2% | 38 | $45.65 | 9.9 |
| claude-fable-5.1 | 172 | 57.0% | 2 | $8.22 | 3.5 |
| claude-haiku-4.5 | 218 | 100% | 0 | $0.95 | n/a (beat vehicles only) |
| glm-5.3-prime | 5 | 60% | 0 | $1.17 | n/a (2 length-truncated) |

Sonnet landed MORE receipts than opus (39 vs 38) for one sixth the money, at 3.4x the
receipt bytes per dollar. Fable-5.1 is the worst receipts-per-token model on every axis:
57.0 percent ok, 42 of the 89 refusals, $13.88/Mtok (2x opus rate), 2 landed receipts.
Haiku went 100 percent ok but only ever served TAVERN/DND0 beat actors (by design, no
hermes_burn receipts). The 2 glm-5.3-prime fails are `finish_reason: length` at the
20000 cap (GALA_OUROBOROS_PRIME_JUDGMENT rows) - z-ai fires need a staged-turn shape,
not a bigger cap. Steal: default design/spec asks to sonnet-5.5 first, spend opus on
the asks that stall under sonnet, never stage fable on contract work.

## 3. PLAN PATTERN: 84 of 87 staged asks landed; the carrier completes what it survives

Ask-state classification over `memory/plans/hermes_burn_*/*/` (check file section 4):
87 ask dirs = 80 LANDED + 4 HEALED + 2 REFUSED + 1 NEVER_FIRED + 0 FIRED_NORECEIPT
(96.6 percent landed-or-healed). The garbage class is byte-confirmed two ways:

- 4 receipts quarantined as `.poisoned-evidenceless` (T1W2_S5_stores, S6_docker,
  S7_mates, S8_stealth) - the evidence:[] fires; all 4 have clean refires on disk too.
- 2 clean-named receipts still self-confess "The EVIDENCE block is empty" in their own
  bytes: DUEL2_train_01.md and DUEL2_train_06.md (of 28 duel2 receipts).

The 2 REFUSED asks carry terminal `REFUSED` markers (hermes_burn_batch4/N1_parables_songmap,
hermes_burn_duel1/hidden_5); the 1 NEVER_FIRED is playground_20261003/PODCAST_STRUCTURE_spec
(a CLAIM marker, claimed by another lane, zero burn). Family completion: T1W1 4/4,
T1W2 4/4 healed, T1W3 3/3, T2 3/3, T3 2/2, batch1-4 10/10, duel1 11+1refused/12,
duel2 28/28, playground 14/15, refire 3/3.

## 4. WASTE PATTERN: three named classes ($24.74 + $14.90-ambiguous + $4.05)

- W1 plan-ask re-burn theater: 74 ok turn-1 rows re-firing already-landed ids =
  $24.74 = 38.9 percent of all spend. A1_steer_antiforgery alone: 52 ledger rows,
  48 after its landing ($20.60 post-16:10Z), 4 before ($1.65) - reconciles with the
  carrier docstring's "45x at $20.53" (written mid-drain; the drain continued to
  20:17Z). The cure is already in the carrier (`tools/hermes_burn.py:206` _landed_skip,
  the single choke point); it cures NEW staging only.
- W2 beat-vehicle id collision: TAVERN/DND0 ids carry no run-dir stamp
  (`tools/tavern.py:10` documents `TAVERN_<run>_r<round>_<actor>` but
  `tools/tavern.py:157` emits `TAVERN_r{rnd}_{name}`), so every replayed playground
  run reuses ids: 665 same-id ok rows / $14.90 that the ledger alone cannot split into
  game turns vs replays. Side effect: the doubled-key ingest alarm is saturated -
  809 of 1150 rows flagged (70.3 percent) - which is alarm fatigue by construction.
- W3 provider-side losses: 89 refusal rows billed $0.00 (wall-clock disease, cured by
  the REFUSED-IS-TERMINAL patch), 151 silent-empty rows billed $0.47 (DND0 x143),
  and $3.58 of paid fires whose receipts confess or were quarantined. Clean money:
  roughly $35.26 of $63.58 produced first-pass clean receipts.

## 5. TICKET_LEDGER CROSS-REF (50/37/74)

The ask's 50-issued / 37-run / 74-percent claim is verified in bytes:
`watch/inbox/hermes_burn/TICKET_LEDGER.md:117-118` reads "Row one: issued 50 / run 37 /
parked 13 / dropped 0-known. Reconciles: 37 + 13 = 50. Redemption rate 74.0 percent (was
65.3)." Cross-reference to the burn lanes:

- The 6 duel refires (parked per row one) ARE the hermes_burn_duel1/hidden_*_r2 plans -
  all 6 landed receipts exist on disk now, so that parked tail converted after row one.
- The T1W2 refire debt is the poisoned-evidenceless quartet - all 4 now HEALED with
  clean refires.
- The gap between the carrier's 96.6 percent ask completion and the ledger's 74.0
  percent ticket redemption lives in the prose-ticket parked tail (5 deliberate CLIMB
  deferrals, memlance witness, quant tag, V12 .bak, V15 sid, Godot precompile), not in
  paid-ask failure. The paid carrier does not stall; it over-completes by re-burning
  (W1). Redemption risk and burn waste are DIFFERENT diseases with different owners.

## 6. LAWS MINED (with falsifiers)

1. LANDED-BEATS-FORCE (already law, now quantified): 38.9 percent of the burn's first
   three days went to re-fires of landed asks. Falsifier: a burn week where W1 rows
   stay under 5 percent of spend without the entry check would kill this law.
2. RECEIPTS-PER-DOLLAR BEATS TOKENS-PER-DOLLAR: sonnet 33.9 KB/$ vs opus 9.9 KB/$;
   fable 2 receipts for $8.22. Falsifier: a sonnet-first week where opus-tier asks
   fail sonnet review more often than the 4.5x cost delta saves.
3. MECHANISM-NOT-CLOCK: every trough hour is explained by queue content (refusal
   loops, empty-channel dungeon beats), zero by hour alone. Falsifier: a trough hour
   that stays bad across three different queue compositions.
4. ID-STAMP OR THE LEDGER LIES: without the run stamp in the id, 665 rows / $14.90
   are unanalyzable and the doubled-key alarm saturates. Falsifier: after stamping,
   zero new rows sharing an id across run dirs.
5. COMPLETION IS NOT REDEMPTION: 96.6 percent paid-ask completion coexisted with 74.0
   percent ticket redemption; the difference is parked prose tickets. Falsifier: a
   future row where paid asks stall while prose tickets convert.

## 7. GAPS (honest)

- W2 replay-vs-turn ambiguity is NOT resolved: pricing it as waste would fabricate a
  number; pricing it as clean would ignore the collision. The fix is a one-line id
  stamp in tools/tavern.py (left for its owner; this lane touched no tools/ code).
- The launcher that re-fires tavern/dnd runs every ~15-60 min (run dirs
  tavern_20261003T171056Z .. 190348Z under watch/inbox/playground/, each DONE +
  GWAP_BANKED) was not identified to its process; only its run-dir trail is cited.
- The SHERPA-lane results files in memory/runs/hermes_burn/ (socratic, deepgemm,
  ds_baseline, xmodel_cross, judge2_duel, lens1_sherpa, assemble: 3-14 rows each) bank
  ZERO rows in usage.jsonl - they are the free-lane SENSING legs, so "best results per
  token" cannot be scored for them from this ledger.
- The ledger moved during the sitting (1099 -> 1150 rows); per B2-216 only the frozen
  moment is authoritative.

## 8. SELF-CHECKS RUN THIS SITTING

1. Probe: `.venv/Scripts/python.exe watch/inbox/dd_dogfood/hermes_patterns_probe.py`
   exit 0, raw output frozen at the check-file path above.
2. Citation lint on this receipt (self-dogfood, not asked):
   `.venv/Scripts/python.exe tools/citation_lint.py check --files watch/inbox/dd_dogfood/hermes-patterns.md`
   exit 0 (4 anchors, 0 blocking, 0 warns) after one TOKEN-MISS warn was fixed by
   widening the TICKET_LEDGER citation to lines 117-118 with the claim tokens inline.
3. Citation lint on the raw check file: exit 1, 8 blocking PHANTOM-NUMBER findings -
   the tool's own documented prose-heuristic class hitting a machine table (the table
   numbers' true source is memory/runs/hermes_burn/usage.jsonl, which the check file is
   the receipt for). Left unedited: raw instrument output is not rewritten to please a
   prose heuristic.
4. Violation ratchet: NOT run - this lane touched no code under mag/ or tools/ (the
   probe lives under watch/inbox/dd_dogfood/).
