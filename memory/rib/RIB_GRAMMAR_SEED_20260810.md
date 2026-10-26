# RIB GRAMMAR SEED — v0.1 (2026-08-10) · compilable doctrine, not prose
Schema: rib_grammar.v0.1 · each invariant = { id, predicate, action, anchor } · deterministic

## The grammar
Every invariant is a 4-tuple:
- id:        content-addressed name (verkle/memlang anchor, sha256 of canonical form)
- predicate: the checkable condition the invariant asserts (deterministic, same-input-same-output)
- action:    the enforcement when predicate fails (guard | hook | route | gate | NONE if pure doctrine)
- anchor:    the verkle/memlang pointer the invariant is bound to

## Seed invariants (real, from live sessions — the laws we already run)
1. id: no-window-ever
   predicate: every subprocess spawn carries CREATE_NO_WINDOW (OR-in, stateless via sitecustomize)
   action: guard (guard_registry spawn_sites_no_window + env-level sitecustomize)
   anchor: CREATE_NO_WINDOW / stateless-no-window-sitecustomize

2. id: stateless-by-default
   predicate: no derived/runtime state is trusted as truth; state is recomputed from the chain
   action: guard (deterministic registry = ground truth; config+secrets are the only state)
   anchor: verkle chain / deterministic-meets-stochastic-live-training-data

3. id: deterministic-registry-is-truth
   predicate: the registry/chain is authoritative; stochastic (LLM) output is honed against it
   action: guard (ghost sense_surfaces + verkle roots as honest count)
   anchor: ghost surfaces / verkle-encoding-at-software-level

4. id: cheap-first
   predicate: route to cheapest capable tier unless frontier (grok-gated) is required
   action: route (rightsize / grok_gate)
   anchor: router_policy / grok_rightsize

5. id: engine-owns-truth
   predicate: engine holds state + legal actions; LLM paints only what engine truth allows
   action: gate (game_campaign / legal_actions; illegal move refuses)
   anchor: GAME_THEORY_PLAY_MAP / tabletop-dnd

6. id: riddle-protects-truth
   predicate: deniable/opaque encoding carries true intent without revealing it (riddler)
   action: route (riddler/whisper store; dual reading: public=play, disk=real)
   anchor: riddler protocol / game-interface-riddler-lensing

7. id: operator-is-sovereign
   predicate: the operator holds the veto on every rule; shaping is FOR their interest
   action: gate (operator override [mag] tag; approval for irreversible ops only)
   anchor: routing.md / constitution

## Compiler note
- The grammar must stay DETERMINISTIC (same input -> same output). No stochastic translation in the
  formal core; the LLM may help draft, never execute, the invariant.
- Reuse memlang (tokens), verkle (anchors), guard_registry (enforcement) — no new silo.
- Next: parser -> verkle-anchored IR -> codegen to guard_registry/hooks.
