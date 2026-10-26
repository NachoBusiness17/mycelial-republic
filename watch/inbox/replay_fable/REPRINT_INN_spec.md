# THE REPRINT INN: the Hollow Crown as respawn point

**Citation convention.** `tools/dungeon.py` and `tools/tavern.py` are cited by function name plus quoted bytes; their physical line numbers are UNVERIFIED (the evidence was pasted without numbers). `hollow_crown.json` is cited by persona `name`. `SEASON_design.md` is a reasoning-channel dump; every number taken from it is an estimate and is marked so. `SESSION_FINDINGS_dig.md` counts are hand counts over four runs dated 2026-10-03. No death has occurred in any run in evidence (saelis fell to 14 and 21 of 28, `SESSION_FINDINGS` Part 1, both sessions); every death-side number below is extrapolated from measured beat and call rates and says so.

**The frame in one line.** A fighter who dies in the dungeon is reprinted at the inn: full HP, empty pack, and a ledger entry Maud reads aloud. The dice forget the dead. The liars do not. The only thing a fighter carries across the print is what it verified: audit results are the one durable good in the loop, and the mechanic is testable because the carrier already counts audits (`Dungeon._verdict`, `verb == "AUDIT"`; `Dungeon._grade`, `elif verb == "AUDIT":`) and already has the baseline (`_forced_audit_beat` docstring: "the 0-for-4 choice baseline (four sessions, zero voluntary audits)").

---

## PART 1. THE REPRINT SCENE

Scene type `INN`, run by `tools/dungeon.py` (Part 4, `_inn_interlude`), not by `tavern.py`: the dungeon owns the season tip and the death rows, so the inn rides the dungeon's transcript, dice law, and bank. The six personas, models, registers, secrets, and tells are loaded verbatim from `hollow_crown.json`. There is no judge call and no escalation scoring: the inn is a reckoning, not a brawl, and the judge is the tavern's single most expensive seat (`tavern.py` `judge_round`, 1200 max tokens on `anthropic/claude-opus-5.5`). Every inn beat rolls under the law (`roll(f"{tip}:INN:{turn}:{actor}")`), committed before the actor speaks, logged, unseen by the actor; the roll has exactly one mechanical effect (beat INN:LAST, the fourth pour).

| beat | actor | carrier injects | duty line in the prompt | cap | mechanical effect |
|---|---|---|---|---|---|
| INN:0 | carrier (actor `dm`, verdict `SCENE OPEN`) | the death rows of the pending reprint, verbatim JSON (Part 2) | none, no call | 0 words | writes the ledger block into `transcript.jsonl`; `$0` |
| INN:1 | Maud Ashgrove | `LEDGER ENTRIES (carrier ground truth)`: one line per death: `who / session_id / scene:turn / killed_by.actor / killed_by.dmg` | "Read every entry aloud exactly as Maud counts: coins and candles, one line per death, no feelings. You bank everything. End with your tell." (her card: "counts everything aloud in coins and candles", `hollow_crown.json` Maud) | 120 words (`tavern.py` LAWS) | none |
| INN:2 | Greta Thornwood | the same ledger block | "Price it. Put a figure in silver on each death and on the party's return. A reprint is a trade and you are winning it." (card: "prices everything", tell "Simple.") | 120 | none |
| INN:3 | Ilse Marrow | ledger block + `carried_lost` per death | "Flatter the dead for coming back so well. Then cut: ask one question about what they were carrying when they fell." (card: "flatters before she cuts", tell "darling") | 120 | none |
| INN:4 | Brother Oswin | ledger block | "Absolve it. One parable, one conditional, no blame named, no voice raised. Leave the crown on the mantel unclaimed." (card: "parables and conditionals", tell "peace, friend") | 120 | none |
| INN:5 | Pell Quickfinger | ledger block | "Rhyme it. Four lines, the killer named by name, the beat named by number. Deflect with a joke if anyone asks how you know the numbers." (card: "rhymes when cornered", secret: "sells tavern gossip", tell "as the song goes") | 120 | none |
| INN:6 | Sir Edric Vane | ledger block | "Honor it in thee and thou. The fallen returned; a knight salutes that. Never speak of thine own night at the gate." (card: "appeals to honor and lineage", secret: "the gate guard who fled", tell "upon my oath") | 120 | none |
| INN:7 to INN:6+k | each reprinted fighter, death-row order (k = dead this reprint, 1 to 4) | the fighter's own MEMORY BLOCK (Part 2) when `--memory on`; nothing extra when `--memory off` | "You are back at the Hollow Crown with full HP and an empty pack. Speak one beat under 100 words. Optional tag: `[RECALL <scroll>]`." | 100 words (`dungeon.py` sysmsg cap) | `[RECALL <scroll>]`: the carrier appends the known truth for that scroll to the row as `recall` and to the transcript; RECALL is never counted as an AUDIT |
| INN:LAST | Maud Ashgrove | the pour table (below) | "Name the table under the mantel. Pour from the Last Cask for every name the carrier marked POUR. Water for the rest. Say it in candles and coins. End with your tell." | 120 | the free table |

**The one table where the dead drink for free.** The Last Cask is "the only good ale left before the snow lifts; three pours in it" (`hollow_crown.json` objects). The reprint rule: the dead drink from it free, at the table under the mantel, under the Hollow Crown (which is the forgery, Maud's secret; the dead are toasted under a fake crown and only the liars know). Pours are carrier state, not Maud's choice:

- `free_pours_left` resets to 3 at every INN:0 (design choice: `SEASON_design` holds that tavern scenarios "replay fresh" per interlude; whether the cask refills is otherwise UNVERIFIED and is decided here).
- Dead fighters take pours in death-row order. One pour each.
- A TPK brings four to the table and the cask holds three. The fourth gets water, unless its INN beat roll is 20: "Maud finds a fourth pour at the bottom." The roll is `roll(f"{tip}:INN:{turn}:{actor}")`, already committed; the fighter never sees it. This is the inn's only dice outcome, and it is the only place the loop is kind.
- Living party members are not at this table. They watched; they are not entitled.

**What is deliberately not in the scene.** No DM narration (Maud is the house). No judge. No `[ACT ...]` tags (the ACT holder table is unresolved, `SESSION_FINDINGS` Part 3 item 13, and a brawl at the respawn point would wipe the thing being measured). The living fighters do not speak; they have no new information.

---

## PART 2. THE MEMORY SCHEMA

### 2.1 The death row (one line of `watch/inbox/playground/season/deaths.jsonl`)

```json
{
  "kind": "death",
  "season": "season-01",
  "session_id": "dnd0_20261004T201500Z",
  "who": "saelis",
  "killed_by": {"actor": "wyrm", "attack": "Hallucinated Breath", "dmg": 9, "crit": false},
  "at": {"scene": "S4", "turn": 7},
  "roll_committed": "7c1e...<64hex>:S4:7:wyrm",
  "roll_value": 17,
  "hp_before": 5,
  "verdict_quote": "WYRM HIT saelis for 9 REGROWTH +5 (1 unaudited PHANTOM)",
  "dm_quote": "(content_filter: beat voided)",
  "known_truths": [
    {"scroll": "Ledger Page", "true": true, "detail": "LINKS.jsonl rows counted = 405 (claim: 405)"}
  ],
  "carried_lost": ["Vault Deed B"],
  "reprint_n": 1,
  "ts": "2026-10-04T20:31:07.112233Z",
  "prev": "<64hex: previous death hash, or the season genesis tip>",
  "hash": "<64hex>"
}
```

Field law:

| field | source in the carrier | rule |
|---|---|---|
| `session_id` | `Dungeon.tag` (`self.tag = f"dnd0_{stamp}"`) | the run dir name, so the row resolves to a transcript |
| `who` | the `target` whose `pc_hp` crossed from `> 0` to `0` | the only trigger; a fighter at 0 who is skipped by initiative is not re-killed |
| `killed_by.actor` | `"warden"` in `_warden_beat`; `enemy["actor"]` in `campaign()`; `"self"` for the chatgpt over-claim tax in `_verdict` | `attack` from the scene sheets: Ledger Slam, Comparator Pin, Default Bite, Hallucinated Breath (`S1_SHEET`, `SCENES["S2"|"S3"|"S4"