# RACE + SOWING ENGINES → THE FLEET (harvest, race-sow seat, 2026-09-05)

Picasso license: harvest all, map to each other. Sources: `watch/GAME_MECHANICS_LATTICE_20260903.md`
(RACE row = "patience law: queue is position, the throw is the tide"; SOWING row = "distribution:
resources planted in one pit feed three"), `watch/BASECAMP_GAME_ATLAS_20260901.md` (both engines
DRAFT/present), engine specs `watch/corpus/L1_engines/race_dice.DRAFT.md` +
`watch/corpus/L1_engines/sowing_capture.DRAFT.md`. Fleet organs: `mag/concurrency_gate.py`,
`mag/_conc_test_slot.py`, `mag/percolator.py`, `mag/refeed_guard.py`, ledger `watch/TESUJI_MAP.jsonl`
(6 cells posted, #62c6dcf5..#28a66f31).

The lattice's claim holds both directions: the concurrency runs ARE a race engine, and the
percolator IS a sowing engine — neither needed retrofitting, only naming.

## RACE — the patience law (queue is position, the throw is the tide)

Engine (race_dice.DRAFT): track of ordered squares (linear or ring); pieces advance in fixed turn
order; move amount comes ONLY from the seeded RNG, never chosen or narrated; per-square effects in
a fixed resolution order; bear-off requires an exact landing (land-exact/roll-exact — overshoot is
clamped or the roll ignored).

| Cell | Engine mechanic | The fleet process it IS | Room-spec line for shadow_walk |
|---|---|---|---|
| `G/engine/race/track-turn-order` | ordered-square track, fixed turn order, squares concurrent-or-blocked per pack | the group-of-five concurrency probe: `concurrency_gate.py` leases numbered slots (the squares), `_conc_test_slot` START/DONE rows are the turn order; 5 walkers, 3.75x, 0 losses — the track holds five pieces at once | The Gate corridor: five visible slots, each walker a piece standing on its leased square; occupancy and turn order render live from the slot lease files. |
| `G/engine/race/seeded-throws` | move amount ONLY from seeded RNG — the throw is the tide | lane capacity is the throw: 1400/day clamp, weekly resets, groq refill ~01:10Z, 09-05 receipt (49% left by midday); batches ship at the tide's size, not the walker's preference | The Tide gauge: today's remaining quota rendered as the dice count; oversized turns are clamped roll-exact at the gauge, never argued. |
| `G/engine/race/bear-off-exact` | bear-off on exact landing; overshoot clamped/ignored | the verify gate: a DONE row crosses the finish only on exact evidence (hash-chained ledger row, verify PASS); unverified claims overshoot and return to stock — one builds, one verifies | The Final Square: accepts only a hash as the exact roll; an unsupported claim lands one short, visibly stuck, until the verifier rolls true. |

## SOWING — the distribution law (planted in one pit feeds three)

Engine (sowing_capture.DRAFT): ring of pits; lift the full count, sow one seed per successive pit;
capture fires only when the LAST seed lands in an empty own-side pit opposite a 2/3, then
backward-chains; win by store count; RNG-negative by construction; the feeding rule forbids
stripping the board and a sow never lands in its own store.

| Cell | Engine mechanic | The fleet process it IS | Room-spec line for shadow_walk |
|---|---|---|---|
| `G/engine/sowing/sow-one-to-many` | one pit's full store re-deposited across the ring, one seed each | the corpus itself: one canon (Murray 1952, seven families) sowed into 7 engines x 47 invariants (~329 lawful rooms, no new content); one harvest artifact feeds noise file + invariant registry + explore queue + room spec in one pass | The Seed Lift: the chamber takes one planted artifact and must show >=3 pits it feeds; fewer than three and the turn does not count. |
| `G/engine/sowing/end-of-sow-capture` | capture only at the last-seed landing, then backward-chain | the percolator's REPEAT -> invariant compile: novelty is sowing (spread, nothing captured); a repeat landing on the registry's empty slot compiles an invariant via fact_bus, and the backward chain sweeps related priors in the same fold | The Capture Row: per-step motion renders free; the only scored moment is the last seed's landing — repeat hits flash captured and chain backward through adjacent prior slots. |
| `G/engine/sowing/anti-sow-refeed` | inverted: feeding rule + sow-never-lands-in-own-store (conservation structural) | the refeed guard as the ANTI-SOW: 122M input vs 0.5M output = a session sowing its own pit back into itself; the guard measures the store-ratio and gates Lite re-arm on the verdict | The Anti-Sow clause: the chamber forbids any turn whose harvest re-feeds only itself — a pit that feeds no neighbor reads REFUSED, measure-or-no-move. |

## Sharpest mapping

The refeed guard is the sowing engine's conservation clause run as a sentinel: mancala already
codified the fleet's one measured tax (94% of input is re-fed cache reads — seeds that never leave
the sower's hand) as "a sow never lands in the store." The engine knew in 1300 AD what the pool
lost 122M tokens learning.

Bank receipt: 6 cells SUPPORTED on `watch/TESUJI_MAP.jsonl` (seats race-sow, chain intact
#62c6dcf56046 -> #28a66f314881).
