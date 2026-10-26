# L2 RETENTION LANDED - the smith owns the prune leg - 2026-10-09

Lane B1 deliverable of the standing-wave build (disk_audit_20261009 wave).
Spec first: this landing implements LAW_PACK law L2's retention leg as
written in watch/inbox/disk_audit_20261009/LAW_PACK.md (the ORGAN row names
tools/disk_smith.py; the CLEAN_RUNBOOK P2 order "wire it into the retention
law, do not one-shot it" is now satisfied by an organ, not a script).

## What landed

tools/disk_smith.py grows a --prune mode. NO other behavior changed: the
daily snap path (snap/delta/alert/history) is untouched in code and
byte-identical in output shape; pinned by
tests/test_disk_smith_prune.py::test_snap_path_output_shape_unchanged.

- PRUNE_ROOTS: the exec-forest class roots (config, not code - the L8
  shape; currently zcode_exec = C:/Users/foste/.zcode/cli/exec only).
  Other exhaust dirs join only by operator decision.
- RETENTION: the four-field contract (enabled, max_age_days 7, min_age_days
  1, max_count None). The age legs are wired; max_count lands with the L5
  lifecycle-row leg. Refusals: enabled=False, max_age_days <= 0, or
  max_age_days < min_age_days all exit 2 (usage class) and delete nothing -
  "contract refuses 0" per the Claude Code card 1.1 precedent; min_age
  protects the live window (the L2 falsifier: no kill is ever younger than
  min_age_days, holding by construction since every kill is past max_age).
- DRY-RUN by default: prints the full kill list (size, age, name, sorted by
  size desc) plus per-root and TOTAL totals, deletes nothing, writes
  nothing. --apply deletes exactly the aged set; locked-file failures are
  counted and listed (fail_list cap 50), never fatal.
- Containment identical in kind to harvest_exec_forest.py: safe_child is
  the only join (rejects empty/dot/dotdot and separator-bearing names;
  resolve-check against the allowroot), safe_dir gates every walked dir,
  and the delete re-derives the join adjacent to the access (the harvest
  sample() pattern). A forged kill row pointing outside the root counts as
  failed and the file survives - locked by
  tests/test_disk_smith_prune.py::test_prune_apply_failure_is_counted_never_fatal.
- CLI wiring: --prune, --apply (refused without --prune, argparse error =
  exit 2), --max-age-days (default 7). Ledger default resolves from
  PRUNE_LEDGER at call time so config redirects hold - a def-time default
  arg silently ignored the redirect (caught live by the landing demo; the
  misfired demo row was removed from the real ledger and the footgun is
  locked by test_prune_ledger_resolves_from_config_at_call_time).

## Ledger choice (documented, as the mission ordered)

The SIBLING ledger logs/disk_smith_prune.jsonl, not rows in
logs/disk_smith.jsonl. Reason: the snap delta reads the last row of the
snap ledger expecting a snap row; an interleaved prune row would blank the
next snap's delta math and change the main ledger's row grammar. Prune
receipt rows carry kind=prune, mode=apply, the contract fields, per-root
scanned/kill/errors, deleted, freed_bytes, failed, fail_list. Dry-run
writes nothing (smith-consistent: --dry never appends).

## Test numbers (real, instrument named)

- .venv/Scripts/python.exe -m pytest tests/test_disk_smith_prune.py -q:
  9 passed in 0.58s (final tree state).
- Combined smith selection (tests/test_disk_smith.py +
  tests/test_disk_smith_dotdir_lock.py + tests/test_disk_smith_prune.py):
  22 passed in 737.43s (0:12:17) - the live snap-shape tests walk the real
  seats (.zcode class), hence the 12 minutes. That run collected 22
  because it started before the 9th prune test landed; the final tree
  collects 23.
- pytest --collect-only -q tests -k disk_smith: 23/5004 tests collected
  (4981 deselected) in 8.66s, zero collection errors (final tree).
- Ratchet: .venv/Scripts/python.exe tools/violation_ratchet.py check
  --changed: PASS, hits=0 NEW=0.

## Dry-run demo (synthetic tree, real CLI wiring, verbatim)

Tree: sess_live/now.txt (0.5d, 40B), sess_live/recent.jsonl (3.0d, 60B),
sess_dead/deep/aged_stdout.json (8.0d, 1MiB), loose_aged.log (30.0d,
5MiB); PRUNE_ROOTS redirected to the tmp root.

```
$ python -m tools.disk_smith --prune
prune contract: max_age_days=7.0 min_age_days=1.0
zcode_exec: scanned 4 errors 0 kill 2 files 0.01GiB
    0.0049GiB   30.00d loose_aged.log
    0.0010GiB    8.00d aged_stdout.json
TOTAL: 2 files 0.01GiB past 7.0d
DRY RUN - nothing deleted. Re-run with --apply.
exit: 0
```

Apply on a fresh synthetic tree (2 aged, 1 young):

```
$ python -m tools.disk_smith --prune --apply
zcode_exec: scanned 3 errors 0 kill 2 files 0.00GiB
    0.0020GiB    9.00d aged_stdout.json
    0.0010GiB   12.00d loose_aged.log
TOTAL: 2 files 0.00GiB past 7.0d
APPLIED: deleted 2 freed 0.00GiB failed 0
receipt: <tmp>\disk_smith_prune.jsonl
exit: 0
remaining: ['sess_live\now.txt']
ledger row: {"ts": "2026-10-09T03:50:24.558024Z", "kind": "prune",
"mode": "apply", "max_age_days": 7.0, "min_age_days": 1.0, "roots":
{"zcode_exec": {"root": "<tmp>\\exec", "scanned": 3, "kill_files": 2,
"kill_bytes": 3145728, "errors": 0}}, "deleted": 2, "freed_bytes":
3145728, "failed": 0, "fail_list": []}
```

The young files never appear on the kill list; the real forest was NOT
pruned tonight (mission order): no real --apply has run, the real
logs/disk_smith_prune.jsonl does not exist yet.

## Notes for the next window

- The first real run must bank its dry-run before --apply (runbook law 5):
  .venv\Scripts\python.exe -m tools.disk_smith --prune (review kill list
  + TOTAL against the age-histogram prize) then --prune --apply.
- Wiring into MagDiskSmithDaily (08:50) is an operator call: either the
  task grows a second --prune --apply leg or the operator runs it manually
  until the fleet re-enable (runbook P4) proves the curve honest.
- tools/disk_smith.py sits at exactly 400 lines (the ratchet file-too-long
  cap fires above 400): the L8 lock lane's _row_gb fix and this prune leg
  share the file; the next smith growth owes a split, not a shave.
- Concurrent landing: the L8 dot-dir lock wave (tests/test_disk_smith_dotdir_lock.py
  + the _row_gb None-row fix) landed in tools/disk_smith.py while this lane
  worked; both landings are integrated and the combined 22-test run above
  covers them together.
