# break-moonshot-2 - hostile second pass on lens moonshot-2 (2026-10-02)

Run: ractor_engine / 2026-10-02-dogfood-48h, break pass on the moonshot-2
lens report. Every check below was executed this sitting on the current
tree; nothing is taken from the lens on trust. Prior synthesis read first
(watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md, whole) per the ask,
and nothing here re-derives its banked figures.

## Verdicts

### F1 (all gates live at the push boundary, uncrossed since 10-01): CONFIRMED

- githooks/pre-push:10 (ratchet), :24-25 (citation_lint PUSH-GATE), :91
  (census patrol) read this sitting, byte-exact as cited.
- `git for-each-ref refs/remotes` returns exactly one ref,
  refs/remotes/local/run-beta1-factory-audit-20260914, committerdate
  2026-10-01 08:12:30 -0400 (= 12:12:30Z). `git branch -r --contains
  e3c7d341c` returns empty. Six window commits span 2026-10-01T20:46:30-04:00
  through 2026-10-02T03:31:54-04:00 (git log %cI). None is on any remote.
- `git status --porcelain | wc -l` reads 118 NOW vs the lens's 116: the
  tree kept moving after the lens's read (B2-216: name instrument, moment,
  delta; the claim's substance, a large ungated tree, is intact).
- No .git/census_blind_last_push.txt exists (checked), consistent with zero
  pushes through the hook since the B2-277 block landed.
- Sharpening, not weakening, of the citation_lint clause: the TOOL has run
  by hand (watch/inbox/fillball/citation-lint.md:54, "Command: check --files
  over the six ractor50 chapters"; ractor-topic SYNTHESIS.md:174,
  "citation_lint on that file: ok, blocking=0, 26 anchors") but the hook's
  `check --changed` mode (pre-push:25), the mode behind the landed
  changed-prose claim, has no execution evidence anywhere: no push since
  2026-10-01 12:12:30Z, no --changed run receipted. Falsifier ("a remote
  ref containing e3c7d341c") did not fire. Notation nit only: the lens
  labeled EDT wall times with a Z suffix ("20:46Z...03:31Z EDT").
- The move (chain the three gates into a pre-commit hook via core.hooksPath)
  stands; ~40 min is a fair cost.

### F2 (ledger certifies LANDED work git never accepted): CONFIRMED, strengthened

- TICKET_LEDGER.md:133-143 shows SW1-01..SW1-10 all "LANDED-with-test"
  (rows read this sitting; SW1-05..10 in the tail, SW1-01..04 at :133-136).
- The falsifier (empty diff --stat, test tracked in HEAD) does NOT hold:
  `git diff --stat HEAD` over the ticket paths returns 9 files changed,
  128 insertions(+), 19 deletions(-); `git status --porcelain` shows all of
  them M plus `?? tests/test_sw1_tickets.py`.
- The lens UNDERCOUNTED the class: it omitted tools/roblox_npc_gateway.py
  (SW1-02's file, also M) and tools/code_swarm.py (ticket SS53-5, also
  "LANDED-with-test" in the same ledger block, also M). Ten SW1 ticket
  files + one SS53 file + the untracked test all sit outside HEAD.
- The test half is real and green, run by me this sitting:
  `.venv/Scripts/python.exe -m pytest tests/test_sw1_tickets.py -q
  -p no:cacheprovider` = 17 passed in 0.78s.
- Wording nuance only: a crash does not by itself delete working-tree
  bytes; the true risk is any reset/checkout/clean or the untracked test
  never being added. The finding's spine (the ledger says LANDED, git holds
  none of it) is byte-true and the move (commit the eleven files plus the
  test in one sitting, ~25 min) is right.

### F3 (built-once-never-swept organs): WEAKENED (seed_seal half killed)

- KILLED CLAUSE: "seals nothing (no .seal sidecars beyond pytest tmp)" is
  false. watch/arc_seeds/arc_seed_sess_f4ad2dcb_20260907_0026.seal exists on
  the tree (read this sitting): schema seed_seal.v1, sealed_by
  "mag/seed_seal.py seed_seal.v1 (SS-1)", sealed_at 2026-10-02T04:10:34Z,
  key_id de5fc05e962c43ab. The landed receipt documents it
  (watch/inbox/fillball/seed-seal.md:42-47: one real seal over the
  pam.md-cited seed; :46-47 sign + verify exit 0 + deterministic re-sign;
  :48-57 the 14-test forge drill; :103-105 the second seed deliberately
  unsealed, fail-closed). The lens missed both the sidecar and the receipt.
- SURVIVING CLAUSE: "zero callers outside itself" holds for production
  code, grep this sitting: the only mag/tools/scripts hit for seed_seal is
  the mag/__pycache__ binary. The organ was hand-fired once via CLI and is
  armed-and-opt-in BY DOCUMENTED DESIGN (seed-seal.md section 4: the
  enforcing flip is operator-gated), not forgotten. The honest restatement
  is "armed, dogfired once by hand, unwired at every consume site", which
  still supports the move (wire verify over REGISTRY.jsonl in a pre-commit
  hook, or park with a dated operator row).
- G6 UNDERCOUNT (strengthens the warn-only = warn-never leg):
  memory/workflows/REGISTRY.jsonl carries G6 ok:false on 19 rows since
  2026-09-25 (rows 1, 20, 26, 27, 36, 39, 46-58; python census this
  sitting), 13 of them inside this window (46-58), vs the lens's seven.
  Rows 1, 36, 39 are ok:false WITHOUT the soft flag.
- code_swarm / rib_swarm once-only corroborated negatively: zero
  REGISTRY.jsonl mentions of either name, no scheduled task whose action
  arguments match "swarm" (Get-ScheduledTask sweep this sitting). The
  falsifier (a second scheduled/workflow invocation after 2026-10-02) did
  not fire.
- Contrast organ confirmed richer than the lens knew: water_computer is
  wired at mag/game_campaign.py:21 and :70, AND its own history at
  :1452-1457 records it as a former zero-caller dead seam (5 red tests
  since landing) only cured by the 2026-09-27 module-verb dispatch at
  :1460-1469. The disease recurs; the cure shape exists in-repo.

### F4 (OWED split: commit-shaped done, chore-shaped untouched): CONFIRMED

Every byte-check in the received evidence held:
- pidfile: `grep -l pidfile scripts/*` = scripts/descent_driver.sh only.
- Four tasks DIRECT: MagCensusPatrolDaily / MagFtsIndexDaily / MagImproveDaily
  all powershell.exe -NoProfile -ExecutionPolicy Bypass -File ...ps1;
  MagLeaveProtocolDaily runs .venv\Scripts\python.exe tools\leave_dispatcher.py
  directly (Get-ScheduledTask Actions, this sitting).
- Census proof fire: watch/inbox/census_refresh_20261002.md:3-6, hand-fired
  2026-10-02T03:29:15Z, exit 1 COLLECT-DRIFT (4188 vs 3550), answered by the
  10:08Z refresh; the AGENTS.md carrier bullet reads "2026-10-02 census"
  (grep this sitting).
- NIGHT_CLOSE erratum unpaid: `grep -c "ERRATUM\|1\.0077"
  watch/inbox/NIGHT_CLOSE_20261002.md` = 0.
- kpi.jsonl unrotated and still growing: 753,345,001 bytes NOW (stat this
  sitting) vs the lens's 752,846,276 and the synthesis's 748,222,017; the
  writer is write_kpi at mag/records.py:138 (def read at :130-145).
- invisible_runner.vbs:28 is byte-exact CreateTextFile(..., True):
  overwrite mode, one %TEMP% log, no timestamp or command line.
- commit-queue law ticketed nowhere: zero grep hits in queue/todo.md,
  memory/law/registry.json, TICKET_LEDGER.md, and (my addition)
  memory/law/enforcement_trail.jsonl.
- mag-docker-watchdog still wscript.exe watch\docker_watchdog.vbs.
- Falsifier: no ERRATUM banner, no rotation artifact, no direct-action
  watchdog registration, no commit-queue row exists. None found.
- NOTE: the lens report reached me truncated mid-sentence ("...and the
  cured VBS disease alre") by the engine's own 6000-char slice (see
  addition A1); the received portion is fully verified above, the amputated
  tail could not be checked and is not counted for or against the finding.

## What the lens missed (additions)

A1. THE ENGINE AMPUTATES ITS OWN BREAK INPUT. The hostile-pass ask is built
at .zcode/workflows/ractor-engine.dwf.ts:230 as
`JSON.stringify(s.value).slice(0, 6000)`: this run's lens report arrived
cut mid-finding-4, so the breaker is asked to verdict evidence it never
received. This is the current form of the prior synthesis's move-8 disease
(the FAIL-ledger consolidation drop): the full report now passes in shape,
but the slice amputates it in fact. There is no "FAIL ledger" concept left
in the 342-line script (grep FAIL: zero hits); the live defect is the
truncation. Falsifier: a future run whose >6000-char lens report reaches
its breaker uncut. Move: ~10 min, raise the slice to cover the schema's
worst case or chunk findings; add a G-check that the break input length
equals the report length.

A2. THE "CURED" PATROLS ARE NOT YET PROVEN GREEN. All four re-registered
tasks still read LastTaskResult=1 right now (Get-ScheduledTaskInfo this
sitting): FTS 10/01 09:00, Improve 10/01 08:00, Leave 10/01 08:00 are the
stale PRE-cure failures (no fire since re-registration), and census's
10/02 03:29:29 run is the proof fire that exited 1 by design on
COLLECT-DRIFT (then answered by the 10:08Z carrier refresh). Direct
registration is byte-true; a green standing fire has happened for none of
the four. Falsifier: any of the four showing LastTaskResult 0 from a
post-re-registration SCHEDULED (not hand) fire. Move: ~10 min tomorrow,
one schtasks /Query line per task after the 08:00/08:30/09:00 fires,
banked as the census receipt's follow-up.

A3. G6 FALSE-POSITIVE CLASS IS 19 ROWS DEEP, NOT 7 (detailed under F3;
rows 1/20/26/27/36/39 predate the window, so the class predates the
engine's window runs). Falsifier: a REGISTRY census showing fewer than 19
G6 ok:false rows since 2026-09-25. Move: ~15 min, teach the engine's
receipt-mention to carry the dated stamp the t62 prefilter wants, or
retire the soft flag as noise.

A4. LINKS 250->257 IS BYTE-TRUE AND NOW INDEPENDENTLY RESOLVED (the lens's
own blind spot): memory/corpus/LINKS.jsonl = 257 lines (wc -l this
sitting), last row id GALA-fillball-1001-fill-citation-lint stamped
2026-10-02T06:36:12Z, i.e. the fill-ball's own citation-lint lane banked
the 257th link. Falsifier: a future wc -l reading below 257 (the counter
is append-only, it only grows). Move: 0 min, fact banked; the metric's
home belongs in the next OWED sweep so no lens has to hunt it again.

A5. LIBRARIAN D1-D3 ARE NAMED-NOT-FIXED. The instruments' repo homes are
untouched by every window commit: mag/librarian_catalog.py (verify_canon's
home, grep -rln verify_canon) last commit 3752abae2 2026-09-25T23:42-04:00;
mag/librarian.py last commit 60b1bde7f 2026-09-14. The expedition banked
the disease names and the A-division doctrine, but no code fix landed in
5d2263f10..e3c7d341c. (D1's receipt_state script was not found in tools/
this sitting; its home is unlocated expedition-lane artifact, OWED.)
Falsifier: a window-range commit touching the arXiv regex, the
disjointness guard, or verify_canon's content-read path. Move: ~90 min,
one fill-ball lane per disease, D2 (guard-as-code) first as the smallest.

A6. THE PAID LEDGER WENT DARK AT 21:53:52Z MID-WINDOW. My re-sum of
memory/runs/hermes_burn/usage.jsonl: 236 rows, $37.7591 total, every row
inside the window, last row ts 2026-10-01T21:53:52Z (the final doubled-key
moment of the twin burn). $37.7591 + garden $3.4746 (NIGHT_CLOSE:52-54) =
$41.2337, so the lens's combined figure and the commit's "~$42 of 145"
are byte-true. But nothing after 21:53:52Z is priced anywhere: fill-ball,
ractor dogfood, and the 223M+ subscription workflow tokens carry no dollar
row (the lens named this blind spot; the byte boundary is new). Falsifier:
a usage.jsonl row stamped after 2026-10-01T21:53:52Z. Move: ~20 min, add a
subscription-lane cost row (token counts, even $0-marked) at each close, or
scope the ledger's coverage claim in NIGHT_CLOSE-class receipts.

## Checks run this sitting (instrument + output)

git for-each-ref refs/remotes (one ref, 2026-10-01 08:12:30 -0400); git
branch -r --contains e3c7d341c (empty); git log -6 %cI; git status
--porcelain | wc -l (118); git diff --stat HEAD over eleven ticket paths
(9 files, +128/-19); pytest tests/test_sw1_tickets.py (17 passed 0.78s);
grep seed_seal over mag/ tools/ scripts/ main.py (pycache only); find
*.seal (pytest-tmp dirs plus watch/arc_seeds, 61 total per PowerShell
count); python census of REGISTRY.jsonl G6 (19 ok:false rows);
Get-ScheduledTask / Get-ScheduledTaskInfo for Mag* and mag-docker-watchdog
(actions + LastTaskResult); stat logs/kpi.jsonl (753,345,001); sed
mag/records.py:130-145 and scripts/invisible_runner.vbs:20-32; grep
ERRATUM/1.0077 on NIGHT_CLOSE (0); grep commit-queue over four ledgers (0);
grep pidfile scripts/* (one file); Read githooks/pre-push (whole),
SYNTHESIS.md (whole), fillball/seed-seal.md (whole),
census_refresh_20261002.md (head), game_campaign.py:1440-1469,
ractor-engine.dwf.ts:218-262; grep FAIL in ractor-engine.dwf.ts (0);
usage.jsonl re-sum (236 rows, $37.7591); grep 250->257 across memory/
watch/ corpus/ (provenance found); wc -l memory/corpus/LINKS.jsonl (257).
Not run this sitting: WMI/process census, the full pytest -q suite, the
107-check gate reproduction, sweep-2, Nous balance re-query, and the
ractor-topic SYNTHESIS's own verification battery (already triple-verified
per its stamp; not re-derived here).

Filed by break-moonshot-2. No em-dash bytes in this file.
