# Lane B — build/attack (cage-note: worker draft)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the likeliest deploy failure is split-brain — v1 swarm_cycle and v2 harness both driving the swarm_worker blackboard — not the missing v2 modules A flagged — SUPPORTED (ls/grep/sed receipts in card, v1 eager-import line cited) · falsifier: the card's own single-ownership test — one harness.run_once() pass with zero v1-schema blackboard writes would break the claim

## Verifying A (all receipts from grep/ls, read-only)
- ✓ `/patches/` is empty; 4 `self_steal_*.json` live in `/patches/applied/`, 18–33KB each, code-bearing. [ls + grep]
- ✓ 4 modules exist in `/mag/mag/`: effect_broker.py, policy_engine.py, switchboard_v2.py, harness.py. [ls]
- ✓ No `swarm_cycle_v2.py` / `ask_router_v2.py` anywhere (only `.mimosa/` hit-noise). [ls + grep]
- ✓ harness.py:34–36, switchboard_v2.py:39 exactly as A quoted. [sed]
- A's "closed graph imports cleanly" is **unsupported at runtime**: A admits no interpreter exists. I only confirm the *eager* load graph is acyclic (eb/pe/sb imports are function-lazy at eb:89, eb:226, sb:456). Reasoned.

## What A got wrong / missed
A's narrative is "2 modules absent → silent dead-import; test file-set completeness." **Dead wrong on the deploy reality.** `/mag/mag/swarm_cycle.py` (the **v1**, not the missing v2) **exists** and at line 109 eagerly imports `effect_broker` + `switchboard_v2`. [sed receipt] So the control surface is NOT missing the cycle layer — a functioning **v1** `swarm_cycle` shares the same `swarm_worker` blackboard (sb:42, eb:107) and switchboard trail. Deploying v2 harness/switchboard over a still-live v1 cycle = **two competing drivers writing one namespace (split-brain / dual-effect-execution)**, not a silent hole. A's inventory test would PASS (v1 present alongside the 4 → set-counts fine) and miss exactly this.

## The single most likely deploy failure
**Split-brain: v1 `swarm_cycle` and v2 `harness` both drive the `swarm_worker` blackboard, double-proposing/double-executing effects.** Missing v2 modules are a red herring; v1 fills the role.

## The ONE test that catches it earliest
A **single-ownership/integrity test**: run `harness.run_once()` once, then assert the `memory/runs/swarm_worker/blackboard` entries in that pass were written by one schema (v2 `harness.queue.v1` → effects) and zero by the v1 cycle path. It fails on the very first pass the moment v1 and v2 both touch the board — earlier and more decisive than A's count-check, which can't see the duplicate driver.
