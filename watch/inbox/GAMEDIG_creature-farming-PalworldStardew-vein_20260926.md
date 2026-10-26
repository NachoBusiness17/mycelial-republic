# GAME DIG WHEEL SPEC (creature-farming-PalworldStardew-vein, 30-game dig receipt, 2026-09-26)

# Creature-farming wheel spec (Palworld x Stardew vein), assembled, rev 2

Revision note: this revision responds to a cold-read defect list. Fixes are inline; every fix is grounded in the payload, in arithmetic done during this revision without a machine (worked rows shown so any reader can re-verify), or in an explicitly marked assembler decision. Where a defect required data nobody holds (re-fetches, operator calls), the item moved to 5.4 or 0.3 and the document says so.

## 0. Provenance, method, count hygiene

Assembled by the assembler seat from three inputs handed over in one ask: the MECHANICS wheel spec, the RETENTION AND ABUSE section, and 8 deep-dive findings delivered as structured payloads (ac-stalk-market, digger-cf-06, cf-02, digger-cf-04, digger-cf-13, gk-corpse-quality-processing, digger-cf-05, cf-08). This seat fetched zero pages and ran zero commands in the first pass; the revision pass ran arithmetic checks by hand only (each one shows its worked rows; none ran as a machine command). Every number and quote below is as the finding recorded it. Quote fidelity rests on the digger sessions' own fetch records; where this document quotes a source line, the quote is relayed from the finding that fetched and read it, cited as (quoted in [id]). Verdicts (clone, reskin, skip) are the diggers' and are preserved as filed. Every finding's unresolved items are carried in 5.4 and are placeholders for a builder, never sourced constants.

ID alias law: the RETENTION index uses cf-06 and cf-07 for the same findings the deep-dive payload and MECHANICS call digger-cf-06 and digger-cf-07. This document standardizes on digger-cf-06 and digger-cf-07 in the body; the registry in section 6 keeps the index's original labels with the alias noted there.

Count hygiene across the inputs: MECHANICS states 30 findings (14 clone verdicts, 16 reskin verdicts); RETENTION states 29 and its index table lists 29 rows; the union is 30 findings because the RETENTION index omits gk-corpse-quality-processing, which RETENTION covers in body text and the deep-dive payload delivers with a clone verdict. The tallies reconcile at 30 findings: 14 clone, 16 reskin.

Provenance marking law: rows and parameters traceable to the payload carry a finding id. Assembler inference (integration assignments, parameter proposals, the clock model, the MVP cut) carries the tag (assembler) and is a proposal for the operator, never a sourced constant. This marking applies throughout, including section 4.

### 0.1 The game this spec describes (grounded frame)

- Platform and authority: a server-authoritative Roblox stack. Source: the digger-cf-13 deep dive's ask-provided lane context states the target as "a server-authoritative Roblox stack"; the Kynseed design edit in the payload says "compress the 18-year heir gate to a same-session or few-session cycle for Roblox pace". This is the only platform signal in the payload.
- Product shape: a persistent multiplayer creature-farming and life-sim economy built on four lane systems (VM currency, boon drafts, faction war, Pilgrim class), driven by the wheel defined next. There is no combat-design payload in this document; combat arrives only as gate events, star scoring, and the war window, and its design is a separate spec.
- The wheel, defined: the five-cadence loop the MECHANICS basis table organizes everything around. Session (per login), Daily (one server day), Weekly (7 server days), Season (28 server days), and Lineage (breeding) plus Generation (rebirth). Every mechanic in sections 1 to 3 hangs off exactly one primary cadence; the integration map in section 4 is that assignment.

### 0.2 The clock model (assembler decision; the inputs conflict and this resolves them)

1. All clocks are server-day counters advanced by play. Zero real-time dependencies. Consequence: the time-travel crack class ACNH shipped is structurally impossible on this clock; the 1.2.0a server-side regeneration rule is kept anyway as defense in depth.
2. 1 server day is the base tick. 1 week = 7 server days. 1 season = 28 server days. 1 year = 4 seasons = 112 server days.
3. Annual definition: the Portia rep reset and the annual ceremony land on each year boundary (every 112 server days). Rank persists across resets.
4. War, reconciled: the two inputs used "war window" at two granularities. This spec fixes it: the faction war campaign runs one season (28 days); a war window is the weekly scoring checkpoint inside it (4 checkpoints per campaign, final tally at day 28). The 1.4-row phrase "28-day faction war windows" refers to the campaign; the cadence-spine phrase "the war window" refers to the checkpoint.
5. Turnip cycle: 1 week, 12 sell periods (2 per server day), rot at the next day 7. Source day names (Sunday buy, Friday municipals) are kept as position labels inside the 7-day week.
6. Source clocks (Graveyard Keeper 7.5-minute days, Frostpunk hour cooldowns, RimWorld days, ACNH real weeks, Palworld real-hour incubation) are session-length evidence about pacing, never adopted constants. Palworld's incubation formula carries its structure; its 72-hour constant is a re-roll dial (the formula and worked outputs are in 1.1).

### 0.3 Decisions owed to the operator (no source in the payload covers these)

| Decision | Status | Assembler proposal (unbacked, adopt or replace) |
|---|---|---|
| Session length target | owed | 25 to 40 minutes median, sized so a gordo-class payout fits one session (the fit-to-session law is sourced, digger-cf-07; the minutes are proposal) |
| Player count / server model | owed | Single shared server per faction cluster, 20 to 50 concurrent per instance (proposal) |
| Win and loss states | owed | No terminal win state. Recurring peaks: season close (faction scoreboard), year close (ceremony), personal ladder tops. Loss is always soft (wither, crash, decay, strike), never character deletion (proposal, consistent with every sourced catch-up band) |
| Content policy for corpse and creature-harm reskins | owed, REQUIRED | GK's chain ports as quality scoring with care-shaped verbs (see 1.7 adaptation note); "sweatshop" language in 5.1 item 11 is dig vocabulary for an abuse pattern, and the lane's own framing is worker care. Operator sign-off required against current Roblox content rules before either system ships |
| Aggregate server budget for the 5.2 invariant stack | owed | The stack is per-row counters plus daily passes (per-system notes exist: one volume counter per SKU plus a daily decay pass, digger-cf-06). No aggregate estimate exists in any source; engineering owes a budget before launch |
| Retention targets | owed | See 0.7 (proposals, unbacked) |
| Closed-economy faucet/sink totals | owed | Inventory exists (0.5 VM block); balancing pass is engineering work; laws 5.3.7 and 5.3.8 are the only sourced stabilizers |
| Fork tuning (friendly vs hardcore) | owed | Keep the pre-commitment seam, per the digger-cf-04 reading (proposal) |

### 0.4 Scope cut: core vs optional, MVP build order (assembler proposal)

| Phase | Ships | Mechanics (finding) | 5.2 invariants live from |
|---|---|---|---|
| M0 vertical slice | The daily loop | Capture formula (cf-19), luck scalar (digger-cf-05), commission board + ranks (digger-cf-13 subset), market ledger with visible saturation (digger-cf-06), season clock + published ROI table (digger-cf-03) | 1, 2, 3, 5 (protections precede features) |
| M1 | The collection loop | Breeding core on the Temtem fertility rules (digger-cf-21; the Palworld payout table stays quarantined per 1.1), pity + hatch-near-best (digger-cf-26), licence ladder (digger-cf-24), daily-cap stack (cf-23), stock-scarcity depot (cf-29), grove rally (cf-28) | 4, 7, 9 |
| M2 | The war and care loop | Gate ladders + vendor rows (cf-18, cf-08, tinkertown), corpse-quality station (gk, content-reskinned per 0.3), labor + care (digger-cf-01), turnip weekly per faction (ac-stalk-market), alignment fork (digger-cf-04) | 6, 8, 10 |
| M3 | The long arcs | Rebirth ladder (kynseed), hope/morale meter (digger-cf-14, digger-cf-15), mastery band (cf-20), gene counters (cf-22), cap-raise events (gk), skill pools (digger-cf-25), settler compounding (digger-cf-12), gordo chokepoints (digger-cf-07), infinite tail (digger-cf-10) | all, audited |

Core means the M0 and M1 rows. Everything else is additive. The Factorio-shaped charge ceiling ships only if hub logistics exist as a system; the skip note in section 3 otherwise governs.

### 0.5 The four lane pillars, specified (parameter blocks are assembler proposals; shapes cite their findings)

**Boon drafts.** Draft = 3 offers from a weighted pool of 10 or more (number proposed; shape precedents: Niche's 2-slot draft at 50% application per pick, cf-22; Palworld's 1-to-4 pick inherit, cf-02). Timing: 1 free draft per server day; further drafts cost VM priced at 10x that day's median board payout (proposed; day-gate precedent cf-23). Reroll: 1 per draft at the same cost, consumed server-side before display (5.2.1). Pity weighting toward uncollected outcomes (shape, digger-cf-26). Fertility burn: each completed chain burns 1 fertility from both parents, child inherits the lower remaining, cap 8 (digger-cf-21, clone). Faction-scale drafts charge shared morale on reskinned Frostpunk cooldowns 18/36/45/72 hours mapped to 1/2/3/5 server days (mapping proposed, digger-cf-14). Stacked-speed multipliers capped (cf-02 law). Relief actions carry per-source diminishing returns (5.1.9).

**Faction war.** Win condition: highest cumulative star points at season close; 2,000 points per star, hidden 6th star above 12,000 as the stretch ceiling (shape, digger-cf-26). 4 weekly checkpoints per 28-day campaign (0.2). Score resets each year, earned rank persists; season-close payouts reskinned from the Portia monthly mails 10,000 / 7,000 / 4,000 (digger-cf-13). Rival pacing: the rival faction starts each year at a published head start (Higgins 5,250 shape) on a published daily gain (digger-cf-13). Kill-to-unlock ratchet mints resource tiers and vendor rows on named kills; re-fights cost keys with cooldowns (cf-18, cf-08, tinkertown). Star tier scales rare-drop odds 20 to 100% (digger-cf-26). Market layer: one turnip seed per faction; cross-faction selling allowed only through owned queue tooling with a sell-side fee or a volume cap (ac-stalk-market patch list; this bound is load-bearing everywhere cross-faction selling appears).

**VM currency.** Faucets (sourced): board payouts (1.9), market sales (1.5), turnip sales (1.6), star-scaled gold bonus 100 to 175% (1.3), licence commerce rates +5/10/15% (1.9). Sinks (sourced): cake economy and incubation gear (1.1), medicine ladder 780 / 1,820 / 3,120 (1.8), licence tiers 250 to 9,000 (1.9), the paid fork's 135,000 to 500,000 shape (1.9), condensation 4/8/12/24 (1.1), respec 300 (1.3), boss idols (1.11), aging infrastructure (1.13). Stabilizers (sourced): geometric volume decay self-heals (1.5); per-faction ledgers bound dumps; the unlock currency is insulated (5.1.3). Owed: closed-economy balancing (0.3).

**Pilgrim class, assembled (assembler synthesis of six mechanics the payload assigns to it).** A Pilgrim is a shared-respawn identity with one body, one base, one bar, one ladder. The body is the capture instrument: a sleeping Pilgrim auto-fails the attempt, and success costs 5% MaxHP + 1 (cf-19). The base runs under the attendance law: assigned workers produce while the player does anything else, decay and care price neglect, upkeep resists purchase (digger-cf-01). The station turns every delivered unit into a fresh quality puzzle against a budget the player already understands (gk). The morale bar is shared and visible, with threshold bands 35/20/5% and a catharsis valve so a bad night never deletes progress (digger-cf-15). The draft is metered against that bar (digger-cf-14). The luck carries: the Pilgrim's charm drags the faction average up, visibly attributed (digger-cf-05). Death is a scheduled promotion: the contract guarantees the handoff, talents exist only through inheritance, the heir gate is compressed to a few sessions, and loss pressure rides the handoff (kynseed, with the digger's two design edits). A session reads: check the fortune, run the station, claim the board, pay the care, draft or breed with what the day paid.

### 0.6 Retention claims discipline

Every "retention" sentence in this document is design rationale sourced from shipped games. The payload contains zero measured retention evidence and zero targets. The single in-source retention event (Temtem halved its whole loop "once retention data landed", digger-cf-21) cites no numbers. Proposed targets, unbacked: D1 return 40%+, D7 20%+, D30 8%+, median session 25 to 40 minutes. The operator owes real targets (0.3).

---

## 1. The wheel: cloned mechanics with their numbers

Verdict note: clone-verdict findings land here with their numbers. Two reskin findings (cf-02, digger-cf-06) carry tables strong enough to clone as-is and are flagged inline. Deep-dive enrichment is folded in. Known-bad constants are quarantined at the point of use and cross-listed in 5.4; they never lead a section.

### 1.1 Breeding core: the trait roll table [cf-02, reskin verdict, table clone-worthy; digger-cf-21, clone]

- The roll procedure (clone this part): pool both parents' passives, discard duplicates. Roll X in {1,2,3,4} at 40 / 30 / 20 / 10 percent; the child inherits X random picks from the pool. Roll Y on the same distribution; Y > X fills the gap with random wild passives. Expected X = 2.0 (finding's own computation).
- QUARANTINED TABLE, the clean-inherit payout. Published on the wiki: pool of 1 = 40%, 2 = 24%, 3 = 12%, 4 = 10%. The cf-02 deep dive recomputed two derivations of the wiki's own stated rules: derivation A (X >= n draws) gives 65 / 49 / 28 / 10; derivation B (X = n exactly) gives 16 / 21 / 18 / 10. All three tables disagree, and the two derivations disagree with each other. The true table is unknown. Build directive: implement the procedure above, parameterize the payout table, calibrate in-engine, and treat every row of all three tables as a candidate, never a constant.
- Species rule: hidden rank per species, 1 (rarest) to 1,500 (commonest). Child = eligible species nearest the parents' average, halves round up, tie goes to the lowest index. Hard ceiling: the child never exceeds the rarest parent. Sampled ranks verified by the finding on wiki.gg (2026-09-27): Bellanoir 1, Blazamut 10, Suzaku 50, Jetragon 90, Frostallion 120, Grizzbolt 200, Anubis 570, Cattiva 1460, Lamball 1470, Chikipi 1500. Ceiling quote: "you can never breed a Pal stronger/rarer than your strongest/rarest parent" (quoted in [cf-02]).
- Worked back-cross chain, quoted as recorded: (570+1460)/2 = 1015 Robinquill; (570+1015)/2 = 792.5 Croajiro 795; (570+795)/2 = 682.5 Univert 680; (570+680)/2 = 625 Omascul 630; (570+625)/2 = 597.5 Incineram 590. Finding-internal defect, flagged: the final step averages with 625 (Omascul's average) where the rule requires Omascul's rank 630; the rule-consistent step is (570+630)/2 = 600. The chain also exercises the nearest-species rule on unfetched ranks (597.5 to 590 rests on a species at 590 that the 10-sample list above cannot confirm; the full rank table was never fetched). Treat the chain's shape as the lesson (one rare catch back-crosses down the curve) and re-derive every step against a full rank table.
- Active-skill pass 50%. IVs 30% father / 30% mother / 40% random, per a community 100-egg test the wiki cites; the dedicated potentials page 404s, so this rides on the Breeding page quote only (5.4).
- Jackpots: mutation 1% base, 3% with the Extravagant Vegetable Cake; mutant package = different species outcome, always 4 passives with 2+ tier-4 including one mutation-exclusive (Babysitter, Heavily Armored, Idiosyncratic, Immortality, Skymarcher), Condensation Level 2, high potentials, always Alpha. Alpha 5%, independent of parents. Finding's odds math: mutation at 3% is one per 33.3 eggs; perfect one-parent IVs at (0.30)^3 = 2.7% is one per ~37 eggs; Alpha one per 20.
- Condensation: sacrifices 4 / 8 / 12 / 24 per rank, 48 total (1.0 cut this from 116); +5% Health/Attack/Defense per level to 20% at level 4; +1 work suitability per rank; a mutant equals rank 2, a 12-sacrifice head start.
- Cake economy: base Cake = 5 Flour + 8 Red Berries + 7 Milk + 8 Egg + 2 Honey, buy 6,300 / sell 630 (1.0 sell nerf from 1,000); cakes do not spoil in the Breeding Farm chest. Variants are spendable levers: Vegetable Cake doubles eggs per cycle, Special Cake raises pass-down, Extravagant raises mutation and IVs, Mushroom Cake raises IVs. Finding's workload math: 33 Extravagant rolls = 165,000 workload; 100 base-cake rolls = 200,000.
- Gates and pacing: Breeding Farm tier 19 plus a boss gate (defeat Lily and Lyleen); Egg Incubator tier 10 (tier-7 conflict flagged, 5.4); farm cap 20 eggs. Incubation, complete and implementable: Time = (Configuration 72 x 3600) / (Base Time x Incubation Speed), with Base Time Normal 12, Large 2, Huge 1 (divisors restored from the deep dive; the first revision's assembly dropped them) and Speed 1 / 1.5 / 2 at comfort 0 / 50 / 100%. Worked row: Normal at comfort 0 = 259,200 / (12 x 1) = 21,600 seconds = 6 h. Full outputs: Normal 6 / 4 / 3 h, Large 36 / 24 / 18 h, Huge 72 / 48 / 36 h. On the target clock these become day-fraction dials (0.2). Egg-cycle pacing conflict stands (Fandom "every 5 minutes" vs wiki.gg "base productivity modifiers", 5.4).
- Anti-printer history to copy: 0.1.5.1 fixed launch-window fixed-passive inheritance; 1.0 banned Tower Pals from special combos and locked top-of-curve species to same-species-only breeding. The loop-passive self-compounding vector (Philanthropist +100% breeding speed, breedable; Babysitter +30% egg and +30% incubation, mutation-exclusive) needs a stacked-speed cap (finding's law).
- Temtem extension [digger-cf-21, clone]: per-stat inheritance 40% higher parent / 40% average rounded up / 20% lower; shiny 1/2,000 base, x10 per shiny parent (1/200, 1/20); fertility cap 8, minus 1 per egg per parent, child inherits the lower parent's remaining value; wild catches pay fertility for 49-50 SVs (1-2 high stats = 7, 3-4 = 6, 5-6 = 5, 7 = 4); pair deposit 50, max 2 pairs, free cancel before the egg exists; forced-inheritance gear 500 single-stat / 2,500 dual-stat / 5,000 trait (all halved by patch 1.8), +1-SV item and trait-swap item each burn 1 fertility; market taxes 2% listing + 8% sale, egg listings expose parents and filter on min fertility; timers egg 5 min same line / 10 min cross-line, hatch 3-30 min by species, instant-hatch ticket; perfect-project bill 10 donors + 20 strands, about 30,000 currency of strands per 7x50 project.

### 1.2 Capture math: one visible formula [cf-19, clone]

RecordRate = (DamageBonus x HPBonus x LevelBonus x SpeciesRate x TapeRate x UpgradeBonus) / 10000, with:

- HPBonus = 1 - (2/3)(HP/MaxHP): 1/3 at full HP, near 1 at 1 HP.
- LevelBonus = (1/6) x (20/min(level,30) + 5): 0.944 at level 30+, 1 at 20, 4.167 at 1.
- SpeciesRate tiers 50 / 40 / 30 / 25 / 15 / 3 / 1; bootlegs record at floor(species/2) + 1.
- TapeRate: basic x1, chrome x3.5, elemental x4.5 on type match and x1.5 otherwise; two chase tapes skip the formula entirely.
- UpgradeBonus = (1 + mic/20) x (1 + mod/20), caps at 1.875x.
- Variant rates: wild 1/1,000; static encounters 2%; rogue fusion 1/50 (flood components 1/20); swarm 1/10; orb fusion 1/5.
- Attempt rules: the target holds at 1 HP during the attempt; success costs 5% MaxHP + 1 and locks re-recording; an asleep recorder auto-fails even a guaranteed tape. (Lane read, assembler: the Pilgrim body is the at-risk recorder.)
- Ladder: noticeboard track 15 / 50 / 100 / 120 / 150 / 150 materials; level 7+ repeats pay a chase tape + 2 non-common stickers; 10 materials rerolls the board.
- Guard from the dig: cap multiplicative refund stacking and soulbind the recycle stream (the AP-battery class, 5.1 item 6).

### 1.3 Loot gates: star rating + pity [digger-cf-26, clone]

| System | Value |
|---|---|
| Star cost | 2,000 points per star; 5 stars = 10,000; hidden 6th star above 12,000; theoretical max 15,000 (7,000 duration + 3,500 healthiness + 4,500 execution) |
| Rare loot by star 1-6 | 20 / 30 / 40 / 60 / 100 / 100% |
| Gold bonus by star | 100 / 110 / 120 / 130 / 150 / 175% |
| Egg roll | AS RECORDED, under-specified: "1/3 species, then 1/3 slot (2 loots + egg); an uncollected species doubles its egg share; all three uncollected = 1/6 egg / 1/12 loot, 50-50." The recorded text accounts for one quarter of the roll's mass in the all-uncollected case (1/6 + 1/12 = 1/4) and states no referent for the trailing "50-50". A builder can implement the pity direction (uncollected species weighted up) from this text and nothing more; the exact distribution needs the Monster_Eggs page re-fetched (5.4) |
| Hatch catch-up | lands within 3 levels of your best unit (best 1-3: same; 4-11: -1; 12-32: -2; 33+: -3) |
| Build economy | full respec 300; +1 skill point item 1,000, once per monster; cap level 42 = 42-point build budget |
| Combo | +5% damage per hit landed this round to the next monster in order, uncapped, resets each round |
| Shift fork | 25% of wild spawns are shifted; consecutive shifts alternate; Reward Box eggs 50% shifted |

Pity-weighted acquisition is the retention core: clean wins pull the collection toward complete, sloppy wins stall. 27 champions sit behind one-time 5-star gates with unlimited score-improving rematches. Dev-side patches the digger recorded: matchmaking now rates top-3 monsters plus average gear level (the low-level-backline deflation fix); the settled post-incident Shield Burst conversion value was unfound (5.4).

### 1.4 Season clock + crop ROI [digger-cf-03, clone]

- 28-day seasons, 4 per year. Out-of-season crops wither at rollover; fertilizer expires unless on a continuing multi-season tile.
- The formula, corrected during this revision. The finding recorded the simplified line: Min Gold per Day = ((Max Harvests x Sell Price per Harvest) - Seed Price) / Growing Days. Hand-checked arithmetic this revision shows the simplified divisor reproduces the non-regrower rows only (melon (250-80)/12 = 14.17; pumpkin (320-100)/13 = 16.92; starfruit (750-400)/13 = 26.92) and fails every regrower. The printed per-row values reproduce exactly under the completed divisor: Days = Grow Days + (Max Harvests - 1) x Regrow Days. Verification rows: strawberry day 1: 5 harvests (days 9, 13, 17, 21, 25), profit 5x120 - 100 = 500, days 8 + 4x4 = 24, 500/24 = 20.83; strawberry day 13: 2 harvests, 240 - 100 = 140, days 8 + 4 = 12, 140/12 = 11.67; blueberry: 4 harvests, 600 - 80 = 520, days 13 + 12 = 25, 520/25 = 20.8; hops: 17 harvests, 425 - 60 = 365, days 11 + 16 = 27, 365/27 = 13.52; cranberry: 5 harvests, 750 - 240 = 510, days 7 + 20 = 27, 510/27 = 18.89. Seven of eight rows reproduce exactly. The Ancient Fruit row is unverifiable from its recorded cells (the sell column carries "multi-season" with no number, and 57.14 is unexplained by the completed formula); owed (5.4). The completed divisor above is assembler arithmetic consistent with all fetched rows; a builder clones the table with that divisor and re-verifies against the page.

| Crop | Seed | Sell | Grow | Regrow | Gold/day |
|---|---|---|---|---|---|
| Strawberry | 100 | 120 | 8 | 4 | ~20.83 (planted day 1) / ~11.67 (planted day 13) |
| Blueberry | 80 | 50 x3 | 13 | 4 | ~20.8 |
| Hops | 60 | 25 | 11 | 1 | ~13.52 |
| Melon | 80 | 250 | 12 | none | ~14.17 |
| Cranberry | 240 | 75 x2 | 7 | 5 | ~18.89 (worked example on the page) |
| Pumpkin | 100 | 320 | 13 | none | ~16.92 |
| Ancient Fruit | 550 | multi-season, number not carried | 28 total | 7 | ~57.14 (unreproducible from the row, owed) |
| Starfruit | 400 | 750 | 13 | none | ~26.92 |

- Growth accelerators 10 / 25 / 33%, first harvest only on regrowers.
- Seed Maker: 1-3 same seeds at 97.51% (avg 2), 1.99% mixed, 0.5% jackpot seed; about 51% of harvests sacrificed sustains the seed line.
- Processing: wine 3x fruit base (6.25 days), juice 2.25x vegetable base (4 days); the keg beats the jar above 50g fruit base and 200g vegetable base.
- Appointment seed: one festival window per year (Spring 13, 9am-2pm) sells the best early crop.
- Law from the dig: publish the ROI table and price processed goods in it on day one, because players reorder an unpriced table within days.
- Shared-respawn caution the digger carried: wither must bind to owner responsibility, or a faction kills a harvest by inaction.

### 1.5 Commodity market crash [digger-cf-06, reskin verdict, table + curve clone-worthy]

SR1 volume ledger (fetched Plort Market page): price halved at or above the type's volume cap.

| Tier | Base price | Volume cap (units) |
|---|---|---|
| 1 | 7 | 40 |
| 2 | 15 | 30 |
| 3 | 30 | 20 |
| 4 | 40 | 15 |
| 5 | 50 | 12 |
| Jackpot | 200 | 50,000 (effectively crash-proof) |

- Volume decays 25% of previous value per day; day 1 starts at 50% of max. Midnight reroll: +/-30% per SKU plus +/-30% whole market; total band 49-169% of base in theory, 50-167% in practice. Worked scale: 10,000 units of a cap-30 good holds the halved floor about 20 days.
- SR2 deltas from the deep dive (same franchise, one fewer moving part): the hard cap is replaced by a saturation curve, 0-50% uses the uprate, 50-80% blends uprate to downrate, 80%+ uses the downrate; saturation decays 25% daily at midnight; daily noise is two rolls with amplitudes 0.3 and 0.4 multiplied together, and after day 10 the 0.4 amplitude is capped at -1.0. Counter-cyclical rule on the SR2 page: "If a player sells plorts during a day in which prices were raised, the prices will drop the next day, even if they do not exceed the maximum saturation value." (quoted in [digger-cf-06]).
- SR2 floor semantics, conflicted as recorded and quarantined: the page per the deep dive says both "When selling, plorts will be sold at approximately half price if saturation reaches 100%" and carries the worked floor "base 15, minimum 20, floor 17 after rounding" (midpoint reading). These cannot all hold: the midpoint of 15 and 20 is 17.5 (rounds to 17, matching the worked example), and half of 15 is 7.5 (matching the half-price phrase against the base only). Hand-checked, this revision. Working reading adopted for the clone: floor = floor((base + max) / 2), because the worked example is the more specific evidence; the "approximately half price" phrase is left unresolved and the SR2 floor needs a re-fetch (5.4).
- The canonized player behavior, from the game's own Slimepedia text: "Plort market values fluctuate and some of the more savvy ranchers will hoard certain plorts for days when sale prices are high, especially rare plorts." (quoted in [digger-cf-06]).
- Server cost per the dig: one volume counter per SKU plus a daily decay pass (aggregate stack budget owed, 0.3).
- The visibility patch is mandatory for a shared lane: SR1 hid the ledger behind the Market Link ("The Market Link does not show the price of plorts", quoted in [digger-cf-06]) and generated bug threads where players read the hidden ledger as broken (Steam threads in the finding: 12 to 20 in-game day stalls waiting for hoard-driven peaks). Show a saturation number in the sell UI, ship a floor-price dump override as the pressure valve, and run per-player or per-faction volume ledgers so a dump stays a resource decision instead of a griefing weapon.
- Side tables worth porting with it (deep dive): corral upgrade ladder 250 / 350 (High Walls) / 350 (Music Box) / 500 (Auto-Feeder) / 450 (Air Net) / 500 (Plort Collector) / 425 (Solar Shield); hard capacity exists only on Coops (12 chickens, Deluxe 24) and Ponds (8 plort cap with 10-14 catch-up bursts); hunger clock 3.44% per in-game hour, eat at 33.33%, about 29 hours to full agitation; garden 4 units per 12 in-game hours, 25 harvests then replant, Spring Grass 500 halves to 6 h; 7Zee ladder invite at noon day 7, rank 1 = 750, every later rank 450, rank 28 cumulative 1,326,500, function interleaved with cosmetics (Market Link at rank 11, Tank Booster Ultra at 20, Golden Sureshot at 22, extractor blueprints 23-25, Gold Teleporter 27); Range Exchange six offers per day resetting at noon, four deepening rounds, rival NPCs land days 2 / 7 / 13; day-1 inventory four Pink Slimes, three Chickadoos, three Pogofruit, three Carrots, two Hen Hens; Grotto 800.

### 1.6 Weekly speculation: the turnip Markov [ac-stalk-market, clone]

- Buy 90-110 each in batches of 10 (900-1,100 per bundle); 12 sell periods per week (two half-days per day, split at noon; the shop opens 8am so the AM price is effectively a 4-hour window); rot the next day 7 (5 AM Sunday in New Horizons). Sell range on the item data runs 9 to 660 per turnip; the minimum sell price conflicts across fetched sources (9 on two reads, 20 on a third, owed, 5.4). Salvage: spoiled turnips sell for exactly 100 in NH, 0 in Wild World, and NL charges a 400 disposal fee. WW/CF capped purchases at 990; NH caps only by bells and pocket space (stack data: 10 bundles of 100 = 1,000).
- Transition matrix, P(this week | last week):

| Last week | Large spike | Small spike | Decreasing | Random |
|---|---|---|---|---|
| Large spike | 5% | 25% | 20% | 50% |
| Small spike | 25% | 15% | 15% | 45% |
| Decreasing | 45% | 25% | 5% | 25% |
| Random | 30% | 35% | 15% | 20% |

- Steady state with unknown last week: fluctuating 34.6%, large spike 24.7%, decreasing 14.8%, small spike 25.9% (predictor source: 4530/3236/1931/3385 over 13,082).
- Curves (deep dive, from the reverse-engineered predictor code the wiki cites): large spike peakStart = randint(3,9); the 5-period peak ladder is U(0.9,1.4) / U(1.4,2.0) / U(2.0,6.0) / U(1.4,2.0) / U(0.9,1.4), so the hard ceiling is 6.0x buy price (660 at a 110 buy); all prices are integer-ceiled multiples of the market's own day-1 buy price. Small spike peaks 140-200% with the middle period the maximum. Decreasing starts 85-90% and decays 3-5% per period; the wiki's own line: "The only way to turn a profit is to go on a different town to sell." (quoted in [ac-stalk-market]). Random weeks show 2-3 peaks capped at 140%.
- Hope conditioning is the design rationale: after a Decreasing week the Large Spike chance is 45% against a 24.7% steady state, and a Decreasing repeat is 5%. A losing week is mechanically the promise of a 2x-6x week ahead.
- Mercy rules: the first-ever purchase is code-forced onto the profitable pattern (small spike; doc quote: "immediately set to Pattern 3 - Small Spike"); loyalty reward at 3 purchase weeks plus 100 aggregate units pays by mail.
- Crack history to design against (deep dive): the generator was lifted from the binary and productized (Turnip Prophet, 1,555 stars / 246 forks / 214 open issues, created 2020-03-31); 2-3 observed prices pin the week because per-draw entropy has publicly enumerable support. Time travel: the 1.2.0a patch regenerated price and pattern on any backwards step ("even 1 minute will generate a new price and likely also generate a new pattern as a deterrent", quoted in [ac-stalk-market]); backwards travel rots in every era; forward-within-week is the single free skip; the WW table-drop placement glitch stopped spoilage outright. Arbitrage at scale: prices seed per market, cross-market selling is legal even across weeks, and communities industrialized it (Turnip Exchange "reached 1.3 million users with 300,000 peak concurrent users, built in about five days"; hosts charging entry fees; r/ACTurnips banned fees because hosts would "boot players after they've already paid an exorbitant bell fee"; both quoted in [ac-stalk-market] from IGN). NL shipped a documented two-system infinite loop (Joan in one town, 500+ Re-Tail price in another).
- Clone/patch list (the finding's own): keep the weekly appointment, the rot deadline, per-market seeding, the first-buy mercy, the week-3 streak gift, and Markov hope conditioning. Patch with: server-side weekly seed that re-entropies pattern and curve parameters (never a client-enumerable fixed table); server-authoritative clock where any backwards step regenerates price and pattern and forward-outside-week rots; an expiry check inventory placement can never bypass; an explicit arbitrage decision (if cross-market selling is allowed, ship the queue tooling as an owned feature and bound it with a sell-side fee or volume cap; this bound restated at every integration point in section 4); onboarding mercy (first cycle profitable, small salvage, streak gift at week 3); a solver tripwire where pattern identification needs most of the week's prices. Developer-posture note from the finding: the source's own producers treat clock freedom as player choice and aim pressure at economics; on the target clock (0.2) the whole crack class is structurally dead.
- Legacy GC decomp constants (same finding, cited for the 3-state ancestor of the NH 4-state chain): day-1 buy = 100 x (1 + (fqrand()-0.5) x 0.6) = [70, 130) bells; one price per day; spike weeks pay exactly 8x the day-1 price on one uniformly chosen weekday; random weeks rise 1.05x plus 0.01 per rise and fall x0.7 with an 0.8x floor; falling weeks multiply by U[0.8, 0.95). Red turnip side market (WW/CF): 1,000 bell seed, one per week, daily watering or wilt, sell ladder 2 / 100 / 500 / 2,000 / 4,000 / 8,000 / 16,000.
- FLAGS: minimum sell price 9 vs 20 (above); backwards-travel price behavior straddles the 1.2.0a patch boundary across three sources; constants come from community reverse-engineered code with a self-declared float-fidelity caveat; the original datamine thread was unreachable (all in 5.4).

### 1.7 Corpse-quality processing chain [gk-corpse-quality-processing, clone; content-reskin required per 0.3]

Adaptation note (assembler, required): the source's corpse/butcher framing needs a content-policy pass before shipping on the target platform. Port the mechanism exactly: every delivered unit is a randomized resource with a visible two-axis quality score, a fixed-delta removal pass, once-per-type priced treatments, a decay clock, and a quality-gated payoff. The theme verbs are operator's call; the math below is theme-neutral.

- Clock (deep dive, fetched Days page): a day lasts 7.5 real minutes, the week has six days and lasts 45 real minutes, sermons fire once per the payday day. Source pacing evidence only (0.2). The courier rings a map-wide bell on delivery; cadence is every 2 days before the feeding crate, daily once it is stocked (5 carrots per unit; strike event costs 10 food + oil; patch 1.027 stopped deliveries into an empty crate).
- Arrival roll: 4-6 white / 2-4 red. Every unit is a randomized resource with a visible quality score.
- Autopsy/removal deltas: blood -1R+1W, fat -1R+1W, flesh -1W, skin +1R-1W, skull +1R, bone 0, organs random 2R / 1R+1W / 2W (the Morgue cultist table reads +/-3 on both axes and varies by quest stage; the inconsistency is flagged), dark organ -4R-1W. Injections/treatments, once per type: lye +1R+1W, acid -1R-1W, glue +1W, silver -1R+1W, gold -2R+2W, dark +2R; silver needs 1R present, gold needs 2R.
- Budget math: a 12-white build requires arrival of 5+ white and 4 or fewer red, keeping 2+ red for the priced treatments.
- Decay: every 10% freshness lost = -1 white (green skull); below 90% the unit cannot convert to the premium path. Mitigation ladder: stations slow the clock, tier-2 stations halt it, a restore treatment gives back half, a preservative halts permanently.
- Conversion ladder, white count to worker efficiency: 0-1 = 2%, 2 = 5%, 3 = 8%, 4 = 10%, 5 = 12%, 6 = 15%, 7 = 18%, 8 = 20%, 9 = 22%, 10 = 25%, 11 = 28%, 12 = 30%, 13 = 32%, 14 = 35%, 15 = 38%, 16 = 40%, 17 = 42%, 18 = 45%, 19 = 48%, 20 = 50%, 21 = 52%, 22 = 55%, 23 = 58%, 24 = 60%, 25 = 62%, 26 = 65%. Asymmetry worth cloning: "Zombies get no penalty from red skulls but a grave does" (quoted in [gk-corpse-quality-processing]), so junk converts into permanent labor at zero rating cost. Worker unlock at 19.5 source-days; the juice gate runs 150/50/50 techpoints.
- Economy: certificate fixed 150; re-open permission 175; the wiki's own arithmetic: "These cost 175, which is 25 more than what you are paid for the Burial certificate." (quoted in [gk-corpse-quality-processing]), so each bury-unbury-rebury cycle nets -25 while refunding a full rebuild. Finding's correction to the first pass: this is a near-costless re-roll, and it becomes a true printer in any clone that pays per burial without a per-dig fee and without binding one certificate per unit instance.
- Payday: base rate 3 copper : 1 rating, once per week, plus 1 faith : 5 church rating. FLAG (load-bearing): a fetched Church line claims 3,000 to 4,000 per payday at 200 rating on a gold sermon against a 600-copper base-rate read; the church-rating donation bonus is undocumented and the tension is unresolved (5.4).
- Rating and caps: decor cap +12 per slot (base best unit 13 white, 16 after the first cap raise, 26 after the second); the DLC pattern ships a matching decor ladder in lockstep with each cap raise (documented max layouts 1258 base, 1594 after v1.3, 2488 at 26-quality units) plus a new currency and processing room, reopening the whole chase. Royal services money ladder: Citizen 10, Rightful Citizen 300, Aristocrat 120,000.
- Gates: preacher at rating 5; the mid church at 30 rating + 20 church rating + papers; the cathedral at 200 + 50 + carved marble.
- Documented engine bugs to design out: negative-count treatments mint white points past the budget (clamp both sums at 0 after every mutation); the courier's delivery depended on area-load state (make cadence a function of elapsed day ticks alone); a double-click placement glitch duplicated structures; payday-formula tension above.

### 1.8 Labor + care loop [digger-cf-01, clone]

- Worker skill 0-8 natural, hard cap 10: +1 per condensation (up to 4), +1 per book consumable (300 medal currency, one level per skill per worker), +1 from each of 12 partner species (one per skill) stationed in base. Raise caps at natural + 6 and at the hard cap 10, so a natural-8 worker can gain only +2; the "max +6" figure holds for natural 0 to 4 (arithmetic from the recorded numbers, this revision).
- Base gates: level N grants N worker slots to 30; base count 1 / 2 / 3 / 4 at levels 1 / 10 / 15 / 25; per-level build objectives (level 3 feed box + 3 beds, level 4 plantation, level 7 hot spring, level 11 research lab).
- Status ladder, post-0.7.0 values: hungry attack/defense/work -10%, starving -20%, cold -5%, ulcer work -10 / move -5, depressed work -20 / move -10; damage stops draining sanity. Pre-0.7.0 values ran double; the halving patch is a live-tuning lever (section 2, item 18). FLAGS: numeric SAN drain, depression threshold, recovery ticks, per-level work-speed multipliers, and monitoring-stand hardmode multipliers are all unverified (5.4).
- Care sink: medicine buy prices 780 / 1,820 / 3,120 (craft: 5 berries + 2 horn, 3 ingot, 5 ingot at workload 50 / 150 / 500). Research bills: handiwork +10% at 50,000 workload, +5% at 200,000, +5% at 500,000. FLAG: the recorded tree cap reads "cumulative +35%" while the three named handiwork nodes sum to +20 (hand-checked, this revision); 15 points of the tree are unlisted, so either nodes are missing from the record or the cap is wrong; implement +20 as the sourced sum and treat +35 as an unexplained ceiling (5.4).
- Rest and control: hot spring tier 9 (workload 80), high-quality bed tier 31 (workload 500); monitoring stand tier 7 tunes pace and per-task allow/disallow.
- The attendance law, quoted from the dig's fetched Palbox page: "Pals likely don't work as much when you're away from the base" (quoted in [digger-cf-01]). Production must bind to attended sessions and upkeep must resist purchasable cleanup, or location-keyed extraction bases plus the medicine ladder bypass decay entirely. Location-keyed mining bases became official content in 0.3.1, which is the strongest possible confirmation the bypass is real player behavior. Pathing caveat: the wiki's stuck-worker starvation passage plus two official mitigation patches document recurring silent labor death; a server-side labor sim needs stuck detection and reachable-feed validation as day-one systems (see skips, section 3).

### 1.9 Board, rank, and the paid shortcut [digger-cf-13, clone; digger-cf-24, reskin verdict, table clone-worthy; digger-cf-04, clone]

Portia commission board (deep dive, bands are min-max across the full wiki tables; they widen the first pass, which reported modal rows):

| Rank | Rep gate | Gols | Exp | Rep | RP | Deadlines |
|---|---|---|---|---|---|---|
| D | 0-500 | 140-780 | 40-100 | 20-100 (standard 28-32) | 0-30 | 5-10 days |
| C | 501-2,500 | 316-1,108 (city 1,060-1,300) | 80-200 | 40-200 (standard 58-62) | 0-80 | 10-15 days |
| B | 2,501-7,500 | 450-1,082 (city 1,970-3,411) | 100-250 | 88-280 | 0-34 | 10-15 days |
| A | 7,501-17,500 | 367-1,702 (city 3,866-6,131) | 120-300 | 98-360 (standard 98-102) | 0-36 | 10-15 days |
| S | 17,501+ | 777-2,041 (city 4,800-9,549) | 150-350 | 85-450 (standard 108-112) | 0-70 | 10-20 days |
| SS | municipal, weekly | 4,058-45,000 (city 15,238-24,954; blank-requester 40,000-45,000) | 300-1,200 | 200-1,000 | 0-37 city, 32-37 NPC | 15-25 days |

(Source deadlines are in source days; on the target clock they map to server-day counts per 0.2.)

- Caps: 1 active commission, 1 board claim per day. The documented hole: story commissions sit outside both caps and are refarmable same-day. The finding's read: this is also the sanctioned catch-up valve against a rival with a 5,250-point head start (Steam guide: "depriving the competition (that is, Higgins) of extra Workshop points", quoted in [digger-cf-13]); port it with the story slot consuming the daily claim and diminishing rep on repeat clears, or gate it behind per-quest server flags.
- Rival pacing: Higgins starts 5,250 and gains 144-214/workday (the Hotfix 1.1 weekend-gains line carries the wiki's Verify flag); Allen Carter 826 at +30-50; Sweet 291 at +20-30; Wang 110 at +8-22; the player starts 0. Rivals draw from their own server-side pools, immune to player geometry (the wiki states blocking Higgins physically does nothing). Year 2 onward all rivals start at 0.
- Reset law: rep resets to zero each year, earned rank persists (Pathea email quoted in the finding: "now rank s is still 17,501 to reach"); top-3 mails 10,000 / 7,000 / 4,000 gols plus Data Discs; the annual ceremony awards the Gold Trophy to rank 1 only. Blueprint rolls are reload-proof by the wiki's own line (Data Disc page), the one lottery the dev hardened.
- Social pays economy: relationship steps at 100 points gate photo / play / confession / proposal; Antoine pays +3 / +6 / +10% gols at Buddy / Friend / Lover; Presley pays +1 / +2 / +3 / +5 rep at Associate / Buddy / Friend / Good Friend; the Commerce Hot Shot skill adds +1-4 rep and +5-20% gols; chat and gift capped 1 per NPC per day; holidays x2 and birthday x3; relic displays tick 20-40 points per viewer per day; the gratitude gift is a ~1% pull-tab (The Waiting Girl Music Box) decided at hand-in and therefore reload-fishable in the source. City orders pay 0 RP with top-of-tier rep. Weekend inspections (rank C+): 4 items/day, flaw table 2/120s/5, 3/140s/6, 4/160s/7 mistakes, first error free, rep per item D 8-12 up to S 16-20 (3-flaw flat 16-24, 4-flaw 20-28), special accessory at exactly 100 from an 11-item pool (reward table carries the wiki's own stub flag). Newspaper ad: 100 gols buys +20 rep the next morning, one at a time.
- Abandon and fail are soft: abandon costs town rep "a small amount" (unnumbered), fail costs "an extreme loss" (unnumbered); port with abandon priced as a percentage of the commission's own rep band plus a burned claim day.
- Dinkum licence ladder [digger-cf-24, reskin, table clone-worthy]: incomes board task 100 PP, NPC daily 50, museum set 100, 3 daily milestones 25-100 each; lifetime milestone ladder of 250 levels totaling about 34,700 PP. Costs: core licence tiers 250 / 1,000 / 3,000 (full line 4,250), vehicles 1,200 / 2,400 / 7,200, commerce +5 / +10 / +15% sell at 750 / 3,000 / 9,000. Licences buy verbs (tools, vehicles, sell rates), never raw stats. Caution carried from the dig: the bank conversion (500 currency = 1 point) collapses the licence gate once any money loop exists; keep the unlock currency insulated (5.1 item 3). FLAGS: the Licences wikitext carries the wiki's own Under Review flag; time-travel reroll claims carried zero quoted evidence.
- Checklist vs paid shortcut [digger-cf-04, clone]: 6 rooms, 30 bundles; "A few bundles display more items than there are slots to fill (e.g., Artisan Bundle: 12 items, 6 slots to fill)" (quoted in [digger-cf-04]), so donation is a choice; mixed qualities accepted in one slot. Honest path: calendar-locked across seasons; "Completing all Vault bundles costs 42,500g, and repairs the Bus Stop" (quoted in [digger-cf-04]); room rewards are permanent communal world changes (Quarry bridge, Greenhouse, Copper Pan plus a working fish tank, minecarts, bus to the Desert) plus one room paying +500 friendship to every met non-datable villager, a reward with no paid equivalent. Paid path: 5,000 membership, developments 15,000 / 20,000 / 25,000 / 35,000 / 40,000 = "It costs 135,000g to complete all developments (140,000g including the membership purchase). There are no 'Friendship' rewards" (quoted in [digger-cf-04]); "Only one development can be purchased per day" (quoted in [digger-cf-04]), a 6-day floor; 500,000 endgame theater purchase; 50,000 Auto-Petter. The digger's tuning note: 140,000 vs 42,500 is a 3.29x multiple on the checklist's cash component, so the shortcut buys time; the entry token sits at about 12% of the cash room so the fork is always affordable and always tempting.
- Hard gates from the patch history: 1.4 "It is no longer possible to purchase a Joja membership after completing the Community Center."; 1.5.4 fixed perfection checks for mid-run route switches. Keep the pre-commitment leak deliberately: the wiki's own strategy line coaches farming easy bundle rewards before buying in, and the finding reads that seam as where the drama lived. Route toggling history: 1.5.2 and 1.5.4 fixed both-direction perfection and access bugs for players who flipped routes mid-run; 1.6 monetized the bypass as waivers at 500,000 per 1% (the page's own arbitrage note: 14 waivers at 7,000,000 undercut 13,000,000 of legit buildings by 6,000,000). Multiplayer boundary races are on record: a host buying membership while a farmhand completes the last bundle, and same-day membership-plus-completion, left the world randomly flipping between states (patch fixes through 1.5.1). Donation validators decayed toward accepting anything (furniture-as-donation fixed twice in 1.3.27); reward claims were only idempotent after the 1.4.3 menu-close fix. Appointment supply: Traveling Cart twice-weekly, 10 items in quantities 1 or 5, furniture at 1/146 per piece, Rare Seed 1,000g at 100% spring/summer appearance; a published never-sold list keeps the calendar lock honest (5 of the 6 Missing Bundle slots are on it).

### 1.10 The daily luck scalar [digger-cf-05, clone]

- One hidden scalar per server day: "The base value for daily luck is a randomly generated number from -0.1 (unlucky) to 0.1 (lucky)." with 201 discrete values at 1/201 each (quoted in [digger-cf-05]). Integer-tick implementation avoids the source's float lesson (the charm's +0.025f makes exact neutral unreachable through a rounding error).
- Reveal only as vague tiers through a free daily ritual (the Fortune Teller model); six mood tiers over the tick bands; the exact boundary floats are secondhand in the dig (5.4). "Daily luck does not change if the day is restarted, but it can change by replaying the previous day." (quoted in [digger-cf-05]); port the persistence, keep it server-side per character-day across rejoins.
- Permanent charm +0.025. Arithmetic correction, this revision: 0.025 is 12.5% of the full 0.2-wide band and 25% of the positive half; the MECHANICS input's phrase "exactly 25% of the band" holds only for one side. Buff ladder of consumable sinks: Ginger Ale +1 (5m, 1,000g shop, craftable), Banana Pudding +1, Fried Eel / Spicy Eel +1 (mail gates at 3+ / 7+ hearts), Pumpkin Soup +2 (7+ hearts), Lucky Lunch +3 (TV recipe, year 2), Magic Rock Candy +5 (8m24s; sources 0.13% Haunted Skulls, 0.2% / 0.4% Mystery Boxes, 3 Prismatic Shards at the Thursday trader, museum 90 donations); stacking cap +10.
- Buff equivalence, resolved as per-table coefficients (hand-checked from the recorded formulas, this revision): Skull Cavern treasure rooms 0.01 + (Daily Luck / 10) + (Luck Buffs / 100) makes 1 buff point = 0.01 = exactly 1x of a max daily roll (0.1/10 = 0.01). Fishing treasure chests run on half the value (+5% best at 0.1, buffs +0.5% per point), again 1 point = 1x daily max. The mines ladder (2% base rock, daily swing +2.5 points at max, buffs +1 per point) makes 1 point = 0.4x of the daily max there. The wiki's loose line "a buff of +2 may have similar effects to a daily luck value of 0.1" matches the 1x tables loosely and overstates the mines relationship; carry the per-table coefficients as the constants and treat the prose line as a flagged approximation (5.4).
- Wire-ins (opportunity tables only): the mine and monster-kill ladders and Skull Cavern formula above; fishing golden chests on full value (+10% best, charm adds 2.5%) with a 37.5% hard cap; special-item chance uses (1 + DailyLuck) x DistanceFromLand/5 and is 5x at 5 tiles from land; panning spots and garbage items are predetermined per day with luck touching only the drop chance; crop doubling, wood bonus pieces, trinket drops, roe quantity, lightning density all ride the scalar. Death softeners: passout costs 10% of gold capped 1,000; mine death 5-25% capped 15,000.
- Guardrail, verbatim from the dig: "(Luck does not increase the chance to receive rare minerals and artifacts from breaking geodes. These results depend only on the save file and the sequence in which the geodes are broken.)" (quoted in [digger-cf-05]). Luck modulates opportunity tables; content tables stay outside the scalar.
- Determinism lesson: the public predictor "simulates the random number generator used in Stardew Valley" from the full save file and defaults to worst possible daily luck; the fix pattern is fresh server entropy per day, one display surface, no seed reuse across days.
- Lane policy, single and final (resolves the cold-read contradiction): the shared scalar ships as a designed feature on the multiplayer-average rule (Skull Cavern uses "the average of luck stats of players present", quoted in [digger-cf-05]); the charmed Pilgrim is the faction's luck carrier with visible attribution. Contribution caps apply to shared loot pools (5.1 item 7); the scalar itself carries no contribution cap, only the +10 buff stack limit.

### 1.11 Gate ladders: tier-by-kill

Terraria [cf-18, clone]:

| Ore tier gate | Value |
|---|---|
| Tool-power thresholds | Meteorite 50 / Demonite 55 / Hellstone 65 / Cobalt 100 / Mythril 110 / Adamantite 150 / Chlorophyte 200; tools step 55, 65, 70, 100, 110, 150, 200, 210, 225 |
| Boss chain | Eye (spawn needs 200 max HP + 11 defense + 4 town NPCs, 1/3 per night) > Wall of Flesh (world permanently converts, drops the altar hammer) > 3 mechanical bosses (10% per night) > Plantera (bulbs only after all 3, always drops the Temple Key) > Golem > Cultist + 4 pillars > final boss |
| Repeat-smash decay | nth altar cycle yields 1/n; cycles 4-6 half, 7-9 third; each smash spawns 1-2 wraiths (hazard priced into the unlock) |
| Top-tier scarcity | Chlorophyte capped at 40 ore in 71x71 and 130 in 171x71 checks, renewable by spread |

Exploit history to design against: fishable crates minted hardmode ore before any gate event; the fix bound the tier to the gate itself (crate variants split at the gate) plus yield nerfs of roughly 40 / 30 / 20%; the Reaver Shark fell 100 to 59 pickaxe power; the temple shipped several pre-Plantera entry methods.

Core Keeper [cf-08, reskin verdict, numbers worth borrowing]: distance curve from the hub 65 / 190-210 / 300 / 330 / 550 / 600 / 600 / 650 / 650 / 700 / 1240-1280 tiles per tier; gear gates at 110 and 280 mining power plus 180 and 280 fishing; every one of 18 bosses (20 with seasonal variants) drops a unique key; re-fights cost a crafted or coin-priced idol (500 cut to 200 after launch; endgame idol stocked only after the kill) and a 5-6 minute soul cooldown on the six titans; loot = guaranteed key + 1-of-9-style pool + 5-of-21/27-style pool, with per-boss shapes tabled in the deep dive (Glurch 1-of-11 + 5-of-19 up to Core Commander 1-of-5 + 6-of-13 plus seasonal tables) and ore faucets keyed to the next gate's threshold (Iron 19.82% at Ghorm rising to Galaxite 37.69%/90.61% at Ra-Akar, Solarite ~29.3%/85% at the hydras); figurine chase buffed ~10x in one patch (0.09% to 3.38% on Igneous); anti-cheese kit: leash regen (2%/5s Ghorm, 10%/5s slime bosses past 25 tiles), add caps (12 within 15 tiles; Ivy 30 to 15), key consumed atomically with spawn success (1.0.1.0 fix: "Boss-summoning items are no longer lost if they are broken the moment before the boss spawns", quoted in [cf-08]), no-waste rule ("Nothing happens", item kept), loot chests anchored to generated ground after a dialogue beat, and zero lootable blocks under gate structures. First-boss hook: the day-1 kill drops a progression key and a merchant NPC, so the first gate-check widens the base loop. Controlled experiment worth copying: the crossover boss ships seven items all at 100%, zero RNG, zero chase.

Gordo chokepoints [digger-cf-07, reskin]: burst thresholds 30 (starter) / 50 (standard) food units, favorites count double; shake tell at 23 / 37; guaranteed pop payout of 10 units + 2-3 crates + a key or a teleporter reveal; 16 chokepoint bosses, 11 keys, 8 + 3 gates, credits demand 5 gates; jackpot pops sit behind a tradeable bait. The pop must fit a session: patch history cut 50/75 to 30/50 for exactly this. Snare-reuse fix 0.5.1c: "Fixed bug where you could pick up Gordo Snares with the gordo on them and reuse the snare." (quoted in [digger-cf-07]). Movement-tech caveat: jetpack and largo physics found gate skips; seal geometry server-side. On the target clock (0.2) the 5-6-minute cooldowns and pop pacing rescale to session-fit dials.

Tinkerlands vendor rows [tinkertown-dungeon-loot-shop-stock, reskin]: 1 named boss kill = 1 vendor stock row; boss-gated ore rows run 15 silver to 2 gold 50 silver against an always-available baseline, roughly 3-13x spread (time-to-earn grounding unfetched, 5.4); soul-token premium rows 4g-40g; relationship-max cosmetic rows 5g. Tinkertown itself ships zero shops; the loop lives in the sibling title, and its patch history names the abuse class: instant boss respawn (fixed 0.1.3) and re-enter-to-refarm chest respawns (fixed 0.7.0e), plus the deliberate counter-example of reusable keys (0.7.0g: "Scarab keys no longer get consumed by the gate keepers, you can therefore reuse them if you want to fight the boss right away!", quoted in [tinkertown-dungeon-loot-shop-stock]). The shop becomes a kill checklist players read every visit; stock unlocks ride durable one-time clear flags.

### 1.12 Daily-cap appointment stack [cf-23, clone]

| Cap | Value |
|---|---|
| Battle goals by team size | 1v1 3/4/20; 2v2 4/4/25; 3v3 4/4/30; 4v4 5/5/35; 5v5 5/5/40; 6v6 5/6/40 (beats/hand/points) |
| Turn limit | hard cap 9 turns, warning at 7; draw and forfeit both count as loss |
| Deck | default 10 cards; signature moves unlock at levels 1 / 3 / 6; club moves 2 per club at 1 and 5 tokens, max 3 owned |
| Rarity | common 359/400, uncommon 40/400, gleamy 1/400; weather boost + a purchasable once-per-day gleamy lure |
| Daily income | up to 35 from three tasks (5 / 10 / 20); badge bank 3,415 one-time; tournament 20 + 50 plus an item prize on a 7-day schedule with the next 4 days visible |
| Shop caps | 10 seeds/day (20 upgraded); one 50%-off item/day; the seed loop mints a collectible from every wild win whose 3 cards permanently change the battle deck |

Abuse record on this finding: item-mint moves pay out on loss and "Battles can be forfeit at any time" (quoted in [cf-23]); the Finite Loop card replayed the once-per-day Puffed Disrupt to spawn two gleamies in one day; wild encounters reroll on leave-and-reenter. All three die under server-authoritative resolution (5.1 items 1 and 13).

### 1.13 Stock-scarcity menu [cf-29, reskin verdict, mechanic worth porting]

Customers order only stocked menu lines; drink lines cap at 8 against 48 dish lines; kegs, taps, and a day-bin that clears overnight define storage roles; aging runs 5 stages over 5 days paying +10 / +20 / +30% price; brewing takes 30 minutes to 12 hours by tier. The menu cap is the strategy layer: refilling a small capped rotation is the session ritual. Breadth claim, status restated: "every additional unique line pays +4 reputation per customer" is a first-pass figure recorded once in the payload and repeated by the RETENTION input, with no second source confirming it; carry it as provisional and calibration-bound (5.4). Carried warning from the same finding: trend stock at +25% price with uncoupled demand collapsed to single-line stocking, and the punishment-debuff patch that fixed it drew tedium backlash; couple demand to the promoted price on day one. FLAGS: distillery unlock reads level 5 on one page and 11 on another; inventory-cap figures excluded after a 403.

---

## 2. The reskins: curves worth reskinning

Keep the shape, re-roll the numbers for the target clock and the VM economy.

**Pacing ladders**

1. Gentle-then-flat threshold curve (Travellers Rest [cf-29]): 1,000 / 1,500 / 2,000 / 3,000 / 4,000 / 5,000 / 10,000 / 15,000 / 20,000 / 30,000 / 40,000, then 250,000 at level 20, then flat +25,000 steps to 1,000,000 at level 50; occupancy 10 to 38. Reskin as boon-draft tiers or faction season gates; one named unlock per band.
2. Accelerating renown gaps (Kynseed): 0 / 500 / 1,500 / 3,000 / 5,000 / 7,000 / 10,000 / 13,000 / 16,000 / 20,000 / 25,000 for levels 0-10.
3. Gold age gates (Craftopia [digger-cf-11]): 500 / 2,500 / 20,000 / 50,000 / 200,000 / 1,000,000 for ages 3-8, each plus region materials. Abuse receipt: uncapped automation income (claimed ~27M gold/hour/module, Sept 2020, pre-rework, dated) flattened every gate in minutes; bind automation output against the gate curve.
4. Point-spend tier markers (Sun Haven [digger-cf-25]: tiers at 5 / 10 / 15 / 20 / 25 / 30 / 35 / 40 / 45 points spent; Craftopia [digger-cf-11]: 1 / 3 / 5 / 11 in-branch). Both sit on a 1-point-per-level printer (70 levels, 5 pools, about 350 earned points).
5. Rep-to-tier ladder with annual reset (Portia [digger-cf-13]): the 1.9 table; rep wipes each year (every 112 server days, 0.2) while rank persists, which refreshes the ladder for veterans.

**Diminishing and decay curves**

6. Settlement-size decay (Necesse [digger-cf-12]): happiness bonus -10% per tier, +40% at 0-5 settlers down to 0% at 24+; upkeep ladders: food quality +10/20/35%, variety +10/20/30/40%, room size +4 to +20%, furniture +4 to +20%, barracks -20/30/40/50%, crowding -40% each at 24+; strike below 50% happiness. Growth itself decays the bonus, so every roster step forces reinvestment. Combat coupling: boss HP +20% per NPC decaying to +0% at 11, cap 210%; guards +500 base HP. Visitor cadence (5-10 min spawn / 8 min stay / 4 min leave, ticket weights) comes from a mod description quoting vanilla defaults, flagged unverified; the money-farms page self-flags as outdated.
7. Geometric market decay (Slime Rancher [digger-cf-06]): volume x0.75 per day from a 50%-of-cap start. The crash self-heals; hoarding becomes a timed bet the source's own item text blesses.
8. Repeat-yield decay (Terraria [cf-18]): nth cycle yields 1/n. It prices repeat unlocks without banning them.
9. Shrinking purchase steps (Palia [cf-28]): focus cap 200 to 1,000 in 41 purchases at 100 renown each, increments shrinking 50 to 25 to 10 per step; same shape on the bonus track 20% to 100%; recorded total "4,000 renown per track". FLAG: 41 x 100 = 4,100 (hand-checked, this revision), so either the final purchase is discounted or one recorded figure is off by 100; owed (5.4). Pair with hard caps: 999,999 gold, 9,999 renown.
10. Fertility burn (Temtem [digger-cf-21]): the child inherits the lower parent's remaining fertility, so every finished unit is a depreciating consumable and the market prices remaining uses through a min-fertility filter.
11. Action-count unlock counters (Niche [cf-22]): gene unlocks read 30 hot days, 100 swims, 50 digs, 10 generations, survive 100 days; 107 mutations with 59 available by default; a 2-slot draft with 50% application per pick; failure attempts still count toward the counters. Retention rationale from the community thread: "having my progress on gene unlocking reset every time gets frustrating" (quoted in [cf-22]).
12. Per-fight mastery band (Chained Echoes [cf-20]): green zone +25% dealt, -15% taken, half skill cost; dedicated vent/raise skills at 15/17/20 and 20/25/30; a collection skill gated below 25 / 40 / 50% enemy HP, so precision itself is a collectible. FLAGS: red-zone magic damage reads 1.5x on a fan decompile and 125% flat in a guide, unresolved; per-attack gauge deltas unpublished; "punishes overkill" appears in no source read, the mechanic identification is the finding's own mapping.

**Compounding and catch-up curves**

13. Generational compounding (Kynseed): talents 1 to 2 to 3 across generations (spouse talent + inherited + one random); talents exist only through inheritance, so every death is a draft event; six tasks per generation, 3 fixed + 3 randomized. Design edits from the digger: compress the 18-year heir gate to a same-session or few-session cycle for the target platform's pace, and add loss pressure to the handoff, because total carryover ("all the items stay, not just the fairweather ones but the entire inventory as well", quoted in [kynseed-generational-inheritance-skills-farm]) is the source's one systemic flaw; cap the wheel and grass loops per day.
14. Catch-up bands (Monster Sanctuary [digger-cf-26]): hatches land within 3 levels of your best unit; the grind tax on experimentation approaches zero.
15. Inspiration jackpot (RimWorld [digger-cf-15]): mean time in days = 410 - 400 x (mood/100): 210 days at 50% mood down to 10 days at 100%. Source days map to server-day dials on the target clock. A sustained-high-morale super-draft for the Pilgrim bar.
16. Visible threshold bands (RimWorld): minor 35% / major 20% / extreme 5% (major = 4/7 of minor, extreme = 1/4 of major, band capped 1-50%); mean time to break 10 days / 3 days / 0.7 days; moodlet schema of magnitude / expiry days / stack limit / stacking multiplier (marriage +40/30/1; party +8/10/10/x0.75; fine meal +5/1/1); a catharsis valve (3 days, stack 5 at x0.75) so a bad night never deletes progress; difficulty base-mood 42 / 42 / 37 / 32 / 27 / 22. FLAG: Catharsis magnitude reads +30 in prose and +40 in the table row on the same wiki; def-level confirmation owed.
17. Infinite tail (Factorio [digger-cf-10]): cost 2^(level-6) x 1,000 past level 5, benefit a flat +65% per level with gains the source calls increasingly trivial. The permanent next-goal shape for post-cap players.

**Live-tuning levers (patches to copy as day-one dials)**

18. Status halving (Palworld [digger-cf-01]): every debuff number halved in one patch (0.7.0), plus damage stopped draining sanity, production payoffs untouched. Tuning evidence the source protected session cadence.
19. Timer halving (Temtem [digger-cf-21]): egg production 25/15 cut to 10/5 minutes at launch; hatch up to 45 cut to 3-30. The whole loop was roughly halved once retention data landed; the finding cites no numbers, so this is a directional precedent only (0.6).
20. Pop-fit-to-session (Slime Rancher gordos [digger-cf-07]): burst requirements cut 50/75 to 30/50 across two patches so the payout lands inside one session.
21. Skill-XP cost with comfort upkeep (ONI [digger-cf-16]): point n costs 150,000 x (n/15)^1.44 XP (point 1 about 3,037.52, point 2 about 8,241.43). Morale upkeep, restated cleanly from the recorded text: each learned skill tier adds its tier number to the worker's morale requirement; 2 or more points of requirement above the morale supply costs -20% stress per cycle; each point of requirement below the supply returns +2.5% per cycle, capped at 10 points. Recorded as-is; the per-stat game semantics sit behind the finding's compression and are unverified (5.4).
22. Law cooldown ladder (Frostpunk [digger-cf-14]): 18 / 36 / 45 / 72-hour cooldowns by severity; the emergency relief event hardens to one use. Reskin as boon-draft tax cadence mapped to server days (0.5); the juggling exploit must be designed out first (5.1 item 9).

---

## 3. The skips, and why

1. Belt-and-bot factory sim (Factorio [digger-cf-10], reskin verdict): skip the physics sim. Port the charge-shaped ceiling (per-hub delivery slots at the 50-70 per minute shape), the cargo curve (1 to 4 items), the player-visible bottleneck, and the infinite tail. Design law: make the binding constraint charge-shaped, because distance-shaped constraints get answered by hub spam. Ships only if hub logistics exist as a system (0.4).
2. Tile-gas simulation (ONI [digger-cf-16], reskin): skip tile physics and diffusion constants. Keep idle-at-cap producers, the 1-9 errand ladder with a fixed default of 5, and the emergency bypass priced at +50% stress per cycle, as per-zone ledgers and a per-player errand board. The dig states the hook survives zone-level abstraction. The pressure-limit puddle exploit (a vent in shallow liquid compresses without limit) is the standing argument for surface-condition audits on every hard cap. The errand ladder's lane destination is the Pilgrim labor board (section 4).
3. Proximity-ticked automation (Craftopia [digger-cf-11], reskin): the ~10-tile tick radius and persistence monolith are sim-cost workarounds; run production server-side on a ledger. Skip the save-file split that enabled the documented dupe, and bound automation output against the gate curve (the 27M/hour claim above is the receipt).
4. Plot rent (Palia [cf-28], reskin): the dig checked Housing_Plot, Housing_Slots, Housing_Add-ons, Trees, and Currency; plots are one-time purchases (50,000 to 225,000 in 25,000 steps) and no rent, tax, or upkeep line exists on any fetched page. Skip the rent framing; use Palia as the purchase-sink reference (slots, add-ons, hard caps) and as the shared-spawn reference (nightly grove rally: 1 spawn per night, 2 max, quarter-map audio cue, tap-once full loot, nodes persist 3-5 minutes, Monday weekly challenges at 3 per skill). A recurring-plot-cost design needs its own reference; this dig supports it with zero sources. The star-quality sell multiplier is implied at 1.5x by two samples and stated on no page (flagged).
5. Worker pathing simulation (Palworld [digger-cf-01]): the wiki's stuck-worker starvation passage, the dedicated-server summon-space fix (0.1.5.0), and the 0.3.1 mitigation line document recurring silent labor death. A server-side labor sim needs stuck detection and reachable-feed validation as day-one systems, and even then the attendance law stands. Build the Pilgrim labor loop as ledgered production under the attendance rule instead.

---

## 4. How each mechanic lands on the lane (VM economy / boon drafts / faction war / Pilgrim)

Integration map. Source column: "ask map" rows come from the MECHANICS integration map as delivered; "assembler" rows are this revision's additions closing the cold-read holes; amended rows are marked.

| Mechanic | Lands on | Finding | Source |
|---|---|---|---|
| Trait roll table + fertility burn | boon drafts as breeding picks; VM prices on gear consumables | [cf-02], [digger-cf-21] | ask map |
| Capture formula + variant rates | wild encounter math; the Pilgrim body as the at-risk recorder (assembler lane read; the asleep-auto-fail rule is the finding's) | [cf-19] | ask map, amended |
| Star rating + pity | faction war scoring feeding drop tables | [digger-cf-26] | ask map |
| Season clock + published ROI table | the 28-day season frame; the economy table players optimize against | [digger-cf-03] | ask map, amended (war-window reconciliation per 0.2) |
| Market crash curve | VM commodity sinks on per-faction ledgers, saturation visible in the sell UI | [digger-cf-06] | ask map, amended |
| Turnip Markov | weekly faction market, one seed per faction; cross-faction selling only through owned queue tooling with a sell-side fee or volume cap (the 1.6 bound restated here) | [ac-stalk-market] | ask map, amended |
| Luck scalar | shared server-day fortune; Pilgrim luck-carrier via the multiplayer-average rule, scalar uncapped beyond the +10 buff stack | [digger-cf-05] | ask map, amended |
| Commission board + rank gates | daily board; year reset with persistent rank; rival pacing as the faction scoreboard | [digger-cf-13] | ask map, amended |
| Licence ladder | per-player verb unlocks (tools, vehicles, commerce rates) on an insulated currency | [digger-cf-24] | ask map |
| Labor + care loop | Pilgrim base class under the attendance law | [digger-cf-01] | ask map |
| Checklist vs paid shortcut | communal scroll vs corp fund as an alignment fork, priced per 5.3.4 | [digger-cf-04] | ask map, amended |
| Gate ladders + vendor rows | boss keys mint resource tiers; vendor rows flip on named kills | [cf-18], [cf-08], [tinkertown-dungeon-loot-shop-stock] | ask map |
| Corpse-quality chain | the Pilgrim processing station (content-reskinned per 0.3) | [gk-corpse-quality-processing] | ask map, amended |
| Hope/discontent as law cost | draft tax on faction morale; a capstone deletes the meter at permanent cost | [digger-cf-14] | ask map |
| Moodlet schema | Pilgrim shared morale bar with visible threshold bands | [digger-cf-15] | ask map |
| Generational inheritance | rebirth ladder with a guaranteed heir draft and a per-life challenge board (3 fixed + 3 randomized) | [kynseed-generational-inheritance-skills-farm] | ask map |
| Skill pools + tier markers | five XP pools; non-tradable token pricing on power | [digger-cf-25] | ask map |
| Gene-unlock counters | Pilgrim profile ladder with visible counters | [cf-22] | ask map |
| Mastery band + thresholds | faction skirmish pacing; precision collectibles | [cf-20] | ask map |
| Daily-cap stack | login calendar (tasks, tournament schedule, shop caps) | [cf-23] | ask map |
| Stock-scarcity menu | faction depot with a small capped rotation | [cf-29] | ask map |
| Nightly grove rally | shared spawn appointment: 1 per night, 2 max, quarter-map audio cue, tap-once full loot | [cf-28] | ask map |
| Gordo chokepoints | faction war gate events; pop-fit-to-session pacing on war-window payouts | [digger-cf-07] | assembler |
| Repeat-yield decay (nth altar 1/n) | pricing repeat tier unlocks inside one season (faction war re-clears of already-opened tiers) | [cf-18] | assembler |
| Shrinking purchase steps (Palia renown shape) | VM sinks: large capped purchases with shrinking increments toward a cap | [cf-28] | assembler |
| ONI errand ladder (1-9, default 5, +50% bypass) | Pilgrim labor: per-zone errand board under the attendance law | [digger-cf-16] | assembler |
| Settler appointment compounding | Pilgrim roster growth welded to boss kills, tier bonus decays 10% per tier | [digger-cf-12] | assembler |
| Factorio charge ceiling + infinite tail | optional hub-logistics layer only if that system ships (0.4) | [digger-cf-10] | assembler |

Cadence spine (reconciled to the clock model 0.2; each line cites only its own findings):

- Session (per login): labor and care decay [1.8], capture rolls [1.2], board claim [1.9].
- Daily (one server day): the luck reveal, one scalar revealed once per day through the ritual [1.10]; market reroll plus 25% volume decay [1.5]; three daily goals and shop caps [cf-23, digger-cf-24]; the one board claim lands here [digger-cf-13]; the keg-priced processing check [1.4]; Range-Exchange-shaped six-slot offers as the daily-return surface [digger-cf-06 side tables].
- Weekly (7 server days): the buy window with the rot deadline, day 7 [ac-stalk-market]; the appointment shop twice weekly [digger-cf-04]; municipal orders plus the inspection weekend [digger-cf-13]; the war window checkpoint, 1 of 4 per season [0.2, 0.5].
- Season (28 server days): the faction war campaign close and tally [0.5]; crop rollover wither and the ROI race [digger-cf-03].
- Year (112 server days): rep reset with rank persistence and the ceremony [digger-cf-13]; licence-ladder long-arc checkpoints [digger-cf-24].
- Lineage and generation: breeding rolls and fertility burn [1.1]; rebirth, talent inheritance, per-life challenge board, compressed heir gate [kynseed].
- Long arcs: age gates 500 to 1,000,000 [digger-cf-11]; cap-raise events that reopen the whole chase with a shipped decor ladder [gk]; the infinite tail for post-cap players [digger-cf-10].

---

## 5. Abuse patches owed

### 5.1 The 13 abuse classes, each with documented precedent and the pre-patch rule

All precedents fired in shipped games; treat each as a confirmed player behavior.

| # | Class | Lane hits | Documented precedent | Pre-patch rule |
|---|---|---|---|---|
| 1 | Client-resolved RNG | boon drafts, VM, daily scalars | Sanctuary reward-box save-scum ("Save game open box u don't like what u get force quit game n reopen them", [digger-cf-26]); Portia board re-randomizes on reload, gratitude gift decided at hand-in ([digger-cf-13]); Stardew luck survives restart ([digger-cf-05]) | every roll, box, and daily scalar resolves server-side at grant time, committed before any client read, persisted per character-day across rejoins |
| 2 | Determinism leakage | VM speculation, visible RNG | ACNH generator lifted from the binary; predictor recovers exact ranges from 2-3 prices ([ac-stalk-market]); Stardew predictor simulates RNG from the save ([digger-cf-05]) | hidden re-entropy per cycle, server-authoritative clock, zero client-readable seed state, spoilage clock as the hard deadline, telemetry tripwire so identification needs most of the week |
| 3 | Currency-to-gate conversion | VM vs any unlock currency | Dinkum bank 500:1; a half-million-Dink trapping burst at double price bought four tier-1 licences ([digger-cf-24]) | unlock currency earned by activity only; any exchange rate bounded or absent; payout authority server-side |
| 4 | Uncapped repeat windows | faction payouts, commissions, spawn rerolls | Dinkum unlimited trapping deliveries at double price ([digger-cf-24]); Portia story commissions bypass the daily cap, mass-completable same-day ([digger-cf-13]); Ooblets leave-and-reenter rerolls ([cf-23]); Palworld location-keyed bases became official content 0.3.1 ([digger-cf-01]) | server caps per window per account and per faction; rerolling costs the full bait up front; story class consumes the daily claim; if the Portia catch-up valve is kept, repeat clears pay diminishing rep |
| 5 | Cross-pool conversion printers | VM, XP pools, faction-wide buffs | Sun Haven jam 90 Combat EXP with 40% amplification and 50 stacks, designer-tolerated ([digger-cf-25]); Craftopia ~27M gold/hour/module claim vs a 1,000,000 gate, dated pre-rework ([digger-cf-11]); Necesse wheat at 75/min/plot, "will run forever no matter where the player is" ([digger-cf-12]) | cross-pool power priced in non-tradable earned tokens (the Sun Haven Community Token model: "Cannot be sold"); capped deliberate valves; apply-once rule for faction buffs; automation output bound against the gate curve |
| 6 | Multiplicative stacking on a tradable economy | boon drafts, faction PvP | Cassette Beasts AP battery, stacked AP Refund stickers shared through Mind-Meld, guide subtitle "How to break mortal limits, and probably the game's balance too", commenter "this trivializes the game" ([cf-19]); Sanctuary Shield Burst 400% conversion, 20k one-shots, dev replied in-thread ([digger-cf-26]) | per-action conversion caps; PvP-specific coefficients; cap refund-class stacking; soulbind or cooldown any sellable recycle stream on guaranteed-capture items |
| 7 | Griefing in shared systems | VM market, luck, shared plots, shared spawns | shared-ledger dump halves a rival's cash crop for days ([digger-cf-06]); Skull Cavern averages the luck of players present ([digger-cf-05]); wither-by-inaction kills a shared harvest ([digger-cf-03]); Palia etiquette page documents spawn sniping ([cf-28]) | per-player or per-faction volume ledgers; owner-bound decay on shared assets; per-player contribution rate caps on shared loot pools; the luck scalar is exempt from contribution caps by design and ships with visible carrier attribution (1.10 policy, single and final); etiquette surfaces that credit callers |
| 8 | Cap bypass by surface conditions | every hard cap, gate geometry, tier entry | ONI puddle-vented pressure limit ("It is possible to exceed the 2 kg pressure limit by placing the vent in small amount of liquid.", [digger-cf-16]); Slime Rancher snare reuse (0.5.1c fix) and jetpack gate skips ([digger-cf-07]); Terraria crates minted Hardmode ore pre-gate, Reaver Shark 100 to 59, pre-Plantera temple entries ([cf-18]) | audit every per-zone cap server-side against surface conditions; bind tier access to the gate event itself (Terraria's fix pattern); seal gate geometry; purchasable substitutes stay sidegrade-only |
| 9 | Toggle-cost farming | shared morale meter, gauges, draft steering | Frostpunk juggling: raise and lower toggled sources, "you gain both Hope and Discontent immunity for free", plus deferred law costs after the Hope drop ([digger-cf-14]); Chained Echoes tag-outs vent at zero cost, 100-credit gauge items ([cf-20]); Niche slot re-steering between breedings ("a bit like cheating") and 5-food fresh-blood imports ([cf-22]) | per-source diminishing returns or shared cooldown on every relief action; one-shot costs charge at draft time, never on a deferrable trigger; toggle-on/off sources priced in both directions; slot swaps cost a draft token; fresh-blood imports capped or cooldown-gated |
| 10 | Leaky state machines | faction fork, breeding, summons, crafts | Stardew same-day membership-plus-completion left the world randomly flipping; 1.5.4 fixed mid-run route switches ([digger-cf-04]); Temtem Mimit female-slot bug minted an egg every second deposit, fixed 0.7.3 ([digger-cf-21]); Core Keeper key-loss race, fixed 1.0.1.0 ([cf-08]); Ooblets item-mint pays on loss ([cf-23]); Tinkertown full-inventory craft dupe, fixed ([tinkertown-dungeon-loot-shop-stock]); Kynseed death-broker replay bug, dev acknowledged ([kynseed]) | one authoritative event ordering server-side; order-invariant validation on universal-slot interactions; costs consumed at challenge time, rewards minted only on server-confirmed completion; a full purse or inventory never changes craft or trade outcomes |
| 11 | Care-loop and mood-system bypasses | Pilgrim labor, morale, expectations | Palworld sweatshop passives (Nocturnal + Workaholic + Artisan, the dig's label for the combo) collapse care into purchasable cleanup; stuck-worker starvation needed two mitigation patches ([digger-cf-01]); RimWorld joywires (+30 mood at -20% consciousness), misery farming, arrest-interrupt laundering, wealth-suppression expectation farming (+30 below 15,000 wealth, 0 above 308,000) ([digger-cf-15]) | upkeep partially non-purchasable; break states NPC-side or strictly opt-in in multiplayer; mood cures priced in VM currency, never permanent stat trades; treat wealth-derived expectations as a leak surface; on the target platform the care framing ships as care (0.3 content-policy decision) |
| 12 | Restock and clear-flag farming | vendor stock, dungeon loot | Tinkertown fixed instant boss respawn (0.1.3) and re-enter loot refarm (0.7.0e), then deliberately made keys reusable (0.7.0g) ([tinkertown-dungeon-loot-shop-stock]) | vendor stock unlocks ride durable one-time clear flags; audit every rejoin or re-enter path that could re-fire a clear flag |
| 13 | Day-gate bypass inside battle logic | once-per-day limits | Ooblets Finite Loop replayed the once-per-day Puffed Disrupt to spawn two gleamies in one day ([cf-23]) | day gates live in the server ledger; server-authoritative resolution (item 1) removes the class |

Finding-level patch plans worth adopting verbatim:

- From [gk-corpse-quality-processing]: clamp both quality sums at 0 after every mutation; bind one certificate per unit instance and price the re-open fee above the payout; ship the matching decor ladder in the same update as each cap raise and scale the payday superlinearly or add rating-gated sinks; make the courier cadence a function of elapsed day ticks alone; convert waste into progression via the red-immune automation seam.
- From [cf-08]: decide the trap question on day one (price the cheese above expected loot value or tax the loot table on trap kills; the source's documented numbers are 50-150 spike traps at one tin bar each for Ghorm, ~20 Galaxite Turrets at 15 bars + 4 parts each for Ra-Akar); creatures drop nothing from day one with add caps shipped in the same patch; consume the summon key atomically with spawn success and adopt the no-waste rule everywhere; anchor loot chests to generated ground after a lockout beat; never generate lootable blocks under gate structures; per-player gating on the guide NPC; publish HP scaling as clean multiples with infobox and table identical.
- From [digger-cf-06]: show saturation in the sell UI; floor-price dump override as the pressure valve; per-faction ledgers before any shared market goes live.
- From [ac-stalk-market]: if cross-market selling is allowed, ship the queue tooling as an owned feature with a sell-side fee or volume cap; scam surface (price promises "impossible without save-file hacking" per IGN) is evidence the market needs a server-side truth surface.

### 5.2 Day-one server invariants (priority order, from the RETENTION input; landing phases per 0.4)

| # | Invariant | Kills | Lives from |
|---|---|---|---|
| 1 | Server-authoritative RNG resolution, committed before client read, persisted per character-day across rejoins | 5.1 item 1, halves item 10 | M0 |
| 2 | Insulated unlock currency, earned by activity only | item 3 | M0 |
| 3 | Window caps on all repeatable payouts, counted server-side per account and per faction | item 4 | M0 |
| 4 | Non-tradable token pricing for cross-pool power; apply-once rule for faction-wide buffs | item 5 | M1 |
| 5 | Per-faction volume ledgers and owner-bound decay on shared assets | item 7 | M0 |
| 6 | Tier entry bound to the boss-kill event; purchasable substitutes are sidegrades | the currency half of item 8 | M2 |
| 7 | Costs at challenge time, mints on confirmed completion | the Ooblets and Tinkertown halves of item 10 | M1 |
| 8 | Conversion caps and PvP coefficients on stacking synergies; soulbind recycle streams | item 6 | M2 |
| 9 | Durable one-time clear flags for vendor stock | item 12 | M2 |
| 10 | Diminishing returns on meter relief and draft-time charge landing | item 9 | M1 |

Cost note (owed, 0.3): the stack is per-row counters plus daily passes. The only sourced per-system cost figure in the payload is the market's one-volume-counter-per-SKU plus daily decay pass (digger-cf-06). No aggregate budget for invariants 1 to 10 exists in any source; engineering owes it before M0 ships.

### 5.3 Standing build laws (stated once, sourced in sections 1 and 2)

1. Resolve server-side and reveal nothing early (eggs, drafts, reward boxes).
2. Bind tier access to the gate event; purchasable substitutes stay sidegrade-only.
3. Every hard cap gets a surface-condition audit.
4. Paid-shortcut pricing, restated without the conflation: the minimum is 2.0x the honest path's cash component; the sourced precedent lands at 3.29x (140,000 vs 42,500, hand-checked) for a calendar-locked checklist. Rule: price at 2.0x minimum, tune toward 3.0x to 3.3x when the honest path is calendar-locked; the shortcut buys time and keeps the social reward mass exclusive.
5. Luck modulates opportunity tables; content tables stay outside the scalar.
6. Production requires attendance; upkeep resists purchase.
7. Decay curves self-heal; demand coupling is the day-one fix for bonus-price rules, since punishment debuffs drew backlash in the source.
8. Publish the economy table and price processed goods in it (with the 1.4 completed-divisor formula, verified against seven of eight recorded rows).

### 5.4 Owed and flagged register (load-bearing unresolved items, per finding)

A builder treats every row here as a placeholder. None of these numbers may be cited as sourced constants. Items marked NEW arrive from this revision's cold-read pass or its hand arithmetic.

| Finding | Owed / flagged |
|---|---|
| [cf-02] Palworld breeding | Clean-inherit table quarantined (1.1): published 40/24/12/10, derivations 65/49/28/10 and 16/21/18/10, all three disagree; calibrate in-engine. Back-cross chain final-step arithmetic defect recorded (rule-consistent step is (570+630)/2 = 600); chain jumps rest on unfetched ranks. Breeding Farm workload 150 vs 15,000 across wikis; Ancient Hatchery workload 10,000 vs 1,000,000; Egg Incubator tier 10 vs 7. Egg-cycle pacing (5 minutes vs productivity modifiers) unresolved. Research tree: named handiwork nodes sum to +20, recorded cap +35, 15 points unlisted (NEW). Official Pocketpair patch notes unfetched (Steam hub returned navigation chrome); patch lines stand on wiki version histories. IV numbers rest on one page quote plus a community test. Full per-species rank table unfetched (10 samples verified). Ranch production intervals absent, so the AFK cake chain's hourly output is unknown. "Anubis via Rushoar + Blazamut" unverified (carried as suspect); same-gender glitch quote retracted by the digger after a zero-byte grep. Press single-source rows (InvenGlobal 349-ways, Game8 post-1.0 pairs) un-cross-checked. WebSearch rate-limited mid-session. |
| [digger-cf-21] Temtem | Launch-era breeding-exploit ban wave is community-recorded; the Reddit record stayed unread (bot-blocked). Patch fixes 0.5.15 and 0.7.3 are the cited evidence. |
| [digger-cf-01] Palworld labor | Numeric SAN drain rates, depression threshold, per-tick recovery, per-level work-speed multipliers, monitoring-stand hardmode multipliers all unverified (a Reddit thread's numbers were discarded after a revision-history check); the patch raising the base cap 25 to 30 was not located; world-slider ranges unfetched. |
| [digger-cf-05] Stardew luck | Per-table buff-equivalence tension recorded in 1.10 (1 point = 1x daily max on Skull Cavern and fishing treasure; 0.4x on the mines; the wiki's "+2 buff" line is loose prose over these) (NEW). Fortune Teller tier boundary floats secondhand (two consistent reads, raw table never seen); slot machine percentages absent from the Casino page; before-midnight sleep luck bonus unconfirmed on every fetched page; Lucky Ring Skull Cavern drop rate is a pass-1 claim unverified; garbage base drop percentage and exact formula absent; player community threads unfetched; decompiled code never fetched, all code references wiki-cited secondhand. |
| [ac-stalk-market] turnips | NH minimum sell price 9 vs 20 bells unresolved, two sources vs one (introduced at 1.6). Backwards-time-travel price behavior straddles the 1.2.0a patch boundary; Nintendo patch notes never fetched. The Ninji tweet thread itself unfetched after exhaustive attempts (Wayback CDX, nitter, API search); the datamine is instead triple-sourced from fetched pages. Constants come from community reverse-engineered code with a self-declared 32-bit ARM float-fidelity caveat. Reddit r/ACTurnips fee ban attested only via IGN (reddit JSON login-walled). turnips.exchange deeper behavior unreadable (SPA shell only); the 120-visitor cap figure is uncitable chatter. Per-title disposal fees beyond NL's 400 unfound. GC [70,130) range reconciled by integer truncation, filed resolved. |
| [digger-cf-06] Slime Rancher | SR2 floor semantics self-conflicted as recorded: "approximately half price at full saturation" vs the worked midpoint floor (base 15, minimum 20, floor 17); working reading adopted is the midpoint; re-fetch owed (NEW, 1.5). Per-corral hard slime capacity: no page states a number. Overgrowth, Docks, and Lab purchase prices unfetched (Overgrowth page carries none). SR1 plort names for the middle table tiers unnameable (names render as images). The tofu-largo 20-30k exploit is player-named, undocumented. SR2 Market Link and drone specifics unfetched. Silo and Vacpack capacities unfetched. Pond production-halt slime-count threshold unnumbered. |
| [digger-cf-04] Stardew bundles | Cart price formula absent from the page (bands observed, multiplier unstated). Slot counts beyond the Artisan 12-shown/6-slots example unstated. Remixed Bundles tables skimmed by grep only. JojaMart stripped lines 300-443 unread. Copper Pan delivery step unverified. Fish Shop (boat materials) unfetched. Speedrun and forum threads on route choice unreached; the abuse account rests on wiki patch history and the wiki's own strategy notes. |
| [digger-cf-13] Portia | B-tier city Blender row (RP 32-34) contradicts the 0-RP city law on the same wiki. Abandon and fail penalties unnumbered anywhere. Two Verify-flagged figures ride through: missed-playdate ~-30 RP, Hotfix 1.1 Higgins weekend gains. Commissions posted per weekday (board width) stated nowhere. Inspection reward table carries the wiki's own stub flag. Town-reputation page resolved to a 27-byte stub. Reddit threads 403-blocked. Per-character gift tables unexpanded. Changelist pages unfetched. |
| [gk-corpse-quality-processing] | Payday formula tension: 3 copper : 1 rating base gives 600 at 200 rating against a fetched 3,000-4,000 claim; church-rating donation bonus undocumented; the max-rating editor's measured 1.5 gold per payday deepens it. Surgeon's Mistake odds: zero percentages published. Organ roll ranges inconsistent across wiki pages (2R/1R+1W/2W vs +/-3 vs guides' -2R/+3W); possibly stage-partial. Sin_shard wiki page missingtitle; shard numbers come from two mutually consistent Steam guides. Courier cadence micro-rules are a single editor's claims. Every number is wiki- or guide-reported; none verified against game files. |
| [digger-cf-26] Monster Sanctuary | Egg-roll distribution under-specified as recorded: the all-uncollected case accounts for 1/4 of the mass and the "50-50" referent is unstated; the Monster_Eggs page needs a re-fetch before implementation (NEW, 1.3). Post-incident settled Shield Burst value not found; matchmaking top-3-plus-gear rating is per the dev's own patch note. |
| [cf-08] Core Keeper | Nimruza infobox HP (114160/228320/342480) disagrees with her rendered table row (124913/249826/374747-equivalent values as printed). Hive Mother 8-player rows cut off mid-extraction. Awakened Azeos 5-6 minute cooldown inherited by inference. Omoroth figurine history line says "decreased" while raising the number; cause unknown. Official wiki cross-check resolved negatively: wiki.gg empty (0 articles), atma.gg 403 Cloudflare. Steam and Reddit threads unread; community abuse picture rests on two fetched Gamepur guides plus wiki Tips and History. |
| [cf-20] Chained Echoes | Red-zone magic damage 1.5x (fan decompile) vs 125% (guide), unresolved. Per-attack gauge deltas and zone boundaries unpublished. "Punishes overkill" appears in no source read; the mechanic identification is the finding's own mapping. |
| [digger-cf-15] RimWorld | Catharsis magnitude +30 in prose vs +40 in the moodlet table row; def-level confirmation owed. |
| [digger-cf-14] Frostpunk | The 24h discontent-immunity duration on the juggling loop is the wiki author's estimate ("24h probably"); named band labels and per-law numeric deltas unfetched. |
| [digger-cf-16] ONI | The morale-upkeep sentence in section 2 item 21 is the finding's own compression of the mechanic; the per-stat game semantics behind it are unverified (NEW). |
| [cf-28] Palia | Renown totals conflict as recorded: 41 purchases at 100 each computes to 4,100 against the recorded "4,000 total"; one figure is off (NEW). Star-quality sell multiplier implied at 1.5x by two samples, stated on no page. Plots are one-time purchases on every fetched page; a rent mechanic needs a rent-native reference dig. Bot ban wave unfetched (search rate-limited). |
| [digger-cf-12] Necesse | Money-farms page self-flags as outdated; 15-coin and 75-per-minute figures need reconfirmation. Visitor cadence (5-10 min spawn / 8 min stay / 4 min leave, ticket weights) comes from a mod description quoting vanilla defaults. |
| [cf-29] Travellers Rest | The "+4 reputation per customer per unique line" figure is first-pass-only, no second source; provisional, calibration-bound (NEW, 1.13). Distillery unlock reads level 5 on one page and 11 on another; pick and verify. Inventory-cap figures excluded after a 403. |
| [kynseed] | Wheel slice odds, surgeon-mistake percentages, per-crop grow days, friendship point thresholds: absent from every fetched page. |
| [digger-cf-24] Dinkum | Licences wikitext carries the wiki's own Under Review flag. Time-travel reroll claims carried zero quoted evidence. Console commands are dev-shipped and therefore precedent for client-authority risk. |
| [tinkertown-dungeon-loot-shop-stock] | The earn-rate curve for silver/gold was unfetched, so the 3-13x price spread has no time-to-earn grounding. The loop lives in Tinkerlands, a separate title; Tinkertown ships zero shops. |
| [cf-19] Cassette Beasts | Shop purchase prices for tapes and upgrades 404'd. Sticker-attribute probabilities unfetched. |
| [digger-cf-03] Stardew crops | Ancient Fruit ROI row unreproducible from its recorded cells (sell number never carried; ~57.14 unexplained by the completed divisor formula); the Agriculturist profession percentage unfetched (NEW, 1.4). |
| [digger-cf-11] Craftopia | The ~27M gold/hour automation claim is dated (Sept 2020, pre-rework). |
| [digger-cf-10], [cf-22], [cf-23], [digger-cf-25], [digger-cf-07] | No additional load-bearing owed items beyond what sections 1 to 3 carry; the Niche counter numbers, Ooblets caps, Sun Haven tiers, and gordo thresholds stand as recorded by their findings. |

---

## 6. Closed bibliography (closed over the delivered payload)

Provenance rule: every source below was fetched and read by the digger session that filed the finding, as recorded in the finding's own sources and evidence fields. This seat read the finding texts handed to it in the ask and none of the underlying pages; no entry here is a claim of first-hand fetch by the assembler.

Audit-scope statement (closing the cold-read overstatement): the closure claim covers exactly what the payload delivered. For 8 findings the payload carried full source lists (the deep dives); for 10 more it named specific pages; for the remaining 12 it carried verdict, game, page counts, and inline citations with no page list. Source-level audit is possible only where pages are named below; for the other 12 findings the registry row plus the finding's inline citations are the entire provenance this document can attest.

**Deep-dive findings (full source lists as recorded in the payloads):**

- [ac-stalk-market] Animal Crossing Stalk Market, clone. nookipedia.com/wiki/Stalk_Market, /Turnip, /Daisy_Mae, /Joan, /Time_travel, /Red_turnip, plus Item pages: Turnips (New Horizons), Spoiled_turnips (New Horizons), Red_turnip (Wild World), Spoiled_turnips (Wild World); raw.githubusercontent.com/mikebryant/ac-nh-turnip-prices (predictions.js, README.md); api.github.com/repos/mikebryant/ac-nh-turnip-prices; raw.githubusercontent.com/ACreTeam/ac-decomp m_kabu_manager.c; animalcrossing.fandom.com/api.php White_turnip (plus disambig chain Turnip, Turnips, Turnip_(disambiguation)); the Edricus findings doc (docs.google.com, mobilebasic, 353,747 bytes); ign.com Animal Crossing turnip black market article; turnips.exchange homepage; web.archive.org CDX queries for twitter.com/_Ninji/status and nitter.net/_ninji/status plus two fetched archived statuses (both unrelated, 0 turnip matches); nookipedia api.php search; html.duckduckgo.com search page; old.reddit.com r/acturnips JSON (login-walled).

- [digger-cf-06] Slime Rancher market + corral, reskin. slimerancher.fandom.com: Plort_Market (Slime Rancher), Plort_Market (Slime Rancher 2), Corral, Agitation, Hunger, Pond, Coop, Chicken_Breeding, 7Zee_Rewards_Club, The_Ranch, The_Grotto, The_Overgrowth, Garden, Range_Exchange, Market_Link; gaming.stackexchange.com/questions/283639; steamcommunity.com plort-market search page and threads 3182216552781841410, 152390014790042677.

- [cf-02] Palworld breeding, reskin. palworld.fandom.com: Breeding (wikitext receipt), Cake, Breeding_Farm, Egg_Incubator, Passive_Skills, Alpha_Pals, Pal_Eggs, Ranch, Ancient_Hatchery, Monitoring_Stand, Egg; palworld.wiki.gg: Breeding (two passes), Cake, Egg_Incubator, Breeding_Farm, Ranch, Condensation, Ancient_Hatchery, Large-Scale_Electric_Egg_Incubator; invenglobal.com/articles/18731; game8.co/games/Palworld/archives/440029; store.steampowered.com news hub (chrome only); wiki.gg block-page receipt on disk.

- [digger-cf-04] Stardew bundles vs Joja, clone. stardewvalleywiki.com: Community_Center, Bundles, Joja_Community_Development_Form, JojaMart, Traveling_Cart, Movie_Theater, Version_History, Achievements, Perfection, Remixed_Bundles, Bus, Greenhouse, Minecart, Fish_Tank, Crafts_Room (all fetched, HTML-stripped, read per the finding's line map).

- [digger-cf-13] Portia commissions, clone. mytimeatportia.fandom.com via MediaWiki API: Commissions, Workshop_Rank, Relationship, Skill, Antoine, Presley, Higgins, Universal_gifts, Gift_preferences, Commerce_Guild, Inspection, Portia_Times, Data_Disc, Workshop, Reputation (27-byte stub); missingtitle pages: Inspections, Municipal_commission, Commission_board, Gratitude_gift, Abandon; steamcommunity.com/sharedfiles/filedetails/?id=1320333387 (411,461 bytes, stripped and grepped); reddit 403-blocked.

- [gk-corpse-quality-processing] Graveyard Keeper corpse chain, clone. graveyardkeeper.fandom.com via api.php: Sermon (Prayer redirect), Preparation_place, Morgue, Corpse, Donkey, Church, The_Graveyard, Zombie, Embalming_table, Souls_room, Faith, Days, Breaking_Dead, Game_of_Crone, Better_Save_Soul, Burial_certificate, Salt, Zombie_juice, Resurrection_table; missing titles: Day, Energy, Grave, Sin, Sin_shard; steamcommunity.com guides id=2275207503 and id=2837430236 (fetched, sectioned, read); reddit gl28xq unreadable (login wall / 403).

- [digger-cf-05] Stardew luck, clone. stardewvalleywiki.com: Luck, Television, The_Mines, Skull_Cavern, Fishing, Casino, Sleep, Special_Charm, Garbage_Can, Panning, Crops, Trees, Cooking, Lucky_Lunch, Magic_Rock_Candy, Ginger_Ale, Banana_Pudding (404s: /Garbage, /Garbage_Cans, /Fortune_Cookie); mouseypounds.github.io/stardew-predictor.

- [cf-08] Core Keeper biome gates + boss keys, reskin. core-keeper.fandom.com rendered via API: Omoroth_the_Sea_Titan, Ra-Akar_the_Sand_Titan, Nimruza, Glurch, King_Slime, The_Hive_Mother, Ivy, Morpha, Igneous, Atlantean_Worm, Urschleim, Druidra, Crydra, Pyrdra, Core_Commander, Haunted_Hive_Mother, Awakened_Azeos, Mining, The_Passage, The_Core, Crystal_Skull_Shard, Mysterious_Idol, Slime_Oil_Idol, Crown_Summoning_Idol, Hive_Mother_Summoning_Idol, Core_Commander_Summoning_Idol, Large_Golden_Egg, Corrupted_Sap, Profane_Override, Primeval_Slime_Cell; pass-1 cached wikitext: Biomes, Bosses, Statues, Great Wall, Ghorm's Horn, Stolen Crystal Heart, Boss-summoning items, Ghorm Summoning Idol, Giant Slime Summoning Idol, Large Shiny Glimmering Object, Thumper, Malugaz Summoning Idol, Brood Void Neuron; gamepur.com Ghorm and Ra-Akar guides; corekeeper.wiki.gg api probe (0 articles); corekeeper.atma.gg probe (403).

**Findings with named pages (as carried in the ask's payload):**

- [digger-cf-01] Palworld labor + SAN, clone: palworld.fandom.com wiki, 16 pages; the Palbox page is the quoted attendance line's source.
- [digger-cf-03] Stardew seasons + ROI, clone: stardewvalleywiki.com/Crops, /Seasons, /Seed_Maker, /Keg.
- [digger-cf-24] Dinkum licences + request board, reskin: dinkum.fandom.com wiki, 8 pages.
- [cf-18] Terraria boss gating + ore tiers, clone: terraria.wiki.gg, 19 pages (Pickaxe_power named in the citation convention).
- [digger-cf-07] Slime Rancher gordos, reskin: slimerancher.fandom.com, 9 pages.
- [tinkertown-dungeon-loot-shop-stock] Tinkertown/Tinkerlands clear-gated stock, reskin: tinkerlands.fandom.com/wiki/Merchants and 4 more pages.
- [cf-23] Ooblets dance battles + seed farming, clone: ooblets.fandom.com/wiki/Dance_Battle and 8 more pages.
- [cf-29] Travellers Rest inn stock + upgrade pacing, reskin: travellersrest.wiki.gg, 10 pages.
- [digger-cf-12] Necesse settlers, reskin: Necesse wiki including the self-flagged money-farms page; the visitor-cadence mod description.
- [digger-cf-14] Frostpunk hope/discontent, reskin: Frostpunk wiki including the Advanced strategies page for the juggling loop.
- [digger-cf-15] RimWorld mood, reskin: RimWorld wiki Inspiration, Mental break, Thoughts pages.
- [digger-cf-16] ONI pressure + labor, reskin: ONI wiki including its own Exploit section.
- [cf-22] Niche genetics + mutation menu, reskin: Niche wiki surfaces plus the community forum thread carrying the quoted frustration line.
- [cf-20] Chained Echoes overdrive gauge, reskin: Chained Echoes wiki plus guides (the 1.5x vs 125% conflict sits across a fan decompile and a guide).
- [cf-28] Palia shared-respawn commodity economy, reskin: Palia wiki Housing_Plot, Housing_Slots, Housing_Add-ons, Trees, Currency, plus the etiquette page.
- [kynseed-generational-inheritance-skills-farm] Kynseed generational pass-on, clone: Kynseed wiki surfaces plus Steam thread quotes for the total-carryover record.

**Findings whose page lists were absent from the payload (registry row plus inline citations are the full provenance):**

- [digger-cf-10] Factorio throughput funnels, reskin: infinite-research curve per the finding; page list not carried.
- [digger-cf-11] Craftopia jobs + ages, reskin: Craftopia wiki surfaces per the finding; the 27M/hour claim's Steam guide named in the abuse record; page list not carried.
- [digger-cf-25] Sun Haven XP pools, clone: Sun Haven wiki surfaces per the finding; page list not carried.

**Finding registry (the RETENTION index's 29 rows plus gk; original labels preserved, body uses the alias law from section 0):**

| ID | Game or system | Verdict |
|---|---|---|
| digger-cf-01 | Palworld, labor + SAN | clone |
| cf-02 | Palworld, breeding | reskin |
| digger-cf-03 | Stardew Valley, seasons + ROI | clone |
| digger-cf-04 | Stardew Valley, bundles vs Joja | clone |
| digger-cf-05 | Stardew Valley, daily luck | clone |
| cf-06 (alias digger-cf-06) | Slime Rancher, market + corral | reskin |
| cf-07 (alias digger-cf-07) | Slime Rancher, gordo gating | reskin |
| cf-08 | Core Keeper, biome gates + boss keys | reskin |
| digger-cf-10 | Factorio, throughput funnels | reskin |
| digger-cf-11 | Craftopia, jobs + ages | reskin |
| digger-cf-12 | Necesse, settlers | reskin |
| digger-cf-13 | My Time at Portia, commissions + relationship | clone |
| digger-cf-14 | Frostpunk, hope/discontent | reskin |
| digger-cf-15 | RimWorld, mood | reskin |
| digger-cf-16 | Oxygen Not Included, pressure + labor | reskin |
| ac-stalk-market | Animal Crossing, turnips | clone |
| cf-18 | Terraria, boss gating + ore tiers | clone |
| cf-19 | Cassette Beasts, fusion + tape economy | clone |
| cf-20 | Chained Echoes, overdrive gauge | reskin |
| digger-cf-21 | TemTem, breeding + SV economy | clone |
| cf-22 | Niche, genetics + mutation menu | reskin |
| cf-23 | Ooblets, dance battles + seed farming | clone |
| digger-cf-24 | Dinkum, licences + request board | reskin |
| digger-cf-25 | Sun Haven, XP pools | clone |
| digger-cf-26 | Monster Sanctuary, eggs + skill trees | clone |
| kynseed-generational-inheritance-skills-farm | Kynseed, generational pass-on | clone |
| cf-28 | Palia, shared-respawn commodity economy | reskin |
| cf-29 | Travellers Rest, inn stock + upgrade pacing | reskin |
| tinkertown-dungeon-loot-shop-stock | Tinkertown / Tinkerlands, clear-gated stock | reskin |
| gk-corpse-quality-processing | Graveyard Keeper, corpse-quality processing | clone (deep-dive payload; absent from the RETENTION index row list, present in MECHANICS' 30-finding basis) |

**Method note.** First pass: zero fetches, zero commands, zero checks (the ask named none). Revision pass: arithmetic checks performed by hand during this revision, each shown with worked rows in place (1.4 crop-divisor verification, 7 of 8 rows reproduced; 1.5 SR2 midpoint vs half-price conflict; 1.1 back-cross final step; 1.10 buff-equivalence coefficients and charm percentage; 1.8 research-node sum; 2 item 9 Palia total; 5.3.4 shortcut multiple). No machine commands ran at any point in this session. The fetch and verification work behind each number belongs to the digger sessions named in each finding's sources and owed fields. Everything unresolved is in 5.4 or 0.3; nothing was smoothed over.
