# W2 Gate Canary (Mickey17 wave 2, return 7/24 gate-liveness) 2026-09-29

Concept source: `watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md` line 49 (RETURN 7
IMPROVEMENT): expendable gate-liveness CANARY, scheduled clone plants one
known-bad per gate in a throwaway worktree, runs pre-push, requires every
gate to fire; silence files its own death receipt.

## Files landed (Mickey17 W2 lane, file ownership held)

- `tools/gate_canary.py` (400 lines exactly, zero ratchet violations): builds
  a throwaway `git worktree` of HEAD (sparse cone over tools/configs/scripts/
  tests/mag/memory-workflows/the two watch subtrees; `core.autocrlf false`
  for a byte-faithful checkout), links a `.venv` junction so the secret
  gate's repo-venv check arms, plants one known-bad per gate family, runs
  the hook's exact gate command, asserts the gate's own named detection,
  restores (checkout tracked, unlink planted), tears the worktree down, and
  appends a `memory/attention.md` row for every DEAD/BLIND gate. Exit
  0 all fired / 1 dead or blind / 2 cannot verify. Fake token only:
  ghp_ prefix + 36 'A' built by concatenation; the canary source itself
  scans clean in the secret gate core (test-pinned).
- `tests/test_gate_canary.py`: 35 tests. Laws covered: broken-gate stub
  detected DEAD with attention row naming it; crash = BLIND not DEAD;
  real-tree untouched (scoped mtime snapshot, race-hardened); every family's
  fired predicate on the documented detection output plus silent negatives;
  plants edit exactly their targets; live subprocess firings of ratchet,
  config_seal, description_pin, freshness, checkbox, census on fixture trees.
- `scripts/register_gate_canary_task.ps1`: registers MagGateCanaryDaily
  09:45 (after improve 08:00 / census 08:30 / fts 09:00), log
  `logs/gate_canary.log`. NOT registered yet: operator decision.

## Test line (real, pytest -q, 2026-09-29)

`tests/test_gate_canary.py -q` -> **35 passed** (13.9s).

## THE key finding: real canary run, alive/dead table

Run: `.venv/Scripts/python.exe tools/gate_canary.py` (throwaway worktree on
HEAD, venv junction linked, control sweep + one planted run per family).
Exit **1**. Attention rows filed for the two dead gates.

| gate family (hook block) | verdict | evidence |
|---|---|---|
| violation_ratchet (ENFORCING) | ALIVE | planted except-pass -> NEW + RATCHET: FAIL, rc 1 |
| config_seal (ENFORCING) | ALIVE, control fired at HEAD | planted drift -> MODIFIED + FAIL rc 1; pristine HEAD already red, see control finding below |
| secret_gate (ENFORCING) | ALIVE | planted fake ghp_ token -> GITHUB-TOKEN blocking, rc 1 |
| census_drift_patrol (WARN/exit2) | ALIVE | stale carrier -> CENSUS-PATROL: STALE, rc 1 |
| freshness_gate (WARN-only) | ALIVE | stale stamp -> FRESHNESS-GATE: FAIL, rc 2 |
| checkbox_receipt_gate (WARN) | ALIVE | receiptless checked row B2-9999 -> NEW DEBT, rc 1 |
| description_pin (WARN-only) | ALIVE | unpinned manifest -> finding, rc 2 |
| caption_ledger_verify (WARN cond.) | **DEAD** | deleted ledger row -> `RESULT: PASS - 266 rows`, rc 0: gate silent on its known-bad |
| refold_gate (WARN cond.) | **DEAD (BLIND)** | its own `RecursionError` on every run at HEAD; can never print ok or a meaningful FAIL |
| workflow_gate_scenarios (ENFORCING cond.) | ALIVE | armed + flipped card -> SCENARIOS FAIL, rc 2 |

8 alive, 2 dead.

## Dead gate 1: refold_gate.py cannot run at all

`tools/refold_gate.py` `_run` (line ~66-70) calls itself:
`def _run(*args, **kw): kw.setdefault("creationflags", ...); return _run(...)`
-> infinite recursion -> `RecursionError` on every invocation. Root cause:
the HEADLESS-law sweep commit 4458355e8 ("prepush + 4 tools wrapped
headless") introduced the self-call; `tools/secret_gate_scan.py` carried the
identical bug and was fixed 2026-09-28 (its own comment names the pattern),
refold_gate was missed. Hook impact: the refold block's WARN arm prints this
traceback on every armed push; the fold pins never run. Verified in the real
repo: `python tools/refold_gate.py` -> rc 1, RecursionError. Fix is the same
one-liner secret_gate_scan got (call `subprocess.run`); NOT applied here
(file ownership: gates lane).

## Dead gate 2: caption ledger verifier is deletion-blind

Known-bad: dropped the last ledger row (id 10972934, a normal drop row).
Verifier: `RESULT: PASS - 266 rows, 162 drops`, rc 0. Cause (read from
`scripts/the50_t21_q_caption_ledger_verify.py` check6): `by_id` is built
from the LEDGER rows, so a deleted row removes itself from the comparison;
the check verifies each surviving row is extractor-reproducible but never
verifies coverage (that every source drop's rows appear). Denominator is
self-referential -> silent shrink passes. Same disease family as B2-238
(unearned flips mute the dispatcher). Fix direction: add a coverage check
over `qdrops.jsonl` ids; NOT applied here (ownership).

## Control findings (gate fires, but pristine HEAD is already not green)

- config_seal: at HEAD, all 56 sealed hashes mismatch the committed blob
  bytes (seal computed over this machine's CRLF working-tree bytes, blobs
  are LF). Any byte-faithful checkout (Docker/WSL/CI/canary worktree) fails
  `verify` with every file MODIFIED. The register is autocrlf-fragile; the
  gate itself fired correctly on planted drift.
- checkbox_receipt_gate: 2 worktree-only offenders (rows citing receipts
  under memory/ root and a gitignored memory/biography path). Real repo
  control is 0 offenders; clone-inherent, not HEAD debt.

## Canary-harness lessons fixed during the run (gates exonerated)

- Sparse cone originally omitted `mag/`: `tools/__init__.py` imports modules
  needing `mag`, so the secret gate crashed in the worktree (first-run
  BLIND was a canary bug, not a gate bug). Cone now includes `mag`.
- autocrlf smudge on checkout faked caption check8 CRLF failures and
  config_seal hash drift; worktree now checks out with
  `core.autocrlf false` (byte-faithful).
- First-run false attention rows (from those canary bugs) were removed by
  hand; the final run filed exactly the two true rows.

Laws: em-dash 0 across all three files; no real secret anywhere (fake token
built by concatenation, canary source scans clean); real tree untouched
(41,205 tracked paths snapshotted; only sibling-lane movement observed,
attributed in the run log).
