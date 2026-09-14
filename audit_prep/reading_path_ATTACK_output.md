## Finding — what your cell yields

**Disputed:** The "one hour to first true claim" metric is unverifiable due to undefined "true claim" and missing timing instrumentation. The reading path assumes a clear progression from STACK_V1 to tavern, but the actual entry point is fragmented across multiple undocumented files with no timing correlation.

## Evidence — what in the repo supports it (file/shape, no invention)

- Entry fragmentation: `memory/biography/verkle_chain.jsonl` (7,924 lines) contains timestamps but no "claim" classification
- Missing definition: No file defines what constitutes a "true claim" vs false claim
- No timing correlation: Chain knots have timestamps but no measurement of "time to first true claim"
- Multiple entry points: `AGENTS.md`, `docs/ref/RTFM_20260904.md`, `dashboard/static/claim_check.html` all claim to be entry points but none establish the one-hour metric
- No baseline timing: The oldest chain entry (2026-07-10) cannot establish a "first claim" timeline
- Missing instrumentation: No code tracks claim evaluation time or validates truthfulness

## Risk if wrong — what the audit breaks on if this is missed

The audit fails because the falsifier (Matthew Steiniger) cannot falsify a metric that isn't defined. His reproducibility requirement demands concrete definitions and timing measurements. Without a falsifiable "true claim" definition and timing data, the entire reading path claim collapses into unsubstantiated marketing rather than engineering truth.

## The act — the concrete prep step (file/spec/number)

1. Create `audit_prep/CLAIM_METRIC_SCHEMA.md` that defines:
   - What constitutes a "true claim" (3 criteria with examples)
   - How to measure "time to first true claim" (start/stop events)
   - Baseline timing data from the verkle chain (oldest entry: 2026-07-10T17:31:00Z)

2. Add timing instrumentation to `mag/claim_validator.py`:
   ```python
   class ClaimTimer:
       def __init__(self):
           self.start_ts = None
           self.true_claim_ts = None
       
       def record_claim_attempt(self, claim_text: str) -> bool:
           # Check if claim meets "true" criteria
           pass
       
       def get_time_to_first_true_claim(self) -> float:
           # Return seconds from start to first true claim
           pass
   ```

3. Generate timing baseline from existing chain data:
   - Process first 100 chain knots
   - Classify each as "true/false/unknown" claim
   - Calculate actual timing distribution

## Falsifier — what would prove this wrong

- Discovery of existing code that tracks "time to first true claim" with concrete measurements
- Evidence that the one-hour metric was actually measured rather than claimed
- A documented definition of "true claim" that existed before this audit prep
- Timing data showing consistent one-hour achievement across multiple entry points
- Any instrumented claim validation system that predates this audit preparation

If any of these exist, the finding is WRONG and the metric is real rather than invented.