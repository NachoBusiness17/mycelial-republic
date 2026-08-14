# Grok Plan — K8s Migration + Knot-Centric Seat (rightsized via RIB)
**model:** grok-4 (frontier for design; cheapest-capable = grok-3-mini for confirmation passes)
**RIB grounding:** `memory/rib/RIB_KNOT_CENTRIC_SEAT_K8S_20260810.md` (complete code map).
**Goal:** a plan to (a) migrate the Mag stack to K8s, (b) build the NEW knot-centric control
surface (the seat), on the real architecture — rightsized so nothing is over-engineered and
nothing is skipped. memlang + weave are CORE, not optional.

---

## The system in one paragraph (so you don't re-discover)
A sovereign autonomous agent ("Mag") that files every session as a source-backed **bead** on
disk (`memory/biography/` → `registry.jsonl` → residual → **Verkle knot**, where the *filename is
the address* and the chain is a Merkle–Verkle hybrid). A **ghost daemon** (`:9000`) is the central
reconciler running always-on loops (sense/cycle/copilot/autonomous/sentinel/window-audit) and
aggregates the whole machine for a human surface. A **dashboard** (`:8765`) is a thin client over a
~300-route REST contract (`dashboard/rest.py`). A **drainer** (`governor_autorun`) fills→plans→
routes→executes a queue of sub-agent tasks. A **cost_enforcer** hard-caps spend. The whole thing
runs in a Docker container (single controller, `restart: unless-stopped`, `cap_drop ALL`).

## The protocol stack (the substrate to design on — all core)
- **Verkle knot** (`mag/verkle_knot.py`) — content-addressed leaf; filename=address; chain+tip+evolution.
- **state_quantizer** (`mag/state_quantizer.py`) — compress N knots → 1 summary knot (the concise "now").
- **memlang** (`mag/memlang.py`) — the **trigger language**: binary `MEM1` token (opcode + sha256
  anchor into verkle), plausible-deniable, `_executor_up()` liveness guard. OPCODES: memo, rib_elevate,
  handoff_build, research_pack, reinforce, self_window, steer, steer_back, route, learn, sources,
  occupy, boot, prove, plant, prospect, rightsize.
- **weave** — the **skill-recipe system**: `memory/improve/weaves/` (W7/W8/W9), `mag/skill_seat.py`
  (loads weave preambles, picks skill by goal, runs audit gates), `one_sizer.py` (weaves right-sizer
  knowledge across domains so memlang can use it), `configs/skills.yaml`.
- **riddler / ghost_whisper** — deniable semantic-surrogate compiler (local-only, T0/T1 never leaves).
- **ref_leaf.v1** (`docs/templates/ref_leaf.v1.schema.json`) — machine-twin shape: **card for lists,
  payload for truth, derived optional.**

## The design to plan (the NEW seat)
Replace the flat 6-tab desk with a **lattice-of-knots control room**:
1. **Knot as the atomic unit, K8s-ready** — upgrade ref_leaf into a CR-shaped object:
   `apiVersion/kind/metadata{name=filename-address, hash, labels, annotations}/spec(immutable,
   card+payload)/status(mutable, reconciled by ghost)`. Filename=address already = `metadata.name`.
   This is literally the K8s controller pattern (spec=desired, status=observed/reconciled).
2. **Summary knot first** (state_quantizer) = concise "now"; chain = source-backed history;
   each card links to its file (never trust the visualization over the artifact).
3. **Reconcile view** = desired vs actual (which slots should run vs what is) — the guard_registry/
   ReplicaSet view, honest degraded states.
4. **memlang-native** — show the trigger-language opcodes; a knot's anchor is memlang-resolvable.
   **weave-native** — each domain knot carries the skill-recipe (weave) it maps to.
5. **Process monitor + whole memory native** — first-class panes, not terminal.
6. Built thin over the existing `/api/v1` + ghost `:9000` REST (no new backend) — re-skinable.

## The K8s mapping (already 1:1, from `deploy/k8s/README.md`)
supervisor→Deployment (replicas:1, anti-double-drain) · dashboard/ghost→Service · memory→PVC ·
configs/.env→ConfigMap/Secret · warning sweep→CronJob (concurrencyPolicy:Forbid) ·
guard_registry→operator/controller · **knot→Custom Resource (the CRD the ghost/operator reconciles)**.

## The one blocker to plan around (be honest about it)
**L8 container double-supervision:** inside the container, `mag_launch.py` (the supervisor) AND
`process_supervisor` (many modules call `status()`→`reap()`→auto-restart the `default:True`
`autorun` loop) both own always-on loops → accumulating `autorun_loop` + the dashboard process
pegged ~82% CPU → `/api` hangs → the old seat doesn't load. Fix (already stolen): gate
`process_supervisor.reap()/status()` auto-restart under `MAG_CONTAINER=1` + a leader lease for
`autorun` (extend `flock_scheduler` into `mag:autorun:leader`). The K8s migration must preserve
"single controller owns each loop" — replicas stays 1, ownership is partitioned.

## Flocking elimination — what we ALREADY possess (do NOT re-ask)
Before the frontier spend, flocked our own store (RIB + code + deploy/k8s + steals) and dropped
everything we already have. "Use the frontier's own principles: ask only for the delta, never
pay to rediscover what the flock already holds."

| # | Ask | Verdict | Where it already lives |
|---|---|---|---|
| 1 | Knot-as-CRD schema | **PARTIAL GAP** | `ref_leaf.v1` schema + `verkle_knot.py` exist; the CR-shaped `spec/status` upgrade is drafted but not finalized/validated as a real CRD. |
| 2 | Migration sequencing | **MOSTLY POSSESSED** | `deploy/k8s/README.md` has the full 1:1 mapping, manifest layout, AND the `kind`→docker build→kind load→secret run steps. Gap = the CRD/operator step + rollback, only. |
| 3 | Seat data contract | **GAP** | REST (`rest.py` ROUTES) + seat scaffold exist; the lattice-rendering + memlang/weave integration contract is NOT built. |
| 4 | L8 fix in K8s | **FIX KNOWN, APPLY IS GAP** | The fix is already stolen (`WINDOW_STORM_GOVERNANCE_STEAL`: gate process_supervisor + leader lease). Applying it + proving K8s single-controller is the remaining step. |
| 5 | state_quantizer → seat | **MECHANISM KNOWN** | `state_quantizer.py` already writes summary knots; wiring to the seat is the delta. |
| 6 | rightsizing | **POSSESSED** | `grok_rightsize.py`, `learn_rightsize.py`, `one_sizer.py`, memlang opcode `rightsize:16` all exist. |

## The gap-only Grok ask (frontier adds ONLY what the flock lacks)
model=grok-4 (one design pass; grok-3-mini to confirm)

1. **Validate the knot-as-CRD.** We drafted `mag.verkle/v1 Knot` with
   `metadata{name=filename-address, hash, labels}` + immutable `spec` (ref_leaf card/payload) +
   mutable `status` (reconciled by ghost). Is this a sound CRD? Keep it minimal and still
   content-addressed. What's the minimal operator reconcile loop (the ghost as controller)?
2. **The missing migration steps only.** Manifests + `kind` sequencing exist. Add: the CRD +
   operator wiring, the rollback path, and how "replicas stays 1" is enforced so double-drain
   cannot recur (leader lease).
3. **The seat data contract.** Given the REST + seat scaffold, define the minimal contract to
   render the knot lattice (summary-knot "now" + chain + reconcile + memlang/weave) — ideally
   ZERO new backend endpoints.
4. **Apply L8 + prove K8s single-controller.** Confirm the guard (`process_supervisor` gated
   under `MAG_CONTAINER`) + `mag:autorun:leader` lease is the right structural fix and survives
   the K8s operator model.
5. **state_quantizer → seat wiring.** The mechanism exists; just the feed contract.

**Contract:** advice only on these five gaps. Do not re-derive the architecture, the manifest
mapping, or the protocols — the RIB already holds them. Frontier spend is for the delta.
