# WAVE RECEIPT - invariant percolator, wave 3 (policy v2, readable surface, dependency truth)

**Wave id:** wave-invariant-percolator-20261020-w3
**Parent:** `watch/inbox/WAVE_INVARIANT_PERCOLATOR_W2_20261020.md`
**Fired:** 2026-10-20T20:56Z
**Mode:** Standing Wave Protocol - one ask, bounded steps, $0, no provider calls
**Mutation:** ledger append (22 rows) + one generated markdown surface.
**Registry byte-identical immediately before and after** (same-instant sha check).

## Envelope

| Axis | Bound | Used |
|---|---|---|
| Ask | close the three named wave-3 gaps: policy leak, consumer surface, dependency truth | 1 |
| Steps | 10 tool calls | 9 |
| Spend | $0 | $0 |
| Live writes | ledger only + generated export | 22 ledger rows, 1 file |

---

## 1. Policy v2 - the leak is closed

`promotion.v2` sha `639ba9d453ed97c0` adds the tool-guard vocabulary to the
blocked patterns: `write_file missing path|emit flat JSON|sibling keys|\[REMEDY`.

| | v1 | v2 |
|---|---|---|
| promoted | 18 | **17** |
| the `write_file missing path=` row | promoted | **blocked** |
| ledger rows appended | 1,286 | +22 (18 re-confirmed, 1 demoted, 3 new) |

Promotion re-emission is now compact: a policy change re-confirms **promoted**
rows, but does not respam the 1,273 blocked rows whose verdict did not move.
Proved by `test_policy_change_does_not_respam_blocked_rows`.

## 2. A consumer surface exists now

`python tools/invariant_promote.py --export` writes
`memory/percolator/PROMOTED_INVARIANTS.md` - 17 rows, 2,896 bytes, generated
2026-10-20T20:55:54Z. It reads the ledger, never recomputes, so the export cannot
disagree with `audit --promoted-only`.

Domain split of the final surface: **8 behavioral (all `[steer]` doctrine) +
9 `org_v2_external_steal` architectural invariants.** The tool-guard line is gone.
Zero probe chatter, zero status lines.

The file states its own weakness in the header: *"Falsifier: none declared. No
registry row carries a falsifier pointer yet, so every line below is a claim
without a stated kill condition."* That is the next real gap, named on the
surface itself rather than hidden in a receipt.

## 3. Dependency truth - I5 was measuring the wrong population

Read-only mine (`percolator.mine_depends_on(apply=False)`), 1,290 rows:

```
rows with edges: 423 of 1290   |   edges: 963
edges touching promoted rows:  0
```

**All 17 promoted invariants are leaves.** The dependency graph lives entirely
in the non-promoted mass (status strings citing each other, tool-guard strings
containing each other's text). So I5's "10% of rows must declare depends_on",
applied to the promoted surface, is vacuously red - the surface is a leaf set,
not a graph with missing edges.

Deliberate non-action: **`--mine-depends-on --apply` was NOT run.** The
percolator is a live writer (about 10 rows/minute in the window we measured) and
the miner is a read-modify-write of the whole `invariants.json`; even with the
atomic writer, an apply can drop rows written between its read and its save.
Safe paths, in order: (a) stop the percolator writer, apply, restart; (b) run it
inside the percolator's own `--maintenance` window; (c) never - because on the
promoted surface it would change nothing (0 edges) and only fill `depends_on: []`
on the remaining 423 rows.

## The audit after wave 3

```
PERCOLATOR-AUDIT: VIOLATED -- 3/5 gates green [surface: promoted (17 rows)]
  registry: 17 invariants, 100.0% meet the repeat gate, median count 4, max 29
  [PASS] I1 0/17 below the repeat gate
  [PASS] I2 0/1 top-decile are fleet failure strings
  [PASS] I3 0/17 probe_* chatter
  [FAIL] I4 1479/2592 explore rows still open (57.1%)   <- queue-level
  [FAIL] I5 0/17 declare depends_on                     <- leaf set, see above
```

Tests: **26 passed** (`test_invariant_promote.py` 15 + `test_invariant_percolator_audit.py` 11).

## What is left (wave 4 candidates, ranked)

1. **Falsifier pointers on the 17.** The promoted surface says every claim is
   unfalsifiable. Add `falsifier: {metric, threshold, window}` per promoted row -
   even a one-line "what would prove this false" - and gate promotion on it.
   This is the only change that turns the surface from a list into a discipline.
2. **I4 (queue) is now the biggest red**: 1,479 open of 2,592. Promotion gate does
   nothing for it; it needs an explore consumer or a decay rule.
3. **I5 redesign**: keep it registry-level (13/1,290 = 1%) and add a promoted
   variant `leaf-or-declared` so the gate says something true about the surface.

## Self-steal ledger (wave 3 additions)

| Stolen piece | From | Used as |
|---|---|---|
| `--export` readable surface pattern | `memory/improve/field_brief.md` (generated brief) | `PROMOTED_INVARIANTS.md` |
| atomic-writer race caution | `mag/invariant_ledger.py`, `percolator._save_registry` | why `--apply` on the miner was refused |
| report-only mode | `percolator.mine_depends_on(apply=False)` | dependency truth without mutation |
| policy sha pinning | `mag/claim_ledger.py` | v2 reproducibility |

## Fireball

Wave 3 terminated. Ledger appended 22 rows, export generated, registry untouched
at apply time, no cron, no lane, no provider calls, no mining apply.
