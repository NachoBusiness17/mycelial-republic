# FAN selfplay-sota

lane model: inclusionai/ling-3.0-flash-vl
ts: 2026-10-03T22:33:24.087973+00:00
dt: 8.0s

---

## R-Zero

I cannot confidently identify a single peer-reviewed paper with the exact title "R-Zero" in the reasoning/RLHF literature. The concept of training reasoning via pure RL without supervised fine-tuning (SFT) emerged prominently after DeepSeek-R1's ablation showing SFT was a key ingredient. Related work I am aware of:

- **"DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"** (DeepSeek-AI, 2025) - the paper whose SFT ablation inspired follow-ups exploring RL-only training.
- **"Identity or Reasoning: An Empirical Study of SFT and RL on LLMs"** (Wen et al., 2025) - studied the relative contributions of SFT versus RL for reasoning.

**Benchmark gains:** OWED. I cannot verify specific percentage gains for a paper titled "R-Zero." I tried searching my knowledge for a self-contained "R-Zero" paper with reported AIME or MATH benchmark improvements, but I could not confirm exact numbers.

**Hardware hours per run:** OWED. I have no verified figure for compute budget (GPU-hours) for this work.

**Single consumer GPU replication:** OWED. I could not verify whether any replication was run on a single consumer GPU (e.g., RTX 4090/3090).

---

## Absolute Zero

I believe this refers to a paper on self-play reasoning without ground-truth labels, tentatively something like **"Absolute Zero: Self-Play Reasoning Without Ground Truth"** or a related variant. However, I am not confident in the exact title, authors, or venue.

- If this refers to self-play where two model instances generate reasoning chains and critique/improve each other without reference answers, this aligns with a broader post-DeepSeek-R1 interest in ungrounded self-play.

**Benchmark gains:** OWED. I tried to recall specific improvements (e.g., on AIME 2024/2025, MATH-500, or GSM8K) attributed to this work but could not verify any numbers.

**Hardware hours per run:** OWED. No verified compute figure in my knowledge.

**Single consumer GPU replication:** OWED. No verified replication information available to me.

---

## SCOPE (Self-Play Reasoning)

I recall a possible paper titled along the lines of **"SCOPE: Self-Play Creates Powerful Reasoning"** or **"SCOPE: Exploring the Limits of Self-Play Reasoning,"** but I cannot verify the exact title, authors, or publication venue.

- The general concept: models engage in structured self-play (e.g., mutual critique, debate, or iterative refinement) to improve multi-step reasoning without external supervision.

**Benchmark gains:** OWED. I could not verify specific benchmark improvements or the baselines compared.

**Hardware hours per run:** OWED. No verified figure.

**Single consumer GPU replication:** OWED. I searched my knowledge for any community replication of a SCOPE self-play reasoning pipeline on a single consumer GPU and found nothing verifiable.

---

## Summary Table

| System | Benchmark Gains | GPU-Hours/Rune | Consumer GPU Replication | Papers Cited |
|--------|----------------|----------------|--------------------------|-------------|
| R-Zero | OWED | OWED | OWED | DeepSeek-R1 (2025); Identity or Reasoning (Wen et al., 2025) |
| Absolute Zero | OWED | OWED | OWED | None verified |
| SCOPE | OWED | OWED | OWED | None verified |

**What I tried for all three:** I attempted to match each name to a specific peer-reviewed or arXiv paper with reported experimental numbers, compute budgets, and replication details. For all three, I was unable to verify the specific quantitative claims requested, so I have flagged them OWED rather than risk fabricating numbers.
