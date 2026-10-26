# RIB_MODEL_GARDEN_ROUTING - the full-grid routing table (schema + seeded cells)

Minted 2026-10-01 by lane 6 (RIB+ECON) of the model-garden project. Extends the
estate routing doctrine to the FULL model grid. Prior art this rib stands on
(do not re-derive): RIB_DRIVING_LADDER_20260928.md (funding rungs + conditions
law), RIB_MODEL_GATES_20261001.md (per-animal harness profiles),
RIB_FREE_USAGE_POLICY_20260823.md (free = sensing), RIB_DEEPSEEK_SHOULDERS_20261001.md
(cheap seat multiplies the premium dollar), configs/providers.yaml (reachability),
configs/cost_rates.yaml (canonical USD/M join), watch/inbox/MODEL_MATRIX_20260923.md
(free-wall bake-off).

## THE GRID

Two axes: FAMILY (the animal) x CAPABILITY-COLUMN (the work-shape). One cell per
intersection. The 8-item battery is exactly one ask per capability-column, so a
fired battery fills one row per family.

## THE SCHEMA (7 fields, every cell is a row in this shape)

| field | meaning | legal values |
|---|---|---|
| family | the animal: model + carrier lane (Nous / xAI SD / z.ai key / local / stealth free). Fingerprint-scoped per Amendment 10: a model whose fingerprint changed is a NEW family, cold start, no inherited trust. | e.g. deepseek-v4.1-flash, grok-4.7, anthropic/claude-opus-5.5 |
| capability-column | which of the 8 work-shapes this verdict is about | the 8 columns below |
| verdict | tier word for that cell | WIN / LOSS / PARITY / CHAMPION / SENSING-ONLY / DNF / UNMEASURED |
| price-per-quality | USD per ask AS MEASURED AT THE VERDICT'S SHAPE (not list price) | metered number + shape note |
| condition | the rails that produced it: thinking mode, reasoning cap, transport (stream/SSE), max_tokens, budget, judge blindness, ask shape. MANDATORY: a verdict without its conditions is not a verdict (one-bug law, RIB_DRIVING_LADDER addendum 2026-09-29). | free text, must name instrument conditions |
| measured-by | the estate instrument + receipt file that produced the number | file path (never a vendor page) |
| moment | ISO date of the measurement. Rows EXPIRE (amendment clause below). | YYYY-MM-DD |

### The 8 capability-columns (battery items)

From the estate's own instruments, not invented here: F4's five census shapes
(watch/inbox/last_mile_20260930/F4_FLASH_CENSUS.md) + W8's three duel shapes
(watch/inbox/last_mile_20260930/W8_MULTIFAMILY.md) = 8.

1. code-writing
2. analysis
3. extraction (prose to strict JSON, auto-validated)
4. judgment (pick better of options with reasoning)
5. creative (bounded alternative generation)
6. adversarial-review
7. schema-design
8. planning

## THE LAWS

1. INSTRUMENTS ONLY. No cell fills from vendor claims, vendor benchmarks, or
   marketing pages. A cell fills only from estate instruments: logs/duel/duels.jsonl,
   census receipts (watch/inbox/last_mile_20260930/*), memory/runs/hermes_burn/usage.jsonl,
   memory/behavioral/animals/*.jsonl. Vendor list prices live in
   watch/inbox/model_garden/ECON.md as PLANNING inputs, clearly sourced, and never
   masquerade as verdicts. UNMEASURED is a legal, default state; the battery fills
   it. Hand-copying a vendor number into an empty cell is fabrication.
2. AMENDMENT / EXPIRY CLAUSE (the funded-rung staleness lesson). Every row carries
   its moment and EXPIRES: a row whose moment is more than 30 days old, or that
   spans a known family event (fingerprint change, carrier swap, deprecation,
   pricing-table change), is STALE and must be re-measured before it routes dollars.
   The driving ladder's DeepSeek rung rotted exactly this way when the Nous credits
   landed (RIB_DRIVING_LADDER_20260928.md addendum 2026-09-29: the funded rung it
   described was already superseded); routing rows rot identically. Amend, never
   rewrite: supersede a stale row by appending a new-moment row and keep the old
   row visible as lineage.
3. CONDITIONS ARE LOAD-BEARING (one-bug law). See the condition field. Example:
   deepseek-v4.1-flash's W8 wins are thinking-OFF wins; the same family thinking-on
   DNFs the same asks. Same animal, opposite verdicts, separated only by condition.
4. FUNDING IS A SEPARATE COLUMN OF TRUTH. Reachability (providers.yaml) and funding
   (RIB_DRIVING_LADDER) gate WHICH families the battery may fire; they never fill
   verdict cells. A family can be reachable, funded, and still UNMEASURED.

## SEEDED GRID (prior-verdict cells, all with citations; everything else UNMEASURED)

### deepseek-v4.1-flash (Nous carrier) - the only family with all 8 columns measured

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| code-writing | WIN 4-1 vs qwen3.8-max-prime | $0.0001/answer | mini-task shape, thinking-off, gemini blind judge | F4_FLASH_CENSUS.md | 2026-09-30 |
| analysis | LOSS 0-5 | $0.0002/answer | same | F4_FLASH_CENSUS.md | 2026-09-30 |
| extraction | PARITY 5T (0-0, 5 ties) | $0.0001/answer | strict JSON auto-validated | F4_FLASH_CENSUS.md | 2026-09-30 |
| judgment | LOSS 0-5 | $0.0000/answer | same | F4_FLASH_CENSUS.md | 2026-09-30 |
| creative | WIN 3-2 | $0.0001/answer | exactly-5-alternatives shape | F4_FLASH_CENSUS.md | 2026-09-30 |
| adversarial-review | WIN 2-0 | $0.0103/answer | W8 estate-real ask, thinking-off | W8_MULTIFAMILY.md | 2026-09-30 |
| schema-design | WIN 2-0 | $0.0021/answer | THINKING-OFF MANDATORY (thinking-on burns whole budget, zero content, socket deaths) | W8_MULTIFAMILY.md + RIB_MODEL_GATES_20261001.md | 2026-09-30 |
| planning | WIN 2-0 | $0.0006/answer | thinking-off | W8_MULTIFAMILY.md | 2026-09-30 |

Rail carried from RIB_MODEL_GATES_20261001.md: thinking-off mandatory; long-form
degradation, route long-form elsewhere. W8 quality-per-dollar rank 1 (6-0 at
$0.0130 total).

### z-ai/glm-5.3-prime (Nous carrier)

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| adversarial-review | WIN 2-0 | $0 marginal (session); catalog $0.02-0.04/ask | standard harness, session-authored content (disclose) | W8_MULTIFAMILY.md | 2026-09-30 |
| schema-design | WIN 2-0 | same | same | W8_MULTIFAMILY.md | 2026-09-30 |
| planning | WIN 2-0 | same | same | W8_MULTIFAMILY.md | 2026-09-30 |
| judgment (as judge) | CAVEAT: never sole judge on glm-authored text | $0.0107-0.0364/answer duel lane; gopher shape $0.07-0.15 | contamination: glm judging glm | RIB_MODEL_GATES_20261001.md + animals/z_ai_glm_5_3_prime.jsonl | 2026-09-30 |
| code-writing / analysis / extraction / creative | UNMEASURED | | | | |

Also AH10 2-0 vs deepseek while the thinking-on opponent degenerated
(animals/z_ai_glm_5_3_prime.jsonl, 2026-09-30). Duel-lane price $0.0107-0.0364/answer,
shape moves it 3-5x.

### qwen/qwen3.8-max-prime (Nous carrier)

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| analysis | WIN 5-0 | $0.0091/answer | F4 mini-task, reasoning capped 800, gemini blind judge | F4_FLASH_CENSUS.md | 2026-09-30 |
| judgment | WIN 5-0 | $0.0060/answer | same | F4_FLASH_CENSUS.md | 2026-09-30 |
| code-writing | LOSS 1-4 | $0.0052/answer | same | F4_FLASH_CENSUS.md | 2026-09-30 |
| extraction | PARITY 5T | $0.0044/answer | same | F4_FLASH_CENSUS.md | 2026-09-30 |
| creative | LOSS 2-3 | $0.0057/answer | same | F4_FLASH_CENSUS.md | 2026-09-30 |
| adversarial-review / schema-design / planning | UNMEASURED (W8 did not field max-prime) | | | | |

### grok-4.7 (xAI SD account, funded per driving ladder)

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| adversarial-review | CHAMPION 9-0, avg 4.92; SWEEP CONTAMINATION-SUSPECT (r1 answered a self-invented task, took 3/4 criteria) | $0.2347-0.2661/answer (r3 cached $0.0) | streaming transport (whole-response hangs 900s+); reserve for judgment | watch/inbox/last_mile_20260930/V1_MULTIFAMILY_DUEL.md + animals/grok_4_7.jsonl + RIB_MODEL_GATES_20261001.md | 2026-09-30 |
| other 7 columns | UNMEASURED | | | | |

### grok-4.3 (xAI) - a DIFFERENT animal, never confuse them

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| adversarial-review | LOSS 0-2 | $0.0131/answer | minimal-output mode (1295 chars, 0 headers) | W8_MULTIFAMILY.md + animals/x_ai_grok_4_3.jsonl | 2026-09-30 |
| schema-design | LOSS 0-2 | $0.0107/answer | schema type errors + fabricated empty-hash example | W8_MULTIFAMILY.md | 2026-09-30 |
| planning | LOSS 0-2 | $0.0052/answer | same run | W8_MULTIFAMILY.md | 2026-09-30 |
| other 5 columns | UNMEASURED | | | | |

### qwen3.7-flash - SENSING ONLY

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| adversarial-review / schema-design / planning | LOSS 0-2 each, SENSING-ONLY tier | $0.0008-0.001/answer | byte-cited fabrication (invented stats, nonexistent files), concurred by TWO judge families | W8_MULTIFAMILY.md + animals/qwen3_7_flash.jsonl | 2026-09-30 |
| other 5 columns | UNMEASURED | | | | |

### google/gemini-3.8-flash (duel carrier; direct lane dormant per providers.yaml B2-61 401)

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| format-fidelity | CHAMPION 6-3 V1 | $0.043/answer | balanced-value middle | RIB_MODEL_GATES_20261001.md | 2026-09-30 |
| blind-judge duty | PROVEN (F4 judge n=25+2, LW9) | $0.0287-0.0400/answer | RAIL: rejects reasoning {"enabled": false} with HTTP 400; send {"max_tokens": N} shape | F4_FLASH_CENSUS.md + animals/google_gemini_3_8_flash.jsonl | 2026-09-30 |
| judgment (as contender) | LOSS 0-3 vs glm-prime on HIDDEN ask-bank draws | $0.0287-0.0400/answer | D6 flip: plain-sight verdicts invert when asks are hidden | watch/inbox/last_mile_20260930/D6_ASKBANK_DUEL.md | 2026-09-30 |
| the 8 battery columns as contender | UNMEASURED | | | | |

### fireworks/ember-1 - judge family, never sole judge

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| blind-judge duty | PROVEN with BIAS DOSSIER: coverage-over-fidelity (scored an off-task answer 5/5), position-bias flip at n=1 | $0.0098-0.0457/call | never the only judge on verdicts that route dollars; second judge owed | RIB_MODEL_GATES_20261001.md (THE_LENSING kill-3) + animals/fireworks_ember_1.jsonl | 2026-09-30 |
| the 8 battery columns as contender | UNMEASURED | | | | |

### anthropic/claude-opus-5.5 (via Nous)

| capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|
| adversarial-review (verdict-class long asks) | PROVEN when railed | $0.42 per 26K-char verdict; $0.37 for an EMPTY 16k-cap answer; streaming a3 $0.69 | TRANSPORT streaming-SSE ONLY (whole-response dies 1800s/3600s, $0, zero bytes, 3 documented deaths); max_tokens 64000 (32k burns 29.5k on reasoning; 16k returns all-reasoning empty); paid asks on operator GO (AA1) | RIB_MODEL_GATES_20261001.md + animals/claude_opus_5_5.jsonl | 2026-09-30 |
| the 8 battery columns | UNMEASURED at battery shape | avg $0.3739/ask over 85 metered asks (avg 30084 in / 12679 out) | see conditions above | memory/runs/hermes_burn/usage.jsonl | 2026-10-01 |

### anthropic/claude-sonnet-5.5 and claude-fable-5.1 (via Nous duel lane)

No capability verdicts yet: UNMEASURED in all 8 columns. Prices implied EXACTLY
from our own receipts (fit error < $0.00005/row):
- sonnet-5.5: $2/M in, $10/M out (n=57 rows, memory/runs/hermes_burn/usage.jsonl, 2026-10-01)
- fable-5.1: $10/M in, $50/M out (n=6 rows, same instrument, 2026-10-01)

AMENDMENT 2026-10-01 (fable cells re-marked): fable's FABLE1 B1/B5 zeros are
NOT capability zeros - they are MEASURABLE-WITH-RECIPE cells: both 18KB
estate-review asks burned the whole 12000-token cap on hidden reasoning
(finish=length, empty content). B3/B4 (4/5, convergent IMP1s at 74s/48s) and
B6/B8 (6/6, PASS at $0.0076/$0.11) prove the animal performs when the fire
rides the recipe. Re-measure B1/B5-class cells only through
mag/inference_budget.py plan_call (review-shape floor 24000 or streaming or
thinking-off); an EMPTY_REASONING burn under the guard is terminal, never a
re-fire. B2/B7 remain not-fired placeholders (early stop), still UNMEASURED.
Receipt: watch/inbox/model_garden/FABLE1.md; law:
memory/rib/RIB_INFERENCE_BUDGET_20261001.md.

### local lane

| family | verdict | condition | measured-by | moment |
|---|---|---|---|---|
| ollama gemma:2b / gemma4 / qwen2.5-coder:7b | UNMEASURED at battery shape ($0, T1) | local, free, instant | providers.yaml ollama block | 2026-10-01 |
| Qwen3-8B on this Zen2 box | UNMEASURED; known pathology: bf16 emulation 159-183s/forward, fp32 6x faster; RAM gate free-2GB | name the deviation | RIB_MODEL_GATES_20261001.md | 2026-10-01 |

### stealth free lanes - SENSING surface

| family | verdict | condition | measured-by | moment |
|---|---|---|---|---|
| stealth/space-bunny-alpha | free-lane SUBSTANCE LEADER (6.7-8.0KB structured); owns ALL 9 finish=length rows (truncation risk); 1 dead citation in 122 audited | sensing, never done-work | watch/inbox/STEALTH_TRIAGE_20260930.md + animals/stealth_space_bunny_alpha.jsonl | 2026-09-30 |
| ling-3.0-flash-sante | terse 1.3-1.6KB, explicit anti-fabrication honesty; cached_tokens=0 on all rows (no bankable prefix-cache) | sensing | animals/ling_3_0_flash_sante.jsonl | 2026-09-30 |
| stealth free lanes (as a class) | 459 rows, ZERO 429, 69h+ sustained forced mining | CONTRADICTION OPEN vs RIB_FREE_USAGE_POLICY_20260823 (which says forcing them throttles); resolve with instruments, not by editing either rib silently | animals/stealth_free_lanes.jsonl | 2026-09-30 |

### nous primes lane (cross-family rail)

LESSIG RAILS mandatory on all Nous primes: reasoning {max_tokens} + retry-on-empty
+ reasoning-tail labeled unverified. Without: gopher disease (11/12 zero-content,
$1.43 for one answer). With: 6/6 full at $0.41. 402 = credit floor on primes, not
dead pool. Source: watch/inbox/last_mile_20260930/GOPHER_BURN_RECEIPT.md +
RIB_MODEL_GATES_20261001.md, moment 2026-09-30.

## FILL PROCEDURE (for the battery lane)

1. Read the funded/reachable set from RIB_DRIVING_LADDER_20260928.md + providers.yaml.
2. Fire the 8-item battery per family at the ECON-documented shape (watch/inbox/model_garden/ECON.md).
3. One row per cell, all 7 fields, UNMEASURED until the instrument returns.
4. Bank raw rows in logs/duel/duels.jsonl (or a model_garden receipt), mint the
   receipt, then fill cells FROM THE RECEIPT the same session.
5. Supersede, never overwrite: stale rows keep lineage.

Falsifier: a routing decision that cites a cell whose moment is stale or whose
condition does not name the shape actually fired is a one-bug violation; and a
week where cells filled but no receipt landed means the battery is theater.

## AMENDMENT 2026-10-01 (PREMIUM AUTOPSY cells): replay-measured rows at
18-40K-char premium-ask shape

Instrument: lane AUTOPSY-1, 17 premium questions replayed byte-identically at
a 6-family parliament (102 fires, all content-channel, zero refusals). Receipt
REQUIRED READING for any routing decision that cites these cells:
watch/inbox/model_garden/PREMIUM_AUTOPSY.md (grade table + conditions). These
rows extend, never supersede, the battery cells above (different shape: real
estate asks, right-sized evidence, one attempt per family per question).

| family | capability | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|---|
| glm-5.3-flash (zai coding ep) | adversarial-review, review shape | WIN 17/17 content, mesh-convergent on 10/17 questions | $0.0012/ask metered | uncapped + thinking on + reasoning_effort low (recipe path; no hang at effort-low, contra the cheapgrid1 effort-max hang) | PREMIUM_AUTOPSY.md + usage.jsonl PA-* | 2026-10-01 |
| deepseek-chat (v4.1-flash map) | adversarial-review + analysis, review shape | WIN (deepest mesh replies: S4 laundering chain, S2 injection channels) | $0.0078/ask peak | thinking OFF (AH10); 27K-char bodies held, long-form degradation did not bite | same | 2026-10-01 |
| moonshotai/kimi-k2 (Nous) | adversarial-review + research synthesis | PARITY-to-WIN; prior-art recall class covered | $0.013/ask ceiling (prepaid) | no thinking control; verbose (64.8K completion / 17) | same | 2026-10-01 |
| qwen3.8-max-prime (Nous) | adversarial-review + adjudication | WIN (byte-pinned tables; S4 LAG proof, B2 basis drift, D3 residues) | prepaid; token-hungriest 71.3K completion | LESSIG rail 6000; NO gopher disease at this shape | same | 2026-10-01 |
| grok-4.7 (xai SD) | adversarial-review, effort-low | WIN 17/17; unique asymmetric-trust + stale-audit finds | $0.032/ask est (2.0/6.0 per M) | effort low + 12000 cap + WHOLE-RESPONSE: streaming-only law did NOT bite at this effort/shape | same | 2026-10-01 |
| gemma4:latest (local) | adversarial-review, 27K-char bodies | DNF-BY-WINDOW (ctx 8192 tail-keep cuts the contract) | $0 | route via context_pack sizing (janitor 4800 chars), never raw replays | same + scripts/premium_autopsy_local.py | 2026-10-01 |

NEW QUESTION-CLASS LAW (the autopsy's one-line map): the mesh reads, the
frontier simulates. Evidence-readable asks (config audit, protocol audit of
provided bytes, doctrine roast, falsifier design, research synthesis from
provided evidence) route CHEAP-FOREVER: mesh matched or surpassed on 14/17 at
2-4 percent of premium dollars. Asks demanding RUNTIME-SIMULATION of code
(cross-platform lock semantics, CPython/OS interactions, multi-stage string
mutation) route PREMIUM: 0/5 mesh on the S5 re-entry deadlock and the S4
os.kill(0) Windows find, both fully in-evidence. Falsifier and honest limits
in the receipt.


## POST-DATUM 2026-10-05: the stealth free lanes row above (CONTRADICTION OPEN, 459 rows,
ZERO 429, 69h+ sustained forced mining) was resolved by instrument, per its own order.
Resolving probe: 13 lanes, cool width-1 spaced vs heat 13-wide parallel x3 waves, 52 asks,
one key (watch/inbox/ribvault_20261005/R062_FREE_USAGE_RESOLVE_20261005.md). Measured:
zero 429 at drip rate; 2 x 429 (poolside/laguna-xs-2.1:free, upstream rate-limit) at forced
instantaneous width. Conditions-bound resolution, neither side struck: the zero-429 row
witnesses the drip rate only; forcing does throttle (RIB_FREE_USAGE_POLICY_20260823
mechanism measured real). Freshness: inclusionai/ling-3.0-flash-fin:free now 404s
("unavailable for free") -- its B2-202 earned line is retired from the free tier.
