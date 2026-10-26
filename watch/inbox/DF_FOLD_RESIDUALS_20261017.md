# DF Fold Residuals Receipt (2026-10-17)

- **Date:** 2026-10-17
- **Writer:** antigravity-primary (pair programming with operator)
- **Status:** COMPLETED
- **Target Item:** `queue/todo.md:253` (`[mag] DF fold residuals`)
- **Strict Invariants:** Zero em-dashes (`--` or `-` only), zero shell pings, append-only ledger registration.

---

## 1. Summary of Folds

The three residual obligations from the 9-agent Dwarf Fortress mine (`corpus/df_mine/`) have been implemented directly into THE MOUNTAIN's shared Luau modules:

1. **Supernatural Villain Plots (`roblox/src/shared/Temptation.luau`):**
   - Folded the complete DF villain motivation spectrum into the temptation resolution engine.
   - Added supernatural plots:
     - `deathless_cult` (strength 55, ethic `CORRUPTION`, weighs against `TRUTH`, feeds on `POWER` and `BELONGING`): necromantic defiance of mortality.
     - `artifact_theft` (strength 50, ethic `THEFT`, weighs against `LAW`, feeds on `WEALTH` and `POWER`): infiltration to seize sacred artifacts from mountain vaults.
     - `usurp_throne` (strength 60, ethic `TREASON`, weighs against `LOYALTY`, feeds on `POWER`): subversion of sovereign rule and coup schemes.
     - `false_prophet` (strength 45, ethic `DECEIT`, weighs against `TRUTH`, feeds on `BELONGING` and `POWER`): proclamation of false prophecies and deceptive doctrine.
   - Added query interfaces: `Temptation.listPlots(): { string }` and `Temptation.getPlot(plotId: string): PlotDef?`.
   - Wired `Corrupted` attribute dynamics into `Temptation.profile(player: Player)`.

2. **Per-Class Attack Triggers Beyond Scorpion-Force (`roblox/src/shared/ProceduralBody.luau`):**
   - Folded anatomical, material, and alignment constraints mined from `corpus/df_mine/df_procedural.json` (`attack_tweaks` and creature flags vocabulary).
   - Unconditional forced triggers:
     - `material == "FLAME"` forces `FIRE` (DF law: flame material grants built-in fireball and firejet).
     - `must_have_scorpion_tail` forces `TAIL_STINGER`.
     - `must_have_insect_stinger` forces `INSECT_STINGER`.
     - `must_have_webs` forces `WEBS` (spiders).
     - `must_have_poison_bite` forces `POISON_BITE` (vipers, cobras, gila monsters).
     - `suck_blood_through_proboscis` / `suck_blood_through_mouth` forces `PROBOSCIS_BLOOD`.
   - Anatomical and alignment filtering for procedural attacks:
     - `FIRE`: gated by `hasMouthOrBeak(p, flags)` or flame material (amorphous blobs without mouth cannot breathe fire).
     - `BREATHE_TRAILING_FLOW` and `BREATHE_UNDIRECTED`: evil-only breath attacks (vapor, gas, deadly dust).
     - `BREATHE_GLOB`: deadly spittle, gated by head/mouth.
     - `POISON_BLOOD`: evil-only, requires vertebrate or fleshy circulatory system.
     - `SECRETION`: evil-only, requires solid surface exoskeleton, scales, or plates.
   - Extended `ProceduralBody.assemble(rng: any, maybeOpts: AssembleOpts?): Spec` backward-compatibly with `AssembleOpts` (`isEvil`, `material`).

3. **Ages of Powers Branch (`roblox/src/shared/Worldgen.luau`):**
   - Unmined calendar branch closed per Dwarf Fortress world-history laws.
   - Initialized `Worldgen.INITIAL_POWERS = 30` with `Worldgen.remainingPowers()` and `Worldgen.setSupernaturalPowers(count)`.
   - When megabeasts fall below threshold (`remainingPowers <= 3`):
     - 3 powers remaining: `"The Age of Three Powers"`
     - 2 powers remaining: `"The Age of Two Powers"`
     - 1 power remaining: `"The Age of Powers"`
     - 0 powers remaining with active supernatural forces: `"The Age of Ghost and Shadows"`
     - 0 powers remaining with supernatural purged: `"The Age of Civilization"`
   - Preserves standard earlier cycle progression (`Myth`, `Heroes`, `Legends`) with ordinal recurrence (`Second`, `Third`, etc.) when `remainingPowers > 3`.
   - Purged existing historical em-dashes from module header.

---

## 2. Verified Disk Footprint

- `roblox/src/shared/Temptation.luau`: 116 lines, 4,562 bytes
- `roblox/src/shared/ProceduralBody.luau`: 414 lines, 15,466 bytes
- `roblox/src/shared/Worldgen.luau`: 300 lines, 7,517 bytes
- `tests/test_df_residuals.py`: 72 lines, 2,624 bytes
- Em-dash check: 0 matches across all 4 files.

---

## 3. Queue Resolution

Item `queue/todo.md:253` marked `[x] CLOSED`.
Monotonic registration appended to `watch/inbox/index_events.jsonl`.
