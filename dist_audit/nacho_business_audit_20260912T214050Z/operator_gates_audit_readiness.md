## Finding — what your cell yields
The enforcement of the four operator-only gates (KEYS, spend, ONE STOP, operator GO) is not adequately represented in the codebase, leading to potential discrepancies between policy and implementation.

## Evidence — what in the repo supports it
1. **Documentation**: `docs/ref/OPERATOR_GATES_SCHEMA.md` states the existence of policies but notes only two gates implemented in code: `burn_gate.py` and `trust_gate.py`. The remaining gates are merely policy declarations without corresponding enforcement mechanisms.
2. **Code**: In `grok_frontier_loop.py`, the argument `--force` for bypassing the budget/cooldown gate is explicitly labeled as `operator-only`. This indicates the existence of operator-only actions but lacks proper gate implementation for all areas.

## Risk if wrong
If this discrepancy is not addressed, the audit may reveal insufficient gate enforcement, leading to unregulated actions that could compromise governance and integrity of data. This could result in a loss of trust from the auditor and stakeholders in the system's operational fidelity.

## The act
Propose to create the file `docs/ref/OPERATOR_GATES_IMPLEMENTATION.md` which outlines the current enforcement code of all four operator-only gates — describing their intended functionality, current state, and proposing the necessary implementation guidelines or corrections needed to align policy with implementation.

## Falsifier — what would prove this wrong
Providing concrete proof of gate implementations and a fully traceable audit trail that correlates existing code to the stated policies would disprove the claim of inadequate enforcement. Any records showing successful audits conducted under current implementations alongside thorough testing results would suffice.