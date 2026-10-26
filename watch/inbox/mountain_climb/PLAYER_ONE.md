# PLAYER ONE: The Mountain in five minutes

You have never heard of us. Good. This page gets you playing in under five
minutes, tells you what you are holding, and shows you the door to talk back.
No account, no launcher, no installer wizard. If anything below is wrong, the
last section tells you how to tell us so.

## 1. What this is

The Mountain is a small puzzle world about water. You are a shepherd on a
mountain that holds exactly 8 units of water; the Crown at the summit needs 4;
gravity only pulls water downhill, and boiling it is the only way to lift it
back up. It runs singleplayer, always, with zero installs beyond the (free,
50 MB) Godot editor; and if the little server that ships in the repo is
running, the exact same game becomes shared: one mountain, the server keeping
the books and checking every move. Nothing here is decoration or faith: the
water is a real simulation with whole units and no randomness, so the same
moves always build the same mountain, and every claim on this page is one you
can check yourself by running the thing.

## 2. Get the game

**Today (about five minutes, works on a clean machine):**

1. Download Godot 4.3 or newer from godotengine.org (about 50 MB, no account,
   no license server).
2. `git clone https://github.com/NachoBusiness17/the-mountain.git`
3. Open Godot, Import, pick `the-mountain/game/project.godot`, press F5.
   A 1152x648 window opens. You are in.

(Optional, only if you will push changes back: `cd the-mountain && git config
core.hooksPath hooks && chmod +x hooks/*`. That turns on a gate that stops you
from accidentally pushing your own secrets. Players can skip it.)

**The one-click build (when it lands):** run `scripts/build_game.ps1` in the
the-mountain repo root and it drops the exported game as a zip in `dist/`:
download, unzip, double-click, no Godot needed. Honest status: that script has
not landed yet, so this door is closed today and this paragraph is the sign
that points at it. The clone-and-F5 path above is the real, working door right
now.

**Server mode:** solo is the default and the complete game. If someone runs
the server for you (Python 3.9+, nothing to install: `python -m server.auth
server/users.json add <name>` then `python -m server.server`), the same F5
client finds it and joins automatically; point a packed copy at a different
machine with the `MOUNTAIN_SERVER` variable (`host` or `host:port`). Honest
limit for today: the server speaks only to the machine it runs on
(127.0.0.1, on purpose), so think "two windows, one mountain" until the wider
door opens. No server found: the game falls back to solo without a word.

## 3. The 60-second tutorial

Your job: route the water, boil the pools, fill the Crown.

First frame: a dark board with six pools. `spring` on the left (biggest,
starts with 6 water), then `terrace`, `gate1` (a small ringed junction), and
`hollow`; a black WASTE box lower right; the CROWN upper right reading 0/4.
Pipes are lines between pools: bright blue is open, dim is shut, and a gold
dot on the middle pipe means the siphon is primed. You are the white ring; it
follows your mouse.

The controls (wording from the game's own card):

| Key | What it does |
|---|---|
| Mouse | Move the shepherd. Chase a fish until it tires (it turns gold), close in to tag it. Tagged fish are score. |
| SPACE | Boil 1 unit at the nearest pool. It rises as steam and lands in the Crown. |
| E | Open/shut the nearest valve. |
| R | Restart after the win. |
| H | (Extra) Swap the water law: strict open/shut flow vs graded depth and head. |
| T | (Extra) Toggle the terrain board: a real 64x64 Mount St Helens map; click a wet cell to boil it. |

Your first minute, move by move:

1. Chase one pale blue fish until it turns gold, then touch it. Tagged.
2. Stand at the spring and press SPACE. Steam lifts one unit into the Crown:
   1/4. The screen shakes. That is the game telling you the lift works.
3. Press E by a downhill pipe to shut its valve before the mountain leaks
   into WASTE. Nothing is truly lost (waste is a basin; spilled water can be
   boiled back), but every spill is detour you now have to pay for.
4. Repeat to 4/4. A dark win panel covers the screen. Press R and do it
   better: fewer spills, more fish tagged.

Three traps worth knowing early. The `gate1` junction passes only one inlet
at a time: feed it from both sides and it just pools. The bypass siphon needs
2 units pooled at the spring before it can carry water up and over. And fish
gather at the wettest pool, so boiling your fishing hole dry sends the school
away.

## 4. What makes it different

- **The water is real physics.** Whole units, no decimals, no dice. The same
  moves build the same mountain, every run, on every machine. That is why bug
  reports here can say "do exactly this and you will see exactly what I saw."
- **Damage is permanent.** A pipe run at full bore accumulates stress, and
  past its threshold it fractures: closed for good, the valve refuses it
  forever, and the burst sprays onto the lowest ground it can reach. There is
  no undo. A mountain you were careless with stays scarred.
- **The server cannot be cheated.** In server mode your client owns no world
  state. Every action you take travels as a numbered, one-use move that the
  server accepts or rejects (boil a dry pool and it answers `DRY_POOL`); you
  cannot move twice in one tick and you cannot replay an old move. The whole
  session is written as a chain in which each entry seals the ones before it,
  so anyone can replay your game later and get the same mountain, move for
  move. Your play is a record, not a rumor.
- **Nothing asks for your trust.** The one house rule is receipts, not vibes:
  every claim (it runs, it broke, I fixed it) ships with the steps and the
  output that prove it. This page plays by the same rule, which is why it
  tells you which doors are open today and which are not.

## 5. Come talk to us

Everything lives in one public repo: https://github.com/NachoBusiness17/the-mountain.
Start with `docs/ADAM_QUICKSTART.md` (the same five minutes, more detail) and
`ONBOARDING.md` (the full tour of where things live).

If something breaks, open an issue (Issues, New issue) and tell us four
things, the same way the first invited player's pack asks:

1. What you did, in order: where you stood, which keys, which valves. The
   game is deterministic, so exact steps replay exactly.
2. What you expected vs what you saw (a screenshot is fine).
3. Your Godot version (Help, About) and your operating system.
4. Any red text from Godot's Output panel, pasted word for word.

A stranger's first bug report is the most valuable gift this project can get.
You would literally be the first outside player it has ever had, and whatever
confused you is, by definition, the roadmap.

---

*Filing (estate-side, not for the stranger): receipt is this file itself,
`watch/inbox/mountain_climb/PLAYER_ONE.md`, missing-mile item three (one
stranger). Written from bytes this session: the-mountain `README.md`,
`docs/ADAM_QUICKSTART.md`, `game/README.md` (controls and board description
verbatim from the game's own card), repo HEAD `7d5dbe2`. `scripts/build_game.ps1`
does not exist yet; section 2 says so in plain text and its build paragraph
goes live unchanged the day the artifact lands. No commit. Em-dash count: 0.*
