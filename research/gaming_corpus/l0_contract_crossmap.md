# L0 CONTRACT CROSSMAP — game-contract grammar onto the fleet (harvester L0, vol-2)

Date: 2026-09-06 ~05:03Z · Seat: L0 (zcode harvest) · License: Picasso (operator)
Sources read fully: `watch/BASECAMP_GAME_ATLAS_20260901.md`, `watch/GAMES_CORPUS_PRIMER_SALON_SYNTHESIS_20260901.md`, `watch/corpus/L0_universal_contract.DRAFT.md`, `watch/corpus/L0_contract.md`, `watch/inbox/SHADOW_WALK_20260906.md`.
Cells: 7 posted to the TESUJI map (6 x G + 1 x A6), all SUPPORTED, seat=L0.

## 1. Six-function contract <-> TESUJI probe schema

| L0 function (DRAFT contract) | L0 fallback contract | TESUJI probe schema slot | Fleet engine twin |
|---|---|---|---|
| F1 STATE ENCODING (canonical string, `^`-flagged reprint) | `setup()` state + `render()` view | input / parser | state-hash in `world_state.json` |
| F2 INITIAL STATE (seeded, deterministic) | `setup(seed, players, opts)` | fixture bootstrap | seed recorded before model sees task (atlas loop step 3) |
| F3 LEGALITY (ambiguity -> hard false) | `legal(state, actor) -> [action]`, authoritative | expected / legal moves | `mag/game_emulator.py` verifier vocabulary |
| F4 TRANSITION (new canonical string; prose never alters it) | `move(state, actor, action) -> nextState \| ERROR` | transition | engine owns mutation, model proposes only |
| F5 TERMINAL (pack WIN rule; loop -> LOOP + prior hash) | `evaluate(state) -> VERDICT {PASS,FAIL,TIE}` | terminal | verifier reason codes |
| F6 SCORING (canonical fields alone) | evaluate + pack SCORE rule | scoring | receipt commit (atlas loop step 6) |

Cell: `G/L0/six-function-probe-schema` #39a3ef756e67.

## 2. Universal RNG protocol <-> roguelite seeds-from-data-hashes

L0 law: every draw is `TABLE[game-id][mode][seed-phrase][turn-index mod len]`; the model
reports, never rolls. Historical modes (astragali 1/3/4/6 unequal faces; Ur binary
tetrahedral 0..4 per BM 33333/Finkel, reconstructed; casting-sticks; cowries; marked-beans
with exhaustive reshuffle-reseed) all resolve seeded-external.

Fleet twin already live: shadow_walk NEW RUN seeds mulberry32 from
`fnv1a32(data_hash:run#)` — entropy anchored to the content hash, not model choice.
Convergent law spoken twice. Cell: `G/L0/rng-seeded-external` #157151cb3e02.

## 3. Primer salon's three amendments <-> fleet organs (each ALREADY IMPLEMENTED)

| Primer amendment | Fleet organ that already implements it | Cell |
|---|---|---|
| 1. build-row schema += `research_status / is_delta_over_engine / patch_owner` | `mag/grounding_wave.py` + `watch/GROUNDING_WAVE.jsonl` — hash-chained tri-state GROUND ledger: status per row (SUPPORTED/DISPUTED/UNPROVEN) with evidence path = research_status; seat field = patch_owner; the L1->L3 thin-delta layer law + DRAFT/builder-original headers = is_delta_over_engine | `G/L0/amendment-1-research-status` #784749703998 |
| 2. Rule-7 patch governance (who amends a byte-stable static once metered; K_T2 qualifier) | the verkle chain — append-only signed knots; a patch is a NEW knot citing the elder (v2-anchors-into-v1); PROMPT-BODY-START byte-stable block + epoch-pinned instruction layer; cross-chain citation IS the K_T2 qualifier (appended-below growth that cites its parent is not drift) | `G/L0/amendment-2-rule7-governance` #780f31658994 |
| 3. legal-acceptance meter beside the cache-hit meter | `mag/cite_gate.py` — deterministic primary-source verify BEFORE rightsize, cite-rate 100% falsifier, deliberately independent of `mag/refeed_guard.py` cache economics: two dials, exactly the primer's split. `mag/game_emulator.py` is the same meter for moves | `G/L0/amendment-3-legal-acceptance-meter` #d3103fc9638a |

Bonus cells: `G/L0/canonical-restatement-hash` #ef27fb67d518 (state-hash-is-truth /
narration-is-a-view; UNKNOWN-RULE = tri-state refusal), A6-adjacent
`A6/shadow-walk/l0-room-contract` #a398bf7796f9 (fog-of-war = UNKNOWN-RULE; no-hash-no-draw
fnv1a32 gate = hard-false legality; the walkable room spec inherits the six-function
contract: manifest=encoding, hash gate=legality, run seed=terminal, vision-gated JIT=render).

## 4. Receipt

- `python -m mag.tesuji_map verify` -> PASS 155 cells, chain intact, tip=15f4290fad22 (2026-09-06T05:05Z, final check before slot release).
- 7/7 L0 cells present (seat=L0 filter), all SUPPORTED, zero DISPUTED/UNPROVEN.
- Incident 1 (found + repaired): pre-existing row 126 (codex `G/engine/narrative/mud`)
  cited `training/events.jsonl` — path dropped its `memory/` prefix; the artifact is
  `memory/training/events.jsonl` (125 MB, live). Note fixed, rows 126+ re-chained.
  Pre-surgery backup: `watch/TESUJI_MAP.jsonl.bak-20260906-L0` (135 rows, pre-repair state).
- Incident 2 (lost update, live race): this seat's first two cells (hashes #0cc80c0ab1ee,
  #096cb62d7959, posted ~04:57-04:58Z) were overwritten by a concurrent baroque-seat
  batch write to the same ledger in the same window; baroque rows 133-135 landed in their
  place. Reposted both cells (fresh hashes above). Lesson: `post()` is append-mode but a
  sibling seat is doing read-modify-write rewrites — the tesuji ledger needs the same
  concurrency-slot discipline the `_conc_test_slot` protocol gives workers, or an
  append-and-fsync-only writer per seat.
- Incident 3 (verify broke again post-harvest, fixed without ledger surgery): new codex
  row 154 cited `memory/percolator/invariants.json.bak`; the real artifact is
  `invariants.json.bak-20260902`. With codex appending live (5 rows/min), a read-modify-write
  repair risked another lost update, so the cited path was materialized as a copy of the real
  backup instead. Lesson stands: tesuji post() needs per-seat append discipline.
- Slot protocol honored: `mag._conc_test_slot start L0` / `end L0` (released=True).
