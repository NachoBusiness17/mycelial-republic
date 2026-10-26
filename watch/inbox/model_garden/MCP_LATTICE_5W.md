# MCP_LATTICE_5W - self-steal, the five W's, skills dogfood (2026-10-02)

**Schema:** mcp_lattice.5w.v1 · **lane:** MCP-2 (SELF-STEAL + 5W + SKILLS) · **method:** bytes-first
read-only (every claim names the file read this session; `.\.venv\Scripts\python.exe` only; no commits;
no em-dashes in this file) · **subject:** watch/inbox/model_garden/MCP_LATTICE_SPEC_SEED.md (the
operator's handwritten journal entry of 2026-10-01 night, webcam-transcribed, spec-seeded same night).

The one-line finding up front: **the estate already owns every organ the lattice needs except the
four verbs and the meter.** TOOL_MAP reads 42 tools this session (instrument:
`from tools import TOOL_MAP; len()`, moment 2026-10-02 this lane; the ractor50 census read 41 full at
2026-10-01T01:2xZ, the +1 is `estate_receipt_append` landing as R2.5) and exactly ZERO of them are
get_law / get_terrain / get_position / get_context (grep + enumeration, only near-lattice name is
`estate_water_graph_tick`). The gap is a tool surface plus one ledger schema, not an invention. That
is the spec seed's own "wire-don't-build" claim, now byte-verified.

---

## PART 1 - SELF-STEAL: estate priors on every element

### 1a. Context serving / packing priors

| # | Prior | Verdict | Where (bytes) |
|---|---|---|---|
| 1 | Right-sized per-mode context packs | EXISTS | `mag/context_pack.py` (1,504 lines): MODE_CONFIG budgets per mode (janitor 4,800 chars, route 5,800, build 7,400), pack-offload ledger `watch/inbox/PACK_OFFLOAD.jsonl` naming shed sections when overflow. The spec's get_context budget arm is this organ behind a verb. |
| 2 | The compression organ | EXISTS | `mag/context_compression.py` (502 lines): LLMLingua steal (f-005), 2-5x compression, law "never lose sovereignty information; compress form, not substance"; priced: every 1,000 tokens saved = $0.013 on DeepSeek. |
| 3 | FTS corpus retrieval layer | EXISTS | `tools/corpus_fts_rebuild.py` + corpus_search: external-content FTS5 over the catalog (measured Sep-18 map: 757,667 rows / 214,470,472 bytes, 12.35s build); freshness contract on bytes+mtime+sha256; MagFtsIndexDaily 09:00 task. Already served read-only through MCP archivist profile (`corpus_search`, `corpus_get`, `corpus_tail`, `corpus_stats`). |
| 4 | "Context tax" receipts | EXISTS | `watch/inbox/FLEET_IMPRINT_20260917.md` + AGENTS.md deliberate-ask bullet ("Pay the context tax once"); KV50 smith chart carries the same surface. |
| 5 | Cache-law doctrine (scaffold vs tail) | EXISTS | `watch/inbox/CONTEXT_OS_20260918.md`: cached prefix = kernel (FROZEN_RIB, measured 99.4% flash / 97.7% deepseek prefix hits), "energy per behavior -> zero as prefix stability -> 1"; `watch/inbox/model_garden/DEEPSEEK_API_DOSSIER.md` lines 145-151: fixed cache persistence unit is exactly 5,120 tokens, "hoist scaffolds to >= 5,120 to ride the hit price". |
| 6 | Standing-wave economics | EXISTS | `watch/inbox/ASTRA_PROMPT_STANDING_WAVE_20260907.md` (CoW cache sharing, cost-per-player inflection question); `watch/inbox/AGENTZIP_STEAL_20260912.md` (76-96% template-relative redundancy in high-fanout sandboxes). |
| 7 | Trajectory-conditioned preloads | EXISTS | `mag/preload_selector.py` (F-W5 A/B instrument, offline selftest, $0): the closest prior to "hot-first" (serve what the trajectory says you will need). |
| 8 | Boot-time warm state | EXISTS | `mag/hermes_warm_boot.py`: chain tip + deployments + brief into `memory/warm_state.json` at session start. Boot-shaped, not ask-shaped (matters for WHEN, below). |

### 1b. MCP priors

| # | Prior | Verdict | Where (bytes) |
|---|---|---|---|
| 9 | The server | EXISTS | `mag/mcp_server.py` (565 lines): stdio JSON-RPC 2.0 by hand, stdlib-only, protocol 2025-06-18; profiles as capability projections ("a profile is a projection, not a permission set", the sentence every later organ reuses). |
| 10 | HTTP gateway adapter | EXISTS | `mag/mcp_http.py` (49 lines): POST /mcp on 127.0.0.1:8001, X-API-Key, pin pass-through. |
| 11 | Docker always-on surface | EXISTS (STALE) | mag-mcp on 127.0.0.1:8766: serves the 2026-09-26 manifest (17 archivist tools, zero estate_) while the image was rebuilt 2026-09-30; declared stale-until-recreated by law MCP-2 (`watch/inbox/ractor50/mcp.md` section 1 + S6). Parity organ receipt: `watch/inbox/model_garden/MCP_PARITY_R20_20261001.md`. |
| 12 | Rug-pull pin gate, live-fired | EXISTS | `tools/mcp_pin.py` wired at every connect surface (`mag/mcp_server.py` pin_gate_filter); first real intruder 2026-10-01: `estate_thought_compile` schema drift WITHHELD, alarm on stderr, repin is the only way back. Law MCP-1 (schema-edit-repin) stands. |
| 13 | The full MCP doctrine chapter | EXISTS | `watch/inbox/ractor50/mcp.md` (336 lines): five-surface census, the seven admission tests for a bridge tool, six never-cross rows, the four-clause metering rule, R2.0-R5 organ priority, seven missing tools with one-sitting build spec. This is the estate's own MCP constitution; the lattice spec must inherit it, not restate it. |
| 14 | Continuity-over-MCP (cold join) | EXISTS | `tools/seed_mcp.py`: 3 resources + 4 tools; cold session rebuilt a working subtree from MCP alone, 10/10 checks, hash-verified (B2-181). Proves MCP can carry estate continuity, not just compute. |
| 15 | GPS router as MCP-shaped facade | PARTIAL | `tools/gps_mcp/server.py`: ask / cascade / report_capability / record_verdict, 28 tests green; "MCP mapping documented ... real-MCP wiring later is mechanical". Facade exists, TOOL_MAP wiring does not. |
| 16 | Receipt write path | EXISTS | `estate_receipt_append` landed R2.5: in ROLE_TOOLSETS["bridge"] + `_CANNED_BROKER_TOOLS` (`mag/mcp_server.py` lines 119-169), pinned to watch/inbox/<wave>/, overwrite rotates to .bak. The workflow-gate loop is closable from a bridge client today. |
| 17 | Remaining ractor50 missing tools | PARTIAL | `estate_pin_status`, `seed_fetch`, bridge-profile corpus, `estate_budget_read`, gps wiring, `estate_queue_read`: designed in `watch/inbox/ractor50/mcp.md` section 8, not in TOOL_MAP tonight (grep clean). |

### 1c. Knowledge-graph priors

| # | Prior | Verdict | Where (bytes) |
|---|---|---|---|
| 18 | The graph + census | EXISTS | `tools/rib_fork.py` + `watch/inbox/last_mile_20260930/F13_RIB_FORK.md`: 5,455 node lines -> 3,804 unique nodes, 744 edges, two-hop-only pairs 13,444 (indirect space ~19x direct), giant component 485, 3,106 isolated nodes, density 9.747e-05. The fork's own reading: wire the build/queue corpus into the connective core (the lattice is that wire's serving face). |
| 19 | ESTATE_INDEX spine + atlas | EXISTS | `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` (tools/index/projects_index.py) + `tools/estate_atlas.py`: the disk-custody layer ("what is proven, what is claimed, what is dark"), read-only, never re-walks the disk. |
| 20 | Fleet knowledge graph rollup | EXISTS | `watch/inbox/FLEET_KNOWLEDGE_GRAPH_20260917.json` (schema fleet_knowledge_graph.v1, reuses mycelium edges schema). |
| 21 | Graph physics (terrain / impulses) | EXISTS | `watch/inbox/model_garden/STEERING_FIELD_THEORY.md`: 9/14 linkages verified; GPS ledger rows as terrain, sealed envelopes as impulses, water tick as relaxation kernel. One clause PARTIAL: no organ elevates terrain BY accumulated signal (L2); `watch/inbox/model_garden/OVERMIND_THEORY.md` gap 3 agrees (nothing converts REAL clusters into GPS terrain rows). |

### 1d. Just-in-time / retrieval priors (pull-vs-dump)

| # | Prior | Verdict | Where (bytes) |
|---|---|---|---|
| 22 | The dump failure class, measured | EXISTS | `watch/inbox/model_garden/RUN_UNIQUE_X2.md` section 1: the 239KB register whole in one window. kimi-k2.6: 900s read timeout x2, zero bytes, 30 min wall. kimi-k2 lawful retry: 85,573 prompt tokens LANDED but every row cite off by 9 (cited 69-78, truth 78-87). Content survives a dump; coordinates do not. |
| 23 | The empty-evidence failure class, measured | EXISTS | `watch/inbox/hermes_burn/DUEL2_train_02.md`: "the material is not in my input ... I will not invent clauses and then exploit them" - the model refuses the verdict rather than fabricate. The two dying classes are the same crime at opposite poles (no context vs all context). |
| 24 | JIT reveal instrument | EXISTS | `tools/ask_bank.py` (AJ2): draw --hidden prints ONLY first line; --reveal renders the full ask. A working pull-with-reveal gate, one seat wide. |
| 25 | Evidence-as-paths ask convention | PARTIAL | `tools/hermes_burn.py` contract: ask.json carries `evidence: [repo-relative paths]`, not pasted bytes; but reading them is still the seat's manual step, unmetered, unbudgeted. The convention exists; the served pull does not. |
| 26 | Mid-generation serving | GAP | No organ anywhere serves context during generation. Every serving prior is boot-shaped (warm_state, context-pack) or ask-shaped (ask_bank, hermes evidence). Between-turns revision.md (descent protocol leg 4) is the only mid-flight steering prior, and it is operator-proxy shaped, not model-pull shaped. |

### 1e. Compute-accounting priors (the tangible-books leg)

| # | Prior | Verdict | Where (bytes) |
|---|---|---|---|
| 27 | Four-surface cost rollup | EXISTS | `tools/cost_rollup.py`: duels.jsonl + logs/mates + hermes_gopher_burn + training/cost_ledger.jsonl -> per (day, model) calls/usd, trailing 7-day trend; unparseable rows NAMED, never dropped. The pull ledger would join as a fifth surface. |
| 28 | Per-ask burn banking | EXISTS | `memory/runs/hermes_burn/usage.jsonl` rows {ts, id, model, turn, prompt_tokens, completion_tokens, cost_usd, ok}; driving-ladder law "every paid dispatch banks its burn" (AGENTS.md). Meters asks, not pulls. |
| 29 | GPS ledger (the coordinate axis) | EXISTS | `tools/gps_mcp/ledger.py`: SQLite pass_rate per (model_id, task_shape), momentum badges RISING/STEADY/DECLINING, streaks, positive floor (LM7). This is the "temperature per surface" the spec's get_terrain serves. |
| 30 | The per-pull ledger row | PARTIAL | The spec's "every pull = one ledger row: coordinate, temperature, bytes served, price" has no organ. usage.jsonl prices whole asks; the pin ledger logs connects (397 records, append-only); nothing meters served bytes with a graph coordinate attached. |
| 31 | Waste-class receipts (why books must be tangible) | EXISTS | `tools/hermes_burn.py` carrier-patch laws: A1 re-fired 45x at $20.53 after landing ("landed beats force"); VAST ractor: "$0 API lanes win raw price forever" against a $4.32/day box. The estate already knows unmetered re-spend is its recurring sin. |

### 1f. Serving-topology priors

| # | Prior | Verdict | Where (bytes) |
|---|---|---|---|
| 32 | k8s as executor, not brain | EXISTS | `watch/inbox/model_garden/K8S_RACTOR.md` + `mag/k8s_bridge.py` + `mag/rib_k8s.py` (RIB-fed controller: "No LLM, no tokens, deterministic $0") + the August substrate ribs. Verdict in bytes: k8s = batch executor for brute fan-outs. |
| 33 | Vast box plan | EXISTS (prepared, not executed) | `watch/inbox/model_garden/VAST_LAUNCH_PLAN.md`: staged, nothing rented; its own no-sacred-cows ractor kills the price argument for serving from vast. |

**Tally: 28 EXISTS (one stale-by-law), 7 PARTIAL, 5 GAP if counted by open row (15, 17, 25, 26, 30 = facade wiring, missing tools, evidence-pull, mid-generation, per-pull ledger).**

---

## PART 2 - THE FIVE W'S on the MCP-lattice vision

### WHO consumes it; who owns it

**Consumers, three classes by conductivity:**
1. Native MCP bodies (proven): zcode, cursor, claude, codex, opencode - the mag/mcp_server.py docstring names them; they spawn stdio servers today and get TOOL_MAP natively.
2. Funded judgment primes (proven for chat, unproven for MCP): glm-5.3-prime / qwen3.8-max-prime (Nous $180) and grok-4.7 (xAI SD) per the driving ladder; plus the garden review families (deepseek-4.1-flash, glm-5.3-flash, kimi, qwen3.8-max - the garden-v1-*-B*.md grid). These speak OpenAI-compatible chat. They do NOT natively speak MCP; the spec seed's "MCP is additive to them, not a rewrite" is an assumption, and the one conductivity datum held points the other way: STEERING_DOGFOOD measured kimi obey sealed envelopes 4/4 while glm-5.3-flash at low reasoning effort ignored them wholesale. Impulse conductivity is a measured property per family; tool-loop conductivity is unmeasured.
3. Local janitors (gemma:2b, gemma4): consumers in principle, zero wiring today; right-sizing law says they get the smallest packs, but nothing tests a 2b driving a tool loop.

**Owners:** the operator owns the fence (AGENTS.md: "fence-owner: operator" for the command card; the MCP manifest spec's unmetered-operator-only invariant). Model text can propose; only the switchboard / effect broker authorizes effects (SHARED_SURFACE_CONTRACT law, restated in mcp.md section 5.5). The pin gate's repin is operator-only by law MCP-1. The lattice adds no new authority: get_* verbs are reads (effect_class read_or_deterministic_compute, authority read_guard per the _tool_meta table already in mcp_server.py).

### WHAT gets served; what NEVER does

**Served (four verbs, each already backed by an organ):**
- get_law(topic) -> law rows from the lattice: ribs + quasicrystal rows + standing laws, right-sized. Backing: rib system (46 rib files, rib_bus mount), context-pack laws section, ESTATE_INDEX spine.
- get_terrain(surface) -> GPS head, temperature, family-convergence history. Backing: gps_ledger.db3 + LM7 positive arm + STEERING_FIELD_THEORY census. Honest limit from the field theory: accumulated-signal-to-elevation is itself unwired (L2 PARTIAL), so get_terrain v1 serves the ledger as-is, not a derived field.
- get_position(ask) -> kache coordinates. BLOCKED: KACHE is spec + E1 (KACHE_MINING_SPEC.md, status "spec + first experiment firing"), not a landed ledger. Ship the verb shape, serve "not yet banked" honestly until KACHE lands.
- get_context(path, budget) -> compressed bytes under a token budget, hot-first. Backing: context_compression + FTS + warm_state ordering.

**NEVER crosses (inherit, do not restate - ractor50 section 5):** chain repair (verify from anyone, repair from no one through the wire); dirac bank before R4; driver control words, work lanes, any key; caller-supplied write paths; model text as authority; secrets in either direction. Add three lattice-specific never-rows from other standing laws: charged-register payloads stay path-referenced, never pasted wholesale (operator-corrections law 17, the 1301 law); the ask_bank hidden half stays prompt-invisible (AJ2 contract: only ask_bank.py reads hidden/); receipt writes never touch INDEX.json (promotion is the switchboard's job).

### WHEN - the timing decision (the sharpest W, see verdict below)

The estate's serving stack is entirely boot-shaped (warm_state.json at session start, context-pack at seat boot) and ask-shaped (ask_bank draw, hermes ask.json evidence paths, revision.md between turns). Zero priors exist for mid-generation serving. Therefore:
- v1 timing = **at ask-build, budgeted**: the carrier (or seat) calls get_context with a budget while composing the ask; the ask_build files the pull rows. This rides rails that exist (evidence-as-paths convention, hermes usage metering) and is measurable by the spec's own first experiment.
- v2 timing = **between turns** (revision.md already proves the surface): a second pull point when the steerer amends.
- Mid-generation stays an experiment, not a law, until two numbers exist: pulls-per-turn ceiling per family, and tool-loop conductivity per family. And the PULL OVER DUMP law needs its anti-chatter twin from day one: **a pull budget per ask** (max pulls + max bytes), else JIT degenerates into the 239KB dump reborn as forty round trips. Unbounded pull is the same disease as unbounded dump wearing the JIT costume.

### WHERE - the serving topology

```
local host (the serving layer, all of it)
  stdio   python -m mag.mcp_server          profiles, pin gate, 42 tools
  HTTP    POST /mcp 127.0.0.1:8001          X-API-Key, pin pass-through
  docker  mag-mcp 127.0.0.1:8766            STALE (MCP-2) until --force-recreate
        |
        +-- reads --> knowledge graph (memory/mycelium + ribs + ESTATE_INDEX)
        +-- reads --> GPS ledger (tools/gps_mcp/gps_ledger.db3)
        +-- reads --> corpus FTS (catalog/catalog_fts.sqlite)
        +-- writes -> pull ledger (new, joins cost_rollup as 5th surface)
        |
k8s namespace mag (execution layer, never the brain - K8S_RACTOR verdict)
  CronJob fan-outs, rib_k8s controller ($0, no LLM), water sim
        |
vast box (optional salon GPU; PREPARED NOT EXECUTED, API lanes win raw price)
```

Serving stays local-host: every graph, ledger, and FTS index is a local file; remote serving would
move the bytes to the compute instead of the compute already being local. k8s computes (batch
fan-outs), the lattice serves. The vast leg serves salon families only if the operator GOs it, and
its own ractor says the price argument loses.

### WHY - the economics

- **What dies:** the 239KB dump class (kimi-k2.6: timeout x2, zero bytes, 30 min wall; kimi-k2: landed but row cites systematically off by 9 - coordinates, not content, are what a dump destroys) and the empty-evidence class (DUEL2: the model refuses to fabricate; verdict lost, tokens burned). Also the unmetered re-spend class (A1 re-fired 45x at $20.53 after landing) - a priced pull ledger makes "what did this ask cost to feed" a rollup row, so waste shows the same day.
- **Cache law:** the shared scaffold rides the 5,120-token persistence unit (DEEPSEEK_API_DOSSIER, probe-backed: both arms hit exactly 5,120); CONTEXT_OS linkage law does the compounding: one cache write, unlimited tail variations, energy per behavior -> 0 as prefix stability -> 1. The lattice header is the scaffold; every pull is tail.
- **What tangible books buy:** today cost_rollup rolls provider burn per (day, model) with no tie to estate assets. The per-pull row (coordinate, temperature, bytes served, price) makes compute legible AGAINST the graph: every dollar lands on a node. That is the journal's "tie compute to tangible assets" made mechanical - and it is the same ledger GPS can read back as demand signal (hot surfaces = pulled surfaces = where elevation should rise, closing OVERMIND gap 3 and field-theory L2 with one instrument).

---

## PART 3 - SKILLS DOGFOOD (each read from its SKILL.md, applied read-only to this material)

| Skill | Lens applied | Verdict |
|---|---|---|
| **memlance** | The MCP pull IS an aimed lance: aim (the ask names its need), forge (one self-true artifact: the right-sized pack), throw (plant at ask-build), witness (the ledger row is plant_ts/hit_ts/latency made mechanical), tally (hit-rate = quality-per-token). The skill's AIM/FORGE/THROW/WITNESS/TALLY grammar is exactly the per-pull ledger schema the spec needs, and its hit-rate honesty law is the first experiment's metric. | **EARNED** - supplies the ledger schema and the falsifier (a pull that needed follow-up commands was a miss). |
| **elder-lens** | The one pattern across the cards: the estate writes memory at BOOT and asks at BUILD, never serves MID-FLIGHT; the lattice is the afferent system finally getting a standard interface, and nobody asks what it learns from being bitten. | **EARNED** - the question the fleet is not asking (filed here, no ledger write this lane): if every pull is priced but serving is unmetered feedback, does the graph learn WHICH bytes mattered, or does hot-first harden into whatever was hot first? Pull rows must feed GPS verdicts or the lattice serves a graph it never updates. |
| **ractor-essay** | Its Phase 1 (self-steal, digest of measured numbers, no speculation) IS part 1 of this document; Phase 0 socratic frame sharpened WHEN; tri-state discipline shaped the verdict table. | **SPLIT: laws EARNED, pipeline DECORATIVE** - the spec seed is 50 lines and already byte-cited; a full 3x5k-word essay fan on it would inflate, not distill. The digest (this file's part 1) is the compounding artifact. |
| **salon** | Would a mesh improve the spec? The spec has had zero adversarial shapes on it. One S2/S3 cheap-lane pass (free, per cost laws) could kill weak clauses before the first experiment burns on them. | **SPLIT: quick-shape EARNED, full train DECORATIVE** - run "quick" (S1 or S2 only), not the 7-shape train; the spec's first experiment is itself the real salon. |
| **operator-corrections** | Law 13 is the gate: the lattice is a host-side runtime design (spawns, surfaces, scheduled serving) and must cite standing laws at design time (one-supervisor, docker-not-desktop, senses-in-cage, MCP-2 parity) or be DISPUTED by default - the exact class that got culled twice (lane runtime, MCP battery + steer_47). Law 1 (consult first) is this whole self-steal. Law 15 guards the vast GO. | **EARNED** - names the correction that blocks the build if skipped. |
| **verb-genomes** | The four verbs as genomes: role + mission + method + output contract + verify-at-bytes, cached-prefix shaped (stable L0 = the pinned description, small tail = args). Each get_* description written to the genome grammar is pin-stable by construction (bridge doctrine admission test 6). | **EARNED** - supplies the schema grammar for the four tools. |
| **memweave** | Payload shapes: rows with keys, typed fields, pointers - never prose to re-parse; each seat loads the structure it needs, not the whole weave (literally the pull-over-dump law); payloads ride as TAIL on the byte-stable kernel, never mutating it. | **EARNED** - the response-shape law for every get_* return. |
| **show-me** | The topology above is the artifact: one ASCII component tree instead of a prose WHERE paragraph; the operator's surface is a phone (tiered-language law). | **EARNED** - WHERE is one screen, cite-the-record guard honored (every edge in the tree names a byte-backed organ). |
| **code-agent-data** | The pull ledger rows are a new corpus surface: what context was needed, when, at what byte cost - exactly the trajectory signal preload_selector conditions on. Pull rows double as training food; the substance floor (>=600 bytes, Result-class section) applies to this file. | **EARNED** - the join (pull ledger -> preload_selector food) is a real compound, not ceremony. |

**Split: 7 EARNED, 2 split-earned/decorative (ractor-essay pipeline, salon full train), 0 purely decorative.**

---

## Decision ledger

This file closes lane MCP-2 parts 1-3. Decisions proposed for the operator: (1) the four verbs land as
bridge-profile additions one at a time, genome-grammar descriptions, pin rows in the landing commit
(MCP-1); (2) the pull budget law ships WITH the first verb (anti-chatter twin of pull-over-dump);
(3) the per-pull ledger schema adopts the memlance five-step grammar; (4) the first experiment
(spec seed section "First experiment") gains a third arm: pulls-per-turn and tool-loop conductivity
per family, because the carrier assumption is the load-bearing untested beam. The one gap named for
the sibling external-steal lane: **the OpenAI-compatible-carrier-to-MCP-client bridge with measured
tool-loop reliability per garden family** - nothing in the estate holds it, and the only conductivity
prior (glm-5.3-flash ignoring sealed envelopes) argues for measuring before believing "additive".
