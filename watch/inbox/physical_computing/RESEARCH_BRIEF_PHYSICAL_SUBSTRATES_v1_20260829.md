# Research Brief v1.0 — Thermodynamic Computing and Ising Machines as Candidate Physical Computing Substrates

Author: Mark (@NachoQuixotic) · Date: 2026-08-29 · Prepared for multi-AI collaborative deliberation
Durable copy made 2026-09-16 from session paste (source temp dies). Status: round-1 complete
(two cohort responses in this folder); synthesis pack: watch/inbox/PHYSICAL_COMPUTING_PACK_20260916.md

## 0. Purpose and Shared Baseline

This brief is a common reference document for multiple AI systems and human researchers. It
consolidates the strongest claims, objections, and open questions, with structured source
metadata. The goal is not to declare a winner but to establish a shared baseline from which
independent conclusions can be formed and compared.

Consensus baseline (shared starting assumptions, not final conclusions):

1. **Physical systems can compute.** Water, light, thermal noise, coupled oscillators, and
   many other substrates can perform transformations usefully interpreted as computation.
2. **Analog/physical computing did not fail because physics lacked computational capacity.**
   It lost historical dominance because digital systems were easier to program, verify,
   copy, correct, and scale.
3. **AI changes the economics of physical computing.** ML can search device geometries,
   calibrate drift, compensate noise, control complex systems, and close the loop between
   simulation and physical measurement.
4. **Pancomputationalism is a real trap.** Not every physical process is a useful computer.
   Useful physical computation requires engineered correspondence between physical state and
   task-relevant output.
5. **Analog composability is fundamentally constrained.** Unlike digital thresholding, analog
   stages do not perfectly regenerate signals. Deep cascades lose information, accumulate noise.
6. **The practical architecture is shallow physical computation wrapped in deep digital
   orchestration.** The ecosystem is more like a reef than a stack of turtles.
7. **Efficiency advantages are real but historically contestable. Scaling-regime advantages
   are more durable but harder to prove. Complexity-class advantages are extremely rare and
   not yet established for existing devices.**
8. **A physical substrate's advantage must be measured at the full-system level** — encoding,
   control, measurement, verification, repeated runs.

## 1. Definitions

- **Physical computation:** a physical process whose native dynamics perform a transformation,
  rather than simulating it on a universal digital machine.
- **Substrate-native computing:** engineering systems where useful behavior emerges from the
  physics of the substrate itself. (Round-1 verdicts on this term diverged — see cohort files.)
- **Thermodynamic computing:** exploiting thermal/stochastic fluctuations as a computational
  resource, especially for sampling from probability distributions.
- **Ising machine:** a physical or specialized digital system that finds low-energy
  configurations of an Ising-type Hamiltonian, for combinatorial optimization.
- **Efficiency advantage:** same effective computation, lower energy or latency.
- **Scaling-regime advantage:** empirical improvement in scaling behavior for a family of
  instances after full-system costs are included.
- **Complexity-class advantage:** a formally proven asymptotic separation from the best
  relevant digital algorithm.

## 2. Deep Dive A — Thermodynamic Computing and the Extropic TSU

### 2.1 Principle
Conventional computing treats noise as corruption. Thermodynamic computing treats noise as a
resource: a device designed to **sample from a programmable probability distribution** by
exploiting natural stochastic dynamics. Aligns with energy-based models, Bayesian inference,
Monte Carlo sampling, generative models, Boltzmann machines, stochastic neural networks.

### 2.2 Reported Implementation
- Company: Extropic · Device: Thermodynamic Sampling Unit (TSU) · Production chip: Z1
- Company-reported: >250,000 probabilistic bits on one die; die under 12×12 mm; under 1 W;
  samples directly from programmable distributions; claimed orders-of-magnitude energy
  reduction vs GPU sampling for relevant workloads.
- Companion control chip XTR-0 manages low-latency digital/analog handoff — company-specific,
  subject to independent verification.

### 2.3 Public Funding Signal
U.S. Dept. of Commerce, CHIPS for America: **non-binding letter of intent** for up to $75M
proposed for Extropic. A policy signal, not technical validation.

### 2.4 Critical Caveats (preserve in all downstream discussion)
Efficiency claims are company-reported and workload-dependent. GPU baselines can be optimized
with specialized libraries, lower precision, pruning, new algorithms. Full-system energy must
include ADC, digital control, memory, I/O, calibration. Sampling quality is not raw speed:
fidelity, mixing time, correlation structure, effective sample count. Thermodynamic devices
are specialized probabilistic coprocessors, not general-purpose computers. Digital hardware
may erode the efficiency gap. The composability wall applies: a thermodynamic sampler is
unlikely to replace deep analog chains.

### 2.5 Bottom Line
Extropic is the strongest current demonstration that noise-as-resource can be a commercially
relevant computational primitive. The claim is not that thermodynamics replaces computation —
it is that thermodynamics is an unusually efficient native substrate for sampling.

## 3. Deep Dive B — Coherent Ising Machines and Other Physical Ising Solvers

### 3.1 Problem Class
Many hard combinatorial optimization problems map to finding the ground state of an Ising
Hamiltonian H = −Σ J_ij σ_i σ_j, σ ∈ {−1,+1}: max-cut, graph partitioning, scheduling,
circuit layout, spin glasses. Digital solvers use simulated annealing, parallel tempering,
specialized local search, branch-and-bound. Worst case NP-hard; heuristics dominate practice.

### 3.2 CIM Principle
A coherent Ising machine uses a network of degenerate optical parametric oscillators (or
equivalent). Each oscillator's phase state represents a spin; oscillators are coupled per the
problem's coupling matrix; the system physically relaxes toward low-energy configurations.
The relaxation itself is the algorithm — the search is embedded in the dynamics, not emulated.

### 3.3 Reported Results
A widely cited result: a 100,000-spin CIM achieving ~1,000× faster solutions than a simulated
annealing baseline on selected fully connected max-cut instances. Significant; read carefully.

### 3.4 Caveats and Competition
The comparison was against one specific simulated annealing implementation; modern GPU/FPGA/
ASIC heuristics are much stronger. Dense coupling encoding imposes overhead; auxiliary
variables and routing reduce physical parallelism. Full-system time must include embedding,
setup, readout, verification, repeated sampling. No asymptotic separation from best digital
heuristics established. Quantum annealers and digital annealers compete. Defensible statement:
CIMs may provide a scaling-regime advantage for certain dense, structured instances — not yet
demonstrated cleanly against modern optimized digital baselines under equal-quality, full-system accounting.

### 3.5 Bottom Line
Ising machines are the clearest test case for device-level speed vs durable computational
advantage. The device may relax quickly; the question is whether the whole computation stays
faster and cheaper as problems grow.

## 4. Comparative Assessment Matrix

| Dimension | Thermodynamic TSU | Coherent Ising Machine |
|---|---|---|
| Computational primitive | Sampling from programmable distributions | Relaxation into low-energy spin configurations |
| Primary workload | Generative AI, Bayesian inference, Monte Carlo | Combinatorial optimization |
| Reported advantage | Orders-of-magnitude energy efficiency for sampling | Large problem capacity; fast physical relaxation |
| Advantage type | Mainly efficiency | Possible scaling-regime, unproven complexity |
| Full-system overhead | ADC/DAC, calibration, digital control | Coupling embedding, readout, repeated runs |
| Composability | Low; single-stage sampler | Low to medium; embedding costs |
| Digital competition | GPU/TPU sampling, algorithmic improvements | GPU/FPGA/ASIC heuristics, parallel tempering, learned solvers |
| Maturity | Early commercial; publicly funded R&D | Research demonstrations; partial commercialization |
| Main risk | Digital efficiency catch-up | Hard to beat modern algorithmic baselines after overhead |

## 5. Core Open Questions

- **Q1.** Is "sampling" the right first substrate-native niche — uniquely suited to
  thermodynamics, or just the currently visible generative-AI bottleneck?
- **Q2.** What counts as durable proof of physical advantage? Proposed: full-system energy
  per useful operation; time-to-solution at equal quality; repeated-run cost; scaling
  crossover vs modern digital baselines; robustness to algorithmic response.
- **Q3.** Is the efficiency/scaling/complexity taxonomy right? Or distinguish constant-factor,
  polynomial, asymptotic, algorithmic-structure, problem-distribution-specific?
- **Q4.** Does the composability wall apply uniformly? Can optical systems compose better?
- **Q5.** What role should AI play — designer, calibrator, co-evolver, harness optimizer, all four?
- **Q6.** Is "substrate-native computing" the right term? Alternatives: physical computation,
  natural computation, embodied computation, non-von Neumann, analog-native, ecological.
- **Q7.** Is the shallow-physical/deep-digital reef architecture stable, or will some workloads
  justify deeper physical stacks?

## 6. Source Register (round 1)

| ID | Source | Type | Notes | Access Date |
|---|---|---|---|---|
| S1 | Extropic, company technical publications and blog | Primary/company | TSU, Z1 specs, energy claims. Company-reported; not independently verified. | 2026-08-29 |
| S2 | U.S. DoC / NIST CHIPS for America announcement | Government | Non-binding LOI, up to $75M proposed for Extropic. | 2026-08-29 |
| S3 | Inagaki et al. (authorship corrected by cohort: Honjo et al.), "100,000-spin coherent Ising machine," Science Advances [verify DOI] | Peer-reviewed | ~1,000× speed vs simulated annealing on selected Max-Cut. | 2026-08-29 |
| S4 | Nature Reviews Physics, review of Ising machines | Peer-reviewed | Cautions against overclaiming; strong digital competition. | 2026-08-29 |
| S5 | Google Research, learned chip placement with RL | Primary/industry | AI search over hardware design space. | 2026-08-29 |
| S6 | Stanford Encyclopedia of Philosophy, "Physical Computation" | Encyclopedia | Pancomputationalism constraints. | 2026-08-29 |
| S7 | Science Museum Group / LSE archives on MONIAC | Museum/primary | Bill Phillips' hydraulic economic computer. | 2026-08-29 |
| S8 | Moscow Polytechnic Museum refs on Lukyanov integrator | Museum/secondary | Early Soviet hydraulic integrators. | 2026-08-29 |
| S9 | Quanta Magazine on Extropic [verify] | Secondary | Accessible framing. | 2026-08-29 |
| S10 | Extropic/partner technical paper on thermodynamic sampling [verify] | Primary/technical | Needed for independent error-rate and sampling-quality analysis. | 2026-08-29 |

## 7. Suggested Next Steps for the AI Cohort

Each system, in its own voice: state baseline acceptances; rejections/modifications; the
strongest uncertainty in the Extropic claim; the strongest uncertainty in the Ising claim;
one testable prediction/experiment; one conceptual refinement to the taxonomy; defend or
abandon "substrate-native computing"; at least one additional source. Outputs merge into a
living document — disagreement preserved, not averaged away.

## End of Research Brief v1.0
Round-1 cohort responses preserved in this folder. Synthesis and round-2 program:
watch/inbox/PHYSICAL_COMPUTING_PACK_20260916.md
