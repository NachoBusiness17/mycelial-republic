# bare-spawn-descent (gala ball-20260929, division B)

Lane: bare-spawn-descent · Date: 2026-09-29 · Owner: this lane
Receipt bytes: `watch/inbox/gala_20260925/ball-20260929/lanes/bare-spawn-descent.check.txt`

## The owed work

Descend the bare-spawn debt in tests/: census the remaining bare subprocess
spawns (no CREATE_NO_WINDOW on win32), convert at least 20 of the worst
offenders to the conftest default or explicit creationflags, and lower the
accepted ratchet baseline by name with the census as evidence. Never loosen
the hook; only shrink the debt.

## The instrument (what actually counts)

The ratchet is NOT tools/violation_ratchet.py (that gate scans mag/+tools/ for
other rules and has no spawn rule). The spawn ratchet is the headless-law test
`tests/test_headless_law.py` (operator order 2026-09-27/28): AST scan over
top-level `tools/*.py` and `tests/*.py` for `subprocess.run/Popen/check_call/
check_output/getoutput/getstatusoutput` calls WITHOUT a `creationflags`
keyword; the accepted debt lives in `state/fuel/headless_census.json`
(`bare_spawn_total`); the count may only ratchet DOWN; `os.system/popen` are
banned outright. The conftest default (tests/conftest.py -> mag.headless.
install_no_window_defaults) makes spawns windowless AT RUNTIME under pytest;
the static keyword is what the ratchet counts, so the descent is explicit
`creationflags`.

## Before (live census at lane start, byte-backed)

Command: `.venv/Scripts/python.exe watch/inbox/gala_20260925/ball-20260929/lanes/_census_bare_spawns.py`
(replicates the ratchet's `_scan()` exactly, plus line numbers; full sites in
`census_before.json` next to it)

- TOTAL 43 = tests/ 21 sites in 16 files + tools/ 22 sites in 17 files
- The accepted baseline read `bare_spawn_total: 41`, so the ratchet test was
  RED at lane start: `HEADLESS LAW: bare spawns grew 41 -> 43` (pytest run
  2026-09-29). The +2 drift is `tests/test_surface_rebuild.py` (2 bare sites,
  landed 2026-09-29 by the wave5 queue-closes lane, never re-ran this gate).
- Ask-context corrections (byte truth over brief): the ask said "accepted
  baseline 91" (file says 41) and "roughly 50 sites still bare in tests/"
  (live truth: 21). Both corrections are recorded in the lane JSON.

## The conversions (21 sites, 16 files, all in tests/)

House idiom (dominant in tests/, 38 existing sites): module constant
`HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if
sys.platform == "win32" else 0` + `creationflags=HEADLESS` per site
(0 on POSIX, where nonzero creationflags raise ValueError).
Comment on each constant names the receipt: HEADLESS law +
bare-spawn-descent 2026-09-29.

| File | Sites |
|---|---|
| tests/hook_pairing.py:46 (+`import sys`) | 1 |
| tests/test_hook_prefix_pairing.py:60,71 | 2 |
| tests/test_hunger_ledger_parity.py:61,121 | 2 |
| tests/test_icon_drop_escape.py:94 (inline idiom; local subprocess import kept) | 1 |
| tests/test_index_fold_host.py:63 (+`import sys`) | 1 |
| tests/test_k17_holds.py:31 | 1 |
| tests/test_k17_pilot.py:28 | 1 |
| tests/test_quote_gate.py:24 | 1 |
| tests/test_quote_hitrate.py:28 | 1 |
| tests/test_repo_readiness.py:8 (+`import sys`) | 1 |
| tests/test_scenarios_gate_hook_pin.py:46,55 | 2 |
| tests/test_seed_mcp.py:190 | 1 |
| tests/test_steer_sign.py:9 (+`import sys`; `["python", ...]` interpreter left as-is, out of lane scope) | 1 |
| tests/test_surface_rebuild.py:44,63 (+`import sys`) | 2 |
| tests/test_wow_player.py:115,118 | 2 |
| tests/wave_driver_test.py:140 | 1 |

tools/ (22 sites) is NOT this lane's domain and stays registered untouched.

## After + baseline lowered by name

- After census: TOTAL 22 = tests/ 0 + tools/ 22 (`census_after.json`).
- `state/fuel/headless_census.json` rewritten: `bare_spawn_total` 41 -> 22,
  census = the live tools/-only per-file counts, with `accepted: 2026-09-29`,
  `by: bare-spawn-descent lane, gala ball-20260929 (division B)` and a note
  carrying the 43-was-drifted-live fact. Named acceptance per the test's own
  law ("re-baseline by editing that file, which is a named acceptance").
  The hook (tests/test_headless_law.py) was not touched: it can only get
  stricter, and the debt shrank under it.

## Finish-line checks (all run this session, raw output in the check file)

1. Before/after census: 43 -> 22, delta -21 (ask requires >= 20). PASS
2. `.venv/Scripts/python.exe -m pytest tests/test_headless_law.py -q`
   -> `2 passed` (was 1 failed / 1 passed at lane start). exit 0. PASS
3. `.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
   -> `RATCHET: PASS` NEW=0, exit 0. (Its scope is mag/+tools/; this lane
   touched only tests/, but the gate was run anyway per the ask. Three
   pre-existing GROWTH lines printed: mag/corpus_acquire.py +77,
   mag/corpus_selfsteal.py +23, tools/stealth_driver.py +683 line growth on
   accepted file-too-long claims. Non-blocking, not this lane's files; the
   wave5 commit names the corpus_acquire pair as already-registered owner
   debts. Flagged here so the numbers do not silently ride.)
4. All 15 modified collected test files green, 4 groups: 47 + 10 + 47 + 16
   = 120 passed, 0 failed. (tests/hook_pairing.py is the shared helper, not
   collected; it is imported by test_hook_prefix_pairing.py which passed.)

## Decision ledger

Closes the bare-spawn descent decision: tests/ is now ZERO bare spawn sites
under the headless law, and the accepted register dropped 41 -> 22 (live 43
at start). Any new tests/ spawn without creationflags goes red against 22
with zero tests/ headroom; the next descent (if any) is tools/, which is not
this lane's domain. The operator's visible-window complaint (headless law,
2026-09-27/28) now has both halves sealed: runtime (conftest default) and
static (ratchet with no tests/ debt left).
