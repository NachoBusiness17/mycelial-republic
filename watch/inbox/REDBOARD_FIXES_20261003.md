# REDBOARD FIXES 2026-10-03 (overnight wave, Grok Bot executor)

STATUS: PARTIAL. The PC (DESKTOP-7C70KSC) dropped off local-exec around 23:30 ET and was still offline at close. So this receipt was written on the box and is NOT yet on disk at watch/inbox/. The after meter (tools/redboard.py --json) was NOT run. Wave protocol followed: bounded chunks, failures filed too, no commits.

## Meters
- BEFORE (state/REDBOARD.json, 19:36 ET): METER 8 red | worst streak 9d (Estate Ratchet) | 5 seat-fixable | 3 operator-needed | alarms 12 types / 1030 lines | stealth dead routes 2
- AFTER: NOT RUN (PC offline). Also note: redboard reads each scheduled task's Last Result, so hand runs don't flip a task green until its next scheduled fire.

## Self-steal (reused)
- watch/inbox/W2_ZERO_COLLECT_20260929.md: cure is "rename/convert, never tolerance".
- watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md: x_radar revived 19:40 ET (grok.exe path); GROWTH drivers; LeaveProtocol left open.
- commit 025fb2ba0 LITE LANE PULL (20:44 ET): ZAI_API_KEY_Lite commented in .env, configs re-sealed 20:42 ET.
- watch/inbox/KEY_LAW_20260923.md: GROK_API_KEY was an empty placeholder slated for deletion.
- watch/inbox/audit_20260926/WAVE2_LANE1_DISK_MAP.md: dashboard/data/ESTATE_INDEX.jsonl is tracked (590 MB then).

## Fixes applied (backups *.bak-20261003w)
1. MagCensusPatrolDaily ZERO-COLLECT [known, first seen 2026-09-29]
   Cause: tests/test_selffeed_integration.py is a __main__ script with zero test functions. If it collected, it would fire hermes and append to the live stealth work queue.
   Fix: renamed it to tests/selffeed_integration_check.py (moved, contents unchanged). Backup: tests/test_selffeed_integration.py.bak-20261003w.
   The file is missing from disk because of this rename. It was not lost. Do not restore it under test_*.py.
2. COLLECT-DRIFT +41 [NEW 2026-10-03]
   Cause: an instrument mismatch. The 20:30 ET carrier ran `pytest --collect-only -q tests`, which leaves out tools/gps_mcp (41 tests, 1 file). The patrol uses the default testpaths. Either way `tests` alone reads 4,216.
   Fix: refreshed the AGENTS.md **Tests:** carrier to 4,257 / 504 and kept the parse grammar. Backup: AGENTS.md.bak-20261003w.
3. census_patrol_daily.ps1 fossil-alert bug [NEW 2026-10-03]
   Cause: `"@` and ` -Encoding utf8` sat on separate lines, so PowerShell threw "-Encoding is not recognized" and the WARN log line was skipped.
   Fix: joined them into `"@ -Encoding utf8`. Parse errors: 0. Backup: scripts/census_patrol_daily.ps1.bak-20261003w.
   Verify (hand run 23:09 ET): "collect ok ... pytest 4257 vs carrier 4257 (delta +0) ... every disk candidate collects items", "FOSSIL-CHECK: WARN alert appended", END exit=0.

## Seat items verified, no edit needed
- MagGapSentinelDaily SENSOR-SILENCE [known, first seen 2026-10-01]: cleared by the sibling's x_radar revive. Hand run 23:04 ET: "sensor x_radar.json fresh (0.14d of 2.0d bar)". I did NOT retire XRadar: it is live again, and the X intake desk is only a proposal (OPERATOR_WORKFLOW_DIVE_20261003.md).
  It is still exit 1 on GROWTH (10.60 GiB/day) [known since 2026-10-01]. I left the threshold alone. New sub-finding: the git-tracked 3.4 GB ESTATE_INDEX.jsonl is stored twice (watch/ + dashboard/data) and gets swept into broad commits (5d2263f10, ecf47999a). .git/objects grew 6.9 GiB in 24h.
- Estate Spine Index 0xC000013A [NEW 2026-10-03]: the 09:00 run finished every output by 10:00:02 (3498 s, 8,803,599 files). It was killed during exit, so the data is whole. I started a hand run at 23:01 ET (hidden, BelowNormal). Its result is UNKNOWN because the PC went offline. Check %TEMP%\spine_rc.txt.

## Staged, not applied
- MagLeaveProtocolDaily [known 2026-10-03; root cause NEW]: 8 opencode instances starting in the same second lock its sqlite ("database is locked"). Mates that got past that died because the unpinned model resolved to glm-5v-turbo, which the plan doesn't include. Diff: watch/inbox/REDBOARD_LEAVE_PROTOCOL_20261003.diff (20 s stagger plus `--model zai/glm-4.7`). git apply --check rc=0; leave_dispatcher --dry rc=0. Not applied because proving it needs a live 8-mate dispatch.
- Stealth routes [probe20 known 2026-09-27; rumor known 2026-09-28; status() ignoring the HELD close row is NEW]: the driver is live (pid 17732, running since 10/1), so I did not apply. Diff: watch/inbox/REDBOARD_STEALTH_ROUTES_20261003.diff. It drops probe20 from TOPICS and runs the idempotent `rumor_drill.py close` before `status`. apply --check rc=0; compiles.

## Operator steps
1. Estate Ratchet: the seal already PASSES (re-sealed 20:42 ET by zcode-53). Before 09:45, run `.venv\Scripts\python.exe tools\config_seal.py verify`. If configs/mirrors.json has drifted again, run `python tools/config_seal.py update --by <you> --note "<why>"`. Then decide whether mirror runtime state should move out of configs/.
2. TipWitness 403: mint a fine-grained PAT with Account permission Gists: Read and write, or a classic PAT with gist scope. Put it in .env as GITHUB_TOKEN (key_law github_token). Then run `powershell -File scripts\tip_witness_daily.ps1`.
3. XRadar: no grok CLI step needed any more (fixed 19:40 ET). Just watch the 08:00 fire.
4. Estate KeyAudit [NEW 2026-10-03]: zai_lite is empty because of tonight's Lite pull, and GROK_API_KEY now has a value but isn't declared. In configs/keys.json, mark zai_lite dormant/awaiting, and either declare GROK_API_KEY or remove it from .env. Then re-seal configs.
5. Growth: `git rm --cached` both ESTATE_INDEX.jsonl copies and add them to .gitignore (needs your commit).
6. Apply the two diffs if you agree: `git apply <diff>`. Restart the stealth driver for its diff to take effect.


## ADDENDUM 2026-10-04 05:00 ET (PC back online)

- Receipt copied to watch/inbox (it was drafted on the box during the outage).
- Selffeed rename confirmed against `git log --all -- tests/test_selffeed_integration.py`. Two commits touch it: 0b4ca2d2f (2026-09-29, hygiene lane banked the file) and a7ca49be1 (2026-10-04 02:15 ET, author Codex). Codex committed my working-tree changes in that sweep: a pure rename to tests/selffeed_integration_check.py (0 line changes), plus AGENTS.md and scripts/census_patrol_daily.ps1. The ps1 shows 389 changed lines; this looks like CRLF/LF normalization by git, not content. The file was never lost, so it was NOT restored. Restoring it as test_*.py would bring back ZERO-COLLECT.
- Spine Index hand run: NO RESULT. %TEMP%\spine_rc.txt does not exist. spine_out/err are 0 bytes from the first launch (23:01:19, killed by me within seconds). The cmd wrapper launched at 23:01:51 never ran the indexer: no output files, no process, and watch/ESTATE_INDEX/last_run.json is unchanged at 2026-10-03 10:00. The most likely cause is a quoting failure in cmd /c. Not re-run: it takes about 58 min and rewrites about 6.8 GB, and the scheduled fire is at 09:00. Verdict stays as written above: the 09:00 10-03 run finished all outputs and was killed at exit. Watch the 10-04 09:00 result.
- AFTER meter (tools/redboard.py --json, 2026-10-04 04:58 ET, rc=0):
  METER 8 red | worst streak 9d (Estate Ratchet) | 5 seat-fixable | 3 operator-needed | alarms 14 types / 279 lines | stealth dead routes 3
  Red: Estate Ratchet 0x1 9d; MagTipWitnessDaily 0x2 4d; MagGapSentinelDaily 0x1 3d (GROWTH only); MagLeaveProtocolDaily 0x1 3d (runner exit=1 at 2026-10-04 04:43:48, a fire I did not start); Estate KeyAudit 0x1; Estate Spine Index 0xC000013A; MagCensusPatrolDaily 0x1; MagXRadarDaily 0x2.
  Why the count did not drop: redboard reads the Last Result of each scheduled task. My hand runs (census exit 0 at 23:09, gap sensor-silence cleared at 23:04) and the sibling's x_radar run (exit 0 at 19:40) don't change that field. Census, XRadar and the gap sensor line should clear at the 08:00-08:30 fires. Alarm lines dropped 1030 -> 279 (sibling attention.md dedup, not this wave).
  Dead routes 3: probe20 and rumor (diff staged), plus fossil [NEW 2026-10-04 as a dead route; known as a WARN 2026-10-03]: memory/improve/SEATS.md is stale past the 168h bar. The fix is a SEATS recompile, which is operator/seat content and was not done.
