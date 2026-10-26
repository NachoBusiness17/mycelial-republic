# K8S_RACTOR - Kubernetes discovered from first principles, the map and the steal

**Schema:** ractor.k8s.v1 · **ts:** 2026-10-01 · **lane:** K8S-1 (ZCode subagent, THE KUBERNETES RACTOR)
**Mission (operator):** "kubernetes this is our entire swarm theory" - the estate's mesh-intelligence
swarm theory is Kubernetes rediscovered. Build the organ-by-organ map, verify each mapping against
estate bytes, steal the decade of solved patterns as tickets, name what has NO k8s analog, and
rule on whether the overmind should be built on literal k8s primitives.
**Sibling input:** OVERMIND_THEORY.md was NOT landed under watch/inbox/model_garden/ at the moment
this lane started (checked by ls, 2026-10-01); this ractor proceeds from the brief. When the theory
lands, the map below is its appendix A.
**Method:** every estate claim below was verified by reading the named file bytes this session; every
k8s claim is cited to the k8s doc page (footer). Web research was used for exact k8s semantics
(backoff timing, GC modes, finalizer flow, PDB behavior, client-go jitter).

## 0. What we already knew (prior k8s contact, mined)

The estate has had THREE k8s contact waves before this lane. None of this map starts from zero.

1. **August 2026 (the substrate doctrine).** `memory/rib/RIB_EMERGENT_FLOCK_ON_K8S_20260810.md`
   ("K8s is the flock's placement + reconcile engine... Job parallelism fans them out, reconcile
   keeps them alive"), `memory/rib/RIB_EMERGENT_TOOLING_K8S_DEEP_DIVE_20260810.md` (the
   elimination + field + reconcile + fold grammar; guard_registry = "desired-state reconcile
   (probe/reapply/backoff)"), `memory/rib/RIB_KNOT_CENTRIC_SEAT_K8S_20260810.md` +
   `memory/rib/GROK_PLAN_K8S_KNOT_SEAT_20260810.md`. A real cluster stood: Docker Desktop node,
   namespace `mag`, a CRD, a `mag-swarm` CronJob with explicit resource requests/limits and
   MAX_PER_PASS bounded draining, a state PVC.
2. **The bridge organs (system-native, still in the tree).** `mag/k8s_bridge.py` ("the ONE
   system-native way the framework talks to our k8s cluster... every cluster operation goes through
   here, windowless"), `mag/gpu_k8s.py` (GPU telemetry read inside cluster pods, folded as verkle
   knots, published on mag:verkle), and the crown jewel `mag/rib_k8s.py`: "the RIB action-invariants
   and the folded doctrine ARE declarative desired-state policy. Our k8s already has the reconciler
   machinery... a RIB-fed controller reads the action-invariant RIB as INSTRUCTIONS, checks the live
   cluster against each, and applies SAFE drift-fix actions. No LLM, no tokens, deterministic $0."
   That rib inverted today's map: it compiled RIBs INTO cluster state. This lane compiles cluster
   patterns BACK into estate organs. Same discovery, both directions.
3. **September 2026 (the simulator + the metaphor).** `tools/k8s_water_sim.py` (2026-09-30, "the
   water_graph as a k8s scheduler simulator... pod, ResourceQuota, per-pod limit, priority ladder,
   load shedding, autoscaler burst-then-drain, escalation/retry, scheduling trace", pinned by
   `tests/test_k8s_water.py`: priority ordering, quota caps, sill shedding, no negative pods,
   no economy leaks) and `watch/inbox/K8S3D_RACK_FIND_20260911.md` (webernetes: real reconciliation
   semantics in-browser; the doctrine line mined from wow.txt: "The mirror may reveal Kubernetes
   state. It may not become Kubernetes authority"). `mag/compute_reconcile.py` already names the
   cluster shape ("swarm queue undrained -> REVIVE the swarm drain (cluster/CronJob)").

So: the estate discovered k8s three times (substrate, bridge, simulator) and each time stopped short
of adopting it as authority. Section 4 rules whether that was right.

## 1. THE MAP, organ by organ

Verdict grammar: VERIFIED = both sides read in bytes/docs this session. PARTIAL = estate side
exists but the mapping is forward-looking or diverges materially. DIVERGENT = the k8s concept
exists but the estate's version deliberately differs (usually better for paid inference).

| # | Estate organ (bytes) | k8s concept (doc) | Verdict | Notes |
|---|---|---|---|---|
| M1 | Ribs/law rows: 52 files under `memory/rib/`, each with a `Schema: rib.<name>.v1` header, receipt-cited rows; compiled to desired-state checks by `mag/rib_k8s.py` (policy table: invariant keyword -> check + safe action); folded/published by `mag/rib_bus.py` | CRDs + manifests: typed declarative objects applied as desired state; controllers reconcile toward them (kubernetes.io concepts/.../kubernetes-objects, "controller pattern") | VERIFIED | `mag/rib_k8s.py` docstring states the identity outright: RIB invariants ARE declarative desired-state policy. The rib `Schema:` header is our apiVersion; the receipt citation is our openapi-validation (a row without a receipt is void). |
| M2 | Overmind glm-flash loop (planned organ, sibling lane; no bytes yet) | controller-manager reconcile loop (observe->act) | PARTIAL | The overmind itself is theory-not-bytes today. The landed reconcile cadences it will generalize: `mag/improve.py` ("Daily improve loop: scout -> candidates -> eval -> promote (gated)", MagImproveDaily 08:00), `mag/swarm_cycle.py` propose->grant->execute, ghost sense/cycle loops. Map is sound; organ pending. |
| M3 | Driver + heartbeat: `mag/afk_cadence.py:124-128` seat_heartbeat pings every seat/lane; `mag/swarm_health.py` probe_agent -> {alive, last_heartbeat, staleness_s, status} + health_law (sick/stale -> restart/sweep/log/improve); `mag/subswarm_health.py` bulkhead + circuit breaker (route_guard skips ISOLATED sub-swarms); `watch/heartbeat.json` via `mag/autorun_status.py` | kubelet + liveness/readiness probes: node agent runs containers, probes health, restarts on failure; readiness gates service traffic | VERIFIED | swarm_health literally already steals agent-swarm liveness idioms (its docstring names applyLiveness/STALE_AFTER, breaker). subswarm_health's circuit-open is our readiness gate. |
| M4 | Verkle / shared inbox: `watch/inbox/index_events.jsonl` append-only log; INDEX.json folded from it (`scripts/index_fold_host.mjs`); living-file seal law in `mag/shared_surface.py`; `mag/verkle_knot.py` hash chain (row_sha256 binds seq+ts+payload+prev_sha256); `mag/verkle_bus.py` Redis pub/sub + fold on every event | etcd: the consensus KV store; every mutation gets a revision; watches stream changes; informer caches are materialized views rebuilt from the log | VERIFIED (with divergence) | The event log + fold IS a WAL + materialized view. Divergence: etcd runs raft consensus for multi-node writes; we are single-host append by design (sovereignty). The fold-repair verb (`mag/shared_surface.py rebuild`) is our cache-resync. |
| M5 | GPS routing: `tools/gps_mcp/router.py` ask()/cascade(): (a) hard constraints filter (max_cost_usd, max_latency_ms), (b) measured pass-rate >= 0.85 from `tools/gps_mcp/ledger.py`, (c) cheapest qualifying wins, ties by tier then id, (d) momentum rank RISING > STEADY > DECLINING, (e) no-history task shapes route to a designated exploration model with exploration:true, (f) every decision emits an append-only JSONL receipt row | kube-scheduler: filter (predicates: resources, taints, affinity) then score (priorities: least-request, spreading); scheduling events auditable | VERIFIED (epistemic variant) | Same two-phase shape. The difference is the score source: kube-scheduler scores static node facts; GPS scores a verdict-evidence ledger the work itself grows. See section 3. |
| M6 | inference_budget per-family recipes: `mag/inference_budget.py` FAMILY_TABLE (10 rows: small/review token floors, thinking_control extra_body, forbidden ask keys, uncap flag, per-animal notes) + plan_call() applied on every fire path | resource requests/limits + node pools + taints/tolerations: per-workload resource envelopes matched to per-node capacity | VERIFIED | The FAMILY_TABLE row is a node-pool profile. forbidden_keys = parameters a family rejects outright (its taints: qwen 400s on any reasoning param). "SENSING ONLY" notes = no-judgment taints. |
| M7 | EMPTY_REASONING / REFUSED terminals: `mag/inference_budget.py` classify_empty()/react()/skip_terminal() (terminal marker minted, same params NEVER refired, two sanctioned recoveries only) + `tools/model_garden.py` REFUSED after 2 refusals per (id, family) with skip-on-sight marker | pod phases + CrashLoopBackOff: Pending/Running/Succeeded/Failed; kubelet restarts with exponential backoff 10s, 20s, 40s ... capped 300s, backoff resets after 10 clean minutes | VERIFIED + DIVERGENT | Divergence is deliberate and better: k8s retries are free, our retries burn dollars, so a burned ask (whole budget on hidden reasoning, empty content) is TERMINAL, not retried. Our missing half is the retryable transport class; that is steal K8S-01. |
| M8 | Swarm width: `tools/code_swarm.py --concurrency` default 10 (SWARM_1: 159 asks, main pass 8m06s, then 2 catch-up passes at width 2/1 for 429s); AGENTS.md fan-out width law (Task width 10 = 109.4M tok/h clean; workflow children capped 3; first rate contact = HOLD, not a width cut); `tools/k8s_water_sim.py` burst siphon = burst-then-drain autoscaler | HPA: replica count driven by observed metrics | PARTIAL | The width knob and the measured envelope exist; nothing closes the loop from live metrics (429 rate, queue depth, tok/h) to width. That is steal K8S-06. The HOLD-on-first-contact law is already a disruption budget in spirit (see M12/K8S-05). |
| M9 | Patrol law: `tools/workflow_gate.py` (no ungated CreateWorkflow; exit-2 blocks; dogfood laws; REGISTRY.jsonl rows), githooks/pre-push (violation ratchet + scenario suite), `tools/census_drift_patrol.py` B2-215 tripwire on the census carrier, `mag/effect_broker.py` (every side effect routed through authority + granted_capabilities + policy TTL/budget/revocation) + `mag/switchboard_v2.py` | admission controllers (validating webhooks reject bad requests at the API boundary) + finalizers (deletion blocked until cleanup conditions are met) | VERIFIED | effect_broker IS a validating admission webhook for effects ("Model text can propose; only the switchboard/effect broker authorizes effects", AGENTS.md). The finalizer half (Done blocked until siblings wired) is steal K8S-03. |
| M10 | Salon mesh: `mag/scale_salon.py` (12 lens lanes + adversarial red-team + architect gopher via research_fanout LANES), `mag/salon_50.py`, `tools/code_swarm.py` stage -> fire -> rollup, workflow_gate law "interagent pass-off (outputs feed later asks)" | Jobs / CronJobs / Argo-style DAG workflows: steps with dependencies, retries, parallelism | VERIFIED | stage->fire->rollup is generate->execute->aggregate over a manifest of work items; the workflow_gate pass-off law is exactly a DAG edge requirement (a step's input must name its upstream's output). |
| M11 | animal_profiles: `tools/animal_profiles.py` observe()/distill() over `memory/behavioral/animals/<slug>.jsonl` (append-only, receipt-cited, fingerprint column: same name + different fingerprint = different animal, no inherited trust) feeding RIB_MODEL_GATES | node capacity/labels/conditions: the scheduler's model of each node | VERIFIED (stronger than k8s) | k8s node identity is stable hardware; model families drift version-to-version with the same name. The fingerprint amendment is a node-identity law k8s never needed. |
| M12 | Budget caps: `tools/code_swarm.py` --cap 2.0 checked against this run's metered ledger rows before EVERY dispatch (overrun skips and names the remainder); hermes_burn/model_garden usage.jsonl meters; effect_broker budget caps | ResourceQuota: per-namespace hard limits enforced at admission time | VERIFIED | Both are check-at-admission against a running total; both skip/reject rather than clamp. |

Count: 12 mappings attempted, 9 VERIFIED, 2 PARTIAL (M2 organ pending bytes, M8 loop unclosed),
1 VERIFIED-with-deliberate-divergence folded into M7's verdict. Zero mappings failed outright.

## 2. THE STEALS - where k8s already solved what we fumble

Each steal is a ticket in the SWARM_1 TICKET_LEDGER row shape. Files named are the change sites.

**K8S-01 backoff-with-jitter for the re-burn class (transport retries).**
k8s solved it twice: kubelet CrashLoopBackOff (exponential 10s, 20s, 40s ... cap 300s, reset after
10 clean minutes; kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle) and client-go's retry
machinery (util/retry DefaultBackoff carries Jitter: 0.1; wait.JitterUntil jitters every period;
the SIG-api-machinery jitter proposal exists precisely because synchronized retries hammer a
recovering system - our 429 storms). Our current state: `tools/code_swarm.py fire()` is one
attempt per ask, and SWARM_1 recovered its 4 glm 429s with HAND-RUN catch-up passes at width 2/1
("conditions changed = lower width, not a same-params refire"). That is a human being the backoff.
Ticket: add a shared transport-retry envelope (exponential base 10s doubling to a cap, jitter
factor 0.1, counter reset after a clean-dispatch window) to the fire path for TRANSPORT-class
failures only (429/5xx/socket). NEVER for EMPTY_REASONING - that class stays terminal (money law).
Change sites: `tools/code_swarm.py` fire(), `tools/model_garden.py` run_ask error return.

**K8S-02 ownerReferences + garbage collection (the wiring-debt orphan disease).**
k8s law: dependents carry ownerReferences; deleting an owner cascades (background), and with
foreground deletion the owner survives in Terminating until its dependents are gone; a dependent
whose owner reference points cross-namespace is treated as ABSENT and gets collected
(kubernetes.io/docs/concepts/architecture/garbage-collection). Our disease, in
`watch/inbox/model_garden/X2_material_wiring_census_frozen.md` words: "a proven fix/organ exists in
ONE surface while sibling surfaces run ungated. Patient zero: thinking-off lived at
tools/ds_workhorse.py:55 while hermes_burn + model_garden ran ungated for months." The census
found rows 1-3+ of exactly this (bounded queues in room.py but unbounded in server.py; MACs on
replies but bare on ticks; atomic writes in some callers, bare appends in others), and
`tools/orphan_census.py` already classes the shared-inbox version (never_registered,
registered_missing, registered_never_consumed). We keep finding orphans by hand because nothing
declares ownership at creation. Ticket: every landed organ/fix/promotion banks an owners manifest
(the sibling surfaces that must adopt it); a standing GC sweep (extend the wiring census into a
tool, e.g. tools/wiring_gc.py) joins landed owners against adoption and reports owner-Done +
dependent-ungated as ORPHAN rows. The cross-namespace-absent rule maps to our scope law: an owner
reference naming a surface outside the manifest's declared scope is absent, not silently forgiven.
Change sites: promotion/receipt writers (workflow_gate, ticket ledger), new sweep tool fed by the
X2 census method.

**K8S-03 finalizers: nothing is Done until siblings are wired (the patrol law EXACTLY).**
k8s law: DELETE on an object with finalizers only sets deletionTimestamp; the object stays
Terminating while controllers do cleanup and remove their keys; empty finalizers + timestamp =
actual deletion; strip a finalizer carelessly and you break the cluster
(kubernetes.io/docs/concepts/overview/working-with-objects/finalizers). Our version: a ticket or
fix marked Done while sibling surfaces are still ungated is an object deleted with finalizers
force-stripped - the exact disease of patient zero. The patrol family
(tools/workflow_gate.py exit-2, tools/census_drift_patrol.py, gate_age_patrol) detects some of
this after the fact; finalizers would make it structurally impossible to close early. Ticket:
PARKED->Done transitions and promotion receipts carry finalizer keys (wiring/<surface> for each
sibling surface named in the owners manifest from K8S-02); the gate refuses Done while any key is
uncleared (exit 2, amend-not-rewrite, same contract as the workflow gate). Change sites:
tools/workflow_gate.py checks, TICKET_LEDGER row shape.

**K8S-04 level-triggered reconcile instead of the imperative driver loop.**
k8s law: controllers are level-triggered - they observe current state, diff against desired, act
on the delta, and are safe to re-run at any cadence; they do not care about the events they
missed (the controller pattern; informer resync re-lists and re-diffs). Our fire path is
edge-triggered imperative with one ad-hoc reconcile primitive bolted on:
`tools/model_garden.py _landed_skip` ("the deliverable-exists truth beats the force flag; only a
pending revision re-fires") is a one-bit diff. code_swarm already has the right shape waiting:
manifest.jsonl IS desired state, raw/ IS observed state, sha_drift_since_ask IS a diff column -
but the only verbs are stage (write desired) and fire (execute all). Ticket: a reconcile verb:
diff manifest vs raw vs terminal markers vs sha drift, fire ONLY the delta (missing, non-terminal,
not sha-drifted), idempotent, safe to run on a cadence. This turns SWARM catch-up passes, family
deaths, and file drift from hand-work into the loop. Change sites: `tools/code_swarm.py` (new
reconcile verb composing _landed_skip + skip_terminal + sha_drift), `mag/improve_loop.py` cadence
to run it.

**K8S-05 pod disruption budgets for the convergence quorum.**
k8s law: a PDB (minAvailable / maxUnavailable on a label selector) makes the Eviction API BLOCK
and RETRY voluntary disruptions that would drop a workload below its floor; a replacement pod
coming up is what unblocks the next eviction; drains without PDBs evict immediately
(kubernetes.io/docs/concepts/workloads/pods/disruptions). Our floor is convergence: SWARM_1 kept
every file at 2-family coverage even after 6 kimi terminals ("those files still carry glm +
deepseek coverage, so no file lost 2-family convergence") - by luck of staging, not by law. The
AGENTS.md width law already encodes the same instinct at account level ("first rate-limit contact
is a HOLD signal, not a width cut"). Ticket: the fire/rollup path enforces a convergence PDB:
min_families_per_file = 2; when a family death or cap eviction would breach it, the wave blocks
(banked, not dropped) until the ask is re-staged on a replacement family. Change sites:
`tools/code_swarm.py` fire()/rollup(), config knob in the run manifest.

**K8S-06 metrics-driven width (close the HPA loop).**
See M8. The width is operator-fixed today; the signals to drive it already bank (usage.jsonl
tokens/cost, 429 counts, wall time per pass). Ticket: width adapts per wave from measured signals
(tok/h trend, 429 rate) inside the envelope table, preserving HOLD-on-first-contact as the
disruption budget. Change sites: `tools/code_swarm.py --concurrency` -> adaptive from ledger.

Ranked: K8S-02/K8S-03 (the wiring-debt disease, one mechanism in two legs), K8S-01 (the re-burn
class), K8S-04 (the diff loop), K8S-05, K8S-06.

## 3. THE NOVELTY - what has no k8s analog and is genuinely ours

Name: **epistemic scheduling** (verdict-weighted scheduling with a convergence quorum).

k8s schedules deterministic containers: a pod either runs or fails observably, node facts are
static hardware facts, and the scheduler's truth is assumed. Three things in our swarm theory have
no k8s counterpart:

1. **The scheduler's view of its "nodes" is itself a contested, learned artifact.** GPS
   (`tools/gps_mcp/router.py` + `ledger.py`) scores model families by measured pass-rate and
   momentum, with every verdict bound to a row_sha256 in a hash-chained evidence ledger
   (`mag/gwap_to_gps.py`: "an auditor holding the evidence hash can re-walk the chain and point at
   the exact row that earned the verdict"). kube-scheduler reads node conditions; GPS reads a
   corpus of verdicts about non-deterministic executors, distilled into animal_profiles that drift
   version-to-version (fingerprint law: no inherited trust). Placement feeds evidence; evidence
   feeds placement.
2. **Executors can succeed-while-wrong; truth is manufactured post-hoc.** k8s has no notion of a
   container that returns 0 while being incorrect. Our truth-filter is cross-family convergence
   (`tools/code_swarm.py converge()`: 2+ families, same line-window, lexical claim overlap = REAL;
   same window different diagnosis = CO-LOCATION, reported, never counted as agreement). The
   quorum is the workload manager, not the executor. This is the organ with zero k8s precedent.
3. **The scheduled resource is reasoning budget against burn pathologies.** ResourceQuota counts
   tokens of compute we trust; our quota guards against families that spend the whole output
   budget on hidden reasoning and deliver an empty content channel (EMPTY_REASONING,
   `mag/inference_budget.py`), a failure mode where the executor reports success-shaped telemetry
   while producing nothing.

One sentence: **k8s orchestrates deterministic containers it trusts onto static nodes; we
orchestrate non-deterministic model families we do not trust, routing by accumulated verified
evidence (GPS) and manufacturing truth through cross-family convergence - the scheduler and the
truth-filter are the same loop, and that is epistemic scheduling.**

Where the theory and k8s genuinely rhyme (worth saying so the novelty claim stays honest): the
GPS cascade (escalate on low confidence, max 3 tiers) rhymes with priority classes + preemption;
the exploration rule (no-history shapes route to a mid-tier model with exploration:true) rhymes
with taints/tolerations for canaries; EMPTY_REASONING rhymes with CrashLoopBackOff only in shape -
our terminal-no-refire law is stricter BECAUSE retries cost money, which k8s never had to consider.

## 4. VERDICT - build the overmind on literal k8s, or pattern-only?

**Pattern-only, with one narrow exception.** The control plane stays estate-native; the existing
Docker Desktop cluster may be used as a batch executor for brute fan-outs, nothing more.

What a k3s/CRD-backed overmind would buy: real watch/reconcile machinery, real backoff, real
quota, kubectl as an operations surface, and the water-sim promoted to rehearsals against real
semantics (the webernetes/K8S3D insight). The estate already speaks kubectl system-natively
(`mag/k8s_bridge.py`) and ran the shape in August (mag namespace, CRD, CronJob, PVC).

The honest cost, itemized:

1. **The unit mismatch.** k8s schedules long-running/restartable processes onto nodes. Our unit
   is an ASK: bytes-in, recipe, contract, one shot, graded on landing. Wrapping asks in pods adds
   image build + container start (seconds) to a fire path that currently lands a 159-ask wave in
   8m06s at $0.218, and buys nothing the manifest/ledger does not already model. A Job-per-wave is
   defensible; a Pod-per-ask is tax.
2. **Double scheduling.** kube-scheduler would place pods onto the one node we have while GPS
   still has to choose family/tier/recipe. The decision that matters (M5) is epistemic; k8s would
   add a scheduler that cannot see it.
3. **The novel organs get no help.** The convergence quorum, the verdict-evidence ledger, the
   burn-pathology terminals - none exist in k8s. We would operate a second control plane AND still
   build everything that differentiates us.
4. **Operational weight on a dev box.** etcd + apiserver + controller-manager memory and upgrade
   churn on the Windows Docker Desktop host, against an estate whose build discipline explicitly
   refuses guard-branches papering over sync problems - a whole second system's failure modes.
5. **The estate already ruled it.** "The mirror may reveal Kubernetes state. It may not become
   Kubernetes authority" (wow.txt mine, K8S3D_RACK_FIND). rib_k8s.py proved the profitable
   direction: compile OUR doctrine into checks wherever a cluster exists, never hand the
   doctrine TO the cluster.

The narrow exception: long, wide, embarrassingly-parallel fan-outs (swarm fires, salon meshes)
may run as k8s Jobs on the existing Docker Desktop cluster through `mag/k8s_bridge.py`, with the
verkle/inbox remaining the state plane (never etcd) and GPS remaining the brain. k8s as a node
pool; never the overmind. Between waves, `tools/k8s_water_sim.py` stays the rehearsal plane for
desired-state changes (priority, quota, shedding, burst) at $0 and zero cluster risk - the
fly's maze_arena for scheduler theory.

Net: the decade of solved patterns is stealable as CODE (section 2) without adopting the
substrate - which is exactly what rib_k8s, k8s_bridge, and k8s_water_sim already did three times.

## 5. Sources (k8s side)

- Pod lifecycle / CrashLoopBackOff: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- Garbage collection / ownerReferences: https://kubernetes.io/docs/concepts/architecture/garbage-collection/
- Finalizers: https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/
- Pod disruption budgets: https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
- client-go wait/jitter: https://pkg.go.dev/k8s.io/apimachinery/pkg/util/wait
- client-go retry (DefaultBackoff Jitter 0.1): https://github.com/kubernetes/client-go/blob/master/util/retry/util.go
- Jitter proposal (SIG api-machinery): https://groups.google.com/g/kubernetes-sig-api-machinery/c/3MfqjMXh6xE

Estate receipts: all estate file:line cites in sections 0-3 were read in bytes this session
(2026-10-01, tree state as-is, no commits). Related landed receipts: SWARM_1.md (the wave this
steals from), X2_material_wiring_census_frozen.md (the disease K8S-02/03 cure), GARDEN_RACTOR.md
+ CROSS_RACTOR_MATRIX.md (the convergence law), tools/k8s_water_sim.py header (the prior map).
