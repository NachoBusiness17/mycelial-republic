# B11 — SLIDING WINDOW vs LINEAR → RIB MAPPING (2026-09-16)

- **Lane:** research / verified-pending → VERIFIED (full text fetched 2026-09-16)
- **Source ask:** wave coordinator — find the "sliding-window beats linear attention" paper; extract exact empirical claim + mechanism + caveats; map to fleet RIB doctrine (frozen RIB = system+bootloader+manifest+verkle tip; deliberate-ask pays the context tax once).
- **Method:** WebSearch (free) to identify the paper, WebFetch/webReader of arXiv abstract + HTML full text for exact numbers. No paid APIs, no git.
- **Status:** COMPLETE

---

## Paper identification

**"Sliding-window beats linear attention"** — arXiv:2608.28444 — submitted 2026-08-28.
Authors: Alexia Jolicoeur-Martineau, Rhea Sanjay Sukthanker (Microsoft, Applied Sciences Group), Pashmina Cameron (Microsoft ASG), Emy Gervais (Independent).
- Search hit directly on the ask's exact phrasing; first result, abstract + HTML fetched and read.
- Cross-check leads found (not load-bearing): arXiv:2512.10411 (SWAA — SWA post-training adaptation), arXiv:2509.24552 / Cabannes et al. ICLR 2026 ("Short window attention enables long-term memorization"), Xiao et al. 2024 StreamingLLM (attention sinks).

## Exact empirical claim

Setup: **SWA(w, s)** = attend to previous w tokens **plus the first 4 tokens (attention sinks)**, w ∈ {64…512}, sinks fixed at s = 4. Applied **training-free** at inference — it is only an attention-mask change on pretrained checkpoints. Models span **1.3B–70B** (Phi-1.5, Mistral-7B, Llama-2/3.x, Qwen2.5-7B/32B/72B, QwQ). Baselines are **post-trained linearization methods**: SUPRA, Hedgehog, LoLCATs, Liger-GLA, MOHAWK, Mamba-in-the-Llama, DiJiang, ARWKV, Llamba, QLinAtt, QRWKV6/7.

Short context (MMLU-5shot, ARC-C/E, HellaSwag, PIQA, WinoGrande):
- SWA(64, 4) with **0 post-training tokens** recovers **93.2%** of teacher on MMLU and **99.0%** average across the 6 benchmarks — best non-teacher in **9 of 11** model cases. Best linear method (QRWKV6: 92.4% / 99.1%) needed **350–700M post-training tokens** to tie it.

Long context (Llama 3.1 8B base, contexts up to 4K, windows 128/256/512):
- **S-NIAH**: SWA ≥ linear at every window size and context length. At 4K, SWA recovers **17.2–23%** of full-attention accuracy; LoLCATs ≤ **5.8%**, Liger-GLA ≤ **0.8%**.
- **BABILong** (QA1–5 avg, window 256): at 4K SWA **15%** vs LoLCATs **3%** (≈5×); SWA recovers **25%** of baseline at 4K vs LoLCATs' **5%**. The abstract's headline: SWA is **2–10× higher than linear attention** on NIAH/BABILong.
- Speed/memory: SWA is the **fastest** decoder tested and its memory cost is **constant after the window fills** (lowest at w=64).

## Mechanism (why recency/anchoring wins)

1. **Exact recall over in-window tokens.** Softmax attention keeps raw (key, value) pairs; inside the window it is lossless copy/retrieval. Linear attention compresses all history into a fixed recurrent state (s_t, z_t) that "must continuously rewrite itself" — the paper calls deciding what to forget "an untractable problem," and that is exactly where associative recall dies at range.
2. **Attention sinks as anchors.** LLMs dump surplus attention onto the first tokens regardless of semantics (Xiao et al. 2024; Barbero et al. 2025). Once those tokens slide out of a naive window, performance collapses catastrophically — which is why earlier linear-vs-SWA comparisons (against sink-free SWA) were inadequate. Keeping the **first 4 tokens permanently attended** restores the model's own anchoring mechanism; the effective receptive field then grows layer by layer (≈ l·w after l layers), and short windows even improve long-term memorization and length extrapolation (Cabannes et al., ICLR 2026).

## Caveats

- **A pure window is still blind past its edge:** on 4K NIAH even SWA recovers only ~17–25% of full attention. It wins because linear attention recovers ~1–6%; neither approaches full attention for out-of-window recall.
- Sink-free SWA is catastrophic — the sink anchor is load-bearing, not optional.
- Results are for **training-free** SWA; post-training (SWAA) could improve it further (future work). No hybrid full-attention layers compared. Benchmarks are standard short/long-context suites, not agentic or multi-modal tasks; models ≤ 70B.

---

## Fleet doctrine mapping

**(a) Context-pack practice — pay-once prefix vs rolling window.** The paper is a direct empirical endorsement of the deliberate-ask shape: a tiny **frozen anchor prefix plus a recency window** preserves 99% of baseline quality at zero adaptation cost, while any scheme that rewrites history into a fixed state — rolling summaries are the prompt-level twin of linear attention's recurrent state — loses recall exactly where it matters. The frozen RIB (system + bootloader + manifest + verkle tip) should sit as the **first tokens of every window**, in the literal sink position the model already over-attends to; the context tax is paid once, into a static prefix, never re-derived per message. And it kills the temptation to "linearize" the chain to save tokens: a modest verbatim window is cheaper *and* better than a compressed summary state.

**(b) Trails/ledger retrieval — the wave capsule's stateless-window answer.** Strengthened, on both prongs. First, the paper shows exact recall exists **only for tokens inside the attention window** — so injecting k-relevant chain rows verbatim at context time is the only mechanism that gives an old row full-quality recall; any rolling digest of that row is the linear-attention failure mode. Second, the caveat cuts the other way: a pure sliding window recovers only ~17–25% of full-attention accuracy on 4K needle tasks — the window is exact but **blind past its edge**, which proves injection is not an optimization but the *only* path to old-row recall. The k-relevant-rows-plus-hashes design is the right union: softmax gives lossless compute over what is in-window, the hash pointer keeps verification of what was injected in the ledger layer (trust the bytes, not the attention). Constraint inherited: injected rows and the RIB must fit inside the w+4 mask — evidence that falls outside the window might as well not exist.

**(c) The ONE design change it justifies.** Formalize SWA-with-sinks as the context-pack layout: the pack builder emits **[frozen RIB prefix — never evicted, pinned as the sink anchor | k hash-verified retrieved ledger rows | recency tail]** within an explicit window budget, and rolling summaries of the chain are dropped entirely. One structure, three zones, no state that has to remember what to forget.

---

## Canonical URL + filed-ready one-liner

**Canonical:** https://arxiv.org/abs/2608.28444 (full text: https://arxiv.org/html/2608.28444)

**One-liner:** arXiv:2608.28444 (Jolicoeur-Martineau et al., 2026): training-free sliding-window attention with 4 sink tokens recovers 99% of short-context quality and beats post-trained linear attention 2–10× on long-context recall — so pin the RIB as the sink anchor, never roll the chain into summary state, and inject k hash-verified ledger rows at context time, because the window is exact but blind past its edge.
