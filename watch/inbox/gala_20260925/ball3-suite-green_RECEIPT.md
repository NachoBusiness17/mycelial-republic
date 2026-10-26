# RUN RECEIPT: ball3-suite-green

- Gala: gala_20260925
- Slug: ball3-suite-green
- Written: 2026-09-29, herald receipt seat
- Receipt path: watch/inbox/gala_20260925/ball3-suite-green_RECEIPT.md
- Source: the script-written sections pasted into the filing ask, marked authoritative. Numbers below are those script numbers verbatim; narrative detail comes from the ask's metadata, fold, review, and filing blocks. Nothing here is re-derived or invented by the receipt seat.

## Header / gate

GATE PASS

Authoritative script sections:

- lanes_json_count: 3 (expected 3)
- lanes_parsed_ok: 3/3
- by_division: {"B": 3}
- byte_checks_cited: 18, mined_rows: 3
- decisions_changed: 3
- ballroom_count (danced/refired/buried): 3/0/0

## Scoreboard

Division B: 3 danced / 3 total, 0 refired, 0 buried. (fold scoreboard; metadata lists danced=3, refired=[], buried=[])

| Lane | Div | ok | rows mined | Standout (fold scoreboard) |
|---|---|---|---|---|
| driver-meter | B | true | 3 | closed all four driver/meter failures at root and met its finish line (35 passed at BOTH basetemps, the 4 named tests green, the live driver's production mutex probe-verified still held, the ratchet default-attribution pollution hypothesis refuted by byte census) |
| live-state | B | true | 0 | decided the config-seal-trio smell as CODE never seal state (52 passed x2, one repo-root-relative display-path class masked all suite life by conftest.py:14's in-repo default; 5 LINKS rows registered by-name with ledger bytes untouched) |
| quantizer-fallout | B | true | 3 | closed as already-banked in commit 93f85e0dd with zero edits (62 tests passed; full suite 2F/2566P, both survivors re-routed to sibling lanes) |

Grounding (fold scoreboard text): gate sections from the ask are authoritative; the reviewer ran ls on watch/inbox/gala_20260925/ball3-suite-green/lanes (exactly 3 lane .json files), read all three, confirming 3/3 parsed ok, by_division {"B": 3}, checks blocks 7+6+5=18 matching byte_checks_cited: 18, and mined_rows: 3 = the three law rows in quantizer-fallout.json. This receipt seat re-ran the ls on the same directory this ask and saw exactly driver-meter.json, live-state.json, quantizer-fallout.json plus check/register evidence files (driver-meter.check.txt, live-state.check.txt, live-state.register.py, quantizer-fallout.check.txt, quantizer-fallout.fullsuite.txt).

## Decision ledger

Parade: NO (fold carries "parade": false). Three decisions changed, no parade.

1. driver-meter.json: ball3 suite-green closes the four driver/meter failures; the instance-lock test surface is made live-driver-proof by lock namespace while the production lock stays strict (probe-verified InstanceLocked); the relative_to-out-of-repo defect class is fixed at root in tools/stealth_driver.py, mag/agent_state.py, tools/violation_ratchet.py; the ratchet register default-attribution pollution hypothesis is refuted by byte census (no by=operator entries, stamps only under named accepters).
2. live-state.json: the config-seal-trio smell ("seal file state vs code") is decided as CODE, never seal state; the trio + dead_hand + voice_turn failures were one repo-root-relative display-path class exposed only under an external --basetemp (conftest.py:14's in-repo default masked it for the suite's whole life), so ball3 can certify suite-green on these six tests; the ball close still owes the 3-file named-act re-seal; the durable practice is full-suite honesty runs on an external basetemp. Held, not changed: LINKS drift is absorbed by the B2-168 register-by-name path (9th grandfathered entry), never by editing the ledger.
3. quantizer-fallout.json: the 42:05 post-ball owed work is closed as already-banked (healed atomically in hygiene commit 93f85e0dd), and the ball's suite-green gap is re-routed to its real owners: the 2 remaining failures are game-world optics plus the driver-meter lane's namespace-less lock test, not quantizer fallout.

### Top laws mined (3, from the fold)

1. live-process-mutex-poisons-lock-tests: the full suite's one surviving lock failure is exactly this law in action, since tests/test_stealth_tools_wave5_repair.py:128 still acquires the production mutex namespace-less while the namespace escape the driver-meter lane added already exists for any test to take, so every run with the live stealth driver up stays non-hermetic until the owner flips that one arg. (Note: the review found this row's premise stale at its write time, see review verdict, last bullet.)
2. fallout-premise-needs-a-receipt: the dispatch alleged 9 stale-shape failures with no suite receipt; the lane's byte-check showed all 9 green at HEAD (healed in-commit by 93f85e0dd) and the 2 real failures belonged to sibling lanes, so an unreceipted fallout premise burns a fix lane re-verifying ghosts while the real failures hide in other lanes' territory.
3. hygiene-lane-owns-its-skew: commit 93f85e0dd bumped the compiled-v0.3 to compiled-v0.4 marker and its test assertions in the same commit (grep for compiled-v0.3 across tests/ mag/ tools/ returns zero hits), which is precisely why the fallout premise was false; keeping marker bump and assertion update atomic is the pattern that keeps it false.

## Refired

None. (metadata refired: [])

## Buried

None. (metadata buried: [])

## Review verdict

ACCEPT. (review seat findings, from the ask)

- QUOTES: all 3 byte-match, modulo soft line-wraps. Q1 = tools/thought_quantizer.py:21-22 joined; Q2 = exact diff line in `git show 93f85e0dd` and live at tests/test_thought_quantizer.py:97; Q3 = tools/stealth_driver.py:729-733 docstring (the driver-meter fix's own receipt comment). grep -F missed only across newlines; joined content is faithful.
- BYTE-CHECKS BACKED: driver-meter.check.txt carries CHECK 1-7 matching the JSON (35/35/4/35 passed, ratchet PASS NEW=0; CHECK 7 honestly discloses grep-rc-instead-of-pytest-rc); live-state.check.txt carries RUN1-4 (52 passed x2, seal FAIL, ratchet FAIL); quantizer check.txt 62 passed + fullsuite.txt exactly "2 failed, 2566 passed, 12 skipped" naming the same two failures. Two live-state checks (register scan, compile_intention probe) have no .check.txt capture, but the reviewer verified them independently on disk: register row seq 1790707788389165800 in index_events.jsonl, links_kind_baseline.json sha256 85bdad32... / 4584 bytes exact, recomputed LINKS-JEEVES line sha 02446bef... exact, 9 grandfathered entries, LINKS.jsonl git diff vs HEAD empty (no-erase held).
- DECISION LEDGER HONEST: every decision names things the reviewer confirmed on disk: stealth_driver.py:726-738 namespace param + :460 _rel_posix (used :548/:643), agent_state.py:177/:425-426 _display_path, violation_ratchet.py ~:300 print fix, config_seal.py:89-100 + dead_hand.py + voice_handoff.py:289/:352 fixes all present with receipt comments; the ratchet pollution refutation is true (reviewer census: zero bare "by": "operator" accepters, all 900+ stamps under named accepters); commit 93f85e0dd real and touches the quoted test. One wrinkle: live-state JSON check-3 evidence says seal "modified=3" but its own cited check.txt RUN3 says "modified=4" (adds links_kind_baseline.json), an undercount vs its receipt, not decision-corrupting (both agree re-seal owed).
- B-DIVISION FINISH LINES MET: driver-meter (CHECK 1/2/3/6 in receipt, matching counts), live-state (52 passed exit 0 x2 both basetemps), quantizer (62 passed FINISHLINE_EXIT=0 + full-suite receipt). The reviewer re-ran the fold gate: `bash fold_gate.sh ball3-suite-green/lanes 3` -> 3/3 parsed, by_division {"B":3}, 18 byte_checks_cited, ballroom 3/0/0, GATE PASS rc=0. One unverifiable detail: driver-meter's "heartbeat advanced cycle 28 (18:29Z) to cycle 30" (cycle 30 @18:42:25 is in check.txt but cycle 28 is no longer on disk; state/fuel/stealth_driver.jsonl now holds only cycles 33-36, 19:02-19:19Z, which independently confirms the driver still running).
- NO WORK THEFT; ONE STALE CLAIM: quantizer's rows explicitly attribute the hygiene commit (ball-20260929 quantizer-hygiene) and the namespace escape (ball3 driver-meter), not claim them. But quantizer row 3 asserts tests/test_stealth_tools_wave5_repair.py:128 "still acquires namespace-less": stale vs disk, the test now acquires in pid-unique namespace (lines 127-140), and driver-meter's CHECK 3 passed it at 18:46Z, before quantizer's 19:14Z JSON; the claim was true only of quantizer's 47-min full-suite snapshot (started ~18:25Z). Honest in attribution, outdated at write time; the row's own falsifier condition was already satisfied by driver-meter's CHECKs.

## Filing verdict

DONE. (filing seat, from the ask)

- LINKS rows: the filing seat read all three lane JSONs in watch/inbox/gala_20260925/ball3-suite-green/lanes/ (driver-meter.json, live-state.json, quantizer-fallout.json; the dir holds exactly these 3 lane JSONs plus check/register evidence files). Dedupe first: grep 'ball3-suite-green' in memory/corpus/LINKS.jsonl returned 0 matches (ledger 198 rows); the append script re-checked srcs against the parsed ledger before writing. Appended 3 rows, kind 'gala', slugs GALA-ball3-suite-green-driver-meter / -live-state / -quantizer-fallout, src watch/inbox/gala_20260925/ball3-suite-green/lanes/<lane>.json each, lane 'gala-20260925/ball3-suite-green/B'. Titles: driver-meter 'instance-lock-test-namespace' (the top law per the ask; the lane JSON itself has no top key, so the ask's claim + falsifier are carried in the row note); live-state title = its changed decision (top null per ask; 0 law rows mined, rows:[] in lane JSON); quantizer-fallout 'fallout-premise-needs-a-receipt' (its top/first row; 3 rows mined, the other two named in the note). decision_changed copied verbatim from each lane JSON. Post-append: ledger 198 -> 201, whole-ledger re-parse OK (all 201 lines parse), em-dash byte scan on the 3 appended rows CLEAN.
- STATE entry: the filing seat appended ONE entry ("BALL3 CLOSE 2026-09-29 19:33Z - GALA ball3-suite-green banked") to memories/session/next-window-handoff.md after its BALL CLOSE 17:10Z entry: danced 3 (all lanes ok:true; no fold_gate output exists in the ball3-suite-green dir, so the basis is the lane JSON ok flags, no refired/buried split), decisions changed 3 (lock-namespace test surface with production strictness probe-verified; config-seal-trio smell decided CODE never seal state with the B2-168 register-by-name second decision held; quantizer fallout premise killed as already-banked in 93f85e0dd), B-division finish 3/3 (all three lanes division B, ok per lane JSON; driver-meter finish_line met true), graves filed 0 (no ball3 graves/ dir and no GALA_GRAVE_* for ball3; only ball2's 19 exist, verified by find), plus owed set (3-file named-act re-seal, game-world optics failure, two live stealth driver pids). Entry occurs exactly once, contains 0 em-dashes; the 56 em-dashes in the file's pre-existing historical entries left untouched (append-only).
- Not run by filing: the lanes' pytest batteries were not re-run; those results are cited from the lane JSONs and their check files as the ask directed.

## Checks run by this receipt seat (herald)

1. `ls C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/gala_20260925/ball3-suite-green/lanes` -> 8 entries: driver-meter.check.txt, driver-meter.json, live-state.check.txt, live-state.json, live-state.register.py, quantizer-fallout.check.txt, quantizer-fallout.fullsuite.txt, quantizer-fallout.json. Exactly 3 lane .json files, consistent with lanes_json_count: 3.
2. Wrote this receipt to watch/inbox/gala_20260925/ball3-suite-green_RECEIPT.md.
3. Em-dash byte scan on this receipt file, via the repo venv interpreter (`.venv/Scripts/python.exe`, byte counts of the UTF-8 sequences): output was `bytes: 12151`, `U+2014 em dash: 0`, `U+2013 en dash: 0`. CLEAN.

Everything else in this receipt is cited from the ask's authoritative script sections, metadata, fold, review, and filing blocks; it was not re-executed by this seat. Not run here: the lanes' pytest batteries, the fold gate rerun, the LINKS append, and the disk verifications (all performed and reported by the fold, review, and filing seats as quoted above).
