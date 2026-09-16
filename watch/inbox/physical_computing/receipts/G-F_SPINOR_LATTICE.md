# G-F_SPINOR_LATTICE — receipt (wave lane: physical_computing / GAP G-F)

**Gap:** the operator's own math, never built. Belt-trick lattice (720° spinor untangle —
naive 360° fails, Lipschitz-bounded march, domain repetition for lattice representation;
his 2026-07-18 diary entry "Dirac Belt Trick with Domain Repetition for Lattice
Representation" + Three.js scene, never implemented as shader) meets the printed lattice:
what would a 720°-symmetric CHANNEL/PATH TOPOLOGY mean for the Dirac layer's fluid
channels or hyphal network? (Cube 3, DESIGN_MULTISPECIES_LATTICE_20260916.md: "spinor-
parable geometry in the lattice design, water in the channels, mycelium in the walls.")
**Wave law:** receipt FIRST, append as you go · no git · no paid APIs · WebSearch/WebFetch only.
**Date:** 2026-09-16

## Socratic tease

1. Is there a real computational meaning to orientability/double-cover in a transport
   network — e.g. two channel families that must both be traversed to return to identity,
   phase picked up per loop?
2. What published work connects spinor/covering-space structure to physical networks or
   reservoir computing? (search seeds: spinor lattice reservoir, covering space network
   computation, topological computation channels)
3. Design: the SMALLEST printable artifact whose behavior distinguishes a 360° loop from
   a 720° loop — in flow, in hyphae, in wire?

## Log (appended as gathered)

- [receipt opened — repo anchors pulled, searches starting]

### Search 1 — "spinor lattice reservoir computing" (landed as spintronics PRC)

- Physical reservoir computing (PRC) reviews: Tanaka et al. 2019 "Recent advances in
  physical reservoir computing" (the citable baseline); Springer tutorial 2024;
  arXiv 2412.13212 intro.
- Spin-based RC is REAL and published: spin-wave interference reservoirs (IOP Neuromorph.
  Comput. Eng. 2024, "Fast physical reservoir computing with nonlinear spin wave
  interference"; npj Spintronics 2024 nanoscale spin-wave RC); skyrmion-crystal spin-wave
  RC; spintronic RC with interpretable nonlinearity (Phys. Rev. Research 7, 013310, 2025).
- KEY NUANCE for G-F: "spin" in spintronic RC = magnetization dynamics (SO(3)-classical),
  NOT spinor (SU(2) double-cover) structure. Nobody in the RC literature uses the
  double-cover property AS the computational resource. UNPROVEN: a reservoir whose
  state-space is a covering space of its configuration space.

### Search 2 — arXiv "belt trick" (via export.arxiv.org curl after WebFetch 429/503)

- arXiv:1001.1778 — "Understanding Quaternions and the Dirac Belt Trick" (2010): the
  formal home of the operator's scene math — SU(2)→SO(3) double cover, 720° identity.
- arXiv:2107.01681 — "The spinor linkage — a mechanical implementation of the plate
  trick" (2021). A MECHANICAL DEVICE that implements the plate trick. Closest published
  ancestor to "smallest artifact" in the mechanism class.
- arXiv:2303.15215 — "The spinorial ball: a macroscopic object of spin-1/2" (2023).
  Macroscopic spin-1/2 behavior built as an object.
- arXiv:2006.16311 — "Controlled creation of a singular spinor vortex by circumventing
  the Dirac belt trick" (2020, BEC): "spinor" is operational physics in a quantum fluid —
  the closest thing to the Dirac layer's "fluid" reading.
- arXiv:1807.01867 — "Rogue breather modes: topological sectors and the 'belt-trick' in a
  1D ferromagnetic spin chain" (2018): belt-trick homotopy sectors realized in a magnetic
  chain.

### Search 3 — 4π-periodic Josephson / Majorana wires (the "wire" class)

- The 4π fractional Josephson effect (Kitaev 2001 prediction; Rokhinson et al. PRL 2012
  InSb nanowire; Wiedenmann et al. Nat. Commun. 2016 NbN–InSb) is the ONLY mature
  published case of a WIRE whose supercurrent returns to identity at 720° (4π), not 360°
  (2π) — i.e., a literal double-period device.
- HONEST CAVEAT (2021–2024 literature): missing odd Shapiro steps are NOT unique evidence
  of 4π periodicity — topologically trivial overdamped junctions reproduce the signature
  (Davesne et al. Nat. Commun. 2021; PRB 110, 184511 (2024); SciPost 2021-2022 model
  papers). Cryogenic, contested, not printable. Cited as proof-of-principle class only.

### Search 4 — hyphae/slime-mold network computation baseline (the "hyphae" class)

- Tero et al., Science 2010, "Rules for Biologically Inspired Adaptive Network Design" —
  Physarum recreates the Tokyo rail network; transport-network computation baseline.
- Adamatzky et al., Phil. Trans. R. Soc. A 2015, "Slime mould processors, logic gates and
  sensors" — computation via network TOPOLOGY of the organism itself.
- Whiting et al., Sci. Rep. 2016, "Towards a Physarum learning chip."
- Fungal (hyphal) computing: Adamatzky's fungal-computing program (electrical spiking in
  mycelium as signal; matches the G-D receipt's myco-memory ladder).
- KEY GAP for G-F: every published bio-network computation uses planar/orientable
  substrates. NO published work grows or prints a non-orientable / double-cover topology
  (Möbius loop, twisted 3D lattice) and asks whether traversal parity changes behavior.
  UNPROVEN and — as far as this search shows — UNEXPLORED.

### Search 5 — Möbius topology in photonic/acoustic channels (the STRONGEST bridge found)

- "Möbius" microring resonator, Appl. Phys. Lett. 114, 101106 (2019): light must
  circulate **TWO full loops** before returning to its initial state; enables
  polarization-mode conversion. A literal 720°-symmetric CHANNEL, published and
  fabricated.
- "Topological resonances in a Möbius ring resonator," Communications Physics 6, 84
  (2023): experimental twisted optical-fiber-loop resonator; resonance wavelengths
  shifted vs an ordinary ring — the non-orientable loop has a MEASURABLY DIFFERENT
  spectrum. Berry phase per loop is the mechanism (Optics & Photonics News, Jan 2023).
- "Topological edge states on the acoustic Möbius band" (Materials Today Physics, 2023):
  edge channels propagating on a non-orientable lattice — topological channels on a
  double cover.
- arXiv:2312.04582 — "Split ring versus Möbius strip: topology and curvature effects"
  (2023).
- MEANING for G-F: in any wave-carrying channel (light, sound, spin waves) a
  non-orientable / double-cover channel topology is REAL physics with measurable
  consequences (spectral doubling, polarization swap, Berry phase). The missing
  transfers are to BULK FLUID (Navier–Stokes carries dye, not phase) and to LIVING
  HYPHAE — both unexplored.

### Search 6 — double cover / holonomy as COMPUTATION on graphs (Q1's formal home)

- arXiv:2209.07901 — gauge-twisted vs topologically twisted Gaussian free fields: builds
  the **double cover of a discrete graph induced by the gauge field**. The construction
  "network → its double cover" exists as formal math.
- arXiv:2509.10536 (2025) — "Contextuality, Holonomy and Discrete Fiber Bundles": cycles
  in a graph = closed paths; composite weights = **holonomies = failure of global
  triviality**; SU(2) as double cover of SO(3) inside a discrete-bundle framework.
- Cohen et al., ICML 2019, "Gauge Equivariant Convolutional Networks and the Icosahedral
  CNN" — gauge structure on graph neighborhoods as a computational resource; plus 2025
  fiber-bundle-learning preprints (preprints.org 202511.2221 — PRE-PRINT, low trust).
- Conclusion: the MATH of "two channel families, identity only after both traversed" is
  Z2-holonomy over a double cover, and it is established. What nobody has built is a
  PHYSICAL transport network (fluid or hyphal) whose holonomy group is nontrivial by
  construction and whose computation exploits it.

## Analysis — answers to the socratic tease

### Q1. Real computational meaning of orientability/double-cover in a transport network?

YES — with a precise sense, and one honest distinction to keep.

- The REAL sense: give every loop of the network a holonomy in Z2 (odd laps flip the
  channel family A↔B, even laps restore). That is a discrete gauge bundle over the
  network; the construction is published math (arXiv:2209.07901 double cover of a graph
  from a gauge field; arXiv:2509.10536 cycle holonomy). Computational meanings, all
  published in at least one medium:
  - WIRE: odd/even inverter ring — odd loop oscillates (identity only in phase after two
    rounds), even loop is bistable memory. Parity = the network's holonomy bit.
    Textbook. Also π-junction SQUIDs (half-flux-quantum ground state) — published since
    the d-wave experiments.
  - PHOTONICS: the Möbius microring (APL 2019) — two loops per identity, supermodes and
    spectra measurably different from an orientable ring; Berry phase per loop
    (Commun. Phys. 2023).
  - SUPERCONDUCTING: 4π Josephson (wire needs 720° of phase for identity) — mature but
    contested and cryogenic.
- The DISTINCTION to keep (flag it every time): the belt trick is homotopy of PATHS IN
  ROTATION SPACE, π1(SO(3)) = Z2 — about a body that rotates while tethered. A channel
  network cannot rotate; what it can carry is holonomy PER LOOP. Both are Z2, and the
  Möbius microring realizes the spinor ROTATION LAW (state → −state after one loop,
  identity after two) as a propagation law. That is a legitimate transfer; calling a
  fluid channel "spinorial" without that law is metaphor. UNPROVEN remains: any fluidic
  or hyphal artifact that carries a true per-loop phase/sign holonomy.

### Q2. Published work connecting spinor/covering structure to physical networks or RC?

- Spintronic reservoir computing exists (spin waves, skyrmions) but uses magnetization
  DYNAMICS, not the double cover, as the resource. No published "covering-space
  reservoir." UNPROVEN/OPEN.
- Wave channels on non-orientable topology: Möbius microring resonator (APL 2019),
  topological resonances in a Möbius fiber loop (Commun. Phys. 2023), acoustic Möbius
  band edge states (2023). These are the closest published "720°-symmetric channels."
- Double covers of networks as formal objects: gauge-induced graph double cover
  (arXiv:2209.07901); holonomy on graph cycles (arXiv:2509.10536); gauge-equivariant
  GNNs (Cohen ICML 2019).
- Mechanical spin-1/2 objects: spinor linkage (arXiv:2107.01681), spinorial ball
  (arXiv:2303.15215). Macroscopic belt-trick math is buildable and published.
- Quantum fluids: singular spinor vortex in a BEC (arXiv:2006.16311). Belt-trick sectors
  in a ferromagnetic chain (arXiv:1807.01867).

### Q3. The smallest printable artifact that distinguishes 360° from 720°

Primary spec (FLOW — the Dirac layer's water reading): **the Möbius parity loop.**
- Body: one closed loop of two parallel channels (A, B) in a printed or tubing ribbon,
  closed through a HALF TWIST (180°) so the ribbon is non-orientable. Control: identical
  loop closed with NO twist (orientable cylinder).
- Drive: two dye pulses injected simultaneously into A and B at the inlet junction;
  laminar flow, no mixing required.
- Discriminator: at the SAME readout junction, after one lap the A-pulse arrives in B's
  port and vice versa (odd laps swap); after two laps both arrive home (identity only at
  two laps = 720° law). The orientable control returns both pulses home every lap.
- Cost/time: aquarium-tubing version <$5 and <1 hour (two colored lines, one half twist,
  zip ties); printed version: 2 channels × 2 mm, one print, $1 filament.
- What it proves: geometric transport on a double cover — dye swap per lap. What it does
  NOT prove: any quantum-like phase. Honest label: kinematics, not spinor physics.

Wire version ($0.10): two-channel parity pair — odd-inverter ring oscillator vs
even-inverter latch on one breadboard; the oscillator's period IS "identity after two
rounds." Behaviorally distinguishes one-loop-identity from two-loop-identity networks,
but abstracts away the geometry entirely.

Hyphae version (cube-3 lineage, UNPROVEN, exploratory): print the same two-track ribbon
in spent-oat substrate, inoculate one track, and ask whether traversal parity is visible
in colonization order or spiking statistics vs the orientable control. Timescale:
days–weeks. NOBODY has published this; treat as art-with-a-control until a parity
readout survives.

### The operator's diary math, mapped (July 18 entry → printed lattice)

- "Domain repetition for lattice representation" = quotient space: one cell + a group
  action stands for the infinite lattice. A printed lattice IS domain repetition made
  physical (unit cell repeated by the printer). Same machinery as the double cover, run
  in reverse: domain repetition projects down to a quotient; the spinor lattice lifts up
  to a cover. His two shader ideas were one group-action idea in both directions.
- "Lipschitz-bounded march" = sphere-tracing's bounded step = bounded propagation speed.
  In the lattice: flow fronts and hyphal tips advance with a bounded-rate rule; the
  front-march is the physical raymarcher.
- "720° untangle" = loop holonomy Z2: channel pairs that return to identity only after
  two laps (parity loop above). The belt trick itself (rotate the tethered body) stays
  in the mechanism class — spinor linkage / spinorial ball are its published builds.

## VERDICT (honest)

- REAL PHYSICS: double-cover channel topology in wave systems (photonics Möbius
  resonators; acoustic Möbius bands; 4π Josephson). The 720°-identity law has published,
  fabricated instantiations.
- REAL MATH: Z2 holonomy over a graph double cover — established, citable.
- ENGINEERING-GEOMETRY (novel but buildable): the Möbius parity loop for printed fluid
  channels — a dye-swap demo, not a phase demo. Nobody seems to have printed one for
  computation; the physics it demonstrates is classical geometry.
- METAPHOR (for now): any claim that the hyphal network or bulk-water Dirac layer
  COMPUTES differently on a non-orientable lattice. No mechanism carries per-loop phase
  in dye or hyphae; only geometry-swap and growth-order effects are on offer, and those
  are unmeasured.
- UNEXPLORED MATH/APPLIED (genuinely open, flagged as such): covering-space reservoirs —
  a reservoir whose state space double-covers its configuration space; and transport
  networks DESIGNED with nontrivial holonomy as the computational resource. Nothing
  published found in any substrate. UNPROVEN.

## Smallest artifact spec (final answer to Q3)

**Möbius parity loop** — two-channel half-twist ribbon loop + orientable control.
PASS = odd-lap port swap, even-lap restore, control never swaps. $5 / 1 hour in tubing;
1 print / $1 filament. First run planned under cube-3 staging (after cube-1's $31 rig).

## Citation list

Belt-trick / mechanical spinors:
1. arXiv:1001.1778 — Understanding Quaternions and the Dirac Belt Trick (2010).
2. arXiv:2107.01681 — The spinor linkage: a mechanical implementation of the plate trick (2021).
3. arXiv:2303.15215 — The spinorial ball: a macroscopic object of spin-1/2 (2023).
4. arXiv:2006.16311 — Controlled creation of a singular spinor vortex by circumventing the Dirac belt trick (2020).
5. arXiv:1807.01867 — Rogue breather modes, topological sectors and the belt-trick in a 1D ferromagnetic spin chain (2018).

Double-cover channels (waves):
6. "Möbius" microring resonator — Appl. Phys. Lett. 114, 101106 (2019). https://pubs.aip.org/aip/apl/article/114/10/101106/36781/
7. Topological resonances in a Möbius ring resonator — Communications Physics 6, 84 (2023).
8. Topological edge states on the acoustic Möbius band — Materials Today Physics (2023). https://www.sciencedirect.com/science/article/pii/S2211379723001158
9. arXiv:2312.04582 — Split ring versus Möbius strip: topology and curvature effects (2023).
10. Optics & Photonics News (Jan 2023) — Optical Möbius strips yield new secrets (Berry phase framing).

Holonomy / double cover on graphs (math):
11. arXiv:2209.07901 — gauge-twisted vs topologically twisted GFF (graph double cover from a gauge field).
12. arXiv:2509.10536 — Contextuality, Holonomy and Discrete Fiber Bundles (2025).
13. Cohen et al. — Gauge Equivariant Convolutional Networks and the Icosahedral CNN, ICML 2019.
14. Nakahara — Geometry, Topology and Physics (canonical text: covering spaces, holonomy).

Wire-class double-period devices:
15. Kitaev — Unpaired Majorana fermions in quantum wires, Phys.-Usp. 44, 131 (2001) [4π prediction].
16. Rokhinson, Liu, Furdyna — PRL 109, 266402 (2012) [fractional ac Josephson, InSb].
17. Wiedenmann et al. — Nat. Commun. 7, 10303 (2016) [4π-periodic Josephson, NbN–InSb].
18. Davesne et al. — Nat. Commun. (2021) + PRB 110, 184511 (2024) [CAVEAT: missing odd Shapiro steps are not unique evidence].

Reservoir computing baselines:
19. Tanaka et al. — Recent advances in physical reservoir computing, Neural Netw. 115 (2019).
20. Spintronic reservoir computing with interpretable nonlinearity — Phys. Rev. Research 7, 013310 (2025).
21. Fast physical reservoir computing with nonlinear spin wave interference — Neuromorph. Comput. Eng. 1, 024002 (2024).

Bio-network computation baselines (hyphae class):
22. Tero et al. — Rules for Biologically Inspired Adaptive Network Design, Science 327 (2010).
23. Adamatzky et al. — Slime mould processors, logic gates and sensors, Phil. Trans. R. Soc. A 373 (2015).
24. Whiting et al. — Towards a Physarum learning chip, Sci. Rep. 6, 19948 (2016).

Canonical spinor/phase anchors (from knowledge, standard): Aharonov & Bohm (1959);
Kane & Mele PRL 95, 226801 (2005) [π Berry phase, helical two-channel pair];
Penrose (1971) spin networks. NOT re-verified this session.

Search-method note: WebSearch/WebFetch were heavily rate-limited (429s); verified hits
came via export.arxiv.org (curl) and WebSearch summaries with links. Items 1–14, 19–23
seen with title+venue this session; canonical items 15–18 partially re-verified (names/
venues from search summaries); item 24 and canonical anchors not re-verified this
session — trust bytes before filing any of this into a paper trail.
