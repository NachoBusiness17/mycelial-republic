# economy_FOLD — how DF prices the world (mined 2026-09-25)

## The value token chain

DF's price of everything is three raws-verified tokens multiplied, plus one engine layer:

**value = BASE x MATERIAL_VALUE x QUALITY + QUALITY_BONUS + decorations**

1. **MATERIAL_VALUE** lives in material raws (`inorganic_metal.txt`, `material_template_default.txt`, plant sub-materials). Nearly all matter is 1; only parchment (10), iron/silver/pig iron (10), steel/gold (30), platinum/aluminum (40), adamantine (300) rise above.
2. **BASE** = the item's `[VALUE:N]` token if the itemdef has one (only tools do: cauldron/minecart/wheelbarrow/stepladder 50, scroll/quire 20, die 1); otherwise the engine class base (weapons, armor, crowns, crafts 10; statues/windows 25; mechanisms 30; cut gems 20; bars 5).
3. **QUALITY** is engine-only, not raws: x1.1 well-crafted through x2 masterful, artifact **x20 +300**. Quality is a mild ratchet; *material choice is the real lever* — a plain adamantine item beats a masterful steel one 10:1.
4. Reactions create value out of proportion (flour mv 20 from mv-2 wheat; coke 9 bars from 1 coal), so *processing*, not rarity, mints most wealth.

## 3 fold notes for the fleet's Ledger Exchange

1. **Artifact classes for the conveyor: instruments, crowns, slabs.** All are *engine* item classes invisible in raws — the Steam install ships no `item_instrument.txt` (vanilla instruments are 100% procedurally generated; the raws include only a modding example where an assembled `ITEM_INSTRUMENT` carries `VALUE:50` from `VALUE:10` tool pieces). Adopt ratios: crown/scepter 10x material, statue 25x, instrument 5x (50 base, worth it), slab 10x — a gold crown (300) = 3 steel bars; an instrument equals a crown; a slab equals a bone figurine unless inscribed.
2. **Price in material, decorate in quality.** Ledger Exchange should weight tradegoods by MATERIAL_VALUE tier (2/10/30/40/300 metals; 2-60 gems) and let quality be a small multiplier, mirroring DF's anti-quality inflation. Artifact rarity = x20 ceiling, not x200.
3. **Mint value via reaction chains, not stock.** DF's economy rewards transforms (ore->bar, plant->thread->cloth->armor, mill->dye mv 20). The conveyor should price a good at its chain depth: raw mv 1-2, processed 20, crafted 10x material, artifact-class 10-50x.

Byte sources: `df_economy.json` (same dir). Install untouched, read-only.
