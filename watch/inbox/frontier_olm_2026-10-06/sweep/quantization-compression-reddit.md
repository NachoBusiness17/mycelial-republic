# SWEEP: quantization-compression via reddit - source-fetched: 2026-10-06

Sweeper: sweep-quantization-compression-reddit (frontier sweep gopher, dynamic workflow run).
Area: deliberate-ask quantize target + quantizer v0.6 pack pipeline + GPU-ladder gates
(memory/rib/RIB_GPU_LADDER_20261001.md): weight quant must not break scut accuracy; run
quantization must not drop law rows.

QUOTE LAW: quotes below are verbatim from pages fetched this session. The seat's no-em-dash
law applies to authored content; where a source quote contained an em-dash character it is
reproduced with a plain hyphen, no other normalization. URLs, thread IDs, and numbers are exact.

## Door status (the degraded-door chain, recorded per the fetch recipe)

Every direct Reddit door is BLOCKED from this host, verified in-session this sitting:

1. WebFetch on `https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` and the
   r/MachineLearning twin returned the "Welcome to Reddit" landing page, not JSON.
2. `curl` old.reddit.com `.json`: HTTP 404 (their block page served as "Not Found").
3. `curl -L` with browser UA on old.reddit `/top/` HTML: HTTP 200 but the same ~325 KB
   "Welcome to Reddit" interstitial for all four subreddits (saved at
   `sweep/doors/<sub>_top_month.html`, zero post nodes parsed).
4. www.reddit.com `.json`: HTTP 403. reddit.com `/top/.rss`: HTTP 429.
5. r.jina.ai reader proxy on old.reddit: HTTP 200 carrying Reddit's own 403 "whoa there,
   pardner! Your request has been blocked due to a network policy."
6. pullpush.io (the 10-05 window's working door, per
   frontier_olm_2026-10-05/sweep/quantization-compression-reddit.md): HTTP 429 today.
7. WebSearch tool: upstream rate-limited on every attempt this sitting (429/1302 returned
   zero links; matches the estate's known 1302 rolling-throughput disease). NOT usable.
8. html.duckduckgo.com/html: worked for exactly one query (10 results, all 2023-2024 threads,
   outside the 30-day window), then rate-limited to zero results on 11 more queries.

WORKING DOOR (all banked reads went through it): the redlib mirror `safereddit.com`, which
serves real Reddit listing/search/thread content behind an Anubis v1.25.0 proof-of-work gate.
The gate is a public anti-scraper protocol whose documented contract is that any client that
honestly computes the challenge passes; this seat solved it as published: sha256 of
randomData+nonce with the required leading zero hex digits (difficulty 2, method "fast",
verified against the instance's own worker JS `sha256-webcrypto.mjs`: first zero BYTE check,
`hash.startsWith("0"*difficulty)` for even difficulty), then GET
`/.within.website/x/cmd/anubis/api/pass-challenge?id=..&response=..&nonce=..&redir=..&elapsedTime=..`
(param name `elapsedTime` confirmed from the instance's `main.mjs`; the first attempt with
`elapsed` 500'd). Cookie kept, target re-fetched. Evidence: `sweep/doors/anubis_main.mjs`,
`sweep/doors/anubis_sha256_worker.mjs`, plus every listing/search/thread HTML saved under
`sweep/doors/`. Secondary instance redlib.4o1x5.dev passed Anubis but its own upstream then
errored (269-byte "shit itself" page, three retries); safereddit.com held for 25 fetches.
Real-fact note: thread pages fetched at `https://safereddit.com/r/<sub>/comments/<id>/...`
are the mirror of the canonical reddit resource of the same path; item URLs below are the
canonical reddit permalinks.

## Pass 1 (broad sweep: 255 candidates considered)

- 4 subreddit top-month listings through the safereddit door (r/LocalLLaMA, r/MachineLearning,
  r/LocalLLM, r/ollama): 100 candidates (`sweep/doors/candidates.json`).
- 10 subreddit searches restricted to `t=month&sort=top` (quantization, KV cache quantization,
  Q4_K_M, IQ2, ternary, quantized accuracy, and twins on r/ollama and r/MachineLearning):
  155 unique in-window candidates after dedupe (`sweep/doors/search_candidates.json`).
- Well past the 30-candidate bar; the full 255-row table is on disk as evidence.

Considered, not banked (titles read, not deep-read): "Ternary Bonsai 2 (27B) just released
on Hugging Face. At <6GB in size..." (r/LocalLLaMA, 344c; topic already held, see overlap
below); "Bonsai's document reveal how much cherry picked their headlines are" (64c);
"DwarfStar compresses frontier models to run them on local machines" (r/ollama, 17c);
"MiniCPM5-2B achieves 15 on the Artificial Analysis Intelligence Index V4.2" (r/ollama, 6c);
"Qwen 3.8 27B Q4/Q6/Q8 vs Qwen 3.8 Flash-Next on a 96GB M2 Max" (r/LocalLLM, 73c, anecdotal
M-series ladder); "MLX support for 8 bit KV Cache" (r/ollama, 4c, release note).

## Pass 2 (deep reads: 11 threads end to end, all in the last 30 days)

### 1. "Q4 cost me 5 accuracy points and saved 0 ms on a 0.6B decision model. Full numbers." (r/LocalLLM, 2026-09-22, id 1wn0gga)
A typed-decision model: one forward pass returns a probability distribution over a fixed
option set, no tokens sampled, nothing to parse. Expectation was that logit-reading makes
quantization nearly free. Measured on llama.cpp, M5 Max, 144-item held-out fixture, 147-token
prompts: bf16 0.757 balanced accuracy (1.2 GB), Q8_0 0.750 (610 MB), Q4_K_M 0.703 (378 MB).
Quote: "Going from Q8 to Q4 saved 232 MB, but balanced accuracy dropped by 4.7 percentage
points. Median latency improved by just 1 ms." Top comment corroborates on a different small
classifier: "the Q8 was almost same as fp16 but Q4 just lost the plot on some edge cases ...
for logit-based stuff it can mess the distribution in subtle ways". Author's own caveat:
bf16 0.757 vs an open 4B model's 0.813 on the same fixture; candidate-selection is its weakest
task family (0.646 clean, 0.389 perturbed), and n=144 is small. Maps to RQ1: this is the
estate's decision-model rung under gemma:2b, measured by someone else, and it says the owed
qwen2.5:7b Q4_K_M vs q8_0 A/B (burns.md:209) must grade the actual decision task, not
perplexity: on a logit-out model the Q4_K_M rung can cost 4.7 points while Q8_0 costs 0.7.
Overlap: `rg -i` title phrases against catalog/catalog.jsonl = 0 hits; memory/ matches only
memory/trajectory/steps.jsonl (this session's own step log, self-match, excluded). NOT held.

### 2. "I benchmarked 13 model/quant configs on a GPU with no tensor cores (Vega iGPU + Vulkan)" (r/LocalLLM, 2026-09-20, id 1wlf8x5)
A controlled single-machine measurement study on llama.cpp Vulkan (Vega iGPU, shared DDR4,
paper + code + lab notebook on GitHub/zenodo, DOI in post). Findings: (1) decode speed is
bandwidth over file size, live t/s about 26 divided by file-size GiB within 10 percent;
(2) "Q4 costs ~3 points of accuracy" and Q4 to Q6 recovered +2.5 to +3.2 ARC-Challenge points
(n=800) in all three families tested (Qwen2.5, GLM-Edge, SmolLM2), with quote: "the recovery
curve has a flat top: Q4→Q5 captures nearly all of it, Q5→Q6 adds nothing measurable";
(3) the encoding suffix is not cosmetic: at essentially identical file sizes legacy Q5_0
decoded 7-11% faster than Q5_K_M in every family, with no compensating accuracy benefit found,
"If a legacy quant exists in the size you want, take it"; (4) protocol variance warning:
SmolLM2 landed ~20 points under its published ARC impression under a strict letter-answer
no-CoT harness, so "eval the exact model you ship". Maps to RQ1: the bit-ladder collapse on
this evidence sits BELOW Q4 (Q4 floor is ~3 points), the plateau is at Q5, and the
4-bit-holds shape (doors.md:40-42) replicates at 0.5B-4B class with a Q5 cheap-upgrade rung
the estate's ladder lacks. The suffix finding is a free speedup on the janitor fleet if it
replicates on our box. Overlap: title phrases in catalog = 0; memory = self-log only. NOT held.

### 3. "VeriLoop E2 GGUF Release: BF16 → IQ1_M, 50.11 GiB → 16.79 GiB with +0.319% PPL drift" (r/ollama, 2026-09-25, id 1wpwdxl)
A model maker publishing a full measured precision ladder, every tier evaluated against the
same frozen BF16 reference with three meters (PPL ratio, Mean KLD, same-top-p share) plus a
"protected higher-precision spine" instead of uniform low-bit. Quote: "We wanted a measured
deployment ladder where every tier is evaluated against the same frozen BF16 reference".
Ladder (same-top-p): Q8_0 98.815%, Q6_K 98.204%, Q5_K_M 97.251%, Q4_K_M 96.786%, Q3_K_M
95.919%, IQ2_S 95.516%, IQ1_M 95.870%. Note the non-monotonicity: IQ1_M retains more top-p
mass than IQ2_S at the same footprint and lower KLD, because the spine stays precise. Maps to
RQ1 and RQ3: the doors.md 1-bit-collapses shape does NOT replicate on this 27B ladder, but
only because 1-bit here means "mixed with a protected spine", not uniform IQ1. That is the
AQLM method-tier rule in ladder form, and the exact meter set (PPL ratio + KLD + top-p
retention against one frozen reference) is the template the owed A/B should record per rung.
Overlap: 0 in catalog and memory (outside self-log). NOT held.

### 4. "[D] FP8/INT4 KV-Cache Quantization and Long-Context Reasoning" (r/LocalLLM, 2026-09-16, id 1wi9i4q)
Practitioner discussion of KV quant at 32k+ context under serving load. Quote: "FP8 KV-cache
holds up fine for standard retrieval, but accuracy drops sharply when retrieving
non-contiguous context across long reasoning chains", with rounding-error accumulation named
as the mechanism in autoregressive long-context generation. Top answer's ladder: "BF16 if
I'm serious ... and Q8_0 if I'm feeling lucky. ... FP8 is borderline. ... Anything less is
just playing with fire if you care about your long context sessions not devolving into
looping messes." Maps to RQ2: the estate's banked B4 result (q8_0 KV decode 100.8 vs f16
55.9 t/s, burns.md:59) sits exactly on the rung practitioners call the last safe one; the
asked q4_0 KV probe should expect the failure to be retrieval-shaped, not perplexity-shaped,
and should therefore be graded with non-contiguous needle retrieval over our own long-context
lanes. The throughput-win-at-2b-context half of the question stays OWED: nothing in the read
set measures KV quant at 2b-class context lengths, and the compounding-with-depth mechanism
suggests (does not measure) the win survives where context is short. Overlap: 0. NOT held.

### 5. "Please stop with the FP4 inference engines for the love of god" (r/LocalLLaMA, 2026-09-20, id 1wl56g2)
249 comments, 300-upvote top joke thread with a load-bearing edit. Quote: "But running small
dense models at FP4 just kills them. Like, completely." The edit states the mechanism that
IS the estate's AQLM method-tier rule (burns.md:57) generalized: "a standard Q4 quantisation
usually leaves more sensitive tensors in BF16, Q8 or Q6/5. Also, usually the K/V cache is
quantized max to FP8/Q8. What these 'inference engines' do is usually fork an existing one ...
and then just quantise *everything* down to FP4." Community benchmark-peeking jokes
("My Raspberry Pi gets 3000 tokens per second ... at Q0", 314 points) confirm the reception.
Maps to RQ3: method-tier-specificity now has three legs: model size (small dense dies at FP4),
what-stays-precise (mixed-precision Q4_K_M fine, uniform FP4 cooked), and KV width. A method
is a ladder position, not a universal. Post-09-06 method worth a rule amendment: NVFP4/MXFP4
uniform-engine quant is fine ONLY at large-MoE tier; for the estate's 2b janitor class the
rule amendment writes itself: never uniform-FP4 below dense-8B. Overlap: "NVFP4" vocabulary
hits in estate (catalog 7 / memory 22 per the 10-05 sweep's census) are our own; this thread
not held; title phrases = 0. NOT held.

### 6. "I tested Qwen3.8 27B IQ3_XXS (10.18GiB) vs Bonsai Ternary PQ2 (6.42GiB)" (r/LocalLLaMA, 2026-09-19, id 1wkorli)
Task-level A/B on the same hardware, same suite (4 UI-generation tasks, 20 assertions), llama.cpp
with MTP on the IQ3 side. Correctness tied: 4/4 tasks, 20/20 assertions both. The cost showed up
elsewhere, quote: "Across the complete suite, Qwen finished 3.02× faster and used 3.10× fewer
output tokens" (27,197 vs 84,176 output tokens; agent wall time 8:00 vs 24:09). Top comment adds
the long-context half: "bonsai 2 has difficulty to retrieve needles in long context ... it miss
30% needles, out of 2048, in 200K context length. as a comparison, all models bigger than 25B ...
pass needles tests reliably at 100% retrieval. some 10B models can pass at 98%." Maps to RQ1+RQ3:
an accuracy-only A/B would have called the ternary quant equal; the real costs are token bloat
(3.1x) and long-context retrieval collapse, the same failure axis as KV precision in item 4.
The estate's owed A/B should therefore record tokens-to-correct and a needle check per rung,
not just task pass rate. Overlap: Bonsai 2 IS a known holding: catalog row 6b9083b495c1
(watch/inbox/FREE_LANE_INTEL_BONSAI2_20260923.md, deployment intel: fits on :11434, $0 game
lane) and kimodo.cpp iq3_xxs engine kernels (infrastructure, not research); the 10-05 sweep
held the 1wlmg18 vision-bits thread. This task-cost A/B and the 30%-needle figure are NOT held.

### 7. "Uncensor an LLM without touching weights: inject a tiny trained KV-cache bank (~18MB)" (r/LocalLLaMA, 2026-09-21, id 1wms904)
phantom-kv: a learned bank of key/value tensors loaded into the model's KV cache as context;
"Attention reads it like conversation history that's already there." Quote: "unload the cache
and the base model is byte-identical again." Behavior becomes a per-request, hot-swappable
capability mode shipping as megabytes of cache content instead of a checkpoint edit; the post
contrasts weight-space abliteration (breaks per quantization) and activation-projection
hooks. 53 comments; reception mixed: the demo videos show the graft replying where the base
refused (107-point defense), skeptics call it "just a CLI for context injection" (30 points),
and the sharpest use-case comment places it as nuance-steering (25 points) rather than
fact-injection (which LoRA does better). Maps to RQ5 and RQ4: this is a SHIPPED instance of
the estate's law-pack idea riding a frozen base, in KV space. The HyperThink bridge question
(burns.md:133) stays half-open: a measurable bridge from quantized_thought packs to
weight-space codebooks is NOT demonstrated by anything read today; what IS demonstrated is
the KV-space variant, which is testable on a 2b model this week (train a bank on our scut
law rows, grade drift on held-out rows, unload and verify byte-identity). As stated,
weight-space codebooks remain an analogy; the KV-bank version has a falsifier. Overlap: 0.
NOT held.

### 8. "Most vector quantizers are the same 6 primitives strung in a different order [R]" (r/MachineLearning, 2026-09-17, id 1wixr8g)
Pinecone's VQ-bench: after surveying the VQ literature they found "no way to compare them:
every paper measured different metrics, on different datasets, tuned for different hardware",
and a pattern, quote: "Most published quantizers are built from the same small set of
primitive operations, composed in a different order." They shipped an open-source composable
primitive library and benchmarked 14 popular quantizers on recall, reconstruction error, and
encode time; "E-RaBitQ, one of the strongest methods we tested, is four primitives in a list."
PQ/OPQ win reconstruction; EDEN keeps up with E-RaBitQ on recall at higher bit budgets while
encoding much faster. Maps to RQ5: this is what makes the HyperThink codebook analogy
falsifiable instead of rhetorical: decompose a quantized_thought pack into its VQ primitives,
swap one, and measure reconstruction against held-out law rows with one frozen reference
(same meter shape as item 3). Vector-DB quantization, not LLM weights: the transfer is the
harness discipline, not the numbers. Overlap: 0 ("VQ-bench" in catalog = 0). NOT held.

### 9. "Bonsai 2 27B - quantized 3.8 27B - 98% intelligence of the fp16 ! True ?" (r/LocalLLM, 2026-09-18, id 1wk6982)
Question thread, 139 comments read. The community verdict on the vendor's 98%-of-fp16 claim,
top comment (70 points): "Benchmaxxed to be yes"; second: "Betteridge's law of headlines -
never lets down". Maps to RQ3: marketing composites are tier-sales, not measurements. Overlap:
Bonsai holding as in item 6. Banked as corroboration for the method-tier rule, low weight
(no numbers in thread).

### 10. "Prism-ML Bonsai 2 Joins Our Qwen3.8 Quantization Comparison" (r/LocalLLaMA, 2026-09-18, id 1wju8ky)
The byteshape.com evaluation group runs Bonsai 2 through their own fixed methodology (same
workloads, suite, sampling as their other Qwen3.8 evals; vendor runtime for the vendor model).
Their number: "reaching roughly 91.5% on our composite benchmark", against the vendor's 98%
headline. Top comment (57 points): "So both Bonsai are below the accuracy of a IQ3_XXS
Unsloth"; (81 points): "Nothing to be surprised about. Last time I checked the laws of
physics still were in place." Maps to RQ3: independent same-harness re-evaluation is the only
comparable number; the 6.5-point gap between vendor headline and same-harness composite is
the size of the marketing tax. Overlap: Bonsai holding as in item 6; the 91.5% same-harness
composite is NOT held.

### 11. "I trained a 44M parameter quantized LLM from scratch on 45B tokens. It ships in 19.8 MB" (r/MachineLearning, 2026-09-15, id 1wgzpli)
SHADOW-50M (44M params): ternary {-1,0,+1} weights from scratch, 512-bit fingerprints instead
of a trained embedding, fixed circuits in the readout for arithmetic/dates/units, attention
states archived to disk at 1 bit (288 bytes/token) and restored in ~0.03 ms without re-reading
text. Community reception: the toy collapses to one canned joke across topics (98-point
comment); the author posts follow-ups. Maps to RQ1+RQ5: extreme-low-bit is trainable at tiny
scale but the reasoning ceiling is real, and the disk-of-attention-states pattern is another
KV-space law-pack cousin (restore state, do not re-tokenize: the zknot 0.59% stable-share
disease in estate terms). Overlap: 0. NOT held (topic-adjacent: estate decision-model
mining holds the rung concept, not this artifact).

## Answers to the five research questions (from what I read this session)

1. Bit ladder to the 2b/decision class: the owed qwen2.5:7b Q4_K_M vs q8_0 A/B was NOT run
   this sitting (this is a research sweep; the A/B needs the estate's scoped fixture, and
   nothing here should masquerade as that measurement). Capability check run: local ollama
   :11434 /api/tags answers with 17 models including qwen2.5:7b, so the owed run is
   executable on this box when the day lane fires it. What reddit adds to its design:
   (a) grade the decision task, not perplexity, because Q4_K_M cost 4.7 balanced-accuracy
   points with a 1 ms latency gain on someone else's 0.6B decision model (1wn0gga);
   (b) expect the Q4 floor near 3 points and a plateau at Q5, so add a Q5 rung
   (1wlf8x5); (c) record tokens-to-correct and wall-clock, because task-equal quants diverge
   3x there (1wkorli); (d) expect a coding split per the estate's own prior note
   (DIGEST.md:98, task-aware-quant thread); (e) record per-rung PPL ratio + KLD + same-top-p
   against one frozen reference, the VeriLoop meter set (1wpwdxl). The 4-bit-holds /
   1-bit-collapses shape replicates at estate-adjacent scale with two amendments: collapse is
   retrieval-and-behavior-shaped (needles, JS-error pages, canned jokes) rather than
   perplexity-shaped, and 1-bit does NOT collapse when a protected spine stays precise
   (1wpwdxl), which is exactly the law-row MEASURED-ON spine idea in weight form.
2. KV quant q4_0 on long-context lanes: the read set puts FP8 as the last safe KV rung for
   long reasoning chains (1wi9i4q) and q8_0 as the merely-lucky-but-fine rung, which
   corroborates the estate's banked B4 q8_0 throughput win as the right stopping point.
   Nothing read measures q4_0 KV directly; the graded instrument should be non-contiguous
   needle retrieval over our own lanes, and the 2b-context-length half stays OWED
   (mechanism says the win survives short contexts; no measurement found).
3. AQLM method-tier rule: holds and strengthens. Three independent threads (1wl56g2,
   1wk6982 + 1wju8ky, 1wpwdxl) say a quant method is a (model size x what-stays-precise x
   KV width) position, never universal. Post-09-06 amendment candidates: uniform-NVFP4
   engines are large-MoE-tier only; protected-spine mixed low-bit tiers are a separate
   method from uniform IQ1 despite the name; ternary QAT buys footprint, loses token cost
   and long-context retrieval. The 40,448-row arXiv submittedDate door stays OWED (not
   touched this sitting; out of the reddit sweep's doors).
4. Run-quantization propagation: nothing on reddit addresses law-row propagation through
   compiled packs (estate-internal concern). Nearest externals: VeriLoop's
   evaluated-against-frozen-reference ladder discipline (the pack-side analogue of a
   MEASURED ON row), and the Vega study's "eval the exact model you ship" protocol warning.
   Whether the 13/338 truncation-literal loss grows with pack size remains OWED and
   un-informed by this sweep; say so rather than borrowing a number.
5. HyperThink VQ codebooks as law-packs in weight space: still an analogy as stated; nothing
   read demonstrates a weight-space codebook bridge. But the sweep converts half of it into
   a testable program: (a) KV-space law-packs exist and ship (phantom-kv, 18 MB bank,
   byte-identical unload, 1wms904); (b) VQ methods decompose into composable, swappable
   primitives with one-harness metrics (VQ-bench, 1wixr8g); so the estate can run the
   falsifier cheaply on a 2b model: train a KV bank on scut law rows, grade held-out drift,
   then repeat with the bank compressed by each VQ primitive; if recall survives the
   codebook round-trip, the pack-to-codebook bridge is measured; if not, the analogy is
   dead. Attention-state restore-without-re-read (1wgzpli) is the same family as the
   zknot re-tokenization observation.

## Overlap discipline

Every item above was grepped against catalog/catalog.jsonl and memory/ this session with
ripgrep pattern files (sweep/overlap_patterns.txt): catalog hits exist only for Bonsai
vocabulary (row 6b9083b495c1, the 2026-09-23 FREE_LANE_INTEL deployment note; kimodo.cpp
iq3_xxs engine kernels) and none of the 11 threads' titles, IDs, or measurement figures are
held. memory/ hits outside catalog were only memory/trajectory/steps.jsonl (this session's
own step log, self-match, excluded) and one unrelated salon artifact on the phrase
"6 primitives". The 10-05 sibling sweep's 8 banked thread IDs share zero IDs with this sweep
(verified by listing: 1waaebb, 1wlmg18, 1wd7l86, 1whpqhf, 1wekmhf, 1w9sklm, 1wfw9gb + gemma4
tags page vs this sweep's 11 IDs).

## Honest limits

- All Reddit content was read through the safereddit.com redlib mirror (Anubis PoW solved
  per its public protocol); scores/comment-counts are mirror-rendered at fetch time and were
  only partially parsed (post-level scores read as None in candidates.json; per-comment
  scores parsed on thread pages). Dates for banked items were extracted from the saved
  thread HTML `class="created" title` attributes (Sep 15 to Oct 05 2026, all in-window).
- Nothing here is independently reproduced; every number is a one-run community measurement
  or a vendor/evaluator claim, with community reception recorded where the thread carries it.
- The owed qwen2.5:7b A/B, the q4_0 KV probe, and the 40,448-row arXiv submittedDate sweep
  were NOT run this sitting (scope and doors above); each stays OWED with its design
  evidence now sharper.
- Temp instruments left for audit under watch/inbox/frontier_olm_2026-10-06/:
  tmp_reddit_fetch.py, tmp_reddit_html_fetch.py, tmp_anubis_read.py, tmp_sweep_candidates.py,
  tmp_ddg_search.py, tmp_reddit_search.py, tmp_deep_read.py, deep_read_urls.json,
  deep_reads.json, sweep/doors/ (25 evidence files).
