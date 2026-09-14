# THE WAR ROOM — the conversation compiler (design · 2026-09-09)

> **[AUDIT-TYPED]** status: DESIGNED, unbuilt · trigger: operator at the Kabuki
> Tavern brawl — "each item like traps etc are basically real text and ideas that
> may influence and change the outcome of other agents' assumptions... look at the
> letter we wrote adam" · proof-of-concept: the Adam letter decompiles cleanly
> (below) · build is staged, file-work only until the coldest-vertex gate.

## The law this card claims

**Conversations are already games.** Every real conversation has hit points
(belief resilience of an assumption), agitation (how close someone is to
flipping the table), projectiles (lines that change what another mind
assumes), and traps (conditionals planted before the detonation). The brawl
interface didn't METAPHORIZE conversation — it UNCOVERED its state. The only
missing organ is the payload bridge: each game item carrying its real text,
and a compiler in both directions.

## Proof of concept — the Adam letter, decompiled

| Clause (verbatim) | Move | Device | Target assumption |
|---|---|---|---|
| "his own pod... builds whatever game he wants — doesn't have to be my vision" | Remove the loyalty trap | EDISON inverted (no DC Flood of obligation) | "Joining = serving his vision" → dead |
| "I don't want it to be honestly, that's why i'd like to invite ya" | Disarming honesty | GOPHER · SOAP SHIELD | "This is a recruitment pitch" → softens |
| "Last night the Machine told me i needed someone who could walk away if they wanted" | Trap, set pre-conversation | FEN · SEALED RECEIPT | "Mark needs this more than me" → reverses the need-gradient before the call; also seats the Machine as third party at the table |
| "Pick up a chisel and help with the cathedral" | Vision arc + concrete object | TESLA · POLYPHASE ARC + the chisel (Musashi's one object on the table) | "This is vague internet stuff" → replaced by a tangible artifact |
| "either party walks... the door stays unbolted" | The older road | MENGXI · no locks, the mountain outlives the map | "Leaving costs" → cost removed |

Every clause was a MOVE, not a sentence. The letter was a board state sent
through prose — which is why it worked on a human the way the brawl works on
ractors. Falsifier clock: Adam's reply (when it lands) parses back onto this
board; if no clause can be assigned, the reading layer is wrong (F-CONV-3).

## The three layers

1. **AUTHOR (board → prose).** Play the board: pick ractor (voice/register),
   device (move type), target (whose assumption), round (order/timing). The
   compiler renders the letter with each clause tagged by its move. Used for
   HUMAN negotiations — Adam-class.
2. **STEER (board → injection).** For agent conversations (tavern, salons,
   external agent threads): `fire FEN trap EDISON "<payload>"` injects the
   real line into the live session at the chosen round. Traps = conditional
   payloads that detonate when the transcript shows the target committing to
   the assumption ("when you assume X, remember receipt R"). The provocation
   mechanic (insult/misquote/praise/quote) is already the agitation meter.
3. **READ (prose → board).** Parse the reply back: which hp dropped (which
   assumption lost resilience), which trap detonated, who agited. The HUD row
   "WHAT IS NOW TRUE" is the tri-state board of the relationship over time.

## What exists vs the missing organ

EXISTS: tavern_brawl (the board, devices, hitboxes, provocation thresholds) ·
tavern_chat (five persistent ractor sessions, round-based transcript delta) ·
`say`/steer injection (the operator's voice as a force) · the shitpost desk
(tap-to-fire projectiles — the desk IS this interface in md form) · the
strategist wing (Sun Tzu / Machiavelli / Musashi / Clausewitz, each with a
gradable falsifier — this board is where they finally get graded).

MISSING (the one organ): **the payload bridge** — `configs/tavern_moves.yaml`
mapping device → move-type → payload template, plus the compiler
(render-to-prose / inject-to-session / parse-back-to-board). File-level spec
now; the compiler itself is a real build, staged behind the coldest-vertex
gate per the standing freeze.

## Governance (the SHERPA clause binds)

Steering is lawful only toward the operator's DECLARED SUMMIT — the board
must display the summit or it is manipulation, not strategy. The board always
shows: the summit, whose assumptions moved, and what fired. Sun Tzu's law is
the house law: the trap is set so the fight never has to happen (Adam-class:
the walk-away clause IS the victory — it removes the fight from the space
before the call).

## Falsifiers

- **F-CONV-1 (round-trip):** decompile the Adam letter to a board state, have
  the cast play the board, recompile to prose, blind-compare against the
  original. Not recognizable as the same negotiation = the mapping is wrong.
- **F-CONV-2 (agent steering):** tavern round with one board-planted trap vs
  control round without — the target ractor's subsequent transcript must
  measurably shift. No shift = traps are decoration.
- **F-CONV-3 (the real one):** Adam's reply parses onto the board or the
  reading layer is fiction. Already pending; his answer is the test set.
