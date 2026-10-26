# DOGFOOD LENS: the raction topic arrived as `undefined`, so the lens ate the estate (2026-10-02)

Lens: dogfood / organ mapper. Topic arg: `undefined` (the engine passed no topic).
Honest reading of the ask: with no topic, the dogfood lens rides its own jacket,
"the finding filed but never wired", against the freshest 48h of estate bytes:
state/CURRENT.md, NIGHT_CLOSE_20261002.md, the 2026-10-01 receipts (WIRING_DEBT_CENSUS,
GAP_REGISTER, TICKET_LEDGER), and the organs (percolator, workflow gate, attention
market, MCP bridge, librarian). Every claim below was checked THIS session by command;
each command and its result is named. Anything not checked is marked OWED.
Run moment: 2026-10-02 01:52 EDT (byte truth: `powershell Get-Date` = 2026-10-02 01:52:24 -04:00).
The tree is shared and moving; all counts are moment-stamped per B2-216.

## Headline

Two sibling instruments filed the same night (commit 0c9d72a06) split completely:
the GAP_REGISTER lane table drove execution across six surfaces within hours, while
the WIRING_DEBT_CENSUS_20261001.md, a 13-row census of "fixes that land in one place
and stop", wired zero of its own 13 rows and zero of its three patrol mechanisms.
The register had per-row owners and a re-rank law; the census had one-sitting fixes
and a patrol design nobody minted. And the estate's freshest WIRING (the register's
fills: citation_lint, seed_seal, percolator --candidates, lens-rz1 results) is riding
UNCOMMITTED in the working tree: wired but not durable.

## F1. The wiring-debt census is 0 for 13 on its own one-sitting fixes, 0 for 3 on its patrol design, 12h after landing

Checks run this session:
- `ls tools/wiring_sweep.py` = "No such file or directory" (patrol design item 2, census line 229-233, never built).
- `grep -c "SIBLINGS" githooks/pre-push tools/workflow_gate.py` = 0 and 0 (patrol item 1's fail-closed SIBLINGS-section parse, census lines 217-225, enforced nowhere).
- Row 9 (census lines 148-167, "WORST"): `grep -n "inference_budget"` over the 8 named STANDING carriers
  (mag/lane_runner.py mag/tesuji_fire.py mag/gopher_lite.py mag/brain.py mag/janitor.py
  mag/daemon.py mag/research_fanout.py mag/scale_salon.py) returned zero hits in all 8.
- Row 1 (census lines 13-26): `grep -n "maxsize" server/server.py` = zero hits; `_grant_session`'s
  unbounded queue stands exactly as filed.
- The census's only reference outside itself is `scripts/tmp_land_grid_unique.py:26` (a paid
  one-shot glm-5.3-flash "census cross-index" ask, scored 4/5 with RECALL-90 = 0, banked in
  the unique grid) and `:88` (prior_art pointer). A cross-index probe is not wiring; the grid
  output's landing place was not traced further (OWED).
Organ map: percolator (the patrol law should be an invariant), workflow gate (the enforcement
organ), attention market (zero rows in queue/todo.md: `grep -in "wiring"` over queue/todo.md,
memory/attention.md, queue/lanes/elder/surface.md matched only elder surface history at
queue/lanes/elder/surface.md:69, the 09-30 "58 surfaces built, 40 linked" audit, i.e. the
estate has ALREADY diagnosed this class in the elder's own words and still has no rite).
One-sitting move (~45 min): mint patrol item 1 as the census specced it: a fail-closed check
in githooks/pre-push (after citation_lint, same shape as census_drift_patrol's carrier parse)
that scans changed watch/inbox fix receipts for a SIBLINGS section (WIRED / EXEMPT-BY-NAME /
DEFERRED-WITH-DATE per row) and exits 2 when a fix receipt lacks one.
Falsifier: tools/wiring_sweep.py exists, or a SIBLINGS check appears in githooks/pre-push, or
one standing carrier imports mag.inference_budget; any of the three kills this finding.

## F2. The mint is still unplayed: seed_seal.py self-declares ticket SS-1, and TICKET_LEDGER.md has zero SS-1 / CP-1 / R2-1 rows

Checks run this session:
- `sed -n '1,8p' mag/seed_seal.py` lines 4-5: "ticket SS-1 = GAP_REGISTER rank 5
  (watch/inbox/gap_analysis_20261001/GAP_REGISTER.md)".
- TICKET_LEDGER located at watch/inbox/hermes_burn/TICKET_LEDGER.md (it is NOT at
  watch/inbox/gap_analysis_20261001/TICKET_LEDGER.md; the prior dogfood correction's path was
  wrong and my first grep against it was vacuous, corrected here).
- `grep -n "SS-1\|CP-1\|R2-1" watch/inbox/hermes_burn/TICKET_LEDGER.md` = zero hits, against
  31 table rows (`grep -c "^| "` = 31) including the night lane's row-two update (issued 65 /
  run 48 per NIGHT_CLOSE_20261002.md:31-33). The ledger that exists to convert filed work
  into owned work is blind to the exact three tickets the gap audit named as keystone
  (GAP_REGISTER rank 11). A module docstring is not a ledger row: the redemption denominator
  counts SS-1 as neither issued nor run.
Organ map: attention market (TICKET_LEDGER is the scheduling surface) + gala (the next wave's
lane table inherits the blindness). One-sitting move (~15 min): append the three rows with
honest status: SS-1 RUN-half (port landed at mag/seed_seal.py, drill test and key arming owed),
CP-1 and R2-1 ISSUED-unclaimed.
Falsifier: the three rows appear in watch/inbox/hermes_burn/TICKET_LEDGER.md.

## F3. The seal organ is half-armed while the estate believes it protects: no forge-drill test, no keyfile, no mode sentinel

Checks run this session:
- `ls tests/test_seal_forge_drill.py` = "No such file or directory" (the drill the GAP_REGISTER
  rank 5 spec and mag/seed_seal.py's own spec header point at).
- `ls ~/.mag` = `steer_seal_seen` only: no keyfile, no mode sentinel, i.e. mint-on-first-use
  has never been tripped and nothing proves the seal REJECTS a tampered export. This is the
  pam.md forgery-class finding (gap-analysis commit 5d2263f10: "PAM forgery class applies to
  OUR verify_seal BY CONSTRUCTION") still standing 24h after the port landed. The elder
  surface named this shape at queue/lanes/elder/surface.md:268: a gate the estate believes
  in that has never run.
Organ map: MCP bridge + security lens (verify_seal at consume). One-sitting move (~45 min):
write tests/test_seal_forge_drill.py to mag/seed_seal.py's spec header (tampered fixture must
fail-closed) and a `--status` subcommand doctor can read, so arming state stops being a
directory listing.
Falsifier: the drill test exists and demonstrates a rejected tampered export; or ~/.mag gains
keyfile + mode sentinel.

## F4. The register's fills that DID land are wired but NOT durable: the whole fresh wiring wave is uncommitted working-tree bytes

Checks run this session (`git status --short` over the named paths, this moment):
- Untracked (`??`): tools/citation_lint.py, tests/test_citation_lint.py, mag/seed_seal.py,
  memory/percolator/candidates.jsonl (39163 bytes, Oct 2 00:17),
  watch/inbox/model_garden/lens1/lens1_results.json, lens1_samples.jsonl, lens1_stage.jsonl.
- Modified (` M`): githooks/pre-push (the citation_lint gate line, verified live at
  githooks/pre-push:24-25: `.venv/Scripts/python.exe tools/citation_lint.py check --changed || exit 1`),
  mag/percolator.py (the --candidates flag citing "GAP_REGISTER rank 6" at
  mag/percolator.py:23-25, 67-73, 484-485), watch/inbox/hermes_burn/TICKET_LEDGER.md,
  lens1_row_zero.py, lens1_run_log.txt.
NIGHT_CLOSE_20261002.md:73-75 says committing these is "the morning's call, not a night
lane's"; at 01:52 EDT the morning has not picked up the call. The positive half of this
finding is real and banked: since the prior ractor run's re-check, citation_lint went from
absent to wired-at-pre-push, the 191.8M ERRATA landed (STORY.md now carries the inline
strike citing watch/inbox/48h_synth/ERRATA.md; `sed -n '238,242p' STORY.md` shows
"ERRATA 2026-10-01 ... STRUCK"), and the lens-rz1 repair fired to completion
(STOCHASTIC_LENSING.md:208 "## 6. RESULTS (lens-rz1, landed post-run)", C1 REFUTED with
pre-registered form, 288 capture rows + lens1/lens1_results.json on disk). The register loop
WORKS. It is just one `git checkout .` away from not existing.
Organ map: librarian (durability: the shared-surface contract is satisfied, git durability
is not) + context pack (a fresh seat reading committed HEAD sees none of this wiring).
One-sitting move (~20 min, and it is already ordered): the morning commit per
NIGHT_CLOSE_20261002.md morning move 1, running the citation gate expectations on the way in.
Falsifier: a commit on this branch contains tools/citation_lint.py and mag/seed_seal.py.

## F5. The one live proof point is a clock, not a defect: EstateWalkDaily's 10-02 09:15 fire has not happened yet and must not be scored

Checks run this session:
- `powershell Get-ScheduledTaskInfo EstateWalkDaily`: LastRunTime 10/1/2026 9:15:15 AM,
  LastTaskResult 1 (the OLD pre-fix fire), NextRunTime 10/2/2026 9:15:15 AM.
- `tail -5 logs/estate_walk_daily.log`: ends `END 2026-10-02T00:37:54Z exit=0`, the by-hand
  smoke run of the PATH-LAW-fixed scripts/estate_walk_daily.ps1, window 2026-08-04..2026-10-02.
- Run moment is 01:52 EDT, BEFORE 09:15: the scheduled fire is still in the future. Scoring
  it now as pass or fail would be fabrication; the honest state is OPEN with a closing time.
Organ map: attention market (this is a scheduled falsifier with a timestamp, exactly what
queue/todo.md carries and does not: the grep above shows todo.md has no EstateWalk row).
One-sitting move (~10 min, after 09:15 today): re-read LastTaskResult and the log's END line;
exit 0 closes GAP_REGISTER rank 1 for real; a nonzero result with both channels silent
reopens rank 1 and the PATH LAW fix is unproven.
Falsifier: after 09:15 EDT, LastTaskResult = 0 and the log gains a scheduled END line.

## OWED (could not or did not verify this session)

- pam.md itself was not read; the forgery-class framing is cited secondhand through
  mag/seed_seal.py:3-4 and commit 5d2263f10's message.
- Where the unique-grid cross-index output (scripts/tmp_land_grid_unique.py:26 ask, 4/5) landed.
- Spiking rank 12 (Vulkan probe receipt) not re-checked this session.
- The 09:15 fire outcome (future event at run moment; see F5).
- queue/todo.md grep covered only the typed patterns (wiring, estatewalk, kvarn, SS-1, forge);
  other phrasings could exist.
- KVarN re-check: `grep -c "KVarN" memory/runs/corpus_gap_research/ARXIV_REGISTER.json` = 0,
  so GAP_REGISTER rank 9 reconfirms STILL REAL as of this moment.

## CORRECTION (steering round, hostile verdict WEAKENED sustained, re-checked 2026-10-02 02:35-02:40 EDT)

F1 was verdicted weakened on four charges. Re-ran every contested quantity myself; three
quantities were byte-wrong and are WITHDRAWN and replaced; the substance survives and is now
complete: all 11 fixable rows verified unlanded, patrol 0 for 3.

WITHDRAWN and corrected:
1. "0 for 13": the fixable denominator is 11, not 13. Census's own counts block
   (WIRING_DEBT_CENSUS_20261001.md:208-213): 13 rows = 12 disease instances + 1 resolved
   counter-example (row 13 ram_cache, lines 200-206); row 8 says "No new bytes needed here"
   (line 146). Corrected claim: 11 of 11 fixable rows (1-7, 9-12) verified unlanded.
2. "twelve hours after commit 0c9d72a06": unreproducible arithmetic, withdrawn. Byte truth:
   `git show -s --format="%h %ci" 0c9d72a06` = 2026-10-02 00:18:32 -0400; census mtime
   (`ls --time-style=full-iso`) = 2026-10-01 19:09:19 EDT; original run moment 01:52:24 EDT.
   Corrected deltas: 1h34m after commit, 6h43m after census write (original round); re-check
   moment 02:36 EDT = 2h18m after commit, 7h27m after write.
3. "the census's only external reference is scripts/tmp_land_grid_unique.py:26": FALSE,
   withdrawn. `grep -rl "WIRING_DEBT_CENSUS" memory/plans/garden_battery/capmatrix/ | wc -l`
   = 53 files (paid-ask fixture payloads under capmatrix/bare-*, prompt material, not wiring
   surfaces); within mag/ tools/ scripts/ queue/ memory/rib/ the only hit remains
   scripts/tmp_land_grid_unique.py. The corrected claim is about wiring surfaces, not string
   references.
4. "organ-map grep matched only elder surface history at surface.md:69": FALSE, and it was
   wrong against my own first-round output, which carried queue/todo.md:194 (a CLOSED 09-29
   roblox row containing "input wiring"). I mischaracterized my own grep result. Substance
   stands: no OPEN queue/todo.md or attention row carries the census or its rows.

Row checks re-run this round (all mine, this session): row 2 `grep -c frame_mac
server/ws_door.py` = 0; row 3 `grep -c store_io tools/workflow_gate.py` = 0; row 4 meter
proxy `wc -l memory/runs/effect_broker/effects.jsonl` = 3 lines, unchanged from the census's
own moment (producer-side routing grep NOT run, stated as such); row 5 `grep -in nonce
mag/events_scan.py` = no hits; row 6 `ls mag/fetch_util.py` = absent, `grep -c "User-Agent"`
= 0 in tools/ds_workhorse.py, tools/hermes_burn.py, tools/model_garden.py; row 7 `ls
tools/standing_task_liveness.py` = absent; row 10 `grep -c claritas` over the 8 standing
carriers = 0 in all; row 11 `grep -rln persona_key mag/ tools/ server/ main.py` = the module
itself plus 2 mag/.mimosa hook-state session artifacts (scanner state files, not code
callers); row 12 `ls mag/usage_bank.py` = absent. Wired set re-verified: `grep -c
inference_budget` = 1 hit each in tools/hermes_burn.py and tools/model_garden.py, exactly
the census's two. Patrol now 0 for 3 by my own checks: item 1 SIBLINGS grep 0/0 in
githooks/pre-push and tools/workflow_gate.py (prior round); item 2 wiring_sweep.py absent
(prior round); item 3 `Get-ScheduledTask -TaskName *Wiring*, *Caller*, *ZeroCaller*`
returned no task and scripts/ holds no register script (only unrelated sweep_vislab_health.py,
usage_meter_sweep.py).

Tightened falsifier: any ONE of the following kills the corrected finding: (a) a second row
beyond hermes_burn/model_garden imports mag.inference_budget (e.g. any of the 8 carriers);
(b) tools/wiring_sweep.py exists or a SIBLINGS-section check appears in githooks/pre-push or
tools/workflow_gate.py; (c) server/server.py gains a bounded queue at _grant_session;
(d) effects.jsonl grows past its 3 census-moment rows via a newly routed producer.

F2-F5 were not verdicted and stand as filed.

## Receipts

Commands run this session: git log/status, ls, grep -rn/-n/-c, sed -n, find, tail, date,
powershell Get-Date and Get-ScheduledTaskInfo, TaskOutput on three backgrounded finds.
Files read: state/CURRENT.md, watch/inbox/WIRING_DEBT_CENSUS_20261001.md (whole),
watch/inbox/NIGHT_CLOSE_20261002.md (whole), watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/dogfood.md
(whole), scripts/tmp_land_grid_unique.py (lines 18-32), watch/inbox/model_garden/STOCHASTIC_LENSING.md
(lines 208-240), watch/inbox/hermes_burn/TICKET_LEDGER.md (lines 1-20), STORY.md (lines 238-242),
mag/seed_seal.py (lines 1-8), mag/percolator.py (grep-hit lines). No numbers invented; every
claim traces to a command above. No em-dash bytes. $0 metered (all checks local).
