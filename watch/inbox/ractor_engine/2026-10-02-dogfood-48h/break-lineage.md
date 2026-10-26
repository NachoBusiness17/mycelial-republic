# BREAK-LINEAGE: hostile second pass on the lineage lens (2026-10-02-dogfood-48h)

Seat: break-lineage (ractor engine hostile pass). Moment: 2026-10-02 ~07:0x-07:25 EDT
(~11:0x-11:25Z). Method: every load-bearing byte claim in the lineage lens's four
findings was re-run or re-read this sitting; every falsifier was actively hunted
(sweeps, wmic process reads, scheduled-task reads, dollar sums over the whole
memory/runs usage surface). Commands and outputs named inline. No em-dash bytes
below; one source log line is paraphrased for that reason. Nothing below is
carried from the lens without an independent byte unless marked not run.

## Verdicts

### F1 closure-recording disease: WEAKENED (core byte-true, headline sentence falsified by the lens's own falsifier)

Held, re-verified this sitting:
- Get-Item: watch/inbox/gap_analysis_20261001/GAP_REGISTER.md = 16,660 bytes, mtime
  2026-10-01 18:41:58 (read whole: table at GAP_REGISTER.md:72-85 has no
  status/checked-at column; the only update law is the late-lane clause at :13-15).
- Sole version: `git log --oneline -- watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`
  returns exactly one commit, 5d2263f10; directory holds only GAP_REGISTER.md.
- Prescription-before-fill ordering: SYNTHESIS.md:197-200 (ranked move 2, status/
  checked-at/checked-by columns) written 2026-10-02 00:28-00:36 EDT (SYNTHESIS.md:4)
  precedes the FILL-BALL commit 3c83da5b0 at 2026-10-02 02:54:04 -0400 (git log,
  this sitting).
- Open rows re-grepped: `grep -c "2606.03458" memory/runs/corpus_gap_research/
  ARXIV_REGISTER.json` = 0 (rank 9); `grep -c "1sy7srk" watch/inbox/
  frontier_olm_2026-10-01/steal/quantization-compression.md` = 0 (rank 10);
  `grep -nE "SS-1|CP-1|R2-1" watch/inbox/hermes_burn/TICKET_LEDGER.md` = 0 hits
  (rank 11; the ledger's mtime moved to 10-02 01:13:31 for the SW1 redemption rows
  named in NIGHT_CLOSE_20261002.md:28-33, still without these three). Rank 12 open:
  newest file in watch/inbox/spiking_wide/ is Oct 1 14:42 (ls -lat), before the
  register itself was written.

Fell: "recorded zero of them" is false as written. The lens's own falsifier
("closure receipts keyed by register rank existing anywhere on the tree") fired:
watch/inbox/fillball/seed-seal.md:3 ("The owed waltz from GAP_REGISTER rank 5") and
:91 ("Closes: SS-1 (GAP_REGISTER rank 5 / a07-r3)") are closure receipts keyed by
register rank; my sweep found seven fillball receipts plus 48h_synth/ERRATA.md
referencing the register. The surviving disease is narrower and still real: the
closures are recorded in scattered receipts, never in the register, whose bytes
have not moved since 18:41:58 on 10-01. The lens's 45-min move remains valid and
is if anything cheaper (the receipt material already exists to copy into the
status column).

### F2 five OWED items still live: CONFIRMED (all five byte-verified live; one move premise defective)

- kpi.jsonl: 753,203,531 bytes at my 07:04:26 check, 753,406,066 at the 07:19
  logs listing: unrotated AND actively growing (+~560KB during this pass; lens saw
  752,846,276 at 06:42:59). Writer confirmed at mag/records.py:138 (`def write_kpi`).
- NIGHT_CLOSE_20261002.md: 5,147 bytes, mtime 10/2 01:14:18, read whole this
  sitting: no erratum section; tree-wide sweep finds no file referencing
  NIGHT_CLOSE_20261002 except this run's own lenses and the unrelated
  watch/inbox/model_garden/NIGHT_CLOSE.md.
- 23:32 launch unattributed: `grep -rln "23:32" watch/inbox` = 0 files. Extended
  beyond the lens's scope to memory/: ten memory/agent_sessions/orc-*.json hits,
  all routine 2026-09-13T23:32:18Z pheromone timestamps (spot-read one), none
  naming the 10-01 23:32 EDT wrapper launch. Still unattributed.
- T1W2 19:17 double-fire: `grep -rlnE "19:17|double-fire" watch/inbox` = 0 files.
- commit-queue law unticketed: `grep -rnE "commit-queue|commit queue"` over
  memory/law, memory/rib, queue/todo.md, TICKET_LEDGER.md = 0 hits (with -E; the
  alternation is real, not a broken-BRE artifact).
- Engine topic fix held: .zcode/workflows/ractor-engine.dwf.ts:29-32 declares
  topic required: true (read this sitting); this run's own topic arrived defined.

Defect in the lens's move, not its evidence: "one INDEX row for
POSITION_CHANNEL_RESULT.md" targets a file that does not exist (`ls
watch/inbox/POSITION_CHANNEL_RESULT.md` fails; NIGHT_CLOSE_20261002.md:40-42
itself says "never existed"). You cannot index a nonexistent file; the erratum
re-scoping that line is the whole repair for that half. POSITION_CHANNEL has 0
rows in watch/inbox/INDEX.json and index_events.jsonl (both greps run).

### F3 ratchet RED with 3 unaccepted NEW rows: CONFIRMED and STRENGTHENED

Re-run this sitting: `.venv/Scripts/python.exe tools/violation_ratchet.py check
--changed` = "RATCHET check: scope=10 changed files; hits=10; registered=7; NEW=3
... RATCHET: FAIL" with NEW 876887f16352c360 file-too-long tools/code_swarm.py:410,
NEW dc70327b03aef390 tools/reverse_map.py:406, NEW b028ac6b4f4c92ab
tools/tier_probe.py:413. Byte-identical to the lens's run.

Strengthened beyond the lens: the receipt it cited (fillball/percolator-candidates.md:73-81)
names a DIFFERENT foreign triple (field_experiment.py 637L, hermes_burn.py:393
except-pass, model_garden.py 446L). So inside one window the unaccepted-foreign-debt
class produced two different triples at two different moments and neither triple was
ever accepted by name (today's run still FAILs; yesterday's three no longer show as
NEW, meaning they left changed-scope or were resolved, while three fresh ones
appeared). The pattern is worse than the lens stated: the debt is regenerating, not
merely standing.

### F4 pidfile guard on a dead organ: WEAKENED (guard-monoculture confirmed; "dead organ / no driver process" falsified by a live process)

Held:
- `grep -rn "pidfile" scripts tools` = exactly one hit, scripts/descent_driver.sh:20
  (stale-pidfile reclaim message). Guard monoculture is real.
- No proof receipt that the guard ever fired (no second-instance exit-3 receipt
  found in my sweeps).
- logs/census_patrol.log tail = "[2026-10-02 03:29:15] END exit=1" (the COLLECT-DRIFT
  hand-fire by design); logs/fts_index.log tail = "[2026-09-30 09:00:02] END
  exit=0". usage.jsonl: 236 rows (re-counted this sitting via json parse), mtime
  10/1 5:53:52 PM EDT. Note: the lens's "2026-09-30T21:53Z-equivalent" label is off
  by one day; 10/1 5:53:52 PM EDT = 2026-10-01T21:53:52Z, which matches
  NIGHT_CLOSE_20261002.md:52-53 ("all landed by 21:53Z").
- Payoff unproven, sharpened with scheduled-task bytes (Get-ScheduledTaskInfo +
  Actions this sitting): all five tasks are now DIRECT (powershell -File or
  .venv python.exe, no wscript), all five Last Result = 1 from the pre-fix fires
  (census LastRun 10/2 03:29:29 matching the log's 03:29:15 END; FTS/Improve/
  Leave/EstateWalk LastRun 10-01), and ZERO have fired since re-registration;
  first proof lands at today's 08:00/08:30/09:00/09:15 EDT fires (12:00-13:15Z).

Fell: "the one organ that is now dead" and "no driver pro[cess]" are false.
wmic process read this sitting: bash.exe PID 44072 running
`scripts/descent_driver.sh`, born 20261001173124-240 = 2026-10-01T21:31:24Z, alive
at this sitting; NIGHT_CLOSE_20261002.md:50 names "driver start 21:31:24Z" (this
is the sanctioned night driver, not one of the killed 20:40:13Z twins). The lens's
"tasklist shows no driver" was its own admitted blind spot firing (its
bash/wscript/wsl filter cannot see command lines at all, and tasklist without
wmic cannot distinguish drivers from harness shells; my own first interleaved
tasklist also returned empty, a pipe artifact). One instance only, so no live
descent twin; but the organ is alive, and the guard's actual exposure is
elsewhere (see additions).

## Blind spot dispositions

1. Run introspection: REPRODUCED UNAVAILABLE from this seat too (ListWorkflowRuns
   = workflow_introspection_unavailable, this sitting). The lens's totals
   (63.1M/37.6M/54.0M/68.7M, Salon provider stop) remain carried, now from two
   seats. Promoted to an addition below.
2. Full pytest suite: not run by me either; 4,147/496 remains receipt-carried
   (watch/inbox/census_refresh_20261002.md). Not needed for any verdict here.
3. python.exe invisibility: FIRED. wmic found the hermes gateway (PID 14828,
   hermes_cli.main gateway run), the stealth twins below, and the hot supervisor
   fleet (see addition 2).
4. 23:32 attribution elsewhere: checked memory/agent_sessions; hits are unrelated
   2026-09-13 pheromone rows. Attribution stands absent.
5. D1 line-by-line: pattern-grepped (not full read) mag/persona_priorart_acquire.py
   and mag/head_museum.py: no semantic-title matching surface and no literal
   backslash-b regex found (grep -Fn); the librarian's one-sitting semantic
   recovery did not land as a standing fix in these tools. Scoped honest: grep
   patterns, not a full read.
6. 61 primaries / 90.6MB: not byte-checked (not run).
7. Nous balance $47.54: no live query (not run).
8. The $0.77 gap: RESOLVED (see addition 4).

## Additions (what the lens missed)

1. The estate's best single-instance law is being violated in its own log, live
   now. tools/stealth_driver.py:46-47 promises a second instance "prints a loud
   refusal and exits 2" behind a win32 named mutex / lockfile (:693-715, lockfile
   state/stealth_driver.lock, wave5 lock test 2026-09-29). But
   logs/stealth_driver_stdout.log (1,010 bytes, static since Oct 1 03:57) holds
   TWELVE "stealth_driver: loop start" lines and ZERO refusal lines, including
   three starts AFTER a ".off flag present, exiting on operator word" line (the
   log's line 9, paraphrased; source carries an em-dash byte). And two same-second
   instances are alive right now: pythonw PIDs 17732 (.venv, 796K RSS, stuck-
   looking) and 54236 (uv, 26MB), both running scripts/run_stealth_driver.py,
   born 2026-10-01T07:57:19.213Z and .273Z (wmic CreationDate), 60ms apart, on two
   different interpreter installs (a named mutex is interpreter-independent, so
   cross-interpreter lock failure or a pre-lock hang is the open question; the
   796K instance may be hung before the lock). Who launched two drivers at 03:57
   local after an operator .off stop is unattributed (same class as the 23:32
   wrapper launch). Falsifier: one PID being a parent/child stub of the other
   rather than an independent loop, or timestamps inside state/stealth_driver.lock
   showing the second start was refused after all. Move: ~30 min: read
   state/stealth_driver.lock, kill the 796K instance after confirming the 26MB one
   holds the lock, add a per-line timestamp to the loop-start log, and name the
   03:57 launcher (schtasks sweep) in the same sitting.
2. The organ census the lens never ran: descent_driver.sh is ALIVE (PID 44072,
   born 2026-10-01T21:31:24Z, wmic this sitting), and the supervisor fleet is hot
   at this sitting: logs written 07:19-07:20 EDT Oct 2 for lab_sv, dashboard_sv,
   api_gateway_sv, backend_sv, drainer_sv, ghost_sv, lane_scheduler(_sv),
   supervisor.jsonl (ls -lat logs). None of these carry a pidfile/mutex surface
   (the scripts+tools grep found only descent_driver.sh:20); whether the
   supervisor enforces single-instance for its _sv services is unverified (OWED).
   Falsifier: a supervisor config proving single-instance enforcement for each
   _sv service. Move: ~20 min: one sitting reads the supervisor's restart policy
   and records which of the eight hot organs are twin-safe by construction.
3. The engine cannot byte-verify its own cost dogfood from inside a run.
   ListWorkflowRuns fails with workflow_introspection_unavailable from dwf actors
   (reproduced this sitting from a second seat), so every token/cost claim about
   the window's workflow runs (63.1M/37.6M/54.0M/68.7M, the provider stop) is
   carried, never byte-checked, by exactly the seats asked to dogfood cost
   (question 3). Falsifier: a dwf actor session where the tool succeeds. Move:
   ~10 min: the main seat (which can list runs) attaches the run table with token
   totals to this run's receipt before fold.
4. The dollar truth is exact and the $42 carrier overstates it. Summed every
   usage.jsonl under memory/runs this sitting (recursive glob, cost_usd column):
   hermes_burn 236 rows $37.7591 + model_garden 725 rows $3.4746 + grok_free 540
   rows $0.0 = $41.2337, exactly the lens's figure; no other usage files exist
   under memory/runs, so the ~$0.77 gap to the "~$42 of ~$145" carriers (ask and
   commit 0c9d72a06) is carrier rounding-up, not missing files. Falsifier: a
   usage ledger outside memory/runs feeding the same carrier. Move: ~10 min:
   correct the carrier line at its next edit (also reconciles with
   NIGHT_CLOSE_20261002.md:52-56's $8.9954 overnight subset).
5. The unwired-guard sweep, run: 8 of 18 while-True loop scripts carry no lock,
   mutex, or pidfile surface (pattern grep this sitting): tools/autopilot.py,
   tools/dfhack.py, tools/seed_mcp_cold_client.py, tools/weights_consolidate.py,
   scripts/capacity_ladder.py, scripts/handoff_escalation_watcher.py,
   scripts/run_ghost_loop.py, scripts/trailer_mode.py. Ten of eighteen show a
   lock-ish surface (grep-scoped: any "lock|Lock|mutex|pidfile" token, may
   overcount). Combined with addition 1 this is the real answer to the window's
   "pidfile guard exists on descent_driver.sh only" question: one pidfile, one
   named mutex that demonstrably double-started, eight naked loops.
   Falsifier: guards living outside the scripts (supervisor, task scheduler
   single-instance flags). Move: ~40 min: either land a shared lock helper and
   adopt it in the eight, or record the eight as accepted debt by name in the
   ratchet baseline's cousin (a guards register), plus add the while-True check
   to the dogfood lens's standing checklist.

## Not run (stated, not guessed)

- Full pytest suite; the 4,147/496 census (carried from the 10-02 receipt).
- Byte-verification of the 61 primaries / 90.6MB librarian claim.
- Live Nous balance query.
- The 3-concurrent-descent-drivers puzzle: twins born 20:40:13Z were killed per
  e3c7d341c while PID 44072 (born 21:31:24Z) ran through the same window to now;
  whether three concurrent descent drivers existed 21:31Z-07:31Z is not
  determinable from the bytes I read (OWED to the descent driver's own log).
- A second-instance exit-3 proof of the descent pidfile guard (no receipt exists;
  firing one is a 5-minute sandbox test the next seat can run).

Fold note for synthesis: verdicts F1 and F4 weakened (not killed) with their
falsifier hits named; F2 and F3 confirmed with corrections that make their moves
cheaper, not weaker.
