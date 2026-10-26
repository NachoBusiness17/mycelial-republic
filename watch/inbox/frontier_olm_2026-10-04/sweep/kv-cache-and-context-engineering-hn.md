# SWEEP: kv-cache-and-context-engineering via Hacker News (frontier_olm 2026-10-04)

source-fetched: 2026-10-04. Seat: sweep-kv-cache-and-context-engineering-hn (workflow child).
Doors used: HN Algolia `search_by_date` + `search` (clean all session, zero 403s, zero
degrades), then news.ycombinator.com item pages for the two big threads, then the cited
primary pages. No fallback door needed; nothing 403'd. Every quote below was read by this
seat on the fetched page this session. ASCII only, no em or en dashes.

## Held-lens grounding (read this session, before mining)

- `lens/corpus.md:20` - lmcache-src = 2,331 rows, the estate's ONLY serving-runtime source.
- `lens/graph.md:16` - context_compression.py is the graph's real top node (degree 5).
- `lens/laws.md:75` - the seven unwired inference-budget carriers: stealth_driver,
  duel_harness, tesuji_fire, lane_runner, lite_scale, wave_fire, ds_workhorse (class-kill
  enforced only in hermes_burn + model_garden).
- `lens/burns.md` - reasoning-quant ladder probe open, ranked above new mining.

## Pass 1: candidate pool (34 unique in-window stories, 09-04 to 10-04)

Queries run against hn.algolia.com/api/v1 (numericFilters created_at_i > 1788480000):
"KV cache" by-date (20) and by relevance (25, mostly overlapping); "context compression" (5);
"prompt caching" (12); "long context" (20+); "sparse attention" (4); "prompt compression" (1);
"KV quantization" (0 hits); "LLMLingua" (0 hits); "lmcache OR vLLM" (1). Named candidates:
49643543 LRU-vs-papers 108/58; 49735410 DeepSeek-v4.1-Flash 131/10; 49911995 Magnitude 194/97;
49820496 LensVLM 91/10; 49734038 Quantifying Context Rot 3/0; 49758259 vLLM prefix cache 3/0;
49893944 Fathom 1/0; 49883064 Internet for the KV Cache 2/0; 49578969 Yandex KV agent runtime
6/1; 49945575 KV memory wall 2/0; 49701675 agentic KV efficiency 3/1; 49619645 zero-copy KV
migration 2/3; 49637425 Prompt Trees 2/0; 49807383 GPT-6 prompt caching 3/2; 49898130 Jev-style
prompt caching 1/0; 49783040 Ask HN provider KV swarms 1/0; 49896983 Learning to Forget 1/0;
49820191 HySparse2 2/0; 49566170 GLM-5.3-Flash sparse attention 7/0; 49895928 Jtoken 2/0;
49911910 token compression CLI 11/5; 49848678 revefi prompt caching 2/1; 49691257 Replay cache
misses 1/0; 49699918 cache-hit-truth 2/0; 49911500 weave-os router 119/41; 49802789
InstinctFlash 27/4; 49796779 what are KV caches 4/0; 49838474 KV rules everything 3/0;
49813610 trained KV bank 5/2; 49714867 token CDN Ask HN 1/1; 49609821 syntax breaks LLMs 5/3;
49586561 how LMs work 2/0; 49607341 Raschka KV caching 1/0; 49575769 Minilith 13/5.

## Dedup against sibling lanes and prior folds (grep-instrumented, this session)

Before banking I grepped `catalog/catalog.jsonl` (1,040,765 rows per `lens/corpus.md:7`) and
`memory/`, and read the three sibling 10-04 HN bank files. Already held, NOT re-banked here:
- 49643543 LRU-vs-KV-papers: banked 09-30 (`sweep/quantization-and-compression-hn.md:45`);
  catalog grep "LRU is harder to beat" = 0 rows, "agentic-kv-cache" = 0 catalog rows but
  present in memory/percolator/candidates.jsonl + memory/corpus/LINKS.jsonl. I re-read the
  thread and repo independently; my read adds: TTL-300s byte-identical to LRU-leaf in every
  run, LFU-leaf -447.1 pct recompute cost at 50k blocks, +4-6 pp systematic offset vs the
  published Mooncake curve (0.341-0.553 measured vs 0.30-0.51 published), and the Belady
  broken-harness diagnosis (prefix eviction while filling). Whether the 09-30 fold carried
  these exact deltas I did not verify; flagged, not asserted.
- 49734038 boolean.ai context rot: banked 10-01 by the kv lane, re-confirmed 10-03, addendum
  banked today by the agent-memory sibling (`sweep/agent-memory-and-continuity-hn.md:144,309`).
  My independent read reproduced the same numbers (GPT-5.6 Sol 31 to 24 pct pass 0 to 250k,
  Opus 5 flat unrelated / 50 to 40 related, momentum-induced collapse at 250k+). Cross-verified,
  not new.
- 49945575 KV Cache Is the New Memory Wall: banked TODAY by the quantization sibling
  (`sweep/quantization-and-compression-hn.md:228`), including the same verbatim quote I
  pulled. My read adds the crossover numbers (s*(b) = 427k tokens at batch 1 vs 13.4k at
  batch 32 for a 70B) and "Tiering is for reuse between steps, not for reads within a step."
- 49758259 doug.sh prefix cache: banked TODAY by the swarm sibling
  (`sweep/swarm-orchestration-hn.md:39`). My read adds the measured before/after (cached
  token share 55 to 95 pct, TTFT 26-28 s to 7.3 s, worst wait 514 s to 54 s, template edit
  alone 78 to 95 pct) and the GPU-hit-counter trap quote.
- DeepSeek-v4.1-Flash technique: held via 22 catalog rows matching "V4.1-Flash" plus
  memory/behavioral/animals/deepseek_v4_1_flash.jsonl (my grep; the quantization sibling
  counted 8 with their pattern - different instrument, not differenced) and named held
  frontier practice at `sweep/quantization-and-compression-hn.md:107-109`.

## Banked items (8, strongest first)

### 1. The KV cache as an agent runtime (Yandex Research, HN 49578969 + 49598646, 2026-09-05/07)

https://research.yandex.com/blog/the-kv-cache-as-an-agent-runtime - fetched and read.
Quote: "The KV cache is the model's active execution state. It determines which previous
computations are visible to each new query, their causal ordering." Also: "Thinking longer
no longer has to imply responding later."
Measured: AsyncReasoning gives up to 80x reduction in time to first non-thinking token and up
to 12x lower total user-perceived delay while retaining most of reasoning's accuracy benefit;
training-free (pretrained models only); SGLang implementation + custom kernels in progress.
Mechanisms: multi-view shared cache blocks (one physical block, per-consumer logical offsets
via RoPE-relative math), Hogwild!-style concurrent writers, thinker/writer stream split,
streams-as-async-IO (Qwen3.5 agent playing Doom training-free).
Why: this is the Q3 answer with the biggest measured number - the seven unwired carriers are
KV/context-shaped because every dispatch re-sends a prefix; a multi-view cache makes lane
isolation a serving property instead of a prompt-shape hack. Also cross-feeds swarm lane
(flock decode redesign, laws.md open question 2).
Overlap: catalog grep "KV Cache as an Agent" = 0; not in any sibling bank; genuinely new.

### 2. LensVLM: selective context expansion, measured compression curves (HN 49820496, 2026-09-23)

https://huggingface.co/apple/LensVLM-9B + arXiv abstract 2605.07019 - both fetched and read.
Quote (arXiv): "maintains accuracy comparable to the full-text upper bound at 4.3x effective
compression" and "outperforms retrieval-based, text- and visual-compression baselines up to
10.1x effective compression across seven text QA benchmarks."
Mechanism: render pages as compressed images; the model scans them and tool-expands only
relevant pages to full text. HF page exposes 5x/10x/15x compression flags but carries no
benchmark numbers (checked; the abstract is the metrics source).
Why: this is the missing Q2 curve benchmark for context_compression.py (graph.md:16 names it
the real hub): selective expansion (retrieve-then-decompress) BEATS text-compression baselines
out to 10.1x - i.e., at high compression the measured winner is retrieval-shaped, which is
also the Q4 retrieve-vs-compress steer.
Overlap: catalog "LensVLM" and "49820496" = 0 rows; no sibling bank; the paper title IS
registered (registration only, never read into a fold) in
memory/runs/corpus_gap_research/ARXIV_REGISTER.json (grep this session). Genuinely new at the
read layer.

### 3. lmcache upstream delta beyond the held shelf (Q1, releases page read this session)

https://github.com/LMCache/LMCache/releases - fetched and read. Held source:
corpus/library/lmcache-src sits at commit 770e413, 2026-09-21, "[MP][Coordinator] Add Kafka
cache-event sink in producer side (#5285)" (git log this session), build-locked to torch
2.13.0 (pyproject.toml).
Upstream adds since our snapshot: v0.5.6rc1 (09-26) and v0.5.6rc2 (09-28, changelog entry
"[Docs] Add local and Kubernetes Dynamo integration guide (#5257)"); pinned-ABI ROCm 7.2.4 /
torch 2.10.0 wheels for gfx942/gfx950 (09-26/09-28); Moore Threads MUSA wheels; CUDA 13.0 and
12.9 nightlies (10-04, commit 3efdd26).
Unwired-into-serving verdict (grep this session): the estate serving path (Ollama janitors +
remote API lanes) has zero lmcache wiring; only tools/secret_gate_scan.py:84 names the corpus
path in a comment and tools/lattice_build.py mentions it; no mag/ file does. The held source
ships the full feature surface unconnected: cache_policy/{fifo,lfu,lru,mru}, nixl_storage_backend,
p2p_backend, pd_backend(+async) prefill-decode disaggregation, gds_backend, dax, transfer_channel,
offload_server, kv_codec/asym_k16_v8, ec_engine, distributed L2 adapters, hidden_state_store.
Why: for the operator's AMD box the ROCm 7.2 ABI-matched wheels are the concrete new wireable
rung; for the serving path, lmcache remains a vLLM extension the estate has never attached.
Overlap: catalog "lmcache" = 2,333 rows (the shelf itself); "v0.5.6" catalog = 0 rows (grep
this session); no memory/ bank file names the release line. New.

### 4. Prompt Trees: training-time prefix caching, 70x on shared prefixes (HN 49637425, 2026-09-10)

https://www.scaledcognition.com/blog/prompt-trees - fetched and read.
Quote: "We present a method for representing these shared prefixes as prompt trees and
encoding them efficiently in a single forward pass of a standard transformer."
Mechanism: depth-first linearization + path-based position IDs + bit-packed path-vector
block-sparse attention mask, on PyTorch FlexAttention (no custom kernels; ~3 pct cost vs
FlashAttention, relative speedup 0.97). Measured: >70x speedup on H200 with realistic
multi-turn conversational data, scaling roughly linearly with cached-token ratio; embeddings
and gradients match independent per-path encoding.
Why: Q3's "prompt-cache reuse without paid dispatch" has a training-side twin: when the
missing post-training shelf (corpus.md verdict: no RL/post-training rows) is built, shared
RL-rollout prefixes are the dominant wasted compute, and this is the kernel-free recipe.
Overlap: catalog "Prompt Trees" = 0; no sibling bank. Genuinely new.

### 5. Token compression CLI: 29.6 pct Codex savings by stripping tool output (HN 49911910, 2026-09-30)

https://news.ycombinator.com/item?id=49911910 - fetched and read (text post + comments).
Quote: "It cut down tokens by 29.6% and now I just leave it on by default in Codex."
Mechanism: local proxy with a fine-tuned Qwen that removes tool results before they return to
the model, claimed without disturbing the KV cache; savings measured from response.usage.
The lead comment names the failure mode: raw token reduction is the wrong metric; tool outputs
carry single-line anchors (stack traces, exit codes) that must be preserved exactly.
Why: the 10-03 kv lane explicitly left this "unbanked Q3 lead, not read this ask"
(quantization sibling :48 quoting 10-03 kv sweep :58). It is now read. The anchor-preservation
caveat is the estate's own material-rendering law in the wild (STANDING_RAILS: material must
render; empty text is not success), and 29.6 pct is a concrete compress-rung number for
context_compression.py's batch-lane targets.
Overlap: catalog "spenmcke" = 0 rows (grep this session); no sibling bank carries it; the
10-03 kv lane named it unread. New at the banking layer.

### 6. Fathom: per-query adaptive bit-depth over offloaded KV (HN 49893944, arXiv 2609.17652, 2026-09-29)

https://arxiv.org/abs/2609.17652 - fetched and read.
Quote: "each query decides how many bits of each key channel to read" and "the method is not
faster when the index is resident in GPU memory."
Measured (Qwen3-8B, 1M tokens): 1.67x faster decode GPU-time vs 136-bit scans (Double
Sparsity, Loki, SparQ r=32); 18 pct fewer bytes than SparQ's 68-bit scan with lower attention
error in 6 of 7 settings; matches exact top-k on RULER; 92 bits matches 136-bit accuracy on
real coding-agent sessions.
Why: the offload-tier decode recipe for the lmcache shelf (Q1) - it makes the 4-bit-K offload
rung (Q5) actually fast, and its own caveat draws the boundary: the win exists only while the
index lives in host memory, i.e., only in the offload configuration.
Overlap: the abstract is already in the estate: catalog row state/arxiv/2026-09-17/2609.17652v1.txt
(grep this session); no bank file read it before. New at the read layer.

### 7. HySparse2: two-level KV sharing, prefill exits after the self-decoder (HN 49820191, arXiv 2609.26368, 2026-09-23)

https://arxiv.org/abs/2609.26368 - fetched and read.
Quote: "This two-level KV sharing allows all cross-decoder KV caches to be constructed from
self-decoder hidden states. Prefill can therefore exit after the self-decoder, skipping all
cross-decoder layers."
Mechanism: outer YOCO-style KV bridging across full-attention layers only (SWA self-decoder,
sparse-attention cross-decoder); inner token-level (not block-level) sparse reuse; SWA branch
folded into sparse selection. On an 80B-A3B MoE it beats HySparse and hybrid SWA on
long-context retrieval and multi-turn agentic tasks while cutting prefill compute and KV
storage (abstract gives no numbers).
Why: the architecture-side twin of the held DeepSeek v4.1 cross-layer-reuse lever (4 KV source
layers, 5.4x) - it is the general design the estate should hold when reasoning about which
rungs of the serving stack can share KV. Q2/Q1.
Overlap: abstract already cataloged at state/arxiv/2026-09-23/2609.26368v1.txt; no bank file
read it. New at the read layer.

### 8. An Internet for the KV Cache: CDN framing, vision paper (HN 49883064, arXiv 2608.01526, 2026-09-28)

https://arxiv.org/abs/2608.01526 - fetched and read (abstract page).
Quote: "We propose a vision for an Internet for the KV Cache, with KV Cache management working
as a content-distribution system." Also "decoupling of compute and KV Cache storage across
cloud and datacenters."
Why: weakest of the eight (vision paper, zero measured numbers, and the abstract does not name
LMCache), but it is the framing the lmcache shelf's own docs point at: offload/transfer/p2p
backends in the held source are exactly the CDN primitives this paper systematizes. Held for
the serving-path argument, not for numbers.
Overlap: catalog 0; the only memory/ hits for "2608.01526" are prior seats' grep-command echoes
(memory/trajectory/steps.jsonl, quote_audit inbox_concat), not banked content - checked this
session. New.

## RQ answers (short form)

- RQ1: everything in the held lmcache source is unwired (zero serving-path references; grep
  this session). Upstream delta since 770e413: v0.5.6rc1/rc2, the Dynamo-on-K8s integration
  guide (#5257), ROCm 7.2.4 gfx942/gfx950 pinned wheels, MUSA wheels, CUDA 13 nightlies.
- RQ2: the window's measured curves are LensVLM (parity at 4.3x, beats baselines to 10.1x),
  the token CLI (29.6 pct on tool output with an anchor-preservation constraint), and the held
  SoK's KV rungs. LLMLingua-lineage: zero HN stories in-window (Algolia nbHits 0, run this
  session) - no new LLMLingua curve exists on this door this window.
- RQ3: all seven unwired carriers (laws.md:75) are prefix-shaped; the KV-shaped subset is
  everything that re-sends a shared prompt-file prefix per dispatch (ds_workhorse, lane_runner,
  wave_fire, lite_scale). Wireable without paid dispatch: byte-stability discipline (sort
  tool-schema JSON keys, volatile text last, append-only tool results) - doug.sh measured
  55 to 95 pct cached share and 26-28 s to 7.3 s TTFT from exactly that, no hardware, no new
  spend. The estate's byte-identical-ask law already holds the principle; the delta is
  applying it to the carriers' request builders.
- RQ4: no published packing-density floor exists in this window - boolean.ai reports fixed
  token thresholds (250k degradation onset, Sol collapse mode) and explicitly no
  retrieve-vs-compress knee; LensVLM supplies the directional curve (selective expansion beats
  compression past ~4x). Steer: context-pack should treat compress-rungs above ~4x as
  retrieval-shaped, and pack-density floors stay UNMEASURED (an honest UNMEASURED cell, per
  the routing-grid law).
- RQ5: the interaction is real and component-selective. Held spine (SoK 2609.30854): 8-bit KV
  free, 4-bit near-free per-channel, naive 2-bit loses >1 ppl; quantization sibling banked the
  stacking law today (byte savings compose, quality costs do not). New this session: DeepSeek
  v4.1 Flash keeps SWA KV at FP8 while main KV goes FP4 storage-only with dequant before
  attention - a shipped combined config that is aggressive on weights, selective on KV; the
  memory-wall crossover (427k tokens at b=1 vs 13.4k at b=32 for a 70B) says batch width moves
  the regime as much as bit-width; Fathom makes the 4-bit offload rung decode-competitive. Safe
  combined shape for reasoning: deep weight quant + conservative FP8 KV on
  attention-critical/sliding components + FP4 KV only at the offload tier.

## Door health

HN Algolia search_by_date + search: clean, all queries answered first try. news.ycombinator.com
item pages: clean (2 fetched). External primaries (zartbot, doug.sh, boolean.ai, jaehun.me,
research.yandex.com, huggingface.co, scaledcognition.com, github releases, 3 arXiv abs pages):
all fetched clean. Zero 403s, zero fallbacks, zero fabricated recoveries.

## Not run / owed

- No tests were run; none apply to a web sweep.
- Magnitude (49911995) and weave-os/router (49911500) were left to the quantization and
  open-and-local siblings respectively (both already banked/claimed in sibling files).
- Minor instrument delta, flagged not resolved: my case-insensitive "Memory Wall" catalog grep
  reads 1 row (state/arxiv/2026-09-28/2609.30854v1.txt, the SoK abstract itself) while the
  quantization sibling reported catalog 0 - consistent with case sensitivity, not differenced
  per the counts law.
- The doug.sh item has a pre-existing memory trace at memory/runs/gapwave/context_economics_1m.md
  ("prefix cache warm" hit, grep this session); unread this session, held item anyway via the
  swarm sibling's same-day bank.
