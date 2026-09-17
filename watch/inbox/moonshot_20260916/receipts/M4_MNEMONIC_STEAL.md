# M4 — MNEMONIC.AI STEAL RECEIPT

- **Lane:** moonshot_20260916 / M4
- **Writer:** zcode-mnemonic-20260916
- **Date:** 2026-09-16
- **Mission:** Operator-named source for "deep learning and decision prediction for recreation of convincing thought processes using physical brain structure mapped to ocean models." Fetch all four URLs, map to our ractor engine / OCEAN Laplacian witness design, file in ledger.
- **Constraints honored:** no git, no paid APIs, WebFetch only. All four pages fetched clean — no 403, no bot-block, no mirrors needed.
- **Coordination:** M1_MNEMONIC_PRIORART.md (sibling lane) already resolved the homepage; M4 independently confirmed its findings and adds the two publications + learn hub, which M1 had not fetched.

## FETCH LOG

| # | URL | Status | Notes |
|---|-----|--------|-------|
| 1 | https://mnemonic.ai/ | 200 OK | MarTech SaaS; matches M1's read exactly |
| 2 | https://mnemonic.ai/research/learn/ | 200 OK | 3 articles, "Model Training" filter EMPTY |
| 3 | https://mnemonic.ai/research/publications/digital-twin-fidelity/ | 200 OK | Real self-benchmark with real numbers |
| 4 | https://mnemonic.ai/research/publications/difference-machine/ | 200 OK | Wennker, 2026-06-17, tipping-point engine |

## FINDINGS

### 1. Homepage — what the company is
Mnemonic AI is a **marketing intelligence SaaS vendor** ("Unify Your Data. Understand Your Customers. Automate Your Growth."). Products: **Data Hub · AI Personas · Digital Twin · Digital Panel · Marketing Analytics**. OCEAN line confirmed verbatim: "Uncover deep psychographic insights with OCEAN personality analysis." Whose model: proprietary AI implementing the academic **OCEAN/Big-Five** framework; no third-party LLM attributed. Marketing claims (ROAS +275%, revenue +33%) are unverified testimonials. **No brain-structure content anywhere** — the "physical brain structure mapped to ocean models" framing is the operator's layer, not theirs (M1 agrees).

### 2. /research/learn/ — the "research program"
A **free article library, 3 articles total**, all by Phil Wennker: Vector Databases (2025-10-29), "The OCEAN Model Revisited … Across Psychology, Education, Marketing and Human Resources" (2025-10-28), RAG vs Fine-Tuning (2025-10-28). The "Model Training" topic filter exists and is **empty**. Verdict: education-as-marketing, not a research program. The OCEAN explainer is their only "neuroscience" content.

### 3. digital-twin-fidelity — the real payload
"MNAI Digital Twin: Fidelity on Twin-2K-500" — headline: "MNAI beats the published state of the art at predicting real people."
- **What twin:** of a **person** (customer). "Give it a person's profile and it predicts how that specific individual would answer a new question: their choices, judgments, and preferences." Personas built from prior survey waves + demographics + psychometrics.
- **Fidelity metric:** normalized accuracy against a **human test–retest ceiling** (self-inconsistency caps any predictor), with **partial credit** for near-misses (distance normalized by answer-scale range). Headline 𝒩 = raw accuracy ÷ human ceiling.
- **Measured:** Twin-2K-500 (N=2,058 people, 191,406 held-out answers, temperature-0): MNAI raw 74.2% (±0.15) vs human ceiling 83.4% (±0.14) → **𝒩 = 89.0%** [88.66, 89.40] (cluster bootstrap, 4,000 draws). By topic: reasoning/judgment 93.8% of ceiling, economic choices 84.0%. Strict exact-match: 81% of ~71% ceiling.
- **Anchors:** Park et al. 2024 (arXiv:2411.10109, "Generative Agent Simulations of 1,000 People", ~85% claim) and Toubia et al. 2025 dataset. They report reproducing published numbers (ceiling 0.831 vs 0.827; reference LLM twin 0.746 vs 0.737).
- **Caveats:** vendor self-benchmark with a "Book A Strategy Call" CTA; partial-credit convention is theirs; single deterministic run (no run-to-run variance); not peer-reviewed.

### 4. difference-machine — the mechanism payload
"Difference Machine: modeling the moment a population tips" (Phil Wennker, 2026-06-17; engine at dfmchn.com). "People do not change their minds one at a time. They change all at once."
- **What computes differences:** an engine that models how a population moves between behavioral states under pressure, using **only public language** (reviews, comments, open discussion) — unprompted text chosen to dodge survey framing effects.
- **Mechanism:** (1) pressures learned from the corpus, not imported; (2) **"Pressures do not add up independently"** — compounding interactions decide hold vs tip; (3) states: **settled → actively reconsidering → leaving**, plus permanent states on either side; (4) forward simulation — "a flight simulator for a population"; (5) **determinism as the reliability contract**: same inputs, same result, bounded values, only valid transitions.
- **Case study:** 377,487 public comments, zero internal data, reconstructed a subscription service's churn structure — reversible churn ≈ **6×** the permanent churn (linked to a Netflix stress test report). No dataset or code released.

## STEAL MAP (their terms → ours)

1. **Their digital twin is of a PERSON, and their fidelity metric is exactly the one our ractor engine lacks.** The metric shape: *fidelity = fraction of the human's own test–retest consistency ceiling achieved on held-out judgments, partial credit for near-misses, temperature-0 determinism*. Never report raw % (meaningless without the ceiling). For "convincing thought processes" this is the honest eval: our witness is convincing if it matches a person's judgments as well as the person matches their own retest. **Steal the metric wholesale — it is eval design we would otherwise have to invent.**
2. **Their difference/decision mechanism is our Laplacian coupling argument in marketing clothes.** OCEAN conditioning appears in their product line (personas), but the publication-level mechanism is: corpus-derived pressures that interact non-additively ("do not add up independently" = off-diagonal coupling terms in our OCEAN-parameterized Laplacian, where OCEAN traits set diffusion parameters), a three-state transition taxonomy (settled / reconsidering / leaving = our witness states and threshold crossings), and a determinism contract (same inputs → same result = our witness reproducibility requirement). Their implementation is a black-box LLM over text; ours is explicit graph dynamics. **Steal the state model and the determinism contract, not the implementation.**
3. **Claim vs verifiable.** Verifiable: arXiv:2411.10109 is real; their reproduction of published ceiling numbers is stated with method (cluster bootstrap); the dataset is credited (Toubia et al. 2025). Weak/claim-only: the fidelity benchmark is vendor math with their own partial-credit convention and one run; Difference Machine is a single case study, no released data or code; "Model Training" research filter is empty; ROAS numbers are testimonials. Their "research" is a moat-claim wrapped around two artifacts.
4. **Honest framing correction for the operator:** nothing on the site supports "physical brain structure." OCEAN = Big Five personality; the two publications are behavioral/statistical. The brain-graph layer of our design remains OURS (M3's Laplacian math) — mnemonic.ai supplies the OCEAN-conditioning precedent, the person-twin business case, and the eval discipline.

## LEDGER FILING (all four, via mag.link_library)

- REGISTERED: https://mnemonic.ai
- REGISTERED: https://mnemonic.ai/research/learn
- REGISTERED: https://mnemonic.ai/research/publications/digital-twin-fidelity
- REGISTERED: https://mnemonic.ai/research/publications/difference-machine
- Writer: `zcode-mnemonic-20260916`

## STEAL TABLE

| What we take | From where | What it costs us |
|---|---|---|
| Ceiling-normalized fidelity metric (𝒩 = raw ÷ human test–retest ceiling, partial credit, temp-0) | digital-twin-fidelity publication | Nothing but citation (Park et al. 2024 + Mnemonic Labs) |
| Held-out-answer eval protocol shape (N≈2K people, ~190K answers, per-topic ceiling breakdown) | digital-twin-fidelity publication | Nothing but citation |
| Three-state tipping taxonomy: settled → reconsidering → leaving (+ permanent endpoints) | difference-machine publication | Nothing but citation |
| "Pressures do not add up independently" as prior art for Laplacian off-diagonal coupling | difference-machine publication | Nothing but citation |
| Determinism contract: same inputs → same result, bounded values, valid transitions only | difference-machine publication | Nothing but citation |
| Vocabulary: "digital twin of a person", "fidelity of ceiling", "flight simulator for a population" | both publications | Nothing; free framing for receipts and docs |
| Proof the niche pays (MarTech SaaS selling person-twins + tipping engines) | homepage | Nothing |
| Their architecture (LLM answer-prediction SaaS, black-box corpus model) | — | NOT STOLEN — wrong mechanism for us; we need explicit local dynamics, not another hosted LLM |

## VERDICT

**Our ractor engine is NOT a reinvention of their product — it is a new composition.** They sell OCEAN-conditioned LLM answer-prediction over survey data plus a black-box population model; we build an explicit OCEAN-parameterized Laplacian witness with local determinism. What they handed us is the part we had not finished: the fidelity metric (score against the human's own retest ceiling) and the state taxonomy + determinism contract. Steal their metrics and vocabulary, cite Park et al. 2024 as the academic anchor, and keep the brain-graph math — on mechanism we are ahead of them; on eval discipline they taught us the test.
