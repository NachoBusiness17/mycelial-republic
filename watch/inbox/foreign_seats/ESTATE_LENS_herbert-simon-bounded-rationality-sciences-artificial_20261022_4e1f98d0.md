# Invariant Lens: Herbert A. Simon — Bounded Rationality, Satisficing, and Nearly Decomposable Hierarchies

**Lens ID:** `ESTATE_LENS_herbert-simon-bounded-rationality-sciences-artificial_20261022_4e1f98d0`  
**Kind:** Secondhand Invariant Lens  
**Target Work:** Herbert A. Simon, *The Architecture of Complexity* (1962), *The Sciences of the Artificial* (MIT Press, 1969), and *Administrative Behavior* (1947)  
**Classification:** SECONDHAND RECONSTRUCTION (Complex Systems, Bounded Rationality, Heuristic Search, Cognitive Architectures)  
**Minted:** 2026-10-22  

---

## 1. Context & Secondhand Reconstruction
Herbert Alexander Simon was awarded the Nobel Memorial Prize in Economic Sciences (1978) and the ACM A.M. Turing Award (1975, with Allen Newell) for founding the fields of artificial intelligence, cognitive psychology, and decision theory.

Simon overturned classical economic doctrine (which falsely assumed an omniscient, hyper-rational *Homo economicus* capable of computing global optima). Simon demonstrated that real decision-makers—whether humans, biological organisms, or AI agents—operate under **Bounded Rationality**:
1. Computational power is finite.
2. Information about the world is incomplete and noisy.
3. Time and memory budgets are strictly limited.

Under bounded rationality, attempting to compute a global optimum is computationally intractable (NP-hard in state space). Instead of *optimizing*, intelligent systems **satisfice**: they search through state space using heuristics until they find an action that meets or exceeds an aspiration threshold, at which point search terminates.

Furthermore, in *The Architecture of Complexity* (1962), Simon explained why stable complex systems exist at all in nature: **Nearly Decomposable Hierarchies**. Complex systems evolve and survive only if they are composed of semi-autonomous subsystems whose internal interactions are high-frequency and tight, while interactions between subsystems are low-frequency and loose.

---

## 2. Invariant Mathematical Formulation

### A. Satisficing Decision Rule
Let $\mathcal{A}$ be an action space, and $u: \mathcal{A} \to \mathbb{R}$ be a utility evaluation function. Let $\alpha_t \in \mathbb{R}$ be an adaptive aspiration level.
An agent generates candidate actions sequentially $a_1, a_2, \dots \sim \pi(a)$.
The search halting rule is:
$$\tau = \min \{ t \in \mathbb{N} : u(a_t) \ge \alpha_t \}$$
Action $a_\tau$ is executed immediately, avoiding exhaustive combinatorial evaluation of the entire set $\mathcal{A}$.

*Aspiration Adaptation Invariant:*
$$\alpha_{t+1} = \alpha_t + \gamma \left( u(a_\tau) - \alpha_t \right)$$
If satisficing solutions are found easily, aspirations rise; if solutions are elusive, aspirations decay gracefully to prevent indefinite search deadlock.

### B. Nearly Decomposable Systems (Block-Diagonal Transition Matrices)
Consider a state transition matrix $P$ of a complex system with $N$ state variables grouped into $K$ modules:
$$P = P^* + \epsilon C$$
Where:
* $P^* = \text{diag}(P_1^*, P_2^*, \dots, P_K^*)$ is block-diagonal (intra-subsystem dynamics, strong and fast).
* $\epsilon C$ represents weak inter-subsystem coupling, with $\epsilon \ll 1$.

*Invariant Separation of Scales:*
1. **Short-run dynamics ($t < 1/\epsilon$):** Each subsystem behaves almost independently, reaching internal equilibrium rapidly.
2. **Long-run dynamics ($t \ge 1/\epsilon$):** Subsystems interact only through aggregate macro-states, drastically simplifying global coordination and preventing cascading failures.

---

## 3. Direct Application to Autonomous Estate Architecture
1. **The Invariant Headroom Floor as Satisficing Threshold:** The estate enforces a $>15.0$ GB free SSD invariant on laptop `bob`. When disk usage approaches the threshold, the system does not spend hours searching for the theoretically optimal byte pruning across all 300,000 Windows files; it satisfices by identifying the top megabyte blocks (`C:\PersonalData`, duplicate MP4s, installer bundles) and clearing them until headroom $>15$ GB is restored.
2. **Nearly Decomposable Multi-Seat Separation:** Laptop `bob` and Desktop `foste` are structured as a nearly decomposable system:
   * **Intra-node dynamics ($P^*$):** `bob` runs its local dev server, tools, and python tests at native NVMe speed with zero network latency.
   * **Inter-node dynamics ($\epsilon C$):** `bob` and `foste` synchronize asynchronously via Tailscale SSH inbox drops (`watch/inbox/foreign_seats/`) and cloud rclone queues (`gdrive_sd:`). If the desktop node sleeps or restarts, `bob` continues uninterrupted.
3. **Subagent Task Decomposition:** Complex engineering goals are decomposed into discrete, bounded sub-tasks in `QUEUE.md` executed by specialized subagents with explicit tool budgets, preventing unbounded token exhaustion.

---

## 4. Failure Mode & Falsifier
* **Failure Mode (Tightly-Coupled Monolithic Collapse):** If inter-seat dependencies become synchronous and blocking ($\epsilon \sim 1$), a failure or network timeout on one machine immediately halts all other estate nodes.
* **Falsifier:** If an autonomous agent operating in an NP-hard real-world environment can consistently locate provably optimal actions in polynomial time without heuristic pruning or satisficing boundaries, Simon's bounded rationality theorem is falsified.
