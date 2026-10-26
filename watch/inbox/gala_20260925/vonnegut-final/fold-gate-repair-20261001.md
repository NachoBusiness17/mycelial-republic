# Fold gate repair receipt - vonnegut-final (gate-repairer pass, 2026-10-01)

Failure: the GALA fold gate (`watch/inbox/gala_20260925/fold_gate.sh`, args
`lanes-dir expected-count` = `vonnegut-final/lanes 1`) exited 2 with:

    == SECTIONS BEGIN (script-written numbers, authoritative) ==
    lanes_json_count: 2 (expected 1)
    GATE FAIL: lane count mismatch

## Defect - the lanes archive held a non-lane verifier byproduct (count 2, gate expects 1)

`vonnegut-final/lanes/` is the fold archive: one `*.json` per lane receipt,
counted non-recursively by `fold_gate.sh:30` (`ls "$DIR"/*.json | wc -l`), failing
on mismatch at `fold_gate.sh:32`. It held two JSONs:

- `vonnegut.json` (09:44 EDT, 7072 bytes) - the TRUE lane output, GalaLaneOut
  shape (`lane`/`division: A`/`ok: true`/5 `rows`/3 `checks`/`decision_changed`).
- `vonnegut.checks.json` (09:49 EDT, 3705 bytes) - a tier-1 mechanical textual
  entailment VERIFIER REPORT over the lane's rows ("supports yes 1 / no 4"), not a
  lane output: no `division`, no `ok`, no `rows`, no `checks`. A downstream
  verifier wrote it into the lanes dir five minutes after the lane banked. The
  shared-surface index confirms the class: registered 13:49:01Z as
  `"class": "receipt"` by writer `md-record-seal`
  (`watch/inbox/index_events.jsonl:7860-7861`), sealed sha256
  `99f600f151eb20634d5456f744e458a623146787462eb10f52e190386dae6052`.

Same defect class as wave5's Defect 2 (receipt
`watch/inbox/gala_20260925/wave5-repair/fold-gate-repair.md`: 7 stray QC JSONs,
count 19 vs 12) - byproducts in the lanes archive inflate the gate's count.

## Fix (data moved, gate untouched)

1. Hash-verified before touching: `sha256sum` on the live file returned exactly
   the sealed `99f600f1...` - bytes intact.
2. Moved `lanes/vonnegut.checks.json` -> `vonnegut-final/vonnegut.checks.json`
   (beside the deliverable it grades, `vonnegut-final-cuts.md`; still durable
   under `watch/inbox/`). Post-move hash re-verified identical.
3. Shared-surface pointer kept honest: appended to `index_events.jsonl` one
   `invalidate` (old path, reason names the move; mirrors the drift-patrol-cron
   retire shape, line 7172ff) and one `register` (new path, same sha256, class
   receipt) - the CLI has no move verb (`python -m mag.shared_surface --help`:
   path/status/validate/rebuild only), and the log's own precedent is
   repairer-appended matching-shape rows (the 09-21 `repair` op, line 908).
   Last pre-append log write was 13:49:01Z, ~10 min stale - no contention.
4. Zero references broken: repo-targeted grep for `vonnegut.checks.json` over
   memory/workflows + watch/inbox + state + queue hit ONLY the index events
   themselves; `vonnegut.json`'s own checks cite `vonnegut.check.txt` /
   `vonnegut.grep.txt`, never the checks report. Repo-wide grep (completed after
   the move) found 4 files mentioning `vonnegut.checks.json`: this receipt, the
   reconciled `index_events.jsonl`, `.mimosa/hook-status/...actor_2_1-*.json`
   (sibling actor's session cache recording the pre-move observation) and
   `memory/trajectory/steps.jsonl` (this run's own append-only command log) -
   both run-scoped history, no live pointer broke.

## Verification (all run during this pass)

1. THE ASK'S CHECK: `bash watch/inbox/gala_20260925/fold_gate.sh
   watch/inbox/gala_20260925/vonnegut-final/lanes 1` from the estate cwd ->
   exit 0, `GATE PASS`, sections: `lanes_json_count: 1 (expected 1)`,
   `lanes_parsed_ok: 1/1`, `by_division: {"A": 1}`, `byte_checks_cited: 3`,
   `mined_rows: 5`, `decisions_changed: 1`,
   `ballroom_count (danced/refired/buried): 1/0/0`.
2. Anti-weakening negative test: same command with expected `2` -> exit 2,
   `GATE FAIL: lane count mismatch`. (First attempt through a pipe reported the
   grep's rc 0; re-run captured the gate's own exit: 2.)
3. `python -m mag.shared_surface validate`: no vonnegut errors post-repair (the
   move added zero new indexed-missing/hash errors; the invalidate+register pair
   reconciled the pointer). Pre-existing live-run drift visible at baseline AND
   after, unrelated to this lane and not healed here:
   `indexed item missing: gala_20260925/ractor50/lanes/logic.checks.json`,
   hash mismatches STEALTH_SWEEP_LATEST.md / PACK_OFFLOAD.jsonl /
   STEALTH_MINED_FINDINGS.jsonl / DRIFT_PATROL_20261001.md.
4. Gate bytes: `git diff watch/inbox/gala_20260925/fold_gate.sh` shows ONLY the
   pre-existing uncommitted ractor50 shape-guard block (added 2026-09-30, a
   fail-loud STRENGTHENING guard, present in the tree before this pass and seen
   in the initial read at lines 57-63). The failing count check (lines 30-32) is
   byte-identical committed vs working. This pass edited no gate bytes.

Residual, stated plainly: the verifier report's 1-yes/4-no entailment verdicts
on the lane's rows are preserved byte-for-byte at the new path and are the
tier-1 checker's business, not the fold gate's; the gate counts lanes, and
exactly one lane danced (division A, ok true).
