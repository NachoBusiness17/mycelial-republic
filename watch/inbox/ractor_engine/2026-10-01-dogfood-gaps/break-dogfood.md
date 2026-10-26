# BREAK-DOGFOOD: hostile second pass on the dogfood lens (2026-10-01/02)

Break pass on `watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/dogfood.md`,
topic `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`. Every byte-check
below was re-run by this seat this session. Poll moments: first sweep
2026-10-01 23:13:05 EDT (`date`), final sweep 2026-10-02 00:09:21 EDT. That
window matters: the estate started filling the register DURING the pass (see
A5). Nothing here was taken from the lens's word; anything I could not settle
is marked OWED.

## Instrument note (census-denominator law, B2-216)

Two of my own snapshots disagree and both are honest: `grep -c candidates
mag/percolator.py` = 0 at ~23:05 EDT, = 19 at ~00:06 EDT (file mtime
2026-10-02 00:05:48 EDT). A check is a moment, not a fact. Timestamps are on
every claim below.

## Verdicts

### headline ("1 of 12 filled ~18h after landing; 11 rows byte-reconfirm; register exemplifies MINED-NEVER-SCHEDULED") - WEAKENED

Confirmed at the lens's moment and at my first sweep; dying at my final sweep:

- 1/12 held at 23:13: every rank 2-12 check re-ran clean (details per finding).
- "~18h after landing" (dogfood.md:11) is unreproducible from any byte: the
  register was written 18:41:58 EDT (mtime) and committed in 5d2263f10 at
  2026-10-01T20:46:30-04:00 (`git log --format='%h %cI'`); at my 23:13:05 poll
  that is 4h31m / 2h27m of elapsed time. 18h requires a ~05:13 EDT landing; no
  byte shows one. Direction survives (hours, zero fills), the number does not.
- Row 10 does NOT reconfirm (see A2): the register's "zero mentions anywhere"
  is byte-false and the lens's single-file grep missed the holdings.
- At 00:09:21 the score is no longer 1/12: a fill wave is landing ranks 2, 4,
  5, 6, 7 in real time (A5). The "register exemplifies MINED-NEVER-SCHEDULED"
  frame inverted: the register demonstrably drove execution within ~3h of
  commit, by name, with code comments citing its row numbers.

### F1 (amendment clause live and unexercised) - CONFIRMED

- Clause byte-verified at GAP_REGISTER.md:14-15; register still reads "merges
  8 siblings" (line 14) with no amendment section (file read in full, 248
  lines, mtime 18:41:58 unchanged through 00:09).
- Lane bytes: a09-a14 main files landed 18:45:43 EDT (a11) through 19:30:04
  EDT (a13), all AFTER the register write; NOT the lens's "18:46 to 18:53"
  (a11 predates it, a13 is 37 min past it; `ls --time-style=full-iso`).
- The falsifier ("lanes contain nothing rank-relevant") fails by direct read:
  a10-drops.json master_list = 27 items (10 DONE / 9 OWED / 4 SCHEDULED /
  2 PARTIAL / 2 DEAD); a11-build-queue.json queue_audit = 12 builds with
  one-sitting minute costs and blockers; a14-coverage.json surface_ledger =
  10 untouched surfaces. Also a12-commits.json scope = "64 commits since
  09-30 00:00", matching the lens's description.
- Sharpened: FOLD_SECTIONS.md (19:37:26) counts 15 lanes fired / 14 landed and
  commit 5d2263f10 (20:46:30) says "15/15 lanes", so the estate knew the lanes
  landed while register line 239 still asserts "no late landings appeared" -
  true at write (18:41:58), false at commit. The fill wave now firing is not
  an amendment: the register text itself is still unamended.

### F2 (fill 9's fetch is unwired; register self-cites a phantom) - CONFIRMED, framing softened

- Still true at 00:09: sweep label unchanged,
  `watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-x.md:52`
  reads "Confidence 0.55"; no receipt file in sweep/ (glob) nor in sweep/_fx/
  (18 raw fxtwitter JSONs, 10:37-11:05 EDT, none theneurondaily, zero
  'RunAnywhere' hits); '203,655'/'203655' zero in the day-2 window; day-2
  RECEIPT.md and DIGEST.md grep clean for theneurondaily/203,655/status id.
- Blind spot 2 RESOLVED against the harsher reading: the fetch happened
  in-session. a15-rollup.json:68: "cross-checked against raw bytes via
  curl -sL (203,655 bytes to $TEMP/tnl_tweet.json)". The raw bytes went to a
  session temp dir and were never landed, so this is WIRING failure, not
  in-lane fabrication. Full estate homes of the sentence
  ('RunAnywhere says hosted GLM-5.3 Flash reaches 380'): GAP_REGISTER.md only,
  on the tracked tree (rg); a15-rollup.json and memory/trajectory/steps.jsonl
  on the ignored tree (grep).
- Sharpened: the register contradicts itself. Line 241: "The theneurondaily
  0.55-confidence number is now primary-confirmed", while lines 127-129 still
  list "append the receipt ... and relabel 0.55 to primary-confirmed" as fill
  9's remaining action, and the disk label is unchanged. The estate's own
  LIVENESS-IS-NOT-TRUTH doctrine (962e41054) forbids the relabel until fetched
  text is landed.
- OWED: .zcode transcript greps for '203,655' timed out twice (rc=124);
  in-session occurrence beyond the lane's self-receipt is unproven either way.
  The '203655' hits in catalog/catalog.jsonl are an id fragment
  (f7d092036559), not the fetch.

### F3 (misranked by its own law; clock row not first) - CONFIRMED

- Ranks 9-10 are S3 one-sitting, ranks 11-12 are S2 one-sitting
  (GAP_REGISTER.md:82-85) against "cheapest-cure-first inside a severity
  band" (GAP_REGISTER.md:25-26). No documented fill-ease-dominant reading
  exists anywhere in the file (read in full).
- Rank 1 closed, rank 2 the only open clock: my schtasks query -
  TaskName \EstateWalkDaily, Last Run Time 10/1/2026 9:15:01 AM, Last Result
  1, Next Run Time 10/2/2026 9:15:00 AM, Status Ready, Task To Run points at
  the fixed scripts/estate_walk_daily.ps1. Script PATH LAW verified at
  scripts/estate_walk_daily.ps1:5-13; log END 2026-10-02T00:37:54Z exit=0
  (read via python, file is UTF-16).
- Note: the fill wave is executing rank 2's fill right now
  (watch/inbox/fillball/elder-salvage.md, 00:08:55) but the table itself
  remains unsorted; the doc defect stands.

### F4 (meta-gap dominance; GATES-UNARMED slowest class) - CONFIRMED then overtaken

- 11/12 unfilled at the lens's moment: citation_lint absent, seed_seal absent,
  drill absent, ~/.mag = only steer_seal_seen/ (mtime Oct 1 14:29), percolator
  zero candidates, day-1 window unfolded, INDEX.json carries 0 of the 4 day-2
  headline paths (38 refs to the window, all lens/steal/sweep), KVarN = 0 in
  ARXIV_REGISTER.json (mtime Sep 29 05:59), TICKET_LEDGER.md (10,140 bytes,
  Oct 1 17:35:33) zero SS-1/CP-1/R2-1, spiking_wide/ = 8 files zero vulkan.
- "Zero estate motion of any kind since the audit" is now FALSE at 00:08:
  mag/seed_seal.py landed (14,423 bytes, 00:08:24), state/keys/seed_seal_key
  exists, the percolator --candidates flag landed (00:05:48, lines 23/67/484/
  719 citing "GAP_REGISTER rank 6"). ~/.mag still unarmed, drill test absent,
  zero .seal sidecars, invariants.json unchanged (229,209 bytes, 19:17:50,
  zero candidates rows): the class is moving, the teeth are not in yet.
- The "~18h" arithmetic wound from the headline applies here too.

### F5 (librarian diseases + ractor engine postdate the register; owner column) - CONFIRMED

- Commit times: 5d2263f10 20:46:30 EDT < 962e41054 20:54:07 EDT <
  f4cfcdf9b 21:57:07 EDT (`git log --format='%h %cI'`). Both landings
  postdate the register commit, exactly as claimed.
- Owner column: "any seat"-variants on exactly 10 of 12 rows (ranks
  1,2,3,4,6,7,8,9,10,11); register read in full shows no librarian D1/D2/D3
  rows. The proposed amendment row is still owed and the firing fill wave did
  not amend the register either.

## Additions (what the lens missed)

### A1. The register's poll stamp is a timezone mislabel, provable

GAP_REGISTER.md:12 says "lanes dir poll 2026-10-01 ~18:30Z", but line 10
claims all 8 siblings "read in full this session" and the last-written
sibling a06-spiking.json has mtime 18:28:44 EDT. A 14:30 EDT (18:30Z) poll
could not have read it. The poll was ~18:30 EDT; the Z is wrong. Line 243's
"at 18:37Z" carries the same pattern (fits a15's 18:30-18:46 EDT session;
unproven to the same standard, flagged as likely). A citation-precision
defect inside the document whose meta-gap 3 is citation precision; resolves
the lens's blind spot 5. Falsifier: an a15 session log showing the poll in
UTC. Move: one-line ERRATA-style stamp fix in the register, 5 min.

### A2. Rank 10 is the register's worst row: "zero mentions anywhere" is triply false and the fill re-fetches held bytes

- U2 (1sy7srk): the full measured KV table is ALREADY BANKED at
  watch/inbox/frontier_olm_20260928/sweep/kv-cache-context-engineering-reddit.md:44
  ("f16 89.4 / q8_0 87.4 / turbo3 79.5" at depth 0, through "1M (only turbo3
  6.5 survives)", with the context-budget reading). The id also rides
  frontier_olm_20260928/DIGEST.md, the 09-30 window's
  sweep/kv-cache-context-engineering-reddit.md, catalog/catalog.jsonl,
  catalog/tags.jsonl, watch/ESTATE_INDEX/ESTATE_INDEX.jsonl, and the a01 lane
  files that authored the row (memory/runs/.../a01-olm-day2.json).
  catalog.jsonl also carries a dead holding: path
  "local_sovereign_agent/%TEMP%/ppc_1sy7srk.json", 32,148 bytes,
  2026-09-29T18:58:11Z - the file is GONE from %TEMP% (ls: No such file), a
  catalog liveness lie under LIVENESS-IS-NOT-TRUTH.
- U3 (2609.21341): the day-2 sweep adjudicates it in full at
  watch/inbox/frontier_olm_2026-10-01/sweep/open-local-language-models-reddit.md:27
  ("2609.21341 SLM database agent - HELD in 09-28 sweep raw
  (sweep/_raw/full_2609.21341.txt)"), and the full text sits on disk
  (frontier_olm_20260928/sweep/_raw/full_2609.21341.txt + .html + abs page).
- Consequence: fill 10's cost spec ("2 archive fetches") is wrong for both
  halves; the true fill is two cite/fold edits into
  steal/quantization-compression.md (the OWED ledger) plus a dead-pointer
  cleanup. The lens's row-10 "STILL REAL" rode a grep of one file and
  certified a row whose claim text and cost are both byte-false. Falsifier:
  the KV numbers shown above are not in the 09-28 sweep (they are; line 44).
  Move: rewrite rank 10 as a fold edit and delete the %TEMP% catalog row, 20
  min.

### A3. The fold's scoreboard is key-shape-blind exactly on the costed-queue lane, and 70 vs 75 rows is unreconciled

FOLD_SECTIONS.md:9 scores "landed-empty (0 rows): 1 - a11-build-queue" while
a11-build-queue.json carries queue_audit len 12 + evidence_rows len 5 (it has
no 'rows' key; verified by venv python json read). The lane holding the
unpaid build queue with one-sitting costs scored zero in the fold. Also 70
rows (FOLD_SECTIONS.md:16, 19:37:26) vs "75 rows" (5d2263f10, 20:46:30) is a
two-instrument count delta nobody named: B2-216 inside this very burst.
Falsifier: a fold rerun counting a11's queues. Move: re-run the fold script
with a rows-or-queues key union and reconcile 70/75, 15 min.

### A4. a14 carries an S1-class row the table never picked up

a14-coverage.json surface_ledger: "operator-gated security (Q10 key rotation,
Q07 PAT) ... correct mechanism, urgent content: 7 live keys, exploit window
open". Under the register's own S1 law (GAP_REGISTER.md:29-30, "breaks a live
trust/safety gate"), seven live keys with an open exploit window outranks
several S2 rows in the table and appears in none of the 12. The F1 amendment
is therefore not bookkeeping: merging a09-a14 imports a missed S1. Falsifier:
the row is adjudicated elsewhere in the register (it is not; full read).
Move: add the row at S1 in the amendment, owner operator, 5 min.

### A5. LIVE MOTION: the register started filling DURING this pass; every verdict above is moment-bound

Timestamped landings between 23:56 and 00:09 EDT: watch/inbox/fillball/ dir
00:02:04 with elder-salvage.md 00:08:55 (rank 2 receipt;
queue/lanes/elder/inbox.jsonl still 0 bytes at 00:09:21); lanes
fill-elder-salvage.json, fill-percolator-candidates.json, fill-seed-seal.json
under watch/inbox/gala_20260925/fillball-1001/lanes/ plus _191_8_grep_raw.txt
(rank 4 evidence); mag/percolator.py --candidates flag 00:05:48 with code
comments citing "GAP_REGISTER rank 6" (lines 23, 67, 484, 719); mag/
seed_seal.py 00:08:24 + state/keys/seed_seal_key (rank 5 seat half; ~/.mag
operator flip pending, drill test absent, zero .seal sidecars); day-1 window
register.jsonl 33,037 bytes at 00:09:12 (rank 7 fold landing as I stat'd;
DIGEST.md not yet present). Staged tool files (tools/m1_grammar_bench.py et
al., git status 'A') match a11's queue names by filename; purpose unverified.
Consequence: the lens's central frame ("nobody has fired anything") was a
census, and the census moved. Falsifier: the fillball lane files predate
22:53 (they do not; the dir is 00:02:04). Move: the next seat re-scores the
register AFTER fillball-1001 settles and files which of the 12 rows closed.

## Not run / OWED

- No gates or test suites run (document topic; matches the lens's scope).
- .zcode session-transcript search for the a15 fetch bytes: timed out twice
  (rc=124), inconclusive; the fetch is evidenced only by a15-rollup.json:68.
- fillball-1001's final state: the wave was still landing at 00:09:21; what
  closes by dawn is unproven here.
- Whether any other seat amended GAP_REGISTER.md after 00:09: not checked
  (single-pass scope; the register's mtime was still 18:41:58 at last stat).

## Receipt

Commands this session: ls --time-style=full-iso, grep (-c/-n/-rl/-o/-A2),
sed, tail, wc, date, rg (WinGet ripgrep 15.2.0), git log/status via
"C:\Program Files\Git\cmd\git.exe", schtasks via
C:\Windows\System32\schtasks.exe (MSYS_NO_PATHCONV=1), venv python json reads
(a09-a14, log tail), TaskStop on two oversized greps replaced by targeted
rg sweeps. Every number above carries the command that produced it or a
path:line cite. No em-dashes. Nothing asserted that I did not read or run.
