# sweep: kv-cache-context-engineering via x, 2026-10-05

source-fetched: 2026-10-05. Window: 2026-09-05 to 2026-10-05. Area feed: lmcache-src shelf
(catalog 2,339 rows matching "lmcache", mostly the source import), the B4 KV sweep, and the
descent protocol's prompt-shape leg (mag/claritas.py + deterministic estate-law block).

## Doors actually used (honest door log)

- fxtwitter JSON door (`https://api.fxtwitter.com/<user>/status/<id>` via curl): worked every
  time, zero 403s, full text + created_at + engagement for 11 posts. Primary door for banking.
- Z.ai WebSearch: recurrent MCP 429/1302 rate limits on burst; clean when paced to about one
  query per cooldown. `site:x.com` queries surfaced zero direct x.com links (X is not indexed
  by the engine); the fallback that produced real status URLs was the Latent Space AINews route.
- Latent Space route: section RSS feed `https://www.latent.space/feed?sectionId=327741` gave
  every AINews edition URL in-window; three editions read end to end (Sep 17 "Reality Checks",
  Sep 18 "not much happened today-612", Oct 3 "not much happened today-cee"); their tweet links
  were then resolved through fxtwitter. A bare-slug fetch redirected to the Apr 29 edition
  (out of window; its candidates rejected on date).
- Provider docs fetched live: Anthropic (docs.anthropic.com now 301s to platform.claude.com)
  and OpenAI (platform.openai.com now 301s to developers.openai.com). The docs hosts moved;
  citations below use the live hosts.

## Pass 1 tally

Candidates considered in-window: 100+ tweet URLs listed across the three AINews editions
(~60 + ~65 + ~80), of which ~25 shortlisted on RQ fit, plus ~10 from searches. Rejected
outright: the Apr 29 edition's KV items (vLLM v0.20.0 TurboQuant 2-bit KV cache tweet,
SemiAnalysis DeepSeek V4 serving, Poolside FP8 KV, all pre-window), the Astra persona/compaction
tweet (photo-embedded, content unverifiable), eval-integrity and safety-cluster tweets (off-RQ).

## Pass 2 deep reads (end to end, fetched this seat)

Full fxtwitter JSON read for: dair_ai 2100250366495625320, theo 2100762304862384257 (plus tail
chars 1700-3600) and 2100762775668805960, dair_ai 2106047824093979033, dair_ai 2105915729812050342,
PrimeIntellect 2106146492721648033, khoomeik 2100338891492577727, _philschmid 2100635151080550793,
ekzhang1 2100651678110515383, CompleteSkeptic 2100702845779775675. Plus: two paper pages
(academy.dair.ai protocol-trimming 2609.16461; NVIDIA Staying-on-Task 2609.38712) and both
provider prompt-caching doc pages. 15 end-to-end fetches; the >=5 bar is passed with margin.

## Answers by research question

### RQ1 (KV reuse / prefix caching designs, LMCache lineage, vLLM/SGLang)
The X window itself was quiet on LMCache specifically (no in-window LMCache announcement tweet
surfaced in any AINews edition or search). The lineage's action moved to: (a) SGLang-side
per-turn delta caching for multi-turn agentic serving, Delta Router Replay: cache previous
turns' router decisions client-side and export only the delta (khoomeik, Sep 16; upstreamed as
SGLang #24851); (b) radix-cache prefill reuse as the parallel-agent primitive (ekzhang1's
openjev-s: 64 parallel tasks <1s on Qwen3.6-35B-A3B, Sep 17); (c) KV latent storage compression:
PrimeIntellect stores the MLA latent in NVFP4 (576 to 352 bytes/row, ~50% more cached tokens
per decoder vs FP8), kernel contributed to FlashInfer (Oct 2); (d) vLLM docs (Sep 8) still
document KV offloading with the `lmcache` option alongside `native`. Search-level leads NOT
banked (snippet-only, no exact URLs captured): TuringData ContextCube shared-KV launch
(Sep 28, Yahoo Finance), Tessera demand-driven KV cache management (arXiv, Sep 26).

### RQ2 (context ordering / section structure vs accuracy)
NVIDIA's Long-Transduction (Staying on Task, arXiv 2609.38712, via dair_ai Oct 2) is the
cleanest 2026 measurement: across seven open-weight models accuracy drops 62.8% scaling context
4K to 128K, 36.5% when ONLY the input format changes, 39.9% when per-step operation difficulty
rises. Format/section structure alone moves accuracy by a third; this is the strongest fresh
number backing the deterministic estate-law block and canonical serialization choices. Lead not
banked (not resolved through fxtwitter): huggingface 2106034221005312448 multi-harness RL, same
weights scoring 62% vs 33% across harnesses (Oct 3 AINews listing).

### RQ3 (compaction preserving tool-call fidelity)
Two independent results agree with Theo's practitioner critique. (1) Protocol-aware trimming
(arXiv 2609.16461 via dair_ai, Sep 16): keeping identifiers, constraints, tool schemas and
unresolved commitments intact while compressing the rest reaches 96.0% task success / 1.0%
cascading failure at 56.0% token savings, where recency/relevance/summarization drop success to
66.6-77.3%; keeping <=25% of context raises failure odds 10.92x vs >=50%; caveat: protected
state came from gold annotations. (2) Microsoft FOCUS (arXiv 2609.37590, Oct 2): training-free
decision-preserving compression, -48% peak context, +8.9 pts task success; ALREADY in holdings
(state/arxiv/2026-09-30/2609.37590v1.txt, banked Sep 30, not re-banked). Theo (Sep 18, 2591
likes) supplies the systems Why: compaction is not a filter; per-tool-call line-by-line deletion
orphaned tool results and causes "stupid loops"; frontier APIs return encrypted reasoning that
must not be dropped (Anthropic requires full history to keep reasoning data); and cache writes
are the dominant agent cost: "If your history is '1,2,3,4,5,6' and you delete '2', you have to
rewrite '3,4,5,6'". OpenAI's own docs now list context-management (compaction) as a setting that
invalidates prefix reuse. The two views converge: compact only at boundaries, never mutate
mid-history.

### RQ4 (do provider prompt caches key on byte-identity?)
Confirmed-but-refined as of today's live docs. Anthropic (platform.claude.com, fetched
2026-10-05): "Exact matching: Cache hits require 100% identical prompt segments... up to and
including the block marked with cache control"; one entry per breakpoint, "a hash of the prefix
ending at that block"; hierarchy tools -> system -> messages, "Changes to tool definitions
invalidates the entire cache"; 5-minute default TTL refreshed on use, paid 1h option; caches
org-scoped. OpenAI (developers.openai.com, fetched 2026-10-05): "Cache reuse requires the entire
rendered prefix to match". Rendered, not just your bytes: hidden system tokens and settings
(model, tools, parallel_tool_calls, text.format, reasoning.effort, text.verbosity, context
management) enter the match; minimum 1,024 tokens on GPT-5.6+; TTL 30m refreshed on reuse;
`prompt_cache_key` influences routing only ("do not pin requests to a machine or guarantee a
cache hit"). Verdict for corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md lines 10-12: its
byte-identical-ask assumption holds for both providers, but the estate law should note (a)
matching is on the RENDERED prefix, so serialized settings/schema changes are invisible
byte-changes that break hits; the existing canonical-serialization rule (w3-research-cachemech
holding, json.dumps sort_keys) is exactly the right countermeasure; (b) provider hits remain
machine-local and routing-dependent, so byte-identity is necessary, not sufficient.

## Estate steal-list (one line each)

1. Theo's cache-write economics (60%+ of spend) quantifies why the frozen-prefix law is the
   paid-turn cost lever; feed the descent protocol's prompt-shape leg.
2. Protocol-aware trimming's protected set (identifiers, constraints, tool schemas, unresolved
   commitments) is a ready-made spec for mag/lane_runner transcript folding.
3. Long-Transduction's 36.5%-from-format-alone is the falsifiable number behind the
   deterministic estate-law block ordering.
4. NVFP4 MLA latent (FlashInfer kernel) belongs on the lmcache-src shelf as the current
   KV-capacity best practice in the vLLM/SGLang stack.

## Overlap receipts (grep instruments run this session)

- `grep -c -i lmcache catalog/catalog.jsonl` -> 2,339 (source-shelf rows).
- Phrase greps vs catalog+memory (.md, minus agent_sessions): "cache writes are more
  expensive" 0/0; "Long-Transduction" 0/0; "protocol-aware trimming" 0/0; "decision-preserving"
  catalog:1 (the already-banked FOCUS abstract); "NVFP4" catalog:7 +
  memory/runs/gapwave/kvmem_digest.md (Unsloth NVFP4 weight-quant digest, partial, different
  subject); "radix cache" 0; "Delta Router Replay" 0/0; "openjev" catalog:22 +
  memory/continuity/seat_memory_20260927/* (OpenJev known via VERB DSL steal); "20-block
  lookback" 0; "stupid loops" 0/0. memory/ hits for "byte.identical|prompt cach" were only
  memory/agent_sessions/orc-t*.json transcripts (no curated holding).
