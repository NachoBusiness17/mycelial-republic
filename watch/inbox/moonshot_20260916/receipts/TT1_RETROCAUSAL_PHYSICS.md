# TT1 — RETROCAUSAL PHYSICS SWEEP (receipt-first)

- **Lane:** operator moonshot 2026-09-16 — retrocausal steering & time travel
- **Window:** literature 2015–2026 (+ canonical pre-2015 anchors)
- **Discipline:** tri-state per claim — **[measured]** (instrument), **[mechanism]** (theory-level machinery), **[interpretation-overreach]** (ontology beyond evidence)
- **Budget law:** $0–100 fleet, no lab, no paid APIs. Sources: WebSearch / WebFetch / arXiv API (free).
- **No git.** This file is the receipt; appended as the sweep progresses.

<!-- SWEEP LOG -->
- [ ] §1 Retrocausal interpretations (TSVF, TI, all-at-once/Wharton, PPS)
- [ ] §2 Delayed-choice family (Wheeler, entanglement swapping, cosmic)
- [ ] §3 Time interfaces in metamaterials (temporal reflection/refraction, time crystals)
- [ ] §4 CTC computation (Deutsch, Aaronson critique, simulations)
- [ ] §5 Weak values / "past of a quantum particle"
- [ ] Closing: honest hierarchy + 3 must-read papers

## §1 — Retrocausal interpretations of QM (survey, 2015–2026)

### 1a. Two-State Vector Formalism (TSVF) — Aharonov, Bergmann–Lebowitz lineage; Aharonov & Vaidman
- **What it claims:** quantum systems are described by TWO boundary conditions — a forward-evolving state from preparation and a backward-evolving state from post-selection. Between them, weak measurements read out "weak values" A_w = ⟨φ_f|A|ψ_i⟩/⟨φ_f|ψ_i⟩ that can be anomalous (outside the operator eigenvalue range).
- **What it forbids:** nothing new — TSVF is claimed to be *mathematically equivalent* to standard QM. It generates no novel measurable deviations; the "backwards-in-time" state is inferred from the future boundary condition, not a controllable signal channel.
- **Experimental status:** all TSVF-consistent experiments (weak measurement of pre-/post-selected ensembles) are equally well described by standard QM. No experiment distinguishes TSVF from Copenhagen/Many-Worlds.
- **Tri-state:** [measured] the weak-value statistics on pre-/post-selected ensembles; [mechanism] the two-boundary formal bookkeeping; [interpretation-overreach] the ontological reading that "the future state really exists backward in time" / that weak values are the real properties of individual systems.
- **Canonical citation:** Y. Aharonov & L. Vaidman, "The Two-State Vector Formalism of Quantum Mechanics" (review; arXiv:quant-ph/0105101, updated in *Time in Quantum Mechanics*, Springer 2002; Vaidman's pedagogical review arXiv:0706.1347). Recent formal work: "No contextual advantage in nonparadoxical scenarios of the TSVF," Phys. Rev. A **107**, 012206 (2023).
- **$0–100 fleet translation:** nothing to build — this is bookkeeping over standard QM; the fleet's honest instrument is a Qiskit/numpy weak-value simulator for auditing any "looked at the future" claim before believing it.

### 1b. Transactional Interpretation (TI / RTI) — Cramer 1986; Kastner's relativistic "possibilist" extension
- **What it claims:** quantum events are "transactions" — a handshake between an emitter's retarded offer wave and an absorber's advanced confirmation wave (Wheeler–Feynman absorber theory). Kastner's RTI (2nd ed. of her CUP book, *…A Relativistic Treatment*) pushes the waves outside spacetime as "possibilist" entities.
- **What it forbids:** signaling via the advanced waves — the handshake is intrinsically self-consistent and collapses the ensemble of possible transactions; no controllable message can ride an advanced wave backward.
- **Experimental status:** empirically identical to standard QM by design. No distinguishing experiment exists or is proposed with a feasible budget; decades of debate (Maudlin, Marchildon, and others) over whether the absorber-response story is well-defined remain *conceptual*, not experimental. Kastner argues TI is consistent with Bell tests "eliminating observer-dependent reality" — this is interpretation, not data.
- **Tri-state:** [measured] nothing TI-specific; [mechanism] the advanced/retarded wave algebra is a re-derivation of standard scattering math; [interpretation-overreach] the absorber ontology (waves "outside spacetime," transactions as the birth of actualized events).
- **Canonical citation:** J. G. Cramer, Rev. Mod. Phys. **58**, 647 (1986); R. E. Kastner, *The Transactional Interpretation of Quantum Mechanics: The Reality of Possibility*, 2nd ed. (CUP, ~2022, "A Relativistic Treatment"); arXiv:1204.5227.
- **$0–100 fleet translation:** a storytelling layer over textbook QM with zero instrumentation payoff — treat any "absorber feedback steers the emitter" claim as unfalsifiable poetry unless it predicts a Born-rule deviation (none does).

### 1c. All-at-once / Lagrangian-view retrocausality — Wharton (& Argaman)
- **What it claims:** (Bell-derived) quantum correlations that look nonlocal in a state-at-an-instant picture become local if the hidden variables are constrained by measurement settings *in the future* as well as the past — an all-at-once, action/Lagrangian ("block-universe") dynamics. Bell's theorem does NOT exclude these "locally mediated" models because Bell assumes the settings are free inputs exogenous to the model.
- **What it forbids:** retro-*signaling* — in these models future settings influence past parameters only in ways that keep observed statistics Born-rule; the retrocausal channel is exactly the one that cannot carry a controllable message.
- **Experimental status:** none distinct from standard QM; this is a research program for *reformulating* QM, motivated by (a) Bell-inequality closure, (b) avoiding retro-signaling paradoxes. No experiment can currently tell an all-at-once model from ordinary QM — it is program-level theory.
- **Tri-state:** [measured] the underlying Bell-violation experiments (settings chosen late, spacelike separated); [mechanism] the argument that Bell assumptions (not just locality) can be relaxed; [interpretation-overreach] any claim that experiments *confirm* retrocausal influence rather than merely remain compatible with it.
- **Canonical citation:** N. Argaman & K. B. Wharton, "Colloquium: Bell's theorem and locally mediated reformulations of quantum mechanics," Rev. Mod. Phys. **92**, 021002 (2020) (arXiv:1906.04313); Stanford Encyclopedia of Philosophy, "Retrocausality in Quantum Mechanics" (cites it as the umbrella review).
- **$0–100 fleet translation:** this is the *only* intellectually serious lane where "the future constrains the past" survives Bell — but it lives entirely at the theory level; fleet work = read the RMP Colloquium in full, do no experiments, expect no steerage.

### 1d. PPS (pre- and post-selected) ensembles — Aharonov, Popescu, Tollaksen
- **What it claims:** with careful pre-selection AND post-selection, quantum systems exhibit "week-value"-type regularities (e.g., photons doing "week-value analogs of teleportation," claims that quantum computations can complete before the gates run — the "counterfactual computation" and "measurement without interaction" family). PPS is the ensemble concept underlying TSVF and weak values.
- **What it forbids:** any faster-than-light or backward signaling: all PPS phenomena reduce to conditional statistics given both boundaries; without post-selection (which is only known *after* the fact) nothing observable changes.
- **Experimental status:** PPS experiments (three-box paradox in NMR/photons, weak-value amplification) consistently measured and consistent with standard QM; the dramatic *interpretations* ("the photon was in box A with amplitude 1 and box B with −0") are the contested part.
- **Tri-state:** [measured] conditional expectation values on PPS ensembles; [mechanism] the ABL rule + weak-value algebra; [interpretation-overreach] "the measurement reached back in time" rhetoric.
- **Canonical citation:** Y. Aharonov, S. Popescu, J. Tollaksen, "A time-symmetric formulation of quantum mechanics," Physics Today **63**(11), 27 (2010); ABL rule: Aharonov, Bergmann & Lebowitz, Phys. Rev. **134**, B1410 (1964) — the anchor pre-dates the window but every 2015–2026 PPS paper cites it.
- **$0–100 fleet translation:** PPS effects are real statistics but zero communication capacity — a fleet protocol could *use* weak values as a conditional-estimation trick in simulations; it cannot *receive* anything from the future.

<!-- SWEEP LOG -->
- [x] §1 Retrocausal interpretations (TSVF, TI, all-at-once/Wharton, PPS)
- [ ] §2 Delayed-choice family (Wheeler, entanglement swapping, cosmic)
- [ ] §3 Time interfaces in metamaterials (temporal reflection/refraction, time crystals)
- [ ] §4 CTC computation (Deutsch, Aaronson critique, simulations)
- [ ] §5 Weak values / "past of a quantum particle"
- [ ] Closing: honest hierarchy + 3 must-read papers

## §2 — Delayed-choice family (2012–2026)

### 2a. Wheeler delayed choice (incl. space-scale 2017)
- **Claim tested:** the choice of wave-vs-particle measurement can be made *after* the photon is "in flight"; outcome statistics match standard QM.
- **Measured:** Vedovato et al., "Extending Wheeler's delayed-choice experiment to Space," Science Advances 3, e1701180 (2017) (arXiv:1704.01911) — satellite-ground interferometer, thousands of km, choice while photons in flight. Companion line: "Quantum eraser with causally disconnected choice," Ma et al., PNAS 110, 1221 (2013).
- **What it forbids:** no signal back — which-way/vs-interference is a description chosen by the measurement context; marginals never move.
- **Tri-state:** [measured] the wave/particle statistics under late choice; [mechanism] complementarity + postselection algebra; [interpretation-overreach] "the observer decides the past behavior of the photon."
- **$0–100 fleet translation:** description-order convention, not time steering — fleet instrument = a free Qiskit MZI sim that reproduces the algebra in minutes.

### 2b. Delayed-choice entanglement swapping (the Ma line)
- **Canonical:** X.-S. Ma, S. Zotter, J. Kofler, R. Ursin, T. Jennewein, Č. Brukner, A. Zeilinger, "Experimental delayed-choice entanglement swapping," Nature Physics 8, 479–484 (2012) (arXiv:1203.4834). NOTE (verified): the operator's "Ma/Zhao/Perumal" attribution is garbled — no Zhao or Perumal on this paper; author list above is from the source.
- **What was demonstrated:** photons 1 and 4 detected and recorded *before* the Bell-state measurement (BSM) on photons 2&3; BSM choice made later by quantum random number. In post-selected 4-fold coincidences, 1&4 — which never interacted — show correlations consistent with having been projected onto entangled or separable states.
- **What it forbids:** signaling — the singles/marginals of photons 1&4 are unchanged; the "entangled in the past" appears only in post-selected conditional statistics assembled after the fact.
- **Tri-state:** [measured] the 4-fold coincidence correlations; [mechanism] entanglement-swapping algebra (the state of 1&4 is *defined* only relative to the later BSM outcome); [interpretation-overreach] "the future measurement determined what photons 1&4 were earlier."
- **$0–100 fleet translation:** correlations-at-detection, zero retro-channel; the honest fleet move is simulating the 4-photon circuit and the post-selection algebra — free — and using it as an audit tool against "future changed the past" claims.

### 2c. Cosmic-scale versions (freedom-of-choice closure)
- **Measured:** Handsteiner et al., PRL 118, 060401 (2017) (arXiv:1611.06985) — Bell settings from Milky Way stars (~600 yr back); Rauch et al., PRL 121, 080403 (2018) (arXiv:1808.05966) — settings from quasar light emitted ~7.8 and ~12.1 Gyr ago, 9.3σ violation, closing local-realist influence for ~96% of the experiment's past light cone.
- **What it does NOT demonstrate:** retrocausality. It *constrains* "freedom-of-choice" (superdeterministic back-action) windows; a retrocausal model is *consistent* with the data, not confirmed by it. Argaman's comment (arXiv:1705.04140, 2017) explicitly reads the cosmic tests through a retrocausal toy model — theory-level.
- **Tri-state:** [measured] Bell violations with cosmologically old setting seeds; [mechanism] closing the measurement-independence loophole class for bounded spacetime regions; [interpretation-overreach] "the universe answered from 12 billion years ago" rhetoric.
- **$0–100 fleet translation:** pure big-lab physics; fleet value is comprehension only — these are the strongest public evidence that whatever correlates exist, they cannot be *steered* (no setting-dependence is ever extractable as a signal).

<!-- SWEEP LOG -->
- [x] §1 Retrocausal interpretations (TSVF, TI, all-at-once/Wharton, PPS)
- [x] §2 Delayed-choice family (Wheeler, entanglement swapping, cosmic)
- [ ] §3 Time interfaces in metamaterials (temporal reflection/refraction, time crystals)
- [ ] §4 CTC computation (Deutsch, Aaronson critique, simulations)
- [ ] §5 Weak values / "past of a quantum particle"
- [ ] Closing: honest hierarchy + 3 must-read papers

## §3 — Time interfaces in metamaterials: the REAL "time boundary" physics (2023–2026)

### 3a. Temporal reflection & time refraction — demonstrated
- **Landmark (microwave):** H. Moussa, G. Xu, S. Yin, et al. (senior: A. Alù), "Observation of temporal reflection and broadband frequency translation at photonic time interfaces," Nature Physics 19, 863–868 (2023) (arXiv:2208.07236). A stripline medium whose impedance is switched in ~picoseconds by varactor metasurfaces; the "reflected" wave emerges at a *conjugated frequency band*, and paired time interfaces form the temporal Fabry–Pérot cavity.
- **Optical era (2026):** Segal, Konforty, Schiller, ... Plotnik, Segev, "About Time: Observation of Time-Reflection at Optical Frequencies," arXiv:2605.15632 (May 2026) — order-unity, sub-cycle refractive-index change; and "Sub-cycle time-refraction at optical frequencies," arXiv:2601.05566 (Jan 2026). Microwave PTC amplification through loss: Jones et al., arXiv:2605.21014 (3.8 dB gain). Full momentum bandgap in a PTC: Huang et al., arXiv:2604.17408. Spin waves: Schultheiss et al., PRL 126, 137201 (2021). Theory anchor: time-reflection enhanced near critical angle — Bar-Hillel et al., arXiv:2311.15070.
- **What "time reversal" actually means here:** the wave does NOT travel backward in time. A sudden impedance change mixes forward and backward waves; the "time-reflected" copy runs forward in time with frequency conjugated across the switched band. Energy is supplied by the external modulation pump. "Time mirror" is a boundary-condition metaphor, same family as phase conjugation.
- **Tri-state:** [measured] temporal reflection/refraction, frequency conjugation, momentum bandgaps, temporal Fabry–Pérot (2023–2026, multiple groups); [mechanism] time-domain scattering theory (Morgenthaler 1958 lineage; impedance mismatch in time = space analog); [interpretation-overreach] "a mirror that reflects into the past."
- **$0–100 fleet translation:** the transfer-function math is fully classical and laptop-sized — a fleet can implement temporal-interface DSP (frequency conjugation ≈ all-pass/phase-conjugate) in numpy and even approach a $20 breadboard L-C switched-line microwave demo (the 2023 experiment is electronics, not exotic optics). No backward-in-time communication exists here at any budget.

### 3b. Time crystals
- **Measured:** J. Zhang et al., "Observation of a Discrete Time Crystal," Nature 543, 217 (2017) (arXiv:1609.08684, trapped ions; verified) — with the companion Choi et al., Nature 543, 221 (2017) (diamond; standard citation, not re-verified this sweep). NMR: Rovny et al., PRL 120, 180603 (2018) (arXiv:1802.00126, verified). Prethermal: Kyprianidis et al., Science 372, 1192 (2021) (arXiv:2102.01695). 57-qubit superconducting: Frey & Rachel, Sci. Adv. 8, eabm7652 (2022) (arXiv:2105.06632). NV diamond: Randall et al., Science (2021) (arXiv:2107.00736). Google Sycamore eigenstate order: Mi et al., Nature 601, 531 (2022) (standard citation, not re-verified this sweep).
- **What "time crystal" actually means:** a periodically driven many-body system whose response is *sub-harmonic* (period-doubled or -multiplied) and rigid against perturbation. It is temporal pattern rigidity — Floquet many-body order — nothing oscillates "backward."
- **Tri-state:** [measured] sub-harmonic rigid response on ≥4 platforms; [mechanism] Floquet/MMB theory, prethermal and eigenstate-order frameworks; [interpretation-overreach] "breaking time-translation symmetry forever"/"perpetual motion in time" headlines.
- **$0–100 fleet translation:** fleet-simulable exactly (10–50 spin Floquet dynamics in numpy/JAX on a laptop reproduces every published time-crystal figure); nothing steerable, nothing backward.

## §4 — CTC computation

- **Deutsch model (1991):** a CTC system must be in a fixed point of a quantum channel; evolution is nonlinear (postselection-like). **Aaronson & Watrous, "Closed timelike curves make quantum and classical computing equivalent," Proc. R. Soc. A 465, 631–647 (2009)** (arXiv:0808.2669, verified): with CTCs, classical and quantum computers both land at exactly PSPACE. Two load-bearing consequences: (1) no hypercomputation from time travel; (2) any "power" comes from the unphysical nonlinearity, not from time. **Aaronson's standing critique:** Deutsch's nonlinear fixed-point condition is asserted, not mechanized — it smuggles in arbitrary post-selection, so the model proves nothing about physics and only redefines a complexity class.
- **Post-selected alternative (P-CTC):** Lloyd et al., "Closed timelike curves via post-selection: theory and experimental demonstration," PRL 106, 040403 (2011) (arXiv:1005.2219, verified) — teleportation + post-selection; resolved a photonic "grandfather paradox" *within the model*. Critique line: T. C. Ralph, "Problems with modelling closed timelike curves as post-selected teleportation," answered in Lloyd et al., arXiv:1108.0153.
- **Simulation claims:** Ringbauer, Broome, Myers, White, Ralph, "Experimental simulation of closed timelike curves," Nature Communications 5, 4145 (2014) (arXiv:1501.05014, verified) — photonic qubit "interacting with its earlier self," reproducing model effects (perfect discrimination of non-orthogonal states). Recent: Arvidsson-Shukur, McConnell, Yunger Halpern, "Nonclassical advantage in metrology established via quantum simulations of hypothetical closed timelike curves," PRL 131, 150202 (2023) (arXiv:2207.07666, verified) — press said "time travel simulated"; the substance is an entanglement+postselection metrological gain within the model. Follow-through: Song et al., "Agnostic Phase Estimation," PRL 132, 260801 (2024) (arXiv:2403.00054) on a superconducting processor. And the model-side theory keeps advancing: Ji, Lloyd, Wilde, "Retrocausal capacity of a quantum channel," PRL 136, 230801 (2026) (arXiv:2509.08965, verified) — capacity of backward-in-time messaging in noisy postselected CTCs. No refutation of the PRL 2023 metrology claim surfaced in this sweep; note it is statistics-within-model, not causality violation.
- **Tri-state:** [measured] lab circuits implementing the model's mathematics (2014 photons, 2024 superconducting); [mechanism] fixed-point/postselection algebra; PSPACE ceiling; [interpretation-overreach] "time travel demonstrated/simulated" — the labs simulated a *model*, and nothing moved backward.
- **$0–100 fleet translation:** every published "CTC simulation" figure is reproducible on a laptop for free (fixed-point iteration + Qiskit) — the fleet's honest instrument; and the PSPACE ceiling is the standing fact that kills "time travel = oracle" fantasies at the complexity level.

<!-- SWEEP LOG -->
- [x] §1 Retrocausal interpretations (TSVF, TI, all-at-once/Wharton, PPS)
- [x] §2 Delayed-choice family (Wheeler, entanglement swapping, cosmic)
- [x] §3 Time interfaces in metamaterials (temporal reflection/refraction, time crystals)
- [x] §4 CTC computation (Deutsch, Aaronson critique, simulations)
- [ ] §5 Weak values / "past of a quantum particle"
- [ ] Closing: honest hierarchy + 3 must-read papers

## §5 — Weak values and anomalous weak measurement

### 5a. Weak values as measured statistics
- **Measured:** anomalous weak values observed across platforms and tied to contextuality witnesses — Piacentini et al., PRL 116, 180401 (2016) (arXiv:1602.02075, experimental Pusey test); Waegell et al., "Confined contextuality in neutron interferometry... quantum pigeonhole effect," PRA 96, 052131 (2017) (arXiv:1609.06046); Maffei et al., PRA 107, 023710 (2023) (superconducting circuits, arXiv:2210.05323).
- **Mechanism-level:** anomalous weak values are provable witnesses of generalized contextuality — Kunjwal, Lostaglio, Pusey, PRA 100, 042116 (2019) (arXiv:1812.06940, robust and tight); Wagner & Galvão, "A simple proof that anomalous weak values require coherence," PRA 108, L040202 (2023) (arXiv:2303.08700); unifying framework: Kirkwood-Dirac quasiprobabilities — Lostaglio et al., Quantum 7, 1128 (2023) (arXiv:2206.11783).
- **Caveat (amplification toolkit):** the weak-value-amplification literature carries a known controversy — gains are largely parameter estimation in disguise; postselection can be traded against probe size (Ferrie–Combes line, mid-2010s; standard citation, not re-verified this sweep). 2026 synthesis: Wang, Salvati, Arvidsson-Shukur, Braasch, Murch, Yunger Halpern, "Quantum metrology enhanced by effective time reversal," arXiv:2601.20952 — unifies echo metrology, WVA, simulated CTCs, and indefinite causal order as "time-reverse metrology." That review is the bridge from this topic back to §4.
- **Tri-state:** [measured] weak-value statistics and contextuality-violation witnesses; [mechanism] Kirkwood-Dirac quasiprobability algebra; [interpretation-overreach] weak values as the real properties of individual systems.

### 5b. "The past of a quantum particle"
- **The claim:** Danan, Farfurnik, Bar-Ad, Vaidman, "Asking photons where have they been," PRL 111, 240402 (2013) (arXiv:1304.7469, verified) — weak traces in a nested Mach-Zehnder indicate "the past of a photon is not a set of continuous trajectories," photons leaving weak traces in arms they "couldn't have reached." Vaidman's ontology: the particle's past = overlap of forward and backward evolving wavefunctions, plus "secondary presence" (PRA 87, 052104 (2013), arXiv:1304.7474; PRA 89, 024102 (2014), arXiv:1312.7566).
- **The critics (2015–2026 window):** Englert et al., "Past of a quantum particle revisited" — answered by Peleg & Vaidman, PRA 99, 026103 (2019) (arXiv:1805.12171); Hance, Rarity & Ladyman (2023) attack on weak-value histories — answered by Vaidman (arXiv:2305.13828). Earlier anti-realist position (Sokolovski school): weak values are not properties, and asking "where it was" before detection is meaning-free. The debate is LIVE and purely interpretive — both sides agree on all detector statistics.
- **Tri-state:** [measured] the weak-trace detector clicks in nested interferometers; [mechanism] two-boundary conditional expectation (same algebra as §1a/§1d); [interpretation-overreach] the headline "photons told us where they have been."
- **$0–100 fleet translation:** the weak-value math is a conditional-estimator toolkit — numpy-able, genuinely useful for metrology design per the 2026 review — and useless as a time machine; treat any "measured the past of a particle" claim as description-order rhetoric until a marginal moves (it never does).

<!-- SWEEP LOG -->
- [x] §1 Retrocausal interpretations (TSVF, TI, all-at-once/Wharton, PPS)
- [x] §2 Delayed-choice family (Wheeler, entanglement swapping, cosmic)
- [x] §3 Time interfaces in metamaterials (temporal reflection/refraction, time crystals)
- [x] §4 CTC computation (Deutsch, Aaronson critique, simulations)
- [x] §5 Weak values / "past of a quantum particle"
- [x] Closing: honest hierarchy + 3 must-read papers

---

## THE HONEST HIERARCHY

**Instrument-grade (built, measured, replicated 2015–2026):**
1. Bell violations with late/cosmically-sourced settings (stars 2017, quasars 2018 — freedom-of-choice closure back ~7.8–12.1 Gyr).
2. Delayed-choice entanglement swapping (Ma 2012) and Wheeler choice at satellite scale (Vedovato 2017) — correlations at detection, post-selected.
3. Temporal reflection and time refraction at switched interfaces (Moussa 2023 microwave → Segal/Segev 2026 optical), momentum bandgaps, temporal cavities.
4. Discrete time crystals on ≥5 platforms (ions, diamond, NMR, NV, superconducting, 2017–2022).
5. Anomalous weak values + contextuality-witness violations (photons 2016, neutrons 2017, superconducting 2023).
6. Lab circuits implementing the *mathematics* of CTC models (photonic 2014; superconducting phase estimation 2024).

**Mechanism-level (load-bearing math, no differential predictions):**
- No-signaling from postselection — the universal firebreak under §1, §2, §5.
- ABL rule + Kirkwood-Dirac/weak-value algebra.
- Time-domain scattering (frequency conjugation, energy from the modulation pump).
- Deutsch fixed-point vs P-CTC teleportation algebra; Aaronson-Watrous PSPACE ceiling (even granting CTCs, no oracle).

**Interpretation (permitted readings, empirically equivalent to standard QM):**
- TSVF ontology; Transactional/RTI absorber ontology; all-at-once retrocausal reformulations (Argaman–Wharton); "past of a particle" as weak traces; weak-value realism.

**Poetry (kill on sight):**
- "Message from the future," "time travel demonstrated/simulated," "cosmic feedback," "observers deciding the past," "photons asked where they've been" as fact, "temporal mirror reflects into the past," retrocausal steering of outcomes. Every 2023 "scientists simulate time travel" headline maps to §4: postselection statistics inside a model.

**Bottom line for the moonshot lane:** nothing measured, ever, moves information backward. What survives is (a) a serious retrocausal *reformulation* program (Wharton/Argaman) with zero instrument angle, (b) real time-boundary wave physics whose "reversal" is frequency conjugation, and (c) complexity results capping any hypothetical CTC power at PSPACE. For a $0–100 fleet: simulate, audit claims, and file the firebreak (no-signaling-from-postselection) on every retrocausal artifact before promotion.

## THE 3 PAPERS THIS LANE MUST READ IN FULL

1. **N. Argaman & K. B. Wharton, "Colloquium: Bell's theorem and locally mediated reformulations of quantum mechanics," Rev. Mod. Phys. 92, 021002 (2020)** (arXiv:1906.04313) — the only intellectually serious standing for retrocausality; the lane's theory floor. Read before touching any TSVF/TI material.
2. **H. Moussa et al., "Observation of temporal reflection and broadband frequency translation at photonic time interfaces," Nature Physics 19, 863 (2023)** (arXiv:2208.07236) — the real "time boundary" physics; the honest definition of what "time reversal" means in an experiment.
3. **S. Aaronson & J. Watrous, "Closed timelike curves make quantum and classical computing equivalent," Proc. R. Soc. A 465, 631 (2009)** (arXiv:0808.2669) — the ceiling for CTC power; kills the "time travel = oracle" fantasy at the complexity level, and the paper behind every "time travel simulation" press release's fine print.

---
*Receipt complete 2026-09-16. Sources: WebSearch + arXiv API (free) only. No git. Verification notes: all load-bearing arXiv IDs above were resolved against the arXiv API this sweep; two guessed IDs were caught wrong in-flight (1311.2959 → correct CTC sim ID 1501.05014; Lloyd P-CTC 1005.2213 → 1005.2219) — tri-state discipline applies to citations too. Items marked "standard citation, not re-verified this sweep": Choi et al. Nature 543, 221 (2017); Mi et al. Nature 601, 531 (2022); Ferrie–Combes WVA critique.*
