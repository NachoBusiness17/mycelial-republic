# WAVE RECEIPT - invariant percolator, wave 4 (kill conditions; first live bite)

> **RETRACTION (wave 5, 2026-10-20T22:05Z): the two FAILs below are false positives.**
> The matching log rows carry `phase: "escalate"`, and that phase is written in
> exactly one place: `mag/decision_framework.py:230`, inside `escalate_on_loop`.
> Each "failure" was therefore the *escalation firing*, not the steer being
> ignored. Measured across 30 days: 51 loop pairs, **max 2 distinct nudges per
> pair**, which is precisely the collapse detector's designed budget before it
> escalates (`mag/agent_cli.py:1718-1790`). The false `log_zero` falsifier was
> replaced by `nudge_budget` and the lint is now green. Details:
> `watch/inbox/WAVE_INVARIANT_PERCOLATOR_W5_20261020.md`. The rest of this
> receipt stands.

**Wave id:** wave-invariant-percolator-20261020-w4
**Parent:** `watch/inbox/WAVE_INVARIANT_PERCOLATOR_W3_20261020.md`
**Fired:** 2026-10-20T21:34Z
**Mode:** Standing Wave Protocol - one ask, bounded steps, $0, no provider calls
**Mutation:** new falsifier file, regenerated export, new lint tool. No registry write.

## Envelope

| Axis | Bound | Used |
|---|---|---|
| Ask | give all 17 promoted invariants a stated kill condition, and run it | 1 |
| Steps | 12 tool calls | 11 |
| Spend | $0 | $0 (stdlib only) |
| Live writes | `memory/percolator/falsifiers.jsonl`, regenerated `PROMOTED_INVARIANTS.md` | 17 entries |

---

## 1. Every promoted row now has a kill condition

`memory/percolator/falsifiers.jsonl` - schema `invariant_falsifier.v1`, one entry
per promoted canonical, four kinds:

| kind | meaning |
|---|---|
| `log_zero` | rows matching `<pattern>` in `<target>` within `<window_days>` must be 0 |
| `file_absent` | `<target>` must not exist |
| `field_complete` | every row in `<target>` must carry a non-empty `<field>` |
| `manual` | unmeasured by design: names an owner and a review date |

`tools/falsifier_lint.py` runs them with the estate's tri-state ladder:
**PASS / FAIL / UNMEASURED**, exit 0 / 1 / 2. A `manual` entry is never counted as
a pass; coverage (every promoted row has some entry) is reported apart from
correctness (the check actually passing).

## 2. The first live bite

```
FALSIFIER-LINT: FAILED -- 17 promoted, 4 PASS / 2 FAIL / 11 UNMEASURED (coverage 100.0%)

[PASS] a77444ce log_zero        0 hits in 7d
       [steer] Verify with git diff / actual file bytes before declaring done.
[PASS] 368a0fee log_zero        0 hits in 7d
       [steer] Verify via OUR systems before declaring done.
[PASS] 997e65e9 field_complete  6/6 rows carry 'verifier'
[PASS] ff96a7ed file_absent     absent: logs/training_events.jsonl
[FAIL] be509348 log_zero        4 hit(s) in 7d, latest 2026-10-17T15:42:38Z
       [steer] Escalate to next tier; stop token bleed.
[FAIL] 74dbeef7 log_zero        4 hit(s) in 7d, latest 2026-10-17T15:42:38Z
       [steer] Escalate to the next smarter tier; stop local token bleed.
```

Two doctrine invariants are **falsified by the last seven days of the fleet's own
log**. The hits are `run_shell:46d11cf8108d`, "5x identical run_shell calls",
provider deepseek, sessions `orc-t8e96382427` (14:39) and `orc-t48b3fe6ddb`
(15:42). Two real loops, counted twice: the duplicate `log_failure` in
`operator_inbox.py` (documented in `memory/working.md`) wrote each event twice -
timestamps 14:39:41.915 / .085 and 15:42:38.417 / .461. **Raw 4, deduped 2.**

That is the surface doing its job: the first falsifier run found the escalation
steer being violated in practice, not a hypothetical.

## 3. The 11 manual debts are named, not hidden

Each carries an owner and `review_by 2026-11-20`: accepted decision records
immutable (no id field in `decisions_log.jsonl` to detect rewrites), owner/purpose
register, generation-closure rollback, alert dedup, deterministic candidate rule,
rollback scope, deletion reachability, trust-boundary attestation, deliberate-ask
contract, permission-asking, smoke-test claim.

They are explicitly *debts*: `UNMEASURED` never rolls up into a pass.

## 4. Consumer surface now shows the kill condition per row

`PROMOTED_INVARIANTS.md` regenerated: 17 rows, 3,220 bytes, new column.
Header line: `Kill conditions: 6 checkable, 11 manual debts, 0 missing.`

## Audit after wave 4

```
PERCOLATOR-AUDIT: VIOLATED -- 4/6 gates green [surface: promoted (17 rows)]
  [PASS] I1 repeat gate      [PASS] I2 failure strings
  [PASS] I3 probe chatter    [PASS] I6 17/17 promoted rows carry a falsifier
  [FAIL] I4 explore backlog  1489/2602 open (57.2%)
  [FAIL] I5 depends_on       0/17 (leaf set)
```

Tests: **35 passed** across `test_falsifier_lint.py` (9),
`test_invariant_promote.py` (15), `test_invariant_percolator_audit.py` (11).

## What wave 5 should do (ranked)

1. **Fix the loop the falsifier found** - `run_shell:46d11cf8108d` is a real
   escalation failure, not a metric artifact. The steer exists; the behaviour did
   not follow it. Separate lane.
2. **Dedupe in `log_zero`** - a `dedupe_ms` window so duplicate `log_failure`
   rows cannot double-count a breach (today: 4 raw, 2 real).
3. **Convert manual debts** in order of cheapness: `decisions_log` ids (enables
   immutability check), a configs owner/purpose register, an alert ledger.
4. **I4 remains the biggest red** - 1,489 open of 2,602; promotion and falsifiers
   do nothing for the queue.

## Self-steal ledger (wave 4 additions)

| Stolen piece | From | Used as |
|---|---|---|
| tri-state PASS/FAIL/UNMEASURED | `mag/claims` + `claim_drift_patrol` verdict vocabulary | falsifier status, never collapsing unknown into pass |
| exit ladder 0/1/2 | `tools/claim_drift_patrol.py` | lint exits |
| manual-debt naming with owner + review date | `AGENTS.md` owed-items discipline, `state/CURRENT.md` "Owed" | 11 manual entries |
| log-window scanning | `mag/failure_kb.py` query shape | `log_zero` kind |

## Fireball

Wave 4 terminated. Falsifiers written, lint run, one real breach surfaced and
named, no registry write, no cron, no lane, no provider calls.
