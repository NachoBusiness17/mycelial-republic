# break-logic: hostile second pass on logic.md (2026-10-06, stockfish-coding run)

Byte-check of every evidence cite in logic.md's four findings, re-running each named check
where cheap, plus a counter-evidence hunt. Instruments are named per the quantifier law;
absence claims below carry their own scope. No em-dashes.

## Instruments run this pass (each with its scope)

1. Read end-to-end: `mag/selfplay_orchestrator.py` (317 lines), `mag/llama_cpp_bridge.py`
   (274 lines), `tests/test_selfplay_orchestrator.py` (199 lines),
   `memory/steal/STEAL_STOCHASTIC_DETERMINISTIC_20260814.md`,
   `memory/runs/selfplay/evidence_latest.json`,
   `memory/corpus/quantized_thought/compile_report.json`,
   `watch/inbox/MIRA_METAREASONING_20261006.md`,
   `watch/inbox/QUEEN_CHESS_LM_20261006.md`,
   `memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/d13_selfplay_run_probe.py` (168 lines).
2. Read ranged: `tools/gps_mcp/coverage.py:30-44,188-244`, `tools/workflow_gate.py:1-18,612-633`,
   `mag/effect_broker.py:300-334`, `tools/dungeon.py:1-15`,
   `watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md:106-123`,
   `watch/inbox/ractor_engine/2026-10-06-stockfish-coding/{operations.md,economics.md,break-economics.md,accuracy.md,break-accuracy.md}` (grep-anchored, then read at the anchors).
3. `wc -l memory/runs/trajectory/steps.jsonl` -> 109 (reproduces the lens).
4. `find . -name "steps.jsonl" -not -path "./.git/*"` + wc on every hit -> 30 files: the 109-row
   production file, pytest-tmp fixtures (60300 and 64652), and `memory/trajectory/steps.jsonl`
   at 65,151 lines. This last file is the counter-evidence that kills F3.
5. Tolerant python census of `memory/trajectory/steps.jsonl`: 65,225 lines, 65,151 valid
   `trajectory_step.v1` rows, 74 unparseable, 2,995 sessions, first ts 2026-09-05T17:07:17Z,
   last ts 2026-10-07T00:50:33Z (live at census moment).
6. Scoped greps (re-running the lens's own): `grep -ril gladiator memory/rib memory/law memory/game docs`
   -> rc=1 (zero); `grep -rnE "won.?bout|won_bout" memory/rib memory/law` -> rc=1;
   `grep -ril magnetic memory/rib memory/game` -> `memory/rib/RIB_MOSAIC_SEED_20260921.md` only.
   All three reproduce the lens exactly. A repo-wide recursive grep was launched and stopped
   before completing; no repo-wide absence claim is made from it.
7. `grep -rln --include="*.md" "won bout|won_bout" watch/inbox memory` -> only
   `watch/inbox/QUEEN_CHESS_LM_20261006.md` and 7 sibling files under
   `watch/inbox/ractor_engine/2026-10-06-stockfish-coding/`. The phrase is receipt-of-today-only.
8. Pack census: `grep -icE "queen|mira|alodlm|token.?cue"` and
   `grep -cE "2610\.02525|2610\.04198|2610\.06851|2610\.03695"` over
   `memory/corpus/quantized_thought/instructions_{flash,frontier,local}.jsonl` -> zero on both,
   all three packs. `grep -icE "queen|mira|alodlm|2610\." memory/percolator/invariants.json`
   -> zero; file mtime Oct 6 19:00 (after the 18:26:38Z compile stamp).
9. Scorer-death probe (in-process; NOT the lens's named falsifier):
   `.venv/Scripts/python.exe -c` importing `mag.selfplay_orchestrator`, monkeypatching
   `mag.lane_runner.flash_call` to raise RuntimeError, then `play_one(MATH_PROBLEMS[0])`
   with the default bridge. Output verbatim:
   `result reward= 0.5 correct= False` / `scorer sample ok= True detail= ''` / `elo= 984.0`.
10. Python census of the 109-row file: 84/109 rows carry `tool_result.exit_code`.
11. `git log --oneline` on both steps.jsonl paths -> empty for both (untracked/ignored);
    no git history exists to check. Stated as not available, not as checked-and-clean.

## Verdicts

### F1 (reward leg has no adjudicator; scorer failures die into silent neutral 0.5) - CONFIRMED, upgraded to behavior-observed

Every cite byte-real: `mag/selfplay_orchestrator.py:164-170` (except branch into
`_fallback_score`; `:170` appends `BottleneckSample(leg="scorer", ms=scorer_ms, ok=True)`
with ok hardcoded), `:248-251` (`_fallback_score` returns "0.5"), `:179`
(`self.elo.update(reward if correct else 0.0)` verbatim), `:283-304` (main()'s evidence dict
omits the samples list). `tools/gps_mcp/coverage.py:37-40` (`MIN_PROBLEMS_FLOOR = 10` with the
thin-air-is-fabrication comment), `:207` (`margin: float = 0.05`), `:214-241` (the trivalent
verdict). `memory/runs/selfplay/evidence_latest.json` byte-exact: 8 games, 5 correct,
Elo 1033.1. My probe (instrument 9) makes it behavioral: a dead scorer records reward 0.5 into
the artifact, reports `ok=True` with empty detail, and no counter exists.

Two precision strikes, neither fatal:
- "Every scorer failure flows into the Elo update as half-credit" is wrong for one branch. Elo
  half-credit (0.5) applies only on games the deterministic ground-truth check flags correct; on
  incorrect games the Elo leg takes a full loss (probe: 984.0 = 1000 + 32*(0.0 - 0.5)) while the
  reward column still shows 0.5 and the sample still says ok=True. That is worse than the lens
  stated: two instruments disagree inside one artifact row with no adjudicator flag.
- The banked d13 run's scorer was fully alive (instrument: `d13_selfplay_evidence.json`
  usage_rows = 8, all openrouter/auto; all rewards in evidence_latest.json are 0.0 or 1.0), so
  the defect is latent in the banked numbers, not their cause. The lens did not claim
  contamination, but the record should hold it: nothing in the banked evidence exercises this path.
The lens's named kill check (unset OPENROUTER_API_KEY, re-run the probe) remains NOT RUN; my
monkeypatch probe is a narrower in-process substitute and is reported as such.

### F2 (spawned-but-never-queried server; in-process Llama per move; "actor dominates" is a wiring artifact) - CONFIRMED

All cites byte-real on an end-to-end read: `mag/llama_cpp_bridge.py:129` (endpoint string
returned), `:132-148` (`_wait_ready` is the only urllib use in the file; import at `:21`,
urlopen at `:143`), `:152-196` (`generate_move`), `:171-176` (fresh in-process `Llama(...)`
constructed per call). No HTTP generation call exists anywhere in the file. Scope of the
"no client" claim, re-run: `grep -rln "spawn_server" --include="*.py" mag tools tests` ->
only the bridge itself and `tests/test_selfplay_orchestrator.py`; nothing consumes the endpoint
string. CONVERGENT verified: operations.md:11 (F1 spawned-but-never-queried) and :17 (F2 reward
leg cannot report its own death) are the same shape, independently derived.
Banked consistency: evidence_latest.json shows real model text per problem ("5! = 120."),
avg_actor_ms 3472.6 vs avg_scorer_ms 2966.9, bottleneck "actor". Provenance pinned (the lens
left this open): `d13_selfplay_run_probe.py:101-103` spawns the server, its docstring `:7-8`
states "generate_move then runs real in-process inference", spawn_meta in
`d13_selfplay_evidence.json` shows `ok: true, pid 15036, endpoint http://127.0.0.1:8081/completion`,
and `:135-153` shows the probe (not main()) writes evidence_latest.json. The banked "actor
dominates" verdict is therefore the per-move model-load cost on a CPU gemma2 stand-in
(probe deviations documented at `:9-17`), not a property of the landed lane profile. The lens's
falsifier (route generate_move through the endpoint, re-run) remains NOT RUN and is still the
right kill test.

### F3 (MIRA receipt prices the forecaster on a 340x phantom steps.jsonl denominator) - KILLED

The cites were real (MIRA_METAREASONING_20261006.md:21 verbatim, wc -l 109 reproduced), and the
lens's own falsifier was "any steps.jsonl or joined equivalent carrying a five-digit row count".
The falsifier fires: `memory/trajectory/steps.jsonl` holds 65,151 valid `trajectory_step.v1`
rows (65,225 lines, 74 unparseable), 2,995 sessions, first ts 2026-09-05T17:07:17Z, last ts
2026-10-07T00:50:33Z (instrument 5). The corpus the receipt gestures at is real, live, and
within about 1.8x of the claimed count, not 340x phantom. The estate already carries the
erratum: `watch/inbox/READ_ESTATE_RUN_SPEC_ADDENDUM.md:114` names the genre:
"r01 ('~37k rows' inherited from AE5, live stream read 55,571+)". The INSUFFICIENT-floor clause
was doubly wrong: 84 of the 109 production rows carry `tool_result.exit_code` (above the floor
of 10 even on the small file), and coverage.py's floor is a routing-verdict instrument, not a
training-set floor. The 340x arithmetic (37,000/109 = 339.4) was correct arithmetic on a wrong
denominator choice. Residual kernel, real but small: the receipt's bare "steps.jsonl" is
ambiguous between the 109-row production file at `memory/runs/trajectory/` and the 65k-row live
spine at `memory/trajectory/`, and the count is stale; amend the receipt with the absolute path
and a fresh wc (5 min), do not "gate the forecaster ask" on a phantom. Convergence note: the
economics lens and its breaker hit the same 109 (break-economics.md:30-35) and that break's own
repo-wide find (break-economics.md:31) also missed `memory/trajectory/steps.jsonl`; two
instruments converged on the same incomplete census.

### F4 (prior-art rows phantom-named; four-paper stack absent from quantized packs) - WEAKENED

Pack half CONFIRMED and hardened: zero matches for queen/mira/alodlm/token-cue AND zero for the
four arXiv ids across all three packs (instrument 8); compile stamp byte-real
(compile_report.json:2 = 2026-10-06T18:26:38.318229+00:00, kept 625 at :9, flash pack 12 at
:17). Hardened further by A2 below: the quantizer's input also carries zero rows, so the lens's
"rerun the sanctioned quantizer compile" move is a no-op until rows are filed upstream.
Phantom half mostly dies:
- Magnetic-field doctrine: full card at
  `memory/steal/STEAL_STOCHASTIC_DETERMINISTIC_20260814.md:14` ("magnetic microbots, not
  individually commanded"), `:34` ("field is law, nodes look stochastic"), `:61` ("Magnetic
  swarm stays a view over flock_field. No new physics."), dated 2026-08-14. The lens's
  four-directory scope (memory/rib, memory/law, memory/game, docs) excluded memory/steal; its
  scoped absence is true as written and its "phantom-named" conclusion is false at estate level.
- Gladiator: carrier docstring `tools/dungeon.py:5-11` ("gladiatorial combat in D&D
  environments - bouts over real problems"; dice law "the roll is committed BEFORE the actor
  speaks, and the actor never sees it"); the 10-03 spec `watch/inbox/hermes_burn/DND_module.md`
  exists (23,448 B, mtime Oct 3 07:59) but carries no bouts/stakes phrasing (my grep over it
  matched only "about" substrings); the exact phrase "won bout" exists only in the QUEEN receipt
  (:23, :30) and the day's sibling lens files (instrument 7). Name-only, substance distributed:
  "phantom" overstates, the accuracy break's ruling (break-accuracy.md:36,45) stands and
  logic.md did not consult it.
The lens's three scoped greps themselves reproduce byte-true (instrument 6). The true residual
is narrower and matches A2: the door's law and prior art are not in the boot-loaded
rib/invariants/pack path, which is a propagation gap, not a phantom.

## Additions (what logic.md missed)

### A1. The steps.jsonl census was incomplete in the lens AND in the economics break
Finding: the estate's trajectory spine is `memory/trajectory/steps.jsonl` (65,151 valid rows,
live, 2,995 sessions) and the receipt's ~37k was already a flagged stale-inherited number
(READ_ESTATE_RUN_SPEC_ADDENDUM.md:114). Falsifier: a full-tree steps.jsonl census showing no
five-digit file (would require this file to have moved or purged). Move: amend the MIRA receipt
with the absolute path plus a fresh wc and strike the phantom framing downstream (5 min).

### A2. The quantizer propagation gap is upstream of the compile stamp
Finding: `memory/percolator/invariants.json` (the compile's declared input,
compile_report.json:30, rib_feed at :23-29) contains zero rows matching
queen|mira|alodlm|2610. (grep, instrument 8) at mtime Oct 6 19:00, after the 18:26:38Z stamp.
Recompiling without filing the rows reproduces the same absence. Falsifier: invariants.json
gains the four rows and a fresh compile still packs zero. Move: file the four stack rows as
invariants or rib amendments, then recompile and verify the packs go nonzero (20 min).

### A3. benchmark_bridge fabricates its own fallback flag
Finding: `mag/llama_cpp_bridge.py:273` computes
`"fallback": all(not r.get("ok", False) for r in [{"ok": False}] * rounds)` - it iterates a
fabricated constant list instead of `results`, so `fallback` is always True regardless of the
rounds it just timed. Same evidence-fabrication class as F1's ok=True hardcode. Falsifier: any
input on which the expression reads `results` (code-reading falsifier; it never does). Move:
iterate `results` and add a unit test asserting the flag reflects the actual runs (10 min).

### A4. No repo entrypoint can reproduce the banked d13 evidence
Finding: main() (`mag/selfplay_orchestrator.py:283-304`) constructs the default bridge with
model_path=None (`:138`; `llama_cpp_bridge.py:44`) and never spawns, so every move rides the
sha256 hash fallback with ok=False and timing 0; evidence_latest.json was written by the d13
lane probe (`d13_selfplay_run_probe.py:135-153`), which spawns with a hardcoded Ollama blob
path (`:66-69`, `:101-103`) and documents three deviations from the landed profile (gemma2
stand-in, chat-template wrap, CPU build, `:9-17`). The next re-run is currently an archaeology
dig, not a command. Falsifier: run main() on repo bytes and observe non-fallback moves
(impossible by code reading). Move: give main() a --model-path/--spawn path or promote the
probe into scripts/ so the falsifier of F2 is one command (30 min).

### A5. A test pins coincidence as correctness
Finding: `tests/test_selfplay_orchestrator.py:109` asserts `result.correct is True` with the
inline comment "fallback move won't match; but check structure" - the comment contradicts the
assert, and the pass depends on the answer's digit appearing inside the sha256 fallback string.
Falsifier: any problem whose expected digit is absent from that prompt's hash flips the assert.
Move: fix the assert to the honest expectation (correct is False on the fallback actor) or mock
the actor leg (5 min).

## Convergence checks

- F2 x2 with operations F1/F2: VERIFIED at operations.md:11,17.
- F3 with economics falsifier 2: convergence VERIFIED but both censuses shared the same hole
  (break-economics.md:31 find missed memory/trajectory/steps.jsonl); the convergence converged
  on an incomplete census.
- F4 pack-absence with accuracy F5 / break-accuracy A4: VERIFIED (break-accuracy.md:49 credits
  logic.md:26; my name-and-id grep extends it). break-accuracy.md:36,38,45 additionally carries
  the magnetic card and dungeon.py findings that would have weakened F4's phantom half; logic.md
  did not consult its own sibling break.

## Not run / OWED

- The lens's named falsifiers all remain unrun: the unset-OPENROUTER full d13 re-run, the
  endpoint-routed generation re-run, and the outcome-bearing join over memory/runs/*/lanes/.
- The repo-wide gladiator/magnetic grep was launched and stopped before completion; every
  absence claim above is scoped to the named instruments instead.
- The lens's blind spots 5 (local fleet marginal cost priced at zero) and 6 (bank-time
  concurrency) were not checkable in this pass and stand as declared.
