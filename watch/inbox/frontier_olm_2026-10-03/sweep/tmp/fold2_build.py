# -*- coding: utf-8 -*-
"""Round-2 fold append for watch/inbox/frontier_olm_2026-10-03/.

Appends:
  - 19 confirmed-find rows to register.jsonl (rows 24-42)
  - 4 steal rows to percolator_candidates.jsonl (rows 6-9)
  - round-2 section to DIGEST.md (after fixing stale header counts)

Run from repo root with .venv/Scripts/python.exe.
"""
import json
import os
import sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03"

SRC_OLM = "arXiv export API via curl (primary door, after WebFetch 429s) + arXiv abs pages + Hugging Face raw card/API"
SRC_FT_REDDIT = ("reddit (all four named old/www .json doors blocked: landing shell / HTTP 403 / timeouts; "
                 "deep reads via the Arctic Shift archive API door certified in lens/burns.md:107-111; "
                 "TACO verified at arxiv.org/abs/2610.02199)")
SRC_HN = ("HN door: hn.algolia.com API via curl (26 date-filtered queries, created_at_i>1788393600) "
          "+ news.ycombinator.com item threads + primaries (developers.redhat.com, api.github.com releases, "
          "tomshardware.com, vercel.com, api.featherless.ai); every fetch HTTP 200 this session, no door degradations")

REG_ROWS = [
    {
        "area": "open-and-local-language-models",
        "confidence": 1,
        "date": "2026-09-15",
        "overlap": "catalog stub only (catalog/catalog.jsonl:444218, state/arxiv/2026-09-17/2609.17848v1.txt); zero hits in the four sibling olm sweep dirs, fold register, DIGEST, and memory/ (only self-echo in memory/trajectory/steps.jsonl, which is this session's own live journal). NEW.",
        "quote": "SFT with LoRA is the strongest in-distribution method throughout the 0.6B-32B range and best in 15 out of 18 experimental settings.",
        "source": SRC_OLM,
        "title": "SFT or RL for Tool-Calling Agents? A Controlled Study Across Data, Method, and Scale",
        "url": "https://arxiv.org/abs/2609.17848",
        "why": "Controlled six-scale Qwen3 study: LoRA-SFT dominates in-distribution tool-calling (15/18) while GRPO's transfer edge averages under one point and LoRA beats full FT at preserving agentic behavior, which directly sets the model-garden finetune-lane default and the RIB_MODEL_GATES per-size priors.",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 1,
        "date": "2026-10-01",
        "overlap": "catalog stub only (catalog/catalog.jsonl:870471); zero hits in sibling sweeps, register, DIGEST, memory/. NEW.",
        "quote": "no open-weight model exceeds 42% exact-command accuracy in the unrestricted setting",
        "source": SRC_OLM,
        "title": "KaliBench: A Fine-Grained Benchmark for Cybersecurity Tool Use on Kali Linux with Runtime-Free Verifiable Rewards",
        "url": "https://arxiv.org/abs/2610.02206",
        "why": "8,504 query-command pairs over 1,642 real Kali tools with deterministic canonicalization and sandboxed verification measure that open-weight agentic CLI claims sit far below their cards, and SFT+RLVR on an 8B reaches performance comparable to a 685B MoE model, so verifiable rewards, not size, is the lever the garden should steal.",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 1,
        "date": "2026-09-30",
        "overlap": "no catalog stub; zero hits in sibling sweeps and memory/. NEW.",
        "quote": "ActionGuard intercepts each Tool Call at OpenClaw's before-tool-call stage and enforces the Reviewer's ALLOW or DENY decision under a fail-closed policy.",
        "source": SRC_OLM,
        "title": "ActionGuard: Tool Call Authorization under Poisoned Skills",
        "url": "https://arxiv.org/abs/2609.39450",
        "why": "Strangers measured the estate's own model-proposes/switchboard-authorizes pattern on the estate's own surface (OpenClaw before-tool-call stage): reviewer context separated from skill text, fail-closed enforcement, ASR/TSR over 139 contextual + 180 obvious injections with five reviewer models, directly reusable by mag/policy_engine and effect_broker.",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 1,
        "date": "2026-09-30",
        "overlap": "no catalog stub; zero hits in sibling sweeps and memory/. NEW.",
        "quote": "Together, these failures represent critical liabilities in long-horizon agentic workflows",
        "source": SRC_OLM,
        "title": "Staying on Task: Testing the Foundations of Long-Horizon Agent Reliability",
        "url": "https://arxiv.org/abs/2609.38712",
        "why": "Long-Transduction diagnostic over seven open-weight models measures a 62.8% drop scaling context 4-128K, 36.5% from input-format variation and 39.9% from local task complexity, which is the janitor ledger workload's exact failure surface and a bound any lane-runner context budget must respect.",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 1,
        "date": "2026-10-01",
        "overlap": "no catalog stub; zero hits in sibling sweeps and memory/. NEW.",
        "quote": "One epoch of GSPO on a rank-32 LoRA adapter improves pass@1 on each of the six external benchmarks we evaluated",
        "source": SRC_OLM,
        "title": "Cross-Benchmark Transfer from RL on Agentic Coding Tasks",
        "url": "https://arxiv.org/abs/2610.00890",
        "why": "One epoch of RL on a rank-32 LoRA over 1,700 hidden-test-graded tasks transfers to all six external agentic-coding benchmarks and both never-trained harnesses (SWE-Bench Pro 60.1 to 64.8, Terminal-Bench 2.1 67.4 to 82.0), and its hidden fail-to-pass + pass-to-pass grading shape is the template the estate's local-27B Q4_K_M replication should copy.",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 1,
        "date": "2026-10-01",
        "overlap": "no catalog stub; zero hits in sibling sweeps and memory/. NEW.",
        "quote": "MoE-CORE records a mean time per output token (TPOT) of 38.0-44.8 ms versus 1268.9-1269.1 ms for the evaluated vLLM Prefetch configuration on DeepSeek-V4-Flash-W4A8",
        "source": SRC_OLM,
        "title": "MoE-CORE: Coordinated Expert Offloading and Residency for Memory-Constrained MoE Inference",
        "url": "https://arxiv.org/abs/2610.01950",
        "why": "Measured expert-offloading serving under a device-memory cap (TPOT 38.0-44.8 ms vs 1268.9-1269.1 ms for vLLM Prefetch; 21.5 ms at an 84-GB NPU cap with substitution+MTP), banked as genre intel for memory-constrained MoE janitors even though its appliance class is not RX 5600 XT class.",
    },
    {
        "area": "finetuning-and-adaptation via reddit",
        "confidence": 1,
        "date": "2026-09-19",
        "overlap": "ft_overlap.py single-pass scan (catalog.jsonl + 453,074 memory files): id catalog=0, memory only trajectory/steps.jsonl own-session echo; 'bonsai' catalog hits are shadertoy false friends. NEW.",
        "quote": "Across the complete suite, Qwen finished 3.02\u00d7 faster and used 3.10\u00d7 fewer output tokens.",
        "source": SRC_FT_REDDIT,
        "title": "I tested Qwen3.8 27B IQ3_XXS (10.18GiB) vs Bonsai Ternary PQ2 (6.42GiB)",
        "url": "https://www.reddit.com/r/LocalLLaMA/comments/1wkorli/",
        "why": "source-fetched: 2026-10-03 - the measured LoRA-quant baseline the RQ1 asks for: same-hardware agent A/B where ternary Bonsai PQ2 finished the same 4 tasks with 84,176 vs 27,197 output tokens and 24:09 vs 8:00 wall time, so a ternary janitor lane pays ~3x token inflation even when task scores hold; direct yardstick against TACO-successor headline claims (TACO itself, arXiv 2610.02199 verified from its abstract, is an optimizer-state method needing an 80GB H100 for 30-32B, not a 6GB-card path).",
    },
    {
        "area": "finetuning-and-adaptation via reddit",
        "confidence": 1,
        "date": "2026-09-18",
        "overlap": "id catalog=0, memory only trajectory echo. NEW.",
        "quote": "reaches 52.8 and 60.8, respectively, compared with 69.7 and 80.6 for Qwen3.5-27B, retaining roughly three quarters of the full-precision performance on both benchmarks.",
        "source": SRC_FT_REDDIT,
        "title": "bonsai's document reveal how much cherry picked their headlines are",
        "url": "https://www.reddit.com/r/LocalLLaMA/comments/1wjnklv/",
        "why": "source-fetched: 2026-10-03 - the ternary successor's own whitepaper numbers (Terminal-Bench 2.1 / SWE-bench Verified, page 7 of the PrismML whitepaper) contradict its 98.2 percent-intelligence headline at roughly three quarters retained: the exact perplexity-vs-measured-baseline trap RQ1 names, and the same phantom-number failure shape our citation-lint law exists for; planning figure for any ternary lane should be ~75 percent agentic, not 98.",
    },
    {
        "area": "finetuning-and-adaptation via reddit",
        "confidence": 1,
        "date": "2026-09-15",
        "overlap": "id catalog=0, memory only trajectory echo. NEW.",
        "quote": "Non unanimous cases went from 2 of 21 to 6 of 21 depending on which run you look at.",
        "source": SRC_FT_REDDIT,
        "title": "I applied Dan Luu's \"what's wrong with this benchmark?\" reading to my own two LLM judges. Five exercises.",
        "url": "https://www.reddit.com/r/LLMDevs/comments/1wgvfpr/",
        "why": "source-fetched: 2026-10-03 - the variance half of the imagined-grader defense (burns.md:91-93 banked the consensus half): 16 identical replicate runs moved non-unanimous cases 2/21 to 6/21 (a single run samples, not measures, the noise floor), a fixed threshold rule went deaf as the suite grew 17 to 144 cases (one case worth 5.9 points at 17, 0.7 at 144, real regression stops reaching threshold with zero code changed), and one reviewed prompt edit dropped recall 0.80 to 0.50 - adopt median-of-N judge runs and growth-aware thresholds in judge2/duel before any self-training loop fires.",
    },
    {
        "area": "finetuning-and-adaptation via reddit",
        "confidence": 1,
        "date": "2026-09-12",
        "overlap": "id catalog=0, memory only trajectory echo. NEW.",
        "quote": "The agent can change prompts, tool handling, retries, or other pieces of its setup, then run against the same independent evaluation.",
        "source": SRC_FT_REDDIT,
        "title": "Letting an agent rewrite its own harness while keeping the grader separate",
        "url": "https://www.reddit.com/r/LLMDevs/comments/1wefk8o/",
        "why": "source-fetched: 2026-10-03 - the pre-fire gate spec for any estate self-training loop, with the comment thread supplying the checklist: grader completely outside the rewrite loop, held-out slice the proposer never sees feedback from, edit budget so a one-line prompt change and a tool-policy rewrite are not scored as the same win, pinned model endpoint and tool versions so a backend change is not credited to the candidate, mechanical evaluator wherever expressible, provenance (run id, task revision, tool trace) on failure reports, shadow stage before publication - maps one-to-one onto the percolator's promotion gate.",
    },
    {
        "area": "finetuning-and-adaptation via reddit",
        "confidence": 1,
        "date": "2026-09-08",
        "overlap": "id catalog=0, memory trajectory only; the olm fold already flags 'OUI-1 4B generative-UI claim UNVERIFIED' (burns.md:112) - this item is the team's own measured primary thread. NEW with context.",
        "quote": "Training on a single component library improved structural validity from 13% to 28.8%, but generation slowed from 1.6s to 4.3s.",
        "source": SRC_FT_REDDIT,
        "title": "I'm fine-tuning a Open Weight model for Generative UI. SFT slowed it down; self-training fixed it.",
        "url": "https://www.reddit.com/r/LLMDevs/comments/1wavhij/",
        "why": "source-fetched: 2026-10-03 - measured proof the percolator's shape (deterministic accept gate + judge check + human-gated promotion) can outrank weight finetuning: ~700 synthetic SFT examples made benchmark performance worse while loss dropped, then the parser-accepted defect-repair self-training loop lifted structural validity 13 to 57.1 percent while generation time fell back from 4.3s to 1.9s, and 71.7 percent across 27 libraries - also the OpenUI team's own numbers against the fold's OUI-1 UNVERIFIED flag.",
    },
    {
        "area": "finetuning-and-adaptation via reddit",
        "confidence": 1,
        "date": "2026-09-05",
        "overlap": "id catalog=0, memory trajectory only; 'mql5' echoes 18 operator biography PDFs (domain already personal to the operator, makes it more relevant, not a duplicate). NEW.",
        "quote": "clean domain data moves a 14B from useless to within five points of frontier in one epoch.",
        "source": SRC_FT_REDDIT,
        "title": "One epoch of domain fine-tuning took Qwen2.5-Coder-14B from 1% to 92% compile success on MQL5. gpt-5.6-sol got 97% on the same items. Benchmark is public.",
        "url": "https://www.reddit.com/r/LocalLLM/comments/1w7umnd/",
        "why": "source-fetched: 2026-10-03 - the corpus gate that lets SFT win at all: 11 months of generated specs with EVERY completion machine-verified through the real MQL5 compiler and backtest, one epoch 1.09 to 92.39 percent compile success vs 97.28 for gpt-5.6-sol (McNemar p=2.29e-49), the whole train+eval loop on one AMD R9700 under ROCm with no NVIDIA anywhere, and the poster conceding in-distribution scope - the template for converting seat tapes only where a mechanical verifier exists, and the AMD-training datapoint the RX-class RQ1 asks about.",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 0.97,
        "date": "2026-09-06",
        "overlap": "zero in catalog, memory/, fold register and DIGEST; present only in today's superseded 11:05 same-lane file (item 1 there, replaced by this sweep); substring noise in 09-28 _raw reddit JSON. NEW post-purge.",
        "quote": "built for on-device, local deployment, and resource-constrained scenarios, reaching 2B-class open-source SOTA",
        "source": SRC_OLM,
        "title": "MiniCPM5-2B model card (OpenBMB)",
        "url": "https://huggingface.co/OpenBMB/MiniCPM5-2B",
        "why": "The window's cleanest Q1 answer: dense 2,516,756,480-param Apache-2.0 model (HF API verified: createdAt 2026-09-06, lastModified 2026-09-29) with tool-calling/on-device tags, a measured card table (avg 53.9, beating listed larger models) and SGLang named the tool-calling backend, though scores are self-reported so any fleet swap stays OWED a third-party run.",
    },
    {
        "area": "quantization-and-compression",
        "confidence": 0.97,
        "date": "2026-09-30",
        "overlap": "grep \"Quantization-aware Reasoning Behavior Analysis\" and id 2609.39801: 0 hits across catalog/, memory/, watch/inbox/, docs/, state/ (own _raw scratch excluded); genuinely new.",
        "quote": "when applied to reasoning models, PTQ not only degrades reasoning performance but also exacerbates overthinking, leading to longer reasoning trajectories",
        "source": "arxiv",
        "title": "RATIO: Reasoning Analysis and Token-level Inference Optimization for Quantized Reasoning Models",
        "url": "https://arxiv.org/abs/2609.39801",
        "why": "Directly extends the banked 2-bit output-token inflation finding (burns.md:103-106): I read its Table 1 showing W3 inflates CoT length 2.94x (GPTQ) to 3.77x (AWQ) on Qwen-1.5B while accuracy falls 60.13 to 33.82, plus a training-free token-penalty fix the janitor fleet could test.",
    },
    {
        "area": "quantization-and-compression",
        "confidence": 0.97,
        "date": "2026-09-03",
        "overlap": "catalog grep -c 0; estate holds a pointer only (watch/inbox/frontier_olm_2026-10-03/lens/burns.md:106 \"GatedDeltaNet NVFP4 W4A4 2609.04098 (r23)\" plus an incidental mention in memory/runs/compaction_eval/steps_frozen_20260920.jsonl); no prior catalog row or full-text read, so the deep read is new value.",
        "quote": "Minima matches BF16 within seed noise (5-task average \u22120.52) while being the smallest (17.5 GiB) and fastest-prefill (+14\u201319%) of the recipes we compare",
        "source": "arxiv",
        "title": "Why Gated DeltaNet Survives 4-Bit Quantization: NVFP4 W4A4 for the Recurrent Half of a Hybrid 27B LLM",
        "url": "https://arxiv.org/abs/2609.04098",
        "why": "RQ4 anchor read end to end: full W4A4 including GDN gates matches BF16, calibrated FP8 KV scales recover 83% of long-context KV penalty for free, and kernel-fused global-scale mismatch is a serving landmine no GGUF metadata records.",
    },
    {
        "area": "agent-memory-and-continuity",
        "confidence": 0.97,
        "date": "2026-10-01",
        "overlap": "grep+rg: \"transcripts are precious\" and \"quesma.com/blog/agent-session\" = 0 hits in catalog.jsonl, memory/, watch/inbox/; quesma domain known only via the 09-28 quant lane's different article (qwen38-27b quant bench, register). Genuinely new primary.",
        "quote": "They are proof of work for the tokens you paid for, and lessons you will pay to relearn.",
        "source": "hn",
        "title": "Agent session transcripts are precious, keep them",
        "url": "https://quesma.com/blog/agent-session-transcripts-are-precious/",
        "why": "RQ2/RQ5 counterparty that completes the re-derivability law: the raw transcript stays the archived leaf layer (re-derivation wins in context, deletion loses the receipts); banked numbers include Claude Code's default 30-day transcript deletion, 91 pct vs 43 pct task resolution with/without an AGENTS.md change, and Anthropic's 200,000-transcript analysis.",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 0.95,
        "date": "2026-09-29",
        "overlap": "/v1/systemone + nimble/tev1 already a percolator candidate (memory/percolator/candidates.jsonl:10); NEW here: v0.35.1's Clef/Clef Flash multimodal, web-search cap 3-to-10, CAPABILITY declarations, and the measured estate gap (estate 0.34.3 by ollama --version this session vs 0.35.1 upstream).",
        "quote": "Ollama now supports decision models through /v1/systemone, based on TypeSafe's Jev API.",
        "source": SRC_HN,
        "title": "Ollama v0.35.0 and v0.35.1 release notes (GitHub releases API)",
        "url": "https://github.com/ollama/ollama/releases/tag/v0.35.1",
        "why": "RQ5 primary text: the owed upgrade adds the /v1/systemone decision endpoint (Nimble, Tev1, then Clef 27B / Clef Flash 9B multimodal), raises web search 3-to-10 per response, and adds CAPABILITY declarations; the notes name NO change to the ordinary generate path the gemma janitors ride, and their own example shows output_tokens: 1 (release-note number, not an estate measurement; the A/B at burns.md:203 stays owed).",
    },
    {
        "area": "open-and-local-language-models",
        "confidence": 0.95,
        "date": "2026-10-03",
        "overlap": "Instrument design and the 09-27/09-28 intervals are held (watch/inbox/BURN_free-resource-landscape_20260927_h.md:20-24 and 20260928_g.md:9, total_items 50641); NEW: this 5-day 51112-vs-50641 delta, the Gensyn-Swarm flood share, and the absent rate-limit headers.",
        "quote": "\"total_items\": 51112, \"total_pages\": 512",
        "source": SRC_HN,
        "title": "Featherless /v1/models roster, live interval fired this session (total_items 51112, +471 over the 09-28 receipt)",
        "url": "https://api.featherless.ai/v1/models?sort=-created_at&page=1&per_page=100",
        "why": "RQ3 live check (I ran it, HTTP 200 keyless, 0.83-0.92 s, JSON saved to tmp/hnolm/featherless_roster_100.json): roster-diff food still flows, +471 models in 5 days vs the 09-28 receipt (50641), 44 of the 100 newest rows are Gensyn-Swarm 0.5-0.6B fine-tunes, pre-registered falsifier untriggered, and no rate-limit headers present so the rate limit stays unmeasured; lane stays recon-only.",
    },
    {
        "area": "quantization-and-compression",
        "confidence": 0.95,
        "date": "2026-09-29",
        "overlap": "grep \"STEPQuant\": 0 hits across catalog/, memory/, watch/inbox/, docs/, state/; catalog id count 0; new.",
        "quote": "the FP32 state pool of Qwen exceeds the memory footprint of its BF16 weights at 70 supported concurrent requests",
        "source": "arxiv",
        "title": "STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization",
        "url": "https://arxiv.org/abs/2609.38169",
        "why": "Names the real serving bottleneck for hybrid linear-attention models under concurrency (state pool, not weights) and shows 6-bit state matches FP32-state accuracy with >5x state compression and up to 68.7% total serving-memory cut in SGLang.",
    },
]

PERC_ROWS = [
    {
        "area": "open-and-local-language-models",
        "claim": ("For open and local model levers the measured order is task-matched adaptation first (LoRA-SFT best in-distribution "
                  "tool-calling in 15 of 18 settings across 0.6B-32B), verifiable rewards second (no open-weight model above 42 percent "
                  "exact-command accuracy; SFT+RLVR lifts an 8B to 685B-MoE parity), parameter count last; port a KaliBench-shape "
                  "canonicalized command scorer into the janitor loop and route every verdict to record_verdict, CI-gated with mandatory "
                  "Wilson intervals."),
        "source_url": ("https://arxiv.org/abs/2610.02206 | https://arxiv.org/abs/2609.17848 | https://arxiv.org/abs/2610.00890 | "
                       "https://arxiv.org/abs/2609.38712 | https://arxiv.org/abs/2609.39450 | https://arxiv.org/abs/2610.01950 | "
                       "https://huggingface.co/OpenBMB/MiniCPM5-2B | https://github.com/ollama/ollama/releases/tag/v0.35.1 | "
                       "https://api.featherless.ai/v1/models?sort=-created_at&page=1&per_page=100"),
        "estate_map": ("Organs: gopher fleet janitor lane (mag/ollama_policy.py:16 pins MAG_JANITOR_MODEL gemma:2b; mag/lanes.py:44-48 pins "
                       "clerk/router gemma:2b, worker/biographer gemma4:latest); authorize seam mag/policy_engine.py:6-19 plus "
                       "mag/effect_broker.py:1-11 (ActionGuard port: reviewer context separated from skill text, fail-closed "
                       "before-tool-call DENY, verdict banked in the broker receipt chain); the verdict ledger tools/gps_mcp/ledger.py:270 "
                       "record_verdict keyed (model_id, task_shape) with the evidence-resolution gate at :291 (amended organ per critique "
                       "fix 4: probe and grader scores route here, and policy_engine gate 2 reads its aggregates); percolator "
                       "(mag/percolator.py:14-17; the Ollama 0.35 candidate already filed at memory/percolator/candidates.jsonl:10); "
                       "quantizer weights side (mag/auto_quantize.py:1-24 is analytics-resolution only; real weight-quant surface is "
                       "tools/llamacpp/llama-quantize.exe plus mag/gguf_cartography.py); model-gates rib "
                       "(memory/rib/RIB_MODEL_GATES_20261001.md:1-11) for the per-size LoRA-SFT default row and the context-cliff priors. "
                       "Concrete port move: stand up the KaliBench-shape canonicalized command scorer inside the janitor loop, route every "
                       "score to record_verdict, and make candidate swaps clear ledger aggregates before touching configs/lanes.yaml; the "
                       "MiniCPM5-2B swap stays behind the 09-11 UNPROVEN gate (watch/inbox/STEAL_FOLD_RESEARCH_PIPELINE_20260911.md:67-70, "
                       "memory/runs/gapwave/_owed_live_all.json:936) plus the loadability OWED (safetensors-to-GGUF or vetting the community "
                       "localellm/WebGPU-minicpm5-2b-i1-gguf derivative, plus an ollama 0.34.3 architecture-support check); MoE-CORE stays "
                       "genre intel (the host is a 6GB RX 5600 XT, mag/ollama_policy.py:1, and the paper's own comparison caps mismatch at "
                       "1K vs 128 tokens)."),
        "probe": ("KaliBench-shape janitor grading run, $0, proposed and not run. Harvest (goal, exact shell command) pairs from this "
                  "seat's documented session work (memory/trajectory/steps.jsonl is the journal; the card's Checks section is a seed set), "
                  "canonicalize both sides with a deterministic alias-aware matcher (lowercase, flag-order and whitespace insensitive), "
                  "score gemma:2b and gemma4:latest via /api/generate at temperature 0, n at least 30 with a difficulty control (10 or more "
                  "pairs rephrased into unfamiliar phrasing or drawn from an unworked domain, to price the self-harvest in-distribution "
                  "bias). Statistics gate (round 1's 'either outcome is decision-grade' retracted): the 95 percent binomial half-width at "
                  "n=30 and p=0.42 is about 18 points, so Wilson intervals are mandatory in the result; retire-the-ceiling-as-routing-prior "
                  "fires only when the interval lower bound clears 42 percent (roughly 60 percent observed at n=30); adopt-verifier-as-"
                  "garden-gate fires only when the upper bound sits below 42 percent (roughly 25 percent or below); anything between is "
                  "UNDECIDED pending larger n (about a 10-point half-width at n=100). Every verdict routes to "
                  "tools/gps_mcp/ledger.py:270 record_verdict keyed (model_id, task_shape) so repeats accumulate a running pass-rate "
                  "instead of overwriting."),
        "steal_card": "watch/inbox/frontier_olm_2026-10-03/steal/open-and-local-language-models-arxiv-hf.md",
    },
    {
        "area": "quantization-and-compression",
        "claim": ("Quantization damage surfaces as behavior (overthinking token inflation: W3 CoT 2.94-3.77x on a 1.5B reasoning model) "
                  "and as serving state (the FP32 recurrent-state pool exceeds BF16 weights at 70-way concurrency; 6-bit state matches "
                  "FP32-state accuracy) before it surfaces as a weights-side score drop; never import an llm-compressor/NVFP4 checkpoint "
                  "into the GGUF tier without the fused global-scale rewrite, and budget the state pool as a water-graph ceiling row."),
        "source_url": "https://arxiv.org/abs/2609.39801 | https://arxiv.org/abs/2609.38169 | https://arxiv.org/html/2609.04098v1",
        "estate_map": ("Organs: gopher fleet local tier (deepseek-r1:1.5b on box; roles pinned at configs/lanes.yaml:31-37 on the 6 GB / "
                       "CONTEXT=8k envelope of :28-30), quantizer (weights side now real: tools/llamacpp/llama-quantize.exe landed 09-23; "
                       "mag/gguf_cartography.py:1-24 is the GGUF parser; analytics side mag/auto_quantize.py laws :22-24 untouched), water "
                       "graph (mag/water_graph.py:1-49 flow-physics engine; fracture at sustained full bore :26-34 makes a state-pool "
                       "ceiling row native), kv slot pilot (tools/kv_slot_pilot.md:56-57 already serves q8_0 KV; :3 STAGED now stale), "
                       "percolator intake (the quant law sits UNPROMOTED in memory/percolator/candidates.jsonl rows 15/16, grep-verified "
                       "this round). Concrete port moves: (1) extend the owed Q4-vs-Q8 A/B with thinking-token + output-length + "
                       "empty-content channels on the deepseek-r1 arms and, on confirmation, patch the janitor runner sampler with a "
                       "TSPD-style per-token penalty table; (2) standing law on the weights side: no llm-compressor/NVFP4 import into the "
                       "GGUF tier without the fused global-scale rewrite, enforced by a gguf_cartography provenance census; (3) state-pool "
                       "ceiling row in the serving ledger from blob metadata, measured by a --parallel 1/2/4/8 ramp on the pilot's own "
                       "launch line (kv_slot_pilot.md:54-58)."),
        "probe": ("Reasoning-quant ladder, $0 compute plus one 1.9 GB pull, one afternoon: deepseek-r1:1.5b (ON BOX, Q4_K_M, 1.8B "
                  "parameters, thinking-capable; ollama show this round) vs deepseek-r1:1.5b-qwen-distill-q8_0 (library-verified 1.9 GB "
                  "this round; no bare 1.5b-q8_0 tag exists; digest check at pull time), fp16 3.6 GB rung as tiebreaker. 20 fixed prompts "
                  "(10 decode-heavy reasoning, 10 short controls), temperature 0, identical caps; log per response done_reason, eval_count, "
                  "eval_duration, thinking-token count (between think tags), correctness against a fixed key, and the empty-content flag "
                  "(sibling sweep digest :38 channel). STOPPING RULE (sweep-1 card round-2 fix 1, git 2206f2354): token counts compare "
                  "only on EOS-terminated responses or cap >= 512 both arms; speed ratio eval_duration/eval_count is valid under any cap. "
                  "Predictions: (1) Q4_K_M median thinking tokens >= 1.15x q8_0 on finished reasoning tasks (RATIO direction; the "
                  "2.94x-3.77x magnitudes live at W3, so expect nearer the 1.25x quesma class); (2) correctness co-moves down on Q4; (3) "
                  "length-cap and empty-content finishes concentrate in Q4. Falsifier: all three channels flat within 10 pct, which banks "
                  "as a below-4-bit boundary condition and routes the follow-up to a llama-quantize.exe W3 rung (on disk since 09-23). "
                  "Executing also mints the q8_0 arm owed since "
                  "watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:69."),
        "steal_card": "watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.md",
    },
    {
        "area": "agent-memory-and-continuity",
        "claim": ("The vendor session store reaps on a roughly 30-day horizon (146 sessions older than 30 days at the 2026-10-04 census "
                  "read, oldest 2026-08-25), so the thought-bank continuity exporter is P0: finish the incremental mode=ro exporter, extend "
                  "it to text parts and session/message tables sized against the text-scope stock, run an own full-text redaction pass, and "
                  "register exports in the catalog FTS surface; a weekly retention census on the vendor store gates the P1/P2 call."),
        "source_url": "https://quesma.com/blog/agent-session-transcripts-are-precious/",
        "estate_map": ("Unchanged from the round-2 approved-shape card: context pack + boot recap as primary consumer (AGENTS.md:51 "
                       "min-token pack; memory/zknot/LATEST.md at tools/zknot.py:11), the thought-bank continuity exporter as the mechanism "
                       "base (mag/thought_bank_app.py:3-11,26-27,57 incremental mode=ro exporter, dedup on part_id, lapsed since its "
                       "2026-09-30T11:52:39.054529 last write re-measured by stat this round; DB-path/mode=ro/redact origin credited to "
                       "mag/knot_at_close.py:17-18,37,39 per tools/zknot.py:21-22), the corrected gopher-fleet corpus organ claim "
                       "(code-agent-data SKILL.md:9-12 names estate-side sources only; the wall threatens only the vendor-DB feed the skill "
                       "never names), water graph secondary (proof-of-work receipts), sovereign mirror (docs/DNA.md:23 presented layer). "
                       "Port move: resume the reasoning harvest, extend to text parts + session/message tables sized at 364,932,976 bytes "
                       "text-scope stock vs the 3.5 GB live DB (whole-file mirror rejected), full-text redaction pass specced "
                       "(mind_window.py:51-62 patterns were only exercised on ~150-char first lines), register exports in "
                       "catalog/catalog.jsonl for the FTS surface (AGENTS.md:116)."),
        "probe": ("Unchanged: weekly retention census on the vendor store, $0, pinned instrument SQL_PIN = select count(*) from session "
                  "where time_updated < ? (d30 = now_ms - 30*86400*1000, mode=ro; time_created companion banked). Reference read "
                  "2026-10-04: 5,634 sessions, 146 over 30d by time_updated - now stable across the critic's third read (146 again), 210 "
                  "by time_created on my read and 212 on the critic's later read, oldest 2026-08-25T11:01:35.177Z to the millisecond on "
                  "every read. P1 (store reaps ~30d horizon): the time_updated count shrinks weekly and the oldest advances, making the "
                  "exporter P0. P2 (no reaper, floor = profile age): counts hold or grow; exporter still banks at background priority. "
                  "Owner: MagCensusPatrolDaily surface (scripts/census_patrol_daily.ps1:3-4 ride-along precedent; registers via "
                  "scripts/register_census_patrol_task.ps1, logs to logs/census_patrol.log); cadence: weekly, day-of-week-gated, alerting "
                  "only on a shrink of the time_updated count or an advance of the oldest timestamp. Implementation OWED; hand-run weekly "
                  "until it lands."),
        "steal_card": "watch/inbox/frontier_olm_2026-10-03/steal/agent-memory-and-continuity.md",
    },
    {
        "area": "finetuning-and-adaptation via reddit",
        "claim": ("Gate every self-training and finetuning ambition on the measured hierarchy: judge noise floor first (16 identical "
                  "replicates moved non-unanimous judge cases from 2/21 to 6/21; a fixed threshold went deaf as the suite grew), grader "
                  "outside the rewrite loop, weights only where a mechanical verifier exists (machine-verified MQL5 corpus: one epoch 1.09 "
                  "to 92.39 percent compile, all-AMD ROCm), promotion loops beat weights elsewhere (OpenUI: SFT made the benchmark worse, "
                  "self-training 13 to 57.1 percent), and any ternary lane carries the measured tax (about 75 percent agentic retention, "
                  "about 3x output tokens), never the vendor headline."),
        "source_url": "https://www.reddit.com/r/LLMDevs/comments/1wavhij/",
        "estate_map": ("Percolator is the keystone: mag/percolator.py:25/:90-91/:508 (alpha-budget promote gate, auto-promotion forbidden, "
                       "ingest_candidates :544) absorbs the 1wefk8o checklist (held-out slice, edit budget, pinned endpoints, provenance "
                       "fields, shadow stage) and 1wavhij is measured proof its promote-loop shape outranks weight finetuning on "
                       "non-verifiable lanes (13% to 57.1% to 71.7% structural validity, generation 4.3s back to 1.9s); weights fire only "
                       "where a mechanical verifier exists per 1w7umnd (seat tapes through the real compiler, 1.09% to 92.39% in one epoch, "
                       "McNemar p=2.29e-49, all-AMD ROCm). Gopher fleet grading instruments get the noise-floor port: "
                       "tools/overmind_judge.py:168/:224 and tools/duel_harness.py:263 are single-pass today (zero median/replicate logic, "
                       "grep = 0 this session), so median-of-N and growth-aware thresholds wire in before any self-training loop. "
                       "Quantizer + water graph carry the ternary tax: any low-bit janitor lane budgets 3x output tokens and ~75% agentic "
                       "retention from the 1wkorli same-hardware A/B (27,197 vs 84,176 tokens, 8:00 vs 24:09), cap set via "
                       "mag/water_graph.py:145 add_pipe with :93 fracture_threshold as the burn alarm. Context pack / citation-lint treats "
                       "vendor headlines as PHANTOM-NUMBER candidates (tools/citation_lint.py:23, :117): 1wjnklv's 98.2% headline "
                       "contradicted by its own whitepaper page 7 is the founding fixture, filed as a percolator candidate via "
                       "mag/percolator.py:213. Sovereign mirror (configs/mirrors.json) takes the OUI-1 primary numbers from 1wavhij to move "
                       "the burns.md:112 UNVERIFIED flag."),
        "probe": ("Judge replicate noise-floor census on the estate's own duel instruments: take the 20 most recent judged pairs "
                  "tools/overmind_judge.py:114 build_pairs already assembles, re-fire the same judge model and prompt 2 extra times per "
                  "pair with nothing changed (judge_kimi :168 or judge_deepseek :224), parse with tools/duel_harness.py:263 parse_judge, "
                  "count winner flips. Pre-registered: (a) 2+ of 20 pairs flip, the 1wgvfpr noise floor transfers (16 replicates moved "
                  "non-unanimous cases 2/21 to 6/21 there) and median-of-N wires into the duel path before any self-training loop; (b) 0-1 "
                  "flips, the floor is refuted at this tier, the port drops to a one-line reminder and self-training proceeds on "
                  "deterministic gates only; (c) fewer than 20 re-judgeable pairs, instrument-inconclusive, pairs built first, probe "
                  "re-runs next window. Cost: about 40 judge calls on the sensing lane, roughly an hour. A clean 20-for-20 unanimity "
                  "falsifies the transfer and is itself bankable."),
        "steal_card": "watch/inbox/frontier_olm_2026-10-03/steal/finetuning-and-adaptation via reddit.md",
    },
]

DIGEST2 = """
---

## Round 2 fold (2026-10-04 night seat; appends the 17:07 round-1 fold above)

The mine's second same-day pass: all 32 lanes re-ran their doors and appended their round-2 banks to the same sweep/ files (every round-1 section preserved verbatim above its round-2 section), a fresh confirmation pass resolved 24 candidates to 19 confirmed finds plus 5 held with evidence, and 4 steal cards landed (three round-2/3 refinements of round-1 areas plus one new olm arxiv+hf card). This section is the round-2 fold of that mine. The register grew in place from 23 to 42 rows (rows 24-42 below; row 38 deep-reads the same paper as round-1 row 23 and its overlap field states the upgrade). Percolator candidates grew from 5 to 9 rows (rows 6-9). Steal cards grew from 5 to 9. Provenance boundary, unchanged from round 1: this seat verified on-disk facts itself (byte walk, JSONL parse, dash scan, cross-checks of lane-claimed byte counts, gate-registry grep; commands in RECEIPT.md's round-2 section) and carried all sweep, confirmation, and steal-card claims from the run's outputs, cited to their bank files; this seat did not re-fetch remote URLs and did not re-run the confirmation pass's fetches.

### Executive summary (round 2)

1. **The adaptation hierarchy is measured end to end.** LoRA-SFT is the in-distribution tool-calling default across the 0.6B-32B range, best in 15 of 18 settings, with GRPO's transfer edge under one point and LoRA beating full FT at preserving agentic behavior (register row 24, arxiv.org/abs/2609.17848). One epoch of GSPO on a rank-32 LoRA over 1,700 hidden-test-graded tasks transfers to all six external agentic-coding benchmarks and both never-trained harnesses (register row 28, arxiv.org/abs/2610.00890). On non-verifiable lanes promotion loops beat weight finetuning: about 700 synthetic SFT examples made the OpenUI benchmark worse while loss dropped, then parser-accepted defect-repair self-training lifted structural validity from 13 to 57.1 percent (register row 34). Weights win only where a mechanical verifier exists: an MQL5 corpus with every completion machine-verified went 1.09 to 92.39 percent compile success in one epoch, all-AMD ROCm (register row 35).

2. **Verifiable rewards, not parameter count, is the capability lever.** KaliBench's 8,504 query-command pairs over 1,642 real Kali tools with deterministic canonicalization and sandboxed verification found no open-weight model above 42 percent exact-command accuracy unrestricted, while SFT+RLVR on an 8B reached performance comparable to a 685B MoE (register row 25). The bound on the same fleet shape is context: a 62.8 percent drop scaling 4-128K, 36.5 percent from input-format variation, and 39.9 percent from local task complexity across seven open-weight models (register row 27).

3. **Quantization damage arrives as behavior and as serving state before it arrives as scores.** W3 inflates chain-of-thought length 2.94x (GPTQ) to 3.77x (AWQ) on a 1.5B reasoning model while accuracy falls from 60.13 to 33.82, and a training-free token penalty is the mitigation shape (register row 37). The Minima deep read upgrades round-1 row 23: full W4A4 including the GDN gates matches BF16 within seed noise, calibrated FP8 KV scales recover 83 percent of the long-context KV penalty for free, and kernel-fused global-scale mismatch is a serving landmine no GGUF metadata records (register row 38). STEPQuant names the real serving bottleneck under concurrency: the FP32 recurrent-state pool exceeds the BF16 weights at 70 concurrent requests, and 6-bit state matches FP32-state accuracy at over 5x compression with up to 68.7 percent total serving-memory cut (register row 42).

4. **The 6 GB reality check closed.** No post-2026-10-02 release at janitor VRAM class ships measured agentic capability in its card; the measured class exemplar remains the gemma-4-E4B QAT q4_0 GGUF (lane-banked: sweep/open-and-local-language-models-x.round2.md). Ternary lanes carry a measured tax, not the vendor headline: a size-matched IQ3_XXS quant finished the same four agent tasks 3.02x faster with 3.10x fewer output tokens than the ternary build (register row 30), and the ternary vendor's own whitepaper contradicts its 98.2 percent headline at roughly three quarters retained (register row 31).

5. **The Ollama 0.35.1 upgrade stays held, now with a failed confirmation.** The release-noted half is confirmed: decision models through /v1/systemone, CAPABILITY declarations, web search raised 3 to 10 per response (register row 40). The measured half (a 3.2x janitor decode regression on the estate's own RX 5600 XT) failed page confirmation: the claimed quote is not on the cited release page and the numbers are estate-side, so the claim is held out of the register and a clean re-measure is owed (unconfirmed item 1 below).

6. **The decision-model layer arrived upstream while the estate stays on 0.34.3.** llama.cpp merged /v1/systemone decision-model serving into llama-server itself (lane-banked: sweep/inference-efficiency-x.md); an independent Jev research report measured MMLU-Pro 82.7 percent for about $0.28 total with a roughly 4x order-of-options primacy bias any routing use must randomize against (lane-banked: sweep/open-and-local-language-models-reddit.md); Gevva0 shows single-prefill logit-scored routing works on stock Gemma 26B while janitor-class E2B/E4B hit a hard wall (lane-banked: sweep/inference-efficiency-reddit.md). Free-class: LLM7 remains the one measured free lane and its live roster still reads 64 models (the claimed churn to 68 was contradicted on re-fetch; unconfirmed item 3); the Featherless roster is alive and growing (register row 41) and the claimed five-day halving failed its re-run (unconfirmed item 2).

7. **Continuity's exporter went from nice-to-have to P0.** The vendor session store reaps on a roughly 30-day horizon (146 sessions older than 30 days at the card's census read; steal/agent-memory-and-continuity.md), and the transcript-as-leaf law got its counterparty primary: raw transcripts are proof of work, deletion loses the receipts, 91 vs 43 percent task resolution with and without an AGENTS.md change (register row 39). External warning shot banked lane-side: eleven of twelve real memory-system pairings failed to beat memory-off while execution-verified experience injection helped on all five solvers (sweep/agent-memory-and-continuity-arxiv.md).

8. **Swarm governance moved from anecdote to protocol, and the estate's own trails still cannot answer the redo-vs-resume census.** Reserve-before-dispatch budget conservation with terminal-evidence settlement and epoch fencing, a release budget that caps committed-but-unfinished work so the first 429 is a HOLD signal, and the recast of multi-agent debate as an ensemble-sampling effect that budget-matched self-consistency matches or beats are all lane-banked this pass (sweep/swarm-orchestration-arxiv.md). Private-evidence quoting is the measured brake on shared-board false-belief cascades, and the rogue-spend thread names the missing spend admission control (sweep/swarm-orchestration-hn.md). Two independent estate censuses found zero quota or limit kill rows in any lane trail, so the redo-vs-resume fraction is unmeasurable until a death-event writer exists (sweep/swarm-orchestration-hn.md, sweep/swarm-orchestration-reddit.md).

9. **Judge instruments acquired their measurement discipline.** Common-mode error is not identifiable from internal ensemble scores alone, so no same-family judge panel can certify its own shared blindness, and pinned temp-zero judges still flip about 5 percent of items with far higher flip rates on close calls (lane-banked: sweep/evals-and-self-improvement-arxiv.md). An activation-probe pre-filter cuts LLM-monitor cost 90 percent at about one point of precision (lane-banked: sweep/evals-and-self-improvement-hn.md). The estate-side noise-floor probe is now specified in percolator row 9: 20 judged pairs re-fired twice each, flip census, pre-registered branches.

10. **Estate telemetry split found and priced.** The burns LEDGER is silent since 2026-09-28 while the hermes usage ledger logged 1,275 rows over three days with 888 of the newest day's rows carrying a doubled-key flag; two lanes' verdict: telemetry break, not a spend stop (sweep/inference-efficiency-hn.md, sweep/inference-efficiency-x.md). Per-dispatch tank accounting stays owed and must count requests, not headers: both hot free doors expose zero rate-limit headers (sweep/open-and-local-language-models-x.round2.md).

**Door health, round 2** (per-lane receipts in each bank file): the Arctic Shift archive API is the certified working reddit engine, re-certified independently by four lanes this pass; every direct reddit door stayed blocked; X discovery degraded all pass (stripped status URLs, 1302 and 429 storms) with fxtwitter resolution alive wherever a status ID existed; arXiv export API clean in every lane that used it; WebSearch rate-limited intermittently across lanes. One new working reddit variant this pass: thread permalinks via their .rss endpoints (sweep/kv-cache-and-context-engineering-reddit.md).

### Top steals (round 2; full cards under steal/)

### 6. KaliBench-shape janitor grading with CI-gated verdicts
- **Steal:** open and local model levers are measured, not vendor-claimed, in the order task-matched adaptation first, verifiable rewards second, parameter count last; stand up a canonicalized command scorer inside the janitor loop and route every score to the verdict ledger keyed by model and task shape so repeats accumulate a running pass rate instead of overwriting; the MiniCPM5-2B swap stays behind the 2026-09-11 UNPROVEN gate plus a loadability check.
- **Estate map (organs; the card carries the line-anchored map):** janitor lane pins in mag/ollama_policy.py and mag/lanes.py; the authorize seam mag/policy_engine.py plus mag/effect_broker.py takes the ActionGuard port shape (reviewer context separated from skill text, fail-closed before-tool-call DENY); the verdict ledger tools/gps_mcp/ledger.py record_verdict is where probe and grader scores route and whose aggregates gate candidate swaps before configs/lanes.yaml changes; percolator intake and the model-gates rib carry the per-size LoRA-SFT default row and the context-cliff priors.
- **Probe:** KaliBench-shape janitor grading run, $0, proposed and not run: harvest goal-plus-exact-command pairs from documented session work, canonicalize both sides with a deterministic alias-aware matcher, score gemma:2b and gemma4:latest at temperature 0 with n at least 30 and a difficulty control; Wilson intervals mandatory in the result; retire-the-ceiling and adopt-verifier branches pre-registered on interval bounds.
- **Card:** steal/open-and-local-language-models-arxiv-hf.md, JSON mirror beside it

### 7. Quant damage is behavior and state before it is scores (round-3 card)
- **Steal:** quantization damage surfaces as behavior (overthinking token inflation) and as state (the recurrent/KV pool under concurrency) before it surfaces as a weights-side score drop; the owed Q4-vs-Q8 A/B gains thinking-token, output-length, and empty-content channels; no llm-compressor or NVFP4 import into the GGUF tier without the fused global-scale rewrite, enforced by a GGUF provenance census; the state pool gets a water-graph ceiling row.
- **Estate map (organs; the card carries the line-anchored map):** gopher fleet local tier on the 6 GB envelope (configs/lanes.yaml roles); the quantizer's weights side is now real (llama-quantize binary landed 2026-09-23; mag/gguf_cartography.py parses containers; mag/auto_quantize.py stays analytics-only); the water graph (mag/water_graph.py) takes the state-pool ceiling row natively via its fracture threshold; the kv slot pilot (tools/kv_slot_pilot.md) serves q8_0 KV and is unblocked by the landed llama.cpp binaries; percolator intake already holds the quant law unpromoted in memory/percolator/candidates.jsonl.
- **Probe:** reasoning-quant ladder, $0 compute plus one 1.9 GB pull, one afternoon: deepseek-r1:1.5b (Q4_K_M, thinking-capable, on box) vs the library qwen-distill q8_0 rung, fp16 tiebreaker; 20 fixed prompts, temperature 0, identical caps; log done_reason, eval_count, thinking-token count, correctness, and the empty-content flag; stopping rule and falsifiers pre-registered in the card.
- **Card:** steal/quantization-and-compression.md, steering-gate JSON beside it

### 8. The continuity exporter is P0 (round-3 card)
- **Steal:** the vendor session store reaps on a roughly 30-day horizon, so the thought-bank continuity exporter is the only durable copy of estate session history and lands at background priority either way; resume the reasoning harvest, extend to text parts and session/message tables, run an own full-text redaction pass, and register exports in the catalog FTS surface.
- **Estate map (organs; the card carries the line-anchored map):** context pack and boot recap are the primary consumers (AGENTS.md min-token pack; memory/zknot/LATEST.md); mag/thought_bank_app.py incremental mode=ro exporter is the mechanism base with dedup on part_id; DB-path, mode=ro, and redact origin credited to mag/knot_at_close.py per tools/zknot.py; register exports feed catalog/catalog.jsonl for the corpus FTS surface; water graph secondary (proof-of-work receipts); sovereign mirror docs/DNA.md presented layer.
- **Probe:** weekly retention census on the vendor store, $0, pinned instrument SQL count of sessions older than the 30-day horizon, mode=ro; reference read already taken (146 sessions over 30 days, stable across three reads); P1 if the count shrinks weekly with the oldest advancing, P2 if counts hold; owner is the MagCensusPatrolDaily surface, implementation owed, hand-run weekly until it lands.
- **Card:** steal/agent-memory-and-continuity.md, JSON mirror beside it

### 9. The measured hierarchy gates every self-training and finetuning ambition
- **Steal:** judge noise floor first, grader outside the rewrite loop, weights only where a mechanical verifier exists, promotion loops beat weights elsewhere, ternary lanes carry the measured tax (about 75 percent agentic retention, about 3x output tokens), never the vendor headline.
- **Estate map (organs; the card carries the line-anchored map):** the percolator is the keystone (mag/percolator.py alpha-budget promote gate, auto-promotion forbidden, ingest_candidates); the gopher fleet grading instruments tools/overmind_judge.py and tools/duel_harness.py are single-pass today, so median-of-N and growth-aware thresholds wire in before any self-training loop; quantizer and water graph carry the ternary tax as a lane budget with the fracture threshold as the burn alarm; citation lint treats vendor headlines as PHANTOM-NUMBER candidates (the ternary 98.2 percent headline contradicted by its own whitepaper is the founding fixture); configs/mirrors.json takes the OUI-1 primary numbers to move the burns UNVERIFIED flag.
- **Probe:** judge replicate noise-floor census on the estate's own duel instruments: the 20 most recent judged pairs re-fired twice each with nothing changed, parsed with the duel parser, winner flips counted; pre-registered branches (2 or more flips: the noise floor transfers and median-of-N wires into the duel path; 0-1 flips: refuted at this tier; fewer than 20 re-judgeable pairs: instrument-inconclusive, rebuild pairs first). About 40 judge calls on the sensing lane, roughly an hour.
- **Card:** steal/finetuning-and-adaptation via reddit.md

### Confirmed finds, round 2 (19; register rows 24-42)

| # | title | url | date | area |
|---|-------|-----|------|------|
| 24 | SFT or RL for Tool-Calling Agents? A Controlled Study Across Data, Method, and Scale | https://arxiv.org/abs/2609.17848 | 2026-09-15 | open-and-local-language-models |
| 25 | KaliBench: A Fine-Grained Benchmark for Cybersecurity Tool Use on Kali Linux with Runtime-Free Verifiable Rewards | https://arxiv.org/abs/2610.02206 | 2026-10-01 | open-and-local-language-models |
| 26 | ActionGuard: Tool Call Authorization under Poisoned Skills | https://arxiv.org/abs/2609.39450 | 2026-09-30 | open-and-local-language-models |
| 27 | Staying on Task: Testing the Foundations of Long-Horizon Agent Reliability | https://arxiv.org/abs/2609.38712 | 2026-09-30 | open-and-local-language-models |
| 28 | Cross-Benchmark Transfer from RL on Agentic Coding Tasks | https://arxiv.org/abs/2610.00890 | 2026-10-01 | open-and-local-language-models |
| 29 | MoE-CORE: Coordinated Expert Offloading and Residency for Memory-Constrained MoE Inference | https://arxiv.org/abs/2610.01950 | 2026-10-01 | open-and-local-language-models |
| 30 | I tested Qwen3.8 27B IQ3_XXS (10.18GiB) vs Bonsai Ternary PQ2 (6.42GiB) | https://www.reddit.com/r/LocalLLaMA/comments/1wkorli/ | 2026-09-19 | finetuning-and-adaptation via reddit |
| 31 | bonsai's document reveal how much cherry picked their headlines are | https://www.reddit.com/r/LocalLLaMA/comments/1wjnklv/ | 2026-09-18 | finetuning-and-adaptation via reddit |
| 32 | I applied Dan Luu's "what's wrong with this benchmark?" reading to my own two LLM judges. Five exercises. | https://www.reddit.com/r/LLMDevs/comments/1wgvfpr/ | 2026-09-15 | finetuning-and-adaptation via reddit |
| 33 | Letting an agent rewrite its own harness while keeping the grader separate | https://www.reddit.com/r/LLMDevs/comments/1wefk8o/ | 2026-09-12 | finetuning-and-adaptation via reddit |
| 34 | I'm fine-tuning a Open Weight model for Generative UI. SFT slowed it down; self-training fixed it. | https://www.reddit.com/r/LLMDevs/comments/1wavhij/ | 2026-09-08 | finetuning-and-adaptation via reddit |
| 35 | One epoch of domain fine-tuning took Qwen2.5-Coder-14B from 1% to 92% compile success on MQL5. gpt-5.6-sol got 97% on the same items. Benchmark is public. | https://www.reddit.com/r/LocalLLM/comments/1w7umnd/ | 2026-09-05 | finetuning-and-adaptation via reddit |
| 36 | MiniCPM5-2B model card (OpenBMB) | https://huggingface.co/OpenBMB/MiniCPM5-2B | 2026-09-06 | open-and-local-language-models |
| 37 | RATIO: Reasoning Analysis and Token-level Inference Optimization for Quantized Reasoning Models | https://arxiv.org/abs/2609.39801 | 2026-09-30 | quantization-and-compression |
| 38 | Why Gated DeltaNet Survives 4-Bit Quantization: NVFP4 W4A4 for the Recurrent Half of a Hybrid 27B LLM | https://arxiv.org/abs/2609.04098 | 2026-09-03 | quantization-and-compression |
| 39 | Agent session transcripts are precious, keep them | https://quesma.com/blog/agent-session-transcripts-are-precious/ | 2026-10-01 | agent-memory-and-continuity |
| 40 | Ollama v0.35.0 and v0.35.1 release notes (GitHub releases API) | https://github.com/ollama/ollama/releases/tag/v0.35.1 | 2026-09-29 | open-and-local-language-models |
| 41 | Featherless /v1/models roster, live interval fired this session (total_items 51112, +471 over the 09-28 receipt) | https://api.featherless.ai/v1/models?sort=-created_at&page=1&per_page=100 | 2026-10-03 | open-and-local-language-models |
| 42 | STEPQuant: When and Where Errors Matter in Delta-Rule Recurrent State Quantization | https://arxiv.org/abs/2609.38169 | 2026-09-29 | quantization-and-compression |

Row-38 note: same paper as round-1 row 23, which cites the html URL form; row 38 banks the deep-read upgrade at the abs URL and its overlap field states the relationship. All 19 rows are inside the run's 2026-09-03..2026-10-03 fetch window. Full per-row fields (source, quote, why, overlap, confidence) live in register.jsonl rows 24-42.

### Honest gaps (round 2)

Stated by the round-2 lanes, carried here; each cites its bank file.

1. The local qwen2.5:7b Q4_K_M-vs-q8_0 A/B is still unrun after four lanes re-owed it this pass; the instrument is now fully specified (pin or reset serving-cache state per arxiv.org/abs/2609.04748, thinking-token and finish-reason and empty-content channels, paired seeds, token counts compared only on EOS-terminated responses or equal caps) (sweep/quantization-and-compression-arxiv.md, sweep/quantization-and-compression-hn.md, sweep/quantization-and-compression-reddit.md, sweep/quantization-and-compression-x.md).
2. The estate-side 27B Q4_K_M replication is hardware-blocked by arithmetic: the banked community run of the same result class peaked in the 22,934 MiB range on a 24 GB card against this estate's 6 GB RX 5600 XT; the designed alternative is the 7B A/B (sweep/open-and-local-language-models-hn.md, sweep/open-and-local-language-models-reddit.md).
3. Per-dispatch tank accounting was not run; its passive-header variant is refuted by measurement, since both hot free doors expose zero rate-limit headers, so the probe must count requests (sweep/open-and-local-language-models-x.round2.md, sweep/inference-efficiency-hn.md).
4. The redo-vs-resume census does not replicate on the estate corpus because no subagent-granularity death ledger exists; two independent censuses over the lane trails this pass found zero quota or limit kill rows (tallies taken at different moments over different lane sets: one read 7,492 trail rows with 748 strict-429 rows and 26 fatal, the other read CYCLE 3,119, MONITOR 2,852, CYCLE_FAIL 735, HEARTBEAT 605); answering it needs a death-event writer (attempt count plus redone, resumed, or salvaged disposition) (sweep/swarm-orchestration-hn.md, sweep/swarm-orchestration-reddit.md).
5. The literal after-2026-10-02 arXiv sub-window read empty at fetch time on both runs (announcement lag); a re-query is owed inside 48 hours (sweep/open-and-local-language-models-arxiv.md).
6. The medium.com fact-retirement post (HN 49877124) stayed behind a 403 plus Cloudflare wall for a second same-day seat; open read debt (sweep/agent-memory-and-continuity-hn.md).
7. Waggle (arxiv.org/abs/2609.34136) is banked at abstract level only and flagged; a full-text read is owed before any port (sweep/swarm-orchestration-arxiv.md).
8. No measurement of empty-reasoning rate by quant level exists anywhere in the window; only the owed A/B, instrumented through mag/inference_budget.py, can answer it (sweep/quantization-and-compression-hn.md).
9. The Ollama adapter swap-cost question is moot on 0.35 and later (adapter support removed, bisected by the finetuning x lane); the janitor path becomes merge-offline plus merged-GGUF swap, and a measured swap cost is owed only if a version gets pinned (sweep/finetuning-and-adaptation-hn.md, sweep/finetuning-and-adaptation-x.md).
10. The 0.35.1 upgrade decision stays HELD pending a clean re-measure with the x lane's A/B protocol (portable 0.35.1 from the shared blob store, primary re-verified as control, server killed by recorded PID afterward) (sweep/open-and-local-language-models-x.round2.md).
11. Clef Flash 9B weight and license remain UNVERIFIED (sweep/open-and-local-language-models-reddit.md).
12. The Featherless roster-diff instrument needs a size and hash stability check per pull: the round-2 full-dump reading did not survive its own re-run three hours later (unconfirmed item 2 below) (sweep/open-and-local-language-models-x.round2.md).
13. The MiniCPM5-2B fleet swap stays behind the 2026-09-11 UNPROVEN gate, owes a loadability check (safetensors-to-GGUF), and its card scores are self-reported (steal/open-and-local-language-models-arxiv-hf.md).
14. Warm-boot defects reported this pass, not fixed: the boot brief pointer still targets the brief frozen 2026-09-26, warm state carries no residual or leaf pointers, and a tokens-to-competence instrument for warm boot is owed (sweep/agent-memory-and-continuity-x.md).
15. Lens mirror: the evening lens covers round-1 rows only; mirroring register rows 24-42 into lens/burns.md is owed to the lens owner (this fold deliberately touched only the four fold files).

### Unconfirmed (round 2): held out of the register, with confirmation evidence

**1. Ollama 0.35.1 regresses gemma janitor serving 3.2x on the estate's RX 5600 XT (sweep/open-and-local-language-models-x.round2.md; candidate URL github.com/ollama/ollama/releases/tag/v0.35.1).**

- Confirmation evidence: the page is live (v0.35.1, published 2026-09-29, verified twice via WebFetch and the GitHub releases API). The claimed quote ("llama-server GPU discovery watchdog timed out") appears nowhere on the page; no throughput, gemma, or RX content exists in the release notes; the release-note-gains sub-claims (Clef and Clef Flash via /v1/systemone, CAPABILITY declarations) are verbatim-supported.
- Disposition: not registered. The decode numbers are estate-side measurements, unverified at this URL and cited to the wrong URL if they came from a server log; the upgrade stays HELD and a clean re-measure is owed (gap 10).

**2. Featherless served roster halved in five days (sweep/open-and-local-language-models-x.round2.md; candidate URL api.featherless.ai/v1/models).**

- Confirmation evidence: the quote is byte-confirmed (the dump's first row matches verbatim). But a re-run of the same keyless GET about three hours later read 22,122 data rows byte-identical across three refetches, not the claimed 10,175, and the sorted arm read 22,113 rows with a total of 51,141, not 4,023; the ledger citations at memory/burns/LEDGER.jsonl lines 683 and 692 verify (22,054 and 22,059 on 09-28), making the roster continuous with its measured growth rather than halved. The claimant's numbers are consistent with truncated downloads at the 00:14Z fetch moment (labeled inference in the evidence).
- Disposition: central assertions falsified by re-run of the named instrument; not registered. The paged-arm live-interval item (register row 41) stands; the instrument needs the size-and-hash stability check (gap 12). The no-rate-limit-headers and no-new-provider legs confirmed.

**3. LLM7 roster churned 64 to 68 models (sweep/open-and-local-language-models-x.round2.md; candidate URL api.llm7.io/v1/models).**

- Confirmation evidence: page live; quote near-equivalent except a drifted created epoch field between snapshots; the live roster parses to 64 models, matching six prior byte-backed estate receipts, so the claimed plus-four churn is contradicted; zero rate-limit headers confirmed on both the models and chat-completions doors; a free-usable set of four models still exists on the roster.
- Disposition: header-absence leg confirmed and folded into the round-2 tank-accounting note; the churn claim contradicted; not registered.

**4. TTPO: label-free test-time training via majority-vote disagreement (sweep/finetuning-and-adaptation-reddit.md; candidate URL reddit.com/r/LLMDevs/comments/1wgxzvw/).**

- Confirmation evidence: the live page was unreachable from the confirmation environment (every fetch route blocked, no archive snapshot). An independent archive (api.pullpush.io) holds the full post with the claimed numbers sentence verbatim, the asymmetry rationale, the stated boundary (competition math and verifiable code only), and the ablation question; the thread's single comment defers the ablation. Two caveats: the claim's "never summarisation/drafting" hardens the poster's hedged phrasing, and the underlying arXiv paper was not fetched in the confirmation pass.
- Disposition: substance archive-confirmed, but the page standard (seeing the quote on the page itself) was not met; not registered. The lane's own bank stands as lane-banked evidence.

**5. OUI-1 Apache-to-Gemma license-flip quote (sweep/finetuning-and-adaptation-reddit.md; candidate URL reddit.com/r/LocalLLaMA/comments/1wcqa03/).**

- Confirmation evidence: live Reddit blocked; the pullpush archive supports the DiffusionGemma-unsupported-by-llama.cpp portions and the community GGUF path verbatim, but the claimed license-flip quote appears nowhere in the 17 recovered thread comments, and no comment in the recovered thread discusses licensing at all; an exact-phrase web search found no match.
- Disposition: not registered; the license-gate lesson survives through the finetuning x lane's independent license verification via the GitHub API, but this specific quote and its community-catching narrative are unconfirmed.

### Round-2 probe order (proposal; the fold does not authorize)

1. Judge noise-floor census (percolator row 9): about 40 sensing-lane judge calls, under an hour, and its outcome gates any self-training loop.
2. Reasoning-quant ladder (percolator row 7): $0 plus one 1.9 GB pull on the operator's box, one afternoon; also mints the q8_0 arm owed since the 09-30 round's steal card.
3. KaliBench-shape janitor grading (percolator row 6): $0 on the operator's box, Wilson-gated.
4. Continuity exporter census (percolator row 8): weekly ride-along on the existing census patrol surface until the exporter lands.

Round 1's five probes (fold recommendation above) stand unchanged; the round-2 lanes re-owed round-1 probe 3's tank accounting and probe 5's A/B without firing them.
"""

HEADER_EDITS = [
    ("This file is the run-level fold. What lives beside it:",
     "This file is the run-level fold. A round 2 fold (second same-day passes across all 32 lanes, 19 further confirmed finds as register rows 24-42, 4 further steal cards) was appended below by the 2026-10-04 night seat; see the Round 2 fold section. What lives beside it:"),
    ("- `steal/` - the 5 full steal cards plus the quant card's steering-gate JSON",
     "- `steal/` - 9 full steal cards (5 from round 1, 4 from round 2) plus the quant card's steering-gate JSON"),
    ("- `register.jsonl` - 23 confirmed finds, one row each (area, source, title, url, date, quote, why, overlap, confidence)",
     "- `register.jsonl` - 42 confirmed finds, one row each (area, source, title, url, date, quote, why, overlap, confidence); rows 1-23 are the round-1 fold, rows 24-42 the round-2 append"),
    ("- `percolator_candidates.jsonl` - 5 rows, one per steal (claim, source_url, estate_map, probe), ready for percolator review",
     "- `percolator_candidates.jsonl` - 9 rows, one per steal (claim, source_url, estate_map, probe), ready for percolator review; rows 1-5 round 1, rows 6-9 round 2"),
]


def append_jsonl(path, rows):
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")


def validate_jsonl(path, expected_rows, required_fields):
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if l.strip()]
    assert len(lines) == expected_rows, "%s: %d rows, expected %d" % (path, len(lines), expected_rows)
    parsed = [json.loads(l) for l in lines]
    for i, row in enumerate(parsed, 1):
        missing = [k for k in required_fields if k not in row]
        assert not missing, "%s row %d missing %s" % (path, i, missing)
    return parsed


def main():
    reg_path = os.path.join(ROOT, "register.jsonl")
    per_path = os.path.join(ROOT, "percolator_candidates.jsonl")
    dig_path = os.path.join(ROOT, "DIGEST.md")

    # --- register append
    with open(reg_path, encoding="utf-8") as f:
        before = len([l for l in f if l.strip()])
    append_jsonl(reg_path, REG_ROWS)
    reg = validate_jsonl(reg_path, before + len(REG_ROWS),
                         ["area", "confidence", "date", "overlap", "quote", "source", "title", "url", "why"])
    print("register rows now:", len(reg))

    # --- percolator append
    with open(per_path, encoding="utf-8") as f:
        before_p = len([l for l in f if l.strip()])
    append_jsonl(per_path, PERC_ROWS)
    per = validate_jsonl(per_path, before_p + len(PERC_ROWS),
                         ["area", "claim", "estate_map", "probe", "source_url", "steal_card"])
    print("percolator rows now:", len(per))

    # --- area counts over the appended register rows
    from collections import Counter
    new_rows = reg[len(reg) - len(REG_ROWS):]
    areas = Counter(r["area"] for r in new_rows)
    print("appended area counts:", dict(areas), "sum:", sum(areas.values()))

    # --- DIGEST header fixes + append
    with open(dig_path, encoding="utf-8") as f:
        text = f.read()
    for old, new in HEADER_EDITS:
        count = text.count(old)
        assert count == 1, "header edit target found %d times: %r" % (count, old[:60])
        text = text.replace(old, new)
    if not text.endswith("\n"):
        text += "\n"
    text += DIGEST2
    with open(dig_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("DIGEST.md bytes now:", os.path.getsize(dig_path))
    print("register.jsonl bytes now:", os.path.getsize(reg_path))
    print("percolator_candidates.jsonl bytes now:", os.path.getsize(per_path))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
