# STEAL — MemLands: the dual-function memory surface (2026-08-11)

Operator: "MemLands ... a dual function rewrite sort of like the RIB file itself so when it goes in
it's sort of doing a steal protocol while it's reading and writing so it's sort of this flow state
which is what I'm trying to achieve with our flocking." + "swarms and it's really just VRAM but used
in a different fashion like ghosts mem tools."

## Synthesis (all machinery already exists — MemLands binds it into ONE flow)
- read    -> mag.ghost_memlance.select   (grounded, provenance-verified memory selection)
- write   -> mag.work_register.record    (content-addressed verkle knot + shared manifest)
- lattice -> mag.gpu_k8s.status          (GPU VRAM as memory) + mag.verkle_bus (Redis<->knot bridge)
- flock   -> mag.flock_job / flock_steal (pods fold knots back into the same lattice)
So the swarm IS VRAM used as a memory surface (like ghost mem tools), and MemLands is the single
surface where ghost reads AND writes that shared lattice in one act. Single-surface theorem applied
to memory (see DEEP_RESEARCH_SINGLE_SURFACE_MEMLANG).

## Built: mag/mem_lands.py (mem_lands.v1, $0, stdlib-only)
- flow(label, content, ctx) — THE DUAL FUNCTION: eliminate → read(grounded) → adapt → write
  (verkle+manifest+bus) → reindex. Reading and writing are the same act = the flow state. A flock
  member's fold and ghost's read both live here on the same lattice.
- read(ctx)   — grounded read (delegates ghost_memlance.select).
- lattice()   — swarm-as-memory view: GPU VRAM telemetry (gpu_k8s) + verkle bus channels + knot tail.
- self_check()— n flows, gpu source, bus channels, knot tail.

## Verified (via OUR headless runner, ghostlance surface)
- ghostlance diagnose: syntax_ok, no real errors.
- flow() ran a REAL fold: eliminate(not dup) → read(4 grounded sources: single-surface-memlang,
  fleet-terminal, window-storm, RIB-protocol) → write(manifest landed, verkle=false — honest, no
  fabricated knot) → reindex(1305 states). Reading + writing = one act, on the shared lattice.
- lattice(): gpu source "none" (no pod reported — honest), bus quiet, real knots present.

## Lessons / law
- Honesty: verkle=false / gpu="none" are reported as-is (grounding law) — never fabricate.
- Dual-function = read and write are the same flow; that IS flocking (collective adaptation on one
  shared lattice). Registered as ghost_server RESOURCE memory/lands.
