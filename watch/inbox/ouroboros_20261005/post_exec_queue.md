# post-exec queue: R1 rows 1, 6, 7 (2026-10-05)

Filed by the post-executor lane after dwfrun-e9656e14's file fence lifted.
Two amendment sets, merged with what the executor's lanes already landed.
Instruments: `.venv\Scripts\python.exe` only; no commits; no em/en dashes in
landed text. Moments UTC.

## SET 1: tools/mickey17_v2_fold.py de-blind (R1 row 1)

Read in full first; e12's A14 unbound-aggregate check (`unbound_aggregates`,
`--check-master`, the 191.8M ERRATA class) preserved byte-identical. Landed,
merged on the same file:

- deep_tier2 walk: checks files are walked for `deep_tier2` arrays; entries
  matched to rows by row_key `<laneId>: <first six claim words>` (the
  mickey17-v2.dwf.ts deepAsk shape), exact JS-style and Python-style word
  splits, normalized on both sides. `unconfirmed` and `crashed` both file
  into PRISMA excluded code 9, separate labels (`9 verifier-unconfirmed
  (deep_tier2)`, `9 verifier-crashed (deep_tier2)`); the legacy top-level
  `unconfirmed` list walk stays for older archives.
- verdict-VALUE splits replace bare list lengths in the verifier table:
  `deep_tier2 12 (verdict split: verified 12)` style.
- header stamp: `folded_at: <UTC> (script sha256 <12 hex>)`.
- gate-vacuous marker on the Law 7 line when median==max==min.

Proof (fold run on the executor archive, 17:11:53Z, exit 0):

```
lanes=13 rows=59 included=59 excluded=0 dups=0 median_rows=5 -> memory\runs\mickey17_v2\runs\2026-10-05-exec\FOLD_SECTIONS.md
```

Header carries `folded_at: 2026-10-05T17:11:53Z (script sha256 31b0b8d178fc)`.
excluded=0 is now a verified zero: the archive's 12 deep_tier2 verdicts are
all value `verified`, zero unconfirmed, zero crashed (split printed in the
table). Synthetic fixtures (tmp dirs, module-level RUN_ROOT override) prove
the unconfirmed branch, the crashed branch, and the gate-vacuous marker fire;
PRISMA invariant held in every run.

Residue: the archive holds 13 json files, not 12: e11's
`e11-catalog-research.measure.out.json` rides the `*.json` lane glob and
counts as one landed-empty lane (0 rows). Named, not fixed; out of row 1
scope. And the exec runner wrote verdict value `verified`, outside the
canonical confirmed/unconfirmed/crashed vocabulary; the fold counts by value
so seats can dispute it, nothing is silently merged.

## SET 2: tools/workflow_gate.py gate teeth (R1 rows 6+7)

Additive; G1-G8 plus e04's two G8-width cards untouched.

- Row 6 stop-cert: registry status shape read first. REGISTRY.jsonl (88 rows
  at read moment) carried NO status field anywhere; the shape is defined
  additively: a row may carry `"status": "retired" | "superseded"` keyed by
  name, script path or digest. A matching script cannot mint a fresh PASS
  row: verdict becomes `BLOCKED-STOPCERT`, exit 2, and the check's own row
  still lands with a `stopcert` reason, so the refusal is a ledger fact.
- Row 7 FIRE_LEDGER: every single-script check appends
  `{ts, script, verdict, digest, fired_args, max_concurrency}` to
  memory/workflows/FIRE_LEDGER.jsonl (created on first append, append-only,
  single writer). `fired_args` parses the saved-workflow header args block
  into `{name: default_or_null}`; `max_concurrency` reuses the G8 regex
  (null when undeclared). Scenario mode stays read-only (LAW-12 contract
  unchanged) and `--no-register` skips the ledger too, same temp-file-row
  rationale as the registry skip.

Proofs: (a) scenario suite exit 0, 9 of 9 cards green including
G8_width_shape and G8_width_exception (17:07Z, read-only, no row written).
(b) End-to-end in a tmp cwd: PASS path mints the ledger row with parsed
args and width; appending a retired status row then re-checking the same
bytes yields `BLOCKED-STOPCERT`, exit 2, no fresh PASS row. (c) First real
ledger row, banking the round's own product on current bytes
(mickey17-burn.dwf.ts, the row 3 cure, not a retirement candidate), gate
PASS digest 977a8cbb7159 at 17:52:58Z:

```
{"ts": "2026-10-05T17:52:58Z", "script": ".zcode/workflows/mickey17-burn.dwf.ts", "verdict": "PASS", "digest": "977a8cbb7159", "fired_args": {"genre": "audit", "topic": null, "slug": null, "targets": null, "width": "50"}, "max_concurrency": 3}
```

## Tests

- `pytest tests/ -k "fold or gate or metadata" -q` (moment 17:20 to 17:52Z,
  1931.81s): 465 ran, 463 passed, 2 failed. Both failures pre-existing red,
  neither file touches the two amended tools:
  - test_freshness_gate.py::test_cli_hash_match_exit0_mismatch_exit2: date
    bomb, its fixture stamp 2026-09-20 crossed the 14d bar on 2026-10-04.
  - test_ldt_lattice.py::test_setval_targets_are_gated_on_singletons:
    lattice gate numeric assertion (np.False_), unrelated subsystem.
- Directly relevant files alone: test_workflow_gate +
  test_mickey17_v2_fold_unbound + test_workflow_registry_append_only +
  test_scenarios_gate_hook_pin + test_prepush_workflow_metadata = 26 passed
  (17:56Z). e12's check is green under the merge.

## Status of the teeth

The stop-cert is armed but unloaded: no registry row carries a status field
yet, so no live workflow is barred until the operator's fleet-verdict pen
(row 9, operator call) mints status rows for the retirement candidates.
FIRE_LEDGER readers: none yet beyond this gate; the journal join is the next
seat's surface.
