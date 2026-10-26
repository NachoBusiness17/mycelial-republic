# Fold gate repair receipt - ball-20260929 fold-gate lane (2026-09-29)

Owed waltz: `watch/inbox/gala_20260925/fold_gate.sh` exited 127, so every gala fold ran
without its counting gate and the wave5 filer wrote 12/0/0 by hand. Raw output of every
check below: `watch/inbox/gala_20260925/ball-20260929/lanes/fold-gate.check.txt`.

## Root cause (byte-proven this session)

The three hypothesized causes all die on evidence:

- NOT a missing file: `fold_gate.sh` exists on disk (1,709 B before this pass).
- NOT never committed: git-tracked, last touched by a5dd96176 (`git log --oneline -- watch/inbox/gala_20260925/fold_gate.sh`).
- NOT a wrong shebang: first bytes are `#!/usr/bin/env bash` with LF endings (od dump).

The real defect is invocation-side, two sibling modes on this Windows host:

1. Bare `bash` spawn: `CreateProcess` searching for `bash` can land on
   `C:\Windows\System32\bash.exe` (the WSL launcher). Pre-2026-09-29 the WSL default
   distro was `docker-desktop`, which has no `/bin/bash` - execvpe failure, the gate
   never started. Receipt of that diagnosis:
   `watch/inbox/gala_20260925/wave5-repair/fold-gate-repair.md` (prior gate-repairer
   pass). Its fixes were verified holding this session: WSL default is now Ubuntu
   (`wsl -l -v` shows `* Ubuntu`), and the estate-root `bash.exe` shim exists
   (6,144 B, 09:27) and intercepts the dwf's spawn shape (probe 2: bare `bash` via
   node spawnSync from the estate cwd resolves to MINGW64, rc 0).
2. The 127 itself, reproduced byte-exactly: under WSL-side bash, the gate's line-12
   venv python call `C:/Users/.../.venv/Scripts/python.exe` does not exist, so the
   script dies mid-run with "No such file or directory", rc 127. The ask's named
   failure mode. With the absolute `C:/` script path (the shape the-gala.dwf.ts:269
   actually passes), WSL bash cannot even open the file: rc 127 before any script
   line runs (probe 6).

Conclusion: the gate script was never the defect; the gate also never printed the
ballroom count (danced/refired/buried) - the filer's 12/0/0 was hand-computed. That
hand-written-number gap is what this lane closes in the script itself.

## What changed in fold_gate.sh (only file edited)

1. Ballroom counter, mapped 1:1 onto the saved the-gala workflow's own bankLane
   branches (the-gala.dwf.ts:233-248): danced = `ok` truthy, or `ok` absent/false but
   rows or checks banked (the workflow banks an ok-false result that carries evidence
   as danced); buried = parseable JSON with no ok, no rows, no checks (the exact
   "empty on refire" shape, ts:240); refired = counted from an optional per-lane
   `"refired": true` marker, else 0 (refire state lives at workflow runtime; the
   GalaLaneOut schema cannot carry it). Prints
   `ballroom_count (danced/refired/buried): D/R/B` plus `stuck:`/`banked:` detail lines.
2. decisions_changed now reads the three decision key names observed in the wild
   (`decision_changed`, `decision`, `decision_ledger`) - prior gate printed 10 and the
   midnight reader had to explain the gap; the filer's hand count was 12. The gate now
   prints 12, matching the verified truth.
3. Wrong-bash guard, fail-loud: non-MINGW/MSYS/CYGWIN `uname -s` prints
   `GATE FAIL: wrong bash: ...` and exits 2 naming the cause, instead of the silent
   mid-run 127. Not a fallback branch: this script is Windows Git Bash only by
   construction (line 6 hardcodes the Windows venv python).
4. Everything else byte-preserved: args contract (LANES_DIR EXPECTED_LANE_COUNT),
   `lanes_json_count` / mismatch exit 2, all existing section lines, `GATE PASS` /
   `GATE FAIL` verdicts, corrupt-JSON exit 2. Exit semantics unchanged: a counted
   burial does NOT fail the gate (a burial is a real outcome the fold reports; a
   nonzero exit would summon the dwf's gate-repairer at every honest burial).

## Checks run (all raw output in fold-gate.check.txt)

| Probe | Command shape | Exit | Verdict |
|---|---|---|---|
| 1 | git-bash: fold_gate.sh wave5-repair/lanes 12 | 0 | `ballroom_count (danced/refired/buried): 12/0/0`, GATE PASS - finish line A met |
| 2 | node spawnSync bare `bash` + absolute script path from estate cwd (the dwf's exact spawn, ts:269) | 0 | same sections via the estate-root shim |
| 3 | git-bash: synthetic archive, 11 danced + 1 stuck | 0 | `ballroom_count (danced/refired/buried): 11/0/1` + `stuck: synth-stuck.json (...)` - finish line B met |
| 4 | wave5 lanes with EXPECT=11 | 2 | `GATE FAIL: lane count mismatch` (no-weakening negative) |
| 5 | archive with 1 corrupt JSON | 2 | `corrupt: broken.json: ...` counted, rc 2 |
| 6 | System32 WSL bash, absolute C:/ script path | 127 | reproduced the ask's failure byte-exactly: `/bin/bash: C:/.../fold_gate.sh: No such file or directory` - unfixable from inside the script; the estate-root shim is the load-bearing defense (probe 2 proves it holds) |
| 6b | System32 WSL bash, relative script path (the shape where a wrong bash does open the file) | 2 | guard fires: `GATE FAIL: wrong bash: Linux - this gate is Windows Git Bash only` |

Synthetic fixtures: `watch/inbox/gala_20260925/ball-20260929/synth_lanes/`
(11 `ok:true` lanes across divisions B/A with one check each, plus `synth-stuck.json`
with `ok:false`, empty rows and checks - the buried shape).

Stated plainly, transcript-observed but not in the check file: the PRE-rebuild gate
under direct git-bash exited 0 printing `lanes_parsed_ok: 9/12` and
`decisions_changed: 10` with no ballroom line (the filer's hand-count gap, now closed);
`"C:/Windows/System32/bash.exe" -c 'echo BASH-OK'` exits 0 since the WSL default
flipped to Ubuntu. The 3 wave5 lanes that omit `ok` (events-door, patrol-fix,
suite-burn) carry `status: "done"` and 5-6 checks each; the gate counts them danced
via the evidence rule and prints them as `banked:` lines.

Not run: `tools/violation_ratchet.py check --changed` - the condition (touches under
mag/ or tools/) is not met; every edit lives under watch/inbox/.

Consumers: the only programmatic caller is the-gala.dwf.ts:94 (FOLD_SH). Additive
section lines change no exit semantics for it.

Decision ledger: the gala fold's arithmetic is now script-written end to end - the
ballroom danced/refired/buried count and the decisions_changed tally come from
fold_gate.sh sections, closing the filer-wrote-numbers-by-hand disease named in the
wave5 completion finding.
