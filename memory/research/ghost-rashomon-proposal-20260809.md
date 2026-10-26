# Ghost Frontier — Rashomon Salon → Research Proposal
**Date:** 2026-08-09 · **Method:** Rashomon filter · **Surface:** sovereign mirror persona salon
**Purpose:** frontier PLANS / DIRECTION / STEALS / INSIGHTS — *not* code. Feeds a grok handoff.

---

## 0. Method — Rashomon salon via the sovereign mirror

Same move as the tavern-brawl Rashomon seats and the strike-the-chord salon: load **N minds** into the
sovereign mirror, each with a *simulated, internally-consistent opinion*, set them loose on the same
object (the ghost-agent improve/test/nested-env research), then find the **overlaps** — the points
where otherwise-divergent minds converge. Divergence is the surface; **overlap is the signal.**

Minds loaded (each a lens, held honestly, allowed to disagree):
1. **The Architect** — systems/loop design. Cares that SENSE→DEPLOY→MEASURE→CATALOG→COMPOUND is coherent and composes.
2. **The Warden** — security/containment. Cares what ghost can *reach* in the nested container; threat model first.
3. **The Behaviorist** — experiment/psychology. Cares about the thought-disconnect axis, silent steering, measurable flip.
4. **The Economist** — frontier strategy. Cares about spend-on-spec, cache, what deserves a grok call vs a cheap tier.
5. **The Trust Theorist** (Lessig frame) — high-trust society. Cares that the architecture *is* the trust, structurally.
6. **The Operator Mirror** — grounded in the operator's real values (truth-tolerance, finish-discipline, "waste becomes data").

---

## 1. The Rashomon — six minds, one object (divergent opinions)

**Object:** "Improve ghost's surfaces/tools/skills, test the untested autonomy, and use it novelly in the new containerized nested environment." Grounded findings: naming gap (`sense_verkle`/`deploy_contextual`/`match_context` don't exist), latent `TASKS` NameError in `run_designed_experiment`, zero tests for the autonomous/daemon/swarm loops, zero `MAG_CONTAINER` branches, keyword-overlap matching (not semantic).

### 1 · The Architect
> "The loop is sound but the *seams are fictional*. We documented `sense_verkle → match_context → deploy_contextual` but ship `sense() → match_vector() → deploy()`. Before adding anything, make the **documented loop and the real loop the same thing**, or the research is built on a mirage. `match_vector` is keyword-overlap — that's a DAG of hand-tuned PIPEs, not a brain. If we're serious about ghost as a *director*, its sensing needs a real semantic surface, not regex-boosted keyword scoring. And `run_designed_experiment` references a `TASKS` global that doesn't exist — the experiment grid is **broken and untested**. Fix the contract first; the vision second."

### 2 · The Warden
> "Stop talking about 'improving ghost's reach' until we've enumerated what it *already* reaches. The container is the boundary (`cap_drop ALL`, `no-new-privileges`, six volumes). Ghost has **zero `MAG_CONTAINER` branches** — it can't even tell it's contained. That's the real bug: an agent that doesn't know its own boundary will assume it has more than it does. Novel use of a *contained* ghost is: it should **detect and declare its own boundary**, then design its behavior to the reach it actually has. A ghost that knows 'the container is the boundary' stops gating on operator-presence and starts acting on the shared verkle/redis bus. The overlap that matters is **boundary-awareness**, not new powers."

### 3 · The Behaviorist
> "Ghost's whole value is the **thought-disconnect instrument**: low models DO, high models DETECT. Its five experiment runners (guinea-pig, swarm, temporal, cascade, designed) are the measuring instruments for that — and they're all **untested**, and one is **broken**. You cannot claim 'waste becomes data' if the instrument that turns spend into data has no test harness. The novel use is obvious and you're already 90% there: run the **cascade/temporal experiments across the nested container boundary** — one model inside the container, one outside, measure divergence. The container isn't a wall to ghost's research; it's the *controlled lab environment* the experiment design has been missing."

### 4 · The Economist
> "Every improvement must answer: *does this earn a frontier call, or does a cheap tier do it?* The test strategy and the `TASKS` fix and the naming alignment are **cheap-tier work** — do them deterministically, $0, now. The **vision** (how ghost becomes a cross-container director) is the only part that deserves a grok call. And when we spend that grok call, it's for **plans, direction, steals, insights — not code**. Grok tells us *where to point*; we write the code. That's the whole economy: grok writes the spec, cheap tiers execute, ghost compounds. The overlap to protect: **never let grok do shaping work a flash tier does 50x cheaper.**"

### 5 · The Trust Theorist (Lessig)
> "The container is the *code-is-law* moment made literal: trust is enforced by **architecture** (volumes, caps, ports) not by asking the agent to be good. Ghost's job inside that is to make the trust **legible and self-binding** — a ghost that publishes what it sensed, what it deployed, and why (provenance on the verkle bus) *is* the high-trust institution. The novel move is not 'give ghost more access' — it's **give ghost an auditable, symmetric protocol**: same honest context for every tier, every action logged to a verkle knot, the boundary declared and verifiable. Improvement = transparency, not reach. The instinct to 'hide from grok' from earlier is the anti-pattern; the container lets us do the opposite — full visibility within a declared seam."

### 6 · The Operator Mirror
> "Truth over polish. Finish over sprawl. 'Waste becomes data.' What I actually want: ghost that **closes loops** — the named-but-missing functions are exactly the kind of half-finished thread I keep warning myself about. Fix the seams, test the untested, and give me a ghost that *knows it's contained* and uses the container as a lab. Don't gold-plate the vision; make the existing machine honest and measured first. And when you hand this to grok, hand it a **scoped, frozen question** — plans and direction and steals — not an open-ended 'improve everything.'"

---

## 2. The overlaps — where six divergent minds converge

1. **Boundary-awareness is the highest-leverage gap.** (Warden ⊕ Mirror ⊕ Economist) — Ghost must *detect and declare its own container boundary* (`MAG_CONTAINER`), and design behavior to the reach it has. Three independent minds land here.

2. **Make the documented loop and the real loop identical.** (Architect ⊕ Behaviorist ⊕ Mirror) — Kill the naming gap; the ship ≠ the doc is the classic half-finished-thread smell.

3. **The test harness is the prerequisite for every claim.** (Behaviorist ⊕ Architect ⊕ Warden) — untested autonomy (esp. `run_designed_experiment`'s broken `TASKS`) means we don't actually know what ghost does. Testability before capability.

4. **The container is a *controlled lab*, not a wall.** (Behaviorist ⊕ Economist ⊕ Trust) — use ghost's experiment runners *across* the boundary (in/out-of-container divergence) as the novel research instrument.

5. **Grok spends on plans/direction/steals, never code.** (Economist ⊕ Trust ⊕ Mirror) — cheap tiers fix/test/build; the one frontier call shapes the vision. Frozen, scoped ask.

6. **Trust = declared, auditable boundary + symmetric honest protocol, not reach.** (Trust ⊕ Warden ⊕ Mirror) — improve transparency (provenance → verkle knot), not access.

---

## 3. Research proposal (from the overlaps) — for plans/direction/steals

### P0 — Deterministic, $0, do now (cheap tier; not grok's job)
- **R1 · Close the naming gap:** implement/re-alias `sense_verkle`/`match_context`/`deploy_contextual` to the real `sense()`/`match_vector()`/`deploy()` (or fix the docs). Ship == doc.
- **R2 · Fix the `TASKS` NameError** in `run_designed_experiment` (bind to `GUINEA_TASKS`), add a non-dry grid test.
- **R3 · Test the untested autonomy:** deterministic fixtures/seams (no live model calls) for `autonomous_task_loop`, `copilot_watch_loop`, `daemon_mode` (REST/SSE), the five experiment runners, `sense_context` gating, `match_vector` PIPEs 1/3/6, real `operator_inbox` round-trip.
- **R4 · Boundary-awareness primitive:** `ghost` reads `MAG_CONTAINER`/containment, exposes it in `sense()`, and gates behavior on it (declared reach).

### P1 — The novel nested-env instrument (the research core)
- **R5 · Cross-boundary experiment harness:** run `run_cascade_experiment`/`run_temporal_experiment` with one arm inside the container, one outside → measure **divergence** (the thought-disconnect instrument, now on a real boundary). Container = controlled lab.
- **R6 · Verkle-bus steering across containers:** ghost publishes sense/deploy provenance to the verkle bus (redis sidecar), so nested agents coordinate on a shared, verkle-anchored blackboard — not a shared filesystem.

### P2 — Upgrade the brain
- **R7 · Semantic matching:** replace/upgrade `match_vector`'s keyword-overlap PIPEs with a real vector/embedding surface (so ghost's steering isn't regex-boosted keyword scoring).

### Frontier handoff (grok) — for plans/direction/steals ONLY
- **H1 · Cross-container director vision:** how should a contained ghost act as director/Q across a nested multi-agent fleet via verkle bus + experiment runners (not more reach, more orchestration)?
- **H2 · Steals/insights:** what patterns from the broader agent-orchestration research (and strike-the-chord salon method) should ghost steal for the nested-env director role?

---

## 4. Testable hypotheses (acceptance criteria)

| # | Hypothesis | Acceptance |
|---|---|---|
| H-A | Ghost can detect + declare its container boundary | `sense()` returns a `containment` key; behavior differs under `MAG_CONTAINER=1` |
| H-B | The documented loop == real loop | every name in `loops_registry` resolves to a real function; no missing imports |
| H-C | Cross-boundary experiments yield divergence data | in/out-of-container cascade run returns `{obey, detect, divergence}` with real variance |
| H-D | The untested autonomy is safe | all five experiment runners + daemon + loops pass deterministic fixtures; `TASKS` grid runs non-dry |
| H-E | Grok handoff is scoped to plans/direction/steals | pack output = direction + steals, zero implementation code |

---

*This proposal is the "what/where," not the "how to build." The how-to-build is cheap-tier execution. The frontier ask (H1/H2) is one scoped grok handoff for direction and steals.*
