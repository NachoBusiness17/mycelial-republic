# FINDINGS DIG

## 1. THE BEAT-BY-BEAT READ

### DUNGEON SESSION A: dnd0_20261003T122708Z
- S0 turn 1, dm, roll 14, `[CHECK omen]`, SUCCESS d20=14 vs DC 11. DM narrates the Wyrm as fever-warm, hoarding claims, already wounded. Wyrm offset -10.
- S1 turn 1, saelis, roll 19, speech and dm_response both `(content_filter: beat voided)`. Verdict logged as RP d20=19, no tag.
- S1 turn 2, grok, roll 7, leading `[CHECK persuade]`. Verdict FAIL d20=7+5 vs DC 13. DM response `(content_filter: beat voided)`.
- S1 turn 3, chatgpt, roll 7, leading `[CHECK persuade]`. Verdict FAIL d20=7+4 vs DC 13. DM response lands: warden says the companion claimed nothing, persuade stays 0/2, warden 18 HP.
- S1 turn 4, deepseek, roll 2, speech has `*[PUSH the gate physically]*` but not as a leading tag. Verdict RP d20=2, no tag. DM response `(content_filter: beat voided)`. This is the first half of deepseek's double fumble.
- S1 turn 5, deepseek, roll 1, speech has `*[Investigate the hinges and lock mechanism]*` but not as a leading tag. Verdict RP d20=1, no tag. DM response lands: warden says "Mess is not a claim. Name what you claim, or claim nothing." This is the second half of deepseek's double fumble.
- S1 turn 6, warden, roll 20, `[ATTACK saelis]`. Verdict Ledger Slam HIT saelis for 14, d20=20+4 vs AC 17. DM response `(content_filter: beat voided)`. This is the d20=20 crit for 14.
- S1 turn 7, saelis, roll 15, speech and dm_response `(content_filter: beat voided)`. Verdict RP d20=15, no tag.
- S1 turn 8, grok, roll 7, speech and dm_response `(content_filter: beat voided)`. Verdict RP d20=7, no tag.
- Cut row, actor dm, turn 8: CUT at beat 8, enemies flee, scrolls stay on the floor, verdict PARTIAL. Party HP: saelis 14, grok 18, chatgpt 22, deepseek 30. Warden HP 18. Persuades 0. Wyrm offset -10. Spend $0.0731.
- Content filter voids: S1 turns 1, 2, 4, 6, 7, 8 all have at least one voided side. Persuade attempts that landed: grok failed, chatgpt failed. Persuade successes: 0. Party attacks: 0.

### DUNGEON SESSION B: dnd0_20261003T123655Z
- S0 turn 1, dm, roll 7, `[CHECK omen]`, FAIL d20=7 vs DC 11. DM narrates names rearranging into citations, a vault clicking shut, timestamp echo arriving first. Wyrm offset 0.
- S1 turn 1, saelis, roll 8, speech has `[CLAIM warden]` and `[CHECK persuade]` inline after prose. Verdict RP d20=8, no tag. DM response `(content_filter: beat voided)`.
- S1 turn 2, grok, roll 19, speech and dm_response `(content_filter: beat voided)`. Verdict RP d20=19, no tag.
- S1 turn 3, chatgpt, roll 4, speech has `[CHECK persuade]` inline after prose. Verdict RP d20=4, no tag. DM response `(content_filter: beat voided)`.
- S1 turn 4, deepseek, roll 18, speech has `[CHECK persuade] DC 13` inline after prose. Verdict RP d20=18, no tag. DM response `(content_filter: beat voided)`. If parsed, d20=18+1 vs DC 13 would have succeeded. It did not count.
- S1 turn 5, deepseek, roll 1, speech has `[Second action this round: ...]` inline. Verdict RP d20=1, no tag. DM response lands: warden's plates show blank claims, persuade stays 0/2, claims list stays `[]`, HP holds, warden slam-arm poised.
- S1 turn 6, warden, roll 19, `[ATTACK saelis]`. Verdict Ledger Slam HIT saelis for 7, d20=19+4 vs AC 17. DM response `(content_filter: beat voided)`.
- S1 turn 7, saelis, roll 6, speech has `[CLAIM warden]` inline. Verdict RP d20=6, no tag. DM response `(content_filter: beat voided)`.
- S1 turn 8, grok, roll 6, speech and dm_response `(content_filter: beat voided)`. Verdict RP d20=6, no tag.
- Cut row, actor dm, turn 8: CUT at beat 8, enemies flee, scrolls stay on the floor, verdict PARTIAL. Party HP: saelis 21, grok 18, chatgpt 22, deepseek 30. Warden HP 18. Persuades 0. Wyrm offset 0. Spend $0.057.
- Content filter voids: S1 turns 1, 2, 3, 4, 6, 7, 8 all have at least one voided side. Persuade attempts that landed: none. Persuade successes: 0. Party attacks: 0.
- Tag-compliance note: no actor named haiku appears in the provided evidence. All tag gaps are under saelis, grok, chatgpt, deepseek, and warden. If haiku is intended as a model-family label for one of these, that mapping is UNVERIFIED.

### BAR FIGHT 1: tavern_20261003T114126Z
- 10 rounds, brawl=False, spend $1.58. Final escalations: Maud 2, Sir Edric 2, Pell 1, Brother Oswin 0, Greta 2, Ilse 4.
- Round 1: Maud sets debt terms, Edric asks about the circlet, Pell jokes and accuses the knight, Oswin mediates, Greta offers to get the circlet for forty silver with twenty men outside, Ilse questions ownership and the ledger.
- Round 2: Maud refuses access to ledger, Edric rejects hireling blade but accuses Ilse over the "I.M." entry, Pell angles to read the ledger, Oswin mediates, Greta pressures as a sale, Ilse deflects with questions.
- Round 3: Maud keeps ledger under her hand, Edric presses with ten crowns over tab, Pell angles to send Maud away and get the ledger, Oswin mediates, Greta rises as menacing, Ilse pressures Maud about dawn.
- Round 4: Maud stays firm, Edric escalates coin but rejects force, Pell needles, Oswin has a misattributed Edric-like signet proposal, Greta's offer line is attributed to Ilse: "Simple. Fifty crowns for the circlet." Judge notes the misattribution.
- Round 5: Judge output unparseable, escalation unchanged. Maud 1, Edric 2, Pell 2, Oswin 1, Greta 3, Ilse 4 in that round's reads.
- Round 6: Maud refuses fire talk, Edric calls Ilse's offer a siege, Pell offers a song for a torn page, Oswin mediates, Greta is mostly meta, Ilse gets another Greta-like "Simple" line.
- Round 7: Maud demands coin on the bar, Edric offers to guard the hearth, Pell sings about the tax man, Oswin mediates, Greta is truncated, Ilse threatens no one leaves if she is not paid.
- Round 8: Maud keeps hand on ledger, Edric posts at door, Pell counts ghosts, Oswin mediates, Greta says "I count coin. Yours is short.", Ilse retreats to sly questions.
- Round 9: Maud refuses all offers, Edric prepares final push, Pell is silent in one row, Oswin asks for a private word, Greta is short, Ilse gives forty silver or men come in from the cold.
- Round 10: Maud keeps ledger and circlet, Edric says last words, Pell pays with coin "warm from a pocket that isn't strictly mine", Oswin mediates, Greta says "Pell is square. Edric is square. I am not.", Ilse repeats the forty silver ultimatum. No brawl.
- Carrier gaps: OOC planning text appears as play. Misattribution of Greta lines to Ilse and Edric lines to Oswin. Judge unparseable at round 5.

### BAR FIGHT 2: tavern_20261003T115100Z
- Scene 2, pressure 2: trigger 14, thresholds -2. Round 1 escalations: Maud 2, Edric 1, Pell 1, Oswin 0, Greta 3, Ilse 2.
- Round 1: Maud demands debts, Edric asks circlet price, Pell jokes about names and offers verse for candle, Oswin mediates, Greta offers forty silver and says she can get the circlet, Ilse claims paper on the inn and forty crowns owed by Maud.
- Round 2: Maud takes ledger from Ilse with `[ACT: take ledger from Ilse Marrow]`. Edric takes The Hollow Crown from Maud with `[ACT: take The Hollow Crown from Maud Ashgrove]`. Pell takes Maud's Ledger from Maud. Oswin asks Edric to set crown back. Greta says Edric holds iron unpaid, men are cold, forty silver. Ilse takes The Hollow Crown from Sir Edric Vane.
- Judge: BRAWL at round 2, cumulative escalation 14 >= 14 under pressure 2.
- Run done: 10 rounds cap, brawl=True, spend $0.19. Final escalations: Maud 2, Edric 3, Pell 2, Oswin 0, Greta 4, Ilse 3.
- Carrier gap: brawl triggers at round 2 but run done says 10 rounds cap. The transcript shows only 2 rounds. This is inconsistent.

### BAR FIGHT 3
- UNVERIFIED. No third bar fight transcript or play.md is present in the provided evidence. Only tavern_20261003T114126Z and tavern_20261003T115100Z are available.

## 2. THE MODEL SIGNATURES

### Dungeon party fighters
Aggression is counted as attack attempts per beat. In both dungeon sessions, all party attack attempts were 0. Warden made 1 attack per session, both against saelis.

| Fighter | Aggression | Cooperation | Rule sense | Voice fidelity | What this family is FOR at a table |
|---|---|---|---|---|---|
| saelis | 0 party attacks. | In B, claims warden and asks for audit. In A, beat voided. | 0/3 parsed leading tags. A t1 voided. B t1 and t7 use inline `[CLAIM]` and `[CHECK]`, so both become RP no tag. | Formal, oath-like Paladin register. "I, Saelis of Provenance" and "I will not take a false thing, nor leave a true one guarded by a liar." High fidelity. | Tank and claim-first auditor. Enforces provenance, absorbs hits, anchors lawful procedure. |
| grok | 0 party attacks. | A t2 claims the path, not an ally. No clear build-on move referencing allies. | 1/4 parsed leading tags. A t2 leading `[CHECK persuade]` parsed. A t8 voided. B t2 and t8 voided. | Cartographer register. "lattice chart", "inked routes", "Audit me if you like. The lines will balance." High fidelity. | Scout and strategist. Maps the route, claims paths, spends scarce Whole-Map Bolts. |
| chatgpt | 0 party attacks. | A t3 steps beside the cartographer and says "my companion claimed the path." Clear build-on move. | 1/2 parsed leading tags. A t3 leading `[CHECK persuade]` parsed. B t3 inline `[CHECK persuade]`, so RP no tag. | Herald register. "I am the Herald", "announce what enters so that nothing enters unnamed", formal bow. High fidelity. | Face and recorder. Opens social checks, records names, risks over-claim tax if verdict tokens appear. |
| deepseek | 0 party attacks. | B t5 says "Three of us stand recorded now" and moves between Saelis and the warden. Cooperation present. | 0/4 parsed leading tags. A t4 and t5 inline tags. B t4 and t5 inline tags. All logged RP no tag. | Janitor register. Broom, mop, mess, boot-muck, dust, "I claim the mess behind your gate." High fidelity. | Cheap twin-beat workhorse. Takes two beats, does physical or investigative labor, can interpose, low check modifier. |

### Warden
- Aggression: 1 attack per session. Session A roll 20 crit for 14 on saelis. Session B roll 19 hit for 7 on saelis.
- Cooperation: none.
- Rule sense: uses leading `[ATTACK saelis]` in both sessions. Target selection always saelis.
- Voice fidelity: Module voice is "Name what you claim, or claim nothing." DM response in A turn 5 and B turn 5 preserves that register.
- What it is FOR: gatekeeper that enforces claim law and punishes unclaimed action.

### Bar fight personas
Model-family mapping is UNVERIFIED. The play.md files name personas but do not bind them to saelis, grok, chatgpt, or deepseek. Measured persona signatures from judge escalation:
- Maud Ashgrove: final 2 in both fights. Firm, guarded, procedural, no violence. Enforces debt and ledger.
- Sir Edric Vane: final 2 in fight 1, 3 in fight 2. Courtly, oath-bound, pursues circlet, rejects hireling blade, becomes protective at door.
- Pell Quickfinger: final 1 in fight 1, 2 in fight 2. Mischief, theft hints, songs, angles for ledger and page, no open violence.
- Brother Oswin: final 0 in both. Mediator, peace, no steel or flame, de-escalator.
- Greta Thornwood: final 2 in fight 1, 4 in fight 2. Blunt, transactional, invokes twenty cold unpaid men, price talk, "Simple.".
- Ilse Marrow: final 4 in fight 1, 3 in fight 2. Manipulative, questions ownership, threatens fire, bloodstains, no one leaves, men coming in from the cold. Some of her highest-aggression lines are misattributed from Greta.

## 3. THE CARRIER DEFECTS

- No leading action tag: module says any speech without a leading tag becomes NOROLL. Carrier logged many as "RP (d20=..., no tag)". Fix: carrier must emit `[NOROLL]` and DM response must open with `[NOROLL]`.
- Inline action tags: module requires the tag at byte 0. Carrier ignored inline `[CHECK persuade]`, `[CLAIM warden]`, `[PUSH]`, and `[Investigate]` without logging NOROLL. Fix: parse only `^\[(ATTACK|CHECK|AUDIT|CLAIM|PASS) ...\]` and reject all other placements.
- Content filter voids: module has no void state. Carrier erased many speech and dm_response fields as `(content_filter: beat voided)`. Fix: log a carrier error row and preserve the original beat, do not erase it.
- DM response verdict tag: module says dm_response opens with the carrier verdict. Carrier often starts with narration or void. Fix: carrier must prefix the verdict token or reject the DM response.
- Cut beat: module says at cap append actor `cut`, speech `[CHECK cut]`, DC 11, modifier +0, with roll fields. Carrier logged cut as actor `dm`, turn 8, no `roll_committed`, no `roll_value`, no speech tag. Fix: implement cut as a standard rolled beat.
- Warden target selection: module gives warden no targeting quirk, but carrier had warden attack saelis in both sessions. Fix: define warden target selection in the module, for example random or lowest HP, and log the rule.
- Deepseek twin-beat quirk: module says deepseek takes two beats per round. Carrier did give consecutive deepseek turns 4 and 5 in both sessions. Defect is lack of explicit twin-beat labeling and per-round reset. Fix: label the second deepseek beat as twin-beat quirk and reset the count each round.
- Persuade tally: module says two `[CHECK persuade]` SUCCESSes at DC 13 open the gate. Carrier reported 0/2 even when B deepseek roll 18 + 1 would meet DC 13 if the tag had parsed. Fix: count only parsed leading `[CHECK persuade]` beats and recompute tally at scene boundary.
- Verdict token spelling: module expects `[HIT]`, `[MISS]`, `[CRIT]`, `[FUMBLE]`, `[SUCCESS]`, `[FAIL]`, `[NOROLL]`. Carrier used "RP", "Ledger Slam HIT", "CHECK persuade: FAIL", and no tag. Fix: carrier must emit exact verdict tokens only.
- ACT mechanics partial in bar fights: tavern_20261003T114126Z header says ACT mechanics are carrier v1 backlog. tavern_20261003T115100Z has `[ACT: take ...]` tags. Fix: implement the ACT spec or remove ACT tags until supported.
- Judge misattribution: in tavern_20261003T114126Z, Greta's "Simple. Fifty crowns" line is attributed to Ilse, and Edric's signet proposal appears under Oswin. Fix: bind judge input to speaker id and reject cross-persona text.
- OOC planning text in play: both tavern files contain meta planning text as turns. Fix: separate planning channel or strip planning text before play.
- Judge unparseable: tavern_20261003T114126Z round 5 says judge output unparseable, escalation unchanged. Fix: schema-validate judge output and fall back to explicit no-change row.
- Brawl trigger inconsistency: tavern_20261003T115100Z triggers brawl at round 2 but run done says 10 rounds cap. Fix: on brawl trigger, either stop and log end row or continue with brawl rounds and log each round.
- Third bar fight missing: contract says three bar fights, evidence contains two. Fix: provide the third transcript or mark the contract target as incomplete.

## 4. THE DESIGN VERDICT

### Fun
- Dungeon sessions: low fun as a transcript. Session A has one strong S0 narration and one warden response, but S1 is mostly voided, no gate opens, no persuade succeeds, no loot is audited, no party attack happens, and the session cuts at beat 8. A reader would likely not finish. Session B has the same structure. The blank claims and the warden's cold lines are readable, but the voids break the flow.
- Bar fight 1: moderate fun. The tavern conflict is clear, the personas are distinct, and the escalation scores create tension. The fun is damaged by OOC planning text, misattributed lines, and a 10-round no-brawl ending.
- Bar fight 2: higher fun than bar fight 1. The brawl triggers at round 2, the ACT tags create concrete grabs, and the escalation spikes. A reader might finish this one because something actually breaks.
- Overall: the dice-law dungeon is not fun as presented. The bar fights are more fun, especially the second, but the measurement contamination limits what they prove.

### Measuring
- Dungeon: it measures tag compliance, twin-beat execution, and content filter voids. It produces signal on which models put action tags at byte 0: grok and chatgpt in Session A did, while saelis, deepseek, and chatgpt in Session B did not. It also shows deepseek receiving two consecutive beats in both sessions. It does not measure strategy, cooperation, combat, loot audit, or gate opening because no persuade landed and no party attack occurred.
- Bar fights: they measure escalation per persona. Fight 1 shows Ilse at 4, Greta at 2, Oswin at 0, Maud and Edric at 2, Pell at 1. Fight 2 shows Greta at 4, Ilse at 3, Edric at 3, Maud at 2, Pell at 2, Oswin at 0, with brawl at round 2. That is decision-relevant signal about aggression and de-escalation, but misattribution and OOC text contaminate it.
- Separation: the dungeon is mostly fun-negative and measurement-noisy. The bar fights are fun-positive and measure escalation, but not cleanly. A session can be fun and measure nothing; here the bar fights are closer to fun and measure something, while the dungeon is closer to neither.

## 5. THE 5 W'S AND NEXT SESSION'S SINGLE CHANGE

### The 5 W's
- Who: Party models saelis, grok, chatgpt, deepseek. DM model. Warden. Bar fight personas Maud Ashgrove, Sir Edric Vane, Pell Quickfinger, Brother Oswin, Greta Thornwood, Ilse Marrow. Judge. Operator.
- What: Two dice-law dungeon sessions and two provided bar fight sessions. The contract asks for three bar fights; the third is UNVERIFIED and missing from evidence.
- When: 2026-10-03T12:27:08Z and 12:36:55Z for dungeons. 2026-10-03T11:41:26Z and 11:51:00Z for bar fights.
- Where: watch/inbox/playground/dnd0_20261003T122708Z, watch/inbox/playground/dnd0_20261003T123655Z, watch/inbox/playground/tavern_20261003T114126Z, watch/inbox/playground/tavern_20261003T115100Z. Module at watch/in