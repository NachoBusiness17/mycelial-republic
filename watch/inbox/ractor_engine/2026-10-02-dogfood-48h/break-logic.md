# BREAK-LOGIC: hostile second pass on the dogfood-48h lens report

Run 2026-10-02-dogfood-48h, break pass on the lens report whose five findings
were handed to me verbatim. Sitting moment 2026-10-02T11:13:02Z (powershell
Get-Date). Every check below was run this sitting on the CURRENT tree; commands
and outputs named. No em-dashes. The lens report's fifth finding arrived
truncated mid-evidence in my input; its verdict covers the visible bytes only.

## Verdicts

### F1 GAP_REGISTER write-once vs commits claiming closure: CONFIRMED

- Register table: 12 data rows at watch/inbox/gap_analysis_20261001/
  GAP_REGISTER.md:74-85, columns rank|gap|lane|sev|fill cost|owner, no status
  or closed column. Row 1 at :74 still reads "repeats 10-02 09:15 with the
  same relative-path defect" while commit 5d2263f10 (message read this
  sitting, git show -s) claims the EstateWalkDaily fix smoke-proved before
  that fire. Byte-true.
- LastWriteTimeUtc 2026-10-01T22:41:58.0623825Z (powershell Get-Item, this
  sitting). The fill-ball commit 3c83da5b0 ("all 7 register gaps CLOSED",
  committed 2026-10-02T06:54:04Z) and e3c7d341c (07:31:54Z) both landed AFTER
  the register's last write: neither commit amended it. Still unamended at
  11:13Z, roughly 12.5h later, matching the lens's "unchanged 12h later".
- accuracy lens quote byte-true: watch/inbox/ractor_engine/2026-10-01-dogfood-
  gaps/accuracy.md:15 "register unamended; the register itself converted zero
  rows."
- grep -c fillball watch/inbox/INDEX.json = 11 (run this sitting): receipts
  registered. The register directory holds ONLY GAP_REGISTER.md (ls), so no
  sidecar annotation exists either.
- Precision the lens under-drew: the denominator IS auditable, just not via
  the register. The 7 receipts exist (ls watch/inbox/fillball/: citation-lint,
  corpus-fold-land, day1-digest, elder-salvage, errata, percolator-candidates,
  seed-seal) and name their ranks (citation-lint.md:3 "Closes GAP_REGISTER
  rank 3"). The no-adjudicator claim (no instrument states which rows are
  open) stands; "unauditable denominator" is slightly strong.
- Citation nit on the lens itself: it cited the table at ":73-84"; the data
  rows are 74-85 (:73 is the separator). Count right, range off by one, the
  exact anchor-precision class the lint polices.

### F2 lint teeth bind only to path:line anchors: CONFIRMED

- Reproduced the lens's run byte-exact: ./.venv/Scripts/python.exe
  tools/citation_lint.py check --files AGENTS.md -> "ok records=1 anchors=0
  numbers-checked=15 blocking=0 warns=0".
- Code: ANCHOR_RE at tools/citation_lint_io.py:70-73 requires ":digits";
  lint_record at tools/citation_lint.py:199-211 iterates ONLY
  ANCHOR_RE.finditer. PATH_RE (citation_lint_io.py:74-76) is consumed only by
  the numbers engine (citation_lint_numbers.py:25,35,130) as a named-source
  matcher, never as a blocking existence check. So the 15 bare pathed cites
  the numbers engine DID see in AGENTS.md were used as number sources while
  their existence was never checked: the asymmetry is exactly as the lens
  named it.
- Reproduced the probe, both grammars, temp record deleted after each run:
  - pathed anchored "watch/inbox/nonexistent_probe_dir/probe_anchor.md:12"
    -> FAIL blocking=1 PATH-MISSING, exit 1; pathed bare
    "watch/inbox/nonexistent_probe_dir/probe_bare.md" on the line above ->
    NOTHING. This matches the lens's claimed result exactly (its probe was
    the pathed grammar).
  - Added nuance the lens missed: a BARE-BASENAME anchor
    ("nonexistent_probe_file_anchor.md:12") gets WARN SHORTHAND-UNRESOLVED
    (citation_lint.py:155 routes unresolvable bare basenames to warn). The
    fully unchecked classes are precisely: any cite without a :line suffix,
    and all commit messages (no instrument reads them; nothing in tools/
    greps commit text).
- File-count instance byte-true: ls watch/inbox/ractor_engine/
  2026-10-01-dogfood-gaps/ = exactly 6 lens + 2 moonshot + 8 break files +
  SYNTHESIS.md, while e3c7d341c claims "8 lenses + 2 moonshots rode".
- "88 findings" stays uncountable: grep -oE "F[0-9]+" across the 8 rider
  files yields 20 unique ids; economics.md and moonshot-1.md contain zero
  occurrences of the word "finding" (grep -c). No deterministic scheme
  reproduces 88. OWED, correctly not asserted.
- "8 ranked moves" byte-true: numbered items 1-8 at that SYNTHESIS.md
  (lines 193-213, grep this sitting).

### F3 twin fix instance-level, disease path-level: CONFIRMED

- Whole-file scan reproduced with venv python over memory/runs/
  hermes_burn/usage.jsonl: 236 rows, 29 sub-60s same-(id,turn) pairs, last
  row 2026-10-01T21:53:52.578003Z (N1R_parables_songmap). All three numbers
  byte-exact against the lens.
- The named pairs byte-exact: A1_steer_antiforgery 0.3323 -> 0.3715 at
  7.47s (19:20:30.554 -> 19:20:38.025Z); N1_parables_songmap and
  DUEL1_hidden_5 doubled at 19:20/19:53/19:58/20:01Z.
- Pre-twin (twins born 20:40:13Z per e3c7d341c) doubled keys = exactly 6
  distinct ids: T1W2_S5_stores, T1W2_S7_mates, T1W2_S8_stealth,
  A1_steer_antiforgery, N1_parables_songmap, DUEL1_hidden_5. "At least 6
  keys" confirmed. Dollar nuance: the N1 and DUEL1 copies are costed 0.0 on
  both sides; the dollar-bearing pre-twin double-fires are A1 and T1W2 only.
- grep -n "lock|claim" tools/hermes_burn.py -> lines 152, 155, 156, 226,
  all prose or comments. No claim lock anywhere in the writer. Confirmed.
- Zero post-guard observations confirmed: guard shipped in e3c7d341c
  (2026-10-02T07:31:54Z); ledger's last row is 2026-10-01T21:53:52Z, so no
  dispatch has ridden the guard yet.
- Corroboration the lens did not cite: the ten DUEL2_train_02..14_r2
  sub-60s pairs all sit 21:39-21:53Z, INSIDE the twins' lifetime, matching
  the commit's "13 doubled keys" from the ledger side.

### F4 moves 3/5/7 unpaid, adjudicating receipts unregistered: CONFIRMED (strengthened)

- grep -cE "ERRAT|10.0031|1.0077|55.2" watch/inbox/NIGHT_CLOSE_20261002.md =
  0 hits, exit 1; LastWriteTimeUtc 2026-10-02T05:14:18.9033008Z (unchanged
  since creation moment). Move 3 unpaid: confirmed.
- commit-queue rows: grep -cin over watch/inbox/hermes_burn/TICKET_LEDGER.md,
  queue/todo.md, memory/law/registry.json = 0/0/0. Move 7 unpaid: confirmed.
- logs/kpi.jsonl now 753,223,654 bytes (Get-Item this sitting), PAST the
  lens's 752,846,276 and the 748,222,017 baseline: growth continued, no
  rotation; the writer at mag/records.py:138 (write_kpi) shows no rotation
  logic in the span read. Move 5 unpaid and worse than reported: confirmed
  and strengthened.
- INDEX.json: grep -c census_refresh_20261002 = 0, grep -c NIGHT_CLOSE = 0
  (fillball = 11). Both adjudicating receipts unregistered: confirmed. The
  census receipt exists (watch/inbox/census_refresh_20261002.md, 2,730
  bytes, Oct 2 06:10 local) and IS the proof for paid move 4, so the rank-8
  index-last disease recurred on the very receipt that answered the patrol.
- Move texts verified at watch/inbox/ractor_engine/ractor-topic/
  SYNTHESIS.md "## Ranked moves" (line 138), items 3, 5, 7 as quoted.

### F5 instrument dogfood evidence (finding text truncated in transmission): CONFIRMED on visible bytes

- ls verifies all six test files: tests/test_code_swarm.py,
  test_rib_swarm.py, test_water_swarm.py, test_seed_seal.py,
  test_citation_lint.py, test_percolator_candidates.py.
- memory/percolator/candidates.jsonl = 16 rows (wc -l), LastWriteTimeUtc
  2026-10-02T04:17:43.3050340Z; row 1 read this sitting carries status
  "candidate", promoted false, real arXiv source URLs, and a concrete claim
  against mag/knowledge_graph.py:165. The percolator intake actually FIRED
  after landing: dogfooded, not merely built. The finding sentence,
  falsifier, and move were cut off in my input; nothing further asserted.

## What the lens missed (additions)

1. THE PIDFILE GUARD WAS NEVER SWEPT. grep -Li pidfile scripts/*.sh returns
   14 of 15 shell scripts with no pidfile mention (astra_convo_loop.sh,
   start_autorun.sh, teach_recorder.sh, v3_deepseek_run.sh, both mesh_comm
   runners, all six pull_* cloners, survival_extract.sh, hofw_001_seed.sh,
   vast_ollam_bootstrap.sh); the guard lives only at scripts/
   descent_driver.sh:10-22. The ask's question 2, directly answerable in one
   grep, absent from the lens report. Falsifier: a second guard-bearing
   long-runner in that list. Move: ~60 min to port the guard block to the
   loop-shaped runners (astra_convo_loop, start_autorun, teach_recorder,
   mesh_comm pair) or register the one-guard decision as law.
2. THE 10-01 RUN LOST 2 OF 8 LENSES SILENTLY. The bank holds no
   communication.md or logic.md for 2026-10-01-dogfood-gaps and no break
   files for them; SYNTHESIS.md never mentions the loss (grep
   communication|logic lens = 0 hits); the commit still says "8 lenses rode".
   This 48h run banked all 8 (communication.md and logic.md on disk in
   2026-10-02-dogfood-48h/), proving capacity: the 10-01 loss was a silent
   partial failure, an engine defect class distinct from F2's file-count
   discrepancy. Falsifier: a receipt in the 10-01 run naming the two lenses
   as skipped-or-failed. Move: ~20 min, engine turn gate that fails the run
   if any riders library id lacks a banked file.
3. MOVE 6 IS ALSO UNPAID. grep -in "audit|jsonl|append"
   scripts/invisible_runner.vbs = zero hits: the audit-jsonl instrument that
   would attribute the unattributed 23:32 EDT launch does not exist. The
   unpaid set is moves 3, 5, 6, 7, not 3/5/7. Falsifier: an audit append in
   the vbs bytes. Move: fold into the move-3 erratum sitting (~15 min).
4. THE CLOSURE RECEIPTS MIS-MAP THE REGISTER'S OWN NUMBERING.
   watch/inbox/fillball/seed-seal.md:91 says "Closes: SS-1 (GAP_REGISTER
   rank 5)" but SS-1 is named in rank 11 (GAP_REGISTER.md:84); rank 5 is the
   steer-seal arming row, whose operator enforce flip is still unflipped
   (no steer_seal_mode sentinel visible in ~/.mag; listing returned empty
   this sitting). A seat auditing closures from receipts would mark rank 5
   closed when its operator half is open. The no-adjudicator disease is
   worse than F1 stated: even the closure evidence disagrees with the row
   ids. Falsifier: a ~/.mag/steer_seal_mode file. Move: ~10 min, add
   "cites register rank by quoting the row text, not the number" to the
   fillball receipt convention.
5. THE ENGINE TOPIC FIX HOLDS IN BYTES AND IN THIS RUN. .zcode/workflows/
   ractor-engine.dwf.ts:30-32 declares topic required: true in the metadata
   args block (the 2026-10-02 fix the ask named), and this 48h run's lens
   files carry the real topic in their headers (2026-10-02-dogfood-48h/
   accuracy.md:1 names the window). Harness enforcement of required:true
   remains untested (would need a deliberate topic-less fire): OWED, same
   stance the lens took in its blind spots.

## Not run this sitting

WMI or any process census; the full pytest suite; any paid dispatch; USN
journal queries; harness enforcement probe of the engine's required:true
(same refusal the lens recorded). The two historical kpi.jsonl sizes
(748,222,017 and 752,846,276) are the lens's measurements plus the ask's own
748MB figure; I verified only the current 753,223,654 bytes and the absence
of rotation logic.

Filed by the break-logic pass. Written to watch/inbox/ractor_engine/
2026-10-02-dogfood-48h/break-logic.md. No em-dash bytes.
