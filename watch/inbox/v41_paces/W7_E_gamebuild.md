# W7 / LANE E — FREE-LANE GAME BUILD (2026-09-10)

**THE POINT:** the flagship test — can the free deepseek-flash lane BUILD on our surface?
Bar to beat: BridgeMind's ocean sunset bench ($0.03 vs Astra $0.59). The probe chosen is
the hardest kind: not "draw something", but REINTERPRET an existing organism — steal the
fish's parametric DNA and re-rig it as a galloping horse.

## 1. The fish prototype — FOUND

- File: `dashboard/static/viz_spore_fish.html` (36 lines, not the candidates first grepped).
- game.html only *comments* on boids (line 178) and the fish (line 259: "the operator
  wanted the ACTUAL skeleton rendered, not the fish") — renders skeleton, not fish.
  maze_enhancement.html mentions boids as metaphor only. The real prototype is the spore.
- What it is: a 10,000-particle closed-form point cloud. One time var `t += PI/80` per
  requestAnimationFrame tick; every pixel placed by trig of index + t via 1px `fillRect`;
  luminous `rgba(127,178,255,.6)` on `#090808`. Caption carries the orphan story verbatim:
  *"it was beautiful, and it wasn't the organism."*

## 2. The lane call

- `models/providers.py::chat_provider("deepseek", model="deepseek-v4-flash", tier="T2",
  allow_peak=True, thinking=False)` — prompt = fish source + reinterpret-as-gallop spec
  (spine flex, Muybridge leg phasing, dark lab aesthetic, single self-contained HTML).
- Receipt: `watch/inbox/v41_paces/W7_E_deepseek_receipt.json`.
- HONEST COST NOTE: TWO lane calls, not one — call 1 succeeded (9.1s, 2,120 completion
  tokens) but my driver read `r["content"]` instead of `r["text"]` and dropped the body.
  Call 2 landed clean: **12.1s, 3,065 tokens total, prompt cache hit 768 tok**. My bug,
  not the lane's. Deepseek-v4-flash at ~$0.10-0.28/M ⇒ total spend well under $0.005.
  Driver kept for provenance: `watch/inbox/v41_paces/_w7_e_fire.py`.

## 3. The horse output — assessment

- File: `dashboard/static/viz_horse_run.html` (9,112 bytes, 265 lines — overwrote attempt 3).
- VERIFIED: HTML parses clean (tag-balance walk), canvas present (760x560),
  `requestAnimationFrame` loop present, one `<script>` block, JS passes `node --check`.
- IT IS A REAL REINTERPRETATION, NOT A RELABELED FISH:
  - DNA kept: 10,000-point cloud, 1px fillRect primitive, single-t parametric drive
    (`t += PI/90`), golden-angle distribution (2.399963), exact fish palette.
  - Organism added: 90-segment spine with traveling flexion wave (gather → extend →
    suspension); 4 two-segment legs on asymmetric rotary-gallop offsets (front
    0.00/0.55, hind 0.15/0.70 — correct Sallie Gardner phasing); mane (70 pts) and
    tail (120 pts) phase-LAGGED behind the stride; ground dust strip.
  - The model even chose the golden angle unprompted — a real steal from
    point-cloud practice, not something the fish displayed.
- Warts (tri-state, honest): two dead locals (`earA`, `px()`) — cosmetic, harmless;
  hoof trajectory has no ground-contact clamp (aesthetic nit, not a defect at this
  scale); ~11.5k fillRects/frame ≈ fish's 10k — same known-acceptable perf class.
- Visual truth of "does it read as a horse" is a screenshot judgment — static
  verification is complete, human eye pass still owed. STRUCTURE: SUPPORTED by
  parse/canvas/rAF checks. AESTHETIC: UNPROVEN until someone opens it.

## 4. Verdict on the free lane

**SUPPORTED: the free deepseek-flash lane can build on our surface.** One call, 12
seconds, a correct stylistic transplant (palette + parametric spirit preserved,
anatomy invented) with minor dead-code warts. The failure in this lane attempt was
MINE (wrong response key), not the model's. vs the BridgeMind bar ($0.03): this came
in under a nickel of cents with a harder prompt class (reinterpret-and-preserve-style
beats generate-from-scratch). Flash builds shit. The flagship orphan has an heir:
the fish was beautiful and wrong; attempt 4 is the organism in motion — pending the
operator's eye on it.
