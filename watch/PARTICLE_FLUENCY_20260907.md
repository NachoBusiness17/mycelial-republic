# PARTICLE FLUENCY — the Houdini program (2026-09-07, operator commission)

Operator: "It's time we become an expert in houdini and we need to map everything we can
about it to 3js and our own tools for dogfood — we are soon going to be speaking particle
simulation fluently. We need to start treating our mazes like the mapping of physical
computing. This is why I fed you all this hardware information and physics."
+ "Remember the state change from liquid to gas to plasma — self steal."

## 1. THE SELF-STEAL (the doctrine was already in the walls)

compuiter.txt (the dissector's own corpus — watch/inbox/desktop_bundle_20260901/):
- L93: "The new contract: **use a system's natural relaxation, interference, flow, or
  phase transition as the solver**; accept noise and nonlinearity; wrap AI around it."
- L139/L187: physical computing stack = "natural collective dynamics — relaxation,
  resonance, interference, **phase transitions**, flow."
- L37: "reservoir computing with water tank... **Liquid state machines**."
- L1386/L1583: coherent Ising machine — "**phase states represent spin up/down**."

So the ladder is already ours, stated as computing-substrate doctrine:
**LIQUID** (water integrator, liquid state machine — the reservoir computes by its flow)
→ **GAS** (expansion/diffusion as search; pyro fields) → **PLASMA** (ionized, collective,
charge-dominated — the Ising machine's optical phase states are plasma-adjacent computing).
Our mazes become MEDIA: the walker is a particle, the medium has a phase, the phase is a
computing mode, and energy input is the control. **A maze in the liquid phase computes by
flow; in gas, by diffusion; in plasma, by collective charge.** That is physical computing
mapped onto game surfaces — the hardware/physics feed was the syllabus for this.

## 2. THE EXPERT MAP — Houdini concepts → three.js + our tools

The fluency program = knowing Houdini's organ names and mapping each to something we can
RUN. Every row must carry a working cite (our repo or a doc'd three.js addon) — no vibes
rows (F-PF2).

| Houdini organ | What it really is | Our mapping | Cite |
|---|---|---|---|
| SOP (Surface Operators) | procedural geometry DAG, cook-on-demand | BufferGeometry pipelines + our procedural builders | calabi_yau.html, viz_3d_verkle.html |
| VEX | per-point SIMD language over attributes | **GLSL** — same mental model: attributes in, position/color out, run everywhere at once | every ShaderMaterial we ship |
| POP (Particle Operators) | attribute-driven particle sim | FBO ping-pong (GPUComputationRenderer): position+velocity textures | dashboard/static/phase_particles.html (R1, this card) |
| DOP pyro (gas) | velocity-field advection + dissipation | curl-noise advection in the velocity shader | phase_particles.html GAS phase |
| FLIP/Vellum (liquid) | position-based fluids, constraint projection | PBF/Verlet constraint passes in FBO (Verlet integration — yes, the pun is load-bearing: verkle keeps history, verlet keeps physics) | R2 door |
| CHOP (channels) | signal/channel graph over time | telemetry streams + our meters (overseer.json) | mag/overseer.py |
| PDG/TOPs (task graphs) | dependency-graph batch pipeline | **salon_runner / queue / batch lanes — already built, same shape** | mag/salon_runner.py |
| Cook chain / dirty propagation | recompute only what changed, radiating from the edit | **tesuji dirty-radius invalidation — the self-steal hit: Houdini's cook model IS our field invalidation doctrine** | arc_seed.py, tesuji map ("field beats bounce") |
| Attributes (@P @v @Cd @pscale) | data on points, carried through the graph | BufferAttributes / data textures | all WebGL surfaces |
| Wrangle node | attribute snippet injector | onBeforeCompile injections / full ShaderMaterial | existing pages |
| Solaris/USD | scene composition layering | three.js scene graph + glTF | mesh_gallery.html |
| State change (the operator's law) | energy in → phase out: liquid → gas → plasma | energy slider → MEASURED phase diagnosis (mean speed + spread), never labeled from the slider | phase_particles.html instrument |

## 3. DOGFOOD LADDER

- **R1 — phase_particles.html (BUILT + VERIFIED same turn):** GPGPU curl-noise particles,
  65k (256²), FBO ping-pong via GPUComputationRenderer; energy slider; phase DIAGNOSED
  from observables (mean speed + spread, read back through a float RT) against
  pre-registered thresholds. **F-PF1 PASS — measured ladder:** e=0.2/1.0 → SOLID
  (v̄ 0.00/0.36, spread 0.89 = the lattice itself), e=1.5/2.0 → LIQUID (2.93/2.99),
  e=2.5/2.9 → GAS (5.36/4.04), e=3.3 → PLASMA (13.62; walls pinned white-hot, vortex
  filaments, frame receipted memory/runs/video_smoke/phase_particles_plasma.png).
  Visual: additive points, phase palette teal→amber→violet.

  **Debugging lessons = mapping-table rows in disguise (the real Houdini→GLSL fluency
  receipts):**
  1. Float textures + LinearFilter = black samples unless OES_texture_float_linear —
     Nearest sampling is core WebGL2. (Houdini analog: never let a plugin silently
     resample your attributes.)
  2. **GPUComputationRenderer dependencies are DECLARED (setVariableDependencies),
     never parsed from shader text** — undeclared = samplers unbound = compute passes
     silently render nothing. The sim looked fine (init copy correct) while producing
     zeros. (Houdini analog: an unwired node input doesn't error, it cooks empty.)
  3. texture2D wants NORMALIZED uv, not raw texel coords — one dot = 65k particles
     stacked on one texel. (Houdini analog: attribute vs index space confusion.)
  4. Phase bands must be calibrated to the MEASURED dynamics, not the other way —
     the first tuning had "liquid" running at plasma speeds; the instrument caught it.
- **R2 — liquid proper:** Verlet/PBF constraint pass in FBO — pouring, pooling, sloshing
  in a container; the maze walls become the container.
- **R3 — the maze becomes the medium:** shadow_walk or a new maze gains a phase state —
  same corridors, three computing modes (flow-solve / diffusion-solve / collective-solve).
  The maze-as-physical-computer test (F-PF4).
- **R4 — procedural geometry:** SOP-style build of a maze from attributes (corridors as
  swept curves), VEX→GLSL port of one Houdini tutorial verbatim (F-PF3 fluency test).
- **R5 — PDG dogfood:** one salon/batch pipeline re-expressed as a PDG-style node graph
  UI over our own queue (the map says it's the same shape — prove it visually).

## 4. FALSIFIERS

- **F-PF1:** phase diagnosis from MEASURED observables changes state exactly when the
  energy crosses pre-registered thresholds — and the room shows a real transition, not a
  relabel (speed distribution + spread both move).
- **F-PF2:** every mapping-table row carries a running cite in our repo or a doc'd addon;
  a row without a cite gets demoted to "door".
- **F-PF3 (fluency):** one Houdini tutorial's node graph re-expressed in our tools
  produces equivalent output. If we can't port one tutorial, we're not fluent.
- **F-PF4 (physical computing):** a maze run in different MEDIUM PHASES yields different
  solutions to the same corridor — the maze computed, not just displayed.

## 5. LINKS (8, triaged)

Hardware/physics corroborations: @essen463404 open-source FPGA fabric (FABulous/gf180mcu,
open silicon — physical computing at the bottom); @NathanFlurry WASM/isolates agent
sandboxes (agent density per CPU — the fleet's next substrate question); @analogalok
local TTS 1.6× realtime on CPU (ractor voices); @VaderResearch 4 open robotic arms
(embodied lane); @DeryaTR_ Astra+AlphaFold fusion protein in 9 min (renaissance shelf);
@Thechemicalhub 99 chemical processes (phase diagrams — the chemical-engineering view of
the state-change ladder); @0xAsm0d3us + @KirkDBorne noise.


## R3-PREVIEW LANDED SAME NIGHT: LIGHT MAZE (dashboard/static/light_maze.html)

The operator posted the mood board (our three rooms + a ray-traced light maze reference)
saying "this is the light maze i want to build :D" — so it was built before dessert.
Ray-cast visibility polygon (rays to every wall corner), glyphs lit only inside the
light, exit opens at full collection, and THE SHERPA ORGAN IN-GAME: press H and a wall
becomes a hand — a light pulse pointing to the nearest unlit glyph. First light
receipted (memory/runs/video_smoke/light_maze_first_light.png): two glyphs gold, the
rest dust, hard shadows. The update-loop bug (draw scheduled, update forgotten) caught
by the same-night dogfood instinct. Spectral splitting (B7 red/blue demux) = v1.
