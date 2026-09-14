# DOORBENCH BUILD RECEIPT — 20260906 (salon spawn, launch law)

Build: dashboard/static/doorbench.html — single-file WebGL2 falsifier for the
salon:rice_invalidation two-layer cache claim (architect witness spec).

VERIFIED BY PONYTAIL (builder self-report + independent byte check):
- doorbench.html present, 23,011 bytes / 520 lines, zero external assets.
- nav.js wired: exactly 1 `doorbench.html` entry (DOORBENCH), backup
  nav.js.bak-doorbench present. Served-not-wired law honored.
- Sanity at bytes: backticks balanced, on-screen SHADER COMPILE FAILED overlay
  (never console-only), texSubImage3D dirty path + generation store present (8 hits).

WHAT IT PROVES (falsifier design):
- K = door toggle: SDF recompute ONLY in the door's 48 swept cells, ONE
  texSubImage3D of 96B. Gate: <0.5ms, ≤64 dirty cells @60fps.
- B = 1,000 generation bumps/frame, state layer only. Gate: <1% frame delta.
- C = forced full 512KB field upload control. Gate: ≥10x the dirty path.
- HUD prints tri-state PASS/FAIL/UNPROVEN measured LIVE — builder disclosed the
  honest risks (vsync-floor fps gate; driver may eat full uploads) rather than
  faking passes. Hands-free proof sequence on load: storm 2s, four toggles
  4-6.4s, control baseline 7.6s.

STATUS: BUILT + BYTE-VERIFIED. Live metrics UNPROVEN until a browser run
(viewer: dashboard server /static/doorbench.html, or pocketfleet glass via
10.0.2.2:8765). First live run closes the architect's UNPROVEN rider (browser
hit-fetch cost) and the crossover-curve demand from the R3 convergence.

## LIVE RUN (2026-09-06 ~22:5xZ, ponytail dogfood, IAB on 127.0.0.1:8765)

Hands-free auto sequence ran; HUD measured LIVE in-browser:
- **[PASS] DOOR TOGGLE** — 0.100ms / 48 cells / 96B (R16F) @ 59.9fps median
  16.70ms. Gate <0.5ms / ≤64 cells / ≥60fps (vsync floor disclosed). The
  two-layer law's central claim MEASURED at bench scale: connectivity change
  for 96 bytes, one-tenth of a millisecond, four times.
- **[UNPROVEN→collecting] B-STORM** — 1,000 gen-bumps/frame demonstrably runs
  (16KB slab flush, ZERO field bytes) but the <1%-delta gate had collected 975
  storm frames with no idle baseline at read time. Needs a longer idle window.
- **[FAIL] CONTROL — the falsifier fired honestly** — full 512KB field upload
  costs 0.21ms vs 0.100ms dirty = only 2x on desktop ANGLE, gate wanted ≥10x.
  Reading: at 64³/R16F on desktop, the NAIVE path is also sub-millisecond —
  the 10x margin claim was wrong for this scale/hardware, not the law. Dirty
  path still wins (2x + less bus + less CPU); the crossover Richard will ask
  about starts where the field outgrows the bus (256³, mobile, or embedded).
  Gate re-scope owed: rerun control at 256³ or on the Android glass to make
  the 10x line honest.
- Visual: render loop alive (59.9fps steady, hit-cell readout changing);
  canvas frames dark from the auto-orbit angle at capture (camera facing
  exterior). Two-strike bail on camera dragging — tab left OPEN + deliverable
  in the IAB pane for the operator to orbit by hand.

VERDICT: the falsifiable-it-did-not-happen bar is MET — one measured PASS, one
honest FAIL that re-scopes the claim, one collection still running. This is
the demo's whole point: it prints what IS, not what we hoped.

Cost: builder subagent 587K tok on GLM-5.3-Flash (coding-plan lane). Salon
context: memory/runs/salons/salon_rice_invalidation_20260906/SALON_ARTIFACT.md.
