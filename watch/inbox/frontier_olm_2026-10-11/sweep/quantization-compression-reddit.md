# Frontier sweep: quantization-compression via reddit (frontier_olm 2026-10-11)

source-fetched: 2026-10-11

Seat: sweep-quantization-compression-reddit (dwfrun-5d623493 lineage). This is the
fourth run of this exact area (after 10-08, 10-09, 10-10 daily sweeps and the adhoc
attempt folded 2026-10-11). Feeds: memory/research_polished/kv_cache_compaction.md
(the owed provenance re-audit), AGENTS.md:30 deliberate-ask quantize target, the
distill-don't-dump doctrine island (lens/graph.md:31), the closed quant A/B tie
(frontier_olm_2026-10-08/sweep/quant_ab/SUMMARY.json), and the percolator pipeline.

## Door record (2026-10-11, this seat's own probes)

- Recipe door old.reddit.com/r/LocalLLaMA/top.json: LOGIN-WALLED ("Log in to use old
  Reddit"), same for old.reddit HTML. Confirmed again this sitting.
- www.reddit.com .json: network-security blocked. www.reddit.com/r/LocalLLaMA/top/.rss
  via WebFetch: HTTP 429 twice this sitting (it was GREEN for the 10-10 sweep).
- Arctic Shift archive API (arctic-shift.photon-reddit.com): WebFetch gets 400/422
  from it, but the web-reader MCP fetches it fine. WORKING endpoints this sitting:
  /api/posts/search?subreddit=X&after=ISO&before=ISO&limit=100&fields=...,
  /api/posts/ids?ids=..., /api/comments/search?link_id=... . Field list is
  validated server-side ("'permalink' is not a valid field"). Caveat, disclosed:
  after/before plus limit=100 returned the NEWEST ~100 posts per sub, not a
  balanced month (the r/LocalLLaMA rows span 2026-10-04 through 10-11), so the
  month-weighted view comes from the safereddit door below.
- safereddit.com mirror: GREEN. /r/LocalLLaMA/top/?t=month, /r/LocalLLM/top/?t=month,
  /r/MachineLearning/top/?t=month each returned a 25-row month-top listing with
  scores, comment counts and relative dates. This is the true full-month view.
- PullPush (api.pullpush.io /reddit/search/submission/?ids=1x2azke,1x2d9wb,1x2dmt4,
  1x2k567): returns an EMPTY data array for all four ids. The adhoc run's proven
  deep-read door is now degraded to empty for these ids; PullPush never archived
  them.
- WebSearch fallback: one success ("reddit LocalLLaMA quantization October 2026
  GGUF" timed out twice, succeeded on retry), ~8 candidate rows.
- Sibling corroboration, cited not claimed: watch/inbox/frontier_olm_2026-10-11/
  sweep/raw_reddit/ holds top_month RSS for LocalLLaMA/LocalLLM/MachineLearning/
  ollama fetched 10:50-10:57 today by sibling lanes, proving the www.reddit.com
  .rss top?t=month door was GREEN today with pacing. I did not fetch those bytes;
  they are door evidence only.

## Pass 1: broad sweep

Candidates considered: 100 arctic rows (r/LocalLLaMA) + 50 (r/LocalLLM) + 50
(r/ollama) + 50 (r/MachineLearning) + 75 safereddit month-top rows (3 subs x 25) +
~8 WebSearch rows, deduped against the 10-10 sweep's 200-row corpus, the adhoc
run's ~20, and the 10-08/10-09 banks. Roughly 330 real in-window rows considered;
the 30-candidate floor is met. On-area rows not banked below (held, already held
by prior sweeps, or off-area): 1x1tclb, 1x1zhnx, 1x223ai, 1x0b1ws, 1wynomx,
1wz4vh6 (all banked 10-10); 1wvzmt3, 1wyc2b0, 1wgzpli, 1wzdti3 (held 10-10);
1wj6c4l was held-as-discovery by 10-09/10-10 and is BANKED here after a full read;
1x3agp7 (FP8 vs BF16 Qwen3-Coder 30B on MI300X: "31% slower for one user and 35%
faster at 64 concurrent", r/LocalLLM, candidate-level read), 1x35kdg (Flash-Next
IQ3_XXS 700K context, r/LocalLLM, candidate-level), 1x37fpr (GLM 5.3 Flash Q2 on
DGX Spark, candidate-level), 1x33ctq (DIY opencode distillation of qwen 3.8
reasoning traces SFT/RL, r/ollama, candidate-level, cited under RQ4), 1x367ar
(GLM-5.3-Flash abliterated MLX 4-bit), 1x3atcl (DeepSeek-V4.1-Flash 552B on Mac
Studio 28 tok/s), 1x34nyx (102M recursive BitNet-v2 from scratch), 1x2vz3y and
1x2eeds (embedding search apps), 1wvz1ex (iPhone second GPU, held 10-10), 1wz6ist
(54GB VRAM for $35), 1x2ji7y (system prompt token bloat), rig/price/news threads.

## Pass 2: deep reads (this seat's fetches)

Six threads read end to end, four read at title+comment level because Reddit
itself has removed their bodies.

### BANKED 1. r/LocalLLaMA 1x357dq (2026-10-10) "Standard evals can't tell my local
quants apart. My own agentic bench can (Qwen3.8 27B / Flash-Next, Q3 to Q8)"

Full selftext read via Arctic Shift. Five quants of Qwen3.8-27B (UD-Q4_K_XL
through Q8_0, plus NVFP4) are indistinguishable on GSM8K / MMLU-Pro / IFEval
(deltas within about 2 points); per-domain KLD against Q8_0 with top-1 agreement
is the only ordering signal (Q4 differs from Q8 about once per 28 tokens), and a
purpose-built agentic bench is what actually separates rungs: 27B NVFP4 scores 77%
where Flash-Next NVFP4 scores 98%, F-group 1/12 vs 12/12, SWE-rebench 69% vs 82%
(p about 0.007), and a ~3-bit GSQ IQ3_S build on Strata matches NVFP4 on 11 of 12
discriminating tasks. Harness matters as much as the quant (OpenCode 2-4x faster
than the alternative shell). This is the estate's quant A/B tie receipt replicated
and extended: the tie is a property of standard evals, not of the quants.

### BANKED 2. r/LocalLLaMA 1x2k567 (2026-10-10) "The ultimate Qwen3.8 27B 16GB VRAM
Cheat Sheet - Benchmarking KLD for 19 model quants and 9 KV quant combinations
(171 benchmarks)"

Body self-deleted on Reddit ([deleted]); title and metadata verified through the
arctic listing (score 10, 30 comments at snapshot). Comment fetch was attempted
twice; the response could not be read in full this sitting, so this bank is
title-and-meta level, honestly stamped. The 19-quant x 9-KV-combo KLD matrix is
exactly the measurement the estate's KV doctrine flagged as unmeasured (KV-cache
quantization "flagged unmeasured" in the adhoc card's 1upc6md comments note).

### BANKED 3. r/LocalLLaMA 1x2d9wb (2026-10-10) "Real long-term memory for local
LLMs: saved KV state on NVMe, reloaded byte-exact instead of recompute"

Body [removed] on Reddit and absent from every archive (PullPush empty); 5
comments survived and were read via /api/comments/search?link_id=1x2d9wb. The
top comment (Queasy-Contract9753) is deflating about the OP but the thread's
existence datum stands: practitioners are persisting KV state to NVMe for
byte-exact session resume, and the reply surface immediately reached for LMCache
as the comparison point. This is the consumer-grade mirror of the estate's
frozen-prefix doctrine (stable-prefix-for-cache): the estate version trusts
prefix tokens to be identical and re-bills at cache-hit rates; this thread pins
actual KV bytes to disk across sessions.

### BANKED 4. r/LocalLLaMA 1x37q7b (2026-10-11) "UPDATE: Qwen 3.8 27B 140 tok/s on
single RTX 3090 Megakernel: KL divergence 0.0009 vs llama.cpp"

Full selftext read. The custom megakernel's accuracy story is an engine-fidelity
table: KL divergence vs llama.cpp on the same weights, with a quant-support
column (Q4_K_M native; other quants fall back) and KV policy (fp16 to about 80k
context then q8). Speculative decoding is bit-exact. Paired with the original
thread below, this is the second 2026 datapoint (after Basalt, banked 10-10)
that non-llama.cpp engines now ship with KLD-vs-reference receipts as their
acceptance gate.

### BANKED 5. r/LocalLLaMA 1x2erdj (2026-10-10) "Qwen3.8-27B on a single 3090: 140
tok/s on code with a custom megakernel"

Full selftext read (score 39, 32 comments at snapshot). Claude Opus 5.5 wrote a
CUDA megakernel doing 1.4-1.9x over llama.cpp at Q4_K_M, one kernel launch per
spec-decode cycle; repo github.com/L-Forster/open-jet/tree/master/megakernel.

### BANKED 6. r/LocalLLaMA 1wj6c4l (2026-09-17) "Ternary Bonsai 2 (27B) just
released on Hugging Face. At <6GB in size, it can even run locally in-browser on
WebGPU."

Full thread text read: my own Arctic Shift fetch confirms id/title/score
(1,603 at snapshot, 320 comments), and the estate's 10-09 raw intake
(frontier_olm_2026-10-09/sweep/_txt_1wj6c4l.txt, 63,805 bytes per
catalog/catalog.jsonl id 5c0536f7340f) carries the full OP and comment set,
read this sitting. OP: ternary-weight derivative of Qwen3.8-27B, architecture
unchanged, "9x smaller than FP16 while retaining 98.2% of the intelligence".
The comment section is the value: the 98.2% claim traces to "84.78 average
across 14 thinking-mode benchmarks" vs 72.59 for a conventional IQ2_XXS build
(Uncle___Marty), skeptics answer "Most likely 98% compared to the 2 bit quant"
(crapaud_dindon) and mock the saturated benchmark choice (PM_ME_DEAD_CEOS),
while one practitioner reports "tool use, agentic flow all are working fine
with similar performance as the full precision model" (ffiw). Held as
discovery by the 10-09 and 10-10 sweeps; now read and banked with the
skepticism attached.

### BANKED 7. r/LocalLLaMA 1x3078i (2026-10-10) "Converting dense models into
Mixture-of-Experts"

Full selftext read. Dense-to-MoE upcycling evals on Qwen2.5-0.5B converted to a
0.3B-active MoE: WikiText-2 perplexity 14.66 to 19.20, mean acc_norm 0.467 to
0.408 at roughly 40% of the MLP compute; SmolLM2-360M shows the same shape. OP's
own conclusion: "There will most likely always be a quality gap." Upcycling is
the inverse operation of pruning/quantization and this quantifies its cost curve.

### BANKED 8. r/LocalLLaMA 1x2j3gx (2026-10-10) "48Gb VRAM speed AND quality !
(Qwen 3.8 27B Swift 1.5 W8A16)"

Full selftext read. 8-bit AWQ+GPTQ W8A16 build served by vLLM with MTP at about
100 tok/s on 2x3090, 21.6GB per card, FP16 KV cache at 128k context. The
quality-safe 8-bit production rung that pairs with the estate's Q4-vs-Q8 tie:
speed lives at 4-bit, quality insurance at 8-bit.

### Removed-body threads, title-level (read what survives)

- 1x2azke (2026-10-10) "Integer-quant GGUFs quietly break Qwen3.8-27B's deep
  thinking - reproduced on llama.cpp, vLLM, and AMD/Vulkan, now with palette-level
  proof": body [removed]; its single comment is an AutoModerator notice (karma
  filter). The claim never circulated on Reddit; title only.
- 1x2dmt4 (2026-10-10) "Show: Mreaia - Zero-Token Context Engine & Hardware-Locked
  Blueprint Distillation for Local LLMs (>99.9% Compression)": same AutoModerator
  karma-removal class; title only. Its r/ollama crosspost 1x2dpdk is also
  title-level.

## Answers to the four research questions

**RQ1: why zero confirmed rows in three sweeps while lmcache-src holds 2,331?**
It is a fold-time artifact, not a knowledge void, and this sitting is the cure for
one of its two causes. Cause 1: the area was never empty, it was OVER-banked: the
adhoc register shows 29 items banked and 23 confirmed in this area
(frontier_olm_adhoc/DIGEST.md:7-9), the 10-08/10-09/10-10 sweeps each banked 6-8
reddit threads here, and the estate additionally holds the 2,331-row lmcache-src
library (lens/corpus.md:15) and the closed quant A/B tie (burns.md:253
anti-rebank). Confirmation passes kept covering only the newest slice (24 items,
DIGEST.md:8) while reddit's doors were walled, so the reddit slice of the area
went thin and stale (the adhoc card's six deep-read threads all span 2026-04-18 to
2026-07-06). Cause 2: enumeration doors. This sitting's new door (Arctic Shift via
the web-reader MCP, plus safereddit month-top) enumerated ~330 real in-window rows
where the recipe's JSON doors return login walls. The lesson for the fold: a
zero-confirm row for this area means "deduped against four predecessor sweeps",
not "nothing found"; the instrument to trust is the door record.

**RQ2: does the owed kv_cache_compaction provenance re-audit validate or strike
the doc?** Both, with receipts. STRUCK: the doc's "freeze_system_prompt() and the
socratic tail-buffer never built - repack still rebuilds the pack per turn"
(memory/research_polished/kv_cache_compaction.md:23) is false as of 2026-09-25:
`def freeze_system_prompt(` exists at mag/context_pack.py:948 (origin commit
3752abae2, 2026-09-25 boot-lane interference burn, verified by git log -S this
run's earlier session), so the doc's next-action-2 (build it) is already cured.
VALIDATED this sitting: _detect_spikes at mag/cost_learn.py:144; cache telemetry
at models/providers.py:559-562 and models/providers.py:847; flash cache rates
mag/cache_map.py:41 {hit 0.0028, miss 0.14} are consistent with the LIVE DeepSeek
pricing page fetched this sitting (deepseek-flash: input cache hit $0.003
off-peak / $0.006 peak, cache miss $0.15 / $0.30, output $0.60 / $1.20; peak
hours 01:00-04:00 and 06:00-10:00 UTC Mon-Fri). NEW STALE ROW FOUND:
mag/cache_map.py:42 carries pro rates {hit 0.003625, miss 0.435} = a 120x hit/miss
ratio, but the live page reads deepseek-v4-pro hit $0.022 / miss $0.66 = exactly
the 30x ratio the doc says was corrected on 2026-09-25. The correction landed in
the doc, never in cache_map.py. Owed still: the OpenAI caching-update URL from
the doc's sources was not re-fetched this sitting; and cache_map.py:42 should be
re-pointed at live numbers by a code seat, not by this sweep.

**RQ3: is the AGENTS.md:30 quantize target still right?** Yes, and no re-measure
row is needed. The quantize target is ask-compression doctrine, not numeric
precision: "strong asks = frozen RIB (system+bootloader+manifest+verkle tip) +
small ask + output contract + quantize target" (AGENTS.md:30), restated verbatim
in the newer rib: "Compress toward: the rails above, the record laws, the current
board (what is live, what is owed). Everything conversational is heat; only the
frozen spec persists" (memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md:64-68). The
roster changes (Lightning dead, DeepSeek proven, lens/burns.md:59-60) move which
animal pays, not what a compressed ask keeps. The stale surface nearby is
AGENTS.md:33 (the old tier-ladder line, superseded by the DRIVING LADDER at
AGENTS.md:35), which is an editor's errand, not a re-measure.

**RQ4: can distill-don't-dump be wired, and is distillation practiced?** Both.
Practiced: mag/arrival.py:82-119 defines `_distill(text, limit=400)` as
"Deterministic, $0 distillation of an authored pack to its invariant core", and
mag/arrival.py:143 calls it "a lossy $0 extraction, not a frontier summary";
mag/code_map.py distills the codebase to its frontier; mag/claritas.py distills
prompt faces; the graph itself carries module:distill.py, module:max_distill.py,
module:max_distill_arms.py and two distill schema invariants
(memory/knowledge_graph.json, read via heredoc this run's earlier session). The
doctrine node "doctrine:distill don t dump" has zero edges, and no edge type
exists that could express "doctrine governs module" (lens/graph.md:29-32: doctrine
217/217 zero-edge, relation types are only has_invariant/maps_to/already_inside/
superseded_by). So the wiring gap is a graph-builder schema gap, not missing
practice: add a doctrine-governs-module edge type and wire distill-don't-dump to
mag/arrival.py:_distill first. In-window reddit corroboration that the doctrine
is mainstream practice: r/ollama 1x33ctq "DIY opencode distillation and qwen 3.8
reasoning traces (SFT/RL) training pipeline" (title-level read, candidate pool).

## Overlap record (greps run this sitting)

- catalog/catalog.jsonl fixed-string greps: "can't tell my local quants apart" 0;
  "megakernel" 0; "Mreaia" 0; "W8A16" 0; "KL divergence" 0. "Ternary Bonsai" 3
  rows, all accounted: memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md
  (unrelated estate Bonsai verification) plus the 10-09 and 10-10 raw intake of
  this same thread (_txt_1wj6c4l.txt, bonsai2_8gb.txt), never banked as claims.
  "byte-exact" 4 rows, all estate gala/last-mile hash artifacts, none about KV
  state persistence.
- memory/ bounded greps (frontier, percolator, research_polished, press):
  "megakernel" 0 files, "Ternary Bonsai" 0, "Mreaia" 0, "W8A16" 0, "KL divergence"
  0, "agentic bench" 0.
- Sibling-sweep dedup (10-08, 10-09, 10-10, 10-11, adhoc sweep dirs): no hit for
  "quants apart". Per-id grep: the four removed ids appear only in
  frontier_olm_adhoc/sweep/_tmp_a1.json (this run's own scratch, no content);
  1wj6c4l and 1wvz1ex appear in 10-10 files as held/discovery rows.
- Self-contamination disclosure: memory/trajectory/steps.jsonl now carries this
  session's fetch ids, same class the 10-10 card recorded.

## Honesty notes

- Every quote above is a verbatim substring of bytes fetched this sitting (Arctic
  Shift API responses, safereddit pages, PullPush empty response, DeepSeek pricing
  page) or of the estate's 10-09 raw intake of 1wj6c4l read this sitting;
  provenance is stated per item.
- The four removed-body threads are banked at title level with the removal cause
  named (AutoModerator karma filter for 1x2azke and 1x2dmt4; author deletion for
  1x2d9wb and 1x2k567); nothing was reconstructed from search snippets.
- Arctic Shift's after/before params returned newest-first slices, not a balanced
  month; the month-weighted view is safereddit's top?t=month (25 rows per sub).
  Scores differ between snapshots (1wj6c4l: 1,603 in the arctic snapshot vs 1.7k
  on safereddit live); both are cited.
- No local probe or A/B re-run was fired: sweep seat, no burns-lane authority.
  The TIE stands as receipted; 1x357dq explains WHY it ties rather than
  overturning it.
