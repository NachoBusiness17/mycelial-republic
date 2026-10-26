# SWEEP: inference-efficiency via Hacker News (frontier_olm 2026-10-02)

source-fetched: 2026-10-02
Seat: sweep-inference-efficiency-hn. Door: hn.algolia.com API + news.ycombinator.com threads.
Questions: the four in lens/questions.md area 3 (KV-recompute-vs-prefill, cache-invalidation
classes, linear/hybrid/neuromorphic TTFT tables, efficiency per landed deliverable).

## Instruments run this sitting

- Pass 1 candidate harvest: `.venv\Scripts\python.exe %TEMP%\hn_sweep_20261002\sweep_hn.py sweep`
  (script at C:\Users\foste\AppData\Local\Temp\hn_sweep_20261002\sweep_hn.py; raw candidates at
  ..\hn_sweep_20261002\candidates.json). 20 queries x (search_by_date + search), tags=story,
  numericFilters created_at_i > 1788220800 (= 2026-09-01T00:00:00Z, machine clock read
  2026-10-02T14:34:13Z). Result: 267 unique candidates, all in-window, zero API errors, no
  degraded-fallback needed. Queries with zero/near-zero yield: "SpikingBrain" 0, "cache
  invalidation" 2, "neuromorphic" 2, "linear attention" 2. Well over the 30-candidate minimum.
- Pass 2 deep reads (11 fetches, end to end): arXiv 2609.28870 abs + full-text HTML, arXiv
  2609.38386 abs (x2, quote-lock), doug.sh vllm-kv-cache-agents (x2, quote-lock), siddhantkhare
  kv-cache-truth-auditor (x2), HN thread 49643543 (58 comments), j9s.io agentic_inference,
  sference.com prefill-head-of-line-blocking, github corruchaga/D-Engine, github
  LiterateDrivenDevelopment/kcc, arXiv 2608.28444 abs, z.ai glm-built-its-inference-infrastructure
  (DEGRADED, see below).
- Overlap greps: same script's grep mode over catalog/catalog.jsonl + memory/ +
  frontier_olm_2026-10-02 (24 phrases; log in session exec log call_1a2b413e, completed exit 0),
  plus native `grep -rinF` passes over all three prior olm window dirs (20260928, 2026-09-30,
  2026-10-01) and memory/research_polished.

## Rebank kills (the anti-rebank law earned its keep today)

Eight strong candidates died as already-held. Recorded so nobody re-mines them:

| Candidate | Holding that already owns it |
|---|---|
| LRU is harder to beat than the KV-cache papers suggest (HN 49643543, 108 pts) | 09-30 DIGEST register row 6 (watch/inbox/frontier_olm_2026-09-30/DIGEST.md:48); its 17.5/33.1/~49.4 decomposition + ~60 pct fill cliff are banked law text at lens/burns.md:68-69 |
| Keeping vLLM's Prefix Cache Warm (doug.sh) source post | 09-30 DIGEST row 7 (DIGEST.md:49), numbers partially held at context_economics_1m.md:46 |
| A cache hit is not proof you skipped the work (khare) | 09-30 DIGEST row 11 (DIGEST.md:53); my read this sitting re-verified its thesis sentence byte-true: "A cache hit can be true and still fail to prove that work was skipped." |
| Show HN: Replay cache-miss auditor | 09-30 DIGEST row 10 (DIGEST.md:52) |
| Prefill Concurrency in SGLang (sference.com) | 10-01 sweep item 4 (frontier_olm_2026-10-01/sweep/inference-efficiency-hn.md:27-30), same numbers incl the 0.81s-2.42s quote |
| When Fancy Eviction Fails (2609.28870) claim-level | memory/runs/mickey17_v2/runs/agent-engineering-frontier-sweep-40/lanes/kv-agents-week.json:55-60 (2026-09-25); kept below ONLY as a disclosed numbers-extension row |
| Sliding-window beats linear attention (2608.28444) | Held THREE ways: full PDF memory/corpus/training_pdfs/20260916/b11_sliding_window_sinks_2608.28444.pdf (catalog.jsonl:267547), GOAT-vs-SINKS receipt (catalog.jsonl:458560), ARXIV_REGISTER.json:4367 + B11 RIB mapping VERIFIED 09-16 |
| Fathom offloaded-KV sparse decoding (2609.17652) | Abstract-only register pull, catalog.jsonl:444208 (state/arxiv/2026-09-17/) |

SpikingBrain: zero HN hits this window; the baseline table (7.3x at 256k to 26.5x at 1M, H100s)
is held at model_garden/spiking_wide/spikingbrain-deep.md:9-20 per lens/burns.md:129-130, with
primary bytes in gala_20260925/spiking-wide/lanes/ (catalog.jsonl:806908, 807835-807844).

## Findings by question

### Q1 KV-recompute vs prefill beyond 17.5/33.1/~49.4

1. NEW: Decode-Latency Feedback Prefill (arXiv 2609.38386, HN 49925655, 2026-10-01). A model-free
   vLLM controller that throttles prefill chunk size when new prompts overlap active decodes.
   Three paired 100-request trials on Qwen3-0.6B BF16, one A100 80GB: P99 inter-token latency
   "reduce P99 inter-token latency by 24.8%, 30.1%, and 28.2%" (mean 27.7, 95 pct CI 21.0-34.3,
   exact output agreement), at the cost of mean P99 TTFT +34.8 pct inside the declared SLO. The
   load-bearing part for the estate is the published non-reproduction boundary: "the mechanism
   does not generalize to Qwen3-8B, Qwen3-32B, or a two-GPU tensor-parallel" setup, attributed to
   the async scheduler-call interval being only a proxy for GPU iteration time. This is the first
   post-10-01 primary that quantifies the decode-side half of the prefill tradeoff AND names
   where it dies, which is exactly the shape the FAMILY_TABLE wiring debt (lens/laws.md:61)
   needs: params are per-host-shape, never portable. Overlap: "2609.38386"/"Decode-Latency
   Feedback Prefill" grep over memory/+catalog hits only my own trajectory rows this sitting.
   NEW.
2. EXTENSION (claim banked): When Fancy Eviction Fails (arXiv 2609.28870, HN 49927418, 10-01).
   Claim banked 09-25 (kv-agents-week.json:57). My full-text read adds the measured results the
   banked claim lacks: 14 eviction policies on H200 + Qwen3-Coder-30B over two production traces
   (327.5K and 515.8K requests, agentic-heavy) plus AgentX replay of the same 393 Claude Code
   sessions behind the banked decomposition. Headline: "our partial-node compute-aware design
   cuts average Time-To-First-Token (TTFT) by 19.9% (1.04 s vs. 1.29 s) and raises prefill
   throughput by 18.8%" (65.6K vs 55.2K tok/s). Also: fancy policies mostly lose to LRU,
   frequency-based substantially worse, Belady oracle shows the real headroom; block-granular
   compute-aware eviction fails 4.0x on TTFT from fragmentation; session-level eviction costs LRU
   10.5 hit-ratio points at 24 GiB but the gap vanishes at 1 TiB; top 10 pct of sessions hold
   76.2 pct of KV bytes. Answers the 09-30 thread critique (unreferenced "papers", LLM-picked
   metrics) by naming and scaling the baselines. Do the results reproduce outside the original
   stack? Inside this paper, yes across two companies' traces; the LRU-negative reproduces, the
   gains come only from the compute-aware + partial-node combination.
3. NEW: j9s.io agentic KV efficiency (HN 49701675, 2026-09-14). Independent-stack reproduction of
   the agentic re-prefill waste class: SWE-bench Lite via OpenHands against Qwen3-32B-FP8 on vLLM
   (RTX 6000 Pro class, FP8 KV, CPU-RAM offload). "Per turn, we have to process a median of
   15,146 tokens of prefill, and generate a median of 501 tokens of decode." Hinted (state-aware)
   eviction lifted GPU-local prefix hit rate 28.80 to 35.79 pct at c=52 with 1.04-1.27x
   throughput. That is the reproduce-outside-the-original-stack leg of Q1 answered yes: the
   waste class shows up on a different harness, different model, different hardware. Hardware
   note: RTX 6000 Pro / A100 / H200 class in all three Q1 items; whether any of it passes the
   five GPU gates (lens/laws.md:35) is a gates run, not a sweep verdict - not run here.

### Q2 cache-invalidation classes: shipped fixes since 78-to-95

1. EXTENSION (source banked): the doug.sh post IS the origin of the banked 78-to-95 number
   (burns.md:90-91). My read adds what the estate did not hold: the class SHIPPED FIXES. Root
   cause: mcp-go decoded tool lists into Go maps (unordered); Bifrost re-emitted them under Go's
   deliberately randomized map iteration, and since the Qwen template renders tool definitions
   before the system prompt, "one shuffled schema invalidated everything behind it." Merged
   fixes: bifrost#7170 (sort keys during conversion) and mcp-go#984 (preserve server key order);
   the author's template-side stopgap was tojson(sort_keys=True). Instrument recipe worth
   stealing: track prompt_tokens_cached_total / prompt_tokens_total, and diff tokenized
   consecutive turns to find the first divergent token. Overlap: "bifrost"/"mcp-go"/"sort_keys"
   have zero hits across all three olm sweep dirs and memory/research_polished - fix PRs NEW.
2. Corroboration already held: khare truth-auditor (row 11) and Replay (row 10) remain the
   attestation-instrument class; DIGEST law 3 (DIGEST.md:24) already holds "a cache hit
   certifies bytes, not skipped work." Nothing post-10-01 superseded them on this door.
3. KVarN (2606.03458) stays UNCONFIRMED per burns.md:99-100; no second primary surfaced on HN
   this window either. Not repeated.

### Q3 linear/hybrid/neuromorphic TTFT tables

Honest answer: the HN door added NOTHING new this window. "SpikingBrain" 0 hits, "linear
attention" 2 hits (one is the already-held sliding-window paper, one a false positive), the two
neuromorphic hits are a bionic-eye news piece and a podcast, no serving TTFT tables. The one
Q3-adjacent new datum is negative and indirect: DLFP's generalization failure on Qwen3-8B/32B
and 2-GPU TP (Q1 item) is evidence that serving-stack gains observed on one host shape do not
transfer, which cheapens any single-host TTFT table as a purchase argument before the five GPU
gates run. The estate's B11 holding (SWA-with-sinks beats post-trained linear retrofits, 2-10x
on NIAH/BABILong) remains the operative baseline against the hybrid-linear class; it is already
VERIFIED estate-side, no rebank.

### Q4 efficiency per landed deliverable

1. NEW: D-Engine (github corruchaga/D-Engine, HN 49925593, 10-01). Tokens-per-landed-edit
   baseline: deterministic SEARCH/REPLACE harness with a compile gate. "The model proposes
   SEARCH/REPLACE blocks; a local runtime applies them in a shadow git worktree"; merge only on
   green tsc. README table: 10 frozen tasks, quality tied 48/48 vs an agentic loop, avg ~2,100
   vs ~93,000 tokens/task (14-42x), same-model head-to-head 2,552 vs 107,000 tokens, zero broken
   merges. Stated limits: cannot create files, fuzzy-match 0.85 is the weak link, the file
   selector is non-deterministic. Single fetch, one attempt per task, n=10: treat as a lead with
   the descent falsifier's shape (tokens per merged artifact), not a verified number.
2. NEW, weak: Kcc (github LiterateDrivenDevelopment/kcc, HN 49926294, 10-01). Q4 dollars-per-
   artifact datum with an honesty problem: the HN TITLE claims $100/month to build a C compiler
   that "compiles itself to a byte-identical binary; and it cross-compiles to x86-64 (Linux and
   macOS)" and boots a Linux kernel (README-verified: ~1000-page book-as-source, 428 commits,
   difftest vs clang) - but the README states NO cost anywhere. The dollar denominator is
   title-only: OWED, do not cite as measured.

## Degraded reads and OWED

- z.ai "How GLM built its own inference infrastructure" (HN 49737922, 411 pts, top of window):
  first read returned title + opening lines only; re-fetch via a second door returned EMPTY. Not
  banked, nothing fabricated. A re-read attempt is OWED for whoever holds the provider-economics
  line.
- agent-cost-bench (HN 49927585, "cost-amplification bugs", 10-01): surfaced in pass 1, NOT read
  this sitting, therefore not banked. Lead only.
- The Kcc $100/month claim (above).
- Raw candidates file lives in %TEMP%; the durable record is this file.

## Items (strongest first, mirrors the returned JSON)

1. Decode-Latency Feedback Prefill (2609.38386) - NEW, Q1, published non-reproduction boundary.
2. doug.sh shipped-fix extension (bifrost#7170, mcp-go#984) - Q2 answer, source banked.
3. j9s.io agentic KV efficiency - NEW item, Q1 cross-stack reproduction.
4. When Fancy Eviction Fails measured extension - Q1 numbers, claim banked 09-25.
5. D-Engine tokens-per-edit table - NEW, Q4.
6. Kcc dollars-per-artifact (title-only cost) - NEW, Q4, weak, OWED flag.
