# BURN rsi-harness _d - 2026-09-26

## Verdict
steal

## Evidence
- tools/workflow_gate.py docstring, birth trace: "Born 2026-09-25 by operator order: we need to stop pinging me for workflows, we need to have a gate that makes sure workflows are being improved, enhanced, dogfooded, and using our systems like Mickey17 gophers, interagent communication and steering. Self steal."
- Gate code: `failed.append(cid)` per hard check; `verdict = "PASS" if not failed else "FAIL"`; exit 2 on any fail. G6 exception (t69): a soft finding stays "out of the failed set", "not a hard block".
- t69 comment: "dated-stamp requirement behind G6... soft-false WARN row... never a new hard-block exit." No scenario pass record accompanies the change.
- AGENTS.md line 106: "the one-time user approval is the harness contract, the gate is what keeps it rare." No rollback note, no runtime pair, no scenario set.
- Web search 2026-09-26 ("AI governance amendment drill tabletop exercise retroactive policy testing September 2026"): zero admissible results (SEC tokenization, campus emergency tabletops, a law-firm page). Owed, unsynthesized. Third straight pass the web gave nothing.

## Steal or Vacuous
Steal: the live amendment drill. LAW-12 checklist (from _c) run retroactively against the workflow gate:

1. Scenario cards: FAIL. The motivating trace exists (operator's rejected-confirmation ping, quoted in the docstring) as prose only. No versioned card (persona/goal/expected tools/end state) minted from it. No trace pointer, no card.
2. Non-compensatory admission: HOLDS, 6 of 7. Any hard-failed check forces FAIL/exit 2 regardless of the rest. Caveats: G6 is soft since t69, so any-zero-fail is not total; and the axes are dogfood axes, not LAW-12's five. trace_provenance, eval_independence, cost_honesty, rollback_safety are absent from the gate's own checks.
3. Dual-runtime or rollback note: FAIL. Single runtime (regex over script text), no rollback story.
4. Incumbent-stays-default: HOLDS for gate subjects. Failed submissions exit 2 and file FAIL rows in memory/workflows/REGISTRY.jsonl, so the failed proposal is filed, never half-landed. Unexercised for the gate itself: it predates its own checklist.
5. Regression criterion: FAIL. No scenario set to re-run on gate change; the gate already self-amended (t69) with zero scenario records. The gate of the gate does not exist.

Score: 3 of 5 items the real amendment would have failed. That proves LAW-12 non-vacuous (it would have blocked a working gate) and exposes the genesis gap: every gate is born before its gate exists, so generation zero is structurally ungated and self-amendments like t69 land outside any gate.

## Falsifier
Pre-registered genesis clause: LAW-12 passes only if, within 14 days of registration, one scenario card per G1-G7 is minted from real REGISTRY.jsonl FAIL rows and workflow_gate.py re-passes all seven on a sample gated script; the clause dies if cards cite no FAIL row or a soft-warn recurs on a hard check without a scenario record.

## Bibliography
1. watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md s4, read 2026-09-26
2. memory/law/registry.json, read 2026-09-26 (LAW-12 unregistered)
3. watch/inbox/BURN_rsi-harness_20260925.md, _b.md, _c.md, read 2026-09-26
4. tools/workflow_gate.py, read 2026-09-26
5. AGENTS.md line 106, read 2026-09-26
6. Web search 2026-09-26, query quoted in Evidence; no admissible source, owed
