# PROBE 1 - three-ledger join - first internal price rows
moment: 2026-10-09T03:01:14.467299+00:00
rows: usage 3038, ledger 705, smith 2

| day | cost_usd | tokens | steal | green | vacuous | other | free_gb |
|---|---|---|---|---|---|---|---|
| 2026-09-25 | 0.00 | 0 | 22 | 1 | 0 | 0 |  |
| 2026-09-26 | 0.00 | 0 | 80 | 1 | 0 | 436 |  |
| 2026-09-27 | 0.00 | 0 | 65 | 14 | 2 | 27 |  |
| 2026-09-28 | 0.00 | 0 | 43 | 6 | 6 | 2 |  |
| 2026-10-01 | 37.76 | 4368123 | 0 | 0 | 0 | 0 |  |
| 2026-10-02 | 1.17 | 241281 | 0 | 0 | 0 | 0 |  |
| 2026-10-03 | 25.62 | 4340905 | 0 | 0 | 0 | 0 |  |
| 2026-10-04 | 26.29 | 5011722 | 0 | 0 | 0 | 0 |  |
| 2026-10-05 | 3.76 | 760394 | 0 | 0 | 0 | 0 |  |
| 2026-10-06 | 0.03 | 17380 | 0 | 0 | 0 | 0 |  |
| 2026-10-07 | 0.10 | 100218 | 0 | 0 | 0 | 0 |  |
| 2026-10-09 | 0.00 | 0 | 0 | 0 | 0 | 0 | 458.1 |

## The first price rows
- total measured cost: $94.74 over 12 days
- green verdicts: 22, steal: 210, vacuous: 8
- dollars per GREEN verdict (all-time): $4.31
- dollars per STEAL verdict (all-time): $0.45
- cost on green-verdict days only: $0.00 across 4 days
- cost on vacuous-bearing days: $0.00 across 2 days

## Gaps (a missing column is itself the finding)
- smith rows exist only from 2026-10-09: GB/day rates need the daily cadence to accumulate
- usage ledger covers Hermes-paid dispatch only; free-lane and account burn are separate ledgers (the join shape holds, the source list widens)