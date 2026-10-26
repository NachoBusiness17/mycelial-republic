# C18 — HYDRAULIC THIRD CHANNEL (two-bucket XOR physical artifact)

Lane: physical_computing · gen-2 (gen-1 died to rate limit, no output) · Mickey17
Date: 2026-09-16
Falsifier target: pack §4.5 — the Hermes circularity attack ("the sim is its own spec"). Breaking move: a physical artifact whose behavior the MUD sim must predict in advance, pre-registered, then measured.

## Status
- [x] Receipt created first (wave-lane law)
- [ ] (1) Read `memory/game_modules/water_computer.v1.json` — "The Clear Pipes" MUD keep
- [ ] (2) Write sim PREDICTION as numbered falsifiable statements (fluid levels, timing, failure modes)
- [ ] (3) ~$15 physical build spec (two containers + tubing + valves, water level = bit), MONIAC/Lukyanov + fluidics lineage, street-price BOM, build time
- [ ] (4) Comparison protocol: which physical measurements vs which sim outputs, pre-registered tolerance
- [ ] (5) Meaning for falsifier §4.5 (sim stones count as substrate evidence only after this passes)
- [ ] Receipt ends with BOM total + numbered prediction list verbatim

## Findings (appended as gathered)

### (1) What the sim already encodes — `memory/game_modules/water_computer.v1.json` ("The Clear Pipes")

- Schema `mag_game_module.v1`, aliases include `moniac`, `lukyanov` — lineage declared in-module; `license_note`: "Lukyanov/MONIAC isomorphism, not a replica. **Engine owns heights.**"
- Tank chain: SOURCE (3 marks, "the only full tank at dawn") → Valve-A → WORK ("Work Integrator") → Valve-B → OUT ("Output Cistern"). Gravity is the only computer; "height is the computation."
- **Unit of compute:** discrete. "Closed, nothing flows. Open, gravity takes a **mark each wait**" — one mark per tick. Pump-Janitor: "I move water. I do not pour. Hire me and I **tick once**." Time is ticks, quantity is marks.
- **Check valve doctrine:** "Check valve holds. I will not fill OUT from a bucket" — one-way flow, no backflow, no bypass.
- **Scripted failure mode (the gift):** Valve-B hook — "Open only after water has arrived, **or both valves siphon**." The sim already asserts that simultaneous/open-out-of-order valves produce siphon-drain behavior. This is the sim's one *quantitative-adjacent* hydraulic claim, and it becomes the physical gate's XOR mechanism (see P8).
- **Anti-cheat:** OUT contains a bucket; "pour bucket to fake a height. That is not computation." Physics calls it DISPUTED. The physical build inherits this: output must arrive through pipes; reading the bit must be a sight-glass level, never a pour.
- What the sim does NOT encode: numbers. Marks per wait is qualitative. The prediction below extends the sim's own rules to quantities — that extension is the falsifiable content.

### (3a) Prior-art / lineage (literature)

- **Lukyanov Water Integrator (USSR, 1936):** water height = variable value; solved PDEs for permafrost/concrete temperature; in use into the 1980s. [Wikipedia — Water integrator](https://en.wikipedia.org/wiki/Water_integrator) · [Amusing Planet — Lukyanov's water computer](https://www.amusingplanet.com/2019/12/vladimir-lukyanovs-water-computer.html)
- **MONIAC / Phillips Machine (LSE, 1949):** transparent tanks, valves, gravity flow modeling an economy; "uses fluidic logic." [Wikipedia — Phillips Machine](https://en.wikipedia.org/wiki/Phillips_Machine) · [Science Museum](https://www.sciencemuseum.org.uk/objects-and-stories/how-does-economy-work)
- **Fluidic logic:** Coanda-effect wall-attachment amplifiers (1960s industrial fluidics; e.g. Honeywell fluidic controls, Soviet Soyuz pneumatic systems); XOR arises from opposing control jets canceling. Microfluidic digital logic: Prakash & Gershenfeld, "Microfluidic Bubble Logic," Science 2007 (Stanford Prakash lab). Fluid-diode (check-valve) logic builds OR/AND; XOR from combinations. WebSearch rate-limited mid-query (429, code 1302) — same hazard that killed lane gen-1; lineage above verified, Coanda/bubble-logic claims are from the search tool's own fallback summary and flagged as lower-confidence citations.
- **Threshold element:** self-priming siphon (Pythagorean-cup principle) as a binary hydraulic threshold device — crest primes at a fixed height, then dumps to waste regardless of continued inflow; intake near the bottom drains to ~empty, then breaks. [Wikipedia — Pythagorean cup](https://en.wikipedia.org/wiki/Pythagorean_cup) · [incoherency.co.uk build note](https://incoherency.co.uk/blog/stories/pythagorean-cup.html) · [Steve Mould, "The Greedy Cup Has Become Even More Devious"](https://www.youtube.com/watch?v=Gav25xB0LtE) (same auto-drain siphon lives in washing-machine softener dispensers). Household precedent for a siphon as a *reliable binary threshold device*, which is the load-bearing component choice.

### (3b) The physical gate — "BOTH VALVES SIPHON" (pulsed two-bucket XOR)

**Design rationale:** steady-state flow-balance XORs are fragile (orifice flow ∝ √h; drift kills them). This design puts the discrimination in a **threshold instability** (siphon prime / no-prime), which is binary and robust, and keeps time discrete (one 60 s tick), faithful to the sim's "a mark each wait." XOR = (A OR B) AND NOT(A AND B), where the siphon is the NOT(A AND B).

**Parts (2 buckets, 4 lines):**
- **Bucket S (SOURCE):** clear tub, filled ≥ 300 mL (3 marks), marked at 100 mL intervals. Supply only.
- **Bucket W (WORK):** clear tub, sight-glass marks at 100 mL intervals (1 mark = 100 mL). Bit read = W level. Fitted with:
  - **Crest siphon:** 6 mm ID vinyl tube bent over a 150 mL-crest (1.5 marks), intake 5 mm above W floor with a small V-notch break, outlet → waste catch (graduated cup).
  - Two **input lines** entering at the TOP of W, each terminating above the max water line (gravity break): S → hand valve (barbed shut-off) → check valve → calibrated ~1.4 mm orifice (drilled in a grommet) → free fall into W. Each line delivers ~1 mark per 60 s tick at working head.
  - **Bottom drain plug** (sealed with silicone) for reset between trials.
- Timer (phone). Valve labels A and B.

**Operation (one trial):** fill S ≥ 300 mL, W empty, plug in. Open the enabled valve(s) **simultaneously for exactly T = 60 s** (one Pump-Janitor tick), close. Read W at **t_read = T + 90 s**. Inputs are pulsed; nothing pours; output arrives only through pipes (the DISPUTED rule).

**Physics of the truth table:**
- (0,0): nothing flows → W ≈ 0 → read **0**.
- (1,0) / (0,1): one mark delivered → W ≈ 100 mL < 150 mL crest → siphon never primes → read **1**.
- (1,1): two marks/60 s = 3.3 mL/s in vs. siphon 20+ mL/s out once primed → level crosses 150 mL at ~45 s, siphon primes ("**both valves siphon**" — the module's own hook, made mechanism), dumps to ~0 → read **0**.

**Build time:** ~2–2.5 h total (assembly 30 min + calibration gate 45 min + trial battery ~45 min + contingency 30 min).

### (3c) BOM (street prices, US hardware/aquarium/Walmart, 2026)

| Item | Street price |
|---|---|
| 2 × clear storage tubs with lids, 6 qt (Sterilite; or free 2 L soda bottles) | $5.94 |
| Vinyl tubing 3/16" ID × 6 ft | $2.50 |
| 2 × 1/4" barbed plastic shut-off valves (aquarium) | $2.40 |
| 2 × 1/4" aquarium check valves | $2.20 |
| Silicone sealant — or hot glue if owned | $0.00 |
| 1.4 mm drill bit / heated pin (tool owned) | $0.00 |
| 2 × binder clips (flow trim) — owned | $0.00 |
| Graduated kitchen cup (waste catch + measure) — owned | $0.00 |

**BOM TOTAL: $13.04** (~$13–15; inside the ~$15 envelope; $18 worst-case boutique pricing)

### (4) Comparison protocol — pre-registered

**Calibration gate (build-quality gate, runs before any scored trial, not itself pass/fail):** each input line alone, 3 × 60 s ticks from S ≥ 300 mL → each delivers 100 ± 15 mL, and the two lines match within 10 mL. Trim with binder clip on the tubing; re-drill if out.

**Physical measurements (M):**
- **M1** — per-line delivery per 60 s tick (mL), both lines, 3 trials each → tests P1.
- **M2** — W level at t_read, four input cases × 3 randomized-order trials → tests P2–P4, the XOR truth table.
- **M3** — siphon prime event (gurgle/crossing 150 mL): yes/no and time-from-valve-open, case 11 → tests P3.
- **M4** — post-prime W drain slope (mL/s), case 11 → tests P8.
- **M5** — envelope: max level ever seen in single-input trials; min crest-crossing level in double-input trials → tests P5.
- **M6** — S volume monotonic decrease + mass balance (S + W + waste catch = initial − 10 mL) per trial → tests P6.
- **M7** — repeat of one (1,0), one (0,1), one (1,1) trial with valves opened 5 s apart → tests P7.

**Read bands (fixed before any trial):** bit **1** = W ∈ [70, 130] mL at t_read; bit **0** = W ∈ [0, 30] mL; W ∈ 31–69 = FAIL (under-delivery / partial dump); W ∈ 131–169 = FAIL (siphon primed but did not break); W ≥ 170 = FAIL (siphon never primed). FAILs score as trial failures, not rebuilds, and map to the specific violated P-statement.

**Sim-output ↔ physical-measurement mapping:**

| Sim rule (water_computer.v1.json) | Physical measurement | Prediction |
|---|---|---|
| "gravity takes a mark each wait" | M1 | P1 |
| WORK height after one tick (the state) | M2 | P2–P4 (truth table) |
| "or both valves siphon" | M3, M4 | P3, P8 |
| "Check valve holds" | M6 | P6 |
| Implicit determinism ("Engine owns heights") | M5, M7 | P5, P7 |

**Scoring:** gate PASS = XOR truth table correct under the bands (00→0, 01→1, 10→1, 11→0) AND P1, P5, P6, P7, P8 each individually hold. Any violated statement = that hydraulic claim is falsified; log which one.

### (5) Meaning for falsifier §4.5 — the Hermes circularity attack

The attack: "the sim is its own spec — it predicts only what it was written to encode; sim stones are narrative, not substrate evidence." This artifact is the **third channel** that breaks the circle:

1. The sim's hydraulic rules were fixed **before** the build (the module file predates this receipt); the numbered predictions below are **pre-registered here, before any water runs**.
2. If the physical buckets obey P1–P8, then the sim's rules constrained expectations about matter, and matter complied — a non-sim consequence. The sim encoded *causal structure* (mark/tick transfer, one-way valves, threshold dump), not just text that mirrors itself. That is substrate evidence.
3. If any P-statement fails, the sim's hydraulic claims are model-only; §4.5 stays **closed**; sim stones remain narrative until a corrected prediction passes.
4. On PASS: sim stones of `water_computer.v1` may be cited as substrate evidence, **scope-limited to the hydraulic claims P1–P8** — no generalization to other modules without their own third channel.
5. The DISPUTED rule is the epistemics of the whole move: pouring water into W to fake a 1 *is* the circularity attack in physical form. The protocol forbids it structurally — output arrives only through pipes, and M6 mass-balance closes the system so a pour would show up as missing water in the waste catch.

**Verdict procedure:** run the calibration gate, then the 15-trial battery (4 cases × 3 = 12 scored + 3 skew trials), file M1–M7 with raw numbers in a follow-up receipt. "Trust bytes, not reports": photo of sight-glass at t_read per trial, waste-cup readings logged.

---

## APPENDIX A — BOM TOTAL

**BOM TOTAL: $13.04** (2 tubs $5.94 + tubing $2.50 + 2 shut-off valves $2.40 + 2 check valves $2.20; sealant/drill/clips/measure owned at $0). ~$13–15 street, inside the ~$15 envelope. Build time 2–2.5 h.

## APPENDIX B — NUMBERED PREDICTION LIST (verbatim, pre-registered 2026-09-16, before any physical trial)

- **P1 (unit transfer).** With SOURCE at ≥ 300 mL and exactly one input line open for one 60 s tick, W gains 100 ± 20 mL. (Post-calibration; the calibration gate requires 100 ± 15 mL per line, 3 consecutive ticks, lines matched within 10 mL.)
- **P2 (single input = bit 1).** For inputs (A=1,B=0) and (A=0,B=1), W level at t_read = T + 90 s lies in [70, 130] mL in ≥ 2 of 3 trials per case, and the siphon never primes in those trials (level never reaches 150 mL; no gurgle).
- **P3 (double input = bit 0).** For (A=1,B=1), the siphon primes (level crosses 150 mL) within 90 s of valve opening, and W level at t_read is ≤ 30 mL, in ≥ 2 of 3 trials.
- **P4 (zero input = bit 0).** For (A=0,B=0), W level at t_read is ≤ 30 mL in 3 of 3 trials (drain plug sealed; only residual/splash water present).
- **P5 (threshold margin).** The maximum level recorded in any single-input trial is ≤ 130 mL, and the minimum crest-crossing level observed in any double-input trial is ≥ 140 mL (≥ 10 mL separation between the single-input envelope and the dump threshold).
- **P6 (check valve holds / conservation).** During any tick, SOURCE volume only decreases; water never flows back from W into S; and S + W + waste-catch volumes reconcile to the initial fill within 10 mL per trial.
- **P7 (timing skew immunity).** A ±5 s offset between the two valve openings does not change any case's read-band outcome (P2–P4 results hold in the skew trials).
- **P8 (the sim's scripted fault, quantified).** In case (1,1), after priming, W drains at ≥ 3 mL/s (a 2-mark contents dumped in ≤ 60 s) — the physical realization of the module's Valve-B hook: "Open only after water has arrived, or both valves siphon."

**Predicted failure modes (named, detectable):** F1 over-delivery prime (single line > 150 mL/tick → XOR degrades to AND; shows as P2 fail with gurgle in single-input trials). F2 crest miss (both lines < 75 mL → 11 never primes, reads 1; shows as P3 fail, W ∈ 131–169). F3 siphon never breaks (re-wet/dribble → residual > 30 mL; shows as P3/P4 residual fails; mitigated by intake V-notch). F4 backflow past check valves (mitigated by top-entry inlets above waterline; shows as P6 fail). F5 splash/capillary losses ±5 mL (inside P1/P6 tolerances). F6 operator timing skew beyond ±5 s (bounded by P7 trials). F7 orifice clog/drift (re-run calibration gate if trial day ≠ build day).

— C18 out. Receipt ends here: BOM total $13.04; prediction list in Appendix B verbatim.
