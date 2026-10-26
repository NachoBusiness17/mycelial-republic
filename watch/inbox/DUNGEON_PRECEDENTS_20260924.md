# DUNGEON PRECEDENTS — Exanima-style spooky maze dungeon (Roblox)

2026-09-24 · research for game design · sources verified via web fetch/search (some wikis bot-gated; gaps filled from community knowledge, flagged inline)

## 1. Exanima (Bare Mettle, EA 2015) — the atmosphere engine

- **Active-ragdoll physics combat:** no canned attacks; swings are rigid-body motions. Damage scales with **relative velocity/momentum at impact** — footwork, swing arc and turning radius are the skill. Everyone is clumsy, including enemies.
- **Darkness:** near-pitch-black dungeon; **torch/lantern radius** is your vision budget; real-time GI settings exist (PCGamingWiki). You hear enemies before you see them.
- **Senses-based AI:** enemies have sight cones + hearing; they investigate noises, wander, and fight each other. No wallhacks; stealth viable in darkness.
- **Weight:** inventory weight and encumbrance affect movement; gear matters more than stats.
- **Structure:** fixed handcrafted first dungeon (Undercroft) → **procedurally generated deeper levels**; roguelike descent, permadeath difficulty, permanent character unlocks after early content; separate **Arena** wave-gauntlet mode with persistent cash/gear (save files arena001.rsg / exanima001.rsg).
- **Why scary:** sensory deprivation (light+sound only), unpredictable physics resolution (fights end in undignified piles), scarce healing, dread pacing. Sources: https://store.steampowered.com/app/362620/Exanima/ · https://www.pcgamingwiki.com/wiki/Exanima

## 2. Freeze-on-observation (the statue rule)

- **SCP-173:** moves only when **not directly observed** by a living being; observation = line of sight, eyes (not cameras); groups must stagger blinks so coverage never gaps. Source: https://en.wikipedia.org/wiki/SCP-173
- **SCP: Containment Breach** implementation: **blink meter** fills → forced blink (screen flash) = movement window; manual blink on spacebar to control timing.
- **Doctor Who Weeping Angels:** same rule (quantum-locked); cover your eyes and it moves even "while watched."
- **Minecraft Creaking (1.21.4):** shipped mainstream version — frozen while looked at, immune to damage otherwise.
- **Roblox:** SCP games (SCP: Roleplay, Site-76, Area-47-style) recreate 173 freeze+blink; Roblox implementation is standard: server raycast from entity to each player camera + visibility/occlusion check → freeze state machine. (No single canonical game page; pattern is well established in dev community.)

## 3. Roblox horror dungeon precedents

**Doors (LSPLASH, 2022)** — door-by-door hotel descent. Telegraph grammar: **lights flicker = Rush incoming (hide NOW)**; dark room + "psst" = Screech, look at it or eat 40 dmg; **Figure** = blind, hears you, crouch-sneak; **Seek** = scripted hallway chase; **Halt** = flashing "TURN AROUND" corridor; **Eyes** = don't look; **Dupe** = fake doors; **Ambush** = multi-pass Rush. Universal counter = **closets**, but hiding too long gets you ejected (Hide entity) — anti-camping timer. Guiding Light gives subtle blue hints. Sources: https://doors-game.fandom.com/wiki/Rush · https://en.wikipedia.org/wiki/Doors_(video_game)

**Rooms & Doors (rework of nicorocks' Rooms)** — endless room crawl, no items/hiding spots; entities are pure pattern-timing. A-60/MultiMonster spawns behind, rushes room chain (from A-20 here); A-120/Happy Scribble spawns **in the current room**; exclusivity rules (A-60′ vs A-200 never overlap). Source: https://roomsanddoors.miraheze.org/wiki/Entities

**Grace (2024)** — Rooms-like with **detection-state entities**, the best find for our maze:
- **Carnation:** periodic room sweeper; screen-edge tentacles telegraph; must reach yellow-marked hide room, keep moving until then.
- **Slight:** moves while you **look at it** (speed scales with screen-center proximity) — don't stare.
- **Heed:** exact inverse — moves while you **don't** look at it; walls block sight. A literal weeping-angel pair with Slight.
- **Dozer:** appears center-screen, eyes open after ~1.5s → you must **crouch and send zero inputs** (input check, not movement check).
Source: https://grace.miraheze.org/wiki/Entities

**Pressure (Zeal Studios, 2024)** — Doors formula in the Hadal Blacksite: **Angler** rushers + variants (Froger bounces back, Pinkie fast/close, Chainsmoker slow+lingering), **Eyefestation** drains health if you look through windows, **Searchlights** sweep kill-beams (move cover-to-cover), **Wall Dwellers** camouflage as wall art and ambush, **Pandemonium** locker minigame, fake "Good People" doors. Sources: community wiki/search; fragments verified, details from player consensus.

## 4. Lara Croft GO (Square Enix Montreal, 2015) — the puzzle layer

- **Turn-based node graph:** levels are nodes+lines; you move 1 node per turn; **enemies/obstacles take a turn whenever you move or rest** (strict alternation).
- **Pattern enemies:** snakes, lizards, spiders each follow fixed movement rules (some activate on line of sight); killable by **one-use throwable spears** or luring onto hazards.
- **State machinery:** levers shift walls/platforms to open paths; boulders, saw blades, traps as board furniture.
- **No timers — fake urgency:** floors **crack with each successive turn** you stand on them.
- **Curriculum design:** 5 chapters / 40 levels; one new mechanic at a time, later levels combine; set-piece boss chases (giant snake). Source: https://en.wikipedia.org/wiki/Lara_Croft_GO

## 5. Synthesis — our game

**Room/MUD structure (spine):** dungeon = graph of rooms with typed exits; each "floor" procedurally stacked from room templates (Exanima descent). Roblox-scale: 1–8 players, one complex entity per zone, server-side raycasts.

**Keep from Exanima (atmosphere):** torch radius as vision budget; hear-before-see enemy intros; senses AI (sight cone + noise events); scarcity/encumbrance-lite; clumsy = tuned acceleration/friction + recovery stumbles, not ragdoll control.

**Too heavy for v1:** full active-ragdoll momentum combat. **Light version:** wind-up + release swings with weapon-weight swing speed, hit direction from camera/body facing, damage scaling with walk-speed into the swing ("momentum feel"), Roblox ragdoll only on death/knockdown. Fighting stays readable, physics stays cosmetic.

**Puzzle layer (Lara Croft GO):** adopt its *state* ideas in real time — lever/plate state machines per room, fixed-pattern patrol skeletons (predictable, lurable onto spikes), one-use throwables, crack/degrade-floor urgency instead of timers, one-mechanic-per-room curriculum.

**Entity grammar (Roblox precedents):** every killer needs a 2-second telegraph + a universal counter (hide spot) + an anti-camping timer (Doors/Hide). The centerpiece: a **statue Custodian** (SCP-173/Heed rule) — frozen while inside any torch's light radius **or** directly looked at, advances in darkness and blinks; but light+noise attracts the hearing-based hunter. Players must arbitrate light as safety vs bait. That single tension is the whole game.

Word count: ~890
