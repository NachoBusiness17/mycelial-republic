# MOONSHOT-1: the eleven remaining doors, self-stolen and repriced (2026-10-04)

Lens: moonshot-1 (no sacred cows, including the 24-wide receipt and its reviser
order). Ask: per door, self-steal first (what the estate already holds), hostile
pass on the falsifier, honest EV-per-hour order, cargo call. Everything below
was checked this session by me (commands named inline) or is marked receipt-
carried. Read first: watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md (full 320
lines, door table at :229-249) and watch/inbox/GWAP_INDEPENDENT_COP_20261004.md
(door 1 landed as bb0f34586). state/CURRENT.md read in full.

## The one-sentence verdict

The reviser order is a hygiene ladder written from lane snapshots that the tree
has already moved past: one of its top-5 doors is cured on-disk, another's
premise does not reproduce, a third is a registry edit wearing a 4-8h ticket -
while the only door that produces anything a learner touches sits at rank 11
with its named gate already cleared.

## Door-by-door self-steal table (all checks run this session)

| Door | Self-steal verdict | Evidence I checked |
|---|---|---|
| arena-bench CI tripwire | SURVIVES but premise STALE and cost collapses 1-2h -> ~30min | ran `.venv/Scripts/python.exe mag/arena_bench.py --selftest` -> exit 0, JSON verdict "FAIL" (computed at mag/arena_bench.py:323, threshold 0.9), NO ValueError at :102; `git grep -n "arena_bench" -- tests/` -> zero hits (scoped: tracked tests/ only) |
| clippy-as-prober | SURVIVES; state organ is genuinely new, delivery vehicle is not | `git grep -n -i -E "fsrs|spaced.?repetition|retrieval.?state|free.?recall" -- mag/ tools/ main.py tests/` -> only a Godot binary false-positive; but tools/zknot.py:53-54,:198-209 already runs a self-steal+forgot per-1000-prompts METER - the probe delivery surface exists |
| night-cycle checkpoint legs | CARGO (pre-empted on-tree) | mag/lane_runner.py:932-938 carries the 2026-10-04 trail-BEFORE-persist cure comment for the exact 5x-CYCLE_FAIL class; tests/test_night_march_cure_20261004.py:100-128 pins cycle_night state-write behavior |
| monoculture agreement proxy | GATED CARGO until a second funded family exists | commit 03da1ee56 ("grok-4.7 403 unfunded noted"); AGENTS.md driving ladder: only Nous primes + xAI funded; `git grep -n -i -E "agreement|overlap|monoculture" -- tools/social_rsi.py` -> zero (scoped) |
| pheromone metabolism | HALF-EXISTS: door shrinks to time-decay + shift-reset | tools/gps_mcp/ledger.py:430-443 already runs a momentum FLOOR ("a fail absorbs (rate unchanged), it never rewards") over the 1/n mean at :433; momentum derived from verdict_log window at :80-87 |
| mycelium-v2 bi-temporal | SURVIVES as specced | mag/mycelium.py:183 ("jsonl is append-only; replace by rewriting the file") and :188-198 (contradiction = counter bump, no lineage) re-read this session |
| MCP-lattice shim | COST COLLAPSES 4-8h -> ~1 sitting: registration, not a build | mag/mcp_server.py:226-252 (manifest is generic over tools/_FN + TOOL_MAP filtered by ROLE_TOOLSETS at :67), :308-321; `git grep -n -i "lattice|context_pack|build_context" -- tools/__init__.py` -> zero (scoped: the callables are simply not registered yet) |
| three-signal query broker | PARTIAL: two of three signals exist; broker organ exists too | mag/lattice_query.py (query_by_theme/neighbors/summary/graph_viewport, no FTS/embedding) + catalog FTS live; tools/estate_query.py already fuses provenance surfaces by corr_id (ran --help this session: trajectory/burns/duels -> one timeline); only the embedding lane is new |
| weld door (beat ractive) | SURVIVES and its gate CLEARED | cop fix landed bb0f34586 (GWAP receipt: "9 new tests, 65 gwap-surface green" - receipt-carried, not rerun by me); beat_map 574 deterministic rows at tools/beat_map.py:139-172 (receipt-carried; file present) |
| build-once calibrator (Gero-4B) | GATE HOLDS; cheaper eval-first surface exists | watch/inbox/X_INTEL_PROPER_SCORING_20261004.md:44-45 "No published evals on the card"; :75-78 names tests/test_concept_predictor.py as the in-estate probability organ to eval on first |
| consume-the-ledger wire | SURVIVES as specced | `git grep -n "ledger|gps" -- mag/flock_field.py` -> zero hits (scoped: mag/flock_field.py) |

## Findings

### F1. The reviser order ranks two doors on tree states that no longer exist

The receipt's ranks 2-4 (its own "then" items) rode lane snapshots taken before
same-day cures landed. Night-cycle checkpoint legs (rank 4, 2-4h, "documented
5x re-run class") targets a class the tree already cured on 2026-10-04: the
composite is trailed BEFORE persisting last_night so a state-write failure can
no longer void the cycle (mag/lane_runner.py:932-938, the comment names the
exact 2026-10-03 5x-CYCLE_FAIL incident), and
tests/test_night_march_cure_20261004.py:100-128 pins it. What remains of the
door is a per-leg guard (skip monitor if it already ran today) - a ~15-minute
if-clause, not a 2-4h build. Arena-bench tripwire (rank 2) claimed a live
ValueError at mag/arena_bench.py:102 from an empty GATES parse; I ran the
instrument: `.venv/Scripts/python.exe mag/arena_bench.py --selftest` exits 0
and emits a computed verdict FAIL (verdict logic at :323, threshold 0.9,
weights_sha256 printed). The bench runs end-to-end today; the breakage the door
cited is gone. The tripwire itself is still owed (zero test references,
scoped-grep named above) and shrinks to a ~30-min pin: assert selftest exit 0,
ground-truth keys present, parse count > 0. The receipt's synthesis lane wrote
door evidence without re-running it against the moving tree - the exact
hand-copied-count disease AGENTS.md's census bullet polices. This is
CONVERGENT with the receipt's own honesty section (its gwap chain 559->589
drift between lane and reviser moments), and it generalizes: every door's
evidence is a snapshot with a moment, and the build order was priced off
moments hours stale.

Falsifier: if the selftest raises on a fresh checkout, or
test_night_march_cure_20261004.py fails on this tree, both doors stand as
sized. Move (45 min): strike night-cycle to a 15-min guard ticket, land the
arena-bench pin test, re-price the ladder.

### F2. The MCP-lattice shim is a registry edit wearing a 4-8h ticket

mag/mcp_server.py is not a server you extend; it is a manifold over the estate's
callables: _load_tool_functions() pulls tools/_FN + TOOL_MAP (:226-242),
_profile_names() intersects ROLE_TOOLSETS (:245-252, the dict at :67), and
tools_manifest() compiles name/description/schema from live signatures
(:308-321) - "the registry stays compiled-from-code: signature drift updates
the schema" (:258-259). The door's 4-8h estimate (post-reconciliation) is
priced against building server plumbing that already exists. The lattice
callables are simply not registered yet: my scoped grep over tools/__init__.py
for lattice/context_pack/build_context returns zero. The wire-not-build version
of this door is: add lattice_query + context-pack functions to the tool map,
add one ROLE_TOOLSETS profile, pin a tools/list test. The agentmemory
memory_recall grammar (token_budget, format) is then wrapper callables in the
same registry - parameters, not protocol.

Falsifier: if the lattice/context-pack callables cannot be registered without
breaking the server's stdlib-only discipline (the lazy-import posture at
:336) or the grammar genuinely needs protocol work, the original sizing
returns. Move (1 sitting): registration + pin test, before any reconciliation
pass on agentmemory's grammar.

### F3. MOONSHOT SWING: the order parks the product behind gates that are open

The reviser's own falsifier for the whole Primer thesis is that "a primer that
only entertains is a soundtrack; the property that makes it a Primer is the
verification ractive closing the loop" (X_INTEL_PRIMER_20261004.md:55-57,
receipt-cited in the primer chapter). The weld door - the only door that
produces an artifact a learner plays - is ranked 11th of 13, gated on "needs
the cop fix so its banked scores mean something." The cop fix LANDED (commit
bb0f34586; GWAP receipt read this session: honest verdict shape VERIFIED_AGREE
161 / CHALLENGE 88 / DISPUTE 64 / BLOCKED 216 over 529 payloads). The gate is
open and nobody re-ordered the ladder. Meanwhile ranks 2-8 are all
infrastructure nobody outside the estate will ever perceive: tripwires,
meters, decay plumbing. The 10x version of this build order starts the weld
TODAY in parallel with the cheap pins, because (a) its inputs are live
(beat_map's 574 deterministic damage rows, arena banking v3-cop scores), (b)
its 1-2 day cost is half one decay-family instantiation, and (c) every other
door's value is conditional on there being a learner - which only the weld
creates. The current order optimizes for zero-risk maintenance and calls it a
build order.

Falsifier: 30 days after the weld lands, if zero quiz/challenge attempts are
banked by any seat other than its author, the ractive is demo theater - then
wire it into clippy's session-start surface (F-move below) or kill it.
Move (start now, parallel): beat-indexed challenge harness over beat_map rows,
banked through arena_gwap v3.

### F4. Pheromone metabolism already has its slash; what is missing is only time

The receipt's headline "all memory, no metabolism" cites the 1/n running mean
(tools/gps_mcp/ledger.py:433, re-read this session). Four lines below the
cited line sits the un-cited metabolism: a momentum floor where a fail
absorbs without reward and the rate is floored at the window-start rate when
momentum is rising (ledger.py:434-443), with momentum derived from the
verdict_log window (:80-87). So dispute-streak slashing - the door's second
named feature - partially exists. The genuinely missing pieces are exactly
two: a time half-life on stale measurements and a drift-patrol-keyed
distribution-shift reset (the README's own growth item 2,
tools/gps_mcp/README.md:229-231, receipt-cited). Both land on the existing
momentum module without touching verdict_log (LM7 forbids that edit,
STEERING_FIELD_THEORY.md:147-148 receipt-cited). The door is real but is half
the 4-8h ticket.

Falsifier: the L19 catastrophic-drift experiment - if a half-life + shift-reset
on momentum cannot recover a poisoned task_shape row in that experiment shape,
the metabolism door's mechanism is wrong. Move (~2-4h): updated_at half-life +
drift-keyed reset on the momentum module, falsifier run banked.

### F5. The monoculture proxy is cargo until the xAI key reissues - spend the ticket on the probe

A cross-model agreement-rate proxy needs two models that can disagree. The
estate has exactly one funded judgment family (Nous primes; AGENTS.md driving
ladder) and the second (grok-4.7) is 403-unfunded with a reissue thread open
(commit 03da1ee56). social_rsi.py carries no agreement/overlap surface today
(scoped grep, this session). So the door's cross-model leg measures nothing
now and would permanently read "monoculture confirmed" - an alert that always
fires is not an instrument. Its fallback leg (citation overlap across lanes of
one dig) is real but weaker than the door claims: shared sources are
correlated evidence, not correlated error. Meanwhile the clippy-as-prober
door (same 2-4h price) builds the estate's only missing retrieval-practice
state (my FSRS/spaced grep over mag/+tools/+main.py+tests/ returns zero,
instrument named) and self-steals its delivery surface from the zknot meter
(tools/zknot.py:198-209) - it converts a recap the seat already reads into
the retrieval condition the curriculum science says wins. That is where the
2-4h goes.

Falsifier: the xAI key reissues or CACHE_LANES gains a second free family
(state/CURRENT.md owed list) - then the monoculture door revives at full
value with a real second family to measure. Move: bank a two-line failure-KB
row "monoculture-unmeasurable: one funded family, key 403" and build the
prober instead.

## Honest EV-per-hour order after re-pricing (replaces receipt ranks 2-13)

1. arena-bench pin (~30 min, F1) - cheapest, evidence stale but tripwire owed.
2. MCP registry shim (~1 sitting, F2) - before any grammar reconciliation.
3. clippy-as-prober as a zknot extension (2-4h, F5) - starts the FSRS bank.
4. WELD DOOR, started now in parallel (1-2 days, F3) - the product swing.
5. pheromone time-decay + shift-reset on momentum (~2-4h, F4).
6. mycelium-v2 bi-temporal (4-8h, unchanged) - decay-family schema first.
7. three-signal broker, embedding lane only (the other two signals + the
   provenance broker already exist; recall@5 falsifier before any fusion).
8. build-once calibrator, eval-first on concept_predictor before any download.
9. consume-the-ledger wire (1-2 days, semantics change, last).
Cargo: night-cycle checkpoint legs (cured on-tree; 15-min guard at most);
monoculture agreement proxy (gated on second funded family).

## Blind spots (honest)

- I did not rerun the gwap test suite; "65 green" and the 529-payload census
  are receipt/commit-carried, not re-derived.
- My FSRS/spaced-repetition absence grep covered mag/, tools/, main.py,
  tests/ only - .agents/skills/, corpus/, and the ZMEM harness store were
  outside my instrument; a skills-dir spaced-repetition implementation could
  exist unseen (the receipt's lanes had the same scope).
- Gero-4B not downloaded, not evaled; the calibrator's gate stays unmeasured.
  agentmemory's server.ts grammar bytes not read by me (receipt-cited only).
- The playground dnd0/tavern run dirs listed empty under cmd `dir /b` - I
  could not confirm their contents; the weld door's runtime evidence is the
  GWAP receipt's playground claim, not my own run.
- arena_bench's current verdict FAIL (vs threshold 0.9) is undiagnosed - one
  run, no deep read; I do not know if it is honest capability reporting or
  ground-truth drift. The pin test must assert parse health, not PASS.
- EG-20 pass@K (receipt rank 3, the only measured-effort door) was excluded
  from my eleven-door ask; I did not investigate why it left the list.
- No external web verification this session; mem0/graphiti/agentmemory/
  Gero-4B facts are receipt-carried.

Writer: moonshot-1 (subagent, dynamic workflow run). fetched: 2026-10-04.

## HOSTILE-PASS CORRECTIONS (2026-10-04, second pass; three findings weakened, re-checked)

CP-1 (was F1, split). The arena-bench prescription is REDUNDANT - the tripwire
landed at commit 00cb15c77 (2026-10-04 12:39:31 -0400, tests/test_arena_bench.py,
receipt watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md, existence verified by ls)
four minutes before this file's first write; I re-ran the suite this pass:
`.venv/Scripts/python.exe -m pytest tests/test_arena_bench.py -q` -> 4 passed in
1.50s; grep now 6 hits in tests/test_arena_bench.py (my earlier zero was true at
its moment, stale at filing). My selftest exit-0 ran on the sibling-REPOINTED
tree (the commit names the real defect: static/arrakis.html was a 459-byte
redirect stub since the 09-22 dedupe, canonical at games/arrakis.html, the bench
"raising honestly into the void for 12 days") - I misread a mid-session sibling
fix as organic staleness. The night-cycle "CARGO (pre-empted)" verdict is
WITHDRAWN: what landed is observability (trail-before-persist,
mag/lane_runner.py:932-938), not the door's deliverable - the gate is still
day-granular last_night only (re-verified at :919-920), no per-leg flags, so a
failed state write still re-runs monitor+march, now visibly. Door verdict:
survives, urgency reduced.

CP-2 (was F2). The manifold facts stand but the equivalence dropped the door's
named deliverable and inverted the receipt's gate order. Byte-verified this
pass: agentmemory's memory_recall grammar at library_parked/agentmemory/src/mcp/
server.ts:84-113 (format full/compact/narrative with 400-validation,
token_budget positive-integer validation, limit default 10, optional agentId);
the reconciliation-before-building gate at watch/inbox/
X_INTEL_AIENG_SCRATCH_20261004.md:92-94 verbatim ("The lattice spec owes a
reconciliation pass against it ... BEFORE any lattice building starts - the
wire-don't-build law"); the wrong-path citation at :89 ("memory/mcp-lattice
spec-seed") still uncured. Corrected claim: the registry edit is a cheap first
slice AFTER the reconciliation, not the door; the citation cure (~2 min) can
land immediately regardless.

CP-3 (was F3, mechanism REVERSED). The momentum floor is not slashing - it is
LM7 positive-steering ANTI-punishment protection. Docstring re-read verbatim
(tools/gps_mcp/ledger.py:78-97, receipt last_mile_20260930/LM7_POSITIVE_GPS.md
named inside it): "while a pair is RISING, a FAIL verdict never demotes
pass_rate below it (the fail still lands in verdict_log; it logs, it does not
punish). A fail can never RAISE the meter either (clamp is min(floor, pre-fail
rate)), so there is no Goodhart surface where a fail pays." The only streak
logic is a PASS-streak badge (MOMENTUM_STREAK_BADGE_MIN = 3, :113) -
reward-side. "Half price" WITHDRAWN. Sharpened finding: the pheromone-
metabolism door is partially working AGAINST an explicit operator steering law
- any fail-streak slashing reopens the Goodhart surface LM7 closed - so the
door is design-gated on an operator ruling (decay must be time-keyed and
reset-keyed only, punishment-free) before its 4-8h. The 24-wide receipt cited
the LM7 verdict_log clause but missed this docstring 60 lines above its own
:433 cite.
