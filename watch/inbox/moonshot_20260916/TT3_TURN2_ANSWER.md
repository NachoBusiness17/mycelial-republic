# TT3 Turn 2 — Union Alpha (verbatim)

**Prompt:** Translate a pre-registered falsifier into a two-state-vector-style description: final boundary condition constraining the initial experiment. Where does the math allow it and where does it become poetry?

---

**Translate it first. Then break it.**

## 1. The formal translation

Let the experiment have:

- initial preparation \(\rho_i\) (or pure state \(|\psi\rangle\));
- forward evolution \(U\);
- final measurement with outcome space \(\mathcal{Y}\);
- a pre-registered falsifier \(F \subseteq \mathcal{Y}\).

The falsifier is a **condition on outcomes**: if \(y \in F\), the hypothesis is refuted. It is fixed before the experiment.

In two-state-vector language, for a specific final outcome \(y_0\), define the backward-evolving state
\[
\langle \phi| = \langle y_0| U.
\]
The system is then described by the two-state vector
\[
\langle \phi | \psi \rangle.
\]
For an observable \(A\) at an intermediate time, the weak value is
\[
A_w = \frac{\langle \phi| U A |\psi\rangle}{\langle \phi| U |\psi\rangle}.
\]
Conditional probabilities for intermediate outcomes are computed from both boundaries.

If the falsifier is a **set** \(F\), it is not a single state. It is a projection
\[
\Pi_F = \sum_{y \in F} |y\rangle\langle y|.
\]
The two-boundary probability for \(y \in F\) is
\[
p(y \mid \psi, F)
=
\frac{\|\Pi_y U |\psi\rangle\|^2}
{\|\Pi_F U |\psi\rangle\|^2}.
\]
This is exactly post-selection. The final boundary is an **effect**, not a pure backward-evolving state, unless \(F\) is a singleton.

So the math allows a TSVF-style description **if and only if** you specify the quantum system, the measurement, and the post-selection. The falsifier becomes a projector onto a subspace of final outcomes.

## 2. Where the math allows it

- **Post-selection.** You can condition on the subensemble of runs satisfying \(F\). The two-state formalism then gives a time-symmetric description of that subensemble.
- **Retrodiction.** Given \(F\), you can update your probability distribution over initial states:
  \[
  p(\psi_i \mid F) \propto p(F \mid \psi_i)\, p(\psi_i).
  \]
  This is Bayesian inference. The final condition constrains which initial states are plausible.
- **Weak values.** In the surviving subensemble, intermediate observables can have anomalous weak values. That is real quantum mechanics.
- **Conditional probabilities.** The final boundary renormalizes the statistics. It does not change the forward evolution.

All of this is standard. It is conditional probability dressed in time-symmetric language.

## 3. Where it becomes poetry

- **The falsifier is not a quantum state.** It is a classical logical condition. It has no phase, no coherence, no interference. It cannot be weakly measured unless you embed it in a quantum measurement. A set of outcomes is not a state vector.
- **The final boundary does not constrain the initial experiment causally.** In TSVF, the initial state \(|\psi\rangle\) is fixed. The final boundary does not change it. The experiment runs the same way. Only the analysis changes. If you say the final condition “constrains the initial experiment,” you mean it constrains what you can say about the initial experiment given the outcome. That is retrodiction, not causation.
- **Pre-registration is a forward-causal device.** Its whole point is to prevent the outcome from influencing the falsifier. It blocks a forward causal arrow. It does not add a backward one. Calling it a “final boundary condition” is a formal analogy, not a physical mechanism.
- **The “backward-evolving state” is a boundary condition, not a signal.** In TSVF, it is not an additional physical entity that travels backward. It is part of the quantum formalism. The pre-registered falsifier is not even part of the quantum formalism unless you define a measurement that post-selects on \(F\).
- **Category error for classical experiments.** If the experiment is classical, there is no TSVF. There is just conditional probability. Calling it TSVF is a category error.

## 4. The brutal distinction

| Claim | Status |
|---|---|
| Falsifier as a projector on final outcomes | **Real math** |
| Post-selection on \(F\) and conditional probabilities | **Real math** |
| Retrodictive inference about initial states given \(F\) | **Real math** |
| Weak values in the surviving subensemble | **Real physics** |
| Falsifier as a physical backward-evolving state | **Poetry** |
| Final boundary changing the initial experiment | **Poetry** |
| Pre-registration as retrocausal steering | **Poetry** |
| Pre-registration as a commitment device with forward-causal effects | **Real engineering** |

The math allows a two-state-vector description of a **post-selected ensemble**. It does not allow the final boundary to reach backward and alter the initial preparation. The falsifier constrains the **analysis**, not the **experiment**. The real causal effect of pre-registration is forward: it changes incentives, prevents post-hoc adjustment, and disciplines inference. The retrospective step is bookkeeping—useful, rigorous bookkeeping—but not retrocausation.
