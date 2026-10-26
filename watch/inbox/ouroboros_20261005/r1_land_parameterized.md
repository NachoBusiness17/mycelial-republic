# R1 LANDING: parameterized mickey17-burn (amendment row 3)

Filed by the R1-landing lane, 2026-10-05. Row source:
watch/inbox/ractor_engine/2026-10-05-ouroboros-r1-fleet/SYNTHESIS.md row 3
(the fork-and-forget cure).

## What landed

ONE saved parameterized workflow: `.zcode/workflows/mickey17-burn.dwf.ts`
(52,981 bytes, 611 lines, LF-only, zero CR bytes in the metadata block, zero
em-dash / en-dash characters, no BOM), consolidating the three proven
skeletons:

- `.zcode/workflows/mickey17-v2.dwf.ts` (the audit engine; the saved copy IS
  the skeleton the synthesis cites by line)
- `.zcode/workflow-drafts/read-the-estate.dwf.ts` (12 lanes, dwfrun-a6bacf9c,
  ALL FILED)
- `.zcode/workflow-drafts/execute-register.dwf.ts` (12 executor lanes)

All three source skeletons stay on disk untouched (operator retires them only
after one clean fire of the consolidated one).

## Shape

- `genre` arg (audit | estate-read | execute, default audit) selects the
  default lane table inline: audit = standing claim-surface audit panel
  (a01-a12, GAP_REGISTER rollup; derived from the proven gap-analysis lane
  shapes generalized to standing surfaces); estate-read = the r01-r12 table
  verbatim; execute = the e01-e12 table verbatim minus one dead pointer (see
  below).
- `targets` json arg overrides any table ({id, what, start} rows); `width`
  caps it (default 50, truncated to table length); unknown genre throws with
  the three valid names.
- ONE slug formula: `slugify(slug) || slugify(topic) || genre-default` - bare
  letters/digits/dash (the fold tool's `--run` contract), NO vestigial
  lane-count suffix, NO hardcoded "-exec". Master fold name derives from the
  slug: `MASTER_<SLUG_UPPER>.md` (read-estate -> MASTER_READ_ESTATE.md,
  mickey17-v2 -> MASTER_MICKEY17_V2.md). Spec addendum path derives per slug
  (`<SLUG_UPPER>_RUN_SPEC_ADDENDUM.md`). Run archive at
  `memory/runs/mickey17_v2/runs/<slug>/`.
- Row 2 bake-in (tier-1 merge clause, exact wording): supportsAsk now reads
  "Read the file first if it exists; keep every existing key verbatim
  (including deep_tier2); replace only lane/supports/counts." after the
  "(Write tool)" sentence.
- Row 4 bake-in (manifest + RUNNER in the estate-filer ask): the filer copies
  the RUNNING script bytes from `.zcode/workflows/mickey17-burn.dwf.ts` to
  `runs/<slug>/RUNNER.dwf.ts` and writes `runs/<slug>/manifest.json` with
  exactly {topic, width, lanes, fired, script_path, moment}. The git add -f
  half of row 4 is repo-root work, not this lane's.
- Proven ceremony intact: lane ramp 8 then waves, refire-once + tombstones,
  G4 incremental report(), tier-1 supports persisted, tier-2 mechanical
  byte-verify, deep_tier2 persist before the fold, counting-gate fold
  (tools/mickey17_v2_fold.py via fold_run.sh, one repair pass), fresh-reader
  five-point review with REVISE-once repair, spec-writer for audit/estate-read
  (the proven exec ceremony has none), ALL-FILED filer verdict, WorkflowReport
  return. Artifact ids are compile-time literals ("steals", "fold"); only
  paths derive. Phases cover every stage.
- Fixed in transit: interface renamed `Target` -> `LaneTarget` (DOM-lib
  collision risk in the dwf compiler); exec e10 start date typo 20260904 ->
  20261004; conclusion now carries refired count for all genres plus executed
  count for execute.
- Dead pointer cure (evidence this sitting: `ls watch/inbox/read_estate_2026-10-04/`
  -> No such file or directory): the execute-default e01 start drops that
  folder and cites the live bytes (corpus/steal/MASTER_READ_ESTATE.md row 1 +
  the r04 lane rows under memory/runs/mickey17_v2/runs/).

## Gates (both re-run after the last edit)

- `.venv/Scripts/python.exe tools/workflow_gate.py check --script
  .zcode/workflows/mickey17-burn.dwf.ts` -> PASS, digest 423db130b866,
  G1-G8 all ok, zero soft warns (judge-model: groq/compound-mini stamp and
  source-fetched: 2026-10-05 stamp both present). Exit 0. Registry row
  written (the sanctioned cert for a NEW workflow, not a retirement
  candidate).
- `.venv/Scripts/python.exe tools/prepush_workflow_metadata.py` ->
  WORKFLOW-METADATA: ok - scanned 88 workflow file(s) (22 without a metadata
  block, skipped), 0 finding(s). Exit 0. The count moved 87 -> 88: this file
  is the only delta.

## Honest residue

- NOT FIRED. The parameterization needs one clean CreateWorkflow fire
  (finding 5's falsifier class); the three drafts stay until the operator
  sees that fire. Compile fitness is verified only by proven-byte fidelity
  plus the textual gate, not by a machine compile (no tsc in the venv;
  EvalWorkflowSnippet would execute agents).
- The audit default table is newly derived (standing surfaces), not a copy of
  a fired table; its first fire is its proof.
- The manifest "fired: true" value is a boolean per this landing's reading of
  row 4's key list; if the operator wants fired = the fired args, that is a
  one-token amendment.
- Amendments row 3's draft-side edits (gap-analysis.dwf.ts:90 suffix,
  rte:87 vestige, rte dead guard) were NOT made: the drafts stay frozen as
  the consolidation's provenance until retirement.
