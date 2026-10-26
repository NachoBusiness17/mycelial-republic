# ECONOMIST SPEND AUDIT — 2026-09-01 01:30Z
*Economist seat — half Satoshi, half Friedman. English, tables, no novel. Every number MEASURED (source) or labeled ESTIMATED / UNKNOWN-OPERATOR-PULL.*

**Window:** audit of capacity vs burn, closing 2026-09-01 01:30Z.
**Spend doctrine (water_ledger 14:07Z):** $1/hr operator-active, cheap/off-peak autonomous. **COST LAW (riddler 01:00Z):** the mixture IS the optimization — expensive model does less work, more valuable work; gophers increasingly free; *only real cost is the driver.*
**Conservation law (MEMORY L13):** until 2026-09-02 12:52Z — DeepSeek + free lanes; zcode key hands-off.

---

## A. CAN-SPEND — every funding source (capacity table)

Legend for `state`: **MEASURED** = billing/telemetry/probe receipt behind it; **CORPUS** = carried in `/mag/memory/runs/seat_corpus/latest.json` (ts 08-29T17:46Z); **UNKNOWN-OPERATOR-PULL** = no receipt, operator must fetch. Ceiling/reset where known.

| Lane (ref) | type | ceiling / quota | reset (known) | marginal $/1M | state |
|---|---|---|---|---|---|
| **water pool** (ledger) | operator cash pool | $20.00 pool | n/a | — | MEASURED (water_ledger jsonl) |
| **ollama** (local) | local, $0 electricity | unlimited (GPU/power) | — | $0 | MEASURED (electricity only) |
| **zai-pro** `/z_ai2` (Max plan) | funded plan — cash sunk | Max GLM Coding V3 Quarterly $403.20/qtr paid; 1600 prompts/5hr, 8000/wk, each 15–20 model calls | rolling 5hr/7d | ~$0 marginal (97–99.9% cache hit measured 08-26) | MEASURED (probe-2 200 OK tonight; billing export 08-29) |
| **zai-lite** `/z_ai3` (Lite) | funded plan — cash sunk | Lite V3 Yearly $131.10/yr (list $216, 63% off) | annual billing cycle | ~$0 marginal (cache lane) | CORPUS ($131.10/yr from MEMORY L47) |
| **z_ai** `/z_ai` (coding-plan #1) | coding-plan quota | monthly/weekly quota — **WALLED 429/1310** | **reset 2026-09-02 12:52:28Z** (MEASURED) | $0 marginal on plan | MEASURED (probe-1 429 reset) |
| **z_ai4** `/z_ai4` (coding-plan #2) | coding-plan quota | same 1310 wall | same reset | $0 marginal on plan | CORPUS ("same 1310 wall") |
| **zai** `/zai` (paas API key 3254...c7fd) | prepaid API (per-use) | no quota — **BILLED per token** | n/a | **$0.075/$0.25/$0.015** (in/out/cache) | MEASURED (billing export 08-31) |
| **deepseek** (direct) | prepaid API | no hard quota; off-peak (01–04, 06–10 UTC Mon–Fri) = half price | n/a | off-peak out ~$0.66/1M? blended; late-month avg **$1.33/day** | MEASURED (telemetry MEMORY L47) |
| **together** | trial/paid API | no hard quota; batch −50% | n/a | $0.14/$0.28 (cached $0.03; batch → $0.07/$0.14) | MEASURED (rate card L46; activated 08-31 20:39Z) |
| **nvidia** (NIM) | free credits | 102-model catalog; credits balance | UNVERIFIED | $0 (credits) | CORPUS / **billing UNVERIFIED** (L46, docs 404) |
| **groq** | free tier | 30 RPM / 1K RPD / 200K TPD | daily | $0 | MEASURED (rate card; fuel 90/103=87.4%) |
| **cerebras** | free tier | 5 RPM / 30K TPM / **1M TPD** | daily | $0 | MEASURED (rate; activated 08-31 21:15Z) |
| **openrouter** | free lanes (50→1000 RPD @ ≥$10 bal) | quota-based | daily | $0 free fleet | CORPUS (operator receipt, not probed) |
| **grok_a / grok_b** (desktop) | desktop subscription | subscription (sunk) | billing cycle | $0 marginal | UNKNOWN-OPERATOR-PULL (idle seats, hook-state only) |
| **chatgpt_codex** (desktop) | desktop subscription | subscription (sunk) | billing cycle | $0 marginal | UNKNOWN-OPERATOR-PULL (idle seat, zero burn rows) |
| **zcode** (GLM CLI) | desktop/coding CLI | coding-plan CLI quota | — | $0 marginal | **POLICY-HELD** to 09-02 12:52Z (conservation, not waste) |
| **openai / xai / anthropic / google** | prepaid/paid API | configured but **key_present:false** (openai/xai/anthropic/google per corpus) | n/a | unmeasured | UNKNOWN-OPERATOR-PULL (no receipts; no keys live) |
| **moon h/w** (M5 covenant) | optional vast blade | **$0.12/hr blade cap** (operator word gate) | per hour | $0.12/hr | CORPUS (MOONSHOT M5; operator word required) |

**Hard ceiling (MOONSHOT §5):** **$3/day** without operator word. (M5 blade only at operator word.)

---

## B. HAVE-SPENT — per-lane actual burn (recipient table)

### B1. water_ledger — ALL 7 lines (entire burn ledger, enumerated)

| ts | id | amount | note (abbreviated) | receipt rank |
|---|---|---|---|---|
| 08-31 11:49:03Z | zai_credits | **$0.75** | ESTIMATE: 5.3 lead-hr @ ~100k tok (in+out) at 50% off until 09-09; 5 leads — rate receipt, not per-lane burn | ESTIMATED (rate-receipt math) |
| 08-31 11:41:00Z | zai_credits_rate_note | **$0.00** | RATE RECEIPT: 5.3 lead ≈ $0.75/hr at 50% off; OCTANT wave-1 ran 6 leads ≈ 4.5 lead-hrs ≈ $3.40 (in-budget); full price $1.50/hr — windows matter | MEASURED (rate card) |
| 08-31 12:21:11Z | zai_credits | **$2.65** | CORRECTION: OCTANT wave-1 true burn ~4.5 lead-hrs; reconciles ledger to estimated reality (rate math, not provider invoice) | ESTIMATED (reconciliation) |
| 08-31 14:07:37Z | zai_credits | **$0.00** | OPERATOR BUDGET LAW: $1/hr active, cheap/off-peak away — first spend-policy receipt | POLICY (operator) |
| 08-31 14:07:00Z | spend_policy | **$0.00** | OPERATOR BUDGET LAW formalized ($1/hr active / cheap autonomous); water clock gets policy context | POLICY (operator) |
| 08-31 20:39:25Z | together_activation | **$0.00** | TOGETHER LANE ACTIVATED: Flash-0731 serverless 200 OK (probe 5, 7s) | MEASURED (probe) |
| 08-31 21:15:31Z | lane_activations | **$0.00** | CEREBRAS LANE ACTIVATED: gpt-oss-120b 200 OK (10s, 165 tok); groq rate-limited in flight; codex pending paste | MEASURED (probe) |

**Ledger dollar-burn total: $0.75 + $2.65 = $3.40** (2 rows carry dollars; 5 rows are policy/activation/rate receipts at $0).

### B2. Other actual burn (beyond ledger)

| item | amount | receipt |
|---|---|---|
| **Tonight's zai API session burn** (billed lane 3254...c7fd, before 01:21Z route fix) | **$0.743** (4.29M in / 11.3M cache / 374k out over 236 calls) | MEASURED — archivist `zai_billing_telemetry` 08-31 14:18Z |
| **DeepSeek** late-month avg | **$1.33/day** (run-rate ~$40/30d; month-scale $93.34 / 69,335 req / 98.01% cache) | MEASURED — telemetry MEMORY L47 |
| **zai credits estimate** (pool entry) | **$0.75** estimate (5-lead burn) | ESTIMATED — ledger line, rate-receipt math |
| **z.ai API 6-day** | **$0.81/6d** (08-30 = $0.743 of it) | MEASURED — billing export key 3254...c7fd |

### B3. The wound: $19.25 founding claim vs $16.60 truth

The founding wound: a $19.25 burn claim applied to the $20 pool left **$0.75** — then honest money-lane correction (ledger 12:21Z) re-derived **$16.60** left. UNTOUCHED_SURFACE §"Ledger reconciliation" confirms ledger zai_credits burn = 0.75 + 2.65 = **$3.40** → **$20 − $3.40 = $16.60** — the ledger now agrees with itself.

**Current status:** HEALED at the ledger level (internally consistent), but still **rate-receipt math, NOT a provider invoice.** The $16.60 has no z.aai billing receipt behind it. UNTOUCHED_SURFACE §1 marks the original $3.40-estimate "not per-lane burn" (MOONSHOT §2 references "ocean row 4: $16.60 true, $19.25 claimed"). Mark **UNKNOWN-OPERATOR-PULL** for true per-lane burn confirmation.

---

## C. RECONCILIATION — ledger totals vs billing-receipt claims

| claim | ledger shows | billing receipt behind it? | status |
|---|---|---|---|
| $20 water pool | $20 (implicit ceiling; $16.60 left after $3.40) | no provider pool invoice | partial — pool is operator-defined |
| $3.40 zai_credits burn | rows 1+3 = $3.40 | **NO** — rate-receipt math, not provider invoice | **CREED GAP** |
| $16.60 balance | ledger-consistent | **NO** — inferred from $3.40 | **CREED GAP** |
| $0.743 session burn | not a ledger row | **YES** — zai_billing_telemetry export | RECEIPTED |
| $1.33/day deepseek | no ledger row | **YES** — telemetry billing | RECEIPTED |
| $93.34 month / $40 30d run-rate | no ledger row | **YES** — MEMORY L47 telemetry | RECEIPTED |
| $534.30 z.ai combined cash / $296 list-value (Max 4-day) | no ledger row | **YES** — billing export 08-26..29 | RECEIPTED |
| zai API $0.81/6d | no ledger row | **YES** — billing export key 3254 | RECEIPTED |
| $403.20 / $131.10 plan cash | no ledger row | **PARTIAL** — MEMORY L47 (subscription cost, not line-item) | **CREED GAP (plan cash basis) ** |

**Creed gap list — numbers with NO billing receipt behind them:**
1. **$3.40** zai_credits burn (both rows — ESTIMATED, reconciliation only)
2. **$16.60** water-pool balance (derived, not invoiced)
3. **$19.25** founding-wound claim (original, uncorrected — the discrepancy source, superseded by $16.60)
4. **$0.75** estimate (ledger row 1 — 5-lead burn, rate-receipt math)
5. **$403.20 / $131.10 / $0.75/hr / $1.50/hr** plan + rate numbers — subscription cash from MEMORY, no per-lane receipt
6. **zai credits post-09-09 full price $1.50/hr** — rate not re-verified
7. **nvidia credits balance + $5/$10 credit tiers** — billing UNVERIFIED (docs 404)
8. **openai / xai / anthropic / google spend** — no receipts at all, no live keys

*(4 of tonight's 8 gaps are z_ai/credit-lane cash without provider invoices; 3 are subscription/plan-cash basis; 1 is nvidia.)*

---

## D. DELTA — capacity minus usage (untapped money + waste + the 11x ROI test)

### D1. Untapped money (untouched lanes × ceilings)

| lane | ceiling | burn this window | Δ untapped |
|---|---|---|---|
| **zai-pro (Max plan)** | 1600 prompts/5hr, 8000/wk; $0 marginal | ~0 (probe only) | **~8000 prompts/wk** — the single biggest untapped line |
| **zai-lite** ($131.10/yr sunk) | $0 marginal cache lane | 0 | full capacity |
| **cerebras** | 1M TPD free | ~165 tok (probe) | **~1M TPD free** |
| **groq** | 200K TPD free | ~0 (rate-limited probe) | ~200K TPD |
| **together** | per-use, batch −50% | activation only | full rate headroom |
| **nvidia** | free credits | 0 | full (held for UNVERIFIED billing) |
| **openrouter** | 50→1000 RPD free | 0 | full |
| **chatgpt_codex / grok_a / grok_b** | subscription sunk | 0 (idle seats) | full — the operator-named GPT-utilization gap |
| **deepseek** | off-peak half price | $1.33/day | headroom off-peak |

### D2. Waste items found

1. **`reasoning_effort=high` everywhere** — Flash's weakest mode at a premium. High ≈ 1.5–2× output (ESTIMATED multiplier, z.ai doesn't publish exact); doubles effective $/100K on the billed zai lane ($0.25/1M out → $0.50 under high). Verdict: **default `low`; `high` only single-shot reasoning-critical** (archivist `reasoning_effort_cost_analysis` 00:53Z). Full-cost waste while `high` was default on the billed lane.
2. **Billed-lane session until 01:21Z route fix** — the session ran on `zai` API key 3254 (BILLED $0.075/$0.25 per 1M), not the funded plan key. Burned **$0.743** before fix. **Waste corrected tonight** — operator configured route to zai-pro (funded Max, $0 marginal).
3. **1310 thrash risk** — z_ai / z_ai4 / zai-2 all carry the same 429/1310 wall until 09-02 12:52:28Z. Any routing attempt to them = guaranteed quota error. **Fix applied:** prefer_order demotes z_ai/z_ai4/zai-2 to bottom tonight (ROUTE §3c). **Waste avoided.**
4. **Cold zai-pro first call** — cached_tokens=0 on tonight's probe (probe-2, cold start). Warm-prefix cache-hit (97–99.9%) is a *steady-traffic* property, not a window-open guarantee. Waste only if burst routed there cold. Mark awareness, not current spend.

### D3. The 11x subscription ROI claim — does the receipt support it?

**Claim (riddler MAKE-IT-FUN 00:14Z):** "11x subscription ROI, 150% bonus, $40/mo floor."

**Receipt test:** The **only** receipted subscription-value math is **M5 §2 / MEMORY L47 Max-plan line: $403.20/qtr cash → 4-day $296 list-value ≈ 5–7x quarter return.** That is **5–7x**, on the Max plan alone, one quarter.

- The **11x claim is NOT receipted** in any source I have. It appears only as an operator-confirmed economics assertion in MAKE-IT-FUN (00:14Z). No 150% bonus arithmetic, no 11x derivation, no $40/mo floor backing lives on /board or in MEMORY.
- The dollar values that WOULD back 11x ($403.20 → ~$4,400+ output value within the ROI frame) are not split across a receipt.
- **UNTOUCHED_SURFACE flags the same:** plan/rate numbers are subscription-cash-from-MEMORY, not reward receipts.

**Verdict on 11x: UNSUPPORTED by current receipts.** Supportable today is **5–7x** (Max plan, receipted). The 11x / 150% / $40/mo floor are **UNKNOWN-OPERATOR-PULL** — the operator holds the subscription-portal economics that would prove or kill them.

---

## E. OPERATOR PULL LIST — 6 exact billing pages/exports only the operator can fetch

| # | page / export (operator) | what number it closes |
|---|---|---|
| 1 | **z.ai billing dashboard** → Max plan (GLM Coding Max V3) monthly/annual usage + spend in $ | the 5–7x vs 11x ROI verdict; true quarter return; closes `$296 list-value` ↔ paid-price delta |
| 2 | **z.ai subscription portal** → Lite plan (V3) annual spend + if credits-based new-plan migration hit the grandfathered sub | the `$131.10/yr` basis; confirms Lite still $0-marginal post July-30 plan revision |
| 3 | **z.ai API usage export** (key 3254...c7fd, next cycle ≥09-01) | actual `$0.743` line-item vs telemetry estimate — closes Creed gap #1 of session burn |
| 4 | **DeepSeek billing export** (all keys, next cycle) | confirms `$1.33/day`, `$93.34/mo`, `$40/30d` run-rate, `98.01%` cache to a true invoice |
| 5 | **NVIDIA NIM credits balance** (docs/portal 404'd) | the unverified credits balance — unlocks nvidia from STALE to USED with a spend ceiling |
| 6 | **OpenAI + xAI balance** (both keys absent today) | converts openai/xai lanes from UNKNOWN to MEASURED; optional, only if keys are re-added |

*(Also helpful: one z.ai credits-plan page pre/post 09-09 to verify the 50%-off → full-price $1.50/hr window math.)*

---

## F. VERDICT

**Net position: solvent, under budget, but the audit's honesty floor is thinning.** Ledger-consistent cash is **$16.60 of $20**, and hard ceiling is $3/day — we are nowhere near a breach. The fleet is NOT short on capacity: the funded Max plan (zai-pro, $0 marginal), Lite plan, desktop subscription seats (codex/grok), and free remote lanes (cerebras 1M TPD + groq 200K TPD + openrouter) carry **near-zero-to-$0 marginal** capacity that is largely untouched. The single greatest under-deployed asset is **zai-pro's ~8,000-prompt/week Max-plan quota** (cash already sunk, $0 marginal, probe-verified live tonight). The next dollar — or rather the next *distribution of effort*, since the driver is the only real cost — SHOULD flow per the ranking law: T0 ollama for janitor scut, T1 free/cached remote (cerebras/groq/together/openrouter) for bulk, T2 zai-pro + zai-lite for the funded $0-marginal backbone, deepseek off-peak as the paid driver lane, and the **billed zai API lane demoted to LAST** (it is the only lane costing real per-token dollars). Because the routing is still open-loop (economist computes, router doesn't auto-obey), the highest-leverage spend is one operator apply-gate: commit the ROUTE §3 diffs (zai-pro key swap for the session lane + reasoning_effort default `low` + prefer_order), which eliminates tonight's only real burn source. The $0.743 billed-session burn was the waste specimen; the fix is already applied.

**Not printed:** no secret key values.
