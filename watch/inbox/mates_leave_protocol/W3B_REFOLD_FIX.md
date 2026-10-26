# W3B — refold_gate recursion fix (Mickey17 W3, 2026-09-29)

## The defect

`tools/refold_gate.py` `_run` called itself (`return _run(*args, **kw)`) —
the name had been rebound away from `subprocess.run`. The first spawn (the
B2-343 restore-guard audit) died with `RecursionError: maximum recursion
depth exceeded`, so the gate fail-closed every run with a traceback instead
of a REFOLD-GATE verdict. Proven at HEAD by the gate_canary refold_gate
family (BLIND, `rc=1 fired=SILENT on its known-bad`, traceback tail) and
reproduced by hand before the fix.

Same bug class secret_gate had fixed: `tools/secret_gate_scan.py` `_run`
(2026-09-28 drift-patrol receipt; secret-gate go-live e60b4e801). The
mirrored fix lands in `tools/refold_gate.py` `_run`:
`subprocess.run(*args, **kw)` with `shell=False` default and the HEADLESS
`CREATE_NO_WINDOW` default kept; fix comment carries cause + evidence per
build discipline.

## Verification (real numbers, byte-backed)

- Fixed gate on the real tree: `REFOLD-GATE: ok (tests/test_index_fold_host.py
  ran against scripts/index_fold_host.mjs: 27 passed; RESTORE-GUARD: ok ...)`,
  exit 0. (Docstring's "21 tests" is stale prose; the run reads 27.)
- New regression test `tests/test_refold_gate_run.py`: 2 passed in 4.22s —
  runs the gate as a subprocess on a self-contained fixture tree (stub
  restore-guard, stub queue-dupes, stub host, one stub pin) and pins
  exit 0 + `REFOLD-GATE: ok` + no traceback; second case pins exit 2
  "cannot verify" on a tree missing pins/host. Skips (not passes) when
  node is absent, because the gate exits 2 at its node check before the
  first spawn and a pass would be vacuous.
- Sibling refold-referencing tests: `test_gate_canary.py +
  test_hook_prefix_pairing.py + test_refold_gate_run.py` → 44 passed in
  21.46s.
- Canary rerun `--only refold_gate` with `--attention` pointed at a TEMP
  file (no real-tree write; real tree snapshotted 41,504 tracked paths,
  no taint): still BLIND at HEAD bytes with the RecursionError tail —
  expected, because the canary worktree checks out committed HEAD and
  this fix is deliberately UNCOMMITTED (W3 lane: do not git commit). The
  family flips to ALIVE only after the operator commits; the fix itself is
  verified by the direct green gate run above.

## Same-class latent debt found, NOT touched (outside this lane's ownership)

`tools/quote_audit_wide.py` `_run` (line ~59-63) still self-recurses
identically. No canary family exercises it. Flagged for the owner of that
file; not fixed here per file ownership.

## Files

- `tools/refold_gate.py` — `_run` recursion fix (mirrors secret_gate_scan)
- `tests/test_refold_gate_run.py` — new regression test (2 tests)
- No commits made, per lane instruction.
