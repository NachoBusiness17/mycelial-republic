# B2-33: pre-burn rejection recount (2026-09-26)

## Verdict

Denominator FROZEN at 41. The recount from the snapshot committed alongside the
taxonomy confirms the headline byte-exact: 41 rejection rows, 39 infrastructure
/ 2 merit, infra share 39/41 = 95.1%. The table's 42 was never a population:
one wrong cell (empty_content written 12, true 9) plus the IncompleteRead row
appended to a 4-class sum that had absorbed that +3. F3's correction
branch (recount != 41) does not fire; the unrecoverable-rows branch (widen pass
to < 60%) does not fire. The < 70% pass threshold in
BURN_JUDGE_LANE_BUILD_20260925.md stands against the frozen 41. failure_class
added to LEDGER rows going forward (append-only); this row is the first
carrier.

## Evidence

- REJECTION_TAXONOMY_20260917.md:5 "41 rejection rows total"; :6 "Only **2 are
  merit rejections**"; :7 "The other **39 are infrastructure failures**";
  :15 table cell "empty_content | 12".
- git 3d12289f9 (2026-09-17T23:56:48-04:00; mtime 23:54:09 -0400) carries
  union_fullsend_20260917/build_lane/proposals.jsonl: 71 rows, 41 verdict
  FAIL. Class tally from those committed bytes: 200-error-body 16 (12
  "KeyError: 'choices'" + 4 explicit "200_error_body"), 404 11, empty_content
  9, schema 2, IncompleteRead 1, merit 2. Sum 41 exact.
- empty_content=12 is unreachable under any cutoff: the live file (111 rows,
  0 malformed) holds 9 forever (8 on 09-17 + 1 at 2026-09-18T03:28:58Z;
  09-26 rows all HTTP 404).
- The commit message census (16+11+12+2 = 41) dropped the IncompleteRead row
  while carrying the +3; the table then appended the IR row, summing 42.
  Headline 41 survived two cancelling errors.
- GOOGLE_CODIRECTOR_STEAL_20260925.md:14 "39/41 failures were infrastructure,
  2 merit"; :28 "(39/41 pattern)"; BURN_JUDGE_LANE_BUILD_20260925.md:49
  "41 rows, 39 infra / 2 merit (95.1% infra)" - all confirmed, no correction
  owed.
- memory/burns/LEDGER.jsonl: 80 rows at append (79 prior; 4 landed
  concurrently from other lanes); failure_class in 0 of the 79 prior rows;
  line 80 (this lane) is the sole carrier.
- Root raw.jsonl ruled out as a competing census: or-union-alpha research-lane
  rows.

## Work done

- Read both pointers in full; taxonomy (37 lines) read in full.
- Parsed all 111 proposals.jsonl rows with the repo venv; classified by day,
  ok, verdict, error class.
- Located the write-time snapshot via file mtime + git; recounted FAIL rows
  from committed bytes, independent of the live file.
- Verified append-only: committed 71 rows are a prefix of today's 111
  (09-17 = 56 both sides; 09-18 = 15 committed, 43 live).
- Appended a dated ERRATUM to the taxonomy (append-only, no line rewritten;
  its 4 em-dashes are pre-existing in the 09-17 commit, erratum adds 0).
- Appended the LEDGER row with failure_class as a class:count object via venv
  python json.dumps.
- Self-fed B2-117 and B2-118 to QUEUE.md under Open (108-116 taken by
  concurrent lanes).

## Falsifier

F3 pre-registered: (a) recount != 41 means correcting the 95.1% figure in
GOOGLE_CODIRECTOR_STEAL_20260925.md and BURN_JUDGE_LANE_BUILD_20260925.md
before the 50-wide gate; (b) unrecoverable rows means filing the baseline
approximate and widening pass to < 60%. Neither branch fires: the recount is
41 exact from committed bytes and the rows are fully recoverable. 41-vs-42
resolves as a single-cell census defect; 42 was never a population.
Reproduction: git show
3d12289f9:watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl,
then tally verdict FAIL by error class; any tally other than {16, 11, 9, 2, 1,
merit 2} = 41 inverts this receipt.

## Bibliography

- watch/inbox/REJECTION_TAXONOMY_20260917.md (read in full, erratum appended)
- watch/inbox/BURN_judge-lane-spec_20260925_d.md (read in full, falsifier F3)
- watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl (111 rows parsed)
- git 3d12289f9 committed snapshot of proposals.jsonl (71 rows recounted)
- watch/inbox/union_fullsend_20260917/build_lane/state.json (read; rejected: 2)
- union_fullsend_20260917/raw.jsonl (head + grep, ruled out)
- watch/inbox/GOOGLE_CODIRECTOR_STEAL_20260925.md (:14, :28 verified)
- watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md (:37, :49 verified)
- memory/burns/LEDGER.jsonl (79 prior rows; row 80 appended)
- watch/inbox/burn_wave_20260926/QUEUE.md (read in full; B2-117, B2-118 fed)
