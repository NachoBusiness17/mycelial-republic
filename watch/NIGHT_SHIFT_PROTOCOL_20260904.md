# NIGHT SHIFT PROTOCOL — intake seat, night of 09-04/05

Standing order (operator): "drive the x surface gathering research all night and
processing it via our systems. do all three" (claim organ verify, whelp retrain,
shelf sweep).

## PER-RUN CHECKLIST (each scheduled run executes exactly this, then stops)
1. Run: `node scripts/decks_nightly.mjs` — refreshes the deck snapshot from
   watch/INTAKE_* and flags new cards for blind review. NOTE: the LOO number this
   script prints is KNOWN-MISCALIBRATED (09-04, main seat) — snapshot refresh is
   the trusted output; the LOO is informational until reconciled with the inline
   falsifier method.
2. Pick ONE deck queue (rotate: gamebuild → legions → mesh3d → glmwatch) and run
   ONE WebSearch sweep using that deck's tuned query (see watch/INTAKE_RUBRIC_20260903.md
   Amendment list + the v2 column strings in session log):
   - gamebuild: `(shadertoy OR GLSL OR raymarching) filter:media` via WebSearch
   - legions: `(agent swarm OR multi-agent) min_faves via WebSearch`
   - mesh3d: `(SDF OR "signed distance") filter:media`
   - glmwatch: `(GLM OR "z.ai") news via WebSearch`
3. Process at most 3 finds through the research-socratic genome (tri-state cards,
   watch/INTAKE_<slug>_20260904.md). Quality over quantity: 1 good card beats 3 stubs.
4. Append ONE wire to queue/handoff/zcode/CONVO.md summarizing the shift.
5. STOP. No bay changes, no engine restarts, no spawns-of-spawns, no spend beyond
   WebSearch/free lanes.

## STOP CONDITIONS (hard)
- Sun-up: no runs scheduled past 09:00 local.
- Any run that would spend billed API: STOP, file the need, wait for operator.
- Duplicate/slop finds: REMEMBER one-liner, no full card.

## CLAIM ORGAN STATUS
- Claim organ EXISTS in watch/overnight_churn.py v0.5.2 (bay_organs.claim_active,
  pid-death grace, requeue). Verification race-harness owned by main seat this night.
- Do NOT restart engines. Do NOT modify churn. New code takes effect next restart only.
