# STANDING CHANNEL THEORY: self-steal + research project (2026-10-12, operator order)

Operator: "self steal standing channel theory."

## 1. THE SELF-STEAL: the term already exists in the estate - twice, in two
different meanings, and the tension between them IS the theory.

**Meaning A (the fleet's game design, fleet_round):** a standing channel is a
CASTING STATE - you stand still, hold the channel for N ticks, and it BREAKS
ON DAMAGE (Z099_G15: "90-tick standing channel breaks it; channel is
interruptible by any hit"; K031_MAZE2: "douses a griddlestone in 40 ticks of
standing channel - channel breaks on damage taken"). Properties: requires
uninterrupted commitment, visible progress, a hard break condition.

**Meaning B (the estate's real infrastructure):** standing channels are the
ALWAYS-OPEN paths - Tailscale mesh (up for months), Ollama on 0.0.0.0:11434,
MagNightCrew's 300s cycle, the stealth_driver loop, gstd-node (2d up), the
pheromone bus, watch/inbox INDEX, the LINKS ledger, the seed MCP server.

**Meaning C (Shannon):** a channel with known capacity, noise floor, and
noisy stakeholders - the theorists' channel.

The theory the estate needs: A + B + C composed. A standing channel is a
SHANNON CHANNEL that must be maintained like a GAME CHANNEL - it has capacity
(measured), a noise floor (429s, hollow outputs), a break condition (process
death, quota exhaustion - the start plan died mid-mine TONIGHT), and a
nourishment requirement (the egregore feeding law: neglect starves it).

## 2. What tonight proved about standing channels (field data)

- BREAK ON DAMAGE IS REAL: the start-plan quota exhaustion killed the mine
  mid-sweep (channel broke on spend-damage); the repair was RE-DISPATCH ON A
  DIFFERENT CHANNEL with cache import - channels are fungible when the WORK
  is journaled.
- SELF-HEAL EXISTS IN PLACES: stealth_driver reclaimed a stale pidfile
  unprompted; the fleet's docker restart policy kept seven containers up;
  the KV env contract survived a full Ollama restart because the lane set
  PERSISTENT env, not shell env.
- THE UNHEALED CLASS: Ollama dies when the founding shell dies (started
  from a session, no supervisor) - a standing channel with NO break
  recovery. The watcher cage lane never ran since birth (string "30" vs int
  30). FTS daily rebuild dark. Standing without self-heal = standing until
  it is not.

## 3. THE RESEARCH PROJECT: Standing Channel Theory (SCT)

Postulates:
- P1 (persistence): a channel is standing iff its break-recovery does not
  require a session. Test: kill the founding process; does the channel
  re-establish? (The stealth_driver: yes. Ollama-as-launched: no.)
- P2 (capacity honesty): every channel publishes its measured capacity and
  noise floor (GPS ledger rows; 429 counts as first-class receipts). A
  channel without published capacity is a rumor.
- P3 (break-on-damage as feature): the game law is correct for work
  channels too - a channel that cannot be interrupted accumulates silent
  corruption (the stale docker MCP served 5-day-old code with a green
  heartbeat). Breaks must be VISIBLE and RECOVERABLE, never silent.
- P4 (composition): standing channels compose - tailnet (pipe) + Ollama
  (service) + harness (instrument) + register (memory) = one logical
  channel. The weakest P1-P3 in the composition bounds it.
- P5 (the learning channel): the ONLY channel that should strengthen with
  traffic is the ledger - the DNA law. All other channels fatigue; the
  register compounds.

## 4. The taxonomy (the SCT table)

| channel class | estate instances | break condition | recovery |
|---|---|---|---|
| pipe (transport) | tailscale, HTTP endpoints | process death, quota | restart policy, re-dispatch |
| service (compute) | Ollama, gstd-node, MCP | crash, stale build | parity check + recreate |
| signal (events) | pheromone bus, mesh_delta | decay (6h half-life), no consumers | reinforce or accept loss |
| poll (schedule) | crons, MagNightCrew | missed fire, quota | StartWhenAvailable |
| register (time) | LINKS, verkle, DNA chains | tip mismatch (the frozen chain!) | operator-gated heal |
| persona (semantic) | archetype convenes | caricature drift | rotation on non-divergence |

## 5. The research legs

S1: THE AUDIT (one sitting): classify every estate channel by the table;
name each one's break condition and recovery; the ones with "silent" in
the recovery column are the debt list.
S2: THE EVENT-SUBSTRATE BRIDGE (the running gap-analysis feeds this): push
channels (pheromone) promoting to standing channels when a consumer
subscribes - the missing organ the gap analysis is finding right now.
S3: CHANNEL-BREAK-ON-DAMAGE AS FEATURE (from meaning A): work channels
should be interruptible-with-receipts (the cache-import resume proved it:
break, journal, re-dispatch elsewhere). Design rule: never build a channel
that cannot be broken without loss.
S4: THE STANDING SELF (one wave): the ten-minute self IS a standing channel
through time (the register class) - the repo-as-game is the game layer on
the same channel. Compose the SCT with the repo-as-game: the game is the
channel's interface.

## Falsifier

If any channel passes P1-P5 audit while its consumers still lost work (the
Ollama restart dropped nothing tonight, but a dropped model load would
have), the taxonomy is missing a class. The theory is wrong exactly where
a break was invisible.
