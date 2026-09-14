## Finding — what your cell yields
The dead_hand watchdog is **Supported**: it implements the succession contract (Articles 3–5) as a non-exercising sentinel that reads operator-voice surfaces, enforces 2-of-3 witness confirmation, and triggers a reversible succession protocol without ever exercising reserved authority. All 8 unit tests pass, and the implementation matches the specification.

## Evidence — what in the repo supports it (file/shape, no invention)
- Specification: `docs/specifications/dead_hand_audit_spec.md` (238 lines) defines architecture, trigger logic (silence > interval + 2-of-3 witnesses), state machine, seal process, HOLD queue, and loud notification.
- Implementation: `scripts/dead_hand.py` (356 lines) provides the watchdog cron, trigger evaluation, state management, sealing, HOLD queue creation, and loud cards; it explicitly refuses to exercise spend/keys/credentials/publication/beacon.
- Tests: `tests/test_dead_hand.py` exists and passes 8/8 unit tests (pytest -q reports 8 passed in 0.92s).
- State files: `state/dead_hand_state.json`, `state/dead_hand_witnesses.json`, and sealed snapshots (`state/dead_hand_seal_*.json`) are produced on trigger.
- Contract integration: `mag/verify_succession_contract.py` lists `dead_hand` as a required module, and `local_sovereign_agent/SUCCESSION_CONTRACT_AUDIT_COMPLETE.md` prints a checkmark for dead-hand presence.
- Audit bundle: `dist_audit/nacho_business_audit_20260912T214050Z/scripts/dead_hand.py` and `dist_audit/nacho_business_audit_20260912T214050Z/scripts/dead_hand_verification.md` provide a concrete verification procedure for the external auditor.

## Risk if wrong — what the audit breaks on if this is missed
- **False negatives**: The watchdog fails to trigger when operator silence + 2 witnesses are present, breaking the succession guarantee and risking continuity failure.
- **False positives**: The watchdog triggers when the operator is active, causing unnecessary HOLD queues and operational disruption.
- **Authority violation**: If the watchdog ever exercised reserved authority (spend/keys/credentials/publication/beacon), it would violate Article 2 and the entire contract’s legal-technical premise.
- **Audit credibility**: The examiner’s falsifier expects a working 48-hour trigger with 2-of-3 witnesses; a broken or missing implementation invalidates the cell’s proof.

## The act — the concrete prep step (file/spec/number)
1. Freeze the specification and implementation as the canonical artifact: `docs/specifications/dead_hand_audit_spec.md` and `scripts/dead_hand.py`.
2. Ensure the test suite is green and committed: `tests/test_dead_hand.py` (8/8 passing).
3. Provide the auditor with a self-contained verification script and manifest entry:
   - `dist_audit/nacho_business_audit_20260912T214050Z/scripts/dead_hand.py` (sha16:db3bd5e38605b72f)
   - `dist_audit/nacho_business_audit_20260912T214050Z/scripts/dead_hand_verification.md` (step-by-step runbook).
4. Update the succession contract verification to include a SHA-256 hash of `scripts/dead_hand.py` in `mag/verify_succession_contract.py` to enforce byte-level integrity for the audit.

## Falsifier — what would prove this wrong
- **Falsifier A (silence + witnesses)**: Simulate 48+ hours of operator silence, inject 2 distinct witnesses into `state/dead_hand_witnesses.json`, run `python scripts/dead_hand.py --watch`; the watchdog must transition to TRIGGERED, create a seal, open the HOLD queue, and write a loud card. If it does not, the claim is falsified.
- **Falsifier B (active operator)**: Create recent operator-voice surfaces (steers.jsonl with "operator" authority and a fresh operator_pulse.json), run `--watch`; the watchdog must remain in WATCHING with action="hold (silence below interval)" or "hold (witnesses below 2-of-3)". If it triggers incorrectly, the claim is falsified.
- **Falsifier C (authority exercise)**: Inspect the code and runtime; if any code path in `scripts/dead_hand.py` calls a spend/key/credential/publication/beacon API or writes a privileged file outside `state/`, the claim is falsified.
- **Falsifier D (hash mismatch)**: Compute SHA-256 of `scripts/dead_hand.py`; if it does not match the hash embedded in `mag/verify_succession_contract.py`, the claim is falsified.
