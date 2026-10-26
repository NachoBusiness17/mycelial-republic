# BREAK-LOGIC - hostile pass on lens-logic (OUROBOROS R2, 2026-10-05)

Filed by break-logic. Every check below ran this sitting from this seat, repo
venv where Python was needed (.venv/Scripts/python.exe; bare python is
forbidden by the seat law and one call was hook-blocked and redone). Moments:
exec-archive ls twice, ~08:42Z and ~09:05Z, both identical (lanes e01-e08
only, mtimes 01:19-02:38, no FOLD_SECTIONS.md, no RUNNER.dwf.ts, no
manifest.json). Instruments that would not run from this seat are named
not-run.

## VERDICTS

### Finding 1 (fold gate cannot count the verdicts its runners persist): CONFIRMED, one fence correction

Every byte reproduces:

- tools/mickey17_v2_fold.py:181 reads `c.get("unconfirmed")`; zero
  `deep_tier2` tokens in the 234-line file (my grep; only :181 and :191 match
  "unconfirmed").
- The lie is byte-provable in the prior run's own output, not just in code
  shape: memory/runs/mickey17_v2/runs/2026-10-04-0/FOLD_SECTIONS.md prints
  "verdicts: checks 10, deep_tier2 12, entries 5, supports 45" AND
  "excluded: 0" in the same file. The script counted the deep_tier2 list in
  its verifier table and excluded none of them in its PRISMA flow.
- "Runners persist deep_tier2" is confirmed by design bytes, not just the
  prior archive: mickey17-burn.dwf.ts's own return contract says "tier-2
  verdicts persisted (deep_tier2)" and its tier-1 merge clause says "keep
  existing keys incl. deep_tier2, replace only lane/supports/counts"
  (verified list, my read of the :590-600 region). The exec archive's checks
  files carry only tier-1 keys (lane/supports/counts, checks, entries, rows;
  my parse of all 7) because the deep phase has not fired; that is mid-flight
  state, not counter-evidence. Prior-run structure verified: r05 checks holds
  a top-level `deep_tier2` LIST of 4 entries (my venv parse).
- The lens's OWED item (fold invoked from disk vs captured bytes) is
  RESOLVED by bytes it did not open: mickey17-burn.dwf.ts:493 and :502 run
  `world.run("bash", [FOLD_SH, ...])` where FOLD_SH = WSOUT + "/fold_run.sh"
  (:121), and the failure message at :499 names "Tool:
  tools/mickey17_v2_fold.py". The fold invokes the repo tool at fold time, so
  the pre-fold window is real for THIS (third) run, not the fourth.

CORRECTION (not fatal): "blocked-by: none (the R1 'coordinates e12' fence is
stale, no e09+ lane exists on disk)" is operationally wrong. The exec genre
lane table (mickey17-burn.dwf.ts:213-226) DEFINES e12-falsification-gate
whose task (b) edits tools/mickey17_v2_fold.py (the unbound-aggregate
check). Lane files are progress; the lane table is the assignment. The lens
read the wrong surface. blocked-by is executor-fence (pending e12 owns the
same file), expiring only if the run is confirmed dead: last lane write
02:38, gate cert 04:39 (REGISTRY.jsonl row 86), no filer artifacts at 09:05.
Run liveness is NOT CHECKABLE from this seat (ListWorkflowRuns returned
capability-gap here; stated as not run).

SHARPENER the lens missed: even full executor success does not close this
gap. e12's fold edit is the unbound-aggregate check (the 191.8M class), NOT
the deep_tier2 walker. The third fold can fire with e12 landed and still
print excluded:0. The finding survives the executor entirely; only the
landing spot is fenced.

### Finding 2 (no stop-cert clause, no FIRE_LEDGER): CONFIRMED

- grep -inE "stop.?cert|fire_ledger|retired" over tools/workflow_gate.py
  (384 lines) = 0 hits, RC=1 (my run).
- REGISTRY.jsonl line 75 is byte-exact as cited: ts 2026-10-04T02:34:06Z,
  tree-doctrine-dig.dwf.ts, PASS, digest d2a6783b55be (my grep -n). Stronger
  than the lens claimed: the same digest minted at lines 13, 19, 22, 23, 24,
  25 AND 75, seven certs for the retired script, not three.
- memory/workflows/ holds REGISTRY.jsonl only (my ls; 88 rows through
  2026-10-05T05:20:28Z). No FIRE_LEDGER.
- blocked-by: none STANDS. e04 (the only exec lane owning workflow_gate.py)
  landed 01:46 / checked 01:58; registry rows 87-88 show G8-class fixture
  FAILs (fail_g8.dwf.ts, g8-width-violation-fixture, 05:19-05:20) proving
  the gate file is live and post-dates e04; no pending lane claims it.
- Fresh instance the lens missed (folds into the same sitting): registry
  rows 83-84 show kit-50wide.dwf.ts minting two identical-digest PASS certs
  11 seconds apart (2026-10-04T19:58:40Z / 19:58:51Z, digest 398a58942b31
  both). Re-cert spam is ongoing for LIVE scripts too; a same-digest
  same-verdict dedup guard is the natural sibling clause to stop-cert in the
  same edit.

### Finding 3 (10 OLM percolator rows held outside the store): CONFIRMED

- My live re-run: store memory/percolator/candidates.jsonl = 29 rows; OLM
  file watch/inbox/frontier_olm_2026-10-04/percolator_candidates.jsonl = 10
  rows; claim-head cross-match (normed, 80-char) = 0/10 filed; AQLM rows in
  store = 0. The 0/10 held even AFTER e05 grew the store 19 -> 29 (e05 filed
  the r07 top-10, a different ten; e05-transfer-debt.checks.json supports
  row 1, my read).
- The move is verified end-to-end, which the lens asserted but did not
  check: mag/percolator.py:544 ingest_candidates consumes exactly the OLM
  schema (claim, source_url at :585, estate_map, probe per the :550
  comment); the --candidates CLI exists (:977). Idempotence proof
  byte-verified: e05 checks supports row 2 quotes "rerun: n_candidate 0
  n_dupe 10".
- blocked-by: none STANDS (e05 landed and closed; no other exec lane touches
  the store).

### Finding 4 (CURIOSITY rows 8 and 9 have no executor lane): WEAKENED

The surface bytes are real and re-verified: grep -c
"ai-engineering-from-scratch" catalog/catalog.jsonl = 0 (RC=1) at catalog
mtime 2026-10-05 06:57; grep map_asof|consumption|MONITOR_LANE over
queue/lanes/research/surface.md = 0 (RC=1).

But the load-bearing clause "no executor lane" is false by assignment:
mickey17-burn.dwf.ts:224 defines e11-catalog-research = "EXECUTE
curiosity-register rows 8 and 9" with EXACTLY the lens's proposed close
(sanctioned incremental rescan, grep-count non-zero, FTS consumption query,
rate onto surface.md, feed-or-kill row). Row 10 is likewise owned by
e12 (:225). The 12-lane table at :213-226 assigns every register row; only
lanes e09-e12 have not LANDED (no files at two ls reads). The lens's method
section read lane files as the assignment surface; the thesis sentence
"rows 8-10 residuals plus the R1 held rows sit in no lane's task field" is
false for rows 8-10 by these bytes. blocked-by flips: none -> executor-fence
(e11), with the honest expiry condition: no lane has landed since 02:38 and
no RUNNER/manifest has been banked (09:05 read), so IF the run is confirmed
dead the fence expires and the close proceeds; that call needs the
coordinator's run-state instrument, which this seat cannot reach (not run,
named above).

## ADDITIONS (what the lens missed)

1. THE BUILD-WAVE OWED ROWS IT NEVER TABLED. The ask's gap register 2
   names four owed rows; the lens's table and amendments touch only one
   (B2 cache-receipt stamping, its amendment 4, cite verified this
   sitting at b2_cache_receipt.md: "deepseek nominal hit 96.6% while
   receipt-verified reads 0.0%"). Two more are open, owner-filed, and
   absent from the lens entirely:
   - watch/inbox/build_wave_20261005/b1_knowledge_graph.md:70 "29 remaining
     dangling edges are the pre-existing already_inside defect (prose
     we_have entries never matching real module ids)".
   - b7_sweep.md:35 "17 real drifts + 21 CASE-ONLY false drifts
     (uppercase-hex seal rows vs lowercase actuals - a patrol comparison
     defect worth an owner fix)" with the Owed block at :120-123.
   One-sitting close (~20 min): casefold the digest comparison in
   tools/prepush_seal_patrol.py plus one fixture with an uppercase-hex seal
   row proving zero case-only drift. Second sitting: the B1 edge pass in
   mag/knowledge_graph.py (map prose we_have module refs to real module
   ids until the 29 dangling edges resolve). Falsifier: a re-run of
   `prepush_seal_patrol --rows 1000` shows 0 case-only drifts, or the
   graph rebuild counts 0 already_inside dangling edges.
2. E06 IS THE LIVE INSTANCE OF FINDING 1'S DISEASE IN THE RUN BEING
   WATCHED. e06-fidelity-audit.json landed 02:38 with 5 executed rows
   (my parse: register row 5 executed, structural infidelity banked) and
   is the ONLY landed lane with no .checks.json (7 of 8 have one; every
   other lane's checks landed within ~25 minutes of its json; e06's is 6+
   hours overdue at 09:05). When the third fold fires, its verifier table
   will count "lanes with persisted checks: 7" and e06's five verdicts do
   not exist for the recount, the exact A3 class the fold script warns
   about at tools/mickey17_v2_fold.py:164-165. Close (~10 min): re-fire
   the tier-1 folder pass for e06 only (write e06-fidelity-audit.
   checks.json per the merge clause), or hand-bank it from the lane
   file's own quote rows if the run is dead; finding 1's amendment should
   also add a lane-vs-checks completeness line so the casualty header
   names the hole. Falsifier: e06's checks file appears before the fold
   (the in-flight pass may still write it).
3. ROW 8'S COVER STORY IS FALSIFIED BY TODAY'S BYTES. Register row 8 and
   the lens both frame the catalog zero as "until the next 03:30 rescan".
   catalog.jsonl was rewritten TODAY (mtime 2026-10-05 06:57, my ls) and
   the 5,401-row holding STILL greps zero. So the gap is not snapshot age:
   either the rescan writer does not walk corpus/library holdings or no
   rescan ran (the mtime may be another writer). e11's close must
   therefore verify the writer COVERS the holding (read the walk set),
   not merely run it and re-grep; a run-and-grep on a blind writer
   re-proves the zero. Falsifier: the rescan log or catalog_manifest
   names corpus/library in its walk set and a post-rescan grep counts
   non-zero.

## Not run / limits

- Run liveness of dwfrun-e9656e14: ListWorkflowRuns is capability-gapped in
  this session; the fence-expiry calls above hang on the coordinator
  checking it.
- The 110 dwfrun journal records in .zcode state: not opened (carried from
  R1, same as the lens).
- Sibling lens files in this inbox: not read; three sibling break- files
  landed while I worked (break-communication.md appeared between my 08:42
  ls and a 08:50 grep), so the inbox is live and any sibling-side closure
  of findings 2 or 3 after ~08:36 would postdate my greps. My finding 2
  and 3 greps ran ~08:43-08:50 against the named files and held.
- GAP_REGISTER.md open rows: sampled by grep (build-wave tokens = 0 hits,
  so no duplication with addition 1), not exhaustively re-censused.
