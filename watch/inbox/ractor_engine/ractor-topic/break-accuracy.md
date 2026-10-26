# break-accuracy - hostile second pass on the lens report (ractor-topic, d06 sitting)

Moment: 2026-10-06 ~21:03 EDT to ~21:25 EDT (01:03Z Oct 7), `date` read
"Tue Oct 6 21:03:14 EDT 2026" mid-pass. HEAD 8dd34b388, branch
mag/run-beta1-factory-build-audi-20260806T231709Z. Every verdict below is
byte-checked against bytes I read or commands I ran this sitting; anything I
did not run is named where it matters. Prior-run pass bytes (2026-10-02, tree
0c9d72a06) were overwritten by this filing per the ask's named path; they are
recoverable from git at commit e3c7d341c
(`git show e3c7d341c:watch/inbox/ractor_engine/ractor-topic/break-accuracy.md`).

## Verdicts

### F1, AGENTS.md census carrier stale +343 with four unactioned reds: CONFIRMED (two blemishes, neither kills)

Reproduced the instrument: `.venv/Scripts/python.exe -m pytest --collect-only
-q` (default testpaths) reads **exit 0, "4701 tests collected in 21.54s"**,
4701 node-id lines, **564 unique item-bearing files** (563 under tests/, 1
under tools/gps_mcp), 0 error lines. The lens's 4701 and exit 0 reproduce
exactly; its "565 unique files" reads 564 on my re-run at the identical item
count, a one-file delta I could not reproduce. AGENTS.md:29 still reads
"4,358 tests collected / 518 files (2026-10-04 census" byte-exact as quoted.
logs/census_patrol.log: line 320 "[2026-10-06 08:30:02] START census deep
check (--collect)", line 338 the exact drift text "pytest holds 4648 vs
carrier claim 4358 (delta +290, bar 20)", line 356 "[2026-10-06 08:30:02] END
exit=1". memory/attention.md:532 (10-04, +29), :588 (10-05, +133), :646
(10-06, +290) match. Commit a7ca49be1 (2026-10-04 02:15:42 -0400) message
carries "census carrier refreshed 4,257/504 (moment 2026-10-04T03:02Z" as
cited. The "four consecutive mornings" census is exact: the 08:30 deep check
fired COLLECT-DRIFT exit 1 on 10-03 08:30:01 (+41 vs carrier 4156, log lines
185-192, END exit=1 at line 212), 10-04 08:30:04 (+29 vs 4358, lines 257-264,
exit=1 line 282), 10-05 08:30:01 (+133, lines 283-301, exit=1 line 319), 10-06
08:30:02 (+290, lines 320-338, exit=1 line 356). The working-tree AGENTS.md
diff (4 changed lines: boot-recap paragraph + load-order row 0a) does not
touch the Tests bullet, so "nobody actioned the B2-246 refresh" holds as of
this sitting.

Blemishes: (a) the instrument moment "2026-10-06T23:47:12-40Z" is a malformed
UTC offset (none exists beyond +-14:00), so the moment is unparseable as
written even though the count verified; (b) the move's "~24-file growth the
patrol log lists" misquotes the log, which reads "29 file(s) since census"
(log line 332) and 556 disk candidates vs carrier 518 (lines 333-337). A
refresh writer must attribute from the log bytes, not memory.

### F2, AGENTS.md row 0b cites tools/zknot.py:51-52, a never-true line-cite: CONFIRMED (byte-exact; one imprecise reason clause; one move hazard)

tools/zknot.py:51-52 in the working tree are `import os` / `import re` (Read,
lines 51-52). The contract lives at :14-15 (docstring "Selection: task_type
not subagent_child/workflow_child, no parent, >=5 real user prompts"), :69
(`CHILD_TYPES = ("subagent_child", "workflow_child")`), :312 (`real = [s for
s in sessions if s["tu"] >= since_ms and len(prompts[s["id"]]) >=
MIN_PROMPTS]`), all verified by Read. `git log -S"zknot.py:51-52" -- AGENTS.md`
returns exactly one row: bc1bd1fd7 2026-10-05 22:31:16 -0400, "driver: R4
ticked". `git show HEAD:tools/zknot.py` (400 lines) has lines 49-55 = ROOT /
sys.path.insert / DB / OUT / LATEST / RUNS, exactly as the lens said. I went
one step further than the lens: at the birth commit itself, `git show
bc1bd1fd7:tools/zknot.py` (386 lines) has lines 51-52 = blank line +
`DB = Path.home()...`, so the cite was never true at any revision, birth
included.

Reason-blemish: "invisible to the pre-push citation lint because AGENTS.md is
unchanged prose" is imprecise twice over. AGENTS.md is working-tree modified
(" M AGENTS.md", porcelain); and even inside a changed set the lint would pass
this cite, because its structural checks only see that lines 51-52 exist and
are non-blank. A content-wrong line cite is outside the lint's detectable
class either way, so the invisibility conclusion holds, for a different reason.

Move hazard the lens missed: the proposed repoint pins :69/:312, which are
working-tree line numbers on a file carrying 81 uncommitted changed lines
(`git diff --stat`: tools/zknot.py | 81 +-). The repoint must land in the same
commit as the zknot refactor, or cite the stable docstring prose (:14-15),
which is the lesson the communication lens already banked (cite by quoted
text, not line number, on moving surfaces).

### F3, ESTATE_INDEX pointer cure byte-verifies, walk_bytes unverified: CONFIRMED, and the lens's own evidence carries a 10x phantom digit

`wc -c -l watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` reads 1218137 lines /
363012458 bytes, exact match to dashboard/data/ESTATE_INDEX.pointer.json:4-5
(master_rows 1218137, master_bytes 363012458) and to the lens's wc. Pointer
line 8 ts "2026-10-06T13:09:25Z" exact (file mtime Oct 6 09:09 local = 13:09Z,
consistent). Retired copy dashboard/data/ESTATE_INDEX.jsonl.retired-20261006
= 2,523,006,985 bytes (ls), matching DAWN_REPORT_20261006.md:181-183. Reader
half confirmed: dashboard/server.py:189 (pointer const), :193-221
(_estate_index_source resolver; the lens's :194-211 range sits inside it),
:813 (data-door comment naming the pointer follow), and :202 still carries the
rotted "346,683,794-byte master" figure in its root-cause comment (live master
is 363,012,458 now).

The catch: the lens quotes walk_bytes as **1,405,100,237,137** twice (blind
spot 4 and the finding body). The pointer's byte-truth is `"walk_bytes":
140510023713` (pointer line 7), about 130.9 GB, not 1.28 TB. An untruncated
search `grep -rn "1405100237137" watch/inbox state memory dashboard tools`
finds the 13-digit string NOWHERE in those roots (single hit: my own command
echoed into memory/trajectory/steps.jsonl during the search); the 12-digit
truth lives in exactly three places: pointer line 7,
dashboard/static/index_data/last_run.json line 4, and
watch/ESTATE_INDEX/last_run.json line 4 (total_bytes 140510023713,
total_files 1218137, same 13:09:25Z ts, "seconds": 564.5). So "walk_bytes
unverified, no walk instrument run" is still true (I did not re-run the
9.4-minute estate walk either), but the lens reported the number wrong by 10x
with no source anywhere in the estate: exactly the PHANTOM-NUMBER class the
citation lint hunts. The finding survives on corrected digits.

### F4, freshness-gate cure byte-verifies: CONFIRMED (and the cure's test now actually run)

Two runs of `.venv/Scripts/python.exe tools/freshness_check.py` this sitting:
both exit 0, both print "FRESHNESS: PASS" and the byte-exact clause
"state/START_BRIEF.md: [machinery-regen] excluded from the mtime crown
(AGENTS.md row 0a)". START_BRIEF.md mtime is Oct 4 08:37 (two days stale) and
PASSes: the exclusion demonstrably does the work. DAWN_REPORT_20261006.md
lines 171-174 record the prior FAIL (logic lens amendment, 09:36:17Z) as
cited, and state/CURRENT.md lines 83-86 name
tests/test_freshness_machinery_exclusion.py. The lens never ran the cure's
test; I did: `pytest tests/test_freshness_machinery_exclusion.py -q -p
no:cacheprovider` reads **4 passed, exit 0**.

Blemish: the lens's falsifier is mis-specified. A tree where START_BRIEF is
stale and the meter PASSes is the exclusion working, not dead (that is this
tree right now). The clause-dead falsifier is the clause string vanishing
from the meter's output, or a stale machinery page FAILing anyway.

### F5, the d06 lane left its own landing uncommitted: CONFIRMED

`git status --porcelain` this sitting: " M AGENTS.md" (line 1) and " M
state/CURRENT.md" (line 75) among 100+ modified paths. state/CURRENT.md line 8
reads "updated: 2026-10-06T18:30:00Z", mtime Oct 6 14:31 local, both as the
lens said. The relay chain is committed: ba03060bb (2026-10-06 07:23:52 -0400)
and d5f89d97b (2026-10-06 09:58:24 -0400) both touch
watch/inbox/DAWN_REPORT_20261006.md (git show --stat). DAWN lines 95-98
(stash-sweep defect class, dawn item 7) and lines 201-207 (communication
lens: "The fold must commit before you boot") confirmed.

Two sharpenings: the freshness cure prose rides the uncommitted AGENTS.md diff
(row 0a adjudication hunk) and tests/test_freshness_machinery_exclusion.py is
UNTRACKED (porcelain "??"), so the move's "if not already in HEAD" hedge
resolves: it is not in HEAD. And "~5h uncommitted" fits CURRENT.md (14:31
mtime at the lens's ~19:47 moment, about 5h16m) but understates AGENTS.md,
whose mtime is Oct 6 07:29 local, about 12 hours at that moment.

## What the lens missed (additions)

A1. The walk_bytes 10x phantom (F3 above): 1,405,100,237,137 appears nowhere
    in the estate; byte-truth 140,510,023,713; instrument identified at
    tools/index/projects_index.py:218 (sources last_run["total_bytes"]);
    corroborated by both last_run.json copies at the same 13:09:25Z ts.
    Falsifier: a walk receipt or pointer revision carrying the 13-digit value
    (my grep covered watch/inbox, state, memory, dashboard, tools; other
    roots ungrepped). Move: strike the wrong digits wherever the accuracy
    report lands, before anyone quotes them (~2 min).

A2. F1's refresh move misquotes the patrol log's growth list (~24 vs the
    log's "29 file(s) since census", log line 332; disk candidates 556 vs
    carrier 518, lines 333-337). Falsifier: the log line reading 24. Move:
    attribute the refresh from the log bytes (~2 min).

A3. The malformed collect moment "-40Z": a census rewrite must name a
    parseable moment per the B2-216 denominator law (instrument, moment,
    delta). Falsifier: none needed, the string is its own evidence. Move:
    fold into the F1 rewrite discipline (~0 min, a rule).

A4. The F2 repoint cite-rot hazard: :69/:312 are working-tree line numbers on
    a file with 81 uncommitted changed lines. Falsifier: zknot.py landing
    with identical line numbering to the working tree. Move: cite the
    docstring prose (:14-15) or land the repoint in the same commit as the
    zknot refactor (~1 min of care).

A5. F4's falsifier is mis-specified (PASS-with-stale-START_BRIEF is the cure
    working); the real falsifier is the clause string vanishing from output
    or a stale machinery page FAILing. Move: none; note for the engine's
    falsifier hygiene (~0 min).

A6. Convergence flags under the quantifier law: F1 is CONVERGENT (four
    independent instruments agree: patrol log, attention.md alerts, the
    patrol's own 08:30 collect run, my fresh collect); F4 is CONVERGENT with
    state/CURRENT.md:83-86's own claim. Both outrank single-source findings.

A7. Fresh census numbers for the F1 rewrite, instrument named: 4701 collected
    / 564 item-bearing files (563 tests/ + 1 tools/gps_mcp), exit 0, zero
    collection errors, "4701 tests collected in 21.54s". The rewrite must
    keep the exact "N tests [collected] / M files (YYYY-MM-DD census" grammar
    (B2-249 carrier shape law, AGENTS.md:29) or the patrol gate fails closed
    on grammar.

## Not run this sitting (disclosed, never guessed)

- The executed denominator (`pytest -q` full suite): not run; collect
  instrument only, the same scope limit the lens declared.
- The estate walk (fresh walk_bytes verification): not re-run; 1,218,137
  files, 564.5s per last_run.json. Internal consistency only.
- QUEEN paper external identifiers: remain OWED exactly as the lens marked;
  no resolution attempted here.
- USN journal or other forensics on the lens's own first instrument runs (the
  ones whose exit codes it could not capture): not run; I verified only the
  re-run results it reported, by reproducing them.

Filed by break-accuracy, 2026-10-06T21:2x EDT. No em-dash bytes.
