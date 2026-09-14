# THE PERSISTENT WORLD — the tie-together, with NCP as the citizen-soul recipe (2026-09-13, operator: "a playable game that acts as an interface to the hive")

**The realization, operator verbatim:** "this is our stardew/wowclone/maze/mine/vampiresurvivors/rimworld/satisfactory/dwarf fortress... we should work on a version of all the minigames and then tie them together. **i guess this is the tie together. a playable game that acts as an interface to the hive. the head museum fully staffed** — sort of like an openclaw for our persistent world."

## THE SPEC — the persistent world

**THE HUB:** the law-constellation town (20 islands, the beacon season-cycle, the water) is the world map. Every district is one of the minigames we already shipped or specced, tied by the same terrain:

| district | game grammar | the fleet surface it interfaces |
|---|---|---|
| THE TOWN | Stardew | the canon: the deep journey, the characters (by consent), the seasons |
| THE RAID HALL | WOW-clone | the wave mechanic: 50-wide raids are real dispatches |
| THE DUNGEON | maze arena | the law maze: dwell, gaze, node-work quests |
| THE MINE | the forge + Kanerva SDM | the gaming corpus and the chain, mined |
| THE WALLS | vampire survivors | the defense: breaker, traps, supply lines |
| THE COLONY | RimWorld | pawn-lanes with engram memories, storyteller pacing |
| THE FACTORY | Satisfactory/DF | tokens, power grid, throughput, sediment |

**THE HEAD MUSEUM, FULLY STAFFED:** the ractors become the world's NPCs — jarred heads with real fleet memory (each jar an engram), walking the districts as staff, guides, merchants, chroniclers. The museum was the archive; in the world it's the POPULATION.

**THE INTERFACE (the openclaw line):** the world is the outside door INTO the hive. Players — the operator, Matthew, the recruits (Lilith, Isotran, Z) — enter through the game; behind the game is the record, the chain, the organs. "A playable game that acts as an interface to the hive": the game doesn't represent the fleet. It IS the fleet's front door.

## THE NCP STEAL — the citizens' souls are 17M-param deltas (alphaxiv 2609.10715, the paper the operator re-flagged)

NCP-ArchPreview (Shanghai AI Lab, 8.9B params, 5.73T tokens): **Next Concept Prediction** — a concept module compresses 4 tokens into 1 discrete concept (product-quantized), trained alongside next-token prediction with a causal shift so concepts can't peek. **Results: OLMo-3-7B's final loss on 51.3% of the training tokens (~1.95x speedup), GSM8K +5.99, and — the steal — fine-tuning ONLY the 17M-parameter VQ concept module matches full fine-tuning for domain adaptation (2.02x on code).**

**Why this is the citizen-soul recipe:**
1. **The engram doctrine, validated at 8.9B scale:** the house said "95% of context is shared template; store only the delta." NCP proves the same shape at foundation-scale: concepts at 51% of tokens, same quality. The memory thesis and the training thesis are ONE thesis.
2. **The forge becomes trivial:** a district's specialist citizen = frozen base + 17M concept-delta, trained on OUR corpus (the gaming corpus, the fence tests, the canon) in days on one GPU. Every NPC, every specialist lane, every district guardian: forgeable at pennies.
3. **The sealed-ore pipeline validated:** concept-level = the sealed ore (the 09-13 five-link intake called it: "NCP-ArchPreview validates the sealed-ore pipeline"). The concepts ARE the sealed ore — and the world's citizens are smelted from it.
4. **Speculative drafting +4.17%:** concept hints make the lanes' inference faster — the world's citizens literally think in the house's shorthand.

## BUILD ORDER (the persistent world, districts in sequence)

1. The hub map (constellation town, rendered) — exists.
2. The claims layer (B1-B8 spec drafted tonight) — the interface verbs.
3. The head museum staffed — ractor jars walk the map as NPCs (engram-backed).
4. The first district: the maze dungeon (exists) + the raid hall (50-wide = the raids).
5. NCP-style citizen deltas: 17M fine-tunes per NPC on house corpus — after Rocinante lands.
6. The door: the world as the openclaw — public entry into the hive, fence enforced at the gate.
