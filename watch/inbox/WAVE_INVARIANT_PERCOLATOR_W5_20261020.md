# WAVE RECEIPT - invariant percolator, wave 5 (the instrument was wrong; retraction)

**Wave id:** wave-invariant-percolator-20261020-w5
**Parent:** `watch/inbox/WAVE_INVARIANT_PERCOLATOR_W4_20261020.md`
**Fired:** 2026-10-20T22:05Z
**Mode:** Standing Wave Protocol - one ask, bounded steps, $0
**Mutation:** two falsifier entries rewritten, one kind added, export regenerated.
No registry write, no log write.

## Envelope

| Axis | Bound | Used |
|---|---|---|
| Ask | explain the wave-4 FAIL before acting on it | 1 |
| Steps | 10 tool calls | 9 |
| Spend | $0 | $0 |
| Live writes | `falsifiers.jsonl` (2 entries), `PROMOTED_INVARIANTS.md` | 2 |

---

## 1. The wave-4 FAIL was a false positive - retracted

Wave 4 reported two doctrine invariants falsified:

```
[FAIL] be509348 log_zero  4 hits in 7d, latest 2026-10-17T15:42:38Z
       [steer] Escalate to next tier; stop token bleed.
[FAIL] 74dbeef7 log_zero  4 hits in 7d
       [steer] Escalate to the next smarter tier (escalate_on_loop).
```

Root cause of the false positive, traced at bytes:

1. The matching rows carry `phase: "escalate"`.
2. That phase is written in exactly one place in the estate:
   `mag/decision_framework.py:230`, inside `escalate_on_loop`.
3. `escalate_on_loop` is called from the collapse path at
   `mag/agent_cli.py:1763-1771`, immediately after the nudge budget is spent.
4. Therefore every matched row is **the escalation firing**, not the steer being
   ignored. Wave 4 counted detections as failures.

Cross-checks:

- `memory/decisions_log.jsonl` has exactly two "behavioral collapse" decisions at
  2026-10-17T14:39:41.912Z and 2026-10-17T15:42:38.413Z, matching the two real
  events (the 4 log rows are 2 events, double-written by the known duplicate
  `log_failure` in `operator_inbox.py`).
- Across the last 30 days: **51 loop pairs, max 2 distinct nudges per pair**
  (35 pairs at 1 nudge, 17 at 2). Two is exactly the detector's designed budget
  before escalation (`mag/agent_cli.py:1718`). No pair exceeded it.

Verdict: the escalation doctrine held in all 51 observed loops. Wave 4's claim is
withdrawn; the wave-4 receipt now carries a retraction block at the top.

## 2. What changed in the instrument

| change | why |
|---|---|
| new kind `nudge_budget` | the claim is "escalate *when* looping"; the falsifier must detect a loop that was **not** handled, i.e. a (sig, session) pair that exceeded the 2-nudge budget. Nudge rows are deduped per pair. |
| `dedupe_ms` on `log_zero` | duplicate `log_failure` writes made 2 events look like 4. Raw and unique counts are now both reported. |

Two entries rewritten (`be509348ee7becc5`, `74dbeef70dc87fe6`) from `log_zero`
to `nudge_budget` (window 30d, max_nudges 2, dedupe 1000ms). The note in each
entry records the retraction so the next reader cannot re-make the mistake.

## 3. Lint after the fix

```
FALSIFIER-LINT: ok -- 17 promoted, 6 PASS / 0 FAIL / 11 UNMEASURED (coverage 100.0%)
  [PASS] a77444ce log_zero       0 hits in 7d            "trust bytes, not reports"
  [PASS] 368a0fee log_zero       0 hits in 7d            "verify via OUR systems"
  [PASS] 997e65e9 field_complete 6/6 claims carry verifier
  [PASS] ff96a7ed file_absent    logs/training_events.jsonl absent
  [PASS] be509348 nudge_budget   51 loop pairs in 30d, none exceeded 2 nudges
  [PASS] 74dbeef7 nudge_budget   51 loop pairs in 30d, none exceeded 2 nudges
```

Exit 0. 11 manual debts unchanged, still named with owners and review dates.

Audit unchanged: 4/6 green on the promoted surface (I4 explore backlog 57.2%,
I5 leaf set red). Export regenerated with the corrected labels.

Tests: **38 passed** - `test_falsifier_lint.py` 12 (three new: dedupe, nudge
budget pass, nudge budget breach), `test_invariant_promote.py` 15,
`test_invariant_percolator_audit.py` 11.

## 4. Lesson (worth more than the fix)

A falsifier is a claim too. Wave 4 trusted its own instrument the way the steers
warn against trusting a report: it read `4 hits` and concluded `breach` without
asking what wrote those rows. The rule this wave adds to the discipline:

> **Before acting on a FAIL, trace the row to its producer.** A falsifier that
> fires is evidence about the instrument until the producer is identified.

That is now encoded in the entry notes and in this receipt, so the next seat
inherits the check rather than the mistake.

## 5. Still open (wave 6)

1. **I4 - the queue is the biggest red**: 1,489 of 2,602 explore rows open. No
   falsifier or promotion work touches it.
2. **Manual debts, cheapest first**: `decisions_log` ids (enables the immutability
   check), configs owner/purpose register, alert ledger.
3. **Duplicate `log_failure` in `operator_inbox.py`** - still double-writing every
   event; `dedupe_ms` hides it, a one-line fix removes it. Real bug, separate lane.
4. **The nudge budget is only measured, not enforced** - if a future run exceeds
   2 nudges, the lint will now catch it, but nothing stops the run in-flight.

## Self-steal ledger (wave 5 additions)

| Stolen piece | From | Used as |
|---|---|---|
| producer-tracing before accepting a signal | `memory/working.md` FKB diagnoses (every loop traced to its logging site) | the retraction method |
| paired keys, set comparison | `mag/p2p/quorum-coordinator.ts` dedupe-by-pubkey pattern (analogue) | `nudge_budget` pairing by (sig, session) |
| dedupe window | failure_kb duplicate-row history | `dedupe_ms` |

## Fireball

Wave 5 terminated. Retraction filed in the wave-4 receipt, instrument fixed,
lint green, tests 38/38, no registry or log writes.
