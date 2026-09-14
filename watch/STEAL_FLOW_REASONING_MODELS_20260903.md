# STEAL: FLOW REASONING MODELS — our architecture, named in weight-space (2026-09-03)

Source: operator drop, https://x.com/alec_helbling/status/2095498033504940355
Paper: "Flow Reasoning Models" — Helbling, Bryutkin, Martino, Chau, Dehmamy (Georgia Tech /
IBM), arXiv:2606.29150. Author: diffusion/flow PhD, Georgia Tech, NSF Fellow.

## THE PAPER (verified from abstract)
FRMs = "continuous flows over discrete structured outputs with a simple recurrent refinement
mechanism." Self-conditioning a flow model on its own past outputs "turns one-shot denoising
into iterative solution refinement" — decisions revised IN PARALLEL, not sequentially.
Fixed-Point Forcing (FPF) closes exposure bias by "training FRMs on states produced by their
own inference dynamics." Results: 99.5% Sudoku-Extreme, 100% Zebra, 99.9% Maze-Unique —
beating the next-best method with **44× fewer inference FLOPs**. Direct anti-CoT claim:
"autoregressive models commit sequentially and cannot revise earlier decisions."

## THE MAPPING — five point-steals, all tri-state Supported with receipts

1. **THE RECONCILER IS FIXED-POINT FORCING ON INFRASTRUCTURE.** engine_spec.json declares
   desired state; engine_reconciler.py diffs reality and drives it back; repeat until the
   diff is empty. That is FPF's loop verbatim, running on containers instead of weights.
   We built FPF on 09-03 without the name. (watch/engine_spec.json + watch/engine_reconciler.py)

2. **COVERAGE THESIS GAINS ITS WHY.** FRMs refine only what they can see: self-conditioning
   reads the model's own past outputs — no record, no gradient, no refinement. The fleet's
   coverage gap (watch/SYSTEMS_SALON_GAP_MAP_20260903.md: actions that emit no record) is
   exactly missing self-conditioning signal. An unrecorded action is a decision the fleet
   can never revise — the paper's own words damn it: sequential commits that cannot revise.

3. **THE FOLD IS AN FRM IN SOCIAL SPACE.** Salon doctrine: one question, N blind posts,
   fold keeps what survives; percolator iterates 47 invariants; chord theory claims the
   fold beats the best single post. Revise-all-decisions-in-parallel = our ensemble-over-seat
   epistemology. FRM is the weight-space twin; our falsifier-in-residence (chord test, N=12)
   measures whether our "flow" beats our "autoregression."

4. **MAZE-UNIQUE 99.9% = THE LIGHT CODEC VALIDATED IN WEIGHT-SPACE.** Independent lab solves
   discrete mazes with a continuous refined field — the Light Codec thesis (continuous field,
   discrete pieces, steer the interior by writing on the film) now has an external,
   peer-visible existence proof. Our maze_arena walkers already run the same shape at
   runtime: BFS field (continuous) over maze cells (discrete), walkers gradient-follow.
   (watch/maze_arena.html, STEAL_LIGHT_CODEC_20260903, SHADERTOY_SHADOW_FIELDS)

5. **FPF IS THE ROCINANTE TRAINING RECIPE CANDIDATE.** The QLoRA deep compile (campaign
   Stage 5, Rocinante-gated Oct 27) is planned one-shot: corpus → adapter. FPF says: train
   on states produced by the system's own inference dynamics — i.e., fold the maze-keeper's
   OWN room answers back into the training set, iteratively, not the raw corpus once.
   Exposure bias (their stated failure mode) is our stub-passing-gate failure class, named.
   Candidate rung for the deep compile: FPF-style iterative self-conditioning beats
   single-pass SFT on our own tapes. Unproven — needs the run, but the run is a variant of
   the training we already GO'd, not a new one.

## BONUS: the economics rhyme
44× fewer FLOPs via parallel refinement ≈ our lane economics: cheap cached-prefix passes
with ~30-token steer tails beat one giant sequential frontier call. Refinement beats depth
at BOTH scales — model weights and fleet lanes.

## NEXT (cheap, ordered)
1. $0: run the chord test (N=12) — it is literally our FRM-vs-CoT ablation, and it's the
   thesis' biggest DISPOSE debt.
2. Name the pattern in canon: reconciler + spec = "fixed-point forcing on infrastructure"
   (sacred-cows law: steal the bones, name the reinterpretation).
3. Rocinante window: write the FPF training variant into the Stage 5 plan as an explicit
   arm (one-shot SFT vs self-conditioned refinement, same corpus, maze-keeper eval).

Sources: fxtwitter mirror fetch (tweet, 57.3K views, 1,499 likes — Emad Mostaque reposted),
arxiv.org/abs/2606.29150 abstract fetch. Quotes verbatim from abstract fetch, 09-03.
