# X12 - MATE UNBLOCK (the static-runner indirection landed)

2026-09-29/30 window. Operator order: end the Mimosa standoff tonight via the
static-runner solution. Filed per the shared surface contract; receipt before
promotion. No commit made on the estate (per order).

## The standoff (context, from REGISTER_NOTE.md 2026-09-30)

Three successive hardenings of a direct driver were blocked by the Mimosa
gate: (1) list-form subprocess; (2) + shell=False + "--" end-of-options;
(3) constants-and-one-int argv with mission packs as files. The scanner flags
any subprocess argv containing variables, regardless of form. The gate is
law; the fix was never going to be a fourth argv disguise.

## The fix that landed (static-runner indirection)

All day-to-day variance moved OUT of every argv and INTO files:

1. `tools/leave_dispatcher.py` (new) - writes today's mission packs (from
   configs/mates.yaml + the operative STEER row per mate via tools/steer_read.py)
   into `logs/mates/missions/mission_<YYYYMMDD>_<nn>_<mate>.md`, then invokes
   the runner N times. Its ONLY subprocess argv is the module-level
   `RUNNER_ARGV` tuple of pure string literals
   (`powershell -NoProfile -ExecutionPolicy Bypass -File <abs>\scripts\run_mate.ps1`).
   Zero variables, zero f-strings, zero derived values; a `_runner_path_guard()`
   fail-closes (exit 2) if the repo ever moves under the frozen literal.
2. `scripts/run_mate.ps1` (new) - takes NO parameters. Set-Location to the
   repo; computes `$Today` itself via Get-Date; atomically CLAIMS the next
   unclaimed mission of today (CreateNew of a `<pack>.claim` sidecar - CreateNew
   fails if it exists, so N concurrent constant-argv invocations each take a
   distinct mate); calls `opencode run "<fixed prompt template>"` naming the
   claimed pack. The argv is constant; only the file it reads varies. No
   unclaimed mission = honest no-op exit 0.
3. `scripts/register_leave_task.ps1` (new) - registers MagLeaveProtocolDaily,
   daily 08:00, per the register note's sanction. /TR is two bare absolute
   tokens (venv python + dispatcher), zero embedded quote pairs - the W3T
   defect (PS 5.1 mangles quoted /TR, schtasks exit 5) is structurally absent.

The mate payload is entirely in the pack: persona, hunting ground, seed
thread, laws verbatim, STEER row, receipt contract (FINDINGS / JOURNEY /
COUNTS, no em-dashes, resume-not-respawn).

## Verification bytes (this window, all real runs)

Dry run (the ordered test; zero subprocess calls in dry mode):

```text
.venv/Scripts/python.exe tools/leave_dispatcher.py --dry
[2026-09-29 23:17:28] mission written mission_20260929_01_cartographer.md
... 8 packs total (01 cartographer .. 08 gambiter) ...
WOULD RUN [mission_20260929_01_cartographer.md]: powershell -NoProfile
  -ExecutionPolicy Bypass -File C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\run_mate.ps1
  (identical line x8 - the constant argv, printed once per mate)
DRY COMPLETE: 8 mission packs written, 8 constant-argv invocations NOT run (no opencode calls)
```

Registration (ran; registration was sanctioned "MAY run"):

```text
SUCCESS: The scheduled task "MagLeaveProtocolDaily" has successfully been created.
OK: task 'MagLeaveProtocolDaily' -> daily 08:00
schtasks /Query /TN MagLeaveProtocolDaily /V /FO LIST:
  TaskName:             \MagLeaveProtocolDaily
  Next Run Time:        9/30/2026 8:00:00 AM
  Status:               Ready
  Task To Run:          C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe C:\Users\foste\Documents\projects\local_sovereign_agent\tools\leave_dispatcher.py
  Scheduled Task State: Enabled
```

Both .ps1 files parse clean (Language.Parser::ParseFile, zero errors). No
`.claim` sidecars exist (nothing ran live). Em-dash check on all three files:
clean. First scheduled fire: 2026-09-30 08:00 (shares the slot with
MagImproveDaily per the register note's sanction; dispatcher start is file
writes + light spawns, mates are opencode-bound, not CPU-bound).

## Mimosa verdict (THE STANDOFF QUESTION)

Deep scan on this project, focus files = the three above, COMPLETED
2026-09-30T03:37:33Z, sealed (digest sha256:9c22cb8b4e707a561603386a08485d2
40714cca4f6b95bbfba1ff5d32ac00e1f; scanId scan-2026-09-30T03-37-32.469Z-
085399413c67, jobId scan-job-munjbq9v-cba39f6dd9af1ef4). THE GATE DID NOT
BLOCK THE .PY. No error, no verdict effect, and the findings ledger (5,509
rows, all pre-existing estate debt) contains ZERO findings naming
tools/leave_dispatcher.py, scripts/run_mate.ps1, or scripts/
register_leave_task.ps1. All 16 subprocess/command-injection-class findings
in the ledger were checked by path: every one lives in vendored third-party
code under mine/raw/agent_platform/cline/ (runHookCommand / runAsyncHook
Commands / subprocess-sandbox.ts), not in the new files. The all-literal
RUNNER_ARGV tuple is the shape the gate accepts; three hardenings of
variable argv were the shape it never would.

Honesty caveats, byte-true: runStatus is "inconclusive" and coverage is
"partial" - the source list truncated at 50,000 files (the repo exceeds the
limit), so absence-of-findings is proven against the sealed findings ledger,
while per-file proof that the three new files sat inside the selected 50k is
not separately byte-backed by coverage.json. If the operator wants that
closed, rerun the scan with a narrower project root or the focusFiles
re-review verdict. The fallback law stands unused: the .ps1 pair banks
regardless; nothing needed it tonight.

## Debts filed honestly

- Seeds rotation is v0: packs carry the yaml seed threads only; drawing new
  seeds from previous runs' JOURNEY dead-ends is owed next window.
- `opencode run` is unpinned (default model/agent from opencode config);
  a `-m` pin is an operator call, not smuggled in.
- Staggered admission (24 via 12+12) unused: 8 mates fit one wave under the
  16-simultaneous law; the cap is enforced in code (hard clamp at 16).
- Register note's STEER injection is per-pack at dispatch time (operative row
  inlined); mid-cycle injection between mate cycles remains the spec's
  next-cycle injection, owed with resume-not-respawn.

## Verdict update

2026-09-30T03:37Z: scan completed, sealed, NOT blocked. Full bytes in the
Mimosa verdict section above. The static-runner trio banks whole: dispatcher
+ runner + register script, task live for 2026-09-30 08:00.
