# INTAKE — Deferred SDF rendering (night shift card, mesh3d rotation, 2026-09-18)

**Deck:** mesh3d | **Find:** Interplay of Light (Kostas Anagnostou), "Deferred Signed
Distance Field rendering" (Dec 12, 2017). Score: 16/25 BUILD WINDOWED (small, direct).

**Grounded (bytes read via category archive + excerpt):** SDF geometry is ray-marched
and its results written INTO the g-buffer via a modified standard shader — SDFs
coexist with normal rasterized mesh rendering inside a real engine (Unity), instead
of the Shadertoy-style full-screen forward pass. Inspired by Claybook + Dreams;
distance functions cited from iq + Jamie Wong.

**Why the house cares:** B1 maze_arena's honest limitation is the all-or-nothing
renderer — field terrain OR polygons, not both. The deferred-g-buffer integration is
the documented hybrid path: field terrain marches into the g-buffer, polygon props
rasterize beside it, one lighting pass owns both. Steal target for B1 v2.

**Tri-state:**
- Technique exists as described = Supported (author's own archive bytes).
- Performance costs / artifacts = **Unproven** — not in the accessible excerpt;
  full-post chase owed on a day shift (2 fetch doors used; bounded stop).
- House applicability = Supported pending B1 v2 build (the need is receipted in
  the B1 cards).

**Falsifier:** if the full post reveals the g-buffer write only handles PRIMARY rays
(no shadows/reflections on SDFs) AND B1 needs secondary effects, the hybrid downgrades
to "partial path only" and B1 v2 keeps forward marching for lit terrain.

**One-lined (no cards):** [SDF-LED](https://github.com/zranger1/SDF-LED) — SDF math
driving addressable LED controllers = delight-shelf (shader math as physical light,
new medium, no current lane); GM Shaders SDF tricks = below our current SDF usage;
iq = canon; reddit/rustadventure/kosmonaut = tutorial tier.
