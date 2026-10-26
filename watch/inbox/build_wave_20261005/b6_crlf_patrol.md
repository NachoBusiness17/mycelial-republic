# B6 - CRLF metadata patrol (build-it-all wave, 2026-10-05)

Lane: B6 of the build-it-all wave. Defect class (struck twice):
ractor-engine.dwf.ts moonshots default read as the STRING "2<CR>" (a quoted
2 with a CR inside the quotes, type: number) and refused runs; the .env CRLF
outage is the same byte disease on another surface.

## What landed

- `tools/prepush_workflow_metadata.py` - the patrol. Scans
  `.zcode/workflows/*.dwf.ts` and `.zcode/workflow-drafts/*.dwf.ts`
  metadata blocks (`/* zcode-workflow ... */`, first block only) for two
  finding classes: CR-IN-METADATA (any CR byte inside the block; one row per
  file with count and line range) and TYPE-DEFAULT (an arg declaring type
  number/boolean whose default fails the type; a quoted default of ANY
  content is a string default under YAML, an unquoted one must parse as the
  declared literal). Quoted defaults stay legal for json/string types. Files
  without a metadata block are counted and skipped (22 of 86), not findings.
  Accept-by-NAME via fingerprint into a baseline that starts ABSENT (zero
  baseline day one; citation_lint / credential_shape precedent). Output
  contract B2-338: green first line opens `WORKFLOW-METADATA: ok`. Exit
  0 clean / 1 findings / 2 cannot-verify.
- Findings fixed: 10 files, 289 CR bytes total stripped from metadata
  blocks ONLY (2 in `.zcode/workflows/`: game-mechanics-deep-dig 18,
  ractor-engine 37; 8 in `.zcode/workflow-drafts/`: Dogfood-48h,
  Grok-estate-audit, Ractor-dogfood-workflows, ractor-engine-2,
  ractor-engine-on-the-eleven-doors, Ractor-fleet-meta,
  Ractor-the-surface-migration-question, THE-50--reset-day-fullsend).
  Zero TYPE-DEFAULT findings live on the tree today: every number/boolean
  default already sits as a bare literal (the struck moonshots default now
  reads `default: 2`); the patrol holds the class for the next regression.
- `githooks/pre-push` - append-only wiring, WARN-ONLY, at the tail after
  seal_patrol. Byte-verified append: the new file starts with the exact HEAD
  bytes (31,153) plus 2,337 appended bytes; nothing above the seal_patrol
  block was touched (the workflow_gate.py owner's blocks untouched).
  `sh -n` clean. The appended block standalone prints
  `PUSH-GATE: workflow_metadata ok` on the fixed tree.
- `tests/test_prepush_workflow_metadata.py` - 10 tests: the byte-faithful
  struck shape (quoted "2<CR>", type number) trips WARN exit 1; clean files
  pass exit 0; CR in script body never flagged (block-only law); number and
  boolean default shape batteries; json/string quoted defaults stay legal;
  file-absolute line numbers; baseline accept-by-NAME leaves other findings
  fresh; no-scan-dir exit 2; no-block counted not flagged; --files extra
  scanning.

## Edit-tool deviation (named, with evidence)

The brief ordered the CR fixes "via the Edit tool". Measured twice at
landing: the harness Edit tool EOL-normalizes - an LF-only multi-line
old_string MATCHED a CRLF metadata block (edit "succeeded") and the write
preserved CRLF (block still 18 CR), and a literal `\r` in old_string stays a
two-character backslash-r (no-match error). It cannot strip CR bytes. The
load-bearing law ("metadata blocks only, never touch script bodies") was
kept by block-scoped byte surgery with per-file asserts: bytes before and
after the block identical, block content equal to old-minus-CR. Script
bodies byte-identical (their CRLF counts preserved: 143, 315, 305, 312,
312, 316, 315, 312, 312, 164).

## Gate numbers

- pytest: `tests/test_prepush_workflow_metadata.py` 10 passed. Full-suite
  verdicts and the sibling-drift caveat in the lane report.
- Ratchet: `tools/violation_ratchet.py check --changed` PASS, NEW=0
  (scope 19 changed files, 12 registered hits, zero new; the patrol adds
  none).
- Patrol on the fixed tree: exit 0,
  `WORKFLOW-METADATA: ok - scanned 86 workflow file(s) ... 0 finding(s)`.
- No git commit (lane law). No em/en-dash bytes in any file this lane
  wrote or appended (7 em-dashes in githooks/pre-push are pre-existing HEAD
  bytes, zero in the appended portion).

## Sibling-tree caveats (not this lane's files)

A full `pytest -q` run cannot finish: `tests/test_gwap_independent_cop_20261004.py`
line 191 is a SyntaxError (`..dumps(`) in a sibling lane's uncommitted
working-tree rewrite (HEAD version parses clean; the file is ` M` with a
whole-file rewrite in flight). A full `sh githooks/pre-push` run stops at
the ENFORCING citation_lint gate on sibling-changed rib records
(memory/rib/RIB_INFERENCE_BUDGET_20261001.md, memory/rib/RIB_MODEL_GARDEN_ROUTING.md),
also pre-existing working-tree state. Both are named here so the operator
routes them to their owning lanes; this lane's own bytes clear every gate
it owns.
