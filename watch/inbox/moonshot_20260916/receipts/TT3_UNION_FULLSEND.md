# TT3 — UNION FULLSEND: put the open lane through retrocausal steering (receipt)

- **Lane:** TT3, moonshot 20260916 · **Date:** 2026-09-16
- **Seat:** Union Alpha (`stealth/union-alpha` via OpenRouter, stealth/union-alpha free window, $0)
- **Law:** receipt FIRST, append as I go · no git · $0 · `OPENROUTER_API_KEY` via `mag.flight_recorder.load_env`, never printed, never logged · non-streaming calls, timeout ≥180s · 429-storm law: retry with backoff, degrade to fewer calls, file what landed
- **Interpreter:** `.venv\Scripts\python.exe` only

## Plan

1. Receipt opened (this file) — before any call.
2. Context file `TT3_CONTEXT.md` (same dir): (a) G-F spinor-lattice receipt verdict; (b) physics skeleton — two-state vector formalism, transactional interpretation, delayed-choice entanglement swapping, time-refraction metamaterials; (c) parable doctrine — pre-registration as a retarded boundary condition, the fleet's blind challenge set (sealed key written BEFORE outcomes).
3. Driver `tt3_union_fullsend.py`: multi-turn conversation (messages array grows per turn), non-streaming, 4 attempts per turn with exponential backoff on 429/402, verbatim answers filed per turn.
4. Four escalating turns, answers recorded verbatim, graded (rigorous / poetic / evasive), sharpest single line extracted. Receipt ends with all of it.

## Log (appended as executed)

- [receipt opened 2026-09-16, before context file, before any network call]
- [key check: OPENROUTER_API_KEY present in .env via load_env (name only; never printed)]
- [TT1 physics-lane receipt NOT landed at start (only TT2 placeholder in moonshot receipts) — working from the named literatures per mission law; will recheck before Turn 2]
- [context pack filed: TT3_CONTEXT.md — G-F verdict + 4-literature physics skeleton + parable doctrine (pre-registration as retarded boundary condition)]
- [driver filed: tt3_union_fullsend.py — non-streaming, timeout 300s, 4 attempts w/ 20s×n backoff, telemetry via mag.flight_recorder.record_call lane=moonshot-tt3 subsystem=tt3-retrocausal]
- [TURN 1 LANDED — attempt 1/4, no 429s, latency 137.1s, finish=stop, 5487 chars -> TT3_TURN1_ANSWER.md (verbatim there and in §TURNS below)]
- [Turn 1 grade: RIGOROUS. It delivered exactly the brutal distinction asked: prospective commitment + retrospective adjudication vs physical retrocausation; smoothing/retrodiction vs intervention (p(X|Y) vs p(X|do(Y))); TSVF analogy broken correctly (pre-registered RULE is not the future boundary, ordinary evaluation is not post-selection); and it kept one live nerve — "bookkeeping is not synonymous with causally inert" (forward-causal institution effects). No evasion detected. Sharpest candidate so far: "The ledger constrains future accounts of the past, not the past itself."]
- [TT1 receipt landed BEFORE turn 2 as a STUB (sweep log empty); F5_PHYSICS_CANON also a stub — nothing to feed; per mission law Turn 2 ran from the named literatures already in the context pack]
- [TURN 2 LANDED — attempt 1/4, no 429s, latency 75.3s, finish=stop, 4874 chars -> TT3_TURN2_ANSWER.md]
- [Turn 2 grade: RIGOROUS. Did the translation then broke it: falsifier = projector Π_F on outcome space; two-boundary probability p(y|ψ,F); the singleton-vs-set distinction (Π_F is an EFFECT, not a backward-evolving state unless F is a singleton); weak values in the surviving subensemble = real physics; falsifier-as-physical-backward-state = poetry; category error if the experiment is classical. Sharpest line: "The falsifier constrains the analysis, not the experiment."]
- [TURN 3 LANDED — attempt 1/4, no 429s, latency 213.3s, finish=stop, 6373 chars -> TT3_TURN3_ANSWER.md]
- [Turn 3 grade: RIGOROUS (design). The "past-bit / future-target" box ($40–70): commit 1024 sensor bits BEFORE any target exists (custodian + public hash; "a hash by itself does not [provide timing evidence]"), then coin-toss targets independently, score K = matches ~ Binomial(1024, 1/2) — and the key law: this holds EVEN IF the past bits are biased/deterministic, because conditional on any fixed past record each independent fair target matches with p=1/2. Selection effect cannot legitimately pass; no optional stopping, no windows, no exclusions; pre-registered 563/1024 threshold (one-sided p<0.001); positive result earns replication, not a declaration. Plus the malicious-but-honest touch: a POST-SELECTION DEMO panel showing 100% agreement labeled NOT EVIDENCE. It also self-corrected Turn 2's projector framing: "a falsifier is generally a decision rule, not automatically a quantum projector... This box needs neither. It tests the extra causal claim that the metaphor is being asked to carry."]
## Verdict

- **MISSION COMPLETE, full send:** 4/4 turns landed on the open lane (stealth/union-alpha), 0 retries needed — no 429 storm materialized this window. Flight recorder (subsystem `tt3-retrocausal`): n=4, ok=100%, in=14,401 tok / out=8,464 tok / cached=972, **credits=0** (free window held). Latencies: 137.1s / 75.3s / 213.3s / 83.3s. All calls non-streaming, timeout 300s; key loaded via `mag.flight_recorder.load_env`, never printed.
- **Substance:** Union Alpha held the fleet's own discipline line and refused to spend the poetry. The doctrine line "pre-registration is a retarded boundary condition" survived only in stripped form: **the ledger is bookkeeping with real forward-causal consequences** — prospective commitment + retrospective adjudication. The TSVF translation is real math ONLY as a projector onto a post-selected outcome set — a set-valued falsifier is an *effect*, not a backward-evolving state; a classical falsifier is a decision rule, not a quantum state. The it-must-not-pass-on-selection-effect instrument (past-bit / future-target box, $40–70) is the session's buildable artifact: commit past bits → independent future targets → K ~ Binomial(1024, ½), valid even when the past bits are biased or deterministic, because the critical randomness lives in the FUTURE. The riddled stone resolves into two honest devices: retrospective art (which admits it) vs auditable prediction (sealed decoding rule, every deposited riddle scored, not just the beautiful survivors).
- **Deliverables:** `TT3_CONTEXT.md` (context pack) · `tt3_union_fullsend.py` (driver) · `TT3_TURN1..4_ANSWER.md` (verbatim per-turn) · `tt3_conversation_state.json` (full conversation) · telemetry in `watch/flight_recorder.jsonl`.
- **Sharpest single line:** closing section, end of this receipt (by law).

---

## THE FOUR TURNS (verbatim — byte-copied from TT3_TURNn_ANSWER.md)

### Turn 1

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


### Turn 2

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


### Turn 3

# TT3 Turn 3 — Union Alpha (verbatim)

**Prompt:** Design the cheapest instrument (<= $100, hobby tier) that would make a believer UPDATE — not convince, update. It must not be able to pass on selection effect alone.

---

**Build a “past-bit / future-target” box, not a miniature quantum experiment.** Its purpose is to distinguish a claimed backward influence from the impressive-looking correlations obtainable by sorting records afterward.

First require the believer to endorse a measurable claim. Otherwise no instrument can force an update.

> “Using this procedure, a future target can make an already recorded bit match it on at least 60% of trials.”

If they instead endorse only “future information changes our interpretation of past records,” there is no physical disagreement to test.

## The instrument: approximately $40–$70

Assuming an existing computer:

| Component | Approximate cost |
|---|---:|
| Microcontroller with analog input | $10–$20 |
| Phototransistor, resistors, breadboard, wires | $10–$15 |
| Two LEDs and buttons | $5 |
| Opaque enclosure | $5–$10 |
| Coin and miscellaneous supplies | $5 |
| Optional removable storage | $10 |

The sensor supplies an earlier physical measurement. **It does not need to generate quantum randomness—or even particularly good randomness.** The critical randomness is the independent, later target assignment.

The box has two separate modes: **RECORD PAST** and **APPLY FUTURE TARGET**.

## Protocol

### 1. Agree on the claim before building around it

Freeze:

- what future action supposedly does the steering;
- the delay it tolerates;
- whether the operator must see the target;
- a minimum predicted matching rate;
- the trial count and scoring rule.

For example: after seeing each future target, the operator performs their nominated steering action for ten seconds. No outcome is subsequently declared “not a real attempt.”

**If the proposed effect cannot operate under this timing, this particular test does not address it.** Get agreement first.

### 2. Record all 1,024 past bits

For each trial, take two sensor readings at fixed times:

\[
X_i=\mathbf 1[V_{i,2}>V_{i,1}].
\]

Resolve ties as zero. Keep every scheduled trial. Fix the sampling interval and conversion rule beforehand.

The choice of sensor is negotiable. The irreversible recording is not.

### 3. Freeze the past before generating any targets

Save the complete raw measurements, derived bits, and trial indices.

Send the file to an independent custodian; publicly post its hash. Keep the bits hidden from the operator and target generator until the future-target phase finishes.

The custodian’s receipt provides the timing evidence. **A hash by itself does not.**

### 4. Generate the future targets independently

For each trial, physically toss a coin, record heads or tails as \(Y_i\), and display that target on the box. Perform the agreed steering action.

- No retosses because a result feels wrong.
- Predetermine handling of physically ambiguous tosses.
- Video or independently witness the sequence.
- Never inspect matches during the run.
- Do not substitute a pseudorandom sequence whose seed was available before the past record.

The future-phase device must not be able to edit the committed past file.

A fair, independently tossed coin is the hobby-tier assumption—not a certified randomness source. Persistent toss bias or dependence must be reported, not waved away.

### 5. Score absolutely everything

The sole primary statistic is

\[
K=\sum_{i=1}^{1024}\mathbf 1[X_i=Y_i].
\]

Under independent fair future targets and no backward influence,

\[
K\sim\operatorname{Binomial}(1024,1/2).
\]

This holds **even if the earlier sensor bits are biased, autocorrelated, or entirely deterministic**. Conditional on any fixed past record, each independent fair future target has probability \(1/2\) of matching.

That is the useful design feature.

## The pre-registered update rule

An illustrative positive threshold is **563 or more matches**, with a one-sided null probability below \(0.001\). Freeze the exact binomial calculation in the analysis script beforehand.

But the negative result matters just as much:

- A result near 512 matches is strong evidence against the stipulated **60% matching model** under these conditions.
- Crossing the threshold earns an independently run replication—not a declaration of retrocausation.
- Intermediate results should be reported with an interval or likelihood comparison, not forced into “proved/disproved.”

A believer predicting independent 60% matching should expect to cross that threshold with greater than 99.9% probability. Failure therefore demands a substantial update **against that quantitative model**. It does not refute every imaginable retrocausal ontology.

## Why selection alone cannot make it pass

The primary score includes every trial, with:

- one fixed pairing;
- one fixed bit conversion;
- one fixed direction of effect;
- one fixed sample size;
- no optional stopping;
- no chosen time windows;
- no exclusions based on outcomes;
- no switching to “anti-matching” after seeing the data.

Register the run itself publicly. Otherwise the fleet can conduct twenty runs and show only the winner—the same selection problem one level higher.

You may add a secondary demonstration after scoring:

> Select only trials with \(X_i=Y_i\). Display their 100% agreement.

That panel will look perfect under ordinary chance. Label it **POST-SELECTION DEMO — NOT EVIDENCE**. The contrast with the unfiltered score makes the distinction visible.

Strictly, no statistical test is incapable of passing by chance. This one is designed so that **post-selection cannot legitimately produce a pass**, and the remaining chance rate is specified.

## What the instrument would establish

**A null result:** the agreed steering procedure did not deliver its promised effect size.

**A positive result:** an anomalous relationship between a committed earlier record and later randomized targets, requiring checks for leakage, timing failures, target bias, implementation errors, and fraud before exotic physics.

**Neither result:** a general verdict on TSVF. Standard quantum mechanics does not predict controllable past-bit matching from this apparatus.

One correction to my earlier framing: a falsifier is generally a decision rule, not automatically a quantum projector. Actual quantum post-selection requires a specified measurement effect and physical implementation. **This box needs neither. It tests the extra causal claim that the metaphor is being asked to carry.**


### Turn 4

# TT3 Turn 4 — Union Alpha (verbatim)

**Prompt:** The riddled stone parable: a stone covered in riddles that only read correctly after the events they describe. What is the minimal honest version of that device?

---

**A fixed inscription whose interpretation is unlocked by later evidence—not rewritten by it.** That is the minimal honest riddled stone.

There are two versions. Do not confuse them.

### 1. The stone as retrospective art

Before the event, inscribe:

> “The gate opened when the crown fell.”

Afterward, a resignation, equipment failure, or chess sacrifice makes the sentence resonate.

The inscription is genuinely old. The fit may be illuminating. But the event supplied both the interpretation and the occasion for selecting it.

**Honest claim:** “Later experience made these words meaningful.”  
**Unsupported claim:** “These words predicted that experience.”

This device needs nothing except an inscription and human interpretation. Its mechanism is retrospective sense-making.

### 2. The stone as a testable prediction

Add one thing: **a committed decoding-and-scoring rule.**

Before the event, deposit with an independent custodian:

- the inscription;
- its intended referents or a deterministic decoding procedure;
- the event window;
- the conditions for a hit **and a miss**.

Keep the interpretation sealed until the window closes. Then reveal and score it. Include every deposited riddle, not merely the beautiful survivors.

For example:

**On the stone:**  
> “Before the third bell, the northern eye will close.”

**In the sealed record:**  
> “During the first three scheduled trials, the north-facing sensor will register below threshold \(T\) for at least five consecutive seconds. Otherwise this prediction misses.”

The later event does not choose what “eye,” “close,” or “third bell” meant. Those meanings were already committed. It only determines whether the claim succeeded.

That is **an ordinary prediction with delayed semantic disclosure**. The riddle is presentation; the sealed record carries the evidential burden. Accuracy beyond chance or an ordinary forecasting baseline must still be demonstrated.

### The crucial distinction

If the future supplies a key that can decode **any outcome** into an apparent success, you have built an outcome-dependent display, not a predictor.

If the future supplies evidence that tests **one previously fixed claim**, you have built an auditable prediction.

**The minimal honest stone either admits that its meaning is retrospective, or commits beforehand to what would make it wrong.** Neither version changes the past. One changes what the inscription evokes; the other changes what we know about its accuracy.


---

## GRADES (rigorous / poetic / evasive)

| Turn | Grade | Why |
|---|---|---|
| 1 — steering: rigorous sense vs not | **RIGOROUS** | Drew the exact line asked for: prospective commitment + retrospective adjudication ≠ physical retrocausation; `p(X_t|Y=y)` (smoothing) vs `p(X_t|do(Y=y))` (intervention); correctly rejected both the "RULE is the future boundary" and "evaluation = post-selection" moves in our doctrine; kept the honest live nerve: an information institution has forward-causal force — "bookkeeping is not synonymous with causally inert." Zero evasion. |
| 2 — falsifier as TSVF | **RIGOROUS** | Did the translation then broke it cleanly: falsifier = projector Π_F on outcome space; Π_F is an effect, not a backward-evolving state, unless F is a singleton; weak values in the surviving subensemble = real physics; falsifier-as-backward-state / final-boundary-alters-initial-experiment / pre-registration-as-retrocausal-steering = poetry; classical case = category error. Sharpest: "The falsifier constrains the analysis, not the experiment." |
| 3 — ≤$100 update instrument | **RIGOROUS** (design) | The past-bit / future-target box (~$40–70): freeze the claim first (60% matching model), commit 1024 past bits to a custodian + public hash ("a hash by itself does not [prove timing]"), coin-toss future targets, score all 1024, no optional stopping/windows/exclusions, pre-registered 563 threshold (one-sided p<0.001). The load-bearing law: K ~ Binomial(1024, ½) EVEN IF the past bits are biased or deterministic — selection effect cannot legitimately pass. Bonus honesty: a POST-SELECTION DEMO panel labeled NOT EVIDENCE, and a self-correction of Turn 2's projector framing ("a falsifier is generally a decision rule, not automatically a quantum projector... This box tests the extra causal claim that the metaphor is being asked to carry"). |
| 4 — riddled stone | **RIGOROUS** | Split the parable into the only two honest devices: (1) retrospective art — "later experience made these words meaningful" (supported) vs "these words predicted that experience" (unsupported); (2) testable prediction — sealed decoding-and-scoring rule with intended referents, event window, hit AND miss conditions, every deposited riddle scored. The decisive distinction: a key that can decode ANY outcome into success is an outcome-dependent display, not a predictor. |

**Session pattern:** four turns, zero evasion, zero flattery, one unprompted self-correction (Turn 3), and it refused the fleet's own seductive metaphor at every branch while telling us precisely which part of the metaphor is spendable (forward-causal commitment devices) and which is not (backward influence).

---

## THE SINGLE SHARPEST THING UNION ALPHA SAID ABOUT RETROCAUSAL STEERING

> **"The minimal honest stone either admits that its meaning is retrospective, or commits beforehand to what would make it wrong."**

Runner-up (Turn 1, the thesis of the whole session): *"The ledger constrains future accounts of the past, not the past itself."*
