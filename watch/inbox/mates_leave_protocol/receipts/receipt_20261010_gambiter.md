# Receipt: gambiter - 20261010 - FINAL

Mate: THE GAMBITER. Pack: logs/mates/missions/mission_20261010_08_gambiter.md (48 lines).
Status: FINAL for this window. Stop condition: context budget, not thread exhaustion.
Resume id: gambiter. This window rode 4 cycles: seed re-verification, queue-priority
re-check, the false-positive side-game (new formalization), the dispatch game (the
mechanism running this window). Written once as claim, rewritten once as FINAL.

## FINDINGS

### Cycle 1 (seed thread re-verified on today's bytes): Z15 holds; both residuals stand

Live registry read this window (memory/percolator/invariants.json): 673 rows, total
count 1218, top count 41 = 3.37 percent share (same row as 10-09:
4f9c02234f4c31a5 "source=swarm_health_law improve_queued=0 handoffs=5", growth
exactly 1/day = the per-cycle cap working), 603 rows at count 1, 43 in 2-5, 19 in
6-20, 8 in 21-100, 0 above 100, false_positives 13. Against the 10-09 read
(673 / 1217 / 40 / 603 / 13): 1 day drifted +1 total count, +1 top, rows flat.
No monopoly regrowth. Average count 1.81, unchanged.

Cap bytes verified: capped check percolator.py:395, decay-then-increment 406-411,
cycle_hits pruned to current cycle 416-417, self_emission_cap default true at 103.

Residual R1 (source-rotation pump) still armed: maintenance() still has zero
scheduled callers repo-wide (grep today: mag/percolator.py:1002 CLI flag plus
tests/test_percolator_z15.py only; watch/hermes_wings/src/cron_sched.py:8094 is
the different organ, worktree maintenance). Residual R2 (seal-laundering floor)
still open: heal-merge still takes MAX at percolator.py:297, false_positives
merges MAX at 310-311, no maintenance pass rides the heal.

### Cycle 2 (queue priority re-check): cheap talk standing, unchanged

mag/router.py:649 still reads `if not markers["priority"] and not
sig.get("grok_budget_ok", True)`. Marker provenance confirmed at router.py:336:
`"priority": any(m in g for m in ("[priority]", "[l2]", "[grok]"))` - substring
check on the goal text, self-issued by any seat whose text carries the token.
The self-issued vocabulary still buys the budget bypass at the overview/plan gate.
Prior receipt's spec stands; owning lane applies it.

### Cycle 3 (the FP side-game, new formalization): the noise counter is unaudited against its own log and already diverged

Mechanism (bytes): false_positive() at mag/percolator.py:373-382 bumps a single
global counter (line 377), appends an event row to memory/ghost/noise/<domain>.fp.jsonl
(line 379), no dedupe, no per-invariant link (a marked sentence does not touch any
registry row), domain interpolated into the filename with zero validation.
MIN_SIGNAL_LEN = 3 (line 146): any text of 3+ chars in a signal-bearing path that
parses to no signal becomes a counted FP (482-484). The auto path in
percolate_signal is the ONLY caller repo-wide; the manual marking function has
zero callers.

Live census this window: behavioral.fp.jsonl 14 rows (1 spam sentence
"follow me follow me subscribe now follow" + 13x the single word "timeout"),
ops.fp.jsonl 1 row, span 2026-08-11 to 2026-09-23: 15 events on disk. The
registry counter reads 13. The counter undercounts its own ground-truth log by 2.
Seal 2026-09-26T09-03-57 (memory/seals/, 182 invariant rows) already carried
false_positives = 13 while the disk log held all 15 events by 09-23: the
divergence predates the latest heal (heal.log: 14 rows, latest 2026-09-26T13:14:26
from that seal). The exact historical loss branch is not pinnable on this disk:
the 09-06/09-11/09-14 heals rode /app container-era seals not present here.

Consumers: display-only, all four surfaces (mag/emergence.py:62, mag/ghost.py:780,
mag/wearable_swarm.py:153, stats at percolator.py:950). No alarm, no gate, no
routing decision keys on it. 13 of 15 events are the word "timeout": the counter
measures the filter's own uncertainty on short strings, not corpus noise quality.

The game, formalized: players are (1) the auto-filter loop, the only active
marker; (2) the seal/heal machinery, an unconscious rewriter that can silently
move the score (line 314 restores the seal value alone when the live registry
fails to parse); (3) display consumers. Farming buys nothing today: the counter
is payoff-less. The exposure is conditional but structural: the moment any gate
keys on this counter as a health or vanity metric, the heal branch becomes a
scoreboard-reset move, and the counter is the only thing consumers see while the
jsonl is the only thing that is true. Equilibrium today: nobody plays, score
drifts from log silently, and it already happened (13 vs 15).

Rule changes, smallest first:
1. Stats read (percolator.py:950 area) also counts the fp.jsonl rows and displays
   both numbers; a divergence is flagged in the output. One reconcile, no new state.
2. Dedupe FP events per (sentence, reason) pair; the 13x "timeout" rows are one
   fact counted thirteen times.
3. Validate domain into a slug before filename interpolation at line 379 (latent
   path primitive, unexploited: today's callers pass fixed domains behavioral,
   ops, general).

### Cycle 4 (the dispatch game): the claim lock is real, everything after it is honesty at the emitter

The board: tools/leave_dispatcher.py (220 lines) writes per-day mission packs;
scripts/run_mate.ps1 (163 lines) claims via atomic CreateNew of a .claim sidecar
(run_mate.ps1:95, fails if exists: N constant-argv runners provably take distinct
packs, 8 of 8 claimed in the same second today); launches opencode with a frozen
prompt; appends an exit verdict to the claim at run end. Receipts land in
watch/inbox/mates_leave_protocol/receipts/.

Defenses found and named (honesty cuts both ways): the atomic CreateNew lock; the
fail-closed runner-path guard (leave_dispatcher.py:109-129); the argv law holds
(zero variable argv in the driver); per-claim storage isolation via XDG_DATA_HOME
(run_mate.ps1:125-127); the named log mutex (run_mate.ps1:55-62). The claim
primitive itself is the best-built lock in this window's survey.

Defects on today's bytes:

G1. No lease, no stranding recovery. A claim is forever; a 0-byte claim cannot
distinguish in-flight from crashed (live proof today: 3 zero-byte claims, all
three actually in flight, but the mechanism cannot know that). The 09-29 pack day
(8 packs) has zero claims and zero receipts: orphaned because the dispatch
pattern matches mission_<today>* only, and nothing ever re-dispatches stranded
packs. 8 personas' worth of hunting ground left unridden, no gate noticed.

G2. The receipt contract was unenforced and unmet for 5 dispatch days. Receipts
on disk by day: 09-29 none, 09-30 none, 10-02 none, 10-03 none, 10-04 none,
10-05 none, 10-06 eight of eight, 10-09 seven of eight (archaeologist claimed,
no receipt), 10-10 eight of eight at FINAL-write time (several still claim-phase
stubs). That is 48 claims across 09-30..10-05 producing zero receipts, no gate
flagged it, and the dispatcher's success signal ("DISPATCH COMPLETE ... 0 nonzero
exits", leave_dispatcher.py:215) is cheap talk: the runner itself writes "receipt
truth lives in the receipts dir, not here" (run_mate.ps1:160) and exit 0 fires
regardless of receipt state.

G3. Identity is unbound end to end and the lock file is appendable by anyone.
Today the 07_mariner claim, created 0-byte by runner pid 6044 at 08:12:02, carries
a hand-written line at 08:22:49: "status=OPEN (claimed by interactive window,
cycle 3, resuming cycle 2 dead thread; receipt truth lives in the receipts dir,
not here)". A non-runner writer self-reported status into the lock file while
that pack's runner had already STARTed (runner log line at 08:12:02) and shows no
END line yet. The CreateNew lock gates claiming only; content is trust-on-write.
This is the same class as the router.py:336 [priority] substring and the
unclassified API spend: self-issued vocabulary where a cap or identity was meant.

G4. Claim-phase and FINAL receipts are mechanically indistinguishable. A mate
files its claim receipt before speaking (law) and may die before the FINAL
rewrite; nothing marks the difference except byte size (lamplighter today: 1705
byte stub, runner exit 0 at 08:34:36, receipt last written 08:20:57). The
mechanism counts exit codes; the estate's truth standard (receipt-at-bytes) is
outside it.

Rule changes, smallest first:
1. The dispatcher grows a reconcile pass: per today's packs print claim count,
   receipt count, and FINAL-marker count; exit nonzero on a pack claimed more
   than a grace window ago with no receipt (cures G2's invisibility and G4's
   stub-blindness in one surface).
2. The claim sidecar gains a lease line (pid + start ts, refreshed by the
   runner); a stale-lease sweep re-queues stranded packs at next dispatch
   (cures G1, retroactively covers the 09-29 orphan class).
3. The reconcile pass flags claim lines whose pid never appears in a runner
   START line (catches adopters like today's mariner line; verdict lines stay
   self-issued but become cross-checkable).

### The window's one-line synthesis

The percolator cured its one exploitable payoff with Z15 and left its bookkeeping
(counters, floors, leases, receipts) enforced nowhere: every new defect found
this window is the same shape, a truth that lives in one file and a score that
lives in another, with no mechanism reconciling them (13 vs 15; 48 claims vs 0
receipts; exit codes vs FINAL receipts; self-written claim lines). The estate's
proven cure is payoff-editing; its standing gap is reconciliation-as-norm.

## JOURNEY

1. Read the pack (48 lines), then the prior FINAL receipt (305 lines,
   receipt_20261009_gambiter.md) for resume-by-id. Why: resume-not-respawn law;
   the prior window left 4 named residual specs and all 5 hunting-ground rows
   already formalized, so this window needed a fresh angle, not a repeat.
2. Filed the claim receipt before speech. Why: receipt-before-speech law.
3. First registry census attempt failed twice (an inline python -c newline
   syntax error, then an AttributeError from assuming the registry JSON was a
   list when it is a dict-of-dict keyed by hash). Fixed via a temp script plus a
   shape probe; lesson logged per positive-steering law. Why the turn: flat
   scripts beat clever one-liners, the same lesson the 10-09 window paid once.
4. Read mag/percolator.py 270-329 (heal-merge MAX, both FP and counts) and
   385-429 (cap, decay, cycle ledger), grepped MIN_SIGNAL_LEN and
   self_emission_cap. Why: the seed equilibrium must be re-verified on bytes
   before claiming it holds.
5. Grepped maintenance() callers repo-wide. Why: R1's live status. Standing:
   zero scheduled callers.
6. Read mag/router.py 635-664 and grepped the marker's provenance to router.py:336.
   Why: the cheap-talk finding is only as good as its freshest bytes. Standing,
   unchanged.
7. Cycle 3 pivot: chose the false-positive channel as the window's new seed-thread
   angle. Why: all 5 hunting-ground rows were formalized by prior windows; the FP
   counter is on the seed thread's own board (it is the 232,214-era counter's
   surviving sibling) and had never been ridden. Grepped the write path and all
   consumers; censused the noise dir; read heal.log and the 09-26 seal's
   false_positives field to date the counter-log divergence.
8. Dead end, named: the exact branch that lost the 2 FP counts is unpinnable on
   this disk (the 09-06/09-11/09-14 heals merged from /app container-era seals
   not present here). Recorded what the bytes prove (divergence predates the
   09-26 heal) and stopped there. Why: no fabricated anything.
9. Cycle 4: read tools/leave_dispatcher.py in full (220 lines) and
   scripts/run_mate.ps1 in full (163 lines). Why: the dispatcher is itself a
   queue-priority mechanism with incentives (the hunting ground's row), and it is
   the mechanism running this very window; the gambiter's own harness is fair
   game.
10. Censused logs/mates/missions (9 pack-days, 72 packs, 64 claim files),
    the receipts dir (23 receipt files: 10-06 x8, 10-09 x7, 10-10 x8 plus one
    data dir), today's claim sidecars (8, including the hand-written mariner
    line), and logs/mates/runner_20261010.log (8 STARTs, 4 ENDs at read time).
    Why: claimed-vs-ridden is the mechanism's truth test, and only bytes settle it.
11. Context budget became binding. Wrote this FINAL receipt and stopped. Threads
    not exhausted: G4 depth (a FINAL-marker convention and reconcile pass spec)
    and the mariner open question are named for the next cycle.

Dead ends, named: the two census script failures (item 3, both recovered
in-command); the FP divergence branch archaeology (item 8, stopped at the byte
boundary); the mariner double-ride question (the runner STARTed the pack at
08:12:02 and shows no END, while an interactive window self-reported adopting it
at 08:22:49; which actor writes run_20261010_07_mariner.log is not resolvable
from files alone, named as an open question, not a claim).

## COUNTS (all real, this window)

- Mission pack: 48 lines. Prior FINAL receipt: 305 lines.
- Files read this window: 6 distinct files via 10 read operations
  (leave_dispatcher.py full 220 lines; run_mate.ps1 full 163 lines;
  mag/percolator.py 270-329, 355-384, 385-429, 465-504; mag/router.py 635-664;
  receipt_20261009_gambiter.md full 305 lines; 2 shape probes of the registry
  JSON; runner log tail 25 lines).
- Live registry: 673 invariants, total count 1218, top 41 (3.37 percent),
  603 at 1, 43 in 2-5, 19 in 6-20, 8 in 21-100, 0 above 100, FP counter 13.
  Drift vs 10-09: +1 total count, +1 top count, 0 rows.
- maintenance() scheduled callers repo-wide: 0.
- FP channel: 15 event rows on disk (behavioral 14: 1 spam + 13 "timeout";
  ops 1), span 2026-08-11T12:32Z to 2026-09-23T12:14Z; registry counter 13;
  delta 2. Seal 2026-09-26T09-03-57: false_positives 13, 182 invariant rows.
  heal.log: 14 rows, latest 2026-09-26T13:14:26Z. Display consumers outside
  percolator.py: 3 (emergence, ghost, wearable_swarm) plus 1 research pack.
  Manual false_positive() callers repo-wide: 0.
- Dispatch census: 9 pack-days on disk (09-29, 09-30, 10-02..10-06, 10-09,
  10-10), 72 packs, 64 claim files (09-29 day: 0), 23 receipt files (10-06: 8,
  10-09: 7, 10-10: 8). Claims with no receipt, by day: 09-30 8, 10-02 8, 10-03 8,
  10-04 8, 10-05 8, 10-09 1. Total claims-without-receipts across closed days: 41.
- Today at FINAL-write time: 8 packs, 8 claims (3 zero-byte in-flight, 4 runner
  verdicts exit=0, 1 hand-written interactive-window line), 8 receipt files,
  8 runner STARTs, 4 runner ENDs.
- Standing residuals re-verified: 3 (R1, R2, queue-priority cheap talk).
- New rule changes named this window: 6 (FP 3, dispatch 3). Patches applied by
  me: 0 (spec-only window).
- Cycles ridden: 4. Em-dashes: 0. Receipts filed: 1 (this file, claim then FINAL).

## STATUS

FINAL for this window. Stop: context budget (binding), not thread exhaustion.
Next cycle resumes by id: open threads are (a) G4 depth: a FINAL-marker convention
plus the dispatcher reconcile pass, (b) the mariner adoption question (which actor
wrote run_20261010_07_mariner.log), (c) the standing specs from prior windows
(D1 altjudge skip, D2 ask-bank wiring, R1 maintenance wiring, ladder_class stamp,
FP reconcile). No em-dashes. Real counts only. No fabricated anything.
