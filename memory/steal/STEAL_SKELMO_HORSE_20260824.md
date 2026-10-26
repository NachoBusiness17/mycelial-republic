# STEAL — SkelMo: the horse made literal (deterministic skeleton + stochastic motion) (2026-08-24)

**Date:** 2026-08-24
**Commitment:** `steal-skelmo-horse-001`
**Method:** steal the INVARIANT, not the DNA. No diffusion model, no graphics runtime, no 20k dataset.
**Source:** https://arxiv.org/html/2606.01518 — SkelMo: Universal Skeletal Motion Generation for 3D
Rigged Shapes (Tao, Yao, Liu, Wu, Hou — CityU HK, cs.CV, June 2026).

## What the paper actually does

SkelMo animates ANY rigged 3D shape (human, quadruped, dragon, drawer) from a 2D driving video,
with no per-species template. Four moves:

1. **GLOBAL COORDINATES, NOT RELATIVE** — it diffuses in global xyz joint positions instead of
   relative rotations. Ablation: relative representations → "floating" artifacts, broken limb
   lengths, lost ground contact. Global → robust, universal geometric language.
2. **PERSISTENT STRUCTURAL PRIOR, INJECTED AT EVERY STEP** — the rest-pose skeleton is
   concatenated with the noisy latent at EVERY diffusion step t. The bones are never absent from
   the stochastic process; they anchor it and prevent anatomical distortion.
3. **SKELETAL ATTENTION (topology-aware correlation)** — self-attention weights are modulated by a
   tree-based distance matrix from the skeleton graph: parent–child joints stay correlated. The
   structural relationship is computed from the TOPOLOGY, not from observed agreement.
4. **SKINNING-AWARE SEMANTIC INJECTION + BIDIRECTIONAL FUSION** — visual features are projected
   onto the mesh surface, aggregated to joints through skinning weights (each joint = a localized
   aggregator of its body part's semantics), and then cross-attended BOTH ways: skeleton queries
   video (motion cues) AND video queries skeleton (topology constraints). Ablation: removing
   either direction degrades fine alignment.

Plus IK post-processing: raw outputs are re-projected onto the skeleton so bone lengths are never
violated (no stretching).

## The lens: this IS the horse

The operator's mind's eye (2026-08-24): "The running horse in my dream is all of them working in
tandem becoming greater than the sum of their parts — my mind's eye for understanding the
stochastic versus deterministic." The Rocinante image: a running horse with its bones drawn inside.
SkelMo is that image as an architecture:

- The **skeleton** = our deterministic shape (verkle chain, module map, invariant lattice, RIBs).
- The **diffusion/motion** = our stochastic life (seats, reasoning, novel exploration).
- The bones do NOT stop the running — they are injected into it at every step, which is what lets
  it run without collapsing. Deterministic isn't the opposite of stochastic life; it's the frame.

## Self-steal (do not rebuild — we already wrote this)

- **Global coordinates, not relative** = "SEATS RECEIVE COORDINATES, NOT PAYLOADS" (own-tokenizer
  moonshot). Our canonical hashes / RIB handles / flock positions are the global xyz; the paper
  confirms the choice against relative-template representations. Self-steal validation, no change.
- **Persistent structural prior at every step** = the FROZEN_PREFIX / work_contract.BRIEF /
  standing invariant injected at every call (fuel_feed, ox_resident). Already standing-wave.
- **Topology-aware correlation** = our error-independence invariant n* = n/(1+(n-1)rho). The paper
  sharpens it: the correlation is STRUCTURAL (compute rho from the topology graph / lineage), not
  just statistical (observed agreement). TAKE this sharpening.
- **Bidirectional fusion** = the organism-loops steal (percolate improvements up, steer down;
  meta_percolate.feed_back routes the one back into the swarm). Ablation confirms both directions
  are load-bearing. Already built this session.
- **IK post-processing (re-project onto skeleton)** = the quality gate / verify-gate / "never let
  the reply overwrite the envelope." Already built.

## External-steal (the genuinely new atom)

TAKE — **the skinning matrix: surface semantics aggregated INTO the atoms.** In SkelMo, each joint
is a localized aggregator: W[joint, vertex] maps the mesh surface onto the skeleton, so every
coordinate carries the semantics of the body part it is skinned to. Our coordinates (RIBs, cores,
verkle leaves) are currently thin handles; the paper's move is to skin each atom with the surface
it belongs to. That is the natural enrichment of the HOT LATTICE: the lattice preloads on RIB
coordinates, and the skinning weights tell the lattice WHICH surface content is attached to WHICH
atom — so preload carries semantics, not just addresses.

REFUSE:
- A diffusion model, a graphics pipeline, a 20k 3D-animation dataset, AutoRig-Pro. Mag is not a
  lab scrape; we do not mint a skeleton dataset to learn how to draw bones we already own.
- Per-case optimization (their §1 critique) — that is the ad-hoc fresh-brief escalation we already
  replaced with cache-aware escalate_cached.
- Relative representations of any kind (their ablation is our confirmation).

## Plain English

A graphics lab, trying to animate any creature from any video, rediscovered the same law we live
by: a fixed skeleton injected at every stochastic step, coordinates not templates, structure and
signal fused both ways. They spent 20k curated animations learning it; we already wrote it as
invariants. The one thing worth taking is the skinning matrix — how the surface's meaning gets
bound onto the bones.

## Rope

Global coordinates, bones at every step, structural correlation, bidirectional fusion. We hold all
four; the fifth (skinning) is the only new bone. Take the weighting idea; refuse the dataset.

## Ordered adaptations (cheapest first)

1. Fold this steal (self-steal confirmation + the correlation-sharpening + skinning as the open
   atom). Deterministic, $0.
2. When the hot lattice is next touched: define a skinning matrix from existing content (which
   corpus/surface items map to which core/RIB) so each atom's preload carries its surface
   semantics. Reuse what exists — do not build a new mapping store from nothing.
3. No new runtime, no model, no dataset.
