# W1 REPRINT HARNESS (2026-09-29, MICKEY17 wave 1, lane scripts/test_server_reprint.py)

Ledger return 21 claimed server/README grades more than tests exercise
(replays same-sequence only, no ACTION_FORK) and prescribed
`scripts/test_server_reprint.py` with "the log IS the reprint; every saved
tape becomes a grader". Built and RUN. All results below are pasted from
real executions on 2026-09-29 (repo venv, Python 3.11.15).

## What was built

`scripts/test_server_reprint.py` (runnable harness, NOT pytest; same shape
as `scripts/test_mud_replay.js`: a main that prints PASS/FAIL lanes and
exits 1 on red; zero collection when pytest points at it on purpose).
Drives `server/world.py` (MountainWorld) read-only; server/ untouched.

Three lane groups over one frozen 15-row tape (9 staged actions + 6 ticks;
staged actions apply at the start of the next tick, per the determinism law):

- REPRINT: record a world under the tape, dump its hash-chained log to
  JSONL, build a FRESH world fed ONLY the dumped log (action rows become
  staged actions in seq order, tick rows become ticks), assert per-tick
  node volumes byte-identical, the fresh chain verifies, and the fresh log
  is byte-identical to the tape file it replayed.
- ACTION_FORK: flip ONE verb in the log-derived tape (boil -> valve on the
  action staged for tick 3), replay, assert ticks 1-2 stay byte-identical
  and divergence fires at EXACTLY tick 3 with the nodes named; the flipped
  stage is a typed UNKNOWN_TARGET reject (valve takes pipes, the target is
  a node), so the boil simply never happens.
- CHAIN_CONTINUITY: reopen the log path in a fresh world and append: seq
  resumes at last+1, prev links to the file tip, the grown file verifies.

## Real run (verbatim, exit 0)

```text
    ACTION_FORK @ tick 3: ada boil spring -> valve spring (typed UNKNOWN_TARGET); nodes diverge: crown 2->1, spring -1->0
    consequence: crown 4 vs 3; winner True vs False at tick 6 (win delayed past the tape end)
    reopened log: seq resumed at 16, prev linked to file tip; 15 rows -> 17 rows, chain verifies
PASS  1 R1: the tape lived (9 acks, 6 ticks, 4 verbs, siphon + XOR + WIN @ 5)
PASS  2 R2: dump is the tape (JSONL reloads, chain verifies, disk == memory)
PASS  3 R3: REPRINT from the dump: fresh world, per-tick volumes byte-identical
PASS  4 R4: REPRINT log byte-identical to its tape + fresh chain verifies
PASS  5 F1: ACTION_FORK boil->valve: divergence at EXACTLY tick 3, nodes named
PASS  6 F2: the fork costs the win (record WIN @ 5 sticky, fork never wins)
PASS  7 C1: CHAIN_CONTINUITY: reopened log appends (seq resumes, prev links)

7/7 lanes green
reprint harness: tape 15 rows (9 actions + 6 ticks), fork tick 3, win tick 5
```

Run command: `.venv\Scripts\python.exe scripts\test_server_reprint.py`
(re-run twice during development; identical output both times, exit 0).
Regression guard: `pytest tests/test_server_v0.py -q` still reads
`15 passed in 4.08s`.

## Findings (the claim gap is now graded, and it holds)

- The README's "any (action, tick) interleaving replays byte-identically"
  claim SURVIVES the stronger instrument: replaying purely from the dumped
  log reproduces per-tick volumes AND the full chained log byte-for-byte
  (tape file == reprint file, both chains verify). The log is genuinely
  self-describing enough to be the tape: rows carry user/verb/target/tick,
  and action-before-tick ordering preserves the interleaving.
- The fork is load-bearing and priced: one flipped verb (a single boiled
  unit at tick 3) delays the WIN past the end of the tape (crown 4 vs 3,
  winner True vs False). Divergence lands exactly at the apply tick, not
  before (validation-at-receipt plus staged application is a total order).
- Physics observed, not fabricated: the record run ends with spring at -1
  (deferred gate inflow and the siphon draw both debit spring in the same
  tick). Deterministic and already blessed by test_server_v0's determinism
  laws; noted here because the harness snapshots it in the fork naming
  (spring -1->0). Candidate v1 physics debt, not a harness bug.

## Laws

Em-dash 0 in the harness and this receipt (verified by grep, count 0).
No git commit made; scripts/test_server_reprint.py is the only repo file
added; watch/inbox receipt is the durable copy. No fabricated results:
every quoted line above is from a real run.
