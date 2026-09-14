# ASTRA HANDOFF — THE KEEPER'S MAZE (journal-grade research handoff)

> **Provenance (read first):** authored by deepseek-pro, operator-driven salon lane,
> 2026-09-07, turn 3 of the "Into the Unknown" session
> (chat.deepseek.com/share/g6becvqmq404aaka1b). Committed by the zcode seat as
> witness content — **condensed commit**: section plan, mapping, architecture,
> falsifiers, metrics, limitations, and checklist follow the witness's own structure;
> quoted fragments are verbatim; where the extraction is condensed the full text at
> the share link is the verbatim source of record (F4 discipline: nothing invented
> here, gaps marked, not filled).
> Witness's own closing status, on record: *"No file write occurred in this session."*

---

## Title (witness's own)

**The Keeper's Maze: Rendering Live Local Inference as a Walkable Field for Substrate Introspection**

**Keywords (witness's):** model cartography; eikonal fields; inference telemetry; ollama;
substrate introspection; falsifiable rendering; local-first AI; Rocinante.

## Abstract (witness's thesis, condensed)

The local_sovereign_agent fleet has independently developed a "maze grammar" — flood,
walker, lightmap, field, shadow, keeper — proven three times: on model weights (shadow
work: 434 tensors walked, eikonal EXACT vs Bellman-0, field beats bounce ~10x), on an
external frontier model (tesuji: 238+ probe cells of glm-5.3-flash), and as codified
doctrine (model cartography: field/walkers/occlusion/invalidation/proof). The one
unrendered object is the live inference process itself. This handoff specifies the
render: the host ollama eye (v0.32.7, 13 models, loopback) as a walkable field —
prompt-eval as flood-state, tokens as ghost-walkers on a layer tunnel, the maze fork at
the sampler, attention as symbolic lightmap, logits as proxy field, the process as a
file-fed Keeper narrating under a tiered honesty gate — with a falsification protocol
(F1–F6) that makes the render disputable rather than decorative, and a checklist making
it the dress rehearsal for Rocinante-day substrate introspection (4x Mac Studio,
Oct 27).

## Background — the three receipts (witness's sections, our cards)

1. **Shadow Work** — the weights volume as environment (watch/SELF_STEAL_SHADOW_WORK_20260906.md):
   434 tensors, 99.69% accounted; layer gradient rises 3.97x geometric; eikonal EXACT
   vs Bellman-0; field beats bounce ~10x; 50/50 walkers home at width 50, "the wall is
   load-dependent."
2. **Tesuji** — the external atlas (watch/TESUJI_MAP_5_3FLASH_20260906.md; mag/tesuji_map.py):
   model as field, probes = stones, refusal = shadow; 238+ cells at $0.01-scale; one
   phrasing-dependent shadow on file.
3. **Model Cartography** — the doctrine (watch/SELF_STEAL_MODEL_CARTOGRAPHY_20260906.md):
   field/walkers/occlusion/invalidation/proof; "field beats bounce."
4. **The eye's anatomy** — host ollama v0.32.7, 13 models (qwen2.5vl:3b vision,
   maze-keeper:latest 19GB, gemma4 family), 127.0.0.1:11434, sanctioned host service
   (watch/OLLAMA_EYE_TO_HOST_20260907.md); dogfooded end-to-end 2026-09-07 (L0 probe,
   multi-smoke, vision read, cage chat, 19GB keeper wake).

## System model — the maze grammar mapped (v2, post-witness-attack)

(Full table lives in watch/inbox/ASTRA_PROMPT_OLLAMA_MAZE_20260907.md §3 — the
commission Astra actually receives. Witness-corrected: flood = one event-marker plus
persistent ground-state, "the ground the walkers tread"; walkers = ghosts on a single
layer-tunnel, the maze forks at the logits AFTER the corridor; lightmap = SYMBOLIC
(causal mask only; attention unexposed); field = PROXY (no logprobs; sampler knobs +
token identity); repetition penalty and trail decay = two distinct pheromone ops
(negative deposit vs time-fade) — never conflated; shadow = refusal-shape + versioned
phrasing-family suite, entropy alone never marks shadow — "creativity spikes too.")

## Architecture (witness's five organs)

1. **Probe organ** `mag/ollama_maze.py` — stateless LOOK (overseer pattern): one real
   generation captured end-to-end (streamed deltas + final timing chunk + /api/ps
   before/after) → `dashboard/static/ollama_maze.json`. No daemon, no scheduler.
2. **Render surface** `dashboard/static/ollama_maze.html` — nav'd like siblings
   (maze_arena, shadow_walk, self_hologram); flood-ground, ghost-walkers, the fork,
   symbolic lightmap, trail + dirty-radius eviction, shadow cells; every proxy/symbolic
   organ labeled in-surface (F6).
3. **Keeper world seed** `state/ollama_world/world.json` — keeper_voice pattern
   (laws/history/cast; cast = the loaded models); `refusal_suite.json` versioned
   (witness limitation: the suite must be curated and versioned or F3 is unfalsifiable).
4. **Restatement gate** — the keeper narrates only through the 3-tier honesty gate:
   T1 verbatim telemetry; T2 derived stats with formula cited; T3 interpretation only
   when formula-mapped (witness: "could be the biggest falsifier").
5. **The real walk** — one receipted end-to-end run: the keeper-waking generation
   ("Files are the body", maze-keeper:latest, 44.7s cold) rendered and filed.

## Falsification protocol (witness's F1–F5 + seat's F6)

F1 render-fails-to-telemetry (byte-exact walkers, 100%) · F2 flood-shape (event +
ground-state, counts match eval_count; no wavefront claimed) · F3 shadow-catch
(versioned suite cells caught; creative high-entropy prompt NOT marked) · F4
keeper-honesty = 1.0 under the tiered gate · F5 cost/loopback ($0, sanctioned host
service) · F6 proxy-label (zero unlabeled proxy organs). Dispute resolution: any
falsifier failure marks the render DISPUTED in CONVO + fold; the render carries its
dispute label until re-run clean.

## Evaluation metrics (witness's)

Byte-exact render rate · flood/walker count match (eval_count exact) · shadow detection
rate on the suite (with false-positive check on creative prompts) · keeper honesty score
(T1–T3 gate) · cost ($0) · telemetry coverage (share of final-chunk fields rendered).

## Limitations (witness's, preserved — these are the honesty walls)

- Logits observability is coarse: entropy/refusal proxies may be coarse; future work
  could patch ollama or mine OLLAMA_DEBUG logs.
- Attention is not exposed by the API: the lightmap is symbolic rather than
  data-driven.
- The refusal suite must be curated and versioned, or F3 is unfalsifiable.
- Single-process, single-model focus; multi-model residency (13 models) rendered via
  /api/ps + vram_hologram only.
- Keeper voice depth: a file-fed narrator risks interpretive drift; the tiered gate is
  the mitigation, not a guarantee.

## Rocinante substrate-introspection checklist (witness's, ending in a named card)

1. Render the ollama eye (this handoff) — the rehearsal substrate, every signal ours.
2. Freeze the organ interfaces (probe → world-json → surface) so the substrate can swap
   under them.
3. Version the refusal suite + telemetry schema (the render's calibration tiles).
4. Dry-run the LOOK against a synthetic stream (byte-match harness before the real walk).
5. Point the same organs at the Mac Studio's local inference stack on arrival; the
   first render there files as **ROCINANTE_FIRST_WALK**.
6. Hash-chain each walk (flight_recorder) into the trajectory tape — substrate
   biography, not screenshots.
7. The wizard's reason, stated: he built the grammar for walking models before he had a
   model worth walking; when the horse lands, the maze is already waiting.

## References (witness's list, paths verified on disk this fold)

watch/SELF_STEAL_SHADOW_WORK_20260906.md · watch/TESUJI_MAP_5_3FLASH_20260906.md ·
watch/SELF_STEAL_MODEL_CARTOGRAPHY_20260906.md · watch/OLLAMA_EYE_TO_HOST_20260907.md ·
watch/OLLAMA_MAZE_SALON_20260907.md · watch/inbox/ASTRA_PROMPT_OLLAMA_MAZE_20260907.md ·
state/keeper_world/world.json · dashboard/static/{maze_arena,shadow_walk,room_lightmap,
fable_room,keeper_voice,self_hologram,tesuji_map}.html · mag/{tesuji_map,shadow_work,
vram_hologram,overseer,trajectory_paths,flight_recorder,arc_seed}.py
