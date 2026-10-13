# CLONED MECHANICS — what rules Roblox and what we lift

**2026-09-24 · The wheel book. Popular games already solved feel, loop, and controls.
We clone the wheels, skin them in estate lore, and spend our invention only where
nobody has a wheel.**

---

## 1 · THE POPULARITY BOARD (numbers, not vibes)

Current (live trackers, 2026-09):

> **Decay warning (wave report, 2026-09-24):** Steal a Brainrot's 25.8M record
> peak decayed 99.7% within twelve months; it sits at ~80k CCU now. Clone the
> wheels for their loops, never marry a trend's lifespan. Horror-maze is the
> durable lane: DOORS holds ~25k CCU for years on updates alone.

| Game | CCU (approx) | Genre | Core loop in one line |
|---|---|---|---|
| Steal a Brainrot (and the "Steal a…" wave) | record **25.8M** concurrent, first game past 2.5M | base-steal idle | conveyor spawns units → buy → slots generate cash → steal neighbors' units, carry them home |
| Grow a Garden 2 | ~566K | planting idle | plant → server-side growth continues while offline → mutations → sell |
| Murder Mystery 2 | ~541K | social deduction | 60-second role rounds; knife/one-shot-sheriff; item prestige keeps traders trading |
| Brookhaven RP | ~455K | free RP | zero-friction roleplay: houses, vehicles, emotes, no fail state |
| Blox Fruits | ~191K | progression RPG | quests → levels → fruit abilities (Z/X/C/V) → seas → rebirth |
| RIVALS | ~183K | arena FPS | fast TTK, kill-streak announcer, weapon variety, shift-lock aim |

All-time (the formats that never died):

| Game | What it proved |
|---|---|
| Adopt Me! | trading + care loop beats content volume |
| Tower of Hell | NO CHECKPOINTS + shared 8-minute timer = rage-shareable clips |
| Doors | telegraphed horror entities (lights flicker → Rush) + hide-in-closet |
| Pet Simulator X/99 | hatch loop + pets that auto-grind for you = the idle engine |
| Jailbreak | asymmetric roles and robbery timers create drama without content |
| Arsenal | kill = new gun roulette + streak announcer = self-hyping loop |

Sources: [Roblox charts](https://www.roblox.com), [rtrack.live](https://rtrack.live),
[Rolimons](https://www.rolimons.com),
[Steal a Brainrot Wiki](https://stealabrainrot.fandom.com) (base/lock/carry numbers below are from it).

## 2 · CONTROL SCHEMES (desktop + mobile)

| Pattern | Binding | Used by | We adopt |
|---|---|---|---|
| Universal | WASD + Space jump | everything | yes, baseline |
| Sprint | Shift (hold) | Doors, MM2, RIVALS | yes, x1.5, no stamina at v1 |
| Dash | Q tap, 0.25s burst | Blox Fruits, RIVALS | yes, 60 studs, 3s cd |
| Double jump | Space in air, once | Blox Fruits, obbies | yes |
| Ability slots | **Z / X / C / V** | Blox Fruits (fruit moves) | yes, 4 slots, cooldown chips |
| Interact | ProximityPrompt **E** | Doors (closets), Steal-a (carry) | already in (prompts everywhere) |
| Shift lock | toggle click / Shift-lock switch | MM2, RIVALS aim | optional per zone (Swarm/Arrakis on) |
| Menu / map | M | Blox Fruits | v1.1 (leaderstats page) |
| Mobile | thumbstick + jump + ContextActionService buttons | everything modern | ability + dash + interact buttons |
| Reset | R / Esc menu reset | Tower of Hell | yes (instant respawn, see below) |

## 3 · THE CLONES (wheel → our skin → exact numbers)

### 3.1 The Steal-a economy → **the Ledger Exchange** (Basecamp)
The single biggest loop on the platform right now, cloned 1:1 with estate skin:

| Steal a Brainrot | The Mountain skin |
|---|---|
| Conveyor | **the Marble Run** along Basecamp's south edge |
| Brainrots | **estate artifacts** (Chair Nail, Salt Scraps, Vellum's Pen, the Bard's Lyre, a Locked Eye) |
| Cash | **Virtue Marks** (earned honestly by counting chairs, surveying, climbing) |
| Buy | cost by rarity: common 50 / rare 200 / epic 800 / legendary 3,000 VM; income 1/5/20/80 VM per 10s |
| Base slots | alcove with **4 slots**; rebirth adds +2 |
| Steal | prompt on an unlocked neighbor's slot; **carry penalty**: walkspeed x0.6, abilities disabled, owner notified, their lock timer **+10s** on your steal; anyone can take it off your back |
| Base lock | **the Counting Circle**: 60s immunity, +10s per rebirth |
| Shield | once per 5 minutes |
| Rebirth | at 5,000 VM banked: slots reset, **x1.5 income**, +2 slots, +10s lock, hatch a **pet orb** (Pet-Sim auto-grind: follows you, auto-collects swarm gems in a 12-stud radius) |

**Dwarven appraisal layer (2026-09-25, DF fold, WORLDGEN_MINE.md #8).** The
cloned numbers above are frozen. On top of them, every conveyor artifact
carries a DF appraisal (BASE x MATERIAL x quality, artifact x20 +300,
`shared/DfValue.luau` over generated `shared/DfGoods.luau`). The appraisal
decides only the deposit income when a stolen artifact is run home
(band 1..80 VM, `DfValue.vmIncome`), replacing the old flat 5; buys, slot
incomes, costs, locks and rebirth stay exactly as tabled.

### 3.2 Tower of Hell → **LightMaze reborn as the Flicker Tower**
- NO checkpoints. Fall = instant respawn at tower base (Players.RespawnTime = 1).
- Shared **8:00 round timer**; finishers banked into the ledger.
- Tower = 8 sections drawn from a **seeded pool of 5** (SeedRng, round seed shown on the plaque — replayable, verifiable).
- At 4:00 the tower spawns a **bully wisp** per player (ToH mutators, our skin).

### 3.3 Blox Fruits movement + slots → **PlayerFeel + AbilitySlots** (all zones)
- Sprint x1.5 (Shift), **dash** Q: 60-stud impulse, 3s cooldown, FOV 70→82 kick (client landed 82; 2026-09-28 Q-040 reconciled this line to the code, which shipped 82), air dash allowed once.
- **Double jump**: one extra mid-air jump, resets on landing.
- Ability slots **Z/X/C/V** with cooldown chips and mobile ContextActionService buttons:
  - **Z — Fire** (Swarm): neon pellet, 0.25s cd (0.18 with LONG TEETH), kills horde on hit, +streak.
  - **X — Thumper Toss** (Arrakis): throws a thummer at aim point, redirects the Maker, 10s cd.
  - **C — Wing Chun Redirect** (THE ANSWER): 1.5s parry window, 8s cd; a redirected wave takes a boss phase.
  - **V — Count** (Basecamp): reveals what the hall is filing (ledger whispers, Vellum tells, bully wisps), 20s cd.

### 3.4 Doors telegraphs → **the Maker surfaces** (Arrakis)
Rush never hits without the lights dying first. The Maker now must telegraph:
2 seconds of rumble + a red dust column at the breach point before it lunges.
Column height = how close it is. Fair horror is scarier horror.

### 3.5 Arsenal streak announcer → **Swarm taunts go vertical**
Kill streaks announce on the arena plaque: 5 = "the grid remembers every hit.",
10 = "mark, the horde scales — tell them.", 25 = "the maze named its depths. i named nothing."
(the swarm.html taunt lines, hoisted from flavor to reward).

### 3.6 Grow a Garden → **Warm Springs plots** (Basecamp)
Each player has one plot. Plant a Virtue Seed (free, once per visit); it grows on
**server-side timestamps** (unlocks while you are offline): 30 min → Spring Herb,
8 h → Moon Bloom (worth 5 herbs at the Exchange). Offline progress is the hook
that brings players back; Roblox servers made it trustworthy by making it boring.

### 3.7 swarm.html crop physics → **the Swarm flock** (`shared/Flock.luau`)
The gems are alive (swarm.html:949 "the crop is ALIVE — XP is a spore fish, and it
flees"). One pure module owns all three laws; SwarmZone maps them onto the arena:

- **Flee / tire / rest** (swarm.html:951-968): an airborne fish flees the player
  inside the flee radius, accelerating away at `max(min, base − flee·fatigue)` (×6
  horizontal, ×4 vertical of the same speed scalar), accumulates `flee` fatigue,
  then tires: fatigue decays by `0.4^dt`, gravity pulls it down, and floor contact
  flips it to `rest`. Drag `0.985` per frame, frame-normalized as `0.985^(60·dt)`;
  arena walls bounce at half restitution (swarm.html:963).
- **School** (swarm.html:970-981, the boids core): a resting fish steers by direct
  position nudges only — cohesion toward the centroid of neighbors inside the
  school radius (rate 0.9 plane / 0.55 height), separation from neighbors inside
  the separation radius (rate 0.6 plane / 0.35 height), plus the identity wiggle
  `sin(t·7 + x·0.05)·amp·dt` along world X, then the floor clamp. Never touches
  velocity: a resting fish has none, exactly like the source.
- **Pheromone trail** (swarm.html:842-851 drop law :1113-1121): the horde steers
  at the freshest trail point when `life · (1 − manhattan/radius)` beats the
  score floor 1.2, else straight at the player. Walking drops points with life
  2.5; the loud action (firing, the harvest-header analog) drops life 5. Cap 140.
- **Crop loop**: kills drop fish with the toss law (swarm.html:631) — random
  horizontal velocity, upward start; 30 unharvested → the "the fish stir..." warn
  (swarm.html:1074); population cap 45.
- **Scale law (the port mapping, one place)**: original units are canvas pixels on
  a 2400-wide world; the port arena is 90 studs and the port's established speed
  ratio is ×0.08 (player 200→16). Lengths scale ×0.125–0.25 to stay playable:
  flee 95→14, catch 15→3.5 (the port's existing touch collect), school 155→20,
  separation 15→3, trail radius 300→38, wiggle amp 6→1.5, toss/gravity ×0.08.
  Rates, thresholds, lives, the 1.2 score floor, drag, the 0.4^dt fatigue decay
  and the boids structure carry over verbatim. Not cloned here: the header
  harvest row, the county-line survey, and THE FISH boss duel (45 stays a cap,
  not a trigger) — separate mechanics, open moves.

## 4 · WHAT WE DO NOT CLONE (and why, on the record)

- MM2 role rounds: social deduction needs a crowd; at our size the Hall's Roshomon
  survey IS our deduction loop, and it is more ours.
- Jailbreak asymmetry: two-role balance is a live-ops job we cannot staff yet.
- Adopt Me trading: open trading without an economy team is a dupe exploit.

## 5 · THE DETAIL BAR (how this doc was made, so we can repeat it)

1. Name the exemplar ("Kimi/Claude detail" = numbers per mechanic, tables per system).
2. Pull the live board (who is on top RIGHT NOW, with CCU).
3. Read the wiki of the #1 game before opining (the carry penalty numbers came from the wiki, not memory).
4. Every wheel lands as: source → skin → file → exact numbers → status row in the queue.
