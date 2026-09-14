# Probe 1 — Sparse/Linear Attention Boundary: INVALID (no boundary measured)
Date: 2026-09-01 10:37Z · Lane C · glm-5.3-flash · distances 512/4096/16384/32768 tok · 32K ctx
## Verdict
No valid boundary obtained. All 4 runs FAILED as instrumentation, not model recall.
## Failure signature: harness_leak_read_tool
Worker subagents had read/grep tool access and located the sentinel byte-exactly via search, not attention recall (dist 512 "verified via grep against file bytes"; 4096 "needle at line 285"; 16384 "tagged SENTINEL-OCTAGON in first section"; 32768 read truncated ~90KB, sentinel at token offset 118 = near top → trivial retrieval). Confidence ~1.0 reflects string lookup, not recall. Needle→query distance is irrelevant; the test measured subagent retrieval tools, not model sparse/linear attention.
## Does NOT establish
Any PASS/FAIL of the local-linear-state / sparse-global-window claim, or any boundary locus X. Do not treat as evidence either way.
## Required fix (re-run only after)
1. Feed ~32K prompt as immutable task payload string, OR revoke read/grep/find from the probe worker (pure-generation recall), OR grade strict free-form verbatim recall.
2. Keep fixed 32K ctx, same 4 distances. Cost unchanged (~0.69 cr/call).
3. Incurred: 4×0.69 = 2.76 cr (receipted). Cap 400 cr unaffected. No bail triggered.
## Receipts
/board/salon_glm53/lane_c_probe_receipts.jsonl (4 rows, all outcome=FAIL, ts 10:37Z).
