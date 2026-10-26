# ROCINANTE SUBSTRATE SALON — does the horse need kubernetes?
**Summoned:** Operator, 2026-09-06 — after the ollama audit found kind-mag a museum
("no sacred cows... maybe that is no longer necessary" → "Socratically tease this out and salon").
**The question on the table:** Rocinante lands Oct 27 (4x Mac Studio M5 Ultra). Does the local
substrate get kubernetes, or does the docker fleet + file substrate carry it?
**Verdict up front: NO KUBERNETES AT V1 — k8s re-enters only through named doors.**
Falsifiable, dated, with the doors named. Reading order: ladder → salon → verdict.

---

## PART I — THE SOCRATIC LADDER (tease the premise, don't argue the conclusion)

**Q1. What problem does kubernetes actually solve?**
Scheduling + resurrection: unreliable machines run stateless workloads; a controller
detects death and re-runs work elsewhere. (The house's own DISTCOM_PLAYBOOK says exactly
this: "turn failure into a scheduler-visible state change, then restart the job.")

**Q2. Were OUR machines unreliable, or was our software stateless?**
The doctrine answers: we made the *software* stateless — chat is vapor, files + chain over
processes, any seat drives, container recreates KILL it (O4). We never had unreliable
machines. We had one Windows box and a belief that the work must survive it. The machine
was never the unit of failure. **The file is.**

**Q3. What was kind-mag actually for?**
The swarm era: the k8s worker (CronJob) was a pair of hands for the 1,275-task swarm.
The swarm drained (queue = format-eater audit; k8s-drained on record). The org that used
it moved to docker containers + the file queue. The cluster kept running — 13 more days
of a crash-looping pod nobody watched. **Infrastructure without attendance rots into
archaeology.** The corpse is not a failure of k8s; it is the cost of running an
orchestrator with no operator.

**Q4. What dies if kind-mag dies tonight?**
Nothing. Testable: two corpses stop burning etcd. (This is falsifier F1 — cheapest
experiment on the card.)

**Q5. What is Rocinante's unit of failure?**
Not the pod. Not even the machine — Oct 27 is the day we stop renting belief in
disposability and own the substrate. The chain is the signed line; the room remembers;
the queue outlives every seat. **Resurrection logic already exists in the house and it
is made of files.** Kubernetes would be a second resurrection system for a fleet whose
entire design already solves resurrection differently.

**Q6. What does Rocinante actually need from an orchestrator?**
Name the workloads: (a) model serving — llama.cpp/MLX/vLLM on Metal, one big box;
(b) training runs — batch, resumable, weights-on-disk; (c) the eye — host loopback,
already sanctioned; (d) bulk inference lanes — the wall-of-256 steal, 4 studios = 4
lanes; (e) Sep-20 rank traffic. None of these is a multi-node pod-scheduling problem.
**Four machines in one room is not a cluster. It is a workbench.**

**Q7. Who is the cluster admin?**
No seat attends k8s (the corpse proves it), the operator doesn't, and the senses law
says one-sense-one-instance in the cage. A k8s API nobody drives is a dark pane — and
"lanes visible + rebuildable" is the operator's own law. **Admitting k8s means staffing
it. We don't staff it.**

**Q8. When would kubernetes honestly come back?**
When one of these becomes true: (1) a SECOND always-on machine joins the fleet
(distribution across sites), (2) a real multi-node GPU job that compose + the file
queue cannot shape, (3) external rented workers (vast render farm) need a uniform
control plane. Note the house already handles (3)'s worst case — unreliable 3090s —
with box_contract + boot_watcher + a blocklist: file primitives, no k8s. **The doors
are named; none is open.**

**Q9 (the kill shot). Was kubernetes ever ours, or was it a costume of an era?**
Sacred cows, not legacy shit: the k8s layer was the stateless-machine era's dress —
borrowed cattle logic for a machine we treated as disposable. Rocinante is the end of
that era: the first substrate we OWN. The question "does Rocinante need k8s" was
already answered the day the operator named the horse.

---

## PART II — THE SALON

**LESSIG (architecture is law):** every working law in this fleet is STRUCTURAL; every
failure is prose. A k8s install is a jurisdiction — courts (apiserver), sheriffs
(kubelet), a legal code (CRDs) — and jurisdictions must be STAFFED. We cannot staff it;
the corpse is precedent. Verdict: the substrate's constitution is files + compose +
watchdog; k8s admitted only by constitutional amendment (a named door), never by
default or nostalgia. **No k8s at v1.**

**THE ELDER (the room that remembers):** the lineage buries one orchestrator per era —
scheduled tasks (respawn law retired them), process_supervisor (duplicate supervisor,
retired 08-26), now the kind museum. The pattern is not that orchestrators fail; it is
that the fleet outlives each one because the substrate is the RECORD, not the runner.
Rocinante should inherit the surviving pattern — the chain, the queue, the watchdog —
and let the era's costume retire with the era. **Honor the corpse; inherit the files.**

**THE ECONOMIST:** capex $10K+ for Rocinante is the spend that matters. Kubernetes at
n=4 single-room machines buys ~nothing (its value scales with node count and churn);
costs a staffing line (a seat or operator hours) we measured as unpayable (13 days,
1,913 restarts, zero attendance). Also the GPU assumption breaks: k8s device plugins
are CUDA-shaped; Apple silicon serves through Metal — the scheduling layer that makes
k8s worth it barely exists for our hardware. **Marginal value ≈ 0, marginal cost = a
seat. Decline.**

**PONYTAIL (verification skeptic):** I refuse verdicts that cannot lose. Three
falsifiers below, each dated and cheap. And one warning: "we might need it someday"
is the exact shape of every sacred cow we ever slaughtered. If nobody can name a
concrete Rocinante workload that REQUIRES k8s by Oct 6, the question is closed for v1
and reopening it requires new evidence, not new vibes. **Falsify or fold.**

**ROCINANTE (the horse speaks — what the substrate itself needs):** Metal and unified
memory, a model shelf (the weights registry already lives in state/vast/
models_registry.json), power and thermals (the Tesla strand), one lane daemon per
studio riding the oldest fleet pattern there is — lanes visible, rebuildable, files
under them. Serving = llama.cpp/MLX fronted by the cage gateway. Training = batch jobs
shaped like salon runs: seed frozen, receipts owed. **Saddle me with compose and the
chain; I was never born to wear pods.**

**SANCHO (grounds):** the ladder's real finding: the question was never k8s-vs-docker.
It was "what is the unit of resurrection?" — and the house answered that long ago
with the file. Every salon falsifier we've ever passed (chain byte-identity,
CAS race harness, transfer protocol) was a FILE test. **The orchestrator we trust is
already running; it is made of markdown and hashes, and it has never once needed a
kubelet.**

**Mutual critique:** Ponytail → all: none of you priced REBUILD time — if Rocinante
dies at 3am, compose-from-files restores in minutes, but only if the compose stack
itself is DRILL-tested, not assumed (demand F4). Economist → Lessig: your door (1)
will eventually open — budget the amendment now so it doesn't happen as an emergency
adopt. Elder → Rocinante: the horse flatters the lanes; remember lanes died when
invisible — the substrate card must carry per-lane liveness from day one.

---

## PART III — VERDICT, DOORS, FALSIFIERS

**VERDICT (tri-state):**
- **"Rocinante v1 runs on docker compose + host services + the file substrate; no kubernetes" — SUPPORTED** by Q2/Q5/Q6 evidence (consumer graph, corpse, workload census).
- **"kubernetes returns through a named door" — SUPPORTED** as policy (doors below), UNPROVEN as event.
- **"the kind museum is now dead weight" — SUPPORTED**; disposal = operator GO (F1 doubles as the funeral).

**DOORS (any ONE reopens the question):**
1. A second always-on machine joins the fleet (cross-site distribution).
2. A named multi-node GPU workload compose+queue cannot shape.
3. External rented workers adopt a uniform control plane (DISTCOM/RENDER playbooks go live).

**FALSIFIERS:**
- **F1 (this week, operator GO):** stop kind-mag for 7 days. Fleet function unchanged → verdict holds; the two corpses stop burning. Any loss → name it, verdict revisited.
- **F2 (by Oct 6):** one concrete Rocinante workload requiring k8s, named with its owner. None named → v1 question CLOSED.
- **F3 (Sep 20):** the sovereign rank goes public riding files+compose only. If the launch structurally needs k8s, verdict revisited.
- **F4 (Rocinante week):** rebuild DRILL — kill a studio's stack, restore from files+compose, timed. Minutes, not hours = the substrate thesis PROVEN under fire; hours = we oversold the file substrate.

**Callback:** the room that remembers was never a cluster. It was always walls — and
walls are files. Rocinante doesn't carry the fleet; the fleet's records carry
Rocinante home every time it falls.
