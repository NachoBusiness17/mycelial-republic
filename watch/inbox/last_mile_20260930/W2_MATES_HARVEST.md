# W2 - MATES HARVEST (2026-09-30, ~06:09-06:15 EDT)

Question: did MagLeaveProtocolDaily fire at 08:00? Answer: NO, and it is NOT
late. Nothing to harvest yet; the chain was instead proven live so the 08:00
fire has only the opencode agent call left unproven. One real defect filed
(STEER line 7). No commit made.

## 1. Task state (schtasks /Query /TN MagLeaveProtocolDaily /V, 06:08 EDT)

```text
Last Run Time:   11/30/1999 12:00:00 AM   (never ran)
Last Result:     267011                   (0x41303 = task has not yet run)
Next Run Time:   9/30/2026 8:00:00 AM
Status:          Ready / Enabled, Daily 08:00, Start Date 9/29/2026
Task To Run:     <repo>\.venv\Scripts\python.exe <repo>\tools\leave_dispatcher.py  (live, no --dry)
```

Machine clock at check: 2026-09-30 06:09 EDT (PowerShell Get-Date, Eastern).
The X12 window registered the task ~23:2x on 9/29, after that day's 08:00
slot, so the FIRST fire is today 08:00, roughly 1h50m ahead of the check.
The mission premise "it's now past that" is wrong against the clock: not a
missed fire, an imminent one.

## 2. Artifact census (all paths absolute under repo root)

- logs/mates/dispatcher_20260929.log: the X12 ordered DRY run only
  (23:17:28, 8 packs, dry=True, zero runner calls).
- logs/mates/missions/: 8 packs mission_20260929_* (23:17) plus 8 packs
  mission_20260930_* (written by my dry proof at 06:12, see section 4).
  ZERO .claim sidecars anywhere: no mate has ever been claimed or run.
- logs/mates/runs/: did not exist before 06:12 (runner had never executed).
- watch/inbox/mates/: DOES NOT EXIST. The brief's path is wrong; the
  contracted receipts root is watch/inbox/mates_leave_protocol/receipts/,
  which exists and is EMPTY (created 23:17 by the dry run's mkdir).
- logs/mates/night_burn_20260930.jsonl + n5_refire_20260929.jsonl: NOT mate
  journeys. They are banked glm-5.3-prime asks (N1 operator-model hostile
  audit, N2 baseline attack, N3 build order, N4 LDT experiment design,
  N5 oral-law schema v2 critique + refire, N6 essay grade), pointers only;
  their harvesting belongs to the night-burn lane, not the mates.

## 3. Harvest verdict

The mates did NOT fire, so there are no JOURNEY sections, top threads, or
dead ends to harvest. Receipts dir empty, claims zero, runs zero.

## 4. Diagnosis and chain proof (W3T law: prove the chain before the fire)

Every link re-proven live this morning, in the safe order (runner BEFORE
packs existed, so no real claim could happen by accident):

1. Runner: hand-ran the exact constant argv
   `powershell -NoProfile -ExecutionPolicy Bypass -File <repo>\scripts\run_mate.ps1`
   -> `[2026-09-30 06:12:11] no unclaimed mission for 20260930 ... honest
   no-op, exit 0`, log landed in logs/mates/runner_20260930.log. Claim loop,
   mkdir law, and logging all proven.
2. Dispatcher: `.venv/Scripts/python.exe tools/leave_dispatcher.py --dry`
   -> exit 0, wrote 8 packs mission_20260930_01..08 (cartographer,
   locksmith, archaeologist, innkeeper, jester, lamplighter, mariner,
   gambiter), zero subprocess calls. Venv deps, mates.yaml parse, and STEER
   injection proven. The 08:00 live fire will see these packs as "mission
   exists (kept, claims in flight are sacred)" and go straight to the 8
   live spawns (width 8, under the 16 cap).
3. opencode path: `Get-Command opencode` resolves to
   C:\Users\foste\AppData\Local\hermes\node\opencode.ps1; the hardcoded
   fallback C:\Users\foste\AppData\Local\hermes\node\opencode.cmd EXISTS;
   `--version` -> 1.18.23, exit 0.

Unproven remainder: exactly one link, the first live `opencode run <prompt>`
agent call, which cannot be proven without spending a real mate run. It
fires at 08:00.

## 5. Defects and risks filed

- DEFECT (real, minor, operator call): watch/inbox/STEER.md line 7 is a
  malformed row: `{"ts": "2026-09-30", "law": "COMPUTE LADDER (operator
  correction): ..."}` uses the key "law" and carries no "mate" and no
  "steer", so tools/steer_read.py WARNs (`malformed row line 7:
  missing/empty required field(s): mate, steer`) and DROPS it. The COMPUTE
  LADDER correction therefore reaches ZERO mission packs; every pack
  carries only the line-6 row st_20260930_seed_1 ("keep rolling 24 wide;
  proven seats only; dogfood gps"). Not silently fixed by me: the channel
  header says a landed row is never rewritten, that is an incident. Fix is
  an operator append of a well-formed row (mate + steer + ts + via) or
  relocating the law text to its proper channel.
- RISK (registration, not fixable from this seat): Logon Mode is
  "Interactive only" and no "run as soon as possible after a missed start"
  is set, so if the console session is logged OUT at 08:00 the fire is
  missed silently (Last Run stays 11/30/1999). Currently logged on, so the
  default path holds.
- RESIDUE (harmless): the 8 mission_20260929_* packs are unclaimable by
  design (the runner matches mission_<Today>* only). Orphaned dry-run
  output; deleting them is cosmetic, left in place.

## 6. What to check at/after 08:00

1. `schtasks /Query /TN MagLeaveProtocolDaily /V` -> Last Run Time today,
   Last Result 0.
2. logs/mates/runner_20260930.log -> 8 START + 8 END lines.
3. logs/mates/missions/ -> 8 .claim sidecars with exit verdicts.
4. watch/inbox/mates_leave_protocol/receipts/ -> receipt_20260930_<mate>.md
   files with FINDINGS / JOURNEY / COUNTS.

## COUNTS

Real numbers only: schtasks queries 2 (06:08, cmd via cmd //c), clock checks
2, runner hand-run 1 (no-op), dispatcher dry runs 1 (8 packs), opencode
version checks 1, STEER WARNs observed 8 (one per mate at pack time),
claim sidecars 0, receipts 0, commits 0.
