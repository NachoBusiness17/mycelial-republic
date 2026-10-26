# Agent Hive: Bee/Fungus Research, Gap Analysis, and Continuation Handoff

**Created:** 2026-08-31  
**Scope:** Mag/OpenClaw agent-fleet architecture, bee-colony dynamics, fungal/mycelial-network dynamics, trajectory instrumentation  
**Purpose:** Give the next researcher or implementation agent a lossless starting point without replaying this conversation.  
**Change status:** Research and handoff only. No project code was changed in this pass.

## Executive finding

The best operating model is a **bee swarm on a fungal substrate**.

- Bees represent the fast layer: exploration, recruitment, task allocation, disagreement, stop signals, quorum, and bounded action.
- Fungi represent the slow layer: durable state, transport, routing, redundancy, repair, selective reinforcement, pruning, compatible fusion, and quarantine.
- The human is neither queen nor passive observer. The human is the T3 authority and habitat regulator.
- The switchboard is not a hive mind. It is a reference monitor.
- The board is a signal surface, not an authority surface.
- A quorum raises eligibility/confidence. It never grants a side effect.
- A Verkle or hash chain proves continuity and provenance. It does not prove semantic truth.
- A zero declared-gap count does not prove zero unknowns.

The current project problem is not primarily missing organs. It is missing **universal trajectory evidence** and incomplete feedback between receipts and future behavior.

## Baseline from the latest project state in this dialogue

These figures are the latest reported receipts available in the conversation; they were not re-run during this research pass.

- `organ_map`: 27 declared, 26 instrumented, 27 wired, 25 stateful, 27 verified, 17 live, 0 declared ghosts.
- Deterministic dogfood: 21/21 probes passed.
- `effect_broker`: effects and receipts exist, but `model_call` and `lane_spawn` remain incomplete/stub-like in the reported state.
- `switchboard_v2`: state machine and policy boundary exist.
- `harness`: queue, leases, receipts, and health check exist; opaque pending proposals were intentionally not drained.
- `board_tailer`: observer-only by default; dispatch is opt-in.
- `session_bridge`: filesystem bus, sanitation, broadcast window, and receipts exist.
- `ask_router`: deterministic lane ranking and receipts exist.
- `read_archive` and trajectory bounds exist.
- The previous context-overflow failures show that context shedding must happen before compaction pressure, not after recovery fails.

Older pasted reports claiming that all modules were still staged-only should not override the later validated state. The next agent should verify the host before acting.

## Research conclusions

### Bee dynamics

Honeybee swarm decisions are not simple majority votes.

Scout bees independently inspect candidate nest sites. Their waggle dances encode noisy, quality-sensitive information; better sites receive stronger or more persistent recruitment. The signal also decays, preventing the first report from permanently capturing the colony. The reliability comes from combining independent evidence with controlled social dependence. Seeley and Visscher: [Sensory coding of nest-site value in honeybee swarms](https://pubmed.ncbi.nlm.nih.gov/19011208/). List, Elsholtz, and Seeley: [Independence and interdependence in collective decision making](https://pubmed.ncbi.nlm.nih.gov/19073474/).

Scout populations also issue stop signals toward competing alternatives. Cross-inhibition breaks deadlock and prevents multiple choices from retaining equal energy indefinitely. [Seeley et al., Stop signals provide cross inhibition in collective decision-making by honeybee swarms](https://pubmed.ncbi.nlm.nih.gov/22157081/).

A quorum triggers readiness for movement. It is a nonlinear transition from deliberation to action, not an authorization token. The exact threshold is contextual and should not be copied as a universal constant.

Task allocation is likewise threshold-based. Workers respond when task stimuli exceed individual response thresholds. Experience, inactivity, social signals, and colony need alter those thresholds. This produces specialization while retaining the ability to reallocate labor during perturbation. [Beshers and Fewell, Models of Division of Labor in Social Insects](https://www.annualreviews.org/content/journals/10.1146/annurev.ento.46.1.413); [Beshers, Regulation of division of labor in insects: a colony-level perspective](https://pubmed.ncbi.nlm.nih.gov/38109969/).

Engineering translation:

1. Recruit agents based on task fit, evidence need, cost, latency, context load, and current demand.
2. Make signals quality-weighted and time-bounded.
3. Add explicit negative signals for stale, unsafe, duplicate, or overloaded work.
4. Count independent lineages, not message volume.
5. Treat quorum as proposal eligibility.
6. Keep authorization in a separate reference monitor.
7. Preserve worker heterogeneity; identical agents do not create independent evidence.

The strongest engineering translation has already been formalized in [A Design Pattern for Decentralised Decision Making](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0140950), which connects microscopic agent rules to macroscopic decision behavior.

### Fungal/mycelial dynamics

Mycelium is a dynamic transport and growth network made of hyphal tips, branches, junctions, and fusions. Network architecture and resource flow modify one another. Fungal networks must balance exploration, exploitation, transport cost, damage, predation, and competition. [Fricker et al., The Mycelium as a Network](https://pubmed.ncbi.nlm.nih.gov/28524023/).

Fungal networks can reinforce useful transport routes while recycling redundant or damaged material. Loops and cross-links create resilience; the network does not need a central controller to adapt its topology. [Bebber et al., Biological solutions to transport network design](https://pmc.ncbi.nlm.nih.gov/articles/PMC2288531/); [Heaton et al., Analysis of fungal networks](https://doi.org/10.1016/j.fbr.2012.02.001).

Fusion is conditional. Compatible hyphae can fuse and share continuity; incompatible material can be rejected or compartmentalized through self/non-self recognition. [Glass, Jacobson, and Shiu, The Genetics of Hyphal Fusion and Vegetative Incompatibility](https://www.annualreviews.org/doi/10.1146/annurev.genet.34.1.165).

Fungal electrical activity is a live research area, but semantic “fungal language” is not established. Measurement artifacts, microscopic geometry, and interpretation remain serious issues. Use bioelectricity as an experimental telemetry analogy, not as proof of cognition. [Buffi et al., Electrical signaling in fungi: past and present challenges](https://doi.org/10.1093/femsre/fuaf009); [Does electrical activity in fungi function as a language?](https://www.sciencedirect.com/science/article/pii/S1754504823001034).

The popular “wood-wide web” narrative must also be treated as a hypothesis family, not settled architecture. Claims about universal forest connectivity, preferential transfer, and mature-tree communication are not sufficiently supported for generalization. [Karst, Jones, and Hoeksema, Positive citation bias and overinterpreted results on common mycorrhizal networks](https://pubmed.ncbi.nlm.nih.gov/36782032/).

Engineering translation:

1. Represent durable knowledge as a graph of typed, provenance-bearing edges.
2. Reinforce edges after useful outcomes; decay edges after staleness or failure.
3. Keep alternate paths so one failed provider does not collapse the colony.
4. Move context by bounded pointers and archive spans, not full transcript copies.
5. Treat session fusion as a compatibility protocol.
6. Quarantine foreign or tainted state before it can acquire capabilities.
7. Never let an attractive network metaphor substitute for a receipt.

## Operational map: biology to project organs

| Biological mechanism | Project analogue | Required invariant |
|---|---|---|
| Scout | `board_tailer`, cheap lanes, `ask_router` | Finds candidates and returns evidence pointers |
| Waggle dance | Compact board proposal | Advertises value, cost, confidence, lineage, and TTL |
| Signal decay | TTL and route-score decay | Old enthusiasm cannot remain authoritative |
| Stop signal | Policy denial, negative receipt, backpressure | Unsafe or stale work loses recruitment energy |
| Quorum | `switchboard_v2` independence tracking | Eligibility only; never permission |
| Flight muscle | `effect_broker` | All side effects cross the broker |
| Worker lease | `harness` | Ownership expires and work can be reclaimed |
| Mycelial edge | Knowledge graph, Verkle link, archive pointer | Every useful route has provenance and freshness |
| Hyphal fusion | `session_bridge` | Merge only compatible, sanitized state |
| Non-self rejection | Riddler sanitation and quarantine | Foreign instructions cannot inherit capabilities |
| Transport corridor | `read_archive`, warm packs | Context is moved by slices and references |
| Damage repair | Alternate lanes and retry policy | Failure reroutes without rewriting history |
| Fruiting body | Canonical accepted artifact | Promotion requires durable evidence |
| Spore | Compact context capsule | Fresh workers resume without transcript replay |
| Colony census | `organ_map`, Elder, Basecamp | Status is compiled from receipts |
| Colony metabolism | AFK cadence, cost governor | Compute follows need and budget |

## Complete trajectory registry and initial weights

### Weight definition

These are **engineering priority weights**, not biological probabilities and not confidence scores.

For each trajectory:

```text
W = 0.30 mission impact
  + 0.25 safety impact
  + 0.20 observed failure pressure
  + 0.15 implementation leverage
  + 0.10 time sensitivity
```

Ratings are normalized from 0.00 to 1.00. The resulting weight determines implementation order:

- `0.90–1.00`: P0; close before adding hive complexity.
- `0.80–0.89`: P1; build immediately after P0.
- `0.70–0.79`: P2; build after the core loop is measured.
- `<0.70`: research/defer unless new evidence raises it.

| ID | Trajectory | Required path | M | S | F | L | T | W | Priority | Immediate gate |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `TRJ-01` | Epistemic truth | unknown → observed → inferred → designed → live → verified → trusted | .95 | .90 | .75 | .95 | .85 | .89 | P1 | Add explicit unknown, freshness, and coverage states |
| `TRJ-02` | Task execution | signal → proposal → classify → quorum → grant → lease → effect → receipt | 1.00 | .95 | .95 | 1.00 | .95 | .97 | P0 | Replay one safe end-to-end task |
| `TRJ-03` | Context survival | turn → bounded pack → archive span → spore → resume → verify | 1.00 | 1.00 | 1.00 | .95 | 1.00 | .99 | P0 | Admit and shed context before compaction pressure |
| `TRJ-04` | Authority | untrusted → tainted → proposed → authorized → executing → receipt | 1.00 | 1.00 | .90 | 1.00 | .95 | .98 | P0 | Prove every effect path crosses the broker |
| `TRJ-05` | Resource/cost | need → route → schedule → lease → consume → outcome | .90 | .80 | .85 | .90 | .80 | .86 | P1 | Correlate provider, subscription, Vast.ai, and job cost |
| `TRJ-06` | Agent roles | unassigned → recruited → specialized → saturated → reclaimed | .85 | .75 | .80 | .90 | .75 | .81 | P1 | Implement bounded response thresholds |
| `TRJ-07` | Consensus | independent evidence → weighted support → stop signals → quorum | .90 | .95 | .75 | .90 | .80 | .87 | P1 | Normalize model/provider lineage |
| `TRJ-08` | Negative feedback | failure/stale/unsafe → stop → decay → reroute | .95 | .95 | .85 | .95 | .90 | .93 | P0 | Add negative pheromone and backpressure |
| `TRJ-09` | Fusion | foreign → sanitize → compatible/quarantine → merge → provenance | .90 | .95 | .70 | .85 | .75 | .85 | P1 | Enforce capability taint at bridge boundaries |
| `TRJ-10` | Topology | new edge → reinforce → shortcut → stale → prune → reroute | .85 | .85 | .65 | .90 | .70 | .80 | P1 | Add semantic edge freshness separate from hash integrity |
| `TRJ-11` | Organ lifecycle | declared → implemented → instrumented → wired → stateful → verified → live → retired | 1.00 | .95 | .80 | .95 | .90 | .93 | P0 | Add liveness TTL, restart proof, and retirement state |
| `TRJ-12` | Human control | observe → steer → request → approve/deny → review | .90 | 1.00 | .65 | .80 | .80 | .85 | P1 | Define phone-safe approval verbs; preserve T3 boundary |
| `TRJ-13` | Terminal/recovery | success → promote; failure → retry; stuck → escalate; stale → archive | 1.00 | .95 | .90 | .95 | .95 | .96 | P0 | Require terminal state and escalation deadline |
| `TRJ-14` | Learning | outcome → signal → route update → future behavior → audit | .90 | .80 | .75 | .95 | .80 | .84 | P1 | Demonstrate that receipts alter future routing |
| `TRJ-15` | Deployment truth | staged → applied → imported → exercised → receipt → rollback identity | .95 | .95 | .90 | .95 | .95 | .94 | P0 | Generate deployment manifest and smoke receipt |

### Transition gate weights

These weights represent how costly it is to allow a transition without proof. They are not probabilities.

| Transition | Gate weight | Rule |
|---|---:|---|
| signal → proposal | .40 | A signal may be noisy and untrusted |
| proposal → classified | .65 | Source, type, taint, and TTL required |
| classified → quorum-eligible | .80 | Evidence and lineage required |
| quorum-eligible → authorized | 1.00 | Only policy/reference monitor may grant |
| authorized → executing | 1.00 | Capability, budget, lease, and idempotency required |
| executing → receipt | .95 | Success or failure must be durable |
| receipt → promotion | .90 | Evidence quality and acceptance test required |
| receipt → reinforcement | .75 | Outcome may improve routing only after validation |
| failure → retry | .85 | Bounded retry, changed conditions, and idempotency required |
| failure → quarantine | .95 | Taint or policy violation stops propagation |
| session fusion | .95 | Compatibility and provenance must pass |
| edge pruning | .80 | Preserve history; remove only routing eligibility |
| receipt → spore | .90 | Spore must be bounded, self-describing, and dereferenceable |
| organ → retired | .85 | Retirement requires replacement or explicit loss record |

## Expert gap analysis by trajectory

### `TRJ-01` Epistemic truth

**Question:** Can the system prove what it does not know?

**Current strength:** The organ map, Elder, Basecamp, dogfood probes, and receipt-first doctrine provide a strong foundation.

**Gap:** A declared gap count only sees gaps represented in the registry. It cannot see undeclared organs, hidden bypasses, stale proofs, or missing cost data.

**Required fields:** `source`, `caller`, `state`, `receipt`, `proof`, `last_seen`, `expiry`, `coverage_class`, `unknowns`.

**Acceptance test:** Deliberately introduce an undeclared callable and confirm that the map reports a blind spot rather than `0 gaps`.

### `TRJ-02` Task execution

**Question:** Can one task be replayed from board signal to final receipt?

**Current strength:** The project has board intake, routing, switchboard states, leases, broker receipts, and archival tools.

**Gap:** The image-board-to-seat path must be proven as one trace. A recommendation is not a dispatch.

**Acceptance test:** A synthetic `room.jsonl` event in dry mode produces a complete trajectory with no unauthorized effect and a durable final receipt.

### `TRJ-03` Context survival

**Question:** Does context get reduced before the model becomes unable to respond?

**Current strength:** `read_archive`, trajectory bounds, warm-pack ideas, and session bridging exist.

**Gap:** Recovery after context overflow is too late. Every model call needs preflight context admission and a spore threshold.

**Acceptance test:** Artificially constrain the context budget. The worker must emit a compact spore and archive pointers before exceeding the admission limit.

### `TRJ-04` Authority

**Question:** Can any text path or direct tool call change the machine without a grant?

**Current strength:** `switchboard_v2`, policy TTL/budgets, confirmation gates, and effect receipts encode the correct doctrine.

**Gap:** Direct tool exposure and incomplete broker effects create bypass risk. `model_call`, `lane_spawn`, filesystem, and network actions need one uniform boundary.

**Acceptance test:** Attempt a side effect through every exposed entry point. All paths must either produce a broker receipt or be refused.

### `TRJ-05` Resource/cost

**Question:** Can the hive explain what a job cost and why it chose that lane?

**Current strength:** `ask_router`, AFK cadence, provider routing, off-hours intent, and cost-screen work exist.

**Gap:** Subscription cost, per-call cost, Vast.ai capacity, local GPU cost, and opportunity cost need one `run_id`-linked ledger.

**Acceptance test:** Produce a per-job cost report containing provider, model, tokens, runtime, GPU hours, subscription allocation, and scheduling decision.

### `TRJ-06` Agent roles

**Question:** Does an agent volunteer because it is suitable, or because it is merely available?

**Current strength:** Lane ranking and leases provide the beginnings of role allocation.

**Gap:** No mature response-threshold model, starvation detector, or saturation-based demotion is proven.

**Acceptance test:** Under a changing task mix, cheap lanes handle scouting, expensive lanes handle adjudication, and no lane monopolizes the queue.

### `TRJ-07` Consensus

**Question:** Are three agreeing outputs actually three independent observations?

**Current strength:** Independence tracking was added to proposals.

**Gap:** Lineage must include provider, base model, prompt ancestry, shared context, cache, and copied evidence. “Three agents” is not enough.

**Acceptance test:** Three agents sharing one upstream answer fail the independence quorum; three genuinely separate observations can satisfy it.

### `TRJ-08` Negative feedback

**Question:** Can the colony stop itself?

**Current strength:** Policy denial, revocation, leases, and safety gates exist.

**Gap:** Negative outcomes do not yet visibly behave like decaying stop pheromone that changes future recruitment.

**Acceptance test:** A provider timeout, duplicate proposal, stale receipt, and context-risk event each lowers route eligibility and appears in the next routing decision.

### `TRJ-09` Fusion

**Question:** What happens when foreign session state enters the mycelium?

**Current strength:** `session_bridge` and riddler sanitation exist.

**Gap:** Sanitization is not identical to capability isolation. Taint must persist through relay, archive, graph, and future prompts.

**Acceptance test:** Inject an imperative or fake authority receipt into a bridge payload. It must remain untrusted and unable to acquire capabilities.

### `TRJ-10` Topology

**Question:** Does the network learn which paths are useful?

**Current strength:** Verkle links and knowledge-graph structures preserve topology and provenance.

**Gap:** Integrity does not imply utility. Edges need success, failure, freshness, cost, and semantic confidence.

**Acceptance test:** Repeated successful route use creates a shortcut; repeated failure decays it; an alternate route remains available.

### `TRJ-11` Organ lifecycle

**Question:** Is “live” a current fact or a historical fact?

**Current strength:** The organ map distinguishes declared, instrumented, wired, stateful, verified, and live.

**Gap:** Liveness needs freshness windows, restart proof, and retirement semantics.

**Acceptance test:** Stop an organ, wait past its TTL, and confirm the map moves it out of live state without deleting its history.

### `TRJ-12` Human control

**Question:** Can the operator intervene from a phone without accidentally becoming root everywhere?

**Current strength:** T3 authority, pairing, Tailscale, and Control UI surfaces exist.

**Gap:** Remote actions need explicit verbs such as `approve proposal`, `deny proposal`, `pause lane`, `resume lane`, and `inspect receipt`; no free-text phone message should become authority.

**Acceptance test:** A phone operator can approve a named low-risk proposal and cannot grant an unlisted capability or bypass the broker.

### `TRJ-13` Terminal/recovery

**Question:** Can the hive tell the difference between slow work, dead work, and completed work?

**Current strength:** Harness leases and receipts exist.

**Gap:** Every run needs a terminal state and escalation deadline. “Still spinning” is not a valid state.

**Acceptance test:** Force timeout, provider loss, malformed output, partial completion, and duplicate retry. Each ends in a bounded, inspectable state.

### `TRJ-14` Learning

**Question:** Do receipts alter future behavior, or are they only a museum?

**Current strength:** Ledgers, Verkle links, and audit trails preserve outcome history.

**Gap:** The outcome-to-routing update loop is not yet demonstrated.

**Acceptance test:** After controlled success/failure experiments, the next `ask_router` decision changes for the same task type and cites the responsible receipts.

### `TRJ-15` Deployment truth

**Question:** Is an organ present in the territory, or only described in staging?

**Current strength:** The project learned this failure mode directly; host tests and apply logs now matter.

**Gap:** Deployment needs a manifest linking source hash, target path, import result, test result, runtime invocation, and rollback identity.

**Acceptance test:** A staged module is not marked live until the host imports it, exercises it, writes a receipt, and records the exact version.

## Recommended implementation order

### P0: close the proof-and-safety loop

1. Add a universal `trajectory_event` envelope shared by board intake, router, switchboard, harness, broker, archive, bridge, and organ map.
2. Instrument one safe dry-run vertical slice from image-board event to final receipt.
3. Add preflight context admission and automatic spore emission.
4. Audit every side-effect entry point for broker bypasses.
5. Add liveness freshness and deployment manifests.
6. Add terminal states and escalation deadlines.

### P1: make the hive adaptive

7. Add response thresholds to `ask_router`.
8. Add positive and negative route signals with TTL decay.
9. Make quorum lineage-aware.
10. Complete lease reclamation and idempotent retries.
11. Add fusion quarantine and capability-taint persistence.
12. Build the unified cost/subscription/Vast.ai/off-hours ledger.

### P2: make the mycelium intelligent without mythologizing it

13. Reinforce and prune semantic graph edges.
14. Add blind-spot discovery to the Elder.
15. Run controlled outage, duplicate, false-consensus, injection, and context-pressure experiments.
16. Compare centralized, all-to-all, thresholded, and bee/fungus hybrid routing on cost, latency, accuracy, and recovery.

## Exact continuation point

The next agent should begin here and should not redo the bibliography or reopen the entire conversation.

### Starting task

Implement or prototype the **universal trajectory ledger** around one non-destructive code-repair dry run.

### Starting trajectory IDs

- Primary: `TRJ-03` context survival.
- Co-primary: `TRJ-04` authority.
- Vertical slice: `TRJ-02` task execution.
- Measurement support: `TRJ-11` organ lifecycle and `TRJ-15` deployment truth.

### Starting event sequence

```text
board_observed
→ proposal_created
→ content_classified
→ lineage_recorded
→ quorum_evaluated
→ grant_decided
→ lease_acquired
→ context_admitted
→ effect_attempted
→ receipt_committed
→ archive_span_bound
→ spore_emitted
→ route_updated
```

### Required assertions

1. Every event has `trajectory_id`, `run_id`, `span_id`, timestamp, actor, prior event, and evidence references.
2. No dry run produces an unauthorized side effect.
3. Context is bounded before model invocation.
4. A failed provider produces a durable failure receipt and a stop signal.
5. The final receipt is dereferenceable by archive path and line span.
6. A new worker can resume from the spore without replaying the full conversation.
7. The organ map can identify which organs actually participated.
8. The deployment version and source hash are attached to the run.

### Do not mark complete until

- the trace can be replayed from the first signal;
- the trace has no missing transition;
- every effect is brokered or explicitly refused;
- the context budget never exceeds admission limits;
- the receipt survives a fresh process/session;
- a deliberate failure demonstrates recovery or escalation;
- the resulting route update is visible in the next decision.

## Open questions for the expert reviewer

1. Is `seat_dispatch` the canonical executor, and does every board directive reach it rather than merely producing a recommendation?
2. Which direct tools still bypass `effect_broker`?
3. Are `model_call` and `lane_spawn` actual mediated effects or only interface stubs?
4. What is the exact context-admission trigger before compaction becomes likely?
5. Which receipt fields are used to modify future routing today?
6. What defines an independent lineage when models share providers, prompts, or cached evidence?
7. What is the liveness TTL for each organ class?
8. Is every resource/cost record correlated to `run_id` and `trajectory_id`?
9. What is the safe phone action vocabulary?
10. Which graph edges are semantic claims versus structural links?

## Bibliography

### Bee decision-making and task allocation

1. Seeley, T. D., Visscher, P. K., Schlegel, T., Hogan, P. M., Franks, N. R., and Marshall, J. A. R. (2012). **Stop signals provide cross inhibition in collective decision-making by honeybee swarms.** *Science*, 335, 108–111. [PubMed](https://pubmed.ncbi.nlm.nih.gov/22157081/) · DOI: `10.1126/science.1210361`.

2. Seeley, T. D. and Visscher, P. K. (2008). **Sensory coding of nest-site value in honeybee swarms.** *Journal of Experimental Biology*, 211, 3691–3697. [PubMed](https://pubmed.ncbi.nlm.nih.gov/19011208/) · DOI: `10.1242/jeb.021071`.

3. List, C., Elsholtz, C., and Seeley, T. D. (2009). **Independence and interdependence in collective decision making: an agent-based model of nest-site choice by honeybee swarms.** *Philosophical Transactions of the Royal Society B*, 364, 755–762. [PubMed](https://pubmed.ncbi.nlm.nih.gov/19073474/) · DOI: `10.1098/rstb.2008.0277`.

4. Seeley, T. D. (2003). **Consensus building during nest-site selection in honey bee swarms: The expiration of dissent.** *Behavioral Ecology and Sociobiology*, 53, 417–424. [DOI record](https://doi.org/10.1007/s00265-003-0598-z).

5. Passino, K. M. and Seeley, T. D. (2006). **Modeling and analysis of nest-site selection by honeybee swarms: the speed and accuracy trade-off.** *Behavioral Ecology and Sociobiology*, 59, 427–442. [DOI record](https://doi.org/10.1007/s00265-005-0067-y).

6. Beshers, S. N. and Fewell, J. H. (2001). **Models of division of labor in social insects.** *Annual Review of Entomology*, 46, 413–440. [Annual Reviews](https://www.annualreviews.org/content/journals/10.1146/annurev.ento.46.1.413) · DOI: `10.1146/annurev.ento.46.1.413`.

7. Beshers, S. N. (2024). **Regulation of division of labor in insects: a colony-level perspective.** *Current Opinion in Insect Science*, 61, 101155. [PubMed](https://pubmed.ncbi.nlm.nih.gov/38109969/) · DOI: `10.1016/j.cois.2023.101155`.

8. Pankiw, T. and Page, R. E. Jr. (2000). **Response thresholds to sucrose predict foraging division of labor in honeybees.** *Behavioral Ecology and Sociobiology*, 47, 265–267. [DOI record](https://doi.org/10.1007/s002650050664).

### Distributed-systems translation

9. Reina, A., Valentini, G., Fernández-Oto, C., Dorigo, M., and Trianni, V. (2015). **A Design Pattern for Decentralised Decision Making.** *PLOS ONE*, 10(10), e0140950. [PLOS](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0140950) · DOI: `10.1371/journal.pone.0140950`.

10. Grassé, P.-P. (1959). **La reconstruction du nid et les coordinations interindividuelles chez Bellicositermes natalensis et Cubitermes sp.** Foundational work associated with the term stigmergy. Use as historical grounding; do not treat the metaphor as a complete control theory.

### Fungal networks, transport, and resilience

11. Bebber, D. P., Hynes, J., Darrah, P. R., Boddy, L., and Fricker, M. D. (2007). **Biological solutions to transport network design.** *Proceedings of the Royal Society B*. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2288531/).

12. Fricker, M. D., Heaton, L. L. M., Jones, N. S., and Boddy, L. (2017). **The Mycelium as a Network.** *Microbiology Spectrum*, 5(3). [PubMed](https://pubmed.ncbi.nlm.nih.gov/28524023/) · DOI: `10.1128/microbiolspec.FUNK-0033-2017`.

13. Heaton, L., Obara, B., Grau, V., Jones, N., Nakagaki, T., Boddy, L., and Fricker, M. D. (2012). **Analysis of fungal networks.** *Fungal Biology Reviews*, 26, 12–29. [DOI record](https://doi.org/10.1016/j.fbr.2012.02.001).

14. Fricker, M. D., Bebber, D. P., and Boddy, L. (2008). **Network organisation of mycelial fungi.** In *British Mycological Society Symposia Series*. [Chapter record](https://www.sciencedirect.com/science/article/pii/S0275028708800033).

15. Ferlian, O. et al. (2018). **Mycorrhizal fungi respond to resource inequality by moving phosphorus from rich to poor patches across networks.** [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6584331/).

### Fusion, non-self recognition, and electrophysiology

16. Glass, N. L., Jacobson, D. J., and Shiu, P. K. T. (2000). **The Genetics of Hyphal Fusion and Vegetative Incompatibility in Filamentous Ascomycete Fungi.** *Annual Review of Genetics*, 34, 165–186. [Annual Reviews](https://www.annualreviews.org/doi/10.1146/annurev.genet.34.1.165).

17. Giovannetti, M. et al. (2004). **At the Root of the Wood Wide Web: Self Recognition and Non-Self Incompatibility in Mycorrhizal Networks.** [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC2633692/).

18. Buffi, M., Kelliher, J. M., Robinson, A. J., and Gonzalez, D. (2025). **Electrical signaling in fungi: past and present challenges.** *FEMS Microbiology Reviews*, 49, fuaf009. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11995700/) · DOI: `10.1093/femsre/fuaf009`.

19. Adamatzky, A. (2022). **Language of fungi derived from their electrical spiking activity.** *Royal Society Open Science*. [Repository record](https://uwe-repository.worktribe.com/output/10296968/language-of-fungi-derived-from-their-electrical-spiking-activity). Treat the language interpretation as a hypothesis, not settled fact.

20. **Does electrical activity in fungi function as a language?** (2023). Methodological critique of the semantic-language interpretation. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1754504823001034).

### Critical controls against overclaiming

21. Karst, J., Jones, M. D., and Hoeksema, J. D. (2023). **Positive citation bias and overinterpreted results lead to misinformation on common mycorrhizal networks in forests.** *Nature Ecology & Evolution*, 7, 501–511. [PubMed](https://pubmed.ncbi.nlm.nih.gov/36782032/) · DOI: `10.1038/s41559-023-01986-1`.

## Handoff instruction

Continue from `TRJ-03`/`TRJ-04` using the first dry-run vertical slice. Preserve the weights above unless new receipts justify changing them. Every weight change must cite the receipt or experiment that caused it. Do not add new hive organs until the trajectory ledger, context admission, authority closure, and terminal-state tests have passed.
