# ROBLOX MONETIZATION PLAN — The Estate's Games
## 2026-09-24 · GO: operator ("how do we adapt our games and make some dough")

---

## THE NUMBERS

| Metric | Value |
|---|---|
| Developer cut | 70% (Roblox takes 30%) |
| DevEx rate | $0.0035 per Robux |
| Minimum payout | 30,000 Robux (~$105) |
| Net per Robux spent | ~$0.00245 |
| Best genres | Simulators, Roleplay |
| Worst genres | Educational (direct), low-volume story |
| Story game at 10K DAU | 50K–300K Robux/month |
| Simulator at peak | 1M–50M+ Robux/month |
| Time to first payout | 1–6 months (with marketing) |

---

## THE ESTATE'S INVENTORY

**35 playable games** already built (from the gaming corpus pass):
- Arcade: Arrakis, RUINS GO, SkiFree clone, swarm bullet-hell, maze arena
- Puzzle: Spectral Maze, Light Maze, Riddle Maze, Erosion Field
- Educational: Hardware Primer (Darlington pairs), Incident Dungeon
- Simulation: Airflow Home, Erosion Field, Steer Field
- Narrative: Persistent World, Table (text adventure)
- Art/Toy: Isfahan Lattice, Spore Fish, Bad Apple Field

**The flagship IP**: The Ledger of Empty Chairs (world, lore, boss, factions, the Answer)
**The engine**: game_campaign.py (4,765 lines), game_mud, game_dm, the full narrative loop
**The audience**: existing X following (1.37M views on pillar posts), the beacon site

---

## THE STRATEGY — Three Tiers

### TIER 1: VOLUME — Arcade Ports (Fast Money)
Port the 5 simplest arcade games to Roblox as individual experiences. Each one is a template: same mechanics, different theme from the estate's lore.

| Game | Roblox Genre | Monetization |
|---|---|---|
| swarm (bullet-hell skate) | Action | Game Pass: double score |
| RUINS GO (grid puzzle) | Puzzle | Dev Product: extra lives |
| Arrakis (desert riding) | Simulator | Game Pass: faster board + Dev Product: spice boost |
| Light Maze | Obby | Free (Premium Payouts from engagement time) |
| SkiFree clone | Obby | Dev Product: skip the yeti |

**Why this tier first:** Obby and Action games get volume. Volume drives Premium Payouts. Premium Payouts are passive — you earn per Premium-user-hour regardless of purchases. 5 games × even 100 concurrent players each = 500 Premium-hours/day = passive income while you build the flagship.

**Timeline:** 2-3 weeks per port. Use Roblox Studio templates. The Luau code is simpler than the Python originals.

### TIER 2: THE FLAGSHIP — Ledger of Empty Chairs (The Brand)
This is the story game. The Hall of Shared Supper. The Answer boss. The shadow ledger. The mechanic where the hall files what you chose.

**Monetization model:** Free-to-play + Game Passes + Premium Payouts

| Item | Type | Price (Robux) | What It Does |
|---|---|---|---|
| The Watchful Eye | Game Pass | 199 | See the shadow ledger's disposition of other players |
| Skip the Waiting | Dev Product | 99 | Skip Brother Vellum's grant dialogue |
| The Salt-Cellar Key | Game Pass | 299 | Unlock the Cellar realm early |
| Virtue Mark Doubler | Dev Product | 149 | Double marks for 1 hour |
| The Answer's Weakness | Game Pass | 499 | See the 15-degree tell highlighted in Phase 3 |

**Why:** Story games with a strong boss fight retain players. Retention drives Premium Payouts. The Answer is the reason players tell their friends. The 5-phase fight with the Calabi-Yau deflection and the Wing Chun redirect is content nobody else has.

**Timeline:** 8-12 weeks. Build on the Luau modules already written (GameConfig, ShadowLedger, TheAnswer, HallOfSupper).

### TIER 3: THE EDUCATIONAL LAYER — Learning Through Play
The estate's educational games (Hardware Primer, Incident Dungeon) don't earn directly on Roblox. But they do something else: they establish the estate as a legitimate creator, not a trend-chaser. And Roblox has an education vertical.

**Play:** Submit the Hardware Primer and Incident Dungeon to Roblox Education. If accepted, they get visibility in the education category. Low revenue, high credibility.

---

## THE PATH TO FIRST PAYOUT

Target: 30,000 Robux earned = ~$105 cash out.

Fastest route:
1. Port **swarm** (bullet-hell) first — it's the simplest, most replayable, and the disco-soundtrack gimmick is a TikTok hook
2. Add one 99-Robux Game Pass (double score) and one 49-Robux Dev Product (extra life)
3. Enable Premium Payouts
4. Post the launch clip on X (the estate has 1.37M views on pillar posts — use the audience)
5. Target: 430 pass sales = 30,000 Robux = first payout

At the existing audience size, this is achievable in 2-4 weeks if the game is fun. The disco-soundtrack bullet-hell is genuinely unique on Roblox — nobody else has a 122bpm procedural soundtrack bullet-hell.

---

## THE HONEST MATH

| Scenario | Monthly Robux | Monthly USD | Notes |
|---|---|---|---|
| 5 arcade games, low traffic | 2,000 | $7 | Most likely starting point |
| 1 game goes viral | 100,000 | $350 | The disco-soundtrack hook |
| Flagship at 10K DAU | 200,000 | $700 | The real target |
| Simulator at peak | 1,000,000+ | $3,500+ | The dream |
| Top 1% Roblox dev | 10,000,000+ | $35,000+ | Not the plan |

The honest truth: most Roblox games earn nothing. The ones that earn are the ones that get external traffic. The estate has external traffic (X following, beacon site, existing games). The advantage isn't the games — it's the audience that already trusts the name.

---

## THE BUILD ORDER

1. **Week 1:** Port swarm to Roblox Luau. Add Game Pass + Dev Product. Publish.
2. **Week 2:** Post launch clip on X. Cross-promote on the beacon. Monitor Premium Payouts.
3. **Week 3:** Port RUINS GO and Arrakis. Three games live = cross-traffic.
4. **Week 4-8:** Build the Hall of Shared Supper in Roblox Studio. The flagship.
5. **Week 8-12:** The Answer boss fight. The 5 phases. The pre-registered mechanics.
6. **October:** If the window produces, the flagship launches into a primed audience.

---

## THE PRINCIPLE

The estate's games are the evidence. The Roblox games are the distribution. Same patterns, different medium. The lore was already written. The engine was already built. The boss was already designed. Roblox is where the audience is.

The map precedes the territory. The games already exist in Python. Roblox is the port, not the invention.

---

*Bibliography: Roblox Developer Hub (create.roblox.com/docs), DevEx documentation, Roblox monetization guidelines 2026. Verified via DeepSeek research + direct API probing.*
