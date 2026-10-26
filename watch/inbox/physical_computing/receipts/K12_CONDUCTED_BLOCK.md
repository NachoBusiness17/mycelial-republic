# K12 — THE CONDUCTED BLOCK (synthesis draft)

**Lane:** K12 (synthesis desk) · **Date:** 2026-09-16 · **Status:** OPEN — appending as lanes land
**Scope:** Full spec v0.1 for a 3D-printed spent-oats block with embedded Cu/Ag lattice traces (electrode grid + guard + steering fields), capillary channels, zoned nutrient doping, inoculated as a living computer substrate with electrical readout.
**Discipline:** DESIGN DRAFT. Every number not anchored to a sibling receipt or a cited source is marked **[UNVERIFIED]**. No git, no paid APIs. Receipt-first, append-as-you-go.

---

## 0. Synthesis inputs (receipt ledger)

| Receipt | Status | What K12 takes from it |
|---|---|---|
| G-C_ZONE_TOPOLOGY.md | LANDED 18:07 | zone geometry, channel topology |
| G-J_INSTRUMENT_TIER.md | LANDED 17:42 | instrument/readout tier, mux |
| C18_HYDRAULIC_THIRD_CHANNEL.md | LANDED 14:01 | hydraulic third channel, passive moisture |
| CUBE1_SHOPPING_LIST.md | LANDED 15:45 | cube-1 reuse, $34–66 baseline |
| K2 / K5 / K7 | **NOT LANDED** (absent from receipts/ at draft open 18:45-ish) | open cells below |
| G-D, G-E, G-F, G-G, G-H, G-I, G-B, GA | landed G-lanes (will mine opportunistically) | write mechanisms, fab, signal magnitude |

**Tag legend:** [V] = byte-verified this session (sibling receipt bytes or live fetch) · [F] = flagged folklore/canon-consistent, not byte-verified · [U] = UNVERIFIED design guess, needs K-lane or bench answer.

---

## 1. The artifact in one paragraph

THE CONDUCTED BLOCK = a printed spent-oats cube (~150×150×60 mm internal [U]) built in four strata: a wet base reservoir, an embedded Cu/Ag lattice plane (16-node sensing grid + perimeter guard + 2 steering bars), a ~30 mm living substrate plane (zoned nutrient doping, zoned inoculation, seeded two-species zone line through the instrumented corridor), and a lid sensor grid (4×4 top electrodes + camera window + SHT31). The block is inoculated, grown for 1–3 weeks, then read electrically through the lattice (cube-1 ear, muxed) and optically (G-C camera pipeline), and *written to* by bipolar-pulse steering fields — the block is simultaneously substrate, wiring, sensor, and (the claim under test) a steerable living computer. It is DESIGN_MULTISPECIES_LATTICE's cube-2 given a fab drawing, with C18's hydraulic doctrine at the base and G-J's ear on top.

**Fabrication order (v0.1):** print-then-inoculate (the lower-risk variant G-I verified exists) — print the paste body in a mold or with a paste head, place the lattice net mid-print at the carrier plane, cure/set, then zone-inoculate by syringe. Living-from-print (spawn mixed into paste) is the v2 variant. [V: both process orders exist, G-I]

## 2. Dimensions & layer structure

Overall: **150 × 150 × 60 mm internal**, 10 mm printed paste walls, sitting in the cube-1 foil-lined 6 qt tub (≈40×28×25 cm [F — Sterilite 6 qt class]) with ≥2 cm air margin on all sides. [U — ergonomics guess; sized to: 4×4 grid at 2 cm pitch = 6×6 cm corridor + perimeter buffer + guard + wall]

| Layer | z-range | Thickness | Content |
|---|---|---|---|
| **L0 base reservoir** | 0–10 mm | 10 mm | Water/salt reservoir flooded from a fill port; sight-glass level marks on the wall at 5 mL intervals (C18 anti-cheat doctrine verbatim: level is read, never poured [V]); 8 wicking columns (Ø8 mm paste columns, capped with unbleached cotton cord) rise from L0 through the lattice carrier into L2 — passive capillary moisture, zero pumps. Overflow notch at 10 mm. |
| **L1 lattice plane (carrier)** | 10–14 mm | 4 mm | The Cu/Ag trace net (§3) laid into the paste at print mid-height on a PVA release sheet; Ag/AgCl node tips protrude 2–3 mm up into L2; trace tails exit through the wall at z=12 mm via a sealed grommet bus to the mux harness. Guard ring in-plane. |
| **L2 substrate plane** | 14–44 mm | 30 mm | Spent-oats paste (Mycofluid-class recipe transferred: ~55 wt% spent oats / ~14 wt% brown rice flour / ~1 wt% xanthan / water to ~55% moisture, 8-mL-syringe stand test as print gate [V G-I; exact oats recipe U — one bench iteration owed, G-I's own caveat]); 4 doping quadrants (§5); spawn injected post-print at registered coordinates. |
| **L3 lid sensor grid** | 44–60 mm | 16 mm | Printed lid carrying: 4×4 chloridized-Ag/ECG-pad grid on the underside (2 cm pitch, same x-y registry as L1 nodes — gives vertical differential pairs L1↔L3), polyfill+micropore gas vent, SHT31 temp/RH (concert amendment: stage-1 required [V]), ESP32-CAM window over the corridor with fixed focus/distance and diffused constant LED (G-C rig [V]). |

Timescale anchor: day 5 loose growth, day 10 full colonization for the paste class [V G-I, Mycofluid]; zone-line formation over days 7–21 [F]; read windows are weeks, per C17 stage ladder.

## 3. The lattice drawing

**Material strategy:** Cu = routing + guard + steering bars (cheap, high conductivity); Ag/AgCl = every substrate-contact sensing tip (cube-1 chemistry law — Cu in the wet reading path is a metal-salt confound [V: CUBE1/FEMS warning]). Conductive junctions (Cu-to-Ag, Cu-to-tail wire) made with silver-loaded paint/epoxy. [U — junction recipe]

- **Trace width:** 2 mm Cu foil (0.05 mm stock). End-to-end resistance of the longest trace (~80 mm): ≈ 0.07 Ω [U — arithmetic from ρ_Cu=1.68×10⁻⁸ Ω·m; negligible vs electrode impedance, so no trace-heating or IR-drop issue at our currents]. Matches FPC's 2 mm electrode precedent [V G-C].
- **Grid:** 4×4 sensing nodes, **20 mm pitch** (6×6 cm instrumented corridor centered in the block). **Deviation flagged:** G-C's law is pitch ≤ daily front advance (~1 cm/day) to keep the active pair within ~5 mm of the front; at 2 cm pitch the active-pair error grows to ~10 mm and re-selection must run *daily* to stay valid. Chosen 2 cm anyway to free mux budget; **open cell OC-1** — G-C lane owns the arbitration.
- **Guard ring:** single 4 mm Cu loop, 5 mm outside the outermost nodes, tied to star ground (battery −, ONE point, G-J bonding law [V]). Function: fringe-field taming around the steering bars + pickup reduction; NOT a driven guard in v0.1. [U]
- **Steering bars:** 2 bars, 20 mm wide, at x = ±35 mm flanking the corridor (field span 7 cm), each fed by its own H-bridge channel — never through the sensing mux. Field at corridor center = V_drive / 70 mm.
- **Layout topology:** radial, zero crossings — all node tails run straight to a perimeter bus on the release sheet, tails exit at the +y wall. Single-layer foil net, cut by hand or vinyl cutter from a registered 1:1 template printed with the same file that prints the block (the print file IS the fab drawing; 4 printed fiducials on the lid register camera↔PCB coords, G-C homography [V]).
- **Mux tap points (channel map):** N1–N16 (row-major) → two CD74HC4067 muxes (X-leg and Y-leg) → ADS1115 #2 AIN0/AIN1 differential → any of C(16,2)=120 pairs [V G-C architecture; cube-1 ADS1115 #1 stays on the dead twin + lid vertical pairs]. ADS1115 run at **8–16 SPS**, log 1 Hz averages [V G-J]. Steering H-bridge enable is hardware-gated OFF during ADC conversion windows (GPIO-driven, verified in firmware bring-up). [U]

## 4. Capillary moisture (passive)

Reservoir → wicking columns → substrate, target moisture ~55–60% wt [V-adjacent: Mycofluid's 52% total with 60–75% as literature-normal [V G-I]]. No pumps, no valves in v0.1 (C18's valve logic is cube-3's active channel, deliberately not imported here). Moisture *gradients* as a steering lever (K10 lever #5) are available for free by doping the reservoir — but v0.1 holds moisture uniform, because attribution is the enemy (cube-1 law). Refill through the fill port is logged as a `status` trail row with mL; mass balance closes like C18's M6. [V doctrine, U numbers]

## 5. Zoned nutrient doping (growth steering, chemical half)

4 quadrants of the substrate plane, seeded zone line down the corridor midline:

| Zone | Doping | Rationale | Status |
|---|---|---|---|
| A (+x,+y) | plain spent oats | control quadrant | [V-adjacent] |
| B (−x,+y) | + brown rice flour ~14 wt% | carb dopant, Mycofluid-proven at that dose [V] | growth-rate steering |
| C (−x,−y) | + CaSO₄ (gypsum) pinch | standard substrate supplement folklore; ion map perturbation | [F — K5 owns the real answer] |
| D (+x,−y) | second species inoculation | zone-line seeding (the novel unit [V DESIGN_MULTISPECIES]) | species pair = open cell OC-2 (S1/G-B lane) |

Zoning method: v0.1 = post-print syringe/hand-pack zoning (free, G-I's endorsed v1 [V]); dual-paste head = v2. Continuous gradients explicitly not wanted (G-I verdict [V]). Electrical effect of doping = a designed resistance/conductivity map — that formalization is K5's lane, landing as **OC-3**.

## 6. Safe-voltage envelope (K7 not landed — the line stated here, K7 to own it)

**The hard line [V, fetched 2026-09-16, Wikipedia "Electrolysis of water"]:** water splitting is thermodynamic at **E° = −1.229 V (≈1.23 V) at 25 °C, unchanged at pH 7 by Nernst**; the thermoneutral point is **1.48 V**; practical electrolyzer cells run **1.5–2.0 V** at real current densities. Therefore:

1. **DC red line:** no wet metal–substrate interface in this block shall be held at |V| ≥ 1.23 V. Working ceiling **≤ 0.8 V DC** across any interface [U — margin is a guess pending K7's overpotential data for Cu/Ag in oat-medium].
2. **Bipolar pulse mitigation (the primary steering method):** charge-balanced biphasic pulse pairs — phase 2 (reversed polarity, equal charge) cancels net Faradaic charge at the electrode double-layer, standard neuromodulation practice [F — neurostim textbook canon, UNVERIFIED this session, **K7 owns it**]. Pulse width/gap/charge-density limits: **open cell OC-4**. Interpulse instantaneous field can exceed the DC ceiling only insofar as net delivered charge ≈ 0 — that claim itself is K7-verdict material.
3. **Current limiting:** series resistance per steering channel targeting ≤ 1 mA [U — depends on electrode area and medium impedance; K7].
4. **Readout isolation:** steering driver hard-gated off during ADC windows (§3); ADS1115 FSR ±0.256 V [V G-J] means steering voltages must never appear at mux commons — series R + firmware gate + a clamp diode to rails [U].
5. **Consequence, stated now because it is load-bearing:** the corridor's steering bars are 70 mm apart. At the 1.23 V DC line, the bulk field is only **~1.76 V/cm**. If fungal galvanotropism needs more (K2's plan asks whether 3–10 V/cm [F — K2's own framing, not yet evidence]), **the safe DC envelope is below the steering threshold and the block cannot steer with DC**. Pulsed-bipolar may close the gap or may not. This is the block's central physical gamble — see §9, biggest unknown.
6. Chronic-exposure tolerance of live mycelium to days-long fields: **open cell OC-5** (K7 §4).

## 7. Falsifier set

Inherited (each pre-registered before any scored data, C17 registration law [V]):

- **F1 Dead twin (primary control).** A second, identically printed + inoculated-then-killed block, wired to the same harness — cube-1 amendment makes it a *concurrent* channel from first power-up [V C17/G-J]. Every live claim must beat the matched twin, not history.
- **F2 Sham field.** Identical steering pulse train delivered into the **dead twin's** lattice (or through an unmated/blocked trace set in a second live block) — electronics, duty, leads all identical; O3's sham-light pattern applied to fields [V O3 pattern]. Growth/steering claims must beat sham-field blocks.
- **F3 Cage A/B.** 30 min cage-off / 30 min cage-on inside the first 4 h of the 72 h stage-0 run, live-vs-dead simultaneously — quantifies our own EM pickup in situ [V GA]. Steering "responses" must survive cage-on.
- **F4 Boundary falsifiers (inherited from G-C rung 2), tracker clause adopted wholesale:** if pigmentation/condensation/light drift defeats the camera pipeline, zone-line-correlated claims are untestable at this budget → auto-retreat [V G-C].

**NEW — F5 steering falsifier (galvanotropism claim):**

- **Prediction (pre-register):** under steered drive (pulsed-bipolar, envelope §6), the +x corridor half shows a hyphal-front position / density asymmetry toward the driven bar vs the sham-field twin, visible in the camera record AND as mux pair-asymmetry (impedance/SPR difference across the corridor midline), within one colonization week. Effect must be ≥2× the twin's same-sidedness [F threshold — number is a placeholder pending GA-style adjudication].
- **Falsified if:** (a) steered block indistinguishable from sham twin (galvanotropism not expressible in-block at safe envelope → the §6.5 gamble resolved NO); (b) the asymmetry appears **equally in the dead twin's conductivity map** — ion migration and electro-osmosis steer salts through dead wet medium too; only *growth* (camera-visible, live-only) counts; (c) the asymmetry co-varies only with SHT31/moisture regressors (the "wet cardboard" kill [V C17 amendment]) or dies in shuffled-label analysis (n=100, α=0.025 Bonferroni, C17 stage-2 law [V]).
- **Pre-register the alternative reading:** a pass localizes *steering*, not "compute" — it certifies the lattice as a write channel (DAD ceiling [V C17]). Task-level claims need the full stage ladder re-run on the block.

## 8. BOM by tier

| Tier | Contents | Cost | Basis |
|---|---|---|---|
| **T0 — reuse cube-1** (the ear + defenses) | ESP32, 2× ADS1115, ECG pads, foil cage, chloridized Ag wire, cal parts, SHT31 | **$34 floor / $60–66 with defenses** | [V G-J corrected stage-0 BOM, supersedes C17's $31] |
| **T-L lattice delta** (target ≤ $15) | 2× CD74HC4067 ($2 ea [V G-C]) · Cu foil tape 2-4 mm ($4–6 [U]) · H-bridge/steering driver ($2–3 [U]) · silver conductive paint/epoxy ($4–6 [U]) · PVA release sheet + grommets ($1–2 [U]) | **≈ $13–19** (core $13; worst-case $19 breaches the ≤$15 target — flag) | part-class street guesses [U] except muxes |
| **T1 — biology** | oyster spawn $14 [V] + second species LC $10 [F] + spent oats $0 (waste stream) + tubs $6 [V] | **$24–30** | [V CUBE1/C17] |
| **T2 — fab (only if printing)** | DIY paste extruder $30 [V G-I] … bolt-on head $100–165 [V G-I] … StoneFlower kit €600 [V G-I] | $0 (mold/hand-pack variant) – $600 | [V G-I]; **explicitly NOT inside the ≤$15 delta** |

Block total, hand-packed variant: **T0 + T-L + T1 ≈ $71–115** (floor ≈ $71 = 34+13+24; defended ≈ $115 = 66+19+30). Printed variant adds T2. Phasing identical to C17: no biology or lattice spend until T0 proves the ear (stage 0, operator word gates all spend).

## 9. Open cells (what K1–K11 must still answer)

| # | Cell | Owner | Blocks |
|---|---|---|---|
| OC-1 | Sensing pitch: 2 cm (this spec) vs G-C's ≤1 cm front-tracking law — corridor geometry arbitration | G-C / K12 | §3 grid |
| OC-2 | Species pair for the seeded zone line (fast grower × high-spiker from Adamatzky tables) | S1/G-B lanes | §5 zone D, F5 |
| OC-3 | Doping → conductivity/resistance map: which ions, what Δρ, do printed salt zones persist in a wet block | **K5** | §5, §3 impedance model |
| OC-4 | Bipolar pulse grammar: width, gap, charge-density limit, net-charge tolerance at Cu/Ag in oat medium | **K7** | §6.2–6.4 |
| OC-5 | Chronic field exposure: does days-long ≤0.8 V/pulsed drive harm oyster-class mycelium | **K7** | §6.5, F5 |
| OC-6 | Galvanotropism thresholds in fungi (V/cm, anode/cathode, species) — Europe PMC free-tier sweep found NO V/cm numbers today; K2's plan asks 3–10 V/cm | **K2** | §6.5 (the central gamble) |
| OC-7 | Grown-in conductive phase (mycelium-bound composites, carbonized/PEDOT paths) as lattice alternative to placed foil | **K4** | §3 material strategy |
| OC-8 | Stamets corpus: does prior art describe feeding networks into living mycelium + readout (novelty) | **K1** | §1 claim wording |
| OC-9 | Metal-lattice-in-living-mycelium prior art, any builder | **K9** | §1 claim wording |
| OC-10 | Steering toolkit ranking (chemo/electro/photo/thigmo/moisture) + the combination for zone-line engineering | **K10** | §5, F5 |
| OC-11 | K3, K6, K8, K11: receipts not even opened at this writing — scope unknown | — | — |
| OC-12 | Spent-oats paste recipe (moisture %, grind, xanthan) — class proven, exact recipe unproven | bench (G-I's own caveat) | §2 L2 |

**THE SINGLE BIGGEST UNKNOWN:** the **steering window** — whether a field strong enough to galvanotax hyphae can exist inside a wet conductive block *below* the electrolysis/cooking line at the traces. §6.5 puts the DC-safe ceiling near ~1.76 V/cm across this geometry [V line, U geometry margin]; the literature threshold for fungal galvanotropism is unverified and may sit 2–5× higher. If K2 lands thresholds above what K7's envelope allows (with pulsed-bipolar still inside the charge-balance budget), **the "conducted" half of the block dies honestly and it re-scopes to a sensed, doped, zone-lined living substrate** — which is still a paper-worthy artifact, but the write channel is the gamble.

---

**Status: SPEC v0.1 FILED — proposal tier, two-eyes pending, no spend.** Synthesis inputs: G-C, G-J, C17, C18, G-I, GA, CUBE1, DESIGN_MULTISPECIES (byte-read this session) · K1/K2/K4/K5/K7/K9/K10 read as opened skeletons (0 findings each at 18:49) — all K-dependent numbers above marked [U]/[F] and mapped to open cells. 1.23 V electrolysis line byte-verified live. No git, no paid APIs. This receipt ends where wave law puts it: the open-cells table above and the single biggest unknown.
