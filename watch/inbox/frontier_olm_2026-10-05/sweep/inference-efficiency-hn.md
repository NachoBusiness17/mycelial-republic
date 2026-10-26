# Sweep: inference-efficiency via hn - source-fetched: 2026-10-05

Seat: sweep gopher (inference-efficiency, Hacker News door). Two passes per ask.

## Pass 1 (broad census)

HN Algolia API (`search_by_date`, `numericFilters=created_at_i>1788566400` = 2026-09-05,
`tags=story`) over 9 queries: "speculative decoding", vLLM, llama.cpp, "LLM inference",
"continuous batching", "KV cache", Ollama, "paged attention" (relevance mode), "tokens per
second", plus "small language model local" and one empty "structured output inference" query
(nbHits:0, reported as-is). Roughly 90 distinct candidate stories considered from the window
2026-09-05..2026-10-05; the 30-candidate bar is cleared with margin. One transient network
failure (4 parallel fetches, ECONNRESET) was retried sequentially and recovered.

## Estate-side grounding (what I ran here)

- Overlap grep (this session, `grep -in "speculative decoding|prompt lookup|LRU is harder|
  agentic-kv-cache|Benchmarking Local LLM Servers|congestion control|Decision Models|KV Cache
  Compression|Magnitude|paged attention|continuous batching" catalog/catalog.jsonl`):
  1,096,848 catalog rows scanned; hits are arXiv abstracts already held (Osprey drafters
  2609.09338, ASPIRE 2609.17943, H-Spec 2609.24197, AgSpec 2610.01108 retrieval-based spec
  decoding for coding agents, DeepSeek-V4.1-Flash tech report 2609.19969 at
  catalog/catalog.jsonl:444521) plus corpus EAGLE/EAGLE-3/PagedAttention course docs
  (catalog/catalog.jsonl:885371-886641). Conclusion: the estate holds the PAPER layer; HN
  banking must add engineering threads and measured numbers, not paper summaries.
- Prior-sweep dedupe: `watch/inbox/frontier_olm_2026-10-05` is new but the 2026-09-30 sweep
  (`watch/inbox/frontier_olm_2026-09-30/sweep/inference-efficiency-hn.md:41-145`) already
  banked 8 items in this area. EXCLUDED from re-banking this window: vLLM spec-decoding on AMD
  (49596054), prompt-lookup drafting (49859982), Mozilla local-server benchmark (49742415),
  Mercury 2.5 (49823348), slotstream (49524447), JevBench (49800574), Ollaya (49848269),
  DeepSeek v4.1 internal beta (49607094).
- Envelope check: `grep -rin "109.4M" memory/ watch/inbox/` confirms the number lives in the
  estate's own receipts (memory/continuity/seat_memory_20260927/width-envelope-amendment-20260926.md
  et al.), not in any external source I found this window.
- Fleet-leak confirmation: `grep -rin "agentic-kv-cache" watch/inbox/ouroboros/ corpus/` hits
  watch/inbox/ouroboros/holdings-of-fleet.md:40 and :63 - the repo is a KNOWN LEAK (cited by
  gap-analysis, fill-ball, 48h-synth but never held), and memory/corpus/LINKS.jsonl:264 queued
  it as an acquisition lead 2026-10-02. Item 1 below is the first read-and-banked evidence
  against that leak; the repo itself remains uncloned (I read the HN thread only).

## Banked items (8, strongest first)

1. LRU is harder to beat than the KV-cache papers suggest (HN item 49643543, 2026-09-10,
   108 pts/58 comments, github.com/gauravapiscean/agentic-kv-cache). The author ran a simulator
   against radix-leaf LRU and every alternative LOST; the measured diagnostic on 393 real
   Claude Code sessions: recompute waste is a CAPACITY problem, not an idleness problem - gaps
   past the 5-minute provider TTL cause 17.5% of recompute while gaps under 10 seconds cause
   33.1%, because tight tool loops carry ~88k-token working sets that exceed cache capacity
   (all numbers as reported in the fetched thread). Thread also carries the neocloud
   counterpoint (talolard: providers on GB300 hardware run "wild ttls on the kv cache and still
   comfortably hit SLAs") and the agentic-recency defense (bob1029: "I want this new
   information to dominate the old information"). Why it matters: the estate's fan-out lanes
   are exactly tight tool loops with big working sets - the finding says chasing exotic
   eviction policies is worth less than making the janitor KV budget fit the working set.
   Also cures a named fleet leak (holdings-of-fleet.md:63 lists this repo unheld).
   Overlap: catalog 0 exact hits; queued-but-unheld in LINKS.jsonl:264 and named a leak in
   holdings-of-fleet.md:40,63. The thread's measured numbers are new to the estate.

2. Launch HN: Magnitude - self-optimizing inference engine for agents (HN item 49911995,
   2026-09-30, 194 pts/99 comments). Rust engine with on-device kernel autotuning, catalog
   models shipping with assigned drafters ("Models in our catalog come assigned with an
   assigned drafter model for speculative decoding"), TurboQuant-inspired K8/V4 KV quant, and
   agent-shaped claims: M4 Pro decode 30 to 57 tok/s with 28% less memory per agent. The
   thread did the vendor-claim autopsy for us: bythreads' independent M5 Max run found it
   SLOWER than rapid-mlx (161 vs 175 tok/s decode), mrtsepelev found prefill 2.6x slower than
   oMLX on M5 Pro, and kmike84 listed the standard engine failure modes ("Degraded performance
   at large context sizes" at realistic 100-200K contexts). sebastienburel named the
   transferable insight: for agents the real cost is "resending the same system prompt plus
   tool schemas every turn" - answered by a confirmed prefix tree reused across sessions.
   Why it matters: (a) the autotune-on-your-hardware model is the 2026 pattern for the
   janitor fleet's heterogeneous boxes; (b) the rebukes are a receipt-not-claims checklist
   identical to what the estate runs on its own tok/s claims.
   Overlap: catalog 0 for the repo; TurboQuant prior art already estate-held as code
   (catalog/catalog.jsonl:29813-29816, lmcache turboquant kernels). Genuinely new.

3. New in Llama.cpp: Decision Models (huggingface.co/blog/ggml-org/decision-models-in-llamacpp,
   HN item 49934323, 2026-10-02). Decision scoring lands natively in the janitor serving
   stack: a `/v1/systemone` endpoint where "A decision model reads the input once, and its
   answer is always one of your options, with a probability attached" - one forward pass,
   zero generated tokens (sample response shows `"input_tokens": 130, "output_tokens": 0`).
   Median per-question latency on one RTX PRO 6000: Julia-1 (144M) 3 ms, Laya (421M) 5 ms,
   Kev-4B (4B) 12 ms, lev (4B) 36 ms, OpenJev (27B) 43 ms; confidence output routes
   uncertain cases to humans (a vague ticket "scored 0.25 with Julia-1 but 0.80 with
   Kev-4B"). Why it matters: this is the fastest path to making gemma:2b-scut-class models
   absorb TYPED verdicts (tri-state, seal checks, lane gates) at millisecond cost - the cheap
   tier's per-verdict cost drops to near zero and the budget question becomes which model
   SIZE per question class. Ollama shipped the same support in 0.35 per its 2026-09-30 blog
   title seen in the Algolia listing (fetch of that blog TIMED OUT; mechanism known via this
   HF post - not fabricating its contents).
   Overlap: Jev-sphere prior art held as arXiv abstracts (LLM2Jev 2610.02076, JevOut
   2609.30243, SecJev 2610.03073) and Ollaya banked 09-30; the llama.cpp-native endpoint +
   latency table is the new delta.

4. Adaptive LLM routing via TCP-style congestion control (getunblocked.com/blog/
   adaptive-routing-inference-providers/, HN item 49897322, 2026-09-29). A production
   multi-provider router treats 429s as congestion: "A 429 means the provider is asking for
   less traffic, so we halve the rate, as TCP does when it detects congestion", success adds
   0.25 req/s, "Recovery is slow on purpose", and the scheme is "additive increase and
   multiplicative decrease, and it converges to a stable rate whatever rate it starts from".
   Errors gate rather than score; provider rank = 0.7 x cost ratio + 0.3 x speed ratio on a
   per-TASK ledger ("the task is what the customer pays for and waits for"). Results: median
   task time fell 55%, cost per task fell 14%/4%, seven automatic interventions in four weeks.
   Why it matters (Q4): this is the first external engineered analog of the estate's measured
   envelope law - provider caps handled as rolling THROUGHPUT with AIMD convergence and
   deliberate slow recovery, not as a fixed width. It is consistent with (does not prove) the
   estate's width-10/109.4M tok/h finding: both treat first-contact 429 as a HOLD signal and
   through-put as the state variable. No published multi-tenant study publishing a numeric
   rolling-throughput cap was found this window, so 109.4M tok/h stays estate-original.
   Overlap: catalog 0, memory 0 for getunblocked/congestion-control routing. Genuinely new.

5. Keeping vLLM's Prefix Cache Warm Between Agent Turns (doug.sh/posts/vllm-kv-cache-agents/,
   HN item 49758259, 2026-09-18). The structured-tool-call failure mode made concrete: vLLM
   prefix matching is exact-prefix, so "a change at token 12,000 of a 120,000-token prompt
   throws away 108,000 tokens of finished work"; a gateway bug where shuffled JSON keys in
   MCP tool schemas broke matching left turns only 2-25% cached despite prompts "94-96%
   identical to the previous turn". Fixes (sort tool-schema keys via
   `tool.function.parameters | tojson(sort_keys=True)`, stable-first prompt ordering, fewer
   compactions) moved cache share 55% to 95% and worst TTFT 514 s to 54 s. Side finding the
   estate should steal whole: speculative decoding looked WORSE at 55% cached but BETTER at
   95%, because "At 95% cached there's hardly any reading left to slow down" - spec-decode
   verdicts flip with cache state (Q2).
   Overlap: catalog 0, memory 0, prior sweep 0. Genuinely new.

6. Improving Throughput by Optimising KV Cache Efficiency for Agentic Workloads
   (j9s.io/posts/agentic_inference/, HN item 49701675, 2026-09-14). Quantifies the agentic
   workload shape that makes prose-style serving wrong: per turn "a median of 15,146 tokens
   of prefill" vs 501 decode, and tool outputs return in "a median return time of 0.18s
   versus chat requests' 96.24s", so eviction between turns forces recompute. KV accounting
   is per-token bytes: 256 KiB/token at BF16 (Qwen3-32B-FP8) = ~3.9 GB per median request.
   Optimizations: FP8 KV (`--kv-cache-dtype fp8_e4m3`) moved the throughput elbow from
   c=20 to c=40; CPU offload via `--kv-transfer-config`; madvise-style eviction hints
   (`dontneed`/`pageout`/`willneed`) driven by per-tool-type EWMA gap durations gave 1.06x-
   1.44x prefix hit-rate and 1.04x-1.27x throughput, with the author's own honest caveat
   that results are confounded and not statistically powered. Related systems cited:
   Autellix up to 8x, CacheWise 3.5x session completion, KVFlow 2.19x.
   Why it matters: the EWMA-per-tool-gap eviction hint is directly portable to the estate's
   lane runner (we KNOW our tool gap distributions from trail.jsonl), and the KiB/token
   accounting is a reproducible per-tier budget line (Q3).
   Overlap: catalog 0, memory 0. Genuinely new.

7. The KV Cache as an Agent Runtime (research.yandex.com/blog/the-kv-cache-as-an-agent-runtime,
   HN item 49578969, 2026-09-05). Reframes KV cache as "the model's active execution state":
   RoPE block-local caching (one physical block, per-consumer logical offsets), Hogwild!
   inference (concurrent model instances sharing one attention memory - the fleet mirror at
   the attention level), and AsyncReasoning splitting user input / private reasoning / public
   output streams: "reduces time to the first non-thinking token by up to 80x and total
   user-perceived delay by up to 12x". Metric proposal the estate's budget law should adopt
   for agent lanes: reaction latency and time-to-first-useful-action, not tokens per second
   (Q3). Limitations stated honestly: sequential-trained models may mishandle partial state;
   SGLang implementation in progress.
   Overlap: catalog 0, memory 0. Genuinely new.

8. Show HN: Token compression CLI to save Codex/Astra costs (HN item 49911910, 2026-09-30,
   12 pts/5 comments, text post). Small but it carries the Q3 instrument: token savings are
   measured proxy-side from provider truth - "we're a proxy so could count the tokens using
   openai response.usage" - claimed 29.6% reduction on Codex tool-call outputs. The top
   critique is the estate's own tri-state instinct (SerhiiDrozdov): task success must be
   re-checked post-compression and "anchors" (HTTP statuses, failing test names, stack
   traces, exit codes) preserved exactly while the rest compresses. Why it matters: a
   working example of usage-field accounting as the cheap reproducible spend meter the
   inference-budget law needs per tier, plus the failure mode (silent anchor loss) to
   design against.
   Overlap: catalog 0, memory 0. Genuinely new.

## Surveyed and REJECTED (pass-2 reads that did not survive)

- "LLaMA Now Goes Faster on CPUs" (HN item 49938916, 2026-10-02, 4 pts): justine.lol/matmul
  is UNFETCHABLE (certificate expired, http and https both), and the HN thread fallback
  shows the article is from March 31, 2024 (commenter LargoLasskhyfv: "While impressive,
  it's from Mar 31st, 2024") - not a 2026 serving win. Dropped, not banked.
- DeepSeek-v4.1 Flash KV compression HN post (49735410, 131 pts): skipped - the estate
  already holds the tech report itself (catalog/catalog.jsonl:444521,
  state/arxiv/2026-09-18/2609.19969v1.txt). Re-banking the blog post adds nothing.
- All items already banked by the 2026-09-30 sweep (listed above under dedupe).

## Door health

- hn.algolia.com API: clean (11 queries; one transient ECONNRESET on a 4-wide parallel batch,
  recovered on sequential retry - not a degradation, noted for width hygiene).
- news.ycombinator.com item pages: clean (4 fetched).
- huggingface.co blog: clean. doug.sh, j9s.io, research.yandex.com, getunblocked.com: clean.
- DEGRADED: ollama.com blog timed out at 60 s (reported, no fallback success fabricated).
- DEGRADED: justine.lol certificate expired (item rejected, see above).
No fallback was fabricated anywhere.

## OWED / not done here

- The agentic-kv-cache REPO itself: still unheld (leak per holdings-of-fleet.md:63). This
  sweep banked the HN thread only; the librarian queue should land the repo.
- Spec decoding measured ON structured tool-call outputs specifically: no item this window
  reports acceptance rates on tool-call JSON distributions; Magnitude's thread ASKED the
  question (bursty tool-use token distributions vs single-turn evals) and it was left
  unanswered. The doug.sh cache-state flip is the closest evidence. Estate-side measurement
  on our own tool traces: OWED.
- Any local tok/s run to verify consumer-hardware claims: not run here (sweep seat, no model
  executed this session); every performance number above is the fetched source's own.
