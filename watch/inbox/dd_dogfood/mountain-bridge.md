# DD-TO-MOUNTAIN BRIDGE receipt (gala lane dd-mountain-bridge, division B)

Date: 2026-10-03. Ask: what does the D&D corpus teach that the Mountain game needs?
Encounter design, loot tables, riddle mechanics, boss design, party dynamics. Name 3
concrete port moves from the DD corpus to the Mountain game.

## What was actually read (paths + lines, this seat)

Mountain game (the target):

- `mag/game_campaign.py` (5,099 lines, schema mag_game_campaign.v1, "engine owns truth"):
  archetypes fighter/rogue/wizard/cleric (`_ARCHETYPES`, mag/game_campaign.py:28), character
  traits `_TRAITS` at mag/game_campaign.py:36, room dicts with per-room `encounter` / `loot` /
  `hooks` / `flags_on_clear`, encounter HP/AC/attack resolution at mag/game_campaign.py:2590-2635
  (1d20+bonus vs AC, trait modifiers: hotheaded +1 bonus, craven nags), weighted table picker
  `_pick_weighted` at mag/game_campaign.py:1297, trait-reactive rest events `_fire_rest_events`
  at mag/game_campaign.py:1310-1351 ("if row.get('id') == 'omen' and 'craven' in traits"),
  storyteller crisis budget `{"threat_budget": 2, "days_since_crisis": 0}` at
  mag/game_campaign.py:355, and the zero-RNG table pick `_donjon_sense`
  ("one sensory atom, hashed to the room, no new geography", sha256 index into SENSORY_TABLES)
  at mag/game_campaign.py:485-504.
- `mag/game_world.py:79-99` (schema game_world.v1): the server-authoritative world core, every
  change folds as a content-addressed verkle knot.
- `mag/game_brawl.py` (schema mag_game_brawl.v1): the bar-fight carrier. Initiative
  `_roll_initiative` (mag/game_brawl.py:386), grapples `_try_grapple` (mag/game_brawl.py:522),
  absurdity detection `_classify_absurd_flavor` (mag/game_brawl.py:587), and the pressure line:
  `_ds_color_batch` packs each beat with `"color"`, `"pressure"`, `"motif"` (mag/game_brawl.py:815;
  fallback rows at mag/game_brawl.py:846-858: `"pressure": "The failed hunt still burns."`).
- `mag/game_dice.py:12` (`roll_dice`): deterministic dice notation with optional seed.
- The Godot port: `C:\Users\foste\Documents\projects\the-mountain\` (repo the-mountain,
  sibling of this estate checkout). `game/scripts/game.gd:8-14` header: the mountain routes
  water through valves, a siphon, and an XOR junction; steam law lifts water to the Crown;
  WIN = Crown to 4 units of 8 total. `game/README.md:22`: the XOR gate "passes only one inlet
  at a time - feed it from both and it pools", `p_bypass` siphon must prime 2 units. Pipe
  fracture law: full-bore stress past a deterministic djb2-hash threshold, permanent burst
  (game/README.md:42, AD1). Server: `server/` wire v0, SRP6 auth, persistence, anti-cheat
  ReceiptGate (RATE_CAP + STALE_NONCE), innkeeper bot, "minimal multi-room (`rooms.py`: one
  world + tick + innkeeper per room, capacity law)" (the-mountain/README.md:61), and "the Z1
  verdict-feed weld (each tick can mint a GWAP agreement payload into a sqlite capability
  ledger; dormant by default)" (the-mountain/README.md:55-57).

DD corpus (the reference), everything the estate holds on disk:

- `corpus/game_estate/DND_ACTUALPLAY_INTEL_20261003.md`: operator-pasted roster of the five
  actual-play shows (NADDPOD, Critical Role, The Adventure Zone, Worlds Beyond Number,
  Dungeons of Drakkenheim) + the fight-club notes: "Worlds Beyond Number and NADDPOD bring
  PvP to the table as a core feature"; cadence teaching = "scene pacing, cliffhanger
  placement, when the DM cuts a scene, how stakes escalate beat over beat (the estate's
  bar-fight pressure knob is the formalized version of this)". The file itself flags: no
  full transcripts on the desktop corpus, transcript hunt = librarian expedition pickup,
  this layer stays UNVERIFIED-PATH until bytes land. Treated accordingly: design-level only.
- `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/handoff/P2P_DND_ARCHITECTURE.md`
  (72 lines): "In D&D, the DM IS the frontier - the model that watches the state of play and
  steers the actors in real time. We don't bolt a 'monitor' on top; the DM is the monitor"
  (lines 12-14). Topology: per-node portal (human) + small AI player (cheap DeepSeek seat)
  around one shared verkle world, frontier DM watching all nodes (lines 19-26). Mapping
  table (lines 43-50): DM = game_dm.py, party = game_dm.party(), world = game_world +
  verkle, portal = game_portal.py. Core law: "same table, seats swapped" (line 52).
- `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/mag/dungeon_dev.py`
  (201 lines): "a DnD-style roguelite DUNGEON where every room is a CODING TASK, workers are
  the party, and conquering a room folds a knot that STRUCTURES the hologram" (lines 2-4).
  Rooms carry hp, floors, region mapping; `generate_room` / `assign_workers` / `conquer`
  (lines 108-176); conquered = a verkle knot folds, "the temple keeps that room for
  everyone, not a throne" (the campaign engine's conquer call at mag/game_campaign.py:2624-2631).
- `corpus/library/evennia/evennia/contrib/tutorials/evadventure/dungeon.py` (489 lines, the
  Knave-based EvAdventure tutorial): the `not_clear` room gate - "Each room in the dungeon
  starts with a Tag `not_clear`; while this is set, all exits out of the room (not the one
  they came from) is blocked. When whatever problem the room offers has been solved (such as
  a puzzle or a battle), the tag is removed" (lines 16-19), enforced by the exit lock
  `"traverse:not objloctag(not_clear, dungeon_room)"` (line 138) with the fail message
  "You can't get through this way yet!" (line 159). Depth-as-difficulty: "the dungeon's depth
  acts as a measure of the current difficulty level. This is the radial distance from the
  (0, 0) (the entrance)" (lines 292-295). Party mechanics: "you must all pick the same path
  from here ... or you'll quickly get separated" (line 467) - one branch instance per path,
  branch collapses after a week of idleness (lines 396-420).
- `corpus/library/evennia/evennia/contrib/tutorials/evadventure/random_tables.py`: "Random
  tables - adopted from _Knave_" (line 2), chargen_tables + `death_and_dismemberment`
  (line 618) - the table-as-data loot/damage tradition.
- `memory/game_modules/dnd_classic_stub.v1.json` (mag_game_module.v1, B2-shaped homage,
  "Original Mag structure. SRD tools for monsters/spells. Not B2 text."): 14 rooms tavern ->
  keep -> cave; per-room encounter dicts (barracks `goblin_scout` hp 7 ac 15 at line 148,
  claw_hall `goblin_band` hp 14 at line 221, `flags_on_clear` at line 233); key-gated loot
  (lord_solar holds `cave_key`); eight weighted event tables (tavern_rumor w 30/25/20/15/10,
  tavern_drink, random_road, random_woods, rest_safe, greedy_merchant, curveball_color,
  curveball_divert). This proves the estate's campaign engine already runs DD encounter +
  loot shapes; the Mountain port is a re-role, not a new build.
- `configs/riddler_domains.yaml`: the surrogate-domain grammar (fantasy_village constraint
  patterns: "only one traveler may cross the bridge at a time" -> sequential execution) -
  a riddle is a surrogated statement of a real constraint. (`canon/riddler_corpus/` is
  conspiracy-source material, Mystery Babylon / William Cooper - NOT game riddles; checked
  and excluded.)

## What the Mountain needs (the gap, byte-honest)

The Godot slice's whole verb set is movement, SPACE boil, E valve, R restart, H head law,
T terrain (the-mountain/game/README.md:18-25). Its dangers are deterministic physics
(fracture, STARVED) and its reward is tagged fish + Crown fill. It has no gated encounters,
no loot layer, no riddles beyond the implicit valve puzzles, no boss, and no cooperative or
adversarial party mechanics; the GWAP verdict feed that could carry them is wired but
dormant (the-mountain/README.md:55-57). The D&D corpus supplies exactly these five shapes,
and the estate has already proven three of them on the campaign engine.

## THE 3 PORT MOVES

### Port move 1: `not_clear` room gating + depth-as-difficulty (encounters)

DD teaching: a dungeon room is a GATE, not decoration. All forward exits refuse while the
room's problem stands (puzzle or battle), then the tag lifts; difficulty scales with radial
distance from the entrance (evennia dungeon.py:16-19, 138, 159, 292-295).

Port: the Mountain server's room layer gets the same law. Each room's tick declares a
problem from the graph's own state: a live fracture spray, a STARVED junction, or an unmet
Crown quota. While `not_clear`, `valve` and `boil` verbs that target the next room's pipes
are refused with the EvAdventure grammar ("You can't get through this way yet!") - the
refuse path already exists in protocol_table.py's ReceiptGate (gate-before-verb, typed
refusals; the-mountain/README.md:53). Depth = graph distance from `p_spring`, computable
from the water graph the server already ticks. Landing spot: `the-mountain/server/rooms.py`
(one world + tick + innkeeper per room, the-mountain/README.md:61) plus a `clear` predicate
on the welcome/tick snapshot. Precedent on this estate: dnd_classic_stub.v1.json already
carries per-room encounters with `flags_on_clear` (lines 148, 221, 233), and
mag/game_campaign.py:2619-2631 folds a `conquer` knot when an encounter drops - "the temple
keeps that room for everyone, not a throne." Same table, seats swapped: the Mountain's
encounters are hydraulic, so clearing a room = restoring the water (patch the fracture
downstream, feed the STARVED junction), which keeps the engine deterministic and the
encounter legal-by-physics.

### Port move 2: weighted loot/riddle tables with loss rows and trait reactions, picked zero-RNG (loot tables + riddle mechanics)

DD teaching: loot is a TABLE, not a bespoke reward: weighted rows with explicit ids, loss
fields, and character-trait reactions (dnd_classic_stub event_tables; evennia
random_tables.py "adopted from _Knave_" incl. death_and_dismemberment at line 618). The
campaign engine already runs the full pattern: `_pick_weighted` (mag/game_campaign.py:1297)
over rest_safe rows that `lose` inventory items, with trait sting lines ("As a greedy soul,
the missing ration stings extra.", mag/game_campaign.py:1331-1333).

Port: a `loot` + `riddles` block in the Mountain module spec, same shape as event_tables,
served off the water graph's own event feed. The Mountain's zero-RNG law is the constraint
that makes this clean: the pick is tick-keyed sha256 exactly like `_donjon_sense`
("one sensory atom, hashed to the room, no new geography", mag/game_campaign.py:495-504) -
index = sha256("loot:" + node + ":" + tick) % len(rows), same inputs, same mountain, same
loot, replayable like the wow_bones seeded Stream. Loot mints only off real physics events
(a boil on a node that just fractured sprays a vein pickup; a primed siphon yields a valve
charm) and lands in the player's hash-chained ledger row. Riddles reuse the riddler-domain
grammar: each riddle is a surrogated statement of a REAL graph constraint with the physics
as the answer key - the XOR junction is already one in the shipped text ("it passes only
one inlet at a time - feed it from both and it pools", the-mountain/game/README.md:22).
Landing spot: module JSON beside `the-mountain/game/` (or a `riddles` table in the server's
per-room data), served when a player first stands at a junction; solving = operating the
valve correctly, verified by the graph's own verdicts, so a riddle cannot be
brute-forced past the physics.

### Port move 3: the bar-fight register as a multi-tick boss over the dormant GWAP feed (boss design + party dynamics)

DD teaching: the operator's own fight-club notes - WBN and NADDPOD "bring PvP to the table
as a core feature" and teach cadence: "scene pacing, cliffhanger placement, when the DM
cuts a scene, how stakes escalate beat over beat (the estate's bar-fight pressure knob is
the formalized version of this)" (DND_ACTUALPLAY_INTEL_20261003.md:24-29). P2P
architecture: "the DM IS the frontier... the DM is the monitor" (P2P_DND_ARCHITECTURE.md
lines 12-14), party = per-node human + cheap AI seat around one shared world (lines 19-26).
The estate's formalizations already exist: game_brawl's initiative/rounds/pressure line
(mag/game_brawl.py:386, 815) and the campaign storyteller's crisis budget
(mag/game_campaign.py:355).

Port: THE DROUGHT - the Mountain's first boss, running on the Z1 verdict-feed weld that is
already on the wire but dormant (the-mountain/README.md:55-57). A deterministic drain pulls
1 unit from the Crown every N ticks (phases escalate beat over beat: trickle -> steady ->
burst, mirroring the fracture's own escalation grammar). Boss "HP" = the Drought's demand;
damage = the party's per-tick GWAP agreement_score with the already-designed roles Robber /
Cop / Witness + Blocker (KissKissBan, the GWAP payload schema in the-mountain/docs and
LANES_20260929.md L-SELF-2) - the boss is only hurt when the party's judgments AGREE, so
the DD party-dynamics law (must pick the same path or get separated, evennia
dungeon.py:467) becomes must-agree-or-do-nothing. The bar-fight pressure line renders boss
state in the HUD (one line heat per beat, the game_brawl `_ds_color_batch` shape), and the
innkeeper bot + AI companion seats take the party slots around the shared authoritative
world. PvP register for later: SOVEREIGN vs AUTHORITATIVE lobbies already give the
two-sides shape; the fight-club port is the Drought first because it needs no new netcode.

## Honest gaps and limits

- No WBN/NADDPOD transcripts exist on the desktop corpus; the actual-play layer is
  operator-attested design intel only (UNVERIFIED-PATH per the file's own flag and the
  no-fabrication law). Every quote above is from estate files that ARE on disk.
- The Godot slice has never been executed per the basecamp audit (LANES_20260929.md:
  "Godot slice: CODE-ONLY, never executed"); all Mountain-side mechanics here are cited
  from source bytes and READMEs, not play.
- No code was touched in this lane (mag/ or tools/ or the-mountain/): this is a design
  bridge + receipt. The violation ratchet therefore does not apply; nothing was pushed.

## Falsifiers

- Port move 1 dies if the Mountain server's verbs cannot be conditioned on room state
  without breaking the tick determinism (a refused verb must not perturb the water graph).
- Port move 2 dies if a tick-keyed sha256 pick makes loot feel scripted-repetitive in
  playtests (same row every session on the same node) - that is a design falsifier to
  check at the next playtest, not today.
- Port move 3 dies if GWAP agreement_score cannot be computed per-tick at the server
  without a frontier call (the Drought must stay deterministic; if agreement needs an LLM
  judge in the hot loop, the boss design changes).
