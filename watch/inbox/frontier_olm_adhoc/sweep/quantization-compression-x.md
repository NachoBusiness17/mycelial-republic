# SWEEP: quantization-compression-x (adhoc, 2026-10-11)

source-fetched: adhoc. Seat: sweep-quantization-compression-x. Area: quantization-compression via x.
This file SUPERSEDES the 2026-10-10 write-up at this same path (that seat's 8 banked items are not
re-listed here; they remain in git history and are treated as estate holdings in section 4).

## 0. Door truth (X lens, second session running)

- X DISCOVERY is walled AGAIN, now with the mechanism fully mapped: the WebSearch backend drops
  `site:x.com` on every shape (returns llama.app/wikipedia/merriam instead), storms MCP 429/1302 on
  retries, and states X content is not indexed (three queries this session). html.duckduckgo.com
  answers a bot-verification challenge. bing.com mangles `site:` to a single letter. xcancel.com
  (live nitter instance) returns HTTP 451. threadreaderapp.com/search is an instructions-only page.
  PullPush `ids=` (the reddit sibling's working reader) returned `{"data":[]}` for the one in-window
  quant reddit thread (1wju8ky, ByteShape Bonsai-2 post) - deleted or never archived.
- Status-ID mining that DID work: hn.algolia.com full-text search returns stories/comments carrying
  real twitter/fxtwitter `/status/` IDs (query "fxtwitter" and "twitter.com quant" surfaced 25+
  live IDs). Every quant-relevant ID found this way is out of window (newest: awnihannun Mistral
  4-bit, 2023-12; _jakubchura Qwen3-0.6B 90tok/s, 2025-10; carrigmat DeepSeek-R1 Q8 DDR5, 2025-01).
  Zero in-window (>= 2026-09-11) X status IDs on quant exist on any surface this seat can reach.
- fxtwitter RESOLVE door verified GREEN first-hand this session:
  api.fxtwitter.com/awnihannun/status/1738031136994181376 -> 200, tweet JSON, media shape included
  (42.8s MP4). The door is not the problem; discovery is.
- Per the recipe's fallback clause, DISCOVERY fell back to non-X doors (HN Algolia date-filtered,
  HF, GitHub, byteshape.com, export.arxiv.org). Every quote below is verbatim from a page this seat
  fetched itself in this session; nothing snippet-grade is banked (snippet leads named in section 5).

## 1. Pass 1 (broad): candidates considered

HN Algolia `search_by_date` (numericFilters created_at_i>1789084800, i.e. 2026-09-11..10-11),
queries `GGUF` (22 stories) + `quantization` (14) + `quantized` (23): LoRA-over-GGUF woct0rdho
(10-10, estate-held), gpufind MCP (10-10), EmbeddingGemma2-in-browser (10-11), ByteShape Bonsai-2
reddit post (10-08), Reflex cold-start engine (10-07 + 09-23), Neural Dynamics arXiv 2609.32487
(10-07, off-area), Hopf Spherical hscq (10-06, sibling-banked), AMD Quark Strix Halo (10-06,
sibling-banked), arXiv 2606.00206 quantized-overthinking (09-27), HF-down noise (10-04), Gufo
Q6dense (10-03), Kokoro TTS (10-02), Janus Vulkan GGUF (10-01), GGUF Libra (10-01), Credence
(09-27), VeriLoop E2 (09-25, estate-held), UkisAI Swift (09-24 + 09-16), quant-delta-predictor
(09-23, sibling-banked), Lifeboat no-quantization (09-23), vla-edge Jetson (09-22), QLoRA-explained
substack (09-20), Ternary-Bonsai-8B (09-20), Weaviate 4-bit rotational (09-17), Quantifying Context
Rot (09-16), Sanskrit ASR onnx (09-16), GSQ-RCO (09-14, sibling-banked), Dwarf Star DeepSeek 4.1
(09-12), bartowski layout maps (09-12, sibling-banked). WebSearch adds: Unsloth Dynamic 3.0/2.0,
unsloth.ai blogs, spheron + kaitchup guides, HF calibration-issue, OpenRouter Bonsai-vs-Qwen tok/s,
mindstudio + regolo Bonsai reviews (snippet-grade). Direct: llama.cpp releases.atom (b11550-b11559),
b11556 release page. Total ~47 distinct in-window candidates; 8 primaries deep-read end to end
(byteshape.com/blogs/Qwen3.8-27B/, Ternary-Bonsai-2-27B-gguf card, unsloth Qwen3.8-27B-GGUF card,
llama.cpp b11556 release, ukisai/Swift-Qwen3.8-27b card, gufo Q6dense README, export.arxiv.org
id_list=2606.00206, fxtwitter door test).

## 2. Banked items (strongest first; quotes verbatim from pages this seat fetched)

### 2.1 ByteShape Qwen3.8-27B report - the independent measurement the vendor posts lack

https://byteshape.com/blogs/Qwen3.8-27B/ (blog 2026-09-14, updated 2026-09-18 adding Bonsai 2
plots). Quote: "We were impatient. This time, it worked out pretty well." Numbers read on the page:
five learned-compression builds on the quality-speed frontier across six GPUs - 2.56 bpw at 93.04%
of BF16, 3.23 bpw at 98.72% (11.0 GB), 3.84 bpw at 99.63%; KLD measured on ~5M response-only tokens
with per-request boundaries; benchmark suite includes BFCL V4 (8 subsets, tool calling) and
Multi-IF; MTP embedded draft head gives 1.28-1.66x, DFlash2 external draft 1.34-2.10x. The steal:
Prism-ML Ternary Bonsai 2, measured independently, scores "91.4% and 91.7% of BF16" (1.77/2.14
bpw) - BELOW ByteShape's own 2.56 bpw build (93.04%) and 6-7pp under Prism's self-claim (98.2%,
item 2.4). Vendor-announcement numbers on X carry a measurable inflation gap; independent
quality-normalized-vs-BF16 + KLD instrumentation is the estate's instrument shape.

### 2.2 llama.cpp b11556 - ternary sub-2-bit weights entered STOCK llama.cpp today

https://github.com/ggml-org/llama.cpp/releases/tag/b11556 (2026-10-11T13:31Z, PR #29600, commit
a9d27ac, co-authored with Georgi Gerganov). Quote: "Runtime support for Prism Bonsai 2 27B".
Release bullets name folded Hadamard weights in the converter; several bullets noted
"Assisted-by: Claude Code". This CURES two standing estate flags in one landing: the 09-20 splash
digest's "watch, don't run - fork-only load is a second engine-stability risk" and the Bonsai card's
own "stock llama.cpp won't run it". Sovereign serve path for 1.72 bpw weights is now the stock
local binary (no cloud, no fork) - the RQ4 acceptance-bar datum for this class.

### 2.3 arXiv 2606.00206 - quantization damage is behavioral before it is accuracy

https://arxiv.org/abs/2606.00206 (published 2026-05-29; authors Lotfi, Kirichenko, Li, Liu; HN
landing 2026-09-27, 13 pts). Quote (title, verbatim): "Quantized Reasoning Models Think They Need
to Think Longer, but They Do Not". Abstract (read via export.arxiv.org id_list, first-hand):
aggressive PTQ lengthens chain-of-thought while lowering accuracy; in up to 52% of failures the
model reaches the right answer mid-reasoning but never emits it; token-level KL vs FP16 spikes at
high-entropy positions; quantized models over-sample overthinking markers ("wait",
"alternatively"); a training-free logit penalty on those markers cuts CoT 12-23% while preserving
or improving accuracy across 5 models (1.5B-32B), 3 quant methods, 5 benchmarks, reducing
overthinking errors up to 58%. Feeds RQ1 directly: the janitor-tier battery must carry CoT-length
and marker-frequency axes, not just induction/retrieval retention; the logit penalty is a
steal-grade, training-free parity lever for quantized janitors.

### 2.4 Prism-ML Ternary Bonsai 2 27B card (DELTA on a held holding, not a new discovery)

https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf (citation September 2026). Quote: "98.2%
of FP16 intelligence retained: 84.78 average across 14 thinking-mode benchmarks - far above the
conventional IQ2_XXS build (72.59)". New over the 09-20 splash digest: PTQ1_0 dense-trit packing
1.75 bpw / 5.95 GB vs PQ2_0 2-bit-slot packing 2.13 bpw / 7.21 GB; AIME26 95.83 vs IQ2_XXS 57.50;
LiveCodeBench 90.07 vs 56.40; math 96.57 vs FP16's 97.06; intelligence density 0.457/GB vs IQ2_XXS
0.257; ~47 tok/s M5 Max, ~130 tok/s RTX 5090. Held context: estate already holds the splash digest
(memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md), Saluki's BFCL-derived
Bonsai score of 70 (hn sibling bank), and two reddit raw pulls. The vendor-vs-independent gap
(98.2% claim vs 91.4-91.7% ByteShape, vs 70/120-task BFCL underdog number) is the quant lore.

### 2.5 Unsloth Dynamic 3.0 - strongest vendor claim in the window, X-first, unverifiable locally

https://huggingface.co/unsloth/Qwen3.8-27B-GGUF (card + collections read; Dynamic 3.0 collection
"Updated Aug 26"). Quote: "Unsloth Dynamic v3.0 delivers >10% top-1% better accuracy at the same
size compared to every other provider". The X announcement post itself was unresolvable (discovery
walled, section 0; unsloth.ai blog deep-URL 403s this box). Sovereignty angle the sibling sweeps
did not carry: Dynamic 2.0/3.0 quants are built on calibration data Unsloth refuses to publish
(GitHub issue "Publish Calibration Dataset for Dynamic-GGUF-Quants-2.0", May 2026, 300K-1.5M+
hand-curated tokens) - the weights download but the recipe cannot be reproduced or audited on-box,
which fails the estate's sovereign-isolation bar for anything that must survive a cloud cut.

### 2.6 UkisAI Swift-Qwen3.8-27B (DELTA: the INT4 table under the held HN pull)

https://huggingface.co/ukisai/Swift-Qwen3.8-27b (created 2026-09-08, modified 2026-09-24). Quote:
"using 58.3% fewer thinking tokens while maintaining near-identical performance". New over the
10-10 raw HN pull: the card's W4A16/AWQ INT4 evaluations show the thinking-token savings SURVIVE
4-bit quantization - AIME INT4 82.67% base vs 84.00% Swift (Swift-INT4 above base-INT4); GPQA
88.38->88.28, MMLU-Pro 85.47->84.95 at BF16; LiveCodeBench v6 76.76->81.55 (improved). Token-
efficiency post-training and weight quantization compose instead of compounding - one more axis
the ceiling-tie re-run can include cheaply.

### 2.7 Gufo Q6dense on Strix Halo - throughput datum, provenance-thin

https://github.com/NinjaPear/gufo-Qwen3.6-35B-A3B-Q6dense (HN 2026-10-03). Quote: "3000 tok/s
prefill; 120 tok/s decode on Strix Halo." README read end to end: 3,095 tok/s pp at 4096 depth,
190.67 tok/s tg single-user, 334.35 aggregated with MTP, on iGPU; "a fork of gufo to support Qwen
3.6 35B A3B for workloads that prioritizes speed over intelligence". No quant internals on the
page; weights are third-party (ligamentexceed/...Q6dense-GGUF); no quality numbers. Banked at the
bottom for one reason: it is the local-iGPU serving band (sovereign path, no cloud) at a Q6-class
variant the estate has no other datum for. Provenance-thin by its own README - exactly the class
laws.md:114 says cannot carry decision force without a path:line receipt.

## 3. Research-question verdicts (X-lens)

- RQ1 (stratification law on the janitor fleet): X contributed nothing (walled). New public
  evidence says the battery needs a third axis beyond induction/retrieval retention: arXiv
  2606.00206's high-entropy KL spike + overthinking-marker oversampling + 52%
  right-answer-never-emitted (2.3). gemma:2b / gemma4 across Q8/Q4/Q3 should log CoT length,
  "wait"/"alternatively" frequency, and final-answer-emission rate, with the logit-penalty arm as
  the training-free cure to test. ByteShape's KLD-on-response-tokens instrumentation (2.1) is the
  copy-recipe for distribution sensitivity (VeriLoop's KLD-not-PPL law, independently reproduced).
- RQ2 (reddit census to 30-item floor): not curable from this seat - the reddit door is walled to
  WebFetch (doors.md third consecutive session) and PullPush returned empty for the one new in-window
  quant thread. What the X/announcement side holds that the folds missed: the vendor-claim
  inflation gap (98.2% self vs 91.4-91.7% independent vs 70 on a 120-task BFCL derivative) - any
  reddit lore built on vendor numbers inherits that gap.
- RQ3 (can provenance-only instruction rows carry decision force): the public mechanism answer is
  bartowski's canary pattern (sibling-banked, not re-banked): layout maps ship with a per-model-
  shape canary test and FALL BACK to the old heuristic on failure - provenance earns force only by
  executing a checkable artifact, else it steps aside. b11556 is the same law at the runtime layer:
  ternary support landed as runnable code + folded-weight converter, not as documentation. The 17-
  of-21 failed trust-byte probes (laws.md:89) say the estate's 24 rows are documentation-class
  until each carries an executed receipt; path:line stays the only carrier.
- RQ4 (sovereign-isolation acceptance bars): the demonstrable refusers-of-cloud in this window are
  stock llama.cpp (now incl. ternary, 2.2) and the Strix Halo iGPU fork band (2.7). The bar that
  NEW evidence exposes: reproducibility of the recipe. Unsloth Dynamic 3.0 (2.5) fails it (closed
  calibration data); ByteShape documents method + builds but ships via its own product
  (ShapeLearn code openness unverified - OWED); Bonsai 2 passed only today when the fork
  requirement died (2.2). REFUSE-cloud is necessary but not sufficient; REFUSE-unreproducible is
  the sharper test.
- RQ5 (sub-4-bit structured-output schemes, 1-8B, headroom above the ceiling tie): 2026 now has
  three scheme families with sub-4-bit numbers at 27B (none at 1-8B - the estate cell is still
  open): non-uniform sensitivity-allocated GGUF (GSQ-RCO 3.065 bpw sibling-held; Saluki 7.89GB
  IQ2-mix holds BFCL 88 vs 84; bartowski layouts shipping), learned scalar frontiers (ByteShape
  2.56 bpw at 93.04% incl. BFCL V4 subsets), and ternary+Hadamard (Bonsai 1.72 bpw: strongest
  density, weakest independent quality, BFCL-derivative 70, OpenRouter median 16 vs 57 tok/s -
  speed cost). A re-run with headroom: pick non-uniform assignment + tool-call-shaped calibration
  + constrained decoding, N >= 1000/cell, refusal-of-inapplicable-tool and CoT-length as
  first-class metrics, KLD not PPL.

## 4. Overlap record (commands this seat ran)

Grep over catalog/catalog.jsonl (snapshot 2026-10-11T08:51:55Z): "ternary bonsai" 3 rows
(splash_bonsai digest, frontier_olm_2026-10-09 _txt_1wj6c4l.txt, frontier_olm_2026-10-10
raw/bonsai2_8gb.txt); "bartowski" 2 (unrelated letta test config + this workflow's _tmp_pages
scratch); "ukisai" 1 (10-10 raw swift pull); q6dense/byteshape/"dynamic 3.0"/"layout maps"/
b11556/PTQ1_0: 0 rows. 2606.00206 / "think longer" / shapelearn / "compress and forget": 0 rows.
memory/ + watch/inbox recursive grep (completed before submit): bonsai/bartowski/q6dense/ukisai
hits only in run machinery (gapwave hn_x_fanout shortlists, splash_bonsai digest, file_dogfood
manifest, quote_audit concat, trajectory steps) and sibling raw pulls; the four new keys
(2606.00206/shapelearn/"think longer") appear ONLY as mentions: sweep/raw/hn_quantized.json (raw
HN title text), _kv_s6.xml (raw RSS), memory/runs/x_bookmark_harvest_20260905/
fxtwitter_raw.json.2091490338267341185 (one harvested tweet raw; the paper HAD X discussion in
early Sept - unmined, discovery-walled), quote_audit concat, trajectory steps. No bank, card, or
analysis file anywhere. Sibling sweep files read
directly: quantization-compression-hn.md banks bartowski (item 3) + Saluki; quantization-
compression-arxiv.md mentions none of my candidates; the 10-10 x file at this path banked none of
them. Verdict: 2.1, 2.2, 2.3, 2.5, 2.7 genuinely new; 2.4, 2.6 are explicit deltas on held holdings.

## 5. OWED / not done

- Zero X posts banked: discovery walled (section 0). The X-native corpus for this area (unsloth
  QAT posts, PrismML/ByteShape announcements, ggml_org b11556 note) stays unmined until a status-
  ID source exists. HN-full-text mining IS a working ID source (25+ live IDs proven) - it just
  holds zero in-window quant posts.
- mindstudio.ai "Bonsai 2 27B Benchmarks" (09-23), regolo.ai comparison (10-02), OpenRouter
  Bonsai-vs-Qwen tok/s: snippet-grade only, not fetched, not banked.
- ShapeLearn code openness (is the optimizer open-source?) unverified - byteshape.com product
  pages not fetched beyond the blog.
- arXiv 2606.00206 read at abstract depth (export API); body tables not read.
- No local runs (no ollama pulls, no battery execution) - this was a mining ask.

## 6. Instrument log (what this seat actually ran)

WebFetch: hn.algolia.com search + search_by_date x4 shapes (GGUF/quantization/quantized/ggml_org
+ twitter-URL mining x2); raw.githubusercontent.com unsloth README; unsloth.ai/blog (nav shell)
+ /blog/dynamic-v3 (403); huggingface.co x4 (unsloth Qwen3.8-27B-GGUF, prism-ml Ternary-Bonsai-2,
ukisai Swift, blog/bartowski page was sibling's; mine: three cards + collections);
github.com releases x2 (releases.atom feed, tag/b11556); NinjaPear gufo README; byteshape.com
root + /blogs/Qwen3.8-27B/; export.arxiv.org api/query id_list=2606.00206; api.pullpush.io
ids=1wju8ky (empty); html.duckduckgo.com (bot wall); bing.com (site: mangled); xcancel.com (451);
threadreaderapp.com/search (instructions shell); api.fxtwitter.com door test (200, media shape
verified). WebSearch x6 (three useful: unsloth dynamic v2/3 surfaces, ByteShape comparison
surfaces, Bonsai review surfaces; three degraded/429). Bash grep: catalog.jsonl + memory/ +
corpus/steal overlap walks (section 4). Scratch: none written beyond this file (sibling _qz_*
scratch reused read-only).
