# PROPOSAL — Three-body T1: authority-boundary doctrine consistency

**Verdict:** Internally consistent in intent. Charter law, the state-machine doctrine, and all 4 staged patches point the same direction: proposals may flow freely, permissions require an operator-gated transition, and every write carries provenance. No patch contradicts the charter or another patch; each maps to a named audit defect. But the doctrine is not yet consistent in effect — enforcement is keyed to provenance strings the pipeline itself never anchors.

**Claims:**

1. The charter line "a roast can become a proposal; it cannot become a permission" is encoded as executable law in patch 1: sensitive-label proposals fail DENIED instead of self-granting AUTHORIZED. — **supports**. Pointer: /patches/fix_authority_label_gate.json, replace block (`if label in ("untrusted-instruction", "external-content"): status = "DENIED"` + embedded LAW comment).

2. The state-machine doctrine's permission core is real and fail-closed where it runs: AUTHORIZED is reached via grant()/confirm() with validate_authority checking status, capabilities, revocation, TTL, and budget fail-closed. — **supports**. Pointer: /board/audit_constitutional_code.md, §1 AUTHORIZED row + §2 (switchboard_v2.py:243; policy_engine.py:267-330).

3. Patch 1's gate consumes a label the live pipeline never assigns: classify() is CLI-only, never called by propose/grant/execute/harness, and the label is caller-settable via propose(authority_label=...). The gate therefore tests a proposer-chosen string, and 5 of 7 labels (incl. agent-generated) still self-grant through the legacy else-branch. — **shows**. Pointer: /board/audit_constitutional_code.md, §1 CLASSIFIED row + §2 ("bypassed via propose(authority_label=...)", else-branch switchboard_v2.py:279) + §4 defect 1.

**Biggest inconsistency:** The doctrine treats authority_label as law, but no layer binds label to truth. CLASSIFIED — the assignment stage — is dead in the live path, and none of the 4 patches re-anchors it. Until label assignment is independent of the proposer, patch 1 gates a self-declared field, and the charter line holds only for honestly-labeled proposals.

**Residual note:** Even with all 4 patches applied, POSTED stays absent from _STATE_MACHINE and CLASSIFIED stays orphaned — the doctrine chain remains 6/7 at its origin stages.
