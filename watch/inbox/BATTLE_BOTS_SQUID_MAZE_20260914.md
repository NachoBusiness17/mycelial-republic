# Battle Bots in the Squid Maze — concept note (2026-09-14)

Operator pitch, verbatim: *"3d printed battle bots in squidgames that people control through our mazes"* + Microduck link + *"rollerskating death bots kind of like the robots in marathon."* Reference image: chibi 3D-printed bots, candy-palette shells, blocky toy guns, glowing eyes.

## The blend

Three ingredients, and we already own the hardest one:

1. **Microduck** (pollen-robotics.com/microduck) — the bot is plausibly real. Open RL stack, train in sim, deploy on hardware, four colourways (Cream, Graphite, Lavender, Sky). Skates ship in the $39 accessory pack. The fiction writes itself: you don't play a character, you pilot a bot.
2. **Squid Game** — trial structure. Elimination rounds, pink guards, candy palette, corporate sponsor voice, one act of mercy per contestant.
3. **Our mazes** — maze_arena (constellation mode, light-bending optics, internal nodes) is the arena. The MUD contributes the horde, torch vision, superhot, the puzzle vault, chain-rewind, and the presence relay on :8766.

## Why skating is the right movement (not just flavor)

- **Feel:** glide + carve + drift reads beautifully even with simple art. Momentum is drama — you can't stop on a dime, walls punish greed, and carrying speed through a bend is the skill.
- **Tech:** no walk cycle, no foot IK. Momentum-based top-down movement is cheap to build and hard to make feel bad. Cheapest path to "this controls great."
- **Differentiation:** every arena shooter has runners. Nobody has skaters in a maze that bends light.
- **Sim2real story:** it's literally what Microduck ships. When a realbot shows up, the trials are already deterministic sims — the policy port is a straight line.

## The maze is the opponent

Our mazes bend light. Players exploit the optics to see around corners; the guards (horde) don't. Line-of-sight gameplay that skating movement exploits — carry speed through a refraction corridor, fade from a pursuit pack the moment you round a bend. The horde already learns (kites→mines, swarms→pack+interception, grudges on survivors): the guards adapt per trial, which is the Squid Game dread.

## Trial ladder — each one maps to something already shipped

| Trial | Already built |
|---|---|
| Red Light, Green Light | superhot powerup (time moves when you move) — invert the framing, ship it as the trial |
| Lights Out | torch-vision raycast cone, maze goes dark, guards hunt the lantern |
| The Bridge / pressure plates | puzzle vault (key → plates → gate) |
| Guards that learn | learning horde + grudges on survivors |
| The sponsor's mercy | chain rewind — one death-undo per run, press T |
| Duels | presence relay :8766 — two browsers already see each other's lanterns |
| The announcer | elder lane already has a surface — it narrates the trials |

## The print loop (progression system)

Every bot is a seed: chassis, skates, head, weapon, procedurally assembled, stats derived from parts. Colourway = paint. Tracksuit number = seed number stenciled on the shell. "Death" = reprint, at a cost — the stakes economy. Parts catalog IS progression. One day the same seed exports an STL; until then the fantasy is fully deliverable digitally, and the same render shows up everywhere (maze, MUD, player files, vislab).

## Hardware reality check

Microduck: $399 pre-order, 25 cm, 800 g, 15 motors, camera + LiDAR + 2 IMUs, 7 policies at 50 Hz onboard, Apache-2.0, MuJoCo, Hugging Face training stack. The "death" stays in sim — realbots do exhibition days, sims run the tournaments. That's the Marathon irony anyway: cute shell, corporate sponsor, staged lethality.

## First stones (browser-only, no hardware)

1. **Stone 1:** skating controller (momentum, carve, drift) in a maze_arena variant, one trial (red light via superhot inversion), bot rendered from a parts seed. Follow the mud.html pattern; edit site/dist source then sync.
2. **Stone 2:** parts catalog + colourways + vislab catalog entry + play.html player.
3. **Stone 3:** relay → duel mode. The second-lantern experiment becomes last-one-standing.
4. **Stone 4:** horde-as-guards learning per elimination.
5. **Later/optional:** Microduck-class realbot exhibition hooks; STL export of seeds.

Team fit: Melissa writes the announcer (elder lane voice — corporate-sponsor dread, mud-tier door, no code). Adam gets player one. Marque gets the parts catalog.

## Open questions

- Walkers-through-walls decision still open in the MUD — the skating controller sidesteps it (glide collision, no legged stepping) but pick one rule for both surfaces.
- Spectator/VIP layer: dashboard exists; presence relay could push a spectate view. Fake-money VIP betting on trials = percolator's play-history weighting, reskinned.
