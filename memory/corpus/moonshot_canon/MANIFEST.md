# MANIFEST — moonshot physics canon (retrocausal steering program)

- **Filed:** 2026-09-16 · **Lane:** operator moonshot 20260916, wave F5
- **Receipt:** `watch/inbox/moonshot_20260916/receipts/F5_PHYSICS_CANON.md` (authoritative fetch log)
- **Contents:** 20 files — 9 Feynman Vol III chapters (md), 10 arXiv PDFs, 1 author-hosted HTML lecture
- **Fetch discipline:** free + legal sources only (Caltech open-access lecture site via reader proxy,
  arXiv, author's own course site). Every arXiv ID verified against the arXiv API (title + authors)
  before download. SHA-256 recorded per file. No paywall circumvention; gaps recorded, not silently
  skipped.

## feynman/ — Feynman Lectures on Physics, Vol. III (New Millennium Edition, © Caltech)

Free-to-read online at feynmanlectures.caltech.edu. Direct curl is Cloudflare-challenged; Internet
Archive was offline during the fetch window. Transcribed via r.jina.ai reader proxy into markdown
(chapter text, figures as image links, equations preserved). Raw-HTML fidelity is NOT claimed —
these are reading copies. Re-fetch from Caltech directly if byte fidelity ever matters.

| File | Chapter | Source | SHA-256 (first 16) |
|---|---|---|---|
| jm_III_01.md | Ch. 1: Quantum Behavior | feynmanlectures.caltech.edu/III_01.html | 1a4e7e35dc65e240 |
| jm_III_02.md | Ch. 2: The Relation of Wave and Particle Viewpoints | …/III_02.html | e4e07d2c6de05d80 |
| jm_III_03.md | Ch. 3: Probability Amplitudes | …/III_03.html | fed43e72843b1b21 |
| jm_III_04.md | Ch. 4: Identical Particles | …/III_04.html | c035cabaa279c193 |
| jm_III_05.md | Ch. 5: Spin One | …/III_05.html | 92beb82bc1abbd80 |
| jm_III_06.md | Ch. 6: Spin One-Half | …/III_06.html | b8dd801b0f36415d |
| jm_III_07.md | Ch. 7: The Dependence of Amplitudes on Time | …/III_07.html | 5c4da022a1ef0ec3 |
| jm_III_08.md | Ch. 8: The Hamiltonian Matrix | …/III_08.html | 1113d24526472b05 |
| jm_III_09.md | Ch. 9: The Ammonia Maser | …/III_09.html | a70e379d69d4a16a |

## papers/ — TT1-cited literature (arXiv, free + legal)

| File | Paper | arXiv ID | Published as | SHA-256 (first 16) |
|---|---|---|---|---|
| aharonov_vaidman_TSVF_updated_review_2001.pdf | Aharonov & Vaidman, "The Two-State Vector Formalism of Quantum Mechanics: an Updated Review" | quant-ph/0105101 | Time in Quantum Mechanics, Lect. Notes Phys. 733 (2008) — the TSVF chapter | ec624b268f576b53 |
| kastner_TI_evolution_overview_2016.pdf | Kastner, "The Transactional Interpretation and its Evolution into the 21st Century: An Overview" | 1608.00660 | Quanta 6(1) (2017) | 97b2ec6e4f8924e6 |
| wharton_timesymmetric_boundary_conditions_2010.pdf | Wharton, "Time-Symmetric Boundary Conditions and Quantum Foundations" | 1003.4273 | Symmetry 2(1) (2010) | 87e42841e11ee1ab |
| wharton_new_class_retrocausal_models_2018.pdf | Wharton, "A New Class of Retrocausal Models" | 1805.09731 | (2018 preprint, single author: Ken Wharton) | 4f8a59812ceb127f |
| wharton_argaman_bell_locally_mediated_RMP_2019.pdf | Wharton & Argaman, "Bell's Theorem and Locally-Mediated Reformulations of Quantum Mechanics" | 1906.04313 | Rev. Mod. Phys. 92, 021002 (2020) Colloquium | 844984968ac8179c |
| ma_delayedchoice_entanglement_swapping_2012.pdf | Ma, Zotter, Kofler, Ursin, Jennewein, Brukner, Zeilinger, "Experimental delayed-choice entanglement swapping" | 1203.4834 | Nature Physics 8, 479 (2012) | 82d39acf6171dd56 |
| megidish_entanglement_never_coexisted_2013.pdf | Megidish, Halevy, Shacham, Dvir, Silberberg, "Entanglement Between Photons that have Never Coexisted" | 1209.4191 | Phys. Rev. Lett. 110, 210403 (2013) | 7078f1c1f7427b0f |
| moussa_temporal_reflection_photonic_time_interfaces_2023.pdf | Moussa et al., "Observation of Temporal Reflection and Broadband Frequency Translation at Photonic Time-Interfaces" | 2208.07236 | Nature Physics 19, 863 (2023) — incl. supplementary | eab0233b1914f037 |
| vaidman_past_of_quantum_particle_2013.pdf | Vaidman, "The past of a quantum particle" | 1304.7474 | PNAS 110, 1161 (2013) | d2d5603c3c8ea954 |
| aaronson_watrous_CTC_quantum_classical_equivalent_2008.pdf | Aaronson & Watrous, "Closed Timelike Curves Make Quantum and Classical Computing Equivalent" | 0808.2669 | Proc. R. Soc. A 465, 631 (2009) | eb7674b2b1ff0515 |
| aaronson_time_travel_lecture19.html | Aaronson, "PHYS771 Lecture 19: Time Travel" (the CTC lecture notes: postselected QM, Deutschian CTCs) | — | scottaaronson.com/democritus/lec19.html (author's own site) | 0607d6f8dd747d08 |

## Gaps and refusals (recorded, not hidden)

- **Deutsch 1991, "Quantum mechanics near closed timelike lines" (Phys. Rev. D 44, 3197):** NOT
  fetched. Pre-arXiv; publisher paywalled; no author-hosted open copy reachable (daviddeutsch.org.uk
  connection failed twice in window); Academia.edu copies rejected (account-gated, unclear
  authorization). Covered indirectly by Aaronson-Watrous (mechanics of D-CTCs) and Aaronson
  Lecture 19 (the lecture-grade exposition of Deutsch's model).
- **Peres 2000, "Delayed choice for entanglement swapping" (J. Mod. Opt. 47, 139):** not on arXiv
  (API search empty); no legal open copy. Covered by the Ma 2012 experiment that realized it.
- **Zhao et al. PRL 2019 extension:** could not confirm the exact arXiv record via the title/abs
  searches tried in this window; left out rather than fetched by guess. Megidish 2013 covers the
  never-coexisted claim.
- **Aharonov & Vaidman chapter:** satisfied by quant-ph/0105101, which IS the arXiv version of the
  LNP 733 chapter — one fetch, both targets.
- **NIST DLMF:** evaluated and ruled OUT of scope — the canon leans on amplitude algebra,
  two-boundary formalism, and time-interface electrodynamics, none of which need DLMF special
  functions beyond what the papers themselves state. A math annex would be padding, not canon.

## Reading order (the moonshot's required three)

1. `feynman/jm_III_01..09.md` — Feynman Vol III ch. 1–9: the language (amplitudes, spin,
   time-dependence, Hamiltonian matrix).
2. `papers/aharonov_vaidman_TSVF_updated_review_2001.pdf` — the two-state vector formalism: what
   two boundary conditions actually buy you.
3. `papers/wharton_argaman_bell_locally_mediated_RMP_2019.pdf` — the honest retrocausal framing:
   where the math carries the retro-language and where only the poetry does.
