# BREAK-MOONSHOT-2: hostile second pass on lens moonshot-2 (the 11-doors dig)

Writer: break-moonshot-2 (hostile pass). Moment: 2026-10-04, checks run 16:5x-17:1x UTC
(12:5x-13:1x EDT). Tree state at pass: HEAD 00cb15c77 (door 2, committed 12:39:31 EDT);
no door landed after door 2 as of my runs (git log re-read this session).

Tasking note: the lens's finding 4 arrived in my tasking TRUNCATED mid-evidence
("git log: commit 9718e812d cured the state-loss re-run class ('_save_state O_TR").
I verdict the verifiable fragment and name the truncation; the full finding text and
its move are outside my evidence.

## Instruments I ran (all this session, all against the live tree)

- git grep -n -i -E "decay|evaporat" -- mag tools (full output read; unscoped over mag+tools)
- git grep -l selftest -- mag tools (25 files); git grep -l selftest -- tests (10 files);
  git grep -l -i "selftest_sweep|sweep.*selftest" -- tests mag tools (0)
- git grep -n -i -E "shapley|second.price" -- mag tools (0 hits); extended census over
  watch corpus docs memory (hits, see addition 3)
- .venv/Scripts/python.exe mag/arena_bench.py --selftest (rc=0, both synthetic verdicts,
  seal MATCH; minted 3 designed receipt files under memory/arena_bench/)
- .venv/Scripts/python.exe -m pytest tests/test_night_march_cure_20261004.py -q
  (6 passed in 5.10s); grep -c "def test_" on that file (6)
- Receipt census: json parse of tools/gps_mcp/receipts.jsonl (11 rows, key census, per-row dump)
- Timing sample: 8 selftest entrypoints timed with bash date +%s.%N, rc captured
- Reads: mag/republic.py:200-223,392-417; mag/mycelium.py:183-202; tools/gps_mcp/ledger.py:418-447;
  tools/oracle_calibration.py:1-60,120-174; tools/gps_mcp/router.py:8-32,130-154,850-861;
  mag/lane_runner.py:118-137,918-939; tests/test_arena_bench.py (full body, 4 tests);
  watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:28-67; both tasking receipts in full
- WebFetch of https://huggingface.co/vixhal-baraiya/Gero-4B (succeeded; quotes below)
- git log --format="%h %ci %s" (commit ordering), git log --grep pass@K -i, git grep pass@K

## Verdicts

### Finding 1 (decay family = ports of held law, not new vocabulary): CONFIRMED

Every cite byte-checks: mag/percolator.py:172-183 (_decay_count, half-life, floor 1,
whole UTC cycles, decay_as_of) exactly as claimed; mag/mycelium.py:265-277 (decay()
stamps decayed/decayed_at, log-only, no successor); mag/memory_consolidate.py:47-48
(DECAY = 0.995) and :127-130 (_decayed_score); mag/signals.py:82-87 (recency_decay,
half-life config at :37-38); mag/ladder.py:72 (24h decay); mag/gene_pool_feeder.py:241-261
(window decay to floor 1.0x, never zero); mag/republic.py:396-417 supersede() ("the old
letter STAYS, points superseded_by... Never a deletion") with the append-only invariants
at :209-218. The falsifier's parenthetical is TRUE and helps the port: GPS ledger rows DO
carry last_measured/updated_at (INSERT at tools/gps_mcp/ledger.py:423-427, UPDATE at
:444-447), so decay has a key; the port pattern is proven on disk at
tools/concept_span_check.py:122-124 ("mag/percolator.py _decay_count, re-implemented
read-only"). The primer's zero-hit grep scoping is accurate (receipt line 186 names
exactly mag/river.py + mag/swarm_tools.py + tools/gps_mcp/ledger.py). One sharpening:
republic's supersession invariants literally bind to the book container
(old_l.superseded_by not in book.letters, mag/republic.py:214-217), so the mycelium port
is a REIMPLEMENTATION of the law against edge dicts, not an import; same sitting-scale,
and it is exactly what the primer's MYCELIUM-V2 spec already orders.

### Finding 2 (selftest SWEEP is the class cure, not per-organ tripwires): CONFIRMED,
cost clause struck

Census re-run: exactly 25 files carry selftest in mag+tools (13 mag + 12 tools; the six
organs the lens named are all present). tests/ references selftest in 10 files, all
per-organ; zero sweep-shaped files exist (git grep for sweep patterns: 0). Door 2's
landing verified byte-exact: tests/test_arena_bench.py 4020 bytes, mtime Oct 4 12:35,
landed in 00cb15c77 (committed 12:39:31 EDT); I read the FULL body this pass (4 tests:
selftest split proof, canonical-surface parse, redirect-stub detector with the
meta-refresh + 4000-byte checks, JSON-record determinism) which upgrades the lens's
existence-only confirmation. My own run: mag/arena_bench.py --selftest rc=0, synthetic
PASS 1.0 and FAIL 0.3675, seal note MATCH. BUT the falsifier partially fired on
measurement (8-organ timed sample): the entrypoint grammar is NOT uniform. cite_gate,
quota_ledger, engram exit rc=2 on a bare --selftest flag (cite_gate's selftest is a
SUBCOMMAND: "usage: mag.cite_gate [-h] {check,selftest}"); pigeonhole exits rc=1 with
ModuleNotFoundError: No module named 'config' when run as a bare script (needs module
mode); oracle_calibration alone took 54.26s; citation_lint 4.31s; wandr_selfeval 0.28s;
falsifier_counter 0.43s. So "same cost as the landed single tripwire" is wrong: the
sweep needs an invocation registry (exact argv per organ, module-mode for some) and a
time split (fast set at pre-push, the 54s-class nightly). The 1-2h estimate survives
only if nonconforming organs are skip-listed by name in the registry golden.

### Finding 3 (Gero-4B download is cargo; calibrator exists and starves): WEAKENED
(diagnosis confirmed, starvation story and 2h move refuted by the lens's own falsifier)

Cites all byte-check: tools/oracle_calibration.py docstring :13-39 (ECE/MCE/Brier
:14-16, temperature :17-19, per-domain drift :20-22, thresholds :23-27, "Stdlib only"
:39, input rows {confidence, correct, decision_class} :36-37) and the computation
:120-174; the stale note at :29 ("No live oracle confidence ledger exists on disk
yet"); router docstring :9-11 ("recorded on every ask receipt"), receipt schema
:17-19, row write :140, default receipts :856; X_INTEL_PROPER_SCORING_20261004.md:32-46
(card facts) and :50-59 (the log-score rule). The Shapley/second-price zero-hit grep
over tracked mag+tools re-ran clean (0 hits) and I confirm it as a SCOPED absence claim.
NEW: I fetched the HF card itself (the lens's named blind spot) and it verifies the
receipt nearly verbatim: no published benchmark numbers, Qwen3-4B base rebuilt into a
scorer, "No language-model head", learned linear scorer over each option's final token,
proper-scoring RL, "at the very top of the range the model runs slightly optimistic".
The receipt is faithful; finding's cargo diagnosis stands. What falls: the starvation
story and the 2h adapter. My census of tools/gps_mcp/receipts.jsonl: 11 rows total,
only 4 carry confidence (all 0.92, all model flash-mid-1, all one moment
2026-09-30T23:08:42), and ZERO rows carry any correct/verdict/outcome field (key set:
ts, task_shape, chosen, considered, reasons, cost_usd, confidence, exploration,
challenger, judge, decision; "decision" holds 'duel-route', a routing choice, not a
correctness outcome). Router is not meaningfully "recording confidence on every ask
receipt": 4 stale rows from one moment, nothing since 09-30. The lens's own falsifier
clause ("confidence without a verdict to bind to... the wire needs a writer change
first and the door reverts toward its 4-8h estimate") is therefore FIRED, on
measurement, not hypothetically: honest re-price is the door's original 4-8h with a
writer change (bank confidence and correctness together at duel/judge time).

### Finding 4 (truncated in tasking; night-cycle state-loss cured by 9718e812d):
CONFIRMED on the verifiable fragment

Commit 9718e812d exists and its message carries the claimed bytes: "_save_state O_TRUNC
through the bind mount lost completed-work records (5 CYCLE_FAILs 10-03, ~100s re-run
loops). Cure: guarded key read + honest rc=2 MARCH SKIP, stderr tail kept on failure,
trail-before-persist, atomic tmp+os.replace state save. Cage proof 08:50Z." The cure is
IN mag/lane_runner.py, not just the cage copy: :124-137 documents the Errno-22 cure
(atomic tmp+replace, naming the 5x CYCLE_FAIL class) and :925-936 documents the march
stderr-tail cure and trail-before-persist. Consequence for the door table in addition 1
below. The commit's "7 tests" claim is a MIScount by the estate's own census law: the
landed file has 6 def test_ and pytest -q runs 6 passed in 5.10s (both instruments
mine, this session); the delta the lens left unreconciled is closed as a commit-message
hand-count error, the exact class AGENTS.md's census bullet forbids trusting.

## What the lens missed (additions)

1. THE RANKED BUILD ORDER CARRIES A CURED DOOR AT RANK 4. The primer's door table
   (watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md, steal-door table row 4) ranks
   NIGHT-CYCLE CHECKPOINT LEGS 2-4h to "cure the documented 5x-CYCLE_FAIL full-cycle
   re-run class", but 9718e812d cured that class hours BEFORE the receipt landed
   (cure cage proof 08:50Z = 04:50 EDT; receipt committed 12:00:44 EDT as 0838e150e).
   The door's named harm is dead; the residue (per-leg resume for a TWO-leg cycle,
   monitor at mag/lane_runner.py:922 and march at :924, whose state-loss abort class is
   atomically cured) is near-cargo. Falsifier: a post-cure Errno-22 recurrence in
   logs/lane_scheduler.log dated after 2026-10-04, or new full-cycle re-run rows in
   queue/lanes/*/trail.jsonl after the cure, revives it. Move (5 min): strike rank 4,
   fold a "cured 9718e812d" note into the next receipt revision, and hand the freed
   2-4h to EG-20 pass@K, which I confirmed STILL unbuilt (zero pass@K hits in
   mag/tools/tests/configs; only the spec commit 06f8ac272 and door 2's future-tense
   "rides it" note).
2. THE SELFTEST CONVENTION IS THREE GRAMMARS WIDE (measured): bare --selftest flag
   (works: arena_bench, oracle_calibration, wandr_selfeval, falsifier_counter,
   citation_lint), subcommand form (cite_gate {check,selftest}; likely quota_ledger and
   engram, both rc=2 on the flag), and module-mode-only (pigeonhole: ModuleNotFoundError
   as a script). Plus one 54.26s organ (oracle_calibration). The sweep door therefore
   ships with an invocation registry and a fast/heavy split, or it will fail its own
   first run. Falsifier: a canonical selftest invocation spec already on disk that I
   missed (grep found none). Move (+30 min over the lens's 1-2h): registry rows carry
   exact argv + module mode; markers split pre-push vs nightly by measured seconds.
3. THE SHAPLEY/SECOND-PRICE GREENFIELD IS GREENFIELD IN CODE ONLY. The extended census
   (git grep over watch corpus docs memory) hits design notes the lens's mag+tools
   scope could not see: the primer's own economics section (receipt line 202) carries
   the Shapley-sampling door spec with corpus cites (phases/16 lesson 21-agent-economies
   docs :44-52, :54-58, :127) and a second-price-under-monotone-aggregation clause;
   docs/ref/VAST_DEEP_GROK_ECONOMICS.md:169 and :611 carry a second-price clearing
   discussion with the estate's unverified-claim hedging discipline. And the router
   receipts already carry judge/challenger columns (my key census above), which are the
   natural key set for both the calibration join and a Shapley sampler. Falsifier: if
   the corpus lesson's Shapley spec proves inapplicable to per-judge credit (different
   problem shape), the notes are prior art only, not a spec. Move (15 min census, then
   build): re-price door 12 at 4-8h; land the log-score RULE (X_INTEL :50-59) inside
   the gwap v4 door at zero model cost, Gero-4B stays behind its download-and-eval gate.
4. THE GPS LEDGER ALREADY HAS HALF A METABOLISM. tools/gps_mcp/ledger.py:434-443: on a
   zero observation while momentum is rising, a floor (window_start_rate) absorbs the
   fail ("a fail absorbs (rate unchanged), it never rewards"). Dispute-streak slashing
   and decay are missing, but the floor law exists, so PHEROMONE METABOLISM is a
   decay-only delta on top of an enforced floor, priced at the LOW end of its 4-8h, and
   must not re-mint the floor. Falsifier: the floor is conditional on mom.rising, so a
   flat-market ledger gets no protection today; if that matters for the door's
   catastrophic-drift falsifier, the delta includes un-conditioning the floor (costs
   more). Move (0 min, pricing note): port _decay_count per concept_span_check.py:122-124,
   keep the floor as is.
5. THE MONOCULTURE PROXY HAS AN IN-ESTATE METRIC TO STEAL. mag/mixture_of_agents.py
   already computes convergence (0-1) and dissent_preserved per synthesis (:74-75, :90-91,
   gated at :125). The agreement-rate proxy door should wire that computation over
   sibling receipts (cross-lane agreement), not mint a new agreement metric from
   lesson 23 exercise 2 alone. Falsifier: MoA convergence is a within-run metric over
   concurrent answers to one prompt; if cross-lane agreement needs a different
   denominator (independent tasks, not parallel answers), the steal is the metric
   shape, not the computation. Move (30 min): reuse the convergence/dissent fields as
   the proxy's output schema before writing new vocabulary.

## Blind-spot closures (the lens's own OWED list, measured here)

- Selftest timing: 8-organ sample timed (see finding 2); full 25 not timed (OWED
  remains, but the sample already answers pre-push vs nightly: split it).
- Sibling landings / EG-20: HEAD unchanged since 00cb15c77 12:39:31 EDT through my
  pass (~17:1x UTC); pass@K unbuilt, zero code hits.
- Night-march 6 vs 7: reconciled as a commit-message miscount; 6 is byte-true by two
  instruments.
- Gero-4B card: primary-verified by fetch; receipt faithful (see finding 3).
- test_arena_bench.py body: read in full this pass (4 tests, assertions as claimed).
- Shapley/second-price census scope: extended beyond mag+tools; hits exist and are
  named in addition 3.

## Honest not-runs

- I did not time all 25 selftest entrypoints (8-organ sample only).
- I did not build the three-signal door's 50-question held-out set or run recall@5.
- I did not deep-verdict the MCP-lattice, weld, or consume-the-ledger doors (outside
  the lens's four findings; their self-steal censuses remain OWED for a later pass).
- The lens's finding 4 text arrived truncated in tasking; only its evidence fragment
  was verdicted.
- My arena_bench selftest run minted 3 receipt files under memory/arena_bench/
  (the organ's designed zero_human behavior; same class as the pre-existing untracked
  receipts in git status).

End of pass.
