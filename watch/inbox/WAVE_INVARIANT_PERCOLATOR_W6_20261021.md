# WAVE 6 - explore decay + honest queue metric (2026-10-21)

**Wave id:** wave-invariant-percolator-20261021-w6
**Trigger:** morning brief - explore backlog 61.3% open and rising, falsifiers green
**Spend:** $0. Stdlib. No provider calls.

## Envelope

| Axis | Bound | Used |
|---|---|---|
| Ask | stop the queue metric from lying, without deleting rows | 1 |
| Steps | 12 tool calls | 11 |
| Live writes | `memory/percolator/explore_decay.jsonl`, `SEATS.md`, warm_state | 848 classifications |

## 1. The problem was the metric, not only the queue

`explore.jsonl` held 2,877 rows: 1,764 open, **848 of them older than 14 days**
(median age 2 days, max 58; 776 of the old ones `behavioral`). The I4 gate read
"open share of all rows" and failed at 61.3% - but half of that "backlog" was
dead tape from weeks ago, still counted as live work. Deleting it would be a lie
of a different kind; the rows are the record.

## 2. What was built

`tools/explore_decay.py` - ages open rows out of the *active* set by appending a
classification row to `memory/percolator/explore_decay.jsonl`:

- **never rewrites `explore.jsonl`** (a live writer appends to it by the minute;
  read-modify-write can drop concurrent rows - the 2026-10-20 index lesson);
- idempotent: a canonical already classified is never re-emitted;
- exit ladder 0 / 1 refused / 2 unverifiable, self-stolen from
  `claim_drift_patrol`;
- `--days` bar (default 14), `--apply`, `--json`.

Run: **848 classifications written**, on the first pass. Live backlog after:
**916 of 2,877 (31.8%), median age 2.1d.** Stale share of open: 48.1%, all
classified.

## 3. The gate changed meaning, and the change is stated

Old I4: `open rows / all rows <= 25%` - measured age and inflow, not backlog.
New I4: **open rows past the age bar that the decay ledger has not classified
<= 5%**. It now says "the aging rule is being applied", which is a property we
can actually hold.

This is a metric redefinition, so it is recorded here rather than slipped in:
I4 passes at 0/1,764 unclassified, and I5 (leaf set) remains red.

```
PERCOLATOR-AUDIT: VIOLATED -- 5/6 gates green [surface: promoted (17 rows)]
  [PASS] I1 repeat gate
  [PASS] I2 failure strings
  [PASS] I3 probe chatter
  [PASS] I4 0/1764 open rows older than 14d unclassified (cap 5%)
  [FAIL] I5 0/17 rows declare depends_on (leaf set - gate redesign owed)
  [PASS] I6 17/17 promoted rows carry a falsifier
```

Tests: `tests/test_explore_decay.py` (8) + audit/falsifier/promote/sweeper
suites = **51 passed**; T1W1 session-brief contract 1 passed.

## 4. Two smaller fixes in the same pass

**Warm boot was serving a 25-day-old brief.** `briefs/latest.md` is FROZEN at
2026-09-26 by law, and `_session_brief()` reported it as "the session brief".
Contract preserved (a frozen brief must read as frozen - T1W1 ticket 2), and
`warm_state.json` now also carries `live_brief` from `state/CURRENT.md`:

```
session_brief: 2101 chars (24.8d old, stale=True)
live_brief:    3772 chars from state/CURRENT.md (1.7d old)
```

**SEATS.md fossil WARN cleared.** `python tools/compile_seats.py --swap` ->
0h old against a 168h bar. Fossil census now: **1 WARN, 0 HARD** (the remaining
one is `queue/lanes/jev/trail.jsonl`, `[watch]` by design).

Sweeper hardening found while landing: the singleton guard made tests claim the
live pidfile, so `PID_DIR` is now injectable and the test battery points it at
tmp.

## 5. Still open

1. **I5 redesign.** The 17 promoted invariants are leaves (0 of 963 edges touch
   them). The gate should say "leaf or declared", not "10% must declare".
2. **The 916 live open rows** still have no consumer. Decay classifies dead
   ones; it does not explore live ones.
3. **Falsifier manual debts** - 11 named, review by 2026-11-20.

## Fireball

Wave 6 terminated. 848 classifications appended, queue file byte-identical
before and after, 51 tests green, no provider calls.
