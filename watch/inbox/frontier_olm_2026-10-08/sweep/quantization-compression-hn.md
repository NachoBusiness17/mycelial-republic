# Sweep: quantization-compression via Hacker News - 2026-10-08

source-fetched: 2026-10-08. Door: HN Algolia API (search_by_date + search, tags=story,
numericFilters=created_at_i>1788739200 = 2026-09-07, 30-day window), then per-item page
fetches; HN thread news.ycombinator.com/item?id=... for strong hits; arXiv export API for
the RQ5 release scan; two WebSearch probes for the RQ4 market-data check (HN alone carries
no price tables this window). All quotes below are from pages I fetched this sitting.

## Doors and degradation

- hn.algolia.com: worked, every query sub-second. Queries run: quantization, GGUF,
  quantized, llama.cpp (all search_by_date, 30-day filter), plus relevance search on
  "GPU prices" and "quantization benchmark", and search_by_date on "RTX 5090".
  No timeouts this sitting (the day-7 sweep lost three complex boolean queries; the
  plain-term shape held here).
- news.ycombinator.com item pages: worked for 49953495 (422-comment thread) and 49702319.
  No timeouts.
- arXiv export API: NEW SHAPE PROVEN. The doors lens (lens/doors.md:39) recorded that
  sortBy/phrase variants hang. This sitting the submittedDate-range filter shape returned
  fine: `search_query=abs:quantization+AND+abs:GGUF+AND+submittedDate:[202610010000+TO+
  202610082359]&max_results=15` gave 1 entry in-window (2610.04403, fetched in full).
  The sort variant stays untested; the date-range shape is the new minimal shape.
- WebSearch (z.ai web_search_prime): used only for RQ4 market data; its numbers are
  second-hand summaries, flagged as such below.

## RQ1 status: the owed A/B is still UN-RUN, and this seat did not fire it

The ask's research question 1 says "run the amended A/B end to end". Not run, on measured
grounds, and the non-run is itself instrumented:

- Box state this sitting: `curl -s http://localhost:11434/api/tags` returns 17 models.
  Arm A IS present: qwen2.5:7b, Q4_K_M, digest 845dbda0ea48ed749caafd9e6037047aa19acfcfd
  82e704d7ca97d631a0b697e - the exact digest the spec pins (QUANT_AB_SPEC_AMEND.md:53).
  Arm B is ABSENT: no qwen2.5:7b-instruct-q8_0 in the tag list (names: gemma2:2b-instruct
  -q5_K_M, gemma:2b, Ternary-Bonsai-2-27B, athena-class, ling-3.0-flash, qwen2.5:7b,
  maze-keeper, deepseek-r1:1.5b, qwen2.5vl:3b, qwen2.5:32b, qwen2.5-coder:7b, qwen-desk,
  qwen2.5:3b-instruct, gemma4-desk, gemma4, gemma4-hermes, nomic-embed-text).
- Firing therefore needs the 8.1 GB pull first (spec line 55), then ~100+ runs at 50 per
  arm minimum over 10 tasks x 5 prompts (spec legs 1-2). The spec's own status line
  reserves that: "Nothing here executes the probe; the burns ledger owns firing"
  (QUANT_AB_SPEC_AMEND.md:4-5), and today's burns lens re-ows it with "the A/B itself has
  no run receipt I found. Owed." (lens/burns.md:206-208). A sweep seat firing it would
  preempt the owed-probe queue; a partial run (one prompt, few tasks) would manufacture
  exactly the screening artifact the amendment exists to forbid (spec leg 2). So: NOT RUN
  here, still owed, arm A verified on box, arm B needs one pull.
- Which tasks flip verdict: unanswerable until the run exists. Public priors banked below
  (2610.04403) say what to expect per channel: at 7.6B params the lexical channel should
  be flat at Q4_K_M ("Q4_K_M remains lexically clean at >=1B"), so flips, if any, should
  come from the tool-failure-recovery pipeline itself (leg 2's full-pipeline verdict) and
  the strict-parse rider (leg 4, Qwen-flat prior stated up front).

## Pass 1 - candidates considered (on-topic, 30-day window; 41 unique)

Strong new ground: 49953495 Strata 125B-on-4090 (930 pts / 422 comments); 49702319 RTX
5500 Pro Blackwell 84GB; 49936468/49954024/49956396/49967869 MicroCenter RTX 5090 ID +
no-export pledge (4 dups); 49701038 RTX 5090 ($9,500) vanishes from US retail; 49951188
Flash-Next 177B on RTX 5070 12GB + 32GB RAM; 49941824 Gufo Qwen3.6-35B-A3B-Q6dense Strix
Halo (3095 tok/s prefill); 49829063 gpufind.cloud rent-vs-buy calculator; 49792523
computeassay graded GPU cloud price registry; 49691112 Kairo routing from RTX 5090
measurements; 49999451/49819913/49903234 Reflex cold-start GGUF engine (3 dups);
49966238 finetuned 1.5B Qwen bash generation; 49925937 GGUF Libra; 49861867 Credence
typed decisions; 49644045 GLQ trellis-quant vLLM plugin; 50002054 Bonsai 2 joins
ByteShape Qwen3.8 quantization comparison; 50000321 Neural Dynamics quantized units;
49778955 QLoRA explained; 49804932 VLA runtimes on Jetson Thor.
Held/banked ground resurfaced (not re-banked): 49611128 Quesma ladder (286 pts, day-7
banked), 49926773 Janus Vulkan GGUF (106 pts, day-7 OWED-not-read, read today), 49676635
bartowski per-tensor maps (banked), 49703818 GSQ-RCO Flash-Next (banked), 49727511/49833102
Swift-Qwen3.8 (banked), 49869861 quantized reasoning think-longer (banked), 49823211
quant-delta-predictor, 49822130 Lifeboat, 49847732 VeriLoop E2 (day-6 register row 15),
49812339 transformers llama.cpp quants, 49813964/49774861 Bonsai GGUFs, 49942092/49934323
decision models (banked), 49980637 Hopf, 49975499 AMD Quark (banked), 49876817 Intel Arc
2.2x, 49742415 Mozilla server benchmark (day-1 deep-read), 49859982 prompt lookup drafting
(89 pts), 49911995 Magnitude, 49845314 llama.cpp fork multiGPU MoE, 49814172 under the
hood, 50002660/49997807/49998043 Windows ML / DeepSeek V4 Flash local.
11 pages fetched and read end to end this sitting (see banked items plus held ground).

## Pass 2 - answers to the five research questions

### RQ1+RQ2. The A/B and which pins are load-bearing

- The engine variable is now measured at task level, not just throughput level. On the
  Strata thread (49953495), Jackson__ ran a 50-image vision benchmark, temperature 0,
  SAME GGUF weights, BF16 vision towers in both arms: Strata median error 154.8 px vs
  llama.cpp 46.5 px - "a gap comparable to 9B vs 35B model differences" (fetcher-reported
  numbers); amitp85 reported similar Strata-vs-llama.cpp hallucination differences. This
  is the day-7 "harness/serving stack dominates" finding (DIGEST.md:16) replicated at
  task level with weights held fixed. Consequence for the A/B pin contract: the spec's
  export-cast rider (leg 6: hash the GGUF, pin the exporter) is necessary but not
  sufficient - the serving binary identity is a third arm of the pin.
- Mozilla's controlled benchmark (HELD ground, day-1 deep-read, re-verified today from
  the live page) quantifies how much a build pin is worth: same llama.cpp commit built
  with two Vulkan shader toolchains moved prompt processing +25.9% (0.8B) / +63.3% (9B)
  and decode +18.2% (9B) on the Deck; "Check how your server was built, not just which
  one it is. The same engine compiled two ways differed by 1.6x on the Deck." Their pin
  grammar is exactly what the A/B receipt should carry: llama.cpp b10441 (commit
  0177dcc73), Ollama 0.34.0, LM Studio runtime 2.28.2, llama-benchy 0.4.0 - named bytes,
  not names.
- VeriLoop's ladder (HELD ground, day-6 register row 15) is the reference for the
  artifact pin: every tier "built directly from the canonical BF16 GGUF and measured
  against one frozen BF16 logit reference", per-tier PPL ratio / mean KLD / same-top-p
  published for all 8 rungs (BF16 50.113 GiB -> IQ1_M 16.790 GiB), and their own boundary
  line, verbatim: "these are quantization-retention measurements, not downstream
  benchmark-loss percentages." KLD/PPL is a diagnostic channel, never the verdict - which
  is the same structure as the spec's leg 3 (diagnostics never headline).
- Minimal pin contract for future quant A/Bs on this box (synthesis, each element
  traced): (1) GGUF blob sha256 per arm (spec leg 6); (2) exporter/conversion toolchain
  named (spec leg 6, 2610.07853 rider); (3) serving binary + build: ollama version and
  its bundled llama.cpp commit, or the llama-server commit if raw - Mozilla grammar,
  Strata thread shows task-level flips at identical weights across engines; (4) serving
  cache state pinned-or-reset between arms (spec KEPT line 59-60; Mozilla restarts
  servers before every run, "so weights and KV cache start cold", and interleaves to
  defeat machine drift); (5) token counts on EOS-terminated or equal-cap responses only
  (spec KEPT); (6) verdict unit declared = full-pipeline task success pooled over all
  tasks x >=5 prompts (spec legs 1-2; the source paper's own four choices); (7) imatrix/
  UD status of each arm named in the receipt (day-7 thread caveat, wgd/kouteiheika: UD
  quants are already mixed-precision, "4-bit isn't actually a 'true' 4-bit"); (8) the
  lexical rider below if cheap.
- Load-bearing ordering for comparability: prompt phrasing first (matched-task deltas
  +8.3 to -50.0 to +35.0 at exactly the estate's pair, spec line 38-41), then task
  screening (17.5-point artifact, spec line 42-44), then parsing policy (Llama-side
  +28.3 -> -15.0 flip, Qwen-flat prior, spec line 45-46/74-77), then uncertainty unit.
  The four are not symmetric: choices 1-2 manufacture verdicts at the headline, 3-4
  corrupt channels. On this box, choices 1-2 are enforced by the amended legs; 3 is a
  logged rider with a stated prior; 4 is per-task spread reporting.

### RQ3. Per-role quant ladder vs one global quant

Public evidence this window supports per-role over global, three ways:

- 2610.04403 (arXiv, 2026-10-03, fetched in full): regime split by scale at Q2_K -
  "total collapse into unusable builds, severe semantic dissociation in sub-2B models,
  and mostly robust preservation above about 3B"; damage correlates with parameter count
  (rho=0.72) not tokenizer size (rho=0.12); "Q4_K_M remains lexically clean at >=1B";
  closing sentence "Validation must be per artifact." Read onto estate roles: the 7B
  short worker at Q4_K_M sits in the robust regime; the gemma:2b / gemma2:2b janitor
  scut sits at the paper's boundary (2.6B params per the box tag list) where sub-2B
  artifacts lost 20-67% of definition ability - any future Q2/Q3 drop for janitor scut
  is the dangerous cell, not the current Q4/Q5 pins.
- The paper's strongest design warning is against the global number: "not calibrated by
  WikiText-2 perplexity: across nine artifact-matched ladders, near-identical Q2
  penalties (44.7%/47.6%) separate an artifact keeping its definitions (3.6%) from one
  losing them (43.6%)." Perplexity-ranked ladders cannot choose per-role pins; only
  task-graded, per-artifact runs can - which is the day-6 ladder law (DIGEST.md:2)
  confirmed from a second independent group.
- VeriLoop positions tiers by role in their own recommendation: Q6_K "overall sweet
  spot", Q5_K_M "memory-quality sweet spot", IQ1_M "minimum-footprint sweet spot" -
  i.e. the ladder is a menu, and picking one rung globally is a category error. The
  estate's day-6 per-artifact bit-ladder subject (lens/burns.md:69-71) extends cleanly
  into a per-role default: scut stays Q4/Q5 (or higher), worker Q4_K_M pending the A/B,
  judgment-adjacent drafts at Q6_K per VeriLoop positioning, decision-rung models kept
  at Q8_0 per the day-6 0.7-point delta.

### RQ4. GPU-ladder price triggers: NOT FIRED, market moved the wrong way

Trigger (lens/laws.md:189-191): "24GB+ Blackwell under ~$1200 or used H100 under ~$4000
flips the quant-vs-card economics on the AMD box" (RIB_GPU_LADDER_20261001.md:14-23).

- RTX 5090 (32GB Blackwell): HN 49701038 (2026-09-14) carries the Tom's Hardware story
  "Nvidia's RTX 5090 ($9,500) vanishes from online retail in the US"; the RTX 5500 Pro
  thread (49702319, fetched) adds kristianp's note that the RTX Pro 5000 (72GB) "already
  starts at $9,209". WebSearch cross-check (second-hand, page not fetched - OWED):
  bestvaluegpu.com Oct 2026 reads $4,999 new / $3,822 used, Tom's tracker lowest $6,995,
  scalper listings $9,000-9,500. Every figure is 3-8x above the ~$1200 trigger.
- Supply-side tightening, not loosening: four dup stories (10-02..10-05) report
  MicroCenter now requires photo ID + a signed no-export pledge to buy an RTX 5090.
- Used H100: search summary (second-hand) reads ~$20K-26K late 2026 (CloudZero:
  new ~$31K, 8-GPU HGX $250-320K, used "meaningfully less"; A100 80GB used ~$12.5-14.5K
  per GPUPoet/GPUDojo pages surfaced). The sub-$4000 trigger is ~5x away. Page-level
  verification OWED (none of these listings fetched directly).
- The cheap end of the ladder is RENTAL, not purchase: Jarvislabs H100 SXM $2.69/hr and
  RunPod $2.89/$1.99/hr (Oct 2026 pricing pages via search summary), and on the Strata
  thread a11r rents an RTX Pro 6000-class box at "~$1/hr" spot for 4-bit serving. The rib
  trigger is a purchase trigger; rental was always available and is the existing tier
  ladder's remote-specialist rung. Verdict: quant-versus-card economics unchanged, the
  AMD box stays the quant play, no lane change is justified by price.

### RQ5. 2026-10 releases that sharpen or contradict the A/B design

- arXiv 2610.04403 (2026-10-03, abstract fetched in full) is the one in-window GGUF
  quantization paper the date-range probe returned, and it SHARPENS the design twice:
  (a) it generalizes the four-pinned-choices rule across artifacts ("Validation must be
  per artifact"); (b) it hands the A/B a cheap new rider channel - rare-word surface
  inclusion vs one-sentence definition, tiered multi-synonym matcher, blind-judge census
  - with the estate-relevant prior that Q4_K_M >=1B should be flat on it. Overlap note:
  day-6 already held this paper at sweep level (frontier_olm_2026-10-06/DIGEST.md:
  "arXiv 2610.04403's sub-2B silent-cliff finding - refetch confirmed its quote and
  mechanism, one estate extrapolation was struck, and the item stays sweep-level"); my
  delta is the full-abstract quantitative regime table above, never before carried in a
  register row. It stays sweep-level here too, per the day-6 fold's own disposition.
- Nothing in-window contradicts the four-pinned-choices design; the Strata thread
  (Winfred-zz's 89.1% vs 71.9% cross-model benchmark, seamossfet's "you need somewhere
  near 50x chinchilla to do QAT" for 1-2 bit targets, grutiro's imatrix explanation,
  walrus01's "Running Q8 on 256GB RAM daily; Q4 is noticeably worse. Would never let a
  Q2 near a codebase he cares about") all point the same direction: verdicts are
  task x prompt x engine x artifact conditioned. seamossfet's QAT-for-deep-quant claim
  is thread-comment tier (unverified), worth a paper hunt OWED.
- Door capability: the submittedDate-range shape works on export.arxiv.org (one probe,
  1 hit, no hang) - extends lens/doors.md:39 which only cleared the bare minimal shape.

## Banked items (fetched and read this sitting; overlap greps run against
catalog/catalog.jsonl and memory/ via ripgrep; held-ground greps extended to
watch/inbox/frontier_olm_2026-10-0{1,4,6,7})

1. Strata HN thread (930 pts / 422 comments) - https://news.ycombinator.com/item?id=49953495
   Quote (OP snehesht): "I tried it and it worked surprisingly well."
   Overlap: the engine is already percolator candidate 5a938176e21c3b4b (memory/percolator/
   candidates.jsonl, from LINKS.jsonl L397 operator drop, verdict TEST not ADOPT, "all
   benchmarks author-claimed", falsifier "Strata vs llama.cpp --n-cpu-moe same-box
   benchmark"; distinctive token Niko1221 => catalog 0). DELTA banked here: independent
   task-graded thread evidence - identical-weights vision delta 154.8 px vs 46.5 px across
   engines (Jackson__, amitp85 concurring), 89.1% vs 71.9% cross-model task benchmark
   (Winfred-zz), QAT-at-pretraining argument (seamossfet), imatrix explainer (gruturo),
   Q8-vs-Q4 daily-driver verdicts (walrus01). Speed claims were already verified in-band
   by the 10-05 candidate row; do not re-verify.
2. Strata repository - https://github.com/Niko1221/Strata
   Quote: "reaches 91% of the full model's SWE-bench Verified score" (Coder variant, per
   its authors).
   Overlap: same candidate row as item 1; repo claims (expert cache + SSD lookup table +
   speculative decode 1.6-1.8x) byte-match the 10-05 row's summary. This sitting adds the
   per-quant speed table (RTX 5070 12GB: Q2_0 94 tok/s out / 2650 tok/s prompt; IQ3_S 53/
   1620; RX 9070 XT: Q2_0 60/1160) and the artifacts list (ISTA-DASLab, UkisAI, Unsloth
   compressions) - the estate falsifier row can now name exact quant rungs to benchmark.
3. Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write
   Rare Words They Can No Longer Define - https://arxiv.org/abs/2610.04403
   Quote: "Validation must be per artifact."
   Overlap: catalog 0, memory 0 for the arXiv id, but day-6 DIGEST holds the paper at
   sweep level (quote + mechanism confirmed there, one extrapolation struck, sweep-level
   disposition). DELTA: full-abstract regime numbers now in-repo: sub-2B definition loss
   20-67%; Q4_K_M lexically clean >=1B; parameter count rho=0.72 vs tokenizer rho=0.12;
   PPL non-calibration 44.7%/47.6% vs 3.6%/43.6% definition outcomes. Stays sweep-level.
4. Janus: Go binary running GGUF via Vulkan - https://github.com/Vibra-Ingenn/Janus
   Quote: "Janus is a single Go binary that runs .gguf models on your machine (GPU or
   CPU) and exposes an OpenAI-compatible API."
   Overlap: day-7 sweep pass-1 candidate, explicitly OWED-not-read there
   (frontier_olm_2026-10-07/sweep/quantization-compression-hn.md:188-189); "Vibra-Ingenn"
   => catalog 0, memory 0. Discharges the owed read: it wraps llama.cpp with FFI bindings
   "pinned to llama.cpp b11146 on Linux", Vulkan default across AMD/Intel/NVIDIA, but is
   8-commits/129-stars early - watch-list for the estate's Vulkan serving, not a switch.
5. RTX 5500 Pro Blackwell 84GB HN item - https://news.ycombinator.com/item?id=49702319
   Quote (story title as shown): "Nvidia Launches RTX 5500 Pro Blackwell Desktop Edition
   with 84GB GDDR7 RAM".
   Overlap: "RTX 5500" => catalog 0, memory 0 (day-6 door files carry "RTX Pro 5000" only
   as search-result noise). The RQ4 datum: RTX Pro 5000 72GB already starts at $9,209
   (kristianp, comment tier), 5090 vanished from US retail at up to $9,500 - the ~$1200
   24GB-Blackwell trigger (lens/laws.md:189-191) is not approached; no trigger fired.

## Held/corroborated this sitting (no re-banking)

Mozilla server benchmark (day-1 deep-read: open-local-language-models-x.md item 10 +
inference-efficiency-reddit.md Q5; raw page harvested day-4 as
ihn_page_49742415_mozilla_bench.txt) - re-verified from the live page today, all numbers
match (63.3% shader toolchain, +16.8% CUDA graphs, draft flips, 0.4/1.8/5.4 ms host
overhead). VeriLoop E2 ladder (day-6 register row 15 + catalog d69fb4b623a4) - full
8-tier table re-read today, consistent. Quesma ladder, bartowski maps, GSQ-RCO, Swift,
AMD Quark, decision models: all day-7 banked, untouched here.

## OWED / not done (never asserted as done)

- THE A/B: still un-run. Arm A on box (digest verified this sitting), arm B needs the
  8.1 GB pull; ~100+ runs; firing belongs to the burns-ledger queue per spec lines 4-5.
- RQ4 page-level price verification: bestvaluegpu/CloudZero numbers are search-summary
  tier; no marketplace listing fetched directly.
- seamossfet's "~50x chinchilla for QAT" claim: thread-comment tier, paper hunt owed.
- Gufo Qwen3.6-35B-A3B-Q6dense (49941824), Bonsai-2 ByteShape comparison (50002054),
  gpufind rent-vs-buy (49829063), computeassay (49792523), Kairo (49691112): candidate
  level only, not read this sweep.
- The LRU-vs-KV-papers thread (49643543) stays unread, carried from day-7.
