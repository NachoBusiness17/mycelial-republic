# DOGFOOD LENS - the estate's past 48h applied to itself (2026-10-02, ~11:05Z)

Run: ractor_engine dogfood lens, window 2026-09-30T20:00Z to 2026-10-02T11:00Z.
Prior synthesis read FIRST (watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md,
whole) and NOT re-derived: its night-receipt arithmetic, POSITION_CHANNEL
finding, excluded $1.0077 hour, twin drain census, and blind-doctor reading all
stand as filed. This lens swept the same disease classes WIDER: every finding
below is new on the current tree, checked this sitting, with the command named.

## F1. The surviving production driver runs pre-guard code; the pidfile guard cannot see it

MOVE 1 of e3c7d341c landed a real guard (scripts/descent_driver.sh:10-24, read
this sitting; second instance exits 3, stale-pid reclaim, trap cleanup;
committed, git log -1 confirms e3c7d341c). But the LEGITIMATE third driver is
still alive on the OLD script image: powershell Get-CimInstance Win32_Process
shows bash PID 44072 CreationDate 10/1/2026 5:31:24 PM EDT (= 21:31:24Z, the
synthesis's third instance), and its beat is live (tail driver.beat: cycle 933
at 2026-10-02T11:01:01Z). state/descent_driver.pid does NOT exist (ls exit 2,
checked twice). A process that never wrote a pidfile is invisible to the guard:
spawn the guarded script now and it finds no pidfile, writes its own, and TWO
drivers drain memory/plans/hermes_burn_* together, the exact twins disease,
re-enabled today. No dollar damage while the queue reads all-skipped (driver.log
tail: "OK T1W1_* cost=$0.00 (skipped)"; "HERMES-BURN: PASS - 4/4 asks; ledger
total $37.76"), but the queue refills the moment a seat stages new asks.
Falsifier: a pidfile present while 44072 lives, or 44072 gone (then the hole is
moot until the next spawn). One-sitting move (~10 min): touch
memory/runs/hermes_burn/DRIVER_STOP, wait one ~48s cycle, confirm the beat
stops, remove STOP, relaunch from the guarded script, verify
state/descent_driver.pid exists.

## F2. The shared INDEX lags its own event log by 114 receipts; the night's two headline receipts ride in NEITHER

INDEX.json mtime is Oct 2 00:18:45 EDT (04:18:45Z), 767,503 bytes, unchanged
through 11:24Z. The append-only territory log keeps growing past it: a strict
json.loads census (3 unparseable lines skipped, named) counts register rows
with ts > 2026-10-02T04:18 at 107 by the hostile pass at 11:10Z, 109 at
11:20Z, and 116 at my recount 11:24:09Z (max event ts 11:23:22Z), none of
them folded: fillball/citation-lint.md is events:2 / INDEX:0 (register op
stamped 2026-10-02T06:16:46Z, still INDEX:0 at 11:24Z), same shape for
percolator-candidates.md and census_refresh_20261002.md. The night's actual
close receipt, NIGHT_CLOSE_20261002.md (created 05:14:18Z, 5,147 bytes, mtime
still creation), greps 0 in INDEX.json and 0 in index_events.jsonl.
POSITION_CHANNEL_RESULT.md (13,416 bytes, mtime 06:09:53Z) is a POST-CLOSE
artifact, 56 minutes after the close, so it is not a night receipt and
NIGHT_CLOSE:40-42's "never existed" was true at its 05:14Z writing (the prior
synthesis held this at SYNTHESIS.md:38-46); it carries the same plain
registration debt (0 in both surfaces, re-grepped 11:24Z). No fold is
scheduled (schtasks /Query /FO CSV /V grep for index_fold = 0 matches; control
grep census_patrol_daily = 1, so the sweep saw real actions). AGENTS.md makes
INDEX.json the first read of every new seat, so the estate's front door map is
hours-to-never behind the territory; the prior synthesis's "registered in
neither" was one instance of a standing fold debt, not a one-off. CORRECTION
(this file's first draft said "114 register rows" via loose grep and called
POSITION_CHANNEL a night headline receipt; both bytes wrong, fixed here per
the hostile pass). Falsifier: an INDEX.json whose mtime postdates the max
register ts in index_events.jsonl AND greps positive for
NIGHT_CLOSE_20261002.md and citation-lint.md, recounted with the same strict
parser; for the post-close label, an NTFS USN record showing a pre-close file
at that path (USN query not run, mtime is the only instrument). One-sitting
move (~20 min): run the WO-10 fold (python -m mag.shared_surface rebuild,
verb documented at mag/shared_surface.py:15), register NIGHT_CLOSE and the
post-close POSITION_CHANNEL_RESULT.md by hand, and ticket the fold onto a
daily task.

## F3. Proof-by-hand-fire covered 1 of 4 re-registered patrols; three remain dark-unproven and the wrapper class survives in a fifth task

The direct re-registration is real in the registry (schtasks /V: MagFtsIndexDaily,
MagImproveDaily, MagLeaveProtocolDaily, MagCensusPatrolDaily all show
powershell/python -File actions, no wscript). But only census was hand-fired to
a log line (logs/census_patrol.log 03:29:15, exit 1 = the COLLECT-DRIFT signal,
since answered byte-exact by watch/inbox/census_refresh_20261002.md: fresh claim
4,147 / 496 at 10:08Z, grammar kept). The other three: FTS Last Run 10/1 9:00:01
AM result 1, logs/fts_index.log last stamp 2026-09-30 09:00:02; improve Last Run
10/1 8:00:01 AM result 1, logs/improve_daily.log last write Sep 30 08:01; leave
same shape. By the estate's own B2-465 test ("no START stamp for today means
the surface is dark... run by hand", AGENTS.md), all three are dark until their
08:00/09:00 EDT fires, which fall after this window's close, so the fix is
unproven exactly where its own commit admits the failure class lives ("path
fixed after my own first registration used a wrong filename"). And the class
was not swept: mag-docker-watchdog still runs
wscript.exe ...\watch\docker_watchdog.vbs (CSV /V grep, this sitting), the same
headless-wrapper shape whose audit trail is one overwritten %TEMP% file
(scripts/invisible_runner.vbs unchanged this sitting, CreateTextFile overwrite
at tail; %TEMP%/invisible_runner_rc.log currently reads "1"; its 23:32 EDT
launch stays unattributed, OWED live; no task references invisible_runner.vbs
anymore, grep 0, so it is an orphaned unaudited tool on disk). Falsifier: exit-0
START stamps for all three in their logs dated 10-02, or a wrong-path failure at
08:00 (which would prove the unproven fix wrong). One-sitting move (~15 min):
hand-fire fts_index_daily.ps1, improve_daily.ps1, leave_dispatcher.py and read
one exit-0 log line each, before trusting tomorrow.

## F4. The citation-lint pre-push wiring is an uncommitted working-tree diff; "LANDED at pre-push" is byte-true only on this disk

3c83da5b0's message says "Citation lint LANDED... byte-checked at pre-push".
The tool and tests ARE committed (git log -1 tools/citation_lint.py =
3c83da5b0, worktree clean). The WIRING is not: git log -1 githooks/pre-push =
f0768f3be (pre-window) and git diff HEAD -- githooks/pre-push shows the entire
15-line citation_lint block as + lines, uncommitted. core.hooksPath=githooks,
so the gate runs on THIS machine (the prior synthesis self-dogfooded it,
SYNTHESIS.md:174), but HEAD's tracked hook has no citation gate: one
checkout/clone/stash-away silently drops the window's flagship guard. Same
shape as the register's staged-never-ticketed disease: the claim names a
landed state, git names a diff. tools/code_swarm.py is likewise M in the
worktree (in-flight edits unaudited here). Falsifier: a commit containing the
githooks/pre-push citation block (git log -S "citation_lint" -- githooks/pre-push
non-empty). One-sitting move (~5 min): commit the hook diff now; the estate's
own build discipline says landed wiring never floats.

## F5. seed_seal signed exactly one production artifact and has zero production verifiers

The window's SS-1 organ is built, specced, and self-tested (mag/seed_seal.py:1-30
read this sitting; fail-closed verify, sign-the-root). Disk census: 61 .seal
sidecars exist, 60 under agents/pytest-tmp-* (test fixtures), exactly ONE in
production: watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.seal,
sealed_at 2026-10-02T04:10:34Z, mtime matches. Caller sweep: grep -rln
"seed_seal|verify_seed" across tests/ tools/ githooks/ INDEX.json returns only
tests/test_seed_seal.py. So the PAM lesson's ported trust anchor (hashes are
forgeable, only the signature binds) is minted once and checked by NOTHING
standing: no patrol, no pre-push leg, no lane verifies seals, and the enforcing
flip is operator-gated by declared design. The instrument answers "is it
forgeable" with no organ asking. Falsifier: any non-test caller of verify_seed,
or a second production .seal with a verifying consumer. One-sitting move
(~30 min): one patrol leg (census_patrol_daily or a weekly gate) running
verify_seed over watch/arc_seeds/*.seal, failing on tamper or missing sidecar.

## What the window cost and what survives (checked, not asserted)

Paid API, this window, both ledgers re-summed this sitting: hermes_burn
usage.jsonl 236 rows $37.7591, ALL between 2026-10-01T13:11:41Z and
21:53:52Z (file max ts; the ledger has NO 10-02 rows); model_garden
usage.jsonl 725 rows $3.4746 (269/$3.1257 on 10-01 + 456/$0.3489 on 10-02,
matching NIGHT_CLOSE's 725/$3.4746). Total ~$41.23, consistent with the ~$42
ledger claim; driver.log's own "ledger total $37.76" matches my hermes sum.
Workflow tokens per the run list given in the ask: 63.1M + 37.6M + 54.0M +
68.7M = ~223.4M across four runs. What survives next week, byte-checked:
ticket redemption 73.8 pct with named same-arc conversions (TICKET_LEDGER.md
row two: 10 SW1 tickets LANDED-with-test, 5 SELFSTEAL upgrades, 4 PROMOTED
with receipts), the census carrier refreshed byte-true, the pidfile guard
committed, 16 live candidate rows in memory/percolator/candidates.jsonl
(mag/percolator.py:484), citation_lint committed as tool+tests, one production
seal. The 223M tokens bought mostly durable bytes; the $37.76 descent day
bought the protocol's first full loop with its ledger legs intact.

## OWED list status, re-checked on the tree right now

- kpi.jsonl: STILL LIVE and GREW, 748,222,017 -> 752,865,877 bytes (wc -c this
  sitting); writer mag/records.py:138 write_kpi appends at :167; no rotation.
- invisible_runner.vbs 23:32 EDT launch: STILL unattributed; script unchanged,
  orphaned (no task references it), %TEMP% rc reads "1".
- T1W2 19:17-19:18Z double-fire cause: STILL unattributed; no new receipt
  names it (grep T1W2 across watch/inbox/*.md returns only day-1 files).
- NIGHT_CLOSE erratum: UNPAID; mtime still creation 2026-10-02 01:14:18 EDT,
  size 5147, zero erratum/1.0077/10.0031/55.2 strings.
- commit-queue law (2093ca518's OWED): STILL ticketed nowhere; grep across
  memory/law/, memory/rib/, queue/todo.md, TICKET_LEDGER.md = zero hits.
- topic-undefined engine input defect: did NOT reproduce in this run (the ask
  arrived with a full topic); code-level fix not inspected (harness side).

## Instrument dogfood verdicts (built vs ridden)

ractor-engine: ridden hard, four runs this window, moves executed same-sitting.
citation_lint: built, wired locally, self-run by the prior synthesis on its own
output. percolator --candidates: ridden once, 16 rows live. seed_seal: built,
fired once, verified by nothing (F5). code_swarm/rib_swarm/water_computer:
receipts exist and one SW1 fold converted code_swarm findings into landed
tests; their night numbers were NOT re-verified this sitting (time-boxed).

Verification stamp (this sitting, ~10:50-11:05Z): wc -c and stat on the paths
named; schtasks /Query /V (MSYS_NO_PATHCONV=1) on five tasks plus CSV /V
sweeps with a control grep; powershell Get-CimInstance Win32_Process;
Get-Process bash (PID 44072, 10/1 5:31:24 PM); git log/diff/status on six
instrument files; grep registration census over INDEX.json +
index_events.jsonl; .venv python re-sums of both usage ledgers; find .seal
census; reads of descent_driver.sh, invisible_runner.vbs, seed_seal.py head,
shared_surface.py head, census_refresh_20261002.md, TICKET_LEDGER tail.
Not run: the SW1 pytest suite, the percolator promote gate, any Nous balance
query, USN journal. Hostile-pass correction applied 11:24Z: strict json.loads
recount of index_events.jsonl (116 register rows past the 04:18Z fold at that
moment, 3 unparseable lines skipped) and the POSITION_CHANNEL_RESULT.md
post-close relabel (mtime 06:09:53Z vs close 05:14:18Z). No em-dash bytes in
this file (kept by construction).
