# AC6 — refold_gate W3b fix: already at HEAD; gate GREEN on real tree; canary DEAD has a NEW cause (2026-09-30)

Seat: AC6 (ZCode), venv `.venv/Scripts/python.exe`. File ownership: `tools/refold_gate.py`.
Mission premise (AA4 triage #2): "W3b fix was working-tree only and never committed."
Byte verdict: **premise stale — the fix IS committed and IS at HEAD.** No commit was
made because there was nothing to commit (`git diff HEAD -- tools/refold_gate.py` empty);
an empty commit would be a fabricated landing.

## 1. Fix on disk — YES

`grep subprocess tools/refold_gate.py`: `_run` body returns
`subprocess.run(*args, **kw)` (line 80) with the Mickey17 W3 fix comment
(lines 68-76) naming the old `_run` self-recursion RecursionError. No recursive
call remains.

## 2. Fix at HEAD — YES, landed 579109f44 (2026-09-29 23:01:38 -0400)

- `git log -S 'return subprocess.run' -- tools/refold_gate.py` → single landing
  commit **579109f44** ("TIE-IT-ALL: … gates resurrected …").
- `git show HEAD:tools/refold_gate.py | grep subprocess.run` → line 80 present at HEAD.
- `git status --porcelain tools/refold_gate.py` → clean; HEAD is 19dff2287
  (2026-09-30 06:48:26, AB1 merge-conflict fix).
- Same commit 579109f44 also landed `memory/burns/LEDGER.jsonl` (tracked,
  `git ls-files --error-unmatch` passes) — load-bearing for finding 4.

## 3. Real-tree gate run — GREEN

```
$ .venv/Scripts/python.exe tools/refold_gate.py   # exit 0
  QUEUE-DUPES: ok, 498 rows, 498 distinct ids, 0 doubles
  REFOLD-GATE: ok (tests/test_index_fold_host.py ran against
  scripts/index_fold_host.mjs: 27 passed; RESTORE-GUARD: ok
  (audit: 1 record(s) checked, 1 historical, 0 informational, 0 standing stale))
```

All three arms green: restore-guard audit, queue-dupes census, 27 fold pins.
The W3b recursion fix works — the gate that fail-closed on every run since the
B2-343 landing now reaches and passes its verdicts.

## 4. Canary rerun (`--only refold_gate`) — STILL DEAD, but a DIFFERENT defect

```
GATE-CANARY: 1 families, throwaway worktree on HEAD
  refold_gate              DEAD  WARN conditional: B2-279 tier-swap fold mutation
    rc=2 fired=SILENT on its known-bad
      tail: RESTORE-GUARD: FAIL, cannot verify: ledger not found:
      %TEMP%\gate_canary_l8nurtyx\memory\burns\LEDGER.jsonl
```

Root cause chain (byte-read, not inferred):

1. The canary builds its worktree with cone-mode sparse checkout
   (`tools/gate_canary.py` `setup_worktree`, lines 226-249).
2. `SPARSE_DIRS` (lines 41-42) = tools, configs, scripts, tests, mag,
   memory/workflows, watch/inbox/burn_wave_20260926, watch/inbox/qdrop_export —
   **`memory/burns` is NOT in the set.**
3. `memory/burns/LEDGER.jsonl` is tracked but never materializes in the worktree;
   `tools/restore_guard.py` line 254 raises `CannotVerify("ledger not found")`.
4. refold_gate maps that to exit 2 (cannot verify) BEFORE the pins run, so the
   planted B2-279 tier-swap mutation is never named → rc=2 SILENT → DEAD.

So: the W3b recursion bug is fixed and committed; the residual DEAD is the
canary's stale sparse-set, not refold_gate. The ledger only became a gate
dependency when the B2-343 restore-guard arm landed, and it only became
canary-visible when 579109f44 tracked the ledger — SPARSE_DIRS was never widened.

**One-line canary fix (owned by the canary's fence-owner, not this seat):** add
`"memory/burns"` to `SPARSE_DIRS` in `tools/gate_canary.py` line 41, then rerun
`tools/gate_canary.py --only refold_gate` expecting ALIVE (rc=1, WARN fired).
Alternative if the ledger is meant to stay worktree-private: restore_guard needs
a canary-mode ledger fixture — an owner call, not mine.

Attention alert: the canary filed its own refold_gate DEAD alert to
`memory/attention.md` during this rerun; do not double-file.

## State summary

| Check | Result |
|---|---|
| W3b fix on disk | YES (subprocess.run, no self-recursion) |
| W3b fix at HEAD | YES (579109f44, 2026-09-29 23:01:38 -0400) |
| Commit made | NO — nothing to commit (premise stale, empty diff) |
| Real-tree gate | ok, exit 0 (27 pins, restore-guard ok, queue-dupes ok 498) |
| Canary `--only refold_gate` | DEAD rc=2 SILENT — canary SPARSE_DIRS missing `memory/burns`, NOT refold_gate |

## 5. Post-script (orchestrator seat, same session): SPARSE_DIRS fixed, canary ALIVE

Applied the one-line fix this receipt prescribed: `"memory/burns"` added to
`SPARSE_DIRS` (tools/gate_canary.py:41-43). Rerun `--only refold_gate`:

```
  refold_gate              ALIVE  WARN conditional: B2-279 tier-swap fold mutation
    rc=1 fired=REFOLD-GATE: FAIL, fold pins red on the current tree
```

The canary now materializes the ledger, the gate reaches its verdicts, and the
planted mutation FIRES (rc=1 named, not rc=2 silent) — ALIVE. The WARN text
("fold pins red on the current tree") is the B2-279 conditional describing the
canary's own planted tier-swap in the throwaway worktree, i.e. the canary
working as designed, not a real-tree defect. Canary defect CLOSED end-to-end
this session.
