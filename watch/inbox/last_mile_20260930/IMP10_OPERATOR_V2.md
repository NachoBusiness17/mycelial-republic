# IMP10 — operator model re-based on unfiltered counts (2026-09-30)

Mission: N1's kill on the operator-model doc ("the instrument is pointed at its own
commissioner... under 0.1% quote sampling with no base-rate contrast"). ACTION executed:
re-based on UNFILTERED full-corpus counts. Files owned and written:

- `watch/inbox/operator_model/OPERATOR_MODEL_V2_BASE.md` — the V2 doc, labeled
  **SELF-MODEL selection-bias-corrected**; every claim carries (count, denominator, method)
  or is deleted / marked FRAME-NOT-FINDING.
- `watch/inbox/last_mile_20260930/imp10_operator_counts.py` — reproducer (zero API spend).
- `imp10_operator_pool.jsonl` / `imp10_operator_counts.json` / `imp10_audit_sample.json` —
  byte-backing (this directory).

## What was counted (instrument, moment 2026-09-30 ~12:40 EDT, local bytes)

- grok pool 852 session files → 845 sessions yielded **889** operator messages
  (2,003 tagged boilerplate + 2 continuation blobs dropped, rules stated in script).
- codex pool 193 rollout files → 170 files → **1,015** messages (358 tagged envelopes,
  64 md-context, 15 tiny dropped).
- **M = 1,904** raw operator-side messages; **1,231 unique texts** (673 duplicate rows; one
  fleet template sent 591x); **tone pool = 532** unique texts <=1,000 chars
  (length cap justified: uncapped P∧A∧C cell = 90 rows of median 80,905 chars = paste
  artifact, NACHO MASK blobs). Date range 2026-08-04 → 2026-09-09.

## Heuristic + error bars (stated, audited)

Keyword flags P/A/C (exact regexes in script header + V2 doc §2). Manual stratified audit
(seeded random.Random(20260930), author-read): A precision 3/9 [12%, 65%]; C precision 5/15
[15%, 58%]; P precision 12/15 [55%, 93%] (audit also caught 51 auto-injected codex envelopes
that were then excluded — the filter bug the audit existed to catch); loose-word probe bounds
approval false negatives (+6 rows ceiling). Wilson 95% CIs throughout.

## What survived / died (headline)

SURVIVED: profane-correction register (P∧C 6/532 = 1.1%; genuine profanity ≈6.3%, ~2/3
failure-directed); ALL-CAPS=correction (7/532 = 1.3%); approval register real but rare
(strict 3/532 = 0.56%, ceiling 1.7%); 20 laws + 4,968 presence rows byte-verified.
DIED: "challenging is the affection" → FRAME-NOT-FINDING (affection-in-challenge co-occurrence
2/532 = 0.38%, both banter; modal message = neutral dispatch 82.9%); "HIGH loyalty" → no
instrument; AGREEABLENESS rating deleted. N1's sampling charge quantified: OCEAN's
agreeableness section = 8 quotes = 1.5% of interactive pool / 0.16% of the presence
instrument. Other OCEAN axes demoted QUALITATIVE-UNREBASED.

## Cross-lane note

Pools end 09-09; OCEAN quotes to 09-29 live in watch/inbox receipts (different instrument,
uncounted here — stated in V2 §1). No commit, no spend, no API calls.
