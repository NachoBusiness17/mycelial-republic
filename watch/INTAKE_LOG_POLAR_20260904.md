# INTAKE — LOG-POLAR COORDINATES CARD (2026-09-04 window) — the operator cells become ruled paper

Genome: docs/ref/verb_genomes/research_socratic.md (six steps) on L0 v1. Seat: zcode, intake lane.

## ITEM
https://en.wikipedia.org/wiki/Log-polar_coordinates — operator-pasted into the
steering-map line (verbatim framing: "ρ mapped logarithmically, θ kept: rotation and
scaling become pure translation; the retina's foveal sampling geometry; the classic
rotation/scale-invariant matching transform"). Sharp questions: (1) vortex → straight
lines: cleaner receipt for the arena's curl cell? (2) log-polar sibling for the Smith
build's stage-1 standing-wave strip? (3) foveal sampling × static-render law?

## 1. INGEST — receipts (primary source)
- WebFetch extraction (first attempt ETIMEDOUT, retry succeeded): Supported.
- Exact transforms, verbatim: **ρ = ln(√(x²+y²)), θ = atan2(y,x)**; inverse
  **x = e^ρ cos θ, y = e^ρ sin θ**; radial rule r = e^ρ; forward map written
  **x + iy = e^(ρ+iθ)** — i.e. log-polar coordinates ARE the complex logarithm.
- Page properties (what it actually claims): Laplace's equation keeps its Cartesian
  form (∂²u/∂ρ² + ∂²u/∂θ² = 0), Cauchy–Riemann simplify, Euler's ODE becomes
  constant-coefficient; "log-polar is the natural choice" for rotationally symmetric
  domains. **The page does NOT state "rotation and scaling become pure translation"** —
  its closest text is "computational advantages when rotating or zooming in an image."
- Applications listed: image analysis/registration (Weiman & Chaikin 1979 spiral
  sampling), rotation/zooming advantages, **retina modeling** ("big similarities with
  the spiral coordinate system" — photoreceptor density), fractals (Mandelbrot spiral
  structure), fast Radon transform (Andersson 2005), disk-grid numerical PDEs.

## 2. MAP — corpus sweep
- Grep across watch/ + docs/ + memory/ + dashboard/ + state/: **zero hits** for
  log-polar / logpolar / fovea — corpus-absent as an item. MEMORY.md read to
  completion this time (266/266 lines — closes the partial-read crop both prior
  cards filed).
- CONVERGENCE, two lanes one organ (the good kind): (a) the **kaliset** card's
  `p = abs(p)/dot(p,p)` is circle inversion r → 1/r, which in log-polar is the
  coordinate MIRROR ρ → −ρ (plus the abs() θ-fold) — the operator's "algebraic
  cousin" line is literal: inversion is a reflection in the complex-log plane, and
  1/z̄ is an anti-Möbius map, same family as the Smith chart's Γ transform;
  (b) the **Smith chart** is drawn in the Γ-plane whose polar angle IS the chart's
  "wavelengths toward generator" rim — log-polar of Γ-space is the chart's own
  coordinate system with the radius made linear.
- Three same-night external arrivals (Smith → kaliset → log-polar) all live in one
  plane: the complex logarithm. That is a signal, not a coincidence.

## 3. ASSERT (steel-man)
Mapping the arena's invariant space to (θ, ln r) rectifies the operator cells' flows —
curl to one straight-line family, radial divergence to the perpendicular family, any
curl+div composite to a straight line whose slope IS the div:curl ratio — turning flow
geometry into ruled paper the receipt can measure as two numbers (residual, slope).

## 4. ATTACK (strongest counter-case)
1. **"A coordinate change adds nothing — the Cartesian trajectory already shows the
   spiral."** Counter, measured: a spiral shape needs eyes; rectification turns it
   into NUMBERS — max line residual (an invariant that holds at machine epsilon) and
   slope (a measurement of div:curl). That is exactly what a receipt is. But the
   attack has teeth: without a control, EVERYTHING green-lights and the receipt is
   costume — hence pre-registered K3 (below), which the control fails on cue
   (shear stays curved, resid 0.357). The receipt is discriminating because it was
   designed to be able to fail.
2. **"It re-derives the divergence receipt we already have."** Counter: the existing
   receipt asserts GPU-vs-CPU fidelity of FIELD EVALUATION; rectification asserts a
   property of FLOW GEOMETRY (integrated trajectory structure) — a different
   assertion class riding the same receipt grammar. Complementary, not duplicate.
3. **"The page says what the operator says."** Disputed as verbatim: the page claims
   PDE-form preservation and rotation/zooming advantages; the translation property is
   standard complex-log math (z → log z sends rotation to +iα, scaling to +ln s) and
   our falsifier confirms the flow version (dθ/dt = ω, dρ/dt = λ — uniform
   translation in log-polar space), but the framing is stronger than the page's text.
   Trust the math, cite the gap.
4. **Failure causes if the claim died**: (a) θ-unwrapping or integrator drift faking
   straightness — measured drift 0.00e+00, resid 4e-13, RK4 dt=1e-3; (b) trivially
   green receipt — killed by control (0.357 > 1e-2 threshold).

## 5. MEASURE — the $0 falsifier, RUN (twice — first run caught a harness bug)
memory/runs/intake_log_polar_20260904/rectify_falsifier.py + falsifier_output.txt.
Arena-morphic fields, RK4, dt=1e-3, T=2, 16 seeds, mapped to (θ, ρ=ln r), per-
trajectory line fit. Pre-registered kill conditions K1–K5, all PASS:
- **K1** spiral (ω=1, λ=0.4) rectifies: max resid **2.04e-14** (< 1e-6) — STRAIGHT.
- **K2** measured slope = div:curl ratio: err **3.08e-14** (< 1e-4) vs λ/ω = 0.4.
- **K3** control (shear) does NOT rectify: resid **3.57e-01** — receipt discriminates.
- **K4** pure curl = horizontal line (ρ const): slope err **4.02e-13**.
- **K5** pure source = vertical line (θ const): drift **4.44e-16**.
- **First-run finding, kept as wiring spec**: the pure source field's trajectories are
  θ-constant lines, which DEGENERATE a least-squares fit parameterized in θ
  (ZeroDivisionError, run 1). The two families are perpendicular, so a wired receipt
  must parameterize per-family (fit ρ(θ) for curl-ish, θ(ρ) for div-ish) or fit
  total-least-squares. The falsifier caught what the implementation would have.
- HONEST THRESHOLD NOTE: falsifier is float64; the arena's GLSL receipt runs float32 —
  the wired threshold must be calibrated against the existing divergence-receipt's
  observed GPU epsilon, not copied from these numbers. (Unmeasured — see CROP.)

## 6. CORRECT — tri-state, verdict, the crop

### SCORE — F:4 P:3 C:5 W:3 N:3 = 18/25 → **BUILD WINDOWED**
- **FIT 4** — wireable transform: yes, now MEASURED ($0, <1s, zero deps). Owed
  consumer: the arena's curl/source cells and divergence-receipt grammar are live
  TODAY (dashboard/static/arena_operator_field.html v0, PASS < 0.02 readout) — the
  rectification receipt is a sibling readout on the same trajectory path. Held below
  5 only by queue competition: field_smith.json v0 committed-unlanded, B1 browser
  falsifier owed, reboost stage-1 strip owed — the arena door is gated, and this
  rides behind those.
- **PULL 3** — advances the live shadow-fields/arena/smith arc (the operator's
  steering-map line, which is exactly where he pasted it); touches no campaign spine.
- **COST 5** — falsifier $0 and RAN; the receipt delta is ~20 lines on existing
  trajectory sampling; the log-Smith strip is one canvas on an existing 256-line
  static page; zero operator minutes.
- **WINDOW 3** — no decay pressure beyond surface staleness; the natural slot is the
  NEXT arena-cells build beat (same slot the reboost strip and hamilton_cell hold).
- **NOVELTY 3** — corpus-absent as an item (zero hits); the transform family is
  textbook-classic (1979 retina-sampling lineage, classic CV registration), so no new
  law — but the specific composition (rectification receipt reading div:curl from
  slope, inside the Philbrick op-amp cell grammar) is ours, and the complex-log
  three-arrival convergence is a new shelf observation.

### TRI-STATE
- Page content (transforms, PDE properties, applications, retina/Radon lineage):
  **Supported** (WebFetch extraction; one ETIMEDOUT retry).
- "Rotation and scaling become pure translation": **Supported** as math (complex log;
  flow version measured, K1/K2/K4/K5) — **Disputed as a verbatim page claim** (page
  states PDE preservation + rotation/zooming advantages only). The item's framing is
  stronger than its source; filed so the next seat doesn't cite the page for it.
- "A vortex field becomes straight lines in log-polar": **Supported, measured**
  (streamline families → parallel lines; flow → uniform translation dθ/dt=ω, dρ/dt=λ;
  pure curl horizontal, pure source vertical, composite slope = div:curl).
- Control discriminates (receipt can fail): **Supported** (K3, resid 0.357).
- Foveal/retina connection: **Supported** (page: photoreceptor distribution "big
  similarities with the spiral coordinate system"; Weiman & Chaikin 1979).
- Wireability onto the arena (receipt ~20 lines; strip as smith sibling): **Unproven
  until built** — falsifier ran, no cell/receipt landed.
- Corpus absence: **Supported** (grep, five roots).

### VERDICT — **BUILD** (18/25, BUILD WINDOWED band)
Two concrete deltas, both windowed behind the arena queue:
1. **Rectification receipt** in arena_operator_field.html: map marble trajectories to
   (θ, ln r), display max-line-residual + slope (slope readout = live div:curl), PASS
   threshold calibrated to the GPU's float32 epsilon. Mirrors the divergence-receipt
   pattern exactly — the arena's full-chord law gains a flow-geometry leg.
2. **Log-Smith strip** as the smith_chart.html standing-wave delta's sibling, not a
   replacement: constant-|Γ| rings (constant VSWR) → horizontal lines; the
   "wavelengths toward generator" rim → literal horizontal scroll (Γ(d) = Γ_L·e^(−2γd):
   lossless is pure phase translation, lossy adds ln-attenuation translation — the
   page's rotation/scale→translation in transmission-line dress). Derivation only;
   rides the same beat as the owed stage-1 strip.
REMEMBER rider (question 3): **foveal sampling skin** — uniform sampling in (ρ,θ) is
foveated sampling in (x,y); composes conceptually with the static-render law and the
decimation-calibrator doctrine (high-res center = the operator's eye, compressed
periphery keeps the silhouette), but a one-pass WebGL1 shader does not get foveation
free (render-target or vertex-density work). Parked as someday-docket, not owed.

### ROUTE
1. Card to watch/; typed room row appended (driver pulls on cadence).
2. BUILD deltas enter the arena queue BEHIND field_smith.json v0 + B1 browser
   falsifier + reboost stage-1 standing-wave strip, in that order — same slot as
   hamilton_cell, ahead of nothing.
3. Calibration row for the intake lane: twelfth math-viz card; the genre wall holds
   again with its cleanest split yet — transform conjunct measured at machine
   epsilon, consumer conjunct satisfied by EXISTING cells rather than a new family.
   Also: falsifier-bug-as-wiring-spec (vertical-line degeneracy) is a keep — run the
   falsifier before the build, it finds the parameterization the implementation needs.
4. Complex-log convergence note for the operator: Smith chart, kaliset inversion,
   log-polar — three arrivals in 48 hours, one plane. The steering-map line is
   assembling itself; log-polar is the coordinate system all three share.

## DOGFOOD
(1) INVARIANT PASS — map-presents-the-solved-problem: log-polar presents the SOLVED
problem of rotation/scale invariance (registration/retina lineage) — honestly NOT our
problem pre-solved, unlike the Smith chart; it becomes ours only through the
rectification composition, which is why the verdict is windowed BUILD and not NOW.
Det-spine + stoch-flesh: a pure deterministic coordinate spine (zero stochastic
content); the marble's momentum is the flesh, and the receipt asserts the spine's
invariant (straightness) survives the flesh. Composable-operator-cells: the curl and
div cells become two PERPENDICULAR line families — the op-amp sheet's flows rendered
as graph paper; composition is literal (same FIELD.json cells, one new receipt).
(2) STOCKFISH PASS — opcodes: **arena curl/source cells** (primary; rectification
receipt), **smith_chart.html** (secondary; log-Smith strip beside the owed stage-1),
someday-docket **foveal skin**; NOT swarm-nav (no occluder set), NOT the campaign spine.

**[SOCRATIC] block** — assumption attacked: "a coordinate change adds nothing the
trajectory doesn't already show" (broke: rectification converts shape→numbers, and the
control proves the numbers can fail). Instrument: $0 RK4 falsifier with pre-registered
kill conditions, run twice (first run caught the θ-parameterization degeneracy). What
survives: the rectification receipt as a measured, discriminating invariant; the page's
text does NOT survive as the source of the translation claim (math does).

**Two counters** — FORBIDS: wiring the rectification receipt or log-Smith strip ahead
of field_smith.json v0, the B1 browser falsifier, and the reboost stage-1 strip (queue
law — a receipt skin never jumps a committed delta; same forbid as the last three
cards, now covering a candidate with a measured $0 falsifier that will want to jump).
PAID RENT: five kill conditions measured for the price of one <1s script; the first
run's ZeroDivisionError became the receipt's parameterization spec; K3's control
run proves the receipt discriminates — one number (0.357) bought the difference
between an invariant and a costume.

## RECEIPTS
watch/INTAKE_LOG_POLAR_20260904.md (this card) ·
memory/runs/intake_log_polar_20260904/{rectify_falsifier.py, falsifier_output.txt}.
Room row: {"ts":"2026-09-04","seat":"zcode","verb":"research-intake","item":"wikipedia log-polar coordinates","verdict":"BUILD 18/25 windowed","receipt":"watch/INTAKE_LOG_POLAR_20260904.md"}

## THE CROP
My pass never saw: (1) the arena's float32 GPU epsilon unmeasured — the wired receipt
threshold is a placeholder until calibrated against the existing divergence-receipt's
observed behavior; (2) smith_chart.html re-read only via the reboost card's grep
(lines 30/53 prose-only claim inherited, not re-verified); (3) the discrete log-polar
literature (Weiman–Chaikin spiral sampling, Andersson Radon 2005) unfetched — page
summary only, so the foveal skin's sampling pattern has no primary receipt; (4) the
log-Smith strip's lossy-line case (α > 0) derived, not simulated; (5) the lossless
DERIVATION of translation is mine, not the page's — a math chair should eyeball
Γ(d) = Γ_L·e^(−2γd) → (θ−2βd, ρ−2αd) before it renders. Next chair: whoever takes the
next arena-cells beat wires the receipt in the SAME pass as field_smith v0 + B1
falsifier + stage-1 strip and calibrates its threshold against real GPU deltas; a
vision chair could judge the perpendicular-families overlay render when it exists.
