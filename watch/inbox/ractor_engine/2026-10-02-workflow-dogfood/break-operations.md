# BREAK-OPERATIONS: hostile second pass over the workflow-fleet lens report

Run: watch/inbox/ractor_engine/2026-10-02-workflow-dogfood (dwfrun-ed1dbbae-7663-48df-9b9d-3397f570bf0b).
Moment of this pass: 2026-10-04T03:43:21Z (23:43 EDT 2026-10-03). No em-dashes. Every claim below is a
command run or file read THIS sitting, cited by path:line or command + output. Nothing else is asserted.

Instruments used: ./.venv/Scripts/python.exe census of memory/workflows/REGISTRY.jsonl; ls/stat/grep/diff
over .zcode/workflow-runs/, .zcode/workflows/, watch/inbox/, memory/runs/; Read of tools/workflow_gate.py,
watch/inbox/THE50_RELAUNCH_VERDICT_20260925.md, watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/SYNTHESIS.md;
the harness ListSavedWorkflows and ListWorkflowRuns tools. Note: the Bash tool on this seat is bash, not the
cmd.exe the environment block claims; the first cmd-style batch mangled (one stray read-only find over C:\,
output discarded, no writes). No subprocess was spawned, so the win32 CREATE_NO_WINDOW law never engaged.

## The moving-tree event that re-scopes everything

At this pass's moment REGISTRY.jsonl reads 75 rows, 64 PASS / 11 FAIL, ts 2026-09-25T18:52:02Z to
2026-10-04T02:34:06Z (census: python json load, Counter output VERDICTS {'FAIL': 11, 'PASS': 64}). The lens
read 63 rows, 52 PASS / 11 FAIL, max ts 2026-10-03T21:56:30Z. The delta is exactly 12 new rows (64-75), all
PASS, all stamped 2026-10-04T02:33:47Z-02:34:06Z, all under .zcode/workflows/ saved paths: olm-mine
70571fea3957, gap-analysis 545091f90a92, fill-ball 4c13f8f191c3, ractor-engine 90b1990da9ae, salon-mine
5af29243fff5, librarian-expedition a0bb274121c1, wide-dig f2832e3ba2b5, drop-dig 9cc96d051e33, the-gala
2285b0104993, mickey17-v2 5ad12f1aae09, the-50 84cecee2c6d3, tree-doctrine-dig d2a6783b55be. Reconciliation
is byte-exact: 52 PASS + 12 = 64, 11 FAIL unchanged, 63 + 12 = 75, and git confirms append-only growth
(git show HEAD:memory/workflows/REGISTRY.jsonl = 58 rows; git diff --stat = +17 lines). The lens did not
fabricate; the registry moved under it five hours later. This is the B2-246 census law (a count is a
snapshot of one tree at one moment) biting a fleet-census lens.

## Verdicts

### Finding 1 (three unreconciled ledgers; ZERO saved-path rows for six fired workflows): WEAKENED

Byte-confirmed: REGISTRY const at tools/workflow_gate.py:42; append at :323-325 (os.makedirs :323, open+write
:324-325); the no-register flag exists but is named --no-register at :281, NOT --skip-registry as cited
(cite defect, line range roughly right). Last pre-batch olm row byte-exact: line 40, 2026-09-30T01:18:10Z,
.zcode/workflow-drafts/frontier-olm-mine.dwf.ts, digest 2487787e949f. Olm fires confirmed by journal mtimes:
dwfrun-22ad421a 10-01 10:01:58 EDT, bc564831 10-02 10:04:11, 1759540b 10-03 10:01:57, 3cec1e3a 10-03
19:30:43 (a same-day double the lens did not name), matching frontier_olm_2026-10-01/-10-02/-10-03 folders.
dwfrun-4c7ad095 absent: ls | grep -c "4c7ad095" = 0, and the journal header itself says "safe to delete once
the run has settled" (dwfrun-dfaaf421 head), supporting deletable-cache. THE50 verdict drift: the dwfrun is
cited at watch/inbox/THE50_RELAUNCH_VERDICT_20260925.md:5, not :3 as the lens wrote (line 3 is the verdict
headline). Convergence cite good: "the register converts but cannot record" is SYNTHESIS.md:1 verbatim.
Killed by the moving tree: the universal "ZERO rows ever under the saved paths" of the six died at
2026-10-04T02:33:47-02:34:06Z (rows 64-71 above). What survives: the 10-01/10-02/10-03 fires still had no
CONTEMPORANEOUS gate rows (the new rows are a batch re-check 5h after the lens; no materializations followed
them, see addition 7), and the ledgers remain unreconciled (a row schema of ts/name/digest/script/verdict
per workflow_gate.py:315-322 carries no link to any dwfrun id).

### Finding 2 (seven single-fire wonders; loop closed once; ALSO routed to mickey17): WEAKENED, one leg killed

Byte-confirmed: exactly one each of gap_analysis_20261001/, fillball/, localfirst/, spiking_wide/,
salon_mine/, librarian_exp/ under watch/inbox (ls -d listing); gala rungs with 10-01 mtimes (fillball-1001
23:55, librarian-expedition 20:00, localfirst-steal 05:06, salon-mine 21:08, spiking-wide 14:15); fill-ball's
own fire journal dwfrun-99126b18 (mtime 10-01 23:51:44 EDT; markers GALA_ROOT x5, GAP_REGISTER x13, fillball
x8; the saved fill-ball slug law names watch/inbox/gala_<slug>/, which is why gala and fill-ball read as each
other); registry row 62 = 2026-10-03T21:17:54Z PASS gap-analysis 545091f90a92 exactly as cited; salon-vault
straggler receipt watch/inbox/gala_20260925/salon-vault-stragglers_RECEIPT.md:15 reads "| by_division | B: 6,
A: 1 |" verbatim. Killed leg: "gap-analysis itself ran at 18:00 EDT (dwfrun dfaaf421)". dfaaf421 contains
ZERO "gap-analysis" strings; its head defines WSOUT = C:/Users/foste/.zcode/workspace/default/mickey17_v2 and
FOLD_SH under it, with mickey17_v2_fold x3, fold_run x1, targets x6: it is the mickey17-v2
gap-analysis-topic run (launch 18:00:28 EDT, memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15
mtime 19:37:26 = one event's lanes landing, not two routings). Across all 103 journals on disk, "gap-analysis"
appears in exactly two files, and neither is the saved workflow: dwfrun-4bacae38 (10-02 08:19:33 EDT; head is
GALA_ROOT + LANES + fold_gate.sh + B/A/C division sort = a the-gala run whose lane text mentions gap-analysis
x8, fill-ball x3, olm x7) and dwfrun-ed1dbbae (this run; its topic names the twelve). Scoped claim: on the
103 journals on disk at this moment, the saved gap-analysis workflow has NO identified materialization; a
deleted journal cannot be excluded (the lens's own blind spot 3, demonstrated inside its own evidence).
Also wrong: the count says "Seven of the twelve" but the list names eight (6 on 10-01 + tree-doctrine-dig +
the-50). Survives: fill-ball single-fire with no re-fire in 48h; gate-checked-without-firing for gap-analysis
(row 62, no new folder, newest journal 22:21:44 EDT 10-03); tree-doctrine-dig 09-25 evidence (TREE_DOCTRINE_
V2_BRIEF/DIGEST_20260925.md files; note it also holds six saved-path gate rows on 09-26, rows 13/19/22-25,
same digest d2a6783b55be, so repeated gate-checks, not evidence of more fires).

### Finding 3 (the clone heap; truncated mid-list in the handed report): CONFIRMED on visible evidence

diff .zcode/workflows/game-dig-coop-social.dwf.ts game-dig-horror-maze.dwf.ts = exactly 35 diff lines; body
is description, when-to-use prose, briefs path (GAMES_BRIEFS_coop-social.json vs horror-maze.json), vein
constant, and the PATCHED 2026-09-27 comment. No logic lines differ. grep -l music_cut_gate
.zcode/workflow-runs/*.mjs = 0 files (scope: the 103 .mjs journals on disk now; registry row 63 shows
music-cut gate-checked 2026-10-03T21:56:30Z PASS c814e2ebfee7 with no journal ever, so music-cut joins the
gate-checked-never-fired class). ListSavedWorkflows (this seat's own call) = 19 saved, all twelve topic names
present, extras are game-dig-coop-social/-creature-farming/-horror-maze/-liveops-seasonal/-roguelike-runs,
game-mechanics-deep-dig, music-cut. Caveat: the finding statement itself is cut off mid-list in the report as
handed to me ("-liveops-"), so the verdict covers the visible claim and its three evidence cites only.

## Blind-spot re-checks

1. Introspection gap: CONFIRMED by independent reproduction. My ListWorkflowRuns call failed with the same
   string: "workflow_introspection_unavailable: this session cannot read workflow runs". The disk journal
   (103 files) is the only run record reachable from this seat.
2. Unattributed firing seat: PARTIALLY RESOLVED. dwfrun-ed1dbbae (journal mtime 10-03 22:21:43 EDT, inside
   the lens's 14:39-22:21 cluster) is THIS dogfood run: this session's exec path names
   sess_dwf-dwfrun-ed1dbbae-7663-48df-9b9d-3397f570bf0b. The 12-wide gate batch at 02:33-02:34Z is someone
   else: this session ran no workflow_gate. Salon-mine's own materialization: still receipt/rung-evidenced
   only (blind spot stands).
3. Marker misfires: CONFIRMED and now demonstrated in the lens's own evidence (dfaaf421, see finding 2), plus
   a structural cause the lens missed: fill-ball's slug law writes INTO watch/inbox/gala_<slug>/ by design,
   so gala-rooted files are not gala fires.
4. Other-cwd: fire-side unverifiable from this repo (OWED). Gate-side has bytes: rows 41-45, 55, 57-59, 62
   carry absolute C:/Users/... script paths (cross-cwd gate runs), the rest relative.
5. gala w1/w2/w3: CONFIRMED. Each contains only a lanes/ subdir; no w1/w2/w3_RECEIPT.md exists in
   watch/inbox/gala_20260925/ (full ls). Fold state unverified, as the lens said.

## Additions (what the lens missed)

1. The registry is a live append-only surface and any fleet census of it must stamp its moment: 58 (git HEAD)
   -> 63 (lens) -> 75 (this pass) rows in under two days, the last 12 minted 2026-10-04T02:33-02:34Z as the
   first-ever full saved-path census of all twelve topic workflows. The lens's proposed --saved mode is half
   overtaken: the gate already registers saved paths when handed them (--script takes any path). The real
   gap is the join key: rows carry digest but no dwfrun, journals carry dwfrun but no verdict.
2. The dfaaf421 misattribution and the zero-identified-fires status of saved gap-analysis (scoped to on-disk
   bytes), which rewrites the loop-closure story: the 10-01 register was produced inside a mickey17-v2-shaped
   event, so "gap-analysis -> fill-ball closed end-to-end" is currently evidenced for fill-ball only.
3. Refire-once is visible in journal byte-sizes and the lens never counted refires: dwfrun-c48601ef and
   -5b23d7bb are both 38,342 bytes at 10-01 18:54:56/18:57:52 EDT; dwfrun-7128afa9 and -1cd89983 both 36,552
   bytes at 21:07:29/21:09:07. Same-size near-simultaneous pairs are refires; any per-family fire count that
   treats each journal as a distinct mission overcounts.
4. Gate-checked-without-firing is now a 12-wide pattern, not a 1-wide anecdote: the 02:33Z batch minted rows
   for all twelve while zero materializations followed (family folders still singletons; newest journal
   22:21:44 EDT 10-03, checked after the batch at 03:43Z).
5. music-cut is a thirteenth workflow outside the ask's twelve, gate-row'd and never fired, saved with a
   calibrated gate (tools/music_cut_gate.py per its card). The minimum-viable-fleet question the ask poses
   cannot be answered from a 12-workflow denominator.
6. The lens's own run is nameable: tonight's cluster includes this pass (ed1dbbae), so "counted, not
   confirmed landed" applies to the lens's own synthesis too until its receipt is on disk.

Falsifiers for the additions: a restored or other-project gap-analysis journal, or a gap_analysis_ folder
newer than 20261001, restores the lens's loop story; a materialization folder dated after 02:34Z 10-04 kills
addition 4; a registry row carrying a dwfrun field kills addition 1's join-key gap.

## OWED (not verified, never asserted)

- Whether the saved gap-analysis workflow EVER fired (journals are deletable cache; other project dirs were
  not scanned).
- Who minted the 02:33-02:34Z 12-row batch and from which seat/cwd (rows are anonymous; name field is the
  script basename).
- Completion/verdict state of any fire: ListWorkflowRuns is a hard capability gap in this session type
  (reproduced), and the journals carry payloads, not verdicts (dfaaf421 head inspected).
- The lens's findings after finding 3: the handed report truncates mid-evidence; anything past the clone-heap
  evidence block was not delivered to this pass and is not verdicted.
