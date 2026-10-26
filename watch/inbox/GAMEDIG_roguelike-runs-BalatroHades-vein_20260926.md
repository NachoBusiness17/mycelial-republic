# GAME DIG WHEEL SPEC (roguelike-runs-BalatroHades-vein, 30-game dig receipt, 2026-09-26)

# RUN WHEEL SPEC: ROGUELIKE RUNS, BALATRO / HADES VEIN (revision 2)

Assembled 2026-09-27 from three ask-given inputs: the mechanics synthesis (tags `[01]` through `[30]`), the retention-and-abuse synthesis (rr ids), and eight deep-dive findings (rr-01, rr-03, rr-04, rr-06, rr-08, rr-10, rr-13, rr-24). Carried material: every number tagged to a finding is that finding's, and every quotation is a digger-fetched verbatim quote carried from that finding's evidence field; the page lists in section 6 are the findings' own source records. Revision 2 adds work run in this session: two live page fetches, three repo file reads, and one arithmetic verification battery, all listed in the closing note. Anything labeled PROPOSED is a lane design value computed by me from cited constants, never a sourced fact about a game.

Lane socket assumptions, from the findings' verdict reasoning (`[04]`, `[13]`, `[25]`), now corroborated by code I read this session (see 4.1): the lane already owns VM currency (`LedgerExchange.luau`, currency attribute VirtueMarks, start 100), seasonal faucet zones (`OssuaryZone.luau`), and a documented economy falsifier (`SEASONAL_LAUNCH.md:131`). The boon-draft, faction-lobby, and Pilgrim-class surfaces are asserted by the findings; no file naming them was opened this session, so those three stay carried. Every gate, roll, and payout lands server-authoritative (invariant 1, section 5).

## REVISION 2 DISPOSITION (cold reader findings, 17 items)

| # | Finding | Disposition |
|---|---|---|
| 1 | Isaac 410 vs tier sum 430 | quarantined: current page wikitext carries neither number (session fetch); load-bearing uses are denominator-independent; see W4 and 3.3 |
| 2 | Broker rates vs arbitrage loop | reconciled: loop legs are limited deals (80% and 85% undercuts, inside the carried 50-85% band) plus one standard leg; arithmetic verified this session; see R3 and 5.3 |
| 3 | "Ten clone games" count error | header rewritten: 10 entries over 9 named games; the 10th clone verdict's identity is not recoverable from the ask and is filed owed (6.3) |
| 4 | Heat table bare-number ambiguity | convention stated (all values are totals at max ranks); sum verified 63 / 64 by script this session |
| 5 | Cap 20 vs Hell 25 unreconciled | reconciled: one 21-rung ladder, standard span 0-20, Hell span 5-25; lane inherits the single-cap form (4.3) |
| 6 | RoR2 figures underivable | difficultyValue 1/2/3 and the benchmark monster constants added; derivation shown; verified by script |
| 7 | Roblox standards claimed and disclaimed | reconciled: Community Standards page was read by the `[09]` digger; the distinct paid-random-item disclosure policy is the owed item; wording fixed in 4.1, 5.4, 6.3 |
| 8 | No lane-owned constants | added 4.0 LANE CONSTANTS v0 (PROPOSED, with derivations and acquisition-rate math run this session) |
| 9 | Respawn charges and assist dial undefined | defined in 4.0 (PROPOSED) |
| 10 | Faction-war interaction model missing | added 4.0b WAR SHELL v0 (PROPOSED) |
| 11 | No MVP or sequencing | added 4.6 PHASING (PROPOSED) |
| 12 | Middle Management unknown effect | resolved by session fetch: verbatim effect text now in W1 |
| 13 | "score +5%/rank" undefined referent | war score object defined in 4.0c (PROPOSED); matrix cell re-pointed |
| 14 | Closed relay | three repo citations converted to session-verified at exact lines; two page fetches added to 6.2; remaining relay limits stated in 6.3 |
| 15 | Retention case analogy-only | business-model mismatch and measurement plan stated in 4.1a; thresholds left as operator decisions |
| 16 | Missing paid-failure abuse family | Family K added plus invariant 12 (5.1, 5.5) |
| 17 | Minor debts (a)-(f) | all six fixed in place: Clone Bay ambiguity flagged (W6, 5.2), R1 sentence reworded, MT figures itemized (5.2), odds triplet tagged and flagged (matrix W3, 4.1), WP identifiers defined (5.2), night-clock decision made explicit (4.2) |

## 1. THE WHEEL: CLONED MECHANICS WITH THEIR NUMBERS

Ten wheel entries over nine named games; Hades occupies W1 and W2. The ask's census counts 10 clone verdicts across the 30 findings; the ninth and tenth named games plus one further clone verdict do not close the census (verdict fields per finding id were summarized in the ask, never enumerated), so the census line is carried as stated and the residual is filed owed in 6.3 rather than guessed.

### W1. Self-selected difficulty: heat menu + bounty rung law (Hades `[01]`, deepened rr-01; three condition effects re-fetched this session)

Unlocked after one final-boss clear. Ceiling 63 heat (64 in Hell Mode). Table convention: the Heat column shows the condition's total contribution at maximum ranks; per-rank splits are shown where they are non-uniform. The 15 standard-condition totals sum to 63 and Personal Liability adds 1 for the Hell Mode 64; this sum was verified by script this session.

| Condition | Effect | Ranks | Heat total |
|---|---|---|---|
| Hard Labor | foes +20% damage per rank | 5 | 5 (1/rank) |
| Lasting Consequences | healing -25% per rank | 4 | 4 (1/rank) |
| Convenience Fee | obol prices +40% per rank | 2 | 2 (1/rank) |
| Jury Summons | foes +20% per rank | 3 | 3 (1/rank) |
| Extreme Measures | boss rework per rank; rank 4 needs a House Contractor purchase after story completion plus one more final-boss fight (rr-01) | 4 | 10 (1/2/3/4) |
| Calisthenics Program | foe life +15% per rank | 2 | 2 (1/rank) |
| Benefits Package | most Armored foes have Perks, +1 per rank (fetched this session); 11 perks, certain perks banned from certain foe types since Patch 041 (rr-01) | 2 | 5 (2/3) |
| Middle Management | each Mini-boss Encounter contains +1 Armored foe (or some additional problem) (fetched this session) | 1 | 2 |
| Underworld Customs | the exit to each Underworld region requires purging 1 Boon to unlock it (fetched this session); the purge sells at full obol value (rr-01) | 1 | 2 |
| Forced Overtime | all foes bonus move and attack speed, +20% per rank (fetched this session) | 2 | 6 (3/rank) |
| Heightened Security | traps +400% damage | 1 | 1 |
| Routine Inspection | -3 Mirror talents per rank, bottom up; also strips Fated dice (rr-01) | 4 | 8 (2/rank) |
| Damage Control | 1 shield hit per rank | 2 | 2 (1/rank) |
| Approval Process | boon choices -1 per rank | 2 | 5 (2/3) |
| Tight Deadline | 9 min per region, -2 min per rank (5:00 floor); 5 true damage per second once expired, unreducible by any means including invulnerability; 9 listed pause cases (fishing, game paused, choosing a boon, and 6 more) | 3 | 6 (1/2/3) |
| Personal Liability (Hell Mode only, mandatory) | Auto Defense (brief invulnerability after a burst of damage) is +100% inactive (fetched this session) | 1 | 1 |

Session fetch note: Middle Management, Underworld Customs, Personal Liability, Benefits Package, Forced Overtime, and Tight Deadline effect texts above are quoted from the Pact_of_Punishment wikitext I fetched this session via `hades.fandom.com api.php?action=parse&page=Pact_of_Punishment&prop=wikitext` (curl, 15,947 bytes, scratch `C:/Users/foste/AppData/Local/Temp/hades_pact.json`); rr-01 remains the source for rank-4 Extreme Measures gating, the pause-case count, and patch history.

Hell Mode: fixed at file creation, disables God Mode, 5 mandatory one-rank conditions = 5 heat from run 1. God Mode (rr-01): 20% base damage resistance, +2% per run ended in death, 80% cap, resistance retained when toggled off, achievements unaffected, records stored separately.

Bounty rung law, quoted (`[01]`): "You can only claim rewards for the lowest Heat you have not yet completed, even if you defeat a boss at a higher heat". Cap reconciliation (derived from the two carried sentences): there is one 21-rung ladder; standard characters climb rungs 0 through 20; Hell Mode characters begin at rung 5 (their 5 mandatory heat) and climb to 25; both spans are 21 rungs, which is why the sources state 21 completed runs per weapon to collect all bounties. Per-boss drops of Diamond, Ambrosia, or Titan Blood at target heat; tracked independently per weapon, per boss, per heat level; 0-heat bounties tracked separately. Milestones: cosmetic statues at 8/16/32 heat; challenge gates at 5/10/15. First-clear curve (rr-01, self-selected Steam thread, 13 point estimates): median 18 attempts, range 8 to 60.

Patch trail (rr-01): 042 fixed unlimited Cast ammo via Routine Inspection; 048 redesigned Tight Deadline ("your time no longer resets between regions; clearing regions adds more time") and added Extreme Measures rank 4; 049 made one Doom instance proc Merciful End at most once; 052 fixed lifesteal under Lasting Consequences and final-boss event logic for boonless runs; cherry-picking is wiki-admitted ("conditions can be nearly ineffective against one particular weapon build").

### W2. The duo prerequisite graph (Hades `[01]`, deepened rr-01)

28 duo boons over 8 gods, a complete K8 graph (every god pairs with every other exactly once); Hermes and Chaos excluded. Wide gates: 1-of-4/5 slot boons or the god's Aid from each god; Merciful End needs Curse of Agony or Curse of Pain plus Divine Strike or Divine Flourish. Narrow single-boon gates: Lightning Phalanx (Phalanx Shot), Hunting Blades (Slicing Shot), Cold Fusion (Static Discharge), Cold Embrace (Crystal Beam), Crystal Clarity (Crystal Beam), Ice Wine (Trippy Shot), Blizzard Shot (Flood Shot), Curse of Drowning (Flood Shot/Flood Flare), Scintillating Feast (Trippy Shot) (rr-01). Vengeful Mood also needs 1 Revenge boon from any god; Lightning Rod needs the Infernal Soul Mirror talent; 7 duos cannot combine with Aspect of Beowulf. Offerable by either god of the pair; blocked in Trial of the Gods rooms. Duos are flat at acquisition, quoted (rr-01): "Special boons cannot be upgraded with Pom of Power". Collection payout: all 28 pays 15 Ambrosia.

Steering economy (rr-01): god keepsakes guarantee the next boon from their god once per run and carry +10/15/20% Rare-or-better all run; keepsake rank 2 at 25 cleared encounters equipped, rank 3 at 50; swap only between regions; a swapped-out keepsake cannot return that run (display case 10 gemstones). Yarn of Ariadne, 70 obols, until next boon: guarantees Rare, +25% Epic chance, +10% duo/legendary chance. Refreshing Nectar: the next 3 boons have upgraded rarity. Mirror talent Gods' Legacy: +10% Legendary-or-Duo chance over 10 ranks at 250 per rank (2,500 total). Base duo offer weight: unpublished (owed, 3.3). Patch trail: Patch 025 nerfed Merciful End on introduction; 042, 048, 049, 050, 051, 052 all re-tuned duo gates or procs.

### W3. Rarity damper + corruption meter (Gungeon `[11]`)

Magnificence (soft top-tier pool depletion, per run): +1 per S/A pickup; each floor starts with generated magnificence equal to its red + black chest count. Downgrade chance for the next S/A roll: (1 - (0.006260342 + 0.9935921 x e^(-1.626339 x m))) x 100%:

| m | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| downgrade % | 0 | 79.84 | 95.53 | 98.62 | 99.23 | 99.34 |

Curse (opt-in risk stat): 1 = 1% jam; 5 = 5% jam / 25% fused chests; 7 = 10% jam / 20% boss jam; 9 = 25% / 30%; 10+ = 50% / 50%, Lord of the Jammed spawns, shops lock; 20+ all chests fused; 47+ all chests mimics; 100+ no room rewards. Jammed enemies: health x3.5 + 10, +50% speed, cooldowns -33%, drop more money. Cleanse shrine free; negative curse pays 5 money per point.

### W4. Pool weights, sight decrementation, temptation fork (Isaac `[13]`, deepened rr-13)

Item weights: default 1; tuned exceptions 0.1 to 0.5 (Mega Blast 0.2 Devil pool; Delirious 0.4 Angel; rr-13 adds 0.2 on Plan C and Forget Me Now, 0.5 on Void, Abyss, Berserk!, Dark Arts, Lemegeton, Heartbreak). Sight decrementation: seeing an item decrements its weight (full decrement for most pools, one sighting removes it for the run); 0.5 shop and beggar pools (shop made full in Repentance); 0.4 golden and red chests; 0.1 library. Touching removes it from all pools. Exhausted pool falls back to the Treasure Room pool; exhausted Treasure Room yields only Breakfast.

Devil door odds: 1% base; +35% damageless boss fight; +99% damageless floor; +10% per blown-up shopkeeper; multiplicative decay x0.5 if the door was seen two floors ago, x0.25 if nearer; ceiling 204% (Afterbirth) / 254% (Repentance); page worked example: 145% base shows as 100%, falls to 36.25% once seen. Prices: 1 or 2 red heart containers tracking power; 3 soul hearts flat for builds with no red containers; a 2-heart deal is buyable holding 1 red heart; Keeper pays 15/30 cents (the currency-swap precedent).

Quality layer (rr-13, census quarantined): quality is a hidden 0-4 stat; the current Item_Quality wikitext, which I fetched this session via `bindingofisaacrebirth.fandom.com api.php?action=parse&page=Item_Quality` (curl with custom UA, 1,200 bytes, scratch `C:/Users/foste/AppData/Local/Temp/isaac_quality.json`), confirms the 0-4 range and that qualities are defined in `items_metadata.xml`, and carries no item census; the rr-13 digger's rendered read reported both a 410-item total and tier counts of Q4 = 5, Q3 = 220, Q2 = 180, Q1 = 20, Q0 = 5, which sum to 430; the 20-item gap is unresolved (verified by script this session: 5+220+180+20+5 = 430). Handling: the total is quarantined; the uses carried below are per-item and denominator-independent. "An item's Quality also directly scales with Devil Deal prices" (rr-13): Q4 devil items price at 2 hearts, Q3 at 1 (Brimstone and Mom's Knife confirmed in the fetched devil table of 94 rows, 24 actives + 70 passives); shop coin price = (2 x quality) + offset of -1/0/+1; Treasure Room spawn weights Q4 20 / Q3 10 / Q2 5 / Q1 2 / Q0 1.

Angel gate: a devil door spawned earlier in the run plus zero deals taken all run; selection by sequential coin flips (base 50%; +50% Rosary Bead; +50% donating 10 coins; +25% per Key Piece); flips multiply rather than sum (page math: 0.5 x 0.75 = 0.375 failure, so 62.5% angel).

Adjacent HP-priced gambles (rr-13): sacrifice room generation base 1/7, rising to 5/14 at full health; 1 full heart per spike; 12-step ladder: steps 1-2, 50% nothing / 50% 1 penny; step 3, 33% nothing / 67% lesser blessed fortune; step 4, 50/50 random chest; step 5, 33% 3 coins / 67% stronger fortune; step 6, 33% teleport to Angel Room / 67% chest; step 7, 33% angel item / 67% soul heart; step 8, 6-7 troll bombs; step 9, Uriel fight; step 10, 50% 7 soul hearts / 50% 30 coins; step 11, Gabriel fight; step 12 and after, 50% nothing / 50% teleport to Dark Room; counter resets each floor. Donation machine: lifetime meter persists across runs, cap 999; the 1000th donation explodes it, resets to 0, drops about 12 dimes; jam chance pre-Repentance flat 5% per coin (10 coins 40.13%, 25 coins 72.26% cumulative); Repentance resets per floor and scales with coins donated that floor (1 coin 0.15%, 10 coins 14.02%, 25 coins 61.53%, 50 coins 97.97%); 2% +1 Luck side roll per donation; bombing drops 6-14 pennies and reduces the lifetime total by dropped + 1 (a net loss).

### W5. Visible map + elite pricing (StS `[06]`, deepened rr-06)

Map: 7 columns x 15 floors (17 counting the boss chest); up to 6 locations per floor; every room 1-3 paths in and out; exactly 6 paths per map; paths never cross; pins: floor 1 all monsters, floor 9 all treasure, floor 15 all rest sites. Node weights on free floors: Normal 53% / Unknown 22% / Rest 12% / Elite 8% / Merchant 5%; Unknown resolves among Monster/Merchant/Treasure/Event with the picked type dropping to baseline and others incrementing, reset each act; Ascension 1 moves elite 8% to 16% and monster 53% to 45%. Placement bans: no elite or rest below floor 6; no consecutive elite/merchant/rest; no rest on floor 14; branch destinations unique. Elite payout: 1 random relic at 100% + 25-35 gold + card reward + score bonus (10/20/30 per elite by act; Champion 25 per no-damage elite). Gold curve: monsters 10-20 (avg 15), elites 25-35 (avg 30), boss 95-105 (avg 100). Relic odds 50/33/17; chest odds by size: small 75/25/0, medium 35/50/15, large 0/75/25 (rr-06; the `[05]` relics finding summarizes an aggregate 49/42/9 cut, a different table); boss relics only from bosses (choice of 3) or the Neow trade. Card removal 75 gold, +25 per use, shared across all shops in the run; Courier 20% stacks multiplicatively with Membership Card 50% for 60% (rr-06).

Ascension grammar: 20 cumulative levels per character; A1 unlocks by beating all three acts with that character; each further level by winning the previous; quoted (`[05]`): "Losing a run will NOT reset any progress"; +5% score per level to +100% at A20 (the score object this multiplies is the StS run score, rr-06's additive table; the lane analog is defined as a proposal in 4.0c); A16 raises shop prices 10%; A20 is two Act 3 bosses back to back. Designer anchor, quoted (Anthony Giovannetti, show notes, `[06]`): "The core design of Slay the Spire is risk versus reward." Measured funnel (rr-06, Steam global achievements, percent of all owners): first Act 1 boss 85.0%, first full clear 66.4%, Ascend 10 14.8%, Ascension 20 7.3%, full completion 2.7%; tail: about 6.6k average concurrents seven years after launch (SteamCharts, third-party estimate). Derived by rr-06: A20 on one character costs 21 wins minimum, 84 across four.

### W6. Crew skill table + pursuit clock (FTL `[20]`)

XP to level (Human cost in parentheses), three levels per skill, leveled only by doing the job:

| Skill | XP per level | Bonus at L1/L2 | Cap bonus |
|---|---|---|---|
| Piloting | 15 (13) | +5% / +7% evasion | +10% |
| Engines | 15 (13) | +5% / +7% evasion | +10% |
| Shields | 55 (50) | +10% / +20% faster recharge | +30% |
| Weapons | 65 (58) | +10% / +15% faster charge | +20% |
| Repair | 18 (16) | +10% / +20% faster repair | +20% |
| Combat | 8 (7) | +10% / +20% crew damage | +20% |

Clone Bay tax, carried verbatim: "cloning costs 20% of skill points in every skill, only 1 point in Combat" `[20]`. Source-ambiguity flag: the finding does not state whether the Combat loss is a flat 1 point or 20% capped at 1; the lane floor mentioned in 4.4 is a PROPOSED addition, labeled there. Economy: medium scrap 12-19 (sector 1) to 45-74 (sector 8), roughly 3.8x (derived from the sector table); repairs 2/3/4 scrap per hull point by sector band; store prices fixed 3 scrap per fuel, 6 per missile, 8 per drone part. Pursuit clock: the fleet advances each jump; an escaped scout doubles pursuit one turn; a mercenary delays 2 turns; nebula beacons halve (or cut by 1/5 inside nebula sectors) that turn's advance. Unlock gates: 2 of 3 behavioral achievements per ship for layout B; reach the final sector with layout B for layout C.

### W7. Covenant ladder + shop escalators (Monster Train `[23]`)

25 ranks, each unlocked by winning at the current maximum; any Covenant win masters every card in the winning deck (golden frame); win streaks live in cups bucketed 1-9 / 10-19 / 20-24 / 25, reset on a loss. Rank examples: rank 1 bosses +200/600/1301 HP; ranks 2 and 17 add Deadweight to the starting deck; ranks 6 and 13 add a primary-clan starter copy; rank 10 Emberdrain on the top unit; rank 11 reroll +20%; rank 16 purge +20%; rank 18 goods +20%; rank 20 middle floor -1 capacity; rank 25 final bosses +1000/+1500 HP. Shop escalators: card removal 50/75/100/150/200/250 (Covenant 0-15) and 60/90/120/180/240/300 (16-25), shared across all merchants in the run; reroll 50 gold once per merchant (60 at Covenant 11); artifacts, two figures carrying the wiki's own [verify] flag, itemized: (1) artifact base price 160-220, (2) the Covenant-18 merchant goods variant `[23]`. Sanctioned-shape precedent, quoted (`[23]`): "using mutators prevents all progression because you can make very easy runs - you do not gain XP, master cards, or unlock new covenant levels when using mutators".

### W8. Curse-priced altar + vendor ledger (UnderMine `[26]`)

Dev blog, quoted: "Prayers give the player one blessing and one curse". Penance removes a curse at a health price (formula unpublished); curse pool 66 at v1.2.0; reported cadence 5-6 curses per deep run. Price curses: Inflation +10% shop costs; Market Crash +20%; Tariffs x1.5 to all costs including health, curses, and keys (since 1.2.0; earlier x2; conflict flagged in 3.3); Security Theater locked shops charge 4 keys, 8 with Tariffs. Discount stack: Loyalty 10% per stack, hard cap 80% (cap added 0.2.2); Pilfer Ring 20%; memberships 1,200g program, 800g Silver Star, 1,800g Gold Star. Curse-payoff items: Twisted Blade +2% crit per minor curse, +4% per major; Aphotic Charm 1 HP per distinct curse per new room; Absolution 800g removes exactly 5 unique curses, no partial effect. Credit and debt: Gold card 5,000g limit at 0% interest; negative balance "is carried over to subsequent peasants" and becomes the Debt major curse blocking all gold buying until repaid; the Shop Keeper's vermin quest sets the balance to 0. Meta sink: 742,950g all permanent upgrades, 942,950g all upgrades.

### W9. Fail-forward banking (ScourgeBringer `[27]`)

One free Altar of Blood per realm (choose 1 of 3 blessings; 4 with Generous Altar); realms 5 of 7 per run; 15-20 rooms per realm. Knockout banking: leftover run Blood converts at 1300 to 1 Judge Blood (EA-era guides say 1000:1; flagged in 3.3); Instant Gift refunds 10% of total spent; Persistent Blessing carries one draft forward when the prior run found 3 or more; reroll costs 2 HP (Let's Roll). Meta tree: 29 skills, 7 branches, costs 1,1,1,2 / 1,2,2,3 / 2,2,3,4,6 / 3,4,6,8,12 / 4,8,14,20 / 5,10,18,30 / 35,30,30; branches gated behind named boss kills. Post-game: 17 stars across 10 difficulty modifiers.

### W10. Night meter + pity counter (Dredge `[28]`)

Panic: 5 stages; rises in darkness (faster with lights off), falls in daylight, resets when resting docked; night 18:00 to 04:00, encounters 20:00 to 04:00; mitigation is priced (lights 100 to 435 gold, per-lumen slowing, internal 4,000-lumen cap). Aberration odds stack: night flat +3%; green-glow spot +35%; last fish of a green-glow spot 100%; pity +0.5% per non-aberrated catch, reset on any aberration, cap 35% after 70 consecutive. Payout premium: Blue Mackerel 5.00 vs Grotesque Mackerel 15.00 (3x); exotics 35.71 vs 100-140; endgame gear priced in the rare currency itself (Tendon Rod costs any aberration).

## 2. RESKINS: SHAPES TO KEEP, CONSTANTS TO REBIND

### R1. Pressure ladders

- Balatro ante base chips, antes 1-8: 300 / 800 / 2,000 / 5,000 / 11,000 / 20,000 / 35,000 / 50,000; blind multipliers 1x small, 1.5x big, 2x boss (The Wall 4x, Showdown 8x, Violet Vessel 6x); the Ante 8 boss at 100,000 chips is the win line; stakes reprice the same ladder (Purple Stake Ante 8 base 200,000; rr-03 adds the full Green and Purple curves and the Endless rows: A24 1.6e77, A39 4.8e309 which overflows double precision to naneinf; Endless formula: Chip = Ante8 x ((1.6 + 0.75(Ante-8)) / (1 + 0.2(Ante-8)))^(Ante-8), rounded to 2 significant digits). Stake ladder is per deck, quoted (rr-03): "you must complete a run on the current highest unlocked stake for each specific deck individually." Hand ladder (rr-03): High Card 5 x 1 through Flush Five 160 x 16, each with per-level Planet upgrades; "There is no limit to how many times a poker hand can be leveled up", and levels reset each run.
- Luck be a Landlord rent ladder, floor 1: 25 / 50 / 100 / 150 / 225 / 300 / 350 / 425 / 575 / 625 / 675 / 777 coins; spins between payments 5,5,6,6,7,7,8,8,9,9,10,10 (derived: a 90-spin run pays 4,277 coins total); each spin costs 1 coin; win = 12 payments `[09]`.
- Endless ceilings, reference only: Balatro overflow past 1.8e308 at Ante 39 `[03]`; Noita caps firing at once per frame (60/sec) `[12]`; RoR2 enemy level caps at 99 `[10]`. Lane ruling: cap the endless math; an uncapped ceiling in a shared economy is a printer (G3). Concretely (rr-04's port): clamp or switch to integer math past 1e15, and record the cap hit as a completed-state event, the way Balatro's community reads Ante 39 as having finished endless rather than broken it.

### R2. Draft weights, rarity, pools

- Balatro shop (rr-03, rr-04): card weights Joker 20 / Tarot 4 / Planet 4 (71.4 / 14.3 / 14.3%); joker rarity 70 / 25 / 5; pool counts 61 / 64 / 20 / 5 = 150 jokers, 105 live on a fresh profile; duplicates cannot spawn on-screen without Showman; booster offer weights Standard/Arcana/Celestial 4 / 2 / 0.5 and Spectral 0.6 / 0.3 / 0.07; The Soul at 0.3% (3 in 1000 per card slot) is the only legendary source and legendaries are never buyable; reroll $5 base, +$1 each, resets each shop; packs and the voucher never restock on reroll, the voucher restocks after each boss blind; the first pack of every run is a guaranteed Normal Buffoon Pack (added 1.0.1f). Raw internal rarity integers were never found on any page read; the wiki's 70/25/5 is the only sourced figure (3.3; rr-04 re-confirmed the absence).
- StS relic odds 3:2:1 = 50 / 33 / 17; boss relics only from bosses or the Neow trade `[05]`, chest odds by size under W5 (rr-06).
- LbaL symbol draft odds by payments paid (C/U/R/VR): 0: 100/0/0/0; 1: 90/10/0/0; 2: 79/20/1/0; 3: 74/25/1/0; 4: 69/29/1.5/0.5; 5+: 68/30/1.5/0.5; post-rent guarantees: payments 1-5 all Uncommon+, 6-8 one Rare+, 9 two Rare+, 10+ all Rare+ (page self-flags the formula "seems somewhat wrong"; treat as community-observed) `[09]`.
- Peglin shop: fixed 5 orbs, 4 relics, 1 removal; orb price by rarity 15 / 25 / 35; relic flat 50; removal 30 then +15 per use (flat 50 before v0.8.6) `[15]`.
- Wildfrost charm pulls: dispenser 45 / 65 / 85, resetting to 45 each new visit; merchant charm price = base 45-65 plus or minus 30; item price = base x 0.8-1.2, minus 5; max 3 charm sockets per card, attachment permanent and order-snapshotted `[25]`.
- Hades boon shop: 150 obols per boon (200 before Patch 037); 5 exclusive slots (Attack/Special/Cast/Dash/Call); exchange raises rarity one tier and holds level; rarity roll formula "currently unsolved" per the wiki `[01]`.

### R3. Banking, interest, vendor math

- Balatro: $1 interest per $5 held, capped $5 per round (the $25 breakpoint); vouchers raise the cap to $10 ($50 held) and $20 ($100); $1 per unused hand; sell value floor(buy/2); interest snapshot rules (rr-04): payers firing after round end (Golden Joker, Rocket) count next round, in-run payers count immediately. Wiki intent, quoted: "This incentivizes the player to save money up to a point."
- The Bazaar (rr-24): per-item base cost in {2,3,4,6,8,12,16,24} doubling per tier step; modal bronze-start curve 2/4/8/16 (124 of 636 items); legendary buy 64 / sell 32 (Patch 6.0; wiki rows still read 100, flagged in 3.3); par-value sellback anywhere any time; premium buyers +1 small / +2 medium / +3 large; rerolls 2/4/6/8 by merchant tier (tiers unlock day 1/3/7/9); income 5 gold per in-run day (Patch 16.0 lowered it from 7); monster kills 2-6 gold by tier; a level every 8 XP; a run is 10 wins against async ghosts, chests 2/4/6 at 4/7/10 wins.
- Dead Cells two-loop: cells lost on death; Collector mutations 50-200 cells; Blacksmith forge sinks +500 cells at 5% per 25 invested, ++ 3,000 at 5% per 150, S 10,000 at 5% per 500, sequential gate, BSC-capped; cell multipliers x2/x2/x3 at 2/3/4 BSC `[07]`.
- Vampire Survivors (rr-08): PowerUp price = InitialPrice x (1 + Bought) + floor(20 x 1.1^TotalBought); full board 7,818,959 coins = 1,911,240 base + 5,907,719 fees (75.6% fees); the digger recomputed all three sums from the parsed 25-row table and matched the wiki exactly; fees flat (order-independent) since v0.7.2; free full Refund; Golden Eggs 10,000 each with per-stat hard caps and a float32 count cap.
- Hades Wretched Broker. Standard chain (one-way exchanges, `[02]`): 10 gemstones per key, 5 keys per nectar, 10 nectar per diamond, 2 diamonds per ambrosia, 1 ambrosia per titan blood. Standard-chain composition, verified by script this session: 1 titan blood = 1 ambrosia = 2 diamonds = 20 nectar = 100 keys = 1,000 gemstones. Limited deals undercut 50-85% `[02]`. The arbitrage loop (5.3) is built from limited deals against this chain and is reconciled there. Gift economy totals `[02]`: 151 Ambrosia total sink against 194 supply (126 boss bounties + 68 prophecies); 149 Nectar to max all affinity; companions 1-5 uses, upgrades 1/2/3/4 Ambrosia, 10 each.

### R4. Time and threat scaling

- Risk of Rain 2 (rr-10; constants below are the finding's, the derived numbers were re-verified by script this session): coeff = (playerFactor + timeInMinutes x timeFactor) x stageFactor; playerFactor = 1 + 0.3 x (playerCount - 1); timeFactor = 0.0506 x difficultyValue x playerCount^0.2; difficultyValue = 1 Drizzle / 2 Rainstorm / 3 Monsoon; stageFactor = 1.15^stagesCompleted; enemyLevel = 1 + (coeff - playerFactor) / 0.33; +30% health and +20% damage per level; named sub-difficulty rungs are +1 coeff each and cosmetic; HAHAHAHA begins at coeff 9. Derivation: solo Monsoon stage 1 gives coeff(t) = 1 + t x 0.1518, so coeff 9 lands at t = 8 / 0.1518 = 52.7 min (script: 52.7); at a 5 min/stage pace, stage 6 lands at 25 min. The structural anti-farm is the exponent split: chest cost = baseCost x coeff^1.25 (small chest base $25: $25.00 at coeff 1, $444.57 at 10, $1,755.26 at 30, script-verified). Income: enemyGoldReward = 2 x coeff x monsterValue x rewardMultiplier. Benchmark monster for the kills-per-chest figure (rr-06's table is generic; rr-10's computation fixes it): the Lemurian, monsterValue 11, under a Fast/Slow director whose rewardMultiplier is 0.2, paying 2 x 11 x 0.2 = 4.40 x coeff per kill. Kills per small chest = 25 x coeff^1.25 / (4.40 x coeff) = 5.68 x coeff^0.25: 5.7 at coeff 1, 10.1 at 10, 13.3 at 30 (script-verified); farming efficiency decays 2.34x from coeff 1 to 30 (30^0.25 = 2.3403). Teleporter: charge rate = fraction of living players inside the roughly 120m dome; minimum 90 seconds; natural spawns stop at 99%; interactables outside the dome lock. Bazaar clock pause, quoted: "The time and difficulty meters are paused while the player is in this map."
- Dome Keeper: cycle duration = 60 + 45 x sqrt(TileCount/1000) x IronMined% (24 seconds shorter on the hardest difficulty); threat weights iron x0.6, cobalt x2.2, water x1.2, gadget x8; cycle term round(cycle x (9 + difficulty + cycle x 0.15)) + cycle x 2, all x (1 + difficulty x 0.1), minimum 15; final wave max(800, runWeight x 4.5); inter-wave timers 72 / 66 / 60 / 48 seconds by difficulty; prestige multiplier starts 20, decays 1 per cycle, hard 20-cycle cap `[16]`.
- Loop Hero banking tiers: retreat at the campfire keeps 100%, mid-loop retreat 60%, death 30%; the campfire heals 20% max HP per crossing; counterweights: 10 rocks or mountains spawn a Goblin Camp, 2 villages spawn a Bandit Camp `[14]`.

### R5. Risk meters and morale

- Death Road to Canada: morale 0-6 per survivor; food 2 per member per day (3 big eaters, 1 tiny); a full-ration day gives +1 morale to anyone below 2 (+2 with high Attitude); despair roll once per day below 0: 5% base +1% per point below 0 (+15% despair trait), triggered by the highest-loyalty survivor (prose says 5% base while the outcome table row reads 10%; unresolved, 3.3); outcomes: destroy 3 supplies / 5 food / 3 ammo + 1 damage to all / 1 damage to the party / a member's morale set to 0 / shove / steal 20 supplies and leave / leave with weapons + 15 supplies / leave plus 3 damage to all; Haze gate at party average under -1: end the run or face a hard siege, surviving it pays +4 morale to all `[19]`.
- Loop Hero formation synergies: 3x3 rocks/mountains = Peak (+48% health, one per expedition, Harpy every 2 days); Treasury pays a random resource per adjacent card placed and a lump when all 8 tiles fill; River multiplies adjacent landscape effects x2 / x4 / x6 / x8 by sides touched; 20 Noticeable Change = 1 Metamorphosis `[14]`.

### R6. In-run mastery ticks

- Astronarch mana clock: flat 10 MP per second for every unit; max mana equals ability cost; ability cost floor 10 (fastest cadence 1 cast per second); hero MP staircase 52 to 92 in +2 steps (one cast every 5.2 to 9.2 seconds); Symbiote -3/6/9 cost per cast cumulative within a fight; Brain Sage heals 100/200/300 per 50 MP expended `[17]`.
- Into the Breach pilot XP: 1 XP per Vek HP killed; two skills at 25 and 50 more (75 cap); indirect kills split across the squad; skill pool exactly 4 candidates, 2 drawn and pre-rolled per timeline `[21]`.
- Hades keepsakes: rank 2 at 25 cleared encounters equipped, rank 3 at 50; details under W2 `[02]`.
- HoloCure duplicate consolation: every dupe raises G. Rank by 1 for +1 HP, +1% ATK, +1% SPD, stacking 20 times (cap at rank 21); every dupe mints 1 Gambler's Tear (7 = any character, 15 = outfit, banner-locked); pulls at 1,000 coins `[18]`.
- FTL station skills: the W6 table; the finding's port is per-class station mastery with visible integer tiers inside runs `[20]`.

### R7. Loss-pays ladders and unlock gates

- Slice & Dice: cumulative deaths 25 / 50 / 75 / 100 / 150 / 200 unlock items, heroes Wraith and Roulette, and the Permadeath curse; a new mode every 15 wins from 15 to 195; undo 500 times unlocks 11 items `[22]`.
- Balatro gate grammar (rr-03, rr-04): loss gates (Mr. Bones: lose 5 runs), grind gates (Acrobat: play 200 hands; Bloodstone: 30 heart-suit cards), win gates (Blueprint: win a run); 45 of 150 jokers locked on run one; 75 unlockables (45 jokers, 14 decks, 16 vouchers); unlock conditions visible on hover; the Unlock All valve exists at the cost of achievements for the profile; gold-stake Soul pity steer (1.0.1f: the first Legendary Joker on that seed is one the player has not won with on Gold Stake).
- Into the Breach coins: 70 achievements at 1 coin each; squads cost 2-4 coins, the Secret Squad 25; only the Last Traveler keeps XP across timelines `[21]`.
- Noita unlock ledger: 99 spells behind permanent gates, split 31 boss, 26 quest, 14 orb, 13 note, 15 experimental `[12]`.
- Dead Cells blueprint chase: drop tiers 100% (104 blueprints) / 10% (33) / 1.7% (53) / 0.4% (64) / 0.03% (2); per-biome cap of 1 outfit + 1 item per run; pity valve = Hunter's Grenade (150-cell unlock, 3,000 gold, guaranteed rare blueprint from a targeted enemy at 40% HP, explicitly allowed to exceed the cap) plus the Hunter's Mirror naming the holder `[07]`.
- Monster Train mastery matrix: best win tracked per clan pairing (5 x 5); full mastery at level 10 plus all cards plus Covenant 25 wins on all combos `[23]`.

### R8. Ordered-slot assembly (the authored-build hook)

- Noita: non-shuffle wands cast left to right; a modifier or multicast at the end of the queue wraps back to the head; a wand fires at most once per frame; delay reductions placed last apply right before recharge `[12]`.
- Peglin: crit pegs relocate every shot and apply retroactively across the whole bounce chain; per-peg accumulation capped at 999 damage (cap added v0.8.13) `[15]`.
- Cobalt Core: 1 Evade = 1 lane move; overheat at 3+ heat end of turn deals 1 hull damage and resets; 3 energy per turn; hand cap 10; repair yards heal exactly 50% of max hull rounded down; the wiki's own loop guide names the seam ("a draw card can re-draw itself") and the dev counters are the hard-coded 99-loop stop plus trash-card injection `[29]`.
- Balatro trigger-order law (rr-03): +Mult before xMult scores higher (40 x ((4+4)x2) = 640 chips vs 480 for the reversed placement, a 33% gap from ordering alone); retriggers stack additively. Lane: slot order becomes a program, and trigger order plus retrigger additivity get written into the spec before launch.

## 3. SKIPS AND WHY

### 3.1 Skip outright

1. The DRTC ZP shop: the lane already owns a persistent wallet; cloning it duplicates the VM socket `[19]`.
2. Client-rolled gacha with unpublished odds (the HoloCure shape): a server platform needs published odds, and the HoloCure save sits in a plaintext file that community editors already target; keep only the dupe-consolation curve (R6) `[18]`. Owed: the current Roblox paid-random-item disclosure policy page was never fetched; verify it before shipping any pull mechanic `[18]`, `[09]`.
3. The Potion Craft timing minigame: its speed is tied to framerate, and Roblox clients control their own frame timing. Keep the pricing curves (tier multipliers 1 / 1.75 / 2.5; multi-effect request stacking x1.25 / x1.5 / x2.5 / x5; haggle bands 20/30/40/45/50% with failure penalties 0/10/20/25/30; haggle costs 1 popularity point) and drop the reflex layer `[30]`.
4. The Astronarch "piety" framing: the digger's full-wiki search returned 0 hits for piety, pious, faith, and worship; the real system is the mana clock (R6). No religion economy on this evidence `[17]`.
5. Single-player infinite ceilings as shipped content: the Balatro naneinf route (45 held Steel Kings passing 1.8e308), the LbaL 9.9e247 coin crash boundary, the RoR2 Shaped Glass 128th-stack float death; in a shared economy these are printers, so cap them `[03]`, `[09]`, `[10]`.
6. Per-death XP taxes on the Pilgrim: Into the Breach's Cyborg pilots lose 25 XP per disable and players park them in backline mechs to dodge it `[21]`.

### 3.2 Premise corrections carried into this spec

- The Bazaar has no shop freeze. Every "Freeze" reference in its live patch notes is the combat keyword; rr-24 re-verified the absence across official notes (through Nov 2025), the Steam feed (through Sep 2026), the wiki, and two guides. The actual refresh controls are priced rerolls (2/4/6/8 by merchant tier) and, since Patch 15.0, a consumable encounter reroll (Reroll Token, replaced by Dragon Statue at Tempo cost 8 in Patch 18.0). If the lane wants carry-over, the only sourced genre convention is Hearthstone Battlegrounds freeze, quoted: "Frozen minions stay in the shop next turn." `[24]`
- Cobalt Core never uses the word orbit; the mechanic is Evade and lane movement `[29]`.
- Astronarch has no piety system; see 3.1 item 4 `[17]`.

### 3.3 Numbers to distrust (era conflicts, self-flags, owed items)

| Number | Conflict | Handling |
|---|---|---|
| Isaac item census vs tier sum | rr-13's rendered read: 410 items stated, tier counts 5+220+180+20+5 = 430 (sum verified by script this session); my session fetch of the current Item_Quality wikitext (1,200 bytes) carries neither number | total quarantined; the price function and per-tier weights carried below it are per-item and denominator-independent; a re-dig of the rendered page or items_metadata.xml is owed |
| UnderMine Tariffs | x1.5 since 1.2.0 (dedicated page) vs x2 (Altar and Pilfer Shop pages) | digger treated the patch-noted page as authoritative `[26]` |
| ScourgeBringer crystallization | 1300:1 (wiki, 1.44 era) vs 1000:1 (EA guides); shop-smash 500% (EA) vs 200% + 3-item rotation (1.44) | both quoted, wiki preferred `[27]` |
| Noita uncapped capacity roll | 1 in 10,000 (Wand page) vs 1/10,001 (Wands page) | both quoted as printed `[12]` |
| LbaL rarity formula | page's own "seems somewhat wrong" caveat + standards banner | community-observed `[09]` |
| Balatro rarity raw integers | community 100/28.5/4.5 never found on any page read (rr-04 searched again) | only the wiki's 70/25/5 claimed `[04]` |
| RoR2 0.0506 and playerCount^0.2 | predate or include the +10% rate bump, unstated on the page | page gap `[10]` |
| Monster Train merchant figures | wiki's own [verify] flag on two figures: artifact base 160-220, and the Covenant-18 goods variant | unverified, itemized `[23]` |
| DRTC despair base | prose 5% vs outcome table row 10% | unresolved `[19]` |
| Hades duo offer weights, Gods' Legacy percentages, boon rarity formula | never fetched / "currently unsolved" | owed `[01]` |
| Dead Cells save-scumming | community-reported only, never verified from a fetched page | asserted nowhere `[07]` |
| The Bazaar Chunk of Gold and legendary prices | wiki 3/6/9/12 and 100 vs official patches 2/4/6/8 and 64/32 | official preferred, wiki stale `[24]` |
| Loop Hero Empty Treasury payout | pages say only "a large amount of resources" | unquantified `[14]` |

## 4. LANE LANDING

### 4.0 LANE CONSTANTS v0 (PROPOSED; every value below is a design proposal computed from cited constants, labeled by derivation; none is a sourced fact about any game)

Anchor facts verified in repo code I read this session: VM start 100 per player (`roblox/src/server/LedgerExchange.luau:285`, attribute VirtueMarks set to 100 on join); slot income every 10 seconds times 1.5^Rebirths, uncapped in code (`LedgerExchange.luau:261-280`, multiplier at line 276); candy faucet capped 6 per floor per day (`roblox/src/server/OssuaryZone.luau:241`), 3 floors (`OssuaryZone.luau:33`), code comment stating max 12 VM/floor/day = 36/day, 72 with the Candy Doubler (`OssuaryZone.luau:236-240`); the falsifier line ("If Candy Bones inflow exceeds Exchange sink, the economy prints VM") at `roblox/docs/SEASONAL_LAUNCH.md:131-132` with the landed cap named at lines 133-134.

| Constant | Proposed value | Derivation |
|---|---|---|
| Draft pack price | 20 VM | 36 VM/day faucet (verified) / 20 = 1.8 packs/day, matching Balatro's early-run buy cadence of 2-3 per shop `[03]` |
| Reroll price | 10 VM base, +5 per reroll, resets each shop | Balatro $5 + $1 on a $4 pack (ratio 1.25x pack, escalation 0.2x pack) rebinding 1:0.5:0.25 onto the 20 VM pack |
| Interest | 1 VM per 20 held, capped 5 per cycle | Balatro $1 per $5 capped $5; breakpoint 100 VM = the verified start wallet, sits above one pack plus one reroll (30 VM) exactly as $25 sits above $9 |
| Two-loop drop tiers | 100% / 10% / 1.7% / 0.4% / 0.03% | carried verbatim from Dead Cells `[07]` |
| Expected chase at 36 VM/day and 20 VM per draft | 10% tier: 5.6 days; 1.7%: 32.7 days; 0.4%: 138.9 days; 0.03%: 1,851.9 days | 1/(p x 1.8 pulls/day), computed by script this session; the 0.03% tier is unreachable inside a season and must ride the pity valve (Hunter's Grenade analog), which is why 4.1 prices it in VM |
| Pilgrim respawn charges | cap 3; regen 1 per act cleared | Isaac 3-soul-heart flat price for no-red builds `[13]`; cap 3 makes a Q4 dark boon (2 charges) plus one more pick the full budget |
| Dark boon prices | Q3 boon = 1 charge; Q4 boon = 2 charges; Q4 on a shield-only build = 3 charges (full budget) | Isaac quality pricing: Q4 devil items 2 hearts, Q3 1 heart `[13]` rr-13; the 3-charge surcharge tier carried from the finding's port |
| Assist dial | +2% damage resistance per lost war objective (party present), -2% per won objective, floor 20%, cap 80% | God Mode 20/+2/80 `[01]`; personal per player (a faction-wide dial is the collusion surface, Family K); win-decay added so tanking cannot stack it (5.5) |
| War shell | see 4.0b | PROPOSED |
| War score | see 4.0c | PROPOSED |

### 4.0b WAR SHELL v0 (PROPOSED; no lane source read this session defines any of these; the only verified lane facts are the VM pool, the faucet caps, and that a faction war exists per rr-08's LINKS-337 read)

Two factions per war. A war is a weekly window containing 6 scheduled runs (sessions). Faction heat pick: bound at war open by the faction owner (top-3 contributors of the prior war), locked at each run's start; players joining mid-war inherit the lock. Posted path: the faction's StS-contract act path posts at war open (W5). Contested elite: an elite node open to both factions during its scheduled window; the faucet (VM + boon + card) is awarded to the first server-verified clear; on collision (both parties inside the window), the second party's server instance reroutes to the alternate elite, and the contest is resolved by clear timestamps, head-to-head PvP stays out of scope for this revision. Party size cap 4, one Pilgrim slot per party. The pursuit clock (W6 analog) advances one tick per objective regardless of outcome. All of 4.0b is a proposal awaiting operator ratification; it exists so that "contested" and "faction picks" have referents.

### 4.0c WAR SCORE (PROPOSED; the lane currently defines no score object in any source I read; this gives the W1 "+5%/rank analog" and W5's StS score analog a target)

Per-faction season points: +1 per floor cleared, +10/+20/+30 per elite by act (StS elite score bands, rr-06), +50 per war objective, multiplied by (1 + 0.05 x faction covenant rank), capped at +100% (StS A20 cap, `[05]`). Displayed on the war board; seeds the next war's matchmaking and ladder; converts to zero VM by design (score and currency stay separate, per the welding law, so a score run can never become a farm). W1's matrix cell refers here.

### 4.0d COVERAGE MATRIX

Every wheel entry lands in at least one socket; PROPOSED referents point into 4.0.

| Wheel | VM economy | Boon drafts | Faction war | Pilgrim |
|---|---|---|---|---|
| W1 heat + rungs | sanitized configs pay zero VM; war score +5%/rank (4.0c) | Approval Process -1 choice as a heat condition | heat menu per faction bound at war open (4.0b); lowest-rung payouts; milestones 8/16/32; gates 5/10/15; single-cap ladder inherited | personal assist dial (4.0) |
| W2 duo graph | collection payout (all 28) | K8 topology; narrow gates as commitment; steering items rank 25/50 | cross-faction pair collection chase | pair gates read the Pilgrim's held boons |
| W3 damper + curse | corruption meter on the wallet: 50%-off vendor at +2.5 curse per purchase and a steal penalty at +1 curse with odds 100/50/20 (both carried from `[11]`'s lane note; the odds triplet's referent is unspecified in the ask and is flagged owed), faction-visible enforcer at cap | per-player damper across the war session, reset at war end | enforcer is faction-visible | boosted drops priced into the meter |
| W4 pools + fork | Keeper 15/30 cents currency-swap precedent | sight decrement server-side; dark/pure fork; exhausted-pool fallback | per-siege-captain temptation beat | dark boons priced in respawn charges per 4.0 |
| W5 map + elites | contested elite faucets pay VM + boon + card | elite pays guaranteed relic-tier draft at 50/33/17 | posted paths per 4.0b; one burning elite per act holds the key appointment | elite risk prices as party-wipe economics |
| W6 skills + pursuit | sector-band repair pricing | station mastery tiers visible in-run | pursuit clock advances every objective (4.0b) | Clone Bay 20% tax with PROPOSED floor (4.4); one carryover |
| W7 covenant | escalator costs shared across the whole war | rank examples reprice draft sizes | 25-rank ladder per faction; streak cups; mutators pay zero | wipe counts toward streak reset rules |
| W8 altar + ledger | vendor ledger; debt succession; discount stack cap 80% | 1 minor curse per draft (the altar) | curse-ledger drama is faction-visible | debt survives the shared respawn, attaches to the spender |
| W9 fail-forward banking | knockout banking 1300:1, rate-limited per 5.5; 10% refund; carry-forward at 3+ | Persistent Blessing draft carry | realm gates 5 of 7 | wipes bank into Judge-Blood-analog meta |
| W10 night + pity | mitigation ladder priced in VM (lights 100-435 analog) | exclusive night pools on the war-local clock (4.2); +3% odds; +0.5%/catch pity to 35% | stage thresholds gate faction-war hazards | safe-zone rest resets the meter |

### 4.1 VM economy

- 4.1a EVIDENCE BASIS AND MODEL MISMATCH (stated plainly): every retention structure in this spec comes from premium single-purchase games with 20-120 minute run shapes (Hades, Balatro, StS, and peers); the lane is a Roblox free-to-play surface with shorter sessions and a different audience. No behavioral telemetry (DAU, D1/D7/D30, session length) exists in any source read (6.3). The spec therefore claims structures, never outcomes: what ships is the ladder-and-valve architecture plus the day-one instrumentation of invariant 11 (per-boon pick rates, per-combination win rates, return-per-session). Target thresholds and kill criteria for each wheel system are operator decisions taken against that telemetry once it exists; this document declines to invent them.
- Two-loop split (Dead Cells `[07]`): war income is volatile VM until banked at a faction tile; the banked layer buys a permanent unlock checklist whose drop tiers run 100 / 10 / 1.7 / 0.4 / 0.03%; the acquisition-rate math at 4.0's proposed pricing makes the 0.4% tier a 139-day chase and the 0.03% tier season-unreachable, which is the intended shape only if the pity valve (Hunter's-Grenade analog, priced in VM) carries the tail; every drafted outcome advances at least one track (HoloCure consolation grammar).
- Interest with caps (Balatro `[03]`, `[04]`; rebinding in 4.0): held VM earns 1 per 20 to a per-cycle cap of 5; the breakpoint (100 VM) sits above one pack plus one reroll (30 VM) so saving and spending stay in tension; hoards get use-by dates using the rental ($3 per round) and perishable (5 rounds) decay templates (rr-04 patch 7).
- Fee curve as burn (VS rr-08): every meta upgrade charges InitialPrice x (1 + Bought) + floor(20 x 1.1^TotalBought); fees are a pure VM sink (75.6% of the VS board); free Refund keeps theorycrafting costless.
- Vendor ledger (UnderMine `[26]` + Bazaar rr-24): discount stacks hard-capped (Loyalty 80% precedent); fixed-price memberships; par refund pays min(purchase price, current value) so post-purchase value gains never cash out above cost (rr-24 patch 1); on-sell-effect items sell for 0 (Patch 6.0 pattern); credit personal with a 5,000g-analog limit at 0%; debt survives respawn and attaches to the spender.
- Threat-welded income (RoR2 rr-10): payouts scale at coeff^1 and costs at coeff^1.25, so farming efficiency decays 2.34x across a session; difficulty multipliers stay welded to income (the Dead Cells x2/x2/x3 BSC direction).
- Platform-law reconciliation: the odds-disclosure and no-empty-outcome requirements are carried from the Roblox Community Standards page that the `[09]` digger fetched and read (about.roblox.com/community-standards is in that finding's source list, and the requirements are quoted in its synthesis). The separately owed item is the current paid-random-item disclosure policy, a distinct and more specific Roblox policy page that no digger in this chain fetched. Consequence: the consolation track ships as a requirement carried secondhand from `[09]`, and final compliance of any paid pull surface is gated on the owed policy fetch (5.4).
- Live lane code, verified by my own reads this session (superseding the carried rr-08 citations): `LedgerExchange.tick` pays every player their slot sum floored x 1.5^Rebirths each 10 seconds with no cap (`roblox/src/server/LedgerExchange.luau:261-280`, multiplier at :276); new players start at 100 VirtueMarks (`:285`); the candy faucet is capped at 6 per floor per day (`roblox/src/server/OssuaryZone.luau:241`) over 3 floors (`:33`), with the code comment stating 12 VM/floor/day = 36/day, 72 with the doubler (`:236-240`); the falsifier line sits at `roblox/docs/SEASONAL_LAUNCH.md:131-132`. Big Trouser's uncapped +1% Greed per level is the cautionary pattern against the uncapped rebirth multiplier: cap it (x1.5 to a named ceiling, then additive) or add a per-day payout cap.

### 4.2 Boon drafts

- Topology (W2 `[01]`): 8 factions, 28 pair boons, wide and narrow gates; narrow gates priced as build commitment; all-28 collection payout; steering keepsake analogs rank at 25/50 encounters and carry +10/15/20%.
- Damper (W3 `[11]`): per-player magnificence on the draft pool, carried across the war session, reset at war end; the 79.84 / 95.53 / 98.62 curve self-cools a hot streak while the pool ceiling sinks instead of hard-zeroing.
- Sight decrementation (W4 `[13]`): offers deplete server-side on sight; window-shopping is a decision; passed pedestals grow strictly rarer; exhausted pools fall back to a named floor item (Breakfast analog).
- Dark/pure fork (W4 `[13]`, rr-13): dark boons priced in respawn charges per 4.0 (Q3 = 1, Q4 = 2, Q4 shield-only = 3 of a 3-charge budget regenerating 1 per act); purity pool behind zero dark boons all war, tracked on a visible ledger so the squad polices its own deal-takers (rr-13 retention port); deathless-floor +99%-analog odds; x0.25 seen-offer decay forces commitment; quality-tier pricing ports the Isaac price function directly.
- Jackpot handling (rr-04): keep jackpot-tier boons (Soul-analog, 0.3%) personal, excluded from the Pilgrim share, and steered per player for completion on the gold-stake model.
- Sockets and order (R8 + `[25]`): 3 sockets per loadout card, permanent order-snapshotted attachment; slot order as a program; trigger order and retrigger additivity specified pre-launch (the 640-vs-480 gap is 33% from ordering alone); iteration cap 99 plus trash injection ship before the first combo boons.
- Mirror boss (`[25]`): field the previous war's winning charm-stacked loadout as the next war's phase-1 raid boss (source shape: leader HP x3, Snow immunity, Counter +1).
- Night pools (W10 `[28]`), clock decision made explicit (PROPOSED): night windows run on the war-local clock (phases inside a scheduled run), so exclusive pools never gate on real-world time of day; real-time exclusive pools are rejected in this revision because they put FOMO pressure and timezone exclusion on a Roblox audience; the operator may override.

### 4.3 Faction war

- Heat menu + rung law (W1 `[01]`): the faction's heat pick binds at war open (4.0b) and locks at run start; payouts ladder per faction under the lowest-incomplete-rung rule, ported verbatim; each rung costs exactly one run. Cap inheritance, stated: the lane takes the single-cap form (one ladder, rungs 0 through the cap); the offset variant (Hell Mode's start-5 window) is optional and, if used, shifts the window by exactly the mandatory heat it imposes. Milestones at 8/16/32; gates at 5/10/15. The finding's own ruling: self-selected difficulty in a multiplayer economy otherwise prints free rewards `[01]`.
- Pre-committed paths (W5 `[06]`, rr-06): the faction's act path posts at war open; clone the generator contract whole (15 floors + boss + chest, 6 non-crossing paths, pins on floors 1/9/15, weights 53/22/12/8/5 with the rank-1 analog doubling elite weight, placement bans); elites become contested VM-and-boon faucets resolved per 4.0b; one burning elite per act per faction holds the key appointment (source buffs: +25% max HP, act-scaled Strength/Metallicize/Regenerate).
- Clock antagonist (R4 `[10]`, `[16]`): a visible countdown on the war heartbeat; VM harvested during the countdown scales the enemy push (Dome Keeper threat weights); the payout multiplier decays across the extraction window (prestige 20, -1 per cycle, 20-cycle cap); the draft-phase clock freeze is zone-scoped (the Bazaar pause is the precedent; the Void Fields four-patch saga is the counter-lesson: pauses only inside the draft zone, stalling anywhere escalates a cost).
- Sanitized configs (W7 `[23]`): private, solo, and mutated configs pay zero faction contribution and zero VM, on the Monster Train mutator law quoted in W7.
- Assist dial (rr-01, parameters in 4.0, PROPOSED): +2% per lost war objective with the player's party present, -2% per won objective, floor 20%, cap 80%, personal, rewards preserved, records stored separately.
- Morale layer (R5 `[19]`): party morale 0-6 across the war session; despair drains priced in VM and boons; Haze-gate analog at party average under -1: end the run or face a hard siege, survivors paid +4 morale.

### 4.4 Pilgrim

- Exactly one carryover (`[21]`): a single named attachment object keeps mastery across wipes (Last Traveler precedent).
- Respawn priced in mastery (`[20]`): the Clone Bay 20% skill-point tax (verbatim text and its ambiguity flagged in W6); PROPOSED lane floor: the tax never reduces any skill below level 1, so a veteran never zeroes. No per-death XP tax on the dying class (the ITB Cyborg anti-pattern).
- Wipes as progression currency (`[03]`, `[22]`): loss-gated unlocks (lose 5 runs) and the cumulative death ladder 25 / 50 / 75 / 100 / 150 / 200, both under the Family K rate limits in 5.5.
- Wounded return (`[25]`): a wiped Pilgrim re-enters wounded with sockets intact (Injured Companion pity hook).
- Visible tiers (`[20]`): per-station mastery with small integer tiers (+5 / +7 / +10 grammar), leveled only by doing the job.
- Debt succession (`[26]`): personal credit line; negative balance carries to the next life ("This amount is carried over to subsequent peasants") and blocks gold-tier buying until repaid; debt attaches to the spender, never the team.
- Share discipline (rr-04, `[19]`, `[21]`): the Pilgrim share excludes jackpot-tier boons; join-time party costs and inherited party state close the mass-recruit dodge; zero floor-immune members; undo lives only inside a live turn, costs VM, and achievement checks run at cycle commit.

### 4.6 PHASING (PROPOSED; each phase gated by the abuse patch that must precede it)

- Phase 0 (before any wheel system): invariants 1-8 (5.1) land as server infrastructure; the Roblox paid-random disclosure policy fetch (5.4) closes; telemetry hooks (invariant 11) wire.
- Phase 1 MVP: W1 rung law + heat menu (single cap), W5 posted paths + contested elites under the 4.0b shell, W4 fork priced in respawn charges, two-loop VM banking with the fee curve and pity valve, 4.0 constants. Everything here is pay-on-clear and per-run bounded, so Families A-G are closed by Phase 0 infrastructure.
- Phase 2: W2 duo graph + W3 damper + R8 sockets and ordered-slot boons, shipping only after the loop guards (iteration cap 99, trash injection, degraded-copy rule) and after per-boon telemetry from Phase 1 has a baseline.
- Phase 3: W10 night windows (war-local clock), R5 morale and despair, mirror boss, W7 covenant ladder with streak cups, Family K failure-pays rate limits fully exercised by then.
- Explicitly deferred until telemetry exists: any real-time-gated pool, any paid pull surface, endless-mode math beyond the capped ladder.

## 5. ABUSE PATCHES OWED

### 5.1 Day-one build invariants (retention synthesis; families A-K in parentheses)

1. Server-authoritative gates, rolls, and wallets; the client requests, the server decides. (A)
2. Rolls commit at draw time; rejoin resumes committed state; inventory ops idempotent; no mid-wave menu re-triggers. (B)
3. Countdowns advance independent of player state; payouts land on cycle completion; anti-stall escalation; difficulty multipliers stay welded to income. (C, E)
4. Iteration caps on every trigger chain; ceilings on every stack; integer clamps below float limits; fine-print taxation as the standing answer to discovered engines. (D)
5. Trade graphs audited for positive cycles; value-added sell caps; discounts priced under marginal yield; rate-limited repeatable payouts; cooldown on debt forgiveness. (F)
6. Lowest-incomplete-rung payout on all self-selected difficulty; sanitized configs pay zero. (E)
7. Identical odds rolls on every entry path; coin sinks walled off from offer odds; sight decrementation server-side. (G)
8. Zero client-timing-priced gates. (H)
9. Pilgrim share excludes jackpot-tier boons; credit personal; no floor-immune members; no per-death mastery tax on the dying class; undo priced and committed at cycle end. (I)
10. Published odds plus consolation on every paid random surface; gambling framing audited against Roblox standards. (J)
11. Telemetry from day one: per-boon and per-combination pick rates (Monster Train's Remnant+Umbra fusion became must-use and forced a core-rules change), plus upload-all-runs logging as the cheat-detection feed `[23]`.
12. Every failure-pays mechanic is rate-limited per account per window and engagement-gated; assist state is personal and decays on wins. (K)

### 5.2 Per-wheel patches, each with its patch precedent

- W1 heat: per-condition composition-immunity audit before shipping (Underworld Customs was fully bypassed boonless; press admits "free point of heat" picks); activity-agnostic timers, pausing only when the war pauses (the 9-case Tight Deadline pause list is the seam list); one-proc-per-trigger combo rule (Patch 049); gate edges and weights ship as tunable data (Supergiant re-tuned gates in 048 through 052); cap repeat purchases of any stacking buff per run or run the Convenience Fee +40%/rank cost curve on it (Chaos stacking survived every patch through 057); conditions locked at run start.
- W2 duos: offer weights were never published even for Hades, so ours are designed, telemetry-watched, and tunable from day one; one edge (Merciful End) needed three separate nerfs (025, 048, 049), the standing warning that pair-gate edges are the live balance surface.
- W3 damper + curse: damper state persists server-side across rejoin (Gungeon magnificence reset to 0 on save/exit between floors was the seam, later recalculated on load); discount vendors priced below the marginal drop gain (Cursula's 50% off at +2.5 curse made curse 9 a stable farming plateau); the negative-curse cleanse paying 5 money per point converts a risk stat into income, so audit that conversion; the `[11]` steal-odds triplet (100/50/20) is carried without referent and must be specified before any steal mechanic ships.
- W4 pools + fork: identical odds on every entry path (Isaac teleport-in skipped the x0.25/x0.5 seen-decay); coin sinks walled from offer odds (10 donated coins bought +50% angel flip); par conversion for every alternative HP or currency (Bone Hearts paid half rate for the identical ladder); priced teleports into a track consume the same resource and the same decay; atomic commits on any lifetime meter (the force-quit method carried the donated total while restoring the machine, labeled cheating on the page itself); per-session jam valve on repeat conversion (Repentance curve: 10 coins 14.02%, 25 coins 61.53%); 999 cap with a 1000th-donation overflow reset and consolation; whitelisted clean-floor damage predicates (Repentance had to exempt spike damage post-launch).
- W5 map: path-repricing items get a generator invariant (charge cap 3, floor cap at two-thirds act depth, asserted when the map is built; the Wing Boots spawn-filter leaked and needed WP50 plus a WP51 bugfix); off-map multi-fight events decrement the act's elite budget and declare which fights count as elite (the Dead Adventurer leak); seed wall day one: seeded or observer runs write zero unlock, ladder, and leaderboard state (StS needed WP30, WP47, WP51, plus the Watcher unseeded and modded-character guards); double-boss finale timers and score checks run only after the final required kill (WP44). WP identifiers defined: WPn = Weekly Patch n in the StS fandom Ascension page's Update History, the series in which all these fixes shipped (rr-06).
- W6 pursuit: mastery ticks only on meaningful actions (FTL's documented farms: skill gain against harmless enemies, weapon-toggle XP with zero ammo, bombing your own ship, boarding repair loops); the pursuit clock advances every jump regardless of client state; the Clone Bay Combat clause is ambiguous in the source (W6 flag), so the lane writes its own floor (4.4) and names it new.
- W7 covenant: the mutator zero-progression law verbatim (W7); re-verify both [verify]-flagged merchant figures before pricing (itemized in W7: artifact base 160-220; Covenant-18 goods variant).
- W8 ledger: debt forgiveness on a cooldown (the vermin quest zeroed a 5,000g balance in one fight); the full vendor graph audited for positive cycles (G4).
- W9 banking: banking conversions rate-limited; the hex-edit family (bytes at 0x05 writing 200 Judge Blood) closes under invariant 1.
- W10 night: night pools and pity counters never reroll on rejoin or server-hop (Dredge fishing spots repopulated on save/reload until 1.5.1, quoted patch "Sorry!"; item dupe 1.5.2; anchor dupe 1.5.3).

### 5.3 Economy-engine patches (reskin families, deep-dive specifics)

- Clamp or integer math past 1e15 and record the cap hit as content; the naneinf 1.8e308 overflow and the LbaL 9.9e247 coin crash are the proof cases `[03]`, `[04]`, `[09]`.
- Server-authoritative slot ledger: every generated copy consumes a slot or counts against a per-player off-ledger ceiling; the Perkeo chain quantified at 566 Plutos and an 89-King hand generated off-ledger (rr-04).
- Duplicated boons inherit degraded editions; exact-Negative copies stripped (Balatro 0.9.3L did exactly this to Invisible Joker and Ankh); lease or decay duplicates with the rental ($3/round) and perishable (5 rounds) grammar (rr-03, rr-04).
- Persist purchases atomically server-side before discovery credit (the reload-cancel dupe-of-record on joker discovery).
- Rotate deterministic draft orders per season so a leaked seed spoils nothing (packs are seed-deterministic in Balatro; seeded runs stopped counting in 0.9.0q).
- Snapshot interest at one fixed point in the round pipeline (Balatro had to spell out which end-of-round payers count).
- Pool-exhaustion fallback plus a sanctioned unlock-all valve that disables achievements (both proven in the original).
- Vendor anti-arbitrage (rr-24): par refund pays min(purchase, value); on-sell-trigger items sell for 0; currency-bank storage items depreciate on a schedule with yield under the income drip (the Bazaar equilibrium after four Chunk of Gold nerfs); premium buyers capped below any value-gain rate; reroll discounts capped (the Arbitrage cap: 3 off a Diamond's 8); refresh control as a priced consumable, with the Hearthstone Battlegrounds freeze as the only sourced carry-over if playtests demand it.
- Vendor cycle law, worked and reconciled (G4). The Hades broker loop, carried verbatim from the retention synthesis quoting `[02]`: "1 Titan Blood to 200 gemstones to 20 keys, then 15 keys back to 1 Titan Blood plus 5 keys, net +5 keys per cycle". Reconciliation against R3's standard chain (1 titan blood = 1,000 gemstones = 100 keys, composition verified by script this session): leg 1 sells 1 titan blood for 200 gemstones, an 80% undercut of the standard 1,000; leg 2 converts 200 gemstones to 20 keys at the standard 10-per-key rate; leg 3 buys 1 titan blood for 15 keys, an 85% undercut of the standard 100. Both discounts sit inside the carried "limited deals undercut 50-85%" band `[02]`, and the loop closes only because two limited deals bracket one standard leg. This is the proof case for the law: any limited deal must be priced against the full composed standard chain, never against the adjacent hop alone. Same family: Loop Hero Mountain Peak Oblivion-refarm and Treasury adjacency printer; rate-limit repeatable formation and turn-in payouts per run; pay retreat banking only at the designated safe tile with an enemies-alive check.
- Idle and stall (G2, Family C): the war countdown advances independent of player state; payouts land on completion; low-intensity stalls trigger escalation; Dome Keeper's own patch arc ("the countdown to the next wave will start even if you keep sitting in the station", v4.0.x); VS's documented AFK tier at roughly 5 billion gold in 7 hours bounded only by engine lag near 180 chests; White Hand as the deterministic session ender pattern ("It is impossible to kill or stall White Hand."); cap any stat that divides spawn interval (VS curse is the root cause); keep VM taps pickup-gated and daily-capped (the candy cap already landed, verified this session at `OssuaryZone.luau:241`); cap the rebirth multiplier.
- Copy and stack engines (G3, Family D): iteration cap 99 on every trigger chain (Cobalt Core's hard-coded stop); ceilings on every stack; Peglin's 999 per-peg cap; Astronarch's cost floor 10; when an engine is discovered, Landlord-style fine-print taxation in place while leaving the combo standing (Cultist base payout cut to 0; Dwarf taxed through Landlord fine print: 2.5x rarity suppression, +1 reroll cost, +1 removal cost, one fewer symbol choice).
- Threat and clock (rr-10): forced ending on the faction war (Eclipse removed exits; the wiki concedes "Item scaling outpaces enemy scaling over time"); scope every clock pause zone-wise (the Void Fields saga took four patches); apply any income tax to all faucets at once (Eclipse 6 missed barrels, Ghor's Tome, Brittle Crown); cap repeatable payout triggers doll-style (the 3-doll cap exists because the loop "would escalate to the point where there would be enough dolls and on-kill effects to overload and crash the game"); too-cheap third condition in any AI budget spender; hard-cap effective coeff (combat 99; boss formula (1 + coeff/2.5) x sqrt(livingPlayers) beyond it; explicit endless mode only past that).
- Drawback boons: type every drawback against every modifier before shipping (Transcendence voided 3 of 8 Eclipse rungs from one shop slot); price drawbacks by expected session duration (Spinel Tonic downsides "rarely matter" on short runs).
- Rejoin idempotence (G8, Family B): Dome Keeper gadget dupe on save/reload (fixed v2.3.1); Dredge spot repopulation and dupes (1.5.1-1.5.3); Monster Train Logbook artifact retrigger while paused; Bazaar pre-level-up pool rigging removed in beta; Wildfrost autosave reroll window (backing out before the event completes rerolls for free).
- Client gates (G1, Family A): ITB shipped a dev console ("xp 25", "unlock all", "makeitso"); Monster Train metagameSave.json ("maxAscensionLevel": 26); HoloCure plaintext save.dat with two public editors; ScourgeBringer hex guide; Peglin locked-class access via character select (fixed v0.9.15, quoted: "Removed exploit that made it possible to access locked classes via the character select screen"); StS killed seeded-run credit twice (WP47, WP51). The Roblox client UI is Peglin's character select screen.

### 5.4 Platform law (Family J)

Published odds on every paid random surface; a consolation track on every outcome; the slot-machine framing audited against the Roblox Community Standards before theme lock. Compliance basis, stated once: the requirements are carried secondhand from the Community Standards page the `[09]` digger read; the current paid-random-item disclosure policy is a distinct Roblox page that no one in this chain has fetched, and it remains the gate on any pull mechanic shipping.

### 5.5 Family K: paid failure and organized losing (new in revision 2)

The spec pays players for losing in at least four places: W9 fail-forward banking, R7 death ladders and lose-5-runs gates, the W1 assist dial, and 4.4's wipes-as-progression. Each needs a rate limit or anti-collusion rule, with precedents already in the material:

- Loss-gated unlocks pay once per account per gate, ever (the gates are lifetime counters, so a throw syndicate farming "lose 5 runs" gains the one unlock and then nothing further; Slice & Dice's ladder is lifetime-cumulative by construction `[22]`, and its own community treats death-farming as "the common route" `[22]`, the warning that the payoff must stay one-shot).
- Wipe banking (W9) converts at the knockout rate with a per-player per-war cap and an engagement floor (minimum contribution score in the losing run), so idling into deaths banks nothing.
- The assist dial is personal, decays on wins (4.0), and pays zero VM, so a faction tanking early wars buys tempo for its members while handing the opponent faction score and faucets; Hades stores God Mode records separately `[01]`, the precedent for quarantining assisted state from competitive records.
- Death-ladder thresholds count only deaths inside sanctioned war runs, never private or mutated configs (the W7 mutator law already zeroes those).
- Anti-syndicate: DRTC's dodge patterns are the model of what to forbid; the finding documents mass-recruit churn and penalty-floor immunities as the exploit family `[19]`, closed by join-time party costs, inherited party state, zero floor-immune members (invariant 9).

## 6. CLOSED BIBLIOGRAPHY

### 6.1 The 30-finding legend (reproduced from the mechanics synthesis; these are the pages each finding's digger fetched and read)

- `[01]` Hades duos/heat: hades.fandom.com Duo_Boons, Pact_of_Punishment, Boons, Patch_025 (wikitext via api.php).
- `[02]` Hades keepsakes/gifts: hades.fandom.com Keepsakes, Nectar, Ambrosia, Companions, Bouldy, Bouldy/Boons, Wretched_Broker (api.php).
- `[03]` Balatro jokers/antes: balatrowiki.org Blinds_and_Antes, Shop, Money, Jokers, Legendary_Jokers, Guide:_naneinf, Updates, Hands, Discards, Hand_size.
- `[04]` Balatro spectral: balatrowiki.org The_Shop, Spectral_cards, Booster_Packs, Rarity, Money, Interest, Perkeo.
- `[05]` StS relics/ascension: slay-the-spire.fandom.com Ascension, Relics, Shop, Dead_Branch, Corruption, Sundial, Ice_Cream (Wayback snapshots).
- `[06]` StS map: slay-the-spire.fandom.com Elites, Map_locations, Ascension, Wing_Boots, Act_4 (api.php); slaythespire.wiki.gg Map_Generation; Steam guide 2830078257; Justin Gary Design show notes.
- `[07]` Dead Cells: deadcells.wiki.gg Cells, Blueprint, Boss_Stem_Cells, Collector, Hunter%27s_Grenade, Blacksmith, Mutations, Spartan_Sandals, Gear, Weapons.
- `[08]` Vampire Survivors: fandom PowerUps, Level_up, Evolution, Treasure_Chest, Whip, Bloody_Tear, Golden_Egg, Gold_Coin_(currency), Greed, Luck, Experience_Gem (api.php); vampire.survivors.wiki Guide:Gold_farming; Steam guide 2927997156; Steam discussion.
- `[09]` Luck be a Landlord: luck-be-a-landlord.fandom.com Rent, Slot_Machine, Symbols, Items, Reroll/Removal/Essence_Tokens, Emails, Dud, Floors, Landlord, Coins, Cultist, Dwarf, Coin, List_of_Patch_Notes (api.php); Steam store page; Wikipedia; about.roblox.com/community-standards.
- `[10]` Risk of Rain 2: riskofrain2.wiki.gg raw wikitext Difficulty, Lunar_Coins, Bazaar_Between_Time, Shaped_Glass, Newt_Altars, Eclipse.
- `[11]` Enter the Gungeon: enterthegungeon.wiki.gg Magnificence, Curse, Shops, Chests, Lord_of_the_Jammed, The_Jammed, Quality, Items; fandom Curse.
- `[12]` Noita: noita.wiki.gg Wand, Wands, Spells, Wand_and_Spell_Tiers, Holy_Mountain, Unlocks, Guide_To_Wand_Mechanics, Guide:_Rapid-Fire_Wands, Expert_Guide:_Draw, Chainsaw.
- `[13]` Isaac: bindingofisaacrebirth.fandom.com Devil_Room, Angel_Room, Item_pool (web reader full text).
- `[14]` Loop Hero: loophero.fandom.com api.php Synergy, Campfire_(tile), Meadow, Rock, Mountain, Treasury, Village, River, Gymnasium, Field_Kitchen, Materials, The_Hero; IGN Risk_Vs._Reward.
- `[15]` Peglin: peglin.wiki.gg api.php Shop, Peg, Peglin, Cruciball, Gold, Refresh_Peg, Critical_Peg, Coin_Peg, Fight, Encounters, 0.9.15, orbs, relic pages, category counts.
- `[16]` Dome Keeper: domekeeper.wiki.gg Relic_Hunt (raw), Version_History, Minerals, Enemies, Laser_Dome, Engineer, Gadgets, Prestige, Keepers, Domes.
- `[17]` Astronarch: astronarch.fandom.com api.php Keywords, item and hero pages, full allpages/search sweeps; Steam guides 2395108692 and 2395485613; Steam store page; pullpush.io archived thread.
- `[18]` HoloCure: holocure.fandom.com Character_Gacha, Collab; holocure.wiki.gg Character_Gacha, Collab, Super_Collab, HoloCoins; GitHub save-editor READMEs (aclich, nnotwen).
- `[19]` Death Road to Canada: deathroadtocanada.fandom.com Stats, Zombo_Points, Food/Resources, Always_Be_Looting, Unomey, Cool_It/Despair_Events, Zombo_Town, Personality; Steam tips thread.
- `[20]` FTL: ftl.fandom.com Crew_skills, Rewards, The_Kestrel_Cruiser, Rebel_Fleet, Beacons, Stores_and_resources, Achievements, Ship_Achievements, Sectors.
- `[21]` Into the Breach: intothebreach.fandom.com Pilots, Squads, Reset_Turn, Corporate_Reputation, Achievements, Skills, Islands, Missions, Vek, Cheat_Codes, Difficulty (webReader + api.php); Steam guide 1386007005.
- `[22]` Slice & Dice: slice-and-dice.fandom.com api.php Achievement, Special_Interactions, Curses, Blessings, difficulty pages, keyword and item pages; Steam guide 3234507089; Google Play listing; tann.itch.io.
- `[23]` Monster Train: monster-train.fandom.com Covenant_Ranks, Battle, Pyre, Gold, Ember, Merchants, Monster_Train, Awoken, Hellhorned, Champions, Version_History, Mutators, Daily_Challenge, Expert_Challenges, Save_File_Editing, Gifts_for_a_Guard, Imp-portant_Work.
- `[24]` The Bazaar: official patch notes (playthebazaar-cdn.azureedge.net PatchNotes.html), Steam news RSS app 1617400, thebazaar.wiki.gg api.php (Day, Merchants, Curio, Bar_of_Gold, version pages), thebazaar.fandom.com beta pages, Steam guide 3573365196.
- `[25]` Wildfrost: wildfrostwiki.com Charms, Counter, Charm_Merchant, Woolly_Snail, Blings, Icebreaker_Cabin, Daily_Voyage, Snowdwell, Version_History; Steam news API app 1811990; Steam Jimbo thread; dood.gg ja guides; problemmachine review.
- `[26]` UnderMine: undermine.wiki.gg Curse, Shop_Keeper, Pilfer_Shop, Altar, Red_Shop_Keeper, Absolution, Twisted_Blade, Aphotic_Charm, Cursed_Chest, Pilfer_Credit_Card(_Gold), Debt, Upgrade, Tariffs, Inflation, Loyalty; dev blog; Steam thread.
- `[27]` ScourgeBringer: scourgebringer.fandom.com api.php Blessings, Skills_tree, Achievements, The_Roots_of_Chaos, Realms; Neoseeker Map_Explained, Altar_of_Blood_Blessings, The_Chiming_Tree_Skills; Steam guides 2393177785, 2973377604, 3437594361, 2081785829, 3184125372, 2832183532; metagame.guide.
- `[28]` Dredge: dredge.wiki.gg Panic, Aberrations, Time, Lights, Rods, Engines, Updates, Fish, Shipwright, Dry_Dock; strategywiki.org DREDGE/Panic.
- `[29]` Cobalt Core: cobaltcore.wiki.gg api.php Mechanics, Status, Card_Traits, Guide_to_Infinite_Loops, Repair_Yard, Hardmode, Achievements, card and artifact pages, allpages index; Steam and publisher store pages.
- `[30]` Potion Craft: potion-craft.fandom.com api.php Haggling, Potions, Pricing, Tiers, Popularity, Talent_Points, Experience_and_levels, Alchemy_Map; Steam multiple-effects thread.

### 6.2 Deep-dive sources and session fetches

Deep-dive findings (page lists from their source fields):

- rr-01 Hades: hades.fandom.com api.php wikitext for Mirror_of_Night, Keepsakes, Duo_Boons, Boons, Pact_of_Punishment, Fated_List_of_Minor_Prophecies, God_Mode, Hell_Mode, Infernal_Arms, Stygian_Blade, Well_of_Charon, Eurydice, Patches index, Patch_041 through Patch_057; Steam discussion thread (curl, 15 comments); gamerant.com and hadesguides.com pact guides (WebFetch); videlais.com game log (checked, no telemetry).
- rr-03 Balatro jokers: balatrowiki.org /w/Poker_Hands, Planets, Vouchers, Stakes, Booster_Packs, Tags, Spectral_Cards, Unlocks, Decks, Challenges, Scoring, Blinds_and_Antes, Jokers, Seals, Enhancements, Guide:_naneinf, Collection (18 WebFetch reads); Steam store page 2379780.
- rr-04 Balatro spectral: balatrowiki.org /w/The_Shop, Booster_Packs, Jokers, Spectral_cards, The_Soul, Perkeo, Observatory, Blinds_and_Antes, Naneinf, Guide:_naneinf, Vouchers, Editions, Stakes, Unlockables, Collection, Decks, Challenge_Decks, Achievements, Interest, Money, Updates (oldids cited in the finding); api.steampowered.com GetNewsForApp appid 2379780.
- rr-06 StS: slay-the-spire.fandom.com api.php Ascension, Score, Merchant, Achievements, Custom_Mode, Daily_Challenge, Silent, Defect, Watcher, Ironclad; local first-pass files sts_elites_wikitext.json, sts_wingboots.json, sts_act4.json; slaythespire.wiki.gg Map_Generation, Ascension, Relics, Ironclad, Silent; steamcommunity.com/stats/646570/achievements (curl + parse, 46 rows); steamcharts.com/app/646570; megacrit.com (checked, no sales figures).
- rr-08 VS: vampire-survivors.fandom.com api.php PowerUps, Level_up, Achievements, Characters, Imelda_Belpaese, Poe_Ratcho, Stages, Weapons, Weapons/Overview_Stats, Evolution, The_Reaper, White_Hand, Merchant, Eggman, Moongolow, Curse, Big_Trouser, Golden_Egg, Version_History; vampire.survivors.wiki Guide:Gold_farming; Steam guide 2927997156; Steam discussion 3473981814943934463; repo reads (digger-run): roblox/src/server/LedgerExchange.luau, roblox/src/server/OssuaryZone.luau, roblox/src/server/MudBasecamp.luau, roblox/docs/SEASONAL_LAUNCH.md, roblox/README.md, memory/corpus/LINKS.jsonl LINKS-337; computations via the repo venv python.
- rr-10 RoR2: riskofrain2.wiki.gg ?action=raw Difficulty, Eclipse, Lunar_Coins, Prismatic_Trials, Teleporter, Transcendence, Void_Fields, Simulacrum, Bazaar_Between_Time, Brittle_Crown, Forgive_Me_Please, Directors, Artifacts, Chests, Challenges, Survivors, Items, Version_History; steamcharts.com/app/632360; computed tables via ./.venv/Scripts/python.exe.
- rr-13 Isaac: bindingofisaacrebirth.fandom.com Devil_Room_(Item_Pool), Sacrifice_Room, Item_Quality, Angel_Room_(Item_Pool), Donation_Machine (web reader, full articles); first-pass pages (Devil_Room, Angel_Room, Item_pool) carried in the ask.
- rr-24 Bazaar: playthebazaar-cdn.azureedge.net/thebazaar/PatchNotes.html (curl, HTTP 200, 504,891 bytes); store.steampowered.com/feeds/news/app/1617400 (curl, 319,005 bytes, May 2026 through Sep 2026 patches); thebazaar.wiki.gg api.php (22 pages incl. Merchants, Day, Level_Up, Start_of_Run, Freeze, Bar_of_Gold, Chunk_of_Gold, plus action=cargoquery 636 item rows); steamcommunity.com guide 3573365196; thebazaar.fandom.com api.php (1.0.1781, closed-beta notes); hearthstone.fandom.com api.php (Battlegrounds Freeze + Recruit Phase); mobalytics.gg beginner guide (webReader); playthebazaar.com/faq (HTTP 200, Blazor WASM shell, no server text). Failed routes: forums.playthebazaar.com (DNS), Reddit .json (HTTP 403).

Session fetches run by me in this revision:

- `https://hades.fandom.com/api.php?action=parse&page=Pact_of_Punishment&format=json&prop=wikitext` via curl, HTTP OK, 15,947 bytes, scratch `C:/Users/foste/AppData/Local/Temp/hades_pact.json`. Yielded verbatim effect text for Middle Management, Underworld Customs, Personal Liability, Benefits Package, Forced Overtime, Tight Deadline (W1).
- `https://bindingofisaacrebirth.fandom.com/api.php?action=parse&page=Item_Quality&format=json&prop=wikitext` via curl with custom UA `mag-research-harness/1.0 (foste; local research)`, 1,200 bytes, scratch `C:/Users/foste/AppData/Local/Temp/isaac_quality.json`. Current wikitext confirms the 0-4 quality range and that qualities are defined in items_metadata.xml; it carries no item census and no tier table, so the 410-vs-430 conflict stays quarantined (3.3).
- WebFetch attempts on `hades.fandom.com/wiki/Middle_Management` and `bindingofisaacrebirth.fandom.com/wiki/Item_Quality` returned HTTP 403 both times; the api.php curl route is the working path on these domains, matching the diggers' experience.

Session repo reads (converting carried rr-08 citations into direct verification):

- `roblox/src/server/LedgerExchange.luau:261-280` (tick loop, 10s cadence, `income * (1.5 ^ Rebirths)` at :276), `:285` (VirtueMarks start 100).
- `roblox/src/server/OssuaryZone.luau:33` (FLOORS = 3), `:241` (CANDY_PER_FLOOR_DAILY_CAP = 6), `:236-240` (comment: max 12 VM/floor/day, 36/day, 72 with doubler).
- `roblox/docs/SEASONAL_LAUNCH.md:131-136` (falsifier line and the landed-cap note).

### 6.3 Owed ledger (unfetched or unverified; nothing above rests on these)

- Clone-census residual: the ask states 10 clone verdicts across 30 findings; the material handed to me names at most 9 clone games (Hades, Gungeon, Isaac, StS, FTL, Monster Train, UnderMine, ScourgeBringer, Dredge); per-finding verdict fields were summarized, never enumerated, so the 10th clone finding's identity is unknown and unstated anywhere in this spec.
- Isaac item census: 410 stated vs tier sum 430 (3.3); resolution needs the rendered Item_Quality table or items_metadata.xml; my session fetch of the current wikitext carries neither number.
- Roblox paid-random-item disclosure policy text, owed from `[18]` / `[09]`; verify before any pull mechanic ships. The Community Standards page itself was read by the `[09]` digger; the two documents are distinct.
- `[11]` steal-odds triplet (100/50/20): carried from the finding's lane note; referent unspecified in the ask; specify before any steal mechanic ships.
- Clone Bay Combat clause: flat 1 point vs 20% capped at 1, unresolved in `[20]`.
- Community threads unreachable on every route in `[05]`, `[06]`, `[07]`, `[11]`, `[16]`, `[23]`, `[29]`, `[30]`, and re-blocked in the deep-dives (Reddit 403 or empty 200, Steam discussions partial); Dead Cells save-scumming stays community-reported; VS idle-check cadence figures were search-snippet-only and excluded; the VS community curse sweet-spot figure stays unverified.
- Hades: official supergiantgames.com patch pages 404 (all post-1.0 patch lines are wiki mirrors); base duo offer weight unpublished; boon rarity roll formula "currently unsolved"; per-god Pom level curves unfetched; Hades II unread.
- Balatro: raw internal rarity integers never found (rr-04 retried GitHub code search, gh CLI, grep.app; all blocked); buffoon/spectral pack internal rarity odds owed; Red/Black/Blue/Orange/Gold per-ante chip tables absent from pages read; balatro.fandom.com 403 on both passes; behavioral telemetry (run length, DAU) absent, so retention statements are structure-derived.
- StS: decompiled mapgen writeup unlocated (only a Poisson-disk approximation repo and a 2021 DiVA thesis surfaced); Mega Crit sales milestone pages carry no figures; per-act A2/A3/A4/A7/A8/A9 multipliers live on unread enemy pages; achievement percentages include dormant owners.
- RoR2: official Hopoo/Gearbox patch notes unfetched (the Version_History page renders server-side and read empty); steamcharts figures are single-extraction; player XP curve unfetched; code constants (0.0506, 1.15, 1.25, portal 0.375-then-0.05) are wiki-transcribed.
- Vampire Survivors: pre-0.7.2 multiplicative fee formula unfetched; DLC unlock pages unfetched; Collection denominator unfetched; support weapons lack rows in the stats table.
- The Bazaar: forums DNS failure; Reddit 403; FAQ body requires executing the app; live 2026 client values unverified; two wiki-vs-patch conflicts flagged in 3.3.
- Potion Craft: base prices verified for 3 of 41 effects.
- Relay limits of this document: the 30-legend page lists in 6.1 are titles under domains, carried from the ask; the deep-dive rows record the routes their findings actually used; only the fetches and repo reads listed in 6.2 (session rows) were verified by me directly. The lane's boon-draft, faction-lobby, and Pilgrim-class surfaces remain asserted by the findings' verdict reasoning; no file naming them was opened this session.
- Telemetry: no behavioral retention data (DAU, D1/D7/D30, session length) exists in any source read; every retention statement above is structure-derived from unlock ladders and patch cadences, labeled as such by the diggers who wrote it; targets and kill criteria are operator decisions (4.1a).

## CLOSING INSTRUMENT NOTE (revision 2)

Carried material: all finding-tagged numbers and all quotations trace to the ask's finding set, whose evidence fields record the original fetches. Session work in this revision: (1) two page fetches via curl on api.php routes (Hades Pact_of_Punishment, 15,947 bytes; Isaac Item_Quality, 1,200 bytes; scratch paths in 6.2) plus two WebFetch attempts that returned HTTP 403; (2) three repo file reads at the cited lines (`LedgerExchange.luau`, `OssuaryZone.luau`, `SEASONAL_LAUNCH.md`); (3) one python arithmetic battery (heat sum 63/64; RoR2 52.7 min, kills 5.7/10.1/13.3, decay 2.34; broker composition 1,000 gemstones / 100 keys; Isaac tier sum 430; chase rates 5.6/32.7/138.9/1,851.9 days); (4) one dash byte scan on this document, run with the repo venv python: bytes 87491, U+2014: 0, U+2013: 0, U+2012: 0, U+2015: 0. The mcp web reader was used once on the Isaac Item_Quality page and returned a partial extraction whose table section read empty; the curl api.php route is the session's authoritative fetch for that page.
