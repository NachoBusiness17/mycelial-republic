# Y6 - N5 REFIRE: the oral-law-schema gopher, second burn (2026-09-29, lane 6/12)

- **v1 failure (night burn 2026-09-30 file, fired 09-29):** finish=length, $0.1411, 142s, content = one word ("Below"). Reasoning 6000 starved output. Receipt: `watch/inbox/hydrology/X5_NIGHT_READ.md` section N5.
- **v2 fix applied:** reasoning cap 3000, max_tokens 8000, same ask reframed ("critique this working schema against what a 12k-thread scale-up needs") + first 3 rows of `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` pasted verbatim + the surviving v1 reasoning-tail fragments (dedupe/audit sub-schemas) salvaged in, per the X5 re-fire order.
- **v2 result:** finish=**stop**, **$0.0191**, 21.4s, 7,315 chars, seat `z-ai/glm-5.3-prime`. 86% cheaper than the truncated v1. Budget $0.30 respected. Raw row (prompt_chars, reasoning_tail, full content): `logs/mates/n5_refire_20260929.jsonl`. 0 em-dashes.
- **Byte-verified against the live 33-row index:** `laws_or_debets` typo real (2 occurrences, row 2); 88 law/debt entries with 0 evidence pointers; confidence = 25 high / 5 med / 3 none.

## What N5 v2 says that matters for the 12k scale-up

1. **Identity is per-thread, not per-law.** `thread_id` is the only key; the same law surfacing in hundreds of threads has no join key. Dedupe needs `law_text_normalized` -> `law_key_hash` with a deterministic normalization (lowercase, strip LAW:/DEBT: prefix, punctuation-fold), else ~4k phantom unique laws at 12k.
2. **No evidence pointers = the single worst field.** Every law is assertion-only; at 12k, unverifiable assertions are indistinguishable from confabulation. Required: `evidence: [{source_file, line_span|msg_index, quote}]` resolvable against `session_index.jsonl`. Verified: the live index has zero.
3. **Confidence is saturated and self-graded.** All-first-3 "high"; across all 33 rows 76% high (so the live index already fails N5v2's own predicate 5: no grade over 70%). Needs a rubric (grade + basis) with `verifier_model != model` as a hard constraint, not convention.
4. **No scope field.** Without `scope: ephemeral|project|constitutional`, session trivia (row 1's path-name "decisions") drowns constitutional law at 12k. Rank: evidence > normalization > scope > conflict resolution > confidence rubric > extractor_version/prompt_hash > lifecycle status > session_type.
5. **Conflict resolution needs `ts`.** Salvage `superseded_by` is inert without temporal ordering and a resolution rule; every `conflict_with` pair must resolve or flag `needs_review`.
6. **The falsifier (UNPROVEN at any scale today):** blind cross-model ground-truth on N=200 sampled laws (verifier sees only source+span), 20 synthetic law-free negative controls, cross-model re-run of 500 threads, and a zero-law thread prefix test (row 2's typo'd field shows the schema pressures the model to fill fields). Pass: <5% confabulation, 0% on negative controls.
7. **Acceptance test, 10 JSONL-checkable predicates:** schema integrity (zero `laws_or_debets`), 100% evidence coverage, dedupe closure (unique active <15% of raw), zero unresolved conflicts, confidence entropy >1 bit, temporal coherence (no back-edges), >=5% audited by a different model, zero laws from negative controls, scope separation, sublinear cost scaling.

**Salvage verdict:** the v1 fragments were directionally right but inert (hash without normalization, audit without verifier independence). Nothing needs rebuilding; everything needs wiring.

- Fired by `watch/inbox/hydrology/.tmp_n5_refire.py` (deleted post-run; script posture: pinned host, redirects refused, budget guard).
