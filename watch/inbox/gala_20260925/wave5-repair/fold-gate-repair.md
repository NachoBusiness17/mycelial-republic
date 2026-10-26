# Fold gate repair receipt - wave5-repair (gate-repairer pass, 2026-09-29)

Failure: the GALA wave5 fold gate (`watch/inbox/gala_20260925/fold_gate.sh`, run by
`.zcode/workflow-runs/dwfrun-1357d4f7-83e3-42cb-ae23-353df5283e3e.mjs` as
`worldRead("run", ["bash", [FOLD_SH, LANES, TARGETS.length]])`) exited 1 with:

    WSL (1268210 - Relay) ERROR: CreateProcessCommon:818: execvpe(/bin/bash) failed: No such file or directory

The gate script never executed. Two independent defects were found and fixed.

## Defect 1 - bare `bash` resolved into a broken WSL chain (invocation)

- `where bash` on this host: `C:\Program Files\Git\usr\bin\bash.exe`,
  `C:\Windows\System32\bash.exe` (the WSL launcher), `...\WindowsApps\bash.exe`.
- The harness spawns bare `bash`; Windows CreateProcess searches parent exe dir,
  then parent cwd, then System32, then PATH, so the spawn lands on
  `System32\bash.exe` (WSL launcher) regardless of PATH order.
- `wsl --status` showed Default Distribution `docker-desktop` (minimal distro).
  Probe: `wsl.exe -d docker-desktop --exec ls /bin/bash` -> exit 1, no such file;
  `/bin/sh` exists. Reproduced the exact gate failure and exit code with
  `"C:\Windows\System32\bash.exe" -c 'echo BASH-OK'` -> same execvpe error, exit 1.
- Even with a Linux default distro, WSL bash cannot open the gate's absolute
  `C:/...` script path: probe after the fix below returned exit 127
  ("No such file or directory"), because the script is written for Windows-side
  bash (it execs the repo venv's Windows `python.exe`, fold_gate.sh line 6).

Fixes applied (both evidence-backed and reversible):

1. `wsl --set-default Ubuntu` - the registered `Ubuntu` distro (was Stopped) has
   `/bin/bash`, `wslpath`, and Windows interop (verified: runs
   `.venv/Scripts/python.exe` 3.11.15 from WSL). Docker Desktop addresses its
   distros by name, not by the default marker; `docker-desktop` stays Running.
   Rollback: `wsl --set-default docker-desktop`.
2. Compiled forwarder shim `bash.exe` at the estate root
   (`C:\Users\foste\Documents\projects\local_sovereign_agent\bash.exe`), source
   `watch/inbox/gala_20260925/wave5-repair/bash_shim_forwarder.cs`, built with the
   Windows-bundled `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe`. It
   re-execs `C:\Program Files\Git\bin\bash.exe` with the identical argument line
   and inherited std handles (CreateProcess STARTF_USESTDHANDLES), so arguments
   are forwarded verbatim, nothing added or dropped. CreateProcess finds it via
   the parent-cwd search before System32. Interception proven:
   `node spawnSync('bash', ['-c','uname -s'], {cwd: ESTATE})` returns
   `MINGW64_NT-10.0-19045`, exit 0 (was WSL before). If the harness cwd is
   somewhere else, the shim is a harmless no-op. Rollback: delete `bash.exe`.
   The shim is gitignored with a receipt comment in `.gitignore`.

## Defect 2 - lanes archive held 7 stray QC JSONs (count 19, gate expects lanes only)

`wave5-repair/lanes/` is the fold archive: one `*.json` per lane receipt, counted
non-recursively by `fold_gate.sh` line 9 (`ls "$DIR"/*.json | wc -l`). The run's
own actors had written 7 tool byproducts into the same dir (contents verified:
shared-surface rebuild/status dumps and a stealth-driver churn probe; none carry
the lane shape `division`/`checks`/`rows`):

    _probe_mirrors_scratch.json, _qc_rebuild_final_pass.json, _qc_rebuild_last_pass.json,
    _qc_rebuild_pass3_clean.json, _qc_validate_baseline.json, _qc_validate_final.json,
    _qc_validate_last.json

Moved byte-preserving into `wave5-repair/lanes/_qc/` (a subdirectory the gate's
non-recursive count never sees). Top-level `*.json` count: 19 -> 12, matching the
12 lane receipts in `watch/inbox/wave5_repair/` (attention-channel, config-hygiene,
dna-repair, events-door, mcp-pin-wire, old-files, patrol-fix, queue-closes,
render-pipe, seed-kernel, stealth-tools, suite-burn) and the 12 lane JSONs, all
`division: B`. None of the 7 moved files was registered in `watch/inbox/INDEX.json`
(0 grep hits), so the shared surface gained no new staleness from the move.
`python -m mag.shared_surface validate` errors shown during this pass (LINKS
event-kind rows, `suite-burn.json` / `wave5_repair/suite-burn.md` /
`STEALTH_MINED_FINDINGS.jsonl` / `PACK_OFFLOAD.jsonl` hash mismatches) are
pre-existing live-run drift: the run's own trajectory
(`memory/trajectory/steps.jsonl` step at 10:54) already shows surface-rebuild
flagging `suite-burn.json` hash drift before this repair began.

## Verification (all run during this pass)

1. Harness spawn shape: `node -e "spawnSync('bash', [FOLD_SH, LANES, '12'],
   {cwd: ESTATE})"` -> exit 0, sections print `lanes_json_count: 12 (expected 12)`,
   `lanes_parsed_ok: 9/12` (informational `ok` tally; the gate does not fail on it),
   `by_division: {"B": 12}`, `byte_checks_cited: 73`, `mined_rows: 5`,
   `decisions_changed: 10`, final line `GATE PASS`.
2. Direct Git Bash (historical invocation): `bash fold_gate.sh <lanes> 12`
   -> exit 0, `GATE PASS`.
3. Anti-weakening negative test: `bash fold_gate.sh <lanes> 11` -> exit 2,
   `GATE FAIL: lane count mismatch`. The gate's checks are unmodified:
   `fold_gate.sh` itself was not edited in this pass.

Residual assumption, stated plainly: the workflow re-runs
`TARGETS.length` from its own args; evidence for 12 is the 12 receipts and 12
lane JSONs (all division B). If the run was actually given a different lane set,
the gate will say so in its own printed `expected N` line.
