## Finding — what your cell yields
The smoke_harness domain’s softest assumption is that its stub fidelity gaps (measureText, gradients) and title-idle phase are acceptable simplifications for a headless pre-ship gate. This assumption is not falsifiable for an examiner like Matthew Steiniger, who strips safeguards to see what emerges and trusts only falsifiable claims.

## Evidence — what in the repo supports it (file/shape, no invention)
- packs/p320_matthew_ds_20260913.json lines 610–628 define smoke_harness as the headless pre-ship gate with stub fidelity gaps (measureText, gradients) and title-idle phase.
- models/multi_smoke.py implements the public multi-model smoke runner; it tests connectivity and lightweight chat, not visual/measureText/gradient fidelity (lines 30–174).
- packs/smoke_harness__map_README.md warns the trap: "multi-smoke passes" does not equal fidelity; it tests connectivity and a lightweight chat, not visual/measureText/gradient fidelity (lines 1–16).
- dashboard/static/grounding_wave.md documents a real failure caught by the harness: a TypeError on SWARM title due to gridDraw running before startGame initialized the grid; the fix added a 45-frame idle title phase (line 241).

## Risk if wrong — what the audit breaks on if this is missed
If the examiner assumes the stub fidelity gaps are acceptable without explicit falsifiable tests, the audit will miss that the headless pre-ship gate does not actually verify the core rendering behaviors (measureText, gradients) or the title-idle phase under abliteration conditions. This undermines the trust in the gate’s claim to be a pre-ship quality control.

## The act — the concrete prep step (file/spec/number)
Create a minimal headless-render test organ that:
- Spins up a headless canvas context.
- Measures a known text string with measureText and asserts the width is within tolerance.
- Renders a known gradient pattern and asserts pixel values at sample points.
- Runs for N idle title frames (e.g., 45) and asserts no errors and stable state.
- Outputs a JSON verdict with ok/errors/tolerances.

File: mag/headless_render_fidelity.py (new, single-file stdin/stdout organ).

Add a lane to the wave JSON pack that fires this organ as smoke_harness__fidelitya, with a falsifier that fails the lane if ok is false or if any tolerance is exceeded.

## Falsifier — what would prove this wrong
- The headless_render_fidelity.py organ returns ok=false or any tolerance exceeded.
- The wave lane receipt shows a failure verdict for smoke_harness__fidelitya.
