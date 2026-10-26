# break-accuracy: hostile second pass on the accuracy lens report (GAP_REGISTER dogfood)

Session 2026-10-01, seat break-accuracy, engine run dogfood-gaps. Every check below was
run in this session against estate bytes unless marked not-run or adopted. No em-dashes.
Instrument note: this shell is git-bash with a semicolon PATH, so every check ran through
absolute-path PowerShell (C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe),
git.exe at C:\Program Files\Git\cmd\git.exe, and rg. Commands are quoted verbatim per check.

## Verdicts

### Finding 1 (10 of 12 ranked rows byte-verify still live; no status column; rank 1 fixed-in-waiting): CONFIRMED

Every per-row cite reproduced. Checks run this session (command: PowerShell
Test-Path / Get-Item / Get-ChildItem / Select-String -SimpleMatch; outputs):

- queue/lanes/elder/inbox.jsonl: Get-Item -> Length 0, LastWriteTime 9/4/2026 10:43:28 AM. Matches the lens byte-for-byte.
- tools/citation_lint.py: Test-Path False. githooks/pre-push Select-String "citation_lint" count = 0.
- watch/inbox/48h_synth/STORY.md: Select-String "191.8M" -> "line 240: cards with falsifiable probes, 191.8M tokens spent, and the two percolator code reads verified".
- watch/inbox/frontier_olm_20260928/DIGEST.md: Select-String "191" count = 0.
- watch/inbox/48h_synth/ERRATA.md: Test-Path False (dir holds lattice.md, laws.md, measure.md, next.md, steals.md, STORY.md, .mimosa only).
- C:\Users\foste\.mag: Get-ChildItem -Force -> single entry "steer_seal_seen".
- mag/seed_seal.py: Test-Path False. tests/test_seal_forge_drill.py: Test-Path False. seed/verify_seal.py: Test-Path True (the register fill 5 target at GAP_REGISTER.md:106 is valid). mag/steer_seal.py: Test-Path True. pam.md found at watch/inbox/localfirst/pam.md (rg --files -g pam.md).
- mag/percolator.py: Select-String "candidates" count = 0; add_argument lines are 558-567 (text, --source, --domain, --noise-log, --intake, --status, --maintenance, --dry, --apply), no --candidates flag.
- watch/inbox/frontier_olm_2026-09-30: 93 files on disk; recursive filter DIGEST|register|percolator|RECEIPT returns zero files. Rank 7's "fold step missing" holds.
- memory/runs/corpus_gap_research/ARXIV_REGISTER.json: Length 233406, LastWriteTime 9/29/2026 5:59:04 AM; Select-String "2606.03458" count = 0.
- quantization-compression.md: recursive Get-ChildItem over watch/inbox + corpus + memory returns exactly 3 copies (frontier_olm_2026-09-30, 2026-10-01, 20260928, each under steal\); none in corpus/steal; per-copy counts 1sy7srk=0 and 2609.21341=0 in all three.
- watch/inbox/hermes_burn/TICKET_LEDGER.md: SS-1=0 CP-1=0 R2-1=0. rg "estate_corpus_search" over mag+tools returns no files (rank 11 re-confirmed).
- watch/inbox/spiking_wide: 8 files, none a Vulkan receipt; rg -il "vulkan" hits only nonnvidia-stacks.md and nonnvidia_stacks_signals.jsonl (plan-side mentions, no landed receipt). Rank 12 live.
- scripts/estate_walk_daily.ps1: lines 5-13 carry the PATH LAW comment and absolute $repo/$log/$alarm (lines 11-13). logs/estate_walk_daily.log tail ends "END 2026-10-02T00:37:54Z exit=0" (10-01 20:37:54 EDT smoke, 9 min before the commit). schtasks /Query /TN EstateWalkDaily /V: Next Run Time 10/2/2026 9:15:00 AM, Status Ready, Last Run 10/1/2026 9:15:01 AM, Last Result 1. memory/attention.md Select-String "ESTATE-WALK" count = 0 (the alarm channel has still never fired; the residual the lens named is real).
- No status column: the register table header at GAP_REGISTER.md:72 is "rank | gap | lane | sev | fill cost | owner" and no status column exists anywhere in the file (read in full, 247 lines).

Blind spot 6 stays honestly open: the 10-02 09:15 fire is a future event, not run, and
cannot be verified at this sitting. Everything checkable today (schtasks state above) is
consistent with fixed-in-waiting.

### Finding 2 (coverage claim stale at its own landing; amendment clause never exercised): CONFIRMED, with two corrections

Reproduced byte-exact:

- Lane mtimes (Get-ChildItem recursive on memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes): a08-48h-synth.json 18:13:46, a15-rollup.json 18:39:32, a14-coverage.json 18:48:13, a09-balls.json 18:49:19, all 2026-10-01 -0400. All four match the lens exactly.
- git show -s 5d2263f10 -> "2026-10-01T20:46:30-04:00", subject carries "15/15 lanes, 75 rows" verbatim. git show --stat 5d2263f10 shows watch/inbox/gap_analysis_20261001/GAP_REGISTER.md | 247 + (new file) and scripts/estate_walk_daily.ps1 | 19 +- riding the same commit.
- watch/inbox/gap_analysis_20261001/ holds GAP_REGISTER.md only (mtime 6:41:58 PM, 16660 bytes), so the amendment clause at GAP_REGISTER.md:13-15 was never exercised: no amendment file exists.
- Sharpening the lens: the register file's last write (18:41:58) PRECEDES all six a09-a14 landings (a11 18:45:43, a14 18:48:13, a09 18:49:19, a10 18:53:47, a12 18:54:58, a13 19:30:04). So the register text was true at write time and went stale in the 2h04m window before the commit shipped it. "Sat on disk for about two hours" is exact for a11/a14/a09 and generous for a13 (1h16m).

Correction 1, the 33-row count is wrong. Per-lane "rows" array counts (ConvertFrom-Json
schema dump, hand count for a01): a01=5, a02=10, a03=5, a04=5, a05=5, a06=5, a07=5,
a08=5, a09=5, a10=5, a11=0 (a11 has no rows key; it carries queue_audit=12 and
evidence_rows=5), a12=5, a13=5, a14=5, a15=5. So a09-a14 hold 25 rows under the register's
own rows schema, or 42 row-shaped items counting a11's two arrays. No schema produces the
lens's 5+5+8+5+5+5=33 (nothing in a11 counts 8).

Correction 2, the 75-vs-78 denominator is now adjudicated and the commit wins: rows
arrays across all 15 lanes sum to exactly 75 (5+10+13x5... computed: a01 5 + a02 10 +
a03..a08 30 + a09,a10,a12,a13,a14,a15 30 = 75). The commit headline "75 rows" is exact
under the rows-key schema; the register's "merges 8 siblings" (GAP_REGISTER.md:12) counts
the lanes read, whose rows sum to 45. No 78 exists anywhere I searched.

### Finding 3 (register instantiates its own meta-gap 3 twice: phantom OWED-ledger path + primary-confirmed never relabelled): CONFIRMED, with one correction

Reproduced:

- The three quantization-compression.md copies and their zero trio hits (see finding 1 checks). corpus/steal has no copy, so fill 10's cited "steal/quantization-compression.md" ledger path is phantom as the lens said.
- GAP_REGISTER.md:241-244 reads "The theneurondaily 0.55-confidence number is now primary-confirmed" while fill 9 at GAP_REGISTER.md:124-129 still instructs "append the receipt beside sweep/inference-efficiency-x.md and relabel 0.55 to primary-confirmed". The register claims the same item DONE and OWED in two sections; the lens undercharged this: it is an internal self-contradiction, not just a stale label.
- sweep/inference-efficiency-x.md line 52 reads "Banked degraded per recipe: the thread resolved but the article content truncated ... Confidence 0.55." (Get-Content index 51). DIGEST.md:120 likewise says the numbers "currently ride a search snippet at confidence 0.55" with the fetch as queued action 2, so the fold's own record sides with the sweep, not with the register's primary-confirmed bullet.
- rg "theneurondaily" over watch/inbox/frontier_olm_2026-10-01 returns exactly 2 files: DIGEST.md and sweep/inference-efficiency-x.md. sweep/_fx exists (Test-Path True) and holds no theneurondaily file. No receipt file anywhere.

Correction: the lens's "the 203,655-byte evidence held only inside a15-rollup.json" is
literally impossible. a15-rollup.json is 8,259 bytes (regex counts inside it: fxtwitter=3,
"380 tokens/second"=1, theneurondaily=6, "203,655"=2), and it is the only copy repo-wide
(Get-ChildItem -Recurse -Filter a15-rollup.json -Depth 6 returns one file). The raw
203,655 bytes exist nowhere on disk; what a15-rollup.json holds is the prose CLAIM of the
fetch. The register's primary-confirmed assertion therefore rests on an unverifiable
in-lane claim, which is worse than the lens stated, and the lens's blind spot 4 framing
("they exist only as text inside a15-rollup.json") repeats the same error.

### Finding 4 (MINED-NEVER-SCHEDULED dominant; exactly 2 of 12 rows moved, both as side effects): WEAKENED

Confirmed parts: the class name and prescription are in the register (GAP_REGISTER.md:44
names MINED-NEVER-SCHEDULED; 48-49 carry the schedule-and-fire prescription; the lens's
cite of 48-49 for the name drifts by 4 lines). The zero-ticketing mechanism reproduces:
TICKET_LEDGER.md SS-1/CP-1/R2-1 = 0/0/0, estate_corpus_search absent from mag+tools. The
rank 1 fix rode 5d2263f10 (git --stat: scripts/estate_walk_daily.ps1 | 19 +-), and
2093ca518 reads "2026-10-01T16:44:35-04:00" with "healed the INDEX as a side effect ...
(shared surface rebuild: window rows 0 to 37, stale hashes healed, card registered)"
byte-verified in the message.

Killed part: rank 8 did NOT move. INDEX.json (mtime 10/1/2026 6:00:56 PM, post-heal)
contains exactly 38 lines matching frontier_olm_2026-10-01 (matching the "rows 0 to 37"
heal), and those 38 rows are 6 lens + 29 sweep + 3-4 steal lane files; the line filter
returns 0 rows for DIGEST, register.jsonl, percolator_candidates, RECEIPT, and
arxiv_deepread, and the day-2 steal card quantization-compression.md has no row either.
Every output rank 8 names is still unindexed. So the truth is: exactly 1 of 12 rows moved
(rank 1), rank 8 partially moved (lane files indexed, named headline-output debt intact),
and finding 1's arithmetic inherits this: 11 of 12 rows are still live, not 10 of 12 plus
an unmentioned rank 8.

Also wrong in emphasis: rank 1's fix was the HEADLINE of 5d2263f10 ("the audit caught a
live bug now FIXED"), not a side effect of another commit; and rank 8's heal (16:44)
predates the register's own landing (file write 18:41:58, commit 20:46), so "in the
register's first day" is loose for the one row that did move.

## Blind-spot adjudication (lens's six)

1. a09-a14 content unread: CLOSED by this pass. All six lanes read in full. They hold at
   least five S1-class rows under the register's own rubric (GAP_REGISTER.md:29-31): a09
   row 1 (commit 2093ca518's headline overclaim; I independently ran Select-String
   "judge" on tools/abliterate_p1_probe.py = 0), a10 row 2 and a14 row 2 (key rotation
   OPEN, leaked keys, falsifier-clocked), a11 queue rank 1 (recovery pack, git tag empty
   per lane) and rank 3 (M1 bench under F2 deadline 2026-10-02T23:59Z), a13 row 1
   (invisible_runner.vbs never launches children; corroborated: script mtime 9/30/2026
   10:59:12 AM, and logs/fts_index.log, logs/census_patrol.log, logs/improve_daily.log all
   end on 09-30, the last pre-wrapper fires; queue/todo.md:204-205 Studio checkboxes still
   open per a10 row 4, read directly). The rerank threat the lens owed is real.
2. Only 2 of 5 register quotes spot-checked: CLOSED, and the register WINS. Case-sensitive
   -SimpleMatch over the whole run dir: all five quotes return exactly 1 hit in their named
   lane files (q1 in a06-spiking.json, q2+q3 in a08-48h-synth.json, q4 in
   a07-localfirst.json, q5 in a05-ractor50.json). Instrumentation confession: my first
   quote pass printed four zeros; that pass was invalid (an unresolved $f path in that
   PowerShell invocation) and is retracted; the schema-pass rerun above is the valid one.
3. 75-vs-78 denominator: CLOSED, commit's 75 is exact under the rows-key schema (see
   finding 2, correction 2). a01-olm-day2.json fails PowerShell 5.1 ConvertFrom-Json at
   char 14085 ("Invalid object passed in, ':' or '}' expected"), confirming the lens's "a01
   unparseable"; its 5 rows were hand-counted from the file text.
4. 203,655 bytes unverified: CLOSED with a correction. The bytes exist nowhere on disk;
   only prose claims do (see finding 3 correction). The lens's verification debt was
   undrawable, not merely undone.
5. Rank 2 card-side clock terms: CLOSED. a05-ractor50.json carries the card's clause and a
   dedicated field: quote "bank one lens from 48h-synthesis/STORY.md into the elder inbox
   before ~10-02 and the card resurrects by its own terms", field elder_lens_salvage_clock
   "inbox.jsonl 0 bytes mtime Sep 4; window closes ~10-02; NOT banked". See addition A5
   for why the fill is more broken than the clock suggests.
6. 10-02 09:15 fire: remains OWED (future event). schtasks state recorded above; nothing
   else is checkable today.

## Additions (what the lens missed)

- A1: The unmerged a09-a14 lanes hold at least five S1-class rows that would rerank the
  top 12 (evidence in blind spot 1). Falsifier: merging a09-a14 and finding no row meeting
  GAP_REGISTER.md:29-31 S1 criteria. Move: 30 min, exercise GAP_REGISTER.md:13-15's own
  amend clause with per-row grep receipts.
- A2: Rank 8 is byte-still-live for its named outputs; the lens's moved verdict is wrong
  (INDEX.json 38 day-2 rows, zero matches for DIGEST/register.jsonl/percolator_candidates/
  RECEIPT/arxiv_deepread). Falsifier: an INDEX rebuild adding those six paths. Move:
  20 min, rerun the sanctioned writer after the fold's last write per fill 8.
- A3: Register rank 10's "zero mentions anywhere" (GAP_REGISTER.md:83) is byte-false as an
  absolute: rg -l "2609\.21341" hits 8+ files including the day-2 window's own
  sweep/open-local-language-models-reddit.md and the 20260928 DIGEST/RECEIPT; rg -l
  "1sy7srk" hits the 20260928 DIGEST and two kv-cache-context-engineering-reddit.md
  sweeps. The scoped truth (day-2 DIGEST/register/percolator only, per a01's grep) stands.
  Falsifier: re-scoping the register wording makes it true again. Move: 10 min reword.
- A4: The same commit that landed the register grew the estate index binaries into git:
  git show --stat 5d2263f10 shows dashboard/data/ESTATE_INDEX.jsonl Bin
  1945896570 -> 2523006985 and watch/ESTATE_INDEX/ESTATE_INDEX.jsonl Bin 92 ->
  2523006985 (a 2.5GB binary landing). No gap row tracks it. Falsifier: a receipt or row
  naming the index growth. Move: 10 min, add an S4 row for repo weight.
- A5: The elder salvage consumer is dead: queue/lanes/elder/surface.md records cage
  lane-down "HTTP Error 429" every single day 09-17 through 10-01 (15 consecutive rows,
  latest 2026-10-01T12:00:23Z), and the 09-18 entry on the same surface documents
  success-shaped false logging in mag/lane_runner.py::cycle_elder (trail writes "lens on 1
  cards" on 429 days). Filling inbox.jsonl before the ~10-02 clock feeds a lane whose
  runner 429s daily. Falsifier: a post-10-01 surface.md cage row firing a real LENS. Move:
  10 min, annotate rank 2 that the fill must also wake or bypass the cage runner.
- A6: The register's token denominator premise is ~8.3x under its own ledger:
  CYCLE_BRIEF_20260930.md:33 reads "714,810,462 recorded on 300 fires + 49 unrecorded x
  mean 2,382,701 ~= 831,562,811 total (cache-inclusive, fire-time attributed)" (verified
  byte-level this session; also carried in a14-coverage.json negatives). Falsifier: a
  burst-scoped count near 100M. Move: 5 min, add the denominator note to the register.

## Not run / OWED

- The 10-02 09:15 EstateWalkDaily fire (future event).
- A full pytest or census run (not asked, not run).
- Python json.load on a01-olm-day2.json (my parse evidence is PowerShell 5.1
  ConvertFrom-Json; a strict python parse might differ, untested).
- Content-level Vulkan probe verification on the RX 5600 XT box (rank 12's fill itself).

CREATE_NO_WINDOW note: no subprocess-spawning script was authored this session; the law
had no surface to apply to.
