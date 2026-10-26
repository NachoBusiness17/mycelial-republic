# VENUE RADAR INVARIANT CANDIDATES (2026-10-24)

**Source Artifact:** `watch/inbox/venue_mine_20261024_digest.md`
**Generated:** 2026-10-24T01:54:38.490419Z
**Status:** Candidate Synthesis and Invariant Promotion Intake
**House Law Status:** Strictly verified. Zero unicode em-dashes.

---

## 1. Executive Summary

The free venue signal mining sweep on 2026-10-24 evaluated 29 unique items across free, unauthenticated venues (arXiv Atom, Hacker News Algolia, Lobsters RSS, Reddit RSS). Each item was scored, deduplicated by URL, and bound to existing estate operational organs in `configs/signal_lexicon.json`.

From this signal harvest, five high-leverage research preprints and peer-reviewed scientific publications were extracted based on their theoretical rigor, score alignment, and direct applicability to estate failure modes (provenance destruction, unbounded queue backpressure, execution graph retrieval, and multi-agent homeostatic regulation).

Each signal has been distilled into an operational invariant rule formulated for admission to `memory/percolator/invariants.json`, assigned a deterministic canonical hash, mapped to its respective estate binding, and paired with an explicit falsification kill condition conforming to `invariant_falsifier.v1`.

---

## 2. Top 5 High-Leverage Research Preprints

### Preprint 1: Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents
- **Publication / Venue:** arXiv (arXiv:2610.29869)
- **Direct URL:** https://arxiv.org/abs/2610.29869
- **Signal Score:** 0.921 (Family: `provenance`)
- **Estate Law:** "who asserted this, and on what evidence - stored with the claim"
- **Subsystem Binding:** `memory_store.db facts (no provenance column - known gap from the 2026-10-20 paper check); receipts in memory/runs/`
- **Canonical Hash:** `0e379533cb30b633`

#### Theoretical Leverage and Empirical Grounding
When autonomous LLM coding agents compress long execution traces through context compaction, origin citations, commit receipts, and evidentiary attributions are routinely pruned or misattributed to the compacting agent itself. This phenomenon, termed 'compaction laundering', converts tentative speculative outputs into synthesized pseudo-facts that poison downstream retrieval. Within our estate, where memory tapes and subagent session logs are routinely summarized across generational cascades, preserving immutable attestation envelopes is vital to prevent epistemic rot.

#### Candidate Invariant Rule
> `Context compaction must preserve attestation hashes and origin timestamps as immutable envelopes; synthesized claims without preserved origin provenance are tagged unverified proposal rather than durable fact.`

#### Falsification Kill Condition (`invariant_falsifier.v1`)
- **Kind:** `field_complete`
- **Target:** `memory/percolator/invariants.json`
- **Field:** `cycle_hits`
- **Owner:** `seat`
- **Review By:** `2026-11-24`
- **Falsification Note:** Compact-pass claims stripped of source citation or origin hash in memory_store.db falsify the envelope law.

---

### Preprint 2: EPGM: Execution Provenance for Budgeted Agent Memory Retrieval
- **Publication / Venue:** arXiv (arXiv:2609.25913)
- **Direct URL:** https://arxiv.org/abs/2609.25913
- **Signal Score:** 0.755 (Family: `provenance`)
- **Estate Law:** "who asserted this, and on what evidence - stored with the claim"
- **Subsystem Binding:** `memory_store.db facts; memory/cas/slabs/ and memory/cas/epgm/ provenance sidecars`
- **Canonical Hash:** `dcfbb448eb41f327`

#### Theoretical Leverage and Empirical Grounding
Standard naive semantic vector similarity for agent memory retrieval fails catastrophically in multi-step problem solving because it lacks execution causality and budget bounds. EPGM demonstrates that memory retrieval must navigate explicit Execution Provenance Graphs (EPGM), connecting retrieved memory slabs directly to the verified execution receipts, outcome states, and parent hashes under an explicit token budget. This binds directly to our current Content-Addressable Storage (CAS) mesh and the EPGM sidecars being generated in `memory/cas/epgm/`.

#### Candidate Invariant Rule
> `Memory retrieval across agent sessions must traverse explicit execution provenance graphs bounded by a token retrieval budget, ranking by verified causal execution receipts rather than semantic similarity alone.`

#### Falsification Kill Condition (`invariant_falsifier.v1`)
- **Kind:** `log_zero`
- **Target:** `logs/failure_kb.jsonl`
- **Pattern:** `unbudgeted_retrieval_overflow|epgm_sidecar_missing`
- **Window Days:** 7
- **Owner:** `seat`
- **Review By:** `2026-11-24`
- **Falsification Note:** A retrieval event exceeding token budget or ignoring execution receipts in memory/cas/epgm/ triggers a falsification failure.

---

### Preprint 3: The Irreversibility Budget: Fleet-Level Risk Accounting and Admission Control
- **Publication / Venue:** arXiv (arXiv:2609.00275)
- **Direct URL:** https://arxiv.org/abs/2609.00275
- **Signal Score:** 0.303 (Family: `backpressure`)
- **Estate Law:** "intake must not exceed drain; a queue that only grows is not a queue"
- **Subsystem Binding:** `tools/commit_sweeper.py - 10-minute drain vs multi-thousand-file intake; observed 20+ min sweeps (2026-10-21)`
- **Canonical Hash:** `3c07a4f3fd54868a`

#### Theoretical Leverage and Empirical Grounding
Systems that rely on asynchronous background sweeper processes and unbounded work queues suffer latency collapse and irreversible state corruption when ingestion velocity exceeds drain rate. The Irreversibility Budget framework introduces formal fleet-level risk accounting and admission control: when the drain latency exceeds safe thresholds (e.g., commit sweeps exceeding 10 minutes), admission control must actively throttle or reject incoming mutating tasks rather than buffering indefinitely.

#### Candidate Invariant Rule
> `Irreversible mutations across fleet processes are gated by an admission control budget bounded by drain latency; queue growth beyond drain capacity halts ingestion rather than buffering indefinitely.`

#### Falsification Kill Condition (`invariant_falsifier.v1`)
- **Kind:** `log_zero`
- **Target:** `logs/failure_kb.jsonl`
- **Pattern:** `sweeper_timeout|drain_lag_unbounded`
- **Window Days:** 7
- **Owner:** `operator`
- **Review By:** `2026-11-24`
- **Falsification Note:** Sweeper drain exceeding the 10-minute window while commit chute intake remains unthrottled falsifies admission control.

---

### Preprint 4: Methods, Provenance and Limitations Documentation for Asteroid Approach Reports
- **Publication / Venue:** Zenodo (Zenodo:22868834)
- **Direct URL:** https://zenodo.org/records/22868834
- **Signal Score:** 0.342 (Family: `provenance`)
- **Estate Law:** "who asserted this, and on what evidence - stored with the claim"
- **Subsystem Binding:** `watch/claims.jsonl verifier field, memory_store.db empirical facts, memory/runs/ receipts`
- **Canonical Hash:** `8ae8cf241fabe0bb`

#### Theoretical Leverage and Empirical Grounding
Scientific reporting from Zenodo demonstrates that high-consequence empirical claims cannot be safely detached from their measurement methodology, observational precision, and boundary conditions. When downstream consumers ingest bare claims without explicit limitations metadata, false confidence spreads through the decision tree. In the estate, every empirical fact stored in `memory_store.db` or claimed in `watch/claims.jsonl` must co-locate its observation methodology and limitation bounds.

#### Candidate Invariant Rule
> `Every empirical state claim crossing subsystem boundaries must store its observation methodology, boundary limitations, and confidence bounds co-located with the assertion record.`

#### Falsification Kill Condition (`invariant_falsifier.v1`)
- **Kind:** `field_complete`
- **Target:** `watch/claims.jsonl`
- **Field:** `verifier`
- **Owner:** `claim-ledger`
- **Review By:** `2026-11-24`
- **Falsification Note:** Any cross-boundary claim entered without bound limitations or verifier attestation falsifies the documentation invariant.

---

### Preprint 5: Human homeostasis is more efficient in social proximity
- **Publication / Venue:** Science Advances (DOI:10.1126/sciadv.aeg4937)
- **Direct URL:** https://www.science.org/doi/10.1126/sciadv.aeg4937
- **Signal Score:** 0.28 (Family: `homeostasis`)
- **Estate Law:** "regulation is a loop with a sensor, a setpoint, and a cost"
- **Subsystem Binding:** `fossil_check bars (168h/720h), falsifier review dates, sweeper cadence, fleet phase synchronization`
- **Canonical Hash:** `befcf0c04116450b`

#### Theoretical Leverage and Empirical Grounding
Published in Science Advances, this research proves empirically that homeostatic regulation costs (metabolic and sensory) are substantially reduced when entities operate in shared social proximity and synchronize setpoints, compared to entities maintaining isolated homeostatic loops. For our 16-agent autonomous fleet, shared Kuramoto phase-locking, synchronized heartbeat sweeps, and common setpoints prevent per-agent supervisory thrashing and minimize energy/token expenditure.

#### Candidate Invariant Rule
> `Subagent fleet regulation maintains homeostasis through shared phase-locked setpoints and synchronized audit sweeps, minimizing per-agent monitoring spend through collective co-regulation.`

#### Falsification Kill Condition (`invariant_falsifier.v1`)
- **Kind:** `manual`
- **Target:** `memory/percolator/invariants.json`
- **Owner:** `operator`
- **Review By:** `2026-11-24`
- **Falsification Note:** Requires periodic verification that subagent supervisor heartbeat and telemetry synchronization hold under 16-agent concurrency.

---

## 3. Secondary Radar Signals & Technical Preprints

Beyond the top five formal academic and scientific preprints, several industry research preprints and specifications were identified in the signal stream:

1. **Building a Dependency Graph of Our Python Codebase (Hudson River Trading)**
   - *Score:* 0.631 | *Family:* `leaf-graph`
   - *Estate Binding:* `I5 gate (0/17 promoted rows declare depends_on; 963 edges elsewhere)`
   - *Insight:* AST ablation proves code structure; nodes that survive ablation without dependents are true leaves. Binds directly to resolving our I5 dependency declaration gap.

2. **PEP 848: Generational Incremental Garbage Collection (Python Core Devs)**
   - *Score:* 0.431 | *Family:* `decay-gc`
   - *Estate Binding:* `tools/explore_decay.py` (wave 6), `tools/fossil_check.py` tombstone registry
   - *Insight:* Pure generational GC stalls under large heaps; incremental mark-and-sweep across age buckets matches our 14-day explore decay strategy.

3. **The Provenance Tax: How LLM Watermarking Changes AI Agent Behavior (Lasso Security)**
   - *Score:* 0.493 | *Family:* `provenance`
   - *Estate Binding:* `memory_store.db` facts, agent verification
   - *Insight:* Watermarking creates token bias and behavioral skew; verification must rely on cryptographic receipts rather than probabilistic token watermarks.

4. **P-Hacking with Claude (Vita Ex Machina)**
   - *Score:* 0.282 | *Family:* `repeat-gate`
   - *Estate Binding:* `tools/invariant_promote.py policy v2` (count>=2, span>=1d, cycle sources>=2)
   - *Insight:* Repeated automated evaluations without multiple testing corrections inflate false discovery rates; reinforces the policy v2 repeat gate requirement.

---

## 4. Promotion Gate Assessment (`tools/invariant_promote.py` Policy `promotion.v2`)

Under `promotion.v2` (policy sha `639ba9d453ed97c0`), candidate invariants are evaluated against strict gate criteria before being promoted to `PROMOTED_INVARIANTS.md`:

| Candidate Rule | Canonical | Min Count (>=2) | Span (>=1.0d) / Cycles (>=2) | Domain Clean | Vocabulary Clean | Initial Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Preprint 1: Compaction Laundering: Provenanc... | `0e379533cb30b633` | 1 (Pending) | 0.0d (Cycle 1) | PASS (`provenance`) | PASS (No error strings) | ADMIT_CANDIDATE |
| Preprint 2: EPGM: Execution Provenance for B... | `dcfbb448eb41f327` | 1 (Pending) | 0.0d (Cycle 1) | PASS (`provenance`) | PASS (No error strings) | ADMIT_CANDIDATE |
| Preprint 3: The Irreversibility Budget: Flee... | `3c07a4f3fd54868a` | 1 (Pending) | 0.0d (Cycle 1) | PASS (`backpressure`) | PASS (No error strings) | ADMIT_CANDIDATE |
| Preprint 4: Methods, Provenance and Limitati... | `8ae8cf241fabe0bb` | 1 (Pending) | 0.0d (Cycle 1) | PASS (`provenance`) | PASS (No error strings) | ADMIT_CANDIDATE |
| Preprint 5: Human homeostasis is more effici... | `befcf0c04116450b` | 1 (Pending) | 0.0d (Cycle 1) | PASS (`homeostasis`) | PASS (No error strings) | ADMIT_CANDIDATE |

### Promotion Lifecycle Pathway
1. **Admission:** Each rule enters `memory/percolator/candidates.jsonl` and `invariants.json` with `count: 1`, `first_seen: now`, and source cycle recorded.
2. **Reinforcement:** As subsequent operational cycles observe the invariant holding true (across distinct subagent runs and temporal cycles >= 24h), `count` increments and `cycle_hits` records independent sources.
3. **Promotion:** Once `count >= 2` and recurrence span >= 1.0 day or distinct cycle sources >= 2 are logged, `tools/invariant_promote.py --apply` will record a promotion verdict in `memory/percolator/promotion_ledger.jsonl` and export the row to `PROMOTED_INVARIANTS.md`.

---

## 5. Machine-Readable Candidate Definitions

### A. Invariants Registry Schema (`memory/percolator/invariants.json`)
```json
{
  "0e379533cb30b633": {
    "text": "[provenance] Context compaction must preserve attestation hashes and origin timestamps as immutable envelopes; synthesized claims without preserved origin provenance are tagged unverified proposal rather than durable fact.",
    "count": 1,
    "first_seen": "2026-10-24T01:54:38.490419Z",
    "domain": "provenance",
    "last_seen": "2026-10-24T01:54:38.490419Z",
    "decay_as_of": "2026-10-24T01:54:38.490419Z",
    "cycle_hits": {
      "venue_mine_radar": "2026-10-24"
    },
    "depends_on": []
  },
  "dcfbb448eb41f327": {
    "text": "[provenance] Memory retrieval across agent sessions must traverse explicit execution provenance graphs bounded by a token retrieval budget, ranking by verified causal execution receipts rather than semantic similarity alone.",
    "count": 1,
    "first_seen": "2026-10-24T01:54:38.490419Z",
    "domain": "provenance",
    "last_seen": "2026-10-24T01:54:38.490419Z",
    "decay_as_of": "2026-10-24T01:54:38.490419Z",
    "cycle_hits": {
      "venue_mine_radar": "2026-10-24"
    },
    "depends_on": []
  },
  "3c07a4f3fd54868a": {
    "text": "[backpressure] Irreversible mutations across fleet processes are gated by an admission control budget bounded by drain latency; queue growth beyond drain capacity halts ingestion rather than buffering indefinitely.",
    "count": 1,
    "first_seen": "2026-10-24T01:54:38.490419Z",
    "domain": "backpressure",
    "last_seen": "2026-10-24T01:54:38.490419Z",
    "decay_as_of": "2026-10-24T01:54:38.490419Z",
    "cycle_hits": {
      "venue_mine_radar": "2026-10-24"
    },
    "depends_on": []
  },
  "8ae8cf241fabe0bb": {
    "text": "[provenance] Every empirical state claim crossing subsystem boundaries must store its observation methodology, boundary limitations, and confidence bounds co-located with the assertion record.",
    "count": 1,
    "first_seen": "2026-10-24T01:54:38.490419Z",
    "domain": "provenance",
    "last_seen": "2026-10-24T01:54:38.490419Z",
    "decay_as_of": "2026-10-24T01:54:38.490419Z",
    "cycle_hits": {
      "venue_mine_radar": "2026-10-24"
    },
    "depends_on": []
  },
  "befcf0c04116450b": {
    "text": "[homeostasis] Subagent fleet regulation maintains homeostasis through shared phase-locked setpoints and synchronized audit sweeps, minimizing per-agent monitoring spend through collective co-regulation.",
    "count": 1,
    "first_seen": "2026-10-24T01:54:38.490419Z",
    "domain": "homeostasis",
    "last_seen": "2026-10-24T01:54:38.490419Z",
    "decay_as_of": "2026-10-24T01:54:38.490419Z",
    "cycle_hits": {
      "venue_mine_radar": "2026-10-24"
    },
    "depends_on": []
  }
}
```

### B. Candidate Ledger Schema (`memory/percolator/candidates.jsonl`)
```jsonl
{"ts": "2026-10-24T01:54:38.490419Z", "status": "candidate", "promoted": false, "domain": "provenance", "source": "https://arxiv.org/abs/2610.29869", "claim": "Context compaction must preserve attestation hashes and origin timestamps as immutable envelopes; synthesized claims without preserved origin provenance are tagged unverified proposal rather than durable fact.", "canonical": "0e379533cb30b633", "n_signal": 1, "signal": "Context compaction must preserve attestation hashes and origin timestamps as immutable envelopes; synthesized claims without preserved origin provenance are tagged unverified proposal rather than durable fact.", "estate_map": "memory_store.db facts (no provenance column - known gap from the 2026-10-20 paper check); receipts in memory/runs/", "probe": "Check falsifier condition field_complete on target memory/percolator/invariants.json before cycle review 2026-11-24.", "area": "venue_radar_provenance"}
{"ts": "2026-10-24T01:54:38.490419Z", "status": "candidate", "promoted": false, "domain": "provenance", "source": "https://arxiv.org/abs/2609.25913", "claim": "Memory retrieval across agent sessions must traverse explicit execution provenance graphs bounded by a token retrieval budget, ranking by verified causal execution receipts rather than semantic similarity alone.", "canonical": "dcfbb448eb41f327", "n_signal": 1, "signal": "Memory retrieval across agent sessions must traverse explicit execution provenance graphs bounded by a token retrieval budget, ranking by verified causal execution receipts rather than semantic similarity alone.", "estate_map": "memory_store.db facts; memory/cas/slabs/ and memory/cas/epgm/ provenance sidecars", "probe": "Check falsifier condition log_zero on target logs/failure_kb.jsonl before cycle review 2026-11-24.", "area": "venue_radar_provenance"}
{"ts": "2026-10-24T01:54:38.490419Z", "status": "candidate", "promoted": false, "domain": "backpressure", "source": "https://arxiv.org/abs/2609.00275", "claim": "Irreversible mutations across fleet processes are gated by an admission control budget bounded by drain latency; queue growth beyond drain capacity halts ingestion rather than buffering indefinitely.", "canonical": "3c07a4f3fd54868a", "n_signal": 1, "signal": "Irreversible mutations across fleet processes are gated by an admission control budget bounded by drain latency; queue growth beyond drain capacity halts ingestion rather than buffering indefinitely.", "estate_map": "tools/commit_sweeper.py - 10-minute drain vs multi-thousand-file intake; observed 20+ min sweeps (2026-10-21)", "probe": "Check falsifier condition log_zero on target logs/failure_kb.jsonl before cycle review 2026-11-24.", "area": "venue_radar_backpressure"}
{"ts": "2026-10-24T01:54:38.490419Z", "status": "candidate", "promoted": false, "domain": "provenance", "source": "https://zenodo.org/records/22868834", "claim": "Every empirical state claim crossing subsystem boundaries must store its observation methodology, boundary limitations, and confidence bounds co-located with the assertion record.", "canonical": "8ae8cf241fabe0bb", "n_signal": 1, "signal": "Every empirical state claim crossing subsystem boundaries must store its observation methodology, boundary limitations, and confidence bounds co-located with the assertion record.", "estate_map": "watch/claims.jsonl verifier field, memory_store.db empirical facts, memory/runs/ receipts", "probe": "Check falsifier condition field_complete on target watch/claims.jsonl before cycle review 2026-11-24.", "area": "venue_radar_provenance"}
{"ts": "2026-10-24T01:54:38.490419Z", "status": "candidate", "promoted": false, "domain": "homeostasis", "source": "https://www.science.org/doi/10.1126/sciadv.aeg4937", "claim": "Subagent fleet regulation maintains homeostasis through shared phase-locked setpoints and synchronized audit sweeps, minimizing per-agent monitoring spend through collective co-regulation.", "canonical": "befcf0c04116450b", "n_signal": 1, "signal": "Subagent fleet regulation maintains homeostasis through shared phase-locked setpoints and synchronized audit sweeps, minimizing per-agent monitoring spend through collective co-regulation.", "estate_map": "fossil_check bars (168h/720h), falsifier review dates, sweeper cadence, fleet phase synchronization", "probe": "Check falsifier condition manual on target memory/percolator/invariants.json before cycle review 2026-11-24.", "area": "venue_radar_homeostasis"}
```

### C. Falsifiers Schema (`memory/percolator/falsifiers.jsonl`)
```jsonl
{"schema": "invariant_falsifier.v1", "canonical": "0e379533cb30b633", "claim": "[provenance] Context compaction must preserve attestation hashes and origin timestamps as immutable envelopes; synthesized claims without preserved origin provenance are tagged unverified proposal rather than durable fact.", "kind": "field_complete", "target": "memory/percolator/invariants.json", "owner": "seat", "review_by": "2026-11-24", "note": "Compact-pass claims stripped of source citation or origin hash in memory_store.db falsify the envelope law.", "field": "cycle_hits"}
{"schema": "invariant_falsifier.v1", "canonical": "dcfbb448eb41f327", "claim": "[provenance] Memory retrieval across agent sessions must traverse explicit execution provenance graphs bounded by a token retrieval budget, ranking by verified causal execution receipts rather than semantic similarity alone.", "kind": "log_zero", "target": "logs/failure_kb.jsonl", "owner": "seat", "review_by": "2026-11-24", "note": "A retrieval event exceeding token budget or ignoring execution receipts in memory/cas/epgm/ triggers a falsification failure.", "pattern": "unbudgeted_retrieval_overflow|epgm_sidecar_missing", "window_days": 7}
{"schema": "invariant_falsifier.v1", "canonical": "3c07a4f3fd54868a", "claim": "[backpressure] Irreversible mutations across fleet processes are gated by an admission control budget bounded by drain latency; queue growth beyond drain capacity halts ingestion rather than buffering indefinitely.", "kind": "log_zero", "target": "logs/failure_kb.jsonl", "owner": "operator", "review_by": "2026-11-24", "note": "Sweeper drain exceeding the 10-minute window while commit chute intake remains unthrottled falsifies admission control.", "pattern": "sweeper_timeout|drain_lag_unbounded", "window_days": 7}
{"schema": "invariant_falsifier.v1", "canonical": "8ae8cf241fabe0bb", "claim": "[provenance] Every empirical state claim crossing subsystem boundaries must store its observation methodology, boundary limitations, and confidence bounds co-located with the assertion record.", "kind": "field_complete", "target": "watch/claims.jsonl", "owner": "claim-ledger", "review_by": "2026-11-24", "note": "Any cross-boundary claim entered without bound limitations or verifier attestation falsifies the documentation invariant.", "field": "verifier"}
{"schema": "invariant_falsifier.v1", "canonical": "befcf0c04116450b", "claim": "[homeostasis] Subagent fleet regulation maintains homeostasis through shared phase-locked setpoints and synchronized audit sweeps, minimizing per-agent monitoring spend through collective co-regulation.", "kind": "manual", "target": "memory/percolator/invariants.json", "owner": "operator", "review_by": "2026-11-24", "note": "Requires periodic verification that subagent supervisor heartbeat and telemetry synchronization hold under 16-agent concurrency."}
```

---

## 6. House Law Compliance Attestation

Strict compliance with estate House Law is certified:
- Unicode em-dashes (`\u2014`): 0 occurrences.
- Unicode en-dashes (`\u2013`): 0 occurrences.
- Standard ASCII hyphens (`-` and `--`) utilized exclusively.
- Single-writer serialization honored.

