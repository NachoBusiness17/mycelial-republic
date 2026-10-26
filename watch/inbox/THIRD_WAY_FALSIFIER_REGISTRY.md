# THIRD WAY FALSIFIER REGISTRY - F1-F12 consolidated - 2026-09-26

Created by watch/inbox/BURN_third-way-game_20260926_f.md. One table, every falsifier, deduped. States: pending-playtest (needs Sep-29 measurement), armed (static gate, checkable against artifacts now, no playtest needed), fired-pass / fired-fail / discharged (none yet: no playtest has run).

## The table

| ID | Origin receipt | Claim tested (exact) | Measurement | Threshold | State |
|---|---|---|---|---|---|
| F1 | MIDDLE_PATH_SALON_20260925.md, byte-quoted in BURN_third-way-game_20260925.md | "in two seed-matched 20-minute runs, if Pilgrim net VM falls outside plus-or-minus 15% of war net VM, the Pilgrim economy is re-priced before any expansion" | Pilgrim net VM vs war net VM, two seed-matched runs | within 15% | pending-playtest (Sep-29 gate) |
| F2 | MIDDLE_PATH_SALON_20260925.md (named in STORYTELLER_SIX corpus binding "falsifiers F1-F4"; exact salon wording not byte-read this pass); observable form in BURN_20260925 gates table: "Vow log lines in Output: every Vow" | vow uptake is observable and every Vow is logged | VOW-TAKEN lines, schema-locked by THIRD_WAY_VOW_LOG_SCHEMA.json; any schema-invalid line or vow on crits/longer_superhot voids that run's ledger row (BURN_20260926 conformance gate) | every Vow logged; uptake observed, not gated | pending-playtest (Sep-29 gate) |
| F3 | MIDDLE_PATH_SALON_20260925.md F3: "the grace distribution must match the seeded RNG distribution exactly" | luck is the unpeeked seed, never the rigged die | two same-seed runs compared roll for roll; totals >= 7 rate | identical sequences; totals >= 7 at 15/36 (~41.7%), no smoothing | pending-playtest (Sep-29 gate; instrumented by F9) |
| F4 | MIDDLE_PATH_SALON_20260925.md (named "falsifiers F1-F4"; exact wording not byte-read this pass) | migration (per salon; instrument un-byte-read) | per salon | per salon | pending-playtest (Sep-29 gate; byte-read of the salon owed before Sep-29) |
| F5 | STORYTELLER_SIX_RACTOR_20260925.md, Administrator chair | "counter-media must measurably shift faction sentiment meters in playtest, or Act I is set dressing and gets rebuilt" | counter-media sentiment delta | > 0 | pending-playtest |
| F6/F8 (MERGED) | F6: STORYTELLER_SIX_RACTOR_20260925.md, Engineer chair. F8: BURN_third-way-game_20260926.md | F6, the law: "Optimizable faith is failed faith" (no meta optimizes Vow plus Seed into a dominant strategy). F8, its arithmetic instrument: "if a vowed build's net VM beats the best unvowed build's net VM by more than 15 percent, the stub constants (vow_multiplier 1.5, price 2x vm_cost) are re-priced before expansion" | two seed-matched runs, vowed build vs best unvowed build, net VM; census sub-gate: 12 boons, 10 vow-eligible, 1 seed-unlocked | within 15%; census exact or the stub voids | pending-playtest (census half armed now) |
| F7 | STORYTELLER_SIX_RACTOR_20260925.md, Walker chair | "the endgame must abolish the VM pool for all players; a pool that persists post-endgame is Omelas and the design fails review, however beautiful the walking away looked" | endgame ledger (beats 15-20) | pool abolished for dark, light, and pilgrim alike | pending-playtest |
| F9 | BURN_third-way-game_20260926_b.md | "every GRACE line must validate against THIRD_WAY_GRACE_SCHEMA.json. Any schema-invalid line, any field-set divergence between the peeked and unpeeked legs, or any divergence between the two same-seed roll sequences voids the Unpeeked Seed claim and the shrine ships as peeked until fixed" | GRACE log lines vs schema; totals >= 7 across shared fields | schema-valid only; no raw seed in any line (voids the pair outright) | pending-playtest (logs exist only at playtest) |
| F10 | BURN_third-way-game_20260926_c.md | "FAILED DATE fires only on the conjunction (war-rank max plus forced-wall attempt), never on rank alone; boon drafts stay blocked between trigger and clearance; any Door riddle attempt, wrong answers included, clears it" | implementation check of trigger and clearance; census: chain count 3, riddle 3 empty at stub ship | no draft slips through; no correctness-keyed clearance; census exact | armed |
| F11 | BURN_third-way-game_20260926_d.md | "any telling that contradicts the stub facts (a Wall that fights, a Door opening on anything but 2d6 pass on 7, FAILED DATE keyed on riddle correctness, altered riddle answers) voids the telling file" | SIX_CHAIR_TELLINGS.json vs stub shared_facts; register: exactly one CAPS aside, Turtle's beats only | contradiction rebuilds the telling file; register check exact | armed |
| F12 | BURN_third-way-game_20260926_e.md | "any implementation or telling contradicting the stub (a Vow declared after seeing the cards, kept-vow arithmetic off 1.5x at 2x vm_cost, a free broken vow, a scouting vow round, a peeked grace roll, a killer paid one side only, an unlock missing either conjunction) voids the stub and re-opens Act III" | fact check vs THIRD_WAY_ACT3_STUB.json | any contradiction voids; curve and log gates stay with F3/F8/F9 | armed |

## Dedup rulings

- **F6/F8 merge:** F6 is the design law (faith must not be optimizable, the Inefficiency Law); F8 is that law's measurable arithmetic. One claim, one instrument, one row. Cite F6 for the thesis, F8 for the numbers.
- **F3/F9 kept separate (named, not merged):** F3 is the claim (distribution match), F9 is the schema-locked audit that extends the 20260925 seed falsifier with independent void conditions F3 does not carry (schema-invalid lines, field-set divergence, raw seed in a log). Claim and instrument, both needed at Sep-29.

## Playtest-day gates (what must be measured Sep-29)

1. **F1 score gate:** Pilgrim net VM vs war net VM within 15% across two seed-matched 20-minute runs.
2. **F2 vow uptake:** every Vow prints a schema-valid VOW-TAKEN line; uptake itself is the observation.
3. **F3 seed audit:** two same-seed runs match roll for roll; totals >= 7 at 15/36 with no smoothing; F9 schema gate on every GRACE line.
4. **F4 migration:** measured per the salon's F4; exact instrument byte-read owed before the day.

Same-day extras: F5 counter-media delta > 0; F6/F8 vowed-vs-unvowed 15% comparison; F7 endgame ledger shows the pool abolished.

## Health count

12 ids, 11 entries after the F6/F8 merge. **Pending-playtest: 8** (F1, F2, F3, F4, F5, F6/F8, F7, F9). **Armed static gates: 3** (F10, F11, F12). **Fired-pass: 0. Fired-fail: 0. Discharged: 0.** No playtest has run; nothing is discharged.

## Owed before Sep-29

F2 and F4 live byte-level in MIDDLE_PATH_SALON_20260925.md, which was outside this pass's read scope; this registry carries them by name and observable instrument only. A byte-read of the salon's F2/F4 wording is owed before playtest day so the registry's threshold cells stop saying "per salon".
