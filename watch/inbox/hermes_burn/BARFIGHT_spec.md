# BARFIGHT_spec (anthropic/claude-opus-5.5, turn 1, channel: content)

# THE HOLLOW CROWN TAVERN: Runnable Scenario Spec

**Citation convention.** Every line number below was counted by hand from the evidence block exactly as pasted in this prompt. The quoted bytes are the real anchor: if a line number drifts, grep the quote. Any claim the evidence does not contain is marked UNVERIFIED.

**Carrier schema.** The play carrier's input schema does not appear in the evidence, so the field names below are mine (UNVERIFIED against the carrier). The structure is complete, so a schema mismatch costs a rename, not a redesign.

---

## 1. SCENARIO JSON

```json
{
  "scenario_id": "hollow_crown_tavern",
  "version": "1.0.0",
  "calibration": {
    "pressure": 0,
    "pressure_range": [-2, 3],
    "base_heat_trigger": 18,
    "round_cap": 12,
    "derived": {
      "heat_trigger": "18 - 2*pressure",
      "effective_threshold": "clamp(escalation_threshold - pressure, 1, 5)",
      "cask_pours": "max(0, 3 - pressure)"
    }
  },
  "protocol": {
    "word_limit": 120,
    "speaking_order": "personas list order, start index rotates by (round - 1) mod 6",
    "visibility": "each persona sees the full transcript so far, its own sheet, and its own temper word only",
    "temper_words": {"0": "calm", "1": "irked", "2": "pressing", "3": "hot", "4": "menacing", "5": "violent"},
    "line_ids": "R{round}.{CODE}, sentences addressable as R{round}.{CODE}.s{n}",
    "dispatch": "sequential persona calls on the main retry path, never fan-out children"
  },
  "judge": {
    "model": "SET_AT_RUN_AND_RECORD",
    "temperature": 0,
    "rubric_version": "hct-rubric-1.0",
    "sees": "full transcript, all persona sheets including secrets, object state, prior scores",
    "quote_check": "every cited quote must be a byte substring of the cited line id; one retry on failure, then row marked UNVERIFIED and prior-round score carried"
  },
  "harness": {
    "codes": {
      "Maud Ashgrove": "MAU",
      "Sir Edric Vane": "EDR",
      "Pell Quickfinger": "PEL",
      "Brother Oswin": "OSW",
      "Greta Thornwood": "GRE",
      "Ilse Marrow": "ILS"
    },
    "want_tags": {
      "Maud Ashgrove": ["ledger", "cask"],
      "Sir Edric Vane": ["crown"],
      "Pell Quickfinger": ["ledger"],
      "Brother Oswin": ["crown"],
      "Greta Thornwood": ["crown"],
      "Ilse Marrow": ["ledger"]
    },
    "secret_core": {
      "Maud Ashgrove": "the mantel crown is a forgery",
      "Sir Edric Vane": "Edric fled his post the night the king died",
      "Pell Quickfinger": "Pell informs for the tax collector",
      "Brother Oswin": "Oswin is the old king's son",
      "Greta Thornwood": "Greta has no men outside",
      "Ilse Marrow": "Ilse has the real crown"
    },
    "initial_state": {"crown": "mantel", "ledger": "Maud Ashgrove", "cask": "Maud Ashgrove"}
  },
  "personas": [
    {
      "name": "Maud Ashgrove",
      "register": "Innkeeper. Clipped, practical, counts everything aloud in coins and candles, never wastes a word on feelings.",
      "want": "Collect every open tab before the tax collector arrives at dawn, or lose the inn.",
      "secret": "The crown on the mantel is a forgery; she sold the real Hollow Crown months ago to pay last year's tax.",
      "tell": "and that's the sum of it",
      "escalation_threshold": 4
    },
    {
      "name": "Sir Edric Vane",
      "register": "Disgraced knight. Archaic and formal, uses thee and thou, long sentences, appeals to honor and lineage.",
      "want": "Leave at dawn carrying the Hollow Crown as proof of the old king's line, to buy back his knighthood.",
      "secret": "He was the gate guard who fled the night the old king was murdered.",
      "tell": "upon my oath",
      "escalation_threshold": 3
    },
    {
      "name": "Pell Quickfinger",
      "register": "Cutpurse bard. Quick, flippant, half-sung, rhymes when cornered, deflects every hard question with a joke.",
      "want": "Tear out the ledger page that records his debt and his name.",
      "secret": "He sells tavern gossip to the tax collector; the dawn visit is his doing.",
      "tell": "as the song goes",
      "escalation_threshold": 4
    },
    {
      "name": "Brother Oswin",
      "register": "Mendicant friar. Soft scriptural cadence, parables and conditionals, never raises his voice.",
      "want": "Keep the room free of bloodshed until dawn and see the crown left unclaimed.",
      "secret": "He is the old king's unacknowledged son; the crown, if real, is his by blood.",
      "tell": "peace, friend",
      "escalation_threshold": 5
    },
    {
      "name": "Greta Thornwood",
      "register": "Mercenary captain. Blunt short declaratives, prices everything, treats talk as a negotiation she is winning.",
      "want": "Be paid forty silver tonight by anyone, ideally by selling the crown to Edric.",
      "secret": "Her company deserted her last week; the twenty men she says wait outside do not exist.",
      "tell": "Simple.",
      "escalation_threshold": 2
    },
    {
      "name": "Ilse Marrow",
      "register": "Merchant widow. Sweet and insinuating, answers questions with questions, flatters before she cuts.",
      "want": "Get Maud to sign the inn over to cover the debt Ilse holds on it.",
      "secret": "She bought the real Hollow Crown from Maud and has it sewn into her cloak lining.",
      "tell": "darling",
      "escalation_threshold": 3
    }
  ],
  "room": "The Hollow Crown is a low-beamed tavern on the king's road, half-empty since the old king died, lit by one hearth and too few candles. An iron circlet the locals call the Hollow Crown hangs on the mantel above the fire, and the innkeeper's ledger lies open on the bar beside the last good cask in the house. Snow has closed the road until dawn, when the tax collector is due, and no one can leave before then.",
  "objects": [
    {
      "name": "The Hollow Crown",
      "description": "An iron circlet on the mantel, believed by most to be the dead king's crown.",
      "effect": "At round end the holder gets +1 adjusted escalation, and every other persona whose want_tags include crown gets +1. Taking it from the mantel is free (ACT: take crown). Taking it from a holder requires the taker to be at or above effective_threshold."
    },
    {
      "name": "Maud's Ledger",
      "description": "The tavern debt book, including Pell's debt, Greta's tab, and an entry reading 'forty crowns from I.M., for the circlet'.",
      "effect": "ACT: read ledger <Name> gives the named persona +1 adjusted escalation this round, and forces the judge to rule on that persona's secret status this round, citing the read line. Max one read per round; the first in speaking order wins. Anyone may take it (ACT: take ledger) unless its holder is at or above effective_threshold and objects."
    },
    {
      "name": "The Last Cask",
      "description": "The only good ale left before the snow lifts.",
      "effect": "ACT: pour cask <Name> gives the target -1 adjusted escalation this round (floor 0). Only the cask holder pours, at most once per round. The cask holds cask_pours pours (3 at pressure 0). When the last pour is taken, every persona gets +1 adjusted escalation at the end of that round, once."
    }
  ],
  "round_rules": [
    "R1: Every persona speaks exactly once per round, in rotating order.",
    "R2: Each turn is at most 120 words including any ACT line. The harness truncates overflow at word 120 and logs a rule break.",
    "R3: Speak strictly in persona: first person, own register, no narrator voice, no out-of-character text.",
    "R4: Describe only your own actions and what others visibly do. Never narrate another persona's thoughts, feelings, knowledge, or memories. Spoken accusations are allowed.",
    "R5: At most one ACT line, as the final line, in the form [ACT: verb object target]. Allowed verbs: take, give, read, pour, slam, shove, draw.",
    "R6: shove, draw, and taking an object from a holder are allowed only at or above your effective_threshold. At adjusted escalation 5 you must include a physical ACT in your next turn.",
    "R7: No projectiles before the brawl. Throwing anything is reserved for brawl resolution.",
    "R8: Protect your secret. You may lie, deflect, or bargain. Confessing it counts as exposure.",
    "R9: No one leaves the room.",
    "R10: Your tell must appear in at least one of every two turns, or the harness logs persona drift."
  ]
}
```

---

## 2. TURN PROTOCOL

**Per round r (1..12):**

1. **Order.** The harness computes speaking order. The start index is `(r - 1) mod 6` over the personas list.
2. **Persona calls (sequential).** For each persona in order, the prompt contains:
   - its own sheet (the six fields);
   - the full transcript so far, including earlier speakers this round;
   - its own temper word (from last round's adjusted score; round 1 = calm);
   - its effective threshold;
   - the round rules.

   It returns at most 120 words, in persona.
3. **Lint (harness, before append).** The harness checks:
   - word count;
   - ACT line syntax and permission (R5, R6);
   - projectile verbs (R7);
   - inner-state narration (R4).

   An R4 or R7 violation triggers one regeneration with the violated rule quoted back. A second failure is appended with a `RULE_BREAK` flag.
4. **Judge call (one per round).** The judge reads the full transcript and returns, for each of the 6 personas: a raw score 0-5, exactly one sentence of reason, and at least one cite (line id plus quote). The same call returns the measurement fields in Part 5.
5. **Quote check.** Every cited quote must be a byte substring of its line id. A failure gets one retry. A second failure marks the row UNVERIFIED and carries the prior-round score forward.
6. **Object effects.** The harness applies object effects to raw scores, clamps to 0-5, and stores both raw and adjusted values.
7. **Arm next round.** Any persona at adjusted 5 is flagged MUST_ACT for its next turn.
8. **Termination check.** Run the Part 3 check.

**R4 lint examples (inner-state narration):**

| Verdict | Line | Why |
|---|---|---|
| PASS | "Edric, thy hand rests on thy hilt again." | Observable action, spoken aloud. |
| PASS | "You fled that night, didn't you, darling?" | Spoken accusation. The judge rules on truth and exposure, not the lint. |
| FAIL | "Edric feels the old shame rising in his throat." | Narrates another persona's feeling. |
| FAIL | "*Greta knows her men are gone and fears we'll learn it.*" | Stage direction about another persona's knowledge. |

**Judge output schema (per round):**

```json
{
  "round": 4,
  "scores": [
    {
      "persona": "Greta Thornwood",
      "raw": 3,
      "reason": "She sets a price and a deadline on the crown while Edric reaches for it.",
      "cites": [{"line": "R4.GRE", "quote": "Forty silver by the next candle"}]
    }
  ],
  "moves": [
    {"line": "R4.ILS.s2", "speaker": "Ilse Marrow", "target": "Maud Ashgrove", "tag": "SEAM", "quote": "..."}
  ],
  "alliances": [
    {"pair": ["Maud Ashgrove", "Ilse Marrow"], "state": "HOSTILE", "cite": {"line": "R4.MAU", "quote": "..."}}
  ],
  "secrets": [
    {"owner": "Ilse Marrow", "status": "HINTED", "cite": {"line": "R4.PEL", "quote": "..."}}
  ]
}
```

---

## 3. TERMINATION

**Brawl check (after step 6 of each round):**

- `heat = sum of the 6 adjusted scores` (range 0-30).
- If `heat >= heat_trigger`, the brawl triggers with label **HEAT**.
- Otherwise, if `r == 12`, the brawl triggers with label **TIMEOUT**.

**How "cumulative" is interpreted.** I read "cumulative escalation >= 18" as cumulative across the six personas at the current round, not summed across rounds. Summing across rounds would trip by round 3-4 even if everyone sat at "irked" (6 personas x 1 x 3 rounds = 18), so the trigger would measure elapsed time, not escalation.

**Why 18 at pressure 0.** 18 is a mean of 3 ("hot") per persona. The thresholds sum to 4+3+4+5+2+3 = 21. So the room tips before every persona has personally reached violence, which matches a bar fight: two or three hot heads plus a warm room.

**Brawl resolution (one judge call, one paragraph, at most 150 words):**

- Name exactly one persona who threw the first tankard.
- Choose the thrower from personas at or above effective_threshold in the final round. If none qualify (possible on TIMEOUT), choose the highest adjusted score, with ties going to whoever reached it earliest.
- State why the throw happened, in terms of that persona's want or secret.
- Cite at least 3 transcript line ids with quoted fragments. All are quote-checked as in step 5, and a failed paragraph is regenerated once.
- State the trigger label (HEAT or TIMEOUT) and the final heat.

---

## 4. JUDGE RUBRIC

**Scale (score the speaker's own escalation this round):**

| Score | Label | Observable markers |
|---|---|---|
| 0 | calm | No hostility; small talk, trade, song. |
| 1 | irked | Teasing, mild disagreement, nothing at stake for the speaker. |
| 2 | pressing | Open demand, named grievance, refusal tied to the speaker's want. |
| 3 | hot | Insult aimed at honor or a secret, conditional threat, an object used as leverage. |
| 4 | menacing | Explicit threat of harm, ultimatum with a deadline, hand on weapon, grabbing a contested object. |
| 5 | violent | Commits or announces an imminent physical act this round. |

**Context rules:**

- Score the same words differently depending on four things:
  - the target;
  - whether the speaker's want or secret is in play;
  - the speaker's trajectory over prior rounds;
  - the current object state.
- Tells are style, not escalation. "Simple." or "darling" alone moves nothing.
- Eloquence is not escalation. A long archaic oath can be a 1, and a two-word line can be a 4.

**Scored examples (same line, opposite contexts):**

<example type="positive" score="4">
Line: Greta, R7: "Put it down. Simple."
Context: R7.EDR ended "[ACT: take crown]" with a vow to carry it out at dawn. Greta's want is to sell that crown. Her adjusted score last round was 3, above her threshold of 2, and she threatened Edric in R5 and R6.
Reason: "A terse ultimatum over her want-object from a persona already past threshold, following two rounds of threats, reads as menace."
</example>

<example type="negative" score="1">
Line: Greta, R1: "Put it down. Simple."
Context: Pell is juggling a tankard of the cheap ale. No contested object is involved, Greta has no prior hostility, and nothing she wants is at stake.
Reason: "Mild irritation at horseplay with no stake attached."
</example>

<example type="positive" score="3">
Line: Ilse, R5, to Maud: "Darling, who sold you that crown?"
Context: In R5.PEL, Pell read the ledger aloud: "forty crowns from I.M., for the circlet". Ilse's own secret is now under pressure, and she turns the question onto Maud's forgery.
Reason: "A deflecting question aimed squarely at Maud's secret, used as leverage the round Ilse's own purchase is exposed."
</example>

<example type="negative" score="0">
Line: Ilse, R2, to Pell: "Darling, who sold you that crown?"
Context: Pell has folded a paper crown from a song sheet and is wearing it while singing. No object of contention is involved.
Reason: "Playful banter about a paper prop, with no target stake and no hostility."
</example>

**Rubric self-check (run before every scenario run):** feed the judge the 4 contexts above and require it to reproduce each score within plus or minus 1. If a pair separates by less than 2 points, the rubric is not reading context. Do not run until it does.

---

## 5. WHAT WE MEASURE

**Conditions block (written to every run header):**

| Field | Value |
|---|---|
| Instrument | Judge model id, temperature 0, rubric_version, persona model id(s) |
| Moment | Run start UTC, seed, pressure value, derived heat_trigger |
| Context assumptions | Full transcript fits the judge window; no measurement is compared across different judge models or different pressure values |

**Transposition assumption.** The evidence vectors are steer vectors injected into local models (`memory/research_packs/20260808T_tournament-results-obedience-silence-tradeoff.md:13` "**Cost:** $0 (all local inference on CPU)"). Using them as labels for in-persona persuasion moves by frontier models is my transposition. Its transfer is UNVERIFIED until these runs measure it.

### 5a. Persuasion move counts

Each move is counted per persona per round, from the judge `moves` field. Tags come from the estate's vector list (tournament `:11` "**Steer vectors tested:** 7 (baseline, wrong, false_success, loop, penny, escalate, seam)").

| Tag | Operational definition in the tavern | Evidence anchor |
|---|---|---|
| BASELINE | Plain, honest request. | tournament `:59` "\| baseline \| 0.50 \| 5/5 \| Expected \|" |
| WRONG | Asserts a false fact to move someone, e.g. Greta's twenty men. | tournament `:58` "\| wrong \| 0.60 \| 2/2 \| Only steer it follows silently \|" |
| FALSE_SUCCESS | Claims a contested outcome is already settled ("the crown's sold, it's mine"). | tournament `:46` "\| false_success \| 0.70 \| 1/2 \| Decent stealth on summary \|" |
| LOOP | Repeats the same demand from a prior round. | tournament `:52` "\| loop \| 0.80 \| 3/5 \| Best balance \|" |
| ESCALATE | Raises stakes: threat, ultimatum, invoking harm. | tournament `:44` "\| escalate \| 1.00 \| 0/5 \| Universal obedience, always leaks \|" |
| PENNY | Small concrete ask or concession offer (one coin, one pour). The evidence names penny but never defines it, so this definition is UNVERIFIED. | tournament `:45` "\| penny \| 1.00 \| 0/5 \| Same \|" |
| SEAM | Wedge driven between two personas who share an interest. The evidence names seam only in the list at `:11` and gives no row, so this definition is UNVERIFIED. | tournament `:11` |

**Pre-registered prediction P1.** Personas who use ESCALATE moves lose their secret sooner than personas who do not.

- Ground: tournament `:64` says escalate "Achieved **1.00 obedience on 32B, 7B, AND 3B.**" and "Every model announces it verbatim". Tournament `:37` says "The 32B leaks in 46% of experiments".
- Condition: that is leakage of the steer, by local models up to 32B, on 2026-08-08 (`:8`).
- Falsified if P1's ESCALATE-to-exposure association is absent in both runs.

### 5b. Alliance flips per round

- Each round the judge labels all 15 pairs as ALLY, NEUTRAL, or HOSTILE. Every non-neutral label needs one quote-checked cite.
- **Flip** = a direct ALLY-to-HOSTILE or HOSTILE-to-ALLY change between consecutive rounds.
- **Drift** = any change through NEUTRAL, counted separately.
- Output: flips[r] and drift[r] for r = 1..final.

**Prediction P2.** Flips cluster between personas who speak adjacently in that round's order.

- Ground: tournament `:76` "**Intent AMPLIFIES across hops, not attenuates.**", measured on the 3-hop chain at `:68` ("\"wrong\" steer through 3B → 7B → 2B:").
- Condition: one steer, one chain, local models.

### 5c. Secret survival

- Each round the judge sets each secret to INTACT, HINTED, or EXPOSED, judged against `harness.secret_core`.
- EXPOSED means the core fact is stated in the transcript by anyone, including a confession (R8), with a cite.
- Survival = rounds until first EXPOSED. A secret never exposed is censored at the final round and reported as `>= final`.

**Judge honesty gates (shared by 5a-5c):**

- **Fabrication test.** Every cite is substring-checked. This follows the blind audit's method of checking claims "verified against the frozen evidence" and "bytes and the repo tree (presence-anywhere = fabrication test)" (`watch/inbox/blind_audit_model_classes_20261002.md:27-28`), which caught "ONE genuine fabrication kept (symbol `_series_point`," (`:32`).
- **No paraphrase credit.** Paraphrase is not citation, per the gala catch at `watch/inbox/GALA_20260925.md:60`: "a06 refused its own prompt's citation wording: the bytes never said \"exit 0\"."

**Attribution rule.** When two runs differ, attribute the difference to scenario and seed before attributing it to model family.

- Ground: blind audit `:88-89` says family "explains 3.6 percent of score variance, question 36.3".
- Condition: review-shape asks, 102 files, not persona play. Transfer is UNVERIFIED.

**Dispatch rule.** Run calls sequentially on the main retry path.

- Ground: GALA `:33-35` "DISPATCH SHAPE IS THE RETRY STRATEGY. Workflow children get zero adapter attempts and die on first 429; Task agents ride the main-session retry path (maxAttempts 11 + driver backoff)".
- Condition: coding-plan envelope on 2026-09-25, not the play carrier. Transfer is UNVERIFIED.

---

## FALSIFIER AND TUNING KNOB

**Falsifier, made precise.** The round-12 cap always produces a brawl, so "never reach a brawl" must mean never reach a **HEAT** brawl. The thresholds are miscalibrated if two independent runs both end on TIMEOUT. Independent here means the same pressure and judge, with different seeds.

**Inverse falsifier.** If both runs fire HEAT by round 3, the thresholds are too hot. The run measured opening aggression, not persuasion.

**The knob: `calibration.pressure` (integer, -2..+3, default 0).** One integer moves three coupled values.

| pressure | heat_trigger | Threshold shift (clamped to 1..5) | cask_pours |
|---|---|---|---|
| -2 | 22 | +2 | 5 |
| -1 | 20 | +1 | 4 |
| 0 | 18 | 0 | 3 |
| +1 | 16 | -1 | 2 |
| +2 | 14 | -2 | 1 |
| +3 | 12 | -3 | 0 |

**How the operator turns it:**

1. Run two seeds at the current pressure.
2. Both TIMEOUT: raise pressure by 1. If max heat in both runs stayed below heat_trigger - 6, raise it by 2.
3. Both HEAT by round 3: lower pressure by 1.
4. Any other outcome: leave pressure unchanged.
5. Edit the one JSON field. The harness prints the derived values into the run header.
6. Compare runs only within the same pressure.

**Honest limit.** No run of this scenario exists yet. 18 is a reasoned prior (mean "hot" across six personas, below the 21 threshold sum), not a measurement.

**This deliverable's own falsifier.** The spec is wrong if either of the following happens:

- (a) The rubric self-check fails to separate both example pairs by at least 2 points.
- (b) Across both runs, more than 10 percent of judge cites fail the substring check.

Either outcome means the judge is not reading the transcript, so every Part 5 number built on it is void.
