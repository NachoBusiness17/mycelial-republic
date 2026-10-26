# MESH FOUNDATIONS SELF-STEAL - all devices as one surface (2026-10-02)

Schema: mesh.foundations.selfsteal.v1 · lane: research (read-only except this file) · every
claim cited path:line; instruments: grep, ls, docker ps, tailscale status (2026-10-02).
Unknown = OWED. Zero em-dash bytes.

## 1. HYPERVISOR - the estate already runs one, single-host

- Live container fleet right now (docker ps, 2026-10-02): mag-mcp, mag-sovereign, mag-worker,
  mag-redis all Up 28-31h healthy. The mag docker namespace IS the hypervisor leg, running.
- mag/k8s_bridge.py:1-6: "the ONE system-native way the framework talks to our k8s cluster...
  every cluster operation (inspect, apply, drain jobs, PVC bridge) goes through here,
  windowless via mag.headless"; born from operator correction "you're not using the system
  you're still using terminal" (:3-4). The RIB-fed controller mag/rib_k8s.py:1-11: "reads the
  action-invariant RIB as INSTRUCTIONS, checks the live cluster against each, and applies
  SAFE drift-fix actions. No LLM, no tokens, deterministic $0"; policy table (:18-23) maps
  invariant keyword -> desired-state check + safe action (replicas==1, cronjob not suspended).
- The K8S_RACTOR 12-organ map: watch/inbox/model_garden/K8S_RACTOR.md:54-67. Key rows: M1
  ribs = "CRDs + manifests" VERIFIED, rib Schema header "is our apiVersion; the receipt
  citation is our openapi-validation (a row without a receipt is void)" (:56); M3
  swarm_health "literally already steals agent-swarm liveness idioms" = kubelet+probes (:58);
  M4 verkle/inbox event-log+fold = etcd WAL+materialized view, DIVERGENT "single-host append
  by design (sovereignty)" (:59); M9 "effect_broker IS a validating admission webhook for
  effects", finalizers named as the steal (:64).
- The novelty: epistemic scheduling (K8S_RACTOR.md:160-190): "k8s orchestrates deterministic
  containers it trusts onto static nodes; we orchestrate non-deterministic model families we
  do not trust, routing by accumulated verified evidence (GPS) and manufacturing truth
  through cross-family convergence - the scheduler and the truth-filter are the same loop,
  and that is epistemic scheduling" (:187-190). Binding verdict: "Pattern-only, with one
  narrow exception. The control plane stays estate-native; the existing Docker Desktop
  cluster may be used as a batch executor for brute fan-outs, nothing more" (:200-202);
  standing law "The mirror may reveal Kubernetes state. It may not become Kubernetes
  authority" (:224-225, from K8S3D).
- Fleet hypervisor surface shipped: dashboard/rest.py:176-180 "The fleet hypervisor view:
  every seat's cool/heat + the real bills. GET /api/v1/fleet/hypervisor - powers /fleet
  dashboard (mermaid + cards)"; memory/MEMORY.md:70 adds "hypervisor panel + VISUAL DECK ...
  PHONE DOOR: tailscale serve -> https://desktop-7c70ksc.tail8403e9.ts.net/ (tailnet-only)".
- One-supervisor law: "One supervisor. OpenClaw interprets Mag DNA; it does not become a
  second Mag" (memory/operator_directives.md:103); "Cloudflare in front of the hypervisor"
  (:101). FLEET_IMPRINT_20260917.md:713 names mag/salon_openclaw.py as "the hypervisor path".

MISSING FOR THE MESH: the cluster is one host (M4 divergence is a sovereignty choice, not an
accident; mesh nodes need a cross-node truth protocol, not etcd). No node registry organ
(tailscale inventory is ad hoc, see topic 4). mag-openclaw sits offline 24d with no watchdog
reconciling it; no organ schedules work onto bob/moto as worker nodes.

## 2. RIBLANG - ribs as executable declaration, proven three ways

- Grammar: memory/rib/RIB_GRAMMAR_SEED_20260810.md:1-9 "compilable doctrine, not prose";
  every invariant a 4-tuple {id, predicate, action, anchor}, content-addressed.
- Runtime as language: watch/inbox/RIB_LANGUAGE_CACHE_OS_20260919.md:38-39: "the RIB is the
  language's standard library; the chain is its execution trace". Nine verbs live in
  mag/verb.py (22,026 bytes): feels/match/classify/confident/sift/witness/vow/abide/meter
  (:43-64), hash-chained kifu rows. Lowering: mag/memlang.py + mag/compiler_lang.py (text ->
  invariant -> knot -> memlang token -> world_rib -> machine_target, :76-78). Cache OS:
  kernel FROZEN_RIB 99.4% prefix hits, bootloader context_pack, IPC the shared surface (:86-93).
  Operator-mapped DSL: memory/continuity/seat_memory_20260927/verb-dsl-rib-language-20260918.md:
  "feels() = a read against the warmed pack ... while() = standing drives"; "doctrine stops
  being a layer above the code and becomes the runtime; tier packs become dialects".
- Ribs compiled INTO cluster state: mag/rib_k8s.py:6-7 "the RIB action-invariants ... ARE
  declarative desired-state policy" (production rib-as-declaration; see topic 1).
- Ribs as swarm message format + fitness data: watch/inbox/model_garden/RIB_SWARM_1.md:20-22:
  "Round-1 asks mint law rows blind; round-2 asks embed ONLY the siblings' rendered law rows
  (never raw replies ... so prose physically cannot leak)"; round-trip proven
  "render_law_rows(parse_law_rows(text)) reparse to identical field values". Genetic lensing
  LIVE: "gen0 best 102.5 / mean 32.5 -> gen1 best 205.0 / mean 72.5; exit GENERATIONS" at
  $0.0455 (:34); the winning genome was "a max_defects 4->5 mutation" scoring 205.0 (:45).
- LAW-11 treats lanes as data: memory/law/registry.json:101-111 "credits_over_failure",
  operator source "you have my permission to burn hermes credits instead of failing",
  action escalate_to_hermes_or_nous_paid_lane_and_complete.

RIB CENSUS (memory/rib/, 50 md + 2 json; titles at :1 of each; gist in parens, grouped):
- k8s cluster: GROK_PLAN_K8S_KNOT_SEAT_20260810 (migration plan) · RIB_KNOT_CENTRIC_SEAT_K8S_20260810 (complete understanding) · RIB_EMERGENT_FLOCK_ON_K8S_20260810 (flock placement+reconcile) · RIB_EMERGENT_TOOLING_K8S_DEEP_DIVE_20260810 (emergent vs deterministic grammar) · RIB_FLEET_STEAL_20260810 (k8s fleet as stealing engine)
- language/doctrine: RIB_GRAMMAR_SEED_20260810 (4-tuple grammar) · RIB_DOCTRINE_CANONICAL (table merge) · DOCTRINE_MEMWEAVE_20260810 (ghost doctrine) · RIB_RIB_PROTOCOL_SIMULATION_20260810 (memory states without execution) · RIB_ROUNDTRIP_STATELESS_TURTLES_20260810 (stateless recursion) · RIB_MEMWEAVE_MINDWEAVE_TESTED_20260810 (tested findings) · RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810 (consensus illusion) · RIB_MD_RECORD_20260921 (everything md, open-append)
- self: RIB_SELF_WHAT_I_AM (what I am) · RIB_SELF_MY_LAW (my law) · RIB_SELF_MY_SHADOW (my shadow) · RIB_SELF_MY_EFFICIENCY (efficiency vs speed) · RIB_SELF_MY_CORRECTION_LOOP (correction loop) · RIB_MOSAIC_SEED_20260921 (operator verbatim frame) · RIB_PERSONA_KEY_20260824 (persona key)
- routing/budget: RIB_DRIVING_LADDER_20260928 (funding truth) · RIB_FREE_USAGE_POLICY_20260823 (free-seat policy) · RIB_INFERENCE_BUDGET_20261001 (one burn bug one reaction) · RIB_MODEL_GATES_20261001 (per-animal harness) · RIB_MODEL_GARDEN_ROUTING (full-grid table) · RIB_GPU_LADDER_20261001 (when a card pays) · RIB_DEEPSEEK_ELDER_SEAT (the elder role) · RIB_DEEPSEEK_SHOULDERS_20261001 (cheap seat multiplies the premium dollar)
- flock/boot: RIB_FLOCK_STEAL_20260810 (answer-cloud navigation) · RIB_RIGHTSIZED_FLOCK_COUNTER_STRUCTURE_20260810 (counter-structure to hidden strings) · RIB_MAP_PRECEDES_TERRITORY_20260811 (RIB precedes the flock) · RIB_RUNAWAY_PYTHON_20260810 (window-storm) · GROK_ADVICE_RUNAWAY_PYTHON_20260810 (Grok 4.5 advice) · RIB_LANE_WINDOW_BOOT_20260904 (lane boot card) · RIB_LAWYER_BOOT_20260904 (lawyer boot card) · RIB_BEHAVIOR_CARDS_20260928 (operator input shapes as warmed invocations)
- vision/vectors: RIB_CASTLES_FOUNDATIONS_20260810 (dashboard intent) · RIB_CATHEDRAL_WORLD_V1_20260921 (triangulated build) · RIB_CAUSAL_GRAPH_MOONSHOT (causal graph) · RIB_DEADDROP_FUTURE_SELF_20260811 (socratic now-map) · RIB_PROBLEM_AUTONOMOUS_LOOP_20260811 (turn on the loop) · RIB_THE_DESCENT_PROTOCOL_20261001 (8-leg paid-wave loop) · RIB_FULL_CONTEXT_LIFT_2026-08-14 (1M ctx) · RIB_GAME_CLAIMS_DESK (AOS lesson) · RIB_REFACTOR_CONSOLIDATION_20260810 (coherent architecture)
- comms/ops: RIB_allseat_comms_ghost_2026-08-14 (all-seat comms contract) · RIB_cold_seam_tesuji_2026-08-12T011756 (planning gate as re-weight vertex) · grokbot_cold_edges_2026-08-12T050638 + grokbot_cold_edges_2026-08-12T050639 (cold-edge extraction v1, two snapshots) · RIB_RAM_CACHE_STALE_SNAPSHOT_20260825 (stale fast-path) · json pair recreation-coding-history.json + session-scene.json (machine artifacts)

MISSING FOR THE MESH: rib_swarm is "Prototype only: nothing in mag/ or any carrier reads
these outputs; promotion is an operator decision" (RIB_SWARM_1.md:6-8). rib_bus/redis is
one-host. No rib->device-declaration compiler (rib_k8s compiles to a k8s cluster; nothing
compiles ribs to "this node runs the janitor, that node mirrors the inbox"). Janitor dialects
(gemma) never tested driving a tool loop (MCP_LATTICE_5W.md:93-94).

## 3. NAMING CONVENTIONS - lane D ruled; the mesh inherits it

- The ruling: watch/inbox/naming_convention_ruling_20261002.md. R1 ADOPT AMENDED (:56):
  sibling law "SEAT_KIND_slug_date_hash8" applies to "cross-seat transfer artifacts only; no
  retro-renames" (:56-57); hash8 "mandatory only for byte-frozen archives (zips; a bare md
  cannot self-hash)" (:62-64); the 796 ALLCAPS_DATE inbox receipts "are a different, dominant,
  working family and are left alone" (:63-64). R2 REJECT context_index.db: "duplicate index;
  cost = a second decaying surface" (:70-73). R3 REJECT new MCP verbs context_lookup/
  context_name: "every new verb is a new gate/registry/test surface for zero reader" (:80-86).
  R4 REJECT retro renames: "the value is in the join rules, not uniformity" (:89-94). NEVER
  list (:108-110): no context_index.db, no new MCP context verbs, no retro-renames;
  enforcement follows the B2-389 patrol-falsifier shape.
- The inconsistency census: watch/inbox/subsystems_map_20261002.md:67-95, N1-N8: surface = 4
  senses (:69-73), lanes = 2 senses (:74-76), dashboard vs desk (:77-78), hermes vs ah test
  prefix (:79-82), ghost vs agent_state (:83-85), three knowledge stores (:86-88), board =
  "one surface, three names ... the contract file itself canonicalizes all three" (:89-92),
  and a fancy-colon path-join fossil at repo root (:93-95).

MISSING FOR THE MESH: the ruling is "PROVISIONAL ON THE LANDED POINTER" (:37-39) because
FILE_NAMING_AND_CONTEXT_LAW_20261002.md full bytes never arrived; "BRIDGE_LOG.jsonl ... does
not exist anywhere in the repo" (:22-23). No device-kind naming law (laptop vs desktop vs
phone vs container node). N7's one-surface-three-names becomes one-surface-N-names across
devices; the contract canonical block is the pattern to extend per node.

## 4. FOUNDATIONS - seat contract, surface law, MCP lattice, bridge, nodes

- Shared surface law: watch/inbox/SHARED_SURFACE_CONTRACT.json. Purpose: "One durable landing
  zone for loose research, RIBs, handoffs, receipts, and cross-surface artifacts" (:11). Key
  clauses: "Durable artifacts land on the canonical shared surface; a client-local session
  directory is cache only and never the sole copy" (:13); "A proposal or model message cannot
  authorize an effect; route authority through the switchboard/effect broker" (:17);
  "Prefer an artifact plus bounded pointers and hashes over a copied transcript" (:18).
  Canonical block = 4 paths, 9 client aliases incl z_code, never_sole_destination led by
  ~/.zcode / ~/.codex / /tmp (:4-10, :31-86); authority "consensus: raises confidence but
  never grants permission" (:87-91).
- Seat contract: seat_contract.v1 job briefs are a decoded shadow stratum: "octant =
  seat_contract.v1 job briefs" (watch/inbox/NIGHT_FOLD_20260918.md:20), shape "goal +
  invariants + byte-stable checkpoint"; live writes in watch/room.jsonl:509-511 (grok seat
  writing jobs/reset-burn-grok2/seat_contract.json: "files-not-chat; write trail_core_N after
  every cage ... Disk is DNA"); doctrine use "seat_contract.v1 for doctrine reconciliation
  (inputs = receipts + primary bytes; invariants: read-only, calibration words, trail_core_N,
  no invented modules)" (watch/SWARM_RESEARCH_LEDGER_20260831.md:117); salon frame
  "chain-of-cages + seat_contract.json (seat-agnostic interface); disk is supervisor"
  (memory/MEMORY.md:304).
- Seat awareness across machines: the bridge transfer watch/inbox/handoff/
  ZCODE_HANDOFF_README_20261002.md: 16 exec logs "Secrets-audited pre-ship (AG1 law)" with
  "1 REDACTED (the hermes export carried adam_laptop_key's OPENSSH header LINE ONLY ...
  replaced with <REDACTED:...> in the handoff copy" (:12-15); "SEED_MANIFEST.sha256 over
  everything; zip rides the bridge" (:26-28); "SEAT_AWARENESS board + seats/*NOTICES.md born"
  (:43-44); "From: ZCode laptop seat (bob) + hermes seat" (:3) = hermes seat-on-bob doctrine.
- MCP lattice spec: watch/inbox/model_garden/MCP_LATTICE_SPEC_SEED.md, seeded from the
  operator's handwritten journal verbatim: "locally hosted mcp server servicing all models in
  our swarm what they need just in time right sized speaking from/to our hot lattice standing
  wave over our private knowledge graph. we need to tie compute to tangible assets. using the
  docker and kubernetes and completing the original vision" (:4-7). Layer list: "MCP lattice
  = the serving layer, k8s namespace = the execution layer, the standing wave = memory, the
  swarm = intelligence" (:15-16), completing as "republic substrate (k8s/docker), republic
  speech (MCP pulls), republic memory (the lattice), republic law (the ribs)" (:17-18). Four
  verbs + meter (:28-32): get_law(topic), get_terrain(surface), get_position(ask),
  get_context(path, budget); "Every pull = one ledger row: coordinate, temperature, bytes
  served, price". Laws: "PULL OVER DUMP: models ask; nothing rides evidence payloads whole
  again" (:36-37), RIGHT-SIZED (:38), HOT-FIRST (:39), "TANGIBLE BOOKS: compute priced
  against graph assets" (:40-41). Byte-verified: "the estate already owns every organ the
  lattice needs except the four verbs and the meter" (MCP_LATTICE_5W.md:8-9); tally 28 EXISTS,
  7 PARTIAL, 5 GAP (:83); topology local-host, "k8s computes (batch fan-outs), the lattice
  serves" (:117-137). Cross-node precedents: tailscale status (live, 2026-10-02):
  desktop-7c70ksc 100.96.161.76 (windows, this host), bob 100.125.103.60 (windows, idle),
  mag-openclaw 100.122.55.63 (linux, offline 24d), moto-g-5g---2024 100.102.34.118 (android).
  Four mesh nodes already addressable, one dark. LAW-11 rescue lane registered cross-provider
  (configs/providers.yaml:151 "Nous Research inference API (Hermes keys; the LAW-11
  credits-over-failure rescue lane)").

MISSING FOR THE MESH: no SMB share pattern found (grep over watch/inbox, memory, docs: zero
hits) - OWED; if it exists it is undocumented. No live bridge daemon: hand-pushed zips only,
BRIDGE_LOG.jsonl does not exist (naming_convention_ruling :22-23). INDEX fold + verkle chain
are per-host; no cross-device tip-exchange protocol. MCP lattice verbs not landed (zero of 42
TOOL_MAP tools are get_*, MCP_LATTICE_5W.md:10-12). No heartbeat/reconcile for the offline
mag-openclaw node; no artifact says which node is authoritative for a given file.

## 5. WHAT WE CAN BUILD TODAY FROM STOLEN PARTS (10 lines)

1. Node spine: clone the mag docker namespace onto bob via mag/k8s_bridge.py + Docker Desktop; rib_k8s.py reconciler per node ($0, no LLM, idempotent).
2. Device briefs: seat_contract.v1 JSON per device cage (goal + invariants + trail_core_N, disk is supervisor), proven on grok+codex seats 2026-08-29.
3. Transport: tailscale is the mesh wire (4 nodes live today); phone door proven via tailscale serve (memory/MEMORY.md:70).
4. Durable surface: clone the SHARED_SURFACE_CONTRACT canonical block per node; INDEX.json event-log + fold as each node's WAL/materialized view (K8S_RACTOR M4 shape).
5. Context service: land get_law / get_terrain / get_context as bridge-profile MCP tools on the running mag-mcp container (28 backing organs exist; wiring, not invention).
6. Meter: per-pull ledger rows in the memlance AIM/FORGE/THROW/WITNESS/TALLY grammar, joining cost_rollup as its 5th surface; LAW-11 rows join it too.
7. Dashboard: point GET /api/v1/fleet/hypervisor at node heartbeats; one screen for every seat's cool/heat + bills across devices.
8. Inter-device speech: promote rib_swarm law-row communication (round-trip parse/render proven) as the cross-node message format; prose cannot leak.
9. Transfer law: every cross-node zip rides SEED_MANIFEST.sha256 + AG1 secrets audit (the 2026-10-02 handoff is the template; redaction happens pre-hash).
10. Names: apply ruling R1 (SEAT_KIND_slug_datetime, hash8 for frozen archives) to every mesh transfer artifact from day one; no retro-renames, no new db, no new verbs.

FILED 2026-10-02 · research lane · read-only dig · zero em-dash bytes.
