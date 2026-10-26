# queue_truth.md - lane 7 (queue-truth) receipt, mickey17_v2 GO item 7

Filed 2026-10-04 by queue-truth-a14 (REFIRE; the first attempt died in a
provider burst). Master spec: corpus/steal/MASTER_MICKEY17_V2.md section 9
GO item 7. Evidence rows:
memory/runs/mickey17_v2/runs/run-0/lanes/a14-queue-truth.json (rows cited
below by idem hash; the wave brief's a14#N labels are shifted by one against
the JSON array, so idems are the canonical citation here).

## Finding on arrival (prior-attempt state)

The wave brief said the prior attempt "died before landing anything". Bytes
say otherwise for one file: `git diff queue/queue_index.jsonl` already held
the Q-005/Q-025 closes (closed_by queue-truth-a14, closed_ts
2026-10-04T08:30:26Z) before this sitting touched anything. Proof of health,
not partiality: 50 rows total, zero duplicate ids, both rows closed in place
(the ledger is one-row-per-id; appending duplicates would corrupt it, so the
in-place close is the correct shape and matches every other close in the
file). Command: `.venv/Scripts/python.exe` Counter over parsed rows. I
accepted the landed edit after verification and did not duplicate it.

## Sub-item 1 - Q-005/Q-025 closed rows in the queue index (idem 6e7a090b8cab5b4e)

DONE (landed by the prior sitting, verified this sitting). Both rows now
status closed with close_receipt pointing at the real receipts:
- watch/inbox/burn_reset_20260927/queue/Q-005.md (3,576 B, Sep 28)
- watch/inbox/burn_reset_20260927/queue/Q-025.md (6,830 B, Sep 28)
Q-025 close_note's five packet files byte-verified on disk under
watch/inbox/fifty_wide_20260917/ (FW27_publish_manifest.md, FW28_blind_hour.md,
FW29_cube_assembly.md, FW30_discord_runbook.md, FW31_sep20_demo.md, all five
present). Root cause named in both close_notes: the WO-12 flip sweep
(watch/inbox/wave5_repair/queue-closes.md) flipped the todo boxes but never
appended to the index (grep Q-005/Q-025 there = 0 hits), so the two surfaces
disagreed since 2026-09-29.

## Sub-item 2 - todo citation paths fixed (idem 6e7a090b8cab5b4e)

DONE. queue/todo.md line 98 (Q-005) and line 151 (Q-025). Both old paths
verified broken before the edit (`ls queue/Q-005.md queue/Q-025.md` = No such
file or directory for both) and both new paths verified present after.

- Q-005: old queue/Q-005.md (nonexistent) -> new
  watch/inbox/burn_reset_20260927/queue/Q-005.md (exists, 3,576 B). Both verified.
- Q-025: old queue/Q-025.md (nonexistent) -> new
  watch/inbox/burn_reset_20260927/queue/Q-025.md (exists, 6,830 B). Both verified.
Each fixed line carries the fix receipt inline (cause + evidence per the
fix-comment law). Out of scope, observed: sibling WO-12 lines (Q-003, Q-007,
Q-020, Q-021, Q-022, Q-023, Q-026, Q-027) still cite queue/Q-0xx.md paths;
the lane row named only the two Q-005/Q-025 paths, so the rest are left for
the owner of that sweep and are recorded here as a finding.

## Sub-item 3 - todo.md:31 flipped to parked (idem 22beb710e1c48c2d)

DONE. The open box "- [ ] Verkle noise compaction ... Recompute Merkle chain"
is now "- [x]" with: ">> PARKED per ELDER_CONSULT_COMPACTION_20260929.md,
verdict (b) Park it, 4 named re-raise conditions; do not execute (chain
mutation on the append-only provenance spine is forbidden until a re-raise
condition fires); Q-001 closed STALE-superseded 2026-09-30 (queue-truth-a14
mickey17_v2 GO item 7)". Evidence byte-checked before writing:
watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md exists (3,398 B, mtime
Sep 29 18:52) with "**Verdict: (b) Park it.**" at its line 11, and
queue/queue_index.jsonl Q-001 row reads closed 2026-09-30T09:28:35Z by
queue-sweeper-Z9 citing that consult. The todo box now instructs what the
park forbids no more.

## Sub-item 4 - NIGHT_CLOSE move 2 struck (idem 0dc2e4ead0721e82)

DONE. File identified from the lane row: watch/inbox/NIGHT_CLOSE_20261002.md
(the final report; watch/inbox/model_garden/NIGHT_CLOSE.md is the running
summary and was not the move-list carrier). "Morning first-three-moves"
item 2 now opens "STRUCK 2026-10-04 by queue-truth-a14 (mickey17_v2 GO item
7)" with the proof pointer (STOCHASTIC_LENSING.md section 6 "RESULTS
(lens-rz1, landed post-run)" + section 7 verdict + lens1_results.json ts
2026-10-02T05:49:57Z) and keeps the original order text below for the
record. Evidence byte-checked before striking: the results json exists
(13,505 B, internal ts "2026-10-02T05:49:57.674040Z"); section 6 title and
the C1 REFUTED verdict read directly from the file. Firing the ordered
repair would have re-run a landed analysis.

## Sub-item 5 - A16 verdict-fired addendum (idem 765d7cb3edbc6b7b)

DONE, append-only. Note: the wave brief's path watch/inbox/A16_LENS1_VERDICT.md
does not exist; the file lives at
watch/inbox/model_garden/archeology_w2/A16_LENS1_VERDICT.md (that is the
file amended; path corrected here). Appended "## ADDENDUM 2026-10-04: verdict
fired" citing lens1_results.json (13,505 B, ts 05:49:57Z) and STOCHASTIC_LENSING.md
secs 6-7, and closing the receipt's own "LANE COUNT: A-16 partial" line
(A-16 COMPLETE) without altering any original byte. The two surfaces no
longer contradict each other.

## Sub-item 6 - GAP_REGISTER ranks 2/3/4/6/7 annotated (idem 6d68833a810bae54)

DONE, annotations only (the register's own amend-not-rewrite law honored;
original claim text kept, FILLED marker appended in the gap cell). Every
receipt path and fill proof byte-checked before writing:

- rank 2 (elder-lens salvage): watch/inbox/fillball/elder-salvage.md;
  queue/lanes/elder/inbox.jsonl now 2,024 B (was the 0 bytes the rank cites).
- rank 3 (citation lint): watch/inbox/fillball/citation-lint.md;
  tools/citation_lint.py on disk 13,447 B.
- rank 4 (191.8M errata): watch/inbox/fillball/errata.md; the erratum at
  watch/inbox/48h_synth/ERRATA.md, 5,983 B.
- rank 6 (percolator intake): watch/inbox/fillball/percolator-candidates.md;
  --candidates flag live at mag/percolator.py:23.
- rank 7 (day-1 fold backfill): watch/inbox/fillball/day1-digest.md;
  DIGEST.md + register.jsonl + percolator_candidates.jsonl dir-listed under
  watch/inbox/frontier_olm_2026-09-30/.

## Files touched

- queue/queue_index.jsonl (verified prior sitting's landed edit; not re-edited)
- queue/todo.md (3 lines: :31 park flip, :98 and :151 citation fixes)
- watch/inbox/NIGHT_CLOSE_20261002.md (move 2 strike + pointer)
- watch/inbox/model_garden/archeology_w2/A16_LENS1_VERDICT.md (append-only addendum)
- watch/inbox/gap_analysis_20261001/GAP_REGISTER.md (5 rank annotations)
- watch/inbox/go_wave_20261004/queue_truth.md (this receipt)

Not touched: queue/STANDING_RAILS.md (lane 3 owns it; its 39/39
delta_judge_results.jsonl amendment read in place and left alone; the lane's
delta-judge row, idem 61ba6d4c1a45884f, is GO item 3 scope, not mine).

## Verification commands run

- git status --porcelain queue/ and git diff queue/queue_index.jsonl (prior-attempt state)
- ls on every receipt path cited (all 17 exist; sizes printed above)
- python Counter/dup check + JSONL parse over queue_index.jsonl (50 rows, no dups)
- grep -c per id in queue_index.jsonl (Q-005 = 1, Q-025 = 1)
- em/en-dash scan over all five edited files: lane-written lines carry zero
  (queue/todo.md's 59 pre-existing dashes untouched; the other four files
  scan 0 total)
- .venv/Scripts/python.exe -m mag.shared_surface validate: pass, warnings only
  (unindexed inbox files, GO item 5 scope, pre-existing)

## Blockers

None. One finding filed, not blocking: 8 sibling WO-12 todo lines still cite
queue/Q-0xx.md paths that do not exist (same rot class as sub-item 2, outside
this lane's named two-path scope). One brief correction filed above: the
prior attempt had landed the index edit before dying; the "died before
landing anything" premise was wrong for queue_index.jsonl.

Filed by queue-truth-a14, 2026-10-04. $0 metered. No em-dash bytes.
