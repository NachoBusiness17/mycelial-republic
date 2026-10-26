# MUD ENGINE STEAL MAP — filed from RyanSael's list · 2026-09-23

**Source:** operator + x.com/RyanSael/status/2102591147927654847 (comprehensive
open-source MUD inventory). This is the Living Mud's engine selection matrix.

## THE PICK: Evennia (Python)

**Why:** the estate is Python-first. Evennia has a built-in web client (no
telnet), SQL persistence, Twisted networking — and the critical line:
"easy to hook AI/LLM stuff into." That's the Mantella move, native.

Our architecture maps directly:
- Engine owns truth = Evennia's command parser + typeclass system
- Model narrates = an LLM hook on the narration pipeline
- World memory = Evennia's SQL-backed attributes + our knot-chain layer
- The dnd_classic_stub + tavern + beacon rooms port as Evennia scripts/objects

**Install:**
```
pip install evennia
evennia --init mymud
cd mymud
evennia migrate
evennia start
```
Web client at localhost:4001, game at localhost:4000.

## THE FULL INVENTORY (filed for the steal ledger)

| Engine | Lang | Stars | Why it matters |
|---|---|---|---|
| Evennia | Python | 2,106 | Framework + web client + AI-hookable. THE PICK. |
| CoffeeMUD | Java | — | Full Diku in a box: combat, crafting, email, IMC2. |
| Ranvier | Node.js | 857 | Light modern JS engine. Good if JS-native. |
| tbaMUD | C | — | Living CircleMUD line (classic Diku). |
| DikuMUD3 | C | — | Modern Diku with HTML + websockets. |
| FluffOS | C/C++ | — | LPMud driver (Discworld-style LPC worlds). |
| GoMud | Go | — | Quick to stand up, playable default world. gomud.net |
| EllyMUD | TypeScript | — | Telnet + websocket + React world builder + MCP for AI. |
| OpenRPI | C++ | — | RPI (permadeath, classless). Shadows of Isildur lineage. |
| awesome-mud | list | — | github.com/mudcoders/awesome-mud — the master index. |

## Playable open-source games
- LuminariMUD — Pathfinder/d20, luminarimud.com:4100
- GoMud demo world
- Arx after the Reckoning (Evennia, source published)
- Stock worlds: CoffeeMUD, tbaMUD, Circle, ROM, SmaugFUSS

## Clients
Mudlet (Lua) · TinTin++ · Blightmud (Rust) · Evennia web client

## Practical picks per use case
- Build something modern: **Evennia**
- Game that fights and loots tonight: **CoffeeMUD** or **tbaMUD**
- JS/TS native: **Ranvier** or **EllyMUD**
- Classic C: **tbaMUD** / **DikuMUD3**
