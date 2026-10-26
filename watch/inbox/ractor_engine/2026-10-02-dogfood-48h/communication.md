# COMMUNICATION LENS - dogfood 48h (window 2026-09-30T20:00Z to 2026-10-02T11:00Z)

Ride: relay audit. What actually reached the operator-facing surfaces versus
what the window's receipts claim was communicated. Every check below was run
this sitting (2026-10-02 ~10:45-10:55Z) unless marked OWED/not-run. Read
FIRST and went beyond: watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md
(the prior synthesis; its money core was triple-verified there, I did not
re-derive it, I spot-checked the ledger tail and kpi size only).

## Finding 1: the window reached git log and nothing else the operator reads first

state/CURRENT.md, the surface AGENTS.md load order names "live truth", is
stamped updated 2026-09-30T11:56:08Z (file bytes line 8; NTFS LastWriteTimeUtc
matches, Get-Item this sitting): it predates the entire 48h window. Its "Last
result" still points at the 09-30 last-mile wave (state/CURRENT.md:20). Six
commits, 223M+ workflow tokens, and the ledger's ~$42 never touched it. The
file is not even git-tracked (git ls-files state/CURRENT.md returns empty).
Its writers are lane/harness organs (grep: mag/agent_cli.py, mag/lanes.py,
mag/operator_inbox.py, mag/realign.py, mag/session_maze.py), and none of the
window's six arcs rode a lane, so the write never fired. The sibling surfaces
agree by omission: state/LIVE_REPORT.md (written 09:58:33Z today, in-window)
says "Supervised loops running: none" and carries zero window events; the
dashboard day_work trail's newest rows are lane heartbeats only
(dashboard/static/trails/day_work.jsonl tail: 10:03:59Z HEARTBEAT, 10:30:24Z
CYCLE "mirrored 10 lanes"). The only channel that carried the window's
content out is the six commit messages themselves.

Falsifier: a CURRENT.md or LIVE_REPORT.md or day_work row written in-window
that names any of the six arcs. Move (one sitting, ~20 min): add "stamp
state/CURRENT.md (Last result + updated)" to the close checklist of every
window close receipt, or have mag/surface_rebuild.py refresh the pointer
alongside the fold it already owns.

## Finding 2: the night close receipt, the window's headline artifact, is invisible to the shared surface, and its erratum is unpaid

The estate's own instrument, run read-only by me (.venv/Scripts/python.exe -m
mag.shared_surface rebuild --dry), returns "invisible": ["NIGHT_CLOSE_20261002.md"]
(the only top-level invisible file, alongside 7 stale). Zero register events
(grep index_events.jsonl for NIGHT_CLOSE* : 0 rows) and zero INDEX.json rows.
Per the estate's own law this is permanent: mag/surface_rebuild.py:5-8,
"files on disk with ZERO register events ... are truly invisible to the fold
(a refold alone can never see them)". The heal verb exists (WO-10) and was
not run after the close. Worse, the awareness-layer repair the prior
synthesis ranked move 3 is still unexecuted: NIGHT_CLOSE_20261002.md's
LastWriteTimeUtc is 05:14:18Z, identical to its creation stamp, so the file
has never been edited; line 40 still reads "POSITION_CHANNEL_RESULT.md:
never existed"; the excluded $1.0077 is still absent from the totals; and
watch/inbox/hermes_burn/TICKET_LEDGER.md:130 still paraphrases sweep 2 as
"- k touched-module keywords 23 passed" with no keyword list. Commit
e3c7d341c executed moves 1 and 2 and skipped the relay move.

Falsifier: any register event for NIGHT_CLOSE_20261002.md, any file mtime
after 05:14:18Z, or an erratum section present. Move (~45 min): run
python -m mag.shared_surface rebuild (the real heal, idempotent by its own
docstring), then pay the erratum: re-scope the "never existed" line, add the
excluded $1.0077, correct the cadence, add sweep 2's exact command, and
surface the TALK-1 verdict to the morning surface.

## Finding 3: the heal organ has the unwired-sibling disease inside itself: its census is top-level only, so subdir receipts are blind forever

mag/surface_rebuild.py:133-134 builds the invisible census from
inbox.iterdir() filtered to p.is_file(): recursion depth zero. So
watch/inbox/model_garden/POSITION_CHANNEL_RESULT.md (zero register events:
grep 0; zero INDEX.json rows: grep 0) is invisible to the fold AND to the
heal whose entire purpose is curing invisibility. Even a perfect heal run
today registers the night close and still leaves the position-channel
verdict unfindable by the contract's read-first path. The commit message
claim "position channel half-channel banked" is byte-true on disk and
unreachable by the surface contract: banked bytes, no relay.

Falsifier: the dry census naming any file inside a subdirectory (would prove
recursion exists). Move (~30 min): widen the census iteration to one-level
subdirs (or rglob) with the same skip set, plus a test row in the WO-10
suite.

## Finding 4: the alert channel healed one leg and left three, and one descent driver is still alive with no close-out receipt

What worked, byte-checked this sitting: memory/attention.md carries the
03:29:15 census COLLECT-DRIFT row and the response was executed in one
sitting (AGENTS.md Tests bullet refreshed to the 2026-10-02 census, receipt
watch/inbox/census_refresh_20261002.md written 10:10:13Z). All four patrol
tasks are re-registered DIRECT on the live scheduler (schtasks /Query /V via
watch/inbox/ractor_engine/2026-10-02-dogfood-48h/_taskquery_comm.ps1: every
"Task To Run" is powershell -File or python.exe, no VBS), and census is
proven: logs/census_patrol.log is 14,425 bytes, today-stamped, ends
"END exit=1" (the COLLECT-DRIFT verdict, not a wrapper corpse).

Still open, same sitting's bytes: (a) the meter patrol's GAP alert for
2026-10-01 remains unfilled and unanswered: watch/inbox/DATED_METERS.jsonl
holds 4 rows for 2026-10-02 and ZERO for 2026-10-01 (venv-python row count),
so the window's biggest day has no meter witness, and the decision the
alert demanded ("decide whether the gap days need a manual wire pull",
memory/attention.md) has no receipt anywhere I searched; (b) kpi.jsonl grew
PAST the synthesis figure: 752,846,276 bytes at 10:42:59Z (Get-Item), +
4.6MB since the 06:58Z reading, writer still unrotated at mag/records.py:138;
(c) the FTS surface is dark right now: logs/fts_index.log last write
2026-09-30T13:00:21Z, catalog.jsonl (07:34:42Z today) is newer than
catalog_fts.sqlite (2026-10-01T23:45:12Z), so corpus_search is in decay, and
3 of the 4 re-registered tasks (FTS 09:00, improve 08:00, leave 08:00 EDT =
12:00/13:00Z) have not yet had their first direct firing: their Last Result
is still the 10-1 failure; proof exists for 1 of 4; (d) the 21:31:24Z
descent driver, the one whose birth the night close anchored its window to
("since driver start 21:31:24Z"), is STILL ALIVE: Get-CimInstance Win32_Process
this sitting shows PID 44072, CreationDate 10/1/2026 5:31:24 PM local =
21:31:24Z, CommandLine "bash.exe scripts/descent_driver.sh", while the
ledger's last row is 21:53:52Z on 10-1 (usage.jsonl tail: N1R_parables_songmap
turn 1, twice, 21:53:42 and 21:53:52). The commit's kill claim is true for
exactly the two 20:40:13Z twins it named, and no receipt names this driver's
fate; the 19:17-19:18Z double-fire cause stays unattributed with its host
still resident.

Falsifier: DATED_METERS rows dated 2026-10-01; kpi.jsonl frozen or shrinking;
fts_index.log stamped today; PIDs gone; a decision receipt for the meter gap.
Move (~40 min): write the meter-gap decision receipt (wire-pull or
accept-gap, either is legal, silence is not); land kpi rotation at the
mag/records.py:138 writer; at 13:05Z today verify the two 12:00/13:00Z
firings wrote non-zero logs and bank one line naming driver 44072's
disposition (kill or own-it-alive).

## Finding 5 (positive control): the engine topic-undefined input defect is fixed and the fix held

.zcode/workflows/ractor-engine.dwf.ts:29-31 declares topic required:true in
the args schema, and String(args.topic) is threaded into the breaker ask
(:226) and the synthesis ask (:293). This very run's asks carry the full
topic paragraph, so the path that once delivered the literal string
"undefined" (prior synthesis OWED) now delivers the subject. Registry rows
(memory/workflows/REGISTRY.jsonl, 58 rows) carry no topic field at all, so
the registry alone still cannot answer "what did this run ride"; that is a
minor OWED, not a defect of the fix.

## Blind spots (honest)

- I did not re-run the pytest census (the 4147-collected figure rides the
  AGENTS.md bullet and the prior synthesis's own run; not my check, not run).
- I did not verify balances (Nous ~$47.54, ledger ~$42) or re-sum the money
  window; I trusted the prior synthesis's triple-verified core and checked
  only the ledger tail and kpi size.
- My index_events greps are substring matches on exact case-sensitive names;
  a registration under a mangled name would evade them (path prefixes would
  not, the substring survives).
- The 110-file uncommitted tree was sampled (CURRENT, trails, DATED_METERS,
  attention, patrol logs), not exhaustively read; other in-window comm
  surfaces (queue/lanes/*/inbox.jsonl, elder surface) were not opened.
- WMI-class checks were one CIM query at ~10:52Z; transient state before or
  after that moment is not mine to claim.
- Driver 44072's aliveness says nothing about whether it is hung versus
  queue-drained; distinguishing them needs its log, which I did not read.

Filed by lens-communication, 2026-10-02. No em-dash bytes. The two
_taskquery*.ps1 stubs in this folder are this sitting's sealed instruments
(autoseal nonces 2158/2159), left in place deliberately.
