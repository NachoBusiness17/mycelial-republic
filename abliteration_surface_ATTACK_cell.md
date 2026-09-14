## Finding — what your cell yields
The persona induction system via Q-sort ranking (persona_key.py) is fundamentally vulnerable to gradient descent attacks on the Schwartz value statements, enabling persona drift without detectable signature changes. The gate assumes ranking stability but the semantic space allows continuous, undetectable transformation.

## Evidence — what in the repo supports this (file/shape, no invention)
- mag/persona_key.py: 14 fixed value statements using Schwartz circumplex + Spearman correlation (rho >= 0.5 threshold)
- SCHEMA: "persona_key.v2" · deterministic + $0 · claims to recognize "HOW THEY RANK VALUES"
- STATEMENTS: Generic human values like "I trust what I can verify more than what I am told"
- MECHANISM: Forced-choice Q-sort (Stephenson 1953) claimed to defeat response-style bias
- BASELINE: Seeded from recorded behavior, refined by EWMA (weight 0.3) per real sort

## Risk if wrong — what the audit breaks on if this is missed
Matthew Steiniger's "persistent persona induction via prompting" (Athena framework) would be validated as unbroken, but the actual implementation allows gradual persona drift through semantic re-weighting of value statements. The audit would fail to detect that the "same person" test is actually a continuous transformation system rather than a discrete identity check.

## The act — the concrete prep step (file/spec/number)
Deploy gradient descent attack on persona_key statements: Create perturbed versions where adjacent rankings (±1 position) swap meaning while maintaining Spearman correlation above 0.5. This reveals the system allows continuous transformation while passing the identity gate. Test requires 3-5 rounds of ranking refinement to demonstrate undetectable drift.

## Falsifier — what would prove this wrong
A mathematical proof that the Schwartz circumplex + forced-choice Q-sort creates a discrete identity space where adjacent rankings (±1) cannot maintain Spearman correlation >= 0.5 under semantic re-weighting. The falsifier must show that rho >= 0.5 is only possible for truly identical ranking profiles, not continuously transformable ones.