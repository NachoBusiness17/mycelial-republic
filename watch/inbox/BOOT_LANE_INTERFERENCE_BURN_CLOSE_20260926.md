# BOOT LANE: INTERFERENCE BURN — CLOSE RECEIPT (running close, 2026-09-26 ~04:45Z)

Operator went to bed at ~01:00 with "just go, you have my permission." This
receipt covers the night; it updates in place when Arm C lands. Plan of record:
watch/inbox/BOOT_LANE_INTERFERENCE_BURN_20260925.md.

## Scoreboard (night of 09-25 / morning of 09-26)

1. **Interference-search replication** — ARM B PASS 30/30 EXACT vs published
   (judge-alone 21/30 exact, 13.7ms/problem, torch CPU). ARM A gemma-text 0/30
   (~80 tok/problem, no thinking mode; filed as-is). ARM C budget-50: 0/30,
   frozen bar kept, matches their own trained judge's weakness at 50.
   **ARM C budget-200: RUNNING, 1/30 with the first problem SOLVED (n=1, no
   claims until the leg completes).** Prereg + amendment 1 governed every arm;
   zero bars moved after results.
2. **Referee (stone 6) CAST** on operator GO: GLM prime cold via nous.
   water_first @ 0.6 = LEAN NOT PROOF; saddle-law ruling: a third vote adds a
   fourth path, RIB CONTESTED stands; settlement = adventure_2d6 +0.017 to the
   HILL bar (cheapest hill) + engram on-manifold; 5 flip conditions on file.
   Receipt: watch/inbox/REFEREE_VERDICT_20260926.md.
3. **Eigen-map overlay BUILT** (the 09-21 candidate build, unblocked by the
   referee outcome): tools/cathedral_eigen_map.py ->
   watch/inbox/CATHEDRAL_EIGEN_MAP_20260926.html. Regions at eigen_centroids,
   water_first chain drawn with missing stitches dashed, hub_first faint,
   hop table with distance/bearing, referee line in the header. 5 regions in
   eigen space, 4 wired cross-region edges, stub modules off-map (recorded).
4. **Wave 1 dwfrun-217c37f5**: 9/9 lanes, 45 rows, ACCEPT, ALL FILED. Punch
   list executed: pile write-back verified (FULL DRAIN 137/137, 0 errors, the
   snapshot gauge finally moves), chain_guard healed to healthy (dangling all
   flagged; canary itself stale = re-mark after next repair), md_record verdict
   now in the audit JSON (verified live), seal-verify in pre-push (gala-b2),
   runbook drift fixed, drift.py/pile-CLI premise drifts receipted in the fold.
5. **Shared-surface fold REBUILT** (punch 7): scripts/index_fold_host.mjs
   rebuild folded 2,527 events -> 730 active items. Debt honestly transformed:
   fold no longer stale; 207 files have NO register event at all = writer
   contract debt. Proposed fix (not landed while other seats run): the
   md_record_seal hook should append a register event alongside the autoseal.
   Verify also flagged 3 registered-but-missing files (cathedral_v1.html,
   QUIET_RADAR_20260921.md, LINKS.jsonl path drift) — morning triage rows.
6. **Box burn (stone 7)**: watcher tools/box_burn_watch.py live to 07:00,
   curve in state/fuel/box_burn_watch.jsonl (night peaks: CPU 88%, GPU 53%).
   **GPU unlock discovered**: llama-server.exe already drives the RX 5600 XT
   via llama.cpp Vulkan while ollama runs CPU-only; wiring estate lanes to it
   is the unlock. Whisper backlog corpus NOT FOUND at shallow depth (no D:/E:
   drives; likely taken in the 09-21 purge) — needs operator pointer.
7. **LAW-11 armed** and unused tonight (nothing needed rescuing): nous wired
   in providers.yaml + fuel_feed rescue tier, live armed-check True.
8. **Defender storm**: diagnosed as convergence load with zero threats;
   operator added the exclusions himself. Root cause of the pre-reboot stall
   was real-time scanning racing a genuine multi-process write night.

## Still open at this receipt's timestamp

- Arm C 200-leg completion (folds here on notification; bars frozen: >= 15/30
  secondary, reference trained-judge 30/30).
- Grok seat packet (stone 5) awaiting the Grok window (ends ~09-28).
- Writer-contract fix: seal hook -> register event (207 unindexed files).
- Fold-rebuild triage rows: cathedral_v1.html + QUIET_RADAR missing, LINKS
  path drift, drift-patrol nonce gaps.
- GLM deep-read paced rerun + Cooper synthesis (stone 3 tail).
- Ghost supervisor 30s error loop (reaper PATH) — Defender bait, still owed.

## ARM C 200-leg status addendum (2026-09-26T21:45Z, B2-140 close-out fold)

The leg still has NOT landed; no solve count exists and the >=15/30 secondary
reading stays unmeasured. Byte state: the full-leg attempt launched 20:04Z
with the keep_alive 2h gemma pin completed problem 1 (solved, rounds 3) and
was killed at ~21:10Z still inside problem 2 (run log:
memory/runs/interference_replication_20260925/armC_200_run_log.txt, last line
"budget=200 [1/30] solved=True rounds=3"; output file holds exactly 1 row) --
66 minutes for 1/30 projects a multi-hour leg against the 09-28 window close,
and the process was stopped rather than left to burn the box overnight.
Prior partials preserved verbatim: armC_200_attempt1_starved.jsonl,
armC_200_attempt2_partial.jsonl, armC_200_attempt3_partial.jsonl (each 1 row,
problem 1 solved). Bars remain frozen per amendment 1 (>=15/30 secondary,
trained-judge 30/30 interference reference); nothing is claimed from n=1.
OWED for the next lane with box time: rerun
`memory/runs/interference_replication_20260925/run_armC.py` to completion
(prior partials are archived; the script rewrites
armC_gemma2b_judge_200.jsonl from scratch), then fold the final solve count
into this receipt against the frozen bar. Receipt:
watch/inbox/burn_wave_20260926/B2_140_armc_closeout_20260926.md.
