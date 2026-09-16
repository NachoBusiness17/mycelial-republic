# Receipt — X_MINE_FIGURES_20260916

Lane: background wave-lane (source hunt, WebSearch/WebFetch only, no git, no paid APIs)
Started: 2026-09-16
Mission: identify sources + mechanisms for three operator ore drops (X feed, sampling/geometry math) feeding the physical-computing research pack (§2 self-steal table, §4 falsifiers).

Status: COMPLETE (2026-09-16). Drop 1: exact paper unidentified — ranked candidates + full mechanism extracted. Drop 2: anchors identified, 3 instrument proposals extracted. Drop 3: tweet identified, mechanism captured. Verdict below.

---

## Drop 1 — two-panel 3D figure: double-well p(x) + separatrix; blurred r(x′) with merged wells + dashed funnel path, "Blur" arrow

Best source: **UNIDENTIFIED as an exact single paper** (confidence: LOW-MEDIUM on all candidates; ~20 distinct queries + arXiv API scans found no paper whose abstract matches a two-panel p(x)/r(x′) blur figure). Closest candidates, ranked:

1. **"Analytic Gaussian Convolution for Faster Molecular [Optimization and Sampling]"** (OpenReview T4giFEzWan, under review 2025-26; no arXiv twin found; OpenReview CAPTCHA-blocks bots). Confidence: MEDIUM-LOW that this is the source; HIGH that its mechanism is the one depicted. Quote from search capture: "analytical Gaussian convolution of the Lennard–Jones potential as a principled, scalable smoothing operator that accelerates both optimization and sampling." ULA on the blurred energy, then annealed back to the true potential. Canonical URL: https://openreview.net/forum?id=T4giFEzWan
2. **Theory anchor for the figure's mechanism:** Ge, Lee, Tong — "Simulated Tempering Langevin Monte Carlo II" (arXiv:1812.00793, NeurIPS): heat-kernel smoothing is the natural tempering; blur damps each Fourier mode by exp(−σ²|k|²/2), flattening barriers so the smoothed target has one basin, giving polynomial mixing on multimodal targets where local LMC needs exponential time. https://arxiv.org/pdf/1812.00793
3. **Choi & Zhang — "Improved annealing for sampling from multimodal distributions via landscape modification"** (arXiv:2111.02675): explicit landscape-modified Hamiltonian with reduced critical height; annealed penalty gives strong ergodicity + TV mixing bounds; polynomial mixing on Ising/Potts where Glauber is exponential. Illustrations are Ising/Potts (not the double-well figure). https://arxiv.org/abs/2111.02675
4. Family (mode-hopping via smoothed/tempered landscapes): ALPS arXiv:2112.12908; tempered Hamiltonian transitions arXiv:2111.06871; Neal's tempered transitions (1996, canonical prior art); "Restricted Spectral Gap Decomposition for Simulated Tempering" (NeurIPS 2025) — "flattened (high-temperature) landscape" framing; "Efficient Monte-Carlo sampling of metastable systems" arXiv:2512.16812 (flows for metastability).
5. Plausible alternative: the figure may be **original explanatory art from an X thread** (matplotlib-style custom render, "Blur" annotation) illustrating kernel/heat-kernel tempering, not a paper figure — the r(x′) notation (blurred density as a function of a new variable) is thread-typical, not paper-typical.

Exact mechanism (what blur does), 5 sentences:
1. Blur = convolution of the target with a Gaussian kernel: r_σ(x′) = (p ∗ φ_σ)(x′); in Fourier space this multiplies every frequency component by exp(−σ²|k|²/2), so the highest-curvature features — well walls and the saddle lip that define the separatrix — are erased first.
2. The barrier height between wells shrinks continuously with σ: smoothed critical height scales like O(σ²·local curvature) instead of ΔH, and once σ ≳ half the mode separation the two wells merge into a single basin with one spectral gap.
3. Metastability is thereby broken: a chain on r_σ mixes in polynomial (near-log-concave) time instead of needing an exponentially rare event to cross the separatrix — particles released anywhere funnel down the merged basin's gradient toward the dashed "highway" between the old mode locations.
4. The target is recovered by annealing σ → 0 along a schedule, with importance weights / self-normalized bias-corrected estimators (Choi & Zhang) or a tempering path; mixing-time guarantees come from spectral-gap decomposition along that path (Ge et al.; NeurIPS 2025 restricted decomposition).
5. Reading it as geometry (ties to Drop 2): blur lifts the negative-curvature neck at the saddle — the volume deficit the separatrix marks is exactly what the kernel pays to remove — so the Merge panel is a curvature-flattening operation, and the dashed path is the instanton/great-circle of the smoothed metric.

Feed to pack: §2 self-steal table — row "blur-as-tempering: convolve target, sample single-basin, anneal weights back"; directly implementable on substrates as thermal-noise softening of coupler landscapes (p-bits, annealers, thermodynamic units). §4 falsifiers — (i) merge onset σ* should track √(barrier curvature), measure hop-rate jump on hardware; (ii) polynomial-vs-exponential hop scaling across grid size; (iii) importance-weight variance blowup as σ→0 is the predicted failure mode (weights collapse to a few particles).

---

## Drop 2 — Ricci scalar curvature (R = g^μν R_μν) applied to loss/sampler geometry

Best source (confidence: HIGH for the explainer's technical anchor, MEDIUM for the exact X thread):
- **"On the curvature of the loss landscape"** — Pouplin, Roy, Singh, Arvanitidis — arXiv:2307.04719 (ICML-adjacent line; the canonical "Ricci scalar of a loss landscape, computed analytically" paper). URL: https://arxiv.org/abs/2307.04719
- **"Scalar Curvature and Functional Dimension in Neural Loss Landscapes"** (OpenReview gzTJPhMGzZ, 2025-26; OpenReview CAPTCHA-blocked to bots, treat as candidate twin).
- 2025–2026 cluster confirming this is an active X-visible research wave:
  - "Geometric Meta-Learning via Coupled Ricci Flow" — arXiv:2503.19867 (loss couples with scalar curvature R on the parameter manifold).
  - "Neural Feature Geometry Evolves as Discrete Ricci Flow" — arXiv:2509.22362 (local Ricci evolution coefficients).
  - "Loss-aware state space geometry for quantum variational algorithms" — arXiv:2604.05627 (Ricci scalar of VQA loss metric — directly physical-computing adjacent).
  - "The Geometry of Robustness..." — arXiv:2603.27139 (per-layer scalar-curvature score via EMAs).
  - "Neural Geometrodynamics, Complexity, and Plasticity" — PMC11154528 (Einstein–Hilbert-style metric/Ricci/Ricci-scalar for learning dynamics).
  - Debate context: "Are Flat Minima an Illusion?" (arXiv:2605.05209) vs "Flatness After All?" (arXiv:2506.17809).

What a scalar-curvature readout MEANS for a sampling landscape (mechanism, 4 sentences):
1. In Bakry–Émery / CD(K,N) theory, a lower Ricci bound on the (Fisher/Wasserstein) manifold of the target is exactly the condition that controls entropy decay: K > 0 ⇒ log-Sobolev and Poincaré constants ⇒ exponential mixing of Langevin dynamics; K ≤ 0 at "necks" between modes ⇒ exponential slowdown (metastability).
2. Scalar curvature R is the trace of that congestion: negative R regions are where geodesics diverge and probability mass must squeeze through a volume deficit — the Bishop–Gromov deficit is a direct "how much thinner is the mode-neck than it should be" meter.
3. So the readout for a sampler landscape: R (or its discrete proxy) at the saddle/neck between wells predicts the mixing-time blowup that the blurred r(x′) panel of Drop 1 removes — blur literally lifts negative-curvature necks.
4. On hardware substrates the same instrument reads coupler graphs: negative curvature edges = barrier funnel, positive = flat merge region.

Three concrete instrument proposals (for the pack's §4 falsifiers):
1. **Bakry–Émery κ-meter (Ricci proxy per state):** along sampler trajectories, log λ_min(−∇²V) (or the measured Hessian of log-density at chain states); CD(κ,∞) constant κ gives a lower bound on the Poincaré constant ⇒ falsifiable prediction: time-to-mode-hop scales like exp(−κ·d²). Cheap: Hessian-vector products only.
2. **Bishop–Gromov volume-deficit readout:** on a 2–3 D Fisher-metric slice of the posterior/energy surface, compare measured geodesic-ball volumes vs Euclidean model; deficit profile locates mode-neck congestion; falsifier: deficit peak at the separatrix should vanish under kernel blur, predicting the Merge.
3. **Ollivier-Ricci curvature of the transition graph:** for discrete substrates (p-bits, Ising machines, thermostat arrays), compute edge curvature n_{xy} from transition-kernel neighborhood overlap; curvature-bound ⇒ spectral gap bounds (Peres-type); falsifier: edges with most negative curvature are where annealing/blur schedules must be slowest; measure hop-rate asymmetry on hardware.

Feed to pack: §2 self-steal — "blur lifts negative-curvature necks" is the bridge between Drop 1 and Drop 2 (one mechanism, two instruments); §4 falsifiers — the three meters above are hardware-implementable (HVPs, slice Jacobians, transition-graph stats on p-bit arrays).

---

## Drop 3 — a³−b³ = (a−b)(a²+ab+b²) + https://x.com/Alex_Dukett/status/2099727643222417736

Tweet identified (via fxtwitter API, 2026-09-16):
- Author: @Alex_Dukett (bio "THE EVENT"; verified individual account).
- Text: "Plan B" — no paper link, no DOI. Sole attachment: photo 1962×2048 (https://pbs.twimg.com/media/HSO7KZPXoAAppx_.jpg?name=orig) — presumed the cubic-identity image the operator described. Posted Tue 2026-09-15 05:10:55 UTC; ~30.8K views, 406 likes, 9 quotes.
- Context captured: it is a standalone math-image post, not a paper thread; the "compression device" framing is the operator's read, not a quote-tweet chain I could recover.

Mechanism of the identity as a compression/steal gadget (3 sentences):
- a³−b³ = (a−b)(a²+ab+b²) is the n=3 case of xⁿ−yⁿ = (x−y)(x^(n-1)+x^(n-2)y+…+y^(n-1)): any difference of like powers factorizes into a *drive term* (the gap a−b) times a *strictly positive kernel* (the sum).
- Its workhorse use is telescoping finite differences: Σ_k[(k+1)³−k³] collapses exactly, so cubic growth audits reduce to endpoint bookkeeping — the identity converts a difference at the top into a contract over the path below it.
- In a physical-computing pack this is the same shape as a barrier decomposition: energy-gap = drive × positive spectral sum; worth stealing wherever logs of ratio-of-partition-functions or gap accounting appear.

Feed to pack: §2 self-steal table — row "factor-then-telescope: differences of like powers become drive×positive-kernel"; §4 falsifier — any claimed sublinear scaling of an energy-gap estimator must still pay the (a²+ab+b²)-shaped sum somewhere; if it doesn't, the gap is being hidden, not compressed.

---

### Adjacent finds worth keeping (2026-09-16 hunt)
- **"At the Top of the Mountain, the World can Look Boltzmann-Like: Sampling Dynamics of Noisy Double-Well Systems"** (arXiv:2602.04014, Hasan & Shukla) — p-bits/probabilistic computing: near the barrier top all smooth double wells collapse to the canonical quartic; noise+bias+curvature give a topologically robust tanh-like Boltzmann sampling response. Not the blur figure's source, but a directly relevant substrate paper for the pack.
- Ruled out as Drop 1 source: Smoothed Energy Guidance (2408.00760), MIED (2210.13400), mollified relative entropy VI (2406.04012), "mode merging"+"sampling" arXiv hits (1 unrelated 2012 superconductivity paper).

## Verdict — most stealable mechanism

**Drop 1 (blur-as-tempering) carries the most stealable mechanism.** Three reasons:
1. It is the only drop whose mechanism is a single reversible *operator* — Gaussian convolution of the landscape — that a physical substrate can execute in hardware (thermal noise softening / coupler de-sharpening), sample in the merged basin, and anneal back with importance weights. Blur in, hops out.
2. It composes with Drop 2 rather than competing with it: the blurred panel is precisely a negative-curvature-neck-lifting operation, so the Drop 2 curvature meters become the *control law* for the Drop 1 schedule (blur until the κ-meter reads nonnegative at every neck). One mechanism, two instruments, one falsifiable law: σ* ∝ √(barrier curvature).
3. It has a clean falsifier ladder for §4 (merge-onset σ* tracking, polynomial vs exponential hop scaling, weight-variance collapse as σ→0) that can be run on p-bit arrays today, whereas Drop 2's Ricci instruments need metric estimation and Drop 3's identity is a bookkeeping gadget, not a dynamics.

---

## Verdict — most stealable mechanism

(pending)
