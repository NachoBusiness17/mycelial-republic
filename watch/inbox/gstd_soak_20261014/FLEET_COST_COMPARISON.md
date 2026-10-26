# FLEET COST COMPARISON - owned watts vs rented tokens

Closes falsifier-index rows 67 and 84 (fleet cost comparison). Thesis 67 (falsifier-index/THESES.md:155-156): "three machines you own beat any quota you rent, because ownership compounds and rent resets at the next terms update." Thesis 84 (falsifier-index/THESES.md:196-197): "the church's hell is moderated by night workers paid in pennies and volunteers paid in badges; our janitors are two small models paid in watts."

Measurement date: 2026-10-15. All data is estate-local; no paid API calls were made. Sources: the last 5 run receipts under watch/inbox/gstd_perimeter_build_20261010/runs/ and one web-verified posted price (source URLs at the bottom).

## 1. What the receipts actually carry (byte-truth first)

The run receipts carry NO duration field and NO token counts. summary.json in each run dir reports tasks, models, consensus rates, and verdict; receipt.jsonl carries per-task answers with no timestamps. The instruction that the summaries "carry durations" is FALSE in byte-truth and is struck here.

Wall-time was therefore DERIVED, not read: each run dir name is the run start timestamp (UTC), and summary.json's mtime is the run end. The pair is sequential (run 20261015T223909Z's derived end time 22:39:57Z equals the next run dir's start name exactly), which cross-checks the method.

## 2. Measured wall-time, last 5 runs (battery: gemma:2b, deepseek-r1:1.5b, qwen2.5:3b-instruct, gemma2:2b-instruct-q5_K_M, qwen-desk:latest or qwen2.5:7b)

| run dir | tasks | verdict | derived wall-time | energy at 300W | energy cost at $0.24/kWh |
|---|---|---|---|---|---|
| runs/20261013T215230Z | 13 | STRUCTURE | 90 s | 0.0075 kWh | $0.0018 |
| runs/20261014T120012Z | 13 | STRUCTURE | 86 s | 0.0072 kWh | $0.0017 |
| runs/20261015T120006Z | 13 | STRUCTURE | 83 s | 0.0069 kWh | $0.0017 |
| runs/20261015T223909Z | 6 | STRUCTURE | 48 s | 0.0040 kWh | $0.0010 |
| runs/20261015T223957Z | 6 | STRUCTURE (1 model_error retried in-band) | 505 s | 0.0421 kWh | $0.0101 |
| TOTAL (5 certified runs) | 51 | 5/5 certified | 812 s = 13 m 32 s | 0.0677 kWh | $0.0162 |

Canonical 13-task battery run: 83-90 s, ~$0.0017 of electricity per certified run. Fleet average including the 505 s dispute outlier: $0.0032 per run.

## 3. Token volume (estimated, no meters exist)

Method: receipt.jsonl in each run shows exactly 5 model answers per task (one per battery model). Each answer in the receipts is 5-40 words of short QA; deepseek-r1 adds short chain-of-thought. Estimate per model-task: 100 prompt tokens + 100 completion tokens = 200 tokens. Stated as an ESTIMATE, not a measurement; a 2x error here moves the rented column 2x, not the owned column.

- 51 tasks x 5 models = 255 model-tasks x 200 tokens = 51,000 tokens (25,500 in / 25,500 out).
- Canonical 13-task run: 13,000 tokens (6,500 in / 6,500 out).

## 4. Rented equivalent (real posted prices)

| lane | posted price per 1M tokens (in / out) | cost, 5-run batch (51k tok) | cost per canonical 13-task run |
|---|---|---|---|
| GLM-4.6 via OpenRouter | $0.43 / $1.75 (web-verified 2026-10-15, source below) | $0.0110 in + $0.0446 out = $0.0556 | $0.0028 in + $0.0114 out = $0.0142 |
| GPT-4o-mini (OpenAI posted pricing) | $0.15 / $0.60 | $0.0038 in + $0.0153 out = $0.0191 | $0.0010 in + $0.0039 out = $0.0049 |

## 5. Named assumptions (every one)

1. 300 W total-system draw (desktop + GPU under LLM inference, 250-400 W band midpoint). ASSUMPTION; no watt meter on the estate.
2. $0.24/kWh, NY residential rate. ASSUMPTION.
3. Wall-time = run dir start timestamp to summary.json mtime. Derived; sequential-scheduling cross-check holds on 2026-10-15 (48 s gap matches the 48 s derived duration).
4. 200 tokens per model-task (100 in / 100 out). ESTIMATE; receipts carry no token meters. Deepseek-r1 reasoning tails could push this 2-3x.
5. Owned hardware is sunk capex (three machines already bought); watts are the only marginal cost. Capex amortization deliberately EXCLUDED from the per-run number; thesis 67 is about the margin, not the purchase.
6. The 505 s outlier run is included, not dropped; dropping it would flatter the owned column and the falsifier index does not take flattery.
7. Rented comparison assumes a mini-class paid API could match the battery's consensus format at one call per model-task (5 calls per task); a single frontier-model call doing all 5 roles would cut rented tokens 5x but changes the epistemics (one judge, no council), which theses 68/84 explicitly reject.
8. Rates: NY residential, no solar offset, machine otherwise idle-watts attributed to the runs (idle baseline inside the 300 W assumption).

## 6. Verdict row (feeds theses 67/84 kill conditions)

| metric | OWNED (battery on local GPUs) | RENTED GLM-4.6 | RENTED GPT-4o-mini |
|---|---|---|---|
| cost per certified 13-task run | $0.0017 | $0.0142 (8.4x owned) | $0.0049 (2.9x owned) |
| cost per run, fleet avg incl. outlier | $0.0032 | - | - |
| 5-run certified batch | $0.0162 | $0.0556 | $0.0191 |
| annualized at 1 battery run/day | ~$0.62/yr | ~$5.18/yr | ~$1.78/yr |
| quota behavior | none observed: 47 run dirs 2026-10-10 to 2026-10-15, zero quota/rate-limit failures, one model_error retried in-band | rate limits + terms reset each cycle | rate limits + terms reset each cycle |

VERDICT: theses 67 and 84 HOLD directionally and are graded LIVE at the margin: the owned janitors run a certified consensus battery for $0.0017/run, 2.9x to 8.4x cheaper than the same token volume on real posted mini-class or GLM pricing, with zero quota resets across the observed archive, which is the "rent resets, ownership compounds" leg in evidence. HONEST CAVEAT, stated because the index does not take homilies: at the current measured cadence the absolute stakes are pennies per year either way ($0.62 vs $1.78-5.18 annualized); the thesis's cost leg is a ratio win and an availability win, not a dollar windfall at n=1/day. If the cadence compounds (the battery already runs ~8 runs/day across the soak archive), the ratio holds and the dollars scale with it; if the cadence never grows, thesis 67 survives on the quota-reset leg alone, not on savings. Thesis 84's "paid in watts" is byte-true: $0.0017 of electricity is the entire marginal wage of a certified run.

## Sources

- Run receipts: watch/inbox/gstd_perimeter_build_20261010/runs/20261013T215230Z/summary.json, runs/20261014T120012Z/summary.json, runs/20261015T120006Z/summary.json, runs/20261015T223909Z/summary.json, runs/20261015T223957Z/summary.json and sibling receipt.jsonl files (mtimes read 2026-10-15 for wall-time derivation).
- Theses: falsifier-index/THESES.md:155-156 (row 67), falsifier-index/THESES.md:196-197 (row 84).
- GLM-4.6 posted pricing: https://openrouter.ai/z-ai/glm-4.6 ($0.43 in / $1.75 out per 1M tokens, web-verified 2026-10-15).
- GPT-4o-mini posted pricing: https://openai.com/api/pricing/ ($0.15 in / $0.60 out per 1M tokens, posted rate).
