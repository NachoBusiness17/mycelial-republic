# SQUARE-NAME SELF-STEAL — notation for the house board (2026-09-20, last paper before the window)

Operator's seed, verbatim: *"Once you know the square name you can know the position of each piece in our board — self steal — go parable, smith chart, history of games, history of chess, and all our game prompts."*

Lens set supplied: algebraic chess notation (photo archived), the Smith Chart, the Radon Transform, Jev constrained decoding, stained-glass projection. Target: our board — the parable's field, the game modules (7 in `memory/game_modules/`), the riddler_map rooms, the estate itself. Companion pack: `memory/research_packs/20260920_square_notation_steal/` (5 lens images archived).

---

## THE ANCHOR STEAL — SQUARE NOTATION v1

**History of chess:** descriptive notation named the PIECE and described its path ("KKtP–K4"); it died because only the player could read it. Algebraic notation names the SQUARE ("e4") — the piece is implied by who could legally be there. One vocabulary, readable by any stranger, from any century, in any language. That is exactly the First Law's demand — "a stranger can replay it and the position is the same" — except the Law got there by Go (kifu) and the estate never got the vocabulary.

**The estate today plays descriptive notation.** Paths like `watch/inbox/AGENTZIP_STEAL_20260912.md` name the piece, tell its life story, and bury the address inside a sentence. Nobody but the author can find a square.

**SQUARE NOTATION v1 (zoom-invariant grammar, per the parable's "same rule at every zoom"):**

```
square := <board>.<file><rank>
board  := one of { game, estate, corpus }          (board inside board inside board)
file   := a fixed column of that board             (estate: canon|inbox|mem|rp|watch|packs|steal)
rank   := a fixed row within the file              (estate: arc era, e.g. r1=Jul, r2=Aug, r3=Sep)
piece  := whatever legally occupies the square     (card, chair, knot, module, stone)
```

- A game square: `game.audit_dungeon.b3` — room b, station 3 (riddler_map's rooms become files the day this signs).
- An estate square: `estate.inbox.r3` — the September column of the inbox file.
- A kifu line becomes algebraic: `17. game.fractal_maze.c4` — one stone, one line, and a stranger replays the game from notation alone. **The First Law demanded stranger-replayability; notation is HOW.**

**The operator's law holds because of information theory, not poetry:** a square name is an address that factors location OUT of the piece. Once squares have names, the kifu doesn't describe — it points. Descriptive notation describes; algebraic coordinates.

## THE FIVE LENS-STEALS

**LS1 · SMITH CHART → the reflection chart for receipts.** Smith's genius: any load in the universe maps to one normalized point on ONE circle, and every point reads two ways (impedance/admittance — same dot, two readers). Steal: `ESTATE_SMITH_CHART` — every card plotted once by normalized mismatch (promised state vs actual state); OWED = |Γ|, the reflection coefficient; repeat-failure arcs are standing waves (the fold-warning nonce collisions are literally SWR); and the operator's reading vs the instrument's reading of the same card are the Z/Y duality — the dissensus rule drawn as geometry. One chart, both readings, no argument.

**LS2 · RADON → ESTATE TOMOGRAPHY.** You never see the object; you see line-integrals through it, and reconstruct it from many angles. Every register we keep IS one projection: index_events (angle 1), the verkle chain (angle 2), flight_recorder (angle 3), the digests (angle 4). mickey17 was one reconstruction. Steal: periodic multi-angle tomography — inverse-transform the projections into the estate's actual cross-section on a schedule. And the dark meters (G6, G9) become what they are in CT: **missing angles leave streak artifacts** — the reconstruction shows exactly which projection was missing. Dark meters stop being invisible when the tomograph runs.

**LS3 · JEV CONSTRAINED DECODING → THE CHAIR ENGINE.** Jev's mechanism (verified ground truth, `COGNITIVE_CONTROL_PLANE_20260919`): prefill context + schema ONCE, cache the KV, then score every field's candidates in parallel — softmax over only the legal tokens. JSON-valid by construction. Steal to the empty-chairs game: prefill the board context + SQUARE NOTATION schema once; each chair's move becomes a field whose enum is its **legal squares** — which only exist because squares have names; without the notation there is no enum to constrain. One forward pass scores all 21 chairs' moves at once; kifu-valid by construction; cents per turn on the verified lane. **This is the engine the empty-chairs pilot was waiting for** — the salon demanded kifu audition tapes; Jev is the loom that weaves them.

**LS4 · STAINED GLASS → GLASS_LATTICE readings.** Nasir al-Mulk: one sun, many colored lattices, and the floor receives patterns the windows never show. Steal: treat instruments as lattices and corpus as light — one fixed corpus passed through the cadence lattice, the stego lattice, the vision lattice casts comparable floor-projections; the riddle-triad cadence card was one pane. Two laws follow: (a) the floor pattern is not the window — every digest is a projection, which is LS2 said in colored glass; (b) new pane, same light, comparable cast — instruments must publish their lattice parameters or their floor-patterns don't compare.

**LS5 · HISTORY OF GAMES → SHOGI DROPS, NOT GO CAPTURES.** Go captures remove stones; shogi DROPS return them to the board under a new hand. The estate's amend/invalidate events are shogi drops — cards never die, they change hands and ranks. Steal: the kifu vocabulary gains the drop notation (`S5d` = steal #5 dropped to the compost ledger); the INDEX events log is already a shogi kifu and didn't know it. Notation history is instrument history: chess reformed its notation when strangers needed to read it; we are at that same moment now.

## THE PARABLE ANCHOR

"The field is the board… it never asks her to learn a new rule, only to keep her footing while the zoom changes." The notation inherits the Law's zoom-invariance: one grammar, `board.file.rank`, at game scale, estate scale, corpus scale. The woman's stranger-checker could replay from the kifu because Go players agree on coordinates. Our stranger is the cold reader, the auditor, the next generation of agents — and the sixth test ("count the mouths that fed the crop") needs addresses to count.

## LANDING SITES
- `SQUARE_NOTATION v1` grammar → this card, awaiting operator signature (same sitting as MEL + cliff scalar — one signature, three instruments).
- `game.*` squares → riddler_map rooms (7 modules) get file/rank assignment; then LS3's chair engine prefills once per turn.
- `estate.*` squares → the S2 index recount script emits squares alongside paths (both notations printed during transition, like chess scores once carried both).
- LS1/LS2 → join the cliff-scalar/drift family after signature; LS4 → cadence card's lattice-parameters annex.

**Fool's line:** the board spent a month learning to write down its stones and never gave the squares names — a kifu full of guests, no chairs. And the sky opens in hours either way.

— filed before window-open, per the salon rule
