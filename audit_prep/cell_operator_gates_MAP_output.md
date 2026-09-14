## Finding — what your cell yields

**Supported:** Operator gates are defined as doctrine (KEYS, spend, ONE STOP, operator GO) in three places: `RTFM_20260904.md:50`, `dashboard/claim_check.html:63`, and the intake rubric. **Disputed:** Code enforcement is incomplete. Only two gates (burn_gate, trust_gate) are implemented; three core gates (KEYS, spend, ONE STOP) are purely policy with no executable check functions. **The trap:** The existing gates are enforcement-light (burn_gate checks UTC hours; trust_gate is content-policy). The operator-GO gate is documented as deferring builds, but no `operator_go_gate.py` exists to CHECK operator permission before a build launches.

**Reading path for an outsider:** (1) Entry file `docs/ref/RTFM_20260904.md:50` (LAUNCH LAW). (2) Visual contract in `dashboard/static/claim_check.html:63` (card verifier shows the gate rule, not a code implementation). (3) Actual enforcement in `mag/burn_gate.py` and `mag/trust_gate.py`. The three things to check: Does each gate have a `check()` function? Is it called before a build launches? Does it log the gate decision to the verkle chain? The one trap: The HTML dashboard shows the gates as known rules, but no enforcement layer calls them; policy lives in docstrings, not in the swarm worker or governor.

## Evidence — what in the repo supports it (file/shape, no invention)

- `docs/ref/RTFM_20260904.md:50` — "Only operator gates (KEYS/spend/ONE STOP) defer, and the card names the gate." (Policy, not enforcement.)
- `dashboard/static/claim_check.html:63` — "operator gate (KEYS / spend / ONE STOP / operator GO). The gate defers, not the lane." (Visual rule, HTML form validation only.)
- `mag/burn_gate.py` — Exists, implements promo-window check + quota floor; called explicitly with `--force` flag for override. Exit codes: 0=GO, 3=DEFER(window), 4=DEFER(quota).
- `mag/trust_gate.py` — Exists (8.7 KB), content sanity gate; no explicit operator GO check observed in code scan.
- Missing files: `mag/keys_gate.py`, `mag/spend_gate.py`, `mag/one_stop_gate.py`, `mag/operator_go_gate.py` do not exist.
- `mag/law.py:51–81` — DEFAULT_LAWS array lists LAW-1 through LAW-7, none named for operator-gate enforcement.
- `mag/governor.py` and `mag/lane_runner.py` — No grep hits for burn_gate calls or ONE_STOP checks; policy documented, not integrated.

## Risk if wrong — what the audit breaks on if this is missed

Steiniger would flag this as a **ceremony-vs-enforcement gap**. The claim "operator gates are code-as-law constraints" fails when: (a) gates are named in a dashboard, but the swarm worker never reads the dashboard to check them; (b) a build can be authorized by a card that names "ONE STOP" as the gate, but no code interprets or enforces the ONE STOP state; (c) the operator can say "KEYS required" but a build fires anyway if KEYS are not actually checked. The audit verdict: governance theater, not constraint. The verkle chain records a gate name, but the chain doesn't record whether the gate was actually enforced — a falsifiable claim undermined by its own incompleteness.

## The act — the concrete prep step (file/spec/number)

**Minimum prep (72 hours to audit-ready):**

1. Create `mag/gate_dispatch.py` (stub, ~40 lines) that implements:
   ```python
   def gate_check(gate_name: str, task_ctx: dict) -> dict:
       """Dispatch to named gate. Return {ok: bool, reason: str, exit_code: int}."""
       gates = {
           "burn": burn_gate.check,
           "trust": trust_gate.check,
           "spend": None,  # TODO: implement
           "keys": None,   # TODO: implement
           "one_stop": None,  # TODO: implement
           "operator_go": None,  # TODO: implement
       }
   ```
2. Add one test: `test_gate_dispatch_missing_gates.py` → Verify that calling an unimplemented gate returns `ok=False, exit_code=2`.
3. Update `docs/ref/OPERATOR_GATES_SCHEMA.md` (already exists as a frame) to list which gates are implemented vs stubbed.

**This prepares the audit reader to see:** (a) The gates are named and documented; (b) Some are implemented (burn_gate, trust_gate); (c) The rest are known-missing stubs in a single dispatch table; (d) The repo is honest about the gap, not hiding it.

## Falsifier — what would prove this wrong

- Discovery of existing `keys_gate.py`, `spend_gate.py`, `one_stop_gate.py`, or `operator_go_gate.py` files in `mag/` with real enforcement logic (not stubs).
- Evidence that `mag/governor.py` or `mag/lane_runner.py` calls any of the missing gates before launching a build.
- Evidence that the verkle chain records gate-check verdicts (e.g., a knot field `gate_checked=true, gate_name=ONE_STOP, gate_result=DEFER`).
- A test in `tests/` that verifies operator gates are enforced end-to-end (not just documented).

If any of these exist, the finding is **WRONG** and the repo's enforcement is stronger than the evidence shows.
