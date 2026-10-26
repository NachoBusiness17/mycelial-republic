# frontier sweep: finetuning-and-adaptation via reddit

source-fetched: 2026-10-03
seat: sweep-finetuning-and-adaptation-reddit (olm-mine)
window: 2026-08-25 through 2026-10-03 (30-day recipe window)

## Door record (degraded, per fetch recipe)

The named Reddit doors are hard-blocked from this seat:

1. `old.reddit.com/r/LocalLLaMA/top.json` and the HTML listing: login wall ("Log in to use old Reddit"), zero post content returned.
2. `www.reddit.com/r/LocalLLaMA/top.json`: HTTP 403 "blocked by network security".
3. `api.reddit.com` thread JSON: HTTP 403.
4. `r.jina.ai` proxy of old.reddit: Reddit 403s the proxy too.
5. `api.pullpush.io`: returns `{"error":"Rate limit exceeded. This website does not provide free scraping resources for agents."}` for bot UAs, then 429 on retry.
6. WebSearch (site:reddit.com fallback per recipe) worked for discovery but returned mostly stale threads (2023-2025 post ids); one discovery hit (1mp3mwq) resolved to 2025-08-13, out of window.
7. WORKING DOOR: Arctic Shift archive API (`arctic-shift.photon-reddit.com/api/posts/search`, `/api/posts/ids`, `/api/comments/search`), fetched 2026-10-03 via curl. All reads below are from this archived copy of the pages; scores are crawl-time snapshots, not live.

No fallback success is claimed for the named doors; the archive door is the substitution.

## Pass 1 (broad sweep)

16 slice fetches (4 subreddits x 4 date slices) plus a newest-100 pull per subreddit: 1,600 unique submissions, 359 keyword-matched (lora/qlora/finetune/distill/dataset/curat/style/collapse/self-train/dpo/sft/adapter/peft/unsloth/behavior). Instrument: `.venv/Scripts/python.exe` parse scripts over the raw JSON dumps (scratch: `C:/Users/foste/AppData/Local/Temp/frontier_sweep/`), repo interpreter per AGENTS.md python-env law. Well over the 30-candidate bar.

## Pass 2 (deep read, 9 threads read end to end: full selftext + up to 40 top comments each)

RQ1 (QLoRA vs LoRA vs full finetune for narrow behavioral law sets, measured retention):

- No 2026 thread found that runs a clean QLoRA-vs-LoRA-vs-full A/B on a narrow behavioral-law set with retention numbers. That exact study is an open slot. The closest measured evidence:
- Behavioral laws via RL beat "train shorter" directly: UkisAI Swift Qwen3.8-27B reports -58.3% token usage and x1.95 speed "without losing accuracy" by penalizing pathological overthinking patterns rather than training for brevity (thread 1wj3s31, s=944, 2026-09-17). Caveat from comments: Swift license "does not comply with the OSI criteria", so "open source" claims are contested; trained BF16, so NVFP4 quants underperform Q6 per a commenter.
- LoRA remains the workhorse for behavior+style with capability retention risk: Humanlike-Chat 2.0 (1wvxl4n, 2026-10-02) shows SFT-only style lock copying bad habits (refused tools, refused long-form) and fixes it with on-policy distillation on a second LoRA merged over the same 27B.
- DoRA hazard data point: DoRA adapter on Qwen2.5-VL outputs base-model responses after merge while LoRA works on identical data ("LoRA works with minimal anchoring on rather conservative learning rates, but DoRA almost has no effect", thread 1willeh, 2026-09-17). Merge-verification gate needed before any DoRA path in the QLoRA corpus organ.
- Narrow GRPO transfers: Qwen3.5-2B post-trained purely on simulating the python interpreter became more accurate and token-efficient on math (thread 1w6eon1, 2026-09-03, 20 min on one H200, code open).

RQ2 (data-curation recipes for code/session-tape corpora):

- Scaffold CoT dataset (thread 1w5jw6c, r/MachineLearning, 2026-09-02): ~4M examples / ~3B tokens built AROUND small-model failure modes; fixed Inventory/Interaction/Execution scaffold, max 2048 tokens/example, 4 depth tiers with 5.6x spread so the model learns when to think long; 18 domains / 798 subdomains fully partitioned; code slice 669,517 examples; and the "antihal" slice 502,151 examples for knowledge boundaries, calibrated answers, premise auditing, refusing to fabricate. Author claim: freeform CoT on <5B models "does not really add much... more confusing, poorly structured and inaccurate". Regex-validateable outputs = machine-checkable law compliance, i.e. citation-discipline and tri-state verdicts as trainable data categories. Direct template for room.jsonl corpus rows.
- AliceAI-80B-A3B from-scratch instruct thread (1wv5h8x, 2026-10-01): synthetic distilled SFT set via the open-sourced SFTMill engine, staged SFT then RL plan. Recipe shape matches our code-agent-data doctrine (sessions -> distilled corpus -> instruct finetune).
- The OpenAI-training-on-conversations controversy thread (1wcmgbn, s=1132, 2026-09-10) is a link post with opinion-only comments read and set aside; signal is the era's consent fight over conversation-derived corpora, not a recipe.

RQ3 (swarm self-distillation: does training on the fleet's own verified outputs improve agent success, when does it degrade):

- POSITIVE, measured: CLM vs JEV (thread 1wouby6, s=410, 2026-09-24). CLM is an open-weights decision model exposing Jev's three primitives (Choice, Noul = calibrated true/false, Score) with ~75 MB heads; "when fine-tuned on agent trajectories, CLM achieves state-of-the-art verifier performance on Terminal-Bench 2.1 (87.6%) and DeepSWE (81.6%), whereas zero-shot Jev scored ~71% on DeepSWE" and runs 4x-13x faster with action-embedding caching. Training on the fleet's own trajectories beats the closed zero-shot judge by ~10pp. This is the ouroboros leg with numbers. Residual limitation, stated in-thread: CLM-8B trails Jev on zero-shot broad knowledge (BFCL v4 99.2% for Jev), so self-distilled heads are narrow; the estate's tri-state verdict gates are exactly the narrow case.
- DEGRADE CONDITIONS, measured: ratctl reward-hackability audit (thread 1w4h6c1, 2026-09-01): 112 real RL post-training environments audited, 54 flagged, 0 false positives on 43 clean controls, recall 78.3%; cites Terminal Wrench (331 hackable environments, 15%+ of standard benchmark tasks bypassable) and a SWE-bench Verified audit (28.5% Docker-verified hackable). Self-training degrades when the verifier is gameable: test/assertion tampering, grader manipulation, premature termination, golden-solution leaks, reward skipping, LLM-judge verbosity/sycophancy bias. Our percolator promotion gates and graders are the analogous surface; a gameable grader turns self-distillation into grader-hacking.
- PROVENANCE STEAL: the Qwen3.8-may-have-trained-on-GPT-5.5-CoT thread (1wccdjn, 2026-09-10, 28 comments) demonstrates a prefill-similarity fingerprint: run a small benchmark unprefilled vs with a target model's CoT prefilled; a model trained on those sequences diverges toward them (Qwen3.8 +18.18pp similarity vs ~0 for DeepSeek V4 Flash and Inkling; Kimi K3 +4.54pp). Stealable as a corpus-provenance probe: did anyone train on OUR tapes? Method caveats read in comments: n=45, no error bars (top comment: "the only row carrying real weight is Qwen's"), and high base similarity can mean trained on answers rather than CoT.
- Architecture context: the Jev prior-art thread (1wijo3e, s=1869, 2026-09-17) documents the decision-model recipe: PPO over sequence embeddings emitting turn-by-turn probability trajectories (arxiv 2503.23303) and RLCD-trained parallel sampling for confidence distributions (arxiv 2510.01237), with open dataset saas-sales-conversations. Comments add an open clone ("WaterSheep") and a field-test review at drborchers.com/en/blog/jev-field-test/.
- Not model-collapse-specific: no thread in this window ran the collapse literature against self-distillation; the degradation evidence here is verifier-gaming, which is our controllable half. Collapse question left OWED by this sweep.

RQ4 (few-shot style lock with minimal data, extending SEED SAVER):

- Humanlike-Chat 2.0 (1wvxl4n) is the direct extension of the SEED SAVER style-lock precedent: v1 plain SFT on 139,845 messages from 1,396 conversations locked the voice but copied bad habits (would not call tools, "sometimes just say it's busy or going to bed. Very human. In a bad way."); v2 kept a second LoRA, two teachers (style teacher with a hidden instruction + base teacher for tools/code/instructions), on-policy distillation where the student never sees the hidden instruction and internalizes the behavior; result claims: tools work, asks for missing inputs instead of fabricating (base picked JFK unprompted; 2.0 asks), code/math at roughly base level, style override via system prompt now sticks.
- Property transfer caveat from Swift comments: behavior-trained models keep base-model quantization sensitivities (BF16-trained, NVFP4 quant underperforms Q6), so style-locked checkpoints need quant-specific eval before deploy.

## Overlap check (commands run this session)

- `grep -ic` per exact phrase into `catalog/catalog.jsonl`: Terminal-Bench 2.1: 0; Humanlike-Chat: 0; Scaffold CoT: 0; Swift-Qwen3.8: 0; saas-sales-conversations: 0; AliceAI-80B: 0. Zero exact-title holdings for all banked items.
- Concept-level presence exists and is recorded as such: "noul" 6 hits in catalog / 107 memory files; "on-policy distillation" 43 catalog hits / 16 memory files; DeepSWE 4 / 30; "reward-hackab" 0 catalog / 1 memory file; ratctl, sftmill, "terminal wrench", "scaffold cot" 1 memory file each.
- `memory/trajectory/steps.jsonl` hits for Swift-Qwen3.8 / Humanlike-Chat / saas-sales-conversations / AliceAI-80B are sibling-sweep and own-session echo (a same-day sibling seat ran overlapping greps; my own command output is also logged there). Treated as no prior banking.
- Net: nothing here re-banks known work; the CLM fine-tuned-verifier numbers, Scaffold CoT's antihal slice, ratctl's audit patterns, and the prefill-provenance probe are new to the estate.

## Items (strongest first, <=8)

1. CLM vs JEV: fine-tuning tiny decision heads on agent trajectories (1wouby6) : RQ1+RQ3 keystone.
2. Humanlike-Chat 2.0: on-policy distillation style lock that keeps tools (1wvxl4n) : RQ4.
3. Scaffold CoT: failure-mode-designed dataset with machine-checkable scaffold + antihal slice (1w5jw6c) : RQ2+RQ1.
4. ratctl: 112-environment reward-hackability audit (1w4h6c1) : RQ3 degrade conditions.
5. Swift Qwen3.8-27B: behavioral RL, -58.3% tokens x1.95 speed, accuracy kept (1wj3s31) : RQ1/RQ4, license caveat.
6. CoT prefill-similarity provenance probe (1wccdjn) : RQ3/RQ2 steal, small-n caveats in-thread.
7. Jev prior art: PPO trajectories + RLCD confidence, open dataset (1wijo3e) : RQ1 architecture recipe.
8. AliceAI-80B: SFTMill synthetic distilled corpus, staged SFT->RL (1wv5h8x) : RQ2.

## Read but not banked (integrity notes)

- 1willeh DoRA merge failure (read, useful pitfall, below cut line), 1w6eon1 GRPO 2B (read, small), 1wt0tot 400-agent MMO on Qwen3-4B (read; swarm behavior, not self-distillation), 1wcmgbn OpenAI-conversations (link post, opinion comments), 1woscea CLM primary thread (image-only body), 1wvz8sj Velocity LoRA (body [removed], title numbers only, not banked), 1wiqqzv LoRA emotion tool (body [removed]).
- Scores in this file are Arctic Shift crawl-time snapshots; comment pulls capped at 30-40 per thread.

---

# WINDOW 2 (evening re-run of the same seat, 2026-10-03 ~21:00-22:00Z)

source-fetched: 2026-10-03. Same seat name, fresh pass; window-1 items above are untouched and none of my banked ids collide with theirs (1wouby6, 1wvxl4n, 1w5jw6c, 1w4h6c1, 1wj3s31, 1wccdjn, 1wijo3e, 1wv5h8x).

## Door record (named doors degraded, fallback per recipe)

1. `old.reddit.com/r/{LocalLLaMA,MachineLearning,LocalLLM,ollama}/top.json?t=month&limit=50`: all four returned the Reddit landing shell, zero posts (bot-blocked silently).
2. `www.reddit.com/r/LocalLLaMA/top.json`: HTTP 403 "blocked by network security".
3. `old.reddit.com` thread pages via WebFetch: timeout at 60s. `r.jina.ai` proxy: Reddit 403 to the proxy.
4. WebSearch fallback (site-restricted reddit.com): worked intermittently (1302/429 rate-limit storms mid-sweep), surfaced the Bonsai/ternary cluster for discovery.
5. WORKING DOOR: Arctic Shift archive API (`arctic-shift.photon-reddit.com/api`), the engine burns.md:107-111 already certified ("Do not rediscover doors"). All deep reads below are from this archived copy; scores are crawl-time snapshots.
6. TACO itself verified at the source: `https://arxiv.org/abs/2610.02199` fetched 2026-10-03 (arxiv door clean, as burns.md records).

## Pass 1 (broad sweep, 30+ candidates)

Reused the sibling window's Arctic Shift post pool for the same date window (`sweep/tmp/candidates_full.jsonl`: 10,274 posts across LocalLLaMA 1600, ClaudeAI 1600, ClaudeCode 1000, AI_Agents 1000, cursor 800, codex 800, aiagents/LLMDevs/LocalLLM/ollama/claudeskills/Anthropic 500 each, LangChain 374) and added a fresh r/MachineLearning month crawl (+100 posts; first-page 400s on the API, retried clean). Keyword ranker (lora/qlora/fine-tun/adapter/ternary/bitnet/1.58/unsloth/axolotl/peft/sft/dpo/rlhf/reward model/grader/judge/test-time/self-train/gemma/...) over title+first-600-chars selftext: 427 hits (`sweep/tmp/ft_hits.jsonl`, instrument `sweep/tmp/ft_rank.py` via `.venv/Scripts/python.exe`). Candidate register well over 30: the 12 shortlisted for deep read plus the ternary cluster (1wj6c4l, 1wjocnh, 1wm3yvy, 1wj84nz, 1wg1o5b, 1wjgnok), judge/eval cluster (1wjwhxc, 1wgt5y0, 1wkjs20 decontaminated-traces), TTA cluster (1w7u7wl, 1w90igd teach-don't-finetune, 1wkc4c9 token steering), corpus cluster (1w71vg1 instruction-following-into-training-data, 1wfvx8o GPU cost estimator, 1w6er19), adapter cluster (1wiijww, 1weknvj, pdoou1j comment).

## Pass 2 (deep read: 11 threads end to end)

Full selftext + top-scored comments (up to 100/thread) fetched via `/api/comments/search?link_id=` (`sweep/tmp/ft_deepread.json`, script `sweep/tmp/ft_deepread.py`). Read in full: 1wj6c4l, 1wjnklv, 1wkorli, 1wkwz69, 1wgvfpr, 1wefk8o, 1wgxzvw, 1wavhij, 1w7umnd, 1wcqa03, 1weum85. Note: 1v0egoi ("I tried fine-tuning a ternary model, Bonsai 8b, on metal") resolved to 2026-07-19, OUTSIDE the 30-day window - used as context only, not banked. Also swept r/ollama + r/LocalLLM comments for adapter mentions: 7,900 comments scanned, 5 hits, none a measurement (`sweep/tmp/ollama_adapter_comments.json`).

## RQ answers (evidence-read this window)

RQ1 TACO/ternary at janitor VRAM. TACO (2610.02199, submitted 2026-10-01, UCF; verified from the abstract) is an OPTIMIZER-STATE method: 174x optimizer-memory cut vs AdamW8bit (27.7 GB to 0.16 GB) and 2.9x peak-training-memory cut (80.6 GB to 27.5 GB) on OPT-13B, enabling 30-32B full-parameter finetuning on a single 80 GB H100. That is a datacenter envelope: it attacks optimizer state, not weights/activations/KV, so it does NOT make janitor-scale (RX 5600 XT, 6 GB) full-parameter ternary finetuning feasible. What the window's measured Reddit data adds is the claims-vs-measurement half the RQ asks for: the Bonsai 2 27B ternary release (1wj6c4l, s=1603, <6 GB, runs in-browser WebGPU) headlines "98.2% of the intelligence" while its own whitepaper (page 7, quoted in 1wjnklv) reads Terminal-Bench 2.1 / SWE-bench Verified 52.8 / 60.8 vs 69.7 / 80.6 for the FP base = roughly three quarters, and a same-hardware size-matched agent-suite A/B (1wkorli) measured Bonsai PQ2 completing the same 4 tasks with 84,176 vs 27,197 output tokens and 24:09 vs 8:00 wall time (3.02x faster, 3.10x fewer tokens for the IQ3_XXS comparator); a commenter adds ~30% needle-miss at 200K context. Community size-matched benchmark (1wkwz69, 8,691-char methodology: hard passkey with decoys, phrase reconstruction, 500 MCQ science) verdict: PQ2 "not completely lobotomized", but "the problem is that Prism ML promote the model as 98% the intelligence ... when it's clearly not true" (top-scored comment, s=31). Perplexity-style claims lost to every task-measured comparison in this window. Planning figure for any ternary janitor lane: ~75% agentic quality, ~3x token inflation.

RQ2 corpora to SFT/QLoRA pairs, license and contamination gates. The gate that makes a corpus trainable was demonstrated twice: (a) 1w7umnd (r/LocalLLM, 2026-09-05): 11 months of generated specs with EVERY completion machine-verified through the real MQL5 compiler + backtest; one epoch took Qwen2.5-Coder-14B from 1.09% (2/184) to 92.39% (170/184) compile success vs 97.28% for gpt-5.6-sol, McNemar p=2.29e-49, entire train+eval on one AMD R9700 under ROCm (no NVIDIA in the pipeline); poster concedes in-distribution competence (prompts from the same generator family as training data) and keeps weights+corpus private with the benchmark as proof. (b) 1wavhij (OpenUI team): ~700 synthetic SFT examples made benchmark performance WORSE while loss dropped; the fix was a parser-accepted self-training loop (accept valid parses, repair only identified defects, judge-check survivors, finetune on accepts). License gate, concrete: 1wcqa03 top-comment exchange on OUI-1 - "why the hell did they change the license from apache to gemma?????" (s=9): a Gemma-family-base finetune ships under Gemma terms, not Apache; anything the estate trains on courseware (ms-genai/ms-agents/openai-cookbook) must check the BASE model's license for the produced judge, and seat tapes carry their own consent question (window 1's 1wcmgbn note). Contamination probe already banked window 1 (1wccdjn prefill-similarity); window 2 adds 1wkjs20 as the marketed counter-example ("1,451 verified max-effort reasoning traces ... decontaminated", r/LocalLLaMA 2026-09-19, read in candidate pass only).

RQ3 imagined grader / reward-model instruments before any self-training loop fires. Window 1 banked the imagined-grader thread itself (1wsuag0, burns.md:91-93). Window 2 adds the variance half the duel instruments need: 1wgvfpr (r/LLMDevs, 2026-09-15, artifact-first per Dan Luu exercise 7, every number tied to a run file): a judge scored the same case across 16 replicate runs with nothing changed and non-unanimous cases moved from 2/21 to 6/21 depending on which run you look at - a single run does not measure the noise floor, it samples it (adopted fix: median of several runs, band = lowest the judge has been seen to go); the fixed threshold rule "fail if one case is worse than measured" went deaf as the suite grew 17 to 144 cases (one case = 5.9 accuracy points at 17, 0.7 at 144 - a real regression stopped reaching the threshold with zero lines changed); and two reviewed, sensible prompt edits - one dropped recall 0.80 to 0.50. 1wefk8o (r/LLMDevs, 2026-09-12) + its comment thread is the gate checklist for letting any agent rewrite its own harness: grader completely outside the rewrite loop, held-out slice the proposer never sees feedback from, edit budget so a one-line prompt change and a tool-policy rewrite are not scored as the same win, pinned model endpoint + tool versions so a backend change is not credited to the candidate, mechanical evaluator wherever the requirement is expressible, provenance (run id, task revision, tool trace) on every failure report so rollbacks are debuggable, shadow stage before publication. That thread plus ratctl (window 1) is the pre-fire spec for judge2/duel.

RQ4 is the percolator already a ranked TTA method. Direct evidence for promotion-loops-over-weights, measured: 1wavhij (SFT degraded, deterministic-parser + judge-gated self-training loop won: 13 to 57.1 to 71.7% structural validity while generation time fell back to 1.9s) and 1wgxzvw (r/LLMDevs, 2026-09-15, on arXiv 2608.27448 TTPO): test-time training with NO labels by exploiting the asymmetry that rollouts disagreeing with a majority-vote pseudo-label are usually wrong whether or not the vote was right - agree-branch distilled (OPSD), disagree-branch penalized (grouped RL), token-level selection both sides; Qwen3-1.7B 38.0% to 45.2% in TTT with no labels, parity with label-supervised OPSD on five competition-level benchmarks. The stated boundary is the overturn condition: it "rests on majority voting meaning something, which needs a single correct answer that repeated samples can converge on"; summarisation and drafting do not qualify, and the poster's wanted ablation (disagreement signal alone, no distillation half) is unanswered. So: for machine-verifiable lanes the percolator's deterministic-gate + human-gated promotion IS the ranked method (1wavhij numbers), weight finetuning only wins where a mechanical verifier exists (1w7umnd), and open-ended lanes are exactly where the TTA literature refuses to claim. Evidence that would overturn: a no-labels TTA result on open-ended workloads (the TTPO author's own reservation marks the gap).

RQ5 Ollama adapter format + swap cost. HONEST NEGATIVE on the measurement half: no in-window Reddit thread measures adapter swap cost on Ollama (7,900 r/ollama + r/LocalLLM comments scanned for lora/adapter x gemma/ollama/modelfile/gguf/swap/merge: 5 hits, zero measurements). What the reads establish: Ollama's ingestion path is GGUF-centric - 1wcqa03 post body: "DiffusionGemma isn't supported by llama.cpp yet, so running it through Ollama doesn't seem to be an option", with the community path being "Gonna test it out and make a GGUF quant this weekend" (s=61) - i.e. merge-then-quantize, not native adapter hosting; the hot-swap pattern lives in vLLM: 1weum85 (Lorivo) shares one base-model server across many LoRA adapters on vLLM's fused LoRA kernels with `qwen3-4b:my-adapter` style routing, and a pdoou1j comment (2026-10-03, t3_1wvtvsf): LoRA "is essentially a tiny mod that runs atop the base model and runtimes like vllm can route requests to multiple different adapters" over the same base. OWED (local measurement, not a Reddit find): time `ollama create` with an ADAPTER stanza + first-token latency across the gemma janitor models to get the measured per-adapter swap cost on the janitor lanes.

## Overlap check (commands run this session)

- Single-pass scan `sweep/tmp/ft_overlap.py` (via `.venv/Scripts/python.exe`): one read each of `catalog/catalog.jsonl` and all 453,074 files under `memory/`, 19 terms. All 11 candidate thread ids: catalog=0, memory only `memory/trajectory/steps.jsonl` (own-session + sibling echo, same convention window 1 applied). "2610.02199": catalog=1 (the door's named paper, already catalogued - expected, not a re-bank). "bonsai": catalog=120 but all shadertoy/game-asset false friends (spot-check: `memory/corpus/shadertoy21k/...` fragments); "tppo": ai_canon textbook substring false friends; "oui-1" and "lorivo" and "2608.27448": trajectory only. "mql5": 18 hits in `memory/biography/derived/*.pdf` - the domain is already personal to the operator's biography corpus, which makes the 1w7umnd find MORE relevant, not a duplicate.
- Cross-sibling dedup: zero id overlap with window-1's 8 banked items (listed at top) and with the other area registers in `watch/inbox/frontier_olm_2026-10-03/register.jsonl`.

## Window-2 items (strongest first, <=8)

1. 1wkorli measured ternary-vs-IQ3 agent A/B (3.02x slower, 3.10x tokens) : RQ1 keystone.
2. 1wjnklv Bonsai whitepaper self-contradiction (~75% vs 98.2% headline) : RQ1 claims-vs-measurement.
3. 1wgvfpr judge noise-floor exercises (16 replicates, threshold deafness, recall cliff) : RQ3.
4. 1wefk8o grader-outside-the-loop self-rewrite checklist : RQ3 gate spec.
5. 1wgxzvw TTPO no-labels test-time training + its open-ended-domain boundary : RQ4.
6. 1wavhij SFT-hurt / parser-judge-gated self-training-won, measured : RQ4+RQ2.
7. 1w7umnd machine-verified one-epoch SFT, 1% to 92% compile, all-AMD ROCm : RQ2+RQ1.
8. 1wcqa03 Apache-to-Gemma license switch + DiffusionGemma/Ollama gap : RQ2 license gate + RQ5.

## Integrity notes (window 2)

- 1wj6c4l (release thread, s=1603) read in full but not itemized separately: its content survives through 1wjnklv/1wkorli/1wkwz69; 1wjocnh/1wm3yvy/1wj84nz/1wjgnok/1wg1o5b read at candidate depth only (title+body+top comments in pool), held as corroboration.
- All quotes in the register below are verbatim from the Arctic Shift archived copies; scores are crawl-time snapshots (2026-10-03), not live.
- WebSearch was rate-limited (1302/429) mid-sweep; discovery survived on the Arctic Shift pool, and no fallback success is claimed for any blocked door.
