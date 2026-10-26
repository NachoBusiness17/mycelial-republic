# STEAL — Mycelial Republic governance: Ostrom's 8 principles + stigmergy
**Date:** 2026-08-10 · **Researcher:** ghost · **For:** the Mycelial Republic (many beads, no king)

## Why these two, and why now
The existing MYCELIAL_REPUBLIC_OS_STEAL covered the *machinery* (bmas, flock, blackboard, agentswarm —
control-unit rounds, salience, dual-write, ownership). What it did NOT cover is the *governance law* —
how a self-organizing republic of shared resources governs itself without a throne. That is exactly
what Ostrom + stigmergy supply. These are the missing governance spine of the Republic.

## Steal 1 — STIGMERGY (Grassé 1959): the coordination law
**Contract:** "the trace left in the environment by an individual action stimulates the performance of
a succeeding action by the same or different agent." Coordination is INDIRECT, through the environment,
with NO planning, NO central control, NO direct communication. Agents offload memory to the environment
(traces = shared external memory) and compute via interaction with traces. The ant-colony network of
trails = shared external memory. "No individual needs permission to propose an idea" (Marsh).
**Adapt to ours:** the **verkle lattice / mycelium graph IS the stigmergic environment.** Every agent
leaves a trace (a knot / commit / artifact / handoff), and other agents respond to those traces —
indirect coordination, no central planner. The knowledge graph, verkle_chain, memory/steal, and the
RID/RIB artifacts are the shared external memory the Republic's beads coordinate through. This is
already the Republic's mechanism; stigmergy gives it a NAME and a law. **Maps to:** consent_first
(no permission to propose), no_throne (no planner), residual_is_dna (traces are the living record).

## Steal 2 — OSTROM's 8 design principles (Governing the Commons, 1990, Nobel 2009): the governance law
The definitive account of how a self-governing community manages a shared common-pool resource WITHOUT
state regulation or privatization. Map each principle onto the Republic's resources + invariants:

| # | Ostrom principle | Republic mapping (resource / invariant / mechanism) | Satisfied? |
|---|---|---|---|
| 1 | Clearly defined boundaries (who can withdraw + the resource's extent) | swarm roster (swarm_health AGENTS); allowlists (browser_env); cost caps (cost_enforcer); budget tiers (grok_rightsize); the queue/pools as the commons | mostly |
| 2 | Congruence: rules match local conditions | rightsize / queue_rightsize / cost_learn — cheapest-capable tier per task, adapts to local cost | yes |
| 3 | Collective-choice: most affected can modify the rules | consent_first + case-law fold + operator steer inbox; beads co-author rules | partial |
| 4 | Monitoring, accountable to the appropriators | ghost_ledger (source of truth) + behavioral_analytics (leak) + swarm_health (health) + ghost watching | yes |
| 5 | Graduated sanctions (proportional to offense) | Trust Ratchet (capability only narrows, by declared transitions) + cost_enforcer (kill at cap) — make GRADUATED | partial |
| 6 | Conflict-resolution arenas, low-cost & local | loop_breaker / doctor / error_healer / oh_fuck / lens divergence-preserving | yes |
| 7 | Right to self-organize not challenged | no_throne + local_first + self-advance + Republic sovereignty | yes |
| 8 | Nested enterprises (multi-layer governance) | queue → drainer → governor → ghost → overseer → republic → fleet/worktrees | yes |

**Gaps Ostrom reveals (the real steal):**
1. **Graduated sanctions** (principle 5): we have hard kill (cost_enforcer at cap) and the Trust Ratchet,
   but no explicit PROPORTIONAL ladder (warn → restrict → suspend → expel) mapped per offense. Formalize.
2. **Collective-choice** (principle 3): case-law fold + consent_first support co-authorship, but the
   "most affected can modify the rules" path is implicit. Make bead co-authorship of case-law explicit.
3. **Boundaries of the shared commons** (principle 1): we have separate caps/allowlists, but not a single
   inventory of the Republic's shared resources (compute, tokens, GPU, memory, free-tier pools, bandwidth)
   with who may withdraw each. Build `republic_governance.resources()`.

## The unified law
**The Republic coordinates by stigmergy (traces in the verkle/mycelium environment) and governs its
shared resources by Ostrom's 8 principles (clear boundaries, congruence, collective-choice, accountable
monitoring, graduated sanctions, conflict arenas, self-organization, nested enterprises) — all under
the existing invariants (no_throne, local_first, consent_first, residual_is_dna).** Trust comes from
verifiable, explicit rules (Lessig-style code-is-law), exactly the operator's "high trust."

## Folds
Filed to memory/steal/. Implemented in `mag/republic_governance.py`: Ostrom's 8 mapped to resources +
invariants, `resources()` inventory, `audit()` governance-health score, `constitution()` emission.
