# B10 — "MLP AS KV-CACHE" PRIOR-ART SWEEP (2026-09-16)

- **Lane:** research / verified-pending
- **Source ask:** wave coordinator — prior-art sweep on feedforward/recurrent state replacing or compressing the KV-cache for long-context memory. Is "MLP as KV-cache" NOVEL, REDISCOVERED (cite oldest), or DEAD-ON-ARRIVAL (cite strongest counter-result)?
- **Method:** WebSearch (free) to identify the 2024–2026 architecture wave; WebFetch of arXiv abstracts/full text for exact claims. No paid APIs, no git.
- **Moving baseline:** arXiv:2608.28444 (sliding-window + 4 sinks, training-free, beats post-trained linearizations 2–10× on long-context recall — see `receipts/B11_SLIDING_WINDOW_RIB.md`, VERIFIED). Any KV-cache replacement must now beat that.
- **Status:** IN_PROGRESS — receipt first, appended as research lands.

---

## Findings

*(appended per architecture as evidence lands)*

### F1 — TTT-MLP (Test-Time Training layers), arXiv:2407.04620 — Sun et al., Jul 2024, ICML 2025. THE literal "MLP as KV-cache."

Mechanism: the recurrent hidden state of an RNN-like sequence layer is itself a small **MLP**, updated at inference by one gradient-descent step of self-supervised reconstruction ("learning to learn at test time") on each incoming token. The fixed-size MLP weights therefore play exactly the role the KV-cache plays for softmax attention — a compressed, growing-informativeness memory of all history — with linear complexity and constant memory. Variants TTT-Linear and TTT-MLP are drop-in replacements for self-attention blocks.

Claim: matches or exceeds Mamba and strong Transformer baselines (e.g., "mamba-at-scale" 1.3B and 8k-context Transformer) on Pile/Books3-style LM evals; TTT-MLP gets closer in gap to the 8k-context Transformer on longer contexts; effective context can reach ~2M "virtual" tokens while per-step cost stays constant. Cost: ~linear training, constant-memory inference; the catch is the inner gradient step per token (engineered around with mini-batch parallelization in chunks of e.g. 16k). Follow-up framing: NVIDIA's TTT-La ("TTT with KV binding is secretly linear attention") argues TTT is learned linear attention with extra capacity — i.e., even the discoverers' successors fold it back into the linear-attention family.

### F2 — Titans: Learning to Memorize at Test Time, arXiv:2501.00663 — Behrouz, Zhong, Mirhoseini (Google), Jan 2025, NeurIPS 2025.

Mechanism: an **MLP-based long-term neural memory** trained at test time by a "surprise"-gated gradient update (memorize what violates expectations, weight-decay what is stale), running alongside sliding-window attention. Three integration modes: memory-as-context (MAC), memory-as-gate (MAG), memory-as-layer (MAL). The MLP's parameters are the persistent memory; attention keeps exact short-range access.

Claim: beats Transformers and recurrent baselines (LSTM, Mamba family) in both short LM evals and needle/haystack-style long-context tasks; scales to **context length beyond 2M tokens** with better needle-in-haystack than baselines while attention window stays small. Cost: constant-memory streaming inference, parallelizable training; memory module adds per-token gradient compute.

### F3 — Memory Layers at Scale, arXiv:2412.09764 — Berges et al. (Meta FAIR), Dec 2024, ICML 2025. The *other* sense of "MLP as memory."

Mechanism: replace some FFN layers with a **trainable key-value lookup** (product-key quantized sparse memory): the hidden state queries a huge table of (key, value) pairs, retrieves the top-k values, mixes them. This is a giant MLP made addressable — parametric memory without extra FLOPs. Not sequence state (it does not cache the context) — it is the associative-memory-layer prior art for "feedforward weights as a key-value store."

Claim: at 1.3T memory parameters (trained up to 1T tokens), memory layers beat compute-matched dense and MoE baselines on factual QA and code. Cost: sparse lookup, near-zero extra FLOPs, large RAM footprint. Direct ancestor: Lample et al. 2019 "Large Memory Layers with Product Keys" (arXiv:1907.05242) — which makes this lineage the oldest "MLP as key-value memory" in the modern stack.

### F4 — Kimi Linear (KDA hybrid), arXiv:2510.26692 — Moonshot AI, Oct 2025. The 2025–26 production SOTA for KV-cache replacement.

Mechanism: 3:1 hybrid — 20 **Kimi Delta Attention (KDA)** layers (fine-grained chunkwise linear attention with learned per-channel forgetting = a recurrent matrix state that is the compressed KV-cache) interleaved with 7 gated MLA (full-attention) layers. The linear layers carry the compressed history state; the few full-attention layers do exact in-window recall.

Claim: first hybrid linear architecture to **outperform full attention under fair comparison** (same data, similar params) at all tested scales; **75% KV-cache reduction**, up to **6× decoding throughput at 1M context**; ships with a 1M-token window. Note for the verdict: even the strongest replacement keeps 25% full-attention layers — the fleet does not run pure-recurrent. Same shape as Qwen3-Next (Gated DeltaNet 3:1 hybrid), MiniMax (lightning attention), IBM Granite 4.0 (Mamba-2 hybrid).

### F5 — STRONGEST COUNTER-RESULT: "Repeat After Me", arXiv:2402.01032 — Jelassi, Brandfonbrener, Kakade, Malach, Feb 2024, ICML 2024.

Mechanism/claim: transformers copy strings of **arbitrary length** via induction heads (soft-max attention lookup over raw KV pairs), while any model with a **fixed-size state** — SSMs, linear attention, and by extension any MLP-state KV-cache replacement — has a provable copying limitation that grows with state size. This is the theoretical wall every "compress history into a fixed state" design hits: associative recall at range is exactly what a compressed state cannot guarantee, and it is the same mechanism B11 measured empirically (linearizations recover 1–6% of full attention at 4K NIAH vs SWA's 17–25%). Corroborated in practice by the entire 2025 production hybrid wave: nobody ships pure-recurrent; everyone keeps 1-in-4 full-attention layers.

### F6 — OLDEST LINEAGES (the "rediscovered" dating): two independent roots.

(a) **KV-side compression:** Compressive Transformer, arXiv:1911.05507 — Rae et al., DeepMind, Nov 2019, ICLR 2020. Extends Transformer-XL with a two-tier memory: recent KV states attended exactly, older ones passed through a compression function (1×1 conv, mean/max pooling) into a **compressive memory** the model still attends to — with a reconstruction loss to train the compressor. The direct ancestor of every "compress the KV-cache into something smaller" scheme. Even older shell: Transformer-XL (Dai et al., 2019) recurrence.

(b) **State-side (weights-as-memory):** "Linear Transformers Are Secretly Fast Weight Programmers," Schlag, Irie, Schmidhuber, ICML 2021 — shows linear attention IS an outer-product fast-weight associative memory, tracing the idea to **Schmidhuber's Fast Weight Programmers (1991)**: history stored in slowly-updated weight matrices, retrieved by association. Any "MLP/weight-matrix as KV-cache" claim lands inside a 35-year-old frame. On the lookup side, product-key large memory layers go back to Lample et al. 2019 (arXiv:1907.05242), and "attention = Modern Hopfield associative memory" (Ramsauer et al. 2020, arXiv:2008.02217) closes the associative-memory loop.

### F7 — 2026 SOTA CHECK: the production consensus is hybrid, not replacement.

Systematic result: "Characterizing SSM and Hybrid Language Models" (arXiv:2507.12442) — SSMs/hybrids outperform Transformers for long-context *serving* across platforms (constant-memory state vs growing KV). Production hybrids: Kimi Linear (Oct 2025, F4) and its frontier-scale followup Kimi K3 (linear attention in 3 of 4 layers), Qwen3-Next (Gated DeltaNet 3:1), MiniMax (lightning attention), IBM Granite 4.0 / Bamba-9B (Mamba-2 hybrid), NVIDIA Hymba. Analyst consensus (Raschka's architecture gallery, AI21 "rise of hybrids"): a few full-attention retrieval layers interleaved with constant-state linear/SSM layers is the dominant post-Transformer pattern through 2026–2028. The 2026 open problem is literally named "the recall gap" — compressed state vs exact attention on precision retrieval. Nobody ships a pure MLP/linear state at production scale; the 2026 endgame validates the hybrid, not the replacement.

---

## VERDICT: **REDISCOVERED — repeatedly, with a 35-year root. The pure variant is dead-on-arrival against the B11 baseline; only the hybrid survives.**

1. **Not NOVEL.** The literal mechanism — an MLP whose weights are the persistent state standing in for the KV-cache — is TTT-MLP (arXiv:2407.04620, Jul 2024, ICML 2025): "make the hidden state a machine learning model itself, and the update rule a step of self-supervised learning." Titans (arXiv:2501.00663, Jan 2025) independently ships an MLP-based test-time memory past 2M context. The lookup sense (giant FFN as trainable key-value store) is Memory Layers at Scale (arXiv:2412.09764, Dec 2024) → product-key memory (Lample et al. 2019). Oldest roots: Compressive Transformer for KV-side compression (arXiv:1911.05507, Nov 2019/ICLR 2020) and Schmidhuber's Fast Weight Programmers (1991) via "Linear Transformers Are Secretly Fast Weight Programmers" (Schlag, Irie, Schmidhuber, ICML 2021) for state-as-associative-weights. The idea has been rediscovered at least four times across three decades.

2. **Not fully DEAD-ON-ARRIVAL — but the pure form is.** The strongest pro-result: Kimi Linear (arXiv:2510.26692) beats full attention under fair comparison with 75% KV reduction at 1M context — proof the compressed-state direction is alive. The strongest counter: "Repeat After Me" (arXiv:2402.01032, ICML 2024) proves fixed-size states have a copying/recall limitation that attention does not; empirically sealed by the moving baseline arXiv:2608.28444 (B11): training-free sliding-window + 4 sinks recovers 99% short-context quality and beats **every** post-trained linearization (SUPRA, Hedgehog, LoLCATs, Liger-GLA, Mamba-in-the-Llama, ARWKV, Llamba, …) **2–10×** on long-context recall. A proposal that swaps the KV-cache for an MLP state must therefore beat SWA+sinks, not just full attention — and every pure-replacement entry in this sweep loses to SWA+sinks on needle recall at small windows. Only the 3:1 hybrid form clears the bar (it keeps exact-attention layers for what the window misses), and at that point "MLP as KV-cache" has already conceded the claim: attention stays; the MLP state is the *bulk-storage* tier, not the replacement.

3. **Fleet posture unchanged and corroborated.** The sweep confirms B11's doctrine from the other side: compressed-state recall dies at range in theory (F5), in training-free measurement (B11), and in production practice (no pure-recurrent deployment exists). Verbatim injection beats state compression; the window is exact but blind past its edge.

## Fleet mapping (what this touches)

- **Context-cap doctrine (`docs/FRAMEWORK_LOAD.md` deliberate-ask / context-pack; B11 §fleet):** no change — B10 *corroborates* the B11 layout (frozen RIB as sink anchor, k hash-verified ledger rows injected verbatim, recency tail). The research adds the reason nobody should ever be tempted to replace that with a learned summarizer state: that is the TTT/Titans/KDA failure mode at needle range.
- **Local janitors (gemma:2b scut, gemma4):** not actionable at inference — TTT/Titans layers require *training*, and the fleet runs pretrained checkpoints. Retrofitting a trained attention model with MLP-state memory is out of scope; the fleet's constant-memory lever remains the window size (w+4 mask), which is training-free.
- **Residual/bonds/percolator (the fleet's own test-time memory):** conceptual precedent, not a dependency. TTT/Titans are the canonical citation that "weights updated at test time as memory" works — the same move the percolator makes with invariants. If the Headroom-Closed boundary (memory/game/RESEARCH_SEEDS_20260914.md: the XP-never-spends gap, stage 2→3) is ever actually crossed toward stage-3/4 architecture change, Titans-style test-time memorization is the literature's proof-of-life that weight-writing memory is viable — with F5 as the standing caveat for why the ledger stays verbatim.
- **RESEARCH_SEEDS tie-in:** the KV-cache-as-binding-constraint framing ("the recall gap," 2026) is the compute-side twin of the Headroom-Closed Index: both are walls scaling laws alone will not move. The hybrid wave is the field's answer to the memory wall; the fleet's answer is the context cap + injection. Same boundary, two levels — file B10 alongside B11 as the pair that fences it.

## Top 3 canonical citations (ready to file)

1. **Sun et al., "Learning to (Learn at Test Time): RNNs with Expressive Hidden States,"** arXiv:2407.04620 (Jul 2024, ICML 2025) — the literal prior art: hidden state = two-layer MLP updated by self-supervised gradient steps at test time, linear complexity, replaces attention; "TTT-Linear and TTT-MLP can keep reducing perplexity by conditioning on more tokens, while Mamba cannot after 16k context" (125M–1.3B scale).
2. **Moonshot AI (Kimi Team), "Kimi Linear: An Expressive, Efficient Attention Architecture,"** arXiv:2510.26692 (Oct 2025) — the strongest surviving claim: KDA recurrent-state layers + 1-in-4 gated MLA hybrid beats full attention under fair comparison, 75% KV-cache reduction, up to 6× decoding throughput at 1M context.
3. **Jelassi, Brandfonbrener, Kakade, Malach, "Repeat After Me: Transformers are Better than State Space Models at Copying,"** arXiv:2402.01032 (Feb 2024, ICML 2024) — the counter-result that kills the pure variant: fixed-size states cannot copy/retrieve at range; attention can. (Standing baseline to beat: arXiv:2608.28444, B11.)

*Honorable mentions: Titans arXiv:2501.00663 (MLP neural memory, 2M+ context, NeurIPS 2025) · Memory Layers at Scale arXiv:2412.09764 (1.3T param product-key lookup) · Compressive Transformer arXiv:1911.05507 (oldest KV compression, ICLR 2020) · Schlag/Irie/Schmidhuber ICML 2021 + Schmidhuber 1991 FWP (oldest state-as-weights root) · arXiv:2507.12442 (2025–26 hybrid serving win) · arXiv:2608.28444 (the moving baseline, B11).*

---
**Status: COMPLETE** (2026-09-16 · receipt-first honored · appended as evidence landed · no git, no paid APIs)
