# INTAKE — Uno: diffusion-augmented LLMs (lossless parallel token draws)

Source: @iScienceLuvr (Tanishq Abraham, Sophont AI), 2026-09-04 08:28Z. Paper arXiv:2609.04010
(IFM/UIUC/Cornell/Cerebras, Sep 3 2026). Code github.com/ifm-ai/uno, HF checkpoints
huggingface.co/collections/s-sahoo/uno. Image = paper p.1 (verified by eye).

**What:** Keeps the AR model distribution, adds lightweight diffusion weights (one extra
training phase, "negligible overhead") that draw MULTIPLE tokens in parallel. Psi-Spec
samplers give up-to-3x lossless speedup over base AR, beating speculative decoding at every
batch size, no draft model, no quality loss. Models built from scratch OR by augmenting
EXISTING open-weight AR LLMs. Their 8B beats 26B DiffusionGemma and Mercury 2 on agentic
tool use, coding, long-context.

## Score: 22/25 — BUILD NOW

| FIT | PULL | COST | WINDOW | NOV |
|-----|------|------|--------|-----|
| 4 | 5 | 4 | 4 | 5 |

- FIT 4: composes with what we run — HF checkpoints + open code + local inference; no new
  vendor. One unknown: does the Psi-Spec sampler run on our stack (llama.cpp/MPS support
  unverified). That verification IS the build.
- PULL 5: dead-center Rocinante. 3x lossless throughput on an 8B agentic model multiplies
  every token the swarm grinds — free lanes, accumulator primitive, agent-organs all scale.
- COST 4: checkpoints + code are free; eval rides free lanes; one builder pass to wire the
  runtime. Zero operator minutes, zero billed spend.
- WINDOW 4: payoff compounds at Rocinante arrival (Oct 27) but the falsifier (tokens/sec,
  batch 1 vs 8, our hardware) runs NOW on existing infra — and the Sep 20 proof wall wants
  faster local legs.
- NOVELTY 5: new class (diffusion-augmented AR), brand-new paper, not a re-find.

**Tri-state:** Paper's own benchmarks (3x, beats d-LLMs) — Supported (their evidence).
Fleet claim "retrofit + 3x on our Mac substrate" — Unproven. Falsifier: run 8B Uno vs its
base AR from HF, measure tokens/sec at batch 1 and 8, verify output identity (lossless
claim) on a fixed prompt set. Disproven if speedup <1.5x at batch 1 or outputs diverge.

**Verdict: BUILD** — falsifier workbench measurement first (one run, cheap), then
wire as the throughput primitive if it survives. Feeds: Rocinante, accumulator, mining arc.

**Room row:** appended to watch/room.jsonl (thread intake).

## ADDENDUM — stage-1 falsifier prep (card-worker, 2026-09-04 ~20:10 ET)

**Servable-today: NO.** Measured probes:
- Weights EXIST and are public: `huggingface.co/s-sahoo/uno-qwen3-8B` — full 5-shard
  safetensors (~16GB) + LoRA adapter bundle, apache-2.0, 127 downloads. Also
  `IFM/K2-Horizon-7B-Uno` and `IFM/K2-Horizon-0.9B-Uno`. Repo `github.com/ifm-ai/uno`
  live (HTTP 200). Collection claim in the card: CONFIRMED.
- Format is the blocker: repo ships `modeling_sdar.py` / `configuration_sdar.py` /
  `fused_linear_diffusion_cross_entropy.py` — `custom_code` PyTorch (SDAR), NOT GGUF.
  HF search "uno gguf": zero hits. Ollama tags: no Uno (12 models, none match).
- This box: no nvidia-smi (no CUDA GPU), 360GB disk free, ollama 0.32.7 running.
- Base AR comparison arm: `IFM/uno-qwen3-8b` base API returned 401 (gated or renamed);
  the qwen3-8B Uno repo bundles full weights so base AR = stock Qwen3-8B is the
  practical control.

**Falsifier plan (staged, honest about compute):**
1. CPU losslessness proxy (~1h, THIS box, $0): pull `IFM/K2-Horizon-0.9B-Uno`
   (~2GB), pip torch+transformers, `trust_remote_code=True`, 5 fixed prompts greedy
   temp-0, compare output identity vs base AR arm. Kill-test: outputs diverge on CPU →
   lossless claim dead before any GPU spend. tok/s on CPU = NOT a valid speedup datum
   (do not log it as one).
2. GPU falsifier (the real one, ~1-2h wall, needs CUDA ~20GB VRAM for 8B bf16):
   clone github.com/ifm-ai/uno, run their Psi-Spec sampler vs stock Qwen3-8B, batch 1
   and 8, fixed prompt set, log tok/s both arms. Disproven if <1.5x batch-1 or output
   divergence (per card). Compute source: Rocinante (Oct 27) or a burst CUDA lane if
   one exists by then — this box cannot host it.
3. PORT WATCH (running in background, $0): whether llama.cpp/vLLM land SDAR/Psi-Spec
   support or a GGUF conversion appears. That event flips servable-today to YES with a
   plain pull and re-opens branch 2 of this task immediately.

**Kill-switch (honest-boundary law):** Uno inference requires custom PyTorch runners
(trust_remote_code SDAR + Psi-Spec sampler). No ollama/GGUF path. Until a GGUF or
llama.cpp port exists OR Rocinante arrives with the PyTorch env, it is theater on this
box. Nothing spent: $0, no pulls executed, 0 operator minutes.
