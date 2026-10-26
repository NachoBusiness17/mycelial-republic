# security.md - ractor lens: security (2026-10-02 dogfood-48h run)

Lens: security, lethal-trifecta frame (private data + untrusted content +
communication). Jacket: the gate that tests itself and nothing else. Filed
~06:55Z (02:55 EDT... local 06:55 EDT, 10:55Z). Prior synthesis read FIRST
(watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md, whole file); every
finding below is new beyond it or extends its OWED list with fresh bytes.
All checks run this sitting unless marked OWED. No em-dash bytes.

## F1. The citation-lint pre-push wiring is uncommitted: enforcement theater at history level

3c83da5b0's message claims "Citation lint LANDED ... changed prose
byte-checked at pre-push". The tool and tests are committed (git ls-files
lists tools/citation_lint.py, tests/test_citation_lint.py), but the one-line
hook wiring exists ONLY as dirty working-tree bytes: `git show
HEAD:githooks/pre-push | rg -c citation_lint` printed nothing (zero matches
in the committed hook), `git log --oneline -3 -- githooks/pre-push` names
f0768f3be, dffd32a72, 48f7f5ace (all pre-window; no window commit touched
the hook), and `git diff -- githooks/pre-push` shows the citation block as a
pure + addition (githooks/pre-push:11-25 in the working tree).
core.hooksPath=githooks (git config, this sitting), so THIS machine enforces
from the dirty file, but any fresh clone, any second machine, any
post-checkout sibling gets no citation gate at all. The gate file itself is
guarded by nothing: the violation ratchet covers mag/ and tools/ only
(githooks/pre-push:9-10), so hook edits ride unwatched. This is the prior
synthesis's receipts-only-theater class (its POSITION_CHANNEL proof) found
again one organ deeper: the estate's newest truth-gate is itself uncited in
history. Falsifier: a window commit carrying the citation bytes in the hook
(none exists; `git log -S citation_lint -- githooks/pre-push` would show it).
Move (~10 min): stage and commit githooks/pre-push with the next push; add
githooks/ to the ratchet's watch or name the gap in the OWED register.

## F2. A real TLS private key has been tracked in git since 08-19, below every gate's radar

`git ls-files memory/tls/` lists lan.crt AND lan.key; `rg -c "PRIVATE KEY"
memory/tls/lan.key` = 2 (real PEM key material; bytes not printed here); it
landed in 799ddb6fe (2026-08-19) whose own message says "LOCAL ONLY, not
pushed" - tracked is not local-only. .gitignore carries no memory/tls rule
(rg over .gitignore, this sitting). The pre-push secret gate cannot see it
by design: blocking tier is "specific provider shapes only"
(githooks/pre-push:387-388), it scans --changed only (:390-391), and the
hook's own comment names "known-true positive memory/tls/lan.key detected
critical" (:392-393) while configs/secret_gate_baseline.json (read whole)
holds no acceptance for it - the key passes because it is unchanged and not
provider-shaped. Dogfooded the gate on the current dirty tree exactly as
the hook runs it: `.venv/Scripts/python.exe tools/secret_gate.py --changed
--baseline configs/secret_gate_baseline.json` = 122 files scanned,
critical=0 high=0 blocking=0, exit 0, results banked at
watch/inbox/secret_gate_results/changed_20261002T105211Z.json. The only
remote is a local backup repo (`git remote -v` = local
C:\Users\foste\Documents\projects\Mag-backup.git), so exposure today is
same-machine; the failure is structural: the gate that tests everything
cannot test its own history, and a five-week-old key rides every backup.
Falsifier: the file being placeholder bytes (false: 2 PRIVATE KEY markers)
or a gitignore rule existing (none). Move (~20 min): git rm --cached
memory/tls/lan.key lan.crt, add memory/tls/ to .gitignore, rotate the LAN
pair; history purge is the operator's separate call (the 09-26 purge
machinery exists).

## F3. seed_seal: one retroactive seal on the OLDER seed, the newer seed bare, zero consumers

SS-1 closed as "seed_seal Ed25519 LANDED" (3c83da5b0). Byte truth: key
minted state/keys/seed_seal_key (64 B, 2026-10-02 00:07:15 local), exactly
ONE sidecar written - watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.seal
(748 B, 00:10:34) - while the NEWER arc seed on disk,
arc_seed_c424b80a-5f44_f69d1c0fd1073f55.md (2026-09-19), has no seal
(directory listing, this sitting). Coverage: 1 of 2 seeds, 0 consumers: rg
for seed_seal across the repo (excluding watch, memory/runs) hits only
mag/seed_seal.py, tests/test_seed_seal.py, catalog rows, AGENTS.md, and
memory/corpus/LINKS.jsonl - no production call site. The module's own
docstring confesses the dormant gate (mag/seed_seal.py:36-40): "nothing in
mag/arc_seed.py or any consumer REFUSES an unsealed/forged seed yet."
Tamper-evidence today protects nothing that anything reads. Key custody is
sound (state/ gitignored, .gitignore:40; hex-seed file never commits).
Falsifier: a .seal for c424b80a or any non-test verify_seed() caller (none
on tree). Move (~30 min): seal the c424b80a seed, add one flag-guarded
verify_seed() at the arc_seed consume site, then ask the operator for the
enforcing flip.

## F4. The pidfile guard is non-atomic and I beat it 21 times in 40 simultaneous pairs

The twin-kill fix (e3c7d341c, "PIDFILE GUARD installed") reads
scripts/descent_driver.sh:13-22: `[ -f "$PIDFILE" ]` check, then a plain
`echo $$ > "$PIDFILE"` at :22 - check-then-write with no O_EXCL, no
noclobber, no mkdir lock. I reproduced the stanza verbatim in a sandbox
(.venv/Scripts/python.exe watch/inbox/ractor_engine/2026-10-02-dogfood-48h/
_race_repro.py, bash children spawned with CREATE_NO_WINDOW per the win32
law): pairs=40 both_proceeded=21 at_least_one_refused_exit3=19. More than
half of simultaneous launches BOTH pass the guard - the exact same-second
twin class it was installed to kill. Honest caveat: the sandbox holds the
pidfile 0.25 s and compresses contention; the non-atomicity itself is
byte-visible regardless. Sibling sweep: rg pidfile|PIDFILE over scripts,
tools, mag hits only scripts/descent_driver.sh and mag/lane_runner.py - the
other queue-drainers (tools/hermes_burn.py, tools/ds_workhorse.py
invocation sites) carry no second-entry guard, and the T1W2 19:17-19:18Z
double-fire that PREDATES the twins is still unattributed (prior synthesis
OWED; no new attribution found this sitting), so at least one other
double-fire door remains unnamed. Falsifier: rerun the repro against an
atomic (mkdir/noclobber) guard and observe both_proceeded=0. Move (~30
min): swap to `mkdir state/descent_driver.lock || exit 3` with trap rmdir,
sweep the drainer class for the same guard.

## F5. invisible_runner.vbs survives as an unattributable hidden-exec primitive; the dark-patrol fix covered 4 of 10+ red tasks; the OWED list is still live

scripts/invisible_runner.vbs (read whole, still on tree, mtime 09-30):
line 27 runs `cmd /c <first-arg>` with a hidden window; lines 28-29 write
the exit code to %TEMP%\invisible_runner_rc.log via CreateTextFile(...,
True) = OVERWRITE, no timestamp, no command line, no attribution - one
overwritten temp file is the entire audit trail of a silent-execution
primitive any process can invoke. Zero scheduled tasks reference it now
(PowerShell sweep over all task actions, this sitting) - the e3c7d341c
re-registration claim is byte-true - but the 23:32:51 EDT 10-01 launch is
STILL unattributed: rg for invisible_runner across watch/ memory/ queue/
hits only the ractor-topic lens files and file indexes, no naming receipt.
The four re-registered patrols: MagCensusPatrolDaily ran 10-02 03:29 local
(the hand-fired proof; exit 1 = the COLLECT-DRIFT the census refresh
answered, per AGENTS.md B2-246 law), FTS/Improve/LeaveProtocol last ran
10-01 red, next fire today 08:00-09:00 local (current time 06:48 EDT, so
post-fix greenness UNVERIFIED - named, not guessed). Outside the fix
entirely, still carrying 10-01 red LastResults: MagGapSentinelDaily=1,
MagTipWitnessDaily=2, MagXRadarDaily=2, plus key_law audit=1,
lane_supervisor probe=1, estate_walk=1 (schtasks, this sitting) - the
same dark-patrol disease, six sibling organs left unswept. OWED list live
on the tree right now: logs/kpi.jsonl GREW 748,222,017 -> 752,865,877
bytes between the prior synthesis and 06:44 today, sole writer
mag/records.py:138, rotation still unpaid; NIGHT_CLOSE_20261002.md mtime
still 05:14:18Z = the erratum sitting still unpaid. Falsifier: a receipt
naming the 23:32 launch (none found), or any task still pointing at the
vbs (none). Move (~15 min + one 09:30 check): make the vbs append a jsonl
audit line (timestamp, cmdline, rc) or delete it; after 09:30 local,
re-query the seven red tasks and file which stayed red.

## Dogfood scoreboard (the five questions, this lens's slice)

Q1 byte-true vs theater: byte-true on tree = patrol re-registration
(schtasks bytes), seed_seal module+key+one seal, citation tool+tests,
engine gate rows (memory/workflows/REGISTRY.jsonl tail: ractor-engine
PASS, digest 04f898db351e at 10:38Z today). Theater-at-history = the
citation hook wiring (F1). Blind-by-design = secret gate vs the tracked
key (F2). Window receipt dirs ARE registered: rg counts 21
model_garden|fillball|gap_analysis_20261001 rows in watch/inbox/INDEX.json
(honest negative; the synthesis's unregistered-receipt class does NOT
extend to the window's directories).
Q2 unwired organs: verify-consumer absent + second seed unsealed (F3);
guard class porous and unswept (F4); six red tasks outside the four-task
fix (F5); citation lint covers changed prose only, .jsonl data excluded by
design (AGENTS.md Citation lint bullet).
Q3 cost: not re-derived this sitting (the prior synthesis triple-verified
the night's money core; re-summing would re-derive it). OWED for any lens
that wants per-commit dollars: memory/runs/hermes_burn/usage.jsonl +
watch/inbox/hermes_burn/TICKET_LEDGER.md.
Q4 OWED still live: kpi.jsonl (grew, F5), NIGHT_CLOSE erratum (mtime
unchanged, F5), 23:32 launch (unattributed, F5), T1W2 cause (unattributed,
F4). Engine topic-undefined fix: HELD - this run's lens ask carries the
topic text verbatim ("DOGFOOD THE ESTATE'S PAST 48 HOURS...") and
.zcode/workflows/ractor-engine.dwf.ts:141 interpolates String(args.topic)
into every lens ask; no undefined arrived.
Q5 dogfooded vs built: dogfooded live = the engine itself (gated,
registered, topic fix verified by this very run), the secret gate (I ran
it on the 122-file changed set: exit 0, 33.6 s), the pidfile guard (I
falsified it, F4). Built-not-fired = seed_seal beyond one retroactive seal
(F3), the citation wiring at history level (F1).

## Blind spots (honest)

- tools/secret_gate.py and tools/citation_lint.py rule internals unread;
  I relied on the hook's contract comments, the baseline bytes, and live
  runs of both gates.
- No WMI or process-table read this sitting: whether any descent driver is
  alive RIGHT NOW is unverified (the commit says twins killed).
- The untrusted-content leg of the trifecta (corpus/steal house, chan
  rows, the librarian's 61 primaries, the 46 unrelated Gutenberg
  transcripts) was not audited for injection flows into model prompts;
  only seed and catalog surfaces were touched.
- Task exit-code semantics per script unread: exit 1 from a patrol may be
  a designed signal (census COLLECT-DRIFT is), so "red" above means
  nonzero, not necessarily broken.
- No admin USN journal query (the F1 pre-close mtime question stays with
  the prior synthesis); NTFS mtimes only.
- Per-commit dollar conversion (Q3) not attempted.

## Verification stamp (commands run this sitting, 06:20-06:55 EDT)

git config --get core.hooksPath; git log/--show/--diff/--ls-files/--remote
as quoted inline; rg over .gitignore, seed_seal, pidfile, invisible_runner;
schtasks //Query + Get-ScheduledTask/Info sweep (script banked:
_taskquery.ps1); Get-Item sizes/mtimes (kpi.jsonl, NIGHT_CLOSE, vbs, seal,
keys); secret_gate --changed live run; TOCTOU repro (_race_repro.py, 40
pairs); Read of githooks/pre-push (whole), scripts/invisible_runner.vbs
(whole), scripts/descent_driver.sh (whole), mag/seed_seal.py:1-80,
configs/secret_gate_baseline.json (whole), SYNTHESIS.md (whole),
state/CURRENT.md (whole). Not run: full pytest, WMI, USN, per-commit cost
re-sum, the six sibling patrol scripts by hand. Cleanup: _race_sandbox
removed; _race_repro.py and _taskquery.ps1 kept as instruments.

Filed by the security lens. Banked at
watch/inbox/ractor_engine/2026-10-02-dogfood-48h/security.md.
