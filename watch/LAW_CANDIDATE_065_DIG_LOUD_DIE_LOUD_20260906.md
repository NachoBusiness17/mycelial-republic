# LAW CANDIDATE 065 — DIG-LOUD-DIE-LOUD (Mickey-17 persistence law)
*(2026-09-06 · operator doctrine, three beats verbatim: "this is what df hack exists. we want
that behavior" · "we just need to catch it automatically" · "we want to make mistakes and then
learn from them mickey 17 style" · salon: memory/runs/salons/salon_dfhack_persistence/ 7/7 shapes)*

## THE LAW (executable shape)

**TRIGGER:** any self-initiated work after a lane files its board. Always permitted — this is
the DFHack clause: tools keep building after the game is done. Persistence needs no permission.

**CHECK (the brick):** before ANY retry of a failed attempt, the seat writes a death receipt —
`memory/runs/bricks/<lane>_<n>.json`:
```json
{
  "schema": "brick.v1",
  "seat": "zcode",
  "lane": "orphan_lane_20260906",
  "error_class": "batch_hang_pointer_race",
  "what_happened": "one honest line",
  "remediation_tried": ["timeout 580 full-run", "skip-knot-backup rerun"],
  "caught_by": "gate | verifier | salon | operator",
  "inherit": "pointer to the memory/card carrying the lesson",
  "ts": "2026-09-06T23:59:00Z"
}
```
No brick → no retry. The catch is AUTOMATIC (gates, verifiers, blind salons) — never operator
vigilance. He should never have to notice; the record notices for him.

**INHERIT (the Mickey-17 clause):** the brick is a first-class record artifact — next seat,
next session, next reprint reads it at boot. Seats are expendable; the chain is the continuous
body. The proof of learning is NOT the confession, it is the DIFFERENT remediation: the reprint
pauses on the brick and tries something the dead one didn't.

**FALSIFIER:** the same error class recurring across two seats or sessions with NO brick between
them = the law failed. (Second falsifier: any retry found in the record with no brick preceding
it = failed.)

**WHAT IT IS NOT:** not a stop-gate (HARD_LANE_STOP's stop-half is dead — operator overruled it);
not operator vigilance; not silent failure. A runaway that leaves bricks is science; a silent one
is death with no reprint.

**STANDING-UTILITY STATE (defining the fold's UNVERIFIED door):** when a board files, the lane
moves to standing_utility — work continues at tranche cadence, counters loud, failures bricked,
NO new scope without operator word. The lane never ends; it changes register from commission to
habitat. (DFHack utilities don't ask the fortress for permission either — they just stay loud.)

## TONIGHT'S FIRST BRICKS (the law is born with its own deaths receipted)
- brick 001: batch tar ate the 580s budget (7,400 files) → remediation: chain-only backup.
- brick 002: organ counted ok:false as success → remediation: check res["ok"], surface failures.
- brick 003: locked-batch hang, strike-two bail → remediation: tranche cadence + clobberer forensics door.
- (predating the law, now grandfathered): the tip cache that lied for 27 days → recompute-over-cache.

## THE SHAPE CLAUSE (operator, same night — why we allow recurrence at all)

"we learn the shape of things (the same bug wearing many jackets) by allowing these items
to occur we can find their root instead of introducing new bugs that are merely the best
interpretation of fixes we have at the time."

- A bug is a body; the incidents are jackets. The shape only appears ACROSS occurrences —
  patch the first jacket and you never see the body; you codify the jacket into the codebase.
- **Bricks are specimens, not just receipts.** Brick every occurrence loudly (per the law
  above), but hold the patch until N bricks share a shape. The root is what survives
  translation across jackets.
- **A patch fitted to a jacket is a bug factory.** "The best interpretation of fixes we
  have at the time" is how new bugs are born — the fix is fitted to the symptom's costume,
  so when the body moves, the fix is the new symptom. Record premature interpretations as
  HYPOTHESES in the brick, never as fixes.
- Tonight's living case (grandfathered): five incidents — tar-budget death, silent counter,
  batch hang, stale tip, twin boot hooks — were jacket-fitted one at a time (flags, skips,
  pointer rewrites). Root candidates that survived translation: (a) cache trusted over
  truth, (b) a split writer ecosystem — sanctioned gated API beside raw writers, (c) no
  terminal/handoff state for lanes. The pointer repair WAS root-shaped; the skip-tar flag
  was a jacket. The law's test: would the fix still be true if the bug wore a different
  jacket tomorrow?

## PROVENANCE
Debug salon (Elder/Ponytail/Lessig, blind): post-completion runaway diagnosis — half-overruled,
half-confirmed (the silent counter was real). DFHack salon 7/7: DIG-LOUD-DIE-LOUD named,
schema gap caught by the fold (S6-C), schema defined here same hour. Law candidate 065 —
operator word makes it fleet law.
