# ONE_SHOT_GAME.prompt.md — the single-file playable shape

AMENDED from the verified wave report (watch/inbox/STEAL_ONESHOT_PROMPTS_20260924.md):
the viral one-shot prompts share SIX moves — (1) one self-contained HTML file,
(2) a bullet feature checklist, (3) juice as an explicit quality bar
("smooth and elegant", "Make it hilarious to play"), (4) a stated interaction
loop ("Clicking should cycle..."), (5) NAMED aesthetic references ("GTA
1-style", "8-bit"), (6) multi-turn repair = "keep comparing against the
reference and fix differences". Honest note from the archaeology: the famous
"GTA 1 one-shot prompt" circulates as folklore — no canonical published
prompt text exists (HN thread 43163011 datable, prompt not archived). The
canonical verbatim opener is Alex Albert's weather-card demo
(x.com/alexalbert__/status/1894426652429738349). Collections worth mining:
AnthemK/Prompt-to-Play, xiiyioozzz/opus55-3d-games, goldiebench.com,
mattgodbolt/daredevil-demis (one-shot 6502 game + MCP eval harness).

---

Build a complete, playable game in ONE self-contained {{HTML_FILE | LUAU_MODULE}}.
No assets, no network, no build step. A stranger must be playing in 10 seconds.

## CONTRACT

1. **Playable immediately**: title overlay → click/press to start → real
   loop → death/restart loop. No menus beyond start.
2. **Controls on screen**: the control map renders inside the game, first
   frame. {{CONTROLS: WASD/Space/Shift...}}
3. **Juice is not optional, enumerate it**: screen shake on hit, particles on
   every kill, procedural audio (oscillator, no files), hit-flash, freeze-
   frames on big hits. Every event emits particle+sfx+shake as one bundle
   (the js13k law, phoboslab lineage).
4. **One sentence of aesthetic**, not "make it good": e.g. "Vampire Survivors
   density × disco strobe × the swarm's taunts".
5. **Seeded runs**: RNG seeded; the seed displays; same seed = same game.
6. **Score that reads at a glance**, high score persisted, difficulty curve
   with explicit numbers (spawn interval, ramp per level).
7. Fixed sections in your answer: `## The Game` (30 words) → `## Aesthetic`
   (the sentence) → `## Code` (complete, no ellipses) → `## Curve` (the
   difficulty numbers) → `## Next Three Hooks` (what a second prompt adds).

## THE BRIEF

{{ONE PARAGRAPH: genre, fantasy, the one memorable beat}}

## THE SIX MOVES, AS A CHECKLIST (verified anatomy)

- [ ] one self-contained file, no assets, no network
- [ ] bullet feature checklist (the model ticks every line)
- [ ] juice named as the quality bar, with the register ("make it hilarious to play")
- [ ] interaction loop stated mechanically ("clicking cycles X")
- [ ] aesthetic named by reference ("GTA 1-style", "8-bit", "Vampire Survivors density")
- [ ] multi-turn repair move: "keep comparing against the reference and fix differences"
