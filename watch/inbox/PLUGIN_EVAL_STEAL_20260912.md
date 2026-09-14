# CLAUDE CODE `plugin eval` — the steal + the cost math (2026-09-12, operator link)

THE POST (ClaudeDevs, 09-11): `claude plugin eval` — draft test cases from real prompts,
score your plugin's runs, **then run each case again WITHOUT the plugin to see the difference.**
Pilot with `--runs 1` quotes the full-run cost before you fire. HTML report, private artifact.
Evals call the model → tokens.

## THE NEAT PART (name it precisely)

Anthropic shipped the fleet's own eval doctrine as a product feature:
- **paired with/without arms** = the null-generation control the dozen-wide fold demanded for
  falsifier 2 (L05: "replace with paired null-generation controls so the falsifier can die");
- **blind paired scoring** = the Astra-vs-cheap protocol we ran TONIGHT (same pack, shuffled
  arms, sealed key);
- **pilot-first cost preview** = the fuel_feed/lite_guard pacing discipline (meter before fire);
- **fixed case suite** = the zoo tier map's falsifier (each row beats the default on a 40-task
  suite or dies) and W7's honest-tier-list spec (pre-registered suite, n≥40, published logs).

Third mainstreaming receipt in a week: codex-router (seat decoupled from weights) → honest
cache-tier lists (W7) → eval-with-null-control. The organ-table doctrine is becoming product
category. That's the thesis rendering again.

## COST TO US (tri-state)

- **The feature itself: $0** — ships with `claude update`; hermes bundles claude.cmd, so the
  harness is already on disk.
- **Their tokens: UNPROVEN plan, gated anyway.** What plan the hermes-bundled claude rides is
  not on record — CHECK before any run (quota is money: the 09-05 promo lesson). The tool
  self-prices: pilot 1 run, it quotes the full suite. Our rule: no full run on Anthropic
  tokens without that quote in the receipt first. Rough scale if we did: N cases × 2 arms ×
  R runs × ~10-50K tok/case on Sonnet/Opus class = single-digit dollars per small suite,
  more on Opus.
- **Our lanes: pennies.** Tonight's 12-wide burned ~65K completion tokens for ~$0.002. A full
  organ eval (40 tasks × 2 arms × ~2K tok ≈ 160K tok) ≈ $0.01-0.05 on Lite/deepseek, $0 on
  the zoo's :free rows. 10-100x cheaper than the same suite on frontier tokens.

## THE DOGFOOD ANSWER: YES — WE BUILT EVERY PIECE ALREADY

`mag/organ_eval.py` v0 spec (the fleet's version of plugin eval, at fleet prices):
1. **Suite**: fixed 40-task set per organ class (the zoo falsifier's suite — same one powers
   both, no new build).
2. **Paired arms**: each task runs with-organ and without-organ (organ table row toggled) —
   the null control, product-shaped.
3. **Blind shuffle**: outputs anonymized A/B before scoring (tonight's blind/ pattern; the
   judge doesn't know which arm produced which).
4. **Judge tiering**: flash lanes score bulk cases; opus-5-class zoo rows only for
   seal-grade cases (metered, $220 budget, receipted).
5. **Fan-out**: 4-wide Lite lane like tonight (~55s/lane) — full eval in minutes, pennies.
6. **Cost preview**: computed from OUR receipt ledger before the full run (we know lane
   prices from fuel_feed; the M12 meter counts operator minutes too — their tool doesn't).
7. **Receipts**: every run appends usage JSONL (honest_cache_meter v0 fields — timestamp,
   provider, model, tokens, cache) — publishable per W7.

Falsifier for the organ (in our own grammar): a plugin/organ that can't show a with/without
delta on the fixed suite gets DEMOTED in the organ table — rightsizing for organs, not just
models. That closes the loop with tonight's zoo census: models rightsize per task class,
organs rightsize per measured delta.

## NEXT (standing order, $0)

1. Check what plan hermes' claude.cmd rides (names only) — UNPROVEN until read.
2. Run one REAL pilot their way if the plan is quota-cheap: their tool on one of our skills
   (e.g. riddled or librarian), --runs 1, keep the quote as the comparative price receipt.
3. Build organ_eval v0 (spec above, ~150 lines over lane_runner + fuel_feed primitives).
4. The 40-task suite gets drafted once, shared by zoo rows AND organ rows — one instrument,
   two censuses.
