# M2 — RECURRENT DEPTH (receipt-first)

- **Lane:** operator moonshot 2026-09-16 — wave-lane, figure "Scaling up Test-Time Compute with Recurrent Depth"
- **Window:** fetched 2026-09-16
- **Targets:** arXiv 2502.05171 (abstract + open full text/HTML). Free fetches only (WebFetch). No git. No paid APIs.
- **Mission:** verify identity (Geiping et al.?), deep-read, extract (1) mechanism, (2) scaling numbers + shape, (3) adaptive recurrence, (4) FLEET TRANSLATION → ractor witness recurrence budgets + receipt `depth` field design.
- **Discipline:** receipt appended as evidence lands; every number traced to fetched text; the T1.3-disintegration lesson caps recurrence budgets.

<!-- SWEEP LOG -->
- [x] receipt filed (this file)
- [x] paper identity VERIFIED (abstract fetch)
- [x] full text fetched (HTML if open)
- [x] mechanism extracted (latent recurrent depth core loop)
- [x] scaling numbers + shape extracted (3.6B × recurrence 1→64 vs 103B-materialized; ARC/GSM8K/OpenBookQA)
- [x] adaptive recurrence extracted (mean recurrence vs difficulty)
- [x] fleet translation table (model class → recurrence budget → expected depth behavior)
- [x] receipt `depth` field design (loop count + final state hash)
- [x] THE WEAVE one-sentence closing

<!-- APPEND POINT -->

## APPEND 2 — full text fetched (2026-09-16)

- Route: WebFetch timed out on the big HTML (60s cap, twice, incl. ar5iv) → `curl` of `https://arxiv.org/html/2502.05171v2` (438,912 bytes) → tags stripped locally → 133,952 chars of text, grepped/sectioned. Free fetches, no paid API, no git.
- Figure 1 is an SVG with vector-path text (not extractable as text) → rendered via headless Chrome screenshot and READ visually. Figure 1 title is verbatim **"Scaling up Test-Time Compute with Recurrent Depth"** — the exact title on the operator's figure. Top axis: **"Materialized Parameters"**, ticks **3.6B / 8.3B / 11.5B / 14.6B / 21.0B / 33.6B / 52.6B / 77.9B / 103B** spanning recurrence 1 → 64. Series: ARC challenge (blue), GSM8K CoT (orange), OpenBookQA (green).
- **Operator-figure check #2 (settled):** operator's "3.6B" and "103B-materialized" are BOTH the Figure-1 materialized-parameter axis (3.6B at r=1, 103B at r=64). Paper body text says "3.5B parameters" (the model itself); the HF model card gives materialized = `num_steps × 1.5B + 2B` (→ 50B @ 32, 98B @ 64). Figure axis rounds slightly higher (3.6B/103B). Abstract's "equivalent to 50 billion parameters" = the r=32 point. All consistent.

## APPEND 3 — MECHANISM (latent recurrent depth)

- **Update rule (paper §3, exact):** `e = P(x)`; `s₀ ~ N(0, σ²I)`; `sᵢ = R(e, sᵢ₋₁)` for i ∈ {1..r}; `p = C(sᵣ)`. The embedded input **e is re-injected every iteration**; the latent state starts **random** (not from e) — this pairing (input injection + random init) stabilizes the loop and promotes *path independence* (converges to a steady state independent of initialization; Anil et al. 2022 deep-preconditioning line). Analogy in paper: the loop is gradient descent on a data-dependent energy — e plays the data, the state iterates.
- **Architecture (Huginn-0125):** triplet (lP, lR, lC) = **(2, 4, 2)** transformer layers — only **8 "real" layers**; at r=32 it unfolds to effective depth 2+4·32+2 = **132 layers**, deeper than any fixed-depth transformer. h=5280, 55 heads × 96, MLP inner 17920, RoPE base 50000, RMSNorm in "sandwich" order, tied embeddings. Params: **~1.5B prelude+head (non-recurrent) + ~1.5B core block (recurrent, weight-shared) + ~0.5B tied embedding = 3.5B total.**
- **Training:** mean recurrence **r̄ = 32** drawn from a heavy-tailed **Poisson** (r varies per sequence); **truncated backprop-through-time, last k=8 iterations only** (memory independent of r). **795B tokens** (paper says "800B"), fully public data, instruction data mixed in so it natively knows a chat template; **21 segments on 4096 AMD MI250X GPUs, OLCF Frontier supercomputer, Dec 2024**, constant LR (never cooled), 47k steps. Two prior runs failed (representation collapse / model learned to ignore the state) — the fix was sandwich norms + embedding scale + learned adapter + LR 4×10⁻⁵. Weight-shared core is the whole point: **reasoning is learned into the loop, not the layers.**
- **No CoT anywhere:** reasoning happens in the evolving latent state between prelude and coda. No specialized reasoning training data, works with small context windows, can express "reasoning not easily represented in words."
- **Not a diffusion model:** noise injection didn't help; step-conditioned core Rᵢ(e, s) broke path independence and extrapolation.
- **Emergent computation:** tokens needing numeric work fall into multi-dimensional **orbits** in latent space (PCA-visible "orbiting" on a GSM8K token "3"), analogous to periodic arithmetic circuits in fixed-depth transformers, but generalizing to structural tokens ("makes", "thinks").

## APPEND 4 — SCALING NUMBERS + SHAPE

**Figure 1 (teaser, rendered and read):** x = Test-Time Compute Recurrence (1→64), y = Accuracy (%).
- **GSM8K CoT (orange) — the sigmoid that thinks:** ~0% at r=1, ~2% at r=4, ~24% at r=8, ~39% at r=12, ~42% by r=16-20, still creeping to **~47% at r=32-64**. Largest recurrence gain of any task shown (0 → 47). Needs the most loops before it moves at all.
- **ARC challenge (blue):** ~22% at r=1 → ~33% at 4 → ~40% at 8-12 → plateau **~43-44% from r=16 on**.
- **OpenBookQA (green) — converges quickest:** ~25% at r=1 → ~40% by r=12 → plateau **~41-42%**. Caption: "Tasks that require less reasoning like OpenBookQA converge quicker than tasks like GSM8k, which effectively make use of more compute."
- Shape law: **easy/recall tasks saturate by ~8-16 loops; hard/procedural tasks have a delayed sigmoid and keep gaining to 32-64.**

**Table 1 (zero-shot, lm-eval; main 0.8T checkpoint):**

| model | ARC-E | ARC-C | HellaSwag | MMLU | OBQA | PiQA | SciQ | WinoGrande |
|---|---|---|---|---|---|---|---|---|
| Ours r=4 | 49.07 | 27.99 | 43.46 | 23.39 | 28.20 | 64.96 | 80.00 | 55.24 |
| Ours r=8 | 65.11 | 35.15 | 58.54 | 25.29 | 35.40 | 73.45 | 92.10 | 55.64 |
| Ours r=16 | 69.49 | 37.71 | 64.67 | 31.25 | 37.60 | 75.79 | 93.90 | 57.77 |
| Ours r=32 | 69.91 | 38.23 | 65.21 | 31.38 | 38.80 | 76.22 | 93.50 | 59.43 |
| OLMo-7B (2.5T) | 68.81 | 40.27 | 75.52 | 28.39 | 42.20 | 80.03 | 88.50 | 67.09 |

→ r=32 3.5B ≈ OLMo-7B (trained 3× tokens) on most tasks; beats OLMo-7B on SciQ and MMLU. Beats all Pythia. HellaSwag needs only **8 recurrences** to near-peak (paper text; the "88" in the HTML is a LaTeXML digit-doubling artifact).

**GSM8K trajectory (Table 2/4/EMA):** r=1 → **0.00/0.00**. r=32 w/ sys prompt → 34.80 flex / 42.08 strict (CoT). **EMA-averaged checkpoint at r=64 → 47.23 flex / 38.59 strict.** For scale: OLMo-7B CoT 6.07/7.28; OLMo-2-1124-7B 61.94/66.19. The 180B-token recurrent twin already beat its fixed-depth twin 5× on GSM8K (9.02/10.24 vs 1.82/2.20) and on ARC-C (29.18 vs 26.96).

**r=1 ablation (Table 4, 0.8T):** ARC-C 24.06 (**below random 25**), HellaSwag 29.34, GSM8K 0.00 — *everything* the model knows how to *do* lives in the loop; the non-recurrent skin is nearly empty. Corollary (paper): the single-recurrence model stops improving between the 180B and 800B checkpoints — further pretraining built zero capability into the prelude/coda; **all gains encoded into recurrence iterations.**

**Compute equivalence (paper's own framing):** 3.5B params but pretraining FLOPs ≈ a **32B** dense transformer; test-time scaling useful **up to FLOP budgets equivalent to a 50B-parameter fixed-depth transformer** (i.e., r≈32; materialized 52B on Fig-1 axis). Fig-1 axis max 103B materialized at r=64 (HF formula: 1.5B·r + 2B).

**Recurrence × context (Fig 9) — the budget curve:** ARC-C zero-shot saturates at **8-12** iterations; with 1 few-shot example **~20**; with 25-50 examples **~32**. *More context in → more useful loops out.* Open-book OBQA (fact handed to the model): 38.2 → 49.2 (+11.0), almost closing the gap to OLMo-2 (53.4). Reading: recurrent models **memorize less, reason more about what's in context** — give the witness the fact, not the training run.

**Arithmetic (appendix):** 1-digit addition improves steadily 1→64 recurrences; 2-3-digit addition needs **>16 recurrences**; at r=32 reliably adds two operands to 4-5 digits each but fails multi-operand single-digit. Depth buys *procedure length*, not new knowledge.

**Hard ceiling (HF model card):** gains "up to around num_steps=64, after which extra steps don't hurt but add no improvement." **64 is the paper's own saturation wall — the natural T1.3 cap.** Below 4 steps: "very coarse answers."

## APPEND 5 — ADAPTIVE RECURRENCE (does it think longer on harder inputs?)

- **Yes, but with a twist — it exits on *convergence*, not on difficulty.** Zero-shot per-token early exit: stop when **KL divergence between two successive latent steps < 5×10⁻⁴**; sample and move to the next token. No exit heads, no finetuning (standard transformers need special training for early exits).
- Measured (Fig 10, first 50 questions per MMLU category, free-form chat): the model exits **earlier on high-school mathematics** and takes **~3.5 steps more per token on moral scenarios**; on philosophy it re-uses states (converges quickly on some tokens, deliberates on others). Math questions have crisp convergent attractors; squishy ethics questions keep the state moving.
- **Convergence speed is per-token and content-dependent at scale** (Fig 11, r=128 probes): slow convergence on the *key phrase* of a loaded question; oscillating latent patterns on structural tokens; the model once deliberated then refused an unsafe question. Emergent with scale despite training with fixed r per sequence.
- Context effect (Fig 9) is the difficulty lever: zero-shot budgets saturate at 8-12 loops, but rich context extends the useful loop range to ~32. The model uses more loops when there is more *to chew*.
- Practical cost: early exit costs almost nothing on MTBench (5.56 vs 5.63 standard). KV-cache sharing with a 16-step recurring budget: **no loss** (5.86) — because all recurrent KV entries come from the same projections, caches at different depths "match" and you can attend to the deepest available entry.
- Criteria available in the released code: `entropy-diff`, `latent-diff`, `kl`, `argmax-stability`, plus `warm start`/continuous-CoT (`continuous_compute=True` — feed the final state of a previous answer back as the initial state: a latent thought carried across turns).

## APPEND 6 — FLEET TRANSLATION (ractor engine compute law)

**The law:** a small weight-shared model with a loop budget becomes a difficulty-proportional thinker. Compute per question is now a *dial* (loops), not a *purchase* (parameters). Depth is how a gemma-class local witness approaches 50B-class behavior on procedural tasks without a bigger model — while remaining a 2-4B download. Caveats the paper itself prices in: depth buys **procedure**, not **facts** (closed-book OBQA stays behind; open-book +11.0) — facts still route to the specialist or to retrieval.

**Fleet translation table:**

| fleet seat | model class | recurrence budget | expected depth behavior (from paper curves) |
|---|---|---|---|
| scut janitor | gemma:2b | **4 loops max** | Fig-1 r=4 zone: "very coarse answers" (<4 is worse); fine for triage/classify, no reasoning expected |
| short worker | gemma-class 4B | **8 loops** (zero-shot default) | easy/recall tasks at near-peak by 8 (HellaSwag/ARC/OBQA zone); cheap |
| witness (standard) | gemma-class + loop engine | **12-16 loops** | MMLU/OBQA saturated; ARC plateau reached; the workhorse depth |
| witness (context-loaded) | same, with retrieved facts in prompt | **20-32 loops** | Fig-9 law: rich context extends useful saturation from 8-12 → ~32; open-book jumps (+11 OBQA) |
| obsessive witness | same, math/procedural only | **64 loops — hard cap** | GSM8K sigmoid tail (42→47% from 32→64); >64 = zero gain, pure burn (paper's own wall) |
| specialist (remote, scarce) | pro-class | n/a | reserved for what depth cannot buy: long-tail facts, synthesis breadth. Recurrence delay, not replacement |

**Per-question budget policy (difficulty dial):**
1. **Probe:** one cheap pass at low depth (r≈2-4 draft). Classify: answer stable + task recall-class → done at worker depth; unstable/procedural → escalate.
2. **Stability exit, not fixed depth:** loop until the answer draft stops moving between successive loops — the paper's KL-exit (<5×10⁻⁴) translates to "diff the draft/answer-state between loops; stop when delta < threshold." Easy questions converge by 8 on their own; hard ones earn more loops. Cost of early exit ≈ nil (MTBench 5.56 vs 5.63).
3. **Context scaling:** budget rises with prompt richness — zero-shot cap 12, with retrieved evidence cap 32 (Fig-9 numbers).
4. **THE T1.3 CAP (non-negotiable):** 64. The paper's own model card says gains end at ~64; beyond that compute is disintegration theater — the loop budget is where the T1.3 lesson bites: **cap the loop or the loop caps you.** Budgets are per-question, armed per witness persona, logged per answer.
5. **Loop hygiene:** 16-state KV rolling budget is lossless (paper §6.2) — a looped witness need not grow memory linearly with depth.

**Receipt `depth` field (what the latent trace leaves behind):**
```json
"depth": {
  "loops": 24,               // recurrence actually executed
  "budget_cap": 64,          // armed ceiling (persona × difficulty policy)
  "exit": "stability",       // "stability" | "cap" | "probe-pass"
  "final_delta": 3.1e-05,    // last state/draft diff vs threshold (5e-4 analog)
  "state_hash": "sha256:…",  // hash of final latent state / final pre-answer draft — the sᵣ fingerprint
  "stable": true             // path-independence check: rerun at different init hash-equals? (cheap, optional)
}
```
Rationale: the paper's traceable quantities are exactly loop count and final state (path independence makes sᵣ reproducible regardless of random s₀ — so `state_hash` is meaningful evidence, not vapor). `exit:"cap"` + `stable:false` on a saturated answer = the flag that this question actually needs the specialist.

## APPEND 7 — OPERATOR CLAIMS vs PAPER (verification table)

| operator figure said | paper says | verdict |
|---|---|---|
| title "Scaling up Test-Time Compute with Recurrent Depth" | exact Figure-1 title; paper title is "…with Latent Reasoning: A Recurrent Depth Approach" | VERIFIED (fig) |
| Geiping et al. | Geiping (1st) + 8 others, Goldstein lab (UMD/LLNL), arXiv 2502.05171 | VERIFIED |
| 3.6B model | 3.5B in text; **3.6B on the Figure-1 materialized axis at r=1** | VERIFIED (both true, different ledgers) |
| recurrence 1→64 | x-axis 1→64; gains end ~64 (model card) | VERIFIED |
| matching a 103B-materialized model | Fig-1 top axis ends at **103B materialized at r=64**; text says FLOP-equivalent 50B at r=32; HF formula 1.5B·r+2B → 98B @64 | VERIFIED (103B is the figure's own axis label) |
| ARC/GSM8K/OpenBookQA curves | exact three series in Figure 1 | VERIFIED |
| GSM8K CoT curve benefits most, keeps climbing | orange sigmoid 0→47%, still rising at 64; OBQA converges quickest; ARC plateaus ~16 | VERIFIED |
| adaptive recurrence / think longer on harder | yes, via zero-shot convergence exits (KL<5×10⁻⁴); nuance: exits track state convergence (early on math, +3.5 loops on moral scenarios) and context richness extends useful depth 8→32 | VERIFIED with nuance |

**Bottom line:** every load-bearing element of the operator's figure checks out against arXiv 2502.05171v2. The paper is a proof-of-concept (800B tokens, no LR cooldown, public data only) — treat magnitudes as directional, but the *shape* (sigmoid-vs-plateau per task class, saturation at 64, context-extends-depth, r=1 collapse) is the law the fleet can run on.

---

## APPEND 1 — identity VERIFIED (2026-09-16, WebFetch arxiv.org/abs/2502.05171)

- **Title (exact):** "Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach"
- **Authors (9):** Jonas Geiping, Sean McLeish, Neel Jain, John Kirchenbauer, Siddharth Singh, Brian R. Bartoldson, Bhavya Kailkhura, Abhinav Bhatele, Tom Goldstein (UMD + LLNL).
- **Versions:** v1 Fri 2025-02-07 18:55:02 UTC; v2 Mon 2025-02-17 17:14:04 UTC (current).
- **DOI:** 10.48550/arXiv.2502.05171 · Subjects cs.LG (primary), cs.CL.
- **Artifacts:** model `tomg-group-umd/huginn-0125` on Hugging Face; code + data recipe `seal-rg/recurrent-pretraining` on GitHub.
- **Abstract verbatim (segmented):** "We study a novel language model architecture that is capable of scaling test-time computation by implicitly reasoning in latent space. Our model works by iterating a recurrent block, thereby unrolling to arbitrary depth at test-time. This stands in contrast to mainstream reasoning models that scale up compute by producing more tokens. Unlike approaches based on chain-of-thought, our approach does not require any specialized training data, can work with small context windows, and can capture types of reasoning that are not easily represented in words. We scale a proof-of-concept model to 3.5 billion parameters and 800 billion tokens. We show that the resulting model can improve its performance on reasoning benchmarks, sometimes dramatically, up to a computation load equivalent to 50 billion parameters."
- **Operator-figure check #1:** operator's figure says "3.6B" — abstract says **3.5 billion parameters** (3.5B total incl. embeddings is the paper's own framing; check full text for the exact "3.5B/3.6B" split). Operator says "matching a 103B-materialized model" — abstract itself claims "equivalent to 50 billion parameters"; the 103B figure likely comes from the Figure-1 x-axis (materialized depth at 64 recurrences). To verify in full text.
- **VERDICT:** YES — this is the recurrent-depth paper the figure depicts. arXiv 2502.05171, Geiping et al. (first + last authors confirm), Huginn model.

---

**THE WEAVE:** Depth is the small model's equalizer.

