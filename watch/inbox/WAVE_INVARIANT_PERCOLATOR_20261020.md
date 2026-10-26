# WAVE RECEIPT - invariant percolator, Socratic pass

**Wave id:** wave-invariant-percolator-20261020-socratic
**Seat:** L2-Hermes (gopher body), operator machine
**Fired:** 2026-10-20T17:06Z (probe) / receipt written 17:08Z
**Mode:** Standing Wave Protocol (`kit/PROTOCOLS.md`) - one ask, bounded steps, $0
**Spend:** $0 (stdlib only, no model calls, no cron, no lane spawned)

## Wave envelope (bounded before firing)

| Axis | Bound | Used |
|---|---|---|
| Ask | one: test the percolator's own claim against its own bytes | 1 |
| Deliverable | one audit tool + one receipt + one fold proposal | 3 artifacts, 1 wave |
| Steps | 12 tool calls | 11 |
| Tokens | no provider calls | $0 |
| Mutation | read-only on live data; new files only | `tools/invariant_percolator_audit.py`, `tests/test_invariant_percolator_audit.py`, this receipt |

The experiment under test is the Invariant Percolator (500GB -> 1GB thesis,
`watch/inbox/SELF_STEAL_INVARIANT_PERCOLATOR_FACTORIO_20261018.md` section 2).
CURRENT.md calls the build CLOSED; the registry is still being written
(`invariants.json` mtime 13:02 local today, last explore row 17:00:42Z), so the
experiment is closed as a build and live as an organ. This wave audits the organ.

---

## Socratic rounds

### Q1. What does the percolator say it does?
`mag/percolator.py:1-10`: "anything that can be repeated is compiled into
invariants, anything novel explored and folded"; the pipeline is "if that
canonical has been seen before -> REPEAT -> compile to INVARIANT ... if it is
NOVEL (first time) -> NOVEL -> log to the EXPLORE queue".

So the stated rule: **recurrence is the gate to invariant status.**

### Q2. What does the code do?
`mag/percolator.py:421-424`:
```python
reg["invariants"][canonical] = {"text": text, "count": 1, "first_seen": now,
                                "domain": domain, "last_seen": now, ...}
```
`_compile_invariant` writes a registry row with `count: 1` on FIRST sighting,
then returns `{"status": "novel"}` (`:437`) which also queues an explore row
(`:456-459`). Novel signal is therefore compiled into the invariant registry
AND queued as un-explored. The gate described in the docstring is not in the
code path.

**The docstring and the function disagree. The function wins.**

### Q3. Then how many rows ever repeated?
Measured on the live registry at 17:06:13Z:

| metric | value |
|---|---|
| invariants in registry | 1,225 |
| rows with count >= 2 | 115 (9.4%) |
| rows with count < 2 | 1,110 (90.6%) |
| median count | 1 |
| max count | 49 (was 232,214 before the Z15 count laws) |
| sum of all counts | 1,803 |

So 90.6% of the registry sits below the condition the module says it enforces.
The Z15 laws (`mag/percolator.py:32-46`, half-life decay + heal-merge MAX +
self-emission cap) fixed the arithmetic that inflated counts; they did not
change what gets admitted. The arithmetic is honest now. The admission gate is
still absent.

### Q4. If not repetition, what is the registry measuring?
Three probes:

1. **Run-specific strings.** 591 of 1,225 rows contain an 8-12 hex run id,
   e.g. `pro-2a371395ff -> ok (Verify with git diff ...)`. A string that is
   unique by construction cannot be an invariant.
2. **Probe chatter.** 525 rows (42.9%) are `probe_*` domains whose text is
   model small talk: "I never imagined I would be here today." (last explore
   row, 17:00:42Z, status open).
3. **The top of the table.** Top 20 by count: the `[steer]` doctrine lines
   (legitimate - operator law really is repeated), fleet status lines
   (`source=swarm_health_law improve_queued=0 handoffs=5`, 49), and the fleet's
   own error vocabulary (`backend timeout after 300s` 30, `backend reported
   failure` 21, `backend not reachable at http://127...` 20, `false-success:
   claimed edits, wrote nothing` 17, `5x identical run_python calls` 24).

The registry is measuring **frequency in the fleet's own instrumentation**, not
stability in the world. That is the difference between a log and an invariant,
and it is the same class of error the Z15 diagnosis found - the loop reinforcing
itself - one level up: Z15 fixed the counting, not the sampling. Samples drawn
from your own telemetry are not independent samples (`kit/PROTOCOLS.md`,
"fingerprinting by invariance").

### Q5. Is the top therefore dominated by the fleet's bugs?
**No - this hypothesis died in the audit, and that is the point of asking.**
Gate I2 (top-decile fleet-failure share <= 50%) came back **12/122 = 9.8%,
PASS**. The fleet's error strings are present and loud, but the top decile is
mostly steer doctrine and status lines. Recording the refutation rather than
the story I expected.

### Q6. What would make an invariant an invariant?
Not more counting laws. A **promotion gate**, separate from admission:

- admission (unchanged, append-only): every signal still lands as a row with
  `count: 1` - no data is lost, nothing is deleted;
- promotion (new): a row is *read as an invariant* only when
  `count >= 2` AND it was seen in >= 2 distinct source cycles AND its source is
  not `probe_*` and not the failure-KB vocabulary AND it carries a falsifier
  pointer.

That shape already exists in this repo: `memory/percolator/candidates.jsonl`
holds `promoted: False` rows and the comment at `mag/percolator.py:504-509`
states the law - "the promote gate stays alpha-budget: ingestion never compiles
invariants or explore rows; promotion happens only through the standing
percolate() path on reviewed signal." The percolator already knows this pattern.
It just does not apply it to its own registry.

---

## Measured audit (the receipt)

Tool: `tools/invariant_percolator_audit.py` (read-only, stdlib, $0).
Exit ladder self-stolen from `tools/claim_drift_patrol.py`:
0 green / 1 VIOLATED / 2 cannot-verify.

```
PERCOLATOR-AUDIT: VIOLATED -- 1/5 gates green
  registry: 1225 invariants, 9.4% meet the repeat gate, median count 1, max 49
  [FAIL] I1 1110/1225 registry rows have count < 2 (90.6%)
  [PASS] I2 12/122 top-decile invariants are fleet failure strings (9.8%)
  [FAIL] I3 525/1225 rows are probe_* model chatter (42.9%)
  [FAIL] I4 1414/2527 explore rows are still open (56.0%)
  [FAIL] I5 13/1225 rows declare depends_on (1.1%)
EXIT=1
```

The explore queue is not draining either: 2,527 rows, 1,414 open (56%), 684
done, 429 explored over 70 days - about 36 rows/day in and no observed drain.

Tests: `tests/test_invariant_percolator_audit.py` - **9 passed** (synthetic
estates; green / first-sighting / probe / backlog / dependency / CLI exit
0-1-2 / JSON receipt). Run: `./.venv/Scripts/python.exe -m pytest
tests/test_invariant_percolator_audit.py -q`.

---

## Self-steal ledger (nothing invented)

| Stolen piece | From | Used as |
|---|---|---|
| exit ladder 0/1/2, "cannot-verify is not failure" | `tools/claim_drift_patrol.py` | audit exit codes + UNVERIFIABLE arm |
| `promoted: False` alpha-budget gate | `memory/percolator/candidates.jsonl`, `mag/percolator.py:504-509` | the fold proposal (Q6) |
| count laws / self-emission cap rationale | `mag/percolator.py:32-46`, `watch/inbox/hydrology/Z15_PERCOLATOR_FIX.md` | why arithmetic alone was insufficient |
| failure-signature vocabulary | `mag/failure_kb.py` | I2 gate + the "loop, not world" reading |
| bounded ask / show-your-word / fireball | `kit/PROTOCOLS.md` | wave envelope + termination |
| recurrence-is-not-invariance | `kit/PROTOCOLS.md` "fingerprinting by invariance" | the Socratic spine |

Not done, deliberately: no write to `memory/percolator/invariants.json`; no
edit to `mag/percolator.py`; no lane or cron spawned; no model calls.

---

## Fold (one proposal, one falsifier)

**Proposal (next wave, not applied):** add `promoted: bool` to registry rows.
Admission stays as-is (append-only, `count: 1` on first sight). Consumers read
promoted rows only. Backfill is a pure function of existing bytes: `count >= 2`
AND >= 2 distinct `cycle_hits` values AND `domain` not `probe_*` AND text not in
the failure-KB vocabulary. Expected promotion on today's bytes: **12 rows**
(the strictest reading) to **79 rows** (count >= 2, non-probe), from 1,225.

**Falsifier:** if, after filtering to promoted-only, the top-20 rows are still
the fleet status/error vocabulary rather than steer doctrine and operator law,
then promotion alone does not fix the semantic problem - the source whitelist is
doing all the work and must move to ingest (block `probe_*` and failure
sources at `percolate_signal`). Kill the proposal if that happens; do not add a
second filter on top.

**Acceptance test for the next wave:** `invariant_percolator_audit.py` exits 0
with `--promoted-only` (a new flag) AND the registry row count is unchanged at
whatever it was before the change (no deletion), AND the explore queue's open
share is falling week over week (I4 trend, not snapshot).

## Fireball

Wave terminated. No background process, no queued work, no mutation of live
state. Artifacts are the tool, its 9-test battery, and this receipt. Next wave
fires on operator word only.
