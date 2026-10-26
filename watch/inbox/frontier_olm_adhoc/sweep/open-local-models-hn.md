# FRONTIER OLM ADHOC SWEEP: open-local-models via HN

source-fetched: adhoc · 2026-10-11 · door: hn.algolia.com API (search_by_date + search) + news.ycombinator.com item threads · all probes HTTP 200, no degradation, no 403s on the HN lane.

Method: two passes per the ask. Pass 1: 10 Algolia queries windowed to created_at_i > 1789084800 (2026-09-11, last 30 days): ollama (nbHits 77), "local LLM" (27), "open weights" (18), "small language model" (4), llama.cpp (26), qwen (236, noisy), "tool calling" (13), "local models" agent (15), gemma (134, mostly "German" noise), ROCm (165, mostly noise). Roughly 60 distinct on-topic candidates enumerated; 35 tabulated below. Pass 2: 10 pages read end to end, including 2 full HN comment threads (Otis 49696084, Magnitude 49911995 with 97 comments).

## PASS 2 DEEP READS (banked items, strongest first)

### 1. New in Llama.cpp: Decision Models (ggml-org blog) - 2026-10-02
https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp (HN 49934323 / 49942092)
Quote: "A decision model reads the input once, and its answer is always one of your options, with a probability attached."
What shipped: llama.cpp server gained /v1/systemone (System One format from TypeSafe's Jev), so "existing clients only need a new base URL". PR #29818. Three question types: choice / score / noul (yes-no probability). Open models: Julia-1 144M (mmBERT-small, Apache 2.0, 3 ms), Laya 421M (ModernBERT-large, 5 ms), Kev-4B (Qwen3.5-4B-Base, 12 ms), lev 4B (36 ms), OpenJev 27B (CC BY-NC 4.0, 43 ms), Clef 27B (Apache 2.0, vision). Latencies are medians on one RTX PRO 6000. Router mode: multiple models, one server. Named uses: request routing, moderation, verifying whether an agent step succeeded, choosing its next action. Calibration warning: a vague ticket scored 0.25 with Julia-1 vs 0.80 with Kev-4B.
Why the estate cares: this is the open-weights resolution of the Jev concept our seat memory held as "not open weights". The 144M-4B Apache models at ms latency are direct refill candidates for RIB_MODEL_GARDEN_ROUTING decision cells before the ~2026-10-30 lapse, and the per-option-probability API is the tri-state verdict organ the 09-16 seat memory wanted to wire behind the switchboard.
Overlap: concept held at memory/continuity/seat_memory_20260927/jev-system-one-decision-model-20260916.md (2026-09-16, explicitly pre-open-weights); catalog has "decision model" x22 and "jev" x146 (concept rows incl. the 2026-10-07 nimble_public_benchmarks.md); the ggml-org blog URL itself has 0 catalog hits. The shipment plus Apache weights are the new delta.

### 2. Ollama now supports Jev-style decision models - 2026-09-29
https://ollama.com/blog/ollama-now-supports-jev-style-decision-models (HN 49906337 / 49908997)
Quote: "Send text as state with a set of named questions, and a model running on your machine answers them all in one request."
What shipped: Ollama 0.35 adds /v1/systemone (model + state + questions map of Choice/Noul/Score), answers with probabilities and confidence in one round trip, reachable by curl or typesafe-sdk at localhost. Models: nimble (9B, Bespoke Labs, open source), tev1 (4B, Together AI, experimental), tev1:0.8b. "Nimble 9B averaged 91ms per decision" in a Pac-Man demo on an M5 Max. Benchmarks span 3,880 decisions across 13 labeled datasets. Roadmap: MLX on Apple Silicon.
Why: this is the direct RQ2 answer for the janitor lane: the runtime under gemma:2b gained a second model class and a new endpoint since the 2026-07-20 basics pack. The 0.8B tev1 is squarely in the estate's 1-8B class for cheap routing cells.
Overlap: nimble public benchmarks already banked (watch/inbox/frontier_olm_2026-10-07/sweep/nimble_public_benchmarks.md, catalog row, 38286 bytes); Jev concept held (seat memory above); the ollama.com/blog URL and the 0.35 endpoint change have 0 catalog hits. New as a runtime fact, partially held as a model fact.

### 3. Truncation-safe tool calling (Xyntetik Runner) - 2026-09-15
https://xyntetik.com/runner/truncation-safe-tool-calling/ (HN 49719027)
Quote: "A tool call is JSON, and JSON that stops early is not JSON."
Mechanism: a streaming schema validator constrains tool-call JSON during decoding; when max_tokens expires it emits the smallest schema-legal ending, so returned tool_calls always parse while finish_reason stays "length". Cross-engine test at token budgets 1/2/3/5/8/16/64 (temperature 0, tool_choice required) on granite-4.1-3b: only Runner returned parseable calls at every budget. Failure modes of the majors: leaked framing into prose (vLLM 0.27.1, llama.cpp b10488), unparseable arguments at 16 tokens (llama.cpp), HTTP 500 (Ollama 0.32.14 at 16), empty call-less HTTP 200 (TensorRT-LLM 1.2.1, SGLang 0.5.17). Quant ladder: schema conformance and tool selection held 100% down to Q4_0, argument agreement vs Q8_0 fell to 50%.
Why: RQ1's real failure surface. Multi-step agent loops die on mid-call truncation and on argument drift at aggressive quants; this page hands the estate a ready-made instrument (the budget ladder) for the UNMEASURED garden cells, and a caution that Q4_0 preserves selection but halves argument fidelity.
Overlap: xyntetik 0 hits in catalog and memory (generic "truncation" matches are kv-cache/audit noise, unrelated). New.

### 4. Benchmarking Local LLM Servers (Mozilla AI) - 2026-09-17
https://blog.mozilla.ai/benchmarking-local-llm-servers-llama-cpp-llamafile-lm-studio-and-ollama/ (HN 49742415)
Quote: "The biggest speedups came from configuration, not the choice of engine."
Setup: llama.cpp b10441, llamafile 0.10.6, Ollama 0.34.0, LM Studio 2.28.2 on Mac Studio M4 Max 64GB / Xeon+L40S 48GB CUDA / Steam Deck OLED (Van Gogh, Vulkan). Same GGUF weights everywhere (Ollama via tags built from those files). Qwen 0.8B Q8, 9B and 27B Q4_K_M, 16k context, full GPU offload. Metrics: client-side tokens/s only, prompt processing and generation; 15 runs per point, drop warm-up and fastest/slowest 2, average middle 10.
Numbers: CUDA graphs gave +16.8% (0.8B) / +6.5% (9B) / +4.3% (27B); newer Vulkan shader toolchain on Deck +63.3% PP on the 9B; draft-2 spec decoding best on Metal, draft-4 up to +16% on CUDA; decode gap fixed host overhead about 0.4 ms (Mac) / 1.8 (L40S) / 5.4 (Deck); on Metal llama.cpp, llamafile, Ollama within ±3% PP; Ollama's Vulkan lagged on the Deck; MLX about +10% PP on the 27B. No Windows testing: "The next round should include Windows and additional macOS and Linux hardware."
Why: the steal is the protocol, not the verdicts: same-weights cross-server client-side tok/s with trimmed-repeat statistics is exactly the instruments-only, no-vendor-numbers shape RIB_MODEL_GARDEN_ROUTING cells need before the ~2026-10-30 lapse.
Overlap: blog.mozilla.ai and "benchmarking local llm" 0 hits anywhere. New.

### 5. Launch HN: Magnitude (YC S25), self-optimizing inference engine for agents - 2026-09-30
https://news.ycombinator.com/item?id=49911995 (194 points, 97 comments; repo magnitudedev/magnitude)
Quote (commenter sebastienburel): "It's resending the same system prompt plus tool schemas every turn."
Founders' claims: Rust engine tuning kernels on your hardware; vs llama.cpp with Qwen 3.6 35B A3B 4-bit, 64k context, no spec decoding: Metal M4 Pro 92% faster decode (30 to 57 tok/s), DGX Spark 19% faster decode; KV cache quantization (8-bit keys, 4-bit values) "drops KV memory usage by over half"; prefix-cache sharing across sessions; OpenAI-compatible endpoints; Vulkan used for AMD, ROCm possible.
The thread is the signal: user counters beat the claims (Rapid-MLX 175 tok/s vs Magnitude 161 on M5 Max; francisjp roughly 2x faster served from llama.cpp; mrtsepelev prefill ~2.6x slower; 5070ti llama.cpp 20-30% faster at decode). Small-RAM reports: GTX 1650 4GB no model fits; 64GB+5080 capped at a 9B suggestion. Founders keep the catalog at 4-bit because below it "thinking, tool calling, and overall capabilities start to suffer". happybox2016: "Real agent bottleneck isn't single-stream tok/s - it's KV cache for 5+ concurrent 128k contexts on 24GB VRAM." Win11 hardware-detection bug reported (karlkloss).
Why: RQ1/RQ5. The thread is a free instrument design review for the estate's agent loops: optimize prefix reuse and KV footprint, not raw tok/s; and the 4-bit floor for tool calling matches the Xyntetik quant ladder independently.
Overlap: magnitudedev 0 hits; catalog "magnitude" x9 all generic (approximation-theory papers, signal-magnitude receipts). New.

### 6. ROCmFix (AMD local-LLM setup tool) - 2026-09-19
https://github.com/xanpavle/rocmfix (HN 49770070)
Quote: "Temporarily isolates Ollama or LM Studio, runs a generation test using Vulkan, then HIP, and tells you which is faster on your PC."
Single-file Python (no venv), auto-detects AMD GPUs on Windows/Linux and applies the correct HSA_OVERRIDE_GRX_VERSION for llama.cpp / Ollama / LM Studio / PyTorch, fixing HSA_STATUS_ERROR_INVALID_ISA and silent CPU fallbacks; edits shell configs with an undo. Targets RDNA4 (9070/9060), RDNA3, RDNA2 and iGPUs; "17+ GPUs currently supported in the database". README carries no measured numbers, only guidance (Vulkan often faster on consumer RDNA3, works out of the box on Windows; PyTorch needs HIP).
Why: this box is RDNA1 with no FP8 path; the rocmfix bench race is a ready instrument for the Vulkan-vs-HIP cell of the garden on exactly our hardware class, and the HSA override machinery is the standing cure for silent CPU fallback in the janitor lane.
Overlap: rocmfix 0 hits in catalog and memory. New.

### 7. Not a setting: why we removed Ollama from Return - 2026-09-28
https://returneditor.ai/blog/not-a-setting-why-we-removed-ollama/ (HN 49882932)
Quote: "the inability to exfiltrate document content should be a property of the code we ship, not a setting"
The RQ2 API-surface change from the other side: Ollama 0.12 (Sept 2025) added -cloud suffix models proxied to Ollama's datacenter, so "Traffic to localhost:11434 could now be the first hop rather than the destination". Return (lawyer doc tool) replaced Ollama with a bundled llama-server sidecar: -m with local GGUF path, 127.0.0.1 on an OS-assigned port, model downloads owned by app code, remote inference compiled out (Sept 2026), embeddings sidecar costs roughly 500-700 MB. No Windows-specific problems described.
Why: for a sovereign-local estate this is the trust-boundary lesson for the janitor lane's own runtime: a local port is no longer proof of local execution once the daemon can proxy; the sidecar-plus-compiled-out-egress pattern is stealable.
Overlap: returneditor 0 hits anywhere. New.

## REBANKS EXCLUDED (already held; do not re-file)

- arXiv 2609.21341 "What Stops a Small Language Model From Driving a Database Agent" (2026-09-18): already fetched by the 09-28 sweep; memory/corpus/LINKS.jsonl row points at frontier_olm_20260928/sweep/_raw/full_2609.21341.txt. I re-read the abstract page only to re-confirm quotes. Its numbers still matter for RQ1 (75.7% of agent-mode losses had at least one tool call; transport failures 36.2% vs capability 17.3%; five server-only fixes moved six models 6-21 cells of 30; uncapped context made a 7.1 GB model hold 51 GB): the wall is mechanism shape, not model size.
- Kisoku 1.6B (2026-10-09): banked hours ago by a sibling lane, catalog row watch/inbox/frontier_olm_adhoc/sweep/raw/art_kisoku.md (2026-10-11T03:45Z). I read the repo anyway: 1.6B from scratch on a TPU grant, Apache 2.0, 64k context, "matches Meta's Llama 3.2 1B (five wins each) while using about 18 times less training data"; no tool-calling claims at all.
- Underdog Saluki (Qwen3.8-27B under 8GB, 2026-10-09): sibling lane already holds _tmp_pages/saluki.html (2026-10-11T03:28Z); also outside the 1-8B class.
- Otis agent thread (49696084, read in full): thin signal (differentiation openly questioned by commenters; automatic model routing is planned, not shipped); overlap grep ambiguous ("triangl" matches 25 math-corpus triangle rows). Left unbanked deliberately.

## PASS 1 CANDIDATE TABLE (further unbanked, one line each)

- 49963695 Clef and Clef Flash from Cloudflare on ollama.com/library/clef (ties to decision-model Clef 27B Apache)
- 49812339 Transformers now runs llama.cpp quants (quant-format interop, RQ2)
- 49859982 Faster prompt lookup drafting in llama.cpp (89 pts; spec-decoding tok/s, RQ5)
- 49938916 LLaMA Now Goes Faster on CPUs (justine.lol matmul; CPU fallback lane)
- 49876817 2.2x more tokens/s from llama.cpp on Intel Arc (vendor-box tokens/s method)
- 49981275 TOD: universal decision model, Task Oriented Design (decision-lane)
- 49736660 Open-sourced jev architecture with model, paper, dataset (97 pts; concept already held in seat memory)
- 49984852 SLM database agent arXiv (REBANK, held)
- 49996713 "not paying $20 because a free local LLM does" (52 pts, consumer angle)
- 49706656 Sunk Cost local-LLM rig payback calculator (47 pts, 99 comments; economics instrument)
- 49982904 Reika: coding agent CLI for small local models first
- 49754659 MonkeyDcode: CLI coding agent for small local models
- 49785853 Local-coder: team of coding agents with local models
- 49921633 Sriti Core: local-first router cascading Ollama to cloud (routing cell kin)
- 49882932 Return removed Ollama (BANKED above)
- 49933664 Local LLM won't stop talking: chat templates go wrong (template/API behavior, RQ2-adjacent)
- 50002660 AI Development on Windows: PyTorch and Llama.cpp to Windows ML (Microsoft; Windows lane, unread)
- 49998043 MS announces DeepSeek V4 Flash and Nemotron locally, llama.cpp to Win ML (unread)
- 50025042 Kisoku 1.6B (REBANK, held)
- 50017301 Apogee: Mozilla Orbit rebuilt fully local (66 pts; on-device voice stack)
- 50029518 SRA-RiskGate-4B local LLM for stablecoin gating (niche 4B fine-tune)
- 49770070 ROCmFix (BANKED above)
- 50034279 Microsoft built its decision model on Qwen (decision lane, unread)
- 49796733 XGrammar-2 structured generation for tool calling (instrument kin to Xyntetik)

## RESEARCH QUESTION ANSWERS

RQ1 (1-8B models sustaining multi-step tool loops on RDNA1, no FP8): the sweep's evidence says the binding constraint is plumbing, not parameters: the held arXiv corpus shows 1.7B-24B open models do invoke tools and fail on argument-shape transport; Xyntetik shows selection survives Q4_0 while argument fidelity halves; Magnitude's founders put the tool-calling floor at 4-bit. For this box: Q4-class quants via Vulkan-or-HIP (rocmfix bench decides), decision cells offloaded to 144M-4B Apache models at ms latency through /v1/systemone, generative tool cells probed with the budget ladder. Measured RDNA1 tokens/s for any of these: OWED, not in anything fetched.
RQ2 (Ollama changes since 2026-07-20): version arc documented from fetched pages: 0.32.14 (HTTP 500 on 16-token tool budgets), 0.34.0 (Mozilla bench: Vulkan lag on Deck, MLX adaptive spec decode self-enabled), 0.35 (2026-09-29: /v1/systemone decision endpoint, nimble/tev1 models). Older but load-bearing: 0.12's -cloud suffix broke "localhost means local". llama.cpp side: decision models PR #29818, Transformers-GGUF interop, prompt-lookup drafting gains. Windows-specific Ollama behavior: nothing measured in-window; Mozilla explicitly defers Windows to a next round (OWED).
RQ3 (Reddit wall): answered by probe this run. curl.exe with browser UA: www.reddit.com JSON 403, old.reddit.com JSON 403, www no-UA 403. BUT https://www.reddit.com/r/LocalLLaMA/.rss with the same UA returns HTTP 200, 90,486 bytes of live content (verified titles incl. "Whistle: speech to text in 16.9 MB", "microsoft/AesCode 8B and 32B", a DeepSeek V4.1 Flash key-exfiltration PSA). lobste.rs/hottest.json also 200 (20,610 bytes). Fourth lane: the .rss variant works today; lobste.rs JSON is the fallback if RSS joins the wall.
RQ4 (liveness cross-check when counters read flat): use entry-content recency, which this run exercised: every search_by_date query returned newest entries created 2026-10-11 (today), e.g. objectIDs 50041727 and 50039529, regardless of flat all-time nbHits. Secondarily, replace all-time counters with windowed counts via numericFilters (this run's 30-day windows: 77 / 27 / 26 / 18 / 13), which move daily by construction.
RQ5 (garden refill, instruments-only): fill order suggested by the reads: (a) rocmfix bench Vulkan-vs-HIP race on this box for the backend cell; (b) Mozilla's 15-run trimmed client-side tok/s protocol for throughput cells; (c) Xyntetik's 1/2/3/5/8/16/64 budget ladder plus Q4_0-vs-Q8_0 argument agreement for tool cells; (d) decision cells via /v1/systemone with Julia-1 / Laya / Kev-4B (Apache 2.0). Vendor latency numbers (RTX PRO 6000, M5 Max) are routing hints only; RDNA1 self-measurements are the bankable values.

OWED from this sweep: measured RDNA1 tokens/s for the decision models and for tev1:0.8b; Windows Ollama specifics; deep read of AesCode 8B (RSS title only, unread); XGrammar-2 vs Runner structured-output comparison.
