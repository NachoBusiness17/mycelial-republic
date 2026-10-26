# BREAK-SECURITY pass - the security lens report, byte-checked against the estate

Ractor: ractor_engine, hostile second pass on lens: security. Topic:
`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`. Every check below was
executed this sitting, 2026-10-01 ~23:00-23:55 EDT. Laws held: no fabrication
(unverifiable items are OWED, never asserted), no em-dashes, path:line
citations, commands named exactly as run.

Input note: the ask's JSON was truncated mid-F4. The lens's own banked
write-up (`watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/security.md`)
carries FIVE findings; F5 (rank-1 dogfood) is verdicted from that write-up
and every F5 byte-check was re-run here independently.

## Verdicts

| id | verdict | one-line reason |
|---|---|---|
| F1 steer_seal warn-default | WEAKENED (survives corrected) | Host state and live steering path confirmed unarmed, but "every steer permit" is overbroad (field_experiment runs its own enforce+keyfile lane) and the requested forge drill already exists in tests/test_steer_seal.py |
| F2 verify_seal PAM class | CONFIRMED | Generator source re-read line-by-line, zero .seal sidecars in bounded search, seed_seal and forge-drill absent, pam.md:65/:89 byte-exact, TICKET_LEDGER SS-1/CP-1/R2-1 grep = 0 |
| F3 register = unverified directive bus | CONFIRMED (strengthened) | Every cite byte-exact; decay began 3m45s after landing (earlier than the lens's 6m15s cite); a09 row-1 OVERCLAIM re-proven from the commit message and a zero-hit grep; no watcher; no amendment; register decayed TWICE (rank 1 content too) |
| F4 scheduler = unpinned persistence primitive | CONFIRMED (upgraded to census) | All TEN Estate* tasks enumerated and their Task To Run pulled: 10/10 operator context, 10/10 executing from the repo-writable tree, 0/10 integrity-pinned; 4/10 red right now |
| F5 rank 1 fixed but alarm-blind | CONFIRMED (move sharpened) | Script bytes, log tail, never-fired alarm grep, and schtasks state all confirmed; correction: a LastTaskResult watcher EXISTS but its "Mag*" filter excludes every Estate task, so the fix is one string, not a new watcher |

## F1 - WEAKENED (survives corrected)

Confirmed halves (re-run this sitting):
- `mag/steer_seal.py:83-102`: resolve_mode chain explicit > env > sentinel,
  line 102 is a bare `return "warn"`. `:21` names the fullwidth-GO fold; `:65`
  carries "unverified-warn" in the authority enum.
- `ls -la ~/.mag/`: contains ONLY `steer_seal_seen/` (created Oct 1 14:29).
  No `steer_seal_key`, no `steer_seal_mode` sentinel.
- `grep -rnI "MAG_STEER_SEAL_MODE" mag tools scripts configs githooks`:
  hits only inside `mag/steer_seal.py` itself (:15, :84, :90). Nothing on the
  host sets the env or the sentinel.
- Live consumer confirmed: `mag/hermes_steering.py:270` calls
  `steer_seal.admit_text(args.nudge)` with NO mode arg (context :262-274:
  unsealed permit passes with a logged warning in warn mode, refused exit 2
  in enforce). GAP_REGISTER.md:78 (rank 5) is accurate as written.

What breaks the wording: the finding says "every steer permit on this host is
consumable with zero cryptographic verification". False as written:
`tools/field_experiment.py:516-520` mints its own keyfile
(`ss.write_keyfile(keyfile, key, force=True)`) and calls
`ss.admit_text(..., mode="enforce", keyfile=keyfile, ...)`, so that lane
refuses unsealed permits cryptographically. The corrected claim: the live
steering surface (`mag/hermes_steering.py` cmd_steer) and the default gate
state are unarmed; one $0 experiment lane brings its own key.

Move correction (the lens's move is largely redundant): `tests/test_steer_seal.py`
already exists with 9 drills including forged-MAC rejection (:66), replay
rejection (:85), missing-keyfile-fails-closed-in-enforce (:148), and the
fullwidth-GO case the lens wanted asserted (:183-187:
`ss.classify("\uff27\uff2f") == "permit"` under NFC, folds only under NFKC).
The register's rank 5 scopes the MISSING drill to the PAM-class verify_seal
and is accurate; a new `tests/test_seal_forge_drill.py` against steer_seal
would rebuild existing coverage. The genuinely missing halves: the operator
sentinel flip, and the verify_seal red test (F2's move).

## F2 - CONFIRMED

- `tools/seed_v2.py:776-792` re-read this sitting: generated verify_seal
  resolves `root = Path(__file__).resolve().parent` (:780), reads
  `MANIFEST.sha256` from that same directory (:782), compares sha256 only,
  exits 0 when nothing drifted (:792). Verifier, manifest, and payload share
  one writable trust domain. By construction, as the lens said; no forgery
  was executed by the lens or by me.
- .seal sidecars: `git ls-files | grep -i "\.seal$"` = 0; `find watch state
  corpus memory/runs/mickey17_v2 -name "*.seal"` = 0. Bound stated: the
  full-tree find was aborted (hundreds of permission-locked pytest dirs);
  the search covers every git-tracked file plus the dirs pam.md names.
- `mag/seed_seal.py` ABSENT; `tests/test_seal_forge_drill.py` ABSENT;
  seal-named test files on disk: test_kv_seal.py, test_md_record_seal.py,
  test_steer_seal.py only.
- `watch/inbox/localfirst/pam.md:65` = "## The estate port: Ed25519-signed
  arc-seed export (the seed-seal slot)"; `:89` = "Ed25519 signature, and
  fail closed to UNVERIFIED". Both byte-exact.
- `grep -cE "SS-1|CP-1|R2-1" watch/inbox/hermes_burn/TICKET_LEDGER.md` = 0.
  The file exists (row-one census sections present); the three tickets do not.

## F3 - CONFIRMED, strengthened

- Register cites byte-exact: GAP_REGISTER.md:5-6 (directive mandate), :13-15
  (a09-a14 produced-no-files + amend-don't-rewrite law), :20-22 (only 5
  byte-checked quotes), :237 (negative finding).
- mtimes (ls -la --time-style=full-iso, EDT):
  GAP_REGISTER.md 18:41:58.06; a11-build-queue.json 18:45:43.97 (3m45s
  after landing); a14-coverage.json 18:48:13.57 (6m15s); a09-balls.json
  18:49:19.53 (7m21s); a10-drops.json 18:53:47.30 (11m49s);
  a12-commits.json 18:54:58.76 (13m00s). The lens's "decayed within seven
  minutes" is TRUE and conservative: the first unmerged lane landed under
  four minutes after the register. All of a09-a15 on disk, as claimed.
- a09-balls.json row 1 re-proven end to end: `git log --format=%B -n 1
  2093ca518` contains "port amends the banked abliterate P1 probe with
  judge channel and arm metadata"; my `grep -inE "judge|arm"
  tools/abliterate_p1_probe.py` returned ZERO hits. The OVERCLAIM rides the
  commit message against the file on disk, byte-true.
- No enforcer: `grep -rlnI "gap-analysis-of-the-estate" mag tools scripts
  githooks` = 0 hits. And the amendment has not happened:
  `ls watch/inbox/gap_analysis_20261001/` holds only GAP_REGISTER.md
  (16,660 bytes, mtime unchanged 18:41).
- NEW, strengthens F3: the register decayed TWICE. Its rank-1 row (:74,
  "repeats 10-02 09:15 with the same relative-path defect") went stale the
  same evening: scripts/estate_walk_daily.ps1 was rewritten with absolute
  paths (:11) and smoke-proved (see F5), landing in commit 5d2263f10. A
  directive bus that decays in minutes on coverage and in hours on content.
- NEW, resolves the lens's timezone blind spot: GAP_REGISTER.md:12 stamps
  the poll "~18:30Z", but the eight merged lanes landed 18:10-18:32 EDT
  (= 22:10-22:32Z). A literal 18:30Z poll (14:30 EDT) predates every input
  and contradicts the register's own "Inputs: 8 sibling lane audits, read
  in full". The only consistent reading: the poll was ~18:30 EDT = 22:30Z;
  the register's Z label is wrong by 4 hours (same skew at :244 "18:37Z").
  The landed-after-poll conclusion holds; the stamp is a mislabel, a
  phantom-citation cousin inside the register itself.

## F4 - CONFIRMED, upgraded from 3-of-~10 to census

`schtasks /Query /FO CSV | grep -i estate` enumerates TEN tasks: Estate
Cooker, Estate FullScan, Estate Gopher, Estate KeyAudit, Estate
LaneSupervisor, Estate Librarian, Estate Ratchet, Estate Spine Index,
Estate StealthSweep, EstateWalkDaily. I pulled Task To Run + Run As User
for all 10 (`schtasks /Query /TN <name> /V /FO LIST`):

- ALL 10 run as `Run As User: foste` (operator context).
- ALL 10 execute from the repo-writable tree: repo .ps1 scripts (WalkDaily,
  Ratchet), repo venv python running repo modules (KeyAudit
  `python -m mag.key_law --audit`, FullScan, Librarian, Spine Index), or
  system python with relative repo-module args (Cooker `mag\cooker.py fire
  --due`, LaneSupervisor `mag\lane_supervisor.py probe`, StealthSweep
  `tools\stealth_sweep.py`).
- Both PowerShell tasks carry `-ExecutionPolicy Bypass`.
- ZERO integrity pins anywhere: no sealed copy, no hash check, no
  out-of-band digest. The register, read in full, has no row modeling task
  integrity; only rank 1 / fill 1 touch the scheduler at all (for the
  silent-alarm and relative-path defect).
- NEW: 4 of 10 tasks are red RIGHT NOW (Last Result 1): EstateWalkDaily
  (10-01 09:15), Estate Ratchet (10-01 09:45), Estate KeyAudit (10-01
  09:45), Estate LaneSupervisor (last ran 9/28, Next Run N/A). The lens
  knew about one.
- Honesty correction (my own hypothesis, killed): the three relative-path
  actions are CWD-safe, all three carry `Start In:
  C:\Users\foste\Documents\projects\local_sovereign_agent` (Cooker and
  StealthSweep Last Result 0). The live exposure is integrity, not CWD.

The lens's OWED (inventory not enumerated) is closed: the census is done
and the class claim holds at 10/10.

## F5 - CONFIRMED, move sharpened

- `scripts/estate_walk_daily.ps1`: absolute `$repo` at :11, PATH LAW
  comment :5-10 naming the System32-CWD cause, alarm at :19-21 and END at
  :23 both INSIDE the script: any pre-parse failure (repo moved, script
  deleted, venv gone) reproduces red-AND-silent by construction.
- `tail -2 logs/estate_walk_daily.log`: "END 2026-10-02T00:37:54Z exit=0"
  (UTF-16LE on disk): the smoke run was success-path only.
- Alarm never fired: `grep -rlnI "ESTATE-WALK-BAKE-FAILED"` over scripts,
  logs, memory/attention.md, memory/trajectory/steps.jsonl, and the lanes
  dir hits only the script itself, trajectory steps (old relative-path
  step :36579 of 2026-09-29, plus tonight's repair steps :41383+), and the
  two a08 lane files (claim byte-exact at a08-48h-synth.json:27). Zero hits
  in memory/attention.md. The fill-1 injected-failure requirement has never
  been executed.
- schtasks this sitting: EstateWalkDaily Last Result 1, Status Ready,
  Next Run 10/2/2026 9:15 AM: the fix awaits its live proof fire. The
  register's rank-1 row is stale exactly as the lens said.
- SHARPENING: "Nothing watches LastTaskResult" is imprecise. A fleet task
  doctor EXISTS at `scripts/census_patrol_daily.ps1:115-128` (docstring at
  :115-119 names "a failure nobody watched") and reads LastTaskResult at
  :128, but its filter is `Get-ScheduledTask -TaskName "Mag*"` (:126),
  which structurally excludes all ten Estate* tasks. The estate built the
  exact instrument and pointed it at the wrong prefix. The one-sitting move
  is therefore: widen the doctor's prefix to cover Estate* and run the
  injected-failure drill. One string plus a drill receipt, cheaper than a
  new watcher.

## Dogfood verdicts on the register (the topic's test)

- rank 1: FIXED IN BYTES, pending live proof (misranked as open; row stale).
- rank 2: still real. `queue/lanes/elder/inbox.jsonl` = 0 bytes, mtime
  2026-09-04 (stat this sitting).
- rank 3: still real. `tools/citation_lint.py` absent.
- rank 4: still real. `watch/inbox/48h_synth/ERRATA.md` absent;
  STORY.md:240 still carries "191.8M tokens spent";
  `grep -c "191" watch/inbox/frontier_olm_20260928/DIGEST.md` = 0.
- rank 5: still real on the host (~/.mag keyless, no sentinel); the row's
  wording is accurate (drill scoped to verify_seal).
- rank 9 (half): still real. `grep -c "2606.03458"
  memory/runs/corpus_gap_research/ARXIV_REGISTER.json` = 0.
- rank 11: still real. TICKET_LEDGER grep = 0 (see F2).
- ranks 6, 7, 8, 10, 12: NOT CHECKED by me (accuracy/ops/econ scope).
- The register's five byte-checked quotes: re-run this sitting, all five
  return grep-cF = 1 (a06-spiking, a08 x2, a07, a05 lanes). The register's
  :20-22 claim is TRUE. This closes the lens's blind spot 5.
- Meta-gap verdict: the register's "MINED-NEVER-SCHEDULED dominant" holds
  for width; security-wise its meta-gap 4 (GATES LIVE BUT UNARMED) is
  3-of-4 still open (steer_seal host state, verify_seal, SAELIS untested
  by me = OWED; EstateWalkDaily fixed). The classes the register missed:
  register-decay-unwatched (F3) and scheduler-integrity (F4), plus
  tonight's third instance of the same disease: the patrol doctor trusts
  its own "Mag*" filter while four Estate tasks sit red and unwatced.

## OWED (not done, not guessed)

- No PAM forgery was executed (by the lens or by me); the hole is by
  construction only.
- The .seal search is bounded (git-tracked files + watch/state/corpus/
  mickey17-runs), not the whole tree (locked pytest dirs abort full finds).
- The four red Estate tasks' exit-1 causes are unexamined; a daily audit
  that exits 1 with zero consumers is itself silent-red, but the causes
  are unverified.
- Whether `scripts/garden_battery_local_profiles.py` uses steer_seal beyond
  its name reference: no admit/mode lines found (grep), call site not read.
- Ranks 6, 7, 8, 10, 12 unchecked (other lenses' scope).
- git status this sitting: 54 modified + 167 untracked = 221 porcelain
  lines (the lens said ~60 modified off the session-start snapshot; both
  moments differ, snapshot law applies).

## Commands run this sitting (exact)

- `ls -la ~/.mag/`
- `grep -rln "steer_seal" mag tools scripts tests` (consumers)
- `grep -rnI "MAG_STEER_SEAL_MODE" mag tools scripts configs githooks`
- `stat -c '%y %n' watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`
- `ls -la --time-style=full-iso memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/`
- `git ls-files | grep -i "\.seal$" | wc -l`; `find watch state corpus memory/runs/mickey17_v2 -name "*.seal"`
- `ls mag/seed_seal.py tests/test_seal_forge_drill.py`
- five `grep -cF "<quote>" <lane>.json` re-runs (register :226-233)
- `grep -cE "SS-1|CP-1|R2-1" watch/inbox/hermes_burn/TICKET_LEDGER.md`
- `schtasks /Query /TN <each of 10 Estate tasks> /V /FO LIST`
- `git log --format=%B -n 1 2093ca518`; `grep -inE "judge|arm" tools/abliterate_p1_probe.py`
- `ls watch/inbox/48h_synth/ERRATA.md`; `grep -n "191.8" watch/inbox/48h_synth/STORY.md`; `grep -c "191" watch/inbox/frontier_olm_20260928/DIGEST.md`
- `stat -c '%s %y' queue/lanes/elder/inbox.jsonl`; `grep -c "2606.03458" memory/runs/corpus_gap_research/ARXIV_REGISTER.json`; `ls tools/citation_lint.py`
- `grep -rlnI "ESTATE-WALK-BAKE-FAILED" scripts logs memory/attention.md memory/trajectory/steps.jsonl watch/inbox/gap_analysis_20261001 <lanes dir>`
- `grep -rlnI "LastTaskResult" mag tools scripts`; `sed -n '108,135p' scripts/census_patrol_daily.ps1`
- `grep -n "seed-seal slot|fail closed to UNVERIFIED" watch/inbox/localfirst/pam.md`
- `git status --porcelain | wc -l` and split by status
- `tail -2 logs/estate_walk_daily.log`
