# DOGFOOD LENS: the GAP_REGISTER eaten by its own dog (2026-10-01)

Lens: dogfood / organ mapper. Topic: watch/inbox/gap_analysis_20261001/GAP_REGISTER.md,
the ranked lane table from the 100M audit. Test: which gaps are still real, which
are already fixed, which are misranked, which meta-gap class dominates, what the
register itself missed. Every claim below was checked this session against estate
bytes; anything I could not check is marked OWED.

## Headline: the register is 1 of 12 filled, and the one fill it claimed for itself is not wired

I ran the register's own checks back against the estate ~18h after it landed.
Score: rank 1 (EstateWalkDaily) is fixed and smoke-proved. The other 11 rows
byte-reconfirm as still real. And the register's own line 247 ("Nothing in this
register is a fill claim except fill 9's fetch half, which was executed in-lane
with raw-byte verification") fails its own standard: the receipt and relabel that
fill 9's spec names never landed. Details per finding below. The register named
MINED-NEVER-SCHEDULED as the dominant meta-gap (GAP_REGISTER.md:44-49) and then
exemplified it: a table that tells the next job what to fire, which nobody has
fired, sitting on the same zero-execution surface it diagnosed.

## Row-by-row dogfood results (all run this session)

| rank | register claim | my check | verdict |
|---|---|---|---|
| 1 | bake fires red, repeats 10-02 with same defect | scripts/estate_walk_daily.ps1:5-13 carries the PATH LAW fix (absolute $repo/$log/$alarm); logs/estate_walk_daily.log ends `END 2026-10-02T00:37:54Z exit=0` (the by-hand smoke run, window 2026-08-04..2026-10-02 baked); schtasks EstateWalkDaily: Last Result 1 (the old 10-01 09:15:01 fire), Next Run 10/2 9:15 AM, Status Ready | FIXED in code, smoke-proved; the row is stale and the 10-02 09:15 fire is the remaining live proof point |
| 2 | elder lens unbanked, inbox 0 bytes mtime Sep 4 | ls: queue/lanes/elder/inbox.jsonl = 0 bytes, Sep 4 10:43 | STILL REAL; only row with a falsifier clock closing 10-02 (tomorrow) |
| 3 | tools/citation_lint.py absent | ls: No such file or directory | STILL REAL |
| 4 | STORY.md:240 191.8M fails byte check | sed -n 238,242p shows "191.8M tokens spent" at STORY.md:240; grep -c "191" frontier_olm_20260928/DIGEST.md = 0 | STILL REAL; ERRATA.md absent from watch/inbox/48h_synth/ |
| 5 | steer_seal unarmed, no seed_seal port, no forge drill | ~/.mag holds only steer_seal_seen/ (no keyfile, no mode sentinel); mag/seed_seal.py absent; tests/test_seal_forge_drill.py absent | STILL REAL on all three prongs |
| 6 | percolator zero-ingestion, no --candidates flag | grep "candidates" mag/percolator.py = 0 hits; grep -c "candidates" memory/percolator/invariants.json = 0 | STILL REAL (organ-side check confirmed; the register's "0 consumers in mag/tools/scripts" breadth I only partially reproduced: substring hits exist in mag/arxiv_mine.py etc., presumably the writer side, not ingest - full consumer census OWED) |
| 7 | day-1 window uncitable, fold missing | ls frontier_olm_2026-09-30 = lens, steal, sweep only; no DIGEST.md, no register.jsonl, no percolator_candidates.jsonl (day-2 sibling has all three) | STILL REAL |
| 8 | day-2 headline outputs unindexed | grep INDEX.json for the 4 exact paths (DIGEST.md, register.jsonl, percolator_candidates.jsonl, RECEIPT.md under frontier_olm_2026-10-01) = 0 hits while sweep/ and steal/ siblings are indexed | STILL REAL, precisely as specced |
| 9 | KVarN line undelivered | ARXIV_REGISTER.json mtime Sep 29 05:59; grep KVarN and 2606.03458 = 0 hits | STILL REAL |
| 10 | trio dropped by day-2 dedupe | grep -c "1sy7srk\|2609.21341" in frontier_olm_2026-10-01/steal/quantization-compression.md = 0 | STILL REAL |
| 11 | SS-1/CP-1/R2-1 none ticketed | TICKET_LEDGER.md exists (10140 bytes, Oct 1 17:35) with zero hits for SS-1, CP-1, R2-1 | STILL REAL; the commit message named SS-1 but naming in a commit is not a ledger row |
| 12 | spiking MOVE 1 scheduled nowhere | watch/inbox/spiking_wide/ holds 8 sweep files, no Vulkan probe receipt | STILL REAL |

## Findings

### F1. The register's own amendment clause is live and unexercised (the register missed its own trigger)

GAP_REGISTER.md:14-15: "if a09-a14 land later, they amend this register, they do
not rewrite it." The lanes dir poll was ~18:30Z; a15-rollup.json is mtime 18:39
EDT; a09-balls.json through a14-coverage.json landed 18:46 to 18:53 EDT the same
evening (ls --time-style=full-iso). Six lanes of gap material (a09 ball-receipt
audit, a10 drops master SCHEDULED/OWED/DEAD list, a11 unpaid build queue with
one-sitting costs and blockers, a12 64-commit git-log audit, a13 cadence rows,
a14 coverage-gap lens) landed minutes after the rollup closed. No amendment
exists. Organ: librarian + attention market. One-sitting move: merge the 6 lanes'
rows into GAP_REGISTER.md as an amendment section per its own clause, re-ranking
the table with their findings included. Cost: ~30 min. Falsifier: an amendment
section appears in GAP_REGISTER.md, or the 6 lanes prove to contain nothing
rank-relevant beyond a01-a08.

### F2. The register's one self-claimed executed fill is a phantom citation of its own (meta-gap 3 inside the register)

Fill 9 (GAP_REGISTER.md:124-129) says the theneurondaily fetch is DONE with raw
fxtwitter bytes of 203,655 bytes, and orders: append the receipt beside
sweep/inference-efficiency-x.md and relabel 0.55 to primary-confirmed. I checked:
grep for "203,655" and "203655" across watch/inbox/frontier_olm_2026-10-01/ = 0
files; inference-efficiency-x.md:52 still reads "Confidence 0.55" with the
truncated-snippet caveat; no receipt file exists beside the sweep. The raw-byte
verification may have happened in the a15 lane's session, but the estate artifact
was never landed, so the claim is unverifiable from disk and by the no-fabrication
law it is OWED, not done. This is exactly the jacket my lens wears: the finding
filed but never wired, riding in the very document that warns about the class.
Organ: context pack intake (the sweep feeds later seats' briefs). One-sitting
move: re-run the fetch or mark it OWED in the register, then land the receipt
beside inference-efficiency-x.md and flip the 0.55 label; 15 minutes. Falsifier:
the receipt bytes surface somewhere outside the day-2 window, or the label flips
with a receipt.

### F3. Misranked by its own ranking law, and the clock row is not first

Ranking law (GAP_REGISTER.md:24-26): rank = severity x fill-ease, cheapest-cure
first inside a severity band. Rows 9 and 10 are S3; rows 11 and 12 are S2; all
four are fill cost one-sitting. Yet the table order is 9, 10, 11, 12
(GAP_REGISTER.md:82-85): two S3 rows ride above two S2 rows with equal fill cost,
violating the law as written. Worse, rank 11 (mint SS-1, CP-1, R2-1 into
TICKET_LEDGER.md) is the keystone one-sitting in the whole table: it is the
literal act of scheduling, the direct counter to the dominant meta-gap, and it
converts three rows of unscheduled work into owned work for the price of 3 ledger
rows. And rank 2 is the only row with a falsifier clock that closes 10-02
(tomorrow at write time); with rank 1 now closed, rank 2 is the effective top of
the table and is unfilled. Organ: attention market (TICKET_LEDGER is the
scheduling surface; queue/lanes/elder is a gala lane inbox). One-sitting move:
re-sort the register by its own law, mint the 3 ticket rows (fill 11, ~15 min),
and bank the elder lens row (fill 2, ~20 min) before 10-02. Falsifier: the
register is re-sorted with a documented reading of the ranking law as
fill-ease-dominant, or the tickets and elder row land and the ordering stops
mattering.

### F4. Meta-gap class dominance confirmed, with one correction: GATES-UNARMED is also the slowest-moving class

MINED-NEVER-SCHEDULED dominates exactly as claimed: 11 of 12 rows unfilled in
~18h, zero fills fired from a table whose own header says it tells the next job
what to fire (GAP_REGISTER.md:5-6). The correction: meta-gap 4 (GATES LIVE BUT
UNARMED, GAP_REGISTER.md:63-68) is the class with zero estate motion of any kind
since the audit. The 10-01 commits keep naming the disease (5d2263f10: "the
Ed25519 port spec exists at pam.md and never landed, zero .seal sidecars; SS-1
ticket named") while ~/.mag gained nothing but steer_seal_seen/ all day (ls
~/.mag, one subdir, mtime Oct 1 14:29). Rank 3's citation_lint is the same shape:
spec written, tool absent, pre-push hook unwired. Organ: MCP bridge + the gate
organs (githooks/pre-push, verify_seal at consume). One-sitting move: land
mag/seed_seal.py to the pam.md spec plus tests/test_seal_forge_drill.py (fill 5's
seat half), and build tools/citation_lint.py to the accuracy.md spec wired after
the ratchet (fill 3), proving it on ractor50's 2 known drifts. Falsifier: ~/.mag
gains a keyfile and mode sentinel, or seed_seal.py and citation_lint.py exist
with a wired hook line.

### F5. What the register structurally could not see: the librarian organ's disease map and the standing executor that landed after it

Two landings postdate the register and change its owner column. Commit 962e41054
(LIBRARIAN EXPEDITION) banked three new diseases the register's four meta-gaps do
not cover: D1 arXiv-id matching blind even to id-bearing holdings (28 of 257
receipts seen), D2 the duplicate detector's disjointness guard is a comment not
code, D3 hash verdicts without content reads (verify_canon ok on a 4096-null-byte
file). Meta-gap 3's fix (citation_lint at pre-push) lints claims-to-disk; the
librarian's D1/D3 are the holdings-side cousin (disk-to-receipts), which no
listed fill touches. And commit f4cfcdf9b (RACTORSWARM) landed the standing
8-lens ractor engine, which is the concrete answer to the register's owner column
saying "any seat" 10 times: the accuracy lens owns fills 3 and 4, the operations
surgeon owns fill 1, the lineage miner owns fill 2, and the engine's
per-finding-move stage is the schedule-and-fire pass the register says the next
100M job should be (GAP_REGISTER.md:48-49). Organ: librarian (INDEX/holdings) and
the ractor engine as executor. One-sitting move: append a register amendment row
naming the librarian's D1/D2/D3 as register-relevant gaps with the ractor engine
lenses as named owners. Falsifier: the register is shown to already carry the
librarian diseases (it cannot; the commit postdates it), or an amendment naming
them lands.

## OWED (could not verify this session)

- The full mag/tools/scripts candidates-consumer census behind rank 6's "0
  consumers" parenthetical (I verified the organ side: mag/percolator.py has zero
  candidates hits).
- Whether the a09-a14 lane content duplicates a01-a08 (I read their ask fields
  and key structures, not every row).
- The 10-02 09:15 EstateWalkDaily fire result (tomorrow; the task's Last Result 1
  predates the fix).
- Whether the a15 fetch of theneurondaily actually happened in-session (the raw
  bytes claim is plausible but unwired to any estate surface I can grep).

## CORRECTION (hostile second pass verdict, re-checked 2026-10-02)

The hostile pass verdicted the headline WEAKENED and the re-check sustains it on
two of three charges. Corrections to the text above:

1. THE ~18h NUMBER IS WITHDRAWN. Byte truth: GAP_REGISTER.md mtime 2026-10-01
   18:41:58 EDT; committed as 5d2263f10 at 20:46:30 EDT; my original checks ran
   the same evening, roughly 3h after write and 1h after commit. "18h" was
   unreproducible arithmetic, never byte-backed.
2. ROW 10's "STILL REAL" CELL IS WITHDRAWN AS SCORED. The register's premise
   "zero mentions anywhere" is byte-false: grep -rln "1sy7srk" returns 4 estate
   surfaces (frontier_olm_20260928/DIGEST.md; frontier_olm_20260928/sweep/
   kv-cache-context-engineering-reddit.md:34 which cites "the held 09-28 depth
   tables (1sy7srk)"; frontier_olm_2026-09-30/DIGEST.md; the a01 lane JSONs).
   2609.21341 appears in both DIGESTs. What is actually missing is the KV table
   BYTES in the day-2 card's OWED ledger, not "mentions anywhere".
3. THE HEADLINE'S DOMINANCE VERDICT INVERTED WITHIN ~3h OF COMMIT. The
   fillball-1001 wave (watch/inbox/gala_20260925/fillball-1001/) landed fills
   citing the register's own row numbers in code: mag/percolator.py:23,67 and
   :484,719 ("GAP_REGISTER rank 6", --candidates flag + review-pass ingest,
   memory/percolator/candidates.jsonl 39163 bytes Oct 2 00:16); mag/seed_seal.py:4-5
   ("ticket SS-1 = GAP_REGISTER rank 5"); queue/lanes/elder/inbox.jsonl 2024
   bytes Oct 2 00:09 (rank 2); frontier_olm_2026-09-30/ now carries DIGEST.md,
   register.jsonl, percolator_candidates.jsonl (rank 7); INDEX.json now carries
   3 day-2 headline paths (rank 8 partial). Re-checked open set as of this
   correction: rank 3 (citation_lint absent), rank 4 (STORY.md:240 still
   191.8M, no ERRATA under watch/inbox newer than 10-01 20:00), rank 9
   (ARXIV_REGISTER.json mtime 2026-09-29, 0 KVarN), rank 11 (TICKET_LEDGER zero
   SS-1/CP-1/R2-1 rows even though seed_seal.py self-declares the ticket), rank
   12 (spiking_wide 0 vulkan/move1/r0 files). Rank 5 is half-landed (seed_seal
   port yes; tests/test_seal_forge_drill.py absent; ~/.mag still unarmed). The
   register is not a mined-never-scheduled artifact; it is a live lane table
   that drove execution. The 10-02 09:15 EstateWalkDaily fire remains the open
   proof point for rank 1's fix.

## ERRATUM 2 TO THE CORRECTION (estate-wide grep completed)

The background estate-wide grep for the trio (1sy7srk / 2609.21341 outside
gap-analysis surfaces) completed after the correction was filed and shrinks row
10's residue further:

- 1sy7srk's FULL MEASURED KV TABLE IS ALREADY BANKED in the estate:
  frontier_olm_20260928/sweep/kv-cache-context-engineering-reddit.md:44 holds
  the complete depth table (decode tok/s at 0/32K/128K/256K/512K/1M for
  f16/q8_0/turbo3/turbo4, 3 reps, 8h wall clock), plus :19 and :38. The
  09-28 DIGEST.md:459 carries the full thread title as U2.
- 2609.21341 appears in SIX surfaces: frontier_olm_20260928/DIGEST.md,
  RECEIPT.md, steal/open-and-local-language-models-arxiv.md,
  frontier_olm_2026-09-30/DIGEST.md, frontier_olm_2026-10-01/sweep/
  open-local-language-models-reddit.md (the day-2 window's OWN sweep), and
  watch/inbox/fillball/day1-digest.md.
- The day-1 DIGEST.md:82 explicitly names "The rank-10 pair" as owed debt,
  so the register's row 10 is already tracked by the fold that landed.

Net: row 10's true residue is a bookkeeping pointer only - the day-2 card's
OWED ledger lacks a cross-reference to table bytes already banked at
frontier_olm_20260928/sweep/kv-cache-context-engineering-reddit.md:44. It is
not a content gap, and the register's "zero mentions anywhere" was its own
phantom-citation-class member.

## receipts

Checks run this session: sed/grep/ls/find on the paths above; schtasks query via
powershell for EstateWalkDaily; python (venv) json reads of lanes a09-a14. No
fabricated numbers; every table cell traces to a command in this session.
Correction-session checks: git log/show timestamps, ls --time-style=full-iso,
targeted greps listed in the correction block, plus the completed estate-wide
grep cited in Erratum 2.
