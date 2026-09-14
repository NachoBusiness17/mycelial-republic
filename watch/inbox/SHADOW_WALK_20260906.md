# SHADOW WALK — voxel roguelite · vision-gated · JIT
**2026-09-06 · builder "walk" · implements watch/SELF_STEAL_SHADOW_PHYSICS_20260906.md as a walkable place**

**Files**
- `dashboard/static/shadow_walk.html` — ONE self-contained page (74 KB, zero deps, no three.js, no network, no CDN). Hand-rolled software column raycast (Comanche-style heightmap march), internal 320×200 upscaled pixelated (house maze_arena grammar), potato-proof: no WebGL, typed-array fills only.
- `dashboard/static/_build_shadow_walk.py` — the generator: voxelizes `state/shadow_work/volume.json` (9,305 pts, shadow_work.v1) + `weights_volume_qwen3b.json` into a 288×64 heightmap, emits the page AND `state/shadow_work/chunk_manifest.json`.
- `state/shadow_work/chunk_manifest.json` — 72 chunks (16×16), each `{id, origin, dims, biome, slab_id, stats{cells,points,max_law,mean_law,questions,tensors}, content_hash, vision_validated:false}`. Hash algo fnv1a32, identical impl both sides (python builder + in-page JS). data_hash `aaad8ddf`.

**World = the data, quantized** (block types by measurement, no decoration)
- x = part idx scaled, y = law density (height `1+round(log2(1+law)*1.7)`), z = log2(chars).
- law_hits 0 → void-dark stone (the shadow volume); 1–24 dim ore; 25–59 mid; 60–89 bright cyan; ≥90 gold ore; questions≥10 → water-blue; weights annex = second biome, terrain height+brightness = per-layer norm_rms ramp (walker 50's RISING 3.97× gradient is literally ascending brightening terrain; spawn key W faces down the ramp).
- BFS wavefront from the doctrine core (max-law cell, [113,56]) = the arena lightmap grammar; corridors carved downhill on the field = Fermat least-time paths; slab boundaries (all 50) raise chamber walls, corridors punch doors through.
- Roguelite: NEW RUN (N) seeds mulberry32 from `fnv1a32(data_hash:run#)` — same data, different traversals; natural local-minima + seeded spurs terminate in dark-side ORGAN monoliths (amber rim).

**Physics implemented (per the dictionary)**
- DOF: focal distance defaults to the attention target (doctrine core), Q/E or wheel slides the focal plane; blur = thin-lens CoC proxy `|d−f|/(0.6f+7)` → columns smear + fade off-focus. HUD: "focus = attention · blur = falloff (thin-lens)".
- Lensing (L): the marched ray deflects toward the core each 4th sample, `Δ ∝ 149/(d²+30)` — weak-lens form; image visibly warps near the mass. Label: "attention is mass".
- Shadow (S): shadow-only view — non-void mass renders as silhouette, void stone stays.
- Fog of war IS the anti-hallucination barrier (vision-gated JIT): chunks materialize only within radius 46, budget 2/frame (visible pop-in = JIT); unvalidated chunks render as ghost wireframe scanlines (structure, no texture/light); chunk-boundary edges lit.

**Vision gate / falsifier hooks**
- **No hash, no draw.** V = vision pass: in-browser fnv1a32 recomputed from the embedded data voxels per chunk, compared to the manifest → `vision_validated:true` only on hash match; mismatch renders RED tamper stripes.
- Node harness (stubbed DOM, real page code): `VISION_PASS validated=72 tampered=0 of 72` (JS↔python hash agreement), `TAMPER_TEST tampered=1` (corrupted hash caught). `node --check` PASS.
- The seat's later vision pass flips flags in `state/shadow_work/chunk_manifest.json`; H opens a paste box that loads an updated manifest — `data_hash` must match or it's rejected.
- LAW-061 stamp in footer: "projection: behavioral features quantized to voxels — preserves nothing about semantics". Footer carries "voxel JIT · vision-gated · potato-proof".

**Controls**: WASD fly (Shift sprint) · ↑/↓ fly fwd/back, ←/→ turn · mouse-drag look, double-click = pointer lock · Q/E or wheel focal plane · Space/C rise/sink · L lens · S shadow · V vision pass · N new run · B/W biomes · P internal res (320×200/240×150/160×100) · H help+manifest paste.

**Verify receipts**: `node --check` PASS (70,988 JS bytes) · `curl http://127.0.0.1:8000/static/shadow_walk.html` → 200 (74,044 B) · vision contract 72/72 JS=python, tamper caught 1/1. Not yet done: real-browser eyeball pass + the actual vision-validation pass (that's the next seat's flip, by design — the page ships 100% ghost).

**Nav entry (NOT wired, per law — nav.js untouched)**: `["/static/shadow_walk.html", "Shadow Walk"]` — insert beside `["/static/maze_arena.html", "Maze Arena"]` (nav.js:55).
