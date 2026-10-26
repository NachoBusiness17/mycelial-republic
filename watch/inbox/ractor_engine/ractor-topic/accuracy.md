# accuracy.md - lens verdict, ractor-topic ride (2026-10-06)

Lens: accuracy (falsifier-hunter). Topic arg arrived undefined, so the lens rode its
standing beat: byte-check the numbers and citations the estate is carrying right now.
Canon read first per load row 0a: state/CURRENT.md (authored, mtime 14:31:20 local),
state/NIGHT_LOOP_20261005.md (canon window doc), state/LIVE_REPORT.md newer by mtime
(18:59:39 local) but machinery-excluded and the exclusion prints. Receipts read:
watch/inbox/DAWN_REPORT_20261006.md, watch/inbox/QUEEN_CHESS_LM_20261006.md,
logs/census_patrol.log. Moments UTC; counts name instrument + moment per the census
denominator law (AGENTS.md B2-216). The prior sitting's verdict on the 10-02
night-close wave is preserved byte-identical at
watch/inbox/ractor_engine/ractor-topic/accuracy_20261002_nightclose.md.

## Instruments run this sitting

1. `.venv/Scripts/python.exe -m pytest --collect-only -q` (repo root, pytest.ini
   default testpaths: tests + tools/gps_mcp), moments 2026-10-06T23:47:12Z to
   23:47:40Z, exit 0, summary line "4701 tests collected in 20.86s", 565 unique test
   files counted from the node-id stream (`grep -oE '^[^:]+\.py' | sort -u | wc -l`),
   zero collection errors (clean summary line, exit 0). Note: 81 output lines contain
   the substring "error"; those are test-name matches, not collection errors.
2. `.venv/Scripts/python.exe tools/freshness_check.py`, run twice (~23:44Z and
   ~23:51Z), both exit 0, verdict "FRESHNESS: PASS", with
   "state/START_BRIEF.md: [machinery-regen] excluded from the mtime crown (AGENTS.md
   row 0a)" printed verbatim.
3. `wc -c -l watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` at ~23:50Z: 1,218,137 lines /
   363,012,458 bytes.
4. git probes: `git log -S`, `git show HEAD:tools/zknot.py`, `git status --porcelain`,
   `git log -- <path>` as cited below.

## Findings

### F1: the census carrier is 2 days stale with a +343 drift, and the red has fired daily with nobody actioning it

AGENTS.md:29 still carries "4,358 tests collected / 518 files (2026-10-04 census".
My collect run at 2026-10-06T23:47Z reads 4701 tests / 565 files: delta +343 vs the
carrier. The patrol's own instrument agrees and is getting louder:
logs/census_patrol.log at [2026-10-06 08:30:02] reads "COLLECT-DRIFT ... pytest holds
4648 vs carrier claim 4358 (delta +290, bar 20)" exit 1, alert appended at
memory/attention.md:646; prior reds at memory/attention.md:532 (+29) and :588 (+133,
the row DAWN_REPORT_20261006.md:102-104 cites). B2-246 puts the refresh on the
operator's pen, and the refresh path provably works when actioned (commit a7ca49be1
refreshed the carrier to 4,257/504 on 10-04). This is the exact disease the logic
lens named at dawn ("a red firing with nobody actioning it",
DAWN_REPORT_20261006.md:174-177), now on its fourth consecutive fire against one
stale carrier. The growth is attributable, not a fabrication smell: the patrol log
names the added test files since 10-04 (test_fold_gate.py, test_cache_kpi_receipt.py,
test_consensus_degeneracy_20261005.py, test_seal_patrol_tamper_20261005.py,
test_cr_strip_at_load.py "... and 19 more").
Falsifier: a fresh `pytest --collect-only -q` reading 4,358/518, or the AGENTS.md:29
bullet already carrying a 2026-10-06 census date.
Move (~15 min): rewrite AGENTS.md:29 from a fresh collect run with instrument and
moment named, attributing the ~24-file growth from the patrol log, in the same commit
as F2 and F5.

### F2: AGENTS.md row 0b cites tools/zknot.py:51-52 for the session exclusion; those lines are imports

The row 0b boot-recap bullet cites "tools/zknot.py:51-52" for "excludes child
sessions and under-5-prompt mains". Live bytes at tools/zknot.py:51-52 are
`import os` and `import re`. The real contract lives at tools/zknot.py:14-15
(docstring: "Selection: task_type not subagent_child/workflow_child, no parent, >=5
real user prompts"), tools/zknot.py:69 (CHILD_TYPES tuple) and tools/zknot.py:312
(the `len(prompts[s["id"]]) >= MIN_PROMPTS` filter). Provenance:
`git log -S"zknot.py:51-52" -- AGENTS.md` returns exactly one commit, bc1bd1fd7
("driver: R4 ticked", 2026-10-05 22:31:16 -0400); `git show HEAD:tools/zknot.py`
lines 49-55 hold ROOT/sys.path/DB/OUT/RUNS, so the cite was wrong at birth, not
rotted by later edits. The irony is load-bearing: the dud cite sits in the doc that
mandates citation discipline, and the pre-push citation lint only scans CHANGED
prose, so a never-true cite in an unchanged carrier survives every push.
Falsifier: any committed version of tools/zknot.py whose lines 51-52 carry the
child/under-5-prompt selection logic.
Move (~5 min): repoint the row 0b cite to tools/zknot.py:14-15 + :69 + :312 in the
same AGENTS.md edit as F1.

### F3: the ESTATE_INDEX pointer cure byte-verifies; one field stays unverified and one rot seed remains

The logic lens (DAWN_REPORT_20261006.md:179-184, 09:36Z) caught the pointer claiming
131,284,922,658 bytes / 1,164,604 rows, matching neither file. The pointer was
regenerated at 2026-10-06T13:09:25Z with renamed fields
(dashboard/data/ESTATE_INDEX.pointer.json:4-9, note on :9). My check: `wc -c -l
watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` reads 1,218,137 lines / 363,012,458 bytes,
an exact match to the pointer's master_rows/master_bytes. The retired frozen copy
sits at dashboard/data/ESTATE_INDEX.jsonl.retired-20261006 at 2,523,006,985 bytes,
matching the dawn report's frozen-copy figure to the byte. The reader half landed:
dashboard/server.py:189 (pointer path), :194-211 (pointer-following resolver with
root-cause comment), :813. Residuals: (a) walk_bytes 1,405,100,237,137 is an
estate-walk total I did not verify this sitting (no walk instrument run; asserted,
not checked); (b) dashboard/server.py:202 still hardcodes the 10-05-era
"346,683,794-byte master" in the root-cause comment while the live master is
363,012,458, a contradiction waiting for the next byte-checker.
Falsifier: rerun wc after the writer next appends; a stale master_bytes against a
moving master (the pointer carries a ts field, so staleness is detectable) would
falsify the cure's durability.
Move (~10 min): fix the server.py:202 comment to name the pointer as the live source
of the byte figure; verify walk_bytes the next time the estate walk runs, before any
consumer quotes it.

### F4: the freshness cure byte-verifies (CONVERGENT with CURRENT.md's own claim)

state/CURRENT.md:60-63 claims the meter that FAILed exit 1 at window start now reads
PASS. My two runs of tools/freshness_check.py this sitting both returned exit 0 with
"FRESHNESS: PASS", and the output prints the START_BRIEF.md machinery-exclusion
clause verbatim, proving the d06 adjudication clause is live code, not just a claim.
The logic lens's 09:36Z read (meter FAIL exit 1,
DAWN_REPORT_20261006.md:171-174) was true at its moment and is now cured: the loop
works end to end.
Falsifier: a tree where START_BRIEF.md is the newest state mtime and the meter still
PASSes would prove the exclusion clause dead.
Move (~2 min): none; keep tests/test_freshness_machinery_exclusion.py green.

### F5: the d06 lane left its own landing uncommitted on the tree that minted the stash-sweep disease

`git status --porcelain` at ~23:50Z reads ` M AGENTS.md` and ` M state/CURRENT.md`:
the d06 lane's refresh (CURRENT.md header updated 2026-10-06T18:30:00Z, mtime
14:31:20 local) and the AGENTS.md row 0a prose are still working-tree only, roughly
5 hours after landing. The relay chain itself got committed (DAWN_REPORT_20261006.md
in ba03060bb; NIGHT CLOSED d5f89d97b), and the communication lens ordered exactly
this ("The fold must commit before you boot", DAWN_REPORT_20261006.md:200-207) after
sibling stash-sweeps twice swept mid-landing landings on this same night (dawn list
item 7, 3 stashes verified). The lane that cured the pattern repeated it.
Falsifier: `git status --porcelain` showing both paths clean, or a stash whose diff
contains CURRENT.md bytes absent from HEAD.
Move (~5 min): one commit carrying AGENTS.md (F1 carrier refresh + F2 cite fix folded
in), state/CURRENT.md, and the freshness clause + its test if not already in HEAD.

## What checks out (verified true this sitting)

- mag/governor_autorun.py:992 holds MAG_LIVE_REPORT_EVERY default "300" exactly as
  AGENTS.md row 0a cites; the regeneration call sits at :1353-1357 as cited.
- mag/agent_cli.py:2251 lands on the _sync_current mirror docstring exactly as
  state/CURRENT.md:76-79 cites.
- mag/rib_boot.py:47 lands on the "AMENDMENT TAILS" cure exactly as
  DAWN_REPORT_20261006.md:44 cites.
- memory/attention.md:586-591 carries the +133 patrol row exactly as
  DAWN_REPORT_20261006.md:102-104 cites.
- tools/citation_lint.py:12 and tests/test_citation_lint.py:3 carry the struck 191.8M
  phantom fixture as AGENTS.md claims; tools/census_drift_patrol.py:350 fail-closes
  with the exact "need the claim shape" message as the B2-249 law claims.
- QUEEN link-drop (watch/inbox/QUEEN_CHESS_LM_20261006.md): internal arithmetic
  checks (2697-1782=915, claimed as "over 900 Elo"), the Elo figures are flagged as
  the paper's own claims at :36, and the unresolvable identifiers are marked OWED at
  :6 and :35 rather than asserted. The no-fabrication law is visibly holding in the
  newest receipt.
- Boot crown: LIVE_REPORT.md newest by mtime and the meter prints its machinery
  exclusion, so canon correctly falls to the authored pages.

## Blind spots (honest)

- My absence claims are scoped to named files and greps: I read three receipts of the
  window's thousands, plus the instruments. The dawn fold's "no --apply claimed" is
  its scoped grep, not mine, and I do not adopt it as universal.
- The 565-file count comes from a grep over node IDs; the patrol distinguishes
  "pytest-named candidates" (556 this morning) from "item-bearing files", so the
  carrier's M could legitimately differ from 565 by a few files either direction.
- I ran the collect instrument only, never the suite: the executed denominator is
  unknown this sitting; the two are different denominators by law.
- walk_bytes (1,405,100,237,137) on the pointer is unverified; the QUEEN paper's
  external identifiers remain OWED (no arXiv resolution attempted; the receipt itself
  reports search-index lag).
- My first two instrument runs failed to capture exit codes (PowerShell
  $LASTEXITCODE came back empty through the harness); I re-ran both under bash with
  explicit `echo $?` and report only the re-run results. The first runs' verdict
  lines matched the re-runs.

Filed by the accuracy lens, 2026-10-06T~23:55Z. All checks run this sitting.

## ERRATUM (2026-10-07, lane m7-phantom-erratum, run morning-block-20261007)

The walk_bytes figure this report carries is a phantom and is struck. Residual
(a) at accuracy.md:86 carries walk_bytes 1,405,100,237,137, and the walk_bytes
blind-spot line at accuracy.md:157 repeats the figure, an unverified
transcription (F3's own words: "asserted, not checked", accuracy.md:87-88).
The pointer's walk_bytes line at dashboard/data/ESTATE_INDEX.pointer.json:7
reads `"walk_bytes": 140510023713,` (140,510,023,713 with separators),
timestamped 2026-10-06T13:09:25Z on :8. The phantom digit string equals the
pointer's digit string with an extra character appended at the end. Corrected
truth: walk_bytes = 140510023713. F3's byte-verified half (master_rows
1218137 / master_bytes 363012458, pointer :4-:5) is untouched by this
erratum. Verified this sitting by byte Read of the pointer file; no walk
instrument was re-run (per the pointer's own note on :9 the estate-wide walk
total's source is the pointer's regeneration). Erratum filed by lane
m7-phantom-erratum.
