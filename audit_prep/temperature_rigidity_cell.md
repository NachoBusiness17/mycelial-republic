## Finding — what your cell yields
The wave's parallelism (width) is **temperature-gated**: each heat band (cold→scarce) in configs/temperature_stacks.yaml maps to measurable timeouts and token budgets via mag/temperature_stack.py, making rigidity an emergent property of the temperature field. The system enforces these constraints at runtime; deviation falsifies the claim.

## Evidence — what in the repo supports it (file/shape, no invention)
- configs/temperature_stacks.yaml defines four bands with explicit parameters:
  - cold: temperature 0.1, timeout_s 300, max_tokens 2048
  - warm: temperature 0.2, timeout_s 600, max_tokens 4096
  - hot: temperature 0.35, timeout_s 900, max_tokens 8192
  - scarce: temperature 0.5, timeout_s 1800, max_tokens 16384
- mag/temperature_stack.py implements TemperatureRegistry and resolves stacks by goal/tag, returning TimingProfile with timeout_s, max_tokens, temperature.
- backend/provider_gateway.py uses temperature=0.2 for provider calls, referencing the stacks.
- configs/local_playbooks.yaml and configs/virtual_desk.yaml reference temperature values matching the bands.
- audit_bundle_manifest.md documents the 480-wide wave capability and sanctioned idle between waves.

## Risk if wrong — what the audit breaks on if this is missed
- The examiner will conclude the system lacks hard reproducibility for wave width and token budgets, violating the house's standing program.
- Without enforced timeouts/tokens per band, the falsifier cannot verify that 480-wide waves behave as claimed under load.
- The identity/substrate coupling claim (Oct-27 Apple Silicon migration) cannot be falsified if temperature gates are not mechanically enforced.

## The act — the concrete prep step (file/spec/number)
Create a verification spec at configs/verifiers/temperature_rigidity_verifier.yaml that:
- Lists each band (cold, warm, hot, scarce) with its resolved timeout_s and max_tokens from mag.temperature_stack.TemperatureRegistry.
- Includes a runtime check: run a 480-wide wave with a goal tagged "[improve]" and assert the resolved stack's timeout_s and max_tokens are applied to every lane.
- Records the resolved stack id and values in state/temperature_rigidity_verifier_latest.json on each run.

File to write: configs/verifiers/temperature_rigidity_verifier.yaml

Example skeleton:
```yaml
schema: mag_verifier.v1
verifier: temperature_rigidity
bands:
  cold:
    stack_id: cold
    expected_timeout_s: 300
    expected_max_tokens: 2048
  warm:
    stack_id: warm
    expected_timeout_s: 600
    expected_max_tokens: 4096
  hot:
    stack_id: hot
    expected_timeout_s: 900
    expected_max_tokens: 8192
  scarce:
    stack_id: scarce
    expected_timeout_s: 1800
    expected_max_tokens: 16384
runtime_check:
  goal_tag: "[improve]"
  assert_stack_applied: true
```

## Falsifier — what would prove this wrong
- A 480-wide wave with goal tagged "[improve]" resolves to a stack whose timeout_s or max_tokens do not match the band's expected values in the verifier.
- Instrumentation shows lanes exceeding the resolved max_tokens or timeout_s for the band.
- The verifier's runtime check fails to assert stack application across lanes.
