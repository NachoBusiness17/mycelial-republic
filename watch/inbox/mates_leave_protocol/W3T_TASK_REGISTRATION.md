# W3T — scheduled-task registration (Mickey17 W3, 2026-09-29)

Lane: W3 (task registration). Operator "keep rolling" order covers the
operator-call registrations. Mission: register the three orphaned scheduled
tasks that landed today; FTS already existed (skip confirmed by bytes).

## Outcome

| Task | Script | When | State |
|---|---|---|---|
| MagGateCanaryDaily | `scripts/register_gate_canary_task.ps1` | daily 09:45 | registered + verified Ready/Enabled, next run 2026-09-30 09:45 |
| MagGapSentinelDaily | `scripts/register_gap_sentinel_task.ps1` (new) | daily 08:15 | registered + verified Ready/Enabled, next run 2026-09-30 08:15 |
| MagFtsIndexDaily | (existing) | daily 09:00 | verified Ready, next run 2026-09-30 09:00 — untouched |

Daily lane order now: 08:00 improve / 08:15 gap sentinel / 08:30 census
patrol / 09:00 FTS index / 09:45 gate canary. No overlap.

## Defect found and fixed (build discipline: align the design, no guard branch)

`scripts/register_gate_canary_task.ps1` as landed (W2 return 7/24) built its
schtasks /TR as an inline `powershell.exe ... -Command "& 'py' 'tool' *>> 'log'"`.
Windows PowerShell 5.1 mangles embedded double quotes when passing /TR to
schtasks.exe, so the first run died BEFORE creating any task:

```text
ERROR: Invalid argument/option - ''C:\Users\foste\Documents\projects\local_sovereign_agent\.venv\Scripts\python.exe''.
WARN: schtasks create failed (exit -2147467259).
```

Not a permissions failure — the inline form can never register from any
console. Fixed by aligning to the byte-proven census pattern
(`register_census_patrol_task.ps1` -> `census_patrol_daily.ps1`, registered
2026-09-26, runs clean daily): a `-File` wrapper with zero embedded quote
pairs in /TR.

Files:
- NEW `scripts/gate_canary_daily.ps1` — wrapper: logs to `logs/gate_canary.log`
  (UTF-8 Add-Content, no Tee-Object — B2-246 law), passes exit code through.
- EDIT `scripts/register_gate_canary_task.ps1` — /TR now `-File gate_canary_daily.ps1`;
  fix comment carries the cause + evidence.
- NEW `scripts/gap_sentinel_daily.ps1` — same wrapper law for
  `tools/gap_sentinel.py`, log `logs/gap_sentinel.log`.
- NEW `scripts/register_gap_sentinel_task.ps1` — census pattern from birth.

Both tools self-alert to `memory/attention.md` (single-writer law), so the
wrappers only stamp and pass exit codes.

## Verification bytes

Register (both run via `powershell -ExecutionPolicy Bypass -File`):

```text
SUCCESS: The scheduled task "MagGateCanaryDaily" has successfully been created.
OK: task 'MagGateCanaryDaily' -> daily 09:45
SUCCESS: The scheduled task "MagGapSentinelDaily" has successfully been created.
OK: task 'MagGapSentinelDaily' -> daily 08:15
```

`schtasks /Query /TN ... /V /FO LIST`:

```text
\MagGateCanaryDaily  Next Run 9/30/2026 9:45:00 AM  Ready
  Task To Run: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\gate_canary_daily.ps1
  Scheduled Task State: Enabled
\MagGapSentinelDaily Next Run 9/30/2026 8:15:00 AM  Ready
  Task To Run: powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\foste\Documents\projects\local_sovereign_agent\scripts\gap_sentinel_daily.ps1
  Scheduled Task State: Enabled
\MagFtsIndexDaily    Next Run 9/30/2026 9:00:00 AM  Ready   (pre-existing, untouched)
```

First live runs by hand (prove the chain before tomorrow's first scheduled
fire — the instruments-built-not-run disease):

```text
# gap sentinel wrapper
[2026-09-29 22:27:27] START gap sentinel cwd=C:\Users\foste\Documents\projects\local_sovereign_agent
GAP-SENTINEL: ok - baseline: no prior rollup snapshot to diff, run 2026-09-29T14:23:05+00:00 recorded
GAP-SENTINEL: ok - sensor dashboard/static/x_radar.json fresh (mtime age 0.60d of 2.0d bar)
[2026-09-29 22:27:27] END exit=0

# gate canary wrapper (exit 1 = a gate was dead/blind: the canary working, not a registration fault)
GATE-CANARY: attention alert filed for caption_ledger_verify (DEAD)
GATE-CANARY: attention alert filed for refold_gate (BLIND)
[2026-09-29 22:27:34] END exit=1
```

## Findings handed to the operator (canary's own output, not this lane's fix)

The canary's first run flagged real gate-health findings and filed them to
`memory/attention.md` per its design: `caption_ledger_verify` DEAD
(RecursionError tail), `refold_gate` BLIND, and scenario card
`G1_multiplicity.card.json` expected PASS got FAIL. W3A/W3B receipts in this
folder claim fixes for the first two — verify against the attention rows
before trusting any push.
