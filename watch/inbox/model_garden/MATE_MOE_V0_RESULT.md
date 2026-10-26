# MATE_MOE_V0_RESULT - THE FALSIFIER RAN (lane MATE-0)

Date: 2026-10-01 (UTC). Spec: memory/plans/mate_moe_v0/EXPERIMENT.md, operator GO.
Amendment context: watch/inbox/model_garden/MATING_LIT_SWEEP.md (BAR / HARC / PopEvolution).
Verdict detail and kill quotations: memory/runs/mate_moe_v0/VERDICT.md. Every number also
lives in memory/runs/mate_moe_v0/results.jsonl with its env stamp.

Environment (applies to every number): repo HEAD 962e41054aceac8077ab25dbcec9c4a5b896fd58
(212 dirty working-tree entries; nothing committed by this lane), AMD Ryzen 7 3800XT
(8C/16T, torch 8 threads, 64 GB RAM), Windows 10 19045, Python 3.11.15,
torch 2.13.0+cpu, transformers 5.15.0. Parents: HF revisions
P1 Qwen/Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775,
P2 Qwen/Qwen2.5-Coder-0.5B-Instruct ea3f2471cf1b1f0db85067f1ef93848e38e88c25.
Checkpoints (gitignored models/): models/mate_moe_v0/{A_ties, B_mate_moe, A_linear, B1_trunkP1}.
Scripts: memory/runs/mate_moe_v0/scripts/s0_gate.py through s7_verdict.py.

## STEP 0 GATE: PASS

- Configs identical (all checked fields; zero diffs). Tokenizer cores hash-equal
  (tokenizer.json both c0382117ea329cdf..., vocab.json, merges.txt equal);
  tokenizer_config.json differs (chat template), expected.
- FFN cosine P1 vs P2, per layer over concatenated gate/up/down: mean 0.409550,
  min 0.336494, max 0.464759. Attention cosine mean 0.4941. Mean is NOT above 0.99, so
  the abort rule did not fire. Reading recorded: this pair is same-base by paperwork but
  weight-space ISOLATED (see verdict; the gate lacks a lower bound).

## BUILDS

- A (TIES dense merge): hand-rolled per the spec fallback clause (see deviations).
  Trim top-50% magnitude per parent per tensor, sign elected by weighted mass, weighted
  mean of sign-agreeing entries; applied to attention matrices (q/k/v/o) and MLP matrices
  (gate/up/down): 168 tensors. Norms, q/k/v biases, and the tied embedding use linear
  0.5/0.5 mean: 123 tensors. Saved-A witness: FFN zero fraction 0.2766, FFN cosine
  A-vs-P1 0.7444 (a genuine TIES-shaped output, not a coding artifact).
- B (MATE_MOE_v0): E=2, top-1, Qwen2-MoE container (transformers 5.15.0), 812,012,416
  params. Shared trunk = artifact A's trunk bytes (TIES merge). Expert 0 = P1 MLP
  verbatim, expert 1 = P2 MLP verbatim (fused gate_up/down 3D tensors). Router rows =
  unit-L2-normalized mean layer-l hidden states of each parent on its own fixed prompt
  set (6 prompts per parent, recorded verbatim in router_stats_receipt.json; no overlap
  with eval slices). norm_topk_prob=True so top-1 applies the chosen expert at weight
  exactly 1.0 (verbatim FFN semantics). The container-mandatory shared expert is
  neutralized exactly (intermediate size 64, down_proj zeroed, gate zeroed: contribution
  is identically 0). Sanity: logits finite on code and prose probes.
- Controls (DEVIATION-logged additions for kill attribution, not spec artifacts):
  A_LIN (linear 0.5/0.5 dense merge) and B1 (identical MoE container, trunk = P1
  verbatim instead of the merge).

## SLICES

- S_code: 8 held-out repo Python files (list + per-file sha256 in slices_receipt.json),
  30,025 tokens available, first 20,000 kept. Concat sha256 dfe9b314dbe26477..., 20k
  slice sha256 c25a58c8968b3fe2...
- S_prose: Salesforce/wikitext wikitext-2-raw-v1 test split, 298,938 tokens available,
  first 20,000 kept. Concat sha256 bbf94c53a05abe9e..., 20k slice sha256
  ceb46c83d20b8032...

## INSTRUMENT

fp32, CPU, context 512, sliding window stride 256 (canonical recipe; every token scored
exactly once as a target with up to 511 tokens of context), 78 windows per slice, 19,999
tokens scored per artifact x slice (the first token of a slice cannot be a target).
output_router_logits=True on B and B1; usage counted on the same positions whose NLL was
scored. Per-line settings and env stamps are inside results.jsonl.

## THE NUMBERS (perplexity; lower is better)

| artifact | S_code | S_prose |
|---|---|---|
| P1 Instruct (S_prose specialist per spec) | 13.1262 | 14.2793 |
| P2 Coder (S_code specialist per spec) | 13.9452 | 29.6069 |
| A TIES merge | 13558.9759 | 4361.4394 |
| B MATE_MOE_v0 E=2 top-1 | 2602.9582 | 2708.1190 |
| A_LIN control | 67.9512 | 148.4126 |
| B1 control (P1 trunk) | 451.5381 | 870.8765 |

Measured reality vs the a priori mapping: P1 beat P2 on the raw-text code slice too
(13.13 vs 13.95). The feed/kill arithmetic below still uses the spec's fixed mapping
(S_code specialist = P2, S_prose specialist = P1); the diagnostic is recorded, not
substituted.

## B ROUTER BEHAVIOR (the specialization measurement)

| slice | expert0 (P1) share | expert1 (P2) share | logit gap mean / std |
|---|---|---|---|
| S_code | 0.2470 | 0.7530 | -0.5309 / 1.5730 |
| S_prose | 0.1559 | 0.8441 | -0.7427 / 1.3924 |

Usage split across slices: 9.11 points (expert0 basis; identical magnitude on expert1).
Per-layer expert0 share (S_code): 0.63 0.26 0.74 0.10 0.51 0.59 0.45 0.27 0.23 0.06 then
layers 10-20 all 0.00, then 0.60 0.70 0.79. S_prose: same mid-stack zero block, lower
early/late shares. The router init vectors themselves are weakly separated: per-layer
cosine between the two parents' router rows has mean 0.9262 (min 0.4108), so the
discriminative direction is a small fraction of the row norms; the logit gap distribution
straddles zero with a systematic P2 lean on both slices. B1 repeats the pattern (split
12.41 points, P2 preferred even on prose, which is backwards for the mapping).

## FEEDS / KILLS (applied exactly as written in EXPERIMENT.md)

| rule | threshold | measured | verdict |
|---|---|---|---|
| FEED 1: B within 3% of specialist, each slice | B <= 1.03 x specialist | 186.66x (code), 189.65x (prose) | FAIL |
| FEED 2: A > 5% worse than specialist somewhere | ratio > 1.05 | 971x (code), 305x (prose) | HOLD |
| FEED 3: usage split > 30 points | > 30 | 9.11 | FAIL |
| KILL 1: dense suffices (B >= A both slices) | B worse than A | B beats A on both | NOT FIRED |
| KILL 2: router not specializing (within 10 points) | < 10 | 9.11 | FIRED |
| KILL 3: shared attention broke experts (B > 3% worse than specialist on own slice) | ratio > 1.03 | 186.66x / 189.65x | FIRED |

DOOR DOES NOT FEED (feeds 1 and 3 fail). TWO KILLS FIRE.

## VERDICT: DOOR-DEAD (the v0 form: merged shared trunk + training-free fitness router,
on this parent pair)

The amendment re-labels only the router kill: by itself it would read
ROUTER-METHOD-DIED-BAR-IS-FALLBACK (BAR, arXiv:2604.18473, is the known-good
router-training fallback; HARC, arXiv:2606.03391, names this merged-router breakdown and
offers a training-free calibration probe - per-layer router logit stats are banked for
exactly that). But KILL 3 also fired and is not amendable, and the controls prove the
two deaths are independent:

- Trunk death (KILL 3's cause): B1, the identical MoE container with P1's un-merged
  trunk, is 5.8x better on code and 3.1x better on prose than B; the pure-trunk controls
  show the merge destroying function on its own (A 971x/305x off the specialists; A_LIN
  4.9x/10.4x). A BAR-trained router cannot rescue spec-B because the trunk it would
  route inside is itself destroyed.
- Router death (KILL 2's cause): under B1's healthy trunk, all-expert0 routing would
  reproduce P1 exactly (14.28 prose), yet B1 measures 870.88 - the 70-82% of tokens the
  flat router sends to P2's FFN inside P1's trunk carry all of that damage. Wrong-parent
  FFN insertion at this divergence (FFN cosine 0.41) is chimeric, not compositional.

Root cause was visible at the gate: same-base by config/tokenizer/hash, but FFN cosine
0.41 means the parents are reproductively isolated by convention conflict (Evolution of
Sex, arXiv:2609.18560, predicts exactly this failure mode). The gate screened only for
too little specialization (cosine > 0.99 abort); it needs a lower bound (merge-window
roughly 0.9 to 0.99), or branched-off-one-checkpoint parents (BTX regime), or alignment
transforms first (PLeaS / Scaling-LMC, arXiv:2606.23607). TIES was also the wrong dense
baseline for this pair (A_LIN beats A by 199x/29x; consistent with arXiv:2607.11997's
method-by-parent interaction).

Novelty scoping per PopEvolution (arXiv:2503.01155): this run claims nothing about
population evolution (scooped at 2B on one 4090). The claim space tested was the EXPORT
FORM: training-free FFN-verbatim MoE + fitness-initialized router + local CPU runtime.
That form is dead at v0 on this pair, for the two independent reasons above.

## FEED RERUN (2B, E=4, Q4_K_M, llama.cpp Vulkan): NOT TRIGGERED, NOT JUSTIFIED NOW

The door did not feed, so per the spec the GPU rerun does not schedule. If a future pair
inside the divergence window feeds, the rerun costs: two ~1.5-2B parent pulls (~6 GB),
E=4 build (~12-16 GB fp32 peak RAM, one artifact at a time), GGUF Q4_K_M conversion,
tok/s logged against the best dense parent at the same quant on the gfx1010 box; hours
of local compute, zero paid API spend. The cheaper and better-ordered next probes on
CPU first: (1) re-run this falsifier with parents inside the cosine window (e.g., two
fine-tunes of one base), (2) B1 form + BAR-style lightweight router training or HARC
calibration to test the fallback arm.

## DEVIATIONS LEDGER (all honest, all named)

1. pip lines: the spec's bare installs would churn the shared estate venv (mergekit
   wants transformers 5.12.1, pydantic 2.10.6, plus accelerate/peft; datasets wants
   fsspec 2026.6.0). Executed instead: pip install --no-deps datasets dill multiprocess;
   pip install --no-deps mergekit; pip install --no-deps immutables; pip install
   --no-deps accelerate==1.6.0 peft==0.21.2. transformers 5.15.0, pydantic 2.13.4,
   fsspec 2026.7.0, torch 2.13.0+cpu all untouched.
2. mergekit 0.1.4 is installed but unusable here: mergekit.moe / mergekit.merge raise
   PydanticSchemaGenerationError (torch.Tensor fields under pydantic 2.13.4). Fixing
   needs the pydantic downgrade refused in deviation 1. The spec's fallback was used:
   hand-rolled TIES for A, hand-rolled router init for B. The router convention mirrors
   mergekit source verified on disk (router.py: unit-L2 rows, hidden_states[:-1],
   sequence-mean for hidden_avg) with one spec-mandated difference: prompts run through
   each parent's own forward, not one base model.
3. TIES scope decision: matrices TIES; norms, q/k/v biases, tied embedding linear mean.
   No base checkpoint exists in the artifact set, so TIES ran on raw weights (the spec's
   hand-rolled clause names no base either).
4. transformers 5.15 container facts: experts are fused 3D tensors (filled accordingly);
   the always-constructed shared expert is neutralized exactly (zeroed down_proj, size
   64); norm_topk_prob=True for full-weight top-1; qkv_bias=True carries parent biases.
5. Instrument bug, found and fixed mid-run: the first window's mask under-scored 511
   tokens (negative slice index). P1's first pass (19,489 tokens) was discarded, the
   instrument fixed, P1 re-run; results.jsonl contains only fixed-instrument lines
   (19,999 tokens each).
6. Sliding window: canonical stride-256 recipe; 19,999 of 20,000 tokens scored (first
   slice token is unpredictable by construction); 78 windows per slice.
7. Attribution controls A_LIN and B1 were added beyond the spec (named above); the
   verdict's rule arithmetic uses only the spec artifacts.

## RECEIPT FILE INVENTORY

memory/runs/mate_moe_v0/: gate_receipt.json, build_A_receipt.json,
router_stats_receipt.json (+ router_stats.pt), build_B_receipt.json, slices_receipt.json
(+ slice_scode.pt, slice_sprose.pt), controls_receipt.json, results.jsonl (12 lines),
verdict_computation.json, VERDICT.md, scripts/s0_gate.py .. s7_verdict.py.
