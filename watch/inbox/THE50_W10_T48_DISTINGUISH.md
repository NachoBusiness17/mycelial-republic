# THE50 W10 T48: DISTINGUISH schema -> draft amendment rows (2026-09-19)

THE POINT: The DISTINGUISH schema drafted in ARC_LAWS is now three draft rows in the
amendment ledger, where it belongs. Row 3 proposes DISTINGUISH itself as the ledger's
third move (keep, kill, narrow); rows 4 and 5 are two worked demonstrations. All three
carry status "proposed": nothing activates until the operator gates them, and the
DISTINGUISH-writer stays owed deterministic code.

## What landed

- `state/fuel/amendments.jsonl` rows 3-5 appended (amendment.v1, all `"status": "proposed"`)
- this draft: `watch/inbox/THE50_W10_T48_DISTINGUISH.md`

## Lineage (all read on disk this session)

| Source | What it gave |
|---|---|
| `watch/inbox/ARC_LAWS_20260918.md:33-57` | the DISTINGUISH row schema (ADV-I-6), "draft for the amendment ledger"; sha256 `e919a38c2604829d9abc5cc6e4e0afa5bd57efaec5e32de3c81b4648e3906dcd` |
| `watch/inbox/DEEPSEEK_ADVERSARIAL_ARC_20260918.md:245` | invariant I-6 "DISTINGUISH BEATS OVERRULE"; sequence step 4: "Add DISTINGUISH to the amendment ledger schema (I-6)" |
| `watch/inbox/THE_50_PROGRAM_20260918.md:73` | task 48, W10 THEORY: "DISTINGUISH schema -> draft amendment rows [LANE]" |
| `memory/runs/adv_arc_50/RECEIPT.json` (C01) + `memory/runs/adv_arc_50/ADV_ARC_PACK.md:349` | receipt for D-0001: retraction raises Shannon entropy 0 to ~0.69 bits; sha256 `c9c143d3e8a75019208636a51da4185f75ad3c057ea698fcff4e1f4654b2e65c` |
| `watch/inbox/THE_BOOKS_DISAGREEMENT_20260919.md` + commit `e56a190f8` | receipt for D-0002: moon-speak law applied to the public reply, "canon keeps the full-depth version, public gets the one-pass version"; sha256 `4faf7c9371a2c17769f0251faefa0b45db22cf18251f683fc0065c6bdd11a3cd` |

Existing ledger before this task: 2 rows (`state/fuel/amendments.jsonl`), the tide
amendment obligation (2026-09-17) and AMENDMENT 001 attempt-budget (2026-09-17), both
`"active"`. The rows below are numbered 002-004 to continue that series.

## The rows

### Row 3: AMENDMENT 002, adopt the third move (proposed)

`target`: amendment ledger schema (the amendment.v1 row shape itself).
`change`: DISTINGUISH (ADV-I-6) joins keep and kill: it narrows a law's applicability
to a fact-pattern without retracting it. Row form per ARC_LAWS: `id` D-<seq>, `date`,
`target` (law or amendment id), `dimension` (lane | environment | scale | time-window |
stake-class | actor, extensible by operator gate only), `predicate` (deterministic
A3-clean ordinary code), `branch` (inside the predicate), `remainder` (outside, default
unchanged), `receipt_hash`, `conflict_rule` (narrowest-predicate-wins; ties by operator
gate, never model vote). The DISTINGUISH-writer is deterministic code over
operator-filed proposal rows, never an autonomous amendment path.
`falsifier`: a branch that contradicts its target outside the predicate (narrowing
became override), or a dimension added without operator gate, voids the amendment and
the ledger reverts to binary keep/kill.

### Row 4: AMENDMENT 003, draft D-0001 (proposed, gated on 002)

Target law: ADV-I-5, the chain never enters active context un-pruned.

```json
{
  "id": "D-0001",
  "date": "2026-09-19",
  "target": "ADV-I-5 chain-unpruned law",
  "dimension": "row-class (PROPOSED vocabulary extension, needs operator gate; the six seeded dimensions lane|environment|scale|time-window|stake-class|actor do not cover row kind, so this draft row is also the first vocabulary-extension request)",
  "predicate": "row.kind == 'precedent_of_error'",
  "branch": "retracted material may enter the active view only as compressed precedent-of-error (what was believed, what killed it, what it cost), priced as fragility weighting",
  "remainder": "unchanged: every other retracted row hash stays excluded from the active view; the tombstone sidecar is consulted at pack compile",
  "receipt_hash": "c9c143d3e8a75019208636a51da4185f75ad3c057ea698fcff4e1f4654b2e65c (memory/runs/adv_arc_50/RECEIPT.json C01: retraction raises Shannon entropy 0 to ~0.69 bits; memory/runs/adv_arc_50/ADV_ARC_PACK.md line 349)",
  "conflict_rule": "narrowest-predicate-wins; ties by operator gate"
}
```

Honest notes: the carve-out is already prose in the ADV-I-5 law text itself ("the
precedent of error is the only ghost allowed in the machine", ARC_LAWS lines 29-31);
this row converts prose exception into ledger lineage. It also exercises the gate on
purpose: none of the six seeded dimensions covers row kind, so D-0001 doubles as the
first vocabulary-extension request. The `row.kind` field binding to actual chain row
schemas is DISTINGUISH-writer work and is owed, not claimed done.

### Row 5: AMENDMENT 004, draft D-0002 (proposed, gated on 002)

Target law: moon-speak law (one-pass readability, no fleet jargon; salon 2026-09-11,
extended to all artifacts same day).

```json
{
  "id": "D-0002",
  "date": "2026-09-19",
  "target": "moon-speak / readable law",
  "dimension": "actor",
  "predicate": "reader.audience == 'public-external'",
  "branch": "the one-pass version: plain English, no fleet jargon, short enough for one pass on a phone (the 275-char public reply form)",
  "remainder": "unchanged: fleet-internal and canon artifacts keep the full-depth version with the detail below the point",
  "receipt_hash": "4faf7c9371a2c17769f0251faefa0b45db22cf18251f683fc0065c6bdd11a3cd (watch/inbox/THE_BOOKS_DISAGREEMENT_20260919.md)",
  "conflict_rule": "narrowest-predicate-wins; ties by operator gate"
}
```

Honest notes: this distinction is already operator-applied practice (commit
`e56a190f8`, 2026-09-19). The row codifies standing practice into lineage; it changes
nothing and gates nothing new.

In the ledger, each D-row rides inside its amendment.v1 row's `change` field as a
`json.dumps(..., sort_keys=True)` string, so `state/fuel/amendments.jsonl` stays
uniformly amendment.v1-typed and the payloads stay machine-recoverable.

## Gate boundary (what this task did NOT do)

- No row is active. All three are `"status": "proposed"`; ARC_LAWS keeps the amendment
  ledger human-only and the dimension vocabulary operator-gated.
- No law was narrowed in behavior. D-0001 codifies an existing prose carve-out; D-0002
  codifies an operator-applied practice.
- The DISTINGUISH-writer is not built. ARC_LAWS build order is schema first, writer
  second, and the writer is deterministic code over operator-filed proposal rows. T48
  delivers the schema as rows; the writer stays owed.

## Falsifiers (as filed in the rows)

- AMENDMENT 002: a DISTINGUISH branch that contradicts its target outside the
  predicate, or an ungated dimension, voids it; ledger reverts to keep/kill.
- D-0001: any retracted row hash reaching a pack compile outside the
  precedent-of-error predicate violates it; edited (rather than compressed-and-pointed)
  precedent rows void the branch.
- D-0002: a public-external artifact needing a second read or carrying fleet jargon
  violates it; flattening the full-depth canon version to one pass collapses the
  distinction and voids it.

## Check run (this session)

Command: `.venv/Scripts/python.exe -c "...json.loads each line; assert schema=='amendment.v1'..."`

Output:

```
total_rows: 5 | t48_rows: 3 | statuses: ['proposed', 'proposed', 'proposed']
d_rows_embedded: 3
```

The append itself ran via a temp builder using `json.dumps` per row, with an idempotency
guard (skips if "THE 50 W10 T48" already present) and an em-dash assertion over every
field; the temp script was removed after the run. No em-dashes in this document or in
the appended rows.

## Re-verification (2026-09-25, independent seat; ledger NOT re-appended, 5 rows stand)

Every lineage claim above was re-run from disk this session and held:

- `sha256sum` of the three cited files reproduces all receipt hashes exactly:
  ARC_LAWS `e919a38c...6dcd`, RECEIPT.json `c9c143d3...e65c`,
  THE_BOOKS_DISAGREEMENT `4faf7c93...3cd`.
- `memory/runs/adv_arc_50/RECEIPT.json:30` (C01) says "Shannon entropy 0 -> 0.69 bits
  per retraction"; `memory/runs/adv_arc_50/ADV_ARC_PACK.md:349` carries the same figure.
- `THE_50_PROGRAM_20260918.md:73` is task 48 as cited; commit `e56a190f8` exists with
  the moon-speak message quoted in D-0002's reason.
- Check command (`.venv/Scripts/python.exe`, json.loads over each ledger line): rows
  3-5 are `amendment.v1`, all `"status": "proposed"`; row 3 states all nine ADV-I-6
  field names (id, date, target, dimension, predicate, branch, remainder,
  receipt_hash, conflict_rule); the embedded D-0001 and D-0002 payloads in rows 4-5
  parse and match this draft's json blocks field-for-field; em-dash scan over every
  field of rows 3-5 and this document: zero hits.
