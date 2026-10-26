# r-selfplay-sota: R-Zero / Absolute Zero / SCOPE self-play reasoning deep dive

Item: r-selfplay-sota · 2026-09-28 · gopher flash50
Method: primary-source fetches this session (arXiv abs + full HTML for each paper, official GitHub READMEs, GitHub issue listings, HuggingFace model search, arXiv API via curl). Every number below was read off a fetched page this session unless marked OWED. Hardware-hours: not reported by any primary source for any of the three systems, so that field is OWED, not invented.

---

## 1. R-Zero (arXiv 2508.05004, ICLR 2026)

**Identity (verified).** "R-Zero: Self-Evolving Reasoning LLM from Zero Data". Author list pulled from arXiv API this session (`curl -s https://export.arxiv.org/api/query?id_list=2508.05004`): Chengsong Huang, Wenhao Yu, Xiaoyang Wang, Hongming Zhang, Zongxia Li, Ruosen Li, Jiaxin Huang, Haitao Mi, Dong Yu (Tencent AI Lab / WashU per search results; a search snippet claiming a "Chengqi98/R-Zero" repo returned HTTP 404 on direct fetch, so the official repo is github.com/Chengsong-Huang/R-Zero, which serves the paper's code and FAQ).

**Mechanism.** Two models initialized from the same base: a Challenger generates questions (candidate pool N=8,000 per iteration), the Solver answers each with m=10 samples, questions kept only when majority-vote agreement lands between 3 and 7 of 10 (delta=0.25), BLEU dedup at tau=0.5. Both then trained with GRPO on the EasyR1 codebase, BF16 + FlashAttention-2. 3 iterations in the main tables (iteration-4 appears in the scaling analysis). Math eval used GPT-4o as programmatic judge (Section 4.1.2), which is a human-model-in-the-loop caveat the "zero data" framing does not remove.

**Measured gains (Table 1 / Table 2, arXiv HTML v3, fetched this session).**

Math benchmark average (7 benchmarks: AMC, Minerva, MATH-500, GSM8K, OlympiadBench, AIME-24, AIME-25):
- Qwen3-4B-Base: 42.58 -> 49.07 (+6.49, the headline claim)
- Qwen3-8B-Base: 49.18 -> 54.69 (+5.51)
- OctoThinker-3B: 26.64 -> 29.32 (+2.68)
- OctoThinker-8B: 36.41 -> 38.52 (+2.11)

Qwen3-4B-Base per-benchmark (base -> iter 3): AMC 45.70 -> 57.27; Minerva 38.24 -> 52.94; MATH-500 68.20 -> 79.60; GSM8K 72.56 -> 92.12; OlympiadBench 34.8 -> 44.59; AIME-24 10.94 -> 12.71; AIME-25 6.15 -> 4.27 (declines; the average gain coexists with regressions on the hardest benchmark).

General-domain average (3 benchmarks: SuperGPQA, MMLU-Pro, BBEH): Qwen3-4B-Base 26.34 -> 31.15 (SuperGPQA +6.67, MMLU-Pro +4.89, BBEH +2.85); Qwen3-8B-Base 31.98 -> 34.50; OctoThinker-3B 7.47 -> 11.12; OctoThinker-8B 11.70 -> 23.00.

**Discrepancy flag.** The abstract claims "+7.54 on general-domain reasoning benchmarks" for Qwen3-4B-Base, but Table 2's average delta reads 26.34 -> 31.15 = +4.81. I could not reconcile these two numbers from the pages fetched. Reported as found, unresolved (see OWED).

**Hardware.** Official README FAQ, verified byte-level via raw.githubusercontent fetch (README lines 121-123): "All our experiments were conducted on an 8-GPU server, using models that can run on a single GPU (e.g., 4B or 8B). If you need to run experiments under different conditions, such as with larger models or different hardware, you will need to modify the code accordingly." GPU type is never named; the paper (HTML v3) states only BF16 + FlashAttention-2 (Appendix A.1).

**Hardware-hours: OWED.** No wall-clock, GPU-hours, or token-throughput figure appears in the paper HTML v3 or the README.

**Reproduction assets.** Code released (EasyR1-based; run via `bash scripts/main.sh Qwen/Qwen3-4B-Base qwen3-4b`); generated datasets uploaded to HF; no released checkpoints. README troubleshooting admits the questioner-training run can hang on a math_verify infinite loop that the timeout may miss.

---

## 2. Absolute Zero / AZR (arXiv 2505.03335, NeurIPS 2025)

**Identity.** "Absolute Zero: Reinforced Self-play Reasoning with Zero Data". Tsinghua / BIGAI (LeapLabTHU), first author Andrew Zhao (andrewzh112). Official repo github.com/LeapLabTHU/Absolute-Zero-Reasoner; paper branch is the sanctioned reproduction target ("Use the paper branch to replicate results from original paper", README).

**Mechanism.** One model, two roles: it proposes code tasks in three modes (deduction, abduction, induction) and solves them; a Python executor is the verifier, so the reward is machine-checkable. GRPO-style RL on veRL; batch 64x6 (2 roles x 3 task types), lr 1e-6, AdamW. Trains 200+ steps for 7B/14B (still improving at 200); the 3B model plateaus. Single identity-function "zero triplet" as seed.

**Measured gains (Table 1, arXiv HTML v1, fetched this session).** Qwen2.5-7B-Coder -> AZR-Coder (zero external data):
- Code average +5.0 (to 61.6), Math average +15.2 (to 39.1), Overall +10.2 (to 50.4)
- Per-benchmark (final, delta; base values derived by subtraction from the fetched deltas): MATH-500 72.6 (+22.6), Minerva 36.4 (+19.1), OlympiadBench 38.2 (+16.3), AMC 57.5 (+17.5), AIME-24 20.0 (+13.3), AIME-25 10.0 (+6.7), LCBv5 31.7 (+11.8), HumanEval+ 83.5 (+3.0), MBPP+ 69.6 (+0.3)

AZR-Base (Qwen2.5-7B): overall +7.0 (to 46.8), math +10.9. Scaling (OOD total gain): 3B 40.7 (+5.7), 7B 50.4 (+10.2), 14B 53.3 (+13.2); Llama-3.1-8B +3.2. Cross-domain claim: expert-code-data models move math by only +0.65 avg while AZR moves math by +10.9/+15.2, and code-data-free AZR beats the best code-data model on code by 0.3pp. AZR beats the previous best zero-data model (ORZ at 48.6) by 1.8pp.

**Hardware (README, exact quote fetched this session).** "3b models need 2 X 80gb GPUs, 7/8b models need 4 X 80gb, 14b requires 8 X 80gb". So the smallest published configuration (3B) already requires 160 GB of accelerator VRAM (A100/H100 class), roughly 5x a 24 GB RTX 4090 before counting the code-execution sandbox the loop needs (README calls the bundled executor "very raw... not secure for production" and offers a Docker Sandbox-Fusion alternative).

**Hardware-hours: OWED.** Nothing in arXiv HTML v1 or v2, nor the README, reports wall-clock or GPU-hours. W&B logs are linked from the repo (could yield run durations; not parsed this session).

**Reproduction assets.** Official checkpoints on HF (`andrewzh/Absolute_Zero_Reasoner-Coder-3b/7b/14b`, Base-7b/14b), seed datasets in-repo, W&B logs. HF model search this session found community artifacts that are quantized repacks of the official weights only (bartowski GGUF ~1.5-1.7k downloads each, mradermacher, Mungert, DevQuasar, exl3 packs); zero community-retrained models or LoRA adapters surfaced. Issue #35 (2026-03-27, closed) asks for a batch-size recipe to run AZR-14B on 4x A100, i.e. users down-shard within the datacenter, not down to consumer cards.

---

## 3. SCOPE (arXiv 2605.31433, v1 2026-05-29, EdinburghNLP)

**Identity.** "SCOPE: Self-Play via Co-Evolving Policies for Open-Ended Tasks". Wai-Chung Kwan, Aryo Pradipta Gema, Joshua Ong Jun Leang, Pasquale Minervini (University of Edinburgh). This is the newest of the three and extends self-play from verifiable (math/code) to open-ended tasks.

**Mechanism.** Challenger generates document-grounded tasks; Solver answers via multi-turn retrieval (2018 English Wikipedia, E5-base-v2, 3 docs per query, 500-token tool responses; FAISS index + corpus ~75 GB per the repo); a frozen copy of the initial model is a fixed Judge that writes rubrics from source documents and grades. GRPO on verl with FSDP (offloading + gradient checkpointing) and SGLang rollouts. 3 iterations of 20 steps per role (extended to 6 for Qwen3-8B); batch 64 (Challenger) / 256 (Solver), group size 8; tasks kept only when mean rubric score is in [0.2, 0.8].

**Measured gains (paper HTML v1, fetched this session).** Open-ended 8-benchmark average (DRB, ResearchRubrics, ResearchQA, SQAv2, ResPlan, HealthBench, WildBench, Arena-Hard-CW):
- Qwen2.5-7B-Instruct: 24.4 -> 34.8 (+10.4)
- Qwen3-8B: 37.7 -> 43.1 (+5.4; 44.8 at iteration 6)
- OLMo-3-7B-Instruct: 30.7 -> 38.5 (+7.8)

Held-out short-form QA 7-benchmark average: Qwen2.5-7B 45.9 -> 59.7 (+13.8); Qwen3-8B 54.0 -> 61.8 (+7.8); OLMo-3-7B 40.0 -> 49.2 (+9.2). Baseline comparison: GRPO trained on ~9K curated prompts scores 33.4 / 41.5 / 39.0 open-ended and 56.3 / 60.7 / 48.6 short-form, so SCOPE beats the curated-data GRPO on all three models on short-form (by up to 3.4) but loses to it on OLMo-3-7B open-ended (39.0 vs 38.5). Scoring itself used GPT judges (gpt-5.4-mini / gpt-5-mini), same caveat class as R-Zero's GPT-4o judge.

**Hardware (two primary sources agree).** Paper: "All three models are trained with the same optimiser and schedule on 6 NVIDIA H100 GPUs." Repo README: "Hardware: 6x NVIDIA H100 80GB or equivalent." with "GPUs 0-1 for retrieval/inference servers and GPUs 2-5 for training." 480 GB H100-class VRAM total; a third of the fleet runs the retrieval/eval side, which is overhead the math/code systems do not carry.

**Hardware-hours: OWED.** No wall-clock in paper HTML or README. W&B logs published (wandb.ai/cyruskwan/SCOPE); not parsed this session. Paper's own limitation (Appendix A): "This overhead limited our experiments to 7-8B models; whether the gains hold at larger scales (e.g., 32B) remains an open question."

**Reproduction assets.** Code released (github.com/EdinburghNLP/SCOPE), checkpoints (HF collection wckwan/scope), W&B logs. Reproduction additionally requires an OpenAI API key for judging and the 75 GB Wikipedia+FAISS corpus.

---

## 4. Single-consumer-GPU replication: NONE FOUND

What I searched this session: multiple web-search probes (several queries hit 429/1302 rate limits mid-run and returned nothing; those are reported as failed probes, not negative evidence), the R-Zero GitHub issue list (no issue mentions single-GPU/VRAM/reduced-hardware reproduction; closest are #21 fsdp comms and #23 batch-size), the AZR issue list (closest is #35, a 4x A100 request, still datacenter), a HuggingFace model search for AZR (quantized repacks only, no retrained/LoRA community models), and direct fetches of both READMEs. Findings:

1. No documented single-consumer-GPU replication of R-Zero, AZR, or SCOPE surfaced anywhere I looked. Absence of evidence after this search is reported as "none found", not "none exists".
2. Every published configuration sits above consumer VRAM by a wide margin: R-Zero "8-GPU server" (model size only), AZR 2-8x 80 GB, SCOPE 6x H100. A single RTX 4090 (24 GB) is below the smallest published config for all three; AZR's smallest (3B on 2x80GB) alone is ~6.7x a 4090.
3. The consumer-side ecosystem around these papers is inference-only: GGUF/EXL3 quantizations of AZR's official weights exist and are the most-downloaded community artifacts; nobody appears to have retrained the loop on a consumer card.
4. Closest adjacent artifact, different lineage: TinyZero (github.com/Jiayi-Pan/TinyZero, now deprecated in favor of veRL) reproduces R1-Zero-style GRPO on countdown/multiplication with Qwen2.5-0.5B/3B and claims "You can experience the Aha moment yourself for < $30", with single-GPU mode documented only for models <= 1.5B and 2 GPUs for 3B. It is reward-RL on fixed external tasks, not self-generated curricula, so it replicates none of the three systems; it is only evidence that tiny-scale RL loops fit on small hardware.

Practical read for a single-consumer-GPU attempt (inference from the fetched configs, clearly marked as my analysis): the self-play loop's cost is dominated by rollout generation (R-Zero: 10 solver samples per question across an 8,000-question pool per iteration; SCOPE: 5-turn retrieval rollouts with 16k-token answer budgets), so a LoRA-quantized single-card run would bottleneck on generation speed, not on the training-side memory that ZeRO/FSDP offloading already solves. Nobody has published that run as of this session.

---

## 5. OWED (claimed by nobody I could verify; left unwritten rather than guessed)

1. **Hardware-hours per run, all three systems**: not reported in any fetched primary source (papers, READMEs, project page). AZR and SCOPE publish W&B logs that could yield wall-clock; not parsed this session.
2. **R-Zero abstract +7.54 general-domain vs Table 2 +4.81 for Qwen3-4B-Base**: unresolved discrepancy between two pages of the same paper version.
3. **R-Zero exact GPU type and count**: "8-GPU server" is all either source states (ambiguous between 8x single-server GPUs and an 8-GPU server fleet).
4. **AZR NeurIPS camera-ready reproducibility statement content** (search summaries claim it names cluster/compute workers; the arXiv HTML v1/v2 pages I fetched do not show it).
5. **SCOPE per-GPU memory and wall-clock**; also whether the OLMo-3-7B open-ended loss to GRPO_data (39.0 vs 38.5) is statistically meaningful (no significance tests seen in fetched text).

## Sources (all fetched 2026-09-28 this session)

- arXiv abs 2508.05004 + HTML v3 (R-Zero): https://arxiv.org/abs/2508.05004 · https://arxiv.org/html/2508.05004v3
- R-Zero repo + README (raw byte fetch): https://github.com/Chengsong-Huang/R-Zero + https://raw.githubusercontent.com/Chengsong-Huang/R-Zero/main/README.md (hardware FAQ at lines 121-123)
- R-Zero issue listing: https://github.com/Chengsong-Huang/R-Zero/issues?q=is%3Aissue
- arXiv API author verification: `curl -s https://export.arxiv.org/api/query?id_list=2508.05004` (ran this session, output in transcript)
- arXiv abs 2505.03335 + HTML v1 and v2 (AZR): https://arxiv.org/abs/2505.03335 · https://arxiv.org/html/2505.03335v1 · https://arxiv.org/html/2505.03335v2
- AZR repo + README: https://github.com/LeapLabTHU/Absolute-Zero-Reasoner
- AZR issue listing (#35): https://github.com/LeapLabTHU/Absolute-Zero-Reasoner/issues?q=is%3Aissue
- HF model search AZR: https://huggingface.co/models?search=absolute+zero+reasoner
- arXiv abs 2605.31433 + HTML v1 (SCOPE): https://arxiv.org/abs/2605.31433 · https://arxiv.org/html/2605.31433v1
- SCOPE repo + project page: https://github.com/EdinburghNLP/SCOPE · https://edinburghnlp.github.io/scope/
- TinyZero (adjacent lineage): https://github.com/Jiayi-Pan/TinyZero
