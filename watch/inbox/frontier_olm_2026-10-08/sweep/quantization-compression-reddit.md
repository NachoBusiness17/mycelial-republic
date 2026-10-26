# Sweep: quantization-compression via Reddit (frontier_olm 2026-10-08)

source-fetched: 2026-10-08

Seat: sweep-quantization-compression-reddit. Area: quantization/compression on the Reddit door,
feeding the owed qwen2.5:7b Q4_K_M vs q8_0 A/B queue
(`watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md`), the model-garden quant cells, and the
GPU-ladder rib. The A/B itself was NOT run by this seat and stays owed
(`watch/inbox/frontier_olm_2026-10-08/lens/burns.md:205-208`, verified this sitting: "the A/B
itself has no run receipt I found. Owed."). This sweep feeds its instrument.

## Doors: what worked, what degraded

- `https://old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` (recipe door): 302, empty body
  (curl `-w` probe: `HTTP=302 SIZE=0`). DEGRADED.
- `https://www.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50`: 403, 189,908-byte block page.
  DEGRADED.
- Thread HTML on old.reddit: 302 to `old.reddit.com/login/?reason=lor2` (login wall). WebFetch on
  the same URLs returns only the "Welcome to Reddit" shell. DEGRADED.
- `r.jina.ai` text proxy: Reddit returns 403 through it ("You've been blocked by network
  security"). DEGRADED. Not retried with evasion tricks on purpose.
- Redlib mirrors: redlib.catsarch.com dead (000); safereddit.com serves an Anubis JS
  proof-of-work challenge. Not solved by design (that is an anti-scraping measure, and beating
  it is not research). DEGRADED.
- web.archive.org CDX: "Internet Archive: Temporarily Offline". DEGRADED.
- WebSearch `site:reddit.com` (recipe's named fallback): WORKING. Used for discovery + snippets.
- WORKING FULL-TEXT DOOR found by probe: Reddit's RSS surfaces. `/r/<sub>/top/.rss?t=month`
  (dated entries), `/r/<sub>/search/.rss?q=...&restrict_sr=1&sort=new&t=month&limit=100` (dated,
  in-window), and per-thread `/comments/<id>/.rss` (OP body + up to ~150 comments, full text,
  with `<published>` dates), fetched via `curl -A "research-sweep/1.0"` with 35-40 s spacing
  (Reddit rate-limits bursts: 14-of-16 rapid fetches returned LEN 0; spaced retries succeeded).
- r/LocalLLM and r/ollama `/top/.rss?t=month`: 200 but 0 entries. DEGRADED for those two subs;
  their coverage came through site-restricted WebSearch instead.

## Pass 1: broad sweep (30+ candidates, all dated in the last 30 days)

Discovery corpus: `/r/LocalLLaMA/search/.rss?q=quantization&restrict_sr=1&sort=new&t=month&limit=100`
returned exactly 100 dated entries (2026-09-16 through 2026-10-08), plus `/top/.rss?t=month`
(25 entries) and site-restricted WebSearch. Candidates considered (date | title):

1. 2026-10-08 | $2800 rig with 8x Radeon Pro V620 (256 GB VRAM) + custom vLLM fork (1x0wnz1)
2. 2026-10-08 | [2506.13771] LittleBit: Ultra Low-Bit Quantization via Latent Factorization (1x0sa6g)
3. 2026-10-08 | Comparing Qwen3.8-27B fine-tunes and baselining vs. frontier (1x0gaqv)
4. 2026-10-07 | 2x CMP 170HX 64GB: GLM-5.3-Flash at 384K context / ~90 tok/s (EXL3) (1x0b1ws)
5. 2026-10-07 | My progress on a [new] model-architecture specific dynamic quant technique - v1 (1x083w0)
6. 2026-10-07 | Can I run Swift 1.5 flash next iq3xxs in 16GB VRAM and 32GB RAM? (1wzjm5d)
7. 2026-10-06 | Qwen3.8-27B with just 12GB VRAM + 8GB RAM - ~18 tok/sec (1wzha67)
8. 2026-10-06 | Optimizations Claude did for Qwen 3.8 27B and Qwen Flash Next on dual and quad 7900xtx (1wzh32j)
9. 2026-10-06 | Qwen3.8-27B (Q6_K_XL) 110+ TPS at 256k context on a single RTX 5090, KV buffer decoupled (1wzg75e)
10. 2026-10-06 | If you benchmark llama.cpp on AMD with the official ROCm builds, check that you're actually on the GPU (1wzdti3)
11. 2026-10-06 | I made an "Opus 5.5 style" code-rendered video - but on a local NVFP4 Qwen 3.8 27B (1wzdhwf)
12. 2026-10-06 | What models do you want to see new dynamic quants for? I'll make them. (1wz-paged)
13. 2026-10-06 | I quantized GLM-5.3-UNCENSORED to MXFP4 for AMD GPUs (1wz-row)
14. 2026-10-06 | Qwen3.8: 27b vs flash next. We all know the benchmarks... (1wz-row)
15. 2026-10-06 | [Benchmark] Running Local LLMs on Orange Pi 5 Plus (RK3588, 16GB) (1wz-row)
16. 2026-10-06 | DeepSeek V4.1 Flash on a single DGX Spark: 113.6 GB VQ base + 40 MB domain sidecars (1wz-row)
17. 2026-10-05 | Gigabyte AORUS RTX 5090 AI BOX (1wy-row)
18. 2026-10-05 | k_llama.cpp MoE Optimizations: Expert Residency, Hybrid CPU/GPU Execution, Q2_0 Support (1wy-row)
19. 2026-10-05 | We swapped AdamW's optimizer states for a Fast Fourier Transform (FFT) to cut VRAM in half (1wy-row)
20. 2026-10-05 | Spent Rs30,000 on an RTX 5060 ... Reality hit so hard (1wy-row)
21. 2026-10-05 | I squeezed Kolibri-1 78B-A3.5B to 20.9 GiB / 2.30 bpw - 59% lower KL than standard IQ2_XS (1wyeanf)
22. 2026-10-05 | 4-bit Qwen2.5 that stays closer to fp16 than the official AWQ, on the same vLLM kernel (1wyc2b0)
23. 2026-10-05 | Infermeld: a Linux kit for running one GGUF across AMD + NVIDIA GPUs with llama.cpp (1wy-row)
24. 2026-10-03 | Running Qwen3.8 Flash Next 176B on a 16GB RTX 3080 Laptop + 32GB RAM + SSD (1wx-row)
25. 2026-10-03 | I built Ninfer 4080 for 16GB class GPUs (1wx-row)
26. 2026-10-02 | 200 Task Custom Dataset Performance Result: 10 Popular Models, from 2B MoE to 27B Dense (1wv-row)
27. 2026-10-02 | Heavily quantized Qwen3.8-Flash vs Q8 Qwen3.8-27B - thoughts? (1wvzmt3)
28. 2026-10-02 | Qwen3.8-Flash-Next (5.05bpw + ngram at bf16) exl3 on one r9700: 863 t/s prefill (1wv-row)
29. 2026-10-01 | Running 95.5 GiB Qwen3.8-Flash-Next at 41-52 tok/s on a 64GB Mac (1wu-row)
30. 2026-09-30 | Two open-weights releases: Victoria (Qwen3.8-Flash-Next with 44% of experts cut) (1wu-row)
31. 2026-09-30 | [Release & Deep Dive] ATX-Swift-1.5-Qwen3.8-27B-Uncensored-MTP (i1-Q5_K_M) (1wu-row)
32. 2026-09-29 | Local Q2_K model dunked on DeepSeek V4-Flash during my mini test (1wt-row)
33. 2026-09-29 | 50B+ MoEs with few active parameters, what's the sweet spot (1wt-row)
34. 2026-09-29 | [Release] GSQ-RCO GGUFs for Qwen3.8-Flash-Next, plus a 50% expert-pruned Coder build at ~1.89 bpw (1wt4s88)
35. 2026-09-25 | Qwen3.8-27B: Using KV Cache Transplants to Boost Output Quality (1wq76f6)
36. 2026-09-23 | Dynamic Quantiser - a way to make your own high quality dynamic quants (1wq-row)
37. 2026-09-20 | Postulate: Context compaction is good for Quantized models (1wlss89)
38. 2026-09-20 | Please stop with the FP4 inference engines for the love of god (1wl56g2)
39. 2026-09-16 | What benchmarks do you run locally? (1wi2en4)

Plus from `/top/.rss?t=month` and WebSearch: "I trained a 44M parameter quantized LLM from
scratch on 45B tokens. It ships in 19.8 MB" (r/ML, 2026-09-15, 1wgzpli), "Don't buy a $9K RTX
5090.... instead." (2026-09-15, 1whf7ov), MoQ GGUFs and GSQ (1tyjkfh, discovered via WebSearch,
thread predates the window - not dated in-window, not banked), "Qwen 3.6 27B BF16 vs Q4_K_M vs
Q8_0 GGUF evaluation" (1sxzqry, `<published>` 2026-04-28 - OUTSIDE the window, excluded from
candidacy; search matched content, not recency).

Out-of-window candidates considered and dropped by rule: 1sxzqry (2026-04-28), 1w05kbt "5090 now
officially cost [sic] $5,000" (`<published>` 2026-08-27), the older KLD/Q8-vs-Q4 classics the
WebSearch fallback surfaced (1o5mr9j, 1n3ezr4, 1rlgbac, 1rk5qmr, 1sl59qq, 1uy635o, 1vz3ieu,
1vr643w, 1vt80nk et al., all 1o*-1v* IDs, pre-September).

## Pass 2: deep reads (9 threads read end to end this sitting)

Each fetched via `curl -A "research-sweep/1.0" https://www.reddit.com/r/LocalLLaMA/comments/<id>/.rss`
with backoff; raw RSS saved to local temp `reads/` (session cache, not durable); OP body and
comments parsed and read. 1sxzqry also fully read (150 entries) before its April date excluded it.

1. 1wyc2b0 (2026-10-05) qwen25awq - full table read: Qwen2.5-7B-Instruct fp16 7.15 ppl / 70.1%
   HumanEval vs custom 4-bit 7.29 / 67.1% vs official Qwen AWQ 4-bit 7.58 / 64.6% (A10G, vLLM
   0.29, awq_marlin kernel). OP's own "What this does not show": one run per row; HumanEval
   4-bit differences within ~3.6-point noise; WikiText-2-train calibration flatters the ppl
   channel (~0.3 on 1.5B); lead shrinks with scale; at 3 bits ppl holds but half of code/math
   ability is lost.
2. 1wzdti3 (2026-10-06) rocm - on four AMD hosts the official ROCm prebuilt (b11327) never
   touched the GPU: HIP backend wants libamdhip64.so.7/libhipblas.so.3/librocblas.so.5, stock
   ROCm 6.3.0 ships .so.6/.so.2/.so.4; llama-server silently serves from CPU, /health green,
   even `-ngl 999` changes nothing; ggml-org/llama.cpp#26964. Top comment: the reverse case,
   400 tok/s desktop vs 30 tok/s laptop, cause was accidentally using the Vulkan build.
3. 1wyeanf (2026-10-05) kolibri - IQ2_XS-family custom quant of Kolibri-1 78B-A3.5B MoE at
   2.30 bpw / 20.94 GiB, ~59% lower KL than standard IQ2_XS, 90.5% top-token agreement vs 84.6%;
   method: tensor/layer sensitivity spending bits where they matter most.
4. 1wvzmt3 (2026-10-02) flash_vs_q8 - 84-entry thread read. Top answer: "Flash next at 4 bits
   medium beats 27b at 8 bits xhigh"; second: IQ3 Flash next vs Q6 27B, "27B was about 3x
   faster tok/s, flash next gave me more utility"; VRAM note: ~120B regular weights at 4 bits
   ~60GB + 51B expert weights SSD-offloaded on 4x3090.
5. 1wt4s88 (2026-09-29) gsqrco - GSQ+RCO GGUF release for Qwen3.8-Flash-Next (512 experts x 48
   layers, 176.9B params, 354 GB BF16) plus 50% expert-pruned Coder at ~1.89 bpw. Failure
   report from a Delphi/C++/asm coder; maintainer concedes capabilities underrepresented in
   calibration data can be lost.
6. 1x0sa6g (2026-10-08) littlebit - arXiv 2506.13771 (v5 2026-02-05, NeurIPS 2025) plus
   LittleBit-2 follow-up (arXiv 2603.00042, v2 2026-05-03) surfaced in comments; code
   SamsungLabs/LittleBit. Abstract fetched directly from arXiv (quote banked below).
7. 1wlss89 (2026-09-20) compaction - postulate that quant error accumulates with context and
   128k-with-compaction beats raw 256k/1M at ~Q4; chart is illustration-only by OP's own
   admission; top comment correctly notes plain long-context degradation confound. Read and
   NOT banked as an item: evidence class too weak, but it sharpens the A/B's context-length pin.
8. 1x0wnz1 (2026-10-08) v620 - 8x Radeon Pro V620 (RDNA2, 32 GB each, 256 GB total) for ~$2800
   running Qwen3.8-Flash-Next at 60-100 t/s decode, 3000+ t/s prefill via custom vLLM fork; OP
   corrects the $350/card figure upward in-thread. Comments debate GLM-5.3-Flash vs Qwen-Flash
   at quant headroom ("full quant qwen flash or a Q4 or maybe Q6 if u can fit glm flash").
9. 1w05kbt (2026-08-27, out of window, read for Q4 price context only) 5090price - RTX 5090 at
   ~$5,000; comments price a fair 5090 at $850-1200 and note ASUS GX10 128GB workstation + 5070
   Ti costs the same as one 5090.

## Overlap check (run this sitting)

Scoped grep of `catalog/` + `memory/` for each thread ID and a distinctive phrase of every
banked item (18 probes incl. "1wyc2b0", "1wyeanf", "1wvzmt3", "1wt4s88", "1x0sa6g", "1wzdti3",
"1x0wnz1", "2604.18556", "2506.13771", "stays closer to fp16", "2.30 bpw", "gsq-rco",
"heavily quantized qwen3.8-flash vs q8", "context compaction is good for quantized",
"radeon pro v620"): ZERO hits in `catalog/catalog.jsonl` or any catalog file. `memory/` hits are
exclusively (a) this session's own trajectory log (`memory/trajectory/steps.jsonl`, which
records this seat's own tool calls - self-referential, not prior holdings) and (b) the estate's
own A/B vocabulary in `memory/runs/ds_batches/*.jsonl` (the owed probe's own name). `kolibri`
also string-matches an unrelated nvidia llama probe row in
`memory/runs/free_lane_fleet/ledger.jsonl:275` - not Kolibri-1. Conclusion: every banked item is
genuinely new to the estate. First search-of-record also confirms the day-7 mine
(`watch/inbox/frontier_olm_2026-10-07/steal/quantization-compression.md`) banked arXiv sources,
not these Reddit threads.

## Answers the sweep feeds (scoping stated)

- Q1 (run the amended A/B): NOT run here - sweep seat, no burns-lane firing authority; the spec
  remains amended-only and owed (`watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md:3-5`,
  `frontier_olm_2026-10-08/lens/burns.md:205-208`). What Reddit adds to the instrument: a
  backend/device verification leg (item 2: a green /health on an AMD box can be a CPU silently
  serving), a noise floor datum (item 1: ~3.6 HumanEval points single-run), and a second
  diagnostic channel next to strict-parse (top-token agreement, item 3).
- Q2 (load-bearing pins): the paper's four choices stay pinned per the spec; Reddit evidence
  nominates two contract extensions - pin the serving backend + device actually used (rocm
  thread), and pin the calibration-mix coverage when any arm is a dynamic/pruned quant (gsqrco
  thread's Delphi failure + maintainer admission). One-run-per-row with ±3.6-pt task noise
  (qwen25awq) is the measured reason the spec's 50-runs-per-arm floor matters.
- Q3 (per-role ladder): flash_vs_q8 is direct community evidence that quant-per-role beats one
  global quant: a heavily-quantized big MoE outperforms a Q8_0 smaller dense on agentic utility
  while losing ~3x on tok/s - i.e., role (judgment vs scut), latency budget, and quant must be
  chosen together. Kolibri (tensor-sensitivity bit spend) is the mechanism for per-artifact
  laddering inside one model.
- Q4 (GPU-ladder trigger): NO trigger evidence found - no in-window thread shows 24GB+ Blackwell
  under ~$1200 (`frontier_olm_2026-10-08/lens/laws.md:189-191`) or a used H100 under $4000. The
  in-window price signal points the other way: RTX 5090 ~$5,000 (2026-08-27 thread, out-of-window,
  context only) while the cheap-VRAM collapse is on used RDNA2 enterprise cards: 256 GB for
  ~$2,800 (~$10.9/GB, v620 thread). Quant-vs-card economics therefore still favor quant on this
  box. Caveat: thread anecdotes, not a price index; no marketplace scraped (IA offline, not
  attempted otherwise).
- Q5 (2026-10 releases vs the A/B design): GSQ (arXiv 2604.18556) closes most of the
  scalar-to-QTIP gap at 2-3 bits and improves existing GGUF K-Quants (Qwen3-8B Q2_K 50.03 to
  56.28) - i.e., the quant identity of an arm is becoming a versioned artifact, sharpening the
  spec's export-cast rider (hash the blob, pin the toolchain). LittleBit/LittleBit-2 push sub-1-bit
  QAT; both are scut-tier-relevant, verdict-channel-irrelevant at Q4_K_M-vs-q8_0.

## Banked items (strongest first, full citations in the structured result)

1. 4-bit Qwen2.5 vs official AWQ on the same vLLM kernel (1wyc2b0, 2026-10-05) - matched-kernel
   A/B on the estate's exact model family, with the OP's own noise/contamination limits section.
2. ROCm prebuilt silently serving from CPU on AMD (1wzdti3, 2026-10-06) - the missing pin leg
   for any A/B on this box.
3. Kolibri-1 at 2.30 bpw with tensor-sensitivity bit spend (1wyeanf, 2026-10-05) - KL + top-token
   agreement as paired channels; per-artifact ladder mechanism.
4. Heavily quantized Flash vs Q8_0 27B (1wvzmt3, 2026-10-02) - per-role quant-vs-quant verdict
   evidence with a measured latency cost.
5. GSQ-RCO release + expert-pruned Coder at ~1.89 bpw (1wt4s88, 2026-09-29) - calibration-mix
   coverage is load-bearing; capability loss is real and admitted by the maintainer.
6. GSQ paper, arXiv 2604.18556v2 (2026-05-15) - scalar-grid quants closing on QTIP; improving
   shipped GGUF K-Quants; quant identity versioning.
7. LittleBit, arXiv 2506.13771 (Reddit 2026-10-08; paper v5 2026-02-05, NeurIPS 2025) - sub-1-bit
   QAT frontier; LittleBit-2 (2603.00042) in thread.
8. 8x V620 = 256 GB VRAM ~$2,800 (1x0wnz1, 2026-10-08) - price-ladder evidence: no Blackwell
   trigger; used-RDNA2 per-GB collapse instead.

## Honesty notes

- Door was degraded for everything except RSS + WebSearch; recorded above with probe results.
  No fallback success is claimed beyond what ran.
- Scores/comment counts are not in RSS; "strong" here = relevance to the five questions plus
  thread depth read, not upvote counts.
- The three quotes banked from arXiv were fetched from arxiv.org directly this sitting; all
  Reddit quotes are verbatim substrings of the RSS content of the thread named, fetched this
  sitting. Nothing is quoted from search snippets alone; snippet-only threads were used for
  discovery and explicitly marked unbanked.
- The A/B remains un-run. This file does not change any lane's quant; register rows + burn
  receipt belong to the firing lane.
