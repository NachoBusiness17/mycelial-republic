# wave_receipts_READING_GUIDE.md

## Finding — what your cell yields
The wave_receipts domain is the **lane-level failure log, token accounting, and integrity ledger** for the 480-wide wave proof. It is the **annalea standard applied**: every lane's receipt is a falsifiable claim that the lane executed within the temperature stack's constraints, producing a verifiable hash-chain artifact.

## Evidence — what in the repo supports it (file/shape, no invention)
- **Entry file**: `audit_prep/wave_receipts_schema.json` (lines 1-23) defines the `mag.wave_receipt.v1` schema with required fields: `schema`, `ts`, `wave_width`, `lane_id`, `goal`, `resolved_stack`, `timeout_s`, `max_tokens`, `temperature`, `lane_hash`, `verifier_pass`.
- **Shape**: `memory/runs/*/receipts.jsonl` files contain `harness.receipt.v1` records with `event_id`, `status`, `ts`, and `receipt_path` fields (e.g., `C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/receipts.jsonl` lines 1-20).
- **Temperature stack enforcement**: `mag/temperature_stack.py` lines 78-260 defines `TemperatureStack` and `registry().resolve()` which computes the resolved stack for a goal, including timeout, max_tokens, and temperature. The `lane_hash` is computed as a SHA-256 hash of the lane's resolved stack and parameters (see `_leaf_hash` function lines 277-279).
- **480-wide wave test**: `test_480_wave_temperature.py` lines 1-112 simulates a 480-wide wave with `[improve]` tag, verifying that all lanes resolve to the same improve stack and enforcing runtime constraints. The `verifier_pass` field is computed as `all_match and runtime_check_pass` (line 84).
- **Pointer knots**: `mag/temperature_stack.py` lines 125-335 defines `PointerKnot` and `_leaf_hash` which produces the `lane_hash` as a SHA-256 hash of the pointer payload, ensuring Verkle-style integrity.

## Risk if wrong — what the audit breaks on if this is missed
- **Entropy-minimization narrative (EUT frame)**: Missing or inconsistent receipts will cause Matthew Steiniger to reject the claim that the 480-wide wave scales without bespoke runners per pack. The examiner expects **hard reproducibility** — scripts and figures ride every record. Without receipts, the audit cannot falsify the scaling law.
- **Hard reproducibility requirement**: The examiner strips safeguards to see what emerges. If receipts are missing or do not contain the required fields (`lane_hash`, `verifier_pass`), the audit will fail the reproducibility gate.
- **Identity/substrate coupling**: The lane_hash is a Verkle-style pointer that must chain into the verkle chain. Missing or incorrect lane_hash breaks the chain's integrity, causing the examiner to reject the entire wave proof.

## The act — the concrete prep step (file/spec/number)
Create `audit_prep/wave_receipts_READING_GUIDE.md` with the following content:

---

## wave_receipts domain — outsider's reading guide

### Entry point
- **File**: `audit_prep/wave_receipts_schema.json`
- **Shape**: JSON Schema `mag.wave_receipt.v1` with required fields: `schema`, `ts`, `wave_width`, `lane_id`, `goal`, `resolved_stack`, `timeout_s`, `max_tokens`, `temperature`, `lane_hash`, `verifier_pass`.
- **Example receipts**: `memory/runs/*/receipts.jsonl` (e.g., `memory/runs/receipts.jsonl` lines 1-20).

### Three things to check
1. **Schema compliance**: Every receipt must validate against `mag.wave_receipt.v1` (see `audit_prep/wave_receipts_schema.json`).
2. **Temperature stack enforcement**: Verify that `resolved_stack` matches the expected stack for the goal (e.g., `[improve]` tag resolves to the `improve` stack in `configs/temperature_stacks.yaml`). Check that `timeout_s`, `max_tokens`, and `temperature` are within bounds.
3. **Integrity hash**: Confirm that `lane_hash` is a SHA-256 hash of the lane's resolved stack and parameters (see `mag/temperature_stack.py` lines 277-279). This ensures Verkle-style chain integrity.

### One trap
- **Missing receipts or incorrect `lane_hash`**: The examiner will immediately detect missing pack files or incorrect hashes. Ensure that every lane's receipt is committed and that the `lane_hash` is computed correctly from the resolved stack and parameters. Do not fabricate receipts.

---

## Falsifier — what would prove this wrong
- **Missing pack files**: If the examiner cannot locate the claimed pack files for the width ladder (e.g., `audit_prep/fanout_organ_width_ladder_receipt.md` claims 9 specific pack files but they are missing), the 480-wide scaling claim is falsified.
- **Incorrect `lane_hash`**: If the `lane_hash` does not match the SHA-256 hash of the lane's resolved stack and parameters, the integrity claim is falsified.
- **Failed `verifier_pass`**: If `verifier_pass` is `false` for any lane, the wave proof fails the falsifier gate.
- **Missing required fields**: If any receipt lacks a required field (e.g., `lane_hash`, `verifier_pass`, `resolved_stack`), the audit fails the hard reproducibility requirement.
