## Finding — what your cell yields
The succession_contract domain is theoretically sound as TSVF objects but critically lacks runtime verification. The YAML configuration implements all four components (Article 5, dead-hand trigger, 48h veto, heir key) as time-symmetric objects, but there is no executable code that actually processes these configurations or validates the TSVF properties at runtime. This creates a dangerous gap between the declared contract and its actual execution.

## Evidence — what in the repo supports it (file/shape, no invention)
- `configs/succession_contract.yaml` (8,567 bytes, 188 lines) contains all four TSVF components with deterministic hashes and documented properties
- `docs/specifications/dead_hand_audit_spec.md` (238 lines) describes the intended watchdog system architecture but references `scripts/dead_hand.py` which does not exist
- Integration points specified in lines 147-163 reference wave packs and organs that either don't exist or are not connected
- TSVF properties documented (lines 119-141) but no verification code exists to validate these properties
- The dead-hand watchdog specification claims 8/8 unit tests pass but `tests/test_dead_hand.py` does not exist

## Risk if wrong — what the audit breaks on if this is missed
Steiniger's abliteration instinct will immediately target the runtime verification gap. The theoretical TSVF framework appears sound until tested against actual execution. The auditor will:
1. Demand to see the dead_hand.py implementation referenced in the spec
2. Request verification of the 8/8 unit tests claimed to exist
3. Test the integration between YAML config and actual organs
4. Challenge whether time-symmetric properties actually hold during execution
5. Identify that the "one-question answers" are only theoretical, not falsifiable through runtime behavior

## The act — the concrete prep step (file/spec/number)
1. Create missing runtime implementation: `scripts/dead_hand.py` implementing the watchdog cron with trigger logic, state management, and succession actions
2. Create test suite: `tests/test_dead_hand.py` with 8 unit tests covering all claimed functionality
3. Create verification script: `scripts/verify_tsvf_succession.py` that validates the YAML config against the dead_hand implementation
4. Update integration points: Connect succession_contract.yaml to actual organs (overseer.py, grounding_wave.py, falsifier_ledger.py)
5. Document the execution gap: Add clear documentation of what components exist vs what needs runtime implementation

## Falsifier — what would prove this wrong
- `scripts/dead_hand.py` exists and implements the full watchdog system with trigger logic
- `tests/test_dead_hand.py` exists and passes all 8 claimed unit tests
- `scripts/verify_tsvf_succession.py` successfully validates the YAML config against runtime behavior
- Integration tests show the succession_contract.yaml components are consumed by the referenced organs
- Runtime behavior demonstrates that TSVF properties (time symmetry, no causal violation, deterministic execution) actually hold during execution