# TT3 Turn 1 — Union Alpha (verbatim)

**Prompt:** A fleet keeps an append-only ledger and writes sealed predictions before experiments. In what rigorous sense is this retrocausal steering, and in what sense is it not? Be brutal about the distinction.

---

**It is not retrocausal steering in the physical or interventionist sense. It is prospective commitment followed by retrospective adjudication.** There is real mathematics behind the retrospective step, but none of it licenses a backward causal arrow.

## 1. What the ledger actually does

Let:

- \(P\): the prediction recorded before the experiment;
- \(R\): the committed scoring rule;
- \(Y\): the experimental outcome;
- \(V=R(P,Y)\): the eventual verdict.

The ordinary causal structure is
\[
(P,R,Y)\longrightarrow V.
\]

If publishing predictions changes experimental conduct, there may also be \(P\to Y\). If anticipated grading disciplines predictors, the **present expectation of future grading** affects present behavior. Neither requires \(Y\to P\).

A valid commitment prevents changing \(P\) or \(R\) after learning \(Y\). It does not let \(Y\) reach backward and write them.

**The ledger constrains future accounts of the past, not the past itself.**

## 2. The rigorous “backward” mathematics

Future evidence can change a probability distribution over earlier unknown states. Given an earlier state \(X_t\), earlier information \(D\), and a later observation \(Y=y\),
\[
p(X_t\mid D,Y=y)
=
\frac{p(Y=y\mid X_t,D)\,p(X_t\mid D)}
     {p(Y=y\mid D)}.
\]

This is **smoothing or retrodiction**. The likelihood supplied by later evidence reweights hypotheses about the earlier state. For suitable dynamical models, this likelihood can be propagated backward mathematically.

That is a genuine connection to two-boundary inference. It is not merely a literary resemblance.

But distinguish:

- **Conditioning:** Which earlier histories remain plausible *given* this later observation?
- **Intervention:** Which earlier histories change *because we physically set* a later variable?

Those are different operations:
\[
p(X_t\mid Y=y)\quad\text{versus}\quad p(X_t\mid \operatorname{do}(Y=y)).
\]

In an ordinary forward-causal model, intervening on a later variable does not change the distribution of earlier states. Conditioning can change it dramatically.

**Backward inference is not backward influence.**

For a fully recorded prediction, even “retrodiction” may overstate the case: nobody is estimating what the prediction was. They are computing its score.

## 3. Where the TSVF analogy breaks

A backward-evolving quantum state has a specific mathematical role in quantum probabilities for pre- and post-selected ensembles. Your falsification criterion is a classical decision rule. It is not a quantum state, a dynamical field, or a mechanism carrying influence backward.

Moreover, the correspondences in the doctrine are misplaced:

- The **pre-registered rule** specifies how results will be evaluated.
- The **observed outcome**, or a selected subset of outcomes, supplies the later evidence.
- The **verdict** evaluates the earlier record against that evidence.

The rule itself is not the future boundary.

Nor does merely recording and grading every outcome constitute post-selection. Post-selection means selecting a subset according to an outcome criterion. Calling ordinary evaluation “post-selection” imports physics vocabulary without its defining operation.

Even in TSVF experiments, an outcome-conditioned weak-value signal is recovered using the post-selection information; it is not an advance channel for reading an independently controllable future.

## 4. What is genuinely more than bookkeeping

The protocol can have real causal force:

- commitment makes prediction substitution harder;
- separation of roles reduces leakage and discretionary grading;
- frozen criteria constrain hindsight;
- mandatory corrections change subsequent beliefs and decisions;
- anticipated accountability changes present incentives.

These are **forward-causal effects of an information institution**. “Bookkeeping” is not synonymous with “causally inert.” Contracts, accounting systems, and access logs also change behavior.

But cryptography does not establish experimental truth. A hash commitment establishes consistency with committed bytes under its security assumptions. It does not by itself establish when they were created, that no alternative commitments existed, that nobody leaked the key, or that the measurement was honest. Public witnessing, completeness controls, and procedural audits remain necessary.

## 5. The brutal verdict

| Claim | Status |
|---|---|
| Later evidence changes rational assessments of earlier claims | **Real mathematics** |
| Commitments and grading change future behavior | **Buildable, ordinary causal engineering** |
| A frozen rule and an outcome jointly determine a verdict | **Exactly bookkeeping—and useful** |
| The outcome makes failed predictions cease to have occurred | **False** |
| The ledger realizes a TSVF backward-evolving state | **Unsupported** |
| The fleet steers the physical past | **No demonstrated mechanism or evidence** |

A failed prediction remains an actual historical event. It becomes **refuted**, not retroactively inadmissible as history.

Your “both” survives only in this form: **the system is bookkeeping with real forward-causal consequences.** It does not survive as “part bookkeeping, part physical retrocausation.”

The defensible name is **prospective commitment with retrospective adjudication**. Calling it “retrocausal steering” is metaphor unless you supply evidence of backward influence that conditioning, selection, leakage, and ordinary forward causation cannot explain.
