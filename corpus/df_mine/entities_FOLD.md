# entities_FOLD — how DF encodes temptation vs values

Source hall (only file in the stratum): `data/vanilla/vanilla_entities/objects/entity_default.txt` — 6 entities (MOUNTAIN, FOREST, PLAINS, EVIL, SKULKING, SUBTERRANEAN_ANIMAL_PEOPLES), 132 ETHIC lines, 22 ethic acts, 17 response categories, 30 fixed POSITION blocks. `PUNISHMENT_EXCLUSIVE`/`EXECUTION_STYLE` do not exist in this install; punishment is purely ETHIC responses plus executor positions.

## The mechanical chain

1. `[ETHIC:<act>:<response>]` — society-level law. 22 acts (THEFT, TREASON, OATH_BREAKING, ASSAULT...), responses on a gravity ladder: NOT_APPLICABLE < PERSONAL_MATTER < ACCEPTABLE/JUSTIFIED_* < SHUN/APPALLING/MISGUIDED/UNTHINKABLE < PUNISH_REPRIMAND < PUNISH_EXILE < PUNISH_SERIOUS < PUNISH_CAPITAL. Only PUNISH_* values are crimes; the rest are mere opinion.
2. `[VALUE:<axis>:<N>]` — personal weight, -50..+50. Dwarves are fixed (LAW:30, CRAFTSMANSHIP:50); goblins inverted (POWER:50, TRUTH:-50, LAW:-50); elves niche (NATURE:50, SELF_CONTROL:-15); kobolds near-zero except CUNNING:50. Humans roll `[VARIABLE_VALUE:ALL:-30:30]` per civilization — no native conscience.
3. A figure falls when the act's ETHIC response is tolerable (PERSONAL_MATTER/ACCEPTABLE/NOT_APPLICABLE — goblin THEFT:PERSONAL_MATTER, kobold THEFT:NOT_APPLICABLE) and a strong positive value pulls the other way (CUNNING, POWER). `[BANDITRY:n]` (PLAINS:10, EVIL:50) seeds how many plotters exist.
4. If caught: `[RESPONSIBILITY:LAW_ENFORCEMENT]` (SHERIFF, replaced by CAPTAIN_OF_THE_GUARD at pop 50) beats, then HAMMERER (`RESPONSIBILITY:EXECUTIONS` + `EXECUTION_SKILL:HAMMER`) kills — but every noble carries `[PUNISHMENT_EXEMPTION]` + `[ACCOUNT_EXEMPT]`. The lawgivers are outside the law; that is DF's villain cradle.

## Three folds for the Roblox hall (Brother Vellum's Grant of Belonging)

1. Grant = ETHIC line, not a gift: encode it `[ETHIC:BELONGING_GRANT:PUNISH_EXILE]` in the hall ledger so accepting it is only a crime if the hall's response token says so — otherwise it is PERSONAL_MATTER and the roll decides.
2. Temptation roll = VALUE vs counted chairs: weight = hall's chairs-counted history (its VALUE map) minus a d50 pressure roll; grant succeeds only if pressure > counted loyalty (mirror dwarves' CRAFTSMANSHIP:50 anchoring).
3. Vellum needs a HAMMERER-shaped executor with `[PUNISHMENT_EXEMPTION]` — the one who grants belonging must also be the one who cannot be exiled by it.
