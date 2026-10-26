# ARENAPHYSICA CATALOG SWEEP (the reboost card's open vein, closed 2026-10-18)

Source: https://www.arenaphysica.com/publications (fetched 2026-10-18, full
catalog enumerated). The reboost card named this shop "an open vein, not an
item"; this sweep closes the reading debt at $0.

## THE CATALOG (8 publications)

1. Edge Elements: How FEM Solvers Represent Electromagnetic Fields - Oct 1
   2026 - READ (below)
2. Can the US build a DJI? - Sep 16 2026 - NOT READ (industry/policy, off-vein)
3. Simulator-Refined Diffusion for Radio-Frequency Inverse Design - Sep 30
   2026 - arXiv:2609.38363 - ABSTRACT URL TIMED OUT TWICE this pass, body
   unread (honest gap; the rf-studio read covers the inverse-design thesis)
4. Introducing Heaviside-1 - Sep 1 2026 - READ (below)
5. What is a Smith Chart? - Jul 10 2026 - CONSUMED (the founding card,
   watch/INTAKE_SMITH_CHART_20260903.md; our build: dashboard/static/
   smith_chart.html v1.3)
6. Converting Compute into Performance in a Data-Constrained World - May 6
   2026 - arXiv:2605.09189 - NOT READ this pass
7. Inverse Design of Multi-Layer Sub-Pixel-Resolution RF Passives - May 6
   2026 - arXiv:2605.08233 - NOT READ this pass
8. Introducing Atlas RF Studio - Apr 1 2026 - READ (below)

## WHAT THE THREE READS SAY

- **Heaviside-1** (350M params, 250k designs, 500B field samples): a
  foundation model that predicts full complex E and H fields in 3D from
  geometry/materials/excitations, claimed ~10^5x faster than commercial
  full-wave solvers within 1 dB. THE THESIS: supervising on dense physical
  FIELDS (not downstream scalars like S-parameters) is what generalizes -
  the field-supervised model beats the identical S-parameter-only twin out
  of distribution. Ships EMVal v1.0 benchmark (public split on Hugging Face).
- **Atlas RF Studio** (beta): Heaviside-0 (forward, S-params, 13 ms/board
  vs ~4 min solver) + Marconi-0 (inverse, diffusion-to-layout), ~3M
  simulated designs. Adding field data for 0.3 percent of designs cut
  in-distribution loss 15 percent - fields again. Frontier LLMs
  substantially outperformed on both forward and inverse tasks.
- **FEM Edge Elements**: why solvers store line integrals of E along mesh
  edges (Nedelec/Whitney basis) instead of nodal values - tangential
  continuity is the physical law, full vector continuity is false. There is
  no "collect all E values" export in an FEM solver; probes interpolate from
  edge coefficients.

## THE ESTATE READ (repetition-as-emphasis, again)

This shop independently landed on the estate's own laws while building EM
foundation models: **fields, not scalars** (supervise on the dense field and
generalization follows - the hologram close in
watch/STANDING_WAVE_DOCTRINE_20260905.md: the boundary holds the bulk; also
the Light Codec: infinite field -> discrete film), and **the probe
interpolates from the frozen coefficients** (edge DOFs = the frozen nodes;
our smith strip v1.2: nodes don't move, the wave between is re-derived).
The smith chart thread that opened this vein (an annotated 1939 chart as a
map-used-as-a-computer) ends at a company building exactly
map-presents-the-solved-problem as a product, with the falsifier
discipline we require: a public benchmark split anyone can grade them on.

Caveat carried: all performance numbers are vendor-self-reported; EMVal's
public split is the independent check.

## WHAT REMAINS

- arXiv:2609.38363, 2605.09189, 2605.08233 bodies unread (timeouts this
  pass; next window or a sensing lane).
- DJI teardown skipped as off-vein (flag if the operator wants it).
- Mesh-fit for our side: Heaviside-1's "fields as the right training
  signal" is directly our inference-budget/lane-routing question - a
  sensing note, not a build.
