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
