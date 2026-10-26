# STEAL CARD: evals-self-improvement via x (frontier_olm_adhoc) - rev 2

source-fetched: adhoc · seat: steal-evals-self-improvement-via-x · moment: 2026-10-11 · rev 2 (round-2 critique applied)
Inputs: 3 confirmed finds delivered by the round-1 and round-2 asks, all banked by the 2026-10-11
run-2 sweep (watch/inbox/frontier_olm_adhoc/sweep/evals-self-improvement-x.md:15 item 1
Self-Harness, :17 item 2 Rethinking Harness Evolution, :25 item 6 MemSkill; overlap verdicts at
:37). Source doc read in full this session (95 lines). External paper pages NOT re-fetched this
session: every quote below is verbatim from the sweep doc, re-grepped at its cited line this
session.

## Revision ledger (round-2 critique -> this rev)

1. FABRICATION-CLASS FIX (defect 1): round 1 presented the find's abstract-phrasing quote
   ('identifies model-specific failure patterns...'; 'generates diverse yet minimal harness
   modifications...') as if verbatim at sweep doc :15. Re-grep this session: neither phrase appears
   anywhere in the sweep doc; the sweep's own capture reads "Weakness Mining extracts
   model-specific failure patterns from execution traces, Harness Proposal ties minimal edits to
   those failures" (sweep :15, grep run this session). This rev quotes only sweep-verbatim text;
   the find's abstract phrasing is named as the find's, unattributed to the sweep doc.
2. PROBE RESPEC + RESULT FOLDED (defects 2-3): the round-1 flip join keyed on skill_id/job, but
   the 1,635 pending rows are decision.v1 rows whose key union is exactly schema/ts/goal/
   task_shape/provider/model/reasoning_level/seat/outcome/detail/source (measured this session;
   no skill_id, no job, not even content_hash) - the join could not execute as specified. Re-run
   this session goal-keyed (the only identity field): pending 1,635 rows span 19 distinct goals,
   consumed 144 rows span 1 distinct goal at this read (the reviewer's read minutes earlier
   found 2; the file is append-live, total drifted 11,075 -> 11,077 between rounds), overlap
   ZERO. No pending row EVER flips to consumed under the only available key: the falsifier is
   DEAD and the hard_moves/schema ports green-light. The round-1 population-level 8.1 pct framing
   is struck and replaced by the cohort answer: 0 pct.
3. SELF-CHARACTERIZATION CORRECTED (defect 4): round 1 called this "an already-gated run
   family". FALSE for this run: RECEIPT.md:34 states verbatim "This adhoc mine run (gate holder
   olm-mine:adhoc) has no gate-registered row of its own; DIGEST.md honest gap 3 classifies it as
   an incident, not registered debt". Family history IS gated: 15 REGISTRY rows across 4 script
   paths / 3 script names (frontier-olm-mine.dwf.ts 7, olm-mine-2.dwf.ts 3, olm-mine.dwf.ts 5 in
   two path spellings), verdicts 14 PASS + 1 STATUS-ROW, latest 2026-10-06T18:53:21Z - every one
   predating this run (the only REGISTRY rows since 10-10 are fill-ball 10-10 and
   mcp-landscape-wide-dig 10-11; counted this session). Round 1's probe-3 claim "15 rows, all
   frontier-olm-mine.dwf.ts PASS" was wrong on both counts and is corrected here. The 2026-10-11
   adhoc run that produced this card IS the incident class the port names.
4. PORT (a) DETECTION KEY RESPECIFIED (defect 5): keying the coverage check on
   directory-name-in-REGISTRY false-positives (gated family whose script name shares no token
   with its directory) and false-negates (stale PASS rows from months ago counting as coverage -
   the exact trap in fix 3). This rev keys the check on the family-to-script mapping (fold-gate
   holder id in the family RECEIPT, the run register, or the workflow journal) plus a recency
   window: a row counts as coverage only if its ts falls inside the family's artifact-landing
   window.
5. GATE CITES FIXED (defect 6): the REGISTRY append is tools/workflow_gate.py:738-751 (row built
   :739-746, appended :749-751; read this session). Round 1's ":53" is the FIRE-ledger docstring
   sentence (FIRE_LEDGER.jsonl, not REGISTRY) and ":474-475" is run_checks' internal check-row
   append - both mispointed for the REGISTRY claim. The index cite :485-494 stands.
6. Dir size noted current (defect 7, no action): 644 files / 51,460,052 bytes at this session's
   walk (RECEIPT.md's 281 / 15,027,763 was its moment; the reviewer's 644 / 51,460,100 theirs;
   the incident grew ~2.3x within the day, still zero REGISTRY rows naming it).

## The steal (three mechanisms, one discipline)

1. **Self-Harness (arXiv 2606.09498, v3 2026-08-20): harness edits must be weakness-driven and
   regression-gated.** Sweep-verbatim: "Weakness Mining extracts model-specific failure patterns
   from execution traces, Harness Proposal ties minimal edits to those failures", and Proposal
   Validation "accepts candidate edits only after regression testing" (sweep :15; both phrases
   re-grepped at that line this session). The discipline: an accepted edit is a triple (failure
   pattern mined from real traces, the minimal edit tied to it, the regression test that gated
   it). An edit without the triple is unproven - and in the sweep's own Q5 framing, "a run that
   lands artifacts but no REGISTRY row is, in this paper's terms, an edit accepted without
   Proposal Validation: unproven, unraatcheted, an incident" (sweep :15).
2. **Rethinking the Evaluation of Harness Evolution (arXiv 2607.12227, v2 2026-08-27): a harness
   claim must beat a budget-matched null on held-out work.** Verbatim: "automatic harness
   evolution does not consistently outperform simple test-time scaling baselines once the cost of
   searching for improved harnesses is accounted for" (sweep :17). Protocol demands: matched
   feedback and inference budgets, and held-out task evaluation, because search and final eval
   sharing one benchmark risks overfitting.
3. **MemSkill (arXiv 2602.02474, v2 2026-05-24): the skill bank evolves from its hard cases.**
   Verbatim: "a designer that periodically reviews hard cases where selected skills yield
   incorrect or incomplete memories, and evolves the skill set by proposing refinements and new
   skills" (sweep :25). Case-law coverage grows by logging where a skill produced wrong or
   incomplete results plus the evolution decision taken, not by logging successes.

The one-sentence steal: the estate's self-improvement records are win-biased and edit-biased
(they count accepted moves and successful case law; failures and unvalidated acceptances have no
consumer), and all three papers attack exactly that bias from three sides (gate the edit, race
the null, review the hard cases).

## What the estate already has (self-steal check, verified this session)

- **Proposal Validation exists for workflow scripts**: tools/workflow_gate.py appends one
  memory/workflows/REGISTRY.jsonl row per single-script check (row built and appended at
  tools/workflow_gate.py:738-751; registry index at :485-494). Live census run this session: 177
  rows, keys checks/digest/name/script/ts/verdict, verdict counter PASS 111 / STATUS-ROW 35 /
  FAIL 31, last rows mcp-landscape-wide-dig.dwf.ts PASS at 2026-10-11T02:07:34Z.
- **skill_ledger is real and already feeds the context pack**: mag/skill_ledger.py (decision
  rows at memory/improve/skill_ledger.jsonl, DECISIONS_PATH mag/skill_ledger.py:31; schema
  skill_ledger.decision.v1 at :151-166 with outcome + a 200-char detail at :161; B2-410 outcome
  registry at :46-53, no ghost dialect registered). proven_moves (:94-134) is its ONLY reader
  outside tests: consumed by the context pack L0d/L1c proven-moves layer (mag/context_pack.py:93,
  :890-899, :129, :1447, :1712-1716; mag/gene_pool_feeder.py:12 rides it). Grep this session
  found zero consumers of non-ok rows anywhere in mag/ tools/ main.py.
- **The null-arm law already exists in the cache lane**: G1 gap law, any "eviction/compaction
  claim must beat LRU/ARC/PBKV/Belady-MIN arms or it is decoration" (tools/lru_null_arm.py:3-5;
  the underlying clause verified at memory/research_polished/kv_cache_compaction.md:13 at this
  session's grep, with the file under active sibling edit today so its line numbers are volatile
  - the stable cite is the lru_null_arm docstring). Instrument pattern to copy: deterministic
  replay, claim threshold, HOLDS/FAILS with named consequences (tools/lru_null_arm.py:158-176).
- **The improve lane already carries prose hard cases**: memory/improve/candidates.jsonl row 1
  (schema improve_candidate.v1, read this session) records a rejected candidate with the
  resolution note "env bug not model bug" - exactly MemSkill's hard-case shape, but in a
  free-text note no machine consumes.
- **The percolator already runs a proposals-never-mutations review pass**: repeatables compile
  to invariants, novel signal queues for exploration (mag/percolator.py:8-27), and the
  --candidates path ingests frontier run candidates into memory/percolator/candidates.jsonl
  promoted=False (mag/percolator.py:23-27; the adhoc run's bridge file
  watch/inbox/frontier_olm_adhoc/percolator_candidates.jsonl read this session).

## Estate organ map (each find to the organ it feeds, concrete port move)

- **Self-Harness -> gopher fleet gate + context pack (skill_ledger).**
  (a) GATE SIDE (Q5): REGISTRY.jsonl is the estate's Proposal Validation ledger, but its rows
  key on script name/digest only, so a run family that lands artifacts under its own directory
  identity is invisible to it - and this run is the live instance, not a hypothetical:
  grep -c "adhoc" memory/workflows/REGISTRY.jsonl = 0 while watch/inbox/frontier_olm_adhoc/
  holds 644 files / 51,460,052 bytes (both measured this session), and RECEIPT.md:34 records
  that this run "has no gate-registered row of its own" and is classified "an incident, not
  registered debt". PORT MOVE (detection key respecified per fix 4): a run-family coverage check
  that resolves each family to its script(s) through the family-to-script mapping (fold-gate
  holder id in the family RECEIPT - here "olm-mine:adhoc" - the run register, or the workflow
  journal) and requires >=1 REGISTRY row for that script whose ts falls INSIDE the family's
  artifact-landing window; stale PASS rows from before the window do not count (the trap this
  run demonstrated: family rows exist, all predate the run, coverage was still zero). Families
  that fail the check are incidents, not debt.
  (b) LEDGER SIDE (Q2): record_decision has no failure-pattern field and no gating-test field
  (mag/skill_ledger.py:151-166; field audit this session: the 70 fail rows carry zero
  non-standard fields, detail mean 33.5 / max 87 chars). PORT MOVE: schema amendment adding
  failure_pattern (mined from the execution trace) and gated_by (the test/gate row that
  validated acceptance) to accepted-move rows, plus a stable job id so cohort joins are possible
  (see the probe result below: goal is today the only join key). The prose law already exists
  ("fix comments carry the receipt: cause + evidence", AGENTS.md Build discipline); the port
  makes it a byte field the pack can serve.
- **Rethinking Harness Evolution -> the routing/eval lane (L23), via the null-arm law the cache
  lane already holds (Q4).** The 36.3-pct-question-class vs 3.6-pct-family split (read this
  session at watch/inbox/frontier_olm_2026-10-03/lens/laws.md:29, sourcing
  memory/rib/RIB_ROUTING_CLASSES_20261002.md:11-16) routes dollars under law L23 (question-class
  first, watch/inbox/frontier_olm_2026-10-09/lens/laws.md:92-97) and awaits same-shape
  replication (Q11, same lens :290-292 - which demands replication, not yet a budget-matched
  test-time-scaling null; that is this port's delta). PORT MOVE: before the split routes more
  dollars, mint its test-time-scaling null arm - same budget spent on more/cheaper inference on
  the losing family instead of routing cleverness, scored on held-out asks the routing search
  never saw - using the lru_null_arm instrument shape (deterministic replay, claim threshold,
  HOLDS/FAILS consequence, tools/lru_null_arm.py:158-176). If routing does not beat the
  budget-matched null on held-out asks, L23 demotes from routing law to hypothesis, exactly as
  the paper's verdict says harness evolution fails to beat test-time scaling once search cost is
  accounted.
- **MemSkill -> percolator + context pack (the missing failure-review surface) (Q2).** Live gap
  measured this session: proven_moves is win-only by construction (min_count 3, min ok_rate 0.7,
  mag/skill_ledger.py:94-134; live call returned 12 entries, top = ops count 1077 ok_rate 0.93
  deepseek/flash), the ledger holds 11,077 rows of which 2,016 are non-ok, and the failure lane
  is starved and dialect-split: outcome='fail' is only 70 rows (0.6 pct) while the ghost seat
  writes 1,785 steer rows in an unregistered compound dialect ('deploy=deployed measure=pending'
  1,635, 'deploy=ok measure=consumed' 144, 'escalated' 127; all source='ghost'). The dialect is
  LIVE, not legacy: pending rows span 2026-08-08 through 2026-10-11T19:36:32Z (ts range read
  this session; rows landed while this card was being written). normalize_outcome passes unknown
  strings through unchanged (mag/skill_ledger.py:56-65) and the B2-410 registry's own feedback
  loop ("a consumer meeting one files it here", :42-44) never fired because no consumer ever met
  one. PORT MOVE: hard_moves(), the MemSkill designer pass - periodic deterministic
  bucket-review of non-ok rows by (source, task_shape, outcome), each bucket closed with an
  appended evolution decision (refine the skill / retire it / escalate to a rib), the ghost
  dialect registered into OUTCOME_REGISTRY or routed through the percolator (which already
  compiles repeatables and queues novel signal, mag/percolator.py:8-27), and the result served
  into the context pack beside proven_moves so the stateless agent sees both lanes.

## Probes RUN this session (receipts, exact commands and outputs; rev-2 battery)

1. Sweep verbatim re-grep: `grep -n "extracts model-specific|ties minimal edits|accepts
   candidate edits"` over the sweep doc -> all three phrases at line 15, confirming the
   round-1 misattribution and the rev-2 quotes.
2. Census + goal-keyed flip join + fail audit (one `.venv\Scripts\python.exe -X utf8` instrument
   over memory/improve/skill_ledger.jsonl, json.loads per line): total 11,077 rows (live drift
   +2 since round 1); non-ok 2,016; fail 70, zero non-standard fields, detail len mean 33.5 /
   max 87; pending 1,635 across 19 distinct goals; consumed 144 across 1 distinct goal at this
   read (reviewer's read the same day: 2; append-live file, both moments recorded); overlap
   ZERO - no pending row ever flips to consumed under the only available key. Pending row key
   union: exactly the decision.v1 fields minus content_hash (no skill_id, no job) - the round-1
   join key was unrunnable, the respec to goal is now the measured key. Pending ts range
   2026-08-08T00:54:59Z .. 2026-10-11T19:36:32Z (dialect live). FALSIFIER VERDICT: DEAD - the
   >=90-pct-measured branch is impossible (measured 0 pct), the structured-fail-field branch is
   false (zero non-standard fields); the hard_moves port, the ghost-dialect registration, and
   the failure_pattern/gated_by amendment all green-light.
3. proven_moves live: 12 entries, first {move: ops, count: 1077, ok_rate: 0.93, model: flash,
   provider: deepseek}.
4. REGISTRY census (same python instrument over memory/workflows/REGISTRY.jsonl): 177 rows,
   verdicts PASS 111 / STATUS-ROW 35 / FAIL 31; grep -c "adhoc" = 0; family drill (name or
   script matching frontier|adhoc|olm): 15 rows, 4 script paths / 3 script names
   (frontier-olm-mine.dwf.ts 7, olm-mine-2.dwf.ts 3, olm-mine.dwf.ts 5 across two path
   spellings), verdicts 14 PASS + 1 STATUS-ROW, max family ts 2026-10-06T18:53:21Z; the only
   rows since 2026-10-10 are fill-ball (10-10, mixed PASS/FAIL) and mcp-landscape-wide-dig
   (10-11, PASS x3). Corroboration read this session: RECEIPT.md:32-34 ("Workflow gate row
   pointer: NOT FOUND for this run").
5. Consumer grep: `grep -rn "proven_moves|best_moves"` over mag/ tools/ main.py -> only
   mag/context_pack.py consumption sites plus mag/gene_pool_feeder.py:12; no reader of non-ok
   outcomes exists.
6. Re-bank greps (this session): `grep -c "2606.09498|2607.12227|2602.02474|Self-Harness|
   MemSkill"` -> catalog/catalog.jsonl 0, CORPUS_CATALOG.md 0; `grep -rl` over memory/rib/ and
   corpus/steal/ -> no files. None of the three steals is re-banked work.
7. Gate cite reads: tools/workflow_gate.py:738-751 (REGISTRY row build + append) and :753-757
   (fire-ledger block, confirming round 1's ":53" pointed at the FIRE-ledger docstring
   sentence); kv_cache_compaction.md G1 clause found at :13 by grep this session, file under
   active sibling edit today, line numbers volatile.
8. Dir walk: os.walk over watch/inbox/frontier_olm_adhoc -> 644 files, 51,460,052 bytes.
9. Instrument interference, carried from round 1: one Bash call (sed print of mag sources) was
   refused by the Mimosa PreToolUse hook as a suspected direct source write; the reads were
   redone with the dedicated Read tool, which is what the citations rest on.

## The falsifiable probe for this week (new, replaces the dead one)

Mapping-keyed run-family coverage census ($0, deterministic, minutes to an hour): enumerate
every top-level watch/inbox run family with artifacts modified in the last 14 days; for each,
resolve its script(s) through the family-to-script mapping (fold-gate holder id in the family's
RECEIPT - the adhoc pattern "olm-mine:adhoc" - the run register, or the workflow journal), then
require >=1 REGISTRY row for that script with ts inside the family's artifact-landing window.
FALSIFIER: if every artifact-landing family maps to a same-window row, the incident class has
exactly one member (this adhoc run) and the port shrinks to registering it plus a one-line
fold-gate check; if two or more unmapped families surface, the nightly census port is justified
at fleet scale. Decisive either way, and it tests the respecified detection key (mapping +
recency) rather than the round-1 name grep that this run itself would have gamed.

## OWED (never asserted as done)

- The three arXiv pages were NOT fetched this seat; quotes are the sweep seat's verbatim
  captures (sweep doc :15 :17 :25), re-grepped at their lines this session.
- The 21,852-file overlap scan (MISS verdicts) is the sweep seat's instrument run (sweep doc
  :37), delivered with the ask; this seat ran the bounded re-bank greps (probe 6) instead.
- hard_moves(), the mapping-keyed coverage check, the failure_pattern/gated_by + stable-job-id
  schema amendment, the ghost-dialect registration, and the test-time-scaling null arm are
  DESIGNED here, not implemented or run.
- The new coverage-census probe is specified, not run; the dead flip-join probe WAS run (probe
  2) and its verdict is folded into the organ map.
- The 36.3-vs-3.6 split was read at the 10-03 lens line citing RIB_ROUTING_CLASSES_20261002.md;
  the rib file itself was not opened this session (lens line is the citation of record here).
- No REGISTRY row was written by this seat: per RECEIPT.md:34 the run has none, this card
  cannot self-certify one, and closing that gap is the port's job, not the steal seat's.
