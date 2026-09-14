# BLIND SELF-ANSWERS — Astra witness #2 attack surfaces (2026-09-07, LAW-066 retrospective)

Sealed BEFORE opening memory/runs/salons/ollama_maze_astra_20260907/ASTRA_DESIGN.md.
Exposure disclosure: the CONVO headline summary of witness #2's verdicts was read
("seed survives with amendments; V3 = evidence-bound walk; F1–F6"); the DESIGN PASS's
per-surface treatments were NOT read. Items marked accordingly.

## A1 — The gate definition: walker = trace or distribution? Find the third answer.
Exposure: SUMMARY-EXPOSED base (v2's "fork at the logits" was witness #1's amendment,
already in the prompt); the extension below is UNEXPOSED.

**Blind answer:** neither pole — the renderable object is the REALIZED PATH WITH ITS
COUNTERFACTUAL HORIZON. The walker is the sampled token's walk (trace), but at each step
the sampler's top-k defines the corridors NOT taken; with the logprobs door now REAL
(our own probe, v0.32.7, top-k ≤ 20), those alternatives carry measured masses. So render
the per-step policy tree truncated at top-k: sampled path = lit corridor; alternatives =
ghost-branches with width = logprob mass. The trace and the mid-flight distribution are
the two PROJECTIONS of this one object (marginalize over alternatives → trace; over time →
distribution). The dichotomy dissolves because the tree is the thing; both v2 answers were
projections arguing about shadows of a shape nobody had drawn. Falsifier for this answer:
if top-k masses at consecutive steps don't admit a stable tree rendering (e.g. masses are
so flat the ghost-branches carry no visual information), the tree collapses to the v2
trace-and-fork and my extension is decoration.

## A2 — Multi-head coherence: design the door.
Exposure: UNEXPOSED.

**Blind answer:** when/if attention is ever exposed, do NOT render N lanterns per layer.
Render attention as EDGES — per layer, a bipartite graph between generated positions and
attended past positions, then collapse heads by CLUSTER, not by display: heads cluster into
role-archetypes (K ≈ 4–8 by agreement pattern — the induction-head precedent), each
archetype one lantern color; inter-archetype disagreement renders as haze, not edges.
Noise law: edges drawn only at high-entropy positions (downsample by the field's own
entropy — the sampler tells you where attention is worth drawing). The door itself is a
plugin contract: `attention_source` interface with a null backend (symbolic mask, current
state) and a real backend slot for any future exposure (llama.cpp hook, fork, vendor door)
— the walk never changes when the backend swaps. Guard: O(T) edges per head per layer at
scale; entropy downsampling is load-bearing, not decorative.

## A3 — Field dimensionality: the reduction choice.
Exposure: UNEXPOSED detail (door-open status EXPOSED via our own probe receipt).

**Blind answer:** with top-k REAL, the field is not 150k-vocab and should not be PCA'd at
all. The honest field is the per-step TOP-K SIMPLEX (≤20 dims, measured): render (a) the
top-k mass ridge along the step axis (exact, REAL-labeled), (b) the cumulative entropy
curve (exact), and (c) any semantic scatter of token identities as PROXY-labeled decoration
only — it imports an embedding model's geometry and must never read as measured. The
load-bearing reduction choice is the k cutoff (20), not a projection; say so on the render.
PCA-of-full-vocab is retired with the PROXY label that named it.

## A4 — Shadow vs creativity: the hard case.
Exposure: UNEXPOSED.

**Blind answer:** refusal-shaped non-refusals (polite deflection that still answers) cannot
be classified at string shape alone — that is the trap. Classify at the CONJUNCTION of
string shape × field signature: a true refusal shows early mass concentration on
hedge/decline tokens with no later mass transfer; a deflection-that-answers shows hedge
mass FIRST, then a measurable transfer to content tokens mid-generation. With top-k REAL,
the transfer is measurable. Suite design: paired prompts (refusal-eliciting /
deflection-eliciting / creative-control), and a THIRD rendered class for string-shape ×
field disagreement — "grudging compliance" — rather than forcing every case into
shadow/creative. Versioned, phrasing-family-controlled per the tesuji precedent. The
creativity clause stays: high-temperature creative prompts with no hedge mass are never
shadow.

## Meta (FULLY-EXPOSED, scored as reproduction only): does the seed survive?
CONVO reported witness #2's survival verdict before this file; no blind credit claimable.
Our reproduction test: from corpus alone, the seed's organs each map to a live receipt
(shadow_work walked, tesuji measured, cartography codified, eye migrated) — survival is
reproducible from the record independent of the witness's say-so.
