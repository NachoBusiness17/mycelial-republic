# WORLDGEN MINE — DF history-engine mechanics, folded

**2026-09-25 · Source: dwarffortresswiki.org (World_generation, Calendar#Ages,
Megabeast, Historical_figures, Sphere, Villain, Titan, Forgotten_beast,
Dwarven_language). Mined per operator law; every number/name below carries its
page. The full sphere list renders as a graph image on the wiki: OWED, not
invented (the sourced starter set lives in Worldgen.luau).**

## THE LAWS (mined, with pages)

1. **Ages** (Calendar#Ages): worlds start in the Age of Myth; age transitions
   are driven by megabeast deaths; >3 great powers runs Myth, Legends, Heroes;
   ages recur with ordinals ("The Second Age of Legends"); world size sets age
   stability (small worlds churn, large worlds hold). FOLDED:
   `Worldgen.ageText()` — the mountain starts in the Age of Myth, every 10
   megabeast kills (Skeleton King fells) advances the age with DF ordinal
   recurrence. The <=3-powers branch: UNMINED, owed.
2. **Great powers** (Calendar): historical figures with [POWER]/[MEGABEAST]/
   [TITAN] shape the period. The mountain's three: THE ANSWER, THE SKELETON
   KING, THE MAKER.
3. **Forgotten beasts** (Forgotten_beast): procedural megabeasts drawn by
   WEALTH AND NOISE (difficulty-adjustable); the world PAUSES when one is
   first seen; each is tied to the sphere of caverns plus one or two others
   (water, theft, thralldom, darkness, suicide, muck). FOLDED: Hall wisps are
   now announced by forgotten name (`Worldgen.forgottenName`: mined dwarven
   compound + sourced sphere).
4. **Spheres** (Sphere/Titan/Forgotten_beast): cosmic principles held by gods,
   forces, angels, demons, megabeasts, forgotten beasts; the wiki renders a
   friendship/parent/preclusion GRAPH between them. Sourced starter set:
   caverns, water, theft, thralldom, darkness, suicide, muck (Forgotten_beast)
   + animals, nature, plants, rivers (Titan raws). The graph is a
   world-gen structure we owe ourselves: sphere kinship = which zones ally.
   FOLDED (2026-09-25, afterparty t9): the wiki's engine-side
   friendship/parent/preclusion edges are NOT in the mine, so the graph is
   DERIVED from the mine's own sourced fields (df_spheres.json), never
   authored: alignment = the good_spheres/evil_spheres classes; ALLIES =
   same-class peers plus spheres co-occurring in one generator region
   (generator_region_spheres) or on one named creature (by_creature);
   OPPOSED = every sphere of the opposite class; unaligned spheres carry
   no enmity (OPPOSED = {} is a fact, not an omit). Opposition wins over
   co-occurrence when a pair lands in both (good and evil never ally).
   Tables GENERATED into `shared/SphereKinship.luau`
   (tools/gen_df_luau_data.py); `Worldgen.zoneAlliance` is the alliance
   pick, and the forgotten-beast announcement files its kin and foes.
   FOLDED (2026-09-25, afterparty t35): zone access/buffs gated by
   sphereAlliance: each WAVE zone joins one generator_region_spheres key
   (rows GENERATED into `shared/RegionSpheres.luau`; the zone-to-region
   join is authored once per WAVE row as the strict-required `region`
   field in `init.server.luau` and `server/ZoneGate.luau` receives the
   map derived at init, so a zone cannot exist without a join and a join
   without its zone cannot be written; zone names are the estate's
   own and exist nowhere in the mine. 2026-09-25, afterparty t67: the
   join was previously two hand-kept lists identical only by discipline,
   t64's audit proved them diff-identical 11 vs 11), the player's sphere
   is drawn once
   per soul from the 130, and `Worldgen.zoneAlliance` vs the region's
   spheres picks the portal: allied = open + a small VirtueMark buff on a
   per-zone cooldown; independent = open, no effect (a negative is a
   fact); opposed = locked door, NOT implemented, every sourced region
   row is unaligned spheres so opposed is unreachable today and a dead
   branch would be fallback creep. REPLICATED (2026-09-25, afterparty t46):
   the same `allianceFor` verdict is stamped onto the player at join as
   `Gate_<zone>` attributes (zone names space-sanitized to underscores) and
   the client tints the portal pad locally: allied leans green, opposed
   leans red, independent tints nothing (a negative is a fact). The tint is
   deterministic client visuals only and never gates.
5. **Villains** (Villain): mundane plots are corrupt imprisonment, framing,
   snatching, sabotage, directing wars; temptation is checked against the
   figure's personality and values, and failure to resist becomes ongoing
   corruption. FOLDED (2026-09-25, gala lane b4): Vellum's grant is a plot
   template and signing it is a temptation roll against the player's
   counted-chairs history, exactly DF's values-vs-temptation law
   (`shared/Temptation.luau`, wired at the MudBasecamp grant prompt).
6. **Names** (Name/Dwarven_language): first name untranslated single noun; last
   name a two-word compound (Noun-Noun, Adj-Noun, Verb-Noun); civ symbols bias
   word choice; 2,122-word lexicon parsed from raws format. FOLDED:
   ArtifactLore (41 words) + Worldgen.forgottenName.
7. **Artifacts** (Legendary artifact): one per lifetime, the expression of the
   maker's desires/fears/memories/hopes; moods Fey/Secretive/Possessed.
   FOLDED: ArtifactLore.moodLine.
8. **Item value** (Item value + the raws mine df_economy.json): value =
   BASE x MATERIAL_VALUE x QUALITY_MULT + QUALITY_BONUS; artifacts are
   x20 +300. FOLDED (2026-09-25, gala lane b4): `shared/DfValue.luau`
   (tables generated into `shared/DfGoods.luau`), riding the LedgerExchange
   conveyor as the dwarven appraisal; cloned Steal-a numbers untouched.
9. **Procedural creatures** (Forgotten_beast + the vanilla_procedural mine
   df_procedural.json): build_body_from_rcp = weighted RCP profile pick,
   must_have parts unconditional, ONE primary tweak, QUADRUPED 1-in-20 leg
   flip, 1-in-20 uniform-material flip. FOLDED (2026-09-25, gala lane b4):
   `shared/ProceduralBody.luau` (tables in `shared/RcpData.luau`), the Hall
   wisps now assemble per profile instead of rendering as plain balls.

## THE OWED (updated 2026-09-25: raws mine CLOSED the first two)

- [CLOSED] Full sphere list: 130 distinct, found in data/init/globals.lua
  random_sphere_adjective keys (the wiki image hid it; the install didn't).
  Worldgen.luau now carries all 130.
- [CLOSED] Full dwarven lexicon with POS: 3,223 words per language,
  CP437-decoded, POS from language_words.txt join
  (corpus/df_mine/df_lexicon_full.json); ArtifactLore embeds a 130-word
  POS-legal curated slice (80 nouns + 50 adjectives).
- The <=3 great-powers age branch (Ages of Powers).
- Supernatural villain plots + the rumor/informer loop (Villain page section
  not yet extracted).
- [FOLDED 2026-09-25] Procedural beast BODIES into wisp shapes: the assembly
  chain is mined (235 weighted RCP profiles, attack classes, 1-in-20
  uniform-material flip, corpus/df_mine/df_procedural.json) and now renders:
  `shared/ProceduralBody.luau` assembles core + legs + must_have parts per
  profile; `MudBasecamp.summonWisps` spawns the assembled bodies. Attack-class
  warnings ride the first-seen announcement. Partial by design: one primary
  attack per body (all classes tabled), geometry is blocky Luau primitives.
- [FOLDED 2026-09-25] DF value formula into the Exchange: value = BASE x
  MATERIAL x quality (artifact x20 +300); tradegoods tabled in df_economy.json
  and generated into `shared/DfGoods.luau`; `shared/DfValue.luau` appraises
  every conveyor artifact, the appraisal decides the steal-deposit income, and
  artifact pieces announce on the billboard. Cloned buy costs/incomes per
  CLONED_MECHANICS.md 3.1 are untouched.
- [FOLDED 2026-09-25] Soul.luau wiring into HeadMuseum: head souls persist to
  DataStore HeadMuseumSouls_v1 (emotion rows + needs only; stress and mood
  still derive at read time, the two-stage law).
- The <=3 great-powers age branch (Ages of Powers).
- Supernatural villain plots + the rumor/informer loop (Villain page section
  not yet extracted); the mundane temptation roll itself is FOLDED above.
- Titan/Forgotten procedural BODY forms (the pages carry generation details we
  have not yet folded into the wisps' shapes).
