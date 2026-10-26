## Finding — what your cell yields
The grounding wave's truth-gate is mechanically sound but procedurally vulnerable. The second-witness rule for SUPPORTED claims is enforced at post-time, but there's no mechanism to validate witness identity or authority. The system accepts any non-empty witness string, making the truth-gate trivial to bypass.

## Evidence — what in the repo supports it (file/shape, no invention)
mag/grounding_wave.py lines 126-133: SUPPORTED auto-demotes to UNPROVEN only for missing witness string, not witness validity. The code accepts any truthy value: `if verdict == "SUPPORTED" and not witness.strip():`. No verification of witness identity, credentials, or authority exists anywhere in the 267-line file.

watch/GROUNDING_WAVE.jsonl shows 46 legacy-unwitnessed SUPPORTED rows that were grandfathered, proving the system doesn't audit witness provenance retroactively.

## Risk if wrong — what the audit breaks on if this is missed
Matthew Steiniger's abliteration instinct would exploit this immediately: he could post a SUPPORTED claim with witness "admin" or "root" or any string, bypassing the truth-gate's intended security. The wave's entire credibility as a ground ledger collapses when the second-witness rule is just string-length validation.

## The act — the concrete prep step (file/spec/number)
Add witness validation to mag/grounding_wave.py:
1. Implement witness registry (seat-to-public-key mapping) 
2. Require cryptographic signature verification for witness attestations
3. Add `--witness-signature` CLI parameter
4. Auto-demote unverified witnesses to UNPROVEN with clear error messaging

## Falsifier — what would prove this wrong
Demonstrate a verified cryptographic link between witness identity and the claim's domain of authority. Show that any witness string not in the registry fails post() with a specific "unauthorized witness" error rather than auto-demotion.