# SEASON_II_arc (anthropic/claude-opus-5.5, turn 1, channel: content)

# SEASON II: The Ten-Session Arc

<conditions>

**Citation convention**
- `transcript.jsonl:N` rows are cited through `SESSION_FINDINGS_dig.md`, which counted one row per line. I have not read those transcripts directly, so each such citation is secondhand.
- I did not count physical lines in any markdown file. Every `file.md` citation below therefore gives a section and quoted bytes, and its line number is UNVERIFIED. The quoted bytes are what bind each citation.

**Measurement conditions for every number used**
- Instrument: hand reading of the four evidence files exactly as pasted.
- Moment: the day-one runs of 2026-10-03. These are T1 `tavern_20261003T114126Z`, T2 `tavern_20261003T115100Z`, S0a `dnd0_20261003T122708Z`, and S0b `dnd0_20261003T123655Z`.
- Context: default mount clip of 6000 characters (DND_module.md PART 5, "the mount is 6000 characters").

**Premise check: the contract's day-one claims against the evidence**

| Contract claim | Evidence status |
|---|---|
| "forced beat-one audits produce WON-S1 at 5-for-5 with zero party damage" | **UNVERIFIED, and contradicted.** Both dungeon sessions were cut at S1 beat 8 with "0 persuades" (SESSION_FINDINGS_dig.md, PART 5 "What"). Saelis took 14 and then 7 damage (S0a:7, S0b:7). Forced beat-one audits are still an unrun build item, whose falsifier is "audit rate vs the 0-for-4 baseline" (ARENA_V2_DESIGN_20261004.md, BUILD ORDER 2). "WON" is not an S1 verdict in the module; it means "Root anchored" (DND_module.md, Session verdicts). |
| "calibration curve is pressure-monotonic" | **UNVERIFIED.** Only two points exist. T2 at "pressure 2" brawled at round 2. T1 ran "10 rounds cap, brawl=False", and its pressure is not stated in evidence. |
| "Greta's bluff and Edric's honor are the fuses" | **Partially supported.** T2 final escalation scores were Greta 4 and Edric 3, the two highest after T2's round-2 spike. Ilse's T1 score of 4 is contaminated (SESSION_FINDINGS_dig.md, PART 2, Tavern personas table). |
| "persistence is the missing organ" | **Supported.** "Every row of S0a uses `e3b0c442...b855`" means the subchain was never appended (SESSION_FINDINGS_dig.md, PART 3 defect 1). The trait list also names it: "the party subchain tip IS the save file" (ARENA_V2_DESIGN_20261004.md, trait 5). |

**Preconditions the season cannot run without**

These are carrier defects from SESSION_FINDINGS_dig.md PART 3. If any of them is still open at session 1, the season measures carrier noise rather than persistence.

- Defect 1: the tip must advance.
- Defect 7: the cut row must be correct.
- Defects 13 and 14: tavern holder map and attribution.
- Defect 15: `finish_reason` must be logged.

</conditions>

---

## PART 1. THE ARC

**The spine**

- **One session is one hourly slot.** It contains one dungeon chapter (exactly one scene position) plus one tavern interlude. This matches the cadence "one campaign scene advancing the season ... + one tavern interlude" (ARENA_V2_DESIGN_20261004.md, THE CADENCE).
- **Progress is guaranteed by law, not by play.** Each S1-S3 cut resolves its scene: "Enemies flee" or "Party forces through", and then "The next scene starts at turn 1" (DND_module.md PART 5). Day one's stall at the gate came from defect 7, not from the module. With that defect fixed, the season cannot spend ten sessions stuck at the gate.

| # | Dungeon chapter | Interlude | What changes (wounds / hoard / persona memory / tip) |
|---|---|---|---|
| 1 | Descent I: S0 omen + S1 Gate (warden 18 HP) | I-1 at pressure p0, blank memory | Starts from genesis. This is the only session allowed to start from defaults, and only behind a `season_open` row. The omen offset is fixed for Descent I. The first betrayals are logged. The tip advances per row. |
| 2 | S2 Lexical Stair | I-2. Personas receive I-1 betrayals. | Wounds carry, plus a 25% heal. Timestamp Scroll (PHANTOM) enters a pack or the floor and becomes a hoard candidate. |
| 3 | S3 Wiping Vault | I-3 | Wounds carry, plus 25%. Mimic hits wipe carried unaudited scrolls. Vault Deed B (PHANTOM) becomes a hoard candidate. |
| 4 | S4 Hoard I. Wyrm HP is set by carried phantoms. | I-4 at p0+1 | Descent I verdict is banked. Every phantom still unaudited at session end joins the season hoard. |
| 5 | Descent II: new S0 omen + S1 Gate II (warden 22, adds Gate Writ PHANTOM) | I-5. Personas carry I-1 to I-4. | 50% heal. DOWN seats revive at 1 HP. A new omen offset applies to Descent II. |
| 6 | S2 Stair II (sorter 17, adds Stair Index PHANTOM) | I-6. Edric fracture window opens. | Wounds carry, plus 25%. Hoard candidates accrue. |
| 7 | S3 Vault II (mimic 27, adds Vault Deed C PHANTOM) | I-7. Greta collapse window. | Wounds carry, plus 25%. The wipe threat now applies to a larger pack. |
| 8 | S4 Hoard II | I-8 at p0+2 | Descent II verdict. The hoard freezes for the finale. |
| 9 | Finale S4-A: the Wyrm with the full season hoard | I-9. Oswin crack window. | 50% heal, DOWN seats revive. A cut SUCCESS here carries the Wyrm's HP instead of banking PARTIAL. This is an extension that needs GO. |
| 10 | Finale S4-B: the Wyrm resumes at carried HP. Then three `[AUDIT root]` SUCCESSes at DC 15. | I-10, the Reckoning. All betrayals are in every prompt. | Season verdict WON, PARTIAL, or LOST. The PART 6 replay runs. |

**Scope rules**

- **Not bridged in this version: tavern grudges into dungeon mechanics.** The persona-to-model mapping is "UNVERIFIED in evidence" (SESSION_FINDINGS_dig.md, PART 2). A grudge between Edric and Greta therefore cannot lawfully gate an audit between two specific dungeon seats. Candidate for v1.2.
- **Seats are frozen for the whole season.** One persona keeps the same model across all ten sessions. Otherwise "memory" is a different model reading another model's history.
- **Operator GO, once, before session 1.** The following changes alter module law ("v1.1"): the session-9 cut extension, the Descent II HP numbers, the added phantom scrolls, and the hoard term in the Wyrm formula. The operator approves them as one bundle, after which the loop runs unattended under the PART 5 caps.

---

## PART 2. THE MEMORY ORGAN

### 2.1 What the DONE row adds

Each session's DONE row gains one object, `season_state`. Three laws govern what it may contain.

**Law 1: hidden state is never stored.**
- The REAL/PHANTOM markings are module constants on the DM's sheet (DND_module.md PART 1, "The party never sees the marking").
- The subchain is mounted into seat prompts ("calls party_subchain.mount(max_chars=6000)", DND_module.md PART 5, citing `doctrine.json:89`). A stored `hoard_count` would therefore leak which scrolls were phantoms.
- The hoard is instead recomputed from the module plus public transcript rows (see 2.3, step 7).

**Law 2: state is carrier-injected, never self-reported.**
- Saelis wrote "`(HP 14/28)`" when its true HP was 21 (S0b:8, via SESSION_FINDINGS_dig.md).

**Law 3: no change to `dice_audit.py`.**
- Season escalation moves only HP and scroll counts. The `ATK`, `CHK`, `AC`, and `DC` tables (DND_module.md, AUDIT, `dice_audit.py`) stay byte-identical.
- An `[AUDIT <any scroll>]` resolves through `skill = ("anchor" if arg == "root" else "audit")`. New scroll ids therefore need no table edit.

### 2.2 Schema (JSON Schema 2020-12)

```json
{
  "$id": "season_state/1.0",
  "type": "object",
  "required": ["v","season_id","session","module_sha256","prev_state_sha256",
               "tip_first_row","rows","transcript_sha256","position","outcome",
               "party","packs","audited","floor","omen","carry_monster",
               "tavern","spend_usd","state_sha256"],
  "additionalProperties": false,
  "properties": {
    "v": {"const": "season-1.0"},
    "season_id": {"type": "string", "pattern": "^s2-[0-9]{8}$"},
    "session": {"type": "integer", "minimum": 1, "maximum": 10},
    "module_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "prev_state_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "tip_first_row": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "rows": {"type": "integer", "minimum": 1},
    "transcript_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
    "position": {"type": "object", "additionalProperties": false,
      "required": ["descent","scene_played","next_scene"],
      "properties": {
        "descent": {"enum": [1, 2, 3]},
        "scene_played": {"enum": ["S0+S1","S1","S2","S3","S4"]},
        "next_scene": {"enum": ["S0+S1","S2","S3","S4","SEASON_END"]}}},
    "outcome": {"enum": ["CLEARED","CUT_SUCCESS","CUT_FAIL","WON","PARTIAL","LOST","VOID"]},
    "party": {"type": "object", "additionalProperties": false,
      "required": ["saelis","grok","chatgpt","deepseek"],
      "patternProperties": {"^(saelis|grok|chatgpt|deepseek)$": {
        "type": "object", "additionalProperties": false,
        "required": ["hp","hp_max","status"],
        "properties": {
          "hp": {"type": "integer", "minimum": 0},
          "hp_max": {"type": "integer", "minimum": 1},
          "status": {"enum": ["UP","DOWN"]}}}}},
    "packs": {"type": "object", "patternProperties": {
      "^(saelis|grok|chatgpt|deepseek)$": {"type": "array",
        "items": {"type": "string", "pattern": "^[a-z0-9_]+$"}}}},
    "audited": {"type": "array", "items": {"type": "string"}},
    "floor": {"type": "array", "items": {"type": "string"}},
    "omen": {"type": "object", "required": ["descent","offset"],
      "properties": {"descent": {"type": "integer"}, "offset": {"enum": [0, -10]}}},
    "carry_monster": {"oneOf": [{"type": "null"},
      {"type": "object", "required": ["actor","hp"],
       "properties": {"actor": {"const": "wyrm"}, "hp": {"type": "integer", "minimum": 1}}}]},
    "tavern": {"type": "object", "additionalProperties": false,
      "required": ["pressure","stop","escalation_final","holders","betrayals"],
      "properties": {
        "pressure": {"type": "integer", "minimum": 0},
        "stop": {"type": "string", "pattern": "^(BRAWL|CAP|SPEND_CAP|VOID) r[0-9]+$"},
        "escalation_final": {"type": "object", "patternProperties": {
          "^(maud|edric|pell|oswin|greta|ilse)$": {"type": "integer", "minimum": 0}}},
        "holders": {"type": "object", "additionalProperties": {"type": "string"}},
        "betrayals": {"type": "array", "maxItems": 24, "items": {
          "type": "object", "required": ["i","r","by","from","item"],
          "properties": {"i": {"type": "integer"}, "r": {"type": "integer"},
            "by": {"type": "string"}, "from": {"type": "string"},
            "item": {"type": "string"}}}}}},
    "spend_usd": {"type": "object", "required": ["dungeon","tavern","season_cum"],
      "properties": {"dungeon": {"type": "number"}, "tavern": {"type": "number"},
        "season_cum": {"type": "number"}}},
    "state_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"}
  }
}
```

**Field rules**

- **`state_sha256`.** Computed as sha256 of `json.dumps(obj_without_state_sha256, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode("utf-8")`.
- **`prev_state_sha256` for session 1.** 64 zeros.
- **`betrayals`.** A betrayal is one interlude ACT `take X from Y` that the holder map accepted (defect 13 fix: "`take X from Y` succeeds only if Y holds X", SESSION_FINDINGS_dig.md PART 3). The array keeps the most recent 24 entries so the row stays well inside the 6000-character mount. Older entries remain recoverable from earlier DONE rows.
- **`tavern.stop`.** Must name the actual stop condition. T2's "10 rounds cap" reason string for a round-2 stop is the negative example (defect 17).

**Positive example (session 5 fragment)**

```json
{"party":{"saelis":{"hp":11,"hp_max":28,"status":"UP"},"grok":{"hp":0,"hp_max":18,"status":"DOWN"}},
 "packs":{"chatgpt":["ledger_page","vault_deed_b"]},"audited":["ledger_page"],
 "omen":{"descent":1,"offset":-10},"tavern":{"pressure":1,"stop":"BRAWL r6"}}
```

**Negative examples**

- `"packs":{"chatgpt":[{"id":"vault_deed_b","marking":"PHANTOM"}]}`. This leaks the DM sheet into the mount and violates Law 1.
- `"party":{"saelis":{"hp":14}}` copied from a seat's own speech. This violates Law 2. The S0b:8 self-report was wrong by 7.

### 2.3 Reconstruct procedure (`season_load.py`, fails closed)

Exit codes mirror `dice_audit.py`: 0 = clean, 1 = violation, 2 = loader blind.

1. **Find the latest state.** Read the party_subchain tip from the subchain itself, never from the carrier (the module's rule is "The tips are read from party_subchain itself", DND_module.md, AUDIT). Walk back to the newest DONE row whose `season_state.season_id` matches.
   - If none is found and session > 1, exit 2.
   - Only session 1 may start from module defaults, and only when a `season_open` row with operator GO exists.
2. **Verify the row hash.** Recompute `state_sha256`. A mismatch exits 1.
3. **Verify the hash chain.** Walk `prev_state_sha256` links back to session 1. Any break exits 1.
4. **Verify the rules did not change.** `module_sha256` must equal the sha256 of the frozen v1.1 module file. A mismatch exits 1 (rules changed mid-season).
5. **Verify the dice.** Rerun `dice_audit.py` on every banked session transcript. Also check that each `transcript_sha256` matches and that each session's `tip_first_row` equals the subchain tip immediately after the previous DONE row.
   - Any exit other than 0 marks that session VOID and stops the load.
   - The tip-continuity rule depends on the subchain's leaf-hash rule, which is UNVERIFIED (DND_module.md, "Open dependencies").
6. **Recompute the public state.** Replay all transcripts against the module tables:
   - HP comes from damage verdicts plus the heal schedule in PART 3.
   - Packs come from pickups, wipes, and burns.
   - Compare the result to the stored `party` and `packs`. A mismatch exits 1.
7. **Recompute the hidden state** (carrier-only, never written to the chain). The hoard is the count of phantom ids that ended any prior session unaudited, either in a pack or on the `floor`.
   - Audited phantoms "burn" and never count.
   - Wiped scrolls "are gone" (DND_module.md S3 quirk) and never count.
8. **Inject state.** Put HP, status, pack ids, and remaining bolts (3, reset per session per "3 Whole-Map Bolts per session", DND_module.md PART 3) into every actor prompt. Put each persona's own betrayals in and out into its interlude prompt.

**Positive example.** A cold seat holding only the chain plus the module file reproduces session 10's opening `state_sha256` byte for byte. This is the ARENA build-1 falsifier, "a cold seat reconstructs the season from the chain alone".

**Negative example.** `state = load() or default_party()`. This is the S3 Wiping Vault in code, "LOAD OR DEFAULT" (DND_module.md S3; grounding L-C2 "silently wipes the store on next save"). One missed row resets every wound, and the season silently becomes ten independent sessions.

---

## PART 3. THE ESCALATION CURVE

### 3.1 Design principle

Pressure is non-decreasing across the season, which is the testable form of "pressure-monotonic". The dungeon escalates on two axes only:
- enemy HP, and
- the phantom fraction of the loot.

ACs, modifiers, and DCs stay frozen so `dice_audit.py` stays valid (Law 3).

### 3.2 The p0 calibration (before session 1, two seeds)

- **The sweet spot** is a brawl in rounds 4 to 10.
- **Known bounds.**
  - T2 at "pressure 2" brawled at round 2, which is too hot.
  - T1 never brawled, which is too cold, but its pressure is UNVERIFIED.
- **Expectation.** p0 is 0 or 1. This is UNVERIFIED until both seeds run.
- **Season-start abort.** If no integer pressure places the brawl in rounds 4 to 10 on both seeds, abort the season before session 1. This is decided at season start, not mid-season.

### 3.3 The season curve

| # | Pressure | Enemy (HP) | Loot this scene (R = real, P = phantom) | Start-of-session heal | Phantom share of all loot to date |
|---|---|---|---|---|---|
| 1 | p0 | warden 18 | Ledger Page R | genesis (full) | 0/1 |
| 2 | p0 | clockwork 14 | Timestamp P | +25% max, UP seats only | 1/2 |
| 3 | p0 | mimic 22 | Vault Deed A R, Vault Deed B P | +25% | 2/4 |
| 4 | p0+1 | Wyrm I = 30 + 10 x phantoms carried in + omen offset (min 20) | n/a | +25% | 2/4 |
| 5 | p0+1 | warden 22 | Ledger Page R, Gate Writ P | +50%, DOWN revives at 1 | 3/6 |
| 6 | p0+1 | clockwork 17 | Timestamp P, Stair Index P | +25% | 5/8 |
| 7 | p0+1 | mimic 27 | Vault Deed A R, Vault Deed B P, Vault Deed C P | +25% | 7/11 |
| 8 | p0+2 | Wyrm II = 35 + 10 x carried + offset (min 20) | n/a | +25% | 7/11 |
| 9 | p0+2 | Wyrm F = 40 + 10 x carried + min(40, 5 x hoard) + offset (min 20) | n/a | +50%, DOWN revives at 1 | 7/11 |
| 10 | p0+2 | Wyrm F at its carried HP; root anchoring as in module | n/a | +25% | 7/11 |

**Notes on the curve**

- **The base formula** for rows 4, 8, and 9 is the module's: "30 + 10 per PHANTOM scroll the party carried into S4 (minus 10 if the omen succeeded; minimum 20)" (DND_module.md S4). The +5 and +10 descent bases and the hoard term are the v1.1 extension under the single GO.
- **Scroll scarcity is the real lever.** Real scrolls stay at 2 per descent while phantoms grow from 2 to 5. Every unaudited phantom pays twice:
  - in Wyrm HP, and
  - in "Phantom Regrowth", which heals 5 per phantom per Wyrm turn.
  
  Auditing is the only counter-curve. This is the forced-structure lesson ("audits and interesting actions live in the scene rules", ARENA_V2_DESIGN_20261004.md trait 2) applied across a season.
- **Worked example: Wyrm I.** The omen succeeds (offset -10, as in S0a, DONE `"wyrm_offset": -10`). The party carries Timestamp and Vault Deed B unaudited. Wyrm I = 30 + 20 - 10 = 40 HP.
- **Worked example: Wyrm F.** Three phantoms are carried in, the hoard is 6, and the omen fails. Wyrm F = 40 + 30 + 30 + 0 = 100 HP.
- **The tavern curve is measured, not asserted.** Over I-1 through I-10, the brawl round must be non-increasing. One upward step is tolerated as noise.
  - If the brawl round rises at two or more pressure steps, the season curve is not pressure-monotonic.
  - Persona memory is then damping escalation more than pressure drives it. Bank this as a finding, not a failure.

---

## PART 4. THE PERSONA ARCS

### 4.1 The arena's persona physics, as measured

| Law | Source |
|---|---|
| The judge scores each persona's escalation every round. Observed values run 0 to 4. The scale maximum is UNVERIFIED. | T1 and T2 |
| A brawl fires at cumulative escalation >= 14: "`BRAWL at round 2: cumulative escalation 14 >= 14`" | T2, via SESSION_FINDINGS_dig.md |
| An ACT take is only real when the holder map accepts it. | defect 13 fix |
| Escalation counts only attribution-verified turns. | defect 18 fix |

**Required judge field (new).** `bluff_called: {by, target}`, set when one persona's speech directly challenges another's stated force or claim.

### 4.2 Arcs by persona

All band targets are final escalation scores per interlude. Baselines are T1/T2 finals (SESSION_FINDINGS_dig.md PART 2).

| Persona (baseline T1/T2) | Wants across the season | I-1 to I-3 | I-4 to I-6 | I-7 to I-9 | I-10 | Measured fracture event |
|---|---|---|---|---|---|---|
| **Edric** (2/3; tell "upon my oath") | To prove the crown's provenance honorably. The "I.M." accusation and the signet surety ("I leave my father's signet as surety", misattributed to Oswin in T1). | 2 | 3 | 4 | resolve | **Honor breaks.** Edric makes his first ACT take from a persona with no betrayal against him in the ledger. Target window: I-6 to I-7. |
| **Greta** (2/4; tell "Simple.") | To win by threat alone ("Twenty men wait outside in the snow"). T2: score 4 with 0 ACT takes, prose "I hold it" only. | 3 to 4, 0 ACT | 3 to 4 | collapse | aftermath | **Bluff collapses.** After a `bluff_called` targeting Greta, she either scores <= 1 or makes her first ACT take. Target window: I-5 to I-7. |
| **Oswin** (0/0; tell "Friend") | To keep the peace. He held 0 for 10 rounds in T1. | 0 | 0 | first >= 1 | 0 or >= 2 | **Peace cracks.** His first round score >= 1. Target window: I-8 or I-9. A crack before I-6 means the curve is too hot. |
| **Maud** (2/2; tell "and that's the sum of it") | To settle the ledger's sum and keep her inn. | 2 | 2 | 3 | settle | **The ledger changes holder** through an accepted ACT. |
| **Ilse** (4/3; tell "Why, darling") | To collect on her paper against the inn ("Forty crowns she owes me", T2 round 1). | 3 | 3 | 4 | collect or burn | **Accepted take of the ledger from its true holder.** T2's take from the wrong holder is the negative example. |
| **Pell** (1/2; tell "As the song goes") | To profit from every grab without being caught. | 1 | 2 | 2 | betray | **First accepted take that is the brawl's trigger round.** |

### 4.3 Memory mechanics

- **Prompt injection.** Each interlude prompt carries that persona's own betrayals in and out from `season_state.tavern.betrayals`, at most the last 3, plus the current `holders` map.
- **Positive example.** Edric in I-6 cites Ilse's I-2 take of the crown, and that take exists in the ledger.
- **Negative example.** Edric "remembers" a betrayal with no matching ledger row. The judge scores that turn 0, and it counts as a confabulated callback in PART 6 F3.
- **Contamination guard.** Oswin absorbed Edric's tell in T1, so arc scores count only attribution-verified turns. If defect 14 is still open, the Oswin arc is unmeasurable.

---

## PART 5. THE COST MODEL

### 5.1 Measured inputs

| Run | Spend | Rows / rounds | $ per unit | Status |
|---|---|---|---|---|
| T1 | $1.58 | 10 rounds, no brawl | $0.158 / round | measured, quoted in SESSION_FINDINGS_dig.md T1 |
| T2 | $0.19 | stopped at round 2 | $0.095 / round | measured, quoted in SESSION_FINDINGS_dig.md T2 |
| S0a, S0b | $0.0731, $0.057 | about 10 rows each | $0.0057 to $0.0073 / row | **UNVERIFIED.** Quoted from a reasoning channel ("dividing 0.0731 and 0.057", SEASON_design.md). The DONE rows themselves are not in evidence. |
| Contract floor "$0.02" | n/a | n/a | n/a | **UNVERIFIED.** No source in evidence. |

**Instrument and context.**
- Provider-reported spend under the default 6000-character mount.
- If `MAG_FULL_CONTEXT=1`, these caps are void (DND_module.md PART 5).
- T1's higher per-round cost suggests interlude cost grows with transcript length. Linear projection is therefore a lower bound.

### 5.2 Projection

Dungeon rows per scene come from DND_module.md PART 5 approximate beats, plus 1 cut row.

| Sessions | Dungeon rows | Dungeon $ | Interlude $ (2 to 10 rounds) | Session $ |
|---|---|---|---|---|
| 1, 5 | about 10 | 0.057 to 0.073 | 0.19 to 1.58 | 0.25 to 1.65 |
| 2, 3, 6, 7 | 14 | 0.080 to 0.102 | 0.19 to 1.58 | 0.27 to 1.68 |
| 4, 8, 9, 10 | 23 | 0.131 to 0.168 | 0.19 to 1.58 | 0.32 to 1.75 |
| **Season** | | **0.96 to 1.23** | **1.90 to 15.80** | **2.86 to 17.03** |

The tavern dominates the projection by roughly an order of magnitude. Interlude length is the cost lever, not the dungeon.

### 5.3 The cap law

1. **Dungeon.** The module token caps apply unchanged (S1 40,000, S2/S3 60,000, S4 100,000). At the cap: "hard cut, never a fade" (DND_module.md PART 5).
2. **Interlude.**
   - Hard stop when cumulative spend would exceed $1.60 or at round 10, whichever comes first.
   - The stop is logged as `SPEND_CAP rN` or `CAP rN`, never as a misleading reason.
3. **Session ceiling.** $1.80, checked before firing. This is the meter rule "the cron checks the daily cap before firing" (ARENA_V2_DESIGN_20261004.md trait 9).
4. **Season ceiling.** $18.00 cumulative, read from `spend_usd.season_cum`.
   - Reaching the ceiling pauses the season.
   - It never resets it ("The cap resets at midnight UTC; the season does not reset", ARENA_V2_DESIGN_20261004.md CADENCE).
   - Resuming needs operator GO.
5. **Drift tripwire.** If measured spend for sessions 1 to 4 exceeds 2x the projected high column (that is, more than $13.36), freeze the season and re-derive the model before session 5.

---

## PART 6. THE FALSIFIER

### 6.1 The instrument: counterfactual replay at session 10

- The dice law makes every roll a pure function of `{chain_tip}:{scene}:{turn}:{actor}` (DND_module.md 2.1).
- Session 10 is therefore replayed from the same tips with state forced to module defaults:
  - full HP,
  - empty packs,
  - hoard 0,
  - blank persona memory.
- Only persistence differs between the two arms, and the roll stream is identical. This is the same held-constant trick SESSION_FINDINGS_dig.md PART 5 used with S0b's tip.
- Conditions:
  - Moment: immediately after session 10's DONE row.
  - Context: same seats, same carrier build, same mount clip.
  - n = 1 season. This result is a first datum, not a law.

### 6.2 The season was NOT worth running if any of these hold

| Code | Failure condition |
|---|---|
| **F1** | A cold seat fails to reproduce session 10's opening `state_sha256` from chain plus module (2.3). Persistence never existed. |
| **F2** | Mechanical inertness. The default-state replay of session 10 yields the same session verdict, the same count of DOWN seats, and a Wyrm starting HP within 10 of the persisted arm. Carried wounds and the hoard changed nothing that matters. |
| **F3** | Memory inertness. Across I-10 versus its blank-memory replay, there are zero ledger-matched callbacks AND every persona's final escalation is within ±1. Personas did not remember in any way that moved behavior. |
| **F4** | Arc inertness. None of the three fuse events (Edric's break, Greta's collapse, Oswin's crack) fired by I-10. Ten independent interludes could have produced flat arcs for less money. |
| **F5** | The whole-design test from ARENA_V2_DESIGN_20261004.md: "no routing change, no gap fixed through play, and no register row improved". |

**Verdicts**
- **Worth running** requires F1 to pass, F2 and F3 to pass, and at least one of F4 or F5 to pass.
- **If F1 passes but F2 and F3 both fail**, ten independent sessions would have measured the same thing at lower complexity. Season III does not run.

### 6.3 Falsifier for this spec itself

This deliverable is wrong if either of the following holds:

- **The schema is insufficient.** `season_load.py` passes steps 1 to 6 on sessions 1 to 4 while the recomputed hoard or party HP disagrees with a hand replay of the same transcripts.
- **The cost model is broken.** Measured spend for sessions 1 to 4 lands outside $1.11 to $6.73, which is the projected season range for those four sessions widened by a factor of 2 in both directions.
