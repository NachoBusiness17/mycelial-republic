# THE LONGRUNNERS-CAGED LAW: containers by default, lessig not prose

- Operator order 2026-10-07 (verbatim intent): "what long running processes
  should be in containers by default so we lessig this shit rather than asking
  in prose."
- Law carrier: configs/longrunner_policy.json (tiers, allowlist, threshold,
  staged migration rows R1-R4). Enforcement tooth: tools/longrunner_patrol.py
  via MagLongrunnerPatrolDaily 08:45 (registered, schtasks SUCCESS).
- Founding incident: run_armC.py (interference_replication_20260925), 24.4
  CPU-hours over 11 days at ~1 live core, killed 2026-10-07T00:30Z.

## The ruling

- TIER A (caged by default): everything the compose already cages (mag,
  redis, openclaw stack, mcp, worker beat loop) PLUS the scheduled burn
  cycles (fleet, gauntlet, hermes_247, lawpack, patrols) and experiment arms.
  The Task Scheduler clock stays host-side; the WORK moves into a `burners`
  compose service (staged row R1: same image, watch/ + memory/runs volumes,
  cpus 2.0, mem 2g, pids_limit 64, no-new-privileges, cap_drop ALL). An
  11-day runaway is structurally impossible behind that fence.
- TIER B (host by necessity): Task Scheduler itself, Docker Desktop + vmmem,
  seat processes (ZCode/opencode), LM Studio/Bionic GUI.
- TIER C (violations): any interpreter older than 120 min outside the
  allowlist. The patrol alerts; it never kills (a live seat's work must not
  die to a patrol - the sibling-stash lesson).

## First patrol run caught 20 (same sitting, before the law was an hour old)

- KILLED (unambiguously hung, cycle design <=10 min): free_lane_fleet --cycle
  twins PIDs 9144/22544 age 295 min, fleet ps1 19744, hermes_burn_247 ps1
  27080 age 287 min (its python child had already exited; the shell was
  pipe-waiting). The hourly hermes clock kept firing while shells stacked -
  a watchdog row is owed on the hermes driver (max one shell per fire).
- LEFT ALIVE pending operator ruling (sanctioned infra or duplicates?):
  run_stealth_driver.py pythonw twins age 29h, leave_dispatcher.py twins
  age 16.6h, hermes gateway + ollama serve age 29h (cage candidates),
  z_ai mcp npx quads age 16.5h.
- ARTIFACT to investigate: two processes claimed `-m tools.longrunner_patrol`
  at age 240 min, but the tool was written 5 min before the scan - either a
  WMI creation-date parse edge or PID reuse; the patrol's own rows must be
  trustworthy before its kills are ever automated.

## The stacking cure this sitting

The hung hermes/fleet ps1 shells existed because Task Scheduler kept firing
while old shells never exited. Until R2/R3 move the work into capped
containers, the practical fences are: cycle scripts get their own internal
timeout, and any task whose last shell is still alive from a prior fire is a
patrol row. The burners container closes it structurally (pids_limit + the
run --rm lifecycle).
