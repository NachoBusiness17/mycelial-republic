# PROPOSAL — Sancho tier-lattice row (NOT in apply queue; needs explicit operator yes)

**Status:** PROPOSED. Staged here deliberately OUTSIDE `/patches` (the jail inbox) so no apply run can self-grant it. This is the one fix from the 2026-08-30 self-gap analysis I cannot and will not self-apply.

## What
Register the Sancho seat (OpenClaw orchestrator, agent `main`) in the switchboard tier lattice as **T1 — trusted operator-delegate**.

## Why
Self-gap analysis (2026-08-30): the orchestrator holds spawn/spend/patch-drop/board-write with de facto execution force and no formal row. Avenue-2 bypass test fails *because of* this seat. The switchboard's trust gates were designed for dumb seats; they apply hardest to the smart one.

## Constraints on the row (the point of it)
- T1 receives T0+T1 drops only; **no T3 human-authority claims**; never inherits T0 secrets.
- Patch-drop keeps its operator gate: every `/patches` file stays PROPOSED until the operator's `apply` — the lattice row grants visibility and routing, **not** a new execution channel.
- Spawn/spend remain bounded by the conservation law (DeepSeek + free lanes until 2026-09-02 12:52Z) — policy-as-prose today; migrate to `policy.json` budget gates when policy_engine is live.

## How (after apply, mechanism from the real schema)
The lattice lives in switchboard code (T0–T3 constants) and the seat mesh — not in `configs/agent_fleet/jones.yaml` (verified: roles manifest only). So: after the suite is applied, read `mag/switchboard_v2.py`'s actual peer/seat schema and register via its sanctioned path (mesh registration or its config surface). No invented keys.

## Decision
Operator says yes → enqueue a proper patch or run the v2 registration. Operator says no → this file is the tombstone, and the gap stays documented.
