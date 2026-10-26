# B2-56 grounding chain returncode law 2026-09-26

## Verdict

LANDED. The defect is real and is fixed at the design level: the grounding row is now appended AFTER the cycle's fires, and every fired action carries the child exit code (or fire_error for timeout or launch failure) plus the lane state (remaining work + lock age) read before and after the child exited. A crashed driver can no longer leave a clean "firing" row over stranded state; the row says what happened. 6 new tests pass, ratchet NEW=0, live dry-run verified against real state.

## Evidence

- Defect (git f0e992d3e, the bytes B2-07 ran): grounding_chain.py:175 `subprocess.run(act["cmd"], cwd=str(ROOT), timeout=900, shell=False)` with the returned CompletedProcess discarded; :166 `record(actions)` called BEFORE the fire loop, so no outcome could ever reach the row. B2-07's 11:28:14Z row filed over the crashed KeyError fire is the on-disk proof (watch/inbox/burn_wave_20260926/B2_07_grounding_20260926.md).
- Fix: scripts/grounding_chain.py:190-199 cause+evidence comment; :201 `act["state_before"] = lane_state(name)`; :205 `act["exit_code"] = proc.returncode` (nonzero also prints); :210-215 TimeoutExpired or Exception sets `exit_code = None` plus `fire_error`; :217 `act["state_after"] = lane_state(name)`; :218 `record(actions)` moved after the loop.
- lane_state (:155): research maps to `{"remaining": queue_remaining(), "lock_age_s": lock_age(BASE/"run.lock")}`; build maps to build_remaining plus build_lane/run.lock. The post-fire delta falls out of state_before vs state_after with no new state format.
- Docstring (:14-18) documents the additive outcome fields and names the residual: a hard kill of the chain itself mid-fire leaves no row for that cycle; driver state and locks stay ground truth.
- tests/test_grounding_chain.py: 6 passed (0.33s). Nonzero exit recorded with state delta; row-after-fire ordering proven by a marker line the fake child writes before the row appears; FileNotFoundError and TimeoutExpired each recorded with exit_code None plus fire_error; dry mode invents no outcome fields; non-fired actions untouched; lane_state build path.
- Live dry-run 13:13:30Z appended an honest snapshot row (tender_signal, research queue 0, no fires, no outcome fields invented) to watch/inbox/union_fullsend_20260917/grounding_chain.jsonl.
- tools/violation_ratchet.py check --changed: PASS, NEW=0, registered=11.

## Work done

Read grounding_chain.py whole and the B2-07 receipt; grep-verified no code consumes grounding_chain.jsonl (mining and docs only), so additive row fields break no reader; confirmed the working tree was clean against f0e992d3e; rewrote the fire and record path; wrote the regression suite following the tests/lesson_gate_test.py scripts-import convention; ran pytest (6/6), the ratchet gate, and one real dry cycle. Console failure prints preserved for the operator tail. The pre-existing em-dash in the module docstring was cleaned (law compliance, docstring only). No live fired-child proof exists yet: research queue is 0 and build briefs were drained by B2-55, so no real fire could be induced without planting briefs into production state; the fire path is proven by tests with a fake child plus the dry cycle. That gap is filed in the Falsifier, not papered over.

## Falsifier

1. If any future grounding row shows a fired action without exit_code, the law is broken; inspect scripts/grounding_chain.py:201-218.
2. The new path has never recorded a real dead child; the first live nonzero exit or timeout proves or breaks the recording. Until then the fix is fake-child-proven only.
3. Residual by design and documented, not hidden: a hard kill of the chain between fire and record leaves no row; the 900s stale-lock law stays the only net for that case.

## Bibliography closed

scripts/grounding_chain.py (git f0e992d3e base, working tree); scripts/union_fullsend_day.py (lock and SYSTEMS context); tests/test_grounding_chain.py; tests/lesson_gate_test.py (convention); watch/inbox/burn_wave_20260926/B2_07_grounding_20260926.md; watch/inbox/union_fullsend_20260917/grounding_chain.jsonl (4 prior rows plus the new dry row); tools/violation_ratchet.py output; watch/inbox/burn_wave_20260926/QUEUE.md. No web sources used.
