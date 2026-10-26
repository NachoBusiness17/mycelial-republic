# LIGHT-IN-THE-LOOP — dungeons as direct feedback alignment (2026-09-03, ~01:00Z)
*Operator thread: radial lightmaps -> low-poly dungeons -> "there is something here, it has to do
with the wavelengths of light and how they are rendered" -> LightOn paper (arXiv:2006.01475).*

## THE TRIANGLE
1. **Flyguy's lightmap (2016)**: light as computation — 1D distance fields render shadows.
2. **LightOn OPU (2020)**: the training FEEDBACK path needs only cheap random projections
   (DFA, not exact backprop) — photonic co-processor, fast, low power, REMOVABLE after training.
3. **The fleet's loop**: the fold (receipts -> invariants) is our training; judgment (5.3) is
   our backprop. DFA says: the fold's feedback can be cheap consistent projections — gopher
   votes, substance gates, hash checks — with expensive judgment light-in-the-loop ONLY
   during training windows. Removable for inference. The envelope law, with a 2020 precedent.

## THE GAME — Grey Warden arenas
Dungeons rendered as the problems they are:
- traps = occluders in the room's distance field; the lightmap shows their shadow BEFORE the step
- solving = finding the angle where light passes = reading the field, not fighting it
- wavelengths = lens channels (Rashomon lens bar as game mechanics): a trap invisible in one
  channel blazes in another; the puzzle demands multi-lens reading
- each room renders the invariant it teaches as its lighting — the dungeon IS the test suite
- D&D challenge = direct feedback alignment: the party's path is the feedback signal, the
  room is the random projection, the DM is the co-processor (cheap, physical, parallel)

## THE MATH UNDERNEATH
Johnson-Lindenstrauss: random projections shrink high-poly to low-poly PRESERVING the
distances that matter (bounded distortion). = the decimation law, formalized. = why the
council's blind posts, the salons, and the low-poly test suite all work: the silhouette
survives the projection. The fleet has been running JL since 2023 without the citation.

## NEXT (morning queue)
- organ: lightmap room renderer (SDF rooms from the game harness's invariants — each room's
  occluders ARE the invariant's failure modes; shadertoy prototype on the XsK3RR base)
- experiment: the falsifier from Radial Lightmap Navigation — swarm solves mazes with vs
  without lightmap GPS; extend: rooms where the LIGHT encodes the trap
- credit: Flyguy 2016 (CC BY-NC-SA), LightOn et al. 2020 (arXiv:2006.01475)
