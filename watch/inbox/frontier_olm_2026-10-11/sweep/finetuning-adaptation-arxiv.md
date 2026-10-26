# Frontier sweep: finetuning-adaptation via arXiv (2026-10-11)

source-fetched: 2026-10-11. Gopher: sweep-finetuning-adaptation-arxiv (dwfrun actor_3_17).
Ask: 4 research questions over the adhoc run's 8 confirmed finetuning-adaptation finds
(frontier_olm_2026-10-11/lens/burns.md:103-104, pointing at frontier_olm_adhoc/register.jsonl),
the JIT fine-tuning law coinage (lens/burns.md:153-154), Universal Weight Subspace
(lens/burns.md:146), and the Dead Salmons card (lens/burns.md:147-148). House laws held:
ascii only in my own prose, no em or en dashes, every claim cites what was read or run
this sitting; verbatim quotes from sources keep their own characters.

## 1. Doors run this sitting (instruments)

- 8 arXiv export API queries via WebFetch, all returned Atom XML clean (no 403, no
  degradation), each filtered to submittedDate:[202609110000 TO 202610112359] and sorted
  submittedDate descending: (a) cat:cs.CL OR cs.LG + abs:"parameter-efficient" =
  totalResults 96; (b) abs:"LoRA" = 297; (c) abs:"test-time training" = 28;
  (d) abs:"model merging" OR abs:"weight subspace" = 36; (e) abs:"catastrophic
  forgetting" = 73; (f) abs:"continual pretraining" OR "continued pretraining" = 26;
  (g) abs:"on-policy distillation" = 177; (h) abs:"context to weights" OR
  "context-to-parameter" OR "memory into weights" OR "internalize context" = 12.
- abs pages fetched: arxiv.org/abs/2512.05117 and arxiv.org/abs/2512.18792 (section 4).
- HTML full texts fetched and read end to end: 2610.09639v1, 2610.05076v1, 2610.11291v1,
  2610.05200v1, 2610.07819v1, 2610.11715v1 (the six new banks, section 3), plus
  2610.11655v1, 2610.09122v1, 2610.09835v1 (dedupe reads of already-banked items,
  section 2).
- Disclosed deviation from the fetch recipe: the recipe's /list/cs.CL/recent and
  /list/cs.LG/recent listing pages were NOT fetched. The recipe also names the
  date-windowed export API, and that door answered the 30-day window directly with
  totalResults counts, so the listing pages were redundant. No fallback success is
  claimed for them.

## 2. Pass 1 census and the four-pass dedupe map

This area has been swept FOUR times before this sitting; every dedupe below is from
greps run this sitting against the lanes' files and catalog/catalog.jsonl:

- 10-06 lane: deep-read 2610.06542 (LoRA landscape) and 2610.05303 (ASCENT)
  (watch/inbox/frontier_olm_2026-10-06/sweep/finetuning-adaptation-arxiv.md:209-224);
  deep-read 2609.34924 (Audit the Scaffold) under evals-self-improvement
  (its sweep/evals-self-improvement-arxiv.md:80).
- 10-08 lane: deep-read 2610.09835 (Deafening Silence)
  (frontier_olm_2026-10-08/sweep/finetuning-adaptation-arxiv.md:100).
- 10-09 lane: 24-row register; finetuning-relevant confirmed rows: 2610.11655 (Harness
  Evolution, register row 1 of its file, "THE RQ3 ANSWER" at its sweep file :24-66),
  2610.09122 (PEFT methods, register.jsonl:22), 2610.06542, 2610.09934 (Itgan),
  OnlineQAT, LoRA's Second Descent, radiology-report fine-tuning comparison, LoRA over
  GGUF (reddit); its pass-1 candidate list names 32 more on-topic IDs
  (frontier_olm_2026-10-09/sweep/finetuning-adaptation-arxiv.md:12) including 2610.11715
  and 2610.11620, neither deep-read by that lane.
- adhoc run (folded 2026-10-11): 8 confirmed finetuning-adaptation rows
  (frontier_olm_adhoc/register.jsonl, grep -i finetuning = 8 rows): 2607.03441 (aTTT),
  2610.12002 (Agentic-TTT), 2610.11776 (DPPM), 2610.11659 (DIAL-OPD), 2610.12367
  (SGUID) on arXiv, plus three reddit finds (MedGemma 1wywscq, MOLT 1wyvc8k, AgileRL
  1wdjk0y).
- Today's sibling HN-door sweep for this same area
  (frontier_olm_2026-10-11/sweep/finetuning-adaptation-hn.md): grep for my six IDs
  returns zero hits; no collision.

Pass-1 candidates considered this sitting (35 named from the query outputs above, beyond
the prior-banked set): 2610.11076, 2610.09122*, 2610.11655*, 2610.09835*, 2610.08669,
2610.08049, 2610.06542*, 2610.06243, 2610.05800, 2610.07036, 2610.05318, 2610.01702,
2610.02283, 2610.00928, 2610.00685, 2610.00431, 2610.11715, 2610.11620, 2610.11231,
2610.11160, 2610.10349, 2610.10345, 2610.07553, 2610.07518, 2610.06765, 2610.06387,
2610.09772, 2610.12002*, 2610.11659*, 2610.11776*, 2610.12367*, 2607.03441*, 2609.34924,
2609.39405, 2609.40089, 2609.27262, 2610.07819, 2610.09639, 2610.05076, 2610.05200,
2610.11291, 2610.11373, 2609.34924 (* = already banked by a prior lane, listed for the
dedupe map, not re-banked). Plus the eight OPD-family items (2610.11989, 2610.11529,
2610.11519, 2610.11332, 2610.11247, 2610.11167, 2610.10878, 2610.10460) and merge-family
items (2610.07990, 2610.03199, 2609.24517, 2609.22886, 2609.24612) read at title level
only from the query output; not banked, not read beyond titles this sitting.

## 3. Pass 2 deep reads: the six NEW banks (strongest first)

### 3.1 On-Policy Distillation Teaches New Skills but Not New Knowledge (2610.09639, 2026-10-07)

https://arxiv.org/abs/2610.09639 - full HTML read (arxiv.org/html/2610.09639v1).
source-fetched: 2026-10-11.
Quote: "replacing reverse KL with forward KL substantially increases single-step greedy
accuracy: from 10.95% to 54.10% in Qwen3-4B, and from 32.95% to 94.10%".
Setup: Qwen3-0.6B/4B, Gemma-2-2B, OLMo3-7B students; synthetic lookup-table "facts"
(unguessable digit-pair mappings) chained into multi-step tasks; 2x2 factorial over
prefix source (student vs teacher) and KL direction; real-world check on Knowledge-2026
(809 post-cutoff QA) and Math-2026 (201 problems). Key numbers: skill transfer under
reverse-KL OPD 79.10% vs 0.72% baseline on unseen tree structure; new-fact transfer
13.12% under the same objective; reverse-KL OPD lifts math reasoning +6.47 points with
zero factual-recall gain; LoRA weight analysis shows factual and skill updates
near-orthogonal (cosine 0.004-0.046), facts concentrating in final layers (peak layer
35), skill in early/middle layers (peaks 3 and 11).
Why it matters: this is the JIT law's missing axis. The law says fine-tuning delivers
detected-pitfall bypasses "just in time"; this paper measures that WHAT the weights
absorb is gated by the training objective, not just by the corpus: procedural food
transfers through mode-seeking reverse KL, factual food needs forward KL. It also hands
lora_pipeline a measurable design fact (fact/skill updates are near-orthogonal subspaces,
depth-specialized), which is the same decomposition Universal Weight Subspace claims at
corpus scale (section 4).
Overlap: grep catalog/catalog.jsonl = 1 row, the ingest stub
local_sovereign_agent/state/arxiv/2026-10-08/2610.09639v1.txt (title+abstract only);
zero hits in any lane sweep/register (targeted grep over 10-06..10-11 lanes run this
sitting); git grep over tracked memory/ = zero hits; the only memory/ hit is
memory/trajectory/steps.jsonl rows stamped this session (session_id
sess_dwf-dwfrun-af85b9b8-3c33-4975-b386-e1079a88d86b-actor_3_17, ts 2026-10-11T16:45Z),
i.e. my own step log. New analysis is this sitting's.

### 3.2 Self-Generated Feedback Destabilizes Test-Time Training (2610.05076, 2026-10-04)

https://arxiv.org/abs/2610.05076 - full HTML read (arxiv.org/html/2610.05076v1).
source-fetched: 2026-10-11.
Quote: "Fixed Generation removes over 98% of the damage at 125M and 760M by using a
frozen model to generate training chunks."
Setup: TTT-E2E models (125M/760M/3B, DCLM+PG-19) plus Qwen3-4B and Qwen3.8-27B agents;
128K-token streams mixing real text and ~105 self-generated chunks; causal decomposition
via Fixed Generation (frozen generator), Recorded Replay, and paired one-update
keep/discard branches; "Settlement" validates candidate states on independent real text.
Key numbers: retaining updates lowers source NLL but raises next-real-passage NLL in
every row; damage concentrated (4 of 24 source sequences caused all write costs above
0.5 nats); gradient conflict between generated-chunk and real-text gradients predicts
harm (correlations -0.50 to -0.79); Settlement closes the endpoint gap (0.07 nats at
125M, -0.02 at 760M, both intervals including zero); real-text writes help (+0.034 to
+0.35 nats).
Why it matters: this is the JIT law's dead-salmon rider (CARD.md:30-31: "a pitfall must
be DETECTED under controls before its bypass is food, else you fine-tune on phantom
pitfalls") turned into a measured causal mechanism, with the control arms named: frozen
independent generator for the corpus, validation on independent real text before a state
is kept. For an estate that mines its own traces, the paper is the falsifier for any
self-supervised adaptation loop: unverified self-output as training food is not neutral,
it accumulates.
Overlap: grep catalog/catalog.jsonl = 0 rows; zero lane sweep/register hits; git grep
tracked memory/ = zero. Completely absent from the estate before this sitting.

### 3.3 When Do We Need On-Policy Distillation? Distilling on Offline Student Rollouts Is Often Better (2610.11291, 2026-10-08)

https://arxiv.org/abs/2610.11291 - full HTML read (arxiv.org/html/2610.11291v1).
source-fetched: 2026-10-11.
Quote: "Semi-OPD outperforms OPD in 14 cases, with up to +13.6% accuracy and 11.4×
training speedup." (quote kept verbatim from the paper's HTML, multiplication sign
included).
Setup: 17 teacher-student pairs (1.5B-235B) across Qwen3, DeepSeek-R1-Distill,
Nemotron-Cascade-2, thinking and non-thinking; DAPO-Math-17K; AIME 2024/2025/2026 and
HMMT Feb 2026 at avg@32; Semi-OPD samples rollouts once from the initial student, then
trains offline. Cost table (H100-hours per 100 steps): Qwen3-1.7B pair OPD 56.8 vs
Semi-OPD 5.0 (11.4x); Qwen3-4B 199.1 vs 31.0 (6.4x); 14B thinking 480.0 vs 63.0 (7.6x).
Key numbers: teacher-student overlap correlates with OPD's advantage (Pearson r = -0.73
across 17 pairs); OPD needed only for high-overlap pairs; Semi-OPD trailed OPD on 3 of
17 pairs by 0.1-2.6%.
Why it matters: the descent protocol's cheap-first leg (AGENTS.md:37: "SHERPA cheap-first
... before any $0.4+ premium ask") formalized for the weight lane: measure alignment
first, pay for on-policy machinery only where overlap is high. The same routing logic
transfers to any premium-vs-cheap adaptation ask.
Overlap: grep catalog/catalog.jsonl = 1 row, the ingest stub
state/arxiv/2026-10-09/2610.11291v1.txt; zero lane hits; git grep tracked memory/ = zero.

### 3.4 Learning without Overwriting: A Theory of Self-Distillation and Supervised Fine-Tuning in Continual Reasoning (2610.05200, 2026-10-04)

https://arxiv.org/abs/2610.05200 - full HTML read (arxiv.org/html/2610.05200v1).
source-fetched: 2026-10-11.
Quote: "SFT on correct reasoning paths can lead to catastrophic forgetting due to dense
updates along the training paths, which overwrite the information previously acquired."
Setup: CoT-as-DAG theory (RIKEN/U.Tokyo, Uemura and Suzuki); synthetic reasoning graph,
4 sequential tasks; hint-conditioned on-policy self-distillation (SD, stop-gradient on
the hint's source) vs SFT on teacher paths; correct-generation probability over ten
seeds; code repo "continual-reasoning-experiments". Key numbers: SD preserves each prior
task's performance during subsequent-task training while SFT drops tasks 1-3
significantly; SD's gradient is zero except at hint-source nodes (Theorem 3: earlier
tasks' correct transitions never decrease); SFT overwrites exactly where old and new
correct paths conflict (fraction theta of paths); pre-training diversity governs
restartability from intermediate states (Proposition 1).
Why it matters: the mechanism-level twin of the rib append-never-rewrite law
(memory/rib/RIB_MD_RECORD_20260921.md:14-17, via lens/laws.md:26): hint-gated sparse
updates leave prior competence untouched, dense SFT overwrites conflicts. It tells the
estate WHAT SHAPE the JIT food must take if weights are ever touched: bypasses delivered
as hints at the model's own decision points, not dense path supervision.
Overlap: grep catalog/catalog.jsonl = 0 rows; zero lane hits; git grep tracked memory/ =
zero. Absent from the estate before this sitting.

### 3.5 αTransfer: Coefficient Transfer for Efficient Model Merging (2610.07819, 2026-10-06)

https://arxiv.org/abs/2610.07819 - full HTML read (arxiv.org/html/2610.07819v1).
source-fetched: 2026-10-11.
Quote: "achieves zero performance degradation for both Task Arithmetic and TIES-Pairwise
on the 4B scale".
Setup: merging coefficients (per-task/per-layer alpha) optimized on a small proxy model
transferred to a larger target in the same family; Appier AI Research + NTU. Key
numbers: 20x speedup and 85% memory reduction on LLM merging search, 6x/70% on ViTs;
correlation rho up to 0.94 across proxy-target pairs; weakest cell ViT-B/32 to ViT-L/14
(rho = 0.58, patch-size difference blamed); hybrid search as fallback.
Why it matters: Universal Weight Subspace's guild mechanic (unisub_drop_20261010/CARD.md
steal list: "coefficient federation - local fine-tunes exchanged as subspace coefficients
over the mesh") gets its cost point: coefficient search does not need to run on the big
model at all, it transfers down-family. Note the paper never mentions spectral subspaces;
it is task-vector arithmetic, adjacent to unisub, not a replication of it.
Overlap: grep catalog/catalog.jsonl = 1 row, ingest stub
state/arxiv/2026-10-07/2610.07819v1.txt; zero lane hits; git grep tracked memory/ = zero.

### 3.6 Internalizer: Portable Context-to-Parameter Mapping for Very Large Language Models (2610.11715, 2026-10-08)

https://arxiv.org/abs/2610.11715 - full HTML read (arxiv.org/html/2610.11715v1).
source-fetched: 2026-10-11.
Quote: "At 8192 tokens adapter accuracy has fallen back to roughly the base model's
level" (their own boundary sentence on extrapolation past the trained window).
Setup: a model-agnostic hypernetwork reads per-layer hidden states of a context passed
through a frozen 284B LLM, Perceiver-compresses (layer, chunk) latents, decodes LoRA A/B
rows onto gated-MLP projections, concatenates chunks along the rank axis (rank-16(k+1));
one forward pass produces the adapter; only the hypernetwork trains. Key numbers:
84.9% top-1 / 97.8% top-5 teacher-forced accuracy vs 63.4% / 83.5% for the base model;
warm-started trunks pass 90% top-1 within budget while cold starts stall below 75%;
trunk trained on 1-3B models fit the 284B target via thin entry/exit layers; at 16,384
tokens accuracy collapses to 22-25% top-1; PG-19 out-of-domain prose internalizes worse
(81.0% vs 86.2/87.5%).
Why it matters: the DPPM-class context-to-weight door (adhoc register row 6) at 70x the
parameter scale, with the boundary priced: internalization wins inside the trained
window and hands ownership back to retrieval outside it. That is the JIT law's
retrieval-vs-weights trade (CARD.md mapping 2) with a number on the edge.
Overlap: grep catalog/catalog.jsonl = 1 row, ingest stub
state/arxiv/2026-10-09/2610.11715v1.txt; pass-1-listed by the 10-09 lane
(frontier_olm_2026-10-09/sweep/finetuning-adaptation-arxiv.md:12) but never deep-read by
any lane (absent from every register); git grep tracked memory/ = zero. The full read is
this sitting's.

## 4. The named papers, verified first-hand this sitting (not re-banked)

### 4.1 Universal Weight Subspace (arXiv 2512.05117) - one factual delta vs the card

abs page fetched 2026-10-11. Title/authors match the card (Kaushik, Chaudhari, Vaidya,
Chellappa, Yuille; JHU). Version history: v1 2025-12-04, v2 2025-12-06, and a NEW v3
2026-10-05 (the card, written 2026-10-10, records v1/v2 only). Two deltas from the
current v3 abstract, both OWED-flags for the probe: (1) the v3 abstract reads "over 1200
models" where the card says "1100+ models"; (2) my read of the current abstract does not
find the card's "100x compression" or "train by optimizing coefficients" wordings - the
current application sentence is "Furthermore, this inherent structure has significant
implications for model reusability, multi-task learning, model merging, and the
development of training and inference-efficient algorithms". Those claims came from the
v1/v2 abstract and the project site per the card; before the spectral-overlap probe
fires, re-read v3 end to end and re-anchor the claims.

### 4.2 Dead Salmons of AI Interpretability (arXiv 2512.18792) - matches the card

abs page fetched 2026-10-11: single version v1 2025-12-21; authors Meloux, Dirupo,
Portet, Peyrard (card matches); fix quote on the page: "explanations of computational
systems should be treated as parameters of a (statistical) model, inferred from
computational traces". No delta vs dead_salmon_airllm_drop_20261010/CARD.md.

## 5. The four research questions

### RQ1: do the 8 confirmed finds refine, contradict, or restate the JIT law - is it evidence-backed or still coinage?

Verdict: REFINE, with convergent third-party support, no contradiction - and still
operator coinage until the law's own falsifier fires. The law's text and falsifier:
watch/inbox/fine_tuning_jit_law_20261010/CARD.md:3-5 (coinage verbatim) and :43-45
("if a fine-tune built only from a controlled pitfall-bypass corpus does not beat
prompt-only on the held-out pitfalls, the JIT framing overclaims and it is just
distillation wearing a clock"). Reading the 8 adhoc rows against the law's claims:

- Timing/mechanism evidence (the law's core claim "same food, different serving time"):
  aTTT 2607.03441 is the strongest leg - matched-update-text experiment (same text as
  adapter update 54.3% vs in-context injection 49.3%) plus the JIT serving shape
  (runtime LoRA hot-swap, 1.9x overhead) and an honest bound (preserves competence,
  does not teach new abilities). DPPM 2610.11776 prices the compression side (history
  compiled to LoRA beats full context and runs 62.7x faster). Agentic-TTT 2610.12002
  supplies the WHEN gate and its 03:00Z-drain twin (overuse without a compute penalty).
- Food-selection refinements: DIAL-OPD 2610.11659 (select tokens, teacher scale is not
  the lever) and SGUID 2610.12367 (unselected co-evolution DEGRADES: -0.3 naive vs
  +1.1 selected on Qwen3-4B HMMT25) both refine the pitfall-bypass-corpus claim; the
  MedGemma row adds a serving-layer bound the law lacked (merge attenuation: 83.8%
  agreement post-merge, ~2x alpha/r effective scale under Unsloth, bf16 merge rounding
  erasing 17-37% of delta elements) - the just-in-time idea can arrive attenuated.
- Pure restatements: MOLT (fit tests/checkpoints/base-vs-adapter eval = the improve
  lane in miniature) and AgileRL Arena (tooling shelf) restate infrastructure, not the
  law.
- What was missing until this sitting: no row ran the falsifier itself. My new reads
  close the mechanism gap from the outside: 2610.09639 shows the OBJECTIVE gates what
  weights absorb (skills yes, new facts no, under reverse KL), 2610.05200 shows
  hint-shaped food preserves while dense SFT overwrites, 2610.05076 shows unverified
  self-generated food actively damages - so the law's rider (detected under controls)
  is now mechanism-backed, but the estate's controlled pitfall-bypass corpus has never
  been built or fired. Status: evidence-adjacent coinage. The falsifier remains the
  single experiment that would promote it to law.

### RQ2: does Universal Weight Subspace change lora_pipeline, and is it compatible with the ignore-DeepGEMM standing state?

Grounding: lens/graph.md:22 records module:lora_pipeline at degree 5; the module is
mag/lora_pipeline.py (562 lines; read this sitting via ls/grep: HardwareProfile,
detect_hardware, generate_training_config, _batch_size, generate_training_script,
tokenize_function, pipeline_status - it is a local training-config/script generator; my
grep -in deepgemm over it returned zero matches). Compatibility: YES, trivially.
DeepGEMM is an FP8 grouped-GEMM runtime that pays only on SM90/SM100 NVIDIA
tensor-core arch, and the standing state "Ignore DeepGEMM itself on this box" is
explicit (memory/rib/RIB_GPU_LADDER_20261001.md:5-8 gates context, :11-23 the five
gates, :27-31 the standing verdict). Unisub's method is mode-wise spectral analysis of
weight deltas (SVD/eigendecomposition class) plus coefficient optimization - small
matrix math with no FP8/tensor-core dependency, runnable on this box's RDNA1 GPU or
CPU. No GPU-ladder gate is touched. Design delta for lora_pipeline, sized honestly:
not a rewrite. The pipeline gains (a) an adapter-exchange format (delta -> SVD ->
coefficients, and merge-from-coefficients) if the guild-federation mechanic is ever
built, and (b) a spectral-overlap probe (the card's own steal list, one evening) on two
public LoRA adapters from disjoint tasks, falsifier: top-k principal directions of the
deltas align better than chance. Adjacent support banked this sitting and prior:
2610.09122 (10-09 register) found adapted singular BASES carry the task while
restoring pretrained singular VALUES preserves it - the same basis/value decomposition
unisub claims; 2610.07819 (new, section 3.5) shows merging coefficients transfer
down-family at rho up to 0.94, which lowers the compute bar for coefficient exchange.
Caveat carried from section 4.1: the card's 100x-compression and coefficient-training
claims need a v3 re-read before they anchor any design.

### RQ3: evidence threshold for a premium turn on actual weight adaptation (descent cheap-first leg)

The threshold is an INSTRUMENT, not a paper count. AGENTS.md:37 leg 1 demands the cheap
baseline (~$0.001 deepseek/local) and the prior-art sweep before any premium ask; the
prior-art sweep is now done four times over (10-08, 10-09, adhoc, this sitting), and
the sweep's convergent picture defines the gate sequence:

1. Corpus gate: build the controlled pitfall-bypass corpus from the compost/pitfall
   registry (JIT card mapping 3) with detection evidence per row and the 2610.05076
   controls (frozen independent generator for the food, settlement validation on
   independent held-out text). Unverified self-output as food is measured harmful, so
   this gate is binary.
2. Cheap-run gate: one local LoRA run, Qwen3-4B class (the scale all three 2026
   weight-adaptation papers used), with the 2610.11655 placebo design (10-09 register,
   confirmed find: "a placebo adapter trained on answer-shuffled trajectories falls
   below the base model, so the gain is in the trajectory content") on held-out
   pitfalls vs prompt-only. That is the JIT law's falsifier, run at SHERPA cost.
3. Premium trigger: only if the cheap run shows a real placebo-verified gap AND the
   residual failure class is judgment-shaped (content failures dominating delivery
   failures, the 2610.11655 trigger) does a premium turn buy anything - and 2610.11291
   says measure teacher-student alignment first (r = -0.73): the premium method is the
   exception, the offline/cheap variant is the default.
So: the 8 rows plus this sweep's 6 justify building and firing the falsifier cheaply
NOW; they do not justify a premium weight-adaptation turn before the falsifier's local
run lands. A premium turn justified only by more paper reading would be spend theater
by the descent protocol's own falsifier (AGENTS.md:37: "a descent week where the ledger
grew but no rib/pack/receipt carries a frontier contribution forward").

### RQ4: Dead Salmons - applicable to the estate's adaptation failure modes, or pure landscape?

Applicable, and already load-bearing; the card itself made the mapping
(dead_salmon_airllm_drop_20261010/CARD.md:15-29: trust-bytes, falsifier law,
suppression-topology negative-control amendment, citation-lint PHANTOM-NUMBER
parallel). This sitting adds the adaptation-specific cash-out: 2610.05076 is the dead-
salmon artifact INSIDE adaptation loops - plausible-looking self-improvement that
measures well on its own generated text and damages real text - with the exact control
battery (frozen generator, independent real-text settlement, gradient-conflict
prediction, concentration check). Combined with 2610.11655's placebo adapter and
MOLT's base-vs-adapter eval (adhoc row 2), the estate gets a concrete protocol: any
weight-adaptation instrument must carry (a) a random/shuffled-control arm (placebo
adapter), (b) an independent-generator arm for self-mined food, (c) held-out real-text
settlement. The MedGemma row (adhoc row 1) is a third failure class the paper does not
cover - not phantom signal but real signal lost in serving - so the eval must sit
downstream of the merge, not upstream. Not pure landscape.

## 6. Anti-rebank for the next window

1. Do not re-bank: 2610.11655, 2610.09122, 2610.06542, 2610.05303, 2610.09835,
   2609.34924, 2607.03441, 2610.12002, 2610.11776, 2610.11659, 2610.12367, 2610.09934,
   2610.09346, or any subject of the adhoc register's 8 finetuning rows or the reddit
   rows (MedGemma/MOLT/AgileRL).
2. This sitting's new set: 2610.09639, 2610.05076, 2610.11291, 2610.05200, 2610.07819,
   2610.11715.
3. Opened, do not re-derive: unisub v3 re-read (section 4.1); the JIT falsifier design
   (section 5 RQ3); the merge-attenuation guard as a lora_pipeline eval step.

## 7. Receipt (commands run this sitting)

- Local reads: frontier_olm_2026-10-11/lens/{burns,graph,laws,corpus}.md (full);
  frontier_olm_adhoc/lens/{burns,graph}.md (full); frontier_olm_adhoc/register.jsonl
  (grep -i finetuning = 8 rows, read in full); fine_tuning_jit_law_20261010/CARD.md,
  unisub_drop_20261010/CARD.md, dead_salmon_airllm_drop_20261010/CARD.md,
  memory/rib/RIB_GPU_LADDER_20261001.md (all full); mag/lora_pipeline.py (symbol
  listing + wc + deepgemm grep).
- Greps: `grep -c <id> catalog/catalog.jsonl` for 14 IDs (results in section 2/3);
  catalog path extraction greps; lane greps over
  frontier_olm_2026-10-{06,07,08,09,10,11}/sweep+register+DIGEST and
  frontier_olm_adhoc/sweep+register for all banked IDs; `git grep -lF <id> -- memory/`
  for the six new IDs = zero tracked hits (plain grep -rl over memory/ was started,
  confirmed the trajectory self-hit on 2610.09639 with session_id/ts inspection, then
  stopped as too slow on the 577k-row biography tree; the git grep result stands for
  tracked files, and untracked-carrier coverage comes from the lane greps above).
- Web: 8 export API queries, 11 full-text/abs fetches, listed in sections 1-4. All
  returned; none 403'd; no fallback claimed.
- Not run this sitting: any pytest; no catalog FTS check; the unisub v3 full-text
  re-read (flagged OWED, section 4.1); any premium or paid dispatch (none needed).
