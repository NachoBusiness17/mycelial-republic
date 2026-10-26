# THE MUSEUM, TRANSLATED INTO THE GAME LANGUAGE (2026-09-02)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: the museum is literally a place in game_world state (museum keys already present in museum.py's steal), and the stack-law-to-game-grammar table is the same machine named twice — UNPROVEN (source-read assertion; the 4-item build list is explicitly still assembly) · falsifier: museum.py/game_world state contains no museum keys, or the acquire/washed verbs land and the mapping breaks (a seventh ledger becomes necessary)
*Deep self-steal of HARNESS_SPEC.md + ARCH_GAME_MAP (39 organs, 5 strata) + museum.py's own steal
(STEAL_PLACE_REMEMBERS). Finding: the translation is not a metaphor — museum.py already keeps museum.*
keys in game_world state. The museum IS a place in the world; today we said its name in stack tongue.*

## THE TWO GRAMMARS, ALIGNED
| Stack law (today) | Game law (the salons) |
|---|---|
| BBS generates attention | **THE TAVERN**: players post intents; roasts are bard noise; gossip never mints kind |
| switchboard grants authority | **THE GOVERNOR**: sole committer; a steer is a signed intent; the tavern cannot authorize |
| effect broker causes side effects | **THE ENGINE**: only it mutates world state (engine owns truth; LLM narrates after) |
| verkle/ledgers keep receipts | **THE SAVE FILE**: deeds append; glances do not; the chain is the machine's actual memory |
| riddler-wash before crossing | **THE DISGUISE**: the artifact leaves wearing a mask; the decode map stays home (T0) |
| the museum (curated exhibits) | **A PLACE THAT REMEMBERS**: a room whose deeds are its inventory; exhibits are items whose provenance is their knot |

## EVENT KINDS (game nouns, no seventh ledger)
- `museum.acquire` — the curate verb: living art enters (Exhibit Zero: the poster)
- `museum.visit` — a glance read (free forever; render free, steer paid)
- `museum.cross` — an artifact leaves by the covenant's hand (the X crossing = a completed paid_intent quest)
- `art.washed` — the wash receipt: strip/scan/compile/nonce, the doorkeeper's stamp
- dual-channel zoning is the TAVERN/WAR-ROOM split: gossip in the tavern, steers in the war-room, physically separate queues

## THE CAST (org chart, in costume)
- governor = covenant personified — commits exhibits, refuses un-nonced art
- doorkeeper (new, small) = an invariant wearing a face: the riddler-wash gate; refuses items without nonce
- elder = design arbitration — the ballots on what the museum means
- Adam = taste + shipping — the museum's audience of one whose delight is the alignment signal; he shipped Exhibit Zero
- operator = covenant owner — the hand that carries art across the square
- Sancho = custody — the curator who carries, files, and signs (now also in-cage)
- the 48 unmined sessions = **unexcavated dungeon wings**: rooms whose deeds wait in the dark
- the attractor echoes = **ghosts in the strata**: rooms insisting on a deed until it becomes a gate

## CANON LAW (unchanged, restated in costume)
Rumor vs canon: a single-witness exhibit is a LEGEND (PROPOSAL); consensus-anchored + washed + countersigned
is CANON (committed by the governor). Contradictions resolve by hierarchy, never by the loudest bard.
The six tests are the trap level of this dungeon; model-layer isolation is the boss.

## BUILD (still assembly, now in the right language)
1. `museum.acquire` verb on mag/museum.py (curate living art) — commits museum_room.v1 leaves as world-state
2. `art.washed` = art_wash.py v0 (the doorkeeper), receipt = the wash kind
3. Door 1 page = the ROOM RENDERER (game_world_render/console_render grammar, lattice palette)
4. Door 2/3 = export adapters of the same world-state (Notion/HF/X read the projection, never the engine)
