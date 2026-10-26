# AE2 — NCP-ArchPreview vs the estate's LDT: same thesis, two scales (2026-09-30)

Seat: Explore (read-only), banked by orchestrator. Files read: tools/ldt_train.py, tools/ldt_lattice.py, tools/legality_propagator.py, V7_LDT_LATTICE.md. NCP claims run off the mission brief (paper fetch is AE1's lane).

## 1. Mapping

Their concept codebook = our 5 legality labels as lattice atoms; their discrete-latent next-concept prediction = our cascade descent (`cascade_chain`, ldt_lattice.py:112) shrinking TOP to a feasible set; their concept-space inference = our strict projection (`project`, ldt_lattice.py:161) masking softmax mass to feasible atoms, BOTTOM=abstain. Their "predict the next concept, not the next token" = our "classify the verdict, not the render."

## 2. What 1.95x predicts

Concept-space learning compounds: their 51.3%-budget parity implies prediction over short discrete codes converges faster per sample. LDT analog: v0 must reach its soundness ceiling with fewer rows / smaller model. Testable — train v0 on subsampled splits.

## 3. Divergence

They learn the codebook end-to-end (VQ-style, soundness unguaranteed); we project post-hoc onto a hand-built exact lattice — 0.883->0.986 soundness by construction (shrink-only law, 195 kills, 0 correct lost). Ours is sound; theirs is portable.

## 4. The steal

v1 = learned concept layer (set-valued predictions over all 32 lattice elements, renorm mode) trained UNDER the exact mask: learned compression for coverage (renorm already Pareto-dominates raw: 0.9806 soundness, 0.9805 coverage), exact verification for soundness. Their 1.95x says this layer should be cheap.

## 5. Falsifier

End-to-end v1 with lattice-conditioned training failing to beat renorm's 0.9806/0.9805 — or residual errors escaping F (truth-outside-feasible > 0) — breaks the mapping.
