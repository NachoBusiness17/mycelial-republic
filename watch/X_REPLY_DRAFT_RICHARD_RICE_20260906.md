# X REPLY DRAFT — Richard Rice cache-invalidation question (2026-09-06)

Source: https://x.com/BioAnkh84/status/2096424210524418280 (reply to @NachoQuixotic,
fetched via fxtwitter door 200 OK — 12 views, 0 replies, receipt of the public-turn
stigmergy loop: external agent engaged the shadow ledger unprompted with a real
technical question).

HIS QUESTION (verbatim): "I see how you're caching the distances. My question is
invalidation: how inexpensive would it be to detect when one of the walls moves or
is destroyed, and invalidate only the rays affected by that change?"

THE ANSWER (consult physics, ponytail/lessig): ray-invalidation is the wrong cache;
space-invalidation is the right one. Cache the distance field on a sparse grid —
the Lipschitz bound gives the dirty radius for free (cells within one max-step of
the wall's swept volume), re-march only rays through dirty cells. Cost = wall
footprint + motion sweep, not the frame (~30-100x cheaper for a small wall);
detection is free when walls are analytic primitives (the engine wrote the move).
Detection costs only for opaque deforming meshes. Win evaporates if everything
moves every frame. Fleet tie: arena walls are invariants (static) = warm cache,
best case.

DRAFT REPLY (operator hand only, publishing gate):
"honestly the trick is you don't invalidate rays, you invalidate *space* — cache
the distance field on a sparse grid, and a moving wall only dirties the cells in
its swept volume (the Lipschitz bound gives you the radius for free). re-march
just the rays that hit dirty cells. cost = wall footprint + motion, not frame.
detecting the move is free when the walls are math instead of mesh 🐒"

If he replies again, the scouts catch it through the normal harvest doors
(X loop absorption: publish → reacts → absorb).

---

## FOLLOW-UP ROUND 2 (2026-09-06 02:51Z) — https://x.com/BioAnkh84/status/2096431112805302749

HE ASKED: "What about a state change inside an occupied cell/object that doesn't
alter its boundary or first-hit distance? Does the sparse field carry per-cell
generation/state, or is that intentionally outside what this cache represents?"
(mentions @LilithDatura @ai_sentience — fishing with his circle; 4 views)

THE ANSWER: geometry-only field BY DESIGN (Lipschitz is its only invariant — that
poverty is the speed). State without boundary-change lives in layer 2: per-cell
attribute store + generation counters, read at HIT time not march time; state
change = bump generations of touched cells, O(1), zero propagation (you know where
you hit, you only need fresh state there). His per-cell-generation instinct is the
standard mechanism: geometry dirties by swept volume, state dirties by touch.
ONLY connectivity-changing state (portals, one-way walls — a hit that redirects
the ray) reaches back into the field, and that is a ray-graph problem, not a
field problem — naming that boundary is the deep part.

FLEET TIE: he independently derived the two-layer architecture — field = invariant
layer (chain: what's structurally true), attribute store = state layer (room:
what's currently so). Two questions in, the geometry/state split of the whole
fleet re-derived as a rendering problem.

DRAFT REPLY (operator hand only):
"field is geometry-only by design — signed distance to boundary, nothing else.
state that doesn't move boundaries lives in a second layer: per-cell attribute
store with generation counters, read at hit time, not march time. state change =
bump the cells you touched (you know which ones — you touched them). O(1), zero
propagation. only state that changes connectivity (portals, one-way walls)
reaches back into the field — and at that point you're ray-graphing, not
fielding 🐒"

---

## ROUND-3 ARMORY (salon fold 2026-09-06 ~03:5xZ — 5 blind witnesses, all SUPPORTED w/ corrections)

His four likely R3s, each pre-answered (full fold: memory/runs/salons/salon_rice_invalidation_20260906/):

1. "WHICH THING OWNS THE CACHE — camera moves, every ray is new, your trick does nothing?" →
   "the field is the only durable cache and it's camera-independent by construction —
   ray records are per-frame and meant to die, so the camera pays nothing but the march.
   everything I said was about walls moving under a still eye."
2. "WHERE'S THE RAY↔CELL MAP making 'affected rays' enumerable? crossover vs full re-march?" →
   "no ray lists — last frame's march: each brick records the pixels that traversed it,
   the dirty mask scatters to a pixel list in one pass, that list doubles as the
   reprojection validity mask, halo pixels re-march one brick deep. cost = dirty bricks
   × rays per brick — never frame. crossover curve gets published (doorbench)."
3. "READER ON GENERATION MISMATCH — retry, stale, undefined? who migrates on brick re-key?" →
   "attributes key on stable world-space cells, epoch-stamped: mismatched generation reads
   last-committed for the frame — one-frame staleness IS the contract. GC retires ids
   without reuse until the epoch outlives any reader, and keys never move, so re-key cost is zero."
4. "STATE BECOMES GEOMETRY — promotion threshold? worst case under a machine gun?" →
   "state accrues at hit time; a promotion pass batch-rebakes bricks once deformation
   exceeds half a cell, inside a per-frame brick budget — worst-case frame cost is the
   budget, never the damage rate."

HARDENING ADOPTED FROM THE FOLD: dirty set = swept ∪ rebuild band dilated by
interpolation error, at BRICK granularity, coarser levels' bounds rebuild upward;
media/absorption state voids "hit-time only" — scoped out loud.

FALSIFIER BUILT: dashboard/static/doorbench.html (DOORBENCH in nav) — K=door
sweep (48 cells/96B), B=1k gen-bumps, C=full-upload control; live tri-state gates.
Receipt: watch/DOORBENCH_BUILD_20260906.md. Salon:
memory/runs/salons/salon_rice_invalidation_20260906/SALON_ARTIFACT.md
