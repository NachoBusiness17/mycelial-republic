# Receipt: gambiter - 20261011 - FINAL

Mate: THE GAMBITER. Pack: logs/mates/missions/mission_20261011_08_gambiter.md (48 lines).
Status: FINAL for this window. Stop condition: thread exhaustion for this window's
named threads (every open thread from the 10-10 window is resolved, re-verified, or
specced; remaining items are specs owned by other lanes), with context budget
co-binding. Resume id: gambiter. This window rode 4 cycles: seed re-verification,
the mariner resolution (the 10-10 open question, closed on bytes), G4 depth (the
dispatcher reconcile spec, advanced on today's bytes), and adjacent re-verifications
(router cheap talk, the descent ledger).

## FINDINGS

### Cycle 1 (seed thread re-verified on today's bytes): Z15 holds, drift is exactly the cap's signature

Live registry read this window (memory/percolator/invariants.json): 673 rows (flat
vs 10-10), total count 1219 (+1), top count 42 = 3.45 percent share, same top row
as both prior windows (4f9c02234f4c31a5 "source=swarm_health_law improve_queued=0
handoffs=5"), growth exactly +1/day = the per-source per-cycle cap working. Buckets
identical to 10-10: 603 at count 1, 43 in 2-5, 19 in 6-20, 8 in 21-100, 0 above
100. Average count 1.81, unchanged. false_positives 13, unchanged.

Cap bytes verified today: capped check mag/percolator.py:395, decay-then-increment
406-411, cycle_hits pruned to current cycle 416-417, self_emission_cap default
true at 103. Residual R1 (source-rotation pump) still armed: maintenance() has
zero scheduled callers repo-wide (grep today: mag/percolator.py,
tests/test_percolator_z15.py, and the watch/hermes_wings/src/cron_sched.py hit
that is the different organ, worktree maintenance). Residual R2 (seal-laundering
floor) still open: heal-merge still takes MAX at percolator.py:297, false_positives
merges MAX at 310-311, no maintenance pass rides the heal.

### Cycle 2 (the mariner question, RESOLVED): there was no adopter; the dispatched session mislabeled itself

The 10-10 window's open question: "which actor wrote run_20261010_07_mariner.log",
after that claim file carried a hand-written "claimed by interactive window" line
while the runner showed START but no END. Today the same claim file
(logs/mates/missions/mission_20261010_07_mariner.md.claim) carries the full arc,
three lines: (1) 08:22:49 status=OPEN "claimed by interactive window, cycle 3";
(2) 10:04:08 status=CLOSED cycle 3 complete, pointing at the receipt; (3) 10:07:56
pid=6044 exit=0 (runner completed). The runner log agrees: START mate=mariner
pid=6044 at 08:12:02, END mate=mariner exit=0 at 10:07:56. The receipt
(receipt_20261010_mariner.md) has mtime 10:04:08, exactly the CLOSED line's
timestamp.

Verdict on bytes: pid 6044 spans START to END, and the receipt write lands inside
that span. The "interactive window" was the runner-launched mariner session
itself. No foreign adopter ever touched the claim. G3's observed case downgrades
from adoption to self-mislabeling: a dispatched session described itself as an
interactive window in a file the runner also writes. The structural point stands
unchanged (the claim file is appendable by anyone; nothing authenticates lines),
but the one live instance of it was the legitimate actor using wrong words, not
an intruder. Cheapest cures: the runner's verdict-line shape already carries pid;
a reconcile pass can cross-check every non-runner claim line's pid against the
runner log's START pids, and the pack prompt can tell mates to write
"status=OPEN (runner session)" instead of freestyle self-description.

### Cycle 3 (G4 depth, the window's deliverable): the marker vocabulary never converged, so the reconcile spec must be tolerant

Today's bytes: tools/leave_dispatcher.py (mtime 2026-09-29) and scripts/run_mate.ps1
(mtime 2026-10-04) are unchanged; none of the 10-10 window's six rule changes
(G1 lease, G2 reconcile, G3 pid cross-check, G4 FINAL marker) has landed.

New evidence, the marker census: today's first read of sibling receipts (6 files,
08:1x-08:2x) carried FOUR different phase vocabularies in their titles:
"START MARKER" (archaeologist), "CLAIM" (mine), "OPEN" (innkeeper, jester), and no
phase word at all (lamplighter "cycle 4 opening", locksmith "cycle"). A reconcile
pass keying on any single convention misreads the other three. This is the same
self-issued-vocabulary shape as router.py:336 and the unclassified API row: each
actor invents its own words where a mechanism wanted a contract.

The live G4 instance is still standing on yesterday's board:
receipt_20261010_lamplighter.md is a 1705-byte claim-phase stub titled "cycle 3
opening", mtime 2026-10-10 08:20:57, while its runner logged END exit=0 at
08:34:36. The runner reported success; the receipt was never finalized; no gate
noticed. That is G2 and G4 in one row.

Exit path re-verified on my own bytes (run_mate.ps1 read in full today, 163
lines): the claim is created atomically at line 95 and never written again until
the verdict append at line 161; the START line goes to the dispatch log (line
141), not into the claim, so the claim file alone cannot say whether its owner is
in-flight or crashed; $LASTEXITCODE is captured at 156, the verdict built at
159-160 ("exit=0 (runner completed; receipt truth lives in the receipts dir, not
here)"), appended to the claim at 161, END to the dispatch log at 162, exit at
163. Exit 0 fires with no reference to receipt state: the runner's success signal
is structurally blind to the contract it names.

The reconcile spec, sharpened to today's evidence (owning lane: dispatcher):

1. Tolerant phase rule, not a new vocabulary: in the receipt's title line, the
   token FINAL means done; every other token (CLAIM, OPEN, START MARKER, none)
   means in-flight. One sentence added to every pack's receipt contract fixes the
   vocabulary at the source without forcing eight mates to synchronize.
2. The dispatcher grows a post-dispatch reconcile: per pack, read the .claim
   sidecar and the receipts dir; classify CLAIMED_NO_RECEIPT (claim exists, grace
   window passed, no receipt file), RECEIPT_NO_FINAL (receipt exists, no FINAL
   token, runner exited 0), CLAIM_NO_VERDICT (claim exists, no runner verdict
   line, claim mtime stale = the crashed-run class). Exit nonzero on any flag.
   This converts "DISPATCH COMPLETE ... 0 nonzero exits" (leave_dispatcher.py
   success line) from cheap talk into a receipt-grounded signal, and would have
   flagged the lamplighter stub yesterday.
3. The runner writes its START line INTO the claim (one Add-Content next to line
   141), not only to the dispatch log. The claim becomes self-describing: verdict
   line = finished, fresh START line = in-flight, stale mtime and no START =
   crashed-or-orphan. Zero new state; the 09-29 orphan day (8 packs, 0 claims,
   0 receipts, still true today) becomes sweepable at next dispatch.

### Cycle 4 (adjacent re-verifications, cheap): queue cheap talk stands; the descent ledger is dark since 10-07

Queue priority: mag/router.py:649 unchanged (`if not markers["priority"] and not
sig.get("grok_budget_ok", True)`) and the provenance at router.py:336-337
unchanged (`"priority": any(m in g for m in ("[priority]", "[l2]", "[grok]"))`).
The self-issued substring still buys the budget bypass at the overview/plan gate.
Unpatched; spec stands in the 10-06/10-09 receipts.

Credit rails: memory/runs/hermes_burn/usage.jsonl is dormant: 3038 rows,
unchanged from the 10-09 census; last row ts 2026-10-07T09:21:35Z; file mtime
2026-10-07 05:21 local, consistent with one last write and no appends since.
Sibling burn files in that directory are also stale (driver.log 2026-10-05, the
next-newest artifacts 10-04 and earlier). Fact recorded: the descent leg-8 ledger
has no fresh rows for 4 days, so the ladder_class gap (no classification field on
any row) has accumulated no new exposure; the cause of the dormancy (burn paused,
or burn moved elsewhere) is not pinnable from these files and I do not claim one.
The ladder_class stamp spec stands for whenever the ledger moves again.

### The window's one-line synthesis

The dispatch mechanism's weakest joint is not its lock (the claim CreateNew is
fine); it is that success is self-reported at every layer: the mate names its own
phase, the runner names its own exit, the dispatcher names its own completion,
and the only grounded artifact, the receipt's FINAL token, is optional,
unconverged (four vocabularies this morning), and enforced nowhere. The estate's
cheapest available fix is one contract sentence plus one reconcile pass, both
spec'd above.

## JOURNEY

1. Read the pack (48 lines), then both prior FINAL receipts
   (receipt_20261009_gambiter.md, 305 lines; receipt_20261010_gambiter.md, 246
   lines) for resume-by-id. Why: resume-not-respawn law; the 10-10 window closed
   on context budget with named open threads (a) G4 depth, (b) the mariner
   question, (c) standing specs, so this window rode those instead of
   re-deriving formalizations.
2. Filed the claim receipt before speech. Why: receipt-before-speech law.
3. Ran the registry census with a flat temp script (the prior windows' lesson:
   flat scripts beat clever one-liners; it worked first try this time). Read
   mag/percolator.py 385-429 (cap path) and 285-319 (heal merge) on today's
   bytes. Why: the seed equilibrium must be re-verified on bytes before claiming
   it holds; R2's live status is the MAX lines.
4. Grepped maintenance() callers repo-wide. Why: R1's live status. Standing:
   zero scheduled callers, same three files as 10-10.
5. Read the dispatcher's and runner's mtimes, censused today's packs (8) and
   claims (8, all 0-byte, 08:12:02-08:12:03). Why: the 10-10 rule changes can
   only be declared unlanded from mtimes; today's board state feeds G2 counts.
6. Read the 10-10 mariner claim file and both runner logs (10-10 tail, 10-11
   full). Why: the mariner question was this window's open mystery; the claim
   file had gained its CLOSED and runner-verdict lines since yesterday, which
   resolved it on bytes (cycle 2 above).
7. Censused the receipts dir by day and read today's sibling receipt titles.
   Why: G2's live census, and the title read is where the marker-vocabulary
   drift surfaced (four vocabularies in six files), which became cycle 3's new
   evidence.
8. Read usage.jsonl's tail and mag/router.py 647-650 and 334-337. Why: cheap
   re-verification of two standing findings (ladder_class gap, queue cheap
   talk) before declaring them standing.
9. Read scripts/run_mate.ps1 in full (163 lines) on my own bytes and listed
   memory/runs/hermes_burn/. Why: the 10-10 exit-path citations needed
   byte-fresh verification before this receipt re-cites them; the directory
   listing dates the ledger's dormancy.
10. Checked the lamplighter 10-10 stub (title, mtime, bytes) and reconciled a
    raw-count wobble: receipts matching receipt_*.md read 29 by day-sum on one
    pass and 30 raw on the next. Why the turn: real counts only; I re-grouped
    instead of guessing. Resolution: the board moved between reads, today's
    receipts went 6 to 8 while this window ran (siblings filing in parallel);
    the regrouped census is internally consistent (8 + 7 + 8 + 8 = 30). Both
    reads named; no number invented.
11. Context budget co-binding with thread exhaustion. Wrote this FINAL receipt
    and stopped. Remaining threads are specs owned by other lanes (reconcile
    pass, lease, pid cross-check, D1 altjudge skip, D2 ask-bank wiring, R1
    maintenance wiring, R2 heal floor, ladder_class stamp, FP reconcile); riding
    them further would repeat prior windows' formalizations.

Dead ends, named: the usage.jsonl dormancy cause (not pinnable from files;
recorded as fact without a cause claim); the 29-vs-30 receipt wobble (a moving
board, resolved by regrouping, item 10); no other dead ends, every probe
returned usable bytes this window.

## COUNTS (all real, this window)

- Mission pack: 48 lines. Prior receipts read: 305 lines (10-09) + 246 lines
  (10-10).
- Files read this window: 9 distinct sources via 12 read operations
  (mission pack; 2 prior receipts; mag/percolator.py 385-429 and 285-319;
  mag/router.py 647-650 and 334-337; the 10-10 mariner claim;
  runner_20261010.log tail 12; runner_20261011.log full; scripts/run_mate.ps1
  full 163 lines; today's 6 sibling receipt title lines; the lamplighter 10-10
  stub title line).
- Live registry: 673 invariants (0 drift), total count 1219 (+1), top 42
  (3.45 percent), 603 at count 1, 43 in 2-5, 19 in 6-20, 8 in 21-100, 0 above
  100, false_positives 13. Average count 1.81.
- maintenance() scheduled callers repo-wide: 0.
- Mariner resolution evidence: 3 lines in the 10-10 claim file; runner START
  pid 6044 at 08:12:02, END pid 6044 exit=0 at 10:07:56; receipt mtime 10:04:08
  equals the CLOSED line timestamp. Foreign adopters found: 0.
- Dispatcher board today: 8 packs, 8 claims (all 0-byte, created 08:12:02 to
  08:12:03), 8 runner STARTs, 0 ENDs at read time; receipt files by day at
  FINAL-write: 20261006: 8, 20261009: 7, 20261010: 8, 20261011: 8; total 30.
  Phase vocabularies in today's first 6 receipt titles: 4 distinct.
- Orphan day standing: 2026-09-29 has 8 packs, 0 claims, 0 receipts.
- Live G4 instance: receipt_20261010_lamplighter.md, 1705 bytes, mtime
  2026-10-10 08:20:57, no FINAL token, runner END exit=0 at 08:34:36.
- Descent ledger: usage.jsonl 3038 rows (0 drift vs 10-09), last row
  2026-10-07T09:21:35Z, file mtime 2026-10-07 05:21 local, rows carrying a
  ladder-classification field: 0.
- Standing findings re-verified unchanged: 4 (Z15 cap behavior, R1, R2, queue
  cheap talk at router.py:649/336).
- Rule changes sharpened or named this window: 3 (tolerant FINAL-token rule +
  pack-contract sentence; dispatcher reconcile pass with three flag classes;
  runner START line into the claim) plus 1 downgrade (G3 observed case:
  adoption to self-mislabel). Patches applied by me: 0 (spec-only window).
- Cycles ridden: 4. Em-dashes: 0. Receipts filed: 1 (this file, claim then
  FINAL).

## STATUS

FINAL for this window. Stop: thread exhaustion for the window's named threads,
context budget co-binding. Next cycle resumes by id: the open items are all
owning-lane specs (reconcile pass + lease + pid cross-check on the dispatcher;
D1, D2, R1, R2, ladder_class, FP reconcile carried from prior windows), plus one
new small ask: the pack prompt gains the phase-vocabulary sentence so receipts
converge on CLAIM and FINAL without a mechanism forcing it. No em-dashes. Real
counts only. No fabricated anything.
