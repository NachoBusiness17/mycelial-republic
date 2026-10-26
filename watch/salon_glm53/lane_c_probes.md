# LANE C — GLM-5.3-Flash Probe Battery (probe-design lens) · 2026-09-01

Sources: `/board/GLM53_LINEAGE_DROP_20260901.md` (architecture claims), `staging/glm_parts.txt` (GGUF Q4_XL+mmproj = native-MM + quant-deploy lineage). NOTE: `staging/GLM53_FLASH_DEEPDIVE_20260831.md` does NOT exist — only `glm_parts.txt` available in staging; using that as deep-dive substitute.

## Doctrine gates (from ZAI_LITE_LAW)
Flash off-peak: 8,000 cr/wk ≈ 17,400 calls. Cached input NOT free (1.7 mult = 24.6% of fresh 6.9). Cold 100k 5.3 = 70 cr = 0.7% of week → **5.3 fresh long-context PROHIBITED**. Probe vehicle = **Flash cached/frozen-prefix only**. Battery cap ≤ 5% of Flash slice = **400 cr**.

## Cost model (Flash cached, input-dominant)
ctx→cr: 32K 0.69 · 100K 2.15 · 250K 5.38 · 500K 10.76 · 1M 21.53. One full cached ladder = 40.5 cr; ~197 ladders/wk fit. Low rungs give SAME architecture signal at ~1/30 cost.

## 1. Sparse/Linear attention boundary — H+test (info: HIGHEST, cheapest)
- **Claim (UNVERIFIED, vendor "3× less attention, 4.4× less KV"):** local (linear/recurrent) state dominates near-range recall; sparse global window gates long-range. Predict: recall is near-perfect in a contiguous window (~4-16k, "local linear state") then DROPS discontinuously at the sparse-global sweep distance; needs get recalled only if the indexer/IndexPool marked them salient.
- **Test:** needle-in-haystack, vary needle→query distance 512/4k/16k/64k/128k on a FIXED short prompt (identical, cacheable). Sweep the drop-off locus. PASS if recall ≥0.9 ≤16k then falls ≤0.6 at the predicted boundary; FAIL if linear decay (no boundary). This is the cheapest discriminating signal — run first, high volume (32K ctx only).

## 2. Long-context ladder 32K/100K/250K/500K/1M
- **Test:** same needle battery at each rung (degradation curve + verbatim-verbosity of a 1.5k-fact doc at end-of-context). PASS=maintains needle recall ≥0.8 up to stated ceiling (1M brand claim); FAIL at first rung where recall <0.8 OR where end-of-context verbosity collapses — reveals the real effective ceiling vs advertised 1M.
- **Vehicle:** Flash cached, frozen-prefix doc. Budget 120 cr = 3 full ladders. Run 32K/100K every ladder; 250K/500K/1M only after low rungs pass (validation, not discovery).
- **Cost:** 3× ladder = 121.5 cr.

## 3. Tool-use vs GLM-4.5 / GLM-5 (agentic-claim probe)
- **Claim (UNVERIFIED):** Flash native-agentic (Token-in-Token-out, stale-trajectory filtering). Test a deterministic zcode steered loop: grep→edit→run→fix 2-iteration task on a seeded syntax-bug fixture.
- **PASS** if Flash completes the loop correcting its own failure on iteration 2 (recovery behavior) and keeps thinking-block before tool calls. **FAIL** if it refuses, loops forever, or does NOT retain corrective trajectory across tool call (stale KV, i.e. indexer dropped the trace).
- Compare against 4.5/5 receipts already on board (grep MODEL_VAULT_PASSPORTS); do NOT run parallel cold — budget 80 cr, ~35 loops.

## 4. Behavioral signature capture
- **Metrics over short-context probes (near-$0):** repeat rate (verbatim duplicate answers to p-distinct queries), refusal rate (benign-policy battery), verbosity (answer token-count distribution), planning failure (multi-step instruction where it skips/compresses a required step).
- **PASS** = within-family norms (calibrated on GLM-5 receipts); **FAIL**/SIGNATURE = Flash-specific deviation (e.g. monotone repeats from linear-state, over-refusal). Budget 80 cr, short-ctx so volume-priced.

## 5. Receipt fields (all four families, per probe)
model_version, settings(temp/top_p/system), ctx_size, prompt_hash, needle_loc, tool_trace(json), latency_ms, credits(cost), outcome(PASS/FAIL), failure_signature, ts. Append `/board/salon_glm53/lane_c_probe_receipts.jsonl`.

## Rank by info-per-credit
1. **Sparse/linear boundary** (32K, ~0.7cr/call, answers the core architecture question — highest signal/credit).
2. **Behavioral** (short-ctx, volume, cheap, feeds passport failure-signatures).
3. **Tool-use vs 4.5/5** (agentic claim; needs 5.3 only if #1 confirms efficiency wins are real).
4. **Long ladder** (costliest; run only to validate ceiling after low rungs pass — confirm 1M is real, don't discover on it).
Total ≈ 400 cr ≈ 5% of Flash slice; leaves zcode scut undamaged.
