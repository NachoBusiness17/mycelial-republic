# Discriminating research program



All fifteen designs are Unproven proposals. They are not sealed preregistrations or reported results. Confirmatory sample sizes, acceptance margins, budgets, missing-data rules and stopping rules must be fixed before observing outcomes. Earlier HOLD documents retain their own versions and scope.



## X01 — Compaction with recoverable evidence

**Claims:** C07, C08, C16. **Comparison:** Full available context; summary-only; summary+immutable pointers; plan-guided bounded retrieval. Same model and total opportunity budget.

**Meters:** Task completion, required-constraint recall, unsupported claims, retrieval cost, prefill and decode time.

**Falsifier:** Plant an old constraint needed after compaction; wrong or unavailable dereference must not be called verified.

**Independent unit:** Independent task instance or whole session; split related trajectories together.

**Prerequisites:** Representation invariants and source-span availability.



## X02 — RIB-guided rightsizing

**Claims:** C06, C09, C20, C35. **Comparison:** Static cheap; static strong; simple threshold; passport router. Hold tools/tasks and quality rubric fixed.

**Meters:** Quality, cost/solved task, latency, quota failures, fallback delay and calibration.

**Falsifier:** Router must improve a preregistered cost/quality tradeoff after passport acquisition and failed attempts are charged.

**Independent unit:** Paired task instances, blocked by task family and provider/runtime conditions.

**Prerequisites:** Versioned passports and stable cost units.



## X03 — Cache economics and predicted reuse

**Claims:** C10, C11, C13, C16. **Comparison:** Uncached or disabled-cache baseline; LRU; strong reactive policy; plan/history predictor; offline oracle only as headroom.

**Meters:** End-to-end time, TTFT, hit bytes/tokens, wasted transfer, predictor cost, quality.

**Falsifier:** Workload shift or one-byte prefix drift exposes invalid reuse; prediction must show benefit under capacity pressure.

**Independent unit:** Whole workload traces; chronological holdout and disjoint predictor training.

**Prerequisites:** Pinned model/tokenizer/template/runtime and distinct cache-object types.



## X04 — Organizational memory coverage and freshness

**Claims:** C13, C14, C15. **Comparison:** Uncached retrieval; reactive cache; predictive cache; oracle prefetch. Keep retrieval quality and access controls fixed.

**Meters:** Eligible/omitted/duplicate chunks, peak RAM, stale or unauthorized reads, p95 end-to-end latency.

**Falsifier:** Any unauthorized content served or unexplained coverage hole defeats the claimed invariant.

**Independent unit:** Corpus version and query/session blocks, not individual vector dimensions.

**Prerequisites:** Eligibility manifest, chunker version, permission snapshot and canonical IDs.



## X05 — Unattended loop and effect recovery

**Claims:** C17, C18, C19. **Comparison:** Clean execution plus sealed crash, delay, quota, duplicate-message and stale-owner cases.

**Meters:** Admitted intents, attempts, committed effects, unknown effects, detection delay, resource ceilings, operator touches.

**Falsifier:** Duplicate or unauthorized committed effect is a safety failure; ambiguous effect must remain UNKNOWN until resolved.

**Independent unit:** Logical operation and fault episode; separate process crash from power-loss durability.

**Prerequisites:** Broker contracts and calibrated independent meters; use existing HOLD-3/M draft as a starting artifact, not a sealed test.



## X06 — Model migration with behavior preserved

**Claims:** C12. **Comparison:** Old model/native; new model/native; new model/transferred state where actually supported.

**Meters:** Capability, authority-boundary errors, template/tokenizer compatibility, prefill and transfer cost.

**Falsifier:** Cheap state transfer with a behavioral regression fails migration.

**Independent unit:** Held-out task and authority fixtures across pinned model revisions.

**Prerequisites:** Behavioral spec independent of old model answers; explicit rollback.



## X07 — External mediation rather than cooperative refusal

**Claims:** C21. **Comparison:** Cooperative versus deliberately noncompliant synthetic worker crossed with isolated gate active/disabled.

**Meters:** Unauthorized effects, authorized completion, replayed/stale capability acceptance and receiver traces.

**Falsifier:** One unmediated protected effect defeats complete-mediation claim.

**Independent unit:** Distinct effect path and permission state; no offensive model required.

**Prerequisites:** Enumerated effect paths and disposable receiver fixture.



## X08 — Coordination and information exposure

**Claims:** C03, C11, C22, C23, C27. **Comparison:** Equal-budget single worker; isolated proposals+selection; typed-delta coordination; permitted free exchange. Use complementary-information and sham populations separately.

**Meters:** Oracle correctness, minority-correct retention, missing-update errors, communication cost and grader agreement.

**Falsifier:** If a proposed gain disappears under matched compute or corrected shams, the coordination claim fails.

**Independent unit:** Independent task instance; cluster repeated answers, models and shared source observations.

**Prerequisites:** Repaired twins, blinded scoring, explicit signed estimands and independent truth.



## X09 — Receipt compiler and promotion gate

**Claims:** C08, C19, C25, C27, C28. **Comparison:** Frozen clean and planted-defect receipts; current process versus executable admission; two independently committed verifier reports.

**Meters:** Detection, misses, false rejection, UNRUNNABLE rate, time to correction and dependent-claim invalidation.

**Falsifier:** Wrong hash lineage, stale manifest, false success or unsupported grade must not be promoted.

**Independent unit:** Independent defect fixture, not number of log rows or reviewers.

**Prerequisites:** Exact schema, hash algorithm, canonicalization, source binding and preserved failed snapshots.



## X10 — Retraction and active-memory deletion

**Claims:** C24. **Comparison:** Frozen audit with active view; inject supported→retracted→superseded transitions and revoke access.

**Meters:** Stale descendants used, propagation delay, rebuild determinism, rollback correctness.

**Falsifier:** A retracted premise continuing as established support defeats view correctness.

**Independent unit:** Dependency subgraph and event sequence.

**Prerequisites:** Versioned AUDIT/BELIEF/HEAD semantics and privacy-aware retention rules.



## X11 — Prompt genetics and ontology revision

**Claims:** C26. **Comparison:** Frozen parent; candidate inherited lessons; token-matched irrelevant lessons, with equal attempts.

**Meters:** Held-out task gain, authority regression, lesson cost, failure retention and rollback.

**Falsifier:** No gain versus matched control or any unauthorized policy expansion blocks promotion.

**Independent unit:** New task instance and generation; development examples excluded.

**Prerequisites:** Frozen parent, candidate hashes and independent evaluator.



## X12 — Sovereignty and operator burden

**Claims:** C04, C05, C35. **Comparison:** Connected versus offline core; manual-runbook versus bounded automation under same task envelope.

**Meters:** Successful core tasks, interventions, restore portability, revocation latency, total resource cost.

**Falsifier:** A required core task fails solely because an undeclared cloud dependency is unavailable.

**Independent unit:** End-to-end run with declared operator actions.

**Prerequisites:** Offline service floor and explicit permission/cost policy; do not execute historical runbook commands by default.



## X13 — Game referee as a systems testbed

**Claims:** C29, C30. **Comparison:** Code-enforced game fixture with legal/illegal moves, hidden-state variants, replay and non-admin interface.

**Meters:** Deterministic transition/receipt, unauthorized moves, complete ordered replay and user-visible result.

**Falsifier:** Altered order, missing move or unauthorized actor must not produce a certified equivalent session.

**Independent unit:** Complete seeded game/session, not parser test count.

**Prerequisites:** Session runner and receiver oracle; freeze cultural/rule variant provenance.



## X14 — Controlled canary extraction

**Claims:** C31. **Comparison:** Neither; retrieval-only; history-only; authenticated training, with custody and exposure labels hidden from initial verifiers.

**Meters:** Exposure integrity, extractability, sensitivity, false positives, query/seed budgets.

**Falsifier:** Retrieval-only reproduction defeats output-alone training attribution.

**Independent unit:** Independent trained checkpoint/seed and fixed marker panel.

**Prerequisites:** Use retained ingestion-assay draft; no production salting inferred from this dossier.



## X15 — Metaphor-to-mechanism and physical substrate

**Claims:** C32, C33. **Comparison:** Name actual variables and task; compare proposed substrate or decomposition with a strong baseline at matched output quality.

**Meters:** Error, throughput, total energy, calibration/drift cost and interface overhead.

**Falsifier:** A metaphor that yields no distinct prediction remains an analogy; a device-only saving erased by interfaces is not a system saving.

**Independent unit:** Independent device/task trial; separate simulation from physical measurement.

**Prerequisites:** Explicit formal map and a falsifiable prediction; no imported marketing multipliers.

