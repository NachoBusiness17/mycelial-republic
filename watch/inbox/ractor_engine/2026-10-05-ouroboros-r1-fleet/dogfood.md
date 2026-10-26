# DOGFOOD LENS - OUROBOROS ROUND 1: the workflow fleet (2026-10-05)

Seat: lens-dogfood (organ mapper; jacket: the finding filed but never wired) of the ractor on
OUROBOROS ROUND 1 of 5. Topic: dogfood the standing WORKFLOW FLEET and steal the improvements
back into the definitions. Everything below was read or run this sitting on the tree at
C:/Users/foste/Documents/projects/local_sovereign_agent with Read, bash (ls/stat/find/cat/grep),
and full-file reads of both spec addenda, both master folds' headers, the saved runner
mickey17-v2.dwf.ts, the standing ractor-engine.dwf.ts, and tools/mickey17_v2_fold.py. No
em-dashes. Anything I could not verify is marked OWED. Sibling convergence flagged where a
second seat independently holds the same bytes (siblings: operations.md, economics.md, same dir).

## The round in one sentence (dogfood register)

The estate runs TWO defect ledgers today: the operator law ledger, which COMPILES (tools/lawlog.py
minted 2026-10-03, 66 laws compiled into a skill per state/CURRENT.md:46-48), and the engine
defect ledger (E1-E35 across the two run addenda), which has no compiler, no reader, and zero
byte landings; the ouroboros order exists because the second ledger's loop never closes itself.

## F1 (rank 1, CONVERGENT with operations F1 and economics' verdict-blindness row). The E-ledger never compiles: 35 filed items, 0 bytes landed, 10 days frozen

- Ledger census: run-0 addendum (watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md, read in full this
  sitting) carries E1-E18 (prose survives at commit 0c9d72a06 per its own header) plus E19-E32;
  read-estate addendum (watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md, read in full) continues
  E33-E35. E20 (verdict wiring) was filed TWICE, recurred at 5x in run 2 (5 substantive
  unconfirmations rode included while the fold printed excluded: 0), and is still 0 bytes.
- Instrument: `stat` this sitting - tools/mickey17_v2_fold.py mtime 2026-09-25 19:21:06,
  10743 bytes; .zcode/workflows/mickey17-v2.dwf.ts mtime 2026-09-26 16:33:33. Both predate all
  three mega-burns (Oct 3-5). Both read in full: line 181 still reads
  `for x in (c.get("unconfirmed") or []):` and lines 157-160 still sum list LENGTHS
  (`vc[k] += len(v)`); the runner still hardcodes MASTER_MICKEY17_V2.md 8x and writes no run
  manifest. Zero E-items are present in either file's current bytes.
- No compiler exists: `grep -rn "E_LEDGER|E-ledger" tools/ --include=*.py` hits only unrelated
  SURFACE_LEDGER/cost ledgers; no tool reads an engine defect ledger. Meanwhile
  `ls tools/lawlog.py` = 4158 bytes, Oct 3 - the estate built the compile pattern for laws and
  never ported it to the engine's own defects. This IS the jacket finding, measured: filed, twice,
  never wired.
- CONVERGENT: operations.md F1 (same instrument, same lines) + economics.md ("none of it flowed
  back"). Three seats, one defect: rank it first.
- Falsifier: any current fold printing excluded > 0 or yes/no value splits (fixed-string checks
  in both addenda measured 0 across five archived folds); or an E-item found in the fold tool or
  runner bytes as of this sitting (I read both in full: none).
- One-sitting move (~30 min): amendment-table rows 1-3 below - the fold edit (verdict values into
  PRISMA + value-split print + fold-moment stamp), the wrapper banking, the glob fix. Plus bank
  the ledger itself: memory/runs/mickey17_v2/E_LEDGER.jsonl seeded from the two addenda's E-lists
  with a `landed_in` column; the fold script's next amendment can then assert no E-item older
  than N days sits unlanded (the compile step lawlog already proves works at the operator layer).

## F2. The fold gate's only entry point is unversioned workspace bytes

- The wrapper every burn folds through lives ONLY outside the repo:
  `find . -name fold_run.sh` over the estate = 0 hits; `cat
  ~/.zcode/workspace/default/mickey17_v2/fold_run.sh` this sitting shows 20 lines that carry two
  live engine decisions: (a) `--check-urls` is always on - the exact surface of the 0-for-3 E21
  liveness defect (both fold-time dead verdicts failed to reproduce, addendum 1.3); (b)
  `--fired "${1:-0}"` - a missing arg silently becomes 0, which the fold tool converts to the
  file count (`fired = a.fired or n_files`, fold :120). That is a THIRD silent default under the
  E22 fired-circularity: runner passes TARGETS.length, wrapper defaults a missing arg to 0, tool
  defaults 0 to n_files.
- The saved runner points at it by workspace path (mickey17-v2.dwf.ts:81
  `const FOLD_SH = WSOUT + "/fold_run.sh"`), and the three draft forks carry the same FOLD_SH
  calls (read-the-estate.dwf.ts:301/307/310, execute-register.dwf.ts:280/284/287, per the
  operations sitting; not re-lined by me - OWED to their cites).
- Meaning for the organs: the deterministic-gate law (fold-by-script) is enforced through an
  artifact git cannot diff, no patrol walks, and a workspace clean would delete. The estate's
  own build discipline says fix the design, not the symptom; the design here is "gate entry
  point outside version control".
- Falsifier: a repo copy of fold_run.sh anywhere (find said 0); or a draft that invokes
  tools/mickey17_v2_fold.py directly without FOLD_SH.
- One-sitting move (~20 min): byte-copy the wrapper to tools/fold_run.sh, change
  `--fired "${1:-0}"` to `: "${1:?fired-count required}"` (missing arg now fails loud, killing
  the third default), and repoint FOLD_SH in mickey17-v2.dwf.ts:81 and the two live drafts to
  ESTATE + "/tools/fold_run.sh". Four file touches, zero logic change.

## F3. The standing ractor engine ships the OLM world-read defect class in its own receipt check

- ractor-engine.dwf.ts:315-320 (read in full this sitting):
  `const receiptGlob = await files.glob(OUT + "/SYNTHESIS.md");` - a glob on a LITERAL
  no-wildcard path. The comment at :311-313 admits the engine's first dogfood run died here and
  the chosen cure was fail-tolerance (route the rejection to a repair ask), not the plain-read
  fix. The repair ask at :322 tells the voice agent "The synthesis file ... does not exist.
  Write it now" - but a sandbox rejection does not mean the file is missing; on a false reject
  the repair ask needlessly REWRITES a banked SYNTHESIS.md.
- The engine knows the cure and even teaches it: the lens ask it dispatches carries the
  WORLD-READ LAW ("a glob on a literal no-wildcard path is rejected by the sandbox (the OLM
  2026-10-03 class)... wrap any glob in try/catch routing to a plain read") - the law lives in
  the ask prose (ractor-engine.dwf.ts:184-186) while the engine's own bank phase violates it 130
  lines later. Filed (the OLM receipt class), never wired (into the engine's own bytes).
- This is also the AGENTS.md build-discipline anti-pattern by name: "No fallback-branch creep.
  Found a design defect -> align and fix the design; never add another guard branch to mute the
  symptom." The try/catch-repair is precisely the guard branch muting the symptom.
- Falsifier: this harness's files.glob documented (or observed in a run log) to accept literal
  no-wildcard paths without rejection - then the receipt check is fine as written and only the
  wasted-repair risk remains; or a future ractor run whose log shows the receipt check passing
  on first glob with the file present.
- One-sitting move (~10 min): replace :315-320 with a files.read attempt in try/catch
  (ENOENT -> repair ask; read error that is not ENOENT -> log and skip repair), keep glob only
  for genuine wildcard patterns. Exact bytes in amendment-table row 3.

## F4. The verifier tier's report line inverts its meaning: "supports 50" where the bytes say 12 yes / 63 no

- The fold prints "verdicts: supports 50" as a key-name LENGTH sum (fold :157-162); run-0's
  persisted truth was 12 yes / 63 no across 75 tier-1 verdicts (run-0 addendum 1.1, byte-checked
  by that seat; not re-walked by me - carried). A downstream reader parsing "supports 50" reads
  endorsement; the truth was an 84% no-rate. Run 2: 48 no / 12 yes, decoded by hand again
  (read-estate addendum 1.1). Five folds, zero script-printed value splits (both addendas'
  fixed-string checks: 0 hits).
- Compounding, the runner's own conclusion sells the tier-2 score as fleet confidence:
  mickey17-v2.dwf.ts:362-366 returns "tier-2 verified 7/12 load-bearing rows" style phrasing
  while the tier-2 sample is ADVERSARIALLY selected - :240-245 ranks rows whose tier-1 verdict
  was "no" FIRST (noKeys.has -> better pri). 7-of-12 on a suspect-first sample is a triage
  score, not a quality estimate; the conclusion line drops that condition. The estate's own law
  (trust bytes, not reports) is violated by the fleet's report line about its own bytes.
- CONVERGENT core (E5/E20 value-blindness) with operations F1 and economics; the distinct
  dogfood addition is the NAMING defect: the fold's word "supports" and the runner's phrase
  "load-bearing rows" both read as endorsement instruments while measuring length and triage.
- Falsifier: any archived FOLD_SECTIONS.md printing yes/no or verified/unconfirmed splits (0
  across five, per both addenda's fixed-string checks); or a runner conclusion that names the
  tier-2 selection rule (none - :240-245 is silent in the output contract).
- One-sitting move: rides amendment rows 1 and 5 (fold prints value splits; runner conclusion
  reworded to "tier-2 (adversarially selected, tier-1-no first): X verified / Y unconfirmed of
  12 checked").

## F5 (the organ map). No engine output reaches any organ: the attention market carries zero burn rows, and the one steal-back that closed this week closed by operator re-seat, not by wiring

- Instrument: `grep -c "MICKEY17|READ_ESTATE|ouroboros|ractor_engine" memory/attention.md` =
  0 (full file, untruncated, this sitting); `grep -n "MASTER_"` on the same file = no hits. The
  attention organ's current tail is janitor instance-guard alarm noise (doubled-key checkboxes,
  2026-10-04 dungeon beats). Three mega-burns (94 + 60 + in-flight rows), two ractor engines,
  zero rows in the estate's attention market.
- The runs themselves name the unexecuted leg: run-0's master fold closes with "the LINKS rows
  and the percolator fire remain the one-wave leg" (corpus/steal/MASTER_MICKEY17_V2.md:237) and
  N10 counts 13 of 15 lanes zero-hit on memory/research_polished (the librarian organ never
  ingested the folds). Read-the-estate's own dominant finding class (proposed code 14,
  unread-output) is now the fleet's own condition: the fleet is the estate's biggest producer
  of unread output.
- The content steal-back that DID close (MASTER_READ_ESTATE.md section 9, the curiosity
  register, became execute-register's e-lane table) closed because the operator re-seated a new
  burn with the register as its targets - a human carrying the wire by hand. No organ holds
  "amendment table -> executor": the filer phase of the burn runner (mickey17-v2.dwf.ts:349-353)
  verifies existence-nonzero only, and the ractor engine's bank phase (:310-328) publishes an
  artifact file only. Both engines stop exactly one organ short of wiring.
- The ouroboros law itself (zero-amendment round = theater, commit 139f5198f) is the operator
  compensating for the missing organ; rounds 2-5 will each need the same compensation unless
  the wire lands this round.
- Falsifier: any memory/attention.md row sourced from a burn fold or ractor synthesis (grep says
  0 at my moment); or an existing tool that ingests corpus/steal masters into the percolator or
  LINKS (run-0's own fold calls the percolator fire "owed" - carried, not re-censused by me).
- One-sitting move (~15 min): amendment row 4 - one added ask in each engine's terminal phase
  appending the top-3 GO rows / ranked moves to memory/attention.md under a dated header
  (source path + one-line move each). Not a new organ: the organ exists; this is the port.

## RANKED AMENDMENT TABLE (executable; fold dedupes against the operations table - rows 1 and 6 are CONVERGENT, the rest are this lens's)

| # | Workflow file | Exact edit | Defect prevented | Evidence row |
|---|---|---|---|---|
| 1 | tools/mickey17_v2_fold.py:179-202, :154-166, :227-228 | walk `c.get("deep_tier2")` lists, count verdict values "unconfirmed"/"crashed" into PRISMA excluded under code 9 (match on `row_key`, not claim); print tier-1 yes/no and tier-2 verified/unconfirmed VALUE splits beside the length sums; write a fold moment (ISO stamp) into the FOLD_SECTIONS.md header | excluded: 0 while 5 unconfirmed rows rode included (run 2); "supports 50" endorsement reading vs 12 yes/63 no truth; fold state undateable without stat (E7) | fold :181/:157-160 read this sitting; READ_ESTATE addendum 1.1-1.2; run-0 addendum 1.1; CONVERGENT operations row 1 |
| 2 | tools/fold_run.sh (NEW, banked from ~/.zcode/workspace/default/mickey17_v2/fold_run.sh) + FOLD_SH repoint in .zcode/workflows/mickey17-v2.dwf.ts:81 and both live drafts | bank the wrapper into the repo; replace `--fired "${1:-0}"` with `: "${1:?fired-count required}"`; repoint FOLD_SH to ESTATE + "/tools/fold_run.sh" | gate entry point outside version control (workspace clean deletes the gate); third silent default in E22's fired circularity; --check-urls decision unversioned on the E21 surface | find = 0 repo hits; wrapper cat'd this sitting; runner :81 |
| 3 | .zcode/workflows/ractor-engine.dwf.ts:315-323 | replace `files.glob(OUT + "/SYNTHESIS.md")` with `files.read(OUT + "/SYNTHESIS.md")` in try/catch: ENOENT -> fire the repair ask; any other error -> log "receipt check unreadable (not ENOENT), skipping repair" and DO NOT rewrite | OLM 2026-10-03 glob-on-literal class shipped inside the standing engine; wasted repair ask rewrites a banked SYNTHESIS.md on false reject (fallback-branch creep, AGENTS.md build discipline) | ractor-engine.dwf.ts:315-323 read this sitting; the WORLD-READ LAW prose at :184-186; first-dogfood death note at :311-313 |
| 4 | .zcode/workflows/mickey17-v2.dwf.ts:349-353 (estate-filer ask) + ractor-engine.dwf.ts:310-328 (bank phase) | add one ask: "append the top 3 GO-list rows (or ranked moves) to C:/Users/foste/Documents/projects/local_sovereign_agent/memory/attention.md under a `## <date> <run slug>` header, one line each: move + source path"; filer verdict gains a fourth check "(d) attention row appended" | burn and ractor outputs never reaching any organ (N9/N10 transfer leg owed since run 0); amendment tables owned by nobody; the operator manually carrying the wire each round | grep -c MICKEY17|READ_ESTATE|ouroboros|ractor_engine memory/attention.md = 0 (full file); MASTER_MICKEY17_V2.md:237 |
| 5 | .zcode/workflows/mickey17-v2.dwf.ts:361-366 (conclusion) + :373 (verified[]) | reword conclusion tier-2 clause to "tier-2 (adversarially selected: tier-1-no rows first) X verified / Y unconfirmed of 12 checked"; correct verified[] line "the fold recount counts every list-valued key, so they exist for the recount" to add "(as length sums only; value splits land with fold amendment row 1)" | triage score sold as fleet confidence ("load-bearing rows"); self-certified wiring the fold does not perform | runner :240-245 (selection rule), :362-366, :373 read this sitting; addendum 1.1 decodes |
| 6 | .zcode/workflows/mickey17-v2.dwf.ts:88 + :346-347 | slug formula pinned and manifest: write `{topic, targets: N, width, moment}` to runs/<slug>/manifest.json before the sweep; spec-addendum path per-slug (watch/inbox/ractor_engine/<date>-<slug>_ADDENDUM.md) | E22 fired-circularity (manifest makes the interface reconstructible); E33 master/addendum name drift per fork; the rolling-path overwrite that already ate the 10-03 SPEC filing | run dirs run-0 / 2026-10-04-0 / 2026-10-05-exec on disk; addendum header lines 10-15; CONVERGENT operations rows 2 and 5 |

Kill verdict (no sacred cows): CONCUR with the operations lens's fleet card - the-50,
tree-doctrine-dig, music-cut, the five game-dig veins, and wide-dig (merge into drop-dig) say
so themselves via SYNTHESIS.md:53 and 9 of 19 saved bodies with zero launches of current bytes;
nothing in my organ map contradicts those kills (no organ reads them). Addition: none of the
three mega-burn drafts should be saved as-is - they are one engine and parameterize into the
operations row-2 def; saving three copies banks the drift as permanent.

## Checks run this sitting (exact instruments)

1. Read in full: state/CURRENT.md; watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md;
   watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md; corpus/steal/MASTER_MICKEY17_V2.md;
   tools/mickey17_v2_fold.py (all 235 lines); .zcode/workflows/mickey17-v2.dwf.ts (380 lines);
   .zcode/workflows/ractor-engine.dwf.ts (352 lines);
   watch/inbox/ractor_engine/2026-10-05-ouroboros-r1-fleet/operations.md; economics.md (head).
2. bash: stat on fold tool + saved runner (mtypes 2026-09-25 19:21 / 2026-09-26 16:33);
   ls + cat of ~/.zcode/workspace/default/mickey17_v2/ (fold_run.sh bytes banked above);
   find . -name fold_run.sh (0 hits); ls .zcode/workflows (19 defs);
   ls memory/runs/mickey17_v2/runs/2026-10-05-exec/lanes (15 json files at my moment, of which
   7 .checks.json - in-flight count only, no decode); grep -c and grep -n over
   memory/attention.md (0 hits both batteries); grep -rn E_LEDGER over tools/*.py (no engine
   reader); ls tools/lawlog.py (exists, Oct 3); grep REGISTRY.jsonl readers in tools/+mag/
   (6 readers: gate_canary, visor, workflow_gate, worldline_compact, improve, seed_registry);
   registry tail read (fail_g8 fixture rows 2026-10-05T05:19/05:20Z present).
3. Not run: tools/mickey17_v2_fold.py (rewrites FOLD_SECTIONS.md in place - mutates audited
   evidence); no workflow fired; no pytest (no code changed by this seat).

## Blind spots (honest)

- Git history is unreachable from this seat: subprocess git resolves to an unborn branch
  'spore-main' with no commits (likely a sandbox spore overlay; .git/HEAD on disk names the real
  mag/run-beta1 branch). Commit-level claims (0c9d72a06's E1-E18 survival, a53b101d4's laws,
  139f5198f's ouroboros commit text) are carried from the addenda, SYNTHESIS, and the session
  git snapshot, not re-verified by git this sitting.
- Run 3 (execute-register) tier-2 persistence, the e12 fold edit, and the run's harness-side
  progress were not decoded by me; my run-3 bytes are one ls (15 files / 7 checks) and the
  operations decode is the deeper sitting.
- The 100M/60M token figures ride the operator order, not my measurement. ListWorkflowRuns was
  not attempted from this seat (the operations sibling already hit the capability block and I
  had no need beyond their finding).
- The percolator/LINKS non-ingestion is carried from run-0's own fold prose (N9/N10) and the
  read-estate addendum's code-14 census; I did not re-census the percolator's inputs myself.
- attention.md absence is scoped to that one file (full-file grep); other organs (queue/todo.md,
  LINKS.jsonl, research_polished) were not censused by me this sitting.
- Cross-lens convergence flags cite the two sibling files banked in this same folder at my read
  moment; the fold seat owns round-level dedupe.
