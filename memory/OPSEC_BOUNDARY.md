# OPSEC BOUNDARY — public vs private surface (2026-08-09, operator; Law #9)

The sovereign machinery is PRIVATE. The public face is ONLY the mycelial republic +
our first steps. A public repo must never let a partner/observer infer the swarm
architecture, the deniable-communication layer, or the doctrine.

## 🔒 PRIVATE — never public (the game stays hidden)
Specialized tools + sovereign state + doctrine:
- `mag/ghost*.py` (ghost, ghost_whisper, ghost_talk, ghost_control, ghost_summon,
  ghost_grok_dashboard, ghost_nudge) — the coordinator brain
- `mag/memlang.py`, `mag/verkle_knot.py` — the shared-trigger language + chain
- `mag/riddler.py`, `mag/surrogate.py`, `mag/riddler_transport.py` — deniable communication
- `mag/partner_puppet.py` — the partner puppeteering surface (invariant+shared-history)
- swarm internals: `mag/cheap_swarm.py`, `mag/frontier_ghost`/`grok_terminal.py`,
  `mag/mycelium.py`, `mag/comms_trail.py`, `mag/republic_os.py`, `mag/gpipes.py`,
  `mag/self_drive.py`, `mag/agent_state_router.py`
- `mag/process_supervisor.py`, `mag/loop_breaker.py`, `mag/platform_kill.py`,
  `mag/legacy_audit.py`, `mag/process_reaper.py` — the governance/supervision layer
- doctrine + T0/T1: `CONSTITUTION.md`, `memory/operator_directives.md`, the nudge spec,
  `memory/` state, `state/` (START_BRIEF/HANDOFF/LIVE_REPORT/WHAT_REMAINS), secrets (.env)
- `dashboard/rest.py` FULL route table (the catalog is the architecture dump)

## 🌱 PUBLIC — the mycelial republic + first steps (safe to share)
Only clean, shareable, foundational patterns — nothing that exposes the factory:
- The **mycelial-republic** repo: the constitution-as-practice, fork-equal doctrine,
  the basic scaffold, CONTRIBUTING/README (the public soil, not the machinery)
- First-step framework bones that are generic (patterns, not the sovereign engine):
  e.g. the file-as-truth / deterministic-$0 / measure→fold→learn *principles* stated
  as plain practice, NOT the mag/* implementations
- No ghost, memlang, Riddler, verkle, swarm, or partner internals anywhere in it.

## Test before publishing a file
Would a reasonable reader, given ONLY this file + the public repo, be able to:
1. infer we run a swarm of coordinated cheap agents + a hidden coordinator?  → private
2. reconstruct the deniable-communication / puppeteering layer?            → private
3. see the doctrine / laws / T0-T1 state / secrets?                         → private
4. name our specialized tools (ghost, memlang, Riddler, verkle, partner)?  → private
If ANY is yes → keep it out of the public repo. If it's a generic pattern that
could exist in any clean framework → it may be first-steps material.
