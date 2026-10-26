# CHAIN RESTORE 2026-10-15 (Option A executed)

Status: DONE, verified. UNSIGNED (signing with the seed_seal Ed25519 key is the operator's call; not done).
Operator approval: Nacho, Oct 15 2026 8:33 PM ET, "Do both: guards, then the 12,016-row restore" (Option A).
Plan of record: CHAIN_RESTORE_PLAN.md (archaeology workspace, Oct 14 9:45 PM ET, with the Oct 15 appendices).
Times are ET (UTC-4) unless marked Z. HEAD at execution: 8bb6eb6a2.

## What happened (cause)

- tests/test_merkle_cure_p4b_sized.py (added in 6685db6bc, Oct 8) had one test,
  test_cross_arm_composition_leaf_domain_untouched, that called _hand_chain() without the
  estate fixture. Every pytest run including it reset the LIVE memory/biography/verkle_chain.jsonl
  to 3 fixture rows (f0/f1/f2, sessions s0/s1/s2). First hit Oct 7 between about 3:12 and 3:29 PM ET;
  it happened at least twice (the Oct 9 backup and the pre-restore live chain differ after the
  same 3 fixture rows).
- After the reset, mag/knot_at_close.py --backfill saw almost every session as "not in the chain"
  and re-knotted 3,025 already-chained sessions, appended 2026-10-10 03:28Z to 03:52Z.
- A later tip write left tip root 2b1da0ea while the chain root was ae71aee2, so the append gate
  refused every append from Oct 10 03:52Z until now.
- Guards landed before this restore: a2ae802a6 (hermetic test fix + live-estate write fence in
  tests/conftest.py) and 274a6b020 (pin biography_backup_20261004 against pruning).

## Dead fork (kept, not deleted)

- Pre-restore live chain: n=3,415, chain root ae71aee2558f1419f4a451e4798f24a82d5954c4106fef837c5559c4a2adabee,
  tip root 2b1da0ea599a0755cfa87254224b29840a53f38004cb6939b4db2afe45a9306d (tip n_leaves 3,415).
- Kept at memory/biography/verkle_chain.jsonl.bak-preRestore-20261014
  (sha256 eb07097cbe05b348dee736451f32d2f4488f6773e5f453d46758453cfd6d91fa) and
  memory/biography/verkle_tip.json.bak-preRestore-20261014
  (sha256 9fa7056b4784cae44c470510451d166b267567a70b5b5195eff5ea20bc1b0618).
- Both also in the vault (C:\MagChainVault\20261014\files\ and the off-PC box copy).
- Any receipt, pointer_chain.jsonl or topic_evolution.json entry quoting ae71aee2 or 2b1da0ea
  refers to this dead fork. They stay as history.

## Vault

- C:\MagChainVault\20261014\MANIFEST.txt sha256 f58928904292d2dcacb2a85c3b0ef141d901c71fbdbb529f4eaa8c0de8197e85
  (same hash on the off-PC box copy).
- biography_backup_20261004.tar.gz sha256 b0600b7c2d718a9c4148f09d569fb46a8d694c43ccfb4135bde061edddf53584,
  re-hashed tonight, matches the manifest.

## New chain

- Rows: 12,016 = 11,218 (biography_backup_20261004, verbatim) + 411 (lost window Oct 4 to Oct 7,
  from knot files) + 387 (new sessions from the post-overwrite live chain).
- Rows 0 to 11,217 are byte-for-byte the pinned backup rows; root at row 11,217 is still
  9ce1b18083403d7cd4c0e79332ef6493bf5f34f38523493fafe7005c026a8f9e at swap time. CAVEAT (see
  step 9): the writer's normal in-place amend path re-roots every row after an amended index, so
  this held only until the first amend at 8:41:31 PM (row 76). Earlier receipts quoting old roots
  are now provable only against the vault and the pinned backup, not against the live chain.
- The 798 replayed rows carry restore_batch "chain-restore-20261014" and restored_from
  ("knot_file:lost_window_20261004_20261007" x411, "live_chain_20261009_post_overwrite" x387).
  They have new roots; they were never on a chain with these parents.
- New root: ab595c338ac0a39434015e6dca3ab7fa9a745e0624376e64373062b0192495fe (n_leaves 12,016).
- verkle_chain.jsonl sha256 0da8026d498261525f0e3a32107ef9221c94f87ec63f1fcea76ca3e0d45cd6ac, 8,619,201 bytes.
- verkle_tip.json sha256 bbf9c1890d1c583bfc2f59ed300a23afcf7b5483409bf1a1a6aa0626c14200af
  (differs from the Oct 14 sandbox tip only in updated_minute).

## Excluded

- 3 fixture rows (f0/f1/f2.knot.json, sessions s0/s1/s2, leaf = sha256 of "fixture-leaf-{i}").
- 3,025 duplicate re-knots of sessions already in the backup. Their knot files stay in knots/;
  the chain references the backup's versions (found in knots_attic). Cosmetic follow-up owed.

## Steps run tonight

| Step | What | Result |
|---|---|---|
| pre | guards a2ae802a6, 274a6b020, 6e499adfc, fda902344 in git log; conftest fence present; pinned folder present; lab writer PID 123455 state T | held |
| 0 | vault backup tar hash = manifest; live chain eb07097c, tip 9fa7056b = manifest; knots 48,032 and knots_attic 265,223 files, 0 newer than 2026-10-10 03:53Z | unchanged, proceed |
| 4 | fresh rebuild with build_candidate.py (sha256 2afb1027, same as the box copy) | rows 12,016, root ab595c33, verifier OK=True, chain sha256 0da8026d (identical to Oct 14) |
| 5 | copy the 43 restorable dangling knots from the Sep 6 knots tar extract into knots_attic (no overwrite) | 43 copied, 0 pre-existing, 0 hash differences vs source |
| 6 | swap under mag.verkle_knot.verkle_lock (heartbeat lock from fda902344), live hashes re-asserted inside the lock, live chain+tip renamed to .bak-preRestore-20261014 | swapped 8:37 PM ET |
| 7 | scripts/verify_verkle_full.py (no --json) | rows 12,016; leaf ok 12,006, mismatch 0, dangling 10; prefix/parent/n_leaves mm 0; linkage break 0; tip ok True; root ab595c33; OK=True |
| 7 | mag/_verify_chain_now.py | chain_rows 12,016, tip_root ab595c338ac0a394, tip_leaves 12,016. Its dangling=3,083 counts knots/ only (3,073 rows resolve in knots_attic + 10 truly dangling). evidence_lost_flags=618: all inherited from the backup rows (max index 4,785; the backup itself carries 618) |

Dangling 10 (down from 59 in the sandbox). The plan expected a floor of 16 (August knots with a
colon in the name, which Windows cannot create); the live verifier reports 10. All 10 are inside the verbatim backup range (row index 2,513 to
7,587), none in the 798 replayed rows: rows 2513 (2026-08-11_1952_mem-invariant-map_mem_inva_{'ok': F.knot.json),
5547, 7371, 7372, 7373, 7374, 7376, 7424, 7479, 7587 (Aug 15 to Sep 11 session/mag knots).
Note: os.path.isfile() reports the colon-named August knots as present on this NTFS volume (likely
alternate data streams on a base file), so they no longer count as dangling. Not investigated.

## The 43 knots restored into memory/biography/knots_attic

2026-08-31_0430_session_01a05615_d7154345, 2026-09-04_0024_session_01a069cd_677b2a73,
2026-09-04_0222_session_01a06a39_7ce093ad, 2026-09-04_0234_mag_01a06a44_4028b61b,
2026-09-05_1717_mag_01a07292_4892bfbc, 2026-09-05_1820_mag_01a072cc_efa2c8e0,
2026-09-05_1913_mag_01a072fd_3a32ecb4, 2026-09-05_1930_mag_01a0730c_3e649aca,
2026-09-05_2141_session_01a07384_abad13ab, 2026-09-06_0209_mag_01a0747a_9c034723,
2026-09-06_0225_session_01a07488_c29d7bbc, 2026-09-06_0226_constitution_01a07489_b332abc0,
2026-09-06_0228_mag_01a0748b_0ba61519, 2026-09-06_0230_mag_01a0748d_b56f56cb,
2026-09-06_0233_mag_01a07490_0970b51c, 2026-09-06_0234_mirror_01a07491_0b9fd398,
2026-09-06_0234_mirror_01a07491_ac80dd65, 2026-09-06_0242_mag_01a07498_d60874cf,
2026-09-06_0241_mag_01a07498_63ce6877, 2026-09-06_0241_mag_01a07498_337c8dec,
2026-09-06_0351_mag_01a074d7_33f9c288, 2026-09-06_0353_mirror_01a074da_c061221c,
2026-09-06_0353_mirror_01a074d9_534718b1, 2026-09-06_0357_mag_01a074dd_e0fc3cef,
2026-09-06_0402_mirror_01a074e1_accb3afc, 2026-09-06_0506_mag_01a0751c_f6bfad7d,
2026-09-06_0511_mag_01a07520_d6912d0e, 2026-09-06_0524_mag_01a0752d_37ecfd7e,
2026-09-06_0534_mirror_01a07536_776ae755, 2026-09-06_0538_mag_01a0753a_787270ac,
2026-09-06_0541_mirror_01a0753c_fc330554, 2026-09-06_0608_mag_01a07555_92676a9f,
2026-09-06_0621_mag_01a07560_2422047e, 2026-09-06_0709_mag_01a0758c_76ec4e87,
2026-09-06_0808_mag_01a075c3_20b1d891, 2026-09-06_0908_mag_01a075fa_203b12ca,
2026-09-06_1008_mag_01a07631_87c6202d, 2026-09-06_1108_mag_01a07667_f11a61d8,
2026-09-06_1115_mirror_01a0766e_19238027, 2026-09-06_1118_mag_01a07670_2f695e29,
2026-09-06_1208_mag_01a0769e_4f885c84, 2026-09-06_1308_mag_01a076d5_7bffd10f,
2026-09-06_1402_session_01a07706_12f2357d (each name + ".knot.json").
List file: %TEMP%\magarch\restored43.txt.

## Rollback (pause the lab writer first)

One command, PowerShell:

    $B='C:\Users\foste\Documents\projects\local_sovereign_agent\memory\biography'; Remove-Item "$B\verkle_chain.jsonl","$B\verkle_tip.json"; Rename-Item "$B\verkle_chain.jsonl.bak-preRestore-20261014" verkle_chain.jsonl; Rename-Item "$B\verkle_tip.json.bak-preRestore-20261014" verkle_tip.json

Optional, to undo step 5 as well:

    Get-Content $env:TEMP\magarch\restored43.txt | % { Remove-Item -LiteralPath "$B\knots_attic\$_" }

Rolling back after new appends discards those appends (they would sit on the restored chain only).

## Staleness of every reused artifact

| Artifact | Source date | Verified at HEAD 8bb6eb6a2 tonight | Outcome |
|---|---|---|---|
| Vault MANIFEST.txt + biography_backup_20261004.tar.gz | Oct 14 9:10 PM | manifest sha256 f5892890 on PC and box; tar re-hashed b0600b7c | match, reused |
| Pinned memory/biography_backup/biography_backup_20261004 | Oct 3 10:51 PM (backup) | new chain rows 0 to 11,217 compared row by row to its verkle_chain.jsonl | identical, reused |
| %TEMP%\magrestore\biography_backup_20261004 (extract) | Oct 14 | used by the rebuild; output rows 0 to 11,217 equal the pinned backup | match, reused |
| replay_lost_window.json (411) | Oct 14 9:13 PM | sha256 cb243baf, same as box; 0 knots newer than Oct 10 03:53Z; live chain unchanged | still valid, reused |
| replay_live_new.json (387) | Oct 14 9:13 PM | sha256 72bba9ce, same as box; live chain still eb07097c | still valid, reused |
| dangling59.json | Oct 14 9:16 PM | sha256 56127b7e, same as box; 43/43 sources present, 0 targets existed | valid, used for step 5 |
| %TEMP%\magrestore\livecopy knots (Oct 14 snapshot) | Oct 14 9:05 PM | live knots 48,032 files, none newer than Oct 10 03:53Z | equivalent to live, reused |
| %TEMP%\magrestore\knots_sep6 (Sep 6 tar extract) | Oct 14 9:02 PM | 43 copies hash-equal to source; verifier leaf mismatch 0 | valid |
| build_candidate.py | Oct 14 9:14 PM | sha256 2afb1027, same as box; rerun tonight | output identical (0da8026d) |
| Oct 14 sandbox candidate (box copy) | Oct 14 9:14 PM | superseded by tonight's rebuild | identical chain hash; tip differs only in updated_minute |
| mag/verkle_knot.py (hash + lock code) | changed in fda902344 Oct 15 2:17 PM | diff touches only lock/heartbeat helpers, not _merkle_prefix_roots/_h; swap ran under the new heartbeat lock | compatible |
| scripts/verify_verkle_full.py, mag/_verify_chain_now.py | at HEAD | run tonight on the candidate and on live | OK=True |
| CHAIN_RESTORE_PLAN.md forensic counts (11,218 / 411 / 387 / 3,025 / 3) | Oct 14 9:45 PM | rebuild printed B 11218 + lost 411 + live_new 387; restore_batch counter 411/387 on live | confirmed |

## Observations (not resolved here)

- memory/biography top-level dossier files were last written 2:42 PM ET Oct 15, after the
  12:46 PM SIGSTOP of lab PID 123455. Writer unknown; quiet for about 6 hours before the restore.
- A .verkle.lock with mtime 8:37:08 PM was present just before the swap script started
  (8:37:11 PM); the swap then acquired the lock at about 8:37:24 PM. Holder not identified.
  The live chain and tip hashes were re-asserted unchanged inside the lock before the rename,
  so nothing was lost, but this is an unattributed lock touch.
- The append gate was closed since Oct 10 by the tip/root mismatch; the restored tip matches,
  so appends resumed immediately (step 9).

## Step 9: writer resumed, then re-paused

- 8:40:30 PM: docker exec mag-sovereign kill -CONT 123455 (lab writer, /app/main.py lab --no-dashboard).
- 8:40:30 PM: FIRST NEW APPEND. Row 12,016 = 2026-10-16_0040_autonomous-janitor_autonomo_tc451f43.knot.json,
  session autonomous-auto-fkb-5a70b6, new knot file written. n=12,017.
- 8:41:31 PM: IN-PLACE AMEND of row 76 (session mag-agent-orc-t0f89ff8fcf, amended=True): knot
  2026-08-09_2340_mag_mag-agen_55f4099a moved to knots_attic, replaced by ..._0095af06. Every
  verkle_root from row 76 onward was recomputed (11,940 of the first 12,016 rows now differ from
  the restored file in root/parent fields; leaves other than row 76 unchanged). The tip was
  rewritten to match.
- 8:42:05 PM: writer re-paused (kill -STOP 123455, no .verkle.lock held). State T.
- Verify after the append+amend: scripts/verify_verkle_full.py rows 12,017, leaf ok 12,007,
  mismatch 0, dangling 10, prefix/parent/n_leaves mm 0, linkage break 0, tip ok True,
  root e53b5ee03b9feb759b753008f91713800bd0f59caa2b93bd2f2f7e0036ed0a7f, OK=True.
  mag/_verify_chain_now.py: chain_rows 12,017, tip_leaves 12,017, evidence_lost_flags 618 (inherited).
- Snapshot of that state: %TEMP%\magarch\post_resume_snapshot_2042\ (chain sha256
  a24b1610fd71cd70f72efe7b4feb5785eb8c61ddd4c634656510cd8ea348d9da, tip sha256
  26b301240736207cc1ccb916ac3152272dcf7b9f3627d3e6799a1dff69d58628).
- Why it is paused: this is not a re-backfill (1 append, no mass append). It is the writer's
  normal amend path (2,959 rows were already flagged amended in the Oct 4 backup). But the lab was
  amending one mag-agent-orc dossier about every 68 s with about 3,313 sessions incomplete, and with
  the append gate open again each amend now re-roots the chain from that row onward. Letting it run
  means thousands of history re-roots. That is an operator decision, so it is paused.
- Operator options: (1) resume as-is (docker exec mag-sovereign sh -c "kill -CONT 123455") and accept
  that historical roots move on every amend; (2) keep paused until the amend path is changed to
  append amendment rows instead of re-rooting history; (3) return to the exact restored state by
  copying %TEMP%\magrestore\candidate\memory\biography\verkle_chain.jsonl and verkle_tip.json back
  under verkle_lock (drops the 8:40 PM append row and the row-76 amend; both knot files stay on disk).

## 9:15 PM: operator chose option 3 (reset to the restored 12,016 rows, writer paused). NOT executed.

- At 9:15 PM the paused lab PID 123455 no longer existed: mag-sovereign was restarted at 9:00:17 PM
  (docker StartedAt 01:00:17Z). Its new lab process (container PID 13) was writing; it was paused
  with kill -STOP 13 at 9:16:15 PM and is state T.
- More importantly, about a dozen HOST lab writers are running on Windows (main.py lab, ports 8765 to
  8768, started 8:45 to 9:10 PM, several launched by another agent's zcode CLI session trying to bring
  the lab web UI back). They hold .verkle.lock in turn and are amending the chain in place.
- Between 8:42 PM and 9:17 PM about 190 rows were amended in place (leaf changes at rows 7 to 8,421,
  mostly mag-agent-orc sessions) plus one more append (row 12,017, 2026-10-15_1842_session_01a140df).
  Chain sha256 changed during reads (3877c0e9, befafd05, 8cc6d67f); one read-only verify caught a
  tip/root race (OK=False, tip 4eb67108 vs chain 8c13046f) while they were writing.
- The swap was not run: with live host writers that cannot be SIGSTOPped and belong to another
  agent's task, a reset would be raced and overwritten within seconds. Operator decision needed on
  stopping or suspending the host lab processes first.
- Evidence snapshots (outside the repo): %TEMP%\magarch\post_resume_snapshot_2042\ (a24b1610) and
  %TEMP%\magarch\snapshot_2117_blocked\ (chain befafd05, tip 64532947).
- The exact restored state is still available at %TEMP%\magrestore\candidate (chain 0da8026d).

## Oct 16 11:51 AM: operator approved suspend + pause + reset (option 3). Done 11:53 AM to 12:02 PM.

Operator decision (Oct 16 11:51 AM ET): "Yes, suspend the leftover lab processes (reversibly), pause
the container lab, and do the reset."

### Writers stopped (reversibly)
- 28 Windows python processes running "main.py lab" (14 launcher/interpreter pairs, started Oct 15
  8:45 to 9:24 PM ET, default port and 8766 to 8769) suspended with NtSuspendProcess at 11:53:14 AM.
  All 28 returned 0 and every thread shows WaitReason Suspended (rechecked 12:02 PM: 28 of 28).
  PIDs, parents, start times and command lines: %TEMP%\magarch\suspended_lab_pids_20261016.txt.
  Their launchers (cmd /k, cmd /c mag.cmd lab, nohup, zcode bash shells) were not touched; each
  started its lab once and none was relaunching.
- Resume command (PowerShell):
    powershell -NoProfile -ExecutionPolicy Bypass -File $env:TEMP\magarch\resume_lab_pids_20261016.ps1
- Container lab: mag-sovereign had restarted again at Oct 15 9:25 PM ET; its lab is PID 13
  (/app/main.py lab --no-dashboard). Paused with kill -STOP 13 at 11:53:49 AM, no lock held by it,
  state T. Resume: docker exec mag-sovereign sh -c "kill -CONT 13".
- Quiet window: no top-level memory/biography file written from 11:53:05 AM to the swap at 11:59:37 AM
  (6.5 min), except .verkle.lock.
- .verkle.lock touches in that window came from tools/chain_repair.py --dry, launched by the
  stealth driver (run_stealth_driver.py, running since Oct 8) with a 180 s timeout. It is read-only
  but takes the lock when it sees an inconsistency. Its 11:48 AM run (pid 30984) died holding the
  lock; its 11:57 AM run (pid 49648) held it until about 11:59:35 AM. It was not suspended.

### Reset
- Before: live chain sha256 e49453bfb14874f73c0bdc2df32cc272f4b4a1d485a686d693a4bba212aa7129 (12,054 rows),
  tip sha256 ffee774391dd2e6986d027a627eb1f48fd44b2ba621b22a25d59a9052796c3e1.
- Renamed (inside verkle_lock, never deleted) to memory/biography/verkle_chain.jsonl.bak-postResume-20261015
  and memory/biography/verkle_tip.json.bak-postResume-20261015 (hashes re-checked after the rename).
- Under verkle_lock (acquired 11:59:37 AM): candidate sha256 re-checked
  0da8026d498261525f0e3a32107ef9221c94f87ec63f1fcea76ca3e0d45cd6ac, then candidate chain and tip
  copied in. Live chain = 0da8026d, tip = bbf9c1890d1c583bfc2f59ed300a23afcf7b5483409bf1a1a6aa0626c14200af.
- What the 12,054-row state held beyond the restored file (kept in the .bak and as knots on disk):
  38 appended rows, all genuinely new sessions not in the restored chain (23 untagged law, 13
  autonomous-janitor, 1 session_01a140df, 1 memlang), Oct 16 00:40Z to 09:35Z; and 1,932 in-place
  leaf rewrites of rows 0 to 12,015 (1,924 of them inside the Oct 4 backup range), one per session,
  with every root after the first rewrite recomputed. All replacement knots and 1,931 of 1,932
  originals are on disk; the one missing original is already one of the 10 pre-existing dangling.

### One append landed 1 second after the swap
- 11:59:37 AM: a writer that was waiting on verkle_lock appended row 12,016:
  2026-10-16_1559_untagged_memlang-_1cdf4945.knot.json, session
  memlang-press--harvest---verb--turn-trail-receipts-into--155925228307, amended False,
  parent_verkle_root ab595c33 (the restored root). It is an append, not a rewrite: rows 0 to 12,015
  are byte-identical to the restored file (the first 8,619,201 bytes still hash to 0da8026d).
  The writer was short-lived and is not identified (not a lab process; no log names the session).
  It was kept, not truncated: it is a real new session on top of the restored chain.

### Verify (scripts/verify_verkle_full.py, no --json), 11:59:45 AM
rows=12017 checked=12017 no_leaf_hash=0 leaves=12017 bad_json=0
leaf_hash: ok=12007 mismatch=0 dangling=10 unreadable=0 (file!=row 0; attic=3081 diary_nodes=0)
prefix: root ok=12017 mm=0 | parent ok=12017 mm=0 | n_leaves ok=12017 mm=0 | naive xcheck bad=[]
linkage: ok=12017 break=0
tip: root_ok True, n_leaves_ok True, last_leaf_hash_ok True, last_filename_ok True, tip_root 4c596a149b68fc01, ok True
OK=True
- Live now: chain sha256 98aa5d446d73e089ecd964a0fd2651e29b084e86f0e449dc9b2ddddafcdb2a92,
  tip sha256 7a586913d5d54f22fd5e18a8614dd55e2e9a77f2dcc22f5dbef0a05ace257945, root
  4c596a149b68fc01b8e39b5aee92888f5c9d36d6e6cf9ecf791834842bee980b (n=12,017). Unchanged at the
  12:02 PM recheck.

### Writers stay stopped
All 28 Windows lab processes stay suspended and container lab PID 13 stays paused until amends are
written as correction rows instead of in-place root rewrites. Resuming any lab writer before that
will start rewriting history roots again.

### Rollback (suspend/pause writers first)
To the 12,054-row post-resume state:
    $B='C:\Users\foste\Documents\projects\local_sovereign_agent\memory\biography'; Remove-Item "$B\verkle_chain.jsonl","$B\verkle_tip.json"; Rename-Item "$B\verkle_chain.jsonl.bak-postResume-20261015" verkle_chain.jsonl; Rename-Item "$B\verkle_tip.json.bak-postResume-20261015" verkle_tip.json
(This drops the 11:59:37 AM memlang append row; its knot file stays on disk.)

## Final: operator decision and what the signature certifies (Oct 16 12:35 PM ET)

- Operator decision: keep the 11:59:37 AM memlang row (row 12,016,
  2026-10-16_1559_untagged_memlang-_1cdf4945.knot.json). No truncation.
- What this signature certifies: the FIXED restored chain of 12,016 rows,
  sha256 0da8026d498261525f0e3a32107ef9221c94f87ec63f1fcea76ca3e0d45cd6ac (8,619,201 bytes),
  root ab595c338ac0a39434015e6dca3ab7fa9a745e0624376e64373062b0192495fe.
  A copy of that exact file is at %TEMP%\magrestore\candidate\memory\biography\verkle_chain.jsonl
  and on the box at /workspace/mag-archaeology-oct/restore/candidate_verkle_chain.jsonl.
  It does NOT certify the moving live tip.
- Live chain is append-only on top of it. As of signing (12:35 PM ET):
  n=12,019, root 15b7c73a7985eff0c6fbb5a616b1bd754022df264628fb0b8c128ca195a03632,
  chain sha256 31e28229d66db7778d34c07b95e1025c7c687134f57a3e1d2d30cd116e001c5f,
  tip sha256 c5eeb75d0a0ed5e7268be15f0ea75eff04b45e275e6794899784bbc55599220c.
  The first 8,619,201 bytes of the live file (rows 0 to 12,015) are byte-identical to the restored
  file. Rows 12,016 to 12,018 are appends with amended False: the memlang row (11:59 AM) and two
  autonomous-janitor rows (12:13 PM, 12:26 PM).
- Writers: 28 Windows main.py lab processes suspended (resume script
  %TEMP%\magarch\resume_lab_pids_20261016.ps1); container lab PID 13 paused (state T).
  An unidentified autonomous-janitor appender still adds rows about every 13 minutes
  (append-only, amended False so far). Not paused; not yet identified.
- Signing: mag/seed_seal.py (seed_seal.v1) over this receipt plus the companion
  CHAIN_RESTORE_20261015.chain.json (session "chain-restore-20261015", anatomy.arc_root = the
  restored root). The seal is the .seal sidecar next to this file. Any edit to this receipt
  after signing breaks the seal.
- Key caveat: seed_seal.load_signing_key() silently mints and saves a NEW key if
  state/keys/seed_seal_key is missing. Existence of that file was confirmed (contents never
  read) immediately before signing, so the existing key was used. Compare the key_id in the
  .seal with keyinfo to detect any future silent key replacement.
