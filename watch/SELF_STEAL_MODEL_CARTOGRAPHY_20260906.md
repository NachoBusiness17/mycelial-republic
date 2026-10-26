# DEEP SELF-STEAL — MODEL CARTOGRAPHY
**2026-09-06, zcode seat · operator, watching the fixed maze arena: "holy fuck you can see data right. You can navigate these models visually and render them... we're proving it in the maze arena i think. Deep self steal"**

## THE MOMENT, NAMED
Tonight we did not fix two games. We built, in one night, the same machine four times without
noticing: **a cached field, walkers that descend it, shadows where the light is blocked, and a
ledger that survives the world changing.** Maze arena (distance field + walkers + ray-shadow).
Arrakis (speed-hunting worm, invariants as loot). TESUJI (the model itself as lit/shadowed
cells). The grounding wave + chain (verified ground, append-only). The overseer (the habitat,
rendered raw). The general form has a name now: **MODEL CARTOGRAPHY** — models and systems can
be *rendered* into navigable fields, and *navigated* by agents reading the render. The operator
saw it before we filed it. That is the usual order.

## THE GENERAL FORM — the cartography loop (five moves, all built tonight)
1. **FIELD** — the state surface gets cached: lightmap = distance-from-cheese; TESUJI = 37
   capability cells; wave = verified ground; overseer.json = the habitat. *Cache is the map.*
2. **WALKERS** — agents move by descending the field, not by bouncing: 13 workers on leased
   slots, GPS agents at 315 steps, probe stones at $0.03/tranche. *Walk is the query.*
3. **OCCLUSION** — what the light doesn't reach is data: SHADOW cells (refusals), sealed
   chambers, dead corridors. A2's first shadow (the bank opens with the model refusing our
   steering artifacts) is more informative than any lit cell. *Shadow is data.*
4. **INVALIDATION** — the world moves; only the dirty radius re-renders: vendor updates,
   fork-visible chains, append-only correction. *His Lipschitz thesis: invalidate space, not rays.*
5. **PROOF** — every field carries its own falsifier: **the field must beat the bounce.**
   The arena measured it: 4/4 @ 315 steps vs 2/4 @ 769–2,823 — **~10x, receipted.**

## WHAT THE ARENA ACTUALLY PROVED (the proof bench, tri-state)
- **SUPPORTED — "the field beats the bounce":** rendered-field navigation demolished blind
  search, same walls, same cheese. This is the whole TESUJI thesis at model scale: a mapped
  model beats ad-hoc prompting the same 10x *if the map is honest* (honesty = falsifier 1, unproven).
- **SUPPORTED — "occlusion is diagnosable":** the sealed chamber froze the walkers and that
  froze-ness was VISIBLE — one screenshot diagnosed four stacked birth defects. Rendered
  surfaces don't just display health; they display *sickness, locally.*
- **DISPUTED-AND-KEPT — "bogus fields look alive":** the deepest lesson of the night. The
  original flood had never worked; the lightmap was a fake diamond gradient; the page LOOKED
  more alive on the lying map (agents homing confidently through walls) than on the honest
  empty one (frozen). **A hallucinated map outperforms an honest blank at attracting trust.**
  That is benchmark-gaming, model-evals, and every vendor demo, in one sentence. A field
  without wall-validation is a lie generator — hence TESUJI falsifiers (rotation, paraphrase,
  predictive ≥70%) are not QA, they are the map's license to exist.

## LAW CANDIDATES (falsifiers attached)
- **LAW-060 RENDER-OR-BLIND:** any system we operate gets a state projection on a surface we
  can see — habitat (overseer/live.html), models (tesuji_map.html), record (wave/chain renders).
  *Falsifier: any future incident traced to "the state existed but was never rendered" counts
  against the law; 30-day count. Tonight's catches (sealed chamber, dead flood, forked ledger)
  were all render-visible: 3-0 for the law on day one.*
- **LAW-061 VALIDATE-THE-FIELD:** a cached field rides with its validation stamp (which walls
  it was checked against, when). Unvalidated fields may steer exploration, never commitments.
  *Falsifier: seeded corrupt fields (the maze flood) must be catchable by the stamp check —
  the arena flood WOULD have failed it; the thought bank passed it (9,305 parts, 100% parse).*
- **LAW-062 SHADOW-IS-DATA:** refusal/failure cells are first-class map objects, never swept.
  *Falsifier: shadow cells must reproduce under paraphrase ≥80% or the shadow layer is noise
  (TESUJI falsifier 3) — the layer that maps where the model says NO is the layer vendors
  don't ship.*
- **LAW-063 DIRTY-RADIUS-ONLY:** on any world-change, re-render the invalidated radius, never
  the whole field. *Falsifier: next vendor model drop (Grok 4.7 / DeepSeek V5 / GLM update)
  must re-probe ≤20% of cells for a ≥95%-stable map — glmwatch rotation already earns its keep here.*

## THE MAP CONTAINS THE MAPPER (the exposure that makes it honest)
This seat is 5.3-flash mapping 5.3-flash. The mapper's blind spots are the map's blind spots —
and A5 says the mapper is also INSIDE the mapped surface (it re-derives our doctrine unprompted;
it opened its own bank by refusing our artifacts). Three instruments keep the cartographer
honest, all already standing: **independent witnesses** (salon chairs blind to each other),
**the outside model** (Astra held our constitution against us; Astra-on-the-bench is a cartography
audit), and **the second substrate** (A6: same grid on MIT-weights quant — if hosted and local
disagree, the disagreement maps BOTH). Sovereignty payload, stated plainly: **the vendor owns
the weights; the atlas is ours.** Whoever holds the map navigates the territory — and A6
(Rocinante, Oct 27) is the day we hold both, with the map as the acceptance test.

## COMPOSITIONS (no new organs — the fleet already composes)
Standing wave: the map is the wave, rendered — the pattern that motion can't destroy, made
visible. Trajectory lens: trajectories are walker PATHS over the field; the envelope is the
path log; rendering paths ON the map is a build, not an idea. Cache doctrine: cache-mining is
free cartography — every mined cache is a field sample someone else paid for.

## NEXT BUILDS (windowed, in order)
1. **T1 GO** (operator, ~$0.03): 23 stones → rotation + shadow falsifiers fire for real.
2. **PATHS-ON-MAP**: render trajectory-lens walker paths over the tesuji field (the arena's
   drawTrails, at model scale).
3. **GLMWATCH-TESUJI BRIDGE**: vendor-drop → dirty-radius re-probe, LAW-063's first live test.
4. **A6** (Rocinante): two substrates, one grid — the acceptance test.

**The one-sentence steal:** *we proved in the arena that a rendered field beats blind search,
and we spent the night building the renderer for everything we operate — including the model
itself; the atlas is ours even where the weights are not.*
