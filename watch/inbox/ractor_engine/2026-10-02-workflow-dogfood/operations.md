# OPERATIONS LENS - the standing fleet censused from its own ledgers (2026-10-03)

Run ractor_engine / 2026-10-02-workflow-dogfood, lens operations. Written
2026-10-03 ~23:00-23:59 EDT. Every claim below is a byte I read or a command I
ran this sitting; anything I could not verify is marked OWED, never asserted.
No em-dashes. Moment law applies: every count is a snapshot of one tree at one
moment, and the tree is moving UNDER this census (a live fleet exercise was in
flight while I counted, see F4).

## Instruments run this sitting

- ListSavedWorkflows (tool): returns 19 saved workflows, scope project. The
  ask's census says 12. Disk agrees with the tool: `ls .zcode/workflows/*.dwf.ts`
  = 19 files. The 7 the ask missed: game-dig-coop-social, game-dig-creature-farming,
  game-dig-horror-maze, game-dig-liveops-seasonal, game-dig-roguelike-runs,
  game-mechanics-deep-dig, music-cut.
- `memory/workflows/REGISTRY.jsonl`: 63 rows (wc -l), full timeline dumped with
  `.venv/Scripts/python.exe` (ts, verdict, script, digest per row). Span
  2026-09-25T18:52Z to 2026-10-03T21:56:30Z. 52 PASS / 11 FAIL.
- `.zcode/workflow-runs/`: 103 files (101 dwfrun-*.mjs, 2 dwfeval-*.mjs), each
  the runtime materialization of one fire ("Generated ... before every launch;
  safe to delete once the run has settled", file header line 2). Classified by
  conjunctive string markers, then corrected by READING payload heads of the
  disputed files (my markers misfired twice before the reads; both
  misclassifications named below).
- Receipt tree: `watch/inbox/` family folders, `watch/inbox/gala_20260925/`
  rung archive (dir listing with full-iso mtimes), `memory/runs/mickey17_v2/runs/`
  (4 run dirs, mtimes read).
- `diff .zcode/workflows/game-dig-coop-social.dwf.ts .zcode/workflows/game-dig-horror-maze.dwf.ts`
  = 35 diff lines (descriptions, briefs path, vein constant, comments; nothing else).
- Prior ractions read: watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md
  (whole) and 2026-10-01-dogfood-gaps/SYNTHESIS.md (head).
- NOT RUN: ListWorkflowRuns (tool answered "workflow_introspection_unavailable:
  this session cannot read workflow runs", so no verdicts or completion states
  for any fire, this run or any other); schtasks query returned nothing useful
  for an olm driver; I did not read the harness source that wires saved fires
  to the gate (OWED, F1).

## The fire table (floors, not exacts; receipt + materialization evidence)

| workflow | fires | first | last | evidence |
|---|---|---|---|---|
| olm-mine | 9+ materializations, 5 receipt slugs | 09-29 | 10-03 19:30 EDT | frontier_olm_20260928/-0930/-1001/-1002/-1003 folders; dwfrun 3cec1e3a ("Daily-burn shape (2026-09-30)" comment in payload head) |
| ractor-engine | 7+ materializations | 10-01 | 10-03 (tonight, x2, one is this run) | ractor_engine/ dated folders x4 + ractor-topic; dwfrun ab6970fe, ed1dbbae (LENS_LIBRARY payload, my own operations persona read in it) |
| the-gala | ~20 rungs | 09-25 | 10-03 | gala_20260925/ rungs: gala-rung0, w1, w2, w3, ball-20260929, ball3-suite-green, ball4-luncheon-follow, build-it-all, dd-selfsteal, evidence, hitler-dig, ouroboros, 48h-synthesis, wave5-repair, afterparty, rung; today's writes: hitler-dig 07:46, dd-selfsteal 14:41, rung 16:20 (receipt 18:19), build-it-all 17:28 EDT |
| mickey17-v2 | 4 run dirs + 3-4 probe materializations tonight | 09-25 | 10-03 | memory/runs/mickey17_v2/runs/: agent-engineering-frontier-sweep-40 (09-25), gauntlet_w4 (09-26), gap-analysis-of-the-estate-s-09--15 (10-01 19:37), run-0 (10-03 21:05); tonight's dwfrun 9bafb3d8, 125a2278, 53ba7956 read as mickey17 payload (WSOUT .zcode/workspace/default/mickey17_v2, fold_run.sh) |
| the-50 | 1 saved-shape fire | 09-25 | 09-25 | THE50_RELAUNCH_VERDICT_20260925.md:3 "Relaunch run: dwfrun-4c7ad095 (the-50.dwf.ts fired with completed=[])"; 44/44 verdict; W1-W10 files are the pre-save 09-19-era program (one dwfrun 09-19) |
| tree-doctrine-dig | 1 | 09-25 | 09-25 | one dwfrun 09-25 14:59; TREE_DOCTRINE_V2_DIGEST_20260925.md |
| gap-analysis | 1 | 10-01 18:00 EDT | 10-01 | gap_analysis_20261001/ (sole file GAP_REGISTER.md, mtime 18:41:58 per the prior synthesis); tonight's gate row 10-03T21:17:54Z has NO materialization or rung behind it |
| fill-ball | 1 | 10-01 | 10-01 | watch/inbox/fillball/ 7 receipts; gala rung fillball-1001 + receipt; dwfrun 99126b18 10-01 23:51 |
| drop-dig | 1 | 10-01 | 10-01 | watch/inbox/localfirst/ 7 files; rung localfirst-steal + receipt |
| wide-dig | 1 | 10-01 | 10-01 | watch/inbox/spiking_wide/ 7 files; SPIKINGBRAIN_DROP_20261001.md; rung spiking-wide + receipt |
| salon-mine | 1 | 10-01 | 10-01 | watch/inbox/salon_mine/ m01-m19 + RESEARCH_BRIEF.md; rung salon-mine. The salon-vault-stragglers rung (10-02) is a gala-shape ball (divisions B/A per its receipt), NOT a salon-mine fire |
| librarian-expedition | 1 | 10-01 | 10-01 | watch/inbox/librarian_exp/ 14 files; rung librarian-expedition + receipt |
| music-cut | 0 | never | never | zero dwfrun match music_cut_gate; zero receipts; only a gate row 10-03T21:56:30Z. Its CUT_SEED_SAVER/CUT_THE_HUM/STYLE_SPEC provenance lives in watch/inbox/music/ and came from the music-ractor + vonnegut-final gala rungs (other workflows, pre-save) |
| game-dig veins (x5) | 19 fires, all 09-26/27 | 09-26 | 09-27 | dwfrun cluster 09-26 18:22 to 09-27 01:36 |
| game-mechanics-deep-dig | 10 fires, all 09-26 | 09-26 | 09-26 | the briefs_path payload cluster (5x 18:24, 5x 18:28) |

## F1: The fleet's fire history lives in three ledgers and none of them can answer "when did fill-ball last run"

The gate law (AGENTS.md: "no ungated CreateWorkflow", "Every check registers a
row in memory/workflows/REGISTRY.jsonl") keeps a ledger that is blind to the
saved fleet's actual fires. Registry facts run this sitting: 63 rows total, and
ZERO rows under the saved paths for fill-ball, salon-mine, librarian-expedition,
drop-dig, wide-dig, or olm-mine, all six of which have receipts proving at
least one fire. The last registry row for any olm script is 2026-09-30T01:18Z
(.zcode/workflow-drafts/frontier-olm-mine.dwf.ts, digest 2487787e949f), while
olm-mine materialized fires on 10-01, 10-02, and 10-03 (dwfrun 22ad421a,
bc564831, 1759540b, 3cec1e3a). Rows that do exist cluster on workflow-drafts
paths, 3 Temp\seatlaw_*.dwf.ts materializations (09-29 only), and manual
checks; the register appends only when someone runs tools/workflow_gate.py
check (REGISTRY path at tools/workflow_gate.py:42, append at :323-324,
--skip-registry at :280-282). The second ledger, .zcode/workflow-runs/, has
per-fire materializations but no verdicts and carries a "safe to delete" header,
so it is a cache, not a ledger (the relaunch's own dwfrun-4c7ad095 is cited in
THE50_RELAUNCH_VERDICT_20260925.md:3 and is already absent from the journal).
The third, the gala_20260925/ rung archive, exists only for gala-shaped
workflows because their scripts hardcode that root. Net: the estate's most
law-adjacent machine (the gate) cannot audit the cadence of the fleet it gates.
CONVERGENT: the prior raction's verdict "the register converts but cannot
record" (watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/SYNTHESIS.md:1-9,
thesis section) is the same disease one layer up, re-derived here from three
different instruments, so it outranks novel findings by the duplication law.
Falsifier: registry rows for the six saved paths, or any registration wire
inside the saved-fire path of the harness, produced as bytes. OWED: I did not
read the harness's saved-fire source to prove where the registration SHOULD
happen. Move (~30 min): give workflow_gate.py a --saved <name> mode that
resolves .zcode/workflows/<name>.dwf.ts and registers the row, and wire it (or
a wrapper) into the fire path, so the fleet's cadence becomes auditable from
one ledger with verdicts.

## F2: Seven of the twelve named workflows are single-fire wonders, and the self-repair loop they exist for has closed exactly once

Fired exactly once ever: gap-analysis (10-01 18:00 EDT), fill-ball (10-01),
drop-dig (10-01), wide-dig (10-01), salon-mine (10-01), librarian-expedition
(10-01), tree-doctrine-dig (09-25), plus the-50's saved relaunch (09-25,
44/44). The 10-01 mega-day ran the full loop the cards advertise (olm intake ->
gap-analysis -> fill-ball -> librarian-expedition, with salon/drop/wide riding
the same day), and in the 48h since, none of them fired again, while
gap-analysis's own card says "Run weekly or per-burst" (saved workflow
description, ListSavedWorkflows output). The receipt tree is the falsifier
instrument: watch/inbox holds exactly one gap_analysis_* folder, one fillball
folder, one localfirst folder, one spiking_wide folder, one salon_mine folder,
one librarian_exp folder. Sharpest wrinkle: tonight's session gate-checked the
saved gap-analysis (registry row 10-03T21:17:54Z, digest 545091f90a92) and did
not fire it, and 10-01's own "gap analysis" need was ALSO routed to
mickey17-v2 (run dir gap-analysis-of-the-estate-s-09--15, mtime 10-01 19:37
EDT, one hour after gap-analysis itself ran). The purpose-built engine exists,
the estate routes around it. Falsifier: a second dated receipt folder or rung
for any cohort member produced after 10-01. Move (~40 min total): fire
gap-analysis on the 10-03 process-improve wave receipts (the burst its own
card names as the trigger) and feed its register straight into fill-ball,
which closes "fired once" on the loop's both halves with real work; or, if the
operator prefers cadence over one-offs, register the pair as a weekly
scheduled fire so the loop stops depending on a seat remembering it.

## F3: The clone heap: 5 of 19 saved workflows are byte-clones of a 6th that is already parameterized, and one saved workflow has never fired at all

diff of game-dig-coop-social vs game-dig-horror-maze = 35 lines, all of them
description text, the GAMES_BRIEFS_<vein>.json path, the vein constant, and a
comment; the digger/triage/deep-dive/synthesis/cold-reader machine is
identical. game-mechanics-deep-dig.dwf.ts already takes briefs_path and
vein_slug as args (its 10 fires on 09-26 are exactly that generic shape, read
from payload heads: `__host.args.briefs_path`), so the five vein saves are
pre-bound copies of a workflow the fleet already has; the family produced 29
fires, every one of them in the 09-26/27 window, zero since. music-cut is
worse than idle: it is saved, its card claims provenance ("the Seed Saver
direction that proved out 2026-10-02"), and its gate row passed tonight
(10-03T21:56:30Z), but it has zero run materializations and zero receipts;
every artifact it claims (CUT_SEED_SAVER, CUT_THE_HUM, STYLE_SPEC in
watch/inbox/music/) was produced by the music-ractor and vonnegut-final gala
rungs before the workflow existed. That is the theater species on this fleet:
a card wearing another machine's receipts. Also a census defect in the ask
itself: 12 named vs 19 on disk, so any "minimum viable fleet" computed off the
ask's list would silently carry 7 phantom absences. Falsifier: any dwfrun
matching music_cut_gate, any vein-family fire after 09-27, or a saved fleet
listing showing fewer than 19. Move (~25 min): delete the five vein clones
(keep deep-dig plus one briefs JSON per vein, which is what the veins
hardcode), and either fire music-cut once for real at width 1 or unsave it and
move its card's provenance line to the gala rungs that earned it.

## F4: The minimum viable fleet is four live engines plus one loop pair; tonight the fleet is dogfooding itself and the archive folder name already lies

Live cadence (multiple fires across multiple days, most recent tonight):
olm-mine (daily intake, 10-03 19:30 EDT), ractor-engine (standing audit, 10-01
through tonight; this run is one of tonight's fires), the-gala (the workhorse
battery, ~20 rungs 09-25 to 10-03, three new rungs today), mickey17-v2
(frontier-burn engine, 4 run dirs plus tonight's probes). Loop pair on a
period trigger: gap-analysis + fill-ball (F2). Finished one-programs kept for
replay: the-50, tree-doctrine-dig. Everything else: clones, never-fired, or
absorbed. The composition contract is real and byte-visible: fill-ball's card
declares gap-analysis's register as its lane table (saved description: "the
register this emits IS fill-ball's lane table"), and five different workflows
archive into one shared rung root. That root is hardcoded: the-gala's saved
script pins GALA_ROOT to watch/inbox/gala_20260925 (read in tonight's dwfrun
bf3b90d0 and 6176a7ae payloads), so 10-03 lanes (dd-selfsteal, build-it-all,
rung) file under a folder named for 09-25, alongside five other workflows'
rungs. The name is now false advertising on the estate's memory. Separately:
while I censused, the journal grew under me (gala, mickey17, ractor-engine,
olm materializations between 14:39 and 22:21 EDT tonight, plus gate rows for
gap-analysis and music-cut), which is either this dogfood mega-run probing the
fleet or a sibling session exercising it; I cannot attribute the firing seat
from any instrument I ran (OWED). Falsifier: sustained multi-fire evidence for
any workflow this census parks, or a rung folder showing per-slug archives
that contradict the hardcoded root. Move (~25 min): make the-gala's archive
root slug-derived (gala_<slug>/, which its own card text already promises) and
fold this census into the manifest as the fleet's fire table with today's
moment stamped, so the next raction differences against a fixed baseline
instead of re-deriving it.

## OWED (honest residue)

- Exact fire counts are floors: the journal is deletable cache and already
  misses cited runs (dwfrun-4c7ad095); earlier cleanups may have removed more.
- No fire's completion state was verifiable: ListWorkflowRuns is a capability
  gap in this session ("workflow_introspection_unavailable"), and the journal
  carries no verdicts. Tonight's fires are counted, not confirmed landed.
- The seat/cause behind tonight's 14:39-22:21 EDT materialization cluster and
  the two saved-path gate rows (gap-analysis, music-cut) is unattributed.
- Family attribution for the ~95 non-read journal files rests on conjunctive
  string markers (documented above); markers misfired twice before I switched
  to payload reads, so any single-family count carries that residual risk.
- The gala rungs w1, w2, w3 have no _RECEIPT.md files in the archive listing
  read this sitting; their fold state is unverified.

## ERRATA (hostile pass corrections, re-verified this sitting, 2026-10-04 ~02:40 EDT)

The hostile second pass verdicted F1 and F2 weakened. Re-ran every killed leg
against the bytes; both corrections CONFIRMED, chapters amended as follows.

1. F1's ZERO-saved-rows universal is DEAD. My census moment predates a
   retro-batch: registry is now 75 rows / 64 PASS / 11 FAIL; rows 64-75 minted
   2026-10-04T02:33:47Z to 02:34:06Z, all twelve named workflows' saved paths
   PASS in one 19-second batch. What survives, narrowed: the saved fleet's gate
   registration is retroactive batch minting, not per-fire (before 02:33Z the
   twelve saved paths had exactly 2 rows ever, gap-analysis 10-03T21:17:54Z and
   music-cut 10-03T21:56:30Z, while the journal shows fires 10-01/02/03); the
   row schema (tools/workflow_gate.py:314-321: ts, name, digest, script,
   verdict, checks) carries NO run id, so registry rows join to nothing; the
   journal is self-described deletable cache and already lost a cited run
   (dwfrun-4c7ad095, cited at THE50_RELAUNCH_VERDICT_20260925.md:5, not :3 as I
   first wrote; zero hits in .zcode/workflow-runs/); the suppression flag is
   --no-register (tools/workflow_gate.py:281, :312), not --skip-registry as I
   first wrote.

2. F2's "gap-analysis itself ran at 18:00 EDT (dwfrun dfaaf421)" is WITHDRAWN.
   Read dfaaf421 this sitting: mickey17_v2 x6, WSOUT x5, fold_run.sh, targets
   x6, and ZERO of the saved gap-analysis script's unique markers (a15-rollup,
   burn_claims_50wide_20261003.md, envelope_50w_20261003.md, severity x
   fill-ease). Sharper: commit 5d2263f10's own message (2026-10-01 20:46:30
   -0400) attributes the lane archive to "memory/runs/mickey17_v2/runs/
   gap-analysis-*/lanes", so the estate's own receipt says the GAP ANALYSIS
   100M ran on the mickey17-shaped engine. The saved gap-analysis card's
   "Proven 2026-10-01: 15/15 lanes, 75 rows" is provenance from another
   engine's run, the same defect class as music-cut. Across 103 journals, grep
   of the gap-unique markers hits only lane text inside mickey17-shaped fires
   (125a2278, 4bacae38, 53ba7956, dfaaf421, e3d51dd6); the saved script's head
   (auditor-shaped, distinct from the mickey17 WSOUT head) has no identified
   materialization. Arithmetic fix: EIGHT of the twelve named workflows have at
   most one fire on record (seven confirmed single-fire plus gap-analysis,
   receipt-only), not "seven" with eight names listed.
