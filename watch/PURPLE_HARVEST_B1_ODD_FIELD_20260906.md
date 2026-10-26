# PURPLE HARVEST B1 — ODD FIELD lands on maze_arena (2026-09-06)

**Build:** B1 of PURPLE_HARVEST_01 (light-maze odd-field propagation). Builder: zcode seat.
**Card math:** `watch/PURPLE_HARVEST_01_20260906.md` §B1 — `T += η·s·(T(rot90(n_best)) − T(rot-90(n_best)))/4`,
η∈[−1,1] slider, s=±1 toggle. **B2/eraser_maze.html untouched** (other builder's file).

## What changed (file:line)

All in `dashboard/static/maze_arena.html` (backup-first: `maze_arena.html.bak-b1-20260906`):

- **L41-103 — the flood is now `buildField()`**, two phases:
  - **Phase A (L56-66): classic BFS flood**, flat-index inner loop, FIFO head cursor
    (same visit order as the old `q.shift()` queue, no per-pop array allocs). At η=0 the
    function STOPS HERE — the η=0 field is produced by an unmodified classic relaxation.
  - **Phase B (L68-99, only when η≠0): the odd field** — a label-correcting solve of the
    handed relaxation over the lit cells (`open` mask derived from phase A, L69-70):
    `t = LM[n]+1 + η·s·clamp(LM[pa]−LM[pb], ±2)·0.25`, where (pa,pb) are the rot90/rot-90
    perpendicular neighbors of candidate step-neighbor `n`, **signs tracked per step
    direction** — E:(n+GW,n−GW) W:(n−GW,n+GW) S:(n−1,n+1) N:(n+1,n−1) (L87-90) — so the
    curl has one consistent chirality. Every decrease re-queues only the 4 neighbors
    (the only cells that read the decreased cell as base or perpendicular, L91-97).
    Guards: both perpendiculars must be lit (`open`), diff clamped ±2 ⇒ perturbation
    ≤ |η|/2 per step; 1e9 sentinels never enter the term; safety pop-cap 8·N sets
    `bCapHit=1` (trip = quiescence not reached; never trips at any tested η, L82).
- **L20 — UI:** `HAND +1` toggle button + `ODD η` range slider (−1..1, step .05) with a
  gold live readout, in the existing button row.
- **L23 — hint line** extended with the odd-field explanation (player-facing).
- **L313-326 — wiring:** hand toggle flips `handOdd`, slider sets `etaOdd`; both call
  `scheduleFieldRebuild()` — rAF-coalesced to at most one flood+redraw per frame
  (potato-proof; flood is init/slider-only, the 60fps render loop is untouched).

Not changed: agents, renderer, GPU shadow-field pass, nav. `nav.js` already carries
`["/static/maze_arena.html", "Maze Arena"]` at line 55 — surface already wired; **no nav
edit needed, none made** (grep-verified against tesuji_map/shadow_walk treatment).

## Falsifier numbers (harness: `watch/PURPLE_HARVEST_B1_ODD_FIELD_harness_20260906.mjs`)

The harness does NOT retype the math — it extracts the geometry+flood section from the
shipped HTML **and from the pre-change backup** and evals both in a sandbox. Node v22.

**(a) η=0 reproduces the old field — PASS, bit-for-bit.**
32,400 cells, 21,429 lit, max finite 354. Mismatches vs pre-change kernel: **0**
(baseline self-mismatches: 0). Stricter than the "float epsilon" bar: exact equality.

**(b) η≠0 shifts L/R route times with sign(s) — PASS on response; chirality PASS via
mirror maze; honest caveat below.** At η=0.6:
- Swirl moves **20,835 / 20,757** of 21,429 lit cells (s=+1 / s=−1), max|dT| 49.7 / 17.4.
- GPS-walk fleet (108 spawn-class starts, shipped walk logic): mean steps **5133 (η=0) →
  4400 (s=+1) / 5855 (s=−1)**; completed **81 → 85 / 77**; left-vs-right mean-steps split
  swings **807 steps** between s=+1 (−2878) and s=−1 (−2071). |Δ| is hundreds of times
  the run-to-run noise (fields are deterministic). eta=−1 (max slider): 20,888 cells
  moved, max|dT| 29.0.
- **Chirality proof:** the arena wall set is only *near*-mirror-symmetric, so the raw L/R
  field imbalance does NOT literally flip sign with s on the real layout (and the coarse
  mean is insensitive: ±0.1-0.6 on shift scale ~3.5). Rigorous test: reflect the wall set
  AND the cheese about world x=1 (reflection reverses handedness); then
  field(mirror, s=+1) must equal mirror(field(orig, s=−1)). Base-field mirror sanity is
  **exact (max|diff| = 0.0)**; field-aggregate chirality mismatch **6.3%** of shift scale
  (tol 10%) — PASS; walk-level mirror match 30% vs non-chiral control 114% (need < ⅓) —
  PASS with clear separation.
- **Honest caveat (DISPUTED edge, evidence attached):** the quiescent fixed point of a
  non-reciprocal relaxation is not unique — decreasing a perpendicular *raises* the
  opposite transverse flux, so the operator is non-monotone and the solve is
  **order-dependent (hysteresis)**: cell-level mirror divergence up to 17.4 remains.
  Physically apt (odd media: work cycles, path-dependence) and deterministic per
  (layout, η, s) — same slider setting always rebuilds the same field — but the field is
  NOT a unique function of geometry. Solver converges to quiescence at all tested η
  (`bCapHit=0`); cap-independence verified at η=0.6 and η=−1.

**(c) Build cost ≤ 2× old flood — PASS.** Median of 50: old 17.1-18.4 ms; new η=0
**14.6-15.4 ms (0.84-0.89×)** — the flat inner loop is *faster* than the old queue;
η=0.6 **30.1-32.0 ms (1.76-1.82×)**; η=−1 **25.8-28.2 ms (1.50-1.57×)**. p90 worst
observed 39.5 ms vs 2×p90 bar 44.8 ms. Per-frame: the field is built once at load and
rebuilt only on slider/hand input (rAF-coalesced); the render loop and the agents' LM
reads are untouched by the term.

## Verified vs not verified (the tape)

- **VERIFIED (machine, this box):** all three falsifiers above; both script blocks pass
  `node --check`; element ids and wiring symbols present (grep-checked); η=0 bit-identity
  includes the fixed BFS-flood y-transform path (source cell floor(y/2.7·GH) untouched).
- **NOT VERIFIED in a live browser:** the subagent sandbox has no browser (one attempt,
  `agent.browsers` unavailable — not retried). The DOM wiring (slider `oninput` →
  `etaOdd` → rAF-coalesced `buildField(); drawLM()`) is **code-review + syntax-check
  only**. Risk is low (plain DOM handlers, ids grep-verified, same pattern as the
  existing FIELD/NEW RUN buttons) but it is not a browser receipt. First human load
  should confirm: no red error banner, η slider visibly re-lights the maze, HAND flips
  the corridor preference.
- **Scope guard:** eraser_maze.html untouched; verkle chain untouched; no Docker.

## Notes for the next phase (moving walls, now GO'd per the card)

`buildField()` is already a callable re-flood — moving walls can call it per wall-move
tick; at η=0 it costs ~15 ms (fine for occasional rebuilds), at |η|=0.6 ~31 ms. For
per-tick cadence, hoist the wall mask or move the flood into a worker — deliberately NOT
done now (potato-proof first, no speculative machinery).

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran the shipped harness (`PURPLE_HARVEST_B1_ODD_FIELD_harness_20260906.mjs`,
kernels extracted verbatim from the shipped HTML and the pre-change backup) in a fresh
Node process: EXIT=0, every number reproduces — swirl moved 20,835 cells at η=0.6 s=+1;
walk fleet 5,133 → 4,400 (s+1) / 5,855 (s−1), L-R swing 807.4 steps with sign of s;
mirror chirality 30% vs control 114% (need <⅓); base-field mirror exact 0.0; cost
η=0 **0.86×** (faster than the old flood), 1.71× / 1.46× under swirl, bar ≤2×;
bCapHit=0 at all tested η. The hysteresis caveat is printed by the harness itself —
accepted as on-theme (odd media: work cycles, path-dependence), deterministic per
(layout, η, s), flagged not papered. Backup-first honored, nav pre-existing (verified,
no edit), scope guard clean. VERDICT: PASS. Browser pixels remain the one open eye —
first human load: watch for the red banner, η re-lighting the maze, HAND flipping the
cheaper corridor.
