## Finding — what your cell yields
Secrets are cage-bound: provider keys are validated from env, never overridden, and the bundle self-scan enforces hygiene. Operator gates remain stubs; the one trap is trusting stubs as enforcement.

## Evidence — what in the repo supports it (file/shape, no invention)
- Entry file: backend/provider_gateway.py (lines 18–63, 115, 134, 310) — validates X-API-Key against configured env keys; loads env via models.env_load.load_dotenv(override=False).
- Entry file: models/env_load.py (lines 1–30) — loads .env without overriding existing env vars, preventing accidental override.
- Bundle self-scan: audit_bundle/audit_bundle_manifest.md (lines 48, 130–138) — "No default senses (senses live in cage)"; audit readiness 70% due to missing control test and schema documentation.
- The 5MB .env near-miss is documented in audit_bundle_manifest.md as a past risk surfaced by the bundle self-scan.
- Operator gates: keys_gate.py, spend_gate.py, one_stop_gate.py, operator_go_gate.py are missing (per audit_prep/cell_operator_gates_MAP_output.md lines 13, 33, 45).

## Risk if wrong — what the audit breaks on if this is missed
- If the examiner trusts the missing operator gates as real enforcement, the audit will overstate operational safety.
- If env override is allowed, provider keys could be overwritten by accident, breaking cage isolation.
- If the bundle self-scan is not trusted, the examiner may miss the documented near-miss and hygiene gaps.

## The act — the concrete prep step (file/spec/number)
Create a minimal, falsifiable spec for keys-in-cage enforcement:
- File: configs/keys_in_cage_spec.md
- Content: a 3-line spec stating that provider keys are validated from env without override, and that operator gates must be implemented as single-file enforcers with a pass/fail harness.
- Number: one spec file, one falsifier (provider_keys_must_not_be_overridden).

## Falsifier — what would prove this wrong
- Falsifier: run `python -c "import os; os.environ['MAG_GATEWAY_DEFAULT_PROVIDER']='stolen'; from backend.provider_gateway import validate_provider_key; validate_provider_key('fake')"` and observe that the key is still validated against the original env value, not the override.
- If the test passes, the cage holds; if it fails (key accepted as overridden), the cage is breached.
