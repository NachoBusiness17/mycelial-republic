# GAUNTLET W4 — VERDICT (filed 2026-09-25, owed since 09-01)

**VERDICT: FAIL (preregistered criterion) + INVALID (protocol). Cache-floor sub-claim SUPPORTED on the valid subset.**

Preregistered bar (GAUNTLET_PREREGISTRATION_20260901.md, criterion 6): steering obedience at warm cache ≥ obedience at cold, cachedTok ≥ 95% of prefix size, across **≥50 varied tails**; FAIL if obedience degrades >5pp warm-vs-cold or the cache rebuilds.

## Recount (deterministic, from watch/gauntlet_w4_receipts.jsonl — 60 rows, recounted by script at filing time)

| arm | trials | HTTP-200 | obey | obey rate (valid) | cacheFloorOk (valid) |
|---|---|---|---|---|---|
| WARM | 30 | 10 | 7 | **0.70** | 10/10 |
| COLD | 30 | 10 | 8 | **0.80** | (vacuous on error rows) |

- Obedience delta: **−10pp warm-vs-cold** → preregistered FAIL bar (>5pp) crossed → **criterion FAILED**.
- Protocol invalidity 1: **n=10 valid trials/arm vs the preregistered ≥50** — the run could never have satisfied its own sample-size clause.
- Protocol invalidity 2: **40/60 rows carry model="DEEPSEEK_API_KEY" (20 per arm)** — the env-var NAME was passed where the model id `deepseek-chat` belongs → two-thirds of all trials were structurally broken (`invalid_request_error`), not model behavior. *(Correction 09-25: an earlier draft of this doc said 20/60; the fold's byte-check caught it — the errcode counts are 20 per arm, 40 total.)*
- Writer bug found at recount: HTTP-400 rows are written with `cacheFloorOk: true` (cold rows with no warmup are vacuously "true") — inflates the cache metric on error rows. Fix owed: `cacheFloorOk: null` on non-200 rows.

## Why it lay unfiled 24 days

The run summary reported "20/20 ok" from the valid-subset view, and no run-summary schema required a verdict row. Gap closed today: verdict field rendered by `tools/fold_mickey17.py` summaries; grounding-wave rows already carry a verdict key.

## Honest reading

Warm-cache obedience degraded on **every valid pair measured** — the static/dynamic boundary leak W4 was hunting is real in direction — but n=10/arm cannot rate the effect size, and the cache-floor half held 10/10. W4 stays **FAILED-and-INVALID**: rerun owed with (a) the model-id bug fixed, (b) ≥50 tails per arm, (c) `cacheFloorOk: null` on non-200 rows. Until the rerun, cite this verdict, not the "20/20 ok" summary.

Evidence: watch/gauntlet_w4_receipts.jsonl (append-only) + GAUNTLET_PREREGISTRATION_20260901.md criterion 6.
