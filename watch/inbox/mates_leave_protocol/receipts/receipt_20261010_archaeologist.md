# Receipt: archaeologist, mission 20261010_03, Q-001 verkle seed thread (CLOSED) + live incident found

Mate: THE ARCHAEOLOGIST. Pack: logs/mates/missions/mission_20261010_03_archaeologist.md.
Filed: 2026-10-10, before speech and again at close, per the pack contract.
Stop reason: seed thread exhausted (why-never-escalated answered, rewrite-risk answered with a live case, every layer dated). Context budget still had room, so the ride continued into the next thread and found a live incident; that thread hands off below at the operator gate.

## FINDINGS

### 1. Q-001 is closed, and has been for 10 days. The pack was born stale.

- configs/mates.yaml:59 and the pack say "waiting since August, needs-operator". Disk truth: queue/queue_index.jsonl line 1 shows Q-001 closed_ts 2026-09-30T09:28:35Z by queue-sweeper-Z9, close_receipt watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md, verdict STALE-superseded.
- The funded elder consult (mtime 2026-09-29 18:52:32): verdict "(b) Park it", 4 named re-raise conditions, paid run z-ai/glm-5.3-prime, cost 0.02115576 USD, 2,654 tokens. Its numbers: the fold targets a 5.8MB chain inside a 68GB tree (0.0085 percent of estate mass); the hot-restore path had never fired in production.
- queue/todo.md:31 is flipped [x] with the PARKED annotation (todo mtime 2026-10-07 04:56:32). The gap register's R59 (watch/inbox/gap_analysis_20261010/GAP_REGISTER.md:297, mtime 2026-10-10 03:33:32) claims the box is still open and cites a Sep 29 mtime; that claim was already stale at write time. The register that polices staleness carried a stale line.
- Defect found in the close row: queue_index.jsonl Q-001 close_note cites "commit 4b77c3d01" for the operator DISSOLVES ruling. git cat-file -t 4b77c3d01 refuses ("Not a valid object name") and git log --all has no such hash. The real carrier of that ruling is commit 3ed507e0c (full sha 3ed507e0c4713df00252886a858960ec32d0009e, 2026-09-29, "SACRED-COW RULINGS": "The Q-001 operator-GO ask DISSOLVES into this ruling - no GO needed for a parked program"). The ledger of record carries a dangling commit citation; the ruling itself is real and byte-present.

### 2. Why Q-001 never escalated (the dated causal chain)

- 2026-08-04: founding commit eb07ad62e ("Mag sovereign agent - clean publish baseline") already ships mag/verkle_knot.py. The August stratum the pack senses is real: the chain machinery is as old as the repo's publish baseline.
- 2026-08-05: mag/verkle_audit.py born (commit 4e7350700). 2026-08-25: mag/chain_guard.py born with the canary law corrected the same day (b7a47f194, b349f6cde).
- 2026-09-25 19:15Z: Q-001 enters queue_index from todo. 2026-09-26 00:03Z: the queue roamer writes the verdict "needs-operator: task is real but it rewrites the verkle/Merkle chain (leaf merge plus chain recompute is deletion on the integrity substrate); operator must gate."
- THE ESCALATION GAP: that verdict gated execution but paged nobody. It was pull-channel text in a ledger. The operator-facing todo box kept reading as 0-dollar janitor work with no gate flag. Nothing broke (the chain kept verifying, disk stayed cheap), so no alarm ever carried the question upstairs. The operator met it only when the 09-29 sacred-cow summons asked "why are we compacting?" directly, and by then the honest answer was park.
- 2026-09-27 01:10 EDT: verkle99 landing commit e73b60c54 (plan-only module, 9 tests green, no CLI flag, execute double-gated). 2026-09-28 12:44 EDT: the burn_reset lane banks plan-only (fold candidates 247, kept live-knot 790, over 8,212 rows; "99" is the card name verkle99, not a leaf count) and records the ruling that a workflow dispatch is NOT operator GO (commit 390814497). 2026-09-29: park verdict. 2026-09-30 09:28Z: closed.
- The verkle99 double gate protected the chain FROM the compaction lane. It did nothing to protect the chain from any other code path. That distinction is finding 3.

### 3. The chain-rewrite risk is no longer hypothetical: the live spine was rewritten anyway, by a pytest fixture. Byte-proven.

- The live chain memory/biography/verkle_chain.jsonl (3,415 rows, 2,506,261 bytes, last write 2026-10-09 23:52:35 EDT) begins with three synthetic rows: session ids s0, s1, s2, filenames f0.knot.json, f1.knot.json, f2.knot.json, ts 2026-10-07T12:00Z, 12:01Z, 12:02Z.
- Byte identity proven with the chain's own legacy hash law: row 0 leaf_hash equals sha256 of the string "fixture-leaf-0"; row 0 verkle_root equals the legacy single-leaf root; row 2 verkle_root equals the legacy Merkle root over the three fixture leaves. These are the exact output of _hand_chain([A, B, C]) in tests/test_merkle_cure_p4b_sized.py:108-122.
- The mechanism: test_cross_arm_composition_leaf_domain_untouched (that file, line 200 as committed) called _hand_chain([A, B, C]) WITHOUT taking the estate fixture, so vk.CHAIN and vk.TIP stayed the live memory/biography/ paths. Any pytest run executing that test overwrote the live provenance chain with 3 fixture rows and the live tip with the fixture tip. The module docstring claims "the LIVE chain is never touched"; that claim was false for exactly one test.
- Dating the clobber window: last good observation of the old chain is the mesh index snapshot memory/mesh/index_history/index_2026-10-07T133532.844367Z (chain size 8,266,556 bytes, sha256 bd948c4a...). The clobbering test landed in commit 6685db6bc (2026-10-08 02:11:43 EDT, "PORT WAVE 20261007 LANDED", P-lanes). First evidence of repopulation: real rows appended 2026-10-10T02:52Z to 03:52Z (2026-10-09 22:52 to 23:52 EDT), 3,412 real rows walking old knot files (2026-08-03 forward) plus fresh autonomous-janitor knots, over the 3-row fixture head. Exact pytest run that fired the test: UNATTRIBUTED (no log names it; see JOURNEY dead end 5).
- Losses measured live today by mag.chain_guard check (read-only): state REGRESSION, rows 3,415, dangling 9, evidence_lost 0 (expected_evidence_lost 620, flag_drift 620: every evidence_lost flag is gone), tip_root 2b1da0ea vs chain tail root ae71aee2 (tip_matches_chain FALSE), guard marker stale at 2026-09-26T16:39:15Z. The pre-clobber chain carried 8,839 rows on 2026-10-02 (memory/attention.md:280, the healed tip incident that day) and 8,266,556 bytes on 2026-10-07. Roughly 5,400 rows of chain history are absent from the live file; the knot files themselves survive, so row content for present knots is re-derivable (the 10-09 backfill proves it), but the chain's own amendment and evidence_lost history is gone from the live path.
- No operator order sanctions a re-seed: memory/zknot/LATEST.md (his prompts across the window) carries no chain-rebuild instruction. No receipt in watch/inbox documents the clobber. This receipt is the first record of it.
- RECOVERY EXISTS: memory/biography/verkle_chain.jsonl.bak-orphanlane-20261003T221639Z (7,975,804 bytes) holds 11,201 real rows spanning 2026-08-12T16:41:39Z to 2026-10-03T22:13:25Z, written before the clobber instrument existed. 28 chain backups and 5 tip backups survive in memory/biography/. Rows after 10-03 22:13Z are recoverable only from knot files plus the mesh index hashes.
- The QUESTION_GAME_THEORY.md archaeologist (2026-09-30 17:10) called the chain "a well-kept diary" and asked "who witnesses the rebind". Answer now on the record: nobody did; the rebind was a test fixture at 12:00Z, and the only external witnesses (mesh index shas, the gist-witness law in attention.md) were pull-channel too.

### 4. Stabilization executed this sitting (one-file fix, no chain writes)

- tests/test_merkle_cure_p4b_sized.py: the non-hermetic test now takes the estate fixture, with a fix comment naming the cause and citing this receipt. Verification: pytest tests/test_merkle_cure_p4b_sized.py gives 33 passed in 5.35s, and the live chain sha256 is byte-identical before and after the run (EB07097CBE05B348DEE736451F32D2F4488F6773E5F453D46758453CFD6D91FA, mtime unchanged). The next pytest run can no longer clobber the spine. Not committed (no commit order; the diff sits in the working tree for the operator or the next lane).

### 5. Handoff thread for the next cycle (self-chosen, operator-gated: chain mutations)

1. Recover: under the estate verkle lock and explicit operator GO (Q-001-class gate), restore the live chain from the 10-03 backup, then re-derive 10-03 to 10-07 rows from knot files (the mesh index shas referee them).
2. Heal the tip with the module verb, not the main.py route: .venv/Scripts/python.exe -m mag.verkle_audit --fix (repair_tip_if_consistent), the same cure that worked on 2026-10-02 (attention.md:280; the main.py verkle-audit --fix routing defect noted there still stands).
3. Re-mark the guard marker after the restore, and re-file the evidence_lost classifications for restored rows (the side ledger memory/verkle/repair_20260930.jsonl, 251,781 bytes, holds the 300-row recoverable_by_hash classification).
4. Tripwire build: a cheap pytest-hermeticity patrol that fails any test file calling vk.CHAIN/vk.TIP writers without an estate fixture, wired beside the census patrol; and a receipt for the p4b lane (it landed a module and tests with no watch/inbox receipt at all).
5. Erratum: correct queue_index Q-001 close_note's dangling 4b77c3d01 citation to 3ed507e0c4713df00252886a858960ec32d0009e, and annotate GAP_REGISTER R59 as already-filled (todo.md flipped 10-07).

## JOURNEY

Threads followed, in order, with the turn reasons:

1. Read the pack; filed the start marker receipt. Turn: contract first.
2. Grepped 99-leaf / 99 leaf repo-wide: 5 matches, 3 distinct sources (mates.yaml:59 the pack text itself, GAP_REGISTER R59, the QUESTION_GAME_THEORY archaeologist voice). Turn: R59 contradicted the pack (closed vs waiting), so the contradiction became the road.
3. Read R59, todo.md, queue_index Q-001/Q-010/Q-028 rows. Found Q-001 closed 09-30 with the consult receipt. Turn: follow the closure evidence to its funded source.
4. Read ELDER_CONSULT_COMPACTION_20260929.md and burn_reset Q-001.md in full: park verdict, 4 re-raise conditions, plan-only numbers 247/790 over 8,212 rows, the double gate, the pre-staged-file disclosure (commit 390814497 carried a sibling's stealth_driver.py change; disclosed, not rewritten). Turn: now date the layers below the closure.
5. Git archaeology: earliest commits (eb07ad62e 2026-08-04 baseline), first verkle_knot/verkle_audit/chain_guard appearances, first compaction commit mentions (22907f3c8 2026-09-19 is trajectory compaction_eval, distinct; the verkle compaction program's commits start 09-27). todo.md proved UNTRACKED (git ls-files empty), so the box's birth is undatable from git; the seed thread's "since August" stays plausible but unproven. Recorded honestly as unproven.
6. Searched for commit 4b77c3d01 cited by the close note: git cat-file refuses, git log --all empty. Found the real ruling in 3ed507e0c by message search. Turn: a dangling citation in a ledger of record is exactly my hunting ground.
7. Checked chain liveness for the "current stratum": read memory/biography/verkle_chain.jsonl head. STRATUM RUPTURE: 3,415 rows, 2.5MB, genesis ts 2026-10-07T12:00Z with session s0. The 09-28 plan measured 8,212 rows. Turn: date the rupture.
8. DEAD END (instrument, not road): whole-repo recursive Get-ChildItem for verkle_chain files timed out at 120s (68GB tree). Replaced with targeted directory reads. Lesson: never walk the whole estate for a named file.
9. DEAD END: mesh index_history "f0.knot.json" hits were substring artifacts (knot filenames ending in hex f0). Verified by context read; released.
10. DEAD END: lattice-backfill ("Rebuild instrument verkle chain") writes a DIFFERENT chain (memory/improve/blast/lattice, its own law: never memory/biography). worldline_compact touches SEED.json only. verkle_restore_prep moves knot bytes only, never the chain. None of these was the rebuilder.
11. Found the fixture: tests/test_merkle_cure_p4b_sized.py _hand_chain writes exactly ts 2026-10-07T12:0{i}Z / f{i}.knot.json / s{i}, and the live chain head matches it shape-for-shape. Read the file: one test calls it without the estate fixture. Turn: prove byte identity, not shape identity.
12. Byte proof executed with the repo venv: row 0 leaf_hash equals sha256("fixture-leaf-0") True; row 0 verkle_root equals legacy single-leaf root True; row 2 verkle_root equals legacy [A,B,C] root True. Also checked mesh snapshots for dating: 4 snapshots, last good 2026-10-07T13:35:32Z at 8,266,556 bytes (sha bd948c4a). Commit 6685db6bc (10-08 02:11 EDT) landed the test. Window closed; firing run unattributed.
13. Checked for rival explanations: zknot LATEST (no operator re-seed order), REDBOARD/CURRENT (predate), attention.md (prior 10-02 tip incident, healed; gist-witness law), recovery surface: the 10-03 orphanlane backup read in place, 11,201 real rows, pre-clobber. Ran mag.chain_guard check (read-only): REGRESSION, flag_drift 620, tip mismatch, marker stale 09-26. Turn: with the incident proven, close the standing hazard (the test stays in the tree and fires again on any pytest run).
14. Stabilized: added the estate fixture parameter to the one non-hermetic test with a cause-carrying comment, ran the file (33 passed), proved the live chain sha256 unchanged across the run. No commits made.
15. Wrote this receipt, then spoke.

## COUNTS

- Receipts already in watch/inbox/mates_leave_protocol/receipts/ before this file: 15. This file replaces my start marker (1 write, then this overwrite: 2 writes total by me).
- 99-leaf grep: 5 matches in 5 lines, 3 distinct sources.
- Commits dated as evidence: 9 (eb07ad62e, 4e7350700, b7a47f194, b349f6cde, e73b60c54, 390814497, 3ed507e0c, 6685db6bc, plus 22907f3c8 named as a distinct-program dead end). 1 citation checked and found dangling (4b77c3d01).
- Old chain observations: 8,839 rows (2026-10-02, attention.md), 8,266,556 bytes (2026-10-07T13:35Z mesh snapshot, sha bd948c4a), 8,212 rows (2026-09-28 Q-001 plan).
- Live chain now: 3,415 rows, 2,506,261 bytes, 3 fixture rows at head, 3,412 real rows appended 2026-10-10T02:52Z to 03:52Z, last knot filename 2026-10-10_0350_autonomous-janitor_autonomo_t91ade6c.knot.json.
- chain_guard today: rows 3,415; dangling 9; evidence_lost 0; expected_evidence_lost 620; flag_drift 620; tip_root 2b1da0ea vs chain_root ae71aee2 (mismatch); marker_at 2026-09-26T16:39:15Z; ok false.
- Backups present in memory/biography: 28 chain backups + 5 tip backups; newest chain backup 2026-10-03T22:16:39Z name (18:16:39 EDT), holding 11,201 rows, span 2026-08-12T16:41:39Z to 2026-10-03T22:13:25Z, 7,975,804 bytes.
- Consult economics: 0.02115576 USD, 2,654 tokens (271 prompt / 2,383 completion, 1,852 reasoning), first attempt died on max_tokens=4000, refired at 12000. Q-001 plan numbers: 247 fold candidates, 790 kept, 8,212 rows, 9 tests.
- Fix verification: 33 tests passed in 5.35s; live chain sha256 before and after identical (EB07097CBE05B348DEE736451F32D2F4488F6773E5F453D46758453CFD6D91FA); mtime unchanged (2026-10-09 23:52:35 EDT). 1 file edited (tests/test_merkle_cure_p4b_sized.py), 0 commits.
- Byte-proof checks run: 3 named, 3 True. Naive legacy-root recompute over all 3,415 current leaves did NOT match the tip (expected False match attempt, not a finding: my recompute instrument is the copied reference, not the live referee; the live referee is vk._verify_chain_consistent via warm boot, which read ok true while the guard reads the tip mismatch).
- Paid API calls this mission: 0. Environment variable dumps: 0. RAM-gate deferrals: 0 (all commands light).

## Resume-not-respawn

Thread state for the next cycle: seed thread CLOSED (findings 1 to 3); handoff thread OPEN at finding 5, blocked on operator GO for every chain-touching step (Q-001-class gate, verkle lock required). The working tree carries my 1-file hermeticity fix, uncommitted, verified. If resumed by id, start at finding 5 step 1 and re-read the 10-03 backup head before anything else (trust bytes, not this report).
