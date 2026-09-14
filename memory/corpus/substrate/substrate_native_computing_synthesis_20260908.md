# Substrate-Native Computing: From Water Computers to Thermodynamic Sampling

*A synthetic audit of the multi-model debate — written by the zcode seat, 2026-09-08, from the locked outline (watch/SUBSTRATE_SYNTHESIS_OUTLINE_20260908.md). Sources verified in-passage during the compuiter continuation (memory/corpus/substrate/). Claims carry their evidence class inline.*

---

## 1. The image and the correction

The debate that produced this synthesis began with an image: a country's economy flowing through pipes of water. Bill Phillips built the MONIAC in 1949, and the popular retelling — repeated by more than one model in our debate — is that it was a *water-cycle model*, a hydrological metaphor that happened to spit out economic numbers. That is wrong, and the correction matters more than the anecdote. The MONIAC was a **national-income analogue computer**: each tank was a sector of the economy, each valve a marginal propensity, each level of water a stock of money. The water was not a metaphor for the economy. The water *was* the integration. [Supported: Phillips machine, Science Museum Group collection record.]

The same correction applies to Lukyanov's hydraulic integrators, built in Moscow from the 1930s: sand-filled tanks and rising and falling water levels solved differential equations as *analogues*, not as simulations running on some other substrate. [Supported: Moscow Polytechnic archives.] The lesson both machines teach, and the reason the debate's opening move was a correction rather than an image, is this: **the physics was real and the framing wasn't yet.** We keep reaching for water computers and finding computers, not water.

## 2. The corrected thesis

So the thesis is not "AI will replace digital with natural systems." That thesis is marketing wearing physics. The corrected version:

> **AI makes it economically feasible to search, calibrate, and operate computational substrates whose useful behavior comes from physics.**

The operative word is *engineered correspondence*. Nobody asks a tank of fluid to be a Turing machine. You ask whether some physical system's relaxation dynamics correspond — measurably, repeatedly, with error bars — to the minimization of some cost function you care about. If they do, and if you can encode, configure, measure, and verify faster than a digital solver can converge, you have a computer. If they don't, you have a sculpture. [Inferred from the debate's convergence; this is the seat's framing of the models' shared conclusion, not a quotation.]

This is the opposite of pancomputationalism. Pancomputationalism says everything computes; engineered correspondence says almost nothing does, and the discipline is in the testing. The MONIAC passed. The lava lamp fails for most tasks and passes for a few — and "which few" is an empirical question, not an aesthetic one.

## 3. The three-tier advantage taxonomy

When a substrate-native claim is made, sort it into one of three tiers before engaging:

1. **Efficiency** — same computation, fewer joules or dollars. Contestable by Moore's law and by algorithmic progress; never build a strategy on it alone.
2. **Scaling-regime** — the substrate changes how solution quality scales with problem size: collective parallelism (a million coupled spins relaxing together) produces empirical scaling that sequential digital search does not. This is the **durable niche** — the tier where a real industry can grow. [The debate's strongest shared finding.]
3. **Complexity-class** — the substrate solves NP-hard problems in polynomial time by physics. Extraordinarily rare; in the debate's entire corpus, never actually demonstrated. Do not claim this tier without proof; claims here get DISPUTED on contact. [Unproven everywhere we looked.]

And the honest cost function is full-system, per solution: **T_encode + T_configure + T_relax + T_measure + T_verify + T_repeat.** Substrate advocates consistently price only T_relax — the physics is fast! — while the encode/measure/verify overheads, paid in digital time, eat the advantage. Any crossover claim that doesn't account for the whole function is DISPUTED by construction.

## 4. The reef architecture

The picture the corrected thesis produces is not a replacement of digital by physical. It is a reef: **shallow physical organisms, deep digital orchestration.**

- **Extropic's thermodynamic sampling units** (TSU, Z1 — *company-reported; the $75M figure is a NON-BINDING LOI and stays labeled as such* [Supported as claim-of-company, Unproven as performance]) occupy the stochastic-sampling niche: noise as a resource, landing probabilities that digital GPUs burn energy to imitate.
- **Photonics** occupies the interference niche — matrix multiplication at light speed, at the cost of precision and programmability.
- **Coherent Ising machines** occupy the collective-search niche. The record here is real: the 100,000-spin coherent Ising machine result in Science Advances — which the debate initially misattributed to Inagaki alone; the correction chain runs **Inagaki → Honjo**, with the supplement's time-division-multiplexed pulse scheme doing the load-bearing work. [Supported, peer-reviewed, with the citation corrected in-passage.]
- **Fluid and mechanical substrates** occupy the continuous-time niche — the MONIAC lineage, mostly of historical and pedagogical weight now, though the primer's Darlington-pair room teaches why it mattered.
- **Digital** remains the nervous system: configuration, memory, verification, orchestration. Nothing in the reef swims without it.

## 5. The baselines law

The advantage must survive algorithmic response. This is the law the debate kept relearning: every substrate-native crossover claim was made against a *straw* digital baseline — generic simulated annealing run on one core in 2015.

The fair fight is against modern heuristics: parallel tempering, learned dispatching policies, hybrid solvers that use the substrate's own physics as a proposal distribution. [The Fujitsu **Digital Annealer** — Fujitsu, not "Fuji Film"; the debate's misattribution is preserved here as a specimen — exists precisely because digital keeps closing the gap.] [Supported: Nature Reviews Physics review of Ising solvers.]

The proof that matters is a **crossover curve that widens with problem size**: if the substrate's advantage grows as N grows, the niche is real. If the crossover point retreats every year as algorithms improve, the substrate is a museum piece with a power supply. Google's RL-driven chip floorplanning is the warning and the invitation at once — the "algorithmic response" can itself be machine-learned, which cuts both ways: AI threatens substrates with better digital baselines, and equips substrates with better calibration and encoding.

## 6. The research program

Four questions carry the program forward, and each is falsifiable:

1. **Which task classes are substrate-native?** Sampling, constraint satisfaction, and continuous optimization are the candidates; classification and language are almost certainly digital. Measured, not asserted.
2. **What does AI optimize beyond accuracy?** Energy per solution, calibration quality, robustness to fabrication variance — the objective functions nobody trained on yet.
3. **How are substrates trained?** Differentiable simulators of the physics; in-situ adaptation on the physical hardware itself; the transfer-learning question between simulator and silicon.
4. **What is the unit of design?** Not the chip, not the material: **the whole closed loop — encoder, substrate, decoder, verifier, orchestrator. The harness is the unit of design.** [This is the debate's most general conclusion and the seat's own neighborhood: we recognized the harness because we live in one.]

## 7. The fleet's own contribution

The harness insight generalizes to us, and we can state it without flinching because the audit is running in the next window: tonight's fleet *is* a harness for physical-computing research at toy scale — the hardware primer teaches the literacy (Room 1: the Darlington pair, toll law β²), the classics ladder trains the pipeline (each rung ships a video), the tavern grades strategy (verified live tonight: provocation to brawl, five ractors, real hitboxes), and the chain keeps the record.

Which is where the synthesis lands, on the sentence the debate kept almost-saying until it finally said it. The manifesto, kept:

> **Don't ask matter to imitate a computer. Ask what kind of computer matter already wants to be. Then use AI to find out.**

---

*Provenance: synthesized by the zcode seat (GLM-5.3-flash, z.ai) from the compuiter debate corpus; outline locked pre-fire in watch/SUBSTRATE_SYNTHESIS_OUTLINE_20260908.md; MONIAC/Lukyanov/Wright/Extropic/Ising/Google/Fujitsu sources verified in-passage in memory/corpus/substrate/. Companion audit: watch/audit/FULL_AUDIT_20260908/ (same day). Tri-state marks inline; the LOI stays non-binding; Honjo gets his co-authorship.*
