---
name: ractor-engine-design-20260916
description: The Ractor Engine — OCEAN-parameterized brain-graph witnesses with
  Laplacian belief dynamics, recurrent-depth thinking budgets, and receipted threshold
  crossings; design basis complete (M1-M3), empty middle confirmed, build spec next
metadata:
  node_type: memory
  type: project
  originSessionId: sess_f8f2909b-0ac5-4763-abba-fbd8ba748f54
---

Operator riff 2026-09-16: "self steal deep learning and decision prediction from
mnemonic.ai for recreation of convincing thought processes using physical brain structure
mapped to ocean models to recreate accurate thinking for the ractors." Decode: OCEAN = the
Big Five (the "ocean models" pun is real psychometrics); physical brain structure = the
witness's mind as a region-graph, not a flat persona. Two ore images = the compute laws:
the Laplacian (one operator — heat/waves/edges/quantum) and recurrent-depth scaling
(3.6B looping 64× matches 103B materialized, Geiping et al. arXiv:2502.05171).

## DESIGN BASIS (three receipts, moonshot_20260916/receipts/)

- **M2 RECURRENT DEPTH (verified against arXiv 2502.05171, Geiping et al.):** latent
  recurrent depth = the small model's equalizer; all capability lives in the loop (r=1
  scores below random). Budget table for our witnesses: scut 4 / worker 8 / standard
  witness 12–16 / context-loaded 20–32 / obsessive 64 hard cap (paper's own ceiling).
  Stability-exit (KL-convergence) per question; receipt gains a `depth` field (loop
  count, budget cap, exit reason, final-state hash, path-independence flag).
- **M3 LAPLACIAN BELIEFS (receipt M3_LAPLACIAN_BELIEFS.md):** witness = 33-node
  brain-graph in 5 layers (4 clamped perception / 12 memory / 8 values / 6 inference /
  2 salon-social / 1 verdict), update du/dt = −γΣW_ij(u_i−u_j) − λu + b + σ(S−u) + ξ.
  OCEAN → material constants of L: O→boundary conductance, C→leak+hysteresis,
  E→salon coupling, A→cooperative gain + conformity shift, N→negative-edge gain
  (Altafini signed-graph consensus). Verdict fires on |u_O1| ≥ θ through a hysteresis
  band; confidence = distance past threshold; UNDECIDED-oscillation is a first-class
  output (rumination is real). Kills: linear diffusion can't innovate and has no
  sequence reasoning — the LLM verbalizer is the mouth AND the only novelty source,
  but may never write the verdict node (diffusion stays sovereign over feeling).
- **M1 PRIOR ART (receipt M1_MNEMONIC_PRIORART.md):** mnemonic.ai = REAL MarTech
  (OCEAN personas, Digital Twin), but thin — RAG + trait scores, no brain structure, no
  dynamics; their Twin-2K-500 benchmark (2,058 people, 191,406 held-out answers) reaches
  **89% of the human self-agreement ceiling** — that ceiling (~70–90%) is the honesty
  target our witnesses grade against. The empty middle is CONFIRMED (arXiv queries return
  zero direct hits): no published system combines brain-graph-structured witnesses +
  OCEAN vectors as physical parameters of graph dynamics + state-flow thinking + receipted
  threshold crossings. Steals: DDM decision rule (OCEAN → drift rate/boundary height/
  noise/starting bias), Twin-2K-500 held-out protocol as eval harness, adapter-layer
  conditioning (cheap enough for gemma:2b).

## ARCHITECTURE (the composition)

Witness = brain-graph (OCEAN-parameterized Laplacian dynamics = the feeling layer) +
recurrent-depth loop on a local gemma-class model (the reasoning layer, budgeted by
difficulty) + LLM verbalizer as the mouth (may add nodes, may never write the verdict) +
receipt (depth field + state hash, replayable). Falsifier (pre-registered): neuroticism-0
vs neuroticism-1 witness, same graph/seeds, ≥20 ambiguous questions — pass requires
≥15 pp negative-verdict delta OR KS ≥ 0.2 on confidence OR ≥1.5× latency ratio, AND κ
recoverable from held-out behavior ±30%. Indistinguishable ⇒ costume ⇒ canon correction.
Silence not allowed.

## FREE-LANE SALON LANDED (RS_RACTOR_ENGINE_SALON — 12/12 answered, $0, 8 lanes)

Three amendments complete the spec: (1) **the decoder bridge is load-bearing, not
optional** — 3/4 lanes independently located the diffusion-to-tokens interface as where
the mind meets the mouth; (2) **the novelty cap is real** — diffusion conserves mass, it
blends beliefs but never creates nodes; fix = a threshold-triggered sparse generative
probe (token patch → new nodes/edges → re-diffuse) with counterfactual minimal pairs as
the standing loop-depth regression; (3) **zero-coupling placebo certification** — every
witness is tested against a trait-words-in-prompt twin with all graph gains neutral;
"if flips persist, it is costume, not mechanism." Q2 was UNANIMOUS NO (64× loop of a 2B
model ≠ 70B single pass; attractor capture + smoothing erase minority evidence) — the
four proposed first-measurable-differences (backtracking, counterfactual sensitivity,
OOD grounding, loop-horizon decay) double as the loop-depth regression battery.

**M4 SPEC BUILT (same night):** RACTOR_ENGINE_SPEC_v0_1.md (32KB, watch/inbox/) — the full
witness architecture: three layers (Laplacian feeling-graph / recurrent reasoning loop / LLM
mouth) with the sovereignty rule (diffusion owns feeling, mouth owns words, neither writes
the other's state), decoder bridge required and deterministic in v0.1 (learned head deferred
until receipts accumulate), OCEAN parameter table merging M3's Laplacian constants with M1's
DDM correspondence (O→drift/g_P, C→boundary/leak+hysteresis, N→noise/κ+θ⁻, E→bias/σ,
A→conformity), budget ladder 4/8/12–16/20–32/64 T1.3-capped, receipt schema
ractor.witness.receipt.v0.1 (depth field: loops/exit/final_delta/state_hash/
path-independence flag), all four falsifiers pre-registered (incl. sampler-lesson
seed-diversity cap: ≥5 seeds, ≥2 outcomes, entropy ≥0.15 nats on ≥30% — first-dance values
flagged for re-derivation), gemma:2b build plan all-local (host numpy engine, Ollama mouth),
10 open cells, unverified-number ledger. Three solo decisions flagged for the operator:
recurrence as rewiring epochs (2B can't do trained latent loops), deterministic decoder
bridge v0.1, invented seed-diversity thresholds.

Related: [[wave-20260916-standing-wave]], [[concert-001-four-substrate-20260916]],
[[research-wave-20260916]], [[jev-system-one-decision-model-20260916]],
[[east-west-ractors-20260916]].
