# CATCH: nvidia/physical-plausibility-evaluator (2026-10-19)

Operator dropped x.com/aitrackerbot/status/2112309371564609650 (automated
release tracker, ~95 views at catch, near-zero engagement). Identified and
carded same sitting.

## What it is

- `nvidia/physical-plausibility-evaluator` on Hugging Face (public since
  09-17, weights newly live, ZERO downloads at catch). NVIDIA Cosmos world-
  model ecosystem. GitHub release "Cosmos Evaluator" scheduled 10/20/2026.
- Architecture: frozen V-JEPA 2.1 ViT-L/16 encoder + attention pooling +
  linear head. Only 2,049 trainable parameters on a ~300M frozen base.
- Input: video only (64 frames, 384x384). Output: bad_logit / bad_score /
  plausibility_score + calibrated good/bad decision. ROC AUC 0.8258 on
  998 held-out Cosmos-generated videos; trained on ~3K FineVideo-derived
  synthetic clips with human 3-level labels.
- License: OpenMDW-1.1 (commercial OK); V-JEPA backbone pulled separately
  under Meta terms. Tested on H100 + PyTorch 2.10/CUDA 12.8; the load is
  light for the parameter count (ViT-L inference).

## Honest read (the card's own caveat)

It is a synthetic-VIDEO quality screener, not a physics oracle: "a passing
score does not certify physical correctness," and it is biased toward
Cosmos-style outputs. It is NOT a text-invariant reality grader for the
percolator. What it IS: a trained, human-labeled reality-anchor instrument
in the visual domain, tiny enough for the local shelf, and a member of the
probe-law instrument class (graded against human labels, not consensus).

## The estate wire

1. Probe lane candidate: run rendered estate exhibits (smith globe RACE
   descent, standing-wave strip, erosion field, maze_arena) through it as
   video clips - a new manifold: does our own simulation layer pass a
   physics grader? Pairs the hand-rolled conservation beat in
   state/probe_water.json with a learned one.
2. Local shelf: 0.3B frozen + 2K trained params; size VRAM on the local GPU
   (not the H100 class, likely sufficient). bob is the alt door.
3. Falsifier for the wire: if estate renders score indistinguishably from
   Cosmos-generated clips' noise floor, the probe manifold is dead and the
   instrument returns to the shelf (no cow).

## Action filed

Queue row [probe] physical-plausibility dogfood: pull the 10/20 GitHub
release, size the VRAM locally, render three estate clips, score them.
