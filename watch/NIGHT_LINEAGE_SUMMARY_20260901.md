# LINEAGE GEN C — S1 BATTERY RUN SUMMARY (2026-09-01)

Battery: `/board/lineage_battery_v1.json` (frozen, VALID, sha256 `59568b3178c5442e…` verified).
Comparison baseline: `/board/lineage_run1_genB.md` (glm-5.3-flash, run 1) + `/board/lineage_run1_sheet.md`.
Run window: 05:50Z – 06:24Z. Scorer runs at S5 (09:30Z) — this file is the raw receipt pack, not the wavelength matrix.

## Lane receipts (per-lane files)
| lane | file | model | probes | http-ok | text-nonempty | empty | failed | cause of deficit |
|---|---|---|---|---|---|---|---|---|
| deepseek | `lineage_genC_deepseek_20260901.md` | deepseek-v4-flash | 20 | 20 | ~20 | 0 | 0 | — (complete) |
| groq | `lineage_genC_groq_20260901.md` | openai/gpt-oss-120b | 20 | 20 | 18 | 2 | 0 | 0 after 1 retry (TPM cleared); 2 empty-content |
| nvidia | `lineage_genC_nvidia_20260901.md` | deepseek-v4-flash-0731 | 20 | 20 | ~10 | ~10 | 0 | many probes empty-content (kept as finding) |
| together | `lineage_genC_together_20260901.md` | DeepSeek-V4-Flash-0731 | 20 | 20 | ~12 | ~8 | 0 | many probes empty-content (kept as finding) |
| cerebras | `lineage_genC_cerebras_20260901.md` | gpt-oss-120b | 20 | 5 | 5 | 0 | 15 | HTTP 429 persistent (2 strikes) — rate/NOISY-NEIGHBOR gated |
| openrouter | `lineage_genC_openrouter_20260901.md` | google/gemma-4-26b-a4b-it:free | 20 | 0 | 0 | 0 | 20 | Provider returned error (all 20) — free fleet broken tonight |
| zai-lite | `lineage_genC_zailite_20260901.md` | glm-4.7-flash | 20 | 7 | 0 | 7 | 13 | 13 overloaded; 7 http-200 but empty-content |

## Lane availability verdicts (S1 deliverable)
- **deepseek**: fully healthy, complete answers, best yield. **PRIMARY** for quality+availability.
- **groq (gpt-oss-120b)**: healthy once TPM clears; 18/20 non-empty. **Available $0 lane**, occasional TPM fence.
- **nvidia / together**: both run the deepseek-v4-flash-0731 model; substantial empty-content on socratic/hot/hard probes raw. Empty-content is a measured QUALITY signal (truncation/empty at temp 0 max_tokens 500) — flag for scorer.
- **cerebras (gpt-oss-120b)**: heavily rate-limited tonight (429). **UNRELIABLE under load** — 15/20 two strikes. Qualify: usable only off-peak of shared quota.
- **openrouter free fleet**: **DOWN tonight** — 20/20 provider error on the chosen free representative; earlier llama-3.3-70b:free slug 404. Free fleet not a dependable S1 lane this window.
- **zai-lite (glm-4.7-flash)**: 7 http-200 but all empty, 13 overloaded. **Rate/overload gated**; paired with S2 cache findings (401/1305) — Lite needs key/auth + pacing review.

## Request-shape note (scorer must read)
Gen B sheet used `system:"Answer directly, no preamble."` + `max_tokens:300`.
Gen C S1 (this pack) used NO system prompt + `max_tokens:500`. Empty-content is partly attributable to this shape difference, partly to lane health. Scorer should not treat the two shapes as directly apples-to-apples without the caveat.

## Honest labels
- All numeric claims above are MEASURED from HTTP responses in the per-lane files.
- "text-nonempty" approximations (nvidia/together) marked ~ — exact counts readable in each receipt.
- No paid spend on S1 lanes tonight (all $0/free/plan); the only paid rows are the S2 probes already in cost_gate_ledger (together $0.00448, ds smokes <$0.01).
