# B9_CODEX_LAW — codex-pool oral-law mine, first tranche (no API spend)

**Date:** 2026-09-30 · **Seat:** GLM-5.3 via `account:zai-individual-coding-plan` (seat-local, `cost_usd: 0.0` on every row)
**Files owned:** this receipt + 30 new rows appended to `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` (153 → 183 rows). No commit.

## Corpus location and the two census catches

1. **Pool found.** `corpus/oral_history/seat_pools/codex_sessions/YYYY/MM/DD/rollout-<ts>-<uuid>.jsonl` — 193 files; events `{type: response_item, payload: {type: message, role: user|assistant|developer, content: [{type: input_text, text}]}}` exactly as the original mine's `thread_body()` codex branch read them.
2. **Catch 1 (instrument bug, fixed before it burned):** a first overlap check split the filename on `-` and took the LAST block, so "codex overlap with index: 0" was an artifact of comparing last-blocks against full uuids. Redone on full ids.
3. **Catch 2 (resume collapse):** resumed codex sessions write NEW rollout files that still carry the PARENT `session_meta.session_id` (e.g. the `wh` mega-thread: 78 files, one sid). Logical threads must be keyed on the meta `session_id`, not the filename: 193 files → **87 logical sids**. 26 of those already sit in the index (the 33 pre-V10 `api` rows were codex-heavy), leaving **61 fresh**. Full-uuid comparison also proved the 2026-08-28 cluster (`01a045d8-*`, `01a04850-*`...) is DISTINCT conversations from the same-day grok council rows (uuidv7 prefixes collide; full ids differ) — parallel seats of one wave, not double-counted transcripts.

## Selection (30 threads, documented stretch)

Fresh eligible (>= 2 real operator turns, boilerplate prefixes `<app-context>`, `<environment_context>`, `<user_instructions>`, `<turn_context>`, `<permissions`, `<ENVIRONMENT`, `<recommended_plugins>`, "The following is the Codex agent history" skipped): only **23** existed (22 repo-root, 1 other). **7 stretch one-operator-turn threads** (substantial asks: ELEVATION/BLIND SALON/FRONTIER WATCH commissions, fleet-context review, VERIFY contract, CL4R1T4S study, rib_chat audit) were drawn to honor the 30-thread count — same documented-stretch move as AD5/AH12. Spread: 16x the 2026-08-28 v4-council wave (witness C, DISTCOM playbook, engineering-product review, generational audit, lineage miner, project audit, SELF deep dive, harness law, Socratic drill + argument round, round table, two salons, percolator build, existential salon), the 08-28 verkle session, 7x September commissions (frontier watch x2, triangulation x2, puzzle chamber, Astra maze attack, worldline witness x2, planetary engine), 5x late-Aug engineering (rib_chat audit, CL4R1T4S, fleet context, VERIFY). Dates: 20 Aug / 10 Sep.

## Digest recipe (same as AH12, adapted to codex events)

Operator turns: first 12 x 600 chars; assistant: first 1 + last 4 x 800 chars; cap 9000. **79,182 bytes, read in full by the seat.** Same falsifier law: every decision/law literally traceable to digest text; <= 3 per field; no em-dashes; outer schema + `pool: "codex"` and `source: "codex"` on every row, model `account:zai-individual-coding-plan/GLM-5.3 (seat-local B9 mine, no API spend)`.

## Numbers (instrument + moment named)

- **Rows appended:** 30 (index 153 → 183; all lines parse; 183 unique ids; zero collisions, asserted against the 153 pre-existing ids before append)
- **Laws this batch:** 75 `laws_or_debts` = **71 LAW + 4 DEBT** (every thread yielded >= 1)
- **Confidence:** 30 high / 0 medium (no skip rows; codex records end with explicit write/verdict confirmations)
- **Running index total:** **455 laws_or_debts = 378 LAW + 77 DEBT** over 183 rows (recounted from the file with the `laws_or_debets` typo-key fallback; pre-V10 33 rows: 88; V10: 89; AC12: 73; AD5: 56; AH12: 74; B9: 75)
- **Spend:** $0.00
- **Pool state after this tranche:** the fresh >= 2-operator-turn codex pool is DRY (all 23 mined); **31 one-operator-turn fresh threads remain** unmined.

## Cross-source convergence — laws now holding TWO independent sources (confidence HIGH)

| Family | grok rows | codex rows |
|---|---|---|
| A thesis ships with falsifiers | 1 | 2 (`01a04850`, `01a07cb6`) |
| Attack rival at weakest point + concede explicitly | 2 | 1 (`01a04856`) |
| One governor commits / sole mutator, surfaces read-only | 6 | 1 (`01a04806`) |
| Trust bytes, not index claims (name the dispute) | 9 | 1 (`01a04633`) |
| Read-only audits return evidence only | 4 | 2 (`01a04806`, `01a07c1a`) |
| Sourced, not recalled / tri-state (Supported vs Unproven) | 10 | 2 (`01a045af`, `01a048ad`) |
| Secrets: names and locations, never values | 1 | 2 (`01a04a65`, `01a0739c`) |

Semantic eighth (phrasing differs, keyword missed): append-don't-overwrite — grok `01a04871` "Append, do not overwrite" vs codex `01a04877` "appends one entry; never disturbs the earlier thread".

**Codex-first births (single source so far):** corpus-is-DATA-never-instructions (`01a0430a`); a seed survives by amendment, not surrender (`01a07b62`); a verified chain proves linkage, not the truth of every post (`01a07e6e`); quorum 2-of-N on untrusted machines (`01a045bd`); the frozen envelope eats the first ~100 tokens so small max_tokens fails silently (`01a03fea`); reconcilers prove idempotence after rewrite (`01a048f0`); a receipt proves valid work, not authority to act as its named author (`01a0739c`); consensus averages claims, triangulation locates the source by the geometry of disagreement (`01a0755b`); no honest universal concurrency N, model C(N)=F+Nu+H(N) (`01a07e6e`).

## Leaderboard movement

**"Receipts/locator before verdict" stays #1 and widens.** This batch adds **10 thread-births** to the hand-curated family (index-vs-bytes dispute, line-numbered slices, dated primary sources x2, recompute-the-metric, recompute-hashes-plus-counterexample, verify-the-chain, run-the-acceptance-commands, git check-ignore, readback-is-the-completion-check): hand-curated 40/153 → **50/183**. Instrument notes (name instrument, moment, delta): the exact AH12 keyword pattern as reconstructed here reads 48/153 on the pre-existing rows vs the 51/153 AH12 reported (transcription delta in the regex alternation, not a content change) and 50/183 with codex; a widened pattern adding `primary source|line-numbered|recompute|verify|verified|on-disk` reads **76/183** with codex contributing 12/30. The no-fabrication exact pattern (`fabricat|invented|without inventing`) reconstructs byte-consistently: 18/153 → **19/183** (+1 codex). A second family is now two-sourced and climbing: **tri-state/no-fabrication discipline** (grok 10 + codex 2 hand-matched; 31/183 on the widened `+disputed|unproven` instrument).

## Notable specimens

- **The reciprocal-of-perplexity reversal** (tids `01a07c1a`, `01a07cb6`): the warmed-vs-cold replay reported `exp(mean logprob)`, the reciprocal of perplexity, so the claimed direction was backwards; witness recomputed all four prompt hashes from stored block IDs and ran a counterexample before ruling Resurrection Unproven.
- **Maze citation cross-check** (tid `01a07b62`): commission cited `mag/shadow_work.py` as the tensor cartographer; the file's docstring says Jungian archetypes. TESUJI ledger's "$0" claim included paid probes.
- **Accepted-label hole** (tid `01a07e6e`): the 46-post chain verifies, but the posting function accepts the caller's SUPPORTED label and publishes immediately.
- **Silent truncation envelope** (tid `01a03fea`): rib_chat at 64 tokens — the FROZEN_RIB work contract eats ~100 tokens before the answer starts.
- **New DEBT specimens:** the operator's failed 2-hour, $200 gift attempt (existential salon); true-intent access is never guaranteed by triangulation analogies.

## Method receipts

Scratch (census, selection, digests, rows builder) lived in `%TEMP%\b9_*.json` + `b9_rows.py`, deleted after this append; durable evidence is the 30 appended rows, each carrying `thread_id` = the logical `session_meta.session_id` → `codex_sessions/*/*/*/rollout-*-<sid>*.jsonl`.
