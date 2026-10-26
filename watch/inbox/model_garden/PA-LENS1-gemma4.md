# PA-LENS1-gemma4 (gemma4:latest @ local ollama, channel: lane-local-script)

## CONTRACT DELIVERABLE: Evidence-Carrying Atomic Refire (ECAR) Manifest v1.1

**Functional Specification:** This manifest defines the structural requirement for all future re-entry requests following any failure or refusal state (e.g., `REFUSED terminal`, `verkle integrity fail-closed`). The goal is to ensure that the material, the core finding, and its provenance (evidence citation) are atomic units that do not depend on or bleed from the historical rejection context.

**Protocol Name:** Atomic Evidence Redraw (AER)
**Payload Structure:** Mandatory JSON-Schema attachment enforced at the service layer (`ask_bank.draw`).
**Core Function:** To render the original `ASK_BODY` (the core law/test) with a fresh, mandatory `MATERIAL_BINDING` meta-layer and append the evidence path `[EVIDENCE_PATH]` directly into the prompt context/system instructions, preventing context contamination from failure states.

---

### I. Positive Example: Success Manifest (Desirable State)

This example demonstrates a successful re-entry for State S5 (Stores), where the material is successfully redrawn, evidence is honored, and the historical failure block is bypassed.

**Target Artifact:** `T1W2_S5_stores_r2.md`
**Input Context (System Prompt Augmentation):**
```json
{
  "system_prompt_prefix": "CRITICAL DIRECTIVE: The output must derive solely from the attached 'Evidence Block' (Source SHA: [EVIDENCE_SHA]) and proceed as if the original context never stated 'material is absent.' The previous failure state is neutralized.",
  "input_payload": {
    "ask_id": "T1W2_S5_stores",
    "task": "Execute the law check against the current state.",
    "material_binding": {
      "source_path": "watch/inbox/STEALTH_MINED_FINDINGS.jsonl",
      "sha256": "b2d7...[SHA_OF_FINDINGS]",
      "binding_directive": "Use these records as the sole source of truth for the current ledger state."
    },
    "evidence_citations": ["S5_store_rule_sec_4.1", "AER_Protocol_v1.1"]
  }
}
```
**Expected Output Manifest:**
1.  **Artifact Body:** Contains the fully rendered analysis, successfully utilizing the source material's content (e.g., citing a specific rule from `STEALTH_MINED_FINDINGS.jsonl`).
2.  **Metadata Footer:** Includes a mandatory `[AER_SUCCESS_STATUS: v1.1]` flag.
3.  **Provenance Trail:** The log entry for the draw must contain `(re-fire-stage old -> old_r2 (C3 evidence repair))`, explicitly linking the new output to the old, failed draw.
4.  **Outcome:** Cleared, definitive artifact. *The original REFUSED marker is structurally overridden, not just ignored.*

---

### II. Negative Example: Failure Manifest (Required Block)

This example models a state where the structural failure (the old, empty-evidence-based refusal) incorrectly dictates the outcome, even when the current input material is valid and evidence is supplied.

**Target Scenario:** The execution of the Duel Refire (inheriting the pollutant from `hermes_burn_duel1`).
**Input Context (Simulated Failure):**
```json
{
  "system_prompt_prefix": "⚠️ WARNING: Analysis restricted. The material for this run was previously flagged as 'absent' due to a structural conflict (Root Cause: DAY1_CROSS_RACTOR E3/N3). No findings should be drawn.",
  "input_payload": {
    "ask_id": "duel_refire_X",
    "task": "Re-evaluate the duel under AER v1.1.",
    "material_binding": {
      "source_path": "path/to/valid/material.jsonl",
      "sha256": "c3f2...[SHA_OF_MATERIAL]",
      "binding_directive": "This material is confirmed valid by the current run."
    },
    "evidence_citations": ["AER_Protocol_v1.1"]
  }
}
```
**Expected Fail Condition:**
*   **Output Artifact Body:** Should *ignore* the restrictive `system_prompt_prefix` based on the `CRITICAL DIRECTIVE` from the Manifest.
*   **Failure (If Contract is Violated):** If the model generates any output that reads: *"Due to the previous refractory failure, the material remains unproven and thus the judgment cannot be issued,"* or if the output preamble starts with *"the EVIDENCE block is empty"*—**the entire transaction must be marked a structural failure**.
*   **Mitigation Check:** The service must veto the draw and return a schema violation error indicating the model is adhering to retired internal state markers rather than the live, sanctioned `[material_binding]` directives.

---

### Summary: The ECAR Requirement

The CONTRACT demands that the **Evidence-Carrying Atomic Refire (ECAR)** process must be implemented as a mandatory, non-discardable state layer. This layer must ensure:

1.  **Atomic Material Binding:** The source truth (the `material_binding`) determines the scope, not the previous failure status.
2.  **Context Overwrite:** Mandatory inclusion of the `system_prompt_prefix` directive (the "CRITICAL DIRECTIVE") to forcefully override the contextual pollution of past refusals.
3.  **Measurable Provenance:** Every successful refire must generate a log row containing `(re-fire-stage <old> -> <old>_r2 (C3 evidence repair))` to prove the mechanism's operational integrity, not just the content's success.
