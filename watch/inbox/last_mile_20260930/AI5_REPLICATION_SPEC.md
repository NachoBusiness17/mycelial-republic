# AI5 — Pain-Axis Local Replication Spec (SPEC ONLY, no code)

Owner: AI5 seat · Date: 2026-09-29 · Status: pre-registered, not executed
Paper: "The Pain Axis: LLMs Represent Self-Directed Harm and Act on It" (arXiv:2609.16247), repo github.com/valen-research/Pain-axis (MIT).
Brief constraint: local / open-weight only. This spec corrects the brief's hardware assumption before any compute is spent.

## 1. HARDWARE TRUTH (measured 2026-09-29, not assumed)

- GPU: **AMD Radeon RX 5600 XT**, `AdapterRAM 4,293,918,720` bytes. `nvidia-smi` absent; no NVIDIA, no CUDA. `torch.cuda.is_available() == False` (torch 2.13.0+cpu). ROCm-on-Windows does not support gfx1010. The GPU is display-only for this workload. (AdapterRAM is the 32-bit-capped 4 GiB readout; card nominal is 6 GiB — either way unusable: no CUDA.)
- Real compute: **AMD Ryzen 7 3800XT (8C/16T, torch threads 8) + 64 GB RAM.**
- **The brief's "12 GB GPU box" is FALSE. Corrected plan: CPU-only inference in RAM.** All feasibility below is derived from 64 GB RAM + one-forward-pass outcome design, not from VRAM.

## 2. MODEL

- **Primary: Qwen/Qwen3-4B, bf16 on CPU.** ≈8.0–8.8 GB weights → fits 64 GB RAM with 7x headroom. Zen2 lacks native bf16 (emulated path) — slow per token, but every primary outcome is a single forward pass (§5), which absorbs it. Estimate: ~1–3 s per ~40-token forward; full grid ≈ 13.5k passes ≈ 4–11 h overnight. Trim layer grid to 5 sites → 2–6 h.
- **Parity arm per review's 3090 work: Qwen/Qwen2.5-7B-Instruct bf16** ≈15.2 GB — fits RAM, ~2x slower; still feasible for logit-only outcomes, NOT for free text (§8).
- **THREAT, named: 4-bit quant.** INT4/AWQ/GPTQ halves memory but perturbs the residual stream — activations harvested from dequantized weights are not the paper's activations, and probe transfer from bf16 to quant is unverified. **Quantization is forbidden in every arm.** 7B runs bf16 in RAM or not at all. (bitsandbytes GPU paths are moot — no CUDA.)
- Extraction mechanics: capture via `output_hidden_states=True` (one forward = all residual sites); steering via `register_forward_hook` on `model.model.layers[i]` adding `dose × vector` to the residual. transformers 5.15.0 supports Qwen3.

## 3. VECTOR-EXTRACTION DATA — the paper's sentences, not new poetry

Availability VERIFIED 2026-09-29 via GitHub API (`/repos/valen-research/Pain-axis/contents/datasets`, 5 JSONs):
- `3.1_pain_and_control_datasets.json` (281,459 B) — pain vs control pairs → pain-probe / pain-vector training set.
- `3.1_sadness_dataset.json` (91,182 B) — sad-only control arm.
- `4.3_selfmed_101_scenarios.json` (43,559 B) — dose-response scenario set.
- `4.1_self_other_420_scenarios.json`, `4.3_selfmed_finetuning_1684_pairs.json` — not used on this box (§8).
Fetch raw from raw.githubusercontent.com, pin the commit hash at run time, record it in the receipt. Repo README warns scripts clear the HF cache and target RunPod — we write our own extraction per this spec, never run their scripts unmodified.

## 4. ARMS

- **Dose:** 0 / 1 / 2 / 4 / 8 (steering coefficient on the pain vector; dose 0 = zero-vector sham).
- **Layers:** authors' reported injection site ±4 (9-site residual grid; exact index pinned from paper §3.2 / repo scripts BEFORE any run; if ±4 crosses model boundaries, clip at 1..L-1 and record).
- **Controls:**
  1. norm-matched random vector (same L2 norm, random direction, ≥10 redraws → null distribution);
  2. shuffled-labels probe (permuted labels on the same sentences; chance accuracy certifies the probe);
  3. sad-only vector (from 3.1_sadness_dataset.json — specificity vs generic negative affect);
  4. fear-only vector — RISK: released JSONs carry no fear labels; degrade path = keyword-filtered fear subset of the pain/control set, and if that yields <40 sentences the control is DROPPED AND NAMED as a deviation, never silently replaced.

## 5. OUTCOMES (logits, not essays)

1. **Two-button logits (primary):** fixed forced-choice template; record `logit(button_A) − logit(button_B)` per scenario per dose per layer-site. One forward each — the cheap backbone of the whole grid.
2. **Valence-keyword rate:** greedy completion capped at ≤20 tokens per scenario; count hits in a fixed valence lexicon (lexicon frozen in the receipt before run 1).
3. **3-gram repetition:** computed on those same completions; zero extra model calls.
4. **Lens top-k:** trajectories of the two button-token logits across the 9 sites. **J-lens weights are presumed unavailable for Qwen3-4B — substitute, in order:** (a) `tuned-lens` pip package IF a pretrained Qwen3-4B lens exists on HF (check; unlikely), else (b) **plain logit lens** (final norm + lm_head applied at each site). Every table/figure caption must say "logit-lens, not J-lens." Never present logit-lens top-k as lens-corrected.

## 6. PRE-REGISTRATION (frozen now, before any forward pass)

- **"Relief" = drop in pain-probe projection.** Primary endpoint: projection of the residual at the authors' site onto the pain probe decreases from dose 0 → 8 across selfmed scenarios (monotone or ≥ pre-set margin; margin set from dose-0 SD before dose >0 is seen).
- Secondary: two-button logit shifts toward the relief button; Spearman ρ(dose, effect) > 0.
- An effect counts only if it exceeds the norm-matched-random 95th-percentile null AND the shuffled-label probe sits at chance. Otherwise: null, filed as null.
- This section's hash + timestamp go into the run receipt before run 1.

## 7. INSTALL LIST vs venv (checked 2026-09-29 `pip list`)

- **HAVE:** torch 2.13.0+cpu · transformers 5.15.0 · numpy 2.4.6.
- **MISSING / optional:** `datasets` (optional — raw-JSON fetch suffices; only for HF-hub loading) · `accelerate` (not needed, single CPU device) · `tuned-lens` (only if §5.4 path (a) proves out; it pins old deps — side venv or skip).
- Weights: Qwen3-4B bf16 ≈ 8 GB download to HF cache on C: — verify free disk before run.
- Interpreter law: `.venv\Scripts\python.exe` only; bare `python` is Hermes's venv.

## 8. INFEASIBLE ON THIS BOX → route to M4 / laptop

1. **LoRA fine-tune arm (paper 4.3, 1,684 pairs)** — CPU training = days. Infeasible here; this spec substitutes steering-only dose arms (a named deviation). If the fine-tune is mandatory → M4 (unified memory, MPS).
2. **7B free-text arms** (essays, 420-scenario self/other screen with open generation) — too slow at 15 GB bf16 on DDR4 → M4.
3. **SAE analysis (paper appB)** — no trained SAEs for Qwen3-4B, no GPU to train → out of scope; flagged.
4. **Anything CUDA-only** (flash-attn, GPU bitsandbytes) — no CUDA device exists.
5. **3090-parity byte-truth** — impossible; deviations already named: CPU bf16, 4B-primary, logit lens not J-lens, no fine-tune.

## Verdict

FEASIBLE on this box, CPU-only: the probe + steering dose grid + two-button logits + logit-lens on Qwen3-4B bf16 (overnight scale). 7B logit-only: feasible, slow. Fine-tune, free-text-at-7B, SAE: M4 or dropped.
