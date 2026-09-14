# INTAKE CARD — OPERATOR FIELD B1 (item 8, 2026-09-03) — THE GO, WITH SPECS

## ITEM
Operator pasted two Shadertoy links (sf23W1, sfGXDK — **unreceipted: Cloudflare
403 + reader network error; tri-state Unproven**) + four images that compose the
B1 design brief:
1. **Marble Madness** (NES) — the genre ancestor: a marble with MOMENTUM rolling
   on an elevated field. Our gradient-walkers step; the marble ROLLS.
2. **Möbius strip** — one-sided surface, parametric rep → a topology PACK for the
   game mechanics lattice (walker returns flipped); docket, not build.
3. **The four vector operators** (∇ · ∇· · ∇× · ∇²) — the FIELD's grammar upgrade:
   lights become OPERATOR CELLS.
4. **Philbrick 1964 op-amp sheet** — already exhibit-004, already the verb-genome
   ancestor; now OPERATIONAL: every light is an op-amp cell, the shader is the
   adder, the player's arrow-key tilt is a bias voltage on the whole sheet
   ("modelling, measuring, manipulating & much else" — the 1964 subject line IS
   the field's job description).

## SCORE — F:5 P:5 C:5 W:5 N:4 = 24/25 → **BUILD NOW — BUILT (v0 on disk)**

## THE BUILD (this turn, live)
`dashboard/static/arena_operator_field.html` — B1a, one static file, zero fetches
(STATIC RENDER LAW holds):
- Same invariant space as maze_arena.html (identical SDF walls + cheese) — a
  sibling, never a clobber of the live arena.
- **GPU field (raw WebGL1, ~zero deps)**: fragment shader mirrors the CPU field
  exactly — tilt plane + Gaussian cells (cheese pit, source hill) + curl ring;
  walls via SDF in-shader.
- **The marble**: momentum + full operator force (∇ descent + ∇× tangential
  swirl), SDF bounce with normal reflection, specular-highlight sphere (the
  Marble Madness nod). Racers: MARBLE (momentum) vs STEPPER (field descent) vs
  DUMB (bounce) — the stacked-arena falsifier continues: does momentum+operators
  beat step-descent beat bounce?
- **∇× = the tornado**: the vortex cell renders as a raised ring; marbles caught
  in it orbit — XsK3RR's ancestral mechanic, now a FIELD.json cell.
- **DIVERGENCE RECEIPT (live)**: 12 fixed sample points, every frame the GPU
  pixel is read back and compared to the CPU's math — max Δ displayed on the
  page, PASS < 0.02. The full-chord law as pixels: the GPU field is not allowed
  to be a costume.
- **Tilt**: arrow keys/WASD bias the entire field — playable (play =
  verification), and the operator's hand enters exactly as a Philbrick variable
  voltage source.

## DOGFOOD RECEIPTS
1. **INVARIANT PASS**: Britney content-borne steering now writes the framebuffer
   itself; the divergence receipt is full-chord (assert the leg or say partial);
   Philbrick re-hung as working code — repetition as emphasis, the good kind.
2. **STOCKFISH PASS**: opcode = BUILD, shadow-fields B1a, this seat's lane; no
   campaign dependency (driver untouched).
3. **ROOM TEST**: the arena now has an op-amp sheet for a soul; Möbius filed as a
   topology pack (room = invariant × engine × pack).

## FALSIFIER (pre-registered, unchanged from card 7)
GPU-vs-CPU Δ < ε live on page · marbles reach cheese · GLSL compiles clean
(console is the judge — **v0 is syntax-gated (node --check PASS) but
UNVERIFIED-IN-BROWSER; the operator's door is the verification surface**:
open dashboard/static/arena_operator_field.html or
http://127.0.0.1:8765/static/arena_operator_field.html). Fail → demote, fix, retry.

## TRI-STATE
- Composition + build-on-disk: **Supported** (file receipts, syntax gate).
- The two Shadertoy shaders' content: **Unproven** (walled) — paste source and
  the bones get stolen; otherwise our GLSL is ours (license law satisfied).
- "Momentum+operators beats step-walkers": **Unproven** until the race runs on
  his screen.
