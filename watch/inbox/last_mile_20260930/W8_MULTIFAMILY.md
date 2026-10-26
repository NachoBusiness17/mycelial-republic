# W8 - MULTI-FAMILY DUEL SERIES (12 duels, 4 families, 3 shapes) - 2026-09-30

Mission (operator): V1 tried 4 families on ONE ask; W8 is the series. 12
duels across glm-prime (content from this account), grok-4.3, deepseek-v4.1-flash,
qwen3.7-flash on 3 task shapes (4 adversarial-review, 4 schema-design, 4
planning), ember judging all BLIND. Question: does any family dominate
quality-per-dollar, or is it parity everywhere (like glm/qwen at n=30)?
Budget $3.00. File ownership: this receipt + rows in logs/duel/duels.jsonl
+ w8_series_duel.py + w8_run_20260930.log + w8_glm_{adv,schema,plan}.md +
w8_contenders_20260930.jsonl.

## V1 history corrected

V1 never landed a row: grok-4.7 timed out twice at the harness 300s socket
(zero spend, clean abort) and the patched relaunch never ran
(logs/duel/duels.jsonl held zero v1mf rows; v1_run_20260930.log). W8 is the
first multi-family data in the ledger.

## Design

Per shape ONE identical ask goes to all 4 families. The 4 duels per shape
are the cycle pairs glm-grok, grok-ds, ds-qwen, qwen-glm: every family
appears twice per shape (once logical A, once logical B) and every pairing
meets once per shape. Consequence: glm-vs-ds and grok-vs-qwen NEVER meet
(cycle blind spot, disclosed). Asks are estate-real: adversarial review of
the full tools/duel_harness.py source embedded in the ask; router-family
JSON Schema design from the real duels.jsonl row shape; router wiring plan
citing the real ledger, V9 price receipt, and harness. Rubrics per shape
(4 criteria each). Judge: fireworks/ember-1, blind (A/B only), swap
alternated by ledger parity, per-criterion scores banked. Answers are
reused across the 4 duels of a shape, so within-shape variance is judge
sampling, not answer sampling.

## Contender provenance and configuration (fairness disclosures)

- glm-prime: authored by THIS ACCOUNT's session model (GLM-5.3) from the
  ask text alone, before any contender fired, banked at cost 0.0. Not a
  Nous call. Catalog-equivalent cost would be roughly $0.02-0.04 per
  answer (lw9 live glm metering $0.0167-0.0364; V9 rates 2.8/8.8).
- grok-4.3: standard harness call (reasoning cap 6000, 16000 tokens).
- qwen3.7-flash: rejects the reasoning param (HTTP 400), so it fires
  without it (verified live before the run).
- deepseek-v4.1-flash: thinking-on DNFs. On schema and plan asks it burned
  the ENTIRE completion budget on hidden reasoning and returned ZERO
  content at 4500 and 8000 total-token caps, with and without the
  reasoning param, and the full 16000 budget died twice on the 900s socket
  (w8_run_20260930.log + 4 manual diags, _ds_diag_schema_nothink.txt kept).
  Fix: reasoning {"enabled": false} -> 38s, 10704 chars, $0.0021. The adv
  answer (banked first) ran thinking-on at full budget and finished in 92s.
  Router law: ds on this gateway is thinking-off only for long-form asks.

## THE RESULT: NOT PARITY. A clean two-tier split, identical in all 3 shapes

| family | adv | schema | plan | total | per-answer cost (metered) |
|---|---|---|---|---|---|
| glm-prime | 2-0 | 2-0 | 2-0 | 6-0 | $0.00 this run (session; catalog ~$0.02-0.04) |
| ds-v4.1-flash | 2-0 | 2-0 | 2-0 | 6-0 | $0.0130 total (adv 0.0103, schema 0.0021, plan 0.0006) |
| grok-4.3 | 0-2 | 0-2 | 0-2 | 0-6 | $0.0290 total (0.0131 / 0.0107 / 0.0052) |
| qwen3.7-flash | 0-2 | 0-2 | 0-2 | 0-6 | $0.0028 total (0.0010 / 0.0010 / 0.0008) |

Every duel was decisive (0 ties, 0 UNPARSED, 4/4 criteria parsed in all 12
rows). A 6-0 record against common opponents is p=0.0156 one-sided (6 fair
coins); glm and ds each hold one, grok and qwen each wear one. Denominator
named: 12 rows in logs/duel/duels.jsonl read 2026-09-30 post-run, ids
w8-*. Judge rationales are consistent: grok and qwen answers drew
"invents defects", "fabricates statistics, files", "weak rollback, thin
test"; glm and ds drew "three real defects with exact evidence",
"concrete and grounded in stated files".

## Quality-per-dollar ranking

1. ds-v4.1-flash: 6-0 at $0.0130 total contender spend (avg $0.0043 per
   ask, and $0.0006 on plan once thinking-off). The value monster of the
   series, with the thinking-off constraint attached.
2. glm-prime: 6-0 at $0 marginal this run; at catalog rates it is the
   quality lane, not the cheap lane.
3. qwen3.7-flash: 0-6 but nearly free ($0.0028 total). Cheap is not
   quality: keep in the sensing tier per the driving ladder.
4. grok-4.3: 0-6 at $0.0290, the most expensive per answer. The V9
   "cheap judgment pick" heuristic row does NOT transfer to workhorse duty
   on these shapes; keep grok-4.3 for judgment-only lanes until re-proven.

The glm-vs-ds order is UNRESOLVED (cycle blind spot): both swept every
common opponent. ds is ~13x cheaper than glm's catalog equivalent, so ds
is the default cheap work lane unless a glm-vs-ds series flips it.

## Validity

- Blind judging: judge sees A/B only (duel_harness v1.1); identities
  logged in the row only. Swap alternated perfectly (6 T / 6 F).
- Slot-A wins 8 of 12 (one-sided p=0.194): within noise, and weaker than
  the V8 n=30 slot-A finding. Decisive point: the top tier won from BOTH
  slots (all four adv duels were slot-B wins by glm/ds; schema and plan
  were slot-A wins). The tier split cannot be a slot artifact.
- Answer reuse within shape (disclosed above); single judge family
  (ember); 3 asks total; temperature 0.4 throughout.
- Zero em-dashes in all 12 rows (byte check chr(0x2014)/chr(0x2013)) and
  in every file this lane wrote.

## Cost accounting (all metered unless marked)

- 12 judge calls: $0.2308 (ledger sum).
- 9 contender fires + the reused ds schema diag: $0.0548.
- Key probes (3 runs) + manual probes + 4 diagnostic fires: ~$0.0183.
- Worst-case estimate for the two unmetered 900s ds timeout generations
  and the two empty-content attempts: ~$0.025 (no response body, so no
  meter; bounded at full-budget token counts).
- TOTAL ~$0.33 against the $3.00 cap. Two clean aborts and one probe-fix
  restart spent nothing but time; the cache + banked-id skip law made all
  resumes free of re-payment.

## Router rows (the feed this mission exists for)

- ds-v4.1-flash: WORK lane, thinking-off mandatory, schema 2-0, plan 2-0,
  adv 2-0 (adv was thinking-on), ~$0.0006-0.0103 per answer.
- glm-prime: QUALITY lane, 6-0 here plus the n=30 glm/qwen parity record.
- grok-4.3: JUDGMENT lane only (V9 role); 0-6 as a worker.
- qwen3.7-flash: SENSING tier only; 0-6, cheapest per answer.

## Next windows could

- Fire the diagonal pairs glm-vs-ds and grok-vs-qwen (3 shapes x 1 pair,
  ~$0.10) to close the cycle blind spot and order the tiers internally.
- Fold these 12 rows into a real router_families.json (the schema and
  plan asks on this run are effectively its spec review).
- File the ds thinking-on DNF to Nous if reproducible elsewhere; it is a
  gateway/model defect worth reporting, not just routing around.
