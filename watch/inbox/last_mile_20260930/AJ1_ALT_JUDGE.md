# AJ1 - ALTERNATE-JUDGE REPLAY OF BANKED W8 DUELS - 2026-09-30

Mission (operator, W8 follow-up #1): every duel verdict in
logs/duel/duels.jsonl is ember-judged only, and LW9 measured slot-A
position bias at p=0.0436 (n=30), so the verdicts need a second judge.
Re-judge 10 banked W8 answer PAIRS with a DIFFERENT judge, blind,
positions preserved, WITHOUT regenerating answers; report agreement
rate, flips, and whether the W8 tier-split (glm/ds 6-0, grok/qwen 0-6)
survives. Budget line was "~$0.03" (see Budget honesty below).

## THE RESULT: 10/10 AGREEMENT, ZERO FLIPS, TIER-SPLIT SURVIVES INTACT

Alternate judge z-ai/glm-5.3-prime (all 12 W8 rows were ember-judged, so
the swap direction is ember -> glm-prime). 10 replays, $0.1246 total,
pool NOT 402 today (probe ok at $0.000016).

| ask_id | banked (ember) | alt (glm-prime) | agree | alt judge_cost |
|---|---|---|---|---|
| w8-plan-glm-grok | A (glm) | A (glm) | yes | $0.0074 |
| w8-plan-grok-ds | B (ds) | B (ds) | yes | $0.0076 |
| w8-plan-ds-qwen | A (ds) | A (ds) | yes | $0.0067 |
| w8-plan-qwen-glm | B (glm) | B (glm) | yes | $0.0071 |
| w8-schema-glm-grok | A (glm) | A (glm) | yes | $0.0146 |
| w8-schema-grok-ds | B (ds) | B (ds) | yes | $0.0163 |
| w8-schema-ds-qwen | A (ds) | A (ds) | yes | $0.0124 |
| w8-schema-qwen-glm | B (glm) | B (glm) | yes | $0.0115 |
| w8-adv-grok-ds | B (ds) | B (ds) | yes | $0.0248 |
| w8-adv-ds-qwen | A (ds) | A (ds) | yes | $0.0162 |

Agreement rate 10/10 (100 percent). Flips: NONE. Every criterion-level
verdict was not compared (banked criteria vs alt criteria differ in
wording) but no winner moved at any pair.

## Tier split under the alternate judge

From the 10 re-judged rows (banked record over the same 10 is identical):

| family | ember (same 10) | glm-prime rejudge |
|---|---|---|
| glm-prime | 4-0 | 4-0 |
| ds-v4.1-flash | 6-0 | 6-0 |
| grok-4.3 | 0-5 | 0-5 |
| qwen3.7-flash | 0-5 | 0-5 |

The two-tier split (glm/ds sweep, grok/qwen swept) SURVIVES the alternate
judge unchanged. Strongest corroboration: ds goes 6-0 under a judge from
a different family than its opponents' wins.

## Slot-A watch (the reason this mission exists)

Under the alternate judge, slot A won 8 of 10 (both slot-B wins are ds).
One-sided binomial p = 0.0547 at n=10 - same lean LW9 measured at n=30
(p=0.0436). Two independent judges leaning the same direction is mild
evidence the position effect lives in the arena, not in one judge. The
router row must still be position-debiased (LW9 law stands).

## Method (why the comparison is clean)

- tools/duel_harness.py gained run_rejudge(orig_row, task, a_text,
  b_text, judge_model): replays the JUDGE call only. Rubric, slot layout
  (swap: positions preserved, not re-sampled) and contender identities
  come from the banked row; the judge prompt is byte-identical to what
  ember saw (same ask, rubric, ANSWER_LIMIT trims, blind A/B tags).
- Provenance gate: loaded answers must match the banked a_chars/b_chars
  exactly or the replay refuses (answer drift protection). All 10 passed.
- The adv ask embeds the full tools/duel_harness.py source, and the
  harness gained run_rejudge for this mission - so the driver builds the
  adv ask from the frozen v1.1 blob aj1_frozen_harness_v11.py (sha256
  aed6338ad70da357ed6f81432bb7fe84cea83c13e362397c05bea4763cd4a4c9,
  byte-matched to the HEAD commit W8 ran on, tree was clean). No contender
  was fired; nothing was regenerated.
- New rows: mode="altjudge", ask_id "<orig>|rejudge-glm-5.3-prime",
  rejudge_of=<orig ask_id>, contender costs copied from the banked row,
  judge_cost metered from usage.cost. 10 rows appended to
  logs/duel/duels.jsonl.
- Selection rule (10 of 12): dropped w8-adv-glm-grok and w8-adv-qwen-glm.
  The adv ask is the biggest per-call cost (embeds ~20KB source) and both
  dropped rows flank glm, halving glm self-judging exposure in the kept
  set. Every family and every pairing kept at least 2 samples per kept
  shape.

## Disclosures and caveats

- SELF-JUDGE CONFOUND: glm-prime judged duels whose glm-side texts were
  authored by GLM-5.3 (this account's session model, per W8 provenance).
  Blinding hides names but self-recognition cannot be excluded for glm's
  4-0; ds's 6-0 under the glm judge is the cleaner signal. A future AJ2
  should rotate a non-contender judge family.
- Budget honesty: the "~$0.03" line prices ember judging; the glm-prime
  rate card is 10x/12.5x ember's. Driver hard cap was set at $0.75,
  cheapest pairs first; actual spend $0.1246 + $0.000016 probe (4x the
  estimate, disclosed, still spare-change scale).
- Both judges route through the same Nous gateway; a gateway-level
  systematic quirk would hit both. Ember and glm-prime share no family.
- The glm judge emitted one long rationale (adv ds-qwen, 1411 chars)
  that itself misread retro mode's KeyError claim - judge rationales are
  color, verdicts are the datum.

## Files owned / landed

- tools/duel_harness.py: run_rejudge + docstring (FILE OWNERSHIP honored)
- tests/test_duel_harness.py: +2 tests (replay prompt identity, swap
  remap on replay, drift/rubric refusals); file now 13 passed
  (.venv/Scripts/python.exe -m pytest tests/test_duel_harness.py -q)
- watch/inbox/last_mile_20260930/aj1_alt_judge.py (driver, idempotent,
  --dry plan, spend-guarded)
- watch/inbox/last_mile_20260930/aj1_frozen_harness_v11.py (frozen ask
  source, sha-verified)
- watch/inbox/last_mile_20260930/aj1_run.log (full fire log)
- logs/duel/duels.jsonl: 10 new mode=altjudge rows
- This receipt.
