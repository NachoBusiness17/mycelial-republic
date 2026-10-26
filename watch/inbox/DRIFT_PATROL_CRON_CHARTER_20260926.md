# drift-patrol-cron writer charter (2026-09-26, burn brief B2-211)

The writer behind 194 register events in watch/inbox/index_events.jsonl
(writer id "drift-patrol-cron", ALL in UTC hour 12, daily ~12:03-12:06Z,
2026-09-14 through 2026-09-26) has NO on-disk source on this host. This
charter is the contract that writer must follow, so the next patrol audit
checks a spec instead of observed work, and whoever finds the job definition
applies it in one pass.

## Hunt result (what this lane measured)

- Host schtasks census: 337 tasks; every Mag*/Estate* task enumerated
  (MagCensusPatrolDaily, MagFtsIndexDaily, Estate Spine Index, Estate Cooker,
  OpenClaw Gateway, ...); ZERO named or containing drift-patrol. "Estate Spine
  Index" runs tools/index/projects_index.py, not the patrol; no task fires in
  the 12:0xZ window (12:03Z = 08:03 ET).
- Repo grep (scripts/ tools/ mag/): zero source carrying the writer name; only
  the fold-host comments at scripts/index_fold_host.mjs:113 and :203 naming the
  writer's mint defect.
- Containers (mag-sovereign, mag-worker): no user crontab; /etc/cron.d holds
  only e2scrub_all.
- Seat attribution: the minted paths are composed
  (/board/inbox/C:/Users/.../watch/inbox/...; index_events.jsonl line 3053),
  which is only mintable by a writer whose INBOX ROOT is /board/inbox, i.e.
  the OpenClaw/board seat, not this Windows host. The OpenClaw gateway is
  currently closed (ws://127.0.0.1:18789 transport error; openclaw.json carries
  no cron key), so the job definition in the gateway's cron store is
  UNREACHABLE from this session. Filed as owed: inspect the OpenClaw gateway
  cron store while it is up and rewrite the job body to the contract below.

## Writer contract (binding once the job is found)

1. Mint inbox-relative paths ONLY (burn_wave_20260926/QUEUE.md, never
   /board/inbox/<absolute-host-path>, never a Windows drive prefix). The fold
   now absorbs composed paths (B2-149 + B2-157, index_fold_host.mjs) but
   absorption is a repair, not a writer license (B2-41 writer-contract
   precedent for md_record_seal.py).
2. Living rows: for every file in
   watch/inbox/burn_wave_20260926/B2_292_living_rows_20260926.json (15 rows,
   including LINKS.jsonl and burn_wave_20260926/QUEUE.md) register with
   `add --living` or `add --living-open`, or register an explicit per-row
   skip. Whole-file hash refreshes of living rows are the disease quantified
   in B2_292_drift_patrol_living_20260926.md (11 whole-file LINKS.jsonl
   registers in one day). Law: LIVING_HASH_LAW_20260926.md point 6.
3. Never re-register a file whose bytes did not change since its last
   register (the refresh habit is the B2-145/B2-292 phantom-and-churn class).
4. Shared-file laws apply to the writer like any lane: board edits carry
   claims (QUEUE.md claim law); effects stay switchboard-authorized.

## Owed (named, not claimed)

- Open the OpenClaw gateway cron store (gateway up), find the drift-patrol
  job, rewrite its minting to contract item 1 and its refresh step to item 2,
  then verify one daily fire produces zero whole-file registers for the 15
  living rows and zero composed paths.
