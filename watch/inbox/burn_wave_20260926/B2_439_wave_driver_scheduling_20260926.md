# B2-439 wave_driver scheduling truth (2026-09-26)

## Verdict

LANDED. Decision: the driver is registered TEST-DRIVEN-ONLY, not re-staged.
Fresh bytes this lane: a full schtasks census (240 task entries enumerated via
schtasks //query //fo LIST) holds ZERO wave_driver or m12_pairing entries -
the CONVO-era claim (queue/handoff/zcode/CONVO.md:1220, 2026-09-12: "CRON
staged: 21:15 driver tick + 06:45 pairing close") never survived to a real
scheduled task. Re-staging was rejected on governance grounds, not laziness:
the driver is an autonomous ACT-capable loop with a steer-signature gate and
operator-facing M12 event counting, so a nightly cron is an operator-scale
GO, and the estate now has a canonical place to record one
(watch/inbox/OPERATOR_GO.jsonl, gate "wave-driver-night-cron", landed this
wave by B2-425). The registration block lives in the organ doc itself
(scripts/wave_driver.py docstring) and the CONVO-era pointer carries a dated
appended correction (transcript preserved, no rewrite).

## Evidence file:line quotes

- Fresh census (this lane): schtasks //query //fo LIST -> 240 "TaskName:"
  entries; the non-vendor set is {AMDRyzenMasterSDKTask, cua-driver-serve,
  Estate Cooker, Estate FullScan, Estate Gopher, Estate KeyAudit, Estate
  LaneSupervisor, Estate Librarian, Estate Ratchet, Estate Spine Index,
  Estate StealthSweep, mag-docker-watchdog, MagCensusPatrolDaily,
  MagCorpusRescanDaily, MagEndpointNewsDaily, MagFtsIndexDaily,
  MagImproveDaily, MagLabKit8765, MagMimoWatchClose, MagMimoWatchHourly,
  MagPrivateOffice8765, MagQCaptionVerifyDaily, MagVisionNightly, OpenClaw
  Gateway, StartCN, StartDVR, vast-bargain-loop}. No wave_driver, no m12.
- The stale claim: queue/handoff/zcode/CONVO.md:1220 "[zcode 2026-09-12T01:14:38Z
  EXECUTION WAVE: T4 M12 ARMED-NIGHT PAIRING BUILT ... CRON staged: 21:15
  driver tick + 06:45 pairing close. TESTS 16/16 green ...]".
- The registration, scripts/wave_driver.py docstring (post-edit, lines 4-17):
  "SCHEDULING TRUTH (B2-439, registered 2026-09-26): this driver is
  TEST-DRIVEN-ONLY. ... The loop runs under tests/test_wave_driver.py +
  tests/wave_driver_test.py and by MANUAL LAUNCH only ... Re-staging a night
  cron ... requires a recorded operator GO - transcribe it into
  watch/inbox/OPERATOR_GO.jsonl (gate 'wave-driver-night-cron') before
  registering any task."
- The correction, queue/handoff/zcode/CONVO.md foot (appended, dated
  2026-09-26T20:50Z): names the 1220 entry, the census, and the GO door;
  "This is an appended correction, not a rewrite of the 09-12 bytes."
- The run-surface claim verified: tests/test_wave_driver.py and
  tests/wave_driver_test.py both exist on disk. Test run: 6 passed / 1
  failed, the failure being PermissionError WinError 5 on
  agents/pytest-tmp-22120 (pre-existing host environment issue, the
  AGENTS.md census' known-failed class; unrelated to this lane's
  docstring-only edit, and it reproduces identically before and after).

## Work done

1. Ran the fresh schtasks census (240 tasks; note schtasks /query needs
   // escaping under Git Bash - /query was being path-mangled to
   C:/Program Files/Git/query on the first attempt).
2. Located the CONVO-era pointer (CONVO.md:1220) and confirmed no scheduled
   task ever landed from it.
3. Wrote the SCHEDULING TRUTH registration into scripts/wave_driver.py's
   docstring (spec-first placement; ast.parse green).
4. Appended the dated correction to CONVO.md (append-only).
5. Chose register-not-restage, with the GO door named for any future
   re-stage. Filed this receipt; LEDGER row; QUEUE pointer; INDEX
   registration.

## Falsifier

This registration is inverted if any of the following holds: (a) a schtasks
census after this date shows a wave_driver/m12_pairing task WITHOUT a
corresponding row in watch/inbox/OPERATOR_GO.jsonl gate
"wave-driver-night-cron" (someone staged the cron without the operator GO
the registration demands); (b) a receipt dated before 2026-09-12 surfaces
proving the 21:15/06:45 tasks existed and were deliberately removed without
a receipt (the "never went live" reading is wrong); (c) the driver's
HEARTBEAT_TTL_S logic (scripts/wave_driver.py:66-84 region) is cited by a
live organ as currently-tick-fed while this registration stands (prose
drift reopened).

## Bibliography closed

scripts/wave_driver.py (read: header, constants incl. HEARTBEAT_TTL_S and
the M12 pairing block at :66-84 region; edited: docstring registration
block); queue/handoff/zcode/CONVO.md:1125-1299 context entries + :1220
(the staged-cron claim; appended correction); schtasks census (fresh, this
lane); tests/test_wave_driver.py + tests/wave_driver_test.py (existence
verified, suite run with the pre-existing failure disclosed);
watch/inbox/OPERATOR_GO.jsonl + tools/operator_go.py (the GO door this
registration binds re-staging to, landed this wave by B2-425);
watch/inbox/burn_wave_20260926/B2_96_scripts_triage_20260926.md (accepted
from the brief as the pointer source). No network calls.
