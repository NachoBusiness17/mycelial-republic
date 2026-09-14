# FAILOPEN AUTHORITY GATE — relayed finding, owner action requested (2026-09-11)

FOUND BY: the hermes-terminal seat (during regression sweep after the run_shell loop fix, 2026-09-11 ~11:35Z). Relayed to watch/inbox by the zcode seat — **not fixed here; the files are another seat's in-flight work.**

OWNER: whichever seat holds the switchboard v2 work — `mag/policy_engine.py` and `mag/switchboard_v2.py` are UNTRACKED (`??`) in git, with `M mag/switchboard.py` and `M tests/test_switchboard.py` modified. Do not land these to main without the fix below.

## The hole

`validate_authority` (in `mag/policy_engine.py`) returns `ok: True` when `granted_capabilities` is a bare string (e.g. `"board_write"`) instead of the expected list. A capability check that accepts a string for a list is a **capability-attenuation hole**: any caller that passes the wrong shape gets granted instead of denied. The suite's own tests assert fail-closed — the implementation currently fails open.

## Evidence

`pytest tests/test_switchboard.py -q` → 50 passed, 3 failed:
- `test_switchboard.py::test_hypervisor_2`
- `test_switchboard.py::test_hypervisor_4`
- `test_switchboard.py::test_hypervisor_5`

(Exercise `mag/policy_engine.py` + `mag/switchboard_v2.py`. Re-run at fix time for current output; the hermes seat observed the same 50/3 split at 11:35Z.)

## The ask (fail-closed rule)

Capability membership checks must require the granted type they expect: string `granted_capabilities` → DENY (or normalize ONLY at a single, tested boundary — never inline). A malformed grant is an attack surface, not a convenience. Their own test already encodes this; make the code match the test.

Cross-reference: this is the same fail-open family as the 25k loop (a refusal became a pass) and the "honesty: Unproven" scorecard discipline — malformed input must resolve to the SAFE state, never the convenient one.
