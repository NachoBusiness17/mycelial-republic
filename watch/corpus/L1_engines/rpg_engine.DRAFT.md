# L1 — RPG Engine: UNIVERSAL DICE PROTOCOL & LAYER‑1 ENGINE

## HEADER — BYTE‑STABLE STATIC PREFIX
*All content below this line is immutable for cache‑hit purposes. Do not edit formatting, whitespace, or ordering after the `PROMPT‑BODY‑START` marker. The engine description is intended to be consumed verbatim by a language model on every invocation.*

---

[PROMPT‑BODY‑START — static, byte‑stable]

### UNIVERSAL DICE PROTOCOL (inherits L0)
The engine embeds the **six‑function contract** from L0 (`THE SIX‑FUNCTION GAME CONTRACT`) **unchanged**. In addition it extends the RNG algebra with the following *RPG‑specific* modifiers, all **deterministic, seed‑external** as defined in L0:

- `^` *critical*: after evaluating an `XdY+Z` expression, if the raw total equals the maximum possible value (i.e. `X*Y + Z`), the result is flagged as a *critical success* and may trigger optional `CRIT` rules.
- `!!` *fumble*: if the raw total equals the minimum possible value (i.e. `X*1 + Z`), the result is flagged as a *fumble* and may trigger optional `FUMBLE` rules.
- `kH` *keep‑highest H*: keep the highest `H` dice of the roll before applying modifiers. Syntax example: `4d6k3` (roll four d6, keep highest three).
- `kL` *keep‑lowest L*: analogous to `kH` but keeps the lowest dice.
- `!` *exploding*: any die that lands on its maximum face is rerolled; the additional roll is added recursively up to eight extra rolls per die.
- `pool Y tN` *success‑pool*: roll `Y` dice, count the number of results `≥ N`. The count is the result.
- `adv` / `dis` *advantage/disadvantage*: roll two dice of the same size, take the higher (`adv`) or lower (`dis`). Can be combined with `kH/kL` and `!` in the order listed in L0.

All RNG calls reference the **UNIVERSAL RNG PROTOCOL** from L0; the engine never generates randomness internally.

---

### RESOLUTION LADDER
A hierarchical difficulty ladder maps numeric roll outcomes to qualitative results. The ladder is static across all RPGs and is used by the **Resolution Block** below.

| Difficulty Class | Target Roll | Interpretation |
|------------------|------------|----------------|
| **Impossible**   | ≤ 1        | Automatic failure (unless a `CRIT` overrides) |
| **Very Hard**    | 2‑4        | Failure, but may earn partial success on a `CRIT` |
| **Hard**          | 5‑7        | Failure, no partials |
| **Moderate**      | 8‑10       | Success with minor complications |
| **Easy**          | 11‑13      | Success, no complications |
| **Trivial**       | ≥ 14       | Automatic success, may trigger bonus effects |

*The numeric roll is the **final numeric result** after all modifiers (keep, explode, adv/dis) have been applied.*

---

### PROGRESSION FRAMEWORK
A **system‑agnostic XP/Level** model tracks character advancement.

- **XP Accrual:** Each resolved action awards XP equal to the **Difficulty Class** index (Impossible = 0, Very Hard = 1, … Trivial = 5) multiplied by a scalar `S` (default `S = 10`).
- **Level Thresholds:** Level 1 starts at 0 XP. Each subsequent level requires `Level × 500` XP (i.e. Level 2 = 500, Level 3 = 1 000, etc.).
- **Level‑Based Modifiers:** On reaching a new level, the character gains a **+1 to all future keep‑highest rolls** and a **+1 to the success‑pool threshold `N`**.
- **Universal Advancement:** The progression model is shared; individual games may provide **optional overrides** in their L2 pack (e.g., different scaling factor `S`).

---

### SOLO ORACLE BLOCK
A solo‑play oracle supplies narrative outcomes without a GM. It consists of four independent sub‑oracles, each expressed as **prompt‑ready tables**.

1. **YES/NO ORACLE (Mythic‑style 2d6 + CHAOS)**
   - Roll `2d6` plus a *chaos modifier* (drawn from a `d6` table defined in the pack). Map the total to the **Likelihood Ladder**:
     - 2‑4 → **No**
     - 5‑7 → **Unlikely**
     - 8‑10 → **Possible**
     - 11‑13 → **Likely**
     - 14‑16 → **Yes**
   - Critical/fumble flags from the Universal Dice Protocol apply.

2. **ACTION/THEME ORACLE (d100 double‑table)**
   - Roll a `d100`. The tens digit selects an **Action** (e.g., *Explore, Fight, Negotiate, Discover*). The units digit selects a **Theme** (e.g., *Lost Artifact, Betrayal, Revelation, Hazard*). The engine concatenates them to produce a prompt such as `"Explore – Lost Artifact"`.

3. **SCENE‑COMPLICATION ORACLE (d10)**
   - Roll a `d10`. Each result maps to a pre‑written complication (e.g., `1 → “Sudden storm”`, `5 → “Unexpected ally appears”`). The result is injected into the scene description.

4. **NPC TRAIT/ MOTIVE / SECRET ORACLE (three‑roll)**
   - Roll `d6` three times:
     - First roll selects a **Trait** (e.g., *cunning, stoic, generous*).
     - Second roll selects a **Motive** (e.g., *revenge, ambition, curiosity*).
     - Third roll selects a **Secret** (e.g., *hidden agenda, lost love, cursed item*).
   - The three‑part string is used to flesh out a newly introduced NPC.

All tables are **static** and stored in the engine’s *oracle payload*; they are part of the **STATIC PAYLOAD MAP** (see below).

---

### SCENE STATE MACHINE
A deterministic finite‑state machine governs scene flow:

1. **ESTABLISH** – The narrator describes the initial setting; the archivist records the canonical state string.
2. **COMPLICATE** – The scene‑complication oracle is consulted; the result modifies the narrative and may affect the game state (e.g., impose a condition).
3. **RESOLVE** – The player (or solo oracle) performs an action; the Resolution Ladder evaluates the roll and yields success/failure, possibly invoking **CRIT** or **FUMBLE** rules.
4. **NEW‑HOOK** – After resolution, the engine either ends the scene (if `TERMINAL?` is true) or generates a **new hook** (a prompt for the next action) using the Action/Theme oracle.

Transitions are *pure* – they never depend on prose, only on the deterministic roll outcome and the static tables.

---

### NARRATOR / ARCHIVIST SPLIT
- **Narrator** – owns all *fictional* output: descriptive prose, scene ambience, character dialogue. The narrator never mutates the canonical state string.
- **Archivist** – owns the **L4 session state** (the canonical string, turn index, RNG seed, etc.). All state‑changing operations (`APPLY`, `LEGAL?`, `TERMINAL?`) are performed by the archivist.
- The split mirrors the research finding in *arXiv 2502.19519* and prevents state‑drift.

---

### STATIC PAYLOAD MAP
The engine’s static payload is partitioned into three token‑budget bands (approximate values based on the primer’s cache paradox). All numbers are **upper bounds**; actual token counts may be slightly lower after compression.

| Layer | Content | Token Budget |
|-------|---------|--------------|
| **System Rules** | Universal Dice Protocol, Resolution Ladder, Progression framework, Scene State Machine, Narrator/Archivist split. | **2 000 – 10 000** |
| **Setting Bible** | Core world‑building facts (e.g., core mythology, primary locations, major factions). | **5 000 – 50 000** |
| **Bestiary** | Creature entries (name, stat block, description) – each entry ~200 tokens. | **3 000 – 20 000** |

The **95 %‑hit layers** are the System Rules (always present) and the Setting Bible (common to many games). The Bestiary is optional per‑game and loaded only when referenced.

---

### FAMILY PACK SLOTS
The engine provides three *plug‑in* family packs that can be swapped in to produce concrete game systems:

1. **PbtA‑lite** – Implements the *Powered by the Adventure* core mechanic (2‑dice roll, +/- modifiers, moves defined in the pack). Uses the universal dice protocol with `2d6` rolls.
2. **d20‑lite** – Classic d20 system: roll `1d20+modifier`; critical on 20, fumble on 1. Includes the standard ability‑check, attack, and skill templates.
3. **FKR** – *Fate‑Killer‑RPG* hybrid: uses a **Fate dice pool** (`4dF`) with success threshold, combined with the universal dice protocol for damage.

Each pack supplies its own **L2 statics** (character sheets, move definitions, equipment tables) and may override the default progression scaler.

---

[PROMPT‑BODY‑END]

## NOTES – NON‑STATIC SECTION (for future extensions)
- The engine deliberately contains **no Python, no heredocs**; all procedural logic is expressed in natural‑language rules and static tables.
- Packs may add **optional rules** (e.g., magic systems, sanity) that reference the base protocol but do not alter the static prefix.
- All token budgets above are *soft limits* to keep the engine within the 2‑10 K range for cacheability.

---

*End of draft.*