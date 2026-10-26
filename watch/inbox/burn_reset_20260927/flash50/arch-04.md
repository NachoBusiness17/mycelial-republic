# arch-04: census_drift_patrol v2 design (2026-09-28)

Item arch-04, source: `tools/census_drift_patrol.py`. Charter: read the file fully, then design v2 - what additional checks should exist, what is redundant, what should be removed, how the fail-closed/fail-open balance looks. This file is the v2 spec draft; per spec-before-behavior, any code change lands against this doc.

## 1. Method: what was read and what was run

Read in full this session:

- `tools/census_drift_patrol.py` (403 lines, whole file)
- `tools/census_collect.py` (85 lines, the B2-365 deep-check split)
- `tools/census_patrol_selftest.py` (197 lines, the B2-248 self-test split)
- `tests/test_census_drift_patrol.py` (568 lines)
- `githooks/pre-push` census block (lines 58-102)
- `scripts/census_patrol_daily.ps1` (196 lines, the B2-246 daily surface)
- `pytest.ini`, `AGENTS.md` line 27 (the live carrier bullet), `logs/census_patrol.log` tail

Ran this session (all via `.venv/Scripts/python.exe`, interpreter verified per AGENTS.md python-env law):

1. `.venv/Scripts/python.exe tools/census_drift_patrol.py --self-test` - exit 0, 30 checks ok, "CENSUS-PATROL SELF-TEST: PASS".
2. `.venv/Scripts/python.exe tools/census_drift_patrol.py` (live estate) - exit 0: "census 2026-09-27 (2303 collected / 352 files)", 5 files grown since census (all dated 2026-09-28) inside the window, disk 369 vs carrier 352 instrument lag, "CENSUS-PATROL: ok".
3. `tail -60 logs/census_patrol.log` - today's 17:20:35 deep check: "collect-only tail: 2410 tests collected", "instrument gap: 1 zero-collect candidate(s): tests/test_selffeed_integration.py", "files: collected 368 vs carrier claim 352", "CENSUS-PATROL: COLLECT-DRIFT - collected drift: pytest holds 2410 vs carrier claim 2303 (delta +107, bar 20)", END exit=1, alert appended to memory/attention.md.
4. Future-date probe: synthetic estate with carrier dated 2026-09-29 (today+1, inside the documented tolerance), bullet as line 1, git committed - exit 2, "CENSUS-PATROL: census dated -1 days in the future (fabrication smell)".
5. Blank-line probe: synthetic estate with a blank line before a byte-canonical live-grammar bullet ("- **Tests:** 2,303 tests collected / 352 files (2026-09-27 census, `pytest --collect-only -q`)") - exit 2, "cannot verify, no parsable **Tests:** census line".
6. `grep`/`git log` evidence runs: pytest.ini testpaths, mag/tests/ contents, `--days` consumers, census_patrol.log watchers, the 2026-09-27 AGENTS.md refresh commit.

## 2. v1 inventory: what the patrol meters today

The patrol is one carrier (AGENTS.md "**Tests:**" bullet, `CARRIER_RELPATH`, census_drift_patrol.py:76) metered by two rungs and two consumers:

- Default gate (dependency-free, pre-push): carrier exists (:302-304), claim parses in the canonical grammar (:305-309, regex :117-119, B2-245 clause anchoring), census date not future (:310-312), commit-added test files strictly after the census day (:219-247), disk candidate shrink below the claim (:261-263); STALE = age > 7 days AND growth (:264-265), constants at :78 and :125.
- Deep check (`--collect`, B2-244): reruns `pytest --collect-only -q` under the executing interpreter (census_collect.py:61-84), enforces the collected claim against a symmetric bar of 20 (:197-216), names the zero-collect instrument gap and the files delta every run (patrol :356-362, B2-247).
- Consumers: githooks/pre-push (exit 1 WARN-ONLY, exit 2 blocks the push with evidence at .git/census_blind_last_push.txt, B2-277, hook :78-97; first-line lowercase contract B2-338, :67-75, :89-90) and the MagCensusPatrolDaily scheduled task at 08:30 (scripts/census_patrol_daily.ps1, B2-246), whose wrapper also carries meter patrol, fleet task doctor, and fossil check steps.
- Self-test and tests own frozen regression vectors under the B2-274 ownership law (selftest:3, tests:2): parser grammar lives in CENSUS_CLAIM_RE plus its comment block; vectors are never auto-synced to the live bullet.

## 3. Two live defects found by probing (v2 must-fix)

### D1. Blank line before the bullet blinds the parser (fail-closed, but with a lying message)

`CARRIER_LINE_RE = r"^\s*[-*]\s*\*\*Tests:\*\*"` (census_drift_patrol.py:83) uses `\s*`, which matches newlines. When the bullet is preceded by a blank line, `^` anchors at the blank line's start, `\s*` consumes the newline into the bullet, and `match.start()` lands ON a newline character. The line extraction at :161 (`text.find("\n", match.start())`) then finds that same newline at offset 0 and slices an empty string, so `CENSUS_CLAIM_RE.search("")` is None and parse_carrier returns None. Probe 5 proves it: a byte-canonical live-grammar claim after a blank line exits 2 with "need the claim shape" - the shape is fine; the layout broke the extractor. Consequences under B2-277: a markdown reflow of AGENTS.md (an ordinary edit) blocks every push with a misleading message, and the daily check goes BLIND.

Why no fixture caught it: every frozen vector in selftest (:40-42, :51-52, :69-71, :155-158, :173-176) and tests (:45-53) has the bullet as the first line or directly after non-blank content, exactly the B2-274 blind spot the ownership law warns about (frozen vectors cannot see live-carrier reflow).

v2 fix: change the line regex to `^[ \t]*[-*][ \t]*\*\*Tests:\*\*` (horizontal whitespace only), or extract by scanning back from the match to the bullet's own line start. Add one frozen vector per surface with a blank line before a canonical claim (must parse) and one with a blank line before a malformed claim (must still exit-2 None). Spec change lands in the :97-116 ownership comment block first, with this file as receipt.

### D2. FUTURE_TOLERANCE_DAYS is dead code and its comment asserts behavior that does not exist

The constant (:79-80) documents "tolerated clock skew for a census dated slightly in the future". run()'s gate (:310) allows a date up to today+1 to pass, but then patrol() (:266-268) returns UNVERIFIABLE exit 2 for any negative age. Probe 4 proves it: today+1 exits 2, "census dated -1 days in the future (fabrication smell)". Net behavior: ANY future census date is exit 2, which is what the module docstring (:26-28) actually claims, so the docstring and behavior agree and the constant plus its comment are the false surface. v2: remove FUTURE_TOLERANCE_DAYS, tighten the run() gate to `parsed["date"] > today`, keep patrol()'s negative-age branch as the sole future guard. Behavior is byte-identical (both probes' paths are exit 2 before and after), verified by the probe evidence above; the frozen vectors at selftest:100-101 and tests:169-170 still pass.

## 4. v2 additional checks (the ask: what should exist)

### A1. Dark-day heartbeat for the scheduled surface (highest value)

The log shows no 08:30:02 entry for 2026-09-28; the day's only run is 17:20:35 (hand-fired shape). The documented response for a dark surface is operator-visual: "No START stamp for today in this log" (census_patrol_daily.ps1:28-30). Nothing automated watches for absence: the fleet task doctor (ps1:121-157) runs INSIDE the daily script, so it cannot fire on the day the script never runs; the only other reference to the log is prose (tools/rumor_drill.py:59). A missed day is invisible until a human reads the log. v2: a second tiny scheduled task (different trigger, e.g. MagCensusHeartbeat 20:00) that exits 1 when logs/census_patrol.log has no START stamp dated today, alerting to memory/attention.md through the same block pattern. This is the direct census analog of the FTS law's "no START stamp means the surface is dark" clause (AGENTS.md B2-465 bullet), which also currently relies on the operator noticing.

### A2. Enforce a files-claim bar (the files dimension is named every run and enforced never)

The deep check prints "files: collected N vs carrier claim M" (:362) but only the items count feeds the verdict (:363). Live evidence the gap is real: the carrier's own census day, 2026-09-27 08:30:02, read "files: collected 350 vs carrier claim 352" (log), and the 352 was committed at 01:10 EDT that day (commit e73b60c54: "AGENTS.md census carrier refreshed 2,303 collected / 352 files ... patrol --collect exit 0") with no log witness of the refresh collection - the only byte-witnessed files count that day is 350. Today the same pair reads 368 vs 352 (+16), evidence-only. v2: compare the SAME apples-to-apples pair already printed at :362 (collected item-bearing files vs claim files; never disk candidates, which are candidates-not-items by B2-247 semantics) and fail COLLECT-DRIFT when the delta crosses a FILES_DRIFT_TOLERANCE (suggest 10, operator call). This would have named the 352-vs-350 as a violation on the claim's own census day instead of as an evidence line.

### A3. Carrier uniqueness

parse_carrier takes the FIRST "**Tests:**" bullet (`CARRIER_LINE_RE.search`, :158); nothing counts. A merge-conflict resolution or a lane edit that leaves two Tests bullets makes the patrol silently meter whichever is first while the second sits unwatched. v2: `len(CARRIER_LINE_RE.findall(text)) > 1` is exit 2 cannot-verify (two carriers is an ambiguous instrument, not a census). One frozen vector each way.

### A4. Pin the collection universe (disk candidates and collected files must share a world)

Disk candidates are pytest-named files under tests/ only (:120, :173-179). Collected files are whatever pytest collects (census_collect.py:47-58), which on this repo means pytest.ini's `testpaths = tests` (pytest.ini:2) - the two universes coincide only by config. The repo already holds test files outside the universe (mag/tests/test_identity_schema_portability.py, mag/tests/verify_identity_coupling.py on disk) that the census counts neither as candidates nor as collected. If testpaths ever widens, the :356-362 gap math silently misattributes (files collected outside tests/ look like negative gap, never like a universe change). v2: after a deep run, assert the collected file set is a subset of the candidate universe and exit 2 (instrument changed, cannot verify the gap math) when not; or derive candidates from the collection's directories. Cheap, fail-closed, one vector.

### A5. House subprocess law on the patrol's own spawns

The tool spawns git (census_drift_patrol.py:227-230) and pytest (census_collect.py:72-77) without `creationflags=CREATE_NO_WINDOW` on win32, while the repo's own test file carries the flag on every spawn (tests/test_census_drift_patrol.py:198-202, 240, 251, and the rest). Headless scheduled runs are unaffected, but any GUI-hosted invocation flashes console windows. v2: add the same guard constant both sites. Trivial, aligns the tool with the house law its own tests already follow.

### A6. Spec-number parity between the carrier bullet and the tool constants

The AGENTS.md bullet restates the bars in prose: "older than 7 days" and "20 or more off" (AGENTS.md:27). The code holds CENSUS_STALE_DAYS = 7 (:78) and COLLECT_DRIFT_TOLERANCE = 20 (:125). Two specs of one mechanism drift silently if either changes. v2 (pick one): a warn-level parity check that greps the bullet for the two numbers and compares them to the constants; or slim the bullet to point at the tool plus receipts and stop restating numbers. The parity check is cheaper and keeps the bullet self-contained for seats that never open the tool.

### A7. A machine channel (--json) to retire string contracts

The patrol currently has two output contracts held together by string shapes: the hook case-matches the lowercase first line "CENSUS-PATROL: ok" (B2-338, patrol :321-325) and the wrapper Select-Strings uppercase tokens (ps1:66, :96). B2-338 exists precisely because a string contract broke once already (uppercase OK read as WARN on every green push). v2 option, low priority: a --json flag emitting one verdict object (verdict, exit, counts, gap, added) per run; the hook and wrapper consume the object, the human-readable block stays for the log. Not urgent; list it so the next B2-338-class fix has a landing spot.

### A8. Refresh runs must leave a log witness

The 2026-09-27 01:10 carrier refresh (e73b60c54) cites "patrol --collect exit 0" in its message but the log holds no record of that collection; the next logged run (08:30) already disagreed on files (350 vs 352). The operator law requires attribution ("an unattributable drift is a fabrication smell", AGENTS.md:27), but attribution of the REFRESH itself is unwitnessed. v2: a carrier refresh runs the deep check inside the logged surface (or appends its collect tail to logs/census_patrol.log) so every claim has a byte parent. Process law, one line in the bullet, enforceable by A2's bar making mismatches loud.

## 5. Redundancy rulings (the ask: what is redundant)

- R1. Self-test vs pytest vector duplication (selftest:40-129 mirrors tests:58-171, 334-383): INTENTIONAL, keep. B2-274 (selftest:3, tests:2) makes the two frozen surfaces the point: the self-test runs without pytest on the CLI path, the tests run under CI. Not redundant, but both proved blind to layout (D1), so each gains the blank-line vector named there.
- R2. Gap naming AND files-delta line both print on every deep run (:356-362): keep both. The gap names zero-collect candidates (instrument property), the delta names carrier movement (claim property); B2-247 mandates the naming, and today's log used both productively (1 zero-collect candidate; 368 vs 352).
- R3. Disk candidate scan in the default path: NOT redundant with --collect. Pre-push never runs pytest (docstring :37-38); the disk scan is the only byte-growth witness on the fast path (shrink direction, :261-263) and feeds the instrument-lag evidence line. Keep.
- R4. The grew-list print cap at 10 (:326-329): fine as evidence-only output; the count line names the total. No change.
- R5. The retired fossil grammar inside CENSUS_CLAIM_RE (:93-95, "N tests / M files" without "collected"): KEEP with the tradeoff stated, which today it is not. Removing it would flip a fossil-shaped carrier from exit-1 STALE (WARN-ONLY, push proceeds) to exit-2 BLIND (push blocks, B2-277). The parseable fossil is the gentler path; the comment block should say so explicitly so a future cleanup does not "simplify" it into a harsher gate.

## 6. Removal candidates (the ask: what should be removed)

- X1. FUTURE_TOLERANCE_DAYS (:79-80) plus the tolerance branch in the run() gate (:310): remove, per D2. Byte-identical behavior, probe-proven; the comment stops asserting a skew tolerance that has never been honored.
- X2. The --days flag (:377-378, usage :34): zero consumers found - githooks/pre-push and census_patrol_daily.ps1 invoke with no flags, tests never pass it; only the usage string mentions it. Low stakes either way; remove for no-orphan-surface discipline or keep as a documented dev knob, but then name a consumer. Removal recommended.
- X3. Considered and REJECTED for removal: the patrol core's disk-over-direction "instrument lag" branch (:283-286) - it looks like noise but it is the named evidence that stops the over-direction from firing forever (the pre-B2-247 disease, tests:148-156); and the `line` key in parse_carrier's return (:169) - it is pinned contract (tests:58-62 asserts the full dict).

## 7. Fail-closed / fail-open balance (the ask)

- B1. Tool core: fully fail-closed. Every cannot-verify maps to exit 2, never a pass: missing carrier (:302-304), unparsable grammar (:305-309), future date (:310-312 + :266-268), git failure (:231-232), collect failure (:78-80 in census_collect.py, mapped at :346-349), no parsable tail (:81-83), pytest timeout (:350-352). Verified by tests (:300-329, :470-486) and by both probes this session. No fail-open path found in the tool itself.
- B2. Hook: the B2-277 exit-class split is sound and well-argued (hook :78-86): exit 1 means the gate SAW the carrier and can name the disease (WARN-ONLY, t40 precedent, the push may carry the fix); exit 2 means the gate saw NOTHING (blocks, with on-disk evidence). Blind-worse-than-stale is the right axiom.
- B3. The one true fail-open hole: the hook SKIPS when AGENTS.md is missing (hook :77, :100-101, "skipped, no AGENTS.md"). The tool itself exits 2 on a missing carrier (:302-304), but the hook never reaches the tool in that case, so deleting or renaming the carrier silences the census gate entirely and the push proceeds on one printed line. v2: treat missing-carrier as BLIND (run the tool anyway and let its exit 2 block, or branch the skip into the exit-2 arm). The freshness gate has the same shape for its own dir; this item scopes the census block only.
- B4. Wrapper layering is correct: missing venv exits 2 (ps1:47-50), null exit reads as 2 (ps1:62-63), census and meter fold worst-code-wins (ps1:190-192), and the doctor plus fossil check hard-catch their own errors WARN-ONLY with the law stated ("a broken doctor must never blind the census/meter steps", ps1:119-120; same for fossil, :163-164). Keep.
- B5. Wrapper verdict extraction is fail-open-adjacent: the alert blocks grep the WHOLE log and take the last match (ps1:66 for "COLLECT-DRIFT|STALE|cannot verify", ps1:96 for "METER-PATROL: (GAP|cannot verify)"). When today's failing step did not print a token (census green, meter red), today's alert can cite a PREVIOUS day's verdict line as its verdict - the log already holds multiple historical COLLECT-DRIFT lines (09-26 11:33 and 09-28 17:20), so the wrong-day citation is reachable. v2: anchor extraction to the current run's block (lines after this run's START stamp), which the log's per-run START/END stamps (ps1:52, and END at :194) already delimit.
- B6. Net verdict: the balance is strongly fail-closed at the instrument (B1) and thoughtfully split at the consumer (B2), with exactly two fail-open edges to close - the missing-carrier hook skip (B3) and the dark-day absence nothing watches (A1) - plus one fail-closed-with-a-lie to fix (D1's misleading message).

## 8. OWED (stated, not done here)

- O1. The live estate is in COLLECT-DRIFT as of the 17:20:35 run today: pytest holds 2410 vs carrier claim 2303 (+107), files 368 vs 352, 1 zero-collect candidate (tests/test_selffeed_integration.py). The refresh belongs to the operator or the landing lane WITH attribution (the five 09-28 test files this session's live run names are the visible candidates); an unattributable refresh is a fabrication smell per the bullet's own law. I did not refresh the carrier: this item's charter is design, and the attribution law forbids a blind bump.
- O2. D1 and D2 fixes are code changes owed against this spec (spec-before-behavior), each with the frozen-vector additions named in D1 and the probe evidence above as the falsifier pair.
- O3. Why the 08:30 MagCensusPatrolDaily run did not fire on 2026-09-28 is NOT verifiable from the log alone (machine off, logged out, or deregistered are all consistent with the gap); the 17:20:35 run used the same script and log. Unknown, stated as unknown; A1 is the instrument that would have answered it.

## 9. Receipt

Commands run this session are listed in section 1; probes were temp estates under the Windows temp dir, removed after the runs. No repo file other than this receipt was modified. Em/en dash scan of this file: run post-write, reported in the item result. Live patrol, self-test, and deep-check log lines quoted verbatim in sections 1 and 8.
