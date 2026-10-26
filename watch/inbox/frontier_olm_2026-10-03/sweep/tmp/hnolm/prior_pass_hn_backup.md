# Sweep: open-and-local-language-models via HN

source-fetched: 2026-10-03
Seat: sweep-open-and-local-language-models-hn (frontier gopher, Mag Resource Harness)
Doors: hn.algolia.com API (search_by_date + search) and news.ycombinator.com item pages, via WebFetch. All fetches live this session.

## Method

Pass 1 (broad sweep): 12 Algolia queries with a 30-day numeric filter (created_at_i > 1788393600 = 2026-09-03), hitsPerPage 30: "open weights", "local LLM", "Qwen", "Gemma", "tool calling", "free tier rate limit", "small language model", "agentic benchmark", "function calling", "ollama", "rate limit", "Groq", "SmolLM", "Nemotron", plus unfiltered relevance searches for "free tier API limits LLM" and "OpenRouter" and "DeepSeek" and "Cerebras". Distinct candidate stories considered: 45+ (enumerated below). Door status: the Algolia API returned clean JSON on every query except "requests per minute" which returned nbHits: 0 (empty, not an error), and "free tier rate limit" returned only 3 stories (mostly off-topic), so RQ2 coverage was carried instead by the Cerebras provider docs plus its 691-point thread. WebFetch's JSON extraction truncated the final hit of two query results (the "tool calling" and "agentic benchmark" lists); those truncated entries were dropped, not guessed. "Groq" as a query surfaced mainly the unrelated Grok/Venezuela news cluster; no usable Groq rate-limit story was found in-window.

Pass 2 (deep reads, 13 fetches, article + thread pairs): Cactus Needle 3 article + 236-pt thread; Cloudflare Clef blog + 622-pt thread; Cerebras Qwen3.8-27B docs overview + 691-pt thread; llama.cpp decision models blog; AA-AgentPerf-Local article; Weave Router HN item (story text + comments); Kolibri tej.as teardown; Raspberry Pi Needle 2 article; Ask HN inference thread; Ollama decision-models blog. Two of those (Cactus Needle 3, Ollama decision models) were read and then EXCLUDED from banking as already-held estate work (see overlap section).

Quotes below are verbatim as returned by WebFetch's page reading of the live URLs; they were not re-verified against raw bytes, so treat exact punctuation with that caveat.

## Findings by research question

### RQ1: open-weight releases of the last 30 days that beat gemma:2b / gemma3-4b at janitor tasks at equal or lower RAM, on named benchmarks

The dominant wave is Jev-style decision models (schema-constrained classify/score/yes-no), and it landed in OUR runtime stack this window:

- llama.cpp now runs them (huggingface.co/blog/ggml-org/decision-models-in-llamacpp): a /v1/systemone endpoint scoring choice/score/noul question types, with a support table of Julia-1 (144M, mmBERT-small base, Apache 2.0, 3 ms), Laya (421M, ModernBERT-large base, Apache 2.0, 5 ms), Kev-4B (Qwen3.5-4B base, Apache 2.0, 12 ms), lev (4B, Apache 2.0, 36 ms), OpenJev (27B, CC BY-NC 4.0, 43 ms, adds vision). Millisecond latencies on one RTX PRO 6000; GGUF quantizations are ordinary (Q8_0 shown).
- Cloudflare shipped Clef and Clef-flash (blog.cloudflare.com/clef-decision-models/): "fully open-sourcing these models on Hugging Face under an Apache 2.0 license", frozen from Qwen3.8-27B and Qwen3.5-9B with rank-256 LoRA; BFCL case-exact 98.47 / 98.76, BANKING77 macro-F1 94.20, median 209.3 ms / 38.8 ms vs Jev 524.1 ms across "43 eval benchmarks".
- Ollama 0.35 ships decision models (nimble 9B open source from Bespoke, tev1 4B and tev1:0.8b experimental from Together AI); "Nimble 9B averaged 91ms per decision" on an M5 Max.

Direct gemma:2b-head-to-head evidence is still thin: no in-window page published a gemma:2b / gemma3-4b baseline against these. The closest adversarial data is the Cactus Needle 3 thread (already held, excluded from banking) where community benchmarks showed vendor claims not transferring, and the Clef thread where dgacmu reported "local gemma4:27b" beating Clef on a vision classification task (41% vs 53%, 4x faster). Honest verdict for RQ1: the decision-model class (0.14B-9B, Apache mostly) plausibly displaces the gemma:2b janitor lane at lower RAM, and the estate should benchmark Kev-4B/lev/Laya against gemma:2b on its own tri-state forms, but no third party has published that comparison yet.

### RQ2: free-tier rate-limit mechanics (width vs rolling throughput) for open-model endpoints

The single strongest evidence in-window is the 691-point thread on "Qwen 3.8 27B available on Cerebras at 1500 tokens/s" (inference-docs.cerebras.ai/models/overview, thread id 49554520). The docs page itself says models are usable on Free Trial and Pay As You Go tiers "subject to rate limits and pricing" without numbers, but the thread measured the mechanics:

- nostrebored: "150k TPM limit on public endpoint means that it's likely unusable for many coding tasks."
- wild_egg: "So that's 3 50k requests per minute. At Cerebras speeds, that's about 5 seconds of usage per minute." The cap is a rolling per-minute TOKEN budget, not a concurrency/width cap; at high tok/s the budget is exhausted almost immediately.
- RussianCow: "10 requests with 50k of context will blow through the limit, even if little to no output was generated." Input tokens dominate; agentic workloads are the worst case.
- gpugreg hit the ~450k tokens/min ceiling in ~90 seconds and noted cached tokens count toward the limit; eli measured p50 890 tok/s with "a few brief 429 rate limit errors" and a 91.4% cache hit rate with zero discount ("Input tokens, whether served from the cache or processed fresh, are billed at the standard input token rate").
- puppymaster: Gemma was pulled from the shared tier the same day Qwen launched, staff saying "you aren't suppose to build production app on shared tier."

This bears directly on the estate's OPEN free-lane contradiction (lens/laws.md): the estate's own measured envelope says the cap lives on rolling throughput, not width, and Cerebras's public endpoint is the same shape: a rolling input-TPM budget that 50k-context agent turns drain in seconds, plus silent model churn on the shared tier. The estate's DRIVING LADDER rule (free lanes are sensing-only, funded lanes for judgment) survives this evidence intact. The community side is thin: the Ask HN "How are you getting inference for personal projects?" thread (49866739) has zero RPM-cap reports; the only limit mentions are subscription weekly windows (intrr: "I very rarely hit the limits, particularly the weekly ones").

### RQ3: permissive-license 7-14B models with clean native tool-calling

- Clef-flash is 9B, Apache 2.0, scored on tool-selection suites (BFCL 98.76, ToolRet nDCG@10 66.43, API-Bank 93.11, When2Call), though it is a decision head, not an autonomous tool executor; the thread's real-world tests were mostly negative vs hosted Jev (agrippanux: "Clef was 2-3x slower and worse (it caught less hate speech) than Jev"; pdlug: Clef p50 ~850ms vs Jev ~110ms).
- The llama.cpp table's Apache 2.0 column (Julia-1, Laya, Kev-4B, lev) is the friction-free option; OpenJev's CC BY-NC 4.0 is the community-license trap to avoid.
- At the extreme low end, Raspberry Pi's guest post on Cactus Needle 2 (14MB function-calling model, "Weights and code on Hugging Face and GitHub under Apache 2.0") shows text-to-tool-call on a Pi 5 CPU at 76-149 ms wall clock with refusal of out-of-scope asks ("What is the capital of France?" produced no call).
- Kolibri (Aleph Alpha, out 2026-10-03) is Apache 2.0 but is NOT the answer: 78.1B total / 3.46B active, ~78 GB FP8, German+English only, and its own teardown lists multi-turn BFCL 39.8 and Terminal-Bench 2.1 at 27.7. No 7-14B Apache/MIT model with demonstrated clean native tool-calling surfaced in-window that beats what the estate already runs.

### RQ4: do sub-8B models clear judgment-class bars on agentic benchmarks?

- AA-AgentPerf-Local (artificialanalysis.ai/articles/aa-agentperf-local, 2026-09-30) replays 8 recorded agentic sessions (168 turns, context growing to ~56K tokens) on 4 local hardware tiers, but its smallest model is Qwen3.5-9B: NO sub-8B model is tested, and it measures completion time, not task success. The absence is itself the finding: the current local-agent benchmarking wave has no sub-8B judgment evidence either way.
- The Weave Router item (49911500, 118 pts) independently supports the tier ladder: it reaches Astra-level pass rates (Terminal Bench 4.0 at 52% of Astra's cost, 2.2x faster; SWE Atlas at 54%, 2.5x faster) by ROUTING simple work down to DeepSeek v4 Flash and keeping judgment up top, and its purpose-built router model is closed-weights. svnt's skepticism ("how do you expect to exceed the performance of frontier models, other than in the cost dimension") went unanswered on quality grounds.
- Verdict: the tier ladder (ollama/local first for sensing, funded primes for judgment) remains correct on current evidence. Nothing in-window shows a sub-8B model clearing a judgment bar; the new decision models are exactly a sensing/triage instrument, not a judgment instrument.

## Overlap check (catalog + memory greps, run this session)

- Cactus Needle 3: HELD. memory/runs/gapwave/hn_x_fanout/skill_quantization.md:11 and :94 already analyze it including the contested HN reception; memory/runs/mickey17_v2/lanes/small-model-agents.json:14,18 hold the claim card. Excluded from banking.
- Ollama decision-models blog: HELD as percolator candidate. memory/percolator/candidates.jsonl:10 sources the exact URL from frontier_olm_2026-10-01. Excluded from banking.
- Jev / decision-model concept: HELD deeply. memory/continuity/seat_memory_20260927/jev-system-one-decision-model-20260916.md ("Hosted API, early-access waitlist, not open weights" at that time); jev-salon2-fold-20260919.md:3,23 ("Nimble front-runner"); rib-language-cache-os-20260919.md:46 ("Bespoke Nimble (open Jev, Qwen3.5-9B LoRA, 90 vs 93 hosted"); MEMORY.md:315. The NEW deltas banked here: Cloudflare's Apache-2.0 open-weights entry, the llama.cpp/Ollama runtime landings, the Cerebras TPM mechanics, AA-AgentPerf-Local, Weave Router, Kolibri.
- Greps that returned zero: catalog.jsonl has 0 hits for Cactus, Needle 3, Clef, Kolibri, AgentPerf, weaveos, "1500 tokens", nimble, tev1, turn-text-input-into-actions, decision-models-in-llamacpp, clef-decision-models, agentperf-local. "Cerebras" has 57 catalog hits but all generic (cookbook notebook, lane fold, icon tsx). "Jev" has 112 catalog hits. "Kev-4B" has 17 hits: corpus/library/kev/docs/model-cards/kev-4b.md and kev-4b-qwen3.md are already ingested, so the llama.cpp item banks on the runtime support, not the model's existence.

## Candidate list considered in pass 1 (story ids, all within 2026-09-03..10-03)

49748553 Cactus Needle 3 (236 pts, HELD) · 49923692 Clef (622) · 49943034 Kolibri tej.as (92) · 49942706 Kolibri aleph-alpha blog (52) · 49848269 Ollaya decision models (617) · 49554520 Cerebras Qwen 1500 tok/s (691) · 49911500 Weave Router (118) · 49911995 Magnitude (194) · 49859112 DeepSeek Elastic Compute (323) · 49929489 DeepSeek Harness Desktop (391) · 49742353 GitLab rate limits (177, off-domain) · 49926512 arXiv rate limit policy (145, off-domain) · 49933381 kapa.ai company-knowledge bench (26) · 49727511 Swift-Qwen3.8-27B (33) · 49713894 Pizza Bot (61) · 49881505 Vespper Docx MCP (36) · 49861047 Codex rogue $78k (82) · 49748553-alt 49897153 Gemma 4 megakernel 640 tok/s (2) · 49941824 Gufo Qwen3.6-35B-A3B Strix Halo (2) · 49911451 Halogen Qwen3.8-Flash-Next (3) · 49867202 Nemotron 3 diarization (2) · 49813524 Nemotron-H (1) · 49913428 Coop volunteer SLM (2) · 49801865 Do SLMs know what they don't know (3, not deep-read) · 49732475 SupraLabs (1) · 49858795 local Jev alternative 94% Banking77 (3, not deep-read) · 49871553 Rene-1 31B classifier (6) · 49926327 Laya free API (2) · 49767430 VisionLaya 256M (5) · 49835080 IttyBittyAI Qwen2.5:0.5B on 2017 phone (2) · 49826663 Needle 2 RPi (banked) · 49796733 XGrammar-2 (2) · 49719027 truncation-safe tool calling (2) · 49737811 tool-calling trust arXiv (1) · 49879676 Gevva0 (3) · 49878572 Jeva.cpp (3) · 49903234 Reflex Engine TTFT (1) · 49906337 + 49908997 Ollama decision models (HELD) · 49865461 System One locally (2) · 49893215 web models API (1) · 49906656 AA-AgentPerf-Local (banked) · 49926485 cua-speedrun (1) · 49838229 SWE-Serve (3) · 49874360 FAB benchmark (2) · 49889169 RuneBench (1) · 49833643 LLMs write tool workflows (2) · 49744109 Insurance Agent Benchmark (7) · 49866739 Ask HN inference (banked) · 49895933 share Claude rate limits (1) · 49800187 Relay gateway (2) · 49585787 in-process rate limits (4) · 49927572 OpenRouter vs DeepInfra ask (1, zero comments) · 49804123 OpenRouter Batch API (2) · 49846863 OpenCode $60 DeepSeek permanent (3) · 49897257/49929489 DeepSeek Harness preview (391, not deep-read).

## Door degradation log

- Algolia "requests per minute" query: nbHits 0 (honest empty).
- "free tier rate limit" query: only 3 hits, 2 off-topic; RQ2 carried by Cerebras docs + thread instead.
- Two WebFetch JSON extractions truncated their final hit line (tool calling query, agentic benchmark query); the truncated entries were dropped, never reconstructed.
- "Groq" query polluted by the Grok/Venezuela news cluster; no Groq free-tier story surfaced in-window.
- No 403s on any door this session.
