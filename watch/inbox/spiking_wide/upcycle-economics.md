# UPYCLE ECONOMICS 2026-10-01: the convert-don't-train menu, priced for the estate

Class: RECEIPT · Lane: gala_20260925/spiking-wide/upcycle-economics (division B) ·
Writer: upcycle-economics lane seat · Trigger: SPIKINGBRAIN_DROP_20261001.md steal 2
("Falsifiable probe: upcycle cost per capability point, measured").

Method: primary links fetched full-text this session (arXiv HTML/API; listed per row).
Published compute is left in the authors' hardware units (A100/H100-hours) and then
translated to estate units. Estate units: the 4GB AMD box (ask-supplied hardware; no
estate receipt names the exact card, searched state/, docs/DNA.md, memory/, watch/inbox/
with no hit: stated here as the ask gives it), and the planned DDR3 body (STRATA_DROP:
"$200 used box + 64GB DDR3 + used 12GB GPU = a 125B MoE at 60-90 t/s local", ~$300
total). "Derived" marks arithmetic I did from cited numbers; everything else is the
paper's own. Capability point = 1% of the teacher's average benchmark score.

## 1. The register: published recipes, primary links

| # | Recipe (link) | Surgery | Published compute | Data | Retention vs teacher |
|---|---|---|---|---|---|
| R0 | SWA + 4 sinks (estate B11 baseline, watch/inbox/wave_20260916/receipts/B10_MLP_KV_CACHE_PRIORART.md; arXiv:2608.28444) | none, inference-time | 0 GPU-h | 0 | 99% short-context recovery; beats every post-trained linearization 2-10x on long-context recall |
| R1 | LoLCATs, Llama 3.1 8B -> linear (arxiv.org/abs/2410.10254) | attention conversion + LoRA | 6.5 A100-40GB-h (2h transfer + 4.5h LoRA); 70B = 18h on 8xH100 | 40M tok (0.003% of pretrain) | 5-shot avg 70.24 vs 72.26 (97%); MMLU 54.88 vs 66.11 (83%) |
| R2 | Depth prune + QLoRA heal, "Unreasonable Ineffectiveness of the Deeper Layers" (arxiv.org/abs/2403.17887) | drop layers (angle-similarity chosen) | single A100 per experiment; 5000 steps, batch 16 (hours not stated) | 164M or 328M C4 tokens | MMLU/BoolQ near-flat until a sharp collapse at ~45-55% cut (Llama-2), ~35% (Mistral-7B), ~25% (Phi-2), ~20% (Qwen); heal only modestly lifts QA but restores C4 loss |
| R3 | Minitron prune + distill, Llama 3.1 8B -> 4B; Mistral NeMo 12B -> 8B (arxiv.org/abs/2408.11796) | depth or width prune + KD recovery | 32 DGX H100 nodes (total GPU-h not stated) | 94B tok (4B); 380B tok (8B) | MMLU 58.7-60.5 vs 65.3 (90-93%); MN-8B beats teacher on GSM8k 58.5 vs 55.7 and HumanEval 36.2 vs 23.8 |
| R4 | Mamba-in-the-Llama, Zephyr/Llama-3-8B -> 25-50% Mamba hybrid (arxiv.org/abs/2408.15237) | attention layers swapped to Mamba (Q/K/V-init) + distill | <5 days on 8xA100-80GB = <960 A100-h | ~20B tok | MT-Bench 7.35 vs 8.00 (92%); 0%-attention variant collapses to 5.64; beats from-scratch hybrids trained on 1.2T-3.5T tok (63.84 vs 59.60) |
| R5 | Llamba, Llama-3.x -> Mamba 1/3/8B via MOHAWK (arxiv.org/abs/2502.14458) | cross-architecture distillation | single 8xH100 node, FSDP; total hours not stated | 8B/10B/12B tok by size (<0.1% of teacher budget) | 3B avg 63.9 vs teacher 61.9 (>100%); MMLU 52.7 vs 60.4 (87%) |
| R6 | Sheared-LLaMA, LLaMA2-7B -> 1.3B/2.7B (arxiv.org/abs/2310.06694) | targeted structured prune + 50B-token continued pretrain | ~50 GPU-h prune (8 GPUs, derived from stated 15K tok/s) + ~1,500 A100-h CPT (16 A100s, derived from stated 145K/77K tok/s); totals not printed in paper | 50.4B tok total (3% of from-scratch compute, paper's own claim) | not teacher-retention: 2.7B avg 56.7 beats every same-size model trained on 0.8-1T tok (OpenLLaMA-3B-v2 55.7) |
| R7 | SpikingBrain-7B upcycle, Qwen2.5-7B-base -> hybrid-linear (arxiv.org/abs/2509.05276) | attention conversion + continued pretrain; 76B adds dense->MoE upcycle | hundreds of MetaX C550 GPUs, stable >2 weeks, 128-way DP at 76B; "<2% of the compute needed for training from scratch" (paper's claim) | ~150B tok (~2% of from-scratch tokens; 100B @8k + 20-30B each @32k/128k) | MMLU 65.84 vs 74.21 (89%); CMMLU 71.58 vs 81.73 (88%); ARC-C 43.32 vs 44.04 (98%); HellaSwag 70.89 vs 72.81 (97%); C-Eval 69.80 vs 81.60 (86%); paper claims "nearly 90%" |
| R7b | SpikingBrain spike/quant conversion (same paper) | activation conversion + quantization only | ~1.5 h on a single 15GB GPU, 128-sample calibration | none (calibration) | ~2% average accuracy drop |

Estate-law constraint on the whole linear/hybrid family (B10 verdict): only the 3:1
hybrid form clears the recall bar; every pure linearization loses to R0 on needle
recall. So R1/R4/R5/R7 are priced as long-context-serving conversions, and R0 is the
zero-cost incumbent any of them must beat to earn its surgery.

## 2. Estate pricing: our hardware, our time, per capability point

VRAM binding facts from the papers: R1 needs the full model in bf16 (8B on a 40GB
A100, published); R2's worst case, a 50%-pruned 70B at 4-bit, fits 17.5GB, which
scales to roughly 3.5GB of weights for a 7B at 4-bit (derived), so a 7B QLoRA heal is
the only full recipe plausibly inside a 12GB consumer GPU (on-box confirmation still
owed). R7b's 15GB single-GPU shape sits just above both estate GPUs.

| Recipe | On the 4GB AMD box | On the DDR3 body (12GB GPU + 64GB DDR3) | On free cloud (Kaggle free GPU tiers, estate scout row LINKS.jsonl; ~30 GPU-h/wk class) | Cost per point (published units) |
|---|---|---|---|---|
| R0 SWA+sinks | RUNS TODAY (llama.cpp) | runs | n/a | 0 (the incumbent) |
| R2 depth prune, surgery only, no heal | GO as probe: 4-bit quantized forward passes + layer-similarity + drop + requant (fits 4GB at 2-4B) | GO | GO | not priced; retention unverified without heal (paper: without healing, rapid degradation) |
| R2 depth prune + QLoRA heal, 7B | NO: below every published training shape | GO: one weekend, 5000 steps x batch 16 = 328M tok at a derived 2-3k tok/s consumer QLoRA rate = ~30-45 GPU-h (derived, unconfirmed on-box) | GO at the edge: ~1 Kaggle week | cheapest for estate money: ~$0 GPU spend; retention "near-flat" below the model-dependent collapse point (~20-35% cut on 7B-class) |
| R1 LoLCATs 8B | NO | NO: published shape is 40GB bf16 | BORDERLINE, UNTESTED: 6.5 A100-h published; 16GB free-tier cards hold the 8B weights only just; unverified | 0.067 A100-h per retained avg point (6.5 h / 97.2%) - cheapest published GPU-h per point; MMLU cost is steep (83%) |
| R4 Mamba-in-the-Llama | NO | NO | NO: ~960 A100-h = 32 Kaggle-weeks (derived) | 0.104 A100-h per retained MT-Bench point |
| R5 Llamba | NO | NO (Mamba CUDA kernels + 8xH100 shape) | NO: total hours unstated, node shape 8xH100 | not priceable from published bytes (hours not stated) |
| R6 Sheared-LLaMA | NO | NO | NO: derived ~1,550 A100-h = ~52 Kaggle-weeks | not a retention recipe (beats same-size from-scratch, does not preserve the teacher) |
| R7 SpikingBrain CPT upcycle | NO | NO: 150B tok at a derived 3k tok/s consumer rate = ~579 days wall-clock (derived) | NO | cheapest per token (2% of from-scratch) and still cluster-class: hundreds of MetaX GPUs, >2 weeks |
| R7b spike/quant conversion | NO: 15GB shape > 4GB | BORDERLINE: 15GB shape > 12GB, unless their tooling ships an offload path (unverified) | GO if the tooling is public and fits a 16GB card: 1.5 h, one sitting | 0.75 GPU-h per point lost (1.5 h / 2%) - cheapest surgery per point in the whole set, but it is their internal tooling, not a shipped repo as far as this fetch saw |

## 3. GO / NO-GO (named)

GO 1, one sitting, the 4GB AMD box, $0: Gromov-style angle-similarity layer probe on
the janitor tier (gemma:2b / gemma4), quantized, drop 2-4 layers, requant, score on
our own eval cards before/after. No heal. Banks the "how many layers does the janitor
actually need" number and is also this receipt's falsifier run.

GO 2, one weekend, the DDR3 body's 12GB GPU, $0 marginal: depth prune a 7B-class
model by 20-35% of layers and QLoRA-heal 5000 steps on a 164-328M token slice (C4 or
our own residual corpus). Expected per R2: near-flat MMLU/BoolQ below the collapse
point, roughly half the memory and compute. This is the cheapest conversion per
capability point that fits one weekend of our hardware.

NO-GO now: R7 SpikingBrain-style CPT upcycle (579 consumer-GPU-days derived), R3
Minitron (32 DGX nodes), R6 Sheared-LLaMA (~1,550 A100-h derived), R4
Mamba-in-the-Llama (~960 A100-h), R5 Llamba (8xH100 node shape), R1 LoLCATs on either
estate box (40GB published shape; both boxes under it).

CONDITIONAL: if the DDR3 body lands with a 16GB GPU instead of 12GB, R1 LoLCATs-8B on
a free Kaggle week becomes the first thing to test (borderline on 16GB, untested,
published at 40GB). If R7b's conversion tooling ships publicly with a <=12GB path, the
spike/quant conversion is a one-sitting experiment worth one lane.

## 4. Answer to the ask, in one line each

- Cheapest per point of capability retained, published: R1 LoLCATs-8B, 6.5 A100-h for
  97% short-context average (0.067 A100-h/point), but it pays in MMLU (83%) and, per
  B10, still loses to R0 on recall.
- Cheapest per point for the estate specifically: R2 depth-prune + QLoRA heal on a 7B,
  ~$0 GPU spend inside one weekend on the DDR3 body's 12GB GPU (30-45 h, derived).
- Anything inside one-sitting / one-weekend: YES, two: GO 1 (one sitting, 4GB box,
  surgery-only probe) and GO 2 (one weekend, 12GB GPU, full prune+heal). R7b is a
  one-sitter only if a <=12GB public path exists (unverified).
- The estate's own bar: R0 SWA+sinks at 0 cost already holds the short-context
  quality and beats the linearizations on recall; a conversion only earns its surgery
  by buying constant-state long-context serving (the hybrid form, B10 verdict).

## 5. Decision ledger + falsifier

Closes: the drop receipt's falsifiable probe is now PRICED (this receipt) - the
"measured" half stays open and is exactly GO 1 + GO 2. Changes: DDR3-body build note -
the used 12GB GPU is not only an inference pager, it is the estate's training tier
(QLoRA-heal capable per this pricing); and any future upcycle ask must state its delta
over R0 before it spends a GPU-hour.

Falsifier: run GO 1; if a 20-35% layer cut without heal degrades our own eval cards
by more than ~5%, the convert-don't-train lane is dead at every estate budget tier
(healing is then proven necessary but only affordable on cloud), and this receipt's
GO 2 collapses to no-go.

## Sources (all fetched this session)

- arXiv 2509.05276 abs + html v1 (SpikingBrain): base Qwen2.5-7B, 150B tok, MetaX
  C550, <2% compute, benchmark pairs, R7b 1.5h/15GB/128-sample numbers
- arXiv 2408.11796 html v2 (Minitron): 94B/380B tok, 32 DGX H100 nodes, Table 1 scores
- arXiv 2403.17887 html v1 (Deeper Layers): SAP method, collapse points, QLoRA heal
  5000 steps / 164-328M tok, single A100, 70B-half 17.5GB
- arXiv 2410.10254 html v1 (LoLCATs): 6.5 GPU-h 8B, 40M tok, Table 7 scores
- arXiv 2408.15237 html v1 (Mamba in the Llama): 20B tok, <5 days 8xA100-80GB, scores
- arXiv 2502.14458 API abstract + html v2 (Llamba): 8-12B tok, 8xH100, 3B avg 63.9
- arXiv 2310.06694 html v2 (Sheared-LLaMA): 50B tok, 16 A100 CPT, 3% compute claim
- Estate: watch/inbox/SPIKINGBRAIN_DROP_20261001.md ·
  watch/inbox/STRATA_DROP_20261001.md (DDR3 body pricing) ·
  watch/inbox/wave_20260916/receipts/B10_MLP_KV_CACHE_PRIORART.md (B10/B11 verdict,
  R0 baseline) · watch/inbox/LINKS.jsonl seq 1789484000013 (Kaggle free GPU tiers)
- Not found: any estate receipt naming the 4GB AMD card model (searched state/,
  docs/DNA.md, memory/, watch/inbox/); the 4GB AMD box is taken as the ask supplies it.
  Wrong-ID corrections this session: LoLCATs is 2410.10254 (not .10226), Llamba is
  2502.14458 (two guessed IDs rejected on fetch).
