# lineage.md - the lineage lens on the 11 remaining build doors (2026-10-04)

Run: dwfrun-3b5af1ac (the ractor-engine wave the operator ordered after "actually
ractor it out self steal then go", per the sibling receipt
watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md header). Lens: lineage. Job: per door,
self-steal first, hostile pass on the falsifier, honest EV-per-hour order, cargo call.

Read this session: watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md (all 320 lines),
watch/inbox/GWAP_INDEPENDENT_COP_20261004.md, state/CURRENT.md,
tests/test_night_march_cure_20261004.py, tests/test_arena_bench.py (sibling, live),
mag/arena_bench.py:85-124, mag/lane_runner.py:905-949, mag/signals.py:75-130,
mag/model_health.py:1-60, mag/mycelium.py:178-200 + :262-280, mag/republic.py:105-150,
mag/flock_field.py:155-175, mag/swarm_tools.py grep, mag/mcp_server.py grep,
tools/__init__.py TOOL_MAP, tools/social_rsi.py grep, tools/gps_mcp/ledger.py:430-436,
watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:30-72,
watch/inbox/ESTATE_GAP_DIG_20261004.md:63,79 (grep). Commands run, all this session:
`.venv/Scripts/python.exe mag/arena_bench.py --selftest` -> exit 0, structured
verdicts PASS+FAIL, zero_human true; `.venv/Scripts/python.exe -m pytest
tests/test_night_march_cure_20261004.py -q` -> 6 passed in 2.08s; scoped greps named
inline below.

## Finding 1 - the queue is already two doors stale, and it silently lost the one
door with a MEASURED effort figure (CONVERGENT with the sibling landing)

The ask's 11 doors are not the receipt's ranked remainder. The primer's own table
(PRIMER_ADJACENT_24WIDE_20261004.md:233-249) ranks 13 rows; door 1 (independent-cop)
landed at bb0f34586, and door 2 (arena-bench CI tripwire) landed LIVE while this
lens ran: tests/test_arena_bench.py mtime 2026-10-04 12:35, untracked, receipt
watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md, and my own `--selftest` rerun exits 0
minting both a synthetic PASS and FAIL. The sibling also sharpened the diagnosis:
the bench was not "shape drift" but a 459-byte redirect stub left by the 2026-09-22
surfaces dedupe (canonical at dashboard/static/games/arrakis.html). Meanwhile EG-20
pass@K, ranked 3 in the table and the ONLY door whose effort figure is measured
rather than estimated (2h at spec, success meter "column present; predicts the mesh
vs frontier routing on one batch", watch/inbox/ESTATE_GAP_DIG_20261004.md:79, gap at
:63), appears nowhere in the 11. Second silent edit: clippy-as-prober sits at rank 7
in the table, gated on "same family schema" (decay family, :240-242), but the GWAP
receipt's closing line promoted it to next-door slot 2 with no gate named
(GWAP_INDEPENDENT_COP_20261004.md:82-83), and the ask inherited that order.
Falsifier: if the run owner or operator holds a postdating order that kills EG-20
and re-ranks clippy on record (ZMEM or sibling lane traffic, outside my greps), the
drop is a decision, not a loss; and if the sibling's arena-bench landing is
reverted, door 2 reopens. Move (15 min): strike doors 1-2 from the queue, reinsert
EG-20 at the top of the build order or bank its kill reason, and restore the
family-schema gate note on clippy.

## Finding 2 - night-cycle checkpoint legs is ~80 percent landed; its 2-4h sizing is
dead spend

The door's documented harm (the 5x CYCLE_FAIL full-cycle re-run, 2026-10-03) was
cured the same calendar night by the sibling night shift: cycle_night now trails the
CYCLE row BEFORE persisting last_night and _save_state is atomic tmp+replace
(mag/lane_runner.py:932-938, comment names the exact incident). I ran the tests this
session: 6 passed in 2.08s, including
test_cycle_night_trails_composite_even_when_state_write_fails, which reproduces the
Errno-22 shape and proves the completed-work record survives
(tests/test_night_march_cure_20261004.py:100-130). CONVERGENT: state/CURRENT.md:94
("night march honest-skip + atomic state saves") and the AGENTS.md census bullet
both bank it. What remains of the door is per-leg resume flags, and cycle_night is a
two-leg $0 composite (monitor + march, mag/lane_runner.py:911-931), so the residual
EV is minutes, not hours. Falsifier: post-cure repeat CYCLE rows in
queue/lanes/night/trail.jsonl after a failed state write would prove the re-run
class alive and restore the door (the trail now records it, so it is greppable).
Move (30 min cap): either park the door as cured or add the two per-leg flags; never
spend the receipt's 2-4h.

## Finding 3 - the decay family's vocabulary is half-built in the estate's own
bytes; the doors would rebuild it

SELF-STEAL, the lens's headline. The primer orders "define the decay/supersession
vocabulary once" before instantiating pheromone/mycelium/FSRS stores
(PRIMER_ADJACENT_24WIDE_20261004.md:216, :240-242) but cites no estate precedent.
Two exist. (1) mag/republic.py:114: Letter carries `superseded_by: int | None  # set
once, by supersede(); never edited` - the set-once supersession-pointer law, already
encoded, with the append-only trail alongside (:117 "append-only routing trail"); I
found no live caller of supersede() in mag/+tools/+main.py (grep this session), so
the organ is dormant, but the pattern is the estate's own tested encode of
supersession-not-deletion. (2) mag/signals.py already owns the metabolism math:
recency_decay (:82, docstring "Self-stolen from mycelium's 0.7^gap", tunable
half-life), wilson_lower (:44), a weighted fusion scorer combine() (:107-110), and
the proven_move Wilson gate (:118-126), consumed live by mag/model_health.py:41.
Meanwhile mycelium contradict() still bumps counters with no evidence link
(mag/mycelium.py:188-198) and decay() stamps a boolean with no successor
(:265-277), and valid_at/invalid_at have zero occurrences in live mag/ and
tools/gps_mcp python (scoped grep this session; the only superseded_by hits are
republic.py). The GPS ledger's 1/n running mean with momentum floor is confirmed at
tools/gps_mcp/ledger.py:430-436. Falsifier: a live supersede() caller or an
existing valid_at field anywhere in live code would shrink this further (grep says
no); if pheromone decay cannot key to an existing shift detector (drift patrol,
endpoint_news per the receipt :186), the distribution-shift reset half dies and
only alpha-decay survives. Move (one sitting, ~2h): lift republic's set-once
supersede pattern plus signals.recency_decay into the family schema, stamp
superseded_by into mycelium contradict()/decay() writes and lattice_edge.v1, and
pheromone metabolism then collapses to a ledger.py wire-up of recency_decay +
wilson_lower instead of new math.

## Finding 4 - monoculture proxy and MCP shim are wire-ups of existing rails, not
builds

Monoculture agreement proxy: tools/social_rsi.py already loads per-lane trails
(load_trails :134) and computes citation overlap (_needles/_needle_hits :251-264);
the door is one cross-lane agreement pass over those rails alerting
memory/attention.md, exactly lesson 23 exercise 2. MCP-lattice shim:
mag/mcp_server.py is wired and pin-gated (:21-23 pin gate, :341-350 drift filter)
serving tools.TOOL_MAP (tools/__init__.py:36-38 corpus_search family), with no
lattice tool in the map yet (grep this session) - so the shim is a grammar addition
after the receipt's own reconciliation pass, not a server build. Falsifier
(monoculture): if trail rows lack per-lane model identity, agreement cannot be
attributed to monoculture - check the trail row shape before building; (shim): if
agentmemory's grammar cannot pin to a tag, wire-not-build fails per the receipt's
own gate (PRIMER :57). Move: keep both doors but re-scope them as wiring; the 2-4h
estimates hold only if no new instrument is minted.

## Finding 5 - cargo call and the honest EV-per-hour order

Cargo (do not start before gates): consume-the-ledger (1-2 days; steer() verified
purely instantaneous this session, mag/flock_field.py:158-175, no social/best-row
term, and CTDE/p_best/belief_list grep zero in live code) and three-signal
query-broker (1-2 days; the embedding lane is genuinely unresolved - the estate owns
fusion math (signals.combine) and vector normalize (mag/bare_numpy.py:116) but no
text-embedding call site surfaced in my grep, so the recall@5 falsifier must run
before any build). Build-once calibrator stays behind its download-and-eval gate:
Gero-4B has no published evals (watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:32-46).
The weld door is now unblocked (door 1 landed, so banked scores mean something) and
is the only door that closes teach, verify, adapt on one surface, but at 1-2 days it
buys a re-verify of the beat_map substrate first (574 rows per the receipt, not
rerun this session). Honest order after doors 1-2: EG-20 (2h, measured) > monoculture
proxy (social_rsi rails) > family schema (Finding 3) > pheromone wiring > clippy-
as-prober > MCP shim after reconciliation > weld > the gated trio last.

## Blind spots

Not checked: the other lenses of this run (cross-lens convergence flags unseen);
beat_map rerun and the playground run dirs (weld substrate is receipt-carried);
external URLs (mem0, Letta, agentmemory, Gero card - all carried from receipts, not
refetched); GPS ledger row recount; queue/lanes/night/trail.jsonl post-cure re-run
audit; ZMEM and sibling lane traffic (where an EG-20 kill decision could live);
whether republic.py's Book store runs in the republic-os entrypoint (main.py:4253
exists, unwalked). The cargo verdicts are judgment on read evidence, not
measurements.
