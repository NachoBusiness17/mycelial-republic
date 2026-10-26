# LANE D — ECONOMIST LENS | GLM-5.3-Flash lineage | 2026-09-01 07:08Z

Scope: does the 3×-attention / 4.4×-KV claim change serving economics? Route re-rank? ZAI Lite tweak?
Lineage source: /board/GLM53_LINEAGE_DROP_20260901.md. Route source: /board/ECONOMIST_ROUTE_20260901.md. Plan law: /board/ZAI_LITE_LAW.md.

## 0. CLAIM STATUS — flag every number (vendor vs measured)
- **3× attention compute, 4.4× KV-cache** = **VENDOR-REPORTED** (Z.AI release). Lineage drop explicitly: "vendor-reported engineering results, not yet an independently reproduced audit." NOT measured by us. Tool: take as hypothesis, treat as UNVERIFIED until a probe on real long-context KV/credit behavior.
- **Flash per-token $0.075/$0.25/$0.015 per 1M** = **MEASURED** (zai billing telemetry 08-31 14:18Z, ECONOMIST_ROUTE §2). This is the paas API card.
- **Flash-first cascade 80.9% @ $1.70/task vs full-alone 69.0% @ $3.99** = **MEASURED pattern, but benchmark-UNVERIFIED** (archivist 08-31 23:00Z: "all vendor+together self-run, none independently audited"). Our numbers rest on Together rollouts 8/21+8/28.
- **Together H100 $5.49→$3.99/hr Sep cut** = **UNVERIFIED / STACKED** (INBOX_LINKS 04:26Z: "auto-harvested/unverified"; archivist digest: "stacked, untriaged").

## 1. If 4.4× KV is real — serving economics
The 4.4× is a **provider-side serving** lever, NOT a per-token-rate lever. Our price card ($0.075/$0.25) is already set; the KV cut does not change what Flash bills us. What it changes is **provider margin + long-context concurrency**:
- Same GPU serves ~4.4× more concurrent long-context KV → vendor's per-request cost drops → headroom for the vendor (or competitors) to undercut on long-context serving, not on our measured $/token.
- Cold long-context cost: ZAI_LITE_LAW law 3 says a cold 100k 5.3 call ≈ 70+ credits. 4.4× KV does NOT erase that — plan credits are token-multiplied, not KV-weighted. No measured Lite credit relief yet.
- **Verdict: the KV claim does NOT re-rank the lane map on evidence we hold.** Route order (T0 ollama → zai-pro → cerebras/groq → together caching → deepseek) is driven by measured $/100K and quota, none of which the KV claim touches. Re-rank only if a probe shows Flash long-context credit/price drop relative to measured today — which we have NOT seen.

## 2. Cascade & the Together cut
- Our Flash-first cascade already wins on measured economics: 80.9%@$1.70 vs $3.99 full-alone. The KV claim would only deepen this by making long-context Flash cheaper for the vendor — but our cascade economics are already favorable without it.
- Together $5.49→$3.99 is UNVERIFIED; if real, it cheapens our cheap-est host for GS/GPT-OSS/Qwen fleet, marginal (dedicated H100 hours, not our per-token lanes). Tag WATCH, not re-rank driver. Respect the together 04:26Z "untriaged" flag — don't lean on it yet.

## 3. ZAI Lite weekly allocation — justified tweak?
- NO measured evidence justifies a re-allocation from the KV claim. Lite law is credit-multiplier-driven, not KV-driven.
- One **directional, not quantified** tweak (flagged ESTIMATE): IF Flash KV-efficiency passes through as a better long-context credit-burn on off-peak (not measured, UNVERIFIED), the 5.3 → Flash drift on Lite could absorb the cold-100k penalty the current law 3 assumes. **Do NOT change the 80/15/5 split on the KV claim alone.** Wait for a real Lite calibration probe (the law's own better-by-default ladder).
- zai-pro Max remains the $0-marginal driver lane per ECONOMIST_ROUTE (a); KV claim doesn't move that — Max is a funded plan, price-immune.

## 4. Bottom line (≤6 lines)
- 4.4×KV / 3×attn are **VENDOR claims, UNVERIFIED** — no measured data, do not re-rank on them.
- Measured serving economics (Flash $0.075/$0.25, cascade $1.70/task) already favor Flash; KV claim is upside, not the load-bearing reason.
- Route map unchanged on evidence held. Together Sep cut = WATCH (unverified).
- ZAI Lite 80/15/5 split: NO change from KV claim alone; probe first.
- Action: add a KV-efficiency probe to the Flash characterization queue (real long-context credit/price vs measured), then reconsider. No spend authorized.
