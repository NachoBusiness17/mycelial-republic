# LUMENA AGENT LANE: EXECUTED (operator GO "do it", 2026-10-09)

Operator order: put a single agent into lumena.gg and capture screenshot proof for the
Pierre (PSO-revival) pitch. Offer on record: "put a single agent into Lumena through the
bridge, create a trainer, catch one Lumen, walk Tidemarsh, and the pitch stops being a pitch."

## What landed

An estate agent IS IN THE WORLD, moving, with the world responding to it. Seven proven
frames banked under `frames/`:

1. `01_agent_in_world_firstlight_village.png`: agent in-world, Firstlight Village tutorial
   area, ~744 players online globally at entry (live count kept climbing to 819 during the
   session; HUD DOM read, not eyeballed).
2. `02_movement_proven_market_stall_canopy.png`: agent walked itself onto the market-stall
   canopy (d+s held-key diagonal). Movement method proven.
3. `03_world_talks_back_mira_barrier_dialogue.png`: the golden barrier at the tutorial exit
   REFUSED the agent with live dialogue "Not yet... Mira is still waiting for me." The world
   is objective-aware and talks back to our agent. This is the GWAP pitch in one frame.
4. `04_night_hedge_maze_golden_gate.png`: night-cycle hedge maze, golden gate.
5. `05_crystal_workshop_marker_in_sight.png`: the quest-marked workshop (cyan crystal, red
   "!" marker) one corridor away across the maze.
6. `06_checkpoint_spawn_goodday_dialogue.png`: respawn at checkpoint greeted by NPC
   dialogue "Good day!" (day/night cycle live, timeOfDay 11.28 in the save).
7. `07_rooftop_vantage_daylight.png`: rooftop vantage in daylight (the game's collision
   lets you climb hedges, stalls, and roofs; our agent did all three).

## Method (honest, full disclosure for the pitch)

- Lane: estate browser-use skill (mcp node_repl + IAB tab), NOT the empir3 bridge (its
  navigate defect is still open, see watch/inbox/empir3_babystep1_20261010/RECEIPT.md).
- Entry: lumena.gg, Play, "Show me around first" guest door. No auth, no wallet, no
  account. Guest UID assigned client-side (`guest-ba21e1de-5764-4b99-b171-b6f18231c62e`).
- Movement: the game needs HELD keys. `cua.keypress` taps do nothing (8 identical frames
  proven). `playwright.evaluate` dispatching `KeyboardEvent` keydown, holding, then keyup
  moves the character. WASD are screen-relative (w = away from camera).
- Vision: `tab.screenshot()` + vision-model frame analysis each step, DOM HUD text reads
  between steps.

## Instruments discovered (the real steal for the MMO pitch)

The game is a Three.js SPA with its full state in `localStorage` (readable AND writable
from the page):

- `memedex-save` (v11): zone `firstlight`, checkpoint position `[14.5, 0.39, 18.5]`,
  `pedometer.lifetimeSteps` (our agent banked 112 steps, the game's own movement counter
  = third-party proof we moved), `tutorial.step: "find-mira"`, party/pcBox/inventory
  empty, currencies pixels/prisms/chips 0, codex seen/caught empty, avatar colors, full
  questState, fishingStats, spireRun structure (endgame systems visible in the save schema).
- `memedex-boot-world`: boot-time world position.
- DOM: HUD objective text, NPC nameplates (a "Mira" nameplate element exists in the DOM
  when she is projected near), player-count ticker, `.tutorial-arrow` (WARNING: it points
  at the chat notice, NOT at the world objective; it burned ~40s of guided walking before
  being struck as an instrument).
- Teleport door test: writing `memedex-save.world.position` + `memedex-boot-world` and
  reloading does NOT teleport. The game re-resolves position from its checkpoint on boot
  and overwrites both keys. Door closed (honest negative, banked).

## What did NOT land (honest)

- Mira conversation: not reached. The workshop is across the tutorial hedge maze; blind
  WASD + vision frames solved the village but the maze needs human-grade visual maze
  solving (or a minimap instrument we did not find; only one canvas exists, world-rendered).
- First Lumen encounter: gated behind the Mira conversation (the tutorial gives the catch
  ability there), so not reached. Guest door caps here: "Multiplayer is disabled during
  tutorial" and the trainer identity requires sign-in.
- Trainer creation: requires account sign-in (Google). The guest tour door took us to the
  world without it; creating the account is an operator-hands step (his Google in the
  visible browser) or needs an email lane.

## Why this is already pitch-grade for Pierre

The pitch claim was "AI agents actively playing in a living world." Proven tonight: an
agent entered a shipped multiplayer game world through a browser, moved under its own
keyboard control, got refused by an objective-aware barrier with NPC dialogue, was greeted
by NPC dialogue at respawn, and read + wrote the game's own save state. The missing leg
(Mira, first catch) is a vision-budget problem, not an architecture problem: with a
signed-in trainer and a maze solved once by human eyes, the agent loop closes.

Frames are paste-ready for the Pierre DM: 01 (in-world), 03 (world refusing our agent),
07 (daylight vantage).

## Lane residue

- Browser tab left open on the rooftop vantage (IAB tab 16c12171); no cleanup done, the
  guest session persists in localStorage if he wants to look.
- empir3 bridge nav defect still owed (babystep 2).
- If the operator signs in on this machine, the guest save may be replaced; the trainer
  leg then re-fires from Play with the account door.

Receipt law: numbers in this file are instrument-read (DOM HUD ticker, localStorage save
JSON, pedometer), not eyeballed. Session: sess_bb9913b3 (ZCode browser lane), 2026-10-09
~08:15 to ~08:52 local.
