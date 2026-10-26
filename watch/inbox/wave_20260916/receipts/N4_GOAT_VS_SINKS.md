# N4 — GOAT vs SINKS: reconcile GOAT (2601.15380) against B11 doctrine (2608.28444)

- **Wave-lane:** wave_20260916 / N4
- **Date:** 2026-09-16
- **Agent:** ZCode subagent (web research + reconciliation)
- **Mission:** verify the operator's GOAT drop ("redefines attention through Entropic Optimal Transport, continuous trainable prior, solves the sink problem, massively boosts length generalization") against our B11 doctrine (sliding-window + FIXED attention sinks recovers 93–99% of teacher, training-free; sinks are load-bearing).
- **Constraints honored:** no git, no paid APIs; WebFetch (free) only. Receipt written first, appended as evidence landed.

## Sources

| # | Source | URL | Status |
|---|--------|-----|--------|
| S1 | GOAT abstract page | https://arxiv.org/abs/2601.15380 | FETCHED 2026-09-16 |
| S2 | GOAT full text (HTML v2) | https://arxiv.org/html/2601.15380v2 | FETCHED 2026-09-16 (first attempt timed out; retry clean) |
| S3 | B11 abstract page | https://arxiv.org/abs/2608.28444 | FETCHED 2026-09-16 |
| S4 | local B11 lane receipt (sibling) | `watch/inbox/wave_20260916/receipts/B11_SLIDING_WINDOW_RIB.md` | READ (full-text-verified numbers) |
| S5 | wave state | `watch/inbox/wave_20260916/WAVE_STATE_20260916.md` | READ (B11 = COMPLETE; B10 = REDISCOVERED verdict) |

## S1 — GOAT identity card (from abs page)

- **Title:** "You Need Better Attention Priors"
- **Authors:** Elon Litman, Gabe Guo
- **GOAT =** Generalized Optimal transport Attention with Trainable priors
- **Venue:** accepted ICML 2026 (v2 dated 23 Aug 2026; 25 pp, 5 figs; v2 adds "1.23B scaling experiments and extended ablations")
- **Core claim (abstract, paraphrased):** standard attention = Entropic Optimal Transport (EOT) regularized by an *implicit uniform prior*; that naive prior is the root cause of attention sinks. GOAT replaces it with a *learnable, continuous prior*, stays FlashAttention-compatible, "combines the flexibility of learned positional embeddings with the length generalization of fixed encodings."
- Operator's drop: **VERIFIED in substance** — EOT framing, continuous trainable prior, sink solution, length-generalization claims all present on the abs page.

## Method detail (from S2 full text)

**The trainable prior — what it is, exactly.** Log-prior decomposes as `K_ij = K^rel_ij + u(j)`, realized as a query-key dot product in a reserved positional subspace (`d_p = 2R+2` of the head dim; content uses the rest):

- **Relative part:** truncated Fourier series `K^rel_ij = Σ_r [α_r cos(ω_r(i−j)) + β_r sin(ω_r(i−j))]`, fixed geometric frequencies (RoPE-style base 10,000), learnable weights α/β that **may be negative** — repulsion is legal because the prior lives in log-space (exp(K) is always a valid distribution).
- **Sink part (the key result):** key-only per-head bias `u_h(j) = λ_h·j + g_h(φ_abs(j)) + b_h·1{j=0}` — a linear drift, a one-layer SiLU MLP on absolute-position features, and **an explicit learned bias on position 0**: the "Prior Sink." Implemented as a broadcast bias, one extra head-dim, single SDPA/FlashAttention call.
- **Support:** prior π ∈ Δ^(L−1) over key positions. Init: uniform (recovers standard attention) or a max-entropy recency prior approximating ALiBi.

**The EOT routing.** One-sided OT: query i is a Dirac δ_i distributing mass over keys, cost `c_ij = −s_ij` (negative dot-product affinity), and — crucially — **no marginal constraint over keys**. Objective (Def 2.1): `p* = argmin_{p∈Δ} { ⟨p,−s⟩ − τH(p) }`; unique minimizer is softmax attention. Generalization (Prop 3.1): replace `−H` with `τ·KL(p‖π)` → solution `p*_j = softmax(s_j/τ + log π_j)`. Since `−H(p) = KL(p‖U) − log L`, **standard attention is the special case of an uninformative flat (uniform) prior**; τ is identified with the √d_c scaling.

**Sink explanation (the theory).** Theorem 5.1 (Collapse to Prior): with content-score dynamic range ω_i, `π_ij·exp(−ω_i) ≤ p_ij ≤ π_ij·exp(ω_i)` — as content signal → 0, attention collapses to the prior. Under standard attention that prior is uniform, so the model must realize the sink through **large-norm content keys**, "entangling a structural default with semantic representation." GOAT materializes the sink as the explicit prior bias instead. Theorem 5.4: uniform-prior sensitivity Ψ → 1 as L → ∞, but a peaked prior needs only **logarithmic margin growth** (δ ~ ln L) to keep the sink dominant.

**Training regime.** All **from scratch** (no finetuning): 125M GPT-style on C4 (4.0×10⁹ tokens, L_train=2048); **1.23B Llama-style** (22L/32H/d=2048) on FineWeb, ≈3.13×10⁹ tokens at the selected checkpoint, identical optimizer to the RoPE baseline ("the only architectural difference is the attention prior"); plus a DNA LM (human reference genome) and ImageNet ViTs.

**Length generalization numbers.** 1.23B FineWeb perplexity at 2k/4k/8k/16k: RoPE = 20.82 / 28.53 / 89.45 / **417.43**; GOAT = 20.75 / 21.04 / 22.69 / **24.77** (16× extrapolation, flat). 125M C4: +1.55 ppl over ALiBi in-distribution, extrapolates to 16× training length; RoPE degrades catastrophically. Passkey/NIAH: "near-perfect retrieval across depths and lengths" (no exact accuracies given); ALiBi "especially brittle on NIAH." ImageNet zero-shot resolution extrapolation beats absolute-PE ViTs; DNA LM beats RoPE on NLL and GC%-correlation.

**Relation to StreamingLLM / training-free sinks.** Xiao et al. 2024 cited repeatedly; GOAT notes existing defaults are "learned implicitly through content representations or enforced through fixed positional heuristics," whereas GOAT makes sinks "part of the prior itself." **No training-free sink method is used or proposed** — the sink bias is learned at training time (Fig. 2b: the model "spontaneously discovers a sharp spike at j = 0" in the learned prior).

## Reconciliation vs B11 (S3 + S4)

**1. GOAT does not contradict B11 — it confirms it from the training side.** B11's core physics ("sinks are load-bearing; sink-free windows collapse") is *derived* in GOAT as Theorem 5.1: in low-signal regimes attention necessarily collapses to its prior, and a uniform prior forces that collapse into content-key norm hacks. GOAT's "solution" to the sink problem is not sink removal — it is making the sink **explicit in the prior** (the `b_h·1{j=0}` Prior Sink). Both papers agree sinks are structural and mandatory; they disagree only on where the sink should live (emergent content keys preserved at inference vs. a trained prior component).

**2. They do not compete — different regimes of the model lifecycle.** B11 (2608.28444, Jolicoeur-Martineau et al., Microsoft ASG) is **training-free, inference-time**: an attention-mask change on pretrained checkpoints 1.3B–70B, recovering 93.2% (MMLU) / 99.0% (6-benchmark avg) of teacher at window 64 + 4 fixed sink tokens with zero post-training tokens. GOAT is a **from-scratch training architecture** at 125M–1.23B. There is no head-to-head in either paper: a pretrained RoPE model cannot adopt GOAT's prior without retraining, and GOAT's models are too small for the B11 benchmark battery. The real comparison — GOAT-trained model vs RoPE-model + SWA-sinks at equal scale — has not been run by anyone in these papers.

**3. The convergence is the story.** B11 pins the first 4 tokens; GOAT trains a peaked prior at j=0 and proves (Thm 5.4) that only a *logarithmic* margin (δ ~ ln L) is needed to keep it dominant as L → ∞ — which is theoretical cover for exactly why a tiny fixed 4-token sink suffices at every length in B11's experiments. Two independent papers, opposite methods, same shape: **a small, non-evicting, position-0 anchor**. B11 is the empirical half; GOAT is the derivation half.

**4. One genuine tension, correctly framed:** GOAT says the emergent sink (large-norm content keys) "entangles a structural default with semantic representation" — a mild critique of *why* B11's recipe works at all (B11 preserves the emergent hack; GOAT replaces the hack with the real thing). This does not threaten the fleet: we run pretrained checkpoints, so the emergent sink is the only sink they have, and pinning it (B11/RIB) is the only lever we hold.

## Fleet design impact (RIB / deck / context-pack)

- **The RIB stays pinned.** Every deployed seat (ollama janitors `gemma:2b`/`gemma4`, remote specialists) is a pretrained RoPE checkpoint — GOAT is inapplicable to them without retraining. The B11 lane's pack layout — **[frozen RIB prefix as sink anchor | k hash-verified ledger rows | recency tail]** — is unchanged.
- **GOAT upgrades the doctrine's standing, not its shape.** The RIB-as-sink was justified empirically (B11: 99% recovery, sink-free collapse). GOAT adds the derivation: an explicit peaked prior at position 0 is the *optimal* structure under the KL-regularized objective (Thm 5.1) and needs only log-margin to hold at any length (Thm 5.4). The deck/context-pack design is no longer "a hack around an emergent artifact" — it is the inference-time twin of what GOAT would train in.
- **Forward option only:** if the sovereign endgame ever trains our own janitor from scratch, GOAT's prior (FlashAttention-compatible, +1 head dim, init-to-ALiBi) is the leading architecture candidate — and the pack shape above already matches it, so nothing downstream changes either way. GOAT's position-dependent terms (λ_h·j + MLP) hint the sink mass could be *scheduled* across positions rather than pinned — a training-time property; at inference we keep pinning.

## Honest caveats

1. **From-scratch only.** No finetuning or retrofit path for pretrained models — the entire current fleet is unreachable by GOAT.
2. **Scale and data ceiling.** Max model 1.23B, and only ≈3.13B FineWeb tokens at the selected checkpoint (light for that size); the 125M C4 run is 4B tokens. No frontier-scale evidence.
3. **Benchmark asymmetry.** GOAT's headline numbers are perplexity extrapolation (16×; 24.77 vs 417.43 at 16k) and qualitative "near-perfect" passkey/NIAH — **no exact retrieval accuracies, no RMT/BABILong, no MMLU-class suites**, i.e., none of the batteries where B11 reported. The two papers' numbers cannot be placed on one axis.
4. **"Redefines attention" is the abstract's perfume.** The operative output is still softmax attention, `softmax(s/τ + log π)`: a learned additive log-prior bias. The EOT framing is the contribution — it exposes the implicit uniform prior, proves sink optimality (Thm 5.1), and licenses log-space (repulsion-capable) priors — but attention was not replaced; its *prior* was.
5. **Single-lab, no independent reproduction found.** Litman & Guo, ICML 2026 acceptance is a peer-review signal, v2's 1.23B scaling is self-reported; this pass found no third-party replication. Paper claim, not yet a reproduced one. (Contrast: B11's sink result reproduces Xiao et al. 2024 + Barbero et al. 2025, a multi-lab lineage.)
6. Operator's drop rating check: EOT ✓, continuous trainable prior ✓, sink solution ✓ (but it is *explicitation*, not elimination), "massively boosts length generalization" ✓ at ≤1.23B scale (orders-of-magnitude ppl win at 16k).

## VERDICT

**COMPLEMENT to B11** (orthogonal regimes, convergent physics): GOAT is the training-time derivation of the sink B11 preserves at inference time — it proves sinks are load-bearing (Thm 5.1), does not remove them, and gives theoretical cover (Thm 5.4: log-margin suffices) for the exact pin-the-first-tokens move our RIB already makes. It threatens nothing in the fleet doctrine and arms the from-scratch endgame.

**Design sentence for THE WEAVE:** *THE WEAVE keeps the frozen RIB pinned in the sink position — GOAT proves a small non-evicting position-0 anchor is the optimal prior (Thm 5.1/5.4), and until we train our own weights, pinning is the only way a pretrained model gets one.*
