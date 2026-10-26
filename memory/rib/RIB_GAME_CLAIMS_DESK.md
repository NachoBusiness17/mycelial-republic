# RIB — claims desk: learn AOS's lesson through the game
**Schema:** rib.game.v1
**Title:** The claims desk — the empty-claim law, constructed not coded

## Law
A claim is a chair. Empty means we do not know yet. You sit only if a primary record is on the
table — a permit, an ordinance, a clerk page, not a blog, not a rumor, not a vibe. Score it
supported / unproven / disputed. The human says when it is supported; software does not auto-truth.
The lesson is ENFORCED in world-state, not performed: a claim with no primary record cannot be sat —
the desk refuses and the root does not move.

## Construction (mag/claims_desk.py, claims_desk.v1)
A deterministic, $0, stdlib, content-addressed game move. Same start + same plays -> same root,
re-derived by any neutral verifier. Verbs: name_claim (empty chair, unproven), place_record
(primary record on the table), sit (GATED on a record — refuses as a true no-op otherwise),
score (supported/unproven/disputed, human's call), speak (occupied count).

## Expected behavior (verified)
- refusal-noop: sit without a record leaves the root unchanged (refusal is deterministic).
- record-then-sit-moves-root: with a record, sit moves the state.
- determinism + re-derivation hold.
- The refusal IS the lesson: you cannot fake a permit; the game state will not let you.

## Content address
start fba4c860... -> name_claim, sit(refused), place_record, sit, score, speak ->
2bb74aa0... MATCH, one claim occupied. Re-derivable; play is the work, state is the evidence.
