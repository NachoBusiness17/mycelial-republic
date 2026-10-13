# FOLD — DFHack inner-life model → fleet organs

DF keeps a dwarf's inner life on the soul: `unit.status.current_soul.personality`
with `stress` (raw int), `emotions[]` (thought instances: `type`, `thought`,
`strength`, `severity`, `year`, `year_tick`, spare flag bit 30 = synthetic),
`needs[]` (`id`, `focus_level` -999..+400), `traits`, `values`, `dreams`,
`preferences`. Stress maps to 7 buckets via cutoffs [50000, 25000, 10000,
-10000, -25000, -50000, -100000] → Miserable..Ecstatic. Full thought/trait
enums live in df-structures (not this clone).

**Folds:**

1. **Estate virtue meters ← stress cutoff ladder.** Copy the exact shape: one
   signed accumulator, fixed cutoff table, `getStressCategoryRaw(level)` with
   middle-bucket default when the soul is missing. dwarfmonitor's `H:` widget
   (7 slash-separated counts, one color per bucket) is the whole estate meter —
   a fleet overview is just `SELECT bucket, count(*)` over this. Adopt
   `stress_cutoffs` verbatim as the decay-curve shape.

2. **Head Museum heads' moods ← `personality_moodst` emotion instances.** A
   head is not a mood; it is a *list of thought instances with weights*.
   Adopt the record: `{thought_trigger, emotion_type, strength, severity,
   timestamp}` appended to a vector, aggregated lazily into the scalar meter.
   misery.cpp proves the write path: inject an instance, flag bit 30, delete
   by flag — synthetic emotions are first-class and revocable. Head moods
   should be event ledgers, not editable scalars.

3. **ShadowLedger disposition lines ← unmet-need focus penalties.** A
   disposition line = one `need_type` + `focus_level < 0`. The gate worth
   stealing: `focus_level <= -10000` makes the dwarf's current activity
   *unbailable* (locked in) — the ledger equivalent of "this agent is pinned,
   do not reassign." autolabor's `scan_needs` is the consumer pattern:
   unmet needs bias *work assignment* (laborer_pull / idle_pull / favored
   skills) rather than just decorating a report.

4. **Trigger→effect is two-stage, keep it that way.** Trigger
   (`unit_thought_type`, e.g. SoapyBath = "has been without drink"-style keys)
   appends an emotion; the *scalar* stress only moves through aggregation;
   effects fire at scalar thresholds (longterm_stress ≥20000/50000/100000 →
   10%/50%/100% Fell/Macabre mood). Fleet version: event log → metric →
   threshold gate. Never wire an effect to a single event.

5. **Personality = static lens over the meter.** `traits` + `values` weight
   *how fast* stress moves (sort.lua's mental-stability formula: cheer 0.41,
   nature 0.27, stress_vulnerability -0.20, knowledge -0.30). Fleet organs
   should store per-agent trait weights and multiply the meter's delta, not
   fork per-temperament logic. Read path is already Lua-exposed:
   `dfhack.units.getStressCategory/getFocusPenalty/getGoalName`.

Source: corpus/dfhack_full (dwarfmonitor, sort, misery, strangemood, autolabor,
Units.cpp, LuaApi.cpp). Field lists: dfhack_innerlife.json.
