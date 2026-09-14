# SHADOW WORK — the model as volumetric environment
**2026-09-06, zcode seat · operator: "you could turn the model on our disk into an environment you traverse... a fanout of 50 agents across whatever the fuck this entire model 5.3flash model is... map the multidimensional objects within each space and represent them via your visual detection/interpretation" (Houdini/water volume-mapping, college era)**

## THE STEAL — water-mapping was always ours
The operator's college technique — immerse voluminous objects in water, read the
displacement — is *exactly* our BFS flood: the maze lightmap IS water-mapping of a space.
SHADOW WORK inverts the direction: stop mapping spaces the model moves through; **map the
model itself as the voluminous object.** Immerse it in probes, read the field.

## THE VOLUMES (what "the model" is, as we hold it)
1. **BEHAVIORAL VOLUME ($0, on disk now):** 9,305 reasoning parts / 22MB of 5.3-flash's own
   thinking, verbatim. 50 slabs × 187 parts. Axes: part-index (x), doctrine-density (y),
   part-size (z), questions (color), code-ratio (size).
2. **WEIGHTS VOLUME (on disk now, stand-in):** Qwen2.5-3B-Instruct.gguf + Coder-7B in LM
   Studio bridge-inbox — REAL weight tensors. Tensor-name/dims/dtype/entropy parsed from the
   GGUF container (mmap, no inference). The pipeline proves itself here before the real thing.
3. **THE REAL THING (P2, GO-gated):** 5.3-flash MIT weights, Q4 quant, 363G free — download
   and the full 50-slab tensor scan runs on the actual substrate. **Rocinante's first cargo.**

## THE FANOUT — 50 walkers, one immersion
50 shadow walkers, one slab each, deterministic carver (`mag/shadow_slab.py`) so the 50 CSVs
tile seamlessly. Width 50 = **the salon's ceiling experiment executed with real work**:
who queues, who dies, who finishes — the concurrency map of the Max seat at 4x its tested
width. Receipts double as the scan.

## THE VISION LOOP (the operator's "visual detection/interpretation")
Render the volumes (`shadow_work.html` — Shadertoy grammar: density, slices, isosurfaces)
→ the seat LOOKS at the render with vision and writes findings → **falsifier: the visual
read must predict the computed stats** (blind read vs ground truth, ≥70% agreement). The
seat's eyes are the instrument; the falsifier keeps them honest.

## SHADOW WORK PROPER
Shadow cells (refusals, A2) get rendered AS shadows — volumetric darkness, not a list. Where
the model blocks light is structure. The bank's opening refusal (163 parts) is the first
shadow body; T1's refusal battery (GO-gated) is the rest of the scan.

## V1-RESPEC (operator, 09-06: "my local card is shit... vision gated just in time renderer. with voxels... roguelite generative. like our wow clone")
The walker renders **voxel roguelite, potato-proof**: (1) WORLD = voxel lattice of the volumes —
law-dense = ore, zero-law = void stone, question-dense = water, tensor blocks = biome with the
RISING norm gradient as a brightness ramp; slab boundaries = chamber walls, field-gradient paths
= corridors (the arena's BFS grammar self-stolen). (2) RENDER = software raycast, low internal
res, fog by distance — no WebGL/three.js requirement. (3) **VISION-GATED JIT** — chunks
materialize only near the camera, each carrying {content_hash, stats, vision_validated} —
unvalidated chunks are WIREFRAME; the seat's vision pass flips them solid. **Fog of war = the
anti-hallucination barrier: unwalked = unvalidated = fog. No hash, no draw, generalized.**
(4) ROGUELITE = deterministic per-run permutation from a data hash. (5) The WoW-clone bridge:
azerothcore is chunk-streaming with fog — the same architecture at server scale; the fleet
lightmap is the minimap. Physics card stands (eikonal/Fermat/lens/DOF); voxel DDA traversal is
the same ray-march family as the shadow field.

## THE DOOM MIRROR (operator: "how does this tie to llm doom self steal", 09-06)
The LLM-Doom family is our construct with the normal flipped:
- **Torchwright Doom** compiles the game INTO tensor ops — Doom-as-weights. SHADOW WORK renders
  weights AS a world — weights-as-Doom. Same bijection, opposite normals: environment↔tensor
  space is traversable from both sides, which is the whole cartography bet proven in reverse.
  [UNPROVEN locally — pasted claim; but Doom-in-X is a proven art genre, engineering-plausible.]
- **DOOM-Mistral's trick is frame-translation**: the world downsampled to the model's native
  substrate (ASCII). Ours inverted: the model already rendered its own gameplay as text — the
  thought bank IS 9,305 native frames of 5.3-flash playing itself. The behavioral volume is
  built from the model's own screen-captures.
- **DoomVLM = our vision gate**: vision-in-the-loop, but our "action" is VALIDATION — every
  frame I truth flips a fog chunk solid. DoomVLM shoots; we swear in.
- **THE FUSE — the game is the falsifier:** playing the model-dungeon (layer gradient 3.97x =
  elevation, refusal directions = hard walls per A2, invariants = loot per arrakis) generates
  probes → probes fill the TESUJI map → the map gates what can be walked next. Playing =
  mapping = researching. One loop, three names.

## FALSIFIERS (inherited + new)
1. **VISION-GROUND:** visual interpretation vs computed stats ≥70% agreement.
2. **SEAM-LESS:** 50 slab CSVs aggregate with zero gaps/overlaps (deterministic carve).
3. **TENSOR-HONEST:** GGUF stats match published tensor counts for the arch (or DISPUTED).
4. **CEILING:** the width-50 run receipts the vendor concurrency wall (predict ~10-12 in-flight).
5. **TRAVERSAL:** by Sep 20, a rendered model volume you can WALK (navigate) on the dashboard.

---

AMENDMENT 2026-09-07 (Astra audit — see watch/OLLAMA_MAZE_SALON_20260907.md, Witness #2):
Two corrections on this card's numbers:
- "layer gradient 3.97x geometric" — use the repo's own reconciliation
  (watch/inbox/SHADOW_PHYSICS_LAB_20260906.md): 4.02%/layer is the logged arithmetic
  fit (slope 0.0135, r 0.739); the log-linear COMPOUND rate is 1.52%/layer
  (slope 0.01505/blk, r 0.705). "3.97x" is not a third figure; cite both rates.
- Specimen binding UPGRADED: Astra flagged byte identity between the walked specimen
  (C:\Users\foste\.lmstudio\bridge-inbox\Qwen2.5-3B-Instruct.gguf) and the ollama
  blobs as UNVERIFIED. VERIFIED 2026-09-07: specimen sha256 5ee4f07cdb9beadbbb293...
  equals ollama blob sha256-5ee4f07c... (model qwen2.5:3b-instruct), both
  1,929,903,008 B. The 434-tensor walk binds to the live ollama weights byte-exactly.
