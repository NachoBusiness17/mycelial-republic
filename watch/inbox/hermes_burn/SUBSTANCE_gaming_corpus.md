# SUBSTANCE_gaming_corpus (anthropic/claude-opus-5.5, turn 1, channel: content)

**Citation convention.**

- `RB` = roblox/README.md
- `DF` = corpus/df_mine/DFHACK_THESIS.md
- `DND` = watch/inbox/hermes_burn/DND_module.md
- `BAR` = watch/inbox/hermes_burn/BARFIGHT_spec.md

`FILE:N` means line N, counted by hand from the evidence as pasted in this contract. The quoted bytes bind the citation. A line number that disagrees with the on-disk file is a carrier finding, and every on-disk line number is UNVERIFIED. `FILE:L?` means the line was not counted and the quote binds.

**Measurement conditions.** I executed nothing in this answer. Every "check passes" below is owed by a seat, not claimed here.

---

## PART 1. THE ONE DESIGN LAW

<law>
**Fixed bytes decide. Models and players only move inside them. Every outcome lands as a receipt that a third party can recompute without trusting whoever produced it.**
</law>

The law has three clauses, and each is testable:

- **(a) Deterministic instruction set.** The rules, formulas, and knobs are frozen text or code before play.
- **(b) Stochastic world.** LLM seats, players, or an engine nobody here wrote supply the variance.
- **(c) Receipt as ground truth.** The receipt is a dated, addressable row. The check is recomputation by a seat that is not the actor. Narration never counts as ground truth.

Examples:

- **Positive.** The DND carrier computes the verdict and the DM "must open with that verdict tag and then narrate" (`DND:138`). Here the law decides and the model only voices the result.
- **Negative.** A DM writes `[HIT] Against all odds...` on a roll of 1 (`DND:L?`, "Negative 1"). The stochastic layer overwrote the instruction set, so the outcome is void.

| Artifact | (a) Deterministic instruction set | (b) Stochastic world it steers | (c) Receipt surface | Who recomputes, and against what |
|---|---|---|---|---|
| DFHack thesis | Overlay tooling. `scripts/fix/*` are "named, scoped, one-defect repairs" (`DF:26`). The thesis is "sit above an engine you did not write, learn it through tooling" (`DF:41`). | The DF engine and, by self-steal, the estate itself (`DF:43-44`). | "every fleet action files a dated receipt" (`DF:35`). World state is "verkle chain + trails + LINKS ledger" (`DF:12`). "ours signs memory" (`DF:37`). | `tools/mountain_check + pytest + ratchet` (`DF:16`). |
| The Mountain | Ports frozen to their sources: "the Python engines are the source of truth" (`RB:141`). The eigen-map compass is "bearing 0° = north = eigen -y" (`RB:73-74`). | Players, plus 7 AI heads on "the free stealth lanes" (`RB:5`, `RB:10`). | ShadowLedger, "keyed by player+day" (`RB:92`). `memory/runs/roblox_npc/gateway.jsonl` (`RB:112`). `eigenmap-two-check.txt` (`RB:82`). | `tools/eigenmap_two_check.py` "diffs it against the scan JSON" (`RB:80-82`). |
| Dice-law D&D | `roll = int(sha256('{chain_tip}:{scene}:{turn}:{actor}')...` (`DND:112`). "The DM may not override." (`DND:139`) | Seat roleplay: "The rolls and the roleplay are stochastic." (`DND:5`) | party_subchain JSONL with `roll_committed` on every row (`DND:L?`, Part 4). | `dice_audit.py`, run by two seats that are not the DM, with a seeded-mutation blindness probe (`DND:L?`, AUDIT). |
| Bar fight | Scenario JSON. `"heat_trigger": "18 - 2*pressure"` (`BAR:23`). | Six persona LLMs plus a temperature-0 judge (`BAR:L?`, `"temperature": 0`). | Line ids `R{round}.{CODE}` and quote-checked judge cites (`BAR:L?`, `"quote_check"`). | Substring check plus rubric self-check (`BAR:L?`, Part 4 and Part 5). |

**Weakest member (named, not hidden).** The bar fight obeys clause (c) only partially. Its outcomes are decided by a model judge, so its receipt recomputes cite validity, not the score itself. A different judge can yield different heat from the same transcript, which is why the spec forbids comparing "across different judge models" (`BAR:L?`). Part 4 closes this gap in-world by replacing the judge with a deterministic event rubric.

**Falsifier of this unification.** The law is false for the corpus if any artifact contains a step that changes outcome state without a row a non-actor can recompute.

- Current status: the bar fight's judge score is the one known partial case, as stated above.
- If a seat finds a second such step, the law is a description of three artifacts, not four.

---

## PART 2. THE PLAYABLE FRONTIER

**What the Mountain gains.** Today, outcome-bearing variance in the Mountain has no recomputable roll. Separately, one known gap is a missing decision: the swarm's "upgrade pool ... is never offered" mid-run (`RB:128`). The dice law gives the Mountain auditable chance. The pressure knob gives it one integer that tunes NPC hostility without code edits.

**"No new infrastructure" means:**

- No new HTTP endpoint, RemoteEvent family, DataStore key scheme, service, or build step.
- New pure Luau modules under the existing `src/shared` are allowed.
- Every receipt rides the existing ShadowLedger t74 path: "every append goes through one UpdateAsync on the player+day key" (`RB:94`).

### Module assignment

| Path (existing tree) | Takes | From | Concrete change |
|---|---|---|---|
| `src/shared/Config.luau` (exists, `RB:38-40`) | The pressure knob | `"pressure": 0`, `"pressure_range": [-2, 3]` (`BAR:18-19`) | Add `Config.Pressure = 0`, an integer clamped to -2..3. This is the only tuning edit an
