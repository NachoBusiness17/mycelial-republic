# QUEUE RESILIENCE STEAL — one dead task must not gate the swarm (2026-08-14)

## Trigger
Operator: "steal" — after diagnosing why the swarm wasn't swarming (only Saelis hitting
DeepSeek, `fleet_live_n=1`, grokbot/chatgpt dormant). Root observed: one stuck task at the
queue head (a `[verkle] summarize-session` on **ollama** in a container with no ollama
sidecar → "Connection refused") seemed to shut the whole swarm down. Operator: "so that
shouldn't shut everything down."

## SELF-STEAL (audit our own system first) — THE ACTUAL ROOT CAUSE
- We **already built `mag/orchestrator.drain_parallel()`** (2026-08-12, "the DeepSeek swarm
  speedup") — bounded concurrency (spawn_cap=8, rightsize, cost cap, autorun-pause guard),
  and it only picks **queued** tasks via `_next_queued()` (skips any `running` head).
- **BUT the autorun loop never used it.** `governor_autorun.autorun_once()` called the SERIAL
  `drain_once()`, gated on `if queued_n > 0 and not _any_running_task():`. A stuck "running"
  task makes `_any_running_task()` True forever → **the loop refuses to spawn anything** →
  whole swarm head-of-line blocked. The fix we'd already built was sitting unwired.
- **Fix applied (adaptation):** wired `drain_parallel()` into `autorun_once()` as the drain
  path (falls back gracefully; kept downstream semantics: action label + governor-idle guard).
  Now the swarm fans out real queued work past a stuck running head; the stuck task settles on
  its own timeout/reconcile. Verified: get_errors clean.

## EXTERNAL STEAL (mine/raw/steal_protocol forest — agentswarm, bmas, subagent-router, harness)
Ranked patterns for OUR file/deterministic shape (contracts only, no wholesale copy):
1. **Ready-set scheduling + `blocked`/`skipped` terminal state** — `agentswarm/src/scheduler.ts`
   (`runnableTasks` filters pending+deps-done; `startReadyTasks` dispatch loop; `blockStuckTasks`
   walks to the failing root and marks tasks `blocked` with reason). Never pop-index-0; drain the
   first **runnable-and-reachable** task; retire a dead-provider task from the head with a reason.
2. **Per-provider rolling circuit breaker + backoff + degrade** — `agentswarm/src/breaker.ts`
   (`shouldTrip` = consecutive>=5 or (window filled & rate>0.7); `shouldDegrade` = consecutive>=3
   or rate>0.5; backoff table [2s,5s,15s,30s] in `executor.conductorTurn`). Adapt as a persisted
   `{provider}.breaker.json` the drainer consults before pulling a task; skip tripped providers,
   halve concurrency.
3. **Bounded per-task `attempt` cap** — `agentswarm/src/executor.ts` (`runTaskPipeline` retry loop
   4940–4977 increments `task.attempt` up to max, then `finalizeTask` frees the slot). A task ALWAYS
   settles out of the active set → no infinite head-block.
4. **Health-aware provider scoring + fallback chain + health mutation** — `subagent-router/src/
   subagent_router/app.py` (`provider_score` 644 subtracts consecutive_errors*20; `call_provider`
   727 walks fallback chain and `update_provider_health` bumps consecutive_errors per failure, resets
   on success). Route tasks to reachable providers.
5. **Liveness heartbeat + max-concurrent ceiling** — `bmas/daemon/src/monitoring/health_loop.py`
   (cheap/expensive probe cadence → `healthy|degraded`); `ollama-agent-harness` `HEARTBEAT_MS=60_000`
   + `squad.maxConcurrentAgents` ceiling. Keep named seats; route dispatch only to alive seats.

## Adaptation principle
Every external mechanism reduces to **state + a decision** the drainer already reads: persist
per-provider health + per-task `attempt`/`status` as small JSON records; change "pop head" to
"pick first runnable-and-reachable"; add `blocked`/`skipped` terminal state with a reason. No new
infra, no wholesale copy.

## Applied now
- Wired `drain_parallel()` into the autorun loop (fixes head-of-line block immediately on next
  drainer restart).

## Follow-on (not yet built — from external steal #1/#2/#3/#4)
- Per-provider circuit breaker (`{provider}.breaker.json`) so the drainer **skips** tripped
  providers (e.g. ollama) and settles their tasks as `failed`/`skipped` instead of spawning them
  to fail — prevents a wall of failing ollama spawns.
- Per-task `attempt` cap so a task always settles.
- Seat/provider health records so dispatch routes only to reachable/alive seats.

## Fold
- Repo memory note recorded. (mag.training_events emit + skill_ledger record_decision pending the
  framework surface.)
