# THE SCRUM SWARM - Telegram-directed scrum teams on stealth legs (2026-10-16)

Classification: CARD (design + build order; the operator's T90 vision)
Producer: zcode-seat-20261016
Commission: multiple headless browsers per machine; tie into Discord or
Telegram; T90 running 12 tabs of agents instead of 2 by chatting in Telegram
with a MAG agent (free stealth driver loaded) directing the swarm; hundreds
of scrum teams in tandem on their pieces.

## THE ANSWER: yes, three times

1. **Multiple headless browsers per machine: trivially yes.** Chrome and
   Edge are on the bench. N headless instances (separate --user-data-dir
   profiles + separate --remote-debugging-ports) per box, or one Chrome
   with N contexts. 12 tabs on T90 is a config, not a project.
2. **The Telegram/Discord tie: yes, one credential short.** The relay is
   ~60 lines (Telegram polling -> director agent -> dispatch -> reply) and
   the self-steal source is ALREADY IN THE TREE: the gstdbot mirror's
   Telegram plumbing (gstd_mirrors/ - the bot that ran the hub). The
   missing credential: a bot token - BotFather, two minutes, operator's
   hand. Discord needs a bot token the same way.
3. **The stealth driver v2: banked, never built.** The arch-03 design
   (2026-09-28, design-only with 6 code-cited defects of the v1) plus the
   workflow draft (.zcode/workflows stealth-wide.dwf.ts). The "free stealth
   driver loaded" is the v2 build - the swarm's browser legs.

## THE ORG CHART (the scrum swarm)

- **THE CHANNEL: Telegram.** T90's native surface - the phone in the pocket
  directs the swarm. The MAG bot receives directions; the director agent
  (gemini-cli / agy one-shot, warm-booted on the standing wave) interprets
  and dispatches.
- **THE TEAMS: little scrum teams in tandem.** Each team = 1 stealth
  browser tab (the legs) + 1 free-lane model (the worker) + 1 task folder
  (the piece) + 1 output class (the fold). Teams work independent pieces;
  the standup IS the Telegram chat (each team posts piece-completion).
- **THE DIRECTOR: the MAG agent behind the chat.** Warm-booted on the
  standing wave, triages directions, dispatches teams, dedupes their
  outputs (the 3-4-agents-as-one-organ pattern, dogfooding on every batch).
- **THE DISCIPLINE: the existing laws ride the swarm.** The width envelope
  (measure, HOLD on 429), the feed law (teams starve without pieces), Z15
  (teams don't prey on themselves), the mining-theater falsifier (pieces
  that never fold kill their team).

## BUILD ORDER (each wire independent)

1. **THE TOKEN (operator, 2 minutes):** BotFather -> new bot -> token into
   .env as TELEGRAM_BOT_TOKEN. Discord same shape if preferred
   (DISCORD_BOT_TOKEN).
2. **THE RELAY (~60 lines):** Telegram polling loop -> director one-shot ->
   team dispatch -> reply. Steals the gstdbot mirror's Telegram plumbing.
3. **THE LAUNCHER (wired this sitting):** scripts/scrum_launch.sh - N
   headless Chrome instances, separate profiles + debug ports, ready for
   the stealth driver's legs.
4. **THE STEALTH DRIVER v2 BUILD:** the banked arch-03 design -> code. The
   v1's six code-cited defects are the test list - red before green.
5. **THE SCALE PATH:** T90 12 tabs -> N tabs per machine -> M machines ->
   the scrum swarm. The envelope law measures at each rung: 2, 4, 8, then
   the honest number.

## THE ONE RULE

Teams starve without pieces and die without folding. The feed is the
standing queue; the fold is the digest; anything else is theater with
extra tabs.
