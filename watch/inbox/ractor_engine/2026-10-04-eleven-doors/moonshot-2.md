# MOONSHOT-2 - the 11 build doors, self-steal census and hostile pass (2026-10-04)

Writer: moonshot-2 lens, dwfrun session, 2026-10-04 ~12:40 local. Every check below was
run or read THIS session; nothing is carried forward unmarked. No em-dashes.

## 0. Live-state bombshell: doors 1-3 of the sequence are already landed or cured

The sequence I was handed is stale on its first three items, and one door landed WHILE
this lens ran:

- Door 1 (independent-cop): LANDED, commit bb0f34586 (git log; receipt
  watch/inbox/GWAP_INDEPENDENT_COP_20261004.md read in full). Known.
- Door 2 (arena-bench tripwire): LANDED MID-ANALYSIS by a sibling seat. At ~12:15 my
  file census read tests/test_arena_bench.py MISSING; at 12:35 it exists (4020 bytes,
  mtime Oct 4 12:35) under commit 00cb15c77 "ARENA BENCH TRIPWIRE (door 2)". That
  commit also names the real root cause the 24-wide receipt missed: dashboard/static/
  arrakis.html has been a 459-byte redirect stub since the 09-22 surfaces dedupe
  (canonical at games/arrakis.html), so the bench was parsing a stub and "raising
  honestly into the void for 12 days with zero tests listening". My own runs agree
  with the post-fix state: `.venv/Scripts/python.exe mag/arena_bench.py --selftest`
  exits 0 (verdict FAIL on synthetic split, correct), and
  `load_ground_truth()` returns GT-OK keys gates/gate_count/blind_name/crown_number/
  ghost_name. My `grep -c "name:'" dashboard/static/arrakis.html` returning 0 was the
  stub, not a dead parse.
- Door 3 (night-cycle checkpoint legs): the 5x re-run defect class was CURED in the
  04:00 night shift, commit 9718e812d (git log: "_save_state O_TRUNC through the bind
  mount lost completed-work records (5 CYCLE_FAILs 10-03, ~100s re-run loops). Cure:
  ... trail-before-persist, atomic tmp+os.replace state save"). I ran
  `.venv/Scripts/python.exe -m pytest tests/test_night_march_cure_20261004.py -q`:
  6 passed in 1.93s (the commit message says 7 tests; instrument and moment named,
  6 is what runs now). mag/lane_runner.py:932-936 now carries the cure's comment where
  the primer cited the harm. Residual: per-leg done flags do not exist, but the
  once-per-night guard (mag/lane_runner.py:919-920) plus an idempotent monitor make
  re-run cost near zero. The door as specced (2-4h) targets a cured defect.

Consequence: the real work is doors 4-13 plus one generalization the landed door 2
points at (finding 2 below).

## 1. FINDING: the decay-family "define the vocabulary once" is already defined, five dialects deep

The 24-wide cross-cluster ruling says: define decay/supersession ONCE, then
instantiate per store. Hostile pass: the estate does not lack the vocabulary, it
lacks the discipline; the vocabulary exists and is already instantiated five-plus
times. Unscoped `git grep -n -i -E "decay|evaporat" -- mag tools` (run this session,
tracked tree only) returns working decay laws in:

- mag/percolator.py:172-183 (half-life decay, whole UTC cycles, floor 1, decay_as_of
  baseline; law 1 / Z15)
- mag/mycelium.py:265-277 (decay() stamps decayed + decayed_at, log-only)
- mag/memory_consolidate.py:47-48, 127-130 (Generative-Agents 0.995/hour exponential
  recency decay inside a multi-signal fusion scorer)
- mag/signals.py:82-87 (recency_decay with half-lives at :37-38)
- mag/ladder.py:72 (24h decay), mag/gene_pool_feeder.py:241-261 (bonus decays to a
  floor, never zero)
- supersession: mag/republic.py:397-414 is a COMPLETE enforced supersede law
  ("the old letter STAYS, points superseded_by"; set once, never edited, invariant
  checks at :209-217, forward-on-superseded at :376-379)

The primer's "greps for decay over river/swarm_tools/ledger return zero" was scoped
to exactly those three files (it says so). The universal-sounding "all memory, no
metabolism" verdict is false at estate scale; it is true only for the GPS ledger and
river. QUANTIFIER LAW catch: the decay-family doors are ports of existing law, not
new vocabulary.

Move (one sitting, ~3h): port percolator's `_decay_count` into tools/gps_mcp/ledger.py
(the port pattern already exists read-only at tools/concept_span_check.py:122-124,
"mag/percolator.py _decay_count, re-implemented read-only"), and adopt
mag/republic.py's superseded_by field law into mag/mycelium.py contradict()
(:188-198 currently bumps counters with no lineage; read this session). Falsifier:
if republic's supersede law cannot lift without its book container, or ledger rows
lack a per-row last_measured/updated_at to key decay on (they have both: the running
mean UPDATE at tools/gps_mcp/ledger.py near :425-441 writes last_measured, updated_at),
the port is bigger than 3h and should stop at the ledger half.

## 2. FINDING: door 2's class cure is the SWEEP, not the tripwire (and the class is measured now)

The estate carries a `--selftest` convention across 25+ organs:
`git grep -l "selftest" -- mag tools` returns mag/arena_bench.py, mag/cite_gate.py,
mag/diary.py, mag/engram.py, mag/falsifier_counter.py, mag/governor.py,
mag/lane_breaker.py, mag/lane_effort.py, mag/pigeonhole.py, mag/preload_selector.py,
mag/probe_route.py, mag/seed_percolator.py, mag/switchboard.py,
tools/census_drift_patrol.py, tools/census_patrol_selftest.py, tools/citation_lint.py,
tools/duty_fuzz.py, tools/mcp_pin.py, tools/oracle_calibration.py,
tools/pointer_rot_check.py, tools/prepush_paths_changed.py, tools/quota_ledger.py,
tools/quota_ledger_report.py, tools/transport_precheck.py, tools/wandr_selfeval.py.
Tests reference selftest per-organ (tests/test_arena_bench.py, tests/test_citation_lint.py,
tests/test_census_drift_patrol.py, tests/test_lane_effort.py, tests/test_wave_driver.py,
tests/wave_driver_test.py, tests/selftests/ack_reaper_selftest.py,
tests/selftests/lesson_gate_selftest.py, tests/test_ack_reaper.py, tests/test_lesson_gate.py:
`git grep -ln "selftest" -- tests`), but NO test parametrizes over the whole entrypoint
set; nothing swept them, which is exactly why arena_bench raised honestly into the
void for 12 days (00cb15c77's own words). The landed tripwire cures one organ and
leaves 24+ siblings one stub-dedupe away from the same silent death.

Move (1-2h): tests/test_selftest_sweep.py, parametrized over the selftest entrypoint
list (pytest.mark.parametrize over (module, argv) pairs), skip-listing network/slow
organs by name, one golden row asserting every mag/tools organ that greps for
"--selftest" appears in the sweep (so a new organ fails the sweep until registered:
the census-carrier shape law applied to tests). Same cost as the single tripwire,
25x the guard. Falsifier: if more than a handful of the 25 entrypoints are
slow (>60s) or network-bound, the sweep degrades to a nightly job instead of
pre-push; measure before landing (I did not time each organ; OWED).

## 3. FINDING: the build-once calibrator's model is cargo; the estate already owns the starved calibrator

Door as specced: download Gero-4B, use it as calibration flag + truthful-revelation
layer, 4-8h with a download-and-eval gate. Hostile pass against the estate:

- tools/oracle_calibration.py IS the calibrator: docstring and code read this session;
  it implements calibration-set reliability with ECE/MCE/Brier (:14-16), temperature
  fitting on a calibration split (:17-19), per-domain drift flags (:20-22), and
  per-decision-class thresholds with escalated share (:23-27), stdlib-only, with an
  --input JSONL mode whose row shape is {"confidence", "correct", "decision_class"}
  (:35-37). Its own line :29 says "No live oracle confidence ledger exists on disk
  yet" and that line is STALE: tools/gps_mcp/router.py records a confidence field on
  every append-only ask receipt (docstring :18; row write :140; receipts default
  tools/gps_mcp/receipts.jsonl at :856).
- The proper-scoring steal from watch/inbox/X_INTEL_PROPER_SCORING_20261004.md is the
  RULE, not the model: score judges by log P of the outcome verification confirms
  (:50-59, read this session). Gero-4B's own card admits no published evals (:45) at
  50 downloads (:32). A log-score/Brier over banked outcomes is pure math on rows the
  estate already banks (gwap verdicts join router/MoA rows by model+shape); the
  learned scorer is an upgrade LATER, after the rule exists.
- Shapley/second-price prior art: `git grep -n -i -E "shapley|second.price" -- mag tools`
  returns zero hits (tracked mag+tools only, this session). Greenfield, but pure code
  on hermes_burn asks; no model required.

Move (2h): an adapter that dumps {confidence, correct, decision_class} rows from
router ask receipts joined to gwap verdicts into `oracle_calibration --input`, bank
the reliability table, and let the per-domain drift flag be the monoculture signal's
judge-side twin. Falsifier (check first, 15 min): if receipt rows carry no joinable
outcome key per row (confidence without a correctness verdict to bind to), the wire
needs a writer change first and the door reverts to the 4-8h estimate.

## 4. FINDING: the handed sequence fails its own hostile pass on ordering and gates

- EG-20 pass@K (rank 3 in the receipt's order, the ONLY measured-effort door, 2h,
  success meter defined at watch/inbox/ESTATE_GAP_DIG_20261004.md:79: "column
  present; predicts the mesh vs frontier routing on one batch") is DROPPED from the
  11-door list I was handed. `git grep -n "pass@K\|pass_at_k" -- tools mag tests`
  returns zero hits as of this session, so it has not landed; the sibling door-2
  commit message says "the pass@K diagnostic rides it", so a sibling intends it.
  Re-insert it; measured 2h with a defined meter beats every estimated door.
- The WELD DOOR is still listed design-gated on "needs the cop fix"; the cop fix
  landed (bb0f34586). Ungated as of now. Its build surface is real: beat_map damage
  rows have zero consumers outside tests (`git grep -n "beat_map" -- mag tools tests`
  hits only tests/test_beat_map_v02.py), so the ractive is genuine new surface, not a
  rebuild. Sequence it after the cheap wires, not never.
- Door 3 (night-cycle) should be struck or shrunk to the 30-min verify (section 0).

## 5. FINDING: consume-the-ledger's premise is half-false, and three-signal must run its own falsifier before any build

- Consume-the-ledger claims "nothing consumes the ledger at decision time". False at
  the routing layer: tools/gps_mcp/router.py rule (b) is "measured pass-rate from the
  ledger" applied on every ask (:5-7 docstring, read this session). The true residue
  is the flock field: mag/flock_field.py steer() (:158-170, read this session) is
  gradient + separation + alignment + cohesion with NO ledger/social term, and the
  runner has no claims section. Re-scope the door to "flock g_best term + runner_state
  claims"; the 1-2 day sizing is honest for that half but the door's headline claim
  must be corrected first or it will be "landed" by a wire that changes nothing the
  router does not already do.
- Three-signal query broker: the estate ALREADY holds a multi-signal fusion scorer
  (mag/memory_consolidate.py:127-130: a*recency + b*importance + g*relevance) and both
  live signals (FTS BM25 via corpus_search; lattice via mag/lattice_query.py). The
  door's own falsifier (recall@5 must beat BM25-only by 10pts; any network/external-DB
  dependency kills it) can run as a 30-minute two-signal check over 50 held-out estate
  questions BEFORE any embedding lane is chosen. Until that check runs, the embedding
  lane is cargo (new dependency class for a third signal nobody has shown is needed).
  Prerequisite the receipt itself names: the FTS body-excerpt column, else the
  BM25-only baseline is a path/title baseline and the falsifier is rigged.
- MCP-lattice shim: mag/mcp_server.py is a tool-map server (_READ_TOOLS at :144-157,
  read this session: corpus_search et al. are exposed; lattice_query and
  build_context_pack are NOT). The self-steal is adding two read-tool entries plus a
  token_budget param on the pack builder, 1-2h. The agentmemory grammar reconciliation
  gate is cargo: adopting a foreign API shape has no falsifier that matters when the
  estate's own server already provides the function; the PULL OVER DUMP law
  (watch/inbox/model_garden/MCP_LATTICE_SPEC_SEED.md:36-37 per the primer) argues for
  serving the estate's own computed pulls.
- Clippy-as-prober: no memory/retrieval dir exists and `git grep -rn -i "fsrs" -- mag
  tools .agents main.py` returns zero hits (this session), so FSRS state is greenfield,
  but minting a SIXTH decay dialect (see finding 1) is the disease wearing a door
  costume. The probes should write percolator observations (an organ with tested decay
  law, floor 1, and an existing consumer in tools/concept_span_check.py); the estate
  also already holds a probability-emitting predictor organ (tests/test_concept_predictor.py,
  named at watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:75-77). FSRS graduates off
  defaults at ~1k probes either way; store them where decay already lives.

## The honest build order by EV-per-hour (my ranking, replacing the handed one)

1. Selftest sweep (finding 2), 1-2h, guards 25+ organs forever.
2. EG-20 pass@K, 2h MEASURED, if the sibling's ride-along has not landed it by the
   time a seat picks this up (grep first).
3. Oracle-calibration wire (finding 3), 2h.
4. Clippy probes into percolator, 2h.
5. Monoculture proxy as a MoA-convergence join over lane trails + attention.md alert,
   1-2h (convergence and dissent_preserved already computed per synthesis:
   mag/mixture_of_agents.py:74-75, :90-91).
6. Ledger decay port (finding 1), 2-4h.
7. Mycelium supersession adoption (finding 1), 2-4h.
8. MCP two-tool wire, 1-2h.
9. Weld door, 1-2 days, UNGATED since bb0f34586.
10. Three-signal falsifier-first, 30 min, then decide the embedding lane.
11. Consume-the-ledger flock term + runner claims, 1-2 days, stays design-gated for
    the semantics change.

## Cargo list (what to cut, with the replacement)

- Gero-4B download: replaced by the oracle_calibration wire (finding 3).
- agentmemory grammar reconciliation: replaced by the two read-tool entries on the
  estate's own live server.
- A new FSRS store (memory/retrieval/state.json): replaced by percolator observations.
- The embedding lane, pre-falsifier: replaced by the 30-minute two-signal check.
- Per-leg checkpoint flags: the class was cured by 9718e812d; verify, do not rebuild.
- "Define the decay/supersession vocabulary once": already defined; port, do not mint.

## Blind spots (honest)

- I did not execute each of the 25 selftest entrypoints or time them; the sweep's
  pre-push suitability is asserted from the convention, not measured. OWED.
- Sibling seats are landing doors concurrently (door 2 landed at 12:35 mid-analysis);
  every live-state claim here is moment-stamped and may be stale within hours.
- I did not build the 50-question held-out set or run the recall@5 falsifier; that is
  the move, not a check I performed.
- The Shapley/second-price zero-hit grep covered tracked mag/ + tools/ only; corpus/
  and watch/ prose may hold design notes outside that scope.
- I read the Gero-4B card claims via watch/inbox/X_INTEL_PROPER_SCORING_20261004.md
  (32-46, 50-59, 75-77), not the huggingface card itself.
- mag/arena_bench.py's own docstring at :71 says "tests/test_arena_bench.py runs
  --selftest + this parse at pre-push"; the sibling's landing satisfies it; I did not
  read the landed test's body, only confirmed existence, size, and commit.

## ERRATUM (hostile second pass, 2026-10-04): finding 3's starvation story and 2h move are REFUTED; corrected finding below

The pass verdicted finding 3 weakened. I re-ran the census myself this session:

- tools/gps_mcp/receipts.jsonl read in full: 11 rows. Confidence is non-null on exactly
  rows 2-5 (all "confidence": 0.92, all ts 2026-09-30T23:08:42, four task shapes,
  exploration routes to fixture model ids yesno-tiny/scut-2b/gemma-worker-4b/
  flash-mid-1/flash-mid-2/frontier-opus). ZERO rows carry any correct/verdict/outcome
  field; "decision" holds "duel-route", a routing choice. Last write 2026-09-30. So
  "router began recording confidence on every ask receipt" is withdrawn: the ledger
  holds 4 fixture-shaped confidence rows from one moment and nothing joinable.
- Writer hunt (this session): tools/model_bakeoff.py grades hard correctness
  (correct_1976 at :95, tallied :132-136) with NO confidence field (grep confidence
  over the file: zero hits); mag/improve.py:2013-2078 pairs verdict + stated
  confidence in one row but binds no later outcome; mag/lane_runner.py:278-302
  (gate_verdict_v2) validates score + confidence + evidence_quote per axis at write
  time, but no observed-correctness binding exists either.
- What SURVIVES (pass-confirmed): the calibrator organ is owned and complete
  (tools/oracle_calibration.py:13-39, :120-174, stdlib :39, --input mode :35-37), and
  Gero-4B stays cargo: the pass primary-verified the HF card by fetch, matching
  X_INTEL_PROPER_SCORING_20261004.md:32-46 (no published evals, Qwen3-4B base, no LM
  head, proper-scoring RL).

CORRECTED FINDING 3: the build-once calibrator door is not starving on a stale note,
it is UNFEEDABLE by any after-the-fact join: no estate organ currently binds a stated
confidence to an observed correctness at write time. The honest move is writer
instrumentation, not an adapter: pick the organ where hard correctness is already
graded (tools/model_bakeoff.py's correct_1976) or where stated confidence is already
validated (gate_verdict_v2 axes, mag/lane_runner.py:286-294), and emit
{confidence, correct, decision_class} rows to a sidecar file oracle_calibration
--input reads (sidecar avoids touching the gate_verdict_v2 schema). That is 1-2h of
work whose VALUE is deferred by the accrual window (the calibrator needs a pile of
graded rows before ECE means anything), so in the honest EV-per-hour order this door
drops below every same-day-paying wire: start the accrual clock now, run the
calibration later. Tightened falsifier: after 50 accrued rows, if the confidence
values are constants or single-valued (the 0.92 fixture shape), there is no
calibration signal to measure and the door stays dead until a real confidence-emitting
organ exists; kill at that point rather than grading noise.

## Instrument log (what this lens ran)

Erratum-pass additions: Read tools/gps_mcp/receipts.jsonl in full (11 rows, census in
the erratum); grep confidence over tools/model_bakeoff.py (zero hits) and
mag/improve.py (:2013-2078); grep '"confidence"' and '"correct"' writer lists over
tracked mag + tools; Read mag/lane_runner.py:278-302 (gate_verdict_v2 axis validation).

git grep selftest/decay/embedding/superseded_by/shapley/pass@K/beat_map/estate_query
scopes named inline; ls/file-census loops; .venv/Scripts/python.exe
mag/arena_bench.py --selftest (exit 0, verdict FAIL synthetic);
load_ground_truth() import run (GT-OK); pytest tests/test_night_march_cure_20261004.py
-q (6 passed); reads of state/CURRENT.md, PRIMER_ADJACENT_24WIDE_20261004.md (full),
GWAP_INDEPENDENT_COP_20261004.md (full), mag/arena_bench.py:80-119,
mag/lane_runner.py:905-949, mag/mcp_server.py:140-175, mag/flock_field.py:140-179,
mag/mycelium.py:183-202, tools/estate_query.py:1-55, tools/oracle_calibration.py:1-40,
tools/gps_mcp/router.py:1-30, watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:28-77,
ESTATE_GAP_DIG_20261004.md greps; git log for arena_bench.py, arrakis.html,
tests/test_arena_bench.py, night-march.
