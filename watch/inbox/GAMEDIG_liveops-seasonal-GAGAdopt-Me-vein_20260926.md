# GAME DIG WHEEL SPEC (liveops-seasonal-GAGAdopt-Me-vein, 30-game dig receipt, 2026-09-26)

# Liveops seasonal wheel spec (GAG / Adopt Me vein), revision 2

## 0. Provenance, inputs, checks, and revision history

**Inputs held.** Four artifacts: the MECHANICS section, the RETENTION AND ABUSE section, the deep-dive payload of 8 findings (`digger-ls-02-gag2-event`, `digger-ls-01-gag2-grow-deep`, `adoptme-trade-economy-rarity-tiers`, `ps99-huge-pet-dupe-economy`, `digger-ls-12-mm2-knives`, `digger-ls-14-fisch-rods`, `stealabrainrot-steal-windows-server-lock`, `digger-ls-30-growdonate-board`), and the revision-2 cold-reader report. Where the cold reader executed arithmetic, this revision re-executed it here rather than carrying the reader's outputs; every load-bearing number below was run in this session.

**Fetch posture.** The assembler ran zero web fetches. The diggers fetched and read their sources 2026-09-26/27 and recorded methods per finding (MediaWiki `api.php` after HTML 403/Cloudflare walls; Wayback for Arsenal; PullPush for Reddit; live Roblox APIs for PTFS and Hunters). Quoted strings are carried verbatim from the findings.

**Check 1.** Re-runs M0, the arithmetic verification block defined in the MECHANICS input (GaG2 growth curve at three ages, years-to-cap, Gold damping, fully-decayed multiplier, PS99 Ornate odds sum, RoCitizens XP total):

```
./.venv/Scripts/python.exe -c "import math; f=lambda a: min(1+0.0128*math.log(1+a/1800)**2.55,25); print('gag2 curve 30min',round(f(1800),4),'5hr',round(f(18000),4),'50hr',round(f(180000),4)); print('years to 25x',round(1800*(math.exp((24/0.0128)**(1/2.55))-1)/31557600)); print('gold damping on single-harvest',1+(10-1)*0.15); print('fully decayed multiplier',1-1*0.8); print('ps99 ornate odds sum',48+35+13+3+0.78+0.2+0.02); print('rocitizens xp to gold star',10+10+40+90+160+250+360+490+640+810)"
```

Output:

```
gag2 curve 30min 1.005 5hr 1.1191 50hr 1.6322
years to 25x 12561
gold damping on single-harvest 2.3499999999999996
fully decayed multiplier 0.19999999999999996
ps99 ornate odds sum 100.0
rocitizens xp to gold star 2860
```

Reproduces the GaG2 wiki curve table at the wiki's rounding (1.01 / 1.12 / 1.63), the 12,561-year cap claim, the 2.35 Gold-damped payout, the 0.2 fully-decayed multiplier, the PS99 Ornate odds summing to exactly 100, and the RoCitizens 2,860 XP total. Note: this check verifies the sum of the RoCitizens list and three damping values; it verifies neither the RoCitizens formula fit nor the Rainbow payout. Both are covered by check 3.

**Check 2.** Deep-dive payload verdict tally, re-run reproducibly (full command, pairs printed, no scratch file):

```
./.venv/Scripts/python.exe -c "pairs=['digger-ls-02-gag2-event:clone','digger-ls-01-gag2-grow-deep:reskin','adoptme-trade-economy-rarity-tiers:reskin','ps99-huge-pet-dupe-economy:reskin','digger-ls-12-mm2-knives:reskin','digger-ls-14-fisch-rods:reskin','stealabrainrot-steal-windows-server-lock:reskin','digger-ls-30-growdonate-board:clone']; [print(p) for p in pairs]; import collections; c=collections.Counter(p.split(':',1)[1] for p in pairs); print('total', len(pairs)); [print(k, v) for k, v in sorted(c.items())]"
```

Output: the 8 id:verdict pairs as listed, `total 8`, `clone 2`, `reskin 6`.

**Check 3.** Arithmetic audit pack over every number the cold read contested (exact script below; output quoted verbatim):

```
./.venv/Scripts/python.exe - <<'PY'
import math
print('dailies per level 80000/9000 =', 80000/9000)
print('mm2 box        ', 70+15+10+5+0.2+0.004)
print('bl regular     ', 62.25+30+7+0.5+0.25+0.0325+0.125)
print('bl lucky       ', 0+0+92.5+5+2.5+0.2+1)
print('cracked egg    ', 45+33+14.5+6+1.5)
print('pet egg        ', 20+35+27+15+3)
print('royal egg      ', 0+25+37+30+8)
print('av traits      ', 26*3+10+6.5+2.5+1.85+0.5+0.375+0.175+0.1)
print('jji spin       ', 70+20+7+2.75+0.25)
print('skibidi triti  ', 60+38.3+1.3+0.4)
print('skibidi hacked ', 55.5+40+4+0.5)
print('sf6 bands      ', 74.94+20.00+5.00+0.06)
print('ps99 cardpack  ', 40+35+21.7+3+0.3)
print('gold pays  ', 1+(10-1)*0.15)
print('rainbow pays', 1+(30-1)*0.15)
print('electric 0.33 vs rainbow 1/300 =', 1/300)
f=lambda a: min(1+0.0128*math.log(1+a/1800)**2.55,25)
print('day1', round(f(86400),4), 'day7', round(f(604800),4), 'day30', round(f(2592000),4))
print('tally < top:', 264354693100 < 300000000000, 'short by', 300000000000-264354693100)
seq=[10,10,40,90,160,250,360,490,640,810]
print('given sum', sum(seq), '| sum 10*(n+1)^2 n=0..9 =', sum(10*(n+1)**2 for n in range(10)))
print('fit max(10,10*n^2) n=0..9:', [max(10,10*n*n) for n in range(10)], 'sum', sum(max(10,10*n*n) for n in range(10)))
print('last-level share 810/2860 =', 810/2860)
pairs=[(25,56),(36,80),(54,120),(107,160),(183,275)]
print('cuts pct:', [round(100*(1-a/b),1) for a,b in pairs])
print('x40/9 predicts:', [round(100*((40/9)/N-1),1) for N in range(1,7)])
print('x4 predicts:   ', [round(100*(4/N-1),1) for N in range(1,7)])
print('drip weekly subset =', 35+140+20+2)
PY
```

Output (load-bearing lines): `dailies per level = 8.88888888888889`; `mm2 box 100.204`; `bl regular 100.1575`; `bl lucky 101.2`; cracked/pet/royal egg, AV traits, JJI spin, both skibidi crates, SF6 bands, and PS99 card pack all `100.0`; `rainbow pays 5.35`; `electric 0.33 vs rainbow 1/300 = 0.003333...`; `day1 1.4094 day7 2.1423 day30 3.0165` (reproduces the digger-ls-01 derived points); `tally < top: True, short by 35645306900`; `given sum 2860 | sum 10*(n+1)^2 n=0..9 = 3850`; `fit max(10,10*n^2)` reproduces the sequence exactly, `sum 2860`; `last-level share = 0.2832...`; `cuts pct: [55.4, 55.0, 55.0, 33.1, 33.5]`; `x40/9 predicts: [344.4, 122.2, 48.1, 11.1, -11.1, -25.9]` (matches the carried ladder exactly) vs `x4 predicts: [300.0, 100.0, 33.3, 0.0, -20.0, -33.3]` (matches nothing carried); `drip weekly subset = 197`.

**Census conflict, resolved by recount this session.** MECHANICS claims 30 findings at 5 clone / 24 reskin / 1 skip; RETENTION claims 29 at 5 / 23 / 1 with an executed grep tally. Recount of the two inputs as delivered: RETENTION's rollup table names 29 ids and omits `jji`, while RETENTION's own body cites `jji` three times (H8, the skip-adjacent guidance, and the conflicts register); MECHANICS cites `jji` throughout and states its verdict explicitly ("[jji, verdict reskin]" in its skip section); MECHANICS does not cite `digger-ls-09`, which sits inside RETENTION's 23-row reskin list. The union of cited ids across both inputs is exactly 30 distinct findings, and 5 clone + 24 reskin + 1 skip partitions it. Resolution: the corpus is 30 findings at 5 clone / 24 reskin / 1 skip; RETENTION's rollup dropped the `jji` row and undercounted its own header. This is a reading-based recount of in-conversation input text (no input files exist here to grep); it supersedes the revision-1 "delta filed as owed" note. The cold reader's `digger-ls-09` hypothesis is contradicted by RETENTION's own rollup, which already contains `digger-ls-09`.

**Verdict-label drift.** The MECHANICS input heads the mutation value ladder as CLONE citing digger-ls-01 plus digger-ls-02; the digger-ls-01 finding holds verdict reskin (digger-ls-02 holds clone). Numbers are unaffected.

**Revision 2 changelog.** Fixed in place: H1-H14 now defined in a hook register (4.0) and M0 glossed (check 1); W4 quest cadence corrected (8.89 dailies per level, executed; the input's "two dailies and change" gloss is wrong); R2 carries executed odds sums with the three violating tables flagged against the PRI shape; R5's WCUE rule softened to match its own counterexample; W3's ladder-completion claim corrected (tally is 35,645,306,900 short of the top rung, executed); R4's RoCitizens fit corrected to `max(10, 10 x n^2)` (the input's `10x(n+1)^2` sums to 3,850, executed) and Adopt Me's cut corrected to 33-55%; R3's law cross-reference fixed (15, active-play); W1 Eclipse durations disambiguated; law 12's premise rescoped to Roblox developers; W4/W5 attestation downgraded to carrier-only; W2 probability-model gap stated; raid spec lines (2), (6), (9), (10) given proposed definitions; tick-zero engineering requirements added; phasing, targets, kill criteria, currency anchor, and seasonal currency end-of-life added as marked proposals and owed decisions; Super Watering Can 300x flagged as an uncorroborated outlier; the 854/week drip figure marked unusable without a period table.

**Lane mapping used throughout** (stated in the inputs): the target game already runs VM currency, boon drafts, faction war, and a shared-respawn Pilgrim class. The wheel = the appointment clocks (R3/R6) wrapped around the seasonal window skeleton (W1), monetized through the pass and collection tables (W4, W5), stocked by the drip economy (W6), and gated by the abuse laws (section 5).

---

## 1. The wheel: cloned mechanics and their numbers

### W1. Seasonal window skeleton [CLONE; digger-ls-02; fetched and held]

The host system for everything else on the wheel: a server-synchronized day clock whose timed windows gate growth boosts, a value ladder, and a presence-gated special spawn.

**Day cycle** (Mechanics L471, Weather L4): 10 minutes total = 7:30 day + 0:30 sunset + 2:00 night. "Every active server experiences the same weather at the same time." A crop carries exactly one mutation at a time. The 2-minute night is also the theft window (R8).

**Day weather windows, Garden Valley** (Weather L101-156):

| Window | Duration | Chance | Effect |
|---|---|---|---|
| Rain | 5 min | 30.77% | 2x growth speed, revives plants |
| Lightning | 5 min | 23.08% | Electric 25x |
| Rainbow | 5 min | 15.38% | Rainbow 30x |
| Snowfall | 2:30 | 7.69% | Frozen 14x |
| Starfall | 2:30 | 7.69% | Starstruck 50x |
| Aurora | 2:30 | 7.69% | Aurora 1.5x |
| Sunburst | 5 min | 7.69% | Ignited 60x |
| Eclipse | 2 min trigger, 2:30 reset ceiling | 0% natural | Player-spawned only (Eclipse Bloom crop); Eclipsed 80x |

**Eclipse duration note** (cold-read fix): the carried sources give two numbers and this spec assigns them explicitly. The Eclipse Bloom trigger starts a 2-minute window; a harvest made during Eclipse resets the running timer to a 2:30 ceiling, silently and unattributed. The 2:30 figure is the reset ceiling, the 2-minute figure is the base duration.

**Night moon lottery** (Weather L37-43 vs L168-201): Time of Day table reads Normal 77 / Gold 13 / Rainbow 6 / Blood 2 / Mega 2; the Night Weathers table on the same page reads 77.45 / 12.75 / 5.88 / 1.96 / 1.96. The digger flags this internal contradiction as unresolved; pick one table and own it (5.3). Fall Harvest variant: 75.96 / 12.5 / 5.77 / 1.92 / Harvest 3.85.

**Presence gate** (Weather L326-330, verbatim): "The fewer people in the server, the lower the chance a gold/rainbow seed will spawn." and "A gold/rainbow seed cannot spawn if there are less than 2 players in the server." The Gold/Mega Seed pages add that odds rise in public over private servers. This is the proven reward shape for a shared-respawn class: it pulls solo players into crowded servers exactly when the lottery is live.

**Seasonal sub-world** (Fall Harvest): opened August 2, 2026, 60-day stay, its own Leaf currency with Robux packs priced identically to base Sheckle packs (5,000 for 10 R$ up to 100,000 for 200 R$), exclusive stock (Amber Cranberry at 0.07% restock), and its own quest loop: Cornucopia runs 5 daily quests with one guaranteed passive-type quest per day, including "Steal from People" targeting 3 to 15 victims. Ghoul Garden adds night-only brewing with a 5 to 55% failure ladder (Spirethorn 5% up to Night Shade 55%), ingredients consumed on fail, and a 10-second Cauldron Charm rescue window. **End-of-season currency handling is unspecified in the source and is a day-one decision for the wheel; see 4.5.**

**Player-triggered windows** (Eclipse Bloom page): harvesting an Eclipse Bloom starts a 2-minute Eclipse; harvesting during Eclipse silently resets the timer to 2:30 with no public announcement; stolen Eclipse Blooms trigger nothing. The Jandel Monkey pet summons random weather every 15 / 12 / 9 minutes by variant; the Wind Staff (2,000,000 Leaf or 399 R$, one per player) traps players in a 10-second tornado on a 10-minute cooldown.

**Patch cadence as content pipeline** (Update Log, digger-ls-01/02): 20 versions in 37 days from the June 12, 2026 public release; each weather+mutation rung shipped as one patch (1.01.0 Aurora, 1.05.0 Mega Moon, 1.10.0 Sunburst/Ignited, 1.15.0 Glow, 1.16.0 Eclipse/Eclipsed). Pre-update Admin Parties run 30 minutes before each patch with rewards every 30 Party Points to 600.

### W2. The reveal ladder (one buff per asset) [digger-ls-01 + digger-ls-02; probability model owed]

One mutation per crop. Base 1% mutate-on-harvest for standard crops, rolled at pickup with "1 final chance to adopt the mutation" (Mutations L10). Ladder, low to high:

| Mutation | Multiplier | Odds / trigger as carried |
|---|---|---|
| Aurora | 1.5x | Aurora window |
| Gold | 10x | 1% harvest (1/100), 0.1% growth (1/1000) |
| Frozen | 14x | Snowfall window |
| Amber | 20x | 5% per ripening fruit (Amber Cranberry) |
| Veil | 20x | 5% on planting (Shadow Dragon) |
| Electric | 25x | 0.33% harvest / 0.033% growth, lightning |
| Rainbow | 30x | 1/300 harvest, 1/3000 growth |
| Starstruck | 50x | Starfall window |
| Chakra | 60x | 20% on Kitsune-stolen fruit |
| Ignited | 60x | Sunburst window |
| Bloodlit | 60x | Blood Moon |
| Eclipsed | 80x | Eclipse window |
| Glow | 100x | Star Fruit plant beams |

**Probability-model gap (build blocker until resolved).** The carried table gives per-harvest odds only for Gold, Rainbow, and Electric; the window-gated rungs (Aurora, Frozen, Starstruck, Ignited, Bloodlit, Eclipsed, Glow) carry trigger text with no rate, and no held source states whether a window applies its mutation to every harvest inside the window, multiplies the base 1% roll, or rolls independently, nor how any of it interacts with the one-mutation-per-crop law. Three candidate models: (A) window-guaranteed application; (B) window multiplier on the 1% base; (C) independent roll with a priority rule (Fisch's priority-squeeze is the corpus analog). The lane mapping below uses model A semantics for boons (a boon entering a window receives that window's multiplier at exit), which needs no per-harvest rate; the literal-crop port stays unpriced until a re-dig resolves the wiki's intent. File in 5.3.

**Rate-identity flag.** Electric's 0.33% harvest sits against Rainbow's 1/300 = 0.3333% (executed comparison, check 3) for adjacent multipliers 25x vs 30x. One of the two rates is likely misattributed on the wiki; re-dig both before either becomes a build constant.

The content pipeline is the ladder itself: each patch added one rung. Lane mapping per the diggers: drafted boons receive window multipliers instead of harvest rolls.

### W3. The donation board, 2026 patch set [CLONE; digger-ls-30; fetched and held]

Four shipped iterations (Beanstalk 2025, Summer Harvest 2025, Beanstalk 2026 rerun Aug 29 to Sep 19 2026, Safari Harvest Nov 2025), plus Fall Market and Christmas Harvest variants. Players donate against an NPC's rotating request; a public board tracks contributions; a shared structure grows on a point goal and decays on a timer; repeat-commitment counters gate premium stock.

- **Server goal**: 900 points fully grows the Beanstalk. Gold variant replaces default at 7.41%, Rainbow at 3.70%. Grown stalk persists 20 minutes then decays; max 5 climb rewards per player per stalk; per-player contribution cooldown 15 minutes (2026).
- **Point curve per rarity** (Summer Harvest table): Common 1 / Uncommon 2 / Rare 3 / Legendary 4 / Mythical 5 / Divine 6 / Prismatic 7; mutation bonus +1 Silver, +2 Gold, +3 Rainbow.
- **Personal reward gates** (Summer): 10 / 500 / 2,000 / 5,000 / 8,500 / 11,000 / 14,000 points, Common through Prismatic.
- **Contribution-count gates**: portal at 7 helped growths (2026; 6 in 2025), shop items at 2 through 9 helped growths, Skycastle Fence at 12; Fall Market 2025 proves count gates scale to 50 for multi-week seasons.
- **Request rotation**: Jack's trait refreshes hourly (2026); Safari Joyce and Fall Market's Harvest Spirit every 30 minutes; Summer Harvest ran a 60-minute cycle with a 10-minute submission window.
- **Sink economics**: 2026 manual restock base 1,000,000,000 Sheckles, tripling per purchase, 24-hour reset, auto restock every 15 minutes. 2025 shipped the hole: 500,000 base tripling with no cap and a contribution reset on rejoin; whales emptied premium stock. Import the 2026 set verbatim.
- **Sub-tracks**: Jack leveling at 25/75/175/300/450 NPC points cuts regrow cooldown 15 to 10 minutes; Giant friendship thresholds 0/20/50/90/140/200/270 with food points Common 2 through Transcendent 9, no feeding cooldown; Giant's Basket pays 30 deliveries with pick 1 of 3 rewards and a 39 R$ reroll, tiered Humble 1-10 / Hearty 11-20 / Giant's Favour 21-30; Gold Cauldron takes 30 to 75 KG of Gold-mutated plants per Beanpod Chest on a 3-minute cooldown.
- **Global tier** (Safari Harvest): individual reward every 500 contributed points; global milestone ladder 250,000 up to 300,000,000,000 points unlocking weathers and compressing the event-shop cooldown 60 to 10 minutes. Final community tally 264,354,693,100. Executed comparison (check 3): the tally is 35,645,306,900 short of the 300,000,000,000 top rung, and the wiki itself marks the 280,000,000,000 Safari Tour rung unreached. The tally proves the server ran the ladder through the 255,000,000,000 rungs. (Revision 1 repeated the RETENTION input's "ran the whole ladder" gloss; corrected here.)
- **Documented 2025 exploits to design out**: hoard-and-dump cheap high-growth crops (the wiki's own Strategies section coaches Tomato hoarding with Pack Bee stockpiling), first-donation attribution that punished early contributors (personal points started only after a player's first drop), and rejoin point resets. Free-riding the climb is by design and stays.

### W4. The pass curve [CLONE; digger-ls-07; ATTESTATION: carrier-only]

Attestation note (cold-read fix): digger-ls-07 is cited through the two synthesis inputs; the assembler holds no source array for it. The constants below are attested at carrier strength. The reader's executed spot checks found the carried arithmetic internally consistent; treat them as design inputs and re-dig before they become build constants.

- **XP per level: 80,000 flat, levels 1 through 200** (fandom Season XP table, corroborated by GamesRadar per the MECHANICS input). The flat curve converts the pass into a fixed per-level budget.
- **Quest cadence**: 9,000 XP per daily quest, 17,500 per weekly. Executed (check 3): 80,000 / 9,000 = 8.89 dailies per level. The MECHANICS input's editorial gloss "two dailies plus change per level" is contradicted by its own numbers by a factor of about 4.4 and is dropped from this spec; the weeklies-as-catch-up role is likewise unquantified in the held material. What stands: the per-level cost, the per-quest payouts, and the ratio.
- **Self-funding pass**: 800 V-Bucks cost, 800 awarded on completion (Epic's pricing page per the input); free track carries 300. 100 rewards per pass, 85 cosmetic; mini seasons cut to 50 levels.
- **Skip pricing**: 150 V-Bucks per level, purchasable to 200.
- **Win-back lever**: Supercharged XP doubles the rate until 500,000 XP banked, then turns off. Aim it at lapsed players at season start.
- **Caps must ship with channels** (the documented failure): Save the World weekly cap 4,000,000; Creative roughly 300,000 XP/day wall with full disablements for the biggest farm maps; Accolade payouts (Victory Royale 80 / Elimination 150 / Landmark 1,000 / Named Location 8,000) arrived post-hoc.
- **Event spikes for calibration** (The Verge, Polygon per the input): Marshmello 10.7M concurrent (2019), Travis Scott 12.3M concurrent / 27.7M uniques across five shows (2020), chapter finale 15.3M single day (2021), Fortnite OG 44.7M single day (2023).

### W5. Collection event + shard pity [CLONE; digger-ls-08; ATTESTATION: carrier-only]

Same attestation downgrade as W4: carrier strength; re-dig before build constants.

- **Set**: 24 event-limited cosmetics from 700-AC event packs with a no-duplicate guarantee (EA FAQ: "Drop Rate per Item increases as you acquire Event Items as there are no duplicates"). Owning all 24 unlocks a free Tier 1 prestige skin; after the event the skin sits in the Mythics Shop for 150 Heirloom Shards, the permanent price floor.
- **Derived full-set ceiling**: 24 x 700 = 16,800 AC (arithmetic on carried prices; PC Gamer's Iron Crown floor was $170 including the 3,500-coin heirloom).
- **Shard economy**: 0.045% drop from standard packs, drops do not consume the pack, **500-pack hard pity**. Secondary: 30-pack legendary pity; standard odds 100% rare-or-better, 24.8% epic-or-better, 7.4% legendary. Base mythics stay uncraftable, so shards and events remain the only two faucets.
- **The one piece to invert**: event packs "do not count towards the Bonus Heirloom Shards" (EA FAQ). That pity exclusion is the documented grievance behind the Iron Crown 2019 revolt (community-computed ~$170 floor printed by PC Gamer; boycott line "Do not spend money on these new packs") and the forced redesign. Let event purchases advance the master pity.
- **Event-pack odds disclosure shape** (SF6 packs): 74.94% Epic band (4.40% per item), 20.00% Legendary (2.22%), 5.00% Iconic (0.63%), 0.06% Mythic. Executed (check 3): the band sums to exactly 100.0; this is the developer-published disclosure shape the wheel copies.

### W6. Trait reroll table + pity + drip economy [CLONE; digger-ls-19; ATTESTATION: carrier-only]

**Trait odds (both AV wikis agree; executed sum check 3: 99.99... = 100.0 at rounding):**

| Trait | Chance |
|---|---|
| Range / Swift / Vigor | 26% each (78% combined junk floor) |
| Scholar | 10% |
| Marksman | 6.5% |
| Fortune | 2.5% |
| Blitz | 1.85% |
| Solar | 0.5% |
| Deadeye | 0.375% |
| Ethereal | 0.175% |
| Monarch | 0.1% |

- Flat cost: 1 reroll per use on any unit.
- **Pity** (post Update 7.0, cut from 2.5x to 1.5x base): Monarch 1,500, Ethereal 858, Deadeye 400, Solar 300 rerolls per unit.
- **Monarch tradeoff, unresolved pair (cold-read fix, filed 5.3).** The carried prose says +300% damage at one placement, while the carried DPS ladder (+344.4 / +122.2 / +48.1 / +11.1 / -11.1 / -25.9 percent at N = 1..6 placements) fits a x40/9 (about 4.44x) one-placement multiplier exactly (executed, check 3), i.e. +344.4% at N=1. The x4 (+300%) reading predicts +300 / +100 / +33.3 / 0 / -20 / -33.3 and matches nothing carried. Both numbers ride the same source line and the derivation is not held; re-dig before treating either as the build constant.
- **Drip economy: the 854/week figure is unusable as carried (cold-read fix).** The page-chart figure "roughly 854 rerolls per week across channels" mixes unstated periods: login calendar 35/week; challenges 1/3/20 (regular/daily/weekly); battle pass 85 free / 170 premium (per season); achievements 420 lifetime; level milestones 206 lifetime; tournaments 2 to 100 (period partially stated); PvP shop 40, Rift shop 50, Boss Event shop 40 (periods unstated); new/returning 220 each (one-time); codes 20 to 100; Elemental Towers 300 (period unstated). A weekly budget is not constructible from this list: the items with stated weekly-compatible cadences sum to about 197/week under one labeled assumption set (login 35 + daily 20 x 7 + weekly 20 + tournaments floor 2; executed, check 3). Marked unusable for economy sizing until a per-channel period table is re-dug; the wheel's drip design (4.2, W6 row) must derive its own budget and publish it.
- **Trading rules that keep the economy honest**: both traders level 50+; traded units keep stats/levels/ascensions but traits and pities are removed (blocks reroll-pity fishing on a cheap unit); only Robux-shop-purchased rerolls are tradable (farmed rerolls stay untradable, confining any flood to the channel with a payment audit trail); trade-history viewer in the trading menu.

---

## 2. Reskins: keep the math, change the skin

### R1. Growth-clock family [digger-ls-01, reskin; fetched and held]

- **Infinite growth**: `multiplier = min(1 + Coefficient[ln(1 + age/Timescale)]^Exponent, MaxMultiplier)`; defaults 0.0128 / 1800 s / 2.55 / 25x cap. Worked points: 30 min 1.01, 5 hr 1.12, 50 hr 1.63; cap reachable in 12,561 years (checks 1 and 3). Derived points on the same constants: day 1 = 1.4094, day 7 = 2.1423, day 30 = 3.0165 (executed this session, check 3; matches the digger's derivations). This is the keep-playing-forever curve: enormous logged hours buy small visible gains.
- **Decay**: `DecayPenalty = 1 - clamp(decayFraction, 0, 1) x 0.8`; fully decayed sells at 20%; watering restores value and connected fruits; decay skips mutated crops.
- **Sell formula**: `floor(SellValue x SizeFactor x SizeMultiplier x MutationMultiplier x DecayPenalty x FriendsBonus)`. Single-harvest damping `effectiveMut = 1 + (raw - 1) x 0.15`: Gold 10x pays 2.35x (executed, check 1); Rainbow 30x pays 5.35x (executed, check 3). FriendsBonus = 1 + friends x 0.1 per friend on the server, capped at +70% per the Sheckles page; it sits adjacent to the documented alt-account techniques and the wiki records nobody farming it, so treat as a flag. Size exponents 2.5 default / 1.9 Mushroom / 1.75 Bamboo; knee 5, tail exponent 1.5; doubling rolls 1% at luck 1 scaling to 5% at luck 100. Carrot price floor 4; Mushroom sells at 0.5x.
- **Growth-speed multipliers**: Rain 2x; sprinklers 1.5x / 2x / 3x / 4x / 5x (Common to Super), all 2-minute duration, same-type never stack, different types do.
- **Outlier flag (cold-read fix, filed 5.3):** the Super Watering Can at "300x" temporary growth plus decay healing rides a single carried line (Gears L337) against every other multiplier in this spec (2x rain, 1.5-5x sprinklers, 1.63x at 50 hours on the infinite curve). If real it is the most economy-distorting item in the document. Excluded from build constants pending re-dig; import nothing at that magnitude silently.

### R2. Rarity pyramids (pick a shape, one per surface)

Sum-check law for this section (cold-read fix): executed in check 3. Tables that sum to exactly 100.0: Adopt Me's three permanent eggs, the AV trait table, the JJI spin, both skibidi crates, the SF6 bands, the PS99 card pack. Tables that fail the 100-sum as carried: MM2 box (100.204), Blue Lock regular (100.1575, with a non-monotonic tail listing 0.0325 before 0.125), Blue Lock lucky (101.2). Section 5.2's PRI shape ("numeric odds displayed pre-purchase summing to 100%") is a hard gate: any of these three tables imported as printed violates the disclosure shape this spec itself cites. Before import, renormalize to a disclosed 100-sum or re-dig the true rates; the violations are recorded in 5.3. A plausible reading for MM2 (its four main tiers already sum to 100 before the godly and chroma rows) is that one of the printed rungs is approximate; unresolved from held material.

- **MM2 box pyramid** [digger-ls-12; fetched and held]: Common 70 / Uncommon 15 / Rare 10 / Legendary 5 / Godly 0.2 / Chroma 0.004, identical across every box (a global rebalance moved commons 60-to-70, uncommons 25-to-15). Executed sum: 100.204; flagged above. A box costs 1,000 coins against a 40-per-round faucet cap (50 with Elite), so one box = 25 capped rounds. Salvage ladder de-ranks loss: x2 shards per weapon of its tier, 12 shards per tier step upward, 20 Legendary shards = the Seer (players salvage 10 legendaries; was 5 before the doubled recipe). The wiki names its own lineage: "The recycling feature was inspired by CS:GO's trade-up feature" (Crafting.txt:327).
- **JJI spin pyramid** [jji; carrier-only; sums to 100.0 executed]: 70 / 20 / 7 / 2.75 / 0.25 over a 24-item pool. Two valves to clone: targeting a specific innate doubles its odds, and a confirmation prompt before rerolling away a top-tier roll.
- **Two-currency pyramid** [digger-ls-18, Blue Lock; carrier-only; sums fail as carried]: regular spin (2,500 Yen) at 62.25 / 30 / 7 / 0.5 / 0.25 / 0.0325 / 0.125 (executed 100.1575; tail order non-monotonic) vs Lucky spin at 0 / 0 / 92.5 / 5 / 2.5 / 0.2 / 1 (executed 101.2). The Lucky currency deletes the two bottom tiers and concentrates weight in Legendary-or-better. The Flow track carries the only documented pity: 50 spins guarantees Legendary-or-better. The LOCK toggle protects the equipped style. Flagged drift: Master odds 0.0325% vs 0.0175% across pages. Import only after renormalization or re-dig.
- **Egg table by price** [adoptme; fetched and held; all three rows sum to 100.0 executed]: Cracked Egg 350 Bucks at 45 / 33 / 14.5 / 6 / 1.5; Pet Egg 600 at 20 / 35 / 27 / 15 / 3; Royal Egg 1,450 at 0 / 25 / 37 / 30 / 8; the 750-Buck limited band runs 3 to 5% Legendary; Golden/Diamond eggs at 100% Legendary as terminal rewards. "Hatch Now!" at 35 R$ per egg, repeatable without limit, is the skip-hatch monetization shape.
- **Event crate ladders** [skibidi; carrier-only; both sum to 100.0 executed]: Tri-Titan Crate 250 gems at 60 / 38.3 / 1.3 / 0.4; Hacked Crate 500 gems + 150 event Bits at 55.5 / 40 / 4 / 0.5; tier ladders per event (Bit 76/18/5/1 up to Emerald 65/28/6/1). Luck Potion boosts any unit under 10%. **Cautionary calibration**: Titan Clockman tested at 0.5%, shipped at 0.005%, walked back to 0.02% after backlash the Update Log itself calls "nerfed due to greed."
- **Tier bands at scale** [digger-ls-15, Sol's RNG; carrier-only]: Basic 1/1-1/999 up through Transcendent and Dimensional to 1/12,500,000,000; luck is a coefficient on the denominator (`List Value = floor(Base Value / Luck)`), every 10th roll doubles luck, gear adds up to +22, one-roll potions add +50,000 to +700,000.

### R3. Appointment clocks (the wheel's ticks)

- **Global shared stock** [digger-ls-05, carrier-only]: Blox Fruits dealer restocks every 4 hours, identical worldwide, minimum 3 fruits; the Mirage advanced dealer runs 2 hours, minimum 7, boosted Legendary chance. GaG2 shops restock every 5 minutes on globally shared stock with rarity odds from Carrot 100% down to Star Fruit 315,000,000 Sheckles at 0.12% [digger-ls-01; fetched and held]; Fruit Stock price multipliers 0.8x to 4x refresh every 10 minutes. One synchronized clock makes every player read the same shop at the same instant. **Engineering requirements for the wheel's version: see the tick-zero box in 4.1.**
- **World spawns**: hourly, 45 minutes on weekends, 20-minute despawn [digger-ls-05]. Weekend acceleration pulls weekend sessions.
- **Famine-feast flagship spike** [digger-ls-05]: pull the flagship from sale (Dragon, Update 23), let scarcity compound through trading, relaunch reworked at +92.3% Robux / +328.57% Money (Update 24, price 2,600 to 5,000 R$). The next day set the Roblox single-game record, 2,781,531 concurrent. The proven liveops lever in the corpus.
- **Limited rotation retirement** [adoptme, digger-ls-12]: Gumball eggs leave after 57 to 252 day windows and become trade-only, so yesterday's pulls appreciate. MM2's endpoint: off-platform value lists run a ~50,000-to-1 spread (Seer 3 to Chroma Travelers Gun 150,000) and the wealth sits in retired event items.
- **Real-time timers** [digger-ls-25 RoCitizens, carrier-only]: investments 1 hour / 4 hours / 1 day / 1 week; daily login ladder 100/250/500/1,000/2,000/3,000 that hard-resets to $100 on a missed day. [digger-ls-11 Arsenal, carrier-only]: daily shop reset 1 AM PST, one free spin ticket per day, 12-to-25-day login ladders with 25 R$ missed-day catch-up.
- **Scheduled live events**: Steal a Brainrot runs "Admin Abuse" Tuesdays 6pm ET and Saturdays 3pm ET, 30 to 45 minutes, 4x to 35x server luck [stealabrainrot; fetched and held]; Blue Lock's W Wednesday gives away 40+ Lucky Style Spins weekly, credited on-wiki with pulling the game "out of the heavy pay-to-win bubble" [digger-ls-18]; GaG's own admin sessions are community rituals with players told to arrive early [digger-ls-30].
- **Idle drip with a return trip** [jji, carrier-only]: AFK Mode pays 1 spin + 1 chest per 10 minutes with a 20-chest cap, forcing a return. Sol's RNG merchants spawn every 15 to 45 minutes announced by a horn [digger-ls-15]. (Accrual must sit behind active-play gates in our lane; law 15, section 5.)

### R4. Accumulation curves

- **Bond curve** [digger-ls-06, Bee Swarm; carrier-only]: 25 levels, 10 bond at L2 to 9 quintillion at L25, rarity-invariant, per-level +5% gather / +10% conversion / +5% energy / +3% movespeed, hit chance = 1/2^(mob level - bee level). Sink: treat shop scales 100 to 10,000 honey; acquisition multipliers cap at 133%; full-hive 0-to-25 costs 500Qn honey, 376Qn at max multipliers.
- **Gifted lottery with pity** [digger-ls-06]: 0.4% (1/250) from jelly/eggs; favorite-treat rolls 1/8,000 Rare, 1/10,000 Epic, 1/12,000 Common and Legendary, 1/24,000 Mythic; 1% premium consumable, 1.1% aged variant; Star Treat as guaranteed pity and the only path for event bees; duplicates never stack, distinct types stack. An "Until Gifted" auto-roller normalizes bulk sessions.
- **Aging curve** [adoptme; fetched and held]: tasks Newborn to Full Grown: Common 25 / Uncommon 36 / Rare 54 / Ultra-Rare 107 / Legendary 183 (pre-2025-09-12: 56/80/120/160/275). Executed per-tier cuts (check 3): 55.4 / 55.0 / 55.0 / 33.1 / 33.5 percent, so the grind cut is a 33-55% range. (The revision-1 and input figure "31-55%" is drift; corrected here.) The cut shipped the same day as the Pet Releaser deletion faucet; grind length and supply discipline are one knob. Fusion sink: 4 Full Grown same-species = 1 Neon, 4 Luminous Neons = 1 Mega (16 pets per Mega); 30 tasks per post-cap Friendship level with a free Age-Up Potion per level.
- **Bestiary ledger** [digger-ls-14; fetched and held]: per-location completion percentage with color-staged bookmarks (red below 70%, yellow above, neon yellow at 100%); each closed page pays coins + XP + a cosmetic; 100% All pays 50,000 C$ + 100,000 XP + the Aurora Bobber; 22 rod rows in the fetched table gate on completion percentages from 40% up to six simultaneous 100% gates on Olympian Godbreaker. **The load-bearing rule**: completion credit requires catching the fish yourself, traded fish never count. Secret/Apex/Limited fish are excluded from the percentage. Rod ladder: Flimsy 0 C$ to Kings 100,000 to Destiny 190,000 to Zeus 500,000 + L250 to Abaia 750,000 + L850 to Tryhard L999; luck stat 0% to 399%. Luck curve: Trash/Common spawn rates scale down 1:10 with luck, top tiers scale up 1:1.
- **Pass currency curve** [tds, carrier-only]: `250 x (waves/20)^1.75 + 100 triumph` per run; full pass 13,175 currency or 2,030 Robux; rank costs 225 to 3,000, Robux 50 to 400 per rank. Ticket-era cautionary curve: launch paid flat 10/wave plus a 600 triumph bonus, rewritten within a day (the flat-plus-fat-completion shape rewards quit-and-requeue loops).
- **Quadratic job XP** [digger-ls-25, carrier-only]: 10/10/40/90/160/250/360/490/640/810 per level, total 2,860 (check 1), last level 810 = 28.3% of the grind (executed, check 3), capped at a visible Gold Star. **Corrected fit (cold-read fix):** the sequence is reproduced exactly by `cost(n) = max(10, 10 x n^2)` for n = 0..9 (executed, check 3). The input's claim that it "fits 10x(n+1)^2" is false as written: that sum is 3,850 with a tail of 1,000 (executed).
- **Geometric pet XP** [ps99; fetched and held]: per-level cost grows 2^(1/7) (about 10.4%), doubles every 7 levels, level 92 is halfway to 99, level 99 costs 13,034,431 total XP, the last single level 1,228,825.

### R5. Scarcity valves

- **Server-capped combine ladders** [ps99; fetched and held]: 10 dust = 1 shard, x10 per rung to prism, 10 prisms = Huge Pixel Bee (100,000 dust per huge), then 5/5/5 rungs upward, with the top crafts capped server-global at 2,000 (Titanic grade) and 10 combos (Gargantuan grade). Countable scarcity makes ownership a public rank signal.
- **Rebirth lock ladder** [stealabrainrot; fetched and held]: base lock 60s, +10s per rebirth (80s at 2, 110s at 5, 240s at 18; the deep pass corrects max rebirths to 19, 250s at R19), +10s VIP gamepass; 30s join grace; cash curve R1 500K to R13 14T; +1 slot per rebirth from R2; Update 66 softened the wipe to required units only (the older whole-board wipe reads on the Outdated-tagged page). The defense you most want is bought by resetting your own progress, cheaply now.
- **Limited-return pricing** [digger-ls-28, WCUE; carrier-only]: seasonal passes expire on a schedule and return at higher prices on the carried record, with one counterexample (cold-read fix): Valentines bundle 225 to 450 to 599 to 699; Holiday 225 to 1,000; Autumn Leaf 25 to 400 to 333 (400 to 333 is a decrease); Spring 299 to 555 to 666; Wanderer's Cloak 249 to 399 to 499; Bat Wing Harness 249 to 699. The input's "strictly higher" is falsified by the Autumn Leaf series; the defensible rule is "higher on average," and the 333 is either the counterexample or a transcription error (filed 5.3). Waiting is a visible penalty; founding owners gain status. Save slots are the scarce container: 12 free, max 100.
- **Vault-with-refund reset cadence** [digger-ls-16, Type Soul; carrier-only]: the 5/6/2026 mega-rework vaulted whole systems, multiplied Kan gains (ranked x1.5, raids x1.5, divisions x5, missions x2.5), reset balances to 250,000 under a 1,250,000 hard cap, changed kill theft to 5% capped at 10,000, and refunded every removed item in rerolls and tokens (8 Locked Element Rerolls + Locked Weapon Reroll + Locked Clan Reroll per removed vow/skin). Reworks re-level veterans and novices onto one economy. This is also the recommended shape for the wheel's seasonal currency end-of-life (4.5).
- **Plot/slot expansion ladders** [digger-ls-01; fetched and held]: plots 6 steps 500 / 40,000 / 1M / 40M / 200M / 1,000,000,000; pet slots 200,000 / 1M / 5M; guild creation 99 R$, slots to 50 (cumulative 1,472 R$).
- **Grandfathered bundle escalator** [ptfs, carrier-only]: a pass that grows with every content drop while its price steps up per drop (Learjet 95 R$ to Private Jets 195 to 225) and old buyers keep everything added later. Buying early is itself the retention device.
- **Token re-run ladders** [tds, carrier-only]: every lapsed exclusive returns later at a fresh Robux price (Archer 250 to 649 across five windows; Sledger 500 to 749; Frost Blaster 350 to 525; Harvester 799 with one 639 dip), and the store priced the same item in both currencies (Gift of Sharpness 2,500 Tickets or 250 R$). 17 passes chained back-to-back October 2020 through June 2026, so the next reason to log in exists before the last one expires.

### R6. Cadence multipliers (paired threat and payout)

- **Every-third-round special** [evade, carrier-only]: special rounds multiply threat and reward together: Double Trouble 2x bots = 1.15x rewards, Triple Trouble 3x = 1.25x, Speed 1.4x = 1.1x, Lurking 3-4 Super Munci = 1.6x, Cat Jard = 1.7x, Plushie Hell = 2.0x; Keep Moving drains 10 HP/s standing still; Swap repositions every 12s. Stated purpose: "used to give the game more variety and keep the player base engaged."
- **Biome windows** [digger-ls-15]: Windy 1/500 x3, Snowy 1/600 x3, Rainy 1/750 x4, Sandstorm 1/3,000 x4, Hell 1/6,666 x6, Starfall 1/7,500 x5, Heaven 1/7,777 x5, Corruption 1/9,000 x5, Null 1/10,100 x1000, Dreamspace 1/3,500,000; breakthrough (off-biome roll) runs regular rarity divided by the biome multiplier.
- **Guaranteed pity spawns on a clock** [stealabrainrot; fetched and held]: guaranteed Legendary every 5 minutes, Mythic every 15, Brainrot God on a like-count threshold (disabled in private servers); exact spawn rates unpublished.
- **Bank accumulator** [digger-ls-15]: 200 coins banked per Jackpot roll (277 with gauntlet), 100 per Gilded, pays at daily reset, cap 100,000 at L1 rising to 400,000 at L7 with +50% roll speed.
- **Hourly clock with grace** [digger-ls-06, Bee Swarm Wealth Clock]: x1.01 honey per pollen per use, 5 stacks, cap x1.05, tickets ramp 1 to 5, resets if you leave, 15-minute offline grace. The grace is the documented bug surface (law 6, section 5).

### R7. Social and trade rails

- **Anti-scam machinery** [adoptme; fetched and held]: 18 trade slots; countdown starts at 5 seconds and resets on every item add/remove; unfair-trade popup then 15 extra seconds to confirm; Trade License (free 3-scenario scam-spotting quiz, retake until pass) gates Ultra-Rare and Legendary trades; Trading Hub listing 100 Bucks, 2 active slots, third at 49 R$, listings escrow-locked, balance-gated, and visible only while online. The Scams page catalogs 41 named scams (deep-pass census) built on one shape: pay first, receive never. Reverted scam trades return items flagged permanently untradable, so recovery cannot be laundered. Design law: any asset excluded from the sanctioned trade surface becomes scam fuel, so gate the top tier inside the sanctioned surface.
- **Trade friction knobs** [digger-ls-12; fetched and held]: level-10 gate (installed 2021-12-28 specifically "as a measure against duping"), 6-second wait per item added, 4 unique items per window.
- **Value-cap binding** [digger-ls-05]: Blox Fruits caps traded value difference at 40%, stretchable to 80 to 100% by pricing Robux products into the trade; if a cap ships, it must bind on total value including premium items.
- **Reroll-as-currency** [digger-ls-16]: Type Soul's community value list denominates trades in reroll items (Clan RRs at 1k with demand 10 at the table top); explicitly player-made, devs published none.
- **Gift-ledger spectacle** [digger-ls-13, carrier-only]: decade-scaled broadcast tiers (1-9,999 tops the board temporarily; 10,000-99,999 holds it plus blimp and fireworks; 100k-999k nuke; 1M-9.9M smite; 10M+ Starfall); receivers drip 1% Giftbux per gift for cosmetic progression; the loop is zero-sum ("No new Robux enters the system"). Compress the decade ladder to VM currency so the tiers stay reachable.
- **Status flex surfaces**: PS99 tradable limited companions as store of value with auto-scaling (section 4); MM2 prestige (level-100 resets, max 10) with 14,572,419 players at the badge [digger-ls-12; fetched and held]; WCUE morphs as account identity, trades copy morphs so visible density grows [digger-ls-28]; DTI's 14-rank star ladder 50 to 150,000 with star-gated servers at 3,000 and 10,000 plus a VIP server [digger-ls-22, carrier-only].
- **Free-instant identity layer** [digger-ls-27, Brookhaven, carrier-only]: 80+ jobs equip instantly as nameplate icons, no tutorial, no progression, monetization on 17 cosmetic/convenience passes at 30 to 999 R$; Ad Rewards let free players preview pass content 10 to 30 minutes per ad; a weekly update drumbeat (59 dated headers across ~16 months) repeatedly pushed past 1M concurrent, record 1,296,208 on 2025-12-19.
- **Hosting as status, with a ceiling** [digger-ls-26, MeepCity, carrier-only]: 400 R$ host pass, public portal of concurrent parties, 50-member cap, furniture sinks 150 to 500 coins, all riding a 50-coins-per-5-minutes dwell drip (parties pay zero and are pure sinks). Carried as a caution as much as a curve: the feature died by execution (law 11, section 5).

### R8. Theft and presence (the coupling worth stealing)

[digger-ls-01 / digger-ls-02 reskin + stealabrainrot; fetched and held.] The load-bearing retention coupling in the corpus: the event window doubles as the heist window, so rare spawns pull defenders off their plots by design (GaG2's "Special Night Technique": "the owner of a garden will look for those seeds instead of protecting crops"). Documented technique meta: Wheelbarrow Method (alt/friend wheeling an AFK owner out of their own garden, with its own teleport glitch), Immediate Join Snipe, Wait Trick, AFK Method. Documented mitigations to carry: owner-presence lock, teleport buttons disabled mid-steal, 3-second steal time on high-value crops, shovel knock-out returns the fruit, stolen event crops never trigger event windows, spawn odds damped in low-population and private servers, guard pets that tackle intruders. The log-off rule ("the player stealing will get to keep the fruits stolen") makes absence a payout event and demands a deliberate, published decision. Steal a Brainrot adds the alarm loop: "Someone is stealing your Graipuss Medussi" rings on theft start, the thief is slowed 34 to 20 (about 41%) with gears stripped, and anyone who hits the thief teleports the loot back. Monetized clock relief (GaG2): Grow Plant 39 R$ skips one crop, Grow All 299 R$, instant restock 39 R$ [digger-ls-01]. Kitsune-class automation pet: checks empty gardens every 5 to 10s at 85%, 3-second steal, 20% Chakra mutation on delivery, 10s success / 3s fail cooldowns [digger-ls-02].

---

## 3. Skips and why

### 3.1 Whole-finding skip

**Hunters season bounty cycles [digger-ls-29]: verdict skip.** The named mechanic is undocumented in every source the digger could reach: zero hits for "bounty" and "season" across the Roblox games API record, 8 badge descriptions, three guide pages, both code trackers, and news/RSS queries; no wiki exists for the game; Discord and Trello were unreachable. The finding files no numbers for the mechanic and claims nothing about it. What is verified, for a re-dig if a source ever surfaces: Reawakening rebirth ladder (level 20 to climb F to E, rank-ups reset stat points, badge funnel E Rank 254,311 down to S Tier 2,625 awarded), offline XP harvest promised in the official description, group-membership luck boost (the digger's alt-boost flag there is labeled inference with zero documented cases), 9 codes across two trackers. The skip stands until a primary source exists. Do not spec against it.

### 3.2 Skip pieces inside adopted systems

- **PS99 paid Robux egg shop and the hatching/rebirth stack** [ps99, reskin; fetched and held]: the paid-random lane carries the five-jurisdiction regulatory block and the 240/950/2,950/14,500 R$ pricing; the finding's own verdict skips both. Take instead: the auto-scaling prestige companion (huge damage = strongest pet's damage x (1 + level bonus + variant bonus); "Huge Pets will always deal more damage than the player's strongest stat pet"), the Golden/Rainbow/Shiny variant ladder (+0.3x/+0.9x/+1x; Titanic +1.2x/+3.6x/+4x), and the server-capped combine ladder (R5).
- **JJI spin system wholesale and its Robux gamepass set** [jji, verdict reskin per MECHANICS; carrier-only]: the draft slot is already occupied (a second competing power lottery), and the 149/399/399/799/2,699/1,699 R$ gamepasses map badly onto VM currency. Take the domain economy skeleton instead: Unique unlock asset at 0.1% chest drop with a 1.2x boss luck modifier, capacity 5, tradable-yet-unsellable, 3-hour market refresh priced in farmable substitutes (4 to 6 scrolls or 48 to 53 fingers), hourly world spawn (1/100 servers), a free fallback unlock behind a level-420+ boss, and a 100%-meter activation filled by dealing or taking damage with a Domain Clash rule on simultaneous casts (a natural faction-war peak event). Reject the unmitigated tradeable endgame asset: the finding documents RMT listings and macro AFK farming around the shard; counter with soulbound unlocks and activity-gated drip.
- **Type Soul AFK hide-to-bank streak and the 96% no-buff floor** [digger-ls-16, reskin]: the wiki itself instructs players to "hide after obtaining a satisfactory streak"; documented degenerate. Any AFK-accrual loop collides with the shared-respawn Pilgrim class; keep accrual behind active-play gates. Take: the vault-with-refund reset cadence, the cap-plus-theft currency tax, and the reroll-as-trade-denomination pattern.
- **Bee Swarm external social distribution and the raw promo-code menu** [digger-ls-06, reskin]: the Discord/Twitter/YouTube reach needs audience scale the lane lacks; the code menu is redundant with boon drafts. Take: the bond curve, the gifted lottery with pity, and the once-per-account hidden-clue drop with 30 to 60 minute windows announced through faction channels, paying drafts and clock buffs.
- **Blox Fruits death-loss fruit economy and unregulated trading floor** [digger-ls-05, reskin]: the economy is welded to a death-loss grind identity and inherits a documented scam surface ("Freeze Trade," "Auto Accept," cap-stretching via Robux products). If a trading floor ever ships, scam mitigations go live day one and the 40% cap binds on total value including premium items. Take: the 4-hour shared stock, the weekend spawn acceleration, the famine-feast flagship spike, and the permanent-forever shop tier (buyable out of stock).
- **DTI expression content** [digger-ls-22, reskin]: the fashion closet, 790-theme list, and makeup sliders have no combat analog. Take: the 360-second judged prep window (maps onto draft commit timers), 1-to-5 peer scoring feeding the star ladder, star-gated matchmaking tiers, unused-vote deduction shipped day one (Showdown's fix for vote dumping), and the walked-back blanket vote penalty as the cautionary tale (it survived only on the gated Master server).
- **PLS DONATE real-money rails** [digger-ls-13, reskin]: a full clone is platform-hostile (cross-game pass sales were killed 2026-05-29 "To protect players... from fraud and exploitation"; the replacement Transfers API caps 500 R$/day and 1,000/month behind a Plus subscription). Take the gift-ledger skeleton only: claimable stands, public real-time gift board, compressed broadcast tiers, 1% drip to receivers, gifts funding shared-respawn charges.
- **MeepCity party hosting as free-form player-hosted venues** [digger-ls-26, reskin]: the feature's death penalty is total deletion (law 11). Host-status aspiration and dwell-drip income survive as shapes; free-form custom-named publicly-listed rooms with social furniture do not.
- **Evade paid queue override** [evade, reskin]: a single 20-R$ submission replaces every nextbot for the whole server's round, with documented blank-submission bypass trivia and a spam fix two days into Alpha; a paid override of shared state is the shape to leave behind. Take: the every-third-round paired multiplier and the camping-proof reward rules.
- **MM2 off-platform price discovery** [digger-ls-12, reskin; fetched and held]: the ~50,000-to-1 value spread lives on third-party sites (mm2values.com, 4.2M holders served) because the devs publish no values and the top tier is leaderboard/manual scarcity (Uniques untradeable). If trading ships, put the value surface inside the game; keep the salvage/craft de-rank ladder and the level gate.

---

## 4. Lane landing: how each piece lands on VM economy / boon drafts / faction war / Pilgrim

### 4.0 Hook register H1-H14 (definitions; every H-reference in this document resolves here)

All fourteen are the RETENTION input's retention hooks, section 1, each stated in one line:

- **H1, the appointment clock stack:** one globally synchronized rotation clock for the event shop, short fixed cycles for boon draft windows, a weekly faction war reset scored per contributed unit.
- **H2, server-synced spectacle with a presence gate:** rare spawns scale with server headcount and hard-zero below a minimum, pulling solo players into crowded servers at window time.
- **H3, a reveal at every window exit:** an asset brought into a window receives that window's multiplier, rolled once at window exit (the diggers' mapping: window multipliers instead of harvest rolls).
- **H4, seasonal sub-world with rising-return reruns:** a parallel seasonal currency with its own sink ladder; retired season items return only at rising prices.
- **H5, famine-feast flagship spikes with countable scarcity:** withdraw a flagship, let scarcity compound, relaunch reworked at a higher cost; cap top conversions globally and publish the count.
- **H6, the self-funding pass with a visible finish line:** the pass repays its cost on completion; every purchase advances a visible meter.
- **H7, status that appreciates:** limited prestige companions that auto-scale so early chases stay meta-relevant, traded as the wealth display, with server-capped conversions as verifiable scarcity.
- **H8, pity meters and safe rerolls:** reroll tokens drip from every mode, the top tier carries a countable pity, and a reroll never silently destroys value.
- **H9, threatened loss with an alarm:** raids ring a named alarm, slow the raider, and reward the chase; raid windows are scheduled against event distractions.
- **H10, the community donation board:** rotating NPC request, public contribution board, shared structure growth and decay, count-gated premium stock, a global milestone ladder.
- **H11, a completion ledger that gates power:** persistent per-region completion percentages gating unlocks, credit bound to the earning account.
- **H12, win-back machinery and scheduled free-value drips:** a returning-player buff aimed at lapses at season start, faction-channel code drops with short live windows, one weekly dev-run chaos window.
- **H13, the gift-ledger spectacle loop:** a public real-time gift board with compressed broadcast tiers, a 1% drip to receivers, gifts funding shared-respawn charges.
- **H14, peer-judged rounds and ladder-gated matchmaking:** judged rounds after bouts feeding a glory ladder, renown-gated servers, unused-vote deduction from day one.

### 4.1 Tick skeleton and the tick-zero engineering box

| Tick | Cadence | Source |
|---|---|---|
| Event shop restock, globally shared stock | every 5 minutes | digger-ls-01 (GaG2), digger-ls-05 (Blox Fruits 4h dealer as the long form) |
| Price-multiplier reroll on sell rates | every 10 minutes | digger-ls-01 |
| Boon draft window | short fixed cycle | H1 |
| Guaranteed pity spawns | 5 min Legendary tier / 15 min Mythic tier | stealabrainrot |
| World spawns | hourly, 45 min weekends | digger-ls-05 |
| Faction war reset, scored per unit contributed | weekly | digger-ls-30 / digger-ls-01 (GaG2 scores 1 point per gram) |
| Dev-run chaos window | weekly, 30 to 45 min, 4x to 35x luck | stealabrainrot |
| Seasonal sub-world with parallel currency | 60 days, with the end-of-life rule of 4.5 | digger-ls-02 |
| Pass window | chained back-to-back, gaps of days | tds |

**Tick-zero engineering requirements (added on cold read; the row above is the spec's largest backend commitment).** The globally shared 5-minute restock commits every server to one orchestrator, and the source games answer the hard parts poorly: GaG2 runs purchases client-sided on shared stock, the corpus's own documented fraud surface, rejected here by law 1. The wheel's version requires, before v1: (a) server-authoritative purchase with stock reservation and an idempotency key per buy; (b) a stated contention policy for the restock instant (all clients hit at t=0: request queueing plus jitter, so stock resolution is ordered and auditable); (c) a stated server-count and capacity assumption, since the stock is cross-server by definition; (d) a degraded mode when the orchestrator is down: freeze stock rather than mint duplicates, resync on reconnect; (e) the law-1 mint alarm wired to the restock path. Law 8's fallback timer covers appointment content going dark; it covers neither contention nor failover. No source game in the corpus demonstrates the sanctioned version of this row; the design is owed, and the row stays out of v1 until it exists.

### 4.2 Per-clone landing (H-refs resolve in 4.0)

| Wheel piece | VM economy | Boon drafts | Faction war | Pilgrim |
|---|---|---|---|---|
| W1 window skeleton | seasonal currency sink ladder (Leaf-analog packs at identical prices); end-of-life per 4.5 | drafted boons receive window multipliers (model A, W2) | war windows where the rare spawn scales with war headcount (H2) | shared-respawn events gated on minimum headcount, hard-zero below 2 players (H2) |
| W2 reveal ladder | mutation bonus prices into sell formulas (+1/+2/+3 Silver/Gold/Rainbow on the donation board) | window exit rolls the drafted boon's multiplier, one buff per boon (H3) | raid loot carries window-tier multipliers | respawn events end in a visible roll |
| W3 donation board | donations are the VM sink (magnitude set by the 4.5 anchor); 2026 tripling restock is the whale sink | Giant's Basket is the draft template: 30 picks, 1 of 3, reroll | public board feeds war scoring; top-contributor table with exact odds | contribution-count gates unlock shared-respawn (fun stays ungated, portal and prestige stock gated) (H10) |
| W4 pass | pass self-funds in VM currency on completion (H6) | quest cadence shapes draft sessions; per-level budget 80,000 XP-equivalents | war quests on the daily/weekly shape | Supercharged-style double drip aimed at lapsed Pilgrims at season start (H6, H12) |
| W5 collection | every purchase advances a visible meter (H6) | collection items as draft cosmetics | faction-set completion unlock | post-event shop floor keeps the set valuable after the window (H6) |
| W6 reroll stack | drip routes players through every mode; only paid-lane rerolls tradable; drip budget derived and published per 4.5, the carried 854/week is unusable | flat reroll cost, countable mythic pity, LOCK-style safe reroll, no silent value destruction (H8) | war rewards pay rerolls | returning-Pilgrim rewards pay rerolls to a banked cap (H12) |
| R3 clocks | one synchronized rotation clock for the event shop (H1) | short draft windows on the same clock | weekly war reset on the shared clock | respawn windows announced on the clock |
| R5 scarcity | server-capped conversion ladders as verifiable VM valves, count published (H5, H7) | flagship boon withdrawn for a season, relaunched reworked at higher cost (H5) | war seasons pay limited prestige companions (H7) | retired season items return only at rising prices (H4) |
| R8 theft coupling | raided stock is VM stock; stolen event stock triggers nothing | boon stores are raid targets | raids ring the alarm, slow the raider, reward the chase (H9) | Pilgrim respawn events are the distraction that opens the raid window, by design |
| H11 bestiary ledger | completion pays currency | region completion gates boon unlocks | war maps carry region ledgers | per-region completion gates Pilgrim unlocks, credit bound to the earning account |
| H13 gift ledger | compressed broadcast tiers on VM currency | gift-funded draft boosts | gifts fund war charges | gifts fund shared-respawn charges |
| H14 peer judging | glory ladder on the DTI curve | draft commit timers on the 360-second window | post-bout judged rounds feeding the ladder; renown-gated war servers | unused-vote deduction from day one |

### 4.3 The raid spec, annotated (proposals marked; the source carries the headlines only)

Carried from digger-ls-02's clone/patch list: (1) event-crop theft never triggers the event window; (3) owner-presence is a zone geofence that forced transport cannot break and AFK does not drop; (4) join-grace immunity against spawn sniping; (5) steal time scales with asset value tier; (7) wager loops get loss caps and cooldowns; (8) gambling-class mechanics get the same geo-gating discipline (law 17). Four lines need definitions the source does not provide; proposals are this assembler's, flagged as such, and each needs its own abuse review:

- **(2) capped per cycle:** proposed default: one attributed, announced extension per harvesting player per window, chain cap 3 per cycle; the cap value is a build decision (the source sets none). The anti-abuse core is attribution and announcement; the silent 2:30 reset is the documented exploit.
- **(6) induced absence pays nothing:** "inducement" is not server-observable as stated. Proposed observable proxy: a displacement event on the owner (grab, carry, or forced teleport by the raider's side) inside a short window before the owner leaves suppresses the thief's payout. This is gameable in the reverse direction (feigned displacement), so the alternative is cleaner: drop the log-off payout entirely and pay the thief only completed steals. Build decision owed; law 9 requires the chosen rule published before launch.
- **(9) explicit movement anti-cheat:** candidate signals: locomotion-envelope violations (speed and position deltas beyond client-declared movement), collision pathing, input telemetry. No source game publishes thresholds; the spec requires shipped numbers with positive-only audit, and retires GaG2's hedge ("The game might have a movement anti-cheat") as an anti-pattern.
- **(10) pet automation vs empty-garden sniping:** tension acknowledged: the Kitsune's documented behavior is checking empty gardens every 5 to 10s at 85%. Proposed resolution: automation against absent-owner gardens is banned inside raid and event windows and rate-limited outside them, and automated steals never carry mutation rolls (the Chakra 20% is the automation payout). Decision owed to the lane owner.

### 4.4 Build phasing, targets, kill criteria (proposed; no source-derived targets exist)

The corpus publishes no retention or DAU statistics (digger-ls-01 files this owed), so every target below is a lane-owner decision; what this spec supplies is the cut order and the measurement points.

- **v1, core loop:** W1 day clock + draft windows + weekly war reset + W6 reroll stack, with laws 1, 6, 8, 9, 15 enforced from the first build. Exit criteria: the tick-zero orchestrator design exists and passes contention and failover tests; cooldown rejoin/world-switch/crash tests green; no mint alarms for the soak window.
- **v2, economy depth:** W3 board (2026 patch set), W4 pass, W5 collection, pity-spawn tick; requires the 4.5 currency anchor published first. Laws 2, 3, 4, 5 ride in with it.
- **v3, scarcity and social:** R5 valves, the H5 flagship withdrawal, the seasonal sub-world with its end-of-life rule, gift ledger, judged rounds; trading rails only with the full R7 machinery live day one.
- **Targets to set before launch (proposed shape):** appointment attendance per tick, D1/D7, session length, sink/source ratio per season, pity completion distribution. Kill criteria per tick: a tick that misses its appointment-attendance threshold for two consecutive windows is re-timed, and retired if a third window misses. No tick is permanent by default.

### 4.5 Currency anchor and seasonal currency end-of-life (decisions owed)

**Anchor.** The wheel cannot import prices until VM currency has a published value rule. Until the anchor exists, every carried price in this spec (Leaf packs 10-200 R$, the plot ladder 500 to 1e9, the 39 R$ clock relief, the restock tripling) is source-denominated and decorative. Proposed mechanism: fix one VM daily-earn anchor, express every imported price as a multiple of it, publish the table with the W3 board, and re-derive the W6 drip budget from the same anchor (per W6, the carried 854/week is unusable). The combined wheel's sink/source balance is unestimated in this document; it is the first number the anchor must produce.

**Seasonal end-of-life.** W1 imports a 60-day sub-world with a parallel currency; the sources specify no end-of-season handling and neither laws 4 nor 18 cover it. Three carried options: expiry (hardest, highest trust cost), published-rate conversion to VM, or the Type-Soul vault-with-refund shape (R5: refunds every removed holding at a fixed published rate). Recommendation: the refund shape, announced at season start; decision owed.

---

## 5. Abuse patches owed

### 5.1 The laws (ship in the same update as the numbers they protect)

Each law is documented by an incident the diggers fetched.

1. **Server-authoritative consumption + mint-time spike alarm.** PS99's April 2024 Tech Chest key-burn dupe: "20k+ of this pet to appear in circulation within hours"; the studio bounty-paid the finders with Shiny Rainbow Titanics and rotated the prize (Huge Cyber Agony out, Huge Circuit Cat in); the 2024 changelog portion contains zero exploit/dupe/patch mentions (grep-checked by the digger), so the alarm lives in mint data; patch notes carried no trace. Same class: RoCitizens' recurring furniture-dupe patches (6/26/2020, 6/4/2022) and a 2018 permissions override; MM2's nine cataloged "Tragedies," six of them dupes, countered post-hoc by reskin-to-Glitch1, a 20+ Corrupt ban line, a 190+ Batwing ban wave, 2022-10-16 mass deletion, and a 2026-08-20 scythe confiscation; Fisch's January 2025 wave punished innocent recipients, so quarantine recipients instead of blanket bans. Ship: idempotency token per consumption, per-account open-rate cap, item-level lineage IDs, hourly mint-count alarm per item id.
2. **Pity counts every spend surface.** Apex event packs excluded from Bonus Heirloom Shards; the Iron Crown $170 floor, the boycott, and the forced redesign are the receipt. Event purchases advance the master pity.
3. **Caps ship in the same update as the channel.** Fortnite's Creative XP farms ran for years before the ~300k/day wall and hard disablements; Accolade rules came post-hoc. TDS's flat 10/wave + 600 triumph launch paid quit-and-requeue loops and was rewritten within a day; the successor shipped earn-gates and loss normalization.
4. **Conversions of owned paid items need grandfathering.** Blox Fruits silently converted owned Dragons into tokens at Update 24; backlash forced a rollback three days later (2024-12-17).
5. **Record the amount actually paid, origin-bind purchases.** PLS DONATE's regional-pricing exploit credited list price on discounted purchases: "almost a 10,000% day-by-day increase in fake donations"; fixed by binding passes to their origin experience.
6. **Cooldowns keyed on account state, server-side.** Bee Swarm's Wealth Clock 15-minute grace was evaded by rejoining within the grace and by a hive-hub exit trick. Type Soul's AFK World pays more than active play with a documented 20-minute idle-kick bypass. Persist cooldown against account identity; test rejoin, world-switch, and crash paths before ship.
7. **Reward streams need anti-farm gates on day one.** Evade pays Wins only on 3-minute survival "without sitting in the camping spot at least one second," and cheat panels void all end-of-round payouts; Arsenal zeroes private-server income except a documented daily-challenge leak. Close the leak class on day one.
8. **Contribution systems need per-player cooldowns, first-donation credit, and hoard counters.** GaG 2025's holes: contribution points reset on rejoin, whales bought uncapped restocks (500,000 tripling, no limit), Tomato hoard-and-dump optimized flat points, and personal points started only after a player's first drop. All patched in 2026 (15-minute cooldown, count gates, 1,000,000,000 base restock with 24h reset, 15-minute auto restock). Import the 2026 set verbatim; credit everyone present from the first second of the window; scale points with item value or cap dumps; appointment content needs a fallback timer (the Harvest Shop went unrestocked during Summer's last admin abuse).
9. **Theft surfaces need presence locks and event-crop immunity.** The full GaG2 mitigation set plus SAB's alarm/debuff/teleport-back; stolen or raided event stock never triggers event windows; absence-during-raid handling is specified before launch and stated to players. The raid spec (4.3) is the build list.
10. **Alt-account surfaces: gate codes and boosts behind account history.** Blue Lock requires Level 10 + liking + group membership so "one cannot simply start creating new alternative accounts" for spin codes; Anime Vanguards keeps farmed rerolls untradable; BSS codes are once-per-account with 30 to 60 minute windows; PS99 limited clan kicks to 1/day during battles; SAB's wiki endorses alt "juggling" in four places; GaG2's FriendsBonus (+10% per friend to +70%) plus a 3-friend referral code pays players to import the accomplice accounts the Wheelbarrow Method needs. Patch: once-per-account rewards behind server-side per-account ledgers, roster changes rate-limited during windows, referral and friend bonuses capped by account history. BSS's documented economy incident (2.5 quintillion honey via a modified wind-shrine exploit, then reset and bans; anticheat resets past 100 quadrillion) is the scale of the downside.
11. **Player-hosted free-form venues are a moderation single point of failure.** MeepCity parties were deleted the same day as press coverage (2022-02-16) and never restored; exploiters backdoored the game during the review chaos; the wiki records the game reaching fewer players afterward. WCUE's glitched-color cats ended through a mechanical fix (spawn-time normalization) after moderation alone failed. Ship moderated templates, filtered discovery names with no free-form room titles, and a kill switch scoped to the venue. Social grants (guest, ally, family, Connections) stay revocable and stripped of defense permissions (Brookhaven's "Family members cannot be banned while they are part of the family"; SAB's Connections gate); paid convenience never buys cooldown immunity or theft immunity in contested spaces (SAB's Robux-only unstealable Spyder Elephant is the worst trust item in the corpus; sell power, never immunity).
12. **Odds-trust needs published rates and stable multipliers.** Rescoped on cold read: no Roblox-game developer in the corpus publishes a rate table; every Roblox odds table here is community-tabulated. The corpus's one developer-published odds material is Apex's EA FAQ and SF6 pack disclosures (W5), and that is the disclosure shape to copy. JJI's premium multiplier reads 1.5x on one page and 2x on two others; Blue Lock's pages disagree on Master odds; Sol's RNG permits macros outright. Publish official rates, keep them stable, and use the Roblox PRI shape (5.2).
13. **Sanctioned-surface law.** Adopt Me's 41 named scams reduce to one shape: pay first, receive never; the catalog maps exactly what the trade box refuses to carry. Ship an in-box escrowed currency lane or a sanctioned listing lane, and make refunds sterile (returned items permanently untradable).
14. **Non-transferable ledger law.** Fisch's completion credit requires the self-performed catch; leaks flagged: the Bestiary page's own "the player can trade for the fish required" line at The Depths, and C$ gifting at 10 to 27 C$ per Robux as a laundering channel. Keep power items untradable from day one (Fisch's rod carve-out is why dupes only polluted fish); ledger credit never transfers.
15. **Active-play accrual law.** The shared-respawn Pilgrim collides with AFK loops: Type Soul's hide-to-bank streak, Blue Lock's AFK world out-earning matches, Sol's RNG Auto Roll force-rejoining every 20 minutes, PTFS infinite-fuel overnight status, RoCitizens station dwell pay. Accrual sits behind active-play ticks; Evade's camping rule is the positive shape.
16. **Anti-grief default law.** DTI's unused-vote deduction ships day one; punishments scope to gated competitive queues, since the blanket Vote Penalty survived only on Master servers. Player-submitted content slots (Evade's blank nextbots) get rate limits and review before they hit a whole server.
17. **Gambling-class mechanics carry wager guards and geo-gating.** GaG2's Double or Nothing wagers the entire inventory, has no fee, and busts return nothing; the Store hides offers in AU/BE/UK/NL "Due to gambling laws," the dev's own classification. Patch: loss caps, cooldowns, jurisdiction gates.
18. **Wipe-and-reset economics need the Update-66 rule.** SAB rebirths now wipe only required units; guard rebirth during an active theft so the unit transfers nothing and the thief window refunds; conveyor price bumps charge the buyer and cap per unit per minute; lucky-block-class rolls resolve at purchase with published odds (SAB's roll-fixed-at-spawn blocks plus its Belgium/Netherlands/Austria/Turkiye/Australia/UK/Brazil purchase bans are the receipt).

### 5.2 Regulatory envelope

- Paid-random blocks by jurisdiction: PS99 blocks paid eggs in Australia, Belgium, Netherlands, South Korea, and UK under-18 (trading and the free pack remain) [ps99]; Arsenal disables cases in Belgium, Netherlands, Australia, UK under-18 [digger-ls-11]; SAB lucky blocks document purchase bans in Belgium ("violations can lead to fines"), Netherlands, Austria, Turkiye, Australia (age restrictions), UK, and Brazil (18+) [stealabrainrot].
- Roblox Paid Random Items compliance (DevForum thread "Clarifying Requirements for Paid Random Items," published 2026-05-26, read by the digger-ls-12 digger): numeric odds displayed pre-purchase summing to 100%; dynamic numeric disclosure when pity/luck modifiers are active; every outcome yields an item; trading of paid randoms gated by PolicyService (AU/BE/NL/UK/BR); coverage extends to indirect purchase via in-game currencies bought with Robux, which is exactly the MM2 Diamond path. **Enforcement note (cold-read fix):** three carried tables fail the sum-to-100 clause as printed (R2: MM2 100.204, Blue Lock regular 100.1575, Blue Lock lucky 101.2, all executed); they enter the wheel only renormalized or re-dug.

### 5.3 Owed and honesty register

**Corpus-level.** The assembler ran zero web fetches; checks 1 to 3 in section 0 are the only things executed this session. No Roblox-game developer in the corpus publishes a rate table; every Roblox rate is community-wiki attested as of 2026-09-26/27 and no digger ran a live client; the sole developer-published odds material held is Apex's EA FAQ and SF6 disclosures (W5, carrier-only). Player-side abuse testimony (macro forums, scam threads, RMT listings) was largely unreachable (1302 rate limits, 403s, login walls); several abuse records rest on developer countermeasures and wiki documentation per the diggers' own flags. Census: resolved by recount to 30 findings at 5 clone / 24 reskin / 1 skip (section 0); a byte-level grep of the inputs remains unexecuted because the inputs are conversation text here, and the recount is reading-based.

**Wiki-internal conflicts carried as found, unresolved:**

- GaG2: night-moon tables 77/13/6/2/2 vs 77.45/12.75/5.88/1.96/1.96 on one page; auction 15 vs 30 minutes (Mechanics contradicts itself, Auction Stand says 30); Sell Stand "2x-4x" vs Mechanics "0.8x-4x"; Cauldron Charm 250,000,000 vs 2,000,000 Candy Corn; Gold vs Midas Moon naming; Currencies page (rev 2026-06-13) still says Sheckles-only while Mechanics and Fall Harvest document Leaf; Atlantic Giant Pumpkin's immunity flags vs its own Gold/Rainbow-moon line; Update Log page stale at 1.20.0 (July 19) while Fall Harvest (Aug 2), Kitsune (Aug 7), and Muffin Bake (Aug 22) prove an August wave.
- Adopt Me: Royal Desert Egg odds row sums to 135 (35/25/37/30/8).
- PS99: free-lane huge odds print "??"; Huge Robot's chest probability "??"; the 33-pack price conflict (2,650 infobox vs 2,950 prose) is unresolved; the dupe incident rests on the wiki Controversial banner alone, with two WebSearch queries finding no independent corroboration.
- Fisch: Zeus purchase level 150 (Level page) vs 250 (rod table), both official, both fetched 2026-09-27; Destiny Rod gate 350 fish vs 70% era drift; Random Rod range 1 to 9,999,999 C$ at luck 350% vs fandom-era 1 to 1,000,000 at 1000%; the luck formulas live inside an HTML comment (editor draft).
- Steal a Brainrot: Admin Panel 9,999 vs 4,999 R$; Secret Lucky Block 2,399 vs 2,999; luck ceiling 35x vs "current best is 25x" with a 30x row present; base slots "up to 27" vs per-floor 10+8+7 = 25; max rebirths 19 (fresh page) vs 18 (Outdated-tagged page); the 25,836,222 CCU record is cited to a YouTube Short while Wikipedia states a 25.4M October peak; the Wikipedia "shield" sentence is single-source and absent from both game wikis and the fetched PC Gamer piece.
- JJI: premium multiplier 1.5x vs 2x. DTI: monthly VIP 299 vs 399 R$. TDS: payout-change dating (25 Dec 2019 vs "prior to the 1st of January 2020"). Blox Fruits: permanent-fruit totals 74,380 vs 72,380 R$.

**Cold-read findings now verified and filed:**

- Odds-table sum violations (all executed, check 3): MM2 box 100.204; Blue Lock regular 100.1575 with a non-monotonic tail (0.0325 listed before 0.125); Blue Lock lucky 101.2. Re-dig or renormalize before import; PRI gate in 5.2.
- W4 cadence: 80,000 / 9,000 = 8.89 dailies per level (executed); the input's "two dailies plus change" gloss is wrong and dropped.
- RoCitizens fit: the listed sequence fits `max(10, 10 x n^2)`, n = 0..9, sum 2,860; the input's `10x(n+1)^2` sums to 3,850 (both executed).
- Adopt Me grind cut range: 33-55% (per-tier 55.4 / 55.0 / 55.0 / 33.1 / 33.5, executed); the carried "31-55%" is drift.
- Monarch tradeoff pair: the DPS ladder fits x40/9 exactly (executed) and contradicts the carried "+300%" prose; derivation not held; re-dig.
- Safari ladder completion: final tally 264,354,693,100 is 35,645,306,900 short of the 300B top rung (executed); the wiki marks the 280B rung unreached; the ladder ran through the 255B rungs.
- W2 probability model: window-gated rungs carry no per-harvest rates and no overlap rule; three candidate models stated in W2; re-dig before the literal-crop port. Electric 0.33% vs Rainbow 1/300 = 0.3333% rate identity flagged (executed); one is likely misattributed.
- W6 drip: 854/week unusable (mixed periods, image-sourced); weekly-compatible subset about 197/week under one labeled assumption set (executed); per-channel period table owed; wheel derives its own published budget.
- WCUE limited-return rule: "strictly higher" falsified by Autumn Leaf 400 to 333; rule restated as "higher on average"; the 333 is counterexample or transcription error.
- R1 Super Watering Can 300x: single-line outlier vs every other multiplier in the spec; excluded from build constants pending re-dig.

**Decisions owed (added on cold read; the sources do not carry them):** currency anchor and sink/source estimate (4.5); seasonal currency end-of-life (4.5); tick-zero shared-stock contention, capacity, and failover design (4.1); raid-spec definitions for extension caps, induced absence, anti-cheat thresholds, and pet automation scope (4.3); all phasing targets and kill criteria (4.4).

**Named gaps (never guess; sweep the per-finding owed registers before build):**

- GaG2 per-plant grow-time tables and any statement of offline growth: the Crop Data module is not inlined in wikitext; the wiki's single "offline" line is an unconfirmed sprinkler-timer freeze; whether crops advance while the client is closed is stated nowhere [digger-ls-01].
- Beanstalk beans-to-points: the 900-point goal has no per-crop base table; the 1-7 curve is the Summer Harvest sibling [digger-ls-30].
- Fisch per-rarity base catch chances: the Rarity page is Under Construction with zero numbers [digger-ls-14].
- MM2 XP-per-level curve: absent, so rounds-to-level-10 (trade gate) and rounds-to-level-100 (prestige) are uncomputable; MM2's current in-game odds display is unverified [digger-ls-12].
- Adopt Me per-stage task breakdown and XP-per-task: unfetched.
- SAB exact rarity spawn rates: unpublished.
- Bee Swarm macro tooling documentation and ban policy.
- Hunters: negative finding; the skip stands until a primary source exists.
- Leads surfaced and never read by the diggers (filed, do not cite): GAG2 "INFINITE DOUBLE OR NOTHING" glitch videos; Reddit vote-farming bot reports for DTI; r/FischRoblox dupe thread; Blue Lock's live odds screen and the Sportskeeda rate table; Roblox Classic alt/AFK Tix farming.

---

## 6. Closed bibliography

Closed to exactly what this chain read: the diggers' reads (2026-09-26/27), the two synthesis inputs, the deep-dive payload, the cold-reader report, and the assembler's checks. Nothing outside this list was read by anyone in this chain.

**6.1 Deep-dive payload findings (source arrays held and carried by the assembler):**

- `digger-ls-02-gag2-event`: growagarden2.fandom.com via `api.php action=parse&prop=wikitext`, 35 pages fetched and read 2026-09-27 (Weather, Mutations, Mechanics, Stealing, Update Log, Fall Harvest, Ghoul Garden, Grow a Garden 2, Module:Crop Data all 2,230 lines, Seed Shop, Crops, Cornucopia Quests, Badge Achievements, Muffin Bake Event, Monsters, Sell Stand, Shovel, Sprinklers, Store, Weather Machine, Weather Staff, Wind Staff, Admin Party, Cauldron Charm, Trowel, Explorer Stand, Eclipse Bloom, Star Fruit, Amber Cranberry, Kitsune, Gold Seed, Rainbow Seed, Mega Seed, Wheelbarrow, Currencies, Codes; Sheckles fetched unread; Pets and Guilds read in sections), plus the 348-title allpages inventory, plus rendered HTML of /wiki/Stealing via web reader, plus growagarden.fandom.com Take Player's Fruit (redirect) and a Weather-page grep; page revisions range 2026-06-13 to 2026-09-07.
- `digger-ls-01-gag2-grow-deep`: same wiki via api.php, 48-title batch, 44 saved (adds Gear Shop, Gears, Auction Stand, Sheckles, Crates, Chests, Seed Packs, Garden Cards, Atlantic Giant Pumpkin, Carrot, Apple, Sunflower, Teleporter, Speed/Invisibility/Supersize/Shrink mushrooms, Flashbang, Freeze Ray, Player Magnet, Door Crowbar, Strawberry Sniper, Common Sprinkler, Shadow Dragon, Necromancer Staff, Great Pumpkin, Build, PartFruit, Magic Dice); Update Log fresh re-fetch (latest entry 1.20.0, July 19, 2026); games.roblox.com lookup returned errors, unfetched.
- `adoptme-trade-economy-rarity-tiers`: adoptme.fandom.com via api.php, 23 pages (Trading_Hub, Safety_Hub, Daily_Reward, Task_Board, Mega_Neons, Gumball_Machine, Neon_Cave, VIP, Gamepasses, Retired_Egg, Pet_Handler_Pro_Certificate, Scams, Gameplay, Eggs, Trade_System, Trade_License, Bucks, Cracked_Egg, Neon_Pets, Age_Up_Potion, Star_Rewards, Pets; Stars returned missingtitle).
- `ps99-huge-pet-dupe-economy`: pet-simulator.fandom.com via api.php (Huge Pets, Template:PS99LevelProgression, Template:PS99DamageProgression, Exclusive Pets Egg, Exclusive Card Pack, The Forever Pack, Exclusive Raffle, Huge Cyber Agony, Tech Chest, Keys, Clan Battles, Combine-O-Matic, List of Eggs, Rebirth, Trading, Huge Pixel Capybara, Huge Circuit Cat, Huge Robot, Titanic Pets, Traveling Merchant, Update Log 2024 section, Template:PetsOnlyTrading, Template:PS99PB), plus biggames.io/post/pet-simulator-99-update-6 fetched direct; two WebSearch queries found no independent dupe corroboration.
- `digger-ls-12-mm2-knives`: murder-mystery-2.fandom.com, 36 wikitext files (Mystery Box 1/2, Knife Box 1/2, Value, Trading, Crafting, Prestige, Seer, Coins, Diamonds, Mystery Key, Season 1, Duping, Nik's Scythe, Gamepasses, Codes, Batwing, XP, TNL, MM2_Tragedies, the 2017/2019/2021/2022 dupe pages, Batwing 2018, Candleflame 2021, Evergreen 2024, Round Ending Screen, Bonus Rounds, Private Servers, Chroma Box, Murder Mystery 2, Effects); mm2values.com 7 pages including the scam-prevention page; supremevaluelist.com; devforum.roblox.com PRI thread (2026-05-26); en.wikipedia.org Skin gambling lead; archive.org availability checks x3.
- `digger-ls-14-fisch-rods`: fischipedia.org raw wikitext for Fishing_Rods (plus rendered), Luck, Bestiary, Destiny_Rod, Mutations (plus rendered), Level, Rarity, Weather, Shop, Progression_Guide, Trading, Template:Fishing Rod Table, and 18 rod pages; fisch.fandom.com Luck via web reader; pass-1 fandom material carried and marked as such.
- `stealabrainrot-steal-windows-server-lock`: stealabrainrot.fandom.com 11 pages via api.php (Base, Stealing, Gamepasses and Dev Products, Rebirth, Brainrots, Events, Admin Abuse, Mutations, Lucky Blocks, Spyder Elephant); roblox.fandom.com BRAZILIAN_SPYDER/Steal_a_Brainrot (Outdated tag); en.wikipedia.org Steal_a_Brainrot; gamerant.com scripts explainer; polygon.com x2; pcgamer.com hands-on. Server Lock and VIP pages returned missingtitle.
- `digger-ls-30-growdonate-board`: growagarden.fandom.com via api.php, 16 fetches (Beanstalk_Event_2026, Beanstalk_Event_2025, Summer_Harvest_Event_2025, Safari_Harvest_Event, Fall_Market_Event_2025, Christmas_Harvest_Event, Giant, Jack, Update_Log/1.19.0, Beanstalk, Pack_Bee, Admin_Abuse, Category:Events, Fall_Market_Event_(disambiguation), Category:Crops_Type; Grow_a_Garden returned missingtitle); four WebSearches, snippets paraphrased, none cited.

**6.2 Findings carried through the synthesis inputs (ATTESTATION: carrier-only throughout this subsection; read by their own diggers 2026-09-26/27 with methods recorded per finding; the assembler holds no source arrays, and the constants in W4, W5, and every [carrier-only] row are attested at carrier strength and require re-dig before build constants):** `digger-ls-05` (Blox Fruits), `digger-ls-06` (Bee Swarm), `digger-ls-07` (Fortnite; per the MECHANICS input: fortnite.fandom.com Battle_Pass / Season_XP / Supercharged_XP, fortnite.com V-Bucks pricing page, The Verge, Polygon, Dexerto, GamesRadar), `digger-ls-08` (Apex; per the MECHANICS input: ea.com FAQ fetched twice with identical wording, ea.com additional-pack-disclosures, ea.com Anniversary Collection Event blog, PC Gamer Iron Crown article), `digger-ls-09` (Roblox The Classic), `digger-ls-11` (Arsenal, via Wayback per the RETENTION input), `digger-ls-13` (PLS DONATE), `digger-ls-15` (Sol's RNG), `digger-ls-16` (Type Soul), `digger-ls-18` (Blue Lock Rivals), `digger-ls-19` (Anime Vanguards; per the MECHANICS input: animevanguards.fandom.com plus wiki.vanguards.gg), `digger-ls-22` (Dress to Impress), `digger-ls-25` (RoCitizens), `digger-ls-26` (MeepCity), `digger-ls-27` (Brookhaven), `digger-ls-28` (WCUE), `digger-ls-29` (Hunters, negative finding, live Roblox APIs per the RETENTION input), `evade`, `ptfs`, `jji` (verdict reskin per MECHANICS), `tds`, `skibidi`, and the pass-1 Adopt Me card material inside the adoptme finding. Total distinct findings across 6.1 and 6.2: 30 (5 clone / 24 reskin / 1 skip; see section 0).

**6.3 Assembler inputs and checks:** the three ask artifacts plus the cold-reader report; checks 1 to 3 run against the repo venv on 2026-09-27 with commands and outputs recorded in section 0. No other source, page, or document was read by the assembler. Bibliography closed.

---
