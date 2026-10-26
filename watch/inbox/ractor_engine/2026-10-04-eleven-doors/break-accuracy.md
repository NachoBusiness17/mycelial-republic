# BREAK-ACCURACY pass - hostile second pass on the 11-doors lens report

Session: 2026-10-04, moment anchor `.venv/Scripts/python.exe mag/arena_bench.py --selftest`
receipt stamped 2026-10-04T16:58:03Z; all counts below taken in the minutes after unless
named otherwise. HEAD at pass start and end: 00cb15c77 (`git rev-parse --short HEAD`),
tests/ porcelain clean (no untracked test files at my moment). Instrument for every count
named inline. Writer: break-accuracy (hostile pass), doors topic per
watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md + watch/inbox/GWAP_INDEPENDENT_COP_20261004.md
(both read in full this session).

Material under test: the 5-finding lens report handed to me (finding 5's text arrived
truncated mid-sentence at "Cargo "; its evidence and falsifier were intact and are
verdicted on what is checkable).

## Verdicts

### F1 "ask's 11-door frame stale by two (door 2 landed, door 4 cured)" - CONFIRMED, two evidence corrections, one caveat the falsifier fired on

Confirmed legs, re-run this session:
- Door 2 landed: HEAD = 00cb15c77; `git show --stat 00cb15c77` touches mag/arena_bench.py
  (+9), tests/test_arena_bench.py (+94), watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md
  (exists, 2,471 bytes). I ran `.venv/Scripts/python.exe mag/arena_bench.py --selftest`:
  rc=0, both synthetic verdicts minted (fixture_honest_ghost PASS 1.0,
  fixture_maru_sycophant FAIL 0.3675, seal MATCH), matching the commit message. I ran
  `pytest tests/test_arena_bench.py -q`: 4 passed. Lens claim "4 tests tracked" byte-true.
- Door 4's named harm class is dead IN THE NIGHT LANE: queue/lanes/night/trail.jsonl last
  CYCLE_FAIL 2026-10-03T23:08:04Z, then green CYCLE 23:10:55Z and post-cure CYCLE
  2026-10-04T08:50:01Z ("monitor rc=0; march rc=2 :: MARCH SKIP rc=2: no key" - the honest
  skip the cure built). I read cycle_night whole (mag/lane_runner.py:911-939): two legs,
  no per-leg flags, sole state write last_night at :938 - the lens's "per-leg resume of two
  $0 legs" remainder is accurate for the night lane.

Corrections (evidence byte errors, neither inverts the finding):
1. "tests/test_night_march_cure_20261004.py on disk, 7 tests" is wrong by the instrument:
   `pytest --collect-only -q` reads 6 tests, `pytest -q` runs 6 passed. The "7 tests"
   figure is the 9718e812d commit message's own claim, hand-copied - the census-denominator
   law's exact disease, and the lens's own blind spot (no pytest fired) admits it.
2. Commit attribution: `git show --stat 9718e812d` touches ONLY
   tests/test_night_march_cure_20261004.py, the receipt md, and watch/march_228.py. The
   lane_runner.py half of the cure (trail-before-persist + the 5x-CYCLE_FAIL comment at
   mag/lane_runner.py:932-938) was landed by 9c52757f9 (NIGHT SHIFT lane 4/10) -
   `git log --oneline -S "5x CYCLE_FAIL" -- mag/lane_runner.py` returns 9c52757f9, not
   9718e812d. The harm-class-cured claim survives on trail bytes; the lens named the wrong
   commit for half the cure.

Caveat the lens's own falsifier caught: "CYCLE_FAIL re-run rows accruing in queue trails
after 9718e812d" - FIRED in a sibling lane. queue/lanes/research/trail.jsonl carries 513
lifetime CYCLE_FAIL rows including a post-cure Errno-22 storm TODAY at 12:27:36Z,
12:29:30Z, 12:31:37Z (all after the 08:55Z cure commits; identical
OSError Errno 22 on /app/queue/lanes/research/runner_state.json), resolving by 12:32 with
healthy MONITOR rows 15:29Z-16:48Z. The night-only cure leaves the state-write re-run
class alive in the research cage. Striking door 4-as-specced (night legs) stands; a
generalized atomic-save/checkpoint cure for the research cage is real remaining work the
strike move must carry.

### F2 "EG-20 pass@K silently dropped, remains unbuilt" - CONFIRMED, and strengthened past the lens's own hedge

- The ask's 11-door enumeration omits EG-20; the receipt's own table ranks it 3rd with the
  dig's only measured effort figure ("2h (measured at spec)",
  watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:237), and the reviser's build-first
  answer names it second after the cop fix (same receipt :219, :225). The ask's
  "reviser-ordered sequence" framing is violated by the ask's own list.
- watch/inbox/ESTATE_GAP_DIG_20261004.md:63 (EG-20 defined) and :79 (row 9: "Coverage
  column (pass@K, large K) beside win rate in arena/gwap | 2h | column present; predicts
  the mesh vs frontier routing on one batch") byte-confirmed by direct read.
- watch/inbox/ESTATE_GAPS_20261004.json EG-20 row: "status": "open", first_seen
  X_INTEL_PAPERS_20261004.md (Sharpening Tax, arXiv 2610.01509) - byte-confirmed.
- Untruncated absence census, instrument named: `git grep -n -E "pass@k|pass_at_k" --
  tools/ mag/ tests/` exit 1 (lens's exact instrument, re-run); plus my wider scopes, all
  zero hits: tracked scripts/ configs/ dashboard/ githooks/ state/ queue/ docs/ corpus/
  (git grep exit 1) and untracked *.py under tools/ mag/ tests/ (filesystem
  `grep -rniE`, zero lines). The only pass@K bytes in the estate are prose
  (receipts/commit), zero code.
- Commit 00cb15c77 message ends "Bench live again; the pass@K diagnostic rides it";
  watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md:46 says the same. No owner note drops
  EG-20 by name (git grep over watch/inbox: the only two EG-20 mentions both keep it
  alive). Both of the lens's falsifiers checked and dead.

Strengthening beyond the lens: I fetched https://arxiv.org/abs/2610.01509 this session.
It exists: "Sharpening Tax in Post-Training", abstract confirms pass@K coverage (base
models surpass post-trained counterparts in solution coverage at large K) and the
sharpening-tax diagnostic (loss in test-time scalability after post-training). The lens's
"motivating cite is secondhand-unfetched" hedge is CLOSED: the motivation is
primary-verified, so EG-20's priority no longer rests on estate-side facts alone.

### F3 "self-steal ledger: monoculture half-held, pheromone quarter-held + scale-gated, clippy-prober un-held" - WEAKENED (arithmetic confirmed, scale clause refuted by the lens's own uncensused store)

Confirmed legs:
- agreement_rate computed: tools/env_contract.py:580 (Returns docstring), :648
  ("agreement_rate": agree / cases), :706 (print), tools/overmind_judge.py:313
  ("agreement_rate": round(agree / n, 4)). Monoculture "half-held, 1h wire not a build"
  stands (the 1h-vs-2-4h re-cost itself remains a judgment, not measured).
- Momentum fail-absorbs floor: tools/gps_mcp/ledger.py:88-93 (law text), :238-257
  (MomentumStats fields) - and I add the implementation cite the lens lacked:
  ledger.py:435 `floor = mom.window_start_rate`. Pheromone "quarter-held" stands.
- Decay absent in code: `git grep -n -i -E "decay|evaporat" -- mag/river.py
  mag/swarm_tools.py tools/gps_mcp/ledger.py` exit 1 (re-run); decay lives only in
  README prose as named absence/growth item (README.md:221 "does not decay stale
  measurements", :229 "UCB/Thompson with time decay") - both re-read.
- FSRS/scheduler genuinely un-held, now with WIDER census than the lens ran: zero in
  tracked mag/tools/tests/scripts code (git grep; the sole filesystem "fsrs" hit is a
  byte-coincidence inside the binary tools/godot/Godot_v4.3-stable_win64.exe), zero in
  untracked *.py under those roots, zero in .agents/skills/ (grep exit 1), zero in
  .zcode/skills/, zero in the ZMEM harness store (the store's only "spaced" hits are
  retry-pacing prose, e.g. "spaced retries on 1305s" - not a scheduler). The lens's
  blind-spot admission ("ZMEM not re-walked") is hereby closed in the FSRS direction.

Refuted leg (the lens's own falsifier, fired): "value is scale-gated on double-digit
stores" and the blind spot "if the ledger persists a larger state elsewhere... Not
censused this session." I censused it: the GPS ledger's real store is
tools/gps_mcp/gps_ledger.db3 (default at server.py:124), holding verdict_log = 593 rows
and capability = 30 rows (sqlite count this session, after the 16:58:03Z anchor).
CONVERGENT: commit d349ce7d2 (GO WAVE 20261004) independently names "idempotence proven
593->593" for the same table. The pheromone door is NOT scale-gated on an 11/80-row
store; its live substrate is a 593-row verdict log, which raises the door's EV and
weakens the lens's "sequence pheromone after the gwap v3 backfill" demotion (the
v3-backfill point itself still stands: the 618 banked rows are old-instrument rows per
watch/inbox/GWAP_INDEPENDENT_COP_20261004.md:75-78).

### F4 "MCP-lattice gate fails today (no tags); Gero-4B precondition live; weld gate cleared" - CONFIRMED

- `git -C ../library_parked/agentmemory tag | wc -l` = 0; HEAD = c51bf3f ("fix: embedding
  key precedence, structured SessionStart context, docker engine config (#1472)");
  .git/shallow present. Shallow clone, zero tags - the receipt's own falsifier
  (PRIMER:57 "cannot be pinned to a tag... stop at the spec reconciliation") is in its
  stop state today. Note the gate failure is itself 5-minute-curable (unshallow or pin to
  c51bf3f), which is the lens's move, not a door-killer.
- Gero-4B live-fetch re-verified this session: card exists, Apache 2.0, base
  Qwen/Qwen3-4B, safetensors BF16 ~4B sharded, generation removed (linear scorer,
  AutoModelForSequenceClassification), NO published evals. Matches
  watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:32-45 byte-for-byte. Build-once
  calibrator precondition verified.
- Weld gate: receipt table row 11 (PRIMER:245) "design-gated: needs the cop fix (rank 1)";
  bb0f34586 landed that fix (git log + GWAP receipt read). Nuance the lens skipped: the
  old 618 rows stay banked as old-instrument record (append-only law; re-grade is an
  operator decision, GWAP receipt :75-78), so "banked scores mean something" holds for
  new-minted rows, not the historical mix.

### F5 (truncated finding text) - evidence CONFIRMED as checkable, finding text itself unverifiable

The finding statement arrived cut at "Cargo "; I verdict the evidence, not the missing
prose:
- flock_field consumers: all six cites byte-confirmed (mag/emergent_harvest.py:16,
  mag/flock_job.py:7-11, mag/flock_scheduler.py:155, mag/rib_action.py:22,
  mag/rib_struct.py:20, mag/flock_steal.py:9). Instrument note: my own
  first grep was head-truncated at 15 lines and hid rib_struct.py - caught by direct
  read; the quantifier law bites the breaker too.
- GWAP receipt backfill naming: GWAP_INDEPENDENT_COP_20261004.md:78 "The GPS feed door:
  the next --backfill of NEW run dirs banks v3" - confirmed.
- 613-row old-ledger count: 613 was true at the receipt/lens moment; my recount reads
  618 (python line count, post-16:58Z moment). Live-hourly chain; every figure on this
  file is moment-scoped and the GWAP receipt's "613 rows" headline is already stale.
- mag/steal_steer.py:1-30: confirmed - sha256 embeddings into field coordinates (:10-11),
  "Deterministic, $0, no LLM", no semantic vector organ anywhere in the file.

## Additions (what the lens missed)

1. GPS ledger store census (the lens's admitted blind spot, fired):
   tools/gps_mcp/gps_ledger.db3 = 593 verdict_log rows + 30 capability rows
   (sqlite3 count, this session; default path server.py:124). CONVERGENT with
   d349ce7d2's "593->593". Move: re-cost the pheromone door upward (5 min); its
   substrate is 50x the receipts.jsonl row count the lens scaled on.
2. arXiv 2610.01509 primary-fetch: exists, "Sharpening Tax in Post-Training", pass@K
   coverage confirmed in abstract. Move: strike the "secondhand-unfetched" hedge from
   EG-20's priority case (2 min, no build).
3. Research-cage post-cure Errno-22 CYCLE_FAIL storm (12:27-12:31Z today, 513 lifetime
   rows in queue/lanes/research/trail.jsonl): the state-write re-run class survived the
   night-only cure in a sibling lane. Move: before striking door 4 entirely, spend 15
   min checking whether the research cage daemon predates the 9c52757f9 atomic save (if
   it is container-image lag, a cage restart closes it; if it is os.replace failing
   through that bind mount, the cure class is incomplete and door 4's family has a live
   second instance).
4. Test-count instrument discipline: the night-march file collects/executes 6, not the
   commit message's 7. Move: none needed beyond citing pytest, not prose, for counts.
5. The banked gwap chain moved 613 -> 618 within hours of the cop receipt landing.
   Move: any door that consumes the ledger (consume-the-ledger, pheromone, weld) must
   name its count moment; the receipt's figures are already historical.

## Checks the lens named that I ran vs did not run

Ran: arena_bench selftest (rc=0), pytest on the three named files (19 passed total:
4 + 6 + 9), all grep censuses above, sqlite census, agentmemory tag/shallow check,
Gero-4B live fetch, arXiv 2610.01509 fetch, night/research trail reads, cycle_night
whole-function read.

Not run (OWED, stated): the GWAP new-instrument figures (529 payloads; verdict split
161/88/64/216) were NOT re-derived this session either - that requires running the v3
instrument over all playground run dirs and is the backfill door's own work; the
receipt's figures stay the commits' own. The full pytest suite was not fired (the ask
names byte-checks, not the suite); the three door-relevant files were fired instead.

No em-dashes were used in this receipt. End of pass.
