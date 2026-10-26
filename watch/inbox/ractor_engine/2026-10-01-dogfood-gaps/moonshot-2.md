# moonshot-2: dogfood ride on GAP_REGISTER.md (watch/inbox/gap_analysis_20261001/)

2026-10-01, moonshot lens. Every claim below was byte-checked this session against the live
tree; commands and outputs are named inline. Anything I could not verify is marked OWED.

## Verdict

The register is honest and mostly right, and it is already stale at row 1 with no mechanism
to know it. 24h after landing: 1 of 12 rows is code-fixed (rank 1, by the audit wave's own
commit), 1 is half-fixed (rank 8, healed as a side effect of the day-2 index rebuild while
the workflow law stays unamended), and 10 rows byte-verify untouched, including every pure
one-sitting fill. Meta-gap 1 (MINED-NEVER-SCHEDULED) dominates, and the register itself is
now its newest specimen: a ranked, costed, owner-assigned schedule that did not get fired.
It is also, by its own rank-8 diagnosis, a NOT-INDEXED artifact: grep -c
"gap_analysis_20261001" watch/inbox/INDEX.json = 0.

## Row-by-row byte truth (checks I ran this session)

- rank 1 EstateWalkDaily: FIXED IN CODE, PROOF INCOMPLETE. scripts/estate_walk_daily.ps1:5-13
  carries the PATH LAW comment and absolute $repo; logs/estate_walk_daily.log ends
  "END 2026-10-02T00:37:54Z exit=0" (hand smoke, 9 min before commit 5d2263f10 at
  2026-10-01 20:46:30 -0400). But `schtasks /Query /TN EstateWalkDaily /V` still reads
  "Last Result: 1" (the pre-fix 10-01 09:15:01 fire) and Next Run 10/2/2026 9:15 AM: the
  fix has NOT been proven on the actual failure surface (Task Scheduler CWD System32).
  The fill spec's receipt beside watch/inbox/48h_synth/ does not exist (dir holds only the
  five 09-30 story files plus .mimosa); the newest watch/inbox mention of the task is
  GAP_REGISTER.md itself. Receipt: OWED.
- rank 2 elder lens: STILL REAL AND NOW TOP SEVERITY. queue/lanes/elder/inbox.jsonl is
  0 bytes, mtime Sep 4 10:43, while the register puts the card's falsifier clock at ~10-02.
  With rank 1 fixed, this is the only S1 with a hard clock and a 20-minute cure.
- rank 3 citation_lint: STILL REAL. tools/citation_lint.py does not exist (ls: no such file).
- rank 4 191.8M ERRATA: STILL REAL. watch/inbox/48h_synth/STORY.md lines 238-242 still carry
  "191.8M tokens spent"; grep -c "191" frontier_olm_20260928/DIGEST.md = 0; no ERRATA file
  anywhere under watch/inbox (find maxdepth 2 -iname "*ERRATA*" = nothing).
- rank 5 seal gates: STILL FULLY UNARMED. ~/.mag contains only steer_seal_seen/;
  mag/seed_seal.py and tests/test_seal_forge_drill.py do not exist; find for "*.seal"
  repo-wide returned zero sidecars.
- rank 6 percolator intake: STILL REAL. grep "candidates" mag/percolator.py = 0 matches;
  memory/percolator/invariants.json (mtime Oct 1 19:17, moved today by something else)
  contains grep -c "frontier_olm" = 0 rows.
- rank 7 day-1 fold: STILL REAL. watch/inbox/frontier_olm_2026-09-30/ holds only lens/,
  steal/, sweep/ subdirs; no DIGEST.md, no register.jsonl, no percolator_candidates.jsonl.
- rank 8 index-last: HALF-FIXED, DISEASE RE-ARMED. INDEX.json now contains register.jsonl
  (2 hits), percolator_candidates.jsonl (1), quantization-compression.md (2): the day-2
  heal (commit 2093ca518, "window rows 0 to 37") covered the symptom. But
  .zcode/workflows/olm-mine.dwf.ts has no "index last, write first" amendment; its only
  case-insensitive INDEX match is `indexOf` at line 259. Day 3 fails the same way.
- rank 9 KVarN: STILL REAL. grep "2606.03458|KVarN" ARXIV_REGISTER.json = 0, file mtime
  still Sep 29 05:59.
- rank 10 trio: STILL REAL. The OWED ledger card is at
  watch/inbox/frontier_olm_2026-10-01/steal/quantization-compression.md (the register's
  "steal/quantization-compression.md" pointer omits the card prefix); it has 0 hits for
  1sy7srk and 0 for 2609.21341.
- rank 11 three tickets: STILL REAL. watch/inbox/hermes_burn/TICKET_LEDGER.md exists
  (10,140 bytes, mtime Oct 1 17:35) with zero SS-1, CP-1, R2-1 rows (grep = no match).
- rank 12 Vulkan probe: STILL REAL as far as surfaces show. watch/inbox/spiking_wide/ holds
  the eight original sweep files, no probe receipt. I did not (and cannot) verify on the
  RX 5600 XT box itself; whether a probe ran off-repo is OWED.

## Findings (full statements)

1. MISRANKED POST-FIX. Rank 1 is fixed and rank 2 is the live S1: the only row whose
   falsifier clock closes ~10-02 carries a 20-minute cure and 0 bytes of progress. Under
   the register's own law (severity x fill-ease) the elder lens salvage is now rank 1.
2. NEW GAP THE REGISTER MISSED. The rank-1 fix left the success channel byte-invisible:
   logs/estate_walk_daily.log is UTF-16LE (od shows FF FE BOM, null-interleaved bytes) from
   the PowerShell `>>` redirect at estate_walk_daily.ps1:18, while Add-Content (lines 20, 23)
   writes ANSI; `grep -c END` on the log returns 0, exit 1. No ASCII grep instrument, the
   estate's standard patrol shape, can ever see an END line, healthy or failed. The a08
   below-cut note ("third failure shape: red AND silent") is still armed in new clothing:
   the detector that would catch a silent failure cannot read the channel it must watch.
3. META-GAP 1 DOMINATES AND ATE ITS OWN CURE. The register ends "the next 100M-token job is
   a schedule-and-fire pass", then demonstrated the disease on itself: the register IS the
   schedule, and 10 of 12 rows stand untouched inside 24h. Firing, not ranking, is the
   bottleneck; another register (or another audit of this one) is more of the disease.
4. THE REGISTER VIOLATES THE CONTRACT IT ENFORCES AND CANNOT AGE. It is unindexed in the
   shared surface it polices (INDEX.json grep = 0) and every still-real row is a moment-bound
   byte state with no re-verification loop, exactly the trap its own negative finding names
   ("true at its moment, false at mine"). The 10x move: make the register executable, a
   tools/gap_register_check.py that reruns each row's byte-falsifier (the checks above, all
   scriptable) and stamps FIXED / STILL-REAL / OWED, on a daily schtask like
   census_drift_patrol, plus one sanctioned-writer run to index gap_analysis_20261001/.

## One-sitting moves

1. Stamp rank 1 FIXED-PENDING-FIRE in the register with a status column, bank the missing
   receipt beside watch/inbox/48h_synth/, and fire the elder lens salvage now (fill 2).
2. Re-encode the bake log to UTF-8 (explicit -Encoding on the redirect and Add-Content),
   re-smoke, prove `grep END` returns 1, amend the receipt.
3. Amend olm-mine.dwf.ts with "index last, write first"; schedule the ten pure one-sitting
   fills as fired asks with per-row receipt paths.
4. Build tools/gap_register_check.py (per-row byte-falsifier, status stamp, daily task) and
   index gap_analysis_20261001/ through the sanctioned writer.

## HOSTILE-PASS CORRECTIONS (2026-10-01, second pass)

The hostile pass weakened findings 3 and 4. Re-examined against the bytes; both corrected.

CORRECTION TO FINDING 3. The "24h after the register landed" frame is FALSE and the
specimen indictment ("the register is the disease's newest specimen") is WITHDRAWN. Real
timeline, byte-checked: GAP_REGISTER.md mtime 2026-10-01 18:41:58.062 -0400
(ls --time-style=full-iso), commit 5d2263f10 at 20:46:30 -0400, lens ran ~22:50 EDT:
roughly 2.1h post-commit, 4.1h post-write. I conflated the burst's age (the 09-30/10-01
gap states are 24-48h old) with the register's age (hours). Count also corrected: 9 rows
byte-verify untouched (ranks 2,3,4,5,6,7,9,10,11), rank 12 is surface-only. What survives:
the register's content is byte-accurate at re-check (this pass re-ran elder inbox 0 bytes
mtime Sep 4 10:43, KVarN grep 0, ERRATA find 0, ticket grep 0), and mined-never-scheduled
stands as the dominant live class. What is withdrawn: any claim that the register-as-
schedule failed. At +2h no firing window has elapsed; untouched rows prove accuracy, not
schedule-failure. The indictment is now prospective: it upgrades to proven only if all 9
byte-verified rows still stand after one full firing window consumes the register as its
lane table.

CORRECTION TO FINDING 4. The NOT-INDEXED core is WITHDRAWN: the register IS indexed at
birth. watch/inbox/index_events.jsonl:8183 holds {"op": "register", "file":
"gap_analysis_20261001/GAP_REGISTER.md", "sha256": "33ad2a6d...", "writer":
"md-record-seal"} and :8184 holds the autoseal (bytes 16660, same sha), both ts
2026-10-01T22:41:58+00:00 = the exact write moment. INDEX.json's own header declares:
"INDEX.json is now DERIVED from the append-only event log index_events.jsonl ... The log
is the source of truth." My grep hit the derived view, whose mtime 18:00:56.968 EDT
predates the register's write by 41 minutes: a false zero. My blind spot ("I grepped, I
did not parse its schema") is exactly where it broke, and the phantom I generated is
itself a live specimen of the register's meta-gap 3: instruments, not only documents,
produce phantom citations from stale derived views. Surviving legs, re-confirmed: the
register has no status column and no re-verification loop (whole-file read, 247 lines);
olm-mine.dwf.ts carries no index-last amendment (grep -inc INDEX = 1, the single match
indexOf at line 259); rank 8's heal is symptom-only. New sharpened leg: any patrol that
checks index state must grep index_events.jsonl (the log), never INDEX.json (the view,
observed lagging 41 minutes). The gap_register_check.py move survives with the log-first
rule; the "sanctioned-writer run to index it" half is moot and dropped.

## Blind spots (honest)

I trusted the register's sibling-lane quotes (a01-a08) and did not re-read the lane JSONs;
my checks target current tree state, not lane fidelity. I adopted the elder card's ~10-02
clock terms from the register and next.md adjacency without reading the card's own falsifier
text. Workers may hold in-flight bytes for ranks 3/5/6/9 that simply have not landed. I
could not verify the rank-12 probe off-repo, could not force the 10-02 09:15 scheduler fire
early, and did not run the percolator, pre-push gate, or any test suite in this session (no
check in this ask named one). NEW, paid for above: I treated a derived artifact (INDEX.json)
as ground truth without reading its header, and I read a duration off the burst's age
instead of the register's mtimes. Both errors are the register's own meta-gaps acting
through the auditor.
