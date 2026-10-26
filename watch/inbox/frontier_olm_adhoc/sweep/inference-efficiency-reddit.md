# inference-efficiency sweep via reddit - 2026-10-11 evening retry (frontier gopher, adhoc)

source-fetched: adhoc

Supersedes the 01:50 attempt (preserved at `_inference-efficiency-reddit.attempt1.md`): that attempt's safereddit.com door was dead by the time this seat ran, and its "Swift-Qwen zero overlap" claim is contradicted by this run's catalog grep (see overlap section). Every quote below was fetched and read by THIS seat this session; nothing carried over unverifiable.

## Door report (degraded doors, per recipe)

- old.reddit.com: FULLY login-walled in 2026 ("Log in to use old Reddit"). Listing .json, search .json, per-thread .json via curl: all serve the "Welcome to Reddit" wall (files `_localllama_top.json`, `_ollama_top.json`, `_localllm_top.json`, `_ml_top.json`, `_sd_search.json` inspected; identical ~327KB block page).
- WebFetch on www/old reddit: JS shell only ("Reddit" / landing stub).
- webReader MCP on www.reddit.com HTML: renders titles + partial top-of-feed, interstitial roulette ("Prove your humanity" / "Please wait for verification"), search pages captcha'd, any .json URL blocked by network security.
- DDG html + lite: form/anomaly page, zero results. Mojeek: 0 reddit links. pullpush.io: agent rate-limited. r.jina.ai: reddit domain blocked until 2026-10-11 21:51 GMT. archive.today: no snapshot. Wayback CDX: 504 x3; the one direct snapshot of thread 1sq7grd archived the verification wall itself. Redlib mirrors incl. safereddit.com: dead or Cloudflare-walled this run.
- WebSearch fallback (recipe-sanctioned): `site:` operator IGNORED by the engine and 429-prone; the productive shape was `"LocalLLaMA" reddit thread <topic>`.
- WORKING DOOR: per-thread RSS via curl, `https://www.reddit.com/comments/<id>.rss` or full canonical path + `/.rss`, UA "Mozilla/5.0 ... MagResearchSweep/1.0", 7-25s spacing (throttles to 0 bytes under rapid fire). Full post + comment Atom feeds landed for 10 threads (`_read_*.xml`, parsed `_read_*.txt`).
- Candidate pool: listing titles from webReader renders of www.reddit.com/r/*/top/?t=month plus 70+ in-window thread URLs cross-harvested from sibling sweep candidate files in this directory (leads only; every banked thread was fetched and read by THIS seat via RSS).

## Pass 1 (broad sweep)

70+ in-window candidates (2026-09-11..2026-10-11) across r/LocalLLaMA, r/LocalLLM, r/ollama, r/MachineLearning; tracker `_cand_inference_efficiency.md`. Top/month render also read directly (Jev, PewDiePie LLM, HF security.txt, "The state of self-hosting LLMs in 2026" 2026-10-01).

## Pass 2 (deep reads - 10 threads read end to end via RSS)

BANKED (7, strongest first, same order as submitted JSON):

### 1. 153 tok/s on 1x AMD Radeon R9700 running Qwen3.8 27b NVFP4, 470 tok/s @ 8 conc requests (r/LocalLLaMA, 2026-09-17)
https://www.reddit.com/r/LocalLLaMA/comments/1wiws8e/153_toks_on_1x_amd_radeon_r9700_running_qwen38/
Measured concurrency scaling on ONE card: 1=120, 2=215, 4=322, 8=471 tok/s aggregate; prefill 3192-3619 tok/s flat from 2K to 64K depth; per-category decode json 153.1 / file_edit 138.0 / code 120.5 / prose 69.2 / chat 67.1 - structure-heavy workloads decode ~2.2x faster than prose, which matches DFlash acceptance-by-task in the Swift thread (Structured 81.2% vs Story 16.7%). RQ4 answer for the multi-ollama janitor shape: batching inside one engine beats adding engines, near-linear to conc 4, +46% from 4 to 8. Overlap: catalog 1wiws8e=0, R9700=0, "470 tok"=0.

### 2. Fork of FreeToken with DeepSeek-V4.1, vision and speculative decoding (2x3090 numbers inside) (r/LocalLLaMA, 2026-09-22)
https://www.reddit.com/r/LocalLLaMA/comments/1wn852z/fork_of_freetoken_with_deepseekv41_vision_and/
RQ1 core, both directions measured. OP bench (256 out tokens, 5 runs): greedy MTP off 48.0/52.4 tok/s vs greedy MTP on 21.5/22.4 tok/s at accept rate ~56% - NET LOSS on expert-offloaded MoE with CUDA graphs; matched eager ~1.5x (17.2 vs 11.4); per-batch-size verify graph moved the MTP path 16 to 28 tok/s. Comment (2026-09-28): ">200 tok/s in total on dual rtx 3090 with 27B and mtp enabled, with acceptance rates from 50-70%" - dense 27B WINS. Fleet lesson: 50-70% acceptance is reachable, but acceptance alone does not predict the win; serving-path architecture (graphs, expert offload) decides. Overlap: FreeToken project known (catalog FREETOKEN_STEAL_20260822.md, 5 rows); this thread's MTP benches postdate it and are not held.

### 3. Qwen3.8-27B at true 128K + Vision on a single RTX 5080 16GB - NInfer v1.3, MTP-3 (r/LocalLLM, 2026-09-22)
https://www.reddit.com/r/LocalLLM/comments/1wmucw0/qwen3827b_at_true_128k_vision_on_a_single_rtx/
RQ1 measured acceptance by context depth: 5080 at an actual 118,001-token prompt: 1380 tok/s prefill / 71.5 tok/s decode / 44.74% MTP acceptance / 2.31 tok per round; 5070 Ti at ~12K context: 102-108 tok/s decode at 74-79% acceptance (one logged request: 4310 tokens at 107.5 tok/s); 5060 Ti: 30-40 tok/s decode, 500-700 prefill. Acceptance DROPS with context depth (74-79% at 12K vs 44.74% at 118K): spec-decode value concentrates in short-context scut, exactly the fleet's scut/judgment split. Also: Q4-G64 KV fused into the attention path (no separate quant pass), default thinking budget 2048, and the admission-queue fix (keep max-concurrency 1, raise --pending-timeout-ms to 120000/300000 instead of widening) - RQ4 adjacent. Overlap: NInfer known (catalog 45 rows incl. OrcaRouter DFlash2 artifacts); thread 1wmucw0 itself not held.

### 4. MiMo-V2.6-Flash on vLLM: fixes for "empty responses" with thinking + tools, and a hidden 2,048-token output cap (r/LocalLLaMA, 2026-09-22)
https://www.reddit.com/r/LocalLLaMA/comments/1wnjbwn/mimov26flash_on_vllm_fixes_for_empty_responses/
RQ2 direct hit - the EMPTY_REASONING failure in the wild with the re-fire count measured: OP's agent reported "No response from provider" and retried the same call 4-5 times while the server logged all 200 OK (en-dash transcribed to hyphen). Root cause: multi-turn prompts contain </think> from history; vLLM's streaming is_reasoning_end() scans PROMPT token ids, declares reasoning already over before generation starts, so delta.reasoning arrives empty and reasoning streams as unclosed <think> content that clients strip and discard. Fix: pre-open <think> in the generation prompt (template patch, verified 6/6 incl. tool-call turns). Plus: reasoning field-name mismatch (reasoning vs reasoning_content) silently drops earlier thinking in tool loops (vllm/entrypoints/chat_utils.py one-line fallback); generation_config max_new_tokens 2048 silently caps thinking-heavy replies (fix: --override-generation-config with max_new_tokens 131072). Thinking-effort economics on 4 prompts x 2 runs: unset 262 avg tokens / 4.8 s / 7 of 8 correct; low 221 / 4.1 / 8 of 8; max 536 / 10.6 / 8 of 8. Wiring cost for the seven jackets: a terminal reaction on empty reasoning + a template assertion, hours not days; saves the 4-5x re-fire class behind the $20.53-of-$29.91 worst case. Overlap: MiMo known broadly (catalog 78), MiMo-V2.6 3, thread not held.

### 5. Running an LLM-driven town with 800+ persistent agents: concurrency, context caching, and inference costs (r/LocalLLaMA, 2026-10-08)
https://www.reddit.com/r/LocalLLaMA/comments/1x0ms0m/running_an_llmdriven_town_with_800_persistent/
RQ4 at fleet scale: 800+ agents, 300-400 calls/day each at ~30K context, ~5B tokens/day under $100 (deepseek-flash, cache hit above 90%; 2026-10-07 day: ~4.424B tokens, 163,742 requests, CNY 472.33). Cache hit is a request-architecture achievement, not a provider feature: stable instructions front, state-dependent tail; dynamic action spaces moved OUT of the schema because a changing schema poisoned the prefix. Validation-retry overhead measured: ~0.9% of ~160K daily decisions (1,450 failures, ~1,490 retry calls). Comment steal for the local fleet: "llama-server can save a slot's kv cache to disk and load it back. we prefill each persona's fixed prompt once and restore it per chat. for a 27k token prefix on cpu that was 98 s of prefill vs 67 ms to restore." Concurrency law: LLM calls run concurrently but NEVER mutate world state directly; results re-validate at execution time. OP's back-of-envelope: self-hosted Qwen-27B-class could cover the throughput "for less than half the cost" (untested). Overlap: thread XML already fetched by today's kv-cache sibling (`_kv_thread_1x0ms0m.xml` in catalog); this sweep's cut is the scheduling/economics read.

### 6. 128K context on Qwen 3.5 4B in 800 MB instead of 4 GB: what we changed in our llama.cpp build (r/LocalLLM, 2026-10-09)
https://www.reddit.com/r/LocalLLM/comments/1x17lnk/128k_context_on_qwen_35_4b_in_800_mb_instead_of/
Byte-identical prefix discipline: system prompt + tool catalog frozen, per-step state at the tail; "a reply on Qwen 27B that used to take 4 min 20 s to start now starts in about 1 s" - cache reuse, not faster kernels. Loop guard = the anti re-fire instrument for RQ2: "Three identical calls in a row get a warning. Five with no new result and the call is blocked. Three blocks and the run stops and tells you why." Reasoning capped ~1500 tokens/step so a small model cannot think in circles. Comment tripwire worth stealing: assert the prefix hash between steps so a cache regression surfaces as a warning, not a stalled session. Skeptic counterweight in comments: kvarn3 tested at least on par with q5; community sees turboquant as not much better than rotated quants. Overlap: TurboQuant known (catalog 9 rows, lmcache serde docs); thread + atomic-agent not held.

### 7. I run 6 LLMs + SD 3.5 + Whisper behind an OpenAI-compatible API on an RX 580 8 GB (r/LocalLLaMA, 2026-10-06)
https://www.reddit.com/r/LocalLLaMA/comments/1wyqk24/i_run_6_llms_sd_35_whisper_behind_an/
The janitor-fleet shape on forgotten hardware, fully measured (Ryzen 5 5600G / 32GB / RX 580 2048SP, Vulkan RADV, one Debian LXC): qwen2.5-coder-1.5b 99.2 tok/s (warm 3.1 s, cold 11.0 s); qwen2.5-vl-3b 66.4; qwen2.5-7b 34.2; ornith-1.5-9b 28.0; qwen3-30b-a3b (18.6GB from RAM) 21.3 (warm 14.1 s, cold 55.0 s). Two fleet laws: do not force -ngl 99 on the MoE (8.1 vs 22.3 tok/s; auto-fit layer offload won ~3x) and model swap = llama-server restart = 7.9-38.5 s, so keep one model per session (sticky routing, no churn). Agent path: first message ~161 s on a 20K-token prompt, ~25 s after caching. MIT repo: github.com/AvilaCarlosDev/polaris-local-ai. Overlap: zero (polaris-local-ai, RX 580: catalog 0).

## Read but NOT banked (already held - re-banking is waste)

- 1wg7dd5 UkisAI Swift-Qwen3.8-27B (-58.3% thinking, x1.95 speed): deep-banked 2026-10-06 (`frontier_olm_2026-10-06/sweep/doors/ff_deep/1wg7dd5.comments.json` + post.json, catalog rows verified this run) plus a 2026-10-10 intake txt of the same title. My independent re-read confirms the headline table (Swift xhigh 88.3% at 2,771 median tokens vs base xhigh 88.4% at 6,642; base medium 84.1% at 1,753) and the DFlash2 acceptance-by-task bench (Code 53.9%, Story 16.7%, Translation 48.9%, Structured 81.2%, AIME 39.1-66.4%) - that task-typed acceptance table is the RQ1 prediction instrument and deserves a pointer from the inference-opt shelf.
- 1wv05u1 Jeff-Qwen3.5-0.8B v1.2 + 9 LoRA adapters (38x faster decisions): catalog already holds 13 rows. My read adds the ablation: adapters-only 95.2%/0.21s, routing-only 87.1%/7.0s, both 95.3%/0.25s - trained small-model competence, not uncertainty routing, carries the win; grounding is the exception (route 11% to the 27B, 98.7%, still ~7x faster).
- 1wiu7xj Keeping vLLM's Prefix Cache Warm Between Agent Turns: thread XML fetched by today's kv sibling (catalog row). Comment gem for the jackets: Qwen3's template strips <think> from earlier assistant turns, so the rendered token sequence no longer matches the cache - keep reasoning in or render history yourself.

## Overlap checks (commands actually run this session)

- `grep -c -i "<phrase>" catalog/catalog.jsonl` for FreeToken(5), NInfer(45), MTP-3(0), Slow Vale(0), slowvale(0), MiMo-V2.6(3), UkisAI(1), Swift-Qwen(1), polaris-local-ai(0), TurboQuant(9), atomic-agent(0), DFlash(2), "Keeping vLLM"(0), 1wv05u1(13), 1wiws8e(0), jeffhub(0), R9700(0).
- `grep -r -l -i --include="*.md" --include="*.json" --include="*.jsonl" <10 phrases> memory/` -> zero files (an earlier -c variant printed garbage on binary rows and was killed; the -l rerun is the trusted one).
- Thread-ID grep: 1wg7dd5 rows = the 2026-10-06 ff_deep bank; 1wiu7xj + 1x0ms0m rows = today's kv sibling fetches; 1wn852z/1wmucw0/1wnjbwn/1wyqk24/1x17lnk/1wiws8e absent.
- Jeff in memory: memory/trajectory/steps.jsonl mentions 1wv05u1 (prior sweep trajectory), consistent with drop.

## Research-question verdicts

- RQ1 (spec decoding, measured): answered with spread - 50-70% acceptance dense-27B dual-3090 (>200 tok/s total), 74-79% at 12K falling to 44.74% at 118K on a 16GB single card, and 56%-yet-net-loss on expert-offload MoE (48.0 -> 21.5 tok/s). No in-window thread measured a discrete 2B external draft model; the 2026 live forms are MTP/DFlash heads and the 0.8B Jeff cascade. A gemma-class discrete-draft bench stays OWED.
- RQ2 (EMPTY_REASONING wiring): mechanism + template fix + measured 4-5x re-fire cost captured (1wnjbwn); loop-guard reference implementation captured (1x17lnk: warn at 3 identical calls, block at 5, stop at 3 blocks). Wiring looks hours-per-jacket, not days; the $20.53-vs-saved accounting is ours to measure after wiring.
- RQ3 (off-state / thinking-disabled economics): partial - thinking-effort token/time table (unset 262 tok / 4.8 s vs max 536 / 10.6 s), the 2048 silent-cap trap, DSV4 prefill-speed praise; Swift's -58% thinking at xhigh accuracy already held. No thread measured deepseek thinking-disabled cost-per-cent directly: OWED.
- RQ4 (scheduling beyond prefix cache): the strongest haul - concurrency table 1/2/4/8 = 120/215/322/471, admission-queue timeout pattern over width, KV save/restore 98 s -> 67 ms per 27K prefix, 90%+ cache-hit request architecture with schema-out-of-prefix, sticky one-model-per-session routing, and never-let-inference-mutate-state-directly.
- RQ5 (burns ledger writer): nothing on reddit bears on memory/burns/LEDGER.jsonl or its writer; the unfreeze-or-retire call stays the operator's (burns.md:57, 226-228). Not invented here.
