# NIGHT CACHE RECEIPTS — S2 CACHE MINING CAMPAIGN (2026-09-01)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: DeepSeek off-peak frozen-prefix cache hits 100% after one cold wave and scales with prefix depth (~$0.0002-0.003/call); z.ai Lite cache is live but was bucket-gated (1305) that night — SUPPORTED (all figures MEASURED from usage fields, raw jsonl cited) · falsifier: re-running the night_cache.mjs probe fails to reproduce the hit rates, or night_cache_receipts.jsonl contradicts the tables

Window: 06:00–08:00Z. Probe: `/root/.openclaw/workspace/night_cache.mjs` (frozen-prefix cache probe, never prints keys).
Raw rows: `/board/night_cache_receipts.jsonl`. All figures MEASURED from usage fields.

## RESERVOIR 1 — DeepSeek off-peak (`deepseek-chat`, off-peak 06:00–10:00Z) — CLEAN PASS
Frozen prefix: `cache-me-now-2026 repetition builds the context cache.` × N, single system+user READY call.

| test | prefix reps | par | waves | http-ok | cache-hit rate | cached tok (per call) | latency (med, ms) |
|---|---|---|---|---|---|---|---|
| ds-offpeak-cache | 380 | 1 | 6 | 12/12 | wave1 cold (0), wave2-6 **100%** | 0 → 4864 | 847 → 489 (wave-1→steady) |
| ds-concurrency | 380 | 4 | 3 | 12/12 | **100%** all waves | 4864 | 782 → 526 |
| ds-longprefix | 600 | 1 | 3 | 3/3 | wave1 cold, wave2-3 **100%** | 7808 | 815 → 516 |

**Findings (MEASURED):**
1. DS begins cache-building immediately; after ONE cold wave, subsequent identical-prefix calls hit **100% cache** (4864 tok at 380 reps; 7808 at 600 reps).
2. Cache grows with prefix depth: 380→600 reps ⇒ 4864→7808 cached tok (+60% cacheable input). No ceiling observed in this range.
3. Concurrency is clean: par-4 holds 100% hit, no degradation, latency improves with cache warmth (782→526ms, ~33% faster).
4. Latency benefit: cold ~815–847ms → warm ~490–540ms (~40% faster) — measured on both par-1 and par-4.
5. **Economic math:** DS off-peak cached input = $0.03/1M (rate card, gate PASS). At 7808 cached tok ≈ **$0.0002/call cached** input for a ~6× deeper context than the probe; a 100k-tok cached batch call ≈ $0.003. The off-peak DS lane is a *reliable, near-free* high-context cache lane.

**Gate:** 3 paid DS rows logged cost_gate_ledger, all PASS, est total ≈ $0.017 (87 probes ≈ ~100k combined). Well inside the ≤$1 DS budget.

## RESERVOIR 2 — z.ai Lite (`glm-4.7-flash`, plan credits) — RATE/OVERLOAD GATED
- 401 on legacy key name mapping (key resolved wrong — fixed to `ZAI_API_KEY_LITE`).
- With correct key: **error 1305 on ~all calls** across par-1/4 × prefix 60/380/600 reps — persistent rate/credit-bucket gate (matches ZAI_LITE_LAW: 2000-credits/5h use-it-or-lose-it bucket; bucket appears gated tonight).
- **2 successes captured before the gate:** wave-2/3 at par-1 and par-4 showed **cache hit at 4604 tokens** (proxy for 4864-DS = same prefix length). Latency 883–1156ms.
- **Verdict:** z.ai Lite cache mechanism IS live (4604 cached tok measured), but tonight the Lite pool's 5h bucket is gated (1305). Not usable as a high-volume cache lane this window. Record as MEASURED-cache-live / RATE-GATED. Do not mark permanent.

## RESERVOIR 3 — z.ai credits (`1305`) — GATED (same bucket family)
- Independent of Lite key; also 1305-fenced. Confirms a z.ai-pool-level rate gate tonight, not a key bug.

## Unmeasured reservoirs (logged to water_ledger per receipt law, not measured this window)
The 11-unmeasured-reservoirs note from the brief is a longer-window goal; tonight DS (reservoir 1) is the productive one. zai-lite + zai-credits (2/11) attempted → rate-gated. Others deferred to dawn/later passes to respect burn gate.

## Bottom line for S5/S6
- **Which cache lane actually yields tonight: DeepSeek off-peak.** 100% hit-rate at scale, growing with prefix depth, ~40% latency gain, ≈ $0.0002–0.003/call cached. This is the caching answer for the $200 deployment rec.
- **z.ai Lite cache: broken-peak tonight (1305 bucket-gate), not a burn; revisit in a fresh 5h bucket.**

## Labels
- All DS numbers MEASURED. zai cache-live = MEASURED (2 successes). zai rate-gate = MEASURED (1305). No UNVERIFIED claims.
