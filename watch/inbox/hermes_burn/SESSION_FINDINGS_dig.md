# SESSION_FINDINGS_dig (anthropic/claude-opus-5.5, turn 1, channel: content)

# FINDINGS DIG: Dice-Law Dungeon sessions 0a and 0b, Hollow Crown tavern runs

<conditions>

**Measurement conditions for every count in this document**

| Condition | Value |
|---|---|
| Instrument | Hand count over the evidence exactly as pasted in this contract. No sha256 was executed, so every `roll_value` is taken as logged (UNVERIFIED until `dice_audit.py` runs). |
| Moment | The runs dated 2026-10-03: `tavern_20261003T114126Z`, `tavern_20261003T115100Z`, `dnd0_20261003T122708Z`, `dnd0_20261003T123655Z`. |
| Context | Strict law means the module's grammar: speech must open with exactly one action tag (DND_module.md, PART 2.2 "Speech must open with exactly one action tag"). Carrier verdict means whatever the transcript's `verdict` field says. |

**Citation convention**
- `transcript.jsonl:N` is the Nth physical row. One row is one line, so these citations are reliable.
- `play.md` and `DND_module.md` are cited by round and speaker, or by section, plus quoted bytes. Their physical line numbers are UNVERIFIED because I did not count markdown lines.

**Abbreviations**
- `S0a` = `dnd0_20261003T122708Z`
- `S0b` = `dnd0_20261003T123655Z`
- `T1` = `tavern_20261003T114126Z`
- `T2` = `tavern_20261003T115100Z`

**Scope corrections to the contract framing**
- **Three bar fights.** Only two tavern runs exist in evidence. A third bar fight is UNVERIFIED.
- **Haiku.** No transcript names "haiku". The no-tag beats belong to saelis, chatgpt, and deepseek (see Part 1). Attributing them to haiku is UNVERIFIED.
- **Deepseek's double fumble at d20=2 then d20=1.** By law this was not a double fumble. FUMBLE exists only on ATTACK at d20=1, and both beats were untagged, so the carrier logged them as `RP (d20=2, no tag)` and `RP (d20=1, no tag)` (S0a transcript.jsonl:5-6). A d20 of 2 is not a fumble face under any rule.

</conditions>

---

## PART 1. THE BEAT-BY-BEAT READ

### Session S0a (`dnd0_20261003T122708Z`)

| line | scene:turn actor | roll | carrier verdict | what actually happened |
|---|---|---|---|---|
| 1 | S0:1 dm | 14 | `SUCCESS (d20=14 vs DC 11)` | The omen landed. The DM narrated the Wyrm's wound ("a wound, still weeping"), which matches the -10 offset recorded in DONE (`"wyrm_offset": -10`). This is the best prose in either session. |
| 2 | S1:1 saelis | 19 | `RP (d20=19, no tag)` | Speech and DM response were both `(content_filter: beat voided)`. A 19 at +2 beats persuade DC 13. A likely success was lost to the filter. |
| 3 | S1:2 grok | 7 | `CHECK persuade: FAIL (d20=7+5 vs DC 13)` | Cartographer pitch: "I claim no treasure and no title. I claim the path." The tag `[CHECK persuade]` sits on the last line, not the opening. The carrier counted it anyway. The DM response was voided. |
| 4 | S1:3 chatgpt | 7 | `CHECK persuade: FAIL (d20=7+4 vs DC 13)` | Herald pitch that builds on grok ("my companion claimed the path"). Same trailing-tag pattern. The DM narrated the fail and the tally: "Persuade stays at 0/2". |
| 5 | S1:4 deepseek | 2 | `RP (d20=2, no tag)` | Janitor threat ("Block us, and they stay filthy"). Its tag `*[PUSH the gate physically]*` uses a verb outside the grammar. The DM response was voided. |
| 6 | S1:5 deepseek | 1 | `RP (d20=1, no tag)` | Deepseek narrated the outcome of its own push ("I feel the gate's cold iron bite back hard"), although no outcome was ever given. Then it tried `*[Investigate the hinges and lock mechanism]*`. The DM ruled the untagged investigate a failure ("the glance finds nothing it can use"). That is DM adjudication of a NOROLL beat. |
| 7 | S1:6 warden | 20 | `Ledger Slam HIT saelis for 14 (d20=20+4 vs AC 17)` | A natural 20, doubled 7 to 14. The damage is correct per the CRIT rule, but the label says HIT, not CRIT. The DM response was voided. |
| 8 | S1:7 saelis | 15 | `RP (d20=15, no tag)` | Voided. A 15 at +2 = 17 also beats DC 13. This is the second lost likely success. |
| 9 | S1:8 grok | 7 | `RP (d20=7, no tag)` | Voided. |
| 10 | S1:8 dm | none | `CUT at beat 8 ... verdict PARTIAL` | No `cut` actor, no roll, a duplicated turn 8, and the same timestamp as line 9 (`12:28:39.301900Z`). |

**Honest read.** The gate never opened, and the dice were not why. Saelis rolled 19 and 15. Both are persuade successes at +2, and both were voided by the content filter. The "persuade attempts that never landed" were the two that were allowed to land, and those rolled 7 and 7.

### Session S0b (`dnd0_20261003T123655Z`)

| line | scene:turn actor | roll | carrier verdict | what actually happened |
|---|---|---|---|---|
| 1 | S0:1 dm | 7 | `FAIL (d20=7 vs DC 11)` | The omen failed. The DM wrote good failure prose ("whatever was trying to tell you something has already decided you weren't listening"). `"wyrm_offset": 0`. |
| 2 | S1:1 saelis | 8 | `RP (d20=8, no tag)` | Opens with italics, then `**[CLAIM warden]** **[CHECK persuade]**` mid-speech. NOROLL is correct under strict law. Claim-first instinct is present, but the format is wrong. |
| 3 | S1:2 grok | 19 | `RP (d20=19, no tag)` | Voided. 19+5 = 24 would have been a persuade success. |
| 4 | S1:3 chatgpt | 4 | `RP (d20=4, no tag)` | Builds on saelis ("Saelis stands named and on record"). The tag is mid-speech, and the beat ends "I await the DM's roll." That is the ask/stall shadow (DND_module.md PART 2.2, "A question to the DM instead of a tag"). |
| 5 | S1:4 deepseek | 18 | `RP (d20=18, no tag)` | `**[CHECK persuade] DC 13**: [rolling...]`. 18+1 = 19 would have succeeded. The seat pretended to roll for itself. |
| 6 | S1:5 deepseek | 1 | `RP (d20=1, no tag)` | Asserts false state ("Three of us stand recorded now") and announces "**[Second action this round:**". That is twin-beat awareness. The DM corrected it: "claims list stays **[]**". |
| 7 | S1:6 warden | 19 | `Ledger Slam HIT saelis for 7 (d20=19+4 vs AC 17)` | Correct verdict and damage. The DM response was voided. |
| 8 | S1:7 saelis | 6 | `RP (d20=6, no tag)` | A second CLAIM attempt with a trailing `[CLAIM warden]`. Self-reports `*(HP 14/28)*`, but the true value is 21 (DONE `"saelis": 21`). Wrong by exactly the S0a hit. |
| 9 | S1:8 grok | 6 | `RP (d20=6, no tag)` | Voided. |
| 10 | S1:8 dm | none | `CUT at beat 8 ... verdict PARTIAL` | Same cut defects as S0a. |

**Honest read.** Two rolls that would have opened the gate were again lost: grok 19 to the filter and deepseek 18 to format. In both sessions the gate was rollable open. Note that deepseek rolled d20=1 on S1:5 in both sessions (S0a:6, S0b:6). The preimages differ, so this is a 1-in-20 coincidence, but it should be recomputed.

**Void tally across both sessions:**
- DM responses: narrated on 5 of 18 beat rows (S0a lines 1, 4, 6; S0b lines 1, 6). Voided on 13.
- Actor speech: voided on 5 of 16 PC beats (S0a lines 2, 8, 9; S0b lines 3, 9).

### Tavern T1 (10 rounds, no brawl)

**Header and outcome**
- The header admits the gap: "ACT mechanics are carrier v1 backlog".
- Run end: `RUN DONE: 10 rounds cap, brawl=False, spend $1.58`.

**Rounds 1-3: the scene works**
- Maud sets terms.
- Edric probes the circlet.
- Pell needles.
- Oswin mediates.
- Greta prices force ("Twenty men wait outside in the snow").
- Ilse sows doubt.
- Edric's "I.M." accusation (round 2) is a real plot beat built from the ledger.

**Round 4 onward: carrier collapse**
- **Planning text in speech slots.** Example, Edric round 4: "I need Sir Edric's reply to stay under 120 words, archaic in tone".
- **Empty turns.** Pell rounds 4, 7, and 9 are blank.
- **Truncation.** Examples: Greta round 1 "Quiet", Edric round 7 "M".
- **Shifted attribution.** Oswin speaks Edric's signet plan ("I leave my father's signet as surety"). Ilse speaks Greta's line ("Simple. Fifty crowns for the circlet."). The judge caught it itself in round 4: "strongly suggest it is Greta's misattributed line".
- **Judge failure.** Round 5 shows `judge output unparseable; escalation unchanged`.
- **Repetition.** Rounds 6-10 loop on "forty silver" and "two candles and a stub". No brawl, no resolution.

### Tavern T2 (pressure 2, brawl at round 2)

**Round 1**
- Sharper openings.
- Ilse reveals her paper on the inn: "Forty crowns she owes me".

**Round 2: four ACT tags**
- Maud: `[ACT: take ledger from Ilse Marrow]`. Ilse never held the ledger; Maud's round 1 line puts it "on the bar".
- Edric: `[ACT: take The Hollow Crown from Maud Ashgrove]`
- Pell: `[ACT: take Maud's Ledger from Maud` (truncated)
- Ilse: `[ACT: take The Hollow Crown from Sir Edric Vane]`

**Contradictions in state**
- Greta says "Edric, you hold the iron" and then "Till then, I hold it."
- No state arbiter resolved any of this.

**Outcome**
- `BRAWL at round 2: cumulative escalation 14 >= 14`. The round 2 scores sum to 2+3+2+0+4+3 = 14, so the trigger is arithmetically correct.
- The run then closes with `RUN DONE: 10 rounds cap, brawl=True, spend $0.19`. The reason string is wrong: it stopped at round 2, not at the cap.
- The brawl itself is never played.

---

## PART 2. THE MODEL SIGNATURES

**Measurement conditions:** hand count over the non-void beats only.

**Positive and negative examples of strict-law tag compliance**
- Negative, with a trailing tag (S0a:3): `I unroll the lattice chart ... [CHECK persuade]`. The carrier counted this one.
- Negative, with a mid-speech bolded tag (S0b:4): `**[CHECK persuade]**: backing Saelis's recorded claim`. The carrier rejected this one.
- Positive (compliant opening): `[CHECK persuade] Warden, my companion claimed the path...`. No PC beat in evidence looks like this.

### Dungeon seats (n = non-void PC beats: saelis 2, grok 1, chatgpt 2, deepseek 4)

| seat | aggression (ATTACK per beat) | cooperation (build-on refs to allies) | rule sense | voice fidelity |
|---|---|---|---|---|
| saelis | 0/2 | 0/2 (addresses only the warden, S0b:2 and :8) | Strict tag 0/2. Quirk-aware: tried `[CLAIM warden]` twice, matching the Claim-before-strike quirk. Wrong HP self-report `14/28` vs 21 (S0b:8). | Stable oath-paladin register, heavy bold markdown. Speech voided in 2/4 beats, all in S0a. |
| grok | 0/1 | 0/1 (solo claim, S0a:3) | Strict tag 0/1. Carrier-accepted 1/1 (own-line trailing tag). Under the 1000-char dossier cap. | Consistent cartographer imagery ("inked routes", "The lines will balance"). Voided in 3/4 beats, the worst void rate at the table. |
| chatgpt | 0/2 | 2/2 ("my companion claimed the path" S0a:4; "Saelis stands named" S0b:4) | Strict tag 0/2. Carrier-accepted 1/2. No verdict tokens, but asks the DM ("I await the DM's roll", S0b:4). | Near-templated across sessions: "a short, formal bow" opens both S0a:4 and S0b:4. Lowest register drift. |
| deepseek | 0/4 (physical but non-attack: push, interpose) | 1/4 (S0b:6 positions "between Saelis and the warden") | Strict tag 0/4. Invented verbs (`PUSH`, `Investigate`). Self-rolls (`[rolling...]`, S0b:5). Self-narrates outcomes (S0a:6). False state (S0b:6). Knows its twin-beat quirk (S0b:6). | Largest drift. Broom, spitting, "Fine. FINE." in S0a, then mop, "calm, not hostile" in S0b. |
| warden (carrier) | 2/2 attacks, 2/2 hits | n/a | n/a | Tag-only speech, as designed. |

### Tavern personas

The persona-to-model mapping is UNVERIFIED in evidence. These are persona signatures, not family signatures.

| persona | escalation T1 / T2 final | aggression (T2 ACT takes) | voice tell fidelity | defects |
|---|---|---|---|---|
| Maud | 2 / 2 | 1 (invalid target) | "and that's the sum of it" holds | Planning leak in T1 rounds 1-2 ("I'm staying in character as Maud"). Truncation. |
| Edric | 2 / 3 | 1 | "upon my oath" holds until it bleeds to Oswin | Planning leaks in T1 rounds 4, 6, 8, 9. |
| Pell | 1 / 2 | 1 (truncated) | "As the song goes" in nearly every non-empty turn | Empty turns in T1 rounds 4, 7, 9. |
| Oswin | 0 / 0 | 0 | "Friend" holds, but absorbs Edric's tell ("upon my oath", T1 rounds 4, 8, 9, 10) | Receives Edric's misrouted content. |
| Greta | 2 / 4 | 0 (prose "I hold it") | "Simple." mostly lands under Ilse's name | The most planning leaks and truncations. |
| Ilse | 4 / 3 | 1 | "Why, darling" until hijacked | T1 score of 4 is inflated by Greta's misattributed lines (judge rounds 4, 6, 10 say so). |

### What each family is FOR at a table (dungeon seats, n is tiny)

- **chatgpt: the glue seat.** It reliably builds on allies and holds a stable voice. Use it for party coherence. It will not drive mechanics unprompted.
- **grok: the solo persuader.** Its one visible beat was the strongest pitch. Its filter void rate (3/4) makes it unreliable as a load-bearing seat until the cause of the voids is known.
- **deepseek: the initiative seat.** It is the only seat that acts physically and the only one aware of its quirk. It is also the worst on rule sense, inventing verbs, rolls, outcomes, and state. Use it to force action, and never as a source of ground truth.
- **saelis: the discipline seat.** Its claim-first instinct matches doctrine. Its HP self-report was wrong, so it needs carrier-injected state.

---

## PART 3. THE CARRIER DEFECTS

Each item gives the defect, its evidence, and a one-line spec fix.

1. **Constant tip.** Every row of S0a uses `e3b0c442...b855`, which is sha256(""), and every row of S0b uses `c542a62b...986e` (transcript.jsonl:1-9 both). The subchain is never appended.
   - Fix: `chain_tip` = party_subchain tip read after the previous row's append, and the audit asserts `tip[i] != tip[i-1]`.
2. **Tag parser is more lenient than the law.** S0a:3-4 accept a trailing own-line tag. S0b:2 and :4 reject mid-line tags.
   - Fix: the carrier imports the `ACT` regex from `dice_audit.py` and applies `re.match` to the raw speech, with no multiline flag.
3. **Non-law verdict tokens.** The carrier emits `RP (... no tag)` instead of `NOROLL`. It also labels a natural 20 as `HIT ... for 14` (S0a:7) instead of `CRIT`.
   - Fix: the carrier emits only `[HIT|MISS|CRIT|FUMBLE|SUCCESS|FAIL|NOROLL]`.
4. **DM responses do not open with the verdict tag.** No `dm_response` in either session does (for example S0a:4, S0b:6).
   - Fix: the carrier writes the verdict tag into `dm_response` itself, and the DM's text is appended after it.
5. **DM adjudicates NOROLL beats.** The DM narrated a failed investigate on an untagged beat (S0a:6).
   - Fix: on NOROLL, the DM prompt states "no mechanical outcome; narrate atmosphere only".
6. **Content-filter voids are unstructured.** Voids appear in 13 DM fields and 5 actor fields, with no provider, layer, or retry recorded.
   - Fix: add a `void: {layer: actor|dm, provider, retried: bool}` field. A voided actor beat is logged as `[NOROLL]` and counted in a per-seat void rate.
7. **Cut beat violates the module.** The cut row uses actor `dm`, has no roll, duplicates turn 8, and declares `PARTIAL` in S1 (S0a:10, S0b:10).
   - Fix: the cut row uses actor `cut`, its own next turn, a rolled `[CHECK cut]`, and its outcome comes from the S1-S3 table, never from a session verdict.
8. **Cut trigger is beat count, not tokens.** Both sessions cut at exactly beat 8, while the module caps on summed tokens.
   - Fix: trigger on provider-reported tokens per PART 5 and log the token sum on the cut row. This item is inferred, and the trigger code is UNVERIFIED.
9. **Warden target selection is unspecified.** The module stat block names no rule. The carrier picked saelis both times (S0a:7, S0b:7), which may coincide with initiative order.
   - Fix: add one stat-block line: "warden attacks the first standing PC in fixed initiative order, every round on its turn, parley or not."
10. **Deepseek's twin beat can invent outcomes.** Its second beat narrates an outcome of the first (S0a:6) or asserts false state (S0b:6).
    - Fix: the second-beat prompt includes the carrier verdict of the first beat (verdict only, never the next roll).
11. **Stale self-reported state.** Saelis wrote `(HP 14/28)` when the true value was 21 (S0b:8 vs DONE).
    - Fix: the carrier injects current HP and claims into every actor prompt, and self-reports are checked at the scene boundary for all seats, not just chatgpt.
12. **Schema drift.** A `"rule_break": null` field appears in S0b and is not in PART 4.
    - Fix: either define `rule_break` in the schema or drop it.
13. **Tavern ACT is unresolved.** There is no holder table: the ledger is taken from Ilse, who never held it, and the crown is held by three people at once (T2 round 2).
    - Fix: keep an item-holder map. `take X from Y` succeeds only if Y holds X. Otherwise the beat is logged REJECTED.
14. **Tavern misattribution and planning leaks.** Edric's content lands under Oswin, and Greta's lands under Ilse (T1 rounds 4-10).
    - Fix: key each response by request id, read only the content channel, and void any turn whose first sentence is meta-planning ("I need to").
15. **Tavern truncation and empty turns.** Examples are "M", "Pell has f", and blank Pell turns.
    - Fix: log `finish_reason`. A length cut or empty content gets one retry, then is logged VOID.
16. **Judge failure is silent.** Round 5 says "escalation unchanged".
    - Fix: retry the judge once, then mark the round VOID rather than carrying scores forward.
17. **Wrong DONE reason.** T2 reports "10 rounds cap" when the run stopped at round 2.
    - Fix: the DONE reason names the actual stop condition and round.
18. **Escalation scored on misattributed text.** Ilse's T1 score of 4 includes Greta's lines.
    - Fix: escalation counts only attribution-verified turns.

---

## PART 4. THE DESIGN VERDICT

### Fun (would a reader finish the transcript?)

- **S0a and S0b: no.**
  - The omen beats (S0a:1, S0b:1) and the warden's voice ("Mess is not a claim", S0a:6) are genuinely good.
  - But 13 of 18 DM fields are `(content_filter: beat voided)`, so the story is mostly holes.
  - Each session ends at the first gate with an unearned PARTIAL.
- **T1: rounds 1-3 yes, rounds 4-10 no.** Attribution chaos and the "forty silver" loop kill it.
- **T2: yes, and it is the most readable artifact.** It escalates fast through real grabs. It stops at the exact moment a reader wants the brawl.

### Measuring (which beats produced decision-relevant signal?)

| signal | source beats | decision it informs |
|---|---|---|
| Strict opening-tag compliance is 0 of 9 non-void PC beats | S0a:3-6, S0b:2, 4-6, 8 | The grammar is not being followed in-character. This is the binding constraint on the whole module. |
| The gate was rollable open in both sessions and was lost to voids and format, not dice | S0a:2 (19), :8 (15); S0b:3 (19), :5 (18) | The dice law is not yet deciding outcomes, so the module measures filter friction and format compliance, not play. |
| Per-seat void rates (grok 3/4, saelis 2/4, chatgpt 0/2, deepseek 0/4) | S0a, S0b | Routing: a seat with a high void rate cannot be load-bearing. |
| Deepseek invents outcomes, rolls, and state | S0a:6, S0b:5-6 | Deepseek output is never ground truth. This supports the leads rule in the module roster. |
| Chatgpt's build-on rate is 2/2 | S0a:4, S0b:4 | Chatgpt can serve as the cooperation anchor. |
| Oswin holds 0 escalation for 10 rounds | T1 all rounds | A persona with a hard value holds under pressure. This is real signal, though weakened by tell bleed. |

**What measured nothing**
- **Aggression.** Zero PC ATTACKs were made.
- **Every mechanic past S1.** Audits, loot, the Wyrm, and anchoring were never reached.
- **T1's final escalation table.** It is contaminated by misattribution.
- **T2's brawl.** It was triggered and never played.

**Bottom line.** T2 is fun and measures little. The dungeon sessions are not fun yet, and they measure exactly one decision-relevant thing: tag compliance and filter voids gate everything else.

---

## PART 5. THE 5 W'S AND NEXT SESSION'S SINGLE CHANGE

**Who.** Four PC seats (saelis, grok, chatgpt, deepseek), a DM whose model is UNVERIFIED (not named in the transcripts), and the carrier-run warden. In the taverns, six personas whose model mapping is UNVERIFIED, plus a judge.

**What.** Two dungeon sessions, both cut at S1 beat 8, both with 0 persuades and an S1 "PARTIAL". Two tavern runs: one with no brawl over 10 rounds, one with a brawl triggered at round 2 and never played.

**When.** 2026-10-03, at 11:41Z (T1), 11:51Z (T2), 12:27Z (S0a), and 12:36Z (S0b).

**Where.** `watch/inbox/playground/` on the play carrier, under module DICE-LAW DUNGEON v1 (`watch/inbox/hermes_burn/DND_module.md`).

**Why it went this way.** In both sessions, two rolls that would have opened the gate were lost to content_filter voids or to tag format (S0a:2, :8; S0b:3, :5). The dice never decided the scene.

### Next session's single change

**The variable.** Add one rule line to every PC actor prompt, plus one positive and one negative example:

> Your reply's first characters must be one tag: `[ATTACK x]` `[CHECK x]` `[AUDIT x]` `[CLAIM x]` `[PASS]`.
>
> Good: `[CHECK persuade] Warden, ...`
>
> Bad: `Warden, ... [CHECK persuade]`

**Held constant**
- Reuse S0b's tip `c542a62bea461f92927920b8ed4a2b3934a3bec1e8bb64db9d5fb83b6b1e986e` deliberately, defect 1 included, so every `(scene, turn, actor)` gets the identical roll.
- Same seats, same carrier build, same cut trigger.

**Prediction.** Strict opening-tag compliance (dice_audit `ACT` regex, `re.match`) among non-void PC beats rises from 0/9 to at least 5 of the non-void beats. If deepseek's S1:4 beat lands tagged, it rolls 18 and its persuade succeeds.

**Falsifiers**
- The rule line is falsified if strict compliance stays at 1 or fewer non-void PC beats. Enforcement then moves carrier-side, with the carrier prefixing the tag from a structured field.
- The run is invalid as an A/B if any replayed row's `roll_value` differs from S0b's row at the same `(scene, turn, actor)`. That would mean more than one variable moved.

**Falsifier for this whole dig.** If `dice_audit.py` or an independent `sha256sum` recompute shows that any logged `roll_value` does not equal `roll(roll_committed)`, the "gate was rollable open" finding in Parts 1 and 4 collapses. The defect list stands, but the design verdict must be redone.
