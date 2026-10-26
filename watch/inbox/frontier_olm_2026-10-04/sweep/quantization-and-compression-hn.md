# sweep: quantization-and-compression via HN (frontier_olm 2026-10-04)

source-fetched: 2026-10-04. Lane: sweep-quantization-and-compression-hn. House laws held:
ascii only, no em or en dashes, every claim cites a page fetched or a command run this
sitting. Quote fidelity is fetch-layer (WebFetch fetch-and-answer), not byte-verbatim; the
Algolia listings are byte-proxies (objectID/points/created_at echoed verbatim and
cross-checked across queries).

## Dedup spine read in full this ask (the area has been swept six times before me)

- watch/inbox/frontier_olm_2026-10-03/sweep/quantization-and-compression-hn.md (both same-day
  cycles, 164 lines)
- watch/inbox/frontier_olm_2026-10-04/sweep/quantization-and-compression-arxiv.md (sibling
  arXiv lane, today, 251 lines)
- watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-hn.md (sibling HN
  lane, today, 171 lines)
- watch/inbox/frontier_olm_2026-10-02/sweep/quantization-compression-hn.md (targeted lines)
- watch/inbox/frontier_olm_2026-10-01/sweep/quantization-compression-hn.md (grep + item 5)
- watch/inbox/frontier_olm_20260928/sweep/quantization-compression-hn.md (grep + line 45)
- watch/inbox/frontier_olm_2026-09-30/sweep/quantization-compression-hn.md (grep + lines 42-59)
- watch/inbox/frontier_olm_2026-10-03/sweep/kv-cache-and-context-engineering-hn.md (grep + :58)
- watch/inbox/frontier_olm_2026-10-03/sweep/inference-efficiency-hn.md (grep, candidate list)
- lens: watch/inbox/frontier_olm_2026-10-04/lens/burns.md (full, 195 lines)
- percolator: memory/percolator/candidates.jsonl rows 1-19 (read in full; rows 7 and 18/19
  are the reasoning-quant ladder and the amended curiosity-scored lane-selection candidate)

## Door health

12 hn.algolia.com API queries, all clean JSON, zero 403s; 11 primary pages fetched clean.
Real negatives recorded as negatives: `EXL3` by-date = 0 hits; `exllamav2` by-date = 0 hits;
`intrinsic reward` by-date = 0 hits; `unsloth` by-date = 1 irrelevant hit. Degraded queries,
discarded, nothing asserted from them: `AWQ` by-date returned an unrelated front-page slice
(same degradation class the 10-03 ledger recorded) and `GPTQ` by-date returned generic
GPT-6-Astra front-page noise. WebSearch was not used; the door is HN per the ask. The
memory-tree grep sweep (~550k files) was cut for runtime after two terms, matching the
10-04 sibling's disclosure, and replaced with catalog + bank-of-record greps (commands and
counts below).

## Pass 1: candidate pool (70+ in-window stories surfaced, 09-04 to 10-04)

By query: `quantization` by-date 12 stories; `GGUF` by-date 19; `KV cache` by-date 19;
`llama.cpp` by-date 20; `fp8` by-date 5 relevant (of 20); `compression intelligence`
relevance 5 in-window; `quantization reasoning` relevance 3 in-window. Named load-bearing
candidates: 49611128 Quesma 27B (286/139, held), 49735410 DeepSeek-v4.1 Flash KV (131/10,
held), 49643543 LRU-vs-KV-papers (108/58, banked 09-30), 49926773 Janus (104/19, banked
10-03), 49911995 Magnitude (194/97, banked 10-03), 49859982 prompt lookup drafting (89/12,
banked 10-03), 49847732 VeriLoop ladder (held), 49823211 quant-delta-predictor (banked 10-03
c2), 49743523 weaviate rotational (banked 10-03 c2), 49703818 GSQ-RCO (banked 10-03 c2),
49676635 bartowski layout maps (banked 10-01 item 5), 49941824 Gufo Strix Halo (banked
10-03), 49742415 Mozilla servers (held gapwave), 49812339 transformers llama.cpp quants
(held 09-28), 49945575 KV Cache Is the New Memory Wall (2 pts, 10-03, listed by the 10-03
inference-efficiency sweep, never read), 49644045 glq trellis vLLM plugin (census-listed
since 09-28, never read), 49918747 Is Compression Intelligence (2 pts, 10-01, never
surfaced by any prior pool), 49911910 token compression CLI (11/5, 09-30, explicitly left
"unbanked Q3 lead, not read this ask" at frontier_olm_2026-10-03/sweep/
kv-cache-and-context-engineering-hn.md:58), 49869861 Quantized Reasoning Models Think
Longer (held, 2606.00206), 49833102/49727511 Swift-Qwen3.8 (banked 10-03 evals sibling with
quant-overthink note), 49845314 llama.cpp MoE fork, 49876817 Intel Arc 2.2x, 49796779 what
are KV caches, 49783040 Ask HN provider KV swarms, 49911910-cluster, 49909913 Strata
(banked today by the olm-hn sibling). Comfortably past the 30 bar; after dedup against the
six prior sweeps the genuinely-unbanked set is the 6 items banked below.

## Pass 2: deep reads (11 pages fetched and read end to end this ask)

1. news.ycombinator.com/item?id=49611128 (Quesma thread, held; read to test for unbanked
   residue, verdict: fully mined, see overlap ledger)
2. discuss.huggingface.co VeriLoop E2 thread (page held as template 09-30; read for the
   unbanked community-audit datum, banked as addendum item 6)
3. zartbot.github.io DeepSeek-v4.1 Flash architecture post (held, 8 catalog rows; nothing
   new banked)
4. github.com/gauravapiscean/agentic-kv-cache + news.ycombinator.com/item?id=49643543 (both
   banked 09-30; nothing new banked)
5. huggingface.co/blog/bartowski/per-tensor-layout-maps-for-gguf-quantization (banked 10-01
   item 5; nothing new banked)
6. github.com/gracejackson-sudo/quant-delta-predictor (banked 10-03 c2 item 4; one unbanked
   sentence, banked as addendum item 5)
7. github.com/cnygaard/glq (NEVER read by any prior sweep; BANKED, item 2)
8. www.echohive.ai/is-compression-intelligence (never surfaced before; BANKED, item 4)
9. news.ycombinator.com/item?id=49911910 (explicitly left unbanked; BANKED, item 1)
10. jaehun.me/en/posts/paper-2609-30854v1 (listed 10-03, never read; BANKED, item 3)
11. news.ycombinator.com/item?id=49911910 thread comments (same fetch as 9)

## Answers to the five research questions

### RQ1. Published quant-vs-reasoning measurements at 4-6 bit; do any contradict a banked rung?

The banked rungs stand: quesma Qwen3.8-27B Q4_K_M free on agentic Terminal-Bench 2.1 with
1-bit collapse (register row 22), RATIO overthinking inflation 2.94-3.77x (register row 38),
today's arXiv sibling's sub-4-bit rungs (2609.26708 exposure bias, 2609.06473 NF4 -18 pts
GSM8K, 2607.14181 AQLM-best/QuIP#-worst). What this door adds: (a) the largest published
W4A16 before/after corpus (quant-delta-predictor, 856 rows from 102 RedHatAI cards) structurally
EXCLUDES the population the ladder probe cares about: "Sub-2B, MoE and reasoning-distilled
models fall outside the validated envelope" (README, read this ask) - so the published
GPTQ-card data cannot fill the reasoning rungs, item 5; (b) glq's trellis measurements are
the strongest new 4-bit-class reasoning numbers on the door: AIME-2026 avg@8 41.7 vs bf16
47.5 and NVFP4 32.5 on SmolLM3-3B, and MMLU-Pro 93.3 vs 86.7 for AWQ and NVFP4 with AIME
90.0 at bf16 parity on a 26B MoE - method-dependent damage at 4 bits, cohering with the
flat-then-cliff law and the method dimension, contradicting nothing banked; (c) one unbanked
practitioner datum on the held VeriLoop page: an IQ1_M mixed-precision artifact (5.36 BPW)
and Q4_K_M gave "exactly the same eight decisions, including the same three wrong ones" on
8 canaries (n=8, anecdote-grade) - consistent with the estate's law that distribution
metrics are not downstream benchmark losses. No banked rung is contradicted by anything I
read.

### RQ2. KV-cache quantization levels with measured reasoning cost; the stacking bound

Held spine (register row 6, the 2609.30854 SoK): 8-bit KV free, 4-bit near-free with
per-channel keys, naive 2-bit loses more than 1 perplexity point. Held frontier practice
(DeepSeek-v4.1 Flash, 8 catalog rows): MXFP4-style FP4 main KV with one E4M3 scale per 16
channels, SWA KV kept at FP8 precisely because quantization sensitivity is selective; 890
bytes/token global KV. Held shipped-stack shape (Magnitude, banked 10-03): 8-bit keys /
4-bit values with a RULER retrieval check. New this ask, item 3: the jaehun.me review of
the SoK adds the reviewer's own limitations (derived speedups assume perfect kernel
efficiency; quality deltas are not cross-comparable across papers; MI300X fabric-bandwidth
assumption unverified) and the load-bearing stacking law: byte savings compose across axes
but quality costs do not combine multiplicatively, so "joint validation is essential" -
exactly the bound the ask's weight-quant + KV-quant stacking question needs. It also tabulates
the published sub-4-bit KV rungs: KIVI 2-bit at 8x compression costs +0.03 to 0.3 ppl with
LongBench near baseline, KVQuant 3-bit under 0.1 ppl - transform-based methods, not naive
quantizers, consistent with the held conclusion that reasoning-grade sub-4-bit KV rides
custom transforms the estate's llama.cpp/Ollama tier does not expose. At the estate envelope
(CONTEXT=8k, 6 GB card) KV quant stays a capacity lever, not a quality lever. Bound: stack
q8_0 KV under weight quant freely, 4-bit KV with calibrated scales, and never assume the
quality cost of the stack from per-axis numbers - joint A/B on the estate's own arms.

### RQ3. Does 2026 compression-as-progress / intrinsic-reward literature extend or falsify the amended percolator candidate?

The candidate is memory/percolator/candidates.jsonl:18 (bytes-to-verbs curiosity ranking of
open lanes) as amended at :19 (primary = carried-history retired + verbs minted, secondary =
defects, kill = lose on BOTH over 5 waves), from the dropped Schmidhuber trio (git
756c78b1b + 9058dc238 per lens/burns.md:154-157). Today's arXiv sibling already banked the
two strongest legs (2606.11417: signed compression progress is Goodhart-resistant only on a
sealed audit; own-stream scoring on a reusable panel is exactly where the guarantee
vanishes; 2607.18433: closed-form learnable-novelty estimator). My door adds one genuinely
new citation, item 4: Min et al., arXiv 2608.06503 (Aug 2026), finding that repeated lossy
compression of an agent's own context "could weaken recent interactions and increase
blocked actions or repeated exploration". That EXTENDS the amendment with a scope
constraint the other legs do not name: the candidate's byte-retirement metric must count
bytes retired from durable ledgers and port artifacts, never bytes shaved off a live agent
context, because the 2026 evidence says the latter measurably damages agent behavior. The
survey's own stance (echohive) supports keeping the kill-falsifier's task-side secondary
metric: "A compression score is informative, not a complete report card for an assistant."
Its headline citation, Tan et al. arXiv:2609.27510 (compression rate vs MMLU, Spearman
-0.884 over 80 base models), is already held as catalog row 8c565a877e7d ("Uncheatable
Eval", abstract stub since 09-24) - disclosed, not re-banked. Nothing read falsifies the
candidate; the constraint stack is now: sealed frozen panel + signed metric + artifact-side
compression scope only.

### RQ4. Best quant format and bit-width for the janitor fleet's task mix; family stability

On the estate's box (RX 5600 XT 6 GB, Vulkan, Ollama GGUF: gemma:2b, gemma4,
deepseek-r1:1.5b) the door found no new 2-8B-class quant-vs-agentic instrument - the same
honest gap the 09-30 and 10-03 sweeps recorded, and burns.md's probe order says firing the
estate's own ladder (percolator row 7) and the qwen2.5:7b A/B (probe 5) beats re-mining
(lens/burns.md:117-119); both remain OWED and UNRUN by me (no GPU in this seat's reach).
Community measurements this window keep the ranking: GGUF k-quants with Q4_K_M as default
and Q3-class as the agentic edge; per-tensor-layout-mapped files change what the names mean
(banked 10-01/10-02: _M = 70 pct named type, sizes shift) so the fleet should record layout
provenance per pull in gguf_cartography; the only new format-level datum is glq (item 2),
which beats GPTQ/AWQ at matched ~4 bpw on 10 of 12 metrics and ships INT8 KV - but it is
Linux/NVIDIA-only (sm_86+, vLLM plugin), so it cannot serve the janitor tier today; it is a
watch-item for any future backend swap, the same reopen-condition the arXiv sibling flagged
for AQLM/QuIP#. Family stability: glq holds across SmolLM3-3B dense and gemma-4-26B MoE (2
families), agreeing with 2607.14181's two-family stability (banked today by the arXiv
sibling); two families is not universality, and both new readings land on non-janitor-tier
models.

### RQ5. Seed rows for a quantization shelf (corpus is thin exactly here)

Held spine already verified by prior sweeps: 2609.30854 SoK (register row 6), 2609.14864
throughput (row 21), quesma (row 22), STEPQuant 2609.38169 (row 42), bartowski layout maps
(10-01 item 5), quant-delta-predictor (10-03 c2 item 4), plus today's arXiv sibling's
2609.26708 / 2609.36760 / 2609.06473 / 2607.14181 / 2606.11417 / 2607.18433. New rows this
door adds: (1) glq as the trellis-method-with-measurements row (the QTIP/QuIP# lineage has
zero estate rows; fills part of the arXiv sibling's EXL2/EXL3 community OWED with a
fetchable primary, though EXL3 itself is never mentioned and that gap stays OWED); (2) the
jaehun.me review as the joint-validation/limitations row riding the held SoK; (3) Min et
al. 2608.06503 as the agent-context-compression row, which also seeds the missing
RL/post-training shelf's neighbor (compression-cost-of-agency); the RL/post-training shelf
itself got no new primary from this door - the sibling's unfetched leads 2609.22870 and
2609.33548 stand as the next fetches. Intrinsic-reward lineage row: held 2609.27510 stub
(catalog 8c565a877e7d) plus the two sibling banks; no new 2026 intrinsic-reward primary
surfaced on HN (query negative recorded).

## Banked finds (6, strongest first; quotes are fetch-layer renderings of pages fetched this ask)

### 1. Token compression CLI: trained-Qwen proxy strips tool outputs, 29.6 percent input-token cut, zero task-success validation (HN 49911910, 2026-09-30)

Quote (authors, thread): "we use proxy + fine tuned qwen model trained on preserving agent
trajectory to remove tool call results before they go back to the model".

Why: this is the exact mechanism class of mag/context_compression.py (the graph's hub) as a
shipped product, and its measurement hole is the finding: 29.6 percent token savings counted
from response.usage with no task-success measurement, while the substantive commenter warns
that "tool outputs can be especially risky when the critical information is only one or two
lines" (stack traces, exit codes, failing test names). Port shape: any estate context
compression must carry verbatim anchor preservation (the cite-keeper/citation-lint habit)
and a task-success gate, not a token-count headline. The 10-03 kv-cache sweep explicitly
left this "unbanked Q3 lead, not read this ask" (kv-cache-and-context-engineering-hn.md:58)
and marked the cluster "never fetched or banked. NEW." (:116).

Overlap: catalog "token compression" = 2 rows, both raw course-data names, not this tool;
prior sweeps list the ID only (10-02 census line, 09-30 reddit census line, 10-03
inference-efficiency candidate list, 10-03 kv sweep :23/:58/:116). Genuinely new at the
banking layer. Confidence 0.75.

### 2. glq: QTIP-trellis post-training quantization on vLLM, 2-8 bpw, beats GPTQ/AWQ at ~4 bpw on reasoning benchmarks (HN 49644045, 2026-09-10)

Quote (README): "GLQ has the smallest footprint, the top MMLU-Pro, and matches the bf16
ceiling on hard reasoning".

Why: first primary in the estate for the trellis/QTIP lineage (QuIP# E8P codebook + QTIP
3INST lookup-free decode, Viterbi tail-biting trellis over 256-weight sequences): measured
SmolLM3-3B trellis 4 bpw at AIME-2026 avg@8 41.7 vs bf16 47.5 vs NVFP4 32.5; gemma-4-26B MoE
at ~4 bit with MMLU-Pro 93.3 vs 86.7 (AWQ and NVFP4) and AIME 90.0 at bf16 parity; "GLQ
beats GPTQ on 10/12 metrics"; single-stream decode at bf16 parity while a third of the
weight memory; deterministic bit-identical kernels; INT8 KV cache built in. Honest scope: the
README never mentions EXL3 (the ask's EXL2/EXL3 question stays partially OWED; this fills
the trellis-format leg the arXiv sibling's degraded WebSearch could not), and it is Linux
NVIDIA-only (sm_86+), so it cannot serve the estate's AMD/Vulkan tier - it is a watch-item
that reopens the method question on any future backend swap. Fill-listed in censuses since
09-28 and never read until now.

Overlap: grep "glq" over the six prior quant sweeps: census-listing lines only (09-28:17,
09-30:15, 10-03 pass-1 pool :13); "cnygaard" = 1 hit, the 10-03 raw query dump
(tmp/hnolm/p1_quant.json); catalog "cnygaard" = 0. Genuinely new. Confidence 0.8.

### 3. The KV Cache Is the New Memory Wall: reviewer limitations on the held SoK plus the joint-validation stacking law (HN 49945575, 2026-10-03)

Quote (post): "Almost every published number is right on its own. But almost none of them
can be interpreted together."

Why: a review-layer read of the already-banked 2609.30854 SoK (register row 6) that adds
what the estate should steal: the reviewer's own limitations section (derived speedups
assume perfect kernel efficiency; quality deltas are not cross-comparable between papers;
the MI300X fabric-bandwidth assumption is unverified; MLA/MoE generalization untested) and
the stacking law for RQ2: byte savings compose across axes while quality costs do not
combine multiplicatively, so joint validation is essential when stacking weight-quant and
KV-quant. Also tabulates the published sub-4-bit KV rungs (KIVI 2-bit: 8x compression,
+0.03 to 0.3 ppl, LongBench near baseline; KVQuant 3-bit: under 0.1 ppl) - all
transform-based, confirming the held conclusion that naive-sub-4-bit-KV has no
reasoning-grade evidence. Listed by the 10-03 inference-efficiency sweep's candidate
inventory, never read.

Overlap: 2609.30854 held (register row 6, today's arXiv sibling re-read it); the jaehun.me
post itself: grep "Memory Wall" over catalog + bank files = the 10-03 candidate-inventory
line only; catalog 0. The limitations and joint-validation layer were never banked.
Genuinely new at the banking layer. Confidence 0.7.

### 4. Is Compression Intelligence? survey: carries the unheld Min et al. agent-context-compression damage result (HN 49918747, 2026-10-01)

Quote (the page's rendering of Min et al., arXiv:2608.06503): "repeated agent-context
compression could weaken recent interactions and increase blocked actions or repeated
exploration".

Why: the survey extends the RQ3 lineage with one citation the estate does not hold: Min et
al. (Aug 2026) found lossy, repeated compression of an agent's own context damages agent
behavior - the scope constraint the amended percolator candidate (candidates.jsonl:19)
needs: byte-retirement must be counted on durable ledgers and port artifacts, never on a
live agent context. The survey's own thesis is measured skepticism ("A compression score is
informative, not a complete report card for an assistant"), which supports keeping the
candidate's task-side secondary metric. Its headline citation Tan et al. arXiv:2609.27510
is disclosed as already held (catalog row 8c565a877e7d, "Uncheatable Eval", abstract stub
since 09-24, cited by three prior sweeps) and is not re-banked.

Overlap: grep "echohive" over catalog + all bank files = 0; grep "2608.06503" over catalog
= 0 and over bank .md files = 0 (the two watch hits are reference-list substrings inside
unrelated raw arXiv HTML). Genuinely new. Confidence 0.75.

### 5. quant-delta-predictor addendum: the published W4A16 corpus structurally excludes reasoning-distilled models (HN 49823211, 2026-09-23)

Quote (README): "Sub-2B, MoE and reasoning-distilled models fall outside the validated
envelope."

Why: the tool was banked 10-03 c2 item 4 (conformal envelope, refusal flags, -39.5pp
adversarial arm); this addendum banks the one unbanked sentence that answers RQ1 directly:
the largest public before/after quantization corpus (856 rows, GPTQ W4A16 class) excludes
exactly the population the estate's reasoning-quant ladder probe (percolator row 7) targets,
so the ladder cannot be filled from RedHatAI-card data - it can only be filled by the
estate's own arms, which is measured support for burns.md's probe-first order
(lens/burns.md:117-119). Also additive: "Predicting the loss for one specific model did not
work" because "most of the differences between models were benchmark measurement noise" -
the same measurement-noise critique the quesma thread's Wilson-CI discussion banked, now
from the corpus's own author.

Overlap: quant-delta-predictor banked (10-03 c2 item 4); grep "reasoning-distilled" and
"Sub-2B" over the 10-02/10-03/10-04 bank files: hits are unrelated (sub-2B MCP reliability
2609.07370, SLM-ensemble tokenomics), the exclusion sentence itself = 0 hits. Scoped
addendum, genuinely new sentence. Confidence 0.85.

### 6. VeriLoop addendum: IQ1_M vs Q4_K_M gave identical answers including identical errors on an 8-canary self-test (HN 49847732, 2026-09-25)

Quote (community auditor John6666, on the held HF discuss thread): "exactly the same eight
decisions, including the same three wrong ones".

Why: the VeriLoop ladder is held as the 09-30 RQ4 template and its "quantization-retention
measurements, not downstream benchmark-loss percentages" warning is banked; this addendum
banks the unbanked independent datum on the same page: on 8 hand-built canaries the 5.36-BPW
IQ1_M mixed-precision artifact and Q4_K_M produced identical answers including identical
errors (n=8, anecdote-grade, disclosed as such). For the ladder probe this is a falsifiable
prior worth one arm: behavior on the estate's canary set may be closer across the ladder
than bit-width suggests, so correctness keys must be hard enough to separate the rungs or
the A/B will read flat for the wrong reason.

Overlap: VeriLoop held (09-30 template use, 10-03 exclusion note :73); grep "John6666",
"eight decisions", "same three wrong" over all frontier_olm sweeps and memory/percolator =
0 hits. Scoped addendum, genuinely new datum. Confidence 0.7.

## Overlap ledger (greps run this ask; exact patterns and counts)

Commands: `grep -il/-rl` term sweeps over catalog/catalog.jsonl and the frontier_olm bank
tree (09-28, 09-30, 10-01, 10-02, 10-03, 10-04) plus memory/percolator and memory/corpus;
background full-memory sweep was cut at two terms (memory/ holds ~550k files, the 10-04
sibling's disclosed precedent) and replaced with these bank-of-record greps. Results:
"VeriLoop" = 8 files, all own-echo or raw dumps (held); "quesma" = 25 files incl. register,
steal cards, DIGEST, and the saved raw thread JSON (_hn49611128.json) (held, fully mined);
"per-tensor layout" = 3 prior sweep files (banked 09-28 items 1-2, 10-01 item 5, 10-02
item 2; EXCLUDED); "bartowski" catalog = 1 unrelated row (a letta model-config filename);
"glq" = census lines only; "cnygaard" catalog = 0; "echohive" = 0; "token compression"
catalog = 2 unrelated rows; "2609.27510" catalog = 1 (held stub 8c565a877e7d); "2608.06503"
catalog and bank .md = 0; "anyfoo" = banked twice (09-28:45, 10-02:29); "sharmajai" =
banked (10-03 reddit :120); "John6666"/"eight decisions" = 0; "reasoning-distilled"/"Sub-2B"
= unrelated hits only. Excluded as held or banked: Quesma thread residue (fully mined:
kouteiheika, anyfoo, kmike84, skolos, sharmajai all banked), DeepSeek-v4.1 zartbot post (8
catalog rows), LRU/agentic-kv-cache (09-30), Mozilla benchmark (gapwave), transformers
llama.cpp quants (09-28), Janus/Gufo/Magnitude/Decision Models/prompt-lookup/Lifeboat
(10-03), weaviate rotational + GSQ-RCO (10-03 c2), Strata + Janus-negative (today's olm-hn
sibling), Swift-Qwen3.8 (10-03 evals sibling), bartowski layout maps (10-01).

## Honesty block

- Fetched this ask: 12 Algolia query pages, 11 primary pages (listed in pass 2), zero 403s,
  zero fabricated fallbacks. Degraded queries (AWQ, GPTQ) discarded and reported; EXL3/
  exllamav2/intrinsic-reward negatives are real negatives.
- Quotes are fetch-layer renderings, not retained bytes (disclosed up top); the Algolia
  objectID/points/date fields are cross-checked byte-proxies.
- Not run: the reasoning-quant ladder probe (percolator row 7) and the qwen2.5:7b
  Q4_K_M-vs-q8_0 A/B (probe 5) - estate-GPU instruments outside a sensing seat's reach;
  lens/burns.md:117-119 ranks firing them above this re-mining, and this bank adds only the
  priors they will test against. No pytest run (none named by the ask). No percolator or
  invariant writes. No probe executed.
- OWED, never asserted: EXL3/EXL2 primary community measurements (glq is trellis-lineage
  but never says EXL3; the arXiv sibling's degraded WebSearch gap stands); glq's numbers
  off its own README (no third-party replication found); Min et al. 2608.06503 full text
  (known from the echohive survey's citation only); the memory-prose residual-overlap risk
  the cut grep sweep leaves (same disclosure as the 10-04 sibling).
- Em-dash scan of this file: none present; quotes were selected to avoid them.
