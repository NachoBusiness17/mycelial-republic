# INTAKE — FRONTIER SOULS · Adam's game design bible · 2026-09-15

**Source:** Adam (collaborator, TEAM.md roster) — 7 pages of design notes + world sketch + weapon sheet, relayed by the operator with the one-line thesis: *"every step you take is moving the level along. it doesn't matter which direction you take as the world advances with each step."*
**Companion link:** @jiqizhixin/2099641851762610232 — "Mechanist" (Zhejiang Univ.): AI studies its own internals — discover behavior → locate mechanism → causal verification → active intervention → capability improvement. Same loop shape as our self-steal doctrine: the game is the mechanism probe, the fleet is the experimenter.

---

## 1. The pitch (Adam, verbatim spine)
"Frontier Souls will be a western roguelike game. FTL meets the wild west. Player wakes up in the middle of the desert with his soul taken by death and left for the buzzards. You must race to catch up to death before your body decomposes too much! You must kill enemies along the way to replenish your life force."

**Load-bearing laws (his emphasis):**
- **PERMADEATH.**
- **EVERY ENEMY CAN BE THE END.** "Dark souls director wanted to make every enemy feel like it could kill the player. I want that feeling. I want every enemy to be SMART... if they let their guard down I want the simplest creature to be able to kill the player."
- **Every step is progressing the levels. No direction is the "correct" path.** Every event is randomly linked to the number of steps taken from the start.
- **MAKE THE PLAYER FEEL SMART** — choices with consequences: see an item you can't reach; take the wrong path and it closes until the next playthrough.
- **NOT CARTOONISH — gritty and bloody** (marked "very important to me").
- **The Diablo hue trick:** "changed the entire hue of the colors and it MADE the game FEEL DIABLO. I want this game to feel dried out husk of color... Lots of gray and browns. Like the arizona wilderness."
- **Minimal music** like Dark Souls — only bosses/cutscenes. Wind, dust, screeching birds of prey, emptiness. Lots of cacti.

## 2. World model (from the sketch)
- **Level 1 is the canyon** — you wake at the bottom, left for dead. Hidden tutorial: jump/dodge/attack your way out. Maybe notes showing the way, "maybe it would be better to have none of those."
- **The world is concentric rings**: LVL 1 (canyon, center) → LVL 2 … LVL 6 → **Death** at the rim. Start at the middle, walk ANY direction outward to level up; the rim is the endgame.
- **Dual clock:** radial distance = level ring; **total step count = event scheduler** (events randomly tied to steps-from-start, FTL-style).
- LVL 2+ has random events that gate quests on levels 3–6; they won't always appear (RNG per player → replayability). At least **4 storylines**, must find part 1 to start, sometimes won't appear at all.
- Achievements per character; **secret characters** shown locked-but-visible before unlocking (hinting they exist).

## 3. Fauna — passive but interactable (his list, verbatim)
- **Tumbleweeds** — cannot be attacked, hurt you on contact.
- **Pack rats** — cannot be attacked, bite you.
- **Scorpions** — attackable, hard to hit, sting you.
- **Rattlesnakes** — highly dangerous, **50% chance to kill you instantly**, attack only if you come too close; **rattle sound when approaching their space.**

## 4. Non-passive enemies
- **Coyote pack** — attack in packs, try to surround and hit from all sides; weak individually.
- **Lone gunman** — small chance to meet; beat him → fire-rate mod for your gun.
- **Cowboy gangs** — most common enemy; one strong OR groups of many weak — both should feel like a challenge that could wipe your run.
- Death (boss): tall skeleton, black robe, massive barbed scythe, throws daggers when you're far.

## 5. Systems
- **Soul Essence** (the souls): death leaves you in the canyon — "you wake up the next day with a tiny scrap of your soul. Just enough to keep you attached to your mortal body." Enemies drop SE; without it you cannot level up. SE levels guns and stats. **Lifeforce slowly fades — a death timer** counting down to when your soul fades completely; essence refills it. "The stress to keep moving is the death timer."
- **No items — gun parts instead**, altering how the gun shoots/does melee. Shot COLOR communicates the mod (red = fire, whitish-blue = lightning, etc.). Blade parts get a visual representation. "It's ALWAYS fun to find new weapons. Lets really implant that."
- 2–3 gun frames per character for playthrough variety; sprites per character.
- **Factions:** NPCs you can meet; helping Red makes Blue hostile on sight.
- **Puzzles** solvable but challenging; chest visible from one area, accessed from another (hidden from the access side).
- **Random encounters / safe havens:** a place you KNOW there are no enemies — no save, just safety.
- **Wishing well** — find it, get one "wish": free level-up or random mod part.
- **Oasis** — free HP / soul essence refill.
- **Traveling merchant** — one mod item or a package of soul essence.
- Roguelike meta-progression: "It's a debate. Could go either way. My instincts say no. (games like Slay the Spire prove me wrong tho)" — **open question, Adam decides.**

## 6. Roster (Adam's)
Starters:
- **Allzaban** — tall thin man, long overcoat, twin pistol-daggers. "Steampunk magician meets the wild west." Light/fast: fast attacks, quick dodges, light damage.
- **The Wolverine type** — grizzled Logan-meets-cowboy, shotgun-axe. Medium speed/damage.
- **Tiny girl, massive cannon hammer** — strongest of the group, slowest. ("Doesn't need to be a lolita type. I like the idea of a tiny girl wielding a giant cannon hammer.")
- **Death** — tall skeleton, black robe, large barbed scythe.

Secret unlockables:
- **Cowboy Monkey** — very fast pistol, dagger out of the grip (high speed, low atk). Unlocks by finding his coconut house and defeating him. Random encounter LVL 4+, medium difficulty, 50% per playthrough.
- **Captain Nishra** — ship captain lost at "sea"; captain's foil + old-school blunderbuss (medium/medium). Unlocks at her scuttled ship in the desert. LVL 5+, hard, 20%.
- **Shinra Khan** — rocket-launcher freakazoid, slow melee; very strong, vulnerable window after firing. Unlocks at his Arena. LVL 5+, hard, 20%. **Strongest char in game.**
- **Riverwind** — Plainsman, incredibly strong bow with a blade on it. Unlocks after unlocking every other char, then finding his quest. Above-average everything.

## 7. Weapon sheet (sketch stats)
- **Twin blades:** low damage, high attack speed, many combo attacks, longest combo chain, very hard to master, weakest DPS on regular attacks.
- **Shotgun axe:** medium damage/speed — the middle ground, always strong, hits hard; combos simple and strong.
- **Cannon blade / hammer:** very high damage, slow swings and slow fire time; slow and devastating.
- **Riverwind's blade-bow** (free-hand, spiked grip); **fencing sword — very high crit damage (highest in game)**; Shinra's RPG: ~10m range, time-consuming but very strong.

## 8. Build decisions taken in the v0 spike (this round)
- Radial rings 420px each, canyon pit at center with 4 passes (any direction works), rim arena at ring 6+.
- Dual clock implemented: `steps` (24px = 1 step) drives the event scheduler; radial distance drives the ring/level.
- Timer + essence + XP are one economy (his death-timer stress), death = wake in canyon with a scrap.
- All 4 fauna implemented to his exact rules; coyote surround; gang leader-or-lackeys; lone gunman duel → fire-rate mod.
-mods recolor the shot (his color language); well/oasis/merchant/grave-chain present (chain 1 of 4 seeded).
- Desert hue locked: grays/browns, film grain, blood persists, buzzards circle when the timer runs low.

## 9. Open questions for Adam (next pass)
1. Meta-progression: his instinct says no, StS says yes — needs a ruling (spike persists unlocks only, no stats).
2. Names for the three starters (Allzaban is named; I provisionally used MARROW / NELL — his call).
3. The other 3 storylines (chain 1 "the stranger's grave" is seeded).
4. Faction roster + what "helping" looks like mechanically.
5. Gun frames per char (2–3) — which parts are frame vs mod.
6. Jump vs roll: his tutorial lists jump AND dodge — spike uses one dodge-roll for both; does he want a distinct jump?
