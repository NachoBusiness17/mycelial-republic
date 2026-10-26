# VERIFICATION: inbox librarian sample, 2026-10-17

Terminal-RSI rule: keep only verified work. A seeded random sample (seed 20261017) of cards was checked against the file's own content (first ~60 lines read, key-like strings masked). Sensitive paths were excluded from the sample. Failed cards carry `verified: false` in catalog.jsonl, and passed cards carry `verified: true`.

| sample | n | correct | accuracy |
|---|---|---|---|
| Model tier, per-file (qwen2.5:7b, root files) | 30 | 15 | **50%** |
| Model tier, folder-level (one call per unmapped active folder) | 10 | 8 | **80%** |
| **Model tier, combined** | **40** | **23** | **57.5%** |
| Rule tier (excluding the purely mechanical `age>30d` rule) | 20 | 14 | **70%** |

The `age>30d` → ω rule (12k+ cards) is date arithmetic on LastWriteTime/filename date. It is correct by construction, so it was not sampled.

## Failure modes seen

1. **γ LANES is over-assigned by the model.** Everything in this estate mentions "AI models", so the 7b model drops ops notes (MORNING_REPORT, W3Q_ATTENTION_DAM), research notes (BOUNDED_TOOL_SURFACES) and games (MAG_DANCE_SPEC) onto γ.
2. **α CHAIN attracts anything that mentions memory or knots** (subsystems_map, SCRATCH_HAUL_SALVAGE, W3_FRONT_DOOR, DROP_MATTER_COMPILER). One summary simply echoed the shelf description.
3. **χ is used for clear ops docs** (WIRING_DEBT_CENSUS, W3W_STEER_LIVE) at confidence 0.8, so they are not flagged needs_review.
4. **Campaign-folder rules are coarse.** `burn_wave_*` / `burn_reset_*` → γ is right for the campaign, but individual files inside are ops scripts (drift-patrol prompt, pointer-rot checks), essays (w4-50 cathedral), game probes, and research (stealth-sw-15 via the STEALTH prefix).
5. **Model confidence is not calibrated.** Nearly every answer says 0.8-0.9 whether right or wrong, so the 0.6 threshold rarely fires on the per-file tier. needs_review mostly comes from pending files, non-readable root files, and the one failed folder call (gala_20260925, empty answer).

## Implications

- Treat rule cards with `folder:frontier_olm*`, `.mimosa`, `RECEIPT`, `DRIFT_PATROL`, `BOB`, `X_` and `age>30d` as reliable.
- Treat model cards as a suggestion until `verified: true`.
- Cheap fixes for a next pass (not applied): add an explicit "if it's an ops/maintenance receipt, choose zeta" tie-break to the prompt; few-shot examples from the verified sample; split `burn_*` folder rules by filename prefix (`B2_*_check` → ζ); use a larger local model (gemma4 / qwen2.5:7b-instruct-q8_0) for the root tier if time allows.
