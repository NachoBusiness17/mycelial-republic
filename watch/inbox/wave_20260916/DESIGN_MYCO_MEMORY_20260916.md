# DESIGN_MYCO_MEMORY_20260916 — steal sheet from R1 swarm research (wave_20260916)

Sources: `r1_fanout_runs/raw.jsonl` (12/12 myco qids answered, free lanes, $0).
**Doctrine: every number below is a LEAD from a free-tier model, not a fact.** Several lanes
produced plausible-looking but fabricated citations (one lane cited a court case for a
Ganoderma temperature spec and a rickrolled YouTube link — treat all DOIs as unverified until
checked against the actual paper). The cube's own instruments are the referee.

## The memory hierarchy model that fell out

| Tier | Medium | Timescale (lead) | Write | Read |
|---|---|---|---|---|
| L1 | ionic/membrane potentials, memristive hysteresis | seconds–hours | ±0.55 V pulse trains (lead) | electrodes / impedance |
| L2 | tube-diameter topology (Tero dynamics) | minutes–hours (reroute 30–90 min) | flow / nutrient gradients | impedance spectroscopy |
| L3 | hyphal growth topology | days–weeks (Pleurotus 1.5–4.2 mm/day lead) | environment: moisture, temp, barriers | time-lapse imaging |

## The 5 steals

1. **Mycelium memristance as the L1 register.** Lead: reversible switching at ~±0.55 V,
   on/off ~5–22, retention ≥10^4 s (~2.8 h), endurance only ~120 cycles before degradation;
   bit stored as K+/Cl- redistribution + wall hydration. Gives an electronic write path that
   does not wait on growth. (M05, M04)
2. **Reservoir readout is just a linear layer.** Physical-reservoir recipes: inject pulses,
   record multi-channel, train ridge/logistic regression on top; Physarum reservoirs on
   NARMA/XOR-class tasks are published. No exotic hardware — the cube's compute substrate is
   the same 16-channel stack used for recording. (M03, M07, M11)
3. **Tero rule as the L2 state equation.** dD/dt = a·|Q|^γ/D − bD; tube thickening visible
   ~5 min under strong gradient, reroute 30–90 min, unused tubes prune. Tube diameter is a
   writable, physically persistent state variable readable non-destructively by impedance.
   (M04)
4. **OECT (PEDOT:PSS) as the head that touches the biology.** Ionic gating (Na/K/Cl) →
   electronic current at sub-1 V; standard materials (Clevios PH1000 + DMSO/EG doping);
   this is the transducer that lets silicon read an ionic substrate without poisoning it.
   (M06)
5. **Surrogate-data falsifier built into the stack.** Spike-"language" claims (Zipf fits)
   die under shuffle tests, dead-mycelium baselines, and surrogate ISI permutation; lanes
   themselves disagreed on whether fungal action potentials exist at all (M01 says slow
   potentials only; M09 cites ~1800 Pleurotus spikes). Every cube signal must beat shuffled
   and sterilized-substrate controls or it is noise. (M09, M01, M02)

## Instrumentation BOM (lead, from M11 + M07)

OpenBCI Cyton + Daisy = 16 ch, 24-bit, up to 16 kS/s, ~$530 with electrodes/power/SD;
noise floors ~1.5 µVrms (Intan 32 ch lab grade) to ~15 µVrms (hobbyist). Ag/AgCl or Pt
electrodes, agar-bridged. Under $600 for the whole L1/L2 instrumented cube.

## The one mechanism that changes build order if true

**Electrical write + electrical read inside living mycelium (memristive hysteresis at
~±0.55 V, hours retention).** If verified with the Cyton rig, the cube is a genuine layered
memory hierarchy from week one: build electrodes + impedance/OECT head first, growth-topology
imaging becomes the archival L3 built last. If falsified (M01's skepticism wins), the cube
collapses to structural memory only (L2/L3, tube dynamics + growth) and the project slows to
days-scale feedback loops — so this is the first experiment to run.

## Verification queue (cheapest falsifications first)

1. ±0.55 V pulse response + hysteresis loop on a mycelium block, dead-block control (M05).
2. Impedance sweep correlation with known tube topology changes (M04 readout).
3. Spike/slow-potential rate vs sterilized baseline, shuffle test (M01 vs M09).
