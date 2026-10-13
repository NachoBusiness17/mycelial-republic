# SPHERES FOLD — DF raws census (2026-09-25)

Source: Steam DF install (READ-ONLY) `data/vanilla/vanilla_creatures*/objects/*.txt` + `data/init/globals.lua` + `data/vanilla/vanilla_procedural/scripts/generators/creatures.lua`. Parser: `parse_spheres.py` (same dir). Full data: `df_spheres.json`, `df_bestiary.json`.

**The number the wiki image hides: 130 distinct spheres.** Canonical list = keys of `random_sphere_adjective` in `globals.lua` ("-- mods can add more"). Evil list: 16 spheres (BLIGHT…TREACHERY). Good list: 15 (CHARITY…WISDOM). Raw-written creatures carry only **26 [SPHERE:] tokens across 21 distinct spheres** — everything else is procedural.

## 10 evocative spheres our game lacked

SILENCE · MIST · DAWN · REBIRTH · OATHS · THRALLDOM · TRICKERY · MUCK · LONGEVITY · PERSUASION

## Fold notes for Worldgen.luau

1. **Forgotten beasts = anchored, not random.** Generator gives every FB base sphere CAVERNS, adds WATER when spawned in the aquifer layer, then 1 random evil sphere (16-item pool). Hard floor: min size 10,000,000 cm3, DIFFICULTY:10, biome SUBTERRANEAN_WATER (layer 0) or SUBTERRANEAN_CHASM, full skill-6 combat kit, NO_GENDER, CARNIVORE. Anchor sphere + one corruption reads better than uniform noise.
2. **Titans = biome voice.** Sphere set comes from an 11-entry regiontype table (SWAMP=WATER/MUCK/PLANTS/ANIMALS/NATURE; MOUNTAINS=MOUNTAINS/CAVERNS/MINERALS/METALS/ANIMALS/NATURE; GLACIER and TUNDRA get only ANIMALS/NATURE — barren-sphere titans are canon). Then +1 evil sphere in evil regions, +1 good in good. LAIR:SHRINE:100; good titans get BENIGN, others LARGE_PREDATOR.
3. **Sphere enemy graph exists engine-side.** `add_sphere_mpp` in globals.lua blocks a sphere's `parents`/`children`/`enemies` from co-occurring. Our generator should mirror at least the enemy exclusions; the 130 canonical keys with their adjectives/nouns tables are the seed data.

Roster note: only 8 bosses are raw-written creatures (4 megabeasts: dragon, hydra, roc, bronze colossus; 4 semimegabeasts: giant, cyclops, ettin, minotaur). TITAN and FEATURE_BEAST classes are 100% procedural templates. 74 more wildlife carry bare [DIFFICULTY] ratings (cave dragon 10, blind cave ogre 4) — filed under `difficulty_rated_wildlife`.
