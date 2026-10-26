# SYNTHESIS - dogfood the 48h window (2026-10-02, filed ~11:50Z)

Run ractor_engine / 2026-10-02-dogfood-48h, stage synthesis: after the lenses,
the hostile second pass, and the steering rounds. Folded inputs: this run's
receipts in watch/inbox/ractor_engine/2026-10-02-dogfood-48h/ (accuracy.md read
whole this sitting; its F5 revision at accuracy.md:105-129 is the corrected
money verdict), the surviving findings array the ask handed me, and the prior
synthesis watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md (read FIRST per
the topic law; this chapter goes past it, it does not re-derive it). Window:
2026-09-30T20:00Z to 2026-10-02T11:00Z, six spine commits plus the in-window
43f50ed71, on the 110-file uncommitted working tree the ask names.

## The chapter: the receipts learned honesty, the mechanisms inherited the lie

Start at the end, at the money. Of the $37.7591 the hermes ledger rows for this
window's paid judgment (236 rows, whole ledger, python (id,turn) census run by
the economics lens this run), $25.5316 is re-fire excess after the first copy of
each key: 67.6 cents of every paid dollar bought an answer the estate already
owned. One ask is most of the bleed: A1_steer_antiforgery re-fired 49 times
between 13:11Z and 20:17Z at claude prices ($0.13 to $0.65 a shot) for $21.0932
of excess. The drain's own code confesses the class in its patch comment:
tools/hermes_burn.py:200-203 records "A1_steer_antiforgery re-burned 45x
($20.53)" as the reason _landed_skip exists. And _landed_skip is check-then-
fire, not a claim: I read it this sitting (tools/hermes_burn.py:197-218, an
existence test with no atomic lock between check and fire), and the 13
twin-doubled keys of 21:39-21:53Z fell AFTER that check was already in the
tree, which is proof by execution that two readers can both pass it and both
spend. The commit celebrated for stopping the bleed, e3c7d341c, addressed the
twin slice: about 4.5 pct of the excess class ($2.2521 doubled vs $1.0939
first-copy, the prior synthesis's pair sum, re-derived digit-exact by this
run's accuracy lens at accuracy.md:12-15). The estate cured the specimen and
declared the epidemic closed while the pathogen, no atomic claim at the money
organ, is still in the code today.

That shape, the N=1 cure, is the window's real disease, and it repeats at every
scale the lenses swept:

- The guard landed on the launcher, not the drain. tools/hermes_burn.py and
  tools/ds_workhorse.py, the queue drainers any seat can hand-fire, carry zero
  claim locks (accuracy.md:76-90); the single-instance doctrine has been a rib
  since 2026-08-25, commit 47d3907e3, mag/autodrain.py:6 ("two loops = double
  cadence + CPU hog (the known failure)"), and descent_driver shipped five
  weeks later without copying it.
- The guard that DID land is inert on the current tree. The surviving descent
  driver, PID 44072 born 21:31:24Z from pre-guard script bytes under a
  daemonized parent, writes no pidfile: my own ls this sitting shows state/
  holds only autodrain.pid (Sep 22) and night_cadence.pid (Aug 28), no
  descent_driver.pid, so scripts/descent_driver.sh's guard passes on every new
  launch and a second driver would double-drain beside 44072 today. The only
  reason no money is doubling right now is that the queues are dry and the
  ledger's last row is 21:53:52Z (economics lens).
- Built once, never swept: exactly 1 of 11 long-running loop/driver scripts in
  scripts/ carries a pidfile guard (ops lens grep this run), and the two organs
  that once wrote pidfiles left theirs stale and unclaimed in state/.
- Built, never fired: seed_seal has signed nothing in production (zero .seal
  sidecars outside pytest fixtures, zero callers outside mag/seed_seal.py
  itself, dogfood lens grep) and percolator --candidates has zero non-test
  callers, both landed by FILL-BALL 1001 as register-gap closures.

Why does the same class keep winning? Because the organ that remembers debts
rotted first. state/CURRENT.md still says updated 2026-09-30T11:56Z with
latest result last_mile_20260930: the estate's live-truth pointer predates the
entire six-commit window. queue/todo.md is mtime Sep 29 06:53. 4 of the prior
synthesis's 8 moves are unpaid on the tree (its moves 3, 5, 6, 7: the
NIGHT_CLOSE erratum, the kpi rotation, the VBS audit trail, the commit-queue
ticket; accuracy.md:54-74), and the kpi wound is on its fourth reading:
748,222,017 bytes at the prior synthesis's moment, 752,846,276 at the accuracy
lens's (accuracy.md:54-56), and 753,736,154 at mine (ls, mtime 2026-10-02
07:36:47 EDT, that is 11:36:47Z), writer unchanged at mag/records.py:138. The
Aug-25 rib ignored in September is the operator's own DESCENT PROTOCOL leg 1
violated by the estate itself: never relearn a known lesson expensively. The
estate paid that tuition again this window, at claude prices.

And now the good news, because it is real and it is new. The receipts got
honest. The prior synthesis watched every claim about a neighbor fall
(POSITION_CHANNEL_RESULT, the excluded twin hour, unregistered receipts); this
run's wider sweep across all six commits found the money core digit-true to the
last token: NIGHT_CLOSE_20261002.md:50-56 says "usage ledgers" plural and names
both files, and the re-sum of exactly those two ledgers reproduces $8.9954 and
5,547,496 tokens including the per-part breakdown (accuracy.md:105-129), while
commit 0c9d72a06's "Ledger ~$42 of 145" re-sums to $41.2337, an honest tilde.
Better: the engine's immune system worked on the engine. The hostile pass
forced the accuracy lens to withdraw, on the record, a false accusation against
a correct receipt (F5 REVISED at accuracy.md:105-129, the withdrawal recorded
per the no-fabrication law), and the break pass caught the lens's own false
evidence sentence (the "only unrelated burn_reset files" grep line; about 40
files hit, banked in break-accuracy.md). The lying did not disappear; it moved
down a layer, from prose numbers to mechanism claims: a guard that guards
nothing, "42 tests" that collect as 19 (pytest --collect-only on
tests/test_inference_budget.py reads 19, accuracy.md:92-103), a commit message
claiming "3 bleed-class patches + 21 tests" while carrying zero files under
tests/, tools/, mag/, or scripts/ (43f50ed71; the bytes landed silently in
5d2263f10 at 00:46:30Z, the tests in 0c9d72a06 at 04:18:32Z, lineage lens
git-show this run), and the morning's flagship census receipt stamping its
proof fire "03:29:15Z" when schtasks shows 3:29:15 AM EDT, that is 07:29:15Z,
bracketed by the 07:31:54Z commit (ops lens). Receipts the estate can now
trust; mechanisms it must now re-audit. That is progress with a bill attached.

## The five dogfood questions, answered

1. Byte-true vs theater, swept wider: SURVIVORS (ran, not trusted): the
   patrols are DIRECT on the live scheduler (schtasks /Query /V, zero VBS
   actions, accuracy.md:20-25); citation_lint is wired at githooks/
   pre-push:24-25 (read by me this sitting); seed_seal's 14 tests pass live
   (ran twice this run); percolator --candidates is at mag/percolator.py:23-25;
   corpus-fold's 6 entries are on disk; census 4,147 reproduced at a second
   moment (10:50:18Z, accuracy.md:34-37); Dynamo and Lamport primaries exist on
   disk (accuracy.md:38-40, sampled); LINKS 250->257 is resolved live (wc -l
   memory/corpus/LINKS.jsonl = 257, economics lens); the engine topic fix HELD
   (saved workflow declares topic required, digest 5253afd2d68d past the
   commit's 912a34520349; this very run rode a formed topic); receipt INDEX
   registration healed (9 rows, ops lens). THEATER: the inert pidfile guard
   (above), the 42-vs-19 tests claim, 43f50ed71's message, the census
   receipt's EDT-as-Z stamp, and the dogfood lens's beat/log join showing the
   20:40:13Z driver stream still cycling at >=07:26:57Z against the kill
   claim (its finding arrived truncated mid-sentence in the ask's
   transmission; the complete evidence is cited here, the truncated final
   clause is not asserted).
2. The unwired-organ disease, beyond the ask's examples: guard on launcher
   not drain; 1 of 11 loops guarded; two stale unreclaimed state/*.pid;
   seed_seal and percolator --candidates with zero production callers;
   citation lint covers changed prose only (data files are another class by
   design, AGENTS.md lint bullet); the seed-seal enforcing flip still
   operator-gated (3c83da5b0 message, ask-given, unchallenged by any lens).
3. Cost and yield: paid hermes $37.7591 (236 rows, 4,368,123 prompt+
   completion; 5,639,068 with reasoning) plus garden $3.4746 (725 rows) =
   $41.2337 the "~$42" rounds honestly; night core $8.9954 / 5,547,496
   tokens, digit-true. The head is blind: hermes first row 2026-10-01T13:11:41Z,
   garden 22:10:27Z, so ~26 hours of the window (all of GAP ANALYSIS and
   LIBRARIAN) are priced by no ledger at all, and the workflow token counts
   (63.1M + 37.6M + 54.0M + 68.7M) are ask-given, not verifiable here
   (workflow_introspection_unavailable, reproduced, accuracy.md:143-145).
   Yield per arc: 67.6 pct of the paid hermes dollars were re-fire excess,
   and the survivor set above is what the other 32.4 pct bought, and it
   holds. Same-arc conversions this window: spec->gate (citation_lint,
   scenario suite), finding->cure (twins, patrols), claim->erratum owed.
4. Prior OWED disposition, live on the tree right now: kpi rotation UNPAID
   (four readings above); invisible_runner.vbs 23:32 EDT launch still
   unattributed, zero audit code; T1W2 19:17-19:18Z double-fire now
   CLASS-attributed (a second driver instance born 19:17:13Z, driver.log:449
   cycle-1 header, racing driver 1's pass; S7_mates ledger rows 19:18:24 and
   19:18:25, same second) with the exact trigger still OWED; NIGHT_CLOSE
   erratum UNPAID (mtime unchanged from its 05:14Z creation); commit-queue
   law still ticketed nowhere (zero rows across todo, TICKET_LEDGER,
   memory/law/registry.json); engine topic-undefined defect FIXED AND HELD
   (verified by this run's own input).
5. Dogfooded vs merely built: SELF-FIRING: citation_lint (wired, and it linted
   the prior synthesis's own file per its stamp), the ractor-engine itself
   (this run; its hostile and break passes caught its own lens twice and
   banked both corrections), the census instrument (second-moment
   reproduction). REGISTERED BUT NOT YET GREEN: all four patrol tasks are
   DIRECT on schtasks but only census has a post-fix proof fire; FTS, improve,
   and leave last ran 10-01 pre-fix with Last Result 1, next fires 08:00/09:00
   EDT today, after this window closes, so their first green direct-fire logs
   are OWED until read. BUILT, NEVER FIRED: seed_seal, percolator
   --candidates. RECEIPT-ONLY (no surviving lens re-ran them): code_swarm,
   rib_swarm, water_computer; their numbers stand on the garden receipts
   (SWARM_1.md:27-28, RIB_SWARM_1.md:34), not on this run's instruments.

## OWED (honest residue, never asserted)

- The ~26-hour blind head: no instrument prices GAP ANALYSIS or LIBRARIAN in
  dollars; workflow introspection stayed down all run. Never assert a window
  total that includes those hours.
- The exact T1W2 19:17 trigger; the reconciliation of the dogfood lens's
  log-join (20:40:13Z stream cycling through >=07:26:57Z) with the ops lens's
  process table (exactly one real driver, PID 44072 born 21:31:24Z); the
  truncated final clause of that finding.
- Where "42" came from (no instrument named anywhere; falsifier open,
  accuracy.md:99-101).
- rib_swarm "$0.075" vs the receipt row's "$0.0455" (accuracy.md:138-139);
  code_swarm "$0.22" and salon "$0.058" not re-derived (accuracy.md:136-137).
- The 61 primaries were sampled (2 of 61), not censused; the 975-artifact
  inventory not re-counted (accuracy.md:148-149).
- Nous $47.54 is probe-true at 00:27:53Z only; live balance not re-probed
  (paid call, accuracy.md:155-156).

## Ranked moves (top first; ~250 min total)

1. Atomic per-ask claim at the drain (O_EXCL marker or lockdir at the
   hermes_burn.py fire path, reusing the descent_driver guard pattern) plus a
   doubled-key alarm at ledger ingest (~40 min).
2. Bounce PID 44072: touch memory/runs/hermes_burn/DRIVER_STOP, wait one ~50s
   cycle, kill, relaunch under the guarded script, then verify the pidfile
   exists and a deliberate second launch exits 3 (~20 min).
3. One erratum + front-door sitting (~60 min): NIGHT_CLOSE erratum (re-scope
   the "never existed" line, add the excluded $1.0077 so the twin-corrected
   night reads $10.0031, fix the cadence to 55.2 s/cycle), fix the census
   receipt's EDT-as-Z stamp, add the commit-queue row to TICKET_LEDGER.md and
   queue/todo.md, land the kpi.jsonl rotation at mag/records.py:138 with a
   last-consumed-offset meter, file the 43f50ed71 erratum, and refresh
   state/CURRENT.md to name the window's six commits.
4. Sweep the instance guard into a shared tools/instance_guard.py across the
   drainers and loops (hermes_burn.py, ds_workhorse.py, wave_driver.py,
   run_stealth_driver.py, run_autorun_loop.py) and purge-or-reclaim the two
   stale state/*.pid files (~45 min).
5. Re-count the inference_budget battery with a named instrument and correct
   the two downstream repeats (census_refresh_20261002.md:26 and the AGENTS.md
   Tests bullet), or name where 42 came from (~15 min).
6. Fire the built organs: one production seed_seal signature with a wired
   verifier leg, percolator --candidates into one scheduled run or both
   registered intentional-manual in the GAP_REGISTER; after the 08:00/09:00
   EDT fires, read logs/fts_index.log and the improve/leave logs for the
   three unproven patrols (~30 min).
7. Stamp both usage ledgers with coverage headers naming their first-row
   moments (2026-10-01T13:11:41Z and 22:10:27Z); future closes bank
   workflow-run token totals at close time so no window grows a blind head
   again (~15 min).
8. A cheap commit lint: a message claiming tests or patches must match the
   diff's file classes (~25 min).

## Verification stamp (this sitting, ~11:30-11:50Z)

Ran by me: ls -la --time-style=full-iso logs/kpi.jsonl state/*.pid (kpi
753,736,154 bytes at 07:36:47 EDT = 11:36:47Z; no descent_driver.pid);
Read tools/hermes_burn.py:185-284 (_landed_skip, REFUSED patch); Read
githooks/pre-push whole (citation_lint at :24-25); Read the prior synthesis
watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md whole; Read this run's
accuracy.md whole; grep on the written file: em-dash count 0, en-dash count 0,
14871 bytes. Cited from the ask's findings array (lens runs this run,
not re-run by me): the (id,turn) census and A1 sums (economics), WMI process
read (operations), schtasks queries (operations, accuracy), pytest runs
(accuracy, economics), git show and log -S (lineage), greps (all lenses).
Not run by anyone this run: WMI re-read, USN journal, the 61-primary census,
a live Nous probe.

Filed by synthesis. Written to
watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md. No em-dash
bytes.
