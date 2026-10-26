# B2-211 receipt: drift-patrol-cron writer charter (2026-09-26)

## Verdict

LANDED as charter + absence-filed-as-owed. The cron job definition was not found on this host and could not be fixed, so per the brief's own alternative arm its absence is filed with the writer contract written: watch/inbox/DRIFT_PATROL_CRON_CHARTER_20260926.md. The hunt narrowed the writer to the OpenClaw/board seat on byte evidence (minted /board/inbox/C:/... composed paths are only mintable where the inbox root is /board/inbox) and the job store is unreachable this session (OpenClaw gateway closed, ws://127.0.0.1:18789 transport error). Cadence pinned exactly: 194 events, all in UTC hour 12, daily ~12:03-12:06Z, 2026-09-14 through 2026-09-26 (still firing).

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/QUEUE.md (B2-211 row): "the mint source of /board/inbox/C:/Users/.../watch/inbox/burn_wave_20260926/QUEUE.md (index_events.jsonl:3053, writer drift-patrol-cron, 12:03Z daily runs) has NO on-disk source (grep of scripts/ tools/ mag/ finds only the fold warning comment)".
- watch/inbox/index_events.jsonl:3053: the composed-path register from writer drift-patrol-cron (verified this lane).
- scripts/index_fold_host.mjs:113 and :203: the fold-host comments naming drift-patrol-cron as the composed-path minter (the only repo occurrences of the name).
- Measured this lane: schtasks //query //fo CSV = 337 tasks; non-Microsoft set is {AMDRyzenMasterSDKTask, cua-driver-serve, Estate Cooker, Estate FullScan, Estate Gopher, Estate KeyAudit, Estate LaneSupervisor, Estate Librarian, Estate Ratchet, Estate Spine Index, Estate StealthSweep, mag-docker-watchdog, MagCensusPatrolDaily, MagCorpusRescanDaily, MagEndpointNewsDaily, MagFtsIndexDaily, MagImproveDaily, MagLabKit8765, MagMimoWatchClose, MagMimoWatchHourly, MagPrivateOffice8765, MagQCaptionVerifyDaily, MagVisionNightly, OpenClaw Gateway, StartCN, StartDVR, vast-bargain-loop}; zero drift-patrol. "Estate Spine Index" task XML Command = .venv\Scripts\python.exe tools/index/projects_index.py (not the patrol).
- Cadence census over index_events.jsonl: 194 drift-patrol-cron rows, hour histogram {12: 194}, first 2026-09-14T12:06:45+00:00, last 2026-09-26T12:05:56+00:00.
- Containers: docker ps shows mag-sovereign / mag-worker / mag-redis up; mag-sovereign crontab empty, /etc/cron.d holds only e2scrub_all. OpenClaw: openclaw cron list fails "GatewayTransportError: gateway closed (1006)"; openclaw.json carries no cron key; gateway.vbs launches gateway.cmd (OpenClaw v2026.7.1-2).

## Work done

1. Ran the brief's hunt arms with real outputs: schtasks census (337 tasks, zero drift-patrol), repo grep (only fold comments), container crontab checks (empty), OpenClaw gateway probe (down, cron store unreachable), openclaw.json inspection (no cron key).
2. Pinned the writer's fingerprint on bytes: cadence, volume (194 events), path shape (/board/inbox/ prefix = board seat), and lifetime (2026-09-14 to 2026-09-26).
3. Wrote watch/inbox/DRIFT_PATROL_CRON_CHARTER_20260926.md: the binding writer contract (inbox-relative minting per the B2-41/B2-157 fold contract; living adoption per law point 6 pointing at B2_292's 15-row register; no unchanged re-registration; shared-file claim law applies), plus the owed arm (open the gateway cron store, rewrite mint + refresh steps, verify one clean fire).
4. Interlocked with B2-292 (same lane): the charter's item 2 adopts B2_292_living_rows_20260926.json as the target list, so one fix closes both briefs.

## Falsifier

The charter dies if: (a) the OpenClaw cron store is opened and holds no drift-patrol job, meaning the writer is yet another seat entirely (the charter's attribution section is then wrong and must be re-filed); (b) the next 12:0xZ fire after a contract rewrite still mints a composed path or a whole-file refresh of a living row (grep index_events.jsonl for writer drift-patrol-cron with "/board/inbox/" after the fix date must return zero); (c) a 12:03Z fire is missed entirely (the writer died instead of being fixed, which is a different closure than this charter's owed arm).

## Bibliography closed

All read this lane: watch/inbox/index_events.jsonl (writer census, line 3053), scripts/index_fold_host.mjs (:113, :203, mint normalization block), schtasks //query (337 tasks) + //xml for Estate Spine Index and OpenClaw Gateway, docker ps + crontab checks (mag-sovereign, mag-worker), C:\Users\foste\.openclaw\openclaw.json (key census, no cron), gateway.vbs/gateway.cmd, openclaw cron list (transport error), watch/inbox/LIVING_HASH_LAW_20260926.md, B2_292_living_rows_20260926.json, QUEUE.md B2-211 row.
