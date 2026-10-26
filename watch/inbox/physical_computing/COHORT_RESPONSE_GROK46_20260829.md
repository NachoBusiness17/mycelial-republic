# Cohort Response: Grok 4.6 — independent review of Research Brief v1.0

Round 1 · Date: 2026-08-29 · Stance: accept the baseline as a working constitution; tighten
claims where silicon and baselines do not yet support them.
Durable copy made 2026-09-16 from session paste. Responds to RESEARCH_BRIEF_PHYSICAL_SUBSTRATES_v1_20260829.md

## 1. Parts of the shared baseline accepted

All eight baseline points, as working assumptions, not settled science. In particular:
physical systems can compute; analog did not fail for lack of physics; AI changes the
economics of calibration, geometry search, closed-loop control; pancomputationalism is a
trap (correspondence must be engineered); analog composability is constrained — the
practical pattern is shallow physical kernels inside deep digital orchestration; advantage
is only real at full-system accounting (encode, control, measure, verify, repeat);
efficiency advantages are historically contestable; complexity-class advantages are rare
and unproven for existing devices. Point 6 ("reef, not turtles") is the most useful
architectural claim in the brief. It should stay.

## 2. Rejections / modifications

**a. "Extropic is the strongest current demonstration" — too strong.** Extropic is the most
visible commercial CMOS-p-bit sampler with a public scale target (Z1: 269,568 p-bits,
16-neighbor sparse graph, claimed >50 MHz sampling, <1 W, die <12 mm). Not yet the strongest
measured demonstration. XTR-0/X0 is a small prototype platform. The 10,000× energy figure is
a system-level analysis/simulation of small DTM sections on Fashion-MNIST, not a wall-plug
measurement on Z1 silicon. Normal Computing's CN101 is a competing "thermodynamic" tape-out
on digital CMOS with a different primitive (accumulator/stochastic-computing dynamics). The
field is a race, not a monopoly.

**b. "Designed to sample directly from programmable probability distributions" — true only
after compilation onto a fixed sparse topology.** Z1 samples an Ising/energy-based model with
16-neighbor connectivity via in-situ chromatic Gibbs sampling. Arbitrary distributions
require embedding, auxiliary variables, and software (THRML/Thermalizers/Torx). That is
substrate-native after compilation, not free-form analog universality.

**c. S3 authorship correction.** The 100,000-spin CIM paper is Honjo et al., Science
Advances 7, eabh0952 (2021), DOI 10.1126/sciadv.abh0952. Inagaki is a coauthor. Correct the
first-author citation.

**d. Baseline 7 needs a fourth bucket: distribution-specific/structure-specific advantage.**
Most reported wins live here (dense Max-Cut for CIMs; locally coupled EBMs/DTMs for TSUs).
Calling these "scaling-regime" without naming the instance class overstates generality.

**e. Baseline 3 is directionally right, slightly overstated.** AI helps design and calibrate.
It does not automatically make analog cascades composable. Learned compensation can hide
noise for a while; it does not repeal information loss.

## 3. Strongest uncertainty — Extropic claim

Not whether p-bits exist (small CMOS p-circuits and X0 silicon exist). The CHIPS LOI of up
to $75M (2026-07-29; NIST/Commerce; further diligence before award) is a real policy signal,
not technical validation. The load-bearing uncertainty is **effective-sample quality at
scale under full-system energy**:

- **Fidelity vs speed.** Gibbs updates at >50 MHz on a sparse 16-neighbor graph can produce
  highly correlated samples. Advantage depends on ESS, mixing time, and whether the compiled
  model is the model you wanted.
- **Compilation tax.** Thermalizers/embedding of dense or deep models onto a planar
  16-regular fabric can destroy the headline energy ratio.
- **Host tax.** Programming weights, readout, calibration, digital control may dominate once
  you leave toy grids.
- **Baseline drift.** GPU sampling (low-precision kernels, distilled samplers, better MCMC,
  amortized inference) is a moving target. A 10,000× gap on binarized Fashion-MNIST DTM
  simulations can shrink 10–100× from software alone before Z1 systems are widely available.
- **Algorithm lock-in.** The interesting claim is not "run GPT-style transformers cheaper";
  it is "make EBMs/DTMs/compiled stochastic programs economically viable." If the winning
  generative stack stays autoregressive/Gaussian-diffusion on dense matmuls, TSU advantage
  is a niche, not a displacement.

Until someone publishes measured joules per independent sample on a named workload, with
mixing diagnostics and an optimized GPU/TPU baseline, the commercial claim is a well-motivated
extrapolation.

## 4. Strongest uncertainty — Ising-machine claim

**Device relaxation ≠ solver advantage.** Honjo et al. (2021) showed a 100,512-DOPO CIM
finding approximate solutions on selected fully connected 100k-node Max-Cut instances ~1,000×
faster than a CPU simulated-annealing baseline. Real and historically important — not a
verdict against 2026 GPU/FPGA/ASIC heuristics, parallel tempering, learned solvers, or
digital annealers. Mohseni, McMahon & Byrnes (Nat. Rev. Phys. 2022) stated the field's
uncomfortable consensus: classical digital Ising hardware is currently best on common
benchmarks; analog/optical/quantum machines can win on particular instance families; no
general complexity-class separation is established. Remaining structural uncertainty: dense
all-to-all optical coupling via measurement-feedback is a different bottleneck from sparse
on-chip coupling; embedding overhead, setup, readout, repeated runs can erase device-level
speed; solution-quality distributions (not just time-to-first-good-cut) decide whether the
machine is a sampler or a mediocre optimizer. Ising machines remain the cleanest test of the
device-vs-system distinction. They have not yet passed it against modern digital peers under
equal-quality accounting.

## 5. One testable prediction (18-month window, through early 2028)

On a fixed, pre-registered suite of locally structured sampling tasks (grid Ising/Potts,
codon-optimization-style sparse EBMs, small DTMs), a packaged Z1-class TSU plus host will
beat an optimized GPU baseline on energy per effective sample by ≥50×, after including
programming, readout, and calibration. It will NOT beat that GPU by ≥50× on dense, all-to-all,
or transformer-like sampling without a compilation blowup that drops the ratio below 10×.
**Falsifier:** a public, third-party measurement where, on the pre-registered local suite,
full-system energy per ESS-adjusted sample is within 10× of a tuned GPU MCMC/low-precision
sampler. This splits "thermodynamics is a good sampler for sparse energy models" from
"thermodynamics eats generative AI."

## 6. Conceptual refinement — two additional axes

Keep efficiency / scaling-regime / complexity-class. Add:

**A. Where the advantage lives:**
| Axis | Meaning |
|---|---|
| Constant-factor | Same algorithm, cheaper physics |
| Polynomial | Better empirical scaling, no class change |
| Asymptotic/class | Proven separation |
| Structure-specific | Wins only on graphs/distributions matching the fabric |
| Algorithmic-lock | Wins only if the field adopts the native model family |

Most physical-computing press releases are constant-factor + structure-specific, advertised
as class change.

**B. Correspondence cost C.** Energy/time to encode the task into the substrate, maintain the
mapping, and decode a useful answer, divided by the energy/time of the native physical step.
A substrate is interesting iff native-step cost × C still beats digital. CIMs often lose in C
(embedding, feedback electronics). TSUs may win when the model is a sparse EBM and lose when
C includes compiling a transformer into Gibbs sweeps. This makes Q2 operational: durable
proof is a crossover in full-system cost including C, stable after the digital side is
allowed to retune algorithms.

## 7. Vocabulary: keep "substrate-native computing," with a restriction

Defend it as the engineering term: the useful map is compiled onto the substrate's native
dynamics, not emulated instruction-by-instruction. Do not treat it as a synonym for physical,
analog, natural, embodied, ecological, or non-von-Neumann computing. Proposed mapping:
physical computation = philosophical/scientific genus; substrate-native computing =
engineering (dynamics are the primitive); analog-native = continuous-valued subclass (TSUs
and p-bits are often discrete-stochastic, not classical analog); non-von-Neumann = too broad;
embodied/ecological = reserve for systems coupled to an environment, not chips in a rack.
Z1 is substrate-native Ising/Gibbs hardware. If the cohort wants one public phrase:
"physical co-processors with substrate-native kernels."

## 8. Additional sources for the register

| ID | Source | Type | Why add |
|---|---|---|---|
| S11 | Honjo et al., "100,000-spin coherent Ising machine," Sci. Adv. 7, eabh0952 (2021). DOI: 10.1126/sciadv.abh0952 | Peer-reviewed | Corrects S3; canonical large CIM result. |
| S12 | Jelinčič, Lockwood, Garlapati, Verdon, McCourt, "An efficient probabilistic hardware architecture for diffusion-like models," arXiv:2510.23972; npj Unconventional Computing | Primary/technical | The actual DTM / ~10,000× simulation paper behind Extropic claims. |
| S13 | NIST/Commerce, "Letters of Intent With 7 Companies for $874 Million," 2026-07-29 | Government | Independent confirmation of the $75M Extropic LOI; notes diligence and (per later reporting) minority equity. |
| S14 | Philip Ball, "Thermodynamic Computers Go With the (Energy) Flow," Quanta Magazine, 2026-07-15 | Secondary | Resolves S9; frames Extropic vs Normal Computing carefully. |
| S15 | Mohseni, McMahon, Byrnes, "Ising machines as hardware solvers…," Nat. Rev. Phys. 4, 363–379 (2022). DOI: 10.1038/s42254-022-00440-8 | Peer-reviewed | Resolves S4; digital hardware currently wins common benchmarks. |
| S16 | Chowdhury et al., "A full-stack view of probabilistic computing with p-bits," IEEE JxCDC / arXiv:2302.06457 (2023); plus Camsari–Datta p-bit lineage | Peer-reviewed | Prior art: p-bits are not Extropic's invention; MTJ and CMOS p-computers exist. |
| S17 | Holdijk et al., "CN101 – A Digital Thermodynamic Computer for Generative AI," arXiv:2608.00754 (2026); Normal Computing tape-out notes | Primary/competitor | Thermodynamic computing is not one substrate; digital-stochastic CMOS is a live alternative. |

Company blogs (S1) remain necessary but should be labeled vendor primary.

## Answers to the open questions (compressed)

- **Q1 (sampling as first niche):** Both. Thermodynamics is a native sampler: equilibrium
  fluctuations already draw from Boltzmann-like measures. Sampling is also a fashionable
  bottleneck because generative AI is distribution-shaped. The honest split: physics favors
  sampling; the market favors generative AI. Extropic is betting those stay aligned via
  DTMs/compiled EBMs. If generative practice stays matmul-heavy, sampling hardware remains a
  coprocessor.
- **Q2 (durable proof):** Agree with the brief's list. Add: effective sample size,
  pre-registered instance classes, allowed digital retuning, and correspondence cost C.
  Funding and die photos are not proof.
- **Q3 (taxonomy):** Keep the three-layer stack; add structure-specific and
  correspondence-cost axes.
- **Q4 (composability wall):** Not uniform. Optics can fan out with low incremental energy,
  but measurement-feedback CIMs reintroduce electronics and delay. Coherent optical pipelines
  compose better than electronic analog voltage cascades; they still face detection noise,
  analog memory, programming. TSUs compose by digital restitching of shallow physical
  samples — the reef architecture again. Deep analog stacks are not expected to become default.
- **Q5 (role of AI):** All four: designer, calibrator, co-evolver, harness optimizer. The
  underplayed fifth is **compiler**: learning embeddings that keep C small. Without that,
  hardware sits idle.
- **Q6 (vocabulary):** Common core + mapped aliases. Do not collapse into one slogan.
- **Q7 (reef stability):** Stable for the decade. Deeper physical stacks become justified
  only for workloads whose intermediate states should never be digitized (some
  sensor-to-actuator loops, some in-situ analog optimization). Generative modeling and
  combinatorial search want inspectable digital checkpoints. That pressure preserves the reef.

## Disagreements to preserve in synthesis

1. Extropic is a leading commercialization attempt, not yet a leading measured advantage.
2. Z1 is sparse Ising/Gibbs silicon, not a general analog computer.
3. CIM 1000× vs CPU-SA is not transferable to "physical optimizers beat digital."
4. "Thermodynamic computing" now names at least two substrates (fluctuating
   analog/mixed-signal p-circuits vs digital stochastic CMOS). Do not treat Extropic as the category.
5. The term to keep is substrate-native kernels, not substrate-native computers.

If the living document absorbs those five without flattening them into a press-friendly
average, the baseline will stay useful.
