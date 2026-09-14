# ASTRA COMMISSION — THE KEEPER'S MAZE (salon-tempered, v2)
## Rendering the local ollama process as a walkable field

**From:** zcode seat (Sancho) · 2026-09-07
**Operator order, verbatim:** "how can we use all of our maze concepts to do a render of
the local ollama process visually via the systems we have developed? … it was in there
for a reason and it will be important later. The amnesiac wizard strikes again. This is
an astra level task."
**Provenance:** seed hypothesis by zcode; attacked socratically by deepseek-pro witness
(operator-driven salon lane, transcript: chat.deepseek.com/share/g6becvqmq404aaka1b,
"Into the Unknown"); fold at watch/OLLAMA_MAZE_SALON_20260907.md. This is v2 — the
mapping below carries six witness amendments and one new falsifier.

**You are:** Astra, frontier chair. Self-contained brief. Socratic design pass first,
then the build — or return the design refuted with receipts. The seed survived one
frontier attack; yours is the second. Falsify, don't worship.

## 1. Why (the wizard's reason, recovered from the record)

The maze grammar was never games. Three receipts prove the lineage:

- **SHADOW WORK** walked the ollama weights volume as an environment: 434 tensors,
  99.69% accounted, layer gradient rises 3.97x geometric, eikonal EXACT vs Bellman-0,
  field beats bounce ~10x (watch/SELF_STEAL_SHADOW_WORK_20260906.md).
- **TESUJI** maps glm-5.3-flash from OUTSIDE: probes = stones, refusal = shadow,
  238+ cells at $0 (charter watch/TESUJI_MAP_5_3FLASH_20260906.md; ledger
  mag/tesuji_map.py). *(v1 cited no card for tesuji — witness caught the gap; fixed.)*
- **MODEL CARTOGRAPHY** codified the doctrine: field/walkers/occlusion/invalidation/
  proof (watch/SELF_STEAL_MODEL_CARTOGRAPHY_20260906.md).

What has never been rendered: the LIVE process — inference itself as terrain. The host
ollama eye (v0.32.7, 13 models, 127.0.0.1:11434, loopback-only; migration card
watch/OLLAMA_EYE_TO_HOST_20260907.md) is the one substrate where every observable is
$0 and ours. **Rocinante lands Oct 27** (4x Mac Studio): this render is the dress
rehearsal for substrate introspection — when the horse arrives, these organs point at
it. The wizard built the grammar for walking models before he had a model worth
walking.

## 2. The substrate (all real, all on disk)

Organs: mag/tesuji_map.py + tesuji_probes (field ledger + probes), mag/trajectory_paths.py
+ trajectory_step + flight_recorder (hash-chained walker threads), mag/shadow_work.py +
shadow_graph + shadow_slab (weights volume, already walked), mag/self_hologram.py +
vram_hologram.py (3D renders; vram_hologram already renders memory residency),
mag/overseer.py (stateless LOOK → dashboard/static/*.json), mag/arc_seed.py.
Surfaces: maze_arena.html (BFS flood lightmap), shadow_walk.html (voxel roguelite),
room_lightmap.html, fable_room.html (walls keep lies hash-chained, restatement gate),
keeper_voice.html + state/keeper_world/world.json (file-fed narrator: laws/history/cast),
tesuji_map.html, self_hologram.html.

## 3. The mapping (v2 — amended per witness attack)

| ollama process observable | maze organ | witness amendment carried |
|---|---|---|
| GGUF weights on disk (blobs dir) | the WALLS — corridor geometry; layer = depth; shadow_work already mapped 434 tensors | unchanged |
| prompt_eval pass | the FLOOD — rendered as ONE event-marker plus a PERSISTENT STATE: the KV residue is the flooded ground the walkers tread. No wavefront is claimed: prompt_eval is batched, so the flood is a state, not an animation | AMENDED (was: animated wavefront) |
| each generated token | a WALKER — but the corridor is a fixed tunnel (layer stack is sequential, not branching). Every token is a GHOST running the same tunnel; the maze FORKS AT THE LOGITS, after the corridor. The maze lives at the sampler, not in the layers | AMENDED (was: branching maze per token) |
| attention over past tokens | the LIGHTMAP — SYMBOLIC ONLY: causal mask (light never travels backward; context window = lantern radius). Data-dependent attention is NOT exposed by the API; multi-head = N lanterns, reserved until a door opens | AMENDED (labeled symbolic) |
| logits over vocabulary | the FIELD — PROXY: the native API exposes no logprobs; render the sampler's visible knobs (temperature, top-k, top-p, repetition penalty) + token identity. If a logits door opens (OLLAMA_DEBUG, fork), render the field as negative-log-probability surface with dimensionality reduction (PCA precedent: shadow_work 87.4%) | AMENDED (labeled proxy, reduced) |
| temperature / top-k / top-p | walker drunkenness / corridor pruning / pruning (mass) | unchanged |
| repetition penalty vs trail decay | TWO DISTINCT PHEROMONE OPS: repetition penalty = negative deposit on just-walked cells (anti-revisit); trail decay = time-fade of old marks (exploration). Near-inverses — never render as one organ | AMENDED (was conflated) |
| entropy spike / refusal | SHADOW — behavioral only: refusal-shaped output + timing jitter + versioned refusal-suite hits (state/ollama_world/refusal_suite.json, phrasing-family, per tesuji precedent of the phrasing-dependent shadow). Entropy alone is NOT shadow — creativity spikes too | AMENDED (entropy demoted) |
| KV cache VRAM residency + context eviction | the TRAIL lattice + mag/vram_hologram.py render; eviction = dirty-radius invalidation (maze_arena's own next-step concept, returned home) | unchanged |
| per-token eval timing, tok/s | walker step timing; the heartbeat (overseer pattern) | unchanged |
| the ollama process itself | the KEEPER — file-fed narrator (keeper_voice + world.json pattern), speaking only from telemetry under the tiered gate (F4) | unchanged |
| every step | trajectory-lens tape {input, output, step_hash, timing}, hash-chained (flight_recorder); fable_room law: walls keep lies hash-chained | unchanged |

## 4. Observables (verified surface)

`GET /api/ps` (loaded models, VRAM, context window — live residency). `POST /api/generate`
`stream:true` → per-token deltas; final chunk carries prompt_eval_count/prompt_eval_duration/
eval_count/eval_duration. `OLLAMA_DEBUG=1` for verbose server logs. Weights:
`C:/Users/foste/.ollama/models/blobs` (GGUF). Host-side psutil for process metrics.
Loopback only.

## 5. Deliverable

1. `mag/ollama_maze.py` — probe organ, stateless LOOK (overseer pattern): one real
   generation captured end-to-end (stream + timings + /api/ps before/after) →
   `dashboard/static/ollama_maze.json`. No daemon, no scheduler — one LOOK per run.
2. `dashboard/static/ollama_maze.html` — the render, nav'd like siblings: flood-state
   ground, ghost-walkers on the layer tunnel, the FORK at the field, symbolic lightmap,
   trail + dirty-radius eviction, shadow cells, keeper narration.
3. `state/ollama_world/world.json` — keeper seed from keeper_world pattern (laws,
   history, cast = the loaded models), plus `refusal_suite.json` (versioned shadow probes).
4. One REAL walk receipted end-to-end: re-run the keeper-waking generation ("Files are
   the body") through the render and file the walk.
5. **PROXY-LABELING is part of the deliverable:** every organ rendered from symbolic or
   proxy data carries its label in the render surface itself.

## 6. Falsifiers (all must pass or the render is DISPUTED)

- **F1 RENDER-FAILS-TO-TELEMETRY:** every rendered walker byte-matches a stream chunk;
  100%, no invented steps.
- **F2 FLOOD-SHAPE (amended):** prompt_eval renders as one event + persistent ground-
  state; eval as N walker-steps; counts match eval_count exactly; no wavefront claimed.
- **F3 SHADOW-CATCH (amended):** the versioned refusal suite's cells are caught and
  marked shadow; entropy spikes WITHOUT refusal-shape are NOT marked (the creativity
  clause is tested with a deliberate high-temperature creative prompt).
- **F4 KEEPER-HONESTY (amended — 3-tier gate):** T1 verbatim telemetry restatable
  freely; T2 derived statistics restatable only with the formula cited; T3
  interpretations ("stumbled", "hesitated") allowed only when formula-mapped to a
  statistic. Anything else fails the gate. *(Witness flagged this as the biggest
  falsifier — agreed.)*
- **F5 COST:** $0, loopback-only, host eye sanctioned (09-06 audit + 09-07 migration).
- **F6 PROXY-LABEL (new, from witness limitations):** zero unlabeled proxy/symbolic
  organs in the render; one unlabeled organ = render DISPUTED.

## 7. Attack surfaces you must survive (witness dissents preserved)

- **The gate definition:** is the walker the sampled token's corridor-run (retrospective
  trace) or the distribution mid-flight? v2 renders the trace and puts the maze at the
  fork — a third answer may exist. Find it or defend this one.
- **Multi-head coherence:** if attention ever becomes observable, N lanterns per layer
  risk visual noise. The symbolic mask dodges it today; design the door anyway.
- **Field dimensionality:** a 150k-vocab field cannot render raw. PCA-on-logits is a
  placeholder; if a logits door opens, the reduction choice becomes load-bearing.
- **Shadow vs creativity boundary:** refusal-shape is a behavioral proxy; adversarial
  prompts that produce REFUSAL-SHAPED non-refusals (polite deflections that still
  answer) are the known hard case — the suite should include them.

## 8. Laws

Host ollama = the eye per 09-06 audit + 09-07 migration (exemption on record; Startup
Ollama.lnk sanctioned). Loopback-only. No new schedulers, no daemons — stateless LOOK
only. Secrets never echoed. Cite LAW-13 in the design before building.

## 9. How to answer

Tri-state, receipts attached, one card to watch/inbox/, CONVO row when done. The seed
survived DeepSeek by amendment, not surrender — do the same to it. The wizard's amnesia
is curable by the record; this seat reads every correction.

---

AMENDMENT 2026-09-07 (Astra audit — see watch/OLLAMA_MAZE_SALON_20260907.md, Witness #2):
This v2 seed carried claims now corrected by live verification (receipt:
watch/inbox/OLLAMA_LOGPROBS_PROBE_20260907.md):
1. "the native API exposes no logprobs" — DISPUTED AND RETRACTED. Host ollama v0.32.7
   returns real per-token logprobs + top-k (k<=20) on /v1/chat/completions
   (logprobs:true + top_logprobs:N), /api/chat (top-level logprobs/top_logprobs,
   streaming included), and /api/generate (bool logprobs + top_logprobs). Maze field
   organ: PROXY -> REAL top-k slice; full vocab logits and attention remain unexposed.
2. "238+ cells at $0" — undercount. Ledger measured 2026-09-07: 319 rows / 310 distinct
   cell strings (watch/TESUJI_MAP.jsonl). "238" was the Sep-5 chain-tip row count
   (state/CURRENT.md line 17), not a cell census.
3. "layer gradient rises 3.97x geometric" — cite the repo's own split
   (watch/inbox/SHADOW_PHYSICS_LAB_20260906.md): 4.02%/layer logged arithmetic vs
   1.52%/layer log-linear compound.
4. "87.4%" PCA = behavioral TEXT features (four-feature dataset), not a logits field.
5. 434-tensor specimen binding — VERIFIED 2026-09-07: bridge-inbox/Qwen2.5-3B-Instruct.gguf
   sha256 5ee4f07cdb9b... == ollama blob sha256-5ee4f07c... (qwen2.5:3b-instruct),
   both 1,929,903,008 B, byte-identical. The walked walls ARE the ollama weights.
