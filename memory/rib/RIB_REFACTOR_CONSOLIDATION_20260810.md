# RIB — The Refactor: Consolidate to the Coherent Architecture
**Schema:** rib.refactor_consolidation.v1 · date 2026-08-10
**Operator's thesis:** "this is why we need a refactor."
**Grounded in:** the whole session's findings (window-storm → container → seat → surfaces-as-spec →
solved_surface → flock_steal) + the internals (pro_library case law, RIB, verkle history).

## Why the refactor is needed (what this session surfaced)
1. **Mechanism accumulation.** This session alone added `source_trace`, `guard_registry`,
   `window_audit`, `amd_window_guard`, `flock_steal`, `solved_surface`, the seat — each a real
   capability, but they've accreted as ad-hoc modules instead of one coherent architecture. The
   system's own case law says it: *"ugliness = missing standard pattern; STOP hand-rolling, find
   the named standard."* We've been hand-rolling the standard.
2. **Double-supervision (L8).** Two supervisors owned the loops → the window-storm class. We fixed
   it in the container by gating `process_supervisor`; the refactor makes single-controller
   STRUCTURAL everywhere, not a gate.
3. **Crude-signals drift.** The surfaces (dashboard/home/story/diary) drifted from the internals —
   the seat had to be re-pointed from `/home,/stack` to the current internals (sovereign,
   ghost/control, chain). The surfaces weren't a spec; they were a rough mirror. Surfaces-as-spec
   fixes this: the surface IS the contract.
4. **Seat data is slow.** The aggregation endpoints (sovereign/home) are synchronous and too slow to
   render. The refactor makes the internals serve the surfaces fast (cache/lazy/async) instead of
   the surface waiting on heavy one-call aggregation.
5. **K8s must surface the solved.** The deployment now carries `mag.solved/*` annotations; the
   refactor makes the ghost-as-operator reconcile the knot-CRDs so the solved history is a first-
   class resource, not an annotation.

## The target architecture (the coherent shape — all already exist, must be consolidated)
```
Operator
  │ (sees the SEAT — the ghost surface = castles made real on current internals)
  ▼
SEAT (port/contract — surfaces-as-spec; surfaces define what internals must deliver)
  │  /api/v1 (same-origin; contract-tested)
  ▼
GHOST (the operator/reconciler — daemon :9000, ghost_control harness, reconcile loops)
  │  reconciles desired→actual (guard_registry), leader-lease single-controller
  ▼
SUBSTRATE  verkle (content-addressed memory) · memlang (trigger language) · weave (skills)
           state_quantizer (summary knots = the fast "now") · riddler (deniable external)
  ▲
CONTAINER / K8s  (single controller; replicas:1 anti-double-drain; knot-CRD; PVC; cronjob)
```

## The refactor moves (consolidate, don't rebuild)
1. **One controller.** The ghost is the operator/reconciler. `process_supervisor` becomes an
   observer (already gated); the leader lease makes single-controller true even without a gate.
   Kill the supervisor fight by construction (K8s replicas:1 + operator reconcile).
2. **One surface, one contract.** The SEAT is the port. The surfaces (home/story/diary) become
   contract-tested views over the current internals (sovereign/ghost_control/chain/story/diary).
   Apply surfaces-as-spec: name the castle → declare the port → red (contract test) → green.
3. **One fast substrate feed.** `state_quantizer` summary knots = the seat's "now" (fast, cached);
   `solved_surface` = the solved problems (fast, reads internals); the heavy one-call aggregations
   become cached/lazy so the seat renders immediately.
4. **Consolidate the ad-hoc modules.** `source_trace`/`guard_registry`/`window_audit`/
   `amd_window_guard` → fold into the ghost reconciler's guard set (they're already wired into the
   cycle; make them a single reconcile registry, not scattered probes). `flock_steal` →
   the ghost's knowledge-acquisition loop. `solved_surface` → the ghost's "what's solved" surface.
5. **K8s-native surfacing.** Knot-as-CRD; ghost-as-operator reconciles knots; the deployment
   surfaces the solved (annotations + the operator's CRDs). Surfaces show the solved history, not
   the raw internals.

## Phases (rightsized, cheapest-capable)
- **P1 — make the seat render (fast, high value):** feed the seat from state_quantizer summary +
  solved_surface + ghost/control (all fast); cache the heavy aggregations. The seat becomes the
  working surface. (This unblocks everything downstream.)
- **P2 — consolidate to one reconciler:** fold the ad-hoc guards into the ghost's single guard
  registry; apply the leader lease; kill remaining double-supervision structurally.
- **P3 — surfaces-as-spec:** contract tests per castle (home/story/diary); the seat defines the
  contract; internals fulfill it. No more crude-signal drift.
- **P4 — K8s/operator:** knot-CRD + ghost-as-operator; deployment surfaces solved; migrate to kind.

## What the refactor is NOT
Not a rewrite. Not discarding the castles (they're the spec). Not removing the mechanisms (they're
the capability). It is **consolidation**: one controller, one surface, one substrate feed, one
solved surface — the mechanisms folded into the coherent architecture they were always reaching for.

## Fold
This is the "why" behind the whole session. It should fold as case law (the standard pattern is
the coherent architecture; the refactor is applying it) + seed the K8s migration plan.
