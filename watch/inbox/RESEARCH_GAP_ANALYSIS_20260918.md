# RESEARCH GAP ANALYSIS — what we need and what it buys (2026-09-18)

*Method: every harvested research piece walked into the knowledge graph (19
families / 158 edges, Librarian-annotated), then the LINKS ledger + pack index
mined for domain coverage, then each thin domain mapped to an operation that
is currently running WITHOUT its research floor.*

## COVERAGE (245 LINKS rows + 107 packs, keyword-domain pass)

Dense: x-social/intel 138 (56%) · fleet-history 71 · retrieval 36 ·
finetune 34 · mesh 30 · games 27 · prompt-cache 18.
**Thin (the gaps):** security/keys 9 · steering/persuasion 9 · esoteric 7 ·
windows/storage 4 · swarm/orchestration 4.

## THE GAPS → OPERATIONAL PAYOFF (each seeded as a lane dig)

| Gap | Rows | Operation starving for it | Payoff if filled |
|---|---|---|---|
| Steering/priming prior art in LLM agents | 9 (mostly our own posts) | retrocausal-steering + memlance (5-lance falsifier pending) | real priming/ICL-steering studies → lance design that hits; hit-rate baseline from literature |
| Multi-agent comms protocols | 30 but zero on A2A/AutoGen/CAMEL schemas | mesh-comms skill + lane registry (Librarian build #6) | message schemas + capability discovery we can adopt instead of inventing |
| Swarm orchestration economics | 4 | union driver (B2-322 byte refresh 2026-09-26 from raw.jsonl: 184 attempts, 156 ok = 84.78% ok, 128 unique completed ids of 131 touched, 1.438 attempts per completed dig; the 143 attempts/88.8% this cell carried since 2026-09-18 was stale) | production retry/fallback/fanout patterns → driver v2, cost per completed dig |
| Prompt-cache invalidation per provider | 18, no provider matrix | CONTEXT OS + the undefined **kernel amendment ceremony** | exact invalidation/keepalive rules per provider → the kernel upgrade path the socratic audit found missing |
| Windows reparse/storage law | 4 | catalog v3 (junction pruned 189K rows, mirror-vs-duplicate untested) | reparse-point handling + MFT-style enumeration → junction policy + fast refresh |
| Secret-scanning/rotation | 9 | dossier sanitization (pending) + 60 filed artifacts never key-scanned | CI-grade scanning patterns → estate hygiene pass |
| QLoRA on small reasoning corpora | 34 generic, thin on latest | Rocinante Oct 27 (9,305 reasoning parts) | current best practice → thought-bank pipeline design |
| Retrieval eval design | (UF-122 pending, undrained) | mining gate (constitution: no auto-merge) | the 50-question eval that gates ALL mining |

## PER-ROW CENSUS (B2-322, 2026-09-26: every gap row above re-checked against
## its named artifact bytes; landed = the starving operation's floor now exists)

- Swarm orchestration economics: STALE denominators refreshed in place this
  census (184/156/84.78 pct/128-of-131/1.438, derived from
  watch/inbox/union_fullsend_20260917/raw.jsonl bytes).
- Prompt-cache invalidation per provider: LANDED 2026-09-26. The "no provider
  matrix" hole is closed: 4 verified LINKS rows (writer zcode-sw-10-b2-340)
  with byte-quoted prefix/invalidation/TTL/pricing for anthropic, openai,
  google, zai; receipt
  watch/inbox/burn_wave_20260926/B2_340_prompt_cache_matrix_20260926.md.
- Multi-agent comms protocols: PARTIALLY FED. A2A no longer zero (1 LINKS hit;
  hands-on receipt watch/inbox/A2A_FIRST_PROBE_20260925.md); AutoGen and CAMEL
  schema rows still 0/0 (LINKS.jsonl bytes, 345 rows at census).
- Steering/priming: row's floor still pending (5-lance falsifier); LINKS
  keyword recount under the census patterns below gives 3 vs the 9 of the
  2026-09-18 pass (different keyword set, census drift named not overwritten).
- Windows reparse/storage law: row stable (4 then, 4 now), floor still owed.
- Secret-scanning/rotation: floor still owed; keyword recount 2 vs 9 (same
  census-drift caveat).
- QLoRA small reasoning corpora: partially fed by the B2-74 redo receipt
  (5 fetched sources quoted, on disk); Rocinante Oct 27 unchanged.
- Retrieval eval design: STALE, still owed. No UF-122 artifact found on disk
  (watch/inbox sweep 2026-09-26), so the mining gate still runs unevaluated.
- Keyword-recount method (comparable only to itself): case-insensitive regex
  over each full LINKS row's JSON, patterns steering|priming|persuasion;
  a2a; autogen; camel; swarm|orchestrat; reparse|junction|MFT; qlora|lora;
  retrieval|rag. LINKS.jsonl held 345 rows at census (2026-09-26).

## THE LIBRARIAN'S BUILD ORDERS (from the graph annotation — 8, all accepted as candidates)

standing receipt writer · edge→doctrine compiler · imprint refresher ·
family-descriptor backfiller · receipt→biography joiner · lane registry ·
**audit→amendment loop** (closes the socratic audit's sharpest gap) ·
canon↔shadow diff (answers "intentional mirror vs duplicate").

## THE ARC THIS ANALYSIS NAMES

The ledger's 56% X-weight is the seat watching the world; the thin domains
are the seat watching itself. Every thin row is a domain where we are
**running an operation on intuition instead of prior art** — that is the
definition of research debt.

## DISPATCHED

UF-124..UF-131 appended to the union queue (one dig per gap, each with the
operation it feeds named in the prompt). Receipts land in
`watch/inbox/union_fullsend_20260917/raw.jsonl` as they drain.
