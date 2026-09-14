# MYCELIAL GAME BASECAMP — JOIN ATLAS

Date: 2026-09-01
Status: MAP BUILT · source corpus preserved · promotion remains gated by tests

This is the join map for the game corpus and the older fiction/basecamp machinery. It
answers one question: how does a piece of research become a playable, verifiable,
cache-efficient world inside Mag?

## 1. The climb in one line

`operator charter → L0 contract → L1 engine → L2 static → L3 cultural/variant pack → L4 instance → engine verifier → verkle receipt → narrative/render surface`

The LLM supplies interpretation and narration. The engine owns legal state, transitions,
terminal predicates, scoring, and RNG. A story can describe a move; it cannot make an
illegal move legal.

## 2. Basecamp regions

| Region | Purpose | Existing anchors | Exit receipt |
|---|---|---|---|
| Gatehouse | operator intent, spend, consent, stop | `docs/ref/OPERATOR_CARD.md`, `docs/ref/GAME_THEORY_PLAY_MAP.md` | bounded goal + budget |
| Contract forge | universal game vocabulary | `watch/corpus/L0_contract.md`, `watch/corpus/L0_universal_contract.DRAFT.md`, `watch/corpus/00_PRIMER.md` | six functions + schema hash |
| Engine foundry | reusable mechanics | `watch/corpus/L1_engines/` | engine fixture passes |
| Archive gardens | historical and cultural modules | `watch/corpus/L2_games/`, `watch/corpus/L3_packs/` | provenance + uncertainty labels |
| Story quarter | fiction, voice, campaign continuity | `memory/game/`, `memory/narrative_corpus/`, `campaigns/` | scene references a real state |
| Verkle observatory | truth, replay, lineage | `mag/game_world.py`, `mag/world_rib.py`, `mag/verkle_knot.py`, `memory/game/world/world_state.json` | state hash / knot receipt |
| Farm and theatre | cheap probes, salons, UI, model comparison | `mag/game_salon.py`, `mag/game_campaign.py`, `watch/WARGAMES_V0_SPEC_20260901.md` | cost, latency, quality, failure row |

## 3. Canonical layer map

### L0 — universal contract

**Meaning:** every game is represented as state encoding, initial state, legal moves,
transition, terminal predicate, and scoring. RNG is a protocol, never improvised prose.

**Sources:**

- `watch/corpus/L0_contract.md` — compact contract candidate.
- `watch/corpus/L0_universal_contract.DRAFT.md` — expanded draft.
- `watch/corpus/00_PRIMER.md` — charter, laws, and research context.
- `watch/GAME_CORPUS_UNIVERSAL_LEAD_20260901.md` — five-layer extension and RNG law.

**Join:** `L0 → mag/game_emulator.py + mag/game_world.py + verifier vocabulary`.

**Gap:** two L0 files exist. Before a public/canonical tag, designate one canonical
contract and keep the other as a derived or historical view; do not let agents choose by
filename.

### L1 — seven engine families

| Family | Source | Receives | Verifier obligations | State |
|---|---|---|---|---|
| race/dice | `watch/corpus/L1_engines/race_dice.DRAFT.md` | Ur, Senet, Patolli, Pachisi, Snakes & Ladders | seeded RNG, path legality, exact exit/finish | DRAFT / present |
| board strategy / capture | `watch/corpus/L1_engines/board_strategy.DRAFT.md` | chess, go, tafl and capture variants | slot-first capture, terminal predicate, king escape where applicable | DRAFT / present |
| sowing/capture | `watch/corpus/L1_engines/sowing_capture.DRAFT.md` | Bao, Kalah, Oware | sowing loop, capture delta, board conservation | DRAFT / present |
| constraint puzzle | `watch/corpus/L1_engines/constraint_puzzle.DRAFT.md` | Hitori, Kakuro, Nonogram, Sudoku | constraint satisfaction, uniqueness where claimed | DRAFT / present |
| narrative/RPG | `watch/corpus/L1_engines/rpg_engine.DRAFT.md` | D&D-shaped, 2d6, solo-oracle worlds | action legality, consequence/state continuity, oracle attribution | DRAFT / present |
| card systems | `watch/corpus/L1_engines/card_systems.DRAFT.md` | Riichi yaku, hanafuda, trick/deck systems | deck inventory, RNG conservation, scoring block | DRAFT / present |
| tile matching | card-system tile bridge + `watch/corpus/L2_riichi.md` | Mahjong/tile-deck descendants | tile inventory, draw/discard legality, hand scoring | bridged / not separately split |

The seventh family is currently a bridge, not a seventh standalone file. That is valid
only if the registry names the bridge explicitly; otherwise it will look like a missing
organ to the next mapper.

### L2 — game statics

| Static | Engine | Source | Reusable payload | State |
|---|---|---|---|---|
| Riichi mahjong | tile/card | `watch/corpus/L2_riichi.md` | tiles, calls, yaku/scoring, hand state | present |
| Nikoli grammar | constraint | `watch/corpus/L2_nikoli.md` | grammar and verifier vocabulary | present |
| Hitori | constraint | `watch/corpus/L2_games/hitori.DRAFT.md` | shading/adjacency constraints | DRAFT / present |
| Kakuro | constraint | `watch/corpus/L2_games/kakuro.DRAFT.md` | run sums and uniqueness | DRAFT / present |
| Nonogram | constraint | `watch/corpus/L2_games/nonogram.DRAFT.md` | line clues and exact fill | DRAFT / present |
| Sudoku | constraint | `watch/corpus/L2_games/sudoku.DRAFT.md` | 81-cell representation, exactly-one oracle | DRAFT / flagship candidate |
| Bao | sowing | `watch/corpus/L2_games/bao.DRAFT.md` | thin rule delta over sowing engine | DRAFT / present |
| Kalah | sowing | `watch/corpus/L2_games/kalah.DRAFT.md` | thin rule delta and commercial history note | DRAFT / present |

**Still missing as canonical L2 statics:** chess, go, tafl, and hanafuda. The complete
synthesis calls these queued; they must not be reported as complete until files and tests
exist.

### L3 — cultural and variant packs

These should be thin deltas over an engine, not duplicated rulebooks.

| Pack | Engine | Source | Historical caution |
|---|---|---|---|
| Royal Game of Ur | race/dice | `watch/corpus/L3_packs/ur.DRAFT.md` | distinguish ancient game from later tablet copy |
| Senet | race/dice | `watch/corpus/L3_packs/senet.DRAFT.md` | reconstruction uncertainty is a parameter |
| Senet GPT-OSS reading | race/dice | `watch/corpus/L3_packs/senet.gptoss.DRAFT.md` | alternate reading, not independent history |
| Patolli | race/dice | `watch/corpus/L3_packs/patolli.DRAFT.md` | source and reconstruction status remain visible |
| Pachisi | race/dice | `watch/corpus/L3_packs/pachisi.DRAFT.md` | regional/lineage distinctions preserved |
| Snakes and Ladders | race/dice | `watch/corpus/L3_packs/snakes_ladders.DRAFT.md` | later moral/game-commercial layers separated |
| Oware | sowing/capture | `watch/corpus/L3_packs/oware.DRAFT.md` | Akan ancestry and uncertainty must not be flattened |

`watch/corpus/L3_packs/SPORE_SEED_20260901.md` is a research seed, not a game static.
It belongs in the archive/research layer and should not inflate the game-pack count.

## 4. Fiction-to-engine joins

| Fiction/basecamp material | Mechanical home | What it contributes | Boundary |
|---|---|---|---|
| `memory/game/hero_journey.md` | RPG L1 + L4 campaign | scene voice, continuity, named objects | prose may narrate only state-backed objects |
| `memory/game/STORY_ORG.md` | RPG verifier / campaign logger | repair from frozen global verbs to room-local legal actions | every turn records room, legal set, result |
| `memory/game_modules/dnd_classic_stub.v1.json` | RPG static/instance seed | rooms, fighter, HP, objects, exits | homage stub, not claim of full 5e |
| `memory/game_modules/adventure_2d6_stub.v1.json` | RPG static/instance seed | 2d6 resolution and crossroads | engine must own roll/result |
| `campaigns/villains_guild/` | narrative campaign | quests, villains, authored setting | campaign choices become proposals/state changes only through engine |
| `campaigns/sunless_citadel/` | narrative campaign | alternate dungeon/world seed | separate instance lineage; no silent merge |
| `memory/narrative_corpus/` | story asset layer | Rashomon voices and reusable scenes | attribution and source status required |
| `memory/game/world/world_state.json` | authoritative world state | water-computer keep, current leaf | state hash is truth; narration is a view |
| `memory/game/maze.jsonl` | distillation/learning trail | many observations → compact invariant | derived map, not authority |
| `memory/rib_bus/castle-in-the-sky.json` | basecamp metaphor/route | climb, regions, organs, surfaces | map must point to live receipts |
| `outputs/CASTLE_IN_THE_SKY_CLIMB_MAP_2026-08-30.md` | prior climb map | inherited doctrine and unfinished joins | superseded by this join atlas where they conflict |

## 5. The operating loop

1. **Select a game row.** Registry supplies engine, static, pack, instance, role, and
   runtime. Clients do not own model weights or choose an unregistered static.
2. **Load the smallest stable prefix.** L0 + L1 are shared cache material; L2/L3 are
   deltas; L4 is ephemeral state.
3. **Generate or choose an instance.** Seed, board/hand encoding, and prompt hash are
   recorded before a model sees the task.
4. **Ask the model for a move/narration.** The model may propose; it cannot mutate the
   authoritative state directly.
5. **Verify deterministically.** Legal action, transition, terminal result, scoring, and
   RNG/deck/board conservation are checked by the engine.
6. **Commit the receipt.** Store prompt/model/runtime hashes, output hash, result, cost,
   latency, and verifier outcome; then fold the compact lesson into the atlas.
7. **Compare wavelengths.** Run the same frozen probes across models/runtimes. Agreement
   is evidence about the probe, not permission and not proof of truth.

## 6. Build order for the new basecamp

| Step | Build | Acceptance |
|---:|---|---|
| 0 | Canonicalize L0 and create one registry join schema | one canonical L0 hash; every entry resolves |
| 1 | Freeze L1 family interfaces and verifier names | each family has one fixture and failure vocabulary |
| 2 | Promote Sudoku as first end-to-end proving ground | generate → verify → meter → receipt; exactly-one oracle |
| 3 | Dock Riichi and Nikoli as cache/grammar comparisons | same L0/L1 prefix, distinct L2 deltas |
| 4 | Attach the seven L3 packs as thin deltas | source status/uncertainty/lineage in every pack |
| 5 | Add fiction as RPG/world instances | every narrated beat resolves to a state or is labeled fictional |
| 6 | Build the missing L2 statics: chess, go, tafl, hanafuda | files + fixtures + verifier receipts |
| 7 | Run the 50-variant pilot | per-layer cache hit, quality, cost, latency, and failure taxonomy |
| 8 | Farm the best bounded workloads | only after local/Bionic or approved burst runtime is verified |

## 7. What is complete vs what is merely present

**Present:** seven named engine-family documents, eight L2 game/grammar documents, seven
L3 game packs plus one spore seed, existing fiction/campaign assets, deterministic game and
verkle machinery, wargame specifications, and cache/wavelength research.

**Reported but not independently rechecked in this map:** the exact DeepSeek spend,
provider-side meter readings, and the synthesis document's registration event. Preserve
those as receipts, but do not substitute them for per-file hashes and executable fixtures.

**Not complete:** canonical L0 designation, structured engine→static→pack registry,
chess/go/tafl/hanafuda statics, a universal L4 instance schema, a single end-to-end game
farm run, and Bionic chat-model loading.

## 8. The basecamp law

**The map precedes the territory only as a hypothesis. The territory is the verified
state transition and its receipt.** Every new game or story must enter through the same
gate: source → contract → engine → instance → verifier → receipt → map.

