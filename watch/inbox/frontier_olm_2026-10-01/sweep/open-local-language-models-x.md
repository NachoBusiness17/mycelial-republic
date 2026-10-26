# sweep: open-local-language-models via x (2026-10-01)

source-fetched: 2026-10-01
(Window: last 30 days, 2026-09-01..2026-10-01. Run by subagent sweep-open-local-language-models-x
on the Mag Resource Harness seat. Dedupe baseline: `frontier_olm_20260928/register.jsonl` (21 rows),
`frontier_olm_2026-09-30/sweep/` (45 files), and root `watch/inbox/x_intel_drop_20261001.md`
(LiteLLM LENS, model-mating, Ghidra, the NachoQuixotic rap) - none re-banked below.)

## Door status (honest)

- WebSearch `site:x.com`: 9 queries fired. Intermittent Z.ai backend 429s (`MCP error -429 code 1302`)
  hit 4 of them on first attempts; all recovered on the search tool's internal retry EXCEPT the
  first Qwen query, which 429'd all three attempts and returned zero links (degraded). Two queries
  returned no usable signal (Gemma September release; refusal-vs-runtime) - recorded as no-signal,
  not as finds. All other queries returned resolvable status URLs.
- fxtwitter door (`https://api.fxtwitter.com/<user>/status/<id>`): 4/4 resolved this session
  (ollama, AntLingAGI, FeitengLi, bnjmn_marie), JSON with verbatim text + timestamps. No 403s.
  Continuity with `lens/doors.md:49-56` (jack/status/20 probe, code 200).
- HN Algolia: 5 fetches clean (search_by_date on llama.cpp, ollama, vllm, refusal + items/49831201).
  One lesson: an `OR` query string is NOT supported the way I wrote it (`vllm OR MLX OR refusal`
  returned fuzzy noise); single-term queries are the working shape.
- arXiv export API: 1 Atom probe clean (`all:"ollama" OR all:"llama.cpp"`, 10 newest of 156 hits).
- Reddit door: NOT probed (blocked per `lens/doors.md:40-47`; not needed for this lane).

## Pass 1 - candidates considered (34, last 30 days; HELD = already in estate holdings, not re-banked)

1. @ollama 2105152056382345544 - Jev-like decision models locally (09-30). DEEP-READ (fx).
2. ollama.com/blog "now supports Jev-style decision models" (09-29). DEEP-READ.
3. HN 49908997 / 49906337 - same story wave (09-30). Snippet.
4. arXiv 2609.26693 - Measuring the Serving Stack (09-22). DEEP-READ (abs + own raw snapshot).
5. blog.madhukaraphatak.in - Dynamic Abliteration via Engram Steering (09-24). DEEP-READ.
6. HN 49831201 - the abliteration thread, 108 pts / 42 comments (09-24). DEEP-READ (items API).
7. huggingface.co/blog/transformers-llama-cpp-quants (09-22, dup HN 49812339/49799125). DEEP-READ.
8. blog.mozilla.ai - Benchmarking Local LLM Servers (09-17, HN 49742415). DEEP-READ.
9. @AntLingAGI 2105335205741596911 - Ling-3.1-flash announcement (09-30). DEEP-READ (fx).
10. @sudoingX 2105372110252319004 - Ling 124B to 560B jump comment. Snippet.
11. @ItsmeAjayKV 2105344855279034756 - "welcome October" Ling post. Snippet.
12. @ItsmeAjayKV 2104526519444066308 - October wave previews (DSv4.1-pro, GLM-5.4). Snippet.
13. @JulianGoldieSEO 2105297085084188837 - GLM 5.4/5.5 Flash/K4 LEAK LIST - RUMOR ONLY, unverified.
14. @FeitengLi 2097609675361710366 - Qwen3.8-27B GGUF 2.96/2.48 bpw (09-09). DEEP-READ (fx).
15. @Alibaba_Qwen - new Qwen3.8-27B GGUFs, "10% higher accuracy" Unsloth Dynamic V3. Snippet.
16. @Oluwaphilemon1 2097502970745090556 - Qwen3.8-27B GGUF #1 most-liked, 10M dl / 24 days. Snippet.
17. @UnslothAI 2093397494889890050 - GLM-5.3 local 2-bit Dynamic GGUF, 256GB class (held-adjacent:
    GLM-5.3-Flash rung is an estate holding; the 2-bit local GGUF fact is snippet-only here). Snippet.
18. @TeksEdge 2098807855822606692 - Qwen3.5-9B post-trained review. Snippet.
19. @TeksEdge 2093927202488455498 - Qwen3.5-4B CPU-only pull-and-run. Snippet.
20. @OrcaRouter 2098040763514794131 - agentic post-train on Qwen3.5-35B-A3B, GGUF on HF. Snippet.
21. @bnjmn_marie 2029227800574447958 - Qwen3.5 27B GGUF eval. DEEP-READ (fx), then EXCLUDED:
    created_at 2026-03-04, out of window.
22. @nutlope - "trained Tev1 0.8B, a tiny Jev-like classifier... running completely locally on my
    mac with @ollama" (profile-page link only, no status ID resolved). Snippet, DEGRADED.
23. @ollama 2098218702210777541 - Ollama 0.34, Codex app can use Ollama models (09-10). Snippet.
24. @ollama 2098892877388714179 - Amp BYOK routing to Ollama cloud (09-12). Snippet.
25. @ollama 2098290160035373524 / 2098235674793242770 - DSv4.1-Flash cloud rollout. HELD
    (09-28 register rows 7 + probe card).
26. HN 49911995 - Magnitude (YC S25) self-optimizing inference engine, 178 pts (09-30). Snippet.
27. HN 49859982 - Faster prompt lookup drafting in llama.cpp, 89 pts (09-26). Snippet.
28. HN 49921148 - InferPilot, vLLM doctor for fp8 (10-01). Snippet.
29. HN 49921077 - "How much do open-weight LLMs memorize specific books?" (10-01). Snippet.
30. HN 49919953 - Jev-powered LLM guardrail (10-01); HN 49908382 - Jev agent orchestration (09-30).
    Snippets (the Jev ecosystem wave around item 2).
31. HN 49878572 - jeva.cpp, llama.cpp fork with JEV-compatible API (09-28). Snippet.
32. arXiv 2609.29757 - OllamaDrama honeypot (09-24). Abstract via Atom probe.
33. arXiv 2609.18526 - Illusion of Local Privacy (09-16). Abstract via Atom probe. DEEP-READ-class
    abstract only; full text NOT fetched (stated).
34. arXiv also surfaced, not deep-read: 2609.35465 Tetra 2.7bpw (HELD raw snapshot, catalog:671313),
    2609.26333 Disaggregated Quantization (Qwen3.8-27B GGUF, 1.78x TTFT llama.cpp), 2609.39358
    Galahad KV-state cache, 2609.39223 QATFactory, 2609.35882 GenomeOcean WebGPU, 2609.18120
    PentestChain (Ollama qwen2.5-7b first rung).

## Pass 2 - deep reads actually executed (10 fetches; bar was 5)

1. arXiv abs 2609.26693 + the estate's own raw snapshot `state/arxiv/2026-09-23/2609.26693v1.txt`
   (read locally; verbatim abstract at :6). REALM @ EMNLP 2026 accepted; 9 pages.
2. blog.madhukaraphatak.in non-destructive-refusal-suppression (full): Qwen3-4B PoC, hidden 2560,
   36 layers; hooks at layers 12/14/16/18/20; sigmoid context gate + O(1) 4-table n-gram hash +
   per-layer projection heads; 2,000 PKU-SafeRLHF samples, loss 3.92 to 1.77 in 250 steps (~9 min
   on an A100); single-layer (L14) steering FAILED, multi-layer needed; 3 hard-refusal prompts
   flipped qualitatively; NO benchmark numbers; HF transformers only, Ollama never mentioned.
3. HN items/49831201 (full comment read): top critiques - baseline "should compute the projected
   vector and subtract only that" (goldemerald, citing the single-direction refusal paper);
   sandbox-not-weights governance thread (javcasas, tomjen3); fiduciary-duty thread (jchw);
   NO runtime-vs-runtime comparisons anywhere in the thread.
4. ollama.com/blog Jev-style decision models (full, 09-29): nimble "open-source 9B parameter
   decision model developed by Bespoke Labs"; tev1 experimental 4B + tev1:0.8b from Together AI;
   Ollama 0.35 `GET localhost:11434/v1/systemone`; question types choice/noul/score with
   probabilities + confidence; Nimble 91ms/decision on an M5 Max; use cases named: ticket triage,
   model routing, content or safety moderation; roadmap: MLX-backed Apple Silicon speedups.
5. huggingface.co/blog/transformers-llama-cpp-quants (full, 09-22): GGUF via `from_pretrained`
   through ggml Metal kernels (`kernels` lib); all standard quants loadable, Q4_K_M recommended;
   `transformers serve repo:file.gguf` OpenAI-compatible; M2 Max benchmark "close to llama.cpp
   across all three checkpoints" with the caveat that transformers measured prefill included vs
   llama-bench decode-only; packed path MPS-only; coverage: Qwen3.5 dense + MoE and compatible
   Qwen3.8 checkpoints; example uses unsloth/Qwen3.5-4B-GGUF Q4_K_M.
6. fxtwitter ollama/status/2105152056382345544 (09-30T04:25Z, 637,230 views, 4,397 likes):
   verbatim text captured; video demo of Nimble "playing Ollama racer" through /v1/systemone.
7. fxtwitter AntLingAGI/status/2105335205741596911 (09-30T16:33Z, 734,816 views): verbatim text
   captured; 1,673 Elo GDPVal-AA v2.1, 75.16 FrontierSWE, 65.35 HealthBench Professional;
   weights "soon" (not yet open).
8. fxtwitter FeitengLi/status/2097609675361710366 (09-09T08:54Z): Qwen3.8-27B GGUFs at 2.96/2.48
   bpw = 9.71/8.20 GiB, MTP included, "achieved 100% on AIME 2026" claim; slimmed vision encoder,
   Q4_K at 314.46 MiB ("64.59% smaller than BF16"), 0.99537 cosine to FP32 vision outputs,
   "no modifications to llama.cpp required".
9. fxtwitter bnjmn_marie/status/2029227800574447958: resolved but EXCLUDED (2026-03-04, out of
   window). Content recorded anyway: UD-Q4_K_L/IQ4_XS/IQ4_NL close to original, UD-IQ3_XXS "good
   enough", no good Q2 found; 9B results similar. Useful prior, not a bank item.
10. blog.mozilla.ai benchmarking (full, 09-17): exp-llama-benchy, 15 runs/point, M4 Max 64GB +
    Xeon/L40S + Steam Deck OLED; Qwen 0.8B/9B/27B, identical GGUFs; all four servers within a few
    percent PP; "biggest speedups came from configuration, not the choice of engine"; shader
    toolchain +63.3% PP on 9B (Deck); llamafile CUDA graphs +16.8% decode on 0.8B; Ollama MLX
    self-enables speculative decode, optimal draft flips by platform (2 on Metal, 4 on CUDA);
    host overhead per token ~0.4ms Mac / 1.8ms L40S / 5.4ms Deck; TTFT explicitly NOT measured.

## Answers to the four research questions

### RQ1 - credible upgrade over gemma:2b / gemma4 for janitor duty at 8B or below

The headline: the estate's janitor slots finally have a PURPOSE-BUILT candidate class. Ollama 0.35
(09-29/09-30) ships Jev-style decision models locally: nimble (9B, Bespoke Labs, "open-source"),
tev1 (4B) and tev1:0.8b (Together AI, experimental), served on /v1/systemone with typed
choice/score/noul questions returning probabilities. Their named use cases (ticket triage, model
routing, content or safety moderation) are literally the scut lane's job description, and 91ms per
local decision on an M5 Max is a latency class gemma:2b-as-chat cannot reach for typed decisions.
Caveats: nimble's specific license is NOT named in the post (only "open-source" - license pull is
OWED); tev1 is "experimental". Second candidate: Qwen3.5-4B (HF blog's own example model,
unsloth/Qwen3.5-4B-GGUF Q4_K_M) now runs under BOTH llama.cpp and transformers. Third: the
decision-model ecosystem wave (jeva.cpp fork, Jev guardrail, Jev agent orchestration, nutlope's
self-trained Tev1 0.8B) shows the shape is replicable. Qwen3.8-27B is the strongest "short-worker
upgrade" if the hardware class is 8-10GiB VRAM (FeitengLi's 8.20GiB at 2.48bpw), but it is over
the 8B cap. Llama line: NO new release in-window (Llama 4 is April 2026; its community license is
not OSI-approved and caps 700M-MAU companies - X article 2099280270637531222). Gemma line: no
September/October X-visible release (search returned noise; Gemma 4 Apache-2.0 of 04-02 remains
the held baseline). DeepSeek line: V4.1-Flash HELD; previews of DSv4.1-pro / GLM-5.4 are
RUMOR-grade (JulianGoldieSEO leak list, unverified). Ling-3.1-flash (09-30, ~560B/25B active,
weights "soon") is the flagship wave, not janitor-class.

### RQ2 - measured refusal/censorship differences across runtimes (C1 E1-E3 extension)

Two direct hits, both new to holdings:
1. arXiv 2609.26693 (09-22, REALM@EMNLP 2026): measured, not folklore - in Ollama "the default
   tools= request is gated per model by a static template flag" and Phi-3 and Gemma-3 "are
   rejected before inference"; rejection/retry-exhaustion not preserved as structured metadata
   makes harnesses report 0% fidelity; cross-stack probes (Ollama, llama.cpp, vLLM, SGLang) give
   different results for identical requests; constrained decoding removes parse failures but can
   induce NON-TERMINATION; turn-pooled vs per-instance estimates differ up to ~55 points. This is
   the published, peer-reviewed version of the fork C1 re-derived in window 1: the runtime is part
   of the measured behavior. E1-E3 should cite it and steal its checklist (treat serving behavior
   as part of the evaluation protocol).
2. Dynamic Abliteration (09-24, HN 108 pts): refusal SUPPRESSION on janitor-class Qwen3-4B via
   runtime residual-stream hooks (transformers forward hooks, weights frozen, layers 12-20).
   Corroborates the C1 fork from the other side: hook-class interventions live in the transformers
   path; Ollama's serving surface exposes no such injection point (the window-1 memlance lesson),
   so the same checkpoint IS a different censorship object depending on runtime. Also method
   evidence for E1-E3 design: single-layer steering failed (L14), multi-layer needed; community
   critique (goldemerald) says the baseline should subtract only the projected refusal direction.
   No Ollama arm exists in either source - that arm is still the estate's own experiment to run.

### RQ3 - local inference stack changes, last 60 days

Four stack-level movements: (1) Ollama 0.35 adds the /v1/systemone decision-model endpoint
(above); Ollama 0.34 (09-10) made the Codex desktop app able to ride Ollama models; Amp BYOK
routing to Ollama cloud landed 09-12. (2) transformers learned to run llama.cpp GGUF quants
natively (09-22, MPS-only packed path, Qwen3.5/3.8 coverage) - the runtime boundary between the
estate's two serving paths is now porous, which doubles as an E1-E3 instrument (same GGUF bytes,
two runtimes). (3) Mozilla's controlled benchmark (09-17) found no engine winner and tens-of-
percent swings from configuration (shader toolchain, speculative-draft depth, compiler flags):
the estate's janitor lane should tune config before swapping engines. (4) Security surface:
OllamaDrama honeypot (2609.29757, 09-24) logged 290,887 interactions from 2,793 IPs against
exposed Ollama-style endpoints (model enumeration, SSRF/RCE probes, crypto-mining), and the
Illusion-of-Local-Privacy paper (2609.18526, 09-16) documents a llama.cpp authorization flaw
(one authenticated client restoring another tenant's conversation, 200/200 trials) plus prompts
recoverable from residual runtime memory. The estate's Ollama binds locally today; both papers
are the reason to keep it that way and to register the exposure check as a law.

### RQ4 - day-0 GGUF/quant builds and per-quant footprints

- Qwen3.8-27B: day-0 community GGUFs with MTP included - 2.96bpw = 9.71GiB, 2.48bpw = 8.20GiB
  (FeitengLi, 09-09, "100% on AIME 2026" self-report); official Unsloth Dynamic V3 GGUFs claim
  +10% accuracy (Alibaba_Qwen, snippet); the Unsloth GGUF hit 10M downloads / 3.7K likes in 24
  days (snippet, 09-2x); disaggregated-quant paper reports Qwen3.8-27B GGUF decode arms with
  1.78x TTFT at 8K prompts in llama.cpp (abstract).
- Qwen3.5-4B: unsloth/Qwen3.5-4B-GGUF Q4_K_M is the HF blog's canonical local example; runs in
  both runtimes (above).
- nimble 9B / tev1 4B / tev1:0.8b: pull-and-run via `ollama pull nimble` day-0 with Ollama 0.35;
  per-quant footprints not published in the post (OWED).
- Qwen3.8-27B vision tower: Q4_K GGUF at 314.46MiB, "no modifications to llama.cpp required".
- Quant-quality priors (context, out-of-window source): bnjmn_marie's March eval found Q4-class
  GGUFs close to original and no good Q2 for Qwen3.5-27B - consistent with the held
  Quantization-Thresholds paper's never-below-3-bit law for agentic work.

## Overlap record (greps actually run this session)

- "2609.26693" catalog = 1 row (catalog.jsonl:445316, raw 1,469B abstract snapshot,
  state/arxiv/2026-09-23/, daily-harvest landed); memory/ knows the ID in
  memory/runs/corpus_gap_research/ARXIV_REGISTER.json + MAP_BACKFILL.{json,md} and
  memory/runs/mickey17_v2/.../arxiv-eval-week.json. Full findings not digested anywhere I found.
- "tev1" / "systemone" / "Jev-like" / "Ollama 0.35" catalog = 0 rows. memory/ holds the Jev
  DOCTRINE: memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:9,30,245,283 names
  POST api.typesafe.ai/v1/systemone, CHOICE/SCORE/NOUL, and "stand a local Jev-compatible
  /v1/systemone". The Ollama-native implementation + model trio is the new fact.
- "Bespoke Labs": memory/research_packs/COMPACTION_ALGO_RESEARCH_20260919.md name-only; "Bespoke"
  catalog 0. "nimble" in memory = Gutenberg corpus common-word false positives only.
- "transformers-llama-cpp-quants" / "GGUF models efficiently": catalog 0, memory
  (research_packs/polished/thinking) 0. New.
- "abliteration": catalog 17 rows + agent_sessions (the technique is held discourse); "engram"
  catalog 21 rows (DeepSeek-Engram architecture references); "madhukaraphatak" catalog 0; the
  post + its 108-point thread are new.
- "Benchmarking Local LLM Servers": catalog 0, memory 0. New.
- "Ling-3.1" / "Ling-3.1-flash" / "AntLingAGI" / "Ling-2" / "OllamaDrama" / "Ollure" / "Illusion
  of Local Privacy" / "2609.18526" / "2609.29757": catalog 0; memory hits are steps.jsonl
  self-echo only (the known false-positive class, cf. 09-30 sweep overlap record). New.
- "Qwen3.8-27B": catalog 2 rows + 3 research_packs (model held); the 2.96/2.48bpw footprints,
  MTP-in-GGUF, AIME claim, and vision Q4_K 314.46MiB numbers appear in no holding I found.
- HELD and not re-banked: DSv4.1-Flash (Ollama-cloud rollout, register rows), ggerganov HF/NVIDIA
  (HN 49567357 resurfaced it), Tetra 2609.35465 (catalog:671313 raw), GLM-5.3-Flash promo lanes,
  x_intel_drop items (LiteLLM LENS, mating, Ghidra, Ternary-Bonsai PTQ1_0 log diagnosis).

## OWED (not done, stated)

- nimble's concrete license (post says only "open-source"); tev1 license unverified.
- arXiv 2609.29757 and 2609.18526 full texts not fetched (abstracts read via the Atom door only).
- "This Week In OS AI Field Notes"-class aggregators not chased this session (out of X-door scope).
- The GLM 5.4 / DSv4.1-pro / Kimi K4 "leak list" is unverified rumor, banked as rumor only.
- E1-E3's Ollama-arm experiment remains unbuilt by this lane; the two RQ2 sources give the design
  citations, not the estate's own measurements.
- FeitengLi "100% on AIME 2026" is a vendor-self-report (laws.md:23: banked is not verified).

## Steal candidates (proposals, sensing-tier)

1. Register the serving-stack checklist of 2609.26693 into the C1 program as E0 (a protocol
   hygiene gate BEFORE E1-E3 arms): preserve rejection/retry as structured metadata, log the
   Ollama template-flag verdict per model, pin turn-pooled AND per-instance reporting.
2. Pull `ollama pull nimble` + tev1:0.8b into the janitor lane as a TYPED-DECISION scut rung
   (triage/routing/moderation at 91ms-class), benchmarked against gemma:2b on the same three
   tasks - this is the replacement-or-keep verdict the estate map asked for, and it is cheap.
3. Add the dual-runtime GGUF read (transformers from_pretrained on the same Q4_K_M file the
   Ollama path serves) as the E1 instrument - the 09-22 HF release makes same-bytes two-runtime
   A/Bs a config change, not a port.
4. Bind-check law candidate: an Ollama/llama-server exposure check (external bind + no-auth)
   into the drift patrol, citing OllamaDrama's 290,887-interaction census.
5. Config-before-engine: apply the Mozilla knobs to the janitor lane first (speculative draft
   depth per platform, shader toolchain vintage) before any engine swap is considered.
