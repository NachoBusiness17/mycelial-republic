# LINEAGE - dogfood the estate's past 48h (2026-10-02, lens lineage)

Run: ractor_engine / 2026-10-02-dogfood-48h, lineage lens. Read FIRST per the
ask: watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md (whole). Everything
below either ran this sitting (command named) or is marked carried. No
em-dashes. My jacket: what prior generations asked that was never delivered,
and what this wave dropped between generations.

## The spine of the 48h, lineage-read

Six commits (git log this sitting). The lineage through them is one sentence:
the estate built a gap-ledger (5d2263f10), then every later discovery in the
same window arrived AFTER the ledger was written and never entered it. The
GAP_REGISTER is a snapshot of 18:41:58 EDT 10-01 (Get-Item this sitting:
16,660 bytes, mtime 2026-10-01 18:41:58, unchanged). The librarian's D1-D3
instrument diseases were diagnosed at ~20:54 that night (962e41054; receipts
under watch/inbox/librarian_exp/, instrument-audit.md), the ractor-topic OWED
list at ~06:58Z 10-02, and neither has a home: my greps this sitting
(grep -rln "instrument diseases|D1 arXiv|arXiv-id matching" and then the
broader "verify_canon|disjointness|phantom-groups|HOLD-BOTH") over
queue/todo.md, memory/attention.md, and TICKET_LEDGER.md return exit 1, zero
files. Every gap found after 18:41 10-01 is ledgerless by construction.

## What converted, byte-true on the current tree (I verified each)

- citation_lint wired blocking: githooks/pre-push:24-25 ("PUSH-GATE:
  citation_lint check --changed", exit 1 on fail). The fillball's rank-3 fix
  held.
- percolator --candidates genuinely dogfooded: receipt
  watch/inbox/fillball/percolator-candidates.md:43-65 records the live run (3
  files, 16 rows, idempotence proven, two self-caught defects fixed
  regression-tested). My byte check: memory/percolator/candidates.jsonl holds
  16 rows, 0 promoted (python count this sitting); invariants.json untouched
  BY DESIGN (the promote gate), 5,153 lines, moved 10:00:45Z today.
- corpus-fold real: exactly 6 CORPUS_FOLD_*_20261001.md files in corpus/steal
  (ls -t). Day-1 fold backfilled: watch/inbox/frontier_olm_2026-09-30/ now
  carries DIGEST.md + register.jsonl + percolator_candidates.jsonl (ls).
- census carrier refreshed with instrument discipline:
  watch/inbox/census_refresh_20261002.md names instrument, moment 10:08Z,
  4,147 / 496, and attributes both deltas by landing (read :1-30).
- the engine's topic fix HELD: .zcode/workflows/ractor-engine.dwf.ts:29-32
  declares topic required; this very run's topic arrived defined and rich
  (the ask's spine). Gate digest amended 912a34520349 (commit f4cfcdf9b
  message) to 5253afd2d68d (saved metadata) - the engine was repaired after
  landing, per e3c7d341c's metadata-block repair.

## What did NOT convert (the receipts-only class, swept wider)

1. GAP_REGISTER.md has recorded ZERO of the window's closures. FILL-BALL
   (3c83da5b0, "all 7 register gaps CLOSED") closed register ranks 2-7 plus
   the corpus-fold meta-gap; the register bytes never moved (18:41:58 mtime
   stands). The 2026-10-01-dogfood-gaps synthesis (54M tok) had already
   diagnosed this exact disease ("conversion-by-reader works,
   conversion-by-ledger does not exist") and prescribed status columns as
   ranked move 2. The next generation paid 68.7M tokens and skipped the
   one-column write. Ranks 9, 10, 11 are still OPEN and unrecorded: my greps
   this sitting, grep -c 2606.03458 memory/runs/corpus_gap_research/
   ARXIV_REGISTER.json = 0 (rank 9), grep -c 1sy7srk watch/inbox/
   frontier_olm_2026-10-01/steal/quantization-compression.md = 0 (rank 10),
   grep -n "SS-1|CP-1|R2-1" watch/inbox/hermes_burn/TICKET_LEDGER.md = 0 rows
   (rank 11 - SS-1's DELIVERABLE landed as mag/seed_seal.py, its TICKET never
   existed). The next 100M-token job reads a table that says everything is
   open.
2. The prior synthesis's OWED list, re-checked on the tree this sitting:
   NIGHT_CLOSE_20261002.md untouched since creation (5,147 bytes, mtime
   10/2 01:14:18 EDT = 05:14:18Z; read whole, no erratum section). kpi.jsonl
   GREW 748,222,017 to 752,846,276 bytes, last write 06:42:59 EDT today,
   writer mag/records.py:138 (def write_kpi, sed :130-142), no rotation, the
   1.1GB-to-748MB shrink still unexplained. POSITION_CHANNEL_RESULT.md still
   registered nowhere (Select-String count 0 in watch/inbox/INDEX.json and
   index_events.jsonl). The 23:32:51 EDT invisible_runner launch still
   unattributed (grep "23:32" over watch/inbox md/jsonl: only data files and
   a 09-27 file). The T1W2 19:17-19:18Z double-fire cause still unattributed
   (grep "19:17|double-fire": only pre-10-02 files). The commit-queue law
   named OWED in 2093ca518 still ticketed nowhere (grep -ril over memory/law,
   memory/rib, queue/todo.md, TICKET_LEDGER.md: zero files). Only the engine
   topic fix held (above).
3. The current tree is NOT pushable. Ran this sitting:
   .venv/Scripts/python.exe tools/violation_ratchet.py check --changed
   -> "RATCHET check: scope=10 changed files; hits=10; registered=7; NEW=3"
   -> FAIL. NEW 876887f16352c360 file-too-long tools/code_swarm.py:410,
   dc70327b03aef390 tools/reverse_map.py:406, b028ac6b4f4c92ab
   tools/tier_probe.py:413. The garden night's flagship instrument
   (code_swarm, its $0.22 headline) now blocks the estate's own pre-push
   gate; the fillball percolator receipt already named this pattern
   (percolator-candidates.md:73-81, "belongs to whichever lanes own those
   files") and no lane accepted the debt.
4. The guard-on-dead-organ inversion. grep -lc pidfile over scripts/*.sh and
   tools/*.sh returns exactly one file: scripts/descent_driver.sh. Meanwhile
   NO driver is alive now (tasklist | grep bash/wscript/wsl: only WSL bits;
   usage.jsonl frozen at 236 rows, mtime 21:53Z 10-01). The twin-kill (move
   1, e3c7d341c) stopped the double-drain and also the single-drain: the
   TICKET_LEDGER's parked tickets have no drainer, and the re-registered
   patrol tasks' first scheduled fires (12:30Z / 13:00Z) were still in the
   future at this sitting (logs/census_patrol.log tail ends at the 03:29:15Z
   hand-fire, exit 1 COLLECT-DRIFT by design; logs/fts_index.log tail ends
   09-30 09:00:02). The window's two executed moves were the two live-damage
   stops; every awareness-layer repair (prior synthesis moves 3, 5, 6, 7)
   sat.

## Instruments: dogfooded vs built (the split is same-sitting live fire)

Dogfooded: percolator --candidates (live run above), citation_lint (wired at
pre-push:24-25; the prior synthesis ran it on its own output, SYNTHESIS.md
:174), ractor-engine itself (third run in 36h is this swarm; it caught and
banked its own topic and glob defects, e3c7d341c). Built-not-dogfooded:
mag/seed_seal.py has ZERO consumers (grep -rln seed_seal over mag/ tools/
scripts/ = one hit, the file itself), ZERO .seal sidecars anywhere (dir /s /b
*.seal: empty), the forge-drill is a test fixture not a live seal, the
enforcing flip is operator-gated and ~/.mag still lacks the keyfile (carried
from the 10-01 synthesis rank 5). The candidates pipeline ends at 16 rows
promoted:false with no named promoter (alpha-budget rationed, reviewer
unassigned). code_swarm / rib_swarm / water_computer each fired once in the
garden night (their own proof runs, 0c9d72a06); I found no second
instrumented run receipt (mention-count greps are noisy: 19 / 16 / 178 files,
not run-evidence, not claimed as such).

## Cost (byte-summed this sitting) vs what survives

- memory/runs/hermes_burn/usage.jsonl: 236 rows, ALL inside the window
  (ts >= 2026-09-30T20:00Z), sum $37.7591 (python re-sum; top prefix A1
  $21.85, T1W1 $2.74, DUEL2 $2.43). Matches the prior synthesis's $5.5208
  receipt-window subset.
- memory/runs/model_garden/usage.jsonl: 725 rows, $3.4746 lifetime, all in
  window (key cost_usd; my first pass read 'cost' and got 0, corrected).
- Metered window total: $41.2337 (the "~$42 of ~145" carrier is this number
  rounded; the residual ~$0.77 vs some carrier readings is unlocated by me).
- Workflow tokens: carried from the ask's ListWorkflowRuns (63.1M + 37.6M +
  54.0M + 68.7M = 223.4M over four completed runs; Salon-mine-20deep stopped
  provider, spend unbilled to me) - NOT verified here: this session's run
  introspection is unavailable (tool error workflow_introspection_unavailable).
- What that bought that survives next week, verified on the tree by me this
  sitting: the wired lint, the percolator flag + 24 tests, 6 corpus folds,
  the 09-30 backfill, the refreshed census carrier, the saved + amended
  engine, the pidfile guard pattern, 4 re-registered patrol tasks (payoff
  pending their first scheduled fires). What it bought that does NOT survive:
  the ledgerless D1-D3 diagnosis, the 4 still-open register rows, the red
  ratchet, the unpaid erratum, two unattributed launches, one unexplained
  kpi shrink, and a dead drain lane under a $180-funded ladder.

## Hostile-pass corrections (2026-10-02, second pass, re-checked on bytes)

1. "Recorded ZERO of the window's closures" was false as written. The
   closures ARE recorded, keyed by register rank, inside seven scattered
   fillball receipts (my grep -c GAP_REGISTER watch/inbox/fillball/*.md:
   citation-lint.md 3, day1-digest.md 3, elder-salvage.md 5, errata.md 2,
   percolator-candidates.md 2, seed-seal.md 3; seed-seal.md:91 "Closes: SS-1
   (GAP_REGISTER rank 5 / a07-r3)"). The surviving disease is narrower and
   stands: the register itself (the lane table for the NEXT 100M-token job,
   GAP_REGISTER.md:5-6) still reads all-open at 16,660 bytes / 18:41:58, so
   closure knowledge lives only in receipt prose a consumer must grep across
   seven files to re-derive. Re-derivation tax persists in moved form.
2. "NO driver is alive now" was my own tasklist truncation error (head -8 cut
   the output before bash.exe). wmic this sitting: PID 44072, "C:\Program
   Files\Git\usr\bin\bash.exe" scripts/descent_driver.sh, CreationDate
   20261001173124.249505-240 = 2026-10-01T21:31:24Z, alive; driver.beat tail
   BEAT 2026-10-02T11:24:56Z cycle=962, ~48s cadence. Corrected finding: the
   pidfile guard's mutex is currently HOLLOW - the running driver pre-dates
   the guard (guard landed with e3c7d341c ~07:31Z 10-02), so it never wrote
   state/descent_driver.pid; Test-Path this sitting: NO PIDFILE on disk.
   Per scripts/descent_driver.sh:13-21 a new invocation checks only the
   pidfile and, finding none, starts anyway: a second concurrent driver can
   launch TODAY with the guard in place. The guard binds only pairs of
   post-guard instances and no post-guard instance has ever run. Also
   corrected: my usage.jsonl timestamp label "2026-09-30T21:53Z-equivalent"
   was wrong by one day; true value 2026-10-01T21:53:52Z. The guard edit was
   also written into the script file UNDER the live pre-guard instance (the
   mid-run-edit class that produced the twins' two-script-versions
   divergence); the running instance kept a clean beat through the edit
   (cycles 961-962), so risk documented, corruption not observed. No
   independent live exit-3 proof exists (grep "exit 3|rc=3" over watch/inbox:
   only this run's own lens receipts quoting the commit). Patrol
   re-registration verified direct by my own Get-ScheduledTask read: all four
   exec=powershell.exe -File / python.exe with absolute paths; census
   lastrun 10/02 03:29:29 (the hand-fire, exit 1 = COLLECT-DRIFT by design),
   the other three lastrun 10-01 with lastresult=1 pending their next fires.

## The lineage verdict

The 48h window's conversions are real wherever a fix fired live bytes the
same sitting it landed, and paper wherever the fix's last step was "someone
else writes it down." The estate has now paid three consecutive generations
(54M, 68.7M, and this swarm) to re-discover that the last step is missing.
The register needs one column; the post-18:41 discoveries need rows; the
ratchet needs three names accepted or three files split; the drain lane needs
one guarded driver. None of that is new knowledge; all of it is one sitting
each.

## Blind spots (honest)

- Run introspection unavailable in-session: all workflow token totals and the
  Salon-mine-20deep provider stop are carried from the ask, not verified.
- Full pytest suite not run; census 4,147 / 496 carried from
  census_refresh_20261002.md and the prior synthesis's run.
- tasklist grep covered image names bash/wscript/wsl only; a driver under
  another image (python.exe loop) would be invisible to my filter.
- The 23:32 and T1W2 attribution greps covered watch/inbox and ticket
  surfaces, not all of memory/runs.
- D1-D3 fix-state verified by absence-of-tickets greps; I did not read
  tools/corpus_lens.py line-by-line to rule out a standing D1 fix inside it.
- The 61 primaries (90.6MB) and salon S1-L8 receipts not byte-checked here.
- Nous $47.54 balance carried from 0c9d72a06 + the ask; no live query run.
