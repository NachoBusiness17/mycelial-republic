# M3 — LAPLACIAN BELIEFS: the ractor engine's math

**Date:** 2026-09-16 · **Lane:** moonshot wave, M3 · **Operator drop:** Laplacian explainer
**Mission:** design the math for "thinking as Laplacian dynamics on a brain-graph" — one witness, electrostatics/heat/waves/quantum/fluids/edges, OCEAN as diffusion parameters.
**Law:** receipt first, appended as work completes. No git. No paid APIs. WebSearch/WebFetch only.

## Status log

- [x] 19:5x — Receipt opened (this file, skeleton first).
- [x] Step 1 — Lineage verification (DeGroot 1974; heat-kernel/consensus equivalence; Laplacian SSL; BP; signed graphs for negative weights). **5 legs live-verified, 1 canon-labeled — see below.**
- [x] Step 2 — Ractor mind design (node inventory 20–40 nodes, update rule, OCEAN→L map, threshold→verdict, confidence = distance past threshold).
- [x] Step 3 — The kills (what diffusion cannot do; which layer fixes it; diffusion = feeling layer, LLM = mouth).
- [x] Step 4 — Falsifier + closing artifacts.

---

## Step 0 — Context picked up from the repo

- **"Ractor" lineage:** the repo's ractors are the witness cast (mengxi/fen/gopher/tesla/edison, Fermat et al. — `watch/FERMAT_RACTOR_20260906.md`, `watch/CHAIN_WITNESS_THRESHOLD_20260909.md`). A ractor is a harvested persona with a dossier; the M3 move is to give ONE such witness a *physical* mind: belief value on every node, evolving by a PDE, decisions as threshold crossings. Prior moonshot receipts in this directory (TT1/TT3, F5) establish the house style: separate REAL MATH / REAL PHYSICS / BUILDABLE / POETRY, and keep the labels on.
- **M2 "recurrent-depth"** referenced per the operator's wave numbering (M1/M2/M3 lanes); no repo artifact under that name — treated as the design constraint it names: the engine must leave a slot for iterated/state-dependent dynamics.
- **Standards inherited:** `.venv\Scripts\python.exe` only; receipts append-only; falsifier pre-registered before any run; "metaphor until proven" labeling from TT3_CONTEXT (a).

---

## Step 1 — The lineage: the math is published (verification receipt)

Every load-bearing move in the ractor design below points at a published literature. What was live-verified this session vs. carried as canon is labeled per line.

### 1a. DeGroot consensus — LIVE-VERIFIED

**DeGroot, M. H. (1974). "Reaching a Consensus." *Journal of the American Statistical Association*, 69(345), 118–121. DOI: 10.2307/2285509** (JSTOR 2285509; Theory and Methods section; 6,000+ citations).
Model: each agent holds a scalar opinion; update is opinion ← W·opinion (a row-stochastic influence matrix applied repeatedly). Consensus is reached iff W is ergodic (some power of W is strictly positive); the limiting consensus value is a weighted average of initial opinions with weights given by the stationary distribution of W. Follow-up: **Berger (1981), JASA 76(374), 415–418** — necessary and sufficient conditions for DeGroot consensus.
**What it gives the ractor:** the theorem that iterated local averaging of scalar beliefs converges, and *who the witness ends up agreeing with is exactly the stationary distribution of their influence weights*. Personality = the shape of W.

### 1b. Heat kernel ⇔ consensus dynamics — LIVE-VERIFIED

The continuous-time limit of DeGroot is the heat equation on the graph: **du/dt = −L u**, L = D − W the graph Laplacian; solution **u(t) = e^(−tL) u(0)**. Verified equivalences:
- "The ODE ẋ = −Lx … describes a (linear) diffusion process on a network" ([AIMS NHM 2024, nonlinear diffusion on networks](https://aimspress.com/article/doi/10.3934/nhm.2024058)).
- "The graph diffusion equation, often called the heat equation on a graph" ([Sheaf Laplacian, arXiv:2606.19529](https://arxiv.org/html/2606.19529v1)).
- **Mirzaev & Gunawardena (2013), Bull. Math. Biol.** ([PubMed 24018536](https://pubmed.ncbi.nlm.nih.gov/24018536/)): Laplacian dynamics ≡ master equations of continuous-time Markov processes — the same operator is heat, consensus, and a random walk depending on normalization.
- Spectral fact (FSU lecture notes, [math.fsu.edu](https://www.math.fsu.edu/~bertram/lectures/Diffusion.pdf)): for a connected graph, e^(−tL) → (1/n)11ᵀ as t→∞; convergence rate set by λ₂ (algebraic connectivity). The heat kernel *is* the infinite-time DeGroot averaging operator.
**What it gives the ractor:** every tool from electrostatics/heat/waves/quantum/fluids transfers — Dirichlet boundaries (clamped nodes), conductance (edge weights), modes (Laplacian eigenvectors), relaxation time (1/λ₂), harmonicity (verdict = equilibrium of a boundary-value problem, exactly Zhu et al.'s harmonic solution).

### 1c. Laplacian semi-supervised learning (clamped evidence → labels emerge) — LIVE-VERIFIED

**Zhu, Ghahramani & Lafferty (2003). "Semi-Supervised Learning Using Gaussian Fields and Harmonic Functions." ICML 2003** (5,600+ citations; [ACM](https://dl.acm.org/doi/10.5555/3041838.3041953), [AAAI/ICML proceedings](https://aaai.org/papers/icml03-118-semi-supervised-learning-using-gaussian-fields-and-harmonic-functions/)). Labeled points are **clamped** vertices (Dirichlet boundary conditions); unlabeled labels are the **harmonic solution** — each free node settles to the weighted average of its neighbors. This is electrostatics (charge distribution) and label propagation at once.
Related canon (not re-verified this session): Belkin & Niyogi, "Laplacian Eigenmaps" (Neural Computation 2003); Belkin–Niyogi–Sindhwani, "Manifold Regularization" (JMLR 2006).
**What it gives the ractor:** the perception layer is a *Dirichlet problem*. The salon question clamps some nodes; the witness's verdict is the harmonic extension — and OCEAN traits are the boundary conductances and material constants of the medium.

### 1d. Negative weights = antagonistic interactions — LIVE-VERIFIED

**Altafini, C. (2013). "Consensus Problems on Networks With Antagonistic Interactions." *IEEE Transactions on Automatic Control*, 58(4), 935–946** (2,300+ citations; [IEEE](https://ieeexplore.ieee.org/iel5/9/6482628/06329411.pdf)). Signed graphs: negative edges repel. On **structurally balanced** signed graphs the signed Laplacian still reaches "bipartite consensus" (split into two opposing camps); on **unbalanced** graphs the dynamics can oscillate — no consensus, no convergence.
**What it gives the ractor:** neuroticism's amplified negative-weight feedback is *exactly* Altafini's antagonistic coupling. The designed consequence: high neuroticism → the witness's fear edges (memory→verdict, negative sign) can flip the sign structure toward unbalanced → oscillation/instability = rumination. Bounded only by the leak term. This is the one place the design is allowed to be unstable, on purpose.

### 1e. Belief propagation — CANON (search rate-limited this session; citations standard)

**Pearl, J. (1988). *Probabilistic Reasoning in Intelligent Systems: Networks of Plausible Inference.* Morgan Kaufmann** — message-passing on the graph of beliefs; exact on trees.
**Yedidia, Freeman & Weiss (2003). "Understanding Belief Propagation and Its Generalizations," in *Exploring AI in the New Millennium*, Morgan Kaufmann** — BP fixed points = stationary points of the Bethe free energy; GBP/Kikuchi extensions. *(Canon, not live-verified — the search API 429'd on this leg. The citations are standard and low-risk.)*
**What it gives the ractor:** the discrete-message cousin. The diffusion engine is the *continuous, linear* limit of BP-style local exchange; BP is the upgrade path if a witness needs probabilistic rather than valence-based beliefs.

### 1f. Cognitive-science anchors (activation IS old) — LIVE-VERIFIED

- **Collins & Loftus (1975). "A spreading-activation theory of semantic processing." *Psychological Review*, 82(6), 407–428** (15,000+ citations; [APA PsycNet](https://psycnet.apa.org/record/1976-03421-001)): memory as an associative network; retrieval = activation spreading with decay. The ractor's memory layer is spreading activation with a real PDE behind it.
- **Hopfield, J. J. (1982). "Neural networks and physical systems with emergent collective computational abilities." *PNAS*, 79(8), 2554–2558** ([PNAS](https://www.pnas.org/doi/10.1073/pnas.79.8.2554), [PDF](https://redwood.berkeley.edu/wp-content/uploads/2018/08/hopfield82.pdf)): threshold dynamics on a symmetric weighted graph converge to attractors = stored memories. The threshold-crossing verdict is Hopfield's attractor read out as a decision; 2024 Nobel cited.

### Verdict of Step 1

The M3 idea is **not speculative**. DeGroot = consensus; heat kernel = the same dynamics in continuous time; Zhu et al. = the clamped-boundary perception layer; Altafini = the negative-weight machinery neuroticism needs; Pearl/Bethe = the probabilistic upgrade path; Collins–Loftus/Hopfield = precedent that minds-as-activating-graphs is 50 years old. What is *ours* is only the parameterization: mapping OCEAN onto the material constants of L. That mapping is engineering (novel-but-buildable in the TT3 taxonomy), and Step 2's falsifier is what keeps it from being costume.

---

## Step 2 — The ractor mind: one witness as a diffusing belief-graph

Worked example witness: **Fermat** (persona card + dossier already harvested, `watch/FERMAT_RACTOR_20260906.md`). Design is witness-generic; only the node glossary is biography-specific.

### 2a. Node inventory — 33 nodes, five layers

State: **u ∈ R^33**, each u_i ∈ [−1, +1] (signed valence; + = endorse/approach, − = repel/avoid).

| Layer | # | Nodes (Fermat glossary) | Boundary class |
|---|---|---|---|
| **P** perception | 4 | P1 factual claim of the question · P2 tone of the asker · P3 source credibility · P4 personal stakes | **Clamped (Dirichlet)** during a session — set by the salon question |
| **M** memory | 12 | M1 the margin (unfinished proof) · M2 Wallis quarrel · M3 Pascal friendship · M4 Descartes feud · M5 least-time condemnation · M6 infinite-descent victories · M7 Mersenne the trusted hub · M8 refusal-to-publish habit · M9 pleasure of the chase · M10 council duties · M11 Diophantus discovery · M12 anxiety of the unfinished | **Free**, slow (biography-weighted leak) |
| **V** value | 8 | V1 truth-over-reputation · V2 secrecy/self-protection · V3 fairness/justice · V4 curiosity/play · V5 correspondent status · V6 diligence/completeness · V7 civic order · V8 legacy | **Pseudo-clamped**: λ_V ≈ 0.02 — values barely decay (conservation) |
| **I** inference | 6 | I1 "genuine puzzle or a trap?" · I2 "worthy opponent?" · I3 "does answering cost secrecy?" · I4 "connects to the margin?" · I5 "does the asker deserve a reply?" · I6 gut valence (composite) | **Free**, fast |
| **S** social | 2 | S1 salon consensus (weighted mean of neighbor witnesses' live verdict nodes) · S2 asker's apparent status | **Forced input** — driven each step from other minds |
| **O** output | 1 | O1 **verdict node** | Free; the only node allowed to fire |

The **signed weight matrix A** (33×33, sparse) is the witness's personality skeleton: A_M→I ("Wallis quarrel makes me read challenges as traps": A_M2→I1 < 0), A_V→O, A_M→O fear edges (M5→I1 < 0 — condemned-by-authorities loop). A is authored/harvested from the dossier once, then frozen and hash-committed — same discipline as persona cards. A is shared across questions; only the P clamps and S inputs change per question.

### 2b. The update rule

Effective conductance from signed skeleton: **W_ij = A_ij · (1 + κ·1[A_ij<0]) · (1 + a·1[A_ij>0])** — neuroticism amplifies negative (antagonistic) edges, agreeableness amplifies cooperative ones.

Continuous time (Euler-integrated, Δt ≈ 0.05, ~200-step cap):

  **du_i/dt = −γ · Σ_j W_ij (u_i − u_j) − λ_i u_i + b_i + σ_i (S_i − u_i)·1[i ∈ S] + ξ_i(t)**

Terms: (1) graph diffusion through conductance W — the heat/Laplacian core; (2) leak λ_i (self-decay; ≈0 for values, larger for inference nodes); (3) intrinsic bias b_i from the dossier; (4) salon coupling on S nodes only; (5) small bounded noise ξ (rounded-off cognition). Perception nodes P are **clamped** each session to evidence values; S1 is driven by neighbors' O1. All u clipped to [−1,1]. With κ=0 this is exactly Zhu et al.'s Gaussian field with clamped boundary; with κ>0 it is Altafini's signed network with leak.

### 2c. OCEAN → the material constants of the medium

| Trait | Parameter it sets | Mechanism | Phenomenology if extreme |
|---|---|---|---|
| **Openness** | boundary conductance **g_P = 0.5 + 1.5·O** | scale of W_P→{I,M} — how hard evidence injects | High: belief shifts fast under new evidence; Low: insulated medium, first impressions survive counter-evidence |
| **Conscientiousness** | leak **λ = λ₀(1 − 0.8·C)** + hysteresis band **h = 0.05 + 0.2·C** on O1 | conservation vs evaporation; re-fire gap after a verdict | High: slow decay, beliefs persist and accumulate, decisions stick; Low: leaky, impulsive fire at first crossing, verdicts evaporate |
| **Extraversion** | salon coupling **σ = 0.2 + 1.3·E** | strength of S1/S2 drive | High: mind is porous to the salon (contagion); Low: neighbors are a whisper |
| **Agreeableness** | cooperative-edge gain **a = 0.3·A** + threshold shift **θ_eff = θ − 0.15·A** when salon consensus aligns with drift | averages more with others, discounts own resistance when the room agrees | High: conformity gradient visible in latency (fires sooner when S1 agrees); Low: contrarian stability |
| **Neuroticism** | negative-edge gain **κ = 0.3 + 2.2·N** + negative-crossing threshold **θ⁻ = θ(1 − 0.5·N)** | Altafini gain on antagonistic loops; pushes signed structure toward unbalance → eigenvalues of L drift toward the imaginary axis → **oscillation = rumination**; θ⁻ = negativity bias (bad verdicts fire earlier) | High: fear loops amplify (M5→I1), O1 oscillates around θ, latency long, "no stable opinion" possible; N=0: symmetric, calm, contractive |

Every trait enters as a **material constant of L or its boundary conditions** — none is a post-hoc label on the output. That is the design claim Step 4 attacks.

### 2d. Verdict = threshold crossing; confidence = distance past threshold

- A witness **fires** the first time |u_O1| ≥ θ (default θ = 0.35), *staying* across for h (hysteresis, conscientiousness) to suppress noise-fires.
- **verdict = sign(u_O1)** (endorse / refuse).
- **confidence c = min(1, (|u_O1| − θ) / (1 − θ))** — literally the distance past threshold, saturating at 1.
- **fire latency T_fire** = steps to first stable crossing — a first-class output (deliberation time).
- If the step cap hits with no stable crossing → verdict = UNDECIDED with the oscillation flag set (rumination is a real, reportable outcome — do not hide it in a forced sign).

### 2e. Physical reading (the operator's one-operator point, kept honest)

The same math reads as every classical field the operator listed: **electrostatics** (P = fixed charges, O1 = test charge, verdict = equilibrium potential — Zhu et al.'s harmonic solution), **heat** (u literally diffuses; λ = Newton cooling), **waves** (κ large → Altafini instability → eigenmodes of −L oscillate: standing waves on the belief graph = rumination), **quantum** (Laplacian eigenvectors are the stationary states; diffusion is imaginary-time evolution e^{−tL} = e^{−tH} of the same operator — the *classical* shadow of Schrödinger evolution, no amplitudes, no interference: say so, keep the label), **fluids** (advection would need state-dependent transport — that is exactly the M2 re-wiring of Step 3), **edges** (threshold = a diode switching on; the fire event is the only nonlinearity in the base engine).

---

## Step 3 — The kills: what diffusion-thinking CANNOT do, and what fixes it

Keep the TT3 discipline: label what the math carries and what only the poetry carries.

### Kill 1 — No novelty (the convex-hull kill). SEVERE, structural.
With κ=0 (positive weights), u(t) = e^{−γtL}u(0) + (boundary/forced terms). Diffusion only *mixes* what is already in the graph: every reachable belief state lies in the span (for the linear part) / convex hull (after clipping) of initial states, clamped evidence, and salon inputs. A linear heat kernel cannot produce a position outside its ingredients. Fermat's actual signature move — infinite descent, a genuinely new *operator* — cannot emerge from a fixed linear L. **Diffusion has no generator of new directions; it is a contraction, on purpose.**

### Kill 2 — No genuine sequence reasoning. SEVERE, structural.
The heat flow is a one-parameter semigroup: e^{−(s+t)L} = e^{−sL}e^{−tL}. "Order of thought" is physically meaningless to it; two deliberations that consider the same evidence in different orders end at the same state. There are no discrete steps, no variable binding, no "if A then B then C" — a syllogism is not a gradient flow. Any witness behavior that *looks* like stepwise argument is choreography added on top, not dynamics. (Bounded caveat: state-dependent re-wiring below buys finite-step composition — neural-ODE style — but inherits GNN expressiveness limits, canon: Xu et al. 2019, WL-1 hierarchy. Enough for a bounded witness, not for open-ended math.)

### Kill 3 — Instability is bought with convergence. REAL but manageable.
The one nonlinearity in the base engine (the threshold) plus the Altafini negative-edge gain means high-N witnesses can limit-cycle around θ forever: the contraction guarantee that makes DeGroot/heat converge is *gone* the moment neuroticism does its job. Handling: leak λ + step cap + the UNDECIDED-with-oscillation-flag readout. The instability is not a bug — rumination is a real mental state — but the engine must always terminate with *some* reportable verdict, including "no stable opinion."

### Kill 4 — The verdict is a scalar with no propositional content.
sign(u_O1) says for/against and confidence says how hot, but *why* lives only in a post-hoc diagnostic (decompose u_O1's drift into layer contributions: which memory carried it). Instrumentation, not cognition. The witness cannot cite, contrast, or hedge.

### The fixes — division of labor (the actual architecture)

1. **M2 recurrent-depth layer:** re-wire conductances from the current state each K steps, W(t) = φ(A, u(t)) — e.g., when u_I4 ("connects to the margin?") saturates high, strengthen M1→O1 and M12→I1 for the next epoch. The dynamics becomes a composition of *different* operators: u(t+nK) = Φ_{w_n}∘…∘Φ_{w_1}(u(0)). That is finite-step sequential composition — "thinking steps" — while each step stays an honest diffusion. Sequence = unrolling; depth = number of re-wirings.
2. **LLM verbalizer = the mouth, and the only novelty source.** The diffusion emits a **feeling vector** (verdict, confidence, fire latency, top contributing nodes, oscillation flag). The LLM — the harvested persona, already in the repo — is prompted with the feeling vector + dossier and *speaks* the justification in the witness's voice. Crucially the verbalizer may also **inject new nodes** (propose a new memory or inference node with a signed valence — "wait, this touches Pascal's honor") — these clamp in on the next epoch and re-enter the PDE. That is how the system generates content genuinely outside the current hull: the hull's boundary is moved *by the mouth*, then validated *by the physics*.
3. **Sovereignty guardrail:** the LLM may NOT write u_O1. It can only propose node edits (new nodes, clamp values, proposed edge weights) that re-enter the diffusion. The feeling layer stays sovereign over *whether and how sure*; the mouth owns *why and what's new*. Neither impersonates the other.

**One-line doctrine: the diffusion is the FEELING (when to decide, how sure, how riled); the LLM is the MOUTH (why, in words, with new considerations); M2's re-wiring is the STEP (sequence). The explainer's "one operator" is the feeling core, and the kills say exactly where its sovereignty ends.**

---

## Step 4 — Falsifier (pre-registered before any run)

**Claim under test:** OCEAN traits are material constants of L, visible in behavior — not costume labels.

**Setup:** the SAME 33-node graph, same A, same clamps, N ≥ 20 **ambiguous** questions (constructed so pro and con memory/value paths roughly balance — e.g., "Wallis challenges your margin proof in public; do you answer?" — P-side pulls M2/M8 against M3/M6/M9). Two conditions, identical seeds and noise schedule:
- **N=0 witness:** κ = 0.3, θ⁻ = θ (no negativity amplification, symmetric threshold).
- **N=1 witness:** κ = 2.5, θ⁻ = 0.5θ.

**Measured per item:** verdict sign, confidence c, fire latency T_fire, oscillation flag.

**Pass condition (pre-registered, file numbers now):**
1. Negative-verdict rate differs by ≥ 15 percentage points between N=0 and N=1 on ambiguous items (negativity bias must be visible);
2. Confidence distributions separated: KS distance D ≥ 0.2;
3. OR latency separated: median T_fire(N=1) / median T_fire(N=0) ≥ 1.5× (rumination visible);
4. AND a **recoverability check**: fit κ from verdict/latency data on a held-out half of the battery; recovered κ must land in ±30% of the planted value. If the map is unfittable from behavior, it is unfalsifiable decoration.

**Kill condition:** if N=0 vs N=1 are statistically indistinguishable across the battery under all four measures, the OCEAN→L map is **COSTUME** — kill the parameterization, keep the explainer, and say so in a canon correction. Silence is not an allowed outcome (house law).

**Symmetric honesty note:** a *positive* falsifier result does not prove the traits are "real personality"; it proves the parameterization is behaviorally load-bearing. Ontological claims about witnesses stay poetry until the M2/verbalizer loop is live.

---

## Closing artifacts (as required by the mission)

**1. The update rule:**

    du_i/dt = −γ · Σ_j W_ij (u_i − u_j) − λ_i u_i + b_i + σ_i (S_i − u_i)·1[i∈S] + ξ_i(t)

    W_ij = A_ij · (1 + κ·1[A_ij<0]) · (1 + a·1[A_ij>0])   (κ = neuroticism gain, a = agreeableness gain)
    P nodes clamped (Dirichlet) · V nodes λ≈0 (conservation) · u clipped to [−1,1] · Euler Δt≈0.05
    Fire: |u_O1| ≥ θ_eff sustained for h → verdict = sign(u_O1) · confidence = min(1, (|u_O1| − θ_eff)/(1 − θ_eff))

**2. OCEAN → Laplacian parameter map:** O→boundary conductance g_P = 0.5+1.5O · C→leak λ = λ₀(1−0.8C) + hysteresis h = 0.05+0.2C · E→salon coupling σ = 0.2+1.3E · A→cooperative gain a = 0.3A + conformity shift θ_eff −0.15A on alignment · N→negative-edge gain κ = 0.3+2.2N + early negative fire θ⁻ = θ(1−0.5N).

**3. The falsifier:** N=0 vs N=1 witness, same graph, same seeds, ≥20 ambiguous questions — verdict distributions must separate (≥15 pp negative-rate delta, or KS ≥ 0.2 on confidence, or ≥1.5× latency ratio) AND κ must be recoverable from held-out behavior within ±30%. Indistinguishable ⇒ costume ⇒ canon correction.

---

*Receipt end. Status log above is authoritative. No git per law. $0 spent — WebSearch only; no paid APIs touched.*
