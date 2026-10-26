# moonshot-1: dogfood pass on GAP_REGISTER.md (2026-10-01)

Lens: moonshot. Topic: `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md`, the ranked
gap table from the 100M audit. Method: every rank re-verified against estate bytes this
session, not adopted from the register's own claims. All checks run in this window.

## Scorecard: 1 of 12 closed, 11 verified still open, 1 half-proved fix

| rank | register claim | byte verdict this session |
|---|---|---|
| 1 | EstateWalkDaily red, repeats 10-02 | FIXED (script absolute, `$repo` at scripts/estate_walk_daily.ps1:11, PATH LAW comment lines 5-10); smoke END `2026-10-02T00:37:54Z exit=0` in logs/estate_walk_daily.log; schtasks shows Last Result 1 (the 10-01 pre-fix fire), Next Run 10/2 9:15 AM. BUT the alarm channel was never exercised: `grep ESTATE-WALK-BAKE-FAILED memory/attention.md` = zero hits, and fill spec 1 (GAP_REGISTER.md:89-92) demanded proof of BOTH channels on an injected failure |
| 2 | elder inbox empty, clock closes ~10-02 | OPEN: queue/lanes/elder/inbox.jsonl is 0 bytes, mtime Sep 4 10:43. The register's tightest live clock, zero motion |
| 3 | citation_lint absent | OPEN: no tools/citation_lint.py on disk |
| 4 | 191.8M phantom, ERRATA owed | OPEN: `sed -n 240p watch/inbox/48h_synth/STORY.md` still reads "191.8M tokens spent"; `find watch/inbox -maxdepth 2 -iname "*ERRATA*"` = zero hits |
| 5 | seal gates unarmed | OPEN: ~/.mag holds only steer_seal_seen/ (no mode sentinel, no keyfile); no mag/seed_seal.py; zero .seal sidecars under mag/ and state/; seed/verify_seal.py:1-13 confirmed hashes-only (docstring "check every file in MANIFEST.sha256 against its hash", hashlib.sha256, no asymmetric verify) |
| 6 | percolator zero-ingestion | OPEN: mag/percolator.py:558-567 argument list has no --candidates flag |
| 7 | day-1 fold missing | OPEN: watch/inbox/frontier_olm_2026-09-30/ contains only lens/, steal/, sweep/ (no DIGEST.md, register.jsonl, percolator_candidates.jsonl) |
| 8 | day-2 outputs unindexed | OPEN, confirmed exactly: DIGEST.md, RECEIPT.md, register.jsonl, percolator_candidates.jsonl, arxiv_deepread.xml sit in watch/inbox/frontier_olm_2026-10-01/ and my INDEX.json grep for top-level files under that window returned zero rows (only lens/steal/sweep paths are indexed) |
| 9 | KVarN line owed | OPEN: memory/runs/corpus_gap_research/ARXIV_REGISTER.json mtime still Sep 29 05:59, zero hits for KVarN or 2606.03458 |
| 10 | trio dropped by dedupe | OPEN: zero hits for 1sy7srk or 2609.21341 in watch/inbox/frontier_olm_2026-10-01/steal/quantization-compression.md (the newest of the three window copies) |
| 11 | SS-1/CP-1/R2-1 unticketed | OPEN: watch/inbox/hermes_burn/TICKET_LEDGER.md exists (10,140 bytes) but mtime is Oct 1 17:35, one hour BEFORE the register landed (18:41), and zero hits for SS-1, CP-1, R2-1, or top-12 |
| 12 | spiking Move 1 unfired | OPEN: watch/inbox/spiking_wide/ holds 8 analysis files, no Vulkan gate-probe receipt |

## Findings

1. RANK 1 IS FIXED BUT HALF-PROVED. The green path is proven by hand (log END line,
   window extended to 10-02), but the repair's whole point was that BOTH channels went
   silent on 10-01, and the alarm channel (scripts/estate_walk_daily.ps1:19-21,
   Add-Content to memory/attention.md) has never fired in any recorded run. a08's own
   below-cut ledger named "red AND silent" as the third failure shape the falsifier
   battery must cover (GAP_REGISTER.md:224). The 10-02 09:15 fire runs a green-proven
   script with an unproven alarm: if the alarm line has its own defect, a red fire
   reproduces the exact S1 shape the fix exists to kill.

2. THE REGISTER'S CENTRAL THESIS IS CONFIRMED AND UNSTARTED. Eleven of twelve
   one-sitting fills, all specced by the register at 18:41 Oct 1, show zero byte motion
   hours later. Zero scheduling surfaces consumed the register: a repo grep for
   GAP_REGISTER across watch/, memory/, queue/, tools/, mag/, scripts/ hits only the
   autoseal index events, librarian inventory rows, a RACTORSWARM_MAP mention, a
   librarian cite, the MICKEY17 addendum, and the lane archive. Zero hits in
   queue/todo.md, TICKET_LEDGER.md, or memory/attention.md.

3. THE DOMINANT META-GAP EATS THE REGISTER ITSELF. a15's own steal card
   (memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/a15-rollup.json:31)
   says "adopt the register's top-12 as a ticket batch into
   watch/inbox/hermes_burn/TICKET_LEDGER.md". Unexecuted. The document that names
   MINED-NEVER-SCHEDULED as the dominant class (GAP_REGISTER.md:44-49) is itself the
   class's newest instance. A register with no consumer is prose, not a lane table.

4. MISRANKS BY THE REGISTER'S OWN LAW. (a) Rank 3 (build a linter, one sitting) outranks
   rank 4 (a 15-minute erratum, GAP_REGISTER.md:104) inside the same S1/one-sitting band,
   inverting the register's own cheapest-cure-first rule (GAP_REGISTER.md:26). (b) With
   rank 1 closed, rank 2's falsifier clock (closes ~10-02) is the top live row, and the
   register has no mechanism to promote it: the amend clause (GAP_REGISTER.md:13-15)
   covers late lane landings only, not closures or fixes. The rank-1 row still asserts
   the defect "repeats 10-02 09:15 with the same relative-path defect" (GAP_REGISTER.md:74),
   which is now false. FIXED-BUT-UNRECORDED is a meta-gap class the register's four do
   not name; the estate already owns the counter-pattern (census_drift_patrol's
   staleness tripwire on the AGENTS.md census claim) and never pointed it at registers.

5. THE REGISTER MISSED ITS OWN RUN'S GAP. The gap-analysis run's phase-4 prose fold
   never landed: MICKEY17_V2_RUN_SPEC_ADDENDUM.md:160 grepped "gap-analysis-of-the-estate"
   across watch/inbox and found only GAP_REGISTER.md, which carries no top-steals,
   DISPUTED, or go-list sections. The register audits 8 sibling lanes and carries no row
   for its own run's unclosed fold duty. The auditor's window is the one window absent
   from the table.

## The moonshot swing

GAP_REGISTER should not be a markdown table; it should be a machine-readable queue
(GAP_REGISTER.jsonl: rank, status, last_verified stamp, receipt pointer per row) plus a
register_drift_patrol that re-verifies each row's claim against disk on a cadence and
fails loud when verified_state drifts, pattern-copied from census_drift_patrol. The
one-sitting version: mint the 12 TICKET_LEDGER rows (a15's own card), append a status
column, and run the rank-1 failure-injection proof. That converts the register from a
document about scheduling into an actual schedule, and it is the "schedule-and-fire
pass" the register says the next 100M-token job should be, started at toy scale.

## Honest limits

- I did not run the failure-injection bake test myself (it would append to the shared
  memory/attention.md alarm surface); proposed as the move, not executed.
- I did not re-poll the lanes dir for a09-a14; the register's 8-sibling coverage claim
  is adopted from its own provenance section plus the a15 lane JSON.
- I did not read all 8 sibling lane JSONs; the row-level claims ride the register, my
  checks were against the estate state each row names.
- Rank 10 was grepped in the 10-01 steal copy only.
- The "hours later" timing is from mtimes (register 18:41, ledger 17:35, script 20:35,
  smoke 00:37Z), not from commit archaeology.
