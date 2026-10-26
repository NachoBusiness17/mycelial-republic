# FRONTIER SWEEP: finetuning-adaptation via reddit (2026-10-10)

source-fetched: adhoc

Doors, honestly recorded. Every reddit-native door named by the recipe degraded this
session: `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` (WebFetch) returned a
"Welcome to Reddit / Log in to use old Reddit" block page instead of JSON; the same door
via the webReader MCP returned the same login wall; `www.reddit.com/.../top.json`
returned HTTP 403 Blocked; `old.reddit.com/r/MachineLearning/top.json` timed out at 60s;
`api.reddit.com` via curl returned an HTML theme page, not JSON; `api.pullpush.io`
refused agents outright ("Rate limit exceeded. This website does not provide free
scraping resources for agents"). The recipe's named fallback (WebSearch site:reddit.com)
was itself 429-rate-limited (error 1302) for roughly the first 15 minutes and only
partially recovered late in the session. The door that actually carried this sweep: the
arctic-shift reddit archive
(`https://arctic-shift.photon-reddit.com/api/posts/search` + `/api/comments/search`),
fetched by the pinned-allowlist scripts `_ft_sweep.py` / `_ft_read.py` in this
directory. WebSearch was used once, late, to confirm the RQ3 negative (no 2026 TRL or
verl release threads).

Pass 1 (broad sweep, last 30 days, at least 30 candidates). Three rounds of keyword
queries (title/selftext filters; full-word only, the archive rejects partial words and
many acronyms with HTTP 422) across r/LocalLLaMA, r/MachineLearning, r/LocalLLM,
r/ollama, plus three score-ranked 100-post created_utc windows. Merged pool: 55 distinct
posts (`_ft_candidates.json`) plus about 50 more from the day-window pages and the
title=LoRA list. Distinct candidates considered: about 90. Topic coverage: LoRA,
fine-tuning, test-time, adapter, distill, Unsloth, GRPO, self-improvement, reinforcement,
PPO/RLHF (422-rejected), ten-minutes. r/LocalLLM and r/ollama returned 0 fine-tuning
rows through every query that survived rate limiting; recorded as a door-side negative,
not as absence of content.

Pass 2 (deep reads, end to end). 11 threads fetched as selftext plus full comment trees
(`_read_*.md` files here; comments ranked locally by score): zebra/PCSS, Jeff
LoRA-router, ML TTT loop, DeepSeek RSI reflections, MOLT, LoRA-serving-11to90, SFTMill,
cost-thread, ImaJev, AgileRL Arena, MedGemma, magnitude. Two were moderator-removed
corpses (1wjkt47 "runnable test-time training loop", 1wr469w "LoRA scored 11/90 then
90/90": selftext [removed], unreadable, discarded). Four were already estate holdings
from sibling sweeps (dropped, listed below). One (magnitude) was read and rejected as
off-question. Five are banked below as genuinely new; the PCSS item was additionally
verified end-to-end against its linked HF blog via WebFetch.

## Banked items (new, strongest first)

1. PCSS: 100 zebra puzzles, 6.5 minutes, +31 on held-out MATH
   https://reddit.com/r/LocalLLaMA/comments/1wdhb24/ (2026-09-11, 37 pts) ->
   https://huggingface.co/blog/tamewild/pcss (read via WebFetch).
   Qwen3-4B-Base fine-tuned on 100 logic-deduction traces (06:23 on one vast.ai H200,
   reproduction notebook public). Full MATH (5k): 54.10% -> 85.26% (+31.16). AIME 2025
   21.67%. Granite-4.1-3B on 500 traces: 23:41. Qwen3.5-9B: 40:21, 5x5 Zebra 17.0% ->
   80.5%. This is the strongest direct support for the operator's JIT fine-tuning law at
   under ten minutes of adaptation latency that this window produced: controlled tiny
   corpus, minutes-scale run, held-out out-of-domain eval, public notebook. Verbatim:
   "Fine-tuning on as few as 100 pure logic deduction traces (zebra puzzles) can elicit
   substantial out-of-domain reasoning generalization."

2. MedGemma oncology LoRA/QLoRA on one DGX Spark + Unsloth merge-scale discrepancy
   https://reddit.com/r/LocalLLaMA/comments/1wywscq/ (2026-10-06).
   4B LoRA 56.0% -> 71.6% in 2h39; 27B QLoRA 68.8% -> 77.9%; tuned 4B beats base 27B by
   paired McNemar (209 gained / 149 lost, p = 0.002). The pitfall half: merging the r=64
   adapter at nominal scale lost most of the tuning (83.8% agreement; alpha=32 gave
   93.2%); identity probes suggest an effective scale of about 2x alpha/r under Unsloth
   (7/7 vs 0/4 under Transformers+PEFT), offered as an open reproduction request with a
   probe script in Zenodo (10.5281/zenodo.23134374) and explicitly NOT a demonstration
   (author's own caveat list: one seed, no CV, no ablation, environment versions outside
   declared ranges, TRL 0.26.1, Transformers 5.18.0). Also: bf16 rounding on merge
   erases 17-37% of delta elements; quiz tasks survive, verbatim memorization does not.
   Cost point: a rigorous single-node domain tune at 2h39 wall clock. Verbatim:
   "Overall accuracy: 4B 56.0% -> 71.6% (2h39 of training), 27B 68.8% -> 77.9%. The
   tuned 4B beats the base 27B (209 items gained, 149 lost, p = 0.002)."

3. MOLT: local fine-tuning with fit tests, checkpoints, deployment tracing
   https://reddit.com/r/LocalLLaMA/comments/1wyvc8k/ (2026-10-06, 0 pts, 2 comments;
   zero traction, architecturally exact).
   Consumer-NVIDIA QLoRA system: dataset validation, pre-run GPU/VRAM/thermal checks,
   automatic microbatch fit testing, safe checkpoints with integrity checks and resume,
   telemetry, base-vs-adapter evaluation, GGUF export. This is `mag improve` plus the
   promotion gate in miniature on one laptop GPU (RTX 4060 8GB, about 1,005 targets/s
   vs Unsloth's about 1,007, honestly labeled not-a-win-yet). Steal: "fit tests before
   run" and "base-vs-adapter eval" as first-class citizens of a local lane. Verbatim:
   "The goal is not only to start a QLoRA run. It is to make the whole process from
   model and dataset to a working local adapter less fragile."

4. AgileRL Arena v1.0: manifest-driven RL training, local or cloud, LoRA/GRPO LLM path
   https://reddit.com/r/LocalLLaMA/comments/1wdjk0y/ (2026-09-11, 5 pts).
   The only in-window release on the deep-rl shelf this door surfaced that targets the
   1-8B local lane directly: YAML manifest (algorithm, env, network, LoRA config,
   reward env), Pydantic validation so bad configs fail before training, LocalTrainer
   with no account, PEFT 0.20 with automatic Mamba target-module exclusion,
   evolutionary-HPO population training. Repo github.com/AgileRL/AgileRL. Verbatim:
   "Validation is Pydantic, so bad configs fail before training instead of 40 minutes
   in."

5. Engineering handbook for GRPO + LoRA with verl (Weyaxi, HF blog)
   https://huggingface.co/blog/Weyaxi/engineering-handbook-grpo-lora-with-verl
   (fetched via WebFetch; page shows no date, vintage unknown, likely pre-2026).
   The concrete cost/latency anchor for a verl-based small-model RL lane: Qwen2.5-3B
   LoRA r64 GRPO on GSM8K, 4x A100-80GB RunPod, roughly $40 total, roughly 6h for 15
   epochs / 105 steps. Load-bearing lessons: TP=4 -> TP=1 cut time by about 33% (tensor
   parallelism is counterproductive at 3B); rollout.gpu_memory_utilization 0.6 -> 0.8
   saved about 8% (0.9 OOMs); N=5 -> N=10 rollouts added 70% time for marginal
   stability (negative ROI); checkpoint disk-full crash discipline (save_total_limit=3,
   resume_mode=auto); a verl release bug required pinning commit d12d6b3e. Internal val
   59% -> 85% with most gain in the first 3 epochs; external benchmark gains modest
   (format overfit). Verbatim: "We are deploying this on a RunPod instance with 4x
   NVIDIA A100 (80GB) SXM GPUs."

## Already held (verified this session, NOT re-banked; the dedup that matters)

- 1wv05u1 Jeff-Qwen3.5-0.8B + 9 LoRA adapters router, 1wtqpjt SFTMill, 1wsgrma
  ImaJev-4b ($1200 / 15 days / 4xH100 decision model with a documented
  collapse-and-recovery data cycle), 1wu9zkn fine-tuning-cost thread ("dataset is 99%
  of the work"; "fine-tuning is often best at teaching: format, style, behavior,
  decision rules, task performance"): all four deep-read by me this session AND already
  cataloged from watch/inbox/frontier_olm_2026-10-04/sweep/_fta_thread_*.txt.
- 1wgii3h DeepSeek engineer RSI reflections (392 pts): held by
  frontier_olm_2026-10-06/sweep/_raw/deep_1006/. Read by me; zeitgeist only, no
  falsifier content, nothing new to bank.
- 1x1bdvl LoRA-over-GGUF 40G VRAM: held by frontier_olm_2026-10-09/sweep/.

## Research-question verdicts

RQ1 (JIT/test-time/LoRA-swap under 10 min): SUPPORTED at the 4B scale by PCSS (6:23
wall clock, 100 samples, +31.16 held-out). The LoRA-swap pattern itself is real and
sibling-held (Jeff router: adapters about 40 MB, about 30 ms per decision on GPU, +8.7
points mean with bootstrap CIs). Bounded by the MedGemma merge-scale finding: the
serving/merge stack can silently eat most of a tune, so the JIT law needs a
merge/serving-verification step or an adapter-only serving path, not just fast training.

RQ2 (loop with ten-minute-self-grade falsifiers): NO published agent self-improvement
loop surfaced, through any door tried, that reports week-over-week pitfall-rate decline
or a controlled-corpus fold beating prompt-only on held-out pitfalls. Published
negative; nothing here clears the rib's falsifiers, so the rib stays unchallenged. The
nearest shapes: PCSS (single-shot, held-out, minutes, but no recurring loop), ImaJev
(collapse-then-recovery data curation cycle, sibling-held), MOLT (the gate/checkpoint
plumbing such a loop would need, but no loop shipped).

RQ3 (2026 TRL/verl/deep-rl releases for a 1-8B lane): published negative on the release
threads: no 2026 TRL or verl release thread surfaced via archive title/selftext search
or the late WebSearch (which surfaced only pre-window GRPO threads and the repos
themselves). In-window shelf signal that did land: AgileRL Arena v1.0 (above). Version
datum from the wild: TRL 0.26.1 + Transformers 5.18.0 (MedGemma post, outside PyPI
declared ranges; treat as environment-drift evidence, not a recommendation). The clone
budget at corpus/CURRICULUM.md:85-89 stays valid as written: trl + verl + deep-rl-class
remain the right repos; nothing this window argues for a different pick.

RQ4 (cost points, context-to-weight door, beats prompt+retrieval?): session-to-weights
cost ladder from this window: $40 / 6h / 4xA100 (verl GRPO LoRA 3B, handbook); 2h39 on
one DGX Spark for a 4B domain tune with McNemar rigor (MedGemma); 6:23 on an H200 for a
100-sample behavioral tune (PCSS, the only true sub-ten-minute point); $1200 / 15 days
for a 4B decision model (ImaJev, sibling-held). Practitioner consensus (sibling-held
cost thread): dataset construction is about 99% of the work; fine-tuning reliably buys
format/style/behavior/decision rules, which is exactly the pitfall-bypass-corpus
regime, while knowledge belongs in context. Nothing this window showed beats
prompt-plus-retrieval at estate scale for knowledge; the evidence for weights is
behavioral, which is the JIT law's own claim.

## OWED (never asserted as done)

- TRL and verl 2026 release notes themselves were NOT fetched (no reddit thread pointed
  at them; reading GitHub release pages is outside this sweep's reddit door).
- r/LocalLLM and r/ollama yielded zero readable rows through every query that survived
  rate limiting; those subreddits stay unswept this window.
- The arctic-shift archive rejects acronym and partial-word title filters (HTTP 422:
  TRL, verl, RLHF, DPO, PPO, "fine-tun", "self-improv"); short-acronym threads are
  systematically under-sampled by this door.
- The MedGemma scale discrepancy is unverified (the author says so; probe script public
  in Zenodo 10.5281/zenodo.23134374); banked as an open reproduction request.

Scratch receipts: `_ft_sweep.py`, `_ft_sweep3.py`, `_ft_read.py`, `_ft_candidates.json`
(55 posts), `_read_*.md` (11 threads), `_tmp_a[123].json` (day windows),
`_tmp_q_lora.json`.


---

# PASS 2: finetuning-adaptation via reddit, second sweep seat (2026-10-11 evening)

source-fetched: adhoc

This section AMENDS the 2026-10-10/01:57 sweep above (amend, never rewrite): that
sweep's five banked items and its held list stand untouched. This pass re-ran the
recipe doors, re-swept, deep-read six threads, and banks only items verified absent
from catalog/catalog.jsonl, memory/, and watch/inbox/frontier_olm_adhoc/register.jsonl
(greps this session; scratch corpus/tmp/as_sweep/).

Doors this pass, honestly recorded. Same degradation as the 01:57 sweep, confirmed
again: old.reddit.com/r/LocalLLaMA/top.json login wall ("Log in to use old Reddit",
webReader + WebFetch both); www.reddit.com top.json HTTP 403 Blocked (WebFetch) and
"blocked by network security" (webReader); www.reddit.com thread pages return a JS
shell or "Prove your humanity"; api.pullpush.io 429 with curl. Recipe fallback
WebSearch site:reddit.com worked partially (several 1302 rate-limit errors; it yielded
thread URLs including the TTT set but no readable bodies). The door that carried this
pass, same as the 01:57 sweep: the arctic-shift archive API
(arctic-shift.photon-reddit.com/api/posts/search, /api/posts/ids,
/api/comments/search), throttled (422 "Timeout. Maybe slow down a bit" under about
30 s spacing; 32-40 s spacing held).

Pass 1 (broad, last 30 days): keyword pulls lora/finetune/qlora/unsloth over
r/LocalLLaMA since 2026-09-11 (4 successful queries; training/ttt/gemma/test/verl/
trl/adapter all 422-throttled, same under-sampling caveat as the 01:57 OWED list).
34 unique posts in the merged pool plus 7 WebSearch-door URLs and 12 shortlist bodies
fetched: about 45 distinct candidates considered this pass. r/LocalLLM, r/ollama,
r/MachineLearning stayed unswept (throttle budget spent on r/LocalLLaMA; recorded as
door-side negative, not absence).

Pass 2 (deep reads): six threads read as full selftext plus comment trees via the
archive API: 1x0xkk7 Castmates (selftext + 4/4 comments), 1wujtbj Victoria/Maple
(selftext + 9/9 comments), 1q5kokx PonderTTT (selftext + 2/2 comments), 1wnrh76
Unsloth Studio vs LM Studio (title + 100/123 comments; OP body not fetched, stated),
1wr0p3n TensorSharp (selftext + 8/8 comments), 1wybqq3 easycommand (selftext only;
its 5 comments not fetched, OWED). Two corpses confirmed again (1wr469w, 1x0egcy:
bodies [removed]). One candidate dropped as thin (1x10r5t VeriLoop-E2 pointer post).

## Banked items (new, strongest first; all quotes verbatim from fetched archive JSON)

6. Castmates: 3B roleplay finetune fully on iPhone, measured
   https://www.reddit.com/r/LocalLLaMA/comments/1x0xkk7/ (2026-10-08).
   Own rank-16 LoRA on Impish Llama 3B, fused and requantized to Q4_K_M from fp16
   (about 2.0 GB, 4 GB phones the floor, about 6 tok/s on A18, KV q8_0 at about
   60 KB/token). Measured laws: history-trim budget, not n_ctx, was binding (trim at
   0.68 x n_ctx took long-conversation fact recall from 25% to 75%); BM25 retrieval
   re-injected superseded facts (says-stale +20.8pp; filtering hits whose rare
   entities still live in the window fixed it, -18.8pp CI [-35.4,-6.2]); prompt
   wording tweaks measured as zero under N=16 same-seed fixed-history controls;
   placement beat wording (scene direction 0/16 in the reminder slot vs 16/16
   elsewhere). RQ1 (what a 3B absorbs on-device, at what cost) and RQ4 (prompt-only
   vs structural changes) in one artifact. Verbatim: "Prompt tweaks mostly measured
   as zero. Single 3-4 seed runs were noise. Fixed-history micro-tests with N=16 and
   same-seed controls were the only thing we trusted."

7. Victoria + Maple: post-quantization retraining, trained for the shipped format
   https://www.reddit.com/r/LocalLLaMA/comments/1wujtbj/ (2026-09-30).
   Qwen3.8-Flash-Next cut 44% by REAP (512 to 288 experts per layer), then RETRAINED
   at NVFP4 so the weights learn the format they ship in: Terminal-Bench 2.1 70.0%
   avg-of-3 (previous NVFP4 build 62.5%); GGUF Q4_K_M 75.3% single run; draft head
   280 vs 135 tok/s on one B300. Serving law for adapted artifacts: mainline
   llama.cpp rejects their GGUF draft head ("expected 1256, got 1224") until patched.
   Maple (Canadian-default finetune on top): official-source citation 6.0% to 62.9%,
   fully-correct 6.6% to 21.8% on 600 held-out questions; coding held (157/164
   HumanEval). Extends the LoRA-over-GGUF law family the estate banked from 1x1bdvl:
   adaptation artifacts carry stack contracts; "quantize after the fact" leaves
   points on the table vs training at the shipped format. Verbatim: "Retrained at
   4-bit (NVFP4) afterwards, so it's trained for the format it ships in rather than
   just quantized after the fact."

8. PonderTTT: gated test-time training at 124M-1.5B (out-of-window gem, Jan 2026)
   https://www.reddit.com/r/LocalLLaMA/comments/1q5kokx/ (2026-01-06).
   TTT-layer weight updates gated by the layer's own self-supervised reconstruction
   loss (threshold + EMA, no extra training): 82-89% oracle recovery on GPT-2 code
   LM, up to 16% lower loss OOD vs random skip; v1 JAX/Flax, v2 targeting Gemma 3.
   RQ3 fit: the first TTT shape surfaced that matches the living-weights two-tier
   contract: selective, threshold-gated updates (reversible by raising the
   threshold), no separate training run, tested at janitor scale (124M-1.5B).
   Caveat from the thread: TTT "does not massively reduce memory requirements
   compared to ssm". arXiv 2601.00894, code github.com/deveworld/ponderTTT.
   Verbatim: "PonderTTT uses the TTT layer's self-supervised reconstruction loss to
   decide when to update weights: high loss = struggling = UPDATE, low loss =
   confident = SKIP."

9. easycommand: 1.5B Qwen folded to gpt-4o-level bash on 400k synthetic examples
   https://www.reddit.com/r/LocalLLaMA/comments/1wybqq3/ (2026-10-05).
   Fully open: dataset (HF dirac-run/ec-training-data), GGUF models 1.5B and 0.6B,
   CLI. RQ4 evidence that a narrow behavioral fold from a fully synthetic controlled
   corpus carries a 1.5B to frontier-level on one task; no prompt-only baseline
   stated in the thread (OWED; the ten-minute-self falsifier still needs that arm).
   COORDINATION NOTE: a sibling seat's scratch (_ft2_easycommand.html, fetched
   15:48 local today) shows it is mid-read on the same artifact; if that seat banks
   it too, dedupe on the register. Verbatim: "Purely a hobby side project to see how
   far I can push a really small model, using (mostly) automated training pipelines."

10. Unsloth Studio vs LM Studio: the local lane is consolidating around one app
    https://www.reddit.com/r/LocalLLaMA/comments/1wnrh76/ (2026-09-23, 123 comments;
    100 read). Community migration LM Studio to Unsloth Studio: chat router plus
    LoRA training plus quantization/export in one local app; LM Studio exit reasons
    are RAM bloat and update cadence; Unsloth Studio complaints are its persisting
    sandbox and context management. RQ1/RQ5 signal: for a 1-8B local adaptation
    lane the de-facto integrated stack is Unsloth (train, quantize, serve), while
    trl/verl stay the scripted-lane picks; nothing here displaces the W-queue
    verdict in the 01:57 section. Verbatim (top comment, psychohistorian8): "I
    stopped using LM Studio because of how much RAM it was sucking up. Unsloth does
    all the same things I need, and is leaner."

11. TensorSharp: LoRA adapters over GGUF served in a second engine
    https://www.reddit.com/r/LocalLLaMA/comments/1wr0p3n/ (2026-09-26).
    C#/.NET local inference engine running Qwen-Image 2.1 GGUF with its LoRA
    adapters (about 12 GB VRAM with LoRA; RTX 3080 16GB / M5 Pro 48GB test rigs),
    author-maintained adapter configs incl. DoRA and accelerated (8-step/6-pass)
    adapters, honestly labeled. RQ2-adjacent: LoRA-over-GGUF is not llama.cpp-only;
    adapter serving is a multi-engine skill, which matters when the estate tests
    whether banked adapter laws transfer off their source stack. Verbatim: "Those
    are fewer model passes, not a claim of a measured end-to-end speedup on
    particular hardware."

## Not re-banked (verified held; this pass's dedup beyond the 01:57 list)

- 1x1bdvl LoRA over GGUF 40G VRAM: catalog 3 rows (frontier_olm_2026-10-09 sweep).
- 1wywscq MedGemma, 1wv05u1 Jeff router, 1wdjk0y AgileRL: banked by the 01:57 sweep
  of this file; catalog rows confirm.
- 1wuj70v magnitude self-tuning engine: read and rejected off-question by the 01:57
  sweep; unchanged.
- 1wr469w LoRA 11/90 vs 90/90: body [removed] again this pass (the title-law stays
  appealing for RQ2 but there is no readable body; do not bank titles).

## OWED (never asserted as done)

- easycommand blog (dirac.run/posts/easycommand) not fetched by this seat (sibling
  has it in flight); its prompt-only comparison arm unverified.
- 1wybqq3 comment tree (5 comments) not fetched (throttle).
- r/LocalLLM, r/ollama, r/MachineLearning unswept this pass.
- verl/trl acronym title queries 422-rejected by the archive door (systematic
  under-sampling, same as 01:57); no 2026 release threads for either surfaced.

Scratch receipts: corpus/tmp/as_sweep/ (lca_*.json keyword pulls, shortlist_posts.json
12-id batch, comments_1x0xkk7/1wujtbj/1wr0p3n/1wnrh76/1q5kokx.json, post_1x10r5t.json,
as_test.json).
