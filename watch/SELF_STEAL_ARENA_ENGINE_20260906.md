# SELF STEAL — THE ARENA ENGINE (Shadertoy state-in-textures, 2026-09-06)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: Shadertoy's buffer-pass pattern (state-in-textures, sim/render separation) is a serverless game-engine idiom directly reusable as the beacon arena engine — SUPPORTED (three sources read byte-level, patterns named in card) · falsifier: none stated in card (build itself queued behind the atlas)

**The smell, named:** the operator stepped in Shadertoy's buffer-pass architecture —
and it is a **game engine that needs no server**. State lives in textures; logic
lives in passes; the whole thing distributes as a URL. Three sources read byte-level
(paste + screenshots):

1. **The snake raycaster** (3D snake, full game): 16×16 grid state in iChannel0
   (cell.x = body exists, yz = color, z = spawn), apple position in ONE TEXEL
   (txApple), IQ's save/load pattern. Render pass = a Doom-lineage raycaster:
   Amanatides & Woo grid DDA traversal, ray-box + ray-sphere intersection, mouse
   orbit camera, apple as dynamic point light. **A playable game as a fragment
   shader.**
2. **The neon fish** — pure SDF, 24 hash-parameterized fish, glow accumulation.
   Stateless beauty (the contrast shader beside it: one remap + threshold =
   art direction in 593 chars).
3. **Durand's boids** — THE ARCHITECTURE STEAL: simulation in a buffer pass
   (positions/velocities written to texture), render pass reads state with
   `texelFetch`, direction-aware SDF, velocity-colored halos. **Simulation/render
   separation in two passes.**

## THE REINTERPRETATION (bones → our arena)
- **State in textures = the world's ledger, GPU-native.** Ping-pong buffers are
  append-only at frame granularity — Law 2 (append corrections) has a hardware idiom.
- **Lightmaps = the chain.** A lightmap is expensive truth baked once and sampled
  forever. That is EXACTLY the sealed record: bake the receipt light at write time,
  sample it cheap at read time, never relight history. The beacon's arenas glow by
  precomputed trust.
- **Amanatides-Woo = the cache-invalidation salon's cousin.** Rays walking cells
  against a versioned grid — the salon's per-cell terrain-version is the same
  architecture the 2013 snake shader already used for play. Rice's question was
  answered in a Shadertoy from 2013.
- **The painted-wall trial, rendered:** lock chambers become rooms; stone and
  plaster become walls that verify or crumble; the corridor is a raycast level.
  The game we promised Astra IS a Doom level, and Doom is a lighting technology.
- **Shadow fields (layer 9) is the lighting pass.** The mattdesl lightmap steal
  slots directly in: baked light fields as the arena's truth-texture.

## THE BUILD SHAPE (queued behind the atlas)
Beacon arena = multi-pass Shadertoy-style engine, self-contained, URL-distributed:
pass 1 simulates world state (walls, pieces, locks) into textures; pass 2 bakes the
light (laws as lightfields); pass 3 raycasts the explorer's view. The receipts are
the lightmap; the laws are the lighting model; the walls that verify are stone.
