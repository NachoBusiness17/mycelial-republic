# SWEEP: kv-cache-context-engineering via X - 2026-10-01

source-fetched: 2026-10-01

Seat: sweep-kv-cache-context-engineering-x (frontier sweep gopher, Mag Resource Harness).
Doors used: WebSearch (Z.ai web_search_prime backend) for discovery; fxtwitter door
(`https://api.fxtwitter.com/<user>/status/<id>`) for resolution - resolved through both
WebFetch and the web reader; every banked item below was read end to end in this session.

## Coverage against the four research questions

**Q1 - prefix/prompt caching behaviors + byte-stable asks.** STRONGEST FIND:
ClaudeDevs "Reducing cost and improving performance with Claude Platform" (2026-09-08)
gives the frontier-API mechanics: exact-prefix matching, cache fork on any tool-set
change ("A change as small as one tool added or removed forks the cache"), fork-shared
cache inheritance for subagent-style sessions, 5-minute default TTL refreshed on hit with
opt-in 1-hour TTL, cache writes at 125% of base input, reads at 10%, cache diagnostics
exposed only in the Agent SDK, and "Pre-warm the cache by running one cheap turn over the
frozen prefix". This is the frontier-API sibling of the estate's byte-identical law
(corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md:10 - amend-cache keyed FNV-1a on
byte-identical ask text; memory/research_polished/kv_cache_compaction.md:9 - DeepSeek
hit/miss 50x/30x, append-at-END policy). Avi Chawla's KV article (2026-09-06) restates the
byte law independently: "Stable prompt templates therefore improve the hit rate."

**Q2 - structure-fed vs prose-fed (memweave numbers).** Two measured anchors:
(1) GoogleCloudTech "Loop Engineering for Sub-Dime Agents" (2026-09-21): "The biggest
cost driver in a coding agent loop is not the model. It is the loop's memory
architecture." - naive loop $1.53 vs pinned-prefix loop $0.042, a 36x cut from pinning
context prefixes and demoting tools to read-only MCP data. (2) talirezun "The Context
Engine" (2026-09-30): three kinds of context with three write rules - Foundations
(replaced whole, never model-summarized), Working state (supersedes), Knowledge
(accumulates): "state supersedes, knowledge accumulates. A wiki page unions its bullets."
Its capture measurement is the striking one: "From the installed skill alone: saved in 0
of 4 runs, with no error, no refusal and nothing on screen to tell you it had not
happened." - instruction block raised it to 3/4, lifecycle hooks to 4/4; the session
boundary, not the window size, is where context dies. That mirrors the estate's own
turn-2 no-echo carrier defect class (window 1) and the memweave feed-structures doctrine
(memory/rib/DOCTRINE_MEMWEAVE_20260810.md). Also: thegreatest_sv's JEV article (09-23)
quantifies structure-feeding economics (~$0.042/M input, 10k decisions = about $0.42,
compaction demos ~1M down to ~86k tokens in about a second) - concept ALREADY HELD
(memory/continuity/seat_memory_20260927/jev-system-one-decision-model-20260916.md,
9 catalog hits), banked only for the compaction numbers.

**Q3 - KV eviction/quantization at 2026 lengths + quality cost.** Ramp Labs "Scaling KV
Cache Compression to Frontier Models" (2026-09-28) is the measured centerpiece: on Claude
Sonnet 4.5 baseline accuracy dropped ~1.4 points at 10% compression but ~9.9 points at
50% compression (29,807-token prefix); Gemini 3 Pro held near-baseline through 30%
compression with KVzip but collapsed ~27 points under ComplexMCP on AIME 2025; DistillKV
takes the middle. Calibration for the estate: cheap-seat compressions must stay near the
10% regime or the judgment tier degrades silently. Kangwook Lee (2026-09-29) ships an
edge-deployed agent's compaction algorithm built for "a very tight KV cache budget (as
everything is running on the edge)" - the local janitor tier's shape. Avi Chawla's
taxonomy (GQA/MLA, sliding windows, Quest query-aware reads, KIVI/FP8 quantization,
H2O/SnapKV/PyramidKV eviction, PagedAttention, offload) is the raid-before-hand-rolling
map; estate overlap is partial (kv_cache_compaction.md:9 already holds RadixAttention
arXiv:2312.07104 + CacheGen/CacheBlend).

**Q4 - lost-in-the-middle at 2026 windows (context-pack budget).** Weakest lane of this
sweep: the X surface mostly recycles the 2023 Liu result and Chroma's context-rot testing;
no new measured degradation curve at 1M+ windows surfaced in-window. Dedupe catch: the
DeepLearning.AI memory-agent item (37.6% to 45.9% on Claude Sonnet 4.5 via structured
memory-agent notes) is ALREADY HELD - memory/research_polished/memory_engram.md carries
"Memory Agent gains (+8.3 / +6.8pp)" from the same underlying result - dropped as re-bank.
Context-pack budgeting therefore still rests on the estate's own kv_cache_compaction.md
line 6 (prefix-as-unit-of-economics) plus talirezun's session-boundary finding.

## Method and counts

- Pass 1: 7 WebSearch queries (site:x.com flavored), 429/1302 rate-limit storms on 5 of
  them (retried internally, 2 came back empty); ~55 unique candidate items surfaced, of
  which 10 fall strictly inside the last-30-days snowflake window
  (ID >= 2094575964779446272 = 2026-09-01; window floor computed by snowflake math in
  this session). Candidates outside the window were considered and filtered, not banked.
- Pass 2: 7 full end-to-end reads through the fxtwitter door (talirezun, GoogleCloudTech,
  RampLabs, ClaudeDevs, DeepLearningAI, Kangwook_Lee, thegreatest_sv - the last returned
  complete raw JSON) plus 1 fxtwitter+WebFetch read (avichawla article: title, preview,
  body opening). The DeepLearningAI read paid for itself as the dedupe catch above.
- Overlap greps run per candidate against catalog/catalog.jsonl and memory/
  (rg -i, phrases: "Context Engine", "Sub-Dime", "KVzip", "ComplexMCP",
  "cache diagnostics", "Pre-warm", "memory agent", "context compaction",
  "KV Cache Engineering for LLM Serving", "RadixAttention", "second brain",
  "System One"). Zero-hit phrases: Sub-Dime, KVzip, ComplexMCP, cache diagnostics,
  context compaction, "KV Cache Engineering for LLM Serving".

## Gaps (stated, not filled)

- LOCAL leg of Q1 is snippet-level only: llama-swap discussion #615 (--slot-save-path +
  POST /slots/{id}?action=save|restore), ollama issue #16635 (cache_prompt hardwired to
  context shift), particula.tech SWA/hybrid full-reprocessing fixes, llama.cpp
  discussion #20574 (host-memory prompt caching) - found via search, NOT deep-read this
  session; treat as OWED leads, not banked findings.
- No in-window X item gave a fresh measured lost-in-the-middle curve at 2026 window
  sizes; Q4 numbers remain the estate's own (kv_cache_compaction.md) until a paper-level
  sweep runs.
- Quotes for RampLabs and avichawla came through reader-door summaries of the fetched
  pages rather than raw page text; confidence on their exact wording is marked below.

## Banked items (strongest first)

1. ClaudeDevs - Reducing cost and improving performance with Claude Platform (2026-09-08)
   https://x.com/ClaudeDevs/status/2097369738968195513
   Quote: "A change as small as one tool added or removed forks the cache."
   Why: extends the ZCODE byte-identical playbook with the frontier mechanics it was
   guessing at - prefix-match-or-fork, fork-inherited cache for subagent fan-outs,
   5min/1h TTLs, SDK-only diagnostics, pre-warm-by-cheap-turn.
   Overlap: "cache diagnostics" 0 hits; "Pre-warm" hits are Descent-Protocol asks,
   unrelated; playbook anchor is corpus/steal (outside the grep roots) at line 10.
   Confidence 0.9.

2. GoogleCloudTech - Loop Engineering for Sub-Dime Agents (2026-09-21)
   https://x.com/GoogleCloudTech/status/2102176810029183478
   Quote: "The biggest cost driver in a coding agent loop is not the model. It is the
   loop's memory architecture."
   Why: a measured naive-vs-pinned loop cost table ($1.53 to $0.042, 36x) that gives
   memweave/context-pack a target number and a second source for prefix pinning.
   Overlap: "Sub-Dime" 0 hits; "Loop Engineering" catalog hits are unrelated
   watch-mining titles; DeepSeek 50x/30x economics already held at
   memory/research_polished/kv_cache_compaction.md:6,9 - this adds the loop-level table.
   Confidence 0.9.

3. Ramp Labs - Scaling KV Cache Compression to Frontier Models (2026-09-28)
   https://x.com/RampLabs/status/2104634941405266021
   Quote: "baseline accuracy dropped 1.4 points at 10% compression but 9.9 points at 50%
   compression"
   Why: the Q3 quality-cost curve for KV compression at frontier scale - calibrates how
   hard carrier echoes and cheap-seat compressions may be squeezed before judgment
   degrades (KVzip vs ComplexMCP divergence included).
   Overlap: "KVzip" and "ComplexMCP" 0 hits in catalog+memory. Genuinely new.
   Confidence 0.8 (quote via reader-door summary of the fetched page).

4. Dr. Tali Rezun - The Context Engine (2026-09-30)
   https://x.com/talirezun/status/2105241698716529044
   Quote: "From the installed skill alone: saved in 0 of 4 runs, with no error, no
   refusal and nothing on screen to tell you it had not happened."
   Why: three write rules (Foundations replaced whole / state supersedes / knowledge
   accumulates) plus the measured session-boundary capture failure (0/4 rising to 4/4
   with lifecycle hooks) - direct ammunition for memweave write rules and the carrier's
   turn-2 echo defect class.
   Overlap: 7 catalog "Context Engine(ring)" hits are generic playbook titles
   (catalogued 2026-09-04); memweave doctrine holds feed-structures; write-rule framing
   and the hook measurement are new.
   Confidence 0.9.

5. Kangwook Lee - edge agent technical report, context compaction under tight KV budget
   (2026-09-29) https://x.com/Kangwook_Lee/status/2104836549489905880
   Quote: "Since we have a very tight KV cache budget (as everything is running on the
   edge), we developed a very neat context compaction algorithm"
   Why: a working compaction algorithm shaped exactly like the estate's local tier -
   small budget, everything on-device - to raid before hand-rolling janitor compaction.
   Overlap: "context compaction" 0 hits; compaction-scored-by-typed-decisions doctrine
   held at kv_cache_compaction.md:6, this is the edge-budget instance. New.
   Confidence 0.85.

6. Avi Chawla - KV Cache Engineering for LLM Serving, clearly explained (2026-09-06)
   https://x.com/_avichawla/status/2096491130489872479
   Quote: "Loading an LLM is only the first part of GPU memory planning."
   Why: the 12-way KV-reduction catalog (GQA/MLA, sliding window, Quest, KIVI/FP8,
   H2O/SnapKV/PyramidKV, PagedAttention, offload) plus the independent restatement of
   the byte law ("Stable prompt templates therefore improve the hit rate").
   Overlap: phrase "KV Cache Engineering for LLM Serving"/"12 ways" 0 hits; partial
   overlap with kv_cache_compaction.md:9 (RadixAttention arXiv:2312.07104,
   CacheGen/CacheBlend already held); the technique catalog itself is new.
   Confidence 0.85 (quote via WebFetch read of the fxtwitter article payload).

7. thegreatest_sv - JEV: Your LLM's Second Brain (2026-09-23)
   https://x.com/thegreatest_sv/status/2102802378378621355
   Quote: "If it creates → LLM. If it picks / scores / gates → Jev. If it does the
   thing → code."
   Why: banked ONLY for the new bytes - compaction demos (~1M down to ~86k tokens in
   about a second) and the ~$0.042/M structured-decision economics; the concept itself
   is held.
   Overlap: HEAVY - memory/continuity/seat_memory_20260927/
   jev-system-one-decision-model-20260916.md + jev-salon2-fold-20260919.md + 9 catalog
   hits already hold the System One model. Re-bank risk acknowledged; kept for the
   measured numbers only.
   Confidence 0.95 (read from complete raw fxtwitter JSON).

## Residue for the next seat

- Deep-read the local leg: llama-swap #615, ollama #16635, particula.tech SWA fixes -
  the Ollama janitor cache behavior is exactly where mag.cmd context-pack lives.
- A paper-level (arXiv) pass for Q4 at 2026 window sizes; the X surface only recycles
  2023-era lost-in-the-middle and Chroma context-rot.
