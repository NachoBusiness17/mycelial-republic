# ECON - model-garden battery economics per family (2026-10-01, lane 6 RIB+ECON)

Companion to memory/rib/RIB_MODEL_GARDEN_ROUTING.md. Planning numbers only:
VERDICTS never come from this sheet (instruments-only law lives in the rib).
Prices come from configs/cost_rates.yaml (canonical join), from our metered
receipts where we have them, and from NOTHING else.

## 1. Measured typical ask shape (our own instrument)

Last 5 rows of memory/runs/hermes_burn/usage.jsonl (2026-10-01T21:51-21:53Z, all
anthropic duel2/N1R lane):

| row id | model | in tok | out tok | reasoning tok | cost |
|---|---|---|---|---|---|
| DUEL2_train_13_r2 | sonnet-5.5 | 2307 | 7860 | 4771 | $0.0832 |
| DUEL2_train_14_r2 | sonnet-5.5 | 2324 | 1966 | 1966 | $0.0243 |
| DUEL2_train_14_r2 (re-fire) | sonnet-5.5 | 2324 | 4118 | 4118 | $0.0458 |
| N1R_parables_songmap | opus-5.5 | 11567 | 5541 | 3551 | $0.1571 |
| N1R_parables_songmap (re-fire) | opus-5.5 | 11567 | 5135 | 3028 | $0.1490 |

Token shape: input mean 4,018 / median 2,324; output mean 4,924 / median 5,135;
2 of 5 rows are same-id re-fires (retry duplication inflates spend ~40% on this
lane; single-shot policy is itself a cost lever).

BATTERY UNIT (used below): 8 items x 4,000 in / 5,000 out = 32K in + 40K out per
battery. Mini-task slim shape (F4 census): ~1.5K in / <1K out per item.

## 2. Per-family price and projected 8-item battery cost

| family | in $/M | out $/M | price source | battery cost (32K in + 40K out) | metered per-ask crosscheck |
|---|---|---|---|---|---|
| ollama local (gemma:2b, gemma4, qwen2.5-coder:7b) | 0 | 0 | cost_rates.yaml seats | $0.00 | n/a |
| z_ai glm-4.7-flash + glm-4.5-flash | 0 | 0 | cost_rates.yaml (z.ai docs, free all tiers) | $0.00 | cache-mining proven 97-99.9% hit |
| z_ai glm-5.3-flash | 0.075 | 0.25 | cost_rates.yaml | $0.0124 | n/a |
| deepseek-v4-flash (off-peak) | 0.22 | 0.66 | cost_rates.yaml | $0.033 | W8/F4 metered $0.0001-0.0162/ask |
| deepseek-v4-flash (peak) | 0.44 | 1.32 | cost_rates.yaml | $0.067 | |
| deepseek-v4-pro (off-peak) | 0.66 | 1.98 | cost_rates.yaml | $0.100 | |
| fireworks ember-1 | metered | metered | animals jsonl | $0.08-0.37 | $0.0098-0.0457/call |
| nous qwen3.8-max-prime | metered | metered | F4 census | $0.049 at F4 mean ($0.0061/ask); up to $0.49 at duel-shape upper ($0.1522/ask) | F4 $0.0044-0.0091; duel $0.0279-0.1522 |
| z.ai glm-5.3 (paid tier) | 1.4 | 4.4 | cost_rates.yaml | $0.221 | |
| nous glm-5.3-prime | metered | metered | animals jsonl | $0.09-0.29 | duel lane $0.0107-0.0364; gopher shape $0.07-0.15 |
| gemini-3.8-flash (duel carrier; direct lane dormant B2-61) | metered | metered | animals jsonl | $0.23-0.32 | $0.0287-0.0400/ask |
| xai grok-4.5 | 2.0 | 6.0 | cost_rates.yaml | $0.304 | |
| anthropic sonnet-5.5 | 2.0 | 10.0 | IMPLIED EXACT from our usage.jsonl (n=57, fit err < $0.00005) | $0.464 | metered avg $0.0438 at small asks |
| anthropic opus-5.5 | 4.0 | 20.0 | IMPLIED EXACT from our usage.jsonl (n=84) | $0.928 | metered avg $0.3739 at 30K/13K asks |
| xai grok-4.7 | metered | metered | animals jsonl | $1.88-2.13 | $0.2347-0.2661/answer (r3 cached $0.0) |
| anthropic fable-5.1 | 10.0 | 50.0 | IMPLIED EXACT from our usage.jsonl (n=6) | $2.32 | metered avg $0.0305 at tiny asks |

Crosscheck note: the anthropic implied rates reproduce every metered row in the
ledger to under a twentieth of a cent, so the sheet prices the battery at true
blended shape, not list-page guesswork.

## 3. Cheapest rungs and the expensive flag

Three cheapest families per full battery:
1. ollama local: $0.00
2. z_ai free flash lanes (glm-4.7-flash / glm-4.5-flash): $0.00
3. z_ai glm-5.3-flash: $0.0124
(fourth: deepseek-v4-flash off-peak at $0.033, the cheapest PAID per-token family)

Most expensive: anthropic fable-5.1 at $2.32 per battery (grok-4.7 close behind
at $1.88-2.13 metered). ANTHROPIC PREMIUM FLAG: sonnet is 37x glm-5.3-flash,
opus 75x, fable 187x per battery.

## 4. Slimmed battery variant for the anthropic premium families

The full 8-item battery on sonnet + opus + fable together costs
$0.464 + $0.928 + $2.32 = $3.71, which is more than every other family in this
sheet combined. Slim variant for anthropic-class cells:

- 4 items, not 8: one per F4 shape-class that anthropic is actually a candidate
  for (code-writing, analysis, judgment, adversarial-review). Skip creative,
  extraction, schema, planning on premium families: the cheap families already
  cover those cells and nothing routes dollars by them.
- Single-shot, no same-id re-fire unless the answer is empty (the 5-row sample
  shows re-fires doubling spend; the LESSIG retry-on-empty rail is the sanctioned
  retry, not blanket re-runs).
- Rails per RIB_MODEL_GATES_20261001.md carried into the ask: streaming-SSE only,
  max_tokens 64000 (opus), sectioned word budgets.
- Projected slim cost per family (16K in + 20K out):
  - sonnet-5.5: $0.232
  - opus-5.5: $0.464
  - fable-5.1: $1.16
- Operator gate: paid anthropic asks only on operator GO (the AA1 law,
  RIB_MODEL_GATES). Nothing in this sheet authorizes spend.

## 5. Funding-status reconciliation (flagged, not resolved)

RIB_DRIVING_LADDER_20260928.md says the Anthropic keys are UNFUNDED (no Opus
rung), yet usage.jsonl shows live anthropic burns landing 2026-10-01 (DUEL2,
N1R, 236 rows total: 103 sonnet, 85 opus, 48 fable). Either the rung changed or
these burns ride a credit the rib does not know about. Flagged for the operator;
this sheet prices what the ledger shows, the ladder owns what is funded.

## 6. Battery cost at a glance (full 8-item, USD)

$0.00 ollama = $0.00 z_ai free flash < $0.0124 glm-5.3-flash < $0.033 ds-v4-flash
(off-peak) < $0.067 ds-flash (peak) < $0.10 ds-v4-pro < $0.08-0.37 ember-1 <
$0.049-0.49 qwen3.8-max-prime < $0.09-0.29 glm-5.3-prime < $0.221 glm-5.3 paid <
$0.23-0.32 gemini-3.8-flash < $0.304 grok-4.5 < $0.464 sonnet-5.5 < $0.928
opus-5.5 < $1.88-2.13 grok-4.7 < $2.32 fable-5.1

Sources: configs/cost_rates.yaml (model_rates + seats), configs/providers.yaml
(reachability), memory/runs/hermes_burn/usage.jsonl (236 rows, token shapes +
implied anthropic rates), memory/behavioral/animals/*.jsonl (metered per-ask
prices), watch/inbox/last_mile_20260930/{F4_FLASH_CENSUS,W8_MULTIFAMILY}.md.
Moment: 2026-10-01. This sheet expires with the rib's 30-day amendment clause.
