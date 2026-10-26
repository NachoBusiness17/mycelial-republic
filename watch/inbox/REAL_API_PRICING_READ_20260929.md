# REAL API PRICING READ (2026-09-29)

Operator dropped https://real-api-pricing.vercel.app/#lang=en bare. Site verified live (HTTP 200, Vercel, Last-Modified 2026-09-29 06:33Z). React SPA; full dataset pulled from the open data door `/data/site.json` (1,254,393 bytes, generatedAt 2026-09-29), banked at `watch/inbox/REAL_API_PRICING_site_20260929.json`. Source repo: github.com/FeiZhuLulu/real-api-pricing (open data, open methodology, static charts on raw.githubusercontent).

## What it is

An instrument for the estate's own standing question (cost truth, previously "accepted unpriced as honest unknown"). Project name: 真实API定价. Core formula, from the conventions block: subscription price / monthly tokens users can actually use = real blended unit price. Plotted against 8 independent capability boards (AA Intelligence Index v4.3 snapshot 09-22, Terminal-Bench 4.0, AA TB4, Code Arena, Agent Arena, AA Coding Agent Index v1.5, OpenDesign Arena, DeepSWE v1.1).

## Dataset census

- 268 subscription plan points, 18 vendors (Zhipu, DeepSeek, StepFun, Xiaomi, Meituan, MiniMax, Kimi, Muse, Alibaba, Tencent, OpenAI, Anthropic, Google, xAI, Cursor, Cognition, OpenCode, other). Each point: real_usd_per_mtok vs list_blended_usd_per_mtok, confidence grade, monthly_tokens, evidence list, promo_until.
- 330 benchmark configurations with median cost/task; 1,590 plan-to-configuration mappings with confidence grades.

## Headline rows (real $/MTok)

- Floor: StepFun Step 3.5 Flash, Step Plan Max (CNY 699): 0.0006 real vs 0.0242 list. Step 3.7 Flash: 0.0012. Chinese flash plans own the sub-penny floor.
- THIS SEAT MEASURED: Zhipu GLM 5.3 Flash (v2), GLM Coding Pro legacy CNY 149, off-peak (闲时): 0.0029 real vs 0.0353 list, conf HIGH. Peak rows 0.0059-0.0079. Lite CNY 49: 0.0058 off-peak. Max CNY 469: 0.0040 off-peak.
- OpenAI: GPT 5.6 Luna on ChatGPT Pro 20x: 0.0013; on Plus: 0.0027 (conf high). GPT 5.6 Terra Pro 20x: 0.0080.
- DeepSeek V4.1 Flash: 0.0024 (Command Code GOAT), API off-peak 0.0097 (conf high).
- Anthropic subscriptions: the discount table. Claude Sonnet 5 on Claude Pro: 0.0043 real vs 0.294 list (69x under). Opus 5 on Pro: 0.0106 vs 0.735 (69x). Max 20x/5x (9/14+ pricing): Sonnet 5 at 0.0051 (58x). All the 40x+ rows are Anthropic.
- Google Gemini 3.8 Flash on AI Pro: 0.0089 (conf HIGH is claimed for this row; Ultra rows conf LOW — allowance unmeasured).
- xAI: cheapest Grok 4.6 row 0.026 (Cursor Ultra), SuperGrok 0.059.
- Unmetered: exactly 1 row, Cognition Devin SWE-2, promo to 10/31, recorded approx-$0 and kept on the frontier.

## Methodology constants worth stealing

- Token mixes (agentic reality, cache-weighted): standard 97% cache / 2.5% input / 0.5% output; lowCache variant 85/14.5/0.5; Anthropic mix separate (cache-write priced). This is the KV-cache-scarcity-cage insight turned into a pricing convention: cache-heavy agentic seats see far lower effective prices than per-token list suggests.
- Unmetered policy: real price tends to 0, shown approx-$0, still on frontier; promotions must carry expiry dates and get re-checked at expiry.
- monthWeeks = 4, 30/7 kept only as sensitivity.
- USD/CNY 6.7787, dated and sourced with previousRate.
- sourcePriority evidence ladder: (1) user panel screenshot back-calculation, controlled full-burn measurement, official absolute token/credit tables; (2) local logs / ccusage and same-window allowance percentage; (3) user confirmation, with public conflict-reconciliation duty; (4) official dollar/credits converted at standard workload; (5) third-party roundups as low-confidence side evidence only. Receipt-grade ladder, directly stealable for estate cost-truth lanes.

## Estate angles

1. This seat's own tier is measured by an outside instrument at conf-high: about $0.003/MTok real off-peak, 12x under list. The driving ladder's workhorse economics now have a third-party number.
2. The Anthropic-unfunded law has a footnote: at allowance boundary a Claude Pro subscription is among the best real-price judgment capacity measured (Sonnet 5 at $0.0043/MTok). Whether the allowance is actually burnable inside window limits is the exact gap between this instrument's model and the estate's 5-hour-window lived law.
3. Steal candidates: the conventions block wholesale (token mixes, unmetered policy, promo expiry discipline, sourcePriority ladder) into the estate's dated-meters / cost-truth surfaces; the schema (points/configurations/mappings) as the shape for a fleet cost-truth ledger.
4. Caveats, honesty lane: no independent re-derivation of any row was performed in this window; confidence grades are the instrument's own. "Tokens you can actually use" is the hard term and this instrument knows it (that is why conf grades and the evidence ladder exist). Instrument banked as sensing; verification climbs to the funded tier per the driving ladder. Site is v1, generated today.

## Filing

- Receipt: watch/inbox/REAL_API_PRICING_READ_20260929.md (this file), registered in index_events.jsonl.
- Data: watch/inbox/REAL_API_PRICING_site_20260929.json (full site.json, byte-banked).
- Em-dash count: 0.
