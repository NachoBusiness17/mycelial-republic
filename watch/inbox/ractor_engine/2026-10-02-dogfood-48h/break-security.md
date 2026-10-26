# break-security: hostile second pass on the security lens (ractor dogfood 48h)

Sitting: 2026-10-02T11:08Z to ~11:25Z (window close 11:00Z overshot by the pass
itself). Lens under attack: watch/inbox/ractor_engine/2026-10-02-dogfood-48h/security.md.
Law held: every claim below is something I read or ran this sitting; anything
unverifiable is marked OWED. No em-dash bytes.

## Instruments fired (exact commands, win32, no state mutated except this file)

- `git show HEAD:githooks/pre-push | rg -n citation_lint` (no match), `git log -3 -- githooks/pre-push`, `git log -S citation_lint --oneline -- githooks/pre-push` (empty), `git config core.hooksPath` (githooks), `git status --porcelain` on the gate files, `git show 3c83da5b0:AGENTS.md | rg -n "Citation lint"` (no match), `git log -1 -- tools/citation_lint.py`
- `git ls-files memory/tls state/keys`, `git log --follow -- memory/tls/lan.key`, `git show dffd32a72:githooks/pre-push | rg -n lan.key` (hit, :317), `git show HEAD:githooks/pre-push | rg -n lan.key` (hit, :378), `git merge-base --is-ancestor 799ddb6fe local/run-beta1-factory-audit-20260914` (true), `git remote -v`
- `rg -c "PRIVATE KEY" memory/tls/lan.key` (2), `wc -c/-l` (1675 B, 27 lines, BEGIN x1; content never printed)
- `.venv/Scripts/python.exe tools/secret_gate.py --changed --baseline configs/secret_gate_baseline.json` (exit 0, 135 files, critical=0 blocking=0), `.venv/Scripts/python.exe tools/secret_gate.py --full memory/tls/lan.key memory/tls/lan.crt` (exit 1, critical=1 blocking=1, PRIVATE-KEY-BLOCK masked). Note: the lens's invocation shape "secret_gate --changed" is not the real CLI (bare `check` arg is parsed as a PATH and exits 2 scanner error, reproduced); the verdict it reported matches the correct invocation, so its conclusion stands but its command cite was malformed.
- `.venv/Scripts/python.exe tools/citation_lint.py check --changed` (exit 1, blocking=3, warns=36)
- `.venv/Scripts/python.exe watch/inbox/ractor_engine/2026-10-02-dogfood-48h/_race_repro.py` (pairs=40 both_proceeded=26 at_least_one_refused_exit3=14)
- WMI `Win32_Process` sweeps at 11:09Z, 11:10Z, 11:11Z; `cat state/descent_driver.pid` (absent); `tail` of memory/runs/hermes_burn/driver.beat (cycle 945 at 11:10:52Z) and driver.log; `rg -c "2026-10-02T11:1" memory/runs/hermes_burn/usage.jsonl` (zero rows)
- `Get-ScheduledTask` action sweep for invisible_runner (zero refs) plus `Get-ScheduledTaskInfo` over the Mag*/Estate* family
- PowerShell on logs/kpi.jsonl (753,324,704 B, no rotation siblings), NIGHT_CLOSE_20261002.md LastWriteTimeUtc (2026-10-02T05:14:18.9033Z), %TEMP%\invisible_runner_rc.log (content 1, mtime 06:20:49Z) and invisible_runner_rc.bak-1002 (content 7, mtime 06:01:18Z)
- `rg -ln "commit-queue|commit_queue|commit queue"` over queue/, memory/law, state, watch/inbox, HANDOFF_MAG_AGENT_TODOS.md
- Reads: githooks/pre-push (1-60, 360-409), .gitignore (whole), configs/secret_gate_baseline.json (whole), scripts/descent_driver.sh (whole), scripts/invisible_runner.vbs (whole), mag/seed_seal.py (whole), mag/records.py:120-150, _race_repro.py (whole), NIGHT_CLOSE_20261002.md (whole), ractor-topic/SYNTHESIS.md:55-139, ractor-topic/communication.md:35-63, .zcode/workflows listing, rg topic over .zcode/workflows/ractor-engine.dwf.ts

## Verdicts

### F1 citation-lint pre-push wiring is working-tree only: CONFIRMED

- HEAD hook carries no citation_lint (rg no-match); `git log -S citation_lint -- githooks/pre-push` is empty; the block sits at githooks/pre-push:11-25 of the dirty file (comment :11-23, invoke `tools/citation_lint.py check --changed || exit 1` at :25); `M githooks/pre-push` in porcelain; core.hooksPath=githooks so only this machine enforces.
- Stronger than the lens said: the claim lives only in commit prose. 3c83da5b0 committed tools/citation_lint.py (git log -1 names it) but `git show 3c83da5b0:AGENTS.md | rg "Citation lint"` has no match, so neither the hook bytes nor the AGENTS.md claim is in any commit. The commit message's "Citation lint LANDED ... byte-checked at pre-push" is receipts-only theater in the exact class the dogfood hunts (Q1).
- One parenthetical corrected: f0768f3be (last hook commit) is 2026-09-30 21:38Z, roughly 1.6h INSIDE the window start 20:00Z, not "pre-window". Immaterial to the core claim.
- Consequence found by this pass (see addition A2): the dirty tree already fails this gate 3-blocking, so the first enforcing push after committing the hook blocks unless three garden-night rows are fixed or baselined first.

### F2 tracked TLS private key invisible to the gates: CONFIRMED, mechanism sharpened (it is worse than invisible: known and still there)

- git ls-files memory/tls lists lan.crt + lan.key; single landing commit 799ddb6fe 2026-08-19 09:36:58 -0400 whose own message says "LOCAL ONLY, not pushed". 1675 B, 27 lines, BEGIN x1, PRIVATE KEY x2: real RSA-shaped PEM, falsifier dead.
- .gitignore read whole: no memory/tls rule. configs/secret_gate_baseline.json read whole: accepted={} plus six path entries, none for lan.key.
- Lens's live run reproduced at correct CLI: --changed over 135 files (lens said 122; tree churn), critical=0 blocking=0 exit 0. Explicit scan: `--full memory/tls/lan.key memory/tls/lan.crt` exits 1, "memory/tls/lan.key:1:PRIVATE-KEY-BLOCK:critical". The gate SEES it when it looks; the --changed hook path structurally never looks at a file unchanged since 2026-08-19.
- Sharpening the lens missed: the committed estate has known for five weeks. dffd32a72:githooks/pre-push:317 and HEAD:githooks/pre-push:378 both read "known-true positive memory/tls/lan.key detected critical". And 799ddb6fe is an ancestor of local/run-beta1-factory-audit-20260914, so the key blob lives in a second on-disk repo (C:\Users\foste\Documents\projects\Mag-backup.git; git remote -v shows no off-machine remote). "Invisible to every gate" is the wrong frame; "detected, documented, accepted nowhere, excised nowhere for 5 weeks" is the byte truth.

### F3 seed_seal fired once, on the older seed, zero production consumers: CONFIRMED

- state/keys/seed_seal_key: 64 B, mtime Oct 2 00:07. Exactly one sidecar, arc_seed_sess_f4ad2dcb_20260907_0026.seal, 748 B, mtime Oct 2 00:10; arc_seed_c424b80a-5f44_f69d1c0fd1073f55.md (mtime Sep 19 05:01) has no seal; the sealed pair's seed/chain are mtime Sep 6 20:26, so the seal indeed landed on the OLDER seed.
- rg over mag/tools/scripts/tests/configs: seed_seal and verify_seed appear only in mag/seed_seal.py and tests/test_seed_seal.py. Zero production call sites; mag/seed_seal.py:36-40 confesses it verbatim ("nothing in mag/arc_seed.py or any consumer REFUSES an unsealed/forged seed yet").
- Clean check this pass (negative result, banked): state/keys is NOT tracked (git ls-files state/keys empty; .gitignore:40-42), so the seal private key's custody law held, unlike lan.key's.

### F4 pidfile guard non-atomic and porous: CONFIRMED, upgraded to live production evidence

- scripts/descent_driver.sh:13-22 read verbatim: `[ -f ]` check, `kill -0`, then plain `echo $$ >` at :22. No mkdir, no noclobber, no O_EXCL. The repro rerun this sitting gave pairs=40 both_proceeded=26 (lens: 21): porosity reproduces across independent runs, 52 to 65 percent both-passed.
- Live production facts the lens could not see (its blind spot 2):
  - The guard landed at 2026-10-02T03:31:54-04:00 (07:31:54Z, commit e3c7d341c, same commit touched scripts/descent_driver.sh).
  - The sanctioned driver, winpid 44072, was born 2026-10-01 21:31:24 local (WMI), which NIGHT_CLOSE_20261002.md:50 confirms as "driver start 21:31:24Z". It started on pre-guard bytes, so it never wrote a pidfile.
  - state/descent_driver.pid is ABSENT at 11:12Z while 44072 still loops (driver.beat cycle 945 at 11:10:52Z). The guard is disarmed against the one driver it was built for; any launcher passes clean.
  - One did: a second instance, winpid 44692, launched 11:10:03Z (WMI), overlapped the sanctioned driver roughly 90 seconds, and was gone by the 11:11:34Z sweep. Attribution OWED (no schtasks fires at 07:10 local; sibling hostile-pass sessions were active in this same workflow).
  - No money lost this time: memory/runs/hermes_burn/usage.jsonl has zero rows after 2026-10-01T21:53:52Z (rg for 2026-10-02T11:1 rows: none), consistent with all asks skipping on existing outputs.
- Sibling disease the lens named but did not open: mag/lane_runner.py:1089-1099 is the same check-then-write shape (PIDFILE.exists, read old pid, REFUSED log, write_text), so the same race class lives in the lane scheduler daemon.
- T1W2 19:17-19:18Z double-fire: still unattributed; ractor-topic/SYNTHESIS.md:126-127 banks it OWED and nothing since names a cause (my 23:32-focused rg and task sweep found no attribution). Killing the twins did not remove the class; today's 11:10:03Z launch is the same species.

### F5 orphaned hidden-execution vbs + unpaid OWED rows: CONFIRMED, with exit-code semantics split

- scripts/invisible_runner.vbs:27-29 read verbatim: hidden `cmd /c` at :27, `CreateTextFile(..., True)` overwrite at :28, rc written with no timestamp and no command line. The whole audit trail is one int.
- Task sweep this sitting: zero scheduled tasks reference invisible_runner (Get-ScheduledTask action sweep). The four-task re-registration is byte-true.
- Red-task readings byte-exact against the lens: MagGapSentinelDaily=1, MagTipWitnessDaily=2, MagXRadarDaily=2, Estate KeyAudit=1, Estate LaneSupervisor=1, EstateWalkDaily=1. Full picture is 11 red, 4 re-registered, 7 open.
- Semantics split (lens blind spot 4, resolved): MagCensusPatrolDaily=1 (LastRun 10-02 03:29:29) is the DESIGNED COLLECT-DRIFT tripwire, answered same morning by watch/inbox/census_refresh_20261002.md; EstateWalkDaily=1 (10-01 09:15) is the failure 5d2263f10 root-caused and rewrote, fix fires 09:15 local today, after this window. Still open and unattributed: Estate Ratchet=1 and Estate KeyAudit=1 (both since 10-01 09:45), Estate LaneSupervisor=1 since 09-28 (four days), MagGapSentinelDaily=1, and the two exit-2 tasks (TipWitness, XRadar), which the B2-246 law classes as cannot-verify incidents. Red is not always broken, but six reds are unattributed and two of them are the ratchet and key-audit patrols themselves.
- logs/kpi.jsonl now 753,324,704 B (lens: 752,865,877; prior synthesis: 748,222,017), zero rotation siblings, writer mag/records.py:138 (write_kpi). Growth continues through this sitting.
- NIGHT_CLOSE_20261002.md mtime 2026-10-02T05:14:18.9033Z, unchanged: the erratum (its "~48s cadence" claim at :58; real 55.2 s/cycle per ractor-topic/SYNTHESIS.md:75-77) is still unpaid.
- 23:32:51 EDT attribution: still absent; the only files naming it are the audits themselves (rg sweep). New forensic fact this pass: %TEMP%\invisible_runner_rc.bak-1002 (content 7, mtime 06:01:18Z) preserves the 23:32:51 EDT 10-01 launch per ractor-topic/communication.md:53, and the live rc.log was overwritten AGAIN at 06:20:49Z (content 1): a vbs execution 19 minutes after the prior probe's backup, with zero tasks pointing at the vbs. Unattributed. The single-slot log destroyed whatever ran before it, again.

## What the lens missed (this pass's additions)

1. LIVE: the pidfile guard is disarmed in production right now and a second driver overlapped the sanctioned one for ~90s at 11:10:03Z today (details under F4). Evidence: WMI sweeps 11:09-11:11Z, absent state/descent_driver.pid, driver.beat cycle 945 at 11:10:52Z, guard commit time 07:31:54Z vs driver birth 21:31:24Z the night before. Falsifier: a pidfile containing the live driver's pid while 44072 loops (none exists). Move: kill 44072, relaunch under guard bytes, verify pidfile appears; swap acquire to atomic mkdir; make the EXIT trap remove the pidfile only when its content is own pid; apply the same to mag/lane_runner.py:1089-1099. ~15 min.
2. The working tree already fails the estate's newest truth-gate: `.venv/Scripts/python.exe tools/citation_lint.py check --changed` exits 1 with blocking=3 (watch/inbox/model_garden/STOCHASTIC_LENSING.md:44 PHANTOM-NUMBER 8062 and 2419; watch/inbox/model_garden/SWARM_1.md:55 EMPTY-SPAN on mag/gpu_ghost.py:174) and warns=36. Both files are tracked-and-modified (porcelain M). The garden night's own artifacts carry the phantom-number disease the lint was built to catch, so the first enforcing push after the hook commits will block. Falsifier: rerun after fixing the three rows yields exit 0 with no new baseline rows. Move: fix or baseline the three rows in the same sitting that commits githooks/pre-push. ~10 min.
3. memory/tls/lan.key is documented-known in committed bytes since 09-27 (dffd32a72:githooks/pre-push:317, HEAD:378: "known-true positive ... detected critical") and my explicit full-mode scan re-detects it critical today; the blob also sits in the Mag-backup.git repo (ancestor check true). Five weeks of known-critical with no acceptance, no gitignore rule, no excision. Falsifier: a post-09-27 purge receipt, baseline entry, or gitignore rule naming memory/tls (none exists). Move: git rm --cached both files, add memory/tls/ to .gitignore, rotate the LAN pair; history purge stays the operator's call. ~20 min.
4. The commit-queue law named OWED in 2093ca518's message is still ticketed nowhere: rg over queue/, memory/law, state, watch/inbox, HANDOFF_MAG_AGENT_TODOS.md finds only discussion artifacts (a gala gitlog dump, RACTORSWARM_MAP, and this sitting's own lens files), zero ticket rows. The prior synthesis's lineage grep finding remains live through this sitting. Falsifier: a row in queue/todo.md, TICKET_LEDGER, or memory/law naming the law. Move: one ticket row naming the law and an owner. ~5 min.
5. invisible_runner.vbs executed at 06:20:49Z today (rc.log content 1, mtime 06:20:49Z), 19 minutes after the ractor-topic probe's documented backup (06:01:18Z, content 7), with zero scheduled tasks referencing the vbs; the single-slot log again destroyed the previous forensic. Falsifier: a seat receipt naming a 06:20:49Z vbs run (none found). Move: make the vbs append a timestamped jsonl line (ts, command line, rc) or delete it. ~10 min.

## Checked and clean (negative results, so nobody re-spends them)

- state/keys/seed_seal_key is untracked (custody law held).
- No off-machine git remote exists (only the local backup path).
- The engine topic-undefined fix held at the metadata layer: .zcode/workflows/ractor-engine.dwf.ts:29 declares topic required (file mtime Oct 2 06:38) and this very run rode a real topic; note String(args.topic) fallbacks remain in-script at :84, :135, :226 if a caller bypasses the harness's required-arg enforcement.
- MagCensusPatrolDaily and EstateWalkDaily reds are answered/root-caused, not broken (semantics split under F5).

## OWED from this pass (never asserted as fact)

- Attribution of the 11:10:03Z descent_driver launch (winpid 44692, ~90s overlap, no paid rows drained).
- Attribution of the 06:20:49Z invisible_runner.vbs execution.
- Whether the 06:20:49Z rc.log write was the ractor-topic probe's own delayed fire rather than a third-party launch; bytes cannot distinguish.
- Per-commit dollar conversion (dogfood Q3) not attempted by either the lens or this pass; live ledger context only: usage.jsonl last row 2026-10-01T21:53:52Z, driver-log ledger total $37.76, NIGHT_CLOSE overnight metered $8.9954 (its own lines 50-58).
- T1W2 19:17-19:18Z double-fire cause: still unattributed, unchanged from the prior synthesis.

Filed by break-security, 2026-10-02T11:2xZ. The lens survived: 5 of 5 findings
confirmed, two of them sharpened past their original frame.
