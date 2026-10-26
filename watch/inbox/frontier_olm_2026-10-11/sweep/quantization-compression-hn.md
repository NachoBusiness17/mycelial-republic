# Sweep: quantization-compression via Hacker News - 2026-10-11

source-fetched: 2026-10-11. Seat: sweep-quantization-compression-hn. Doors: hn.algolia.com
search_by_date + search (tags=story, numericFilters=created_at_i>1789084800 = 2026-09-11,
30-day window), then news.ycombinator.com item pages and linked pages via WebFetch.

## Door health and degradation (run record)

- hn.algolia.com: clean on all 8 WebFetch calls (4x search_by_date, 3x search_by_date
  second wave, 1x relevance). Query shapes that returned noise, stated as negatives:
  BitNet pulls 5 of 6 hits from crypto "Bitget" stories (same trap the 10-09 sweep named);
  "model compression" mostly surfaces text-only Ask/Show HNs.
- Two fetch failures, disclosed, nothing fabricated over them: (1) the Bonsai-2 ByteShape
  reddit comparison (HN 50002054) returned a bare "Reddit" shell on WebFetch this sitting,
  the same wall the 10-10 honesty block hit ("reddit doors blocked for siblings, not
  attempted here"); the item remains surfaced-but-unread. (2) openai.com "Disrupting a
  coordinated model-distillation campaign" (HN 49949746) returned HTTP 403; the
  distillation cluster is anyway held by the 10-10 finetuning lane (read this sitting:
  watch/inbox/frontier_olm_2026-10-10/sweep/finetuning-adaptation-hn.md:12,26 covers
  UniEvo-VL, 2609.30652, Jensen, distillation-defenses).
- One URL mapping disclosed: HN 50035357 is titled "Using KV cache as embeddings" but the
  fetched breadbowl.ai page renders the project's technical article "One vector is too
  few. One per token is too many." (BreadBowl-Embed, Ming Xu, Oct 2026). The banked quote
  is from the page actually fetched.
- Recipe fallback note: the first curl+python plan for the Algolia census was blocked by
  the security hook (dynamic-URL SSRF pattern); WebFetch on the same endpoints is the
  recipe's own instrument and worked, so no fallback success is claimed or faked.

## Pass 1 - broad census (8 queries, 30-day window; ~90 distinct candidates)

Queries: quantization (by-date + relevance), "KV cache", GGUF, llama.cpp, BitNet,
distillation, "model compression". Rough distinct count by query: quantization 14, KV
cache 18, GGUF 17, llama.cpp 24, quantization-relevance 0 new, BitNet 1 on-topic (the
held ESP32S3 thread) + 5 crypto false friends, distillation 13, model compression 3 new.
Load-bearing candidates (id, pts/date): 49735410 DeepSeek-v4.1 Flash KV 131p 09-17;
49926773 Janus GGUF Vulkan 106p 10-01; 49884625 ESP32S3 BitNet 150p 09-28; 49879032
Jensen distillation 73p 09-28; 49911995 Magnitude 194p 09-30; 49859982 prompt lookup
drafting 89p 09-26; 49942092 llama.cpp Decision Models 10-02/10-03; 50013834 Self-Pruning
Transformer 6p 10-08; 49823211 quant-delta-predictor 09-23; 49941824 Gufo Q6dense 10-03;
50002054 Bonsai-2 ByteShape 10-08; 49676635 bartowski per-tensor maps 09-12; 49783040 Ask
HN provider-KV-for-swarms 09-21; 49813610 Trained KV cache bank Jev-like 09-23; 50035357
breadbowl KV-as-embeddings 2p 10-10; 49861867 Credence typed decisions 09-27; 49878572
jeva.cpp 09-28; 49699918 cache-hit-not-proof 09-14; 50043847 EmbeddingGemma2 browser
10-11; 49847732 VeriLoop IQ1_M ladder 09-25; 49975499 AMD Quark Strix Halo 10-06;
49980637 Hopf Spherical 10-06; 49926773-adjacent Reflex triplet 09-23..10-07.

## Pass 2 - end-to-end reads this sitting (12 pages, all fetched here)

zartbot DSV41Flash teardown; HN thread 49735410; HN thread 49926773 (Janus);
huggingface.co decision-models blog; github quant-delta-predictor README; arxiv
2610.09051 abstract; bartowski per-tensor blog; HN thread 49783040; github Gufo README;
github Credence README; github jeva.cpp README; breadbowl.ai BreadBowl-Embed article.
Plus the estate-side reads named in the diagnosis section below. Two failures listed
under door health were NOT banked.

## Overlap method (run this sitting)

Catalog: grep -ci per phrase over catalog/catalog.jsonl (1,136,889 rows per
watch/inbox/frontier_olm_2026-10-11/lens/corpus.md:3): dsv41flash 2 (the estate's own
DESK_DSV41FLASH_20260911.md + r-moe-offload.md), Credence 0, bulyaki 0, breadbowl 0,
PragmaTwice 0, libcredence 0, jeva 7 (ALL false friends: UsersfosteAppDataLocalTemp
jevals_readme.md captures, an ms-agents Slovenian README, arxiv 2609.31142 text; no
jeva.cpp row), 2610.09051 0, Self-Pruning Transformer 0, per-tensor layout 0, Gufo 0,
quant-delta-predictor 0, decision-models-in-llamacpp 0, systemone 0, ByteShape 0,
provider KV caching 0, cache hit is not proof 0.
Sibling sweeps (the check the 10-10 steal card proved mandatory): grep -rli over
frontier_olm_2026-09-28..2026-10-10 + adhoc for every candidate name. Result: the held
ground below is near-total. Memory/: bounded grep over memory/rib, memory/research_polished,
memory/steal, memory/knowledge_graph.json for bulyaki = 0 (full-tree memory greps hang in
this sandbox, the 10-10 sweep's transport note names the same limit; bounded instrument
used instead and disclosed).

## Held ground, NOT re-banked (each re-read this sitting, each prior receipt named)

- bartowski per-tensor layout maps: banked 10-02 item 2 AND adhoc item 3 (full reads).
  My re-read reproduced their numbers (token_embd ~8x worst weight tensor at 0.8B, 16x
  at 4B; 1000+ quants over ~96h; KLD-proxy caveat). No drift found.
- quant-delta-predictor: banked 10-03 cycle 2 item 4 (93.23% coverage, -39.5pp adversarial
  tail, INSUFFICIENT_EVIDENCE refusal). My re-read reproduced all three.
- Self-Pruning Transformer 2610.09051: banked 10-10 item 2 (10x/25x KV compression).
  Re-read agrees; still an architecture retrain, not a drop-in quant.
- Gufo Q6dense: banked 10-03 item 3 (3,095.44 pp / 190.67 tg / 334.35 agg tok/s, incl.
  the 190-vs-120 title/description discrepancy flag). The 10-09 "day-08 candidate,
  untouched" note was stale; 10-10's held-ground list was right.
- llama.cpp Decision Models: banked 10-03 item 2 with the estate wire-compat gap named
  (laya_digest.md:80, no /v1/systemone). My re-read adds only the model-name table
  (Julia-1 144M 3ms .. OpenJev 27B 43ms) and the Oct 2 publish date.
- Janus: banked 10-03 + 10-10 delta. Thread verdict unchanged: wrapper-thin over
  llama-server, no benchmarks vs vllm/sglang.
- DeepSeek-v4.1 Flash: architecture held at watch/inbox/DESK_DSV41FLASH_20260911.md
  (primary tech-report read: 890 bytes/token, FP4 KV, CSA2, CED, Engram, DSpark, MIT);
  thread field reports (mmastrac ~5M effective session compactor, nchmy ~60%-fill cache
  break "paid 50x more than expected") banked 09-30 register line 8 + 10-01 item 4 per
  the 10-02 kv sweep's held-list. The zartbot blog itself banked 10-02 item 1.
- Distillation cluster (UniEvo-VL, Jensen, defenses): held by 10-10 finetuning lane.

## Banked items (3, strongest first; all quotes verbatim from pages fetched this sitting)

### 1. Credence - typed probabilistic decisions from a local GGUF model
HN 49861867 (2026-09-27, 1pt) -> github.com/bulyaki/Credence (Apache-2.0, llama.cpp MIT
bundled). Census-surfaced FOUR times (09-30 qc-hn:15, 10-03 qc-hn:13, 10-08 qc-hn:61, my
Pass 1) and never read until now. Mechanism: scores a fixed label set against the
next-token distribution instead of generating; one prompt decode returns a boolean plus
P(true) with entropy/top-two-margin/conformity diagnostics; Platt (temperature+bias)
calibration fitted from labelled sets; pinned-SHA-256 model manifest (Qwen3-4B-Q4_K_M as
the evaluation quant, Q4_0 0.6B smoke-only); roadmap adds choose/score/rank, Stable C ABI
libcredence, resident daemon with MCP adapter. Verbatim: "Credence is an embeddable local
inference runtime for typed probabilistic decisions from GGUF language models."
Why it matters: this is the estate's typed-decision compaction doctrine
(memory/research_polished/kv_cache_compaction.md finding 5: typed-decision scoring vs
summarization, judged against a free recency null) already running as a Q4_K_M-local
product, and it feeds the owed decision-model meter rows (burns.md:241) with an
off-the-shelf calibrated judge that needs zero output tokens. Estate map: mag/max_distill.py
(SkillCandidate executed by a cheap model), mag/context_compression.py:182 llm_compress
(deepseek default), janitor lane (mag/afk_loop.py:104 gemma:2b).

### 2. BreadBowl-Embed - one pooled representation serves retrieval AND reranking
HN 50035357 (2026-10-10, 2p) -> breadbowl.ai article (Oct 2026; fetch mapping disclosed
above). Zero hits in catalog + all prior sweeps ("breadbowl" 0 everywhere). Mechanism:
passages pooled into 16 routing-value slot pairs (8,192 numbers, 16 KiB bf16); routing
vectors indexed for first-stage retrieval and the same vectors define attention over
stored values for reranking, so reranking never re-reads text. Open weights on a
Qwen3.5-0.8B-Base backbone + ~3.3M pooling/output heads; value pathway DISTILLED from
Qwen3-Reranker-0.6B; BEIR macro nDCG@10 48.47 -> 51.54 at same 100 candidates/query;
value read ~0.27 MFLOPs/candidate vs ~0.4 TFLOPs cross-encoder (arithmetic estimates,
no latency benchmarks, stated on page). Verbatim: "Retrieval and reranking share one
representation: documents are encoded once, and reranking never re-reads their text."
Why it matters: two of this estate's compression levers in one artifact - KV-derived
states crushed into fixed-size slots (the lmcache-src adjacency, lens/corpus.md:15) and
teacher distillation into a 0.8B retriever, both directly portable to estate_query /
corpus FTS reranking where the corpus is read-heavy and the rerank budget is the tax.

### 3. jeva.cpp - a llama.cpp fork speaking the JEV decision API natively
HN 49878572 (2026-09-28, 3p) -> github.com/PragmaTwice/jeva.cpp (MIT). Census-surfaced
(10-03 qc-hn:13 bare id, 09-30 _raw p30 files), never banked. Adds Choice/Score/Noul
evaluations computed from model logits on llama-server while preserving autoregressive
generation; inherits all llama.cpp models/platforms; models without vocab logits keep
original function. Verbatim: "jeva.cpp is a fork of llama.cpp that adds a JEV-compatible
decision API to llama-server, enabling Choice, Score and Noul evaluations".
Why it matters: the ecosystem's typed-decision surface (Choice/Score/Noul, the same
question types this sitting verified on the official /v1/systemone endpoint) now has TWO
open-source cures for the estate's laya wire-compat gap (laya_digest.md:80, named by the
10-03 bank): the upstream llama.cpp decision models and this fork. For the estate's
janitor/scut tier the fork is the lower-trust-but-MIT-local path to scoring judges at
3-43 ms with zero output tokens; both paths need the same meter rows the fold owes.

## Considered, not banked (read the page, verdict stated)

- 50043847 EmbeddingGemma2 on the Browser (10-11, 1p): fetched
  searchyourcollection.com/examples; it is a demo landing page ("Everything runs in your
  browser") with no model/quant/latency detail. Not bankable from this page; the post's
  substance stays unverified.
- 49783040 Ask HN provider-KV-caching-for-swarms: zero replies (verified on the item page
  this sitting); its pain points (fork-from-cached-prefix, cross-agent cache persistence)
  are already banked 09-30 per the 10-02 kv sweep held-list.
- 50002054 Bonsai-2 ByteShape reddit comparison: fetch blocked twice (10-10 sibling,
  this sitting). OWED, never asserted.
- HN 49949746 OpenAI distillation disruption: HTTP 403. Held cluster anyway.

## Estate questions this sweep was asked (answers, all byte-cited)

**Q1: why zero confirmed rows across three sweeps?** All three parts of the hypothesis
answered from bytes. (a) NOT wrong doors: the HN door alone produced banked finds on
10-02 (bartowski, ESP32S3, DSV41 teardown), 10-03 (Decision Models, Gufo, Janus,
quant-delta-predictor, Lifeboat, Magnitude, prompt-lookup), 10-08/09/10 (WinML, 2610.09051,
InferPilot, Quark, Hopf, Saluki, Compress and Forget, OptR) - the adhoc DIGEST itself
counts 29 quantization-compression items banked across its four doors. (b) NOT mined out
in general: this sitting still surfaced 3 net-new bankable items out of ~90 candidates.
BUT the margin is thin and concentrated: the door is mined - 10 sweep seats have hit it
since 09-28 and the held-ground map above is near-total. (c) The zero is a FOLD-CAPACITY
artifact, not a discovery failure: the adhoc DIGEST (grep -i quant
watch/inbox/frontier_olm_adhoc/DIGEST.md, read this sitting) states the confirmation pass
covered only 4 of 8 areas (swarm-orchestration 6, finetuning 8, oll 7, kv 2 confirmed)
while quantization-compression's items "carry sweep-level overlap greps only", owner OWED
by name (honest gap 1). One real bar failure also exists and is named: the 10-10 steal
card's overlap re-run REFUTED that sweep's "winml = 0 hits" claim (35 matched lines in 7
prior files; the Windows ML devblog was banked 10-08). Fix shape: the confirmation pass
for this area needs a seat, and sweep-level 0-hit claims in it need the frontier-dir grep
the 10-10 card ran.

**Q2: kv_cache_compaction.md claims and the owed provenance re-audit.** The doc (14,520
bytes, mtime 2026-10-11 03:29:23 -0400, verified by stat this sitting) claims one doctrine
(prefix bytes are the unit of economics; frozen layer + tiny evolving tail; instrument
hit/miss; waste is a burst not an average; typed-decision compaction scored against a
free recency null) and carries its own correction ledger (pro-ratio corrected 09-25;
citation corrected 10-11 by the adhoc kv card). This sitting ran the re-audit's code half
- the instrument outputs: sed -n '555,572p' models/providers.py shows the cache-split
capture VERIFIED at :558-570; sed -n '845,870p' shows the second call site VERIFIED;
sed -n '130,146p' mag/cost_learn.py shows _detect_spikes at :144 and the analyze() call
at :132 VERIFIED; sed -n '39,60p' mag/cache_map.py shows MODEL_RATES with flash
hit 0.0028 / miss 0.14 (= the doc's $2.8e-9/$1.4e-7 per-token) VERIFIED. Two strikes the
re-audit exists to catch: (1) the doc's Unverified/owed line "freeze_system_prompt() ...
never built ... grep: absent repo-wide" is STRUCK by bytes - defined mag/context_pack.py:948
(byte-identical session prefix per its docstring), imported mag/agent_cli.py:29, called
:1061; the doc's next-action 2 is already built, and its named target "repack_messages()"
does not exist under that name (grep repack over mag/ lands in agent_cli auto-repack).
(2) mag/cache_map.py:42 still carries deepseek-v4-pro hit 0.003625 / miss 0.435 - exactly
the stale pre-Sept-10 absolutes the doc's own 09-25 correction says to re-pull before any
economic decision; the correction landed in prose, never in code. Verdict for banking:
cite the doc's verified/built sections freely (they reproduce); do NOT cite its
Unverified/owed section as current; one strike row + one code re-pull are owed to it.

**Q3: is the deliberate-ask quantize target still right?** The premise partially
dissolves on the definition. AGENTS.md:30 verified this sitting (grep -n "Deliberate-ask"
AGENTS.md -> line 30; the :16 hit floating in older snapshots is oral-history copy). The
term is DEFINED at memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md:64-67: "Compress toward:
the rails above, the record laws, the current board (what is live, what is owed).
Everything conversational is heat; only the frozen spec persists." That is a
compression-target doctrine (what to keep when quantizing a learn), not a model-roster
pin: Lightning's death and DeepSeek's proof (lens/burns.md:59-60) cannot stale it, and
the defining rib postdates those roster rows anyway (10-07 rib vs 09-27/28 ledger). The
model-quant pins the ask worries about are maintained on a different, fresher surface:
memory/rib/RIB_GPU_LADDER_20261001.md (quant lane keeps winning per dollar; gemma:2b Q4_0
pulls ordered 2026-10-01, quoted by the 10-10 steal card). Verdict: no re-measure row
needed on AGENTS.md:30; if the operator wants a re-measure row at all it belongs on the
GPU-ladder rib.

**Q4: can the distill-don't-dump doctrine island be wired, and is the practice real?**
Yes and yes. The island is a GRAPH-BUILDER gap, not a practice gap: graph.md:29-30 (read
this sitting) counts doctrine->module edges at zero and only 4 relation types exist, none
expressing "doctrine governs module"; the builder script was not located (matching
graph.md:41's stated limit). But the modules exist - compression and distillation are
practiced in mag/: mag/distill.py:1-7 ("the LIQUID-INTELLIGENCE distillation machine...
Makes the doctrine REAL", sw59-62 many-to-one), mag/max_distill.py:1-7 ("what fraction of
a frontier model's verified advantage can be recovered as an automatically-extracted,
mechanically-applicable policy executed by a cheap model"), mag/context_compression.py
(algorithmic_compress :129, llm_compress :182 with deepseek default, verify_compression
:315, identity compressors :367-395), plus mag/auto_quantize.py, mag/state_quantizer.py,
mag/tool_quant.py, mag/verkle_compaction.py. Wiring it needs a new relation type
(implemented_by or governs) plus doctrine->module edges for at least those four files -
a graph-builder change, which this sweep did not make (no spec-before-behavior pass for
the builder in this ask's scope).

## OWED (opened or carried by this sitting, named)

- Bonsai-2 ByteShape comparison (HN 50002054): reddit door blocked twice; still unread.
- The adhoc fold's confirmation debt for this area (owner OWED by name, honest gap 1):
  unchanged by this sweep; this bank adds 3 pre-verified items but does not discharge it.
- mag/cache_map.py:42 stale pro absolutes re-pull (Q2 strike 2).
- kv_cache_compaction.md owed-list strike row for freeze_system_prompt (Q2 strike 1).
- Graph builder script location + doctrine->module relation (Q4).
- EmbeddingGemma2 browser post substance (landing page only read).
- UWSH independent replication (carried from adhoc, unchanged).
