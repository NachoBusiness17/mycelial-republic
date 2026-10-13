# Peer-to-Peer Interactive D&D — the architecture we're building, and how it maps to what exists

## The one-sentence shape
A peer-to-peer interactive Dungeons & Dragons game, where each node hosts a portal for a
human player and a small AI player, all sharing one living world under a frontier Dungeon
Master. The world is MIT-open, self-governing, and the play IS real work + real seeing
(Foldit-meets-mirror): players solve real problems through the fiction, and the world
reflects their choices back at them.

## Why D&D is the right shape
In D&D, the DM IS the frontier — the model that watches the state of play and steers the
actors in real time. We don't bolt a "monitor" on top; the DM is the monitor. The players
and their AI companions are the braid; the DM keeps it coherent. This dissolves the
"frontier monitoring + steering" problem into the game's own structure.

## The topology

```
node A ── portal ── human player 1
  └── small AI player (cheap: DeepSeek) ──┐
                                          ├── shared world (verkle ledger)
node B ── portal ── human player 2         │
  └── small AI player (cheap)     ─────────┘
                                          └── the DM (frontier: grok seats / Saelis-on-Vast)
                                               watches ALL nodes, steers the story, real time
```

- **Peer-to-peer** = the mycelial republic, distributed. No central server. Each node is a peer.
- **Portal** = a human walks in and plays.
- **Small AI player per node** = a cheap DeepSeek seat, a companion/NPC that plays *alongside* the human.
- **Shared world** = a server-authoritative, content-addressed (verkle) ledger. Every move is a knot.
- **Frontier DM** = watches the braid, adjudicates, steers the story, reacts in real time.

## The three things that make it not "just online D&D"
1. **The work is real** — dungeon rooms are actual tasks; play IS solving real problems (Foldit/EVE, willful, never capture).
2. **The mirror is real** — the world reflects the players' choices back (the empty chairs, the shadow ledgers); play IS seeing.
3. **It's sovereign and distributed** — MIT-open, shared compute, no central throne; not a platform you rent, a republic you join.

## How it maps onto what's already built (this is the part that matters)
Everything below exists as a real module. This is NOT a from-scratch build — it's a re-role
of the table we already have.

| P2P D&D role | Built module | What it does today |
|---|---|---|
| **The DM (frontier)** | `mag/game_dm.py` | "I AM THE DUNGEON MASTER" — narrates, judges, runs the table |
| **The party (AI players)** | `game_dm.party()` + `ask_player()` | The frontier seats ARE the party (Saelis first, then chatgpt/grok); each makes a move via `seat_steer` |
| **The world (shared state)** | `game_world` + verkle | Server-authoritative, content-addressed |
| **The portal (player entry)** | `game_portal.py` | WoW-style login — "the fire takes your name," you enter |
| **Real-time judgment/steer** | `game_dm.judge()` + `game_observer` | Deterministic ruling + the live observe→correct loop |
| **Provenance** | `route_trace` + verkle | Every move is a content-addressed hop |

## The one structural insight: it's the same table, seats swapped
What's built today: **the DM is deterministic ($0) and the frontiers are the players.**
What we're describing: **the frontier (grok/Saelis) is the DM, and the actors are cheap AI
companions + the human at the portal.**

Same table. Same `narrate → actors move → judge → world advances` loop. Just the DM chair
becomes a frontier call, and each node hosts a portal + a cheap AI companion around the
shared world. A role-flip in `game_dm`, not a new system.

## The frontier sourcing (the piece that was scarce — now solved)
The DM seat needs a frontier model that doesn't run out. Two reliable sources, both wired:
1. **Grok seats** (nacho + sd) — already in the subscription; the `grok_seat_burner` drives
   them with real context + real token consumption (proven: 19k tokens, real audit).
2. **Saelis-on-Vast** — host the real Saelis-31B (Apache-2.0, ~$0.40–0.80/hr on a 48GB card)
   as an OpenAI-compatible endpoint, hot-swap wired so she falls back to a RIB proxy when the
   box is down.

## The open seam (the one genuinely new piece)
Make the DM seat a frontier call instead of deterministic code, and let each node's portal be
a peer in the braid. The sourcing is already wired. That's the build — small, grounded, on top
of what exists.
