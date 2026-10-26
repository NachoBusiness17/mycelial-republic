# FW-40 — Ascension ladder balance sweep (StS scaling curve)

**2026-09-28 · Q-027 (burn-reset gopher) · task: fifty-wide 09-17 board §H**
Sweep script: `watch/inbox/burn_reset_20260927/queue/Q_040_ascension_sweep.py` — **ran this
session** (repo venv python); every number below is its output. The script reads the curve
verbatim from `dashboard/static/games/mud.html` (spawnEnemy :776-794, spawnBoss :812-819,
champion :850-852, player reset :2507-2518, Vigor :1841) and the player-side XP/level math
(xpNext ×1.5 from 20, walker 8 xp).

## The curve as shipped

`a = min(ng,20)`; `hpMult = 1 + a·0.15 + ng·0.05`; `dmgMult = 1 + a·0.22 + ng·0.08`; enemy
`speed = min(base.speed · hpMult, 220)` (mud.html:794 — speed rides the **health** multiplier).

| A | hpMult | dmgMult | walker dmg | hits→kill 100 hp | walker spd | champion (k8 chassis) hp/dmg |
|---|---|---|---|---|---|---|
| 0 | 1.00 | 1.00 | 14 | 8 | 70 | 234 / 25 |
| 5 | 2.00 | 2.50 | 35 | 3 | 140 | 468 / 63 |
| 10 | 3.00 | 4.00 | 56 | 2 | 210 | 702 / 101 |
| 20 | 5.00 | 7.00 | 98 | 2 | 220 (capped) | 1170 / 176 |
| 30 | 5.50 | 7.80 | 109 | **1** | 220 | 1287 / 197 |
| 100 | 9.00 | 13.40 | 188 | 1 | 220 | 2106 / 338 |

A20 boss (mud.html:812-819): 2,500 hp, **224 dmg — one-shots a base player**, speed 162.

## Findings

1. **Hits-to-die collapses too early.** 8 hits at A0 → 2 hits by A10 → one-shot at ~A24. The
   whole ladder's drama lives in A0-A8; everything past A10 is the same two-hit death spiral.
2. **Speed double-dips on the health multiplier (:794).** Dodge/rogue reach the 220 cap —
   faster than the player's 200 — at **A4**; walkers cap at A11; everything is capped by A17.
   StS's design never scales enemy speed at all: ascension makes enemies *meaner*, not *faster*.
   Here A4+ outruns the player, which turns kiting (the game's core verb, per the lore system)
   off for the rest of the ladder.
3. **The "20 levels" ladder never tops (:775 comment vs :777-778).** The `a` cap only binds the
   first term; `ng·0.05` / `ng·0.08` climb forever (A100 = ×9 hp / ×13.4 dmg). Meanwhile the UI
   labels every run past 20 "ASCENSION 20" (`min(G.ng, 20)` at :2537 and :2561) — the display
   caps, the difficulty doesn't, and the label lies.
4. **The player has no cross-run answer.** Ascension is the only cross-run progression; each run
   restarts at 100 hp / 200 speed. In-run, a full monastery queue clear is ~222 xp → level 5 →
   all-Vigor 160 max hp. At A10 the walker hits 56 (3 hits even there); at A20, 98 — the champion
   hits 176, i.e. every late-ladder contact is a two-hit death regardless of build. The continuity
   note's "harder hitting (split scaling)" (mud-superhot-adam-access, 2026-09-14) says dmg
   outpacing hp was deliberate — deliberate or not, at ×7/×5 it eats the endgame.
5. **StS yardstick.** Slay the Spire spreads ~20 ascension steps as *separate small modifiers*
   (a curse here, +elite hp there), compositing to roughly ×1.3-2 effective difficulty at A20,
   with speed untouched. MUD's single-formula curve composites to ×5 hp / ×7 dmg / ×3.1 speed at
   its "top" — an order harsher than the design it borrows its name from.

## Recommendation (ruling requested, not landed)

1. **Cap the ladder honestly:** drive both terms from `a` only — e.g. `hpMult = 1 + a·0.10`,
   `dmgMult = 1 + a·0.12` (A20 = ×3.0 hp / ×3.4 dmg; walker 6→4 hits-to-die; champion 176→~85).
   Keep an endless tail only if the label tells the truth (drop the `min(…, 20)` caps at
   :2537/:2561) and the tail is gentler than +5%/+8% per level.
2. **Decouple speed from hpMult (:794):** base speeds, or `min(1 + a·0.01, 1.2)`. Kiting must
   survive the ladder or A8+ is not a difficulty, it's a different (worse) game.
3. **Cross-run counterweight if the tail stays:** ascension-level souls bonus, so the one-shot
   regime buys something besides faster deaths.

## How this was checked

`./.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/queue/Q_040_ascension_sweep.py` —
ran clean this session (full table above reproduced from its stdout). No game code was changed;
the ask is the sweep + verdict.
