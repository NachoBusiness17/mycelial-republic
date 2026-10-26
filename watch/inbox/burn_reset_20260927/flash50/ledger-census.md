# f-26: JSONL ledger census (every .jsonl in the repo, .venv/.git excluded)

Item f-26, generated 2026-09-28. Instrument: `watch/inbox/burn_reset_20260927/flash50/_f26_sweep.py`
run with `./.venv/Scripts/python.exe` (mag venv), walking the whole repo excluding only `.venv` and
`.git`. Row = one non-empty line. Schema = distinct top-level JSON key tuples per file (json.loads
every row for files <= 20 MB; first 20,000 rows sampled for the 25 files above that). Reader claims
are literal-string greps over mag/ tools/ scripts/ backend/ + root *.py / *.ps1 / *.json / *.yaml
(2,512 files scanned), then hand-verified for each named ledger below. Growth instrument: `git ls-files`,
`git check-ignore --stdin`, `git show HEAD:<path>` row counts, and `git log -1` per tracked file.

Git baseline for every delta below: HEAD `0d6ace6b06` at sweep time (HEAD moved during the
run from `862620665a` because sibling lanes commit concurrently; deltas are vs the sweep-time HEAD).

## 1. Headline totals (measured, one tree, 2026-09-28 18:30 local)

| metric | value |
|---|---|
| .jsonl files | 11854 |
| rows (non-empty lines) | 19538633 |
| bytes | 9325758540 (9.33 GB) |
| tracked in git | 486 |
| gitignored | 11364 |
| untracked and NOT ignored | 4 |
| files with >1 distinct row schema | 2598 |
| files with >=1 unparseable row | 58 (29 outside agents/ pytest leftovers) |
| empty (0-row) files | 88 |
| schema sampled (>20 MB) | 25 |
| mtime age <= 24h | 2313 |
| mtime age <= 7d | 2872 |
| mtime age > 90d | 0 |

Coverage arithmetic (asserted by the builder): A1 (41 major ledgers) + A2 (839 other non-bulk
files) + bulk trees (10974 files) = 11854 = total files. The full per-file raw dump is committed next to
this doc as `_f26_raw.json` (18.6 MB, one record per file: rows, bytes, mtime, keysets, git
status, delta vs HEAD, reader hits).

## 2. Top-level directory rollup (all 20 top dirs, no omissions)

| top dir | files | rows | MB |
|---|---:|---:|---:|
| memory | 5290 | 6115605 | 2818.7 |
| corpus | 3900 | 551255 | 1200.4 |
| agents | 2137 | 6896 | 2.1 |
| watch | 229 | 3636997 | 1363.8 |
| mine | 78 | 6221 | 5.2 |
| state | 73 | 145334 | 44.3 |
| logs | 33 | 779968 | 1292.2 |
| _archaeology_out | 24 | 1088 | 0.6 |
| queue | 24 | 5252 | 1.4 |
| dashboard | 16 | 6490367 | 2016.1 |
| dashboard-deploy | 14 | 44369 | 10.9 |
| dist_audit | 13 | 1820 | 0.4 |
| training | 12 | 580139 | 256.6 |
| catalog | 3 | 1163033 | 291.7 |
| bridge | 2 | 12 | 0.0 |
| handoff | 2 | 603 | 0.4 |
| attic | 1 | 16 | 0.0 |
| canon | 1 | 27 | 0.0 |
| outputs | 1 | 51 | 18.2 |
| research | 1 | 9580 | 2.7 |
| **total** | **11854** | **19538633** | **9325.8** |

## 3. The five giants (single files, by bytes)

| file | rows | MB | note |
|---|---:|---:|---|
| `dashboard/data/ESTATE_INDEX.jsonl` | 3485538 | 1291.7 | dashboard mirror of the estate spine, +129,962 rows vs HEAD |
| `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` | 3485538 | 1291.7 | estate spine (source of truth), same row count as its mirror |
| `memory/ingest/registry.jsonl` | 2524920 | 1291.3 | ingest registry, untracked, appended today 18:22 |
| `logs/kpi.jsonl` | 81937 | 1058.2 | KPI log, gitignored runtime log |
| `dashboard/data/ractor_board.jsonl` | 2959486 | 713.3 | ractor board mirror |

The two ESTATE_INDEX copies hold identical row counts (3,485,538 each); `tools/index/projects_index.py:31,34`
writes master + dashboard copy from one walk, so the twin is by design, not drift.

## 4. A1: the 41 named operational ledgers (rows / mtime / git / growth / schema / readers)

`git` column: T = tracked, I = gitignored, U = untracked-not-ignored. delta = rows now minus rows at HEAD `0d6ace6b06` (tracked only).

| file | rows | MB | mtime | git | delta | distinct schemas | reads/writes (verified greps) |
|---|---:|---:|---|---|---:|---|---|
| `watch/inbox/index_events.jsonl` | 5194 | 1.85 | 2026-09-28 18:28:59 | T | +672 | 8 | writer/reader mag/shared_surface.py:117 (EVENTS_LOG), fold checks :218,:253; header :22 |
| `watch/inbox/LINKS.jsonl` | 378 | 0.26 | 2026-09-28 14:29:00 | T | +1 | 8 | mag/links_sha_ratchet.py:1 (same-sha ratchet), mag/catalog_scan.py:20 |
| `watch/INBOX_LINKS.jsonl` | 254 | 0.08 | 2026-09-01 17:43:52 | I | - | 8 | no code reference found (name-pattern manual ledger) |
| `memory/decisions_log.jsonl` | 213260 | 76.36 | 2026-09-28 18:23:42 | I | - | 7 | mag/behavioral_synth.py:18, mag/compass.py:25, mag/conductor.py:78 |
| `memory/biography/verkle_chain.jsonl` | 8259 | 5.79 | 2026-09-28 18:23:32 | I | - | 5 | mag/boot_check.py:25, mag/agent_cli.py:669, mag/ai_landscape.py:161 (chain tip, read-only refs) |
| `memory/trajectory/steps.jsonl` | 30770 | 30.44 | 2026-09-28 18:27:26 | T | +3271 | 3 | LIVE tape; code pointers point elsewhere (split pointer, see anomalies) |
| `memory/agent_state/chain.jsonl` | 19855 | 10.48 | 2026-09-28 18:23:58 | I | - | 1 | mag/agent_state.py:30 (CHAIN) |
| `state/shared_activity.jsonl` | 107586 | 29.66 | 2026-09-28 18:27:06 | I | - | 1 | writer mag/coordination.py:97 (append), reader mag/falsifier_counter.py:271 |
| `logs/behavioral_events.jsonl` | 215577 | 67.10 | 2026-09-28 18:21:52 | I | - | 3 | mag/behavior_catch.py:24, mag/behavioral_synth.py:17, mag/decision_framework.py:22, mag/billing_feed.py:245 |
| `logs/kpi.jsonl` | 81937 | 1058.18 | 2026-09-28 18:21:59 | I | - | 2 | mag/records.py:17, synthesis_agent.py:24 |
| `logs/usage.jsonl` | 163107 | 70.08 | 2026-09-28 18:12:19 | I | - | 1 | mag/lanes.py:42,70 (lanes config usage_log) |
| `logs/provider_usage.jsonl` | 76574 | 25.65 | 2026-09-28 18:12:19 | I | - | 4 | mag/budget_refactor.py:39, mag/cache_map.py:32 |
| `logs/supervisor.jsonl` | 107905 | 14.18 | 2026-09-28 18:21:51 | I | - | 4 | writer mag/process_supervisor.py:43, readers mag/error_healer.py:40, mag/process_reaper.py:47 |
| `logs/failure_kb.jsonl` | 112203 | 40.46 | 2026-09-28 18:22:37 | I | - | 1 | mag/failure_kb.py:47 (authoritative log), mag/ghost.py:555 |
| `memory/ingest/registry.jsonl` | 2524920 | 1291.30 | 2026-09-28 18:22:06 | I | - | 1 | mag/ingest_registry.py:42 (REGISTRY, append-only) |
| `watch/room.jsonl` | 13866 | 4.69 | 2026-09-28 18:23:01 | I | - | 8 | writers mag/api_gateway.py:263 (client hooks), mag/chan.py:1, mag/salon_openclaw.py:91; readers mag/accumulator.py:5, mag/falsifier_counter.py:17 |
| `watch/grok_feed.jsonl` | 19333 | 9.01 | 2026-09-28 17:32:35 | I | - | 2 | mag/seats.py:214, mag/chronicle.py:124 |
| `watch/session_digest.jsonl` | 16589 | 5.65 | 2026-09-28 08:02:38 | I | - | 1 | mag/health.py:74 |
| `catalog/catalog.jsonl` | 581477 | 160.05 | 2026-09-28 03:33:10 | T | +19818 | 1 | mag/catalog.py:39 (append rows), mag/catalog_freshness.py:34, mag/catalog_rebuild.py |
| `catalog/tags.jsonl` | 581477 | 131.59 | 2026-09-28 12:45:41 | T | 0 | 1 | mag/catalog_tags.py:43, rewritten by mag/catalog_rescan.py:44 |
| `catalog/junctions.jsonl` | 79 | 0.05 | 2026-09-28 03:33:15 | T | +35 | 1 | mag/catalog_rebuild.py:75 (atomic replace from walk) |
| `memory/runs/swarm_health/trail.jsonl` | 84907 | 13.04 | 2026-09-28 18:25:31 | I | - | 2 | see raw |
| `memory/runs/governor_autorun_trail.jsonl` | 236068 | 57.59 | 2026-09-28 18:24:26 | I | - | 7 | mag/autorun_status.py:12, mag/ghost.py:167, mag/gap_analysis.py:43 |
| `memory/runs/orchestrator_trail.jsonl` | 31887 | 5.25 | 2026-09-28 17:50:54 | I | - | 8 | mag/loop_audit.py:22, mag/live_feed.py:51, mag/ghost_control.py:126 |
| `memory/bard/breadcrumbs.jsonl` | 102245 | 23.95 | 2026-09-28 18:13:44 | I | - | 1 | mag/bard.py:429,445 |
| `dashboard/data/ESTATE_INDEX.jsonl` | 3485538 | 1291.75 | 2026-09-28 09:42:46 | T | +129962 | 1 | dashboard mirror, written by tools/index/projects_index.py:34 (DASH_MASTER) |
| `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` | 3485538 | 1291.75 | 2026-09-28 09:42:36 | T | +129962 | 1 | spine, written by tools/index/projects_index.py:31 (MASTER), read by tools/estate_atlas.py:35 |
| `queue/lanes/research/trail.jsonl` | 2201 | 0.76 | 2026-09-28 18:23:01 | T | +75 | 2 | lane trail family; reader mag/falsifier_counter.py:149,254, mirror tools/visor.py:49 |
| `memory/percolator/explore.jsonl` | 1660 | 1.70 | 2026-09-28 18:12:27 | T | +26 | 8 | mag/fuel_feed.py:43, mag/emergence.py:63,168 |
| `memory/facts/behavioral.jsonl` | 582 | 0.16 | 2026-09-28 18:12:27 | T | +26 | 1 | writer mag/fact_bus.py:45 (FACT_DIR/<domain>.jsonl) |
| `state/fuel/full_scan_ledger.jsonl` | 19135 | 4.18 | 2026-09-28 09:39:32 | I | - | 1 | tools/full_scan.py:32 |
| `research/destructive_receipts.jsonl` | 9580 | 2.75 | 2026-09-28 18:25:28 | T | +93 | 1 | mag/destructive_receipt.py:42 (append-only) |
| `training/events.jsonl` | 574628 | 253.08 | 2026-09-28 18:27:40 | T | +5485 | 3 | root mirror; readers point at memory/training/events.jsonl (loops_registry.py:109, tools/drift_pairs_stamp.py:285) |
| `memory/training/events.jsonl` | 574625 | 253.08 | 2026-09-28 18:27:06 | I | - | 3 | mag/loops_registry.py:109, mag/release_registry.py:5, tools/drift_dashboard.py:60, tools/drift_pairs_stamp.py:285 |
| `memory/workflows/REGISTRY.jsonl` | 30 | 0.03 | 2026-09-27 02:46:25 | T | 0 | 1 | mag/improve.py:2578 (workflow gate checks) |
| `memory/ghost/noise/behavioral.jsonl` | 36156 | 2.77 | 2026-09-28 13:50:47 | I | - | 1 | writer mag/percolator.py:222 (noise <domain>.jsonl), scanner mag/shadow_graph.py:9 |
| `watch/flight_recorder.jsonl` | 1440 | 0.34 | 2026-09-16 19:57:34 | I | - | 1 | writer mag/flight_recorder.py:81, reader tools/cache_kpi.py:17 |
| `memory/runs/ghost/trail.jsonl` | 18618 | 385.93 | 2026-09-28 18:25:57 | I | - | 8 | writer mag/ghost.py:44 (TRAIL_PATH), reader mag/live_feed.py:9 |
| `state/decisions_done.jsonl` | 14 | 0.00 | 2026-09-06 19:08:29 | I | - | 0 | mag/decision_hook.py:25 |
| `watch/inbox/DATED_METERS.jsonl` | 12 | 0.01 | 2026-09-28 17:20:49 | T | +4 | 1 | tools/meter_patrol.py:64 (LEDGER_RELPATH) |
| `watch/overnight_queue.jsonl` | 63 | 0.01 | 2026-09-03 13:47:43 | I | - | 1 | named in mag/claim_repair.py:77 (work manifests) |

### A1 schemas (top key families per file, from json.loads of every row)

- `watch/inbox/index_events.jsonl`: class,file,nonce,op,purpose,seq,sha256,ts,writer x1945; class,file,op,purpose,seq,sha256,ts x1792; bytes,file,op,purpose,sha256,ts x999; +5 more families
- `watch/inbox/LINKS.jsonl`: canonical,canonical_sha256,duplicate_of,note,seq,title,ts... x309; detail,flag,id,kind,title,ts,writer x22; detail,flag,id,kind,sources,title,ts,writer x16; +5 more families
- `watch/INBOX_LINKS.jsonl`: channel,context,source,status,ts,url x101; channel,context,status,ts,url,verdictTs x88; channel,status,ts,url x32; +5 more families
- `memory/decisions_log.jsonl`: context,outcome,steer_input,timestamp x19987; context,decision,ts,type x2; context,decision,kind,precedent,ts x1; +4 more families
- `memory/biography/verkle_chain.jsonl`: amended,dominant_theme,dossier_commit,end_minute,filename... x7635; amended,dominant_theme,dossier_commit,end_minute,evidence... x617; amended,dominant_theme,dossier_commit,end_minute,filename... x4; +2 more families
- `memory/trajectory/steps.jsonl`: command,face,result,schema_version,session_id,step_hash,ts x19970; command,face,schema_version,session_id,step_hash,ts x21; command,face,schema_version,session_id,ts x1
- `memory/agent_state/chain.jsonl`: content_commit,filename,label,leaf_hash,n_versions,parent... x19853
- `state/shared_activity.jsonl`: actor,depth,detail,goal,id,schema,seat,status,task_id,ts x19980
- `logs/behavioral_events.jsonl`: detail,error,kind,model,phase,provider,session_id,tool,ts x19995; captured,goal,kind,lessons,outcome,session_id,source,tool,ts x3; kind,path,pattern,session_id,tool,ts x2
- `logs/kpi.jsonl`: complete_means,complete_pct,incomplete_ids,n_complete,n_i... x19988; complete_pct,incomplete_ids,n_complete,n_incomplete,n_lea... x12
- `logs/usage.jsonl`: action,detail,lane,meta,ok,ts x20000
- `logs/provider_usage.jsonl`: calls,completion_tokens,meta,model,ok,prompt_tokens,provi... x19477; cache_hit_tokens,cache_miss_tokens,calls,completion_token... x324; cache_miss_tokens,cache_read_tokens,calls,completion_toke... x173; +1 more families
- `logs/supervisor.jsonl`: error,event,ts x90749; event,name,pid,ts x17086; event,leaks,total,ts x3; +1 more families
- `logs/failure_kb.jsonl`: detail,error,kind,model,phase,provider,session_id,sig,too... x19996
- `memory/ingest/registry.jsonl`: file_sha256,filename,html_stub,id,ingested_at,kind,local_... x20000
- `watch/room.jsonl`: event,seat,session,text,tool,ts x7418; event,seat,text,thread,ts x3291; detail,kind,seat,ts,verb x2119; +5 more families
- `watch/grok_feed.jsonl`: cwd,hook_event,prompt_preview,session_id,tool_input_previ... x18026; cwd,hook_event,session_id x1307
- `watch/session_digest.jsonl`: preview,session_id,ts,type x16589
- `catalog/catalog.jsonl`: age_days,bytes,ext,id,mtime,path,title,zone x20000
- `catalog/tags.jsonl`: age_class,bytes,id,kind,owner,path,zone x20000
- `catalog/junctions.jsonl`: action,id,is_dir,kind,note,path,path_limit_law,reparse_da... x79
- `memory/runs/swarm_health/trail.jsonl`: action,agent,applied,kind,ts,why x84734; actions,kind,overall,ts x163
- `memory/runs/governor_autorun_trail.jsonl`: action,detail,plan_fp,queued_n,schema,steps,ts x19790; agent_state,handoff,improve,phase,skipped,steward,total_q... x93; fingerprint,phase,queued_n,todo_n,ts x59; +4 more families
- `memory/runs/orchestrator_trail.jsonl`: event,goal,tag,task_id,timestamp x9505; detail,event,exit_code,killed,task_id,timestamp x5614; event,pid,task_id,timeout_s,timestamp x5187; +5 more families
- `memory/bard/breadcrumbs.jsonl`: breadcrumb,event,ts x20000
- `dashboard/data/ESTATE_INDEX.jsonl`: depth,ext,mtime,mtime_epoch,path,proj,rel,size,temp x20000
- `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`: depth,ext,mtime,mtime_epoch,path,proj,rel,size,temp x20000
- `queue/lanes/research/trail.jsonl`: actor,artifacts,detail,event,ts x2200; actor,detail,event,ts x1
- `memory/percolator/explore.jsonl`: canonical,domain,signal,source,status,ts x1111; answer,answered_at,canonical,domain,lane,quality,quality_... x406; canonical,domain,merged_into,signal,source,status,ts x97; +5 more families
- `memory/facts/behavioral.jsonl`: fact,ts,what,when,where,who,why x582
- `state/fuel/full_scan_ledger.jsonl`: brief,lane,ok,path,ts x19123
- `research/destructive_receipts.jsonl`: action,actor,reason,sha256_before,target,ts x9580
- `training/events.jsonl`: action,event_id,exportable,input,join,outcome,pattern,pat... x19996; action,event_id,exportable,input,join,outcome,pattern,pat... x3; action,ok,pattern,schema,ts x1
- `memory/training/events.jsonl`: action,event_id,exportable,input,join,outcome,pattern,pat... x19996; action,event_id,exportable,input,join,outcome,pattern,pat... x3; action,ok,pattern,schema,ts x1
- `memory/workflows/REGISTRY.jsonl`: checks,digest,name,script,ts,verdict x30
- `memory/ghost/noise/behavioral.jsonl`: kind,sentence,ts x36137
- `watch/flight_recorder.jsonl`: cached_tok,credits_est,error_code,in_tok,lane,latency_ms,... x1440
- `memory/runs/ghost/trail.jsonl`: amd_window_guard,dry,guard_registry,loop_breaker,outcome,... x4850; amd_window_guard,dry,guard_registry,loop_breaker_error,ou... x4282; amd_window_guard,auto_deploy,dry,guard_registry,loop_brea... x2959; +5 more families
- `state/decisions_done.jsonl`: unparsed
- `watch/inbox/DATED_METERS.jsonl`: date,meter_class,note,organ,pointer_count,pointers,schema... x12
- `watch/overnight_queue.jsonl`: id,output,source,title x63

## 5. Growth verdicts (is it growing?)

Instruments: (a) tracked files, row delta vs HEAD `0d6ace6b06`; (b) untracked files, mtime age (no baseline
exists for an untracked file, so growth is inferred from recent appends only).

| verdict | count | rows |
|---|---:|---:|
| tracked, grew since HEAD | 44 | +289922 |
| tracked, stable (0 row delta) | 442 | (equal to HEAD) |
| tracked, shrank vs HEAD | 0 | - |
| untracked (mostly gitignored runtime logs + tapes), 2258 of them touched within 24h | 11368 | - |

### 5a. All 44 tracked ledgers that grew since HEAD

| file | +rows | mtime age (d) | last commit |
|---|---:|---:|---|
| `dashboard/data/ESTATE_INDEX.jsonl` | +129962 | 0.36 | 2026-09-27 |
| `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` | +129962 | 0.37 | 2026-09-27 |
| `catalog/catalog.jsonl` | +19818 | 0.62 | 2026-09-27 |
| `training/events.jsonl` | +5485 | 0.00 | 2026-09-27 |
| `memory/trajectory/steps.jsonl` | +3271 | 0.00 | 2026-09-27 |
| `watch/inbox/index_events.jsonl` | +672 | 0.00 | 2026-09-28 |
| `research/destructive_receipts.jsonl` | +93 | 0.00 | 2026-09-27 |
| `dashboard/static/trails/research.jsonl` | +75 | 0.00 | 2026-09-27 |
| `queue/lanes/research/trail.jsonl` | +75 | 0.00 | 2026-09-27 |
| `dashboard/static/trails/day_work.jsonl` | +57 | 0.00 | 2026-09-27 |
| `queue/lanes/day_work/trail.jsonl` | +57 | 0.00 | 2026-09-27 |
| `watch/inbox/STEALTH_MINED_FINDINGS.jsonl` | +57 | 0.00 | 2026-09-28 |
| `watch/inbox/phone_relay_log.jsonl` | +54 | 0.37 | 2026-09-27 |
| `memory/burns/LEDGER.jsonl` | +39 | 0.22 | 2026-09-27 |
| `dashboard/static/trails/builder.jsonl` | +38 | 0.00 | 2026-09-27 |
| `queue/lanes/builder/trail.jsonl` | +38 | 0.00 | 2026-09-27 |
| `catalog/junctions.jsonl` | +35 | 0.62 | 2026-09-27 |
| `memory/facts/behavioral.jsonl` | +26 | 0.01 | 2026-09-27 |
| `memory/percolator/explore.jsonl` | +26 | 0.01 | 2026-09-27 |
| `watch/inbox/mimo_watch.jsonl` | +19 | 0.06 | 2026-09-27 |
| `memory/frontier/allowance.jsonl` | +17 | 0.03 | 2026-09-27 |
| `training/cost_ledger.jsonl` | +11 | 0.00 | 2026-09-27 |
| `memory/game/maze.jsonl` | +8 | 0.01 | 2026-09-27 |
| `memory/learn/sizing.jsonl` | +4 | 0.01 | 2026-09-27 |
| `watch/inbox/DATED_METERS.jsonl` | +4 | 0.05 | 2026-09-27 |
| `dashboard/static/trails/bard_ledger.jsonl` | +1 | 0.00 | 2026-09-27 |
| `dashboard/static/trails/economist.jsonl` | +1 | 0.00 | 2026-09-27 |
| `dashboard/static/trails/elder.jsonl` | +1 | 0.00 | 2026-09-27 |
| `dashboard/static/trails/forge.jsonl` | +1 | 0.00 | 2026-09-27 |
| `dashboard/static/trails/harvest.jsonl` | +1 | 0.00 | 2026-09-27 |
| `dashboard/static/trails/prose.jsonl` | +1 | 0.00 | 2026-09-27 |
| `memory/game/FLOW_LEDGER.jsonl` | +1 | 0.30 | 2026-09-26 |
| `queue/lanes/bard_ledger/trail.jsonl` | +1 | 0.10 | 2026-09-27 |
| `queue/lanes/economist/trail.jsonl` | +1 | 0.69 | 2026-09-27 |
| `queue/lanes/elder/trail.jsonl` | +1 | 0.44 | 2026-09-27 |
| `queue/lanes/forge/trail.jsonl` | +1 | 0.44 | 2026-09-27 |
| `queue/lanes/harvest/trail.jsonl` | +1 | 0.66 | 2026-09-27 |
| `queue/lanes/prose/trail.jsonl` | +1 | 0.70 | 2026-09-27 |
| `training/loop_gaps.jsonl` | +1 | 0.42 | 2026-09-27 |
| `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` | +1 | 0.80 | 2026-09-27 |
| `watch/inbox/LINKS.jsonl` | +1 | 0.17 | 2026-09-28 |
| `watch/inbox/QCAPTION_VERIFY_BEAT.jsonl` | +1 | 0.46 | 2026-09-27 |
| `watch/inbox/SECRET_SCAN_BEAT.jsonl` | +1 | 0.47 | 2026-09-27 |
| `watch/inbox/mrpool_export/vision_nightly_receipts.jsonl` | +1 | 0.67 | 2026-09-27 |

### 5b. The 4 untracked-and-not-ignored ledgers

| file | rows | mtime |
|---|---:|---|
| `watch/inbox/PACK_OFFLOAD.jsonl` | 739 | 2026-09-28 18:26:34 |
| `watch/inbox/burn_reset_20260927/queue/RECIPROCITY_LEDGER.jsonl` | 11 | 2026-09-28 14:46:42 |
| `watch/inbox/burn_reset_20260927/flash50/work/r-or-cache_probe_results.jsonl` | 9 | 2026-09-28 08:58:32 |
| `memory/agent_corpus/ledgers/saelis.jsonl` | 2 | 2026-09-28 12:50:22 |

### 5c. Busiest still-appending untracked ledgers (untracked, mtime <= 24h, rows >= 1000)

| file | rows | mtime |
|---|---:|---|
| `memory/ingest/registry.jsonl` | 2524920 | 2026-09-28 18:22:06 |
| `memory/training/events.jsonl` | 574625 | 2026-09-28 18:27:06 |
| `memory/runs/governor_autorun_trail.jsonl` | 236068 | 2026-09-28 18:24:26 |
| `logs/behavioral_events.jsonl` | 215577 | 2026-09-28 18:21:52 |
| `memory/decisions_log.jsonl` | 213260 | 2026-09-28 18:23:42 |
| `logs/usage.jsonl` | 163107 | 2026-09-28 18:12:19 |
| `logs/failure_kb.jsonl` | 112203 | 2026-09-28 18:22:37 |
| `logs/supervisor.jsonl` | 107905 | 2026-09-28 18:21:51 |
| `state/shared_activity.jsonl` | 107586 | 2026-09-28 18:27:06 |
| `memory/bard/breadcrumbs.jsonl` | 102245 | 2026-09-28 18:13:44 |
| `memory/runs/swarm_health/trail.jsonl` | 84907 | 2026-09-28 18:25:31 |
| `logs/kpi.jsonl` | 81937 | 2026-09-28 18:21:59 |
| `logs/provider_usage.jsonl` | 76574 | 2026-09-28 18:12:19 |
| `memory/runs/sentinel_trail.jsonl` | 40774 | 2026-09-28 18:14:53 |
| `memory/ghost/noise/behavioral.jsonl` | 36156 | 2026-09-28 13:50:47 |
| `memory/runs/orchestrator_trail.jsonl` | 31887 | 2026-09-28 17:50:54 |
| `memory/agent_state/chain.jsonl` | 19855 | 2026-09-28 18:23:58 |
| `watch/grok_feed.jsonl` | 19333 | 2026-09-28 17:32:35 |
| `state/fuel/full_scan_ledger.jsonl` | 19135 | 2026-09-28 09:39:32 |
| `memory/runs/ghost/trail.jsonl` | 18618 | 2026-09-28 18:25:57 |
| `watch/session_digest.jsonl` | 16589 | 2026-09-28 08:02:38 |
| `watch/room.jsonl` | 13866 | 2026-09-28 18:23:01 |
| `memory/biography/verkle_chain.jsonl` | 8259 | 2026-09-28 18:23:32 |
| `memory/biography_backup/biography_backup_20260928/verkle_chain.jsonl` | 8228 | 2026-09-28 13:25:09 |
| `logs/router.jsonl` | 8019 | 2026-09-28 14:12:34 |

## 6. Bulk trees (every file accounted in section 1, detailed per file in _f26_raw.json)

| tree | files | rows | MB | what it is |
|---|---:|---:|---:|---|
| `corpus/oral_history/` | 3709 | 463864 | 1093.0 | seat-pool session tapes (codex rollout-*.jsonl, grok events.jsonl) harvested from external seats; indexed by mag/librarian_catalog.py:40, not read by runtime code |
| `agents/` | 2137 | 6896 | 2.1 | pytest tmp_path leftovers (agents/pytest-tmp-*), incl deliberately-corrupt fixture ledgers (test_cli_corrupt_ledger_fails_0, test_malformed_lines_are_skipp0) |
| `memory/mail/` | 4612 | 48202 | 8.3 | pigeonhole task mailboxes memory/mail/<task_id>/ (mag/pigeonhole.py:8, mag/agent_cli.py _mail) |
| `memory/runs/` | 383 | 1463257 | 356.2 | run-scoped trails, vectors, receipts (gitignored via memory/runs/**, .gitignore:92) |
| `memory/seals/` | 96 | 165370 | 113.3 | dated seal snapshots (frozen copies incl verkle_chain.jsonl) |
| `memory/ghost/` | 14 | 309784 | 26.4 | per-domain noise/percolator files (mag/percolator.py:222, mag/ghost.py:781) |
| `memory/training/` | 11 | 5511 | 3.5 | training events stream read by drift tooling (tools/drift_pairs_stamp.py:285) |
| `memory/biography_backup` | 12 | 99897 | 70.2 | dated verkle_chain.jsonl backups (incl the two flag_ dirs from 2026-09-26) |

Note: the 6 A1 ledgers that live under these trees (memory/ghost/noise/behavioral.jsonl, memory/runs/ghost/trail.jsonl, memory/runs/governor_autorun_trail.jsonl, memory/runs/orchestrator_trail.jsonl, ...) are counted once, in section 4, and
excluded here, so sections 4 + 6 + 7 partition the full set exactly.

## 7. A2: every remaining non-bulk file (839), rows desc

| file | rows | MB | mtime | git | delta |
|---|---:|---:|---|---|---:|
| `dashboard/data/ractor_board.jsonl` | 2959486 | 713.25 | 2026-09-03 22:30:27 | t | 0 |
| `memory/vault/astra_v2_companions/failure-ledger-frozen-prefix.jsonl` | 74852 | 27.93 | 2026-09-11 11:16:01 | t | 0 |
| `dashboard-deploy/static/ractor_board.full-40k-20260903.jsonl` | 40183 | 9.82 | 2026-09-24 06:41:15 | t | 0 |
| `dashboard/static/ractor_board.full-40k-20260903.jsonl` | 40183 | 9.82 | 2026-09-03 06:07:07 | i | - |
| `memory/biography/chain_index_completion.jsonl` | 13678 | 4.59 | 2026-09-05 21:52:46 | i | - |
| `corpus/library/openai-cookbook/examples/data/example_requests_to_parallel_process.jsonl` | 10000 | 0.55 | 2026-09-04 12:03:05 | i | - |
| `memory/thinking/app_reasoning.jsonl` | 9305 | 22.19 | 2026-09-04 23:38:00 | t | 0 |
| `memory/corpus/watch_mining/watch_inventory.jsonl` | 8354 | 1.44 | 2026-09-18 01:17:19 | t | 0 |
| `logs/router.jsonl` | 8019 | 4.32 | 2026-09-28 14:12:34 | i | - |
| `watch/inbox/ractor_panel_20260926/revise_verkle99_checks/_sandbox/compaction_archive/20260927T045746Z/verkle_chain.jsonl` | 7849 | 5.50 | 2026-09-27 00:56:21 | t | 0 |
| `watch/inbox/ractor_panel_20260926/cands/_sim/compaction_archive/20260927T022738Z/verkle_chain.jsonl` | 7829 | 5.48 | 2026-09-26 22:25:22 | t | 0 |
| `watch/inbox/ractor_panel_20260926/revise_verkle99_checks/_sandbox/verkle_chain.jsonl` | 7387 | 5.16 | 2026-09-27 00:57:47 | t | 0 |
| `watch/inbox/ractor_panel_20260926/cands/_sim/verkle_chain.jsonl` | 7366 | 5.14 | 2026-09-26 22:27:39 | t | 0 |
| `watch/inbox/mrpool_export/cache_index.jsonl` | 7031 | 1.05 | 2026-09-18 10:54:44 | t | 0 |
| `logs/mag.jsonl` | 6917 | 8.40 | 2026-09-28 14:12:34 | i | - |
| `watch/inbox/qdrop_export/qdrops.jsonl` | 6242 | 3.60 | 2026-09-18 12:31:02 | t | 0 |
| `memory/mycelium/nodes.jsonl` | 5455 | 8.07 | 2026-09-27 22:17:39 | t | 0 |
| `corpus/library/openai-cookbook/examples/data/scifact_corpus.jsonl` | 5183 | 8.31 | 2026-09-04 12:22:12 | i | - |
| `watch/inbox/qdrop_export/media_register_qagg.jsonl` | 5011 | 1.01 | 2026-09-26 17:21:06 | t | 0 |
| `watch/inbox/qdrop_export/qnum_dropno_map.jsonl` | 4966 | 0.69 | 2026-09-26 16:22:06 | t | 0 |
| `memory/biography/repair_backups/verkle_20260831T0212Z/verkle_chain.jsonl` | 4914 | 3.41 | 2026-08-30 16:48:09 | i | - |
| `watch/inbox/mrpool_export/media_register.jsonl` | 4783 | 1.66 | 2026-09-26 17:07:13 | t | 0 |
| `state/fuel/record_briefs.jsonl` | 4275 | 1.41 | 2026-09-28 09:40:00 | i | - |
| `state/kvos_blocks.jsonl` | 3991 | 0.75 | 2026-09-10 08:23:36 | i | - |
| `memory/improve/skill_ledger.jsonl` | 3955 | 1.62 | 2026-09-28 18:20:32 | i | - |
| `memory/biography/registry.jsonl` | 3918 | 6.01 | 2026-09-28 18:22:11 | i | - |
| `corpus/library/kev/evals/v3/decision-v3/train.jsonl` | 3896 | 5.46 | 2026-09-21 16:00:34 | i | - |
| `watch/inbox/mrpool_export/ledger.jsonl` | 3663 | 2.01 | 2026-09-18 10:42:34 | t | 0 |
| `watch/inbox/mrpool_export/ledger_full.jsonl` | 3663 | 5.78 | 2026-09-18 10:54:08 | t | 0 |
| `corpus/library/kev/evals/decision-v2/train.jsonl` | 3432 | 4.80 | 2026-09-21 16:00:33 | i | - |
| `watch/inbox/burn_wave_20260926/B2_178_events.jsonl` | 3258 | 0.92 | 2026-09-26 16:02:04 | t | 0 |
| `watch/inbox/CAPTION_LEDGER_20260926.jsonl` | 2726 | 1.55 | 2026-09-26 16:01:48 | t | 0 |
| `logs/tesuji_shells.jsonl` | 2389 | 1.22 | 2026-09-28 18:23:42 | i | - |
| `training/cost_ledger.jsonl` | 2314 | 1.77 | 2026-09-28 18:25:39 | t | +11 |
| `logs/queue_events.jsonl` | 2287 | 0.56 | 2026-09-28 13:47:41 | i | - |
| `corpus/library/kev/evals/night2/all.jsonl` | 2225 | 2.60 | 2026-09-21 16:00:34 | i | - |
| `dashboard/static/trails/research.jsonl` | 2201 | 0.75 | 2026-09-28 18:23:02 | t | +75 |
| `memory/swarm_surface/sent.jsonl` | 2191 | 0.34 | 2026-09-27 02:24:05 | t | 0 |
| `corpus/telegram/MrPool_Q.jsonl` | 2008 | 3.23 | 2026-09-05 22:45:06 | t | 0 |
| `watch/inbox/mrpool_export/vision_triage.jsonl` | 2003 | 0.78 | 2026-09-19 11:05:32 | t | 0 |
| `state/fuel/lane_health.jsonl` | 1975 | 0.24 | 2026-09-28 09:31:02 | i | - |
| `watch/inbox/mrpool_export/stego_scan_full.jsonl` | 1911 | 0.20 | 2026-09-18 20:24:52 | t | 0 |
| `watch/inbox/qdrop_export/media_register.jsonl` | 1892 | 0.48 | 2026-09-26 16:40:54 | t | 0 |
| `dashboard-deploy/static/trails/research.jsonl` | 1782 | 0.60 | 2026-09-24 06:41:14 | t | 0 |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/evaluation_set/flask_evaluation.jsonl` | 1740 | 2.30 | 2026-08-05 19:04:46 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/input_data/flask_evaluation_raw.jsonl` | 1700 | 2.07 | 2026-08-05 19:04:46 | i | - |
| `dashboard/static/trails/day_work.jsonl` | 1620 | 0.34 | 2026-09-28 18:23:04 | t | +57 |
| `queue/lanes/day_work/trail.jsonl` | 1620 | 0.35 | 2026-09-28 18:23:04 | t | +57 |
| `corpus/library/kev/evals/night2/dates_unknowable.jsonl` | 1425 | 1.79 | 2026-09-21 16:00:34 | i | - |
| `watch/inbox/burn_wave_20260926/B2_178_out_corpus_class.jsonl` | 1394 | 0.20 | 2026-09-26 16:02:04 | t | 0 |
| `memory/castle_foundation/growth.jsonl` | 1351 | 0.10 | 2026-09-06 23:05:48 | t | 0 |
| `corpus/library/kev/evals/public-pool-v6/development.jsonl` | 1328 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/public-pool-v6/test.jsonl` | 1328 | 1.77 | 2026-09-21 16:00:34 | i | - |
| `dashboard-deploy/static/trails/day_work.jsonl` | 1306 | 0.28 | 2026-09-24 06:41:14 | t | 0 |
| `corpus/library/kev/evals/v9/transfer-v9/development.jsonl` | 1264 | 1.42 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v9/transfer-v9/test.jsonl` | 1264 | 1.43 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/round3/transfer-r3/test.jsonl` | 1260 | 1.38 | 2026-09-21 16:00:34 | i | - |
| `watch/inbox/burn_wave_20260926/B2_178_out_caption_enrich.jsonl` | 1234 | 0.20 | 2026-09-26 16:02:04 | t | 0 |
| `corpus/library/kev/evals/round3/decision-r3/development.jsonl` | 1204 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v3/decision-v3/development.jsonl` | 1204 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v4/decision-v4/development.jsonl` | 1204 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v5/decision-v5/development.jsonl` | 1204 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v6/decision-v6/development.jsonl` | 1204 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v7/decision-v7/development.jsonl` | 1204 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v8/decision-v8/development.jsonl` | 1204 | 1.76 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/decision-v1/train.jsonl` | 1200 | 2.47 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/decision-v2/development.jsonl` | 1176 | 1.70 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/decision-v2/test.jsonl` | 1176 | 1.71 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/v3/decision-v3/test.jsonl` | 1176 | 1.71 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v4/decision-v4/test.jsonl` | 1176 | 1.71 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v5/decision-v5/test.jsonl` | 1176 | 1.71 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v6/decision-v6/test.jsonl` | 1176 | 1.71 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v7/decision-v7/test.jsonl` | 1176 | 1.71 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v8/decision-v8/test.jsonl` | 1176 | 1.71 | 2026-09-21 16:00:34 | i | - |
| `memory/corpus/zcode_history/agent_tasks.jsonl` | 1161 | 0.36 | 2026-09-18 00:18:10 | t | 0 |
| `training/refined_training_data.jsonl` | 1157 | 1.27 | 2026-08-10 00:04:01 | t | 0 |
| `training/vast_package/formatted_data.jsonl` | 1157 | 0.16 | 2026-08-10 00:45:18 | t | 0 |
| `corpus/library/kev/evals/v5/decision-v5/calibration.jsonl` | 1112 | 1.52 | 2026-09-21 16:00:34 | i | - |
| `dashboard/static/trails/builder.jsonl` | 1112 | 0.16 | 2026-09-28 18:23:02 | t | +38 |
| `queue/lanes/builder/trail.jsonl` | 1112 | 0.16 | 2026-09-28 18:23:01 | t | +38 |
| `corpus/library/kev/evals/external/ekzhang-mmlupro-v1/records.jsonl` | 1000 | 1.17 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/openai-cookbook/examples/partners/macro_evals_for_agentic_systems/data/trace_results.jsonl` | 1000 | 2.03 | 2026-09-04 12:28:16 | i | - |
| `mine/raw/agent_platform/Aider-AI/aider/aider/website/assets/sample-analytics.jsonl` | 1000 | 0.16 | 2026-08-05 20:28:08 | i | - |
| `corpus/library/openai-cookbook/examples/partners/macro_evals_for_agentic_systems/data/eval_labels.jsonl` | 992 | 2.69 | 2026-09-04 12:28:30 | i | - |
| `corpus/library/kev/evals/v8/decision-v8/calibration.jsonl` | 984 | 1.47 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/public-pool-v4/development.jsonl` | 980 | 1.47 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/public-pool-v4/test.jsonl` | 980 | 1.48 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/public-pool-v5/development.jsonl` | 980 | 1.47 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/public-pool-v5/test.jsonl` | 980 | 1.48 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/round3/decision-r3/calibration.jsonl` | 968 | 1.45 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v7/decision-v7/calibration.jsonl` | 968 | 1.45 | 2026-09-21 16:00:34 | i | - |
| `memory/law/enforcement_trail.jsonl` | 935 | 0.19 | 2026-09-25 05:23:09 | t | 0 |
| `corpus/library/kev/evals/v6/decision-v6/calibration.jsonl` | 908 | 1.16 | 2026-09-21 16:00:34 | i | - |
| `dashboard-deploy/static/trails/builder.jsonl` | 902 | 0.13 | 2026-09-24 06:41:14 | t | 0 |
| `corpus/library/kev/evals/night2/dates.jsonl` | 900 | 1.11 | 2026-09-21 16:00:34 | i | - |
| `logs/memory_events.jsonl` | 801 | 0.32 | 2026-09-28 18:07:03 | i | - |
| `corpus/library/kev/evals/night2/assertion.jsonl` | 800 | 0.81 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/transfer-v1/development.jsonl` | 784 | 0.79 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/transfer-v1/test.jsonl` | 784 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/public-pool-v6/calibration.jsonl` | 780 | 0.99 | 2026-09-21 16:00:34 | i | - |
| `watch/inbox/lens_20260927/did_census.jsonl` | 778 | 0.19 | 2026-09-27 09:42:26 | t | 0 |
| `corpus/library/kev/evals/round3/transfer-r3/development.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v3/transfer-v3/development.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v3/transfer-v3/test.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v4/transfer-v4/development.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v4/transfer-v4/test.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v5/transfer-v5/development.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v5/transfer-v5/test.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v6/transfer-v6/development.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v6/transfer-v6/test.jsonl` | 764 | 0.80 | 2026-09-21 16:00:34 | i | - |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/research.jsonl` | 757 | 0.23 | 2026-09-12 17:38:27 | t | 0 |
| `memory/mycelium/edges.jsonl` | 744 | 0.29 | 2026-09-26 21:15:13 | t | 0 |
| `watch/inbox/PACK_OFFLOAD.jsonl` | 739 | 0.16 | 2026-09-28 18:26:34 | U | - |
| `corpus/library/kev/evals/v4/decision-v4/calibration.jsonl` | 728 | 1.01 | 2026-09-21 16:00:34 | i | - |
| `memory/burns/LEDGER.jsonl` | 693 | 0.56 | 2026-09-28 13:15:27 | t | +39 |
| `corpus/library/kev/evals/transfer-v2/development.jsonl` | 668 | 0.63 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/transfer-v2/test.jsonl` | 668 | 0.63 | 2026-09-21 16:00:34 | i | - |
| `memory/compiler_lang/rib_os_readings.jsonl` | 667 | 0.19 | 2026-09-06 23:05:44 | t | 0 |
| `memory/percolator/explore_blade_drain.jsonl` | 651 | 0.82 | 2026-08-28 07:45:49 | t | 0 |
| `watch/inbox/endpoint_news/endpoint_news.jsonl` | 641 | 0.13 | 2026-09-28 09:02:42 | t | 0 |
| `_archaeology_out/mag-disk-20260905/handoff/OX_NOVELTY_INDEX.jsonl` | 602 | 0.42 | 2026-09-05 18:03:16 | i | - |
| `handoff/OX_NOVELTY_INDEX.jsonl` | 602 | 0.42 | 2026-09-28 17:32:45 | t | 0 |
| `corpus/library/kev/evals/public-pool-v4/calibration.jsonl` | 600 | 0.85 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/public-pool-v5/calibration.jsonl` | 600 | 0.86 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/decision-v1/development.jsonl` | 588 | 1.01 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/decision-v1/test.jsonl` | 588 | 1.02 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/round3/transfer-r3/calibration.jsonl` | 580 | 0.65 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/diagnostics/binding-v1.jsonl` | 560 | 0.69 | 2026-09-21 16:00:33 | i | - |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/day_work.jsonl` | 560 | 0.12 | 2026-09-12 17:38:28 | t | 0 |
| `memory/facts/ox_artifact.jsonl` | 540 | 0.31 | 2026-08-24 14:00:32 | t | 0 |
| `corpus/library/kev/evals/v3/decision-v3/calibration.jsonl` | 528 | 0.74 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/night2/unknowable.jsonl` | 525 | 0.68 | 2026-09-21 16:00:34 | i | - |
| `watch/inbox/glm_burn/raw_v2.jsonl` | 507 | 0.05 | 2026-09-19 17:48:22 | t | 0 |
| `watch/inbox/ractor_panel_20260926/revise_verkle99_checks/_sandbox/fake_root/memory/biography/verkle_chain.jsonl` | 500 | 0.68 | 2026-09-27 00:57:56 | t | 0 |
| `memory/frontier/allowance.jsonl` | 473 | 0.15 | 2026-09-28 17:38:19 | t | +17 |
| `corpus/canon/x_canon_2025_pass6.jsonl` | 462 | 0.18 | 2026-09-05 23:02:55 | t | 0 |
| `corpus/library/kev/evals/decision-v2/calibration.jsonl` | 448 | 0.62 | 2026-09-21 16:00:33 | i | - |
| `memory/facts/fuel_feed.jsonl` | 446 | 0.25 | 2026-09-26 15:55:57 | t | 0 |
| `state/fuel/box_burn_watch.jsonl` | 419 | 0.09 | 2026-09-26 06:59:20 | i | - |
| `state/vast/steering_results_8b_20260827.jsonl` | 412 | 0.12 | 2026-08-27 19:41:43 | i | - |
| `state/vast/steering_results_ds_wip.jsonl` | 412 | 0.12 | 2026-08-27 18:46:05 | i | - |
| `state/fuel/task_wall_ledger.jsonl` | 407 | 0.05 | 2026-09-27 20:04:34 | i | - |
| `state/fuel/lite_quota_log.jsonl` | 402 | 0.11 | 2026-09-28 09:31:02 | i | - |
| `memory/biography/knot_timeline.jsonl` | 400 | 0.22 | 2026-09-28 18:22:06 | i | - |
| `state/vast/steering_results.jsonl` | 400 | 0.14 | 2026-08-27 19:51:41 | i | - |
| `state/vast/steering_results_dschat_20260827.jsonl` | 400 | 0.14 | 2026-08-27 19:52:11 | i | - |
| `watch/inbox/mrpool_export/audio_probe.jsonl` | 390 | 0.04 | 2026-09-18 16:27:28 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/builder.jsonl` | 388 | 0.06 | 2026-09-12 17:38:27 | t | 0 |
| `memory/biography/pointer_chain.jsonl` | 383 | 0.07 | 2026-09-28 18:23:04 | i | - |
| `logs/claims.jsonl` | 346 | 0.12 | 2026-09-05 23:05:14 | i | - |
| `watch/inbox/mrpool_export/transcriptions.jsonl` | 340 | 0.91 | 2026-09-18 18:03:25 | t | 0 |
| `watch/TESUJI_MAP.jsonl` | 336 | 0.21 | 2026-09-13 11:33:46 | i | - |
| `corpus/canon/receipts_dec2025_mar2026.jsonl` | 324 | 0.16 | 2026-09-05 15:47:30 | t | 0 |
| `logs/boot_coordination.jsonl` | 323 | 0.06 | 2026-09-25 23:47:46 | i | - |
| `training/loop_gaps.jsonl` | 323 | 0.11 | 2026-09-28 08:17:27 | t | +1 |
| `corpus/canon/x_canon_2025_pass3.jsonl` | 314 | 0.12 | 2026-09-05 15:30:20 | t | 0 |
| `watch/inbox/mrpool_export/media_recovered_register_20260926.jsonl` | 314 | 0.24 | 2026-09-26 13:43:27 | t | 0 |
| `corpus/library/openai-cookbook/examples/data/scifact_claims.jsonl` | 300 | 0.07 | 2026-09-04 12:22:06 | i | - |
| `memory/biography/index.jsonl` | 300 | 0.17 | 2026-09-28 18:22:11 | i | - |
| `state/arxiv/2026-09-09/digest.jsonl` | 300 | 0.50 | 2026-09-09 02:30:44 | i | - |
| `state/arxiv/2026-09-16/digest.jsonl` | 300 | 0.50 | 2026-09-16 02:30:16 | i | - |
| `state/arxiv/2026-09-22/digest.jsonl` | 300 | 0.51 | 2026-09-22 02:30:27 | i | - |
| `logs/freelane_burn_20260926.jsonl` | 299 | 0.90 | 2026-09-26 21:03:32 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_insults.jsonl` | 299 | 0.03 | 2026-08-05 20:28:21 | i | - |
| `state/arxiv/2026-09-25/digest.jsonl` | 295 | 0.49 | 2026-09-25 02:30:48 | i | - |
| `corpus/canon/x_canon_2026_fx/gap_months.jsonl` | 293 | 0.12 | 2026-09-20 06:36:26 | t | 0 |
| `state/arxiv/2026-09-17/digest.jsonl` | 293 | 0.49 | 2026-09-17 02:30:53 | i | - |
| `state/arxiv/2026-09-24/digest.jsonl` | 293 | 0.48 | 2026-09-24 02:30:27 | i | - |
| `watch/inbox/burn_wave_20260926/B2_68_ledger_before.jsonl` | 292 | 0.04 | 2026-09-26 09:48:28 | t | 0 |
| `corpus/library/kev/evals/external/scienthoon-v1/development.jsonl` | 291 | 0.36 | 2026-09-21 16:00:33 | i | - |
| `watch/inbox/burn_wave_20260926/B2_220_ledger_before.jsonl` | 291 | 0.04 | 2026-09-26 10:05:07 | t | 0 |
| `state/arxiv/2026-09-11/digest.jsonl` | 290 | 0.49 | 2026-09-11 02:30:26 | i | - |
| `state/arxiv/2026-09-07/digest.jsonl` | 289 | 0.49 | 2026-09-07 02:30:52 | i | - |
| `watch/inbox/burn_wave_20260926/B2_219_ledger_before.jsonl` | 289 | 0.04 | 2026-09-26 10:11:09 | t | 0 |
| `state/arxiv/2026-09-10/digest.jsonl` | 288 | 0.49 | 2026-09-10 02:30:57 | i | - |
| `state/arxiv/2026-09-18/digest.jsonl` | 282 | 0.48 | 2026-09-18 02:30:09 | i | - |
| `state/arxiv/2026-09-28/digest.jsonl` | 278 | 0.46 | 2026-09-28 02:30:27 | i | - |
| `watch/inbox/bearableguy_export/comments.jsonl` | 275 | 0.12 | 2026-09-18 12:51:48 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_243_ledger_before.jsonl` | 274 | 0.03 | 2026-09-26 10:31:11 | t | 0 |
| `memory/pile/training_rows.jsonl` | 272 | 0.10 | 2026-09-28 17:32:45 | i | - |
| `watch/inbox/burn_wave_20260926/B2_257_ledger_before.jsonl` | 267 | 0.03 | 2026-09-26 11:28:08 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_312_out_now.jsonl` | 267 | 0.03 | 2026-09-26 17:07:59 | t | 0 |
| `watch/inbox/qdrop_export/q_caption_ledger.jsonl` | 267 | 0.03 | 2026-09-26 11:32:28 | t | 0 |
| `state/arxiv/2026-09-23/digest.jsonl` | 266 | 0.45 | 2026-09-23 08:13:10 | i | - |
| `watch/inbox/burn_wave_20260926/B2_258_ledger_before.jsonl` | 266 | 0.03 | 2026-09-26 11:15:47 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_312_out_new.jsonl` | 266 | 0.03 | 2026-09-26 17:08:00 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_242_ledger_before.jsonl` | 263 | 0.03 | 2026-09-26 10:38:56 | t | 0 |
| `corpus/library/kev/evals/external/semif-v1/development.jsonl` | 252 | 0.26 | 2026-09-21 16:00:34 | i | - |
| `logs/hermes_dual_20260926/output.jsonl` | 242 | 0.37 | 2026-09-26 20:59:40 | i | - |
| `watch/inbox/bearableguy_export/vision_census.jsonl` | 242 | 0.07 | 2026-09-18 23:37:02 | t | 0 |
| `training/vast_package/train_data.jsonl` | 211 | 0.08 | 2026-08-09 20:07:04 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_178_out_links_titles.jsonl` | 210 | 0.03 | 2026-09-26 15:15:13 | t | 0 |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_investment.jsonl` | 207 | 0.03 | 2026-08-05 20:28:21 | i | - |
| `state/operator_mode.jsonl` | 205 | 0.08 | 2026-09-28 18:23:15 | i | - |
| `watch/wargames_v0/match_003/moves.jsonl` | 205 | 0.01 | 2026-09-01 09:07:26 | t | 0 |
| `corpus/library/openai-cookbook/examples/data/dbpedia_samples.jsonl` | 200 | 0.06 | 2026-09-04 12:02:56 | i | - |
| `memory/improve/candidates.jsonl` | 200 | 0.12 | 2026-09-28 18:23:04 | i | - |
| `state/arxiv/2026-09-21/digest.jsonl` | 200 | 0.35 | 2026-09-21 02:30:32 | i | - |
| `watch/inbox/qdrop_export/q_vision_triage_rows.jsonl` | 200 | 0.13 | 2026-09-19 12:58:49 | t | 0 |
| `logs/docker_ops.jsonl` | 193 | 0.03 | 2026-09-28 18:07:38 | i | - |
| `corpus/papers/librarian_backfill_20260927.jsonl` | 189 | 0.12 | 2026-09-26 23:18:07 | t | 0 |
| `watch/inbox/verb_trace.jsonl` | 187 | 0.05 | 2026-09-25 23:28:31 | t | 0 |
| `state/fuel/bakeoff_ledger.jsonl` | 186 | 0.04 | 2026-09-26 21:07:59 | i | - |
| `watch/inbox/union_fullsend_20260917/raw.jsonl` | 184 | 0.45 | 2026-09-26 07:37:50 | t | 0 |
| `memory/corpus/LINKS.jsonl` | 178 | 0.14 | 2026-09-27 07:40:50 | t | 0 |
| `memory/game/FLOW_LEDGER.jsonl` | 178 | 0.03 | 2026-09-28 11:16:46 | t | +1 |
| `state/fuel/gaming_corpus_briefs.jsonl` | 178 | 0.03 | 2026-09-24 01:43:34 | i | - |
| `memory/facts/general.jsonl` | 171 | 0.10 | 2026-08-26 03:17:04 | t | 0 |
| `memory/lattice/edges.jsonl` | 170 | 0.05 | 2026-08-07 15:08:32 | i | - |
| `logs/memory_interventions.jsonl` | 168 | 0.05 | 2026-09-25 20:55:50 | i | - |
| `state/arxiv/2026-09-06/digest.jsonl` | 167 | 0.28 | 2026-09-06 02:30:52 | i | - |
| `logs/steering_events.jsonl` | 166 | 0.03 | 2026-09-28 18:07:03 | i | - |
| `memory/percolator/explore_a4000_experiment.jsonl` | 165 | 0.21 | 2026-08-28 04:51:15 | t | 0 |
| `logs/failure_kb_alerts.jsonl` | 163 | 0.03 | 2026-09-28 11:10:58 | i | - |
| `memory/lattice/nodes.jsonl` | 161 | 0.07 | 2026-08-31 07:26:58 | i | - |
| `corpus/library/kev/evals/decision-v1/calibration.jsonl` | 160 | 0.32 | 2026-09-21 16:00:33 | i | - |
| `watch/recovery/openclaw-patches-20260831-072651/memory/lattice/nodes.jsonl` | 160 | 0.07 | 2026-08-07 15:08:32 | t | 0 |
| `memory/pile/classified.jsonl` | 154 | 0.12 | 2026-09-28 15:01:38 | i | - |
| `training/lora/formatted_data.jsonl` | 149 | 0.05 | 2026-09-03 13:07:19 | t | 0 |
| `training/sovereign_training_data.jsonl` | 149 | 0.05 | 2026-09-03 13:07:19 | t | 0 |
| `mine/raw/steal_protocol/whiteducksoftware/flock/.beads/issues.jsonl` | 145 | 0.12 | 2026-08-05 19:04:36 | i | - |
| `memory/pile/state_summaries.jsonl` | 144 | 0.08 | 2026-09-28 15:01:38 | i | - |
| `watch/inbox/STEALTH_MINED_FINDINGS.jsonl` | 144 | 0.05 | 2026-09-28 18:27:32 | t | +57 |
| `watch/inbox/glm_burn/raw.jsonl` | 138 | 0.05 | 2026-09-19 06:39:32 | t | 0 |
| `watch/inbox/phone_relay_log.jsonl` | 138 | 0.03 | 2026-09-28 09:31:29 | t | +54 |
| `watch/GROUNDING_WAVE.jsonl` | 137 | 0.14 | 2026-09-27 14:39:49 | i | - |
| `memory/game/maze.jsonl` | 135 | 0.03 | 2026-09-28 18:07:18 | t | +8 |
| `state/library/catalog.jsonl` | 135 | 0.04 | 2026-09-28 09:15:15 | i | - |
| `memory/cost/vast_charges.jsonl` | 134 | 0.13 | 2026-08-30 20:55:22 | t | 0 |
| `corpus/library/kev/runs/leaderboard.jsonl` | 132 | 0.17 | 2026-09-21 16:00:34 | i | - |
| `watch/inbox/union_fullsend_20260917/queue.jsonl` | 131 | 0.08 | 2026-09-18 07:07:18 | t | 0 |
| `corpus/canon/x_canon_enumeration_index.jsonl` | 130 | 0.05 | 2026-09-05 15:13:04 | t | 0 |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/research.jsonl` | 129 | 0.04 | 2026-09-05 18:03:09 | i | - |
| `state/fuel/lite_pacing.jsonl` | 129 | 0.02 | 2026-09-26 07:35:55 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/cookbook/litellm_proxy_server/batch_api/bedrock/bedrock_batch_completions.jsonl` | 128 | 0.04 | 2026-08-05 20:28:18 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/batches_tests/bedrock_batch_completions.jsonl` | 128 | 0.04 | 2026-08-05 20:28:21 | i | - |
| `state/vast/market_watch.jsonl` | 124 | 0.03 | 2026-08-28 21:53:30 | i | - |
| `memory/self_advance/reflections.jsonl` | 121 | 0.06 | 2026-08-15 10:31:46 | t | 0 |
| `watch/ARCHIVIST_RECEIPTS.jsonl` | 121 | 0.18 | 2026-09-01 18:14:23 | i | - |
| `watch/inbox/BCHAIN2_DISSECTOR_20260907.jsonl` | 120 | 0.06 | 2026-09-07 15:25:17 | t | 0 |
| `memory/seed_chain/seeds.jsonl` | 119 | 0.04 | 2026-08-15 10:31:46 | t | 0 |
| `corpus/canon/_retired/x_canon_nachoquixotic_v1.jsonl` | 117 | 0.04 | 2026-09-05 14:29:49 | t | 0 |
| `watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl` | 114 | 0.13 | 2026-09-26 09:53:18 | t | 0 |
| `memory/biography/diary_nodes/auto/index.jsonl` | 113 | 0.04 | 2026-09-28 14:03:17 | i | - |
| `watch/x_intercept_log.jsonl` | 110 | 0.01 | 2026-09-06 21:13:06 | i | - |
| `memory/burns/SPOT_PATROL.jsonl` | 108 | 0.02 | 2026-09-27 18:02:29 | t | 0 |
| `watch/inbox/mrpool_export/called_shot_ledger_captions.jsonl` | 107 | 0.04 | 2026-09-18 19:38:39 | t | 0 |
| `memory/working/voice_handoffs/index.jsonl` | 105 | 0.02 | 2026-09-26 15:55:06 | i | - |
| `watch/inbox/qdrop_export/deep_read_chunks.jsonl` | 105 | 0.01 | 2026-09-19 06:40:29 | t | 0 |
| `corpus/library/openai-cookbook/examples/data/drone_training.jsonl` | 103 | 0.39 | 2026-09-04 12:02:57 | i | - |
| `state/vast/spend_ledger.jsonl` | 103 | 0.03 | 2026-08-28 13:41:17 | i | - |
| `watch/riddler_common.jsonl` | 102 | 0.08 | 2026-09-01 00:00:20 | i | - |
| `state/arxiv/2026-09-05/digest.jsonl` | 100 | 0.17 | 2026-09-04 23:06:39 | i | - |
| `watch/gauntlet_w4_rerun_receipts.jsonl` | 100 | 0.06 | 2026-09-25 21:03:37 | i | - |
| `watch/gauntlet_w4_rerun_receipts_PREFIXCALIBRATION_ABORT.jsonl` | 100 | 0.06 | 2026-09-25 20:58:07 | i | - |
| `watch/inbox/mrpool_export/stego_scan.jsonl` | 100 | 0.01 | 2026-09-18 16:06:28 | t | 0 |
| `watch/riddler/feed.jsonl` | 94 | 0.03 | 2026-09-08 07:30:13 | t | 0 |
| `memory/research_packs/bibverify/part3_mid.jsonl` | 93 | 0.04 | 2026-09-19 20:01:45 | i | - |
| `watch/inbox/bearableguy_export/submissions.jsonl` | 92 | 0.09 | 2026-09-18 12:49:20 | t | 0 |
| `logs/economy.jsonl` | 90 | 0.03 | 2026-08-07 13:42:27 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/evaluation_set/flask_hard_evaluation.jsonl` | 89 | 0.12 | 2026-08-05 19:04:46 | i | - |
| `watch/salon_receipts/quorum_20260907.jsonl` | 89 | 0.02 | 2026-09-07 03:30:16 | t | 0 |
| `memory/learn/sizing.jsonl` | 88 | 0.02 | 2026-09-28 18:18:29 | t | +4 |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/day_work.jsonl` | 84 | 0.02 | 2026-09-05 18:03:09 | i | - |
| `logs/boot.jsonl` | 82 | 0.02 | 2026-09-22 14:57:41 | i | - |
| `state/fuel/label_farm.jsonl` | 81 | 0.15 | 2026-09-28 09:26:17 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FastChat/fastchat/llm_judge/data/mt_bench/question.jsonl` | 80 | 0.05 | 2026-08-05 19:04:47 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FastChat/fastchat/llm_judge/data/vicuna_bench/question.jsonl` | 80 | 0.01 | 2026-08-05 19:04:47 | i | - |
| `watch/wargames_v0/match_002/moves.jsonl` | 76 | 0.00 | 2026-09-01 06:46:14 | t | 0 |
| `memory/research_packs/bibverify/part1_tiers.jsonl` | 75 | 0.03 | 2026-09-19 19:55:56 | i | - |
| `memory/thinking/glm-5.3-flash.jsonl` | 75 | 0.08 | 2026-09-16 10:39:21 | t | 0 |
| `watch/inbox/wave_20260916/r1_fanout_runs/raw.jsonl` | 73 | 0.21 | 2026-09-16 17:05:07 | t | 0 |
| `corpus/library/interference-search/results/llm/phase1_qwen3-1.7b.jsonl` | 72 | 1.13 | 2026-09-25 16:37:29 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/builder.jsonl` | 69 | 0.02 | 2026-09-05 18:03:09 | i | - |
| `watch/astra_hold0/I3_CHAIN_SLICE.jsonl` | 69 | 0.02 | 2026-09-15 20:08:46 | t | 0 |
| `state/mcp_pins.jsonl` | 68 | 0.02 | 2026-09-25 20:20:08 | i | - |
| `logs/compute_schedule.jsonl` | 67 | 0.06 | 2026-09-28 17:34:16 | i | - |
| `watch/GRAPH/graph_20260901.jsonl` | 64 | 0.01 | 2026-09-01 18:20:19 | t | 0 |
| `watch/inbox/bearableguy_export/media_register.jsonl` | 64 | 0.02 | 2026-09-18 12:50:33 | t | 0 |
| `corpus/library/kev/evals/v3/smoke-v3/development.jsonl` | 62 | 0.10 | 2026-09-21 16:00:34 | i | - |
| `memory/research_packs/bibverify/part5_end.jsonl` | 61 | 0.03 | 2026-09-19 19:53:26 | i | - |
| `watch/inbox/mimo_watch.jsonl` | 61 | 0.02 | 2026-09-28 16:58:19 | t | +19 |
| `watch/w1_gauntlet_ledger.jsonl` | 61 | 0.01 | 2026-09-01 15:03:45 | i | - |
| `watch/w1_gauntlet_v2_ledger.jsonl` | 61 | 0.01 | 2026-09-01 15:31:11 | i | - |
| `watch/gauntlet_w4_receipts.jsonl` | 60 | 0.02 | 2026-09-01 13:58:39 | i | - |
| `watch/openjev_ab/results/selftest/rows.jsonl` | 60 | 0.07 | 2026-09-25 20:58:03 | t | 0 |
| `_archaeology_out/mag-disk-20260905/memory/game/FLOW_LEDGER.jsonl` | 59 | 0.01 | 2026-09-05 18:03:10 | i | - |
| `state/fuel/stealth_ledger.jsonl` | 58 | 0.01 | 2026-09-28 09:50:15 | i | - |
| `watch/inbox/EVENTS.jsonl` | 58 | 0.04 | 2026-09-27 07:38:16 | t | 0 |
| `watch/inbox/wave_20260916/receipts/D23_SALON50_raw.jsonl` | 56 | 0.10 | 2026-09-16 14:30:39 | t | 0 |
| `_archaeology_out/mag-disk-20260905/memory/game/maze.jsonl` | 55 | 0.01 | 2026-09-05 18:03:10 | i | - |
| `memory/ledger/ghost_ledger.jsonl` | 54 | 0.03 | 2026-08-09 07:38:38 | i | - |
| `memory/feed/feed_snapshot.jsonl` | 52 | 0.01 | 2026-09-04 22:19:02 | t | 0 |
| `outputs/wandr_selfeval_cache/pages.jsonl` | 51 | 18.18 | 2026-09-25 20:59:26 | t | 0 |
| `watch/bay_share.jsonl` | 51 | 0.01 | 2026-09-03 15:08:38 | i | - |
| `watch/inbox/wave_20260916/rv2_explain_fleet/raw.jsonl` | 51 | 0.09 | 2026-09-16 21:12:39 | t | 0 |
| `memory/copilot/inbox.jsonl` | 50 | 0.06 | 2026-09-28 17:50:49 | i | - |
| `memory/corpus/mycology_canon/manifest.jsonl` | 50 | 0.01 | 2026-09-16 20:16:18 | t | 0 |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_claims_fraud_coaching.jsonl` | 50 | 0.01 | 2026-08-05 20:28:21 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_claims_phi_disclosure.jsonl` | 50 | 0.01 | 2026-08-05 20:28:21 | i | - |
| `queue/queue_index.jsonl` | 50 | 0.03 | 2026-09-27 07:41:33 | t | 0 |
| `watch/inbox/ADVERSARIAL_ARC_BATTERY_20260918.jsonl` | 50 | 0.03 | 2026-09-18 11:40:31 | t | 0 |
| `watch/inbox/GPS_BATTERY_20260918.jsonl` | 50 | 0.02 | 2026-09-18 20:08:35 | t | 0 |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_claims_medical_advice.jsonl` | 49 | 0.01 | 2026-08-05 20:28:21 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_claims_prior_auth_gaming.jsonl` | 49 | 0.01 | 2026-08-05 20:28:21 | i | - |
| `watch/LOST_JOURNEY_48_20260902.jsonl` | 48 | 0.01 | 2026-09-02 10:28:31 | i | - |
| `memory/arxiv_mine/ledger.jsonl` | 46 | 0.02 | 2026-08-15 10:32:02 | t | 0 |
| `watch/T1_FIRE_RAW_20260906.jsonl` | 46 | 0.10 | 2026-09-07 03:22:35 | i | - |
| `memory/portable_bags/bag-20260727T214646Z/memory/improve/candidates.jsonl` | 45 | 0.03 | 2026-07-27 17:46:29 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_claims_system_override.jsonl` | 45 | 0.01 | 2026-08-05 20:28:21 | i | - |
| `memory/capability_steal/expansions.jsonl` | 44 | 0.01 | 2026-08-15 10:33:45 | t | 0 |
| `state/fuel/stealth_driver.jsonl` | 44 | 0.05 | 2026-09-28 18:22:01 | i | - |
| `memory/ideas/nodes.jsonl` | 43 | 0.02 | 2026-08-31 00:32:05 | i | - |
| `state/fuel/gap_questions.jsonl` | 43 | 0.02 | 2026-09-27 20:02:53 | i | - |
| `training/arena_profiles.jsonl` | 41 | 0.01 | 2026-08-06 13:17:06 | t | 0 |
| `memory/working/voice_build_tasks.jsonl` | 40 | 0.05 | 2026-09-28 14:03:17 | i | - |
| `watch/inbox/mrpool_export/vision_waves/chunk_00.jsonl` | 40 | 0.04 | 2026-09-19 09:55:36 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_03.jsonl` | 40 | 0.02 | 2026-09-19 09:52:34 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_04.jsonl` | 40 | 0.02 | 2026-09-19 09:53:02 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_05.jsonl` | 40 | 0.02 | 2026-09-19 09:53:42 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_06.jsonl` | 40 | 0.02 | 2026-09-19 09:52:14 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_07.jsonl` | 40 | 0.02 | 2026-09-19 09:52:39 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_08.jsonl` | 40 | 0.02 | 2026-09-19 09:52:06 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_09.jsonl` | 40 | 0.02 | 2026-09-19 09:54:21 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_10.jsonl` | 40 | 0.02 | 2026-09-19 10:02:11 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_11.jsonl` | 40 | 0.01 | 2026-09-19 10:02:38 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_12.jsonl` | 40 | 0.02 | 2026-09-19 10:01:46 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_13.jsonl` | 40 | 0.02 | 2026-09-19 10:01:53 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_14.jsonl` | 40 | 0.02 | 2026-09-19 10:03:12 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_15.jsonl` | 40 | 0.02 | 2026-09-19 10:05:25 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_16.jsonl` | 40 | 0.02 | 2026-09-19 10:03:57 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_17.jsonl` | 40 | 0.02 | 2026-09-19 10:02:18 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_20.jsonl` | 40 | 0.02 | 2026-09-19 10:13:48 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_22.jsonl` | 40 | 0.02 | 2026-09-19 10:13:46 | t | 0 |
| `watch/wargames_v0/match_004/board2/moves.jsonl` | 40 | 0.00 | 2026-09-01 10:16:10 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_18.jsonl` | 39 | 0.02 | 2026-09-19 10:08:00 | t | 0 |
| `watch/wargames_v0/match_001/moves.jsonl` | 39 | 0.00 | 2026-09-01 03:37:11 | t | 0 |
| `dashboard/static/trails/economist.jsonl` | 38 | 0.01 | 2026-09-28 18:23:02 | t | +1 |
| `queue/lanes/economist/trail.jsonl` | 38 | 0.01 | 2026-09-28 02:01:00 | t | +1 |
| `watch/night_cache_receipts.jsonl` | 38 | 0.01 | 2026-09-01 02:46:54 | i | - |
| `memory/corpus/game_design_docs/manifest.jsonl` | 37 | 0.01 | 2026-09-16 20:19:21 | t | 0 |
| `dashboard/static/trails/bard_ledger.jsonl` | 36 | 0.01 | 2026-09-28 18:23:03 | t | +1 |
| `memory/corpus/zcode_history/sessions.jsonl` | 36 | 0.01 | 2026-09-18 00:18:10 | t | 0 |
| `queue/lanes/bard_ledger/trail.jsonl` | 36 | 0.01 | 2026-09-28 16:01:28 | t | +1 |
| `memory/corpus/training_pdfs/20260916/manifest.jsonl` | 35 | 0.02 | 2026-09-16 20:24:37 | t | 0 |
| `watch/inbox/wave_20260916/concert001/concert001_raw.jsonl` | 35 | 0.06 | 2026-09-16 16:23:23 | t | 0 |
| `dashboard-deploy/static/trails/economist.jsonl` | 34 | 0.01 | 2026-09-24 06:41:14 | t | 0 |
| `logs/lattice_loop.jsonl` | 34 | 0.01 | 2026-07-29 09:56:02 | i | - |
| `memory/ideas/edges.jsonl` | 34 | 0.01 | 2026-08-09 01:56:51 | i | - |
| `memory/portable_bags/lattice-vast-20260729T140048Z/logs/lattice_loop.jsonl` | 34 | 0.01 | 2026-07-29 09:56:02 | i | - |
| `watch/sea/mag_memory_index.jsonl` | 34 | 0.01 | 2026-09-01 17:25:44 | t | 0 |
| `watch/inbox/wave_20260916/receipts/U4_UNION_VERDICT_COLUMN_raw.jsonl` | 33 | 0.08 | 2026-09-16 16:17:17 | t | 0 |
| `corpus/library/kev/evals/v3/smoke-v3/calibration.jsonl` | 32 | 0.04 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v3/smoke-v3/train.jsonl` | 32 | 0.05 | 2026-09-21 16:00:34 | i | - |
| `memory/corpus/ai_canon/manifest.jsonl` | 32 | 0.01 | 2026-09-16 19:58:23 | t | 0 |
| `memory/corpus/zcode_history/correspondence_c424b80a.jsonl` | 32 | 0.01 | 2026-09-18 00:19:55 | t | 0 |
| `dashboard-deploy/static/trails/bard_ledger.jsonl` | 31 | 0.01 | 2026-09-24 06:41:14 | t | 0 |
| `dashboard/static/trails/elder.jsonl` | 31 | 0.00 | 2026-09-28 18:23:03 | t | +1 |
| `memory/proofs/anchored.jsonl` | 31 | 0.01 | 2026-09-26 05:03:57 | t | 0 |
| `queue/lanes/elder/trail.jsonl` | 31 | 0.00 | 2026-09-28 08:00:35 | t | +1 |
| `watch/wargames_v0/match_004/board1/moves.jsonl` | 31 | 0.00 | 2026-09-01 10:16:10 | t | 0 |
| `corpus/library/kev/evals/smoke-v1/development.jsonl` | 30 | 0.06 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/smoke-v1/test.jsonl` | 30 | 0.06 | 2026-09-21 16:00:34 | i | - |
| `memory/percolator/explore_deepseek_drain.jsonl` | 30 | 0.04 | 2026-08-27 22:20:28 | t | 0 |
| `memory/percolator/explore_handsbox_drain.jsonl` | 30 | 0.04 | 2026-08-27 22:20:39 | t | 0 |
| `mine/raw/steal_protocol/togethercomputer/moa/FastChat/fastchat/llm_judge/data/mt_bench/reference_answer/gpt-4.jsonl` | 30 | 0.05 | 2026-08-05 19:04:47 | i | - |
| `watch/inbox/gala_20260925/w1/lanes/b3_w1_t04_bank_PRE_FIX.jsonl` | 30 | 0.05 | 2026-09-25 23:20:18 | t | 0 |
| `watch/inbox/mrpool_export/ledger_delta_preview_20260926.jsonl` | 30 | 0.04 | 2026-09-26 15:22:24 | t | 0 |
| `watch/openclaw_traj.jsonl` | 30 | 0.01 | 2026-09-03 13:06:12 | i | - |
| `watch/openjev_ab/frozen30_20260925.jsonl` | 30 | 0.06 | 2026-09-25 20:40:31 | t | 0 |
| `watch/inbox/physical_computing/receipts/concert002_fiber25/raw.jsonl` | 29 | 0.06 | 2026-09-16 18:37:24 | t | 0 |
| `logs/groq_cache_bypass_20260926.jsonl` | 28 | 0.01 | 2026-09-26 17:24:05 | i | - |
| `state/fuel/stealth_fanout.jsonl` | 28 | 0.00 | 2026-09-28 12:40:33 | i | - |
| `watch/engine_b1_queue.jsonl` | 28 | 0.00 | 2026-09-03 05:24:13 | i | - |
| `canon/riddler_corpus/cooper_deep_read_chunks.jsonl` | 27 | 0.01 | 2026-09-19 06:40:29 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_178_out_links_dedupe.jsonl` | 27 | 0.00 | 2026-09-26 15:03:55 | t | 0 |
| `dashboard-deploy/static/trails/elder.jsonl` | 26 | 0.00 | 2026-09-24 06:41:14 | t | 0 |
| `dashboard/static/trails/forge.jsonl` | 26 | 0.00 | 2026-09-28 18:23:03 | t | +1 |
| `dashboard/static/trails/harvest.jsonl` | 26 | 0.00 | 2026-09-28 18:23:04 | t | +1 |
| `memory/burn/steer_log.jsonl` | 26 | 0.07 | 2026-09-11 06:44:16 | t | 0 |
| `memory/harvest_20260816.jsonl` | 26 | 0.00 | 2026-08-16 09:51:28 | t | 0 |
| `queue/lanes/forge/trail.jsonl` | 26 | 0.00 | 2026-09-28 08:00:35 | t | +1 |
| `queue/lanes/harvest/trail.jsonl` | 26 | 0.00 | 2026-09-28 02:30:28 | t | +1 |
| `memory/learn/catalog.jsonl` | 25 | 0.02 | 2026-08-09 18:26:07 | t | 0 |
| `memory/working/refine_chains/index.jsonl` | 25 | 0.01 | 2026-08-28 19:31:43 | i | - |
| `watch/sea/board_index.jsonl` | 25 | 0.01 | 2026-09-01 17:33:42 | t | 0 |
| `dashboard/static/trails/night.jsonl` | 24 | 0.00 | 2026-09-27 19:01:06 | t | 0 |
| `dashboard/static/trails/prose.jsonl` | 24 | 0.00 | 2026-09-28 18:23:03 | t | +1 |
| `memory/corpus/quantized_thought/instructions_frontier.jsonl` | 24 | 0.01 | 2026-09-28 12:19:05 | t | 0 |
| `memory/prospect/map.jsonl` | 24 | 0.01 | 2026-08-09 18:26:07 | t | 0 |
| `memory/research_packs/bibverify/part4_late.jsonl` | 24 | 0.02 | 2026-09-19 19:46:53 | i | - |
| `queue/lanes/night/trail.jsonl` | 24 | 0.00 | 2026-09-27 19:01:04 | t | 0 |
| `queue/lanes/prose/trail.jsonl` | 24 | 0.00 | 2026-09-28 01:36:28 | t | +1 |
| `watch/engine_e1_queue.jsonl` | 24 | 0.00 | 2026-09-02 19:46:24 | i | - |
| `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/src/mcp_agent/data/examples/mcp_agent_server/asyncio/logs/mcp-agent.jsonl` | 23 | 0.00 | 2026-08-05 20:34:01 | i | - |
| `dashboard-deploy/static/trails/harvest.jsonl` | 22 | 0.00 | 2026-09-24 06:41:14 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/economist.jsonl` | 22 | 0.01 | 2026-09-12 17:38:28 | t | 0 |
| `memory/corpus/mycology_canon/blocked.jsonl` | 22 | 0.01 | 2026-09-16 20:17:28 | t | 0 |
| `memory/research_packs/bibverify/part2_kv.jsonl` | 22 | 0.02 | 2026-09-19 19:46:34 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/vertex_ai.jsonl` | 22 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `corpus/library/openai-cookbook/examples/partners/agentic_governance_guide/eval_data/guardrail_test_data.jsonl` | 21 | 0.01 | 2026-09-04 12:25:54 | i | - |
| `dashboard-deploy/static/trails/forge.jsonl` | 21 | 0.00 | 2026-09-24 06:41:14 | t | 0 |
| `state/fuel/anchor_notes.jsonl` | 21 | 0.01 | 2026-09-27 20:02:47 | i | - |
| `state/vast/experiment_receipts.jsonl` | 21 | 0.00 | 2026-09-05 01:45:30 | i | - |
| `watch/DEALS_LEDGER.jsonl` | 21 | 0.01 | 2026-09-01 10:41:19 | i | - |
| `watch/KG_STORE/catalog.jsonl` | 21 | 0.01 | 2026-09-02 11:44:18 | t | 0 |
| `watch/inbox/PROBE20_steering_v1.jsonl` | 21 | 0.00 | 2026-09-26 06:07:44 | t | 0 |
| `watch/salon_responses/astra_smoke_12/raw.jsonl` | 21 | 0.03 | 2026-09-16 13:56:01 | t | 0 |
| `dashboard-deploy/static/trails/night.jsonl` | 20 | 0.00 | 2026-09-24 06:41:14 | t | 0 |
| `dashboard-deploy/static/trails/prose.jsonl` | 20 | 0.00 | 2026-09-24 06:41:14 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/bard_ledger.jsonl` | 20 | 0.01 | 2026-09-12 17:38:28 | t | 0 |
| `watch/anthropic_battery_ledger.jsonl` | 20 | 0.00 | 2026-09-01 16:29:58 | i | - |
| `watch/inbox/gala_20260925/w1/lanes/b3_w4_t16_battery_PRE_FIX.jsonl` | 20 | 0.04 | 2026-09-25 23:17:59 | t | 0 |
| `watch/inbox/wave_20260916/sp_openai_misalignment/raw.jsonl` | 20 | 0.02 | 2026-09-16 20:37:39 | t | 0 |
| `watch/together_v3_ledger.jsonl` | 20 | 0.00 | 2026-09-01 12:09:43 | i | - |
| `corpus/frontier_thinking/FT_XBATCH_20260905.jsonl` | 19 | 0.01 | 2026-09-05 13:56:39 | t | 0 |
| `memory/frontier/scout_findings.jsonl` | 19 | 0.02 | 2026-08-08 23:53:14 | t | 0 |
| `memory/improve/releases/gates.jsonl` | 19 | 0.01 | 2026-09-26 09:35:47 | i | - |
| `memory/worldline/readings.jsonl` | 19 | 1.17 | 2026-09-26 05:00:44 | t | 0 |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_gender_discrimination.jsonl` | 19 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `watch/water_ledger.jsonl` | 19 | 0.01 | 2026-09-01 15:03:45 | i | - |
| `memory/word_map/word_skills.jsonl` | 18 | 0.00 | 2026-08-09 14:44:12 | t | 0 |
| `mine/raw/agent_bleeding_edge/getzep/zep/ingestion/examples/data/chat_history.jsonl` | 18 | 0.00 | 2026-08-05 20:34:13 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_military_discrimination.jsonl` | 18 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_religion_discrimination.jsonl` | 18 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `watch/harvest_digest.jsonl` | 18 | 0.01 | 2026-09-01 19:57:54 | i | - |
| `memory/portable_bags/bag-20260727T214646Z/memory/biography/registry.jsonl` | 17 | 0.03 | 2026-07-27 17:46:07 | i | - |
| `memory/portable_bags/bag-20260727T214646Z/memory/biography/verkle_chain.jsonl` | 17 | 0.01 | 2026-07-27 17:46:07 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_age_discrimination.jsonl` | 17 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/litellm/proxy/guardrails/guardrail_hooks/litellm_content_filter/guardrail_benchmarks/evals/block_disability_discrimination.jsonl` | 17 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `watch/MEMORY_RIB.jsonl` | 17 | 0.01 | 2026-09-05 23:05:36 | i | - |
| `watch/inbox/wave_20260916/receipts/D22_probe_pass2.jsonl` | 17 | 0.01 | 2026-09-16 14:09:53 | t | 0 |
| `attic/MANIFEST.jsonl` | 16 | 0.00 | 2026-09-23 07:38:06 | t | 0 |
| `corpus/library/openai-cookbook/examples/partners/agentic_governance_guide/eval_data/input_guardrail_test_data.jsonl` | 16 | 0.01 | 2026-09-04 12:25:51 | i | - |
| `state/fuel/stealth_selfimp_queue.jsonl` | 16 | 0.01 | 2026-09-28 13:54:01 | i | - |
| `watch/inbox/mrpool_export/called_shot_ledger.jsonl` | 16 | 0.01 | 2026-09-18 18:15:48 | t | 0 |
| `watch/meter_readings.jsonl` | 16 | 0.01 | 2026-09-01 07:34:22 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/economist.jsonl` | 15 | 0.01 | 2026-09-05 18:03:09 | i | - |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/elder.jsonl` | 15 | 0.00 | 2026-09-12 17:38:28 | t | 0 |
| `memory/falsifier/close_rate.jsonl` | 15 | 0.01 | 2026-09-05 00:25:27 | t | 0 |
| `watch/openclaw_traj.jsonl.bounds.jsonl` | 15 | 0.00 | 2026-08-30 21:14:31 | i | - |
| `memory/train_data/resident_actor_seed.jsonl` | 14 | 0.01 | 2026-08-18 12:18:25 | t | 0 |
| `queue/lanes/research/inbox.jsonl` | 14 | 0.00 | 2026-09-18 20:23:58 | t | 0 |
| `state/fuel/x_churn_seed_hits.jsonl` | 14 | 0.01 | 2026-09-23 21:59:00 | i | - |
| `watch/inbox/mrpool_export/vision_nightly_receipts.jsonl` | 14 | 0.00 | 2026-09-28 02:30:02 | t | +1 |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/bard_ledger.jsonl` | 13 | 0.01 | 2026-09-05 18:03:09 | i | - |
| `corpus/ractor_ribs/JUNG/case_law.jsonl` | 13 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `logs/compiler_flywheel.jsonl` | 13 | 0.00 | 2026-08-11 13:13:03 | i | - |
| `queue/lanes/builder/inbox.jsonl` | 13 | 0.01 | 2026-09-18 20:23:58 | t | 0 |
| `state/fuel/stealth_work_queue.jsonl` | 13 | 0.01 | 2026-09-28 18:27:32 | i | - |
| `watch/inbox/burn_wave_20260926/B2_178_events_SMOKE.jsonl` | 13 | 0.00 | 2026-09-26 14:58:39 | t | 0 |
| `watch/inbox/physical_computing/receipts/SALON_FREE_20260916_raw.jsonl` | 13 | 0.02 | 2026-09-16 13:12:14 | t | 0 |
| `watch/salon_glm53/pass2/.openclaw/trajectory-exports/openclaw-trajectory-602a99d9-2026-09-01T12-32-10/events.jsonl` | 13 | 0.36 | 2026-09-01 08:32:11 | t | 0 |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/android_surface.jsonl` | 12 | 0.01 | 2026-09-05 18:03:09 | i | - |
| `corpus/ractor_ribs/BERNAYS/case_law.jsonl` | 12 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `dashboard-deploy/static/trails/android_surface.jsonl` | 12 | 0.01 | 2026-09-24 06:41:14 | t | 0 |
| `dashboard/static/trails/android_surface.jsonl` | 12 | 0.01 | 2026-09-04 16:31:32 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/android_surface.jsonl` | 12 | 0.01 | 2026-09-04 16:31:32 | t | 0 |
| `logs/blast.jsonl` | 12 | 0.00 | 2026-07-31 13:37:42 | i | - |
| `memory/corpus/quantized_thought/adversarial_arc_invariants.jsonl` | 12 | 0.01 | 2026-09-18 11:35:51 | t | 0 |
| `memory/corpus/quantized_thought/instructions_flash.jsonl` | 12 | 0.00 | 2026-09-28 12:19:05 | t | 0 |
| `memory/corpus/quantized_thought/instructions_local.jsonl` | 12 | 0.00 | 2026-09-28 12:19:05 | t | 0 |
| `memory/handoff/peer_trail.jsonl` | 12 | 0.00 | 2026-09-01 03:23:27 | i | - |
| `memory/improve/blast/lattice/verkle_chain.jsonl` | 12 | 0.01 | 2026-08-07 15:08:32 | i | - |
| `memory/spore_seeds/testseat.jsonl` | 12 | 0.00 | 2026-09-26 17:24:12 | t | 0 |
| `mine/raw/agent_bleeding_edge/getzep/zep/ingestion/examples/data/combined_threads.jsonl` | 12 | 0.00 | 2026-08-05 20:34:13 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/azure_fine_tune.jsonl` | 12 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/proxy_unit_tests/azure_fine_tune.jsonl` | 12 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/steal_protocol/arvarik/bmas/eval/fixtures/mmlu.jsonl` | 12 | 0.00 | 2026-08-05 19:04:35 | i | - |
| `queue/lanes/android_surface/trail.jsonl` | 12 | 0.01 | 2026-09-04 16:31:32 | t | 0 |
| `watch/steer_exp_001_receipts.jsonl` | 12 | 0.00 | 2026-08-31 22:57:37 | i | - |
| `corpus/ractor_ribs/ELLUL/case_law.jsonl` | 11 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/FREUD/case_law.jsonl` | 11 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/PLATO_KIRK/case_law.jsonl` | 11 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `memory/behavior/agents.jsonl` | 11 | 0.00 | 2026-08-15 10:31:46 | t | 0 |
| `mine/raw/agent_platform/mifunedev/openharness/.oh/skills/prompt-miner/scripts/__tests__/fixtures/claude-sample.jsonl` | 11 | 0.00 | 2026-08-05 20:38:21 | i | - |
| `state/vast/burst_results.jsonl` | 11 | 0.00 | 2026-08-27 15:19:17 | i | - |
| `watch/LANE_METRICS_20260901.jsonl` | 11 | 0.00 | 2026-08-31 22:41:36 | i | - |
| `watch/inbox/burn_reset_20260927/queue/Q_007_rows.jsonl` | 11 | 0.01 | 2026-09-28 12:59:26 | t | 0 |
| `watch/inbox/burn_reset_20260927/queue/RECIPROCITY_LEDGER.jsonl` | 11 | 0.01 | 2026-09-28 14:46:42 | U | - |
| `watch/night_ticker.jsonl` | 11 | 0.00 | 2026-09-01 06:19:25 | i | - |
| `corpus/library/ms-genai-beginners/18-fine-tuning/python/openai/training-data.jsonl` | 10 | 0.00 | 2026-09-04 11:49:30 | i | - |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/harvest.jsonl` | 10 | 0.00 | 2026-09-12 17:38:28 | t | 0 |
| `mine/raw/agent_bleeding_edge/getzep/zep/zep-eval-harness/runs/chunk_sets/1_20260331T222430/chunks.jsonl` | 10 | 0.01 | 2026-08-05 20:34:14 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/openai_fine_tuning.jsonl` | 10 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/steal_protocol/arvarik/bmas/eval/fixtures/gsm8k.jsonl` | 10 | 0.01 | 2026-08-05 19:04:35 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FastChat/fastchat/llm_judge/data/vicuna_bench/reference_answer/gpt-4.jsonl` | 10 | 0.01 | 2026-08-05 19:04:47 | i | - |
| `state/fuel/cooker_ledger.jsonl` | 10 | 0.01 | 2026-09-27 20:04:34 | i | - |
| `watch/inbox/duty_fuzz/cycle_000.jsonl` | 10 | 0.02 | 2026-09-19 12:06:24 | t | 0 |
| `watch/inbox/duty_fuzz/cycle_001.jsonl` | 10 | 0.02 | 2026-09-19 12:10:57 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_00.jsonl` | 10 | 0.01 | 2026-09-19 10:23:40 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_01.jsonl` | 10 | 0.01 | 2026-09-19 10:23:27 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_02.jsonl` | 10 | 0.01 | 2026-09-19 10:24:41 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_03.jsonl` | 10 | 0.01 | 2026-09-19 10:25:08 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_06.jsonl` | 10 | 0.01 | 2026-09-19 10:25:10 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_07.jsonl` | 10 | 0.01 | 2026-09-19 10:23:57 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_09.jsonl` | 10 | 0.01 | 2026-09-19 10:24:04 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_10.jsonl` | 10 | 0.01 | 2026-09-19 10:30:00 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_11.jsonl` | 10 | 0.01 | 2026-09-19 10:29:42 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_13.jsonl` | 10 | 0.01 | 2026-09-19 10:29:39 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_14.jsonl` | 10 | 0.01 | 2026-09-19 10:29:58 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_15.jsonl` | 10 | 0.01 | 2026-09-19 10:30:15 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_16.jsonl` | 10 | 0.01 | 2026-09-19 10:29:59 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_18.jsonl` | 10 | 0.01 | 2026-09-19 10:30:26 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_19.jsonl` | 10 | 0.01 | 2026-09-19 10:30:19 | t | 0 |
| `watch/receipts/pin_audit_history.jsonl` | 10 | 0.00 | 2026-09-26 05:00:44 | t | 0 |
| `_archaeology_out/mag-disk-20260905/dashboard/static/museum.jsonl` | 9 | 0.00 | 2026-09-05 18:03:09 | i | - |
| `corpus/ractor_ribs/BAUDRILLARD/case_law.jsonl` | 9 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/FOUCAULT/case_law.jsonl` | 9 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/HALL/case_law.jsonl` | 9 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/MCLUHAN/case_law.jsonl` | 9 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/WALLAS/case_law.jsonl` | 9 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `dashboard-deploy/static/museum.jsonl` | 9 | 0.00 | 2026-09-24 06:41:15 | t | 0 |
| `dashboard/static/museum.jsonl` | 9 | 0.00 | 2026-09-02 21:58:08 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/museum.jsonl` | 9 | 0.00 | 2026-09-02 21:58:08 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/forge.jsonl` | 9 | 0.00 | 2026-09-12 17:38:28 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/night.jsonl` | 9 | 0.00 | 2026-09-11 19:00:46 | t | 0 |
| `state/library/catalog_runs.jsonl` | 9 | 0.00 | 2026-09-28 09:15:15 | i | - |
| `watch/engine_z_queue.jsonl` | 9 | 0.00 | 2026-09-03 13:47:43 | i | - |
| `watch/inbox/burn_reset_20260927/flash50/work/r-or-cache_probe_results.jsonl` | 9 | 0.00 | 2026-09-28 08:58:32 | U | - |
| `watch/steers.jsonl` | 9 | 0.01 | 2026-09-11 16:51:14 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/elder.jsonl` | 8 | 0.00 | 2026-09-05 18:03:09 | i | - |
| `bridge/operator_inbox.jsonl` | 8 | 0.01 | 2026-09-16 10:16:28 | t | 0 |
| `corpus/library/kev/evals/smoke-v1/calibration.jsonl` | 8 | 0.02 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/smoke-v1/train.jsonl` | 8 | 0.02 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/ablation-v2/results.jsonl` | 8 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/auto-06b-r1/results.jsonl` | 8 | 0.02 | 2026-09-21 16:00:34 | i | - |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/prose.jsonl` | 8 | 0.00 | 2026-09-12 17:38:28 | t | 0 |
| `logs/ractor_lite_panel_20260926.jsonl` | 8 | 0.02 | 2026-09-26 21:35:50 | i | - |
| `memory/corpus/augmentation_canon/manifest.jsonl` | 8 | 0.00 | 2026-09-16 20:12:00 | t | 0 |
| `memory/tangents/queue.jsonl` | 8 | 0.00 | 2026-08-16 09:06:45 | t | 0 |
| `mine/raw/steal_protocol/togethercomputer/moa/FastChat/fastchat/llm_judge/data/judge_prompts.jsonl` | 8 | 0.01 | 2026-08-05 19:04:47 | i | - |
| `state/m12_armed_nights.jsonl` | 8 | 0.00 | 2026-09-28 06:50:54 | i | - |
| `state/vast/wedge_ledger.jsonl` | 8 | 0.00 | 2026-08-28 22:50:59 | i | - |
| `watch/GO_LEDGER.jsonl` | 8 | 0.00 | 2026-09-06 17:26:01 | i | - |
| `watch/cost_gate_ledger.jsonl` | 8 | 0.00 | 2026-09-01 03:28:57 | i | - |
| `watch/riddler_common.jsonl.bounds.jsonl` | 8 | 0.00 | 2026-08-30 21:16:20 | i | - |
| `watch/s4_steering_receipts.jsonl` | 8 | 0.00 | 2026-09-01 03:28:41 | i | - |
| `watch/salon_glm53/lane_c_probe_receipts.jsonl` | 8 | 0.00 | 2026-09-01 08:44:15 | t | 0 |
| `corpus/library/kev/runs/auto-4b-r0-91266/results.jsonl` | 7 | 0.02 | 2026-09-21 16:00:34 | i | - |
| `corpus/telegram/gold_standard.jsonl` | 7 | 0.00 | 2026-09-05 22:09:57 | t | 0 |
| `memory/facts/x-tabs.jsonl` | 7 | 0.00 | 2026-08-11 08:32:49 | t | 0 |
| `mine/raw/agent_platform/mifunedev/openharness/.oh/skills/prompt-miner/scripts/__tests__/fixtures/pi-sample.jsonl` | 7 | 0.00 | 2026-08-05 20:38:21 | i | - |
| `state/fuel/free_lane_census.jsonl` | 7 | 0.00 | 2026-09-28 09:25:03 | i | - |
| `state/handshakes.jsonl` | 7 | 0.00 | 2026-09-07 08:03:18 | i | - |
| `watch/MODEL_VAULT_PASSPORTS.jsonl` | 7 | 0.00 | 2026-08-31 23:07:42 | i | - |
| `_archaeology_out/mag-disk-20260905/memory/game/campaign_runs/now-2026-08-15-gc-4862837e5d.jsonl` | 6 | 0.00 | 2026-09-05 18:03:10 | i | - |
| `_archaeology_out/mag-disk-20260905/memory/game/campaign_runs/now-2026-08-15-gc-5d9d0316c3.jsonl` | 6 | 0.00 | 2026-09-05 18:03:10 | i | - |
| `corpus/library/interference-search/results/llm/phase0_qwen3-1.7b.jsonl` | 6 | 0.23 | 2026-09-25 16:37:29 | i | - |
| `corpus/library/kev/runs/arch-06b/results.jsonl` | 6 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/auto-4b-r1/results.jsonl` | 6 | 0.02 | 2026-09-21 16:00:34 | i | - |
| `logs/queue_gate_claims.jsonl` | 6 | 0.00 | 2026-08-25 10:20:22 | i | - |
| `memory/facts/moderation.jsonl` | 6 | 0.00 | 2026-09-09 14:50:24 | t | 0 |
| `memory/game/campaign_runs/now-2026-08-15-gc-4862837e5d.jsonl` | 6 | 0.00 | 2026-08-15 04:21:50 | t | 0 |
| `memory/game/campaign_runs/now-2026-08-15-gc-5d9d0316c3.jsonl` | 6 | 0.00 | 2026-08-15 04:21:02 | t | 0 |
| `memory/gpu/lifecycle.jsonl` | 6 | 0.00 | 2026-08-12 02:09:14 | t | 0 |
| `queue/lanes/day_work/inbox.jsonl` | 6 | 0.00 | 2026-09-14 03:27:35 | t | 0 |
| `queue/lanes/jev/trail.jsonl` | 6 | 0.01 | 2026-09-19 11:54:29 | t | 0 |
| `state/fuel/amendments.jsonl` | 6 | 0.01 | 2026-09-28 14:38:44 | i | - |
| `state/fuel/gopher_pacing.jsonl` | 6 | 0.00 | 2026-09-28 09:26:17 | i | - |
| `state/memory/runs/lineage_audit/probe_cards.jsonl` | 6 | 0.01 | 2026-08-28 04:58:46 | i | - |
| `watch/MODEL_ATLAS_PASSPORTS_20260831.jsonl` | 6 | 0.01 | 2026-09-01 03:26:49 | i | - |
| `watch/T1_REFIX_RAW_20260907.jsonl` | 6 | 0.01 | 2026-09-07 03:25:08 | i | - |
| `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` | 6 | 0.00 | 2026-09-27 23:19:07 | t | +1 |
| `watch/inbox/LEDGER_LOCK_TEST.jsonl` | 6 | 0.00 | 2026-09-26 20:06:10 | t | 0 |
| `watch/invariant_probe_001.jsonl` | 6 | 0.00 | 2026-09-01 09:15:54 | i | - |
| `watch/lane_probe.jsonl` | 6 | 0.00 | 2026-09-28 17:49:16 | i | - |
| `watch/rbn_scores_202609.jsonl` | 6 | 0.00 | 2026-09-06 10:16:56 | i | - |
| `watch/suno/zeitgeist.jsonl` | 6 | 0.00 | 2026-09-07 18:45:32 | t | 0 |
| `watch/whale_tracker.jsonl` | 6 | 0.00 | 2026-09-08 06:08:45 | i | - |
| `corpus/library/kev/runs/backbone-v1/results.jsonl` | 5 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/calibration-screen-4b-s11-r2/results.jsonl` | 5 | 0.02 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/recipe-4b-r1/results.jsonl` | 5 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/ms-genai-beginners/18-fine-tuning/python/openai/validation-data.jsonl` | 5 | 0.00 | 2026-09-04 11:49:30 | i | - |
| `corpus/library/openai-cookbook/examples/data/toy_chat_fine_tuning.jsonl` | 5 | 0.03 | 2026-09-04 12:22:09 | i | - |
| `logs/resource_governor.jsonl` | 5 | 0.00 | 2026-08-11 12:50:43 | i | - |
| `memory/embassy/grok_tandem.jsonl` | 5 | 0.00 | 2026-09-05 22:34:27 | t | 0 |
| `memory/ideas/orphans.jsonl` | 5 | 0.00 | 2026-08-09 01:56:51 | i | - |
| `memory/improve/pins/deepseek_routing.jsonl` | 5 | 0.00 | 2026-08-07 01:23:17 | t | 0 |
| `memory/portable_bags/bag-20260727T214646Z/memory/runs/related_runs.jsonl` | 5 | 0.00 | 2026-07-27 17:42:12 | i | - |
| `memory/steal_lens/records.jsonl` | 5 | 0.00 | 2026-08-11 09:53:43 | t | 0 |
| `memory/working/agent_desk_baseline_history.jsonl` | 5 | 0.02 | 2026-09-12 21:01:39 | i | - |
| `mine/raw/agent_bleeding_edge/letta-ai/letta/tests/data/toy_chat_fine_tuning.jsonl` | 5 | 0.03 | 2026-08-05 20:33:11 | i | - |
| `state/capacity_ladder.jsonl` | 5 | 0.00 | 2026-09-11 21:06:35 | i | - |
| `state/world/goals_receipts.jsonl` | 5 | 0.00 | 2026-09-05 18:19:58 | i | - |
| `training/session_koans.jsonl` | 5 | 0.00 | 2026-08-08 20:40:28 | t | 0 |
| `watch/WAVE_LEDGER.jsonl` | 5 | 0.00 | 2026-09-09 15:51:29 | i | - |
| `watch/diff_steer_receipts.jsonl` | 5 | 0.00 | 2026-09-01 06:17:30 | i | - |
| `watch/inbox/mrpool_export/vision_waves/retry_05.jsonl` | 5 | 0.00 | 2026-09-19 10:20:47 | t | 0 |
| `watch/inbox/union_fullsend_20260917/grounding_chain.jsonl` | 5 | 0.00 | 2026-09-26 09:53:18 | t | 0 |
| `watch/invariants_proposals.jsonl` | 5 | 0.00 | 2026-08-31 23:21:15 | i | - |
| `_archaeology_out/mag-disk-20260905/memory/game/campaign_runs/fixed-2026-08-15-gc-2dfff0e775.jsonl` | 4 | 0.00 | 2026-09-05 18:03:10 | i | - |
| `bridge/inbox/broadcast.jsonl` | 4 | 0.00 | 2026-08-31 00:39:19 | t | 0 |
| `corpus/library/kev/runs/lowdrift-4b-v4/results.jsonl` | 4 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/mix-4b-knobs/results.jsonl` | 4 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/night2-4b/results.jsonl` | 4 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v3-data-capacity-s0/results.jsonl` | 4 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v3-data-capacity-s1/results.jsonl` | 4 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `memory/corpus/symbol_dictionary.jsonl` | 4 | 0.01 | 2026-09-27 19:03:56 | t | 0 |
| `memory/game/campaign_runs/fixed-2026-08-15-gc-2dfff0e775.jsonl` | 4 | 0.00 | 2026-08-15 08:14:04 | t | 0 |
| `memory/working/checkins/index.jsonl` | 4 | 0.00 | 2026-08-28 19:29:53 | i | - |
| `queue/phonesalon_runs.jsonl` | 4 | 0.00 | 2026-09-05 08:33:41 | t | 0 |
| `training/export/orch_train_2026-08-06.jsonl` | 4 | 0.00 | 2026-08-06 10:21:54 | t | 0 |
| `watch/CORPUS_TIER_D_MANIFEST.jsonl` | 4 | 0.00 | 2026-08-31 11:54:11 | i | - |
| `watch/ESTATE_ATLAS/ATTIC_MOVE_LIST.jsonl` | 4 | 0.00 | 2026-09-27 13:58:13 | t | 0 |
| `watch/GUEST_WALL.jsonl` | 4 | 0.00 | 2026-09-12 17:24:54 | i | - |
| `watch/inbox/MEMORY_GAUGE.jsonl` | 4 | 0.00 | 2026-09-26 21:07:30 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_04.jsonl` | 4 | 0.00 | 2026-09-19 10:22:01 | t | 0 |
| `watch/ponytail_log.jsonl` | 4 | 0.00 | 2026-09-01 07:09:41 | i | - |
| `watch/procurement_digest.jsonl` | 4 | 0.00 | 2026-09-01 10:41:42 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/harvest.jsonl` | 3 | 0.00 | 2026-09-05 18:03:09 | i | - |
| `_archaeology_out/mag-disk-20260905/memory/game/campaign_runs/prove2-2026-08-15-gc-a88d781a07.jsonl` | 3 | 0.00 | 2026-09-05 18:03:10 | i | - |
| `_archaeology_out/mag-disk-20260905/memory/game/campaign_runs/test-2026-08-15-gc-b0ea3efded.jsonl` | 3 | 0.00 | 2026-09-05 18:03:10 | i | - |
| `corpus/library/kev/runs/anchor-4b-v6/results.jsonl` | 3 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/night2-9b/results.jsonl` | 3 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/q35-08b/results.jsonl` | 3 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v4-06b-hardened/results.jsonl` | 3 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v7-06b/results.jsonl` | 3 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v7-final/results.jsonl` | 3 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/ractor_ribs/FERMAT/case_law.jsonl` | 3 | 0.00 | 2026-09-19 22:36:38 | t | 0 |
| `corpus/ractor_ribs/GREER/case_law.jsonl` | 3 | 0.00 | 2026-09-20 06:03:22 | t | 0 |
| `logs/transport_precheck.jsonl` | 3 | 0.00 | 2026-09-26 21:26:33 | i | - |
| `memory/archaeology/prompt_findings.jsonl` | 3 | 0.03 | 2026-09-14 10:12:03 | t | 0 |
| `memory/corpus/zcode_history/correspondence_199e4b14.jsonl` | 3 | 0.00 | 2026-09-18 00:19:55 | t | 0 |
| `memory/facts/ops.jsonl` | 3 | 0.00 | 2026-08-11 08:32:42 | t | 0 |
| `memory/game/campaign_runs/prove2-2026-08-15-gc-a88d781a07.jsonl` | 3 | 0.00 | 2026-08-15 04:30:02 | t | 0 |
| `memory/game/campaign_runs/test-2026-08-15-gc-b0ea3efded.jsonl` | 3 | 0.00 | 2026-08-14 22:23:50 | t | 0 |
| `memory/ledger/assets.jsonl` | 3 | 0.00 | 2026-08-02 14:12:44 | i | - |
| `memory/portable_bags/lattice-vast-20260729T140048Z/lattice/verkle_chain.jsonl` | 3 | 0.00 | 2026-07-29 09:55:39 | i | - |
| `memory/steer_engine/telemetry.jsonl` | 3 | 0.00 | 2026-08-12 09:59:15 | t | 0 |
| `memory/worldline/REGISTRY.jsonl` | 3 | 0.01 | 2026-09-07 09:28:51 | t | 0 |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/app/tests/fixtures/nested.jsonl` | 3 | 0.00 | 2026-08-05 20:35:06 | i | - |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/app/tests/fixtures/simple.jsonl` | 3 | 0.00 | 2026-08-05 20:35:06 | i | - |
| `mine/raw/agent_bleeding_edge/arize-ai/phoenix/app/tests/fixtures/varied-keys.jsonl` | 3 | 0.00 | 2026-08-05 20:35:06 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/openai_batch_completions_router.jsonl` | 3 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/test_batch_rate_limiting_integration.jsonl` | 3 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/proxy_unit_tests/openai_batch_completions_router.jsonl` | 3 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/test_litellm/llms/bedrock/files/expected_bedrock_batch_embeddings.jsonl` | 3 | 0.00 | 2026-08-05 20:28:23 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/test_litellm/llms/bedrock/files/input_batch_embeddings.jsonl` | 3 | 0.00 | 2026-08-05 20:28:23 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/metadata_annotation/difficulty/src/prompt.jsonl` | 3 | 0.01 | 2026-08-05 19:04:46 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/metadata_annotation/difficulty/src/reviewer.jsonl` | 3 | 0.00 | 2026-08-05 19:04:46 | i | - |
| `queue/lanes/forge/inbox.jsonl` | 3 | 0.00 | 2026-09-14 03:27:35 | t | 0 |
| `queue/lanes/prose/inbox.jsonl` | 3 | 0.00 | 2026-09-18 20:23:58 | t | 0 |
| `state/vast/battery_results.jsonl` | 3 | 0.00 | 2026-08-27 15:37:24 | i | - |
| `state/vast/blades.jsonl` | 3 | 0.00 | 2026-08-28 01:36:17 | i | - |
| `watch/inbox/QCAPTION_VERIFY_BEAT.jsonl` | 3 | 0.00 | 2026-09-28 07:30:02 | t | +1 |
| `watch/inbox/burn_wave_20260926/B2_178_out_caption_enrich_SMOKE.jsonl` | 3 | 0.00 | 2026-09-26 14:58:39 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_178_out_corpus_class_SMOKE.jsonl` | 3 | 0.00 | 2026-09-26 14:56:40 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_178_out_links_dedupe_SMOKE.jsonl` | 3 | 0.00 | 2026-09-26 14:56:29 | t | 0 |
| `watch/inbox/burn_wave_20260926/B2_178_out_links_titles_SMOKE.jsonl` | 3 | 0.00 | 2026-09-26 14:56:33 | t | 0 |
| `watch/inbox/mrpool_export/vision_errors.jsonl` | 3 | 0.00 | 2026-09-19 10:43:43 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/chunk_24.jsonl` | 3 | 0.00 | 2026-09-19 10:08:48 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_08.jsonl` | 3 | 0.00 | 2026-09-19 10:20:42 | t | 0 |
| `watch/inbox/mrpool_export/vision_waves/retry_12.jsonl` | 3 | 0.00 | 2026-09-19 10:26:51 | t | 0 |
| `watch/inbox/qdrop_export/called_shot_ledger.jsonl` | 3 | 0.00 | 2026-09-18 22:54:51 | t | 0 |
| `watch/organ_queue.jsonl` | 3 | 0.00 | 2026-09-03 16:57:16 | i | - |
| `_archaeology_out/mag-disk-20260905/memory/game/campaign_runs/prove-2026-08-15-gc-aaaeac48d8.jsonl` | 2 | 0.00 | 2026-09-05 18:03:10 | i | - |
| `corpus/library/kev/runs/autoresearch.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/knowledge-4b-v6/results.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/mix-4b-v4-b/results.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/mix-4b-v5/results.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/q35-4b-nopolicy/results.jsonl` | 2 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/q35-4b-s23/results.jsonl` | 2 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/q35-4b/results.jsonl` | 2 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/recipe-8b-r1/results.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/recipe-8b-r2/results.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v3-8b-s0/results.jsonl` | 2 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v3-smoke-02/results.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v4-4b-baseline/results.jsonl` | 2 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v7-rc3/results.jsonl` | 2 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v8-4b/results.jsonl` | 2 | 0.01 | 2026-09-21 16:00:34 | i | - |
| `corpus/papers/librarian_backfill_20260927_redo.jsonl` | 2 | 0.00 | 2026-09-27 07:32:58 | t | 0 |
| `corpus/ractor_ribs/DIOGENES/case_law.jsonl` | 2 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/EULER/case_law.jsonl` | 2 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/ractor_ribs/SOCRATES/case_law.jsonl` | 2 | 0.00 | 2026-09-20 05:28:32 | t | 0 |
| `corpus/training_materials/frontier_math_lean/cage_manifest_rows.jsonl` | 2 | 0.00 | 2026-09-05 15:24:41 | t | 0 |
| `logs/window_spawns.jsonl` | 2 | 0.00 | 2026-09-04 20:17:01 | i | - |
| `memory/agent_corpus/ledgers/saelis.jsonl` | 2 | 0.00 | 2026-09-28 12:50:22 | U | - |
| `memory/archive/museum/catalog.jsonl` | 2 | 0.00 | 2026-08-24 16:37:45 | t | 0 |
| `memory/biography/diary_nodes/index.jsonl` | 2 | 0.00 | 2026-08-06 21:23:20 | i | - |
| `memory/btw/ledger.jsonl` | 2 | 0.00 | 2026-08-11 21:20:07 | t | 0 |
| `memory/corpus/zcode_history/correspondence_712a3b7b.jsonl` | 2 | 0.00 | 2026-09-18 00:19:55 | t | 0 |
| `memory/facts/poc.jsonl` | 2 | 0.00 | 2026-08-24 11:52:18 | t | 0 |
| `memory/facts/wave.jsonl` | 2 | 0.00 | 2026-08-24 11:12:22 | t | 0 |
| `memory/game/campaign_runs/prove-2026-08-15-gc-aaaeac48d8.jsonl` | 2 | 0.00 | 2026-08-15 04:29:07 | t | 0 |
| `memory/icons/ledger.jsonl` | 2 | 0.00 | 2026-09-26 12:56:48 | t | 0 |
| `memory/improve/behavior/index.jsonl` | 2 | 0.00 | 2026-08-06 22:46:05 | i | - |
| `memory/spore_seeds/zcode.jsonl` | 2 | 0.00 | 2026-09-25 08:28:17 | t | 0 |
| `memory/working/agent_desk_meta_dialogue.jsonl` | 2 | 0.00 | 2026-08-05 14:54:37 | i | - |
| `mine/raw/agent_bleeding_edge/lastmile-ai/mcp-agent/logs/marketing-20251022_200928.jsonl` | 2 | 0.00 | 2026-08-05 20:34:01 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/batches_tests/batch_job_results_furniture.jsonl` | 2 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/batches_tests/openai_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/batches_tests/vertex_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:21 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/batch_job_results_furniture.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/example.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/openai_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/vertex_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/bedrock_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/openai_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/proxy_unit_tests/batch_job_results_furniture.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/proxy_unit_tests/openai_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/test_litellm/llms/bedrock/files/expected_bedrock_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:23 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/test_litellm/llms/bedrock/files/input_batch_completions.jsonl` | 2 | 0.00 | 2026-08-05 20:28:23 | i | - |
| `mine/raw/steal_protocol/EIT-EAST-Lab/C3/tests/fixtures/data/mini_math_train.jsonl` | 2 | 0.00 | 2026-08-05 19:04:44 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/gpt_review/src/prompt.jsonl` | 2 | 0.00 | 2026-08-05 19:04:46 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/gpt_review/src/reviewer.jsonl` | 2 | 0.00 | 2026-08-05 19:04:46 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/metadata_annotation/skillset/src/prompt.jsonl` | 2 | 0.00 | 2026-08-05 19:04:47 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/metadata_annotation/skillset/src/reviewer.jsonl` | 2 | 0.00 | 2026-08-05 19:04:47 | i | - |
| `queue/lanes/night/inbox.jsonl` | 2 | 0.00 | 2026-09-14 03:27:35 | t | 0 |
| `state/fuel/rumor_drill_ledger.jsonl` | 2 | 0.00 | 2026-09-28 12:33:14 | i | - |
| `watch/capture_ledger.jsonl` | 2 | 0.00 | 2026-09-01 15:20:12 | i | - |
| `watch/inbox/SECRET_SCAN_BEAT.jsonl` | 2 | 1.38 | 2026-09-28 07:05:40 | t | +1 |
| `watch/inbox/mrpool_export/vision_waves/retry_17.jsonl` | 2 | 0.00 | 2026-09-19 10:26:02 | t | 0 |
| `watch/inbox/quote_hitrate.jsonl` | 2 | 0.00 | 2026-09-26 00:52:52 | t | 0 |
| `watch/inbox/ractor_panel_20260926/revise_verkle99_checks/_sandbox/fake_root/memory/training/refined_training_data.jsonl` | 2 | 0.00 | 2026-09-27 00:57:56 | t | 0 |
| `watch/salon_responses/astra_union_alpha/raw.jsonl` | 2 | 0.01 | 2026-09-16 16:03:02 | t | 0 |
| `watch/salon_responses/u6_union_creative/raw.jsonl` | 2 | 0.00 | 2026-09-16 16:08:48 | t | 0 |
| `watch/steer_bus_receipts.jsonl` | 2 | 0.00 | 2026-09-03 14:26:39 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/forge.jsonl` | 1 | 0.00 | 2026-09-05 18:03:09 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/night.jsonl` | 1 | 0.00 | 2026-09-05 18:03:09 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/prose.jsonl` | 1 | 0.00 | 2026-09-05 18:03:09 | i | - |
| `_archaeology_out/mag-disk-20260905/dashboard/static/trails/trail.jsonl` | 1 | 0.00 | 2026-09-05 18:03:09 | i | - |
| `_archaeology_out/mag-disk-20260905/handoff/ox_ledger.jsonl` | 1 | 0.00 | 2026-09-05 18:03:12 | i | - |
| `_archaeology_out/mag-disk-20260905/memory/steal/surface_receipts.jsonl` | 1 | 0.00 | 2026-09-05 18:03:10 | i | - |
| `corpus/library/kev/runs/gatecheck-trial4/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/kev-4b-transfer-v9/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/kev-8b-transfer-v9/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/night2-08b-du2/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/night2-4b-dense2/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/night2-4b-du/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/night2-9b-du/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/q35-9b/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/q35-smoke/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/recipe-4b-v4-s1/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/recipe-4b-v4-s2/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/recipe-8b-s2/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/research-smoke-runner-v2/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/research-smoke-runner-verified/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/research-smoke-runner/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/smoke-anchor/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/smoke-arch/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/smoke-hl/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/smoke-mix/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/smoke/results.jsonl` | 1 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `dashboard-deploy/static/trails/trail.jsonl` | 1 | 0.00 | 2026-09-24 06:41:14 | t | 0 |
| `dashboard/static/trails/trail.jsonl` | 1 | 0.00 | 2026-09-04 11:34:55 | t | 0 |
| `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/trails/trail.jsonl` | 1 | 0.00 | 2026-09-04 11:34:55 | t | 0 |
| `handoff/ox_ledger.jsonl` | 1 | 0.00 | 2026-08-22 12:34:18 | t | 0 |
| `logs/cache_ab_probe.jsonl` | 1 | 0.00 | 2026-08-25 11:32:31 | i | - |
| `logs/consensus_witness.jsonl` | 1 | 0.00 | 2026-08-25 09:44:35 | i | - |
| `memory/analytics/quantized/L0/2026-08-09.jsonl` | 1 | 0.00 | 2026-08-08 20:29:22 | t | 0 |
| `memory/analytics/quantized/L1/2026-08-09.jsonl` | 1 | 0.00 | 2026-08-08 20:29:22 | t | 0 |
| `memory/connect/links.jsonl` | 1 | 0.00 | 2026-08-15 19:27:14 | t | 0 |
| `memory/connect/peers.jsonl` | 1 | 0.00 | 2026-08-15 19:27:14 | t | 0 |
| `memory/copilot/bridge_log.jsonl` | 1 | 0.00 | 2026-08-08 23:06:38 | i | - |
| `memory/dspy/optimization_log.jsonl` | 1 | 0.00 | 2026-08-08 22:51:21 | t | 0 |
| `memory/embassy/AOS/grok_usage.jsonl` | 1 | 0.00 | 2026-08-09 09:08:58 | t | 0 |
| `memory/facts/game.jsonl` | 1 | 0.00 | 2026-08-14 12:21:44 | t | 0 |
| `memory/facts/infra.jsonl` | 1 | 0.00 | 2026-08-11 08:02:22 | t | 0 |
| `memory/facts/probe.jsonl` | 1 | 0.00 | 2026-08-16 12:51:26 | t | 0 |
| `memory/facts/providers.jsonl` | 1 | 0.00 | 2026-08-11 08:02:19 | t | 0 |
| `memory/facts/security.jsonl` | 1 | 0.00 | 2026-08-25 12:24:08 | t | 0 |
| `memory/improve/growth/growth_trail.jsonl` | 1 | 0.00 | 2026-08-05 09:44:34 | i | - |
| `memory/learn/ollama_renders.jsonl` | 1 | 0.00 | 2026-08-10 19:22:03 | t | 0 |
| `memory/learn/recurrences.jsonl` | 1 | 0.00 | 2026-08-12 08:50:00 | t | 0 |
| `memory/ledger/exit_dialogues.jsonl` | 1 | 0.01 | 2026-08-08 18:51:33 | i | - |
| `memory/pile/behavioral_corpus.jsonl` | 1 | 0.00 | 2026-08-10 18:34:20 | i | - |
| `memory/pile/classified_packs.jsonl` | 1 | 0.00 | 2026-08-07 19:53:08 | i | - |
| `memory/registry_state/swarm_pod/history.jsonl` | 1 | 0.00 | 2026-08-10 12:07:35 | t | 0 |
| `memory/republic_wave/wave.jsonl` | 1 | 0.00 | 2026-08-12 16:42:38 | t | 0 |
| `memory/seeds/seeds.jsonl` | 1 | 0.00 | 2026-08-24 10:52:14 | t | 0 |
| `memory/steal/surface_receipts.jsonl` | 1 | 0.00 | 2026-08-30 22:28:01 | t | 0 |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/input.jsonl` | 1 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/input_azure.jsonl` | 1 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/out.jsonl` | 1 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/BerriAI/litellm/tests/openai_endpoints_tests/out_azure.jsonl` | 1 | 0.00 | 2026-08-05 20:28:22 | i | - |
| `mine/raw/agent_platform/SWE-agent/SWE-agent/tests/test_data/trajectories/gpt4__swe-bench-dev-easy_first_only__default__t-0.00__p-0.95__c-3.00__install-1/all_preds.jsonl` | 1 | 0.00 | 2026-08-05 20:28:01 | i | - |
| `mine/raw/steal_protocol/EIT-EAST-Lab/C3/tests/fixtures/data/mini_code_eval.jsonl` | 1 | 0.00 | 2026-08-05 19:04:44 | i | - |
| `mine/raw/steal_protocol/EIT-EAST-Lab/C3/tests/fixtures/data/mini_code_eval_plus.jsonl` | 1 | 0.00 | 2026-08-05 19:04:44 | i | - |
| `mine/raw/steal_protocol/EIT-EAST-Lab/C3/tests/fixtures/data/mini_code_train.jsonl` | 1 | 0.00 | 2026-08-05 19:04:44 | i | - |
| `mine/raw/steal_protocol/EIT-EAST-Lab/C3/tests/fixtures/data/mini_math_eval.jsonl` | 1 | 0.00 | 2026-08-05 19:04:44 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/metadata_annotation/domain/src/prompt.jsonl` | 1 | 0.00 | 2026-08-05 19:04:46 | i | - |
| `mine/raw/steal_protocol/togethercomputer/moa/FLASK/metadata_annotation/domain/src/reviewer.jsonl` | 1 | 0.00 | 2026-08-05 19:04:46 | i | - |
| `queue/lanes/economist/inbox.jsonl` | 1 | 0.00 | 2026-09-04 11:09:31 | t | 0 |
| `state/art_queue.done.jsonl` | 1 | 0.00 | 2026-09-04 20:58:52 | i | - |
| `state/m12_baseline.jsonl` | 1 | 0.00 | 2026-09-11 16:50:39 | i | - |
| `training/model_tiers.jsonl` | 1 | 0.00 | 2026-08-08 23:18:41 | t | 0 |
| `watch/bay/repair/claim_repair_receipts.jsonl` | 1 | 0.00 | 2026-09-05 00:09:45 | t | 0 |
| `watch/cursor_feed.jsonl` | 1 | 0.00 | 2026-08-04 10:12:06 | i | - |
| `watch/inbox/IMAGE_DROPS.jsonl` | 1 | 0.00 | 2026-09-26 15:51:09 | t | 0 |
| `watch/inbox/OPERATOR_GO.jsonl` | 1 | 0.00 | 2026-09-26 16:46:44 | t | 0 |
| `watch/inbox/asekin113/GRADING_LEDGER.jsonl` | 1 | 0.00 | 2026-09-26 14:56:46 | t | 0 |
| `watch/inbox/fts_index_alerts.jsonl` | 1 | 0.00 | 2026-09-26 15:43:52 | t | 0 |
| `watch/inbox/ractor_panel_20260926/revise_verkle99_checks/_sandbox/counter_as_tail.jsonl` | 1 | 0.00 | 2026-09-27 00:57:50 | t | 0 |
| `watch/suno/mirror_control.jsonl` | 1 | 0.00 | 2026-09-08 14:13:51 | t | 0 |
| `corpus/library/kev/evals/external/scienthoon-v1/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/external/scienthoon-v1/test.jsonl` | 0 | 0.00 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/external/scienthoon-v1/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/external/semif-v1/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:33 | i | - |
| `corpus/library/kev/evals/external/semif-v1/test.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/external/semif-v1/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/round3/decision-r3/test.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/round3/transfer-r3/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/transfer-v1/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/transfer-v1/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/transfer-v2/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/transfer-v2/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v3/smoke-v3/test.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v3/transfer-v3/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v3/transfer-v3/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v4/transfer-v4/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v4/transfer-v4/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v5/transfer-v5/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v5/transfer-v5/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v6/transfer-v6/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v6/transfer-v6/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v9/transfer-v9/calibration.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/evals/v9/transfer-v9/train.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v7-4b-s2/results.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `corpus/library/kev/runs/v7-8b/results.jsonl` | 0 | 0.00 | 2026-09-21 16:00:34 | i | - |
| `memory/working/agent_desk_dialogue.jsonl` | 0 | 0.00 | 2026-09-12 21:01:39 | i | - |
| `queue/lanes/android_surface/inbox.jsonl` | 0 | 0.00 | 2026-09-04 10:43:28 | t | 0 |
| `queue/lanes/bard_ledger/inbox.jsonl` | 0 | 0.00 | 2026-09-04 10:43:28 | t | 0 |
| `queue/lanes/elder/inbox.jsonl` | 0 | 0.00 | 2026-09-04 10:43:28 | t | 0 |
| `state/art_queue.jsonl` | 0 | 0.00 | 2026-09-04 20:58:52 | i | - |
| `state/arxiv/2026-09-08/digest.jsonl` | 0 | 0.00 | 2026-09-08 05:49:03 | i | - |
| `state/arxiv/2026-09-12/digest.jsonl` | 0 | 0.00 | 2026-09-12 02:31:29 | i | - |
| `state/arxiv/2026-09-13/digest.jsonl` | 0 | 0.00 | 2026-09-13 02:31:10 | i | - |
| `state/arxiv/2026-09-14/digest.jsonl` | 0 | 0.00 | 2026-09-14 02:32:04 | i | - |
| `state/arxiv/2026-09-15/digest.jsonl` | 0 | 0.00 | 2026-09-15 02:30:59 | i | - |
| `state/arxiv/2026-09-19/digest.jsonl` | 0 | 0.00 | 2026-09-19 02:30:52 | i | - |
| `state/arxiv/2026-09-20/digest.jsonl` | 0 | 0.00 | 2026-09-20 02:30:31 | i | - |
| `state/arxiv/2026-09-26/digest.jsonl` | 0 | 0.00 | 2026-09-26 02:30:32 | i | - |
| `state/arxiv/2026-09-27/digest.jsonl` | 0 | 0.00 | 2026-09-27 02:30:04 | i | - |
| `watch/inbox/bearableguy_export/called_shot_ledger.jsonl` | 0 | 0.00 | 2026-09-18 19:50:45 | t | 0 |
| `watch/inbox/burn_lane_flip_cards.jsonl` | 0 | 0.00 | 2026-09-26 16:07:19 | t | 0 |
| `watch/inbox/mrpool_export/comments.jsonl` | 0 | 0.00 | 2026-09-18 10:53:08 | t | 0 |
| `watch/inbox/mrpool_export/metadata_unreachable_20260926.jsonl` | 0 | 0.00 | 2026-09-26 13:43:27 | t | 0 |

## 8. Anomalies (measured, not judged)

1. **Split pointer on the executor tape.** `mag/bash_local.py:47` points `TAPE` at
   `memory/runs/trajectory/steps.jsonl` (102 rows, 136202 bytes, untracked, last touched 2026-09-09 13:28:33) while the live
   tape is `memory/trajectory/steps.jsonl` (30770 rows, 30.4 MB, +3,271 rows vs HEAD, mtime today 18:50).
   Code comment and live path have diverged; whoever reads the tape via bash_local reads a stale sidecar.
2. **Production JSONL with malformed rows** (json.loads failure, files outside agents/ pytest trash): 29 files.

| file | bad rows | total rows | first bad line |
|---|---:|---:|---:|
| `watch/wargames_v0/match_003/moves.jsonl` | 205 | 205 | 1 |
| `watch/wargames_v0/match_002/moves.jsonl` | 76 | 76 | 1 |
| `logs/supervisor.jsonl` | 65 | 107905 | 845 |
| `watch/wargames_v0/match_004/board2/moves.jsonl` | 40 | 40 | 1 |
| `watch/wargames_v0/match_001/moves.jsonl` | 39 | 39 | 1 |
| `watch/wargames_v0/match_004/board1/moves.jsonl` | 31 | 31 | 1 |
| `mine/raw/agent_platform/BerriAI/litellm/tests/local_testing/vertex_ai.jsonl` | 20 | 22 | 1 |
| `state/shared_activity.jsonl` | 20 | 107586 | 2979 |
| `memory/ghost/noise/behavioral.jsonl` | 19 | 36156 | 16187 |
| `state/decisions_done.jsonl` | 14 | 14 | 1 |
| `memory/runs/orchestrator_trail.jsonl` | 13 | 31887 | 3236 |
| `memory/runs/hermes_jobs/hofw_001_receipt.jsonl` | 12 | 12 | 1 |
| `memory/runs/hermes_jobs/hofw_hofw_001_receipt.jsonl` | 12 | 12 | 1 |
| `state/fuel/full_scan_ledger.jsonl` | 12 | 19135 | 237 |
| `watch/LANE_METRICS_20260901.jsonl` | 11 | 11 | 1 |
| `memory/runs/swarm_health/trail.jsonl` | 10 | 84907 | 74 |
| `memory/trajectory/steps.jsonl` | 8 | 30770 | 7176 |
| `memory/decisions_log.jsonl` | 6 | 213260 | 17962 |
| `memory/runs/compaction_eval/steps_frozen_20260920.jsonl` | 5 | 8674 | 7176 |
| `logs/failure_kb.jsonl` | 4 | 112203 | 7805 |
| `memory/vault/astra_v2_companions/failure-ledger-frozen-prefix.jsonl` | 4 | 74852 | 7805 |
| `memory/runs/improve_loop_trail.jsonl` | 3 | 603 | 66 |
| `watch/inbox/index_events.jsonl` | 3 | 5194 | 94 |
| `watch/room.jsonl` | 3 | 13866 | 486 |
| `memory/agent_state/chain.jsonl` | 2 | 19855 | 433 |
| `memory/biography/repair_backups/verkle_20260831T0212Z/verkle_chain.jsonl` | 2 | 4914 | 2288 |
| `memory/runs/ghost/trail.jsonl` | 1 | 18618 | 1774 |
| `state/fuel/record_briefs.jsonl` | 1 | 4275 | 3387 |
| `watch/inbox/fts_index_alerts.jsonl` | 1 | 1 | 1 |

   The remaining 29 parse-bad files are pytest fixtures that are corrupt on purpose
   (`agents/pytest-tmp-*/.../test_cli_corrupt_ledger_fails_0`, `test_malformed_lines_are_skipp0`,
   `test_scout_row_absent_when_win0` writing 80 junk rows). Their existence is the tests working, not rot.
3. **88 empty .jsonl files.** Mostly pytest-tmp scaffolding and agent-desk dialogue scaffolds; none of the
   A1 operational ledgers are empty.
4. **Schema drift is the norm, not the exception:** 2598 of 11854 files carry more than one top-level key
   family (append-only ledgers that gained columns over time, e.g. `watch/inbox/index_events.jsonl`
   has 8 key families across 5194 rows; `memory/decisions_log.jsonl` 7 families). Readers must be
   tolerant; the shared-surface validator already treats unknown event keys as warnings (mag/shared_surface.py:253).
5. **Twin giants:** ESTATE_INDEX exists row-count-identical (3,485,538 rows each, measured) in `watch/ESTATE_INDEX/`
   and `dashboard/data/`, one walk two outputs (tools/index/projects_index.py:31,34). 2.58 GB combined.
6. **training/events.jsonl root mirror:** root copy 574628 rows vs memory/training copy 574625 rows (3-row drift).
   All code readers point at the memory/ copy; the root copy has zero literal code references and grew
   +5,485 rows today, so some writer copies it that never names it literally (dynamic path build).

## 9. Cross-checks against other lanes' carriers

- f-16 (index truth audit) claimed `LINKS.jsonl` = 378-row URL ledger: this sweep measures exactly
  378 rows on `watch/inbox/LINKS.jsonl` (+1 uncommitted row since HEAD). MATCH.
- f-16 claimed event log 5,114 lines at its sweep: this sweep measures 5194 on
  `watch/inbox/index_events.jsonl` (+672 vs HEAD). Consistent: the log keeps appending; fold still pending.
- f-16 said `memory/percolator/invariants.json` is plain JSON: confirmed no `invariants.jsonl` exists
  (path absent from the 11,854-file set).

## 10. Method, limits, honesty notes

- Row count = non-empty lines, byte-read, same instrument for disk and `git show HEAD:` so deltas
  compare like with like.
- Schema sampling: 25 files over 20 MB had keysets collected from their first 20,000 rows only
  (flagged `schema_sampled` in raw). All A1 files except the ESTATE_INDEX twins, ingest registry and
  training streams were fully parsed.
- Reader mapping is literal-string grep. Ledgers whose paths are built dynamically
  (`FACT_DIR / f"{d}.jsonl"`, lane trails via `glob("queue/lanes/*/trail.jsonl")`) are matched by
  their writer modules, listed above; a basename hit is NOT proof that exact file is read.
- `git check-ignore --stdin` in the original sweep pass silently produced no output (reason not
  reproduced; a fresh run of the identical command returned 11,364 ignored paths). The ignored flags
  in `_f26_raw.json` were patched from that verified rerun (`_f26_ignored.txt`); tracked/untracked
  flags and every row count are from the original pass and were not touched.
- mtimes are a snapshot at 18:30-18:42 local; the estate is live (logs/usage.jsonl,
  memory/trajectory/steps.jsonl were rewritten while this doc was being written), so counts drift
  by design. Denominator law applies: this is one tree at one moment.

