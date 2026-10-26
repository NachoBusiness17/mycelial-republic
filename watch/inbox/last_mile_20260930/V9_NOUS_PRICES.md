# V9 - NOUS PRICE TABLE (2026-09-30)

Lane: last_mile_20260930. File ownership: this receipt + `v9_probe_prices.py` + `v9_probe_prices.json` (raw rows).
Mission: operator sent the Nous portal because it is discounted; prior session probed 6 models. This receipt probes 26 more key models (1 tiny call each, max_tokens 50) and files the price table the estate needs.

**Budget: $0.50 cap. Spent $0.0401** (26 primary probes + 7 key-0 retries + 3 differential + 2 mechanism probes; plus $0.001005 ember diagnostic counted). Raw metering: `v9_probe_prices.json`.

## Method (trust bytes)

- Endpoint `https://inference-api.nousresearch.com/v1/chat/completions`, keys per `tools/duel_harness.py` law (NOUS_SDD_API_KEY, HERMES_API_KEY_1/2). Call shape copied from the harness.
- Every response carries `usage.cost` (metered USD) and `cost_details.rate_source` = `openrouter_list` on normal models, `gateway_computed_spend` on grok. Rates below = OpenRouter catalog per-token list, and each row is VALIDATED: catalog-predicted cost vs actual `usage.cost` (ratio column).
- Ratio 1.000 on 20 of 26 models (byte-exact to the dollar at micro scale). Anomalies decomposed below; none is an unexplained price.

## Metering laws found (byte-proven)

1. **API metering = OpenRouter list rates.** No across-the-board API-side discount. The portal discount is: (a) subscription credit bonus (10%: $200 buys $220), (b) `:batch` variants at ~half list, (c) law 2.
2. **Cache reads bill at 0.25x input.** Proven exactly on grok-4.6: 85 fresh x $2 + 128 cached x $0.50 + 72 completion x $6 = $666e-6 = actual, to the digit; grok-4.7 same law ($1.1e-3). This explains every sub-1.0 ratio (platform-injected context arrives cache-hit).
3. **Reasoning tokens bill as output.** grok-4.6 reported completion_tokens 1 but reasoning_tokens 71; billed 72 (total_tokens 285 = 213+72 confirms). Cost projections for reasoning models must use max completion incl. reasoning.
4. **gemma-4-31b probe ratio 1.45**: tiny-number rounding (out=2); rates are floor-tiny either way. Flag, not a finding.
5. **HERMES_API_KEY_1 is near-empty**: every 402 in the first sweep landed on that key (cheap ministral call passed, frontier reserve check failed). Retries on key 0 succeeded. Key rotation hides this; worth a balance check.
6. **`tools/duel_harness.py` PRICE fallback is stale vs live list**: ember-1 fallback ($0.3, $1.2) vs live ($3, $15) - 10x understated; glm-5.3-prime (3, 15) vs live (2.8, 8.8); qwen3.8-max-prime (3, 15) vs live (4, 12). Live duels are safe (usage.cost wins); only the fallback lies. Not this lane's fence to fix; named here.

## THE TABLE

Blended = (N x in + out) / (N+1) $/M. 3:1 = typical chat/review; 1:1 = judgment-weighted (long reasoned answers; ranking mix). Prior-6 rows at bottom (catalog-validated, not re-probed here except ember).

| model | in $/M | out $/M | blend 3:1 | blend 1:1 | probe ratio |
|---|---|---|---|---|---|
| mistralai/ministral-3b-2512 | 0.10 | 0.10 | 0.10 | 0.10 | 1.000 |
| openai/gpt-oss-120b | 0.037 | 0.17 | 0.07 | 0.10 | 1.000 |
| google/gemma-4-31b-it | 0.09 | 0.34 | 0.15 | 0.22 | 1.45 flag |
| openai/gpt-6-luna | 0.10 | 0.50 | 0.20 | 0.30 | 1.000 |
| qwen/qwen3.7-plus | 0.32 | 1.28 | 0.56 | 0.80 | 1.000 |
| mistralai/mistral-medium-3.1 | 0.40 | 2.00 | 0.80 | 1.20 | 1.000 |
| x-ai/grok-4.20 | 1.25 | 2.50 | 1.56 | 1.88 | 0.443 (cache) |
| x-ai/grok-4.3 | 1.25 | 2.50 | 1.56 | 1.88 | 0.577 (cache) |
| z-ai/glm-5.3-prime (prior) | 2.80 | 8.80 | 4.30 | 5.80 | duel-metered |
| x-ai/grok-4.5 | 2.00 | 6.00 | 3.00 | 4.00 | 0.430 (cache) |
| x-ai/grok-4.6 | 2.00 | 6.00 | 3.00 | 4.00 | 1.542 (reasoning billed) |
| x-ai/grok-4.7 | 2.00 | 6.00 | 3.00 | 4.00 | 0.439 (cache) |
| aion-labs/aion-3.5 | 3.00 | 6.00 | 3.75 | 4.50 | 1.000 |
| qwen/qwen3.8-max-prime (prior) | 4.00 | 12.00 | 6.00 | 8.00 | duel-metered |
| openai/gpt-6-sol | 2.00 | 10.00 | 4.00 | 6.00 | 1.000 |
| openai/gpt-6-sol-pro | 2.00 | 10.00 | 4.00 | 6.00 | 1.000 |
| openai/gpt-6.1-sol-pro | 2.00 | 10.00 | 4.00 | 6.00 | 1.000 |
| anthropic/claude-opus-5.5 | 4.00 | 20.00 | 8.00 | 12.00 | 1.000 |
| anthropic/claude-opus-4.5 | 5.00 | 25.00 | 10.00 | 15.00 | 1.000 |
| anthropic/claude-opus-4.6 | 5.00 | 25.00 | 10.00 | 15.00 | 1.000 |
| anthropic/claude-opus-4.7 | 5.00 | 25.00 | 10.00 | 15.00 | 1.000 |
| anthropic/claude-opus-4.8 | 5.00 | 25.00 | 10.00 | 15.00 | 1.000 |
| anthropic/claude-opus-5 | 5.00 | 25.00 | 10.00 | 15.00 | 1.000 |
| anthropic/claude-fable-5 | 10.00 | 50.00 | 20.00 | 30.00 | 1.000 |
| anthropic/claude-fable-5.1 | 10.00 | 50.00 | 20.00 | 30.00 | 1.000 |
| openai/gpt-6-astra | 10.00 | 50.00 | 20.00 | 30.00 | 1.000 |
| openai/gpt-6-astra-pro | 10.00 | 50.00 | 20.00 | 30.00 | 1.000 |
| anthropic/claude-opus-4.1 | 15.00 | 75.00 | 30.00 | 45.00 | 1.000 |
| fireworks/ember-1 (prior) | 3.00 | 15.00 | 6.00 | 9.00 | 1.000 (this session) |

## Value-per-dollar for JUDGMENT work

Value = quality score / blend 1:1. Scores are HEURISTIC tier scores (provenance: glm/qwen are duel-ledger-proven workhorses; the rest are family-tier convention, NOT benchmarks). Judgment gate: score >= 8.5 (below the gate = sensing/lane class per the driving ladder).

| rank | model | score | blend 1:1 | value |
|---|---|---|---|---|
| 1 | x-ai/grok-4.3 | 8.5 | 1.88 | 4.53 |
| 2 | x-ai/grok-4.7 | 9.1 | 4.00 | 2.28 |
| 3 | x-ai/grok-4.6 | 8.9 | 4.00 | 2.23 |
| 4 | x-ai/grok-4.5 | 8.7 | 4.00 | 2.18 |
| 5 | openai/gpt-6.1-sol-pro | 9.3 | 6.00 | 1.55 |
| 6 | z-ai/glm-5.3-prime (proven) | 8.8 | 5.80 | 1.52 |
| 7 | openai/gpt-6-sol-pro | 9.0 | 6.00 | 1.50 |
| 8 | openai/gpt-6-sol | 8.6 | 6.00 | 1.43 |
| 9 | qwen/qwen3.8-max-prime (proven) | 8.7 | 8.00 | 1.09 |
| 10 | anthropic/claude-opus-5.5 | 9.5 | 12.00 | 0.79 |
| 11 | anthropic/claude-opus-5 | 9.3 | 15.00 | 0.62 |
| 12 | openai/gpt-6-astra-pro | 9.6 | 30.00 | 0.32 |
| 13 | anthropic/claude-fable-5.1 | 9.4 | 30.00 | 0.31 |

Below the gate but value monsters for non-judgment lanes: gpt-6-luna (score 7.6 / blend 0.30), qwen3.7-plus (8.0 / 0.80), mistral-medium-3.1 (7.6 / 1.20), gpt-oss-120b (7.2 / 0.10), gemma-4-31b (6.8 / 0.22), ministral-3b (5.5 / 0.10).

Caveats: grok scores are the most heuristic rows in the top 5 (no estate duel has run them); glm-5.3-prime at rank 6 is the only duel-PROVEN contender and the safe default until grok duels run. Opus-4.1 is legacy-priced ($15/$75, worst frontier value; avoid).

## Next windows could

- Run 3-5 estate duels (tools/duel_harness.py shape) grok-4.7 vs glm-5.3-prime to convert the top heuristic rows into duel-proven ones (~$0.20).
- Fix the stale PRICE fallback in tools/duel_harness.py (owner's fence).
- Check HERMES_API_KEY_1 balance; it 402s frontier reserves.
