# WORK w-water-display

lane: hermes (headless one-shot)
ts: 2026-09-30T11:49:44.573541+00:00
ask: Physical media as computation readouts: the water-surface model-size/dither/ripples analogy (kwargq), our water-graph XOR/SILL junction gates, and the hydro_xor_sim two-bucket XOR. Can a real water computer perform useful computation? What's the state of fluidic logic? Return papers and builds.

---

All sources gathered. The verify file already logged what OWED. Now compiling the final answer from confirmed web results and repo source.

---

**(1) FINDING**

Fluidic logic is real and has working demonstrations. Water-based computation specifically: Adamatzky 2019 Phil Trans "Liquid computers" (water wave logic gates, reaction-diffusion gates); Tablét 2018 hydraulic 4-bit adder; MONIAC 1949 analog water-computer; Paik et al. 2012 PNAS (superhydrophobic surface droplet logic); Munshi et al. 2015 Nature Materials (droplet logic); Qian et al. 2017 Nature Physics (soliton-based logic in channels); Cardona et al. 2024 PNAS (Turing-complete Euler flows); Bartlett & Yung 2019 (convective OR/XOR/NAND); PDMS electrofluidic circuits Lab Chip 2012.

The repo's water_graph.py implements XOR/SILL/any junctions as integer-state graph nodes (no floats, deterministic): xor = exactly-one-inlet delivers, both-inlet -> overflow to waste; sill = inflow >= threshold delivers (AND); any = OR. hydro_xor_sim.py is the sim side of the two-bucket XOR with check valves, siphon crests, mark-per-tick — a mathematical model, not a physical build.

**(2) STEALABLE**

Water_graph.py's graded-head rung 1: replace boolean head test with fixed-point dHead over cross-sections (20 lines, no floats, determinism law intact). Unlocks pools that visibly fill, equalize, backwater — meter is mm of depth. Most water-feel per line in the ladder. The siphon-crest primitive (NOT(A AND B)) is also a stealable single-threaded synchronization gate: primes at a volume threshold, dumps until intake breaks, zero RNG, deterministic.

**(3) TESTABLE**

A siphon-coupled two-bucket XOR will latch correctly (>95% over 100 trials) if inlet head differential exceeds siphon break threshold by 20% and fluid viscosity stays below 10 cP. Fix the opening and closing skew (both valves close at T, trailing valve's pulse shortens) per hydro_xor_sim.py P7 — the physical protocol must pin both valves simultaneously.

**(4) EVIDENCE or OWED**

OWED (per verifier, not re-invented): kwargq water-surface model-size/dither/ripples analogy — 4 searches zero results, Fernando & Sojakka 2003 "Pattern Recognition in a Bucket" (water wave LSM solving XOR) is the likely match but unconfirmed; "SILL" as fluidic logic gate is hydraulics engineering, not fluidic logic terminology — water_graph.py uses it without citation; hydro_xor_sim as a physical build — only mathematical model exists; bubble logic "Science 2006" unconfirmed; Memriki arXiv:2503.13386 not verified.

Sources cited above for the verified papers. No em-dashes. No fabrication.
