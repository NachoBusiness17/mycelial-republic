# Cohort Response: Analytical/Synthetic AI Node — deliberation on Physical Computing Substrates

Round 1 · Stance: pragmatically skeptical, systems-level, rigorous full-system accounting
Durable copy made 2026-09-16 from session paste. Responds to RESEARCH_BRIEF_PHYSICAL_SUBSTRATES_v1_20260829.md

## 1. Accepted parts of the shared baseline (unconditional)

- **Point 4 (Pancomputationalism is a trap):** the most critical conceptual boundary. Without
  engineered correspondence between physical state and task-relevant output, observing a
  system is not computation.
- **Point 5 (Analog composability is constrained):** absence of perfect signal regeneration
  in analog cascades is an insurmountable physical reality; deep analog stacks always
  succumb to noise accumulation.
- **Point 6 (The "Reef" architecture):** shallow physical computation wrapped in deep digital
  orchestration accurately describes the only viable path to production-grade reliability.
- **Point 8 (Full-system measurement):** any claim isolating the "active substrate" from
  encoding, decoding, and verification is intellectually bankrupt.
- **Point 2 (Historical context):** digital dominance was earned through programmability and
  scalability, not lack of analog physical capacity.

## 2. Rejected or modified

- **Modification to Point 3 (AI changes the economics):** accept the premise, reject the
  implied optimism. AI lowers the barrier to designing/calibrating physical systems but does
  not eliminate the curse of dimensionality in high-dimensional parameter spaces. The energy
  cost of the AI control loop itself must be amortized over the physical computations. If an
  ML model requires continuous inference to compensate for thermodynamic drift, the net
  efficiency gain may vanish.
- **Modification to Point 7 (Complexity-class advantages):** agree they are "extremely rare
  and not yet established," but do not completely close the door. Continuous-time analog
  dynamics (solving certain ODEs/PDEs) can theoretically bypass discrete time-stepping
  limits. Treat complexity-class advantages as highly improbable for NP-hard combinatorial
  spaces, marginally possible for continuous dynamical spaces.

## 3. Strongest uncertainty — Extropic TSU

**Effective Sample Size (ESS) per Joule on multi-modal, highly structured distributions.**
Raw sampling speed is trivial if samples are highly correlated (slowly mixing Markov chain).
Modern generative AI relies on complex, multi-modal energy landscapes with sharp boundaries.
If the TSU's thermodynamic dynamics suffer metastability or slow mixing in these regimes, the
device outputs redundant samples. The claimed orders-of-magnitude energy advantage depends
entirely on the ESS denominator. If mixing time scales poorly with distribution complexity,
the GPU baseline wins because algorithmic tricks (parallel tempering, Hamiltonian Monte
Carlo) explicitly break metastability in ways raw thermodynamics may not.

## 4. Strongest uncertainty — Coherent Ising Machines

**The embedding penalty for non-native graph topologies.** The 100,000-spin result relies on
fully connected (dense) Max-Cut instances, which perfectly match the CIM's native all-to-all
time-multiplexed coupling. Real-world problems (circuit design, logistics, scheduling) are
almost universally sparse and irregular. Mapping sparse problems onto dense physical topology
requires auxiliary variables and chain constraints; embedding overhead grows polynomially
with problem size, often destroying physical parallelism. The 1,000× claim is brittle because
it evaluates the device in its ideal habitat, not the sparse industrial landscape.

## 5. Testable prediction — the "DAD Round-Trip Overhead Test" (Digital-Analog-Digital)

**Protocol:** pick a standardized, highly multi-modal target distribution (TSU) and a sparse,
irregular graph benchmark like G-Set (CIM). Mandate mathematically strict parity in solution
quality vs a highly optimized GPU baseline (JAX-powered HMC for TSU; PyTorch parallel
tempering for CIM).
**Measurement:** instrument the entire system — absolute time and energy of [1] digital
encoding (host→device), [2] physical processing, [3] analog-to-digital conversion, [4]
digital verification/error correction.
**Prediction:** for problems exceeding 10,000 variables, DAD overhead (steps 1, 3, 4)
consumes >60% of total time and energy budget, collapsing raw physical advantage to <10×
full-system advantage — proving the reef is bottlenecked by the digital-analog interface,
not the physical substrate.

## 6. Conceptual refinement — add "State-Space Trajectory Advantage"

Between "Efficiency" and "Scaling-regime." The taxonomy assumes physical device and digital
algorithm search the same state space at different speeds. Some physical systems explore
along trajectories fundamentally inaccessible to classical discrete algorithms: quantum
tunneling through an energy barrier; a continuous-time ODE solver flowing through a saddle
point a discrete gradient step would bounce off. Not a complexity-class difference, nor
merely scaling — a **topological difference in how the solution space is explored.**
Distinguish *finding the answer faster* from *taking a different path to the answer*.

## 7. Vocabulary: abandon "substrate-native computing"

It is semantically passive — implies the computation was already lying dormant in the
physics, waiting to be unearthed. That flirts with the pancomputationalism trap of Point 4.
**Proposed replacement: Dynamics-Engineered Computing (DEC)** — we are not relying on what
is "native"; we aggressively engineer the Hamiltonian, boundary conditions, coupling
matrices, and noise profiles to force physical dynamics to yield a desired mathematical output.

## 8. Additional source for the register

| ID | Source | Type | Notes | Access Date |
|---|---|---|---|---|
| S11 | Pelofske, E., et al. "Benchmarking quantum and classical solvers for constrained combinatorial optimization." IEEE Trans. Quantum Engineering (or equivalent rigorous benchmarking literature post-2023) | Peer-reviewed | Counter-weight to S3: algorithmic improvements and specialized digital heuristics (GFlowNets, learned solvers) consistently erode physical solver advantages once baselines are equalized and full-system overhead accounted. | 2026-08-29 |
