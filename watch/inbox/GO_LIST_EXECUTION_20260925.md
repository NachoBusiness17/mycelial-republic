# GO-LIST EXECUTION RECORD — 2026-09-25

Operator: "do what is needed" → the MICKEY-17 v2 master fold's GO list, executed same session. Four of ten rows closed, two organs patched, one negative-result instrument fired.

## P0 — Sonar sunset sweep (deadline 2026-09-27): CLOSED, nothing live to remap

- Sweep: exactly ONE estate lane on a Sonar chat-completions endpoint: `mag/perplexity_research.py:38` (`api.perplexity.ai/chat/completions`). Other "perplexity" hits are browser-frontend seats (perplexity.ai web UI — unaffected by an API sunset).
- **The module is DORMANT: zero `PERPLEXITY_API_KEY`/`PPLX_API_KEY` in .env** — it has never made a live call from this estate. Nothing breaks on 09-27.
- Action taken: loud deprecation guard added (`SONAR_CHAT_SUNSET = "2026-09-27"`); after that date `research()` refuses the endpoint and names the remap path (Search API `$5/1k std / $1/1k fast`, or Agent API). Compiles clean.
- Sunset claim itself verified: perplexity-lab lane row "Perplexity retires Sonar Chat Completions on 2026-09-27" (MICKEY-17 v2 burn, lane JSON on file).

## P1 — W4 verdict FILED (24 days late) + summary schema patched

- Deterministic recount of `watch/gauntlet_w4_receipts.jsonl` (60 rows): **warm obey 0.70 vs cold 0.80 on the valid subset (10/arm) = −10pp, preregistered FAIL bar was >5pp → criterion FAILED.** Run also protocol-INVALID: n=10/arm vs preregistered ≥50, and **40/60 rows (20 per arm)** structurally broken by `model="DEEPSEEK_API_KEY"` (env-var name passed as model id). Cache-floor sub-claim SUPPORTED 10/10 on valid trials. Writer bug found: 400-rows carry `cacheFloorOk: true` (should be null). *(Count corrected 09-25 from 20/60 — caught by the spec-steal fold's byte-check, the A5 class aimed at its own author.)*
- Verdict filed: `watch/GAUNTLET_W4_VERDICT_20260925.md` (full recount + rerun conditions).
- Hash-chained ledger row appended to `watch/GROUNDING_WAVE.jsonl` (row 125, DISPUTED, hash `d540522bbdcb` ← prev `d2c81c2dc98a`…). **Chain hash function identified by round-trip: sha256 of the row JSON (hash field excluded), sorted keys.** Correction owned: my first append used a concat-variant hash; fixed to canonical form seconds later (own row, not history). The md view (`dashboard/static/grounding_wave.md`) had drifted 3 days behind the jsonl — new row re-stitches it to the authoritative chain; full view resync still OWED.
- `tools/fold_mickey17.py` patched: summaries now emit a VERDICTS section (counts per verdict + loud unverified-row warning) and render per-row verdicts. The W4 disease ("20/20 ok" shipped with no verdict) is structurally closed.

## P2 — Nous/Hermes lane WIRED and proven ALIVE

- `hermes proxy` path: **BLOCKED on credentials, not code** — both upstreams "not logged in" (Nous Portal OAuth needs an operator browser login = operator hand). Receipt on file; do not re-attempt without login.
- Static-key rescue instead: `mag/free_tier.py` registry now carries a `nous` lane — `HERMES_API_KEY_1`/`HERMES_API_KEY_2`, base `inference-api.nousresearch.com/v1`, openrouter-style catalog (~40 models: `z-ai/glm-5.3-prime`, `qwen/qwen3.8-max-prime`, `fireworks/ember-1`, `openai/gpt-6-luna`, cohere, upstage…). Accepts both key names (the NVIDIA-mismatch lesson).
- **LIVE RECEIPT: chat completion on `z-ai/glm-5.3-prime` via key 1 returned a real completion object** (200, gen id `gen-1790339555-…`). Gotcha receipted: reasoning models burn a small `max_tokens` on thinking — size the cap or disable reasoning, same fix the OpenRouter lanes got.
- Still OWED (small): wire a caller (fuel_feed/task-wall lane table) so chores can route through `nous`; probe whether Portal tiers expose the free Perplexity Fast Search endpoint to these keys.

## P3 — Verbatim audit of judge evidence_quotes: honest n=0

- Census: `evidence_quote` appears in exactly ONE watch/inbox file (`BURN_JUDGE_LANE_BUILD_20260925.md`), 3 occurrences — **all three are schema-template placeholders ("verbatim"), not real quotes.** The estate holds zero populated judge records in watch/inbox today.
- Verdict: hit-rate n/a (0 audited, 0 failed). The byte-grep audit pattern is proven (it is what the MICKEY-17 verifier lanes ran at width); it re-fires the day judge lanes populate. The instrument is ready; the population does not exist yet.

## Not done (remaining GO rows, in fold order)

Tool schemas with write-tools stripped at fan-out (needs the runner layer); WANDR-shaped self-eval task; tool-result freshness receipts (`tools/freshness_check.py` extension); MCP tool-schema hash pinning; ~~DeepSeek off-peak scheduling + 120x→30x cache-ratio correction~~ (CLOSED 09-25 late, see addendum below); Anthropic effort-tier budgets. Each is spec'd in `corpus/steal/MASTER_MICKEY17_V2_20260924.md` §6.

## Addendum 2026-09-25 (late session): GO row 9 CLOSED

DeepSeek off-peak scheduling + 120x→30x cache-ratio correction: executed by a separate seat. Burn scheduler notes patched (`memory/burns/MANIFEST.json` protocol now carries `deepseek_windows`: paid DeepSeek work fires outside 01:00-04:00 / 06:00-10:00 UTC Mon-Fri, excluding Chinese public holidays; prefer deepseek-flash, off-peak cache-hit $0.003/1M). Stale pro cache ratio corrected to 30x across the living estate surfaces (kv_cache_compaction.md, deepseek_api reference docs, kv50 card, config/code comments), with sealed archives and dated records left byte-intact by class. Full census classification, verification commands, and the one owed follow-up (pro absolute prices in `mag/cache_map.py`/`tools/tier_probe.py` need a live pricing re-pull before editing) are in `watch/inbox/DEEPSEEK_OFFPEAK_CACHE_RATIO_RECEIPT_20260925.md`.
