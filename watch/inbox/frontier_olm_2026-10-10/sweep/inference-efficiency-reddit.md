# Frontier sweep: inference-efficiency via reddit - 2026-10-10

source-fetched: 2026-10-10
Seat: sweep-inference-efficiency-reddit (frontier_olm_2026-10-10 push)
Feeds: RIB_INFERENCE_BUDGET, RIB_STANDING_WAVE_BUDGET, memory/runs/hermes_burn/usage.jsonl + 247 driver log, smith DISK ETA, driving-ladder local rung.

## Doors and degradation (recorded honestly)

- `https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` (recipe door): DEGRADED - "Log in to use old Reddit" wall, no JSON. Same for old.reddit.com HTML.
- `https://www.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50`: DEGRADED - "You've been blocked by network security" (WebFetch + Z.ai webReader) and HTTP 403 via curl with custom UA. `top.rss`: HTTP 429.
- Recipe fallback `WebSearch site:reddit.com`: WEAK - the search backend largely ignores the site:/domain filter and returns general web results; only occasional reddit wiki hits.
- WORKING DOOR USED: redlib mirror `safereddit.com` (thread HTML renders fully, listing + search endpoints). One sibling instance (redlib.catsarch.com) 429'd; safereddit held for all 10+ fetches. All quotes below are from pages fetched through this mirror; canonical reddit permalinks given alongside.

## Method

- Pass 1 (broad): r/LocalLLaMA top/month (pages 1-2, 25 posts each), r/LocalLLaMA search "vllm" top/month (25), r/LocalLLaMA search "thinking tokens speed" top/month (25), r/ollama top/month (25), r/LocalLLM top/month (25), r/MachineLearning top/month (25). After dedup, 75+ unique candidates in the last ~30 days considered; ~30 carried inference-efficiency payload.
- Pass 2 (deep): 9 threads fetched and read end to end (post + substantive comments): 1wfdtm7, 1wg7dd5, 1whx5xi, 1wiws8e, 1x0wnz1, 1wy7wn0, 1wxgm0h, 1wz00vv, plus 1wyaxyd (read, then NOT banked as an item because already held, see overlap).
- Overlap: grepped `catalog/catalog.jsonl` (1,127,563 rows) for exact thread IDs and distinctive phrases, and grepped `memory/` recursively. Catalog thread-ID verdicts: 1x0wnz1:0, 1wfdtm7:0, 1wiws8e:0, 1whx5xi:0, 1wy7wn0:0, 1wxgm0h:0, 1wvxih5:0, 1wtc4j9:0 - all genuinely new. Already held: 1wyaxyd (raw JSON banked 2026-10-07, catalog row 1013545), 1wg7dd5 base + 1wp6gal (sibling raw swift_qwen3827b.txt row 1013972 today; gapwave note memory/runs/gapwave/hn_x_fanout/local_serving.md:34-38 from 09-20), 1wh5elt ThinkingCap (2 rows), 1wgzpli SHADOW-50M (1 row), 1wj6c4l Ternary Bonsai 2 (swept 10-09, row 1013898).

## Banked items (strongest first)

### 1. RTX 3090 24GB runs Qwen3.8-27B INT4 with 144K FP8 KV via vLLM - the estate's exact hardware class
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1wfdtm7/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1wfdtm7/ | ~2026-09-14 (26d ago)
- Quote: "It fits on one GPU with a configured context window of 147,456 tokens."
- Numbers: RTX 3090 245W, WSL2, 48GB DDR4; vLLM 0.27.1 + club-3090 patches, INT4 AutoRound weights, `--kv-cache-dtype fp8_e4m3`, `--max-num-seqs 1`, chunked prefill + prefix caching. Prefill avg 871.93 tok/s (1000 @10K down to 744 @90K); decode avg 38.39 tok/s (42.3 @10K down to 34 @90K); 71/75 BenchLocal at reasoning_effort=low.
- Why it matters (Q1+Q3): the only deep-read thread where the vLLM-class stack runs on a single consumer 24GB card a Windows host can own. Key mechanism comment (u/Gauntlet4933): llama.cpp Q8 KV only dequantizes to BF16, while "FP8 uses hardware acceleration to do compute in FP8 as well" - that is the concrete lever an ollama/llama.cpp fleet lacks. Windows reality check: a Windows-only commenter got only parity with his custom llama.cpp build in Docker; OP notes WSL2 costs speed vs bare metal. Failure modes: JIT-compile OOMs (retry heals), 5-6GB compile caches, single-request only. Quality counter-evidence: FP8 KV "significantly degrades Qwen 3.8's CoT" over long thinking (u/EuphoricPenguin22).

### 2. Swift-Qwen3.8-27B community dispute - the regrade evidence for laws lens open q10
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1wg7dd5/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1wg7dd5/ | ~2026-09-14 (26d ago)
- Quote (u/GoblinEngineer's rigorous paired test, 2400 graded answers): "it guesses where the base model says it does not know."
- The dispute numbers: hallucination 44.3% to 48.0%, abstention 35.1% to 30.5%; paired 106 "base abstained, Swift answered wrongly" vs 55 reverse; McNemar z=4.02, p<0.0001. Author's claim: "-58% thinking tokens, 1.95x speed up, <1% accuracy loss" (GPQA-D 88.4% to 88.3% at 6,642 to 2,771 median tokens). Independent support also present (vick2djax 20/20 vs 13/20 on a five-stage coding task).
- Why it matters (Q2): the estate's 09-20 note holds Swift's accuracy claim unchallenged; this thread supplies the missing adversarial measurement. Verdict for q10: REGRADE, do not confirm. Thinking-token reduction buys wall-clock at the price of calibration (silent guessing where the base would abstain). Any estate re-measure must score the abstention/hallucination split, not just accuracy. Methodology warnings that map onto our instruments-only law: 5 seeds per arm needed (single-run benchmarks disagree); saturated benches (>90%) hide regressions; Swift's embedded MTP draft head measured slower than a stock external draft.
- Overlap: base model known (gapwave local_serving.md:34-38; sibling raw capture today row 1013972). Banked here ONLY for the dispute evidence, which no holding contains.

### 3. KV cache offloaded to RAM at 48 MiB/token - tokens-as-disk gets a bytes-per-token law
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1whx5xi/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1whx5xi/ | ~2026-09-16 (24d ago)
- Quote: "I now get 1M context with 3x 3090. I get ~80 tok/s at short context, dropping to ~60 tok/s once QSA reaches its 2048-token budget"
- The math that matters (Q4): Qwen3.8-Flash-Next keeps KV in only 12 of 48 layers (36 gated-delta-net layers have fixed state); per-step read = 2048 positions x 2 heads x 256 dim x 2 (K,V) x 2B = 4 MiB/layer x 12 = 48 MiB per generated token across PCIe, i.e. ~3.9 GB/s at 80 tok/s, a fraction of PCIe 4.0 x16 (~32 GiB/s). VRAM needs shrink to weights + ~66 B/token/layer. Ceiling: ~1,200 tok/s on PCIe 5.0 x16; pinned host memory mandatory; prefix caching disabled hurts agentic loads. Reproduction: dual 3080s + 128GB DDR4 hit 262k ctx at ~40 t/s gen, 900 t/s prefill.
- Why it matters: converts "KV cache growth" from folklore into a byte-arithmetic budget row, exactly the form the standing-wave GB/day ledger (tokens are disk, law 16) can absorb IF a new row class (PCIe-bytes-per-token + VRAM floor) is added. Answer to Q4's first half: yes, with a new class, not by stretching the old one.

### 4. 153 tok/s NVFP4 on one R9700 - the instruments-only law's case study in reproducibility
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1wiws8e/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1wiws8e/ | ~2026-09-17 (23d ago)
- Quote (u/mr_tolkien): "I reproduced the headline speeds on a single R9700, but found reliability issues with agent workloads"
- Setup: Unsloth Qwen3.8-27B NVFP4 (23.4GB) on author's custom vLLM fork (vllm-radiance / vllm-mxfp4), Linux + Docker; RDNA4 has no native FP4 matmul, so the fork converts NVFP4 to MXFP4 at load. Decode medians by category (json 153.1, reasoning 123.9, prose 69.2); prefill 3,192-3,619 t/s from 2k to 64k ctx; concurrency 1 gives 120, 8 gives 471 t/s total.
- Why it matters (Q3): the headline does NOT survive a near-miss setup. Other users got 13-17 t/s on stock stacks; one skeptic holds "I don't think 150tps concurrency 1 is legit for 27B" (spec-decode/MTP acceptance inflates it). The reproducer also caught corrupted outputs: a 49-request agent test had 4 timeouts + 6 corrupted responses until prefix caching was disabled. Bandwidth comment worth a rib note (u/werunm): 153 to 470 t/s at 8 concurrent "is a good demonstration of memory-bandwidth-bound decode". Instruments-law verdict: bank per-category medians + engine version + spec-decode state or bank nothing; single-number claims are not reproducible.
- Overlap: NVFP4 as a format is held (catalog rows 55964, 55976, 998414/1012796 Gated-DeltaNet W4A4, 1003037 OSFP4); this thread (0 hits) adds consumer-AMD reproducibility evidence, new.

### 5. $2800 8x Radeon Pro V620 + custom vLLM fork - the direct successor to HN 50032575's class
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1x0wnz1/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1x0wnz1/ | 2026-10-09 (1d ago)
- Quote: "Routed experts are W4A16 and everything else remains at BF16. MTP enabled with 3 token drafting."
- Numbers: Qwen3.8-Flash-Next 60-100 t/s decode (40-50 without MTP), 3000+ t/s prefill; PP=4 over PCIe 3.0 x4 bifurcation, no TP (allreduce too slow); RDNA2 custom kernels (~800% prefill over llama.cpp's 350-450); cards power-capped 180W (~400W total draw under pipeline parallel); ~$3000 all-in, though V620s now fetch $650 each.
- Why it matters (Q1): names the actual vLLM-class advance list: mixed W4A16 experts, MTP spec drafting, pipeline parallel, power capping, custom kernels. Verdict for the estate: NONE of this ports to a Windows ollama janitor directly (Linux/ROCm, dual-socket bifurcation, 8 cards); the transferable subset is exactly items 1 and 3's levers (FP8-KV compute, spec decoding, mixed quant). Aggregate-throughput skepticism (PP=4 at concurrency 1 times one card) is the standing caveat class for all such posts.

### 6. Agens Volundr 32B - 18 of 72 layers keep a KV cache; prefix caching is the tax
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1wy7wn0/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1wy7wn0/ | ~2026-10-05 (5d ago)
- Quote: "54 KDA (Kimi Delta Attention) layers: linear attention with a fixed-size recurrent state, no KV cache"
- Numbers: 32B dense, 262K ctx, Apache-2.0; INT4 31.7 GiB on one 48GB card; decode 31.0 t/s @1K down to 29.1 @32K (INT4); 127-130 t/s aggregate at 8-16 users; DFlash2 drafter up to 3.6x on JSON. Beats Qwen3.8-27B on LiveCodeBench v6 (+4.2), loses agents (tau2 74.2 vs 79-80; SWE-bench 44 vs 58-64).
- Why it matters (Q4): the hybrid-arch efficiency class the estate's Gated-DeltaNet NVFP4 holdings point at, with the failure mode named by the team itself: recurrent-state snapshots defeat prefix caching and "the blocker is Engram rather than KDA" (each turn re-prefills, ~15s for 30K tokens). Independent run: beat Qwen on coding but "Qwen took 1h 7m but yours took 5h 9m". Comment verdict "It's DOA until this is fixed" (u/__JockY__). For a janitor fleet doing many short sessions, no-prefix-caching is disqualifying today; watch v1.

### 7. 1x3090 to 20 DGX Sparks - serving scale-out terminates in the power budget, not tokens
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1wxgm0h/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1wxgm0h/ | ~2026-10-04 (6d ago)
- Quote (u/IntercontinentalToea): "You can borrow money to buy equipment. You can't borrow a thicker cable and larger breakers"
- Story: fuses blew when the rig and the electric oven ran together; now 16 GB10 + 4 Sparks on 100Gbit Mikrotik; Kimi K3 2.8T "from an unusable 7 t/s at 100k context to a fairly usable 20 t/s at 300k"; FP8 swap for INT4 bought 20%; "397B at 30 t/s on 400W, versus 50-60 t/s at 6kW" (GB10 vs 16x3090). ~$120-125k all-in; ~$200/month energy; 240W per Spark.
- Why it matters (Q4): the extreme case answers whether serving forces a new budget class. At scale the binding constraint becomes amps/breakers/cooling, a class the GB/day ledger cannot express. The watts-per-token frontier line (30 t/s @400W) is the number a sovereignty estate should quote when weighing local serving growth. Also the skeptic's law: "Running locally is NEVER going to be cheaper if you compare like for like" (u/Cergorach).

### 8. Microsoft page: GPT-6.1 uses looped transformers - 2 inference passes
- Mirror fetched: https://safereddit.com/r/LocalLLaMA/comments/1wz00vv/ | canonical: https://www.reddit.com/r/LocalLLaMA/comments/1wz00vv/ | ~2026-10-06 (4d ago)
- Quote: "GPT-6.1 Sol uses 2 inference passes, with a passing mention of 'instead of three'"
- Horizon item: looping trades compute-per-parameter ("Small rock do big rock job"); the bandwidth-savings claim is disputed (u/greying_panda: "I don't see how your transformer block becomes one large fused operation that can be repeated cheaply"); safety angle: latent non-token reasoning reduces inspectability of thinking, which matters to a fleet whose thinking-on/off economics assumes visible reasoning tokens. Links in-thread: arxiv 2510.25741, 2502.05171, Huginn-0125 (HF).
- Overlap: looped-transformer arxiv state held (catalog rows 999466, 999585, 1001125, 1001280); the confirmation news angle is new.

## Read but NOT banked (already held)

- r/ollama "No think doesn't work" (1wyaxyd): raw JSON banked by the 10-07 arctic sweep (catalog row 1013545). Root cause my read adds for the fold: qwen3:4b now shares its digest with qwen3:4b-thinking (2507 thinking-only), so no flag can disable thinking; you must pull qwen3:4b-instruct-2507-q4_K_M explicitly. And "--hidethinking only hides the reasoning; it won't save your laptop the work of generating it" (u/ChaseMakesThings). Both lines feed the off-switch-must-be-explicit law and suggest a digest-trap check for the janitor fleet's gemma tags.
- Ternary Bonsai 2 (1wj6c4l): swept 2026-10-09 (row 1013898) + gapwave splash_bonsai. ThinkingCap (1wh5elt, 2 rows), SHADOW-50M (1wgzpli, 1 row), Swift series post 2 (1wp6gal, 2 rows): held.

## Answers to the four research questions (evidence-cited above)

1. Do single-host vLLM-class advances apply to a Windows ollama janitor fleet? Directly: no. Every deep-read vLLM success ran Linux (often Docker/ROCm, custom forks); the one Windows-adjacent success paid a WSL2 speed tax, and a Windows-only commenter got parity with a custom llama.cpp build. Indirectly yes, via three levers the fleet can adopt without vLLM: FP8-KV-style hardware-FP8 compute (llama.cpp Q8-KV dequant-to-BF16 does not get this), speculative decoding/MTP drafting (1.5-2x class, needs acceptance-rate logging), and mixed W4A16-experts quant choice. Consistent with the estate's held Mozilla benchmark (engine choice within noise; build/config is the win, memory/runs/gapwave/hn_x_fanout/local_serving.md:22-26). The quant A/B tie at ceiling stays banked and instrument-scoped; not re-run.
2. Thinking on/off economics (laws lens open q10): regrade or confirm? REGRADE. Outside evidence (item 2) shows token-reduction at claimed accuracy parity silently trades abstention for guessing (McNemar-significant). The suspect rows should be re-scored on an abstention/hallucination split before any economics conclusion; and per 1wyaxyd, verify the served digest actually has a non-thinking mode at all, since hidden thinking still burns the tokens. EMPTY_REASONING burns stay terminal per law 8; no refire.
3. Which throughput claims survive the instruments-only law? None of the single-number headlines survive contact with a near-miss setup (153 vs 13-17 t/s on the same card). What survives: per-category decode medians with engine version + spec-decode state + context-depth split (item 1's 871.93/38.39 tok/s with 10K/90K splits is the format to steal), plus reproduction threads with failure counts (6 corrupted of 49 requests).
4. Can standing-wave GB/day accounting absorb a serving stack? Yes only with new row classes; no by stretching. The byte-arithmetic exists (48 MiB/token PCIe traffic; VRAM floor = weights + ~66 B/token/layer, item 3), and the terminal constraint at scale is power/wiring (item 7), a class the ledger does not have. Minimum new classes: VRAM-bytes and PCIe/RAM-bytes per token, and watts per tok/s.

## Honest limits

- All fetches went through the safereddit.com redlib mirror; quotes are verbatim from mirror-rendered pages. Mirror tampering risk is nonzero; confidence per item reflects that (0.85-0.9).
- Dates are "Nd ago" reconstructions from the listing moment (2026-10-10), approximate to +/-1 day.
- The estate's own tok/s baseline numbers were not re-measured in this sweep (out of scope for a mining seat; instruments law).
