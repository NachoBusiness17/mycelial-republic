# SWEEP: open-local-language-models via hn - 2026-10-01

source-fetched: 2026-10-01
Seat: sweep gopher, area open-local-language-models, door = HN Algolia (+ arXiv per lens/doors.md which probed both doors OPEN today). Repo: C:/Users/foste/Documents/projects/local_sovereign_agent. Every claim below was read or run this session.

## Door status

- HN Algolia: CLEAN. 14 `search_by_date` queries returned JSON, zero 403s, zero retries. Date filter `numericFilters=created_at_i>1788220800` (2026-09-01) for 30-day passes and `>1785628800` (2026-08-02) for the 60-day stack pass.
- VentureBeat article page (DeepSeek political-triggers story): HTTP 429 TWICE (initial + one retry). Not read. Banked via the recipe's named fallback (the HN thread, id 49785849) and marked thread-level only. No fallback success is claimed for the article itself.
- arXiv door: probed OPEN this morning by the sibling lens (`watch/inbox/frontier_olm_2026-10-01/lens/doors.md:11,21-28`); this seat consumed its arXiv item via the HN submission of the books-memorization project rather than a second arXiv API pass.

## Pass 1 (broad census, 30-day window unless noted)

40+ stories considered across queries: qwen, gemma, llama.cpp, ollama, deepseek, mistral, "local llm", gguf, quantization, mlx, vllm, refusal, uncensored, "open weights". Strongest raw hits: Magnitude Launch HN 178/87 (49911995, 09-30), Ollaya 615/145 (49848269, 09-25, HELD), quesma Qwen3.8-27B quant bench 286/139 (49611128, 09-08, HELD), DeepSeek Elastic Compute 323/115 (49859112, 09-26, out of area), Dynamic Abliteration 108/42 (49831201, 09-24), prompt lookup drafting 89/12 (49859982, 09-26, HELD), Gerganov ggml-future 76/28 (49567357, 09-04, HELD), Offensive-Security benchmark 38/12 (49888937, 09-29), open letter to Dario 308 (49676085, held 09-28). Low-point but on-RQ: DeepSeek political triggers 5/1 (49785849), Reflex cold-start 1/0 (49903234), books-memorization 1/0 (49921077, 10-01), Echoleak-immunized Llama 3.1 2/0 (49879581), IttyBittyAI Qwen2.5:0.5B on a 2017 phone 2/0 (49835080), PicoLM on Digital Unix (49818282), 2.2x llama.cpp Intel Arc (49876817), Jevstiller distillation (49912498).

## Dedup ledger (prior carriers + catalog + memory greps actually run)

Greps run: `rg -n -i` over `catalog/catalog.jsonl` (full) for 14 candidate terms; `memory/` full-tree for title/URL slugs (`-g *.md -g *.jsonl -g *.txt -g *.json`); term-by-term `rg -l` over `watch/inbox/frontier_olm_20260928/` and `watch/inbox/frontier_olm_2026-09-30/` (the two prior olm carriers per `lens/burns.md:48-61`).

EXCLUDED as already held (re-banking is waste):
- quesma 4-bit-vs-1-bit bench: 09-28 DIGEST.md:72 + quantization-compression-hn.md.
- Gerganov / NVIDIA-HF acquisition: 09-28 register.jsonl row 2 + raw file `fx_ggerganov_status_2095897173376618881.json`.
- prompt lookup drafting (49859982), duane.sh Qwen3.5-4B fine-tune, Ollama 0.35 Jev models, Ollaya, Clippy thread: 09-30 sweep open-and-local-language-models-hn.md pass 2 (its lines 34-47).
- Mozilla local-server benchmark (49742415): 09-28 carrier, inference-efficiency-x + quantization-compression-hn.
- Gemma 4 megakernel (49897153), SoTA Feed, StepFun: pooled/adjudicated by the 09-30 arxiv sibling ("hold: throughput ceiling signal").
- Ternary-Bonsai-8B/27B GGUF, VeriLoop BF16-to-IQ1_M ladder, pfeifferj GSQ-RCO GGUF, bartowski layout maps: 09-30 quantization-compression-hn census + deep read (27B card), and the 27B GGUF is already pulled locally per `watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:11`.
- Abliteration prior art generally: catalog rows for abliteration surface cells (09-13), Steiniger papers, `ABLITERATUS_DROP_20260929.md` (Pliny one-click toolkit), arXiv 2609.16204 decoy-direction defense. Item 2 below is a NEW method (trained gate, non-destructive), not a re-bank of these.

## Pass 2 (deep reads, end to end, this session)

9 pages read: madhukaraphatak Dynamic Abliteration blog + its 42-comment HN thread; pentesttoday offensive-cyber post; HF transformers-llama-cpp-quants blog; books-memorization.github.io; Offensive-Security-AI-Models repo README; HN thread 49785849 (the VentureBeat 429 fallback); lateos-ai/reflex README; magnitudedev/magnitude README.

## Findings by research question

### RQ1 - janitor-class (<=8B consumer) upgrade over gemma:2b/gemma4

No NEW general-purpose <=8B family release surfaced in this pass's window; the upgrade verdict already banked by the 09-30 carrier stands (Ollama 0.35 typed-decision models tev1:0.8B / tev1 4B / nimble 9B as the scut drop-in; Qwen3.5-4B fine-tune path; Gemma 4 getting throughput work only). What this pass adds: (a) a hardened-janitor NICHE exists: 7-9B security-fine-tuned open weights (Dolphin3-Cyber-8B, Lily-Cyber-7B, Qwythos-9B, security-slm-1.5b) catalogued in item 4, all scores vendor-self-reported; (b) a family-vetting lens: the COLM 2026 memorization study (item 5) shows some open weights memorize books at ~100% extraction probability, a reason to screen families before pulling them into the janitor fleet. Licenses seen this pass: Reflex MIT, Magnitude Apache-2.0; the Offensive-Security repo has NO license file; HF GGUF post introduces no new license (checkpoint licenses remain vendor-specific).

### RQ2 - refusal/censorship across runtimes (extends C1 E1-E3, lens/burns.md)

Three measured-behavior reads, none of which ran an Ollama-vs-transformers refusal A/B: that gap is still ours to run, and item 1 removes its last technical excuse.
- Item 1 (HF blog 09-22): transformers now loads the SAME GGUF quants llama.cpp/Ollama serves (Qwen3.5/3.8, Q4_K_M/Q5_K_M/Q6_K; packed inference MPS-only). C1's E-series can now hold weights constant byte-for-byte across runtimes and vary only the runtime, which is exactly the controlled design E1-E3 wanted.
- Item 2 (blog + thread 09-24): Dynamic Abliteration steers Qwen3-4B refusals via a TRAINED gated module on residual activations (forward hooks, transformers bf16, PKU-SafeRLHF trained, ~2k samples). Residual-stream surgery is transformers-shaped; it cannot ride Ollama's prompt-level API, which independently corroborates the window-1 memlance finding that C1 rides prompt-level instruments. Thread adjudication worth stealing: the author conceded goldemerald's correction that naive steering is wrong, the projected refusal direction must be computed and only that subtracted; a suspected training-loop bug around `current_train_input_ids` was flagged and left open. No quantitative refusal metrics were published; refusal was judged by reading outputs.
- Item 3 (09-17): on the T3MP3ST harness vs OWASP Juice Shop, Chinese open-weights refused at surprisingly high rates (Kimi K3 3 vulnerabilities found, GLM 5.3 9, vs GPT 5.6 Sol 29 and its Daybreak Blue variant 56), and abliterated open-weights ALL failed to complete a pentest: refusal suppression does not manufacture capability. E-series should therefore measure compliance AND task success, never refusal rate alone.
- Item 4 (09-29): a 27-model catalogue of uncensored/security-fine-tuned weights (incl. GLM-5.3-Flash-Uncensored at a vendor-claimed 82.8 percent compliance) is a ready substrate list for E-series probes; everything is self-reported, no independent testing described, repo unlicensed.
- Item 8 (09-21, thread-level only): headline claim that Chinese political triggers raise injected security bugs 50 percent; the single thread comment (verdverm) offers the cheaper mechanism, distraction, not censorship: "you're distracting the model, of course it will make more mistakes". The VentureBeat article itself 429'd twice and was NOT read; treat the number as unverified.

### RQ3 - local inference stack changes, last 60 days

Banked-elsewhere and confirmed standing: Ollama 0.35 typed-decision endpoint (09-30), prompt-lookup drafting in llama.cpp (09-26), Gerganov's hardware-agnostic commitment post NVIDIA-HF (09-04). New this pass: two engine entrants positioning against llama.cpp/Ollama/vLLM. Magnitude (Apache-2.0, desktop app) compiles and tunes kernels per device and claims up to 2x over llama.cpp (92 percent faster decode on Metal, 19 percent on CUDA) plus 27 percent less memory per agent; claims are vendor numbers, unverified. Reflex (MIT, Rust, AOT nvcc kernels) targets cold-start: 456 ms p50 process-launch-to-result on a T4 with Qwen3-0.6B-Q4_K_M, 2.6x vs Ollama and 1.13x vs llama-simple on the same box; it discloses that its vLLM comparison ran safetensors rather than GGUF, and reports no warm tok/s. MLX: nothing material in-window beyond the banked Qwen3.8-27B-Uncensored-MLX (08-19, outside window).

### RQ4 - day-0 GGUF and per-quant footprints

No new day-0 GGUF drop beat what the 09-30 quantization carrier already banked (VeriLoop full BF16-to-IQ1_M ladder, Ternary-Bonsai GGUFs, pfeifferj GSQ-RCO on 2x RTX3090). New footprint datapoints this pass are cold-start shaped, not GB-per-quant shaped: Reflex 456 ms p50 (T4, 0.6B Q4_K_M, n=10, phase breakdown: GGUF open ~37 ms, process launch ~130 ms, CUDA init ~140 ms, model load ~237 ms, scoring ~39 ms); Magnitude "27 percent less memory per agent" (relative, unverified). The HF GGUF post recommends Q4_K_M as the starting quant and restricts packed inference to MPS. RAM/VRAM-per-quant tables for a specific drop-in candidate remain OWED (below).

## OWED / not done this seat

- VentureBeat article body: 429 twice, never read; the 50 percent figure is thread-headline only. A funded-tier or UA-different fetch could close it.
- Magnitude and Reflex performance claims: vendor-self-reported; no independent rerun. A `mag` box probe of Magnitude's Windows build vs llama.cpp on gemma:2b scut latency would be the honest test.
- Item 2's suspected Engram-training bug (`current_train_input_ids` never updated during generation): flagged in-thread, not confirmed by me; code inspection of phatak-dev/LLMExperiments owed before citing it as fact.
- No RAM/VRAM-per-quant table for any <=8B candidate was produced this pass; the 09-30 quantization carrier's ladder data remains the best held source.

## Method notes (honest limits)

- Quotes below are verbatim from the fetched pages as returned by the fetcher; the Reflex quote contains one em dash that is part of the original README line.
- The Offensive-Security README fetcher speculated some model families were unfamiliar to it; our own corpus (qwen.ai Qwen3.8-Flash-Next story 49448210 in the 09-28 carrier, GLM-5.3 items throughout) confirms those families exist, so I kept only the self-reported-scores caveat and dropped the fetcher's existence speculation.
- Point/comment counts are as of fetch moment 2026-10-01; counts drift (B2-216 discipline applies).
