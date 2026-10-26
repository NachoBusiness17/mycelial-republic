# RECEIPT: percolator --candidates read path (fillball-1001, lane fill-percolator-candidates)

Date: 2026-10-02 (UTC) · Lane: gala_20260925/fillball-1001 / fill-percolator-candidates (division B) · Seat: GLM-5.3-Flash workflow lane

## The owed work

GAP_REGISTER rank 6 (a02-r2, `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:111-115`):
"percolator zero-ingestion - the mine's percolator_candidates.jsonl rows never reach
invariants.json and no --candidates flag exists (0 consumers confirmed by grep)."
Independently re-confirmed this session before the build: `grep -rn percolator_candidates`
over `mag/ tools/ tests/` returned zero hits.

## What landed

1. `mag/percolator.py`:
   - `--candidates PATH_OR_GLOB [PATH_OR_GLOB ...]` CLI flag (nargs +, glob expansion,
     cwd-first then ROOT-anchored).
   - `ingest_candidates()` + `_expand_candidate_paths()` + `_iter_jsonl_lines()`:
     each row's `claim` runs the standard `partition()` classifier (noise/theater still
     strip to the domain noise file); the surviving signal is filed in the REVIEW PASS
     `memory/percolator/candidates.jsonl` with `status: "candidate"`, `promoted: false`,
     plus `source_url` / `estate_map` / `probe` (and `area` / `card_path` when the mine
     emitted them). Rerun is idempotent: `(file, row, canonical)` dedupe gates EVERY
     disk write.
   - `CANDIDATES_REVIEW` constant + `candidates_review` surfaced in `status()`.
2. `tests/test_percolator_candidates.py`: 11 tests, tmp_path world discipline (same as
   test_percolator_z15.py; live memory/percolator tree never touched by pytest).
   Headline test `test_real_mine_candidate_reaches_review_pass` ingests row 0 of the
   REAL `watch/inbox/frontier_olm_2026-10-01/percolator_candidates.jsonl` and proves it
   reaches the review pass with its real source_url attached.

## The contract (lane ask, verbatim constraint)

Candidates are ingested "as candidates, not auto-promoted - the promote gate stays
alpha-budget". Implementation reads: the ingest path NEVER writes `invariants.json` or
`explore.jsonl`; a candidate reaches invariants only through the standing `percolate()`
path on reviewed signal. Byte-proven on the live tree: sha256 of
`memory/percolator/invariants.json` = `37bca85b6ec54ed3...` BEFORE and AFTER the live
ingest (identical; check.txt section 5). "Alpha budget" as a phrase has zero prior hits
in mag/ docs/ memory/rib/ corpus/steal/ - it is the lane ask's own contract language,
treated here as "promotion is rationed, never free".

## The live run (GAP_REGISTER rank 6's "run once over" both files)

`.venv/Scripts/python.exe -m mag.percolator --candidates "watch/inbox/frontier_olm_*/percolator_candidates.jsonl"`:
- 3 files matched (a third window, `frontier_olm_2026-09-30/percolator_candidates.jsonl`,
  6 rows, landed mid-flight at 04:10Z from the rank-7 backfill lane - the glob caught it;
  09-28: 5 rows, 10-01: 5 rows, 09-30: 6 rows = 16 total).
- Run 1: n_rows=16, n_candidate=16, n_promoted=0. Rerun: n_candidate=0, n_dupe=16,
  n_stripped=0 (idempotent). 22 noise sentences stripped to
  `memory/ghost/noise/frontier_mine.jsonl` (22 rows, stable across rerun).
- Byte probe: the 10-01 mine's row-0 claim ("Measure context as bytes that reach the
  model...") appears in candidates.jsonl exactly once, `promoted: false`.

## Two defects the live run caught (both fixed + regression-tested)

1. Relative-glob hits leaked native backslashes into the review row's `file` field
   (`watch\inbox\...`), which would have broken rerun dedupe keys (every rerun would
   duplicate all rows). Fix: `_expand_candidate_paths` stores RESOLVED paths so ingest
   relativizes against ROOT (forward-slash, repo-relative). Test:
   `test_relative_path_yields_forward_slash_repo_relative_file_field`.
2. Dedupe ran AFTER `append_noise`, so the idempotence rerun doubled the noise file
   (44 = 22 + 22, caught on the live rerun). Fix: dedupe gates every disk write;
   `partition()` is pure and runs before the skip. Test:
   `test_rerun_does_not_double_strip_noise`.

Lane-created artifacts from the buggy intermediate runs (`candidates.jsonl`,
`noise/frontier_mine.jsonl` - neither existed before this lane) were deleted and
re-ingested clean; the invariant registry was never touched at any point.

## Ratchet (exit 1, with an incident disclosed)

`.venv/Scripts/python.exe tools/violation_ratchet.py check --changed` = exit 1. Read of
`tools/violation_ratchet.py:277-279`: exit 1 fires only on NEW/expired rows. All 3 NEW
rows are FOREIGN staged `tools/` work this lane never touched
(field_experiment.py 637L, hermes_burn.py:393 except-pass, model_garden.py 446L) - they
belong to whichever lanes own those files. The `mag/percolator.py` GROWTH line
(accepted 580, now 745, +165) is a ledger fact, not a blocker (`:274-276`), left for
named re-audit or re-acceptance at push time; `baseline-update` is bulk-only
(`cmd_baseline_update`, `:284-316`, no per-file filter), so this lane could not accept
only its own growth without also misattributing the foreign rows.

INCIDENT: an exploratory `baseline-update --help` EXECUTED the bulk update (known filed
wart, commit a48c38543: "baseline-update ignores unknown flags; --help EXECUTES"). It
accepted the 3 foreign debts `by: operator` - none of them this lane's. Reverted
byte-exact (`git checkout -- configs/violation_baseline.json`; pre-check confirmed the
diff vs HEAD was exactly the 3 added claims + updated stamp). Post-revert register state
is the pre-lane state.

## Final numbers

- Tests: 24 passed (11 new + 13 Z15 regression), exit 0.
- Promote-gate byte-check: PASS (invariants.json sha256 unchanged across ingest).
- Review pass: `memory/percolator/candidates.jsonl`, 16 rows, all `promoted: false`.
- Full raw evidence: `watch/inbox/gala_20260925/fillball-1001/lanes/fill-percolator-candidates.check.txt`

## Named debt left open

1. mag/percolator.py growth 580 -> 745: needs named re-audit (split is a refactor, per
   the AG8 audit note) or named re-acceptance at push time. Not done here: bulk
   acceptance would misattribute foreign debt.
2. The 3 foreign NEW `tools/` debts (field_experiment, hermes_burn, model_garden):
   belong to their owning lanes; the ratchet stays FAIL for them until accepted by name.
