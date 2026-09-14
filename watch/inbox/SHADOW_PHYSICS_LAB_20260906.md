# SHADOW PHYSICS LAB — 2026-09-06 — BUILDER "LAB" RECEIPT
**Bench:** `notebooks/shadow_work_physics.ipynb` (13 cells: 6 code) + headless mirror
`notebooks/shadow_work_physics.py` — SAME cells, percent format, runs clean end-to-end
on the real data (`python notebooks/shadow_work_physics.py`, exit 0). numpy/scipy/sklearn
only, zero matplotlib — every render is ASCII or JSON (dictionary §0: no render without
its distortion-label).

**How to open:** VS Code → open the `.ipynb` → Python 3 kernel → Run All (t-SNE cell
takes ~30 s). No jupyter installed: run the `.py` instead, same output.

## Findings (tri-state)

1. **EIKONAL — CONFIRMED.** Maze BFS flood recomputed at 480x270 (same walls/SDF/cheese
   as `maze_arena.html`). Bellman consistency T = 1 + min(4-neighbors) holds at EVERY
   lit cell, residual max = 0.000000 → the flood IS the exact discrete solve of
   |∇T| = 1 (Huygens/FMM, dictionary row 1). ASCII wavefront frames at T = 10/30/60 show
   the ring expanding and bending through doorways. GPS walker from the farthest cell
   (T = 706) reaches the cheese in exactly 706 steps, every step delta = −1, strict
   descent → Fermat least-time ray CONFIRMED (dictionary row 2).
2. **PROJECTION — DONE, lies stamped.** 9,305 points, 50 slabs, features [log chars,
   law_hits, questions, digit_ratio] standardized. PCA: pc1 45.7%, pc2 25.0%, pc3 16.6%
   → 3 comps hold 87.4% of the 4-D volume. Loadings: PC1 = questions+log_chars (+0.60/+0.60)
   = the SIZE/INTERROGATION axis; PC2 = digit_ratio (pure, +1.00); PC3 = law_hits (+0.84,
   −0.39 log_chars) = the DOCTRINE axis. t-SNE (2,000-pt sample, perp 30, seed 42) done,
   KL 0.7487, ASCII scatter printed for both.
3. **LAYER GRADIENT — CONFIRMED, with basis named.** Per-block mean RMS of exact-F32
   norm weights recomputed from the 434-tensor volume (matches `layers[].norm_rms`
   exactly). RECONCILIATION: the logged numbers (slope 0.0135, r 0.739, 4.02%/layer)
   reproduce EXACTLY on a raw-LINEAR fit + endpoint ratio (0.381 → 1.514, 3.97x). The
   log-linear COMPOUND rate is slope 0.01505/blk, r 0.705, 1.52%/layer. blk0 outlier
   CONFIRMED (−0.60 in log space, below trend); mid dip CONFIRMED at exactly blk13.
   Law: quote the basis with the number.
4. **OPTICS — DOF computed.** Thin-lens CoC c = A·|d − f|/d with A = 0.6, camera at the
   data centroid, focal plane f = 2.351 = mean distance of the trajectory-lit set
   (1184 pts with law_hits ≥ 3, top decile = attention actually spent — measured focus,
   LAW-061 clean). In focus: slabs 30, 49, 29, 48, 50 (median blur 0.44–0.47). Most
   blurred: slabs 3, 4, 13, 2, 43 (0.93–1.09). Early low-law slabs are out of focus —
   the fleet's attention lives late in the corpus.

## WHICH-LIE TABLE (every projection stamped)
| Projection | Preserves | Lies about |
|---|---|---|
| PCA 3D | global variance (87.4% in 3 axes) | neighborhoods, local clusters |
| t-SNE 2D | local neighborhoods (KL 0.749) | global shape, cluster sizes, distances |
| BFS/T field | true travel time (residual 0) | Euclidean geometry (it's manifold time, not space) |
| Log-linear layer trend | the depth axis (RISES, 3.97x) | blk0 outlier + blk13 dip (local truth) |
| DOF blur | distance from measured attention | semantic distance (PCA units are not meaning) |
| slab features | measurable behavior | meaning itself |

## Emitted
- `state/shadow_work/projection_3d.json` — 9,305 points, 778 KB:
  `[{idx, pca1, pca2, pca3, slab, law_hits}]` — ready for the 3D walker page
  (`dashboard/static/shadow_walk.html` or any three.js fetch).
- Notebook cells: 0 paths · 1 eikonal · 2 projection · 3 gradient · 4 optics · 5 emit.

**Falsifier hook:** visual read of any render from this bench must predict the printed
stats (dictionary §4, ≥70%). The distortion-labels above are the contract.
