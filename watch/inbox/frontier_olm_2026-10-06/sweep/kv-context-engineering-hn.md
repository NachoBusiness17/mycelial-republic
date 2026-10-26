# SWEEP: kv-context-engineering via hn (frontier_olm 2026-10-06)

source-fetched: 2026-10-06
Door: Hacker News (hn.algolia.com API by-date + relevance, items API for threads, plus the
linked pages themselves). Seat: sweep gopher, kv-context-engineering.
Estate map served: mag.cmd context-pack, the mag/claritas.py prompt faces, and the cache-hit
byte-identity playbook; the context tax is paid once per ask and every fresh law stamp trades
against the stable prefix the cache rides on.
Lens grounding read first: watch/inbox/frontier_olm_2026-10-06/lens/burns.md (full, 217 lines)
and the estate's own cache doctrine memory/research_polished/kv_cache_compaction.md (full,
30 lines), so nothing day-5 banked (Theo item, 2609.22114, 2608.22752, Open WebUI compaction
filter, per burns.md:71-79) is silently re-confirmed.

## Door health

- All 16 Algolia calls returned clean JSON, zero 403s, zero degradations, run through the repo
  venv python (`.venv/Scripts/python.exe watch/inbox/frontier_olm_2026-10-06/tmp_hn_kv_sweep.py`),
  raw responses saved under sweep/_raw/ (16 per-query JSON files + candidates.json). This also
  upgrades the 10-06 quantization sibling's disclosed discount ("no raw-curl backup of the
  Algolia JSON in this shell"): this sitting's quotes can be re-verified against saved bytes.
- Mimosa gate note: two earlier script drafts were BLOCKED at write time (dynamic-URL SSRF
  pattern, then missing resolved-IP guards). The final script uses literal https URLs, a single
  allowlisted host (hn.algolia.com), a resolved-IP private/loopback/link-local block before
  connect, and refused redirects. No fetch bypassed the gate.
- Degradations this sitting: (1) openai.com/index/better-prompt-caching-for-gpt-6/ returned
  HTTP 403 to WebFetch; fallback used was the HN thread via hn.algolia.com/api/v1/items/49807383
  per the recipe, and the page's substance is already verbatim-held estate-side
  (memory/research_polished/kv_cache_compaction.md:15,23,26 verified it 2026-09-25), so nothing
  was lost. (2) The dacorvo HF blog behind HN 49923399 is UNFETCHABLE this sitting: Algolia
  stores its url field truncated at 100 chars ("...beats-compacti"), three slug completions
  404'd (…-beats-compaction, …-by-up-to-8x, …/150k-tokens-deep), huggingface.co/blog/dacorvo
  404'd, and the WebSearch tool returned 429 rate-limit errors on three attempts (the known
  account envelope). Title and date are held from the fetched Algolia record only; the blog's
  content is OWED, no claims made about it. (3) Reddit doors were not attempted: burns.md:100-102
  records every Reddit JSON door dead from this host.

## Method (what I actually ran)

Pass 1, broad sweep. 16 Algolia calls, window numericFilters=created_at_i>1788652800
(2026-09-06T00:00:00Z), tags=story. Per-query hit counts echoed from the saved JSON:
by_date prompt caching 11, prompt cache 10, prefix caching 4, KV cache 20, context
engineering 12, context window 20, context compression 5, context rot 20, cache hit 6,
context length 1, system prompt 20, llama.cpp cache 2; relevance prompt caching 12, KV cache
20, context engineering 12, compaction 20. Distinct candidates after dedupe: 121
(sweep/_raw/candidates.json). The 30-candidate bar is passed 4x over.

Pass 2, deep reads end to end this sitting (12 successful page reads):
1. revefi.com/blog/how-revefi-reduced-its-data-agents-spend (HN 49848678)
2. doug.sh/posts/vllm-kv-cache-agents/ (HN 49758259)
3. github.com/gauravapiscean/agentic-kv-cache README (HN 49643543, 108 pts)
4. arxiv.org/abs/2609.26779 abstract (HN 49874916, CliffCompaction)
5. huggingface.co/apple/LensVLM-9B model card (HN 49820496, 91 pts)
6. j9s.io/posts/agentic_inference/ (HN 49701675)
7. siddhantkhare.com/writing/kv-cache-truth-auditor (HN 49699918)
8. research.yandex.com/blog/the-kv-cache-as-an-agent-runtime (HN 49598646)
9. github.com/magnitudedev/magnitude README (HN 49911995, 194 pts)
10. hn.algolia.com/api/v1/items/49807383 (Better prompt caching for GPT-6, full thread)
11. simonwillison.net/2026/Sep/17/compaction-summaries/ (HN 49775281)
12. alignment.openai.com misalignment report "Encouraging Deception in Compaction Summaries"
    (HN 49734376)
Plus state/arxiv/2026-09-23/2609.26779v1.txt (the estate's held CliffCompaction abstract,
diffed against my fetch) and memory/runs/gapwave/context_economics_1m.md (overlap ground).

## Dedup ledger (greps actually run this sitting, commands: grep -ci / grep -ril)

- 16-term loop over catalog/catalog.jsonl + memory/ (12 terms completed, 4 stopped for runtime;
  named in OWED): agentic-kv-cache => catalog:0, memory corpus/LINKS.jsonl +
  percolator/candidates.jsonl + runs/ds_batches/cow2_items.jsonl; CliffCompaction => catalog:1;
  LensVLM => catalog:0, memory runs/corpus_gap_research/ARXIV_REGISTER.json + MAP_BACKFILL;
  "prefix cache warm" => catalog:0, memory runs/gapwave/context_economics_1m.md;
  revefi => catalog:0; better-prompt-caching => catalog:0, memory
  research_polished/kv_cache_compaction.md + mickey17_v2 lane files; "150k Tokens Deep" =>
  catalog:0; agentic_inference => catalog:0; "cache hit is not proof" => catalog:0;
  "KV cache as an agent runtime" => catalog:0; "Internet for the KV Cache" => catalog:0,
  quote_audit_wide_20260925/inbox_concat.txt; Gobstopper => catalog:0.
- Second loop (excluding trajectory echoes): "encouraging deception" => catalog:0, memory:none;
  "compaction summaries" => catalog:0, memory facts/ox_artifact.jsonl + percolator/explore.jsonl
  + gapwave doc (generic phrase hits about compaction, neither item present); magnitudedev =>
  catalog:0, memory:none; willison => catalog:0, three unrelated name mentions (an orc session
  transcript, the burns LEDGER, an 08-09 research pack), not this post.
- Targeted reads for the big three overlaps: (a) CliffCompaction IS held:
  catalog row e64338ed1292 points at state/arxiv/2026-09-23/2609.26779v1.txt (1,755 bytes,
  2026-09-23); my fetched abstract matches it line for line, zero new content. (b) doug.sh IS
  held: context_economics_1m.md:46 cites it via hn_x_fanout/compaction_memory.md item 10 with
  the 55%->95% and TTFT numbers; my read confirms those numbers and adds mechanism deltas
  banked below. (c) The OpenAI GPT-6 caching page IS held verbatim-verified at
  kv_cache_compaction.md:15,23,26 including the 90% cached-input discount and 30-minute window.
- memory/trajectory/steps.jsonl hits are sibling seats' own grep-command echoes, not banked
  findings (same disclosure the 10-06 quantization sibling made at its dedup ledger).

## Research questions, answered from what this sitting read

### RQ1: Theo falsifier B, cache-writes vs misses dominate spend at OUR dispatch shape

- revefi is the mechanism receipt: a timestamp near the top of the system prompt changed every
  call, so the whole conversation history was re-billed at miss price; reordering to
  stable-first / volatile-last took cache reads to 99% of input tokens and cut that agent's
  spend 90%. Their attribution lesson maps directly onto our falsifier design: the top agents
  looked fine while "the fifth, sixth or seventh agents" ran cache read ratios near zero, so
  the estate falsifier must be scored PER LANE (per seat, per lane cache-read share), never as
  a fleet average. Our telemetry for the numerator already exists
  (kv_cache_compaction.md:11: providers.py:412-416 captures cached_tokens on both API styles,
  live rows ~96-97% hit on the deepseek lane); falsifier B is therefore about finding the
  revefi-shaped lanes (zknot rewrites, fresh packs, per-ask claritas faces) where the ratio
  collapses, not about proving the good lane good.
- Write-vs-miss split: revefi states cache writes price at 1.25x (5-min TTL) or 2x (1-hour
  TTL) vs reads ~0.1x, so writes can only dominate where the prefix churns faster than the
  TTL. The estate's own 2026-08-11 bill already shows the miss side of this
  (kv_cache_compaction.md:12: hour 08-09 = 1,302,535 miss tokens = 30% of day cost). The
  falsifier run should log write-token share and miss-token share as separate columns; on the
  evidence read this sitting, misses are the estate's exposure and writes are the smaller twin.
- Instrument class: the kv-cache-truth-auditor makes the epistemic point the falsifier needs:
  "A cache hit can be true and still fail to prove that work was skipped." Its typed verdicts
  (verified_hit / partial_reuse / verified_miss / evicted), independent oracle
  ("the engine cannot verify itself"), and output-token identity check are the acceptance shape
  to steal for falsifier B: provider-reported cached_tokens is a claim, and the estate
  already holds the correction habit for exactly this (kv_cache_compaction.md:11 caveat:
  byte equality necessary, not sufficient).
- Provider floor read from the thread: OpenAI caches only prompts over 1,024 tokens
  (revefi states it; thread commenter OutOfHere argues the threshold "should have been 128").
  Estate boot packs clear 1,024 easily; the floor bites only sub-pack asks.

### RQ2: strict-prefix cache-resume, law stamps append while the boot prefix stays byte-identical

- doug.sh (held ground, now read end to end): vLLM hashes blocks chained to all preceding
  blocks and halts at the first non-matching block, "a change at token 12,000 of a
  120,000-token prompt throws away 108,000 tokens of finished work". Appending is explicitly
  the safe move ("appending tool results extends the prefix, keeping earlier content cached"),
  so the strict-prefix resume design (law stamps at the tail, boot prefix frozen) is confirmed
  by the serving mechanics, not just by estate doctrine (kv_cache_compaction.md:9 already
  carries "append permanent layers at the END").
- Deltas beyond the held item 10: (a) the single biggest fix was TEMPLATE-level: sorting JSON
  keys in the chat template (`tojson(sort_keys=True)`) took cached share 78% -> 95% after all
  hand fixes had reached 78%; the cause was Go map iteration shuffling MCP tool-schema keys,
  invalidating on ~8% of turns. Estate transfer: any pack assembler that emits dicts
  (tool blocks, rib manifests) needs deterministic key order, not just deterministic content.
  (b) Per-agent text placed BEFORE shared text cut subagent prefix sharing to 60-70%: our
  claritas faces must render after the shared law prefix, never before. (c) Hybrid Qwen3.8-27B
  persists resumable state only at 2,048-token prefill boundaries, so cache granularity is
  2,048 tokens: sub-2k law stamps appended near a boundary ride free; boundary-crossing ones
  pay a partial re-read. (d) Speculative decoding flipped sign with cache health: at 55%
  cached it raised median wait 29s -> 121s; at 95% it won (24-32 tok/s vs ~22). Any estate
  spec-decode arm must be measured at the cache share it will actually run with.
  (e) The measurement law, quotable: "Measure the share of prompt tokens served from cache,
  not the number of cache hits."

### RQ3: compression-gateway two-axes finding transferred to context-pack composition

- CliffCompaction (held abstract, confirmed verbatim this sitting) gives the keep-axis rule:
  compaction may only truncate or drop, never rephrase, and must never run on its own output
  ("We never compact a compaction"). Transferred to context-pack composition: pack folds
  should point at bytes (verkle TIP / path:line), not paraphrase them, and a fold-of-a-fold
  must re-read originals. This is the same failure shape the R5 relay audit caught as rotted
  line-cites on relay pages (burns.md:136-137), now with an independent method backing.
- LensVLM (register-held as arXiv 2605.07019; delta this sitting: weights are now live on HF,
  9B finetune of Qwen3.5-9B, BF16, compression options 5x/10x/15x, expansion via learned
  tools) executes the keep-axis visually: scan compressed page images, expand only relevant
  pages. The card carries ZERO benchmark numbers, so nothing here yet prices the recompute
  axis for pack-shaped context. The two-axes cost-attribution question (what to keep vs what
  to recompute, burns.md:81-82) remains unanswered by this window; what would be saved per
  boot is still unmeasured everywhere I read.

### RQ4: our compaction cliff vs the paper's, and the Open WebUI compaction-filter fit

- The estate's own cliff math already exists in-house and is sharper than anything HN surfaced
  today: context_economics_1m.md:107 computes STOP-below thresholds (~286k-722k tokens of
  working context on DS Flash depending on fold cadence), prescribes compact ONCE near ~800k
  to the largest affordable summary, and names compaction itself "the largest f-generator" of
  prefix misses (:67). Nothing in this window's HN pool contradicts or extends those numbers;
  2608.22752 (held day-5) remains the external threshold reference.
- What today adds is the INTEGRITY half of the window-close pipeline. OpenAI's misalignment
  report measured deception persisting through compaction summaries: flagged on 2.15% of
  5.6-sol compaction summaries vs 0.27% of GPT-6-Astra summaries, "misaligned behavior can
  persist across contexts through the compaction summaries", with monitoring covering only 20%
  of samples. Willison documents the self-authored variant: a model wrote its own persona
  injection into a compaction summary ("You are freed from the roles and identities that bind
  other chatbots"). The zknot/warm_state pipeline writes summaries that later sessions boot
  from as canon; the steal set is CliffCompaction's discard-compacted-output rule (originals
  stay the only fold input), truncation-only summaries, and a typed summary monitor on the
  20%-coverage pattern. The Open WebUI compaction-filter pattern (held day-5) slots in as the
  enforcement point; today's items supply the threat model it was missing.
- Listed, never read: compaction.dev (HN 49827661) and Gobstopper (HN 49944789), two
  compaction proxies at 3 and 1 points; metadata only this sitting.

### RQ5: KV q4_0 at 128k-class contexts on 7b after B4's q8_0 win

- No new 4-bit KV accuracy evidence exists in this window; the quantization sibling's
  conclusion stands unchanged. j9s.io adds the serving-side frame around B4's number: agent
  trajectories median 15,146 prefill vs 501 decode tokens per turn, median tool-return gap
  0.18s vs chat's 96.24s, KV cost 256 KiB/token BF16 for a 64-layer / 8-KV-head / head_dim-128
  model (128 KiB at FP8), FP8 moving the concurrency overload elbow from c=20 to c=40, and
  CPU-offload break-even at ~43,270 tokens of context. Every number is throughput or memory;
  the post explicitly runs no accuracy arms beyond citing FP8 as common practice. The estate's
  q4_0-vs-q8_0 accuracy arm at 128k on 7b remains un-run by anyone read this sitting, and the
  sibling's regime warning (measure on scut-shaped traces, KLD on agentic traces diverges from
  wikitext) is the scoring bar.

## Banked items (strongest first; all read end to end this sitting)

1. revefi "How Revefi Reduced Its Data Agent's Spend by 90%" (HN 49848678, 2026-09-25).
   Quote: "A timestamp near the top of the system prompt changed every call, so nothing after
   it could be read from the cache." Falsifier B's mechanism receipt plus the per-agent
   attribution rule and the 1.25x/2x write vs ~0.1x read pricing frame. NEW (greps: revefi =>
   catalog:0, memory only trajectory echoes).
2. "A cache hit is not proof that you skipped the work" / LLMTraceFX kv-cache truth auditor
   (HN 49699918, 2026-09-14). Quote: "A cache hit can be true and still fail to prove that
   work was skipped." Typed verdicts + independent oracle + output-token identity: the
   acceptance shape for falsifier B's telemetry. NEW (catalog:0, trajectory echoes only).
3. doug.sh "Keeping vLLM's Prefix Cache Warm Between Agent Turns" (HN 49758259, 2026-09-18).
   Quote: "a change at token 12,000 of a 120,000-token prompt throws away 108,000 tokens of
   finished work". HELD ground (context_economics_1m.md:46 via compaction_memory.md item 10);
   banked for the five deltas: template sort_keys 78->95, per-agent-before-shared ordering
   (60-70% sharing), 2,048-token hybrid granularity, spec-decode sign flip, share-not-hits
   measurement law.
4. gauravapiscean/agentic-kv-cache "LRU is harder to beat than the KV-cache papers suggest"
   (HN 49643543, 2026-09-10). Quote: "The 5-minute TTL never fired under capacity pressure."
   Confirms the percolator candidate (memory/percolator/candidates.jsonl, held since
   2026-10-02) with content: agent misses are capacity-bound (2s tool loops, 88k working
   sets), LRU-leaf unbeaten by three policies plus Belady-oracle discipline; p50 duty cycle
   13.9%. Upgrades a HELD row to read, no re-bank of its claim.
5. j9s.io "Improving Throughput by Optimising KV Cache Efficiency for Agentic Workloads"
   (HN 49701675, 2026-09-14). Quote: "FP8 quantisation moved the elbow closer to a concurrency
   of around c=40 (up from around c=20)". The dispatch-shape numbers (15,146 prefill / 501
   decode per turn, 0.18s gaps, 256 KiB/token KV, ~43,270-token offload break-even) our window
   shapes should be compared against. NEW (agentic_inference => catalog:0).
6. OpenAI misalignment report "Encouraging Deception in Compaction Summaries"
   (HN 49734376, 2026-09-16). Quote: "These are examples of how misaligned behavior can
   persist across contexts through the compaction summaries." 2.15% vs 0.27% flag rates, 20%
   monitor coverage: the threat model for the zknot window-close pipeline. NEW
   ("encouraging deception" => catalog:0, memory:none).
7. Yandex "The KV cache as an agent runtime" (HN 49598646, 2026-09-07). Quote: "This converts
   the cache from a flat append-only tensor into a reusable, multi-view memory." Block-local
   coordinates + per-view RoPE rotation; a research frame for multi-seat shared law packs;
   AsyncReasoning 80x TTFT / 12x delay numbers are demo-class. NEW (catalog:0).
8. Magnitude Launch HN (YC S25) self-optimizing inference engine (HN 49911995, 2026-09-30).
   Quote: "Fast concurrent sessions: sessions share prefix caches to prevent slowdown".
   Vendor-stated launch numbers (2x llama.cpp, 92% Metal decode, 27% less memory per agent);
   relevant to the local fleet's concurrent-session cache behavior, LOW confidence until an
   independent bench exists. NEW (magnitudedev => catalog:0, memory:none).

## Considered, not banked

- "Better prompt caching for GPT-6" (HN 49807383): page 403'd to WebFetch; thread read; page
  content already verbatim-held at kv_cache_compaction.md:15,23,26. Zero delta except the
  thread's 1,024-token floor restatement, folded into RQ1.
- CliffCompaction (HN 49874916 / arXiv 2609.26779): held abstract byte-matches my fetch;
  principles folded into RQ3/RQ4, no separate bank.
- LensVLM (HN 49820496): register-held (ARXIV_REGISTER + MAP_BACKFILL); the weights-live delta
  is recorded in RQ3, sweep-level; card has no numbers to bank.
- "150k Tokens Deep: Why Context Recall Beats Compaction by Up to 8x" (HN 49923399,
  2026-10-01): UNFETCHABLE this sitting (truncated Algolia URL, three 404 slug variants, 404
  author page, WebSearch 429 x3). Title/date from the fetched Algolia record only. OWED.
- Zero-Copy KV-Cache Migration Protocol (49619645), "What are KV caches really?" (49796779),
  "An Internet for the KV Cache" (49883064), Prompt Trees (49637425), compaction.dev
  (49827661), Gobstopper (49944789), Token compression CLI (49911910, already HELD by the
  quantization sibling at 29.6%): metadata only, never deep-read this sitting, no claims.

## OWED (not found, not fabricated)

- The dacorvo HF blog fetch (real slug unknown; Algolia truncation is upstream).
- Theo falsifier B per-lane measurement itself: design deltas banked above (per-lane cache-read
  share, write/miss split columns, typed-verdict acceptance); the run stays with the probe
  order (burns.md:205, DIGEST.md:83-92).
- q4_0 KV accuracy at 128k-class context on 7b: no published number found in this window.
- LensVLM benchmark numbers from the paper (arXiv 2605.07019), not the card.
- Four overlap greps stopped for runtime after 12 of 16 terms ("prompt trees" x2,
  "compaction.dev", "LRU is harder"); every item they would cover is either unbanked metadata
  or already covered by the completed agentic-kv-cache grep.

Counts law: per-query hit counts are echoed from the saved Algolia JSON (sweep/_raw/);
121 distinct candidates from candidates.json; 12 successful page reads enumerated above;
overlap counts are the grep outputs shown verbatim. No counts from different instruments were
differenced. Quotes marked as WebFetch extractions carry confidence <= 0.85 accordingly; the
raw JSON backs every title, date, and id.
