# Audit-shape gap diagnosis (HELP_WANTED brief 7)

- Audited: 2026-09-28 by Q-050 frontier gap task-shape audit (queue row Q-050, judge seat).
- Recomputation command: `./.venv/Scripts/python.exe -m mag.gap_map` (deterministic, $0) returned
  task_shape `audit`: cheap_calls 3, cheap_success_rate 0.0, frontier_gap true (bar 0.6, `mag/gap_map.py:35,98`).
- Underlying ledger: `memory/training/cost_ledger.jsonl` (2305 rows parsed 2026-09-28).

## The 3 audit rows (all cited)

| task_id | queue_id | ledger line | ts (2026-08-10) | provider | actual.calls | success | waste_kind |
|---|---|---|---|---|---|---|---|
| tec805beaff | q25726fe418 | 292 | 12:47:39Z | deepseek / deepseek-v4-flash | 0 | false | agent_churn |
| t69d813769c | qc1f90b2877 | 315 | 13:30:45Z | deepseek / deepseek-v4-flash | 0 | false | agent_churn |
| tfc4f1e0826 | q2a3a98630f | 316 | 13:32:25Z | deepseek / deepseek-v4-flash | 0 | false | agent_churn |

Verified per row by direct parse: `actual.calls: 0`, `actual.prompt_tokens: 0`,
`outcome.success: false`, `outcome.leaf_kind: "none"`. All three sit in a 45-minute window.

## What the rows actually were

Queue items recovered from the purge archive
`memory/runs/orchestrator/purged/purge-failed-20260810T134554Z/` (purged 2026-08-10T13:45Z,
13 minutes after the last row):

- q25726fe418: a RESEARCH goal on context-growth management and self-steal capability
  utilization; the word "audit" appears inside the prose, which is what assigned depth=audit
  (`mag/cost_ledger.py:32` classifies depth by goal substring: `"audit" in lowered`).
- qc1f90b2877: a janitor loop-escalation about a stale verkle tip ("Run verkle audit"), tier filler.
- q2a3a98630f: a deep research + codebase audit escalation (from xai), tier filler.

All three share the failure context `tool=write_file detail=false-success: claimed edits, wrote
nothing` in the queue record. All three are tier filler. None is an audit-shaped task that the
cheap system attempted and botched.

## Why the 0.0 rate is not a capability signal

1. `outcome.success` records queue status `done` (`mag/cost_ledger.py:84`), not model success.
2. `waste_kind: agent_churn` is the forced label for every not-done task
   (`mag/cost_ledger.py:93`: `None if success else "agent_churn"`), so "all agent_churn" is
   tautological, not a churn diagnosis.
3. Zero actual calls on all 3 rows: the ledger never observed a real model attempt at
   audit-shaped work, so 0.0 measures churn, not capability.
4. The shape label itself is a goal-text substring artifact (`mag/cost_ledger.py:32`), so these
   3 rows are not even one task type.
5. n=3 with n>=2 qualifying threshold (`mag/gap_map.py:90`): the shape qualifies for demotion on
   the smallest possible sample, all of it from a single morning in August.

## Disposition

- Re-promote to cheap-capable: NOT supported. There is no completed audit-shaped row to prove
  capability either. The shape is unmeasured, not gapped and not cheap-proven.
- Elevate-frontier: NOT supported by the same ledger. Route-shaped rows assigned to grok went
  0/32, glm 0/44, xai 0/4 (all-provider route table in the sibling artifact
  `route_gap_diagnosis.md`), so elevation has no demonstrated record here either.
- Correct disposition: exclude the audit shape from the frontier-gap elevation stack until the
  ledger holds at least one audit-shaped row with actual.calls > 0. The demotion stands only as
  "insufficient data", which is the allowed word below.

verdict: starved
