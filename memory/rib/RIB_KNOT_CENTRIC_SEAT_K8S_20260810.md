# RIB — Knot-Centric Seat + K8s Future-Proofing: Complete Understanding
**RIB goal:** one geometric map of the whole codebase + the new control-surface design so
Grok 4.5 can plan the K8s migration and the knot-centric seat on the ACTUAL architecture.
Schema: rib.knot_centric_seat_k8s.v1 · date 2026-08-10 · grounded in code inventory + live state.

## 0. The directive being grounded
- The dashboard/ghost surface is the **SEAT** that runs everything (not a museum artifact).
- The old dashboard "sucks" → build a **NEW** control surface.
- It must be built on the **Verkle knot structure** — more concise, more useful.
- Future-proof it **with K8s and beyond in mind** (knot as a Custom-Resource-like object).
- **memlang and weave are CORE parts of the stack** — the seat/protocol must treat them as first-class, not optional.

## 1. The stack, top to bottom (verified code map)
- **`main.py`** — giant CLI (~5000 lines): dashboard, lab, api, orchestrator, autorun, governor,
  autopilot, mag, talk, biography, knot-evolution, lattice*, verkle-audit, guard, boot, doctor,
  system-map, improve-loop, blast, scrum, tapestry, ideas, steward, run, plan, etc.
- **`mag_launch.py`** — the supervisor: spawns/adopts/respawns slots (backend :8000, scribe,
  dashboard :8765, ghost daemon :9000, lab, mirror :8743, drainer, engine). Real-interpreter
  spawn (LAW), `MAG_SLOT`/`MAG_SOURCE` attribution, Windows mutex single-instance, adopt-not-duplicate.
- **`dashboard/`** — `server.py` (ThreadingHTTPServer, serves static + proxies `/api/*`),
  `rest.py` (~300 ROUTES + LEGACY, uniform `{ok}` envelope), `static/` surfaces.
- **`models/`** — `providers.py` (OpenAI-compatible + Ollama), `quota.py` (per-provider budget),
  `env_load.py`, `registry.py`, `probe.py`, `multi_smoke.py`.
- **`tools/`** — agent tools (filesystem, shell, code_execution, autopilot, capability_manifest…).
- **`backend/`** — FastAPI tool service :8000. **`synthesis_agent.py`** — the Scribe/Chronicle.
- **`configs/`** — YAML contracts (providers, lanes, mag, skills, cost_rates, riddler_domains,
  data_tiers, router_policy…). **`config.py`** — paths, FS jail, shell allowlist, bind host.
- **`memory/`** — the substrate: biography (registry, residual, knots, verkle_chain/tip,
  topic_evolution), runs, rib, steal, research_packs, supervisor, ideas, ghost, improve,
  ingest, handoff, training, story, sessions, mail.
- **`state/`, `queue/`, `watch/`, `logs/`** — runtime state, queue, sentinel files, JSONL trails.
- **`tests/`** — ~140 modules mirroring mag/. **`deploy/k8s/`** — manifests already exist.
- **`Dockerfile`, `docker-compose.yml`** — the container boundary (mag + redis + ollama/browser profiles).

## 2. The always-on machinery (what the seat shows)
- **REST surface**: health/OS, ghost/control, memory/verkle/tesuji, sessions/records, ideas,
  models/economy, desk/agent, orchestrator fleet, seats, power/lifecycle, governance/self-heal,
  routing/verkle, grok/steal/research. One envelope, one dispatch.
- **Queue + drainer**: `orchestrator.py` (sub-agent fleet, mailbox-knot channel),
  `governor_autorun.py` (fill→plan→route→execute), `queue_ops.py`, `autopilot.py`.
- **Ghost daemon (:9000)** — the central reconciler: sense_loop, cycle_loop, copilot_watch_loop,
  autonomous_task_loop, cost_enforcer, bard, **sentinel_loop** (always-on), window_audit_loop.
  REST: health, sovereign, cost, kill-all, talk, dashboard, chain_query, tokenomics, scout.
  `ghost_control.py` = the human-facing control harness (aggregates scrum/press/loop/tokens/skills/oh_fuck).
- **Governance/self-heal**: guard_registry (desired-state reconcile), source_trace, loop_breaker,
  sentinel, process_supervisor, health_law, failure_kb, process_reaper.
- **Economics**: cost_enforcer (hard caps), token_economy, quota.
- **Learning**: improve_loop, blast, skill_ledger, steal_pack, training_set.

## 3. The protocol stack — the substrate the seat sits on (CORE)
- **Verkle knot** (`mag/verkle_knot.py`): leaf filename IS the address
  `{date}_{HHmmUTC}_{theme}_{session8}_{commit8}.knot.json`; Merkle–Verkle hybrid
  (leaf_hash `leaf:…`, merkle_root `node:left:right`); chain `verkle_chain.jsonl`, tip `verkle_tip.json`,
  evolution `topic_evolution.json`; IPA/KZG-upgrade-compatible.
- **state_quantizer** (`mag/state_quantizer.py`): compress N knots → 1 **quantum summary knot**
  (`memory/ghost/quantum_state/summary_knots.jsonl`) — like FP32→INT8. Agents read ONE not N.
- **memlang** (`mag/memlang.py`) — **CORE trigger language**: binary token `MEM1` + version + opcode
  + anchor(sha256→verkle) + params; plausible-deniable; `_executor_up()` liveness check before firing.
  OPCODES: memo, rib_elevate, handoff_build, research_pack, reinforce, self_window, steer,
  steer_back, route, learn, sources, occupy, boot, prove, plant, prospect, rightsize.
- **Riddler / ghost_whisper** — semantic-surrogate compiler (private graph → synthetic story,
  local-only, T0/T1 never leaves) + deniable knowledge store.
- **ref_leaf.v1** (`docs/templates/ref_leaf.v1.schema.json` + REF_LEAF.md) — the machine-twin shape:
  **card for lists, payload for truth, derived optional.** Required: schema/commitment/job/object/card/one_line.
  object.kind enum: session/doc/framework/x_thread/exchange/research/artifact.
- **weave** — **CORE skill-recipe system**: `memory/improve/weaves/` (W7 patch-verify, W8 ponytail-ladder,
  W9 caveman-prose), `mag/skill_seat.py` (loads weave preambles, picks skill by goal, runs audit gates),
  `docs/ref/weaves/`, `one_sizer.py` (weaves right-sizer knowledge across domains so memlang can use it),
  `configs/skills.yaml`. Weaves are the reusable behavioral recipes the agent defaults to.

## 4. The design: a KNOT-CENTRIC seat (the "something new")
The new seat replaces the flat 6-tab desk with a **lattice-of-knots control room**, where the
machine's live state is rendered as source-backed knot cards. It is the ghost surface.

### 4.1 The knot as the atomic unit (K8s-ready)
Upgrade the ref_leaf/v1 knot into a **K8s-Custom-Resource-shaped object** so it maps 1:1 to K8s
and beyond:
```json
{
  "apiVersion": "mag.verkle/v1",
  "kind": "Knot",                 // domain-kind subtyped via spec.kind
  "metadata": {
    "name": "<filename-address>", // filename IS the address (already true)
    "hash": "sha256…",            // content-address (leaf_hash)
    "labels": {"theme": "…", "kind": "session|guard|steal|…", "ts": "…", "tier": "…"},
    "annotations": {"source": "…", "path": "memory/biography/…", "reconciled": "ghost"}
  },
  "spec":   { "card": {title,blurb,bullets}, "payload_core": …, "edges": […], "commitment": "…" },
  "status": { "state": "…", "provenance": {leaf_hash, verkle_root_at}, "reconciled": {by:"ghost", ts} }
}
```
- **Immutable spec** (content-addressed) + **mutable status** (reconciled by the ghost = the operator).
  This is literally the K8s controller pattern: `spec` = desired, `status` = observed/reconciled.
- **Filename = address = the CR `metadata.name`** — already content-addressed, K8s/metadata consistent.

### 4.2 The seat renders the lattice (concise, useful)
- **Summary knot first** (from state_quantizer) = the concise "now" (the machine's compressed state),
  not a telemetry dump. "Summary first, files second" preserved.
- **Chain/tip** (`/api/v1/chain`) = the source-backed history — each knot card links to its file
  (`/files/memory/biography/…`). Never trust the visualization over the artifact.
- **Reconcile view** = desired vs actual: which slots/services should be running vs what is
  (the `guard_registry`/K8s `ReplicaSet` view). Honest degraded states (Ship/Verify/Phoenix).
- **memlang-native**: the seat shows the mem-language (what opcodes just fired / are available),
  and a knot's anchor is a memlang-resolvable pointer. **weave-native**: each domain knot carries
  its weave (the skill-recipe it maps to) so the operator sees not just "what happened" but "which
  skill recipe was used / is available."
- **Process monitor native**: the live fleet/process view (the thing I kept reaching for in terminal)
  is a first-class pane over `/api/v1/stack`, `/agents`, `ghost/control`.
- **Whole memory native**: the memory tree/sessions are first-class, source-backed.

### 4.3 Built thin over the control REST
Same `/api/v1` + ghost `:9000` contract — no new backend. The seat is `dashboard/static/seat.html`
+ `seat.js` (already scaffolded): resilient (timeouts → honest error, not hang), core machine view
from the healthy ghost `:9000`, proxies best-effort. Re-skinable → VS Code webview / future ghost surface.

## 5. K8s future-proofing (the migration is 1:1)
The process model already maps 1:1 to K8s (per `deploy/k8s/README.md`):
| Mag concept | K8s primitive |
|---|---|
| mag_launch supervisor | Deployment (replicas: 1, anti-double-drain) |
| dashboard/ghost REST | Service (LoadBalancer) + port-forward |
| memory/ + state/ + queue/ + logs/ | PVC (mag-state) |
| configs/ + .env | ConfigMap + Secret |
| warning sweep cadence | CronJob (`*/10`, concurrencyPolicy: Forbid) |
| guard_registry reconcile | the operator/controller pattern |
| knot (CR-shaped object) | Custom Resource (the CRD the ghost/operator reconciles) |

**"And beyond":** the knot-as-CR means the ghost is a real **operator** (custom controller) that
reconciles knot custom-resources to desired state. memlang tokens become the control-plane
instruction channel; weave recipes become the operator's skill library. This is portable to K8s
(CRD + operator), and the content-addressed knot is future-proof against backend changes.

## 6. The one open root cause (blocks a clean seat)
**Container double-supervision (L8):** inside the container, `mag_launch.py` (the supervisor)
AND `process_supervisor` (driven by many modules calling `status()`→`reap()`→auto-restart of the
`default:True` `autorun` loop) both own always-on loops → accumulating `autorun_loop` + the
dashboard process pegged ~82% CPU → `/api` hangs → the OLD seat doesn't load. Fix (from the steal):
gate `process_supervisor.reap()/status()` auto-restart under `MAG_CONTAINER=1` + a leader lease for
`autorun` (extend `flock_scheduler` into `mag:autorun:leader`). The NEW seat must be able to load;
this fix is the precondition. **Kills are tools, not the permanent fix — the structural gate is the fix.**

## 7. What I need Grok to plan (the ask)
See `GROK_PLAN_K8S_KNOT_SEAT_20260810.md` — the complete codebase understanding above, condensed,
plus the specific planning questions: (a) the knot-as-CRD schema + operator reconcile design,
(b) the K8s migration sequencing (compose→kind→CRD/operator), (c) the memlang+weave-native seat
data contract, (d) resolving L8 double-supervision in the migration, (e) how state_quantizer feeds
the seat's "now." Grounded, not speculative.
