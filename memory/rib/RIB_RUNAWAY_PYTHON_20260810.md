# RIB — Runaway Python Window-Storm: Complete Understanding (multi-day)

**RIB goal:** one geometric map of the whole problem so Grok 4.5 can advise on the actual
root, not the symptoms. Schema: rib.runaway_python.v1 · date 2026-08-10 · grounded in
memory leaves + live diagnostics.

## 1. The problem (as the operator experiences it)
For ~3 days: on reboot/start, the Mag stack spawns a storm of Python console WINDOWS
("hundred plus python windows"). Ghost "should have caught it" but did not. Multiple fixes
were tried; several made it WORSE or were false-positive detectors. Operator frustration:
"heard that before", "just do what I asked", "use fucking ghosts", "you don't need the shell".

## 2. The failure anatomy (verified, not guessed)
- **No process visibility:** `psutil` is NOT installed in the venv. Every governance branch
  (loop_breaker, legacy_audit, platform_kill, process_reaper) falls back to a PowerShell CIM
  query. The OLD nested-quote `-Filter "Name='python.exe'..."` form is mangled by PowerShell
  → silently returns 0 procs → ghost is BLIND. (Fixed to single-quoted Where-Object.)
- **Double-counting / venv-uv doubling:** on Windows every logical process = 2 PIDs: the venv
  shim (`...\.venv\Scripts\python.exe`, UNQUOTED cmd) + its uv-cpython child
  (`"C:\...\AppData\Roaming\uv\python\...\python.exe"`, QUOTED cmd), same cmd tail.
  - Without dedup, a HEALTHY single stack reads as 2x every slot + "multi_boot: 8 roots".
  - This produced FALSE "it's back / runaway" readings that made the problem look unfixable.
- **The crash-loop source:** ghost daemon (`-m mag.ghost --daemon`) spawns duplicate
  `autorun_loop` + ghost `cycle` children (seat-exit=-1 host-drainer issue). A 2-way duplicate
  singleton sailed under loop_breaker because its storm threshold was >=4.
- **Gating bug:** ghost daemon's `cycle_loop` SKIPS `cycle()` (and thus loop_breaker) while
  the operator is active — exactly when the storm shows up as windows. Sentinel was never
  wired into the daemon at all.
- **Boot non-idempotent:** `power start --browser` spawned a fresh windowed mag_launch every
  call (boot_mag.cmd had a guard; power.start_all did not). Repeated boots stacked stacks.

## 3. Attempts & outcomes
| Attempt | Outcome |
|---|---|
| psutil fallback -> fixed CIM query | WORKED: ghost can see procs |
| crashLoopBackOff in supervisor reap (2026-08-09) | WORKED: no instant respawn storm |
| source_trace.py (sense/trace_source/break_source) | WORKED: traces to root; false-positives until dedup |
| env stamp MAG_SLOT/MAG_SOURCE in spawners | WORKED: attribution by marker (supervisord steal) |
| power.start_all idempotent + boot lock | WORKED: no double-boot from power |
| sentinel wired into ghost daemon (always-on) | WORKED: not gated on operator |
| loop_breaker singleton threshold 4->2 | WORKED: 2-way dup now caught |
| **flocking dedupe (steal of flock_scheduler)** | **THE key fix**: embed+cluster venv/uv pair -> healthy stack reads clean |
| naive `_cmd_invariant` | FAILED: shim unquoted vs uv quoted -> never matched -> double-count |
| multi_boot as per-proc roots | FAILED: one boot shell miscounted as N roots -> now counts supervisors |

## 4. Where we are now (verified live)
`source_trace.sense()` → **VERDICT: clean**, 10 logical python, every singleton slot = 1,
`multi_boot: False`. Loop_breaker + sentinel share the dedup. 18 tests green. The detector
now distinguishes a healthy stack from a genuine storm.

## 5. Open questions for Grok 4.5 (coding advice)
1. Is per-parent strict 1:1 the correct dedup invariant, or is there a more robust
   Windows-native "process tree / job object" way to attribute a process to its true
   ancestor without psutil (WMI CIM is the only option)?
2. The host drainer seat-exit=-1 (uv-cpython spawn/reap) is the CRASH-LOOP root. What is the
   clean fix: avoid the venv shim entirely (spawn uv python directly), or fix the reaper?
3. Is the always-on sentinel (`taskkill /IM python.exe /F /T` over SPAWN_CAP=24) the right
   storm breaker, or should it kill by source-tree (taskkill /PID <root> /T) instead to avoid
   killing unrelated python?
4. Best way to make the venv/uv doubling structurally impossible (single canonical spawner)
   vs. always dedup at read time?

## 6. Forward path (our plan)
- Keep flocking dedup + supervisor-count multi_boot (already green).
- Fix the crash-loop at its root (host seat spawn/reap) rather than always auto-breaking.
- Confirm sentinel breaks by source-tree, not blanket python.exe kill.
- Wire source_trace.sense into the REST/dashboard surface (ghost :9000) so it's visible.
