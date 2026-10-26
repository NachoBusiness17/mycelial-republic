# Cultural Pack: Senet – `senet.gptoss.DRAFT.md`

> **Status:** DRAFT. **Engine:** race_dice.

CULTURAL PACK: Senet
ENGINE: race_dice
RULE DELTA:
- TRACK: linear, 30 squares (indices 0‑29). Start at square 0, final square before bear‑off is 29.
- CAPTURE: off (pieces cannot capture; they coexist on squares).
- ENTRY: roll‑exact entry; a piece may enter the track only on a roll that exactly matches the entry requirement (as defined by the pack).
- DICE: historical casting‑sticks mode (four flat sticks, each marked side counts as 1; total move = number of marked sticks, seeded‑external RNG).
- SPECIAL SQUARES: squares 26‑30 are ritual squares – safe zones where capture is prohibited and pieces may receive extra effects defined by the pack (e.g., advancement or retreat). These squares are treated as `safe` in the engine.

HISTORICAL MODULE:
- ERA: Predynastic / Early Dynastic Egypt (~3100 BCE)
- CULTURE: Ancient Egyptian
- ARCHAEOLOGY: Kendall 1978; Piccione 1990
- UNCERTAINTIES: Exact functions of squares 26‑30 (ritual vs. passage) and the precise rules for entry on a roll‑exact basis remain debated.
- RESEARCH_STATUS: reconstructed

MATERIALS MODULE:
- ORIGINAL PIECES: four casting sticks (Egyptian “seb” sticks), each with a single marked side.
- MODERN‑SKIN EQUIVALENTS: wooden dowels or plastic tokens representing sticks; alternatively, a digital binary counter (0‑4) can emulate the stick count.

REGIONAL VARIANTS:
- Kendall School (1978): defines squares 26‑30 as ritual exit squares; entry rule requires an exact roll of 1 to bring a piece onto the board.
- Piccione School (1990): treats squares 26‑30 as safe squares with optional advancement effects; entry allowed on any exact roll matching the dice result.

ETHICS/ATTRIBUTION:
- Originating culture: Ancient Egyptian civilization.
- Sources: Kendall 1978; Piccione 1990.
- Sensitivity notes: Respect the cultural heritage of ancient Egypt; avoid modern reinterpretations that misrepresent archaeological evidence.

BUILD PROMPT: Using the race/dice engine as a base, implement a linear 30‑square track where players move pieces according to the result of four casting sticks (0‑4) seeded externally; capture is disabled, squares 26‑30 are safe ritual zones, and pieces may only enter the board on an exact roll matching the entry requirement. Provide the full rule set, board layout, and initial setup so the game can be played directly.

---
NOTE: The seed’s instruction to place the variant‑specific content last (static‑first ordering) proved ambiguous for non‑DeepSeek models, which sometimes reorder sections, risking violation of the byte‑stable contract.
