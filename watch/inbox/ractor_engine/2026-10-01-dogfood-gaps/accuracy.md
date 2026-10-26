# ACCURACY LENS: dogfood of GAP_REGISTER (2026-10-01)

Lens: accuracy (falsifier-hunter). Topic: watch/inbox/gap_analysis_20261001/GAP_REGISTER.md.
Method: every ranked row re-checked against estate bytes this session, commands named inline.
Law: anything not verified here is marked OWED, never asserted. No em-dashes.

## Verdict

The register's per-row accuracy is high: its STORY.md:240 line pointer is exact, 2 of its 5
byte-checked quotes reproduce at exactly 1 grep -cF hit, and 11 of 12 ranked rows verify still
live. But the register went stale at its own landing on coverage (six lanes on disk for ~2 hours
before the commit that says they never landed), it instantiates its own meta-gap 3 twice inside
its first day, and its dominant-class thesis is confirmed and STRENGTHENED: in its first day
exactly 1 of 12 rows moved (rank 1), fixed as the headline of the same commit that shipped the
register unamended; the register itself converted zero rows.

STEERING CORRECTION (hostile second pass, 2026-10-01): this file's original finding 4 claimed
"2 of 12 moved, both as side effects". That count was byte-false: rank 8 never moved. INDEX.json
(mtime 18:00:56 -0400, post-heal, pre-register-write) holds exactly 38 frontier_olm_2026-10-01
rows (6 lens + 4 steal + 28 sweep, all lane files matching the heal's "window rows 0 to 37") and
0 rows for every member of rank 8's named set: DIGEST.md, register.jsonl,
percolator_candidates.jsonl, RECEIPT.md, arxiv_deepread, and the day-2
steal/quantization-compression.md card. The heal (2093ca518, 16:44:35 -0400) also predates the
register's own write (GAP_REGISTER.md mtime 18:41:58), so rank 8's state never changed after the
audit read it. An earlier "39 paths" figure in this file was a miscount; the true count is 38.
Finding 4 below is the corrected version.

## Row-by-row dogfood (commands run this session)

- Rank 1 EstateWalkDaily: FIXED-IN-WAITING, not open. scripts/estate_walk_daily.ps1:5-13 carries
  the PATH LAW comment (2026-10-01 repair) and absolute paths; logs/estate_walk_daily.log ends
  "END 2026-10-02T00:37:54Z exit=0" (hand smoke, mtime Oct 1 20:46). schtasks //Query //TN
  EstateWalkDaily //V //FO LIST reads: Last Run 10/1/2026 9:15:01 AM, Last Result 1 (the pre-fix
  fire), Next Run 10/2/2026 9:15:00 AM, Enabled. GAP_REGISTER.md:74 still lists it open, and both
  the fix and the register rode the same commit 5d2263f10 (2026-10-01T20:46:30-04:00). The fix is
  happy-path-proven only: grep -c ESTATE-WALK-BAKE-FAILED memory/attention.md = 0, so the alarm
  channel has never fired, and fill 1's "prove BOTH channels fire on an injected failure"
  (GAP_REGISTER.md:90-92) has no receipt anywhere (watch/inbox/48h_synth/ holds 6 files, none a
  receipt; gap_analysis_20261001/ holds only GAP_REGISTER.md).
- Rank 2 elder-lens: LIVE. queue/lanes/elder/inbox.jsonl is 0 bytes, mtime Sep 4 10:43 (ls -la),
  matching GAP_REGISTER.md:75 exactly. The ~10-02 falsifier clock closes within hours of this sit.
- Rank 3 citation_lint: LIVE. tools/citation_lint.py does not exist (ls: No such file); grep
  citation_lint githooks/pre-push = 0 lines.
- Rank 4 191.8M phantom: LIVE and the register's pointer is EXACT. grep -n 191.8M
  watch/inbox/48h_synth/STORY.md = line 240, "191.8M tokens spent"; grep 191
  watch/inbox/frontier_olm_20260928/DIGEST.md = 0 hits; watch/inbox/48h_synth/ contains no
  ERRATA.md (listing: STORY, lattice, laws, measure, next, steals).
- Rank 5 seal gates: LIVE. ls C:/Users/foste/.mag = only steer_seal_seen/ (Oct 1 14:29), no
  steer_seal_mode, no keyfile; mag/seed_seal.py and tests/test_seal_forge_drill.py both absent.
- Rank 6 percolator: LIVE. grep candidates mag/percolator.py = 0 hits (no flag, no string).
- Rank 7 day-1 fold: LIVE. ls watch/inbox/frontier_olm_2026-09-30/ filtered on
  DIGEST|register|percolator = nothing (exit 1).
- Rank 8 index-last: LIVE, verified precisely rather than by proxy. INDEX.json contains 39
  frontier_olm_2026-10-01 paths (lens/steal/sweep files, the 16:44 EDT heal from 2093ca518
  "window rows 0 to 37") but none of the four fold outputs; INDEX.json's entry shape is proven by
  the indexed counterpart "frontier_olm_20260928/DIGEST.md" and
  "frontier_olm_20260928/register.jsonl". Day-2's DIGEST.md, RECEIPT.md, register.jsonl,
  percolator_candidates.jsonl sit on disk unindexed. Not misranked.
- Rank 9 KVarN: LIVE (KVarN half). grep -c 2606.03458
  memory/runs/corpus_gap_research/ARXIV_REGISTER.json = 0, file mtime Sep 29 05:59.
- Rank 10 trio carry-forward: LIVE in substance, BROKEN in pointer. The day-2
  steal/quantization-compression.md has 0 hits for 1sy7srk and 2609.21341; but fill 10's path
  "steal/quantization-compression.md" (GAP_REGISTER.md:130-133) does not resolve at the
  corpus/steal reading (file absent there; repo find shows three window copies under
  watch/inbox/frontier_olm_2026-09-30|2026-10-01|20260928/steal/). See finding 3.
- Rank 11 three tickets: LIVE. grep SS-1|CP-1|R2-1 watch/inbox/hermes_burn/TICKET_LEDGER.md = 0 rows.
- Rank 12 Move 1: LIVE. ls watch/inbox/spiking_wide/ filtered on vulkan|move1|probe|receipt = nothing.

Misranked: nothing materially. Rank 1 was correctly S1 at write (48h clock, repeats 10-02 09:15)
and is now stale-not-wrong; rank 8 survives a precise re-check.

## Findings

1. TEN OF TWELVE ROWS BYTE-VERIFY LIVE; THE REGISTER HAS NO STATUS MECHANISM. Every row re-checked
   above with the exact commands; only ranks 1 (fixed in-script) and part of the index surface
   moved. The register (GAP_REGISTER.md:72-84) has rank/gap/lane/sev/cost/owner columns and no
   lifecycle field, so every consumer must re-derive liveness. Falsifier: any of the ten checks
   returning its filled state (ERRATA.md existing, a candidates flag landing) proves motion I
   missed. Move (15 min): append a status column recording today's checks, mark rank 1
   fixed-in-waiting with the alarm-channel proof as the residual.

2. COVERAGE STALE AT LANDING: SIX LANES SAT ON DISK ~2 HOURS BEFORE THE COMMIT THAT SAYS THEY
   NEVER LANDED. GAP_REGISTER.md:13-15 "Lane slots a09-a14 produced NO files in the lanes dir at
   poll time", :237 "Lanes a09-a14 did not land", :197 below-cut claims "none lost". Bytes: lanes
   dir mtimes a14-coverage.json 18:48:13 -0400, a09-balls.json 18:49:19, a15-rollup.json 18:39:32,
   a08-48h-synth.json 18:13:46; commit 5d2263f10 at 20:46:30-04:00 whose own message says "15/15
   lanes, 75 rows" while the register inside it says 8 siblings merged. The register's own
   amendment clause (lines 13-15: "they amend this register, they do not rewrite it") was never
   exercised; no amendment file exists in the directory. The register's poll-law claim
   (lines 238-239, "no late landings appeared") is true at its poll moment and false at its commit
   moment, the exact instrument-and-moment sin it catches in others at lines 241-244. My loose
   row instrument counts 33 unmerged rows in a09-a14 (5+5+8+5+5+5). Falsifier: an amendment file
   landing with a09-a14 content, or a09-a14 proving structure-only (no gap rows), shrinks this.
   Move (45 min): merge a09-a14 through the amend-not-rewrite clause with per-row grep spot-checks.

3. THE REGISTER COMMITS ITS OWN META-GAP 3 TWICE ON DAY ONE. (a) Fill 10's path
   "steal/quantization-compression.md" (GAP_REGISTER.md:130-133) does not exist at the
   corpus/steal reading; the real OWED-ledger surface is
   watch/inbox/frontier_olm_2026-10-01/steal/quantization-compression.md (one of three window
   copies; repo find receipt above), and that file holds 0 hits for the rows fill 10 wants
   appended. (b) GAP_REGISTER.md:241-242 asserts the theneurondaily 0.55 number "is now
   primary-confirmed" while watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-x.md:52
   still reads "Banked degraded per recipe ... Confidence 0.55"; no file matching
   receipt|fxtwitter|theneuron exists anywhere under sweep/ (grep -rl = nothing), and the
   203,655-byte evidence exists only inside a15-rollup.json (grep -o "203,655" = 2 hits there).
   The confirmation is lane-held, not surface-held: held-vs-cited disease in miniature. Falsifier:
   a receipt file beside inference-efficiency-x.md, or a pre-register git history of the 0.55
   relabel, refutes the phantom-state half. Move (20 min): land the owed receipt beside the sweep
   file, apply the relabel, and add GAP_REGISTER itself to rank 3's citation_lint test corpus.

4. MINED-NEVER-SCHEDULED CONFIRMED DOMINANT AND STRENGTHENED: EXACTLY 1 OF 12 ROWS MOVED.
   (Corrected by the hostile second pass; the original "2 of 12, both side effects" was
   byte-false.) Rank 1 is the only row with motion, and it moved as the HEADLINE of commit
   5d2263f10 (message first clause: "the audit caught a live bug now FIXED: EstateWalkDaily"),
   the same commit that shipped the register with its rank-1 row unamended. Rank 8 did NOT move:
   the index heal (2093ca518, 16:44:35 -0400) predates the register's own write (GAP_REGISTER.md
   mtime 18:41:58) and indexed only 38 lane files (6 lens + 4 steal + 28 sweep); INDEX.json
   (mtime 18:00:56 -0400) has 0 rows for every member of rank 8's named set (DIGEST.md,
   register.jsonl, percolator_candidates.jsonl, RECEIPT.md, arxiv_deepread, the day-2
   steal/quantization-compression.md card). The other 10 rows re-verified unmoved (finding 1's
   checks). GAP_REGISTER.md:44-49 names this class and line 49's thesis ("the next 100M-token job
   is a schedule-and-fire pass") is the thing that has not started; the estate's conversion
   surfaces (TICKET_LEDGER.md SS-1/CP-1/R2-1 = 0 rows, re-grepped this session) show zero rows
   converted. Falsifier (tightened): motion beyond rank 1 requires either an INDEX.json row for
   any member of rank 8's named set, or a TICKET_LEDGER / todo/CURRENT / depends_on entry dated
   10-01 or later for any of the 12 rows. Move (30 min): mint fill 11's three named tickets
   first; tickets are the one mechanism that outlives the window.

5. THE EVIDENCE BASE IS PARTLY MACHINE-UNREADABLE AND THE ROW DENOMINATOR DOES NOT REPRODUCE.
   Parse census (".venv/Scripts/python.exe -c" over lanes/a*.json, per-file try/except):
   PARSE_OK 14, TOTAL_ROWS 78 (a02=10, a11=8, twelve lanes=5); a01-olm-day2.json raises
   JSONDecodeError at line 38 column 587 (char 14084). The commit's "15/15 lanes, 75 rows" is
   therefore uncountable-by-machine on one lane and off by 3 under my instrument; a10-drops.json
   shows 27 occurrences of "id" against 5 counted rows, so my counter is loose and 75-vs-78 is
   UNADJUDICATED (OWED). Falsifier: a schema-run counter reproducing exactly 75, or a01 parsing
   cleanly after repair, retires the respective half. Move (30 min): fix a01's JSON syntax error
   and rerun the census with a fixed schema before the next job trusts the denominator.

## Credit where the register is exact

- STORY.md:240 pointer exact (grep -n verified).
- 2 of 5 byte-checked quotes reproduced at exactly 1 grep -cF hit: "scheduled on zero surfaces"
  in a06-spiking.json; "it is the synthesis' one number that fails a byte check" in
  a08-48h-synth.json. The other 3 not re-checked (OWED).
- Rank 8's fold-output claim survives the index heal because the heal covered only
  lens/steal/sweep; verified against INDEX.json entry shapes, not the 38-hit proxy.

## Not run / OWED

- Content of the 33 a09-a14 rows unread (structure and counts only): whether they hold new S1
  gaps that would rerank the table is OWED.
- 3 of 5 byte-checked quotes not re-checked.
- The fxtwitter sentence-level byte check inside the 203,655 bytes not independently performed
  (the artifact exists only as text inside a15-rollup.json; I verified the figure appears there).
- Rank 2's card-side falsifier clock terms not read (only the 0-byte inbox verified).
- The 10-02 09:15 scheduled fire is a future event; rank 1's cadence proof is unverifiable today.
- The "no prior gap register existed" historical grep not re-run (the register now exists, so the
  claim is not re-testable at this moment).
