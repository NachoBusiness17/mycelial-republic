# G2-5 — Percolator FP-Feedback Loop (M7's NEXT, closed)

Date: 2026-09-10 · Seat: zcode (Sancho) · Spawned from M7's NEXT row
Files: `mag/narrative_tests.py` (wired) · `watch/narrative_test_weights.json` (new, the dial)

## The problem

M7's Five Nacho Narrative Tests scored the fence parable 0/5 organic — correct. But the
false-positive risk is real: a genuine community discussion that uses emotional language
(school-safety threads, grief posts) can light up TEARS or PUNISHMENT and get called
manufactured consent. A detector that can't be corrected by a human who saw it be wrong
is a detector that trains humans to ignore it.

## The mechanism (no ML, files not processes)

A human marks a verdict wrong, then edits one JSON file. Next `run_tests()` picks it up.

1. Machine flags a batch (verdict: organic / suspected / manufactured_consent).
2. Human disagrees — FP (flagged but organic) or FN (passed but planted).
3. Human names the test that over/under-counted and moves its weight a notch
   (e.g. `tears: 1.0 -> 0.5`) in `watch/narrative_test_weights.json`.
4. Rerun the batch. Confirm the verdict moves the right way.
5. Append one row to `overrides` in the same file — the correction is part of the record.

## Wiring

- `weights_path()` — repo `watch/narrative_test_weights.json` by default; `NARRATIVE_WEIGHTS`
  env var points at a different file for what-if runs (no edit needed to test a hypothesis).
- `load_weights()` — reads the file; missing file, broken JSON, or missing keys fall back
  to neutral 1.0. Detector still runs uncorrected, never crashes. Range 0.0-2.0.
- `run_tests()` — multiplies each test's raw score by its weight (raw kept as `score_raw`),
  clamps to 0-1, THEN counts positives against the 0.5 flag threshold. Every result carries
  `weights` + `weights_file`, so the output names the dial that shaped it.
- Keys: `tears` (or `tears_trauma`), `archetype`, `clone` (or `phrase_clone`),
  `speed` (or `speed_volume`), `punishment`.

## Receipt (the 3 M7 batches, re-run)

- Baseline (all 1.0): A = manufactured_consent 5/5; B = organic 0/5; C = organic 0/5.
- `tears: 0.5`: A's tears score 1.0 -> 0.5 (verdict holds — raw was a clean 1.0), B/C untouched.
- `tears: 0.0, speed: 0.5`: A drops to 3/5 -> **suspected** (was manufactured_consent);
  B/C speed scores shift (0.262->0.131, 0.391->0.196) but stay organic. The dial moves
  every batch it applies to, and only in the direction the human asked.

## Limits (tri-state)

- SUPPORTED: weights move verdicts deterministically; fallback is neutral; output is
  self-describing. Verified by re-run above.
- UNPROVEN: whether notch-by-notch human correction converges on good long-run weights —
  that needs real FP/FN events to accumulate in `overrides`. This build makes the
  corrections *possible and recorded*, it does not pretend to know the right weights yet.
- The overrides array is the memory; if it grows, a later lane can mine it the way
  percolator mines flag repeats (same shape: repeats -> invariants).

M7's NEXT row is now closed: the loop exists, a human edit is one JSON number away.
