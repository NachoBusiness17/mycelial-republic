# DFHack Data-Model FOLD (stratum: engine's exposed data model)

The engine's schema is runtime-introspectable (`type._fields`, `pairs(ref)`), and everything hangs off `df.global.world`: units, items, buildings, entities, sites, artifacts, history.

**Five revelations — what DF tracks that ShadowLedger / Worldgen / Head Museum NPCs do NOT:**

1. **Emotions are rows, not meters.** `personality.emotions[]` = `{emotion_type, causal unit_thought_type, strength, severity, flags, year, year_tick}`. Every feeling is a timestamped ledger entry naming its cause. FOLD: replace NPC `mood:number` with an `EmotionLog` DataStore (per-NPC sorted array: type/cause/strength/tick), derive mood scalar on read.

2. **Dual identity: flesh vs. biography.** `unit` (living sim) and `historical_figure` (eternal record: birth/death years, entity/hf/site links, kills) are separate rows joined by `unit.hist_figure_id`. The figure outlives the unit; world `history.events` is an append-only event-sourced log (`history_event_hist_figure_diedst`...). FOLD: Head Museum NPC gets a frozen `Biography` record + live `Avatar` record; death archives the avatar, never deletes the row.

3. **Relations are typed edges, never names.** `unit.relationship_ids` is an enum-indexed id map (PetOwner, RiderMount, Dragger...); `general_refs` are typed verb-edges (owns, contains, created, killed, imprisoned, written-about) on every item/building/hf. FOLD: ShadowLedger stores `{ref_type, target_id}[]` edge arrays, not denormalized "mother: 'Name'" strings.

4. **False identity is first-class.** `getAge(unit, true_age)` ignores false identities; professions resolve "accounting for false identity" — the engine keeps truth and persona side by side. FOLD: each NPC may carry a `Persona` view over its true row; queries accept `truthy=false`.

5. **Destiny is stored state.** `unit.status.artifact_name` pre-names the artifact a dwarf will someday make; `personality.dreams[]` carries `{goal_type, flags.accomplished}`; `needs[]` carry `focus_level` that goes negative when unmet. Intent precedes behavior. FOLD: seed NPCs with a `Dream` field + `Needs` map with decay-on-tick, so automation (not just players) can drive them.

Honorable mentions: names are 7-slot word vectors + parts of speech (generative, not strings); region-map tiles store evilness/savagery/drainage (geography has a personality); buildings track build-stage progress and room adjacency; the engine ships its own save-scoped KV persistence (`persistent.getWorldData`).

**Most fold-worthy structure:** `unit_soul` (`status.current_soul`) — body and psyche as separate records, the psyche holding skills-with-rust, preferences, and the emotion/need/dream ledger; copy it whole into a per-NPC `Soul` DataStore.

Receipt: `corpus/df_mine/dfhack_datamodel.json` (catalog; sources and caveats in `meta`).
