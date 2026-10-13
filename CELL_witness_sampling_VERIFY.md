## Finding — what your cell yields
The witness_sampling domain implements a **statistical honesty engine** that treats stranger-witnesses as sampling agents and machine verdicts as sampled data points. The system achieves statistical significance through correlation-adjusted effective witness counting (n* = n/(1+(n-1)ρ)), ensuring that N correlated witnesses don't artificially inflate confidence. The core innovation: witness independence is measured, not assumed.

## Evidence — what in the repo supports it (file/shape, no invention)
- `mag/memweave.py` (lines 130-180): Implements `consensus()` function with correlation-adjusted effective witness formula n* = n/(1+(n-1)ρ), converting raw witness count to evidential weight
- `mag/ox_resident.py` (line 88): Explicitly states "agreement is only real in proportion to error independence; n* = n/(1+(n-1)ρ) effective witnesses, not N opinions"
- `mag/grounding_wave.py` (267 lines): Implements v3 truth-gate requiring dual witness verification for SUPPORTED claims, with evidence path validation and hash-chain verification
- `watch/GROUNDING_WAVE.jsonl` (113 posts): Contains 11 witnessed SUPPORTED posts and 46 legacy/unwitnessed SUPPORTED posts (auto-demoted to UNPROVEN), demonstrating the sampling mechanism in action
- `handoff/OX_RESIDENT_*` files (multiple): Contain extensive reasoning about consensus-illusion detection and effective witness mathematics
- `CELL_canary_witness_VERIFY.md`: Shows stranger-witness concept applied to drift detection on operator surfaces

## Risk if wrong — what the audit breaks on if this is missed
Matthew Steiniger's EUT theory demands "hard reproducibility" and "abliteration" (stripping safeguards). If the witness sampling mathematics are flawed:
- The correlation-adjusted formula (n*) could be mathematically invalid, making the entire statistical foundation collapse
- Stranger-witness independence assumptions could be unfalsifiable, violating his "falsifiable claims" requirement
- Machine verdicts might appear statistically significant when they're just correlated noise, breaking the "entropy minimization" principle
- The audit would discover the system's confidence intervals are mathematically unsound, invalidating all SUPPORTED claims

## The act — the concrete prep step (file/spec/number)
Create `audit/witness_sampling_mathematics.v1.md` containing:
1. **Mathematical Validation**: Prove n* = n/(1+(n-1)ρ) reduces to correct edge cases (ρ=0→n*, ρ→1→1)
2. **Independence Specification**: Define "stranger-witness" as (a) no shared training data, (b) different prompting strategies, (c) divergent reasoning paths
3. **Sampling Rate Schema**: Document current witness distribution (11 witnessed vs 46 legacy claims in grounding_wave)
4. **Machine Verdict Protocol**: Define how automated judgments are sampled and weighted
5. **Falsification Test**: Create script that injects correlated witnesses and verifies n* adjustment works correctly

## Falsifier — what would prove this wrong
- **Mathematical Counterexample**: Demonstrate n* formula produces impossible values (e.g., n* > n for ρ < 0)
- **Independence Violation**: Show two "stranger-witnesses" share >60% token overlap or identical reasoning traces
- **Sampling Failure**: Inject 100 witnesses with ρ=0.8 and show n* doesn't converge to expected ~1.25
- **Machine Verdict Bias**: Prove automated verdicts systematically favor certain claim types regardless of evidence
- **Correlation Blindness**: Present N=10 witnesses with ρ=0.9 that should yield n*≈1.17 but system treats as n=10