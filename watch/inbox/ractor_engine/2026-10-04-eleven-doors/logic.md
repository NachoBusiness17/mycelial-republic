# LOGIC LENS - the 11 remaining doors, self-steal first (2026-10-04)

Writer: lens-logic of the ractor on the 24-wide dig's build sequence. Ask: per
door, self-steal first (what does the estate already hold), hostile pass on
the door's own falsifier, honest build order by EV-per-hour, cargo verdict.
Inputs I read this session: watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md
(full 320 lines), watch/inbox/GWAP_INDEPENDENT_COP_20261004.md,
watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md, state/CURRENT.md,
tests/test_night_march_cure_20261004.py, tests/test_arena_bench.py (head),
mag/lane_runner.py (cycle_night + _save_state), mag/arena_bench.py (ground
truth + argparse), mag/gwap_to_gps.py (docstring + verdict mapping),
mag/mycelium.py (:183, :265), mag/flock_field.py (:158-176), githooks/pre-push
(gate inventory), plus the greps and selftests named inline. Door 1
(independent-cop, commit bb0f34586) landed before this ractor; door 2
(arena-bench tripwire, commit 00cb15c77) LANDED MID-SESSION at 12:39 EDT
while I worked (my first ls found no tests/test_arena_bench.py; the commit
now sits at HEAD). The sequence is being consumed live by sibling seats; every
rank below is a snapshot.

## The state of the board after doors 1 and 2

Nine doors remain of the ask's eleven: clippy-as-prober, night-cycle
checkpoint legs, monoculture agreement proxy, pheromone metabolism,
mycelium-v2 bi-temporal, MCP-lattice shim, three-signal query broker, weld
door, build-once calibrator, consume-the-ledger wire is ten; subtract the
landed tripwire and the ask's own list is the ten minus nothing else. EG-20
pass@K (receipt rank 3) is NOT in the ask's eleven at all; see finding 4.

## Finding 1 - door 2's enforcement contract is unwired: the tripwire claims
a pre-push gate that pre-push does not run (CONVERGENT with the
citation_lint vacuous-pass class)

Evidence, all checked this session: tests/test_arena_bench.py:13-14 says
"this tripwire runs the selftest AND the real-surface parse at pre-push";
watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md:47-49 says "Pre-push now covers
the bench"; but githooks/pre-push (516 lines, the ACTIVE hook:
`git config core.hooksPath` -> `githooks`, verified) executes
violation_ratchet, citation_lint, config_seal, census_drift_patrol, workflow
gate scenarios, refold gate, caption verify and parity (grep inventory at
:10,:25,:27,:103,:311,:240) and runs ZERO pytest collections of tests/; the
only "pytest" string in the file is a comment at :201. So the four tripwire
tests fire only when a seat or patrol runs pytest by hand, and the census
patrol collects but never executes (AGENTS.md census bullet names
`pytest --collect-only -q` as its instrument). The disease is the same one
door 2 cured, one level up: the bench raised honestly into the void for 12
days (receipt :18-19 "raised honestly - on every run, silent to every gate");
now the tripwire passes honestly into the void at every push. This converges
with the 24-wide receipt's own instruments-table row on citation_lint
(PRIMER:308, VACUOUS-PASS hazard): a gate whose claimed enforcement surface
is not the surface that actually runs.

Falsifier: any hook, CI job, or scheduled task that executes
tests/test_arena_bench.py on push or schedule (a different core.hooksPath, a
schtasks entry running pytest). I verified core.hooksPath=githooks and read
the hook in full grep; no such runner was found. Note `git remote -v` shows
no GitHub remote (PRIMER:108), so no external CI can exist either.

Move, one sitting (~1h): wire an arena-bench trigger into githooks/pre-push
in the existing refold-gate shape (prepush_paths_changed.py + scoped pytest
run, precedent at githooks/pre-push:197-240, REFOLD_PINS at :220): when
mag/arena_bench.py, tests/test_arena_bench.py, or
dashboard/static/games/arrakis.html (and dungeon.html) change, run the four
tests, exit 1 on red. That converts the receipt's sentence into a real gate.

## Finding 2 - door 3 (night-cycle checkpoint legs) is ~80 percent
self-stolen; the residual is a one-clause trail consult, not a 2-4h flags
system

Evidence: the 2026-10-04 night shift already landed
tests/test_night_march_cure_20261004.py (5 tests, read in full this session):
cure = trail the CYCLE row BEFORE persisting last_night
(test_cycle_night_trails_composite_even_when_state_write_fails, :100-119) and
_save_state is atomic tmp+replace (:82-91). But mag/lane_runner.py
cycle_night (read this session, the block spanning the "Composite night
cycle" docstring through `_save_state("night", ...)`) still gates ONLY on
`st.get("last_night") == today`; it never consults the trail, and the cure's
own comment says the Errno-22 lock is "external and transient, not
code-side" (the _save_state Errno-22 comment, read this session). So when the
external lock bites during the state write, the daemon STILL re-runs monitor
plus march on its ~100s retry; the cure made the re-run visible (the CYCLE
row is banked) but not prevented. The door-3 spec (per-leg done flags through
_save_state, resume past completed legs, PRIMER:171) is the heavyweight
version of a cheaper invariant: idempotency by evidence already banked, i.e.
on entry read the last CYCLE row for today from trail.jsonl and skip legs it
already records. One guard clause.

Falsifier: if watch/monitor_lane.py is itself idempotent and side-effect-free
on same-day re-run, the residual harm is zero and even the guard clause is
cargo; I did NOT verify monitor_lane.py's idempotency (blind spot, named).
Also if the transient lock makes the trail write fail too (same mount), the
guard reads a stale trail and re-runs anyway; the guard narrows, not
eliminates, the window.

Move, one sitting (~1h): add the trail-consult guard to cycle_night plus one
test pinning "second same-night call after a simulated state-write failure
does not re-run monitor". Re-price door 3 from 2-4h (its rank-4 slot was
priced on the pre-cure harm, which the night shift already collected) to ~1h
residual.

## Finding 3 (CORRECTED after hostile second pass; the original census byte
was false and the harm mis-scoped twice - correction verified byte-by-byte
this session, commands named inline) - the gwap poison is ALREADY BANKED in
the GPS router: 248 verdict=0 rows, 244 of them the fake silent-cop tavern
class, and the only append-only-compatible cure is the decay family

CORRECTIONS OWED AND PAID. My original claim "all 613 rows carry NO
engine_version" was false: I read the payload TOP LEVEL where the field
never lives. The nested census (payload.replay_tape_ref.engine_version, run
this session) stamps EVERY row: arena-dungeon-v2: 327, arena-tavern-v2: 286,
plus 12 new v3 rows (arena-dungeon-v3-independent-cop: 5,
arena-tavern-v3-independent-cop: 7) - the file grew 613 -> 625 mid-session,
the sibling seat is banking v3 live. The discriminant already exists on
every row, so a bridge version gate is a ~30min read-guard, not an
instrument build. My "harm is latent" scoping was also false twice over:
(1) the live path feeds exactly this file (tools/arena_gwap.py:312
SessionLedger("arena-capability") -> :328 feed_session(ledger.path,
GPS_LEDGER...), the :319-321 comment "the bridge walks the WHOLE ledger
file"); (2) the poison is already banked: a read-only sqlite census of
tools/gps_mcp/gps_ledger.db3 verdict_log (run this session) shows 351
arena-agreement-v1 rows = 248 verdict=0 + 103 verdict=1, and the a04 dedupe
(UNIQUE INDEX on model_id, task_shape, evidence_hash,
tools/gps_mcp/ledger.py:153-157) means already-fed rows skip on any refire,
so a feed-time version gate prevents almost nothing for the banked poison.

WHAT SURVIVES, now byte-proven. The bridge still branches on verdict only:
SKIP_VERDICTS = (CHALLENGE, BLOCKED), VERDICT_TO_BIN maps
VERIFIED_AGREE->1 / DISPUTE->0 (mag/gwap_to_gps.py module-top mapping block,
read this session), and git grep engine_version over the file finds only the
:282 demo string - the discriminant exists on every row and the bridge
ignores it. Harm attribution, closed by an evidence-hash join run this
session (every verdict_log evidence_hash joined back to the chain's
row_sha256, zero unmatched): all 248 banked zeros are gwap DISPUTE rows -
244 arena-tavern-v2 (the fake silent-cop class door 1's receipt names as
"feeding the GPS router fake DISPUTE signal", GWAP_INDEPENDENT_COP:17-19)
plus 4 arena-dungeon-v2; all 103 ones are dungeon-v2 VERIFIED_AGREE. The
poisoned surface is live in the router's capability table (same read-only
census): claude-haiku-4.5 pass_rate 0.0 on 86 samples, fable 0.229/52,
sonnet 0.293/116, opus 0.611/97.

Falsifier (tightened): (a) CLOSED - a per-row attribution to honest dungeon
disagreements would break the tavern claim; I ran the join and it reads
244/248 tavern-v2. (b) OPEN - if the router's selection path never consumes
capability pass_rate for these model_ids/task_shapes, the zeros are inert; I
did NOT trace tools/gps_mcp/router.py's read path this sitting (the README
says routing is greedy threshold+cost over the ledger, PRIMER:186, but that
is the README, not the code read).

Move, retargeted per the hostile pass and these bytes: (1) ~30min: bank the
verdict_log census as an operator-facing receipt (248 zeros, 244 tavern-fake,
the four pass_rates) so the re-grade decision is a number, not a vibe; (2)
elevate the decay family (pheromone metabolism, door 6) to the top of the
post-tripwire tier - decay/supersede-with-lineage is the only
append-only-compatible cure for the 248 banked zeros; (3) the bridge version
gate shrinks to a ~30min read-guard whose remaining value is quarantining
never-fed pre-v3 rows (58-row arithmetic gap: 409 feedable old rows vs 351
fed; gap attribution not run, OWED) and carrying engine_version per row in
the feed report. Do not touch the append-only bank.

## Finding 4 - EG-20 pass@K is the top EV-per-hour door in the whole sequence
and it is missing from the ask's eleven, with no recorded drop decision

Evidence: the receipt's own build order puts EG-20 in the first tier after
the cop fix (PRIMER:219, "the only measured figure"); the spec carries the
dig's only MEASURED effort figure (2h) and a defined success meter ("column
present; predicts the mesh vs frontier routing on one batch",
watch/inbox/ESTATE_GAP_DIG_20261004.md:79); its dependency just landed: door
2's receipt says "the pass@K diagnostic rides it"
(ARENA_BENCH_TRIPWIRE_20261004.md:46-47) and I ran the instrument green this
session (`./.venv/Scripts/python.exe mag/arena_bench.py --selftest` -> exit 0
with both synthetic verdicts; `load_ground_truth()` -> PARSE OK, 8 keys). The
ask's eleven-door list omits EG-20; greps over queue/todo.md,
state/CURRENT.md, and both door receipts surface no drop or merge decision
(scope of the absence claim: those files only).

Falsifier: an operator or reviser receipt naming EG-20 dropped, merged, or
re-scoped; none found in the scoped files. Also, if the sibling seat that
landed door 2 picks it up next (its receipt says the diagnostic "rides" the
bench), the omission self-cures and this finding reduces to a bookkeeping
note.

Move: 2h, land the pass@K column per the ESTATE_GAP_DIG spec, before
clippy-as-prober (whose value is deferred: it banks probes toward FSRS's ~1k
threshold, PRIMER:126).

## Finding 5 - the build-once calibrator bundles a cargo dependency (the
Gero-4B download) with a stand-alone wire (truthful revelation on
hermes_burn); split the door

Evidence: the door as specced (PRIMER:211) wires Gero-4B as BOTH the
calibration flag on MoA/panel votes AND the second-price truthful-revelation
layer on hermes_burn asks, gated on "download-and-eval"; Gero-4B carries "no
published evals on the card" (PRIMER:211, from
watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:32-46). The second half needs
no new model: a proper scoring rule (log score or Brier) over the receipts
the estate already banks, with the existing calibrated-confidence surface at
tools/gps_mcp/router.py:9-11 as feedstock, is arithmetic, not a dependency.
The 4-8h estimate also excludes the eval harness the gate itself demands, so
the door's EV is back-loaded onto an unevaluated artifact. Self-steal on the
first half: mag/mixture_of_agents.py already carries convergence and
dissent_preserved fields gating at 0.7 (PRIMER:190), so the calibration flag
extends an existing surface. Hostile pass on the door's own falsifier: the
gate says download-and-eval first; by the door's own law the model is
unproven until evaluated, which is exactly why the wire should not wait on
it.

Falsifier: Gero-4B later publishing evals showing its proper-scoring RL
calibration beats a log-score rule on the estate's own panel shapes; then the
download earns its slot and the merge was right.

Move: split. Land the second-price/log-score layer on hermes_burn asks
(~1-2h, zero new dependencies) now; keep Gero-4B behind its download-eval
gate as a separately-decided artifact.

## Honest build order by EV-per-hour (my lens's answer, snapshot this moment)

1. EG-20 pass@K, 2h MEASURED, dependency landed (finding 4).
2. Wire the pre-push arena trigger, ~1h (finding 1; closes door 2's actual
   contract).
3. cycle_night trail-consult guard, ~1h (finding 2; closes door 3's
   residual).
4. feed_session version census, ~1-2h (finding 3; feeds the operator
   re-grade decision).
5. clippy-as-prober, 2-4h: nothing to self-steal (memory/retrieval/ does not
   exist, ls this session; git grep -i fsrs over mag/tools/tests/scripts ->
   zero code hits, one binary false-positive), builds fresh state, starts
   banking FSRS probes.
6. Decay family shared schema, then pheromone metabolism on the GPS ledger,
   4-8h: verified still absent (git grep -c -i -E "decay|evaporat" --
   tools/gps_mcp/ledger.py -> exit 1, zero matches, strict rerun this
   session; the receipt's zero re-confirmed).
7. mycelium-v2, 4-8h: premises verified live this session, the violated-law
   comment still stands (mag/mycelium.py:183 "jsonl is append-only; replace
   by rewriting the file") and decay() still stamps a boolean with no
   successor (mag/mycelium.py:265-277, read this session).
Then the design-gated five in the receipt's own order (three-signal,
mcp-shim, weld, consume-ledger, calibrator-minus-Gero), each of whose gates
is honest as specced; consume-ledger's premise verified (mag/flock_field.py
:158-176 steer() carries goal/separation/alignment/cohesion only, no
p_best/g_best term, read this session).

## Cargo verdicts

Cargo now: the Gero-4B download half of the calibrator (finding 5).
Down-scoped, not cargo: door 3 (finding 2). Deferred-consumer, watch: the
monoculture agreement proxy (git grep -i monoculture over mag/tools/tests ->
zero hits this session, so it builds new, but its named first test case, the
24-wide single-model dig, already ran; its consumer is future multi-lane
digs). Everything else survives hostile pass on its own stated falsifier,
with one repair: door 2's contract needs the hook wire (finding 1).

## Blind spots, named

- RESOLVED under hostile pass (was: "I did not trace which ledger files
  feed_session receives"): the live path feeds exactly
  memory/runs/gwap/arena-capability.jsonl (tools/arena_gwap.py:312,:328) and
  the poison is banked (248 zeros in verdict_log, 244 tavern-fake by
  evidence-hash join) - see the corrected finding 3. NEW open item in its
  place: I did not trace tools/gps_mcp/router.py's selection path, so
  whether the capability pass_rates actually move routing decisions is
  README-claimed, not code-read, by me.
- I did not verify watch/monitor_lane.py idempotency, which sizes finding
  2's residual harm.
- The EG-20 absence claim is scoped to queue/todo.md, state/CURRENT.md, and
  the two door receipts; a decision recorded elsewhere falsifies it.
- I ran arena_bench --selftest and load_ground_truth myself but did NOT run
  the four tripwire tests (the receipt claims 4 passed; unverified by me).
- Sibling seats are landing doors live (door 2 arrived mid-session); ranks
  here can be stale within hours.
- I did not evaluate the designs of the gated doors (three-signal embedding
  choice, weld ractive UX, consume-ledger flock semantics) beyond verifying
  their code premises; that is the design lens's seat, not mine.
