# B2-150 receipt: reconcile the 232-vs-84 blocked-line delta (2026-09-26, lane SW-03)

## Verdict

PARTIAL MAP LANDED, RESIDUE FILED UNKNOWN WITH EVIDENCE. The 84 is byte-confirmed as the exact count of unique supervisor-mediated autorun spawns across 9/14+9/16+9/19 (started rows 9 + 45 + 30), and the paired auto_restarted rows (8 + 42 + 28, same ts+pid as their started rows) are DUPLICATE event marks, not additional spawns. The detached relauncher is RULED OUT for the streak (its log's content dates to August). The slot log is proven SHARED across slot programs ([swarm-grok-watch] lines bound the streak), so file-line arithmetic cannot attribute spawns. The residual ~148 blocked lines cannot be attributed per-line from retained bytes: mag_launch-slot and manual -c spawns leave no supervisor rows by design and no other retained log records autorun spawns in the window; the blocked lines carry no timestamps. Filed unknown per the brief's second branch, with the log-retention defect named.

## Evidence file:line quotes

- logs/supervisor_autorun.out.log:5477-5708: exactly 232 consecutive "[autorun] blocked: Docker-only runtime is active" (recounted live this lane; total file 7,801 lines), bounded by line 5476 "[swarm-grok-watch] WATCHING (4/12 fail)" and line 5709 "[swarm-grok-watch] WATCHING (2/12 fail)" (the shared-slot proof).
- logs/supervisor.jsonl (byte count this lane): 2026-09-14 events started 9 / auto_restarted 8 / stopped 1; 2026-09-16 started 45 / auto_restarted 42 / stopped 2; 2026-09-19 started 30 / auto_restarted 28 / stopped 1. Sample pairing from the 9/19 burst: "15:06:33 started 7284" + "15:06:33 auto_restarted 7284"; "17:31:02 auto_restarted ...17872", "17:31:17 ...37172" (B2-51's citations) sit inside the same paired scheme; pid 37172's spawn ran ~13h (B2-51: "stopped, autorun, pid 37172" at 9/20T06:04:36Z) and printed no blocked line, so supervisor-attributed blocked lines are at most 83 and the unattributed residue is at least 149.
- logs/autorun_detached.log (6 lines, whole file read): two "--- autorun relaunch ---" banners plus orphan/janitor/framework-map rows only; its rows surface in memory/vault/astra_v2_companions/failure-ledger-frozen-prefix.jsonl dated 2026-08-08T18:08Z and 2026-09-06T22:34Z, none in 9/14-9/19; repo-wide grep finds no script currently writing the banner (no live relauncher in the tree).
- watch/inbox/burn_wave_20260926/B2_51_autorun_autopsy_20260926.md: "232 exceeds the 84 supervisor-logged starts across 9/14+9/16+9/19; the delta is spawn sources sharing the slot log without supervisor rows (detached relauncher pattern, logs/autorun_detached.log)" (the open thread this receipt closes).
- watch/inbox/AUTORUN_AUTOPSY_20260919.md:5: the earlier receipt's "5,708 blocked lines, 20 days" figures (the false claims B2-51 corrected; not reused here).

## Work done

- Byte-recounted the streak (232) and precisely re-counted supervisor.jsonl autorun events per day with the venv interpreter; established the started/auto_restarted same-ts-same-pid pairing that makes 84 the unique-spawn count.
- Traced every writer candidate for the slot log: detached relauncher (ruled out by content dating and absence from the tree), mag_launch slot and manual -c runs (searched queue/handoff + watch/inbox: named as live mechanisms in AUTORUN_AUTOPSY_20260919.md's test-fixture note, but they leave no supervisor rows and no spawn log by design).
- Named the log-retention defect that makes final attribution impossible: the blocked lines are timestamp-less and the only autorun spawn ledger retained for 9/14-9/19 is supervisor.jsonl.

## Falsifier

Kill conditions: (a) a retained log produced that attributes specific 9/14-9/19 autorun spawns outside supervisor.jsonl (would move lines from unknown into a named source; none exists today), (b) a counted mismatch in the 84 or the pairing claim (rerun the per-day event tally; pairing is visible in the raw rows), (c) detached-relauncher activity inside 9/14-9/19 (its log and the failure-ledger sigs would show it; they show August only). The unknown is NOT permanent: any future spawn route that writes this slot log should timestamp its lines and log its spawns, or the next storm reopens the same wall.

## Bibliography closed

- logs/supervisor_autorun.out.log (streak + bounding lines read)
- logs/supervisor.jsonl (per-day autorun event tally, pairing sample read)
- logs/autorun_detached.log (whole file)
- memory/vault/astra_v2_companions/failure-ledger-frozen-prefix.jsonl (autorun_detached sigs, dates)
- watch/inbox/burn_wave_20260926/B2_51_autorun_autopsy_20260926.md (read in full)
- watch/inbox/AUTORUN_AUTOPSY_20260919.md (read)
- queue/handoff/HANDOFF-2026-08-08-SANCHO-SPIKE.json, queue/handoff/zcode/CONVO.md (mag_launch mentions, searched)
- mag/process_supervisor.py:318, mag/runtime_policy.py:22 (corrected-receipt comments, read)
