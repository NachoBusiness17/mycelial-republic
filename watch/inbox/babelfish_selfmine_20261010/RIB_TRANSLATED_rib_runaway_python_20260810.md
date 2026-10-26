# RIB_RIB_RUNAWAY_PYTHON_20260810 - translated by babelfish v1.0.0 (2026-10-10)

**Minted:** 2026-10-10 (caller-supplied; the module reads no clocks).
**Source bytes:** 4,689 | sha256 `8204541a3b02be3cee0cb14b0a9969d39a278bf79b9b9a5692a4c42dc8840bf7`
**Named roles found:** none detected
**Dominant terms:** python (11), ghost (9), venv (7), storm (6), dedup (6), root (5), every (5), daemon (5)

## THE LAW AS THEY STATE IT (verbatim, their voice)

> **RIB goal:** one geometric map of the whole problem so Grok 4.5 can advise on the actual
> root, not the symptoms. Schema: rib.runaway_python.v1 · date 2026-08-10 · grounded in
> memory leaves + live diagnostics.
> ("hundred plus python windows"). Ghost "should have caught it" but did not. Multiple fixes
> were tried; several made it WORSE or were false-positive detectors. Operator frustration:
> "heard that before", "just do what I asked", "use fucking ghosts", "you don't need the shell".

## THE INVARIANT TRANSLATION (each row names its check; status UNVERIFIED until run)

| their claim | invariant form | the check |
|---|---|---|
| For ~3 days: on reboot/start, the Mag stack spawns a storm of Python console WINDOWS | quantity claim (3 days) | re-count from primary bytes; compare against the stated figure |
| query. The OLD nested-quote `-Filter "Name='python.exe'..."` form is mangled by PowerShell | Name = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| - **Double-counting / venv-uv doubling:** on Windows every logical process = 2 PIDs: the venv | on Windows every logical process = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| - Without dedup, a HEALTHY single stack reads as 2x every slot + "multi_boot: 8 roots". | quantity claim (2x) | re-count from primary bytes; compare against the stated figure |
| `autorun_loop` + ghost `cycle` children (seat-exit=-1 host-drainer issue). A 2-way duplicate | children (seat-exit = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| singleton sailed under loop_breaker because its storm threshold was >=4. | ton sailed under loop_breaker because its storm threshold was > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| / psutil fallback -> fixed CIM query / WORKED: ghost can see procs / | psutil fallback - > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| / loop_breaker singleton threshold 4->2 / WORKED: 2-way dup now caught / | loop_breaker singleton threshold 4- > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| / **flocking dedupe (steal of flock_scheduler)** / **THE key fix**: embed+cluster venv/uv pair -> healthy stack reads clean / | uv pair - > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| / naive `_cmd_invariant` / FAILED: shim unquoted vs uv quoted -> never matched -> double-count / | shim unquoted vs uv quoted - > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| / multi_boot as per-proc roots / FAILED: one boot shell miscounted as N roots -> now counts supervisors / | one boot shell miscounted as N roots - > RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| `source_trace.sense()` → **VERDICT: clean**, 10 logical python, every singleton slot = 1, | every singleton slot = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| `multi_boot: False`. Loop_breaker + sentinel share the dedup. 18 tests green. The detector | quantity claim (18 tests) | re-count from primary bytes; compare against the stated figure |
| 2. The host drainer seat-exit=-1 (uv-cpython spawn/reap) is the CRASH-LOOP root. What is the | The host drainer seat-exit = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |
| 3. Is the always-on sentinel (`taskkill /IM python.exe /F /T` over SPAWN_CAP=24) the right | over SPAWN_CAP = RHS | run the arithmetic / evaluate both sides under the corpus's own definitions |

## INSTRUMENT ROWS (measurable with a named instrument)

| claim | instrument |
|---|---|
| - **No process visibility:** `psutil` is NOT installed in the venv. Every governance branch | sample N instances per the universal's domain and count exceptions |
| the operator is active — exactly when the storm shows up as windows. Sentinel was never | sample N instances per the universal's domain and count exceptions |
| / sentinel wired into ghost daemon (always-on) / WORKED: not gated on operator / | sample N instances per the universal's domain and count exceptions |
| vs. always dedup at read time? | sample N instances per the universal's domain and count exceptions |
| - Fix the crash-loop at its root (host seat spawn/reap) rather than always auto-breaking. | sample N instances per the universal's domain and count exceptions |

## REGISTER (the unmappable remainder - kept verbatim, never struck)

The babel fish preserves what it cannot translate. Register is the
seed, not the defect.

- (loop_breaker, legacy_audit, platform_kill, process_reaper) falls back to a PowerShell CIM
- → silently returns 0 procs → ghost is BLIND. (Fixed to single-quoted Where-Object.)
- shim (`...\.venv\Scripts\python.exe`, UNQUOTED cmd) + its uv-cpython child
- (`"C:\...\AppData\Roaming\uv\python\...\python.exe"`, QUOTED cmd), same cmd tail.
- - This produced FALSE "it's back / runaway" readings that made the problem look unfixable.
- - **The crash-loop source:** ghost daemon (`-m mag.ghost --daemon`) spawns duplicate
- - **Gating bug:** ghost daemon's `cycle_loop` SKIPS `cycle()` (and thus loop_breaker) while
- wired into the daemon at all.
- - **Boot non-idempotent:** `power start --browser` spawned a fresh windowed mag_launch every
- call (boot_mag.cmd had a guard; power.start_all did not). Repeated boots stacked stacks.
- | Attempt | Outcome |
- | crashLoopBackOff in supervisor reap (2026-08-09) | WORKED: no instant respawn storm |
- | source_trace.py (sense/trace_source/break_source) | WORKED: traces to root; false-positives until dedup |
- | env stamp MAG_SLOT/MAG_SOURCE in spawners | WORKED: attribution by marker (supervisord steal) |
- | power.start_all idempotent + boot lock | WORKED: no double-boot from power |
- now distinguishes a healthy stack from a genuine storm.
- 1. Is per-parent strict 1:1 the correct dedup invariant, or is there a more robust
- Windows-native "process tree / job object" way to attribute a process to its true
- ancestor without psutil (WMI CIM is the only option)?
- clean fix: avoid the venv shim entirely (spawn uv python directly), or fix the reaper?

## FALSIFIERS

- For each invariant row: run its named check against primary bytes;
  a mismatch kills the row, not the corpus.
- For the translation itself: a second pass over the same bytes must
  produce a byte-identical rib (determinism law).
- Class-deafness: an estate-authored doc must yield nonzero invariant
  rows and a woo corpus must yield nonzero REGISTER rows (spec falsifier).

## LINEAGE

- Translated by babelfish v1.0.0 (2026-10-10); spec watch/inbox/babelfish_20261010/SPEC.md
- Operator thesis: book-to-skill == closed-corpus-to-self-improving-system,
  in the direction you set, despite the platform's best wishes (2026-10-10).
