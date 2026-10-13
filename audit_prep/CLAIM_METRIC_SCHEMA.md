## Claim Metric Schema for External Audit

### Purpose
Define and instrument the "one hour to first true claim" metric for falsifiable verification by Matthew Steiniger.

### Definition of "True Claim"
A chain knot represents a "true claim" if it meets ALL THREE criteria:

1. **Dominant Theme Present**: `dominant_theme` field is not null
2. **Tension Engagement**: `tension_index` > 0.5 (numeric, not string)
3. **Operational Language**: Filename or dominant_theme contains operational terms:
   - build, launch, verify, audit, deploy, check, gate
   - or equivalent system action vocabulary

### Measurement Protocol
- **Start Event**: First chain knot entry (`ts` field)
- **Stop Event**: First knot meeting all three "true claim" criteria
- **Metric**: Time difference in hours between start and stop

### Current Baseline (from verkle chain analysis)
- **First 100 knots**: 0 true claims found
- **Implication**: The "one hour to first true claim" metric is currently UNVERIFIABLE
- **Missing**: Instrumentation to track claim evaluation timing

### Required Artifacts for Audit Readiness

1. **Claim Validator** (`mag/claim_validator.py`):
   ```python
   class ClaimTimer:
       def record_claim_attempt(self, claim_text: str) -> bool:
           # Apply the three criteria
           pass
       
       def get_time_to_first_true_claim(self) -> float:
           # Return hours or None if no true claim found
           pass
   ```

2. **Timing Integration**: Add claim timing to verkle chain knots when a true claim is detected

3. **Test Suite**: Verify the three criteria against known true/false examples

### Falsification Conditions
The metric is PROVEN WRONG if any of these exist:
- Existing timing data showing consistent one-hour achievement
- Prior definition of "true claim" (pre-dates this audit prep)
- Instrumented claim validation system from before 2026-09-13
- Evidence that the one-hour metric was actually measured rather than claimed

### Current Status: DISPUTED
The "one hour to first true claim" metric cannot be verified with existing data and definitions. The claim appears to be aspirational rather than measured.