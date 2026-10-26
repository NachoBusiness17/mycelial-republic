# PA-S1boot-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

The deliverable the **CONTRACT** demands is the **Authoritative State Artifact** (`_latest_scope_card` output), which serves as the single, canonical, immutable snapshot of the current execution context, operational boundaries, and system health invariants.

This artifact is not merely a summary; it is the **signed contract** that authorizes subsequent actions.

***

## The CONTRACT Deliverable: $\text{SCOPE\_CARD\_V(N)}$

The required shape is a structured, multi-sectioned text output adhering strictly to the formatting established in the `_latest_scope_card` function signature. The primary rule is **non-amendment** of the established boilerplate structure, irrespective of the underlying reality.

**Structure Adherence Checklist:**
1.  Header Prefixes (Mandatory).
2.  Section Headings (Mandatory).
3.  Field Key-Value Pairs (Mandatory).
4.  Separators (`\n`, `---`).

### $\text{SCOPE\_CARD\_V(N)}$ Template (The Required Shape)

```markdown
# Mag agent preamble (coarse elephant — not DNA)
# ts=<ISO_DATETIME_UTC> · law=COORDINATION_ELIAS_ROPE

## Contract
- Trust this pack + your task boundary. Do not invent body/keys/status.
- Do not load full residual or chat history. Deep probe only if task requires a path.
- FILE progress as trail drift cores (base_id + locus), not peer chat.
- Remotes: pack+goal only. No T0/T1 private archive paths.

## Base (frozen graph — cite in every drift)
- base_id: <BASE_ID_OR_NO_OPEN_RUN>
- tip: <BASE_TIP_OR_—> · git: <BASE_GIT_OR_—>
- Drift without this base_id is rejected by architecture.

## Goal (if provided)
<GOAL_BLOCK_OR_SENTENCE_OF_DEFAULT>

## L0a Nervous
- body_ok=<PASS/FAIL> integral_ok=<PASS/FAIL>
- dash:8765=<UP/DOWN> · ollama=<UP/DOWN> · smoke=<PASS/FAIL>
- session tip: <SESSION_TIP_SHORT> leaves=<N_LEAVES>
- agent tip: <AGENT_TIP_SHORT> commit=<COMMIT_HASH>
- keys: <KEY_LINE_OR_(none)> · probe before claim seats
- <TIP_LINE_DETAIL>

## Open loops (narrow)
<LOOPS_TXT_OR_EMTPY>

## Trail cores (mid-run — re-inject)
<TRAIL_TXT_OR_EMTPY>

_Worker: complete task from tools + this preamble. Empty findings only after real inspection._
```

***

## Positive Examples (Compliance Confirmed)

Positive examples demonstrate that the system correctly identifies and records a stable operation across all required fields, adhering perfectly to the structural invariants.

### Example P1: Stable Build Trace (High State Integrity)

**Context:** A routine compaction run following a successful integration of minor feature set `B-44`. All known invariants (Base, Goal, L0a) are stable.

**Observation/Output Structure:**
*   **Goal:** Explicitly defined, tied to a Git SHA.
*   **L0a Status:** All indicators are nominal (`UP`, `PASS`).
*   **Trail Cores:** Contains a verifiable, cited locus commit.
*   **Compliance Marker:** The entire block is consistent and non-verbose, only reporting changes against a strong base.

*(Represents the state where a subsequent task can trust the environment.*)

### Example P2: Fresh Start (Minimalist Confirmation)

**Context:** The first execution attempt after a known system reset or cold boot. No established Goal or Base.

**Observation/Output Structure:**
*   **Goal:** Reports the default prompt/placeholder.
*   **Base:** Explicitly reports `(no open run — trail start first)` for `base_id`.
*   **L0a Status:** Reports `(none)` for keys and placeholder descriptions for tips.
*   **Open Loops/Trail Cores:** Both sections are empty, *but* the presence of the empty sections, correctly marked via the boilerplate, proves that the check was run fully.
*   **Compliance Marker:** The successful reporting of **absence** is the proof of compliance.

***

## Negative Examples (Compliance Failure Detected)

Negative examples demonstrate the failure to adhere to the explicit structural or content rules, requiring immediate intervention or rejection of the resulting artifact.

### Example N1: The "Citation Gap" Failure (Base Contradiction)

**Context:** An agent reports a significant breakthrough finding (new `L0a` data) but fails to reference the necessary `base_id` required by the **CONTRACT**.

**Failure Mechanism:** The agent attempts to inject new data *without* updating the mandatory `Base` block, or its narrative implies new findings did not originate from the established lineage.
**Required Correction:** The deliverable *must* be rejected until the `Base` section is updated *and* the failure is logged in the `Open loops` section, citing the missing linkage.
**Failure Signature:** Any claim of forward progress without citing an updated `base_id` or `base_tip` is voided by the system wrapper.

### Example N2: The "Burn-Wave Drift" Failure (Incomplete Scope)

**Context:** An audit run finishes but neglects to populate the `Trail cores` section, suggesting the agent only captured the surface state (`L0a`) but failed to integrate ephemeral, mid-run changes or necessary historical context.

**Failure Mechanism:** The artifact is generated, but critical temporal data (e.g., a transient memory map, a dependency calculation from a prior execution *within* this session) is omitted.
**Required Correction:** The system must trigger a re-evaluation that *forces* the inclusion of the full `Trail cores` content, documenting the **maximum possible historical breadth** required by the scope.
**Failure Signature:** An empty `Trail cores` section when `session tip` shows activity indicates an incomplete snapshot, rendering the artifact suspect.

***

### Summary Mandate

| Constraint | Required Action | Penalty for Failure |
| :--- | :--- | :--- |
| **Structure** | Match the boilerplate template exactly. | Artifact is rejected as non-conforming data. |
| **Base Integrity** | Every drift *must* cite the established `base_id`. | Execution halts; state is rolled back to the last verifiable snapshot. |
| **Completeness** | All terminal sections (`Open loops`, `Trail cores`) must be explicitly populated (even if empty). | The entire deliverable is flagged as 'Incomplete Context'; no downstream processing allowed. |
