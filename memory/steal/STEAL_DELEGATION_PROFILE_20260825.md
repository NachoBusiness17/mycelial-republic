# STEAL — DELEGATION PROFILE: the ONE subagent-routing mechanism worth stealing (2026-08-25)

## Trigger
RIB-driven research task: "subagent-router — the ONE subagent-routing mechanism worth stealing across Claude Code/Cursor/agentswarm/OpenAI, mapped to our router.py+dispatch."

## The ONE steal (named, structural)
**The delegation profile** — a named, installable POLICY layer that sits ABOVE the routing algorithm and controls *how aggressively the parent agent delegates* to subagents, decoupled from *which* subagent/backend handles a given task.

Source: `marikarX/subagent-router` (GitHub, fetched 2026-08-25, main branch). The mechanism is documented in `docs/features/delegation_profiles_and_roles.md` and encoded in `src/subagent_router/templates/profiles/{cost-optimization,orchestrator,deep-delegation}/SUBAGENT_ROUTER_INSTRUCTIONS.md` plus the three role templates `src/subagent_router/templates/agents/{explorer,worker,reviewer}.toml`.

### What it is (from the fetched bytes)
The router proxy (`app.py`) is a plain multi-provider HTTP proxy (DeepSeek/Ollama/Groq/OpenAI-compat) with budget caps and fallbacks — that part is NOT novel; our `router.py`+`dispatch.py` already do provider picking, budget gating (`grok_budget_ok`), and fallback (`fallback=ollama`).

The NOVEL part is the **profile** that ships as *standing instructions* to the parent coding agent. It is not a routing table — it is a **delegation policy** with three orthogonal axes:

1. **Parent role** — how much the parent (Codex/GPT-5.5) may do locally. `cost-optimization` = "minimal coordinator, at most one cheap scope/marker scan before delegation, no broad local exploration, stop rather than take over after delegation failure." `orchestrator` = "primary orchestrator keeps architecture/task-decomposition/final-acceptance, delegates only bounded work."

2. **Delegation selection rules** — WHEN to use each subagent role, and crucially WHEN TO SKIP. E.g. `cost-optimization` says: *skip explorer when the workspace is empty / one cheap command identifies the files / the user gave exact files / the task is greenfield.* Reviewer is **gated by risk**, not run after every worker: "Do not always run reviewer after every worker. Reviewer is gated by risk" (concurrency, sockets, auth, payment, data loss, persistence, migrations, security-sensitive).

3. **Parent local-edit limits** — a hard allow/forbid list. `cost-optimization` forbids the parent from logic changes, concurrency fixes, security/performance hardening, new tests, API changes, lifecycle/ownership fixes; if a forbidden edit is needed, delegate to worker; if worker fails twice, stop and report.

### Why it's the ONE worth stealing
Every other subagent-routing mechanism (Claude Code subagents, Cursor composer, agentswarm, OpenAI) answers "which subagent handles this task." The delegation profile answers a DIFFERENT, higher-leverage question: **"how much should the parent do at all, and when should it refuse to do work locally and hand off?"** It converts routing from a per-task classifier into a **standing policy** that is model-agnostic ("do not treat a cheaper parent model as permission for local coding") and that encodes the *refusal* boundary — the parent's own edit limits — which is exactly the "golden rule / ok=False autopilot" gap our router does not yet cover.

## The ONE invariant (testable)
**Delegation is a policy, not a routing table: the parent's local-edit allowance is a named, model-agnostic, hard allow/forbid list that gates whether a task is delegated at all — and the reviewer role is gated by risk, not by completion.**

Testable against our chain/knots:
- **Invariant DELEG-POLICY-1:** For every routed task, the router must emit a `parent_edit_allow` set (allow/forbid) that is a function of the *delegation profile*, NOT of the parent model. Verify: `route(goal, profile="cost-optimization")` returns a `parent_edit_allow` that is identical regardless of `force_provider`/`force_seat` (model-agnostic). A test asserts the allow-set is unchanged when the provider changes.
- **Invariant DELEG-POLICY-2 (risk-gated reviewer):** The reviewer/verifier role is dispatched only when a risk marker is present (concurrency/sockets/auth/payment/data-loss/persistence/migrations/security), never unconditionally after every worker. Verify: a task with no risk marker must NOT route to reviewer; a task with a risk marker MUST. This maps to our `spec_gate`/`patch-verify` skills and the `_SECRET_MARKERS` risk detection already in `router.py`.

## Mapped to our shape (contracts only, no wholesale copy)
Which of OUR surfaces it changes:
- **`mag/router.py`** — add a `profile` field to `route()` and `_route_payload` (schema `route.v2` gains `delegation_profile` + `parent_edit_allow`). The profile is a named policy (cost-optimization / orchestrator / deep-delegation) selected per-goal or per-run, exactly like `force_seat`/`force_provider` today.
- **`mag/dispatch.py`** — the `_classify_job` path already returns (job, tier, seat); extend to also return the delegation profile so the parent's local-edit limits ride the same hop.
- **`mag/coordination.py`** — `DEPTH_ROUTES` gains a `profile` key per depth (scut/simple_code → cost-optimization; heavy_code → orchestrator; plan/overview → orchestrator with reviewer gated by risk).
- **`mag/skills_pack.py` / `_match_skills`** — the risk-gated reviewer maps onto the existing `patch-verify` skill: reviewer is added to skills only when a risk marker is present, mirroring how `patch-verify` is added for fix/patch/refactor goals today.

## Honesty note
- Source is `marikarX/subagent-router` (fetched live from GitHub main, 2026-08-25). All claims above come from the README, `docs/features/delegation_profiles_and_roles.md`, the three profile `SUBAGENT_ROUTER_INSTRUCTIONS.md` files, and the three role `.toml` templates — I read these bytes directly.
- I did NOT verify Claude Code / Cursor / agentswarm / OpenAI's own subagent mechanisms from their source; the steal is grounded in the ONE repo named. If the operator wants cross-vendor grounding, that is a separate fetch.
- The `subagent-router` repo is already listed in `configs/steal_protocol_repos.yaml` (id: subagent-router, mag_slot: deepseek_ollama_routing) and is a source for the priority-1 `routing-economics` research topic — this steal folds into that slot.
