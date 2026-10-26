# B2-19 improve backlog analysis — 2026-09-26

## Verdict

69 pending candidates (63 new, 6 hold) in memory/improve/candidates.jsonl. Real: 3 (promote). Decoration: 66 (kill). The queue is a stale telemetry mirror: the scout pipeline last wrote 2026-08-31 (state.json last_scout 2026-08-08) while the underlying logs kept growing, so most candidates are frozen counter snapshots of facts that later moved.

3 strongest for operator promote review:
1. `c-5074b7228c67` (risk, FKB write_file:9e0b1bd29 x102). Real meter: 1,440 log events, grew 10x after sibling c-d8fc978dc44e was promoted 2026-08-06 and nothing changed. Stopped 2026-09-22; promote to force a closure verdict (fixed vs source dried up). Remedy already drafted: memory/remedies/rem-write-file-param-shape.md.
2. `c-b341f669f3ea` (risk, FKB run_shell:c73866f2f1b5 x580 "backend reported failure"). Largest signature: 25,328 log events, burst 09-10/09-11, tail to 09-23. Promote to force naming the producer call path.
3. `c-e46d14ea4db4` (tesuji, leaf 2026-08-08, 8 wins). Leaf verified on disk with concrete practices (verify-before-declare, spec gate, penny-spec, loop-escalate, seam placement). Feeds the HABIT.md weekly "promote practices you will run" loop.

Kill families (all verified decoration): 3 web stubs (claims are nav junk from failed reddit/github fetches, matching state.json failed_urls); 6 IJL hold gauges (n=4..22, superseded series; live count is 26 bead .md files on disk); 12 behavioral counters (leaves already on disk through 2026-09-26); 6 crash counters (log tail is INJECTED test rows); 3 decisions counters; 2 heal-smoke duplicates; 15 superseded FKB snapshots (keep newest per fingerprint only); 7 tesuji counters minus the promoted one; 13 lifecycle gap rows (stale: build_lifecycle() run today returns gaps=[lab, scribe], waste=[]).

## Evidence

- mag/improve.py:2143-2198 promote_apply: risk/tesuji promote is a status flip plus training event; only kind=practice writes the playbook (2173-2182); models never auto-edit lanes (2158-2171, configs/improve.yaml:269-272). Most pending promotes cannot change a meter by construction.
- logs/failure_kb.jsonl: 39,245,410 bytes, 108,858 events. write_file:9e0b1bd292e0 last_seen 2026-09-22T23:07; run_shell:c73866f2f1b5 25,328 events.
- memory/failure_kb/signatures.json: first_seen 2026-09-22T14:55 on both fingerprints: the index was reset, losing cross-session counts (candidate says x580, index says 28). Claims and index are not comparable.
- mag/process_reaper.py:82-90 fix receipt ("bare powershell not on PATH... 79,864 reaper-enumerate-error rows"); bare calls persist in gpu_ghost.py:84, legacy_audit.py:181, icon_drop.py:131, offerings.py:152, platform_kill.py:65, loop_breaker.py:99, saelis_room.py:57, power.py:165: 11,818 events run_shell:e566037def80 since 2026-09-19, 228 today. No candidate exists for the live defect.
- tests/test_temperature_stack.py:67 force=True pollutes the production candidate ledger (gap-c4f076b1e0205c27); tests/test_seat_crash_guard.py:35 injects crash rows into logs/seat_crashes.log.
- memory/improve/pins/deepseek_rank_latest.md: all 5 top candidates held as "unverified/vague" by the ranker.

## Work done

Read candidates.jsonl (132 rows, all statuses), SEATS.md, HABIT.md, state.json, field_brief.md, latest.md, eval history, deepseek rank; read promote gate (main.py:2014-2030, mag/improve.py:898-970, 2143-2216, configs/improve.yaml); ran build_lifecycle() live; parsed the full 39MB FKB log; verified leaves, beads, session records, crash log, queue format.

## Falsifier

- c-5074b7228c67: if any write_file param-shape event recurs post-promote without a named fix commit, the promote was decoration.
- c-b341f669f3ea: if no producer of "backend reported failure" can be named in code within one session, kill instead.
- c-e46d14ea4db4: if none of the 5 named practices appears in a playbook append or applied steer within 7 days, it was reading material, not a promote.
- Kill set: if any killed candidate's claim is contradicted by current disk bytes (counters excepted), re-file it.

## Bibliography closed

memory/improve/{SEATS.md,HABIT.md,state.json,candidates.jsonl,field_brief.md,latest.md,pins/deepseek_rank_latest.md,pins/skills/,daily/2026-08-08-tesuji-shells.md,daily/2026-09-26-behavioral.md}; configs/improve.yaml; mag/{improve.py,failure_kb.py,temperature_stack.py,process_reaper.py,lifecycle.py}; main.py; logs/{failure_kb.jsonl,seat_crashes.log}; memory/{failure_kb/signatures.json,remedies/rem-write-file-param-shape.md,remedies/rem-auto-run-shell-c73866f2f1b5.md,decisions_log.jsonl,agent_sessions/orc-*.json}; tests/{test_temperature_stack.py,test_seat_crash_guard.py}.
