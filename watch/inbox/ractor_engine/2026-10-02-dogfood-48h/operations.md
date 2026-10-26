# OPERATIONS - dogfood 48h window (2026-09-30T20:00Z to 2026-10-02T11:00Z)

Lens: operations (dispatch shapes, fold integrity, commit races, silent
failures, cadence). Filed 2026-10-02 ~10:55Z. Read
watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md first and went beyond it;
nothing below re-derives its findings. Every check ran this sitting unless
marked not-run. No em-dash bytes.

## F1. Two thirds of the window's paid ledger was re-fire excess, and the
## executed twin fix addressed 4.5 percent of it

Command run this sitting (repo venv):
`./.venv/Scripts/python.exe -c` over memory/runs/hermes_burn/usage.jsonl
(236 rows, last ts 2026-10-01T21:53:52Z, schema cost_usd/prompt_tokens/
completion_tokens/reasoning_tokens). Output: total $37.7591 and 5,639,068
tokens, ALL 236 rows dated 2026-10-01, zero rows after 21:53:52Z.
Excess-after-first-copy per (id,turn) key: $25.5316 = 67.6 pct of the whole
ledger. Breakdown: A1_steer_antiforgery $21.0932 (49 fires 13:11Z-20:17Z,
each a paid claude-* turn $0.13-$0.65), B2_drift_rows_attribution $1.2330
(6 fires), C1_censorship $1.0582, T1W2 S5-S8 ~$1.02, the twins' 13 DUEL2_r2
keys ~$1.12, N1R $0.149. DUEL1_hidden_5 x46 and N1_parables_songmap x42
re-fired at $0.00 (89 rows zero-cost, ok=False). The RACTOR DOGFOOD commit
(e3c7d341c) acts on the twin slice ("$2.25 vs $1.09 real"); WAVE24
(43f50ed71, in-window, 21:41Z) already claimed the A1 root cause ("A1 x45
re-burn root-caused to one stale boolean") and tools/hermes_burn.py:203
carries the mtime-bypass comment. So the class produced THREE separate
one-organ patches (stale boolean; REFUSED terminal skip at :264-276;
pidfile on one script) while the underlying shape stands: _landed_skip at
tools/hermes_burn.py:197 is check-then-fire with no atomic claim, and the
twins proved the race AFTER the skip existed (13 keys doubled 21:39-21:53Z
with skip logic live, two interleaved consumers passing the same check).
Falsifier: an (id,turn) census showing excess under ~$3, or a lock/marker
file in hermes_burn.py making concurrent first-fire impossible. Move: add
an atomic claim (O_EXCL marker or lockdir per ask) at the fire path plus a
ledger-ingest doubled-key alarm, ~40 min.

## F2. The pidfile guard is inert against the CURRENT tree: the surviving
## driver predates it and holds no pidfile

CIM snapshot this sitting (powershell Get-CimInstance Win32_Process,
CommandLine -like *descent_driver*): exactly ONE real driver, PID 44072,
born 2026-10-01 17:31:24 local (21:31:24Z, the synthesis's third driver),
parent 50236 gone. `ls state/*.pid` shows only autodrain.pid (Sep 22) and
night_cadence.pid (Aug 28); state/descent_driver.pid DOES NOT EXIST. The
guard block (scripts/descent_driver.sh:12-25) passes when no pidfile
exists, so any genuine new launch double-drains alongside 44072 today; the
beats stay single only because queues are dry (driver.log tail: every ask
"skipped", "HERMES-BURN: PASS - 28/28 asks; ledger total $37.76", beat
cycle 922 at 10:52:08Z, ~50s cadence across 919-922, single-instance
rhythm). Honest instrument note: I briefly read my OWN tool shells as a
second driver (PIDs 8660, 47804->15620->58480->49424, parented by
ZCode.exe) because my command lines contain the string descent_driver;
the beat cadence and parent chain falsified it. Observer contamination is
the same mixed-instrument class the synthesis caught in the "~48s cadence"
line. Falsifier: a pidfile appearing from 44072 (impossible: its bash read
pre-guard bytes), or a second launch exiting 3 while 44072 lives (will not
happen: no pidfile to read). Move: bounce 44072 (touch DRIVER_STOP, wait
one cycle, kill, relaunch under the guarded script; verify pidfile written
and a second launch exits 3), ~20 min.

## F3. Guard pattern built once, never swept: 1 of 11 loop scripts

Command: `grep -l "pidfile|PIDFILE|pid_file" scripts/*.sh scripts/*.ps1`
returns ONLY scripts/descent_driver.sh. The long-running class in scripts/
with no guard: astra_convo_loop.sh, council_runner.py,
handoff_escalation_watcher.py, run_autorun_loop.py, run_ghost_loop.py,
run_stealth_driver.py, virtual_desk_loop.py, wave_driver.py, x_auth_loop.sh,
invisible_runner.vbs. Not all drain paid queues, but wave_driver.py,
run_stealth_driver.py and run_autorun_loop.py are the same drain-the-queue
shape that produced the twins. Stale pidfiles from dead loops still sit
unclaimed in state/ (autodrain.pid mtime Sep 22, night_cadence.pid Aug 28):
even the organs that once used pidfiles have no reclaim sweep. This is the
citation-lint disease again: a law lands in the organ that bit, zero sweep
across siblings. Falsifier: guards present in the listed files (grep above
says no), or evidence the other loops are single-instance by construction
(none seen). Move: sweep the pidfile guard (or a shared
tools/instance_guard.py) into the three queue-draining siblings and purge
or reclaim the two stale state/*.pid files, ~45 min.

## F4. OWED scoreboard: which prior-OWED items are live vs paid RIGHT NOW

STILL LIVE, verified this sitting: kpi.jsonl now 752,865,877 bytes (mtime
Oct 2 06:44 local, writer still appending; GREW past the synthesis's
748,222,017; 22,470 lines; rotation at mag/records.py:138 still absent);
NIGHT_CLOSE_20261002.md erratum unpaid (mtime unchanged Oct 2 01:14 local;
grep for erratum/1.0077/10.0031 returns nothing); commit-queue law from
2093ca518 still ticketed nowhere (grep "commit-queue|commit queue" over
watch/inbox/hermes_burn/TICKET_LEDGER.md and queue/todo.md: zero hits; the
ask's path memory/runs/hermes_burn/TICKET_LEDGER.md is stale, the file
lives at watch/inbox/hermes_burn/TICKET_LEDGER.md); the 23:32 EDT
invisible_runner launch and the T1W2 19:17-19:18Z double-fire cause remain
unattributed (my census adds the class was already active at 13:11Z:
A1/B2/C1 triples). PAID since the synthesis: the B2-244 census response
(watch/inbox/census_refresh_20261002.md is byte-solid: instrument, moment
2026-10-02T10:08Z, 4,147/496, both deltas attributed to named commits);
receipt INDEX registration (grep counts NIGHT_CLOSE|POSITION_CHANNEL|
model_garden = 9 rows in watch/inbox/INDEX.json, 34 in index_events.jsonl).
NEW WOUND in the freshest receipt: census_refresh_20261002.md stamps the
proof fire "2026-10-02T03:29:15Z" but schtasks /Query shows Last Run Time
10/2/2026 3:29:15 AM LOCAL EDT = 07:29:15Z (bracketed by commit e3c7d341c
at 07:31:54Z): the receipt stamps EDT as Z, a 4-hour lie in the morning's
flagship awareness artifact. Falsifier: an erratum banner in
NIGHT_CLOSE_20261002.md, a TICKET_LEDGER/todo row naming commit-queue, a
rotation receipt for kpi.jsonl, a log proving the patrol fire was truly
03:29Z. Move: one erratum sitting covering NIGHT_CLOSE + the census stamp
+ ticket the commit-queue law + kpi.jsonl rotation, ~45 min.

## F5. Dogfood census of the window's new instruments: wired vs built

Wired and self-firing: citation_lint (githooks/pre-push:24-25 runs it
exit-on-fail after the ratchet at :10; the prior synthesis self-ran it on
its own output). Engine topic fix HELD: .zcode/workflows/ractor-engine.dwf.ts
metadata declares topic required:true (lines 29-32) and THIS run rode a
real defined topic; morning gate re-checks live in
memory/workflows/REGISTRY.jsonl (10:38Z engine digest 04f898db351e PASS;
10:42/10:43Z game-mechanics-deep-dig PASS x2, both carrying G6-receipts
soft-warns). Built but NOT dogfooded in production: seed_seal (find for
*.seal returns only agents/pytest-tmp-10040 test fixtures, zero production
sidecars; grep -rln seed_seal over tools/ mag/ githooks/ returns only
mag/seed_seal.py itself: no caller, no verifier wired into any pipeline).
The 3c83da5b0 claim "enforcing flip stays operator-gated" is honest, but
the operations truth is the instrument has never signed or verified a real
organ. Patrol re-registration (e3c7d341c MOVE 2) is byte-true on the tree:
schtasks shows all four tasks direct (powershell -File census_patrol_daily,
fts_index_daily, improve_daily; venv python tools/leave_dispatcher.py), no
invisible_runner.vbs in any chain; caveat: only census has a post-fix
proof fire (Last Result 1 = its COLLECT-DRIFT alarm working), FTS/improve/
leave still show their 10-01 pre-fix Last Result 1 and next fire 08:00/
09:00 EDT today, so three of four re-registrations are UNPROVEN until
their first direct fire lands green. Falsifier: a production .seal sidecar
and a wired verifier call for seed_seal; three green direct-fire logs after
08:00/09:00 EDT would falsify the unproven caveat. Move: wire one
production seed_seal verify (shared_surface validate or pre-push leg) and
check the three patrol logs after 09:00 EDT, ~30 min.

## Cost of the window (dogfood Q3, hermes ledger slice)

$37.7591 total, all burned 2026-10-01, 5,639,068 tokens, 236 rows, last
row 21:53:52Z; 13h+ of driver cycles since then at zero marginal spend
(queues dry). Models: claude-sonnet-5.5 103 rows, claude-opus-5.5 85,
claude-fable-5.1 48. Not run this sitting: Nous balance check (~$47.54
claim), z.ai/grok lane costs (not in this ledger), per-commit dollar
splits beyond the ledger, pytest or SW1 suite reruns.

## Blind spots (honest)

- No process-history instrument exists: who launched driver 44072 (parent
  gone) and what launched the 13:11Z-20:17Z storm consumers is not
  recoverable from my snapshot; the T1W2 19:17Z and 23:32 EDT attributions
  stay open.
- I did not re-run the pytest census (4,147 claim), the SW1 suite, or any
  test battery; those numbers are cited from receipts, not re-derived.
- Dollar-per-commit attribution outside hermes_burn/usage.jsonl (z.ai
  salon/genetics/autopsy burns, grok lane) was not summed; the "$42 of
  $145" and "$47.54 Nous" figures are unverified by me.
- salon mesh, rib_swarm, water_computer dogfood depth not audited (only
  code_swarm's SW1-10 LANDED-with-test row seen in TICKET_LEDGER).
- The 110-file uncommitted working tree was not diffed file-by-file; I
  sampled (tools/code_swarm.py, handoff_escalation_watcher.py modified).

## Verification stamp

Ran this sitting: git log/show; schtasks /Query (list + /V on four tasks);
grep pidfile over scripts/*; ls/wc on logs/kpi.jsonl; grep on
githooks/pre-push; tail + grep TICKET_LEDGER (correct path), NIGHT_CLOSE;
find TICKET_LEDGER; sed descent_driver.sh:1-40; cat state/*.pid; driver
beat tail with a 55s re-read; CIM process snapshots x4 (one
observer-contamination near-miss documented in F2); python census of
usage.jsonl x4 (schema, window sum, doubled keys, excess); grep
hermes_burn.py skip/claim; grep INDEX.json/index_events.jsonl; find
*.seal; grep seed_seal callers; sed engine dwf.ts metadata.
