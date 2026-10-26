# INTAKE — UNO_DIFFUSION (2026-09-04)

**NAME** — Uno: diffusion-augmented LLMs — parallel multi-token draw from the model's OWN AR distribution (no draft model, no quality trade).
**SOURCE** — dair_ai tweet 2096010455210959202 (2026-09-04 23:00Z, 5.5K views, 51 likes, 4 replies/1 quote unmined — time-box). Paper receipted: arXiv:2609.04010 "Unlocking Lossless Speedups in LLMs via Discrete Diffusion" (Sahoo et al., 2026-09-03). Abstract matches tweet faithfully.
**CLAIMS** — AR weights train NTP as usual; lightweight diffusion weights added via short Diffusion Distillation (negligible pipeline overhead). Psi-Spec samplers draw multiple tokens in parallel from the same AR distribution => lossless. Existing open-weight AR models upgradeable without retraining. Benchmarks: up to 3x over base, beats speculative decoding at all batch sizes; 8B Uno > 26B DiffusionGemma and proprietary Mercury 2 (tool use / coding / long-context).

**SCORE** — F:4 P:4 C:3 W:3 N:4 = **19/25 BUILD, WINDOWED**
- FIT 4: claim-dense = direct food for falsifier workbench + GA gene pool (genes with falsifier runs get promoted). "Lossless" is measurable (held-out perplexity/KL vs base AR); "3x" is measurable (tok/s). Composes with accumulator (throughput accrual) and agent-organs (agentic evals cited).
- PULL 4: Rocinante critical path — lossless 3x decode on open-weight models is a direct multiplier for the Oct 27 local substrate; one distillation phase upgrades whatever model we run.
- COST 3: digest free-lane; falsifier/repro needs local compute + released weights/code — unfunded until then.
- WINDOW 3: workbench + gene pool live now, but any run gates on weights/code release and local hardware.
- NOVELTY 4: new surface (diffusion-augmented decoding vs draft-model speculative decoding); distinct from today's Terminal-Universe paste; no shelf hit in time-boxed sweep (partial).

**VERDICT** — BUILD, WINDOWED. Lane: falsifier-workbench / GA gene pool — register "lossless (same AR distribution)" as a falsifiable gene the moment weights/code drop; gate: implementation release + Rocinante-class hardware. Per Amendment 5 this is not a deferral: windowed names the lane, driver launches when the gate opens.
**TRI-STATE** — Mechanism (no draft model, lossless-by-construction, distillation overhead negligible): **Supported** (abstract receipt). Benchmarks (3x, beats Mercury 2 / DiffusionGemma): **Unproven** (paper claims only, no independent run; 4 replies unmined — thread-mining pending per Amendment 2).

**DOGFOOD** — Test 1 (invariants): reinforces falsifiability law (claims are measurable by construction — that's why it scores); no contradiction found in time-box. Test 4 (Stockfish): sits on the tool lattice as an INFERENCE-OPTIMIZER opcode feeding the local-substrate leg; placement succeeded.

**FILED** — watch/INTAKE_UNO_DIFFUSION_20260904.md + room.jsonl thread "intake". Second dair_ai paste today (first: Terminal-Universe 20/25) — pattern signal: dair_ai feed is hot, consider a standing monitor term.
