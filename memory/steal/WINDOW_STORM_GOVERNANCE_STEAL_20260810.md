# STEAL — Window-Storm Governance + Control-Room Surface (2026-08-10)
**Scope:** the two themes the window-storm research surfaced that source-attribution alone
doesn't cover. **Self-stole:** `RUNAWAY_SOURCE_TRACE_STEAL` (source attribution), `STEAL.md`
(gated external-op template). **This pack = external sweep for (A) single-controller /
self-replication containment and (B) the control-room / ghost-surface pattern.**

---

## A. Single-controller / self-replication containment
**Problem being solved:** L7 (container power-off exit churn → Docker restart loop) and
L8 (double-supervision → accumulating `autorun_loop`, dashboard starved at ~82% CPU).
Two failure shapes: *an outer restart policy churning a cleanly-exiting unit*, and *two
controllers owning the same loop*.

### A.1 Kubernetes ReplicaSet/Deployment reconcile loop (the model)
**Contract stolen:** the control plane runs a **reconcile loop** — continuously compare
desired state vs observed state and converge; **ONE controller owns each ReplicaSet**.
Desired count = N; if observed < N, create; if > N, delete. Idempotent, eventual-consistency.
**Why it fixes L8:** the anti-double-supervision rule is baked in — ownership is partitioned
by label selector. Two controllers never own the same set.
**Adapt to ours (deterministic):** `guard_registry.reconcile()` *is* this loop (PASS/FAIL →
no-op/reapply). The missing piece is **ownership partitioning**: only ONE process should own
the `autorun` reconcile. Adopt a **leader lock** (see A.4) so even if many modules call
`process_supervisor.status()`, exactly one holder reconciles `autorun`.

### A.2 systemd "hold alive, don't exit" (the L7 fix)
**Contract stolen:** a unit that exits 0 with `Restart=on-failure` does NOT churn; a unit
that stays alive in a `sleep`/`Type=notify` hold is the designed-down state. `KillMode`/
cgroup = kill the whole tree. "Stay alive = idle; exit = churn."
**Why it fixes L7:** matches the fix already applied (mag_launch holds `powered_down`
instead of exiting) — **confirmed correct, external systems do exactly this.**
**Keep + formalize:** the hold-alive state is the K8s/systemd-native pattern. Document it as
the container's designed-down state.

### A.3 Docker restart policy semantics (the outer layer)
**Contract stolen:** `restart: unless-stopped` (start on boot, restart on crash, NOT on
manual stop) vs `on-failure` (only on non-zero exit). The outer policy must be chosen so a
clean exit ≠ respawn churn.
**Adapt:** because mag_launch now holds alive instead of exiting, `unless-stopped` is safe.
Rule: **check the OUTERMOST restart layer whenever an "intentional down" flag doesn't stop
respawn** — the unit's own exit isn't the last word.

### A.4 Leader election (the L8 fix — THE key steal)
**Contract stolen (etcd/consul/`k8s lease`):** a distributed lock — only the holder of the
lease runs a singleton job. Holders renew; on expiry another takes over. Prevents
split-brain (two runtimes doing the same work) when the orchestrator can't reliably know
"is it already running."
**Why it fixes L8 at the root:** the accumulation happened because liveness/state was
unreliable → each caller thought it must spawn. A **lease in `state/` or Redis** makes "one
holder runs autorun" true *even when liveness is wrong*, because a caller that can't take
the lease doesn't spawn.
**Adapt to ours (deterministic, $0):** `mag/flock_scheduler` (the 2026-08-09 flock dedupe)
already gives single-instance semantics via flock — extend it into a **leader lease** for the
`autorun` reconcile: acquire a flock+lease keyed `mag:autorun:leader`; only the holder calls
`autorun_loop`. A stale lease self-expires (age + pid-alive), mirroring the boot-lock pattern.

### A.5 Circuit breaker + bulkhead (the starvation fix)
**Contract stolen (Hystrix/Resilience4j):**
- **Circuit breaker:** after N consecutive failures, open the circuit — stop *calling* the
  failing dependency for a cooldown (fail fast), then half-open to retry. Prevents a broken
  dependency from being hammered forever.
- **Bulkhead/thread-pool isolation:** give each dependency its own bounded pool so one
  slow/hot dependency can't exhaust the shared pool and starve everything else.
**Why it fixes the 82% CPU dashboard:** the dashboard process was doing heavy work while
runaway loops hammered it. Isolation + timeouts mean the dashboard's `/api` handlers run in
their own bounded budget and fail fast instead of hanging.
**Adapt:** wrap the dashboard's heavy home/story reconstruction in a bounded worker/timeout;
if it exceeds budget, return a degraded-but-honest payload (matches "honest empty states").

### A.6 Failure backoff that stops spawning work (supervisord `startretries`→`FATAL`)
**Contract stolen:** supervisord gives up after `startretries` and marks the program
`FATAL` (no more respawn until operator) — versus infinite retry. Already stolen as
`crashLoopBackOff` (cap 300s). **Keep** — but the cap must also gate *spawning work*, not
just respawning the loop, so a broken loop doesn't enqueue a storm of tasks.

---

## B. Control-room / ghost-surface (single-surface operator interface)
**Problem being solved:** the dashboard is the precursor to the ghost surface. Steal how
mature systems present a whole machine on one legible surface.

### B.1 K9s — the terminal control room
**Contract stolen:** one TUI command (`k9s`) gives a pod-centric view of the whole cluster
with drill-down + hotkeys; read is cheap, act is gated. Single surface, not N tabs.
**Adapt:** `/api/v1/ghost/control` ("live view of the whole machine") is the K9s analog.
Ghost surface should be **one pane that reconciles** — everything else is drill-down.

### B.2 Kubernetes Dashboard / systemd-cockpit — "one call sees everything"
**Contract stolen:** a dashboard that summarizes desired-vs-actual for every workload +
health, with honest degraded states; Cockpit gives a web console with the same contract
local/remote.
**Adapt:** the dashboard already does "one call sees everything" (`/api/v1/sovereign`).
Keep the **honest status** (Ship/Verify/Phoenix) — this is the K8s `Conditions`-style
signal (Ready/Progressing/Degraded), which is exactly "source-backed, not invented story."

### B.3 Grafana — question-answering drill-down
**Contract stolen (already in deep-dive):** dashboards answer operator questions; refresh
only as fast as the source changes; drill-down, never dump.
**Adapt:** the "five questions in order" IA maps 1:1. Keep; don't regress to telemetry-dump.

### B.4 Authenticated remote (OpenHands/VS Code remote/Tailscale) — never expose 8765
**Contract stolen:** browser as a lightweight client over an **authenticated tunnel**; the
same control contract local/remote; the management surface is never on a raw LAN port.
**Adapt:** the tablet `control.html` path needs authenticated action envelopes (per
deep-dive). Rule held: **never expose :8765 to LAN/internet** — route via the ghost surface
over an authenticated tunnel (Tailscale-style), not by opening the port.

### B.5 The "operator" pattern (ghost as the controller)
**Contract stolen (K8s operator pattern):** an operator is a custom controller that
reconciles a custom resource to its desired state; the control loop *owns* the boundary.
**Adapt:** the **ghost is our operator** — a reconciler that owns desired state
(`guard_registry`, `restart: unless-stopped` equivalent) and exposes a single control-room
surface. The ghost surface inherits the dashboard's contract and adds reconcile-ownership.

---

## What to steal NOW (prioritized, adapted, deterministic)
1. **Leader lease for `autorun`** (A.4) — fixes L8 double-supervision accumulation at the
   root; extend `flock_scheduler` into a `mag:autorun:leader` lease with expiry.
2. **Bulkhead/timeout on the dashboard** (A.5) — stops the 82%-CPU starvation of `/api`.
3. **Honest degraded payload** (A.6/B.2) — when a subsystem is overloaded, return a
   degraded-but-true status instead of hanging (matches existing "honest empty states").
4. **ghost/control as the single reconciler pane** (B.1/B.5) — one surface that owns the
   boundary; browser/tablet become fallback remotes over an authenticated tunnel.

## Folds
Filed to `memory/steal/`. Register a skill_ledger decision + memory_event
`steal_window_storm_governance` + Verkle witness so it's traceable and not forgotten.
