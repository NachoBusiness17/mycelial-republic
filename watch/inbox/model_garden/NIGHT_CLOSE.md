# NIGHT CLOSE running summary (night lane, 2026-10-02)

Running fold of the still-landing, maintained by the night-shift lane. Final
report: watch/inbox/NIGHT_CLOSE_20261002.md. Bytes over reports; every claim
below was verified on disk this shift.

## 03:5xZ fold (shift start)

- COORDINATOR COMMIT LANDED as 0c9d72a06 "THE MODEL GARDEN NIGHT (24-wide day
  2)" on branch mag/run-beta1-factory-build-audi-20260806T231709Z: 1726 files,
  +443,979/-9,310. The 23:51 EDT attempt was NOT a deadlock: it was the
  precommit secrets scanner grinding a per-file `git show` subprocess pass over
  1726 staged blobs (the gate is O(files) subprocesses by design). The real
  blocker the scanner found: ARCHEOLOGY_WAVE1.md carried 2 live occurrences of
  the GHOST_X_HANDLE value (P0 containment catch, values never printed here).
  Redacted in place to [REDACTED:GHOST_X_HANDLE], re-staged, gate re-passed
  (1726 files clean against 46 live env values), committed. Lesson banked: a
  "stalled" commit on this repo is first a suspect for a live secrets-catch,
  second for scanner slowness, never assume lock disease without the lock file.
- POSITION_CHANNEL_RESULT.md: DOES NOT EXIST on disk (checked
  watch/inbox/model_garden/ and grepped the tree). The position channel landed
  only as the half-channel probe banked inside the coordinator commit message
  ("probe 1.0"). Premise of the fold order was stale on bytes; skipped honestly.
- STOCHASTIC_LENSING.md section 6/7: still PENDING RUN, and the run itself is
  HALF-LANDED: lens1_run_log.txt shows gemma2:2b load (227s), 18 greedy frame
  answers (710s), 60 cloud samples (2392s); kache captures kept landing through
  01:43:44Z (last rows: qwen2.5:3b L9/L18/L27 P10 capture rows in
  memory/runs/kache/captures.jsonl). But NO lens1 python process is alive now,
  lens1_results.json never landed, and the P1-P5 predictions were never
  evaluated. The captures are banked (the expensive part); the analysis phase
  is a cheap local re-run candidate for the morning (lens1_row_zero.py with the
  captures already on disk; check whether it has a resume-from-captures path
  before re-firing anything).

## 05:1xZ fold (archaeology wave 2, first tranche)

8 receipts landed under watch/inbox/model_garden/archeology_w2/ (note: the
plan table names watch/inbox/archeology_wave2/ as its receipt root; the night
orders' path governs tonight's tranche):

- A16_LENS1_VERDICT.md: premise falsified (results never landed; run died
  post-captures at 01:43Z), repair ticket filed (analysis-only amend).
- A01_X_GENEALOGY_ERA01.md: the ENTIRE core vocabulary (chord relic, seed,
  republic, mycelial, verkle, spore) minted in one 48h public window
  2026-03-02..03; the Mar-2 chord relic is byte-confirmed the oldest
  artifact ("Test chord: 44 28 K13 e4 Fool", 05:31:15 GMT).
- A02_ERA2_DOCTRINE_BIRTHS.md: standing-wave minted Aug 11 ~23:42 EDT, cold/
  lensing by Aug 12, all inside the stillbirth window; PREMISE CORRECTION:
  water computer is a 09-04 coin, not Aug (zero Aug water hits across 92
  transcripts + 960 marathon requests + STEAL_0814 family).
- A03_ERA345_DRIFT.md: MEMORY.md live index 35/35 resolve (zero rot), but
  0/441 phantom rooms ever built and zero era-4/5 coverage: the index is an
  abandoned era-3 snapshot that does not say FROZEN.
- A05_X_VOICE_DEVICES.md: 130-post census; two-voice law confirmed (broadcast
  voice = 30 pct direct-address shitpost; the protocol/mycological register
  lives only in the syndication receipts).
- A06_CHORD_KACHE_FUSE.md: chord.v2 spec, strike() gains a position_ledger
  block reading captures.jsonl (both colds in one report; one-sitting impl).
- A07_COLD_ROUTE_TICKET.md: route_work() adopts the COLD-PAYS trial's paid
  shape (8 coldest + 2 divergence, sharedness-size cap).
- A11_ZEITGEIST_004_DRAFT.md: era-004 candidate THE LENS with three
  falsifiers (aquifer rival, instrument-decay, operator word); era-003 file
  27 days stale flagged.
- A-04 skipped: X re-harvest needs the operator's logged-in X surface; not a
  free lane tonight. A-20 consolidation requires 15+ lanes (8 landed).

## Live surfaces at fold time

- Descent driver: alive, beat every ~48s, cycle 416 at 03:52:43Z, left alone
  per orders.
- A fillball-1001 lane is still landing fresh artifacts (seed_seal.py,
  citation_lint.py, tests, corpus folds) that postdate the coordinator commit;
  intentionally NOT committed mid-flight; check its state at dawn.
