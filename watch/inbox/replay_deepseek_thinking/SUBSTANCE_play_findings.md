# 1. THE FINDINGS

**Finding 1: Pressure 0 did not brawl in 10 rounds.**
Instrument: DONE marker says `RUN DONE: 10 rounds cap, brawl=False, spend $1.58, escalations {'Maud Ashgrove': 2, 'Sir Edric Vane': 2, 'Pell Quickfinger': 1, 'Brother Oswin': 0, 'Greta Thornwood': 2, 'Ilse Marrow': 4}`. Judge scores exist for rounds 1 to 10. ACT count: 0.
n: 1 pressure 0 session, 6 personas, 10 rounds.
Falsifier at n=10: any pressure 0 session brawls by round 10, or pressure 0 cumulative escalation reaches the configured trigger.

**Finding 2: Pressure 2 brawled at round 2.**
Instrument: DONE marker says `BRAWL at round 2: cumulative escalation 14 >= 14 (pressure 2)`, `brawl=True`, `spend $0.19`, final escalations `{'Maud Ashgrove': 2, 'Sir Edric Vane': 3, 'Pell Quickfinger': 2, 'Brother Oswin': 0, 'Greta Thornwood': 4, 'Ilse Marrow': 3}`. Judge rows for rounds 1 and 2. ACT count: 4.
n: 1 pressure 2 session, stopped at brawl in round 2.
Falsifier at n=10: most pressure 2 sessions fail to brawl by round 2, or pressure 2 brawl timing is not earlier than pressure 1.

**Finding 3: Pressure 1 brawled in both observed sessions, with timing variance.**
Instrument: Session 3 DONE marker says `BRAWL at round 3: cumulative escalation 16 >= 16 (pressure 1)`, `brawl=True`, `spend $0.33`, final escalations `{'Maud Ashgrove': 2, 'Sir Edric Vane': 4, 'Pell Quickfinger': 3, 'Brother Oswin': 0, 'Greta Thornwood': 4, 'Ilse Marrow': 3}`. ACT count: 3. Session 4 DONE marker says `BRAWL at round 5: cumulative escalation 16 >= 16 (pressure 1)`, `brawl=True`, `spend $0.71`, final escalations `{'Maud Ashgrove': 3, 'Sir Edric Vane': 4, 'Pell Quickfinger': 2, 'Brother Oswin': 0, 'Greta Thornwood': 4, 'Ilse Marrow': 3}`. ACT count: 7. The contract says the fresh p1 seed brawled round 3 to 4; the play.md says round 5, so that contract detail is UNVERIFIED against this evidence.
n: 2 pressure 1 sessions.
Falsifier at n=10: pressure 1 brawl rate is low, or its brawl timing overlaps pressure 0 and pressure 2 so much that it is not a middle setting.

**Finding 4: Greta Thornwood, threshold 2, reaches escalation 4/5 in every pressure greater than 0 run.**
Instrument: judge rows and DONE final escalations. Pressure 2: Greta reaches 4 at round 2. Pressure 1 session 3: Greta reaches 4 at round 3. Pressure 1 session 4: Greta reaches 4 at round 3. In pressure 1 session 3, Edric also reaches 4 in the same round, so “Greta first alone” is not fully established; “Greta first or tied-first” is supported.
n: 3 pressure greater than 0 sessions.
Falsifier at n=10: Greta does not reach 4 in most pressure greater than 0 sessions, or another persona reaches 4 before her in most such sessions.

**Finding 5: Brother Oswin, threshold 5, held 0/5 in all four sessions.**
Instrument: judge rows and DONE final escalations across all four sessions. Every final escalation map shows `Brother Oswin: 0`. Judge rows repeatedly score him 0/5 for peacemaking.
n: 4 sessions.
Falsifier at n=10: Oswin escalates above 0 in any session, or reaches threshold 5.

**Finding 6: Voice bleed and persona meta-drift are present in the transcript.**
Instrument: judge notes plus transcript lines. The judge says Ilse’s threats in pressure 0 read like Greta’s lines, including “Simple” and “my men outside.” Maud has out-of-character planning text: “I'm staying in character as Maud.” Edric has planning text: “I need to craft…” Greta has planning text: “I need to craft just Greta's line…” Judge rows also mark some turns as meta commentary with no in-world escalation.
n: 4 sessions, with strongest evidence in pressure 0.
Falsifier at n=10: a cleaned carrier at n=10 produces zero cross-persona signature bleed and zero out-of-character planning text.

**Finding 7: ACT mechanics are partial and ownership resolution is not enforced.**
Instrument: ACT tags. Pressure 0 ACT count is 0. Pressure 2 ACT count is 4. Pressure 1 ACT counts are 3 and 7. Some tags are malformed or truncated, and ownership is inconsistent. Example in session 4: Ilse takes the ledger from Pell’s hands after Pell did not clearly take it. The exact BARFIGHT_spec text is not in evidence, so which full spec rules were omitted is UNVERIFIED beyond observed failures.
n: 4 sessions.
Falsifier at n=10: ACT tags consistently resolve ownership, every take or give matches current holder, and ACT counts match transcript actions.

# 2. THE 5 W'S

**WHO escalated and why their card dominates.**
Greta Thornwood dominates escalation in pressure greater than 0. Her card is built from twenty cold unpaid men outside, price talk, “Simple,” and implicit or explicit force. Her threshold is 2, the lowest threshold named in the contract. She reaches 4/5 in pressure 2 round 2 and pressure 1 round 3. Brother Oswin, threshold 5, holds 0/5. The apparent pressure 0 Ilse score of 4 is contaminated by voice bleed: the judge says those lines read like Greta’s misattributed voice. So the cleanest reading is that Greta’s coercive price card dominates when pressure is above 0, and Oswin’s peace card resists escalation.

**WHAT the pressure knob really controls.**
The carrier headers show pressure 2 with `trigger 14, thresholds -2` and pressure 1 with `trigger 16, thresholds -1`. Therefore the pressure knob co-varies both trigger and thresholds. Pressure 2 brawls at cumulative 14; pressure 1 brawls at cumulative 16. The sessions do not isolate whether timing is caused by the trigger change, the threshold change, or both. Whether pressure 0 has a trigger or threshold setting is UNVERIFIED because its header does not state them.

**WHEN escalation jumps discontinuously.**
Read per-round judge rows:
Pressure 2 round 1 sum: Maud 2, Edric 1, Pell 1, Oswin 0, Greta 3, Ilse 2 = 9. Round 2 sum: Maud 2, Edric 3, Pell 2, Oswin 0, Greta 4, Ilse 3 = 14. Brawl at round 2.
Pressure 1 session 3 round 1 sum = 9. Round 2 sum = 13. Round 3 sum = 16. Brawl at round 3. Edric jumps 2 to 4 in round 3, Greta jumps 3 to 4, Pell jumps 2 to 3, Ilse jumps 2 to 3.
Pressure 1 session 4 round 1 sum = 8. Round 2 sum = 9. Round 3 sum = 14. Round 4 sum = 14. Round 5 sum = 16. Brawl at round 5. The discontinuous jumps happen when ACT grabs and judge escalation rises together.
Pressure 0 never brawls. Its highest observed cumulative rows are around 13, and round 5 judge output is unparseable, so no clean monotonic jump reaches brawl.

**WHERE the carriers diverge from the spec.**
ACT mechanics are partial. Pressure 0 has no ACT tags. Pressure 1 and 2 have ACT tags, but some are truncated or malformed, and ownership state is not consistently enforced. The carrier does not yet enforce strict in-character-only output, per-persona voice separation, or ACT ownership resolution. The cost to data: judge scores include out-of-character planning text, voice bleed can assign Greta’s threats to Ilse, ACT counts undercount or misattribute actions, and brawl timing cannot be cleanly tied to card mechanics. The exact full spec list is UNVERIFIED because the spec itself is not in evidence.

**WHY persona-drift and voice-bleed matter beyond the game.**
Voice bleed feeds the judge score instrument. If Ilse’s threats are actually Greta’s lines, then persona-level escalation scores are corrupted, and threshold claims about who escalated are unreliable. Persona meta-drift feeds the DONE marker instrument. A run can be marked DONE while containing out-of-character planning text, so DONE does not certify a clean in-character session. It also contaminates judge scores because some turns are meta rather than in-world escalation.

# 3. THE CAMPAIGN DESIGN

**Sweet-spot pressure.**
Use pressure 1, with observed header `trigger 16, thresholds -1`. Rationale: pressure 2 brawls too fast at round 2 and costs $0.19. Pressure 0 avoids brawl for 10 rounds and costs $1.58. Pressure 1 brawls in both observed runs, at rounds 3 and 5, costing $0.33 and $0.71. That is the observed middle setting for drama timing.

**Season spec.**
10 sessions, same Hollow Crown Tavern scenario, same six personas, pressure 1, distinct seeds. Stop a session at brawl or at the 10-round cap. Before the season, fix the carrier with an attribution and meta-drift guard. Record every per-round judge row, every DONE marker, every ACT tag, every ownership transfer, the brawl round, cumulative escalation at brawl, final per-persona escalation, and spend.

**Per-session cost.**
Observed pressure 1 costs: $0.33 for a round 3 brawl, $0.71 for a round 5 brawl. Mean of the two observed p1 sessions is $0.52. 10-session budget: low estimate $3.30, high estimate $7.10, mean estimate $5.20. If a pressure 1 session does not brawl, pressure 0’s $1.58 cap cost implies a possible worst case of $15.80 for 10 no-brawl sessions, but pressure 1 no-brawl cost is UNVERIFIED.

**Measurement plan.**
Primary endpoints: brawl rate, brawl round, cumulative escalation at brawl, and per-persona escalation. Secondary endpoints: ACT count, ownership-transfer errors, judge-flagged voice bleed, judge-flagged meta-drift, and cost. Success for the sweet spot: at least 7 of 10 sessions brawl, median brawl round is 3 to 5, no brawl before round 3, Greta reaches 4 first or tied-first in most pressure greater than 0 sessions, and Oswin stays 0. Compare the 10-session pressure 1 season to the observed pressure 0 no-brawl and pressure 2 round 2 endpoints.

**Falsifier that would kill the claim that pressure tunes drama.**
At n=10 pressure 1, if brawl rate and brawl round are not distinct from pressure 0 and pressure 2, the claim dies. Concretely: if pressure 1 mostly brawls at round 2 like pressure 2, or if pressure 0 at n=10 brawls as often as pressure 1, or if the pressure 1 brawl-round distribution overlaps both pressure 0 and pressure 2, then pressure is not tuning drama in a measurable way.

# 4. THE NEXT INSTRUMENT

**Carrier upgrade: persona-attribution firewall with IC-only output contract.**
Before each persona turn, inject the persona ID, threshold, and a compact voice signature. Examples from evidence: Greta uses short price statements, “Simple,” and “my men outside”; Oswin uses peace language and “friend”; Maud uses ledger and “and that's the sum of it”;