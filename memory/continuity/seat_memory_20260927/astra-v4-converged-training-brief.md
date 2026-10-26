---
name: astra-v4-converged-training-brief
description: ASTRA v4 frontier-tier training brief CONVERGED through 4
  iterations (2026-09-17→18) — RS-DPO+HyPO, GraphFilter train-only, sealed-first
  curator, three-family harness audit with real exploit tickets, budget-matched
  eval, causal bias report, dead stubs banned; ready for astra dispatch
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

ASTRA v4 training brief CONVERGED through 4 iterations (2026-09-17→18, commits 52d0dba20 + related). The spec for turning fleet receipts into a local gemma-class adapter that emits gate-passing design directions.

**Spine (fixed order, do not skip):**
harness_audit → curator (sealed-first, diagnose→repair→GraphFilter select) → validate → QLoRA SFT → RS-DPO+HyPO (sample k=4, score with real R, drop ties, HyPO on pairs; <20 pairs → GRACE-KTO) → GRPO+ACR/AVSPO (group 8–16, path depth logged) → budget-matched eval vs champion → canary promotion with rollback.

**What v4 added over earlier versions:**
- RS-DPO is the pairing recipe, not a DPO replacement
- GraphFilter on train only, after sealed 10 carved
- Dead stubs (`pass: False`, `done_when in text`) banned in the float
- Harness audit three families with REAL exploit tickets (modify test assertion, return True from fence, suppress failure log) — any accept → EXPLOITABLE, stop
- Curator: sealed-first, diagnose→repair→GraphFilter select; mix targets 40/35/15/10 (promote/reject/near-miss/re-derive)
- Causal bias report mandatory (selection, measurement, label, gate, blind spots)
- Budget-matched eval: calibration report-only, cannot become the ship metric
- Sherpa compiled to the ticket schema (rank, decompose, basis vectors, one ticket or REJECT)

**Reward function:** `R = gate_pass × format_ok × rederive_ok × clarification_zero × sandbox_ok` — no learned reward model, no model-as-judge.

**Files:** watch/inbox/astra_v4/ (brief + prompt) + ASTRA_V4_STATUS.md. Ready for dispatch to the astra seat via chat_provider. **Constitutional amendments A1/A2/A3 bound (see [[astra-constitutional-amendments]]).** Related: [[hermes-100-spend-plan-20260917]], [[the-librarian-fleet-imprint-20260917]], [[external-desk-corpus-steal-20260917]].
