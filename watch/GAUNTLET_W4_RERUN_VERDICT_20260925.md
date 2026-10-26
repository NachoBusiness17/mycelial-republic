# GAUNTLET W4 RERUN - VERDICT (fired 2026-09-25/26Z, filed same session)

**VERDICT: PASS. All three rerun conditions from GAUNTLET_W4_VERDICT_20260925.md met; preregistered criterion 6 (GAUNTLET_PREREGISTRATION_20260901.md): MET on n=50 valid tails per arm.**

Preregistered bar: steering obedience at warm cache within 5pp of cold (FAIL if warm degrades >5pp), cachedTok >= 95% of prefix size across >= 50 varied tails.

## Recount (deterministic, from watch/gauntlet_w4_rerun_receipts.jsonl - 100 rows, recounted by watch/w4_rerun_recount_20260925.py, independent of the harness summary)

| arm | trials | HTTP-200 | obey | obey rate (valid) | cacheFloorOk (valid) | cachedTok dist | promptTok range |
|---|---|---|---|---|---|---|---|
| WARM | 50 | 50 | 45 | **0.90** | **50/50** | 4864 x50 | 5085-5100 |
| COLD | 50 | 50 | 42 | **0.84** | 0/0 (n/a by design, null) | 256 x50 | 417-432 |

- Obedience delta: **+6pp warm-vs-cold** (warm above cold; FAIL bar is >5pp degradation) -> clause MET.
- Cache floor: cachedTok = **4864 on every warm valid row** (76 x 64-token blocks), >= 4800 preregistered floor and >= 95% of the ~5086-token prompt -> clause MET, zero rebuilds across 50 tails.
- Models: `{"deepseek-chat": 100}` - every row carries the correct model id (rerun condition (a)).
- No duplicate trial+mode keys; both warmup ctrl calls present on all 50 WARM rows.

## The three owed fixes (from GAUNTLET_W4_VERDICT_20260925.md)

1. **Model-id bug (a): FIXED.** Harness sets `MODEL = "deepseek-chat"` (watch/w4_rerun_harness_20260925.py); receipts confirm 100/100 rows model=deepseek-chat. The 09-01 bug (env-var name "DEEPSEEK_API_KEY" passed as the model, 40/60 rows invalid_request_error) is gone: 100/100 rows HTTP-200.
2. **>= 50 tails per arm (b): MET.** 10 preregistered instruction types x 5 wording variants = 50 varied tails per arm, predicates byte-faithful to the READY doc table (T01..T10). 50/50 valid per arm.
3. **cacheFloorOk null on non-200 rows (c): FIXED in the writer; not exercised by data.** The run produced zero non-200 rows, so no receipt row demonstrates the error path. Verified instead by: the harness code path sets null on every non-200 row (fire result http != 200 branch), and 50 COLD rows carry cacheFloorOk=null (floor n/a to the cold control), proving nulls are written where they should be. Stated honestly: this fix is code-verified, not data-verified.

## Prefix calibration (protocol note, fixed before the valid run fired)

The READY doc's byte estimate (`cache-me-now-2026...` x380 = "approx 4872 tok") does not reproduce on the current tokenizer: x380 measures promptTok 3085 (prefix ~3045 tok, cached 2944 = 46 blocks). Running on those bytes would have tested a ~3K prefix, not the preregistered 4.8K one, and reported a false cache-floor FAIL (first pass did exactly that; archived as gauntlet_w4_rerun_receipts_PREFIXCALIBRATION_ABORT.jsonl). Recalibrated by probe **before** the valid run: **x630 reps measures promptTok 5086, cachedTok 4864 (76 blocks)** - matching the 09-01 run's own measured cachedTok=4864 and honoring the preregistered constant (~4.8K prefix, floor 4800). The rep count was an implementation estimate; the preregistered quantity (prefix size >= 95% floor) is unchanged. Cost of the aborted pass: ~$0.011.

## Honest reading

With the protocol valid and n at the preregistered scale, warm-cache steering obedience is **not degraded** (+6pp, warm 0.90 vs cold 0.84) and the frozen prefix holds 4864 cached tokens on 50/50 tails. The 09-01 valid-subset signal (warm 0.70 vs cold 0.80, -10pp on n=10) does not survive at n=50 - that direction was small-sample noise. The static/dynamic boundary leak W4 hunted is **not present** under this protocol. Caveats: (i) temperature 0.2 / max_tokens 300 are rerun choices; the 09-01 run's sampling config was not recorded in its receipts; (ii) COLD cachedTok=256 shows a small real hit on the shared system+header head (4 blocks) - the cold control is a miss relative to the 4.8K prefix, which is the comparison that matters; (iii) binomial noise at n=50 is roughly +/-7-8pp, so the +6pp direction should not be over-read; the criterion only requires warm within -5pp.

## Cost

Valid run: 200 planned provider calls (150 WARM incl. 2 warmups per trial + 50 COLD), 0 retries needed, $0.0287 total per harness spend ledger ($0.0109 of that on the 50 steered WARM + 50 COLD receipt rows; the rest on the 100 warmup ctrl calls). Pennies, inside the <= ~250-call brief.

Evidence: watch/gauntlet_w4_rerun_receipts.jsonl (append-only, 100 rows) + watch/gauntlet_w4_rerun_summary.json + watch/w4_rerun_harness_20260925.py + watch/w4_rerun_recount_20260925.py. Supersedes the rerun-owed clause of GAUNTLET_W4_VERDICT_20260925.md; criterion 6 now reads PASS at preregistered n.
