# BRING-IN PLAN — hot lattice hologram, kubernetes, docker (2026-09-18)

**Operator order:** self-steal hot lattice hologram + kubernetes + our docker;
we stopped using them and that was a mistake — bring them in.
**Survey verdict:** docker never stopped (3 containers, 5 days healthy);
k8s is solved-but-sleeping; the lattice renders but was starved of new data.
This is not a resurrection — it is a re-wiring into current operations.

## TRACK 1 — DOCKER (the execution layer, alive and underworked)

*What it is:* mag-sovereign (host: dashboard 8765, api 8000/8001, ghost 9000),
mag-worker (the executor), mag-redis (the queue bus) — up 5 days, healthy.
*Why it felt stopped:* the wave routes to REMOTE lanes (groq/nim/zai), and
local work runs venv-direct — the containers idle-serve the dashboard.
*Bring-in:*
1. Local-execution lane work routes through `docker exec mag-worker` (the
   pattern the build lane already used) — isolation for anything untrusted
   or heavy.
2. mag-redis becomes the mesh's live queue beside watch/room.jsonl (chan =
   durable rows; redis = hot signals between containers).
3. The hologram (track 3) serves FROM mag-sovereign:8765 — the dashboard is
   the hologram's wall.

## TRACK 2 — KUBERNETES (the breeding scale, solved and sleeping)

*What it is:* `deploy/flock-k8s-solved.yaml` — a batch Job: 5 parallel flock
agents on mag-sovereign:local, ttl 600s, with the fleet invariants annotated
INTO the manifest (consent_first, local_first, no_throne, residual_is_dna,
window_steer). `mag/k8s_bridge.py` is the one system-native surface
(windowless, via mag.headless); gpu_k8s/rib_k8s flank it.
*Why it stopped:* pod-scale was never needed — docker's single host carried
the wave, and the GA (evolution loop) ran its generations in-process.
*Bring-in trigger (declare, don't deploy blind):* **when the go player's
GA needs more parallel genomes than one host gives** (the cathedral map's
Stone 3: self-play against the previous best genome — breeding wants pods).
First action queued: validate flock-k8s-solved.yaml against the current
image + k8s_bridge dry-apply, so the day the trigger fires, deploy is one
command (WANTS).

## TRACK 3 — HOT LATTICE HOLOGRAM (the self-render, starved of harvest)

*What it is:* the fleet rendering ITSELF — lattice_render.py parses the
operator's numbered correction-laws into lattice_data.js (consumed by the
viz pages); law_lattice.json holds 58 LAW entries; isfahan_lattice.html is
the seeded Voronoi-glass render (12 canon presets); sweep_vislab_health.py
watches it.
*Why it felt stopped:* the renderers kept running but were starved — nothing
fed them the harvest (19-family graph, 757K-row catalog hot temps, quantized
thought pools, the skills).
*Bring-in, done now:* lattice_data regenerated fresh this pass (your laws
I–XX rendered from source). *Bring-in, queued (hologram v2):* one render
surface fed by the new organs — law pools (lattice) + family nodes
(knowledge graph 19) + hot estate temps (ESTATE_INDEX) + quantized-thought
pools (12 flash laws as near orbits) — the wall where the operator sees the
whole estate breathing. Served from mag-sovereign:8765.

## THE SHAPE (why this trio belongs together)

docker is the body that runs, k8s is the body that breeds, the hologram is
the face that shows. The context OS (kernel/ram/scheduler) runs ON docker,
breeds THROUGH k8s, and is SEEN AS the lattice hologram. Stopped, they left
the fleet with a mind but no body and no face.

## RECEIPTS

- docker ps: 3 containers up 5 days (healthy) — mag-sovereign/worker/redis
- flock-k8s-solved.yaml read: 5× parallelism, invariants annotated, ttl 600s
- k8s_bridge.py read: windowless system surface confirmed
- lattice_data.json/js REGENERATED (10KB/6.6KB fresh, laws I–XX)
- law_lattice.json: 58 LAW entries (LAW-001 AX-RESOLVE-OVER-PIXEL-GUESS…)
- WANTS lines added: k8s validate-then-trigger; hologram v2 feeding
- tri-state: container health + file reads + render regen = Supported;
  k8s deploy readiness = Unproven until bridge dry-apply runs
