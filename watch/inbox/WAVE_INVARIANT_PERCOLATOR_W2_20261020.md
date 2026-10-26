# WAVE RECEIPT - invariant percolator, wave 2 (promotion gate built)

**Wave id:** wave-invariant-percolator-20261020-w2
**Parent:** `watch/inbox/WAVE_INVARIANT_PERCOLATOR_20261020.md` (wave 1, audit + fold)
**Fired:** 2026-10-20T17:12Z
**Mode:** Standing Wave Protocol - one ask, bounded steps, $0, no provider calls
**Mutation:** one new ledger (`memory/percolator/promotion_ledger.jsonl`), two new
tools, two test files. **The registry was byte-identical immediately before and
after the apply** (sha256 `0acfe52166176d50...` sampled both sides, 17:12Z).
Note: the percolator is a live organ writing about 10 rows/minute, so a later
reader will see a different hash - that is the loop running, not this tool.

## Envelope

| Axis | Bound | Used |
|---|---|---|
| Ask | build the wave-1 fold: a promotion surface, no admission change | 1 |
| Steps | 12 tool calls | 10 |
| Spend | $0 | $0 (stdlib only) |
| Live writes | ledger only, append-only | 1,286 rows appended once |

---

## What was built

**`tools/invariant_promote.py`** - the gate the percolator never had.
- Policy `promotion.v1` (sha `6753b5fdf377a3fb`), frozen in the ledger for
  reproducibility: `count >= 2` AND (span >= 1 day OR >= 2 sources) AND domain
  not `probe_*` AND text not instrumentation vocabulary.
- Writes one row per changed verdict to `memory/percolator/promotion_ledger.jsonl`.
- Idempotent on `row_hash` + `policy_sha`: a second run on unchanged bytes
  appends nothing (proved in tests and on live data).
- Never edits `invariants.json`. Admission stays append-only as the wave-1 fold
  required.

**`tools/invariant_percolator_audit.py`** - gained `--promoted-only`; it now
reads the same policy through the same ledger loader (`from tools.invariant_promote
import load_ledger`). One policy, two readers - no second definition to drift.

**Tests:** `tests/test_invariant_promote.py` (12) + extended
`tests/test_invariant_percolator_audit.py` (11) = **23 passed** in 3.4s.
They pin the two laws: promotion never touches the registry bytes; promotion is
idempotent. Also: malformed ledger lines are skipped, never fatal; missing
registry or missing ledger exits 2.

---

## Measured on live data (17:12Z)

```
registry: 1286 rows | promoted: 18 | not promoted: 1268
blockers: count<2: 1163 | no-recurrence: 1208 | probe-domain: 586
          instrumentation-vocabulary: 51
```

(blockers overlap: a row can fail more than one test)

```
PERCOLATOR-AUDIT: VIOLATED -- 3/5 gates green [surface: promoted (18 rows)]
  registry: 18 invariants, 100.0% meet the repeat gate, median count 6, max 29
  [PASS] I1 0/18 rows below the repeat gate (0.0%)
  [PASS] I2 0/1 top-decile are fleet failure strings (0.0%)
  [PASS] I3 0/18 rows are probe_* chatter (0.0%)
  [FAIL] I4 1475/2588 explore rows still open (57.0%)   <- queue-level, not registry
  [FAIL] I5 0/18 rows declare depends_on (0.0%)          <- the cascade port never ran on these
```

The registry grew 1,225 -> 1,286 rows in the 6 minutes between wave 1 and wave 2
(about 10 rows/minute). That rate is the argument for the gate, not a footnote.

---

## Falsifier verdict (wave 1's condition)

Wave 1 wrote: *"if, after filtering to promoted-only, the top-20 rows are still
the fleet status/error vocabulary rather than steer doctrine and operator law,
then promotion alone does not fix the semantic problem."*

**The falsifier did NOT fire.** The 18 promoted rows:

- **9 operator doctrine / steer law** - "Verify with git diff / actual file bytes
  before declaring done" (29), "Escalate to next tier; stop token bleed" (16),
  "STOP asking permission / defaulting to operator for clear asks" (6), the
  elevate-with-a-deliberate-ask contract (19), the W0.3 gate surface (8), plus
  the smoke-test claim line (29).
- **9 architectural invariants** from `org_v2_external_steal` - content hash +
  attestation at trust boundaries; immutable decision records with
  superseded-by references; owner/purpose registration for long-lived organs;
  claims tested like code; generation closure + one-step rollback; alerting on
  consumer-visible symptoms; deterministic weighted conflict resolution;
  rollback scope naming; deletion reachability from named entry points.
- **1 known leak** - `write_file missing path= - emit flat JSON {...}` is a
  tool-guard remediation string, not knowledge. It survived because the policy's
  blocked vocabulary does not yet include that phrase.

Zero status lines (`source=... improve_queued=...`) survived - the blocked
vocabulary caught them. Net: 17 of 18 promoted rows are knowledge a new seat
could actually load.

## Known leak + the one policy change for wave 3

Add to `blocked_text_regex` (policy `promotion.v2`):
`write_file missing path=|emit flat JSON|sibling keys|\[REMEDY`

Cost of applying: policy_sha changes, so the next `--apply` re-emits all rows
once (append-only, ~1,300 lines). That is acceptable but should land with a
`--compact` reader or on a quiet cycle, not bundled into this receipt.

## What this does NOT do (named, not hidden)

1. **No consumer yet.** The ledger is a join key; nothing in `mag/` reads
   `promoted` at runtime. Wiring `mag/percolator.py --status` or the morning
   brief to the promoted surface is wave 3 work.
2. **I4 (explore backlog) untouched** - 1,475 open of 2,588. Promotion does not
   drain the queue; that needs an explore consumer or a decay rule.
3. **I5 (dependencies) untouched** - the cascade port (`mine_depends_on`) ran on
   639 rows historically but only 13 carry edges, and none of the 18 promoted
   rows declare one. Wave 3 candidate: run `mine_depends_on` over the promoted
   surface only, which is 18 rows instead of 1,286.

## Self-steal ledger (wave 2 additions)

| Stolen piece | From | Used as |
|---|---|---|
| append-only ledger + idempotency by content hash | `watch/inbox/PROMOTION_LEDGER.jsonl` pattern, `mag/invariant_ledger.py` | promotion ledger shape |
| `policy_sha` reproducibility | `mag/claim_ledger.py` baseline discipline | verdicts replayable per policy |
| one-policy-two-readers | wave 1's audit + `claim_drift_patrol` exit ladder | `--promoted-only` reuses `load_ledger` |
| alpha-budget promotion | `mag/percolator.py:504-509` (`candidates.promoted=False`) | promotion never auto-applies to consumers |

## Fireball

Wave 2 terminated. Ledger appended once, registry untouched, no cron, no lane,
no provider calls. Next wave fires on operator word only.
