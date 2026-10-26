# INSTANCE GUARD LANDED - dogfood-48h ractor moves 1+4 executed (2026-10-02)

Order: operator "next" on the dogfood-48h ranked moves
(watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md). Moves 1 and 4
built, wired, tested, ratcheted same-sitting. Move 2 (driver 44072 bounce)
stays owed - it needs an owner that outlives the seat (see OWED).

## Built

- tools/instance_guard.py (new, 190 lines): three shapes -
  claim_process / guard_or_exit (pidfile singleton, exit-3 semantics,
  stale-pid reclaim; the scripts/descent_driver.sh guard lifted to python),
  claim_ask / release_ask (O_EXCL per-ask CLAIM, stale-steal at 1800s or
  dead-holder), ledger_key_exists / doubled_key_check (ingest tripwire:
  flags doubled (id, turn) rows and alarms memory/attention.md).
- Liveness law honored (T1W1 RACTOR V1): psutil.pid_exists preferred; NO
  os.kill(pid, 0) probing on Windows (sig 0 is CTRL_C_EVENT through
  GenerateConsoleCtrlEvent - the false-stale-unlink class); tasklist
  fallback when psutil is absent. Pattern stolen from mag/orchestrator.py
  _pid_alive (:417), the 12h-run zombie fix.

## Wired (the sweep - a fix that does not sweep siblings is unfinished)

- tools/hermes_burn.py: run_ask is now a claim wrapper around _fire_ask -
  the O_EXCL CLAIM closes the money window where two racers both passed
  _landed_skip (the 20:40:13Z twins, the 19:17Z T1W2 pair; $25.53 of the
  window's $37.76 was re-fire excess, 13 doubled keys, A1 x49 for $21.09).
  _bank stamps doubled_key=true + alarms on repeat (id, turn).
- scripts/run_autorun_loop.py, scripts/run_stealth_driver.py,
  scripts/wave_driver.py: guard_or_exit singleton at entry (exit 3 on a
  live twin - the 09-29 double stealth pids class).
- tools/ds_workhorse.py: singleton KEYED BY the --in batch path
  (sha256[:8]; different seats batching different files stay legitimate;
  two racers on ONE pending file refuse).

## Purged (delete-only-both-conditions law: unclaimed + owner dead)

- state/autodrain.pid (pid 32500, tasklist: dead, mtime Sep 22)
- state/night_cadence.pid (pid 14884, tasklist: dead, mtime Aug 28)

## Proof

- tests/test_instance_guard.py: 9 passed (fresh/busy/stale claims, exit 3,
  held-ask skip through the real hermes_burn.run_ask, doubled-key flag +
  alarm into tmp attention, foreign-claim left alone).
- Live dry-cycle over memory/plans/hermes_burn_DG1: HERMES-BURN PASS,
  DG1_moe_mating_door skipped as landed - the standing queue's skip state
  is intact under the wrapper (the running 45s driver cycle is unbroken).
- Ratchet: caught 3 except-pass NEW debts in the new module - all three
  FIXED in place (named handlers, loud failures); file-too-long on
  tools/hermes_burn.py:428 (>400, grown by the claim wrapper) ACCEPTED BY
  NAME zcode-boot-20261002 (configs/violation_baseline.json, register
  999). RATCHET: PASS, NEW=0.
- py_compile green on all 6 touched files.

## Honest limits

- claim_process stale-reclaim is last-wins between two simultaneous
  starters of a dead holder (microseconds window vs 45s cycles; the bash
  guard carries the same accepted window). The money-tight race is the
  per-ask O_EXCL, which is atomic.
- claim TTL default 1800s: a fire crashed mid-paid-call blocks its ask up
  to 30 min (dead-holder steal fires earlier when the holder pid dies).
- A live CLAIM from the dry path releases in finally (microseconds); dry
  runs cannot starve a paid fire.

## OWED

- Move 2: the surviving descent driver (pid 44072, born 21:31:24Z from
  pre-guard script bytes, writes no pidfile) is STILL unguarded; the
  bounce (DRIVER_STOP touch, wait one ~50s cycle, kill, relaunch under
  the guarded script, verify state/descent_driver.pid + second-launch
  exit 3) needs an owner that outlives this seat - operator hand or a
  registered task, never a seat-owned loop (the hermes-descent DRIVER
  lesson). Queues being dry is the only thing preventing double spend
  right now.
- Move 3 remainder (NIGHT_CLOSE erratum, CURRENT.md/todo refresh, kpi
  rotation, commit-queue ticket) and moves 5-8: separate sittings.

Filed by the 10-02 boot window seat. No em-dash bytes.
