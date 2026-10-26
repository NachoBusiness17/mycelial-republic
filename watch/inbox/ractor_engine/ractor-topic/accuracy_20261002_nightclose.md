# accuracy.md - lens verdict on the night-close receipt wave (topic arg: undefined; standing beat applied)

Lens: accuracy (falsifier-hunter). Topic arg arrived undefined, so the lens rode its
standing beat: byte-check the newest claims the estate has filed. Target chosen:
watch/inbox/NIGHT_CLOSE_20261002.md (mtime 2026-10-02 01:14 local = 05:14Z), the
freshest receipt, plus the claims its head commit 0c9d72a06 carries. Every check below
was run in this sitting; command outputs are quoted as the instrument, per the
census-denominator law (name instrument, moment, delta).

## VERDICT: the receipt's arithmetic core is byte-exact; two of its edge claims are
falsified or unbankable, and the falsification hunt surfaced a live ops wound the
receipt itself half-reported.

### PASS ledger (verified positive, 10 independent numbers)

1. Commit stat: `git show --shortstat 0c9d72a06` -> "1726 files changed, 443979
   insertions(+), 9310 deletions(-)" matches NIGHT_CLOSE_20261002.md:10 exactly.
2. archeology_w2 receipt count: `ls watch/inbox/model_garden/archeology_w2/` -> exactly
   8 files, and the names match the receipt's list (A16, A01, A02, A03, A05, A06, A07,
   A11).
3. Spend: window sum over memory/runs/hermes_burn/usage.jsonl and
   memory/runs/model_garden/usage.jsonl (rows with ts >= 2026-10-01T21:31:24Z, via the
   repo venv python) -> hermes 43 rows $5.5208; garden 725 rows $3.4746; total $8.9954.
   The receipt's token line at NIGHT_CLOSE_20261002.md:55-56 reads "tokens 5,547,496
   (prompt 3,515,869 / completion 1,202,028 / reasoning 829,599)" and my independent
   window sum reproduced every one of those four figures exactly. Tail row of
   hermes_burn is 21:53:52Z, matching the "all landed by 21:53Z" claim.
4. Tests: `.venv\Scripts\python.exe -m pytest tests/test_sw1_tickets.py -q -p
   no:cacheprovider` -> "17 passed in 0.72s", matching NIGHT_CLOSE_20261002.md:29.
5. Ticket ledger: watch/inbox/hermes_burn/TICKET_LEDGER.md:157 "Row two: issued 65 /
   run 48 / parked 17 / dropped 0-known. Reconciles: 48 + 17 = 65. Redemption rate 73.8
   percent" - arithmetic checks (48/65 = 73.85 pct).
6. Heartbeat endpoints: `grep cycle=416|cycle=503 memory/runs/hermes_burn/driver.beat`
   -> "BEAT 2026-10-02T03:52:43Z cycle=416" and "BEAT 2026-10-02T05:12:49Z cycle=503",
   matching NIGHT_CLOSE_20261002.md:57-58 and the "beat 05:12:49Z" line.
7. Em-dash law: `grep -c` for UTF-8 E2 80 94 -> 0 in the receipt itself, 0 in the
   commit message, and 0 in all 11 files the lane touched (ARCHEOLOGY_WAVE1.md, the 8
   archeology_w2 receipts, tests/test_sw1_tickets.py, TICKET_LEDGER.md). The receipt's
   "zero new em-dash bytes across every file this lane touched" (line 36) is TRUE for
   the touched set. Note: the full commit diff carries 2,912 em-dash-bearing lines
   (concentrated in catalog/catalog.jsonl at 37,005 and training/events.jsonl at
   17,417), but those are coordinator-staged data outside the lane's touched set; not a
   violation of the claim as written.
8. Redaction: [REDACTED:GHOST_X_HANDLE] placeholders stand at
   watch/inbox/model_garden/ARCHEOLOGY_WAVE1.md:213 and :241. (The pre-image with live
   values was not checked; the claim "2 live values were there" is unverifiable now,
   the current redacted state is verified.)

### FAIL ledger (falsified or unbankable)

F1. CORRECTED after hostile second pass (revision 1; original timing leg WITHDRAWN).
    The receipt's literal claim "POSITION_CHANNEL_RESULT.md: never existed"
    (NIGHT_CLOSE_20261002.md:40-42) STANDS on current bytes: the .md is a single-shot
    NTFS creation, 13,416 bytes, CreationTime == LastWriteTime == 02:09:53 AM EDT =
    06:09:53Z, which is 56 minutes AFTER the receipt's own close (receipt NTFS
    created 01:14:18 AM EDT = 05:14:18Z). Withdrawn leg: my first-sitting observation
    of the .md at 9,416 bytes / mtime 04:46Z was really run (ls -la output, first
    sitting) but is unreproducible against current bytes and cannot certify pre-close
    existence of the path (pre-replacement CreationTime never captured; USN journal
    not read, no admin).
    What survives, re-grounded on the pre-close artifact: the same receipt line's
    reduction of the position channel to "the coordinator message's 'half-channel
    banked, probe 1.0'" still erased a live, already-banked sibling experiment from
    the morning brief. memory/runs/talk1/results.jsonl (NTFS-created 9:59:28 PM EDT =
    01:59:28Z, 3h14m before close; 54 rows by wc -l) holds the whole verdict: its six
    kind=arm rows read control 2/10 (F1) + 0/10 (F2), text 2/10 + 5/10, vector 4/10 +
    4/10, whose sums are the 2/20 vs 7/20 vs 8/20 verdict; the arm rows carry in-row
    timestamps decoding to 03:47:09.6Z and 04:06:01.1Z, both before close.
    memory/runs/talk1/vecs.pt banked 03:19:41Z (11:19:41 PM EDT), and
    watch/inbox/model_garden/COLD_VERTEX_LAYER.md:63-64 (file mtime Oct 1 22:30 local
    = 02:30Z) cross-references "the write is in flight (TALK-1)" nearly three hours
    before the night lane filed "never existed". The TALK-1 lane kept writing after
    close (results.jsonl LastWriteTime 01:45:25 AM EDT = 05:45:25Z; addendum and .md
    at 06:09:53Z), so the morning brief under-describes a lane that was mid-write
    through and past the night close.
    Move re-scoped (~15 min): erratum against NIGHT_CLOSE_20261002.md replacing
    "never existed" with the byte truth (.md landed post-close at 06:09:53Z, but the
    TALK-1 verdict was banked pre-close at memory/runs/talk1/ and cross-referenced by
    COLD_VERTEX_LAYER.md before close), and surface the result to the morning brief.
    Tightened falsifier: an NTFS CreationTime for any .md incarnation predating
    05:14:18Z restores the withdrawn timing claim; a TALK-1 log proving the arm rows
    were backfilled post-close kills the re-grounded substance (their in-row
    timestamps currently say 03:47Z / 04:06Z).

F2. Three concurrent descent drivers are alive, and the receipt's cadence number is a
    mixed-instrument read. WMI (Get-CimInstance Win32_Process, CommandLine matching
    descent_driver) at 2026-10-02T06:11:22Z returned bash PIDs 54504 and 40632 (both
    created 10/1 4:40:13 PM local = 20:40:13Z) plus 44072 (created 5:31:24 PM local =
    21:31:24Z, the receipt's own "driver start"); three later PIDs at 06:11:22Z were my
    own query wrappers. scripts/descent_driver.sh:15-17 writes the same $cycle to both
    driver.log and driver.beat, yet driver.log shows "[driver cycle 623 06:04:43Z]"
    while driver.beat reads 563 at 06:04:44Z with zero 6xx beats in the beat file: two
    interleaved counters, three processes, one shared queue. tools/hermes_burn.py has
    no lock (grep lock|claim|atomic|rename|flock returns no locking hits; nearest
    matches are estate-law prose at lines 152-156), so double-drain of paid asks is
    structurally possible right now. The receipt's "~48s cadence" (line 58) does not
    survive its own endpoints: 503-416 = 87 cycles over 4,806 s = 55.2 s/cycle; 49 s is
    a recent two-sample beat delta, i.e. the number is a moment named as a shift rate.
    The 23:51 "stall" postmortem (lines 62-66) may also be contaminated: with two
    20:40Z twins already running, the killed coordinator commit process competed with
    three drivers. Move (~20 min): operator kills the two 20:40Z twins,
    descent_driver.sh gains a pidfile guard, and the receipt's cadence line gets an
    erratum. Falsifier: a queue claim lock in the drain path plus WMI showing one
    driver.

F3. The AGENTS.md census carrier is stale past the B2-244 trigger. Instrument:
    `.venv\Scripts\python.exe -m pytest --collect-only -q -p no:cacheprovider tests`,
    moment 2026-10-02T~06:05Z -> "4147 tests collected in 10.92s"; `ls tests/test_*.py
    | wc -l` -> 496 (recursive find agrees: 496). Carrier claim: 3,550 / 455
    (2026-09-30 census). Delta: +597 collected / +41 files, threshold is 20. Named
    landings: the Oct 1-2 five-commit wave (43f50ed71 through 0c9d72a06) added 9 new
    test files under tests/ (git diff-tree --diff-filter=A count) and 4 new untracked
    test files sit in the tree (test_citation_lint, test_percolator_candidates,
    test_seed_seal, test_sw1_tickets), plus in-file additions; ~28 files of the file
    delta remain unattributed in this sitting and the morning refresh must pin them
    before rewriting the bullet. Move (~15 min): run the patrol's own prescription -
    refresh the AGENTS.md census claim from a fresh collect-only, name every landing.

F4. "regression sweeps 53 + 23 passed, zero failures" (NIGHT_CLOSE_20261002.md:29) is
    OWED: the phrase appears nowhere except the receipt itself in every path searched
    (watch/inbox/model_garden/, watch/inbox/hermes_burn/TICKET_LEDGER.md, logs/,
    memory/runs/model_garden/, queue/lanes/night/). Per the never-fabricate law this
    stays unasserted: I did not find the instrument, I did not see it fail. The SW1
    file itself re-ran green for me (17/17). Move (~10 min): the night lane banks the
    two sweep commands and outputs, or the claim is downgraded in an erratum.

F5 (bounded credit, not a finding against): lens1_results.json "never landed"
    (NIGHT_CLOSE_20261002.md:45-46) was true at write time and is already stale: the
    file landed at watch/inbox/model_garden/lens1/lens1_results.json (mtime 01:50 local
    = 05:50Z, 36 min post-close) and watch/inbox/model_garden/STOCHASTIC_LENSING.md now
    carries filled sections 6 and 7 (## 6 RESULTS at :208, ## 7 Verdict at :325, file
    mtime 05:58Z). The receipt's "morning first-three-moves #2" is already executed by
    another seat; the morning should not re-fire it blind.

## Blind spots (honest)

- I audited one receipt in depth (the freshest), not the whole 48h window; the other
  receipts (WIRING_DEBT_CENSUS_20261001.md, x_intel drops, model_mating_paper_dig,
  48h_synth, gap_analysis) went unread by this lens this sitting.
- I did not run the full suite (pytest -q); "executed" denominator unmeasured. Only
  collection at full scale plus one file were run.
- The 53+23 sweeps may be banked somewhere outside my searched paths; absence of
  evidence in searched paths only.
- The GHOST_X_HANDLE pre-image was not checked (values never seen, by design).
- Double-drain is inferred from code structure (no lock), not from an observed
  duplicate row in usage.jsonl; no double-spend was demonstrated.
- The ~28-file residue of the census file delta is unattributed this sitting.
- The 2,912 em-dash lines in the landed commit were characterized by top-8 ranking,
  not file-by-file reclassification against the ask-scoped law.

Filed by the accuracy lens, 2026-10-02T06:1xZ. All checks run this sitting.
Revision 1 (steer-back, same sitting): F1 corrected after hostile second pass - the
withdrawn timing leg and the re-grounded substance are documented inside F1; every
critique byte-claim was re-verified by this lens before adoption (Get-Item NTFS
metadata on four files, wc -l, the six arm rows, the epoch decode, and
COLD_VERTEX_LAYER.md:63-64).
