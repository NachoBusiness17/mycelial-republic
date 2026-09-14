# NIGHT SHIFT 001 SYNTHESIS — the long dark (2026-09-01 05:45Z → 08:50Z)
> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: deepseek-flash off-peak + groq (gpt-oss-120b) are the two load-bearing seats; hold the rest for hardware — SUPPORTED (measured wavelength matrix 96/90 + DS cache receipts cited in card) · falsifier: a re-run of the 20-probe battery ranking another lane above deepseek-flash at $0, or DS cache hit-rate collapsing on re-measure

**Authority:** NIGHT_SHIFT_BRIEF_20260901.md (operator 05:44Z full budget; night-scoped conservation amendment). Every claim below is MEASURED (bytes on disk) unless tagged UNVERIFIED. No provider call was made by the ticker this pass — file synthesis only.

**Paid burn tonight:** ~$0.058 est total in cost_gate_ledger (paid rows ~$0.058), water_ledger rows show $0.017 (DS off-peak cache) + $0.017 (reservoir-1 yield math). **Gate PASS: ≤$2 budget, $0 burned this tick.**

---

## The night answers the brief's four questions

### 1) Which lesser model holds which lane at what quality?
From NIGHT_WAVELENGTH_MATRIX_20260901.md (gen C battery, 20 frozen probes, gen B = glm-5.3-flash baseline at 100):

| Lane | Model | Score | Δ vs gen B | Seat verdict (MEASURED) |
|---|---|---|---|---|
| **deepseek-flash** | DeepSeek-V4-Flash-0731 | **96** | −4 | **Generalist / riddler gate — the replacement seat.** 20/20 non-empty, $0 off-peak. Best value this night. |
| **groq** | gpt-oss-120b | 90 | −10 | Generalist + switchboard fallback. 18/20; strongest *open* lane. |
| together | DeepSeek-V4-Flash-0731 | 32 | −68 | Batch/bulk only — low live-answer trust, needs re-run. |
| nvidia | DeepSeek-V4-Flash-0731 | 30 | −70 | Free-credits scratch only — do not seat. |
| cerebras | gpt-oss-120b | 23 | −77 | Coverage ceiling (5/20 HTTP 429), not competence — static quality high, throttled out. |
| z.ai Lite | glm-4.7-flash | 2 | −98 | **No seat.** Empty/overloaded body; cache-mining-probe duty only. |
| openrouter free | gemma-26b | 0 | −100 | **Dead lane.** Provider 404 — free tier gone server-side. |

**Reading:** deepseek-flash ≈ gen B at $0 off-peak. groq is the honest open-lane fallback. together/nvidia/z.ai-Lite/openrouter are availability- or coverage-limited, not competence-gated (except z.ai Lite which returned nothing usable).

### 2) What does cache mining actually yield on Lite + DS off-peak?
From NIGHT_CACHE_RECEIPTS_20260901.md + CACHE_YIELD_MATH_20260901.md:
- **DS off-peak: CLEAN PASS.** 100% hit-rate at 4864–7808 cached tokens; ~40% latency gain; **$0.03/1M cached vs $0.14 uncached** → $0.11/1M saved. Monthly extrapolation: ~23.8M cacheable tok/30d → **$0.71 cached vs $3.33 uncached → $2.61/mo saved**. Load-bearing reservoir.
- **z.ai Lite + credits: cache mechanism MEASURED LIVE** (4604 cached tok, wave2/3 par-1/4) but tonight's 5h credit bucket RATE-GATED (error 1305) → $/1M **not extrapolatable. DEFFERED, not burn** (0 spent). Re-measure on a fresh bucket.

### 3) Does the switchboard pass its Five Tests?
From FIVE_TESTS_RUN_20260901.md: **BLOCKED-ON-HOST-APPLY — not a code gap.** Patch `patch13` (five-hypervisor-tests) staged since 08-31 awaiting host `openclaw_patches apply` + `pytest`. Cage has no python. Desk-checks pass source-level; **runtime 5/5 green is UNVERIFIED.** Codex convergence gate (no 32×32 until green) correctly HELD.

### 4) $200 deployment recommendation
Grounded ladder (brief S6 options) adjusted by tonight's evidence:

- **Ladder A (OpenRouter $10 top-up → 1000 RPD free fleet): 💀 DEAD — as structured.** OPENROUTER_AUTOPSY: `:free` slugs return 404 serverside regardless of balance ("This model is unavailable for free. The paid version is available now"). The $10 does NOT unlock the free tier. Recast as **A′**: keep the $10 only if targeting cheap *paid* slugs with per-request cost capping — but this competes with cheaper/free alternatives, so it is NOT the priority spend.
- **Ladder B (Together batch credits for bulk): ⚠️ SECONDARY.** together has the same DeepSeek-V4-Flash engine but only 32/100 live-answer trust this window. Good for batch/bulk where quality bar is lower; not the marquee lane.
- **Ladder C (hold for hardware rung after FreeToken host check): ✅ PRIMARY RECOMMENDATION on top of —**

**The actual $200 rec:** put the deployment weight behind **deepseek-flash off-peak (reservoir 1) + groq (gpt-oss-120b) as the fallback open lane**. #1 — fund the **deepseek paid lane** (already wired, $24.13) at off-peak for cache economics (~$2.6/mo saved, near-gen-B quality at ~$0.03/1M); #2 — route groq as the switchboard/generalist open lane (90/100, no forced paid); #3 — **hold the remainder for the hardware rung** (Ladder C) pending the FreeToken host check; #4 — re-test z.ai Lite cache on a fresh 5h bucket (1405→ no, 1305) and OpenRouter against a *known-live* paid slug before any spend.

Ordered: **DS paid lane (off-peak) + groq = the two load-bearing seats; hold for hardware; z.ai-Lite + OpenRouter re-probe before their respective dollars move.**

---

## Honesty register (UNVERIFIED / deferred)
- S3 Five Tests runtime green: **UNVERIFIED-ON-HOST** (patch apply + pytest pending).
- z.ai reservoirs 2–3 $/1M: **DEFERRED** (rate-gated, not burn).
- OpenRouter free tier: **DEAD as `:free`** this window (404 serverside).
- Ponytail ladder: 5/5 fires, 0 fails, ~45min sample — **no promotion, no prune yet** (needs 24h cadence check).
- Codex convergence gate: **HELD correctly** (no 32×32 until Five Tests green).

## Receipt chain (all MEASURED, indexed)
lineage_genC_*_20260901.md (7) · NIGHT_LINEAGE_SUMMARY_20260901.md · NIGHT_CACHE_RECEIPTS_20260901.md + jsonl · CACHE_YIELD_MATH_20260901.md · S4_STEERING_20260901.md + s4_steering_receipts.jsonl · FIVE_TESTS_RUN_20260901.md · OPENROUTER_AUTOPSY_20260901.md · PONYTAIL_LADDER_STATS_20260901.md · NIGHT_CLASSIFIED_REGISTER_20260901.md · NIGHT_WAVELENGTH_MATRIX_20260901.md · cost_gate_ledger.jsonl · water_ledger.jsonl.

---
**End-of-shift note (S5 → S6):** synthesis filed at 08:50Z. S6 wrap = INDEX registration + memory write + this file's rec + removal of ticker at 10:45Z (or when all stages receipted). No gateway restart; no keys printed; paid burn $0 this tick.
