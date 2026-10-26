# Route-shape gap diagnosis (HELP_WANTED brief 6)

- Audited: 2026-09-28 by Q-050 frontier gap task-shape audit (queue row Q-050, judge seat).
- Recomputation command: `./.venv/Scripts/python.exe -m mag.gap_map` returned task_shape `route`:
  cheap_calls 2132, cheap_success_rate 0.224, frontier_gap true (bar 0.6, `mag/gap_map.py:35,98`).
  This reproduces the 2026-09-26 live repro named on the board.
- Underlying ledger: `memory/training/cost_ledger.jsonl` (2305 rows parsed 2026-09-28).

## Recomputed split (cheap providers only: ollama / deepseek / deepseek_overmind)

| slice | n | success | rate |
|---|---|---|---|
| all history (what gap_map scores) | 2132 | 478 | 0.224 |
| actual.calls == 0 (churn rows) | 386 | 132 | 0.342 |
| actual.calls > 0 (real attempts) | 1746 | 346 | 0.198 |
| 2026-08 only | 1689 | 211 | 0.125 |
| 2026-09 only | 445 | 269 | 0.604 |
| 2026-09, calls > 0 | 329 | 203 | 0.617 |
| since 2026-09-21 | 151 | 91 | 0.603 |
| since 2026-09-21, calls > 0 | 72 | 39 | 0.542 |

Read: the aggregate 0.224 is dominated by August (1689 of 2132 rows at 0.125). September
recovers to 0.604 (95 percent CI roughly 0.559 to 0.649, straddling the 0.6 bar), carried by
real calls, not zero-call noise (203 of the 269 September successes have calls > 0). The
improvement is real work, but it only marginally clears the bar.

## Provider contrast (route rows, all providers)

ollama 1677 rows rate 0.218 · deepseek 418 rows rate 0.268 · glm 44 rows rate 0.0 ·
deepseek_overmind 39 rows rate 0.051 · grok 32 rows rate 0.0 · mimo 28 rows rate 0.036 ·
xai 4 rows rate 0.0. The frontier seats assigned route work never produced a completed row in
this ledger, so "elevate-frontier" has no supporting record here.

## Failure rows cited (task_id, ts, provider, actual.calls)

Zero-call churn class (2026-08-06 burst, one row every ~6 seconds):
1. tf178cae22b 2026-08-06T21:02:58Z deepseek 0
2. t70ae756ab6 2026-08-06T21:03:05Z deepseek 0
3. tb8cfa7c282 2026-08-06T21:03:11Z deepseek 0
4. tc7e80399eb 2026-08-06T21:03:18Z deepseek 0
5. t4da75905be 2026-08-06T21:03:25Z deepseek 0
6. tdeec3d7efb 2026-08-06T21:03:31Z deepseek 0

Real-call failure class (calls > 0, task reached terminal not-done):
7. te5894a3749 2026-08-06T21:28:23Z ollama 2
8. tdec4cf4b77 2026-08-07T23:03:28Z ollama 1
9. t1b737d0c95 2026-08-07T23:49:23Z deepseek 214
10. t40a6fbf9b0 2026-08-08T11:59:06Z ollama 1
11. t8eb1f8a946 2026-08-08T12:00:42Z ollama 1
12. ta68c68fe98 2026-08-08T12:01:29Z ollama 1
13. t85c63fa5a8 2026-09-01T00:08:47Z ollama 2
14. t03dfbcdd1b 2026-09-01T00:17:25Z ollama 2
15. t60ee0a773d 2026-09-01T00:36:45Z ollama 2
16. t066a6ca171 2026-09-01T00:43:26Z ollama 1

(204 zero-call August failures and 1274 real-call August failures and 176 September failures
exist in total; the 16 above sample both classes and both months.)

## Instrument findings (why the demotion is an accounting artifact)

1. All-history aggregate with no time window (`mag/gap_map.py:72-99`): August fossils demote a
   shape forever after September recovery. The rule as written was applied correctly; the
   quantity it computes is stale-dominated.
2. Zero-call churn rows count toward n and success (`mag/gap_map.py:79-85` reads only provider
   and outcome), and `success` is queue status done (`mag/cost_ledger.py:84`). The janitor shape
   shows the mirror error: 0.842 "cheap-capable" is carried by 45 zero-call rows all marked
   success while its 12 real-call rows score 0.25.
3. `waste_kind: agent_churn` is forced on every failure (`mag/cost_ledger.py:93`), so the board's
   "failure signature agent_churn" carried no churn diagnosis.
4. `route` is the else-branch of a goal-keyword classifier (`mag/cost_ledger.py:32`), so the
   shape is a catch-all bucket of unmarked goals, and its rate partly measures overall queue
   completion, not a route capability.

## Disposition

- Re-promote route to cheap-capable today: NOT yet justified on the numbers (September 0.604
  clears the bar by margin-of-error only; the last-7-day real-call slice sits below it at 0.542).
- Keep route in the frontier-gap stack on today's aggregate: ALSO wrong (it is a fossil measure).
- Correct action: fix the instrument before either verdict (window the aggregate, e.g. 30 days,
  and score only rows with actual.calls > 0). After the instrument fix, re-run gap_map and let
  the fresh number decide promotion. Batch-elevating route to grok is contradicted by the
  provider table (grok 0/32, glm 0/44, xai 0/4).

verdict: ledger-artifact
