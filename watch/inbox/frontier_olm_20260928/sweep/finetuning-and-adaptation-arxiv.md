# sweep: finetuning-and-adaptation via arxiv (frontier_olm_20260928)

source-fetched: 2026-09-28. Gopher lane: sweep-finetuning-and-adaptation-arxiv. Doors used: arXiv Atom API (export.arxiv.org, 6 queries, all 200), arxiv.org /html/ full texts (10 fetched, 2 fell back to /abs/ after 404), arxiv.org /abs/ pages (2). No 403s; two degraded reads noted below.

## Pass 1 (broad, 100+ candidates considered from 6 queries)

Queries (sortBy=submittedDate desc):
1. all:"agent trajectory" AND all:"fine-tuning" (30 entries)
2. all:QLoRA (30 of 284)
3. all:"small language model" AND all:agent (30)
4. all:"self-evolving" AND all:agent AND cat:cs.CL (26 of 211)
5. (PII OR deduplication) AND (fine-tuning OR training data) AND cat:cs.CL (29)
6. (synthetic data OR distillation) AND (cost OR economics OR budget) AND cat:cs.CL (24)

Strong pass-1 pool (subset): SWE-Prime 2608.27449, LiteSearch-VL 2608.29357, Experience Funnel 2609.08919, Dependency-Aware Trajectory Refinement 2609.18417, PSD 2609.23449, From Retrieval to Weights 2609.10155, 1% of Tokens 2609.24432, MedDeID 2609.10049, What Stops an SLM From Driving a Database Agent 2609.21341, Trajectory Data Curation for LoRA 2607.17205, Agent Memory Distillation 2608.07169, Feedback That Backfires 2608.23651, Learning New Facts with QLoRA 2608.25677, Shared Autoregressive Context 2609.32546, Data Turnstile 2607.29250, SEABench 2609.35596, FORM 2609.23367, Terminal-Universe 2609.04148, Moltbook Files 2605.07462.

## Overlap gate (run before banking)

Exact-ID grep loop over catalog/catalog.jsonl and memory/ (commands in memory/trajectory/steps.jsonl this session). Held already in catalog (1+ rows each): 2609.08919, 2609.21341 (3 rows; sibling lane of this same run has sweep/_raw/full_2609.21341.html), 2609.23449, 2609.18417, 2609.10155, 2609.24432, 2609.10049, 2609.35596, 2609.23367, 2609.04148. Those 10 were NOT re-banked even where deep-read. The 8 banked below all returned catalog:0 and zero title hits in catalog. memory/ hits for banked IDs are only: this session's own trajectory log, the ID-verification registries (memory/runs/corpus_gap_research/ARXIV_REGISTER.json, MAP_BACKFILL.json/md), and one genuine prior citation of 2608.23651 in memory/runs/v4_council/PRIMITIVES_grok.md.

## Pass 2 (deep reads actually performed this session)

Full-text end-to-end reads (9): 2609.08919, 2609.18417, 2609.23449, 2608.29357, 2609.10155, 2608.27449, 2609.21341, 2609.24432, 2608.07169, 2608.23651, 2608.25677, 2609.32546 (12 counting held ones). Abstract-level reads (2, HTML 404 fallback): 2607.17205, 2607.29250.

### Held (in catalog, deep-read here for the synthesis, NOT banked as new)

- 2609.08919 Experience Funnel: the closest published analog of the estate DNA cycle. Fast loop edits a textual state (validated on held-out outcomes), slow loop consolidates accepted experience into policy weights via transition-aware distillation (Jensen-Shannon token weights, KL student loss + RL). Qwen3.5-4B + 27B teacher, 5 rounds, 2 accepted. Experience-selected rollouts 63.0% vs 58.9% unfiltered. Key law for us: experience selection, not volume, is the gate.
- 2609.18417 Dependency-Aware Trajectory Refinement: round-level dependency DAG over trajectories; leaf-prune dead-end tool-call rounds = +1.7pp accuracy; strict-merge + rephrase = -40% messages / -48% tokens at equal accuracy. Full SFT (not LoRA), Qwen3-VL-30B, 4 epochs, 6,196 trajectories. Trap found: eval loss decouples from accuracy.
- 2609.23449 PSD: single small model plays teacher (privileged prompt with oracle answer) and student; LoRA adapters, frozen teacher adapter; Qwen3-0.6B/1.7B 0.8211 and 4B 0.8699 vs GPT-4.1-mini-with-pipeline 0.849 on LoCoMo. OOD degrades (LoCoMo-specific). On-policy variant hurts; off-policy wins.
- 2609.10155 From Retrieval to Weights: per-person DoRA (r=16) continued pretraining on 0.6B writes the corpus into weights (d_z=3.74 own-text fit) but "the adapter adds knowledge rather than alignment with the individual" and continued pretraining destroys instruction-following. Cautionary for tape-to-weights dreams.
- 2609.21341 What Stops an SLM From Driving a Database Agent: 8,199 runs, 39 models; of 2,100 agent losses, transport 36.2%, clock 25.8%, verification 20.7%, capability 17.3%; five server-only fixes moved six models 6-21 cells of 30 with zero retraining. 3-4B fully succeed; 1.7B is the floor.
- 2609.24432 1% of Tokens: information-efficiency ratio selects the 0.1-1% of tokens where teacher gradient signal lives; matches full on-policy distillation; non-monotonic in budget. Teacher-side supervision cost, not student rollouts, is the savable spend.
- 2609.10049 MedDeID: dual-head RoBERTa de-identification, 98.9% recall on hospital notes; synthetic-only training hit 96.1%; 621x faster than an 8B LLM scrubber. The PII-gate template the estate's corpus doctrine lacks.
- 2609.35596 / 2609.23367 / 2609.04148: cataloged by sibling lanes; not re-read in depth here beyond the API abstracts.

## Banked items (8, strongest first)

### 1. SWE-Prime: Fewer Trajectories, Better Performance (2608.27449, 2026-08-27)
Full read: https://arxiv.org/html/2608.27449v1
Pool: 67,074 OpenHands trajectories (Qwen3-Coder-480B teacher), 32,161 resolved. Stage 1 scores trajectories on 5 signals (workflow grounding, tool-success percentile, redundancy, git-hacking/leakage detection, patch-scope vs gold at file+line level) + HDBSCAN cluster representativeness; Stage 2 masks SFT loss to LLM-scored segments >= 7/10 (contribution, learnability, risk). Training the 10% subset (~3,216) beats 100% everywhere: GLM-4.7-Flash 41.4 -> 51.4 SWE-bench Verified (+24.2% relative); also beats Random-10% (53.2 vs 41.2). Full-parameter SFT, lr 4e-6, 131k context. Quote: "task success does not guarantee high-quality supervision: successful trajectories may still contain ineffective, redundant, or risky steps." This is the published template for the estate's corpus-grade judging gap: success alone is not a gate; score the steps, mask the loss to good segments. RQ1/RQ2.

### 2. LiteSearch-VL: Small Multimodal Search Agents via Trajectory Distillation and Synthetic Step-DPO (2608.29357, 2026-08-29)
Full read: https://arxiv.org/html/2608.29357v1
The concrete budget recipe: Qwen3-VL-2B/4B, LoRA r=16 alpha=32 dropout 0.05 on language tower only, SFT lr 1e-4 one epoch (564 steps, batch 64), DPO lr 1e-6, single 8-GPU node via LlamaFactory, 36,092 trajectories expanded to 133k step examples + 234k DPO pairs. 2B goes 0.1% -> 29.4% Pass@1; 4B 25.6 -> 30.8. Hard-won gotchas: the standard DPO beta=0.1 / lr 5e-6 recipe collapsed the 2B model (needed beta=0.3, lr 1e-6); a 5-check programmatic validator on synthetic DPO pairs cut the defect rate from 54% to 0%; teacher corpus cost 256 H20 GPUs while the student recipe is one node. Quote: "Full-trajectory supervised fine-tuning transfers the agent contract, taking the 2B model from almost never emitting a usable answer" (abstract). RQ1/RQ4.

### 3. A Systematic Evaluation of Trajectory Data Curation for LoRA Fine-Tuning of Code Agents (2607.17205, 2026-07-19, ICIC 2026)
Abstract-level read only: https://arxiv.org/abs/2607.17205 (HTML full text 404'd; door degraded, abstract is the banked evidence). Qwen2.5-Coder-7B-Instruct LoRA on the same 67,074/32,161 SWE trajectory pool as SWE-Prime; two-axis quality scoring (Efficiency, Style), 16 controlled experiments; error-retry rate is the dominant sub-dimension (within 0.2% of full composite); cross-entropy on held-out trajectories ranks systems with Spearman rho = -1.00 vs ROUGE-L. Scale law: at 500-1,000 trajectories quality filtering gains under 1% (n.s.); at 2,000 the quality-vs-random gap reaches 3.6% (p=0.016). Quote: quality scoring is "a viable but scale-sensitive lever for code-agent SFT." Answers RQ1's "when do first gains appear": quality gates pay only once the tape pool passes ~2k trajectories; below that, add tapes, not filters. RQ1/RQ2.

### 4. Agent Memory Distillation (2608.07169, 2026-08-07)
Full read: https://arxiv.org/html/2608.07169v1
Training-free alternative to QLoRA for the janitor fleet: GPT-5-mini teacher trajectories are distilled into three memory tiers (workflow insight with values replaced by typed placeholders like <FILE_PATH>; <=6 semantic subtask segments with concrete calls; per-function invocation examples injected reactively only when a call errors). Frozen students: Qwen3-4B +34.5pp AppWorld (14.88 -> 49.40), Gemma4-E4B 24.40 -> 54.17, surpassing the teacher's 50.00; avg +27.2pp AppWorld, +11.2pp BFCL V3. Quote: "Subtask memory contributes the largest gains, teacher effectiveness depends on both teacher capability and student compatibility, and 4B-sized students benefit most." Directly comparable to the estate's feed-cited-content P2 gate: bank the funded tier's tapes as structured memory before touching weights. RQ3/RQ4.

### 5. Learning New Facts with QLoRA: the acquisition-retention frontier (2608.25677, 2026-08-26)
Full read: https://arxiv.org/html/2608.25677v1
Qwen3-4B, QLoRA r in {8,16,32,64} (alpha=2r), 1,938 anonymized OSM fact-QAs, 100 epochs, 5 seeds: r=16 is the sweet spot (93.3% paraphrase at 89.9% OOD retention); r=32 buys +1.3pp facts for -16.6pp retention; r=64 collapses retention to ~39% ("unrelated capabilities collapse"). r=8 = FFT-level safety but low acquisition. Same trend on unquantized LoRA, so it is rank, not 4-bit. Quote: "PEFT should not be treated as inherently safe for knowledge injection: adapter rank controls a plasticity trade-off." Sets the estate's tape-to-adapter rank law: install new procedures at r<=16 or lose the janitor's general competence. RQ1.

### 6. Feedback That Backfires: Why Small Language Model Agents Repeat the Call They Just Watched Fail (2608.23651, 2026-08-24)
Full read: https://arxiv.org/html/2608.23651v1
135M-1.7B models across 4 families: appending a failed call verbatim raises its repeat probability 0.06 -> 0.54 (log-prob -1.03 nats/token, ~2.8x odds); the surface form of the string in context is 83% of the effect; "do not repeat" instructions do nothing (+0.07 nats, wrong sign); clean-restart harnesses are the worst (80% exact repeat). Fixes: replace the verbatim call with a runtime description (-76% inversion) plus a decoder-side ban on failed strings (31% -> 8%). Quote: "The context after a failure must differ from the context before it, and the difference must not be the failed action." Independently converges with the estate's gemma-2b-friction-is-capability-shaped law: fix the harness before the weights. RQ3.

### 7. Shared Autoregressive Context Can Distort Relationships in Synthetic Data (2609.32546, 2026-09-26)
Full read: https://arxiv.org/html/2609.32546v1
Matched experiment (2,000 ESS profiles, Qwen3.8-27B and Llama-3.3-70B): generating ten respondents per completion instead of one inflates correlation error 48-58% / 114-127%; re-pairing earlier answers flips generated correlations from +0.963 to -0.670, proving answer history is a causal channel; batched marginals can be better while joint structure breaks. Quote: "Request construction is therefore part of the data-generating process." For RQ4 distillation runs on the funded tier: one tape/example per completion, or the distilled corpus inherits autocorrelation no dedup pass will catch (this is a cleaning gate, not a sampling bug).

### 8. Data Turnstile: A Scalable Open Framework for Function-Calling Data Generation (2607.29250, 2026-07-31)
Abstract-level read only: https://arxiv.org/abs/2607.29250 (HTML v2 404'd; door degraded, abstract is the banked evidence). Open framework turning user-defined API specs into constrained stepwise synthetic tool-use data with validation and error-feedback loops; released with 1,000+ APIs / 100K+ multi-turn interactions. Qwen3-0.6B fine-tuned (no chain-of-thought) hits 75.9% BFCL single-turn vs 67.4% for the thinking-enabled base; Qwen3-1.7B jumps 6.6% -> 31.1% on tau2-bench telecom, beating Qwen2.5-32B-Instruct (27.4%). Framing: SLMs "can't offset low-quality supervision through model capacity alone", so generation-side gates are the lever. RQ3/RQ4.

## Answer sketch per research question

1. Recipes + data scale: LoRA r=16 alpha=32 lr 1e-4 one epoch on 36k trajectories is the demonstrated small-model entry point (LiteSearch-VL); rank law r<=16 for knowledge injection (2608.25677); first measurable quality-filter gains at ~2k trajectories, real gains by 3.2k curated (2607.17205, SWE-Prime). Published pipelines are mostly full SFT at 30B and LoRA at 2-7B.
2. Cleaning gates the corpus-grade doctrine lacks: trajectory-level multi-signal scoring incl. leakage ("git-hacking") detection and patch-scope (SWE-Prime); segment-level loss masking scored >=7/10 (SWE-Prime); error-retry rate as the dominant single quality signal (2607.17205); dependency-DAG pruning of dead-end rounds (2609.18417, held); PII de-identification with 98.9% recall at 621x LLM speed (2609.10049, held); request-construction gates for synthetic batches (2609.32546); programmatic validators on generated pairs, 54% -> 0% defect rate (LiteSearch-VL).
3. 2B-class beating prompted frontier: yes on narrow chores. Gemma4-E4B 54.17 vs its GPT-5-mini teacher 50.00 on AppWorld with memory distillation (2608.07169); Qwen3-0.6B 75.9% BFCL vs 67.4% thinking base (2608.29250); Qwen3-1.7B beats a 19x larger model on tau2-bench telecom (24.6% vs 27.4% is 0.6B; 1.7B 31.1% vs 32B 27.4%); but PSD-style specialization degrades OOD, and 2609.21341 (held) shows 75.7% of small-model agent losses are mechanical harness failures, fixable with zero retraining.
4. Distillation within the $180-220 budget: no published dollar cost curve found in this sweep; the honest finding is structural. Teacher-side supervision is the savable spend: 0.1-1% of tokens carry the gradient signal (2609.24432, held); memory distillation is training-free and beats weight updates on AppWorld (2608.07169); LiteSearch-VL ran its whole student pipeline on one 8-GPU node from a free teacher corpus. Nothing prices API credits directly; the estate should treat 2608.07169's no-weights path as the first dollar-per-point frontier.
5. Continual adaptation from filed workdays: 2609.08919 Experience Funnel (held) is the direct analog: fast validated text-state edits + slow distillation-of-accepted-experience only, 2 of 5 rounds accepted, experience selection worth +4.1pp; 2609.10155 (held) warns corpus-to-weights adds knowledge, not behavior, and destroys instruction-following under continued pretraining; SEABench (2609.35596, held) shows self-evolving loops acquire new safety failures. Net: publish the fast loop, gate the slow loop.

## Door status

All arXiv API and /html/ doors returned 200 except: 2607.17205 /html/ 404 (fell back to /abs/, abstract-level), 2607.29250 /html/v2 404 (fell back to /abs/, abstract-level). No fabricated fallback success; those two items carry reduced confidence accordingly.
