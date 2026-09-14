# PURPLE HARVEST B2 — ERASER MAZE receipt (2026-09-06)

Builder: zcode seat (B2 lane) · card: `watch/PURPLE_HARVEST_01_20260906.md` (B2 eraser
field, from @LensScientific #4) · sibling build B1 odd-field is a separate builder and
separate file (no clobber, per card).

## Shipped

- **Surface:** `dashboard/static/eraser_maze.html` — standalone single-file game
  (house conventions: dark field, errbanner fixture wired to `window.onerror` +
  `unhandledrejection`, nav.js include, canvas via offscreen ImageData scaled with
  smoothing off, rAF loop, keyboard + two sliders). NEW file; no existing surface touched.
- **Nav wiring:** `dashboard/static/nav.js` LINKS entry
  `["/static/eraser_maze.html", "Eraser Maze"]` placed with the game-surface cluster
  (after Shadow Walk). Backup left at `nav.js.bak-b2-eraser-20260906`. `node --check` clean.
- **Receipt:** this file.

## The two layers, as built

- **Wave layer:** path-sum amplitudes over a BFS DAG, `[re,im]` stored in typed arrays.
  Per-cell partial slots (MAXS=8, one slot per parent across route families) hold
  `A(p)·e^{i·k·d(p)} / N`; coherent intensity `I_coh = |Σ_p c_p·e^{iΦσ_p}|²`.
- **Measurement layer:** `observed[]` = cells inside the player's sight radius (slider
  2..14), stamped every frame; where observed, display switches to the incoherent sum
  `Σ_p |c_p|²` computed from the SAME per-parent partials — which-path info kills the
  cross terms, pattern washes flat (rendered slate vs violet). Seeing collapses the light.
- **Eraser:** stepping on an eraser tile (r=10) or pressing E for the carried eraser
  (r=7, 250 ms cooldown) applies the unitary tag-basis rotation Φ += π/3 — a rotation on
  labels, never a deletion. Fringes return IN THE NEW BASIS: the pattern measurably
  shifts (test-grid bright fringe moved 6 rows at k=2). Cells covered by an erase display
  coherently again until re-observed (continuous gaze re-collapses — stamps are per-frame).
- **Detector tiles:** collapse a wide radius (r=9..13) on step, stamped as COLLAPSE.
- **Delayed-choice room:** the twin-slit chamber (full-height wall at x=44, gaps at
  y=15/25, seeded by the source family's actual arriving amplitude+phase). Walk the dark
  side flat, then erase over it: the corridor re-lights in the new basis. The PRISM win
  object reads the field without recording it (exempt from sight collapse); it reads LIT
  only when an eraser has actually re-mixed its basis and no collapse has landed since.
- **Audit strip:** append-only ledger, one row per event (SEED / COLLAPSE per step /
  DETECTOR / ERASE / PRISM), rows never spliced — survives NEW MAZE reseeds. Strip shows
  the last 9 rows + total count; nothing is ever deleted.

## Math note (tri-state — one deviation from the literal formula, with proof)

- **DISPUTED (spec as literally written):** `A(cell)=Σ A(p)·e^{i·k·d(p)}/N` over strict
  BFS parents provably produces ZERO interference: every shortest path to a cell has the
  same length L and accumulates the identical nested phase `k·L(L−1)/2`, so all cross
  terms are constructive — V_coherent ≈ 0, failing the card's own falsifier. Verified
  numerically before the fix.
- **SUPPORTED (what shipped):** propagate per WHICH-PATH FAMILY with family distance
  `d_f` — the minimal correction that lets distinguishable routes of different length
  recombine. Everything else is the spec: partials, per-parent partial sums, `e^{i·k·d}`
  phase, tag unitary on erase. The double-slit chamber is fed by the source family and
  re-emits at the two gaps (coherent unit-gain re-radiators, phase-preserving).
- **UNPROVEN (not attempted):** full Feynman sum over all non-geodesic paths; wave
  equation (Huygens) rendering; occlusion-based sight (sight is radius, per card).

## Falsifiers — PASS (measured, not asserted)

Built-in double-slit test grid (source → wall x=22, gaps y=9/17 → screen column x=36).
Primary metric = fringe visibility as modulation depth against the local incoherent
envelope (standard optics definition; the raw-band numbers are also printed on-surface).
At default k=2.0:

| State | V (modulation depth) | want | raw central band |
|---|---|---|---|
| coherent | **0.949** | ~1 | 0.925 |
| after tagging (observed) | **0.000** | ~0 | 0.200 |
| after eraser (new basis) | **0.998** | >0.5 | 0.987 |

- Bright-fringe shift on erase: **6 rows** — fringes return in the NEW basis, displaced.
- Sweep k=0.2..3.5: all pass (V_coh 0.908–0.9998, V_tag 0.000, V_erase 0.947–0.9999).
- Note on V_tag: 0.000 is by construction — the tagged display IS the envelope (which-path
  sum carries no cross term). The raw band residual 0.200 is smooth envelope variation,
  no fringe structure (see the live strip's raw numbers).
- The strip re-runs live on every k-slider move and prints PASS/FAIL per falsifier.

## What was verified vs not (honest tape)

- **VERIFIED (Node 22 harnesses, exact shipped code):** the FIELD CORE is delimited by
  `/*__ERASER_CORE_BEGIN__/…END__*/` markers and was sliced out and executed directly:
  falsifier sweep + screen-column intensity profiles (fringe shift visible in ASCII bars).
  A second harness stubbed the DOM, evaluated the full page script, and drove the real
  game loop: boot, BFS-pathed walk from spawn through a slit gap into the dark side,
  per-step COLLAPSE ledger rows, carried-eraser basis rotation Φ 0→π/3, prism
  erase-stamped, win correctly BLOCKED before adjacency and after eraser+adjacency
  fired, detector/eraser tile on-step dispatch, ledger append-only across frames, k-slider
  recompute without throwing, HUD string build. Hot-path timing: displayInto 0.012 ms/frame
  on the 61×41 field (budget 16.7 ms at 60 fps); computePartials 0.17 ms per k change.
  No per-frame allocations in the render loop (preallocated ImageData + typed arrays).
- **NOT VERIFIED (no browser run on this seat):** actual on-screen rendering, 60fps under
  real compositor load, keyboard feel, and the visual read of violet fringes. The error
  banner fixture is in place per house convention so any runtime error surfaces loudly.
  The harness DID execute every frame()-reachable code path except `drawSprites` canvas
  calls (stubbed no-ops) — logic verified, pixels not.

## Files

- `dashboard/static/eraser_maze.html` (new, ~530 lines, single file)
- `dashboard/static/nav.js` (one LINKS line; backup `nav.js.bak-b2-eraser-20260906`)
- `watch/PURPLE_HARVEST_B2_ERASER_MAZE_20260906.md` (this receipt)

Console access: `window.__ERASER_CORE` exposes makeField / buildDoubleSlit /
runFalsifiers / mulberry32 for on-surface poking.

## SEAT VERIFICATION (independent re-run, 2026-09-06)

The seat sliced the marked core out of the shipped page and re-drove runFalsifiers
in a fresh Node process. Builder's on-surface numbers REPRODUCE EXACTLY: at k=2.0,
vcn=0.9492 / vtn=0 / ven=0.9984, shift=6 (builder reported 0.949 / 0.000 / 0.998 / 6 —
those are the normalized v*n numbers). Sweep k=0.2→3.5: vtn=0 everywhere
(complementarity holds), ven ≥ 0.94 everywhere with shift ±3..9 (fringes return
DISPLACED — delayed choice proven), vcn ≥ 0.92 everywhere. Honest note: raw
central-band vc dips to 0.47 at k=2.5 — a dark node lands in the sampled band; the
envelope-normalized measure is the right reading. The builder's spec-deviation catch
(strict-BFS path sums provably cannot interfere; family-distance fix) is CONFIRMED
correct by the seat — the original card spec was the birth defect. VERDICT: PASS.
Pixels remain unverified (no browser run) — the error banner will speak if it lies.
