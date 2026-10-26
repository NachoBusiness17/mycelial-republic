# LINEAGE LENS: the GAP_REGISTER dogfooded at ~2026-10-01T23:00 EDT

Lens: lineage (what the estate asked before that was never delivered, and what
the current wave dropped between generations). Topic: the ranked gap table at
watch/inbox/gap_analysis_20261001/GAP_REGISTER.md. Every probe below was run by
this seat this session; anything I could not verify is marked OWED.

## A. The scorecard: which gaps are still real

Ten of the register's 12 rows are still real at my moment. Row by row, all
probes mine:

| rank | verdict | my evidence |
|---|---|---|
| 1 EstateWalkDaily | FIXED post-audit, scheduled re-fire pending | scripts/estate_walk_daily.ps1:5-13 carries the PATH LAW comment and absolute `$repo` paths; task action is DIRECT powershell (my Get-ScheduledTask enumeration: `powershell -NoProfile -ExecutionPolicy Bypass -File ...estate_walk_daily.ps1`, last=10/01 09:15 result=1, the pre-fix fire); logs/estate_walk_daily.log holds `END 2026-10-02T00:37:54Z exit=0` (the 10-01 ~20:37 EDT hand smoke). The 10-02 09:15 scheduled fire is pending at my moment: fix proven by bytes and by hand run, not yet by the scheduler. |
| 2 elder lens salvage | REAL | queue/lanes/elder/inbox.jsonl is 0 bytes, mtime Sep 4 10:43 (my ls). The register's ~10-02 falsifier clock (GAP_REGISTER.md:75, a05-r3 reported) is the next asset death in the table. |
| 3 citation_lint | REAL | `tools/citation_lint.py` does not exist (my ls, exit 2). |
| 4 191.8M errata | REAL | watch/inbox/48h_synth/STORY.md:240 carries "191.8M tokens spent" (my sed 238-242); grep -c "191" watch/inbox/frontier_olm_20260928/DIGEST.md = 0 at the STORY-cited path; no ERRATA file anywhere in watch/inbox/48h_synth/ (my ls + grep). |
| 5 seal gates | REAL | ~/.mag contains only steer_seal_seen/ (my ls); mag/seed_seal.py and tests/test_seal_forge_drill.py do not exist (my ls, exit 2 both). |
| 6 percolator intake | REAL | mag/percolator.py exists (30,757 bytes, mtime Sep 30 05:50) and grep -c "candidates" = 0. |
| 7 day-1 fold | REAL | watch/inbox/frontier_olm_2026-09-30/ top level is lens/, steal/, sweep/ only; no DIGEST/register/percolator_candidates at top level. |
| 8 index-last | PARTLY REAL, mis-summarized as binary | watch/inbox/INDEX.json now has 38 rows under frontier_olm_2026-10-01/ but every one points at lens/, steal/ or sweep/ content; the fold outputs exist on disk and each has 0 index rows: DIGEST.md, register.jsonl, percolator_candidates.jsonl, RECEIPT.md, steal/quantization-compression.md all grep 0 in INDEX.json. The content heal rode the OLM day-2 commit (2093ca518: "window rows 0 to 37, stale hashes healed"); the fold outputs were left behind. |
| 9 KVarN line | REAL | memory/runs/corpus_gap_research/ARXIV_REGISTER.json (233,406 bytes, mtime Sep 29 05:59), grep -ci "kvarn|2606.03458" = 0. |
| 10 reddit KV trio | REAL | grep -rn "1sy7srk" corpus/steal/ = 0 hits. |
| 11 three tickets | REAL, and its fact verified exact | watch/inbox/hermes_burn/TICKET_LEDGER.md exists (10,140 bytes, mtime Oct 1 17:35, so the organ is alive) and grep -c "SS-1|CP-1|R2-1" = 0; CP-1's premise verified: memory/percolator/invariants.json holds exactly 639 invariant rows and 0 carries depends_on (my python count over the dict). |
| 12 Vulkan move 1 | REAL and owner = THIS seat | my Win32_VideoController query: "AMD Radeon RX 5600 XT"; watch/inbox/spiking_wide/ newest files are 14:37-14:42 (the a06 burst outputs, pre-register), no probe receipt. The register's owner field ("seat on the RX 5600 XT box") reads like another machine; it is this one. |

## B. What the register itself dropped between generations

1. a09-a14 LANDED after the poll. GAP_REGISTER.md:13-15 promises "if a09-a14
   land later, they amend this register, they do not rewrite it". My ls of
   memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/lanes/
   shows a09-balls (18:49), a10-drops (18:53), a11-build-queue (18:45),
   a12-commits (18:54), a13-cadence (19:30), a14-coverage (18:48), each with a
   .checks.json. No amendment exists anywhere I looked; the register's
   "Lanes a09-a14 did not land" negative finding (GAP_REGISTER.md:237) is false
   at my moment.
2. The unamended lanes hold an S1 the register never carried: a13-cadence.json
   row "wrapper-kill" says scripts/invisible_runner.vbs never launches its
   child. I reproduced it independently: wscript run of the wrapper with a
   powershell child told to write a proof file and exit 7 returned rc=1, the
   rc log holds "1", and the proof file was never created. The mechanism is
   visible in scripts/invisible_runner.vbs:22-27: it builds a fully quoted
   string and runs `cmd /c "<child>" <args>`, and cmd /c cannot execute a .ps1
   (not in PATHEXT) while multi-quote lines get the first/last quote stripped.
   My Get-ScheduledTask enumeration shows four wrapper-routed cadences all
   result=1 on 10-01: MagImproveDaily 08:00, MagCensusPatrolDaily 08:30,
   MagFtsIndexDaily 09:00, MagLeaveProtocolDaily 08:00. EstateWalkDaily is NOT
   wrapper-routed (direct action), so the rank-1 fix addresses its true defect
   and should survive 10-02 09:15.
3. Live damage arc of that kill, verified by me: a13 measured
   tools/corpus_fts_rebuild.py --check --deep at rc=2 (index stale) around
   19:30; catalog/catalog.jsonl moved 19:43; catalog/catalog_fts.sqlite was
   rebuilt 19:45; my own check at ~22:55 returns true rc=0, "index_state":
   "fresh", "deep": "match". But logs/fts_index.log has no entry after
   Sep 30 09:00, so the heal was a silent hand-run that bypassed the sanctioned
   writer's logging, and the healer cadence itself is still wrapper-dead. Who
   ran the 19:45 rebuild: OWED (unknown seat, no receipt I could find).
4. Also landed in a13 and confirmed as booleans by my task enumeration but not
   otherwise re-verified: Estate Ratchet result=1 (NEW unregistered violation
   at tools/hermes_burn.py:237 plus 4 growth claims, blocks the next pre-push
   per a13-r3), MagTipWitnessDaily result=2 and MagXRadarDaily result=2 (dark
   surfaces with unacted alarms).

## C. The lineage verdict: the register declared first-of-kind over living organs

GAP_REGISTER.md:16-19 states "No prior gap register existed anywhere ... This
is the first." That grep covered corpus/steal, memory/research_polished and
watch/inbox/*.md only. The estate has a machine-written gap ledger:
training/loop_gaps.jsonl, schema mag_loop_gap.v1, 337 rows, dedupe-hashed
(lines 1-3, first rows 2026-08-06), and its last row is timestamped
2026-10-01T22:38:06Z, four hours before the register claimed none existed. The
uncited organ lineage now runs: loop_gaps.jsonl (08-06, live, machine) ->
MagGapSentinelDaily (daily cadence, fired 10-01 08:15 exit 1 by design with an
unanswered flag, per a13 notes) -> TICKET_LEDGER.md (09-30, fresh today 17:35)
-> a10-drops SCHEDULED/OWED/DEAD master list (18:53) and a11-build-queue
cost-if-unpaid-48h table (18:45) -> GAP_REGISTER (~18:30Z). Five generations of
gap organs; none cites its elders; the sibling lanes adopted dedupe keys
(a09 "idem", a13 "idempotency_key") while the register's 12 rank rows carry
none and have no status column, so it cannot express that rank 1 is fixed and
rank 8 is half-fixed. This is the lens's own jacket, wearing the register:
the estate reinvented its forgotten organ and declared it new in the same
document.

## D. Meta-gap dominance, dogfooded

The register's dominant class (MINED-NEVER-SCHEDULED, GAP_REGISTER.md:44-49)
survives its own dogfood: 10 of 12 rows untouched within ~4 hours of writing.
But the deeper pattern the register missed: rows do not move in rank order.
The two rows that moved moved for non-rank reasons: rank 1 because a falsifier
clock (the 10-02 09:15 fire) forced a seat, rank 8's content half because the
OLM commit healed the index as a side effect. And the register is itself an
instance of its own dominant meta-gap: grep -c "gap_analysis"
watch/inbox/INDEX.json = 0 (the index was rebuilt at 18:00 today, the register
was written after and never indexed), and grep of queue/todo.md and
HANDOFF_MAG_AGENT_TODOS.md for GAP_REGISTER/gap_analysis = 0 hits. The lane
table for the next 100M-token job is scheduled on zero surfaces. The class the
register missed entirely is cadence health: zero table rows about the estate's
own execution surfaces failing, although rank 1 was exactly that and a13 proved
five more, several of which the register's own severity law ("breaks a live
trust/safety gate", GAP_REGISTER.md:29-30) would rank at the top, since the
dead FTS healer means the next catalog move re-stales the index with no working
automatic cure.

## E. Falsifiers for this write-up

- Any of the 10 REAL rows landing flips its verdict: rerun the probes in
  section A verbatim.
- An INDEX.json or todo.md pointer to the register, or a loop_gaps citation in
  GAP_REGISTER.md, would falsify section C's self-instance claim.
- A 10-02 morning where the four wrapper cadences return result=0 would
  falsify the wrapper-kill severity (and my reproduction would need recheck).
- A register amendment commit merging a09-a14 would falsify "amendment clause
  unexercised".

## F. OWED (not verified, not asserted)

- The elder-lens ~10-02 clock text: register-reported and a05-reported; I
  verified inbox.jsonl is empty, not the card's own terms.
- a09, a10, a11, a12, a14 findings: I read only their headers; only a13's
  claims were independently probed.
- Author of the 19:45 FTS rebuild: unknown.
- The 10-02 09:15 EstateWalkDaily scheduled fire: pending at my moment.
- The register's five byte-checked quotes (GAP_REGISTER.md:226-233): taken on
  the register's word, not re-grepped by me except where they overlap my probes.
