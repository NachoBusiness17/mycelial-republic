# MOICHE — mixture-of-agents × mixture-of-experts, rightsized (2026-08-31)

**Receipts used:** seat_corpus `latest.json` ts 08-29 (20 lanes, prefer_order, law "T0/T1 never remote"); groq free tier 30 RPM / 1K RPD / 200K TPD; cerebras 5 RPM / 1M TPD (~3000 tok/s); deepseek off-peak = ½ list (peak-guard refusal 09:55:57Z → ok 10:00:07Z; peak = 2×); z.ai 50% till 09-09 (operator 10:02Z); ollama = electricity; Mag MCP hand = 43 tools (`mcp_server.py`, manifest auto-generated from code); `/room/spawn` presets + patches 6a/6b (outcome auto-record); slot law 6-cap pool; gopher ROW = $0. Arms are themselves MoE checkpoints (gpt-oss-120b, deepseek-v4-flash) — mixture-of-models literally calling mixture-of-experts.

## 1. Ladder

| Rung | Tier served | Agent mix | Arm mix | Est $/hr |
|---|---|---|---|---|
| **8×8** | T0–T1 sweep (verify, count, ROW rows) | 6 OpenClaw seats (cap) + 2 `/room/spawn` ROW lanes | ollama ×6 local (gemma:2b → gemma4-desk) + groq gpt-oss-120b + cerebras gpt-oss-120b; judge = z_ai2 cache (97–99.9% hit, $0) | ≈ $0.03 (power floor only) |
| **16×16** | T1 full + light T2 (synthesis drafts) | 6 + 10 host lanes | + nvidia deepseek-v4-flash-0731 (3.4s verified), openrouter free lanes, z_ai3, together-trial, groq dual-key ×2, cerebras paced; judge = deepseek off-peak (½) | ≈ $0.05–0.10 |
| **32×32** | T2 judgment (T-verdicts, arbitration support) | 6 + 26 host lanes | full set + openrouter rotation ×6, nvidia ×2; judge = z.ai 5.3 (½ till 09-09) prime hours / deepseek off-peak; dissent preserved (MoA law) | ≈ $0.10–0.30 |

**$ formula** (only receipted multipliers): `$/hr ≈ (tok/hr ÷ 1M) × list × 0.5(off-peak or z.ai) × (1 − cache_hit)`. At the receipted swarm budget 30M tok/day ≈ 3M tok/hr: peak cost would be ~$0.90/hr **at an assumed $0.3/M list** (list price not receipted — flagged); the ½ windows and cache-mining push to the table numbers. Electricity ~$0.03/hr for the local 3B–7B arms is the true floor.

## 2. Rightsizing law

Arm count is set by task tier, not ambition (seat-corpus tiers):

- **T0** (mechanical: grep/fetch/format/count) → all-local ollama arms, **zero remote** ("never pay a remote for scut").
- **T1** (cheap think: verify, classify, vote) → 2 free remote arms (groq + cerebras) + local quorum; judge = z_ai2 cache $0.
- **T2** (frontier judgment: verdict, merge, arbitrate) → arms *collapse*: ≤3 arms + 1 judge lane (z.ai 5.3 ½ / deepseek off-peak). At T2, consensus exists to capture dissent, not to add headcount.

Synthesizer is always the cheapest capable model (MoA law); weight votes by confidence, not model reputation. `learn_rightsize` + `lane_cadence` are already cataloged organs for tuning arm counts from observed yield.

## 3. Binding constraint per rung

- **8×8 → OpenClaw 6-cap pool.** Unlock: already exists — `/room/spawn` presets put agents 7–8 on Mag host lanes (no OpenClaw slot consumed); 6a/6b auto-record their outcomes. No new patch.
- **16×16 → groq 30 RPM / 1K RPD / 200K TPD.** Unlock: config-only — dual-key rotation is already in the groq lane contract; cerebras 1M TPD takes spillover paced at 5 RPM; `lane_cadence` sets the rhythm.
- **32×32 → Mag apply-gate + off-peak guard.** deepseek peak 2× refused without `MAG_ALLOW_PEAK=1`; route→outcome wiring staged as 6a/6b awaiting operator apply. Unlock: schedule T2 bursts in the 10:00Z off-peak window (receipted), run z.ai 5.3 at ½ during prime hours; operator applies 6a/6b per runbook.

## 4. Baby-step test (this week, existing organs only)

Run one real Wave-1 duty through 8×8: the leads' verification passes. Each lead: T0 greps → ollama arms; two T1 votes → groq + cerebras; judge → z_ai2 cache. Agents 7–8 = `/room/spawn` ROW lanes repeating the cycle on a second surface. Receipt: `/board/rows/moiche_babystep.row.md`. **PASS** = one full 8-agent × 8-arm cycle with $0 API spend, groq <30 RPM, z_ai2 cache-hit ≥90%, outcomes recorded by 6a/6b.

**Self-attack:** weakest claim = the absolute $/hr figures (only ½ multipliers are receipted; list prices are not). Fixed via formula + flagged assumption. Second weakness: cerebras 5 RPM serializes 16 arms to ~3 min/arm-wave — acceptable at T1 cadence; noted, not hidden.

**GOPHER:** verify groq caps vs today's actual usage receipts | pointer: /mag/memory/runs (fuel_feed, groq) | output: /board/octant_20260831/rows/moiche-g1.row.md
**GOPHER:** confirm z_ai2/z_ai3 cache-hit still ≥95% | pointer: /mag/memory/runs/seat_corpus/latest.json + fuel receipts | output: rows/moiche-g2.row.md
**GOPHER:** list /room/spawn preset names + confirm 6a/6b staged files exist | pointer: /mag/mag/ room/spawn code + staged patches | output: rows/moiche-g3.row.md
